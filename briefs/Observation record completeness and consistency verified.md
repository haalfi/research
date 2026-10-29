# Observation record completeness and consistency verified

A follow-up to `reports/Observation record completeness and consistency.md`
on this branch. The maintainer presented that report to another tool
(Perplexity) twice; its answers named leads that may strengthen or qualify
the report. The maintainer asked for this run: "run it now here, verify
claimcheck yourself and than proceed on proposed follow up".

## 1. Question

For each lead below, establish from its full text what it actually shows and
whether it changes a finding, the check map (§ 3), the stopping rule (§ 4) or
the verification debt (§ 5) of the earlier report. This is a verification
run, not a new survey: no searching beyond the named leads, except to resolve
one of them. "No change" is a valid answer.

## 2. Leads

Citations are as the other tool gave them, and **unverified**.

| # | Lead | Claimed | Bears on |
|---|---|---|---|
| L1 | claimcheck, arXiv 2610.17358 | Blind back-translation of a formal artefact plus a separate judge beats one informed LLM call by 8.2 to 9.8 macro-recall points; 3,234 requirement–artefact pairs over Dafny, Lean 4, Isabelle, Rocq | T3 fidelity judge design; T2 extraction validation |
| L2 | Correlated LLM errors, arXiv 2609.11428 | Mean pairwise error correlation 0.285 across seven models; effective independent count 2.58 | T4 independence; T5 |
| L3 | LLM requirements elicitation, arXiv 2507.02564 | Best setup fully elicited 60.94% of scenario requirements, 73.7% with partial captures, 33 simulated interviews | T1 adjacent evidence |
| L4 | Query-Conditioned NLI (QC-NLI), ACL 2025 Findings, aclanthology 2025.findings-acl.765 | Document inconsistency and intrinsic hallucination detection as query-conditioned entailment | T2 rule × outcome; T3 claim-to-span |
| L5 | RAG4C, KIT repository 1000193552 | 0.97 inconsistency-detection accuracy, synthetic and industrial automotive case, an order of magnitude less manual effort | T2 hybrids |
| L6 | ESEM 2026, LIPIcs.ESEM.2026.82 | Requirement gaps systematically identified | T1 class 4; only if the full text is open |

Not pursued, with reason (from the critical review in the session):
arXiv 2510.21513 (already read in full and excluded: code generation, not
defect finding); a GitHub mirror of GADR (already verified from arXiv); JMIR
medical record QC, COLING 2025 evaluator consistency and an MDPI mapping study
(off topic or without recall figures). C-GRiD and the other leads of the
spec-faithfulness prior-art check belong to that topic's branch.

## 3. For each lead

Corrected citation; grade; full text read (y, partial, n); n, setting, what
"correct" meant, baseline; authors evaluating their own tool; whether agents
did the step and with which result; transfer (direct, analogous,
inference); the delta, quoting the earlier report's text verbatim.

## 4. Evidence rules

As the earlier brief: full texts only, **[unreachable]** where not fetched,
*Inference* labelled, grades A, A-pre, A-workshop, B, C, D.

## 5. Deliverable

`reports/Observation record completeness and consistency verified.md`:
Kernsatz (at most three sentences, naming what changed); one row per lead;
changed findings with old text verbatim, new text and reason; revised
verification debt; sources with grades. The earlier report and its notes stay
unedited.
