# A3: Dual orchestrator running (feed-by-feed migration against one shared storage platform)

Grading key used throughout: **[first-hand]** = practitioner report or case study with a stated outcome; **[documented]** = vendor doc/spec with version and/or date; **[inferred]** = my reasoning, not from a source; **[lead]** = search extract only, full text not fetched or not reachable. Dates checked against today (2026-10-27); anything older than about 2 years is flagged **[>2y old]**. Feature status (GA/preview) is given only where the fetched page states it.

Research scope note: 24 tool calls. Full texts fetched: two Databricks blogs (Mar 2026, Dec 2025), YipitData blog (Dec 2022), Databricks docs for table-update and file-arrival triggers, Azure Databricks Iceberg REST doc, Dagster docs 1.13.27 (Airlift DAG-level observe/migrate, federation observe, Databricks integration overview, DatabricksWorkspaceComponent), DuckLake 0.3 blog and DuckLake 1.1 connecting doc, Lakebridge landing and Reconcile pages, Robinhood Airflow upgrade post (2019), and Google Cloud Composer Airflow 3 side-by-side migration doc. Unreachable: the Medium post "From chaos to clarity: AWS Airflow to Databricks" (HTTP 403). The old `docs.dagster.io/migration/airflow-to-dagster/airlift` landing page returned 404 at its new address.

## Q1: How is each feed's ownership switched over from one orchestrator to the other?

### Takeaway
The only switchover mechanics I found documented in full text are (a) **schedule toggling with a pause-old / static-start-date / unpause-new handshake**, used side by side in Airflow cluster migrations (Robinhood 2019; Google Cloud Composer, Airflow 2->3, doc updated 2026-10-26), and (b) **a per-DAG or per-task "proxied" flag kept in a YAML state file**, read by the old orchestrator (Dagster Airlift). Databricks' migration guidance (Mar 2026) says to migrate incrementally and to let the two coexist, but it gives no cutover mechanics. I found no full-text source for feature-flag, GitOps-driven or ownership-registry cutover between orchestrators. Those options appear below as inference.

### Cited Findings
- **[first-hand, >2y old]** Robinhood upgraded Airflow 1.7 to 1.10 by building a second production cluster beside the old one rather than upgrading in place ("We decided not to upgrade our Airflow cluster in place"). DAGs moved in batches, and "each DAG would exist in both clusters" during the migration, so a DAG could fall back to the old cluster. Outcome: "The migration took a couple of weeks, and we transitioned to the new cluster without any major issues or downtime." The post does not give a DAG count. Published 2019-08-09. — [Robinhood Newsroom](https://robinhood.com/newsroom/upgrading-scaling-airflow-at-robinhood/)
- **[first-hand, >2y old]** Robinhood's per-DAG cutover sequence: (1) pause the DAG on the old cluster after its latest run finishes, (2) add it to the new cluster with a static `start_date` set to the next execution date, (3) unpause it on the new cluster, with backfills disabled by default in the new cluster's `airflow.cfg`. — [Robinhood Newsroom](https://robinhood.com/newsroom/upgrading-scaling-airflow-at-robinhood/)
- **[documented, Google Cloud Composer doc, last updated 2026-10-26]** The side-by-side Airflow 2->3 migration procedure transfers "DAGs one by one". It sets `[core]dags_are_paused_at_creation=True` in the new environment so that "all new DAGs are paused by default", sets "a new static start date in DAGs that you transfer", tells you to "Pause the DAG in your Airflow 2 environment" and then unpause it in Airflow 3, and has you monitor the new environment before removing the old one. — [Google Cloud Composer: Migrate environments to Airflow 3 (side-by-side)](https://docs.cloud.google.com/composer/docs/composer-3/migrate-airflow-3)
- **[documented, Dagster docs 1.13.27]** In Airlift, ownership of execution is switched per DAG (or per task in the task-level variant) by a `proxied` flag in YAML files in an `airflow_dags/proxied_state` folder. The Airflow DAG file calls `proxying_to_dagster(...)` with that state. When `proxied: True`, the task runs as a `DefaultProxyTaskToDagsterOperator`, so Airflow keeps the schedule and hands execution to Dagster. The docs say you can "roll back by changing a single line of code in the Airflow DAG". Before you proxy, the assets must be executable in Dagster, and the docs recommend user acceptance tests in Dagster first and "separate packages for the Airflow and Dagster deployments". — [Dagster docs: DAG-level migrate (1.13.27)](https://dagster.io/docs/migration/airflow-to-dagster/dag-level-migration/migrate); proxied-state and operator details are a **[lead]** from search extracts of [task-level migrate](https://docs.dagster.io/migration/airflow-to-dagster/airlift-v1/task-level-migration/migrate) and the [Airlift reference](https://docs.dagster.io/integrations/airlift/reference)
- **[documented, Dagster docs 1.13.27]** The v1 Airlift pages say: "If you are just getting started with Airlift, we recommend using the new Airlift component" (`AirflowInstanceComponent`). — [Dagster docs: DAG-level observe](https://dagster.io/docs/migration/airflow-to-dagster/airlift-v1/dag-level-migration/observe)
- **[documented, Databricks blog 2026-03-18]** Databricks writes that "Most teams migrate incrementally rather than replacing Airflow wholesale" and that "Lakeflow Jobs is designed to coexist during migration". It suggests moving self-contained or event-driven workflows and file-arrival or data-driven triggers early, and leaving stable, mature Airflow pipelines alone at first. It describes no cutover, parallel-run or double-run mechanics. Jobs are defined as Python Asset Bundles, with mutators for per-environment settings. — [Databricks: How to move Apache Airflow to Databricks Lakeflow Jobs](https://www.databricks.com/blog/how-move-apache-airflowr-databricks-lakeflow-jobs)
- **[documented, Databricks blog 2025-12-01]** The closing advice is "the simplest next step is to migrate one workflow". The post has no coexistence or parallel-run guidance. — [Databricks: From Airflow to Lakeflow, data-first orchestration](https://www.databricks.com/br/blog/from-airflow-to-lakeflow-data-first-orchestration)
- **[lead]** Shadow or parallel runs with reconciliation: a Medium post (403, unreachable) reportedly ran a subset of workloads on Airflow and Databricks at once for 2 weeks with automated reconciliation, then made Databricks primary and Airflow secondary for 1 week before retiring Airflow. A consultancy page reportedly puts typical parallel runs at 2–6 weeks per wave. Neither was verified. — [Medium (unreachable)](https://medium.com/@nidhi2505/from-chaos-to-clarity-our-migration-journey-from-aws-airflow-to-databricks-fd6d95479394); [itechtions (not fetched)](https://itechtions.com/databricks-migration-case-studies/)
- **[documented, Lakebridge docs, no version or date shown, "Provided by Databricks Labs"]** Lakebridge Reconcile "validates data fidelity after migration by comparing your source system against the Databricks target". It offers schema, row (hash, no join key), data (join-key, per-column) and all report types. Listed sources are Oracle, Snowflake, SQL Server, Redshift, Teradata, BigQuery and Databricks. **PostgreSQL and DuckDB are not listed.** It runs as a job on serverless or on DBR 17.3+. — [Lakebridge Reconcile](https://databrickslabs.github.io/lakebridge/docs/reconcile/); [Lakebridge home](https://databrickslabs.github.io/lakebridge/)

### Inferences
Options catalogue for switchover. All entries are **[inferred]** unless a source is named.

- **S1. Schedule toggling, pause old then unpause new** (source pattern: Robinhood, Composer).
  - Mechanism: the feed is defined on both sides. Exactly one side's schedule or trigger is active at a time, and the handover happens at an interval boundary.
  - Requires: both definitions deployed, new-side paused-by-default, a static start or next-interval alignment, and backfill/catchup disabled.
  - Gives: simple, and it worked at Robinhood. Costs: manual per-feed steps, and the state lives in two UIs/APIs (Dagster schedule state and Databricks job `pause_status`), so the audit trail is split.
  - Failure modes: both unpaused (double run), both paused (missed interval), or catchup storms on first enable.
  - Early warning: the run count per feed per interval is not exactly 1 on the shared ledger or storage.
  - Exit cost: low.
- **S2. Proxied-state flag read by the old orchestrator** (Airlift pattern).
  - Mechanism: the old orchestrator keeps the schedule and delegates execution per feed based on a checked-in flag. Only one scheduler ever fires.
  - Requires: the old side must be able to call the new side, e.g. a Dagster schedule or sensor that calls Databricks `run_now`.
  - Gives: one scheduler (structurally no double schedule), rollback by flipping one line in Git, and a Git history of who switched what.
  - Costs: the old orchestrator stays on the critical path until a final "decommission" step moves the schedules.
  - Failure modes: the old orchestrator is down so nothing runs, or the flag is flipped before the new side is executable.
  - Early warning: delegated runs that fail at submit time.
  - Exit cost: moderate, because the schedules have to be re-homed at the end.
  - Note: Airlift itself is Airflow->Dagster only, so a Dagster->Databricks equivalent would be hand-built.
- **S3. Ownership registry/config table** (e.g. a Postgres table `feed_owner(feed_id, orchestrator, effective_from, changed_by)`).
  - Mechanism: both orchestrators read it, and GitOps can write it through migrations.
  - Gives: one auditable source of truth, and fits regulated audit needs. Costs: every job must check it, which overlaps with Q2 D3.
  - Failure modes: a stale cache, or a job that forgot the check.
  - Exit cost: low to moderate (drop the check after the migration).
- **S4. GitOps-driven cutover.**
  - Mechanism: a PR flips the feed's owner in config, and CD deploys a paused or unpaused Dagster schedule and a Databricks bundle with matching `pause_status`.
  - Gives: approval and an audit trail through PR history. Costs: CD lag between two deploy targets can leave a window where both or neither is active.
  - Early warning: drift between the Git-declared owner and the live schedule state.
- **S5. Shadow/parallel run with comparison.**
  - Mechanism: the new side writes to a shadow schema or table, outputs are compared (Lakebridge Reconcile would not cover a Postgres/DuckDB source as documented), and then ownership flips.
  - Costs: double compute, and comparison tooling for DuckLake vs Delta is self-built.
  - Failure modes: the shadow writes leak into published tables.
  - Exit cost: low.
- **S6. Strangler-fig at feed granularity.** This is the overall pattern behind both Databricks' "migrate incrementally / coexist" advice and Robinhood's "batches". S1–S5 are the per-feed switch mechanisms within it.

### Gaps
- I found no full-text practitioner report of a Dagster -> Databricks migration of any kind.
- I found no full-text report of a migration into Databricks from ADF, Control-M, Oozie or cron that describes cutover mechanics. The YipitData report (Q5) gives none.
- I found no first-hand source that uses feature flags (LaunchDarkly-style) or an ownership table for orchestrator cutover.
- Lakebridge: no orchestration-conversion capability was found on the landing or Reconcile pages, and support level, version and date are not stated.

## Q2: How is a double run of a feed prevented while both orchestrators are live?

### Takeaway
Documented practice relies on **making exactly one schedule active**: pausing on the old side, paused-by-default on the new side, a static start date, and catchup or backfill off. The Composer doc says plainly that a DAG enabled in both environments "runs its own copy". Robinhood also named **idempotency** as the backstop and said non-idempotent tasks needed special care. I found no full-text source describing cross-orchestrator leases or locks in a shared DB.

### Cited Findings
- **[documented, Composer doc 2026-10-26]** "If a DAG is enabled (not paused) in both environments, each environment runs its own copy of the DAG, as scheduled... This might lead to concurrent DAG runs for the same data and execution time." Catchup on transfer "might lead to a large number of DAG runs scheduled starting from the specified start date." — [Google Cloud Composer](https://docs.cloud.google.com/composer/docs/composer-3/migrate-airflow-3)
- **[first-hand, >2y old]** Robinhood prevented double runs and missed intervals with: pause old after the last run, a static `start_date` equal to the next execution date, unpause new, and backfills disabled by default. "Ideally, every task in a DAG would be idempotent". Non-idempotent tasks were handled carefully and reworked later. — [Robinhood](https://robinhood.com/newsroom/upgrading-scaling-airflow-at-robinhood/)
- **[documented, Databricks trigger docs, last updated 2026-10-02]** Table-update triggers have a "minimum time between triggers" ("The minimum time to wait to trigger a run after a previous run completes") and a "wait after last change" debounce. These limit repeat runs within Databricks only, not across orchestrators. — [Databricks: table update triggers](https://docs.databricks.com/aws/en/jobs/trigger-table-update)
- **[documented, Unity Catalog Iceberg REST doc, 2026-10-14]** "Unity Catalog blocks external engines from committing duplicate data files to the table". This is a file-level guard, not a run-level one. — [Azure Databricks: Access tables from Iceberg clients](https://learn.microsoft.com/en-us/azure/databricks/external-access/iceberg)

### Inferences
Options catalogue for double-run prevention. All entries are **[inferred]** unless a source is named.

- **D1. Disable schedules on the old side** (documented pattern).
  - Mechanism: as in Q1 S1.
  - Gives/costs: cheap, but it is a convention rather than an enforcement.
  - Failure mode: a GitOps redeploy of the old side re-enables the schedule.
  - Early warning: any run of a migrated feed on the old side.
  - Exit cost: none.
- **D2. Single-writer lease/lock in shared Postgres.**
  - Mechanism: at run start, each job takes a row lock or advisory lock keyed by `(feed_id, delivery_id)`, or inserts a lease row with an expiry.
  - Requires: both runtimes (Dagster on Kubernetes and Databricks job compute) can reach the Postgres instance. Databricks network egress to an in-cluster Postgres is a real dependency.
  - Gives: hard mutual exclusion. Costs: lease expiry tuning, and an orphaned lease when a run crashes.
  - Early warning: lease waits or timeouts showing up in logs.
  - Exit cost: low.
- **D3. Ownership table checked at run start.**
  - Mechanism: a job no-ops (and logs "skipped: not owner") if `feed_owner != self`.
  - Gives: an audit record of skips. It pairs with Q1 S3.
  - Failure mode: a check-then-act race during the flip. Mitigate by combining with D2.
- **D4. Idempotent writes keyed by delivery.**
  - Mechanism: each load is keyed by a delivery/business-date ID and written via MERGE or partition-overwrite, so a second run produces the same state. Robinhood names idempotency as the ideal.
  - Gives: correctness even if D1–D3 fail.
  - Costs: in DuckLake and Delta, a double write still creates extra snapshots or versions, so it is visible in time travel. That is good for audit but noisy.
  - Early warning: two snapshots for one delivery ID.
- **D5. Shared delivery ledger** (also Q3 X6).
  - Mechanism: a `deliveries(feed, delivery_id, status, run_by, run_id)` table with a unique constraint on `(feed, delivery_id, status='succeeded')`, so the second writer fails its commit.

### Gaps
- I found no first-hand report of a lease or lock shared across two different orchestrator products.
- I found no Dagster or Databricks doc that offers cross-system run deduplication.
- Whether a Databricks job can be paused declaratively via bundle `pause_status` in the same GitOps commit as a Dagster schedule change was not verified in this track.

## Q3: How are cross-feed dependencies handled when upstream and downstream sit on different orchestrators?

### Takeaway
Databricks' own guidance (Mar 2026, Dec 2025) is **data-first coordination**: downstream jobs start on table-update or file-arrival triggers instead of cross-DAG signals. But **table-update triggers watch only Unity Catalog tables** (Delta/Iceberg managed, Delta-backed external, MVs/STs, some views). So a DuckLake table written by Dagster cannot trigger a Databricks job directly. The usable cross-boundary hooks are a **file-arrival trigger on a UC volume or external location**, or **Dagster calling the Databricks Jobs API** (DatabricksWorkspaceComponent, preview). Dagster Airlift shows how to observe another orchestrator's runs as asset materializations via a polling sensor (federation tutorial, docs 1.13.27).

### Cited Findings
- **[documented, Databricks blog 2026-03-18]** File-arrival and table-update triggers are "not implemented via long-running sensors". "Trigger jobs on file arrivals or table updates whenever possible; use schedules only when you truly need them." Coordination across jobs goes through tables and files. A Run Job task is for cases "where job-to-job invocation is intentional". — [Databricks blog](https://www.databricks.com/blog/how-move-apache-airflowr-databricks-lakeflow-jobs)
- **[documented, Databricks docs, last updated 2026-10-02]** Table-update triggers support "Unity Catalog Delta and Iceberg managed tables, Unity Catalog external tables backed by Delta Lake", materialized views, streaming tables, UC views and metric views over supported tables, OpenSharing tables and views, and system tables. Views over federated tables or tables outside UC are **unsupported**. Limits: up to 10 tables per trigger, and 1,000 jobs with table-update triggers without file events. The run-as principal needs `SELECT`, `USE CATALOG` and `USE SCHEMA`. **The page does not state GA or preview.** — [Databricks: table update triggers](https://docs.databricks.com/aws/en/jobs/trigger-table-update)
- **[documented, Databricks docs, last updated 2026-10-07]** File-arrival triggers fire when new files land in a **UC volume or external location**. Checks run every minute on a best-effort basis and are recursive. Overwriting an existing filename does not trigger. Unity Catalog is required. Without file events: 50 jobs per workspace and up to 10,000 files in the location. With file events: no file limit. **GA/preview not stated on the page.** — [Databricks: file arrival triggers](https://docs.databricks.com/aws/en/jobs/file-arrival-triggers)
- **[documented, Dagster docs 1.13.27]** `DatabricksWorkspaceComponent` "discovers existing jobs, and exposes them as Dagster assets". "When materialized, the component triggers a job run via the Databricks API and monitors it to completion." It can filter by `job_ids`, map task keys to asset specs, and set `depends_on` overrides. Dependencies can be auto-detected from Delta table paths. **Status: "currently in preview. The API may change in future releases."** The page does not say whether it observes runs started outside Dagster. — [Dagster: DatabricksWorkspaceComponent](https://dagster.io/docs/integrations/libraries/databricks/databricks-workspace-component)
- **[documented, Dagster docs 1.13.27]** The Databricks integration lists five routes: Databricks Connect, Dagster Pipes ("Submit Databricks jobs and stream logs/metadata back to Dagster"), DatabricksAssetBundleComponent (reads `databricks.yml`), DatabricksWorkspaceComponent, and a Dagster+-only Databricks Connection that shows UC tables as external assets. — [Dagster: Databricks integration](https://dagster.io/docs/integrations/libraries/databricks)
- **[documented, Dagster docs 1.13.27]** Airlift federation observes two Airflow instances. `build_airflow_polling_sensor` polls an instance "for new runs", and "whenever there is a successful run of the `load_customers` DAG, there will be a materialization in the Dagster UI". Cross-instance lineage is declared with `replace_attributes(deps=[...])`. The polling interval is not stated. Triggering execution across instances is on a separate "Federate execution" page, which I did not fetch. — [Dagster: federation observe](https://dagster.io/docs/migration/airflow-to-dagster/federation/observe)
- **[lead]** The Airlift reference reportedly says Airlift supports peering multiple Airflow instances by calling `build_defs_from_airflow_instance` several times and merging. dagster-airlift reportedly supports only basic auth against Airflow. Some Airlift pages reportedly carry a "beta" label. None of this was verified in full text. — [Airlift reference](https://docs.dagster.io/integrations/airlift/reference); [Airflow component tutorial](https://docs.dagster.io/migration/airflow-to-dagster/airflow-component-tutorial)
- **[lead]** A Medium post on cross-cluster Airflow upgrades suggests a custom sensor that queries both clusters' metadata DBs. Not fetched. — [Medium: dependency across multiple Airflow clusters](https://faisal-22508.medium.com/dependency-across-multiple-airflow-clusters-3bcf374e7205)

### Inferences
Options catalogue for cross-orchestrator dependencies. All entries are **[inferred]** unless a source is named.

- **X1. Databricks table-update trigger.**
  - Works only when the upstream output is a UC table (Delta/managed Iceberg). With DuckLake storage, a Dagster-owned upstream would first need to publish or sync into UC, so the trigger does not cross a DuckLake/UC storage boundary.
  - Early warning: a downstream job runs on stale data, or never fires, because the upstream wrote to DuckLake only.
- **X2. Databricks file-arrival trigger on a "done/manifest" marker.**
  - Mechanism: a Dagster-owned upstream writes a new, uniquely named marker file into a UC volume or external location over the same object storage.
  - Requires: a UC external location over the bucket.
  - Failure mode: an overwritten marker name does not trigger (documented).
  - Gives: loose coupling.
- **X3. Dagster sensor or asset observing Databricks.**
  - Covers the reverse direction: a Databricks-owned upstream feeding a Dagster-owned downstream. The pattern mirrors Airlift's polling sensor, but no Databricks equivalent of Airlift was found.
  - Options: a custom sensor polling Jobs runs, or a sensor watching DuckLake snapshots / a ledger row. The Dagster+-only Databricks Connection exposes UC tables as external assets, which does not apply to Dagster OSS.
- **X4. run_now from the other side.**
  - Mechanism: Dagster calls Databricks `jobs.run_now` (directly via the SDK, or via DatabricksWorkspaceComponent, preview) after the upstream materializes.
  - Gives: Dagster stays the single control plane during migration (Airlift-like, see Q1 S2).
  - Costs: the downstream still depends on Dagster being up. The reverse direction (Databricks -> Dagster GraphQL launch) is custom.
- **X5. Airlift-style observation.** This is a precedent rather than a ready tool: Airlift is Airflow-specific.
- **X6. Shared delivery ledger table in Postgres.**
  - Mechanism: upstream writes `delivered(feed, delivery_id, ts)`, and downstream on either side polls or senses it.
  - Gives: an orchestrator-neutral and auditable record. Costs: polling, and it is custom code on both sides.
  - Early warning: ledger rows without a matching storage snapshot, or the reverse.

### Gaps
- I did not fetch the "Federate execution" Airlift page, so it is unconfirmed whether Dagster can trigger a downstream run in the other orchestrator via automation conditions.
- GA dates for table-update and file-arrival triggers were not found on the doc pages. Release notes were not checked.
- `Continuous` job triggers were not researched in full text.
- The Dagster Pipes on Databricks serverless details from the brief's lead (docs 1.13.27, dagster_pipes coupling, UC Volumes) were **not verified** in this track. Only the integration overview line was fetched.

## Q4: How do consumers stay unaware of which orchestrator produced a feed?

### Takeaway
Consumer-side indirection depends on where the data lands. If storage stays on DuckLake, both orchestrators must write the same DuckLake tables, and Databricks has no native DuckLake reader or writer in the sources I found. If Databricks writes to UC (Delta/Iceberg), consumers see a second catalog unless data is synced or bridged via Iceberg. Unity Catalog's Iceberg REST endpoint allows external **writes only to UC-managed Iceberg tables**. Foreign Iceberg and Delta tables are read-only through it. DuckLake 0.3+ can copy to and from Iceberg via DuckDB, which is a sync rather than a shared table.

### Cited Findings
- **[documented, Azure Databricks doc, updated 2026-10-14]** Through the UC Iceberg REST catalog (`/api/2.1/unity-catalog/iceberg-rest`), the table types behave as follows:

  | Table type | Read | Write |
  |---|---|---|
  | Managed Iceberg | Yes | Yes |
  | Foreign Iceberg | Yes | No |
  | Managed Delta (with Iceberg reads enabled) | Yes | No |
  | External Delta (with Iceberg reads enabled) | Yes | No |

  Foreign Iceberg tables are not refreshed automatically (`REFRESH FOREIGN TABLE` is needed), and credential vending is unsupported for them. Access requires "External data access" on the metastore and `EXTERNAL USE SCHEMA`. External clients cannot run table maintenance on managed Iceberg tables. — [Azure Databricks: Iceberg clients](https://learn.microsoft.com/en-us/azure/databricks/external-access/iceberg)
- **[documented, DuckLake blog 2025-09-17, v0.3 with DuckDB 1.4.0]** "it is possible to copy data between DuckLake and Iceberg using a shallow copy operation". Iceberg->DuckLake supports metadata-only copy including snapshot history. DuckLake->Iceberg works "given that the schemas are already created in Iceberg". `COPY` does not replace existing tables. Spark, Databricks and Delta are not mentioned. — [DuckLake 0.3](https://ducklake.select/2025/09/17/ducklake-03/)
- **[documented, DuckLake 1.1 docs, undated, (c) 2026]** The documented client is the DuckDB `ducklake` extension via `ATTACH`. Catalogs can be DuckDB, SQLite, PostgreSQL or a Quack server, and data can live on local or S3 paths. No Spark or Databricks client is listed. — [DuckLake: connecting](https://ducklake.select/docs/stable/duckdb/usage/connecting)
- **[lead]** MotherDuck documents a DuckLake Spark connector that is append-only and write-only, with target tables required to exist. Not fetched. — [MotherDuck: Databricks integration](https://motherduck.com/docs/integrations/databases/databricks/)
- **[documented, Databricks docs 2026-10-02]** Table-update triggers do not support views over federated or non-UC tables (see Q3). So a UC view that hides a foreign source would also lose trigger-based orchestration. — [Databricks: table update triggers](https://docs.databricks.com/aws/en/jobs/trigger-table-update)

### Inferences
Options catalogue for consumer unawareness. All entries are **[inferred]** unless a source is named.

- **C1. Stable published tables/views with same names and schemas.**
  - Mechanism: consumers read `published.<feed>` views, and the producer behind them swaps.
  - In DuckLake this works if both orchestrators write DuckLake. For Databricks that means running DuckDB/DuckLake code inside Databricks jobs (e.g. Python tasks), not native Spark/UC.
  - Failure mode: schema drift between the two producers' dbt models.
  - Early warning: contract test failures.
- **C2. Data contracts** (dbt model contracts, schema tests) enforced identically on both sides. Same dbt project, different runners.
- **C3. Write-audit-publish.**
  - Mechanism: write to staging, audit (row counts, reconciliation against the old producer), then publish by swapping a view or snapshot pointer.
  - Gives: an audit artefact per delivery, which suits a regulated firm, and it doubles as the comparison step of Q1 S5.
- **C4. Catalog-level indirection.**
  - If storage moves to UC, consumers point at UC names, and DuckLake data could be synced in (Iceberg copy via DuckDB, then a UC foreign or managed Iceberg table).
  - Costs: two copies, refresh lag on foreign tables (documented manual `REFRESH FOREIGN TABLE`), and an audit-trail split across two catalogs.
  - Exit cost: high if both catalogs persist.
- **C5. One-way bridge with UC as the writer.** Managed Iceberg in UC is writable by external engines (documented), so DuckDB-based Dagster jobs could in principle write UC-managed Iceberg tables via Iceberg REST and keep a single catalog. Whether DuckDB's iceberg extension supports writes against UC's endpoint was not verified.

### Gaps
- I found no source confirming that Databricks can read or write a DuckLake (Postgres-catalogued) lake natively. The conclusion that **data must be synced or bridged via Iceberg** is inference from the absence of any such client in the DuckLake and Databricks docs fetched.
- Unity Catalog Lakehouse Federation to PostgreSQL (query federation of the Postgres DB itself, read-only) was not researched in full text.
- DuckDB writes to the UC Iceberg REST endpoint are unverified.

## Q5: What did real migrations (into Databricks, Airflow->Dagster via Airlift, Airflow 1->2 side-by-side) report about cutover, double runs, cross-orchestrator dependencies, timelines and outcomes?

### Takeaway
The verified record is thin. **YipitData** (vendor-co-published, 2022) moved more than 600 Airflow DAGs to Databricks Workflows with a scripted conversion and called it "relatively smooth", without describing cutover. **Robinhood** (2019) is the clearest first-hand account of two orchestrator clusters run side by side, with a per-DAG pause/unpause handshake, a couple of weeks' duration and no downtime. **No first-hand Airlift migration outcome was found.** Dagster customer stories surfaced in search do not confirm Airlift use.

### Cited Findings
- **[first-hand, vendor-co-published (Databricks blog, YipitData engineering manager co-author), >2y old, 2022-12-07]** YipitData had "over 600 DAGs" active in Airflow and up to 8,000 tasks a day. Tasks were already Databricks notebooks, so the work was "creating a workflow instead of an Airflow DAG". "Using the Databricks APIs, we created a script to automate most of the migration process." Outcome: "relatively smooth"; "we would dedicate several FTEs to maintain our Airflow infrastructure which is now unnecessary". There is no description of parallel running, cutover, double-run prevention or cross-orchestrator dependencies, and no cost or runtime numbers. — [Databricks/YipitData](https://databricks.com/blog/why-we-migrated-apache-airflow-databricks-workflows-yipitdata)
- **[vendor-published claim]** The Dec 2025 Databricks blog attributes "60 percent reduction in database costs and 90 percent faster processing" to YipitData. This figure does not appear in the 2022 YipitData post. — [Databricks blog 2025-12-01](https://www.databricks.com/br/blog/from-airflow-to-lakeflow-data-first-orchestration)
- **[first-hand, >2y old, 2019-08-09]** Robinhood ran Airflow 1.7 -> 1.10 side by side, moving DAGs in batches with each DAG present in both clusters. The handshake was pause old, static start date, unpause new, backfills off. It took "a couple of weeks" with no major issues or downtime. Afterwards they added a canary DAG every 10 minutes and SLAs (scheduler downtime at most 10 minutes, QUEUED at most 15 minutes). — [Robinhood](https://robinhood.com/newsroom/upgrading-scaling-airflow-at-robinhood/)
- **[documented]** The Google Cloud Composer side-by-side Airflow 2->3 procedure (2026-10-26) is a current vendor equivalent of the Robinhood handshake (see Q1 and Q2). — [Composer](https://docs.cloud.google.com/composer/docs/composer-3/migrate-airflow-3)
- **[lead]** AWS Airflow -> Databricks: a 2-week dual run with automated reconciliation, then 1 week of Databricks primary / Airflow secondary, then retirement (Medium, 403). Separately, GetYourGuide reportedly ran a 2-week parallel run for BI cutover, which concerned query latency rather than orchestration. Neither was verified. — [Medium (unreachable)](https://medium.com/@nidhi2505/from-chaos-to-clarity-our-migration-journey-from-aws-airflow-to-databricks-fd6d95479394); [itechtions roundup (not fetched)](https://itechtions.com/databricks-migration-case-studies/)
- **[lead, vendor-published]** Dagster case-study listings (smava: zero downtime and more than 1,000 dbt models; Magenta Telekom: onboarding from months to one day; HIVED: 99.9% reliability) did not establish that Airlift was used. Not fetched. — search extract, see [Airlift tutorial](https://docs.dagster.io/integrations/airlift/tutorial)

### Inferences
- **[inferred]** Across Robinhood, Composer and Airlift, the common rule is: **exactly one active scheduler per feed at any moment, switched at an interval boundary, with idempotent writes as the backstop**. None of the verified reports describes a cross-orchestrator lock.
- **[inferred]** The YipitData case is weak evidence for this context: its tasks already ran on Databricks compute, so only the scheduler moved, not storage or code.

### Gaps
- No verified migrations into Databricks from Dagster, ADF, Control-M, Oozie or cron with cutover detail.
- No verified Airlift migration with a stated outcome.
- No verified Airflow -> Prefect parallel-run report.
- No Data+AI Summit or Airflow Summit talks were fetched.

## Q6: Status, versions and dates of the Databricks and Dagster features relevant to dual running

### Takeaway
As of the pages fetched in October 2026:
- **Databricks:** table-update triggers (doc updated 2026-10-02) and file-arrival triggers (2026-10-07) are documented without a GA/preview label on the page. The UC Iceberg REST endpoint gives read/write for managed Iceberg only (2026-10-14). Lakebridge is a Databricks Labs toolkit (Assessment, Transpiler, Reconciler) with no documented orchestration converter.
- **Dagster:** docs are at 1.13.27. DatabricksWorkspaceComponent is **preview**. The Airlift v1 API docs steer new users to the Airlift component.

### Cited Findings
- **[documented]** Table-update trigger page last updated 2026-10-02; no GA/preview statement. — [Databricks](https://docs.databricks.com/aws/en/jobs/trigger-table-update)
- **[documented]** File-arrival trigger page last updated 2026-10-07; no GA/preview statement. — [Databricks](https://docs.databricks.com/aws/en/jobs/file-arrival-triggers)
- **[documented]** Azure Databricks Iceberg REST doc dated 2026-10-14. A legacy read-only Iceberg REST endpoint also exists. — [Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/external-access/iceberg)
- **[documented]** Lakebridge is "Provided by Databricks Labs", with no version or support level shown. Reconcile runs on serverless or DBR 17.3+. — [Lakebridge](https://databrickslabs.github.io/lakebridge/); [Reconcile](https://databrickslabs.github.io/lakebridge/docs/reconcile/)
- **[documented]** Dagster docs show "Latest (1.13.27)", with archives 1.12.8, 1.11.16, 1.10.21 and 1.9.13. — [Dagster DAG-level observe](https://dagster.io/docs/migration/airflow-to-dagster/airlift-v1/dag-level-migration/observe)
- **[documented]** "DatabricksWorkspaceComponent is currently in preview. The API may change in future releases." — [Dagster](https://dagster.io/docs/integrations/libraries/databricks/databricks-workspace-component)
- **[documented, blog]** Lakeflow Jobs was formerly Databricks Workflows. Databricks claims a 99.95% uptime SLA and "no orchestration surcharge" (vendor claims). — [Databricks blog 2025-12-01](https://www.databricks.com/br/blog/from-airflow-to-lakeflow-data-first-orchestration)

### Inferences
- **[inferred]** Because Lakebridge Reconcile does not list PostgreSQL or DuckDB as sources, it would not run out of the box against a DuckLake-on-Postgres source. A self-built comparison (e.g. DuckDB reading both sides) would be needed for shadow runs.

### Gaps
- GA dates for table-update triggers, file-arrival triggers and continuous jobs were not found. The Databricks release notes would be the place to check.
- The dagster-airlift and dagster-databricks package versions on PyPI were not checked. The only PyPI hit was dagster-airlift 0.0.5, which is old.
- The supported Airflow versions for Airlift were not found.
- Lakeflow Declarative Pipelines' role in dual running was not researched.
