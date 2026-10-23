#!/usr/bin/env python3
"""PreToolUse(Bash) guard: git may touch only `main` and the current branch.

Blocks (exit 2, reason on stderr):
- commit or push while on `main`; push to any ref other than the current branch;
- fetch/pull without an explicit branch (that fetches every branch);
- --all / --mirror / --remotes on history commands;
- any ref argument naming another branch (local, `origin/x`, `x:path`, `a..b`).

Branches the user explicitly allowed go one per line in `.git/claude-allowed-branches`.
Guardrail, not a sandbox: raw hashes and plumbing tricks are not caught.
"""
import json
import re
import shlex
import subprocess
import sys

HISTORY_CMDS = {"log", "show", "diff", "fetch", "pull", "push", "rev-list", "shortlog", "whatchanged"}
REF_CMDS = {"checkout", "switch", "show", "diff", "log", "merge", "rebase", "cherry-pick",
            "rev-list", "shortlog", "whatchanged", "ls-tree", "cat-file", "archive",
            "restore", "reset", "worktree", "branch", "blame", "grep", "format-patch"}
NEW_BRANCH_OPTS = {"-b", "-B", "-c", "-C", "--orphan", "--create", "--force-create"}
OPTS_WITH_ARG = {"-m", "-F", "--format", "--pretty", "-C", "-c", "--depth", "-o"}
SPECIAL = {"", "HEAD", "FETCH_HEAD", "ORIG_HEAD", "MERGE_HEAD", "@"}


def git(cwd, *args):
    r = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def context(cwd):
    current = git(cwd, "rev-parse", "--abbrev-ref", "HEAD")
    refs = git(cwd, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes")
    known = {r.split("/", 1)[1] if r.startswith("origin/") else r for r in refs.split()}
    allowed = {"main", current}
    gitdir = git(cwd, "rev-parse", "--absolute-git-dir")
    if gitdir:
        try:
            with open(f"{gitdir}/claude-allowed-branches") as f:
                allowed |= {ln.strip() for ln in f if ln.strip()}
        except OSError:
            pass
    return current, known - {"origin", "HEAD"}, allowed


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


def check(seg, current, known, allowed):
    try:
        i = next(k for k, t in enumerate(seg) if t == "git" or t.endswith("/git"))
    except StopIteration:
        return None
    args = seg[i + 1:]
    while args and args[0].startswith("-"):  # global options
        args = args[2:] if args[0] in ("-C", "-c") else args[1:]
    if not args:
        return None
    cmd, rest = args[0], args[1:]

    if cmd in HISTORY_CMDS and any(a in ("--all", "--mirror", "--remotes") for a in rest):
        return f"`git {cmd}` with --all/--mirror/--remotes reads every branch"
    if cmd in ("commit", "push") and current == "main":
        return f"`git {cmd}` on main is not allowed; create a research/<kebab-title> branch first"

    pos, skip = [], False
    for a in rest:
        if a == "--":
            break
        if skip:
            skip = False
            continue
        if a in NEW_BRANCH_OPTS:  # next token is a new branch name, not a read
            skip = True
            continue
        if a.startswith("-"):
            skip = a in OPTS_WITH_ARG
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


def main():
    data = json.load(sys.stdin)
    command = (data.get("tool_input") or {}).get("command", "")
    if "git" not in command:
        return 0
    current, known, allowed = context(data.get("cwd") or ".")
    for seg in segments(command):
        reason = check(seg, current, known, allowed)
        if reason:
            print(f"Blocked by branch guard: {reason}. Only `main` and your own branch "
                  f"(`{current}`) may be read or written. Another branch needs the user's "
                  "explicit permission; only then add it to .git/claude-allowed-branches.",
                  file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
