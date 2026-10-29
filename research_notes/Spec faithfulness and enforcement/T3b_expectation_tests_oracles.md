# T3 (second half): Expectation tests derived independently from prose, and oracles for non-commitment

Scope: (1) acceptance/expectation tests derived from natural-language records independently of the spec and model; how to keep them independent; evidence that independently derived oracles catch more. (2) Oracles that accept exactly the allowed set for unspecified / optional / deliberately-not-promised / profile-declared / indeterminate behaviour, on the executable reference model. Spec-enforcing test generation and layer conformance are covered by another researcher. Items in brief §3 (nl2postcond, SpecGen, ImpossibleBench, ioco quiescence, Elle/Porcupine/Knossos, ShardStore has-failed) are not re-surveyed; where touched, it is flagged.

Grades per brief §6: A peer-reviewed/measured; A-pre arXiv; A-workshop; B industrial practice with data or normative docs; C practitioner report; D opinion. [unreachable] = full text not fetched; abstract/snippet content only, used as lead. *Inference* = my reasoning.

Full texts read (scratchpad, not repo): arXiv 2410.21136v2, 2607.22883, 2412.14137, 2403.14965, 2504.07244, 2510.18861, 2404.10100, 2503.15223, 2608.17214, 2305.05567; Ricca et al. 2007 (ECEASST); Leveson et al. 1990 (TSE, scanned copy); Barr et al. 2015 (TSE, UCL OA copy); NonDex JPF 2016 workshop paper; WebAssembly interpreter README + relaxed-SIMD Overview + relaxed_madd_nmadd.wast; JSON-Schema-Test-Suite README; sqllogictest about.wiki (GitHub mirror gregrahn/sqllogictest); LTP Open POSIX Test Suite HOWTO_ResultCodes.

---

## Q1. Specification by example / ATDD / BDD / FIT: measured evidence on defect detection and on requirements misunderstanding caught

### Takeaway
Measured evidence is thin, old, student-based and mostly about *comprehension* and *task correctness* when executable acceptance tables are supplied, not about how many specification misreadings an independently derived acceptance suite catches. No study found measures "expectation tests catch misreadings that a spec-derived suite misses". BDD's own systematic mapping (166 papers) reports an acute shortage of empirical and industrial evidence. All of it is human-only evidence.

### Cited Findings
- **Ricca, Torchiano, Di Penta, Ceccato, Tonella (2007), "The Use of Executable FIT Tables to support Maintenance and Evolution Tasks", ECEASST / Software Evolution 2007 — grade A-workshop, full text read.** Pilot controlled experiment, n = 13 master students (Trento), 2 small Java systems (LaTazza, AveCalc), balanced 2×2 design, 4 change requests each (2 corrective, 2 evolutive). "Correct" = passing a *separate, alternative JUnit acceptance suite* written by the experimenters. Preliminary result: FIT tables helped subjects perform the maintenance/evolution tasks correctly; time difference between groups not significant. Human-only evidence. — [Ricca et al. 2007 PDF](https://profs.scienze.univr.it/ceccato/papers/2007/evol2007.pdf)
  - Note for the pipeline: the experimenters themselves judged correctness with a second, independently written acceptance suite — a small instance of "two test families" in practice. — same source.
  - The same paper cites Melnik et al. (2004) as showing FIT tables plus executability improve requirement comprehension, and a preliminary study (Torchiano, Ricca, Penta 2007) showing FIT availability lets programmers complete more maintenance tasks, without measuring correctness. — same source.
- **Ricca et al., ICSE 2008, "Are Fit tables really talking? A series of experiments…" — [unreachable], grade A if confirmed.** Abstract-level only: three controlled experiments; improved correctness with no significant time impact; benefit varies substantially with developer experience. — [Index entry](https://www.sciweavers.org/node/34777); [DOI 10.1145/1368088.1368138 via bibtex mirror](https://bibtex.github.io/ICSE-2008-RiccaPTTCV.html)
- **Ricca et al., IST 2009 (two experiments, Trento + Politecnico di Torino) — [unreachable].** Abstract-level: Fit helps requirement understanding without significant additional effort; an earlier IWPSE 2007 abstract says "significantly improve requirement understanding, but tend to involve additional effort" — the two abstracts disagree on effort. — [IRIS UniGe](https://iris.unige.it/handle/11567/284198); [IWPSE 2007 page](https://profs.scienze.univr.it/~ceccato/papers/2007/iwpse2007.html)
- **Melnik, Maurer, Chiasson (Agile 2006), "Executable acceptance tests for communicating business requirements: customer perspective" — [unreachable].** Abstract-level: customers partnered with an IT professional can use storytest-based specifications to communicate and validate functional business requirements. No defect figures retrievable. — [bibsonomy record](https://www.bibsonomy.org/bibtex/119d31c1ca8fea04b1f092d82a85eda13/teresadaniela)
- **Binamungu & Maro (2023), "Behaviour Driven Development: A Systematic Mapping Study", JSS — grade A, full text (arXiv) read.** 166 papers 2006–2021; findings: dominance of conference papers, scarce research with industry insights, "acute shortage of metrics for measuring various aspects of BDD specifications"; call for more case studies and experiments. — [arXiv 2305.05567](https://arxiv.org/abs/2305.05567)
- Haugset & Stålhane (ATDD industrial) — not fetched; [unreachable] / not searched to full text. Listed as verification debt.

### Inferences
- *Inference:* The FIT experiments test whether *giving developers* executable acceptance tables improves their output; they do not test whether acceptance tests derived *independently of a spec* catch misreadings in that spec. Their transferable message is narrower: concrete example tables reduce misunderstanding by the implementer (here: the agent writing the spec or model), and correctness is best judged by a separately written suite.
- *Inference:* The brief's records already contain the raw material of specification by example (per decision: concrete scenario, options, decision). The scenario is the natural seed of an expectation test (Given/When/Then); the options not chosen are seeds for negative expectations ("must not"). No measured study of this "options as negative examples" use was found.

### Gaps
- No controlled experiment or industrial dataset found that counts requirements misinterpretations caught by ATDD/BDD suites versus spec-derived suites.
- Full texts of Ricca ICSE 2008 / IST 2009, Melnik 2006, Haugset & Stålhane not retrieved; their n and effect sizes are unverified here.

---

## Q2. LLM generation of acceptance tests / Gherkin / test cases from requirements text (2023–2026)

### Takeaway
Published LLM Gherkin/acceptance-test studies measure syntax validity, executability and user-perceived usefulness — not semantic faithfulness to the requirement and not whether the tests catch a misinterpretation. One industrial study explicitly praises the model for going *beyond* the explicit requirements, which is exactly the "added commitment" failure mode in the brief. Interactive test-based intent clarification (TiCoder) is the only measured case where generated tests were used to catch intent mismatch, with large effect but an idealised user proxy.

### Cited Findings
- **Karpurapu et al. (2024), "Comprehensive Evaluation and Insights into the Use of LLMs in the Automation of BDD Acceptance Test Formulation" — A-pre, full text read.** ~50 real user stories (Mendeley dataset + a blog); GPT-3.5, GPT-4, Llama-2-13B, PaLM-2; zero- vs few-shot. "Correct" = *validation accuracy = feature files without Gherkin-lint syntax errors / total*. GPT-3.5/GPT-4 with few-shot best; zero-shot accounts for 89% of all syntax errors. Semantic adequacy not measured. Agents measured: yes (LLM generation), but only for syntax. — [arXiv 2403.14965](https://arxiv.org/pdf/2403.14965)
- **Sami et al. (2025), "Acceptance Test Generation with LLMs: An Industrial Case Study" (AutoUAT + Test Flow, Critical TechWorks/BMW supplier) — A-pre, full text read.** GPT-4 Turbo. Workshop with 6 experienced product owners (15 min intro + 15 min hands-on), average quality 8/10. Two-month company-wide deployment: 166 uses, 65 feedback responses, 62 answered "Was this AT useful?" positively (95%). Test Flow: 92% of generated Cypress scripts "useful" (after prompt iteration). "Correct" = user-perceived usefulness; for scripts, whether they accurately mirror the Gherkin scenarios. Users report the tool revealed overlooked error scenarios. The authors note "the last two scenarios demonstrate the model's ability to extend beyond the explicit requirements of the user story" — presented as a strength. Datasets not disclosed. — [arXiv 2504.07244](https://arxiv.org/pdf/2504.07244)
- **Fonseca, Lima, Faria (2025), AToMIC (MyBMW app) — A-pre, full text read.** Generates Gherkin, Page Objects and UI tests from JIRA tickets *and recent code changes*; 13 real issues, 170+ screen codebase; 93.3% of Gherkin scenarios syntactically correct, 78.8% Page Objects ran without manual edits, 100% generated UI tests executed; survey of 9 practitioners (all report time savings). "Correct" = syntax/executability. Inputs include code, so the suite is not independent of the implementation. — [arXiv 2510.18861](https://arxiv.org/pdf/2510.18861)
- **Fakhoury, Naik, Sakkas, Chakraborty, Lahiri (2024), "LLM-based Test-driven Interactive Code Generation: User Study and Empirical Evaluation" (TiCoder), IEEE TSE 50(9) — grade A, full text read.** Workflow: LLM proposes tests; user says pass/fail; tests prune candidate code — tests as partial formalisation of NL intent. User study n = 15 programmers (8 professional, rest PhD students; 3 pilot of 18): participants with the workflow were significantly more likely to correctly evaluate AI-generated code and reported significantly less cognitive load. Automated evaluation (MBPP, HumanEval, four LLMs) with an *idealised user proxy* (the hidden reference solution answers the test queries): average absolute +45.97% pass@1 within 5 interactions. "Correct" = passing the benchmark's hidden tests. Agents measured: yes (generation), with human or oracle-proxy judging. — [arXiv 2404.10100](https://arxiv.org/pdf/2404.10100)
  - Example from the paper: for "strings of lowercase letters joined with an underscore", plausible LLM code accepts "aa_bb_cc", inconsistent with intent; a single concrete test exposes the misreading. — same source.
- (Baseline, not re-surveyed: nl2postcond and ClarifyGPT in §3.)

### Inferences
- *Inference:* "Correct" in the LLM-Gherkin literature is syntax, executability or perceived usefulness; none of these measures faithfulness to the record, and none would detect an added or reinterpreted commitment. The Sami et al. remark about extending beyond explicit requirements shows that, unchecked, an LLM expectation-test writer reproduces the brief's observed failure mode ("decision text that went beyond what was asked") in the test family.
- *Inference:* A guard that follows from this: every expectation test must cite the record decision and the scenario it instantiates, and any assertion not traceable to text in that decision (a value, an ordering, an error type) is rejected or flagged as an added commitment. This is a cheap, mechanical check (T4 traceability), not measured anywhere found.
- *Inference:* TiCoder's mechanism (concrete tests, yes/no judgement against intent) is the strongest available evidence that concrete examples expose misreadings; in the pipeline the "user" answering pass/fail would be the record (scenario + decision), read by a human or a separate agent.

### Gaps
- No 2023–2026 study found that measures whether LLM-generated acceptance tests catch misinterpretations in an intermediate spec.
- No study found of LLM acceptance-test generation for library APIs (as opposed to UI/user stories).

---

## Q3. Keeping a test family independent of the spec and the model

### Takeaway
The independence mechanisms with any evidence are: information hiding (derive from requirements only), separate teams (Cleanroom statistical testing, IV&V), and pseudo-oracles / N-version. The best measured study of spec-only checks (Leveson et al. 1990) cuts *against* strict independence for implementation faults: spec-only checks were the minority of effective checks; code-informed checks found more. For LLMs, recent evidence is clear that showing the code (or a model) to the test writer pulls oracles toward actual behaviour. Oracle "anchoring" (expected value computed by the system under test) is the concrete mechanism that destroys independence and can be checked.

### Cited Findings
- **Leveson, Cha, Knight, Shimeall (1990), "The Use of Self Checks and Voting in Software Error Detection: An Empirical Study", IEEE TSE 16(4) — grade A, full text read (scanned).** 24 graduate students, each first wrote self-checks from the requirements specification only (477 spec-based checks in total), then instrumented an existing version (Launch Interceptor Program, from the Knight–Leveson N-version experiment) with code-based checks. Results: of detected faults, 19% by specification-based checks, 43% by code reading, 38% by code-based checks; only 12% (4 of 34) of effective checks were formulated from the spec alone. Of 20 previously known faults, only 12 were detected; previously unknown faults were found, and new faults were introduced by instrumentation. The authors: "Although it has been hypothesized that acceptance tests in the recovery block structure should be based on the specification alone in order to avoid biasing the formulator of the test, our results indicate that the effectiveness of self checks can be improved when the specification-based checks are refined and expanded by source code reading." Self-checks and voting detected different faults; not substitutes. Human-only evidence. — [Leveson et al. 1990 (typeset.io copy)](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf)
- **Barr, Harman, McMinn, Shahbaz, Yoo (2015), "The Oracle Problem in Software Testing: A Survey", IEEE TSE 41(5) — grade A, full text read.** Defines a pseudo-oracle (Davis & Weyuker) as an alternative version produced independently (different team or language) whose outputs must agree; N-version oracle as majority/threshold agreement over k independent versions; contrasts metamorphic relations (one SUT, several executions, relation between outputs). Notes Feldt's genetic-programming and McMinn's transformation-produced versions as automatic diversity. — [UCL Discovery OA PDF](https://discovery.ucl.ac.uk/id/eprint/1471263/1/06963470.pdf)
- **Selby, Basili, Baker (1987), "Cleanroom Software Development: An Empirical Evaluation", IEEE TSE SE-13(9) — [unreachable] (DTIC copy 403).** Abstract-level: 15 three-person teams (10 Cleanroom, 5 traditional); Cleanroom combines formal specification, non-execution-based development and *statistically based independent testing*; Cleanroom products met requirements more completely and had a higher percentage of successful operationally generated test cases. Independence effect is confounded with the whole method. — [UMD DRUM record](https://drum.lib.umd.edu/items/fa62f393-c9f4-4e58-a2a0-02c7fa127224)
- **Konstantinou, Degiovanni, Papadakis (2024/2026), "Do LLMs generate test oracles that capture the actual or the expected program behaviour?" (v2 titled "Can we find bugs using LLM-generated oracles?") — A-pre, full text read.** 24 Java repositories; GPT-3.5-turbo, GPT-4o-mini, DeepSeek V3, Codestral (+ reasoning models). Classification task with four cells (correct/wrong code × correct/wrong assertion; buggy code from µBERT mutants). For correct assertions, accuracy drops when code is buggy, e.g. DeepSeek V3 43.02% (correct code) vs 35.72% (wrong code); GPT-4o-mini 51.15% vs 44.95%; Codestral 70.84% vs 62.34% (prompt MUT+TP). Overall accuracy sometimes < 50%; authors conclude "all LLM oracle suggestions need human inspection". Anonymised (EvoSuite-style) names drop accuracy up to 15.3–15.4 pp. Generation beats classification by up to 13.29 pp. Reasoning models show the same pull toward actual behaviour. "Correct" = assertion matches the original (expected) behaviour. Agents measured: yes. — [arXiv 2410.21136](https://arxiv.org/abs/2410.21136)
- **Zhao, Zhou, Cohen (2026), "Evaluating and Mitigating the Misguidance Effect of Buggy Code in LLM-Generated Unit Tests", PACMSE 3 (ISSTA 2026) — grade A, full text read.** 318 focal methods, 233 real Defects4J defects, 17 projects; 13 LLMs (Gemini 2.5, Claude 4 Sonnet, Grok, GPT-4.1, o4-mini, DeepSeek V3/R1, Qwen3). "Misguided test" = passes on buggy, fails on fixed; "effective" = fails on buggy, passes on fixed (fixed version = gold intent). Given buggy code: avg 137.69 misguided tests (3.84%) vs 16.46 (0.46%) when given fixed code; effective tests 104.15 (2.98%) vs 304.08 (8.51%), ~3× suppression. Stronger code-comprehension models were *more* susceptible. Mitigation: replace the code in the prompt with an LLM-generated specification docstring → misguided 137.69 → 113.00, effective 104.15 → 186.77. Removing code with no behavioural description: only 56.69% of tests pass on either version (vs 81.05%) — the model then guesses. Agents measured: yes. — [arXiv 2607.22883](https://arxiv.org/pdf/2607.22883)
- **Mathews & Nagappan (2024), "Design choices made by LLM-based test generators prevent them from finding bugs" — A-pre, full text read.** 287 real human-written buggy Python programs (Refactory dataset) with reference solutions; Copilot, Codium CoverAgent, CoverUp. Tests that pass on buggy and fail on reference ("bug-validating"): Copilot 12 (4.2%), CoverAgent 171 (59.6%), CoverUp 62 (68.1%) of final suites; CoverUp failed to produce a suite for 196 cases (68.3%). Tools that keep only passing tests systematically discard bug-revealing tests. Example: `find_sum` returning a+b+1, Copilot asserts `find_sum(1,2) == 4`. Agents measured: yes. — [arXiv 2412.14137](https://arxiv.org/abs/2412.14137)
- **Canedo (2026), "Oracles That Cannot Fail: Anchoring and the Expectation That Moves With the Fault" — A-pre, full text read; single author, one system.** Defines *oracle anchoring*: an expectation is specification-anchored when composed from values fixed outside the code under mutation, state-anchored when it flows from that code; a state-anchored oracle cancels the fault ("cannot fail"). Air-traffic-control simulator, 12 model-free property suites, 4 modules, 366 mutants. Re-anchoring one oracle on published procedure (no production change) recovers 8 of 46 surviving mutants; state-anchoring a healthy oracle loses 4 of 19; "a reference model on that population kills exactly what specification anchoring kills". The published test-smell rule would revert the repair. Human-authored tests (no agent measurement). — [arXiv 2608.17214](https://arxiv.org/pdf/2608.17214)
- NASA IV&V return-on-investment data — not retrieved; verification debt.

### Inferences
- *Inference:* For this pipeline, "independent" must be defined by *information flow*, not by team: the expectation-test writer (human or agent) may read the records only; it must not see the spec, formal models, or reference model; and no expected value in an expectation test may be computed by calling the reference model or any spec-derived helper (Canedo's anchoring predicate turned into a lint: expected values are literals or functions of record text only). This is checkable mechanically by dataflow/import analysis of the test files.
- *Inference:* The LLM evidence (Konstantinou; Zhao; Mathews) shows that seeing the artefact under test pulls oracles toward its actual behaviour; the reference model plays the role of "code" here, so an expectation-test agent with model access would confirm model misreadings. Zhao's result that even a docstring *derived from buggy code* improves effective tests suggests partial isolation helps, but the docstring there still carried the bug some of the time — so a spec-derived description is not a substitute for record-derived expectations.
- *Inference:* Leveson et al. is the main disconfirming datum: requirement-only oracles caught a minority of *implementation* faults. The expectation family's job is different — catching *misreadings carried into spec and model*, which code-informed oracles by construction cannot catch. So the right claim is complementarity: expectation tests target translation errors; spec-enforcing and code/model-informed tests target implementation errors. Strict independence should be required only of the expectation family.
- *Inference:* Selection-by-passing (CoverAgent/CoverUp keep only tests that pass) is a direct confirmation filter. An expectation-test pipeline must not drop tests because they fail on the reference model; a failing expectation test is a finding to be adjudicated against the record (record wrong? spec wrong? model wrong? test wrong?).

### Gaps
- No study found that applies Knight–Leveson-style coincident-failure analysis to *test oracles written by multiple LLMs or prompt lineages* (T5 territory).
- No measured data found on IV&V or Cleanroom separating the independence effect from the rest of the method.

---

## Q4. Evidence that independently derived oracles/tests catch more than spec- or code-derived ones

### Takeaway
Evidence that intent-derived oracles beat *code*-derived ones is now solid for LLMs (Zhao ISSTA 2026: ~3× more bug-finding tests when the model is not shown buggy code; Konstantinou; Mathews; baseline nl2postcond). Evidence that prose-derived oracles beat *spec*-derived ones — the brief's actual claim — was not found anywhere. Human evidence (Leveson 1990) shows requirement-only oracles catching fewer implementation faults than code-informed ones.

### Cited Findings
- Code-derived vs intent-derived LLM tests: misguided tests 3.84% vs 0.46%, effective tests 2.98% vs 8.51% (buggy vs fixed code shown), and specification-docstring prompting raises effective tests 104.15 → 186.77. — [Zhao et al. ISSTA 2026, arXiv 2607.22883](https://arxiv.org/pdf/2607.22883)
- LLM oracle classification accuracy drops when the code is buggy (e.g. DeepSeek V3 43.02% → 35.72% on correct assertions); reasoning models also affected. — [Konstantinou et al., arXiv 2410.21136](https://arxiv.org/abs/2410.21136)
- Coverage-driven LLM test tools retain bug-validating tests (59.6%, 68.1% of final suites). — [Mathews & Nagappan, arXiv 2412.14137](https://arxiv.org/abs/2412.14137)
- Spec-only self-checks: 19% of detected faults, 12% of effective checks; code-informed checks the rest. — [Leveson et al. 1990](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf)
- Re-anchoring an oracle on an external procedure recovered 8/46 surviving mutants; a reference model as oracle killed exactly the same set as specification anchoring (one system, one author). — [Canedo, arXiv 2608.17214](https://arxiv.org/pdf/2608.17214)
- **§3 baseline flagged, not challenged:** "specs derived from code confirm the code (SpecGen)" and "intent-derived postconditions find bugs (nl2postcond)" are consistent with the new full-text evidence above (Zhao, Konstantinou, Mathews). No new evidence contradicts them.

### Inferences
- *Inference:* The pipeline's chain is prose → spec → model. A misreading at prose → spec propagates to the model and to spec-enforcing tests consistently, so the spec-enforcing family is "anchored" on the spec in Canedo's sense for that class of fault. Only a family anchored on the prose can fail on it. This is argued, not measured.
- *Inference:* A small trial could measure the claim directly: seed known misreadings into the spec (clause mutants that contradict the record), regenerate the model, and count how many each family kills. This is a mutation experiment on the spec layer (overlaps T4).

### Gaps
- No study comparing prose-derived vs spec-derived oracles on the same faults. This is the central evidence gap for the expectation-test family.

---

## Q5. Oracles for non-commitment: accepting exactly the allowed set

### Takeaway
Mature conformance suites already encode typed non-commitment in the oracle language: WebAssembly uses `either` (allowed-outcome set) and NaN *patterns* (`nan:canonical`, `nan:arithmetic`) and, for relaxed SIMD, specifies a fixed per-environment choice from each set; sqllogictest canonicalises unspecified row order (`rowsort`/`valuesort`) and gates engine-specific behaviour (`skipif`/`onlyif`); JSON Schema separates `optional/` tests; POSIX test methods (IEEE 1003.3) give non-failure verdicts `UNSUPPORTED` (conditional feature absent) and `UNRESOLVED`. NonDex shows how to test the dual problem — tests that assume one behaviour of an underdetermined spec — by randomly exploring allowed behaviours, finding 60 OSS and 110 student bugs. Statistical/metamorphic oracles cover nondeterministic outputs where no single expected value exists.

### Cited Findings
- **WebAssembly reference-interpreter script format — grade B (normative tooling docs), full text read.** `assert_return` takes result *patterns*: literal, `nan:canonical` ("NaN in canonical form"), `nan:arithmetic` ("NaN with 1 in MSB of payload"), and `( either <result_pat>+ )` — "alternative results". So the oracle is set-valued with two encodings: an explicit finite set (`either`) and a predicate pattern (NaN classes). Other assertion kinds: `assert_trap`, `assert_exhaustion`, `assert_invalid`, `assert_malformed`, `assert_unlinkable`; the failure string is checked only as a prefix of the actual message. — [WebAssembly/spec interpreter README](https://raw.githubusercontent.com/WebAssembly/spec/main/interpreter/README.md)
- `either` is used in the core relaxed-SIMD tests, e.g. `relaxed_madd_nmadd.wast` lists alternative f32x4/f64x2 results (fused vs unfused). — [relaxed_madd_nmadd.wast](https://raw.githubusercontent.com/WebAssembly/spec/main/test/core/relaxed-simd/relaxed_madd_nmadd.wast)
- **Relaxed SIMD "Consistency" rule — grade B, full text read.** Two calls with the same inputs may return different results; the spec text adopted: "each such operator produces a fixed-size list of sets of allowed values. For each execution of the operator in the same environment, only values from the set at the same position in the list are returned, i.e., each environment globally chooses a fixed projection for each operator." `IMPLEMENTATION_DEFINED_ONE_OF(...)` returns any one of the listed results. — [relaxed-simd Overview.md](https://raw.githubusercontent.com/WebAssembly/relaxed-simd/main/proposals/relaxed-simd/Overview.md)
- **sqllogictest — grade B (official docs, read via GitHub mirror of SQLite's fossil repo; sqlite.org served a bot check).** Results for queries without ORDER BY: `nosort` only for ORDER BY or single-row queries "since otherwise the order of results is undefined and might vary from one database engine to another"; `rowsort` sorts rows client-side, `valuesort` sorts individual values. `skipif`/`onlyif <engine>` gate records per engine; labelled results are cross-checked even when skipped. Reference results are generated by running prototype scripts on *independently developed engines*, "millions of test vectors". — [about.wiki (mirror)](https://raw.githubusercontent.com/gregrahn/sqllogictest/master/about.wiki)
- **JSON-Schema-Test-Suite — grade B, read.** `optional/` "contains tests that are considered optional", noting it "currently conflates many reasons why a test may be optional" (not required by spec vs language-specific); `optional/format` requires runners to enable format validation where supported; `proposals/` hold volatile tests binding only implementations claiming the proposal. — [JSON-Schema-Test-Suite README](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/README.md)
- **Open POSIX Test Suite result codes (from IEEE 1003.3-1991) — grade B, read.** PASS, FAIL, UNRESOLVED ("blocked from fully completing and the pass/failure results cannot be determined"), UNSUPPORTED ("test is for a conditional feature that is not implemented"), UNTESTED (stub/incomplete). — [LTP open_posix_testsuite HOWTO_ResultCodes](https://raw.githubusercontent.com/linux-test-project/ltp/master/testcases/open_posix_testsuite/Documentation/HOWTO_ResultCodes)
- **NonDex (Shi, Gyori, Legunsen, Marinov, ICST 2016; JPF workshop paper 2016) — A-workshop read; ICST paper [unreachable] here.** Checks client code "against not just one behavior of the library but against a number of different behaviors—all of which are valid with respect to the underdetermined specification" (e.g. HashMap iteration order). ICST 2016 reported 60 bugs in open-source projects and 110 in student submissions; 13 pull requests opened, 12 accepted; Checkstyle integrated NonDex into CI. Human-only evidence (tool + human fixes). — [Gyori et al. JPF 2016 PDF](https://mir.cs.illinois.edu/gyori/pubs/jpf16.pdf); [NonDex repo](https://github.com/TestingResearchIllinois/NonDex)
- **Metamorphic / statistical oracles (Barr et al. survey) — grade A.** Metamorphic relation = constraint over several executions of one SUT; contrasted with pseudo-oracles; survey section on nondeterministic SUTs. — [Barr et al. 2015](https://discovery.ucl.ac.uk/id/eprint/1471263/1/06963470.pdf). Statistical metamorphic testing (Guderlei & Mayer 2007) and partial oracles (Patel & Hierons 2019, SQJ) — [unreachable]/lead only: a statistical oracle cannot decide a single test case and can err. — [Patel & Hierons 2019 (White Rose)](https://eprints.whiterose.ac.uk/148216/)
- **§3 baseline flagged, not re-surveyed:** ioco quiescence and unspecified-vs-nondeterministic outputs; history checkers (Elle, Porcupine, Knossos) accepting any valid linearization/consistency witness; ShardStore's has-failed relaxation instead of outcome sets. Nothing found that challenges them.

### Inferences
- *Inference — mapping of the brief's non-commitment types to oracle mechanisms with precedent:*
  - **Unspecified (one of a stated set):** explicit outcome set (`either`) when small; predicate/pattern (NaN classes) when the set is large but characterisable; canonicalisation (`rowsort`) when the freedom is ordering. If the record also promises stability (same choice every time), add a consistency check across calls (Wasm "fixed projection").
  - **Optional:** a separate, opt-in suite plus a third verdict `UNSUPPORTED` that is not a failure (POSIX), with the declaring profile choosing whether the suite runs (JSON Schema `optional/`; sqllogictest `onlyif`). The suite must still *fail* if the feature is claimed and wrong.
  - **Deliberately not promised:** an oracle that asserts nothing about the dimension, plus a NonDex-style *perturbing reference model* that randomly varies the non-promised behaviour; any test that then fails or flakes is over-strict. This converts "neither stricter" into a mechanical check.
  - **Profile-declared:** parameterise the oracle by the profile value (one suite, per-profile expected set — consistent with the §3 "typed schema plus one parameterised suite" rule) and check the per-environment fixed choice.
  - **Indeterminate:** accept both "took effect" and "did not take effect" at the call, and defer judgement to later observations (history-checker style, §3 baseline); a POSIX-like `UNRESOLVED` verdict is the precedent for "cannot be decided from this run", which must not count as pass.
- *Inference — blow-up versus relaxation (brief's §3 seed):* Wasm shows bounded sets stay small when the freedom is per-operation and local (2–3 alternatives per lane); sqllogictest avoids enumeration by canonicalising; NaN patterns avoid enumeration by predicate. These suggest outcome *predicates* and canonical forms, not enumerated sets, as the default for the reference model, with relaxation flags (ShardStore-style) reserved for state that becomes unknowable (faults, indeterminate commits). This is a design argument, not measured.
- *Inference:* `either` checks membership per call only; nothing in the Wasm script format seen expresses the cross-call "fixed projection" rule, so that guarantee is untested by the core suite unless a test compares two calls. A record that promises stability needs an explicit consistency test.

### Gaps
- No measured study found comparing outcome-set reference models against relaxation flags on cost or bug-finding.
- C/C++ implementation-defined behaviour conformance suites and SQL standard conformance (beyond sqllogictest) not examined in full text.
- Jepsen docs not re-read (history checking is §3 baseline).
- No agent/LLM measurement found for writing set-valued or non-commitment oracles.

---

## Q6. Tests that are neither stricter nor looser: evidence on over-strict and over-loose tests (beyond ImpossibleBench)

### Takeaway
Both failure directions are measured outside ImpossibleBench: tests that encode one implementation's choice of an underdetermined behaviour (NonDex: 170 bugs), brittle assertions (Huo & Clause, unreachable), and loose suites that accept wrong patches (PatchDiff on SWE-bench Verified: 29.6% of "plausible" patches diverge from ground truth; 6.4 pp resolution-rate inflation). Loose tests let agents add behaviour unnoticed; over-strict tests make agents game or overfit.

### Cited Findings
- **Wang, Pradel, Liu (2026), "Are 'Solved Issues' in SWE-bench Really Solved Correctly?", ICSE 2026 — grade A, full text read.** Plausible patches from CodeStory, LearnByInteract, OpenHands on SWE-bench Verified; differential patch testing (PatchDiff) against ground-truth patches. On average 29.6% of plausible patches are behaviourally distinguishable from the oracle patch; divergences due to similar-but-divergent implementations (46.8%) and to patches that "adapt more behavior than the ground truth" (27.3%); manual inspection: 28.6% of divergent patches certainly incorrect; combined weaknesses inflate reported resolution rates by 6.4 absolute pp. Agents measured: yes (agents' patches judged by tests). "Correct" = behaviour matching developer ground truth, verified manually. — [arXiv 2503.15223](https://arxiv.org/abs/2503.15223)
- **NonDex:** 60 OSS + 110 student bugs from tests/code assuming one deterministic behaviour of an underdetermined API. — [Gyori et al. JPF 2016](https://mir.cs.illinois.edu/gyori/pubs/jpf16.pdf)
- **Huo & Clause (2014), "Improving Oracle Quality by Detecting Brittle Assertions and Unused Inputs in Tests", FSE — [unreachable] (TLS failure on host).** Snippet-level: dynamic tainting finds brittle assertions (depend on uncontrolled inputs) and unused inputs; reportedly 164 tests with brittle assertions and 1,618 with unused inputs (secondary listing, unverified). — [author-course copy](https://personal.utdallas.edu/~lxz144130/cs6301-readings/oracle-huo-fse14.pdf)
- **OpenAI, "Introducing SWE-bench Verified" (2024) — [unreachable] (403).** Known as a source of annotation data on underspecified issues and unit tests that unfairly reject valid solutions; figures not verified here. — [OpenAI page](https://openai.com/index/introducing-swe-bench-verified/)
- **§3 baseline flagged:** ImpossibleBench / EvilGenie (agents game checks stricter than spec) not re-surveyed; consistent with the above.

### Inferences
- *Inference:* Two checks bound a test family from both sides on the reference model: (a) **allowed-variant check** — build variants of the reference model that make *different allowed choices* on every non-commitment (NonDex-style perturbation, or the §3 "two witness implementations"); every test must pass on all of them, else it is over-strict; (b) **forbidden-variant check** — per clause/record decision, a mutant that makes a *disallowed* choice (the §3 "mutant reference model" seed); some test in the right family must fail, else the suite is loose. PatchDiff's 27.3% "adapts more behavior" category is precisely what (b) at record granularity should catch.
- *Inference:* Expectation tests written from prose are especially prone to over-strictness, because a concrete scenario in a record fixes values the decision may leave open (e.g. an example ordering). The allowed-variant check is therefore most needed for the expectation family.

### Gaps
- No study found that measures over-strictness of LLM-written acceptance tests specifically.
- Huo & Clause and SWE-bench Verified annotation figures unverified (unreachable).

---

## Disconfirming searches relevant to this track (brief §5)
- (a) Partial disconfirmation found for the *independence* premise: Leveson et al. 1990 — requirement-only checks found 19% of detected faults; authors recommend refining spec-based checks with code reading. Applies to implementation faults, not translation faults. — [Leveson et al. 1990](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf)
- No study found showing that prose-derived acceptance tests catch more spec misreadings than spec-derived tests, and none showing the opposite. The question is open.
- (c) No published pipeline found that derives expectation tests from prose records independently of a spec and runs them on an executable reference model with non-commitment-aware oracles.

## Source grades (summary)
| Source | Grade | Full text | Agents measured |
|---|---|---|---|
| Ricca et al. 2007 ECEASST (FIT pilot, n=13) | A-workshop | yes | no, human-only |
| Ricca et al. ICSE 2008 / IST 2009 | A (if confirmed) | [unreachable] | no |
| Melnik et al. Agile 2006 | A (if confirmed) | [unreachable] | no |
| Binamungu & Maro 2023 JSS (BDD mapping, 166 papers) | A | yes (arXiv) | n/a |
| Karpurapu et al. 2024 (BDD gen, ~50 stories) | A-pre | yes | yes, syntax only |
| Sami et al. 2025 (AutoUAT, 65 responses) | A-pre | yes | yes, perceived usefulness |
| Fonseca et al. 2025 (AToMIC, 13 issues) | A-pre | yes | yes, syntax/executability |
| Fakhoury et al. 2024 TSE (TiCoder, n=15 + benchmarks) | A | yes | yes |
| Leveson et al. 1990 TSE (n=24) | A | yes | no, human-only |
| Barr et al. 2015 TSE | A | yes | n/a (survey) |
| Selby, Basili, Baker 1987 TSE (15 teams) | A (if confirmed) | [unreachable] | no |
| Konstantinou et al. 2024/26 (24 repos, 4+ LLMs) | A-pre | yes | yes |
| Zhao et al. ISSTA 2026 (233 defects, 13 LLMs) | A | yes | yes |
| Mathews & Nagappan 2024 (287 programs) | A-pre | yes | yes |
| Canedo 2026 (366 mutants, one system) | A-pre (single author) | yes | no, human-only |
| Wang, Pradel, Liu ICSE 2026 (PatchDiff) | A | yes | yes |
| NonDex JPF 2016 (citing ICST 2016) | A-workshop | yes | no, human-only |
| Huo & Clause FSE 2014 | A (if confirmed) | [unreachable] | no |
| WebAssembly interpreter README, relaxed-SIMD Overview, .wast | B | yes | n/a |
| sqllogictest docs (mirror) | B | yes | n/a |
| JSON-Schema-Test-Suite README | B | yes | n/a |
| Open POSIX Test Suite result codes (IEEE 1003.3) | B | yes | n/a |
| OpenAI SWE-bench Verified | B (if confirmed) | [unreachable] | — |
