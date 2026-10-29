"""Own trial on OP-01: two mechanical checks, scored against open items O14-O44.

Usage: python3 -I own_trial_op01.py <OP-01.md at eb08d990e>

Blind input: the Environment and Decisions sections only (up to "## Axis
status"), which hold no reference to O14-O44. The Open items section is read
only to build the known defect set, after the checks have run.

Check A, extent register: every sentence in a Decision, Options or
Recommendation bullet that makes a claim of extent ("only", "every", "never",
"no other", "nothing", "none", or a comma list of at least three failure
categories). Scored by whether each known extent defect's decision and phrase
are in the register.

Check B, pair selection: for each pair of decisions, the shared domain
vocabulary (Environment rows, steps, failure categories, stream states,
methods, named mechanisms), and whether either decision's Consistency check
names the other. A pair that shares at least k terms and is named by neither
check is a candidate for a whole-record re-check. Scored by the recall of
known defect pairs ("a reopen of Dx ... against Dy") and the number of pairs
a reader would have to judge.
"""

import itertools
import re
import sys

CATEGORIES = [
    "key refused", "not found", "not an item", "permission denied",
    "authentication failed", "not readable", "unavailable", "timeout",
    "changed", "base category", "caller error", "cancellation", "cancelled",
    "decode",
]
STATES = ["Open", "Exhausted", "Failed", "Closed"]
METHODS = ["read(n)", "readinto", "readline", "chunks", "close()", "read(-1)",
           "context manager", "iterator"]
MECHANISMS = ["resume", "retry", "retries", "pin", "pinned", "If-Match",
              "T_connect", "T_idle", "deadline", "listing", "folder",
              "instant", "buffer", "variation point", "deviation",
              "non-promise", "frame", "lifetime", "handle", "finaliser",
              "descriptor", "tier", "ETag", "version"]
EXTENT = re.compile(
    r"\b(only|every|never|no other|nothing|none|all|always|each)\b", re.I)


def split_sections(text):
    head, _, rest = text.partition("## Axis status")
    open_items = rest.partition("## Open items")[2]
    return head, open_items


def parse_decisions(head):
    decisions = {}
    parts = re.split(r"^### OP-01/D(\d+): .*$", head, flags=re.M)
    for i in range(1, len(parts), 2):
        num = int(parts[i])
        body = parts[i + 1]
        fields = {}
        for m in re.finditer(r"^- \*\*([A-Za-z ]+):\*\*(.*?)(?=^- \*\*|\Z)",
                             body, flags=re.M | re.S):
            fields[m.group(1).strip()] = " ".join(m.group(2).split())
        fields["_all"] = " ".join(body.split())
        decisions[num] = fields
    return decisions


def refs(text):
    out = set()
    for m in re.finditer(r"\bD(\d+)(?:\s+(?:to|and)\s+D?(\d+))?", text):
        a = int(m.group(1))
        if m.group(2) and " to " in m.group(0):
            out.update(range(a, int(m.group(2)) + 1))
        else:
            out.add(a)
            if m.group(2):
                out.add(int(m.group(2)))
    # bare numbers in lists such as "D33, D28 and D38" are caught above;
    # "D21 to D23" expands.
    return out


def vocab(text):
    terms = set()
    for m in re.finditer(r"\bE(\d+)\b", text):
        terms.add("E" + m.group(1))
    for m in re.finditer(r"\bs([1-4])\b", text):
        terms.add("s" + m.group(1))
    for m in re.finditer(r"\bNP(\d+)\b", text):
        terms.add("NP" + m.group(1))
    low = text.lower()
    for t in CATEGORIES + MECHANISMS + METHODS:
        if t.lower() in low:
            terms.add(t.lower())
    for t in STATES:
        if re.search(r"\b" + t + r"\b", text):
            terms.add("state:" + t)
    return terms


def extent_register(decisions):
    reg = []
    for num, f in decisions.items():
        for field in ("Decision", "Options", "Recommendation"):
            for sent in re.split(r"(?<=[.;:])\s+", f.get(field, "")):
                cats = [c for c in CATEGORIES if c in sent.lower()]
                if EXTENT.search(sent) or len(cats) >= 3:
                    reg.append((num, field, sent))
    return reg


def known_defects(open_items):
    items = {}
    for m in re.finditer(r"^- `OP-01/O(\d+)`:(.*?)(?=^- `OP-01/O|\Z)",
                         open_items, flags=re.M | re.S):
        n = int(m.group(1))
        if 14 <= n <= 44:
            items[n] = " ".join(m.group(2).split())
    pairs = {}
    for n, txt in items.items():
        m = re.match(r"\s*(?:a|three)? ?(?:reopen|note|gap)s? (?:of|on|in) "
                     r"(?:the )?(?:OP-01/)?(.*?)\bagainst\b(.*?)[(.]", txt)
        if not m:
            continue
        left = refs(m.group(1))
        right = refs(m.group(2))
        ps = {tuple(sorted((a, b))) for a in left for b in right if a != b}
        if ps:
            pairs[n] = ps
    return items, pairs


# Known extent defects: (open item, decision whose extent claim fails, a
# phrase of the claim). Chosen by reading O14-O44 for "only", "list", "four",
# "never" claims; see the notes file.
EXTENT_TARGETS = [
    (14, 35, "only"),            # D35's read-phase list
    (26, 35, "surface from the open"),  # G5: open-call list
    (39, 35, "surface from the open"),  # same list, more members
    (31, 25, "only for API mutations"),
    (28, 22, "changed category"),  # D22's "fails with the changed category"
    (33, 26, "not promised"),    # D34's table row vs D26 (table, not prose)
    (37, 38, "Caller-level"),    # D38's caller-level table lacks rows
]


def main(path):
    text = open(path, encoding="utf-8").read()
    head, open_items = split_sections(text)
    decisions = parse_decisions(head)
    n = len(decisions)
    print(f"decisions parsed: {n}")

    # Check A
    reg = extent_register(decisions)
    print(f"\n== Check A: extent register, {len(reg)} sentences "
          f"in {len({r[0] for r in reg})} decisions")
    for item, d, phrase in EXTENT_TARGETS:
        hit = [r for r in reg if r[0] == d and phrase.lower() in r[2].lower()]
        print(f"  O{item}: D{d} '{phrase}': "
              f"{'IN REGISTER' if hit else 'missed'}")

    # Check B
    voc = {d: vocab(f["_all"]) for d, f in decisions.items()}
    named = {d: refs(f.get("Consistency check", "")) for d, f in
             decisions.items()}
    cited = {d: refs(f["_all"]) - {d} for d, f in decisions.items()}
    _, pairs = known_defects(open_items)
    known = set().union(*pairs.values()) if pairs else set()
    print(f"\n== Check B: {n * (n - 1) // 2} decision pairs; "
          f"{len(pairs)} open items name 'Dx against Dy', "
          f"{len(known)} known defect pairs")
    for o, ps in sorted(pairs.items()):
        print(f"  O{o}: {sorted(ps)}")

    checked = {tuple(sorted((a, b))) for a in named for b in named[a]
               if a != b and b in decisions}
    print(f"\n  pairs named by some consistency check: {len(checked)}; "
          f"known pairs among them: {len(known & checked)} "
          f"{sorted(known & checked)}")
    any_cite = {tuple(sorted((a, b))) for a in cited for b in cited[a]
                if b in decisions}
    print(f"  pairs where one decision cites the other anywhere: "
          f"{len(any_cite)}; known among them: {len(known & any_cite)}")

    print("\n  k = shared terms; candidates = pairs sharing >= k terms and "
          "named by no check")
    print("  k | candidates | known in candidates | known in checked | "
          "known found by candidates or cite-graph")
    for k in range(1, 9):
        cand = set()
        for a, b in itertools.combinations(sorted(decisions), 2):
            if (a, b) in checked:
                continue
            if len(voc[a] & voc[b]) >= k:
                cand.add((a, b))
        union = cand | any_cite
        print(f"  {k} | {len(cand):10d} | {len(known & cand):19d} | "
              f"{len(known & checked):16d} | {len(known & union)}/{len(known)}"
              f" (judge {len(union)})")
    missed = {p: len(voc[p[0]] & voc[p[1]]) for p in known}
    print("\n  shared-term count per known pair:",
          dict(sorted(missed.items())))


if __name__ == "__main__":
    main(sys.argv[1])
