# Specification categories, levels of abstraction, and forms: how established practice picks a form per category

Notes on method:
- Grades: **A** = peer-reviewed and/or measured; **B** = industrial practice with data; **C** = practitioner report, no data; **D** = opinion or marketing.
- Fetch limits: WebFetch and curl to arxiv.org, acm.org, sqlite.org and queue.acm.org were blocked in this session (DNS failure or proxy 403). Findings marked "(search-verified)" come from search-engine extracts of the primary source. Findings marked "[not verified this session]" are well-known descriptions of primary sources taken from prior knowledge. They link to the canonical primary URL, but I could not re-read them here, so the report writer should treat their specific numbers or wording as needing a check.
- The project's candidate categories are written C1 to C7: C1 structure, C2 pure function, C3 single call (pre/post/errors), C4 resource lifecycle, C5 concurrent environment / multiple observers, C6 error classification, C7 per-backend profile.

---

## Q1. Which established taxonomies separate specification categories, and where do they draw the lines?

### Takeaway
No established taxonomy uses the project's exact categories. The strongest lines in the literature fall along two axes. (1) **What is described**: the environment and requirements, the machine's interface behaviour, or the design (Parnas–Madey, Jackson/Zave). (2) **State and time**: static structure, a single state transition, or behaviour over traces and concurrency (Larch two-tier, ASM/Event-B refinement, TLA+). Most of C1–C7 can be derived from these two axes. C6 (error classification) and C7 (per-backend profile) look like cross-cutting *dimensions* rather than categories of their own (inference).

### Cited Findings
- **Parnas & Madey four-variable model (A).** Required behaviour is written as relations over *monitored* and *controlled* environment quantities: REQ relates the history of M to C, NAT gives the environment's constraints, IN maps M to inputs I, and OUT maps outputs O to C. The model separates the requirement (REQ/NAT) from the software's I/O design (IN/OUT). Published as "Functional documents for computer systems", *Sci. Comput. Program.* 25 (1995) 41–61. — [McMaster Experts record](https://experts.mcmaster.ca/scholarly-works/2169098); [NRL SCR overview, DTIC](https://apps.dtic.mil/sti/pdfs/ADA465161.pdf) (search-verified)
- The four-variable model was created to give a formal basis to the SCR / A-7E requirements work. A "six-variable" extension adds environment quantities that existed before design decisions were made. — [Ulfat-Bunyadi et al., Six-Variable Model, MODELSWARD 2016](https://www.scitepress.org/Papers/2016/59441) (A, search-verified)
- **Zave & Jackson, "Four dark corners of RE", ACM TOSEM 6(1), 1997 (A).** All RE descriptions should be descriptions of the *environment*. Requirements, specifications and domain knowledge are distinct kinds of description, and the paper defines what it means for RE to be complete. The completion criterion is usually written S, K ⊢ R, but I could not confirm that notation from a fetched source. — [Zave's FRE page](https://pamelazave.com/fre.html); [bibsonomy record](https://bibsonomy.org/bibtex/b86b10370cf3feded361cf7955bc3be6) (search-verified)
- Follow-up critique (A): Jureta, Mylopoulos & Faulkner argue the Zave–Jackson ontology is incomplete because it omits stakeholder attitudes such as beliefs and desires. — [arXiv 0811.4364](https://arxiv.org/abs/0811.4364v1) (search-verified)
- **Jackson, Problem Frames (A/C, book).** Problems are classified by recurring "frames", including required behaviour, commanded behaviour, information display, simple workpieces and transformation. Each frame comes with its own descriptions of domains and phenomena. The *transformation* frame corresponds to C2 and the *workpieces* frame to C1/C3. — [not verified this session] [Jackson, Problem Frames, Addison-Wesley 2001 — Google Books](https://books.google.com/books?id=8fqIP83Q2IAC)
- **Larch two-tier (A).** A *shared tier* (Larch Shared Language: algebraic, state-free theories of values and sorts) is kept separate from an *interface tier* (one per language, e.g. LCL for C or Larch/C++): pre/post/modifies clauses per procedure that refer to shared-tier vocabulary. This matches the split between C1/C2 (values, pure functions) and C3 (per-call state change). — [not verified this session] [Guttag & Horning, *Larch: Languages and Tools for Formal Specification*, Springer 1993 (DOI)](https://doi.org/10.1007/978-1-4612-2704-5)
- **Abstract State Machines (A).** Börger's "ground model" is the first, closest-to-the-domain ASM. It is checked by *inspection* against the informal requirements, and by *validation* when executed, and only after that is it refined stepwise toward code. The method treats choosing the level of abstraction as something to justify ("ground model" vs refinements) rather than a fixed choice. — [not verified this session] [Börger, "The ASM Ground Model Method as a Foundation of Requirements Engineering", LNCS 2772, 2003](https://doi.org/10.1007/978-3-540-39910-0_6)
- **Event-B (A).** The model is built by successive refinement steps, each introducing more state or events and discharging proof obligations against the abstract machine. The "level" is therefore whichever refinement step a property first becomes expressible at. — [not verified this session] [Abrial, *Modeling in Event-B*, CUP 2010](https://doi.org/10.1017/CBO9781139195881)
- **ISO/IEC/IEEE 29148 (standard; graded C because it is normative but has no data).** It separates stakeholder, system and software requirement specifications, and lists characteristics of good individual requirements (necessary, unambiguous, verifiable, singular, etc.). It classifies requirements as functional, performance, interface, and so on, but it does **not** prescribe a notation per class. — [not verified this session] [ISO catalogue page, 29148:2018](https://www.iso.org/standard/72089.html)

### Inferences
- *Inference:* The project's existing structure spec (one instant, no operations) is Larch's shared tier / Problem-Frames "workpiece" structure, or the state space of an ASM/Event-B machine. The black-box behaviour specs it now needs are the interface tier (C3), plus trace-level descriptions (C4, C5) that Larch never covered well and that TLA+, ASM and Event-B do cover.
- *Inference:* Read through the four-variable model, a library-over-backends API sits at the IN/OUT boundary of the library and the REQ boundary of the caller. Each backend has its own "NAT" (C7). That suggests modelling a per-backend profile as a parameterisation of the environment assumptions, not as a separate kind of spec.
- *Inference:* Error classification (C6) appears in none of these taxonomies as a category of its own. It shows up as part of the post/exception clauses of C3 (Larch, JML-style specs) and as part of the observable alphabet of C4/C5.

### Gaps
- I could not fetch any full text of Parnas–Madey, Zave–Jackson, Larch, Börger or ISO 29148. Exact definitions and wording are unconfirmed in this session.
- I found no standard that defines categories that map one-to-one onto C1–C7.

---

## Q2. Measured evidence on structured natural-language and tabular forms

### Takeaway
The evidence for structured natural language is mostly qualitative, from the originators (EARS). Tabular expressions have the strongest record in a safety-critical setting (A-7E, Darlington), but the published cost data is thin. The concrete payoff of tables is that mechanical *completeness and disjointness* checks become possible: reviewers otherwise spend their effort on exactly those checks.

### Cited Findings
- **EARS (A, weak).** Mavin et al., RE'09 (Rolls-Royce). The rules target eight common problems of natural-language requirements, including ambiguity, complexity and vagueness, and allow every requirement to be written in one of five templates (ubiquitous, event-driven, state-driven, unwanted-behaviour, optional-feature). The evaluation was a single case: requirements extracted from an aero-engine airworthiness regulation. It reports "qualitative and quantitative improvements" over conventional text. I could not retrieve the actual numbers. — [Univ. of Manchester research record](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/); [Wikipedia summary](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax) (search-verified)
- **EARS follow-up (C).** "Listens Learned (8 Lessons Learned Applying EARS)", RE 2016: four experienced practitioners reflect on six years of use across domains. The lessons are qualitative, with no controlled measurement. — [IEEE record via infona](https://www.infona.pl/resource/bwmeta1.element.ieee-art-000007765533) (search-verified)
- Claims that EARS "drastically reduces or eliminates" natural-language problems come from vendor material (D) and should not be weighted. — [Jama Software webinar recap](https://www.jamasoftware.com/blog/webinar-recap-adopting-ears-notation-to-improve-requirements-engineering)
- **RFC 2119 / RFC 8174 (standard, C).** These define the MUST / SHOULD / MAY keywords. RFC 8174 clarifies that only UPPERCASE forms carry the defined meaning. They standardise *obligation strength*. They do not standardise structure or checkability, and I found no measured evidence on their effect. — [not verified this session] [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- **Requirement smells (A).** Femmer et al., "Rapid quality assurance with Requirements Smells", *JSS* 2017: automated detection of linguistic smells (vague terms, passive voice, etc.). My search for its precision figures failed, so they are unconfirmed here. — [not verified this session] [arXiv 1611.08847](https://arxiv.org/abs/1611.08847)
- **Darlington shutdown system (B).** In 1987 the Canadian regulator was concerned the trip-logic software was not properly engineered. Parnas advised, and Ontario Hydro rendered both requirements and code into tabular form and produced proofs that they matched (the station came online in 1990). — [Bill Kelly (OPG) slides, Queen's](https://research.cs.queensu.ca/home/cisc323/2006w/slides/BillKelly.pdf) (C, search-verified)
- **Darlington redesign (A).** The later Systematic Design Verification process used tabular expressions in the requirements and design documents and was based on the four-variable model. Tools generated "block theorems" for PVS, which verified most functional requirements. The authors note that the original project had to *reverse-engineer* tabular specs to win regulatory approval. — [Lawford & Wassyng, "Formal Verification of Nuclear Systems: Past, Present, and Future", ISIJ 28 (2012)](https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf); [Lawford et al., tables paper](https://www.cas.mcmaster.ca/~lawford/papers/tables.pdf) (search-verified)
- **Why tables help (A).** Heitmeyer & Labaw (NRL, 1993), citing Parnas: reviewers "spent too much of their time and effort checking for simple, application-independent properties" such as domain coverage, at the expense of safety-relevant issues. Automated consistency and completeness checking of SCR tables removes that burden. — [DTIC ADA276077](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf) (search-verified)

### Inferences
- *Inference:* Structured natural language (EARS, RFC 2119, Gherkin) mainly improves *readability and consistency of phrasing*. It does not make the semantics machine-checkable. Tables add mechanical completeness/disjointness checks over a finite case split, which is why they suit C3 error and precondition partitions and C6 error classification.
- *Inference:* The Darlington evidence supports tables for *pure input→output functions with mode/case splits* (C2, C3). It is not evidence for concurrency (C5).

### Gaps
- No quantitative EARS numbers were retrieved, and I found no controlled experiment comparing EARS with plain text.
- I found no measured study of Gherkin/BDD defect detection, and no study of RFC 2119 keyword effects.
- I retrieved no cost figures (person-years) for Darlington or A-7E table inspection.

---

## Q3. Executable specifications used as standards: what each made checkable, and at what cost

### Takeaway
Mature standards use **layered** forms. Normative prose or pseudo-code is accompanied by an executable reference (interpreter or model) and a large conformance suite. In some cases a mechanised formal semantics proves meta-properties, and those mechanisations repeatedly found real errors in the prose spec (Wasm, Cedar). Differential testing of the implementation against an executable model is the recurring bridge between a formal model and production code.

### Cited Findings
- **WebAssembly (A).** Watt's Isabelle mechanisation (about 11,000 lines) of the draft spec, with a verified executable interpreter and type checker, found "syntactic" errors (typos, malformed constraints, missing cases) and deeper "semantic" errors (well-typed programs getting stuck, JS/host interop soundness). The semantic errors surfaced during the soundness proof and led to official corrections. — [Watt, CPP 2018 paper](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf); [Watt slides](https://wp.doc.ic.ac.uk/vetss/wp-content/uploads/sites/122/2019/10/Watt-WebAssembly-slides.pdf); [Watt thesis](https://www.repository.cam.ac.uk/handle/1810/329032) (search-verified)
- The WasmCert-Coq mechanisation also "discovered and helped fix several errors" in the spec. — [Imperial record](https://spiral.imperial.ac.uk/entities/publication/ecf384fa-0800-4dc3-b5ef-a5aac822610e) (A, search-verified)
- The official Wasm spec itself combines prose, formal inference-rule notation, an OCaml reference interpreter, and a shared test suite. — [not verified this session] [WebAssembly/spec repository](https://github.com/WebAssembly/spec)
- **AWS Cedar (A).** Built by "verification-guided development": a formal model (first Dafny, later Lean) with proofs, plus differential random testing (DRT) of the Rust implementation against the model, plus property-based testing (PBT). Proofs found 4 soundness bugs in the validator. DRT and PBT found 21 more bugs in the parser, evaluator, authorizer and validator. DRT generates millions of inputs (policies, entities, requests) and checks that model and production agree. — [Disselkoen et al., FSE 2024 Industry, arXiv 2407.01688](https://arxiv.org/pdf/2407.01688); [Amazon Science record](https://www.amazon.science/publications/how-we-built-cedar-a-verification-guided-approach) (search-verified). Lines-of-code and effort figures from the paper were not retrievable (fetch blocked).
- **SQLite (B).** The TH3 harness gives 100% branch coverage and 100% MC/DC of the core library. TH3 is about 1055.4 KSLOC of C implementing 50,362 distinct test cases, about 2.4 million test instances for a full-coverage run and about 248.5 million in the pre-release soak. 100% MC/DC was reached on 2009-07-25, motivated by DO-178B. TH3 is proprietary. Coverage of extensions (FTS, RTREE) is below 100%. — [sqlite.org/th3.html](https://sqlite.org/th3.html); [sqlite.org/testing.html](https://sqlite.org/testing.html) (search-verified). The commonly quoted test-to-source ratio ("590×") was **not** confirmed. sqllogictest (differential comparison of query results against other SQL engines) is documented on testing.html, but I could not read the details.
- **ShardStore / Amazon S3 (A).** Uses *executable reference models* written in Rust as the specification, with the implementation checked against them by PBT, stateful model-based testing, and model checking of crash consistency and concurrency. The authors explicitly reject full verification in favour of automation and keeping the specs current. ShardStore is about 40k LoC of Rust. 16 issues, including subtle crash-consistency and concurrency bugs, were prevented from reaching production, and the approach was extended by engineers without a formal-methods background. — [Bornholt et al., SOSP 2021 (best paper)](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf); [Amazon Science blog](https://amazon.science/blog/aws-team-wins-best-paper-award-for-work-on-automated-reasoning) (search-verified)
- **Ethereum execution-specs (C).** The Ethereum execution layer is specified as a readable Python reference implementation, one module per fork, used together with shared consensus test fixtures. — [not verified this session] [ethereum/execution-specs](https://github.com/ethereum/execution-specs)
- **ECMAScript / test262 (C).** The ECMAScript spec is written as numbered algorithm steps in prose. test262 is the official conformance suite, with tests tied to spec sections. Normativity stays with the prose, and executable checkability comes from the suite. — [not verified this session] [tc39/test262](https://github.com/tc39/test262)
- **WHATWG HTML (C).** Behaviour is written as imperative algorithms in prose, with RFC 2119 keywords. Conformance is checked through the shared web-platform-tests suite. — [not verified this session] [HTML Standard](https://html.spec.whatwg.org/multipage/); [web-platform-tests](https://github.com/web-platform-tests/wpt)
- **POSIX (C).** Interfaces are specified per function in prose sections (SYNOPSIS, DESCRIPTION, RETURN VALUE, ERRORS). The ERRORS section enumerates errno values with "shall fail" and "may fail" conditions. This is a standard template that combines C3 and C6, and it explicitly allows implementation-defined variance, which corresponds to C7 per-backend profiles. — [not verified this session] [POSIX.1-2017 open()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/open.html)
- **Ferrocene Language Specification (C).** A prose specification of Rust, written for safety qualification, with paragraph-level identifiers that tests and traceability can reference. — [not verified this session] [Ferrocene spec](https://spec.ferrocene.dev/)
- **Python (C).** The language reference is prose. Conformance in practice is defined by CPython's test suite (the de facto oracle for alternative implementations). — [not verified this session] [Python Language Reference](https://docs.python.org/3/reference/)

### Inferences
- *Inference:* A recurring pattern appears across Wasm, Cedar, ShardStore, Ethereum and SQLite. **Normative description** (prose, pseudo-code, or a formal model) plus an **executable oracle** (a reference interpreter or model) plus **generated or shared tests** (a conformance suite, DRT, or PBT). The normative form differs, and the checkable artefact is always executable.
- *Inference:* Mechanised formal semantics paid off mainly for *meta-properties* (type soundness, validator soundness), not for ordinary per-call behaviour. Per-call behaviour was checked more cheaply by differential testing against the model.
- *Inference:* The POSIX ERRORS-section idiom ("shall fail" vs "may fail" with an enumerated condition per errno) is a direct precedent for combining C3/C6 with C7 variance in a single table.

### Gaps
- I retrieved no cost figures for Wasm (person-months), test262 size, or the Ethereum execution-specs.
- Cedar's model and proof line counts and its effort were not retrievable (arxiv fetch blocked).

---

## Q4. Industrial cost/benefit data for lightweight formal methods and property-based testing

### Takeaway
The best-documented industrial data (AWS TLA+/P, ShardStore, Cedar, Volvo/AUTOSAR QuickCheck) consistently shows that model checking or PBT finds concurrency, crash and protocol bugs, and spec ambiguities, that conventional tests miss, at a learning cost of weeks. Bug counts are self-reported by the practitioners. I found no controlled cost comparisons.

### Cited Findings
- **AWS TLA+, 2015 (B).** Used on 10 large, complex systems. In every case it added significant value, either by finding subtle bugs they believed other methods would have missed, or by giving the confidence to make aggressive performance optimisations. Engineers from entry level to Principal learned TLA+ and got useful results in 2–3 weeks. PlusCal is positioned as a direct replacement for pseudo-code. — [Newcombe et al., CACM 58(4), 2015 (MIT-hosted PDF)](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf); [Amazon Science record](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods); [Colyer summary](https://blog.acolyer.org/2014/11/24/use-of-formal-methods-at-amazon-web-services/) (search-verified). The often-quoted DynamoDB "35-step trace" detail was **not** confirmed.
- **AWS 2025 (B/C).** Brooker & Desai, CACM 68(6), June 2025: AWS moved from build-time unit tests (often against mocks) to a portfolio of TLA+, the P state-machine language, PBT, fault injection and deterministic simulation. TLA+ "identif[ies] and eliminate[s] subtle bugs early ... that would have eluded traditional approaches such as testing". — [CACM practice article](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services); [ACM Queue version](https://queue.acm.org/detail.cfm?id=3712057) (search-verified; full text not readable). More than 100 TLA+ models have been created inside Amazon. — [TLA+ Conf 2023 talk page](https://conf.tlapl.us/2023/dragoischwiderski/) (C)
- **ShardStore (A):** 16 issues prevented from reaching production, using reference models plus PBT plus model checking, maintained by non-specialists. — [SOSP 2021](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf)
- **Cedar (A):** 4 bugs from proofs and 21 from DRT/PBT. — [arXiv 2407.01688](https://arxiv.org/pdf/2407.01688)
- **QuickCheck at Volvo/AUTOSAR (A/B).** More than 3,000 pages of textual AUTOSAR specs were translated into QuickCheck state-machine models and used to test implementations from 6 suppliers. This exposed more than 200 issues and 100+ problems in the *standard itself*. The authors call the approach more efficient, effective and correct than the previous manual approach. A recurring failure mode was ambiguous prose, e.g. a callback that is "optionally" called. — [Mondal/Hughes et al., "Testing AUTOSAR software with QuickCheck", ICSTW 2015](https://research.chalmers.se/en/publication/219899); [Hughes, Erlang Factory slides](https://www.erlang-factory.com/upload/presentations/582/CertifyingyourcarwithErlang.pdf); [Hughes, "Experiences with QuickCheck", 2016](https://research.chalmers.se/en/publication/232550) (search-verified; the counts are self-reported)
- **PBT in practice (A).** Goldstein et al., ICSE 2024, 30 interviews at Jane Street. PBT is strong for complex code and for confidence beyond example tests, and most uses fall into a small number of high-leverage idioms (e.g. differential/model-based oracles and round-trips). The costs: writing properties and generators is complex, and judging test effectiveness is hard. — [Penn PDF](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice); [DOI](https://doi.org/10.1145/3597503.3639581) (search-verified)
- **Survey of industrial formal methods (A).** Woodcock, Larsen, Bicarregui & Fitzgerald, "Formal Methods: Practice and Experience", *ACM Comput. Surv.* 41(4), 2009: a survey of industrial projects, with emphasis on formal methods in early specification and design. Its project questionnaire data was not retrieved here. — [draft PDF](https://homepage.divms.uiowa.edu/~tinelli/classes/181/Fall20/Papers/Wood09.pdf) (search-verified)

### Inferences
- *Inference:* Across cases the evidence is that **model checking (TLA+/P) pays off for C5** (concurrency, distributed protocols, failure interleavings) and **state-machine PBT pays off for C4/C3** (API sequences, resource life cycles: AUTOSAR, ShardStore). **Differential testing against an executable model pays off for C2/C3**: Cedar, SQLite's sqllogictest.
- *Inference:* The Volvo case shows that a *by-product* of moving prose into an executable model is discovering ambiguity in the prose standard itself (100+ issues). That matters for a project writing foundational specs.

### Gaps
- I found no published person-hour costs for TLA+ or P models, or for the Volvo models.
- I found no controlled comparison of PBT against example-based tests on defect yield in industry.

---

## Q5. Is there a published rule for choosing a form by category or by "what must be checked"?

### Takeaway
**I found no published rule or validated heuristic that maps specification category → level of abstraction → form.** The closest things are: (a) method-internal guidance (Larch tiers; ASM ground model then refinement; Parnas: tables for REQ/NAT), (b) AWS/ShardStore's practice of decomposing correctness into properties and choosing "a suitable tool" per property, and (c) RE-technique *selection* frameworks that mostly cover elicitation and documentation techniques and have weak empirical validation.

### Cited Findings
- ShardStore states the principle explicitly: decompose correctness into independent properties, check each with the most suitable lightweight tool, and use executable reference models as the specification. — [Bornholt et al., SOSP 2021](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf) (A)
- AWS 2025 describes a portfolio approach (TLA+/P for design, PBT, simulation and fault injection for implementation) without a formal selection rule. — [CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services) (B/C)
- Requirements-*elicitation* technique selection frameworks (Maiden & Rugg; Davis & Hickey; Carrizo et al.) exist, but have "little validation". — [Carrizo et al., WER 2008](https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf) (A)
- Documentation-technique selection: a survey of 42 Polish professionals choosing specification techniques by project-context attributes (a stated-preference study, not outcome data). — [Gdańsk Tech record](https://pub.pg.edu.pl/pl/publication/142925/selecting-requirements-documentation-techniques-for-software-projects-a-survey-study) (A, weak)
- Other selection models: Jiang & Eberlein (RE technique suitability by project attributes, with a case study) — [Adelaide record](https://eres.library.adelaide.edu.au/dspace/handle/2440/44866); Eff-REM QChar (by quality-requirement characteristics, built on IEEE 1233) — [Montclair record](https://digitalcommons.montclair.edu/infomgmt-busanalytics-facpubs/19). Their validation is unconfirmed.

### Category × form matrix (synthesised; each cell is *inference* from the cited cases unless a source is given)

Legend: ++ strong evidential fit; + plausible fit; − poor fit; "checks" = what the form makes mechanically checkable; "cost" = the main cost observed.

| Form → / Category ↓ | Structured prose (EARS/RFC 2119/Gherkin) | Tables (decision / Parnas / state-transition) | Schema data (JSON Schema/YAML) | Executable reference model / oracle | PBT | Model-based / stateful tests | Lightweight formal (Alloy/TLA+/P/Quint) | Proof (Coq/Isabelle/Dafny/Lean) |
|---|---|---|---|---|---|---|---|---|
| C1 Structure (one instant) | + readable, unchecked | − | + shape only (not cross-constraints) | + | + invariants on generated trees | − | ++ Alloy-style relational constraints (inference) | + if meta-theorems are needed |
| C2 Pure function | + | ++ case completeness/disjointness (Darlington, SCR) | − | ++ differential oracle (Cedar DRT, sqllogictest) | ++ (Jane Street idioms) | − | + | + (Cedar validator soundness) |
| C3 Single call pre/post/errors | + (POSIX ERRORS idiom) | ++ precondition and error partitions | + for parameter/result shape | ++ | ++ | + | + | + |
| C4 Resource life open→close | + EARS state-driven/event-driven templates | ++ state-transition table (completeness per state × event) | − | ++ (ShardStore) | + | ++ (AUTOSAR QuickCheck, ShardStore) | + | − cost high |
| C5 Concurrent env / multiple observers | − ambiguity hot spot (AUTOSAR "optionally") | − state explosion | − | + (deterministic simulation) | + | + linearizability-style checks | ++ (AWS TLA+/P: 10/10 systems; ShardStore model checking) | − cost high |
| C6 Error classification | + RFC 2119 shall/may fail | ++ enumerated classification table | ++ enumerations | + | + oracle checks classification | + | − | − |
| C7 Per-backend profile | + "implementation-defined" clauses (POSIX) | ++ capability/variance tables | ++ machine-readable profiles | + parameterised model | + same properties × backend | + | + parameterised constants | − |

What each form makes checkable, and at what cost (with cited anchors):
- **Structured prose**: makes phrasing reviewable and smell-detectable (Femmer), with no semantic checking. Low cost. The evidence is qualitative only (EARS). — [EARS record](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/)
- **Tables**: make completeness and disjointness of case splits mechanically checkable, and allow proof against code (Darlington/PVS). Cost: heavy for the regulator-driven retrofit; I found no numbers. — [Heitmeyer & Labaw](https://apps.dtic.mil/sti/pdfs/ADA276077.pdf); [Lawford & Wassyng](https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf)
- **Executable model + differential testing**: makes implementation agreement checkable on millions of inputs. Cost: writing and maintaining a second implementation; non-specialists can maintain it (ShardStore). — [Cedar](https://arxiv.org/pdf/2407.01688); [ShardStore](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf)
- **PBT / stateful PBT**: makes general laws and API-sequence behaviour checkable. Cost: writing generators and properties is hard, and judging effectiveness is hard. — [Goldstein et al.](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice); [AUTOSAR](https://research.chalmers.se/en/publication/219899)
- **TLA+/P model checking**: makes interleavings and failure scenarios checkable *at the design level*, not against code (unless conformance checking is added). Cost: 2–3 weeks to learn. — [Newcombe et al.](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf)
- **Proof assistants**: make universally quantified meta-properties (soundness) provable, and found real spec errors. Cost: high (Wasm Isabelle about 11k lines); no person-month figure was retrieved. — [Watt slides](https://wp.doc.ic.ac.uk/vetss/wp-content/uploads/sites/122/2019/10/Watt-WebAssembly-slides.pdf)

### Inferences
- *Inference (candidate rule, not an established one):* choose the form by **what must be quantified over**:
  - a finite case split → table;
  - a value domain → executable oracle plus PBT;
  - sequences of calls on one resource → state-transition table plus stateful/model-based tests;
  - interleavings of several actors → model checker (TLA+/P/Quint);
  - every program or input as a meta-property → proof.
  
  The level then follows from the Parnas/Jackson boundary: write at the black-box interface (IN/OUT of the library, REQ for callers), and parameterise per-backend NAT/profile. This is consistent with Larch's tiering and with ShardStore's "property → suitable tool" decomposition, but no source states it as a rule.
- *Inference:* Prose remains the normative, human-facing layer in every surveyed standard (Wasm, ECMAScript, HTML, POSIX, Ferrocene). The evidence argues for prose *paired with* an executable or tabular artefact per category, not for prose alone.

### Gaps
- I found no published, empirically validated category→level→form rule. That is a finding, not a search failure, but my coverage was limited by blocked full-text access.
- I found no head-to-head comparison of forms on the same category (e.g. table vs PBT for error classification). The bake-off would itself generate novel evidence.
- Alloy and Quint industrial cost data was not retrieved in this session.
