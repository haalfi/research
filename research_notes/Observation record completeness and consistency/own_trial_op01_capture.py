"""Own trial on OP-01: capture-recapture over the /observe-review readers.

Usage: python3 -I own_trial_op01_capture.py <OP-01.md at eb08d990e>

O27-O44 each name their source: "reader 1", "reader 2" (or "readers 1 and
2"), "primed", "dossier". The two unprimed readers are the two captures.
Prints Lincoln-Petersen and Chapman estimates of the population the readers
can find, and what the primed review added outside both captures.
"""

import re
import sys


def main(path):
    text = open(path, encoding="utf-8").read()
    open_items = text.partition("## Open items")[2]
    r1, r2, primed = set(), set(), set()
    for m in re.finditer(r"^- `OP-01/O(\d+)`:(.*?)(?=^- `OP-01/O|\Z)",
                         open_items, flags=re.M | re.S):
        n = int(m.group(1))
        if n < 27:
            continue
        src = re.search(r"\(((?:reader|primed)[^)]*)\)",
                        " ".join(m.group(2).split()))
        s = src.group(1) if src else ""
        if re.search(r"reader 1\b|readers 1 and 2", s) or s.startswith(
                "reader 1"):
            r1.add(n)
        if re.search(r"reader 2\b|readers 1 and 2", s):
            r2.add(n)
        if "primed" in s:
            primed.add(n)
        print(f"O{n}: {s}")
    both = r1 & r2
    print(f"\nreader 1: {len(r1)} {sorted(r1)}")
    print(f"reader 2: {len(r2)} {sorted(r2)}")
    print(f"both: {len(both)}; union: {len(r1 | r2)}")
    lp = len(r1) * len(r2) / len(both)
    ch = (len(r1) + 1) * (len(r2) + 1) / (len(both) + 1) - 1
    print(f"Lincoln-Petersen N = {lp:.1f}; Chapman N = {ch:.1f}; "
          f"estimated remaining for readers of this kind = {ch - len(r1 | r2):.1f}")
    only_primed = primed - r1 - r2
    print(f"primed review, outside both readers: {len(only_primed)} "
          f"{sorted(only_primed)}")


if __name__ == "__main__":
    main(sys.argv[1])
