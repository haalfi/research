# T5 Independence (minimal) + disconfirming searches §5(a) and §5(c)

Scope: only what T1–T4 need. Full texts were fetched from arXiv, the authors' own PDFs or Europe PMC unless marked **[unreachable]**. Grades follow brief §6. *Inference* marks my own reasoning. Brief §3 items (Clover, ClarifyGPT, nl2postcond, SpecGen, "notation alone does not beat prose", and so on) are not re-surveyed here.

---

## Q1. Common-mode error, independent derivation, refuter roles, and the limits of LLM self-checking and LLM-as-judge for spec faithfulness

### Takeaway
LLM errors are strongly correlated across models. They are most correlated within one provider or architecture and among the most accurate models. A judge from the same lineage inflates the scores of answers that share its errors. An LLM checking its own work without outside feedback does not reliably improve, and sometimes gets worse. Debate adds little beyond majority voting.

What has measured gains is (a) checking against an artefact that was derived independently or can be executed, and (b) critics trained adversarially on deliberately planted bugs. The strongest *spec-validation* evidence (Arm v8-M, JEST/ESMeta) is human or tool evidence: an independently written second description, compared mechanically, found bugs that heavy testing had missed.

### Cited Findings

**Classical N-version / common-mode (human-only evidence)**
- Knight & Leveson 1986 (IEEE TSE): **[unreachable]**. sunnyday.mit.edu returned 503 and then reset the connection, and the UVA mirror returned 403. The usual summary (27 independently written versions, about 1M test inputs each, independence of failures statistically rejected) is from training knowledge only and could not be re-checked. Eckhardt–Lee and Littlewood–Miller: not fetched; treat as leads. Grade would be A if fetched.
- Arm, Reid 2017, "Who Guards the Guards?" (OOPSLA, **A**, full text). Reid names common-mode failure as the reason that testing a spec against implementations or test suites misses bugs: "the specification and the implementation do the same wrong thing". As a remedy he writes a second, high-level property set, built from the natural-language manual, from past bugs and from discussion with architects. The design rule is that the properties must "describe the architecture differently from the existing specification to reduce the risk of common-mode failure". Manual rules that "simply repeated information found in the formal specification in much the same structure" were rejected as "prone to common-mode failure". The property set was checked formally against the executable ASL spec and found **12 bugs (2 security)** in a spec that had "previously been extensively tested". All 12 were fixed by Arm. Agents: none (human-only evidence). Meaning of "correct": the property holds over the ASL transition function. [Reid 2017](https://alastairreid.github.io/papers/oopsla2017-whoguardstheguards.pdf)
- JEST (ICSE 2021, **A**, Distinguished Paper; ESMeta lineage). "N+1-version differential testing": synthesised programs run on N JavaScript engines plus the executable semantics mechanically extracted from the ECMAScript spec. Where most engines disagree with the spec model, the bug is attributed to the spec. Spectrum-based fault localisation then locates it. In ES11 it found **27 specification bugs** and **44 engine bugs** across 4 engines, using 1,700 synthesised programs covering 97.78% of syntax and 87.70% of semantics. Agents: none. *Inference*: this is the clearest published mechanism that uses several independently built artefacts to detect spec errors rather than to confirm them. [JEST, arXiv 2102.07498](https://arxiv.org/pdf/2102.07498)

**Correlated errors across LLMs (agents measured)**
- Kim, Garg, Peng, Garg 2025, "Correlated Errors in Large Language Models" (ICML 2025, **A**). Data: 349 LLMs on 12,032 MCQs (HuggingFace leaderboard), 71 LLMs on 14,042 MCQs (HELM), 20 LLMs on 1,800 résumé–job pairs. When both models in a pair are wrong, they pick the same wrong answer 0.423 of the time on HuggingFace (random baseline 0.127) and **0.60 on HELM** (random baseline 0.33). 100% of HF pairs and 97.5% of HELM pairs exceed the baseline. The same developer, the same base architecture and similar size all predict higher agreement. **More accurate models have more correlated errors, even with different architectures.** In the LLM-as-judge case study, each judge inflates the accuracy of models weaker than itself and deflates stronger ones. Inflation is worst for models from the judge's own provider. "Correct" here means the MCQ gold label. [Kim et al.](https://arxiv.org/pdf/2506.07962)
- *Inference*: for a pipeline in which agents from one family read, specify, model and test, this predicts that misreadings of the prose are shared rather than independent. Switching to a stronger model or a different provider reduces the correlation but does not remove it. Independence has to come from the *artefact and the derivation path* (as in Reid's "describe it differently"), not only from swapping the model.

**Self-correction limits (agents measured)**
- Huang et al. 2024, "LLMs Cannot Self-Correct Reasoning Yet" (ICLR 2024, **A**). With intrinsic self-correction (no external feedback), GPT-3.5 falls from 75.9 to 74.7 on GSM8K, from 75.8 to 41.8 on CommonSenseQA and from 26.0 to 25.0 on HotpotQA after 2 rounds. GPT-4 falls from 95.5 to 89.0, 82.0 to 80.0 and 49.0 to 43.0. Earlier reported gains came from using oracle labels to decide when to stop. [Huang et al.](https://arxiv.org/pdf/2310.01798)
- Kamoi et al. 2024 (TACL survey, **A**). No prior work shows successful self-correction from prompted-LLM feedback, except on tasks exceptionally suited to it. Self-correction works when **reliable external feedback** is available, and large-scale fine-tuning can enable it. [Kamoi et al.](https://arxiv.org/pdf/2406.01297)

**Judge bias and reliability (agents measured)**
- Panickssery, Bowman, Feng 2024 (NeurIPS 2024, **A**). Setting: summarisation. LLM evaluators recognise their own outputs; GPT-4 is 73.5% accurate at distinguishing itself out of the box. Self-preference strength rises linearly with self-recognition ability, and fine-tuning for self-recognition increases self-preference. [Panickssery et al.](https://arxiv.org/pdf/2404.13076)
- CodeJudgeBench (Jiang et al. 2025, **A-pre**). 26 judge models judged code generation, repair and unit-test generation. Thinking models do best, but all show "significant randomness". Swapping the order of responses changes accuracy by up to 14%. Accuracy also varies with which LLM wrote the candidate. Pairwise judging beats pointwise scoring. "Correct" means a candidate's pass or fail on hidden tests. [CodeJudgeBench](https://arxiv.org/pdf/2507.10535)
- Jin & Chen 2026, "Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement" (**A-pre**). Over 700 tasks from HumanEval, MBPP and QuixBugs. LLMs often judge *correct* code as not meeting the NL requirement. More detailed prompts that ask for explanations and fixes make this worse. *Inference*: an LLM faithfulness judge that is asked to justify its verdict will lean towards false "unfaithful" alarms. That costs reviewer time but is safer than false acceptance. [Jin & Chen](https://arxiv.org/pdf/2603.00539)
- Broccia, Frattini, …, Ferrari 2026 (**A-pre**). Controlled crossover, n=34 (novice) inspectors finding requirement smells in textual specs. **LLM support lowered smell-detection accuracy** (Bayesian model), did not affect classification or time, and slowed learning when used from the start. *Inference*: putting an LLM in the loop for human review of prose is not automatically a gain. [Broccia et al.](https://arxiv.org/pdf/2608.21298)

**Multi-agent debate (agents measured)**
- Smit et al. 2024, "Should we be going MAD?" (ICML 2024, **A**). MAD systems "do not reliably outperform" self-consistency or multi-path ensembling. Some improve only after hyperparameter tuning, for example of agreement level. [Smit et al.](https://arxiv.org/pdf/2311.17371)
- Choi, Zhu, Li 2025, "Debate or Vote" (**A-pre**, later revision). Across 7 NLP benchmarks, **majority voting accounts for most of MAD's gain**. The authors prove that debate induces a martingale over belief trajectories, so debate alone does not raise expected correctness. Only interventions that bias updates towards correction help. [Choi et al.](https://arxiv.org/pdf/2508.17536)

**Adversarial / refuter roles with measured gains (agents measured)**
- CriticGPT, McAleese et al. 2024 (OpenAI, **A-pre**). The GPT-4-based critic was trained with RLHF on code into which human contractors had *adversarially* inserted bugs; the contractors could see a critic while inserting. On code with human-inserted bugs, LLM critics catch substantially more inserted bugs than paid human code reviewers (Fig. 1b). Model critiques are preferred over human ones more than 80% of the time on inserted bugs and 63% on naturally occurring bugs. Critics hallucinate bugs. Human+CriticGPT teams match the model's recall with fewer hallucinations. Setting: real assistant code tasks, not specs. [CriticGPT](https://arxiv.org/pdf/2407.00215)
- *Inference*: the gain comes from training on planted defects, which is close to the "mutant reference model" seed in brief §3 and to T4 spec mutation. No paper found measures an LLM refuter on *spec-vs-prose* mutants.

**LLM judgement of formalisation faithfulness (agents measured, maths domain)**
- Zhang et al. 2026, "Beyond Compilation" (**A-pre**, v4 Oct 2026). Setting: NL to Lean 4 statements, 227 university-level statements, 8 systems. "Faithful" means it compiles **and** two judges from *different model families* (GPT-5.2, Gemini-2.5-Pro) agree. On an independent random audit this criterion agrees with the human majority on 91.5% of cases. It rarely accepts unfaithful outputs but rejects some faithful ones. Their tool-augmented agent compiles 87.2% but only 57.7% are accepted. Human review confirms that 23.8 of the 29.5-point gap are real translation errors. Lean feedback produces most of the compile gain, and nearly half of that gain fails the semantic criterion. **Judge aging/lineage effect:** GPT-5.2 accepts 83% of statements from two newer models, but review finds only 4 of their 54 rejections (7%) are real errors. So most of the measured gap for strong systems is judge error, and "the fewer errors a system makes, the smaller the share of its rejections that are translation errors". [Beyond Compilation](https://arxiv.org/pdf/2606.31002)
- MathAtlas 2026 (**A-pre**). Faithfulness judges do not transfer across domains. CriticLean-32B scores 82.6 on ConsistencyCheck and 86.4 on CriticLeanBench, but 80.0 on in-the-wild definitions and 75.0 on statements (MA-Align, n=200). GPT-5.2 with an engineered few-shot prompt scores 82.1/79.0/86.0/80.0. The in-domain few-shot examples may favour GPT-5.2. [MathAtlas](https://arxiv.org/pdf/2605.14061)
- FormalAlign 2024 (**A-pre**; ICLR 2025 per later listings, not verified). A trained alignment scorer beats GPT-4 on detecting synthetic misalignments: 99.21% vs 88.91% on FormL4-Basic and 66.39% vs 64.34% on MiniF2F-Valid. "Correct" is measured against *synthetic* misalignment strategies, not natural errors. [FormalAlign](https://arxiv.org/pdf/2410.10135)
- Mohammad & Sheikh 2026, "The Faithfulness Gap" (BPF) (**A-pre**, small team, single version). Drift is detected by probing forward and backward consequences in Lean. On DriftBench (2,183 NL/Lean pairs with controlled drift labels) it detects 89.6% of drifted formalisations, against 41.2% for typecheck and **63.3% for an LLM-judge baseline**. Labels are synthetic. Treat with caution. [Faithfulness Gap](https://arxiv.org/pdf/2606.16541)

### Inferences
- *Inference*: the evidence above rules out a gate in which the same lineage judges its own spec. It also only weakly supports a gate that is a single cross-model LLM judge. The best-supported LLM pattern is: cross-family judges must *agree* in order to accept; disagreement or rejection goes to a human; the gate is calibrated on a human-labelled sample; and it is recalibrated when the generating models change (Beyond Compilation's judge-aging effect).
- *Inference*: the strongest gains come from *external, executable or independently derived* checks: Reid's second spec, JEST's N+1 engines, executable tests in Kamoi's "reliable external feedback", CriticGPT's planted-bug training. For brief T3, this supports expectation tests derived from the prose by a different derivation path and, ideally, a different model family, with no view of the spec. It also supports a refuter that is scored on planted spec mutants (T4).
- *Inference*: in Kim et al., stronger models have *more* correlated errors. Upgrading every agent to the frontier model may therefore *reduce* the independence between the spec writer and the expectation-test writer.

### Gaps
- No study measures common-mode error when the *same* LLM writes both a spec and the tests for it from the same prose, compared with different LLMs or different derivation paths. Clover (brief §3) is the closest.
- No measured LLM refuter or adversary for prose-to-spec faithfulness, for example an agent that mutates a clause and then checks whether the expectation tests kill the mutant, was found.
- Knight & Leveson, Eckhardt–Lee and Littlewood–Miller: full texts **[unreachable]**; figures not re-checked.
- All LLM faithfulness-judge evidence is from maths (Lean). None was found for API/behaviour specs.

---

## Q2. Disconfirming search (a): do formal or structured intermediates fail to improve faithfulness to NL intent over careful prose review?

### Takeaway
No full-text study was found that holds intent fixed and shows a formal or structured intermediate leading to *worse or equal* faithfulness than careful prose review. The disconfirming evidence that does exist is indirect. Humans, experts included, misread and miswrite formal notations, and English to formula is the worst direction. Pattern or structured notations beat raw LTL. Formal artefacts are no better understood than code.

The new LLM-era evidence cuts both ways. Compilation and well-formedness gates *overstate* faithfulness by up to about 30 points, so formality without a semantic check gives false confidence. Structured NL as a mediator is reported to help LLMs, but that report is anecdotal and cites a code-translation paper. Net: brief §3 ("notation alone does not beat prose") is **not challenged**. It is reinforced: notation helps only together with a check against intent.

### Cited Findings
- Greenman, Saarinen, Nelson, Krishnamurthi 2023, "Little Tricky Logic" (‹Programming› 7(2), **A**, full text). Four rounds: Round 1 with 90 enrolled students (Quizius), later rounds with students and a Round 3 group of 29 researchers (22 in formal methods/verification). LTL→English, English→LTL and trace-satisfaction questions. Misconceptions recur in experts as well as learners. **English→LTL was the most common source of errors**. "Correct" means semantic equivalence to the reference formula, checked mechanically. Agents: none (human-only evidence). Relevance: a formal intermediate brings its own misreading risk exactly at the authoring step. [Greenman et al.](https://arxiv.org/pdf/2211.01677)
- Czepa, Amiri, Ntentos, Zdun 2019 (Softw. Syst. Model., **A**, full text). Controlled experiment, n=215 students, modelling compliance specs from NL in LTL, EPL or PSP. Semantic correctness: PSP (pattern-based, structured) > EPL > LTL. Advanced users did equally well with PSP and EPL. Raw temporal logic is the worst authoring medium. No prose-only arm. Human-only evidence. [Czepa et al.](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6944266/fullTextXML)
- Snook & Harrison 2004 (IST, Z vs Java comprehensibility): **[unreachable]** (ScienceDirect abstract only). Per the abstract, little difference in comprehensibility between a Z spec and its Java implementation. [abstract](https://www.sciencedirect.com/science/article/abs/pii/S0950584904000710)
- Finney 1996 (IEEE TSE correspondence): **[unreachable]**. Per the abstract, students already trained in discrete maths and Z "performed very poorly" at reading specs. Its n is not available. [record](https://gala.gre.ac.uk/id/eprint/25)
- Zimmerman et al. (RSML readability), Sharpe/Knight comparisons: not found in full text; leads only.
- **LLM era, against "formal = faithful":** Beyond Compilation (above, **A-pre**). Lean compilation overstates faithfulness by 1.3 to 29.5 points across 8 systems, and nearly half of the compile gain from tool feedback is semantically unfaithful. [Beyond Compilation](https://arxiv.org/pdf/2606.31002)
- **LLM era, for structured intermediates:** Mavridou, Farrell, Vázquez et al. 2025 (NASA/Manchester/York, **A-pre**). Their FRET extension says translating ambiguous NL into FRETish before temporal logic "significantly improved output accuracy compared to direct, one-step translation" in "one of our projects". No n or data is given, so this is **C-level** inside an A-pre paper. They support it with a reference reporting 18–43% gains from structured intermediates, but the reference list shows that paper is about *LLM code translation* via intermediate languages, not requirements. Flag: weak support. In the same paper, the authors' own oracle-based validation (random DTMCs plus an independent semantic oracle) caught an `optional` vs `weak` modifier error in their own generated formulas that "could be easily missed during manual inspection". This is evidence that experts' manual review of formal output misses errors, and that an executable, independent oracle catches them. [Mavridou et al.](https://arxiv.org/pdf/2512.15788)
- Broccia et al. 2026 (above): prose-only inspection with LLM help was *worse* than without. This is a caution against assuming that "careful prose review" stays careful once agents assist. [Broccia et al.](https://arxiv.org/pdf/2608.21298)

### Inferences
- *Inference*: across these studies, a formal intermediate catches a class of errors (type, scope, internal consistency) and introduces another (the author misreads operators). It improves faithfulness only when paired with a check that turns it back into something judgeable against the intent. That check could be scenarios, traces, an independent oracle, or a second derivation. This is consistent with the T1 "validation by exhibition" direction.
- *Inference*: structured *intermediate* NL (patterns, FRETish, EARS-like templates) has better human evidence than raw logic (Czepa). This favours keeping the brief's case tables and typed non-commitment as an intermediate layer before Dafny or TLA+.

### Gaps
- No study found that compares, with intent fixed, (i) careful prose review against (ii) formalise-then-check for *detecting faithfulness defects*, for either humans or LLMs.
- No controlled EARS/Gherkin vs free-text faithfulness experiment with full text was found. Search leads (INCOSE 2024 automotive case: LLMs dropped conditions to fit EARS; Gherkin generation studies) were not fetched.

---

## Q3. Disconfirming search (c): published pipelines doing prose → spec → model → reference model with faithfulness gates

### Takeaway
**No published pipeline does the brief's full chain** (prose decisions → normative spec → formal models → executable reference model, with gates checking faithfulness *to the prose*). The closest pipelines are language and ISA standards: Arm ASL, WebAssembly SpecTec and ECMAScript ESMeta/JEST.

They reverse or collapse the chain. Each makes one formal source executable, generates or extracts the other layers mechanically, and checks faithfulness to intent through (a) **human-written conformance suites** that are independent of the spec, (b) **N-version comparison** against independent implementations, and (c) in Arm's case, an **independent high-level property set** written from the NL manual. Prose is a *generated* or parallel artefact, never the source that formal layers are checked against.

Cedar (AWS) and FRET have model ↔ implementation or NL-template ↔ logic gates, but no gate against the source prose. Spec Kit has only LLM self-review checklists. Agents are measured in none of the closely fitting pipelines.

### Cited Findings

**WebAssembly SpecTec** (PLDI 2024, **A**, full text) [Youn et al.](https://people.mpi-sws.org/~rossberg/papers/Youn,%20Shin,%20Lee,%20Ryu,%20Breitner,%20Gardner,%20Lindley,%20Pretnar,%20Xiaojia,%20Watt,%20Rossberg%20-%20Bringing%20the%20WebAssembly%20Standard%20up%20to%20Speed%20with%20SpecTec.pdf)
- Before SpecTec, each Wasm feature needed four artefacts kept in sync by hand: formal rules (LaTeX), prose pseudocode, the reference interpreter and a test suite. The paper calls this "laborious and error-prone".
- SpecTec is a single DSL source. It is type-checked (meta-level). It generates the LaTeX formal spec, the **prose pseudocode** (via an intermediate algorithmic language, AL, designed to mirror the prose) and a meta-level interpreter. Test-generation and theorem-prover backends were planned at the time.
- Gates: (1) DSL type checking; (2) prose generated rather than written, removing transliteration errors; (3) the generated interpreter runs the **official, human-written test suite**, passing 100% of applicable Wasm 2.0 tests and all 1,331 tests per proposal after fixes.
- Retrospective over 2 years of spec-fix commits: all in-scope bugs would have been prevented. That is 3 type errors, 7 prose errors (free identifiers, missing or obsolete steps), 3 semantic errors caught by running tests, plus editorial fixes. On 5 Wasm 3.0 proposals (44 instructions) it found **10 bugs** (2 type, 2 prose, 4 semantic, 2 editorial), all confirmed by the authors. Prose generation worked for 42 of 44 instructions.
- Faithfulness to *intent*: checked only through the independent test suite and human review. Informative prose and notes are still written by hand. Agents: none.
- *Inference*: SpecTec reverses the brief's direction: formal is the source and prose is derived. It removes formal-vs-prose drift, but it cannot detect a *formal* misreading of the designers' intent except through the test suite.

**ECMAScript: JISET/JEST/ESMeta (KAIST)** (**A**) [JEST](https://arxiv.org/pdf/2102.07498)
- The executable semantics is *extracted* from the spec's prose algorithms (JISET). JEST synthesises conformance programs from that semantics, injects assertions, runs them on N engines, and uses voting plus SBFL to blame either an engine or the spec. Results: 27 spec bugs and 44 engine bugs in ES11.
- The faithfulness gate is between the spec text and *community intent as embodied in independent engines* (N-version), not a gate against an upstream design record. Agents: none. The later ESMeta papers were not fetched separately.

**Arm ASL** (FMCAD 2016 and OOPSLA 2017, **A**) [Reid 2016](https://alastairreid.github.io/papers/fmcad2016-trustworthy.pdf); [Reid 2017](https://alastairreid.github.io/papers/oopsla2017-whoguardstheguards.pdf)
- Pipeline: Arm's pseudocode plus English manual → executable ASL spec → tested against Arm's internal Architecture Validation Suite (over 11,000 test programs for AArch64), random instruction tests and trace comparison with processors.
- Results: 100% pass on v8-A and v8-M ISA tests and on v8-M system tests. Some v8-A system tests still failed.
- Where the English text, the tests and the simulator disagreed, all three were fixed "to match the architects' intent", so humans arbitrate.
- 2017 addition: a separate high-level property set, derived from NL rules and architect discussion and deliberately structured differently, is formally verified against the ASL spec. It found 12 bugs.
- *Inference*: this is the published pipeline closest to the brief's need. A spec is checked against an independently authored formal reading of the NL intent, which architects can review because it is short. It still has no per-clause trace to source prose and no agents.

**AWS Cedar** (**A-pre**, extended version of a peer-reviewed OOPSLA 2024 paper) [Cedar](https://arxiv.org/pdf/2403.04651)
- Pipeline: design → Lean model with proofs → Rust implementation, kept in step by differential random testing in CI. This testing found "nearly two dozen bugs since the project's inception". Writing the formal spec "forced us to think deeply about corner cases" and revealed further semantic bugs.
- No gate against a prose source; documentation is downstream. Grade for the practice data: B. Agents: none.

**NASA FRET** (FRETish → pmLTL → Lustre/CoCoSim/Kind 2) [Mavridou et al.](https://arxiv.org/pdf/2512.15788); [NTRS 20200002241](https://ntrs.nasa.gov/citations/20200002241) **[unreachable]**: PDF download failed.
- Gates per search leads, not re-checked in full text: generated NL and diagram explanations of each FRETish requirement; interactive simulation of formulas; realizability analysis (JKind/Kind 2).
- Gate per full text: an oracle-based automated validation framework checking FRET's NL-template → formula translation against an independent semantic oracle on random models.
- Faithfulness of the user's free prose → FRETish is left to the human, with explanations and simulation as aids. Human-only evidence. The LLM-mediator claim is anecdotal (see Q2).

**GitHub Spec Kit / spec-driven development** (**D/B**: official docs, no data) [spec-driven.md](https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md)
- Pipeline: idea → PRD/spec → plan → tasks → code, all by agents.
- Gates: `[NEEDS CLARIFICATION]` markers; checklists that "force the LLM to self-review"; "constitutional" phase gates (simplicity, anti-abstraction); test-first ordering; "AI analyzes specifications for ambiguity, contradictions, and gaps".
- All gates are same-lineage LLM self-review. That is the configuration Q1's evidence (Huang, Kamoi, Panickssery, Kim) says is weakest. No independent derivation and no formal model. No measured results.
- Kiro: not fetched. Treat as the same class (C/D).

### Inferences
- *Inference*: comparison point for the report. The Arm 2017 plus SpecTec/JEST pattern is "one executable formal source + mechanically derived layers + an *independently authored* check set (conformance suite, N engines, or a high-level property set written to differ in structure)". It is the published precedent for the brief's split between spec-enforcing tests and expectation tests. These projects found real spec bugs: Wasm 10, ES11 27, Arm v8-M 12, Cedar about 24. They did so precisely where an independent artefact disagreed with the spec.
- *Inference*: none of these pipelines starts from *decision records*, so the brief's "faithful to the prose records" gate has no published precedent. The nearest analogue is Arm's practice of turning NL rules into reviewable properties, choosing only rules that are not restatements of the formal spec.
- *Inference*: SpecTec's "generate prose from formal" suggests a cheap back-translation check for T1: generate prose from the spec or model and diff it against the records. Its own evidence covers only drift between prose and formal versions, not intent.

### Gaps
- Kiro, Galois/DARPA programs, Sail RISC-V (only via SpecTec related work: Sail generates SMT, prover definitions and LaTeX fragments), P4 and SQL pipelines: not fetched. No evidence that they gate against source prose.
- ESMeta's later papers (for example on test262 conformance and spec-type analysis) not fetched separately. JEST is the ESMeta-lineage evidence used.
- No pipeline found in which agents perform any step and faithfulness to the source prose is measured.
