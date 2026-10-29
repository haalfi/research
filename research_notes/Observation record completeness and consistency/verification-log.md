# Verification log

## Run structure

1. **Deep-research workflow.** 6 search angles, 24 sources fetched, 101
   claims extracted and 25 verified by three adversarial votes each (2 of 3
   refutations kill a claim). 18 were confirmed, 7 refuted, and 10 survived
   synthesis. Its budget dropped 12 claims, including every T4 claim and
   every claim on disconfirming search (d).
2. **A separate verification pass** over full texts for the dropped claims
   (T4, T5, (d), TofuEval, GADR, Quasar). Items 1 to 5 were read by the
   verifying agent itself. Items 6 to 9 were read by two sub-agents, and
   the verifying agent did not re-read their passages.

## Corrections from the verification pass

- **TofuEval:** inconsistent summary sentences range from **14.4 to 27.8%**
  (Table 2), not 17.5 to 27.8%, which is MediaSum only.
  - Per-type shares, computed by the verifier from the released CSVs (not
    in the paper): Extrinsic Information is 50.0% of inconsistent sentences,
    Nuanced Meaning Shift 15.0%, Reasoning Error 14.7%.
  - GPT-3.5-Turbo detected only 50% of extrinsic-information errors, about
    30 points below non-LLM metrics.
  - Annotator κ = 0.42 (MediaSum) and 0.34 (MeetingBank).
- **SEURAT evaluation:** "time differences not significant" holds for
  Mann-Whitney (p = 0.096 to 0.94) only. The F-test was significant for all
  tasks; the author calls it "somewhat suspect". ANACOVA was significant
  for the corrective task only. The SEURAT experts took longer.
- **Briand et al. ISERN-97-22** states the 3-inspector error as ">27%". TSE
  states "-27%".
- **Petersson et al.** does not link positive inspector correlation to
  underestimation. That link stays *Inference*.
- **GADR**: the 52 of 55 ratings came from students rating their own
  projects, and the paper itself notes familiarity bias.
- **Kumar et al. 2606.15689**: its union recall is below a member's recall,
  which is internally inconsistent, so the paper is not usable as evidence.

## Sources confirmed in the verification pass

| Item | Source | Grade | Verdict |
|---|---|---|---|
| 1 | Briand, El Emam, Freimut, Laitenberger, TSE 26(6) 2000 (as NRC ERB-1084) | A | confirmed (a) to (f) |
| 2 | Same authors, ISERN-97-22 | A-workshop | confirmed, with the differences above |
| 3 | Petersson, Thelin, Runeson, Wohlin, JSS 72, 2004 (author PDF) | A | confirmed; correlation link not found |
| 4 | CR over LLM reviewers | — | no peer-reviewed study. Closest: Kansal 2026 (C); Calboreanu, arXiv 2604.04258 (C/D) |
| 5 | Eick et al., ICSE 1992 | — | **[unreachable]** |
| 6 | Burge, SEURAT, WPI PhD 2005 | A | confirmed; evaluation corrected |
| 7a | Elberzhager, Gerbershagen, Ginkel, arXiv 2601.19693 (Quasar) | A-pre; own tool | confirmed |
| 7b | Costa da Silva, Gama, GADR, arXiv 2608.17694 (SBES 2026 header) | A-pre; own tool | confirmed |
| 8 | Tang et al., TofuEval, NAACL 2024 | A | confirmed, with the range corrected |
| 9a | Basili et al., PBR, EMSE 1996 (author manuscript) | A; own technique | confirmed |
| 9b | Simecek et al., HoF-Bench, arXiv 2607.27030 | A-pre; own scaffold | confirmed |
| 9c | Kumar et al., arXiv 2606.15689 | A-pre | internally inconsistent |

### Queries for item 4 (CR over LLM reviewers)

1. `capture-recapture LLM code review remaining defects estimation arXiv`
2. `"capture-recapture" "large language model" reviewers defect estimation 2024 OR 2025`
3. `"Lincoln-Petersen" OR "capture-recapture" LLM agents vulnerabilities "unseen" bugs estimate remaining 2025 2026 arXiv`

## Claims refuted by the workflow (kept for the record)

| Claim | Vote | Source |
|---|---|---|
| Jaffe/Leveson criteria applied as checklists, with industry feedback as the evidence | 1-2 | Leveson 2000 |
| Obstacle completeness criterion relative to known domain properties | 0-3 | van Lamsweerde & Letier, TSE 2000 |
| Obstacle analysis validated only on the London Ambulance System report | 0-3 | same |
| Obstacle analysis has no objective completeness endpoint | 0-3 | retrospective |
| STPA coverage measured against an external hazard taxonomy | 1-2 | Abdulkhaleq & Wagner |
| Scenario readers better on their targeted classes, no worse on others | 1-2 | Porter et al. 1995 |
| PBR teams no better than checklist teams (team level, p = 0.33 and 0.14) | 0-3 | Fabbri et al. TR |

*Note:* a refutation means the three verifiers did not find the claim
supported as worded in the full text. It does not establish the opposite.

## Sources fetched but unusable

- typeset.io copy of Heimdahl & Leveson 1996: graded unreliable, so the
  full text counts as **[unreachable]**.
- core.ac.uk 83782514: unreliable.
- bohrium.com page on CR with two inspectors: unreliable, an abstract
  aggregator.
- Rationale Capture Cycle (Utrecht repository): abstract only, and the PDF
  returned HTTP 500, so **[unreachable]**.
- Ahmeti et al., ECSA 2024, ADRs in practice: abstract page only, so
  **[unreachable]** as full text. Per the abstract, it has no review step.
- Dalhousie CSCI 3130 design-review rubric (2011): grade D, a course
  assignment.
