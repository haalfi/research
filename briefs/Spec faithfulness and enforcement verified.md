# Spec faithfulness and enforcement verified

## 1. Task

Verify the report `reports/Spec faithfulness and enforcement.md` (heading
"Prove the spec wrong before building on it") on this branch against full
texts. Write a corrected edition as a new report. Do not edit the earlier
report or its notes; the two must stay diffable.

Read first:
- the earlier brief `briefs/Spec faithfulness and enforcement.md`;
- the earlier report;
- the earlier notes in `research_notes/Spec faithfulness and enforcement/`.

Scope is verification and correction, not new search, except where a claim
can only be settled by a replacement source.

## 2. Known wrong parts: fix or confirm first

1. **The Cedar "§3 challenge" is likely spurious.** The earlier brief's §3
   never said Cedar's models are Dafny. It listed Cedar under "executable
   reference models", and Dafny separately as a layer in §2. Quote the brief
   verbatim, then decide whether the challenge stands. If it does not, remove
   it and record it as a misreading of the brief by the earlier run.
2. **The Porcupine "§3 challenge"** rests on one preprint (OmniLink, A-pre).
   Its author also builds competing checkers. Re-read it and look for one
   neutral benchmark. Downgrade it to a qualification unless one is found.
3. **Figures used from partial reads:**
   - PBT-Bench (abstract and setup only);
   - SysMoBench Table 3 (parsed from text extraction);
   - TLA+-Bench's invariant-mutation probe wording;
   - Req2LTL's definition of "correct" (internally inconsistent);
   - Gay et al. TSE 2015 (first pages only);
   - Mäder & Egyed (abstract only).

   Re-read each in full, or mark the figure as unverified.
4. **Grade conflicts.** FormalAlign (A vs A-pre, venue disputed). PROPAS,
   the DMN paper, Cirstea et al. and CCF: venue not verified. AlgoVeri was read
   via grep only.
5. **Kernsatz and §4 lean on single studies.** Check that every Kernsatz
   claim is carried by the cited full texts at the stated strength. That
   includes "about 90 % with three tests" (Cunha & Macedo: one A-pre, Alloy,
   structural specs, student errors) and "LLM errors are correlated" (Kim et
   al.: MCQ setting).

## 3. Verification debt: fetch in this order

Fetch the items that can change a conclusion first. Try author copies, arXiv
and institutional repositories when a publisher blocks access.

1. Papadakis et al., ICSE 2018: mutation score vs real faults, suite size
   controlled.
2. Knight & Leveson 1986; Eckhardt & Lee; Littlewood & Miller.
3. Beer et al., CAV 1997: the "20 % vacuous" figure, currently second-hand.
4. Heitmeyer et al., TOSEM 1996 (SCR checker); Selby, Basili, Baker, TSE 1987
   (Cleanroom).
5. NASA IV&V return-on-investment data.
6. Fedchin et al., NFM 2023 (DTest).
7. The AWS "Systems Correctness Practices" article, CACM 2025.
8. The rest of the earlier report's §5 debt table, as time allows.

## 4. Self-qualification (mandatory)

The run must state and qualify its own findings. Do not leave that to a
later review.

- **Per claim**, in the verification log:
  - verdict (confirmed, corrected, not found, refuted, unverifiable);
  - grade;
  - full text read (yes or no);
  - n and setting.
- **Transfer label per recommendation:**
  - *direct*: evidence on library or API behaviour specs;
  - *analogous*: other spec domains;
  - *inference*.
- **Source independence.** Flag tool authors evaluating their own tool, and
  vendor posts.
- **Baseline challenges.** Before writing any "§3 challenge" or
  qualification, quote the baseline text verbatim and say what exactly it
  contradicts.
- **Confidence per recommendation** (high, medium or low), with the one
  finding that would overturn it.
- **A "What this run did not do" section.**
- **A self-check section** that lists any place where this run may have
  misread the brief or a source.

## 5. Deliverable

`reports/Spec faithfulness and enforcement verified.md`:

1. **What changed in this edition**: substantive vs restyled, with
   verification-log IDs.
2. **Corrected report**: same structure as the earlier one, with § 1 to § 6
   updated.
3. **Self-check and limits** (§ 4 above).

Notes go in `research_notes/Spec faithfulness and enforcement verified/`,
including a `verification_log.md`.

## 6. Evidence rules

The same as the earlier brief §6:
- full texts only;
- **[unreachable]** and *Inference* labels;
- grades A, A-pre, A-workshop, B, C, D;
- agent applicability stated per method.

## 7. Delivery

- Branch: `research/spec-faithfulness-and-enforcement` (existing topic
  branch).
- Title: `Spec faithfulness and enforcement verified`.
- Follow the repository's CLAUDE.md.
