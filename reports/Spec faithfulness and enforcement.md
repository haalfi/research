# Prove the spec wrong before building on it

Grades follow brief §6: A, A-pre, A-workshop, B, C, D. **[unreachable]** means the full text was not fetched, so the item is a lead only. *Inference* marks reasoning that is not itself a finding of any source. Every method states whether **agents** (LLMs) were measured doing that step. If they were not, it says "human-only evidence". Measured figures give n, setting, and what "correct" meant. This report does not rest on any earlier report. The brief §3 baseline is taken as given, and where the notes found new full-text evidence against a §3 point, the text says so and flags it **[§3 challenge]** or **[§3 qualification]**.

---

## 1. Kernsatz

No published pipeline runs prose records → spec → formal models → executable reference model with gates that check faithfulness *to the prose*; the best-supported way to build one turns each record's own scenarios and rejected options into spec-blind positive and negative checks before the spec exists, conjoins all normative forms over one shared vocabulary to check conflicts, vacuity and satisfiability over all environment moves, and binds the reference model with two test families whose independence is enforced by information flow and verified by per-family mutant kills plus an allowed-variant check. Every reference-free faithfulness check found (round-trip, dual formalization, LLM judges, compile/verify) is necessary-only and blind to shared misreadings, and LLM errors are correlated across models, so independence must come from the derivation path and the artefact rather than from swapping models. The central claim, that prose-derived oracles catch spec misreadings that spec-derived ones miss, remains unmeasured, and a small trial on one operation can measure it directly.

---

## 2. Findings per track

### 2.1 T1 Faithfulness: prose → spec, proved wrong early

**Core finding.** Round-trip and dual formalization catch *divergent* readings. By construction they miss *shared* misreadings, and every full-text source that discusses the point says so. The strongest measured mechanism that needs no gold formula has three steps: derive concrete positive and negative examples from the NL source without seeing the spec, then require the spec to accept the positives and refuse the negatives. In the one measured study this caught about 90% of wrong specs with three tests of each kind ([Cunha & Macedo](https://arxiv.org/abs/2510.23350)). Exhibition (traces, instances, witnesses) works when it is *targeted*. Browsing what a spec allows rarely reveals what it wrongly forbids ([Jovanovic & Sullivan](https://par.nsf.gov/servlets/purl/10615156)).

| Option | Evidence (grade; n, setting, "correct") | Catches | Misses | Cost | Agents |
|---|---|---|---|---|---|
| **Round-trip**: formalize → back-translate → re-formalize → equivalence check | Amrollahi, Lopez, Barrett (A-pre). 227 Texas statutes, many-sorted FOL, Z3. Equivalence was 44.7–67.1% before repair and 78.9–85.7% after a K=3 diagnose-and-repair loop (90.7%/94.7% when one provider generated and another diagnosed). "Correct" meant Z3 equivalence of the two encodings, which the authors call necessary, not sufficient. Human audit: 1 annotator, 25 rules, 1 minor error among 14 equivalent rules vs 3 among 11 non-equivalent. 26 rules were never repaired ([source](https://arxiv.org/abs/2604.25031)) | Divergent readings between the two legs | Omissions shared by both legs ("if T1 drops a conjunct and T3 reproduces the omission, the check passes"); stable but wrong fixed points; exception clauses and compound conditions | 7.2 LLM calls per repair (vs 19.9 to regenerate) | Measured |
| **Equivalence against a second formalization** | Poiroux et al., EMNLP 2025 (A). 3,752 Lean pairs with human semantic-equivalence labels. Against those labels, BEq+ had precision 98.0 and recall 48.3; BEqL precision 100 and recall 30.9. Type-check rate "can not be used as a substitute for human evaluation" ([source](https://arxiv.org/abs/2406.07222)) | Proven equivalence is strong evidence of *agreement* | About half of true equivalences go unproven, so "not proven equivalent" says little | Low once both formalizations exist | Measured |
| **Independent dual human formalization** | Easterbrook & Callahan, RE'97 (A). Four people translated one NASA FDIR requirement into AND/OR tables and produced **four different tables**. Comparing tables was "much easier" than comparing prose. n = 4, 1 requirement, no statistics ([source](https://ntrs.nasa.gov/api/citations/19970007163/downloads/19970007163.pdf)) | Ambiguity, located row by row | Shared errors (the Saarland complementary-spec report makes this point but is [unreachable]) | One extra formalization | Human-only evidence |
| **Multiple generators + difference witnesses + judge** | NeuroSTAR (A-pre). Several LLMs generate LTLf; DFA difference automata yield traces on which the candidates disagree; an LLM panel judges the traces. 87.8% vs 86.2% (n-shot) equivalence to gold on ConfoNLf. Reference-free study on 108 driving-law sections: 89/106 (83.9%) shortest violating traces judged valid by two authors, a necessary condition only ([source](https://arxiv.org/abs/2609.03161)) | Divergence, shown as a concrete case that can be checked against prose | Agreement when "they might be wrong together"; missing proposition vocabulary | Several generations + automata | Measured (judge panel's own precision not reported) |
| **Paraphrase / explanation review** | FRET's generated English, diagrams and simulator were "instrumental" in the Lockheed Martin case study (A) ([source](https://ntrs.nasa.gov/citations/20205000433)). Humans misread formal text: in four rounds including experts, LTL→English was 15–24% wrong and English→LTL 28–47% wrong, judged by semantic equality ([Greenman et al., A](https://arxiv.org/abs/2211.01677)) | Misreadings visible to a reader | Errors the reader shares; operator misconceptions (weak-until, implicit G/F) | Human minutes per requirement | Human-only evidence |
| **Structured intermediate + mechanical translation** | Req2LTL, ASE 2025 (A). An LLM decomposes into a tree IR, then deterministic rules produce LTL. On 112 industrial aerospace requirements: 88.4% vs 65.2% (NL2TL), 56.3% (nl2spec), 55.4% (NL2LTL), 43.8% zero-shot. "Correct" is inconsistently defined (exact match vs two-expert judgement), and no equivalence checker was used. With a diagram view, engineers fixed 13/112 wrong formulas in about 10 min ([source](https://arxiv.org/abs/2512.17334)). FRET case study: 69/74 requirements captured, and rewriting into FRETish "not always straightforward" (A) ([source](https://ntrs.nasa.gov/citations/20205000433)) | Temporal and conditional confusion, lost nesting, binding errors | Residual ambiguity and context omission | Template training (Großer et al.: substantial; abstract only) | Measured (Req2LTL); FRET human-only |
| **Example tables next to prose** | Ricca et al., IWPSE 2007 (A-workshop). n = 15 students, 6 requirements; answers about requirements were more often correct with Fit tables (p = 7.5e-05), no significant time cost ([source](https://profs.scienze.univr.it/ceccato/papers/2007/iwpse2007.pdf)) | Comprehension errors | Not a faithfulness check of a formalization | Low | Human-only evidence |
| **Targeted exhibition** (simulation, instances, witnesses) | FRET's simulator exposed a trigger-vs-always misreading in AP-003c on a two-step trace (A, no counts). Alloy4Fun, over 93,000 submissions: 25.4% correct, 45.3% semantically faulty, 23.28% both over- and under-constrained. Authors: an absent expected scenario among "hundreds" is hard to notice (A) ([source](https://par.nsf.gov/servlets/purl/10615156)). Quint `--witnesses` and a negated witness used as an invariant give concrete traces (B, no error-rate data) ([source](https://quint.sh/docs/checking-properties)) | Under-constraint (an unexpected scenario appears) | Over-constraint when browsing untargeted | Low per trace | Human-only evidence |
| **Spec-blind positive/negative tests from NL, before the spec** | Cunha & Macedo (A-pre). From NL plus domain model, without seeing a spec, an LLM writes N positive and N negative Alloy runs. 43 requirements, 28–848 (mean 157) known-wrong human specs per requirement. Wrong-spec detection about 62% at N=1, 83% at N=2, 90% at N=3, 93.6% at N=5. 3.9% of tests were wrong (30/774), more often the negatives. Valid-test rate at N=3 varied from 67% to 96% across four models. About $3.5 per 258 tests ([source](https://arxiv.org/abs/2510.23350)) | Both lost cases (positives fail) and missing constraints (negatives pass), against *real* human errors | Requirements ambiguous to humans; structural and educational models only | Cheap | Measured |
| **Concrete-I/O soundness + completeness of a spec** | Lahiri, FMCAD 2024 (A). On MBPP-DFY, 64 of 153 specs analysable. Correctness = spec admits the reference output; completeness = spec rejects mutated outputs; a threshold of about 0.66 separated strong from weak specs. Found specs weaker than labelled, one misread intent, and test transcription errors (25 vs 125) ([source](https://arxiv.org/abs/2406.09757)) | Weak specs (⇒ where ⇔ was needed); misreadings | Depends on test quality | 400-line script | Measured (LLM-written specs included) |
| **LLM judge of NL↔formal alignment** | FormalAlign (A per T1; venue not verified per T5). Human experts matched ground truth 79.58% of the time, the trained scorer 65.00%. An LLM judge had **26–51% precision at 88–95% recall**, i.e. it over-accepts. Humans took about 3 h per 80 pairs ([source](https://arxiv.org/abs/2410.10135)). Beyond Compilation (A-pre): 227 NL→Lean statements, 8 systems. Accept only when two judges from different families agree; this matched the human majority on 91.5% of audited cases, and compilation overstated faithfulness by 1.3–29.5 points ([source](https://arxiv.org/pdf/2606.31002)) | Gross misalignment | Shared readings; judge aging (see §2.5) | Low per item | Measured (maths domain only) |

**Clause-level "says more / says less".** "Says more" (an added commitment) is over-constraint and "says less" (a lost case) is under-constraint. Over-constraint is the harder one to spot by inspection ([Jovanovic & Sullivan](https://par.nsf.gov/servlets/purl/10615156)). Humans make exactly these operator-level errors as "ImplicitG/ImplicitF" misconceptions ([Greenman et al.](https://arxiv.org/abs/2211.01677)). *Inference*: four record-derived checks follow. None is measured as such; each is the nearest analogue of a measured mechanism.

1. **Scenario derivability**: each record scenario's outcome must be permitted by the clause, and entailed where the decision commits. Analogue: Cunha & Macedo positives; Lahiri soundness.
2. **Rejected-option refutation**: the distinguishing behaviour of each rejected option must be refused. Analogue: negatives; mutant rejection.
3. **Added-commitment probe**: generate the minimal behaviour a clause forbids (shortest violating trace, Alloy UNSAT core, failing Dafny assertion) and ask a spec-blind judge whether the record forbids it. Analogue: NeuroSTAR, where 17/106 law sections failed.
4. **Non-commitment typing**: an *unspecified* set needs one positive per allowed outcome and a negative outside the set. A *deliberately not promised* item needs two witnesses with different outcomes.

No source uses rejected alternatives as negatives; that mapping is *Inference*.

**Where a human must look.** Effective human checks in the sources were all made on small concrete artefacts: a sub-translation fragment (nl2spec: 15 of 20 initially wrong translations were fixed by editing fragments, at 1.86 loops on average; [source](https://arxiv.org/abs/2303.04864)), a two-step trace (FRET), a table row (Easterbrook), a formula-tree diagram (Req2LTL), and a shortest violating trace (NeuroSTAR). *Inference*: ask humans yes / no / "not addressed" questions on one concrete case tied to one record sentence. Route to them (a) unresolved difference witnesses, (b) every "not addressed" answer from the added-commitment probe (the brief's observed over-reach failure), and (c) a random audit of agent-judged witnesses.

**[§3 qualification] Clover triangulation.** "Triangular cross-checks help" needs a caveat. Agreement among legs that share a reading does not establish faithfulness, and the round-trip paper's own audit shows equivalence and faithfulness only loosely coupled (1/14 vs 3/11 minor errors, n = 25, single annotator) ([source](https://arxiv.org/abs/2604.25031)).

**What "correct" meant across autoformalization papers.** From weakest to strongest metric (*Inference*): syntax valid < exact match < equivalence to one gold < human intent judgement < detection of real errors. Gold sets are themselves unreliable. NeuroSTAR removed 48% of pooled benchmark data as ambiguous, wrong or trivial. Lahiri found transcription errors in the human reference. ProofNet# exists because ProofNet needed correction ([NeuroSTAR](https://arxiv.org/abs/2609.03161); [Lahiri](https://arxiv.org/abs/2406.09757); [Poiroux](https://arxiv.org/abs/2406.07222)). nl2spec is closest to intent: 36 expert-written instances, interactive fragment editing reached 31/36 (86.1%), authors judged, at least 9/36 ambiguous ([source](https://arxiv.org/abs/2303.04864)).

### 2.2 T2 Conflicts and satisfiability

**Core finding.** Every working cross-form consistency checker found translates all clauses into **one common logic over one shared signature**, checks the conjunction, and returns a **minimal inconsistent subset**. Plain satisfiability is too weak. Every mature tool adds rt-inconsistency (the system can be painted into a corner), vacuity, realizability against the environment, or divergence under a boundary condition. Those stronger notions are the evidenced answer to the brief's "consistency checks that passed but missed a contradiction" (*Inference*).

| Option | Evidence (grade; n, setting) | Catches | Misses | Cost | Agents |
|---|---|---|---|---|---|
| **Common-logic conjunction + minimal inconsistent subset** | ReqCheck / Ultimate ReqAnalyzer at Bosch, RE 2019 (A). Ten device sets of 50–701 requirements: "ca. 310 results … 100 were classified as major issues, although the requirements had been reviewed manually several times before". Nearly 70% of findings led to requirement fixes, the rest to formalisation changes. One 263-requirement set had 6 vacuous requirements, 73 rt-inconsistencies, 18 timeouts, and took 3h58m ([source](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)). Hanfor (A-workshop) returns a minimal core, a timing diagram and vacuous requirements on 20–1000-requirement sets ([source](https://ultimate-pa.github.io/hanfor/references/publications/hanfor-semantic-requirements-review-at-scale.pdf)). EuRailCheck (A-workshop): a failure "cannot by itself separate" a formalisation error from a flaw in the informal spec ([source](https://arxiv.org/pdf/1003.1741v1.pdf)). PROPAS at Scania (A, venue unverified): all injected faults detected by Z3 ([source](https://www.es.mdh.se/pdf_publications/4980.pdf)) | Contradictions across forms; pairwise and k-subset localisation | Divergence in reachable corners unless environment states are enumerated; translation errors (the translation is itself a faithfulness step) | Minutes to formalise a change; 1m33s–4h14m per full run; no result reuse implemented | Human-only evidence |
| **LLM translation + SMT vs LLM alone** | SAT-LLM (A-pre). 55 requirements with 15 injected conflicting subsets (4 composite). LLM alone: P 0.85, R 0.31. LLM→FOL + Z3 MUS/MSS: **P 1.00, R 0.83**. "Correct" = conflict found with its counterpart ([source](https://par.nsf.gov/servlets/purl/10574434)) | Composite conflicts that LLM reading misses | Translation errors | Low | Measured |
| **Table completeness/disjointness** | DMN tables of about 500–1,500 rules (A-pre): missing-rule check 160 ms–18.3 s, overlap check 200 ms–30.7 s. Reported 812 maximal overlapping rule sets vs 23,115 from a naive algorithm ([source](https://arxiv.org/pdf/1603.07466)). TableWise used BDDs for exclusive/exhaustive (C) ([source](https://shemesh.larc.nasa.gov/fm/oldfm/fm-old-sw-ver-tablewise.html)) | Gaps and overlaps inside one table | Disagreement *between* tables over the same state | Negligible; run on every edit | Human-only evidence |
| **Divergence / boundary conditions** | van Lamsweerde & Letier (A-workshop): two goals that are consistent in general become inconsistent under a boundary condition; no detection-rate data ([source](https://webperso.info.ucl.ac.be/~avl/files/avl-MontereyLNCS.pdf)). Degiovanni et al. ASE 2018 (A): GA + LTL-SAT finds boundary conditions ([source](https://nmaguirre.github.io/assets/pdf/ase2018.pdf)); a 2022 critique says it is "not complete" and of modest efficiency (A-pre) ([source](https://arxiv.org/pdf/2203.12903)) | "Consistent but contradictory in a corner" | Completeness not guaranteed | Search cost | Human-only evidence |
| **Realizability / rt-consistency** | FRET compositional realizability, FM 2021 (A): realizable iff every shared-variable partition is; LMCPS FSM 1524.82 s → under 7 s. Results also include "unknown" (non-linear arithmetic) and 12 h timeouts; 3 of 12 benchmarks collapsed to one component via mode variables ([source](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf)). Spectra unrealizable cores (A): 227 student GR(1) specs, 40 unrealizable, many with multiple cores ([source](https://arxiv.org/pdf/2103.00297)). **Well-separation** (A): only 19 of 79 student specs well-separated, i.e. in 60 the system could win by forcing the environment to violate its assumptions ([source](https://zenodo.org/api/records/6577097/files/well-separation-fse16.pdf/content)) | Clause sets that hold only if the implementation could control the environment | Undecidable in general; data domains; interleavings (GR(1) has no native linearization points) | Seconds to hours; needs an input/output split | Human-only evidence; no LLM study found |
| **Structural vacuity gates** | Kupferman–Vardi (A), quoting Beer et al. 1997 ([unreachable]): "typically 20% of specifications pass vacuously during the first formal-verification runs" ([source](https://typeset.io/pdf/vacuity-detection-in-temporal-model-checking-290v578apa.pdf)). Frama-C/WP smoke tests (A): Thales JavaCard VM, 2,350 smoke tests for about 20 min (≈8%) on top of a more-than-4 h proof; they also found unsound axioms in WP's own library ([source](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf)). Dafny proof dependencies flag goals proved vacuously and redundant assumptions (B) ([source](https://dafny.org/blog/2023/10/27/proof-dependencies/)). ProofPulse (A-pre): 252 programs, "perfect precision for precondition classification", "cannot fully capture semantic intent" ([source](https://arxiv.org/pdf/2608.30818)) | Contradictory assumptions, dead antecedents, unreachable code | Consistent-but-weak specs | Low | Human-only evidence (ProofPulse ran on LLM-benchmark programs) |
| **Semantic-strength gates** | Lahiri (A, above). SpecRL (A-pre): "spectests" (outputs the implementation cannot produce) used as reward; +26.46% relative completeness ([source](https://arxiv.org/pdf/2604.05820)). ReForm (A-pre): of 115 failures, 52.2% weak specs, 44.3% unverifiable, 3.5% trivial; RL drifts to weak specs unless rewarded on a subset check against ground truth ([source](https://arxiv.org/pdf/2507.16331)) | Consistent but too weak | Needs an independent source of negatives | Low | Measured |
| **Constructive witnesses** | W3C Process, IETF RFC 6410 ("at least two independent interoperating implementations"), WebAssembly phase 4 ("two or more Web VMs" plus reference interpreter) (B) ([W3C](https://www.w3.org/policies/process/); [RFC 6410](https://www.rfc-editor.org/rfc/rfc6410.txt); [Wasm phases](https://raw.githubusercontent.com/WebAssembly/meetings/main/process/phases.md)). Watt, CPP 2018 (A): mechanisation found errors that made the Wasm type system "originally unsound", which had survived engines and the reference interpreter ([source](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf)) | Satisfiability on the exercised domain; implementability and shared reading | Non-vacuity; unexercised non-commitment branches; soundness | One build per witness | Human-only evidence |

**What a "consistent" result does not show.** An SMT "verified" result does not show that the assumptions are satisfiable: `{:axiom}` and bodiless contracts are taken on faith, and Dafny "still verifies the well-formedness" only (B) ([source](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/Attributes.md)). A smoke-test UNKNOWN gives "no guarantee" (A). Alloy results are scope-bounded (B) ([source](https://alloytools.org/tutorials/online/maintext-FS-2.html)). Lean "cannot check whether new axioms are consistent", so the gate is `#print axioms` (B) ([source](https://lean-lang.org/doc/reference/latest/Axioms/)). After its smoke tests found inconsistencies, the Frama-C team turned "most of our axioms into proper lemmas or Coq realizations" (A).

**Incremental consistency.** Bosch formalised changes "in mere minutes" but did not implement result reuse, and full runs took hours (A). Hanfor tags changed requirements for re-review (A-workshop). FRET's shared-variable partitions keep checks local *unless* mode variables connect everything (A). Nuseibeh et al.: "incremental or localized consistency strategies do not guarantee global consistency" (A) ([source](https://typeset.io/pdf/leveraging-inconsistency-in-software-development-4me5sgffk1.pdf)). *Inference*: on each new clause, run its per-form check, a k-subset conjunction against clauses that share a variable, and vacuity for the antecedents it touches. Run the full conjunction, rt/realizability checks and smoke tests nightly or before any downstream step. Keep every unsat core as a regression fixture. Handle state, profile and lifecycle phase will act as mode variables and defeat partitioning for a store API.

**Witnesses: how many and how different.** No source measures the defect yield per additional implementation. "Two" is a convention. *Inference*: replace the §3 seed "≥2 witnesses" with a coverage criterion: one witness per profile value; for each unspecified or indeterminate set, witnesses that between them choose every allowed outcome; and witnesses that survive adversarial environment schedules.

**[§3 qualification] Vericoding / DafnyBench "conform well to fixed, machine-checked specs".** Vericoding's own manual inspection found Dafny clean, but "conditioned on vericoding success, roughly 9% of the [Verus] specs were too weak and another 15% had poor translations" (A-pre) ([source](https://arxiv.org/pdf/2509.22908)). AlgoVeri shows some Vericoding Dafny/Verus specs accept "simply returning 0" (A-pre) ([source](https://arxiv.org/html/2602.09464v2)). MutDafny found 3 of its 5 weak specs in an LLM-generated set (A-pre) ([source](https://arxiv.org/html/2511.15403v1)). Pass rates therefore overstate conformance wherever the fixed spec is weak.

### 2.3 T3 Two test families on the reference model

#### 2.3.1 Spec-enforcing tests

**Core finding.** Model-generated tests replayed step by step, comparing state after each action, are cheap and strong when the target is small and close in granularity to the model. That is the position of a Python reference model. The decisive variable is granularity distance, not the tool (*Inference*). Model-generated tests inherit the model's blind spots and enforce spec → model only.

| Option | Evidence (grade; n, setting) | Catches | Misses | Cost | Agents |
|---|---|---|---|---|---|
| **TLA+ → test-case generation** | MongoDB Realm Sync, PVLDB 2020 (A). A 1 kLOC merge function, spec transcribed from code. 4,913 generated C++ tests covered **86/86 branches**, vs 18 for 36 handwritten tests and 79 for about 8 M AFL runs. The model checker, not the tests, found a non-terminating merge rule that "had faithfully been transcribed from C++ to TLA+" ([source](https://arxiv.org/abs/2006.00915)) | Spec/implementation divergence on enumerable state | Bugs shared by spec and code (caught only by an independent property) | 1 engineer, 4 weeks | Human-only evidence |
| **State-space-guided testing** | Mocket, EuroSys 2023 (A). 9 bugs in Xraft, Raft-java, ZooKeeper, including 2 in the official Raft TLA+ spec. Mapping annotations 134–152 LOC per system ([source](https://gaoyu-cn.github.io/paper/2023-eurosys-mocket.pdf)) | Divergence per action | Unmodelled behaviour | Hundreds of LOC | Human-only evidence |
| **Multi-grained conformance replay** | Remix, EuroSys 2025 (A; §3 item re-checked). Found message-type, branch and assignment discrepancies; 6 severe ZooKeeper bugs mainly via model checking. "The conformance checking is unsound … We only check safety" ([source](https://arxiv.org/abs/2409.14301)) | Spec ↔ code drift | Liveness; unmodelled behaviour | Within 40 person-hours per mixed-grain spec | Human-only evidence |
| **Quint Connect / Apalache MBT** | Vendor posts and slides (C). Emerald: an AI wrote the Quint spec from *code* and most of the driver; about 80% coverage, one memory leak, n = 1 ([source](https://quint-lang.org/posts/quint_connect_emerald)). Apalache MBT: claims without figures ([source](https://conf.tlapl.us/2020/09-Kuprianov_and_Konnov-Model-based_testing_with_TLA_+_and_Apalache-Slides.pdf)) | Divergence | Spec-from-code confirms code (*Inference*, §3 SpecGen) | Low claimed | Agent, C-grade, n = 1 |
| **Dafny test generation (DTest)** | NFM 2023 paper [unreachable]; author page (B): coverage-directed inputs, "officially part of Dafny" ([source](https://sasha-fedchin.github.io/2024/12/06/dtest.html)) | Statement/path coverage of the contract | No oracle beyond the contract; no Dafny → Python bridge evidence | — | None found |
| **P# systematic testing** | FAST 2016 (A). Bugs per system: vNext 1 (a months-old liveness bug), MigratingTable 11, Fabric 1 unconfirmed. Environment-modelling effort 2 person-weeks to 5 person-months ([source](https://www.doc.ic.ac.uk/~afd/papers/2016/FAST.pdf)) | Concurrency × failure bugs | Faults not modelled | Environment modelling dominates | Human-only evidence |
| **Contract → property tests; stateful PBT** | icontract-hypothesis infers strategies from preconditions (B, no effectiveness data) ([source](https://raw.githubusercontent.com/mristin/icontract-hypothesis/master/README.rst)). Hypothesis rules, preconditions, invariants, Bundles (B) ([source](https://hypothesis.readthedocs.io/en/latest/stateful.html)). Hughes' AUTOSAR/Dropbox reports [unreachable] | Clause violations on generated inputs | Inherits contract weakness | Mechanical | No agent study of the contract→test step |
| **LLM-written PBTs from docs** | Vikram et al. (A-pre): n = 40 API methods; valid and sound PBT in 2.4 samples; best model covered **21%** of documented properties ([source](https://arxiv.org/abs/2307.04346)). PBT-Bench (A-pre): 100 problems, 365 injected bugs, recall **42.1–83.4%**; under an open prompt a frontier model "stops after exposing a single bug" ([source](https://arxiv.org/abs/2605.15229)). Agentic PBT (A-workshop): 100 packages, 56% of n = 50 sampled reports valid, $9.93 per valid bug, properties inferred from code + docs ([source](https://arxiv.org/abs/2510.09907)) | Many property classes incl. stateful | Coverage of the spec unless the harness enforces it | Low | Measured |
| **History checking** | Porcupine (README B, blog C; §3 item re-checked): executable sequential model + history; "1,000x–10,000x faster" than Knossos, self-reported on Jepsen data ([source](https://raw.githubusercontent.com/anishathalye/porcupine/master/README.md)). OmniLink (A-pre): TLA+ meaning per timeboxed event; agreed with Porcupine on every trace; found 2 unknown bugs in WiredTiger/BAT/ConcurrentQueue ([source](https://arxiv.org/abs/2601.11836)) | Linearizability violations; with TLA+, non-linearizable specified behaviour | Only histories actually generated | NP-complete check | Human-only evidence |
| **Environment actions as generated operations** | Remix fault injection; CCF `IsFault` composition; TraceLink found timeout and failure-detector model bugs ([source](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf)); FoundationDB deterministic simulation, "tens of thousands of simulations every night" (B) ([source](https://apple.github.io/foundationdb/testing.html)) | Concurrency + failure bugs; hidden environment assumptions | Faults outside the action alphabet | Environment modelling | Human-only, except Emerald (C) |

**[§3 challenge] Porcupine cost.** OmniLink is the first independent comparison found. Porcupine is "significantly faster" on small or many-thread histories, but "past 200k operations with few threads … takes a long time – often multiple minutes – to reject traces" (traces of 500–450k operations, 1–50 threads, 10 repetitions). Porcupine's own speed figures are self-reported ([OmniLink](https://arxiv.org/abs/2601.11836)).

**Agent applicability.** The measured agent weak spot is *coverage of the spec* (21% property coverage; stopping after one bug), not glue code. The measured remedies are structural: an explicit "test the whole documented specification" instruction, fixed formats, a fixed mapping ([PBT-Bench](https://arxiv.org/abs/2605.15229); [Konnov slides, C](https://conf.tlapl.us/2026-etaps/konnov-2026.pdf)). *Inference*: give agents the clause text and ID, never the reference-model source, when they generate spec-enforcing properties, and have the harness impose one test obligation per clause ID.

#### 2.3.2 Conformance between layers (formal model F ↔ reference model R ↔ spec S)

| Bridge | Evidence (grade) | Strength | Miss | Cost |
|---|---|---|---|---|
| **Differential random testing (DRT)** | Cedar, FSE Companion 2024 (A). Lean model 1,673 LOC vs Rust production 15,693. DRT + PBT found 21 bugs, proofs 4 more. Each target fuzzed 6 h/day on 4 vCPU. DRT missed a non-termination bug (rare inputs). Generator bias: 35.5% of `when` conditions were boolean literals, cut to 9.7% with a new generator. One DRT failure (string size semantics) surfaced a spec ambiguity and **led to dropping a language feature** ([source](https://arxiv.org/abs/2407.01688)) | Output equality on generated inputs | Rare inputs; anything outside the generators | Cheap once the model is executable |
| **Trace validation (impl → model)** | Cirstea et al. (A-pre; §3 item re-checked): "in all cases" found unmatched executions. **"Too imprecise logs may even lead to erroneous traces being accepted."** Logging all variables plus events keeps exploration near trace length ([source](https://arxiv.org/abs/2404.16075)). CCF (A/A-pre): 6 bugs across methods; the first consensus trace spec took about **2 engineer-months**, a later consistency spec about **1 engineer-week**; DFS validation took under 1 s vs about 1 h with BFS ([source](https://arxiv.org/abs/2406.17455)). TraceLink, OOPSLA 2025 (A; §3 item re-checked): 9 bugs, all model↔implementation drift or environment assumptions; fixes "did not change the outcome of model checking" ([source](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf)) | "Everything R did, F allows" | F behaviour R never exercised | 1 week to 2 months |
| **Negative result** | MongoDB MBTC (A): 2 engineers, 10 weeks, abandoned; "Bugs in post-processing could mask implementation bugs"; workarounds avoided or simulated conformant behaviour ([source](https://arxiv.org/abs/2006.00915)) | — | Large, coarse targets | High |
| **PObserve** | P docs (B; §3 item re-checked): log-based monitoring, **no measured data exists** to re-check ([source](https://p-org.github.io/P/advanced/pobserve/pobserve)) | — | — | — |
| **Refinement checks** | No full-text bridge evidence; named only as framing or future work (Remix, MongoDB, Cirstea) | — | — | — |

**[§3 challenge] Cedar's model layer.** The FSE 2024 paper says "We wrote models of the Cedar evaluator, authorizer, and validator in **Lean**", and the OOPSLA-extended preprint likewise describes a Lean model with proofs ([source](https://arxiv.org/pdf/2403.04651)). Any reading of Cedar as Dafny model vs Rust is not supported by these texts. Whether an earlier Dafny phase existed was not verified.

*Inference*: three conclusions follow. First, only F ↔ R has measured mechanical bridges; S ↔ F and S ↔ R need clause-ID traceability plus T1/expectation methods. Second, a complete bridge needs both directions, as Konnov's slides state (C): replay F → R plus trace validation R → F, or DRT plus coverage. Third, R is deterministic and fully observable, so full-state logging removes Cirstea's false-acceptance risk. A reviewed, versioned abstraction function `alpha(R_state) → spec_state` is the single cheapest structural decision, and it is where agents are likely to cut corners ("do not trust the generated harness – TODOs and bugs inside", [Konnov, C](https://conf.tlapl.us/2026-etaps/konnov-2026.pdf)). A failing bridge should route back to the clause (the Cedar lesson), not be fixed in whichever layer is easier (the MongoDB anti-pattern).

**Agents in bridges.** SysMoBench (A-pre): 11 systems, four agent backends, 5 runs each. Conformance was 80–100% on a spinlock but at most 15.38% on Etcd Raft; "few AI-generated models achieved fine-grained conformance". An LLM-built name mapping was inspected and found correct ([source](https://arxiv.org/abs/2509.23130)). The code-translation agent did better, consistent with the spec-from-code confirmation effect (*Inference*). Konnov (C, n = 2): an AI-written TFTP harness took about 1 week and about 200 premium requests of debugging, and found 2 bugs; for ZooKeeper, "sometimes, AI tools cut corners badly". NL → TLA+ over 30 LLMs and 205 specs: up to 8.6% semantically correct (A-pre, abstract only) ([source](https://arxiv.org/abs/2606.05792)). This is consistent with §3 ("LLM-written system-level TLA+ is weak"), so it is not a challenge.

#### 2.3.3 Expectation tests (independent of spec and model)

**Core finding.** Evidence that intent-derived oracles beat *code*-derived ones is now solid for LLMs. Evidence that prose-derived oracles beat *spec*-derived ones, which is the brief's actual claim, **was not found anywhere**. Human evidence shows requirement-only oracles catching a minority of *implementation* faults.

| Option | Evidence (grade; n, setting, "correct") | Catches | Misses | Agents |
|---|---|---|---|---|
| **Specification by example / ATDD / BDD** | Ricca et al. 2007 ECEASST (A-workshop): n = 13 students; Fit tables helped correct maintenance, where correctness was judged by a *separate* acceptance suite ([source](https://profs.scienze.univr.it/ceccato/papers/2007/evol2007.pdf)). BDD systematic mapping, 166 papers (A): "acute shortage of metrics" ([source](https://arxiv.org/abs/2305.05567)) | Implementer misunderstanding | No count of spec misreadings caught | Human-only evidence |
| **LLM Gherkin / acceptance tests** | Karpurapu et al. (A-pre): about 50 stories; "correct" = Gherkin-lint syntax ([source](https://arxiv.org/pdf/2403.14965)). Sami et al. (A-pre): 62/65 found tests "useful"; the authors praise the model's ability to "extend beyond the explicit requirements" ([source](https://arxiv.org/pdf/2504.07244)). AToMIC (A-pre): inputs include code, so not independent ([source](https://arxiv.org/pdf/2510.18861)) | Overlooked error scenarios (perceived) | Faithfulness unmeasured; **added commitments presented as a feature** | Measured, but only syntax or usefulness |
| **Tests as intent clarification** | TiCoder, IEEE TSE 2024 (A): n = 15 programmers evaluated AI code more correctly with less cognitive load; with an idealised oracle proxy, +45.97% pass@1 within 5 interactions ([source](https://arxiv.org/pdf/2404.10100)) | Misreading exposed by one concrete test | Proxy is idealised | Measured |
| **Independence by information hiding** | Leveson et al. 1990 TSE (A): 24 students; spec-only self-checks found **19%** of detected faults, and only 4 of 34 effective checks (12%) came from the spec alone; code reading improved checks ([source](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf)) | Different faults than voting | Implementation faults (a minority) | Human-only evidence |
| **LLM oracle pull toward observed behaviour** | Zhao et al. ISSTA 2026 (A): 233 Defects4J defects, 13 LLMs. Shown buggy code: 3.84% misguided tests vs 0.46% when shown fixed code; effective tests 2.98% vs 8.51%. Replacing code with a spec docstring: effective 104.15 → 186.77 ([source](https://arxiv.org/pdf/2607.22883)). Konstantinou et al. (A-pre): accuracy drops on buggy code, e.g. 43.02% → 35.72% ([source](https://arxiv.org/abs/2410.21136)). Mathews & Nagappan (A-pre): tools that keep only passing tests discard bug-revealing ones ([source](https://arxiv.org/abs/2412.14137)) | Shows the mechanism of confirmation | — | Measured |
| **Oracle anchoring** | Canedo (A-pre, single author, one system): a state-anchored oracle "cannot fail"; re-anchoring one oracle recovered 8 of 46 surviving mutants; "a reference model on that population kills exactly what specification anchoring kills" ([source](https://arxiv.org/pdf/2608.17214)) | Lint target for independence | n = 1 system | Human-only evidence |

*Inference*: define independence by **information flow**. The expectation-test writer reads records only, never sees the spec, models or reference model, and no expected value may be computed by calling R or a spec-derived helper. Canedo's anchoring predicate then becomes a dataflow/import lint. Do not drop expectation tests because they fail on R: a failure is a finding to adjudicate (record, spec, model or test). Require every expectation test to cite its decision and scenario, and flag any assertion not traceable to that decision as an added commitment, guarding against the Sami et al. effect. Leveson's datum fits a complementarity reading: expectation tests target translation errors, while spec- and code-informed tests target implementation errors.

#### 2.3.4 Oracles for non-commitment

Mature conformance suites already encode typed non-commitment in the oracle language (all B, official docs):
- WebAssembly `assert_return` takes `either` (alternative results) and NaN patterns ([README](https://raw.githubusercontent.com/WebAssembly/spec/main/interpreter/README.md)). Relaxed SIMD specifies that "each environment globally chooses a fixed projection" ([Overview](https://raw.githubusercontent.com/WebAssembly/relaxed-simd/main/proposals/relaxed-simd/Overview.md)).
- sqllogictest uses `rowsort`/`valuesort` for undefined order and `skipif`/`onlyif` per engine ([about.wiki](https://raw.githubusercontent.com/gregrahn/sqllogictest/master/about.wiki)).
- JSON Schema separates `optional/` tests ([README](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/README.md)).
- POSIX (IEEE 1003.3) has the verdicts UNSUPPORTED and UNRESOLVED ([LTP](https://raw.githubusercontent.com/linux-test-project/ltp/master/testcases/open_posix_testsuite/Documentation/HOWTO_ResultCodes)).

NonDex explores allowed behaviours of underdetermined specs and found 60 open-source and 110 student bugs (A-workshop; human-only) ([source](https://mir.cs.illinois.edu/gyori/pubs/jpf16.pdf)). On loose suites, PatchDiff (ICSE 2026, A; agents' patches measured) finds that 29.6% of "plausible" SWE-bench Verified patches diverge from ground truth, 27.3% of divergences "adapt more behavior", and resolution rates are inflated by 6.4 points ([source](https://arxiv.org/abs/2503.15223)).

| Non-commitment type | Oracle mechanism with precedent (*Inference* mapping) |
|---|---|
| Unspecified (one of a set) | `either` set when small; predicate when large; canonicalisation for ordering; add a cross-call consistency test if stability is promised (Wasm's per-call `either` does not test the fixed projection) |
| Optional | Opt-in suite, verdict UNSUPPORTED (not a failure); must still fail if the feature is claimed and wrong |
| Deliberately not promised | Assert nothing on the dimension, plus a NonDex-style perturbing reference model: any test that then fails is over-strict |
| Profile-declared | One suite parameterised by profile value with a per-profile expected set (§3 rule) |
| Indeterminate | Accept "took effect" and "did not"; defer to later observations; an UNRESOLVED-like verdict must not count as a pass |

*Inference*: bound each family from both sides on R. The **allowed-variant check** requires every test to pass on R variants that make different allowed choices. The **forbidden-variant check** requires that, for each per-decision mutant making a disallowed choice, some test in the right family fails. Expectation tests are most prone to over-strictness, because a record scenario fixes values the decision may leave open. Predicates and canonical forms, rather than enumerated outcome sets, are the default suggested by the precedents. ShardStore-style relaxation flags are kept for unknowable state. This is a design argument; no study measures outcome sets against relaxation flags.

### 2.4 T4 Adequacy and traceability

**Trace links as checkable data.** All of the following are B (official docs or source):
- **OpenFastTrace** reports missing coverage types, `ORPHANED`, `OUTDATED`, `AMBIGUOUS` and duplicate IDs, and has a quiet, return-code-only mode for CI ([report](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/console_tracing_report.md); [LinkStatus](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/api/src/main/java/org/itsallcode/openfasttrace/api/core/LinkStatus.java)).
- **sphinx-needs** fails on dead links, wrong target types and schema link counts under `-W` ([config](https://sphinx-needs.readthedocs.io/en/latest/configuration.html)).
- **Doorstop** fingerprints links, flags downstream links as suspect when the parent changes, and exits 1 on failure ([validation](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/docs/cli/validation.md)).

Measured benefit: 71 subjects worked 24% faster and produced 50% more correct solutions with traceability (Mäder & Egyed, A, abstract only; human-only) ([source](https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f/full)). LLM trace recovery: LiSSA (A) reached best F1 of roughly 0.25–0.53 on five requirement → code benchmarks. "Correct" means agreement with gold links, and the authors say more research is needed "to be applicable in practice" ([source](https://publikationen.bibliothek.kit.edu/1000179816/164563088)). *Inference*: write links when each artefact is created (with the revision in the ID, as OFT does), gate deterministically, and use LLM recovery only to audit. A link gate shows that links exist, not that they bind; that is mutation's job.

**Mutation of spec, models and reference model.**

| Option | Evidence (grade; n, setting) | Catches | Misses / triage | Cost | Agents |
|---|---|---|---|---|---|
| **Dafny spec mutation + sanity checks + spec-testing proofs** | IronSpec, OSDI 2024 (A): 14 specs; 10 author-confirmed spec bugs in 6 real systems; 13 of 61 surviving mutants were intended weaknesses (false positives); mutation runs "only if the system has a passing proof" ([source](https://par.nsf.gov//servlets/purl/10550356)) | Specs weaker than intended | False positives from intended weakness | 3 s to 80–191 min; STP suites take hours to days | Human-only evidence |
| **Implementation mutation exposing weak specs** | MutDafny (A-pre): 794 programs, 112,810 mutants; 284 survivors reviewed: 77 weak-spec, 157 equivalent, 50 inconclusive; 5 weak specs found, 3 of them in LLM-generated programs ([source](https://arxiv.org/html/2511.15403v1)) | Weak postconditions | Equivalent-mutant triage dominates | About 18 min per file; 1.7 min per survivor | Indirect (LLM-written specs) |
| **Alloy model mutation** | Jovanovic, Patwary, Sullivan, FormaliSE 2025 (A): 25,180 unique real faulty Alloy4Fun models. Mutants reproduce only 10.96% (17.72% with new operators), but mutant-killing suites **detect 91.78%** (95.79%) ([source](https://allisonius.github.io/files/FormaliSE2025.pdf)) | Real model faults | Novices only | Low | Human-only evidence |
| **TLA+ invariant mutation as vacuity probe** | TLA+-Bench (A-pre): of 30 TLC-passing outputs, 18 testable, **only 5 survived** invariant→TRUE. 1.7% of 300 outputs survived vs 10.0% plain "correct"; the probe's wording needs re-checking ([source](https://arxiv.org/pdf/2607.23425)). TLA-Prover tiers (A-pre): Diamond requires a mutated invariant to yield a counterexample ([source](https://arxiv.org/pdf/2606.06133)) | Vacuous model-checking passes | No dedicated TLA+ mutation tool found | Low | Measured (LLM outputs) |
| **Reference-implementation mutants measure contract completeness** | NL2Contract (A-pre): a verification-sound LLM contract discriminates "over three-quarters" of buggy mutants ([source](https://arxiv.org/pdf/2510.12702)). SpecRL output-mutation spectests (A-pre) | Weak contracts | — | Low | Measured |
| **Python mutation; mutation at scale** | mutmut: incremental, type-check filtering, CI stats (B) ([source](https://raw.githubusercontent.com/boxed/mutmut/main/README.rst)). Google, about 15 M mutants over 6 years: mutants coupled to real high-priority faults, and developers wrote more and stronger tests (A) ([source](https://arxiv.org/abs/2103.07189)) | Unasserted effects | Equivalent mutants | Incremental | Human-only evidence |
| **LLM-generated mutants** | Wang et al. TOSEM 2025 (A): 851 real Java bugs; 76.47% real-bug detection vs 44.15% for rule-based tools ([source](https://arxiv.org/pdf/2406.09843)). Meta ACH (A): 9,095 mutants, 571 tests, 73% accepted; LLM equivalent-mutant detector P 0.79 / R 0.47 ([source](https://arxiv.org/pdf/2501.12862)) | More realistic mutants | Compilability, duplicates | — | Measured |

No study tests the §3 seed directly (one mutant reference model per clause, killed by the suite). The closest analogues mutate implementations or outputs. *Inference*: require a **per-family kill**. A clause-linked R mutant killed by only one family is a finding: killed only by spec tests means a hole in the expectation family; killed only by expectation tests means a likely faithfulness gap in the clause. Survivors that map to a registered non-promise are auto-classified "intended", which shrinks IronSpec/MutDafny-style triage.

**Does mutation score track real faults?** For code: 73% of 357 real faults were coupled to mutants and 17% to none (Just et al., A) ([source](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)). Strong mutation had the highest fault revelation of four criteria, once the clean-program assumption is avoided (Chekam et al., A) ([source](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)). Correlation is weak once suite size is controlled (Papadakis et al. 2018, [unreachable]). For models, Alloy4Fun is the only large real-fault result. *Inference*: use mutation as a hole finder, not a numeric target. The 17% uncoupled share is the expected blind spot, and the independent expectation family is the hedge against it.

**Coverage that fits (necessary conditions only).**
- TLC coverage reports actions that "never run (potential errors)" (B) ([source](https://docs.tlapl.us/_export/raw/using:coverage)).
- QuickCheck `checkCoverage` fails a property on statistical grounds (B) ([source](https://hackage.haskell.org/package/QuickCheck-2.14.3/docs/Test-QuickCheck.html)).
- Hypothesis `event`/`target` only *report*, so a wrapper is needed to gate (B) ([source](https://hypothesis.readthedocs.io/en/latest/reference/api.html)).
- Hughes (A; human-only): on a BST with 8 planted bugs, validity properties missed 5/8; model-based properties found the union bug in 8.4 tests vs 50; a label showed the key absent in 79.2% of a million tests ([source](https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf)).
- Goldstein et al. (A; 30 interviews at one firm): practitioners validated PBTs by mutation 7/30, example inspection 8/30, code coverage 2/30 ([source](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf)).

*Inference*: the coverage gates are clause, scenario, case-table row, non-commitment branch (each allowed outcome hit at least once), model action and state × operation cell, plus generator health (invalid and filter-retry rates; a validity property run first).

**Gate composition.** No published ordered pipeline matches the brief. The published partial orderings are:
- TLA-Prover tiers: parse < no warnings < TLC pass < mutation-sensitive.
- IronSpec: cheap sanity checks → STPs → mutation after a passing proof.
- Hughes: the validity property runs first.
- OFT: `direct_failures` lists root causes first.
- Doorstop: suspect links act as a change-triggered gate.

AWS's ordering (CACM 2025) is [unreachable]. *Inference*, proposed sequence; each gate blocks the next stage for the affected clause:

| # | Gate | Fails on | Typical cost |
|---|---|---|---|
| G0 | ID/schema lint | missing or duplicate IDs, malformed form, untyped non-commitment | seconds |
| G1 | Upward trace | clause without `decision~rev` (added commitment), decision without clause (lost case), `OUTDATED` | seconds |
| G2 | Faithfulness exhibition | rejected scenario witness, failed rejected-option refutation, "not addressed" on an added-commitment probe | minutes per clause |
| G3 | Form-local checks | table not complete or disjoint; missing transition cell | seconds |
| G4 | Cross-clause consistency and satisfiability | unsat core, contract inconsistency, rt/realizability failure, well-separation failure | seconds to hours |
| G5 | Vacuity and non-triviality | invariant→TRUE still passes; smoke tests; sanity flags | seconds to minutes |
| G6 | F ↔ R conformance | DRT or replay mismatch; trace-validation rejection | minutes |
| G7 | Downward trace and coverage | clause without spec test, scenario without expectation test, never-fired action, uncovered row or branch, generator health | seconds to minutes |
| G8 | Per-family mutant kill + allowed-variant check | R mutant not killed by both families; any test failing on an allowed variant | minutes to hours |
| G9 | Spec-strength mutation | a stronger clause variant still passes all proofs and tests | minutes to hours |

G5 must precede trusting any model-checking pass. G8 and G9 must follow G6, because mutating a non-conforming R measures the wrong thing. That matches IronSpec's "only if the proof passes" (*Inference*).

**Agent applicability (T4).** Measured: trace recovery (moderate), mutant generation (better coupling than rule-based tools), mutant-killing test generation (73% accepted), and the vacuity of LLM TLA+ (mostly vacuous) and of LLM Dafny specs (weak). Not measured: agents authoring links, designing coverage requirements, triaging spec-mutant survivors, or running a per-family kill gate. Gates must be non-editable by the producing agent (§3 baseline).

### 2.5 T5 Independence (minimal)

| Finding | Evidence (grade; n, setting) | Agents |
|---|---|---|
| LLM errors are correlated, more so within one provider and among *more accurate* models; judges inflate same-provider answers | Kim et al. ICML 2025 (A): 349 LLMs on 12,032 MCQs and 71 on 14,042. When both models are wrong they pick the same wrong answer 0.423 (baseline 0.127) and 0.60 (baseline 0.33) of the time ([source](https://arxiv.org/pdf/2506.07962)) | Measured |
| Intrinsic self-correction does not reliably help | Huang et al. ICLR 2024 (A): e.g. CommonSenseQA 75.8 → 41.8 after 2 rounds for one model ([source](https://arxiv.org/pdf/2310.01798)); Kamoi et al. TACL (A): self-correction works with reliable external feedback ([source](https://arxiv.org/pdf/2406.01297)) | Measured |
| Self-preference and judge noise | Panickssery et al. NeurIPS 2024 (A) ([source](https://arxiv.org/pdf/2404.13076)); CodeJudgeBench (A-pre): swapping response order changes accuracy by up to 14% ([source](https://arxiv.org/pdf/2507.10535)); Jin & Chen (A-pre): over 700 tasks, LLMs over-reject correct code, and asking for explanations makes it worse ([source](https://arxiv.org/pdf/2603.00539)) | Measured |
| LLM help can hurt prose review | Broccia et al. (A-pre): n = 34 novice inspectors; LLM support *lowered* requirement-smell detection accuracy ([source](https://arxiv.org/pdf/2608.21298)) | Measured |
| Debate adds little beyond voting | Smit et al. ICML 2024 (A) ([source](https://arxiv.org/pdf/2311.17371)); Choi et al. (A-pre): majority voting explains most of the gain ([source](https://arxiv.org/pdf/2508.17536)) | Measured |
| Refuters trained on planted bugs work | An RLHF-trained code critic (McAleese et al., A-pre) caught more human-inserted bugs than paid reviewers; human + critic teams matched recall with fewer hallucinations ([source](https://arxiv.org/pdf/2407.00215)) | Measured (code, not specs) |
| Judge aging | Beyond Compilation (A-pre): one judge rejected outputs of two newer systems, but only 4 of 54 rejections (7%) were real errors ([source](https://arxiv.org/pdf/2606.31002)). MathAtlas (A-pre): faithfulness judges lose accuracy out of domain ([source](https://arxiv.org/pdf/2605.14061)) | Measured |
| An independent, *differently structured* second description finds spec bugs | Arm, Reid OOPSLA 2017 (A): a high-level property set written from the NL manual "to describe the architecture differently" found **12 bugs (2 security)** in an extensively tested ASL spec; rules that restated the spec were rejected as "prone to common-mode failure" ([source](https://alastairreid.github.io/papers/oopsla2017-whoguardstheguards.pdf)). JEST, ICSE 2021 (A): N+1-version testing found 27 spec bugs and 44 engine bugs in ES11 ([source](https://arxiv.org/pdf/2102.07498)) | Human-only evidence |

*Inference*: no gate should let a lineage judge its own spec. A single cross-family judge is weakly supported. Best supported: cross-family judges must agree to accept, rejections go to a human, the gate is calibrated on a human-labelled sample and recalibrated when the generating models change. Because stronger models have more correlated errors, upgrading every agent can *reduce* independence between the spec writer and the expectation-test writer. Independence must come from the derivation path and the artefact, as in Reid's "describe it differently". Knight & Leveson 1986 is [unreachable], and its figures were not re-checked.

### 2.6 Disconfirming searches (brief §5)

**(a) Do formal or structured intermediates fail to improve faithfulness over careful prose review?** *Result: no direct disconfirmation found; indirect cautions found.* No full-text study holds intent fixed and shows a formal or structured intermediate giving worse or equal faithfulness than careful prose review. No study measures the faithfulness (as opposed to form quality) of EARS, Gherkin or templates against prose review either. The indirect cautions:
- Humans misread and miswrite formal notation, and English → LTL is the worst direction: 28–47% wrong, including experts ([Greenman et al., A](https://arxiv.org/abs/2211.01677)).
- With n = 215 students, pattern-based PSP beat EPL, which beat raw LTL, for semantic correctness. There was no prose-only arm ([Czepa et al., A](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6944266/fullTextXML)).
- Compilation overstates faithfulness by up to 29.5 points ([Beyond Compilation, A-pre](https://arxiv.org/pdf/2606.31002)).
- LLM-assisted prose inspection got *worse* ([Broccia et al., A-pre](https://arxiv.org/pdf/2608.21298)).
- Templates need substantial training (Großer et al., abstract only), and FRETish authoring was "not always straightforward" (A).
- One NASA/Manchester/York preprint claims structured intermediates "significantly improved" LLM accuracy without data. That is C-level inside an A-pre paper, and its supporting reference concerns code translation. The same paper reports that an independent oracle caught an `optional` vs `weak` error "easily missed during manual inspection" ([Mavridou et al.](https://arxiv.org/pdf/2512.15788)).
- On the independence premise, Leveson et al. 1990 partly disconfirms: requirement-only checks found 19% of detected implementation faults (A).

Snook & Harrison and Finney are [unreachable]. Net: the §3 point "notation alone does not beat prose" is **reinforced, not challenged**. Measured benefit comes from decomposition plus deterministic translation (Req2LTL), example tables (Fit), and formal artefacts *paired with a check against intent*.

**(b) Do model- or mutation-based adequacy measures fail to predict real defects for specs or models?** *Result: partial disconfirmation, strong for coverage targets, weak for mutation.*
- On 7 industrial critical systems built with model-based development, MC/DC-style generated suites often found fewer faults than random suites of equal size, up to 40.6% fewer; observability-aware OMC/DC partly fixes this ([Gay et al. TSE 2015, A, first pages only](https://www.greggay.com/pdf/15covrisks.pdf)).
- Coverage correlates low-to-moderately with effectiveness once suite size is controlled, and effectiveness there was itself measured by mutants ([Inozemtseva & Holmes, A](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf)).
- Mutation-score correlation is weak once size is controlled (Papadakis 2018, [unreachable]).
- 17% of real faults are coupled to no mutant (Just, A).
- For declarative models, operators reproduce only 11% of real faults, yet mutant-killing suites detect 92% (A). That disconfirms operator realism and supports adequacy.
- A plain model-checking pass is a poor signal: 5 of 18 testable LLM TLA+ passes survived invariant mutation (A-pre).

**No** study shows that model-mutation adequacy fails to predict real spec or model defects, and none beyond Alloy4Fun shows that it succeeds. *Inference*: use coverage as necessary-condition gates, never as targets, and mutation as the adequacy signal, hedged by the independent family.

**(c) Is there a published pipeline doing prose → spec → model → reference model with faithfulness gates?** *Result: none found.* The nearest pipelines reverse or collapse the chain:
- **WebAssembly SpecTec** (PLDI 2024, A) generates prose and an interpreter from one DSL. It passed all applicable Wasm 2.0 tests and found 10 bugs in 5 Wasm 3.0 proposals. Faithfulness to intent is checked only via the human-written test suite ([source](https://people.mpi-sws.org/~rossberg/papers/Youn,%20Shin,%20Lee,%20Ryu,%20Breitner,%20Gardner,%20Lindley,%20Pretnar,%20Xiaojia,%20Watt,%20Rossberg%20-%20Bringing%20the%20WebAssembly%20Standard%20up%20to%20Speed%20with%20SpecTec.pdf)).
- **ECMAScript JISET/JEST** extracts the semantics from the spec and blames spec or engine by N-version voting (A).
- **Arm ASL** combines an executable spec, more than 11,000 AArch64 validation tests, and the 2017 independent property set; humans arbitrate disagreements "to match the architects' intent" (A) ([source](https://alastairreid.github.io/papers/fmcad2016-trustworthy.pdf)).
- **Cedar** goes design → Lean model → Rust with DRT in CI, with no gate against prose (A-pre).
- **FRET** has explanations, simulation, realizability, and an oracle on its template → formula translation; prose → FRETish is left to the human.
- **Req2LTL**, **Roundtrip**, **NeuroSTAR** and **Cunha & Macedo** each cover one NL → formal step.
- **GitHub Spec Kit** runs agents only, with same-lineage self-review checklists and no data (D/B) ([source](https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md)).

Agents are measured in none of the closely fitting pipelines. Since no pipeline matches, §4 synthesises, and it uses the Arm/SpecTec/JEST pattern as the comparison point: one executable source, mechanically derived layers, and an independently authored, differently structured check set. Those projects found real spec bugs (Wasm 10, ES11 27, Arm 12, Cedar about two dozen) precisely where an independent artefact disagreed with the spec (*Inference*).

### 2.7 Baseline (§3) points touched by new full-text evidence

| §3 point | Status | Evidence |
|---|---|---|
| Executable reference models (Cedar) | **Challenge**: Cedar's models are Lean, not Dafny | [FSE 2024](https://arxiv.org/abs/2407.01688); [arXiv 2403.04651](https://arxiv.org/pdf/2403.04651) |
| Agents conform well to fixed, machine-checked specs (Vericoding, DafnyBench) | **Qualification**: some fixed specs are weak (Verus 9% too weak + 15% poor translation; AlgoVeri "return 0"), so pass rates overstate conformance | [Vericoding](https://arxiv.org/pdf/2509.22908); [AlgoVeri](https://arxiv.org/html/2602.09464v2) |
| Triangular cross-checks help (Clover) | **Qualification**: agreement among legs sharing a reading ≠ faithfulness | [Roundtrip](https://arxiv.org/abs/2604.25031) |
| History checkers and their cost (Porcupine) | **Challenge/refinement**: speed claims self-reported; slows past about 200k ops with few threads | [OmniLink](https://arxiv.org/abs/2601.11836) |
| Not re-checked items (Cirstea, TraceLink, PObserve, Porcupine, 2409.14301) | **Re-checked**; PObserve has no data to re-check | §2.3 |
| Notation alone does not beat prose; LLM system-level TLA+ weak; SpecGen; nl2postcond | **Reinforced** | §2.6(a); TLA+-Bench; SysMoBench; Zhao et al. |
| Seeds: mutant reference model; ≥2 witnesses | **Still unevidenced directly**; nearest analogues are NL2Contract/SpecRL/MutDafny and standards conventions | §2.2, §2.4 |

---

## 3. Check map per normative form

All cells are *Inference* that maps the cited mechanisms onto the brief's forms. "Earliest" is the first gate (§2.4) at which a defect in that form can fail. "Exp." means the expectation family; "Spec." means the spec-enforcing family.

| Normative form | Faithfulness check | Consistency check | Satisfiability / non-vacuity check | Enforcement (Spec. / Exp. / mutants) | Earliest failure |
|---|---|---|---|---|---|
| **Formula over one instant** | Scenario derivability (permit or entail); rejected-option refutation; added-commitment probe via failing Dafny assertion or Hypothesis-shrunk case shown with the source sentence (Cunha & Macedo; Lahiri) | Conjunction over the shared abstract state (SMT, unsat core); Dafny contradictory/redundant-assumption warnings | Interesting witness (antecedent fires); verified R body; "negate the postcondition, must fail"; output-mutation spectests (SpecRL) | Spec.: contract → Hypothesis property and `@invariant`. Exp.: literal I/O from the scenario. Mutant: R returns a rejected-option output. Miss: rare inputs (Cedar) | **Before the spec** (record pos/neg checks drafted); G2 once the clause exists |
| **Case table (complete, disjoint)** | Dual independent slot-filling, then a row diff (Easterbrook); one scenario per row; the missing or extra row shown as the human artefact | Per-table complete/disjoint check (ms–s, DMN); cross-table conjunction over shared state, reporting maximal overlaps | Each row's guard reachable (smoke test / vacuity) | Spec.: parametrised row enumeration; row coverage via `event`/`cover`. Exp.: scenario per row. Mutant per row | **G3**, on every edit (slot-filling diff even earlier, at G2) |
| **Frame (unchanged set)** | Show the one state variable the clause lets change or forbids changing, against the record | Divergence check vs effect, failure and cancellation tables under a boundary condition (e.g. cancel during write); plain SAT misses this | Witness that exercises the operation with the frame observable | Spec.: full-state snapshot before/after through `alpha`. Exp.: record scenario asserting untouched state. Mutant: R alters one frame variable. Miss: hidden state outside `alpha` | **G4** (needs environment states enumerated) |
| **Termination under timeout assumption** | Two traces (timeout fires / does not) judged against the record; check the timeout assumption is stated as an *environment* assumption | Well-separation: the store must not control the assumption (60/79 GR(1) specs failed this) | Bounded liveness in TLC/Apalache; rt-consistency (no dead end) | Spec.: timeouts as explicit actions in F → R replay. Bridge: trace validation exposes "always/never fires" (TraceLink). DRT misses non-termination (Cedar), so model checking or proof is required | **G4/G5** in the model; TraceLink-class defects at **G6** |
| **State × operation transition table** | Shortest trace (≤ about 5 steps) per cell from a record scenario; rejected-option cell refused | Every state × operation cell defined; consistent with typestate and failure tables | TLC: no never-enabled action, no deadlock; Alloy `run` non-empty | Spec.: Hypothesis `RuleBasedStateMachine` (rules = operations, preconditions = enabled cells, Bundles = handed-out objects) or model-generated sequences with per-step state comparison (Mocket/MBTCG). Exp.: scenario call sequences. Cell coverage gate | **G3** (missing cell, seconds) |
| **Environment actions** (concurrent caller, out-of-band actor, faults, cancellation) | Witness trace per environment scenario; check each non-commitment is classified correctly as system choice vs environment input | rt-consistency / realizability (∀ environment move ∃ allowed response), with environment actions as free transitions in TLC/Apalache; well-separation | Witnesses surviving adversarial schedules | Spec.: faults and cancellation as first-class model actions emitted by the generator (Remix, CCF `IsFault`, P#). Exp.: record fault scenarios. Miss: faults not in the alphabet | **G4** (plain SAT passes; needs the quantified check) |
| **History predicate over interval operations** | Minimal allowed and minimal forbidden history shown against the record scenario | Consistency with per-call contracts (linearizability w.r.t. the sequential R) | Witness histories; TLA+ model of the predicate checked non-vacuous | Spec.: R run concurrently, intervals recorded, Porcupine-style check with R's sequential mode; OmniLink/TLA+ for weaker predicates; Elle for isolation (§3). Exp.: concrete histories from scenarios. Cost: NP-complete; slows past about 200k ops | **G4** if modelled in TLA+, else **G6** |
| **Failure category / phase / effect / retry tables** | Per-row scenario and rejected-option refutation; added-commitment probe on each effect cell | Per-table complete/disjoint; cross-table with frame and state tables; retry × concurrency as divergence | Every category reachable (smoke/vacuity); fault injection points exist in R | Spec.: case-table bridge plus fault actions, asserting category, phase and effect per row; retries × concurrency via the history bridge. Exp.: record failure scenarios | **G3** |
| **Register of non-promises** | Two witnesses with different outcomes per entry (else the spec silently committed) | No clause elsewhere commits on the non-promised dimension: register entry ∧ clauses must admit at least two outcomes | Allowed-variant R (NonDex-style perturbation) still passes all spec checks | Spec./Exp.: tests must not assert on the dimension; **allowed-variant check**: every test passes on perturbing R; survivors mapping to the register auto-classified "intended" | **G2** (two witnesses); over-strict tests at **G8** |
| **Variation points / profiles** | Per-profile scenario; declared deviations checked narrow-only (§3 Liskov–Wing) | Typed profile schema; each profile value conjoined separately | One witness per profile value (normal + each deviation), not a fixed count of two | One parametrised suite with per-profile expected sets; optional features return UNSUPPORTED; fixed-projection consistency test where stability is promised | **G0** (schema lint) |

The non-commitment *types* cut across forms. Their oracle mechanisms are in §2.3.4. Each allowed outcome of each unspecified, profile-declared or indeterminate point needs a coverage event (§2.4).

---

## 4. Candidate pipelines

All three use non-editable gates, information-flow independence for the expectation family, and clause- and decision-revision IDs. They differ in where the formal weight sits.

### Pipeline A: Record-anchored, test-first, light formal core

Precedents: the order in Cunha & Macedo; TiCoder; Fit. Formal layers are added only where a form demands them (environment, history).

**Gate sequence.**
1. G0 lint of records' typed slots.
2. A **record-derived check set** is produced by lineage B, which sees records only: positive scenarios, rejected-option negatives, and expectation tests. This happens *before* the spec exists.
3. Lineage A writes the spec as typed slots.
4. G1 upward trace.
5. G2: the record-derived checks run against an executable rendering of each clause (Hypothesis property / Alloy `run` / Dafny call), plus added-commitment probes to a spec-blind judge.
6. G3 tables; G4 conjunction limited to shared-variable subsets; G5 vacuity.
7. R is built; G6 contract → PBT and state-machine conformance.
8. G7 coverage; G8 per-family kill and allowed-variant check.
9. TLA+ only for environment and history forms, with invariant-mutation probes.

**Expected failure modes.**
- Expectation tests over-strict where a scenario fixes values the decision leaves open, caught by the allowed-variant check.
- About 4% wrong generated tests that need triage, more often the negatives (Cunha & Macedo).
- A shared misreading if lineages A and B are correlated (Kim et al.).
- Weaker cross-form conflict detection than pipeline B, because there is no common logic.
- Agents stopping early unless the harness imposes per-clause obligations.

**Small trial on one operation.**
- Seed 10–20 clause mutants that contradict the record (lost case, added commitment, reinterpreted option), regenerate R, and count kills per family. This directly measures the central gap of §2.3.3.
- Rate of wrong tests and judge false alarms.
- Minutes per clause for human review of witnesses.
- Over-strict test count under the allowed-variant R.

### Pipeline B: Common-logic consistency core

Precedents: ReqCheck/Hanfor, EuRailCheck, SAT-LLM, FRET.

**Gate sequence.**
1. G0 lint.
2. **Dual independent slot-filling** of every decision by two lineages, then a mechanical diff. Difference witnesses go to a cross-family judge, and to a human on disagreement.
3. G1 trace.
4. Each normative form is translated into **one shared typed signature** (the abstract state) in one logic (SMT, Alloy, or TLA+ for temporal parts).
5. G3 per-table checks.
6. G4 conjunction with unsat cores in k-subsets, then rt-consistency/realizability with environment actions as inputs, plus a well-separation check.
7. G5 vacuity (interesting witnesses, smoke tests).
8. Unsat cores and witnesses kept as regression fixtures.
9. R generated or written at the same granularity; G6 replay + trace validation; G7–G9 as in §2.4.

**Expected failure modes.**
- The translation into the common logic is itself a faithfulness step, and a failure cannot separate translation error from source flaw (EuRailCheck).
- Solver UNKNOWN or timeouts (Bosch: 18 timeouts in one set; FRET: "unknown" on non-linear arithmetic).
- Mode variables collapse partitioning, so full runs take hours.
- Difference witnesses resolved by correlated judges.

**Small trial on one operation.**
- Replay the operation's records and count conflicts found against the brief's known history (tables that disagreed; contradictions missed by earlier checks).
- Time per incremental check vs per full check.
- Number of difference witnesses produced by dual slot-filling, and how many were genuine ambiguities vs translation noise.
- Share of findings that led to record clarification vs formalisation fixes. Bosch reported roughly 70/30 as its comparison point.

### Pipeline C: Single executable source plus an independently authored check set

Precedents: SpecTec, Arm ASL 2017, JEST, Cedar.

**Gate sequence.**
1. One executable formal source per operation; which one stays open (it could be R itself, Quint, or Lean).
2. Markdown prose and other models are **generated** from it, not written.
3. G2 diffs the generated prose against the records clause by clause (SpecTec-style back-generation used as a round-trip check).
4. A **differently structured high-level property set** is written from the records by a separate lineage that never sees the source. Reid rejected properties that restate the spec.
5. That property set is checked against the source (proof or model checking).
6. An expectation suite runs on R; an N-version leg uses DRT between R and an independently built second executable model (JEST/Cedar).
7. G5 vacuity, G8/G9 mutation.

**Expected failure modes.**
- A misreading in the single source propagates consistently into every generated layer; SpecTec can detect it only via the test suite.
- The independent property set drifts toward restating the source (common mode).
- The second executable shares the first one's reading if it is built from the spec rather than from the records.
- The per-feature cost of keeping one source executable.
- DRT misses rare inputs (Cedar non-termination).

**Small trial on one operation.**
- Number of disagreements between the independent property set and the source, and the share that trace to genuine misreadings. Arm found 12 in a heavily tested spec.
- Yield of the prose-regeneration diff.
- DRT disagreements between the two executables and how many route back to a record ambiguity (the Cedar pattern).
- Author-hours for the property set vs the source.

**Cross-pipeline trial design (*Inference*).** Run all three on the same operation with the same seeded misreading set. Compare per gate: first gate to fail, false-alarm rate, and human minutes. That yields the first direct measurement of whether prose-derived oracles catch what spec-derived ones miss.

---

## 5. Open questions and verification debt

**Open questions (no evidence found).**
1. Do prose-derived oracles catch spec misreadings that spec-derived oracles miss? No study compares them on the same faults.
2. What is the recall of round-trip and dual formalization on *shared* misreadings against an independent gold?
3. What is the precision of LLM faithfulness judges on API or behaviour specs? All measurements are from maths/Lean.
4. How many witnesses are needed, and how different must they be? No yield-per-implementation study exists.
5. Realizability checking has not been applied to a library or storage API.
6. Agents writing realizable specs or repairing unrealizable ones has not been studied.
7. Agents maintaining consistency as clauses accumulate has not been studied, and incremental consistency cost over a project's lifetime has not been measured.
8. No TLA+, P or Lean spec-mutation tool with published kill rates exists. TLA+-Bench's probe wording needs re-checking.
9. No per-family kill gate on a reference model has been tested. The §3 mutant-reference-model seed is untested directly.
10. Outcome-set oracles vs relaxation flags on cost and bug-finding have not been compared.
11. Agents authoring trace links, writing coverage annotations, or triaging spec-mutant survivors have not been measured.
12. No LLM trace recovery figures exist for requirement → test or prose → clause.
13. No refinement-check bridge (Dafny refinement, TLA+ mappings, FDR) has been measured as a model ↔ reference-model bridge, and no Alloy/Lean ↔ Python bridge evidence was found.
14. Common-mode error when one LLM writes both the spec and its tests from the same prose has not been measured, nor has an LLM refuter scored on spec-vs-prose mutants.
15. No head-to-head comparison of human-review artefacts (trace vs table vs paraphrase) for detecting translation errors exists.
16. Over-strictness of LLM-written acceptance tests has not been measured.

**Unreachable or not re-checked items** (to verify in a follow-up run):

| Item | Track | Status |
|---|---|---|
| Saarland tech report fb14-96-06 (complementary specification) | T1 | [unreachable] (503, bot wall) |
| Brilliant/Knight/Leveson N-version specification debugging | T1 | [unreachable], D lead |
| Kamsties et al. 2001 (ambiguities under-reported) | T1 | [unreachable] |
| FormalRx (ICML 2026) | T1 | abstract only |
| AeroReq2LTL arXiv 2604.21715 | T1 | abstract/extract only |
| Ricca et al. ICSE 2008; IST 2009 | T1/T3 | [unreachable] / abstract only; abstracts disagree on effort |
| Großer, Rukavitsyna, Jürjens REJ 2024 (templates) | T1 | abstract only |
| NL2CTL (ICFEM 2024) | T1 | [unreachable] |
| Alloy output-forms study (LNCS 10.1007/978-3-319-66197-1_11) | T1 | extract only |
| Mashkoor & Jacquot REJ 2017 (ProB animation evaluation) | T1 | [unreachable] |
| Hahn et al. arXiv 2206.01962; Coins arXiv 2608.13077 | T1 | abstract only |
| Req2LTL's definition of "correct" | T1 | internally inconsistent in the paper |
| PBR / Regnell et al. 2000 | T1 | extract only |
| Katis et al. CAV 2022 (FRET diagnosis) | T2 | [unreachable] |
| Beer et al. CAV 1997 (20% vacuous) | T2 | [unreachable]; figure secondhand via Kupferman–Vardi |
| Heitmeyer et al. TOSEM 1996 (SCR checker) | T2 | [unreachable] (DTIC 403) |
| van Lamsweerde, Darimont, Letier TSE 1998 | T2 | [unreachable] |
| Zave & Jackson TOSEM 1993 | T2 | [unreachable], abstract only |
| EuRailCheck ASE 2009 "almost thirty railway experts" | T2 | snippet only |
| ECEASST 2018 model checking vs SMT | T2 | [unreachable] |
| Leino & Wüstholz CAV 2015; iProperty ICSE 2014; ICLP 2020 push/pop | T2 | [unreachable] |
| Watt & Rao FM 2021 (two Wasm mechanisations) | T2 | [unreachable] |
| TLC coverage official docs; TLC never-enabled warnings | T2/T4 | wiki draft (B) / practitioner threads (C) |
| PROPAS venue; DMN venue; AlgoVeri (read via grep) | T2 | not verified |
| Fedchin et al. NFM 2023 (DTest) | T3 | [unreachable] (404) |
| Hughes: AUTOSAR, Dropbox, "Experiences with QuickCheck" | T3 | [unreachable] |
| CrossHair, deal | T3 | not fetched |
| FoundationDB SIGMOD 2021; Jepsen nemesis; Coyote | T3 | not fetched |
| AWS "Systems Correctness Practices" CACM 2025 | T3/T4 | [unreachable] (403) |
| Cirstea et al. venue; CCF NSDI venue | T3 | not verified |
| Bisharat et al. arXiv 2606.05792 | T3 | abstract only |
| SysMoBench Table 3 | T3 | parsed from text extraction; re-check |
| PObserve | T3 | no measured data published |
| Melnik et al. Agile 2006; Haugset & Stålhane | T3 | [unreachable] / not fetched |
| Selby, Basili, Baker TSE 1987 (Cleanroom) | T3 | [unreachable] |
| NASA IV&V ROI data | T3 | not retrieved |
| NonDex ICST 2016 | T3 | [unreachable]; figures via workshop paper |
| Huo & Clause FSE 2014 | T3 | [unreachable] |
| OpenAI "Introducing SWE-bench Verified" | T3 | [unreachable] (403) |
| Patel & Hierons 2019; Guderlei & Mayer 2007 | T3 | lead only |
| Mäder & Egyed EMSE 2015 | T4 | abstract only |
| DO-178C (RTCA) text; ISO 26262; OSLC/ReqIF; StrictDoc link-failure behaviour | T4 | [unreachable] / not fetched / unconfirmed |
| μAlloy demo (ICSE 2018); μAlloyτ | T4 | [unreachable] / extract |
| Black, Okun, Yesha ASE 2000; Ammann & Black | T4 | [unreachable] |
| Papadakis et al. ICSE 2018; Papadakis et al. 2019 survey | T4 | [unreachable]; coefficients unverified |
| Whalen et al. ISSTA 2006 + follow-up (UFC coverage) | T4 | [unreachable] |
| Gay et al. TSE 2015 | T4 | first pages only |
| cosmic-ray, mutatest; Quint/P coverage docs | T4 | not fetched |
| AIRE'25 ensembles; TraceLLM; "Prompts Matter"; Klemens thesis; arXiv 2010.06505 | T4 | leads / abstract only |
| Knight & Leveson 1986; Eckhardt–Lee; Littlewood–Miller | T5 | [unreachable] |
| Snook & Harrison 2004; Finney 1996; Zimmerman RSML | T5 | [unreachable] / leads |
| FRET NTRS 20200002241; Kiro; ESMeta later papers; Sail | T5 | [unreachable] / not fetched |
| FormalAlign venue | T1/T5 | notes disagree (A, ICLR 2025 vs A-pre, venue unverified) |

---

## 6. Sources with grades

"Agents" = whether LLMs or agents were measured doing the step.

| Source | Grade | Full text | Agents | Used for |
|---|---|---|---|---|
| Amrollahi, Lopez, Barrett, Roundtrip verification, [arXiv 2604.25031](https://arxiv.org/abs/2604.25031) | A-pre | yes | yes | T1 round-trip; Clover qualification |
| Poiroux et al., EMNLP 2025, [arXiv 2406.07222](https://arxiv.org/abs/2406.07222) | A | yes | yes | equivalence precision/recall |
| Lu et al., FormalAlign, [arXiv 2410.10135](https://arxiv.org/abs/2410.10135) | A / A-pre (venue disputed) | yes | yes | LLM judge precision |
| Saha et al., NeuroSTAR, [arXiv 2609.03161](https://arxiv.org/abs/2609.03161) | A-pre | yes | yes | difference witnesses |
| Easterbrook & Callahan, RE'97, [NTRS](https://ntrs.nasa.gov/api/citations/19970007163/downloads/19970007163.pdf) | A | yes | no | dual formalization |
| Mavridou et al., FRET Lockheed Martin, RE 2020, [NTRS](https://ntrs.nasa.gov/citations/20205000433) | A | yes | no | FRETish, simulation |
| Greenman et al., Programming 2023, [arXiv 2211.01677](https://arxiv.org/abs/2211.01677) | A | yes | no | human misreading of LTL |
| Req2LTL, ASE 2025, [arXiv 2512.17334](https://arxiv.org/abs/2512.17334) | A | yes | yes | structured IR |
| Ricca et al., IWPSE 2007, [PDF](https://profs.scienze.univr.it/ceccato/papers/2007/iwpse2007.pdf) | A-workshop | yes | no | Fit tables |
| Ricca et al., ECEASST 2007, [PDF](https://profs.scienze.univr.it/ceccato/papers/2007/evol2007.pdf) | A-workshop | yes | no | Fit, separate acceptance suite |
| Cosler et al., nl2spec, CAV 2023, [arXiv 2303.04864](https://arxiv.org/abs/2303.04864) | A | yes | yes | intent-judged correctness |
| Lahiri, FMCAD 2024, [arXiv 2406.09757](https://arxiv.org/abs/2406.09757) | A | yes | yes | spec soundness/completeness |
| Cunha & Macedo, [arXiv 2510.23350](https://arxiv.org/abs/2510.23350) | A-pre | yes | yes | spec-blind pos/neg tests |
| Jovanovic & Sullivan, SEFM 2024, [PDF](https://par.nsf.gov/servlets/purl/10615156) | A | yes | no | under/over-constraint |
| Quint docs, [checking properties](https://quint.sh/docs/checking-properties) | B | yes | — | witnesses |
| Langenfeld et al., RE 2019, [PDF](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf) | A | yes | no | Bosch consistency, rt, vacuity |
| Becker et al., Hanfor, REFSQ 2021, [PDF](https://ultimate-pa.github.io/hanfor/references/publications/hanfor-semantic-requirements-review-at-scale.pdf) | A-workshop | yes | no | process, re-review |
| Cimatti et al., EuRailCheck, FMA 2010, [arXiv](https://arxiv.org/pdf/1003.1741v1.pdf) | A-workshop | yes | no | common logic, translation vs source |
| Filipovikj et al., PROPAS, [PDF](https://www.es.mdh.se/pdf_publications/4980.pdf) | A (venue unverified) | yes | no | SMT consistency |
| Fazelnia et al., SAT-LLM, [PDF](https://par.nsf.gov/servlets/purl/10574434) | A-pre | yes | yes | LLM vs LLM+SMT conflicts |
| Calvanese et al., DMN tables, [arXiv 1603.07466](https://arxiv.org/pdf/1603.07466) | A-pre | yes | no | table check cost |
| TableWise NASA page, [link](https://shemesh.larc.nasa.gov/fm/oldfm/fm-old-sw-ver-tablewise.html) | C | yes | no | BDD table checks |
| van Lamsweerde & Letier, Monterey, [PDF](https://webperso.info.ucl.ac.be/~avl/files/avl-MontereyLNCS.pdf) | A-workshop | yes | no | divergence |
| Degiovanni et al., ASE 2018, [PDF](https://nmaguirre.github.io/assets/pdf/ase2018.pdf); critique [arXiv 2203.12903](https://arxiv.org/pdf/2203.12903) | A; A-pre | yes | no | boundary conditions |
| Nuseibeh, Easterbrook, Russo 2000, [PDF](https://typeset.io/pdf/leveraging-inconsistency-in-software-development-4me5sgffk1.pdf) | A | yes | no | local ≠ global consistency |
| Mavridou et al., FRET compositional realizability, FM 2021, [NTRS](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf) | A | yes | no | realizability |
| Maoz & Shalom, ICSE 2021, [arXiv 2103.00297](https://arxiv.org/pdf/2103.00297) | A | yes | no | unrealizable cores |
| Maoz & Ringert, FSE 2016, [PDF](https://zenodo.org/api/records/6577097/files/well-separation-fse16.pdf/content) | A | yes | no | well-separation |
| Kupferman & Vardi, CHARME 1999, [PDF](https://typeset.io/pdf/vacuity-detection-in-temporal-model-checking-290v578apa.pdf) | A | yes | no | vacuity |
| Blanchard et al., TAP 2024, [PDF](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf) | A | yes | no | smoke tests |
| Dafny proof dependencies blog, [link](https://dafny.org/blog/2023/10/27/proof-dependencies/); Dafny ref `{:axiom}`, [link](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/Attributes.md) | B | yes | no | vacuity, axioms |
| Dafny wiki Cautionary Tales, [link](https://raw.githubusercontent.com/wiki/dafny-lang/dafny/Cautionary-Tales.md) | C | yes | no | negate-postcondition smoke test |
| Lean 4 reference, Axioms, [link](https://lean-lang.org/doc/reference/latest/Axioms/) | B | yes | — | `#print axioms` |
| Alloy tutorial, [link](https://alloytools.org/tutorials/online/maintext-FS-2.html) | B | yes | — | bounded results |
| ProofPulse, [arXiv 2608.30818](https://arxiv.org/pdf/2608.30818) | A-pre | yes | no | proof coverage |
| Vericoding, [arXiv 2509.22908](https://arxiv.org/pdf/2509.22908) | A-pre | yes | yes | weak specs (§3 qualification) |
| AlgoVeri, [arXiv 2602.09464](https://arxiv.org/html/2602.09464v2) | A-pre | yes (grep) | yes | weak specs (§3 qualification) |
| ReForm, [arXiv 2507.16331](https://arxiv.org/pdf/2507.16331) | A-pre | yes | yes | weak-spec drift |
| SpecRL, [arXiv 2604.05820](https://arxiv.org/pdf/2604.05820) | A-pre | yes | yes | spectests |
| W3C Process, [link](https://www.w3.org/policies/process/); RFC 6410, [link](https://www.rfc-editor.org/rfc/rfc6410.txt); Wasm phases, [link](https://raw.githubusercontent.com/WebAssembly/meetings/main/process/phases.md) | B | yes | — | witness conventions |
| Watt, CPP 2018, [PDF](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf) | A | yes | no | mechanisation vs implementations |
| Davis et al., PVLDB 2020, [arXiv 2006.00915](https://arxiv.org/abs/2006.00915) | A | yes | no | MBTCG, MBTC negative result |
| Wang et al., Mocket, EuroSys 2023, [PDF](https://gaoyu-cn.github.io/paper/2023-eurosys-mocket.pdf) | A | yes | no | guided testing |
| Ouyang et al., Remix, EuroSys 2025, [arXiv 2409.14301](https://arxiv.org/abs/2409.14301) | A | yes | no | conformance replay |
| Kuprianov & Konnov, TLA+ Conf 2020 slides, [link](https://conf.tlapl.us/2020/09-Kuprianov_and_Konnov-Model-based_testing_with_TLA_+_and_Apalache-Slides.pdf) | C | yes | no | Apalache MBT |
| Quint Connect posts, [launch](https://quint-lang.org/posts/quint_connect), [Emerald](https://quint-lang.org/posts/quint_connect_emerald) | C | yes | yes (n = 1) | agent MBT driver |
| Fedchin, DTest author page, [link](https://sasha-fedchin.github.io/2024/12/06/dtest.html) | B | yes | no | Dafny test generation |
| Deligiannis et al., FAST 2016, [PDF](https://www.doc.ic.ac.uk/~afd/papers/2016/FAST.pdf) | A | yes | no | P#, environment cost |
| PObserve docs, [link](https://p-org.github.io/P/advanced/pobserve/pobserve) | B | yes | no | log monitoring (no data) |
| icontract-hypothesis README, [link](https://raw.githubusercontent.com/mristin/icontract-hypothesis/master/README.rst) | B | yes | no | contract → strategy |
| Hypothesis stateful docs, [link](https://hypothesis.readthedocs.io/en/latest/stateful.html); API, [link](https://hypothesis.readthedocs.io/en/latest/reference/api.html) | B | yes | — | state machines, events |
| Vikram et al., [arXiv 2307.04346](https://arxiv.org/abs/2307.04346) | A-pre | yes | yes | LLM PBTs |
| Maaz et al., Agentic PBT, [arXiv 2510.09907](https://arxiv.org/abs/2510.09907) | A-workshop | yes | yes | agentic PBT |
| PBT-Bench, [arXiv 2605.15229](https://arxiv.org/abs/2605.15229) | A-pre | yes (abstract, setup) | yes | LLM PBT recall |
| Porcupine README, [link](https://raw.githubusercontent.com/anishathalye/porcupine/master/README.md); blog, [link](https://anishathalye.com/testing-distributed-systems-for-linearizability/) | B; C | yes | no | history checking |
| Hackett et al., OmniLink, [arXiv 2601.11836](https://arxiv.org/abs/2601.11836) | A-pre | yes | no | Porcupine cost challenge |
| FoundationDB testing docs, [link](https://apple.github.io/foundationdb/testing.html) | B | yes | no | deterministic simulation |
| Disselkoen et al., Cedar, FSE 2024, [arXiv 2407.01688](https://arxiv.org/abs/2407.01688) | A | yes | no | DRT; Lean challenge |
| Cedar extended, [arXiv 2403.04651](https://arxiv.org/pdf/2403.04651) | A-pre | yes | no | Lean model pipeline |
| Cirstea et al., [arXiv 2404.16075](https://arxiv.org/abs/2404.16075) | A-pre | yes | no | trace validation |
| Howard et al., CCF, [arXiv 2406.17455](https://arxiv.org/abs/2406.17455) | A/A-pre | yes | no | trace validation cost |
| Hackett & Beschastnikh, TraceLink, OOPSLA 2025, [PDF](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf) | A | yes | no | environment-assumption bugs |
| SysMoBench, [arXiv 2509.23130](https://arxiv.org/abs/2509.23130) | A-pre | yes | yes | agent TLA+ conformance |
| Konnov, TLA+ Community Meeting 2026, [slides](https://conf.tlapl.us/2026-etaps/konnov-2026.pdf) | C | yes | yes (n = 2) | AI harnesses |
| Bisharat et al., [arXiv 2606.05792](https://arxiv.org/abs/2606.05792) | A-pre | abstract only | yes | NL → TLA+ |
| Binamungu & Maro, BDD mapping, [arXiv 2305.05567](https://arxiv.org/abs/2305.05567) | A | yes | n/a | BDD evidence gap |
| Karpurapu et al., [arXiv 2403.14965](https://arxiv.org/pdf/2403.14965) | A-pre | yes | yes (syntax) | LLM Gherkin |
| Sami et al., [arXiv 2504.07244](https://arxiv.org/pdf/2504.07244) | A-pre | yes | yes (usefulness) | LLM acceptance tests |
| Fonseca et al., AToMIC, [arXiv 2510.18861](https://arxiv.org/pdf/2510.18861) | A-pre | yes | yes (syntax) | LLM UI tests |
| Fakhoury et al., TiCoder, TSE 2024, [arXiv 2404.10100](https://arxiv.org/pdf/2404.10100) | A | yes | yes | tests as intent check |
| Leveson et al., TSE 1990, [PDF](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf) | A | yes | no | spec-only checks |
| Barr et al., TSE 2015, [PDF](https://discovery.ucl.ac.uk/id/eprint/1471263/1/06963470.pdf) | A | yes | n/a | pseudo-oracles |
| Konstantinou et al., [arXiv 2410.21136](https://arxiv.org/abs/2410.21136) | A-pre | yes | yes | oracle pull |
| Zhao, Zhou, Cohen, ISSTA 2026, [arXiv 2607.22883](https://arxiv.org/pdf/2607.22883) | A | yes | yes | misguided tests |
| Mathews & Nagappan, [arXiv 2412.14137](https://arxiv.org/abs/2412.14137) | A-pre | yes | yes | pass-only filtering |
| Canedo, oracle anchoring, [arXiv 2608.17214](https://arxiv.org/pdf/2608.17214) | A-pre | yes | no | anchoring lint |
| Wang, Pradel, Liu, PatchDiff, ICSE 2026, [arXiv 2503.15223](https://arxiv.org/abs/2503.15223) | A | yes | yes | loose suites |
| Gyori et al., NonDex, JPF 2016, [PDF](https://mir.cs.illinois.edu/gyori/pubs/jpf16.pdf) | A-workshop | yes | no | underdetermined specs |
| WebAssembly interpreter README, [link](https://raw.githubusercontent.com/WebAssembly/spec/main/interpreter/README.md); relaxed-SIMD Overview, [link](https://raw.githubusercontent.com/WebAssembly/relaxed-simd/main/proposals/relaxed-simd/Overview.md); .wast, [link](https://raw.githubusercontent.com/WebAssembly/spec/main/test/core/relaxed-simd/relaxed_madd_nmadd.wast) | B | yes | — | set-valued oracles |
| sqllogictest about.wiki (mirror), [link](https://raw.githubusercontent.com/gregrahn/sqllogictest/master/about.wiki) | B | yes | — | canonicalisation |
| JSON-Schema-Test-Suite README, [link](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/README.md) | B | yes | — | optional tests |
| Open POSIX result codes, [link](https://raw.githubusercontent.com/linux-test-project/ltp/master/testcases/open_posix_testsuite/Documentation/HOWTO_ResultCodes) | B | yes | — | UNSUPPORTED/UNRESOLVED |
| OpenFastTrace docs/source, [report](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/console_tracing_report.md) | B | yes | — | trace gates |
| sphinx-needs config, [link](https://sphinx-needs.readthedocs.io/en/latest/configuration.html) | B | yes | — | trace gates |
| Doorstop validation, [link](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/docs/cli/validation.md) | B | yes | — | suspect links |
| StrictDoc guide, [link](https://strictdoc.readthedocs.io/en/stable/stable/docs/strictdoc_01_user_guide.html) | B (partial) | partial | — | trace tool |
| Mäder & Egyed, EMSE 2015, [abstract](https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f/full) | A | abstract only | no | trace benefit |
| Fuchß et al., LiSSA, ICSE 2025, [PDF](https://publikationen.bibliothek.kit.edu/1000179816/164563088) | A | yes | yes | LLM trace recovery |
| Goldweber et al., IronSpec, OSDI 2024, [PDF](https://par.nsf.gov//servlets/purl/10550356) | A | yes | no | spec mutation |
| Amaral et al., MutDafny, [arXiv 2511.15403](https://arxiv.org/html/2511.15403v1) | A-pre | yes | indirect | weak specs |
| Jovanovic, Patwary, Sullivan, FormaliSE 2025, [PDF](https://allisonius.github.io/files/FormaliSE2025.pdf) | A | yes | no | Alloy mutation adequacy |
| TLA+-Bench, [arXiv 2607.23425](https://arxiv.org/pdf/2607.23425) | A-pre | yes | yes | vacuity probe |
| TLA-Prover, [arXiv 2606.06133](https://arxiv.org/pdf/2606.06133) | A-pre | yes | yes | tiered gates |
| Richter & Wehrheim, NL2Contract, [arXiv 2510.12702](https://arxiv.org/pdf/2510.12702) | A-pre | yes | yes | contract completeness |
| mutmut README, [link](https://raw.githubusercontent.com/boxed/mutmut/main/README.rst) | B | yes | — | Python mutation |
| Petrović et al., ICSE-SEIP 2021, [arXiv 2103.07189](https://arxiv.org/abs/2103.07189) | A | yes | no | mutation at Google |
| Wang et al., TOSEM 2025, [arXiv 2406.09843](https://arxiv.org/pdf/2406.09843) | A | yes | yes | LLM mutants |
| Meta ACH, FSE Companion 2025, [arXiv 2501.12862](https://arxiv.org/pdf/2501.12862) | A | yes | yes | agentic mutation testing |
| Just et al., FSE 2014, [PDF](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf) | A | yes | no | coupling |
| Chekam et al., ICSE 2017, [PDF](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf) | A | yes | no | strong mutation |
| Gay et al., TSE 2015, [preprint](https://www.greggay.com/pdf/15covrisks.pdf) | A | first pages | no | §5(b) coverage |
| Inozemtseva & Holmes, ICSE 2014, [PDF](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf) | A | yes | no | §5(b) coverage |
| TLA+ wiki coverage, [link](https://docs.tlapl.us/_export/raw/using:coverage) | B (draft) | yes | — | action coverage |
| QuickCheck Haddock, [link](https://hackage.haskell.org/package/QuickCheck-2.14.3/docs/Test-QuickCheck.html) | B | yes | — | `checkCoverage` |
| Hughes, How to Specify It!, TFP 2019, [PDF](https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf) | A | yes | no | property types |
| Goldstein et al., ICSE 2024, [PDF](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf) | A | yes | no | PBT adequacy practice |
| Kim et al., ICML 2025, [arXiv 2506.07962](https://arxiv.org/pdf/2506.07962) | A | yes | yes | correlated errors |
| Huang et al., ICLR 2024, [arXiv 2310.01798](https://arxiv.org/pdf/2310.01798) | A | yes | yes | self-correction |
| Kamoi et al., TACL, [arXiv 2406.01297](https://arxiv.org/pdf/2406.01297) | A | yes | yes | external feedback |
| Panickssery et al., NeurIPS 2024, [arXiv 2404.13076](https://arxiv.org/pdf/2404.13076) | A | yes | yes | self-preference |
| CodeJudgeBench, [arXiv 2507.10535](https://arxiv.org/pdf/2507.10535) | A-pre | yes | yes | judge noise |
| Jin & Chen, [arXiv 2603.00539](https://arxiv.org/pdf/2603.00539) | A-pre | yes | yes | overcorrection |
| Broccia et al., [arXiv 2608.21298](https://arxiv.org/pdf/2608.21298) | A-pre | yes | yes | LLM-assisted inspection |
| Smit et al., ICML 2024, [arXiv 2311.17371](https://arxiv.org/pdf/2311.17371) | A | yes | yes | debate |
| Choi et al., [arXiv 2508.17536](https://arxiv.org/pdf/2508.17536) | A-pre | yes | yes | debate vs vote |
| McAleese et al., code critic, [arXiv 2407.00215](https://arxiv.org/pdf/2407.00215) | A-pre | yes | yes | planted-bug refuter |
| Zhang et al., Beyond Compilation, [arXiv 2606.31002](https://arxiv.org/pdf/2606.31002) | A-pre | yes | yes | cross-family judges, judge aging |
| MathAtlas, [arXiv 2605.14061](https://arxiv.org/pdf/2605.14061) | A-pre | yes | yes | judge transfer |
| Mohammad & Sheikh, Faithfulness Gap, [arXiv 2606.16541](https://arxiv.org/pdf/2606.16541) | A-pre (caution) | yes | yes | drift detection |
| Reid, OOPSLA 2017, [PDF](https://alastairreid.github.io/papers/oopsla2017-whoguardstheguards.pdf); FMCAD 2016, [PDF](https://alastairreid.github.io/papers/fmcad2016-trustworthy.pdf) | A | yes | no | independent property set; §5(c) |
| JEST, ICSE 2021, [arXiv 2102.07498](https://arxiv.org/pdf/2102.07498) | A | yes | no | N+1-version; §5(c) |
| Youn et al., SpecTec, PLDI 2024, [PDF](https://people.mpi-sws.org/~rossberg/papers/Youn,%20Shin,%20Lee,%20Ryu,%20Breitner,%20Gardner,%20Lindley,%20Pretnar,%20Xiaojia,%20Watt,%20Rossberg%20-%20Bringing%20the%20WebAssembly%20Standard%20up%20to%20Speed%20with%20SpecTec.pdf) | A | yes | no | §5(c) |
| Czepa et al., SoSyM 2019, [PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6944266/fullTextXML) | A | yes | no | §5(a) |
| Mavridou, Farrell, Vázquez et al. 2025, [arXiv 2512.15788](https://arxiv.org/pdf/2512.15788) | A-pre (claim C-level) | yes | anecdotal | §5(a); FRET oracle |
| GitHub Spec Kit, [spec-driven.md](https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md) | D/B | yes | no data | §5(c) |
