# Data characteristics a synthetic stand-in must capture, and characterisation-driven generators from database research and benchmarking

Labels used throughout: **[D]** documented (I read the full text, or the relevant full section of an official doc or README). **[I]** my inference. **[L]** lead only (search extract, full text not read). **[U]** source unreachable. **[V]** vendor or author self-claim, i.e. marketing or a claim the paper does not independently verify. Repo dates are `pushed_at` values from GitHub's search API on 2026-11-26 unless I say otherwise. Direct `repos/` API calls were refused in this session, and the search API returned metadata. Today's date is 2026-11-26.

## Characteristics inventory: what a stand-in must reproduce, why, how hard, and with which methods

### Takeaway
Schema and per-column marginals are easy to capture and reproduce. The hard part, and the part that predicts query plans, failures and performance, has four pieces:
- correlations that cross joins
- join fan-out and skew
- duplication and physical ordering
- string and format realities (strings used as keys, non-ASCII text, collations, dates stored as strings)

Standard benchmark generators (TPC-H, TPC-DS) deliberately assume uniformity and independence, so they miss exactly these properties. Cross-source entity overlap (coverage, identifier mismatch, delays) and arrival patterns are not addressed by any database-benchmark generator I found. They need entity-resolution and error-injection generators or custom work.

### Cited Findings

**Evidence that "realistic" means non-uniform, correlated and messy**
- [D] Cardinality estimators rest on uniformity and independence. The TPC-H, TPC-DS and SSB generators use "the very same simplifying assumptions (uniformity, independence, principle of inclusion)". As a result, PostgreSQL's simple estimator "works unrealistically well for TPC-H". IMDB, by contrast, "is full of correlations and non-uniform data distributions". — [Leis et al., "How good are query optimizers, really?", PVLDB 9(3), 2015](https://www.vldb.org/pvldb/vol9/p204-leis.pdf)
- [D] On real data (the JOB benchmark over IMDB), estimates in all tested systems are sometimes wrong by orders of magnitude: underestimates up to a factor of 10^8 and overestimates up to 10^4. Errors "grow exponentially … as the number of joins increases". Systems "systematically underestimate the results sizes of queries with multiple joins", and "No system tested was able to detect join-crossing correlations". — [Leis et al. 2015](https://www.vldb.org/pvldb/vol9/p204-leis.pdf)
- [D] TPC-H synthetic data "has been rife with uniformity, in terms of (a) value distributions, (b) frequency distributions and (c) join fan-out distributions", whereas deployed systems face data "typically skewed in all these aspects". Sampling-based estimation "catches any correlation within a single table". Join-crossing correlations remain elusive: their example is a model introduced in 2009 that has no sales before 2009, which leads to mis-estimates on the joined SALES table. — [Boncz, Anadiotis, Kläbe, "JCC-H", TPCTC 2017](https://ir.cwi.nl/pub/27429/27429.pdf)
- [D] The TPC-H spec defines "random" as "independently selected and uniformly distributed over the specified range". Temporal dependencies are simple offsets, for example L_RECEIPTDATE = L_SHIPDATE + random value [1..30]. Table sizes scale exactly with the scale factor (SF). — [TPC-H Standard Specification 3.0.1 (PDF dated 2022-04-28)](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf)
- [D] Get Real is an analysis of about 62k real Tableau workbooks. Its findings:
  - TPC-H uses integer keys, while "the real-world dataset mostly features strings as keys".
  - Dates and booleans are often stored as strings and parsed at query time, for example with TO_TIMESTAMP, and fiscal years appear as strings such as "2017/18".
  - "64% of the strings contain non-ASCII characters", and "over 85% of the string columns … have a collation".
  - NULL-handling expressions (IS NULL, COALESCE, NULLIF) are very frequent.
  - Benchmarks scale data size, but real queries are large and complex over small datasets.
  
  — [Vogelsgesang et al., "Get Real: How Benchmarks Fail to Represent the Real World", DBTest 2018](https://cs.cit.tum.de/fileadmin/w00cfj/dis/papers/getreal.pdf)
- [D] Generators that match only "volumetric similarity" (operator output row counts) neglect "data duplication, value ordering, data skew, and correlations, which significantly affect query performance". Duplication causes "inefficient hash bucket usage, leading to spills and longer probe times". Presortedness changes sort cost. The paper proposes models of "Duplication Distribution" and "Presortedness", ways to extract them from query execution, and ways to mimic them. — [Sanghi, "Beyond Row Counts", EDBT/ICDT 2025 workshop (CEUR Vol-3931)](https://ceur-ws.org/Vol-3931/short5.pdf)
- [D] Workload-aware generators such as Hydra and Touchstone "neglect data distribution metrics such as NDV, inducing data skew and thus triggering severe hash collisions and unintended disk spilling". Separately, PostgreSQL's catalog statistics "rely on periodic sampling and lack exact global aggregations like precise distinct counts or min/max bounds". — [Zhang et al., "DBRepro", arXiv 2608.27822, 28 Aug 2026](https://arxiv.org/pdf/2608.27822)
- [D] PostgreSQL's planner "normally assumes that multiple conditions are independent of each other, an assumption that does not hold when column values are correlated". When it misses a functional dependency it underestimates. — [PostgreSQL 19 docs, §14.2 Statistics Used by the Planner](https://www.postgresql.org/docs/current/planner-stats.html)
- [D] Extended statistics "are not currently used by the planner for selectivity estimations made for table joins". — [PostgreSQL 19 docs, CREATE STATISTICS](https://www.postgresql.org/docs/current/sql-createstatistics.html)
- [D] Hybrid hash join spill code needs "high skew on the outer join attribute". Testing memory managers needs specific intermediate cardinalities. Arasu et al. use these examples to motivate declarative data characteristics. — [Arasu, Kaushik, Li, "Data Generation using Declarative Constraints", SIGMOD 2011](https://people.iiis.tsinghua.edu.cn/~jianli/paper/mod311arasu.pdf)
- [D] LDBC SNB Datagen reproduces several realistic properties:
  - a person-degree ("knows") distribution "similar to that found in Facebook"
  - attribute values drawn from DBpedia dictionaries, "realistic and correlated", for example names correlated with countries
  - homophily-style edges built along "correlation dimensions"
  - power-law comment generation and burst "flashmob event" posting distributions, i.e. temporal spikes
  
  It is deterministic regardless of the number of machines. — [LDBC SNB specification, arXiv 2001.02299 (PDF version 2024-09-10)](https://arxiv.org/pdf/2001.02299)
- [D] Data-cleaning benchmarks need controlled error injection. BART injects errors that violate denial constraints (FDs, CFDs, editing rules). It lets the user control the percentage of errors, whether errors are detectable, and "repairability". The generation problem is NP-complete, so BART uses a greedy algorithm. — [Arocena et al., "Messing Up with BART", PVLDB 9(1), 2015](https://www.vldb.org/pvldb/vol9/p36-arocena.pdf)
- [L] GeCo (Christen & Vatsalan, 2013) generates personal-data records and corrupted duplicates (several duplicates per original record), and can corrupt an existing dataset. Its successor `gecko-syndata` says GeCo was Python 2.7 and inactive since 2013. — search extracts of [Christen & Vatsalan 2013](https://users.cecs.anu.edu.au/~christen/publications/christen2013cikm.pdf) (PDF [U]: connection reset). `gecko-syndata` 0.6.4 was released 2024-12-06 under the MIT licence according to [PyPI](https://pypi.org/project/gecko-syndata/) [D for version and date].

**Inventory table.** Ease: E = easy, M = medium, H = hard. "Aggregate-exportable?" asks whether the characterisation can be expressed without row-level data. The "Methods/tools" column cites the findings above.

| Characteristic | Why it matters (correctness / failure / performance) | Ease to capture → reproduce | Aggregate-exportable? | Methods/tools that capture it |
|---|---|---|---|---|
| Schema, types, PK/FK/unique/check constraints | Correctness: constraint violations, type coercion. Get Real shows "pragmatic" schemas with strings as keys [D] | E → E | Yes (DDL) | pg_dump --schema-only; DBCC CLONEDATABASE (schema+stats); every generator takes schema as input [D] |
| Marginal value distributions (histograms) | Selectivity estimates, so plan choice (boringSQL shows a plan flip from injected histogram bounds) [D] | E → E (single column) | Mostly, but histogram bounds are real values [D: pg_stats "list of values"] | pg_stats histogram_bounds; Oracle/SQL Server stats; ydata/TFDV/Deequ profiles; RSGen (reverses column stats) [L]; DBRepro initial distribution from column stats [D] |
| Skew / heavy tails / MCVs | Hash-join spills, partition hot spots, plan flips between rare and common values (boringSQL MCV example: bitmap scan for 1.5 % vs seq scan for 95 %) [D] | E/M → E per column. Long-tail rare combinations are H | MCV lists contain real values [D] | pg_stats most_common_vals/freqs; JCC-H -k flag adds skew [D]; Arasu-style histogram-as-constraints [D] |
| NULL fraction and NULL patterns (co-missingness) | Correctness of 3-valued logic, outer joins, COALESCE paths (Get Real: NULL handling is frequent) [D] | E (null_frac) → E. Joint NULL patterns are M | Yes | pg_stats null_frac [D]; Touchstone meta-table "percentage of Null values" [D]; ydata "detailed analysis of missing data" [D] |
| Distinct counts (NDV), cardinalities | Group-by / hash table sizing, join estimates; NDV errors cause hash collisions/spills [D DBRepro] | E/M (sampled estimates are inexact [D DBRepro]) → E | Yes | pg_stats n_distinct (positive or negative ratio form) [D]; Deequ approx distinct [D]; extended ndistinct for column groups [D] |
| Within-table correlation / functional dependencies | Underestimation when the planner assumes independence [D PG docs]; correctness of business rules (e.g. amount = qty × price, REMIX example) [D] | M → M | Partly: PG extended stats (dependencies, ndistinct, multivariate MCV) are aggregates over a sample, but MCV items are real value combinations [D] | CREATE STATISTICS; ydata correlations [D]; DataSynth/Myriad/PDGF dependency specs [D]; SAM learns the joint distribution from cardinalities [D] |
| Physical ordering / presortedness | Index scan cost (pg_stats `correlation` is physical-vs-logical order) [D]; sort cost [D Sanghi 2025] | E (correlation coefficient) → M | Yes | pg_stats correlation [D]; Sanghi 2025 presortedness model [D] |
| Duplication distribution (value multiplicities) | Hash bucket usage, spills, DISTINCT/UNION cost [D Sanghi 2025] | M → M | Yes (frequency-of-frequency) | Sanghi 2025 [D]; PiGen projection (DISTINCT/GROUP BY) cardinalities [D] |
| Referential integrity and orphan rates | Correctness of inner vs outer joins; load failures | E → E (strict FK). Orphans/dangling FKs are M | Yes (counts) | Generators enforce PK–FK; SAM requires acyclic FK joins [D] |
| Join fan-out / join-degree distribution | Join output size, skewed partitions, nested-loop vs hash choice. TPC-H join fan-out is uniform [D JCC-H] | M → M | Yes (degree histograms) | LDBC Datagen degree distributions [D]; Touchstone/Mirage join cardinality constraints [D]; SAM "Group-and-Merge" join key assignment [D] |
| Cross-table (join-crossing) correlations | Multi-join misestimation by orders of magnitude; no tested optimizer detects them [D Leis] | **H** → **H** | Yes as join cardinalities or annotated plans, but the constraint count explodes | JCC-H (synthetic only) [D]; Hydra/Mirage/Touchstone/SAM via query-plan cardinalities [D]; PG extended stats cannot express them [D] |
| Long-tail rare combinations | Edge-case correctness bugs; rare plan branches | **H**: sampling-based stats miss them [I]; small MCV lists truncate [D: target controls list length] | Exporting them risks re-identification [I] | Only partially covered by any tool [I] |
| String formats, lengths, encodings, collations | Parsing failures, collation-dependent ordering and comparisons, width-driven memory (avg_width) [D Get Real; D pg_stats avg_width] | M → **H** (format grammars and variants) | Length/width stats yes; format patterns only if abstracted [I] | pg_stats avg_width [D]; Touchstone avg/max varchar length [D]; TPC-DS dsdgen generates international characters [D]; format variants are not covered by DB generators [I] |
| Dirty values, format variants, violated rules | Robustness of ingestion and validation; cleaning correctness | M → M (controlled injection) | Yes as rates per rule [I] | BART (denial-constraint violations, error %) [D]; GeCo/gecko corruption [L] |
| Duplicates / near-duplicates of the same entity | Dedup/entity-resolution correctness; join explosion | M → M | Rates and similarity distributions yes [I] | GeCo/Febrl-style duplicate generators [L]; ydata duplicate-row count (exact only) [D] |
| Cross-source overlap of the same entity (coverage, identifier mismatch, delays) | Matching correctness, late-arriving updates, double counting | **H** → **H** | Overlap matrices and lag distributions are aggregates [I] | **No database-benchmark generator found that models this** [I]; closest are record-linkage generators (GeCo) [L] |
| Temporal patterns (trends, seasonality, bursts) | Partition pruning, time-window queries, retention jobs | M → M | Yes | LDBC flashmob/time-correlated events [D]; ydata time-series ACF/PACF [D]; TPC-H date offsets [D] |
| Arrival patterns (batch sizes, late data) | Pipeline correctness under late or out-of-order data; throughput | M → M | Yes (distributions) | No DB-generator support found [I]. TPC-DS has refresh/data-maintenance data [D: spec mentions refresh data] |
| Data volume, table and partition sizes | Plan choice (relpages/reltuples), memory spills, timeouts | E → E (scale) | Yes | TPC SF scaling [D]; pg_restore_relation_stats (but the planner rescales to the physical file size) [D boringSQL]; Hydra dynamic regeneration of arbitrary size [D] |
| What drives plans (selectivities, join cardinalities, histograms, MCVs, NDV, relpages) | Plan reproduction | E (catalog stats) to M (annotated plans) | Catalog stats: yes but contain values. Annotated plans: counts plus predicate constants [I] | PG18/19 stats restore; Oracle DBMS_STATS; SQL Server clone; Hydra/Mirage/DBRepro consume EXPLAIN ANALYZE plans [D] |

### Inferences
- [I] The hierarchy of difficulty is consistent across sources. Per-column marginals (histograms, MCVs, null_frac, NDV, width) are aggregate, cheap and directly injectable. Within-table correlations are medium. Join-crossing correlations, fan-out skew, long-tail combinations, string-format grammars and cross-source entity overlap are hard, and they are where tests on simplified data will fail to predict production plans, bugs and performance.
- [I] For the platform described, cross-source overlap (coverage %, identifier-mapping error rates, per-source lag distributions) can be characterised as aggregates, for example an overlap matrix by entity type or a lag histogram. However, no generator in this catalogue consumes such a description, so it would need a custom generator layer, perhaps one inspired by GeCo or BART.
- [I] "Aggregate" does not mean "non-identifying". MCV lists, histogram bounds and multivariate MCV items are literal data values. On personal-data columns they can disclose real names, IDs or rare combinations. Any export needs per-column suppression, coarsening or a noise policy.

### Gaps
- I found no peer-reviewed source that quantifies the effect of arrival patterns (batch size, lateness) on test predictiveness in a database-generator context.
- The GeCo paper and the Febrl generator docs were unreachable, so the duplicate/corruption claims are leads only.
- I read no source that measures how much a long tail of rare combinations is lost by sampling-based ANALYZE.

## Catalogue of characterisation-driven generators (input, aggregate-only?, maintenance, licence, fit)

### Takeaway
Two families fit an environment where only aggregates can leave:
- **Specification-driven** generators (dbgen, dsdgen, MUDD, PDGF, Myriad, DataSynth, LDBC Datagen) need no real rows, but they reproduce only what a human writes into the spec.
- **Workload-aware / cardinality-constrained** generators (QAGen, MyBenchmark, Arasu's DataSynth, Hydra, PiGen, Touchstone, Mirage, SAM, DBRepro) consume schema, column stats and annotated query plans. This input is aggregate-only, apart from predicate constants and stats values.

Maintained code with permissive licences exists for Mirage (Apache-2.0, pushed 2026-07) and DBRepro (Apache-2.0, 2026-07). Both are PostgreSQL-centred research prototypes. Most older systems are dormant.

### Cited Findings

**Specification-driven (no real rows needed)**
- **TPC-H dbgen** [D]: current TPC-H spec and tools v3.0.1 per the [TPC current-versions page](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp). Uniform, independent values by definition ([spec](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf)). Community mirror `electrum/tpch-dbgen` was last pushed 2023-09-03 with no licence listed in GitHub metadata. Licence of the official TPC tools: not verified [gap]. Fit: performance smoke tests only; it carries no characteristics of the real data [I].
- **TPC-DS dsdgen** [D]: spec v4.0.0, dated November 2024 ([PDF](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-DS_v4.0.0.pdf)), with tools v4.0.0. Empty values are treated as NULLs, and the spec states that dsdgen generates international characters. Community `gregrahn/tpcds-kit` was last pushed 2024-04-16. Its MUDD lineage (Stephens & Poess 2004, "MUDD: a multi-dimensional data generator") is cited in [DBRepro refs](https://arxiv.org/pdf/2608.27822) [L: MUDD full text not read].
- **JCC-H** [D]: a drop-in TPC-H dbgen/qgen replacement that adds join-crossing correlations and skew (`-k` flag), plus "normal" and "skewed" parameter classes ([TPCTC 2017](https://ir.cwi.nl/pub/27429/27429.pdf)). Repo `ldbc/dbgen.JCC-H` was last pushed 2024-04-17, no licence listed. A `hyrise/jcch-dbgen` fork also exists [L]. Fit: stress-tests optimiser and skew handling, not the platform's own data [I].
- **PDGF** [D, slides only]: Java framework with a hierarchical seeding scheme (table → column → row RNG) and "computed references", so every value can be recomputed independently, deterministically and in parallel. It supports non-uniform distributions ([TPCTC 2010 slides](https://www.tpc.org/tpctc/tpctc2010/TPCTC2010-04.pdf)). [L] It was "adopted in TPC benchmarks", with a TPC-H implementation at TPCTC 2011 ([search lead](https://www.tpc.org/tpctc/tpctc2011/slides_and_papers/A_PDGF_Implementation_for_TPC_H.pdf)). **DBSynth**, the PDGF extension that builds a generator from an existing database's metadata and stats (Rabl et al., DBTest 2013), was [U] (connection reset to [dbtest2013 PDF](https://dbtest2013.soe.ucsc.edu/papers/a5-Rabl.pdf)). DBSynth/PDGF are commercialised by bankmark [L/V]. I found no public repo.
- **Myriad** [D]: an XML "data generator prototyping language" for "complex statistical constraints". PRNGs with random access to offsets allow fully parallel generation ([VLDB 2012 demo](https://www.vldb.org/pvldb/vol5/p1890_alexanderalexandrov_vldb2012.pdf); [README](https://raw.githubusercontent.com/TU-Berlin-DIMA/myriad-toolkit/master/README.md)). Licence Apache. `TU-Berlin-DIMA/myriad-toolkit` was last pushed 2014-10-28. The companion `TU-Berlin-DIMA/oligos` ("A database profiler for Myriad Toolkit") was last pushed 2014-10-27 [D metadata; L function]. Dormant.
- **DataSynth (LDBC/DAMA-UPC)** [D README]: property-graph schema in JSON with per-property generators, "correlations between those of the same entity and connected entities", and structure generators, running on Spark 2.0.1 ([README](https://raw.githubusercontent.com/DAMA-UPC/DataSynth/master/README.md); paper [arXiv 1704.00630](https://arxiv.org/abs/1704.00630) [L]). GPL-3.0, last pushed 2017-07-24. Dormant.
- **LDBC SNB Datagen** [D]: Spark generator with Facebook-like degree distributions, DBpedia-based correlated attributes and deterministic output ([spec](https://arxiv.org/pdf/2001.02299)). `ldbc/ldbc_snb_datagen_spark` is Apache-2.0 and was last pushed 2026-10-18, so it is active. It is hard-wired to the social-network schema, so not a fit for arbitrary schemas [I].

**Workload-aware / cardinality-constrained (input: schema + stats + queries/annotated plans; no rows)**
- **QAGen** (SIGMOD 2007) [D via journal version]: the input is the schema, the test query and constraints on its operators. It works by symbolic query processing followed by data instantiation ([Lo, Binnig, Kossmann, Özsu, Hon, VLDB J. 2010](https://cs.uwaterloo.ca/~tozsu/publications/other/Lo-vldbj2009.pdf)). It handles a single query, a limitation addressed by **MyBenchmark** ([Arasu 2011](https://people.iiis.tsinghua.edu.cn/~jianli/paper/mod311arasu.pdf)) [D]. The SIGMOD 2007 PDF at Heidelberg returned 404 [U]. No public code found.
- **DataSynth (Arasu, Kaushik, Li, Microsoft, SIGMOD 2011)** [D]: the input is a set of cardinality constraints. A histogram can be expressed as one constraint per bucket, and annotated query plans are constraints. The use cases include outsourced testing when "an outsourcing organization might not be able to share its internal databases". The problem is intractable in general, and efficient algorithms are given for a large class ([paper](https://people.iiis.tsinghua.edu.cn/~jianli/paper/mod311arasu.pdf)). No public code found. SAM reports the PGM-based approach "takes more than 12 hours to process 13 queries on the Census dataset" ([SAM](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf)) [D].
- **Hydra (IISc, EDBT 2018 + PVLDB 2018 demo)** [D demo paper]:
  - At the client, Hydra "fetches the schema, metadata and the query workload with its corresponding AQPs [annotated query plans]" and ships them. "Privacy concerns can be addressed by passing the information through an appropriate anonymization layer at the client."
  - The AQPs become one linear program per relation. The output is a "minuscule memory-resident database summary" that regenerates data of arbitrary size during query execution, i.e. "dataless databases" (CODD project).
  - Results on the demo workload: ">90% of the volumetric constraints were satisfied with virtually no error", and the rest were within 10 % relative error.
  - Implementation: Java, more than 15K lines of code, on PostgreSQL v9.3. "Deployed in major telecom and software organizations" [V].
  
  Source: [PVLDB 11(12):1974–1977](https://www.vldb.org/pvldb/vol11/p1974-sanghi.pdf). The project page and download (dsl.cds.iisc.ac.in) were [U]: curl failed TLS verification with a self-signed certificate chain, and WebFetch returned 503. Licence and last release are therefore unknown. **HF-Hydra** (DASFAA 2021, better fidelity on unseen queries) is [L]/[U].
- **PiGen (PVLDB 15, 2022)** [D]: extends cardinality constraints to Projection (DISTINCT, UNION, GROUP BY) using projection-subspace LPs. Constraints may come from "Annotated Query Plans" of a client installation ([paper](https://www.vldb.org/pvldb/vol15/p998-sanghi.pdf)). No code located.
- **Sanghi 2025 "Beyond Row Counts"** [D]: adds Duplication Distribution and Presortedness, extracted from query execution ([CEUR Vol-3931](https://ceur-ws.org/Vol-3931/short5.pdf)). This is a workshop paper with no code.
- **Touchstone (USENIX ATC 2018)** [D]:
  - Input: schema H; "data characteristics D", a meta table per column with NULL %, domain, number of unique values, and avg/max varchar length; and "workload characteristics W", parameterised queries with expected output cardinalities.
  - It supports non-equi-joins and runs fully in parallel. "1000× speedup" over the prior state of the art on TPC-H [V, author benchmark].
  
  Source: [paper](https://www.usenix.org/system/files/conference/atc18/atc18-li-yuming.pdf). `daseECNU/Touchstone` is Apache-2.0, last pushed 2020-06-01, so dormant. Follow-ups listed in [DBRepro's references](https://arxiv.org/pdf/2608.27822): **Touchstone+** (DASFAA 2024, "Query Aware Database Generation for Match Operators") and a SIGMOD 2025 companion demo, "A Query-Aware Enormous Database Generator For System Performance Evaluation" [L].
- **Mirage (ICDE 2024, ECNU)** [D README; L paper]: the README describes four steps: query analysis, parameter instantiation, data generation and schema generation. Query analysis executes the original queries to get plans and constraint chains. It supports PostgreSQL 12–15 and requires patching PostgreSQL's `explain.c` to print fractional `actual rows` for index scans ([README](https://raw.githubusercontent.com/dbhammer/mirage/main/README.md)). `DBHammer/Mirage` is Apache-2.0, last pushed 2026-07-28. Paper: ICDE 2024, pp. 3989–4001 ([ECNU record](https://pure.ecnu.edu.cn/en/publications/mirage-generating-enormous-databases-for-complex-workloads/)) [L; full text not read].
- **SAM (SIGMOD 2022)** [D]: input is "a query workload, which contains a set of queries and the corresponding cardinalities". The authors argue that "query workloads have lower security level than the data" [V/author argument]. SAM trains a deep autoregressive model, whose cost is linear in workload size, number of attributes and domain size. It requires FK joins with an acyclic schema ([paper](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf)). Repo `Jamesyang2333/SAM` was last pushed 2022-11-10 under the "NTUItive Dual License" ([README](https://raw.githubusercontent.com/Jamesyang2333/SAM/master/README.md)), so it is dormant and not permissively licensed.
- **DBRepro (arXiv 2608.27822, 28 Aug 2026)** [D]:
  - Input is "non-intrusive metadata only — schema, column-level catalog statistics, target SQL statements, and their physical execution plans" ([README](https://raw.githubusercontent.com/ZhaoyungZhang/DBRepro/main/README.md)).
  - It builds an initial distribution from column stats, extracts constraints from plans and solves join constraints with CP-SAT (OR-Tools). The goal is identical physical plans for slow-query reproduction.
  - Its own baselines on TPC-H (22 queries) report consistent plans for Hydra 3, Touchstone 9 and Mirage 15. These numbers are parsed from garbled PDF table text, so treat them as approximate. DBRepro claims 15 % more consistent plans than the best workload-aware baseline [V, author benchmark].
  - It notes that RSGen and Mirage "require expensive full-table aggregation queries" at extraction.
  - Supports PostgreSQL 12–16 and KingbaseES V8. Apache-2.0, `ZhaoyungZhang/DBRepro` last pushed 2026-07-27, code also on Zenodo ([paper](https://arxiv.org/pdf/2608.27822)).
- **RSGen (Shen & Antova, DBTest 2013, Pivotal)** [L]: "reverses column-level statistics to reproduce the original data distribution" (as described in [DBRepro](https://arxiv.org/pdf/2608.27822) [D for that description]). It works from customer schema, integrity constraints and column statistics. Its own limitation: identical statistics can give the same plan but different runtime ([search extract](https://dbtest2013.soe.ucsc.edu/papers/a7-Shen.pdf); full text [U], connection reset).
- Other metadata-driven work cited in DBRepro: Hu et al., SAP, ICDEW 2019, "Distribution-Driven, Embedded Synthetic Data Generation System and Tool for RDBMS" [L].
- **Adjacent 2025–2026 work**
  - **PBench** ([arXiv 2506.16379, Jun 2025](https://arxiv.org/pdf/2506.16379)) [D abstract]: synthesises *workloads* that match real execution statistics (performance metrics, operator distributions) by selecting and combining queries and databases from existing benchmarks. It does not regenerate the user's data. Repo `WASSER2545/PBench` last pushed 2026-07-27, no licence in metadata.
  - **REMIX** ([arXiv 2611.02373, 2 Nov 2026](https://arxiv.org/pdf/2611.02373)) [D abstract]: language-model relational synthesis that **requires the source database D (real rows)**, so it is a non-fit for aggregate-only export.

### Inferences
- [I] **What would leave the protected environment** for the workload-aware family:
  - DDL
  - catalog statistics (which contain literal MCV and histogram values)
  - the query texts, including predicate constants
  - EXPLAIN ANALYZE plans with per-operator actual row counts
  
  Predicate constants and MCVs are the disclosure risk. Hydra's paper points to an "anonymization layer" but does not specify one.
- [I] Fit to the constraints: DBRepro and Mirage are the most current and permissively licensed, but both are PostgreSQL-specific and patch or depend on PG plan formats. They target plan and volume fidelity for a known query set, not correctness edge cases, dirty formats or cross-source overlap. Spec-driven frameworks (PDGF-like seeding, LDBC-style correlation dimensions) are better for encoding hand-authored characteristics such as overlap rates and lag distributions, but the code bases are dormant or commercial.
- [I] Volumetric similarity on a training workload does not guarantee similarity on unseen queries (the motivation for HF-Hydra; DBRepro's LLM-synthesised unseen-query test). Expect drift when the test workload changes.

### Gaps
- Hydra/HF-Hydra licence, download and last release are unknown (IISc site unreachable).
- The Mirage ICDE paper, the Touchstone+ paper, the 2025 SIGMOD demo, RSGen, DBSynth and MUDD full texts were not read.
- "DataFactory" and "Dataset synthesis via query annotations" from the brief: I found no source under those names. Arasu et al.'s annotated-query-plan constraints and Hydra's AQPs appear to be the relevant concept [I].
- The licence of the official TPC dbgen/dsdgen tools was not verified.

## Query-optimiser statistics as a characterisation (PostgreSQL, Oracle, SQL Server)

### Takeaway
All three engines can move optimiser statistics without data into a test database. PostgreSQL 18 added `pg_dump --statistics-only` with `pg_restore_relation_stats` / `pg_restore_attribute_stats`, and PostgreSQL 19 (released 2026-11-19) adds `pg_restore_extended_stats`. Oracle has DBMS_STATS export/import. SQL Server has DBCC CLONEDATABASE. This lets you test plan choice (EXPLAIN) against production-like statistics. It does not test execution time, memory/spill behaviour, result correctness or data-dependent failures. The statistics also contain literal values (MCVs, histogram bounds), so on personal-data columns they are not automatically safe to export.

### Cited Findings
- [D] pg_stats exposes, per column:
  - null_frac
  - avg_width
  - n_distinct (a positive count, or a negative ratio to the row count when the count is expected to grow with the table)
  - most_common_vals and most_common_freqs
  - histogram_bounds (equal-population buckets, excluding MCVs)
  - correlation (physical vs logical order, which drives index-scan cost)
  - element MCVs and histograms for arrays
  - range histograms
  
  List lengths are controlled by `default_statistics_target` / `ALTER TABLE … SET STATISTICS`. — [PostgreSQL 19 docs, pg_stats](https://www.postgresql.org/docs/current/view-pg-stats.html)
- [D] Extended statistics (CREATE STATISTICS) cover functional dependencies, multivariate n-distinct and multivariate MCV lists. They are computed from the same ANALYZE sample. Functional dependencies apply only to simple equality and IN with constants. They are not used for join selectivity. — [planner-stats](https://www.postgresql.org/docs/current/planner-stats.html); [CREATE STATISTICS](https://www.postgresql.org/docs/current/sql-createstatistics.html)
- [D] Stats manipulation functions:
  - `pg_restore_relation_stats`: relpages, reltuples, relallvisible, relallfrozen
  - `pg_restore_attribute_stats`: any pg_stats field
  - `pg_restore_extended_stats` and the `pg_clear_*` functions
  
  A `version` argument helps port statistics across server versions. Callers need the MAINTAIN privilege. Warning from the docs: changes "are likely to be overwritten by autovacuum … and should be considered temporary". — [PostgreSQL 19 docs, §9.28 admin functions](https://www.postgresql.org/docs/current/functions-admin.html)
- [D] `pg_dump --statistics` / `--statistics-only` dumps optimizer statistics for tables, materialized views, foreign tables and indexes. It excludes "custom statistics added by an extension" and cumulative statistics. — [pg_dump docs (19)](https://www.postgresql.org/docs/current/app-pgdump.html)
- [D] Practitioner demonstration ([boringSQL, "Production query plans without production data", 2026-03-08](https://boringsql.com/posts/portable-stats/)):
  - Injecting relation stats alone did not flip the plan. Injecting histogram bounds and correlation flipped a seq scan to an index scan, and an injected MCV list produced different plans for rare and common status values.
  - The planner scales reltuples to the actual physical file size, so absolute row estimates shrink in a tiny test DB while the ratios stay correct.
  - It recommends disabling autovacuum analyze on injected tables.
  - In PG 18, extended stats were not covered; PG 19 closes this.
  - "Statistics dumps are tiny … under 1MB" [V/author].
  - It mentions a `pg_regresql` extension that makes the planner trust injected relpages [L, not verified].
- [L] Known issues found only in search results: BUG #19845 (Nov 2026) reports that extended-stat restore may attach stats to the wrong columns when attribute numbers change, and BUG #19814 reports that pg_restore_attribute_stats validation accepts MCVs without an equality operator. Fixes were backpatched to 18 (incl. CVE-2026-16238 for multirange). — [pgsql-bugs #19845](https://www.postgresql.org/message-id/19845-a2a2ac0ba28b3605%40postgresql.org)
- [D] **pg_dbms_stats** (NTT OSS Center) stores and "freezes" statistics so that the planner uses saved rather than live stats. It supports heap tables, materialized views, foreign tables and indexes ([README](https://raw.githubusercontent.com/ossc-db/pg_dbms_stats/master/README.md); [EN manual](https://raw.githubusercontent.com/ossc-db/pg_dbms_stats/master/doc/pg_dbms_stats-en.md)). Copyright 2012–2022, last pushed 2024-01-12, so low activity. Its purpose is plan stability; moving stats to other servers is possible via its export scripts [D: export_<type>_stats-<PG version>.sql.sample].
- [D] **Oracle**: transporting statistics is "especially useful for testing an application using production statistics". The workflow is DBMS_STATS.CREATE_STAT_TABLE, then EXPORT_SCHEMA_STATS (or DATABASE, DICTIONARY, FIXED_OBJECT variants), a file transfer, and IMPORT_SCHEMA_STATS. — [Oracle 19c SQL Tuning Guide ch. 17](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/transporting-optimizer-statistics.html) (the 23ai URL I tried returned 404)
- [D] **SQL Server DBCC CLONEDATABASE** "generates a schema-only, read-only copy of a database … to investigate performance issues related to the query optimizer". It copies statistics for all indexes and, optionally, Query Store (NO_STATISTICS and NO_QUERYSTORE are opt-outs). Since SQL Server 2019 it captures columnstore stats blobs automatically. The clone is "only intended for troubleshooting and diagnostic purposes", and "any other use … isn't supported". Requires sysadmin. — [Microsoft Learn](https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql). The linked "Understanding data security in cloned databases" page returned 404 [U].
- [D] DBRepro observes that pg_stats are sample-based and lack exact NDV and min/max. Plan-reproduction generators therefore also consume EXPLAIN ANALYZE plans ([arXiv 2608.27822](https://arxiv.org/pdf/2608.27822)).
- [L] RSGen's authors note that identical statistics may yield the same plan but different runtime ([DBTest 2013 extract](https://dbtest2013.soe.ucsc.edu/papers/a7-Shen.pdf)).

### Inferences
- [I] What stats-only cloning **lets you test**:
  - EXPLAIN plan shape, join order, scan choice and estimated rows/costs under production statistics
  - plan regressions in CI (e.g. RegreSQL-style; `dimitri/regresql` was last pushed 2026-05-23)
  - index and partitioning design reviews
- [I] What it **does not** let you test:
  - EXPLAIN ANALYZE actuals and execution time
  - memory, spill and parallelism behaviour, which depend on the real tuples
  - result correctness
  - constraint and format failures
  - data-dependent bugs
  - anything after autovacuum or writes overwrite the injected stats
  
  Fidelity is also capped by what the stats model: no join-crossing correlation in any of the three engines' single-table stats.
- [I] A combined approach is natural: inject production stats for plan tests, and use a generator seeded from the same stats (RSGen/DBRepro-style) for execution tests.
- [I] Confidentiality: MCVs, histogram bounds and Oracle/SQL Server histograms store real values. A stats dump of a name, email or ID column exports real personal data, so per-column redaction is required before stats leave the protected environment. This also applies to the CLONEDATABASE output and the Query Store contents (query texts with literals).

### Gaps
- I did not read the Microsoft page on data security in clone databases (404), nor Oracle 23ai/26ai changes.
- No PG 19 release-notes text was read. The PG 19 status comes from the docs banner ("November 19, 2026: PostgreSQL 19 Released!") and the presence of `pg_restore_extended_stats` in the v19 docs.

## Statistical data-profiling tools as a characterisation (brief)

### Takeaway
Profilers produce single-table characterisations (marginals, completeness, distinct counts, correlations, duplicates, time-series features) in exportable JSON/protobuf form. These could seed spec-driven or stats-driven generators. They do not capture join fan-out, cross-table correlation or plan-relevant cardinalities, and no profiler-to-database-generator bridge is maintained except historic research (Myriad's Oligos).

### Cited Findings
- [D] Deequ's column profiler reports completeness, approximate distinct count and inferred data type per column ([profiling example](https://raw.githubusercontent.com/awslabs/deequ/master/src/main/scala/com/amazon/deequ/examples/data_profiling_example.md)). `awslabs/deequ` is Apache-2.0, last pushed 2026-10-20. pydeequ 1.7.0 was released 2026-09-14 ([PyPI](https://pypi.org/project/pydeequ/)).
- [D] TFDV computes descriptive statistics, infers a schema and detects anomalies. Its statistics are a `DatasetFeatureStatisticsList` protobuf ([TFDV get started](https://www.tensorflow.org/tfx/data_validation/get_started)). Version 1.21.0 was released 2026-06-11 ([PyPI](https://pypi.org/project/tensorflow-data-validation/)).
- [D] ydata-profiling reports:
  - an overview (records, missingness, duplicates)
  - alerts (high correlation, skewness, uniformity, zeros, missing values)
  - multivariate correlations, missing-data analysis and duplicate rows
  - time-series ACF/PACF and seasonality
  
  Output is exportable as JSON, and there is a "sensitive data" mode ([README](https://raw.githubusercontent.com/Data-Centric-AI-Community/ydata-profiling/develop/README.md)). Version 4.18.4 was released 2026-04-22 ([PyPI](https://pypi.org/project/ydata-profiling/)). Observation: the develop-branch README now refers to the package as `fg-data-profiling` [D, observed; implications not investigated].
- [D] great-expectations 1.25.0 was released 2026-11-12 under Apache-2.0. Its PyPI source URL now points to `github.com/fivetran/great_expectations` ([PyPI](https://pypi.org/project/great-expectations/)). I did not read its profiler docs [gap].
- [D metadata] `TU-Berlin-DIMA/oligos`, "A database profiler for Myriad Toolkit", was last pushed 2014-10-27. It was a research bridge from profile to generator spec.

### Inferences
- [I] Profiler JSON maps naturally onto three inputs: Touchstone's per-column "data characteristics" meta table (NULL %, domain, NDV, string lengths), `pg_restore_attribute_stats` arguments, or a PDGF/Myriad-style spec. All three are aggregate exports, but sample rows and value lists in profiler reports need the same redaction as MCVs.
- [I] Profilers are single-dataset tools. Join-degree distributions, cross-source overlap and arrival lags must be computed with custom aggregate queries inside the protected environment.

### Gaps
- I did not verify which profilers emit raw sample rows by default (e.g. ydata "sample" sections), or the details of their sensitive-data modes. That is another researcher's validation scope.
