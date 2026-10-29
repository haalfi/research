# T1. Completeness of a decision record

Sources were read in full text by the workflow's fetchers, and each claim was
put to three adversarial verifiers (2 of 3 refutations kill a claim). Votes are
given as confirm-refute. Grades follow the brief.

## 1. Completeness criteria beyond tables

### Leveson, "Completeness in Formal Specification Language Design for Process-Control Systems" (FMSP 2000) — A

- **Table or state-machine completeness does not give environment
  completeness.** Verbatim: "Although these robustness criterion ensure that
  there is always one transition that can be taken out of every state, they
  do not guarantee that all assumptions about the environment have been
  specified or that there is a defined response for all possible input
  conditions the environment can produce." (vote 3-0)
  - For the record: the settled SCR-style check on declared domains covers
    the AX-3, AX-6, AX-10 and AX-11 tables. It cannot certify the
    Environment list (`E1` to `E15`), which needs its own check.
- **A mandatory slot makes an omission visible.** "by including a place for
  it in the specification language syntax, the specifier must either include
  it or indicate that the information is not applicable or important ...
  need to know that it was considered by the original specifiers and not
  simply forgotten." (vote 3-0)
  - The axis form already does this per axis (decided, explicitly open, or
    not applicable with a reason). *Inference:* the same device can be pushed
    down to cells: one slot per (Environment row × step s1 to s4) in AX-7, and
    one per (Environment row × failure axis AX-10 to AX-13). An empty slot is
    then a mechanical finding.
  - Leveson's own limit: the criteria "allow automated checking or assist
    manual review". A filled slot can still be wrong, and a slot the template
    lacks cannot be found missing. That limit is failure class 4.
- **Refuted (1-2):** that the Jaffe/Leveson criteria have measured yield as
  checklists. The paper reports industry feedback only, with no counts.
- Human-only evidence. No agents were measured.

The Heimdahl & Leveson RSML paper (TSE 1996, "Completeness and consistency in
hierarchical state-based requirements") was found only as a typeset.io copy
the workflow graded unreliable. **[unreachable]** as full text in this run.
Its contribution, mechanical completeness and consistency analysis of
AND/OR-table guards, is the settled SCR result in another notation, so it is
not re-surveyed here.

## 2. Coverage of an environment or fault model

### Abdulkhaleq & Wagner, controlled experiment STPA vs FMEA vs FTA (arXiv 1612.00330) — A-pre

- Mean recall against a reference set of software safety requirements:
  **STPA 0.443, FMEA 0.326, FTA 0.231**, p < 0.05 (two-way ANOVA). (vote 3-0)
- n: 21 students in 3 groups of 7, 3 systems (TDCS, ABS, TCAS). Each group
  produced one merged list, so there are very few effective units. The
  coverage figures in the text (0.70 / 0.60 / 0.30) disagree with Table 6.
- Cost: mean time 116 min STPA, 94 FMEA, 88 FTA, within 2-hour slots.
- "Correct" meant matching a reference requirement list derived by the
  authors. The best method found under half of it.
- **Refuted (1-2):** the claim that coverage was measured against an
  external hazard taxonomy (NASA, Leveson control flaws), in a way usable as
  axis validation.
- Human-only evidence.

### Thesis, STPA vs FMEA on TomoTherapy (MIT DSpace 1721.1/113531) — B/C (S.M. thesis, single analyst)

- STPA: 99 unsafe control actions, 10 causal scenarios, 29 requirements. FMEA:
  74 failure modes. The units differ and no overlap is reported. FMEA's
  causes were "only human factors". This claim was not voted on by the
  workflow; it rests on the fetcher's extract.

*Inference for the record.* STPA's unit is close to an Environment row: an
unsafe control action. It is a control action (provided, not provided, too
early or late, stopped too soon) issued by a controller in a control
structure. Mapped onto OP-01 there are three controllers: O1 (caller), O2
(concurrent caller) and O3 (out-of-band actor), plus the world and the
runtime as disturbances. STPA's four guide-words then generate candidate rows
mechanically, such as O3 acting *during* s3 and not only before it, or the
runtime stopping a step *too soon*. OP-01's late finds fit this shape:
O44 (O3 changes metadata only, not content), O21 (O3 creates a and a/b
together) and O43 (a second host's cache). Each is an O3 or world action
that the Environment did not name. This is a mapping, not a measurement.

## 3. Finding questions no checklist raises

### Obstacle analysis, KAOS (van Lamsweerde & Letier, TSE 2000; retrospective, UCL Discovery) — A

- An obstacle O to goal P must satisfy two conditions: **obstruction**
  (O, Dom ⊨ ¬P) and **domain consistency** (O ∧ Dom satisfiable). Obstacles
  are found by regression through the domain theory, by refinement patterns,
  and by heuristics derived from both. (vote 2-1)
- *Inference:* as an admission test for a candidate Environment row, this
  asks of each candidate O3 or world action: does it, together with what the
  record assumes, falsify some decided outcome? If so, it belongs in the
  Environment with an exposure. That is a **relevance** test, run per
  decision, and it needs each decision restated as a condition. It is **not
  a completeness test**.
- **Refuted, 0-3 each:** that obstacle completeness can be certified
  (domain-completeness relative to known domain properties); that the method
  was validated by the London Ambulance System case; and that the method has
  an objective stopping point. The surviving evidence gives obstacle analysis
  no measured yield.
- Human-only evidence.

### LLM agents producing decision records from dialog (arXiv, see T3) — A-pre

- An LLM agent turning meeting transcripts into ADRs covered about 18 of 23
  decisions that four senior architects listed. It also found decisions the
  seniors had not listed, so the expert baseline was itself incomplete. Not
  voted; pending the verification agent (see T3 and the report).

### What is measured, and what is not

- No source in this run measures a technique that surfaces questions **no
  checklist raises** (class 4). Slot enforcement surfaces the questions the
  slots name. STPA surfaces environment actions at under half recall in one
  student study. Obstacle analysis has no surviving measurement.
- The OP-01 evidence itself (audit-025 § 5 class 4; RFC-0028 P4) shows what
  did surface class 4 questions there. They came from a reader who reads the
  record against **use**: a caller's own deadline (C7), the async shape (G1),
  the file object's other methods (G2). In each, a reader took a familiar
  caller idiom and asked what the record said about it. *Inference:* the
  measurable proxy is perspective-based reading with a "caller" perspective
  that must write a usage scenario per handed-out object and per form (sync
  and async). Its yield on requirements documents is in T2, with weak
  evidence.

## 4. Validating the checklist (the axes) for coverage

- No surviving source validates a requirements checklist's coverage.
  Abdulkhaleq & Wagner's coverage against a hazard-type taxonomy, the nearest
  analogue, was refuted as stated (1-2).
- *Inference, an operational method:* treat each late-found open item as a
  test of the axes. For each one, ask whether an axis question, read
  literally, asks it. If none does, the item is an **axis escape**, and the
  axes gain a question (RFC-0028 P4 did exactly this with C7 and G1 to G4).
  The escape rate per record is then a measure of the axes:
  - OP-01 before P4: of O14 to O26, five items (C7, G1 to G4) were axis
    escapes, about 5 of 13.
  - OP-01 after P4: O27 to O44 have not been classified this way. That is
    verification debt (see report § 5).
  - A falling escape rate over OP-02, OP-03 and later records is evidence
    the axes are converging. A constant rate means they are not.
- SEURAT's "Tradeoff Missing" check (T2 and report; pending verification) is
  the one published device that flags a missing consideration from a
  pre-declared knowledge base. That is, again, coverage only of what was
  declared.

## Catches and misses (summary)

| Option | Catches | Misses | Cost | Agents measured |
|---|---|---|---|---|
| Slot per axis or cell (Leveson) | empty slots, mechanically | wrong fillings; slots the template lacks | low, script | no; human-only evidence |
| SCR table check (settled) | gaps and overlaps in declared domains | undeclared domain members; the Environment | low once domains are declared | settled earlier |
| STPA guide-words over O1, O2, O3 and the world | missing environment actions, timing variants | under half of a reference set in one study | about 25% more analyst time than FMEA | no; human-only evidence |
| Obstacle test per decision | relevance of a candidate action | completeness; needs a formal restatement | high per decision | no; human-only evidence |
| Axis-escape tracking | weak axes, across records | nothing within one record | low | own reading of OP-01 only |
