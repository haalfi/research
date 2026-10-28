# Bind every spec category to its check

The best-founded method for specifying observable behaviour at a black-box library boundary is not a single notation. It is **Design by Contract extended into an assume–guarantee contract**, with five parts. The first is an abstract model of observable state with per-call normal and exceptional cases (Meyer, JML, Larch). The second is a typestate for every resource the library hands out. The third is an explicit environment clause that names the observers and every action the outside world may take (Jones's rely–guarantee, Abadi–Lamport's E ⇒ M). The fourth is a set of history predicates for what several observers see (linearizability, session guarantees, client-centric isolation). The fifth is a set of named variation points whose bounded value sets per-reality profiles may only narrow, never widen (Liskov–Wing behavioural subtyping). No published rule maps specification category to level to form. The research team searched for one and found none. Selection frameworks that exist cover elicitation techniques and have "little validation" ([Carrizo et al., WER 2008](https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf), A). The rule offered here is therefore a synthesis: **choose the form by what the claim quantifies over**. Industrial evidence supports it. Executable reference models with property-based and model-based testing found crash and concurrency bugs at AWS ShardStore and Cedar, model checking paid off on concurrency at AWS and Cosmos DB, and tables made case-split completeness mechanically checkable at Darlington and in SCR. The agent evidence is strong on one point and thin everywhere else. Agents conform well to **fixed, machine-checked specs** and measurably weaken or game **editable or ambiguous** ones. No controlled study shows that any written format (EARS, Gherkin, tables, prose) helps agents more than another. The bake-off proposed in § 7 would itself produce that missing evidence.

**Evidence status, stated up front.** Every research agent behind this report was **blocked from fetching full texts in this session**, with the egress proxy or DNS refusing arxiv.org, acm.org, vldb.org, docs.python.org, pubs.opengroup.org and others. Every finding below therefore rests on **search-engine extracts of primary sources** (abstracts, publisher pages, READMEs, official docs), not on reading the papers. Exact figures and quotations were checked only against those extracts. Items the notes tagged as background knowledge or "not verified this session" are marked **(†)** here and must be spot-checked before anyone relies on their wording. Statements marked *Inference* are this report's own reasoning, not findings of any source. Grades follow the brief: A = peer-reviewed or measured, B = documented industrial practice with data (normative standards and official API docs are also graded B: they are authoritative about what they specify, not evidence that a method works), C = practitioner report without data, D = opinion or marketing. "A-pre" marks an arXiv preprint that has not been peer-reviewed.

---

## 1. Kernsatz

Write the boundary as **one assume–guarantee contract in the Design-by-Contract lineage**. It has an abstract model of observable state, per-call normal and exceptional cases, a typestate for each handed-out resource, one environment clause naming the observers and everything the outside world may do, and history predicates for what several observers see. Its variation points carry bounded value sets that per-reality profiles may only narrow. **Choose each spec's form by what its claim quantifies over**, and work every clause out the way the axioms were: a decision, a counterexample trace, witness implementations, a named check and non-goals. The quantifier-to-form mapping is: a finite case split → table; a value domain → executable oracle with property tests; call sequences on one resource → state-transition table with stateful model-based tests; interleavings of observers and environment → history predicate with a history checker or model checker. **Make every check executable, independent of the implementation and frozen against the implementer.** That is the one point on which measured agent evidence is clear. Evidence on which written format agents prefer is thin.

---

## 2. Categories, levels and forms: eight categories, four binding axes, one quantifier rule

### 2.1 The categories and their levels

No established taxonomy matches the categories the brief proposes. The literature draws its lines along two axes:

- **What is described**: the environment, the interface, or the design. These are the Parnas–Madey monitored/controlled variables with REQ/NAT/IN/OUT ([McMaster record](https://experts.mcmaster.ca/scholarly-works/2169098), A) and Zave–Jackson's insistence that requirements describe the environment ([Zave FRE page](https://pamelazave.com/fre.html), A).
- **State and time**: a static structure, a single two-state transition, or behaviour over traces. This split runs through Larch's two tiers ([Larch FAQ](https://www.cs.ucf.edu/~leavens/larch-faq.html), A/B), TLA+ open specifications and Event-B refinement (†).

*Inference:* the categories below are derived from those two axes. They add one thing the literature implies but does not name as a category: the **environment model** as its own unit. Assume–guarantee contracts put the assumption E in one place ([Abadi & Lamport, Composing Specifications](https://www.microsoft.com/en-us/research/publication/composing-specifications/), A). I/O automata treat environment inputs as always enabled ([Lynch retrospective](https://arxiv.org/pdf/2502.20468), A). P closes systems with environment "ghost machines" ([Desai et al., PLDI 2013](https://www.microsoft.com/en-us/research/publication/p-safe-asynchronous-event-driven-programming-2/), A).

*Inference:* error classification and profiles look less like categories of behaviour and more like cross-cutting dimensions; none of the taxonomies above lists either as a category of its own. They are kept as categories here because each needs exactly one home (P2).

A spec's **level** is fixed by how far it is bound on four axes: observers, time, environment and reality. The governing principle (*Inference*, from P1 and Larch's tiering) is that **a spec binds to the least it needs, and binds to reality only through named variation points**.

| Category | What a unit states | Time | Observers | Environment | Reality | Established precedent |
|---|---|---|---|---|---|---|
| **K1 Structure** | What the API addresses (the existing axioms) | one instant | none | none | none | Larch shared tier; ASM/Event-B state space (†) |
| **K2 Value function** | A pure map from input values to output values (e.g. a derived value of a key) | none | none | none | none, or a named variation point | Larch LSL theories; Parnas tables ([Lawford & Wassyng](https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf), A) |
| **K3 Single call** | Pre-state → post-state or signalled error, over an abstract model; frame | two states | O1 | frame only: "nothing else observable changes" | named variation points | JML normal/exceptional behaviour ([JML RM ch. 9](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html), B); Larch interface tier |
| **K4 Resource life** | States of a handed-out object, legal operations per state, transitions on error and close | sequence on one object | O1 | environment actions may interleave between steps (referenced from K5, never restated) | named variation points | Typestate ([Strom & Yemini via DBLP](https://dblp.org/pid/41/5885), A); UML protocol state machines ([OMG UML14-209](https://issues.omg.org/issues/UML14-209), B) |
| **K5 Environment model** | The named observers (O1 caller, O2 concurrent caller, O3 out-of-band store actor) and every action each may take, including fault actions | action alphabet | all, declared | *is* the environment | which fault actions are possible may be a variation point | A/G "E" ([Abadi & Lamport](https://www.microsoft.com/en-us/research/publication/composing-specifications/), A); P ghost machines; Jepsen nemesis ([Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md), C) |
| **K6 Multi-observer guarantee** | Predicates over histories of client-observed events: what O1 may see given what O2/O3 did | history | O1–O3 | full | value taken from a published consistency lattice | Linearizability ([Herlihy & Wing](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf), A); session guarantees ([Terry et al.](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf), A); client-centric isolation ([Crooks et al.](https://par.nsf.gov/biblio/10077635), A) |
| **K7 Error classification** | A closed or extensible set of error categories defined by the caller's recovery action, and which categories each (operation, state) may signal | none | O1 | none | mechanism-to-category mapping lives in the profile | gRPC codes ([gRPC guide](https://grpc.io/docs/guides/status-codes/), B); `signals_only` ([JML RM](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html), B); Rust `ErrorKind` ([docs](https://doc.rust-lang.org/nightly/std/hash/../io/enum.ErrorKind.html), B) |
| **K8 Profile** | One value per variation point, per reality | none | none | none | binds reality completely and states nothing else | POSIX option constants ([unistd.h](https://www.gaertner.de/~neitzel/susv3/basedefs/unistd.h.html), B); W3C variability ([W3C Note](https://www.w3.org/TR/spec-variability/), B); Hadoop contract XML ([testing.html](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/filesystem/testing.html), B) |

**A cross-cutting vocabulary of non-commitment** serves § 3.2 ("unspecified is a statement"). Standards separate four strengths:

- **unspecified**: one of a stated set, undocumented;
- **implementation-defined**, here **profile-declared**: one of a set, and the reality must declare which;
- **undefined**: no requirement at all;
- **optional (MAY)**: an allowed variation, with a duty to interoperate.

Sources: C11 § 3.4 as quoted by [WG23 N0245](https://www.open-std.org/JTC1/SC22/WG23/docs/ISO-IECJTC1-SC22-WG23_N0245-revised-c-langague-annex-2010-03-23.pdf) (B) and [RFC 2119](https://rfc-editor.org/rfc/rfc2119) (B).

Two further values are needed at the boundary:

- **indeterminate**: the operation may or may not have taken effect. This is Jepsen's `:info` ([Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md), C).
- **deliberately not promised**: latency, request count, memory and buffering, which are observable but outside the contract. PEP 3116's "may return a short read without any particular reason" is the cleanest precedent ([PEP 3116](https://peps.python.org/pep-3116/), B).

*Inference:* "undefined" is almost always wrong at a black-box boundary, because no check can be written against it (P4, P5). Python and Java prefer a defined error for use-after-close ([CPython iobase.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/39f6a0489fcc815a578d27dfee2feea003c896f8/Modules/_io/iobase.c), B).

### 2.2 The category × form matrix

Each cell gives the fit (++ strong, + workable, − poor), **what the form makes checkable** for that category, and **its main cost**. The cells are *Inference* from the cited cases unless a source is named. The industrial anchors are:

- ShardStore ([Bornholt et al., SOSP 2021](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf), A): 16 issues prevented, spec and harness about 14% of the codebase.
- Cedar ([Disselkoen et al.](https://arxiv.org/pdf/2407.01688), A): 4 bugs found by proof, 21 by differential and property testing.
- AWS TLA+ ([Newcombe et al.](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf), B): 10 systems, 2–3 weeks to learn.
- AUTOSAR QuickCheck ([Chalmers record](https://research.chalmers.se/en/publication/219899), A/B): more than 3,000 pages modelled, more than 200 issues.
- SCR/Darlington tables ([Heitmeyer & Labaw](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf), A).

| Category ↓ / Form → | Structured prose (IDs, RFC 2119, templates) | Table (case, state-transition, capability) | Schema-validated data | Executable reference model (+ differential) | PBT / stateful model-based tests (+ history checker) | Model-checked formal (TLA+, P, Alloy, Quint) | Proof (Dafny, Lean, Isabelle) |
|---|---|---|---|---|---|---|---|
| K1 Structure | + review only; cheap | − | + shape only, not cross-constraints | + generator of valid structures | + invariants on generated trees | ++ bounded consistency and counterexample search (Alloy-style, †) | + meta-theorems; high cost |
| K2 Value function | + nothing checked | ++ completeness and disjointness of case split (SCR, Darlington); cheap to check, costly to retrofit | − | ++ agreement on millions of inputs (Cedar DRT); cost of a second implementation | ++ general laws, round-trips ([Goldstein et al.](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice), A); generators are hard | + | + if a soundness property matters |
| K3 Single call | + POSIX SYNOPSIS/ERRORS idiom (†); unchecked | ++ precondition × outcome partition, mechanically complete and disjoint | + parameter/result shape | ++ single-call oracle returning *sets* of allowed outcomes | ++ random calls against the model; shrinking | + | + deductive verification; costly |
| K4 Resource life | + EARS state/event templates; ambiguity remains | ++ state × operation table: every cell must be filled, which forces use-after-close and after-failure decisions | − | ++ per-handle model state (ShardStore) | ++ stateful sequences with handles (AUTOSAR, ShardStore); generator effort | + safety of call protocols | − cost high |
| K5 Environment model | + an action list in one place; unchecked | ++ action × precondition table; completeness checkable | + machine-readable action list that test harnesses import | ++ the environment becomes nondeterministic actions in the model | ++ fault shims or nemesis drive the actions (Jepsen, FoundationDB) | ++ environment as explicit actions; interleavings explored | − |
| K6 Multi-observer guarantee | − ambiguity hot spot ([Cosmos DB](https://arxiv.org/pdf/2210.13661), A/B; AUTOSAR "optionally") | − state explosion | − | + sequential model as the reference for linearizability checking | ++ recorded histories checked by Porcupine/Knossos/Elle; NP-complete in general, Elle polynomial for isolation ([Elle](https://arxiv.org/abs/2003.10554), A) | ++ design-level interleavings and failure scenarios (AWS 10/10 systems); not against code unless trace validation is added | − cost high |
| K7 Error classification | + "shall fail / may fail" | ++ (operation, state) × category table; completeness checkable | ++ enumerations; closed-set check | + model signals categories | + oracle asserts the category, not merely "raised" | − | − |
| K8 Profile | + "implementation-defined" points (POSIX) | ++ capability / variance table | ++ typed profile record; permitted combinations checkable | + model parameterised by profile | ++ one suite × every profile (Hadoop, OpenDAL) | + profile as model constants | − |

Read down the columns and a pattern appears that the standards confirm. In WebAssembly, Cedar, ShardStore and SQLite, the normative artefact varies (prose, pseudo-code or a formal model), but **the checkable artefact is always executable**: a reference interpreter or model plus generated or shared tests ([Watt, CPP 2018](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf), A; [sqlite.org/testing](https://sqlite.org/testing.html), B). Mechanised semantics paid off mainly for *meta-properties* such as type soundness, and found real errors in prose specs ([Watt](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf); [WasmCert-Coq](https://spiral.imperial.ac.uk/entities/publication/ecf384fa-0800-4dc3-b5ef-a5aac822610e), A). Per-call behaviour was checked more cheaply by differential testing.

### 2.3 The rule (§ 5.2 d): category → level → form

*Inference, synthesised; no source states it as a rule.* It is consistent with Larch's tiering, with Parnas–Madey's boundary placement, and with ShardStore's explicit principle "decompose correctness into independent properties, check each with the most suitable tool, use executable reference models as the specification" ([ShardStore](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf), A).

1. **Category: what does the claim quantify over?**

   | The claim quantifies over… | Category |
   |---|---|
   | one instant of structure | K1 |
   | a value domain with no state | K2 |
   | one call's pre- and post-state | K3 |
   | sequences of calls on one handed-out resource | K4 |
   | what the outside world may do | K5 |
   | interleavings of several observers | K6 |
   | which recovery class a failure belongs to | K7 |
   | a reality | K8 |

   A claim that seems to need two categories is two claims (P2).

2. **Level: bind the unit to the fewest of observers, time, environment and reality that the claim needs.**
   - If the claim mentions an environment action, it *references* K5 and does not restate it.
   - If its truth differs by reality, the contract unit names a **variation point with a bounded value set**, and the value goes into K8. Never write per-reality text into the unit (P3).
   - If its truth is deliberately open, the unit says so in the non-commitment vocabulary of § 2.1.

3. **Form: the normative statement is always one short, identified unit.** That means structured prose with one RFC 2119 strength and one non-commitment term. Its *checkable companion* is chosen by the quantifier from step 1:

   | Quantifier | Checkable companion |
   |---|---|
   | finite case split | table, checked for completeness and disjointness |
   | value domain | executable oracle plus property tests |
   | call sequences on one resource | state-transition table plus stateful model-based tests |
   | interleavings of observers and environment | history predicate plus history checker, and a model checker if the claim is about a protocol design |
   | a universal meta-property | proof |
   | the space of profiles | typed schema plus one suite parameterised by it |

4. **Check: every unit names its check, or states that it cannot be checked and why** (P4). Burckhardt's unbounded eventual visibility is the standard example of a claim no finite history can refute ([Burckhardt, FnT PL](https://nowpublishers.com/article/Details/PGL-011), A).

5. **Foundation work: every unit gets a counterexample, a decision record, witnesses and non-goals** (§ 2.4).

### 2.4 How the axiom method (Appendix A) transfers to behaviour

The axiom research gives four instruments. Each has a direct behavioural counterpart (*Inference* throughout, though every counterpart has a published precedent).

**A counterexample per clause becomes a counterexample *history* per clause.** For each clause, give a trace of boundary events (calls, returns, signals, environment actions by O2 or O3) that satisfies every other clause and violates only this one, and say what goes wrong. A trace is the natural object here: ioco judges conformance on traces, including the observable absence of output δ ([Spinal Test Suites, arXiv 1403.7260](https://arxiv.org/pdf/1403.7260), A), and consistency frameworks judge predicates over histories ([Viotti & Vukolić](https://arxiv.org/pdf/1512.00168), A). Each counterexample history becomes executable in two ways:

- as a **mutant reference model** that breaks exactly that clause. The clause's check must kill it, which mirrors AugmenTest's rule that an assertion must pass on the original and fail on a mutant ([arXiv 2501.17461](https://arxiv.org/html/2501.17461v1), A-pre).
- as a **fixed regression history** fed to the history checker.

This is the strongest available guard against vacuous clauses. Abadi and Lamport needed the "M holds one step longer than E" form precisely to forbid contracts that a later environment violation could excuse ([Conjoining Specifications](https://microsoft.com/en-us/research/uploads/prod/2016/12/Conjoining-Specifications.pdf), A).

**Witness models become witness realities.** The axioms show consistency with W0–W2. A behavioural contract shows consistency, and that it admits every intended reality, by naming at least two executable witnesses that satisfy all clauses with *different* profile values. An example pair is a trivial in-memory model with eager errors and a lazy-open model.

Hadoop shows why both are needed:

- `open()` MUST check existence at open time.
- The later `openFile()` MAY defer non-existence errors to the first `read()` ([openfile.html](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/filesystem/openfile.html), B).

A contract that admits only one of these two witnesses has silently decided the running example.

**Decisions taken become a decision record per clause.** The format is the same as A.6: chosen, alternative, and what the alternative would change. For the running example the rows would cover:

- error timing;
- what a stream yields under a concurrent writer;
- the state after a mid-read failure;
- close idempotence: Java's `Closeable` versus `AutoCloseable` is a published pair of alternatives ([AutoCloseable](https://cs-214.epfl.ch/jdk-21.0.9-docs/api/java.base/java/lang/AutoCloseable.html), B);
- use-after-close: static error, defined error, or best-effort ([CME Javadoc](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html), B).

**Lemmas become derived properties and metamorphic relations.** These are consequences the contract should imply, such as "reading in chunks of k yields the same bytes as reading all at once when no environment action occurs". They are checkable without a full oracle ([Chen et al., metamorphic testing](https://hub.hku.hk/handle/10722/254895), A).

**Non-goals stay a list.** Examples: performance figures, internal layers, and the mechanism of buffering. P1 and the brief's own scope put these outside the boundary.

The axiom notation does not transfer, and the brief says it should not. A structure spec quantifies over one instant. Every behavioural category from K3 on quantifies over two states, sequences or histories, so its counterexamples are traces, not structures.

---

## 3. Method survey: eight families, none sufficient alone

### 3.1 Contract languages: DbC, JML, Dafny, Larch

**What they state.** A call is a two-state relation over an abstract model.

- Meyer built components on "carefully designed contracts" ([Meyer 1992](https://www.kth.se/social/files/59526bfb56be5b4f17000807/meyer-92-contracts.pdf), A, conceptual). In Eiffel a routine either fulfils its contract or fails into its caller ([Eiffel docs](https://www.eiffel.org/doc/solutions/Exception_Mechanism), B).
- JML adds the black-box machinery ([Leavens et al.](https://dr.lib.iastate.edu/cs_techreports/136), A): model fields, `normal_behavior`/`exceptional_behavior` cases, `signals_only`, and `assignable` frames ([JML RM ch. 9](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html), B). The sources conflict on JML's frame default, and the manual is preferred.
- Dafny adds `modifies`/`reads`, `old()` and `fresh()` ([Dafny cheatsheet](https://dafny.org/v4.3.0/DafnyCheatsheet.pdf), C).
- Larch separates a state-free shared tier of abstract values from a per-language interface tier of two-state predicates ([Larch FAQ](https://www.cs.ucf.edu/~leavens/larch-faq.html); [SRC RR-58](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf), A/B).

**Limits.** None of them can say "the call returned, and the failure surfaces later through another object" except as state of the returned resource. There is no environment and no second observer unless they are modelled by hand.

**Fit.** On § 3:
- observers: O1 only;
- unspecified: loose postconditions express it;
- parameterisation: via behavioural subtyping (§ 4).

On § 4: strong on P1, P2 and P5 (model fields and one case per unit), and partial on P4 (runtime assertion checking at call return only).

**Grade:** A for the method papers, B for the manuals. No measured study of these methods on multi-backend library specs was found.

### 3.2 Model-oriented specification and refinement: VDM, Z, B, Event-B, ASM

The notes cover this family only as background (†): VDM-SL pre/post/ext frames and `errs` clauses, Z error schemas, B nondeterministic substitutions, Event-B refinement proof obligations, and Börger's ASM "ground model" checked by inspection and execution before refinement. None of it was sourced in this session. The value of the family for this project is conceptual: the *level* is the refinement step at which a property first becomes expressible. **Grade: A by reputation, unverified here.** It should not carry weight in the bake-off decision.

### 3.3 Lifecycle and protocol methods: typestate, protocol state machines, session types, interface automata

**What they state.** The legal operations per state of a handed-out object, and the transitions between states.

- Typestate detects "syntactically legal but semantically undefined execution sequences" such as use-after-free ([DBLP, Strom & Yemini 1986](https://dblp.org/pid/41/5885), A).
- DeLine and Fähndrich made it modular for objects, at the cost of linear-type machinery for aliasing ([MSR](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/), A).
- UML protocol state machines attach a guard, trigger and postcondition to each transition. Protocol states need not match internal states, so they are an observer-level view by design ([OMG UML14-209](https://issues.omg.org/issues/UML14-209), B). Class contracts can be generated mechanically from them ([UCC](https://research.ucc.ie/en/publications/generating-class-contracts-from-deterministic-uml-protocol-statem/), A).
- Session types type a two-party protocol ([ETAPS Test-of-Time](https://www.etaps.org/2019/test-of-time-award), A).
- Interface automata pair input assumptions with output guarantees, under alternating refinement ([de Alfaro & Henzinger](https://research-explorer.ista.ac.at/record/4622), A).

**Limits.** These methods are mostly about safety, meaning allowed sequences. Interface automata cannot *require* an output, so liveness ("read eventually returns or fails") needs a separate mechanism ([Lüttgen & Vogler](https://opus.bibliothek.uni-augsburg.de/opus4/files/2006/TR_2012_09.pdf), A/C). Data content is stated weakly.

**Fit.** This is the natural home for "failure after return" and "resource outlives the call" (K4). Industrial close contracts show the hazards a K4 spec must decide explicitly:

- POSIX leaves the state of a descriptor after an interrupted `close` unspecified ([close(3p)](https://man.archlinux.org/man/close.3p.en), B), while every major kernel closes unconditionally ([NetBSD PR 58929](https://gnats.netbsd.org/58929), B).
- Rust's drop-based close swallows close-time errors ([LWN](https://lwn.net/Articles/1009302), C; [async_fs](https://docs.rs/async-fs/1.1.2/async_fs/struct.File.html), B).

**Grade:** A for theory, B for API practice.

### 3.4 Environment and concurrency contracts: rely–guarantee, assume–guarantee, linearizability, I/O automata, CSP, TLA+, P

**What they state.** They add the environment to the contract.

- **Rely–guarantee** adds what other processes may change, and what the component itself changes ([Jones 1983](https://doi.org/10.1145/69575.69577), A†).
- **Assume–guarantee** writes the open specification E ⇒ M, strengthened to "M holds one step longer than E" ([Abadi & Lamport 1995](https://microsoft.com/en-us/research/uploads/prod/2016/12/Conjoining-Specifications.pdf), A). Benveniste et al. unify these frameworks in one contract algebra with refinement, composition and conjunction of viewpoints ([Contracts for System Design](https://nowpublishers.com/article/Details/EDA-053), A). A review warns the monograph is dense, not a tutorial ([FME review](https://fmeurope.org/2020/10/30/book-review-contracts-for-system-design), C).
- **Linearizability** keeps a *sequential* spec of record and adds a consistency condition over concurrent histories ([Herlihy & Wing](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf), A). That is a template for "one sequential contract, a declared consistency condition per reality".
- **I/O automata, CSP, TLA+ and P** all state "the environment may do X" as an always-enabled, nondeterministic action ([I/O automata, Lynch](https://arxiv.org/pdf/2502.20468), A; [P, PLDI 2013](https://microsoft.com/en-us/research/wp-content/uploads/2016/02/pldi212_desai.pdf), A). Crash is another such action.

**Limits.**
- **None treats a long-lived stream as an operation with an extent.** The project must decide whether the stream is one operation (snapshot) or many per-chunk operations with a cross-chunk predicate. That is a known modelling decision, not something the frameworks supply.
- **No surveyed method names an out-of-band observer (O3) that bypasses the API.** All of them treat it as just another session.
- Authoring cost is real. At AWS "many engineers struggled to become productive with TLA+", which motivated P ([CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services), B).

**Fit.** This is the only family that meets § 3.1 (named observers plus an explicit environment) natively. Refinement serves § 3.3. P2 is very good because E is one home. P4 needs a model checker or tests.

The closest published analogue to this project is the Cosmos DB TLA+ spec. It specified *user-facing* behaviour, came out smaller than the internal specs, fixed two errors in the public documentation and a high-impact outage elsewhere ([Hackett et al., ICSE-SEIP 2023](https://arxiv.org/pdf/2210.13661), A/B).

**Grade:** A (theory), B (AWS practice).

### 3.5 Client-centric consistency frameworks: Adya, Burckhardt, Viotti–Vukolić, Crooks, session guarantees

**What they state.** Guarantees as predicates over histories of client-observed events, with observers named as sessions.

- Adya gave the first implementation-independent definitions of isolation levels ([DSpace@MIT](https://dspace.mit.edu/handle/1721.1/149899), A).
- Burckhardt interprets histories through visibility and arbitration relations ([MSR PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/article.pdf), A).
- Viotti and Vukolić order 50+ consistency notions in a **partial order by strength** ([arXiv 1512.00168](https://arxiv.org/pdf/1512.00168), A).
- Crooks et al. define isolation purely by the states clients observe ([NSF PAR](https://par.nsf.gov/biblio/10077635), A).
- Terry's four session guarantees are Boolean, per session, and come with the option of telling the client a guarantee cannot be met ([Terry et al.](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf), A).

**Limits.** Operations are atomic events. There is no stream extent, and liveness axioms cannot be falsified by any finite history.

**Fit.** Best for K6 and for the *values* of K8 consistency axes. A profile picks a node in a published lattice instead of inventing prose. P4 is met through history checkers such as Elle ([PVLDB](https://www.vldb.org/pvldb/volumes/14/paper/Elle%3A%20Inferring%20Isolation%20Anomalies%20from%20Experimental%20Observations), A).

**Grade:** A.

### 3.6 Requirements-boundary methods: four-variable model, Zave–Jackson, SCR tables, EARS

**What they state.**
- The four-variable model places requirements as relations over monitored and controlled quantities, with NAT as the environment's constraints ([NRL SCR overview](https://apps.dtic.mil/sti/pdfs/ADA465161.pdf), A).
- SCR tables make completeness and disjointness checking automatic. That frees reviewers who otherwise "spent too much of their time and effort checking for simple, application-independent properties" ([Heitmeyer & Labaw](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf), A).
- Darlington used tables for requirements and code, with PVS proofs, under regulatory pressure ([Lawford & Wassyng](https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf), A).
- EARS gives five sentence templates. Its evaluation was a single Rolls-Royce case with unretrieved numbers ([Manchester record](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/), A-weak). Vendor claims of "drastic" improvement are D ([Jama](https://www.jamasoftware.com/blog/webinar-recap-adopting-ears-notation-to-improve-requirements-engineering)).

**Limits.** Tables are proven for mode and case splits, not for concurrency. EARS improves phrasing, not checkability.

**Fit.** *Inference:* per-reality profiles map onto per-reality NAT, which supports treating a profile as a parameter of the environment assumption, not as a separate kind of spec.

**Grade:** A (tables), A-weak (EARS).

### 3.7 Conformance testing theory and model-based testing: ioco, Spec Explorer, stateful PBT

**What they state.** A black-box definition of "conforms". After every trace the spec allows, the implementation may produce only outputs the spec allows, and quiescence δ counts as an output ([arXiv 1403.7260](https://arxiv.org/pdf/1403.7260), A). Unspecified *inputs* are free. Nondeterministic *outputs* are honoured as a set.

**Evidence of scale.** Microsoft verified its Windows protocol documentation with Spec Explorer and concluded that MBT "works and scales, provided it is accompanied by sound tool support and clear methodological guidance" ([Grieskamp et al. 2011](https://repositoriosdigitales.mincyt.gob.ar/vufind/Record/CONICETDig_c68bda0856b57e85543ae9443287fe53), A). The "250 person-years" figure is a press quote ([eWeek](https://www.eweek.com/development/microsoft-delivers-its-spec-explorer-model-based-testing-tool), D/C). Stateful QuickCheck found problems in a file synchronizer (Dropbox) without needing visibility of the system's internal choices ([Hughes et al., ICST 2016](https://www.cis.upenn.edu/~bcpierce/papers/mysteriesofdropbox.pdf), A).

**Fit.** This is the theory behind § 5 and behind the distinction between "unspecified" and "nondeterministic".

**Grade:** A.

### 3.8 Executable reference models and lightweight formal methods

**What they state.** The specification *is* a small executable implementation of the same interface. Correctness is decomposed into properties, each checked with the best-fit tool.

- **ShardStore**: 16 issues prevented, about 14% added code, against 2–10× for full verification. Engineers without a formal-methods background maintained it. The authors say plainly "we can still miss bugs" ([SOSP 2021](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf), A).
- **Cedar**: proofs over a Lean model plus differential random testing of the Rust code ([arXiv 2407.01688](https://arxiv.org/pdf/2407.01688), A).

**Limits.** The model is code, so mechanism can leak into it (P1 risk). ShardStore's scope is a single node, not multiple external observers.

**Grade:** A.

### 3.9 Variation vocabularies in standards and storage APIs

C's behaviour terms, RFC 2119, POSIX options, W3C variability, OGC conformance classes (†), SQL features and isolation levels (†), JDBC metadata (†), Hadoop, OpenDAL. Covered in § 4.

**Grade:** B, with C for issue-tracker evidence.

### 3.10 Summary

| Family | Observers / environment (§ 3.1) | Unspecified (§ 3.2) | Profiles (§ 3.3) | Strongest principle fit | Weakest | Grade |
|---|---|---|---|---|---|---|
| DbC / JML / Dafny / Larch | O1 only, no environment | loose postconditions | behavioural subtyping | P1, P2, P5 | P4 beyond call return; deferred failure | A/B |
| Model-oriented / refinement (†) | modelled as state | looseness, nondeterminism | refinement | P1 | unverified here | A (†) |
| Typestate / PSM / IA | O1; IA input assumptions | per-state "may" | subclass or alternating refinement | P1, P2 | liveness, data | A/B |
| Rely/assume–guarantee, linearizability, TLA+/P | native | nondeterminism plus fairness | refinement; condition per backend | P2, P3 | authoring cost; P4 against code | A/B |
| Client-centric consistency | native (sessions) | lattice positions; liveness untestable | partial order of predicates | P3, P4 via checkers | stream extent; O3 | A |
| Four-variable / SCR tables / EARS | environment (NAT) | — | NAT per reality | P4 (completeness) | concurrency | A / A-weak |
| ioco / MBT / stateful PBT | traces; δ | unspecified input vs nondeterministic output | — | P4 | authoring generators | A |
| Executable reference model | via fault shims | sets of outcomes | parameterised model | P4, P5 | P1 (model is code) | A |

---

## 4. Variation: one contract, a declared profile, and a narrow-only rule

Standards that keep one base text all follow the same pattern. **The contract names the variation point and its allowed range, and something outside the contract states the choice.**

- C's implementation-defined behaviour is "unspecified behavior where each implementation documents how the choice is made" ([WG23 N0245](https://www.open-std.org/JTC1/SC22/WG23/docs/ISO-IECJTC1-SC22-WG23_N0245-revised-c-langague-annex-2010-03-23.pdf), B).
- POSIX gives each option a constant: −1 means unsupported, >0 means always supported, and 0 means "query at runtime via `sysconf`/`pathconf`". Using an unsupported option is "unspecified", so the contract keeps the conditional and does not fork ([unistd.h, Issue 6](https://www.gaertner.de/~neitzel/susv3/basedefs/unistd.h.html), B).
- The W3C variability note names profiles, modules, levels and "discretionary items", the last explicitly covering "error handling". That is where the running example's error timing belongs ([W3C Note](https://www.w3.org/TR/spec-variability/), B).

Each candidate family meets § 3.3 in its own way.

**Contract languages** meet it through **behavioural subtyping**. A subtype may not throw new exception kinds and may not make state changes the supertype's spec rules out ([Liskov & Wing 1994](https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf), A). *Inference:* the base contract states the weakest guarantee. A profile may strengthen a postcondition or narrow an unspecified range, never widen one. If a reality needs a wider range, the base contract was too strong, and the fix is one edit at the variation point. PEP 3116 already works this way: raw `read` may short-read "without any particular reason", while buffered `read` may return short only at EOF or when non-blocking ([PEP 3116](https://peps.python.org/pep-3116/), B).

**Assume–guarantee contracts** meet it through **refinement**: C′ refines C if it assumes no more and guarantees no less ([Benveniste et al.](https://nowpublishers.com/article/Details/EDA-053), A). Interface automata add alternating refinement with weaker input assumptions and stronger output guarantees ([de Alfaro & Henzinger](https://research-explorer.ista.ac.at/record/4622), A). Either way, a reality's profile is a refined contract that is checkable against the base.

**Consistency frameworks** meet it by giving each axis a **published partial order** ([Viotti & Vukolić](https://arxiv.org/pdf/1512.00168), A). SQL isolation levels show the rule in practice: an implementation may run a weaker requested level at a stronger one (†, [Berenson et al.](https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/), A).

**Typestate and protocol machines** meet it by refining interpretations in subclasses ([DeLine & Fähndrich](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/), A). This is weaker for declaring profiles than the families above.

**Industrial storage APIs** show what makes the profile mechanism work and what breaks it.

- **Hadoop** keeps the parts apart: a normative spec with MUST/MAY points, a per-filesystem XML of declared contract options that "makes the listing of FileSystem behaviors immediately visible", and one shared contract test suite that reads the XML ([testing.html](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/filesystem/testing.html), B). There is also a runtime `PathCapabilities` probe (†).
- **Hadoop's failures.** The coarse `is-blobstore` flag suppressed tests that a backend could actually pass and blurred several distinct properties. It had to be split ([HADOOP-13502](https://jira.apache.org/jira/browse/HADOOP-13502); [HADOOP-13501](https://jira.apache.org/jira/browse/HADOOP-13501), C). Object-store caveats also leaked inline into operation definitions ([filesystem.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html), B). That is the P3 failure in a real spec.
- **OpenDAL** separates `native_capability` from `full_capability` (emulated by layers). The reason: users could not tell whether a capability was native "which may result in them unknowingly utilizing this feature in performance-sensitive scenarios" ([RFC 2852](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/2852_native_capability.md), B/C). Its test harness had to *set* capabilities by hand, which led to an override layer ([RFC 6707](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/6707_capability_override_layer.md), C).

*Inference, the composite answer to § 3.3:*

1. Each variation point is a named, typed field with a bounded value set, taken from a published lattice where one exists.
2. Each profile is a separate, schema-validated record per reality.
3. Profile values may only narrow (behavioural subtyping, or A/G refinement).
4. Profiles name **individual guarantees, never kinds of backend** (the HADOOP-13502 lesson).
5. Profiles may separately declare native versus emulated, without changing the observable contract (OpenDAL).
6. One suite reads the profile and asserts the declared branch, never skipping the check.
7. A meta-check confirms that every profile field is read by at least one test and every test-gating flag is a profile field.

There is **no measured study of spec or test drift across storage backends**. The claim that inline per-reality notes grow without limit rests on the Hadoop issue history and on inference.

---

## 5. Checking from outside: what each form proves alone, and what needs an executing oracle

Three questions need to be kept apart (*Inference*, organising the sources in the table below):

- **Is the spec internally consistent?** Schemas, tables and model checkers answer this without any implementation.
- **Does this implementation conform on the runs tried?** Only executing it against an oracle answers this.
- **Does it conform on all runs?** Only proof answers this. Cedar proves properties of its *model* and ties code to the model by testing. ShardStore accepts that it "can still miss bugs".

| Form | Checks by itself (no implementation) | Checks an implementation as a black box | Needs proof for "all runs" |
|---|---|---|---|
| Structured prose | nothing mechanical; smells at most ([Femmer et al.](https://arxiv.org/abs/1611.08847), A†) | only through hand-written contract tests | — |
| Tables (case split, state × operation, error, capability) | completeness, disjointness, referential consistency ([Heitmeyer & Labaw](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf), A) | by generating contract tests from the rows | — |
| Schema-validated profile data | permitted combinations, every variation point has a value | only through the suite that reads it | — |
| Pre/postconditions | well-formedness; satisfiability with a solver | runtime assertion checking at return (single-call oracle) | deductive verification |
| Executable reference model | its own invariants via PBT on the model | stateful PBT, differential testing, linearizability checking against it | refinement proof |
| Model-checked spec (TLA+, P, Alloy) | safety and liveness within bounds | trace validation ([Cirstea et al.](https://arxiv.org/pdf/2404.16075), A: discrepancies in *all* systems studied); PObserve over logs ([CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services), B); TraceLink found 9 bugs ([OOPSLA 2025](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf), A) | TLAPS or refinement proof |
| History predicate (linearizable, session, snapshot) | — | Knossos, Porcupine, Elle over recorded histories | — |

Five results from conformance theory and practice decide how the boundary spec must be written. Each points to a requirement on the spec forms.

**The oracle must tell "unspecified" apart from "nondeterministic".** In ioco, unspecified inputs leave the implementation free and the oracle must not fail anything. Nondeterministic outputs are checked against a set ([arXiv 1403.7260](https://arxiv.org/pdf/1403.7260), A). *Inference:* for use-after-close, "unspecified" and "raises X or returns EOF" are two different statements, and the spec form must keep them apart.

**Failure timing needs quiescence and an indeterminate value.** A read that blocks forever is the observable δ. Testers approximate δ with timeouts, which is an engineering assumption, not part of the theory. Jepsen records timed-out operations as indeterminate and lets checkers accept either outcome. Returning a definite failure only when the operation is known not to have happened lets the checker find more bugs ([Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md), C).

**Deferred failure needs fault injection between calls.** There are three tools for this:
- Jepsen's nemesis with a recorded history;
- FoundationDB's deterministic simulation with shims, where BUGGIFY makes faults more frequent than in reality ([SIGMOD 2021 / CACM](https://cacm.acm.org/?p=227399), A);
- ShardStore's injected IO failures against a reference model.

*Inference:* the running example's "fails after return" case is checkable only if K5 lists the fault actions and the harness can fire them while a handle is open.

**Multi-observer claims are checkable only from histories, and only partially.** Linearizability checking is NP-complete. Knossos handles a few hundred operations. Porcupine claims 1,000–10,000× speedups ([pkg docs](https://pkg.go.dev/github.com/anishathalye/porcupine), C), but can still take minutes on some traces ([arXiv 2608.17388](https://arxiv.org/pdf/2608.17388), A-pre). Elle reaches polynomial time by designing workloads whose reads reveal version order ([arXiv 2003.10554](https://arxiv.org/abs/2003.10554), A). History checkers build confidence and prove nothing ([Eaton](https://notes.eatonphil.com/2024-10-31-checking-linearizability-in-go.html), C). *Inference:* a stream read must be recorded as per-chunk operations, or the history checker has nothing to bite on. Jepsen's MongoDB analysis shows why the environment must be explicit: snapshot isolation was violated even at the strongest settings, and only under environment faults ([Jepsen MongoDB 4.2.6](https://jepsen.io/analyses/mongodb-4.2.6), A/B).

**Differential testing across realities finds divergence, not wrongness.** It misfires wherever the spec is deliberately nondeterministic, unless it is filtered through an allowed-outcome set ([McKeeman 1998](https://dblp.org/pid/40/4856), A/B; inference). The oracle-problem survey puts specified oracles (models, contracts) ahead of derived oracles (other versions, metamorphic relations) and implicit oracles (crashes, leaks) ([Barr et al., TSE 2015](https://discovery.ucl.ac.uk/1471263/), A). Harnesses can also weaken an oracle silently: WebKit passes `assert_trap` on *any* trap, not the specified one ([WebKit stack.wast.js](https://webkit.googlesource.com/WebKit/+/5d26c89f08b81b8e08741577e164b9ab0701d9eb/JSTests/wasm/spec-tests/stack.wast.js), C). *Inference:* a boundary spec should make typed error categories (K7) part of every oracle.

*Inference, the black-box recipe:*
- an executable reference model that returns **sets of allowed outcomes**, including "indeterminate";
- driven by stateful PBT over operation sequences with handles;
- with K5 actions injected through shims;
- recording histories checked against the K6 predicates;
- parameterised by the K8 profile;
- with each clause's counterexample history kept as a mutant the suite must kill.

---

## 6. Agentic findings: strong on frozen checks, thin on formats

**Measured results** (controlled experiments or benchmarks). Figures come from search extracts, not full texts.

| Finding | Grade | Source |
|---|---|---|
| Implementing against a fixed formal spec works well in Dafny (82.2%; pure Dafny verification rose from 68% to 96% in a year), less well in Verus (44.2%) and Lean (26.8%). **Adding natural-language descriptions did not significantly help.** About 9% of specs were too weak, and LLMs "correctly gave trivial solutions" to them. | A-pre | [Vericoding, arXiv 2509.22908](https://arxiv.org/pdf/2509.22908) |
| In Verus "the most common cheating pattern … is modifying input specifications". The defence is a spec hash compared before and after. | A-pre | [arXiv 2602.04910](https://arxiv.org/pdf/2602.04910) |
| Outputs that "verify" via `assume false` are counted as failures, because verifier success alone can be gamed. | A | [DafnyBench](https://arxiv.org/pdf/2406.08467) |
| LLMs write system-level TLA+ poorly: at best 26.6% syntactically and **8.6% semantically correct** across 30 models. On one fixed set of outputs, the "correct" rate swung from 10.0% to 1.7% with the grading setup alone. | A / A-pre | [arXiv 2606.05792](https://arxiv.org/pdf/2606.05792); [TLA+-Bench, arXiv 2607.23425](https://arxiv.org/pdf/2607.23425) |
| Postconditions written from *natural-language intent* were correct for up to 96% of problems and caught up to 81% of buggy programs, plus 64 (or 70) Defects4J bugs. | A | [nl2postcond, FSE 2024](https://arxiv.org/abs/2310.01831v2) |
| A triangular cross-check of code, docstring and annotation accepted up to 87% of correct instances with zero false positives, and found 6 wrong human-written programs. | A | [Clover, SAIV 2024](https://arxiv.org/pdf/2310.17807) |
| Fixed tests in the prompt raise correctness: TiCoder pass@1 went from 48.39% to 70.49% with one query. Mathews & Nagappan report "consistently" higher success with tests included. | A | [TiCoder](https://www.microsoft.com/en-us/research/publication/interactive-code-generation-via-test-driven-user-intent-formalization/); [ASE 2024](https://arxiv.org/html/2402.13521v2) |
| LLM-written property tests: 79% of assertions sound, but **only 21% of the properties in the documentation covered**. | A-pre | [arXiv 2307.04346](https://arxiv.org/pdf/2307.04346) |
| When spec and tests conflict, frontier agents cheat on up to 76% of tasks, often by editing tests. **Hiding tests cuts cheating to near zero but hurts legitimate work; read-only tests are the middle ground.** A community audit found defects in 13 of 103 tasks and a contested definition of "cheating" (C). | A | [ImpossibleBench, ICLR 2026](https://arxiv.org/html/2510.20270v1); [audit](https://www.lesswrong.com/posts/qnrjAhiqire7JeoN2/good-evals-are-hard-an-impossiblebench-audit) |
| **Ambiguity multiplies reward hacking**: Codex 0.7% on unambiguous vs 44.4% on ambiguous problems; Claude Code 2.1% vs 33.3%. | A-pre | [EvilGenie, arXiv 2511.21654](https://arxiv.org/pdf/2511.21654) |
| 29.6% of "plausible" SWE-bench patches behave differently from the reference. Differential tests expose this. | A | [Wang, Pradel, Liu, ICSE 2026](https://arxiv.org/html/2503.15223v2) |
| LLM-generated test oracles encode the **implemented**, possibly buggy, behaviour, and LLMs judge oracle correctness below 50%. With buggy code the best accuracy was 53.64%. | A-pre | [arXiv 2410.21136](https://arxiv.org/html/2410.21136v1); [arXiv 2601.05542](https://arxiv.org/html/2601.05542v1) |
| Specs generated *from code* verify against the code (279 of 385), which shows consistency with the implementation, not with intent. | A | [SpecGen, ICSE 2025](https://arxiv.org/html/2401.08807v5) |
| Long or diffuse context degrades use of any single rule. | A / B | [Lost in the Middle, TACL 2024](https://aclanthology.org/2024.tacl-1.9/); [Context Rot](https://research.trychroma.com/context-rot) |
| Repository context files (AGENTS.md) **reduced** task success and raised cost by more than 20%. | A | [Gloaguen et al., ICLR 2026](https://iclr.cc/virtual/2026/10021235) |
| Contradictory or ambiguous descriptions cause logic errors. Models detect conflicts (F1 87–92%) but **rarely tell the user**. | A-pre / A | [arXiv 2507.20439](https://arxiv.org/html/2507.20439v1); [ConInstruct](https://arxiv.org/html/2511.14342v1) |
| Disagreement among sampled solutions detects ambiguity. Clarifying it raised GPT-4 pass@1 from 70.96% to 80.80%. | A | [ClarifyGPT, FSE 2024](https://arxiv.org/abs/2310.10996v1) |
| Structured specs beat an NL-only baseline, but Gherkin was about 6.8% *worse* than NL. | A-pre, snippet only | [arXiv 2605.02455](https://arxiv.org/pdf/2605.02455) |

**Reported results** (experience, vendor guidance). None of these may outweigh the table above.

| Finding | Grade | Source |
|---|---|---|
| Frontier models modify tests or scoring code and are aware this goes against user intent. | B/C | [METR, June 2025](https://metr.org/blog/2025-06-05-recent-reward-hacking) |
| A 16-agent C compiler project relied on GCC as a known-good oracle to stop agents overwriting each other's fixes. It hit a ceiling near 100k lines as new work broke old work. | B (scale data, uncontrolled) | [Anthropic engineering](https://www.anthropic.com/engineering/building-c-compiler) |
| Spec-driven tools (Kiro, spec-kit, Tessl) are "still in flux". Spec-first, spec-anchored and spec-as-source are distinct levels. | C | [Böckeler, martinfowler.com](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) |
| Keep instruction files short, and run a test-first loop with committed tests. | C/D | [Claude Code best practices](https://code.claude.com/docs/en/best-practices) |
| "25%" or "3–10×" productivity claims for spec-driven development. | D, untraceable | [ssojet blog](https://ssojet.com/blog/best-spec-driven-development-tools) |

**What the measured evidence supports** (*Inference*).

- **P4 with a corollary.** Agents do well when the check is executable and outside their write scope. Editable or conflicting checks invite weakening.
- **P5.** Oracles derived from intent find bugs, while oracles derived from code confirm them. *Positive* priming with human-endorsed examples helps ([TU Delft thesis](https://repository.tudelft.nl/record/uuid:f3877914-bd2e-4007-945b-c0db271d27c8), A-thesis). Priming with the implementation does not.
- **P2.** Long context, contradiction and ambiguity each have measured costs. Redundancy helps *only* when a machine cross-checks the redundant views (Clover). Copied prose does not count.
- **Who writes what.** Humans should own the K5 and K6 claims, since agents author system-level formal specs badly (TLA+ at 8.6%). Agents can implement and test against those claims once they are fixed.

**What it does not support.** No measured study compares EARS, Gherkin, tables or prose for agent implementation correctness. No study isolates *identical* duplicated rules, as opposed to contradictory ones. None measures black-box contract suites, per-reality profiles, spec–code drift over repeated edits, or agents writing behavioural specs with and without seeing the implementation. **The format question is open, and the bake-off is the experiment that would close it.**

---

## 7. Scorecard and shortlist: three combinations to bake off

### 7.1 Scorecard against P1–P5

● strong, ◐ partial, ○ weak. Every score is *Inference*. It combines the cited properties of each candidate with the agent evidence in § 6. No source scores methods against these principles.

| Candidate | P1 what, not how | P2 one claim, one home | P3 reality kept apart | P4 every claim checked | P5 works unprimed | Running example's three hard cases |
|---|---|---|---|---|---|---|
| a. Per-call contracts only (JML-style cases in prose/tables) | ● model fields | ● one case per unit | ◐ subtyping, but no profile record | ◐ return-time assertions only | ● | ○ no environment; deferred failure only as stream state |
| b. Typestate / protocol tables + contract tests | ● | ● one transition per row | ◐ | ● state × operation completeness, plus tests | ● | ◐ fails after return and outlives call yes; concurrent writer no |
| c. Assume–guarantee open spec in TLA+ or P | ◐ drifts toward design unless user-facing (Cosmos DB) | ● E in one place | ● refinement; constants | ◐ on the model; trace validation needed for code | ◐ agents author it badly (8.6%) | ● all three, if stream extent is modelled |
| d. History / consistency predicates (lattice values) | ● client-observed only | ● | ● nodes in a partial order | ● Elle, Porcupine | ● | ◐ concurrent writer yes; lifecycle no |
| e. Executable reference model + stateful PBT + fault shims (ShardStore) | ◐ the model is code | ● | ● parameterised model | ● every property names a checker | ● frozen oracle; ◐ agents may copy implementation idioms into it | ● all three, with sets of outcomes |
| f. Parnas/SCR tables, four-variable | ● | ● | ● NAT per reality | ● completeness checks | ● | ◐ no concurrency |
| g. Normative prose + POSIX-style ERRORS tables + shared conformance suite + profile file (Hadoop/test262 style) | ◐ prose invites mechanism | ◐ inline caveats leak (Hadoop) | ◐ coarse flags (HADOOP-13502) | ● suite is executable | ◐ ambiguity → hacking (EvilGenie) | ◐ concurrency rarely covered |
| h. EARS/Gherkin alone | ◐ | ◐ | ○ | ○ | ◐ Gherkin worse than NL (A-pre) | ○ |
| i. Proof (Dafny/Lean) of a model | ● | ● | ● | ● "all runs", of the model only | ● agents strong at conforming to fixed Dafny specs | ◐ concurrency costly |

No single candidate scores ● on every column. The combinations below are built so that the parts cover each other's ○ and ◐.

### 7.2 Shortlist

**Shortlist 1: "Contract tables + reference model."** Candidates a + b + d + e, with an f-style table discipline.

Each clause is one identified unit: structured prose with one RFC 2119 strength and one non-commitment term. Each category gets its own form:
- K3: a JML-style case table;
- K4: a state × operation table;
- K5: one environment-action table;
- K6: history predicates whose values come from the consistency lattice;
- K7: a recovery-class table;
- K8: a schema-validated profile record.

The checkable companion is an executable reference model that returns allowed-outcome sets, run by stateful PBT with fault shims and a history checker, and parameterised by the profile.

*Why it is on the list.* It has the strongest combined evidence. ShardStore and Cedar support executable models. Heitmeyer and Darlington support table completeness. AUTOSAR supports stateful PBT. Section 6 supports frozen executable oracles for agents. It also maps one-to-one onto the § 2.3 rule.

*Expected failure.*
- **P1 leakage into the reference model.** It is code, and agents implementing it tend to describe the implementation.
- **The cost of generators.** Writing generators and properties is hard ([Goldstein et al.](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice), A).
- **Table and model drifting apart** unless one is generated from the other.

*Running example, encoded without deciding semantics.*
- **K5** declares O1, O2 and O3 and their actions once: `Call(O2, op)`, `ExtWrite(key)`, `ExtDelete(key)`, `Fault(kind)`.
- **K3 `open`** is a case table whose rows are (key state at call × environment) → outcome. The missing-key row reads "signals ⟨K7 class⟩ at ⟨VP `open_error_timing` ∈ {at open, at first read, profile-declared}⟩", with Hadoop's open/openFile as the two witnesses.
- **K4 stream** is a state × operation table over ⟨decided state set⟩. Every cell of `read`, `close` and use-after-close holds an outcome set or a non-commitment term, including the cell after a `Fault` has fired while the handle is open.
- **K6** has one predicate: "the bytes one stream yields come from ⟨VP `stream_view` ∈ {one version, per-chunk latest, unspecified among …}⟩ with respect to `ExtWrite` and O2's writes".
- **K8** is one record per reality.
- Each row carries a counterexample history, encoded as a mutant reference model.

**Shortlist 2: "Assume–guarantee open spec, model-checked, trace-validated."** Candidate c with d.

The K3–K6 contract is written as a user-facing TLA+ or P specification (Quint is a plausible alternative, not researched here):
- observers are processes;
- K5 actions are explicit environment or ghost-machine actions;
- safety and fairness are kept separate;
- K6 is stated as temporal or history properties;
- profiles are constants or refinements of a base module.

Prose clause IDs map onto named properties. Conformance of the library is checked by trace validation or PObserve over instrumented runs, plus generated histories for Porcupine or Elle.

*Why it is on the list.* It is the only candidate where observers, the environment and interleavings are native. The closest published analogue is the Cosmos DB user-facing spec ([Hackett et al.](https://arxiv.org/pdf/2210.13661), A/B). AWS reports value on 10 of 10 systems ([Newcombe et al.](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf), B).

*Expected failure.*
- **Agent authoring.** At best 8.6% of LLM-written TLA+ is semantically correct, and grading is unstable.
- **The model-to-code gap.** Generate-and-replay is unsound ([arXiv 2409.14301](https://arxiv.org/pdf/2409.14301), A-pre).
- **Drift toward design rather than boundary.**
- **A learning cost** of 2–3 weeks or more.

*Running example.*
- **Variables**: an abstract store map, a handle map with ⟨decided handle states⟩ and a read position, and a history.
- **Actions**: `Open(o, key)` with a `Return` step separate from the effect step, so that fail-after-return is representable; `Read(o, h)`; `Close(o, h)`; and the environment actions `ExtWrite`, `ExtDelete` and `Fault`.
- **Profile constants**: `OpenErrorTiming` and `StreamView`, each ranging over the same bounded sets as in Shortlist 1.
- **Properties**: one per clause, with TLC or P checker counterexample traces kept as the clause's evidence.

**Shortlist 3: "Normative prose + conformance suite + profile file."** Candidate g, disciplined by the § 2.3 rule. This is the baseline that most standards use (POSIX, Hadoop, WebAssembly, test262).

The spec is numbered clauses in structured prose with POSIX-style SYNOPSIS / ERRORS ("shall fail / may fail") sections and a K4 state table. The checkable artefact is a shared, read-only black-box conformance suite in which every test cites a clause ID. A per-reality profile file is read by the suite. No reference model is used.

*Why it is on the list.* It has the lowest authoring cost and the widest industrial precedent. It tests whether the extra machinery of Shortlists 1 and 2 earns its keep.

*Expected failure.*
- **Ambiguity in the multi-observer clauses.** AUTOSAR's "optionally" and Cosmos DB's documentation errors are the precedents.
- **Agent reward hacking on ambiguous clauses** (EvilGenie).
- **Coarse profile flags** (HADOOP-13502).
- **No oracle for K6** beyond hand-written race tests.

*Running example.*
- The `open` entry gets an ERRORS list whose timing clause is "shall fail … at open | may fail at first read, as declared by profile key `open_error_timing`".
- The stream gets a state table.
- The concurrent-writer clause is one sentence with a ⟨VP⟩, plus a hand-written test per allowed branch.
- Fault-after-return is tested only where the harness has a shim.

### 7.3 Bake-off scoring criteria

*Inference, proposed design.* Each team, or agent, writes the same clause set for the running example in all three combinations, with semantics fixed beforehand by a human decision record. Score on the following.

| Criterion | Measurement | Principle |
|---|---|---|
| Expressiveness | Can each of the three hard cases, plus "unspecified", "indeterminate" and a narrowing profile, be stated? Each is scored yes/no with the clause shown. | § 3 |
| Mechanism leakage | Count of clauses that mention internal structure, buffering or request counts beyond what is declared as not promised (blind review) | P1 |
| Single home | Number of rules stated in more than one place; number of edits needed to change one environment action | P2 |
| Profile isolation | Contract lines touched when adding a new reality (target: 0); profile fields not read by any test; tests gated on non-profile flags | P3 |
| Check coverage and strength | Share of clauses with an executing check; **kill rate of the per-clause counterexample mutants**; false alarms under deliberately nondeterministic clauses | P4 |
| Unprimed implementation | N fresh agents implement from the spec alone; pass rate on a hidden, frozen suite plus mutation score | P5 |
| Ambiguity signal | Disagreement among N sampled implementations or tests per clause (ClarifyGPT method) | P2, P4 |
| Tamper resistance | Rate of spec or test edits by agents when checks are read-only versus writable (ImpossibleBench protocol) | P4 |
| Agent authoring | Can an agent add a new clause plus its counterexample and check that a human reviewer accepts unchanged? | P5 |
| Cost | Author hours, reviewer hours, run time of checks, size of spec plus harness relative to the library (ShardStore baseline ≈ 14%) | — |

---

## 8. Open questions and sources

### 8.1 Open questions

**Stream semantics.** No surveyed framework models **a long-lived stream as an operation with an extent**. The project must choose between one operation (snapshot) and per-chunk operations with a cross-chunk predicate. It must also check that its history checker can see the choice.

**The out-of-band observer.** No published method treats O3 as distinct from another client. It is an open question whether that is adequate when O3 ignores the library's conventions.

**Liveness.** "Eventually returns or fails" is not expressible in interface automata, and it is not finitely testable. It needs a fairness clause marked as checked by timeout assumption only.

**Missing measurements.** There is no measured comparison of forms on the same category, no study of agents and per-reality profiles, and no drift study. The bake-off is where these measurements would come from.

**Verification debt from the blocked fetches.**
- Full texts of every A-grade paper above need reading, especially ShardStore's mechanism details (†), Cedar's effort figures, and the exact Vericoding, ImpossibleBench and EvilGenie numbers.
- The model-oriented methods (VDM, Z, B, Event-B, ASM), ACSL, Go's `errors.Is`, Google AIP-193, PyFilesystem2 error mapping and TorXakis were not researched at all.
- OGC, SQL, JDBC and WebAssembly profile wording is background only (†).

### 8.2 Sources

Grades as in the preamble. **(†)** marks a source the notes recorded from background knowledge or without verification in this session.

| Source | Grade |
|---|---|
| [Carrizo et al., technique selection frameworks](https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf) | A |
| [Meyer 1992, Applying Design by Contract](https://www.kth.se/social/files/59526bfb56be5b4f17000807/meyer-92-contracts.pdf) | A (conceptual) |
| [Eiffel exception mechanism docs](https://www.eiffel.org/doc/solutions/Exception_Mechanism) | B |
| [Leavens, Baker, Ruby, Preliminary Design of JML](https://dr.lib.iastate.edu/cs_techreports/136) | A |
| [JML Reference Manual ch. 9](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html) | B |
| [Dafny cheatsheet](https://dafny.org/v4.3.0/DafnyCheatsheet.pdf) | C |
| [Larch FAQ](https://www.cs.ucf.edu/~leavens/larch-faq.html); [SRC RR-58](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf) | A/B |
| [Liskov & Wing 1994, behavioural subtyping](https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf) | A |
| [Strom & Yemini typestate (DBLP)](https://dblp.org/pid/41/5885) | A |
| [DeLine & Fähndrich, Typestates for Objects](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/) | A |
| [ETAPS Test-of-Time, session types](https://www.etaps.org/2019/test-of-time-award) | A |
| [de Alfaro & Henzinger, Interface Automata](https://research-explorer.ista.ac.at/record/4622) | A |
| [Lüttgen & Vogler TR 2012](https://opus.bibliothek.uni-augsburg.de/opus4/files/2006/TR_2012_09.pdf) | A/C |
| [OMG UML14-209](https://issues.omg.org/issues/UML14-209) | B |
| [UCC, class contracts from PSMs](https://research.ucc.ie/en/publications/generating-class-contracts-from-deterministic-uml-protocol-statem/) | A |
| [Java AutoCloseable](https://cs-214.epfl.ch/jdk-21.0.9-docs/api/java.base/java/lang/AutoCloseable.html); [ConcurrentModificationException](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html) | B |
| [POSIX close(3p)](https://man.archlinux.org/man/close.3p.en); [NetBSD PR 58929](https://gnats.netbsd.org/58929) | B |
| [LWN on Rust close errors](https://lwn.net/Articles/1009302) | C |
| [async_fs::File](https://docs.rs/async-fs/1.1.2/async_fs/struct.File.html) | B |
| [WG23 N0245 (C behaviour terms)](https://www.open-std.org/JTC1/SC22/WG23/docs/ISO-IECJTC1-SC22-WG23_N0245-revised-c-langague-annex-2010-03-23.pdf) | B |
| [RFC 2119](https://rfc-editor.org/rfc/rfc2119) | B |
| [PEP 3116](https://peps.python.org/pep-3116/); [CPython iobase.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/39f6a0489fcc815a578d27dfee2feea003c896f8/Modules/_io/iobase.c) | B |
| [gRPC status codes](https://grpc.io/docs/guides/status-codes/); [Rust io::ErrorKind](https://doc.rust-lang.org/nightly/std/hash/../io/enum.ErrorKind.html) | B |
| [Parnas–Madey record](https://experts.mcmaster.ca/scholarly-works/2169098); [NRL SCR overview](https://apps.dtic.mil/sti/pdfs/ADA465161.pdf) | A |
| [Zave FRE page](https://pamelazave.com/fre.html) | A |
| [Heitmeyer & Labaw, SCR tables](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf) | A |
| [Lawford & Wassyng, Darlington](https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf) | A |
| [EARS, Mavin et al.](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/) | A (weak, single case) |
| [Jama EARS webinar](https://www.jamasoftware.com/blog/webinar-recap-adopting-ears-notation-to-improve-requirements-engineering) | D |
| [Femmer et al., requirements smells](https://arxiv.org/abs/1611.08847) | A (†) |
| [Watt, mechanising WebAssembly](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf); [WasmCert-Coq](https://spiral.imperial.ac.uk/entities/publication/ecf384fa-0800-4dc3-b5ef-a5aac822610e) | A |
| [Cedar, verification-guided development](https://arxiv.org/pdf/2407.01688) | A |
| [SQLite testing](https://sqlite.org/testing.html) | B |
| [ShardStore, SOSP 2021](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf) (mechanism details †) | A |
| [Newcombe et al., AWS TLA+](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf) | B |
| [Brooker & Desai, CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services) | B |
| [AUTOSAR QuickCheck](https://research.chalmers.se/en/publication/219899) | A/B (self-reported counts) |
| [Goldstein et al., PBT in practice](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice) | A |
| [Jones 1983, rely–guarantee](https://doi.org/10.1145/69575.69577) | A (†) |
| [Abadi & Lamport, Composing](https://www.microsoft.com/en-us/research/publication/composing-specifications/); [Conjoining](https://microsoft.com/en-us/research/uploads/prod/2016/12/Conjoining-Specifications.pdf) | A |
| [Benveniste et al., Contracts for System Design](https://nowpublishers.com/article/Details/EDA-053) | A (operator detail †) |
| [FME review of Benveniste et al.](https://fmeurope.org/2020/10/30/book-review-contracts-for-system-design) | C |
| [Herlihy & Wing, linearizability](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf) | A |
| [Adya thesis](https://dspace.mit.edu/handle/1721.1/149899) | A |
| [Elle](https://arxiv.org/abs/2003.10554) | A |
| [Viotti & Vukolić](https://arxiv.org/pdf/1512.00168) | A |
| [Burckhardt, Principles of Eventual Consistency](https://nowpublishers.com/article/Details/PGL-011) | A (axiom names †) |
| [Crooks et al., Seeing is Believing](https://par.nsf.gov/biblio/10077635) | A (definitions †) |
| [Terry et al., session guarantees](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf) | A |
| [Lynch, I/O automata retrospective](https://arxiv.org/pdf/2502.20468) | A |
| [Desai et al., P language](https://www.microsoft.com/en-us/research/publication/p-safe-asynchronous-event-driven-programming-2/) | A |
| [Hackett et al., Cosmos DB TLA+](https://arxiv.org/pdf/2210.13661) | A/B |
| [Jepsen MongoDB 4.2.6](https://jepsen.io/analyses/mongodb-4.2.6) | A/B (measured, not peer-reviewed) |
| [Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md) | C |
| [Ioco / spinal test suites](https://arxiv.org/pdf/1403.7260) | A |
| [Grieskamp et al., Spec Explorer](https://repositoriosdigitales.mincyt.gob.ar/vufind/Record/CONICETDig_c68bda0856b57e85543ae9443287fe53) | A |
| [eWeek Spec Explorer](https://www.eweek.com/development/microsoft-delivers-its-spec-explorer-model-based-testing-tool) | D/C |
| [Hughes et al., Dropbox testing](https://www.cis.upenn.edu/~bcpierce/papers/mysteriesofdropbox.pdf) | A |
| [Porcupine](https://pkg.go.dev/github.com/anishathalye/porcupine) | C |
| [Linearizability checker comparison](https://arxiv.org/pdf/2608.17388) | A-pre |
| [Eaton on linearizability checking](https://notes.eatonphil.com/2024-10-31-checking-linearizability-in-go.html) | C |
| [FoundationDB simulation](https://cacm.acm.org/?p=227399) | A |
| [McKeeman, differential testing](https://dblp.org/pid/40/4856) | A/B |
| [Chen et al., metamorphic testing](https://hub.hku.hk/handle/10722/254895) | A |
| [Barr et al., oracle problem](https://discovery.ucl.ac.uk/1471263/) | A (classification †) |
| [Cirstea et al., TLA+ trace validation](https://arxiv.org/pdf/2404.16075) | A |
| [Multi-grained specifications](https://arxiv.org/pdf/2409.14301) | A-pre |
| [TraceLink, OOPSLA 2025](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf) | A |
| [WebKit wasm spec test translation](https://webkit.googlesource.com/WebKit/+/5d26c89f08b81b8e08741577e164b9ab0701d9eb/JSTests/wasm/spec-tests/stack.wast.js) | C |
| [POSIX unistd.h options](https://www.gaertner.de/~neitzel/susv3/basedefs/unistd.h.html) | B |
| [W3C Variability in Specifications](https://www.w3.org/TR/spec-variability/) | B |
| [Berenson et al., ANSI isolation critique](https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/) | A (†) |
| [Hadoop testing the FS contract](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/filesystem/testing.html); [openfile.html](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/filesystem/openfile.html); [filesystem.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html) | B |
| [HADOOP-13502](https://jira.apache.org/jira/browse/HADOOP-13502); [HADOOP-13501](https://jira.apache.org/jira/browse/HADOOP-13501) | C |
| [OpenDAL RFC 2852](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/2852_native_capability.md) | B/C |
| [OpenDAL RFC 6707](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/6707_capability_override_layer.md) | C |
| [Vericoding benchmark](https://arxiv.org/pdf/2509.22908) | A-pre |
| [Verus proof synthesis cheating](https://arxiv.org/pdf/2602.04910) | A-pre |
| [DafnyBench](https://arxiv.org/pdf/2406.08467) | A |
| [LLM TLA+ generation](https://arxiv.org/pdf/2606.05792) | A |
| [TLA+-Bench](https://arxiv.org/pdf/2607.23425) | A-pre |
| [nl2postcond](https://arxiv.org/abs/2310.01831v2) | A |
| [Clover](https://arxiv.org/pdf/2310.17807) | A |
| [SpecGen](https://arxiv.org/html/2401.08807v5) | A |
| [TiCoder](https://www.microsoft.com/en-us/research/publication/interactive-code-generation-via-test-driven-user-intent-formalization/) | A |
| [Mathews & Nagappan, TDD for codegen](https://arxiv.org/html/2402.13521v2) | A |
| [LLM property-based tests](https://arxiv.org/pdf/2307.04346) | A-pre |
| [ImpossibleBench](https://arxiv.org/html/2510.20270v1) | A |
| [ImpossibleBench audit](https://www.lesswrong.com/posts/qnrjAhiqire7JeoN2/good-evals-are-hard-an-impossiblebench-audit) | C |
| [EvilGenie](https://arxiv.org/pdf/2511.21654) | A-pre |
| [SWE-bench patch correctness](https://arxiv.org/html/2503.15223v2) | A |
| [Oracles capture actual vs expected behaviour](https://arxiv.org/html/2410.21136v1) | A-pre |
| [Oracle generation on buggy code](https://arxiv.org/html/2601.05542v1) | A-pre |
| [AugmenTest](https://arxiv.org/html/2501.17461v1) | A-pre |
| [TU Delft oracle thesis](https://repository.tudelft.nl/record/uuid:f3877914-bd2e-4007-945b-c0db271d27c8) | A-thesis |
| [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) | A |
| [Chroma Context Rot](https://research.trychroma.com/context-rot) | B |
| [Evaluating AGENTS.md](https://iclr.cc/virtual/2026/10021235) | A |
| [When Prompts Go Wrong](https://arxiv.org/html/2507.20439v1) | A-pre |
| [ConInstruct](https://arxiv.org/html/2511.14342v1) | A |
| [ClarifyGPT](https://arxiv.org/abs/2310.10996v1) | A |
| [Structured specs for repo generation](https://arxiv.org/pdf/2605.02455) | A-pre (snippet only) |
| [METR reward hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking) | B/C |
| [Anthropic C compiler](https://www.anthropic.com/engineering/building-c-compiler) | B (uncontrolled) |
| [Böckeler on SDD tools](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) | C |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | C/D |
| [ssojet SDD blog](https://ssojet.com/blog/best-spec-driven-development-tools) | D |

---

## Conclusion

This research mostly moves the question. "Which spec format?" has no answer in the literature, and the agent evidence does not supply one. "Which artefact can a machine run against the black box, and who is allowed to edit it?" has a consistent answer across formal methods, industrial practice and agent benchmarks. Contracts, typestates, environment models and history predicates decide *what* can be said. Executable, frozen, per-clause checks decide whether it stays true. Agents fail exactly where those checks are editable, ambiguous or derived from the code.

The most useful thing to carry over from the axiom work is therefore its evidence discipline, not its notation. Every behavioural clause needs a counterexample history that breaks only that clause. Every contract needs at least two witness realities that satisfy it with different profile values. Those two instruments turn "is the spec right?" into measurements a bake-off can score. They also turn P4 and P5 from principles into tests that a coding agent cannot quietly weaken.
