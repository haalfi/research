# Independent evaluation of test fixtures and generated test data: real-fault benchmarks, data-intensive defect studies, evidence of unseen-defect detection, and limits of "representativeness"

Labels used on every claim: **[documented]** = full text read (PDF pulled and text-searched, 2026-11-26); **[lead]** = search-engine extract only, full text not read; **[inferred]** = my own reasoning from cited material; **[unreachable]** = full text could not be fetched; **[secondary]** = a result reported in a full-text survey or synthesis I read, not in the original paper; **[vendor]** = commercial claim (none used). Source dates are publication dates.

Limits of method: about 25 tool calls. Full texts came from arXiv, author PDFs and institutional repositories. core.ac.uk, the UMN conservancy and the Springer chapter for Hughes 2016 returned 403 or HTML instead of the PDF. Semantic Scholar rate-limited me (429), so I did not trace citation chains.

## Evaluation methods: real-fault benchmarks, held-out/historical faults, fault injection, mutation vs real faults, and circular evaluation

### Takeaway
The accepted way to judge a test-generation method without circularity is to count how many *real, developer-fixed faults* it detects in an artefact it was not tuned on (Defects4J, BugsInPy, CoreBench, historical issue trackers). Three findings qualify every proxy:
- Mutation score tracks real-fault detection only weakly once test-suite size is controlled.
- About 17–27% of real faults are not coupled to standard mutants.
- Optimising for coverage can make fault detection worse.

I found no curated real-fault benchmark for ETL, dbt or entity-resolution logic. The nearest are Spark framework correctness-issue sets, SQL-debugging datasets and BigFuzz/BigTest seeded-fault suites.

### Cited Findings
**Real-fault benchmarks and their quality**
- Defects4J (the version used in 2014–2015) holds 357 real faults from 5 Java programs (321 KLOC), each paired with a developer-fixed version and a fault-revealing test. **[documented]** — [Just et al., FSE 2014](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)
- BugsInPy holds 493 real bugs from 17 real-world Python projects. It is explicitly modelled on Defects4J and meant for controlled testing and debugging studies. **[documented]** — [Widyasari et al., BugsInPy (FSE 2020 demo; arXiv 2024-01)](https://arxiv.org/pdf/2401.15481)
- A critical review of BugSwarm (3,091 failing/passing CI build pairs) found only 112 of 3,091 pairs (3.6%) suitable for evaluating fault localisation or program repair. Benchmarks assembled automatically from CI can be dominated by non-behavioural failures. **[documented]** — [Durieux & Abreu, "Critical review of BugSwarm", 2019](https://arxiv.org/pdf/1905.09375)

**Generated tests scored against real faults**
- Three Java unit-test generators (Randoop, EvoSuite, AgitarOne) were applied to all 357 Defects4J faults:
  - Together the generated suites detected 55.7% of the faults, but only 19.9% of individual generated suites detected their fault.
  - Many faulty statements were covered without the fault being revealed, which points to weak propagation and assertions.
  - 15.2% of generated tests were flaky.
  - Faults depending on the environment, such as date and time, were hard to reach.
  - **[documented]** — [Shamshiri, Just, Rojas, Fraser, McMinn, Arcuri, ASE 2015](http://www.evosuite.org/wp-content/papercite-data/pdf/ase15_faults.pdf)
  - Caveat: the authors include EvoSuite's developers, so this is a tool-author evaluation, though on a third-party benchmark.
- Method detail that matters for any fixture evaluation: a test counts as detecting a fault only if it passes on the fixed version and fails on the buggy one. Suites were re-run five times on the fixed version to strip flaky tests. Date-dependent tests can still turn flaky later. **[documented]** — [Shamshiri et al. 2015](http://www.evosuite.org/wp-content/papercite-data/pdf/ase15_faults.pdf)

**Mutants as a stand-in for real faults**
- On 357 real faults and about 230,000 mutants:
  - Mutant detection correlates significantly with real-fault detection, independently of code coverage.
  - Only 73% of real faults are coupled to mutants from common operators.
  - 10% of real faults would need new or stronger mutation operators.
  - 17% are not coupled to mutants at all, which the authors call an inherent limitation.
  - **[documented]** — [Just et al., FSE 2014](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)
- Contrary result on CoreBench (C) and Defects4J (Java):
  - Once test-suite size is controlled, "all correlations between mutation scores and real fault detection are weak". The authors attribute the earlier strong correlations to the confounding effect of suite size.
  - Choosing the top suites by mutation score, rather than random suites of the same size, still improves fault detection significantly. Mutants are "good guidance" but weak predictors.
  - **[documented]** — [Papadakis, Shin, Yoo, Bae, ICSE 2018](https://coinse.github.io/publications/pdfs/Papadakis2018aa.pdf)

**Coverage as the optimisation target (the circularity risk)**
- Coverage-directed generation gave up to 93.4% worse fault detection than random tests on some systems with real faults. Random suites reduced to a coverage-providing subset detected up to 13.5% more faults than suites generated to achieve coverage. **[lead]** — [Gay, Staats, Whalen, Heimdahl, TSE 41, 2015, pp. 803–819](https://conservancy.umn.edu/bitstream/handle/11299/217451/15covrisks.pdf?sequence=1). The PDF returned 403; figures come from the search extract only.
- Inozemtseva & Holmes, ICSE 2014, "Coverage is not strongly correlated with test suite effectiveness". **[unreachable]**: the author PDF URL no longer resolves. Treat it as a title-level lead only.

**Practitioners lack a way to evaluate their generators**
- In 30 interviews at Jane Street (property-based testing users), "the difficulty of evaluating their effectiveness" was a main weakness of PBT. **[documented]** — [Goldstein et al., ICSE 2024](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice.pdf)
  - How participants judged their generators: inspecting example outputs (8/30), code coverage (2/30), property coverage (1/30).
  - A participant described the tension between "coverage of everything" and "coverage that is realistic for most inputs".
  - This is documented evidence that, in industrial practice, generators are seldom evaluated against anything independent of how they were built.

**Historical-bug replay (would the tests have caught past incidents?)**
- Holey (meta-property-based testing of Spark and Flink) was replayed against all 178 Spark issues labelled "correctness", resolved as fixed and created 2020–2025:
  - 107 were out of scope: data sources, file formats, other front ends, streaming or nondeterminism, or no wrong query result.
  - 71 were in scope, of which 65 were testable on a release.
  - The meta-properties could express 55 of the 65.
  - **[documented]** — [Wu, Lee, Humayun, Gulzar, Kim, arXiv 2606.11132 v2, 2026-10](https://arxiv.org/pdf/2606.11132)
  - "Express" is an expressiveness check: a property could be written for the issue. The paper does not show that the generator reproduced each historical failure from scratch. Tool-author evaluation.

**Fault injection on the real implementation (data-pipeline specific)**
- BigTest (white-box test generation for Spark applications with user-defined functions) was evaluated on manually seeded faults in 7 programs. It revealed about 2× more seeded faults than the earlier tool Sedge. **[documented]** — [Gulzar, Mardani, Musuvathi, Kim, FSE 2019](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)
  - Seeded fault classes include incorrect branch conditions and wrong join types.
- BigFuzz was evaluated on 52 error-seeded versions of 12 Spark applications. The error types came from a study of Spark and Hadoop errors on Stack Overflow and GitHub, which identified ten common error types. Examples are type mismatches, split/delimiter errors, wrong array or string indices, and swapped relational or arithmetic operators. It detected 80.6% more injected errors than BigTest. **[documented]** — [Zhang, Wang, Gulzar, Padhye, Kim, ASE 2020](http://web.cs.ucla.edu/~miryung/Publications/ase2020-bigfuzz.pdf)
  - Circularity caveat: BigFuzz's mutation operators and its seeded faults are drawn from the same error taxonomy. That is generator and evaluation sharing one criterion. **[inferred]**

**Benchmarks closest to ETL/SQL**
- "Squirrel" is a benchmark built from 268 erroneous SQL scripts from production logs, largely Hive/Spark SQL. It has 469 syntax-error and 516 semantic-error queries. **[lead]** — [Beyond Text-to-SQL: Can LLMs Really Debug Enterprise ETL SQL?, arXiv 2601.18119, 2026](https://arxiv.org/html/2601.18119)
- ELT-Bench and ELT-Bench-Verified are agent benchmarks for building ELT/dbt pipelines. They are not defect benchmarks. **[lead]** — [ELT-Bench, PVLDB 19](https://www.vldb.org/pvldb/vol19/p84-jin.pdf); [ELT-Bench-Verified, arXiv 2603.29399](https://arxiv.org/pdf/2603.29399)

### Inferences
- **[inferred]** A non-circular evaluation of fixtures for this platform has to separate three things: the criterion used to build or choose fixtures (coverage, partitions, rules), the criterion used to score them, and the fault set. The literature supports three scoring tiers:
  - (a) real historical faults of *this* codebase, replayed against the fixed and buggy versions;
  - (b) faults injected into the real implementation, where operators come from a defect taxonomy *not* used to build the fixtures;
  - (c) mutation score, used only with suite size controlled and only as guidance.
- **[inferred]** Mutation analysis misses 17–27% of real faults (Just 2014). Wrong-result, schema-evolution and cross-source semantic faults, for example identifier mismatches between sources, are a plausible part of that uncoupled share. The mutation operators in the cited studies are syntactic code changes and do not alter input semantics.
- **[inferred]** The Defects4J "pass on fixed, fail on buggy" protocol carries over directly to pipeline code if the repository keeps fixed incident commits.

### Gaps
- No curated, reproducible benchmark of real faults in ETL, dbt models, entity resolution or reconciliation logic turned up. The searches returned only Stack Overflow question-mining studies, framework-level Spark issue sets, SQL-debugging datasets and agent benchmarks. This is absence of evidence from about two targeted searches, not proof that none exists.
- Gay et al. 2015 and Inozemtseva & Holmes 2014 could not be read in full. The coverage-vs-effectiveness verdict above rests on the extract for Gay and on the documented Papadakis 2018 and Shamshiri 2015.
- I found no study that cross-validates a data generator against a criterion it was *not* optimised for, other than the indirect cases above: Wang 2017 for EvoSuite, and Gay 2015, lead only.

## Empirical studies of defects in data pipelines and data-intensive software: which defects fixtures must expose

### Takeaway
In the one large production study of data-parallel jobs, most failures came from data rather than code logic: 84.5% of 200 SCOPE failures at Microsoft Bing. 62% were row-level failures caused by "exceptional data", for example unhandled nulls. Repository-mining studies of pipelines point the same way: incorrect data types are the leading root cause (33%), and the data-cleaning stage is the most frequent location (35%).

These studies measure crashes and exceptions far better than silent wrong results, which they mostly exclude. That is a bias that matters for reconciliation and entity-resolution logic.

### Cited Findings
**Microsoft SCOPE production failures (Li et al., ICSE SEIP 2013)** **[documented]** — [Li et al., "A Characteristic Study on Failures of Production Distributed Data-Parallel Programs", ICSE SEIP 2013](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/icse13seip.pdf)
- Dataset: 200 SCOPE failures with their fixes and 50 failures with debugging statistics.
- 84.5% of failures were caused by "defects in data processing rather than defects in code logic".
- 22.5% were table-level failures, mainly programmer mistakes and frequent data-schema changes.
- 62% were row-level failures, "mainly caused by exceptional data".
- 93% of fixes did not change the data-processing logic. Fix patterns include setting default values for null columns.
- 8% had their root cause in an earlier stage than the one where the failure appeared.
- One job ran 13.6 hours and then failed on unhandled null values.
- The authors' implications:
  - "Local testing with a small portion of real input data could effectively detect table-level failures."
  - Row-level failures need exceptional-data handling informed by domain knowledge.
- Stated scope limits:
  - The study *excludes* jobs that finished with wrong results, because no oracles were available.
  - It excludes failures caught by developers' local testing before submission.
- One failure class came from a difference between environments: resource keywords not required locally made those failures invisible to local testing.

**Distributed data-intensive systems (Yuan et al., OSDI 2014)** **[documented]** — [Yuan et al., "Simple Testing Can Prevent Most Critical Failures", OSDI 2014](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-yuan.pdf)
- Failures come from issue trackers of production distributed data-intensive systems. I did not extract the number of systems or failures.
- 74% of failures are deterministic given the right input sequence.
- Almost all manifest on no more than 3 nodes, and most need no more than 3 input events.
- 77% can be reproduced by a unit test.
- 92% of catastrophic failures stem from incorrect handling of non-fatal errors that the software explicitly signalled.
- 58% of catastrophic failures could have been caught by simple tests of error-handling code. 35% follow three trivial patterns: an empty handler, aborting on an overly general exception, or a TODO/FIXME left in the handler.
- Failures "often require an unusual sequence of multiple events with specific input parameters from a large space".
- The authors' tool found bugs, 143 of which have been fixed or confirmed by developers.

**Pipeline repository mining (Foidl et al.)** **[documented]** — [Foidl, Golendukhina, Ramler, Felderer, "Data Pipeline Quality…", arXiv 2309.07067 (2023-09); JSS 2024](https://arxiv.org/pdf/2309.07067)
- Sample: 600 issues from 11 GitHub projects, plus 400 Stack Overflow posts.
- Data-related issues are "primarily caused by incorrect data types (33%)" and occur mainly in the data-cleaning stage (35%).
- Data integration and ingestion account for 47% of developer questions.
- "Compatibility issues" form a separate problem area.
- The paper also gives a 41-factor quality taxonomy validated by 8 expert interviews. Factors relevant here include data-type handling (type casting, delimiter handling, encoding), data-source quality, and the number of data models and sources and the ease of merging them ("joinability").

**Data-analytics programs (Ahmed et al.)** **[documented, abstract and methods only]** — [Ahmed et al., "Characterizing Bugs in Python and R Data Analytics Programs", arXiv 2306.08632, 2023](https://arxiv.org/pdf/2306.08632)
- Sources: 5,068 Stack Overflow posts and 1,800 bug-fix commits.
- Python shows significantly more data-preprocessing bugs than R. R shows more data-flow bugs because intermediate results are implicit.

**Spark application errors (BigFuzz study)** **[documented]** — [Zhang et al., BigFuzz, ASE 2020](http://web.cs.ucla.edu/~miryung/Publications/ase2020-bigfuzz.pdf)
- From Stack Overflow and GitHub, the authors identified ten common error types in Spark and Hadoop applications.
- Examples: type mismatch, split/delimiter errors, incorrect array or string access, incorrect logic (wrong relational or arithmetic operator).
- The same paper says byte-level random mutation "can hardly generate meaningful data, which fails to reveal real-world application bugs". Schema-aware mutation was needed.

**Coverage of real production data (BigTest)** **[documented]** — [Gulzar et al., BigTest, FSE 2019](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)
- Real DISC applications run on full production data are "often significantly skewed and inadequate in terms of test coverage, leaving 34% of Joint Dataflow and UDF (JDU) paths untested".
- Only tens of records were needed to reach the same JDU coverage as the entire production data.
- The paper notes that rare corner cases at this scale cause crashes or "silently produce corrupted output".

**Framework-level wrong results (Holey)** **[documented]** — [Wu et al., arXiv 2606.11132, 2026](https://arxiv.org/pdf/2606.11132)
- "Their most damaging bugs return silently wrong results rather than crashing."
- Example root cause: an aggregate pushed below a join is computed in a narrower integer type and overflows.

**Orchestration (Airflow)** **[lead]** — [Airflow developer-challenges study, arXiv 2406.00180, 2024](https://arxiv.org/pdf/2406.00180)
- Of 1,000 sampled Airflow Stack Overflow posts, 8.2% concern inherent version limitations such as bugs or unsupported features.

### Inferences
- **[inferred]** The fixture-relevant input features these studies name are:
  - nulls and missing values;
  - type and encoding mismatches;
  - delimiter and split anomalies;
  - schema changes between runs;
  - skewed key distributions;
  - out-of-range or overflow values;
  - specific multi-event *sequences*, as in Yuan 2014.
  Hand-written simple fixtures are unlikely to contain these unless they are written to do so.
- **[inferred]** Li 2013's 84.5% is a production *failure* rate for crash-type failures. It is not a share of all defects, and it says nothing about silent wrong results, which the study excludes. It should not be quoted as "84.5% of defects are data-triggered".
- **[inferred]** Li 2013's recommendation to test locally on a small portion of real data, together with BigTest's finding that tens of records match production JDU coverage, implies that a small derived sample can match production *path* coverage. It does not imply that such a sample matches production's *exceptional-value* content.

### Gaps
- No full-text empirical study was found of defects specific to:
  - entity resolution;
  - multi-source reconciliation;
  - incremental processing: late-arriving data, duplicates, reprocessing and backfill, out-of-order events.
  One targeted search on stream-processing bugs returned only fault-recovery benchmarks and patents. This is absence of evidence, not evidence the problem is unstudied.
- No found study measures what fraction of *all* production pipeline defects, including wrong results, are data-triggered. Li 2013 excludes wrong results. Foidl 2023 classifies root causes of data-related issues and does not give the share of data-related issues among all issues.
- "Vasudevan" and "Xu et al." Spark studies named in the brief were not located in this pass.
- Engineering-blog incident write-ups were not collected.

## Evidence that generated or fictional data finds real, previously unseen defects

### Takeaway
There is solid evidence that generated inputs find real, previously unknown bugs in mature *data-processing engines*:
- SQLancer/PQS: 123 bugs reported in SQLite, MySQL and PostgreSQL, of which 99 were fixed or verified by developers.
- Holey: 17 previously unknown wrong-result bugs in Spark and Flink.
- Yuan et al.'s tool: 143 bugs fixed or confirmed by developers.

Developer confirmation is an external check that the bugs are real. Almost all of this evidence is still self-reported by tool authors, mostly against engine code rather than application pipelines.

For application-level data pipelines, published evaluations rely on *seeded* faults (BigTest, BigFuzz). Industrial PBT evidence is mainly interview-based: 10 of 30 Jane Street users said PBT found bugs that other methods had not. EvoMaster's industrial study reports "potential faults" with a low fix rate.

### Cited Findings
**Database engines (SQLancer / PQS)**
- Pivoted Query Synthesis (SQLancer) reported 123 bugs in SQLite, MySQL and PostgreSQL, 99 of them fixed or verified. It targets logic bugs (wrong result sets): it builds a query whose result must contain a randomly chosen "pivot row". **[documented]** — [Rigger & Su, "Testing Database Engines via Pivoted Query Synthesis", OSDI 2020 / arXiv 2001.04174](https://arxiv.org/pdf/2001.04174)
- Tool-author report. Developer fixes give independent confirmation that the bugs are real.

**Spark and Flink frameworks (Holey)**
- 17 previously unknown wrong-result bugs: 7 in Spark 4.2.0, 10 in Flink 2.3.0. All were reported to developers. I did not read their confirmation status. **[documented]** — [Wu et al., arXiv 2606.11132, 2026](https://arxiv.org/pdf/2606.11132)
- 9 of the 17 need relations that existing SQL oracles such as TLP and NoREC do not state.
- "SQLancer could find none of the 17".
- 37 false alarms, fewer than 1 per 10,000 tests. Causes: floating-point rounding (15), overflow (18), and 4 defects in Holey's own type inference.
- This is a cross-tool comparison run by the authors of the new tool, not an independent replication.

**Spark applications (BigTest, BigFuzz): seeded faults only**
- Both report *seeded or injected* faults, not newly found real bugs. **[documented]** — [BigTest FSE 2019](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf); [BigFuzz ASE 2020](http://web.cs.ucla.edu/~miryung/Publications/ase2020-bigfuzz.pdf)
- Both are from the same research group, which also produced Holey.

**Property-based testing in industry**
- Jane Street interviews: 10 of 30 participants said their property-based tests found bugs not found by other methods. 9 of 30 explicitly said PBT increased confidence. Differential properties were the most widely used idiom. **[documented]** — [Goldstein et al., ICSE 2024](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice.pdf)
  - This is self-report by practitioners; the paper gives no measured defect counts.
- QuickCheck has been used at large scale to specify and test AUTOSAR basic-software implementations for Volvo Cars. Model-based, stateful generation is run against the real C implementation, with shrinking to minimal failing cases. **[documented]** — [Mostowski, Arts, Hughes, "Modelling of Autosar libraries for large scale testing", 2017](https://research.chalmers.se/publication/249538/file/249538_Fulltext.pdf)
  - The defect counts for the Volvo project are in Hughes 2016, "Experiences with QuickCheck: testing the hard stuff and staying sane" (LNCS 9600). **[unreachable]**: paywalled. The Chalmers record says it is "not a typical scientific paper" **[lead]** — [Chalmers record](https://research.chalmers.se/en/publication/232550).

**EvoMaster industrial use (Meituan)** **[documented]** — [Zhang, Arcuri et al., "Fuzzing Microservices: A Series of User Studies in Industry on Industrial Systems with EvoMaster", arXiv 2208.03988, 2022](https://arxiv.org/pdf/2208.03988)
- Up to 33.4% code coverage (average 18.1%).
- Up to 210 "potential faults" (average 64.8).
- "The fault fixing rate is low (i.e., around 10% reported by Meituan)".
- The authors confirmed findings with the industrial partner and did a joint manual analysis of the generated tests.
- Tool-author study. "Potential faults" are mostly HTTP-status-based oracles.

**Production-informed testing (PANKTI)** **[documented, evaluation summary only]** — [Tiwari et al., "Production Monitoring to Improve Test Suites", arXiv 2012.01198](https://arxiv.org/pdf/2012.01198)
- Monitored 86 weakly-tested methods in 3 open-source applications, observing 122,194 production invocations.
- Generated 14,222 differential unit tests from production objects; 97.6% pass.
- These tests capture *regressions* relative to observed production behaviour. They are not evidence of finding unseen defects.

**Field behaviour vs automatically generated tests** **[documented]** — [Wang, Brun, Orso, ICST 2017](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf)
- EvoSuite-generated tests added to in-house suites "slightly improved the test suites in terms of coverage, but not at all in terms of killed mutants and behavioral invariants".
- This is an evaluation by researchers who are not EvoSuite's authors.

### Inferences
- **[inferred]** The strongest "unseen defect" evidence comes from tools whose oracle does *not* depend on knowing the right output for a realistic input: metamorphic or pivot-row relations, differential properties, and error-handling checks. That matters here because fictional fixtures cannot carry real expected outputs from the protected environment, while relations such as invariance under re-partitioning, idempotent reprocessing, and order-insensitivity of merges can be checked on both fictional and real data. This is a capability inference, not a technique recommendation.
- **[inferred]** For application-level pipeline code, the brief's target, I found no independent replication showing that generated data finds previously unseen real defects. The evidence is seeded-fault and self-reported.

### Gaps
- No independent, third-party replication of BigTest, BigFuzz or Holey was found.
- The EvoMaster figures are author-reported. Almasi et al. (ICSE SEIP 2017), "An industrial evaluation of unit test generation: Finding real faults in a financial application", is cited in the EvoMaster paper but was not read **[lead]**.
- Hughes 2016 (Volvo/AUTOSAR defect counts) is unreachable. I found no Ericsson PBT figures with full text.

## Equivalence of fictional inputs to real inputs: theoretical limits and what instrumented comparison can establish

### Takeaway
Theory rules out a general guarantee that a test set chosen by partitions or criteria is equivalent to the operational input distribution for fault detection:
- Partition testing beats random testing only when partitions concentrate failures.
- Proportional sampling is the only partition strategy proven, under the model's assumptions, never to be worse than random.
- The "right" partitions are as unknown as the faults themselves.

Empirically, how equivalent tests look to field use depends entirely on the behaviour model. Wang et al. found tests missed only 6.2% of field statements, but 52.6% of field behavioural invariants and 8.6% extra mutant kills. BigTest found that tens of records match production path coverage.

Running fictional and real data through the same instrumented code can establish set differences: covered branches and paths, fired rules, invariants, mutants killed. It cannot establish equivalence with respect to unknown faults, or for wrong-result faults with no oracle.

### Cited Findings
**Partition testing theory**
- Hamlet & Taylor (TSE 16(12), Dec 1990) **[documented]** — [Hamlet & Taylor, "Partition Testing Does Not Inspire Confidence", TSE 1990](https://gwern.net/doc/cs/algorithm/1990-hamlet.pdf):
  - Partition testing "is shown to be more valuable when the partitions are narrowly based on expected failures and there is a good chance that failures occur. For gaining confidence from successful tests, partition testing as usually practiced has little value."
  - "Tests designed to expose failures are not representative, and tests representative of typical operation may seldom encounter failure situations."
  - Confidence in operation "can be gained only by testing that mimics the 'operational distribution'".
  - "If the right subdomains are the ones that find the unknown faults, those subdomains are equally unknown."
  - Their simulations show partition testing has a significant advantage only when the number of classes is of the order of the inverse failure rate, or failures concentrate in classes.
- Synthesis by Chen, Tse and Yu (2001), via the HKU TR **[documented as secondary]** — [Chen, Tse & Yu, "Proportional sampling strategy: a compendium and some insights", JSS 2001 (TR)](https://i.cs.hku.hk/~tse/Papers/2000s/typssTR.pdf):
  - Duran & Ntafos (1984) found by simulation that random testing was surprisingly competitive with partition testing.
  - Hamlet & Taylor (1990) and Loo & Tsai (1988) essentially confirmed this.
  - Weyuker & Jeng (1991) gave the first formal model.
  - Under certain conditions, the proportional sampling strategy is proved to be "the only form of partition testing that outperforms random testing regardless of where the failure-causing inputs are", measured by the probability of detecting at least one failure (Chen & Yu 1994, 1996, 2000).
  - With equal subdomain failure rates, proportional sampling equals random testing.
  - The originals were not read: **[lead]** for Duran & Ntafos 1984, Weyuker & Jeng 1991 and Chen & Yu 1994.

**Systematic vs random testing efficiency** **[documented]** — [Böhme & Paul, "On the Efficiency of Automated Testing", FSE 2014](https://www.st.cs.uni-saarland.de/~boehme/paper/FSE14.pdf)
- Under their model, a systematic technique S0 is more efficient than random testing R only if its per-input analysis cost stays below a bound, about (e·x − e·x²)⁻¹ times R's per-input cost for confidence x.
- Example: to show correctness on 90% of inputs with R at 10 ms per input, S0 must take under 41 ms per input. The bound depends asymptotically only on x.
- The paper also notes "We can never be sure!": confidence is probabilistic, not proof.

**Field vs in-house comparison (Wang, Brun, Orso, ICST 2017)** **[documented]** — [Wang, Brun, Orso, ICST 2017](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf)
- Setup: four real systems (including JetUML, Apache Commons IO and Commons Lang). Developer test suites were compared with recorded field executions under four behaviour models: statement coverage, method coverage, mutation score (libraries only, due to a record-replay limitation), and kTails temporal invariants.
- Tests missed on average 6.2% of field statements and 7.7% of field methods.
- Field-only behaviour killed an extra 8.6% of mutants.
- Tests missed 52.6% of field behavioural invariants.
- Some code exercised by both tests and field was exercised *differently*.
- Filtering trivial differences without filtering important ones is hard: different behaviour can execute the same statements in different orders.

**Coverage equivalence with tiny data (BigTest)** **[documented]** — [Gulzar et al., FSE 2019](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)
- Tens of records achieve the same JDU path coverage as the entire production data.
- The full production data still left 34% of JDU paths untested.
- The authors suggest building a minimised sample of production data by keeping records that cover not-yet-covered path classes.

**Mutation as an equivalence model** **[documented]**
- Real faults not coupled to any mutant (17%) cannot be detected by a mutation-kill comparison, by construction. — [Just et al. 2014](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)
- Equal mutation scores predict equal real-fault detection only weakly once size is controlled. — [Papadakis et al. 2018](https://coinse.github.io/publications/pdfs/Papadakis2018aa.pdf)

### Inferences
**What a run of both fixtures and real data inside the protected environment can establish**
- **[inferred]** A same-instrumentation run yields exact, privacy-light set differences: branches, paths, JDU paths, validation and reconciliation rules fired, invariants, mutants killed. These include "real data reaches rule R or path P; fixtures never do", and the reverse. These are facts about *this* code version and *this* data snapshot. Wang 2017 and BigTest 2019 show the method is feasible and informative.
- **[inferred]** The answer depends on the behaviour model. Coverage models showed small gaps in Wang 2017 (6–8%) while invariant models showed large ones (52.6%). Production data itself can leave a third of paths unexercised (BigTest). Claims of "equivalence" should therefore always name the model, and coverage-level equivalence is the weakest claim.

**What remains unknowable from that comparison**
- **[inferred, grounded in Hamlet & Taylor 1990, Just 2014 and Li 2013]** Three things stay out of reach:
  - (1) equivalence with respect to faults not yet known, since the "right" partitions are unknown;
  - (2) faults not coupled to any mutation operator;
  - (3) silent wrong-result faults on real data without an oracle. Li 2013 had to exclude these for lack of oracles.
- Also unknowable: whether equivalence on today's snapshot persists after schema changes or new source behaviour. Li 2013 attributes table-level failures partly to frequent schema changes.
- **[inferred]** Fault-detection comparisons are possible without moving data out by running the *same* mutants or injected faults against both fixtures and real data inside the protected environment, and exporting only kill sets. They still inherit the mutation-coupling limits above.

### Gaps
- No found study compares *fictional/synthetic fixtures vs real data* through the same instrumented data-pipeline code for rule-firing or mutation-kill equivalence. Wang 2017 compares developer tests with field use in general software. BigTest compares path coverage of generated and production data, not fault detection on real faults.
- I did not locate an explicit undecidability theorem for test adequacy or representativeness, such as Weyuker's adequacy axioms or Goodenough & Gerhart. The "unknowable" statements above rest on Hamlet & Taylor's argument and on inference, not on a formal theorem I read.
- Original papers by Duran & Ntafos (1984), Weyuker & Jeng (1991) and Chen & Yu (1994) were not read; they are covered only via the 2001 synthesis.
