# Let audited aggregates drive stand-in test data

No single open-source tool does what the brief asks. The pattern, though, is well established in neighbouring fields, and most of its parts exist as maintained open source. Official statistics and health data (Simulacrum, OpenSAFELY, IAB test files, Census validation servers) arrive at the same loop. Compute a disclosure-checked characterisation inside the protected environment and treat that characterisation as the thing released. Generate outside from it with ordinary code, keeping the schema identical to production. Show usefulness by running the same code inside and releasing only checked comparison summaries. In the vocabulary of the Netherlands statistics office (CBS, 2026), such output is "simulated", not "synthetic", data, and its realism is capped by which aggregates are released. The characteristics that decide plans, failures and performance are the hard ones: join-crossing correlations, join fan-out and skew, duplication and physical ordering, string and format realities, and the overlap of the same entity across sources with its own identifiers and delays. Standard benchmark generators flatten exactly these, and no generator consumes them off the shelf.

The building blocks that fit an aggregates-only boundary are:

- marginal-based synthesis (Private-PGM/`mbi`, Apache-2.0, release 2.1.0 on 2026-11-06)
- seedless population synthesis (humanleague)
- workload-aware database generators that consume statistics and query plans (DBRepro and Mirage, both PostgreSQL research prototypes)
- transport of optimiser statistics (PostgreSQL 18/19, Oracle, SQL Server)
- property-based generation driven by a data contract (Hypothesis, Pandera, ODCS with datacontract-cli)
- drift detection by diffing profiles (Deequ, TFDV)
- differential privacy (DP) measurement libraries (OpenDP, Tumult Analytics)

The platform-specific middle has to be built:

- a multi-source entity generator with per-source identifiers, coverage and lag
- a delivery-process layer that produces late, duplicate, missing and restated batches
- an export gate
- a renewal loop keyed on a build identity

Two cautions shape the design. Aggregates are not safe merely because they are aggregates: the 2010 US Census was reconstructed for 70% of blocks from its published tables, and optimiser statistics contain literal data values. And every re-characterisation of the same records spends disclosure budget, so how often the stand-in is renewed is a privacy decision. Licensed reference data is a separate, contractual constraint that differential privacy does not relax.

## How to read the evidence in this report

Every claim carries a tag:

- **[D] documented.** A researcher read the full text, or the full primary page, README, licence file or package metadata.
- **[I] inferred.** Reasoning by the research team or by this synthesis.
- **[L] lead only.** A search extract or abstract. It is never the basis of a verdict.
- **[U] unreachable.** The source was tried and could not be retrieved.
- **[V] vendor marketing,** or an author's own unverified claim, including benchmarks the authors ran themselves.

Maintenance states come from PyPI and CRAN release dates and from last-commit dates of shallow clones, all collected on 2026-11-26 [D]. The GitHub API was unavailable, so star counts and issue activity are missing.

Where the research tracks disagreed, this report uses the stronger evidence and says so:

- **Get Real, Touchstone and the Hydra demo paper.** The benchmarking track read the full texts; the validation track saw only extracts.
- **The GeCo paper.** The generation track read it; two other tracks could not reach it.
- **SDMetrics licence.** It is MIT according to its PyPI metadata [D]; the utility track had assumed the Business Source License [I].

Nothing here is legal advice. Commercial products appear only as references for what capabilities exist.

## 1. Join-crossing correlation, skew and cross-source overlap are the characteristics that matter and resist capture

The characteristics fall into two layers. The easy layer is aggregate and cheap to export: schema and constraints, per-column histograms, most-common values (MCVs), null fractions, distinct counts, value widths, physical-order correlation and volumes. PostgreSQL's `pg_stats` exposes all of them per column ([PostgreSQL pg_stats](https://www.postgresql.org/docs/current/view-pg-stats.html)) [D].

The hard layer predicts where tests on simplified data mislead. The strongest evidence comes from database benchmarking:

- **Benchmark generators share the optimiser's assumptions.** TPC-H, TPC-DS and SSB generators use "the very same simplifying assumptions (uniformity, independence, principle of inclusion)" that optimisers make, so PostgreSQL's estimator "works unrealistically well for TPC-H" ([Leis et al., PVLDB 2015](https://www.vldb.org/pvldb/vol9/p204-leis.pdf)) [D].
- **Real data breaks the estimators.** On the real IMDB data, cardinality estimates were wrong by **up to 10^8 (under) and 10^4 (over)**, the errors grew exponentially with the number of joins, and "**no system tested was able to detect join-crossing correlations**" (same source) [D].
- **TPC-H is uniform in three ways.** It is uniform in value, frequency and join fan-out distributions. A join-crossing correlation looks like this: a car model introduced in 2009 has no sales before 2009, and that misleads estimates on the joined sales table ([JCC-H, TPCTC 2017](https://ir.cwi.nl/pub/27429/27429.pdf)) [D].
- **Real business-intelligence data looks different from benchmarks.** A study of about 62k real Tableau workbooks found that keys are mostly strings, that dates and booleans are often stored as strings and parsed at query time, that **64% of strings contain non-ASCII characters**, that over 85% of string columns carry a collation, and that NULL-handling expressions are very frequent ([Get Real, DBTest 2018](https://cs.cit.tum.de/fileadmin/w00cfj/dis/papers/getreal.pdf)) [D].
- **Row counts alone miss performance drivers.** Matching only row counts misses duplication, value ordering, skew and correlation. Duplication causes "inefficient hash bucket usage, leading to spills and longer probe times" ([Sanghi, EDBT/ICDT 2025 workshop](https://ceur-ws.org/Vol-3931/short5.pdf)) [D].
- **Ignoring distinct counts causes spills.** Generators that ignore distinct counts induce skew, "severe hash collisions and unintended disk spilling" ([DBRepro, arXiv 2608.27822, Aug 2026](https://arxiv.org/pdf/2608.27822)) [D].
- **Statistics cannot express what crosses joins.** PostgreSQL's extended statistics "are not currently used by the planner for selectivity estimations made for table joins" ([PostgreSQL CREATE STATISTICS](https://www.postgresql.org/docs/current/sql-createstatistics.html)) [D].

Other fields add characteristics that database work ignores:

- **Every category value, at least once.** The German employment research institute (IAB) builds test files that deliberately include every category value occurring in a wave at least once, distorting the marginals to cover code paths ([IAB BA panel test data](https://doku.iab.de/fdz/ba/Hilfe_Testdaten_e.pdf)) [D].
- **Order and overlap across sources.** IAB's SIAB test data keeps the chronological order and overlap of episodes across sources and regenerates derived variables after anonymisation ([IAB SIAB test data](https://doku.iab.de/fdz/siab/SIAB_Testdaten_en.pdf)) [D].
- **What is lost without longitudinal consistency.** In IAB's panel test data a person's gender can change between waves ([IAB](https://doku.iab.de/fdz/ba/Hilfe_Testdaten_e.pdf)) [D].
- **Linkage logic is itself a characteristic.** Simulacrum does not reproduce the real tumour-linkage algorithm, which uses a −31-day window ([NCRAS guide, June 2020](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/893386/NCRAS_guide_to_using_the_Simulacrum_and_submitting_code.pdf)) [D].
- **Univariate tables are not enough.** The UK Office for National Statistics (ONS) notes that working from univariate frequency tables alone gives "poorer control over illogical combinations" ([ONS WP16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)) [D]. Structural zeros (impossible combinations) therefore have to be supplied as rules, because aggregates cannot tell them apart from suppressed small cells [I].

Two of the brief's own concerns, cross-source entity overlap and arrival patterns, are modelled by **no database-benchmark generator found** [I]. Both can be described as aggregates, such as overlap matrices and lag histograms [I]. Finally, **"aggregate" does not mean "non-identifying"**: MCV lists, histogram bounds and multivariate MCV items are literal data values ([pg_stats](https://www.postgresql.org/docs/current/view-pg-stats.html)) [D]. On personal-data columns they can expose real names, identifiers or rare combinations [I].

In the table below, ease is E (easy), M (medium) or H (hard), given as capture → reproduce.

| Characteristic | What it decides | Ease | Exportable as aggregate? | Methods that capture it |
|---|---|---|---|---|
| Schema, types, keys, constraints | Correctness, load failures | E → E | Yes (DDL) [D] | `pg_dump --schema-only`, SQL Server `DBCC CLONEDATABASE`; every generator takes schema [D] |
| Marginals, MCVs, skew | Selectivity → plan choice; spills; hot partitions | E → E per column; rare tail H | Yes, but MCVs and histogram bounds are real values [D] | `pg_stats`; profilers; JCC-H `-k` skew [D] |
| NULL fraction, co-missingness | Three-valued logic, outer joins, COALESCE paths | E; joint patterns M | Yes | `null_frac`; Touchstone meta-table; ydata-profiling [D] |
| Distinct counts | Hash sizing, join estimates, spills | E/M (sampled statistics are inexact) | Yes | `n_distinct`; Deequ approximate distinct; DBRepro [D] |
| Within-table correlation, functional dependencies | Planner underestimation; business rules | M → M | Partly; multivariate MCV items are real values [D] | `CREATE STATISTICS`; `mbi` marginals; PDGF/Myriad specs [D] |
| Physical order, duplication | Index-scan, sort and hash cost | E/M → M | Yes | `pg_stats.correlation`; Sanghi 2025 models [D] |
| Referential integrity, orphan rate | Inner vs outer join correctness | E → E; orphans M | Yes (counts) | All FK-aware generators [D] |
| Join fan-out / degree distribution | Join output size, skewed partitions | M → M | Yes (degree histograms) | LDBC Datagen; Touchstone/Mirage; AMLSim `degree.csv` [D] |
| Join-crossing correlation | Multi-join misestimates by orders of magnitude | **H → H** | As join cardinalities or annotated plans, but the constraint count explodes [D] | JCC-H (synthetic only); Hydra, Mirage, Touchstone, SAM, DBRepro [D] |
| Long-tail rare combinations | Edge-case bugs, rare plan branches | **H** | Exporting them risks re-identification [I] | No tool covers this fully [I] |
| String formats, lengths, encodings, collations | Parse failures, ordering, memory width | M → **H** | Lengths yes; format grammars only if abstracted [I] | `avg_width`; Touchstone string lengths; `dsdgen` international characters [D] |
| Dirty values, rule violations | Robustness of ingestion and validation | M → M | Rates per rule [I] | BART, Gecko, Jenga [D] |
| Duplicates of one entity | Deduplication correctness, join explosion | M → M | Rates, similarity distributions [I] | Febrl, GeCo/Gecko, SERD [D] |
| Cross-source overlap (coverage, ID mismatch, delays) | Matching, double counting, late updates | **H → H** | Overlap matrices, lag histograms [I] | **None found** [I] |
| Trends, seasonality, bursts | Partition pruning, windows, retention | M → M | Yes | LDBC "flashmob" bursts; ydata ACF; Deequ Holt-Winters [D] |
| Arrival: batch size, lateness, re-delivery, gaps | Pipeline correctness, throughput | M → M | Yes (distributions) | TPC-DI CDC batches [D]; no generator with fitted rates [I] |
| Volume, table and partition size | Plan choice, spills, timeouts | E → E | Yes | TPC scale factors; `pg_restore_relation_stats` [D] |

## 2. Only marginal-based and workload-aware generators fit a boundary that lets out aggregates alone

The useful way to sort generation methods is by what has to cross the boundary. There are four families.

**(A) No real rows at all.** Generators work from a hand-written specification: Faker, Mimesis, Snowfakery, Data Caterer, dbldatagen, LDBC Datagen, TPC `dbgen`/`dsdgen`. They reproduce only what a person writes into the spec [D/I]. Pandera's documentation states the limit plainly: its schema-driven data "in many cases will not qualitatively look like the original data, however it will be valid" ([Pandera docs](https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/data_synthesis_strategies.md)) [D].

**(B) Fitted outside from aggregates exported from inside.** This is the family that matches the constraint.

- **Marginal-based synthesis.** In Private-PGM/`mbi` the estimator takes only a domain and "noisy marginal measurements", then calls `synthetic_data(rows=N)`; no rows enter the estimator ([mbi README](https://github.com/ryan112358/private-pgm)) [D]. The `mbi` API supports splitting the work into measuring inside and estimating plus sampling outside, while SmartNoise's `fit` call bundles both steps [I]. MST and AIM "require columns to be categorical", so bin edges become part of the released characterisation ([SmartNoise SDK](https://github.com/opendp/smartnoise-sdk)) [D/I].
- **Population synthesis.** It fits marginal control tables (Section on neighbouring fields).
- **Workload-aware database generators.** They take schema, catalog statistics, query texts and annotated plans. Hydra's client "fetches the schema, metadata and the query workload with its corresponding AQPs [annotated query plans]" and ships them, noting that "privacy concerns can be addressed by passing the information through an appropriate anonymization layer at the client" ([Hydra demo, PVLDB 11(12)](https://www.vldb.org/pvldb/vol11/p1974-sanghi.pdf)) [D]. The paper does not specify that anonymisation layer [I].
- **Agent-based simulators driven by parameter files.** PaySim's second version "uses aggregated transactional data" ([PaySim README](https://raw.githubusercontent.com/EdgarLopezPhD/PaySim/master/README.md)) [D].

**(C) Trained on real rows inside.** This covers CART, Bayesian networks, copulas, GANs, diffusion and autoregressive models. Either the fitted model leaves (a pickle, a JSON description, network weights, or a generator ZIP file as in MOSTLY AI's quick start), or generation runs inside and only synthetic rows leave ([mostlyai README](https://github.com/mostly-ai/mostlyai)) [D]. Both options need the model or the rows approved as a release, because a model is not an aggregate [I].

**(D) Transforms of real rows.** Masking and subsetting tools produce rows that correspond one to one with real rows, so they cannot leave an aggregates-only environment [I]. Their techniques transfer, as discussed below.

### Families A and B: tools that need no real rows outside

| Tool | Method | Licence | Maintenance (date) | What must leave | Fit |
|---|---|---|---|---|---|
| Private-PGM / `mbi` | Graphical model estimated from marginals; MST, AIM, MWEM in repo | Apache-2.0 | 2.1.0 on 2026-11-06; commit 2026-11-25 [D] | Marginal tables + domain (bin edges included) | **Best fit**; needs discrete domains [I] |
| SmartNoise Synth (MWEM, MST, AIM, DP-CTGAN, PATE-CTGAN) | DP marginals | MIT | 1.0.8 on 2026-04-15 [D] | DP marginals or DP synthetic rows | Good, if measuring is split from fitting [I] |
| DBRepro | Column statistics + plans → CP-SAT solver; targets identical physical plans | Apache-2.0 | Pushed 2026-07-27; arXiv Aug 2026 [D] | Schema, catalog statistics, SQL text, EXPLAIN plans | Plan fidelity for known queries; PostgreSQL 12–16 and KingbaseES only [D] |
| Mirage | Query-aware generation | Apache-2.0 | Pushed 2026-07-28 [D] | Same, plus execution of the original queries | Requires patching PostgreSQL's `explain.c`; PostgreSQL 12–15 ([README](https://raw.githubusercontent.com/dbhammer/mirage/main/README.md)) [D] |
| Hydra | One linear program per relation from annotated plans; "dataless" regeneration | Unknown [U] | Project site unreachable [U] | Schema, metadata, annotated plans | Concept fits; code status unknown |
| Touchstone | Per-column meta-table + query cardinalities | Apache-2.0 | Last push 2020-06-01, dormant [D] | NULL %, distinct counts, string lengths, cardinalities | Dormant |
| SAM | Autoregressive model from (query, cardinality) pairs | "NTUItive Dual License" | Last push 2022-11-10 [D] | Query workload + cardinalities | Dormant, not permissive; needs acyclic FK schema ([SAM, SIGMOD 2022](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf)) [D] |
| Arasu et al. DataSynth, QAGen, PiGen | Cardinality-constraint generation | No public code found [D] | — | Constraints, annotated plans | Reference designs only |
| SQLSynthGen | Aggregate SQL run inside → generate outside | MIT | 0.4.2 on 2023-12-14 [D] | "Source stats" | Design matches the brief, but README unread [L]; dormant |
| Optimiser statistics (PostgreSQL 18/19, Oracle `DBMS_STATS`, SQL Server clone) | Inject production statistics into an empty database | Engine | PostgreSQL 19 released 2026-11-19 [D] | Statistics, which contain literal values | Plan tests only (Section 5) |
| humanleague | IPF and quasirandom integer sampling (QIS) **without a seed** | Not recorded | 2.4.5 on 2026-08-29 [D] | Marginal tables | Good for entity populations [I] |
| Faker / Mimesis | Per-field value providers | MIT / MIT | 40.63.0 on 2026-11-20 / 22.2.0 on 2026-09-23 [D] | Nothing (or category weights) | Identifiers and PII-shaped strings [I] |
| Snowfakery | YAML recipes with `friends` and `reference` relations | BSD-3 | 4.2.1 stable; 5.0.0.dev1 on 2026-04-27; commit 2026-01-09 [D] | Recipe | Multi-table skeleton [I] |
| Data Caterer | Spark generation, FKs across data sources, validations | Apache-2.0 (repo) | Commit 2026-02-14 [D]; paid tiers unverified | Generation task | Volume and referential integrity [I] |
| dbldatagen | Spark, "billions of rows within minutes" [V] | **Databricks License, not OSI** [D] | 0.4.0.post1 on 2024-07-26; commit 2026-10-26 [D] | Spec | Needs legal review [I] |
| getsynth/synth | Declarative model; import infers a model from a database | Apache-2.0 | "Public Alpha"; commit 2024-09-27 [D] | Inferred schema file | Stalled |
| Benerator CE | Rule-based generation | GPL-2 with exceptions | Bug-fix only; commit 2026-08-09; points users to DATAMIMIC [D] | Spec | Declining |
| LDBC SNB Datagen | Spark; degree distributions, correlated attributes, deterministic | Apache-2.0 | Pushed 2026-10-18 [D] | — | Hard-wired to its social-network schema [I] |
| TPC-H `dbgen` 3.0.1 / TPC-DS `dsdgen` 4.0.0 / JCC-H | Uniform and independent (JCC-H adds skew and join-crossing correlation) | TPC licence unverified | Spec 2022 / Nov 2024; JCC-H pushed 2024-04-17 [D] | — | Performance smoke tests and optimiser stress only [I] |
| PDGF / DBSynth, Myriad, DataSynth (LDBC) | Hierarchical seeding; spec languages | Commercial (bankmark) [L/V]; Apache; GPL-3.0 | Myriad pushed 2014; DataSynth pushed 2017 [D]; DBSynth paper [U] | Spec | Design ideas only |

### Family C: models trained on real rows inside the environment

| Tool | Licence | Maintenance (date) | What leaves | Note |
|---|---|---|---|---|
| synthpop (R, CART/sequential) | GPL-2/3 | 1.9-3 on 2026-09-10 [D] | Normally synthetic rows only [I] | No multi-table features ([CRAN](https://cran.r-project.org/package=synthpop)) [D] |
| DataSynthesizer (Bayesian network) | MIT | 0.1.13 on 2023-10-18; commit 2026-07-15; "Pre-Alpha" [D] | JSON description file [I] | Single 1NF table only [D] |
| SDV (GaussianCopula, HMA, PAR) | **BUSL-1.1** since 0.18.0 (2023-01-24) [D] | 2.2.0 on 2026-11-06; 1.39.0 on 2026-11-12 [D] | Pickle; copula parameters can be inspected [D] | Community edition's multi-table HMA "up to 5 tables, depth of 1" [D] |
| copulas, CTGAN, RDT, SDGym | BUSL-1.1 | 2026-10-30 (SDGym 2026-11-13) [D] | Weights or parameters | DataCebo ecosystem |
| MOSTLY AI SDK / engine | Apache-2.0 | 6.2.1 / 2.7.4 on 2026-10-29 [D] | Generator ZIP file | Multi-table, time-series and DP claims are [V] |
| REaLTabFormer | MIT | 0.2.4 on 2026-01-04 [D] | Model directory | One parent→child relation per model pair [I] |
| GReaT, synthcity | MIT; Apache-2.0 | 0.0.14 on 2026-05-12; 0.2.12 on 2025-05-08 [D] | Weights | synthcity release cadence slowed [I] |
| TabDDPM, TabSyn | Not checked | Last commits 2023-03-09, 2024-06-20 [D] | Weights | Research code |
| ClavaDDPM | **No LICENSE file** | Commit 2024-10-27 [D] | Weights | "Tens or hundreds of interconnected tables" ([arXiv 2405.17724](https://arxiv.org/abs/2405.17724)) [D] |
| RC-TGAN / IRG | MIT and Apache stated inconsistently / code withheld | 2023-07-06 / 2026-02-18 with placeholders [D] | — | Not usable [I] |
| ydata-sdk, gretel-synthetics | Proprietary; "source-available" | 2026-02-27; 2025-06-24 [D] | — | Not open source |

The US National Institute of Standards and Technology (NIST) adds a quality point that favours family B: "Current deep learning-based approaches for differentially private synthetic data produce significantly lower quality data than approaches based on marginals" ([NIST SP 800-226, March 2025](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)) [D]. The NIST Collaborative Research Cycle archive offers a ready comparison corpus. It includes outputs of sdcMicro, synthpop, AIM and MST on the same ACS excerpts ([NIST CRC](https://github.com/usnistgov/privacy_collaborative_research_cycle), last commit 2026-03-19) [D].

### Links between tables remain the weak point of learned synthesis

Open-source multi-table synthesis is thin. SDV Community's only multi-table synthesizer is HMA, which is "optimized for smaller datasets with around 5 tables and 1 level of depth". The larger HSA and Independent synthesizers, DayZ, multi-table conditional sampling and composite keys are Enterprise features ([SDV multi-table synthesizers](https://docs.sdv.dev/sdv/multi-table-data/modeling/synthesizers); [SDV compare page](https://docs.sdv.dev/sdv/explore/compare-features)) [D; capability claims V]. SDV's licence permits internal use by employees and contractors; it excludes running a "Synthetic Data Service" for third parties. Each release converts to MIT four years after it ships ([SDV LICENSE](https://github.com/sdv-dev/SDV/blob/main/LICENSE)) [D]. The research literature names the gap directly. PrivPetal notes that "if we generate random records for each entity independently, the resulting synthetic data usually fail to exhibit realistic relationships", and PrivLava says single-relation methods "are unable to model the complex correlations induced by the foreign keys" ([PrivPetal, arXiv 2503.22970](https://arxiv.org/abs/2503.22970); [PrivLava, arXiv 2304.04545](https://arxiv.org/abs/2304.04545)) [D, abstracts]. No packaged code was found for either [D].

Workload-aware database generators handle joins differently: they encode them as cardinality constraints. Touchstone supports non-equi-joins ([Touchstone, USENIX ATC 2018](https://www.usenix.org/system/files/conference/atc18/atc18-li-yuming.pdf)) [D]. SAM assigns join keys by "Group-and-Merge" over acyclic foreign-key joins [D].

For an aggregates-only platform, the practical cross-table route is bespoke [I]:

1. Fit an `mbi` model per table, or for a join of a parent with its children.
2. Add an explicit children-per-parent distribution. Degree histograms are aggregate.
3. Generate parents before children in foreign-key topological order, the order Jailer and Condenser use for subsetting ([Jailer README](https://raw.githubusercontent.com/Wisser/Jailer/master/README.md)) [D for the tool].
4. Use deterministic keyed hashing, as in Greenmask's hash engines ("consistent output for the same input"), so that the same synthetic entity stays consistent across tables ([Greenmask README](https://raw.githubusercontent.com/GreenmaskIO/greenmask/main/README.md)) [D for the tool; transfer I].

### The same entity across sources is modelled only as duplicates, never as sources with identifiers and lags

Record-linkage test data generation has a stable two-step pattern. Generate "original" entities from frequency look-up tables, then emit corrupted duplicates, each keeping a label that links it to its original.

- **Febrl `dsgen`.** It draws the number of duplicates per original from a uniform, Poisson or Zipf distribution. It is dual-licensed ANUOS or GPL-2+, and the fork's last commit was 2016-11-04 ([Febrl fork](https://github.com/J535D165/FEBRL-fork-v0.4.2)) [D].
- **GeCo.** It gives every original and duplicate a unique identifier and supports dependencies "between up-to three attributes" ([Christen & Vatsalan, CIKM 2013](https://users.cecs.anu.edu.au/~christen/publications/christen2013cikm.pdf)) [D in one track; U in two others].
- **Gecko.** Its successor is Gecko (`gecko-syndata`), MIT, release 0.6.4 on 2024-12-06, which describes itself as still in a "beta" state ([gecko](https://github.com/ul-mds/gecko)) [D].
- **Splink's datasets.** Splink (MIT, 5.0.0 on 2026-09-28) ships a small worked example of what the brief needs. In its transaction-origin and transaction-destination pair, "there may be a delay between the source and destination account, and the amount may vary", and the memo field is sometimes truncated ([Splink datasets](https://github.com/moj-analytical-services/splink/blob/master/docs/includes/generated_files/datasets_table.md)) [D].
- **SERD.** It learns the similarity distributions of matching and non-matching pairs from real data, then synthesises entities under DP. Matchers trained on its output differ in F1 "within 6%" on three datasets ([SERD PDF](https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/4-6-Synthesizing_Entity_Resolution_Datasets.pdf)) [D; venue unverified]. The characterisation SERD needs is itself an aggregate: similarity distributions [I].
- **Alaska.** A real multi-source benchmark [L].

**None of these tools treats per-source identifier schemes, per-source coverage or reporting delay as a first-class parameter** [I]. A generator for the brief can be assembled from documented parts [I]:

1. Generate a ground-truth entity table.
2. Per source, sample inclusion at that source's coverage rate for each segment.
3. Per source, sample a reporting delay from the released lag histogram.
4. Assign identifiers in each source's own format.
5. Apply per-source corruption profiles (Gecko mutators).
6. Keep a hidden crosswalk from entity to (source, source identifier) as the label.

Every input is a count that can be computed and released from inside: coverage, pairwise or k-way overlap counts, delay histograms, error rates per field and source, and duplicates-per-entity distributions [I].

## 3. Usefulness is shown by running the same workload inside and exporting only comparisons

The literature separates *general* utility (whether the distributions look comparable) from *specific* utility, "the similarity of results of analyses from the synthetic data and the original data" ([Snoke et al., arXiv 1604.06651](https://arxiv.org/abs/1604.06651)) [D, abstract]. The brief's "beyond matching the characterisation" means specific utility, and official statistics has run it as a service for over a decade.

The US Census Bureau's SIPP Synthetic Beta (SSB) shows the shape of such a service ([Census SSB, revised 17 Nov 2026](https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html)) [D]:

- Users must submit programs that already run without error on the synthetic file.
- Census staff run them on the confidential "Completed Gold Standard File".
- Uploads are processed twice a month. Output is reviewed against disclosure and rounding rules.
- Turnaround is "as little as 7 business days".
- The service is **"temporarily on pause"**.

Other official-statistics programmes add to the picture:

- **SynLBD.** The Synthetic Longitudinal Business Database "has not been fully validated", and "unless validated, there is no guarantee results … reflect results from the underlying confidential data" ([Census SynLBD validity](https://www.census.gov/programs-surveys/ces/data/public-use-data/synthetic-longitudinal-business-database/analytic-validity.html)) [D].
- **Cornell route.** Validation through Cornell's Synthetic Data Server ended in September 2022 ([Barrientos et al., arXiv 2110.12055v3](https://arxiv.org/pdf/2110.12055v3.pdf)) [D]. The Cornell page itself was [U].
- **Urban Institute.** Urban's privacy-preserving validation server reached v2.0 on 11 Sep 2024. It aims to "improve and automate statistical disclosure control" ([Urban v2](https://www.urban.org/research/publication/privacy-preserving-validation-server-version-2)) [D landing page]. Its architecture PDFs were [U].
- **What DP can automate.** Barrientos et al. found DP "feasible for simple, univariate statistics but struggle[s] to produce accurate regression estimates and confidence intervals" [D].
- **Verification servers.** These are a lighter variant. They let users check public estimates against the confidential data "without return[ing] confidential estimates" ([Barrientos et al.](https://arxiv.org/pdf/2110.12055v3.pdf)) [D]. Lin and Reiter show that verification measures still "leak information" and give a DP version ([arXiv 2404.02519](https://arxiv.org/abs/2404.02519)) [D, abstract].

The best documented workload comparison is the Tax Policy Center's 2018 plan. It would run the Center's microsimulation model on the synthetic public-use file and on the confidential data, and compare revenue, marginal tax rates and burden distributions ([Burman et al., 2018](https://www.taxpolicycenter.org/sites/default/files/publication/156011/safely_expanding_research_access_to_administrative_tax_data_creating_a_synthetic_public_use_file_and_a_validation_server_0.pdf)) [D].

The best documented *result* is sobering. The authors applied the exact SynLBD synthesis code to Canadian and German business registers, and the custodians reviewed the outputs before releasing them ([Alam, Dostie, Drechsler, Vilhuber, 2020](https://zenodo.org/records/3832173/files/AlamDostieDrechslerVilhuber_20200518.pdf)) [D]:

- The synthetic data "do not reliably lead to the same modeling decisions".
- With millions of records, confidence intervals "(almost) never overlap even when the estimates … are quite close".
- pMSE ratios ran from 657 to 10,958, so the pMSE test rejects equivalence almost by construction.

At platform scale, then, hypothesis-test utility metrics will always "fail". Effect-size measures such as Q-error, max(a/b, b/a), and absolute differences with tolerances agreed in advance are the workable alternative [I].

Health data runs the same loop in production. Simulacrum's data model "is the same as the real one", so researchers write PL/SQL against it, and NCRAS runs that code on real data. "The more complex the data query the more approximate the results", and requests are capped at three hours of analyst time ([NCRAS guide](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/893386/NCRAS_guide_to_using_the_Simulacrum_and_submitting_code.pdf)) [D]. A UK counter-example shows what breaks the premise. The synthetic Longitudinal Education Outcomes (LEO) data ships as files while the real data "is only available via SQL server", so code may need adapting ([ADR UK, 14 Apr 2026](https://www.adruk.org/news-publications/news-blogs/longitudinal-education-outcomes-synthetic-data-what-is-it-and-why-is-it-useful-1/)) [D]. Format parity is part of fidelity [I].

Database research measures realism by workload too:

- **SAM.** It reports Q-error on the input queries and on an *independent* test query set, plus "performance deviation", the latency difference between synthetic and original databases on PostgreSQL 12 ([SAM](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf)) [D].
- **Hydra.** It reports ">90% of the volumetric constraints were satisfied with virtually no error" on its demo workload ([Hydra demo](https://www.vldb.org/pvldb/vol11/p1974-sanghi.pdf)) [D]. Hydra treats plan equivalence as a precondition, not a measured outcome [L].
- **Identical statistics, different runtime.** RSGen's authors warn that identical statistics can yield the same plan with a different runtime ([DBTest 2013 extract](https://dbtest2013.soe.ucsc.edu/papers/a7-Shen.pdf)) [L].
- **Unseen queries.** Similarity on the training workload does not guarantee similarity on unseen queries [I].

Plan fingerprints should therefore be exported and compared, not assumed [I].

| Utility metric family | Real-side input | Computable outside from an aggregate export? |
|---|---|---|
| Total variation distance (TVD) and Hellinger on categorical marginals; k-way marginal error | Cell counts | Yes, with small-cell suppression or noise [I] |
| synthpop `utility.tab` table pMSE | The same n-way counts | Yes mathematically; the API takes data frames ([vignette](https://cran.r-project.org/web/packages/synthpop/vignettes/utility.pdf)) [D/I] |
| KS / Wasserstein | Empirical CDF | Approximately, from quantiles or shared bins [I] |
| Moments, quantiles, missingness, distinct counts, correlation and MI matrices | Scalars or pairwise statistics | Yes [I] |
| Confidence-interval and coefficient overlap | (estimate, standard error) from the same model run inside | Yes; this is the validation-server pattern [I] |
| Classifier pMSE, detection, MMD, PCA, nearest-neighbour, train-on-synthetic-test-on-real (TSTR) | Real rows next to synthetic rows | No; run inside and export only scores [I] |

Every packaged evaluation tool takes real and synthetic frames together, so as packaged it must run inside the environment [D/I]:

- **SDMetrics.** MIT, 0.33.1 on 2026-11-25, README badge "Pre-Alpha" ([README](https://raw.githubusercontent.com/sdv-dev/SDMetrics/main/README.md)) [D].
- **SynthEval.** 1.7.3 on 2026-10-23; licence unverified ([README](https://raw.githubusercontent.com/schneiderkamplab/syntheval/main/README.md)) [D].
- **synthcity.** 0.2.12 on 2025-05-08 [D].
- **Urban `syntheval`.** Installed from GitHub only, before a 0.1.0 release ([README](https://raw.githubusercontent.com/UrbanInstitute/syntheval/main/README.md)) [D].
- **NIST SDNist v2.5.** It "only supports using the NIST ACS Data Excerpts" ([README](https://raw.githubusercontent.com/usnistgov/SDNist/main/README.md)) [D].
- **SynthGauge.** Last release 2022-10-12, stale [D/I].

None of the READMEs read suggests that a tool accepts aggregate-only real-side inputs [I].

For a data platform, the natural specific-utility test is a **workload-fidelity vector**: run the same pinned pipeline version inside on real data and outside on the stand-in, and compare [I]. The vector would contain:

- row counts per stage and per source
- pass rates per data-quality rule
- join match rates, including unmatched-left and unmatched-right shares, per source pair
- entity-resolution statistics: candidate pairs after blocking, cluster-size distribution, and the share of entities seen in 1, 2 or k sources
- reject rates by error type
- arrival-lag quantiles
- plan fingerprints, stage times, peak memory and spill bytes, normalised per million rows

Measure the noise floor first by repeating the real run [I]. A vendor glossary [L/V] also gives this advice. Industry "shadow" and parity testing (Segment, Yelp, Totango, Twitter's Diffy) compares one pipeline version with another on real data, not real with synthetic, and was seen only as leads [L].

## 4. Aggregates leak, releases compose, and licences bind independently

### Summary statistics are not safe, and optimiser statistics are samples of records

The theory is settled. Dwork and Roth's "Fundamental Law of Information Recovery" holds that "overly accurate answers to too many questions will destroy privacy in a spectacular way". A mechanism whose noise is always bounded by about n/401 "permits an adversary to correctly reconstruct 99% of the entries" ([Dwork & Roth, 2014](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)) [D].

The practice is too. From only 34 of the 180 table sets the 2010 Census published, the Census Bureau's own team reconstructed records with block, sex, age, race and ethnicity. **All records in 70% of census blocks (97 million people)** were verifiably perfectly reconstructed. The authors call the assumption that tables are inherently less disclosive than microdata "fundamentally flawed" ([Abowd et al., arXiv 2312.11283v3](https://arxiv.org/abs/2312.11283)) [D]. Cell suppression unravels when "some other group did a cell-suppressed release of overlapping data but didn't suppress the same cells" ([TopDown Algorithm paper, arXiv 2204.08986](https://arxiv.org/abs/2204.08986)) [D]. Differencing is the everyday version. In the SACRO guide's example, a mean over 16 people and a mean over 15 of them reveal the excluded person's earnings ([SACRO guide, Oct 2023](https://zenodo.org/records/10282526/files/The%20SACRO%20guide%20to%20statistical%20output%20checking.pdf)) [D]: £300,000 by arithmetic [I].

Synthetic data offers no automatic escape:

- **No better trade-off.** Stadler et al. find that synthetic data "does not provide a better tradeoff between privacy and utility than traditional anonymisation techniques", and that it "does not protect outlier records" ([USENIX Security 2022](https://arxiv.org/abs/2011.07018)) [D].
- **Ordinary records are exposed too.** Annamalai et al.'s linear-reconstruction attack targets all records, not only outliers. Prior attacks "can underestimate the privacy risk … by up to 10 percentage points", and larger synthetic releases leak more ([arXiv 2301.10053](https://arxiv.org/abs/2301.10053)) [D].
- **Releasing a model widens the threat.** Sharing a trained model rather than its samples opens the way to white-box attacks [D, Stadler].

Optimiser statistics deserve special care. PostgreSQL itself says `pg_statistic` "should not be readable by the public" because "even statistical information about a table's contents might be considered sensitive", for example the minimum and maximum of a salary column ([PostgreSQL pg_statistic](https://www.postgresql.org/docs/current/catalog-pg-statistic.html)) [D]. CVE-2019-10130 showed that sampled statistics could leak rows hidden by row-level security ([advisory](https://www.postgresql.org/support/security/CVE-2019-10130/)) [D]. Exporting raw MCVs, histogram bounds or min/max is equivalent to exporting samples of records [I]. NIST adds that "revealing the bar chart bins may violate privacy", so histograms need bin edges that do not depend on the data ([NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)) [D].

The multi-source setting makes all of this worse. The same person enters several aggregates through several sources, so **the unit of privacy must be the real-world entity after entity resolution, not the source row** [I]. NIST warns that "guarantees with different units of privacy are not directly comparable" [D].

### Repeated releases add up under DP, and have no composition bound without it

Under differential privacy, privacy loss composes. In NIST's example, ten analyses at ε = 0.1 each cost ε = 1 in total. NIST also warns that DP "does not mitigate privacy risks associated with other (non-differentially private) releases based on the same underlying data" ([NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)) [D]. Mixing a DP characterisation with exact row counts or exact min/max of the same data therefore voids the accounting [I].

For streams, continual-observation mechanisms use a tree of interval noise, so error grows only polylogarithmically in time ([Dwork & Roth §12.3](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)) [D]. The 2020 Census used zero-concentrated DP with a production setting of ρ = 2.63. It treated some statistics as invariants, excluded "as matter of policy" from the accounting ([TopDown Algorithm paper](https://arxiv.org/abs/2204.08986)) [D], and that release defeated the reconstruction attack that worked on 2010 ([arXiv 2312.11283](https://arxiv.org/abs/2312.11283)) [D].

Traditional disclosure control has no composition theorem. ONS Census 2021 instead combined three measures ([ONS](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/protectingpersonaldataincensus2021results)) [D]:

- targeted record swapping, which changed geography for 7–10% of households
- a cell-key method that perturbed about 14% of cells in a typical dataset, to blunt differencing
- sparsity rules for its flexible table builder

Two patterns are therefore viable for a stand-in refreshed over time [I]:

1. **One DP characterisation per schema version, with a fixed lifetime budget.** All later test data is post-processed from it at no further cost.
2. **Periodic DP refreshes against a per-entity ledger of ε or ρ.**

The first pattern is far cheaper. Each re-characterisation of the same records spends budget again.

### Controls and their tools

| Tool | Kind | Maintenance (date) | Fit |
|---|---|---|---|
| ACRO / SACRO | Semi-automated output checking for trusted research environments (TREs): thresholds, dominance, reasons, reports | 1.1.0 on 2026-11-05; 1.0.0 on 2026-08-10 ([PyPI](https://pypi.org/project/acro/)) [D] | Model for an export gate; covers tables, models and plots, not verified for statistics dumps or synthetic sets [I] |
| sdcMicro / sdcTable (R) | Microdata and tabular SDC | 5.8.2 on 2026-06-12 / 0.34.1 on 2026-11-12 [D] | Heuristic, attack-specific protection [I] |
| tau-Argus / mu-Argus | Tabular / microdata SDC | Tag 2024-08-14, commit 2026-04-01 / dormant since 2024-03-13 [D] | — |
| ARX | k-anonymity, l-diversity, t-closeness | v3.9.2 on 2025-09-12; infrequent releases [D] | One-off extracts; does not compose [I] |
| synthpop `disclosure()` | Replicated uniques (RepU) and DiSCO metrics | CRAN 1.9-3; paper v6 1 Sep 2026 ([arXiv 2406.16826](https://arxiv.org/abs/2406.16826)) [D] | Evaluation, not a guarantee [I] |
| Anonymeter | Singling-out, linkability and inference risk | 1.1.0 on 2026-07-23, Clear BSD [D]; "legally aligned" claim [V] | Evaluation; needs real rows inside [D] |
| TAPAS | Attack toolbox | Last commit 2023-09-06 [D] | Dormant |
| OpenDP Library | DP core | 0.16.0 on 2026-10-06; MIT [D] | Preferred core; NIST advises "use well-tested libraries" [D] |
| SmartNoise SQL / Synth | DP SQL / DP synthesis | 1.0.10 on 2026-04-14 / 1.0.8 on 2026-04-15 [D] | DP aggregates inside |
| Tumult Analytics / Core | Spark-scale DP with privacy-ID accounting | 0.21.0 on 2026-06-30 / 0.20.0 on 2026-10-20 [D] | Fits entity-level accounting [I]; OpenDP took it over after the Tumult team joined LinkedIn (31 Mar 2025) ([README](https://raw.githubusercontent.com/opendp/tumult-analytics/main/README.md)) [D] |
| Google DP / PipelineDP / PyDP | DP libraries | v4.1.0 on 2026-02-04 / 0.3.1 on 2026-06-19 / 1.1.5 on 2026-05-11 [D] | PipelineDP had a 2023–2026 release gap [D] |
| IBM diffprivlib | DP library | 0.6.6 on 2025-04-10 [D] | Slow-moving |

There is ownership risk in the DP stack. OpenDP's own news mentions "a challenging 2025", and in September 2026 it advertised for a new director ([OpenDP news](https://opendp.org/news-events)) [D]; releases nonetheless continued [D].

### Regulation treats aggregates and synthetic data as anonymous only after assessment

The European Data Protection Board (EDPB) consultation draft of its pseudonymisation guidelines (adopted 16 January 2025) holds that pseudonymised data is personal "also … if pseudonymised data and additional information are not in the hands of the same person" ([EDPB Guidelines 01/2025](https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf)) [D]. Whether a final version exists by now is unconfirmed [U]. The UK ICO's anonymisation guidance (published 28 March 2025) asks that identification risk be reduced "to a sufficiently remote level". It is flagged "under review" following the Data (Use and Access) Act ([ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/about-this-guidance/)) [D].

The Court of Justice judgment in EDPS v SRB (4 Sep 2025) reportedly accepted that pseudonymised data can be non-personal for a recipient without reasonable means of re-identification [L]. The judgment text was [U]. The European Data Protection Supervisor's TechSonar page calls for a "privacy assurance assessment" of synthetic data [L/U]. In practice, hashed or tokenised identifiers in test copies are pseudonymisation and remain personal data for the platform operator. Each release type needs a documented identifiability assessment [I].

### Licensed reference data is a separate constraint, and DP does not discharge it

The brief asks whether licensed reference data is a separate constraint. Yes. Licences define "derived" material broadly, by contract and database right rather than by identifiability:

- **ODbL (OpenStreetMap).** Extracting "a Substantial part of the Contents in a new Database" creates a Derivative Database. A query result such as a statistic is a "Produced Work". Use inside an organisation and its contractors is not "Public", so share-alike does not trigger ([ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)) [D]. The OpenStreetMap Foundation's guideline treats one-off extracts of "less than 100 Features" as non-substantial, but systematic extraction is substantial ([OSMF guideline](https://wiki.osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline)) [D].
- **SNOMED CT.** Its licence defines a Derivative to include "a Cross-Map and a Sub-Set". Use and distribution in non-member territories carry fees and conditions ([SNOMED CT Affiliate Licence](https://isd.hscic.gov.uk/trud/users/guest/filters/0/licence/4)) [D].
- **Exchange market data.** Cboe Europe requires non-display rights for listed uses "whether or not the Market Data Client creates Derived Works with the Data". Internal use of delayed and historical data for research is fee-free, and there is a "Development Waiver" ([Cboe Europe Data Policy, effective 1 Aug 2026](https://cdn.cboe.com/resources/participant_resources/Cboe_Europe_Data_Policy_August_2026.pdf)) [D].

A practical classification follows [I]:

1. Copying real code values into test data is extraction.
2. Aggregates sit closer to "Produced Work", but market-data contracts can still cover any data "derived from" theirs.
3. Structure alone (formats, check-digit rules, cardinality ranges) carries the least risk.

The licensed-environment boundary may differ from the privacy boundary. A DP synthetic copy can be privacy-safe and still breach a licence, because the real code values are themselves the licensed content [I]. No court or regulator text was found on whether DP synthetic data is a derived work [D: gap].

## 5. One characterisation feeds two samplers: boundary injection for small sets, scaled sampling for large ones

Learned and marginal models decouple fit from size:

- **SDV.** `sample(num_rows)`, with `batch_size` for large runs ([SDV sampling](https://docs.sdv.dev/sdv/sampling/sample-realistic-data)) [D].
- **`mbi`.** `synthetic_data(rows=N)` takes any N [D].
- **SDV multi-table.** `sample_scale(scale=…)` keeps cardinality, with 1 giving "roughly the same size as the original data". SDV 2.0.0 added it on 2026-10-15 ([SDV HISTORY](https://github.com/sdv-dev/SDV/blob/main/HISTORY.md)) [D].
- **Hydra.** Its "minuscule memory-resident database summary" regenerates data of any size during query execution ([Hydra demo](https://www.vldb.org/pvldb/vol11/p1974-sanghi.pdf)) [D].
- **Statistics injection.** Injected statistics also work on a tiny database. The planner rescales `reltuples` to the physical file size, so absolute estimates shrink while the ratios stay correct ([boringSQL, 2026-03-08](https://boringsql.com/posts/portable-stats/)) [D].
- **Rule-based generators.** dbldatagen claims "billions of rows within minutes" [V].

No open-source tool documents billion-row sampling from a learned multi-table model end to end [I/gap].

Over-representing rare cases is where tools diverge:

- **SDV Community** supports single-table conditional sampling (`Condition(num_rows=250, …)`) ([SDV conditional](https://docs.sdv.dev/sdv/sampling/conditional/single-table)) [D].
- **SDV Enterprise** sells multi-table conditional sampling and "extrapolating outside training ranges" as paid bundles ([SDV compare](https://docs.sdv.dev/sdv/explore/compare-features)) [D; V].
- **MOSTLY AI** documents seeded conditional generation and rebalancing ([mostlyai README](https://github.com/mostly-ai/mostlyai)) [D API; V capability].
- **SDV's constraint handling** uses rejection sampling: "it may take multiple batches to create valid data" [D]. That slows down when the target region is rare, so conditioning beats rejection for strong over-representation [I].

Learned models do not extrapolate beyond their training ranges unless asked, so pure model sampling under-produces boundary values [I].

The practical answer is two samplers over one schema and one characterisation [I]:

- **Small edge-case sets.** Rule-based boundary injection uses the released range metadata: min and max, NULL, empty string, maximum length, Unicode, duplicate keys, orphan foreign keys, entities present in only one source, and maximum delay. Hypothesis strategies or Data Caterer's `enableEdgeCase`/`edgeCaseProbability` do this. Data Caterer's edge cases include Int.MaxValue, "", "\u0000" and non-Latin scripts ([Data Caterer generator docs](https://github.com/data-catering/data-caterer/blob/main/docs/docs/generator/data-generator.md)) [D]. Add conditional sampling with skewed condition weights and IAB-style "every value at least once" coverage [D for IAB].
- **Large performance sets.** Sample in independent, seeded batches, parents before children from the cardinality distribution. Seeding must be per entity or counter-based so that the output does not depend on the number of workers, as in PDGF's hierarchical table → column → row seeding ([PDGF slides, TPCTC 2010](https://www.tpc.org/tpctc/tpctc2010/TPCTC2010-04.pdf)) [D] or Myriad's random-access random number generators ([Myriad, VLDB 2012](https://www.vldb.org/pvldb/vol5/p1890_alexanderalexandrov_vldb2012.pdf)) [D].

For plan-level performance work there is a third, cheaper instrument: optimiser-statistics transport [D]:

- **PostgreSQL 18** added `pg_dump --statistics-only` and `pg_restore_relation_stats`/`pg_restore_attribute_stats`. **PostgreSQL 19** (released 2026-11-19) adds `pg_restore_extended_stats` ([PostgreSQL admin functions](https://www.postgresql.org/docs/current/functions-admin.html)).
- **Oracle.** Transporting statistics is "especially useful for testing an application using production statistics" ([Oracle 19c](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/transporting-optimizer-statistics.html)).
- **SQL Server.** `DBCC CLONEDATABASE` builds a schema-only, read-only copy with statistics. It is "only intended for troubleshooting and diagnostic purposes" ([Microsoft Learn](https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql)).

In boringSQL's demonstration, injecting histogram bounds and correlation flipped a sequential scan into an index scan, and an injected MCV list produced different plans for rare and common values ([boringSQL](https://boringsql.com/posts/portable-stats/)) [D]. Injected statistics "are likely to be overwritten by autovacuum" ([PostgreSQL docs](https://www.postgresql.org/docs/current/functions-admin.html)) [D]. Search extracts report November 2026 bugs in the restore functions, such as statistics attached to the wrong columns [L].

Statistics transport tests plan shape, join order and estimated costs. It does not test execution time, memory or spill behaviour, result correctness or data-dependent failures [I]. Fidelity is also capped: no engine's single-table statistics express join-crossing correlation [I].

## 6. No open generator simulates deliveries, so change over time needs its own layer

Benchmarks model change as deterministic batches:

- **TPC-DI** requires a historical load plus **two** incremental updates "to ensure repeatability". Incremental files carry `CDC_FLAG` (insert, update or delete) and a monotonic `CDC_DSN` sequence number. "A row may change multiple times in the course of a day". Its sources are heterogeneous (CDC extracts, CSV, variable-format newswire, XML). Its type-2 slowly changing dimensions use `EndDate` = 9999-12-31 for current rows ([TPC-DI v1.1.0, Nov 2014](https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-di_v1.1.0.pdf)) [D]. Its generator, DIGen, is built on PDGF, is "provided and maintained by Bankmark", and may not be modified (same source) [D].
- **TPC-DS** refresh sets consist of "new, deleted and changed data". Dimension maintenance was removed in v2.0 ([TPC-DS v4.0.0](https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-ds_v4.0.0.pdf)) [D].
- **LDBC SNB** emits update streams with inserts and, in version 2, deletes. Entities have lifespans, and deletions "follow a logic order" ([LDBC SNB spec](https://arxiv.org/pdf/2001.02299v11)) [D].

Learned sequential models learn per-entity sequences from real rows but know nothing about deliveries:

- **SDV PARSynthesizer** (BUSL) ([SDV PAR](https://docs.sdv.dev/sdv/sequential-data/modeling/parsynthesizer)) [D].
- **MOSTLY AI time series** [V].
- **DoppelGANger.** TensorFlow 1.x reference code; its authors say "we do not resolve the privacy problem" ([arXiv 1909.13403](https://arxiv.org/abs/1909.13403)) [D].

Agent-based simulators evolve entities over simulated time from parameter files:

- **Synthea** can advance a saved population: `-i` loads a snapshot, `-u` saves the updated one and `-t` sets the period in days. It also has an append mode for CSV export ([Synthea README](https://raw.githubusercontent.com/synthetichealth/synthea/master/README.md)) [D]. This is a native way to "advance the stand-in by N days".
- **PaySim**'s second version was calibrated from aggregated transaction logs ([PaySim](https://raw.githubusercontent.com/EdgarLopezPhD/PaySim/master/README.md)) [D]. It is the closest precedent for parameterising change from aggregates computed inside.
- **Debezium**'s Testcontainers support tests the CDC path with real DML against a container database. It does not generate change patterns ([Debezium](https://debezium.io/documentation/reference/stable/integrations/testcontainers.html)) [D].

**None of the surveyed tools generates corrections or restatements, re-deliveries, late or out-of-order arrival, or missing drops as a parameterised feature**. That is an absence finding from searches, not proof [I]. TPC-DI's slowly changing dimensions carry valid time only. `CDC_DSN` gives an order of application but no correction semantics, so restatements of past periods must be added explicitly [I].

"Data chaos engineering" is a practice without a framework. lakeFS demonstrates zero-copy "chaos branches": delete a date partition, run the job, observe ([lakeFS blog, modified 2026-02-05](https://lakefs.io/blog/chaos-data-engineering/)) [D; vendor engineering blog]. A small single-author project, Odibi, configures `duplicate_rate` and late arrival by batch label, and asserts exact injected counts ("3% of 1,440 = ~43") ([Odibi docs](https://henryodibi11.github.io/Odibi/simulation/patterns/data_engineering)) [D; maturity unknown]. Infrastructure chaos tools such as LitmusChaos and Toxiproxy inject faults into systems, not into data content [L].

The design that fits the constraints has two layers [I]:

- **Layer 1: entity state history.** A seeded generator of entity state over time, with LDBC/PDGF-style determinism, Synthea-style advancement and bitemporal validity intervals.
- **Layer 2: delivery simulator per source.** Its parameters are daily batch size, the insert/update/delete mix, the lateness distribution (arrival time minus event time), the duplicate re-delivery rate, the probability of a missing drop, the restatement rate and schema-change events.

Every Layer 2 parameter is an aggregate that can be computed inside and exported [I]. The fault library is cheap: pure, seeded, logged functions such as `drop`, `duplicate`, `delay`, `reorder`, `truncate`, `restate` and `schema_mutate`. Because each one is seeded and logged, every injected fault is enumerable and a test can assert exact counts [I]. Learned sequential models would have to be trained inside, with the model released after review [I].

## 7. Diff profiles inside, version the build identity, and pin failing cases as fixtures

Under an aggregates-only rule, drift detection means computing a profile inside on a schedule and diffing profiles outside. Tools that compare *statistics artefacts* fit better than tools that need two data frames [I].

| Tool | What it compares | Defaults that matter | Maintenance (date) |
|---|---|---|---|
| Deequ / PyDeequ | Metric time series in a `MetricsRepository` | `RelativeRateOfChangeStrategy` (e.g. row count more than doubles); `OnlineNormalStrategy` at 3.0 standard deviations; Holt-Winters seasonality ([example](https://raw.githubusercontent.com/awslabs/deequ/master/src/main/scala/com/amazon/deequ/examples/anomaly_detection_example.md)) [D] | PyDeequ 1.7.0 on 2026-09-14; repo pushed 2026-10-20 [D] |
| TFDV | Statistics protobufs against schema comparators | L-infinity (categorical only) and Jensen–Shannon thresholds ([TFDV](https://www.tensorflow.org/tfx/data_validation/get_started)) [D] | 1.21.0 on 2026-06-11 [D] |
| NannyML | Binned reference (stored bin edges + frequencies) | Raw values only below 10,000 reference rows; unseen values get a new bin with reference frequency 0 ([NannyML](https://nannyml.readthedocs.io/en/stable/how_it_works/univariate_drift_detection.html)) [D] | 0.13.1 on 2025-07-12; maintenance questionable [I] |
| Evidently | Two data frames | p-value tests up to 1,000 rows; above that, Wasserstein/JS at threshold 0.1 ([Evidently](https://docs.evidentlyai.com/metrics/explainer_drift)) [D] | 0.7.23 on 2026-09-11 [D]; fits only if run inside [I] |
| whylogs | Mergeable profiles | — | 1.6.4 on 2024-12-03; WhyLabs "discontinuing operations" after its founders joined Apple ([GeekWire, 2025-09-15](https://www.geekwire.com/2025/founders-at-seattle-startup-whylabs-join-apple-following-under-the-radar-acquisition)) [D] |
| Soda Core / Great Expectations | Checks and contracts | Scenario-testing features unverified; Soda docs [U] | 4.32.0 on 2026-11-25 / 1.25.0 on 2026-11-12, with its PyPI source now `fivetran/great_expectations` [D] |
| alibi-detect / deepchecks | — | Features not read | 0.13.0 on 2025-12-11 / 0.19.1 on 2024-12-15 [D] |

Two different drifts need tracking [I]:

- **Real versus real over time.** Does today's inside profile differ from the profile the stand-in was built from? Deequ-style metric series with Holt-Winters or online-normal detection fit this.
- **Real versus stand-in fidelity.** How far is the current inside profile from the stand-in's own profile? Shared bins on both sides, so that only bins leave, fit this.

At millions of rows, KS and chi-square p-values flag trivial differences. That is why Evidently switches to distances above 1,000 rows and NannyML bins above 10,000 [D for the defaults; I for the reason]. Schema drift is better diffed deterministically (column set, types, nullability, enum domains) than tested statistically [I].

Renewal and reproducibility rest on one idea: give every build an identity, here called the **identity tuple** [I]. It consists of:

- the characterisation ID (a hash of the exported profile)
- the generator name and version, as a container digest
- the configuration hash
- the master seed and per-source sub-seeds
- the delivery-fault plan

Store the tuple as an Iceberg tag or a lakeFS commit message, so any failing test report can name it [I]. Iceberg time travel supports `VERSION AS OF` a snapshot ID, branch or tag ([Iceberg Spark queries](https://iceberg.apache.org/docs/latest/spark-queries/)) [D]. lakeFS branches are zero-copy metadata snapshots [D, vendor engineering blog]. lakeFS has acquired DVC [D, banner]; DVC's latest release was 3.67.1 on 2026-03-31 [D].

The renewal loop runs in four steps [I]:

1. A scheduled job inside diffs the current profile against the stand-in's characterisation.
2. On a breach, or on a calendar schedule, the new profile passes the export gate and is versioned.
3. The generator rebuilds outside with a new characterisation ID.
4. The new build gets a new tag, and old tags are kept.

Hypothesis's documentation explains why failing cases must be stored independently of the generator ([Hypothesis API reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html)) [D]:

- Its example database "is best thought of as a cache". Entries "may be transparently dropped when upgrading your Hypothesis version or changing your test".
- `@reproduce_failure` "will error if used on a different Hypothesis version".
- `@example` always runs.
- A committed example directory "only makes sense if you also pin to an exact version of Hypothesis".

Failing tests therefore stay reproducible across renewals through three layers, from most to least durable [I]:

1. **The minimal failing case as an explicit fixture** (`@example` or a small pinned file). It survives upgrades of the generator and the libraries.
2. **The identity tuple.** It regenerates the full dataset only while the old generator version still runs.
3. **A pinned materialised dataset** (Iceberg tag, lakeFS commit or DVC hash). It survives generator changes but costs storage.

Learned generators reproduce only with pinned framework versions and deterministic kernels, so pin the trained artefact rather than retraining from a seed [I]. Each renewal of the characterisation also draws on the disclosure budget from Section 4 [I].

## 8. One contract can validate and generate, but only a prescriptive one should define "valid"

A single specification doing both jobs exists in open source, but only narrowly:

- **Pandera** turns DataFrame schemas into Hypothesis strategies with `schema.strategy(size=n)`. Pandera 0.36.0 was released 2026-11-10 [D]. Custom multi-column checks fall back to filtering, which "can be highly inefficient" ([Pandera docs](https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/data_synthesis_strategies.md)) [D].
- **hypothesis-jsonschema** turns a JSON Schema into a strategy. Release 0.23.2 was on 2026-10-27 ([README](https://raw.githubusercontent.com/python-jsonschema/hypothesis-jsonschema/master/README.md)) [D].
- **polyfactory** generates from Pydantic models and dataclasses. It is MIT, with release 3.5.0 on 2026-10-21 ([README](https://raw.githubusercontent.com/litestar-org/polyfactory/main/README.md)) [D].
- **ODCS with datacontract-cli** is the broadest route. The Open Data Contract Standard (ODCS) v3.2.0 is Apache-2.0 ([ODCS](https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/README.md)) [D]. datacontract-cli (1.2.11 on 2026-11-17) runs `datacontract test` against real sources and exports to JSON Schema, Pydantic, Great Expectations, SodaCL, dbt and a Data Caterer generation task ([datacontract-cli](https://raw.githubusercontent.com/datacontract/datacontract-cli/main/README.md)) [D].

The Data Caterer exporter carries type, uniqueness, enum, pattern and min/max into generation ([exporter code](https://github.com/datacontract/datacontract-cli/blob/main/datacontract/export/data_caterer_exporter.py)) [D]. ODCS `quality` rules are not translated into generation constraints [I, from the code read]. The project's claim that the export yields "production-like data" is its own [V]. Data Caterer can also take validations from Great Expectations and OpenMetadata, "so you can generate data for your upstream data sources and validate your pipelines based on the same rules" ([Data Caterer](https://github.com/data-catering/data-caterer/blob/main/docs/docs/validation/external-source-validation.md)) [D].

Several mature tools validate or test but have no first-party generator [D]:

- **Great Expectations, Soda, Frictionless and Deequ.** Validation only.
- **TFDV.** Its paper describes schema-guided synthetic inputs for fuzzing training code ([Breck et al., MLSys 2019](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)) [D]. Whether the open-source package exposes this is unverified [U].
- **SQLMesh.** `create_test` builds fixtures by querying populated warehouse tables ([SQLMesh tests](https://github.com/TobikoData/sqlmesh/blob/main/docs/concepts/tests.md)) [D]. That copies real rows and does not fit the constraint [I].
- **dbt.** Unit tests use static mock inputs ([dbt docs](https://github.com/dbt-labs/docs.getdbt.com/blob/current/website/docs/docs/build/unit-tests.md)) [D].

Inferring a spec from the data (Deequ suggestions, TFDV `infer_schema`, Frictionless `describe`, `datacontract import`) needs real rows inside. Only the spec leaves, but enum domains, regexes, min/max and ODCS `examples` can leak confidential values or licensed code lists [I].

On "normal ≠ correct", the evidence supports keeping **two artefacts** and never letting the production profile define validity:

- **TFDV.** The paper says the schema is "reverse-engineered and has to co-evolve with the data". When data and code disagree, "either the schema needs to change … or the training code needs to change" ([Breck et al.](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)) [D].
- **Jenga.** In Jenga's case study the automatically inferred schema was "too strict" and was adjusted by hand. It was then stress-tested with 250 random corruptions ([Jenga, EDBT 2021](https://ssc.io/pdf/jenga.pdf)) [D].
- **BART.** Its authors note "a duality between the problem of injecting detectable errors in clean data, and the problem of detecting violations" ([BART](https://www.vldb.org/pvldb/vol9/p36-arocena.pdf)) [D].
- **Schemathesis.** Its negative mode "mutates your schema" to produce data that must be rejected. Release 4.34.2 was on 2026-11-24 ([Schemathesis](https://github.com/schemathesis/schemathesis/blob/master/docs/explanations/data-generation.md)) [D].

The layering that follows has three parts [I]:

1. **A prescriptive contract.** Curated and reviewed by people. It drives both validation and positive generation.
2. **A descriptive profile.** Computed inside, exported as aggregates. It sets realism weights and known-defect frequencies, such as "3% of source X postcodes blank", but never validity.
3. **A defect catalogue.** Named mutations, each tagged with the expected platform response: accept, repair, quarantine or reject.

The same exported profile then feeds three consumers: the generator's weights, the drift diff in Section 7 and the defect frequencies. That is the shared foundation, and the profile is the only part that crosses the boundary [I]. No open-source tool generates table rows that violate exactly one contract rule ("negative mode" for tables), and no paper formally separates descriptive profiles from prescriptive contracts for platform testing [D: gaps].

## 9. Oracles built into the data and metamorphic relations carry most of the testing value

**Expected outcomes carried by the data.** This is standard practice wherever generated data has to be scored:

- **Data cleaning.** REIN keeps ground truth next to the dirty data ([REIN, arXiv 2302.04702](https://arxiv.org/abs/2302.04702)) [D]. Raha requires "a dirty dataset and its corresponding clean dataset" ([Raha](https://github.com/BigDaMa/raha/blob/master/README.md)) [D].
- **Record linkage.** GeCo and Gecko keep the true entity of each duplicate [D/L].
- **TPC-H.** Query output must match a fixed answer set computed on a qualification database at exactly SF = 1 ([TPC-H 3.0.1](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf)) [D].
- **DBMS testing.** Pivoted Query Synthesis (PQS) picks a pivot row that the query must return and found 121 unique bugs ([Rigger & Su, OSDI 2020](https://www.usenix.org/system/files/osdi20-rigger.pdf)) [D]. DQE adds row-identity columns to track each row ([SQLancer](https://github.com/sqlancer/sqlancer/blob/main/README.md)) [D].

For a multi-source platform this becomes a "true world, then rendered views" design [I]:

- Generate hidden entities and events.
- Render each source's view of them, with its own identifiers, coverage, delays and defects.
- Tag every row with its expected outcome.
- Score linkage by precision and recall against the true links, check rejection paths as exact row sets, and compute expected aggregates on the true world.

DQE-style tracer columns let a test follow each row's fate through the pipeline [I].

**Property-based testing.** Hypothesis (6.170.17 on 2026-11-20) is the mature core [D]. Its `RuleBasedStateMachine` generates "entire tests", with `Bundle`s of generated values, and compares a system against a simplified model ([Hypothesis stateful docs](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/docs/stateful.rst)) [D]. That maps directly onto delivery sequences: rules for "deliver batch from source k", "redeliver", "deliver correction" and "advance clock", with an in-memory reference model as the oracle [I].

The ecosystem around it:

- `polars.testing.parametric` exposes Hypothesis strategies ([polars](https://github.com/pola-rs/polars/blob/main/py-polars/src/polars/testing/parametric/__init__.py)) [D].
- spark-testing-base is maintained, with a commit on 2026-10-30 [D].
- sscheck is dormant since 2018 [D].
- chispa (0.12.0) and hypothesis-sqlalchemy (1.2.0) are current [D].

No primary source on property-based testing of ETL invariants was found [D: gap]. The candidate properties are proposals [I]:

- **Idempotent re-delivery.** Loading the same delivery twice gives the same target state as loading it once.
- **Order and split invariance.** Permuting a delivery, or splitting it into consecutive parts, does not change the result, except where corrections are meant to depend on order.
- **Count conservation.** Rows in = loaded + quarantined + rejected, per source and per delivery.
- **Format round-trip.** Parsing a serialised delivery gives back the original.
- **Contract closure.** Every output satisfies the output contract.
- **Source isolation.** A delivery from one source leaves entities seen only by other sources unchanged.

**Metamorphic and differential testing.** DBMS testing has a mature, maintained toolset aimed at engine bugs:

- **SQLancer** (last commit 2026-11-15). Its oracles include TLP, NoREC, PQS, DQE, QPG, CERT, DQP and CODDTest across DuckDB, PostgreSQL, DataFusion and others ([SQLancer](https://github.com/sqlancer/sqlancer/blob/main/README.md)) [D].
- **SQLsmith** (last commit 2026-11-16). It has found 118 bugs ([SQLsmith](https://github.com/anse1/sqlsmith/blob/master/README.org)) [D].
- **Pipeline-level work is thin.** MetaCDP proposes 10 metamorphic relations for containerised pipelines ([MetaCDP, 2024](https://scholarworks.montana.edu/handle/1/18983)) [L].

The transferable idea matters most under the brief's constraint [I]. A metamorphic relation needs no expected output, only a relation between two runs. It can therefore **run inside the protected environment on real deliveries and export only pass or fail and counts**, which exploits the diversity of the real data without moving rows out. Candidate relations:

- row permutation, delivery splitting and replay
- adding an unrelated source
- consistently renaming source-local identifiers
- TLP-style partitioning on p, ¬p and p IS NULL
- coverage monotonicity
- format equivalence: the same content as CSV, JSON or Parquet loads to the same result

Differential runs of the same SQL on the production engine and on DuckDB locally catch dialect drift [I]. dbt's `compute: local` is an example of local DuckDB execution [D].

**Fuzzing delivery formats.** Upstream parsers are already fuzzed in OSS-Fuzz:

- Arrow C++, built with CSV and Parquet enabled and seeded with Parquet `bad_data` files ([OSS-Fuzz arrow build](https://github.com/google/oss-fuzz/blob/master/projects/arrow/build.sh)) [D].
- Avro, the Jackson text formats, pandas, libxml2, simdjson and DuckDB ([OSS-Fuzz projects](https://github.com/google/oss-fuzz/tree/master/projects)) [D].
- CPython, with `fuzz_csv_reader` and `fuzz_json_loads` targets ([CPython fuzzer.c](https://github.com/python/cpython/blob/main/Modules/_xxtestfuzz/fuzzer.c)) [D].

No OSS-Fuzz project file was found for pyarrow, polars or fastavro [D]. So the platform's own job is its parsing, normalisation and rejection code, in three layers [I]:

1. **Byte-level fuzzing** with Atheris (3.1.0 on 2026-06-17, coverage-guided ([Atheris](https://github.com/google/atheris/blob/master/README.md))) [D] or Radamsa (mutates valid samples ([Radamsa](https://github.com/aoh/radamsa/blob/develop/README.md))) [D]. The oracle: no crash, no hang, and every input ends in a defined accept or reject state with a reason.
2. **Structure-aware generation** from the contract: dialects, quoting, byte-order marks, encodings, line endings.
3. **Semantic dirty data** from the defect catalogue.

The dirty-data generators are research code: BART (last commit 2023-05-10, PostgreSQL ≤ 11), Jenga (alpha, 2022), Raha (2025-06-05) and Gecko (beta) [D]. Data Caterer's edge-case options are the maintained but shallower alternative [I].

## Fields the brief did not name

Seven neighbouring fields have solved parts of this problem under their own vocabularies.

| Field | Named practice or term | What transfers | Evidence |
|---|---|---|---|
| Official statistics: terminology | CBS 2026 ladder: arbitrary, dummy, random, **simulated**, synthetic (full, partial, hybrid) | Output built only from metadata plus high-level aggregates is "simulated data". CBS recommends releasing the summary statistics themselves under SDC rather than a file labelled "synthetic" ([CBS, July 2026](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)) | [D] |
| Official statistics: ONS | Six-level spectrum: structural, valid, plausible, multivariate plausible, multivariate detailed, replica | Levels 1–2 for code testing, built from metadata and open sources ([ONS WP16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)) | [D]; date about 2018 [I] |
| Official statistics: remote execution | IAB "Testdaten"; validation and verification servers | Test-before-submit governance: "non-workable evaluation programs … will be returned" ([IAB](https://doku.iab.de/fdz/ba/Hilfe_Testdaten_e.pdf)). IAB and ONS files come from real rows, so only their structural rules transfer [I] | [D] |
| Microsimulation / population synthesis | IPF, entropy list balancing, quasirandom integer sampling, "microsynthesis" | Fit entities to multi-level marginal controls. PopulationSim (0.10.0, 2025-11-03; commit 2026-11-05) needs a real seed sample ([docs](https://activitysim.github.io/populationsim/)). humanleague QIS needs none ([README](https://raw.githubusercontent.com/virgesmith/humanleague/main/README.md)). mipfp 3.2.3 (2026-08-22); simPop CRAN stale since 2024 but GitHub 2026-01-20; ipfn and the Python population-synthesis package named synthpop are dormant; OpenFisca-core 46.1.0 (2026-11-24) | [D] |
| Healthcare | Simulacrum "data cubes"; OpenSAFELY dummy data and Airlock; Synthea's PADARSER principle (publicly available data instead of real records); Eunomia; CMS DE-SynPUF | Simulacrum builds cubes from ≥50 patients inside, releases them, and samples outside ([Simulacrum](https://simulacrum.healthdatainsight.org.uk/?p=3940)). OpenSAFELY generates dummy patients from the dataset definition, and the same command yields real data inside ([OpenSAFELY](https://docs.opensafely.org/ehrql/how-to/dummy-data/)). Synthea is very active (commit 2026-11-25), but its initial validation found several outcomes badly off ([JAMIA](https://pmc.ncbi.nlm.nih.gov/articles/PMC7651916/)). CPRD's Bayesian-network datasets [L] | [D] except CPRD |
| Financial-crime simulation | Parameter files; typologies | Time-bucketed count, sum, mean and standard deviation per event type; balance histograms; degree sequences ([PaySim repo](https://github.com/EdgarLopezPhD/PaySim); [AMLSim](https://raw.githubusercontent.com/IBM/AMLSim/master/README.md)). Even these aggregates were treated as too sensitive to share openly ([NTNU chapter](https://ntnuopen.ntnu.no/ntnu-xmlui/handle/11250/2588208)) [L]. AMLworld was calibrated to public aggregates and released data but not code ([arXiv 2306.16424](https://arxiv.org/html/2306.16424v3)) | [D] |
| Database benchmarking and optimiser statistics | Workload-aware / "dataless" databases; annotated query plans; statistics transport | See Sections 2 and 5 | [D] |
| Test-data management | Subsetting, masking, deterministic transformation | Jailer (2026-11-24), Greenmask (2026-11-25) and PostgreSQL Anonymizer (2026-11-25) are active; Condenser has been dormant since 2023; Neosync is "no longer actively maintained" ([Neosync](https://raw.githubusercontent.com/nucleuscloud/neosync/main/README.md)). The output is real rows, so the tools do not fit; FK ordering and keyed hashing transfer | [D]; non-fit [I] |
| TRE output checking | Five Safes, statbarns (statistical barns) | Thresholds of 5 or 10 "to protect against differencing" ([SACRO](https://zenodo.org/records/10282526/files/The%20SACRO%20guide%20to%20statistical%20output%20checking.pdf)) | [D] |

Two cautions from these fields bear repeating. First, CBS classes agent-based model output as *synthetic*, because "fine-tuning and validating sound agent-based models require intensive use of real-world data on the unit level" ([CBS](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)) [D]. Calibrating such models under an aggregates-only rule therefore means running the comparison inside and releasing only fit statistics [I]. Second, the UK Data Service warns that synthetic data are "not inherently 'safe' simply because they are not real" [L]. Geospatial small-area synthesis, smart-meter, telecom and supply-chain data were not researched [D: gap].

## What exists off the shelf, what must be built, and the open trade-offs

| Need | Off the shelf | Must be built |
|---|---|---|
| Characterisation computed inside | Deequ/TFDV/ydata profiles, `pg_stats` and extended statistics, OpenDP/Tumult DP marginals [D] | Custom aggregate queries for join-degree histograms, cross-source overlap matrices, ID-mismatch rates and lag distributions [I] |
| Export gate | ACRO/SACRO rules, sdcTable, OpenDP accounting [D] | Redaction of MCVs and bounds, data-independent bins, a per-entity budget ledger, licence classification per source [I] |
| Single-table and joint realism | `mbi`/MST/AIM; humanleague QIS [D] | Binning policy and structural-zero rules [I] |
| Plan and performance fidelity | DBRepro, Mirage (PostgreSQL); statistics transport in PostgreSQL 18/19, Oracle, SQL Server [D] | Support for other engines; disclosure review of plans and predicate constants [I] |
| Multi-table skeleton and volume | Snowfakery, Data Caterer, Faker/Mimesis; seeded parallel generation [D] | Children-per-parent models fitted to released degree histograms [I] |
| Same entity across sources | Gecko/Febrl corruption; Splink examples [D] | The multi-source renderer: coverage, per-source identifiers, lag, crosswalk oracle [I] |
| Change over time | TPC-DI/LDBC patterns; Synthea population advancement [D] | The delivery-process layer and its fault library [I] |
| Edge-case sets | Hypothesis, Pandera, hypothesis-jsonschema, Schemathesis-style negation, Data Caterer edge cases [D] | Table-level "violate exactly one rule" generation; the defect catalogue with expected outcomes [I] |
| Usefulness | Validation-server pattern; SynthEval/SDMetrics run inside [D] | The workload-fidelity vector, run on a pinned pipeline in inside CI [I] |
| Drift and renewal | Deequ metric series, TFDV comparators, Iceberg tags, lakeFS/DVC, Hypothesis `@example` [D] | Identity tuple, renewal job, fixture promotion [I] |
| Shared foundation | ODCS + datacontract-cli exporters; Pandera strategies [D] | Carrying cross-row, cross-table and cross-source rules into generation [I] |

The open trade-offs are these [I unless tagged]:

1. **Fidelity versus disclosure.** More released aggregates, especially joint and join-crossing ones, raise fidelity and spend reconstruction budget at the same rate. Join-crossing correlations are both the most valuable characteristic and the most expensive to release.
2. **Simulated versus synthetic.** Training a model inside (family C) captures more joint structure, but the model itself becomes a release needing approval. And NIST finds DP deep models weaker than marginal methods [D].
3. **Plan fidelity versus correctness coverage.** The workload-aware generators target known queries on one engine. Edge-case correctness, dirty formats and cross-source overlap need different generators over the same characterisation.
4. **Renewal frequency versus budget.** One DP characterisation per schema version is cheap; drift-triggered refreshes compose.
5. **Regenerate versus materialise.** Regeneration from the identity tuple is cheap until the generator changes. Pinned datasets survive change but cost storage.
6. **Licence and ownership risk.** SDV (BUSL), dbldatagen (Databricks License) and ClavaDDPM (no licence) restrict use [D]. Tumult, WhyLabs and Neosync show how quickly ownership of open tools moves [D].
7. **Metric choice at scale.** Significance tests always reject at millions of rows [D, Alam]. Effect-size tolerances must be agreed up front.

## Conclusion

The brief frames the work as finding a generator. The evidence says the decisive artefact is instead the **characterisation as a reviewed release**: a versioned, disclosure-checked, licence-classified set of aggregates. One artefact drives generation, drift detection and realism weights, and its version is part of every failing test's identity. Once the characterisation is the product, most tool choices become interchangeable, and the hard questions move to governance: which joint and join-crossing aggregates are worth their disclosure cost, what the unit of privacy is after entity resolution, and how often renewal may spend budget. The fields that already live under this constraint (Simulacrum, OpenSAFELY, IAB, Census validation) show it is workable. They also show its ceiling, "the more complex the data query the more approximate the results", which no generator removes.

The other shift concerns where testing value lies. Realism fitted from aggregates will always lag the real data on rare combinations and cross-source quirks. Two practices do not depend on realism at all, and both work under the boundary rather than against it. Oracles built into a generated "true world" give exact expected outcomes outside. Metamorphic relations, run inside on real deliveries with only pass/fail counts exported, test against the real data's full diversity without moving a row. A platform that pairs a modest, well-governed characterisation with those two practices gets most of the value of realistic data for a fraction of the disclosure cost.

## Sources and dates

All sources were accessed on 2026-11-26. "Label" is the strongest evidence level reached for the source by any research track.

| Source | Date | Label |
|---|---|---|
| [Leis et al., "How good are query optimizers, really?", PVLDB 9(3)](https://www.vldb.org/pvldb/vol9/p204-leis.pdf) | 2015 | D |
| [Boncz et al., JCC-H, TPCTC](https://ir.cwi.nl/pub/27429/27429.pdf) | 2017 | D |
| [Vogelsgesang et al., "Get Real", DBTest](https://cs.cit.tum.de/fileadmin/w00cfj/dis/papers/getreal.pdf) | 2018 | D (L in one track) |
| [Sanghi, "Beyond Row Counts", CEUR Vol-3931](https://ceur-ws.org/Vol-3931/short5.pdf) | 2025 | D |
| [Zhang et al., DBRepro, arXiv 2608.27822](https://arxiv.org/pdf/2608.27822) | 28 Aug 2026 | D; results V |
| [Sanghi et al., Hydra demo, PVLDB 11(12)](https://www.vldb.org/pvldb/vol11/p1974-sanghi.pdf) | 2018 | D; IISc site U |
| [Li et al., Touchstone, USENIX ATC](https://www.usenix.org/system/files/conference/atc18/atc18-li-yuming.pdf) | 2018 | D; speed-up V |
| [Yang et al., SAM, SIGMOD](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf) | 2022 | D |
| [Arasu, Kaushik, Li, SIGMOD](https://people.iiis.tsinghua.edu.cn/~jianli/paper/mod311arasu.pdf) | 2011 | D |
| [Mirage README](https://raw.githubusercontent.com/dbhammer/mirage/main/README.md) | pushed 2026-07-28 | D; paper L |
| [TPC-H 3.0.1](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf) / [TPC-DS 4.0.0](https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-ds_v4.0.0.pdf) / [TPC-DI 1.1.0](https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-di_v1.1.0.pdf) | 2022 / Nov 2024 / Nov 2014 | D |
| [LDBC SNB specification, arXiv 2001.02299v11](https://arxiv.org/pdf/2001.02299v11) | Sep 2024 | D |
| [PostgreSQL 19 docs: pg_stats, planner statistics, admin functions, pg_statistic](https://www.postgresql.org/docs/current/view-pg-stats.html) | v19 released 2026-11-19 | D |
| [boringSQL, "Production query plans without production data"](https://boringsql.com/posts/portable-stats/) | 2026-03-08 | D; size claim V |
| [Oracle 19c, transporting optimizer statistics](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/transporting-optimizer-statistics.html); [SQL Server DBCC CLONEDATABASE](https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql) | current | D |
| [Private-PGM / mbi](https://github.com/ryan112358/private-pgm) | 2.1.0, 2026-11-06 | D |
| [SmartNoise SDK](https://github.com/opendp/smartnoise-sdk) | 1.0.8, 2026-04-15 | D |
| [SDV LICENSE](https://github.com/sdv-dev/SDV/blob/main/LICENSE), [HISTORY](https://github.com/sdv-dev/SDV/blob/main/HISTORY.md), [compare features](https://docs.sdv.dev/sdv/explore/compare-features) | 2.2.0, 2026-11-06 | D; capabilities V |
| [MOSTLY AI SDK](https://github.com/mostly-ai/mostlyai) | 6.2.1, 2026-10-29 | D API; capabilities V |
| [ClavaDDPM, arXiv 2405.17724](https://arxiv.org/abs/2405.17724); [PrivLava](https://arxiv.org/abs/2304.04545); [PrivPetal](https://arxiv.org/abs/2503.22970) | 2024; 2023; 2025 | D (abstracts) |
| [Christen & Vatsalan, GeCo, CIKM](https://users.cecs.anu.edu.au/~christen/publications/christen2013cikm.pdf) | 2013 | D (U in two tracks) |
| [Gecko](https://github.com/ul-mds/gecko); [Splink datasets](https://github.com/moj-analytical-services/splink/blob/master/docs/includes/generated_files/datasets_table.md) | 0.6.4, 2024-12-06; 5.0.0, 2026-09-28 | D |
| [SERD PDF](https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/4-6-Synthesizing_Entity_Resolution_Datasets.pdf) | undated (venue unverified) | D |
| [Dwork & Roth, Algorithmic Foundations of DP](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) | 2014 | D |
| [Abowd et al., 2010 Census reconstruction, arXiv 2312.11283v3](https://arxiv.org/abs/2312.11283) | 28 Jul 2025 | D |
| [Abowd et al., 2020 TopDown Algorithm, arXiv 2204.08986](https://arxiv.org/abs/2204.08986) | 2022 | D |
| [Stadler et al., USENIX Security](https://arxiv.org/abs/2011.07018); [Annamalai et al.](https://arxiv.org/abs/2301.10053); [TAPAS](https://arxiv.org/abs/2211.06550) | 2022; 2024; 2022 | D |
| [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf) | March 2025 | D |
| [SACRO guide to statistical output checking](https://zenodo.org/records/10282526/files/The%20SACRO%20guide%20to%20statistical%20output%20checking.pdf) | Oct 2023 | D |
| [ONS, Protecting personal data in Census 2021](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/protectingpersonaldataincensus2021results) | current | D |
| [ACRO](https://pypi.org/project/acro/); [Tumult Analytics](https://raw.githubusercontent.com/opendp/tumult-analytics/main/README.md); [OpenDP news](https://opendp.org/news-events) | 1.1.0, 2026-11-05; 0.21.0, 2026-06-30; Oct 2026 | D |
| [EDPB Guidelines 01/2025](https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf); [ICO anonymisation guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/about-this-guidance/) | Jan 2025; 28 Mar 2025 | D |
| [CJEU EDPS v SRB commentary](https://www.insideprivacy.com/eu-data-protection/eu-court-of-justice-clarifies-the-concept-of-personal-data-in-the-context-of-a-transfer-of-pseudonymized-data-to-third-parties/) | 4 Sep 2025 | L; judgment U |
| [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/); [OSMF Substantial guideline](https://wiki.osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline); [SNOMED CT Affiliate Licence](https://isd.hscic.gov.uk/trud/users/guest/filters/0/licence/4); [Cboe Europe Data Policy](https://cdn.cboe.com/resources/participant_resources/Cboe_Europe_Data_Policy_August_2026.pdf) | —; —; undated; effective 1 Aug 2026 | D |
| [Census SIPP Synthetic Beta](https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html); [SynLBD analytic validity](https://www.census.gov/programs-surveys/ces/data/public-use-data/synthetic-longitudinal-business-database/analytic-validity.html) | rev. 17 Nov 2026; rev. 12 Feb 2025 | D |
| [Barrientos et al., arXiv 2110.12055v3](https://arxiv.org/pdf/2110.12055v3.pdf) | 30 Jun 2023 | D |
| [Alam, Dostie, Drechsler, Vilhuber](https://zenodo.org/records/3832173/files/AlamDostieDrechslerVilhuber_20200518.pdf) | 18 May 2020 | D |
| [Burman et al., synthetic PUF and validation server](https://www.taxpolicycenter.org/sites/default/files/publication/156011/safely_expanding_research_access_to_administrative_tax_data_creating_a_synthetic_public_use_file_and_a_validation_server_0.pdf) | 2018 | D |
| [Urban validation server v2.0](https://www.urban.org/research/publication/privacy-preserving-validation-server-version-2) | 11 Sep 2024 | D (landing page); PDF U |
| [SDMetrics](https://raw.githubusercontent.com/sdv-dev/SDMetrics/main/README.md); [SynthEval](https://raw.githubusercontent.com/schneiderkamplab/syntheval/main/README.md); [SDNist](https://raw.githubusercontent.com/usnistgov/SDNist/main/README.md) | 0.33.1, 2026-11-25; 1.7.3, 2026-10-23; v2.5 | D |
| [CBS, Synthetic Data Terminology in Official Statistics](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf) | July 2026 | D |
| [ONS Working Paper 16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot) | undated (about 2018, I) | D |
| [IAB BA panel test data](https://doku.iab.de/fdz/ba/Hilfe_Testdaten_e.pdf); [IAB SIAB test data](https://doku.iab.de/fdz/siab/SIAB_Testdaten_en.pdf) | undated | D |
| [Simulacrum method](https://simulacrum.healthdatainsight.org.uk/?p=3940); [NCRAS guide](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/893386/NCRAS_guide_to_using_the_Simulacrum_and_submitting_code.pdf) | v2.1.0 Apr 2023; June 2020 | D |
| [OpenSAFELY dummy data](https://docs.opensafely.org/ehrql/how-to/dummy-data/); [Synthea, JAMIA](https://pmc.ncbi.nlm.nih.gov/articles/PMC7651916/) | current; 2017/2018 | D |
| [PopulationSim](https://activitysim.github.io/populationsim/); [humanleague](https://raw.githubusercontent.com/virgesmith/humanleague/main/README.md) | 0.10.0, 2025-11-03; 2.4.5, 2026-08-29 | D |
| [PaySim](https://github.com/EdgarLopezPhD/PaySim); [AMLSim](https://raw.githubusercontent.com/IBM/AMLSim/master/README.md); [AMLworld](https://arxiv.org/html/2306.16424v3) | 2021; 2022; Jan 2024 | D |
| [Evidently drift](https://docs.evidentlyai.com/metrics/explainer_drift); [NannyML](https://nannyml.readthedocs.io/en/stable/how_it_works/univariate_drift_detection.html); [Deequ anomaly detection](https://raw.githubusercontent.com/awslabs/deequ/master/src/main/scala/com/amazon/deequ/examples/anomaly_detection_example.md); [TFDV](https://www.tensorflow.org/tfx/data_validation/get_started) | 0.7.23; 0.13.1; 1.7.0; 1.21.0 | D |
| [GeekWire on WhyLabs](https://www.geekwire.com/2025/founders-at-seattle-startup-whylabs-join-apple-following-under-the-radar-acquisition) | 2025-09-15 | D |
| [Hypothesis API reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html); [Iceberg Spark queries](https://iceberg.apache.org/docs/latest/spark-queries/); [lakeFS chaos blog](https://lakefs.io/blog/chaos-data-engineering/) | 6.170.17, 2026-11-20; current; mod. 2026-02-05 | D (lakeFS vendor blog) |
| [Pandera strategies](https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/data_synthesis_strategies.md); [datacontract-cli](https://raw.githubusercontent.com/datacontract/datacontract-cli/main/README.md); [Data Caterer](https://github.com/data-catering/data-caterer/blob/main/README.md) | 0.36.0, 2026-11-10; 1.2.11, 2026-11-17; commit 2026-02-14 | D; "production-like" V |
| [Breck et al., TFDV, MLSys](https://mlsys.org/Conferences/2019/doc/2019/167.pdf); [Jenga, EDBT](https://ssc.io/pdf/jenga.pdf); [BART, PVLDB](https://www.vldb.org/pvldb/vol9/p36-arocena.pdf); [REIN](https://arxiv.org/abs/2302.04702) | 2019; 2021; 2015; 2023 | D |
| [Schemathesis data generation](https://github.com/schemathesis/schemathesis/blob/master/docs/explanations/data-generation.md); [SQLancer](https://github.com/sqlancer/sqlancer/blob/main/README.md); [PQS, OSDI](https://www.usenix.org/system/files/osdi20-rigger.pdf) | 4.34.2, 2026-11-24; commit 2026-11-15; 2020 | D |
| [MetaCDP](https://scholarworks.montana.edu/handle/1/18983) | 2024 | L |
| [OSS-Fuzz arrow build](https://github.com/google/oss-fuzz/blob/master/projects/arrow/build.sh); [Atheris](https://github.com/google/atheris/blob/master/README.md); [Radamsa](https://github.com/aoh/radamsa/blob/develop/README.md) | current; 3.1.0, 2026-06-17; current | D |
| Industry shadow and parity testing (Segment, Yelp, Totango, Diffy) | various | L; Segment original URL U |
