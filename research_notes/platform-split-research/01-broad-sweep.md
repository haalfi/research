# Track 01: broad sweep (deep-research workflow run wf_542012fb-65f)

Run 2026-10-27. 6 angles, 23 sources fetched, 112 claims extracted, 25 verified (3 votes each, 2 refutes kill), 22 confirmed, 3 refuted, merged to 12 findings. 11 claims dropped by budget, unverified.

## Summary

This is an options study, so nothing here is a recommendation. The 22 verified claims all come from vendor documentation or tutorials. None is a practitioner report with an outcome. They cover RQ1-RQ5 only in part and give no direct evidence on Databricks Lakeflow Jobs or Declarative Pipelines, or on the RQ6 capability table. On RQ3, Dagster offers config-driven definition through asset factories built as custom Components (docs 1.13.27). Components were called stable in 1.11 (2025-06-26) and GA in 1.12 (2025-10-30). Even so, a new feed is still a Dagster-specific defs.yaml entry that ships inside the code location's image. Minor releases can also break this path: 1.13.0 (2026-04-09) removed Component-loading APIs. On RQ2, Dagster upgrades can change orchestrator-owned storage (the 1.9.0 run and backfill schema migrations, October 2024, now about 2 years old). For Dagster+ Hybrid the vendor sets a one-way rule: agent version >= code location version. Dagster Pipes can run logic on Databricks while Dagster only orchestrates. That route ties the external code to the dagster_pipes protocol and to Unity Catalog Volumes. Triggering existing Databricks jobs with plain run_now avoids that tie. On RQ4, vendor documents show two handoff precedents: a delivery-level completion marker (PDL's COMPLETED; per-subdirectory _SUCCESS markers are documented as unreliable) and a manifest with SHA-256 checksums, record counts and explicit empty-day files (MX SFTP, now closed to new integrations). Temporal's default limits (2 MB payload, 50 MB / 51,200-event history) mean an acquisition-side Temporal design must pass references to stored bytes, not the bytes. On RQ5, Dagster's own guidance says a monorepo shares one CI/CD pipeline and cannot deploy projects independently, while multiple repos deploy independently but have to publish packages to share code.

## Findings

### F1 (high, votes 3-0, 3-0)

RQ3 option, declarative feed definition inside the orchestrator. Dagster asset factories turn configuration into many similar asset definitions. The current guide (docs 1.13.27) builds the factory as a custom Component, which needs a components-ready project or a migration to dg. You scaffold it with `dg scaffold component` / `dg scaffold defs` and declare one etl_job entry per instance in defs/<name>/defs.yaml. A pure-Python factory that returns dg.Definitions is also documented. Gives: a new feed needs no new per-feed Python. Costs: each feed is a Dagster-specific YAML entry in the code location, still released with that location's image, and the factory class is orchestrator code. Exit cost toward Databricks (inferred): Databricks does not read the defs.yaml `type:` (which points at a Dagster Component class) or the factory, so both would have to be rewritten.

**Evidence:** Documented: vendor docs 1.13.27, fetched 2026-10-27. Votes 3-0 and 3-0. The page says 'many engineers use' factories. It does not call them 'the' sanctioned way. The example is a toy S3/duckdb ETL with no outcome. Deploy independence is not addressed. The exit-cost point is inferred.

**Sources:** https://docs.dagster.io/guides/build/assets/creating-asset-factories

### F2 (high, votes 2-1, 3-0)

Lifecycle of Components and dg (the dates matter for RQ3/RQ2). Components were labelled stable in Dagster 1.11 (blog dated 2025-06-26). A separate Dagster post dated 2025-09-18 called them generally available. The 1.12 release notes (2025-10-30) mark the Components framework and dg CLI as GA, 'previously Release Candidate'. The GA statement covers the framework and the CLI. Individual integration components and sub-features such as StateBackedComponent and its storage options have to be checked one by one.

**Evidence:** Documented: vendor blog posts plus CHANGES.md. The 1.11 claim passed 2-1 and the 1.12 GA claim 3-0. The sources use 'stable' (1.11), 'GA' (blog, 2025-09) and 'GA' (1.12) in ways that do not line up; the 1.12 changelog is the most authoritative. The 1.11 source is more than a year old.

**Sources:** https://dagster.io/blog/dagster-1-11-build-me-up-buttercup, https://www.dagster.io/blog/dagster-1-12-monster-mash, https://dagster.io/blog/dagster-components-ga, https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md

### F3 (high, votes 3-0, 3-0)

RQ2 failure mode: minor Dagster releases break orchestrator-bound pipeline code. 1.13.0 (PyPI upload 2026-04-09) removed ComponentLoadContext.load_component_at_path and build_defs_at_path, now context.load_component / context.build_defs. The same release removed external_asset_from_spec(s), Definitions.get_all_asset_specs, the single-AssetKey deps form, legacy_freshness_policy, and deprecated APIs in dagster-airbyte, looker, powerbi and sigma. Any definition code that calls these APIs must change on a 1.12 to 1.13 upgrade. Early warning sign (inferred): deprecation warnings in the 1.12.x line.

**Evidence:** Documented: vendor migration guide and changelog, confirmed against the primary CHANGES.md. Votes 3-0 and 3-0. The docs do not say when these APIs were first deprecated. 'Breaking removals continue in 1.x' generalises from this pattern.

**Sources:** https://docs.dagster.io/migration/upgrading, https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md, https://releases.sh/release/rel_aSQFP62NqOzBdq4Y19clK-1-13-0-core-0-29-0-libraries

### F4 (high, votes 3-0)

RQ2/RQ3 state placement. From 1.13.0, integrations that depend on external metadata (dbt, Fivetran, Airbyte, Tableau, Looker) use persisted local state for components by default, which the notes say makes code location loading more predictable. From 1.13.1, state-backed integration components default to LOCAL_FILESYSTEM storage instead of legacy_code_server_snapshots. This state lives with the code location (a defs_state directory), not in the Dagster instance or run storage. So derived definition state, such as a dbt manifest, is a separate class of state from run history.

**Evidence:** Documented: primary changelog quoted word for word (1.13.0 Major Changes; 1.13.1 entry; StateBackedComponent introduced in 1.12.x). Vote 3-0. What this means for which state should sit with the orchestrator is inferred.

**Sources:** https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md, https://releases.sh/release/rel_aSQFP62NqOzBdq4Y19clK-1-13-0-core-0-29-0-libraries

### F5 (high, votes 3-0)

RQ2: an orchestrator upgrade can change orchestrator-owned run-history storage independently of pipelines. Dagster 1.9.0 shipped schema and data migrations: a new column on runs, a new column on bulk_actions, and a new backfill_tags table, applied with `dagster instance migrate`. The docs 'highly recommend' the migration to avoid slow Runs page loads; it is not stated as mandatory. Run history, backfills and tags therefore belong to orchestrator storage, and each orchestrator upgrade has to plan its own storage migration.

**Evidence:** Documented: vendor MIGRATION.md. Vote 3-0. 1.9.0 shipped around 2024-10, so it is about 2 years old (flag). Whether 1.10 to 1.13 include storage migrations was not checked.

**Sources:** https://docs.dagster.io/migration/upgrading, https://raw.githubusercontent.com/dagster-io/dagster/master/MIGRATION.md

### F6 (medium, votes 3-0)

RQ2/RQ5 compatibility rule, Dagster+ Hybrid only. Agent and code location versions may differ, but the agent must be upgraded first and a code location must never be newer than the agent. The rule is one-way: orchestrator >= pipeline code. Applying it to OSS (webserver/daemon vs gRPC code servers) is inference. No supported version-skew window is stated. A related claim, that agent and code locations can be upgraded fully independently, was refuted 1-2 because the ordering constraint is mandatory.

**Evidence:** Documented: vendor support FAQ, undated ('updated 12 months ago', around late 2025), no versions given. Vote 3-0. The verifier says other Dagster docs (Kubernetes agent and code location guides) agree.

**Sources:** https://support.dagster.io/articles/7616463479-can-the-dagster-cloud-agent-and-code-location-versions-be-different

### F7 (medium, votes 3-0)

RQ1 testability: Dagster supports unit-testing assets and ops by calling the decorated function directly in pytest, passing input values and mocked resources (build_asset_context). The logic can be tested without a deployed orchestrator, which is inferred from in-process invocation; the docs do not say outright that no instance is needed. The unit under test is still Dagster-decorated code, so this does not fix 'feed logic stuck in orchestrator-specific code'. That needs logic kept in plain Python libraries outside the decorators (inferred).

**Evidence:** Documented: vendor docs 1.13.27. Vote 3-0. The cited concepts URL is a navigation page; the content is on the unit-testing guide. A related claim, that direct invocation fails for multi-assets with upstream inputs, was refuted 0-3.

**Sources:** https://dagster.io/docs/guides/test/unit-testing-assets-and-ops, https://docs.dagster.io/concepts/testing

### F8 (high, votes 3-0, 3-0, 2-1)

RQ1/RQ2 bridge option toward Databricks: Dagster Pipes. With Pipes on Databricks serverless (docs 1.13.27), the code runs entirely on Databricks and the Dagster asset is 'the orchestrator, not the executor'. Logs and metadata stream back. Requires: the Databricks notebook or script imports dagster_pipes and wraps its logic in open_dagster_pipes with PipesUnityCatalogVolumesContextLoader, PipesUnityCatalogVolumesMessageWriter and PipesDatabricksNotebookWidgetsParamsLoader, and reports through pipes.log / pipes.report_asset_materialization. Messages pass through a UC Volume because DBFS is unavailable on serverless, so Unity Catalog is required. Dagster still submits the job (jobs.SubmitTask) and holds the materialization record. Costs and exit cost: protocol coupling in the external code has to be removed or wrapped later. A lighter variant on the same page triggers existing jobs with WorkspaceClient.jobs.run_now and has no dagster_pipes dependency. The same pattern works with Google Cloud Functions over HTTP, where the external code needs only the lightweight dagster-pipes library. The official docs say the pipes client is optional and the external code does not have to know anything about Dagster.

**Evidence:** Documented: vendor docs 1.13.27, votes 3-0 and 3-0, no preview label. The Xebia tutorial (updated 2026-01-28, no Dagster version) passed 2-1, is tutorial-grade, and uses private dagster-pipes helpers, which is an upgrade risk (inferred). The serverless page does not cover asset checks, though the general Pipes API has report_asset_check.

**Sources:** https://docs.dagster.io/integrations/libraries/databricks/pipes/serverless-compute, https://dagster.io/docs/guides/build/external-pipelines, https://xebia.com/blog/how-to-use-dagster-to-orchestrate-google-cloud-functions/

### F9 (medium, votes 3-0, 3-0)

RQ4 handoff contract, object drop + delivery-level completion marker. People Data Labs puts a single top-level COMPLETED file in the parent folder of each delivery (S3, Snowflake, Azure, GCP, Direct Download). It is created only after the full delivery and means all files are delivered and no more will be added. Per-subdirectory _SUCCESS markers 'can appear before the overall delivery is complete' and must not trigger ingestion. If COMPLETED is missing, do not ingest partial data; contact support. The Databricks/Delta Sharing delivery has no marker. The precedent does not cover a manifest, checksums, file counts, replay, ordering, or corrections after COMPLETED. Failure mode (inferred): triggering on partial-directory markers ingests incomplete data.

**Evidence:** Documented: vendor docs, undated and unversioned, fetched 2026-10-27. Votes 3-0 and 3-0. Single vendor. 'Spark/Hadoop style' is the claimant's label, not the vendor's.

**Sources:** https://docs.peopledatalabs.com/docs/data-license-ingestion

### F10 (medium, votes 3-0, 3-0, 3-0)

RQ4 handoff contract, object drop + manifest with integrity evidence. MX SFTP delivery sends a PGP-encrypted CSV manifest per batch (client_guid.snapshot_date-manifest.csv.pgp) with one row per daily file: FileName, Checksum (SHA-256), FileSize, EncryptedFileSize, RecordCount, EffectiveDate, ResourceType, EventType. A resource with no data for a day still gets an Avro file with headers and no body. Inferred: the receiver can check completeness and integrity against the declared file list, keep the manifest as audit evidence of what was received, and tell an empty day (file plus row with RecordCount 0) from a missing delivery. The page states no purpose for the manifest, no ordering or timing guarantee, and no signal for late or missing deliveries. MX has halted SFTP enablement for new integrations, so this is a legacy precedent, not an option available today.

**Evidence:** Documented: vendor docs, undated and unversioned; example data dated 2020-06-14, so possibly older than 2 years. Votes 3-0 x3. The completeness and evidence uses are inferred. It is unclear whether the checksum covers plaintext or ciphertext.

**Sources:** https://docs.mx.com/api-reference/more-apis/reporting/sftp-delivery

### F11 (high, votes 3-0, 3-0)

RQ4 where Temporal fits on the acquisition side. Self-hosted Temporal defaults: payload blob warns at 512 KB and errors at 2 MB, gRPC messages and history transactions cap at 4 MB, and event history warns at 10 MB / 10,240 events and terminates at 50 MB / 51,200 events (configurable via dynamic config). Inferred design constraints: delivery bytes must go to object storage, with workflows passing only references and manifests (claim-check pattern). Long-lived per-feed acquisition workflows, such as intraday polling, need Continue-As-New or splitting. Early warning sign: history-size or blob-size warnings. Temporal Cloud limits are on a separate page that was not checked.

**Evidence:** Documented: Temporal docs ('Self-hosted Temporal Service defaults', 2026), no product version, fetched 2026-10-27. Votes 3-0 and 3-0. The design consequences are inferred.

**Sources:** https://docs.temporal.io/kb/temporal-platform-limits-sheet/

### F12 (medium, votes 3-0, 3-0)

RQ5 topology, per Dagster's own guidance (Dagster+ Hybrid page, docs 1.13.27). A single repository with several projects is simple and makes code sharing easy, but all projects share one CI/CD pipeline and cannot deploy independently, and shared dependencies can conflict. Multiple repositories give stronger isolation, with per-project CI/CD, independent deploys and separately managed dependencies, at the cost of coordinating package publishing to share code. This describes the setup the page assumes, not a hard technical limit: the same page suggests limiting CI/CD to the relevant code locations. A related claim, that each code location builds into its own image with a per-location tag, was refuted 0-3.

**Evidence:** Documented: vendor guidance, docs 1.13.27, no publication date, Dagster+ section. Votes 3-0 and 3-0. A pros/cons list, not outcome evidence. There is no data on what breaks first at what scale.

**Sources:** https://docs.dagster.io/deployment/dagster-plus/management/managing-multiple-projects-and-teams

## Refuted

- (0-3) Direct invocation does not work for multi-assets with upstream assets: input_values cannot be used for them. The docs instead require defining source assets plus a mock IO manager and running execute_in_process, which exercises Dagster's in-process execution engine rather than pure Python. [https://docs.dagster.io/concepts/testing]
- (1-2) In Dagster+ (Dagster Cloud), the agent and code location versions can be upgraded independently. This supports decoupling the orchestrator upgrade from pipeline code deploy units (RQ2/RQ5). The page gives no product version. [https://support.dagster.io/articles/7616463479-can-the-dagster-cloud-agent-and-code-location-versions-be-different]
- (0-3) Each code location is defined by build.yaml, container_context.yaml and pyproject.toml. It is built from its own directory into its own Docker image with its own image tag, and the deploy workflow sets an image tag per code location by name. This allows per-location deployment units, which bears on 'adding a feed = releasing one image with all feeds'. [https://docs.dagster.io/deployment/dagster-plus/management/managing-multiple-projects-and-teams]

## Caveats

Evidence grade: every surviving claim is documented (vendor docs, changelogs, support FAQ, vendor blogs) or tutorial-grade (Xebia). None is a first-hand practitioner report or case study with an outcome. That gap matters most for RQ2 (real migrations into Databricks, dual running), RQ5 (what breaks first at what scale) and RQ6.

Coverage gaps: no claim on Databricks Lakeflow Jobs, Lakeflow Declarative Pipelines (DLT), Unity Catalog or Delta survived. The Databricks side rests only on Dagster's Pipes docs, so all Databricks feature versions, GA status and exit costs are still unestablished. RQ6 (the capability-to-layer reference table) and the DQ-semantics split (dbt tests vs orchestrator checks vs validators) have no verified evidence. Neither do schedules, cursors, partitions and asset-check state placement, beyond run storage and component state.

Dates and versions: Dagster docs were read at 1.13.27 (2026-10-27). One verifier saw the docs index list 1.13.8, an inconsistency that was not resolved. 1.9.0 (about 2024-10) is roughly 2 years old. The 1.11 blog (2025-06-26) is more than a year old. The PDL and MX pages are undated, and MX may be older than 2 years and is a legacy channel. The Components lifecycle labels (stable in 1.11, GA blog 2025-09-18, GA in the 1.12 changelog with 'previously Release Candidate') do not agree; the 1.12 changelog is the most authoritative.

Scope: the compatibility rule (claim 7) and repo-topology guidance are Dagster+ Hybrid sources, and applying them to Dagster OSS is inference. The Temporal limits are self-hosted defaults.

Inference: exit-cost statements, the completeness and evidence uses of manifests, testing without an instance, and the Temporal design consequences are all inferred and labelled as such.

Refuted, kept for transparency: multi-asset direct-invocation limits (0-3), fully independent agent and code-location upgrades (1-2), per-code-location image builds from the multi-project page (0-3).

## Open questions

- How do real feed-by-feed migrations from Dagster (or Airflow) into Databricks Lakeflow Jobs / Lakeflow Declarative Pipelines work out when both orchestrators write to the same storage? Settling this needs first-hand case studies with outcomes, plus current Databricks docs with versions and GA status (Lakeflow Jobs triggers, file-arrival triggers, DLT/LDP expectations, and Unity Catalog support for external or DuckLake-adjacent tables).
- Which orchestrator state (schedules, sensor cursors, partitions, asset-check results, materialization history) can be exported or rebuilt when changing orchestrators, and which must therefore live outside the orchestrator, for example in an orchestrator-neutral delivery ledger in Postgres? Settling this needs Dagster storage/API docs for cursor and partition export, plus migration reports.
- Can per-feed deploy independence be achieved in Dagster OSS (multiple code locations, each with its own image and workspace.yaml entry under Kubernetes/GitOps), and at what cost in image count, version skew between the webserver/daemon and code servers, and supported skew window? The per-location image claim was refuted, so this needs Dagster OSS deployment docs and practitioner reports.
- Where should data-quality checks and the completeness decision sit (ingest core vs dbt vs orchestrator asset checks), and how do practitioners keep one semantics across layers? This needs the RQ6 capability-to-layer evidence that no verified source covered: platform engineering write-ups or case studies with outcomes.

## Sources fetched

| url | quality | angle | claims |
|---|---|---|---|
| https://docs.dagster.io/guides/build/assets/creating-asset-factories | primary | Orchestrator-neutral pipeline design and testability (RQ1/RQ3) | 4 |
| https://dagster.io/blog/dagster-1-11-build-me-up-buttercup | primary | Orchestrator-neutral pipeline design and testability (RQ1/RQ3) | 5 |
| https://docs.dagster.io/concepts/testing | primary | Orchestrator-neutral pipeline design and testability (RQ1/RQ3) | 5 |
| https://xebia.com/blog/how-to-use-dagster-to-orchestrate-google-cloud-functions/ | blog | Orchestrator-neutral pipeline design and testability (RQ1/RQ3) | 5 |
| https://reddit.sentinel-team.org/posts/1uf584g/snapshots/2026-07-10T21%3A50%3A27.00695Z | forum | Orchestrator-neutral pipeline design and testability (RQ1/RQ3) | 5 |
| https://docs.dagster.io/migration/upgrading | primary | Dagster version upgrades, components, code locations (RQ2/RQ3/RQ5) | 5 |
| https://dagster.io/blog/dagster-components-ga | blog | Dagster version upgrades, components, code locations (RQ2/RQ3/RQ5) | 5 |
| https://www.dagster.io/blog/dagster-1-12-monster-mash | primary | Dagster version upgrades, components, code locations (RQ2/RQ3/RQ5) | 5 |
| https://releases.sh/release/rel_aSQFP62NqOzBdq4Y19clK-1-13-0-core-0-29-0-libraries | secondary | Dagster version upgrades, components, code locations (RQ2/RQ3/RQ5) | 5 |
| https://dagster.io/blog/code-location-best-practices | blog | Dagster version upgrades, components, code locations (RQ2/RQ3/RQ5) | 5 |
| https://support.dagster.io/articles/7616463479-can-the-dagster-cloud-agent-and-code-location-versions-be-different | primary | Dagster version upgrades, components, code locations (RQ2/RQ3/RQ5) | 3 |
| https://www.databricks.com/blog/how-move-apache-airflowr-databricks-lakeflow-jobs | blog | Migration to Databricks Lakeflow with dual running (RQ2) | 5 |
| https://www.databricks.com/br/blog/from-airflow-to-lakeflow-data-first-orchestration | blog | Migration to Databricks Lakeflow with dual running (RQ2) | 5 |
| https://docs.dagster.io/integrations/libraries/databricks/pipes/serverless-compute | primary | Migration to Databricks Lakeflow with dual running (RQ2) | 5 |
| https://lakehouse-plumber.readthedocs.io/guides/ship/migrate-from-dlt.html | blog | Migration to Databricks Lakeflow with dual running (RQ2) | 5 |
| https://docs.peopledatalabs.com/docs/data-license-ingestion | primary | Ingest handoff contracts, completeness, evidence (RQ4/RQ6) | 5 |
| https://docs.mx.com/api-reference/more-apis/reporting/sftp-delivery | primary | Ingest handoff contracts, completeness, evidence (RQ4/RQ6) | 5 |
| https://docs.dagster.io/deployment/dagster-plus/management/managing-multiple-projects-and-teams | primary | Repo topology and compatibility for small data teams (RQ5) | 5 |
| https://community.databricks.com/t5/community-articles/monorepo-vs-multi-repo-for-databricks-asset-bundles-a-decision/td-p/165123 | forum | Repo topology and compatibility for small data teams (RQ5) | 5 |
| https://discourse.getdbt.com/t/should-i-have-an-organisation-wide-project-a-monorepo-or-should-each-work-flow-have-their-own/666 | forum | Repo topology and compatibility for small data teams (RQ5) | 5 |
| https://blog.rapidflare.ai/blog/temporal-ingestion-pipeline-part1/ | blog | Contrarian: costs of decoupling and Temporal on acquisition side | 5 |
| https://derivai.substack.com/p/learning-temporal-the-hard-way | blog | Contrarian: costs of decoupling and Temporal on acquisition side | 5 |
| https://docs.temporal.io/kb/temporal-platform-limits-sheet/ | primary | Contrarian: costs of decoupling and Temporal on acquisition side | 5 |
