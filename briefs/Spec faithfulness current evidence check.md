# Spec faithfulness current evidence check

## 1. Question

A follow-up to this branch's reports. Another tool (Perplexity) claims "more
current evidence" for this topic (its text is in § 8, unchanged). **For each
new lead, establish what it actually shows, from its full text, and whether it
changes a recommendation already made.** This is a verification run, not a new
survey: do not search beyond the named leads, except to resolve one of them.

The stakes are narrow:
1. Does any lead measure the **central claim** head-to-head: oracles derived
   from the prose records catch *spec misreadings* that oracles derived from
   the spec miss? Answer yes or no for LLM2Alloy explicitly.
2. Does the mutation-adequacy recommendation ("compare per-family kills at
   equal test counts", after Papadakis et al. 2018) need a qualification for
   LLM-generated suites?
3. Do any grades or corroborating citations change?

## 2. Read first

- `reports/Spec faithfulness and enforcement summary.md`, then the deep dive
  (§ 3, § 5.1), the verified edition (§ 1, § 2.1, § 2.4, § 2.5, § 6) and the
  trial design (hypotheses). Cite recommendations by ID (e.g. R3, R4, R17,
  D1-R1, D5-R4).
- `reports/Spec faithfulness prior-art check.md`: claimcheck (L2) and the
  Lahiri / Spec-Harness I/O-oracle line (L4) are already settled there.

## 3. Leads

Already settled on this branch, not re-checked: claimcheck (arXiv 2610.17358),
Cunha & Macedo (FM 2026).

| # | Lead | Claimed | Given source |
|---|---|---|---|
| N1 | LLM2Alloy | Documentation-derived vs code-derived Alloy specs and tests on two libraries; the doc-derived pipeline found a documented-behaviour violation (duplicate flag names accepted) that direct README-to-tests missed in all three runs | ICST 2026, computer.org CSDL 2iasUM9RFHa |
| N2 | Zhao, Zhou, Cohen | Replication for LLM-generated suites: suite size is not a dominant confounder for coverage / mutation score vs real-bug detection | arXiv 2607.22880 (ISSTA 2026 per arXiv comment) |
| N3 | Dai et al., "Validating Autoformalized Specifications via Contrapuntal Languages" | Positive tests from reference executions, negative tests from mutant outputs, Z3 checks whether pre/postconditions admit each pair | arXiv 2610.30059 |
| N4 | Amrollahi, Lopez, Barrett, round-trip verification and repair | Same paper as arXiv 2604.25031 already on this branch; claimed now EMNLP 2026 Findings; "does not guarantee semantic fidelity, but it predicts it" | aclanthology 2026.findings-emnlp.469 |
| N5 | "Wavering Oracles" (Nee, Zhong, Ni) | Mean pairwise error correlation 0.285 across seven models; effective independent count 2.58 | arXiv 2609.11428 |
| N6 | 30-LLM TLA+ evaluation | 205 TLA+ specs; up to 26.6 % syntactic, 8.6 % semantic correctness; size does not predict quality | SciTePress DOI 10.5220/0015070400004088 |

## 4. For each lead

- Does it exist as cited: title, authors, venue, year. Correct the citation.
- Grade (A, A-pre, A-workshop, B, C, D) and full text read (y, partial, n).
- What was measured: n, setting, what "correct" meant, the baseline, and
  whether its authors evaluate their own tool.
- Whether agents (LLMs) did the step, with the result.
- Transfer: *direct* (library or API behaviour specs), *analogous* or
  *inference*.
- **The delta**: which recommendation or open question it confirms, qualifies
  or overturns. Quote the old text verbatim. "No change" is valid.
- Assess the other tool's proposed edits in § 8 (Kernsatz rewrite, mutation
  wording, pipeline additions 1–4): adopt, adopt with changes, or reject, with
  reason.

## 5. Disconfirming checks

- (a) N1: is its comparison prose-derived vs spec-derived oracles on spec
  misreadings, or two documentation routes on implementation bugs?
- (b) N2: does it contradict Papadakis et al. for LLM suites, or only show
  a weaker confounder? Does equal-count comparison stay valid?
- (c) N3: are its positive tests code-derived (reference executions)? Can it
  serve as the spec-blind scenario-derivability gate?
- (d) N5: is its setting multiple-choice or open-ended, and does it add to
  Kim et al. (ICML 2025)?

## 6. Evidence rules

As this branch's earlier briefs: verdicts rest on full texts; search extracts
are leads only; label **[unreachable]** and *Inference*; grades as above; flag
tool authors evaluating their own tool; prefer measured figures with n,
setting and what "correct" meant.

## 7. Deliverable and delivery

`reports/Spec faithfulness current evidence check.md`: Kernsatz (≤ 3
sentences, name what changed), one row per lead, changed recommendations (old
text verbatim, new text, reason; empty if none), verdict on each proposed edit
in § 8, answers to § 1, verification debt, sources with grades. Notes in
`research_notes/Spec faithfulness current evidence check/`. Branch
`research/spec-faithfulness-and-enforcement`; do not edit earlier reports or
notes; follow CLAUDE.md.

## 8. The other tool's text (unchanged)

Yes—there is now stronger, more current evidence for several load-bearing parts of your research, especially the prose→spec faithfulness gap, spec-blind test oracles, and correlated LLM errors. The central design still survives, but two claims can be upgraded from “no direct evidence” to “direct, recent evidence,” and one adequacy claim needs a qualification.

## Strongest new evidence

| Your research claim | Better/current evidence | What it changes |
|---|---|---|
| Prose-derived oracles may catch spec misreadings that spec-derived oracles miss; “no head-to-head measurement” | **LLM2Alloy (ICST 2026)** directly compares documentation-derived versus code-derived Alloy specifications and tests. The documentation-derived pipeline found a real, documented-behaviour violation—duplicate flag names silently accepted—that a direct README-to-tests baseline missed in all three runs.  [computer](https://www.computer.org/csdl/proceedings-article/icst/2026/330800a717/2iasUM9RFHa) | This is the closest current head-to-head analogue to your core claim. It is still only two small libraries and exploratory, so treat it as **direct but preliminary evidence**, not a general result. |
| Formalization/round-trip checks are necessary but not sufficient for faithfulness | **claimcheck (arXiv, Oct. 2026)** gives a large benchmark: 3,234 requirement–formal-artifact pairs across Dafny, Lean 4, Isabelle, and Rocq. Its blind back-translation plus separate judge improves macro recall by 8.2–9.8 points over a single informed LLM call.  [arxiv](https://arxiv.org/abs/2610.17358) | This substantially strengthens the case that NL↔formal alignment needs an explicit faithfulness gate, and that a judge seeing both artefacts is not automatically best. |
| Spec-blind positive/negative tests detect wrong specs | Your cited **Cunha & Macedo, FM 2026** result is now formally published by Springer; it reports that GPT-5 few-shot test generation is “highly effective” at detecting incorrect human-written specifications.  [link.springer](https://link.springer.com/chapter/10.1007/978-3-032-26204-2_15?error=cookies_not_supported&code=ffd364c9-b6dd-4aa9-9874-7c6da8cc61d3) | You can replace the “A-pre / FM 2026” framing with the published venue citation, while retaining the scope limits: Alloy structural models, student-written wrong specs, one LLM. |
| Round-trip verification catches divergent readings but not shared misreadings | **Faithful Autoformalization via Roundtrip Verification and Repair (EMNLP 2026 Findings)** explicitly states that formal equivalence “does not guarantee semantic fidelity, but it predicts it.”  [aclanthology](https://aclanthology.org/2026.findings-emnlp.469.pdf) | This is a cleaner, more recent citation for your necessary-only qualification than relying only on the earlier round-trip preprint. |
| LLM-written formal specs remain unreliable | A 2026 systematic evaluation of 30 LLMs on 205 TLA+ specifications found up to 26.6% syntactic correctness but only 8.6% semantic correctness; model size did not predict quality.  [scitepress](https://www.scitepress.org/Link.aspx?doi=10.5220/0015070400004088) | This reinforces your baseline that LLM-written system-level formal specs need expert oversight and mechanical gates. |

## Important qualification: mutation adequacy

Your report correctly says mutation kills should be compared at equal suite size, citing Papadakis et al. A newer 2026 replication for **LLM-generated** tests complicates the transfer of that conclusion:

- Zhao, Zhou, and Cohen find **little evidence that suite size is a dominant confounder** for correlations among coverage, mutation score, and real-bug detection in LLM-generated suites; suite size correlates only weakly with mutation score and real-bug detection. [arxiv](https://arxiv.org/html/2607.22880v1)
- This does **not** overturn Papadakis for human-written suites, but it means your recommendation should say: control for suite size when comparing families, but do not assume suite size is always the dominant confounder for agent-generated suites. [arxiv](https://arxiv.org/html/2607.22880v1)

## Useful additions to the pipeline

1. **Use claimcheck-style blind back-translation as a G2-style faithfulness gate.** Have one model translate the formal artefact back to English without seeing the original requirement, then have a separate judge compare it with the requirement. The reported gain is 8.2–9.8 macro-recall points across four formal languages. [arxiv](https://arxiv.org/abs/2610.17358)

2. **Treat documentation-derived and code-derived specifications as complementary, not interchangeable.** LLM2Alloy found documentation-derived specs surfaced a documented-constraint violation missed by direct README-based test generation, while code-derived specs captured an implicit abstraction absent from documentation.  This supports your dual-derivation recommendation, but with a sharper mechanism: different sources expose different classes of omitted constraints. [computer](https://www.computer.org/csdl/proceedings-article/icst/2026/330800a717/2iasUM9RFHa)

3. **Add a computable input–output oracle check for autoformalized specs.** A 2026 approach evaluates specifications using positive tests from reference executions and negative tests from mutant outputs, with Z3 checking whether pre/postconditions admit each pair.  This fits your proposed “scenario derivability” and “rejected-option refutation” gates. [arxiv](https://arxiv.org/html/2610.30059)

4. **Keep independence claims modest.** New evidence continues to show correlated model errors: one 2026 study reports mean pairwise error correlation of 0.285 across seven models, reducing seven models to an effective independent count of 2.58.  This supports your conclusion that provider swapping and multiple writers are insufficient; different derivation paths and deterministic adjudication remain necessary. [arxiv](https://arxiv.org/html/2609.11428v1)

## Revised wording for the Kernsatz

I would revise this sentence:

> “That prose-derived oracles catch spec misreadings that spec-derived ones miss has no head-to-head measurement.”

to:

> “Direct evidence remains limited, but a 2026 exploratory study found that a documentation-derived Alloy specification pipeline exposed a documented-behaviour violation missed by direct documentation-to-test generation in all three runs; broader head-to-head evidence across domains is still lacking.” [computer](https://www.computer.org/csdl/proceedings-article/icst/2026/330800a717/2iasUM9RFHa)

And revise the mutation recommendation to:

> “Compare per-family mutant kills at equal test counts; for LLM-generated suites, recent replication evidence suggests suite size may be a weaker confounder than in earlier human-written-suite studies, so report both raw and size-controlled correlations.” [link.springer](https://link.springer.com/chapter/10.1007/978-3-032-26204-2_15?error=cookies_not_supported&code=ffd364c9-b6dd-4aa9-9874-7c6da8cc61d3)

The biggest upgrade is therefore **claimcheck + LLM2Alloy**: together they move your two weakest evidentiary spots—faithfulness measurement and prose-versus-spec-derived oracle comparison—from purely inferred to empirically supported, while still leaving room for a purpose-built trial on your own record/spec/model pipeline. [computer](https://www.computer.org/csdl/proceedings-article/icst/2026/330800a717/2iasUM9RFHa)
