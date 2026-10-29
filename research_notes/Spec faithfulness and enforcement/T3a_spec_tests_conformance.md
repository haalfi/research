# T3a: Spec-enforcing tests and conformance between layers (formal model ↔ executable reference model ↔ spec)

Scope: the first half of T3. It covers tests generated from formal models, contract → property tests, stateful model-based testing, history checking, environment actions as generated operations, and conformance bridges between layers. It does not cover expectation tests or non-commitment oracles (T3b).

Conventions:
- Grades follow brief §6.
- "[FT]" means the full text was fetched and read in this run. "[unreachable]" means it was not; such a source is a lead only.
- *Inference* marks my own reasoning.
- Each method states whether agents/LLMs were measured doing the step.
- Downloads are in `/tmp/claude-0/-home-user-research/8464aabb-24d6-53c7-af9a-cc609bb4c0f8/scratchpad/t3a/pdf/` (not in the repo).

Relation to brief §3:
- Nothing here re-surveys §3. Where §3 listed items as "could not re-check" (Cirstea et al., TraceLink, PObserve, Porcupine, arXiv 2409.14301), they are now re-checked from full text, and each says so.
- One explicit challenge to the §3 baseline (Porcupine cost claims) is flagged in Q3.

---

## Q1. Test generation from formal models (Quint/Modelator MBT, TLA+-based generation, Dafny test generation, P, Apalache/TLC trace export): measured results and cost

### Takeaway
Generating tests from a model and replaying them step by step against an implementation works well, and cheaply, when the implementation is small, self-contained and close in granularity to the model. This is exactly the position of an executable Python reference model. It fails or becomes expensive when the implementation is large and coarsely related to the model.
- Best measured cases: MongoDB Realm Sync, Mocket, Remix.
- The cheapest pattern is the "spec drives, implementation follows, compare state after each action" loop (Modelator/Quint Connect, Mocket, MongoDB MBTCG).
- Evidence for Dafny test generation and for P is thin or unreachable in this run.

### Cited Findings

**TLA+ → test-case generation (MBTCG), MongoDB Realm Sync**
- **Source.** Davis, Hirschhorn, Schvimer, "eXtreme Modelling in Practice", PVLDB 13(9) 2020. **Grade A [FT].** [arXiv 2006.00915](https://arxiv.org/abs/2006.00915)
- **Setting.** The target is MongoDB Realm Sync's operational-transformation merge rules: about 1,000 LOC, a self-contained function. A TLA+ spec was "deliberately written with a close correspondence to the implementation, via direct transcription".
- **Generation.**
  - TLC explored the state space, and a Go program translated it into C++ unit tests.
  - For an initial array of 3 elements and 3 clients with one operation each, it produced **4,913 C++ test cases**.
- **Coverage result.**

  | Test source | Branches covered (of 86) |
  |---|---|
  | 36 handwritten tests | 18 (21%) |
  | AFL fuzzing, about 8 million executions | 79 (92%) |
  | Generated tests | 86 (100%) |

- **Bug found by the model checker, not by the generated tests.**
  - The model checker hit a StackOverflowError: the ArraySwap/ArrayMove merge rule never terminated.
  - The same bug "also exist[ed] in the C++ code; the bug had faithfully been transcribed from C++ to TLA+". The paper found this surprising given the product's maturity and its randomized testing.
  - Outcome: ArraySwap was deprecated, which echoes Cedar dropping a feature.
  - Note on what this shows: the spec was transcribed from code, so a code bug was carried into the spec. Model checking caught it because the property (termination) was independent of the code.
- **Cost.** 1 engineer, 4 weeks: 795 LOC TLA+ and 755 LOC Go.
- **Authors' verdict.** "When MBTCG is possible, and when the state space is not too large, MBTCG is the gold standard of ensuring specification-implementation conformance."
- **Agents:** human-only evidence.

**TLA+ state-space-guided testing (Mocket)**
- **Source.** Wang, Dou, Gao, Wu, Wei, Huang, "Model Checking Guided Testing for Distributed Systems", EuroSys 2023. **Grade A [FT].** [PDF](https://gaoyu-cn.github.io/paper/2023-eurosys-mocket.pdf)
- **Method.**
  - TLC produces the state graph.
  - Mocket picks test cases by edge-coverage-guided traversal plus partial-order reduction. Each test case is an action sequence plus the expected state after every action.
  - Developers annotate Java code to map TLA+ variables and actions to code.
  - Mocket intercepts each annotated action, schedules it according to the test case, and compares states.
- **Results.**
  - 9 bugs in Xraft, Raft-java and ZooKeeper: 3 previously unknown implementation bugs (all confirmed), 4 known implementation bugs, and 2 new bugs in the official Raft TLA+ spec.
  - Time to detection ranged from under 1 minute to 29 hours.
- **Cost (Table 1).**

  | System | Implementation | Spec | Mapping annotations |
  |---|---|---|---|
  | Xraft | 16,530 LOC | 841 LOC, 15 vars, 17 actions | 151 LOC |
  | Raft-java | 15,017 LOC | 809 LOC | 152 LOC |
  | ZooKeeper | 15,895 LOC | 1,053 LOC, 25 vars, 20 actions | 134 LOC |

- **Comparison.** The authors contrast about 1,187 LOC to apply Mocket on ZAB with IronFleet's 1,400 LOC of spec plus 39,253 LOC of proof.
- **Agents:** human-only evidence.

**TLA+ multi-grained specs with conformance replay (Remix)**
- **Source.** Ouyang et al., "Multi-Grained Specifications for Distributed System Model Checking and Verification", EuroSys 2025. **Grade A [FT].** [arXiv 2409.14301](https://arxiv.org/abs/2409.14301). This was a §3 "could not re-check" item and is now re-checked.
- **Conformance check.**
  - The checker "explores model-level state space to generate traces, replays them in the implementation, and compares model- and code-level execution traces".
  - A central coordinator (Java RMI plus AspectJ instrumentation) schedules code-level actions one by one according to the model trace and **injects faults (node crashes) when needed**.
  - Developers supply a mapping from each model action to begin/end events in code.
- **What it found.** Spec/code discrepancies "ranging from inconsistent message types … to incorrect conditional branches and wrong variable assignments that lead to unrealistic state transitions".
  - Overall, 6 severe ZooKeeper bugs violating 5 invariant types were found and their fixes verified. These came mainly from model checking the fine-grained specs, with conformance checking keeping the specs honest.
- **Stated limitation, verbatim:** "The conformance checking is unsound. It could miss behaviors in implementation that are not modeled by the specification … We only check safety properties instead of liveness properties."
- **Cost.**
  - A new mixed-grained spec took "within 40 person-hours … by one person who is familiar with the ZooKeeper code and is proficient in TLA+".
  - mSpec-4 (no coarsening) took 2,793× longer than mSpec-3 to find the first violation.
- **Agents:** human-only evidence.

**Apalache counterexamples as tests (Informal Systems, Tendermint light client)**
- **Source.** Kuprianov & Konnov, "Model-based testing with TLA+ and Apalache", TLA+ Conf 2020 slides. **Grade C [FT]: claims without figures.** [Slides](https://conf.tlapl.us/2020/09-Kuprianov_and_Konnov-Model-based_testing_with_TLA_+_and_Apalache-Slides.pdf)
- **Pipeline.**
  1. "TLA+ tests" are written as assertions.
  2. Apalache produces counterexamples.
  3. A TLA+↔JSON export follows.
  4. "Testgen" turns abstract values into concrete Rust fixtures.
- **Claims.** "MBT eliminates the divergence between the specs and the code", "improves code coverage", "finds real bugs", and "benefits substantially outweigh infrastructure investments".
  - No numbers are given. A search found no published bug counts.
  - The crate README (lead only) says MBT is "limited to core verification".
- **Agents:** human-only.

**Quint Connect (Rust MBT library, 2025)**
- **Source.** Quint blog posts. **Grade C [FT]: vendor practitioner reports.** [Quint Connect launch](https://quint-lang.org/posts/quint_connect); [Emerald case study](https://quint-lang.org/posts/quint_connect_emerald)
- **Mechanism.**
  - The user defines (a) how to convert implementation state to spec state and (b) how to reproduce each spec transition in code.
  - The library replays Quint traces (random, witnesses or named runs) and compares state at each step.
  - Spec-side variables `mbt::actionTaken` / `mbt::nondetPicks` carry the chosen action and nondeterministic picks.
  - Ports exist for TypeScript, Clojure and Elixir. These are leads from [docs.rs](https://docs.rs/quint-connect) and search.
- **Agent use.**
  - The launch post says the library "was designed to work with LLMs" so that AI generates and maintains the glue code.
  - Emerald (EVM framework): "AI read the Emerald code, wrote a Quint specification with Choreo, and generated most of the test driver". Result: about 80% application-layer coverage and one memory leak found.
  - Failure actions (process restart, data corruption) were modelled and replayed as adversarial scenarios.
  - n = 1 system. No baseline. "Correct" is not defined beyond coverage plus one bug.
  - The spec was derived **from code**, which is the SpecGen-type risk in §3: it confirms the code rather than intent. *Inference.*

**Dafny test generation (DTest / `dafny generate-tests`)**
- **Source.** Fedchin et al., "A Toolkit for Automated Testing of Dafny", NFM 2023, LNCS 13903. **[unreachable]**: the Amazon Science PDF returned 404. [Amazon Science page](https://amazon.science/publications/a-toolkit-for-automated-testing-of-dafny)
- **What it is.** The author page (**B [FT]**, [link](https://sasha-fedchin.github.io/2024/12/06/dtest.html)) says DTest "relies on the Dafny verifier to generate test inputs that reach the requested section of your code", guarantees "statement or path coverage (depending on the settings)", can act as a dead-code linter, and "is officially part of Dafny".
- **Leads only (search extract).** Branch coverage was "comparable to the expectations developers set for manually written tests" on two open-source Dafny projects, and greedy generation gives "a test count near the theoretical minimum".
- **Gap: what is generated is coverage-directed inputs, not oracles.** The tests check Dafny-compiled code against its own contracts. For a Python reference model, *Inference*: one would need to compile Dafny to Python (Dafny has a Python backend) or port the generated inputs, then compare outputs against the Python model. No measured evidence of that bridge was found.
- **Agents:** none found.

**P / P# / PObserve**
- **Source.** Deligiannis et al., "Uncovering Bugs in Distributed Storage Systems during Testing (not in Production!)", FAST 2016. **Grade A [FT].** [PDF](https://www.doc.ic.ac.uk/~afd/papers/2016/FAST.pdf)
- **Method.** P# models the environment and specs; systematic testing controls the schedule over the real C# code.
- **Table 1.**

  | System | SUT LOC | Bugs | Harness LOC | Environment-modelling effort |
  |---|---|---|---|---|
  | vNext Extent Manager | 19,775 | 1 (a months-old liveness bug) | 684 | about 2 person-weeks part-time |
  | MigratingTable | 2,267 | 11 | 2,275 | about 5 person-weeks, built in parallel with the system |
  | Fabric user service | 31,959 | 1, unconfirmed | 6,534 | about 5 person-months |

- **Agents:** human-only.

**PObserve (official P docs)**
- **Grade B [FT]: describes the mechanism, no measured results.** [P docs](https://p-org.github.io/P/advanced/pobserve/pobserve). This was a §3 "could not re-check" item. Re-checked, but no data exists to re-check.
- **Mechanism.**
  - "Distributed runtime monitoring framework that allows checking formal correctness specifications on systems implementation using service logs". It needs a log parser plus P specs ("global invariants").
  - Pipeline: parse → time-stamped events → sequencer producing a globally sorted stream → demultiplexer to each spec monitor. Implemented with Java Streams.
  - Usable "during design, testing, and in production".
- **What I found no figures for:** bugs, cost or false-alarm rates. The motivation quoted from AWS service teams is anecdotal.
- **Agents:** none.

### Inferences
- The decisive variable is **granularity distance** between model and target, not the tool.
  - MongoDB's MBTCG worked on a transcribed 1 kLOC function, and its MBTC failed on a large server.
  - Remix and CCF had to add action composition or fine-grained modules to close the distance.
  - A Python reference model written *from the same clauses, at the same action granularity* as the TLA+/Quint model sits in the favourable regime. Making that an explicit design rule ("one reference-model method per spec action, the same state variables or a declared abstraction function") is the main cost lever.
- For a deterministic, single-process Python reference model, the controlled-scheduling infrastructure of Mocket, Remix and P# (coordinators, RMI, AspectJ) is unnecessary. The model can be driven synchronously. That removes most of the reported cost, which went into instrumentation and nondeterminism control.
- Model-generated tests inherit the model's blind spots.
  - Mocket found 2 bugs *in the spec*.
  - Remix calls its check unsound for unmodelled behaviour.
  - These tests enforce spec → reference model. They do not check faithfulness to prose. That remains T1/T3b's job.

### Gaps
- No measured result found for Quint/Modelator beyond vendor blog claims.
- No full text for DTest (NFM 2023).
- No P/PObserve paper with measured results was retrieved. The AWS CACM "Systems correctness practices at AWS" was not fetched.
- TLC/Apalache trace export used as test input appears only inside the cited systems. There is no separate evaluation.

---

## Q2. Contract → property tests (Hypothesis, QuickCheck, icontract-hypothesis, CrossHair, deal) and stateful model-based testing (RuleBasedStateMachine, QuickCheck state machines, Hughes' experience reports)

### Takeaway
Tooling to turn pre/postconditions into property tests exists and is documented, but this run found **no measured study** of the contract → PBT step with human authors. The industrial data (Hughes: AUTOSAR, Volvo, Dropbox) was **unreachable** here and remains verification debt.

The newest measured evidence is on **LLMs writing property tests from documentation**. Agents do it moderately well:
- Valid and sound in about 2.4 samples; 21% of documented properties covered (2023-era models).
- 42–83% recall of injected bugs, including stateful bugs (2026).
- 56% valid bug reports in the wild.

They also miss properties unless told to test the whole documented spec.

### Cited Findings

**Contract → strategy/property tooling (official docs)**
- **icontract-hypothesis.** README, **B [FT]**. [README](https://raw.githubusercontent.com/mristin/icontract-hypothesis/master/README.rst)
  - "Instead of writing manually the Hypothesis search strategies for a function, icontract-hypothesis infers them based on the function's precondition".
  - Two modes: "only assume" (preconditions become `assume`) and inferred strategies. Also a ghostwriter mode.
  - "Since the contracts live close to the code, evolving the code also automatically evolves the tests."
  - No effectiveness data in the README.
- **CrossHair and deal.** Not fetched in this run. Their contract → test/symbolic checking claims are not evidenced here.

**Hypothesis stateful testing (official docs)**
- **Grade B [FT].** [Hypothesis docs](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- "Hypothesis instead tries to generate not just data but entire tests. You specify a number of primitive actions … and then Hypothesis will try to find sequences of those actions that result in a failure."
- The docs give these building blocks:
  - rules;
  - `precondition` (for when a rule is enabled);
  - `invariant` ("run after every step");
  - `Bundle` (values produced by rules and consumed by later rules, i.e. handed-out objects).
- *Inference:* these map directly onto the brief's normative forms:
  - transition table → rules + preconditions;
  - frame / formula over one instant → `@invariant`;
  - handed-out objects → Bundles;
  - environment actions → extra rules.

**Hughes' industrial reports**
- All [unreachable] in this run; snippets are leads only:
  - "Experiences with QuickCheck: testing the hard stuff and staying sane" (LNCS 9600, 2016);
  - "Testing AUTOSAR software with QuickCheck" (ICSTW 2015);
  - "Mysteries of DropBox" (ICST 2016). The UPenn PDF gave a TLS failure via curl and 503 via fetch.
- The search extract says Dropbox/Drive/ownCloud testing exposed unexpected behaviour "in two out of three". **Do not cite as verified.**
- The Cedar paper [FT] confirms the Dropbox paper's existence and summary ("found several bugs").

**LLM-written PBTs from API docs (Vikram, Lemieux, Sunshine, Padhye)**
- **Source.** "Can Large Language Models Write Good Property-Based Tests?", arXiv 2307.04346 v2 (2024). **Grade A-pre [FT].**
- **Setting.** n = 40 Python library API methods; GPT-4, Gemini-1.5-Pro, Claude-3-Opus; two prompting strategies.
- **What "correct" meant.** Validity (runs without error), soundness (the assertion does not fail on correct code), and *property coverage*: the PBT kills property mutants.
- **Results.**
  - Best setup: a valid and sound PBT "in 2.4 samples on average".
  - The soundness metric agreed with human judgement at precision 100% and recall 97%.
  - The best model (GPT-4) covered **21% of properties extractable from API documentation**.

**Agentic PBT across Python packages (Maaz, DeVoe, Hatfield-Dodds, Carlini)**
- **Source.** "Agentic Property-Based Testing", NeurIPS 2025 workshop. **Grade A-workshop [FT].** [arXiv 2510.09907](https://arxiv.org/abs/2510.09907)
- **Setting.** 100 packages, 933 modules, 984 bug reports. Properties were inferred from **code and documentation**.
- **Validity.**
  - Manual review of n = 50 sampled reports: 56.0% valid bugs (95% CI 42.2–69.8%), 32% worth reporting.
  - Initial inter-rater κ = 0.31.
  - Top-21 by rubric: 86% valid.
- **Cost.**
  - $5,474 total; $5.56 per report, giving $9.93 per valid bug.
  - 8.8 min and about 110 turns per module.
  - 5 bugs reported upstream, 3 patches merged.

**PBT-Bench (Jing, Wang, Zhang, Du)**
- **Source.** arXiv 2605.15229 v4 (Oct 2026). **Grade A-pre [FT, abstract and setup read].**
- **Setting.**
  - 100 problems across 40 Python libraries, with 365 injected semantic bugs that random inputs rarely trigger.
  - Three difficulty levels, L1 to L3; L3 = "stateful, cross-function protocol violations".
  - Agents must write Hypothesis tests from the documentation.
  - 8 LLMs, 3 runs each, plus a frontier model inside a coding agent.
- **Results.**
  - Bug recall under the PBT-guided prompt was 42.1–83.4%.
  - The gain from the PBT prompt ranged from −8 to +42 points and was not monotone in model strength.
  - Under an open-ended prompt the frontier model "stops after exposing a single bug". Framework instructions ("use Hypothesis and test the whole documented specification") account for essentially all of its gain.
  - Some bugs were never found by any model in 2 of 3 runs.
- Round-trip properties account for only 18% of targeted bugs; the rest are structural, conformance, ordering, stateful, model-based and metamorphic.

**Stateful LLM-generated tests specifically (RuleBasedStateMachine)**
- No dedicated evaluation was found (search, Oct 2026). PBT-Bench L3 is the closest.

### Inferences
- For the pipeline, "contract → property test" splits into two parts.
  - **(a) Mechanical:** Dafny or icontract pre/postconditions become a Hypothesis strategy plus an assertion. This is cheap and can be automated. It is spec-enforcing, so it binds the reference model to the clause text.
  - **(b) Property discovery:** an LLM finds properties from prose. Measured agent recall is partial (21% coverage in 2023; 42–83% recall in 2026). Agents also stop early unless instructed to cover the whole spec.
  - So per-clause enumeration ("one test obligation per clause ID") must be imposed by the harness, not left to the agent.
- Agentic PBT that infers properties from code (Maaz) is exactly the mode the brief must avoid for spec-enforcing tests: it is spec-from-code. Feed agents the **clause text and its ID**, never the reference-model source, when generating spec-enforcing properties. *Inference, consistent with §3 SpecGen and ImpossibleBench findings.*
- Mechanical contract → PBT inherits contract weakness: a weak postcondition gives a weak test. Mutation of the reference model (T4) is the check on that.

### Gaps
- Hughes' AUTOSAR/Volvo/Dropbox/LevelDB figures: [unreachable]. Verification debt.
- No measured evaluation of icontract-hypothesis, CrossHair or deal effectiveness was found.
- No study measures LLMs translating *formal contracts* (as opposed to prose docs) into PBTs.

---

## Q3. History checking of concurrent histories on the reference model; environment fault/cancellation actions as generated operations

### Takeaway
- **Porcupine** (re-checked from full text) takes an executable sequential model plus a history. Its speed claims against Knossos are self-reported on Jepsen test data.
- **New independent evidence** (OmniLink, 2026) partly confirms and partly qualifies them:
  - Porcupine is much faster on small or many-thread histories.
  - It is inconsistent beyond about 200k operations, taking minutes to *reject* histories.
- TLA+-based checking of interval histories (OmniLink) now gives a bridge from a TLA+ spec straight to concurrent histories.
- Environment actions as generated operations are well evidenced: P# environment models, Remix/Mocket fault injection, CCF composing fault actions, FoundationDB simulation. Their main cost is modelling the environment, and they find bugs that need concurrency combined with failures.

### Cited Findings

**Porcupine (re-check of a §3 "could not re-check" item)**
- **Sources.** README **B [FT]** ([README](https://raw.githubusercontent.com/anishathalye/porcupine/master/README.md)); author blog **C [FT]** ([blog](https://anishathalye.com/testing-distributed-systems-for-linearizability/)).
- **What it takes.** "A sequential specification as executable Go code, along with a concurrent history". Histories can be operations with call/return times, or call/return events. It includes a visualizer of partial linearizations.
- **Algorithm.** It implements Horn & Kroening's "Faster linearizability checking via P-compositionality", an optimization of Lowe's "Testing for Linearizability".
- **Speed claim.** "Porcupine is generally 1,000x-10,000x faster [than Knossos] … Testing on the data in `test_data/jepsen/`", and "millions of times faster" when P-compositionality applies.
  - This is self-reported and benchmark-specific.
- **Effectiveness claim (blog).** In a hand-mutation experiment on the author's own key-value store, ad-hoc tests caught only egregious bugs, while "I couldn't introduce a single correctness bug that the linearizability test couldn't catch".
  - Anecdotal: n and the bug list are not given. Grade C.
- The blog also restates that linearizability checking is NP-complete.

**OmniLink (new; challenges and refines the §3 cost picture, flagged)**
- **Source.** Hackett, Wrench, Macko, Davis, Wei, Beschastnikh, "Trace Validation of Unmodified Concurrent Systems with OmniLink". **Grade A-pre [FT].** [arXiv 2601.11836](https://arxiv.org/abs/2601.11836)
- **Method.**
  - Events are black boxes with a time interval ("timebox") and a TLA+ meaning.
  - TLC solves for a logical total order, giving linearizability-style checking with a general TLA+ spec, including *non-linearizable* specified behaviours.
- **Comparison with Porcupine.**
  - Setup: a 1:1 translation of the BAT model into Go; traces of 500 to 450k operations; 1–50 threads; 10 repetitions each.
  - "Both tool outputs always agreed with one another."
  - Porcupine "runs significantly faster than OmniLink" for small operation counts, especially with many threads.
  - "Past 200k operations with few threads, however, Porcupine's performance is less consistent … takes a long time – often multiple minutes – to reject traces".
- **Systems validated.** WiredTiger, BAT and ConcurrentQueue. It found injected bugs (many of which the original authors had caught only by inspection) and 2 previously unknown bugs, confirmed.
- **Agents:** human-only.

**Environment and fault actions as generated operations**
- **P# (FAST 2016).** **Grade A [FT].** Environment modelling is "a core activity … required for closing a system"; costs are in the Q1 table.
  - The vNext bug had evaded months of stress testing. P# found it "in a very small setting … witnessed by a full system trace".
- **Remix (EuroSys 2025).** **Grade A [FT].** The next-state relation includes "actions for modeling faults (e.g., a node crash)". The replay coordinator "injects faults (e.g., node crashes) when needed".
  - Experimental configuration: up to 3 crashes and 3 partitions.
- **CCF.** **Grade A/A-pre [FT].** Message loss was not logged. To "account for faults at any step of a behavior, we composed an IsFault action with Trace's next-state relation". See Q4.
- **TraceLink (OOPSLA 2025).** **Grade A [FT].** Found "inaccurate, overly restricted timeout modeling", i.e. timeouts that always or never fire (BUG6, BUG7), and a perfect-failure-detector assumption (BUG8).
  - Environment assumptions in the model are a bug class that conformance checking exposes.
- **Quint Emerald.** **Grade C [FT].** Restart and data-corruption failures were modelled in the spec and replayed during MBT.
- **FoundationDB simulation.** Official docs, **B [FT]**. [FoundationDB docs](https://apple.github.io/foundationdb/testing.html)
  - "Deterministic simulation of an entire FoundationDB cluster within a single-threaded process"; simulates machines, drives (including full disks) and the network.
  - "Tens of thousands of simulations every night"; "roughly one trillion CPU-hours of simulation" (estimate).
  - The SIGMOD 2021 paper itself was not fetched [unreachable in this run].
- **Not fetched:** Jepsen nemesis docs and Coyote (OOPSLA 2020 and related).

### Inferences
- For a **Python reference model** the cheapest history-checking route is a Porcupine-style check. Port the algorithm, or use an existing Python linearizability checker; none was evaluated here.
  - The *sequential* reference model itself serves as the step function.
  - Concurrent histories come from running threads or asyncio tasks against the reference model, or from a Hypothesis-generated interleaving.
- Porcupine-style checking only fits a history predicate that is *linearizability against the sequential model*. Weaker predicates (snapshot isolation, client-centric guarantees) need Elle-style or TLA+-style (OmniLink) checking. §3 baseline; OmniLink adds the TLA+ route.
- Fault and cancellation actions should be **first-class operations in the model's action alphabet**: TLA+ actions, Quint actions, Hypothesis rules. They should not be added in the harness.
  - Then the same generator drives them, and conformance checking flags hidden assumptions such as "timeouts always fire" (TraceLink BUG6/7).
  - The brief's "termination under a stated timeout assumption" form is exactly where TraceLink found undocumented assumptions.

### Gaps
- No measured comparison of Python-side linearizability checkers.
- No full text read for Knossos/Jepsen nemesis, Coyote or the FoundationDB SIGMOD paper.
- No agent/LLM evidence for writing history checkers or nemeses.

---

## Q4. Conformance between layers: differential random testing (Cedar), trace validation (Cirstea et al., CCF, PObserve, TraceLink, Remix), refinement checks

### Takeaway
Two bridge families have strong measured evidence.

**(1) Differential random testing of an executable model against an implementation (Cedar).**
- Cheap once the model is executable.
- Found 21 bugs with property-based testing alongside.
- Misses rare-input bugs and anything outside the generators.

**(2) TLA+ trace validation.**
- Trace-checking with TLC: Cirstea et al., CCF, TraceLink, Remix, OmniLink.
- Found discrepancies "in all cases".
- Costs from about 1 engineer-week (consistency spec, tooling in place) to about 2 engineer-months (first consensus spec, including tool work).
- MongoDB abandoned it after 10 weeks on a large server.
- Its soundness depends on trace detail: imprecise logs can *accept wrong traces*.

Refinement checking (Dafny refinement, FDR, TLA+ refinement mappings) appears only as named future work or as a framing in the sources read. There is no measured bridge evidence for it in this run.

### Cited Findings

**Cedar: differential random testing**
- **Source.** Disselkoen et al., "How We Built Cedar: A Verification-Guided Approach", FSE Companion 2024 (industry). **Grade A [FT].** [arXiv 2407.01688](https://arxiv.org/abs/2407.01688)
- **Correction to the brief.** This paper describes **Lean** models, not Dafny.
  - "We wrote models of the Cedar evaluator, authorizer, and validator in Lean".
  - The brief's "Dafny model vs Rust" is not supported by this paper. *Inference:* the Dafny phase predates this paper; not verified here.
- **Method.**
  - cargo-fuzz generates "millions of inputs" (policies, entities, requests). Lean model and Rust output are compared.
  - Minimized corpora are kept as CI integration tests.
  - Property-based testing covers unmodelled parts (parser) and properties not yet proved.
- **Size and run cost.**
  - The Lean model is "an order of magnitude smaller" than the Rust. Table 1 totals: Lean model 1,673 LOC; Lean proofs 5,714; Rust production 15,693; Rust tests 20,458; Rust other 31,391.
  - Proof-to-model ratio is about 3.4:1.
  - Each target is fuzzed daily for 6 h on 4 vCPU / 8 GB.
  - Median per-call time: Lean 6 µs, Rust 10 µs. Checking all proofs and compiling the models takes about 3 minutes.
- **Results.**
  - 21 bugs from DRT plus PBT. Per-target counts in Table 2 were 6, 0, 4, 6, 2, 0, 3.
  - Proofs found 4 more, including a non-termination bug.
  - One DRT failure (string size: bytes vs codepoints vs graphemes) led to *dropping a language feature*. A model ↔ implementation disagreement surfaced a spec ambiguity.
- **Misses.**
  - DRT "did not discover the non-termination bug … the probability of generating inputs triggering this bug is extremely low".
  - It is "inherently unable to find bugs outside the scope of the test generators" (malformed-policy parser bugs).
  - Generator quality: 35.5% of generated `when` conditions were boolean literals. A new expression generator reduced this to 9.7%.
- **Agents:** human-only evidence.

**Cirstea, Kuppe, Loillier, Merz, "Validating Traces of Distributed Programs Against TLA+ Specifications"**
- **Grade A-pre [FT]**, arXiv 2404.16075 v2 (Sep 2024). The peer-reviewed venue was not verified in this run. [arXiv 2404.16075](https://arxiv.org/abs/2404.16075). This was a §3 "could not re-check" item and is now re-checked.
- **Method.**
  - Trace validation is reduced to constrained model checking with TLC.
  - Traces contain only *updates* to a chosen subset of spec variables and/or events. TLC reconstructs the missing values nondeterministically.
  - Success is checked with the predicate `TraceAccepted = TLCGet("stats").diameter - 1 = Len(Trace)`.
  - On failure there is no counterexample, only a maximal matching prefix, inspected in the TLA+ debugger.
- **Results.**
  - Case studies: two-phase commit, snapshot-isolation KV store, EWD998, two Raft implementations, CCF.
  - "In all cases, trace validation quickly identified executions of the distributed implementations that could not be matched to the high-level specification."
- **Discrepancy classes found:**
  - implementation shortcuts (counter instead of set of RMs, which commits prematurely on resend: "reliably detected");
  - overly strict spec (EWD998 self-message);
  - grain-of-atomicity mismatches, handled with TLA+ action composition A ∘ B and stuttering.
  - EWD998 (about 500 LOC implementation) also revealed a real implementation error. "Thousands of traces have been successfully validated" since.
- **Trace detail versus cost (Fig. 5, 1 h timeout).**
  - Logging all variables plus events with arguments (VEA) explores about trace-length states. Examples: 2PC with 16 RMs, 35 states; KV store, up to 310 states.
  - Logging only event names (E) explodes to ∞ for most instances.
  - Well-chosen partial information suffices: events with arguments for the KV store; TM events only for 2PC.
- **Soundness warning, verbatim:** "too imprecise logs may even lead to erroneous traces being accepted because the model checker may be able to infer suitable values that do not correspond to the actual ones."
- **Effort.** Engineers "found it quite straightforward to instrument existing code"; "writing the trace specification is generally systematic and straightforward". This is anecdotal: the authors say "we only have anecdotal evidence".
- **Adoption.** "Trace validation is now part of CCF's continuous integration pipeline", and also used by etcd.
- **Agents:** human-only.

**CCF: "Smart Casual Verification of the Confidential Consortium Framework"**
- **Source.** Howard, Kuppe, Ashton, Chamayou, Crooks; arXiv 2406.17455 v2. Published 2025: TraceLink cites it as "Howard et al. 2025"; I did not verify the NSDI venue. **Grade A/A-pre [FT].**
- **Setting.** 63 kLoC C++ implementation. Specs are TLA+, tied to code by trace validation in CI.
- **Results.** Six bugs (5 safety, 1 liveness) found across model checking, simulation and trace validation, before production.
  - Trace validation itself found "Commit advance on AE-NACK" (safety).
  - The spec revision it forced exposed "Premature node retirement" (liveness).
  - It also showed that an earlier fix, which passed all tests, broke an implicit property.
- **Cost.**
  - Logging plus test-driver changes took about 1 day.
  - The first consensus Trace spec took about **2 engineer-months over 4 months**. This includes building TLC support (action composition, DFS, debugger, state-graph visualisation) and diagnosing whether the spec or the code was wrong.
  - The 400 LoC Trace spec itself was "a minor task". There were 88 commits to the Trace spec and 107 to the consensus spec.
  - The later consistency spec took **about 1 engineer-week over 2 weeks**. It was done mostly by CCF engineers, with no code instrumentation: state was observed via the REST API.
- **Scale (Table 1).** Consensus: spec 1,134 LoC, trace validation 369 LoC, implementation 2,174 LoC (consensus portion). Consistency: spec 375 LoC, trace validation 111 LoC.
- **Scalability.** DFS made trace validation "orders of magnitude faster". For the consistency spec, validation took under 1 s with DFS versus about 1 h with BFS.
- **Agents:** human-only.

**TraceLink: Hackett & Beschastnikh, "TraceLinking Implementations with Their Verified Designs"**
- **Grade A [FT]**, PACMPL 9 (OOPSLA2), 2025. [PDF](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf). This was a §3 "could not re-check" item and is now re-checked.
- **Method.**
  - Fully automated trace validation for systems compiled by PGo from Modular PlusCal to TLA+ and Go.
  - Vector-clock instrumentation is added automatically.
  - Tracing-spec templates keep the TLA+ small.
  - A "sidestep" path strategy finds bugs at shallower depth.
- **Results.**
  - Systems: dqueue, locksvc, raftkvs (990 MPCal LOC; traces of 2,772 to 100,644 events; up to 26 nodes).
  - **9 previously undetected bugs**: network assumptions (2), 1 PGo miscompilation (`@@` arguments swapped, which passed end-to-end tests), instrumentation bugs (2), timeout-model bugs (2), failure-detector assumption (1), symbolic abstraction (1).
  - "Fixing those inaccuracies did not change the outcome of model checking the specification". The found bugs were model ↔ implementation drift and environment assumptions, not protocol bugs.
- **Limitation.** Tied to PGo/MPCal. OmniLink describes it as needing "invasive vector clock instrumentation".
- **Agents:** human-only.

**Remix conformance (EuroSys 2025)**
- Model → code replay, with discrepancies found. It is explicitly **unsound** and safety-only. Refinement checking with abstraction mapping is named as future work. See Q1. **A [FT].**

**MongoDB model-based trace-checking (MBTC), negative result**
- **Grade A [FT].**
- RaftMongo.tla against the MongoDB server, following Pressler's method (Trace.tla plus TLC).
  - Built by 2 engineers in 10 weeks: 570 LOC C++ tracing, 252 LOC TLA+, 484 LOC Python post-processing.
  - Applied to 5 handwritten tests and 1 randomized test. Only 1 passed; 4 violated the spec due to 2 implementation discrepancies.
  - "The effort to implement MBTC proved so costly, we abandoned the project after 10 weeks".
- **Causes.** Lack of close correspondence, intra-process locking and visibility, incomplete TLC support.
  - "No initial infrastructure investment can make the marginal cost of trace-checking additional specifications cheap."
  - "Bugs in post-processing could mask implementation bugs."
  - Workarounds were often to "avoid the non-conforming behavior" or "simulate a conformant behavior" rather than fix either side.
- Cirstea et al. [FT] attribute MongoDB's difficulty to not using TLA+ nondeterminism for missing state and not using action composition. This is their interpretation, not a re-run.

**PObserve**
- A log-based monitoring bridge, P spec ↔ implementation logs. No measured data. **B [FT].** See Q1.

**OmniLink**
- An interval-history bridge, TLA+ ↔ unmodified concurrent implementation. **A-pre [FT].** See Q3.

**Refinement checks (Dafny refinement modules, TLA+ refinement mappings, FDR)**
- No full-text evidence was gathered in this run.
- What the sources read say:
  - Cirstea et al. note that Pressler formalised trace validation "as a refinement check".
  - MongoDB suggests a refinement mapping to a lower-level spec "might" have resolved discrepancies.
  - Remix names refinement checking with abstraction mapping as future work.
  - Konnov's 2026 slides (C [FT]) state the conformance obligation both ways: "If the spec. executes action A, then impl. must be able to execute A; if the impl. executes action A, then spec. must be able to execute A". Reachability: impl state s implies the spec reaches α(s).

### Inferences
- **Which pairs need a bridge.** Three layers (prose-derived Markdown spec S, formal models F, Python reference model R) give three pairs.
  - **F ↔ R** is the pair with measured, mechanisable bridges: DRT, model-driven replay (MBTCG/Mocket/Quint Connect), trace validation.
  - **S ↔ F** and **S ↔ R** have no mechanical bridge in the sources. They need clause-ID traceability plus T1/T3b methods.
  - The Cedar string-size case shows that F ↔ R disagreement often surfaces an S-level ambiguity. A failing bridge should therefore route back to the clause, not be "fixed" in whichever layer is easier. This is the same risk MongoDB describes as working around violations. *Inference.*
- **Direction matters.**
  - Model → implementation replay (Mocket, Remix, MBTCG, Quint Connect) checks "everything the model does, R can do and agrees on". It misses R behaviour outside the model.
  - Implementation → model trace validation (Cirstea, CCF, TraceLink) checks "everything R did, the model allows". It misses model behaviour R never exercised, and it can falsely accept with imprecise logs.
  - DRT on a deterministic function checks output equality on generated inputs.
  - A complete bridge needs both directions, as Konnov states. In practice: replay plus trace validation, or DRT plus coverage measurement.
- **R is deterministic and small.**
  - Full-state logging (VEA in Cirstea's Fig. 5) is affordable, which removes both the state explosion and the false-acceptance risk of partial logs.
  - That makes trace validation of R against TLA+ much cheaper than in CCF or MongoDB. The order of magnitude would be CCF's consistency-spec case (about 1 engineer-week) rather than its consensus case. *Inference, not measured.*

### Gaps
- No measured evaluation of Dafny refinement, FDR or TLA+ refinement mappings used as a model ↔ reference-model bridge was retrieved.
- Cirstea et al.'s peer-reviewed venue was not verified.
- No PObserve data.
- ShardStore was not re-read (§3 baseline; allowed only "as needed").

---

## Q5. Which layer pairs need a bridge, and which bridge is cheapest for which normative form (brief §2)

### Takeaway
The cheapest bridge depends on the form.
- **Finite and value-domain forms** (formula, case table, frame, failure tables): DRT or contract → PBT on R against an executable model or contract.
- **Sequence forms** (transition table, environment actions): model-generated action sequences replayed on R with state comparison, or a Hypothesis state machine derived from the same transition table.
- **History predicates:** a history checker over R's concurrent histories, Porcupine-style or OmniLink/TLA+-style.

Non-promise registers and variation points need oracle work (T3b) rather than a bridge. Everything below is a synthesis: *Inference*, grounded in the cited cases.

### Cited Findings (anchors for the mapping)
- Finite-input deterministic functions: model-generated exhaustive tests reach 100% branch coverage at about 1 engineer-month. — [Davis et al. PVLDB 2020](https://arxiv.org/abs/2006.00915)
- Deterministic evaluator/authorizer: DRT with type-directed generators, daily 6 h per target, 21 bugs (with PBT). Generator bias (35.5% trivial conditions) and rare inputs are the failure modes. — [Cedar FSE'24](https://arxiv.org/abs/2407.01688)
- Action sequences with expected states after each action. Mapping cost about 134–152 LOC of annotations per system. — [Mocket EuroSys'23](https://gaoyu-cn.github.io/paper/2023-eurosys-mocket.pdf)
- Fault actions inside the model's action set, injected by the replay coordinator. — [Remix EuroSys'25](https://arxiv.org/abs/2409.14301); CCF `IsFault` composition — [CCF](https://arxiv.org/abs/2406.17455)
- Timeout and failure-detector assumptions exposed by conformance checking. — [TraceLink OOPSLA'25](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf)
- Interval-operation histories against an executable sequential model (Porcupine), or against a TLA+ spec (OmniLink). — [Porcupine README](https://raw.githubusercontent.com/anishathalye/porcupine/master/README.md); [OmniLink](https://arxiv.org/abs/2601.11836)
- Hypothesis primitives: rules, preconditions, invariants after every step, Bundles. — [Hypothesis stateful docs](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- Precondition → generation strategy. — [icontract-hypothesis](https://raw.githubusercontent.com/mristin/icontract-hypothesis/master/README.rst)

### Inferences
Bridge map. Pair notation: S = Markdown spec, D = Dafny, T = TLA+, A = Alloy/Lean, R = Python reference model.

| Normative form | Pairs needing a bridge | Cheapest evidenced bridge | Cost driver | Main miss |
|---|---|---|---|---|
| Formula over one instant | D/S ↔ R | D contract → Hypothesis property (pre as strategy or `assume`, post as assert). Also `@invariant` in the R state machine | Generator quality (Cedar 35.5% trivial inputs) | Rare inputs (Cedar non-termination); weak postconditions |
| Case table (complete, disjoint) | S ↔ R, D ↔ R | Exhaustive or pairwise enumeration of table rows as parametrized tests (MBTCG style: enumerate everything when small). DRT if D is executable (compile Dafny to Python) | Number of rows | Rows the table itself lacks (T1/T2 job) |
| Frame (unchanged set) | D ↔ R | Postcondition `old(x) == x` for the frame, as a property over a full-state snapshot of R before and after | Needs observable full state of R (an abstraction function, as in Quint Connect `State::from_driver`) | Hidden state not in the abstraction |
| Termination under timeout assumption | T ↔ R | Model-driven replay with timeouts as explicit actions; trace validation exposes "timeouts always/never fire" assumptions (TraceLink BUG6/7) | Representing time; bounded liveness only | Liveness: Remix and TraceLink check safety only; DRT missed non-termination (Cedar) |
| State × operation transition table | T/S ↔ R | Model-generated action sequences with expected state per step (Mocket/Quint Connect pattern), or a Hypothesis `RuleBasedStateMachine` generated from the table (rules = operations, preconditions = enabled cells, Bundles = handed-out objects) | Action ↔ method mapping (about 150 LOC in Mocket) | Behaviour of R outside the model; add trace validation for the reverse direction |
| Environment actions (concurrent caller, out-of-band actor, faults, cancellation) | T ↔ R | Faults and cancellation as model actions that the generator emits and the R harness performs (Remix coordinator, CCF IsFault, Quint Emerald failures, P# environment machines) | Modelling the environment (P#: 2 person-weeks to 5 person-months) | Faults not in the action alphabet |
| History predicate over interval operations | T ↔ R | Run R concurrently, record call/return intervals; check with a Porcupine-style checker using R's sequential mode as the model, or with OmniLink-style TLA+ for weaker predicates | NP-complete check; Porcupine slows past about 200k operations with few threads (OmniLink) | Only histories actually generated |
| Failure category / phase / effect / retry tables | S/D ↔ R | Case-table bridge plus fault actions; assert category and effect per row | Fault injection points in R | Interaction of retries with concurrency (needs the history bridge) |
| Register of non-promises | S ↔ R | No positive bridge; enforcement is "test must not assert X". T3b covers oracles. A mutant R that varies the non-promised behaviour should *not* be killed (see the §3 seed) | — | Over-strict tests, the ImpossibleBench risk in §3 |
| Variation points (normal value plus declared deviations) | S ↔ R(profile) | One parametrized suite over profile values; DRT between R-profile variants on the shared core | Profile count | Undeclared deviations |

Cross-cutting points:
- **The bridge with the best evidence per unit cost for this pipeline: the F → R replay with state comparison.** Its supports:
  - MongoDB MBTCG: 1 engineer-month, 100% branch coverage.
  - Mocket: a few hundred LOC of mapping.
  - Quint Connect: agent-written drivers, C-grade evidence.
  - DRT complements it (Cedar).
- **The reverse direction** (trace validation of R's traces against T) is cheap only because R is deterministic and fully observable. It is the guard against R doing things T forbids.
- **Required abstraction function.** R must expose an abstraction function `alpha(R_state) → spec_state`. Every bridge in the table uses it: Quint Connect `State`, Mocket annotations, Cirstea trace variables.
  - Making `alpha` a reviewed, versioned artefact is the single cheapest structural decision.
  - It is also where agents are likely to cut corners. Konnov's harness lesson: "do not trust the generated harness – TODOs and bugs inside".

### Gaps
- No source measures bridge cost per normative form directly. The mapping is synthesised from per-system figures.
- No evidence was found for Alloy/Lean ↔ Python bridges. Cedar's Lean ↔ Rust DRT is the nearest analogue.

---

## Q6. Were agents/LLMs measured generating such tests or bridges? (per method)

### Takeaway
Agents have been measured on three steps:
- writing property tests from documentation (moderate recall; needs whole-spec instructions);
- writing TLA+ models checked by trace-validation conformance (weak for complex systems);
- writing MBT/test harnesses against a human or AI spec (works, but harness bugs and corner-cutting need human review; effort weeks, not hours).

No agent evidence was found for DRT setup, Dafny test generation, history checkers, or trace-validation specs written by agents for an existing model.

### Cited Findings
- **Docs → Hypothesis PBTs.**
  - n = 40 API methods. Valid and sound in about 2.4 samples. 21% property coverage (best: GPT-4). — [Vikram et al., A-pre](https://arxiv.org/abs/2307.04346)
  - n = 100 problems / 365 injected bugs. Recall 42.1–83.4% with a PBT-guided prompt. The open-ended prompt makes a frontier model stop after one bug. — [PBT-Bench, A-pre](https://arxiv.org/abs/2605.15229)
  - Properties inferred from code and docs. n = 50 sampled reports: 56% valid. $9.93 per valid bug. — [Maaz et al., A-workshop](https://arxiv.org/abs/2510.09907)
- **AI-generated TLA+ models with conformance by trace validation: SysMoBench.** **A-pre [FT]**, arXiv 2509.23130 v3. [arXiv 2509.23130](https://arxiv.org/abs/2509.23130)
  - **Setting.** 11 system artefacts; agents powered by Claude-Sonnet-4, GPT-5, Gemini-2.5-Pro, DeepSeek-R1; 5 runs each, best output kept; up to 3 repair iterations.
  - **Results** (my parse of the Table 3 text extraction):
    - Asterinas spinlock: conformance 80–100% across models.
    - Etcd Raft, basic-modelling agent: only one model passed syntax and runtime checks (runtime 25%), and its conformance score was 7.69%.
    - Etcd Raft, code-translation agent: best conformance 15.38%.
  - Authors: "few AI-generated models achieved fine-grained conformance".
  - **LLM in the bridge itself.** An LLM was used to map model names to code and log names to build the trace-validation harness. The authors "inspected the LLM-assisted mapping … and found the results to be correct". Their gold-model renaming test (10 variants) scored perfectly.
  - Adding a system costs about 4 person-days, mostly "instrumenting the system to collect execution logs".
- **AI-written test harnesses linking TLA+/Apalache to real implementations.** Konnov, TLA+ Community Meeting, Apr 2026. **C [FT]**: slides; n = 2; author self-report. [Slides](https://conf.tlapl.us/2026-etaps/konnov-2026.pdf)
  - **TFTP.** Human-written spec (about 13 h); harness written by Copilot + Sonnet 4.5.
    - About 1 week and about 200 premium requests debugging the harness. 15+ listed fixes.
    - Total effort 2 weeks; 2 implementation bugs found.
    - Lessons: "Surprisingly, it works – not effortlessly though"; "Do not trust the generated harness – TODOs and bugs inside"; "Do not let an LLM define its own formats"; define your own structured log format.
  - **ZooKeeper.** AI wrote both spec and harness: "5 protocols + harness after 1 week"; "~1 month, no impl. bugs so far"; "Sometimes, AI tools cut corners badly"; "Human review & guidance needed".
- **AI-written Quint spec (from code) plus MBT driver.** n = 1 (Emerald). About 80% coverage, one memory leak. — [Quint blog, C](https://quint-lang.org/posts/quint_connect_emerald)
- **NL → TLA+ synthesis.** 30 LLMs, 205 specs. Up to 26.6% syntactic and 8.6% semantic correctness (TLC-validated). — [Bisharat et al., arXiv 2606.05792, A-pre, abstract only read](https://arxiv.org/abs/2606.05792)
  - Consistent with the §3 baseline ("LLM-written system-level TLA+ is weak"). Not a challenge.

**Per-method agent status**

| Method | Agent status |
|---|---|
| MBTCG (TLA+ → tests) | Human-only (MongoDB, Mocket) |
| Remix | Human-only |
| Quint Connect | Agent, C-grade, n = 1 |
| Apalache harness | Agent, C-grade, n = 2 |
| Dafny DTest | None |
| P#/PObserve | Human-only / none |
| Contract → PBT (icontract-hypothesis, etc.) | No agent study of the *contract-to-test* step found |
| Docs → PBT | Measured (above) |
| Stateful PBT | Partially, inside PBT-Bench L3 only |
| History checking (Porcupine, OmniLink) | Human-only |
| Environment / fault generation | Human-only, except Quint Emerald failures (C) |
| DRT (Cedar) | Human-only |
| Trace validation (Cirstea, CCF, TraceLink) | Human-only. LLM-assisted mapping in SysMoBench was measured as reliable on its benchmark |
| Refinement checks | No evidence |

### Inferences
- The measured agent weak spot is not the glue code but **coverage of the spec**: 21% property coverage; stopping after one bug; low conformance on complex models.
- The measured remedies are structural:
  - explicit instruction to "test the whole documented specification" (PBT-Bench ablation);
  - human-defined formats and logs (Konnov);
  - a fixed mapping or abstraction function (SysMoBench).
- For the pipeline, *Inference*:
  - Agents can write F → R drivers and contract → PBT translations, provided the clause list, the action alphabet, the `alpha` function and the log format are fixed beforehand and machine-checked.
  - Every generated harness needs a mutation check (T4) because of the reported "TODOs and bugs inside" and "cut corners".
- Specs derived from code, as in Emerald and SysMoBench's code-translation agent (which did better on conformance), score well on conformance *by construction*. That is the SpecGen confirmation effect from §3.
  - In this pipeline the formal models must come from S, not from R. Otherwise a high F ↔ R conformance score is uninformative.
  - SysMoBench's code-translation agent outperforming the basic modelling agent on Etcd Raft fits this pattern.

### Gaps
- No controlled study compares agent-written versus human-written MBT drivers or trace-validation specs on the same system.
- No agent study of DRT generator construction, history-checker models, or Dafny-contract → Hypothesis translation.
- Konnov's and Quint's reports are self-reports with n ≤ 2 and no baselines.
