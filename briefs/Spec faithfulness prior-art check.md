# Spec faithfulness prior-art check

## 1. Question

A follow-up to this branch's reports. A lightly primed question to another
tool produced the leads below. **For each one, establish what it actually
shows, from its full text, and whether it changes a recommendation already
made.** This is a verification run, not a new survey: do not search beyond
the named leads, except to resolve one of them.

The stakes are narrow:
1. Is there a **measured method that turns verifier counterexamples into
   questions for the decision-maker**? That would be a way to find questions
   no checklist raises, which the record-quality report
   (`research/observation-record-quality`, read below) lists as unmeasured.
2. Is there a **measured faithfulness check of a formal artifact against its
   natural-language source** (the "A ≡ R" gate, as opposed to "M ⊨ A")? That
   bears on the deep dive's held-back judge gates.
3. Does any lead show a **published end-to-end pipeline with faithfulness
   gates against the prose**? That would challenge the verified edition's
   § 2.6(c) search result.

## 2. Read first

- This branch: `reports/Spec faithfulness and enforcement summary.md`, then
  the deep dive (§ 3, § 5.1) and the verified edition (§ 2.1, § 2.5,
  § 2.6). These are the recommendations a lead may change. Cite them by ID
  (for example D1-R1, D4-R1, D5-R4, R2).
- With the maintainer's explicit permission for this run, the branch
  `research/observation-record-quality`, file
  `reports/Observation record completeness and consistency.md`: its § 3
  check map, § 4 stopping rule and § 5 open questions 4 and 5. Add the
  branch to `.git/claude-allowed-branches`.

## 3. The leads

Citations are as the other tool gave them. They are **unverified**, and some
may be wrong, misattributed or nonexistent.

| # | Lead | Claimed | Given source |
|---|---|---|---|
| L1 | C-GRiD, "Neuro-symbolic requirements elicitation utilizing formal verification counterexamples" | An LLM proposes a model and properties, a symbolic verifier runs, counterexamples become natural-language questions to stakeholders; 79.2% mean constraint-recovery recall (ideal oracle), 70.8% (noisy simulated stakeholder) | conf.researchr.org, ASE 2026 research track, paper 49 |
| L2 | Claimcheck | Checks whether a formal artifact "means what its natural-language requirement asks for" | arXiv 2610.17358 |
| L3 | Automotive LLM plus formal methods workflow | Separates M ⊨ A (CEGAR-style refinement) from A ≡ R (expert review of requirement–assertion pairs, traceability matrices, coverage reports, documented limits); a cross-model review run for five rounds with "faithful" as a gated verdict | Springer chapter, DOI prefix 10.1007/978-3-032-26220-2_31 |
| L4 | VeriAct | Closed agentic loop for JML specification synthesis: propose, check, structured harness feedback, revise until verifiable, correct and complete | arXiv 2604.00280 |
| L5 | SpecLoop | Generates specifications from RTL, reconstructs RTL from them, formal equivalence against the original; mismatches drive refinement (a round-trip gate) | arXiv 2603.02895 |
| L6 | Reference equivalence by bidirectional implication | Equivalence checking against a reference model rather than textual similarity | arXiv 2610.10604 |
| L7 | ARSENAL | Extracts formal models and LTL specifications from natural-language requirements, type inference, model checking with SAL | DTIC ADA611691 (DTIC blocks this environment; find an author or institutional copy) |
| L8 | Counterexample replay to agents | Feeding the concrete counterexample, not an error message, improves repair | ssvlab.github.io, FATTW 2026 slides |
| L9 | "Two-stage constrained JSON, then deterministic translation" as preferred practice; provenance gates that fail closed | GitHub `danielrosehill/Spec-Standard-Research` prior-art survey; GitHub `ashbrener/spec-kit-atlas` example output | Likely grade D; verify only whether they cite a primary source, and follow that instead |

Also named without a source: SpecVerify, NL2Spec, OnionL, C-GRiD's
predecessors. Resolve only if one of L1 to L8 depends on it.

## 4. For each lead

- Does it exist as cited: title, authors, venue, year. Correct the citation.
- Grade (A, A-pre, A-workshop, B, C, D) and full text read (y, partial, n).
- What was measured: n, setting, what "correct" meant, the baseline, and
  whether its authors are evaluating their own tool.
- Whether agents (LLMs) did the step, with the result.
- Transfer: *direct* (library or API behaviour specs), *analogous* or
  *inference*.
- **The delta**: which recommendation or open question on this branch or in
  the record-quality report it confirms, qualifies or overturns. Quote the
  old text verbatim. "No change" is a valid and expected answer.

## 5. Disconfirming checks

- (a) Do L2, L3 or L6 measure faithfulness against intent, or only
  agreement with a gold formula or an expert's judgement? Say which.
- (b) Does L1's recall survive a realistic stakeholder, or only a simulated
  one? Does its question generation depend on a correct initial model?
- (c) Does L3 or L7 constitute a published pipeline with a faithfulness gate
  against the prose? If yes, compare it with Pipeline A in the deep dive's
  § 3.3, as the original brief's § 5(c) asked.

## 6. Evidence rules

As this branch's earlier briefs:
- Verdicts rest on full texts; search extracts are leads only. Label
  unreachable sources **[unreachable]** and your own reasoning *Inference*.
- Grades as above. Flag tool authors evaluating their own tool.
- Prefer measured figures, with n, setting and what "correct" meant.

## 7. Deliverable

`reports/Spec faithfulness prior-art check.md`:

1. **Kernsatz**: at most three sentences. Name what changed, if anything.
2. **One row per lead**: corrected citation, grade, full text, measured
   result, agents, transfer, delta.
3. **Changed recommendations**: old text verbatim, new text, reason. Empty
   if nothing changed.
4. **Answers to § 1's three questions.**
5. **Verification debt.**
6. **Sources** with grades.

## 8. Delivery

- This branch, `research/spec-faithfulness-and-enforcement`. Do not edit
  earlier reports or their notes.
- Title: `Spec faithfulness prior-art check`.
- Follow the repository's CLAUDE.md for layout and running.
