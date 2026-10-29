# Own trial on OP-01: capture-recapture over two LLM readers

**Label: own trial.** Script: `own_trial_op01_capture.py` in this folder,
stdlib only, run as `python3 -I own_trial_op01_capture.py OP-01.md` on
`sdd/observe/records/OP-01.md` at `eb08d990e`.

## Data

`/observe-review OP-01` (RFC-0028) raised O27 to O44, each naming its source:
reader 1, reader 2 (two unprimed agents with one fixed brief), the primed
review, or BK-485's dossier. The two unprimed readers are the two captures.

| | Items |
|---|---|
| Reader 1 (13) | O27 to O38, O40 |
| Reader 2 (12) | O27 to O33, O35 to O39 |
| Both (11) | O27 to O33, O35 to O38 |
| Union (14) | O27 to O40 |
| Primed review only (4) | O41, O42, O43, O44 |

## Estimates

- Lincoln-Petersen N̂ = 13 × 12 / 11 = **14.2**; Chapman N̂ = 14 × 13 / 12 − 1
  = **14.2**. Estimated remaining for readers of this kind: **0.2**.
- Read as a stopping rule, this says "done". The primed review, a reviewer of
  another kind with other ground (backend source, SDK docs), then found **4
  more** outside both captures (O41 to O44, all class 3), a 29% addition to
  the union. And the readers' known set itself excludes O14 to O26, which
  were already in the record.

## Second data point: RFC-0028 § Evidence

RFC-0028's table runs the reader twice on a copy of the record at `c58ee74`
against six known targets (C1, C2, G5, O14, O15, O16):

- Run 1 found 4 (C1, O14, O15, O16); run 2 found 3 (O14, O15, O16); both 3.
- Lincoln-Petersen N̂ = 4 × 3 / 3 = **4**, against **6** known targets
  (C2 and G5 found by neither run). An underestimate by a third, on a target
  set that is itself a lower bound.

## What this says

- *Inference:* two LLM readers given the same brief behave like correlated
  inspectors: they agree on the easy items (11 of 14) and both miss the same
  hard ones. Positive dependence between captures biases Lincoln-Petersen
  **down**, so the estimate understates what remains; it is known in the
  inspection literature for human teams (see T4 notes) and here shows up at
  n = 2.
- *Inference:* capture-recapture estimates at best the population that
  reviewers **of that kind** can see. Class 3 defects (backend behaviour) and
  class 4 (questions no axis raises) are outside an unprimed reader's
  detectable population by design, so no overlap between such readers can
  estimate them. A stopping rule has to be per reviewer kind and per class.
- Limits: one record, two small samples (14 and 6 items), sources as the
  record states them (not re-verified), readers of one model family.
