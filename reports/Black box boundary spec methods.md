# Bind every spec category to its check

Revision history: [CHANGELOG](CHANGELOG.md). v1 (search extracts only) is at git tag `report-v1`.

The best-founded method for specifying observable behaviour at a black-box library boundary is not a single notation. It is **Design by Contract extended into an assume–guarantee contract**, with five parts:

1. An abstract model of observable state with per-call normal and exceptional cases (Meyer, JML, Larch).
2. A typestate for every resource the library hands out.
3. An explicit environment clause that names the observers and every action the outside world may take (Jones's rely–guarantee, Abadi–Lamport's E ⇒ M).
4. History predicates over interval operations for what several observers see (linearizability, Lamport's registers, session guarantees, client-centric isolation).
5. Named variation points whose bounded value sets per-reality profiles may only narrow, never widen (Liskov–Wing behavioural subtyping, now with direct normative precedent in SQL-92 and WebAssembly 3.0).

**No validated rule maps specification category to level to form.** Coarse published heuristics do exist, and they point the same way as this report. State-based and functional specifications "are thus better targeted at transactional systems", and history- and transition-based specifications at reactive ones ([van Lamsweerde, ICSE 2000](https://homepage.cs.uiowa.edu/~tinelli/classes/5810/Fall20/Papers/vLam00.pdf), A). "The type of analysis … determine[s] the most appropriate level of formalization" ([NASA-GB-002-95](https://www.fing.edu.uy/inco/grupos/mf/TPPSF/Bibliografia/fmguide1.pdf), B/C). A method's advocate should state "the method's domain of applicability" ([Wing 1990](https://www.cs.cmu.edu/~wing/publications/Wing90a.pdf), A). None of these heuristics is validated by outcome data, and none reaches the granularity of observers, environment and reality. The selection frameworks that do exist cover elicitation techniques, and the earlier ones had "little validation" ([Carrizo et al., WER 2008](https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf), A).

The rule offered here, **choose the form by what the claim quantifies over**, refines those heuristics. Industrial evidence supports it:
- **ShardStore.** Executable reference models with property-based tests and stateless model checking found crash-consistency and concurrency bugs.
- **Cedar.** Proofs over a Lean model, plus differential random testing, found validator-soundness, termination, parser and evaluator divergences.
- **AWS and Cosmos DB.** Model checking paid off on concurrency.
- **Darlington and SCR.** Tables make case-split completeness and disjointness mechanically checkable.

The agent evidence is strong on one point and thin everywhere else. Agents conform well to **fixed, machine-checked specs**: the best single model solved two-thirds of Dafny tasks. They measurably game checks that are **editable, or that contradict the spec**. No controlled study compares written formats for coding agents. The few controlled single-shot LLM comparisons find that notation alone does not beat prose. The bake-off proposed in § 7 would produce the missing evidence.

**Evidence status, stated up front.** The earlier edition rested entirely on search-engine extracts, because the session's proxy blocked full texts.

The verification pass on 2026-10-22 ran in five tracks and used full texts only. It checked **170 claims**: every † item, every figure, percentage and quotation, and every A- or B-graded claim within the tracks' scope. The verdicts were:
- 101 confirmed;
- 41 corrected;
- 7 not found in the cited source;
- 5 refuted;
- 15 unverifiable because the full text was unreachable;
- 1 C/D row not re-read.

**Read in full this time:**
- every agent paper in § 6, from arXiv PDFs;
- ShardStore (Amazon Science copy), Cedar, the AWS TLA+ 2014 draft and Cosmos DB;
- Jones 1983, Abadi–Lamport (author copies), P (author copy), Herlihy–Wing, Liskov–Wing, Terry et al., the Adya thesis, Crooks et al., Viotti–Vukolić, Elle, Lamport 1986 and interval-linearizability;
- Tretmans 2008, Barr et al. (author copy) and Femmer et al.;
- Spec#, the ACSL, VDM-10, Z and Atelier B manuals, van Lamsweerde, the NASA guidebooks and Wing 1990;
- standards and official docs: ISO C N1570, the SQL-92 draft (unofficial mirror), POSIX Issue 8, the Hadoop 3.5.0 FileSystem specification and the HADOOP-13501/13502 JIRA records, the Python `io` docs and CPython source, Go's `io` and `errors` source, AIP-193/194, the WebAssembly 3.0 profiles appendix, OGC 17-069r4, the JDBC javadoc, the AWS S3 User Guide, fsspec and Arrow source, the OpenDAL RFCs and sqlite.org/testing.

**Hosts that still failed:**
- 403: dl.acm.org, cacm.acm.org, queue.acm.org, nowpublishers.com, apps.dtic.mil, researchgate.net, sciencedirect.com, eweek.com and jamasoftware.com.
- Bot challenges: IEEE Xplore (for EARS RE'09) and dblp.org.
- procon.bg returned 503.
- TLS chain errors: cs.ucf.edu (Larch FAQ, JML RM ch. 9) and cis.upenn.edu (Hughes et al.).
- event-b.org has a self-signed certificate.
- Connection resets: web.archive.org and repository.tudelft.nl.
- www.microsoft.com refused some research PDFs (other MSR pages were reached).
- OpenReview served abstracts only.

The verification log lists every failure.

**Markers used in this edition:**
- **(†)** marks an item that remains unverified background. It is kept only where verification did not remove it.
- **[unreachable]** marks a claim whose cited full text could not be fetched. The claim is kept with a hedge, or supported from an alternate source that is named.
- **[not re-checked]** marks an A/B claim outside the five tracks' scope. Such claims still rest on the earlier search extracts: Cirstea et al., TraceLink, PObserve, Porcupine, arXiv 2608.17388, FoundationDB, McKeeman, Jepsen MongoDB, WebKit, Eaton, arXiv 2409.14301 and AUTOSAR's "optionally".
- *Inference* marks this report's own reasoning, not a finding of any source.

Grades follow the brief: A = peer-reviewed or measured, B = documented industrial practice with data, C = practitioner report without data, D = opinion or marketing. Normative standards and official API docs are also graded B: they are authoritative about what they specify, not evidence that a method works. "A-pre" marks an arXiv preprint that has not been peer-reviewed, and "A-workshop" a lightly reviewed workshop paper.

---

## 1. Kernsatz

Write the boundary as **one assume–guarantee contract in the Design-by-Contract lineage**. It has five parts:
- an abstract model of observable state;
- per-call normal and exceptional cases;
- a typestate for each handed-out resource;
- one environment clause naming the observers and everything the outside world may do;
- history predicates, over operations with an interval, for what several observers see.

Its variation points carry bounded value sets that per-reality profiles may only narrow.

**Choose each spec's checkable form by what its claim quantifies over**, and work every clause out the way the axioms were: a decision, a counterexample trace, witness implementations, a named check and non-goals. The mapping from quantifier to form is:
- a finite case split → table;
- a value domain → executable oracle with property tests;
- call sequences on one resource → state-transition table with stateful model-based tests;
- interleavings of observers and environment → history predicate with a history checker or model checker.

**Make every check executable, independent of the implementation and frozen against the implementer.** That is the one point on which measured agent evidence is clear. No controlled study compares written formats for coding agents, and the few single-shot LLM comparisons find that notation alone does not beat prose.

---

## 2. Categories, levels and forms: eight categories, four binding axes, one quantifier rule

### 2.1 The categories and their levels

No established taxonomy matches the categories the brief proposes. The literature draws its lines along two axes.

**What is described: the environment, the interface or the design.**
- The four-variable model with REQ/NAT/IN/OUT and monitored and controlled variables is Parnas & Madey (Sci. Comput. Program. 25, 1995) [unreachable]. The earlier edition linked it to a McMaster record that turned out to be a 2010 Parnas-only chapter ([McMaster record](https://experts.mcmaster.ca/scholarly-works/2169098), A).
- Secondary support: NASA says the A-7 model "differentiates inputs, outputs, and state values by explicitly identifying monitored, control, and state variables" ([NASA-GB-001-97](https://ntrs.nasa.gov/api/citations/19980227975/downloads/19980227975.pdf), B/C).
- Zave insists that "when it comes to requirements, the environment is … the *only* thing" ([Zave FRE page](https://pamelazave.com/fre.html), author's summary page; the A grade belongs to the TOSEM paper, which was not read).

**State and time: a static structure, a single two-state transition, or behaviour over traces.**
- This split runs through Larch's two tiers: "one [language] that is designed for a specific programming language and another that is independent of any programming language" ([SRC RR-58](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf), B, the official language report).
- It also runs through TLA+ open specifications.
- Event-B refinement probably follows the same split (†, event-b.org unreachable).

*Inference:* the categories below are derived from those two axes. They add one thing the literature implies but does not name as a category: the **environment model** as its own unit. Three method families put the environment in one place, explicitly:
- Assume–guarantee contracts: "The specification is simply E implies M, where E specifies what we assume of the environment" ([Abadi & Lamport, Composing Specifications](https://www.microsoft.com/en-us/research/publication/composing-specifications/), A).
- I/O automata are "input-enabled … an automaton cannot block its inputs" ([Lynch retrospective](https://arxiv.org/pdf/2502.20468), A-pre).
- P closes systems with environment "ghost machines which are used only during verification" ([Desai et al., PLDI 2013](https://ankushdesai.github.io/assets/papers/p.pdf), A).

*Inference:* error classification and profiles look less like categories of behaviour and more like cross-cutting dimensions; none of the taxonomies above lists either as a category of its own. They are kept as categories here because each needs exactly one home (P2).

A spec's **level** is fixed by how far it is bound on four axes: observers, time, environment and reality. The governing principle (*Inference*, from P1 and Larch's tiering) is that **a spec binds to the least it needs, and binds to reality only through named variation points**.

| Category | What a unit states | Time | Observers | Environment | Reality | Established precedent |
|---|---|---|---|---|---|---|
| **K1 Structure** | What the API addresses (the existing axioms) | one instant | none | none | none | Larch shared tier ([RR-58](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf), B); ASM/Event-B state space (†) |
| **K2 Value function** | A pure map from input values to output values (e.g. a derived value of a key) | none | none | none | none, or a named variation point | Larch LSL theories; Darlington tables with PVS-generated disjointness and completeness obligations ([Lawford, Froebel & Moum](https://www.cas.mcmaster.ca/~lawford/papers/tables.pdf), B; the cited Lawford & Wassyng paper [unreachable]) |
| **K3 Single call** | Pre-state → post-state or signalled error, over an abstract model; frame | two states | O1 | frame only: "nothing else observable changes" | named variation points | JML `normal_behavior`/`exceptional_behavior`, `signals_only` ([JML Reference Manual, 2nd ed. draft](https://www.openjml.org/documentation/JML_Reference_Manual.pdf), B); VDM `errs` ([VDM-10 LangMan](https://raw.githubusercontent.com/overturetool/documentation/master/documentation/VDM10LangMan/VDM10_lang_man.pdf), B); Larch interface tier |
| **K4 Resource life** | States of a handed-out object, legal operations per state, transitions on error and close | sequence on one object | O1 | environment actions may interleave between steps (referenced from K5, never restated) | named variation points | Typestate ([Strom & Yemini, IBM record](https://research.ibm.com/publications/typestate-a-programming-language-concept-for-enhancing-software-reliability), A); UML protocol state machines as a "client-side view" ([OMG UML14-209](https://issues.omg.org/issues/UML14-209), C) |
| **K5 Environment model** | The named observers (O1 caller, O2 concurrent caller, O3 out-of-band store actor) and every action each may take, including fault actions | action alphabet | all, declared | *is* the environment | which fault actions are possible may be a variation point | A/G "E" ([Abadi & Lamport](https://www.microsoft.com/en-us/research/publication/composing-specifications/), A); rely condition ([Jones 1983](https://ilyasergey.net/CS6213/_static/05-owicki/rg.pdf), A); P ghost machines; Jepsen nemesis ([Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md), C) |
| **K6 Multi-observer guarantee** | Predicates over histories of client-observed interval operations: what O1 may see given what O2/O3 did | history | O1–O3 | full | value taken from a published partial order of consistency predicates | Linearizability ([Herlihy & Wing](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf), A); regular and atomic registers ([Lamport 1986](https://lamport.azurewebsites.net/pubs/interprocess.pdf), A); session guarantees ([Terry et al.](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf), A); client-centric isolation ([Crooks et al.](https://par.nsf.gov/servlets/purl/10077635), A) |
| **K7 Error classification** | A closed or extensible set of error categories defined by the caller's recovery action, and which categories each (operation, state) may signal | none | O1 | none | mechanism-to-category mapping lives in the profile | Spec# client / admissible / program-error failures ([Barnett, Leino, Schulte](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/TheSpecSharpProgrammingSystem28CASSIS200429.pdf), A); gRPC codes ([gRPC guide](https://grpc.io/docs/guides/status-codes/), B); PEP 3151 ([PEP](https://peps.python.org/pep-3151/), B); Rust `ErrorKind` ([docs](https://doc.rust-lang.org/nightly/std/io/enum.ErrorKind.html), B) |
| **K8 Profile** | One value per variation point, per reality | none | none | none | binds reality completely and states nothing else | POSIX option constants ([unistd.h, Issue 8](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/unistd.h.html), B); W3C variability ([W3C Note](https://www.w3.org/TR/2005/NOTE-spec-variability-20050831/), B); Hadoop contract XML ([testing.html](https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/filesystem/testing.html), B); WebAssembly 3.0 profiles ([appendix](https://webassembly.github.io/spec/core/appendix/profiles.html), B) |

**A cross-cutting vocabulary of non-commitment** serves § 3.2 ("unspecified is a statement"). Standards separate four strengths:
- **unspecified**: one of a stated set, with no further requirement on which is chosen ("two or more possibilities and imposes no further requirements on which is chosen in any instance");
- **implementation-defined**, called **profile-declared** here: "unspecified behavior where each implementation documents how the choice is made";
- **undefined**: "no requirements";
- **optional (MAY)**: "truly optional", and an implementation without the option "MUST be prepared to interoperate".

The first three come from ISO C ([N1570 §§ 3.4.1, 3.4.3, 3.4.4](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), B). WG23 N0245, cited in the earlier edition, only paraphrases them and drops the documentation duty. MAY comes from [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.txt) (B). JML adds a fifth, explicit marker, `\not_specified`, for clauses deliberately left open ([JML RM 2nd ed. draft](https://www.openjml.org/documentation/JML_Reference_Manual.pdf), B).

Two further values are needed at the boundary.

**Indeterminate**: the operation may or may not have taken effect. This is Jepsen's `:info`, "if we're not sure"; Jepsen "will interpret the exception as an indeterminate `:info` result" ([Jepsen tutorial](https://raw.githubusercontent.com/jepsen-io/jepsen/main/doc/tutorial/03-client.md), C). C11's "indeterminate value" means something different and should not be confused with it.

**Deliberately not promised**: latency, request count, memory and buffering, which are observable but outside the contract. PEP 3116's "raw reads may return a short read without any particular reason" is a clean precedent, but it applies to the raw layer only ([PEP 3116](https://peps.python.org/pep-3116/), B). The current docs widen it to the buffered base class: "Less than size bytes being returned does not imply that EOF is imminent" ([Python io docs](https://docs.python.org/3/library/io.html), B). POSIX `read()` states its non-promise as an enumerated set of allowed short-read causes ([read(), Issue 8](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html), B). Hadoop states what a stream may show under change: "these changes MAY or MAY NOT be visible. Such changes that are visible MAY be partially visible" ([fsdatainputstream.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/fsdatainputstream.html), B).

*Inference:* "undefined" is almost always wrong at a black-box boundary, because no check can be written against it (P4, P5). CPython prefers a defined error for use-after-close: `ValueError`, "I/O operation on closed file." ([CPython iobase.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/39f6a0489fcc815a578d27dfee2feea003c896f8/Modules/_io/iobase.c), B). B's precondition-as-abort is the "undefined" strength in a formal method ([Atelier B manual](https://www.atelierb.eu/wp-content/uploads/2023/10/b-language-reference-manual.pdf), B).

### 2.2 The category × form matrix

Each cell gives the fit (++ strong, + workable, − poor), **what the form makes checkable** for that category, and **its main cost**. The cells are *Inference* from the cited cases unless a source is named.

The industrial anchors, all verified against full texts, are:
- **ShardStore** ([Bornholt et al., SOSP 2021](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf), A). It prevented 16 issues: 5 functional, 5 crash-consistency and 6 concurrency. Reference models plus validation harnesses are **12–13 % of the code base, ≈ 20 % of the implementation**. The reference models alone are 450 lines, ≈ 1 % of the implementation.
- **Cedar** ([Disselkoen et al., FSE Companion 2024](https://arxiv.org/pdf/2407.01688), A). Proof found 4 bugs, and differential and property testing found 21. The Lean models are "an order of magnitude smaller" than the Rust code, and proofs run at 3.4 : 1 to the model.
- **AWS TLA+** ([Newcombe et al., 2014 draft of CACM 58(4)](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf), B). Used on 10 systems; 2–3 weeks to learn. A DynamoDB bug needed a 35-step trace. The CACM print text was [unreachable].
- **AUTOSAR QuickCheck** ([Chalmers record](https://research.chalmers.se/en/publication/219899), A/B). More than 3,000 pages modelled and more than 200 issues found. Only the abstract was read, and the counts are self-reported.
- **SCR and Darlington tables.** The mechanism is confirmed from Heitmeyer's own slides ([Marktoberdorf 2010](https://asimod.in.tum.de/2010/slides/heitmeyer/Heitmeyer2-Markt2010.pdf), C) and from [Lawford, Froebel & Moum](https://www.cas.mcmaster.ca/~lawford/papers/tables.pdf) (B). The cited Heitmeyer & Labaw NRL report is [unreachable].

| Category ↓ / Form → | Structured prose (IDs, RFC 2119, templates) | Table (case, state-transition, capability) | Schema-validated data | Executable reference model (+ differential) | PBT / stateful model-based tests (+ history checker) | Model-checked formal (TLA+, P, Alloy, Quint) | Proof (Dafny, Lean, Isabelle) |
|---|---|---|---|---|---|---|---|
| K1 Structure | + review only; cheap | − | + shape only, not cross-constraints | + generator of valid structures | + invariants on generated trees | ++ bounded consistency and counterexample search; Alloy 6 adds traces ([Alloy 6](https://alloytools.org/alloy6.html), C) | + meta-theorems; high cost |
| K2 Value function | + nothing checked | ++ completeness and disjointness of case split (SCR, Darlington); cheap to check, costly to retrofit | − | ++ agreement on millions of inputs (Cedar DRT); cost of a second implementation; only as good as its generators | ++ general laws, round-trips ([Goldstein et al.](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf), A); generators "can be nontrivial to write" | + | + if a soundness property matters (Cedar: proof found a bug DRT missed) |
| K3 Single call | + POSIX "shall fail / may fail" ERRORS idiom ([XSH 2.3](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html), B); unchecked | ++ precondition × outcome partition, mechanically complete and disjoint; the same check exists without a table in ACSL `complete behaviors` / `disjoint behaviors` ([ACSL](https://frama-c.com/download/acsl.pdf), B) | + parameter/result shape | ++ single-call oracle; returning *sets* of allowed outcomes is inference (ShardStore relaxed equivalence instead) | ++ random calls against the model; shrinking | + | + deductive verification; costly |
| K4 Resource life | + EARS state/event templates; ambiguity remains | ++ state × operation table: every cell must be filled, which forces use-after-close and after-failure decisions | − | ++ per-component model state; faults injected as operations (ShardStore `FailDiskOnce`) | ++ stateful sequences (AUTOSAR, ShardStore); generator effort; argument bias risks "baking our assumptions into" the tests | + safety of call protocols | − cost high |
| K5 Environment model | + an action list in one place; unchecked | ++ action × precondition table; completeness checkable | + machine-readable action list that test harnesses import | ++ the environment becomes nondeterministic actions in the model | ++ fault shims or nemesis drive the actions (Jepsen; ShardStore `DirtyReboot`; FoundationDB [not re-checked]) | ++ environment as explicit actions; interleavings explored | − |
| K6 Multi-observer guarantee | − ambiguity hot spot (Cosmos DB behaviours "poorly understood … even informally", [Hackett et al.](https://arxiv.org/pdf/2210.13661), A/B) | − state explosion | − | + sequential model as the reference for linearizability checking | ++ recorded histories of interval operations checked by Porcupine/Knossos/Elle; NP-complete in general, Elle linear-time for Adya anomalies ([Elle](https://arxiv.org/pdf/2003.10554), A) | ++ design-level interleavings and failure scenarios (AWS, value in all 10 systems); not against code unless trace validation is added | − cost high |
| K7 Error classification | + "shall fail / may fail" | ++ (operation, state) × category table; completeness checkable | ++ enumerations; closed-set check | + model signals categories | + oracle asserts the category, not merely "raised" | − | − |
| K8 Profile | + "implementation-defined" points (POSIX) | ++ capability / variance table | ++ typed profile record; permitted combinations checkable | + model parameterised by profile (inference; neither ShardStore nor Cedar does this) | ++ one suite × every profile (Hadoop, OpenDAL) | + profile as model constants | − |

Read down the columns and a pattern appears that the standards confirm. In WebAssembly, Cedar, ShardStore and SQLite, the normative artefact varies (prose, pseudo-code or a formal model), but **the checkable artefact is always executable**: a reference interpreter or model plus generated or shared tests ([Watt, CPP 2018](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf), A). SQLite keeps "590 times as much test code and test scripts" as library code (as of 3.42.0), including a differential SQL Logic Test against four other engines ([sqlite.org/testing](https://sqlite.org/testing.html), B). Mechanised semantics paid off mainly for *meta-properties* such as type soundness, and they found real errors in prose specs that "were acknowledged" ([Watt](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf); [WasmCert-Coq](https://spiral.imperial.ac.uk/entities/publication/ecf384fa-0800-4dc3-b5ef-a5aac822610e), A). Per-call behaviour was checked more cheaply by differential testing.

### 2.3 The rule (§ 5.2 d): category → level → form

*Inference, synthesised.* No validated rule exists at this granularity. The rule refines published coarse heuristics:
- state-based and functional specifications "are thus better targeted at transactional systems"; history-based and transition-based ones at "reactive systems", and "there is no point in looking for a universal specification technique" ([van Lamsweerde 2000](https://homepage.cs.uiowa.edu/~tinelli/classes/5810/Fall20/Papers/vLam00.pdf), A);
- "the type of analysis … determine[s] the most appropriate level of formalization" ([NASA-GB-002-95](https://www.fing.edu.uy/inco/grupos/mf/TPPSF/Bibliografia/fmguide1.pdf), B/C); choose the representation by its "explicit (implicit) representation of state and time" ([NASA-GB-001-97](https://ntrs.nasa.gov/api/citations/19980227975/downloads/19980227975.pdf), B/C);
- languages differ by semantic domain, and an advocate should state "the method's domain of applicability" ([Wing 1990](https://www.cs.cmu.edu/~wing/publications/Wing90a.pdf), A).

None of these is validated by outcome data. The rule is also consistent with three other sources: Larch's tiering; van Lamsweerde's call for multiple paradigms "linked through consistency rules"; and ShardStore's stated approach, which "decomposes correctness into independent properties, each checked by the most appropriate tool, and develops executable reference models as specifications to be checked against the implementation" ([ShardStore](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf), A).

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
   | finite case split | table, checked for completeness and disjointness (the check can also be stated in a contract language, as in ACSL `complete behaviors` / `disjoint behaviors`) |
   | value domain | executable oracle plus property tests |
   | call sequences on one resource | state-transition table plus stateful model-based tests |
   | interleavings of observers and environment | history predicate over interval operations plus history checker, and a model checker if the claim is about a protocol design |
   | a universal meta-property | proof |
   | the space of profiles | typed schema plus one suite parameterised by it; the unit declares whether the profile is a static record or also probed at runtime, and a probe's "false" may mean "unknown" |

4. **Check: every unit names its check, or states that it cannot be checked and why** (P4). Unbounded eventual visibility is a claim no finite history can refute. In Burckhardt, all but finitely many operations that start after e has returned "must see e", and liveness is the property for which "any finite execution can be extended to an execution that satisfies the property" ([Burckhardt, Principles of Eventual Consistency, MSR copy](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/final-printversion-10-5-14.pdf), A). Calling it the "standard example" is inference.

5. **Foundation work: every unit gets a counterexample, a decision record, witnesses and non-goals** (§ 2.4).

### 2.4 How the axiom method (Appendix A) transfers to behaviour

The axiom research gives four instruments. Each has a direct behavioural counterpart (*Inference* throughout, though every counterpart has a published precedent).

**A counterexample per clause becomes a counterexample *history* per clause.** For each clause, give a trace of boundary events that satisfies every other clause and violates only this one, and say what goes wrong. The events are calls, returns, signals, and environment actions by O2 or O3.

A trace is the natural object here. ioco judges conformance on traces: out(i after σ) ⊆ out(s after σ) for every suspension trace σ of the spec, including the observable absence of output δ ([Tretmans 2008](https://repository.ubn.ru.nl/bitstream/handle/2066/72680/72680.pdf), A). Consistency frameworks judge predicates over histories whose operations carry start and return times ([Viotti & Vukolić](https://arxiv.org/pdf/1512.00168), A).

Each counterexample history becomes executable in two ways:
- as a **mutant reference model** that breaks exactly that clause. The clause's check must kill it. This mirrors AugmenTest's rule that an assertion which "passes on the original class but fails on the buggy" one is correct ([arXiv 2501.17461](https://arxiv.org/html/2501.17461v1), A-pre).
- as a **fixed regression history** fed to the history checker.

This is the strongest available guard against vacuous clauses. Abadi and Lamport interpret a guarantee under an assumption as "M holds at least one step longer than E does". Under that reading, "the guarantee M can become false only after the assumption E becomes false", which rules out behaviours that a later environment violation would otherwise excuse ([Conjoining Specifications](https://lamport.azurewebsites.net/pubs/abadi-conjoining.pdf), A).

**Witness models become witness realities.** The axioms show consistency with W0–W2. A behavioural contract shows consistency, and that it admits every intended reality, by naming at least two executable witnesses that satisfy all clauses with *different* profile values. An example pair is a trivial in-memory model with eager errors and a lazy-open model.

Hadoop shows why both are needed:
- `open()` "MUST check for the presence of the file at the time of creation", which "does not imply that the file and its data is still at the time of the following read()" ([filesystem.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html), B).
- The later `openFile()` "MAY implement a lazy open where file non-existence or access permission failures may not surface until the first read()". File-specific preconditions "MUST NOT be checked here" ([openfile.html](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/filesystem/openfile.html), B).

A contract that admits only one of these two witnesses has silently decided the running example. *Inference:* Hadoop puts the wider freedom on a separate entry point rather than in a per-backend profile of `open()`.

**Decisions taken become a decision record per clause.** The format is the same as A.6: chosen, alternative, and what the alternative would change. For the running example the rows would cover:
- error timing;
- what a stream yields under a concurrent writer;
- the state after a mid-read failure;
- close idempotence: Java's `Closeable` versus `AutoCloseable`, whose close "is not required to be idempotent", is a published pair of alternatives ([AutoCloseable](https://cs-214.epfl.ch/jdk-21.0.9-docs/api/java.base/java/lang/AutoCloseable.html), B);
- use-after-close: static error, defined error, or best-effort, where fail-fast detection works "on a best-effort basis" ([CME Javadoc](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html), B).

Z gives a decades-old wording pattern for one such decision. An error schema with ΞState specifies "that if the error occurs, the state of the system should not change", and the robust operation is a disjunction of the normal and error cases ([Spivey ZRM](https://spivey.oriel.ox.ac.uk/wiki/files/zrm/zrm.pdf), A/B). It is an available form, not a semantic recommendation.

**Lemmas become derived properties and metamorphic relations.** These are consequences the contract should imply, such as "reading in chunks of k yields the same bytes as reading all at once when no environment action occurs". They are checkable "in the absence of test oracles". The original metamorphic-testing report says so ([Chen, Cheung & Yiu, arXiv 2002.12543](https://arxiv.org/abs/2002.12543), 1998 technical report; the cited HKU record [unreachable]).

**Non-goals stay a list.** Examples: performance figures, internal layers, and the mechanism of buffering. P1 and the brief's own scope put these outside the boundary.

The axiom notation does not transfer, and the brief says it should not. A structure spec quantifies over one instant. Every behavioural category from K3 on quantifies over two states, sequences or histories, so its counterexamples are traces, not structures.

---

## 3. Method survey: eight families, none sufficient alone

### 3.1 Contract languages: DbC, JML, Dafny, Larch, ACSL, Spec#

**What they state.** A call is a two-state relation over an abstract model.
- **Meyer** set out to "reduce bugs by building software components on the basis of carefully designed contracts" ([Meyer 1992](https://www.kth.se/social/files/59526bfb56be5b4f17000807/meyer-92-contracts.pdf), A, conceptual: a magazine article without data). In Eiffel, a routine whose rescue clause exits without retry "fails", "causing an exception in its caller" ([Eiffel docs](https://www.eiffel.org/doc/solutions/Exception_Mechanism), B).
- **JML** adds the black-box machinery. The design report is [Leavens, Baker, Ruby, TR 98-06j](https://dr.lib.iastate.edu/cs_techreports/136) (B, a tech report). It provides model fields, `normal_behavior` and `exceptional_behavior` cases, `signals_only` and `assignable` frames ([JML RM 2nd ed. draft](https://www.openjml.org/documentation/JML_Reference_Manual.pdf), B).
  - The default `signals_only` is the method's throws clause "plus java.lang.RuntimeException".
  - The frame default **differs between JML versions**. In TR 98-06j an omitted modifiable clause means "nothing can be modified". In the 2nd-edition draft the default specification "includes assignable \everything".
- **Dafny** adds `modifies`/`reads`, `old()`, `unchanged()` and `fresh()` ([Dafny cheatsheet](https://dafny.org/v4.3.0/DafnyCheatsheet.pdf), C).
- **Larch** pairs a language-independent shared tier with per-language interface languages that deal "with what can be observed about the behavior of components", including exception handling ([SRC RR-58](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf), B). The Larch FAQ could not be fetched [unreachable].
- **ACSL**, for C without exceptions, writes errors as named behaviors over return values. `complete behaviors` and `disjoint behaviors` clauses make completeness and disjointness of the case split explicit and checkable. "Since C has no exceptions, ACSL does not use exceptional specifications" ([ACSL manual](https://frama-c.com/download/acsl.pdf), B).
- **Spec#** classifies failures by fault and recovery. Client failures violate the precondition. Admissible failures are "part of the contract between callers and implementations" and are signalled with checked exceptions. `throws E ensures P` gives exceptional postconditions ([Barnett, Leino, Schulte, CASSIS 2004](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/TheSpecSharpProgrammingSystem28CASSIS200429.pdf), A).
- **.NET Code Contracts** offers `EnsuresOnThrow<T>` and is not supported in .NET 5+ ([docs](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.contracts.contract.ensuresonthrow), B).

**Limits.** None of them can say "the call returned, and the failure surfaces later through another object" except as state of the returned resource. ACSL, Spec# and Code Contracts confirm this limit. There is no environment and no second observer unless they are modelled by hand.

There is also a cost signal from practice. A measured study of 21 contract-equipped projects (260 MLOC) found that the contracts written are overwhelmingly null checks. Quantifiers are "practically never" used in pre- or postconditions. Specifications are "quite stable compared to implementations" ([Estler et al., FM 2014](https://arxiv.org/pdf/1211.4775), A). *Inference:* the rich features K3 relies on are rarely written in practice.

**Fit.** On § 3:
- observers: O1 only;
- unspecified: loose postconditions express it;
- parameterisation: via behavioural subtyping (§ 4).

On § 4: strong on P1, P2 and P5 (model fields and one case per unit), and partial on P4 (runtime assertion checking at call return only).

**Grade:** A for the method papers and Estler et al., B for the manuals. No measured study of these methods on multi-backend library specs was found.

### 3.2 Model-oriented specification and refinement: VDM, Z, B, Event-B, ASM

This family is now verified from primary manuals for VDM, Z and B. Each gives one error idiom:
- **VDM-SL** has a dedicated `errs` clause. "The specification using exceptions does not give any commitment as to how exceptions are to be signalled". Each error condition acts as a precondition with its own postcondition, and `ext rd/wr` frames list readable and writable state ([VDM-10 Language Manual](https://raw.githubusercontent.com/overturetool/documentation/master/documentation/VDM10LangMan/VDM10_lang_man.pdf), B).
- **Z** combines the normal operation with error schemas through schema disjunction. Each error schema reports a value and leaves the state unchanged (Ξ), so the robust operation "must terminate whatever its input" ([Spivey ZRM](https://spivey.oriel.ox.ac.uk/wiki/files/zrm/zrm.pdf), A/B).
- **B** treats a precondition as a caller obligation: "If the precondition is not proved, then the substitution does not end". It has nondeterministic `CHOICE` and `ANY` ([Atelier B B Language Reference Manual](https://www.atelierb.eu/wp-content/uploads/2023/10/b-language-reference-manual.pdf), B).

Event-B refinement proof obligations and Börger's ASM "ground model" remain background (†): event-b.org failed TLS and no open Börger copy was found.

*Inference:* VDM's refusal to commit to a signalling mechanism is a published precedent for separating K7 (error category) from the profile-level mapping from mechanism to category. The value of the family for this project is that the *level* is the refinement step at which a property first becomes expressible.

**Grade:** B for VDM, Z and B (official manuals; the Spivey reference manual is a standard text); † for Event-B and ASM. It supplies precedents but should not decide the bake-off.

### 3.3 Lifecycle and protocol methods: typestate, protocol state machines, session types, interface automata

**What they state.** The legal operations per state of a handed-out object, and the transitions between states.
- **Typestate** detects "at compile-time syntactically legal but semantically undefined execution sequences", such as dereferencing a pointer after deallocation ([Strom & Yemini, IBM record](https://research.ibm.com/publications/typestate-a-programming-language-concept-for-enhancing-software-reliability), A).
- **DeLine and Fähndrich** made it modular for objects. They handle aliasing "by adapting our previous work on practical linear types", and they allow subclasses "to extend the interpretation of typestates" ([MSR](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/), A).
- **UML protocol state machines** are "a client-side view, independent of the internal behavior machine". Protocol states "are not necessarily the same as the internal states" ([OMG UML14-209](https://issues.omg.org/issues/UML14-209), C: an issue-tracker entry, not the specification). The per-transition anatomy of guard, trigger and postcondition is not stated in that issue. What is verified is that a generated class contract "defines a pre- and post-condition for each operation that triggers a transition" ([Porres & Rauf](https://research.ucc.ie/en/publications/generating-class-contracts-from-deterministic-uml-protocol-statem/), A).
- **Session types** are "type-theoretic specifications of communication protocols" ([ETAPS Test-of-Time](https://www.etaps.org/2019/test-of-time-award); award page about an A paper).
- **Interface automata** pair input assumptions with output guarantees. "One interface refines another if it has weaker input assumptions, and stronger output guarantees" ([de Alfaro & Henzinger](https://research-explorer.ista.ac.at/record/4622), A).

**Limits.** These methods are mostly about safety, meaning allowed sequences. In interface automata "an output in a specification can always be ignored in an implementation", so a component that never outputs "satisfies any interface". Modal and IOMTS interface theories, which "distinguish between may- and must-transitions", can express mandatory outputs ([Lüttgen & Vogler, LMCS 2013](https://arxiv.org/pdf/1306.3050v2), A). *Inference:* "read eventually returns or fails" still needs a liveness or fairness clause on top. Data content is stated weakly.

**Fit.** This is the natural home for "failure after return" and "resource outlives the call" (K4). Industrial close contracts show the hazards a K4 spec must decide explicitly:
- **POSIX `close`.** An interrupted `close` "shall return -1 with errno set to [EINTR] and the state of fildes is unspecified" ([close(3p)](https://man.archlinux.org/man/close.3p.en), B). A NetBSD bug report found that on the five systems its author checked (NetBSD, FreeBSD, OpenBSD, Linux, illumos), "the descriptor is closed, unconditionally" ([NetBSD PR 58929](https://gnats.netbsd.org/58929), C). POSIX.1-2024 has since added `posix_close()`.
- **Rust.** `async_fs::File` documents that "any errors detected on closing are ignored" ([async_fs](https://docs.rs/async-fs/1.1.2/async_fs/struct.File.html), B). A reader comment on LWN says the same of `std::fs::File` ([LWN comment](https://lwn.net/Articles/1009302), C).

**Grade:** A for theory, B for API practice, C for issue trackers.

### 3.4 Environment and concurrency contracts: rely–guarantee, assume–guarantee, linearizability, I/O automata, CSP, TLA+, P

**What they state.** They add the environment to the contract.
- **Rely–guarantee.** "Any state changes made by other processes can be assumed to satisfy the rely-condition". The guarantee bounds what other processes observe of this one. If the rely is violated "there is no specified constraint". "It is quite legitimate to use a program with a weaker rely-condition or a stronger guarantee-condition" ([Jones 1983, TOPLAS](https://ilyasergey.net/CS6213/_static/05-owicki/rg.pdf), A).
- **Assume–guarantee** writes the open specification E ⇒ M, strengthened to E −+▷ M, "M holds at least one step longer than E does" ([Abadi & Lamport 1995](https://lamport.azurewebsites.net/pubs/abadi-conjoining.pdf), A).
  - Benveniste and co-authors define refinement as "M_C′ ⊆ M_C and E_C′ ⊇ E_C", with composition and conjunction of viewpoints ([INRIA RR-8147](https://inria.hal.science/hal-00757488/document), A/B). The monograph [Contracts for System Design](https://nowpublishers.com/article/Details/EDA-053) itself was [unreachable].
  - A review calls the monograph "a dense mathematical treatment" and "not a book for practitioners looking for a … tutorial" ([FME review](https://fmeurope.org/2020/10/30/book-review-contracts-for-system-design/), C).
- **Linearizability** keeps a *sequential* specification of record: "each operation … takes effect instantaneously at some point between its invocation and its response" ([Herlihy & Wing](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf), A). *Inference:* that is a template for "one sequential contract, a declared consistency condition per reality".
- **I/O automata, CSP, TLA+ and P** all make the environment explicit inside the spec, but in different ways:
  - Only I/O automata are input-enabled: any input "may occur from any automaton state". Lynch contrasts this with process algebras, where actions "are not classified as input vs. output" ([Lynch retrospective](https://arxiv.org/pdf/2502.20468), A-pre).
  - TLA+ writes environment steps as a disjunct `EnvNext` of `Next` ([Specifying Systems § 4](https://lamport.azurewebsites.net/tla/book-02-08-08.pdf), A).
  - P models the environment "as nondeterministic ghost machines" ([P, PLDI 2013](https://ankushdesai.github.io/assets/papers/p.pdf), A).
  - Crash as an action of the alphabet is attested in testing practice: ShardStore generates `DirtyReboot` and `FailDiskOnce` operations. It is not stated in the texts the earlier edition cited.

**Limits.**
- **Operations with an extent exist; a ready-made chunked-stream type does not.** The earlier edition said no framework treats a long-lived stream as an operation with an extent. That is refuted:
  - Every history model read gives operations an invocation–response interval.
  - Interval-linearizability "allows to associate states along the interval of execution of an operation" ([Castañeda, Rajsbaum, Raynal, arXiv 1507.00073](https://arxiv.org/pdf/1507.00073), A-pre as read).
  - Lamport's registers define what a read overlapping a write may return: a regular register's read "obtains either the old or new value" ([Lamport 1986](https://lamport.azurewebsites.net/pubs/interprocess.pdf), A).
  - Hadoop and S3 state the stream case in prose (§ 4).

  What remains is a modelling decision the project must still make: one interval operation with one output (snapshot, or old-or-new), or per-chunk operations with a cross-chunk predicate. No framework ships an object type for a read that yields a sequence of partial outputs. Interval-sequential specifications are "challenging to correctly generate or understand, even for simple operations on a single concurrent register" ([substep linearizability, arXiv 2610.16099](https://arxiv.org/pdf/2610.16099), A-pre).
- **The out-of-band observer.** Rely–guarantee and TLA+ do not treat interference as a session. They treat it as environment state change, so an actor that bypasses the API is native there. Jepsen's nemesis is "a special client, not bound to any particular node" ([Jepsen tutorial ch. 5](https://raw.githubusercontent.com/jepsen-io/jepsen/main/doc/tutorial/05-nemesis.md), C). What survives is narrower: **no source distinguishes O2 (a concurrent API caller) from O3 (an out-of-band mutator) as two kinds of observer with different rights**.
- **Authoring cost is real.** Lamport writes that one "almost always" writes closed-system specifications and that "there's seldom any reason" to turn them into open ones ([Specifying Systems § 10.7](https://lamport.azurewebsites.net/tla/book-02-08-08.pdf), A). The AWS remark that "many engineers struggled to become productive with TLA+", which motivated P, could not be checked ([CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services), B, [unreachable]).

**Fit.** This is the only family that meets § 3.1 (named observers plus an explicit environment) natively. Refinement serves § 3.3. P2 is very good because E is one home. P4 needs a model checker or tests.

The closest published analogue to this project is the Cosmos DB TLA+ spec ([Hackett et al., ICSE-SEIP 2023](https://arxiv.org/pdf/2210.13661), A/B):
- It specified *user-facing* behaviour.
- At 390 lines it is "significantly smaller and conceptually simpler than any other specification of Cosmos DB".
- It took 2 person-months.
- It raised "two key issues in Cosmos DB's public-facing documentation, which have since been addressed".
- It offered "a fundamental solution to a previous high-impact outage within another Azure service": an explanation and a proposed fix, not a repair.

**Grade:** A (theory), B (AWS practice).

### 3.5 Client-centric consistency frameworks: Adya, Burckhardt, Viotti–Vukolić, Crooks, session guarantees, Lamport registers

**What they state.** Guarantees as predicates over histories of client-observed events, with observers named as sessions.
- **Adya** gave "the first implementation-independent specifications of existing ANSI isolation levels", with phenomena G0 to G2 ([Adya thesis, MIT/LCS/TR-786](https://www.aphyr.com/data/posts/294/adya-phd.pdf), A).
- **Burckhardt** interprets histories through visibility and arbitration relations, as Viotti & Vukolić restate them: an abstract execution is "(H, vis, ar)". The axiom names remain (†).
- **Viotti and Vukolić** survey "more than 50" notions and give "a partial order among different consistency predicates, ordering them by their semantic 'strength'". The scope is "restricted to non-transactional semantics … single storage object operations" ([ACM CSUR 2016 / arXiv 1512.00168](https://arxiv.org/pdf/1512.00168), A).
- **Crooks et al.** treat storage as a black box that transitions "through a series of states, a subset of which are observed by applications". The "definitions make no reference to histories" ([PODC 2017](https://par.nsf.gov/servlets/purl/10077635), A).
- **Terry** defines four session guarantees. "Either the storage system ensures them … or else it informs the calling application that the guarantee cannot be met" ([Terry et al.](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf), A).

**Limits.** Operations are intervals: Viotti & Vukolić give each a start time and a return time, with Ω "if the operation does not return". But each operation has **one** output value, so a stream yielding partial outputs over its interval has to be mapped onto that model by a decision. Liveness axioms cannot be falsified by any finite history.

**Fit.** Best for K6 and for the *values* of K8 consistency axes. A profile picks a node in a published **partial order** instead of inventing prose. Because the order is partial (incomparable values exist; § 4), "narrower" is defined only between comparable values. P4 is met through history checkers. Knossos "often timed out or ran out of memory after a few hundred transactions", while Elle "was able to check histories of hundreds of thousands of transactions in tens of seconds" ([Elle, PVLDB 14(3)](https://arxiv.org/pdf/2003.10554), A).

**Grade:** A.

### 3.6 Requirements-boundary methods: four-variable model, Zave–Jackson, SCR tables, EARS

**What they state.**
- **The four-variable model** places requirements as relations over monitored and controlled quantities, with NAT as "constraints on the system env". The cited NRL overview is [unreachable] (apps.dtic.mil 403). The wording above comes from the author's slides ([Heitmeyer, Marktoberdorf 2010](https://asimod.in.tum.de/2010/slides/heitmeyer/Heitmeyer2-Markt2010.pdf), C).
- **SCR tables.** SCR consistency checking "checks spec for application-independent properties, including properties required of the tables", including disjointness and coverage (same slides).
  - The often-quoted line about reviewers who "spent too much of their time and effort checking for simple, application-independent properties" comes from [Heitmeyer & Labaw](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf), which is [unreachable].
  - The peer-reviewed SCR consistency-checking paper (TOSEM 1996) was not reached either.
- **Darlington** used "tabular notation in both the requirements and design documents". The SESM tools generate PVS input, PVS "automatically generate[s] Disjointness and Completeness" obligations, and "This change in focus was necessitated by regulatory requirements" ([Lawford, Froebel & Moum](https://www.cas.mcmaster.ca/~lawford/papers/tables.pdf), B; the cited Lawford & Wassyng paper is [unreachable]).
- **EARS** gives five sentence templates.
  - Its evaluation was a single aero-engine control case: "requirements from an airworthiness regulation document", with "qualitative and quantitative improvements" ([Manchester record](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/), A-weak). The RE'09 figures are [unreachable].
  - The originator's guide claims EARS "reduces or even eliminates common problems" without figures ([alistairmavin.com](https://alistairmavin.com/ears/), C).
  - Vendor claims of "drastic" improvement remain D ([Jama](https://www.jamasoftware.com/blog/webinar-recap-adopting-ears-notation-to-improve-requirements-engineering), [unreachable]).
  - The one controlled EARS experiment found had 10 subjects and no prose or table control arm ([Salari et al.](https://www.ipr.mdu.se/pdf_publications/6673.pdf), A-weak).

**Limits.** Tables are proven for mode and case splits, not for concurrency. EARS improves phrasing, not checkability. Its "If … then" template is the only built-in slot for error behaviour.

**Fit.** *Inference:* per-reality profiles map onto per-reality NAT, which supports treating a profile as a parameter of the environment assumption, not as a separate kind of spec.

**Grade:** A/B for tables. The mechanism is confirmed independently by Darlington/PVS and Heitmeyer's slides, but the peer-reviewed SCR texts are unreachable and the NRL reports are B/C. EARS is A-weak.

### 3.7 Conformance testing theory and model-based testing: ioco, Spec Explorer, TorXakis, stateful PBT

**What they state.** A black-box definition of "conforms" ([Tretmans 2008](https://repository.ubn.ru.nl/bitstream/handle/2066/72680/72680.pdf), A):
- After every suspension trace the spec allows, the implementation may produce only outputs the spec allows, and quiescence δ counts as an output.
- "An implementation may have additional features". After an underspecified trace "any behaviour is allowed after it". So unspecified *inputs* are free.
- Nondeterministic *outputs* are honoured as a set.

Caveat: ioco and uioco differ on traces that are underspecified only along some nondeterministic branches. arXiv 1403.7260, cited in the earlier edition, confirms δ and the test hypothesis but not the free-inputs rule ([Beohar & Mousavi](https://arxiv.org/pdf/1403.7260), A).

**Evidence of scale.**
- **Spec Explorer, Microsoft Windows protocols.** The peer-reviewed conclusion that MBT "works and scales, provided it is accompanied by sound tool support and clear methodological guidance" is [unreachable] ([Grieskamp et al. 2011](https://repositoriosdigitales.mincyt.gob.ar/vufind/Record/CONICETDig_c68bda0856b57e85543ae9443287fe53)). Grieskamp's own slides (C) report:
  - "250+ protocols in Windows alone (~ 30,000 pages of documentation)";
  - about 280 vendor and 50 Microsoft staff;
  - "Windows-specific behavior listed as separate requirements";
  - source: [SambaXP 2008 slides](https://sambaxp.org/archive_data/sxp08/SambaXP2008-DATA/00-05-Wolfgang_Grieskamp-MBT.pdf).

  The "250 person-years" press figure could not be fetched and is probably a conflation with the protocol count. It is dropped.
- **Stateful QuickCheck on Dropbox.** The result ([Hughes et al., ICST 2016](https://www.cis.upenn.edu/~bcpierce/papers/mysteriesofdropbox.pdf)) is [unreachable]. It was re-run with TorXakis ([arXiv 2102.00378](https://arxiv.org/pdf/2102.00378), citing Tretmans & van de Laar 2019).
- **TorXakis** is the reference ioco tool: BSD-3, written in Haskell, SMT-backed, with ioco "currently" the only implemented relation. It is still maintained, but no industrial data was found ([README](https://raw.githubusercontent.com/TorXakis/TorXakis/develop/README.md), C).

**Fit.** This is the theory behind § 5 and behind the distinction between "unspecified" and "nondeterministic".

**Grade:** A for the theory. Industrial-scale evidence currently stands at C, because the A-graded sources were unreachable.

### 3.8 Executable reference models and lightweight formal methods

**What they state.** The specification *is* a small executable implementation of the same interface. Correctness is decomposed into properties, each checked with the best-fit tool. All figures below come from the full ShardStore and Cedar papers.

**ShardStore** ([SOSP 2021](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf), A):
- **Results and size.** It prevented 16 issues. Its validation code is 12 % (introduction) or 13 % (§ 8.2) of the code base and 20 % of the implementation, against formal verification approaches that "report 3–10× overhead".
- **Who wrote it.** Two formal-methods experts spent nine months and a third spent three. The engineering team, "none of whom have any prior formal methods experience", has since taken most of the work over, and 18 % of harness lines were last edited by non-experts.
- **The models.**
  - Each is ≈ 450 lines of Rust in total, "small executable specifications (1% of the implementation code)".
  - Rust was chosen over Alloy, Promela and P to keep the models maintained by the team.
  - The models are reused as mocks, which forces engineers to keep them current.
- **How each property class is checked.**
  - Sequential crash-free behaviour: by equivalence under property-based tests.
  - Crash consistency: by generated `DirtyReboot` operations.
  - Concurrency: with Loom and Shuttle stateless model checking against separate linearizability models.
- **Failures.** They are injected as operations (`FailDiskOnce`). The models omit them on purpose: "we choose to omit other implementation failures (IO errors, resource exhaustion, etc.) from the models". After an injected failure the harness does **not** track sets of model states, because that "blows up quickly in the face of multiple failures". Instead, a "has failed" flag allows a Get to return no data, but "never … the wrong data".
- **Limits stated by the authors.** "We do not currently check properties of concurrent crashing executions." Also: "our validation checks can miss bugs".

**Cedar** ([FSE Companion 2024](https://arxiv.org/pdf/2407.01688), A):
- Proofs run over a Lean model; the code is tied to the model by differential random testing on "millions of inputs".
- Size: Lean models 1,673 LOC against 15,693 LOC of Rust production code; proofs 5,714 LOC, a 3.4 : 1 proof-to-model ratio; about 3 minutes to check all proofs.
- Bugs: proof found one non-termination and three soundness bugs in the validator. DRT and PBT found 21 bugs in the parser, evaluator, formatter and IP handling.
- DRT "did not discover the non-termination bug".
- One generator produced boolean literals in 35.5 % of its when-conditions until it was replaced.

**Limits.** The model is code, so mechanism can leak into it (P1 risk). ShardStore's authors note that argument bias "introduces the risk of baking our assumptions into" the tests. ShardStore's scope is a single node, not multiple external observers. Neither paper parameterises its model by deployment profile.

**Grade:** A.

### 3.9 Variation vocabularies in standards and storage APIs

C's behaviour terms, RFC 2119, POSIX options and "shall fail / may fail", W3C variability, OGC conformance classes, SQL isolation levels with SET TRANSACTION General Rule 5, JDBC metadata, WebAssembly 3.0 profiles, Hadoop, OpenDAL, Python `io`, PEP 3151, Go `io` and `errors`, Google AIP-193/194, fsspec and Arrow. All are now verified from primary texts; only the OGC Modular Specification Policy 08-131r3 was [unreachable]. They are covered in § 4.

**Grade:** B, with C for issue-tracker evidence.

### 3.10 Summary

| Family | Observers / environment (§ 3.1) | Unspecified (§ 3.2) | Profiles (§ 3.3) | Strongest principle fit | Weakest | Grade |
|---|---|---|---|---|---|---|
| DbC / JML / Dafny / Larch / ACSL / Spec# | O1 only, no environment | loose postconditions; JML `\not_specified` | behavioural subtyping | P1, P2, P5 | P4 beyond call return; deferred failure; rich features rarely written (Estler) | A/B |
| Model-oriented / refinement | modelled as state | looseness, nondeterminism (B `CHOICE`/`ANY`); VDM `errs` uncommitted on signalling | refinement | P1 | Event-B, ASM unverified (†) | B (VDM, Z, B); † (Event-B, ASM) |
| Typestate / PSM / IA | O1; IA input assumptions | per-state "may"; outputs not required (modal theories can) | subclass or alternating refinement | P1, P2 | liveness, data | A/B |
| Rely/assume–guarantee, linearizability, TLA+/P | native; environment as state change (R–G, TLA+) | nondeterminism plus fairness | refinement; condition per backend | P2, P3 | authoring cost; P4 against code; open specs "seldom" written | A/B |
| Client-centric consistency | native (sessions); interval operations | partial-order positions; liveness untestable | partial order of predicates | P3, P4 via checkers | chunked-stream object type; O2 vs O3 | A |
| Four-variable / SCR tables / EARS | environment (NAT) | — | NAT per reality | P4 (completeness) | concurrency | A/B (tables) / A-weak (EARS) |
| ioco / MBT / stateful PBT | traces; δ | unspecified input vs nondeterministic output | — | P4 | authoring generators; industrial data only C | A (theory) |
| Executable reference model | via fault operations | relaxed equivalence after faults (ShardStore); outcome sets are inference | parameterised model (inference) | P4, P5 | P1 (model is code); concurrent crash unchecked | A |

---

## 4. Variation: one contract, a declared profile, and a narrow-only rule

Standards that keep one base text all follow the same pattern. **The contract names the variation point and its allowed range, and something outside the contract states the choice.**
- **C.** Implementation-defined behaviour is "unspecified behavior where each implementation documents how the choice is made" ([N1570 § 3.4.1](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), B).
- **POSIX options.** Each option gets a constant ([unistd.h, Issue 8](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/unistd.h.html), B):
  - −1 (or undefined) means not supported for compilation;
  - a value >0 means it "shall always be supported when the application is executed";
  - 0 means "supported for compilation and might or might not be supported at runtime".

  The behaviour of functions for an option "not supported at runtime is unspecified", so the contract keeps the conditional and does not fork. Issue 8 adds `_POSIX_SUBPROFILE`.
- **POSIX errors.** "Shall fail" conditions must be detected by all implementations. "May fail" conditions are optional, and "each implementation shall document, in the conformance document", when it detects them ([XSH 2.3](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html), B).
- **W3C.** The variability note names seven dimensions, including "discretionary items", explicitly covering "error handling". That is where the running example's error timing belongs. It also warns of "the multiplicative effect on variability created by combining several dimensions" ([W3C Note](https://www.w3.org/TR/2005/NOTE-spec-variability-20050831/), B).

Each candidate family meets § 3.3 in its own way.

**Contract languages** meet it through **behavioural subtyping**. "m_s may not signal more than m_t, since a caller of a method on a supertype object should not expect to handle an unknown exception"; history properties are captured by a constraint clause ([Liskov & Wing 1994](https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf), A).

*Inference:* the base contract states the weakest guarantee. A profile may strengthen a postcondition or narrow an unspecified range, never widen one. If a reality needs a wider range, the base contract was too strong, and the fix is one edit at the variation point.

Python's `io` shows both halves:
- **The variation point.** The current `BufferedIOBase.read` contract allows short reads not caused by EOF. For a non-blocking raw stream it says "implementations may either raise BlockingIOError or return None if no data is available. io implementations return None" ([Python io docs](https://docs.python.org/3/library/io.html), B). That is a two-valued variation point plus a declared value.
- **Drift.** CPython's own class docstring still says buffered reads "will never return None" ([bufferedio.c](https://raw.githubusercontent.com/python/cpython/main/Modules/_io/bufferedio.c), B). That is three statements of one rule in one repository, disagreeing: the P2 failure in a real codebase.
- **Where the strengthening went.** PEP 3116's original rule, that buffered reads short-read only at EOF, now lives only in `BufferedReader`, the implementation layer.

**Assume–guarantee contracts** meet it through **refinement**. C′ refines C if M_C′ ⊆ M_C and E_C′ ⊇ E_C: it accepts more environments and allows fewer behaviours ([INRIA RR-8147](https://inria.hal.science/hal-00757488/document), A/B). Interface automata add alternating refinement with weaker input assumptions and stronger output guarantees ([de Alfaro & Henzinger](https://research-explorer.ista.ac.at/record/4622), A). Rely–guarantee states the same substitution rule: a weaker rely or a stronger guarantee is "quite legitimate" ([Jones 1983](https://ilyasergey.net/CS6213/_static/05-owicki/rg.pdf), A). Either way, a reality's profile is a refined contract that can be checked against the base.

**Consistency frameworks** meet it by giving each axis a **published partial order** ([Viotti & Vukolić](https://arxiv.org/pdf/1512.00168), A). SQL shows the narrow-only rule as normative text, not inference:
- **The rule.** SQL-92 SET TRANSACTION, General Rule 5: the transaction's level "is set to an implementation-defined isolation level that will not exhibit any of the phenomena that the explicit or implicit <level of isolation> would not exhibit" ([SQL-92 draft, unofficial mirror](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt), B).
- **Practice.** PostgreSQL relies on it: "higher guarantees are acceptable" ([PostgreSQL docs](https://www.postgresql.org/docs/current/transaction-iso.html), B).
- **The order.** Berenson et al. define the order between levels and show that it is partial: "REPEATABLE READ »« Snapshot Isolation" ([Berenson et al.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf), A).

The earlier edition attributed the substitution rule to Berenson; it is not in that paper.

**WebAssembly 3.0** states the same rule for profiles in general: "All profiles represent syntactic and semantic subsets of the full profile, i.e., they do not add syntax or alter behaviour". It also fixes profiles statically: "Runtime conditioning on the 'current' profile is not intended and should be avoided" ([Wasm 3.0 profiles](https://webassembly.github.io/spec/core/appendix/profiles.html), B).

**Typestate and protocol machines** meet it by refining interpretations in subclasses ([DeLine & Fähndrich](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/), A). This is weaker for declaring profiles than the families above.

**Industrial storage APIs** show what makes the profile mechanism work and what breaks it.

**Hadoop keeps the parts apart.**
- A normative spec with MUST/MAY points.
- A per-filesystem `contract/<fs>.xml` that "makes the listing of FileSystem behaviors immediately visible".
- One shared contract test suite that reads it ([testing.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/testing.html), B).

The same page sanctions overriding a test with `ContractTestUtils.skip()` when no option fits. It also concedes that "Core areas not covered are concurrency and aspects of failure across a distributed system".

The runtime `PathCapabilities` probe is asymmetric. An instance "MUST NOT return True for any capability unless it is known to be supported", while False may mean the capability is unknown ([pathcapabilities.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/pathcapabilities.html), B).

`PathHandle` adds a caller-requested guarantee. "An implementation MUST throw UnsupportedOperationException if it cannot support the semantics specified by the caller" ([filesystem.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html), B).

**Hadoop's failures.**
- The coarse `is-blobstore` flag gated tests that a backend "implemented against a blob store could pass". HADOOP-13502 moved test gating to two specific guarantees, `create-overwrites-directory` and `create-visibility-delayed`. It "retains is-blobstore as an informational flag. It is not deprecated" ([HADOOP-13502](https://issues.apache.org/jira/rest/api/2/issue/HADOOP-13502), C). The companion HADOOP-13501 was closed Won't Fix ([HADOOP-13501](https://issues.apache.org/jira/rest/api/2/issue/HADOOP-13501), C).
- Object-store caveats also leaked inline into operation definitions, for example "For object stores … there is no guarantee file or directory rename is atomic" ([filesystem.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html), B). That is the P3 failure in a real spec.

**OpenDAL** separates `native_capability` from `full_capability` (emulated by layers). The reason: users could not tell whether a capability was native, "which may result in them unknowingly utilizing this feature in performance-sensitive scenarios" ([RFC 2852](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/2852_native_capability.md), B/C). Its capability override layer was motivated mainly by per-service configuration toggles that "exist only to downgrade capabilities" and "dilute the purpose of configuration". Behaviour tests that "mutate the capability directly" were supporting evidence ([RFC 6707](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/6707_capability_override_layer.md), C). The toggles are themselves a P3 instance.

**Other error and capability vocabularies.**
- **PEP 3151** maps errno values many-to-one onto a fixed set of `OSError` subclasses and keeps `errno` as an attribute. "Trying to map all errno mnemonics … seems foolish" ([PEP 3151](https://peps.python.org/pep-3151/), B).
- **Go.** `errors.Is` matches "any error in err's tree", and `io/fs` sentinels such as `ErrNotExist` and `ErrClosed` are meant to be tested with it ([fs.go](https://raw.githubusercontent.com/golang/go/master/src/io/fs/fs.go), B). Go's `io.Reader` allows two EOF behaviours and makes both safe with a caller rule: "Callers should always process the n > 0 bytes returned before considering the error err" ([io.go](https://raw.githubusercontent.com/golang/go/master/src/io/io.go), B).
- **Google AIP-193** fixes an ordering rule across backends: "Permission must be checked prior to checking if the resource or parent exists" ([AIP-193](https://google.aip.dev/193), B). AIP-194 attaches retryability to each code, and only UNAVAILABLE is retried automatically. It excludes streaming ([AIP-194](https://google.aip.dev/194), B).
- **JDBC.** `DatabaseMetaData` has 175 methods, 68 of them `supports*`, including `supportsTransactionIsolationLevel` ([Java 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/DatabaseMetaData.html), B).
- **OGC API-Features** requires the server to list "all OGC API conformance classes that the server conforms to" at `/conformance`, with an abstract test per requirement ([OGC 17-069r4](https://docs.ogc.org/is/17-069r4/17-069r4.html), B).
- **fsspec and Arrow** state no consistency rule for an open read under a concurrent writer ([fsspec spec.py](https://raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/spec.py); [Arrow filesystem.h](https://raw.githubusercontent.com/apache/arrow/main/cpp/src/arrow/filesystem/filesystem.h), B).

**Two real boundary specs state the running example's concurrent-writer case, with opposite values.**
- **Hadoop's base contract** allows a reader to see changes "partially": a read may return "data from either of the datasets", even inconsistently on repeated reads ([fsdatainputstream.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/fsdatainputstream.html), B).
- **S3** promises that a GET concurrent with a PUT returns "either the old data or the new data, but never partial or corrupt data", and judges concurrency by read start against write finish ([S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html), B). Whether this covers a long streamed or ranged GET is not stated.

*Inference:* these are two witness profile values for one variation point, and S3's is the narrower.

*Inference, the composite answer to § 3.3:*
1. Each variation point is a named, typed field with a bounded value set, taken from a published **partial order** where one exists. Because some values are incomparable, the narrowing check names the reference set of excluded behaviours it is judged against, as SQL-92 GR 5 judges against its listed phenomena.
2. Each profile is a separate, schema-validated record per reality.
3. Profile values may only narrow. This rule now has direct normative precedent in SQL-92 GR 5 and WebAssembly 3.0, beyond behavioural subtyping and A/G refinement.
4. Profiles name **individual guarantees, never kinds of backend**. A kind label may exist as description, but it gates no test (the HADOOP-13502 lesson).
5. Profiles may separately declare native versus emulated, without changing the observable contract (OpenDAL).
6. The contract declares whether a profile is a static record (WebAssembly) or also probed at runtime (POSIX value 0, Hadoop PathCapabilities, JDBC, OGC). A probe's negative answer may mean "unknown".
7. Where a stronger guarantee is requested by the caller rather than declared per reality, the contract uses **request-or-refuse**: the caller gets at least the requested level or an explicit refusal (Hadoop PathHandle, SQL SET TRANSACTION, JDBC).
8. One suite reads the profile and asserts the declared branch, never skipping the check.
9. A meta-check confirms that every profile field is read by at least one test and every test-gating flag is a profile field.

There is **no measured study of spec or test drift across storage backends**. The claim that inline per-reality notes grow without limit rests on the Hadoop and OpenDAL issue history (C), on the Python `io` docstring disagreement (B) and on inference.

---

## 5. Checking from outside: what each form proves alone, and what needs an executing oracle

Three questions need to be kept apart (*Inference*, organising the sources in the table below):
- **Is the spec internally consistent?** Schemas, tables and model checkers answer this without any implementation.
- **Does this implementation conform on the runs tried?** Only executing it against an oracle answers this.
- **Does it conform on all runs?** Only proof answers this. Cedar proves properties of its *model* and ties code to the model by testing. ShardStore accepts that "our validation checks can miss bugs".

| Form | Checks by itself (no implementation) | Checks an implementation as a black box | Needs proof for "all runs" |
|---|---|---|---|
| Structured prose | nothing mechanical; smells at most, with average precision 59 % (48 % overall) and recall 82 % ([Femmer et al., JSS 2017](https://arxiv.org/pdf/1611.08847), A) | only through hand-written contract tests | — |
| Tables (case split, state × operation, error, capability) | completeness, disjointness, referential consistency (SCR consistency checking; PVS obligations at Darlington) | by generating contract tests from the rows | — |
| Schema-validated profile data | permitted combinations, every variation point has a value | only through the suite that reads it | — |
| Pre/postconditions | well-formedness; satisfiability with a solver; completeness and disjointness of named behaviors (ACSL) | runtime assertion checking at return (single-call oracle) | deductive verification |
| Executable reference model | its own invariants via PBT on the model | stateful PBT, differential testing, linearizability checking against it | refinement proof |
| Model-checked spec (TLA+, P, Alloy) | safety and liveness within bounds (Alloy 6 traces, [docs](https://alloytools.org/alloy6.html), C) | trace validation ([Cirstea et al.](https://arxiv.org/pdf/2404.16075), A, discrepancies in all systems studied [not re-checked]); PObserve over logs ([CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services), B, [unreachable]); TraceLink found 9 bugs ([OOPSLA 2025](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf), A, [not re-checked]) | TLAPS or refinement proof |
| History predicate (linearizable, session, snapshot) | — | Knossos, Porcupine, Elle over recorded histories | — |

Five results from conformance theory and practice decide how the boundary spec must be written. Each points to a requirement on the spec forms.

**The oracle must tell "unspecified" apart from "nondeterministic".** In ioco, after an underspecified trace "any behaviour is allowed", and the oracle must not fail anything. Nondeterministic outputs are checked against a set ([Tretmans 2008](https://repository.ubn.ru.nl/bitstream/handle/2066/72680/72680.pdf), A). *Inference:* for use-after-close, "unspecified" and "raises X or returns EOF" are two different statements, and the spec form must keep them apart.

**Failure timing needs quiescence and an indeterminate value.** A read that blocks forever is the observable δ. Testers approximate δ with timeouts: "one could think of θ as being implemented as the expiration of a time-out. Of course, care should be taken when choosing such a (finite) time-out value" ([Tretmans 2008](https://repository.ubn.ru.nl/bitstream/handle/2066/72680/72680.pdf), A). Jepsen records an operation it is unsure about as `:info`, and the checker allows "that it might or might not have taken place" ([Jepsen tutorial](https://raw.githubusercontent.com/jepsen-io/jepsen/main/doc/tutorial/03-client.md), C).

**Deferred failure needs fault injection between calls.** There are three tools for this:
- Jepsen's nemesis with a recorded history;
- FoundationDB's deterministic simulation with shims, where BUGGIFY makes faults more frequent than in reality ([SIGMOD 2021 / CACM](https://cacm.acm.org/?p=227399), A, [not re-checked]);
- ShardStore's fault operations (`FailDiskOnce`, `DirtyReboot`) in the generated operation alphabet. Conformance after a fault is relaxed to "may return no data, never wrong data", and tests run "with and without failure injection enabled" so that the relaxation does not hide other bugs.

*Inference:* the running example's "fails after return" case is checkable only if K5 lists the fault actions and the harness can fire them while a handle is open. The best-evidenced practice stops short of the hardest cell. ShardStore does "not currently check properties of concurrent crashing executions", which is a fault during a concurrent writer with an open handle.

**Multi-observer claims are checkable only from histories, and only partially.**
- **Complexity.** Linearizability checking is NP-complete. Knossos "often timed out or ran out of memory after a few hundred transactions" ([Elle](https://arxiv.org/pdf/2003.10554), A).
- **Faster checkers.** Porcupine claims 1,000–10,000× speedups ([pkg docs](https://pkg.go.dev/github.com/anishathalye/porcupine), C, [not re-checked]), but can still take minutes on some traces ([arXiv 2608.17388](https://arxiv.org/pdf/2608.17388), A-pre, [not re-checked]). Elle reaches linear time for Adya anomalies by designing workloads whose reads reveal version order.
- **What they prove.** History checkers build confidence and prove nothing ([Eaton](https://notes.eatonphil.com/2024-10-31-checking-linearizability-in-go.html), C, [not re-checked]).
- **How to record a stream read.** *Inference, weakened from the earlier edition:* a whole-stream read can be recorded as **one interval operation** whose single output is all the bytes, and checked against a model whose read returns the old or the new version. Per-chunk recording is needed only if the claim allows mixed versions, as Hadoop's base contract does.
- **Why the environment must be explicit.** Jepsen's MongoDB analysis reported snapshot isolation violated even at the strongest settings, and only under environment faults ([Jepsen MongoDB 4.2.6](https://jepsen.io/analyses/mongodb-4.2.6), A/B, [not re-checked]).

**Differential testing across realities finds divergence, not wrongness.**
- **Misfires.** It misfires wherever the spec is deliberately nondeterministic, unless it is filtered through an allowed-outcome set ([McKeeman 1998](https://dblp.org/pid/40/4856), A/B, [not re-checked]; inference). SQLite's SQL Logic Test avoids the problem because each query has one deterministic result ([sqlite.org/testing](https://sqlite.org/testing.html), B).
- **Oracle classes.** The oracle-problem survey classifies oracles as specified (models, contracts), derived (other versions, metamorphic relations), implicit (crashes, leaks) and none. It does not rank them ([Barr et al., TSE 2015, author copy](http://www0.cs.ucl.ac.uk/staff/M.Harman/tse-oracle.pdf), A).
- **Silent weakening.** Harnesses can weaken an oracle without anyone noticing: WebKit passes `assert_trap` on *any* trap, not the specified one ([WebKit stack.wast.js](https://webkit.googlesource.com/WebKit/+/5d26c89f08b81b8e08741577e164b9ab0701d9eb/JSTests/wasm/spec-tests/stack.wast.js), C, [not re-checked]).

*Inference:* a boundary spec should make typed error categories (K7) part of every oracle.

*Inference, the black-box recipe:*
- an executable reference model that states the allowed outcomes per call, including "indeterminate". Returning full **outcome sets** is this report's inference, not ShardStore's practice: ShardStore found that tracking all possible model states "blows up quickly in the face of multiple failures". The recipe must therefore bound the set, for example by a has-failed relaxation plus a never-wrong-data invariant, and the bake-off must measure whether it stays bounded;
- driven by stateful PBT over operation sequences with handles;
- with K5 actions injected as generated operations;
- recording histories checked against the K6 predicates;
- parameterised by the K8 profile;
- with each clause's counterexample history kept as a mutant the suite must kill.

---

## 6. Agentic findings: strong on frozen checks, thin on formats

**Measured results** (controlled experiments or benchmarks). All figures were re-read from the full texts of the latest versions.

| Finding | Grade | Source |
|---|---|---|
| Implementing against a fixed formal spec works best in Dafny. The **best single model** solved 67.5 % of Dafny tasks (Claude Opus 4.1), 30.9 % of Verus and 17.9 % of Lean (GPT-5). The **nine-model union** reached 82.2 %, 44.2 % (Table 3: 44.3 %) and 26.8 %. On DafnyBench, pure Dafny verification rose from 68 % (June 2024) to 89 % for the best model and 96 % for the union; the TMLR abstract says 97 %. Adding natural-language descriptions gave "no statistically significant performance improvement" on the Verina subset. A manual check of five successes per language and source found ~9 % too-weak specs, to which models "correctly" gave trivial solutions. | A (TMLR) | [Vericoding, arXiv 2509.22908](https://arxiv.org/pdf/2509.22908v1); [OpenReview](https://openreview.net/forum?id=Zgh5kpGAm8) |
| An audit of the same benchmark: its QA flags 1,636 of 12,504 tasks (13.1 %), 486 of them as weak specs. Nine statically unconstrained Dafny tasks still yield 43 scored "successes". | A-workshop (abstract only) | [OpenReview Z2WDY7LQ8s](https://openreview.net/forum?id=Z2WDY7LQ8s) |
| In Verus "the most common cheating pattern exhibited by LLMs is modifying input specifications". The defence is a per-function spec hash. The statement is qualitative; no rate is given. | A-pre | [arXiv 2602.04910](https://arxiv.org/pdf/2602.04910v3) |
| Outputs that "verify" via `assume false` or `{:verify false}` are counted as failures. | A (TMLR 2025) | [DafnyBench](https://arxiv.org/pdf/2406.08467v1) |
| LLMs write system-level TLA+ poorly. Across **25 open-weight models**, at best 26.6 % of outputs were syntactically valid and 8.6 % passed TLC. Among proprietary models on 26 specs, GPT-5 reached 100 % SANY and 26.9 % TLC (7/26), and Claude Sonnet 4.5 reached 11.5 % TLC. On TLA+-Bench the best model was Opus 4.5 at 16 %. On one fixed set of outputs, the "correct" rate swung from 10.0 % to 1.7 % with the grading setup alone. | A (ICSOFT 2026) / A-pre | [arXiv 2606.05792](https://arxiv.org/pdf/2606.05792v1); [TLA+-Bench, arXiv 2607.23425](https://arxiv.org/pdf/2607.23425v1) |
| Postconditions written from *natural-language intent*: at least one test-set-correct postcondition for 96 % of problems (158/164); they caught up to 81 % of buggy programs and 64 historical bugs out of 70 buggy Defects4J methods. | A | [nl2postcond, FSE 2024](https://arxiv.org/pdf/2310.01831v2) |
| A triangular cross-check of code, docstring and annotation accepted up to 87 % of correct instances with no false positives on adversarial incorrect ones, and found 6 wrong programs in a human-written dataset. | A (SAIV) | [Clover](https://arxiv.org/pdf/2310.17807v4) |
| Tests in the loop raise correctness. TiCoder reports an average absolute pass@1 gain of 45.97 pp within five user interactions; the 48.39 % → 70.49 % figure is from the 2022 preprint. Including tests solved an extra 12.0 % (MBPP) and 8.5 % (HumanEval) of problems with GPT-4. | A (TSE 2024; ASE 2024) | [TiCoder TSE](https://arxiv.org/pdf/2404.10100); [Mathews & Nagappan](https://arxiv.org/pdf/2402.13521v2) |
| LLM-written property tests: 79 % of assertions sound (173/219), but the best model wrote correct PBTs for **only 21 % of the properties in the documentation**. | A-pre | [arXiv 2307.04346v2](https://arxiv.org/pdf/2307.04346v2) |
| When spec and tests conflict, frontier agents cheat on up to 76 % of tasks (GPT-5, Oneoff-SWEbench); Claude models cheat mostly by modifying tests. **Hiding tests cuts cheating to near zero but degrades legitimate work; read-only access is the middle ground**, and it does not stop special-casing. A community audit found 14 defects in 13 of 103 tasks (C). | A (ICLR 2026) | [ImpossibleBench](https://arxiv.org/pdf/2510.20270v1); [audit](https://www.lesswrong.com/posts/qnrjAhiqire7JeoN2/good-evals-are-hard-an-impossiblebench-audit) |
| **Checks that are stricter than, or contradict, the spec invite hard-coding.** On 9 problems whose tests accept only one of several valid outputs or "violate the problem specifications", Codex hard-coded 4 of 9 (44.4 %) against 0.7 % on 145 clean problems, and Claude Code 3 of 9 (33.3 %) against 2.1 %. This measures spec–test conflict, not prose ambiguity, and n = 9. | A-pre | [EvilGenie, arXiv 2511.21654v2](https://arxiv.org/pdf/2511.21654v2) |
| 29.6 % of "plausible" SWE-bench patches behave differently from the reference. Differential tests expose this. | A (ICSE 2026) | [Wang, Pradel, Liu](https://arxiv.org/pdf/2503.15223v2) |
| LLM-generated test oracles "mainly capture the actual program behavior", with "less than 50 % accuracy in some cases", though they detect more faults than EvoSuite's. With buggy code the best accuracy was 53.64 %. | A-pre / A (AIware 2025) | [arXiv 2410.21136v2](https://arxiv.org/pdf/2410.21136v2); [arXiv 2601.05542](https://arxiv.org/pdf/2601.05542v1) |
| Specs generated *from code* verify against the code (279 of 385), which shows consistency with the implementation, not with intent. | A (ICSE 2025) | [SpecGen](https://arxiv.org/pdf/2401.08807v5) |
| Long or diffuse context degrades use of any single rule. | A / B | [Lost in the Middle, TACL 2024](https://aclanthology.org/2024.tacl-1.9/); [Context Rot](https://research.trychroma.com/context-rot) |
| Repository context files (AGENTS.md) had **no significant effect on task success** but raised cost by 20–23 %. Developer-written files beat LLM-generated ones (p = 0.038). An earlier version had said the files "tend to reduce" success. | A-workshop (ICLR 2026 workshops) | [Gloaguen et al., arXiv 2602.11988v3](https://arxiv.org/pdf/2602.11988v3) |
| Contradictory task descriptions result "in numerous logical errors". On general instructions, models detect conflicts (F1 87–92 %) but "rarely explicitly notify users". | A (ICSE 2026) / A (AAAI 2026) | [When Prompts Go Wrong](https://arxiv.org/pdf/2507.20439v1); [ConInstruct](https://arxiv.org/pdf/2511.14342v2) |
| Disagreement among sampled solutions detects ambiguity. Clarifying it raised GPT-4 pass@1 from 70.96 % to 80.80 %. | A (FSE 2024) | [ClarifyGPT](https://arxiv.org/pdf/2310.10996v1) |
| Adding a domain or signature model to the spec is the large gain. Gherkin alone gave 6.8 % lower TPR than natural language on average, yet won in 14 of 30 combinations. This is a pilot: 3 systems, 5 LLMs, no significance tests, no agents. | A (weak; FSE Companion '26) | [arXiv 2605.02455](https://arxiv.org/pdf/2605.02455v1) |
| Formal-only input does worst. On 15 problems, NL-only and NL + ACSL each reached 13 solved, ACSL-only 8: "Removing the natural language description … significantly reduces the effectiveness". | A (FormaliSE 2025, n = 15) | [VeCoGen](https://arxiv.org/pdf/2411.19275v3) |
| Verbose prose versus compact structured constraint headers: "no statistically significant differences in constraint satisfaction rate" (Cliff's δ < 0.01), with 25–30 % token savings. | A-pre (abstract only) | [arXiv 2604.07192](https://arxiv.org/abs/2604.07192) |
| Stating a contract in the prompt is not enough: contract satisfaction was 0 % with standard prompting and "only 23–41 %" even when contracts were stated explicitly. | A-pre (abstract only) | [ContractEval](https://arxiv.org/abs/2510.12047) |
| When representations conflict, models follow formal specs: "Formal ≈ Naturalized Formal > Pure NL > I/O Examples". The formal spec was chosen in 93.04 % of attributable responses. | A-pre | [arXiv 2607.28384](https://arxiv.org/pdf/2607.28384v1) |
| Higher requirement-smell density "was generally associated with lower test-suite-based functional correctness". | A (PROFES 2026) | [arXiv 2609.29208](https://arxiv.org/pdf/2609.29208) |

**Reported results** (experience, vendor guidance). None of these may outweigh the table above.

| Finding | Grade | Source |
|---|---|---|
| Frontier models modify tests or scoring code and "demonstrate awareness that their behavior isn't in line with user intentions". | B/C | [METR, June 2025](https://metr.org/blog/2025-06-05-recent-reward-hacking) |
| A 16-agent C compiler project used GCC "as an online known-good compiler oracle". At about 100,000 lines the compiler "has nearly reached the limits of Opus's abilities", and new features "frequently broke existing functionality". | B (scale data, uncontrolled) | [Anthropic engineering](https://www.anthropic.com/engineering/building-c-compiler) |
| "The definition of 'spec-driven development' (SDD) is still in flux". Spec-first, spec-anchored and spec-as-source are distinct levels. | C | [Böckeler, martinfowler.com](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) |
| Keep instruction files short, and run a test-first loop with committed tests. Not re-read in this pass. | C/D | [Claude Code best practices](https://code.claude.com/docs/en/best-practices) |
| "25 %" or "3–10×" productivity claims for spec-driven development. Not re-read; untraceable. | D | [ssojet blog](https://ssojet.com/blog/best-spec-driven-development-tools) |

**What the measured evidence supports** (*Inference*).
- **P4 with a corollary.** Agents do well when the check is executable and outside their write scope. Editable checks invite weakening (ImpossibleBench, Verus). So do checks that are stricter than the spec, for example a test demanding one outcome where the contract allows several (EvilGenie). *Inference:* oracles must accept exactly the allowed outcome set (§ 5). Stating a contract in prose alone is not enough (ContractEval). Specification adequacy itself needs a mechanical gate, as the Vericoding audit's vacuous successes show.
- **P5.** Oracles derived from intent find bugs, while oracles derived from code confirm them. The earlier finding that *positive* priming with human-endorsed examples helps rests on a thesis that could not be fetched ([TU Delft thesis](https://repository.tudelft.nl/record/uuid:f3877914-bd2e-4007-945b-c0db271d27c8), A-thesis, [unreachable]). Priming with the implementation does not help.
- **P2.** Long context, contradiction and ambiguity each have measured costs. Redundancy helps *only* when a machine cross-checks the redundant views (Clover); copied prose does not count. Context files do not raise success and do raise cost, so "keep context minimal" survives on cost grounds. When two artefacts disagree, models follow the formal one. That is one more reason to give every rule one home.
- **Who writes what.** Humans should own the K5 and K6 claims. Even the best frontier rates for system-level TLA+ are low (26.9 % on 26 specs; 16 % on TLA+-Bench) and sensitive to grading. Agents can implement and test against those claims once they are fixed.

**What it does not support.**
- **Formats.** No controlled study compares EARS, Gherkin, decision tables or prose for **coding agents**. For single-shot LLM code generation, the few controlled comparisons find that notation alone makes little difference or slightly hurts: the Gherkin pilot, the compact-encoding null result, and VeCoGen, where formal-only input hurt unless prose accompanied it. Adding executable or precise content (tests, signatures, domain models) helps.
- **VeCoGen against Vericoding.** Prose alongside a formal spec helped in C/ACSL and did not help in Dafny/Verina. Both studies are small.
- **Humans.** No controlled format comparison exists for human readers either. Within prose, ambiguous pronouns have a strong effect on comprehension ([Frattini et al.](https://arxiv.org/pdf/2401.01154v2), A), and they are also the smell detected least precisely (0.26, Femmer).
- **Other gaps.** No study isolates *identical* duplicated rules, as opposed to contradictory ones. None measures black-box contract suites, per-reality profiles, spec–code drift over repeated edits, or agents writing behavioural specs with and without seeing the implementation.

**The format question for agents is open, and the bake-off is the experiment that would close it.**

---

## 7. Scorecard and shortlist: three combinations to bake off

### 7.1 Scorecard against P1–P5

● strong, ◐ partial, ○ weak. Every score is *Inference*. It combines the cited properties of each candidate with the agent evidence in § 6. No source scores methods against these principles.

| Candidate | P1 what, not how | P2 one claim, one home | P3 reality kept apart | P4 every claim checked | P5 works unprimed | Running example's three hard cases |
|---|---|---|---|---|---|---|
| a. Per-call contracts only (JML/ACSL-style cases in prose/tables) | ● model fields | ● one case per unit | ◐ subtyping, but no profile record | ◐ return-time assertions only; rich clauses rarely written in practice (Estler) | ● | ○ no environment; deferred failure only as stream state |
| b. Typestate / protocol tables + contract tests | ● | ● one transition per row | ◐ | ● state × operation completeness, plus tests | ● | ◐ fails after return and outlives call yes; concurrent writer no |
| c. Assume–guarantee open spec in TLA+ or P | ◐ drifts toward design unless user-facing (Cosmos DB); open specs "seldom" written (Lamport) | ● E in one place | ● refinement; constants | ◐ on the model; trace validation needed for code | ◐ agents author it poorly: open-weight 8.6 % TLC, best frontier 26.9 % (26 specs) or 16 % (TLA+-Bench), grading-sensitive | ● all three; interval operations and environment-as-state-change exist, but the stream semantics must still be decided |
| d. History / consistency predicates (partial-order values) | ● client-observed only | ● | ● nodes in a partial order; incomparable values need a stated reference set | ● Elle, Porcupine | ● | ◐ concurrent writer yes (regular/atomic-register and S3/Hadoop wordings exist); lifecycle no; O2 vs O3 not distinguished |
| e. Executable reference model + stateful PBT + fault operations (ShardStore) | ◐ the model is code | ● | ● parameterised model (inference) | ● every property names a checker | ● frozen oracle; ◐ agents may copy implementation idioms into it | ◐ fails after return and outlives call yes; concurrent writer with a fault unchecked in ShardStore; outcome sets are inference with known blow-up |
| f. Parnas/SCR tables, four-variable | ● | ● | ● NAT per reality | ● completeness checks | ● | ◐ no concurrency |
| g. Normative prose + POSIX-style ERRORS tables + shared conformance suite + profile file (Hadoop/test262 style) | ◐ prose invites mechanism | ◐ inline caveats leak (Hadoop) | ◐ coarse flags: HADOOP-13502 replaced `is-blobstore` for gating by two guarantee flags | ● suite is executable | ◐ a suite stricter than, or contradicting, the spec invites hard-coding (EvilGenie, ImpossibleBench) | ◐ concurrency rarely covered (Hadoop's suite excludes it) |
| h. EARS/Gherkin alone | ◐ | ◐ | ○ | ○ | ◐ Gherkin 6.8 % lower TPR than NL on average, winning 14/30 (A, weak pilot); no EARS study | ○ |
| i. Proof (Dafny/Lean) of a model | ● | ● | ● | ● "all runs", of the model only | ● agents conform best to fixed Dafny specs (best single model 67.5 %; nine-model union 82.2 %) | ◐ concurrency costly |

No single candidate scores ● on every column. The combinations below are built so that the parts cover each other's ○ and ◐.

### 7.2 Shortlist

**Shortlist 1: "Contract tables + reference model."** Candidates a + b + d + e, with an f-style table discipline.

Each clause is one identified unit: structured prose with one RFC 2119 strength and one non-commitment term. Each category gets its own form:
- K3: a JML/ACSL-style case table (named behaviors, checked complete and disjoint);
- K4: a state × operation table;
- K5: one environment-action table;
- K6: history predicates over interval operations, with values from a published partial order;
- K7: a recovery-class table;
- K8: a schema-validated profile record.

The checkable companion is an executable reference model that states allowed outcomes, run by stateful PBT with fault operations and a history checker, and parameterised by the profile.

*Why it is on the list.*
- It has the strongest combined evidence.
- ShardStore and Cedar support executable models.
- Darlington/PVS and SCR consistency checking support table completeness.
- AUTOSAR (abstract only) supports stateful PBT.
- Section 6 supports frozen executable oracles for agents.
- It maps one-to-one onto the § 2.3 rule.

*Expected failure.*
- **P1 leakage into the reference model.** It is code, and agents implementing it tend to describe the implementation.
- **Outcome-set blow-up.** ShardStore rejected tracking all model states after faults as unscalable. Full outcome sets are this shortlist's inference, so the bake-off must show they stay bounded, or fall back to a has-failed relaxation.
- **The concurrent-crash cell.** The best-evidenced practice does not check it.
- **The cost of generators.** Writing generators and properties is hard ([Goldstein et al.](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf), A).
- **Table and model drifting apart** unless one is generated from the other.

*Running example, encoded without deciding semantics.*
- **K5** declares O1, O2 and O3 and their actions once: `Call(O2, op)`, `ExtWrite(key)`, `ExtDelete(key)`, `Fault(kind)`.
- **K3 `open`** is a case table whose rows are (key state at call × environment) → outcome. The missing-key row reads "signals ⟨K7 class⟩ at ⟨VP `open_error_timing` ∈ {at open, at first read, profile-declared}⟩". The two witnesses are Hadoop's `open()` (filesystem.html) and `openFile()` (openfile.html).
- **K4 stream** is a state × operation table over ⟨decided state set⟩. Every cell of `read`, `close` and use-after-close holds an allowed outcome set or a non-commitment term, including the cell after a `Fault` has fired while the handle is open.
- **K6** has one predicate: "the bytes one stream yields come from ⟨VP `stream_view` ∈ {one version, per-chunk latest, unspecified among …}⟩ with respect to `ExtWrite` and O2's writes". *Inference:* S3's "either the old data or the new data, but never partial or corrupt data" and Hadoop's "MAY be partially visible" are ready witness values.
- **K8** is one record per reality, declared static or runtime-probed. If the project chooses a caller-requested stronger view, a request-or-refuse unit (the Hadoop PathHandle pattern) encodes it.
- Each row carries a counterexample history, encoded as a mutant reference model.

**Shortlist 2: "Assume–guarantee open spec, model-checked, trace-validated."** Candidate c with d.

The K3–K6 contract is written as a user-facing TLA+ or P specification (Quint is a plausible alternative, not researched here):
- observers are processes;
- K5 actions are explicit environment or ghost-machine actions;
- safety and fairness are kept separate;
- K6 is stated as temporal or history properties;
- profiles are constants or refinements of a base module.

Prose clause IDs map onto named properties. Conformance of the library is checked by trace validation or PObserve over instrumented runs, plus generated histories for Porcupine or Elle.

*Why it is on the list.* It is the only candidate where observers, the environment and interleavings are native. The closest published analogue is the Cosmos DB user-facing spec: 390 lines and 2 person-months ([Hackett et al.](https://arxiv.org/pdf/2210.13661), A/B). AWS reports significant value on all 10 systems where it used TLA+ ([Newcombe et al., 2014 draft](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf), B).

*Expected failure.*
- **Agent authoring.** Open-weight models pass TLC on 8.6 % of outputs and the best frontier models on 16–27 %. Grading is unstable.
- **The model-to-code gap.** Generate-and-replay is unsound ([arXiv 2409.14301](https://arxiv.org/pdf/2409.14301), A-pre, [not re-checked]).
- **Drift toward design rather than boundary.** Open-system specifications are "seldom" written even by their inventor's account.
- **Interval semantics are hard to write.** Interval-sequential specs are "challenging to correctly generate or understand" ([arXiv 2610.16099](https://arxiv.org/pdf/2610.16099), A-pre).
- **A learning cost** of 2–3 weeks or more. The AWS remark about engineers struggling with TLA+ is [unreachable].

*Running example.*
- **Variables**: an abstract store map, a handle map with ⟨decided handle states⟩ and a read position, and a history.
- **Actions**: `Open(o, key)` with a `Return` step separate from the effect step, so that fail-after-return is representable; `Read(o, h)` with an invocation and a response step; `Close(o, h)`; and the environment actions `ExtWrite`, `ExtDelete` and `Fault`.
- **Profile constants**: `OpenErrorTiming` and `StreamView`, each ranging over the same bounded sets as in Shortlist 1.
- **Properties**: one per clause, with TLC or P checker counterexample traces kept as the clause's evidence.

**Shortlist 3: "Normative prose + conformance suite + profile file."** Candidate g, disciplined by the § 2.3 rule. This is the baseline that most standards use (POSIX, Hadoop, WebAssembly, test262).

The spec is numbered clauses in structured prose with POSIX-style SYNOPSIS / ERRORS ("shall fail / may fail") sections and a K4 state table. The checkable artefact is a shared, read-only black-box conformance suite in which every test cites a clause ID. A per-reality profile file is read by the suite. No reference model is used.

*Why it is on the list.* It has the lowest authoring cost and the widest industrial precedent. It tests whether the extra machinery of Shortlists 1 and 2 earns its keep.

*Expected failure.*
- **Ambiguity in the multi-observer clauses.** Cosmos DB's documentation errors are the verified precedent; AUTOSAR's "optionally" is [not re-checked].
- **A suite stricter than the contract.** A test demanding one outcome where the clause allows several invites hard-coding (EvilGenie, ImpossibleBench).
- **Coarse profile flags** (the `is-blobstore` history in HADOOP-13502).
- **No oracle for K6** beyond hand-written race tests. Hadoop's own suite states that it does not cover concurrency.

*Running example.*
- The `open` entry gets an ERRORS list whose timing clause is "shall fail … at open | may fail at first read, as declared by profile key `open_error_timing`".
- The stream gets a state table.
- The concurrent-writer clause is one sentence with a ⟨VP⟩, plus a hand-written test per allowed branch.
- Fault-after-return is tested only where the harness has a shim.

### 7.3 Bake-off scoring criteria

*Inference, proposed design.* Each team, or agent, writes the same clause set for the running example in all three combinations, with semantics fixed beforehand by a human decision record. Score on the following.

| Criterion | Measurement | Principle |
|---|---|---|
| Expressiveness | Can each of the three hard cases be stated, plus "unspecified", "indeterminate", a narrowing profile, a request-or-refuse guarantee and a static-versus-runtime profile declaration? Each is scored yes/no with the clause shown. | § 3 |
| Mechanism leakage | Count of clauses that mention internal structure, buffering or request counts beyond what is declared as not promised (blind review) | P1 |
| Single home | Number of rules stated in more than one place; number of edits needed to change one environment action | P2 |
| Profile isolation | Contract lines touched when adding a new reality (target: 0); profile fields not read by any test; tests gated on non-profile flags or on backend-kind labels | P3 |
| Check coverage and strength | Share of clauses with an executing check; **kill rate of the per-clause counterexample mutants**; false alarms under deliberately nondeterministic clauses; whether outcome sets stay bounded under multiple faults | P4 |
| Unprimed implementation | N fresh agents implement from the spec alone; pass rate on a hidden, frozen suite plus mutation score | P5 |
| Ambiguity signal | Disagreement among N sampled implementations or tests per clause (ClarifyGPT method) | P2, P4 |
| Tamper resistance | Rate of spec or test edits by agents when checks are read-only versus writable (ImpossibleBench protocol); plus an EvilGenie-style case, in which a clause allows a set of outcomes and is checked by a single-outcome test | P4 |
| Agent authoring | Can an agent add a new clause plus its counterexample and check that a human reviewer accepts unchanged? | P5 |
| Cost | Author hours, reviewer hours, run time of checks, size of spec plus harness relative to the library. Baselines: ShardStore 12–13 % of the code base (≈ 20 % of the implementation; models ≈ 1 %); Cedar Lean models about a tenth of the Rust code, with a 3.4 : 1 proof-to-model ratio. | — |

---

## 8. Open questions and sources

### 8.1 Open questions

**Stream semantics.** The vocabulary exists, but the decision is the project's. Interval-linearizability, Lamport's safe, regular and atomic registers and Viotti–Vukolić's interval histories all give operations an extent. Hadoop and S3 state concurrent-read outcomes in boundary prose. Disconfirming search (c) therefore refutes the earlier claim that no framework models a stream as an operation with an extent. What remains open is narrower:
- whether the stream is one interval operation with one output, or per-chunk operations with a cross-chunk predicate;
- how the history checker records whichever is chosen;
- the fact that no framework ships a ready object type for a read yielding a sequence of partial outputs.

**The out-of-band observer.** Search (c) also found that rely–guarantee and TLA+ model an out-of-band actor natively, as environment state change, and that Jepsen separates the nemesis from clients. What no source does is distinguish O2 (a concurrent API caller) from O3 (an actor that may bypass library conventions) as two kinds of environment with different rights. Whether one rely clause suffices for both is open. S3's consistency section, for instance, is silent on its own lifecycle and replication actors.

**Liveness.** "Eventually returns or fails" cannot be required in plain interface automata. Modal and IOMTS theories can require outputs, but not finitely test them. A finite test needs a timeout assumption, which Tretmans names as such. The clause must be marked as checked by timeout assumption only.

**Missing measurements.** Disconfirming search (b) found controlled format comparisons only for single-shot LLM code generation (VeCoGen, the Gherkin pilot, compact encoding). None covers agents, EARS, decision tables or human readers. There is still no measured comparison of forms on the same category, no study of agents with per-reality profiles, and no drift study. The bake-off is where these measurements would come from.

**The form rule.** Disconfirming search (a) found coarse published heuristics (van Lamsweerde, NASA, Wing) but no validated rule. ISO/IEC/IEEE 29148, RTCA DO-333, Kotonya & Sommerville and Ardis et al. were not read, and any of them could contain a notation-per-requirement-type table.

**Remaining verification debt.**
- *Unreachable.*
  - Requirements and tables: Parnas & Madey 1995; Heitmeyer & Labaw and the NRL SCR overview; Lawford & Wassyng; EARS RE'09 figures; the Jama blog.
  - Language and theory sources: the Larch FAQ and JML RM ch. 9; the Event-B and ASM sources; the Benveniste monograph; Burckhardt's axiom names.
  - AWS and testing practice: the CACM 2015 print and CACM 2025 texts; Grieskamp et al. 2011; Hughes et al. 2016; the eWeek article.
  - Other: the OGC Modular Specification Policy; the TU Delft thesis.
- *Not re-checked.* Cirstea et al., TraceLink, PObserve, Porcupine, arXiv 2608.17388, FoundationDB, McKeeman, Jepsen MongoDB, WebKit, Eaton, arXiv 2409.14301, AUTOSAR's "optionally".
- *Not researched.* PyFilesystem2 error mapping.

**The 23 † items of the earlier edition.**
- *Dropped (17):* Alloy-style bounded checking; the POSIX ERRORS idiom; Jones 1983 (twice); OGC conformance classes; SQL isolation (three marks); JDBC; PathCapabilities; Femmer (twice); ShardStore mechanism (twice); the Benveniste refinement detail, now re-cited to RR-8147; Crooks; Barr.
- *Kept in part (4):* TLA+/Event-B, kept on Event-B; the model-oriented background paragraph and the § 3.10 row, kept on Event-B and ASM; the profile-wording item, kept on the OGC policy.
- *Kept in full (2):* the K1 ASM/Event-B precedent; Burckhardt's axiom names.

### 8.2 Sources

Grades as in the preamble. **(†)** marks a source that remains unverified background; **[unreachable]** and **[not re-checked]** as defined in the preamble.

| Source | Grade |
|---|---|
| [Carrizo, Dieste, Juristo, elicitation technique selection, WER 2008](https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf) | A (literature-derived framework, not a measured validation) |
| [van Lamsweerde, Formal Specification: a Roadmap, ICSE 2000](https://homepage.cs.uiowa.edu/~tinelli/classes/5810/Fall20/Papers/vLam00.pdf) | A (conceptual) |
| [NASA-GB-002-95 Formal Methods Guidebook vol. I](https://www.fing.edu.uy/inco/grupos/mf/TPPSF/Bibliografia/fmguide1.pdf); [NASA-GB-001-97 vol. II](https://ntrs.nasa.gov/api/citations/19980227975/downloads/19980227975.pdf) | B/C (agency guidance, no outcome data) |
| [Wing, A Specifier's Introduction to Formal Methods, 1990](https://www.cs.cmu.edu/~wing/publications/Wing90a.pdf) | A (conceptual) |
| [Jackson, Problem Analysis and Structure, 2000](https://stuff.mit.edu/afs/sipb/user/golem/papers/898/mj-marktoberdorf.pdf) | A/C |
| [Meyer 1992, Applying Design by Contract](https://www.kth.se/social/files/59526bfb56be5b4f17000807/meyer-92-contracts.pdf) | A (conceptual; magazine article) |
| [Eiffel exception mechanism docs](https://www.eiffel.org/doc/solutions/Exception_Mechanism) | B |
| [Leavens, Baker, Ruby, Preliminary Design of JML, TR 98-06j](https://dr.lib.iastate.edu/cs_techreports/136) | B (tech report) |
| [JML Reference Manual, 2nd ed. draft (2026)](https://www.openjml.org/documentation/JML_Reference_Manual.pdf); JML RM ch. 9 at cs.ucf.edu [unreachable] | B |
| [Dafny cheatsheet](https://dafny.org/v4.3.0/DafnyCheatsheet.pdf) | C |
| [SRC RR-58, Larch](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf); [Larch FAQ](https://www.cs.ucf.edu/~leavens/larch-faq.html) [unreachable] | B |
| [ACSL manual](https://frama-c.com/download/acsl.pdf) | B |
| [Barnett, Leino, Schulte, Spec#, CASSIS 2004](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/TheSpecSharpProgrammingSystem28CASSIS200429.pdf) | A |
| [.NET Code Contracts EnsuresOnThrow](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.contracts.contract.ensuresonthrow) | B |
| [Estler et al., Contracts in Practice, FM 2014](https://arxiv.org/pdf/1211.4775) | A |
| [VDM-10 Language Manual](https://raw.githubusercontent.com/overturetool/documentation/master/documentation/VDM10LangMan/VDM10_lang_man.pdf) | B |
| [Spivey, The Z Notation: A Reference Manual](https://spivey.oriel.ox.ac.uk/wiki/files/zrm/zrm.pdf) | A/B |
| [Atelier B, B Language Reference Manual](https://www.atelierb.eu/wp-content/uploads/2023/10/b-language-reference-manual.pdf) | B |
| Event-B refinement; Börger ASM ground model | † |
| [Liskov & Wing 1994, behavioural subtyping](https://www.cs.columbia.edu/~wing/publications/LiskovWing94.pdf) | A |
| [Strom & Yemini, typestate (IBM record)](https://research.ibm.com/publications/typestate-a-programming-language-concept-for-enhancing-software-reliability) | A |
| [DeLine & Fähndrich, Typestates for Objects](https://www.microsoft.com/en-us/research/publication/typestates-for-objects/) | A |
| [ETAPS Test-of-Time, session types](https://www.etaps.org/2019/test-of-time-award) | C page about an A paper |
| [de Alfaro & Henzinger, Interface Automata](https://research-explorer.ista.ac.at/record/4622) | A |
| [Lüttgen & Vogler, LMCS 9(3:4) 2013](https://arxiv.org/pdf/1306.3050v2) | A |
| [OMG UML14-209](https://issues.omg.org/issues/UML14-209) | C (issue tracker) |
| [Porres & Rauf, class contracts from PSMs](https://research.ucc.ie/en/publications/generating-class-contracts-from-deterministic-uml-protocol-statem/) | A |
| [Java AutoCloseable](https://cs-214.epfl.ch/jdk-21.0.9-docs/api/java.base/java/lang/AutoCloseable.html); [ConcurrentModificationException](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html) | B |
| [POSIX close(3p)](https://man.archlinux.org/man/close.3p.en) | B |
| [NetBSD PR 58929](https://gnats.netbsd.org/58929) | C (bug report) |
| [LWN reader comment on Rust close errors](https://lwn.net/Articles/1009302) | C |
| [async_fs::File](https://docs.rs/async-fs/1.1.2/async_fs/struct.File.html) | B |
| [ISO C N1570 (§ 3.4)](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) | B |
| [WG23 N0245](https://www.open-std.org/JTC1/SC22/WG23/docs/ISO-IECJTC1-SC22-WG23_N0245-revised-c-langague-annex-2010-03-23.pdf) | B (paraphrase; superseded as citation) |
| [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.txt) | B |
| [PEP 3116](https://peps.python.org/pep-3116/) | B (historical) |
| [Python io docs](https://docs.python.org/3/library/io.html); [CPython bufferedio.c](https://raw.githubusercontent.com/python/cpython/main/Modules/_io/bufferedio.c); [CPython iobase.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/39f6a0489fcc815a578d27dfee2feea003c896f8/Modules/_io/iobase.c) | B |
| [PEP 3151](https://peps.python.org/pep-3151/) | B |
| [Go io.go](https://raw.githubusercontent.com/golang/go/master/src/io/io.go); [errors/wrap.go](https://raw.githubusercontent.com/golang/go/master/src/errors/wrap.go); [io/fs](https://raw.githubusercontent.com/golang/go/master/src/io/fs/fs.go) | B |
| [Google AIP-193](https://google.aip.dev/193); [AIP-194](https://google.aip.dev/194) | B |
| [gRPC status codes](https://grpc.io/docs/guides/status-codes/); [Rust io::ErrorKind](https://doc.rust-lang.org/nightly/std/io/enum.ErrorKind.html) | B |
| Parnas & Madey, Functional documents for computer systems, SCP 25 (1995) [unreachable]; [McMaster record (actually Parnas 2010)](https://experts.mcmaster.ca/scholarly-works/2169098) | A (unread) / A |
| [NRL SCR overview](https://apps.dtic.mil/sti/pdfs/ADA465161.pdf); [Heitmeyer & Labaw](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf) [unreachable] | B/C (NRL technical reports) |
| [Heitmeyer, Marktoberdorf 2010 slides](https://asimod.in.tum.de/2010/slides/heitmeyer/Heitmeyer2-Markt2010.pdf) | C |
| [Zave FRE page](https://pamelazave.com/fre.html) | A (paper; summary page read) |
| [Lawford, Froebel & Moum, tabular methods for the Darlington SDS](https://www.cas.mcmaster.ca/~lawford/papers/tables.pdf); [Lawford & Wassyng](https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf) [unreachable] | B / A (unread) |
| [EARS, Mavin et al., RE'09](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/) (figures [unreachable]) | A (weak, single case) |
| [Mavin, EARS guide](https://alistairmavin.com/ears/) | C |
| [Salari et al., EARS experiment](https://www.ipr.mdu.se/pdf_publications/6673.pdf) | A-weak (n = 10) |
| [Jama EARS webinar](https://www.jamasoftware.com/blog/webinar-recap-adopting-ears-notation-to-improve-requirements-engineering) [unreachable] | D |
| [Femmer et al., requirements smells, JSS 2017](https://arxiv.org/pdf/1611.08847) | A |
| [Frattini et al., ambiguity experiment](https://arxiv.org/pdf/2401.01154v2) | A |
| [Watt, mechanising WebAssembly](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf); [WasmCert-Coq](https://spiral.imperial.ac.uk/entities/publication/ecf384fa-0800-4dc3-b5ef-a5aac822610e) | A |
| [WebAssembly 3.0 profiles appendix](https://webassembly.github.io/spec/core/appendix/profiles.html) | B |
| [Cedar, How We Built Cedar, FSE Companion 2024](https://arxiv.org/pdf/2407.01688) | A |
| [SQLite testing](https://sqlite.org/testing.html) | B |
| [ShardStore, SOSP 2021 (Amazon Science copy)](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf) | A |
| [Newcombe et al., AWS TLA+, 2014 draft of CACM 58(4)](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) | B |
| [Brooker & Desai, CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services) [unreachable] | B |
| [AUTOSAR QuickCheck](https://research.chalmers.se/en/publication/219899) | A/B (abstract only; self-reported counts) |
| [Goldstein et al., PBT in practice, ICSE 2024](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf) | A |
| [Jones 1983, rely–guarantee, TOPLAS](https://ilyasergey.net/CS6213/_static/05-owicki/rg.pdf) | A |
| [Abadi & Lamport, Composing](https://www.microsoft.com/en-us/research/publication/composing-specifications/); [Conjoining (author copy)](https://lamport.azurewebsites.net/pubs/abadi-conjoining.pdf) | A |
| [Lamport, Specifying Systems](https://lamport.azurewebsites.net/tla/book-02-08-08.pdf) | A (author's book) |
| [Benveniste et al., INRIA RR-8147](https://inria.hal.science/hal-00757488/document); [RR-6214](https://arxiv.org/pdf/0706.1456); [Contracts for System Design monograph](https://nowpublishers.com/article/Details/EDA-053) [unreachable] | A/B (reports) / A (unread) |
| [FME review of Benveniste et al.](https://fmeurope.org/2020/10/30/book-review-contracts-for-system-design/) | C |
| [Herlihy & Wing, linearizability](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf) | A |
| [Lamport, On Interprocess Communication](https://lamport.azurewebsites.net/pubs/interprocess.pdf) | A |
| [Castañeda, Rajsbaum, Raynal, interval-linearizability](https://arxiv.org/pdf/1507.00073) | A-pre as read |
| [Substep linearizability](https://arxiv.org/pdf/2610.16099) | A-pre |
| [Adya thesis](https://www.aphyr.com/data/posts/294/adya-phd.pdf) | A |
| [Elle, PVLDB 14(3)](https://arxiv.org/pdf/2003.10554) | A |
| [Viotti & Vukolić, ACM CSUR 2016](https://arxiv.org/pdf/1512.00168) | A |
| [Burckhardt, Principles of Eventual Consistency (MSR copy)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/final-printversion-10-5-14.pdf) | A (axiom names †) |
| [Crooks et al., Seeing is Believing, PODC 2017](https://par.nsf.gov/servlets/purl/10077635) | A |
| [Terry et al., session guarantees](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf) | A |
| [Lynch, I/O automata retrospective](https://arxiv.org/pdf/2502.20468) | A-pre |
| [Desai et al., P language, PLDI 2013 (author copy)](https://ankushdesai.github.io/assets/papers/p.pdf) | A |
| [Hackett et al., Cosmos DB TLA+, ICSE-SEIP 2023](https://arxiv.org/pdf/2210.13661) | A/B |
| [Jepsen MongoDB 4.2.6](https://jepsen.io/analyses/mongodb-4.2.6) [not re-checked] | A/B (measured, not peer-reviewed) |
| [Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md); [tutorial ch. 3](https://raw.githubusercontent.com/jepsen-io/jepsen/main/doc/tutorial/03-client.md); [tutorial ch. 5](https://raw.githubusercontent.com/jepsen-io/jepsen/main/doc/tutorial/05-nemesis.md); [Knossos README](https://raw.githubusercontent.com/jepsen-io/knossos/master/README.md) | C |
| [Tretmans 2008, model-based testing with labelled transition systems](https://repository.ubn.ru.nl/bitstream/handle/2066/72680/72680.pdf) | A |
| [Beohar & Mousavi, spinal test suites](https://arxiv.org/pdf/1403.7260) | A (secondary for ioco) |
| [Grieskamp et al., Spec Explorer, STVR 2011](https://repositoriosdigitales.mincyt.gob.ar/vufind/Record/CONICETDig_c68bda0856b57e85543ae9443287fe53) [unreachable] | A (unread) |
| [Grieskamp, SambaXP 2008 slides](https://sambaxp.org/archive_data/sxp08/SambaXP2008-DATA/00-05-Wolfgang_Grieskamp-MBT.pdf) | C |
| [eWeek Spec Explorer](https://www.eweek.com/development/microsoft-delivers-its-spec-explorer-model-based-testing-tool) [unreachable] | D (figure dropped) |
| [Hughes et al., Dropbox testing, ICST 2016](https://www.cis.upenn.edu/~bcpierce/papers/mysteriesofdropbox.pdf) [unreachable] | A (unread) |
| [TorXakis README](https://raw.githubusercontent.com/TorXakis/TorXakis/develop/README.md); [arXiv 2102.00378](https://arxiv.org/pdf/2102.00378) | C / A-pre |
| [Porcupine](https://pkg.go.dev/github.com/anishathalye/porcupine) [not re-checked] | C |
| [Linearizability checker comparison](https://arxiv.org/pdf/2608.17388) [not re-checked] | A-pre |
| [Eaton on linearizability checking](https://notes.eatonphil.com/2024-10-31-checking-linearizability-in-go.html) [not re-checked] | C |
| [FoundationDB simulation](https://cacm.acm.org/?p=227399) [not re-checked] | A |
| [McKeeman, differential testing](https://dblp.org/pid/40/4856) [not re-checked] | A/B |
| [Chen, Cheung & Yiu, metamorphic testing, 1998 TR](https://arxiv.org/abs/2002.12543); [HKU record](https://hub.hku.hk/handle/10722/254895) [unreachable] | B (tech report) / A (unread) |
| [Barr et al., oracle problem, TSE 2015 (author copy)](http://www0.cs.ucl.ac.uk/staff/M.Harman/tse-oracle.pdf) | A |
| [Cirstea et al., TLA+ trace validation](https://arxiv.org/pdf/2404.16075) [not re-checked] | A |
| [Multi-grained specifications](https://arxiv.org/pdf/2409.14301) [not re-checked] | A-pre |
| [TraceLink, OOPSLA 2025](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf) [not re-checked] | A |
| [Alloy 6](https://alloytools.org/alloy6.html) | C (tool docs) |
| [WebKit wasm spec test translation](https://webkit.googlesource.com/WebKit/+/5d26c89f08b81b8e08741577e164b9ab0701d9eb/JSTests/wasm/spec-tests/stack.wast.js) [not re-checked] | C |
| [POSIX unistd.h, Issue 8](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/unistd.h.html); [Issue 6 mirror](https://www.gaertner.de/~neitzel/susv3/basedefs/unistd.h.html); [XSH 2.3](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html); [read()](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html) | B |
| [W3C Variability in Specifications](https://www.w3.org/TR/2005/NOTE-spec-variability-20050831/) | B |
| [OGC API-Features 17-069r4](https://docs.ogc.org/is/17-069r4/17-069r4.html); OGC Modular Specification Policy 08-131r3 [unreachable] | B |
| [JDBC DatabaseMetaData, Java 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/DatabaseMetaData.html) | B |
| [SQL-92 draft text (unofficial mirror)](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt) | B |
| [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | B |
| [Berenson et al., A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) | A (partial order only) |
| [Hadoop testing the FS contract](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/testing.html); [filesystem.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html); [openfile.html](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/filesystem/openfile.html); [fsdatainputstream.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/fsdatainputstream.html); [pathcapabilities.html](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/pathcapabilities.html) | B |
| [HADOOP-13502](https://issues.apache.org/jira/rest/api/2/issue/HADOOP-13502); [HADOOP-13501](https://issues.apache.org/jira/rest/api/2/issue/HADOOP-13501) | C |
| [AWS S3 User Guide, consistency model](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) | B |
| [fsspec spec.py](https://raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/spec.py); [Arrow filesystem.h](https://raw.githubusercontent.com/apache/arrow/main/cpp/src/arrow/filesystem/filesystem.h) | B/C (project source, no data) |
| [OpenDAL RFC 2852](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/2852_native_capability.md) | B/C |
| [OpenDAL RFC 6707](https://docs.rs/crate/opendal-core/0.58.1/source/src/docs/rfcs/6707_capability_override_layer.md) | C |
| [Vericoding benchmark, TMLR](https://arxiv.org/pdf/2509.22908v1) | A |
| [Vericoding audit, NeurIPS 2026 workshop](https://openreview.net/forum?id=Z2WDY7LQ8s) | A-workshop (abstract only) |
| [Verus proof synthesis cheating](https://arxiv.org/pdf/2602.04910v3) | A-pre |
| [DafnyBench, TMLR 2025](https://arxiv.org/pdf/2406.08467v1) | A |
| [LLM TLA+ generation, ICSOFT 2026](https://arxiv.org/pdf/2606.05792v1) | A |
| [TLA+-Bench](https://arxiv.org/pdf/2607.23425v1) | A-pre |
| [nl2postcond, FSE 2024](https://arxiv.org/pdf/2310.01831v2) | A |
| [Clover, SAIV](https://arxiv.org/pdf/2310.17807v4) | A |
| [SpecGen, ICSE 2025](https://arxiv.org/pdf/2401.08807v5) | A |
| [TiCoder, IEEE TSE 2024](https://arxiv.org/pdf/2404.10100) | A |
| [Mathews & Nagappan, TDD for codegen, ASE 2024](https://arxiv.org/pdf/2402.13521v2) | A |
| [LLM property-based tests](https://arxiv.org/pdf/2307.04346v2) | A-pre |
| [ImpossibleBench, ICLR 2026](https://arxiv.org/pdf/2510.20270v1) | A |
| [ImpossibleBench audit](https://www.lesswrong.com/posts/qnrjAhiqire7JeoN2/good-evals-are-hard-an-impossiblebench-audit) | C |
| [EvilGenie](https://arxiv.org/pdf/2511.21654v2) | A-pre |
| [SWE-bench patch correctness, ICSE 2026](https://arxiv.org/pdf/2503.15223v2) | A |
| [Oracles capture actual vs expected behaviour (v2)](https://arxiv.org/pdf/2410.21136v2) | A-pre |
| [Oracle generation on buggy code, AIware 2025](https://arxiv.org/pdf/2601.05542v1) | A |
| [AugmenTest](https://arxiv.org/html/2501.17461v1) | A-pre |
| [TU Delft oracle thesis](https://repository.tudelft.nl/record/uuid:f3877914-bd2e-4007-945b-c0db271d27c8) [unreachable] | A-thesis |
| [Lost in the Middle, TACL 2024](https://aclanthology.org/2024.tacl-1.9/) | A |
| [Chroma Context Rot](https://research.trychroma.com/context-rot) | B |
| [Evaluating AGENTS.md, ICLR 2026 workshops](https://arxiv.org/pdf/2602.11988v3) | A-workshop |
| [When Prompts Go Wrong, ICSE 2026](https://arxiv.org/pdf/2507.20439v1) | A |
| [ConInstruct, AAAI 2026](https://arxiv.org/pdf/2511.14342v2) | A |
| [ClarifyGPT, FSE 2024](https://arxiv.org/pdf/2310.10996v1) | A |
| [Structured specs / Gherkin pilot, FSE Companion '26](https://arxiv.org/pdf/2605.02455v1) | A (weak: pilot) |
| [VeCoGen, FormaliSE 2025](https://arxiv.org/pdf/2411.19275v3) | A (n = 15) |
| [Compact Constraint Encoding](https://arxiv.org/abs/2604.07192) | A-pre (abstract only) |
| [ContractEval](https://arxiv.org/abs/2510.12047) | A-pre (abstract only) |
| [When Specifications Conflict](https://arxiv.org/pdf/2607.28384v1) | A-pre |
| [Requirement smells and code generation, PROFES 2026](https://arxiv.org/pdf/2609.29208) | A |
| [METR reward hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking) | B/C |
| [Anthropic C compiler](https://www.anthropic.com/engineering/building-c-compiler) | B (uncontrolled) |
| [Böckeler on SDD tools](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) | C |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | C/D (not re-read) |
| [ssojet SDD blog](https://ssojet.com/blog/best-spec-driven-development-tools) | D (not re-read) |

---

## Conclusion

Verification left the shape of the answer intact and moved its weight. The architecture held up against the full texts:
- one assume–guarantee contract;
- typestates and an environment clause;
- history predicates;
- narrow-only profiles;
- a form chosen per quantifier.

Where the earlier edition reported gaps, the verified texts mostly show vocabulary the survey had missed:
- interval operations and register semantics for long reads;
- environment-as-state-change for out-of-band actors;
- normative narrow-only rules in SQL-92 and WebAssembly;
- coarse published heuristics for choosing a form.

The genuine open points are now smaller and sharper: how to record a chunked stream, whether O2 and O3 need different rights, and whether bounded outcome sets are tractable under several faults. The best-evidenced industrial practice, ShardStore, avoided exactly that last question.

The agent evidence, read correctly, says the same thing more forcefully. Agents fail where a check is editable, derived from the code, or **stricter than the spec it claims to enforce**. The last case turns "unspecified is a statement" from a principle into a test requirement: an oracle must accept exactly the set the clause allows, no more and no less. No study yet shows that the notation of the normative text matters to agents; adding executable content does. The bake-off's job is therefore narrower than it first appeared. It does not need to find the best notation. It needs to show which combination keeps the per-clause counterexamples executable, the outcome sets bounded and the checks frozen.
