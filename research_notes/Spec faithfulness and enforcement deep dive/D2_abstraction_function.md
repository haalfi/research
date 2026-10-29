# D2. The abstraction function between reference model and spec (plus disconfirming search §4(b))

Scope: how abstraction functions and refinement mappings (`alpha`: reference-model state → spec state) are written, reviewed and validated in practice; how they fail and how they are checked; how they stay stable as a spec grows; and evidence against the claim that a reviewed `alpha` reduces bridge defects. The setting is an executable Python reference model R checked against a normative spec S and formal models F.

**Tag legend, used on every finding:** [grade; FT = full text read yes/no; n and setting; "correct" = what correct meant in the source; transfer = *direct* / *analogous* / *inference*; agents = what was measured about agents or LLMs, or "human-only evidence"; indep = source-independence flag].

**Baseline under examination.** Verified report §2.3.2, verbatim: "A reviewed, versioned abstraction function `alpha(R_state) → spec_state` is the cheapest structural decision, and the place agents are likely to cut corners". Earlier notes T3a, verbatim: "Making `alpha` a reviewed, versioned artefact is the single cheapest structural decision." The verified report's bridge table, verbatim: "| **Refinement checks** | No full-text bridge evidence | — | — | — |". Its open-points list, verbatim: "13. No refinement-check bridge has been measured; no Alloy/Lean ↔ Python bridge evidence was found."

**Sources read in full for this track (venues checked through Crossref or the PDF header):**
- ShardStore, SOSP 2021
- IronFleet, SOSP 2015
- Verdi, PLDI 2015 (TCB passage only)
- Armada, PLDI 2020 (refinement-relation passages)
- seL4 TOCS 2014 (state relation and bugs-found sections)
- Fonseca et al., EuroSys 2017
- IronSpec, OSDI 2024
- Cirstea et al., SEFM 2024
- CCF, NSDI 2025
- SysMoBench, ICLR 2026
- Cedar, FSE Companion 2024
- VeriStruct, TACAS 2026
- Abadi & Lamport, "The Existence of Refinement Mappings" (DEC SRC report version of TCS 1991)
- Lamport & Merz, "Prophecy Made Simple", TOPLAS 2022
- Hughes, "Experiences with QuickCheck", LNCS 9600, 2016
- documentation for Hypothesis stateful testing, proptest-state-machine, quickcheck-state-machine and Knossos

---

## Q1. Practice: how are abstraction functions and refinement mappings written, reviewed and validated?

### Takeaway
Two patterns recur in practice, and neither treats `alpha` as an artefact that is trusted because it was reviewed:
- **Proof-based systems** (IronFleet, seL4, Armada, Verdi) make `alpha` *untrusted*: the proof checks it. They put the trust into a small, human-reviewed relation over *externally visible* state (IronFleet's `SpecRelation`, Armada's refinement relation R).
- **Test-based systems** (ShardStore, Cedar, CCF, Cirstea, QuickCheck and Hypothesis) compare outputs after every operation, plus a narrow projection of state such as "same key-value mapping". There `alpha` is ad-hoc harness code that is checked only indirectly, by the discrepancies it produces. Two of these sources (CCF, Hughes) report that a large share of discrepancies are in the model or the mapping, not in the implementation.

### Cited Findings

**Proof-based refinement: `alpha` untrusted, observation relation trusted**
- IronFleet defines a refinement function `PRef` from protocol state to spec state, proves `SpecInit(PRef(init))`, and proves that each protocol step maps to a legal sequence of spec steps. "We could use a relation instead of a function, but the proof is easier with a function." Host-level `HRef` and system-level `IRef` refinement functions are composed into `PRef(IRef(·))`. [A; FT yes; n = 2 systems (IronRSL, IronKV), ~3.7 person-years in total; correct = machine-checked refinement; transfer = *analogous*; agents = human-only evidence; indep = authors on their own method] — [IronFleet SOSP 2015](https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf)
- IronFleet's **trusted** surface is the spec plus the main event loop. The refinement functions are not trusted. `SpecRelation` "describes the required conditions on the relation between an implementation state and its corresponding abstract state … To avoid unnecessary constraints on implementations of the spec, SpecRelation should only talk about the externally visible behavior of the implementation, e.g., the set of messages it has sent so far." Trusted spec size: IronRSL 85 SLOC, IronKV 34 SLOC, "making them easy to inspect for correctness". [same tags] — [IronFleet](https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf)
- IronFleet built a generic refinement library for concrete-to-abstract data structures. Given "basic properties about the relationship between the concrete types and the abstract types, e.g., that the function mapping concrete map keys to abstract maps keys is injective", it proves that concrete map operations refine the abstract ones. *(This per-type projection library is evidence for modular `alpha`; see Q4.)* [same tags] — [IronFleet §5.3](https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf)
- Armada: "The developer defines what this means via a refinement relation (R). For instance, if the state contains a console log, the refinement relation might be that the log in the implementation is a prefix of that in the spec." Here R is a *relation* over observable state, not a function. [A; FT yes (sections 2–3.1.3 and the TCB passage); setting = concurrent programs in Dafny; correct = machine-checked refinement; transfer = *analogous*; agents = human-only evidence; indep = own tool] — [Armada PLDI 2020](https://www.andrew.cmu.edu/user/bparno/papers/armada.pdf)
- Verdi's TCB, verbatim: "the specifications of verified applications, the assumption that Verdi's network semantics match the physical network, the Verdi shim, Coq's proof checker and OCaml code extractor, and the OCaml compiler and runtime". No abstraction function appears in it. [A; FT yes (TCB passage); transfer = *analogous*; agents = human-only evidence; indep = own system] — [Verdi PLDI 2015](https://homes.cs.washington.edu/~ztatlock/pubs/verdi-wilcox-pldi15.pdf)
- seL4 proves forward simulation through a "state relation" at each refinement level. The authors "aimed to move effort from the correspondence proofs to the invariant proofs", and "the overall proof effort was clearly dominated by invariant proofs, with the actual refinement statements" taking a smaller share. Effort was ~20 py for the proof versus 2.2 py for kernel development. [A; FT yes (relevant sections); n = 1 kernel; correct = machine-checked functional correctness; transfer = *analogous*; agents = human-only evidence; indep = own system] — [Klein et al. TOCS 2014](https://trustworthy.systems/publications/nicta_full_text/7371.pdf)

**Test-based conformance: output equality plus a narrow state projection**
- ShardStore states its durability property as "the model and implementation remain in equivalent states after each API call. Since the system is a key-value store, we define equivalence as having the same key-value mapping." That is an abstraction onto one observable projection. The property-based test "applies the operation to both reference model and implementation, compares the output of each for equivalence, and then checks invariants that relate the two systems." [A; FT yes; n = 1 production system (>40k LOC Rust), 16 issues prevented; correct = refinement of the reference model ("any observable behavior of the implementation must be allowed by the model"); transfer = *analogous*, the closest to a stateful store API; agents = human-only evidence; indep = Amazon authors on their own system] — [ShardStore SOSP 2021](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)
- ShardStore's reference models are per component, "1% of the implementation code", and written in Rust in the same code base. The authors chose this over Alloy, Promela or P partly to "minimize the cognitive burden of learning a new language and mapping concepts between model and implementation". The model is reused as a unit-test mock, "effectively requiring engineers to update the reference model specifications themselves when developing new code". [same tags] — [ShardStore §3.2](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)
- ShardStore puts background operations (reclamation, clean reboot) into the operation alphabet as **no-ops in the model**: "including them validates that their implementations do not corrupt the index." [same tags] — [ShardStore §4.1](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)
- Cedar's DRT sends the same generated inputs to the Lean model and to Rust and compares outputs. "If the two versions agree on the output, then we obtain a piece of evidence that Rust production code is on par with the Lean model." The comparison is on outputs (authorization decisions, validation results), not on internal state. Three of the 21 DRT/PBT bugs were naming disagreements between Rust and the model ("named extension functions differently (e.g., lt vs. lessThan)"; "ipaddr vs. IPAddr"). [A; FT yes; n = 1 system, 21 bugs; correct = output parity; transfer = *analogous*; agents = human-only evidence; indep = AWS authors on their own system] — [Cedar FSE Companion 2024](https://arxiv.org/abs/2407.01688)
- Cirstea et al.: trace validation checks that the trace's behaviours intersect the spec's behaviours (S ∩ T ≠ ∅), "with arbitrary values assigned to variables whose values are not recorded". It explicitly does not check T ⊆ S, because "this condition would be too strong in the presence of non-deterministically chosen values for variables not recorded in the trace." "In general, the programmer is in charge of tracking the correspondence between the event names in the trace and the actions in the specification as well as the correspondence between the names of the logged variables and those from the specification." [A; FT yes; n = 2 examples (2PC, KV) plus case studies; correct = trace compatibility; transfer = *analogous*; agents = human-only evidence; indep = TLC maintainers on their own tooling] — [Cirstea et al. SEFM 2024](https://arxiv.org/abs/2404.16075)
- CCF built its mapping (the `Trace` spec, ~400 LoC) "by mapping the trace of a straightforward happy-path test line by line to the consensus spec. To proactively catch discrepancies, we added as many assertions as possible to Trace." "Adding cross-references between the implementation and the spec proved useful, particularly when the terminology … differed between the two." [A; FT yes; n = 1 system; correct = trace validated by TLC; transfer = *analogous*; agents = human-only evidence; indep = Microsoft and TLC-maintainer authors on their own system] — [CCF NSDI 2025](https://arxiv.org/abs/2406.17455)

**Lamport-style refinement mappings**
- A refinement mapping maps lower-level states to higher-level states. Abadi & Lamport show that one exists, provided auxiliary (history or prophecy) variables are added, under stated assumptions. [A; FT yes (DEC SRC report version of the TCS 1991 paper); theory; transfer = *analogous*; agents = n/a; indep = n/a] — [Abadi & Lamport](https://lamport.azurewebsites.net/pubs/abadi-existence.pdf)
- A refinement mapping has to hold only on reachable states, so it needs an invariant of the implementation. Lamport & Merz build a plausible mapping and write: "Many readers will also be able to convince themselves that (9) is valid. Those readers are wrong." The step check fails for the unreachable state `seq = ⟨rdy⟩` unless an invariant excludes it. [A; FT yes; worked example; transfer = *analogous*; agents = n/a] — [Lamport & Merz TOPLAS 2022](https://lamport.azurewebsites.net/pubs/simple.pdf)

**Python and other PBT libraries: no first-class `alpha`**
- Hypothesis `RuleBasedStateMachine` keeps the model as ordinary instance state, for example `self.model = defaultdict(set)`. The comparison is whatever the user asserts: in the documented example, an `@invariant`/rule checks `set(self.database.fetch(k)) == self.model[k]` per key. [B; FT yes (docs page); transfer = *direct* (the Python tool); agents = none measured; indep = vendor docs] — [Hypothesis stateful docs](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- proptest-state-machine has a `ReferenceStateMachine` with `type State`. The SUT's `apply` receives `ref_state` "for comparison". The comparison is user-written assertions in `apply` or invariants. [B; FT yes (book page); transfer = *analogous*; agents = none; indep = docs] — [proptest book](https://raw.githubusercontent.com/proptest-rs/proptest/main/book/src/proptest/state-machine.md)
- quickcheck-state-machine: the model plus a `transition` and postconditions on responses. The model holds opaque references to real resources (`Reference (Opaque (IORef Int))`). [B; FT yes (README); transfer = *analogous*; agents = none; indep = docs] — [qsm README](https://raw.githubusercontent.com/stevana/quickcheck-state-machine/master/README.md)
- Knossos checks a client-observed *history* against a single-threaded model (register, CAS register, mutex). No internal-state mapping is involved. [B; FT yes (README); transfer = *analogous*; agents = none; indep = docs] — [Knossos README](https://raw.githubusercontent.com/jepsen-io/knossos/master/README.md)
- Hughes (Quviq) describes eqc_statem the same way: model state, transition functions and postconditions comparing actual results with the model. The dets model was "less than 100 lines of code", against an implementation of "over 6,000 lines". [B (experience essay; the author says "This is not a typical scientific paper"); FT yes; transfer = *analogous*; agents = human-only evidence; indep = tool author and vendor] — [Hughes 2016](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quviq-testing.pdf)

### Inferences
- *Inference*: the brief's `alpha` merges two roles that practice keeps apart:
  1. a projection that is allowed to be wrong because something checks it (proof, or discrepancy detection);
  2. a small *trusted* statement of what is externally observable (IronFleet's `SpecRelation`, Armada's R, ShardStore's "same key-value mapping", Cedar's output parity).
- In a pipeline with no proof (Python R checked by tests and trace validation), role 1 has no checker except the tests themselves. The mapping therefore sits in the TCB, which is the main transfer caveat.
- *Inference*: in the five test-based sources (ShardStore, Cedar, Hypothesis, proptest, Knossos), comparison is output-first, with state projection kept narrow. None maps the full internal state.

### Gaps
- No source describes a formal *review procedure* for an abstraction function (checklist, second reviewer, sign-off). "Reviewed" in the baseline has no direct practice evidence. Only IronFleet's statement that the trusted spec is small enough "to inspect" comes close, and it concerns the spec, not the refinement function.
- Cedar's FSE paper does not describe how Rust values are converted to Lean values in the DRT harness. That conversion layer is itself a mapping, and its review is undocumented in the text read.

---

## Q2. Failure modes of the abstraction function, and checks for them

### Takeaway
Seven failure modes have full-text support:
1. mapping bugs reported as a distinct cause of bridge failure, with no counterexample to guide diagnosis (CCF);
2. partial or imprecise projections that accept wrong behaviour (Cirstea; IronSpec's subset-of-fields specs);
3. a "plausible" mapping that is valid only under an unstated invariant (Lamport & Merz);
4. a mapping that cannot be a function (Abadi & Lamport);
5. operations or observables left out of the model (Hughes);
6. relaxations that can mask bugs (ShardStore has-failed; MongoDB);
7. LLM-written mappings that are trivial (VeriStruct) or checked only at the name level (SysMoBench).

For each mode the sources also give concrete checks. No source counts how often `alpha` itself was wrong.

### Cited Findings

**(a) Mapping bugs are a named failure cause, and diagnosing them is the expensive part**
- CCF, verbatim: "Bogus logging, incorrect mappings from implementation to spec state, or true discrepancies between the spec and the implementation, resulted in T ∩ S = ∅ … In either case, contrary to ordinary model checking, a failure to validate a trace had no counterexample." Effort: "approximately two engineer-months, spread over four months", where a "major task was diagnosing if the root cause of discrepancies arose from bugs in the reverse-engineered spec, the implementation, or both". "Writing the 400 LoC Trace spec itself was a minor task." Churn: "88 fine-grained commits to the Trace spec, while the consensus spec underwent 107 changes." [A; FT yes; n = 1 system; correct = TLC trace acceptance; transfer = *analogous*; agents = human-only evidence; indep = own system] — [CCF NSDI 2025 §6.3, §6.5](https://arxiv.org/abs/2406.17455)
- **Check (CCF):** an "unsatisfied breakpoint" in TLC "triggers for each state in T that is found to be unreachable", to "determine if Trace is overly restrictive". The trace behaviours are visualised with the subformula responsible for each unreachable state. [same tags] — [CCF §6.3](https://arxiv.org/abs/2406.17455)

**(b) Partial projections accept wrong behaviour (hidden or unconstrained state)**
- Cirstea et al.: "too imprecise logs may even lead to erroneous traces being accepted because the model checker may be able to infer suitable values that do not correspond to the actual ones." [A; FT yes; tags as Q1] — [Cirstea SEFM 2024 §4.4](https://arxiv.org/abs/2404.16075)
- IronSpec (Dafny specs of 6 open-source verified systems): the Automatic Sanity Checker led to 5 spec bugs. In 4 of the 5 (TS2, ETH1, AES1, AES2), "the bug was a result of the output consisting of a complex datatype with many sub-fields and having postconditions concerning only a subset of these fields. This combination allows for a different implementation to update the remaining unspecified fields arbitrarily." All 10 bugs were confirmed by the systems' authors, and all were specs that were "too weak". [A; FT yes; n = 14 specs (6 in-house, 2 from Abreu et al., 6 open-source), 10 real spec bugs; correct = author-confirmed weakness, shown by a buggy implementation that still verifies (Counterexample STP); transfer = *analogous* (a subset-of-fields postcondition is the contract-level analogue of state outside `alpha`); agents = human-only evidence; indep = tool authors evaluating their own tool] — [IronSpec OSDI 2024 §5.1](https://www.usenix.org/system/files/osdi24-goldweber.pdf)
- IronSpec, ghost state: one alive mutant in daisy-nfsd "hinted towards underconstrained ghost state". The authors judged it a false positive (no safety impact) but "acknowledged that this weakness was not immediately apparent". [same tags] — [IronSpec §5.3](https://www.usenix.org/system/files/osdi24-goldweber.pdf)
- Fonseca et al., Bug I1: IronFleet's high-level spec did not require exactly-once semantics, although the implementation de-duplicated. A 7-line patch that disabled de-duplication "still verified". The developers said they had been aware of it and added a comment. In effect, implementation state (the dedup table) had no counterpart the spec constrained. [A; FT yes; n = 3 verified systems, 16 bugs; correct = bug judged by the study authors, reported to and confirmed by developers; transfer = *analogous*; agents = human-only evidence; indep = **independent third-party study**] — [Fonseca et al. EuroSys 2017 §5](https://homes.cs.washington.edu/~pfonseca/papers/eurosys2017-dsbugs.pdf)
- **Checks for (b):**
  - *Negative testing.* Fonseca et al. mutate the implementation (flip sub-conditions, suppress structure updates, comment out statements) to see whether the spec still accepts it. Patches equivalent to I1 were found after 377, 18 and 8,015 iterations on average for three functions. [same Fonseca tags] — [Fonseca §5.2](https://homes.cs.washington.edu/~pfonseca/papers/eurosys2017-dsbugs.pdf)
  - *Spec mutation and Spec-Testing Proofs.* IronSpec mutates specs and writes STPs. The daisy-nfsd bug took "approximately 1-2 hours" end to end. [IronSpec tags] — [IronSpec §5.4](https://www.usenix.org/system/files/osdi24-goldweber.pdf)
  - *ShardStore.* Background operations are modelled as no-ops so that corruption of state outside the API is caught. [ShardStore tags] — [ShardStore §4.1](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)

**(c) A mapping that is valid only under an invariant**
- Lamport & Merz's example in Q1: the mapping looks correct but fails on unreachable states unless an invariant restricts the domain. [A; FT yes] — [Lamport & Merz](https://lamport.azurewebsites.net/pubs/simple.pdf)
- seL4 likewise pairs every correspondence proof with invariant proofs, which dominated effort. [A; FT yes] — [Klein et al. TOCS 2014](https://trustworthy.systems/publications/nicta_full_text/7371.pdf)

**(d) Non-functional abstraction: when `alpha` cannot be a function**
- Abadi & Lamport give three reasons a refinement mapping may not exist:
  1. the higher-level spec holds "historical information" the implementation lacks;
  2. it "specif[ies] that a nondeterministic choice is made before it has to be";
  3. it "run[s] slower".

  The remedies are history variables, prophecy variables and stuttering. [A; FT yes] — [Abadi & Lamport](https://lamport.azurewebsites.net/pubs/abadi-existence.pdf)
- In practice, IronFleet chose a function "because the proof is easier". Armada uses a relation. Cirstea and CCF avoid the issue by checking existentially (S ∩ T ≠ ∅) over unlogged variables. ShardStore avoided tracking all possible model states after failures because "this blows up quickly". [A; FT yes] — [IronFleet](https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf); [Armada](https://www.andrew.cmu.edu/user/bparno/papers/armada.pdf); [Cirstea](https://arxiv.org/abs/2404.16075); [ShardStore §4.4](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)

**(e) Missing operations or observables, and errors in the model rather than the code**
- Hughes: operation-distribution statistics "reveal that we have not tested the size function at all! There is a simple reason for this—for simplicity, we omitted it from the model." Adding it exposed a real bug at once. His general lessons, verbatim: "Errors are often in the model, rather than the code. Calling something a specification does not make it right!" For dets, sequential tests ran first to remove model bugs: "any inconsistencies indicate a misunderstanding of the intended behaviour, i.e. a bug in the model". [B; FT yes; anecdotal; correct = developer judgement; transfer = *analogous*; agents = human-only evidence; indep = tool author and vendor] — [Hughes 2016](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quviq-testing.pdf)
- **Coverage check of the model against tests:** asked "does your model cover this test case?", Quviq built tools for it. When AUTOSAR released six official CAN-bus test cases, "three of these test cases were not covered by the model, because they were not consistent with the standard". [B; FT yes (Hughes's account); n = 6 test cases; transfer = *analogous*] — [Hughes 2016](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quviq-testing.pdf). The underlying paper, Gerdes, Hughes, Smallbone & Wang, Erlang Workshop 2015, checks "whether a given unit test could be produced by a QuickCheck property". [A-workshop; **FT no** (author manuscript link 404; search abstract only) — lead only] — [Bristol record](https://research-information.bris.ac.uk/en/publications/linking-unit-tests-and-properties/)

**(f) Relaxations that can mask bugs**
- ShardStore's "has failed" flag relaxes equivalence after an injected failure. A `Get` may return no data but never wrong data. Mitigation: "we separately run our property-based tests with and without failure injection enabled." [A; FT yes] — [ShardStore §4.4](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)
- MongoDB MBTC (baseline, already graded): "Bugs in post-processing could mask implementation bugs". Not re-read here.
- ShardStore's one known miss came from coverage, not from the mapping: a cache-miss path was never reached because tests configured a very large cache. [A; FT yes] — [ShardStore §8.3](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)

**(g) Agent-written mappings**
- SysMoBench uses an LLM (e.g., Claude-Sonnet-4) to "extract constants, variables, and actions from the input model and … map them to the corresponding elements" in the system logs. Authors' justification: "the mapping task is simple and well-defined". Validation: "We inspected the LLM-assisted mapping and concretization, and found the results to be correct". A robustness test used 10 variants of gold models for Etcd Raft and the Asterinas spinlock (5 each), "changing the names of the variables and actions and tweaking the model's granularity". All gold variants scored perfectly. [A (ICLR 2026); FT yes; n = 10 gold variants plus inspection, no error rate; correct = gold models score 100 % after mapping; transfer = *analogous* (name and action mapping for trace validation, **not** state abstraction); agents = **LLM measured**, positive but on a narrow task; indep = benchmark authors validating their own harness] — [SysMoBench §3.2.3, §4](https://arxiv.org/abs/2509.23130)
- VeriStruct (Verus data-structure modules): "LLMs sometimes produce a trivial Cartesian-product view, which includes all of the data fields … This view function, while syntactically valid, fails to abstract away the circular structure of the ring buffer." The fix is an extra "view refinement" prompt that emphasises "abstraction, minimality, and logical coherence over completeness". A provided unit-test suite "helps rule out trivial or vacuous specifications". Results: 10/11 modules and 128/129 functions verified with o1. A Claude Code (Sonnet 4.5) agentic baseline verified 102 functions across 8 benchmarks; a single-prompt baseline verified 52. In one case (Bitmap) the LLM chose a *different but simpler* abstraction than the human ground truth. [A (TACAS 2026, Crossref DOI 10.1007/978-3-032-22749-2_6); FT yes; n = 11 modules; correct = Verus verifies the module and the unit-test assertions; transfer = *analogous* (Verus `View` = `alpha`); agents = **LLM measured**; the frequency of trivial views is not quantified ("sometimes"); indep = tool authors on their own tool] — [VeriStruct](https://arxiv.org/abs/2510.25015)
- AutoVerus was read to check relevance. Its "refinement" means iterative improvement of loop-invariant proofs, not abstraction functions, so it is **not evidence** for this question. [A-pre/arXiv; FT partially; transfer = none] — [AutoVerus](https://arxiv.org/abs/2409.13082)

### Inferences
- *Inference*: for a Python R the failure modes map as follows.
  - (b) partial projection → frame and hidden-state mutants survive.
  - (c) invariant-dependence → `alpha` raises or returns nonsense on states R never reaches, which is harmless, but a wrong invariant hides real states.
  - (d) non-functional → the spec's outcome sets or late nondeterminism cannot be produced as a function of a deterministic R's state. Compare via a relation or membership ("spec allows this observation") rather than equality.
  - (e) missing operations → spec actions with no R method or `alpha` field.
  - (g) an agent-written identity `alpha` → passes trivially but pushes complexity into every spec clause.
- *Inference, candidate checks for `alpha`* (each borrowed from a source above; none measured as a check on `alpha` itself):
  1. per-action coverage statistics (Hughes; SysMoBench action coverage);
  2. a reachability or unsatisfied-state report on the spec side (CCF);
  3. R-mutants that change one field outside the spec projection, which must be caught by some test (Fonseca negative testing, ShardStore no-op background ops);
  4. spec-side mutants or STPs for subset-of-fields postconditions (IronSpec);
  5. assert R's invariant before applying `alpha` (Lamport & Merz);
  6. run every relaxed check also unrelaxed (ShardStore).

### Gaps
- **No source gives a count or rate of abstraction-function bugs.** CCF names "incorrect mappings" as a cause but does not split its discrepancies by cause. Hughes says "often" with no numbers. MongoDB says post-processing bugs "could" mask.
- No study measured LLM-written *state* abstraction functions against a ground truth with an error rate. SysMoBench covers name mapping only; VeriStruct reports a qualitative tendency.
- Surjectivity (every spec state reached through `alpha`) is not measured as such in any source. The closest are CCF's state coverage table (not re-read in detail here), SysMoBench's code-action coverage, and ShardStore's code coverage of the implementation.
- Observational equivalence (`alpha` preserves outputs) is never checked separately. In ShardStore and Cedar, output comparison and state comparison run side by side, so it is implicit.

---

## Q3. Evidence of bugs in abstraction functions themselves, and the disconfirming search §4(b)

### Takeaway
- **Verified systems:** the only independent study (Fonseca et al.) found 16 bugs: 11 in the unverified shim layer, 3 in verification tooling and 2 in specifications (Figure 3 table). **None** is in a refinement or abstraction function. IronSpec's 10 spec bugs are all specs that are too weak or environments that are too restrictive, not mapping errors. seL4 reports no state-relation bugs as a category.
- **Test-based bridges:** mapping errors are named (CCF, MongoDB, Hughes), but none is counted.
- **For §4(b):** no source shows that reviewing `alpha` reduces bridge defects, and none shows that it does not. The independent evidence says defects concentrate at the *trusted interface*: shim, environment model, too-weak spec, logging and instrumentation. This partly disconfirms the baseline's emphasis. `alpha` is one interface artefact among several, and in proof settings not the one where defects were found.

### Cited Findings
- Fonseca et al. abstract: "we found a total of 16 bugs … These bugs were caused by violations of a wide-range of assumptions on which the verified components relied. Our results revealed that these assumptions referred to a small fraction of the trusted computing base, mostly at the interface of verified and unverified components." Figure 3 lists 2 specification bugs (I1, C4), 3 verification-tool bugs (I2–I4) and 11 shim-layer bugs. (The §6 text says "four bugs we found in verification tools"; the table lists three. This discrepancy is unresolved in the text read.) "Finding 5: No protocol bugs were found in the verified systems … we found no shim layer bugs in IronFleet, which is the system studied with fewest unverified components." [A; FT yes; n = 3 systems (IronFleet, Verdi, Chapar); correct = crash, incorrect result or voided guarantee; transfer = *analogous*; agents = human-only evidence; indep = **independent**] — [Fonseca et al. EuroSys 2017](https://homes.cs.washington.edu/~pfonseca/papers/eurosys2017-dsbugs.pdf)
- Fonseca's recommendation on spec tests: "Ideally, such tests should be built by developers that did not write the specification—adding a level of redundancy". Their PK toolkit automated detection of 13 of the 16 bugs. [same tags] — [Fonseca §5.2](https://homes.cs.washington.edu/~pfonseca/papers/eurosys2017-dsbugs.pdf)
- IronSpec: 10 author-confirmed spec bugs across 6 verified systems. Three were in QBFT, where the adversary model was "unnecessarily restricted", i.e. the trusted environment. For both QBFT and DVT, "the alive mutations identified were part of the trusted specified environment, whereas no alive mutations were found for their respective safety properties". [A; FT yes; tags as Q2] — [IronSpec §5.3](https://www.usenix.org/system/files/osdi24-goldweber.pdf)
- seL4: the first refinement led to "some 300 changes in the abstract specification and 200 in the executable specification. About 50% of these changes relate to bugs in the associated algorithms or design". The second refinement uncovered 144 defects, "mainly typos, misreading the specification, or failing to update all relevant code parts on specification changes". The state relation is not named as a bug site. [A; FT yes (section 7.3)] — [Klein et al. TOCS 2014](https://trustworthy.systems/publications/nicta_full_text/7371.pdf)
- TraceLink (baseline, verified report): 9 bugs, "all model↔implementation drift or environment assumptions". Not re-read here.
- CCF: mapping errors are one of three named causes of T ∩ S = ∅, uncounted (Q2a). Hughes: "Errors are often in the model, rather than the code" (Q2e). [tags as above]

### Inferences
- *Inference*: in proof-based systems a wrong refinement function cannot produce a *false pass*. It only blocks the proof. False passes come from the trusted parts: spec too weak, environment too narrow, shim. That explains why Fonseca and IronSpec found no `alpha` bugs. It does **not** carry over to a Python R checked by tests, where a wrong `alpha` can produce false passes silently, as an omitted field or an over-relaxed comparison.
- *Inference, §4(b) verdict*:
  - There is **no direct evidence either way** that a *reviewed* `alpha` reduces bridge defects.
  - **Weak disconfirmation:** independent evidence puts defects at the trusted interface generally: shim, environment, spec weakness, logging. Practice then makes the *observable relation* small and trusted, and keeps `alpha` untrusted but checked.
  - A pipeline that concentrates review effort on `alpha` while leaving the fault and environment model, logging and spec strength unreviewed would contradict the Fonseca and IronSpec distribution.

### Gaps
- No study compares bridge defect rates with and without a reviewed `alpha`. This is the central gap for §4(b).
- Coverage of agents: no study of agents writing `alpha` for test-based conformance measured false-pass rates.
- Only one independent source (Fonseca) carries the "defects concentrate at the interface" claim for verified systems. IronSpec is tool authors evaluating their own tool. **Single-independent-source sub-question.**

---

## Q4. Keeping `alpha` stable as the spec grows

### Takeaway
The supported stability mechanisms are:
- per-component models and projections, composed (ShardStore; IronFleet's composed `PRef(IRef(·))` and generic per-type refinement library);
- co-location in the implementation language, plus reuse as mocks, so that a change breaks the build (ShardStore);
- decomposition into separate, weaker equivalences for crash and concurrency (ShardStore);
- separating a small trusted observation relation from the untrusted mapping (IronFleet).

Versioning `alpha` and round-trip or concretization (`gamma`) tests of `alpha` have **no** full-text practice evidence in the sources read.

### Cited Findings
- ShardStore decomposes durability into:
  1. sequential crash-free (direct equivalence);
  2. sequential crashing (the model is "extend[ed] … to define which data can be lost after a crash, and check a corresponding weaker equivalence");
  3. concurrent crash-free (separate models, linearizability).

  "This decomposition aids the specification effort … the initial reference models are simple and easy to audit, and then we extend them separately." [A; FT yes] — [ShardStore §3.1](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)
- ShardStore on staying current: "Developers must update the models whenever code changes in order to avoid breaking the build." After the experts' first iteration, models "have been updated almost exclusively by the engineering team". 18 % of harness lines were last edited by non-experts (git blame). Effort: two experts for nine months plus a third for three. Models and harnesses are 13 % of the code base. The authors rejected a single public-interface model: "we think it would have been the wrong decision and would have caught fewer bugs." [A; FT yes] — [ShardStore §8.2, §8.4](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf)
- IronFleet composes two refinement theorems into one mapping. Its generic library proves map and sequence operations refine their abstract counterparts given an injective key mapping. [A; FT yes] — [IronFleet §3.5, §5.3](https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf)
- CCF: the mapping (`Trace`) changed in 88 commits while the spec changed 107 times. A later consistency spec, "written with the implementation in mind", needed "significantly less effort" and observed state through the REST API with "no instrumentation". [A; FT yes] — [CCF §6.5](https://arxiv.org/abs/2406.17455)
- CCF on impedance mismatches handled in the mapping layer rather than in the spec: action composition (UpdateTerm + HandleAppendEntriesReq), finite stuttering for multi-event actions, `IsFault` for unlogged message loss, and multiset redefinition of the network. [A; FT yes] — [CCF §6.2](https://arxiv.org/abs/2406.17455)
- VeriStruct's guidance for LLM views, "abstraction, minimality, and logical coherence over completeness", plus a unit-test suite as the anti-vacuity check. [A; FT yes] — [VeriStruct §4](https://arxiv.org/abs/2510.25015)

### Inferences
- *Inference*: for a Python R the analogue of ShardStore's mock reuse is to make `alpha` the code that the expectation-test fixtures or spec-conformance checks call. Any R refactor that breaks `alpha` then fails CI at once.
- *Inference*: per-operation projections (each spec clause reads only the `alpha` fields it names) keep `alpha` additive as clauses grow. IronFleet's per-type library and ShardStore's per-component models are the closest precedents. No source measures this property directly.

#### Recommendations (D2)

| # | Recommendation | Confidence | Load-bearing sources | Finding that would overturn it |
|---|---|---|---|---|
| D2-R1 | Split `alpha` into (i) a small **trusted observation relation** (what S says is externally visible: return values, errors, a declared store projection), which is human-reviewed and versioned with the spec's clause IDs, and (ii) an **untrusted projection** from R's internals, which is checked rather than trusted | medium | IronFleet `SpecRelation` (A); Armada R (A); ShardStore "same key-value mapping" (A) | A test-based study where defects concentrate in the trusted observation relation itself rather than in the projection or the environment |
| D2-R2 | Treat agent-written `alpha` as *code under test*: (a) per-action coverage statistics; (b) R-mutants that alter one non-projected field must be caught; (c) an anti-identity check, flagging an `alpha` that copies R's fields one to one (VeriStruct's trivial view) | medium-low | Hughes (B); Fonseca negative testing (A); VeriStruct (A); SysMoBench (A) | A measured agent study showing that agent-written state projections have false-pass rates no higher than human ones without these checks |
| D2-R3 | Compare by **membership in the spec's allowed outcomes** (relation or existential), not equality, wherever S leaves choices open; never use equality on a forced function | high (theory) / medium (practice) | Abadi & Lamport (A); Cirstea S ∩ T (A); ShardStore has-failed (A) | None plausible on theory; in practice, evidence that membership checks hide more bugs than they prevent (Cirstea's imprecise-log warning is the risk) |
| D2-R4 | Run every relaxed comparison also unrelaxed, and log R's full state (R is deterministic and observable), to avoid Cirstea-style false acceptance | high | ShardStore (A); Cirstea (A); CCF (A) | Full-state logging making validation infeasible for a Python R (Cirstea Fig. 5 shows state blow-up only with *imprecise* logs) |
| D2-R5 | Do **not** make "reviewed `alpha`" the single structural priority. Give equal weight to the environment and fault model, logging and instrumentation, and spec strength (subset-of-fields postconditions) | medium | Fonseca (A, independent); IronSpec (A); TraceLink (baseline) | A test-based bridge study where `alpha` errors are the majority of false passes |
| D2-R6 | Assert R's invariant before calling `alpha`, so that `alpha` is defined only on reachable states | medium | Lamport & Merz (A); seL4 invariant dominance (A) | None found |

**Proposed qualification of the baseline.** Verbatim: "A reviewed, versioned abstraction function `alpha(R_state) → spec_state` is the cheapest structural decision, and the place agents are likely to cut corners". New full-text evidence supports *cheapness of writing* (CCF: the 400-LoC Trace spec "was a minor task"; ShardStore: models 1 % of the code). It does not support *cheapness of getting right* (CCF: diagnosis dominated two engineer-months). Agents cutting corners on abstractions has one measured instance: VeriStruct's trivial views, unquantified. The "single cheapest" framing is not contradicted, but "reviewed" should become "small trusted part reviewed, rest checked". The verified report's "Refinement checks | No full-text bridge evidence" row stays true for F ↔ Python R, but it can now cite *analogous* refinement practice (IronFleet, Armada, seL4), where the mapping was proof-checked and was not a defect site.

### Gaps
- No versioning practice for `alpha` was found.
- No round-trip or concretization (`gamma`, generator over spec states) test of an abstraction function was found in any source read. *Inference*: a property `alpha(gamma(s)) == s` over generated spec states is cheap in Python. It would check that the projection is surjective onto the clause-relevant fields. It is unvalidated.
- The ShardStore "18 %" adoption figure measures adoption, not the stability of the mapping.

---

## What this track did not do
- Did not re-read MongoDB MBTC, TraceLink, Mocket, Quint Connect or the Konnov slides; their baseline grades are reused as cited in the verified report.
- Did not read the quickcheck-state-machine, Hypothesis or proptest source code. Docs only.
- Did not read eqc_statem docs or Hughes's "QuickCheck testing for fun and profit". Did not obtain the full text of Gerdes et al. 2015 (404).
- Did not read Verdi or Armada end to end, only the passages on refinement and TCB. Did not read seL4's full proof-structure sections.
- Did not find or read Apalache or TLC refinement-checking case studies with effort or defect data. No "refinement mapping checked by TLC" practice paper with numbers was retrieved.
- Did not run an own trial (for example a Hypothesis machine with a deliberately incomplete `alpha` and R-mutants).
- Did not search for LLM-written TLA+ refinement mappings beyond SysMoBench; TLAi+Bench and Specula were not retrieved.

## Self-check
- **Possible misreading of the brief:** "abstraction function" could be read narrowly as state → state only. I included output-comparison practice (Cedar, Knossos) because the brief's question on observational equivalence needs it. A reader wanting only state mappings should discount those rows.
- **Fonseca counts:** I report Figure 3 (2 + 3 + 11 = 16). The §6 text says "four bugs we found in verification tools". I did not resolve this; the headline "16 bugs" is consistent with the table.
- **IronSpec as `alpha` evidence:** subset-of-fields postconditions are contract weakness, not abstraction-function bugs. Using them for "hidden state outside `alpha`" is an *analogy* (labelled), not a direct finding.
- **SysMoBench mapping:** it maps *names* (variables and actions) between model and logs, not state values. I flagged that it does not test state abstraction. The baseline already reports its "found the results to be correct"; the 10-variant robustness test is the new detail.
- **VeriStruct frequency:** "sometimes" is the paper's word. I did not upgrade it to a rate.
- **ShardStore source:** read from the Amazon Science CDN copy, not the ACM version (ACM returned 403). The text matches the SOSP '21 headers.
- **Inference on proof vs test settings:** the claim that a wrong refinement function cannot cause a false pass in proof systems is my reasoning from IronFleet's trust structure. No source states it in those words.
- **Single-source sub-questions:**
  - "defects concentrate at the trusted interface" has one independent source (Fonseca);
  - "mapping errors are a named cause of trace-validation failure" has one source with specifics (CCF);
  - the LLM trivial-abstraction failure has one source (VeriStruct).
