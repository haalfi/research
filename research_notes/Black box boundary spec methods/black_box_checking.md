# Black-box conformance checking against a boundary spec, and what each spec form can check by itself

Method note: in this session the WebFetch tool and direct HTTPS were refused by the egress proxy for every academic host tried (amazon.science, arxiv.org, vldb.org, cs.utexas.edu, ucl.ac.uk). All findings below therefore come from search-engine extracts of primary pages (abstracts, READMEs, official docs), plus a few items from prior knowledge. Items from prior knowledge are marked **[unverified this session]**. Grades: A = peer-reviewed or measured; B = industrial practice with data; C = practitioner report without data; D = opinion or marketing.

Running example used for the inferences: `open(key) -> ReadStream`, which the caller consumes and closes. The hard cases are (a) a failure mid-read after `open` returned, (b) a concurrent writer to the same key, and (c) use after close. No semantics are decided here. The inferences only show how each technique would observe or constrain these cases.

---

## Q1. Conformance testing theory: ioco, MBT taxonomy, Spec Explorer, quiescence, nondeterminism and underspecification

### Takeaway
ioco gives a precise black-box meaning of "conforms". After any trace the spec allows, the implementation may only produce outputs the spec allows, and "no output" (quiescence) counts as an observable output. Unspecified *inputs* are left free (the implementation may do anything), while nondeterministic *outputs* are honoured as a set of allowed outputs. Industrial MBT at Microsoft (Spec Explorer, Windows protocol documentation) shows this scales, but the strongest scale figure comes from a single self-reported source.

### Cited Findings
- ioco defines conformance as a relation between a model, given as an input-output labelled transition system (IOLTS), and an implementation under test. It rests on the *test hypothesis* that the implementation behaves like some IOLTS the tester does not know. (A) — [Tretmans, ioco lecture slides, HH CERES wiki](https://wiki.hh.se/ceres/images/d/d4/Luthman_hsst_2016.pdf); summarised in [Spinal Test Suites for SPLs, arXiv 1403.7260](https://arxiv.org/pdf/1403.7260)
- Quiescence is the observable absence of output: a state that will produce nothing without a new input. ioco models it as a special output action δ. A test passes on silence only if the spec permits silence in that state, and fails otherwise. (A) — [Spinal Test Suites, arXiv 1403.7260](https://arxiv.org/pdf/1403.7260); [Quasimodo D4.5](https://quasimodo.aau.dk/Final/Quasimodo-D4.5.pdf)
- ioco allows underspecification in two ways. (1) Unspecified inputs may be implemented arbitrarily ("positive testing", which relies on optimistic environment assumptions). (2) Outputs may be nondeterministic: the implementation must show *at most* the outputs the spec allows, and quiescence forces it to show *at least one* specified output where the spec does not allow silence. (A) — [arXiv 1403.7260](https://arxiv.org/pdf/1403.7260)
- ioco extends to compositional testing under restrictions (van der Bijl, Rensink, Tretmans 2003). (A) — [Compositional testing with ioco](https://ftp.cs.ru.nl/CSI/SoftwEng.FunctLang/papers/2003/bijm2003-compositional_testing_ioco.pdf)
- The MBT taxonomy of Utting, Pretschner and Legeard (STVR 22(5):297–312, 2012, doi 10.1002/stvr.456) classifies approaches along a model dimension (subject, redundancy, characteristics such as deterministic/nondeterministic and timed, paradigm), a test-generation dimension (selection criteria, technology) and a test-execution dimension (online/offline). The 2006 working paper described seven dimensions. (A) — [Waikato repository](https://researchcommons.waikato.ac.nz/handle/10289/6393); [2006 working paper](https://docs.artemis.ase.in.tum.de/lehrstuhl_1/files/teaching/ws0708/ManagementSoftwareTesting/uow-cs-wp-2006-04.pdf). The dimension names come from prior knowledge of the paper **[unverified this session]**. The search extract confirmed only "taxonomy covering key aspects, applied to three tools".
- Spec Explorer at Microsoft: from 2002, as a consequence of a consent decree with the US DoJ, Microsoft had to verify its Windows protocol documentation, and Grieskamp's team applied model-based testing to it. Models are written in C# with "Cord" configuration scripts. The papers are ICST 2008 ("Model-Based Quality Assurance of Windows Protocol Documentation") and the 2011 CACM case study "Microsoft's protocol documentation program: interoperability testing at scale". (A for papers) — [Wikipedia: Spec Explorer](https://en.wikipedia.org/wiki/Spec_Explorer); [CACM 2011 case study](https://cacmb4.acm.org/magazines/2011/7/109908-microsofts-protocol-documentation-program); [Grieskamp et al. 2011 record](https://repositoriosdigitales.mincyt.gob.ar/vufind/Record/CONICETDig_c68bda0856b57e85543ae9443287fe53)
- Scale claim: Spec Explorer was applied to thousands of pages of Windows protocol specs, in a project of "more than 250 person years". This figure is self-reported by Kicillof in a trade-press article and was not independently verified. (D/C: press quote) — [eWeek](https://www.eweek.com/development/microsoft-delivers-its-spec-explorer-model-based-testing-tool)
- Grieskamp, Kicillof, Stobie and Braberman (2011) conclude that MBT "works and scales, provided it is accompanied by sound tool support and clear methodological guidance". (A) — [record](https://repositoriosdigitales.mincyt.gob.ar/vufind/Record/CONICETDig_c68bda0856b57e85543ae9443287fe53)

### Inferences
- *Inference:* For `open → stream`, ioco's split maps cleanly onto the boundary spec. "Unspecified" behaviour after use-after-close (if the spec leaves it open) is an *unspecified input*, so the oracle must not fail any outcome there. A spec that says "read after close raises X or returns EOF" is *nondeterministic output*, so the oracle accepts either. These are two different spec statements, and the spec form must be able to tell them apart.
- *Inference:* Quiescence is the theoretical home for "failure timing". A read that blocks forever is observable as δ, so the spec must say whether δ is allowed after a backend fault (e.g. "eventually raises or returns"). In practice testers approximate δ with a timeout. That is an engineering assumption, not part of the theory.
- *Inference:* ioco's "at most allowed outputs" means a spec with a rich *error* alphabet (typed errors) gives the oracle much more to check than "raises some exception".

### Gaps
- TorXakis (the ioco-based tool from Radboud/ESI) was not researched: no search budget was left. No industrial data on it was found.
- The original Tretmans 1996/2008 papers were not retrieved directly. Only slides and secondary descriptions were available.
- Spec Explorer defect counts or cost-per-page data beyond the 250 person-years quote were not found.

---

## Q2. Property-based and stateful testing; linearizability and history checking; parallel state-machine testing

### Takeaway
Stateful PBT uses an executable *model* (a state machine with preconditions, next-state functions and postconditions) as the oracle for random API call sequences, and shrinks failures to minimal sequences. The industrial data is real (AUTOSAR/Volvo: more than 3,000 spec pages modelled, more than 200 issues). Concurrency is handled by recording a history of concurrent calls and checking whether any sequential interleaving the model allows explains it (linearizability), which is NP-complete in general. Elle sidesteps that for transactional isolation by designing workloads whose reads reveal version order.

### Cited Findings
- Arts, Hughes, Norell and Svensson (ICSTW 2015) wrote model-based acceptance tests for Volvo's AUTOSAR basic software. They turned more than 3,000 pages of specification into QuickCheck models and found more than 200 issues, which were raised with Volvo and the vendors. They report the approach as more efficient, effective and correct than the earlier manual one. (A/B) — [Chalmers record, "Testing AUTOSAR software with QuickCheck"](https://research.chalmers.se/en/publication/219899)
- Hughes's 2016 retrospective calls the Volvo project the largest QuickCheck effort to date. (C, reflective) — [Experiences with QuickCheck](https://research.chalmers.se/en/publication/232550)
- Hughes, Pierce, Arts and Norell (ICST 2016) built a formal, testable model of a file synchronizer's core behaviour. Their testing method for nondeterministic systems does *not* require the system's internal choices to be visible to the test framework. It found surprising behaviours in Dropbox (e.g. a newly created file deleted, data loss) and in other synchronizers. (A) — [Chalmers record](https://research.chalmers.se/en/publication/232551); [paper PDF](https://www.cis.upenn.edu/~bcpierce/papers/mysteriesofdropbox.pdf)
- Hypothesis `RuleBasedStateMachine`: rules are actions, `@precondition` filters which rules apply (preferred over `assume()`), and `@invariant` runs after every step. Preconditions cannot read bundles, so model state must live on the instance. (C, tool docs) — [Hypothesis stateful docs](https://hypothesis.readthedocs.io/en/latest/stateful.html); [Rule based stateful testing article](https://hypothesis.works/articles/rule-based-stateful-testing/)
- PULSE (Claessen, Palka, Smallbone, Hughes, Svensson, Arts, Wiger; ICFP 2009, doi 10.1145/1596550.1596574) combines QuickCheck, the PULSE user-level scheduler (random but replayable scheduling) and a trace visualiser to find race conditions in unit testing. The paper notes that ordinary unit tests cannot find races because they depend on timing. A related QuickCheck module tests that all API functions "behave atomically with respect to each other". (A) — [ICFP'09 accepted paper page](https://web.cecs.pdx.edu/~apt/icfp09_accepted_papers/70.html); [Chalmers record](https://research.chalmers.se/en/publication/125252)
- Porcupine (Go) checks linearizability given a *sequential specification as executable code* plus a concurrent history. It implements "Faster linearizability checking via P-compositionality", an optimisation of Lowe's "Testing for linearizability" (Knossos is based on the earlier Wing & Gong / Lowe line). The README claims 1,000–10,000x speedups over Knossos on the Jepsen test data (self-reported). Checking is NP-complete, so worst cases are exponential. (C/A) — [Porcupine pkg docs](https://pkg.go.dev/github.com/anishathalye/porcupine); [Athalye blog](https://anishathalye.com/testing-distributed-systems-for-linearizability); [GitHub issue 6](https://github.com/anishathalye/porcupine/issues/6)
- A 2026 comparison found Porcupine can take minutes to reject some large traces with few threads. (A, preprint) — [arXiv 2608.17388](https://arxiv.org/pdf/2608.17388)
- History checkers cannot prove linearizability. They only build confidence that it is not obviously violated. (C) — [Eaton, Checking linearizability in Go](https://notes.eatonphil.com/2024-10-31-checking-linearizability-in-go.html)
- Elle (Kingsbury & Alvaro, PVLDB 14(3):268–280, 2021) builds an Adya-style dependency graph from client-observed transactions. Workloads (e.g. list-append with unique values) are chosen so that reads reveal version order. It detects every Adya anomaly except predicate anomalies and explains each one. It aims for polynomial time, in contrast to NP-complete general serializability and linearizability checking. Knossos handles only about hundreds of transactions. (A) — [VLDB paper page](https://www.vldb.org/pvldb/volumes/14/paper/Elle%3A%20Inferring%20Isolation%20Anomalies%20from%20Experimental%20Observations); [arXiv 2003.10554](https://arxiv.org/abs/2003.10554); [Colyer summary](https://blog.acolyer.org/2020/11/23/elle/). Elle is described as roughly linear-time in practice in the paper body, per prior knowledge **[unverified this session]**. The search extract confirmed only the polynomial-time goal.
- Google LevelDB case study: QuickCheck state-machine tests found sequences (reportedly 17 and 31 calls long after shrinking) that lost or resurrected data. This is known from Hughes's talks **[unverified this session; no URL retrieved; treat as C]**.

### Inferences
- *Inference:* `open → stream` is a *resource-carrying* state machine. The model state needs per-handle entries (open, consumed-up-to-offset, closed, failed). Use-after-close then becomes a model transition whose postcondition is whatever the spec allows, possibly a set of outcomes. Hypothesis bundles or QuickCheck symbolic variables are the mechanism for threading the handle through generated sequences.
- *Inference:* A concurrent writer is the case where linearizability or snapshot reasoning is needed. The spec must state the *linearization point* of `open` (the snapshot is taken at open, versus reads seeing later writes). Without that, Porcupine/Knossos-style checking has no sequential spec to check against. A stream read is a *long-running operation* with many sub-observations, which history checkers model poorly unless each `read(n)` is recorded as its own operation.
- *Inference:* The Dropbox paper's technique of not requiring visibility of internal choices is directly relevant when backends differ in when they pick up concurrent writes. The model must carry the set of possible states, not a single state.

### Gaps
- No peer-reviewed measured data on Hypothesis stateful testing in industry was found.
- Lowe's paper ("Testing for linearizability", CCPE 2017) was not retrieved directly.

---

## Q3. Fault injection at the boundary for partial or deferred failure

### Takeaway
The core techniques are: inject faults while recording a client-side history and check that history against a model (Jepsen); make the whole system deterministic so that any fault interleaving replays from a seed (FoundationDB); and conformance-check the implementation against a small executable reference model under injected IO failures and crashes (ShardStore). Differential testing (comparing two implementations) and metamorphic testing (comparing related runs) supply oracles when no model exists.

### Cited Findings
- Jepsen architecture: a generator schedules operations for logically single-threaded client processes, a *nemesis* process injects faults (partitions, clock offsets and jumps, process kill and restart), the start and end of every operation are recorded in a history, and a checker (Knossos, Elle, ...) analyses it. (C, tool docs) — [Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md); [Jepsen tutorial: faults](https://cljdoc.org/d/io.jepsen/generator/0.1.2/doc/introducing-faults)
- Jepsen distinguishes *indeterminate* outcomes. A crashed or timed-out operation is recorded as "may or may not have taken effect" (`:info`), and checkers account for that. Returning a definite `:fail` only when the operation is known not to have happened lets the checker find more bugs. (C) — [Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md)
- FoundationDB (SIGMOD 2021, doi 10.1145/3448016.3457559) uses a deterministic simulation framework "to test every new feature under a myriad of possible faults". Physical interfaces are replaced by shims, the run loop by simulated time, and simulated disasters (machine failure, network clogging, "swizzling") run with the workloads. The BUGGIFY macro randomises code paths and makes faults more frequent than in reality. (A for the paper; C for the talk) — [CACM version](https://cacm.acm.org/?p=227399); [Strange Loop 2014 talk](https://thestrangeloop.com/2014/testing-distributed-systems-w-slash-deterministic-simulation.html); [slides](https://www.slideshare.net/slideshow/deterministic-simulation-testing/39333008)
- ShardStore (Bornholt et al., SOSP 2021, Best Paper): correctness is decomposed into independent properties, each checked by the most appropriate tool, with *executable reference models as specifications* checked against the implementation. This prevented 16 issues from reaching production, including subtle crash-consistency and concurrency bugs. The approach is "lightweight and automated" with "weaker guarantees than full formal verification — we can still miss bugs". It was extended by non-formal-methods engineers. ShardStore is about 40k lines of Rust. (A/B) — [paper PDF](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf); [SOS-VO copy](https://sos-vo.org/sites/sos-vo.org/files/sos_files/Using_Lightweight_Formal_Methods_to_Validate_a_Key-value_Storage_Node_in_Amazon_S3.pdf); [Amazon Science blog](https://www.amazon.science/blog/aws-team-wins-best-paper-award-for-work-on-automated-reasoning)
- ShardStore details from prior knowledge of the paper **[unverified this session]**: the reference model is a much smaller Rust implementation of the same trait. Property-based tests run random operation sequences, including injected disk-IO failures and simulated crashes and reboots, against both implementation and model. Crash consistency is checked by requiring post-crash state to match some persisted prefix, defined via dependency tracking. Concurrency is checked with stateless model checkers (Loom, and the then-new Shuttle).
- Cedar (AWS): verification-guided development. An executable Lean model has mechanically proven properties, and the Rust production code is checked against the model by *differential random testing* (millions of random inputs, compare outputs). Property-based testing covers the parts the model omits. Proofs found 4 bugs in the validator, and DRT plus PBT found 21 more. (A/B) — [arXiv 2407.01688](https://arxiv.org/pdf/2407.01688); [Amazon Science blog](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing)
- McKeeman, "Differential Testing for Software", Digital Technical Journal 10(1):100–107, 1998: generate random programs and compare multiple compilers. A companion patent covers testing two or more compilers this way. (A/B) — [DBLP](https://dblp.org/pid/40/4856); [US patent 5754860](https://patents.google.com/patent/US5754860)
- Metamorphic testing (Chen et al., ACM CSUR 51(1), 2018, doi 10.1145/3143561): *metamorphic relations* are necessary properties linking several inputs and their outputs. They serve as oracles when a single expected output cannot be computed. (A) — [HKU record](https://hub.hku.hk/handle/10722/254895); [Nottingham PDF](https://research.nottingham.edu.cn:443/files/31448151/51607.pdf)
- Wasmtime runs the WebAssembly spec reference interpreter as one engine in a differential fuzzing oracle. (C) — [wasmtime diff_spec.rs](https://docs.wasmtime.dev/api/src/wasmtime_fuzzing/oracles/diff_spec.rs.html)

### Inferences
- *Inference:* "Failure mid-read after `open` returned" is exactly a *deferred* failure. To check it from the boundary, the fault injector must act *between* calls: a backend shim (in the FoundationDB or ShardStore style) or a nemesis that kills the store while the handle is open. The oracle then needs a spec answer to "which errors may `read` raise after `open` succeeded, and must the stream be closable afterwards?" Jepsen's `:info` notion is the template for "the outcome may be either": a spec form needs an explicit *indeterminate* value.
- *Inference:* Differential testing across backends finds *divergence*, not *wrongness*. When the boundary spec permits several behaviours (e.g. snapshot vs. read-latest under a concurrent writer), raw differential comparison gives false alarms. It must be filtered through the spec's allowed-outcome set, or compared against a model that returns sets.
- *Inference:* Useful metamorphic relations for the running example include: reading a stream in chunks of size k gives the same bytes as reading all at once; closing twice behaves like closing once (if the spec says so); and opening the same key twice with no writer gives identical bytes.

### Gaps
- No measured comparison of the cost or yield of nemesis-style vs. simulation-style fault injection was found.
- The full text of the FoundationDB paper was not retrieved, so BUGGIFY's coverage in the paper itself is unconfirmed.

---

## Q4. Contract test suites shared across implementations, parameterised by declared capability

### Takeaway
The pattern is mature. One suite encodes the spec as executable tests, and each implementation supplies a *declaration file* of capabilities and known deviations. Tests skip or switch expectations based on that file. Hadoop's FileSystem contract is the closest analogue to a multi-backend library API. Language and VM suites (test262, Wasm spec tests, Java TCK) are large-scale examples of a shared black-box suite as the operational definition of conformance.

### Cited Findings
- Hadoop: the filesystem specification is accompanied by contract tests. Each aspect is configurable via contract options, so a filesystem "can declare how it diverges" from the standard contract. To add an unfixable FS-specific behaviour, a new option is added to `ContractOptions`, the test reacts to its presence, and per-filesystem XML contract files declare the feature or failure mode. Bindings for remote stores are given in `contract-test-options.xml` (`fs.contract.test.fs.<scheme>`). (B/C, project docs) — [Hadoop: Testing the Filesystem Contract (r3.0.2)](https://hadoop.apache.org/docs/r3.0.2/hadoop-project-dist/hadoop-common/filesystem/testing.html); [Extending the FS specification and its tests](https://hadoop.apache.org/docs/r2.6.3/hadoop-project-dist/hadoop-common/filesystem/extending.html); [Introduction (r3.4.0)](https://HADOOP.apache.org/docs/r3.4.0/hadoop-project-dist/hadoop-common/filesystem/introduction.html)
- From prior knowledge **[unverified this session]**: option keys such as `fs.contract.supports-append`, `fs.contract.is-blobstore` and `fs.contract.supports-seek-on-closed-file` live in per-store XML (e.g. `contract/s3a.xml`). Hadoop's `FSDataInputStream` spec explicitly covers seek and read on a closed stream. `append` is documented as an optional operation in the Java API. — [Hadoop FSDataOutputStream class-use (optional ops)](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/fs/class-use/FSDataOutputStream.html)
- WebAssembly: the spec repo holds the draft spec, the OCaml reference interpreter and the official test suite in an extended text format (`.wast`) with commands such as `assert_return` and `assert_trap (invoke ...) "<failure>"`. Engines translate these into their own harnesses (e.g. WebKit passes `assert_trap` if a `WebAssembly.RuntimeError` is thrown, which is a *weaker* check than matching the failure string). (C) — [WebAssembly/spec PR 268](https://github.com/WebAssembly/spec/pull/268/files); [WebKit stack.wast.js](https://webkit.googlesource.com/WebKit/+/5d26c89f08b81b8e08741577e164b9ab0701d9eb/JSTests/wasm/spec-tests/stack.wast.js)
- A third-party Wasm runner reports directives it cannot run as SKIPPED instead of FAILED. This is an example of capability-based reporting. (C) — [wasmtk wast docs](https://jsr.io/@jrmarcum/wasmtk/doc/wast/)
- test262 (ECMAScript), the Java TCK and the fsspec abstract test suites follow the same pattern (feature flags or front-matter in test262, profile-based TCKs, fsspec's abstract tests subclassed per implementation). **[unverified this session; no sources retrieved]** — [test262 repo](https://github.com/tc39/test262); [fsspec](https://filesystem-spec.readthedocs.io/)

### Inferences
- *Inference:* Capability declarations are themselves part of the spec. "Supports seek on closed file = false" is a declared variant. The suite must check that (a) every backend's declared capabilities are a permitted combination, and (b) the backend behaves per its declaration. Hadoop shows (b). Check (a) is a spec-internal consistency check that a schema can do (see Q5).
- *Inference:* The WebKit `assert_trap` example shows that harness translation can silently weaken the oracle (any trap vs. the specific trap). For the running example, a shared suite should assert typed errors, not just "raised".
- *Inference:* Contract suites check the *single-caller, deterministic* part of a spec well. They need the Q2 and Q3 machinery (histories, fault shims) for the concurrent-writer and mid-read-failure cases. Hadoop's contract tests are largely sequential, per prior knowledge **[unverified]**.

### Gaps
- No published measurements of defect yield for Hadoop contract tests, test262 or the Java TCK were found.
- The fsspec test layout and test262 feature-flag mechanics were not verified this session.

---

## Q5. What each spec form checks by itself vs. needs an implementation, model or proof

### Takeaway
There are three separate questions. (1) Is the spec internally consistent? Schemas, type checkers and model checkers answer this without any implementation. (2) Does a given implementation conform on the runs we tried? Only executing the implementation against an oracle answers it: an executable model, a contract suite, or a history checker. Trace validation and log-based conformance (TLA+ trace validation, PObserve) bridge a model-checked spec to implementation runs. (3) Does it conform on *all* runs? Only proof answers that (Cedar's Lean proofs are about the model; ShardStore explicitly accepts "we can still miss bugs").

### Cited Findings
- Model checking the spec itself: the P language models systems as communicating state machines with safety and liveness properties, and the P Checker systematically explores message interleavings and failures. It was used in S3's migration to strong read-after-write consistency to remove design-level bugs early. (B) — [Systems correctness practices at AWS, CACM / ACM Queue](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services); [ACM Queue](https://queue.acm.org/detail.cfm?id=3712057)
- Bridging spec to implementation: PObserve (AWS, 2023) takes structured logs from executions (in testing and production) and validates post hoc that they match behaviours the P specification allows. (B) — [CACM AWS article](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services)
- TLA+ trace validation (Cirstea, Kuppe, Loillier, Merz 2024): instrument Java programs, log updates to spec variables (possibly only some of them) and reduce trace validation to model checking with TLC. Discrepancies between spec and implementation were found in *all* systems studied. (A) — [arXiv 2404.16075](https://arxiv.org/pdf/2404.16075)
- The reverse direction (generate traces from the model, replay them on the implementation, compare) is unsound: it "could miss behaviors in implementation that are not modeled by the specification". (A, preprint) — [Multi-Grained Specifications, arXiv 2409.14301](https://arxiv.org/pdf/2409.14301)
- TraceLink (OOPSLA 2025) validates traces of PGo-generated Go against Modular PlusCal designs and found 9 previously undetected bugs, including one in the PGo compiler. (A) — [paper](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf)
- Executable model plus proof: Cedar proves properties *of the Lean model* and relies on DRT to tie the Rust code to the model. Proofs found 4 bugs, testing 21. (A) — [arXiv 2407.01688](https://arxiv.org/pdf/2407.01688)
- Executable model as oracle without proof: ShardStore accepts weaker guarantees than full verification. (A) — [ShardStore paper](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf)
- Alloy Analyzer (bounded relational model finding) and TLC check a spec's own invariants and consistency within finite bounds, not implementation conformance. This is standard tool documentation knowledge **[unverified this session]** — [Alloy](https://alloytools.org/); [TLA+](https://lamport.azurewebsites.net/tla/tla.html)

### Inferences
- *Inference*, a classification table for the writer:

| Spec form | Checks by itself (no implementation) | Checks an implementation (black box) | Needs proof for "all runs" |
|---|---|---|---|
| Schema / tables (operation × error × capability matrices) | Structure, completeness (every op has an error column), referential consistency, permitted capability combinations | Only by generating contract tests from it; the schema is not an oracle for sequences | — |
| Prose + examples | Nothing mechanically | Hand-written contract tests | — |
| Pre/postconditions (contracts) | Type and well-formedness; satisfiability if a solver is used | Runtime assertion checking at the boundary (single-call oracle) | Deductive verification |
| Executable reference model (state machine) | Model's own invariants via PBT on the model, or model checking if written in P/TLA+ | Stateful PBT, differential testing, linearizability checking (sequential model) | Refinement proof (Cedar does proofs only of the model) |
| Model-checked spec (TLA+, P, Alloy) | Consistency, deadlock, safety and liveness within bounds | Trace validation / PObserve over logs; MBT test generation (unsound in the generate-and-replay direction) | TLAPS or refinement proof |
| History-level consistency spec (linearizable, snapshot isolation) | — | Knossos / Porcupine / Elle over recorded histories | — |

- *Inference:* For the running example, the "can `read` fail after `open` succeeded, and is the handle still closable?" question is best stated in an executable model with explicit nondeterministic outcomes. A schema can only ensure that the question has *an* answer for every backend capability profile.
- *Inference:* "What other observers see" (a second caller, an external mutator) can only be checked from histories. That needs a consistency-level spec (linearizable at open, snapshot-per-stream, ...), not just per-call postconditions.

### Gaps
- No empirical comparison was found of defect yield from spec-internal checks vs. implementation conformance checks on the same project.
- Alloy, TLC and P checker semantics were not retrieved from primary docs this session.

---

## Q6. The test oracle problem (Barr et al. TSE 2015) and implications for spec forms

### Takeaway
Barr et al. frame the oracle as the bottleneck of test automation. They classify oracles as specified (from specs, models, contracts), derived (from documentation, other versions, metamorphic relations), implicit (crashes, exceptions, leaks) and human. A boundary spec's value for black-box checking is how much of it can serve as a *specified* oracle; whatever it leaves out falls back to derived, implicit or human oracles.

### Cited Findings
- Barr, Harman, McMinn, Shahbaz, Yoo, "The Oracle Problem in Software Testing: A Survey", IEEE TSE 41(5):507–525, 2015, doi 10.1109/TSE.2014.2372785. It defines the oracle problem as distinguishing correct from incorrect behaviour for a given input, argues that automating oracles removes the bottleneck in test automation, and reviews modelling, specifications, contract-driven development and metamorphic testing, with humans as the fallback. (A) — [UCL Discovery](https://discovery.ucl.ac.uk/1471263/); [PDF mirror](https://web.eecs.umich.edu/~weimerw/2018-481/readings/testoracles.pdf)
- The four-way classification (specified, derived, implicit, and handling the lack of an automated oracle) is the survey's structure, per prior knowledge **[unverified this session; the extract confirmed only the techniques listed]** — [PDF mirror](https://huang.isis.vanderbilt.edu/cs4278/readings/testoracles.pdf)
- Metamorphic relations are a derived-oracle answer to the oracle problem. (A) — [Chen et al. CSUR 2018](https://hub.hku.hk/handle/10722/254895)

### Inferences
- *Inference:* Implicit oracles (no crash, no leaked handle, no hang) cover use-after-close and resource life almost for free, *if* the harness can observe handle counts and timeouts. Implicit oracles cannot judge *which* error or *which* bytes, so the spec must supply those.
- *Inference:* Differential oracles between backends are "derived" oracles. They are cheap but inherit the shared misunderstanding of all backends, and they mis-fire wherever the spec is deliberately nondeterministic. An executable model returning *sets* of allowed outcomes is the specified-oracle fix.
- *Inference:* The spec form that maximises specified-oracle coverage for this API is a combination of three parts: (1) a structured table of operations × errors × capabilities (machine-checked for completeness), (2) an executable model that returns allowed-outcome sets including an explicit "indeterminate" outcome, and (3) a stated consistency level for concurrent observers. This is an inference from Q1–Q5, not a finding from any single source.

### Gaps
- No empirical study was found that measures oracle strength for different specification forms on the same API.
