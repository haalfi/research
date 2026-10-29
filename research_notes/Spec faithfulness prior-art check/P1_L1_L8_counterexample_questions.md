# P1: L1 (C-GRiD) and L8 (counterexample replay to agents)

Scope: brief leads L1 and L8, and C-GRiD's predecessors only as far as L1 depends on them. Downloads are in the scratchpad `p1/`. Nothing was fetched from any git branch.

## L1: C-GRiD, "Neuro-symbolic requirements elicitation utilizing formal verification counterexamples"

### Takeaway
The paper exists. It is a peer-reviewed ASE 2026 research-track paper, and the claimed 79.2 % and 70.8 % figures are correctly quoted. It does **not** measure turning counterexamples into questions for a human. No human took part. The "stakeholder" in both conditions is a script that reads the removed ground-truth constraint. In the archived code, that script ignores the generated question, and its constraint is inserted verbatim. The initial model is the correct ground-truth model with 1 to 3 constraints deleted, so the protocol presupposes a correct initial model. **No change** to any recommendation on this branch. At most it adds an unmeasured design precedent for the V §2.1 *Inference* on asking humans one concrete-case question.

### Existence and corrected citation
- Corrected citation: Okba Tibermacine (National School of Artificial Intelligence, ENSIA, Algeria) and Chouki Tibermacine (IRISA, Université Bretagne Sud, Vannes). "Neuro-symbolic Requirements Elicitation: Utilizing Formal Verification Counterexamples as Contextual Prompts". In *Proc. 41st IEEE/ACM ASE 2026*, Munich, pp. 613–623, DOI 10.1145/3832783.3834379, CC BY 4.0. Received 2026-03-26, accepted 2026-06-18. The tool name is C-GRiD (Counterexample-Guided Requirements Discovery). — [Crossref record](https://api.crossref.org/works/10.1145/3832783.3834379); [ASE 2026 research-track program](https://conf.researchr.org/track/ase-2026/ase-2026-research-track)
- The lead's title is truncated: it omits "as Contextual Prompts". The claimed "paper 49" URL was not checked. `conf.researchr.org/track/ase-2026/ase-2026-papers` returns 404, and a guessed `details/ase-2026-papers/49/…` URL also returned 404. The paper is listed in the research-track program as "Research Papers", 15-minute talk. — [program page](https://conf.researchr.org/track/ase-2026/ase-2026-research-track)
- Grade: **A** (ASE research track, published, with DOI).
- Full text read: **y**. Source: the author-deposited HAL copy hal-05794580, 12 pages including the HAL cover. The ACM PDF returned 403 (Cloudflare). — [HAL PDF](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- Replication package also read, partly: Zenodo 10.5281/zenodo.19222714, one version dated 2026-03-25. Code, results and README were inspected; the code was not run. — [Zenodo record](https://zenodo.org/api/records/19222714)

### What the paper claims to do
- Pipeline as described: an LLM produces an initial TLA+ model and properties (V0) from informal requirements; TLC runs depth-bounded (k = 15); a deterministic trace analyser classifies each violation as MissingGuard, RaceCondition, Deadlock or LogicError; a template turns it into a yes/no question for the stakeholder, with an LLM fallback for LogicError; the answer adds, relaxes or strengthens a constraint; then the loop repeats. — [HAL PDF §3.3–3.6, Alg. 1–3](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- Example question from the paper: "Should concurrent transfers be allowed if they might cause an overdraft?" Polarity of the answer decides the repair: "this behaviour is allowed" means relax Φ, and "disallowed" means add a constraint. C-GRiD "does not attempt to distinguish the two cases automatically". — [HAL PDF §1, §3.6](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- Mode 1 versus Mode 2: an LLM answers from a domain knowledge base when match confidence is above 0.85. "Approximately 40% of questions were answerable automatically". The paper does not say on what n. — [HAL PDF §3.5.2](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- The regression guard (§3.7) "is a design proposal… not part of the implementation used in Section 4". — [HAL PDF §3.7](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)

### What was measured (n, setting, "correct", baseline)
- **Setting.** 10 TLA+ specifications "from public literature" with 2–15 constraints each and 2–10 variables. Domains: banking, e-commerce, healthcare, concurrency, distributed, embedded, and one "Generic" spec named `SpecificationName`. — [HAL PDF Table 4](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **Protocol.** "Controlled constraint-removal": start from a complete verified spec and remove constraints by stratified random sampling at quota k ∈ {3, 5}. Only 1 to 3 constraints are actually removed per configuration, and that count is the recall denominator. This gives 20 configurations, each run once per oracle: 40 C-GRiD runs. — [HAL PDF §4.2.2, §4.3](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **"Constraint recovery recall"** = the fraction of *removed formal constraints* that reappear, by "strict semantic matching" of expressions. The paper states explicitly: "We do not measure the recovery of unstated informal stakeholder requirements, and we do not measure the correctness of the initial natural-language-to-TLA+ translation." — [HAL PDF §4, §4.2.4](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **Oracles.**
  - Perfect oracle: "A simulated stakeholder that consults S_GT (the ground-truth specification)".
  - Noisy oracle: 75 % correct, 15 % "ambiguous" (no constraint), 10 % a mutated constraint.
  - The authors call the noise model "deliberately simple… best read as a stress test of the loop's error-recovery mechanism rather than as a model of human behaviour". This contradicts the abstract's framing of it as assessing "robustness under realistic interaction settings".
  — [HAL PDF §4.2.3, abstract](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **Results.**

  | Approach | Recall | Precision | Convergence |
  |---|---|---|---|
  | C-GRiD, perfect oracle | 79.2 % | 90.0 % | 85 % |
  | C-GRiD, noisy oracle | 70.8 % | 80.0 % | 75 % |
  | Gen-Once (one-shot LLM) | 2.8 % | 8.3 % | — |
  | Auto-Repair (CEGIS templates) | 0.0 % | — | — |

  - The baselines ran only on a 6-spec subset (12 configurations). On that subset, C-GRiD scored 65.3 % against Gen-Once's 2.8 %: t(11) = 4.93, d_z = 1.42.
  — [HAL PDF Table 5, §4.3.1](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **How "convergence" breaks down.**
  - Perfect oracle, 20 runs: 2 verified, 13 "recall-saturated" (all removed constraints recovered, but no clean verification by N_max = 10), 2 vacuously terminated (0 % recall), 3 failed.
  - Noisy oracle: 2 / 11 / 2 / 5 in the same categories.
  - The authors: "C-GRiD reliably finds missing constraints, while reliably integrating them into a re-verified specification remains an open problem."
  - The archived metric code also counts any run with recall = 1.0 as converged ("CRITICAL FIX" in `evaluation/lobotomy.py`). That is consistent with the paper's RS category.
  — [HAL PDF Table 6, §4.3.1](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf); [Zenodo package](https://zenodo.org/api/records/19222714)
- **The noisy oracle changed little.** Recall dropped only in 5 of the 10 k = 5 configurations. All 10 k = 3 rows are identical across oracles. The two 0 % "vacuous" runs are included in both recall means. — [HAL PDF Table 6](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **Authors evaluate their own tool**: yes (TA). — [HAL PDF](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)

### What the replication package shows (code inspected, not run)
- The archived `results/revision_full/results.csv` reproduces the published means exactly: 20 runs per oracle, mean recall 79.2 % and 70.8 % (own recomputation). — [Zenodo package](https://zenodo.org/api/records/19222714)
- **The perfect oracle (`core/oracle.py`, `GroundTruthOracle`, used for the `cgrd` runs in `experiments/runner.py`) does not read the question.**
  - It picks the first not-yet-recovered removed constraint whose type matches the error pattern. If none matches, it takes any remaining removed constraint.
  - It returns that ground-truth `Constraint` object itself, with the comment "Return actual GT!".
  - The question text is used only to choose an option index.
  — [Zenodo package](https://zenodo.org/api/records/19222714)
- **The refiner inserts the oracle's constraint verbatim.** `core/spec_refiner.py` builds `constraints=spec.constraints + [new_constraint]` and inserts the expression into the TLA+ source. There is no LLM call in that path. — [Zenodo package](https://zenodo.org/api/records/19222714)
- **The runner passes no LLM to the C-GRiD runs.** It supplies `initial_spec=partial_spec`, the ground-truth spec minus the removed constraints. `core/question_gen.py` imports no LLM. A Groq/LLM generator (`core/llm_generator.py`) is used only by the Gen-Once baseline (`baselines/b1_llm.py`, `b1_strengthened.py`). — [Zenodo package](https://zenodo.org/api/records/19222714)
- **The noisy oracle reuses the perfect oracle.** `core/noisy_oracle.py` is the same oracle plus a random roll. The "ambiguous" outcome returns `TRUE`. The "incorrect" outcome returns a syntactic mutation (operator negation, boundary −1, or dropped conjunct) of the correct ground-truth constraint, and still marks that constraint as used. — [Zenodo package](https://zenodo.org/api/records/19222714)
- *Inference*: in the archived implementation, recall in effect counts how many TLC counterexamples occur before the removed constraints run out, because each counterexample makes the oracle hand back one removed constraint. The questions' wording, correctness and usefulness have no effect on the reported recall. The paper's description of LLM-driven V0 synthesis and LLM refinement (§3.3, §3.8, §4.2.3: llama-3.3-70b at temperature 0.3) is **not exercised** by the archived C-GRiD runs. Caveat: the package has one version, dated 2026-03-25, before acceptance. The camera-ready says the figures are "re-derivable from the archived run records", and they are. An unarchived LLM-based variant cannot be excluded, but no evidence of one was found.

### Agents (LLMs)
- Per the paper, an LLM (llama-3.3-70b-versatile) does V0 synthesis, refinement and fallback questions. — [HAL PDF §4.2.3](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- Per the archive, no LLM takes part in the reported C-GRiD runs (see above). An LLM appears only in the Gen-Once baseline, at 2.8 % recall. — [Zenodo package](https://zenodo.org/api/records/19222714)
- No measured result exists for LLM-generated questions or LLM refinement.

### Transfer
*Analogous* at best: TLA+ transition systems and depth-bounded TLC, not library or API behaviour specs. The *question-generation step* has no measured result to transfer.

### Brief §5(b)
- **Does recall survive a realistic stakeholder?** **Not tested.** Both oracles are simulated and read the ground truth. The authors list "the oracle assumption" as the main construct-validity threat and plan "controlled user studies" as future work. — [HAL PDF §5.2.1, §6](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **Does question generation depend on a correct initial model?** **Yes, in the evaluation.** V0 is the correct ground-truth model minus 1–3 constraints. The NL→TLA+ translation is excluded. The authors say: "our protocol begins from existing formal specifications rather than from informal documents, so it cannot measure how often each case arises in practice", and they call this "the most important gap in this evaluation". — [HAL PDF §4, §5.2.1](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **By design, discovery depends on the model's variables and depth.** "a missing requirement that refers to a domain variable not present in the current state space cannot produce a counterexample and will never be surfaced". Violations deeper than k are never shown. A reduced spec that already satisfies Φ yields no question at all: this happened in 2 of 20 runs, with 0 % recall. — [HAL PDF §3.4, §3.9, §4.3.3](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- **When the initial model is wrong.** The design answer is "symmetric resolution": the human's yes/no polarity decides between relaxing an over-constrained property and adding a constraint. There is one illustrative episode (BasicTransfer, balance ≥ 100 relaxed to ≥ 0) and no measurement. — [HAL PDF §3.6](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)

### Predecessors (resolved only as far as L1 depends on them)
- C-GRiD names LTLTalk (Gavran et al., OOPSLA 2020), SynthTL (Mendoza et al., FMCAD 2024) and ARTEMIS (Mendoza, Mavridou, Katis, Trippel, ICSE 2026, "low-complexity distinguishing traces for semantic validation") as "the closest antecedent". It also names SpecVerify (Wang, Farrell, Cordeiro, Zhao, arXiv 2507.04857 / RE 2025) as closest among the LLM+verifier works. — [HAL PDF §2.3, refs 10, 27, 28, 34](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- L1's results do not depend on any of these, so they were not read. *Inference*: ARTEMIS, which shows distinguishing traces to stakeholders to validate formulas, is the nearer match to brief §1 question 2, but it is outside the named leads.

### Delta
- **V §2.1, *Inference* paragraph, quoted verbatim**: "*Inference*: ask humans yes / no / "not addressed" questions on one concrete case tied to one record sentence. Route to them (a) unresolved difference witnesses, (b) every "not addressed" answer from the added-commitment probe, and (c) a random audit of agent-judged witnesses."
  - Verdict: **no change.** C-GRiD is a published *design* precedent: a counterexample trace becomes a yes/no question about one concrete case, and the answer's polarity decides relax-versus-add. That gives the paragraph an analogue for its form. It does not raise its evidence level, because the question step was never measured. It stays *Inference*.
- **DD §4 new open question 4 (G4a false-alarm rate) and §5 open question 4**: no change. C-GRiD reports no spurious-counterexample rate. Its "vacuous" and "recall-saturated" categories are a different phenomenon.
- **V §2.6(c) (no published end-to-end pipeline with faithfulness gates against the prose)**: no change. C-GRiD excludes NL→formal faithfulness from its evaluation by construction.

## L8: "Counterexample replay to agents" (claim: feeding the concrete counterexample, not an error message, improves repair)

### Takeaway
The slides exist. They are Lucas Cordeiro's invited FATTW 2026 talk "Formal Verification of LLM-Generated Code". **Neither the slides nor the two underlying papers read contain an ablation of concrete counterexample versus error message.** The nearest measurement is ESBMC-AI (AST 2025). It compares verifier output (property violation, line, stack trace and counterexample, bundled together) with **no verifier output at all**: about 31–37 % versus 80–90 % "accuracy" on C vulnerability repair. The two are not separated, and the n for the unassisted condition is not stated in the passage read. The lead's claim as worded is **not supported**. **No change.**

### Existence and corrected citation
- **The slides.** L. C. Cordeiro, "Formal Verification of LLM-Generated Code", invited talk at FATTW 2026, co-located with ASE 2026, Munich, 15–16 Oct 2026. 30 slides, linked from his ssvlab homepage. FATTW is described there as "the invitation-only workshop on the new foundations of software testing". — [slides PDF](https://ssvlab.github.io/lucasccordeiro/talks/fattw2026_slides.pdf); [homepage entry](https://ssvlab.github.io/lucasccordeiro/)
  - Grade: **C** (talk slides that summarise the group's own work).
  - Full text: **y** (all 30 slides).
- **What the slides say about counterexamples.**
  - Slide 12: "Violation → a concrete input, replayed as a regression test".
  - Slide 19 (SpecVerify): "Replay the counterexample against the real system… fed back, not believed… any failing property is fed back".
  - Slide 24: "The counterexample was the bug report".
  - Slide 27, lesson 2: "Maintainers fix what arrives with a concrete input — 18 fixes merged upstream across five codebases."
  - No slide compares counterexample feedback against error-message feedback, and none reports an ablation. The "18 fixes" are counts with no comparison condition, and the fixes were made by human maintainers, not agents.
  — [slides PDF](https://ssvlab.github.io/lucasccordeiro/talks/fattw2026_slides.pdf)

### Underlying paper 1: ESBMC-AI
- **Citation.** N. Tihanyi, Y. Charalambous, R. Jain, M. A. Ferrag, L. C. Cordeiro. "A New Era in Software Security: Towards Self-Healing Software via Large Language Models and Formal Verification". *2025 IEEE/ACM AST*, DOI 10.1109/AST66626.2025.00020. — [Crossref](https://api.crossref.org/works?query.title=Towards+Self-Healing+Software+via+Large+Language+Models+and+Formal+Verification&rows=3); [author PDF on ssvlab](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf)
  - Grade: **A**.
  - Full text: **y** (6 pages, extracted from a two-column layout; method, dataset, results and §VI-B read).
- **Setting.**
  - ESBMC finds a violation in a FormAI C program. The source plus "the identified vulnerability, including its stack trace and counterexample that specifies the line number and error type" go to an LLM (GPT-4o in the experiment). The patch is re-verified.
  - The paper says 50,000 programs were randomly sampled from FormAI. Patch correctness was checked manually on subsets: for example 133 division-by-zero samples (86.47 %), 241 programs (91.29 %), and a reported 90.40 % for another category.
  — [author PDF](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf)
- **The comparison, quoted.** "Without the exact counterexamples and stack traces, LLMs can fix the issues with approximately 31 − 37% accuracy, compared to 80% to 90% accuracy with ESBMC output." The paper also says, without data: "Utilizing a general prompt such as 'fix the code based on this counterexample' will significantly reduce accuracy". — [author PDF §VI-B, §III](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf)
- **What it is not.**
  - The contrast is with-verifier-output versus without it. "Error message only" (property, line) is not separated from "concrete counterexample values". In ESBMC's output the two arrive together.
  - No n, protocol or model is given for the 31–37 % condition in the passage read.
  - Authors evaluate their own tool: yes (TA).
  — [author PDF](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf)

### Underlying paper 2: SpecVerify, the slides' Pattern C
- **Citation.** W. Wang, M. Farrell, L. C. Cordeiro, L. Zhao. "Supporting Software Formal Verification with Large Language Models: An Experimental Study". *IEEE RE 2025*, pp. 423–431, DOI 10.1109/RE63999.2025.00049; arXiv 2507.04857. — [Crossref](https://api.crossref.org/works/10.1109/RE63999.2025.00049); [arXiv PDF](https://arxiv.org/pdf/2507.04857)
  - Grade: **A**.
  - Full text: **partial** (8 pages; method and evaluation sections read for counterexample use).
- **How counterexamples are used.** "we generated test cases based on the counterexamples. We executed the program with additional print statements to directly observe the runtime behavior". This is counterexample replay by the authors, to adjudicate disagreements with CoCoSim/SLDV. It is not feedback to an agent, and there is no feedback-format ablation. — [arXiv PDF §IV-C, §IV-E](https://arxiv.org/pdf/2507.04857)
- **Headline per the slides** (which match the paper's framing): 46 of 58 Lockheed Martin requirements matched expert-written properties (79.31 %); verification rate 46.5 % (27/58), equal to CoCoSim; 0 false positives with Claude 3.5 Sonnet against 8 with GPT-4o. — [slides 19–21](https://ssvlab.github.io/lucasccordeiro/talks/fattw2026_slides.pdf)
- SpecVerify is relevant to brief §1 question 2 (property-from-prose versus expert properties) but is not a named lead. Its "correct" means agreement with expert-written properties, not faithfulness against intent.

### Agents
- ESBMC-AI: an LLM (GPT-4o) writes the patches, and ESBMC re-verifies them. — [author PDF](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf)
- SpecVerify: an LLM (Claude 3.5 Sonnet, GPT-4o) writes the assertions. — [arXiv PDF](https://arxiv.org/pdf/2507.04857)
- Neither isolates the effect of counterexample format.

### Transfer
- ESBMC-AI is *analogous* at most: C memory and arithmetic safety repair, not spec or behaviour faithfulness.
- The claim "concrete counterexample beats error message" is *inference* only; no source read measures it.

### Delta
- No recommendation on this branch rests on counterexample-versus-message feedback to agents. The nearest is the V §3 check map, "Formula over one instant" row, verbatim: "added-commitment probe via failing Dafny assertion or Hypothesis-shrunk case shown with the source sentence (Cunha & Macedo; Lahiri)". L8 neither confirms nor overturns showing a concrete case. **No change.**

## Answers bearing on brief §1 questions

### Takeaway
On §1 question 1, about a measured method that turns verifier counterexamples into questions for the decision-maker: **none found among L1 and L8.** C-GRiD is the published method that does exactly this by design, but its evaluation does not measure the question step. In the archived code the questions do not affect the score, and no human or realistic stakeholder took part. That gap, listed in the record-quality report as unmeasured, stays unmeasured.

### Cited Findings
- C-GRiD turns TLC counterexamples into template yes/no questions, with one concrete case per question. This is design only. — [HAL PDF §3.5.4, Table 3](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- The evaluation answers from the ground truth, and the archived oracle returns the removed constraint regardless of the question. — [Zenodo package](https://zenodo.org/api/records/19222714)
- The authors themselves defer "controlled user studies with software engineers and domain experts". — [HAL PDF §6](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)
- L8's sources concern agent repair of C code from verifier output (ESBMC-AI), or the authors replaying counterexamples to adjudicate verdicts (SpecVerify). Neither involves questions to a decision-maker. — [AST 2025 PDF](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf); [SpecVerify arXiv](https://arxiv.org/pdf/2507.04857)
- On "finding questions no checklist raises": C-GRiD's questions come from four fixed error-pattern templates (MissingGuard, RaceCondition, Deadlock, LogicError fallback). They can only concern variables already in the model. — [HAL PDF §3.5.3, §3.9](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)

### Inferences
- *Inference*: a constraint-removal protocol with a ground-truth oracle cannot, by construction, measure whether a question would lead a real decision-maker to state the missing rule. A settling measurement would need humans who hold the latent intent, scored on the constraints they state. One option is the record-quality report's unmeasured "questions no checklist raises", with blind decision-makers and seeded gaps in records.
- *Inference*: C-GRiD's polarity design treats "this behaviour is allowed" versus "disallowed" as relax versus add. That design is close to this branch's typed non-commitment idea, but it has no "not addressed" or "deliberately not promised" answer. The V §2.1 question format, with its "not addressed" option, is richer than C-GRiD's.
- *Inference*: questions over G4a counterexamples would have to be checked for model reachability (G4c) before going to a human. The DD §4 G4a false-alarm question already covers this, and C-GRiD adds nothing.

### Gaps
- No human-stakeholder evaluation of counterexample-derived questions was found in L1 or L8.
- Questions §1.2 and §1.3 are not touched by L1 or L8, except that SpecVerify's agreement-with-expert-properties result is out of scope here.

## Verification debt
- The C-GRiD replication code was inspected statically, not run, because TLC and Groq are unavailable. The observation that the oracle does not use the question is a code reading. It should be confirmed by running, or by asking the authors, before it is stated as fact in a report. A camera-ready implementation that differs from the archive cannot be excluded, though the published numbers match the archive exactly.
- C-GRiD's "strict semantic matching" for recall and precision: in the archive it is `MetricsCalculator.semantic_match` in `evaluation/lobotomy.py`. Its body was not read.
- ESBMC-AI: the n, model and protocol behind "31–37 % without counterexamples" were not located in the extracted text, because the two-column extraction may have lost a table or paragraph. Treat the figure as the authors' summary claim. [Partial on this point.]
- SpecVerify was read only partially. Not needed for L8's verdict.
- The ASE "paper 49" detail URL was not resolved. Existence is confirmed via the program listing, Crossref and HAL.
- The FATTW 2026 workshop page (conf.researchr.org/home/fattw-2026) was not fetched. The talk's existence rests on the slides and the homepage news item.

## Self-check
- "Constraint recovery recall" could be misread as recovery of stakeholder intent. The paper rules this out explicitly, and these notes keep to its definition.
- The lead's "noisy simulated stakeholder" figures are quoted correctly. The paper's abstract calls the noise setting "realistic interaction settings", while its body calls it a stress test, not a model of human behaviour. The report should use the body's wording.
- I may have over-read the code. `PerfectOracle` (the "next GT in order" class) exists but is not the one the runner instantiates. The runner uses `GroundTruthOracle`, which also returns the GT object and ignores question wording beyond option scoring. Either way, the question text does not change which constraint is added.
- L8's lead wording ("not an error message") may paraphrase the slides loosely. No slide states that contrast. The closest is ESBMC-AI's with-versus-without verifier output, which I report as a different comparison rather than as support.
- No branch other than the current one was read. The record-quality report was not consulted, per `pcommon.txt`.
