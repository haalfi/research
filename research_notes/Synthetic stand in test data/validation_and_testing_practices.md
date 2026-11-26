# Validation as a foundation for generation, and software-testing practices for a data platform

Scope: (a) can one specification of "what is normal" both validate real data and generate test data, given that normal in production is not always correct; (b) which software-testing practices (oracles carried by generated data, property-based, metamorphic, differential testing, format fuzzing, dirty-data generators) apply to testing a multi-source ingestion platform whose real data stays in a protected environment.

Evidence labels used throughout: **[documented]** = full text / source file read by me; **[inferred]** = my reasoning from documented facts; **[vendor]** = vendor's own description of its product; **[lead]** = search-result extract only, full text not read; **[unreachable]** = tried and could not read.
Retrieval date for all sources: 2026-11-26. Release dates are PyPI upload times of the latest version (PyPI JSON API, `https://pypi.org/pypi/<pkg>/json`); "last commit" dates are the HEAD commit of the default branch from a shallow `git clone` on that date.

## 1. Shared foundation: tools where one schema/contract both validates and generates

### Takeaway
In mature OSS, one spec doing both jobs is real but narrow. Pandera (DataFrame schemas → Hypothesis strategies), JSON Schema (validators + hypothesis-jsonschema), Pydantic/dataclass models (validation + polyfactory), and ODCS contracts via datacontract-cli (test + export to a Data Caterer generation task, or to JSON Schema/Pydantic) are the workable routes. All of them generate *type- and constraint-valid* data, not *realistic* data. Cross-row, cross-table and cross-source rules (joins, overlap between sources, delays) are mostly not carried into generation. Great Expectations, Soda, Deequ, TFDV, Frictionless, dbt and SQLMesh validate or test, but have no first-party generator from their rule sets. Two exceptions: TFDV's paper describes schema-driven synthetic inputs, and SQLMesh's `create_test` builds fixtures by querying real tables. No tool needs real rows to generate from a hand-written spec. Profile-inferred specs (Deequ, TFDV, Frictionless `describe`, `datacontract import`) do need real rows, but only the inferred spec (metadata) would have to leave the protected environment.

### Cited Findings
**Pandera (schema → Hypothesis strategy)**
- [documented] Pandera "provides a utility for generating synthetic data purely from pandera schema or schema component objects"; schema metadata is turned into a Hypothesis strategy; `schema.example(size=n)` for interactive use, `schema.strategy(size=n)` for `@hypothesis.given` tests; works for the class-based `DataFrameModel` too; requires `pip install 'pandera[strategies]'`. Feature "new in 0.6.0". — [Pandera docs: Data Synthesis Strategies (source file)](https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/data_synthesis_strategies.md)
- [documented] Pandera's own caveat: generated data "will not be exactly the same as the data in the original dataset, and in many cases will not qualitatively look like the original data, however it will be valid according to the schema". The stated purpose is "to help you test your schema and data validation logic". For realistic data it points to Faker, Mimesis and SDV. — same source
- [documented] Built-in checks (`gt`, `lt`, `isin`, `notin`, `eq`, `ne`, `in_range`, `str_*`) are merged into one constraint set and generated "in one shot". Unsatisfiable combinations raise `SchemaDefinitionError` at strategy-construction time. Custom lambda checks fall back to filtering generated data, which "can be highly inefficient" and "most likely raise an `Unsatisfiable` exception" unless you register a strategy or a "constraint adapter" (`FieldConstraints`: numeric bounds, membership, regex, string lengths). — same source
- [documented] Maintenance: pandera 0.36.0 released 2026-11-10; first PyPI release 2018-11-05. — [PyPI pandera](https://pypi.org/pypi/pandera/json)
- [inferred] Pandera dataframe-level / multi-column custom checks (e.g. "sum of parts = total", foreign-key-like relations) have no automatic strategy, so they fall into the slow filter path. The doc's constraint adapter covers only per-field constraints.

**JSON Schema + hypothesis-jsonschema**
- [documented] `hypothesis_jsonschema.from_schema(schema)` "takes a JSON schema and returns a strategy for allowed JSON objects". Standard formats work; custom formats are ignored unless you pass `custom_formats`. "JSONSchema drafts 04, 05, and 07 are fully tested and working." — [hypothesis-jsonschema README](https://raw.githubusercontent.com/python-jsonschema/hypothesis-jsonschema/master/README.md)
- [documented] Maintenance: 0.23.2 released 2026-10-27 (first release 2018-11-21); last commit 2026-10-27. — [PyPI](https://pypi.org/pypi/hypothesis-jsonschema/json)

**Pydantic / dataclasses + polyfactory**
- [documented] Polyfactory generates mock data "based on type hints and supporting dataclasses, typed-dicts, pydantic models, msgspec structs and more"; MIT licence; successor of pydantic-factories. — [polyfactory README](https://raw.githubusercontent.com/litestar-org/polyfactory/main/README.md)
- [documented] polyfactory 3.5.0 released 2026-10-21; pydantic 2.14.4 released 2026-11-19. — [PyPI polyfactory](https://pypi.org/pypi/polyfactory/json), [PyPI pydantic](https://pypi.org/pypi/pydantic/json)

**ODCS + datacontract-cli (+ Data Caterer)**
- [documented] ODCS current version v3.2.0, Apache-2.0. Properties carry `logicalTypeOptions` (pattern, minimum, maximum, …), an `examples` field ("List of sample element values"), and a `quality` section with `text`, `library` metrics (`nullValues`, `missingValues`, `invalidValues`, `duplicateValues`, `rowCount`), `sql` and `custom` (vendor-specific: Soda, GX, dbt …) rules. — [ODCS README](https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/main/README.md), [ODCS schema.md](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/schema.md), [ODCS data-quality.md](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/data-quality.md)
- [inferred] I found no test-data generation section in the ODCS spec pages I checked (README, schema, data-quality). ODCS is a validation/description standard; generation comes only from tools that read it.
- [documented] datacontract-cli "natively supports" ODCS. It lints, runs schema and quality tests against data sources (`datacontract test`), imports contracts from existing tables/DDL/Avro/JSON Schema etc., and exports to many formats. — [datacontract-cli README](https://raw.githubusercontent.com/datacontract/datacontract-cli/main/README.md)
- [documented] Exporters in the code base include `data_caterer`, `jsonschema`, `pydantic`, `great_expectations`, `sodacl`, `dbt`, `dqx`, `avro`, `protobuf`, `sql`, `spark`, `polars`, `iceberg`, `xsd` and others. — [datacontract-cli `datacontract/export/` directory](https://github.com/datacontract/datacontract-cli/tree/main/datacontract/export) (cloned; last commit 2026-11-24)
- [documented] `datacontract export data-caterer` "Converts the data contract to a data-generation task in YAML that can be ingested by Data Caterer … This lets you generate production-like data in any environment based on your contract." — [datacontract-cli docs: Export Data Caterer](https://github.com/datacontract/datacontract-cli/blob/main/docs/docs/exports/data-caterer.md). The phrase "production-like" is the project's own claim [vendor].
- [documented] The Data Caterer exporter maps the type (physical, else logical), `isUnique`/`isPrimaryKey`, enum values → `oneOf`, `pattern` → `regex`, and `minimum`/`maximum` → `min`/`max`. — [data_caterer_exporter.py](https://github.com/datacontract/datacontract-cli/blob/main/datacontract/export/data_caterer_exporter.py)
- [inferred] From that code read, ODCS `quality` rules (SQL, library metrics) are not translated into generation constraints. Only column-level type, enum, pattern, range and uniqueness carry over.
- [documented] The Pydantic export turns `logicalTypeOptions` into `pydantic.Field` constraints, "so the generated model rejects what `datacontract test` would flag". — [datacontract-cli docs: pydantic-model export](https://github.com/datacontract/datacontract-cli/blob/main/docs/docs/exports/pydantic-model.md)
- [inferred] So one ODCS file can yield (i) `datacontract test` against real data inside the protected environment, (ii) a JSON Schema → hypothesis-jsonschema strategy, (iii) a Pydantic model → polyfactory/Hypothesis generator, and (iv) a Data Caterer task, all outside. That is the closest thing to a shared OSS foundation, but the generator sees only what each exporter maps.
- [documented] datacontract-cli 1.2.11 released 2026-11-17 (first release 2024-01-27). — [PyPI](https://pypi.org/pypi/datacontract-cli/json)
- [documented] Data Caterer: "A test data management tool with automated data generation, validation and clean up". It generates data for databases, files, messaging and HTTP via UI, Scala/Java SDK or YAML, "executed via Spark". It maintains relationships across datasets (foreign keys, including across data sources), suggests validations, does metadata discovery, and runs as a GitHub Action. Repo LICENSE is Apache 2.0; last commit 2026-02-14. — [data-caterer README](https://github.com/data-catering/data-caterer/blob/main/README.md), [foreign-key docs](https://github.com/data-catering/data-caterer/blob/main/docs/docs/generator/foreign-key.md)
- [documented] Data Caterer can take validations from external sources "so you can generate data for your upstream data sources and validate your pipelines based on the same rules that would be applied in production". Supported: OpenMetadata and Great Expectations. Not supported: dbt constraints, SodaCL, Monte Carlo. Metadata guides also exist for ODCS and datacontract-cli. — [external-source-validation.md](https://github.com/data-catering/data-caterer/blob/main/docs/docs/validation/external-source-validation.md)
- [documented] Data Caterer generator options include `enableEdgeCase`/`edgeCaseProbability` (e.g. Int.MaxValue, Int.MinValue, 0; strings such as "", "\n", "\u0000" and non-Latin scripts) and `enableNull`/`nullProbability`. — [data-generator.md](https://github.com/data-catering/data-caterer/blob/main/docs/docs/generator/data-generator.md)

**Validation-only tools (no first-party generator found)**
- [documented] Great Expectations README describes Expectations as "unit tests for your data" plus auto-generated documentation. No generation feature is described. great-expectations 1.25.0 released 2026-11-12. — [GX README](https://raw.githubusercontent.com/great-expectations/great_expectations/develop/README.md), [PyPI](https://pypi.org/pypi/great-expectations/json). The generation side comes from third parties such as Data Caterer (above).
- [documented] Soda Core 4.x is a "data quality and data contract verification engine"; its CLI/API can "generate, test, publish, and verify contracts" (generate = contracts, not data). soda-core 4.32.0 released 2026-11-25. — [soda-core README](https://raw.githubusercontent.com/sodadata/soda-core/main/README.md), [PyPI](https://pypi.org/pypi/soda-core/json)
- [documented] Frictionless: "describe, extract, validate, and transform", where describe = "infer, edit and save metadata" (Table Schema). No generation. frictionless 5.21.0 released 2026-10-15. — [frictionless-py README](https://raw.githubusercontent.com/frictionlessdata/frictionless-py/main/README.md), [PyPI](https://pypi.org/pypi/frictionless/json)
- [documented] Deequ: declarative "unit tests for data", data profiling, anomaly detection on metric time series, and "Automatic suggestion of constraints for large datasets". The paper says ML is used "for enhancing constraint suggestions". — [deequ README](https://github.com/awslabs/deequ/blob/master/README.md) (last commit 2026-09-16); [Schelter et al., "Automating Large-Scale Data Quality Verification", PVLDB 11(12) 2018](https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf). pydeequ 1.7.0 released 2026-09-14.
- [documented] TFDV paper (Breck et al., MLSys 2019): "the schema can be inferred from and co-evolve with the data" and "human operators … encode their domain knowledge about the data as part of the schema". Initial inference uses "a set of reasonable heuristics", after which the validator recommends schema updates. It also uses the schema to generate data: "We base our approach on fuzz testing … using the schema to guide the generation of synthetic inputs", which drive a few training iterations to expose code assumptions that disagree with the schema (example: a log transform failing on synthetic non-positive values). — [Breck et al., Data Validation for Machine Learning, MLSys 2019](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)
- [documented] tensorflow-data-validation 1.21.0 released 2026-06-11; last commit 2026-08-14. — [PyPI](https://pypi.org/pypi/tensorflow-data-validation/json). I could not fetch TFDV's get_started guide (404 at the raw path) [unreachable], so whether the schema-driven synthetic-input generator is exposed in the OSS package is not verified.
- [documented] dbt unit tests use static mock inputs (`given`) and `expect` outputs, as inline `dict`, `csv` or `sql`, or fixture files under `tests/fixtures/`. dbt Labs "strongly recommends only running unit tests in development or CI environments". `compute: local` runs them on DuckDB, but only for Snowflake/BigQuery, only if the SQL translates, and only if upstream relations exist so dbt can fetch their schemas. dbt-core 1.12.7 released 2026-11-12. — [dbt docs: unit-tests.md (source)](https://github.com/dbt-labs/docs.getdbt.com/blob/current/website/docs/docs/build/unit-tests.md), [PyPI](https://pypi.org/pypi/dbt-core/json)
- [documented] SQLMesh unit tests give input rows for upstream models and expected outputs (input may also come from a SQL query). `sqlmesh create_test` "can generate a complete test for a given model, as long as the tables of its upstream models exist in the project's data warehouse and are already populated with data": it runs a user query (e.g. `SELECT … LIMIT 3`) against the warehouse and computes the expected output. sqlmesh 0.236.4 released 2026-10-22. — [SQLMesh docs: tests.md](https://github.com/TobikoData/sqlmesh/blob/main/docs/concepts/tests.md), [PyPI](https://pypi.org/pypi/sqlmesh/json)

**Realistic-value generators (complements, not spec-driven validators)**
- [documented] Latest releases: Faker 40.63.0 (2026-11-20), Mimesis 22.2.0 (2026-09-23), SDV 2.2.0 (2026-11-06), dbldatagen 0.4.0.post1 (2024-07-26). — PyPI JSON for [faker](https://pypi.org/pypi/faker/json), [mimesis](https://pypi.org/pypi/mimesis/json), [sdv](https://pypi.org/pypi/sdv/json), [dbldatagen](https://pypi.org/pypi/dbldatagen/json)

### Inferences
- What has to leave the protected environment for each route:
  - Hand-written specs (Pandera, JSON Schema, Pydantic, ODCS): nothing; they already live in the repo.
  - Spec inferred from data (Deequ suggestions, TFDV `infer_schema`, Frictionless `describe`, `datacontract import` from a table): the spec, which is metadata. Enum domains, regexes, min/max and example values can themselves leak confidential values or licensed reference-data code lists, so they need review before export. ODCS `examples` is an obvious leak vector.
  - SQLMesh `create_test` copies real rows into test fixtures, so it does not fit the constraint unless run on already-synthetic data.
- Fit: the most practical shared foundation is ODCS (or Pandera) as the single source, with:
  - validation run inside the protected environment;
  - Hypothesis/polyfactory/Data Caterer generation outside;
  - a hand-maintained layer for what no exporter carries: cross-source entity overlap, identifier mappings, delivery delays, and multi-row rules.
- Pandera and hypothesis-jsonschema are best for property-based tests: small, shrinkable, adversarial within the spec. Data Caterer is best for volume and multi-table referential integrity. They complement each other.

### Gaps
- I did not verify whether Pydantic v2 still ships a Hypothesis plugin; grepping the Pydantic migration guide for "hypothesis" found nothing. Polyfactory is the documented route.
- I did not verify whether GX 1.x removed or kept profilers / Data Assistants (descriptive suite generation).
- Data Caterer's commercial tiers and feature gating are not verified. The repo is Apache-2.0, but data.catering may have paid features. Treat capability claims as [vendor] until checked.
- I found no OSS tool that generates multi-source overlapping entities with per-source identifiers and delays from a contract. This would have to be built.

## 2. "Normal ≠ correct": descriptive profile vs prescriptive rules, and generating invalid data on purpose

### Takeaway
The literature and tools support keeping two artefacts. One is a *descriptive* profile inferred from production: what the data looks like, including known defects. The other is a *prescriptive* spec curated by humans: what should be true. TFDV makes this co-evolution explicit, and Deequ/TFDV suggestions are descriptive starting points to be reviewed. Generating rule-violating data on purpose is well established: Schemathesis negative mode mutates the schema, BART injects constraint-violating errors with controlled detectability, Jenga corrupts data to stress-test a TFDV schema, and Data Caterer has edge-case and null injection. A generator should therefore take the prescriptive spec plus an explicit "known-defects" mutation layer drawn from the descriptive profile. It should not treat the production profile as the definition of valid.

### Cited Findings
- [documented] TFDV: the schema is "reverse-engineered and has to co-evolve with the data". Discrepancies between schema and code mean "either the schema needs to change (to codify the new expectations) or the training code needs to change to be compliant with the actual shape of the data". — [Breck et al. 2019](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)
- [documented] Jenga's TFDV case: the automatically inferred schema "is too strict however, as it does not account for the fact that all the values in the review_date column will change for future data", so the authors adjusted it by hand. They then ran `SchemaStresstest` with 250 randomly generated corruptions to check whether the schema catches corruptions that hurt model performance. — [Schelter, Rukat, Biessmann, "JENGA – A Framework to Study the Impact of Data Errors on the Predictions of ML Models", EDBT 2021](https://ssc.io/pdf/jenga.pdf)
- [documented] Schemathesis generation modes: `all` (default, valid and invalid), `positive`, `negative`. Negative testing "generates data that should be rejected … because it is deliberately invalid according to your schema. Schemathesis mutates your schema to produce it" (example: for `{"type":"string","minLength":3}` → `42, [], "", "ab"`). All phases are built on Hypothesis plus schema strategy engines. schemathesis 4.34.2 released 2026-11-24. — [Schemathesis docs: data-generation.md](https://github.com/schemathesis/schemathesis/blob/master/docs/explanations/data-generation.md), [PyPI](https://pypi.org/pypi/schemathesis/json)
- [documented] BART injects errors into a clean database under denial constraints (which express FDs, CFDs and fixing rules). Users choose "the percentage of errors, whether they want a guarantee that errors are detectable using the given constraints", and get an estimate of "repairability". The paper notes "a duality between the problem of injecting detectable errors in clean data, and the problem of detecting violations to database constraints in dirty data". — [Arocena et al., "Messing Up with BART: Error Generation for Evaluating Data-Cleaning Algorithms", PVLDB 9(2) 2015](https://www.vldb.org/pvldb/vol9/p36-arocena.pdf)
- [documented] Data Caterer edge-case and null injection by probability (see Q1). — [data-generator.md](https://github.com/data-catering/data-caterer/blob/main/docs/docs/generator/data-generator.md)
- [documented] Deequ suggestions are derived from profiling the data, i.e. descriptive. — [Schelter et al. 2018](https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf)

### Inferences
- Proposed layering, built from the documented patterns:
  1. **Prescriptive contract** (ODCS/Pandera): hand-curated, reviewed, used for both validation and positive generation.
  2. **Descriptive profile**: inferred inside the protected environment. Only aggregate and shape statistics are exported (distributions, null rates, cardinalities, known-defect frequencies such as "3% of source X postcodes are blank"). It drives realism weights, never validity.
  3. **Defect catalogue**: named mutations (blank-instead-of-null, swapped day/month, duplicate delivery, stale identifier, encoding damage). Each is tagged with the expected platform response: accept, repair, quarantine or reject. This is what gives generated defective rows an oracle (see Q3).
- Negative generation from constraints can be done per rule by negating one constraint at a time. That is the Schemathesis approach, applied to tables via a Pandera/ODCS wrapper. I found no OSS tool that does this for DataFrame/table contracts directly (see Gaps).

### Gaps
- I found no OSS DataFrame/table tool with a built-in "negative mode" (generate rows violating exactly one contract rule). Pandera has no documented invalid-data generation in the page I read.
- I found no paper that formally separates "descriptive profile" from "prescriptive contract" for data-platform testing. The separation above is synthesis [inferred].

## 3. Expected outcomes carried by data (oracles by construction) and mutation-based data testing

### Takeaway
"Oracle by construction" is standard in three places:
- error-generation benchmarks (BART, REIN and Raha keep the clean ground truth next to the dirty data);
- entity-resolution generators (GeCo/Gecko keep the true entity of each duplicate);
- TPC benchmarks (a qualification database at SF=1 with a fixed answer set the query output must match).

DBMS testers also build oracles into generated inputs: PQS picks a pivot row the query must return, and DQE adds row-identity columns. For a multi-source platform, the generator should first create a hidden "true world" (entities, attributes, events), then render each source's view of it (own identifiers, coverage, delays, defects). The true world becomes the oracle for matching, deduplication, rejection and aggregate results.

### Cited Findings
- [documented] REIN: an error-injection module generates errors of various types and rates "in an offline phase before running the experiments". It uses BART with denial constraints for "rule violation, outliers, nulls, duplicates, and mislabels", plus an "error generator" library for realistic errors (keyboard typos, implicit missing values). Ground truth Φg is kept alongside dirty Φ− and repaired Φ+. — [Abdelaal, Hammacher, Schöning, "REIN: A Comprehensive Benchmark Framework for Data Cleaning Methods in ML Pipelines", arXiv 2302.04702 (EDBT 2023)](https://arxiv.org/abs/2302.04702)
- [documented] Raha/Baran benchmarking requires "a dirty dataset and its corresponding clean dataset" (`raha/benchmark.py`). The repo was last committed 2025-06-05. — [raha README](https://github.com/BigDaMa/raha/blob/master/README.md)
- [documented] BART last commit 2023-05-10. The README states PostgreSQL 11 is the last supported version (PG ≥12 removed OID support); H2 is also supported. Its options include `checkChanges` ("check, at the end of the process, if changes are detectable"). — [BART README](https://github.com/dbunibas/BART/blob/master/README.md)
- [lead] GeCo (Christen & Vatsalan, CIKM 2013; online demo by Tran, Vatsalan, Christen) generates and corrupts personal data with known entity structure for record-linkage evaluation. The search extract also says that in R package `bstrl` GeCo-derived data, an ID column gives "the entity number of which this record is a copy". — [GeCo paper PDF](https://users.cecs.anu.edu.au/~christen/publications/christen2013cikm.pdf) (download failed to convert, [unreachable] in full text), [ANU GeCo page](https://dmm.anu.edu.au/geco), [bstrl docs](https://search.r-project.org/CRAN/refmans/bstrl/html/geco_30over_3err.html)
- [documented] Gecko (`gecko-syndata`) is a "spiritual successor to the GeCo framework" for "bulk generation and mutation of realistic personal data" with NumPy/Pandas. Its description says it is "still very much in a 'beta' state". MIT licence; 0.6.4 released 2024-12-06. — [PyPI gecko-syndata](https://pypi.org/pypi/gecko-syndata/json)
- [documented] recordlinkage (Python) 0.16 released 2023-07-20, last commit 2023-07-20 (stale). splink 5.0.0 released 2026-09-28. — PyPI [recordlinkage](https://pypi.org/pypi/recordlinkage/json), [splink](https://pypi.org/pypi/splink/json)
- [documented] TPC-H v3.0.1 (©1993–2022), clause 2.3.1: query validation runs against "a qualification database … built in a manner substantially the same as the test database", unmodified by refresh functions, with default substitution parameters, and "the resulting output must match the output data specified for the query validation (see Appendix C)" within the tolerances of Clause 2.1.3.5. The qualification database "must be exactly equal to a scale factor, SF, of 1". — [TPC-H Standard Specification Revision 3.0.1](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf)
- [documented] PQS "randomly selects a row, called a pivot row, for which a query is generated that is guaranteed to fetch the row. If the row is not contained in the result set, a bug has been detected". It found 121 unique bugs in SQLite, MySQL and PostgreSQL (96 fixed or verified). SQLancer now lists PQS as "currently unmaintained" because of its implementation effort. — [Rigger & Su, OSDI 2020](https://www.usenix.org/system/files/osdi20-rigger.pdf), [SQLancer README](https://github.com/sqlancer/sqlancer/blob/main/README.md)
- [documented] DQE appends "two extra columns to each table … to uniquely identify each row and track whether a row has been modified", then checks SELECT/UPDATE/DELETE with the same predicate for consistency (MySQL). — [SQLancer README, DQE row (ICSE 2023)](https://github.com/sqlancer/sqlancer/blob/main/README.md)
- [documented] Jenga corruptions (missing values MCAR/MAR/MNAR, outliers, typos, noisy measurements, broken encodings) are randomly applied and evaluated repeatedly. It is research code: jenga 0.0.1a1 released 2021-11-26, last commit 2022-10-31. — [jenga README](https://github.com/schelterlabs/jenga/blob/master/README.md), [PyPI](https://pypi.org/pypi/jenga/json)

### Inferences
- **Oracle by construction for the platform:**
  - Generate a ground-truth entity table.
  - Derive per-source deliveries with a mapping table (true_entity_id → source_id), coverage masks, delay offsets and injected defects. Each row is tagged with `expected_outcome` (load / repair to value v / quarantine reason r / reject reason r).
  - Expected results:
    - matching/linkage: precision and recall against the true links;
    - rejection paths: exact row sets;
    - aggregates: computed on the true world, then compared with platform output.
- **DQE-style tracer columns**: hidden row-identity or lineage columns in generated deliveries let a test check per-row fate through the pipeline. Strip them before format-level tests if they would change the schema under test.
- **Mutation testing of validation rules**: inject each catalogued defect into otherwise valid data and assert that the specific rule fires. This is BART's detectability guarantee and Jenga's schema stress test, applied to contracts. It measures the "mutation score" of the contract.
- **Protected-environment angle**: the platform team could compute the same aggregates on real data inside the protected environment and export only those aggregates. That gives a realism check of the generator, not a correctness oracle.

### Gaps
- No full text read for GeCo; ground-truth handling is from search extracts and the bstrl doc snippet only.
- I did not find an OSS generator for multi-source entity data with per-source identifiers and *delivery delays* (temporal coverage). Febrl's `dsgen` README was not reachable at the path tried [unreachable].
- I did not read the original "error generator" library that REIN cites.

## 4. Property-based testing (PBT) for data pipelines

### Takeaway
Hypothesis is the mature core: actively released, with pandas strategies, stateful rule-based testing, a failure database, and `@example` pinning. Pandera, Polars, hypothesis-jsonschema and Schemathesis all build on it. On Spark/Scala, spark-testing-base is maintained, while sscheck, the temporal-logic ScalaCheck work, is dormant since 2018. I found no primary source on PBT of ETL invariants (idempotent re-delivery, order independence, count conservation). The invariants below are proposals derived from documented mechanisms.

### Cited Findings
- [documented] Hypothesis 6.170.17 released 2026-11-20 (first release 2013). — [PyPI](https://pypi.org/pypi/hypothesis/json)
- [documented] Failure database: "When a test fails, Hypothesis automatically saves the failure so it can be replayed later", by default in a `DirectoryBasedExampleDatabase` under `.hypothesis`. Saved failures are retried before new generation. `@example` adds fixed inputs run every time ("combining unit-testing with property-based testing"). — [Hypothesis docs: replaying-failures.rst](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/docs/tutorial/replaying-failures.rst) (path in current repo: `hypothesis/docs/tutorial/replaying-failures.rst`)
- [documented] Stateful testing: Hypothesis "tries to generate not just data but entire tests". `RuleBasedStateMachine` rules take strategies or `Bundle`s, which are named collections of generated values that later rules can draw from or `consumes`. The docs' example compares a real `DirectoryBasedExampleDatabase` against a simplified in-memory model. — [Hypothesis docs: stateful.rst](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/docs/stateful.rst)
- [documented] `hypothesis.extra.pandas` is in the strategies reference (data_frames, columns, etc.). — [strategies.rst](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/docs/reference/strategies.rst)
- [documented] `polars.testing.parametric` exports Hypothesis strategies `dataframes`, `series`, `column`, `dtypes`, `lists`, plus `load_profile`/`set_profile`. It requires hypothesis. polars 2.2.0 released 2026-11-24. — [polars/testing/parametric/__init__.py](https://github.com/pola-rs/polars/blob/main/py-polars/src/polars/testing/parametric/__init__.py)
- [documented] spark-testing-base last commit 2026-10-30. Its README says parts are "inspired by sscheck (scalacheck generators for Spark)". — [spark-testing-base README](https://github.com/holdenk/spark-testing-base/blob/main/README.md)
- [documented] sscheck: "Utilities for using ScalaCheck with Spark and Spark Streaming", using "linear temporal logic to write ScalaCheck properties for Spark Streaming programs". Latest documented version 0.3.2 on Bintray (Bintray has since shut down); last commit 2018-04-01. — [sscheck README](https://github.com/juanrh/sscheck/blob/master/README.md)
- [documented] chispa (PySpark DataFrame equality assertions) 0.12.0 released 2026-03-24; hypothesis-sqlalchemy 1.2.0 released 2026-08-15. — PyPI [chispa](https://pypi.org/pypi/chispa/json), [hypothesis-sqlalchemy](https://pypi.org/pypi/hypothesis-sqlalchemy/json)
- [lead] Practitioner posts use Hypothesis `data_frames()` for pandas cleaning code, e.g. a "no duplicate keys in output" property. They note that a failing property test is harder to interpret. These are engineering blogs, not read in full. — [Clarity AI engineering blog (Medium)](https://medium.com/clarityai-engineering/property-based-testing-a-practical-approach-in-python-with-hypothesis-and-pandas-6082d737c3ee), [dev.to post](https://dev.to/rfmf/uncovering-and-solving-data-wrangling-issues-with-property-based-testing-2pg9)

### Inferences
- **Candidate ETL properties** (proposals; each needs only generated data):
  - **Idempotent re-delivery**: `load(D); load(D)` ≡ `load(D)` for the target state.
  - **Order independence**: `load(permute(D))` ≡ `load(D)`, and for independent deliveries `load(A); load(B)` ≡ `load(B); load(A)`. This holds only where the business rules say it should; late-arriving corrections are a deliberate exception.
  - **Split invariance**: `load(A ∪ B)` ≡ `load(A); load(B)`.
  - **Conservation of counts**: rows_in = rows_loaded + rows_quarantined + rows_rejected, per source and per delivery.
  - **Round-trip**: parse(serialise(x)) = x for each delivery format.
  - **Contract closure**: for every x drawn from the input contract strategy, output ⊨ output contract (the Pandera `check_output` pattern documented in Q1).
  - **Source isolation**: adding a delivery from source S leaves entities seen only by other sources unchanged.
- **Hypothesis stateful testing fits delivery sequences**:
  - rules = "deliver batch from source k", "redeliver", "deliver correction", "advance clock";
  - Bundles hold issued source identifiers;
  - a simple in-memory reference model of the expected target state (the docs' own pattern) serves as the oracle.
- **Store the Hypothesis database** in CI artefacts, or use a shared directory, so failures found in one run replay in later runs. Promote important ones to `@example` regression cases. All of this runs outside the protected environment and needs no real rows.

### Gaps
- I found no paper or primary engineering write-up that reports PBT of ETL invariants like those above. A targeted search returned only generic pandas PBT posts.
- I did not read the Spark-side generator APIs in spark-testing-base (e.g. DataFrame generators), so their current API is unverified.

## 5. Metamorphic and differential testing for data systems

### Takeaway
DBMS testing has a mature, actively maintained metamorphic/differential toolset, though aimed at engine bugs:
- SQLancer: TLP, NoREC, PQS, DQE, QPG, CERT, DQP, CODDTest; last commit 2026-11-15; supports DuckDB, DataFusion, PostgreSQL and others.
- SQLsmith: random queries for PostgreSQL, SQLite and MonetDB; last commit 2026-11-16.
- Squirrel: coverage-guided DBMS fuzzer; dormant since 2023.

These test the engine, not your pipeline. Their *ideas* carry over: metamorphic relations need no expected output, only a relation between two runs, which fits test data with no ground truth. Pipeline-level metamorphic testing exists in the literature (MetaCDP, 2024) but is thin.

### Cited Findings
- [documented] SQLancer finds logic bugs, "bugs that cause the DBMS to fetch an incorrect result set". Its oracles, as described in the README:
  - **TLP** (OOPSLA 2020) "partitions a query into three partitioning queries, whose results are composed and compared to the original query's result set". It covers aggregates and is "among the most widely adopted".
  - **NoREC** (ESEC/FSE 2020) compares an optimised query with a hardly-optimisable rewrite.
  - **PQS** (OSDI 2020): pivot row (see Q3).
  - **DQE** (ICSE 2023): SELECT/UPDATE/DELETE with the same predicate.
  - **QPG** (ICSE 2023): query-plan-guided generation.
  - **CERT** (ICSE 2024): performance via cardinality estimates.
  - **DQP** (SIGMOD 2024): different plans for the same query.
  - **CODDTest** (SIGMOD 2025): constant folding/propagation.

  As of January 2025 the README lists Citus, ClickHouse, CockroachDB, DataFusion, Doris, DuckDB, H2, MariaDB, Materialize, MySQL, PostgreSQL, Presto, SQLite, TiDB and others. Bug reproductions are logged, and there is an experimental delta-debugging reducer (`--use-reducer`). — [SQLancer README](https://github.com/sqlancer/sqlancer/blob/main/README.md) (last commit 2026-11-15)
- [documented] NoREC paper: "Incorrect optimizations can result in logic bugs"; NoREC is "a fully-automatic approach to detect optimization bugs". — [Rigger & Su, arXiv 2007.08292](https://arxiv.org/abs/2007.08292)
- [documented] SQLsmith "is a random SQL query generator" modelled on Csmith, supporting PostgreSQL, SQLite 3 and MonetDB. Since 2015 it has found 118 bugs. — [SQLsmith README](https://github.com/anse1/sqlsmith/blob/master/README.org) (last commit 2026-11-16)
- [documented] SQLancer README lists SQLRight (coverage-guided DBMS fuzzer with NoREC and TLP oracles) and Squirrel (coverage-guided DBMS fuzzer) as related tools. Squirrel's last commit is 2023-01-23. — [SQLancer README](https://github.com/sqlancer/sqlancer/blob/main/README.md); Squirrel repo clone
- [documented] DuckDB's SQL unit tests live under `test/` and run with `build/release/test/run` (fast tests target ~20–200 ms). The README I read did not mention sqllogictest by name, and DuckDB's sqllogictest intro page was not found at the path tried [unreachable]. — [DuckDB test/README.md](https://github.com/duckdb/duckdb/blob/main/test/README.md)
- [lead] MetaCDP: Rehman, Umbreen, Rehman, "Metamorphic Testing for Quality Assurance of Containerized Data Pipelines", IEEE Cloud Summit 2024, pp. 135–142. It proposes 10 metamorphic relations for pipeline robustness/correctness and reports finding erroneous behaviours in an e-commerce pipeline. Full text not read. — [Montana State ScholarWorks](https://scholarworks.montana.edu/handle/1/18983)
- [lead] Composite metamorphic relations for integration testing of whole pipelines (bioinformatics case). — [arXiv 2305.00888](https://arxiv.org/abs/2305.00888)

### Inferences
- **Metamorphic relations for ingestion** (proposals modelled on TLP/NoREC):
  1. Row permutation of a delivery leaves the result unchanged.
  2. Splitting a delivery into two consecutive deliveries leaves the result unchanged (or changed only in load metadata).
  3. Replaying a delivery leaves the result unchanged (idempotence).
  4. Adding an unrelated source leaves results for entities not covered by it unchanged.
  5. Renaming source-local identifiers consistently leaves the matched-entity result unchanged up to the mapping.
  6. Partitioning, TLP-style: running the pipeline on rows where p, ¬p and p IS NULL, then unioning the outputs, equals the output on the full delivery, for row-local transforms.
  7. Monotonicity: adding a source that only increases coverage never removes a previously matched entity, unless that is the documented rule.
  8. Format equivalence: the same logical content as CSV, JSON and Parquet gives the same loaded result. This is differential testing across parsers.
- **Differential testing across engines**: if the platform's SQL runs on one engine in production and on DuckDB locally (like dbt `compute: local`), run the same transformation on both with generated data and diff the results. This catches dialect drift.
- **Fit**: the relations need no ground truth, so they also apply to data whose "correct" output is unknown. They can run inside the protected environment on real deliveries, exporting only pass/fail and counts, which is aggregate-level derived information. This is the one practice that safely exploits real-data diversity without moving rows out.
- **Running SQLancer** against the platform's engine is worthwhile only if the platform depends on an engine version that upstream does not test. Otherwise it is the engine vendor's job.

### Gaps
- MetaCDP full text not read, so its 10 relations are unknown here.
- I found no peer-reviewed paper on metamorphic testing of multi-source entity-ingestion pipelines specifically.

## 6. Fuzzing of delivery formats, and dirty-data generators

### Takeaway
Format parsers in the platform's dependency chain are already fuzzed in OSS-Fuzz:
- Apache Arrow C++, including Parquet and CSV in the build;
- Arrow Java, Apache Avro (JVM), jackson-dataformats-text (CSV/YAML/properties);
- pandas, libxml2, simdjson, DuckDB;
- CPython's stdlib, with targets `fuzz_csv_reader`, `fuzz_json_loads` and `fuzz_elementtree_parsewhole`.

The platform's own job is fuzzing its *own* parsing, normalisation and rejection code. The documented tools are:
- Atheris: coverage-guided Python fuzzing, structure-aware via custom mutators;
- Radamsa: mutation from valid samples;
- hypothesis-jsonschema / Schemathesis: schema-aware valid and invalid inputs;
- for semantic "dirty data": BART, REIN's injection module, Jenga, Gecko and Data Caterer edge cases.

Several of these are research code with stale maintenance.

### Cited Findings
- [documented] OSS-Fuzz `arrow` project (C++). The build enables `ARROW_CSV=on`, `ARROW_PARQUET=on` and `PARQUET_REQUIRE_ENCRYPTION=on`, and copies all `*-fuzz` executables and seed corpora. The corpus script builds seeds for `arrow-ipc-stream-fuzz`, `arrow-ipc-file-fuzz`, tensor IPC, `parquet-arrow-fuzz` (seeded with `parquet-testing/data` *and* `bad_data` files) and `parquet-encoding-fuzz`. — [oss-fuzz projects/arrow/build.sh](https://github.com/google/oss-fuzz/blob/master/projects/arrow/build.sh), [arrow cpp/build-support/fuzzing/generate_corpuses.sh](https://github.com/apache/arrow/blob/main/cpp/build-support/fuzzing/generate_corpuses.sh)
- [documented] OSS-Fuzz project.yaml files exist for `arrow-java` (jvm), `avro` (jvm, libFuzzer), `jackson-dataformats-text` (jvm), `pandas` (python, libFuzzer), `libxml2`, `simdjson` (AFL, honggfuzz, libFuzzer), `duckdb` (honggfuzz, libFuzzer), `cpython3` and `python3-libraries`. No project.yaml was found at `projects/pyarrow`, `projects/polars`, `projects/fastavro` or `projects/parquet-java` (404). — [oss-fuzz projects directory](https://github.com/google/oss-fuzz/tree/master/projects)
- [documented] CPython's `Modules/_xxtestfuzz/fuzzer.c` defines `fuzz_csv_reader`, `fuzz_json_loads`, `fuzz_elementtree_parsewhole`, `fuzz_struct_unpack`, `fuzz_builtin_float`/`int`/`unicode`, `fuzz_sre_compile`/`match`, `fuzz_ast_literal_eval` and `fuzz_pycompile`. — [cpython fuzzer.c](https://github.com/python/cpython/blob/main/Modules/_xxtestfuzz/fuzzer.c)
- [documented] Atheris is "a coverage-guided Python fuzzing engine", based on libFuzzer. It can fuzz native extensions with ASan/UBSan, supports Python 3.11–3.14 in current source, and does structure-aware fuzzing via custom mutators. atheris 3.1.0 released 2026-06-17. — [Atheris README](https://github.com/google/atheris/blob/master/README.md), [PyPI](https://pypi.org/pypi/atheris/json)
- [documented] Radamsa is "a test case generator for robustness testing, a.k.a. a fuzzer", that "works by reading sample files of valid data and generating interestingly different outputs from them". — [Radamsa README](https://github.com/aoh/radamsa/blob/develop/README.md)
- [documented] Schemathesis applies schema-aware positive/negative generation to OpenAPI, GraphQL and gRPC APIs (see Q2). hypothesis-graphql 0.13.7 released 2026-11-21. — [Schemathesis docs](https://github.com/schemathesis/schemathesis/blob/master/docs/explanations/data-generation.md), [PyPI](https://pypi.org/pypi/hypothesis-graphql/json)
- [documented] Dirty-data generators and their maintenance state:
  - BART: Java, PostgreSQL ≤11/H2, last commit 2023-05-10.
  - Jenga: alpha, last commit 2022-10-31.
  - Raha/Baran: detection/correction, needs dirty+clean pairs, last commit 2025-06-05.
  - REIN: benchmark framework, uses BART plus an error-generator library.
  - Gecko: beta, 2024-12-06.

  — sources in Q3.

### Inferences
- **Three layers of delivery-format fuzzing**:
  1. **Byte-level**: Atheris or Radamsa on the platform's ingestion entry point (`parse(bytes) → rows | rejection`). Seed with generated valid files per format. The oracle is "no crash, no hang, and every input ends in a defined accept/reject state with a reason".
  2. **Structure-aware**: generate valid CSV/JSON/XML/Parquet/Avro from the contract via Hypothesis (pyarrow writers, csv dialect variations such as delimiter, quoting, BOM, encodings, line endings), then mutate one structural aspect at a time.
  3. **Semantic dirty data**: catalogued defects with expected outcomes (Q2/Q3).
- **What leaves the protected environment**: nothing for layers 1–2. For layer 3, defect frequencies observed in real data, as aggregates.
- **Licensed reference data**: generators should *not* ship real code lists. Use format-valid synthetic codes, or obtain licence clearance for the code list itself.
- **Where upstream fuzzing stops**: `pyarrow`, `polars` and `fastavro` had no OSS-Fuzz project.yaml at the paths tried. Python-level wrappers over Arrow C++ are therefore covered only indirectly through the C++ project (inferred from the 404s).

### Gaps
- I did not verify current OSS-Fuzz status (active vs. disabled targets, open-issue counts) for these projects. Only project.yaml/build.sh presence was checked.
- I found no maintained, general-purpose OSS "dirty tabular data generator" with an active release cadence. The best-known ones (BART, Jenga, the REIN error generator) are research code. Data Caterer's edge-case/null options are the maintained but shallower alternative.
- Grammar-based CSV fuzzers (e.g. dedicated CSV grammars for AFL++/Grammarinator) were not researched for lack of budget. AFL++ itself was not checked.
