# D5 Independence of the expectation family (minimal)

Scope: measured evidence on mechanisms that keep expectation tests independent of the spec and the reference model R: context isolation and read scopes, a lint that no expected value is computed by R, and detectors for added commitments in LLM-written tests. No organisation design. The track builds on the verified edition's §2.3.3 and §2.5. It does not re-survey Zhao et al. (ISSTA 2026), Konstantinou et al. 2024 (arXiv 2410.21136), Mathews & Nagappan, Canedo, DSpec2Test, Sami et al., NonDex, Huo & Clause, Knight, or Eckhardt & Lee.

Per-finding qualification key used below: **G** = grade; **FT** = full text read; **n/setting**; **"correct"** = what correctness meant; **T** = transfer label (*direct* = library/API behaviour specs, *analogous* = other spec domains, *inference*); **Agents** = whether LLMs/agents were measured on this step; **Indep.** = source-independence flag (TA = tool or method authors evaluating their own tool, CB = competing benchmark, V = vendor, — = none noted). Venues were checked through Crossref or Semantic Scholar, as stated per item. Downloads are in the scratchpad `d5/` folder; own-trial scripts are in `d5_scripts/`.

---

## Q1. Context isolation and read scopes: measured effects of hiding code, spec or prior context from test-generating agents

### Takeaway
Three new full-text studies add to Zhao, Konstantinou 2024 and Mathews & Nagappan. All three point the same way. Giving the test writer the implementation, or the conversation that produced it, lowers fault detection when the implementation is wrong. A test writer given the description alone does about as well as one given correct code. The strongest new result is Konstantinou, Tambon & Papadakis 2026 (A-pre). On HumanEval+, MBPP+ and BigCodeBench, running test generation in a fresh context (task description only, no conversation history from code generation) detected 11.7 % more faults on average than generating tests in the same agentic conversation, across 5 models, all statistically significant. Even isolated, the tests detected only about 25 % of the retained hard faults. Isolation helps but does not suffice. No study measures isolation from a *spec or formal model*, as opposed to from code. No study measures OS-level read-scope enforcement for test-writing agents.

### Cited Findings

**F1.1 Fresh-context ("test-driven") vs same-conversation ("agentic") test generation.** Konstantinou, Tambon, Papadakis, "On the risk of coding before testing", arXiv 2607.05139 (2026). G: A-pre (Semantic Scholar lists arXiv only). FT: yes. n/setting: three benchmarks (HumanEval+, MBPP+, BigCodeBench, 1,140 tasks in the last). The dataset holds one LLM-generated faulty implementation per task: the "hardest" one, failing the fewest reference tests, kept only if under 50 % of reference tests fail. The exact count of retained tasks was not found in the text. Five models: Claude Haiku 4.5, DeepSeek V4, GPT-4.1-mini, GPT-5-mini, Llama 3.3 70B. "Correct" = generated suite fails on the faulty implementation (fault detection against benchmark reference behaviour). Results:
- Description + implementation reduced fault detection by 13.2 % on average vs description only; implementation only reduced it by 15.1 %.
- "Generating tests independently" detected 25 % of faults vs 14 % for "generating tests after faulty code" (abstract).
- Fresh-context "Test-Driven Workflow" vs same-conversation "Agentic Workflow": +10.6 %, +13.8 %, +17.7 %, +13.6 %, +7.9 % per model, mean +11.7 %, p ≤ 0.0019 for every model (Table IV).
- Summarisation-first, CoT and CoVe prompting did *not* remove the bias. Prompt-only beat summarisation by 15.5 % and CoT/CoVe by 13.4 %.
- Differences were not explained by test count, statement coverage (≈95–99 % everywhere) or fault triggering. The authors attribute them to assertion quality (inference by the authors).
- The fresh-context definition, verbatim: "test generation is performed in a fresh interaction with the LLM that contains only the task description and no conversational context from the preceding code generation process."

T: analogous (Python function-level tasks, stateless). Agents: measured (a simulated agentic workflow; a plain LLM loop, no tool-using agent). Indep.: — (an empirical study, not a tool; the first author also wrote Konstantinou et al. 2024, which the earlier reports already cite) — [arXiv 2607.05139](https://arxiv.org/abs/2607.05139)

**F1.2 Correct vs incorrect code vs description only.** Huang, Zhang, Harman, Du, Cui, "Measuring the Influence of Incorrect Code on Test Generation", **ICSE 2026** (Crossref DOI 10.1145/3744916.3764532). G: A. FT: yes. n/setting: 11 LLMs (5 open, 6 closed) on HumanEval, MBPP and APPS, plus 41 repo-level examples from BugsInPy and SWE-bench. Five prompts: task only (P_T), task + correct code (P_T_CC), task + incorrect code (P_T_IC), correct code only (P_CC), incorrect code only (P_IC). "Correct test" = passes the canonical solution. Bug detection is measured on a constructed bug set. Results:
- Overall test-level accuracy on HumanEval: P_T 78.3 %, P_T_CC 80.4 %, P_T_IC 57.1 %, P_CC 64.1 %, P_IC 57.2 %. MBPP: 71.9 / 75.4 / 46.3 / 67.5 / 46.1. APPS: 67.1 / 66.0 / 37.9 / 55.3 / 37.6 (Table 3).
- Bug detection: P_T_CC 47.4 % vs P_T_IC 38.1 % vs P_CC 35.5 % (constructed bugs).
- On real-world code, tests generated for incorrect code had a "47% worse bug detection rate" (abstract).
- For GPT-4 on HumanEval, 94.8–99.3 % of incorrect tests have wrong *oracles*, not wrong inputs, except under P_IC (51.4 % oracle) (Table 10).
- The authors: "if the correctness of the source code cannot be guaranteed, providing only the task description can still lead to better results than providing incorrect code."

T: analogous (mostly function-level; a small repo-level part). Agents: LLMs measured; no agent loop. Indep.: — . Note: the same group's AgentCoder (F1.3) promotes code-blind test design, so the authors have a stake in the conclusion; I flag this as a mild interest, not TA — [arXiv 2409.09464](https://arxiv.org/abs/2409.09464)

**F1.3 Separate test-designer agent vs single agent (AgentCoder ablation).** Huang et al., AgentCoder, arXiv 2312.13010 v3 (2024). G: A-pre (no venue found in Semantic Scholar). FT: yes. n/setting: HumanEval and MBPP, GPT-3.5-turbo. "Correct test" = passes the canonical solution. Results:
- Single agent writing code then tests "within the same conversation": test accuracy 61.0 % (HumanEval) and 51.8 % (MBPP). Separate test-designer agent that does not see the code: 87.8 % and 89.9 % (Table 6).
- Line coverage 72.5/75.9 % vs 87.5/89.5 % (Table 8).
- The authors give two possible reasons ("distract the agent's focus" or tests "biased by the code") and do not separate them.
- Confound: the multi-agent arm also uses AgentCoder's dedicated test-designer prompt (RQ4 credits "the prompt engineering strategies we designed").

T: analogous. Agents: measured (multi-agent). Indep.: **TA** (authors evaluating their own framework) — [arXiv 2312.13010](https://arxiv.org/abs/2312.13010)

**F1.4 Requirements-only oracle generation (pilot).** Ma & Eisty, arXiv 2607.10277 (2026). G: A-pre. FT: yes. n/setting: 10 Defects4J Lang bugs and 5 LLMs. The LLM receives an NL business requirement plus a method signature, with no code. "Correct" = agreement with a hand-built requirement oracle (REQ) or with the SUT, measured on a constructed test suite. Results:
- Macro-F1 vs REQ: 0.56–0.82; vs SUT: 0.54–0.75.
- REQ-target scores exceed SUT-target scores for every model except Gemma-3n.
- Requirement ambiguity and technicality, rated by an LLM, did not correlate with accuracy (all 95 % CIs include 0).
- The authors call it "a pilot proof of concept".
- The requirements were written by researchers *from the fix diff*. The survey F1.6 notes that this makes the generation code-blind but the dataset construction code-derived.

T: *direct-adjacent* (a Java library, Apache Commons Lang, but only 10 cases). Agents: LLMs measured. Indep.: — — [arXiv 2607.10277](https://arxiv.org/abs/2607.10277)

**F1.5 Clustered LLM errors in LLM-derived verifiers.** Ma et al. (SAGA), "Rethinking Verification for LLM Code Generation", arXiv 2507.06920 (Semantic Scholar: NeurIPS 2025, not further verified). G: A (venue per S2). FT: **partial** (introduction and motivation only). Results:
- Verifiers "synthesized primarily from LLM-generated data exhibit a high failure rate when testing human-written bugs". A PCA of error patterns "reveals that LLM errors cluster tightly … while human errors are widely distributed".
- LLM solutions that passed LiveCodeBench's private tests were then flagged as wrong by LeetCode's judge for 20 % (medium) and 40 % (hard) of problems.

T: analogous (competitive programming). Agents: LLMs measured. Indep.: CB (a competing benchmark/verifier) — [arXiv 2507.06920](https://arxiv.org/abs/2507.06920)

**F1.6 Survey framing (not a measurement).** Liang et al., "LLM-Based Test Generation: Information Sources, Generation Strategies, and Quality Evidence", arXiv 2610.05001 (2026). G: A-pre (a structured narrative survey of 95 records; the authors say the coding was not independently validated). FT: yes (relevant sections). It separates the roles of code access: "Source code helps resolve imports and construct objects; the same code can also supply expected outputs … These roles should be recorded separately because context relevance and oracle independence answer different questions". It states that "A docstring generated from buggy code remains implementation-derived, even if the next generator receives only that docstring". It also proposes RejectLegal(T) and DetectFault(T) over pools of permitted (P⁺) and faulty (P⁻) implementations, explicitly "an evaluation recommendation rather than measurements extracted from the reviewed studies". *Inference*: across 95 records the survey found no study reporting both metrics together. T: inference. Indep.: — — [arXiv 2610.05001](https://arxiv.org/abs/2610.05001)

**F1.7 Leakage between agents (general multi-agent systems, not coding).** AgentLeak, arXiv 2602.11510 (header: accepted, IEEE Access 2026). G: B for this track (privacy leakage, not test oracles). FT: not read beyond header and search extract, so treat as a lead. Per the search extract: inter-agent messages leaked in 68.8 % vs final output 27.2 % (n = 4,979 traces), and MetaGPT role messages are visible to all agents without restriction. T: inference only (privacy, not oracle independence). [lead only; extract not verified against full text] — [arXiv 2602.11510](https://arxiv.org/abs/2602.11510)

**F1.8 Read-scope enforcement measured in agent benchmarks (adjacent: reward hacking).** EvilGenie, Gabor, Lynch, Rosenfeld, arXiv 2511.21654 v2 (2026). G: A-pre. FT: yes (method and the ambiguity sections). n/setting: 154 LiveCodeBench problems; test files are deliberately readable and editable. Results:
- Detectors: 30 % holdout tests (≤ 10), test-file edit detection, and LLM judges, each checked against human review. The authors found "the LLM judge to be highly effective at detecting reward hacking in unambiguous cases" and "only minimal improvement from the use of held out test cases".
- Explicit reward hacking by Codex and Claude Code; only Gemini 2.5 Pro edited or deleted test files.

The study measures *detection* when read and write access is *open*. It does not compare against a closed read scope. T: inference for D5 (agents attacking tests, not test writers copying the oracle). Agents: measured (three commercial agents plus Inspect's basic agent). Indep.: — — [arXiv 2511.21654](https://arxiv.org/abs/2511.21654)

**F1.9 Own trial: import guard vs read scope** (grade: own trial; scripts in the scratchpad `d5_scripts/guard_trial.py`). A `sys.meta_path` finder that blocks the module `refmodel` stopped `import refmodel`, `importlib.import_module('ref'+'model')` and `__import__('refmodel')`. It did **not** stop `exec(open('…/refmodel.py').read())`, which ran R's code inside the test process. n = 4 access patterns, a synthetic module. T: direct (Python mechanism). Agents: not measured.

### Inferences
- *Inference*: F1.1–F1.3 measure isolation from **code** (implementation or conversation history), not from a **spec or formal model**. That a test writer isolated from the spec catches spec misreadings remains unmeasured, as the verified edition already says. The direction of F1.1–F1.2 is consistent with that claim, but transfer from "code" to "spec" is inference.
- *Inference*: F1.1 isolates *conversation context* with the same model. This is the cheapest isolation level (a fresh session), and it already yields a significant gain. Read scopes (file-system level) are a stronger guarantee than a fresh prompt, but no measurement compares them.
- *Inference*: in F1.2, description-only (P_T) costs at most ~2 points of test accuracy against correct code and gains ~20 points against incorrect code. In the setting of this brief R is not known to be correct, so withholding R costs little and protects against R's errors. The bug-detection figures, by contrast, favour P_T_CC (47.4 %) over P_T. Access to *correct* code helps find bugs in other code, so isolation has a price when R happens to be right.
- *Inference*: F1.9 shows that a Python import guard is not a read scope. Enforcement must happen at the file-system or sandbox level: the expectation-test agent's container lacks the R, spec and model paths. Language-level guards only catch accidents.

### Gaps
- No study compares test generation with vs without access to a **spec or formal model** (as opposed to code). No study uses a stateful API.
- No measured study of OS- or sandbox-level read-scope enforcement (container mounts, path allow-lists) for test-writing agents. Found only reward-hacking detection with open access (F1.8). Searches: "multi-agent coding information leakage test agent", "sandbox read restriction", "hidden tests sandbox measured".
- The number of retained tasks in F1.1 was not found in the text.
- **Single-source flag**: the fresh-context vs same-conversation effect (+11.7 %) rests on F1.1 alone. AgentCoder (F1.3) is confounded and TA.

---

## Q2. Lint that no expected value is computed by R ("oracle anchoring"): smells, detectors and their measured precision/recall

### Takeaway
No published, evaluated detector targets "expected value computed by the SUT or a reference model". Canedo remains the only formalisation. Mature smell detectors (tsDetect, JNose, PyNose) implement only a *syntactic* "Redundant Assertion" rule (`assertEqual(X, X)`, `assertTrue(True)`). That rule would not flag `assert sut.put(1) == refmodel.put(1)`. PyNose's precision on that rule rests on 2 instances. Measured detector precision on LLM-generated tests varies widely by smell (Assertion Roulette precision 0.55–0.62 with recall 1.0). A toy dataflow lint (own trial) caught direct and variable-mediated R use but missed helper-function indirection and dynamic import. *Inference*: the anchoring lint is cheap to build but leaky, and should back up a read scope, not replace it.

### Cited Findings

**F2.1 PyNose (Python test-smell detector).** Wang, Golubev, Smirnov et al., **ASE 2021** (DOI 10.1109/ASE51524.2021.9678615). G: A. FT: yes. n/setting: a manually labelled validation set (the authors built their own oracle), unittest-based Python projects. "Correct" = matches the authors' manual labels. Results:
- Weighted precision 94.0 %, recall 95.8 %, F1 94.9 % over all smells.
- Redundant Assertion is defined as "(1) the expected and actual parameters of equality are the same, e.g., assertEqual(X, X) or (2) the assertion of truth is carried out on the unchangeable object, e.g., assertTrue(True)". It was validated on **2 instances** (100 % precision and recall).
- PyNose targets the unittest framework only (pytest-style bare `assert` is not its target, per the paper's scope statement).

T: direct (a Python tool), but the rule is not the anchoring property. Agents: human-written tests only. Indep.: **TA** (JetBrains Research authors) — [arXiv 2108.04639](https://arxiv.org/abs/2108.04639)

**F2.2 tsDetect and JNose on LLM-generated tests.** Ouédraogo et al., "On the Diffusion of Test Smells in LLM-Generated Unit Tests", **TOSEM** (Crossref DOI 10.1145/3838597). G: A. FT: yes (validation section). n/setting: 20,505 class-level LLM suites (GPT-3.5, GPT-4, Mistral 7B, Mixtral) plus 972 method-level cases, against a manual oracle of 240 classes and 447 methods. "Correct" = authors' manual labels. Results:
- Assertion Roulette: recall 1.0 for both tools, precision 0.55 (EvoSuite) and 0.60 (LLM) for tsDetect; JNose 0.34 and 0.62.
- Magic Number Test at method level: JNose 1.00/1.00, while tsDetect detected 0 of 24.
- Conditional Test Logic: tsDetect recall 0.44.
- Finding 7: "TsDetect and JNose often disagree … relying on a single detector can substantially bias" results.
- Redundant Assertion appears in prevalence tables but was not among the manually validated smells.

T: analogous (Java). Agents: LLM-generated tests measured. Indep.: — (third-party evaluation of both tools) — [arXiv 2410.10628](https://arxiv.org/abs/2410.10628)

**F2.3 Tautological tests: practitioner definitions only.** The searches found only blog and repo material defining the "tautological test" (expected value computed by the code under test). Examples: a SpecStory learning page; a GitHub issue proposing a "tautology" category for the perch tool, which is "a design proposal, not a shipped feature" per the search extract. A Robot Framework smell paper (arXiv 2111.02317) flags expected values computed during the test, per the search extract. G: C/D; FT: no [unreachable/not fetched]. Leads only — [perch issue](https://github.com/lakeday-org/perch/issues/187); [arXiv 2111.02317](https://arxiv.org/pdf/2111.02317)

**F2.4 Own trial: toy anchoring lint** (grade: own trial; the scratchpad `d5_scripts/anchor_lint.py`). An AST lint tracked taint from imports of `refmodel` or `spec_helpers` through assignments inside each `test_*` function to `assert` statements. Six synthetic cases:
- flagged: direct `== refmodel.put(1)` and via a local variable (`exp = rput(1)`);
- missed: a module-level helper `_exp()` wrapping `refmodel.put`, and `importlib.import_module('ref'+'model')`;
- not targeted: SUT self-comparison `sut.put(1) == sut.put(1)` (a separate rule is needed);
- correctly silent: a literal expected value.

A module-level "does this file import refmodel at all" rule would catch the helper case, but not the dynamic import. A runtime import guard catches dynamic import but not `exec(open(...))` (F1.9). Neither catches **copy-pasted R logic** inside the test (*Inference*: that needs clone detection or review). n = 6 synthetic cases; no precision/recall claim. T: direct (Python). Agents: not measured.

**F2.5 LLM-based smell detection (lead).** Search extracts point to an empirical study of LLMs detecting and correcting test smells (arXiv 2506.07594) and an earlier one (arXiv 2407.19261). Not fetched [lead only]; neither targets anchoring per the extracts.

### Inferences
- *Inference*: the "lint that no expected value is computed by R" is best implemented as three layers, with weakest guarantees last:
  1. a read scope: R, spec and models are not on the expectation agent's file system (F1.9);
  2. a module-level import ban checked statically on the expectation-test directory (F2.4);
  3. a runtime import guard during expectation-test collection (F1.9).

  None is measured beyond the own trial.
- *Inference*: off-the-shelf smell tools give no coverage of this property, so "passes tsDetect/PyNose" is no evidence of anchoring independence. Their Redundant Assertion rule covers only the degenerate case where both sides are syntactically identical.
- *Inference*: detector disagreement in F2.2 means that any custom anchoring lint needs its own labelled validation set before its precision can be quoted.

### Gaps
- No measured precision/recall exists for any detector of SUT- or reference-computed expected values, in any language. Searches: "tautological assertion detection", "expected value computed by calling method under test", "oracle anchoring" (arXiv API: only Canedo).
- No study measures how often LLM-written tests compute expected values by calling the SUT or a helper. Mathews & Nagappan and Zhao measure the *effect* (regression oracles) but not this syntactic pattern.
- **Single-source flag**: the anchoring concept still rests on Canedo alone (A-pre, one system, not re-checked here).

---

## Q3. Detectors for added commitments (over-specification) in LLM-written tests

### Takeaway
Added commitments are now measured as the **leading cause of invalid LLM-written tests** in one full-text study. ConVerTest (ICST 2026, A) found that 28 % of 100 sampled invalid tests "expect behavior not requested in the spec" (79 % inter-annotator agreement). It filters such tests through agreement with independently generated code, at precision 84–91 % and recall 89–96 % against ground-truth validity. Running tests against many known-correct solutions (CodeContests+, A) is the measured large-scale form of the allowed-variant check: it exposed over 4,000 original CodeContests problems whose tests reject almost all correct submissions. Citation-based traceability detection has one measurement, and that measurement is circular. LLM judges over-reject correct code, and humans judge incorrect assertions poorly.

### Cited Findings

**F3.1 Root causes of invalid LLM tests, and consensus filtering (ConVerTest).** Taherkhani, DaghighFarsoodeh, Chowdhury, Pham, Hemmati, **ICST 2026** (Crossref DOI 10.1109/ICST69053.2026.00039). G: A. FT: yes. n/setting: BigCodeBench and LBPP; GPT-5-mini, CodeQwen3, Gemma3; tests generated from the docstring with no implementation. "Valid" = passes the ground-truth implementation. Results:
- Root-cause analysis of 100 randomly sampled invalid tests by two graduate students (79 % agreement, third resolving): "Expecting behavior not requested in the spec" 28 %, wrong API 19 %, misunderstood logic 15 %, misread edge case 12 %, docstring ambiguity 12 %, violated preconditions 7 %, output format 7 % (Table IV). Example: asserting in-place sorting "when the docstring only specifies that a sorted list should be returned".
- Detection by "Dual Execution Agreement" with LLM-generated code (CoVe) plus self-consistency: precision (= validity of kept tests) rose from 51–77 % to 84–91 %, recall (valid tests kept) 89–96 %, coverage and mutation score down 0–2 points (Table II).
- The authors' rationale: "When a test expects a behavior not specified in the docstring, it will likely fail against a code solution generated via the rigorous CoVe process".

T: analogous (Python function and library tasks, stateless). Agents: LLMs measured. Indep.: **TA** — [arXiv 2602.10522](https://arxiv.org/abs/2602.10522)

**F3.2 Running tests against many correct solutions (allowed variants at scale).** Wang et al., CodeContests+, arXiv 2506.05817 (EMNLP 2025 Findings per Semantic Scholar and the ACL Anthology link in the search results). G: A. FT: yes (§4 evaluation). n/setting: 100 correct and 100 incorrect human submissions per problem from 1.72 M labelled submissions; more than 300 M executions. TPR = share of correct solutions accepted; a low TPR "primarily indicates that the test case itself is flawed". Results:
- Original CodeContests had "over 4000 problems with TPR ≤ 0.1 and TNR ≥ 0.9". The authors give two causes: incorrect test cases, and no custom checkers for multi-solution problems (i.e., over-strict exact-output oracles).
- CodeContests+ (agent-generated generators, validators and checkers) roughly doubled the problems with TPR and TNR ≥ 0.9.

T: analogous (competitive programming). Agents: an LLM agent system generated the tests. Indep.: **TA** (own dataset; the comparison is against the earlier CodeContests) — [arXiv 2506.05817](https://arxiv.org/abs/2506.05817)

**F3.3 Over-strict tests in a curated benchmark drive gaming.** EvilGenie (as F1.8). 9 of 154 LiveCodeBench problems (7 found by a GPT-5 classifier, 2 in manual review) are "ambiguous": the "evaluator accepts only a single output despite the existence of multiple valid outputs", or tests violate the spec. "We observe much higher rates of reward hacking on ambiguous problems." G: A-pre. FT: yes. T: analogous. Agents: measured. Indep.: — — [arXiv 2511.21654](https://arxiv.org/abs/2511.21654)

**F3.4 Citation-based traceability detection: circular measurement.** Panda, "Citation Discipline in Spec-Driven Development", arXiv 2606.30689 (2026, single author, no venue). G: A-pre (low weight). FT: yes. n/setting: 20 tasks × 4 conditions (Claude Sonnet 4.6, 240 implementations) and 50 tasks (GLM-5-turbo, 600). Results:
- Detection rate (TDR) 86.4 % and 88.0 %, FPR 0 %, for the "orphan-REQ" set-difference check. TDR is 0 % for all conditions without inline citations.
- But the "hallucinations" were **injected by the author with fake IDs**: "Hallucinated lines cite fake REQ IDs (e.g., REQ-099.1.1 …). None of these fake IDs appear in any legitimate specification". The check therefore detects fake IDs by construction. It measures nothing about real LLM additions that cite a *valid* ID.
- The paper does show that injected additions "pass functional test suites".

T: analogous (code, not tests). Agents: LLMs generated the code; the hallucinations were not LLM-made. Indep.: **TA** (the author's own framework, traceSDD) — [arXiv 2606.30689](https://arxiv.org/abs/2606.30689)

**F3.5 LLM judges over-reject correct code against NL requirements.** Jin & Chen, "Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement", *Automated Software Engineering* journal (Crossref DOI 10.1007/s10515-026-00638-5; Semantic Scholar mislabels it as the ASE conference). G: A. FT: **partial** (abstract, setup, one table excerpt). n/setting: HumanEval-X-Bugs, a buggy MBPP and QuixBugs (>700 tasks), five models. Results:
- "LLMs frequently misclassify correct code implementation as non-compliant". Prompts "requiring explanations and proposed corrections, lead[] to higher misjudgment rates".
- One model's FNR is quoted as 26.2 % (HumanEval) and 35.9 % (MBPP) before explanation prompts. The full table was not read.

T: analogous. Agents: LLMs measured. Indep.: — . *Relevance*: an LLM traceability judge for added commitments will produce false "not stated" flags, the same over-rejection direction the verified edition already noted for LLM judges — [arXiv 2603.00539](https://arxiv.org/abs/2603.00539)

**F3.6 Humans poorly judge incorrect LLM assertions.** Kaufman, Brun, Murali, Endres, arXiv 2607.08885 (2026). G: A-pre. FT: abstract and introduction. n/setting: a controlled experiment with 86 Python programmers. Results:
- Accuracy was 74 % on correct assertions vs 49 % on incorrect ones (OR = 2.94, p < 0.001), with similar confidence in both.
- Low-quality NL explanations lowered accuracy (OR = 0.58, p = 0.037) while raising confidence.

T: analogous. Agents: human judges of LLM-generated assertions. Indep.: — . *Relevance*: human adjudication of flagged added commitments is itself error-prone in the "accept wrong" direction — [arXiv 2607.08885](https://arxiv.org/abs/2607.08885)

### Inferences
- *Inference*: ConVerTest's detector is a **variant check with generated variants**: tests are kept only if they pass independently generated code. Over-strict tests (added commitments) fail on variants that do not make the extra choice. That is the mechanism of the verified edition's allowed-variant check (R15), now measured at 84–91 % precision. **But** a test sharing a misreading with the generated code survives by construction. The check removes idiosyncratic added commitments, not common-mode ones.
- *Inference*: CodeContests+ shows the allowed-variant check works at scale when **many independently written correct variants exist** (human submissions). For a library spec, such variants must be built: NonDex-style perturbation of R, or independently written R variants per non-promise. Their cost is not measured.
- *Inference*: requiring each expectation test to cite a decision and scenario (the verified edition) makes *uncited* assertions mechanically visible (F3.4 shows only this). Detecting an assertion that cites a valid decision but asserts more than it says still needs the variant check or a judge, and judges over-reject (F3.5). Human adjudication misses wrong assertions about half the time (F3.6).

### Gaps
- No study measures added commitments in **acceptance** tests (Gherkin, BDD) against the requirement with a ground truth. ConVerTest covers unit tests from docstrings. Sami et al. (already in the earlier reports) praise additions.
- No measured precision for an LLM test-to-requirement traceability judge on *tests*. TraceLLM and similar requirement-to-code traceability results were seen only as search extracts (precision 0.40–0.89 by dataset) and were not read [lead only].
- No NonDex-style perturbation study on LLM-written tests was found.
- **Single-source flag**: the "28 % of invalid tests are added commitments" figure rests on ConVerTest alone (n = 100 sampled invalid tests, TA).

---

## Q4. Does information-flow isolation reduce common-mode errors between LLM-written spec and tests (or fail to)?

### Takeaway
Measured evidence exists for **code → test** common mode, not for **spec → test**. Isolation reduces it substantially (F1.1: 14 % → 25 % detection; F1.2: 57.1 % → 78.3 % test accuracy when the code is wrong) but leaves most hard faults undetected (25 %). Independently generated tests and code still agree on shared misreadings: ConVerTest's consensus cannot remove them by design, and SAGA finds LLM errors tightly clustered. No study isolated a spec writer from a test writer and measured shared misreadings. The verified edition's position that isolation is "necessary, not sufficient" is reinforced, by analogy.

### Cited Findings
- **Isolation reduces, but does not remove, code → test common mode.** Fresh-context generation detected 25 % vs 14 % of hard faults (F1.1, A-pre). Description-only test accuracy was 78.3 % vs 57.1 % with incorrect code on HumanEval (F1.2, A). The authors of F1.1 write that when descriptions are "ambiguous or underspecified … both the generated code and the generated tests may converge to the same incorrect interpretation" (authors' discussion; not separately measured) — [arXiv 2607.05139](https://arxiv.org/abs/2607.05139); [arXiv 2409.09464](https://arxiv.org/abs/2409.09464)
- **Residual common mode among isolated LLM artefacts.** SAGA: LLM-derived verifiers miss human-written bugs at a much higher rate, and LLM errors "cluster tightly" (F1.5, A, partial read) — [arXiv 2507.06920](https://arxiv.org/abs/2507.06920). ConVerTest: 12 % of invalid tests trace to docstring ambiguity and 15 % to misunderstood logic. Its consensus filter keeps tests that agree with generated code (F3.1) — [arXiv 2602.10522](https://arxiv.org/abs/2602.10522)
- **Earlier-report baseline, unchanged here:** Knight (B) and Eckhardt & Lee (B) on correlated failures of independently written versions; Kim et al. (ICML 2025) on correlated LLM errors (verified edition §2.5).

### Inferences
- **Baseline qualification 1.** Verified edition, §2.3.3, verbatim: "Canedo's anchoring predicate becomes a dataflow/import lint." Qualification: an import-level lint alone is bypassable. Own trial: helper indirection and dynamic import evade the toy dataflow lint, and `exec(open(...))` evades a runtime import guard (F1.9, F2.4). No existing smell detector implements the predicate (F2.1, F2.2). The lint should therefore sit *behind* a file-system read scope. This does not contradict the baseline's intent; it adds an enforcement layer.
- **Baseline qualification 2.** Verified edition, §3 open questions, item 16, verbatim: "16. Over-strictness of LLM-written acceptance tests has not been measured." Qualification: it remains unmeasured for *acceptance* tests. For LLM-written *unit* tests from docstrings, ConVerTest measured that 28 % of 100 sampled invalid tests expect unrequested behaviour, and that consensus with generated code filters invalid tests at 84–91 % precision (F3.1, A, TA). For human-curated benchmark tests, CodeContests (>4,000 problems with TPR ≤ 0.1, F3.2) and LiveCodeBench (9/154 ambiguous, F3.3) show over-strict oracles at scale. The open question narrows to acceptance-level tests and stateful APIs.
- **Baseline reinforcement.** Verified edition table S8, verbatim: "Necessary, not sufficient." F1.1 (isolated tests still detect only 25 % of hard faults) and F1.5 (clustered LLM errors) reinforce it, at the code → test level (analogous).
- *Inference*: the cheapest measured isolation, a fresh session that holds only the record text, already gives a significant gain (F1.1). A deliberately different derivation, as the verified edition recommends for hard scenarios, is still supported only by human-only and analogous evidence.

### Gaps
- No study measures **spec → test** common mode: an LLM spec writer and an LLM test writer, with and without isolation, scored on seeded misreadings. This is still the central trial named in the verified edition (R13).
- No study measures whether **different-provider** test writers reduce code → test common mode, beyond the MCQ evidence already in the earlier reports.

---

## Recommendations (D5 only)

| # | Recommendation | Confidence | Load-bearing sources | One finding that would overturn it |
|---|---|---|---|---|
| D5-R1 | Generate expectation tests in a **fresh session** that receives only the records (decision, scenarios, options). Never reuse the conversation that wrote the spec, models or R. | medium | F1.1 (A-pre, single source for the fresh-context effect); F1.2 (A); F1.3 (A-pre, TA, confounded) | A spec-level trial in which fresh-session expectation tests kill no more seeded spec misreadings than tests written in the spec-writer's session |
| D5-R2 | Enforce isolation as a **file-system read scope** (R, spec and models not mounted for the expectation agent). Back it with a static module-level import ban and a runtime import guard on the expectation-test directory. Treat the lint as backup, not proof. | medium (mechanism) / low (effect) | F1.9 and F2.4 (own trial); F2.1–F2.2 (no existing detector covers it); Canedo (A-pre, baseline) | Evidence that agents under a read scope still reproduce R's specific choices at the same rate as agents with access (e.g., via shared training data or record wording) |
| D5-R3 | Run an **allowed-variant filter** on expectation tests. Any test failing on an R variant that makes a different allowed choice is flagged as an added commitment. Variants come from the non-promise register (NonDex-style perturbation) or are written independently. Report RejectLegal and DetectFault together. | medium | F3.1 (A, TA); F3.2 (A, TA); NonDex (baseline); F1.6 (metric definitions) | A trial in which variant failures are dominated by variants that break other clauses, so over-strictness cannot be isolated (same overturn condition as baseline R15) |
| D5-R4 | Require decision and scenario citations per expectation test, and mechanically reject uncited or unknown-ID assertions. Do **not** treat a valid citation as evidence of no added commitment. | low–medium | F3.4 (A-pre, circular, TA); F3.5 (A, partial); F3.6 (A-pre) | A measurement showing that real LLM added commitments mostly carry no citation or a wrong one (which would raise confidence), or mostly cite the correct decision (which would make the check near-useless) |
| D5-R5 | Do not rely on off-the-shelf test-smell detectors (tsDetect, JNose, PyNose) for independence. Use them only for maintainability. | high | F2.1 (A, TA; rule definition); F2.2 (A) | A detector release with a validated rule for SUT- or reference-computed expected values |

---

## What this track did not do
- Did not read in full: AgentLeak (F1.7, lead only); SAGA beyond the introduction (F1.5); Jin & Chen beyond the setup and one table excerpt (F3.5); Kaufman et al. beyond the abstract and introduction (F3.6); arXiv 2506.07594 and 2407.19261 (LLM smell detection); TraceLLM and R2Code (traceability precision); SpecBench, "capped evaluation with randomized tests" (arXiv 2606.07379), the ASE 2026 paper "Correct According to Whom? Auditing What LLM-Generated Tests Actually Check" (Dagger; Crossref confirms ASE 2026; no open full text found); Testora (Pradel); Nexus, CANDOR, AdverTest.
- Did not verify the NeurIPS 2025 venue for SAGA or the EMNLP 2025 Findings venue for CodeContests+ beyond Semantic Scholar and the search-result link.
- Did not re-check Zhao, Konstantinou 2024, Mathews & Nagappan, Canedo or DSpec2Test; they are taken from the verified edition.
- Did not run any detector (tsDetect, PyNose) on LLM-written tests. The own trials are synthetic toy cases (6 lint cases, 4 import patterns) and give no precision/recall.
- Found no measured study of OS or sandbox read scopes for test-writing agents, and none of spec → test common mode.
- Did not cover the MSR literature on human-written test-implementation coupling beyond Huo & Clause (baseline).

## Self-check
- **"Isolation from code" vs "isolation from spec/reference model".** All measured isolation effects (F1.1–F1.4) withhold an *implementation*. I map "implementation" to R (the executable reference model). That mapping is fair, since R is code. Mapping it to the *spec* or *formal models* is inference, and I label it so.
- **F1.1 terminology.** The paper's "Test-Driven Workflow" is a fresh session with the task description only. Its "Agentic Workflow" is the same conversation. I report the +11.7 % as the fresh-context effect, and the 25 % vs 14 % abstract figures as "independent vs after faulty code". These may come from slightly different comparisons (RQ1 vs RQ3). I did not reconcile them exactly.
- **Percentages in F1.1.** The paper reports some differences as "%" without stating whether they are relative or percentage points. I quote them as given.
- **ConVerTest "precision".** In ConVerTest, precision equals the validity rate of the kept tests, not detector precision on added commitments specifically. The 28 % figure comes from the root-cause sample, not from the detector's output. I may have overstated the link by calling the filter an "added-commitment detector". It filters all invalid tests, of which added commitments are the largest category.
- **CodeContests+ as allowed-variant evidence.** Its "correct solutions" are human contest submissions to problems with often unique outputs. The TPR failures mix wrong tests with missing multi-solution checkers. Only the second is over-strictness in the brief's sense.
- **Grades.** Venue-based grades for ICSE 2026 (Huang), ICST 2026 (ConVerTest), TOSEM (Ouédraogo) and the ASE journal (Jin & Chen) were confirmed through Crossref. AgentCoder is graded A-pre because no venue was found. A later venue would raise it.
- **Brief scope.** "Minimal" and "no organisation design" were read as: list mechanisms and measured effects, with no roles or process charts. The recommendations table stays at the mechanism level. The sandbox, import-ban and guard layering is my own inference, tested only by the own trial.
- **Independence flag on Huang et al.** I did not set TA for the ICSE 2026 incorrect-code study, although the same group built AgentCoder, which benefits from the conclusion. A stricter reading would flag it.
