# Automated test-input generation for database-backed and data-intensive software

Scope note: this track covers automated generators that produce test inputs (program inputs, database states, dataflow input records, structured inputs, operation sequences) to expose implementation defects. Evidence labels used on every claim: **documented** = full text (or the relevant full section) read this session; **lead** = search extract or abstract only; **inferred** = my engineering inference; **unreachable** = could not be retrieved; **vendor** = maintainer/vendor claim not independently checked. Maintenance data was collected 2026-11-26 by shallow `git clone` (last commit on default branch), the PyPI JSON API and Maven Central search; licences were read from the LICENSE file header in each clone.

Corrections to the brief, all documented: BigTest appeared at **ESEC/FSE 2019**, not ICSE 2019 ([BigTest paper, in repo](https://github.com/maligulzar/BigTest)). EvoSQL's authors are Castelein, Aniche, Soltani, Panichella and van Deursen (ICSE 2018, DOI 10.1145/3180155.3180202) ([TU Delft repository](https://repository.tudelft.nl/record/uuid:90a6431f-f78f-4ac3-bf87-c052cd9cd5d4)); Zaidman is not an author.

## 1. Symbolic/concolic execution for database applications (Emmi et al., Pan/Wu/Xie, XData, AGENDA, Marcozzi, QAGen)

### Takeaway
White-box concolic approaches can generate both program inputs and the database records that drive query-dependent paths. However, the documented prototypes (Emmi 2007 on Java/JDBC; Pan/Wu/Xie on .NET/Pex) are academic, and I found no maintained release. XData is the most developed query-level generator. It kills SQL query mutants and has a documented evaluation that beat hand-made datasets and TA grading, but it is a query-testing and grading tool, not a whole-application generator, and I could not confirm a maintained public repository.

### Cited Findings
- **Emmi, Majumdar & Sen, ISSTA 2007 (documented, read through the approach sections of a third-party copy).** Given an imperative program that talks to a database through API calls, the algorithm generates both program inputs and "suitable database records to systematically explore all paths of the program, including those paths whose execution depend on data returned by database queries". It runs the program concretely and symbolically at once, over program variables and the database state. It captures the concrete SQL strings at run time because they "cannot be inferred precisely by statically looking" at the code. The constraint language is linear arithmetic plus string equality, disequality and membership constraints. The implementation used Soot and an LP solver on Java/`java.sql` code and was run on a Java reimplementation of a MediaWiki component. The authors list limitations of their implementation and say their solver may fail where arithmetic and string constraints interact. — [Emmi et al. 2007 (typeset.io copy)](https://typeset.io/pdf/dynamic-test-input-generation-for-database-applications-1hfczwa77z.pdf); [dblp](https://dblp.org/rec/bibtex/conf/issta/EmmiMS07)
- **Pan, Wu & Xie line of work (ASE 2011 "Generating program inputs for database application testing"; TOSEM 2014 "Guided test generation for database applications via synthesized database interactions"; 48 and 40 Semantic Scholar citations).** Documented from the abstract of Kai Pan's 2013 UNC Charlotte dissertation, which bundles this work. It uses dynamic symbolic execution with Microsoft Pex for .NET. It generates program inputs for an *existing* database state through "auxiliary query construction", and it generates database states for Boundary Value and Logical Coverage. It synthesizes database interactions that bridge "query-construction constraints, query constraints, database schema constraints, and query-result-manipulation constraints", and it supports mutation testing of database applications. The empirical claims are abstract-level only (lead). — [Pan dissertation](https://ninercommons.charlotte.edu/record/1287/files/Pan_uncc_0694D_10385.pdf); [Semantic Scholar ASE 2011 record, DOI 10.1109/ASE.2011.6100152](https://api.semanticscholar.org/graph/v1/paper/search?query=Generating%20program%20inputs%20for%20database%20application%20testing)
- Pan et al.'s problem of generating inputs *given an existing database state* is the setting closest to running against protected real data (inferred from the documented abstract).
- **XData (IIT Bombay; Chandra, Chawda, Kar, Reddy, Shah, Sudarshan, VLDB Journal 2015, arXiv 1411.6704) (documented).** A mutant Q′ of query Q "is killed by a dataset D if Q(D) ≠ Q′(D)". Earlier XData generated datasets that kill all mutants in a class covering join-type and comparison-operator mutations. The 2015 paper extends this to a wider range of SQL and of mutation classes: aggregation/DISTINCT, string selection and LIKE, missing join conditions, HAVING, NULLs and some subqueries. On a TPC-H/university evaluation, the techniques worked for 17 of 22 queries. Some mutants (e.g., MAX→MIN in one case) were not caught, and the authors leave "handling such cases" as future work. ORDER BY mutations "in general, cannot be caught" by datasets alone. On 14 student assignments from an undergraduate course, "the XData datasets outperform predefined datasets as well as manual grading done earlier by teaching assistants". — [arXiv 1411.6704](https://arxiv.org/pdf/1411.6704)
- **XData successor (Somwase, Das, Sudarshan, arXiv 2409.18821, Sep 2024) (documented, abstract and introduction).** Earlier XData "handled basic single block SQL queries, as well as simple nested SQL queries, but could not handle more complex queries". The new approach targets complex queries, motivated by validating text-to-SQL output. This paper also names **AGENDA** (Chays et al.) as early work on generating test datasets that kill mutants (AGENDA itself not read: lead). — [arXiv 2409.18821](https://arxiv.org/pdf/2409.18821)
- An **XDataPro** demo extends XData to database applications through an IntelliJ plugin that generates data for queries and program inputs together (lead, search extract only). — [Microsoft Research XDataPro PDF](https://www.microsoft.com/en-us/research/uploads/prod/2021/02/xdatapro.pdf)
- XData's maintenance and licence: I found no public repository by clone attempt or search, and the 2015 paper only points to a grading-tool URL (documented absence in what I checked). — [arXiv 1411.6704](https://arxiv.org/pdf/1411.6704)

### Inferences
- These methods expose **path-coverage and query-semantics defects**: wrong join type (inner vs outer), missing join predicates, off-by-one comparisons, NULL handling, aggregation mistakes. Outer-join and NULL mutants map directly to "missing record" and "partial coverage across sources" defects in a reconciliation pipeline (inferred).
- All require **source code (white-box) or the SQL text**, plus the schema. None needs real rows. Pan et al. can use an existing database state as context, which suits running inside a protected environment (inferred).
- None of the documented tools handles multi-source identity ambiguity or temporal ordering. Their database model is a single consistent database state (inferred from the documented problem statements).

### Gaps
- Emmi 2007 evaluation numbers were not extracted from the third-party copy. ACM full texts for Pan et al. ASE 2011 and TOSEM 2014 were not retrieved; ACM returned an HTML interstitial (unreachable).
- Not researched in this session: **Marcozzi et al. relational symbolic execution**, **QAGen** (Binnig et al.) and AGENDA's own papers. No claims are made about them.
- XData code availability and licence are unconfirmed.

## 2. Search-based and constraint-based generation (EvoSQL, EvoMaster SQL handling, SchemaAnalyst, Alloy/SMT, Korat, Cosette)

### Takeaway
Search-based generation of database state is mature and actively maintained only in **EvoMaster**. EvoMaster (LGPL-3.0; commits up to 2026-11-26; tags up to v6.2.0) instruments JVM services, treats SQL INSERTs as genes in the test genotype and uses SQL branch-distance heuristics. Its documented evaluation shows significant coverage gains (up to +16.5%) and 7 new faults on 5 open-source APIs. No gain appeared where input validation blocked the code that touches SQL. EvoSQL (query-level, Apache-2.0) has strong documented results but has been dormant since 2019. SchemaAnalyst (schema-constraint testing, GPL-3.0) has been dormant since 2021.

### Cited Findings
- **EvoMaster SQL handling (Arcuri & Galeotti, TOSEM 2020 "Handling SQL Databases in Automated System Test Generation") (documented).**
  - Mechanism: a heuristic that "takes into account the state of the accessed databases" (SQL branch distance on intercepted queries). The paper also enables "the generation of SQL data directly from the test cases", which is useful when the database is "read-only" for the system under test and "the actual data is generated by other services".
  - Constraint handling: generated INSERTs must respect primary keys, foreign keys, unique and check constraints. Tables a foreign key points to are inserted first, and broken constraints are repaired during the search, including foreign keys to auto-increment primary keys.
  - Results: six RESTful APIs (five open-source, one industrial), 30 repetitions. The SQL heuristics alone gave a significant improvement on only 2 of 5 SUTs, up to 13%, and they made tests longer. Direct SQL data generation improved coverage significantly, up to +16.5%. Average faults (5xx responses) rose: catwatch 9.4→12.3, features-service 16.2→18.9, proxyprint 31.1→32.6, rest-news 1.0→1.8, scout-api 52.3→51.8 (not significant). That is "7 new unique ones", though not found in every run.
  - Negative result: on the industrial API, "SQL heuristics do not help the search if the SUT code dealing with SQL is not even reached due to failed input validation".
  - Threats: only six services, up to 7,500 LOC and 15 tables / 92 columns.
  - [EvoMaster TOSEM 2020 PDF (repo copy)](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications/2020_tosem.pdf); earlier version: [GECCO 2019 "SQL Data Generation to Enhance Search-Based System Testing"](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications/2019_gecco_sql.pdf)
- **EvoMaster current capabilities (vendor, README 2026-11).** White-box mode "can intercept and analyse all communications done with SQL and MongoDB databases" and supports Postgres, MySQL, H2 and MongoDB. It requires a hand-written driver and JDK 9+ bytecode instrumentation (JVM languages only; JS/TS and C# white-box support "has been dropped"). Black-box mode works on any API but gives worse results. The README claims "more than 30 different kinds of faults", including schema mismatches, BOLA and SQL injection. Its 2026 publication list includes "Search-Based Fuzzing For RESTful APIs That Use MongoDB". — [EvoMaster README](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/README.md); [publications.md](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications.md)
- **EvoMaster maintenance (documented).** Last commit 2026-11-26. Git tags reach v6.2.0. Licence LGPL-3.0. Maven Central's search index lists `org.evomaster` 3.4.0 with a timestamp of 2025-01-03. I take this to be a stale index rather than the latest release, which conflicts with the git tags (inferred). — [EvoMaster repo](https://github.com/WebFuzzing/EvoMaster); [Maven Central search](https://search.maven.org/solrsearch/select?q=g:org.evomaster)
- **EvoSQL (Castelein et al., ICSE 2018) (documented).** It treats test-data generation for a single SQL query as search over database contents, targeting SQLFpc full-predicate coverage targets. The authors argue that prior constraint-solver approaches "commonly do not support JOIN expressions, subqueries, and specific database" functions. Evaluation: 2,135 queries from real systems (e.g., SuiteCRM, ERPNext), 10 runs each, with 127 of 12,991 infeasible targets removed by hand.
  - Random search fully covered 140 queries (6.5%) and failed completely on 605 (28.33%).
  - Biased random search fully covered 1,923 (90%).
  - The genetic algorithm fully covered 2,106 (98.6%), with a partial median of 86.66% on the rest and no complete failures.
  - Performance falls as the number of coverage targets rises.
  - [EvoSQL ICSE 2018 (TU Delft repository)](https://repository.tudelft.nl/file/File_6c2d74fc-0c7b-4248-b0a8-decdf4360c20)
- **EvoSQL maintenance (documented).** Last commit 2019-08-24, Apache-2.0. — [SERG-Delft/evosql](https://github.com/SERG-Delft/evosql)
- **SchemaAnalyst (McMinn, Kapfhammer, Wright) (lead for results).** Search-based generation of INSERT data that exercises schema integrity constraints, assessed by mutation analysis of the constraints. The 2013 ICST paper reports it outperforms DBMonster in both constraint coverage and mutation score, with competitive or faster generation times. Follow-on work covers coverage criteria (TOSEM 2015), "virtual" mutation analysis against a local DBMS model to cut DBMS cost (2016), and a taxonomy of ineffective mutants (2019). Out of the box it supports HSQLDB and SQLite (lead). — [Kapfhammer 2013 page](https://www.cs.allegheny.edu/sites/gkapfham/research/papers/Kapfhammer2013); [McMinn 2016a](https://cs.allegheny.edu/sites/gkapfham/research/papers/McMinn2016a); [ineffective mutants preprint](https://eprints.whiterose.ac.uk/126146/1/ineffective-mutants.pdf)
- **SchemaAnalyst maintenance (documented).** Last commit 2021-03-24, GPL-3.0. — [SchemaAnalyst repo](https://github.com/SchemaAnalyst/SchemaAnalyst)
- **Korat (documented maintenance only).** Last commit 2016-03-17, GPL-2.0. — [korattest/korat](https://github.com/korattest/korat)
- **Cosette (documented maintenance only).** Last commit 2024-12-17, BSD-2-Clause. — [uwdb/Cosette](https://github.com/uwdb/Cosette)

### Inferences
- EvoMaster's "database state as genotype" is the only maintained OSS mechanism found that **co-generates multi-table relational state (with foreign-key closure) and the operation sequence** against a running service. It is therefore the most direct capability reference for relational fixtures. Its oracle is generic (5xx, schema mismatch, security), not domain correctness, so reconciliation or ER logic errors that return 200 would go undetected without user-written assertions (inferred from the documented oracle).
- EvoSQL and SchemaAnalyst target **one query** or **one schema's constraints** respectively. They expose predicate and constraint defects, not cross-source or temporal logic (inferred).
- Korat, TestEra/ADUSA and Alloy-style bounded-exhaustive generation would need a hand-written invariant or specification of valid relational structures. Korat's maintenance is effectively frozen since 2016 (inferred, maintenance documented).

### Gaps
- Not read this session: TestEra and ADUSA (Khalek & Khurshid), Alloy/SMT database generators, Cosette's counterexample-generation capability (only repo date checked). No empirical claims are made about them.
- No independent (non-author) evaluation of EvoMaster SQL handling was retrieved.

## 3. Data-intensive / dataflow programs (BigTest, SEDGE, Olston et al., BigFuzz, NaturalFuzz)

### Takeaway
For Spark-style dataflow programs, **BigTest** (FSE 2019, symbolic execution over UDFs with logical models of dataflow operators) and **BigFuzz** (ASE 2020, coverage-guided fuzzing with executable specifications of operators and schema-aware mutations) have documented fault-detection gains over SEDGE and over random fuzzing. Both are research prototypes last updated in 2021–2022.

### Cited Findings
- **BigTest (Gulzar, Mardani, Musuvathi, Kim, ESEC/FSE 2019) (documented).**
  - Mechanism: it symbolically executes UDFs with Java PathFinder / Symbolic PathFinder and abstracts Spark operators logically rather than executing about 700 KLOC of Spark. It solves the combined path constraints with Z3 or CVC4 to produce concrete input records.
  - It explicitly models "terminating cases" of each operator. For joins, that means keys present only in the left table, only in the right, or in neither, because "the output can contain rows with null entries, which are an important source of bugs". It also models collections created by `flatMap` and consumed by `reduce`, and string constraints such as `split(",").length ≥ 2`, which matter because ArrayIndexOutOfBounds and StringIndexOutOfBounds errors are frequent.
  - Loops are unrolled to a user-given bound K (default 2).
  - Results: real DISC applications left "34% of Joint Dataflow and UDF (JDU) paths untested". BigTest "reveal[s] 2X more manually-injected faults than" SEDGE on a benchmark of 31 faulty DISC applications. It reduces data by 10^5–10^8 with "order of tens" of records achieving the same JDU coverage as full production data, and saves 194X CPU time on average.
  - It targets application-level faults only, not framework faults.
  - [BigTest FSE 2019 PDF (in repo)](https://github.com/maligulzar/BigTest); [author PDF](https://people.cs.vt.edu/~gulzar/assets/pdf/fse2019-bigtest.pdf)
- **BigTest maintenance (documented).** maligulzar/BigTest last commit 2022-08-05; the UCLA-SEAL/BigTest mirror 2021-09-26. No LICENSE file appears in the top-level tree. — [maligulzar/BigTest](https://github.com/maligulzar/BigTest)
- **SEDGE (Li et al.) (lead).** It appears as BigTest's baseline, and BigTest characterises prior DISC test generators as either not reasoning about UDFs or treating them "as uninterpreted functions". SEDGE's own paper was not read. — [BigTest FSE 2019](https://github.com/maligulzar/BigTest)
- **BigFuzz (Zhang et al., ASE 2020; tool paper ICSE 2021 companion, arXiv 2103.05118) (documented from the 4-page tool paper).**
  - Mechanism: it rewrites a Spark application into a "semantically equivalent, yet a framework-independent program" using executable specifications of the dataflow operators, which addresses the long latency of DISC runs. It monitors JDU coverage and uses "schema-aware mutations based on common error types in DISC applications".
  - Results against random fuzzing: fuzzing time 78–1477X faster. With valid seeds, coverage rises 20–200% and error detection 33–100%. Without valid seeds, coverage rises 118–271% and error detection 58–157%.
  - [arXiv 2103.05118](https://arxiv.org/pdf/2103.05118)
- **BigFuzz maintenance (documented).** qianzhanghk/BigFuzz last commit 2021-09-16, built on JQF; it has a LICENSE file whose type I did not check. — [qianzhanghk/BigFuzz](https://github.com/qianzhanghk/BigFuzz)

### Inferences
- BigTest's join terminating-case modelling (left-only, right-only, neither) is the closest documented mechanism to systematically generating **missing-record and partial-coverage cases across sources**. It still assumes a single key equality and has no notion of ambiguous identity (inferred).
- Both tools need **source (UDF) access** and a description of the input schema. BigFuzz also benefits from valid seed inputs, which in a protected environment could be real rows used in place (inferred).
- BigTest's finding that tens of records reach the same JDU coverage as production data is direct evidence that generated minimal datasets can stand in for real data **for path coverage** (documented in the paper; generalising it is inferred).

### Gaps
- Not read: Olston et al. SIGMOD 2009 (example generation for Pig) and SEDGE (Li et al.). NaturalFuzz: the clone attempt failed and no claims are made. "DataPrep / Test data generation for Spark" and "HOMEX" were not located.
- The BigFuzz ASE 2020 full paper is ACM-only and returned an HTML interstitial (unreachable). Figures come from the arXiv tool paper.

## 4. Grammar- and constraint-based fuzzing of structured inputs (Fuzzing Book, ISLa, FANDANGO, Hypothesis, QuickCheck, Schemathesis)

### Takeaway
These tools are maintained and permissively or weak-copyleft licensed (except ISLa, GPL-3.0). They encode structure through grammars, JSON/OpenAPI schemas or strategies. Cross-field constraints are expressed in quantified constraint languages: ISLa and FANDANGO use `forall`/`exists` over grammar nonterminals, and FANDANGO additionally allows Python expressions and evolutionary search. Cross-record and cross-table referential constraints are possible in principle but must be written by hand. None ships a relational or foreign-key model.

### Cited Findings
- **FANDANGO (Zeller group) (documented from the tutorial/reference PDF and repo).** Grammar plus constraints. It "evolves" random inputs "through mutations and cross-over until they fulfill the given constraints". Constraints use `forall`/`exists` quantifiers over nonterminals, e.g. `forall <assgn> assgn_1: exists <assgn> assgn_2: (...)`, can be unsatisfiable, and cover features such as checksums and distributions (e.g., a voltage field following a Gaussian capped at 20 mV). Maintenance: last commit 2026-11-25; PyPI `fandango-fuzzer` 1.3.2 on 2026-11-25, first release 2025-01-10; licence EUPL-1.2. — [Fandango reference PDF](https://raw.githubusercontent.com/fandango-fuzzer/fandango/main/docs/_static/fandango.pdf); [PyPI](https://pypi.org/pypi/fandango-fuzzer/json); [repo](https://github.com/fandango-fuzzer/fandango)
- **ISLa (Steinhöfel & Zeller, ESEC/FSE 2022 "Input Invariants", 69 citations).** The paper was not retrieved because ACM was blocked (unreachable). Maintenance (documented): last commit 2024-07-01, PyPI `isla-solver` 1.14.4, GPL-3.0. That I have not verified the activity status is a gap; the commit date suggests ISLa is no longer actively developed while FANDANGO is (inferred). — [rindPHI/isla](https://github.com/rindPHI/isla); [PyPI](https://pypi.org/pypi/isla-solver/json)
- **Fuzzing Book (documented maintenance).** Last commit 2026-01-22. PyPI `fuzzingbook` 1.2.2 on 2024-11-10. Content is licensed CC BY-NC-SA 4.0; the code licence is stated separately in LICENSE.md (truncated in my read). — [uds-se/fuzzingbook](https://github.com/uds-se/fuzzingbook)
- **Hypothesis stateful testing (documented from docs/stateful.rst).** `RuleBasedStateMachine` rules can draw from a `Bundle`, a "named collection of generated values that can be reused by other operations", populated by rule return values (`target=`) and drawn or removed via `consumes()`. Bundles "encourage Hypothesis to choose the same keys and values for multiple operations", which establishes a "universe" of keys. `@initialize` rules run exactly once first. More complex state-dependent draws use `runner().flatmap` or `st.data()`. Maintenance: last commit 2026-11-23, PyPI 6.170.17 on 2026-11-20, MPL-2.0. — [Hypothesis stateful docs](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/master/hypothesis/docs/stateful.rst); [PyPI](https://pypi.org/pypi/hypothesis/json)
- **hypothesis-jsonschema (documented maintenance).** 0.23.2 on 2026-10-27, MPL-2.0. — [PyPI](https://pypi.org/pypi/hypothesis-jsonschema/json)
- **Schemathesis (documented maintenance).** PyPI 4.34.2 on 2026-11-24, first release 2019-08-26, MIT; last commit 2026-11-26. — [PyPI](https://pypi.org/pypi/schemathesis/json); [repo](https://github.com/schemathesis/schemathesis)
- **quickcheck-state-machine (Haskell) (documented from README).** Its tutorial shows both a logic bug and a race condition being caught, and states that parallel testing gives "testing for race conditions for free". Maintenance: stevana/quickcheck-state-machine last commit 2026-05-18. The licence is BSD-style per the copyright header; the full text was not read. — [stevana/quickcheck-state-machine](https://github.com/stevana/quickcheck-state-machine)

### Inferences
- **Cross-record constraints.** In Hypothesis, Bundles give a cheap, documented way to make later records reference earlier generated identifiers. That covers foreign-key-like references, duplicate identifiers across "sources", and delete-then-reference sequences. It has no built-in uniqueness or referential integrity checks; the user encodes these (inferred from the docs).
- **Cross-field constraints** in ISLa and FANDANGO are quantified predicates over a parse tree of one input. Encoding a multi-table dataset means making the whole dataset one grammar-derived document (e.g., a CSV or JSON bundle). Whether solving scales to realistic multi-source datasets is untested in what I read (inferred).
- These tools need a **specification** (grammar, schema or strategies) but no source code and no real rows. Coverage-guided modes need instrumentation (inferred).

### Gaps
- The ISLa and FANDANGO (ISSTA 2025) research papers were not read, so there are no empirical defect-detection figures for them here.
- No documented application of ISLa or FANDANGO to multi-table relational datasets was found.

## 5. Stateful and temporal sequences (model-based testing, TLA+ trace generation, Jepsen/Elle) and incremental/CDC data processing

### Takeaway
Mature MBT tools are maintained: GraphWalker (MIT), fMBT (LGPL-2.1), Hypothesis/QuickCheck state machines, and Modelator (Apache-2.0; last commit 2025-03). The strongest documented defect evidence for history-based checking is **Elle**, which found anomalies in every one of four databases tested, almost all previously unknown. I found **no documented application** of these generators to late-arriving or CDC data in pipelines. The nearest evidence is incremental-view-maintenance engines that test incremental results against full recomputation with random SQL generators. That is absence of evidence, not evidence the problem is unsolved.

### Cited Findings
- **Elle (Kingsbury & Alvaro, VLDB 2020, arXiv 2003.10554) (documented).**
  - What it is: a checker that infers an Adya-style dependency graph from client-observed transactions. It does so by "carefully selecting database objects and operations when generating histories" (e.g., list-append), so that reads reveal version history.
  - Claims: it detects every Adya anomaly except predicate ones, with a soundness proof. Generated transactions were 1–10 random read/append operations, with 10–30 client threads on 5–9 nodes plus fault injection.
  - Results: "Elle revealed anomalies in every system we tested, including G2, G-single, G1a, lost updates, cyclic version dependencies, and internal inconsistency. Almost all of these anomalies were previously unknown". Cases include TiDB re-applying writes on retry and YugaByte DB G2-item anomalies when masters crashed or paused.
  - [arXiv 2003.10554](https://arxiv.org/pdf/2003.10554)
- **Elle maintenance (documented).** Last commit 2026-10-16, EPL-2.0. — [jepsen-io/elle](https://github.com/jepsen-io/elle)
- **Modelator (documented from README).** It takes TLA+ models and "generates tests that can be executed against an implementation of the model" using the Apalache model checker, with `sample` to generate behaviours matching a TLA+ predicate and `check` for invariants. Maintenance: last commit 2025-03-12, Apache-2.0. — [informalsystems/modelator](https://github.com/informalsystems/modelator)
- **GraphWalker (documented maintenance).** Last commit 2026-10-17, MIT. Maven Central's latest is 4.3.3, timestamped 2024-09-26. — [GraphWalker repo](https://github.com/GraphWalker/graphwalker-project); [Maven Central](https://search.maven.org/solrsearch/select?q=g:org.graphwalker)
- **fMBT (documented maintenance).** intel/fMBT last commit 2026-01-14, LGPL-2.1. — [intel/fMBT](https://github.com/intel/fMBT)
- **Incremental view maintenance testing (lead).**
  - pg_trickle docs state the core invariant that applying deltas incrementally "must be identical to recomputing the query from scratch". They describe a production shadow mode comparing the two and use SQLancer random SQL generation to find delta-engine bugs before release (vendor/project claim).
  - Databricks' Enzyme paper (arXiv 2603.27775, 2026) mentions correctness frameworks that "non-deterministically generat[e] test cases spanning the entire domain of valid MV definitions" (lead).
  - [pg_trickle blog: shadow-mode correctness fuzzing](https://pgxn.org/dist/pg_trickle/0.37.0/blog/shadow-mode-correctness-fuzzing.html); [Enzyme arXiv 2603.27775](https://arxiv.org/pdf/2603.27775)

### Inferences
- The documented pattern that transfers to CDC and late-arriving data is the **differential oracle**: incremental result versus full recomputation over generated or permuted event sequences. A further oracle is invariance under delivery-order permutations within allowed bounds. Hypothesis or QuickCheck state machines can generate the delivery sequences (inserts, updates, retractions, late arrivals). The pipeline-specific application is inferred; I found no peer-reviewed study of it.
- Elle's design lesson is to choose operations whose observations make the hidden order recoverable (e.g., append-only lists). That design lesson transfers to testing reconciliation of delayed reports (inferred).
- MBT tools need a hand-written **model** (graph, TLA+ spec or state machine) and no source code. They can run against a live system inside a protected environment and export only pass/fail plus a minimized trace (inferred). The trace may contain values, so what is exported needs review (inferred).

### Gaps
- Not found: any empirical study of MBT or TLA+ trace generation applied to CDC, watermarking or late-data handling in data pipelines. The Enzyme testing section and pg_trickle's claims were not read in full.
- "Model-based trace checking" literature was not read.

## 6. Entity resolution / reconciliation testing

### Takeaway
I found **no documented work applying metamorphic or adversarial input generation to entity resolution or record linkage software with defect-detection evidence**. The closest documented items are a 2016 model-driven test-model proposal for entity reconciliation (no defect data) and metamorphic testing of named-entity recognition, a different problem. Ground-truth generators (Febrl, GeCo) are known to exist but were not verified this session. This is absence of evidence in the sources searched, not evidence the problem is unsolved.

### Cited Findings
- **Testing entity reconciliation (A-TEST 2016, Univ. Oviedo / Seville group) (documented, 4 pages).** It argues "testing the applications that implement the entity reconciliation problem is crucial to ensure both the correctness of the reconciliation process and the quality of the reconciled data". It proposes a first MDE-based approach for creating test models for integration testing of entity reconciliation applications, with a planned case study with an Andalusian institute. It reports no defect-detection results. — [A-TEST 2016 paper](https://giis.uniovi.es/testing/papers/a-test-2016-testing-entity-reconciliation.pdf)
- **Metamorphic testing of NER (IET Software 2022) (lead).** Reports real bugs found in an industrial NER system without an oracle. Not entity resolution. — [DOAJ record](https://doaj.org/article/2549c35b1b2441fabcb98e1a6dc40f9d)
- **ER evaluation framework (arXiv 2404.05622, 2024) (lead).** It notes entity resolution systems are "notoriously difficult to evaluate" and proposes entity-centric evaluation against known clusters. It is about evaluating accuracy, not finding defects. — [arXiv 2404.05622](https://arxiv.org/html/2404.05622v1)
- **ER library maintenance (documented; these are ER implementations rather than generators, listed as capability references).**
  - recordlinkage 0.16, last release 2023-07-20, BSD-3.
  - splink 5.0.0, 2026-09-28, MIT.
  - dedupe 3.0.3, MIT, last commit 2025-07-28.
  - [recordlinkage PyPI](https://pypi.org/pypi/recordlinkage/json); [splink PyPI](https://pypi.org/pypi/splink/json); [dedupe PyPI](https://pypi.org/pypi/dedupe/json)

### Inferences
- Plausible metamorphic relations for ER and reconciliation are inferred, not documented as evaluated:
  - invariance under record or source order;
  - invariance under renaming identifiers;
  - monotonicity when adding an exact duplicate;
  - transitivity and consistency of cluster assignments;
  - stability when a non-identifying attribute is perturbed.
- Generators with ground-truth identities (Febrl-style duplicate generation with controlled corruption) supply an oracle for "same entity" without real data. I believe the recordlinkage package bundles Febrl datasets, but did not verify this in this session (inferred).

### Gaps
- Febrl and GeCo/Gecko generators were not researched (no claims). No study was found on adversarial or ambiguity-targeted generation for ER, or on defect detection in record-linkage software through generated inputs. A targeted search of VLDB/SIGMOD/ICST for "testing entity matching" beyond the one query run here is needed.

## 7. Requirements (white-box, specification, real rows) and fit with a protected environment

### Takeaway
Most approaches need **either source or instrumentation** (concolic, BigTest/BigFuzz, EvoMaster white-box) **or a hand-written specification** (grammar/constraints, schema, state model, TLA+). None of the documented tools needs real rows. Several can use real rows or an existing database state as seeds or context (Pan et al., BigFuzz seeds, EvoMaster against a pre-populated database). Running the generator inside the protected environment and exporting only coverage, failing-path identifiers or minimized synthetic counterexamples is technically compatible with these designs, but none of the sources documents such a privacy-preserving deployment.

### Cited Findings
| Approach / tool | Needs source/instrumentation | Needs spec | Uses real rows | Defects exposed (documented evidence) | Maintenance (2026-11-26) | Licence |
|---|---|---|---|---|---|---|
| Emmi et al. 2007 concolic | Yes (Java bytecode, Soot) | No | No | Path coverage of query-dependent code | Research prototype; no repo found | n/a |
| Pan/Wu/Xie (Pex DSE) | Yes (.NET/Pex) | Schema | Optionally an existing DB state | Coverage, mutation testing (abstract only) | No repo found | n/a |
| XData | Query text + schema | Schema/constraints | No | Kills join/predicate/aggregate/NULL mutants; beat TA grading ([arXiv 1411.6704](https://arxiv.org/pdf/1411.6704)) | No public repo found; 2024 successor paper | unknown |
| EvoSQL | Query text | Schema | No | 98.6% of 2,135 queries fully covered ([ICSE'18](https://repository.tudelft.nl/file/File_6c2d74fc-0c7b-4248-b0a8-decdf4360c20)) | Last commit 2019-08-24 | Apache-2.0 |
| EvoMaster (white-box SQL) | Yes (JVM agent + driver) | OpenAPI/GraphQL/RPC schema; DB schema read | Can run on a pre-populated DB (inferred) | +16.5% coverage, 7 new faults on 5 OSS APIs ([TOSEM'20](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications/2020_tosem.pdf)) | Last commit 2026-11-26; tag v6.2.0 | LGPL-3.0 |
| SchemaAnalyst | No (schema only) | DDL | No | Constraint mutants; beats DBMonster (lead) | Last commit 2021-03-24 | GPL-3.0 |
| BigTest | Yes (UDF source, JPF) | Input schema | No | 2X injected faults vs SEDGE ([FSE'19](https://people.cs.vt.edu/~gulzar/assets/pdf/fse2019-bigtest.pdf)) | Last commit 2022-08-05 | no LICENSE file found |
| BigFuzz | Yes (program rewrite + instrumentation) | Input schema | Optional seeds | 33–157% more errors vs random ([arXiv 2103.05118](https://arxiv.org/pdf/2103.05118)) | Last commit 2021-09-16 | LICENSE present, type unchecked |
| FANDANGO / ISLa | No | Grammar + constraints | No | No paper figures read | FANDANGO active (2026-11-25); ISLa last commit 2024-07-01 | EUPL-1.2 / GPL-3.0 |
| Hypothesis (stateful), QuickCheck-SM | No | Strategies / state model | No | Race and logic bugs in tutorial (QSM README) | Active | MPL-2.0 / BSD-style |
| Schemathesis | No (black-box) | OpenAPI/GraphQL | No | Not assessed here | Active (2026-11-24) | MIT |
| GraphWalker, fMBT, Modelator | No | Graph / model / TLA+ | No | Not assessed here | Active / active / 2025-03 | MIT / LGPL-2.1 / Apache-2.0 |
| Jepsen + Elle | No (black-box clients) | Consistency model + workload | No | Anomalies in all 4 DBs tested, mostly new ([VLDB'20](https://arxiv.org/pdf/2003.10554)) | Last commit 2026-10-16 | EPL-2.0 |

- Real data is not needed for coverage in BigTest's evaluation: "only few of the data records (order of tens) are actually required to achieve the same JDU coverage as the entire production data" (documented). — [BigTest README/paper](https://github.com/maligulzar/BigTest)
- In EvoMaster, generating SQL data directly helps when the database is filled by other services ("read-only" for the system under test). This mirrors ingestion from external sources (documented mechanism; applicability inferred). — [EvoMaster TOSEM 2020](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications/2020_tosem.pdf)

### Inferences
- **Running inside the protected environment** (inferred):
  - White-box generators (EvoMaster, BigTest/BigFuzz-style) can run against real data or a real database state and export derived artefacts: coverage maps, failing-path or branch identifiers, constraint skeletons, or *solver-generated synthetic* counterexamples that satisfy the same path condition.
  - Path conditions or seeds derived from confidential rows can still leak values, such as string-equality constants. Any export needs value-level review.
- **Effort and cost** (inferred): writing an EvoMaster driver, a grammar with constraints or a state model is a one-off specification cost. Concolic and dataflow prototypes carry high integration and maintenance cost because they are pinned to old JPF/Spark/Pex stacks and lack recent maintenance (dates documented above).
- **Coverage of the brief's data concerns** (inferred), by concern:
  - Relational/multi-table: documented in EvoMaster and XData/EvoSQL (per query).
  - Missing records: BigTest join terminating cases and XData outer-join mutants.
  - Conflicts and ambiguous identities: no documented tool.
  - Temporal and delivery order: state-machine and history tools are documented for databases, not pipelines.

### Gaps
- No source documents a deployment where generators run on protected or personal data and export only derived information.
- Cost figures (engineering hours to write drivers, grammars or models) were not found in the documented sources.
