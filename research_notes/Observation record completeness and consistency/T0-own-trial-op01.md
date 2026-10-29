# Own trial on OP-01: extent register and pair selection

**Label: own trial.** Script: `own_trial_op01.py` in this folder, stdlib only,
run as `python3 -I own_trial_op01.py OP-01.md` (Python 3.14.2) on
`haalfi/remote-store` `sdd/observe/records/OP-01.md` at `eb08d990e`, fetched
from raw.githubusercontent.com.

## Input and known defect set

- Blind input: the Session, Environment and Decisions sections (lines 1 to
  959). Checked: the Decisions section holds no reference to O14 to O44 and no
  "Amended by" line, so the checks see nothing the review found.
- Known defect set: open items O14 to O44, parsed only after the checks ran.
  14 of them have the form "a reopen/note/gap of Dx ... against Dy", giving
  **27 known defect pairs** (decision × decision). Items against backends
  (O19 Windows, O21 S3, O43 NFS), gaps without a second decision (O24, O25,
  O37, O39, O44) and log-fidelity notes (O40) are not pairs.
- The set is **incomplete**: RFC-0028 says every reader run raised candidates
  outside audit-025, left unverified in BK-485's dossier, and a later round
  still found new items. Recall below is recall of the known set only.

## Check A: an extent register (mechanical)

Every sentence of a Decision, Options or Recommendation bullet that contains
an extent word (only, every, never, no other, nothing, none, all, always,
each) or lists at least three failure categories.

- Size: **114 sentences in 42 of 44 decisions.** It is a work list for a
  reader (each claim against each decision that might add a member), not a
  detector: it does not decide anything.
- Seven known extent-shaped defects, by reading O14 to O44:

| Item | Decision, claim | In register |
|---|---|---|
| O14 | D35 "only" read-phase list | yes |
| O26 (G5) | D35 open-call list | yes |
| O39 | D35 open-call list, more members | yes |
| O31 | D25 "only for API mutations" | yes |
| O28 | D22 "the read that needs it fails with the changed category" | **no**: an unconditional rule with no extent word |
| O33 | D34 table row "E1 to E5 against a pinned stream \| changed" | **no**: a table row, not a sentence |
| O37 | D38 caller-level table lacks rows | **no**: a table read as complete |

- So a lexical register caught the four prose claims with an extent word and
  missed all three that were an **implicit universal** (a rule stated without
  a quantifier) or a **table read as complete**. *Inference:* a register must
  also list (i) every table, with its row domain declared, and (ii) every
  unconditioned rule ("X fails with C") as a universal over its condition.
  That is a structured extraction (T2), not a lexical one.

## Check B: which pairs does the authors' consistency check cover?

For each decision, the decisions its Consistency check names; for each pair,
the shared domain vocabulary (Environment rows, steps s1 to s4, categories,
stream states, methods, named mechanisms such as resume, pin, T_connect).

- 946 decision pairs. The consistency checks name **61 pairs**; **4 of the 27
  known defect pairs** are among them: (12,14), (12,28), (22,42), (34,35).
  Each of those four still let the defect through: a named pair was checked
  for part of the text only (audit-025 class 1, measured here at 4/27
  covered and 0/4 caught).
- Pairs where either decision cites the other anywhere: 97, holding 7 known.
- Candidates = pairs sharing ≥ k vocabulary terms and named by no check,
  unioned with the citation graph:

| k | candidates | union to judge | known pairs covered |
|---|---|---|---|
| 1 | 885 | 946 | 27/27 |
| 2 | 296 | 368 | 24/27 |
| 3 | 116 | 200 | 17/27 |
| 4 | 36 | 127 | 13/27 |
| 5 | 22 | 116 | 10/27 |

- Known pairs with only one shared term: (1,12), (1,13) (D1's "both forms
  behave alike" against a timeout bound) and (28,33) (descriptor exhaustion
  typed two ways). These are conflicts by a **general clause** (parity, a
  typing principle) that shares no specific vocabulary with what it governs.

## What this says

- *Inference:* scoping the whole-record re-check by shared vocabulary does
  not pay much. Keeping 89% of the known pairs (k = 2) still needs 368 of 946
  pairs judged (39%); the misses are the general clauses. A re-check should
  run **every general clause** (D1 parity, D27 typing principle, D33's
  reason, D10's frame) against every decision, and pairs by vocabulary
  otherwise.
- *Inference:* author-written consistency checks covered 15% of the known
  defect pairs (4/27). This measures RFC-0028's class 1 directly.
- Limits: one record, one known set that is incomplete and was itself found
  by reviewers who read citations, so it may be biased towards pairs a
  reader links by vocabulary. Vocabulary lists were written by the trial's
  author after reading the open items. That is a leak, which favours check B.
  No LLM was run in this trial; it measures what a mechanical step selects,
  not what a judge then finds.

## Raw output

```
decisions parsed: 44
== Check A: extent register, 114 sentences in 42 decisions
  O14: D35 'only': IN REGISTER
  O26: D35 'surface from the open': IN REGISTER
  O39: D35 'surface from the open': IN REGISTER
  O31: D25 'only for API mutations': IN REGISTER
  O28: D22 'changed category': missed
  O33: D26 'not promised': missed
  O37: D38 'Caller-level': missed
== Check B: 946 decision pairs; 14 open items name 'Dx against Dy', 27 known defect pairs
  pairs named by some consistency check: 61; known pairs among them: 4 [(12, 14), (12, 28), (22, 42), (34, 35)]
  pairs where one decision cites the other anywhere: 97; known among them: 7
  k | candidates | known in candidates | known in checked | known found by candidates or cite-graph
  1 |        885 |                  23 |                4 | 27/27 (judge 946)
  2 |        296 |                  20 |                4 | 24/27 (judge 368)
  3 |        116 |                  10 |                4 | 17/27 (judge 200)
  4 |         36 |                   6 |                4 | 13/27 (judge 127)
  5 |         22 |                   3 |                4 | 10/27 (judge 116)
```

(The script's O33 target names D26's phrase, but the defect sits in D34's
table row; either way the register holds no table rows.)
