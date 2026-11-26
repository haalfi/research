# Fixture minimisation: reducing real data and event sequences to small regression fixtures that keep their defect-detection power

Labels used on every claim. **[documented]**: I read the full text, or the relevant full section, of the primary source. **[lead]**: search-engine extract only. **[inferred]**: my own engineering inference. **[unreachable]**: I tried the source and could not fetch it. **[metadata]**: from git clone, LICENSE file or the PyPI JSON API, checked 2026-11-26.

Method note: PDFs were downloaded to the scratchpad and converted with pdftotext. For some papers I read the abstract plus keyword-located passages, not every page. Those claims are marked [documented] only where the passage itself was read. Repository dates are the last commit on the default branch (shallow clone, 2026-11-26).

## Q1. Core reduction algorithms and OSS tools (ddmin, HDD, Perses, C-Reduce, Picire/Picireny, ddSMT, SQL reducers, Hypothesis/QuickCheck shrinking, Jepsen/Elle)

### Takeaway
All mainstream reducers share one model. A black-box "interestingness" oracle, usually a script that exits 0 while the failure still occurs, is re-run on ever-smaller candidates. ddmin gives only 1-minimality, and its worst case is a quadratic number of oracle runs. Structure-aware variants (HDD, Perses, C-Reduce, Picireny, SQLancer's AST reducer, SQLess) produce smaller and more often valid results in fewer runs, but each needs a grammar or format-specific passes. No maintained OSS tool reduces multi-table relational data while respecting keys. SQLancer's INSERT-row removal and the SIGMOD 2019 "smallest counterexample database" work come closest. Because every tool works offline against a local oracle, all of them could run inside a protected environment.

### Cited Findings
- **ddmin (Zeller & Hildebrandt, IEEE TSE 28(2), 2002).** ddmin turns a failing test case into a "minimal test case that still produces the failure" and can also isolate the difference between passing and failing inputs. In the case study, a Mozilla crash after 95 user actions was reduced to 3 relevant actions, and 896 lines of HTML to the single line that caused the failure. This took 139 automated test runs, or 35 minutes on a 500 MHz PC. [documented] — [Zeller & Hildebrandt 2002, author PDF](https://www.st.cs.uni-saarland.de/papers/tse2002/tse2002.pdf)
- ddmin targets **1-minimality**: "removing any single change would cause the failure to disappear". Removing two or more changes together might still give a smaller failing case, so the result is not a global minimum. The worst case, where every test is unresolved, is quadratic in the input size (the paper's bound is |c|² + 3|c| tests). [documented; the formula is garbled in the PDF text extraction] — [Zeller & Hildebrandt 2002](https://www.st.cs.uni-saarland.de/papers/tse2002/tse2002.pdf)
- **HDD (Misherghi & Su, ICSE 2006).** HDD applies ddmin level by level to a tree-structured input, from the coarsest level to the finest. Every configuration it generates is syntactically valid, which cuts the number of unresolved tests. On GCC and Mozilla inputs it gives "simpler outputs and takes orders of magnitude fewer test cases" than ddmin. Its worst case is still O(n²), reached when the input is a flat list, and the ideal case is O(log n) tests. [documented] — [HDD, ICSE 2006](https://web.cs.ucdavis.edu/~su/publications/icse06-hdd.pdf)
- **C-Reduce (Regehr et al., PLDI 2012).** Substring-based delta "typically yields test cases that are too large or even invalid (relying on undefined behavior)". C-Reduce runs a generic fixpoint over modular transformations. Its outputs are on average more than 25 times smaller than those of the authors' other reducers or of the most common existing reducer. The paper concludes that "effective program reduction requires more than straightforward delta debugging". [documented] — [Test-case reduction for C compiler bugs, PLDI 2012 preprint](https://users.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)
- **Perses (Sun, Li, Zhang, Gu & Su, ICSE 2018).** Perses uses the formal grammar so that each step considers only smaller, syntactically valid variants, and it supports transformations as well as deletion. It was evaluated on 20 C programs that trigger GCC/Clang bugs, plus Java. Its outputs are 45% of HDD's size (the corresponding figure against DD was cut off in the extract). It takes 23% of DD's time and 47% of HDD's, and 38–60% of C-Reduce's time even though C-Reduce is C-specialised. [documented abstract] — [Perses, ICSE 2018 author PDF](https://web.cs.ucdavis.edu/~su/publications/perses.pdf)
- **Hypothesis internal reduction (MacIver & Donaldson, ECOOP 2020, LIPIcs vol. 166, art. 13).** Hypothesis reduces "the sequence of random choices made during generation", not the generated test case. The result is generic reduction with no user-written reducer. It also "significantly mitigates ... the test-case validity problem", because any reduced test case is one the generator could have produced. On Csmith programs, "C-Reduce and Picire are able to achieve substantially smaller reduced programs than Hypothesis on average". The authors claim internal reduction is "good enough to be useful", not better than other reducers. On QuickCheck's synthetic shrinking benchmarks, Hypothesis was worse only on "binheap" (9.02 vs 9.0), and the differences were not significant. The paper calls generator-bundled shrinking "integrated" reduction and positions internal reduction as a form of it. [documented] — [MacIver & Donaldson, ECOOP 2020](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf)
- **Hypothesis stateful testing.** `RuleBasedStateMachine` "tries to generate not just data but entire tests", meaning sequences of rule applications. Failures print "a very short program that will demonstrate the problem", which "should generally be pretty close to Python code" and can be pasted into a test. The docs page does not describe the shrinking mechanism itself. [documented, docs page] — [Hypothesis stateful docs](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- **SQLancer reducers.** SQLancer has two reducers:
  - a statement reducer that runs ddmin over the generated SQL statement list;
  - an AST-based reducer built on JSQLParser. Its transformations remove UNION branches, clauses (OFFSET/LIMIT) and list elements, remove rows from an INSERT (`INSERT INTO t VALUES (1,2),(3,4)` → one row), replace expressions with sub-expressions, and shorten constants (3.27842156 → 3.278).

  Both are marked EXPERIMENTAL and are off by default (`--use-reducer`, `--reduce-ast`). Each oracle needs its own "reproducer". Reproducers exist only for SQLite3 NoREC and TiDB TLP-WHERE, and "if reproducer is not implemented for specific oracle, test case reduction is not available". The README says the team has "successfully used C-Reduce" with a scripted oracle. The reducers came from GSoC 2023. [documented] — [SQLancer docs/testCaseReduction.md (git clone, last commit 2026-11-15)](https://raw.githubusercontent.com/sqlancer/sqlancer/main/docs/testCaseReduction.md); [GSoC 2023 final report](https://sqlancer.github.io/blog/gsoc-sqlancer-final)
- **SQLess (Lin et al., ISSTA 2024).** SQLess is a dialect-agnostic SQL query simplifier. It uses an adaptive parser with error recovery and grammar extension, plus "semantics-sensitive" trimming based on alias and dependency analysis, "with preserving bug-triggering capability". It was evaluated on more than 32,000 queries across six DBMSs. On the PINOLO dataset its average simplification rate is 72.45%, which the paper says outperforms the state of the art by 84.91%. Its baselines include "ClauseDelete" tools such as SQLancer's reducer. [documented abstract and baseline section] — [SQLess, ISSTA 2024 author PDF](https://matafeiyanll.github.io/paper/Issta24.pdf)
- **SQLFlex (PACMMOD vol. 4 no. 3, SIGMOD 2026, art. 161; arXiv 2603.16155).** SQLFlex combines grammar parsing with LLM-based segmentation. The paper reports that SQLess's generated grammar rules "fail to produce ASTs that can be interpreted by rewriting rules". SQLFlex parses 91.55–100% of queries across eight dialects. [documented] The claim that it "outperforms SQLess by up to 10x" in simplification rate is a lead: the full-text sentence was cut off in my extract. — [SQLFlex arXiv](https://arxiv.org/pdf/2603.16155)
- **Other tools.**
  - `sql-reduce` (jonamuen) is another pass-based SQL reducer. [lead] — [sql-reduce](https://github.com/jonamuen/sql-reduce)
  - I found no reducer script in the DuckDB main repository (no file path matching "reduc" outside benchmarks and functions). [metadata, absence of evidence only]
- **Elle (Kingsbury & Alvaro, VLDB 2020).** Elle is not a delta-debugger. It infers transaction dependency graphs from client-observed histories. It "can detect every anomaly in Adya et al's formalism (except for predicates) ... and provide concise explanations of each". Its README says Elle "can point to a minimal set of transactions which witness a consistency violation", and its cycle plots show "as small a set of transactions as possible". [documented] — [Elle, arXiv 2003.10554](https://arxiv.org/pdf/2003.10554); README via git clone of jepsen-io/elle (last commit 2026-10-16)

**Tool catalogue [metadata, 2026-11-26]**

| Tool | Kind | Licence (LICENSE file / PyPI) | Latest release / last commit |
|---|---|---|---|
| picire (Hodován & Kiss) | ddmin implementation, parallel | BSD-3-Clause | PyPI 26.11, 2026-11-10; commit 2026-11-09 |
| picireny | HDD over ANTLR grammars | BSD | PyPI 21.8, 2021-08-25; commit 2025-11-23 |
| Perses | grammar-guided reducer | GPL-3.0 | commit 2026-11-24 |
| C-Reduce | C/C++ reducer with generic passes | University of Illinois/NCSA-style | commit 2024-06-01 |
| C-Vise | Python port of C-Reduce | licence file follows C-Reduce's format (not fully read) | commit 2026-11-23 |
| ddSMT | SMT-LIB delta debugger | MIT since 2.0.4 (GPLv3 before) | PyPI 2.0.6, 2025-06-30 |
| Shrink Ray (MacIver) | multiformat, parallel reducer | MIT | PyPI 26.9.13.0, 2026-09-13 |
| treereduce | tree reducer (README not read) | MIT | commit 2026-11-23 |
| Lithium (Mozilla) | reducer (README not read) | MPL-2.0 | PyPI 4.0.0, 2024-11-12; commit 2026-06-10 |
| halfempty (Project Zero) | parallel minimiser | Apache-2.0 | commit 2020-12-24 (dormant) |
| Hypothesis | PBT with internal reduction | MPL-2.0 | PyPI 6.170.17, 2026-11-20 |
| proptest (Rust) | PBT shrinking | Apache-2.0 (plus a second licence file) | commit 2026-10-10 |
| haskell-hedgehog | PBT, integrated shrinking | copyright header only seen | commit 2026-10-15 |
| QuickCheck (Haskell) | PBT shrinking | not checked | commit 2026-09-16 (v2.19.0.0) |
| SQLancer | DBMS fuzzer with ddmin + AST reducer | MIT | commit 2026-11-15 |
| Elle / Jepsen | history checkers, minimal witness cycles | EPL-2.0 (Elle) | Elle 2026-10-16; Jepsen 2026-11-24 |
| DEMi | distributed-trace minimiser | BSD-style copyright text | commit 2016-03-12 (unmaintained) |
| BigSift | Spark provenance + DD | no LICENSE file in repo root | commit 2021-09-29 (Docker/Zeppelin demo) |

### Inferences
- [inferred] ddmin and picire, HDD and picireny, Perses and Shrink Ray work on any serialisation the oracle can consume. That includes CSV or JSONL record files and event logs. They need no network and no knowledge of the data, so they can run inside a protected environment next to the real pipeline. Their output is still real data, so a separate value-replacement step must follow (see Q5).
- [inferred] For relational and multi-source data, the "validity problem" means candidates break referential integrity: a child row survives while its parent is removed, or a source record loses its cross-reference. Flat ddmin wastes oracle runs on such invalid candidates. HDD- or Perses-style reduction, with the schema graph playing the role of the grammar, is the closest documented analogue. No maintained tool does this for relational fixtures (absence of evidence, not proof the problem is unsolved).
- [inferred] Hypothesis-style internal reduction applies only when the failing input came from a generator. A real production extract has no choice sequence, so it cannot be shrunk this way unless it is first re-expressed through a generator.
- [inferred] Cost scales as (number of oracle runs) × (pipeline runtime). The quadratic worst case of ddmin and HDD makes per-run pipeline cost the dominant factor. The parallel tools (picire, Shrink Ray, halfempty) help only if the protected environment allows concurrent runs.

### Gaps
- The Picire/Picireny papers (Hodován & Kiss, A-TEST 2016; Coarse HDD, ASE 2017) were not fetched, so there are no empirical numbers for them here.
- ddSMT's paper was not read. The ProbDD and newer ddmin variants were not covered.
- No documentation was read for a SQLsmith or DuckDB-SQLsmith reducer. The sqlsmith repo clone failed (authentication prompt, likely renamed or private).
- The full texts on QuickCheck stateful/state-machine shrinking (Hughes et al.) were not obtained. Only the ECOOP paper's mention of integrated shrinking and the Hypothesis docs were read.

## Q2. Data-input reduction for dataflow and data pipelines (BigSift, Titian, provenance, smallest counterexample databases, explanation systems)

### Takeaway
Provenance-first reduction is the documented answer for pipelines. BigSift uses lineage to cut more than a billion records to about 15 before running ddmin. Miao, Roy and Yang (SIGMOD 2019) find the smallest sub-database on which two queries disagree, using provenance plus a solver. Explanation systems such as Scorpion return predicates rather than fixtures. These are all research prototypes: BigSift has been dormant since 2021, and I found no maintained OSS equivalent.

### Cited Findings
- **BigSift (Gulzar et al., SoCC 2017).** BigSift combines data provenance with delta debugging to find "a minimum set of failure-inducing inputs" for Spark jobs, given a user test function (for example, one that flags snowfall deltas above 6,000 mm). Compared with Titian provenance alone, it improves fault-localisation accuracy by about 10³–10⁷×. It is up to 66× faster than DD, and it localises fault-inducing data "within 62% of the original job running time". In one case, test-function-driven provenance cut the scope from more than 1 billion records to 15 records in 208 s, where DD needed 12,395 s. [documented] — [BigSift, SoCC 2017 camera-ready](https://people.cs.vt.edu/~gulzar/assets/pdf/socc17-final244-acmpaginated.pdf)
- The BigSift repository holds a Dockerfile, a Zeppelin configuration and data. The last commit was 2021-09-29 and there is no LICENSE file in the root. [metadata] — [UCLA-SEAL/BigSift](https://github.com/UCLA-SEAL/BigSift)
- An extended journal or tech-report version exists. [lead] — [par.nsf.gov 10101001](https://par.nsf.gov/servlets/purl/10101001)
- **Smallest counterexample database (Miao, Roy & Yang, SIGMOD 2019).** Given queries Q1 and Q2 and a test database D on which they differ, the method finds "the smallest counterexample D′ ⊆ D where Q1(D′) ≠ Q2(D′)". The problem is NP-hard in general. The authors give a provenance-based algorithm with a constraint solver for SPJUD queries and extend it to aggregation, group-by and nested queries. It was evaluated on student queries and TPC-H, with a classroom user study. Parameterisation reduced counterexample size by 70%, while solver runtime rose from 0.0134 s to 0.0210 s. The demo tool is called RATest. Keeping D′ ⊆ D is motivated by preserving "the same context for users by using the same data values". [documented abstract and passages] — [Miao, Roy & Yang, arXiv 1904.04467](https://arxiv.org/pdf/1904.04467)
- **Scorpion (Wu & Madden, PVLDB 6(8), 2013).** Given user-flagged outlier points in an aggregate result, Scorpion finds predicates over input tuples "that, when applied to the input data, cause the outliers to disappear". It uses an "influence" measure, and its algorithms run orders of magnitude faster than naive search. [documented abstract] — [Scorpion, PVLDB 2013](https://www.vldb.org/pvldb/vol6/p553-wu.pdf)

### Inferences
- [inferred] Reconciliation and entity-resolution defects match the "Q1 vs Q2" framing well. Wrong output against an expected or reference computation is exactly what a smallest-counterexample search minimises. A golden or previous pipeline version could serve as Q2 inside the protected environment.
- [inferred] For incremental processing, the reduction unit must include the batch or delivery boundary as well as the record (see Q3). BigSift and Miao et al. both assume a single static input.
- [inferred] Provenance-guided pre-pruning, then ddmin over the lineage-relevant records only, is the generalisable pattern. A platform that keeps record-level lineage (source id → resolved entity → output row) could implement it without BigSift itself.

### Gaps
- Titian (VLDB 2015), Rain (SIGMOD 2020), Data X-Ray (SIGMOD 2015) and explanation tables were not fetched. No claims are made about them.
- I tried to fetch Olston et al., "Generating example data for dataflow programs" (SIGMOD 2009, Pig ILLUSTRATE), and could not (the Stanford URLs returned non-PDF). [unreachable] It is highly relevant: it constructs small example data that is complete and concise for each operator.
- No search was run for program-slicing-based input reduction or why-provenance input slicing as standalone tools.
- No "dbreduce"-type tool was found. That is absence of evidence from a limited search, not proof none exists.

## Q3. Event, delivery and trace sequence minimisation

### Takeaway
Minimising event sequences is documented for distributed systems (DEMi, NSDI 2016), where it needs control over non-determinism: interposition on message delivery and timers. With that control it reaches 1×–4.6× of the optimal size. PBT state-machine shrinking (Hypothesis, QuickCheck, Hedgehog, proptest) is the maintained, everyday option, but it applies only to sequences produced by a generator. Elle gives minimal witness sets, not minimised histories.

### Cited Findings
- **DEMi (Scott et al., NSDI 2016).** DEMi minimises buggy executions of Raft (akka-raft) and Spark. Across 10 known and newly found bugs, its results are 1×–4.6× the size of optimal executions. It is about 14,000 lines of Scala and uses AspectJ interposition on Akka to "completely control when messages and timers are delivered". It minimises in three stages: external events first, then internal schedules (for example, leaving messages pending), then message contents. It targets 1-minimality, following ddmin. "Message fingerprints" are defined by hand, and the paper says this "does not require much effort". [documented] — [DEMi, NSDI 2016](https://www.usenix.org/system/files/conference/nsdi16/nsdi16-paper-scott.pdf)
- DEMi Table 1 examples:
  - raft-45: 2,160 events (108 external) → 1,183 after STSSched (8 external) → 23 after TFB, against an optimum of 22.
  - spark-2294: 1,000 (30 external) → 43 (3 external) after STSSched.

  Runtimes vary widely, from STSSched 14–330 s to raft-58a TFB at 43,345 s. Without divergent schedules ("NoDiverge"), raft-45 stays at 1,826 events. [documented] — [DEMi](https://www.usenix.org/system/files/conference/nsdi16/nsdi16-paper-scott.pdf)
- DEMi's repository was last committed 2016-03-12 and carries a BSD-style copyright (Scott, Panda, Brajkovic). [metadata] — [NetSys/demi](https://github.com/NetSys/demi)
- DEMi cites the authors' prior work, STS (SIGCOMM 2014, minimal causal sequences for SDN controllers), as the only other tool that solves replay without code analysis. [documented mention; STS itself not read]
- Hypothesis stateful tests print short, paste-able step programs. [documented] — [Hypothesis stateful docs](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- Elle points to a "minimal set of transactions which witness a consistency violation". [documented] — Elle README (git clone); [Elle paper](https://arxiv.org/pdf/2003.10554)
- The original ddmin paper already reduced an event sequence: 95 user actions to 3. [documented] — [Zeller & Hildebrandt 2002](https://www.st.cs.uni-saarland.de/papers/tse2002/tse2002.pdf)

### Inferences
- [inferred] A batch or incremental ingestion pipeline whose delivery order and reporting delays come from logged timestamps can usually be replayed deterministically. In that case, plain ddmin over the delivery list, with reporting-delay offsets treated as reducible attributes, covers most of DEMi's first and third stages without interposition. DEMi's schedule-search stage matters only if the bug depends on genuine concurrency.
- [inferred] A minimised delivery sequence should keep its arrival-order semantics (late or corrected records). Reducers that reorder elements, which ddmin does not, could create sequences that cannot occur in production. That is the validity problem again.

### Gaps
- The full texts of QuickCheck state-machine shrinking papers (Hughes, "Experiences with QuickCheck"; the Erlang `eqc_statem` documentation) were not read.
- No maintained OSS trace minimiser for non-PBT event logs was found beyond the generic reducers.
- Model-based trace reduction literature was not covered.

## Q4. Preserving defect-detection capability (slippage, cause reduction, test-suite reduction, readability)

### Takeaway
Reducing to "still fails" carries two documented risks:
- **Slippage.** The reduced input triggers a different bug. The paper reports this for 23% of reduced JavaScript cases, and says it is especially hard to avoid for silent wrong-output bugs.
- **Lost general fault-detection power.** ddmin-reduced suites have "little power for detecting new faults".

Defining the reduction criterion as preserving coverage (cause reduction) or killed mutants (Shi et al.) keeps much of the detection capability, at some cost in size.

### Cited Findings
- **Slippage (Chen et al., "Taming compiler fuzzers", PLDI 2013).** "When the original and reduced versions of a test case trigger different bugs, we say that bug slippage has occurred". It "is not hard to avoid for bugs that have an unambiguous symptom ... but it can be difficult to avoid for silent bugs such as those that cause a compiler to emit incorrect code".
  - GCC wrong-code: slippage occurred 15 times in 1,298 test cases.
  - GCC crash: there was one instance.
  - JavaScript: "23% of reduced JavaScript test cases triggered a different bug than the original".

  [documented] — [Chen et al., PLDI 2013](https://users.cs.utah.edu/~regehr/papers/pldi13.pdf)
- **Cause reduction (Groce, Alipour, Zhang, Chen & Regehr, ICST 2014).**
  - Delta-debugged random tests give "effective regression suites for previously detected faults, but such suites often have little power for detecting new faults, and in some cases provide poor code coverage".
  - Reducing with respect to statement coverage instead ("cause reduction") produced a SpiderMonkey suite that ran almost 4× faster and detected more distinct faults, including on a version more than 2 months later, with no re-reduction.
  - For YAFFS2, the coverage-reduced suite ran in a little over half the time and killed more than 99% as many mutants, including 6 the original did not kill.

  [documented] — [Cause Reduction for Quick Testing, ICST 2014 (Utah repository copy)](https://collections.lib.utah.edu/dl_files/8e/ea/8eea2537954679d0e007f1ad9620167d40d6772e.pdf)
- The extended version, "Cause reduction: delta debugging, even without bugs" (STVR 26(1), 2016), returned HTTP 503 from the author site. [unreachable] — [author PDF](https://www.cefns.nau.edu/~adg326/stvr15.pdf)
- **Shi, Gyori, Gligoric, Zaytsev & Marinov (FSE 2014).** The study covers 18 projects, 261,235 tests, 3,590 commits and 35 years of history. Statement-coverage-adequate suite reduction "loses up to 20.5% in killed mutants". Reduction based on killed mutants has no loss in killed mutants, at an 11.9-percentage-point increase in size. Prior studies had reported 40–50% fault-detection loss. The paper proposes evolution-aware metrics, because quality measured only on the reduction version misleads. [documented] — [Shi et al., FSE 2014](https://mir.cs.illinois.edu/awshi2/publications/FSE2014.pdf)
- **Validity and readability.** C-Reduce's authors found delta outputs "too large or even invalid". [documented] — [PLDI 2012](https://users.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf) Hypothesis outputs stay within the generator's validity guarantees, and the authors note that C-Reduce produced a "suspicious" printf with too many arguments. [documented] — [ECOOP 2020](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf) DEMi's authors say walking through a minimised execution event by event was the most fruitful debugging process. [documented] — [DEMi](https://www.usenix.org/system/files/conference/nsdi16/nsdi16-paper-scott.pdf)

### Inferences
- [inferred] Data-platform defects such as wrong reconciliation, a wrong entity merge or a missed late record are mostly silent wrong-output bugs, the class where slippage is hardest to avoid. The oracle should therefore check a specific signature (a particular output row or key, a particular assertion, a specific diff against the reference) rather than "output differs".
- [inferred] To keep regression value beyond the one known bug, reduce with a compound criterion inside the protected environment. One option is "still fails and still covers the same transformation, rule or branch set". Another is "still kills the same mutants of the pipeline code". This follows the cause-reduction and Shi et al. evidence, which comes from compilers and Java projects, not data pipelines.

### Gaps
- No empirical study of slippage or fault-detection loss for reduced data fixtures (as opposed to programs or test suites) was found.
- Holmes and Groce's later slippage and causal-distance work (ISSRE 2018) and "One test to rule them all" (ISSTA 2017, test normalisation) were not fetched.

## Q5. Reduction plus anonymisation: reduce inside, replace values, keep the failure

### Takeaway
Failure-preserving input substitution is documented in research: Castro et al. (ASPLOS 2008, path conditions), Camouflage (ICSE 2011), kb-anonymity (PLDI 2011), kbe-anonymity (ASE 2012), and Andrica & Candea's k-anonymous traces. I could not read the main full texts; these are leads, except Andrica & Candea. The one full-text empirical study (AST 2024) shows that naive anonymisation often breaks reproduction when the failure depends on narrow value domains. I found no maintained OSS tool that does "reduce, then replace values, then re-check the oracle".

### Cited Findings
- **Castro, Costa & Martin, "Better bug reporting with better privacy" (ASPLOS 2008, pp. 319–328).** The method replays the failing execution, symbolically executes the trace to get path conditions, and solves them for new inputs that follow the same failing path and reveal less private data. A lecture slide reportedly gives an example where only 4 bytes had to be revealed. [lead; full-text fetch returned HTML] — [MSR publication page](https://www.microsoft.com/en-us/research/publication/better-bug-reporting-with-better-privacy/); [slides](https://lara.epfl.ch/w/_media/sav09/slides-jula.pdf)
- **Camouflage (Clause & Orso, ICSE 2011, pp. 21–30).** Camouflage automatically anonymises failure-inducing field inputs while preserving the failure, and was evaluated on real applications. It extends Castro et al.'s general technique. [lead; no PDF found] — [ICSE 2011 page](https://2011.icse-conferences.org/content/camouflage-automated-anonymization-field-data.html); [researchr](https://researchr.org/publication/ClauseO11)
- **kb-anonymity (Budi, Lo, Jiang, PLDI 2011, pp. 447–457).** It combines k-anonymity with program-behaviour preservation, using symbolic execution to generate replacement database tuples that keep the same behaviour. The follow-up, kbe-anonymity (ASE 2012), addresses inference across data versions. [lead] — [kbe-anonymity, SMU](https://ink.library.smu.edu.sg/sis_research/1572)
- **Andrica & Candea (EPFL).** They "automatically transform execution traces in a way that preserves their utility for testing and debugging while ... providing k-anonymity to users", evaluated on a smartphone-app testing and bug-reporting system. [documented abstract; year not confirmed] — [EPFL infoscience 186762](https://infoscience.epfl.ch/record/186762/files/main.pdf?version=1)
- **Masserini, Ginelli, Micucci, Briola & Mariani, "Anonymizing Test Data in Android: Does It Hurt?" (AST 2024).** The study covers five privacy-preserving techniques, 19 bugs and 17 apps.
  - Local suppression of numbers reproduced failures 41% of the time.
  - Approximation and perturbation reached up to 63%, "at the cost of disclosing some information about the original value".
  - Some cases fell below 10% reproduction because only a tiny value domain triggers the bug (for example, only 29 February in leap years).
  - Noise addition on numbers reproduced all failures with 95% confidence, at a mean of 17–21 attempts and at most 59.

  [documented] — [arXiv 2402.07460](https://arxiv.org/pdf/2402.07460)
- Miao et al. deliberately keep D′ ⊆ D to preserve real data values for readability. That runs against anonymisation, and it means the smallest counterexample still contains real values. [documented] — [arXiv 1904.04467](https://arxiv.org/pdf/1904.04467)

### Inferences
- [inferred] Order of operations: reduce first, with the reducer and oracle inside the protected environment. Then substitute values in the few remaining records and re-run the same oracle after each substitution. Reduction shrinks the set of values to replace, and the oracle re-check guards against the reproduction failures Masserini et al. measured. Only the substituted, re-verified fixture leaves. This loop has no documented OSS implementation for tabular data.
- [inferred] For entity resolution and reconciliation, substitutions must preserve the relations the logic depends on, not just individual values. Examples are identifier equality and inequality across sources, fuzzy-match similarity bands, date ordering and reporting-delay offsets, and key formats. Path-condition approaches (Castro, kb-anonymity) capture this in principle, but need symbolic execution of the pipeline, which is likely impractical for SQL or Spark jobs. A cheaper alternative is search-based substitution, checked by the oracle.
- [inferred] The derived fixture can still leak through rare values that remain or through structure (k-anonymity concerns). An approval step on the outgoing fixture remains necessary. Licensed reference data inside the fixture may also need licence clearance, not just privacy clearance.

### Gaps
- The full texts of Castro 2008, Camouflage 2011 and kb-anonymity 2011 were not obtained, so their empirical results (how often the failure is preserved, how much information leaks) are unverified here.
- No documented industrial practice of "reduce in production, export an anonymised minimal fixture" was found. That is absence of evidence from a limited search.
- Commercial test-data subsetting and masking products were not surveyed (out of scope except as a capability reference).
