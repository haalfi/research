# B1: Orchestrator-neutral pipeline logic and connector/EL contracts

Grading key: **[documented]** = vendor doc/spec, with version and date; **[first-hand]** = practitioner report with an outcome; **[inferred]** = my inference, labelled. Versions come from PyPI JSON, fetched 2026-10-27. Docs were fetched from the current `devel`/`master`/`main` branches on 2026-10-27, unless a date is given.

Versions as of 2026-10-27 (PyPI, latest release and upload date):
- dlt 1.31.0 (2026-10-07)
- dagster 1.13.27; dagster-dlt 0.29.27 (2026-10-26)
- meltano 4.4.1 (2026-10-07)
- singer-sdk 0.54.9 (2026-10-19)
- airbyte-cdk 7.39.1 (2026-10-23)
- airbyte-protocol-models 0.18.0 (2025-06-27). The protocol changelog lists v0.19.0, dated 2025-10-10.
- dag-factory 1.1.0 (2026-05-07)
- gusty 0.23.1 (2025-05-14)

Source for all versions: [PyPI JSON API](https://pypi.org/pypi/dlt/json) (same endpoint for each package).

## Q1: Where should feed logic live so it runs and is tested without an orchestrator, and what still needs orchestrator integration tests?

### Takeaway
The vendor docs show that the main EL libraries are built to run as plain Python or CLI processes, with the orchestrator integration as a thin wrapper. dlt sources run directly. The Dagster dlt component points at a `loads.py` that "can also be run directly using dlt". Singer taps and Airbyte connectors are CLI or container processes. I found **no authoritative or first-hand source** that applies "functional core / imperative shell" or hexagonal architecture specifically to orchestrated data pipelines, so that framing rests on inference. What stays orchestrator-specific is how definitions load, asset-key mapping, schedules, and partitions. Dagster ships sandbox utilities to test exactly that.

### Cited Findings
- **dlt as plain library [documented, dlt 1.31.0 docs].** A dlt resource is a Python generator decorated with `@dlt.resource`. It reads and writes `dlt.current.resource_state()`, and `dlt.pipeline(...).run()` executes it without an orchestrator. — [dlt docs: State](https://raw.githubusercontent.com/dlt-hub/dlt/devel/docs/website/docs/general-usage/state.md)
- **dagster-dlt wrapper is thin [documented, dlt docs "Deploy with Dagster", current devel].** `@dlt_assets(dlt_source=..., dlt_pipeline=dlt.pipeline(...))` wraps an existing source, and the body is `yield from dlt.run(context=context)`. Limitation: "The dlt Dagster helper works only with dlt sources. Your resources should always be grouped in a source." — [dlt docs: Deploy with Dagster](https://raw.githubusercontent.com/dlt-hub/dlt/devel/docs/website/docs/walkthroughs/deploy-a-pipeline/deploy-with-dagster.md)
- **Dagster dlt Component [documented, Dagster docs master, Dagster 1.13.27 era].**
  - `DltLoadCollectionComponent`: `dg scaffold defs` generates `defs.yaml` and `loads.py`.
  - `loads.py` "contains a skeleton dlt source and pipeline which are referenced by Dagster, but can also be run directly using dlt."
  - `defs.yaml` references sources and pipelines by fully scoped Python identifier. A `translation` key customises the asset properties.
  - Source: [Dagster docs: dlt component](https://raw.githubusercontent.com/dagster-io/dagster/master/docs/docs/integrations/libraries/dlt/index.md) (via a sparse git clone of dagster-io/dagster, HEAD 2026-10-27).
- **What Dagster tests at the orchestrator layer [documented, Dagster docs master].**
  - `dg.components.testing.create_defs_folder_sandbox()` builds a temporary `defs` folder.
  - `DefsFolderSandbox.scaffold_component` and `load_component_and_build_defs` "test instantiation of a component, and validate the definitions it produces". Dagster's own dlt component tests use this to assert the expected asset keys.
  - Source: [Dagster docs: Testing your component](https://github.com/dagster-io/dagster/blob/master/docs/docs/guides/build/components/creating-new-components/testing-your-component.md) (read via the sparse clone).
- **`dagster-embedded-elt` deprecated [documented, Dagster docs master].** "dagster-embedded-elt has been deprecated and replaced by dagster-sling and dagster-dlt." Older tutorials that import `dagster_embedded_elt` are stale. — [Dagster docs: embedded-elt](https://github.com/dagster-io/dagster/blob/master/docs/docs/integrations/libraries/embedded-elt.md)
- **Early dlt + Dagster tutorial [documented tutorial, 2023-11-01, older than 2 years].**
  - The pattern is a `DDltResource` configurable resource that "allows you to reuse pipeline code inside an asset".
  - The tutorial scaffolds test folders but shows no tests, and it claims you can "rigorously test them before shipping" without showing how.
  - The fetched code has defects: an undefined `dlt_resource`, and late binding in a loop inside an asset factory.
  - Source: [dltHub blog: dlt-dagster](https://dlthub.com/blog/dlt-dagster)
- **Functional core / imperative shell applied to pipelines.** The search turned up only generic explanations and an unvetted "skill" file describing an F# ETL with "functional core, imperative shell" and shell scripts as thin wrappers. None is a practitioner outcome report. **Not graded as evidence.** — [claudskills.com ETL skill](https://claudskills.com/skills/etlskill/SKILL.md) (search lead only, not fetched)

### Inferences
- [inferred] The vendors' own designs suggest a layering for the observed symptoms:
  - The feed-specific "functional core" is the parse and normalise functions, plus the dlt resources or Singer tap logic. These take bytes or responses as input and yield records.
  - The "shell" is the EL runner: `dlt.pipeline.run`, `meltano run`, or the Airbyte platform.
  - The orchestrator wrapper (`@dlt_assets`, a Component YAML, a Databricks job task) is the outermost shell.
  - Tests at each layer:
    - pytest on parse functions with recorded vendor fixtures;
    - a dlt pipeline run against `destination="duckdb"` (as in the Dagster walkthrough) or a local DuckLake;
    - only a thin `load_component_and_build_defs` / asset-key test at the Dagster layer.
- [inferred] What still needs orchestrator integration tests:
  - asset-key and lineage mapping to dbt sources (see the MetaOps key-drift finding under Q3);
  - schedule and automation conditions;
  - partition and backfill semantics;
  - resource and secret wiring;
  - concurrency, for example two runs of the same dlt pipeline name or Meltano `state_id`.
- [inferred] Early warning sign that logic has leaked back into the orchestrator: any test needs `dagster.materialize()` or a running webserver to exercise parse or landing behaviour, or feed code imports `dagster` outside the definitions module.

### Gaps
- No first-hand practitioner report found that applies hexagonal or functional-core architecture to an orchestrated ingestion codebase and reports an outcome.
- Recorded-fixture testing of vendor APIs (VCR-style) for dlt or Singer: no authoritative doc fetched.

## Q2: Declarative pipeline definitions that an adapter compiles into orchestrator objects

### Takeaway
Most options are YAML or spec files that a framework adapter turns into orchestrator objects at load time: Dagster Components (`defs.yaml`), dag-factory and gusty for Airflow, Meltano `meltano.yml`, and Databricks bundles. The exit cost depends on whether the spec references plain Python or tool objects (like the dlt Component pointing at `loads.py`) or encodes orchestrator concepts directly.

### Cited Findings
- **Dagster Components [documented, Dagster 1.13.x docs master].**
  - The dlt component's `defs.yaml` pairs sources and pipelines by Python import path.
  - The Sling component scaffolds `defs.yaml` plus `replication.yaml`.
  - Components can be unit tested via `create_defs_folder_sandbox`.
  - Source: [Dagster docs: dlt component](https://raw.githubusercontent.com/dagster-io/dagster/master/docs/docs/integrations/libraries/dlt/index.md); [Testing your component](https://github.com/dagster-io/dagster/blob/master/docs/docs/guides/build/components/creating-new-components/testing-your-component.md)
- **Databricks bundles renamed [documented, Databricks docs "Last updated on Sep 11, 2026"].**
  - "Declarative Automation Bundles (formerly known as Databricks Asset Bundles)" describe Databricks resources such as Lakeflow Jobs and Lakeflow pipelines as source files.
  - A bundle includes "Source files, such as notebooks and Python files, that include the business logic" and "Unit tests and integration tests".
  - Source: [Databricks docs: What are Declarative Automation Bundles?](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- **Dagster ↔ Databricks bundle bridge is PREVIEW [documented, Dagster docs master].**
  - "`DatabricksAssetBundleComponent` is currently in **preview**. The API may change in future releases." The same preview note applies to `DatabricksWorkspaceComponent`.
  - By default it creates one Dagster asset per Databricks task.
  - It supports notebook, Python script, Python wheel, JAR, run-job and condition tasks.
  - Compute options: serverless, new cluster, or existing cluster.
  - Source: [Dagster docs: Databricks Asset Bundle Component](https://github.com/dagster-io/dagster/blob/master/docs/docs/integrations/libraries/databricks/databricks-asset-bundle-component.md)
- **dag-factory [documented, README main; 1.1.0, 2026-05-07].** dag-factory is "a library for Apache Airflow® to construct DAGs declaratively via configuration files". It requires Python 3.10+ and Airflow 2.9+, and offers `load_yml_dags`, custom Python objects and custom operators. Airflow only. — [dag-factory README](https://raw.githubusercontent.com/astronomer/dag-factory/main/README.md)
- **gusty [documented, README main; 0.23.1, 2025-05-14].**
  - gusty turns "every file in a DAG directory into a task". Supported file types: YAML, Python, SQL, Jupyter Notebook and R Markdown.
  - It manages in-DAG and external dependencies. Airflow only.
  - The last release is about 17 months old, which is not yet over the 2-year flag but is worth watching.
  - Source: [gusty README](https://raw.githubusercontent.com/pipeline-tools/gusty/main/README.md)
- **Meltano projects [documented, Meltano 4.4.1 docs main].** `meltano.yml` holds the project, including `state_backend.uri`. — [Meltano docs: State backends](https://raw.githubusercontent.com/meltano/meltano/main/docs/docs/concepts/state_backends.md)
- **dagster-meltano is community-supported [documented, Dagster docs master].** Tagged `community-supported`, with source at `quantile-development/dagster-meltano`. It can also be managed via `meltano add utility dagster`. — [Dagster docs: Meltano](https://github.com/dagster-io/dagster/blob/master/docs/docs/integrations/libraries/meltano.md)

### Inferences
- [inferred] Exit cost toward Databricks for each kind of spec:
  - **Dagster Component YAML** is a Dagster-only format. Moving means rewriting the YAML as bundle job and task definitions. The referenced dlt `loads.py` and its tests move as-is: dlt documents notebook execution and Databricks destination credentials taken from the notebook context (see Q3).
  - **In-house spec compiler:** an internal spec, for example a Pydantic `FeedSpec` covering source, cadence, landing path and schema, compiled to both Dagster objects and bundle YAML, keeps the exit cost in one adapter. The cost is owning and versioning that compiler.
  - **dbt** is the precedent: both Dagster (dagster-dbt) and Databricks (dbt tasks) consume its project.
- [inferred] Failure mode of spec compilers: they drift into encoding orchestrator concepts (retries, partitions, sensors) in the spec. Early sign: spec fields named after a single orchestrator's API.
- [inferred] Because the Databricks bundle bridge is preview, treat any Dagster-runs-a-Databricks-bundle plan as non-GA as of 2026-10-27.

### Gaps
- An in-house spec compiler targeting both Dagster and Databricks bundles: no first-hand report found.
- Dagster Components GA or preview status for the core framework was not checked in this track. Only the Databricks components carry an explicit preview note in the fetched files.
- Lakeflow Connect (Databricks managed ingestion) was not researched in this track.

## Q3: What each EL contract puts on the source side vs the run side, and what it forces or prevents

### Takeaway
The four contracts differ mainly in who stores state:
- **dlt:** state is a dict that the source code reads and writes. dlt also stores it in the destination (`_dlt_pipeline_state`), so a clean container can restore it. That makes it orchestrator-neutral but tied to the destination.
- **Singer and Airbyte:** the source only emits opaque STATE messages. A runner (Meltano, the Airbyte platform) must persist them and feed them back in.
- **Meltano:** stores state in a pluggable backend (system DB, file, S3, Azure, GCS, Snowflake, custom), with locking.

### Cited Findings
**dlt [documented, dlt 1.31.0 docs devel]**
- State is "a Python dictionary that lives alongside your data". It has resource scope (`dlt.current.resource_state()`) and source scope (`dlt.current.source_state()`), and must be JSON serialisable. — [dlt docs: State](https://raw.githubusercontent.com/dlt-hub/dlt/devel/docs/website/docs/general-usage/state.md)
- State is stored locally in the pipeline working directory. In addition, "dlt loads your state into the destination along with all other data, and when faced with a clean start, it will try to restore the state from the destination."
  - The remote state is keyed by pipeline name, destination location (credentials) and dataset.
  - It lives in the `_dlt_pipeline_state` table.
  - Restore can be disabled with `restore_from_destination=false`.
  - The docs give Airflow, "where every task gets a clean filesystem", as the motivating case.
  - Source: same page.
- Limits on state:
  - Do not use state if it can grow to millions of elements.
  - Alternatives: an external store (with the warning that "if the extract stage fails, you'll end up with an invalid state") or querying the loaded data via `dlt.current.pipeline().dataset()`.
  - Parallel resources need one designated state writer.
  - Source: same page.
- Incremental and idempotency features:
  - `dlt.sources.incremental` provides last-value cursors.
  - Write dispositions: append, replace, and merge (`delete-insert`, `scd2`, `upsert`, `insert-only`, `cdc`, using `primary_key`/`merge_key`).
  - `refresh` modes `drop_data`, `drop_resources` and `drop_sources` reset state and tables.
  - Source: [dlt docs: Incremental loading](https://raw.githubusercontent.com/dlt-hub/dlt/devel/docs/website/docs/general-usage/incremental-loading.md)
- REST API source retries and timeouts are configured through a custom `requests` session. — [dlt docs: REST API source](https://raw.githubusercontent.com/dlt-hub/dlt/devel/docs/website/docs/dlt-ecosystem/verified-sources/rest_api/basic.md)
- Databricks:
  - dlt loads into Delta tables via Unity Catalog.
  - It needs a staging bucket (S3 or Azure Blob), or uses "Direct Load" from a Databricks notebook, with a Unity Catalog volume as staging.
  - It reads credentials from the notebook context first and falls back to SQL warehouse discovery.
  - Source: [dlt docs: Databricks destination](https://raw.githubusercontent.com/dlt-hub/dlt/devel/docs/website/docs/dlt-ecosystem/destinations/databricks.md)

**Singer [documented, SPEC.md "Version 0.3.0", undated in file, older than 2 years (inferred from the singer-io repo's age; not verified)]**
- `tap --config CONFIG [--state STATE] [--catalog CATALOG]`.
  - Config is JSON and "typically ... the credentials".
  - Taps may write config changes back to the config file.
  - Source: [Singer SPEC.md](https://raw.githubusercontent.com/singer-io/getting-started/master/docs/SPEC.md)
- Output is JSON lines on stdout.
  - RECORD messages carry `record`, `stream` and an optional `time_extracted`.
  - SCHEMA messages carry a JSON Schema plus `key_properties`.
  - STATE messages carry `value`.
  - "The semantics of a STATE value are not part of the specification, and should be determined independently by each Tap."
  - A tap "should expect the file named by the `--state STATE` argument to have the same format as the value of the STATE messages it emits."
  - Source: same file.
- Versioning: taps should follow SemVer across config, state interpretation and output structure. — same file.

**Meltano [documented, Meltano 4.4.1 docs main]**
- Meltano tracks pipeline state per `state_id`. Backends: the system database (default `systemdb`), local filesystem (`file://`), S3 and S3-compatible stores, Azure Blob, GCS, Snowflake, or custom backends.
- Remote backends are aimed at "ephemeral environments".
- Locking applies per `state_id`, with `state_backend.lock_timeout_seconds` and `lock_retry_seconds`.
- State backends have been available since Meltano 2.10.
- Source: [Meltano docs: State backends](https://raw.githubusercontent.com/meltano/meltano/main/docs/docs/concepts/state_backends.md)

**Airbyte protocol [documented, protocol doc master; changelog latest v0.19.0, 2025-10-10]**
- Source: `read(Config, ConfiguredAirbyteCatalog, State) -> Stream<AirbyteRecordMessage | AirbyteStateMessage>`. Destination: `write(Config, AirbyteCatalog, Stream<AirbyteMessage>) -> Stream<AirbyteStateMessage>`.
- State "is only ever written or read by the source". "Sources are the sole producer/consumer of a State messages' contents".
- A destination re-emitting a state message "indicates that all records which came before ... have been committed". The platform must receive every state message, in order, and errors on dropped or out-of-order states.
- Source: [Airbyte protocol](https://raw.githubusercontent.com/airbytehq/airbyte/master/docs/platform/understanding-airbyte/airbyte-protocol.md)
- State types:
  - Stream: per-stream, allows per-stream reset and parallelism.
  - Global: shared state, for example CDC.
  - Legacy: "No new Connectors should be created using Legacy state."
  - Source: same file.
- Two data-channel modes:
  - STDIO JSON (legacy): source → orchestrator → destination.
  - Socket mode: Protocol Buffers over Unix domain sockets, source → destination directly, with a Bookkeeper on the control channel. It claims "4-10x performance improvements". State messages carry `partition_id` and an incrementing `id`.
  - The platform's ArchitectureDecider picks the mode based on connector compatibility, feature flags and configuration.
  - Source: same file.
- Connector spec: `protocol_version` defaults to "0.2.0". Protocol v0.6.0 (2024-01-24) added `AirbyteRecordMessageMeta`; v0.15.0 (2025-04-07) added file+metadata streams. — same file.
- [inferred from the protocol doc's process model] Connectors are separate actor processes driven by the platform, distributed as Docker images. The doc fetched here does not detail the image packaging, so this point is inferred.

**Practitioner reports [first-hand, graded]**
- **Yespark: Airbyte → dlt.**
  - Context: talk 2026-02-05, published on the **vendor (dltHub) blog** on 2026-03-05.
  - The CTO migrated Postgres, Zendesk, HubSpot, Google Ads, Sheets, GA4, GSC and app-review sources to dlt → Snowflake under **Prefect** (not Dagster), in about a week, with Claude Code.
  - The cutover was incremental, one source at a time, starting with the highest-volume Postgres source. Airbyte was removed on day 4.
  - Reported outcome: "After migration: 11 runs, 0% failure rate". A 5M-row Postgres sync took about 1 hour.
  - Open issues: the Zendesk ticket-comments source still erroring; a Google Ads token still pending.
  - Pre-migration Airbyte pains: partial syncs after ten attempts, a dedicated instance, Docker upkeep, and disks filling with logs.
  - Grade: first-hand, but vendor-hosted, with a short observation window (11 runs).
  - Source: [dltHub blog: Yespark](https://dlthub.com/blog/yespark-airbyte-dlt)
- **MetaOps: Dagster + Airbyte in practice (2026-09-10).**
  - "Dagster owns the clock, Airbyte owns the mechanics": credentials, stream selection, sync modes and sync state stay in Airbyte, and Airbyte schedules must be set to Manual.
  - Failure modes:
    - double scheduling if Airbyte's schedule is left on;
    - connection-level syncs, so materialising one asset syncs every stream in the connection and backfills multiply source load;
    - `DagsterInvalidDefinitionError` for a stream enabled in two connections;
    - asset-key drift producing "unexpected asset" warnings;
    - lineage not linked when keys don't match dbt source names;
    - no rows, bytes or duration on materialisations by default.
  - Grade: consultancy write-up drawn from "a number of client engagements", with no quantified outcomes. Partial first-hand.
  - Source: [MetaOps blog](https://metaops.solutions/blog/dagster-airbyte-integration-in-practice)
- **dltHub "Moving off Airbyte":** cites "99.83% run success across 50m" runs. Vendor marketing, search snippet only, not fetched, unverified. — [dltHub blog](https://dlthub.com/blog/migrate-from-airbyte-to-dlthub)

### Inferences
- [inferred] **dlt forces / prevents:**
  - Because state lives in the destination keyed by pipeline name and dataset, any runner (Dagster, a Databricks job, a laptop) can resume a pipeline it can reach. Exit toward Databricks therefore does not need a state migration if the destination stays the same.
  - That same coupling means changing destination (Postgres/DuckLake → Unity Catalog) resets incremental state unless it is copied. Early warning sign: unexpected full reloads after a destination or dataset rename.
  - Two concurrent runs with the same pipeline name are a risk. dlt docs advise a single state writer; the orchestrator must prevent overlap.
- [inferred] **Singer forces / prevents:** the tap is stateless across runs, and the runner must persist the last STATE emitted. The spec defines only the tap side, so the conventions for target ↔ state echoing and the checkpoint commit point were not in the fetched SPEC.md. Under Dagster, a Singer tap needs Meltano or a custom runner to hold state.
  - Exit to Databricks: the Meltano state backend (for example S3) is portable. A run that happens outside `meltano run` must reimplement state handling.
- [inferred] **Airbyte forces / prevents:** state lives in the Airbyte platform. Dagster or Databricks only trigger syncs, so the Airbyte deployment (Docker or Kubernetes) remains a separate run plane. Moving orchestrators is cheap: change the trigger. Leaving Airbyte is expensive: Yespark rewrote its sources.
- [inferred] Typing:
  - dlt infers and evolves its schema, with schema contracts available (not fetched here).
  - Singer and Airbyte use JSON Schema per stream, declared by the source.
  - Vendor shapes leaking into the generic lake layer is a design choice in all four: none of them forces a normalised canonical model.

### Gaps
- Singer state-echo semantics for targets (CONFIG_AND_STATE.md) was not fetched.
- dlt schema contracts doc was not fetched.
- Airbyte CDK (7.39.1) and declarative low-code manifest docs were not fetched.
- Airbyte Docker image packaging was not verified from the docs.
- No first-hand report found of moving dlt or Meltano pipelines from Dagster to Databricks jobs (searched; nothing found).

## Q4: Raw-bytes retention per delivery (audit)

### Takeaway
None of the four contracts keeps raw vendor payloads by default for API sources. All of them carry parsed records:
- dlt yields Python records;
- Singer RECORD and Airbyte RecordMessage are JSON maps.

Only Airbyte has a documented "Copy raw files" mode, and only for a few file-based sources, with S3 as the sole destination. dlt's filesystem source separates file listing (`FileItem` metadata) from reading, which gives a natural hook for copying files, but this is inferred, not a documented raw-retention feature.

### Cited Findings
- **Singer [documented, spec 0.3.0].** A RECORD message's `record` is "A JSON map containing a streamed data point". There is no raw-payload message type. `time_extracted` is optional. — [Singer SPEC.md](https://raw.githubusercontent.com/singer-io/getting-started/master/docs/SPEC.md)
- **Airbyte [documented, docs master].**
  - "Copy raw files" delivery method: for file-based sources, "Airbyte syncs your raw files and includes structured metadata describing" them.
  - Sources: Zendesk Support, S3, SharePoint, Google Drive, SFTP Bulk.
  - Destination: **S3 only**.
  - Connectors declare `supportsFileTransfer: true`.
  - Source: [Airbyte docs: Sync files and records](https://raw.githubusercontent.com/airbytehq/airbyte/master/docs/platform/using-airbyte/sync-files-and-records.md)
  - Protocol v0.15.0 (2025-04-07) added file+metadata streams. — [Airbyte protocol](https://raw.githubusercontent.com/airbytehq/airbyte/master/docs/platform/understanding-airbyte/airbyte-protocol.md)
  - File size limits conflict in search snippets (1 GB in the v1.2 release notes vs 1.5 GB in a later guide). Unverified.
  - Feature history: v1.2 shipped it as early access. — [Airbyte v1.2 release notes](https://docs.airbyte.com/release_notes/v-1.2) (search lead, not fetched)
- **dlt [documented, 1.31.0 docs].**
  - The `filesystem` resource covers S3, GCS, Azure, Google Drive, **SFTP** and local storage.
  - It "will only list files ... and yield the files metadata. The filesystem resource itself does not read or copy files."
  - Readers parse CSV, Parquet and JSONL into records.
  - Incremental loading over new files via `dlt.sources.incremental("modification_date")`.
  - Source: [dlt docs: Filesystem source](https://raw.githubusercontent.com/dlt-hub/dlt/devel/docs/website/docs/dlt-ecosystem/verified-sources/filesystem/index.md)
- **Meltano:** same as Singer, since it orchestrates Singer taps and targets. — [Meltano docs: State backends](https://raw.githubusercontent.com/meltano/meltano/main/docs/docs/concepts/state_backends.md) (context)

### Inferences
- [inferred] For an audit requirement covering what was received, when and from whom, every option needs a separate **raw landing step** owned by the team:
  - write the HTTP response or SFTP file bytes to object storage, content-addressed or delivery-ID keyed;
  - record a manifest row (source, received_at, sha256, size);
  - the EL tool then parses from the landed bytes.

  dlt fits this as two stages:
  - Stage 1: a plain function or dlt resource that copies bytes and yields manifest records.
  - Stage 2: a `filesystem` + reader pipeline over the landed prefix, with an incremental cursor on `modification_date` or the manifest.

  Singer and Airbyte record streams cannot reconstruct the original bytes. Airbyte's copy-raw-files mode covers SFTP→S3 only for the listed connectors, not vendor HTTP APIs.
- [inferred] Idempotent re-runs then key on delivery ID and hash in the manifest, not on EL-tool state. EL state (dlt cursors, Singer/Airbyte STATE) becomes a performance optimisation, not the audit record.
- [inferred] Early warning sign: an auditor asks for "the file vendor X sent on date D" and only parsed rows exist, or parsed-row counts can't be reconciled with a delivery manifest.

### Gaps
- No vendor doc found describing dlt keeping raw HTTP response bodies per request. The REST API source "response_actions" and hooks could support this but were not verified.
- No first-hand report found of a regulated firm using any of these tools with raw-payload retention.
