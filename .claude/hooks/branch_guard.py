#!/usr/bin/env python3
"""PreToolUse guard: git and GitHub tools may touch only `main` and the current branch.

Bash (git, also inside `bash -c`):
- no commit or push while on `main`; push only to the current branch;
- fetch/pull must name a branch (a bare fetch reads every branch);
- no --all/--branches/--remotes/--glob/--mirror (except `git branch`);
- no ref argument naming another branch (local, `origin/x`, `x:path`, `a..b`).
GitHub MCP tools on this repo: ref/branch/sha arguments must be allowed branches;
writes never target `main`; no pull requests.

Exit 2 blocks, with the reason on stderr. Branches the user explicitly allowed go one
per line in `.git/claude-allowed-branches`. Guardrail, not a sandbox: raw hashes,
command substitution and plumbing tricks are not caught. Fails open on bad input.
"""
import json
import os
import re
import shlex
import subprocess
import sys

REF_CMDS = {"checkout", "switch", "show", "diff", "log", "merge", "rebase", "cherry-pick",
            "rev-list", "shortlog", "whatchanged", "ls-tree", "cat-file", "archive",
            "restore", "reset", "worktree", "branch", "blame", "grep", "format-patch",
            "rev-parse", "merge-base", "range-diff", "show-branch", "name-rev", "describe"}
ALL_REFS = re.compile(r"--(all|branches|remotes|glob|mirror)(=|$)")
NEW_BRANCH_OPTS = {"-b", "-B", "-c", "-C", "--orphan", "--create", "--force-create"}
BRANCH_CREATORS = {"checkout", "switch", "branch", "worktree"}
OPTS_WITH_ARG = {"-m", "-F", "-n", "-S", "-G", "--grep", "--author", "--format", "--pretty",
                 "--depth", "-o", "--since", "--until"}
GLOBAL_OPTS_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
WRAPPERS = {"env", "command", "nice", "nohup", "time", "sudo", "exec"}
SHELLS = {"bash", "sh", "zsh", "dash"}
SPECIAL = {"", "HEAD", "FETCH_HEAD", "ORIG_HEAD", "MERGE_HEAD", "@"}
GH_REF_KEYS = ("ref", "branch", "sha", "from_branch", "base", "head")
GH_WRITE_TOOLS = {"create_or_update_file", "push_files", "delete_file", "update_pull_request_branch"}
GH_BLOCKED_TOOLS = {"create_pull_request", "merge_pull_request", "enable_pr_auto_merge"}


def git(cwd, *args):
    r = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


_ctx = {}


def context(cwd):
    """(current branch, known branch names, allowed branch names) for the repo at cwd."""
    if cwd not in _ctx:
        current = git(cwd, "rev-parse", "--abbrev-ref", "HEAD")
        refs = git(cwd, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes")
        known = {r.split("/", 1)[1] if r.startswith("origin/") else r for r in refs.split()}
        allowed = {"main", current}
        gitdir = git(cwd, "rev-parse", "--absolute-git-dir")
        try:
            with open(f"{gitdir}/claude-allowed-branches") as f:
                allowed |= {ln.strip() for ln in f if ln.strip()}
        except OSError:
            pass
        _ctx[cwd] = (current, known - {"origin", "HEAD"}, allowed)
    return _ctx[cwd]


def ref_names(tok):
    """Branch names a ref-ish token refers to (strips ranges, paths, suffixes)."""
    names = []
    for part in re.split(r"\.\.\.?", tok):
        part = part.lstrip("+^").split(":", 1)[0]
        part = re.sub(r"(@\{.*\}|[~^]\d*)+$", "", part)
        for prefix in ("refs/heads/", "refs/remotes/"):
            if part.startswith(prefix):
                part = part[len(prefix):]
        remote = part.startswith("origin/")
        names.append((part[len("origin/"):] if remote else part, remote))
    return names


def unquoted_newlines_to_semicolons(command):
    out, quote, esc = [], None, False
    for ch in command:
        if esc:
            esc = False
        elif ch == "\\" and quote != "'":
            esc = True
        elif quote:
            quote = None if ch == quote else quote
        elif ch in "'\"":
            quote = ch
        elif ch == "\n":
            ch = " ; "
        out.append(ch)
    return "".join(out)


def segments(command):
    """Simple commands of a shell line: split on ; & | ( ), redirections dropped."""
    command = unquoted_newlines_to_semicolons(command)
    try:
        lex = shlex.shlex(command, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        toks = list(lex)
    except ValueError:
        toks = command.split()
    seg, drop_next = [], False
    for t in toks:
        if drop_next:
            drop_next = False
        elif t and set(t) <= set("<>&") and set(t) & set("<>"):  # redirection: >, 2>&1, <
            if seg and seg[-1].isdigit():
                seg.pop()
            drop_next = True
        elif re.fullmatch(r"\d*[<>]+&?\S*", t):  # glued form in fallback split
            continue
        elif t and set(t) <= set(";&|()"):
            if seg:
                yield seg
            seg = []
        else:
            seg.append(t)
    if seg:
        yield seg


def command_words(seg):
    """Drop leading VAR=x assignments and wrappers such as `env` or `timeout 10`."""
    i = 0
    while i < len(seg):
        t = seg[i]
        if re.fullmatch(r"[A-Za-z_]\w*=.*", t) or t in WRAPPERS:
            i += 1
        elif t == "timeout":
            i += 2
        else:
            break
    return seg[i:]


def check_segment(seg, cwd):
    words = command_words(seg)
    if not words:
        return None
    exe = os.path.basename(words[0])
    if exe in SHELLS and "-c" in words[:-1]:
        return check_command(words[words.index("-c") + 1], cwd)
    if exe != "git":
        return None

    args = words[1:]
    while args and args[0].startswith("-"):  # global options
        opt = args[0]
        if opt == "-C" and len(args) > 1:
            cwd = os.path.join(cwd, args[1])
        args = args[2:] if opt in GLOBAL_OPTS_WITH_ARG else args[1:]
    if not args:
        return None
    cmd, rest = args[0], args[1:]
    current, known, allowed = context(cwd)

    if cmd != "branch" and any(ALL_REFS.match(a) for a in rest):
        return f"`git {cmd}` with --all/--branches/--remotes/--glob/--mirror reads every branch"
    if cmd in ("commit", "push") and current == "main":
        return f"`git {cmd}` on main is not allowed; create a research/<kebab-title> branch first"

    opts_with_arg = OPTS_WITH_ARG - {"-n"} if cmd == "push" else OPTS_WITH_ARG  # push -n = dry run
    pos, skip = [], False
    for a in rest:
        if a == "--":
            break
        if skip:
            skip = False
            continue
        if a in NEW_BRANCH_OPTS and cmd in BRANCH_CREATORS:  # next token is a new name, not a read
            skip = True
            continue
        if a.startswith("-"):
            skip = a in opts_with_arg
            continue
        pos.append(a)

    if cmd in ("fetch", "pull"):
        specs = pos[1:]
        if not specs:
            return f"`git {cmd}` without a branch fetches every branch; name it, e.g. `git {cmd} origin main`"
        for s in specs:
            for name, _ in ref_names(s):
                if name not in allowed:
                    return f"`git {cmd}` of branch `{name}`"
        return None
    if cmd == "push":
        for s in pos[1:]:
            dst = s.split(":", 1)[-1].lstrip("+")
            dst = dst[len("refs/heads/"):] if dst.startswith("refs/heads/") else dst
            if dst not in ("HEAD", current) and dst not in allowed - {"main"}:
                return f"`git push` to `{dst}`; push only your own branch `{current}`"
        return None
    if cmd in REF_CMDS:
        for a in pos:
            for name, remote in ref_names(a):
                if name in SPECIAL or name in allowed:
                    continue
                if remote or name in known:
                    return f"`git {cmd}` reads branch `{name}`"
    return None


def check_command(command, cwd):
    if "git" not in command:
        return None
    for seg in segments(command):
        reason = check_segment(seg, cwd)
        if reason:
            return reason
    return None


def this_repo(cwd):
    m = re.search(r"([^/:]+)/([^/]+?)(\.git)?/?$", git(cwd, "remote", "get-url", "origin"))
    return (m.group(1).lower(), m.group(2).lower()) if m else None


def check_github(tool, inp, cwd):
    if (str(inp.get("owner", "")).lower(), str(inp.get("repo", "")).lower()) != this_repo(cwd):
        return None
    if tool in GH_BLOCKED_TOOLS:
        return f"`{tool}`: this repo delivers on branches only, never via pull requests"
    current, _, allowed = context(cwd)
    for key in GH_REF_KEYS:
        val = inp.get(key)
        if not isinstance(val, str) or not val or re.fullmatch(r"[0-9a-f]{7,40}", val):
            continue  # raw commit hashes are not checked
        name = val[len("refs/heads/"):] if val.startswith("refs/heads/") else val
        if tool in GH_WRITE_TOOLS and key == "branch" and name == "main":
            return f"`{tool}` writes to main"
        if tool == "create_branch" and key == "branch":
            continue  # the new branch name, not a read
        if name not in allowed:
            return f"`{tool}` with {key}=`{name}`"
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    tool = data.get("tool_name", "Bash")
    inp = data.get("tool_input") or {}
    cwd = data.get("cwd") or "."
    if tool.startswith("mcp__github__"):
        reason = check_github(tool[len("mcp__github__"):], inp, cwd)
    else:
        reason = check_command(inp.get("command", ""), cwd)
    if not reason:
        return 0
    current = context(cwd)[0]
    print(f"Blocked by branch guard: {reason}. Only `main` and your own branch (`{current}`) "
          "may be read or written. Another branch needs the user's explicit permission; "
          "only then add it to .git/claude-allowed-branches.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
