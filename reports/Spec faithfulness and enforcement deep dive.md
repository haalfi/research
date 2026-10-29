# Validate the validators before they gate (deep dive)

This deep dive closes five gaps that the verified edition (`reports/Spec faithfulness and enforcement verified.md`) left open. Where the verified edition and the earlier report differ, it builds on the verified edition. It does not re-survey what those reports settle. The inputs are five track notes in `research_notes/Spec faithfulness and enforcement deep dive/`: D1 examples-first, D2 abstraction function, D3 Python and single source, D4 consistency with environment actions, D5 expectation independence. IDs such as "D4 Q3.1" or "D1-R1" point to sections and recommendations in those notes. **Own-trial results are this run's small toy experiments, not published evidence.** They are labelled "own trial" wherever they appear.

---

## §1 Kernsatz

Spec-blind record checks should not gate anything until they have been screened against **several deliberately different correct Python reference models ("wheats")**. In the only line that measures this, one group's education studies on deterministic functions (A, tool authors, *analogous*), suites screened against a single correct implementation were trusted 28–94 % of the time, against 0–81 % with adversarial wheats. Cunha & Macedo's 90 % also presupposes a hidden correct oracle, and nobody has yet replicated their study for temporal or API behaviour.

The ∀-environment-move check has a better gate: a per-operation, one-step response-existence query relative to an inductive invariant (Event-B feasibility and deadlock obligations, AGREE viability; A, tool authors, *analogous*; own Z3 trial: 40 operations × 46 clauses in 1.3 s). It stays local despite mode variables. rt-consistency as implemented has no input/output split and should be relabelled a timing check.

Medium-to-low confidence, mostly *Inference* from analogues, supports four further points:
- Split `alpha` into a small reviewed observation relation and a checked projection. No source counts `alpha` bugs.
- Pipeline A is feasible today in pure Python, with Hypothesis stateful tests and CrossHair as an advisory probe only. A literal single Python source exists only via Dafny plus a back-end check.
- A fresh, record-only session measurably improves tests written against faulty *code* (+11.7 %, one A-pre study).
- Common-mode error from spec to test is still unmeasured.

---

## §2 Findings per track

**Conventions.** Grades are A / A-pre / A-workshop / B / C / D. **[unreachable]** means the full text was not fetched. *Inference* marks reasoning that is no source's finding.

Each evidence cell gives the grade, full text read (**FT** y/n/partial), n and setting, and what "correct" meant.

Transfer labels:
- *direct*: library or API behaviour specs;
- *analogous*: other spec domains;
- *inference*.

Independence flags:
- **TA**: tool or method authors evaluating their own tool;
- **V**: vendor;
- **CB**: competing tool or benchmark;
- **ind**: independent.

"Agents" states whether LLMs or agents were measured on the step.

### 2.1 D1 Examples-first validation against correct ("wheat") and wrong ("chaff") implementations

**Finding.** Wheat/chaff checking splits check-set quality into two parts:
- **validity**: the suite accepts every wheat, so every allowed variant;
- **thoroughness**: the suite rejects each chaff, where a chaff encodes a *conceptual misreading*.

This is exactly the verified edition's allowed-variant and forbidden-variant pair. The best-measured result is the danger of **a single wheat**. Tests that over-fit one correct implementation pass it and are wrongly trusted ([ICER 2018](https://cs.brown.edu/~sk/Publications/Papers/Published/wkf-who-tests-testers/paper.pdf)). Almost all of this evidence comes from one group, Brown PLT, evaluating its own tools on deterministic, side-effect-free student assignments.

| Option | Evidence (grade; FT; n, setting; "correct") | Catches | Misses | Cost | Agents | Transfer |
|---|---|---|---|---|---|---|
| **Single-wheat screening** (one correct reference) | Cunha & Macedo's "Valid" metric adds "the oracle specification as a fact to the model" before scoring tests ([FM 2026, arXiv 2510.23350 v2 §4](https://arxiv.org/abs/2510.23350); A; FT y for these passages). Forge "supplied only one wheat because … models are not overconstrained by implementation details" ([Forge OOPSLA 2024](https://cs.brown.edu/~sk/Publications/Papers/Published/ngp----forge/paper.pdf); A; FT y testing/evaluation sections; 92 + 64 students; TA) | Tests contradicting the one correct reading | Over-zealous tests that happen to match the one wheat | One reference | Cunha & Macedo: yes (GPT-5 etc.); Forge: human-only | analogous |
| **Multiple adversarial wheats** | ICER 2018 (A; FT y; 4 assignments, 38–91 students each; correct = reconciled Axm/AlgMult labelling; TA). Share of student suites trusted, single wheat → multiple wheats: DocDiff 90→81 %, Nile 28→0 %, Filesystem 94→71 %, MapReduce 79→35 %. Two to seven adversarial wheats per assignment. Wheats should "reflect different scenarios allowed by the specification". ICER 2019 (A; FT y): "If the problem specification leaves any behavior underspecified, it is necessary to run suites against multiple correct implementations" ([ICER 2019](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-examplar/paper.pdf)) | Over-strict tests asserting unspecified behaviour | Validity is guaranteed only if wheats "completely exercise" the underspecified space; no study says how many suffice | 2–7 wheats per assignment, "potentially time-consuming" | Human-only | analogous |
| **Examples-first tool with wheat/chaff feedback (Examplar)** | ICER 2019 (A; FT y; 2018 cohort, n = 269 final suites, vs 2017, n = 320; cross-year, not randomised; TA). Invalid final suites fell from 30.3 % to 6.7 % (χ² = 52.373, p < 0.01). Thoroughness held (89.2 % vs 91.0 %). Implementation correctness was inconclusive (p = 0.086). Building wheats early "uncovered major issues in four assignments" before release. Koli 2020 (A, short; FT y; ~59–64 students; no control): 51.64 % of 703 run sequences clicked "Begin Implementation" before the first run ([Koli 2020](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-stud-write-test-no-coercion/paper.pdf)) | Invalid (over-strict) examples, early | Implementation time possibly diverted (FileSystem "declined precipitously", confounded) | Low per run; curation high | Human-only | analogous |
| **Conceptual chaffs; chaffs mined from wheat failures** | Making Hay (A; FT y, figures from a garbled extraction; 2 problems + 1 Forge problem; TA). About 30 % of wheat failures are good-faith misunderstandings. Classsourcing found 17 (Nile) and 11 (DocDiff) potential misconceptions; "The experts (course staff) missed most of these". Fig. 2: classsourced-only 16/9, both 1/2, expert-only 6/3. One Forge chaff rejected valid instances ([Koli 2022](https://cs.brown.edu/~sk/Publications/Papers/Published/pgnwk-making-hay-wheats/paper.pdf)). Programming 2024 (A; FT y method/cost/evaluation; 3 assignments × 3 semesters; TA): 277 of >4,000 wheat failures took "one month of work from two experts"; ~70 % were typos or noise. LLMs and synthesis were explicitly not tried ([source](https://cs.brown.edu/~sk/Publications/Papers/Published/pgnk-conceptual-examplar/paper.pdf)) | Misreadings that occur in practice; chaffs nobody anticipated | Expert-designed chaffs predicting misconceptions that never occur; buggy chaffs | One expert-month per 277 failures | Not used | analogous |
| **Candidate differencing: distinguishing scenarios classified by users** | PICK, ECOOP 2026 (A; FT y; Prolific, 50 per condition; regex, ABAC, LTL; correct = matches ground truth; historical, non-randomised control for LTL; TA). Novices classifying LTL traces scored 56.0 % (84/150) vs 43.3 % and 44.0 % in two earlier formula-writing studies. Voting threshold 2 cut over-elimination by 27 % on average ([PICK](https://www.siddharthaprasad.com/papers/pafk-pick.pdf)). Narrowing, arXiv 2511.19177 (A-pre; FT y; 28 Alloy4Fun requirements; TA): median 14 tests to narrow 28 candidates; no temporal support. On their own LLM tests the authors say they are "a weak characterization of the requirement" ([source](https://arxiv.org/abs/2511.19177)). QSM 2008 (A; FT partial; 3 textbook RE cases, simulated oracle; TA): rejected scenario queries outnumber accepted ones ([source](https://webperso.info.ucl.ac.be/~pdupont/pdupont/pdf/QSM_AAI_08.pdf)). Trace matching is easier than formula writing even for experts ([Greenman FM 2024](https://cs.brown.edu/~sk/Publications/Papers/Published/gpdzdkmnz-miscon-finite-infinite-ltl/paper.pdf); A; FT partial) | Temporal misreadings, shown as one classifiable trace | Readings absent from the candidate set | Several candidates plus a differencing engine | PICK: LLM candidates for regex/ABAC; LTL candidates human-sourced | analogous |
| **Oracle-derived mutant-killing tests on real faulty *temporal* specs** | μAlloyτ, MODELS 2023 (A; FT y evaluation; Trash + Train, 3,669 submissions, 37 exercises; correct = differs from the Alloy4Fun oracle; TA, different group). Detects 90.8 % pooled (87.24 % mean per exercise) with on average 67.3 tests per exercise (26.65 Trash, 115.12 Train) in 40.7 s. "These test cases do [need] a human to provide the oracle" ([source](https://scopelabuta.github.io/files/Models2023-B.pdf)) | Real temporal model faults | Spec-derived, not spec-blind; expert faults may differ | ~67 tests per exercise | None | analogous |
| **Relational predicates instead of concrete expected outputs** | Wrenn, Nelson & Krishnamurthi, Programming 5(3) (A; FT partial; TA): `is-valid` predicates for problems with multiple valid outputs; Toposortacle 46 % perfect ([source](https://cs.brown.edu/~sk/Publications/Papers/Published/wnk-use-rel-prob-pbt/paper.pdf)). Follow-up (A; FT partial; TA): Hypothesis- and SAT-based generators found different errors, and manual suites found errors both missed ([source](https://cs.brown.edu/~sk/Publications/Papers/Published/nrsdwk-auto-targ-test-pbt-pred/paper.pdf)) | Oracles for semi-specified outputs | — | Low | Human-only | analogous |
| **LLM-generated chaffs** | Leinonen et al. (A-pre; FT partial): GPT-4o buggy submissions match real failure *distributions* (8,598 real submissions) ([source](https://arxiv.org/abs/2411.10455)) | — | Matches failure distributions, not misconceptions | Low | Yes | inference |

**Behaviour transfer.** Several limits apply.
- Examplar requires a binary correctness property. Nondeterminism must be realised as "multiple wheats that differ in their behavior, but are individually deterministic", otherwise feedback is flaky ([ICER 2019 §9](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-examplar/paper.pdf)).
- The Koli 2021 problems "do not involve state or other side-effects" ([source](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-examplar-unspecified/paper.pdf); A; FT y; TA). In that study, 16 of 23 TweeSearch posts reported testing every ordering of a semi-specified output, "all of which were (correctly) rejected as invalid".
- Temporal Forge has no `example` ([docs](https://forge-fm.github.io/forge-documentation/latest/testing-chapter/testing/), C).
- **No source measures examples-first validation of a stateful or concurrent API spec** (D1 Q3).

**Replication of Cunha & Macedo (D1 Q4).** None exists as of 2026-10-29. The authors list behavioural requirements as future work ("We also plan to evaluate the effectiveness of this approach … requirements to be specified with temporal logic"), and their narrowing prototype excludes Alloy 6 temporal logic. The nearest behavioural equivalents differ in kind. μAlloyτ is spec-derived. PICK classifies traces rather than writing spec-blind tests. QSM uses a simulated oracle. *Inference*: the public Trash/Train temporal datasets make a direct replication cheap (D1-R6). This is a **single-source sub-question**: only Cunha & Macedo measure spec-blind NL → test generation against wrong specs.

**Rejected alternatives as negatives (D1 Q5).** No study derives negative tests from ADRs, design rationale or decision records. Misuse-case test studies were found as listings only and not read. The nearest analogues all use *plausible alternative readings* as negatives:
- conceptual chaffs ("should exercise logical misunderstandings");
- PICK and narrowing candidates;
- QSM negative scenarios.

*Inference* from Making Hay: a documented rejected option is an *expert-designed chaff*. It covers anticipated misreadings, misses ones that only show up in practice, and is sometimes never triggered. Rejected-option negatives therefore complement negatives mined from check failures; they do not replace them.

**Baseline handling (quoted verbatim from the verified edition, then qualified; none challenged).**
- §2.1 table: "From NL + Alloy domain model, without the spec, GPT-5 (few-shot) writes N positive and N negative instances. … "Detected" = at least one of the 2N tests gives an unexpected result. Mean per-requirement detection: … 90 % (N=3) …, counted only over requirements with complete valid suites". **Qualified.** The validity of those suites was established against the hidden oracle, which acts as a single wheat (*Inference*, D1 Q1). A real pipeline has no oracle, so it needs a wheat substitute.
- Pipeline A failure modes: "About 4 % wrong generated tests, mostly negatives, concentrated on ambiguous requirements (Cunha & Macedo: 30/774; 13 of 14 oracle errors negatives)." **Qualified** (*Inference*). The 4 % is measured against one oracle. Where records leave behaviour open, a single-wheat screen lets over-strict checks through (ICER 2018). The over-strict share for an API with allowed variants is therefore **not bounded by 4 %**.
- §2.1 check 4: "Non-commitment typing: an *unspecified* set needs one positive per allowed outcome and a negative outside the set. A *deliberately not promised* item needs two witnesses with different outcomes." **Supported and qualified.** Two witnesses with different outcomes is what multiple wheats implement, and ICER 2018 measures the benefit. "One positive per allowed outcome" works **against the spec** as a satisfiability check. It does not work as concrete expected values against a deterministic R, which realises only one outcome (TweeSearch). Against R, such positives must be membership predicates, and R variants must realise the other outcomes (D1-R2).
- Part 3: "R2 | Use rejected options as negatives | inference (no source does this) | low". **Confirmed** as unsourced. A chaff-design rationale and an operational overturn test are added (D1-R3).

**Disconfirming search §4(a): examples-first validation fails or costs too much for behaviour specs.** *Result: no refutation, because no measurement exists in either direction. The search did find cost and fragility risks.*
- Curation is expensive: one expert-month per 277 failures, about 70 % noise, two to seven wheats per assignment.
- Wheats themselves can be over-strict. A Forge wheat was "arguably over-constrained", and the authors conclude "It is also vital that a wheat not over-constrain" ([OOPSLA 2024 §7.3](https://cs.brown.edu/~sk/Publications/Papers/Published/ngp----forge/paper.pdf)).
- Chaffs can be buggy (Making Hay).
- Users misattribute invalidity on semi-specified outputs (Koli 2021).
- Temporal tooling is missing (Temporal Forge has no `example`).
- Temporal accuracy stays modest even with tool support: PICK LTL reached 56 %.
- Gaming risk: Examplar hides wheat outputs because a student "may be overly tempted to intentionally write failing assertions to discover what the behavior of wheats is". *Inference*: an agent that can query R can do the same unless information flow is restricted (§2.5).
- *Inference*: the cost scales with the allowed-variant space and the misreading space. Both are larger for APIs with orderings, error choices and interleavings.

### 2.2 D2 The abstraction function between reference model and spec

**Finding.** Practice never trusts `alpha` *because it was reviewed*. It separates two roles.
- **Proof-based systems** make `alpha` untrusted, because the proof checks it. They trust a small reviewed relation over externally visible state: IronFleet's `SpecRelation` "should only talk about the externally visible behavior"; Armada's refinement relation R.
- **Test-based systems** compare outputs after each operation, plus a narrow projection. ShardStore uses "same key-value mapping"; Cedar uses output parity. There `alpha` is harness code, checked only by the discrepancies it produces.

**No source counts how often `alpha` itself was wrong.**

| Option | Evidence (grade; FT; n, setting; "correct") | Catches | Misses | Cost | Agents | Transfer |
|---|---|---|---|---|---|---|
| **Proof-checked refinement function + small trusted observation relation** | IronFleet SOSP 2015 (A; FT y; IronRSL, IronKV, ~3.7 person-years; machine-checked refinement; TA). Trusted spec 85 and 34 SLOC, "easy to inspect". A generic library proves concrete map/sequence operations refine abstract ones given an injective key mapping ([source](https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf)). Armada PLDI 2020 (A; FT partial): R is a relation, e.g. "the log in the implementation is a prefix of that in the spec" ([source](https://www.andrew.cmu.edu/user/bparno/papers/armada.pdf)). Verdi's TCB contains no abstraction function ([source](https://homes.cs.washington.edu/~ztatlock/pubs/verdi-wilcox-pldi15.pdf); A; FT TCB passage). seL4: invariant proofs dominated effort over correspondence proofs ([TOCS 2014](https://trustworthy.systems/publications/nicta_full_text/7371.pdf); A; FT relevant sections) | A wrong mapping blocks the proof | False passes from the trusted parts (spec, environment) | Person-years | Human-only | analogous |
| **Output comparison + narrow state projection** | ShardStore SOSP 2021 (A; FT y; 1 system, >40k LOC Rust, 16 issues prevented; refinement of the reference model; V/TA): "same key-value mapping" after each call. Models are 1 % of implementation code, in Rust, reused as mocks so engineers must update them. Background operations are modelled as no-ops to catch index corruption. A "has failed" relaxation is run with and without failure injection ([source](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)). Cedar FSE 2024 (A; FT y; 21 DRT/PBT bugs; output parity; V): 3 of the 21 were naming disagreements (`lt` vs `lessThan`, `ipaddr` vs `IPAddr`) ([source](https://arxiv.org/abs/2407.01688)) | Output and projected-state divergence | State outside the projection; ShardStore's one known miss was coverage (cache too large) | 1 % of code (ShardStore) | Human-only | analogous (ShardStore closest to a store API) |
| **Existential trace mapping** | Cirstea SEFM 2024 (A; FT y; TA): checks S ∩ T ≠ ∅, not T ⊆ S. "too imprecise logs may even lead to erroneous traces being accepted" ([source](https://arxiv.org/abs/2404.16075)). CCF NSDI 2025 (A; FT y; 1 system; V): "incorrect mappings from implementation to spec state" are one of three named causes of T ∩ S = ∅, "a failure to validate a trace had no counterexample". Writing the 400-LoC mapping "was a minor task"; diagnosing root causes dominated ~2 engineer-months. The mapping changed in 88 commits while the spec changed 107 times ([source](https://arxiv.org/abs/2406.17455)) | Divergence in exercised traces | Erroneous acceptance with imprecise logs | Days to months | Human-only | analogous |
| **PBT-library model state (no first-class `alpha`)** | Hypothesis `RuleBasedStateMachine`: the model is instance state, and the comparison is whatever the user asserts ([docs](https://hypothesis.readthedocs.io/en/latest/stateful.html); B; *direct*). proptest, quickcheck-state-machine and Knossos work similarly ([proptest](https://raw.githubusercontent.com/proptest-rs/proptest/main/book/src/proptest/state-machine.md), [qsm](https://raw.githubusercontent.com/stevana/quickcheck-state-machine/master/README.md), [Knossos](https://raw.githubusercontent.com/jepsen-io/knossos/master/README.md); B). Hughes 2016 (B, experience essay; FT y; TA/V): an operation omitted from the model went untested until distribution statistics showed it; "Errors are often in the model, rather than the code"; 3 of 6 official AUTOSAR test cases "were not covered by the model, because they were not consistent with the standard" ([source](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quviq-testing.pdf)) | Whatever is asserted | Unasserted state; omitted operations | Low | Human-only | direct (Hypothesis mechanism), else analogous |
| **Checks for the mapping itself** | Fonseca EuroSys 2017 (A; FT y; 3 verified systems, 16 bugs; **ind**): negative testing by mutating the implementation; a 7-line patch disabling IronFleet de-duplication "still verified" ([source](https://homes.cs.washington.edu/~pfonseca/papers/eurosys2017-dsbugs.pdf)). IronSpec OSDI 2024 (A; FT y; 14 specs, 10 author-confirmed spec bugs; TA): 4 of 5 sanity-checker bugs were postconditions over "only a subset of these fields" ([source](https://www.usenix.org/system/files/osdi24-goldweber.pdf)). Lamport & Merz: a plausible mapping fails on unreachable states without an invariant ("Those readers are wrong") ([TOPLAS 2022](https://lamport.azurewebsites.net/pubs/simple.pdf); A). Abadi & Lamport: a mapping may need history or prophecy variables ([source](https://lamport.azurewebsites.net/pubs/abadi-existence.pdf); A). CCF "unsatisfied breakpoint" flags over-restrictive mappings | Hidden-state, subset-of-fields and invariant-dependence failures | None measured *as a check on `alpha`* | Low to hours | Human-only | analogous |
| **Agent-written mappings** | SysMoBench ICLR 2026 (A; FT y; TA for the harness): LLM name/action mapping, inspected and "found the results to be correct"; 10 renamed gold variants all scored perfectly. It maps names, not state ([source](https://arxiv.org/abs/2509.23130)). VeriStruct TACAS 2026 (A; FT y; 11 Verus modules; TA): "LLMs sometimes produce a trivial Cartesian-product view, which includes all of the data fields"; fixed by a view-refinement prompt plus unit tests; 10/11 modules verified ([source](https://arxiv.org/abs/2510.25015)) | — | Frequency of trivial views unquantified | Low | **LLM measured** | analogous |

**Failure modes and their checks (D2 Q2).** Seven failure modes have full-text support. *Inference*: each check is borrowed, and none has been measured as a check on `alpha`.

| # | Failure mode | Source | Borrowed check |
|---|---|---|---|
| 1 | Mapping bug with no counterexample | CCF | Spec-side unreachable-state report |
| 2 | Partial projection accepts wrong behaviour | Cirstea; IronSpec, by analogy | R mutants that alter one non-projected field must be caught (Fonseca; ShardStore no-op background operations) |
| 3 | Mapping valid only under an invariant | Lamport & Merz | Assert R's invariant before calling `alpha` |
| 4 | `alpha` cannot be a function | Abadi & Lamport | Compare by relation or membership, not equality |
| 5 | Omitted operations | Hughes | Per-action distribution statistics |
| 6 | Relaxations that mask bugs | ShardStore; MongoDB, per the verified edition | Run every relaxed check unrelaxed as well |
| 7 | Trivial agent-written view | VeriStruct | Anti-identity check; unit tests |

**Stability (D2 Q4).** Four mechanisms are evidenced:
- per-component models and composed projections (ShardStore; IronFleet's composed refinement functions and per-type library);
- co-location with the code, plus reuse as mocks, so that drift breaks the build (ShardStore);
- separate weaker equivalences for crash and concurrency (ShardStore);
- a small trusted observation relation separate from the untrusted mapping (IronFleet).

**No source documents versioning of `alpha`, a review procedure for it, or a round-trip (`alpha(gamma(s)) == s`) test.**

**Baseline handling.** Verified edition §2.3.2, verbatim: "A reviewed, versioned abstraction function `alpha(R_state) → spec_state` is the cheapest structural decision, and the place agents are likely to cut corners". The earlier report's wording is "the single cheapest structural decision".

**Qualified, not challenged.** Writing the mapping is cheap: CCF's 400-LoC `Trace` spec "was a minor task", and ShardStore's models are 1 % of the code. Getting it right is not shown to be cheap, because diagnosis dominated CCF's two engineer-months. Agents cutting corners has one measured instance, VeriStruct's trivial views, with no frequency given. "Reviewed" should become "small trusted observation relation reviewed and versioned; projection checked" (D2-R1, D2-R2).

The bridge-table row "| **Refinement checks** | No full-text bridge evidence | — | — | — |" stays true for F ↔ Python R. It can now cite *analogous* refinement practice (IronFleet, Armada, seL4).

**Disconfirming search §4(b): a reviewed `alpha` does not reduce bridge defects.** *Result: no direct evidence either way; weak disconfirmation of the emphasis.*
- Fonseca et al., the only independent study, found 16 bugs in verified systems: 11 shim-layer, 3 verification-tool and 2 specification bugs in Figure 3. **None was in a refinement or abstraction function.** Their abstract places the violated assumptions "mostly at the interface of verified and unverified components". Their §6 text says four tool bugs and Figure 3 lists three; this is unresolved.
- IronSpec's 10 spec bugs were all too-weak specs or too-restrictive environments.
- seL4 does not name the state relation as a bug site.

*Inference*: in proof systems a wrong refinement function cannot cause a false pass; it can only block the proof. In a Python R checked by tests it can cause a false pass silently. Concentrating review on `alpha` while leaving the environment and fault model, logging and spec strength unreviewed would contradict the Fonseca and IronSpec distribution (D2-R5). **Single-independent-source sub-question.**

### 2.3 D3 Python-native and single-source options

**Finding.** Pipeline A is feasible in pure Python today. **Hypothesis**, including `RuleBasedStateMachine`, is the only tool here that is mature, maintained and backed by independent effectiveness data. That data is mostly stateless.

Pipeline C is feasible only in a weakened form. Only Dafny literally generates a Python R, and its back-ends have fuzzing-found soundness bugs. Quint is the most usable oracle, but it checks a separately written R.

| Option | Evidence (grade; FT; n, setting; "correct") | Catches | Misses | Cost / maturity | Agents | Transfer |
|---|---|---|---|---|---|---|
| **Hypothesis stateful testing** | Ravi & Coblenz, OOPSLA 2025 (venue A via Crossref; **full text [unreachable]**, ACM 403; claims from the artifact README, B; Python OSS projects; mutant killed; ind). Unit tests were 98.4 % of tests and killed 84.7 % of mutations; PBTs (1.6 %) killed 15.3 %, more per test. 76 % of PBT-found mutations appeared within 20 inputs ([README](https://raw.githubusercontent.com/ucsd-salad/python-pbt-eval/main/README.md)). MacIver & Donaldson, ECOOP 2020 (A; FT y; TA): shrunk tests stay generatable, so rule preconditions hold after shrinking (*Inference* for state machines) ([source](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf)). **Own trial 3** (toy store, 1 seeded 4-step bug): default backend found it in 10/10 seeds in 0.6–1.5 s and shrank to the minimal sequence; the CrossHair backend missed it in 1 run (31 s) | Sequence bugs, with minimal counterexamples | Inherits the model's and contract's weakness; no stateful-specific study | 1,592 releases; 144 in the last 12 months (PyPI) | Human-only | direct (mechanism); effectiveness analogous |
| **CrossHair** | Docs (B; TA): "the absence of a counterexample does not guarantee that the property holds"; "Only deterministic behavior can be analyzed" ([limitations](https://raw.githubusercontent.com/pschanely/CrossHair/main/doc/source/limitations.rst)). No peer-reviewed evaluation found. Self-measurement `measured.json` (C; TA): 436 of 2,403 stdlib callables "handled at every size" ([source](https://raw.githubusercontent.com/pschanely/CrossHair/main/doc/source/measured.json)). **Own trial 1**: found a seeded off-by-one in 27.7–40.5 s. After the fix it still reported a counterexample, exposing a **missing precondition**. With the precondition added, nothing was found in 150 s | Contract counterexamples; under-constrained contracts | Nondeterminism; proof | 0.0.112; 224 of ~287 recent commits by one maintainer | Human-only | direct (toy) |
| **deal; icontract; icontract-hypothesis** | deal docs (B; TA): the prover is "**experimental** and always will be", "It will work for only 1% of your code" ([source](https://raw.githubusercontent.com/life4/deal/master/docs/basic/verification.md)); last release 2025-11. Own trial 2: `deal test` targets "pure functions" and gave no output on a mutating operation. icontract: 2 releases in 12 months, one maintainer. icontract-hypothesis: last release 2021-07, last commit 2022-06 (PyPI, git) | Runtime contract violations | No effectiveness data for any of them | Low activity; dormant | Human-only | direct (mechanism) |
| **Python history checkers** | detangle 0.1.0 (B; PyPI description; TA): one release (2026-09-26), WGL/Lowe search "like Knossos and Porcupine", simulated I/O only ([PyPI](https://pypi.org/pypi/detangle/json)). **Own trial 4**: flagged a non-atomic counter in 0.43 s; the offline `lin.check` path was not exercised. c3py: "API is subject to change", last commit 2024-02 ([README](https://raw.githubusercontent.com/shumbo/c3py/main/README.md)). Porcupine (Go) and Elle (JVM via elle-cli, lead only) run out of process. No neutral benchmark | Linearizability violations | — | Brand-new or unreleased | Human-only | direct (toy) |
| **Dafny → Python (literal single source)** | Integration guide (B; V): `--target:py`; "To call python from Dafny, one must edit the translation"; doc still says "as of v3.9.1" ([source](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/integration-py/IntegrationPython.md)). Donaldson et al., ICST 2024 (A; FT y; TA): "24 previously-unknown Dafny compiler bugs … of which 9 are soundness issues"; 5 table rows implicate the Python back-end (alignment from pdftotext); the campaign also changed the language spec ([source](https://www.doc.ic.ac.uk/~afd/papers/2024/ICST.pdf)). XDsmith found 31 bugs, Python not targeted ([ISSTA 2022](https://ahmed-irfan.github.io/papers/issta22.pdf); A; FT partial; V). CompFuzzCI found 3 more ([ICST 2025](https://www.doc.ic.ac.uk/~afd/papers/2025/ICST-Industry.pdf); A; FT partial) | Generates R from verified source | Miscompilation; readability and performance unmeasured | No own trial possible (no dotnet) | Human-only | analogous |
| **Lean (Cedar pattern)** | cedar-lean-ffi README (B; V): Rust calls Lean via FFI and Protobuf ([source](https://raw.githubusercontent.com/cedar-policy/cedar-spec/main/cedar-lean-ffi/README.md)). AWS blog (C; V): Lean 5 µs vs Rust 7 µs per DRT input ([source](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/)). No Lean → Python binding found | Proof-backed oracle | Python plumbing unprecedented | FFI or subprocess | Human-only | analogous |
| **Quint + ITF replay** | **Own trial 5** (toy store spec): the simulator found a seeded spec bug in 20 ms. 10,000 × 20-step samples took 3.4 s. A fixed seed gave identical ITF states. The default Rust backend needed a GitHub download (failed in the sandbox). `--mbt` left `actionTaken` empty for one action, possibly misuse. `itf-py` 0.5.0 crashed on Option `None`. A 25-line replay gave 0/50 divergences for the correct R and 20/50 for a seeded R | Seeded, reproducible oracle traces | Covers only simulator-reachable paths; not a Python generator | npm 0.33.1 (2026-10-28) | Human-only | direct (toy) |
| **P / PObserve** | Compiler outputs PChecker, PObserve, PEx, PVerifier; the PObserve back-end generates Java; no Python target (repo, B; V). PObserve checks service logs, with no stated limitations ([docs](https://p-org.github.io/P/advanced/pobserve/pobserve/)) | Independent log check | Not usable as R | JVM | Human-only | analogous |

**Which choice makes which pipeline feasible (D3 Q3).** Pipeline A works with Hypothesis stateful tests, icontract or deal runtime contracts on R, CrossHair as a time-boxed advisory probe, and an out-of-process or young history checker (R-D3-1, R-D3-2).

For Pipeline C, the baseline text (verified edition §4, Pipeline C) reads verbatim: "1. One executable formal source per operation (R itself, Quint, or Lean; left open)." and "2. Markdown prose and other models are **generated** from it." D3 makes three points against this.
- **(i) "R itself" collapses Pipeline C into Pipeline A.** No Python tool derives TLA+, Alloy or prose from Python. CrossHair and deal only check contracts written in Python.
- **(ii) A literal single source with R generated means Dafny → Python**, plus a mandatory back-end DRT leg: a Python build vs a C# or Java build on Hypothesis inputs. This leg cannot catch front-end errors shared by all back-ends.
- **(iii) Quint plus ITF replay against a separately written R is "C′"**: a source plus a mechanically bridged R. It is not a single source.

All three points are *Inference*, and they rest on D3's strict reading of "single executable source" (§5.5).

**Disconfirming search §4(c): single-source pipelines miss more intent errors than separately authored layers.** *Result: no same-fault comparison exists. Three full texts show the pure single-source failure mode.*
- **IronSpec** (A; TA): 10 spec bugs across 6 real verified systems. For the 5 sanity-checker finds, "The corresponding implementation for all five spec bugs appeared correct, but the specs were buggy, being too weak". For example, the ESDK spec still verified with a constant zero-byte output ([source](https://par.nsf.gov/servlets/purl/10550356)).
- **Fonseca** (A; ind): Bug I1, where IronFleet's spec did not require exactly-once semantics.
- **Sail-RISC-V vs Spike** (B, 2-page summit paper; ind of the Sail authors): the generated golden model deviated from independently written Spike on 0.23 % of valid and 3.73 % of invalid+valid sequences ([source](https://ics.jku.at/files/2026RISC-V_Summit_Europe_RVVTS_SailRV_Spike.pdf)). Not all deviations were verified to be Sail bugs.

In every case a *separately authored* artefact found the errors: spec-testing proofs, negative-test patches, or Spike. This **supports** the verified edition's Pipeline C failure mode, verbatim: "A misreading in the single source propagates consistently into every generated layer; SpecTec can detect it only via the test suite." It does **not** show that Pipeline C *with* an independent check set misses more than Pipeline B (R-D3-4).

### 2.4 D4 Consistency for data-rich APIs with environment actions

**Finding.** "For every environment move, some allowed response exists" has a well-studied **one-step form**:
- Event-B feasibility (FIS) and deadlock-freedom (DLF) proof obligations;
- the AGREE/JKind/Kind 2 viability "extend" check over integers and reals.

With an inductive invariant the one-step form is sufficient for realizability of safety contracts. Gacek et al.'s Theorem 1 says verbatim: "A contract … is realizable if and only if ∃s. G_I(s) ∧ Viable(s)".

The check decomposes **exactly per environment move**, because the universal quantifier distributes over operations (*Inference*). So mode variables become read-only context rather than connectors. rt-consistency as implemented in 2019 has no input/output split. **No source applies any of these checks to a library or storage API.**

| Option | Evidence (grade; FT; n, setting; "correct") | Catches | Misses | Cost | Agents | Transfer |
|---|---|---|---|---|---|---|
| **One-step response existence / viability (AGREE, JKind, Kind 2)** | Gacek et al., NFM 2015 (A; FT y; 3 case studies, 20 component contracts; correct = an implementation exists, confirmed by synthesis or manually; TA). Five of six student teams wrote microwave requirements "inconsistent under certain input conditions", missed by AGREE's consistency check. The GPCA mode × alarm conflict "was not discovered by the regular consistency check". A QFCS fault-response conflict "eluded the engineers". 18/20 decided in 0.1–1.762 s, 2 unknown at the 1000 s timeout; base check depth ≤ 1 ([source](https://arxiv.org/pdf/1502.03005)). Larraz & Tinelli, Kind 2 (A-pre; FT y; 159 benchmarks; correct = agreement with JKind; TA): solves a strict superset of JKind's problems; returns deadlocking computations and conflicting guarantees with 43 % overhead ([source](https://arxiv.org/pdf/2205.09082)) | Clauses pinning a response that only a cooperative environment avoids; plain SAT passes these | Unknown under quantifier alternation; multi-step obligations need full realizability | Seconds per component | Human-only | analogous |
| **Event-B DLF/FIS via constraint solving (ProB)** | Hallerstede & Leuschel, TPLP 2011 (A; FT y; Bosch cruise control: 80 events, 855 guards, 62 variables, plus 14 benchmarks; correct = a solution of the negated obligation exists; TA with an industrial user). The DLF obligation ran to 34 pages and crashed Rodin. ProB solved it in 1.07–2.32 s; explicit model checking "failed to find a counter example after running for almost 4 hours". A "predicate of interest" filters events that cannot fire, giving "a much better decomposition". Counterexample states are "not necessarily reachable". Benchmarks include a file-system model (FMCH02, 9 events) and a BPEL purchase-order process that took 5 iterations to become deadlock-free; one deadlock-freedom proof used "a wrong proof obligation" ([source](https://arxiv.org/pdf/1109.2015)). Event-B wiki (B): FIS soundness flaw for refined machines with witnesses ([source](https://wiki.event-b.org/index.php/Revisiting_Feasibility_POs)) | States with no foreseen action | Spurious counterexamples from unreachable states | Seconds | Human-only | analogous (nearest storage/service precedents) |
| **TLA+ `ENABLED` and deadlock (TLC, Apalache)** | Apalache manual (B): "`ENABLED A` ✖ … Has to be specified manually"; deadlock bounded by `--length` ([features](https://raw.githubusercontent.com/apalache-mc/apalache/main/docs/src/apalache/features.md)). TLC `ENABLED` in invariants: community threads only (C) ([source](https://discuss.tlapl.us/msg04343.html)). The AWS 2014 report (B; V) and Cosmos DB ICSE-SEIP 2023 (A; FT y; V; closest to a client-facing store API) report no response-existence check ([AWS](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf); [Cosmos DB](https://arxiv.org/pdf/2210.13661)) | Reachable deadlocks within bound | No ∀∃ one-step form | Seconds to minutes | Human-only | analogous |
| **rt-consistency (Ultimate ReqAnalyzer, Hanfor)** | Langenfeld et al., RE 2019 (A; FT y; TA + Bosch). The definition, verbatim: "rt-inconsistent if and only if there exists a finite prefix … such that there does not exist any extension of this prefix which satisfies all requirements". It ranges over all observables. Only c-subsets are checked, with c = 2 evaluated; "deadlocks caused by more than c requirements are not checked". Input/output discrimination is future work ([source](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)). FASE 2011 original [unreachable] | Timed-pattern conflicts | Not ∀ environment ∃ response; conflicts among more than c clauses | Minutes to hours | Human-only | analogous |
| **Realizability modulo theories** | Rodríguez & Sánchez, CAV 2023 (A; FT y; 6 industrial-inspired + 1 synthetic spec; TA): Boolean abstraction is doubly exponential in each cluster's input literals; clusters of 2–7 (up to 12) literals; Strix <7 s ([source](https://arxiv.org/pdf/2310.17292)). TSL modulo theories (A-pre; FT y; TA) is *satisfiability*, not realizability ([source](https://arxiv.org/pdf/2104.14988)) | Data-valued reactive conflicts | Clusters joined by shared variables blow up | Seconds to minutes | Human-only | analogous |
| **Alloy 6 / Electrum** | Macedo et al., FSE 2016 (A; FT y; hotel locking, spanning tree; TA): unbounded runs up to thousands of seconds; no API or response-existence case ([source](https://perso.ens-lyon.fr/denis.kuperberg/papers/electrum.pdf)) | Bounded temporal properties | — | High | Human-only | analogous |
| **Mode-aware contracts** | CoCoSpec, SEFM 2016 (A; FT y; 1 case study; TA): the "defensive" property flags reachable unspecified situations; "it quickly became impossible for us to trust a contract without examining the mode reachability graph first" ([source](https://homepage.cs.uiowa.edu/~tinelli/classes/5810/Fall20/Papers/Cham16.pdf)) | Mode incompleteness; deadlocked modes | — | ~80 s compositional *verification* | Human-only | analogous |
| **Own trial (Z3, synthetic store API)** | Own trial, author-written, LIA + arrays. Check: Inv ∧ request ⇒ ∃ response. clauses ∧ Inv′, per operation. 40 operations × 46 clauses: 1.32 s with finite response tags enumerated, 0.13 s for plain consistency. One "unknown" out of 40 with full quantification, none with enumeration. Two injected defects passed plain SAT and were flagged in ≤ 0.027 s with cores of 1 and 3 clauses. The "conflict-free" generator held 3 unintended error-precedence conflicts, one involving 3 clauses (quota vs profile vs fault). A c = 2 subset check would miss that one (*Inference*). Cost grew roughly linearly, 0.22 s → 0.99 s for 10 → 40 operations | Cross-table error-precedence conflicts | No sets or global quantified invariants; no interleaving; counterexamples not confirmed reachable | ~0.03 s per operation | Not measured | inference |

**Mode variables and locality (D4 Q2).** FRET FM 2021 (A; TA) decomposes by "connected components" of shared variables. Three specs stayed one component, and "requirements were connected through mode variables" was "One reason". The fix, "studying the mode-transition logic separately from the intra-mode requirements", is unpublished future work ([source](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf)).

*Inference*: mode variables defeat **variable-sharing partitions**, such as FRET, Boolean-abstraction clusters and ReqAnalyzer subsets. They do not defeat **move-indexed decomposition**. When a per-operation query times out, slice it per mode cell, as with ProB's predicate of interest. Locality is lost again in three cases:
- quantified global invariants over all handles;
- multi-step obligations;
- interval operations with pending state.

**Baseline handling (verbatim, then qualified).**
1. §3 check map, "Environment actions", consistency cell: "rt-consistency / realizability (∀ environment move ∃ allowed response), environment actions as free transitions; well-separation". **Qualified.** The parenthetical fits realizability, FIS/DLF and viability, not rt-consistency as implemented. The earliest-failure note "**G4** (plain SAT passes; needs the quantified check)" is **confirmed** by Gacek's three cases and the own trial.
2. Pipeline B: "Connected requirements, for example via mode variables, defeat partitioning, so full runs take hours." **Qualified.** It holds for variable-sharing partitions of full runs. One-step checks at comparable size took seconds: ProB on 855 guards in 1.07–2.32 s, AGREE at ≤ 1.762 s, own trial 1.32 s. "Hours" belongs to nightly full temporal checks.
3. §2.2: "Expect handle state, profile and lifecycle phase to act as connecting mode variables for a store API." **Qualified.** This still holds for variable-sharing partitions. They do not connect per-operation response-existence obligations (*Inference*).
4. §2.2 Realizability "Misses": "Undecidable in general; data domains; interleavings". **Qualified.** "Data domains" is too strong for LIA/LRA, where Gacek, Kind 2 and the Boolean abstraction work, with "unknown" outcomes. It stays accurate for GR(1), non-linear arithmetic and collections. "Interleavings" stands.
5. Part 3: "R7 | rt-consistency / realizability with environment actions, plus well-separation (G4) | inference by analogy (FRET, GR(1)); no library application | low |". **Raised to medium for the one-step form only** (D4-R1).
6. §5 open question 5: "Realizability checking has not been applied to a library or storage API." **Unchanged.**

### 2.5 D5 Independence of the expectation family

**Finding.** Hiding the implementation, or the conversation that produced it, from the test writer measurably improves tests when the implementation is wrong. **No study measures isolation from a spec or formal model, and none measures OS-level read scopes.** No evaluated detector targets "expected value computed by the reference model". Added commitments are now measured as the largest single cause of invalid LLM-written unit tests (one TA study).

| Option | Evidence (grade; FT; n, setting; "correct") | Catches | Misses | Cost | Agents | Transfer |
|---|---|---|---|---|---|---|
| **Fresh session with the task description only** | Konstantinou, Tambon & Papadakis, arXiv 2607.05139 (A-pre; FT y; HumanEval+, MBPP+, BigCodeBench; one hardest LLM-faulty implementation per task; 5 models; correct = suite fails on the faulty implementation; no conflict noted). Fresh context vs same conversation: +10.6 % to +17.7 % per model, mean +11.7 %, p ≤ 0.0019 for each model. Summarisation, CoT and CoVe did not remove the bias. Isolated tests still detected only ~25 % of hard faults (vs 14 %) ([source](https://arxiv.org/abs/2607.05139)) | Code-anchored oracles | ~75 % of hard faults; spec-level isolation untested | One extra session | Measured (simulated agentic loop) | analogous |
| **Description only vs code access** | Huang et al., ICSE 2026 (A; FT y; 11 LLMs; HumanEval, MBPP, APPS + 41 repo-level cases; correct test = passes the canonical solution; mild interest, same group as AgentCoder). HumanEval test accuracy: task only 78.3 %, with correct code 80.4 %, with incorrect code 57.1 %. 94.8–99.3 % of incorrect GPT-4 tests had wrong *oracles*. Bug detection favoured correct code (47.4 %) over incorrect code (38.1 %) ([source](https://arxiv.org/abs/2409.09464)) | Avoids incorrect-code anchoring | Forgoes the help that correct code gives | — | Measured | analogous |
| **Separate code-blind test designer** | AgentCoder (A-pre; FT y; TA; confounded by its prompt): test accuracy 61.0 % → 87.8 % (HumanEval) ([source](https://arxiv.org/abs/2312.13010)). Ma & Eisty (A-pre pilot; FT y; 10 Defects4J Lang bugs; requirements written from fix diffs): macro-F1 0.56–0.82 ([source](https://arxiv.org/abs/2607.10277)) | — | Confounds | — | Measured | analogous; Ma & Eisty direct-adjacent (n = 10) |
| **Read scope / import guard** | **Own trial (F1.9)**: a `sys.meta_path` guard blocked three import forms but not `exec(open('…/refmodel.py').read())`. EvilGenie (A-pre; FT y; 154 LiveCodeBench problems, test files deliberately open) measures reward-hacking *detection* with open access, not a closed scope ([source](https://arxiv.org/abs/2511.21654)) | Accidental access | Deliberate reads; copy-pasted R logic | Low | Not measured | direct (mechanism, toy) |
| **Anchoring lint** | PyNose, ASE 2021 (A; FT y; TA): "Redundant Assertion" only catches `assertEqual(X, X)` and similar, validated on **2 instances**; unittest only ([source](https://arxiv.org/abs/2108.04639)). tsDetect/JNose on LLM tests (TOSEM; A; FT validation; 20,505 suites, manual oracle of 240 classes): Assertion Roulette precision 0.34–0.62 at recall 1.0; "relying on a single detector can substantially bias" ([source](https://arxiv.org/abs/2410.10628)). **Own trial (F2.4)**, 6 cases: flagged direct and variable-mediated use of R; missed helper indirection and dynamic import | Direct R calls in assertions | Indirection; dynamic import; copied logic | Low | LLM tests (TOSEM) | direct (toy) / analogous |
| **Consensus filter against independently generated code** | ConVerTest, ICST 2026 (A; FT y; BigCodeBench, LBPP; 3 LLMs; valid = passes ground truth; TA). In 100 sampled invalid tests, "Expecting behavior not requested in the spec" accounted for **28 %** (79 % agreement). Filtering raised kept-test validity from 51–77 % to 84–91 %, at 89–96 % recall ([source](https://arxiv.org/abs/2602.10522)) | Idiosyncratic added commitments | Misreadings shared with the generated code survive by construction | Several generations | Measured | analogous |
| **Many correct variants (allowed-variant check at scale)** | CodeContests+ (A per Semantic Scholar; FT §4; 100 correct + 100 incorrect submissions per problem; TA): original CodeContests had "over 4000 problems with TPR ≤ 0.1 and TNR ≥ 0.9", from wrong tests or missing multi-solution checkers ([source](https://arxiv.org/abs/2506.05817)). EvilGenie: 9/154 problems ambiguous, with "much higher rates of reward hacking" on them | Over-strict exact-output oracles | Needs many independent correct variants | 300 M executions | Agent-generated tests | analogous |
| **Citation check; LLM judge; human adjudication** | Panda, arXiv 2606.30689 (A-pre, single author; TA): 86.4–88.0 % detection, but the "hallucinations" used author-injected **fake IDs**, so the measurement is circular ([source](https://arxiv.org/abs/2606.30689)). Jin & Chen (A; FT partial in D5; verified edition: full): LLMs "frequently misclassify correct code implementation as non-compliant" ([source](https://arxiv.org/abs/2603.00539)). Kaufman et al. (A-pre; FT abstract + intro; 86 programmers): 74 % accuracy on correct vs 49 % on incorrect assertions ([source](https://arxiv.org/abs/2607.08885)) | Uncited assertions | Valid-ID added commitments; judge over-rejection; humans accept wrong assertions | Low | Measured | analogous |

**Baseline handling (verbatim, then qualified).**
1. §2.3.3: "Canedo's anchoring predicate becomes a dataflow/import lint." **Qualified.** A lint alone is bypassable (own trials). No existing smell detector implements the predicate. It should sit *behind* a file-system read scope (D5-R2).
2. §5 open question 16: "16. Over-strictness of LLM-written acceptance tests has not been measured." **Narrowed.** It is still unmeasured for *acceptance* tests and stateful APIs. It is now measured for unit tests written from docstrings (ConVerTest, 28 %) and for curated benchmarks (CodeContests, LiveCodeBench). D5's notes attribute this item to "§3 open questions"; it is item 16 of §5 in the verified edition.
3. Table S8: "Necessary, not sufficient." **Reinforced**, by analogy at the code → test level: 25 % detection even when isolated; LLM errors "cluster tightly" ([SAGA](https://arxiv.org/abs/2507.06920), partial read, CB).

### 2.6 Where the notes disagree with each other or with the verified edition, and the choice made

| # | Disagreement | Choice and reason |
|---|---|---|
| 1 | Verified edition and earlier report: "reviewed, versioned `alpha`" is *the* cheapest decision. D2: practice trusts only a small observation relation; defects concentrate elsewhere | **D2.** It rests on new full texts (IronFleet, Armada, Fonseca, IronSpec). Equal review weight goes to the environment/fault model, logging and spec strength |
| 2 | Verified edition Pipeline C: "R itself, Quint, or Lean". D3: drop "R itself"; Quint and Lean give C′ | **D3, with its own caveat.** If "single source" means one *formal* source with a separately written Python R allowed, Quint and Lean are full Pipeline C and the C′ label overstates the difference (§5.5) |
| 3 | Verified check map credits rt-consistency with "∀ environment move ∃ allowed response". D4: it has no input/output split | **D4.** The RE 2019 definition ranges over all observables. The 2011 FASE original was not read |
| 4 | D3 trial compares `alpha(R state)` to the ITF state by equality. D2-R3: compare by membership wherever S leaves choices open | **Both, by case.** Equality is fine where the spec state is determined, as in the toy. Membership applies to unspecified or late-nondeterministic outcomes (Abadi & Lamport) |
| 5 | D1: allowed variants = separately built wheats. D5: variants from the non-promise register (NonDex-style) or generated code (ConVerTest) | **Combined.** Both measure the same validity property. D1's warning (wheats themselves over-strict) and D5's (common-mode misreadings survive consensus) both apply |
| 6 | IronSpec venue: D3 hedges (PDF acknowledgement only). D2 cites the USENIX OSDI '24 PDF; the verified edition says A | **OSDI 2024, A.** The USENIX proceedings URL settles it |
| 7 | Verified debt: Hughes "Experiences with QuickCheck" [unreachable]. D2 read it in full (B) | **Resolved** (B, experience essay) |
| 8 | Jin & Chen: D5 "FT partial". Verified edition "yes" | Keep the verified edition's full read. D5 used only an excerpt |

---

## §3 Updates to the verified edition's check map, gate sequence and Pipelines A, B and C

Every new cell is *Inference*. Each maps the cited analogous evidence onto the brief's forms. Rows not listed are unchanged: case table; termination under timeout assumption, where full realizability or bounded liveness remains necessary (D4 Q3); and state × operation transition table, which is the "mode-transition" half of FRET's proposed split.

### 3.1 Check map (verified §3)

| Row / column | Old cell (verbatim, abbreviated with …) | New cell | Reason | Source / notes ID |
|---|---|---|---|---|
| Formula over one instant / Faithfulness | "Scenario derivability; rejected-option refutation; added-commitment probe …" | Same, **plus**: the record check set is screened against ≥ 2 allowed-variant R wheats before it gates. A check failing any wheat is repaired or discarded | A single oracle lets over-strict checks through | ICER 2018; ICER 2019; D1-R1 |
| Formula over one instant / Enforcement | "Exp.: literal I/O from the scenario. Mutant: R returns a rejected-option output." | "Exp.: literal I/O where the decision fixes the value; **membership predicate** where it leaves a set open. Mutants: R returns a rejected-option output; R randomises output fields the clause leaves unspecified, and the spec must reject that where the decision commits" | A deterministic R realises only one allowed outcome. Subset-of-fields postconditions are the commonest too-weak spec | Koli 2021; IronSpec §5.1; D1-R2, D3 Q4 |
| Frame / Enforcement | "Spec.: full-state snapshot via `alpha`. … Miss: state outside `alpha`" | "Spec.: full-state snapshot through a split `alpha`: reviewed observation relation + checked projection. R mutants altering one non-projected field must be caught. Background and environment operations included as model no-ops. Miss: state outside the observation relation" | Hidden-state and partial-projection failures; ShardStore practice | ShardStore §4.1; Fonseca; D2-R1, D2-R2 |
| Environment actions / Consistency | "rt-consistency / realizability (∀ environment move ∃ allowed response), environment actions as free transitions; well-separation" | "Per-operation response existence relative to Inv (FIS/viability shape; SMT; finite response tags enumerated; minimal clause core). Environment actions preserve Inv. Counterexample confirmed by bounded reachability (TLC; Apalache with an explicit ∃ predicate, since it lacks `ENABLED`). Full realizability (Kind 2) only for multi-step clauses. rt-consistency for timed patterns only. Well-separation unchanged" | rt-consistency has no input/output split. The one-step form is measured, local and sufficient for safety with an inductive Inv | Gacek NFM 2015; Hallerstede & Leuschel; RE 2019; own trial; D4 Q3.1 |
| Environment actions / Earliest failure | "**G4** (plain SAT passes; needs the quantified check)" | "**G4a**, every edit (plain SAT passes; confirmed)" | One-step checks run in seconds | D4 Q3 |
| Failure category / phase / effect / retry tables / Consistency | "Per-table complete/disjoint; cross-table with frame and state tables; retry × concurrency as divergence" | Same, **plus** "G4a response existence across tables per operation" | Error-precedence conflicts across tables pass per-table checks. The own trial's 3-clause conflict is exactly this kind | Own trial; D4 Q3 |
| Failure tables / Earliest failure | "**G3**" | "**G3 + G4a**" | As above | D4 Q3 |
| History predicate / Enforcement | "Spec.: R run concurrently, Porcupine-style check against R's sequential mode …" | Same, **plus**: "Python route: Porcupine as a subprocess, with R's sequential semantics re-expressed as a Porcupine model (a second bridge to review), or detangle `lin.check` only after a seeded-history calibration. Each allowed interleaving or resolution choice becomes a separate deterministic wheat" | No mature Python checker. Nondeterministic wheats give flaky verdicts | D3 R-D3-2; ICER 2019 §9; D1 Q3 |
| Register of non-promises / Enforcement | "Tests must not assert on the dimension; **allowed-variant check**; survivors mapping to the register auto-classified "intended"" | Same, **plus**: "allowed variants = ≥ 2 wheats that differ on every non-promised item, or NonDex-style perturbation. Report RejectLegal and DetectFault together. Wheats and chaffs themselves reviewed for over-constraint" | Measured benefit of multiple wheats; wheats and chaffs can be wrong | ICER 2018; Forge §7.3; Making Hay; ConVerTest; D1-R4, D5-R3 |
| Register of non-promises / Earliest failure | "**G2**; over-strict tests at **G8**" | "**G2** (check set screened against wheats); over-strict expectation tests at **G8**" | Screening moves forward | D1-R1 |
| Variation points / profiles / Consistency | "Typed profile schema; each value conjoined separately" | Same, **plus** "G4a run per profile value (predicate of interest)" | Per-mode slicing keeps checks local and counterexamples readable | Hallerstede & Leuschel; D4 Q3 |

### 3.2 Gate sequence (verified §2.4)

| Gate | Old (verbatim "Fails on") | New | Reason | Source / notes ID |
|---|---|---|---|---|
| G0 | "missing or duplicate IDs, malformed form, untyped non-commitment, undeclared value domain" | Same, **plus** a static module-level ban: the expectation-test directory must not import R, spec helpers or models | The cheapest independence layer. It is leaky, so it backs up the read scope | Own trial F2.4; D5-R2 |
| G2 | "rejected scenario witness, failed rejected-option refutation, "not addressed" on an added-commitment probe" | Same, **plus**: (a) any record check failing an allowed-variant wheat (repair or discard); (b) any conceptual chaff (rejected option or clause misreading) killed by no check; (c) chaffs that also reject valid behaviour. For temporal clauses, distinguishing traces between the intended formalisation and candidate misreadings, classified spec-blind | Validity and thoroughness both measured; candidate differencing fits temporal clauses | ICER 2018/2019; Making Hay; PICK; D1-R1, R3–R5 |
| G4 | "unsat core, contract inconsistency, rt/realizability failure, well-separation failure" | **Split.** G4: conjunction, unsat core in k-subsets. **G4a**: per-operation response existence relative to Inv, optionally per mode cell. **G4b**: Inv preserved by every environment action and allowed response. **G4c**: bounded-reachability confirmation of G4a counterexamples. **G4d**: full realizability for multi-step clauses; rt-consistency for timed patterns; well-separation (nightly) | Per-edit seconds vs nightly hours. Spurious counterexamples from unreachable Inv-states need confirmation | D4 Q3; D4-R1, R4 |
| G5 | "a mutated invariant or model fails to yield a counterexample; smoke tests; sanity flags" | Same. **Ordering added**: G5 must precede trusting a G4a *pass*, because a contradictory Inv makes G4a vacuously pass | Inconsistent axioms make the negated obligation unsolvable | Hallerstede & Leuschel; D4 Q3 |
| G6 | "DRT or replay mismatch; trace-validation rejection" | Same, **plus** `alpha` checks: R invariant asserted before `alpha`; anti-identity flag; R mutants on non-projected fields; every relaxed comparison also run unrelaxed; membership comparison where S leaves choices open. CrossHair runs time-boxed on contract-bearing functions as **advisory**, non-blocking | `alpha` is code under test. CrossHair's silence is not proof, and its bus factor is ~1 | D2-R2–R4, R6; D3 R-D3-1 |
| G7 | "clause without spec test, … never-fired action, …" | Same, **plus** per-action operation-distribution statistics on the state-machine driver | An omitted operation went untested until statistics showed it | Hughes 2016; D2-R2 |
| G8 | "R mutant not killed by both families (compared at equal test counts); any test failing on an allowed variant" | Same; allowed variants as in §3.1; RejectLegal and DetectFault reported together | Measured form of the allowed-variant check | ConVerTest; CodeContests+; Liang survey (metric definitions); D5-R3 |

**Unchanged:** G1, G3 and G9. The verified ordering rules stand: G5 before trusting model checking; G8/G9 after G6.

### 3.3 Pipelines

**Pipeline A (record-anchored, light formal core).**

| Item | Old (verbatim) | New | Reason / ID |
|---|---|---|---|
| Step 2 | "A **record-derived check set** is produced by lineage B, which sees records only, *before* the spec exists." | Same, **in a fresh session holding only the records, enforced by a file-system read scope** (R, spec and models not mounted). Import ban and runtime guard as backup | +11.7 % from fresh-context isolation (code → test); import guards are bypassable. D5-R1, R2 |
| Step 5 | "G2: record-derived checks run against an executable rendering of each clause, plus added-commitment probes to a spec-blind judge." | Same, **after** screening against ≥ 2 allowed-variant wheats and a small conceptual-chaff set (G2 a–c) | D1-R1, R3 |
| Step 6 | "G3 tables; G4 conjunction on shared-variable subsets; G5 vacuity." | "G3; G4 conjunction; **G4a/G4b** per operation; G5 vacuity" | G4a needs only the shared signature G4 already needs. D4 Q3 |
| Step 7 | "R built; G6 contract → PBT and state-machine conformance." | "R built; G6 with Hypothesis `RuleBasedStateMachine` as the driver (rules = operations; model state through the split `alpha`; invariants = spec invariants), icontract or deal runtime contracts on R, CrossHair advisory" | D3 R-D3-1; D2-R1 |
| Step 9 | "TLA+ only for environment and history forms, …" | Same; history forms checked in Python via Porcupine (subprocess) or a calibrated detangle | D3 R-D3-2 |
| Failure mode | "About 4 % wrong generated tests, mostly negatives, …" | "About 4 % wrong tests *as measured against one oracle*. The over-strict share where records leave behaviour open is unbounded until multiple wheats screen it" | D1 Q2 inference |
| Failure mode | "Weaker cross-form conflict detection than Pipeline B (*Inference*)." | "Weaker cross-form conflict detection than Pipeline B, partly recovered by G4a (*Inference*)" | D4 Q3 |
| Failure mode (new) | — | "Wheats or chaffs themselves wrong; curation cost grows with the allowed-variant space" | Forge §7.3; Making Hay; Programming 2024 |
| Small trial (add) | — | Over-strict checks flagged by one wheat vs by several wheats (the ICER 2018 contrast on an API operation) | D1-R1 overturn test |

**Pipeline B (common-logic consistency core).**

| Item | Old (verbatim) | New | Reason / ID |
|---|---|---|---|
| Step 6 | "G4 conjunction with unsat cores in k-subsets, then rt-consistency/realizability with environment actions as inputs, plus well-separation." | "G4 conjunction with unsat cores; **G4a–G4c per edit**; **G4d nightly**" | D4 Q3 |
| Failure mode | "Connected requirements, for example via mode variables, defeat partitioning, so full runs take hours." | "Mode variables defeat variable-sharing partitions of *full* runs (G4d, nightly, hours). The one-step G4a stays per operation and takes seconds. New failure mode: spurious G4a counterexamples from unreachable Inv-states, triaged by G4c" | Gacek; ProB; own trial; D4 Q3.2 |
| Failure mode (new) | — | "Unknown results under quantified global invariants over handles. Slice per mode cell, then fall back to G4d" | D4-R2 overturn condition |

**Pipeline C (single executable source plus an independent check set).**

| Item | Old (verbatim) | New | Reason / ID |
|---|---|---|---|
| Step 1 | "One executable formal source per operation (R itself, Quint, or Lean; left open)." | "(a) Literal single source: **Dafny → Python**, pinned version, with a mandatory back-end DRT leg (Python vs C#/Java build, Hypothesis inputs). (b) Otherwise **C′**: Quint as the executable source, seeded `--mbt` traces replayed against a separately written Python R through the split `alpha`, with an owned ITF decoder. (c) Lean only where proofs about the model are wanted. **'R itself' dropped**, because it collapses into Pipeline A" | D3 R-D3-3 (strict reading, §5.5) |
| Step 2 | "Markdown prose and other models are **generated** from it." | Unchanged for (a) and (b). No Python tool generates prose or formal layers *from Python* | D3 Q3 |
| Steps 4–6 | Independent property set; expectation suite; N-version leg | **Unchanged and mandatory** | IronSpec; Fonseca; Sail; D3 R-D3-4 |
| G4a | — | Expressed as a contract query over the same signature. R is a witness response for the states it reaches, not a proof for all Inv-states | D4 Q3 |
| Failure mode | "A misreading in the single source propagates consistently into every generated layer; SpecTec can detect it only via the test suite." | **Confirmed** with three new full texts (IronSpec, Fonseca I1, Sail vs Spike) | D3 Q4 |
| Failure modes (new) | — | "Back-end miscompilation (Dafny: 9 soundness bugs, Python implicated); trace replay covers only simulator-reachable paths (Quint); young interop tooling (`itf-py` crash; `--mbt` labels experimental)" | ICST 2024; own trial 5 |

### 3.4 Verified Part 3 recommendations that change

| Rec | Old (verbatim, abbreviated) | New | Reason / ID |
|---|---|---|---|
| R1 | "Record-derived, spec-blind positive scenarios and negatives, drafted before the spec … | medium" | Unchanged confidence. Add "screened against ≥ 2 allowed-variant wheats before gating". Overturn condition extended per D1-R1 | D1 Q1–Q2 |
| R2 | "Use rejected options as negatives | inference (no source does this) | low" | Unchanged (confirmed unsourced). Add: rejected options as conceptual chaffs plus chaffs mined from failures. Operational overturn test (D1-R3) | D1 Q5 |
| R7 | "rt-consistency / realizability with environment actions, plus well-separation (G4) | … | low" | **medium** for one-step G4a. rt-consistency relabelled (high). Full realizability stays low | D4-R1, R3 |
| R12 | "F ↔ R bridges in both directions; reviewed `alpha`; full-state logging (G6)" | "… split `alpha` (reviewed observation relation, checked projection); full-state logging; relaxed checks also run unrelaxed". Confidence medium | D2-R1, R4 |
| R13 | "Expectation family: information-flow isolation + anchoring lint + …" | "Fresh record-only session + file-system read scope + lint as backup + …". Confidence low–medium | D5-R1, R2 |
| R15 | "Allowed-variant check with a NonDex-style perturbing R" | "… or ≥ 2 independently built wheats; report RejectLegal with DetectFault". Confidence medium; the evidence base widens to ConVerTest and CodeContests+ (both TA) | D5-R3; D1-R1 |
| R21 | "Porcupine-style history check of R against its sequential mode" | Add the Python route (subprocess Porcupine or calibrated detangle) | D3 R-D3-2 |
| P-C | "Pipeline C as a candidate" | Literal form = Dafny → Python with back-end DRT; practical form = C′ (Quint). Confidence low–medium | D3 R-D3-3 |

---

## §4 Open questions and verification debt

**Updates to the verified edition's §5 open questions.**

| Verified item (verbatim) | Status now |
|---|---|
| "4. How many witnesses are needed, and how different must they be?" | **Still open.** ICER 2019's guarantee is conditional on wheats that "completely exercise" the underspecified space, and no study quantifies it (D1 Q1). For interleavings, the count may grow quickly (*Inference*) |
| "5. Realizability checking has not been applied to a library or storage API." | **Unchanged.** Nearest: Event-B file-system model FMCH02; Cosmos DB client spec without a response-existence check |
| "13. No refinement-check bridge has been measured; no Alloy/Lean ↔ Python bridge evidence was found." | **Partly addressed by analogy** (IronFleet, Armada, seL4, ShardStore). No F ↔ Python bridge is measured. No Lean–Python interop precedent exists |
| "14. Common-mode error when one LLM writes both spec and tests from the same prose is unmeasured …" | **Unchanged** for spec → test. Code → test common mode is now measured: isolation helps but leaves ~75 % of hard faults |
| "16. Over-strictness of LLM-written acceptance tests has not been measured." | **Narrowed** to acceptance-level and stateful-API tests (ConVerTest covers unit tests) |
| "17. No neutral benchmark of history checkers (Porcupine, Knossos, OmniLink) was found." | **Extended**: none for Python checkers either (detangle, c3py) |

**New open questions.**
1. Replicate Cunha & Macedo on the temporal Alloy4Fun exercises (Trash, Train) and compare with μAlloyτ's 90.8 %. This is the single most useful new measurement (D1-R6).
2. Wheat/chaff validation of a stateful API spec, a Hypothesis state machine, Quint `run` tests or TLA+ trace examples. None has been measured.
3. Rate of abstraction-function bugs in test-based bridges. No source counts it. Rate of false passes from agent-written state projections.
4. False-alarm rate of invariant-relative one-step checks (unreachable counterexample states) on realistic specs. Yield of G4b/G4c. Behaviour under quantified invariants over handle collections.
5. Agents writing the invariant Inv that G4a needs, or repairing G4a failures. Not searched specifically; none recorded.
6. Effect of OS or sandbox read scopes, as opposed to fresh prompts, on expectation-test independence.
7. Measured precision of any detector for SUT- or reference-computed expected values.
8. Fidelity, readability and performance of Dafny-generated Python. Systematic vs incidental Quint `--mbt` label defects.
9. A same-fault comparison of single-source vs separately authored layers.

**Verification debt from this run.**

| Item | Track | Status |
|---|---|---|
| Hughes, "Experiences with QuickCheck" (verified debt: [unreachable]) | D2 | **Resolved**: read in full, B |
| CrossHair, deal (verified debt: not attempted) | D3 | Docs read; own trials; **no effectiveness data exists** |
| Ravi & Coblenz OOPSLA 2025 | D3 | [unreachable] (ACM 403); artifact README only; n from a search extract |
| Wrenn dissertation (Brown 2022) | D1 | Not located |
| Alloy4Fun hint generation FM 2024; temporal repair SEFM 2022 | D1 | Search leads only; not read |
| Damas et al. TSE 2005 | D1 | Download failed |
| Misuse-case test-generation papers (Limerick, Boise State) | D1 | Listings only |
| Ashok Kumar & Lan (AAAI AI4ED workshop) | D1 | Abstract only |
| Venues of arXiv 2511.19177, 2411.10455 | D1 | Not verified |
| Gerdes, Hughes, Smallbone & Wang, Erlang Workshop 2015 | D2 | Manuscript link 404 |
| Fonseca tool-bug count (Figure 3: 3; §6 text: 4) | D2 | Unresolved |
| Cedar Rust→Lean value conversion in the DRT harness | D2 | Not described in the text read |
| ICST 2024 bug table: Python rows' categories | D3 | pdftotext alignment; re-check against the PDF |
| fuzz-d MEng report (4 Python miscompilations, extract) | D3 | Not read |
| elle-cli; ISSTA 2022 and ICST 2025 full texts | D3 | Lead only / partial |
| Dafny → Python, Lean, P runs | D3 | Not run (no dotnet, no elan, release downloads unavailable) |
| Post, Hoenicke, Podelski FASE 2011 (rt-inconsistency definition) | D4 | [unreachable] (empty file) |
| de Alfaro & Henzinger, Interface automata | D4 | [unreachable] |
| VDM implementability PO; Event-B FIS general form | D4 | Search extracts only |
| Newer Hanfor/ReqAnalyzer versions with an input/output split | D4 | Not checked |
| Damchoom & Butler flash filestore (Rodin proof statistics) | D4 | Not counted |
| TSL modulo theories venue (FoSSaCS 2022) | D4 | Search extract only |
| AgentLeak; SAGA beyond introduction; Kaufman beyond introduction; LLM smell-detection papers; TraceLLM; Dagger (ASE 2026) | D5 | Lead or partial |
| SAGA (NeurIPS 2025) and CodeContests+ (EMNLP 2025 Findings) venues | D5 | Semantic Scholar only |
| Count of retained tasks in Konstantinou, Tambon & Papadakis | D5 | Not found in the text |

---

## §5 Self-check and limits

### 5.1 Recommendations: confidence, load-bearing sources, overturn finding

No recommendation rests on *direct* evidence of effectiveness for library or API behaviour specs. "Own trial" support is illustrative only.

| # | Recommendation | Confidence | Load-bearing sources | One finding that would overturn it |
|---|---|---|---|---|
| D1-R1 | Screen the record-derived check set against ≥ 2 allowed-variant R wheats that differ on every unspecified and not-promised item. Repair or discard any check failing a wheat | medium | ICER 2018; ICER 2019 §3, §9; Cunha & Macedo "Valid" metric | A stateful or nondeterministic setting where single-wheat screening flags as many over-strict checks as multi-wheat screening |
| D1-R2 | Against R, write semi-specified outputs as membership predicates. Keep "one positive per allowed outcome" for satisfiability checks against the spec | medium | Koli 2021; relational-PBT papers; ICER 2019 §9 | Concrete per-outcome examples against a deterministic R yielding few false alarms |
| D1-R3 | Conceptual chaffs: one per rejected option and per plausible clause misreading. Each must be killed. Mine failures for unanticipated chaffs | low–medium | ICER 2019 §3.2; Making Hay; Programming 2024; QSM | Rejected-option chaffs killed only by checks that also kill positive-scenario mutants (verified R2 overturn condition) |
| D1-R4 | Validate the validators: review wheats for over-constraint; run each chaff against the positive checks; keep a critique channel | medium | Forge OOPSLA 2024 §7.3; Making Hay §5 | Wheat and chaff errors shown to be negligible |
| D1-R5 | For temporal or ordering clauses, prefer candidate differencing with classified distinguishing traces. Budget many more cases | low–medium | PICK; Greenman FM 2024; μAlloyτ; narrowing | A temporal replication of Cunha & Macedo reaching ≥ 88 % with ≤ 6 spec-blind tests |
| D1-R6 | Run the Cunha & Macedo protocol on Trash/Train vs μAlloyτ | high (as a measurement) | Cunha & Macedo future work; μAlloyτ benchmark | — |
| D2-R1 | Split `alpha` into a reviewed, versioned observation relation (clause-ID linked) and an untrusted, checked projection | medium | IronFleet; Armada; ShardStore | A test-based study where defects concentrate in the trusted observation relation itself |
| D2-R2 | Treat agent-written `alpha` as code under test: per-action statistics; non-projected-field R mutants; anti-identity check | medium–low | Hughes (B); Fonseca; VeriStruct; SysMoBench | Agent-written projections shown to have false-pass rates no higher than human ones without these checks |
| D2-R3 | Compare by membership in allowed outcomes wherever S leaves choices open | high (theory) / medium (practice) | Abadi & Lamport; Cirstea; ShardStore | Membership checks hiding more bugs than they prevent (Cirstea's imprecise-log risk) |
| D2-R4 | Run relaxed comparisons also unrelaxed; log R's full state | high | ShardStore; Cirstea; CCF | Full-state logging making validation infeasible for a Python R |
| D2-R5 | Do not make "reviewed `alpha`" the single priority. Give equal weight to the environment/fault model, logging and spec strength | medium | Fonseca (ind); IronSpec; TraceLink (verified) | A test-based bridge study where `alpha` errors are most false passes |
| D2-R6 | Assert R's invariant before calling `alpha` | medium | Lamport & Merz; seL4 | None found |
| R-D3-1 | Pipeline A G6 stack: Hypothesis state machine; icontract or deal contracts; CrossHair advisory only | medium–high (Hypothesis); low (CrossHair beyond advisory) | Ravi & Coblenz (README); ECOOP 2020; own trials 1, 3; PyPI/git | Python stateful PBT missing most seeded clause misreadings that example tests catch, at equal test counts |
| R-D3-2 | Histories: Porcupine via subprocess, or detangle after seeded-history calibration | medium | Verified Porcupine row; detangle PyPI; own trial 4 | detangle disagreeing with Porcupine on a shared corpus, or a benchmarked Python checker appearing |
| R-D3-3 | Pipeline C: Dafny → Python with back-end DRT if a literal single source is required; otherwise Quint C′; drop "R itself" | low–medium | ICST 2024; Dafny Python guide; own trial 5; Cedar FFI README, AWS blog | Dafny → Python miscompilations negligible on the operation's feature subset, or generated Python too slow or unreadable; Quint label defects proving systematic |
| R-D3-4 | Keep Pipeline C's independent, differently structured property set mandatory | medium | IronSpec; Fonseca; Sail vs Spike | Round-trip diffs alone catching as many seeded misreadings as an independent property set |
| D4-R1 | G4a: per-operation response existence relative to an inductive Inv as the primary ∀∃ gate | medium | Gacek NFM 2015; Hallerstede & Leuschel; own trial | Most G4a failures spurious on a realistic store API, or G4a missing conflicts that full realizability finds in the safety fragment |
| D4-R2 | Decompose by environment move, slice by mode predicate; never partition by shared variables | medium | Quantifier structure (*Inference*); ProB; FRET FM 2021; own trial | Per-operation queries timing out or returning unknown even when sliced (e.g. global quantified invariants) |
| D4-R3 | Relabel rt-consistency as timing consistency | high | RE 2019 definition and future-work sentence | A later ReqAnalyzer/Hanfor version with an input/output split |
| D4-R4 | Add G4b (environment actions preserve Inv) and G4c (bounded confirmation) | low–medium | Event-B INV/DLF practice; ProB "not necessarily reachable" | G4b/G4c adding no findings beyond G4a plus G6 |
| D4-R5 | Enumerate finite response tags; quantify only data-valued outputs | low | Own trial only | Repeated trials showing no difference, or enumeration blow-up |
| D5-R1 | Expectation tests in a fresh session that holds only the records | medium | Konstantinou, Tambon & Papadakis (A-pre, single source); Huang ICSE 2026; AgentCoder (TA, confounded) | A spec-level trial where fresh-session tests kill no more seeded spec misreadings than same-session tests |
| D5-R2 | File-system read scope; static import ban and runtime guard as backup | medium (mechanism) / low (effect) | Own trials F1.9, F2.4; PyNose; tsDetect/JNose; Canedo (verified) | Agents under a read scope reproducing R's specific choices at the same rate as agents with access |
| D5-R3 | Allowed-variant filter on expectation tests; report RejectLegal with DetectFault | medium | ConVerTest; CodeContests+; NonDex (verified); Liang survey | Variant failures dominated by variants that break other clauses |
| D5-R4 | Require decision/scenario citations; reject uncited or unknown-ID assertions; a valid citation is not evidence of no added commitment | low–medium | Panda (circular); Jin & Chen; Kaufman et al. | Real LLM added commitments mostly citing the correct decision, making the check near-useless |
| D5-R5 | Do not use test-smell detectors as independence evidence | high | PyNose rule definition; TOSEM evaluation | A detector release with a validated rule for reference-computed expected values |

### 5.2 Coverage gaps: sub-questions carried by one source

| Sub-question | Single source |
|---|---|
| Spec-blind NL → test generation against wrong specs | Cunha & Macedo |
| Multi-wheat screening benefit | Brown PLT group only, all TA |
| Distinguishing-trace classification for LTL | PICK (TA, historical controls) |
| Temporal mutation-test detection on real faults | μAlloyτ |
| Defects concentrate at the trusted interface (verified systems) | Fonseca (only independent source) |
| Mapping errors as a named trace-validation failure cause | CCF |
| LLM trivial-abstraction failure | VeriStruct |
| Python PBT effectiveness | Ravi & Coblenz, via README only |
| Lean performance as oracle | AWS blog (C, V) |
| Python-back-end Dafny bug list | ICST 2024 |
| rt-consistency lacks an input/output split | RE 2019 |
| Mode-sliced one-step check at tens-of-operations scale | ProB/Bosch (TA) |
| Plain consistency misses response-existence conflicts in a contract tool | Gacek (Kind 2 report is the same research line); own trial |
| Fresh-context vs same-conversation effect | Konstantinou, Tambon & Papadakis |
| Added commitments as 28 % of invalid tests | ConVerTest (n = 100, TA) |
| Anchoring concept | Canedo (A-pre, one system) |

### 5.3 Source-independence flags

| Flag | Sources |
|---|---|
| **TA** | All Brown PLT papers (Examplar, Forge, Making Hay, conceptual mutation, relational PBT, PICK); Cunha & Macedo narrowing; μAlloyτ; QSM; IronFleet, Armada, Verdi, seL4; Cirstea (TLC maintainers); IronSpec; SysMoBench harness; VeriStruct; Hughes (QuickCheck); CrossHair, deal, detangle, c3py docs; MacIver & Donaldson and the JOSS paper (Hypothesis author); Dafny fuzzing (ICST 2024, CompFuzzCI); Gacek, Kind 2, Hallerstede & Leuschel, RE 2019, Boolean abstraction, TSL-MT, Electrum, FRET, CoCoSpec; AgentCoder; PyNose; ConVerTest; CodeContests+; Panda |
| **V** | ShardStore (Amazon); Cedar FSE paper, cedar-lean-ffi and AWS Lean blog; CCF (Microsoft); AWS 2014 report; Cosmos DB (Microsoft co-authors); Dafny integration docs; Irfan ISSTA 2022 (Amazon authors); P and PObserve (AWS-led); Forge docs |
| **CB** | SAGA (competing verifier/benchmark) |
| **Mild interest** | Huang et al. ICSE 2026 (same group as AgentCoder, not flagged TA by D5; a stricter reading would flag it) |
| **Independent** | Fonseca et al.; Sail-RISC-V vs Spike (independent of the Sail authors); Ravi & Coblenz; Ouédraogo et al. (third-party evaluation of both detectors); Konstantinou, Tambon & Papadakis; Leinonen et al. (independent of Brown) |

**Consequence** (*Inference*):
- Every efficacy figure for wheat/chaff validation and for one-step response-existence checks is tool-author-reported.
- The only independent evidence bearing on `alpha` and single-source risk is Fonseca, plus the 2-page Sail paper.

### 5.4 What this run did not do

The synthesis ran no new searches, fetched no sources and ran no trials. It did not run git commands.

All own-trial figures come from the track notes:
- D3: CrossHair, deal, Hypothesis, detangle, Quint;
- D4: Z3;
- D5: import guard, lint.

Each is an n = 1 toy, or a small synthetic set written by the same run that interpreted it.

The tracks did not do the following:
- **D1**: did not read Wrenn's dissertation, the Alloy4Fun platform papers, FM 2024/SEFM 2022, the misuse-case studies or Damas TSE 2005. It ran no wheat/chaff trial on a Hypothesis state machine.
- **D2**: did not re-read MongoDB, TraceLink, Mocket or Quint Connect. It found no Apalache or TLC refinement case study with effort or defect data, and ran no trial of an incomplete `alpha`.
- **D3**: did not run Dafny → Python, Lean or P, or measure generated-code performance. GitHub API data (stars, issues) was unavailable. It found no agent measurements for any Python tool.
- **D4**: did not run TLC, Apalache, ProB or Kind 2. It did not research machine closure or Spectra with data, and did not search for LLM studies on these checks.
- **D5**: did not run tsDetect or PyNose on LLM tests. It found no read-scope or spec → test study.

The earlier T1–T5 notes and the verified V1–V5 notes were not re-read line by line. The verified edition's text was used as the baseline, and every quoted baseline sentence was checked against it.

### 5.5 Self-check: possible misreadings of the brief or a source

1. **D3's strict reading of "single executable source".** D3 takes the phrase to mean R is generated from, or is, the source. If the brief means one *formal* source with a separately written Python R, then Quint and Lean are full Pipeline C and the "C′" relabelling and dropping "R itself" overstate the change (§3.3).
2. **D4's read-only git commands.** The D4 track ran `git status --short` and `git branch --show-current`, contrary to its instruction not to run git commands. Nothing was changed. This synthesis ran none.
3. **D1's garbled PDF figures.** Making Hay's "17 / 11" misconceptions and Fig. 2 counts (16/9, 1/2, 6/3) came from a garbled two-column extraction reconciled with layout text; a transposition is possible. The ICST 2024 Python rows (D3) and Fonseca's 3-vs-4 tool bugs (D2) have similar extraction or consistency caveats.
4. **D1 framing.** Calling Cunha & Macedo a "single-wheat design" is D1's *Inference*. The paper uses the oracle to *measure* validity, not as a deployed component. ICER 2018's Table 2 header reads "% of Student Test Suites Incorporated", read as "trusted". PICK's 56 % vs 43–44 % uses historical controls with different formats. μAlloyτ's 90.8 % is pooled and 87.24 % is the mean per exercise.
5. **D1 brief reading.** "Alloy4Fun follow-ups" was read as Cunha & Macedo's follow-ups, not the Alloy4Fun platform papers (unread). Non-Brown "all-bugs" grading studies were not surveyed.
6. **D2 scope.** Output-comparison practice (Cedar, Knossos) was included under "abstraction function" for the observational-equivalence question. IronSpec's subset-of-fields bugs are contract weakness, used for "hidden state outside `alpha`" by analogy. SysMoBench maps names, not state. "Proof-based refinement cannot cause false passes" is D2's reasoning, not a source's words.
7. **D3 sources.** Ravi & Coblenz is unread in full, and its "more effective per test" may depend on normalisation. CrossHair's `measured.json` colour semantics were inferred. The empty Quint `actionTaken` may be misuse. Not all Sail deviations are verified Sail bugs.
8. **D4 readings.** RE 2019's future-work sentence ties the input/output split to completeness analysis. The conclusion that rt-consistency lacks the split rests on the definition, and FASE 2011 was unread. Gacek's "depth ≤ 1" describes 20 contracts only. Hallerstede & Leuschel's DLF is global deadlock freedom, and its use as per-operation FIS is a transfer. G4a is a reframing valid for safety contracts with an inductive Inv, not for timeout or termination forms.
9. **D5 readings.** Measured isolation withholds *code*. Mapping code to R is fair; mapping it to the spec or formal models is *Inference*. F1.1's +11.7 % and 25 %/14 % may come from different comparisons, and relative vs absolute percentages are unstated. ConVerTest's "precision" is the validity of kept tests, not detector precision on added commitments. CodeContests+ TPR failures mix wrong tests with missing multi-solution checkers.
10. **This run's own risks.** The brief's §6.3 "earlier report" was read as the verified edition, per the brief's own preference rule. D5's attribution of open question 16 to "§3" was corrected to §5 after checking. Where D1's and D5's variant mechanisms were merged (§2.6 #5), the merged gate (G8) has no single measured precedent. The new gates G4b and G4c have no measured yield at all.
11. **Transfer labels.** Hypothesis docs and the own trials on toy store operations were labelled *direct* for the *mechanism*. ShardStore, the closest store-like system, stays *analogous*, consistent with the verified edition's treatment of Cedar.

---

## §6 Sources with grades

New or newly read in this run. Sources graded in the verified edition and only re-cited here keep that edition's grade.

| Source | Grade | Full text | Agents | Indep. | Track |
|---|---|---|---|---|---|
| Wrenn & Krishnamurthi, Examplar, ICER 2019, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-examplar/paper.pdf) | A | yes | no | TA | D1 |
| Wrenn, Krishnamurthi & Fisler, ICER 2018, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/wkf-who-tests-testers/paper.pdf) | A | yes | no | TA | D1 |
| Nelson et al., Forge, OOPSLA 2024, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/ngp----forge/paper.pdf) | A | yes (testing, evaluation) | no | TA | D1 |
| Forge docs, [Testing](https://forge-fm.github.io/forge-documentation/latest/testing-chapter/testing/) | C | yes (fetch summary) | — | TA/V | D1 |
| Wrenn & Krishnamurthi, Koli Calling 2020, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-stud-write-test-no-coercion/paper.pdf) | A (short) | yes | no | TA | D1 |
| Wrenn & Krishnamurthi, Koli Calling 2021, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-examplar-unspecified/paper.pdf) | A | yes | no | TA | D1 |
| Prasad et al., Making Hay, Koli Calling 2022, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/pgnwk-making-hay-wheats/paper.pdf) | A | yes (garbled extraction) | no | TA | D1 |
| Prasad et al., conceptual mutation, Programming 8(2) 2024, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/pgnk-conceptual-examplar/paper.pdf) | A | yes (sections) | not used | TA | D1 |
| Wrenn, Nelson & Krishnamurthi, Programming 5(3), [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/wnk-use-rel-prob-pbt/paper.pdf) | A | partial | no | TA | D1 |
| Nelson et al., Programming 6(2) 2022, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/nrsdwk-auto-targ-test-pbt-pred/paper.pdf) | A | partial | no | TA | D1 |
| Cunha & Macedo, FM 2026, [arXiv 2510.23350](https://arxiv.org/abs/2510.23350) (re-read) | A | yes (scope, metrics) | yes | — | D1 |
| Cunha & Macedo, narrowing, [arXiv 2511.19177](https://arxiv.org/abs/2511.19177) | A-pre | yes | no | TA | D1 |
| Prasad, Austen, Fisler & Krishnamurthi, PICK, ECOOP 2026, [PDF](https://www.siddharthaprasad.com/papers/pafk-pick.pdf) | A | yes | yes (regex/ABAC) | TA | D1 |
| Greenman et al., FM 2024, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/gpdzdkmnz-miscon-finite-infinite-ltl/paper.pdf) | A | partial | no | partly TA | D1 |
| Jovanovic & Sullivan, μAlloyτ, MODELS 2023, [PDF](https://scopelabuta.github.io/files/Models2023-B.pdf) | A | yes (evaluation) | no | TA | D1 |
| Dupont et al., QSM, Applied AI 22 (2008), [PDF](https://webperso.info.ucl.ac.be/~pdupont/pdupont/pdf/QSM_AAI_08.pdf) | A | partial | no | TA | D1 |
| Leinonen et al., [arXiv 2411.10455](https://arxiv.org/abs/2411.10455) | A-pre | partial | yes | ind | D1 |
| Ashok Kumar & Lan, [arXiv 2402.07081](https://arxiv.org/abs/2402.07081) | A-workshop | abstract only (lead) | yes | — | D1 |
| Alloy4Fun FM 2024 / SEFM 2022, [FM24](https://haslab.github.io/SpecRep/pubs/FM24.pdf), [SEFM22](https://haslab.github.io/SpecRep/pubs/SEFM22.pdf) | — | no (leads) | — | TA | D1 |
| Practitioner ADR post, [DEV](https://dev.to/masondelan/record-why-an-approach-was-rejected-and-when-to-revisit-it-20op) | D | no | — | — | D1 |
| Hawblitzel et al., IronFleet, SOSP 2015, [PDF](https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf) | A | yes | no | TA | D2 |
| Lorch et al., Armada, PLDI 2020, [PDF](https://www.andrew.cmu.edu/user/bparno/papers/armada.pdf) | A | partial (refinement, TCB) | no | TA | D2 |
| Wilcox et al., Verdi, PLDI 2015, [PDF](https://homes.cs.washington.edu/~ztatlock/pubs/verdi-wilcox-pldi15.pdf) | A | TCB passage | no | TA | D2 |
| Klein et al., seL4, TOCS 2014, [PDF](https://trustworthy.systems/publications/nicta_full_text/7371.pdf) | A | relevant sections | no | TA | D2 |
| Bornholt et al., ShardStore, SOSP 2021, [PDF](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf) | A | yes (Amazon Science copy) | no | V/TA | D2 |
| Abadi & Lamport, existence of refinement mappings, [PDF](https://lamport.azurewebsites.net/pubs/abadi-existence.pdf) | A | yes (DEC SRC version) | n/a | — | D2 |
| Lamport & Merz, TOPLAS 2022, [PDF](https://lamport.azurewebsites.net/pubs/simple.pdf) | A | yes | n/a | — | D2 |
| Hughes, "Experiences with QuickCheck", LNCS 9600, [PDF](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quviq-testing.pdf) | B | yes | no | TA/V | D2 |
| Gerdes et al., Erlang Workshop 2015, [record](https://research-information.bris.ac.uk/en/publications/linking-unit-tests-and-properties/) | A-workshop | no (404) | no | TA | D2 |
| proptest book, qsm README, Knossos README ([1](https://raw.githubusercontent.com/proptest-rs/proptest/main/book/src/proptest/state-machine.md), [2](https://raw.githubusercontent.com/stevana/quickcheck-state-machine/master/README.md), [3](https://raw.githubusercontent.com/jepsen-io/knossos/master/README.md)) | B | yes | — | docs | D2 |
| Fonseca et al., EuroSys 2017, [PDF](https://homes.cs.washington.edu/~pfonseca/papers/eurosys2017-dsbugs.pdf) | A | yes | no | **ind** | D2, D3 |
| Goldweber et al., IronSpec, OSDI 2024, [USENIX](https://www.usenix.org/system/files/osdi24-goldweber.pdf) | A | yes | no | TA | D2, D3 |
| VeriStruct, TACAS 2026, [arXiv 2510.25015](https://arxiv.org/abs/2510.25015) | A | yes | yes | TA | D2 |
| AutoVerus, [arXiv 2409.13082](https://arxiv.org/abs/2409.13082) | A-pre | partial (not evidence here) | yes | TA | D2 |
| SysMoBench, Cedar FSE, Cirstea, CCF (re-read) | A | yes | as verified | as verified | D2 |
| PyPI JSON pages: [crosshair-tool](https://pypi.org/pypi/crosshair-tool/json), [deal](https://pypi.org/pypi/deal/json), [icontract](https://pypi.org/pypi/icontract/json), [icontract-hypothesis](https://pypi.org/pypi/icontract-hypothesis/json), [hypothesis](https://pypi.org/pypi/hypothesis/json), [hypothesis-crosshair](https://pypi.org/pypi/hypothesis-crosshair/json), [itf-py](https://pypi.org/pypi/itf-py/json), [DafnyRuntimePython](https://pypi.org/pypi/DafnyRuntimePython/json) | B | yes | — | V/TA | D3 |
| CrossHair [README](https://raw.githubusercontent.com/pschanely/CrossHair/main/README.md), [limitations](https://raw.githubusercontent.com/pschanely/CrossHair/main/doc/source/limitations.rst) | B | yes | — | TA | D3 |
| CrossHair [measured.json](https://raw.githubusercontent.com/pschanely/CrossHair/main/doc/source/measured.json) | C | yes | — | TA | D3 |
| deal [README](https://raw.githubusercontent.com/life4/deal/master/README.md), [verification](https://raw.githubusercontent.com/life4/deal/master/docs/basic/verification.md) | B | yes | — | TA | D3 |
| Ravi & Coblenz, OOPSLA 2025, [Crossref](https://api.crossref.org/works/10.1145/3764068); [artifact README](https://raw.githubusercontent.com/ucsd-salad/python-pbt-eval/main/README.md) | A venue / README B | **no** [unreachable] | no | ind | D3 |
| MacIver & Donaldson, ECOOP 2020, [PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf) | A | yes | no | TA | D3 |
| MacIver et al., Hypothesis, JOSS 2019, [PDF](https://www.theoj.org/joss-papers/joss.01891/10.21105.joss.01891.pdf) | B | yes | no | TA | D3 |
| detangle, [PyPI](https://pypi.org/pypi/detangle/json) | B | yes (description) | no | TA | D3 |
| c3py, [README](https://raw.githubusercontent.com/shumbo/c3py/main/README.md) | B | yes | no | TA | D3 |
| elle-cli, [repo](https://www.github.com/ligurio/elle-cli) | — | no (lead) | — | — | D3 |
| Dafny Python integration, [doc](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/integration-py/IntegrationPython.md) | B | yes | — | V | D3 |
| Donaldson, Sheth, Tristan & Usher, ICST 2024, [PDF](https://www.doc.ic.ac.uk/~afd/papers/2024/ICST.pdf) | A | yes | no | TA | D3 |
| Irfan et al., ISSTA 2022, [PDF](https://ahmed-irfan.github.io/papers/issta22.pdf) | A | partial | no | V | D3 |
| CompFuzzCI, ICST 2025 industry, [PDF](https://www.doc.ic.ac.uk/~afd/papers/2025/ICST-Industry.pdf) | A (industry) | partial | no | TA | D3 |
| cedar-lean-ffi, [README](https://raw.githubusercontent.com/cedar-policy/cedar-spec/main/cedar-lean-ffi/README.md); AWS Lean blog, [link](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/) | B; C | yes | no | V | D3 |
| Quint npm, [registry](https://registry.npmjs.org/@informalsystems/quint) | B | yes | — | V | D3 |
| P repo, [p-org/P](https://github.com/p-org/P); PObserve docs, [link](https://p-org.github.io/P/advanced/pobserve/pobserve/) | B | yes (source tree; fetch summary) | no | V | D3 |
| Schlägl, Ruep & Große, Sail-RISC-V vs Spike, RISC-V Summit Europe 2026, [PDF](https://ics.jku.at/files/2026RISC-V_Summit_Europe_RVVTS_SailRV_Spike.pdf) | B | yes | no | ind | D3 |
| Gacek et al., NFM 2015, [arXiv 1502.03005](https://arxiv.org/pdf/1502.03005) | A | yes | no | TA | D4 |
| Larraz & Tinelli, Kind 2 realizability, [arXiv 2205.09082](https://arxiv.org/pdf/2205.09082) | A-pre | yes | no | TA | D4 |
| Hallerstede & Leuschel, TPLP 11(4–5) 2011, [arXiv 1109.2015](https://arxiv.org/pdf/1109.2015) | A | yes | no | TA | D4 |
| Event-B wiki, [Feasibility POs](https://wiki.event-b.org/index.php/Revisiting_Feasibility_POs), [Flows](https://wiki.event-b.org/index.php/Flows_Plug-in) | B | yes | — | — | D4 |
| VDM slides, [PDF](https://www.di.uminho.pt/~jno/ps/vdm06sl.pdf) | — | no (lead) | — | — | D4 |
| Apalache manual, [features](https://raw.githubusercontent.com/apalache-mc/apalache/main/docs/src/apalache/features.md), [running](https://raw.githubusercontent.com/apalache-mc/apalache/main/docs/src/apalache/running.md), [invariants](https://raw.githubusercontent.com/apalache-mc/apalache/main/docs/src/apalache/principles/invariants.md) | B | yes | — | TA | D4 |
| TLC `ENABLED` thread, [discuss.tlapl.us](https://discuss.tlapl.us/msg04343.html) | C | yes (thread) | — | — | D4 |
| Newcombe et al., AWS 2014, [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) | B | yes | no | V | D4 |
| Hackett, Rowe, Kuppe, Cosmos DB, ICSE-SEIP 2023, [arXiv 2210.13661](https://arxiv.org/pdf/2210.13661) | A | yes | no | V | D4 |
| Langenfeld et al., RE 2019 (re-read), [PDF](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf) | A | yes | no | TA | D4 |
| Post & Podelski, GI 2011, [PDF](https://fb-swt.gi.de/fileadmin/FB/SWT/Softwaretechnik-Trends/Verzeichnis/Band_31_Heft_1/GI2011_Post.pdf); FASE 2011 [unreachable] | B; — | yes; no | no | — | D4 |
| Rodríguez & Sánchez, CAV 2023, [arXiv 2310.17292](https://arxiv.org/pdf/2310.17292) | A | yes | no | TA | D4 |
| Finkbeiner, Heim, Passing, TSL modulo theories, [arXiv 2104.14988](https://arxiv.org/pdf/2104.14988) | A-pre | yes | no | TA | D4 |
| Macedo et al., Electrum, FSE 2016, [PDF](https://perso.ens-lyon.fr/denis.kuperberg/papers/electrum.pdf) | A | yes | no | TA | D4 |
| de Alfaro & Henzinger, Interface automata, [record](https://research-explorer.ista.ac.at/record/4622) | — | no [unreachable] | — | — | D4 |
| Mavridou et al., FRET FM 2021 (re-read), [NTRS](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf) | A | yes | no | TA | D4 |
| Champion et al., CoCoSpec, SEFM 2016, [PDF](https://homepage.cs.uiowa.edu/~tinelli/classes/5810/Fall20/Papers/Cham16.pdf) | A | yes | no | TA | D4 |
| Konstantinou, Tambon & Papadakis, [arXiv 2607.05139](https://arxiv.org/abs/2607.05139) | A-pre | yes | yes | — | D5 |
| Huang, Zhang, Harman, Du, Cui, ICSE 2026, [arXiv 2409.09464](https://arxiv.org/abs/2409.09464) | A | yes | yes | mild interest | D5 |
| Huang et al., AgentCoder, [arXiv 2312.13010](https://arxiv.org/abs/2312.13010) | A-pre | yes | yes | TA | D5 |
| Ma & Eisty, [arXiv 2607.10277](https://arxiv.org/abs/2607.10277) | A-pre (pilot) | yes | yes | — | D5 |
| Ma et al., SAGA, [arXiv 2507.06920](https://arxiv.org/abs/2507.06920) | A (venue per Semantic Scholar, unverified) | partial | yes | CB | D5 |
| Liang et al., survey, [arXiv 2610.05001](https://arxiv.org/abs/2610.05001) | A-pre | yes (sections) | n/a | — | D5 |
| AgentLeak, [arXiv 2602.11510](https://arxiv.org/abs/2602.11510) | B (lead) | no | yes | — | D5 |
| Gabor, Lynch, Rosenfeld, EvilGenie, [arXiv 2511.21654](https://arxiv.org/abs/2511.21654) | A-pre | yes (method, ambiguity) | yes | — | D5 |
| Wang et al., PyNose, ASE 2021, [arXiv 2108.04639](https://arxiv.org/abs/2108.04639) | A | yes | no | TA | D5 |
| Ouédraogo et al., TOSEM, [arXiv 2410.10628](https://arxiv.org/abs/2410.10628) | A | yes (validation) | yes (LLM tests) | ind | D5 |
| Tautological-test practitioner material, [perch issue](https://github.com/lakeday-org/perch/issues/187); [arXiv 2111.02317](https://arxiv.org/pdf/2111.02317) | C/D | no | — | — | D5 |
| Taherkhani et al., ConVerTest, ICST 2026, [arXiv 2602.10522](https://arxiv.org/abs/2602.10522) | A | yes | yes | TA | D5 |
| Wang et al., CodeContests+, [arXiv 2506.05817](https://arxiv.org/abs/2506.05817) | A (venue per Semantic Scholar) | yes (§4) | yes | TA | D5 |
| Panda, Citation Discipline, [arXiv 2606.30689](https://arxiv.org/abs/2606.30689) | A-pre (low weight) | yes | yes | TA | D5 |
| Jin & Chen, ASE journal 2026, [arXiv 2603.00539](https://arxiv.org/abs/2603.00539) | A | partial in D5 (verified: yes) | yes | — | D5 |
| Kaufman, Brun, Murali, Endres, [arXiv 2607.08885](https://arxiv.org/abs/2607.08885) | A-pre | abstract + introduction | human judges of LLM output | — | D5 |
| Own trials (D3: CrossHair, deal, Hypothesis, detangle, Quint; D4: Z3 synthetic store API; D5: import guard, anchoring lint) | own trial | n/a (scripts in the scratchpad) | not measured | written and interpreted by the same run | D3–D5 |
