# T4. Stopping rules

The workflow's verification budget dropped every T4 claim. The claims below
were verified against full texts in a separate pass; see
`verification-log.md`.

## 1. Capture-recapture (CR) estimators of remaining defects

### Briand, El Emam, Freimut, Laitenberger, IEEE TSE 26(6):518–540, 2000 — A

Read as NRC report ERB-1084 (2001), which states it was also published in
TSE. Page numbers are the report's.

- Setting: two reading experiments at NASA/GSFC, 1994–95, with
  professionals (12 inspectors, and 13 of 14), ad hoc reading, IEEE 830
  requirements documents.
  - Documents: ATM (29 defects), PG (27 defects) and two NASA functional
    specifications (15 to 18 defects). Two runs each are treated as 8
    documents with 6 to 8 inspectors.
  - Defects were seeded ("reintroduced"), so there were no false positives.
  - Smaller teams were simulated as "virtual inspections": all C(n,k)
    inspector subsets for k = 2 to 6, plus 50 random defect subsets per
    level.
  - "Correct" means RE = (estimate − actual)/actual, judged on the median
    RE with a ±20% bar.
- **"For less than four inspectors and according to our evaluation criterion
  (-20% < RE < 20%), no estimator yields satisfactory results."** (§4.1(b),
  p.17)
- At 3 inspectors, the best estimator, Mh-JE, had median RE **−27%**
  (Table 7: −0.2758). At 2 inspectors, Mh-JE had median RE −52%, M0 −36%
  and Mt −45% (Table 6).
- Chao estimators have an acceptable median at 2 to 3 inspectors but show
  "occasional large overestimation".
- Mth-Chao gives no estimate at k = 2: its formula has a (k − 2)
  denominator. Mh-Chao fails when no defect was found by exactly two
  inspectors. Its failure rate is 12.8% below 4 inspectors, and 20.2% at 4
  inspectors with fewer than 12 defects (Table 5).
- At 4 or more inspectors, Mh-type models had median RE between 5% and 16%
  (unsigned).
- Calibration from historical RE "does not work" (§4.4).
- Recommendation: CR "ought not be used with less than 4 inspectors unless
  shown to work in a particular environment". Miller (1998) found some
  models acceptable at 3 inspectors.
- Caveat in the paper: the data come from "a very mature environment", with
  little variation in inspector ability.
- Human-only evidence.

### Briand, El Emam, Freimut, Laitenberger, ISERN-97-22 — A-workshop / technical report

- An earlier, shorter version of the same study. Abstract: "When the number
  of inspectors is below 4, no model is sufficiently accurate and
  underestimation may be substantial."
- It states the 3-inspector Mh-JE error as ">27%", and gives no hedge on
  the 4-inspector recommendation.

### Petersson, Thelin, Runeson, Wohlin, "Capture-recapture in software inspections after 10 years research", JSS 72, 2004 — A

Read from the author PDF at wohlin.eu.

- The review's summary of common knowledge, p.11: "1. most estimators
  underestimate, 2. Mh-JK is the best estimator for software inspections,
  3. Mh-JK is appropriate to use for 4 reviewers and more ...". Also:
  "at least four to five reviewers should participate in order to make the
  accuracy acceptable". For two reviewers: Mh-JK "is non-robust in the case
  with two reviewers and produces underestimates".
- Application is rare: "Only one published paper reports experience from a
  trial application of capture-recapture in an industrial environment".
- Independence: "there is a risk that the reviewers cooperate, which
  violates the assumption of independence between reviewers". Whether
  inspectors are dependent in practice is unsettled: Ekros et al. against
  Miller 2002. The review does **not** link positive correlation between
  inspectors to underestimation; that link is *Inference* from the
  statistics, not from this source.
- **A published process with stopping decision points:**
  - **Decision point A**, after individual preparation, takes subjective,
    objective and calibrated estimates as input, "not solely" deciding by
    them. Its decisions: terminate and send back; hold a meeting; assign
    more reviewers; continue without a meeting.
  - **Decision point B**, after the meeting, has five decisions, from
    "send back" through "re-inspect with a smaller team" to "good enough".
  - The process tracks the historical accuracy of the estimates and
    compensates for systematic error.

### Eick, Loader, Long, Votta, Vander Wiel, ICSE 1992 — [unreachable]

- The first use of CR on software inspections. No full text could be
  fetched; the free copy's domain is parked. Briand et al. report,
  secondarily, that it used model Mt on 13 inspection meetings, with no
  known true count.

## 2. Disconfirming search (c): result

**Confirmed.** On requirements documents with known defect counts, no CR
estimator was accurate to ±20% at 2 or 3 inspectors. Bias was towards
underestimation: Mh-JE −52% at 2 and −27% at 3. Estimators also fail to
return a value more often with few inspectors, and calibration did not help.
Miller 1998 is the only dissenting data point (some models acceptable at 3),
and it was not read here.

## 3. Can two LLM readers' overlap feed an estimator?

### What the literature says about LLM reviewers

- No peer-reviewed study of CR over LLM reviewers was found. Queries are
  listed in `verification-log.md`.
- Kansal 2026 (C, not peer-reviewed, pre-registered) is the closest
  analogue. It applies CR over LLM judges finding label errors in
  MMLU-Redux. With three current models plus confident learning, the
  intervals were calibrated on planted errors (97% coverage), but on the
  real benchmark the interval ran from 102 to 797, against 181 true errors.
  The estimate was on average 95 errors from the truth, against 46 for the
  plain count. Its conclusion: "well calibrated but not precise enough to be
  useful".
- Calboreanu 2026 (arXiv, C/D): a Lincoln-Petersen "interpretive lens" with
  zero overlap between two models. That gives an unbounded interval. Not
  evidence.

### Own trial (`T0-own-trial-op01-capture.md`)

- Two unprimed LLM readers on OP-01 found 13 and 12 items, 11 of them in
  common. Chapman N̂ = 14.2, so about 0.2 remain. The primed review then
  found 4 more (O41 to O44), outside both captures.
- In RFC-0028's run, 4 and 3 items were found, all 3 of the second run's in
  common, so N̂ = 4 against at least 6 known targets.

### Which assumptions break (*Inference* from the above)

1. **Independence between readers.** Two agents of one model family with
   one brief share their blind spots. That is the settled Knight / Eckhardt
   & Lee point, here at the level of detection. Positive dependence inflates
   the overlap and biases N̂ down. The own trial shows exactly this: 11 of
   14 in common.
2. **Equal catchability** (model M0), or heterogeneity of a known form
   (Mh). Defects differ by class. Class 3 and class 4 defects have detection
   probability near zero for an unprimed reader, by design. CR cannot
   estimate a sub-population that its captures cannot reach.
3. **Number of captures.** k = 2 is the case where every estimator in
   Briand et al. failed the ±20% bar, and where Mth-Chao is undefined.
4. **Closure.** The record changes between rounds: reopens add decisions.
   CR needs the same population across captures, so readers must read the
   same commit.
5. **Matching.** Two reports must be matched as "the same defect".
   Briand's data avoid this with seeded defects. For LLM findings, matching
   is a judged step, and it can raise or lower the overlap.

## 4. Other stopping evidence

- **Discovery-curve methods.** Petersson et al. call DPM (detection profile
  method) the best curve-fitting method. It fits the decline of new finds
  per reviewer. Not read in full here, so it is a lead only.
- **Rounds with zero new finds.** This is the stopping practice the brief
  rejects. The own trial shows why: zero new finds by readers of one kind
  coexisted with 4 finds by another kind.

## 5. Agent applicability

| Option | Evidence | Agents measured | Usable at k = 2 LLM readers? |
|---|---|---|---|
| CR, Mh-JK | A, human inspectors, NASA, seeded defects | no; human-only evidence | no: median RE −52% at k = 2 |
| CR on LLM judges | C, label errors, not software | yes; calibrated, imprecise | only with ≥ 3 diverse judges, and still wide |
| Decision-point process (Petersson) | A, review; one industrial trial | no | the structure is usable; the estimate is not |
| Own-trial overlap | own trial, n = 2 data points | yes | it underestimated both times |
