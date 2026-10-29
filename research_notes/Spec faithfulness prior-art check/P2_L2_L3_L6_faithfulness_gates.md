# P2: L2 (claimcheck), L3 (automotive LLM + FM workflow), L6 (reference equivalence): faithfulness gates

Scope: brief leads L2, L3 and L6 only. All three full texts were read. Downloads are in the scratchpad folder `p2/`, never the repo. Recommendation IDs refer to this branch's reports: [V] verified edition, [DD] deep dive, [TD] trial design, [S] summary.

---

## L2: claimcheck (arXiv 2610.17358)

### Takeaway
The paper exists and does what the brief says. It is a workshop paper by the tool's own authors. On a 3,234-row benchmark, two blind steps (informalize the artifact without seeing the requirement, then judge the two English texts without seeing the artifact) beat a direct single-call judge by 8.2–9.8 points of macro recall, and by 4.2–6.0 points over a single call given the same rewrite list. **Its labels come from how each row was built (mutation rule, Dafny or Lean equivalence proof, or source benchmark), not from humans judging intent.** So it measures agreement with a gold original. It does not measure faithfulness to intent as judged by people, and it reports no judge precision against human labels.

### Cited findings
- **Citation, corrected:** Martin Amster, One An, Holly Baker, Fernanda Graciolli, Simon Henniger, Nada Amin, "claimcheck: Measuring and Improving Specification Faithfulness", arXiv 2610.17358v1, 12 Oct 2026, cs.CL. The PDF footer reads "NeurIPS 2026 Workshop on AI for Verifiable Coding". The authors are Apart Secure Program Synthesis fellows, with Harvard and Midspiral affiliations. The acknowledgments say the tool was "initially developed as part of a Claude Code hackathon" — [arXiv API + PDF](https://arxiv.org/abs/2610.17358)
- **Grade A-workshop** (workshop acceptance as stated in the PDF footer, not checked on OpenReview). **Full text: yes.** **The authors evaluate their own tool (TA).** — [PDF](https://arxiv.org/pdf/2610.17358v1)
- **The quoted claim is verbatim:** "We introduce claimcheck, a tool that checks whether a formal artifact means what its natural-language requirement asks for." — [§1](https://arxiv.org/pdf/2610.17358v1)
- **n and domain.** 3,234 rows in four slices:
  - **Dafny: 362 rows** from CloverBench, i.e. 62 hand-written textbook programs. Docstring = requirement; artifact = the contract with the body stripped.
  - **PutnamBench competition-maths theorem statements:** Lean 1,296, Isabelle 920, Rocq 656.
  — [§2](https://arxiv.org/pdf/2610.17358v1)
- **How labels were made.** No human intent labels.
  - Dafny: the 62 originals are "confirmed". Clover's mutation classes C1 (docstring mutated, 62), C2 (contract mutated, 60) and C6 (contract and body, 60) are "disputed". 118 meaning-preserving control rewrites stay "confirmed"; each was kept "only if Dafny proves the rewritten contract equivalent to the original".
  - PutnamBench: five propositional control rules (proved per row in Lean, argued per rule in Isabelle and Rocq) and four semantic mutation rules (negate, forall_to_exists, bump_const, strictness) labelled "by their construction".
  - Controls are 1,029 of the 1,854 confirmed rows. The Limitations section concedes that the semantic labels "rest on the rule that produced them, and for bump_const and strictness that is intent alone".
  — [§2, §7](https://arxiv.org/pdf/2610.17358v1)
- **The defective Dafny rows pass verification.** "All 182 defective rows still verify in Dafny". This illustrates directly that M ⊨ A says nothing about A ≡ R. — [§2.1](https://arxiv.org/pdf/2610.17358v1)
- **Method and models.** Informalizer claude-haiku-4.5, which never sees the requirement. Judge claude-sonnet-4.6, which compares the requirement with the informalization and does not see the artifact. Temperature 0. One row per call. — [§3–4](https://arxiv.org/pdf/2610.17358v1)
- **Baselines.**
  - (1) A zero-shot single call shown the requirement and the artifact, answering YES/NO with no system prompt.
  - (2) The same call plus the judge's verbatim rewrite list and error vocabulary ("baseline + list").
  — [§4](https://arxiv.org/pdf/2610.17358v1)
- **Main results** (macro recall = mean of confirmed and disputed recall, 95 % CI):

  | | Lean | Isabelle | Rocq | Dafny |
  |---|---|---|---|---|
  | Zero-shot baseline | 79.7 | 81.5 | 79.6 | 84.0 |
  | Baseline + list | 83.2 | 85.3 | 83.0 | 88.9 |
  | claimcheck | 87.9 | 91.3 | 88.0 | 93.1 |

  — [Table 2](https://arxiv.org/pdf/2610.17358v1)
- **Where the gain comes from.**
  - Most of it is on faithful rows: confirmed recall rises from 66.5–85.6 % to 77.8–91.7 %.
  - Disputed recall rises on Dafny (92.3 → 94.5 %), falls by at most 3.3 points on Isabelle and Rocq, and falls on Lean (95.9 → 88.4 %).
  - Paired McNemar tests favour claimcheck on all four slices; Dafny 24 vs 9, p = 0.014.
  — [§5.1](https://arxiv.org/pdf/2610.17358v1)
- **Ablations.**
  - Removing the back-translation costs 2.8–6.0 points.
  - **Letting the informalizer see the requirement costs 0.8–3.0 points, all of it on the disputed side** (disputed recall −6.0 to −8.8 points).
  - Letting the judge see the artifact costs 1.4–4.5 points.
  - Holding out rewrite rules changes the score by ≤ 0.8.
  — [§5.2, Table 3](https://arxiv.org/pdf/2610.17358v1)
- **Model sweep.** The gain is "substitutive rather than additive":
  - gpt-5.6-luna gains 18.6–25.2 points and deepseek-v4-pro 6.2–27.5.
  - gemini-3.7-flash already reaches 91.4–94.8 in a single call and stays within a point of its list baseline.
  - Sweep rows use the variant in which the judge also sees the artifact.
  — [§5.3, Table 4](https://arxiv.org/pdf/2610.17358v1)
- **Limitations, in the authors' words.**
  - "negate is 92% and 83% of the disputed rows" on Isabelle and Rocq.
  - Trivial wrappers are ~45 % of those rows.
  - "all four slices are single contracts or single theorem statements"; artifacts "whose meaning lives in their structure … are outside what we measure".
  — [§7](https://arxiv.org/pdf/2610.17358v1)
- **Precision is not reported.** Results are macro recall only. No human-labelled audit of judge verdicts. — [§5](https://arxiv.org/pdf/2610.17358v1)
- **Its related-work section cites prior judge evidence the branch already uses:**
  - FormalAlign: a GPT-4 judge "had far lower precision".
  - Verus-SpecGym: "a judge misses a quarter of the specification failures its executable evaluator catches".
  - Mathesis: the round trip "lost on F1, 0.65 to 0.85".
  So claimcheck's positive result is not uncontested in its own field. — [§6](https://arxiv.org/pdf/2610.17358v1)

### Inferences
- *Inference (own calc from Table 2 and §2 counts; rows scored on answered items, ≤ 12 unanswered per run).* Dafny slice: 182 disputed and 180 confirmed rows; disputed recall 94.5 %, so confirmed recall ≈ 2·93.1 − 94.5 = 91.7 %. A "disputed" verdict is then right ≈ 172 / (172 + 15) ≈ 0.92 of the time. This is precision against **construction labels**, not against humans, on textbook contracts at ~50 % prevalence. It cannot be compared with FormalAlign's 26–51 % (21 negatives per positive).
- **Agents.** LLMs do both steps, and the result is the macro recall above. **Transfer: analogous.** Dafny contracts on textbook functions are closer to API behaviour specs than maths is, but they are single pure-function contracts, with no state, no environment actions and no non-commitments.
- **Delta 1: [V] §5 open question 3 and [S] §5 Q8 are qualified, not answered.** Old text, verbatim: "3. What is the precision of LLM faithfulness judges on API or behaviour specs? All measurements are maths/Lean; the correlation data are MCQ." claimcheck adds a Dafny program-contract slice, so "All measurements are maths/Lean" is no longer strictly true. It still gives no precision against human labels, and none on API specs. The question stays open. TD's calibration (30 "violation" + 30 "fine" verdicts, two blind raters) is still needed.
- **Delta 2: [V] Part 3 R3 and R4 are confirmed in direction; confidence is unchanged.**
  - R3, verbatim: "Added-commitment probe judged spec-blind; every 'not addressed' goes to a human | inference + analogous (NeuroSTAR) | low". claimcheck's ablations are measured evidence that withholding information from a judge helps. The judge that does not see the artifact beats the one that does by 1.4–4.5 points, and the informalizer that does not see the requirement beats the one that does. This fits the branch's information-flow principle.
  - R4, verbatim: "Cross-family judges must agree to accept; human on rejection; calibrate and recalibrate on model change". claimcheck tests no cross-family agreement rule. Its sweep shows the gain depends on the judge, which supports "recalibrate on model change".
  - Confidence stays low / low–medium: TA, workshop paper, construction labels, maths-heavy.
  - *Inference:* a candidate design for the judge gate is "blind informalization, then compare". TD could add it as an arm when calibrating judges. That is a suggestion, not a change.
- **Delta 3: no change** to Pipeline A or to the §2.6(c) search result. claimcheck is a checking tool, not a pipeline.

### Gaps
- Workshop acceptance not confirmed on OpenReview or the workshop site; the PDF footer is the only evidence.
- The repo (github.com/metareflection/claimcheck) was not cloned, so per-class confusion matrices were not checked.
- No human-intent audit exists in the paper.

---

## L3: Automotive LLM + formal methods workflow (DOI 10.1007/978-3-032-26220-2_31)

### Takeaway
The chapter exists. It is a peer-reviewed FM 2026 paper (LNCS 16557), open access. It does separate M ⊨ A (an FDR4 CEGAR-style repair loop) from A ≡ R (expert review of requirement–assertion pairs, ending in a "golden standard" with a traceability matrix, coverage report and documented limitations).

**The brief's "cross-model review run for five rounds with 'faithful' as a gated verdict" is not in the paper or its 72-page appendix.**
- Every experiment uses one model (Claude 4.5 Sonnet).
- "five" refers to "Each case study is run five times for consistency" (synthesis repeats).
- "faithful" appears once, in the A ≡ R sentence.

Measurement of the A ≡ R gate is thin:
- one case (CS1, 23 assertions), 3 expert reviewers;
- no gold and no ground-truth error set;
- the expert verdicts *are* the label;
- the counts in the main paper and its own appendix disagree.

It is a published prose → formal model pipeline with a **human** faithfulness gate against the prose. It stops before any reference model or implementation.

### Cited findings
- **Citation, corrected (Crossref).** Zipong Lim, Bozhi Wu, Yon Shin Teo, Shang-wei Lin, Yi Li, "Shift-Left Requirements Verification: Integrating LLMs and Formal Methods for Automotive Systems", in A. Sampaio and M. Stoelinga (eds.), *FM 2026*, LNCS 16557, pp. 631–650, Springer Cham, 2026. CC BY 4.0, version of record dated 18 May 2026. Affiliations: NTU Singapore, AUMOVIO (formerly Continental Automotive), AUMOVIO-NTU Corporate Lab, Singapore Institute of Technology. — [Crossref](https://api.crossref.org/works/10.1007/978-3-032-26220-2_31); [Springer PDF](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **Grade A** (FM 2026 main proceedings). **Full text: yes**: the Springer PDF (20 pp.) plus the authors' version with appendices (72 pp.) from the paper's supplementary site. **Authors evaluate their own workflow (TA)**; two authors are at the industry partner. — [supplementary site](https://sites.google.com/view/shift-left-requirement-supp)
- **The M ⊨ A vs A ≡ R separation is verbatim:** "While refinement guarantees that the model satisfies the assertions (M |= A), it does not ensure that the assertions faithfully capture the intent of the original requirements (A ≡ R). This validation addresses this gap through human–LLM collaboration." — [§3.2, p. 638](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **What experts review.** Each pair comes with "the original requirement, the corresponding CSP assertion, an LLM-generated natural-language back-translation …, an LLM confidence score (0-1) with rationale …, and the verification evidence". Experts check "semantic alignment, completeness, abstraction adequacy, and case coverage". Verdicts are Approved / Modified / Rejected. Approved assertions form "the golden standard specification Agolden, together with a traceability matrix, coverage report, and documented limitations". — [§3.2](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **The back-translation step sees the requirement.** Prompt L.6 supplies "1. The original requirement in natural language 2. The generated CSPM assertion" and tells the model to "Relate the assertion back to the original requirement". — [appendix L.6, author PDF](https://sites.google.com/view/shift-left-requirement-supp)
- **CEGAR loop.**
  - All assertions are checked in parallel with FDR4, 60 s timeout each.
  - Failed assertions and their counterexample traces go to the LLM, which edits the model and, "only when necessary", the assertions.
  - The loop stops on success, oscillation, no progress, or 20 iterations.
  - The authors name the risk: "assertion weakening, where the loop converges by relaxing properties rather than correcting the model". Their mitigation: changes are logged and shown to experts; after the golden standard, "assertions become immutable and only model refinement is permitted".
  — [§3.2, Algorithm 1](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **Setting.** Three proprietary automotive cases: CS1 grille shutter (23 requirements), CS2 sunroof (56), CS3 remote-services gateway (83). Claude 4.5 Sonnet with FDR4, each case run 5 times. — [§4.1, Table 1](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **RQ1 (M ⊨ A synthesis success):** CS1 5/5, CS2 4/5, CS3 2/5. — [Table 2](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **RQ2 (A ≡ R, CS1 only, 23 assertions).** Main paper: "14 out of 23 assertions (61%) required no changes", 22 % minor changes, 17 % major revisions. Mean confidence by group is 0.81 / 0.74 / 0.59, and the authors claim confidence scores "correlate strongly with correctness". No statistical test; n = 23. Table 4 lists per-reviewer counts R1 16/3/4, R2 18/1/4, R3 18/2/3. — [§4.3, Tables 3–4](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **The appendix contradicts the main paper.** Appendix Table 7, the per-assertion data, gives consensus Approve for 8 assertions (G-2, 3, 4, 17, 20, 21, 24, 26), Minor for 9, Major for 6 (G-0, 1, 16, 25, 30, 31). The main text says 14/5/4. J.3 says "11 assertions requiring minor changes", and J.4 says "4 assertions requiring major revisions" but lists five. J.2 classes G-0 and G-1 as "Full Disagreement (0/3)", yet Table 7 shows M/M/M for both. Inter-reviewer agreement: 10/23 unanimous (43 %). — [appendix J, author PDF](https://sites.google.com/view/shift-left-requirement-supp)
- **What the reviewers caught** (appendix J): added commitments ("Bidirectional channel not in requirement (hallucination)", "CLOSE level incorrectly added", "5-level discretization not in requirement"), semantic mismatches ("acquire" vs "provide"), over-strict sequential composition, and missing context. — [appendix Table 7](https://sites.google.com/view/shift-left-requirement-supp)
- **RQ3 (domain-knowledge validation).**
  - 29 candidate properties generated from retrieved historical defects; 23 failed FDR4, and these were "subsequently reviewed by domain experts who confirmed their validity as genuine requirement deficiencies".
  - 1/1 known defect detected; 22 "novel" gaps.
  - Each gap gets a report with the FDR4 trace, an LLM explanation and recommended actions. Stakeholders then accept, mitigate, reject or defer.
  — [§3.3, §4.4, Table 5](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **RQ4 (cost):** 10–35 min, $1.80–7.80 API cost per project, "< 1 hour expert validation time". — [§4.5, Table 6](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)
- **Single model:** "we did not conduct systematic comparisons across models". — [§6](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)

### Inferences
- **The brief's claim does not hold.** "a cross-model review run for five rounds with 'faithful' as a gated verdict" is **not supported** by the full text or the appendix. *Inference:* the other tool conflated the five synthesis repeats and the three-reviewer review into a "cross-model, five-round" gate. The gate that exists is a human Approve/Modify/Reject review, LLM-assisted, with one model family.
- **§5(a) for L3: expert judgement only.** The A ≡ R measurement is the three experts' verdicts on 23 CS1 assertions. There is no gold formula, no seeded misreadings and no independent ground truth, so the gate's recall on wrong assertions cannot be computed. The internal inconsistency (14/5/4 vs 8/9/6) lowers confidence even in that figure. RQ3's "22 novel gaps" are likewise expert-confirmed, with no external check.
- **§5(c): partly yes.** It is a published end-to-end pipeline: NL requirements → LLM classification (expert-confirmed) → sequence diagram (expert-validated) → CSP model + assertions → FDR4 CEGAR (M ⊨ A) → expert A ≡ R gate per pair → immutable golden standard → model-only refinement → RAG gap properties. The A ≡ R gate faces the prose, and it is human. **It has no reference model or implementation layer** (no analogue of G6–G8), no spec-blind check set and no machine-checked faithfulness gate.
- **Comparison with Pipeline A ([DD] §3.3 and [S] §3)**, *Inference*:

  | Pipeline A | Lim et al. |
  |---|---|
  | Record-derived checks written before the spec, by a records-only session | Back-translation LLM sees both requirement and assertion |
  | Checks screened against ≥ 2 wheats and chaffs (G2 a–c) | No wheat or chaff screening |
  | Spec-blind judge, separate lineages | One model (Claude 4.5 Sonnet) does translation, repair, back-translation and confidence; independence comes only from the human reviewers |
  | Vacuity gate (G5) before trusting passes | No vacuity gate |
  | — | Freezes accepted assertions as immutable before final refinement, an explicit guard against agent assertion-weakening |
  | Covers prose → spec → formal core → R | Stops at the formal model |

  The freeze is not stated as a gate anywhere in [DD] §3.2. *Inference:* Pipeline A's G2 already keeps record checks fixed, but the CEGAR-style "agent may edit A while repairing M" risk is not named for the formal core.
- **Cross-lead (L2 × L3), *Inference*.** L3's back-translation sees the requirement. L2 measured that setting as worse: −0.8 to −3.0 macro recall and −6.0 to −8.8 disputed recall. L3's expert aid is therefore of the kind L2 found prone to echoing the requirement. L3 did not measure this.
- **Agents.** LLMs did the formalization and repair steps (synthesis success 40–100 %). The faithfulness step was human, with the LLM aiding (61 % or 35 % no-change, depending on which table is read). **Transfer: analogous** (automotive reactive requirements in CSP, not library or API specs).
- **Delta 1: [V] §2.6(c) is qualified, not overturned.** Old text, verbatim: "**(c) Is there a published pipeline doing prose → spec → model → reference model with faithfulness gates?** *Result: none found by the earlier run's search* (a search result, not proof of absence)". The result still holds for the full chain to a reference model. The writer should add Lim et al. (FM 2026, A) to the "nearest pipelines" list: it covers prose → formal assertions → formal model with a human A ≡ R gate and an LLM CEGAR repair loop. It is weakly measured (one case, 23 assertions, internally inconsistent counts) and has no R layer. The old line "Agents are measured in none of the closely fitting pipelines" needs qualifying: agents are measured here for synthesis success, not for faithfulness.
- **Delta 2: no change to Pipeline A's recommendations.** Optional addition for the writer, labelled *Inference*: an "assertion freeze" rule. Once a clause or formal assertion passes G2 and human review, agents repairing models may not edit it; any edit re-enters G2. Lim et al. motivate this but do not measure it.
- **Bearing on brief §1 Q1** (counterexamples → questions for the decision-maker), for the report writer:
  - L3's gap reports turn FDR4 counterexamples for failed defect-derived properties into stakeholder decisions (accept/fix, mitigate, reject, defer). 23 reports were produced; all were expert-confirmed; 1/1 known defect was found.
  - The historical-defect database acts as an external checklist, so this is a way to raise questions the requirements did not raise. It is not "questions no checklist raises".
  - Measurement: expert confirmation only, TA, n = 29 properties over 3 cases.

### Gaps
- The appendix PDF is the authors' version on Google Drive; it was not checked against the Springer supplementary material, and Springer's PDF has no appendix.
- Who the three reviewers were, and whether they were authors, is not stated.
- No per-assertion ground truth exists, so the A ≡ R gate's miss rate cannot be computed.

---

## L6: Reference equivalence by bidirectional implication (arXiv 2610.10604)

### Takeaway
The paper exists. It is a workshop **evaluation-framework** paper, not a method that gates on intent. "Bidirectional implication" is BEq+ (from Poiroux et al., EMNLP 2025): Lean proof search for candidate ⊢ reference and reference ⊢ candidate, against the **dataset's reference specification** (VERINA, CLEVER). It is a gold-agreement metric, and the authors say so: "Reference agreement and finite tests do not establish fidelity to the natural-language requirement." In their runs BEq+ almost never succeeded: 0.000–0.021 on VERINA and 0.000 on CLEVER. Failure counts as inconclusive, not as non-equivalence.

### Cited findings
- **Citation, corrected:** Srijith Nair, Aditya Vempaty, Jia Liu, Ashish Jagmohan, "Beyond Type-checking: Towards Holistic Evaluation of Formal Specification Generation", arXiv 2610.10604v1, 7 Oct 2026, cs.SE. arXiv comment: "Accepted at NeurIPS 2026 Workshop on AI for Verifiable Coding (20 pages, 7 figures)". Affiliations: Ohio State University and Emergence AI. — [arXiv API](https://arxiv.org/abs/2610.10604)
- **Grade A-workshop** (acceptance per the arXiv comment, not independently confirmed). **Full text: yes.** It evaluates existing pipelines plus a framework the authors built; the authors' own framework is under test (TA for the framework). — [PDF](https://arxiv.org/pdf/2610.10604v1)
- **The BEq+ definition is verbatim:** "BEq+ (Poiroux et al., 2025) attempts to prove the bidirectional implication: E, π(Q̂) ⊢ π(Q) and E, π(Q) ⊢ π(Q̂) … Failure to find either proof is classified as inconclusive, since search failure does not establish non-equivalence." The check is a Lean kernel-checked proof search, not an SMT decision procedure. — [§2.3](https://arxiv.org/pdf/2610.10604v1)
- **The reference is the dataset's reference specification.** Inputs listed: "the reference specification available in the dataset" alongside "the natural-language statement (user's intent)". The paper does not say whether the references were hand-written. — [§2.1](https://arxiv.org/pdf/2610.10604v1)
- **n and setting.**
  - 350 Lean tasks (189 VERINA, 161 CLEVER).
  - Four SpecGen configurations (direct prompt, VERINA pipeline, CLEVER few-shot, LeanAide), all on GPT-5.6 (Sol).
  - 756 + 644 task–configuration records.
  — [§2.2, §3.1](https://arxiv.org/pdf/2610.10604v1)
- **BEq+ results.** VERINA tasks: 0.000 [189], 0.021 [189], 0.011 [94], 0.011 [181]. CLEVER tasks: 0.000 for all four configurations. LeanScorer, an LLM judge of intent alignment, gives 0.655–0.755 on VERINA. — [Appendix Table 3](https://arxiv.org/pdf/2610.10604v1)
- **Main reported finding.** Restricting GTED to 32 jointly measurable VERINA tasks moves the VERINA configuration from 2nd to 4th. An authored control with precondition False scores R+ = R− = 1 but required-input recall 0. — [Abstract, §3.2, App. B.4](https://arxiv.org/pdf/2610.10604v1)
- **The authors limit their own claims:** "Reference agreement and finite tests do not establish fidelity to the natural-language requirement"; "These measurements characterize the recorded representations … rather than establishing intent fidelity"; "Independently reviewed references and checked counterexamples could strengthen evaluation against user intent." — [§3.2, §4](https://arxiv.org/pdf/2610.10604v1)
- **Behavioural evaluation was largely broken.** Of 469 behavioural non-passes, "357 (76.1%) carry explicit harness errors". — [§3.2](https://arxiv.org/pdf/2610.10604v1)

### Inferences
- **§5(a) for L6: gold agreement only**, by the authors' own statement. Bidirectional implication is checked by Lean proof search against the dataset reference. Its success rate here (≤ 2.1 %) makes it nearly uninformative as a gate in practice: an inconclusive result neither passes nor fails. *Inference:* a BEq-style gate against a reference would almost always return "inconclusive" for generated specs. It is usable only as a sufficient-condition pass signal.
- **Agents.** The LLM (GPT-5.6) generated the specs. No agent did the equivalence step (proof search). **Transfer: analogous** (Lean, pure functions).
- **Delta: no change.** It bears on [V] §2.1's metric ladder. Old text, verbatim: "From weakest to strongest metric (*Inference*): syntax valid < exact match < equivalence to one gold < human intent judgement < detection of real errors." L6 confirms that ordering and that "equivalence to one gold" sits below intent: its authors say it does not establish fidelity. It adds one point the writer may note: Lean proof-search equivalence to gold succeeds rarely (≤ 2.1 % here), so "inconclusive" dominates. It does not touch Pipeline A, which uses no gold reference formula. It does not touch §2.6(c), since L6 is not a pipeline.

### Gaps
- Whether VERINA and CLEVER references are human-written was not verified this run: L6 does not say, and the source benchmark papers were not opened because they are out of scope. *Inference:* both benchmarks describe curated references, but this is unverified here.
- Workshop acceptance not independently confirmed.

---

## Answers bearing on brief §1 questions

### Takeaway
- **Q2 (a measured A ≡ R check): yes, partly, from L2 only.** It is measured against construction labels, not human intent. L3's A ≡ R gate is human and barely measured. L6 is gold agreement and is explicitly not intent.
- **Q3 (a published end-to-end pipeline with faithfulness gates against prose):** L3 is the closest found. It has a human gate and stops at the formal model, with no reference model. [V] §2.6(c) is qualified, not overturned.

### Cited findings
- **Q2.** claimcheck measures an automated A ≡ R judge over 3,234 rows with labels "established by execution, by proof, or by the benchmark it is drawn from": 87.9–93.1 macro recall vs 79.6–84.0 for a direct judge. Precision against human labels is not reported. — [claimcheck](https://arxiv.org/pdf/2610.17358v1)
- **Q2.** Lim et al. state the M ⊨ A vs A ≡ R distinction explicitly and gate A ≡ R by expert review, but measure it only as expert outcome counts on 23 CS1 assertions, inconsistently reported. — [FM 2026](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf); [appendix](https://sites.google.com/view/shift-left-requirement-supp)
- **Q2.** Nair et al.'s BEq+ is reference equivalence; "Reference agreement … do[es] not establish fidelity to the natural-language requirement". — [arXiv 2610.10604](https://arxiv.org/pdf/2610.10604v1)
- **Q3.** Lim et al. call their contribution "An end-to-end industrial workflow synthesizing formal CSP system models from free-form natural-language requirements". — [§1](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)

### Inferences
- **Held-back judge gates** ([V] Part 3 R3 "low", R4 "low–medium"; [S] §5 Q8; [TD] §2.4, §4.2). Nothing here licenses raising them.
  - L2 is TA, workshop, construction-labelled, maths-heavy, with single pure-function Dafny contracts as the nearest analogue.
  - L2 supports the *design* principle behind R3 (keep the judge blind to what would anchor it) and supports recalibrating on model change (R4).
  - The calibration on human-labelled API-spec clauses that the branch already plans is still the deciding measurement.
- **Recommendations changed by L2, L3 or L6: none.**
  - Qualifications for the writer: [V] §5 Q3 wording ("All measurements are maths/Lean") and [V] §2.6(c) nearest-pipelines list (add Lim et al.).
  - Optional *Inference* additions: an assertion-freeze rule; a blind-informalization arm in TD's judge calibration.
- **Brief §1 Q1** (counterexamples → questions): L3's FDR4-counterexample gap reports go to stakeholders for decision. They are expert-confirmed only (23/23 "valid", 1/1 known), with no measure of question quality. The defect database acts as an external checklist.

### Gaps
- None of the three measures intent faithfulness with independent human labels on a non-maths, stateful specification.

---

## Verification debt
1. Workshop acceptance for L2 and L6 (NeurIPS 2026 Workshop on AI for Verifiable Coding) is self-reported (PDF footer, arXiv comment). Not checked on OpenReview or the workshop page.
2. L3's appendix comes from the authors' Google Drive link on their supplementary site and may differ from Springer's ESM. The 14/5/4 vs 8/9/6 inconsistency is reported as read and has not been raised with the authors.
3. L3's reviewer identities, and whether they were independent of the authors, are not stated.
4. The claimcheck repository (per-class results, released earlier runs including a SQL slice) was not inspected.
5. Whether L6's references (VERINA, CLEVER) are human-written was not verified.
6. The precision figure derived for claimcheck on Dafny (≈ 0.92) is own arithmetic from macro and disputed recall and class counts. It ignores up to 12 unanswered rows.

## Self-check
- **"Held-back judge gates" read as** [V] Part 3 R3 and R4 (low and low–medium confidence) plus the TD judge-calibration measurement ([S] §5 Q8). If the brief meant a different set of gates in [DD], the deltas above may need re-mapping. I found no explicit "held back" wording in [DD] by grep.
- **"Cross-model review … five rounds"** is judged *not supported* after searching both the 20-page chapter and the 72-page appendix: "five" occurs only as "run five times for consistency", and "faithful" occurs once. A later version could contain it, but none was found.
- **The L3 appendix arithmetic** (8/9/6 from Table 7) is my count of the "Consensus" column. J.3 and J.4 give yet other numbers (11 minor, 4 major), so the source is internally inconsistent; I did not resolve which count is right.
- **claimcheck grade and roles.** Workshop papers are graded A-workshop per brief §4. An Anthropic hackathon origin is acknowledged; I treat the authors as tool authors (TA), not as independent evaluators.
- **L6 is graded on what its own text says.** I did not read Poiroux et al. for BEq+ internals; the "proof search, not SMT" description comes from L6's §2.3.
