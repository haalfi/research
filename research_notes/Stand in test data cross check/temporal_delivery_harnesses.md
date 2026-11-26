# Test harnesses and simulators for temporal and delivery behaviour (Beam TestStream, Flink DataGen/test harnesses, SimPy, incremental-vs-full-recompute oracles)

Research date: 2026-11-26. Evidence labels:
- **documented**: I read the full text, source file or metadata record.
- **lead**: search extract only.
- **inferred**: my own reasoning.
- **vendor**: a vendor or project claim about its own product.
- **unreachable**: I could not retrieve it.

GitHub issue bodies were read in full through the GitHub search API. Downloads are in the scratchpad (`p3b_*` directories).

## 1. Apache Beam TestStream: control surface, runners, limitations, release, defect evidence

### Takeaway
TestStream is a scripted event source. It interleaves element additions (each with an explicit event timestamp), monotonic watermark advances and processing-time advances. Each step runs to quiescence, so tests can cover early, on-time, late and droppable data and the trigger panes they produce. It is not a generator: every element and every delay is written by hand.

Runner support is narrow:
- Java: DirectRunner, Flink in streaming mode with caveats, and Prism with exclusions.
- Python: always the bundle-based DirectRunner.
- Excluded from the Dataflow, Spark-batch and Kafka Streams runner test suites.

Its strongest defect evidence is against **runners**, not user pipelines. Several wrong-answer issues on Flink are still open, and a Prism late-data bug was fixed in October 2026.

### Cited Findings
- **Blog date and author (documented).** "Testing Unbounded Pipelines in Apache Beam" is dated 2016-10-20, with author `tgroh`. The Beam authors file maps `tgroh` to Thomas Groh (tgroh@google.com). — [blog source test-stream.md](https://raw.githubusercontent.com/apache/beam/master/website/www/site/content/en/blog/test-stream.md); [authors.yml](https://raw.githubusercontent.com/apache/beam/master/website/www/site/data/authors.yml); rendered at [beam.apache.org/blog/test-stream/](https://beam.apache.org/blog/test-stream/)
- **What it controls, per the blog (documented).**
  - TestStream "performs a series of events, consisting of adding additional elements to a pipeline, advancing the watermark of the TestStream, and advancing the pipeline processing time clock".
  - "the read waits for all of the consequences of each event to complete before continuing on to the next event".
  - Tests can show "that late-arriving data produces refinements when it arrives before the maximum allowed lateness, and is dropped after".
  - Lateness categories covered: "unobservably", "observably" and "droppably" late, and EARLY/ON-TIME/LATE panes.
- **Runner support in 2016 (documented).** The blog says only: "The TestStream transform is supported in the DirectRunner." The DirectRunner "directly controls the runner's system clock", so multi-minute processing-time triggers complete promptly.
- **Java API (documented).** Builder methods are:
  - `addElements(...)`, with the current watermark as timestamp or with explicit `TimestampedValue`s.
  - `advanceWatermarkTo(Instant)`: "The watermark must advance monotonically and cannot advance to … TIMESTAMP_MAX_VALUE".
  - `advanceProcessingTime(Duration)`.
  - `advanceWatermarkToInfinity()`.
  - `create(Schema)` for Row input.
  - The class Javadoc says a runner "must ensure that no more progress can be made in the Pipeline before advancing the state of the TestStream". — [TestStream.java](https://raw.githubusercontent.com/apache/beam/master/sdks/java/core/src/main/java/org/apache/beam/sdk/testing/TestStream.java)
- **Not part of the Beam model (documented).** The `UsesTestStream` category Javadoc says TestStream "is not a part of the Beam model but a special feature currently only implemented by the direct runner and the Flink Runner (streaming)". This comment predates Prism support. — [UsesTestStream.java](https://raw.githubusercontent.com/apache/beam/master/sdks/java/core/src/main/java/org/apache/beam/sdk/testing/UsesTestStream.java)
- **Python SDK (documented).**
  - The module docstring says "Provides TestStream for verifying streaming runner semantics. For internal use only; no backwards-compatibility guarantees."
  - Event classes are `ElementEvent`, `WatermarkEvent` and `ProcessingTimeEvent`.
  - It supports multiple output tags, each with its own watermark, and an `endpoint` for a remote TestStreamService. — [test_stream.py](https://raw.githubusercontent.com/apache/beam/master/sdks/python/apache_beam/testing/test_stream.py)
- **Python DirectRunner routing (documented).** The Python DirectRunner sends any pipeline containing TestStream away from both the FnApiRunner ("does not support streaming execution") and Prism ("Python SDK assumes the direct runner TestStream implementation is being used"). That leaves the BundleBasedDirectRunner. — [direct_runner.py](https://raw.githubusercontent.com/apache/beam/master/sdks/python/apache_beam/runners/direct/direct_runner.py)
- **The Python Dataflow runner never mentions TestStream (documented absence in that file).** — [dataflow_runner.py](https://raw.githubusercontent.com/apache/beam/master/sdks/python/apache_beam/runners/dataflow/dataflow_runner.py)
- **Runner test-suite exclusions (documented).**
  - **Dataflow Java:** excludes `UsesTestStream` in both `commonLegacyExcludeCategories` and `commonRunnerV2ExcludeCategories`. Runner v2 also excludes `UsesTestStreamWithProcessingTime`. — [dataflow build.gradle](https://raw.githubusercontent.com/apache/beam/master/runners/google-cloud-dataflow-java/build.gradle)
  - **Flink, streaming:** excludes `UsesTestStreamWithMultipleStages` ("BEAM-8598") and `UsesTestStreamWithProcessingTime`.
  - **Flink, batch:** excludes `UsesTestStream`.
  - **Flink, checkpointing suite:** excludes it with the comment "TestStreamSource does not support checkpointing". — [flink_runner.gradle](https://raw.githubusercontent.com/apache/beam/master/runners/flink/flink_runner.gradle)
  - **Spark:** excludes `UsesTestStream` in one suite. Elsewhere it says "TestStream using processing time is not supported in Spark" and excludes `UsesTestStreamWithMultipleStages`. — [spark_runner.gradle](https://raw.githubusercontent.com/apache/beam/master/runners/spark/spark_runner.gradle)
  - **Prism (Java):** excludes some tests, including "Prism doesn't support multiple TestStreams", `testProcessingTimeTrigger`, and "Some tests failed when using TestStream with keyed elements". — [prism java build.gradle](https://raw.githubusercontent.com/apache/beam/master/runners/prism/java/build.gradle)
- **Kafka Streams runner (documented).** "does not support `TestStream` … The `UsesTestStream` category is excluded"; "The Flink runner has a portable TestStream implementation that could likely be generalised." Open, 2026-08-05. — [apache/beam#39632](https://github.com/apache/beam/issues/39632)
- **Official testing guide (documented absence).** The "Test Your Pipeline" page source never mentions TestStream; a grep found zero matches. — [test-your-pipeline.md](https://raw.githubusercontent.com/apache/beam/master/website/www/site/content/en/documentation/pipelines/test-your-pipeline.md)
- **Latest release (documented).**
  - Beam **2.78.0** reached PyPI on 2026-11-17T20:05Z; Maven Central `beam-sdks-java-core` shows release 2.78.0, lastUpdated 20261117.
  - **2.77.0** reached PyPI on 2026-10-07. Licence: Apache-2.0. — [PyPI apache-beam JSON](https://pypi.org/pypi/apache-beam/json); [Maven metadata](https://repo1.maven.org/maven2/org/apache/beam/beam-sdks-java-core/maven-metadata.xml)
- **Defect evidence: wrong answers on runners (documented; issue bodies read).** Beam's own `TestStreamTest` validates-runner tests have exposed wrong answers on runners:
  - [#20843](https://github.com/apache/beam/issues/20843) "TestStream.testDiscardingMode gives wrong answer on FlinkRunner": an extra "alsoFinalLatePane" was emitted. Open; imported from BEAM-12039.
  - [#20844](https://github.com/apache/beam/issues/20844) testLateDataAccumulating on Flink: an unexpected `-1` appeared. Open.
  - [#20845](https://github.com/apache/beam/issues/20845) testFirstElementLate on Flink. Open; title only read.
  - [#20846](https://github.com/apache/beam/issues/20846) testLateDataAccumulating on Samza: count 2 where ≥3 was expected. Closed 2026-04-28.
  - [#19962](https://github.com/apache/beam/issues/19962) "TestStream broken across multiple stages in Flink" (BEAM-8598). Open.
  - [#18670](https://github.com/apache/beam/issues/18670) "Event time timer not firing with TestStream" (BEAM-3341). Open.
- **Recent late-data bug in Prism (documented).** [#40818](https://github.com/apache/beam/issues/40818), opened and closed 2026-10-26:
  - Title: "Prism admits expired aggregation input while pending work in a later window holds its output watermark … its physical output includes data for a window already past allowed lateness".
  - Reproduced with a four-event finite TestStream: B=4 at t=11s, then watermark→16s, then A=100 at t=5s, then →∞. The pipeline used 10-second fixed windows and allowed lateness of 5s.
  - This is the clearest documented case of TestStream exposing incorrect handling of late data in an engine.
- **Other Prism issues (documented).**
  - [#36965](https://github.com/apache/beam/issues/36965) "Prism panic when TestStream is followed by a stateful dofn". Closed 2026-09-06.
  - [#30083](https://github.com/apache/beam/issues/30083) Prism processing-time handling for TestStream, timers and ProcessContinuations. Closed 2026-05-02.
- **Search counts (lead-level count).** The GitHub search API returned 58 issues mentioning "TestStream" in apache/beam, many imported from Jira in 2022.

### Inferences
- TestStream is a precise **script player**, not a **generator**. It replays a hand-built, fully specified interleaving of data, watermark and clock. It has no notion of a delivery file, a source calendar, a duplicate rate or a correction (inferred from the API read). To use it for many-source delivery faults, an external generator (Hypothesis, SimPy or custom code) would have to emit the event script. TestStream would then be the deterministic executor on the DirectRunner (inferred).
- The issue history shows that TestStream semantics are themselves runner-dependent. A test passing on the DirectRunner does not certify behaviour on Flink, Spark or Dataflow (inferred from the open wrong-answer issues and exclusions).
- It does not change the earlier finding: TestStream is not an open generator of delivery faults (inferred).

### Gaps
- I did not read the bodies of #20845 or Jira BEAM-12036..12039. The rendered Javadoc for 2.77/2.78 was not fetched; the claims rest on master-branch source.
- I found no statement on whether Python TestStream works on the portable Flink runner from Python, beyond the Kafka Streams issue's remark about a "portable TestStream implementation" in Flink.
- I found no documented case of TestStream finding a bug in a *user* pipeline. That is absence of evidence from issue-tracker searches.

## 2. Apache Flink: DataGen connector / DataGeneratorSource and test harnesses; latest release

### Takeaway
Flink offers two generators:
- **DataGeneratorSource (DataStream API)** maps an index sequence `0..N-1` through a user function. It has built-in rate limiting and is deterministic only if that function is deterministic.
- **DataGen SQL connector** produces random or sequence columns. Options include `rows-per-second`, `number-of-rows`, min/max, `max-past` for timestamps and `null-rate`. It has **no seed option**.

Neither generator models late, duplicate or missing deliveries. Watermarks and timers are controlled through the operator test harnesses (`processWatermark`, `setProcessingTime`), which the docs say are "not part of the public API". Latest release is Flink **2.3.0**: Maven artefacts on 2026-06-14, announcement on 2026-06-25.

### Cited Findings
- **DataGeneratorSource (documented).**
  - It "produces N data points in parallel… splits the sequence into as many parallel sub-sequences as there are parallel source subtasks", supplying "index" values of type `Long` to a `GeneratorFunction`.
  - "The order of elements depends on the parallelism. Each sub-sequence will be produced in order."
  - Rate limiting: `RateLimiterStrategy.perSecond(100)` caps the overall rate across subtasks, and other strategies can limit "the number of records emitted per checkpoint".
  - "This source is always bounded"; using `Long.MAX_VALUE` makes it effectively unbounded.
  - Exactly-once holds "under the condition that the output of the GeneratorFunction is deterministic with respect to its input".
  - "it is possible to also produce deterministic watermarks right at the source based on the generated events and a custom WatermarkStrategy."
  - — [Flink docs datastream/datagen.md](https://raw.githubusercontent.com/apache/flink/master/docs/content/docs/connectors/datastream/datagen.md)
- **DataGen SQL connector (documented).**
  - By default it creates "an unbounded number of rows with a random value for each column"; `number-of-rows` bounds it.
  - Options: `rows-per-second` (default 10000), `fields.#.kind` (`sequence` or `random`), `fields.#.min/max`, `fields.#.max-past` ("Maximum past of timestamp random generator"), `fields.#.start/end`, `fields.#.null-rate`, `length` and `var-len`.
  - "If any column in a table is a sequence type, the table will be bounded and end with the first sequence completes."
  - Random timestamps resolve "a past timestamp relative to the current timestamp of the local machine", i.e. relative to wall-clock time.
  - The options table has no seed parameter (documented absence).
  - — [Flink docs table/datagen.md](https://raw.githubusercontent.com/apache/flink/master/docs/content/docs/connectors/table/datagen.md)
- **Operator test harnesses (documented).**
  - Harnesses: `OneInputStreamOperatorTestHarness`, `KeyedOneInputStreamOperatorTestHarness`, `TwoInputStreamOperatorTestHarness`, `KeyedTwoInputStreamOperatorTestHarness`, plus a `ProcessFunctionTestHarnesses` factory.
  - Example calls: `processElement(2L, 100L)` (value, timestamp), `processWatermark(100L)`, `setProcessingTime(100L)`, `getOutput()` and side outputs.
  - Note: "AbstractStreamOperatorTestHarness and its derived classes are currently not part of the public API and can be subject to change."
  - — [Flink docs dev/datastream/testing.md](https://raw.githubusercontent.com/apache/flink/master/docs/content/docs/dev/datastream/testing.md)
- **MiniCluster (documented).**
  - `MiniClusterWithClientResource` runs whole jobs on an embedded cluster.
  - The docs advise: inject test sources and sinks; "implement a custom *parallel* source function for emitting watermarks if your job uses event time timers"; test with parallelism > 1; test state correctness by enabling checkpointing and throwing from a test-only UDF to force a restart.
  - Same source as above.
- **Release (documented for artefacts, lead for announcement).**
  - Maven Central `flink-streaming-java` latest/release is 2.3.0, with the jar timestamped 2026-06-14 and metadata lastUpdated 2026-06-19.
  - The `apache-flink` 2.3.0 package reached PyPI on 2026-06-21. Licence: Apache-2.0.
  - Recent patch lines: 2.2.1 (2026-05-11), 2.1.3 and 1.20.5 (2026-06-12).
  - The announcement page is dated 2026-06-25 (lead: search extract).
  - — [Maven metadata](https://repo1.maven.org/maven2/org/apache/flink/flink-streaming-java/maven-metadata.xml); [PyPI apache-flink](https://pypi.org/pypi/apache-flink/json); [Flink 2.3.0 announcement](https://flink.apache.org/2026/06/25/apache-flink-2.3.0-release-announcement/)
- **`flink-connector-datagen` (documented).** Maven metadata shows latest 2.3.0, lastUpdated 2026-06-19. — [Maven metadata](https://repo1.maven.org/maven2/org/apache/flink/flink-connector-datagen/maven-metadata.xml)
- **DiffStream (documented).** This is a Flink differential-output testing library (Kallas, Niksic, Stanford, Alur; OOPSLA 2020, PACMPL 4, Article 153).
  - It checks "whether two implementations produce equivalent output streams… The notion of equivalence allows reordering of logically independent data items".
  - In its case studies it detected "5 out of 5 bugs" in benchmark MapReduce-style programs, i.e. user programs, not Flink itself.
  - Repo: MIT licence; last commit 2021-01-29 (dormant).
  - — [DiffStream paper PDF](https://www.cis.upenn.edu/~alur/OOPSLA20.pdf); [fniksic/diffstream](https://github.com/fniksic/diffstream), cloned

### Inferences
- "Rate-controlled deterministic" holds only for `DataGeneratorSource` with a deterministic function. The SQL DataGen random mode has no seed and wall-clock-relative timestamps, so it is not reproducible across runs (inferred from the options table).
- Lateness can be approximated with `max-past`, but only as a uniform-looking random backdating relative to now. No delivery batches, duplicates or gaps are generated (inferred). Realistic delivery faults would have to be coded in the `GeneratorFunction`.
- The harnesses give exact watermark and timer control at operator level, analogous to TestStream. This is test plumbing, not data generation (inferred).

### Gaps
- I did not search Flink Jira for DataGen-specific defects.
- I did not read the Flink 2.3.0 announcement page itself.
- I did not verify the RNG behaviour of the SQL DataGen random generator in source.

## 3. SimPy (and salabim, Ciw): DES capabilities, licence, release; use for data deliveries

### Takeaway
SimPy 4.1.2 is confirmed: the changelog dates it 2026-05-23, and the PyPI upload is 2026-05-24 UTC. It is MIT-licensed and marked Production/Stable. It is a maintenance release after a 2.5-year gap: 4.1.1 was 2023-11-12.

Its primitives fit arrival processes, outages and batching:
- processes and timeouts;
- `Interrupt` for breakdowns;
- `Resource`, `PreemptiveResource`, `Container` and `Store`.

I found **no documented use** of SimPy, or any DES engine, to generate data-delivery schedules for pipeline testing. Alternatives are salabim (MIT, very active, 26.0.9 on 2026-11-03) and Ciw (MIT, queueing networks, 3.2.7 on 2025-12-05).

### Cited Findings
- **Release and metadata (documented).**
  - PyPI: simpy 4.1.2, uploaded 2026-05-24T04:37Z; licence MIT; classifiers "Production/Stable" and "OSI Approved :: MIT License"; requires Python ≥3.8.
  - Previous releases: 4.1.1 (2023-11-13 UTC), 4.1.0 (2023-11-06), 4.0.2 (2023-07-30).
  - Source is on GitLab (team-simpy/simpy).
  - — [PyPI simpy JSON](https://pypi.org/pypi/simpy/json)
- **Changelog (documented).** "4.1.2 - 2026-05-23: [NEW] Support Python 3.13 and 3.14" plus test, lint and typing fixes. It has no new simulation features. — [CHANGES.rst](https://gitlab.com/team-simpy/simpy/-/raw/master/CHANGES.rst)
- **Resources (documented).**
  - `Resource`: "can be used by a limited number of processes at a time".
  - `PriorityResource`.
  - `PreemptiveResource`: "processes additionally may preempt other processes with a lower priority".
  - `Container`: "production and consumption of a homogeneous, undifferentiated bulk".
  - `Store`, `FilterStore` and `PriorityStore`: Python objects.
  - — [SimPy resources guide](https://simpy.readthedocs.io/en/latest/topical_guides/resources.html)
- **Interrupts (documented).** `process.interrupt(cause)` throws `simpy.Interrupt` into a process, detaching it from the event it waits on; the process can catch it and resume. — [Process interaction guide](https://simpy.readthedocs.io/en/latest/topical_guides/process_interaction.html)
- **Machine-shop example (documented).** "break_machine periodically interrupts the working process to simulate the machine failure". It uses exponential time-to-failure with MTTF 300 and a `PreemptiveResource` repairman. This is a direct template for source outages. — [Machine shop example](https://simpy.readthedocs.io/en/latest/examples/machine_shop.html)
- **No documented use for data deliveries (lead plus absence).**
  - Searches found only queueing, manufacturing and Poisson-arrival tutorials, plus SimPype, a SimPy add-on for message pipelines.
  - Nothing applies DES to data-delivery test schedules. — [SimPype on PyPI](https://pypi.org/project/simpype/1.1.0) (lead)
- **salabim (documented metadata).** 26.0.9 on 2026-11-03. Recent cadence: 26.0.5 (2026-04-17), 26.0.6 (2026-05-29), 26.0.8 (2026-06-24). MIT; Production/Stable. — [PyPI salabim JSON](https://pypi.org/pypi/salabim/json)
- **Ciw (documented metadata).** 3.2.7 on 2025-12-05, with releases roughly every 2–6 months since 2024. The LICENSE file is MIT (© 2015 Geraint Palmer); PyPI metadata carries no licence field. — [PyPI Ciw JSON](https://pypi.org/pypi/ciw/json); [Ciw LICENSE.txt](https://raw.githubusercontent.com/CiwPython/Ciw/master/LICENSE.txt)

### Inferences
- A SimPy model maps onto the delivery problem as follows (inferred):
  - each source is a process with a delivery calendar (timeouts drawn from fitted inter-arrival distributions);
  - an outage process interrupts it (machine-shop pattern);
  - a `Store` acts as the landing zone;
  - correction and re-delivery processes put duplicate or amended batches.
- The simulator's event log (logical event time, delivery time, batch id, duplicate/correction flags) becomes the input script for TestStream, a Flink harness, or a batch-replay harness. This mapping is mine, not documented anywhere.
- SimPy's low release cadence is not a risk for this use: the API is small and stable. It does, however, mean that "Mature; 4.1.2 released May 2026" overstates activity (inferred).

### Gaps
- I did not read the SimPy README (GitLab rate-limited the raw fetch). I did not check SimPy's documentation for `simpy.rt` (real-time).
- salabim and Ciw capabilities were not read in their docs; only metadata was checked.

## 4. Incremental vs full recompute as an oracle; fuzzing of streaming systems; documented bugs

### Takeaway
The "incremental result = full recompute" oracle is well documented in IVM engines:
- **Databricks Enzyme:** paper, vendor-authored.
- **pg_trickle:** project blog, project claim.
- **Materialize:** sqllogictest `--auto-index-selects`, source read.
- **Feldera:** vendor blog.
- **RisingWave:** batch versus streaming comparison, vendor blog.

Bug evidence:
- pg_trickle lists four delta-rule bug classes found this way (project claim).
- RisingWave claims "nearly 40 bugs" from SQLsmith (vendor).
- SQLxDiff (NUS, arXiv 2025) found 4 bugs in RisingWave among 57 bugs across four systems.
- Holey (arXiv 2026) found 10 wrong-result bugs in Flink 2.3.0, but in **batch mode**; it excludes streaming by design.

**ArrivalBench** (arXiv 2610.02363, Nov 2026) is the closest match to the user's problem. It generates replayable adversarial delivery schedules (late, out-of-order CDC, duplicate, crash-and-retry, backfill, schema evolution) and checks the final state against batch recomputation. However, it targets agent-written DuckDB pipelines, and **its harness is not yet released**.

So the earlier "no open generator" finding stands, but now with a published design precedent.

### Cited Findings
- **Enzyme (Databricks; arXiv 2603.27775v2, 30 Apr 2026) (documented; vendor-authored).**
  - "Enzyme employs multiple complementary strategies to validate correctness. The system leverages a Random Query Generator (RQG) framework to generate random schemas, synthetic data, and SQL queries… For each generated query, Enzyme creates an MV, applies randomized changes to source tables, and validates that the incremental refresh produces identical results to complete recomputation."
  - "To complement synthetic testing, Enzyme leverages an A/B correctness testing system for production workloads that compares MV contents to their definition queries", catching issues "under specific data distributions or timing conditions not covered by synthetic tests".
  - Fallback: "automatic fallback to complete recomputation when planning encounters exceptions… they often reveal bugs in the underlying query engine". Enzyme is "an effective stress test for uncovering optimizer and execution bugs in Spark itself".
  - No bug counts are given.
  - — [arXiv 2603.27775](https://arxiv.org/pdf/2603.27775)
- **pg_trickle (documented blog; project claim).**
  - Invariant: "the result of applying deltas incrementally must be identical to recomputing the query from scratch".
  - Shadow mode runs DIFFERENTIAL and FULL refresh each cycle and compares them row by row, as multisets; it "roughly doubles the refresh cost".
  - A fuzzer generates a random schema, an IVM-valid query and random DML, then compares against FULL.
  - Listed findings: NULL→non-NULL group-key transitions; zero-count groups left behind in some JOINs; JOIN-key and value updated in the same statement in a three-table JOIN; and `SUM(CASE WHEN x IS NULL …)` delta rules.
  - The blog calls the fuzzer "SQLancer-based" yet shows a `cargo fuzz` target. That is an internal inconsistency; treat the mechanism as unclear.
  - Package: 0.108.3, 2026-10-06, Apache-2.0, "stable", targeting PostgreSQL 18.
  - — [pg_trickle shadow-mode blog (md, v0.83.0 dist)](https://api.pgxn.org/src/pg_trickle/pg_trickle-0.83.0/blog/shadow-mode-correctness-fuzzing.md); [PGXN metadata](https://api.pgxn.org/dist/pg_trickle.json)
- **Materialize (documented, source read).**
  - The sqllogictest runner's `--auto-index-selects` option re-runs each successful SELECT through a generated view with `CREATE (DEFAULT) INDEX`, i.e. a maintained dataflow. On a mismatch it emits `InconsistentViewOutcome`. `AS OF` queries are excluded as "inherently racy".
  - The testing guide says sqllogictest ships "something like 6+ million" upstream tests, and that "Testdrive and sqllogictest have discovered numerous bugs with the fiddly bits of timestamp assignment". No counts are given.
  - Licence: Business Source License 1.1, so not open source.
  - — [runner.rs](https://raw.githubusercontent.com/MaterializeInc/materialize/main/src/sqllogictest/src/runner.rs); [guide-testing.md](https://raw.githubusercontent.com/MaterializeInc/materialize/main/doc/developer/guide-testing.md); [LICENSE](https://raw.githubusercontent.com/MaterializeInc/materialize/main/LICENSE)
- **Feldera (blog read via fetch tool; vendor; Lalith Suresh, 2024-12-06).**
  - It "passed all 5M+" SQLite SLT tests; nightly runs use a day-of-year subset.
  - Differential comparison against Postgres, SQLite, DuckDB, DataFusion, Snowflake and BigQuery.
  - It checks "whether the views we incrementally maintain match the results from the matching ad-hoc queries against base tables" using DataFusion.
  - proptest-based model testing of its pipeline-manager API against an in-memory model; Lean proofs of DBSP theory.
  - The SQLancer oracle "hasn't revealed any bugs yet". No bug counts.
  - It does not describe testing late or out-of-order inputs.
  - — [Correctness at Feldera](https://www.feldera.com/blog/correctness-at-feldera)
- **Feldera compiler docs (lead).** sqllogictests become DBSP circuits; for incremental mode, "the test code feeds multiple inputs and only checks the final output". — [sql-to-dbsp-compiler](https://www.github.com/feldera/feldera/blob/main/sql-to-dbsp-compiler)
- **RisingWave (blog read via fetch tool; vendor; Eddie Green, 2023-08-08).** "we generate and test the same query using batch and streaming computation engines"; "SQLSmith has already found nearly 40 bugs in Risingwave across the frontend, execution engines, and storage engine." — [RisingWave blog](https://risingwave.com/blog/how-randomized-sql-testing-can-help-detect-bugs/)
- **SQLxDiff (Jiang, Wang, Zhang, Yap, Liang, Rigger; NUS; arXiv 2501.01236, 2 Jan 2025) (documented).** It maps clauses of emerging systems onto a reference relational DBMS and found "57 previously unknown bugs (17 logic bugs and 40 internal errors)", "uncovering 6 bugs in TDEngine, 4 bugs in RisingWave". — [arXiv 2501.01236](https://arxiv.org/pdf/2501.01236)
- **Holey (Wu, Lee, Humayun, Gulzar, Kim; arXiv 2606.11132v2, 20 Oct 2026) (documented).**
  - Meta-property-based testing (aggregate decomposition, intermediate-materialization equivalence, and others) found "17 previously unknown wrong-result bugs", 7 in Spark 4.2.0 and 10 in Flink 2.3.0, all reported to Apache JIRA.
  - Flink ran in "PyFlink, batch mode". Example: "SUM and AVG on DECIMAL(38,s) over a join are rounded to scale 6".
  - Out of scope: "10 concern Structured Streaming… nondeterministic… which Holey's deterministic local campaigns exclude by design."
  - So this is not evidence about watermark or late-data semantics.
  - — [arXiv 2606.11132](https://arxiv.org/pdf/2606.11132)
- **sscheck (Riesco & Rodríguez-Hortalá; arXiv 1812.11838, 2018) (documented from header and body).** Property-based testing for Spark Streaming. It uses a first-order linear temporal logic (LTLss) over discrete batch-interval time to both generate input streams and state properties. Code at github.com/juanrh/sscheck; maintenance not checked. — [arXiv 1812.11838](https://arxiv.org/pdf/1812.11838)
- **ArrivalBench (P. Kothari, Oxford; arXiv 2610.02363v2, 19 Nov 2026; NeurIPS 2026 workshop) (documented).**
  - Method: "Each task defines a logical event log. A schedule partitions it into delivery batches, possibly duplicating events, reordering them, withholding and later releasing them, or aborting mid-batch." The pipeline runs once per batch against a persistent database, and "its final state must equal a batch recomputation of the complete logical log under every schedule".
  - Six hazards: late arrival, out-of-order change data, duplicate delivery, crash-and-retry, backfill, and additive schema evolution. Two benign controls ("single in-order batch and a multi-batch in-order stream") separate incrementality bugs from temporal ones.
  - Determinism: "The same (task, schedule, seed, artifact) yields byte-identical verdicts."
  - Result: single-execution grading certified 86–100% of agent-written pipelines; replay grading showed 7.0–79.2% silent failure.
  - Scope: 40 tasks, all on DuckDB, authored by one person.
  - Availability: "the harness, the tasks with their negative controls, the pre-registration and the verdict-level results will be released with the archival version of this work", so they are not yet released.
  - — [arXiv 2610.02363](https://arxiv.org/pdf/2610.02363)
- **pg_ivm (documented README).** It "supports PostgreSQL 13-19". `refresh_immv` with full recompute is available, which allows a user-built comparison. I found no documented incremental-vs-full fuzzing in the README. — [pg_ivm README](https://raw.githubusercontent.com/sraoss/pg_ivm/main/README.md)
- **dbt (documented docs page).**
  - Unit tests are "Available from dbt v1.8". They can override `is_incremental` to "unit test your incremental models in 'full refresh' and 'incremental' modes", with `this` mocked as an input.
  - The expected output is "the result of the materialization… not the resulting model itself".
  - "There is currently no way to unit test whether the dbt framework inserted/merged the records into your existing model correctly".
  - — [dbt unit tests](https://docs.getdbt.com/docs/build/unit-tests)
- **dbt full-refresh vs incremental comparison (lead).**
  - dbt-audit-helper provides `compare_relations`, `compare_and_classify_relation_rows` and related macros (README headings read).
  - Practitioner posts describe comparing a full-refresh build with an incremental build (lead).
  - — [dbt-audit-helper README](https://raw.githubusercontent.com/dbt-labs/dbt-audit-helper/main/README.md); [Medium practitioner post](https://medium.com/refined-and-refactored/dbt-incremental-implementing-testing-p2-967e8a8e4240) (lead)
- **Fuzzing streaming engines for temporal semantics (absence).**
  - Searches for 2022–2026 papers that fuzz Flink, Kafka Streams or Spark Structured Streaming for **watermark, late-data or temporal** semantic bugs found none.
  - The hits were Holey (batch), SQLxDiff (RisingWave SQL), the VLDB 2021 watermark-semantics comparison (not testing), and fault-recovery benchmarks.
  - — [Begoli et al. VLDB 2021](http://www.vldb.org/pvldb/vol14/p3135-begoli.pdf) (lead); [Fault recovery benchmark arXiv 2404.06203](https://arxiv.org/pdf/2404.06203) (lead)

### Inferences
- The oracle generalises directly: run the pipeline incrementally over a simulated delivery schedule, then compare its final state with a batch recompute over the deduplicated, corrected logical log. ArrivalBench documents this exact pattern; IVM engines document the narrower DML-sequence version.
- **Caveat 1 (inferred).** The oracle needs a *specification* of the correct final state under late or corrected data. For example, ArrivalBench grades "a watermark that drops late data" as a failure. A platform with deliberate cut-offs needs a reference that applies the same cut-off rules.
- **Caveat 2 (inferred).** Materialize's check compares a freshly created indexed view (initial hydration) with a one-shot query. That is weaker than checking deltas applied over time.
- **Does this change the earlier finding? Partly (inferred).**
  - Still no **open, released** generator of delivery faults: ArrivalBench's harness is unreleased, TestStream is a script player, and Flink DataGen has no fault model.
  - There **is** now a published, documented application of replayable delivery-schedule perturbation with a recompute oracle (ArrivalBench), so the claim should be updated from "none" to "one recent workshop paper, code pending".
  - It is not model-based testing of CDC in the formal-model sense. Its schedules are perturbation families, not derived from a state-machine model.

### Gaps
- I read no Noria testing material; nothing was found on Noria correctness testing.
- RisingWave's deterministic-simulation testing (madsim) was not covered by the page read.
- I did not read the Feldera compiler testing page in full.
- I did not open pg_trickle's fuzz targets in the repo, so the SQLancer-vs-cargo-fuzz inconsistency is unresolved.
- I did not check Databricks Lakeflow/DLT public docs for user-facing incremental-vs-full validation features.
- ArrivalBench's appendices on schedule generation parameters (e.g. lateness magnitudes) were not read in detail.

## 5. Fit: what parameters would have to be estimated inside the protected environment and exported (all inferred)

### Takeaway
None of these tools needs real rows: TestStream scripts, Flink generator functions, SimPy models and recompute oracles all run on fictional data. What they need from the protected environment is a small set of **delivery-process parameters**, aggregated per source or source class. That set is the export surface needing disclosure review.

### Cited Findings
- ArrivalBench's hazard families and benign controls are a documented checklist of what to parameterise: late, out-of-order CDC, duplicate, crash-and-retry, backfill and schema evolution. — [arXiv 2610.02363](https://arxiv.org/pdf/2610.02363)
- The SimPy machine-shop pattern parameterises outages by MTTF and repair time. — [SimPy machine shop](https://simpy.readthedocs.io/en/latest/examples/machine_shop.html)
- TestStream needs per-element event timestamps plus a watermark trajectory; Flink DataGen needs rates and `max-past`. — [TestStream.java](https://raw.githubusercontent.com/apache/beam/master/sdks/java/core/src/main/java/org/apache/beam/sdk/testing/TestStream.java); [Flink table datagen](https://raw.githubusercontent.com/apache/flink/master/docs/content/docs/connectors/table/datagen.md)

### Inferences
Candidate parameters per source or source class, estimated inside and exported after review (all inferred):
- **Delivery calendar:**
  - nominal cadence (daily, weekly, ad hoc);
  - inter-arrival distribution and its jitter;
  - day-of-week and holiday effects.
- **Lateness:**
  - distribution of (delivery time − event/reference time) as quantiles or a fitted parametric family;
  - tail weight (e.g. p95 and p99);
  - share beyond any platform cut-off.
- **Out-of-order rate:** fraction of records or versions arriving after a newer version of the same key, and the version-gap distribution.
- **Duplicates and re-deliveries:**
  - whole-file redelivery rate;
  - partial-batch overlap fraction;
  - within-batch versus cross-batch duplicate rates (ArrivalBench shows these behave differently);
  - time between original and re-delivery.
- **Corrections and retractions:** rate per delivery, back-dating depth distribution, and fraction that are reversals versus amendments.
- **Gaps and outages:** missing-delivery rate, outage duration distribution (MTTF/MTTR analogue), and burst or backfill size after outages.
- **Volume:** records per delivery (distribution) and growth trend.
- **Crash or partial-load rate:** truncated or aborted batches.
- **Schema events:** rate of additive or breaking format changes.

Disclosure considerations (inferred):
- These are aggregate process statistics, not entity values. However, per-source parameters for a small number of identifiable providers could still be commercially sensitive, so coarsen them or group sources.
- Extreme quantiles over small counts can reveal individual events.
- Differential-privacy noise or k-thresholding may be needed for small sources; this links to the DP track.
- The oracle side needs **no** export. A recompute-equals-incremental check can run inside the protected environment on real data, exporting only pass/fail and divergence counts (pg_trickle shadow-mode style). Exported divergence rows would need review.

### Gaps
- No source documents a parameter set for delivery-process simulation estimated from production and exported. This list is my construction.
- No source measured how well simulated delivery schedules reproduce real platform failures.

## 6. Verdicts on the external report's claims (sections 6.2, 9.5, 11 and references)

### Takeaway
The version and date facts are mostly right:
- SimPy 4.1.2 in May 2026: confirmed.
- The 2016 Beam blog: confirmed.
- Beam 2.77: partially confirmed, since 2.78 superseded it on 17 Nov 2026.

The capability characterisations overreach in two places:
- Flink DataGen is "deterministic" only for the DataStream source with a deterministic function.
- TestStream is listed under "fuzzing structured delivery formats", which it does not do.

"Mature/Active" labels are partly contradicted for TestStream: Python's own docstring says internal-use with no compatibility guarantees, it is unsupported on Dataflow, and there are open wrong-answer issues on Flink.

### Cited Findings
| # | Claim in external report | Verdict | Evidence |
|---|---|---|---|
| 1 | §6.2 "SimPy — Mature; 4.1.2 released May 2026" | **Confirmed** (date and version). "Mature" is reasonable; activity is low: 4.1.1 → 4.1.2 took 2.5 years, and 4.1.2 is maintenance only | [PyPI](https://pypi.org/pypi/simpy/json) (2026-05-24 UTC); [CHANGES.rst](https://gitlab.com/team-simpy/simpy/-/raw/master/CHANGES.rst) (2026-05-23) |
| 2 | §6.2 SimPy "Discrete-event simulation framework… Suitable for modelling arrivals, outages, schedules and interdependent events" | **Confirmed** as capability: processes and timeouts, interrupts, resources, stores, and the machine-shop breakdown example. "External simulator consumes approved parameters" is an architecture **inference**, not a SimPy feature | [resources](https://simpy.readthedocs.io/en/latest/topical_guides/resources.html); [machine shop](https://simpy.readthedocs.io/en/latest/examples/machine_shop.html) |
| 3 | §6.2 "Apache Beam TestStream — Mature; current APIs documented in Beam 2.77" | **Partially confirmed.** 2.77.0 exists (2026-10-07), but 2.78.0 was released 2026-11-17, so "current" depends on when the report was written. "Mature" is **partially contradicted**: the Python module says "For internal use only; no backwards-compatibility guarantees" and the Java category says "not a part of the Beam model" | [PyPI apache-beam](https://pypi.org/pypi/apache-beam/json); [test_stream.py](https://raw.githubusercontent.com/apache/beam/master/sdks/python/apache_beam/testing/test_stream.py); [UsesTestStream.java](https://raw.githubusercontent.com/apache/beam/master/sdks/java/core/src/main/java/org/apache/beam/sdk/testing/UsesTestStream.java) |
| 4 | §6.2 TestStream "Tests event time, processing time, watermarks and late data. No production rows needed." | **Confirmed.** Caveat: processing-time support is excluded on Spark and Dataflow v2 and in Flink streaming suites | [blog](https://raw.githubusercontent.com/apache/beam/master/website/www/site/content/en/blog/test-stream.md); [runner gradle files](https://raw.githubusercontent.com/apache/beam/master/runners/flink/flink_runner.gradle) |
| 5 | §6.2 "Useful even conceptually if the platform uses another processing engine" | **Unverifiable** (opinion); reasonable as inference. Note that executing it requires a Beam runner | — |
| 6 | §6.2 "Apache Flink DataGen — Mature, active project" | **Confirmed** for Flink: 2.3.0 in June 2026, and datagen connector artefacts at 2.3.0 | [Maven](https://repo1.maven.org/maven2/org/apache/flink/flink-connector-datagen/maven-metadata.xml) |
| 7 | §6.2 Flink DataGen "Rate-controlled deterministic streaming inputs" | **Partially confirmed.** Rate control is confirmed (`RateLimiterStrategy`; `rows-per-second`). Determinism holds only for `DataGeneratorSource` "under the condition that the output of the GeneratorFunction is deterministic". SQL DataGen random mode has no seed option and wall-clock-relative timestamps | [datastream datagen](https://raw.githubusercontent.com/apache/flink/master/docs/content/docs/connectors/datastream/datagen.md); [table datagen](https://raw.githubusercontent.com/apache/flink/master/docs/content/docs/connectors/table/datagen.md) |
| 8 | §6.2 Flink DataGen "Needs custom logic for realistic entity evolution" | **Confirmed** (inference consistent with docs: index→value function, or random/sequence columns only) | same |
| 9 | §9.5 table: "Apache Beam TestStream — Active — Controls event ordering, processing time and lateness in streaming tests" | **Partially confirmed.** The capability is right. It is miscategorised under "Fuzzing structured delivery formats": TestStream does no format mutation or fuzzing and generates nothing itself. "Active" holds: Prism TestStream fixes landed in 2026 | [#40818](https://github.com/apache/beam/issues/40818), [#36965](https://github.com/apache/beam/issues/36965) |
| 10 | References: "2016 Apache Beam, Testing Unbounded Pipelines. Article" | **Confirmed.** Title "Testing Unbounded Pipelines in Apache Beam", 2016-10-20, by Thomas Groh. The report gives no author | [blog source](https://raw.githubusercontent.com/apache/beam/master/website/www/site/content/en/blog/test-stream.md); [authors.yml](https://raw.githubusercontent.com/apache/beam/master/website/www/site/data/authors.yml) |
| 11 | References: "Current software, May 2026 release — SimPy. Documentation" | **Confirmed** (see #1) | — |
| 12 | §11.1 "Domain-specific temporal simulation — Custom modelling — Synthea patterns, SimPy"; §11.4 "Entity lifecycle simulation — SimPy" | **Unverifiable as a recommendation.** I found no documented use of SimPy for data-delivery or entity-lifecycle test data. Its fit is inferred from the primitives. The "Custom modelling" label is consistent with that | searches in §3 |
| 13 | §9.2 property "Incremental processing equals full recomputation, where specified"; §9.4 "Incremental reconciliation vs Full recomputation" | **Confirmed as an established practice in IVM engines:** Enzyme, pg_trickle, Materialize sqllogictest auto-index, Feldera, and RisingWave batch-vs-stream. ArrivalBench documents it for delivery schedules. The report cites no source for it | §4 sources |
| 14 | §9.4 "The previous release is not necessarily correct, so differential testing detects discrepancies rather than proving which implementation is correct" | **Confirmed** in spirit. Feldera compares against multiple engines; the oracle only finds disagreements (general testing principle) | [Feldera blog](https://www.feldera.com/blog/correctness-at-feldera) |

### Inferences
- The report's §6.2 implies these four tools jointly cover delivery behaviour. They do not (inferred):
  - TestStream and the Flink harnesses **execute** a hand-written timing script;
  - Flink DataGen **generates values** without delivery faults;
  - SimPy is a general DES kernel with no data-delivery library.
- The missing piece remains a delivery-fault generator. ArrivalBench's design shows one is feasible, but its code is unreleased.

### Gaps
- The report's "beam.apache.org+1" and "Apache Flink" citations are unspecific, so I could not tell which pages it read.
- I could not determine the report's writing date, which leaves the 2.77-versus-2.78 "current" status unresolved.
