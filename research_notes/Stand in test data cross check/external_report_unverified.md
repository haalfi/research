# External report (unverified input)

> Status: UNVERIFIED EXTERNAL INPUT. Produced independently by another system on `briefs/Synthetic stand in test data.md`
> and pasted by the user into the conversation on 2026-11-26. Reproduced verbatim as pasted; charts and diagrams
> in the original did not survive the paste and appear only as their residual text. Citation links were reduced
> to domain names in the paste. Nothing below is a finding of this repository; treat every claim as a lead.

---

Research report: production-representative synthetic test data
Research date: 26 November 2026
Executive summary
The problem described in the brief is substantially broader than conventional synthetic data generation. It sits at the intersection of statistical data synthesis, database benchmarking, entity resolution, microsimulation, statistical disclosure control and software testing.

The distinction is important. A dataset can be statistically very similar to production data and still be a poor substitute for testing the platform that processes it. Conversely, a dataset that deliberately exaggerates certain characteristics can be extremely valuable for correctness testing.

The research points towards five complementary approaches:
Approach	What it contributes
Statistical data synthesis	Representative distributions, dependencies and population characteristics
Workload-aware database generation	Realistic query cardinalities, joins, execution plans and performance
Entity and event simulation	Cross-source relationships, lifecycle changes, delivery behaviour and known ground truth
Statistical disclosure control	A controlled way to derive and release information from protected data
Generative software testing	Edge cases, expected outcomes, invariants and reproducible failures

There are established methods and usable open-source components in all five areas. However, I have not identified a mature, genuinely open-source product that combines them into a complete solution for a heterogeneous, multi-source data platform operating across a strict data protection boundary.

One particularly relevant strand of research is workload-aware synthetic database generation. Rather than asking whether generated data resembles real data in the abstract, it asks whether the generated database causes an application or database engine to behave similarly. Research dating back to 2011 explicitly treats query cardinalities, execution plans, resource consumption and execution time as measures of synthetic database utility. Touchstone (2018) subsequently demonstrated scalable generation using workload-derived constraints. 

people.cs.umass.edu+1

Another important finding is that synthetic data is not automatically anonymous. Statistical characterisations, trained generators and generated rows can all disclose information about their source. NIST's March 2025 differential privacy guidelines and empirical security research published at USENIX in 2022 provide particularly useful foundations for addressing this. 

csrc.nist.gov+1

Principal recommendation
Develop a versioned, disclosure-controlled characterisation of production data, with several specialised generators consuming it, rather than adopting a single generator as the solution.

Maintain separate but related test suites for:
- Small, deterministic correctness tests.
- Rare cases and failure scenarios.
- Production-representative integration tests.
- Full-scale performance and capacity tests.
- Longitudinal tests covering successive source deliveries.
Validate those suites against independently measured behaviour inside the protected environment.

This is a proposed synthesis of the research, not an existing standard or a claim that one tool already provides all these capabilities.
Reading conventions
Throughout the report:
- Documented: Supported by a paper, official documentation or source repository.
- Inferred: An engineering application or recommendation derived from established methods.
- Vendor claim: A capability described by a commercial provider without independent verification.
Maintenance assessments distinguish actively maintained software, established software whose current maintenance is uncertain, and academic research prototypes. Publicly available source code is not necessarily open-source software under an unrestricted licence.

1. What characteristics of real data must be captured?
The useful unit of characterisation is not necessarily a table or a column. It is whatever feature of the input influences the behaviour of the system under test.

That means characterising the data at several levels, including the files and events through which the data is delivered.
1.1 A catalogue of relevant characteristics
The following catalogue is an inferred engineering framework drawing on database statistics, statistical synthesis, record linkage and workload benchmarking.
Dimension	Characteristics to capture	Why they matter
Schema	Types, precision, optional fields, constraints, schema versions	Parsing, validation, compatibility
Individual values	Ranges, quantiles, frequency distributions, null rates, distinct counts	Filtering, transformations, storage
Value representation	Lengths, encodings, whitespace, precision, formatting variants	Parsing errors, compression, memory usage
Within-row dependencies	Conditional distributions, functional dependencies, correlated missingness	Business rules, derived fields
Within-table relationships	Uniqueness, duplicates, near-duplicates, clustering, outliers	Deduplication, grouping, indexing
Between-table relationships	Referential integrity, fan-out, orphan rates, many-to-many relationships	Joins, aggregation, memory consumption
Between-source relationships	Coverage, overlap, disagreement, identifier multiplicity, source precedence	Entity resolution, reconciliation
Population structure	Entity types, sizes, subpopulations, long-tail categories	Representativeness and coverage
Time and evolution	Births, deletions, transitions, corrections, seasonal patterns	Incremental processing and historical correctness
Delivery behaviour	Arrival times, batching, missing files, retries, ordering, backfills	Operational reliability and recovery
Physical data characteristics	Row width, compression ratio, sort order, partition sizes, file counts	I/O, shuffle, caching, parallelism
Workload characteristics	Predicate selectivity, intermediate join sizes, hot keys, query frequency	Execution plans, latency, throughput
Defects	Invalid relationships, malformed values, contradictions, missing identifiers	Failure handling and data quality
Change dependencies	Whether multiple sources change together or lag behind one another	Eventual consistency and reconciliation

The catalogue should be extended by investigating historical incidents and performance problems. Each newly understood failure can identify another characteristic worth measuring.
1.2 The particularly difficult characteristics
High-dimensional dependencies. It is relatively easy to preserve individual column distributions. Preserving combinations of ten or twenty attributes is substantially harder. The number of possible combinations grows rapidly, and many combinations may be sparse or entirely absent. The UK Office for National Statistics encountered this problem in its 2019 synthetic data pilot and recommends concentrating on the relationships needed for the intended use. 

Office for National Statistics

Cross-source overlap. Consider three hypothetical sources with 100,000, 80,000 and 60,000 entities respectively. Even knowing every pairwise overlap does not necessarily determine how many entities occur in all three sources.
Example: two populations with identical source counts
Each source contains 100 entities. Every pair shares 50 entities.Population 1
150 unique entities; none present in all three.

Population 2
200 unique entities; 50 present in all three.


Illustrative counts, not real data. The same basic statistics can produce very different reconciliation behaviour.
With many sources, the complete overlap distribution may itself become too large and disclosive. A selected set of intersections or a conditional coverage model is needed.

Skew and extreme entities. Average relationship cardinality can be almost irrelevant to performance. A million entities with three child records each behave differently from a population where a handful of entities have hundreds of thousands of children. Heavy hitters can determine the size of a join partition, the duration of a distributed job or whether memory is exhausted.

Temporal dependencies. Generating two statistically accurate snapshots independently will not reproduce realistic churn. Successive observations must be connected through stable synthetic identities and persistent state.

Physical representation. Identically distributed logical records can compress differently, trigger different execution plans and exhibit different I/O behaviour when their ordering, partitioning or encoding changes.

Rare cases. These are simultaneously valuable for testing, statistically difficult to estimate and potentially the most sensitive information to export.
1.3 Established tools for characterisation
Tool	Documented capabilities	Maintenance	Protected-boundary fit
Apache DataSketches	Approximate distinct counts, quantiles, frequent items and set operations	Active; releases in November 2026	Process real values inside. Export only approved statistics or privacy-protected results. Sketches are not inherently anonymous.  mail-archive.com
PostgreSQL planner statistics	Histograms, null fractions, distinct counts, common values, functional dependencies and multivariate statistics	Mature, active	Read the real database inside. Export sanitised statistics, not raw catalogues.  postgresql.org
Deequ	Spark-based profiling, constraint checks and historical quality metrics	Mature, active development in 2026	Run against production data inside. Export approved aggregate measurements.  GitHub+1
OpenMetadata	Data profiling, cataloguing, quality checks and lineage	Active 2026 releases	Operate internally. Metadata, sample values and query lineage need separate export controls.  GitHub
Splink	Probabilistic record linkage and deduplication across datasets	Active; version 5 announced in 2026	Link real records internally and derive approved overlap, ambiguity and matching statistics. Do not export linked entities.  Justice Digital, Data and Science

Assessment: Profiling and approximate aggregation are largely solved problems. Selecting the right relationships, cross-source metrics, temporal features and workload-sensitive characteristics is the part that remains application-specific.

One important warning from query-optimiser research: apparently innocuous statistics can contain actual production values. PostgreSQL's most-common-value lists and histogram boundaries are examples. Exporting an existing profiling report wholesale would therefore be inappropriate under the stated constraints.

2. Established methods for generating realistic stand-in data
There are four major families of methods worth distinguishing. They differ fundamentally in what they need to know about production data and what they retain.
Four possible generation paths. Passing the release gate is conditional, particularly for fitted models and transformed rows.
2.1 Generation from statistical characterisations
The simplest approach is to calculate distributions inside the protected environment and generate new values outside it.

More sophisticated versions incorporate joint distributions, conditional probabilities, copulas, graphical models and constraints.
Method	Strength	Limitation
Independent marginal sampling	Simple, scalable, readily auditable	Destroys dependencies
Conditional sampling	Preserves selected relationships	Requires decisions about which dependencies matter
Copulas	Reproduces dependencies separately from marginal distributions	Complex categorical and tail dependencies can be difficult
Bayesian networks	Represents conditional structure explicitly	Structure learning and sparse combinations are difficult
Iterative proportional fitting (IPF)	Constructs distributions consistent with supplied aggregate totals	Unmeasured interactions must be assumed
Constraint solving	Guarantees specified relationships and targeted query results	Can be expensive or difficult to scale
Maximum-entropy models	Provides a principled distribution subject to known constraints	Missing constraints mean missing behaviour

These are established statistical and mathematical techniques, not inventions specific to synthetic data.
Direct precedent: NHS England's artificial data generator
This is perhaps the closest documented precedent for the proposed protection boundary.

NHS England describes a production-data aggregation step, a formal disclosure review and a separate generation step that does not have access to real patient records. The project explicitly supports building and testing data pipelines.

Its pilot provides both 10,000-row samples and million-row datasets. The implementation uses independently sampled frequency distributions, followed by basic post-processing and dummy identifiers.

Crucially, the NHS explicitly acknowledges that relationships between fields are not preserved. This is a deliberate limitation of its approach, rather than an overlooked deficiency. 

NHS England Digital

For the platform in the brief, the approach is an excellent architectural starting point, but its statistical model is insufficient: cross-field and cross-source dependencies are central to the platform's behaviour.
Tool	Maintenance and status	Boundary and suitability
NHS Artificial Data Generator	MIT-licensed reference implementation; pilot, current code maintenance unconfirmed	Real rows needed only for profiling. Approved distributions leave. Strong architectural precedent, limited relational fidelity.  GitHub
simPop	Established R package; version 2.1.3, 2024-era release; CRAN checks still running in November 2026	Supports population synthesis and calibration. Some methods require source microdata; approved aggregates can constrain calibrated generation. Useful for structured populations.  jstatsoft.org+1
OpenDP	Active; version 0.16.0, October 2026	Constructs formally privacy-protected measurements. A good foundation for a releaseable characterisation, rather than a complete platform generator.  GitHub
SmartNoise Synth	Active; April 2026 package release	Fits against private data internally. Marginal-based methods such as AIM support synthesis from noisy measurements. Strong candidate for sensitive attributes, mainly single-table use cases.  PyPI+1

Assessment: Aggregate-driven generation is the strongest default for an architecture where external development environments must never access real data.

Its limitation is not principally the generation algorithm. It is deciding how much of the joint structure can be characterised, approved and released.
2.2 Statistical models fitted to real rows
A second approach fits a synthesiser directly to production rows inside the protected environment.

Examples include sequential conditional regression, classification and regression trees (CART), hierarchical modelling, copulas and deep generative models.

The fitted model can capture relationships that would be cumbersome to describe manually. However, such models are themselves derived sensitive artefacts. Exporting one does not automatically satisfy the data protection requirement.
Tool	Maintenance and status	Boundary and suitability
synthpop	Mature and active; version 1.9-3, September 2026; original paper 2016	Fits conditional models to real microdata internally. Approved synthetic output may leave. Interpretable and established in official statistics; not a general multi-source relational simulator.  cran.r-project.org
SDV Community	Mature and actively developed, but current Business Source License means it is source-available rather than conventional open source	Supports single-table, multi-table and sequential synthesis. Fit internally; model or synthetic export requires approval. Useful comparator, not an unqualified OSS recommendation.  GitHub+1
MOSTLY AI SDK	Available Apache-2.0 SDK from a commercial vendor; mature deployment characteristics of the local engine not independently verified here	Documented multi-table synthesis. Local fitting is an option to investigate; keep models inside until cleared. No assumption of formal privacy.  GitHub+1
PrivLava	Academic implementation accompanying a 2023 paper; not established production middleware	Differentially private synthesis across foreign-key relationships. Requires real relational data internally; approved DP outputs may leave. Particularly relevant research direction.  arxiv.org+1
DPSynth	Emerging open-source research library; explicitly working towards a stable release	Supports DP synthesis, including experimental relational capabilities. Real inputs remain inside. Worth evaluating but not yet a mature relational solution.  google-parfait/dpsynth · GitHub

There is a distinction between these tools and training ML systems on synthetic data, which is out of scope. Here, a statistical model is only used to generate structured test inputs.

Recent research, including PrivLava (2023), PrivPetal (2025) and Differentially Private Synthetic Data Generation for Relational Databases (JMLR, 2026), demonstrates that relational synthesis with formal privacy guarantees is an active research topic rather than a fully settled engineering problem. 

arxiv.org+2

2.3 Derivation from real rows: masking, perturbation and subsetting
A commonly used alternative in test data management is to take a production database and transform it:
- Replace identifiers and confidential attributes.
- Generalise or perturb sensitive values.
- Retain related records together.
- Extract a referentially consistent subset.
- Preserve selected structural characteristics.
This can produce exceptional fidelity compared with generation from a statistical description. It retains complex dependencies almost automatically.

It is also the approach least obviously compatible with the strictest interpretation of the brief.
Tool	Maintenance and status	Boundary and suitability
Jailer	Mature, active; project updates in 2026	Extracts relationally consistent subsets. Requires real rows and outputs real row subsets. Suitable for internal testing and preprocessing, not export as-is.  The Jailer Project Web Site
ARX	Mature anonymisation project, established releases; precise recent release cadence not established	Supports generalisation, suppression, microaggregation and multiple privacy models. Real rows processed internally; transformed microdata still needs release approval.  Data Anonymization Tool+1
sdcMicro	Established R statistical disclosure control toolkit; recent release cadence not independently checked	Real microdata transformed internally. Useful for disclosure risk analysis, but outputs are derived from original records.  researchdata.se
PostgreSQL Anonymizer	Established database masking extension; current upstream release cadence not verified here	Deterministic pseudonymisation can preserve joins. Real topology, unchanged values and potentially identifying relationships remain.  GitHub

The fundamental problem is that replacing every name and identifier does not necessarily remove the real information.

For example, a uniquely connected company with a distinctive number of subsidiaries and a particular acquisition history may remain identifiable after its name and identifiers have been replaced.

Assessment: Keep masking and subsetting available for use inside the protected environment. Do not make them the primary export mechanism unless the policy explicitly permits transformed microdata and the applicable licences permit it.
2.4 Workload-aware generation
This is the family of methods most directly concerned with reproducing application behaviour rather than generic statistical similarity.

The inputs are typically schema information, distributions and constraints derived from representative queries.

For example:
- A particular join should produce approximately five million intermediate rows.
- A filter should select roughly 0.01% of its input.
- One grouping key should account for a substantial proportion of all records.
- A particular combination of predicates should be strongly correlated.
The generator creates data satisfying those constraints.
Method or tool	Maintenance and status	Boundary and suitability
Generating Private Synthetic Databases for Database Application Testing, 2011	Foundational academic research	Explicitly connects privacy-preserving database synthesis with application workload fidelity. Excellent conceptual reference.  people.cs.umass.edu
Touchstone, USENIX ATC 2018	Research implementation; current maintenance and production readiness unconfirmed	Generator consumes schema, column properties and intermediate query cardinality constraints. Profiling occurs internally. Highly relevant for performance testing.  GitHub
MyBenchmark	Established academic workload-aware method, rather than a current mature software platform	Generates database instances targeted at input workloads. Useful design reference.  vldb.org
ezGen, 2023	Academic research	Translates query-based cardinality constraints into attribute-level constraints. Relevant to test workloads containing complicated queries.  EECS at UC Berkeley
LDBC SNB Datagen	Established benchmark generator; active repository in October 2026	No production rows required. Generates scalable, correlated graph data with temporal operations. An excellent implementation reference for entity relationships.  GitHub+1
TPC-H / TPC-DS	Mature benchmark specifications and available generator source; benchmark-specific terms apply	No production rows needed. Demonstrates scale factors, data and workload co-design. Fixed business domains limit direct adoption.  tpc.org

Assessment: Workload-aware generation is an essential complement to statistical synthesis for this use case. The methods are well established in research, but a general, maintained generator that can infer and reproduce arbitrary data-platform workloads remains difficult to find.
2.5 Representing the same entities across multiple sources
This deserves its own architecture. Relational synthesis based solely on foreign keys is not enough.

In a multi-source platform, records may refer to the same entity without sharing a common key. The absence, ambiguity or conflict of those relationships is often precisely what the platform is trying to resolve.

A more appropriate model is to generate a fictional underlying world, and then simulate how each source observes it.
Proposed entity-first generation architecture. Source records are observations of fictional entities rather than independently generated rows.
Each source projection can have its own probability of observing an entity, identifier scheme, attributes, reporting latency, duplicate rate and error model.

This enables testing not just whether joins work, but whether the system correctly resolves identities, handles contradictory observations and recovers from inconsistent deliveries.

There are direct precedents in record linkage:
- GeCo, Christen and Vatsalan (2013), generates fictional records and corrupts them using configurable error mechanisms. The original identities remain known for evaluating linkage. It is an older research tool, with current maintenance uncertain, but its design is very relevant. 
  
  ANU
- FEBRL, an older record-linkage research framework, is another useful source of synthetic duplicate and matching datasets.
- Splink is a mature, actively maintained linkage engine rather than a generator. It can help characterise real matching behaviour inside the boundary and assess synthetic matching workloads outside it.
- LDBC SNB demonstrates generation of structured, interconnected populations at large scale.
The proposed generalisation—one synthetic population, many independent but correlated source observations—is an engineering synthesis of these methods.

It is also one of the most important pieces that would need to be built for the platform.

3. How to demonstrate usefulness independently of the generation model
A major weakness of many synthetic-data evaluations is circularity.

If a generator is fitted to match twenty distributions and is evaluated only on how well it matches those twenty distributions, the evaluation shows that the fitting procedure worked. It does not establish that the resulting test data represents production behaviour.

The field of official statistics distinguishes general utility from use-specific utility. Snoke et al. (2018) provide established methods for both. 

academic.oup.com

The same distinction can be extended to platform testing.
3.1 A layered validation framework
Level	Evaluation	What it establishes
1. Structural	Schema, types, referential integrity	Can the platform ingest the data?
2. Statistical	Marginal and joint distribution comparisons	Are selected population characteristics retained?
3. Independent statistics	Measurements not supplied to the generator	Does the generator generalise beyond its fitting targets?
4. Workload utility	Execute equivalent workloads against both datasets	Does the platform exhibit similar processing behaviour?
5. Failure utility	Reproduce historical classes of incidents	Does the data exercise meaningful failure mechanisms?
6. Operational utility	Full delivery, update and recovery sequences	Does it test production-like operational behaviour?

The first two levels are necessary but insufficient.
3.2 Execute a reference workload inside the protected environment
This is the most important independent validation mechanism.

The real and synthetic datasets contain different entities, so comparisons generally must be between behavioural measurements rather than identical row-level output.

Useful metrics include:
Area	Measurements
Correctness-related behaviour	Match rates, unmatched records, ambiguous matches, conflict rates, rejected records
Transformation behaviour	Output/input ratios, grouping sizes, affected entities, branch frequencies
Query behaviour	Predicate selectivity, join cardinality, intermediate result sizes
Performance	Throughput, latency percentiles, CPU, memory peaks, spill, shuffle volume
Storage	Compressed size, file sizes, partition balance, index size
Incremental processing	Work amplification, changed entities, convergence time
Failure behaviour	Timeout rates, retries, exception categories, recovery outcomes

Compare performance using controlled environments, repeated runs, equivalent engine versions and configurations, with explicit treatment of cache state and concurrency. Otherwise, environmental differences may be mistaken for synthetic-data deficiencies.
3.3 An illustrative acceptance report
The following numbers are fictional and demonstrate how an independently measured fidelity report could look.
Workload fidelity
Real workload measurement normalised to 100%Input row count

100%




Joined row count

97%




Entity resolution candidates

94%




Peak memory

62%




Shuffle volume

71%




P95 batch duration

68%




This example would pass a basic volume comparison but materially underestimate production resource requirements.
Acceptance thresholds should be workload-specific. For example, a 10% join-cardinality discrepancy may be acceptable for one test but disastrous when it crosses the threshold at which the database changes its execution plan.
3.4 Relevant evaluation tools
Tool	Maintenance	Use and protection boundary
SDMetrics	Active development and releases	Evaluate statistical and relational similarity. Comparisons require real and synthetic data together inside the protected environment. Export reviewed scores. Not proof of workload equivalence.  GitHub
synthpop utility functions	Active September 2026 release	General and analysis-specific utility measures. Real versus synthetic comparisons run inside.
Deequ / GX Core	Active	Measure equivalent quality and behaviour metrics in both environments.
Database-native instrumentation	Mature, engine-dependent	EXPLAIN ANALYZE, query statistics, stage-level execution metrics. Internal query plans and logs require sanitisation.
LDBC/TPC workload harnesses	Established	Reference designs for repeatable load generation and measurement; adapt rather than expect domain compatibility.

There is no general utility score that substitutes for a representative platform workload.

There is also an important distinction between behavioural similarity and correctness. The real platform may contain bugs. Reproducing those bugs on synthetic data is valuable; treating the erroneous production outcome as the definition of correctness is not.

4. Disclosure, privacy and licensed reference data
This is a separate engineering problem from generation.

The protection boundary must control not only which rows leave but also which information about those rows leaves.
4.1 What different artefacts can disclose
Artefact	Potential disclosure
Minimum and maximum values	Individual extreme observations
Frequency tables	Rare attributes and membership of small groups
Histograms	Actual values used as boundaries
Joint distributions	Unusual combinations that identify entities
Cross-source overlap statistics	Commercial relationships, coverage and participation
Relationship graphs	Recognisable structures even without names
Hashed identifiers	Linkability and potentially recoverable low-entropy values
Statistical sketches	Membership, set intersections or encoded source values
Fitted models	Memorised records, membership and attribute inference
Synthetic rows	Replicated observations or revealing combinations
Repeated aggregate releases	Individual additions, deletions or corrections
Workload metrics and logs	Sensitive query literals, rare event counts or business activity

These are not merely theoretical concerns. Stadler, Oprisanu and Troncoso demonstrated limitations of synthetic-data anonymisation using empirical attacks in their 2022 USENIX Security paper. 

Anonymisation Groundhog Day

4.2 Established disclosure-control methods
Technique	Protection	Main limitation
Suppression	Removes small or sensitive groups	Overlapping releases may allow reconstruction
Generalisation	Replaces precise values with broader categories	Loses detail relevant to correctness
Top/bottom coding	Limits information about extreme observations	Hides extremes relevant to performance
Microaggregation	Replaces values with group summaries	Alters dependencies and variation
Perturbation and rounding	Reduces precision of released measurements	Ad hoc noise may be averaged away
k-anonymity	Limits uniqueness with respect to selected quasi-identifiers	Does not generally protect against attribute inference or composition
Differential privacy	Formally bounds the effect of an individual's or entity's data on releases	Requires careful definition of the protected unit and introduces utility loss
Empirical disclosure testing	Measures vulnerability under specified attacks	Passing tested attacks is not a formal privacy guarantee

4.3 Differential privacy is especially relevant to repeated releases
Suppose a characterisation contains the number of entities in a rare category. Yesterday's count was seven, and today's count is eight.

An observer with contextual knowledge might infer something about a newly added entity. Suppressing small counts or rounding individual reports is not necessarily sufficient when many related reports are available.

Differential privacy offers a formal framework for bounding cumulative disclosure, including through composition across multiple releases.

The most important choices for this platform are:
- Privacy unit: An entire person or entity, rather than an individual database row.
- Contribution bounds: Limit how much any one protected entity can affect the statistics.
- Privacy budget: Account for the cumulative information released over time.
- Domain selection: Avoid learning and exporting sensitive categories or boundaries without appropriate protection.
- Release scope: Decide whether privacy covers one source, all sources jointly, or the full entity history.
The distinction between row-level and entity-level protection is particularly important. A single entity appearing in thousands of records across several sources must not automatically be treated as thousands of unrelated privacy units.

NIST SP 800-226, published in March 2025, is the strongest general guidance identified for evaluating these guarantees. 

csrc.nist.gov

A useful property of differential privacy is post-processing: once a properly privacy-protected characterisation has been released, generating multiple datasets from that characterisation does not itself incur additional privacy loss under the same guarantee.

New measurements of the real data are different. Those consume privacy budget and need accounting.

Consequently, refreshing the characterisation and regenerating the test data should be separate operations.
4.4 The conflict between privacy and performance fidelity
Some characteristics of greatest interest to performance engineers are also particularly difficult to release safely.

Consider a real entity with unusually high connectivity. The system's worst-case performance depends on that connectivity. However, exporting its precise degree or associated attribute combination could reveal the entity.

A practical approach is to separate:
Production-derived information	Independently designed stress case
Approved coarse fan-out bands	Artificial entities with deliberately extreme fan-out
Approximate frequency distribution	Generated hot keys
General defect categories	Fictional examples of each defect
Approved latency distribution	Artificial source outages and extreme delays
Population-level overlap	Deliberate many-to-one and ambiguous matching cases

The stress suite does not need to disclose that a specific extreme case exists in production, or exactly how often it occurs.
4.5 Tools for privacy and disclosure assessment
Tool	Maintenance	Real-data access and export
OpenDP	Active, October 2026 release	Real contributions processed inside. Approved DP measurements leave.
SmartNoise	Active, April 2026 release	Internally fits or measures data; approved DP synthetic data or statistics leave.
ARX	Established	Operates on real microdata inside; assesses transformations and reidentification risks.
sdcMicro	Established; current maintenance uncertain	Internal risk assessment and statistical disclosure control.
TAPAS	Research-oriented privacy auditing toolbox; current release cadence uncertain	Uses source data and generators internally to test inference attacks. Only approved risk assessments leave.  alan-turing-institute/tapas · GitHub
Anonymeter	Established research implementation; recent maintenance uncertain	Evaluates empirical singling-out, linkability and inference risks. Requires protected access to comparison datasets.  GitHub

4.6 Licensed reference data is a separate constraint
A dataset can be privacy-safe and still violate a licence.

Differential privacy concerns the disclosure of information about protected units. It does not determine whether an organisation has contractual or intellectual-property rights to reproduce, derive, distribute or use a dataset.

A reference-data licence may distinguish between:
- Raw records.
- Derived data.
- Aggregated statistics.
- Models trained on licensed material.
- Data that can substitute for the licensed product.
- Internal testing and development.
- Redistribution to other environments, contractors or affiliates.
For example, a generator reproducing a substantial part of a commercial reference dataset's economically valuable structure could create a contractual problem even if it contains no original identifiers or personal data.

Where relevant, the EU Database Directive 96/9/EC also addresses extraction and reutilisation of protected database contents, including certain repeated and systematic extractions of insubstantial portions. 

EUR-Lex+1

The applicable rights depend on jurisdiction and the actual licence agreements.

Recommendation — inferred: Implement per-source export policies. A characterisation derived from multiple datasets should retain the provenance and applicable restrictions of each source.

A privacy approval should not implicitly constitute a licence approval.

5. Serving correctness and performance from one characterisation
Production-representative generation and effective testing are not identical objectives.

If an important edge case occurs once in a million records, a realistically sampled thousand-row fixture will almost always omit it. The correct response is not necessarily to generate larger datasets for every test.

Instead, use several generation policies over a common descriptive model.
One characteristic, three test-data policies
Illustrative frequency of unusual or exceptional casesProduction-representative



Statistically representative performance and integration tests
Edge-case enriched



Small fixtures with intentionally increased coverage
Targeted adversarial



Stress, robustness and failure handling

Ordinary cases

Exceptional cases


5.1 Recommended suite types
Suite	Generation strategy	Purpose
Minimal regression	Explicit, deterministic cases	Reproduce known defects
Edge-enriched	Stratification, quotas, conditional sampling	Exercise rare behaviour
Representative	Sample fitted distributions at realistic proportions	Integration and normal behaviour
Full-scale	Distributed generation with realistic skew and physical structure	Capacity and performance
Adversarial	Deliberately exceed expected ranges or violate assumptions	Robustness and resilience
Longitudinal	Persistent entities and simulated deliveries	Incremental and recovery behaviour

A shared characterisation should specify both the normal distribution and the supported scenario space. The generation policy decides which parts of that space to exercise.

It should not force every generated dataset to match production distributions.
5.2 Established techniques to adapt
Stratified sampling: Divide the population into meaningful groups and deliberately allocate test cases to underrepresented strata.

Conditional generation: Generate records satisfying a specific combination of characteristics—for example, an entity present in three sources but with incompatible identifiers.

Combinatorial testing: Cover selected interactions between input characteristics without exhaustively testing their Cartesian product. Pairwise or higher-order covering arrays can reduce the number of fixtures substantially.

Boundary-value and equivalence-class testing: Concentrate tests on values and transitions that are likely to produce different system behaviour.

Scale-factor generation: Adopt database benchmark practices to generate increasingly large instances while preserving or intentionally varying their relevant structure.
5.3 Generation tools
Tool	Maintenance	Boundary and suitability
Faker	Mature, active; November 2026 releases	No real rows required. Seeded fictional values, locale-aware attributes. Good building block, not a statistical population synthesiser.  PyPI
dbldatagen	Established Spark generator; published package release July 2024, more recent repository activity	Generates large datasets using configurable distributions, dependencies and ranges. Only approved parameters required externally. Strong scalable implementation candidate.  GitHub+1
Hypothesis	Mature, active 2026 documentation	Generates structured inputs, targeted conditions and sequences. No production rows required. Ideal for correctness tests rather than bulk generation.  Hypothesis 6.170.17 documentation
LDBC SNB Datagen	Active	Demonstrates large-scale correlated generation and configurable scale factors.
TPC generators	Mature	Reference designs for deterministic benchmark populations and scale factors.

When scaling a dataset, explicitly specify which characteristics should grow and which should remain fixed. Doubling the number of entities need not double the number of source categories, the fan-out of each entity or the number of files.

Otherwise, a nominal scale factor can alter the nature of the workload.

6. Reproducing data evolution, corrections and deliveries
A realistic snapshot is insufficient for testing a platform that ingests external data repeatedly.

Three different timelines must be modelled:
1. Real-world time: When the entity or relationship changes.
2. Source observation time: When the external provider observes, records or corrects the change.
3. Platform arrival time: When the information reaches the platform.
A single real-world event may appear at different times in different sources, then be repeated or corrected.
6.1 Generate a persistent world and event history
Illustrative synthetic entity history
One fictional entity, two sources and successive deliveriesIndependent snapshots cannot reproduce this history because the identities and causes of changes must persist across deliveries.
The simulator should model:
Event family	Characteristics
Population churn	New, removed, merged and split entities
Attribute updates	Frequency, type, magnitude and dependencies
Relationship changes	New links, removals, changes in cardinality
Source visibility	Entities entering or leaving provider coverage
Corrections	Historical amendments, reversals, backdated events
Re-deliveries	Identical files, partially repeated batches, repeated records
Ordering	Late arrivals, out-of-order versions, inconsistent sequences
Availability	Missing deliveries, gaps, outages, bursts
Format evolution	Schema changes, new enumerations, version transitions

Some behaviours can be modelled using empirical transition probabilities. Others require stateful simulation or explicit rules.
6.2 Relevant neighbouring fields and tools
Method or tool	Maintenance	Fit and boundary
Synthea	Mature, active in 2026	Generates longitudinal fictional patient histories using state-based modules. No private patient rows required. Strong architectural precedent for generating entities before observations.  GitHub+2
SimPy	Mature; 4.1.2 released May 2026	Discrete-event simulation framework. External simulator consumes approved parameters. Suitable for modelling arrivals, outages, schedules and interdependent events.  PyPI
LDBC SNB Datagen	Active	Generates time-dependent interconnected populations, including insertions and deletions. Good benchmark precedent.  GitHub
Apache Beam TestStream	Mature; current APIs documented in Beam 2.77	Tests event time, processing time, watermarks and late data. No production rows needed. Useful even conceptually if the platform uses another processing engine.  beam.apache.org+1
Apache Flink DataGen	Mature, active project	Rate-controlled deterministic streaming inputs. Needs custom logic for realistic entity evolution.  Apache Flink
Hypothesis state machines	Active	Generates sequences of updates, retries and deletions, and shrinks failing sequences. Particularly useful for small stateful correctness tests.

6.3 Why healthcare is especially relevant
Healthcare simulation has had to address a similar problem: records should represent coherent histories of fictional entities across multiple types of observation.

Synthea does this by modelling patients and their progression through states, rather than independently synthesising hospital visits, medications and diagnoses.

The transferable pattern is:

Simulate the domain, then generate the records describing it.

For the platform described in the brief, this means simulating the underlying entities, relationships and changes before generating the separate provider feeds.

This is likely to be more effective than fitting a generic time-series synthesiser to each source independently.

7. Detecting drift, renewing the data and preserving reproducibility
There are two distinct problems:
- Detecting when the current synthetic dataset is no longer representative of production.
- Preserving the ability to reproduce failures discovered using earlier datasets.
The first requires change. The second requires immutability.

They should not be solved by overwriting test datasets every time production changes.
7.1 What constitutes drift?
Drift type	Example	Detection method
Schema drift	New field or changed type	Schema comparison
Marginal drift	Increased null rate	Proportion comparison
Distribution drift	Shift in entity size	Quantile distances, Wasserstein distance, KS tests
Dependency drift	Two attributes become correlated	Joint or conditional distribution comparison
Relationship drift	Increased records per entity	Fan-out distributions
Coverage drift	Provider begins covering a new population	Source coverage and overlap metrics
Temporal drift	Corrections become more frequent	Transition and churn statistics
Delivery drift	Source delivery becomes more irregular	Arrival-delay and batch-size distributions
Workload drift	Previously minor processing path dominates execution	Workload instrumentation
Failure drift	New malformed input category emerges	Error taxonomy and incident metrics

There is no reason to assume that conventional column-level drift detection will catch changes in cross-source relationships or operational behaviour.
7.2 Statistical techniques
Established methods include:
- Kolmogorov–Smirnov tests for distribution differences.
- Chi-square tests for categorical frequencies.
- Jensen–Shannon and Wasserstein distances.
- Population Stability Index.
- Quantile and percentile comparisons.
- Exponentially weighted moving averages and control charts.
- CUSUM and other change-point detection methods.
At production scale, statistical significance alone is often an unsuitable alerting criterion. Very small, operationally irrelevant changes can be statistically significant.

Use a combination of effect size, persistent change and estimated impact on the platform.

For example, a 20% increase in an already extreme join fan-out may deserve more attention than a statistically significant 0.2% change in a low-impact categorical distribution.
7.3 Automated renewal workflow
Proposed controlled refresh pipeline. Failed disclosure or fidelity checks prevent promotion of a candidate.
Automatic regeneration should not necessarily mean automatic publication.

If profiling begins to capture a previously unseen sensitive category, the release policy may need to reject or coarsen the resulting characterisation. The same applies when a new source is added or its licensing terms change.
7.4 Reproducibility requires more than a random seed
A robust test-data release should preserve:
Component	Reason
Characterisation version	Statistical inputs evolve
Generator code revision	Algorithms evolve
Scenario configuration	Deliberate coverage policies evolve
Random seed and RNG algorithm	Random sequences must be reproducible
Library versions	Faker, simulation and generation algorithms can change
Execution environment	Distributed generation may introduce nondeterministic behaviour
Simulation reference date	Relative time behaviour can otherwise change
Generated artefact checksums	Verify byte-level identity
Delivery sequence	Ordering and timing may be responsible for a failure
Test and workload versions	The behaviour being measured also evolves

For important failures, retain the actual approved synthetic input files or event sequence, not merely instructions for regenerating them.

This is consistent with Hypothesis guidance: its failure-reproduction artefacts can be version-specific, and permanent regression cases should be represented explicitly rather than relying indefinitely on the internal example database. 

Hypothesis 6.170.15 documentation

7.5 Established tools
Tool	Maintenance	Fit and boundary
Deequ	Active, 2026 repository development	Historical quality metrics and anomaly detection; runs on real data internally.  GitHub
Evidently	Active releases	Distribution-drift algorithms and reports. Although oriented towards ML observability, tabular drift metrics can be reused without ML training. Raw comparison datasets remain inside.  GitHub
GX Core / Great Expectations	Active; new project stewardship announced in 2026	Declarative validation and historical results. Internal execution; validation reports require disclosure review.  Great Expectations+1
DVC	Established, maintained repository	Versions datasets and reproducible pipelines. Suitable for approved external synthetic artefacts; protected data must use separate storage and access policies.  GitHub
Git and content-addressed object storage	Mature	Store characterisations, configurations and immutable generated artefacts.
Hypothesis	Active	Replays and minimises failing generated test cases.

The missing component is an orchestration layer that connects detection, characterisation, disclosure approval, generation, independent validation and promotion.

8. Sharing a foundation between validation, drift detection and generation
Yes. There is considerable overlap between these capabilities, but there is an important conceptual trap.

What is observed in production is not necessarily what is permitted, correct or desirable.

A production profile describes reality. A data contract describes expectations. A test oracle describes the correct behaviour of the system.

These should share infrastructure without becoming interchangeable.
8.1 Three kinds of knowledge
Observed
What production actually contains
3% of identifiers are missing.


Expected
What the source is supposed to deliver
Identifiers are mandatory.


Required behaviour
What the platform must do
Quarantine invalid records.



A generator needs the observed defect frequency to produce representative workloads. A validator needs the normative rule to detect invalid data. A correctness test needs the expected platform response to determine whether the implementation works.

Automatically deriving the latter two from production observations would risk institutionalising production defects.
8.2 A shared characteristic registry
An illustrative specification might look like this:
characteristic:
  id: source_a.missing_identifier_rate
  scope: source_a
  metric: null_fraction
  field: external_identifier

observed:
  approved_estimate: 0.03
  observation_window: 30_days

contract:
  maximum_allowed: 0.0

generation:
  representative: observed_distribution
  edge_cases:
    - no_missing_identifiers
    - some_missing_identifiers
    - all_identifiers_missing

expected_behaviour:
  missing_identifier: quarantine_record

disclosure:
  classification: approved_aggregate
  release_policy: policy_17


This is a proposed format, not an existing standard. The values are fictional.

The same characteristic definition can support multiple functions:
Consumer	Use of the definition
Profiler	Calculate the observed metric
Drift detector	Compare its current and previous values
Validator	Check whether the contract is satisfied
Generator	Reproduce the observed rate or deliberately override it
Test runner	Verify expected platform behaviour
Disclosure controller	Decide whether the measurement may leave

8.3 Established tools to reuse
Deequ is particularly interesting because it combines metric calculation, constraints, constraint suggestion, historical metric storage and anomaly detection in one framework.

GX Core provides a complementary, declarative representation of validation expectations.

OpenMetadata can provide cataloguing, ownership and lineage around those measurements.

However, none of these should be assumed to provide a complete generator-ready statistical characterisation. Their normal data quality metrics are often descriptive summaries rather than full probability models, temporal models or relationship specifications.

Assessment: Reuse metric computation and validation infrastructure. Build the shared semantics connecting observed characteristics, normative contracts, scenario definitions and generation parameters.

9. What can be borrowed from established software testing?
This is arguably the most effective way to improve the value of synthetic data beyond mere representativeness.

A generator can produce not just input records but the expected truth about those records.
9.1 Generated data carrying its own ground truth
Consider two fictional entities:
True entity	Source A identifier	Source B identifier	Source C identifier
E001	A-104	B-773	Missing
E002	A-105	B-774	C-550

The generator can introduce deliberate complications:
- Two observations of E001 have conflicting attributes.
- Source B reports an obsolete name for E002.
- Source C reports E002 twice.
- E001 and E002 have similar identifying attributes.
The external input delivered to the platform does not include the true entity identifiers. They are retained separately as test ground truth.

The test can then assess whether matching, reconciliation, deduplication and source precedence were handled correctly.

This is directly related to the GeCo and FEBRL approach in entity-resolution research.

It also addresses the test-oracle problem: we can know the answer for generated data even where the correct answer for real production records is not readily available.
9.2 Property-based testing
Rather than specifying thousands of individual datasets and outputs manually, define properties that must always hold.

Hypothesis generates inputs and searches for examples that violate those properties. It can also shrink a complex failure into a much smaller reproducer.

Examples for the platform:
Property	What it checks
An unchanged delivery is idempotent	Reprocessing does not create duplicates
Every accepted source record has an explainable disposition	Records cannot silently disappear
Synthetic identity assignments are preserved across updates	Entity identity remains stable
Rejected records cannot corrupt accepted entities	Isolation of invalid inputs
Incremental processing equals full recomputation, where specified	Correct incremental algorithms
Record ordering does not affect order-insensitive operations	Determinism
Retraction followed by re-addition follows defined semantics	Lifecycle correctness

The important qualification is that each property must reflect the actual intended platform semantics.

For instance, ordering independence is not a valid property of a system whose specification deliberately uses arrival order as a conflict-resolution rule.
9.3 Metamorphic testing
Metamorphic testing is particularly useful where it is difficult to calculate the correct output directly.

Instead of knowing the answer to one input, define the relationship that must hold between the outputs of related inputs.
Transformation of synthetic input	Expected relationship
Rename all external identifiers consistently	Resolved population remains equivalent
Split one file into several smaller files	Final state remains unchanged
Replay an already processed file	No additional accepted entities
Shuffle records within an unordered batch	Equivalent final state
Add an unrelated entity	Existing independent entities remain unaffected
Scale a disjoint population by replication with fresh identifiers	Relevant additive counts scale accordingly
Reorder equivalent SQL predicates	Query result remains equivalent

The SQLancer project provides particularly strong precedent. Its database-testing methods include Non-optimising Reference Engine Construction (2020), Ternary Logic Partitioning (2020), Differential Query Plans (2024) and further approaches published in 2025. These systematically test database correctness without requiring a manually computed answer for every generated query. 

GitHub

The principles can be transferred to data transformation and reconciliation pipelines.
9.4 Differential and model-based testing
Run two independent implementations or processing strategies and compare their outcomes.

Useful comparisons include:
Implementation under test	Reference
Optimised distributed join	Simple reference implementation
Incremental reconciliation	Full recomputation
New parser	Established parser
New matching algorithm	Synthetic ground truth or simpler matching logic
Parallel processing	Sequential processing
New platform release	Previous release plus known-correct invariants

The previous release is not necessarily correct, so differential testing detects discrepancies rather than proving which implementation is correct.

For complex stateful behaviour, a simple reference state machine can act as an independent oracle.
9.5 Fuzzing structured delivery formats
A logically realistic dataset does not automatically exercise format-handling failures.

Separate the generation of records from the generation and mutation of their delivery envelopes.

Relevant cases include CSV quoting and delimiter problems, unusual encodings, inconsistent line endings, truncated files, invalid headers, duplicate columns, precision overflow, unexpected enum values, compressed-file errors and partially delivered batches.

Generate both well-formed and deliberately malformed inputs.
Tool	Maintenance	Boundary and suitability
Hypothesis	Mature, active	Generates logical values and stateful sequences. No real rows required.
SQLancer	Active research-driven project with released software	Generates SQL and uses automated correctness oracles. No real rows required.
Atheris	Active package releases in 2026	Coverage-guided Python fuzzing, including custom structure-aware mutation. Operates on fictional input.  PyPI
AFL++	Mature, active November 2026 repository activity	Coverage-guided fuzzing for native parsers and programs. No real data required.  GitHub
libprotobuf-mutator	Established; recent release cadence uncertain	Structure-aware mutation of Protocol Buffers and related grammar-based inputs. Useful for exercising deeper parser logic.  GitHub
Apache Beam TestStream	Active	Controls event ordering, processing time and lateness in streaming tests.

The generator's approved production characterisation can supply sensible starting distributions and structural parameters. The fuzzer then deliberately deviates from them.

10. Neighbouring fields worth investigating
Searching only for synthetic data generation would miss several of the strongest precedents.
Field	Useful terminology	What to borrow
Official statistics	Synthetic microdata, statistical disclosure control, public-use files	Approved statistical releases, synthesis utility and disclosure assessment
Population microsimulation	Population synthesis, calibration, IPF, simulated annealing	Generating coherent populations under aggregate constraints
Database benchmarking	Application-driven benchmarking, query-aware generation	Workload cardinalities, scalability and deterministic generation
Query optimisation	Selectivity estimation, multivariate statistics, join cardinality estimation	Identification of performance-sensitive data characteristics
Entity resolution	Record linkage, duplicate generation, data corruption models	Known true identities and multiple noisy observations
Healthcare simulation	Synthetic patient populations, longitudinal simulation	Stateful entity histories and domain-driven generation
Discrete-event simulation	Arrival processes, state transitions, event scheduling	Delivery behaviour and interdependent source changes
Performance engineering	Workload modelling, trace-driven simulation, load testing	Bursts, hot keys, concurrency and resource bottlenecks
Privacy engineering	Differential privacy, composition, membership inference	Formal and empirical disclosure controls
Statistical process control	Concept drift, change-point detection, control charts	Continuous detection of meaningful changes
Software testing	Property-based, metamorphic, model-based testing, test oracles	Generated correctness cases and automatic expected outcomes
Test data management	Referential subsetting, masking, data provisioning	Repeatable fixture provisioning and relationship preservation

The closest overall precedents

NHS England — Artificial Data Pilot

Closest precedent for a protected aggregation environment and isolated external generation.
Limitation: independent marginal distributions, deliberately low relationship fidelity.Project and methodology




Touchstone — USENIX ATC 2018

Closest precedent for deriving data-generation constraints from the behaviour of application workloads.
Limitation: research implementation rather than a universal production solution.Research paper




LDBC Social Network Benchmark

Closest precedent for scalable, correlated entity populations with relationships and temporal changes.
Limitation: designed for a specific graph domain and workload.Generator source




Synthea

Closest precedent for generating coherent entity histories from explicit domain and state-transition models.
Limitation: healthcare-specific rules must be replaced by platform-domain rules.Generator source




OpenDP and SmartNoise

Strong foundations for privacy-protected statistical measurements and synthetic releases.
Limitation: full multi-source, entity-level relational and longitudinal synthesis remains difficult.OpenDP · SmartNoise




11. Synthesis: what exists off the shelf and what needs building
11.1 Capability maturity
The following is an inferred assessment of suitability for the exact constraints in the brief, rather than a general rating of the tools.
Capability	Availability	Main candidates
Basic statistical profiling	Mature	Deequ, database statistics, DataSketches
Single-table statistical synthesis	Mature	synthpop, SmartNoise
Configurable bulk generation	Mature	dbldatagen, Faker
Statistical disclosure control	Mature	ARX, sdcMicro, OpenDP
Differentially private measurements	Mature	OpenDP, SmartNoise
Relational synthesis	Partial	Statistical synthesis tools, relational research
Relational DP synthesis	Emerging	PrivLava, DPSynth
Workload-aware generation	Research-heavy	Touchstone, MyBenchmark
Multi-source entity simulation	Custom integration	GeCo and LDBC as precedents
Domain-specific temporal simulation	Custom modelling	Synthea patterns, SimPy
Format fuzzing	Mature	Atheris, AFL++, Hypothesis
Data-quality validation	Mature	Deequ, GX Core
Basic drift detection	Mature	Evidently, Deequ
Cross-source drift detection	Custom metrics	Profiling and linkage infrastructure
Reproducible artefact storage	Mature	Git, DVC, object storage
Independent workload-fidelity certification	Custom integration	Database instrumentation, workload harnesses
Licence-aware release controls	Custom policy	Existing governance infrastructure
End-to-end controlled renewal	Custom integration	Existing orchestration infrastructure

Most of the individual technical mechanisms already exist. The hard part is combining them around a definition of platform-specific fidelity.
11.2 Recommended target architecture
Proposed overall architecture. Production data and unapproved derived artefacts remain protected; development receives versioned, approved information and independently generated test data.
11.3 The components worth building
I would limit custom development initially to six capabilities:
Component	Responsibility
Characterisation specification	Express the statistical, relational, temporal and workload characteristics that matter
Domain simulator	Generate persistent fictional entities, relationships and lifecycles
Source projection layer	Represent each provider's coverage, formats, identifiers, defects and delays
Scenario compiler	Convert representative, rare-case and stress policies into generation configurations
Fidelity harness	Compare independent protected-environment workload measurements with synthetic workload results
Release and version controller	Coordinate drift detection, approval, regeneration and immutable test-data versions

Everything else should be evaluated against existing libraries before custom implementation.
11.4 Suggested initial tool stack
For a Python- and SQL-oriented platform, the following would be a reasonable starting point, subject to the actual technology stack.
Function	First candidate	Alternative or complement
Profiling	SQL + DataSketches	Deequ for Spark
Cross-source linkage	Splink	Existing internal entity-resolution logic
Protected aggregate release	OpenDP	SmartNoise
Statistical synthesis experiments	synthpop	SmartNoise AIM
Basic fictional attributes	Faker	Custom domain dictionaries
Large-scale generation	dbldatagen	Engine-native SQL or distributed generation
Entity lifecycle simulation	SimPy	Custom state-transition models
Correctness generation	Hypothesis	Explicit scenario fixtures
Format fuzzing	Atheris	AFL++ for native components
Data-quality validation	GX Core or Deequ	Existing validation framework
Drift detection	Deequ or Evidently	Custom cross-source metrics
Versioning	Git + object storage	DVC

This is deliberately modular. It avoids coupling the entire solution to one synthesiser, one database system or one statistical modelling technique.

12. Suggested proof of concept
Rather than initially characterising every source and every field, select a narrowly scoped but difficult vertical slice of the platform.

A suitable candidate would have several overlapping sources, imperfect matching, frequent incremental changes, a known skew-related performance problem and several documented historical failure cases.

The proof of concept should compare four generation approaches.
Candidate	Method	Question answered
A	Current hand-written fixtures	How much value does the existing baseline provide?
B	Marginal statistical synthesis	How much improvement comes from basic production profiling?
C	Entity-first correlated generation	How important are source overlap and entity relationships?
D	Entity-first plus workload calibration	Does the additional complexity materially improve platform fidelity?

If permitted, an internally masked or subsetted production dataset can provide an additional high-fidelity reference without leaving the protected environment.
Proposed evaluation criteria
Proof-of-concept acceptance checklist

0 of 10


[ ] No source records or unapproved derived information leave the protected environment.
[ ] Correctness fixtures contain independent expected outcomes.
[ ] Representative data reproduces important cross-source relationship distributions.
[ ] Synthetic workloads reproduce important join and intermediate cardinalities.
[ ] Full-scale tests reproduce relevant memory, shuffle and latency behaviour.
[ ] Historical classes of failures can be reproduced.
[ ] Delivery sequences cover corrections, duplication, late arrivals and gaps.
[ ] New production characteristics can trigger controlled renewal.
[ ] An earlier failed test can be reproduced after renewal.
[ ] Source-specific licence restrictions are enforced.
 Copy checklist
A particularly valuable experiment would be to calibrate the generators using one observation window and evaluate them against an independent set of workloads and a subsequent production observation window.

That would reveal both overfitting to the chosen characterisation and sensitivity to production changes.

13. Open trade-offs
These are the principal architectural choices that the research does not resolve automatically.
Decision	One extreme	Other extreme
Protection versus fidelity	Coarse, low-disclosure statistics	Highly detailed joint models
Interpretability versus statistical richness	Explicit distributions and rules	Complex fitted generative models
Domain modelling versus automation	Hand-modelled entity simulator	Automated statistical inference
Generality versus workload fidelity	Broad statistical similarity	Targeted workload constraints
Normality versus test coverage	Realistic occurrence frequencies	Deliberately exaggerated edge cases
Freshness versus privacy	Frequent characterisation releases	Stable releases with limited cumulative disclosure
Realism versus known truth	Transform production-derived records	Fully simulated fictional entities
Reproducibility versus continuous renewal	Immutable datasets	Continuously regenerated datasets
Accuracy versus generation cost	Expensive constraint satisfaction	Fast approximate generation

Three deserve particular attention.

First, aggregate sufficiency is workload-dependent. There is no universal set of statistics guaranteed to preserve every property of the real dataset. The required characterisation should be treated as an evolving specification.

Second, preserving rare production behaviour and protecting confidential information are sometimes competing objectives. Independently designed stress scenarios can often resolve this conflict more effectively than attempting to reproduce every real extreme observation.

Third, cross-source entity identity is a domain model, not just a statistical relationship. It may be possible to learn aspects of it automatically, but explicit semantics are needed if generated inputs are also expected to carry correct outcomes.

14. Principal sources and further reading
The following are the strongest starting references from the research, grouped by the contribution they make. Research publication dates are distinguished from current software-maintenance observations.
Statistical synthesis and official statistics
Date	Source	Contribution
2016	Nowok, Raab and Dibben, synthpop: Bespoke Creation of Synthetic Data in R. Journal of Statistical Software	Established statistical synthesis methodology
2017	Templ et al., Simulation of Synthetic Complex Data: The R Package simPop. Paper	Population synthesis, calibration, complex data
2018	Snoke et al., General and Specific Utility Measures for Synthetic Data. Paper	Independent and use-specific utility evaluation
2019	UK Office for National Statistics, Synthetic Data Pilot, Working Paper 16. Report	Synthesis methods, disclosure, intended uses
Current service documentation, consulted November 2026	NHS England, Artificial Data Pilot. Methodology	Direct precedent for isolated aggregate-based generation

Workload and database fidelity
Date	Source	Contribution
2011	Generating Private Synthetic Databases for Database Application Testing. Paper	Privacy-preserving application workload fidelity
2018	Li et al., Touchstone: Generating Enormous Query-Aware Test Databases. USENIX ATC	Scalable, workload-constrained synthesis
2020	LDBC Social Network Benchmark task force, The LDBC Social Network Benchmark. Specification	Correlated graph populations and temporal workloads
2023	Query Aware Synthetic Data Generation. UC Berkeley technical report	Cardinality constraints derived from queries
Current documentation, consulted November 2026	PostgreSQL, Statistics Used by the Planner. Documentation	Performance-sensitive statistics and dependencies

Privacy and relational synthesis
Date	Source	Contribution
2022	Stadler, Oprisanu and Troncoso, Synthetic Data — Anonymisation Groundhog Day. USENIX Security	Empirical synthetic-data privacy vulnerabilities
2023	PrivLava: Synthesizing Relational Data with Foreign Keys under Differential Privacy. Paper	Relational privacy-preserving synthesis
2025	NIST SP 800-226, Guidelines for Evaluating Differential Privacy Guarantees. Publication	Formal privacy guarantees and evaluation
2025	PrivPetal: Relational Data Synthesis via Permutation Relations. Paper	Emerging relational privacy methods
2026	Differentially Private Synthetic Data Generation for Relational Databases. JMLR	Recent relational synthesis research
1996	Directive 96/9/EC on the legal protection of databases. EUR-Lex	Separate database-rights considerations

Entity resolution, simulation and testing
Date	Source	Contribution
2013	Christen and Vatsalan, Flexible and Extensible Generation and Corruption of Personal Data. GeCo project	Synthetic identities and configurable corruption
2016	Apache Beam, Testing Unbounded Pipelines. Article	Event-time and late-arrival testing
2017 onward	MITRE, Synthea. Source repository	Longitudinal entity simulation
2020–2025	SQLancer research and test oracles. Project and papers	Metamorphic and differential database testing
Current documentation, consulted November 2026	Hypothesis, Stateful Testing. Documentation	Generated action sequences and minimised failures
Current software, May 2026 release	SimPy. Documentation	Discrete-event simulation

Evidence quality and limitations of this survey
The principal conclusions are based on research papers, public-sector methodology, official technical documentation and software repositories.

The capabilities attributed to SDV and MOSTLY AI are primarily provider-documented capabilities. They should not be interpreted as independently demonstrated effectiveness for this platform. In particular, SDV's current licensing prevents treating its Community version as an unqualified open-source recommendation.

Maintenance assessments are based on available release histories, package registries and repository activity. For several older tools, particularly academic prototypes, current maintenance remains unconfirmed. The NHS Artificial Data Generator repository was indexed publicly, but direct retrieval failed during this research; its architecture is instead substantiated by the official NHS methodology.

This is a desk-based research survey, not an executed benchmark or a complete systematic literature review. I have not installed and evaluated the candidate generators, audited their implementations, reviewed your source licences or inspected your platform's workloads. The proposed architecture, component boundaries and acceptance criteria are consequently engineering recommendations rather than experimentally validated results for your environment.

Final conclusion
The most promising direction is not simply to make synthetic data look more like production data.

It is to establish a maintained and independently validated model of the aspects of production data that determine platform behaviour.

Four principles follow from the research:
- Characterise production data according to the workloads and failure mechanisms that matter.
- Generate fictional entities and their histories before generating the individual source observations.
- Use separate generation policies for representative, exceptional and adversarial datasets.
- Continuously validate fidelity against protected-environment measurements while controlling disclosure and preserving immutable historical test cases.
The individual building blocks are largely available. The platform-specific work lies in defining the characterisation, modelling the domain and source behaviours, establishing independent correctness and fidelity checks, and connecting everything through a controlled release lifecycle.

That is a considerably narrower—and better-founded—engineering undertaking than inventing a general-purpose synthetic data generator from scratch.
