# A1-A4: Where a data-ingestion platform's operational state should live, and what is lost if it moves out of the orchestrator

Scope: options catalogue for seven state kinds (gate verdicts, delivery landed, deadline/arrival, operator acknowledgements, discovery cursors, concurrency limits, schedules/backfill progress). This is an options study, with no overall recommendation or ranking.

Grading used on every line: **[first-hand]** = practitioner report/case study with an outcome; **[documented]** = vendor doc/spec, with product version/date; **[inferred]** = my reasoning; **[lead only]** = search snippet, not fetched, not usable as verdict evidence; **[unreachable]**.

All docs were fetched in full on 2026-10-27, and Dagster/Databricks dates come from the pages or the changelog. Dagster release dates come from the PyPI JSON (`pypi.org/pypi/dagster/json`). The latest Dagster release was **1.13.27 (2026-10-26)**. The docs.dagster.io pages are unversioned "latest" docs, so I take them to describe 1.13.x.

Source-quality caveat, stated up front: **I found no first-hand practitioner report (with an outcome) on moving operational state out of Dagster or into a ledger.** Practitioner patterns below are backed by vendor/framework documentation (ADF, BimlFlex, dbt) and by search leads only. Every "first-hand" slot is therefore empty, and the report writer should not upgrade any of these claims.

---

## A1: For each state kind, options for where it lives, their costs, and named practitioner patterns

### Takeaway
Each of the seven state kinds can live in three places: (a) the orchestrator's event log/instance DB (status quo), (b) a platform-owned ledger in Postgres (control/watermark/delivery/check-result/waiver tables, an established ETL pattern documented by ADF and BimlFlex), or (c) derived from the data itself (DuckLake snapshot metadata, object-store listings, the kept delivery bytes). The orchestrator-native options are the cheapest today and the most expensive to exit. Dagster ties blocking to a single run, and Databricks has no equivalent of cross-run check verdicts, materialisation records or cross-job named pools. Ledger options cost build and maintenance effort but are the only ones both orchestrators can read during a dual-run migration.

### Cited Findings

**Dagster: what the orchestrator natively holds (as of 1.13.x, docs fetched 2026-10-27)**
- [documented] Blocking checks: "By default, if a parent's asset check fails during a run, the run will continue and downstream assets will be materialized. To prevent this behavior, set the blocking argument to True in the @asset_check decorator." The doc example blocks the downstream asset "if the ... check fails". The doc scopes this to "during a run", so it does not cover a later re-execution. — [Dagster docs: Asset checks](https://docs.dagster.io/guides/test/asset-checks)
- [documented] Partitioned asset checks are labelled **"Preview feature ... not considered ready for production use"** on the docs page, though the changelog lists them as a 1.13.0 headline feature (1.13.0 released 2026-04-09). The check's `partitions_def` must equal the asset's. — [Dagster docs: Asset checks](https://docs.dagster.io/guides/test/asset-checks); [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] Failure-mode evidence for in-orchestrator gates, from Dagster 1.13.7 (2026-05-28): "Fixed a regression where a blocking asset check that did not emit a result (e.g. a dbt test that dbt declined to run under `indirect_selection: cautious` or `buildable`) could silently cause downstream assets to be skipped. Missing blocking check results now allow downstream assets to proceed." In other words, the semantics of a *missing* verdict changed across patch releases, and missing results now let downstream proceed. — [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] dagster-dbt, "Changes since 1.10.21" (1.10.x line, between 1.10.0 on 2025-02-13 and 1.11.0 on 2025-06-26): "dbt tests with error severity are now modeled as blocking asset checks, ensuring that if a run fails due to a dbt test failure, the connected model is included in a retried run if it is retried using the experimental 'Enable retries from asset failure' feature." Re-execution semantics for blocking checks are tied to an **experimental** retry mode. — [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] `AutomationCondition.all_deps_blocking_checks_passed` was added in 1.8.12 (2024-10-17; **about 2 years old, so flag it**). It "can be used to prevent materialization when any upstream blocking checks have failed". This is a cross-run gate, but only inside Declarative Automation. Declarative Automation itself became "no longer experimental" in 1.8.0 (2024-08-08; **older than 2 years**). — [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] FreshnessPolicy (new API) was introduced in 1.10.0 (2025-02-13). The changelog's "Major changes since 1.11.0" (i.e. the 1.12 line, 1.12.0 released 2025-10-30) says "**FreshnessPolicies GA** ... now marked as GA (previously Preview)". **Conflict:** the current docs page still says "Freshness policies are under active development. You may encounter feature gaps and the APIs may change" and "Freshness policies are not enabled by default while in preview", and requires `freshness: enabled: True` in `dagster.yaml` for OSS. Policy types are `FreshnessPolicy.time_window(fail_window, warn_window)` and `FreshnessPolicy.cron(deadline_cron, lower_bound_delta, timezone)`. "Freshness policies have superseded freshness checks since the 1.12 release." Minimum resolution is 1 minute. Freshness is evaluated purely from *materialisation timestamps*: "If the asset has not materialized in the window after the deadline passes, it will fail freshness." — [Dagster docs: Asset freshness policies](https://docs.dagster.io/guides/observe/asset-freshness-policies); [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] Sensor cursors are a single string: `context.cursor` / `context.update_cursor(str(max_mtime))`. "For sensors that consume multiple event streams, you may need to serialize and deserialize a more complex data structure in and out of the cursor string." — [Dagster docs: Sensors](https://docs.dagster.io/guides/automate/sensors)
- [documented] Tick retention is configurable in `dagster.yaml` (`retention: schedule: purge_after_days: 90` in the example), so schedule/sensor tick history is purgeable orchestrator state. — [Dagster docs: OSS instance configuration](https://docs.dagster.io/deployment/oss/oss-instance-configuration)
- [documented] Concurrency pools: assign with `@dg.asset(pool="database")`. Set the limit via the UI (Deployment → Concurrency) or `dagster instance concurrency set database 1`. `dagster.yaml` takes `concurrency: pools: default_limit:` and `granularity: 'run'` (vs. op-level). Pools are "ideal for protecting shared resources like databases or APIs" and limit "in progress op executions across all runs". — [Dagster docs: Concurrency pools](https://docs.dagster.io/guides/operate/managing-concurrency/concurrency-pools); [Managing concurrency](https://docs.dagster.io/guides/operate/managing-concurrency)
- [documented] Pool history: 1.9.12 (2025-02-10) distinguishes explicit from default pool limits and "Requires a schema migration using `dagster instance migrate`". The 1.10 major changes made "run blocking ... on by default for concurrency pools". 1.12.9 (2026-01-08) added a helm `concurrency` setting. 1.13.22 (2026-09-11) made dequeuing faster "as pool state is read once per dequeue pass". Pool limits are therefore stateful instance-DB rows whose schema moves between versions. — [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] Backfills are launched from the UI ("Materialize" on Asset details or Global asset lineage) for partitioned assets, "as long as the most upstream assets share the same partitioning". — [Dagster docs: Backfilling data](https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data)

**Databricks Lakeflow Jobs: where equivalent state can sit (docs fetched 2026-10-27)**
- [documented] Task values: `dbutils.jobs.taskValues.set()/get()`, Python notebooks only for set/get. Other task types reference values via `{{tasks.<task_name>.values.<value_name>}}`. Values must be JSON and ≤ **48 KiB**. Their stated purpose is "to pass arbitrary values between tasks in a Databricks job". Page last updated Oct 8, 2026. — [Databricks: task values](https://docs.databricks.com/aws/en/jobs/task-values)
- [documented] "Databricks retains run history for **60 days** for both jobs and pipelines ... If you need to preserve job runs, Databricks recommends exporting results before they expire." Last updated Oct 15, 2026. — [Databricks: monitor jobs](https://docs.databricks.com/aws/en/jobs/monitor)
- [documented] `system.lakeflow` (formerly `workflow`) holds six job tables, including `jobs`, `job_tasks`, `job_run_timeline` and `job_task_run_timeline`, with **365-day free retention**. The tables are regional ("records from all workspaces in your account deployed in the same cloud region"). `job_run_timeline` carries `trigger_type`, `run_type`, `result_state`, `termination_code` and `job_parameters`. SCD2 tables retain the latest record per entity beyond 365 days. Last updated Oct 16, 2026. No preview banner appeared in the fetched text. — [Databricks: Jobs system table reference](https://docs.databricks.com/aws/en/admin/system-tables/jobs)
- [documented] File arrival triggers monitor "a Unity Catalog external location or volume". They "make a best effort to check for new files every minute". File events on the external location are recommended, and there is a "Minimum time between triggers" cooldown. Last updated Oct 7, 2026. — [Databricks: file arrival triggers](https://docs.databricks.com/aws/en/jobs/file-arrival-triggers)
- [documented] Table update triggers fire on updates to Unity Catalog Delta/Iceberg managed tables, UC external Delta tables, MVs, streaming tables, OpenSharing and system tables, with Any/All semantics and a minimum interval. Last updated Oct 2, 2026. — [Databricks: table update triggers](https://docs.databricks.com/aws/en/jobs/trigger-table-update)
- [documented] Concurrency is per job ("maximum number of concurrent runs", default one) plus workspace-level limits. Queueing holds runs "for up to 48 hours", and is on by default for UI-created jobs after April 15, 2024. Last updated Sep 11, 2026. — [Databricks: configure job](https://docs.databricks.com/aws/en/jobs/configure-job); [Databricks: backfill jobs](https://docs.databricks.com/aws/en/jobs/backfill-jobs)
- [documented] Backfill jobs: "A backfill runs your job multiple times with different parameters" over a date range split by an interval. "The job must handle the parameters that you give it to process the correct data for the backfill date range." Last updated Sep 11, 2026. No preview banner in the fetched text. — [Databricks: backfill jobs](https://docs.databricks.com/aws/en/jobs/backfill-jobs)

**Named practitioner patterns (vendor/framework documentation; no first-hand outcomes found)**
- [documented] **Watermark / high-water-mark control table** (Azure Data Factory template; ms.date 2024-10-03, updated 2026-08-05): "an external control table that stores a high-watermark value". The steps are: Lookup old watermark → Lookup current watermark → copy `WHERE TIMESTAMP_Column > last AND <= current` → stored procedure "writes the current high-watermark value to an external control table". The watermark lives outside the orchestrator by design. — [Microsoft Learn: Delta copy with a control table](https://learn.microsoft.com/en-us/azure/data-factory/solution-template-delta-copy-with-control-table)
- [documented] **Audit / row-count / execution tables in a customer-owned DB** (Varigence BimlFlex blog, 2026-06-19, vendor). Tables are `bfx.RowCount(RowCountID, ExecutionID, ComponentName, ObjectName, CountType, RowCount, ColumnSum, ColumnName, AuditDate)`, `bfx.AuditRow`, `bfx.AuditRowData`, plus an execution record with parent/child relationships, start/end and Duration. Quotes: "Nothing leaves your environment, and nothing depends on a vendor runtime staying online to read it later." "A dashboard reads evidence; it does not create it." The post cites no regulation. — [Varigence: row-level reconciliation audit evidence](https://www.varigence.com/blog/row-level-reconciliation-audit-evidence-bimlflex-writes-to-your-own-database)
- [documented] **dbt `store_failures` is not a history**: "A test's results will always replace previous failures for the same test, even if that test results in no failures." The default schema is `{{ profile.schema }}_dbt_test__audit`. Last updated Jul 18, 2026. — [dbt docs: store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures)
- [documented] **dbt `run_results.json`** is per invocation, "only executed nodes appear", and "many run_results.json can be combined to calculate average model runtime, test failure rates", so history exists only if someone persists the artifacts. — [dbt docs: run_results.json](https://docs.getdbt.com/reference/artifacts/run-results-json)
- [documented] **DuckLake snapshot metadata as derived state**: `ducklake_snapshot(snapshot_id, snapshot_time, schema_version, ...)` and `ducklake_snapshot_changes(snapshot_id, changes_made, author, commit_message, commit_extra_info)`. `CALL my_ducklake.set_commit_message('Pedro', 'Inserting myself', extra_info => '{...}')` attaches author/message/extra info inside a transaction. The docs also have an "Expire Snapshots" operation and note "Configuration changes are not snapshot-versioned". (DuckLake "stable" docs; I did not capture the version number.) — [DuckLake spec: ducklake_snapshot](https://ducklake.select/docs/stable/specification/tables/ducklake_snapshot); [ducklake_snapshot_changes](https://ducklake.select/docs/stable/specification/tables/ducklake_snapshot_changes); [DuckLake: snapshots](https://ducklake.select/docs/stable/duckdb/usage/snapshots)
- [lead only] **Audit-Balance-Control (ABC)** framework: batch ID = run date YYYYMMDD + 2-digit sequence; audit table of start/end and rows inserted/updated/rejected per step; "control" = restartability from point of failure. These come from search snippets only (devgenius, XTIVIA, patent US11625371) and were not fetched. — [XTIVIA](https://www.xtivia.com/blog/etl-audit-balance-control-recommendations/); [DevGenius ABC](https://blog.devgenius.io/abc-of-data-platform-implementation-88307e43fe61); [US11625371B2](https://patents.google.com/patent/US11625371)
- [lead only] **Metadata-driven control table + audit table** (Microsoft Fabric "Demystifying data ingestion" blog, six components). **[unreachable]** (HTTP 403 on fetch). Snippet: control table decides which items move; audit tracks records and errors. — [Fabric blog](https://blog.fabric.microsoft.com/blog/demystifying-data-ingestion-in-fabric-fundamental-components-for-ingesting-data-into-a-fabric-lakehouse-using-fabric-data-pipelines)

### Inferences

All mechanisms below are **[inferred]** designs unless a line cites a source. Table sketches assume a Postgres `ops` schema on the platform's existing Postgres (the DuckLake catalog DB or a sibling). "Exit cost" is measured toward Databricks Lakeflow Jobs with both orchestrators running in parallel against the same storage.

**Shared spine, used by several options (inferred).** One identity key per delivery: `delivery_id` (UUID or a deterministic hash of feed_id + vendor-declared identifier + content sha256). Every other table references it. Without this key, gate verdicts, waivers and arrival decisions cannot be joined across orchestrators.

#### 1. Gate verdicts carried across re-executions
- **1a. Orchestrator-native (status quo): Dagster blocking checks + walking parent-run lineage.**
  - *Mechanism:* `@asset_check(blocking=True)`. Custom code walks `parent_run_id`/`root_run_id` to find a prior failed verdict.
  - *Requires:* Dagster run storage retained, plus custom lineage-walking code.
  - *Gives:* check UI, asset health, free storage.
  - *Costs:* Dagster natively blocks only "during a run" [documented, see above]. Cross-run carry is custom code over Dagster internals, or the experimental "retries from asset failure" path, or `all_deps_blocking_checks_passed` (Declarative Automation only).
  - *Failure modes:* a fresh, non-re-execution run (new launch, backfill, sensor) has no parent lineage, so the gate is bypassed. Semantics of missing results changed in 1.13.7, and missing now means "proceed" [documented]. Run purge/retention deletes the evidence.
  - *Early warning:* a downstream materialisation whose upstream's latest check is FAILED; a check row with no result.
  - *Exit cost:* high. Lakeflow has no cross-run check-verdict store. Task values are scoped to a job run and ≤48 KiB [documented], and run history expires at 60 days [documented].
- **1b. Platform ledger: check-result audit table + gate function.**
  - *Mechanism:* `ops.check_result(check_result_id, delivery_id, asset_key, partition_key, check_name, check_version, severity {block,warn}, passed bool, metric jsonb, evaluated_at, run_ref (orchestrator, run_id), code_version)`, append-only. Plus a view `ops.gate_state(delivery_id, asset_key, partition_key, blocked bool, reason)` = latest blocking result minus active waivers (see 4b). Every downstream step calls `assert_gate_open(delivery_id, asset)` before doing work, whichever orchestrator launched it.
  - *Requires:* discipline that *all* step entrypoints call the gate (a library in the shared Python package); write-once semantics.
  - *Gives:* re-execution, new runs and Databricks runs all see the same verdict; audit evidence of every check evaluation.
  - *Costs:* lose the native check UI unless mirrored (A4); the ledger needs build effort plus migrations.
  - *Failure modes:* a step that skips the gate call; clock/ordering bugs (latest-wins on `evaluated_at` vs. snapshot order); Postgres down blocks everything (fail-closed) or nothing (fail-open). That choice has to be made explicitly.
  - *Early warning:* materialisations without a matching `gate_open` audit row; a count of steps invoked without the gate.
  - *Exit cost:* low. Both orchestrators call the same function.
- **1c. Derived from data: verdict encoded in the lakehouse.**
  - *Mechanism:* the check writes its result as a DuckLake table row (`audit.check_results`), or quarantine-promote: the step writes to `staging`, and only a passing check promotes to the consumed table. The downstream reads only promoted data, so "blocked" = "not present". DuckLake `commit_extra_info` can carry check id/verdict [documented capability; use is inferred].
  - *Gives:* the gate holds whatever the orchestrator does; the data itself proves the gate held.
  - *Costs:* extra copy/promote step; "why blocked" is harder to explain; DuckLake snapshot expiry removes derived history [documented that expiry exists].
  - *Failure mode:* someone reads staging directly. *Early warning:* consumers querying staging schemas (catalog/query logs).
  - *Exit cost:* low-medium. Databricks must read DuckLake, or the promote logic is re-implemented.
- **Named patterns:** audit table of check results; quarantine/promote ("write-audit-publish", a pattern name I recall from memory, not fetched); dbt `store_failures` (overwrites, so it is not an audit trail [documented]).

#### 2. "Has this delivery landed?"
- **2a. Orchestrator-native:** materialisation records plus metadata (Dagster event log); external assets via sensor or `POST /report_asset_materialization/` [documented].
  - *Costs:* landing truth sits in an event log the other orchestrator cannot read. Dagster's REST endpoint on OSS needs no authentication ("Authentication headers aren't required if using Dagster OSS" [documented]), so anyone with network reach can forge "landed".
  - *Failure mode:* duplicate/ghost materialisations from re-runs, or a materialisation recorded without bytes kept.
  - *Exit cost:* high. Lakeflow has no asset-materialisation store. The closest is `job_run_timeline` (run-level, 365 days) [documented].
- **2b. Platform ledger: delivery/arrival ledger (a.k.a. inbound file register, batch/load register, manifest table).**
  - *Mechanism:* `ops.delivery(delivery_id PK, feed_id, source_kind {http,sftp,file}, source_ref (URL/path/vendor file id), vendor_declared_as_of, business_date, received_at, discovered_by (orchestrator,run_id|sensor), object_uri, byte_size, sha256, content_type, status {received, validated, loaded, rejected, superseded}, supersedes_delivery_id)`. Plus `ops.delivery_event(delivery_id, event {received,validated,loaded,...}, at, actor, run_ref, detail jsonb)`, append-only. Plus `ops.load(load_id, delivery_id, target_table, ducklake_snapshot_id, rows_in, rows_loaded, rows_rejected, started_at, ended_at, run_ref)`.
  - *Gives:* idempotency key (UNIQUE(feed_id, sha256)); evidence of "what was received, when, from whom"; the shared truth during migration.
  - *Costs:* every ingestor must write it transactionally with the byte upload (write the object first, then insert the ledger row; reconcile orphans).
  - *Failure modes:* ledger and object store diverge (object without row, or row without object). *Early warning:* a nightly reconciliation diff of object-store listing vs. ledger, which should always be zero.
  - *Exit cost:* low.
- **2c. Derived from data:** list the immutable raw-bytes bucket (path convention `raw/<feed>/<business_date>/<sha256>`), and/or DuckLake `ducklake_snapshot_changes` filtered on raw tables with `commit_message` = delivery_id [documented capability].
  - *Gives:* cannot drift from the bytes.
  - *Costs:* listing cost grows with feeds; no "received_at from vendor's perspective" unless it is in the path or metadata; S3 `LastModified` is upload time, not receipt time.
  - *Failure modes:* snapshot expiry, compaction, path-convention violations. *Early warning:* objects not matching the path regex.
  - *Exit cost:* low. Databricks file arrival triggers can watch the bucket **only if it is a UC external location/volume** [documented requirement].

#### 3. Deadline / arrival decisions (late or missing)
- **3a. Orchestrator-native:** Dagster FreshnessPolicy (`cron(deadline_cron, lower_bound_delta, timezone)`), GA per the 1.12 changelog but "preview / not enabled by default" per the docs page [documented, conflicting], evaluated from materialisation timestamps only.
  - *Costs:* freshness measures *materialisation* time, not *vendor delivery* time, so a late re-run makes a late delivery look on time.
  - *Failure modes:* holiday calendars and vendor-specific business days are not expressible in a single cron (inferred).
  - *Exit cost:* high. Lakeflow has job "duration thresholds" (seen in the configure-job page list) but no asset freshness model; arrival SLAs would have to be rebuilt.
- **3b. Platform ledger: expected-delivery / SLA table (a "delivery calendar" or "expectation register").**
  - *Mechanism:* `ops.feed_expectation(feed_id, calendar_id, cadence cron/rrule, expected_by local time + tz, grace interval, required bool, valid_from, valid_to)`. Plus `ops.expected_delivery(feed_id, business_date, slot, expected_by, status {pending, arrived, late, missing, waived}, delivery_id NULL, decided_at, decided_by)`, materialised daily by a calendar job. Plus an arrival evaluator that matches `ops.delivery` rows to slots.
  - *Gives:* "late" and "missing" become recorded decisions with timestamps, which serves as audit evidence and as input to downstream gates.
  - *Costs:* holiday calendars must be maintained; you own the evaluator.
  - *Failure modes:* the evaluator itself stops running, so nothing is ever late (silent). *Early warning:* a heartbeat row and a dead-man's switch (e.g. "no `decided_at` in the last N minutes").
  - *Exit cost:* low (the evaluator is a plain job in either orchestrator).
- **3c. Derived from data:** compute lateness at query time from `ops.delivery.received_at` or object timestamps vs. the calendar.
  - *Gives:* nothing to keep in sync.
  - *Costs:* the decision is not recorded, so "what did we know at 10:00" cannot be reproduced unless results are snapshotted.

#### 4. Operator acknowledgements / waivers
- **4a. Orchestrator-native:** manual asset-check result in Dagster (UI, or `POST /report_asset_check/` [documented]).
  - *Costs:* the acknowledgement is indistinguishable from a machine check unless conventions are enforced. OSS has no auth on the REST endpoint [documented] and limited actor identity (inferred). Scope, expiry and reason are free-text metadata.
  - *Failure mode:* the waiver silently also covers later failures, or is lost with run/event purge.
  - *Exit cost:* high (no equivalent in Lakeflow).
- **4b. Platform ledger: acknowledgement/waiver table (maker-checker).**
  - *Mechanism:* `ops.waiver(waiver_id, scope {delivery_id | feed_id+business_date | check_name+asset_key+partition}, check_result_id (the specific failure acknowledged), reason_code, free_text, ticket_ref, requested_by, approved_by (≠ requested_by), approved_at, expires_at, revoked_at, revoked_by)`, insert-only with revocation rows. Feeds into `ops.gate_state` (1b) and `ops.expected_delivery.status='waived'` (3b). Entry via a small admin UI/CLI that authenticates via SSO.
  - *Gives:* named human, four-eyes, expiry and a link to the exact failure: likely what an auditor expects (inferred).
  - *Costs:* build a UI and identity integration.
  - *Failure modes:* broad-scope waivers; waivers that never expire. *Early warning:* count of active waivers without `expires_at`; waivers matched against more than one check_result.
  - *Exit cost:* low.
- **4c. Derived from data:** not meaningful. A human decision is not derivable from data (inferred). The closest is GitOps: a waiver YAML file committed and reviewed via PR, with git history as the audit trail.
  - *Costs:* latency (PR merge + deploy), and it mixes runtime decisions into config.
  - *Exit cost:* low.

#### 5. Discovery cursors
- **5a. Orchestrator-native:** Dagster sensor cursor (a single string; complex state is serialized into it [documented]) plus the materialised-partition set.
  - *Failure modes:* sensor rename/reset loses the cursor, causing re-discovery or gaps. Two orchestrators each run their own sensor on the same SFTP and race (inferred).
  - *Early warning:* a jump in discovered count after deploy; a discovered set that does not match the ledger.
  - *Exit cost:* medium-high. A Databricks file arrival trigger keeps its own internal state [documented that file events metadata is tracked by an internal service] and is limited to UC locations. The SFTP and vendor-API cursor has no home there.
- **5b. Platform ledger: watermark / high-water-mark table (ADF "control table" pattern [documented]).**
  - *Mechanism:* `ops.source_cursor(feed_id, source_partition (e.g. SFTP dir, API endpoint+account), cursor_kind {mtime, listing_hash, api_since_token, sequence}, cursor_value text/jsonb, advanced_at, advanced_by run_ref, lease_owner, lease_expires_at)`. The cursor is advanced only in the same transaction that inserts the `ops.delivery` rows it covers. The lease columns give single-writer behaviour across two orchestrators.
  - *Gives:* only one orchestrator discovers per feed (the lease is also the migration switch).
  - *Costs:* lease logic.
  - *Failure modes:* the cursor advances before the bytes are kept, causing permanent loss. *Early warning:* gaps in vendor sequence numbers; the reconciliation in 2b.
- **5c. Derived from data:** the cursor is *recomputed* each time as "source listing minus `ops.delivery`/object-store set" (set-difference discovery, no stored cursor).
  - *Gives:* self-healing.
  - *Costs:* full listing every time (SFTP dirs grow; vendor APIs may not support listing history).
  - *Exit cost:* lowest.

#### 6. Concurrency limits
- **6a. Orchestrator-native:** Dagster pools (`pool="vendor_x_api"`, `dagster instance concurrency set ...`) [documented].
  - *Costs:* limits are instance-DB state, set by CLI/UI rather than GitOps unless driven by `dagster.yaml`/helm (helm `concurrency` since 1.12.9 [documented]). A step that "reads back and refuses" depends on internal APIs.
  - *Failure modes:* **during dual-run, Dagster pools do not see Databricks runs, so a vendor API rate limit is exceeded by the sum of the two** (inferred).
  - *Exit cost:* high. In the docs I fetched, Lakeflow offers per-job max concurrent runs, workspace limits and queueing [documented]. I found no named cross-job resource pool (gap, see below).
- **6b. Platform ledger: semaphore/lease table.**
  - *Mechanism:* `ops.resource_limit(resource_key, max_slots, managed_in_git bool)` plus `ops.resource_lease(resource_key, slot_no, holder (orchestrator, run_id, step), acquired_at, expires_at, heartbeat_at)`. Acquire via `INSERT ... WHERE (SELECT count(*) ...) < max_slots`, using `SELECT ... FOR UPDATE SKIP LOCKED` or Postgres advisory locks. Limits are seeded from GitOps.
  - *Gives:* one limit across both orchestrators.
  - *Costs:* lease expiry tuning; the orchestrator does not know about the wait, so it shows a "running" step that is actually waiting and burns a pod (inferred).
  - *Failure modes:* leaked leases (a crashed pod) starve the resource. *Early warning:* leases with a stale `heartbeat_at`; queue wait time.
  - *Exit cost:* low.
- **6c. Derived/external:** the vendor's own rate limiter (429s) with client-side backoff; or a token bucket in a shared cache.
  - *Gives:* the vendor is the source of truth.
  - *Costs:* failures instead of queueing.
  - *Exit cost:* low. Not audit-relevant (inferred).

#### 7. Schedules, on/off state, backfill progress
- **7a. Orchestrator-native:** schedules are defined in code. On/off state lives in the Dagster instance DB (toggled in the UI). Backfill progress lives in Dagster backfill records [documented: UI-launched backfills]. Tick history is purgeable [documented]. In Databricks, schedules and pause status sit in the job definition (`system.lakeflow.jobs` is SCD2 with 365-day retention [documented]), and backfill = N parameterised runs [documented].
  - *Failure mode:* in dual-run, the same feed is scheduled ON in both. *Early warning:* two runs for the same feed/business_date from different orchestrators in `ops.load`.
  - *Exit cost:* medium. Schedules are re-declared per orchestrator anyway.
- **7b. Platform ledger: run-control / feed-ownership table.**
  - *Mechanism:* `ops.feed_control(feed_id, owning_orchestrator {dagster, databricks}, enabled bool, paused_reason, changed_by, changed_at)`, ideally GitOps-generated (YAML → table) so that the git log is the change audit. Plus `ops.backfill_request(backfill_id, feed_id, range_start, range_end, reason, requested_by, approved_by)` and `ops.backfill_item(backfill_id, business_date, status, load_id)`. Orchestrator schedules stay native but each tick first checks `feed_control`: if it is not the owner, the tick no-ops.
  - *Gives:* the migration cut-over becomes one row flip; backfill evidence (why the past was re-derived) survives orchestrator change.
  - *Costs:* two sources of "is it on" (the orchestrator toggle and the table) can disagree.
  - *Early warning:* the orchestrator schedule is ON while `feed_control.enabled=false` (a daily diff).
- **7c. Derived from data:** backfill progress = which partitions exist in DuckLake vs. the expected calendar (3b).
  - *Gives:* always truthful about data.
  - *Costs:* says nothing about intent/approval.

**Pattern-name map (for the report writer).**
- **Delivery/arrival ledger** = 2b (also called inbound file register or manifest table).
- **Batch/load register** = `ops.load` (ABC "batch ID" [lead only]).
- **Watermark/high-water-mark or control table** = 5b [documented ADF].
- **Audit table of check results** = 1b (BimlFlex RowCount/AuditRow as a vendor example [documented]; dbt `store_failures` is a *non*-history counter-example [documented]).
- **Acknowledgement/waiver table** = 4b.
- **Expectation/SLA calendar** = 3b.
- **Run-control/feed-control table** = 7b (ABC "control" [lead only]).
- **Semaphore/lease table** = 6b.

### Gaps
- No first-hand practitioner report with an outcome (bank, asset manager or fintech) on delivery ledgers, waiver tables or moving state out of Dagster was fetched. The Fabric blog was **unreachable** (403). ABC sources are search leads only.
- I did not fetch Dagster docs on the run re-execution API (`parent_run_id`/`root_run_id`) or on run-storage retention for event logs, so the claim that run purging deletes gate evidence is inference.
- Databricks: I did not find (and did not specifically fetch) any doc on a cross-job named concurrency/resource pool. "None exists" is an inference from the configure-job and backfill pages only.
- I did not confirm whether Lakeflow table update triggers can watch non-UC tables (e.g. a DuckLake table). The doc lists only UC/OpenSharing/system tables, so the inference is no.
- Elementary (`elementary_test_results`, `dbt_run_results`) docs: the fetched page was navigation only, so it is unverified. GX result stores and Soda: not verified (Soda URL returned 404).
- The DuckLake version number was not captured from the "stable" docs.

---

## A4: If operational state leaves the orchestrator, what must it still know, what is lost or degraded, and mitigations

### Takeaway
The orchestrator still needs the asset/job graph, schedules/triggers and enough events to drive its UI and automation. Lineage, check UI, freshness views, Declarative Automation and the backfill UI all key on Dagster's own materialisation and check events. Moving truth to a ledger degrades all of them unless the platform mirrors ledger state back via Dagster's `report_asset_*` endpoints or `report_runless_asset_event`. Mirroring costs a sync process, double-writes, possible divergence and an unauthenticated write path on OSS. On Databricks, the reporting-back targets (task values, run history, system tables) hold run metadata only, and that metadata is short-lived or read-only.

### Cited Findings
- [documented] External assets: "Dagster can't materialize external assets directly or put them in a schedule ... an external system must inform Dagster when an external asset is updated." Two ways exist: pull via a sensor that emits `AssetMaterialization` in `SensorResult(asset_events=...)` with a cursor, or push via the REST API. External assets can form a dependency graph and native assets can depend on them, so lineage is preserved if you declare `AssetSpec`s. — [Dagster docs: External assets](https://docs.dagster.io/guides/build/assets/external-assets)
- [documented] REST: `POST /report_asset_materialization/`, `POST /report_asset_check/`, `POST /report_asset_observation/`. Parameters are `asset_key`, `metadata`, `data_version`, `description`, `partition`. Calls return `{}` on 200, and "Authentication is required only if requests are being made against a Dagster+ instance." — [Dagster docs: External assets REST API](https://docs.dagster.io/api/rest-apis/external-assets-rest-api)
- [documented] `DagsterInstance.report_runless_asset_event` became public in 1.5.9 (2023-11-16). The `report_asset_check` REST endpoint was added in 1.5.4 (2023-10-19). **Both are older than 2 years**; the REST docs are still current as of 2026-10-27. — [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] Freshness policies evaluate on materialisations ("If the asset has not materialized in the window..."), so freshness views work for external assets only if materialisations are reported. — [Dagster docs: Asset freshness policies](https://docs.dagster.io/guides/observe/asset-freshness-policies)
- [documented] Cross-run gating in Dagster automation: `AutomationCondition.all_deps_blocking_checks_passed` (1.8.12, 2024-10-17) reads Dagster's check records. If check results live only in a ledger, this condition sees nothing unless results are mirrored with `report_asset_check`. — [Dagster CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- [documented] Backfill UI launches from asset pages for partitioned assets with shared upstream partitioning. — [Dagster docs: Backfilling data](https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data)
- [documented] Databricks reporting targets: task values are intra-job, JSON ≤48 KiB ([task values](https://docs.databricks.com/aws/en/jobs/task-values)); run history is 60 days ([monitor](https://docs.databricks.com/aws/en/jobs/monitor)); `system.lakeflow.job_run_timeline` is 365 days and includes `job_parameters` and `result_state` ([system tables](https://docs.databricks.com/aws/en/admin/system-tables/jobs)); file/table-update triggers are restricted to UC locations/tables ([file arrival](https://docs.databricks.com/aws/en/jobs/file-arrival-triggers), [table update](https://docs.databricks.com/aws/en/jobs/trigger-table-update)).

### Inferences
- **What the orchestrator must still know (inferred):**
  1. The asset/job graph (static, in code), to show lineage and order steps.
  2. Schedules/triggers and which feeds it owns (7b ownership flag read at tick time).
  3. A trigger signal for event-driven runs: either its own sensor (reading the ledger instead of SFTP), or a push.
  4. Enough to *block downstream scheduling*: either the gate function in every step (1b), or mirrored check results so `all_deps_blocking_checks_passed` works.
  5. Run identity to stamp into ledger rows (`run_ref`), so the ledger links back to orchestrator logs.
- **Features lost or degraded per state kind if not mirrored (inferred, built on the documented behaviour above):**
  - **Asset graph/lineage:** kept (static), but *materialisation timeline* becomes empty for steps whose landing is recorded only in the ledger.
  - **Check UI / asset health:** empty or stale for ledger-held verdicts and waivers.
  - **Freshness views and alerts:** fire falsely (no materialisations) or must be disabled.
  - **Declarative Automation:** conditions like `newly_updated`/`all_deps_blocking_checks_passed` do not fire without mirrored events.
  - **Backfill UI:** still launches runs, but "partition materialised" status disagrees with ledger truth.
  - **Pools UI:** shows nothing about ledger leases; steps look "running" while waiting.
  - **Sensor tick UI:** shows a cursor that is no longer authoritative.
  - **Databricks:** there is less to lose. Lakeflow has no asset-level check/freshness model in the docs fetched, so a ledger costs mainly the Jobs UI's run-level view, which is retained anyway.
- **Mitigation options (inferred unless cited):**
  - **M1: ledger to Dagster mirror via sensor (pull).** A Dagster sensor reads `ops.delivery`/`ops.check_result`/`ops.waiver` since `max(id)` (cursor = ledger sequence) and emits `AssetMaterialization`/`AssetCheckEvaluation`/`AssetObservation` [documented mechanism].
    - *Costs:* the ledger sequence is a second cursor; the mirror lags by the sensor interval (≥30 s in the doc example).
    - *Failure mode:* mirror lag or stall makes the UI lie. *Early warning:* a "mirror lag" metric (ledger max id vs. mirrored max id).
    - *Benefit:* all writes originate in the orchestrator, so the OSS REST auth issue is avoided.
  - **M2: push via REST** (`/report_asset_*`) from the ingestion library after the ledger commit [documented endpoints].
    - *Costs:* dual-write is not atomic; the call has to be retried/outboxed (an `ops.outbox` table); OSS endpoints are unauthenticated [documented], so they need network policy/ingress auth in Kubernetes (inferred).
    - *Exit:* this is the only option that also works when Databricks runs a feed but Dagster is still the "single pane". Databricks jobs could POST into Dagster during migration (inferred).
  - **M3: in-process reporting** with `report_runless_asset_event` (from code with instance access) [documented API, from 2023]. Same semantics as M1/M2, but couples the writer to the Dagster instance DB, which works against neutrality (inferred).
  - **M4: Databricks side.** Job parameters carry `delivery_id`/`business_date`; task values pass intra-run decisions; `system.lakeflow.job_run_timeline` joins to `ops.load.run_ref` for 365-day run lineage [documented capabilities]. There is no place to *write back* asset-check verdicts, so the ledger is the UI. A dashboard over `ops.*` (Databricks SQL dashboard or any BI tool) replaces the check UI (inferred).
  - **M5: treat the mirror as cache, never source.** The gate function reads the ledger, never Dagster. Mirrored events are labelled with metadata `source=ledger, ledger_id=...` so divergence is detectable (inferred).
- **Costs common to all mirrors (inferred):** two representations of truth; event-log growth in Dagster (duplicate history); version coupling to Dagster REST/event APIs (which moved: blocking-check missing-result semantics changed in 1.13.7 [documented]).

### Gaps
- I did not fetch Dagster docs on whether externally reported check evaluations (via REST) participate in `blocking` semantics for *runs*, as opposed to Declarative Automation conditions. This is unverified.
- I did not verify whether Dagster asset checks can be attached to external `AssetSpec`s in OSS for the check UI (the REST doc says "asset_check evaluation for an external asset", which implies yes, but I have no full example).
- No Databricks doc fetched on Unity Catalog lineage for non-UC (DuckLake/Postgres catalog) tables. That lineage would need to be inferred as absent.

---

## Which state kinds are audit evidence in a regulated setting (inferred unless sourced)

### Takeaway
On my reasoning (no regulation fetched), four state kinds are evidence of "what was received, when, from whom, what was derived, and who decided": delivery landing (2), gate verdicts (1), operator acknowledgements (4) and arrival/late/missing decisions (3). Backfill requests (part of 7) are also evidence. These arguably should never have lived only in an orchestrator whose run history is purgeable (Dagster tick retention is configurable) or expires (Databricks 60-day run history, 365-day system tables). Cursors (5), concurrency limits (6) and schedule on/off state are operational control state, with evidential value only as change history.

### Cited Findings
- [documented] Databricks run history lasts 60 days, with an explicit recommendation to export before expiry. System tables keep 365 days free. — [Databricks: monitor](https://docs.databricks.com/aws/en/jobs/monitor); [system tables](https://docs.databricks.com/aws/en/admin/system-tables/jobs)
- [documented] Dagster schedule/sensor tick history is purgeable via `retention: ... purge_after_days`. — [Dagster OSS instance config](https://docs.dagster.io/deployment/oss/oss-instance-configuration)
- [documented] Vendor framing that audit evidence should sit in a customer-owned DB independent of the runtime: "nothing depends on a vendor runtime staying online to read it later" (BimlFlex, 2026-06-19, vendor marketing, no regulation cited). — [Varigence](https://www.varigence.com/blog/row-level-reconciliation-audit-evidence-bimlflex-writes-to-your-own-database)
- [documented] dbt's audit schema for failures is overwrite-only ("always replace previous failures"), so it does not preserve history unless snapshotted. — [dbt store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures)
- [documented] DuckLake snapshots can carry author/commit message/extra info, but can also be expired. — [DuckLake snapshots](https://ducklake.select/docs/stable/duckdb/usage/snapshots)

### Inferences
- **Delivery landed (2): strongest evidence candidate.** It directly answers "what was received, when, from whom", and should be append-only with sha256 and object URI. Orchestrator-only storage is exposed to purge, to the unauthenticated OSS write path, and to loss at migration.
- **Gate verdicts (1): evidence of controls operating.** A regulated firm typically needs to show that a control ran and what it decided for each delivery. A verdict that is only reconstructable by walking run lineage is weak evidence.
- **Operator acknowledgements (4): evidence of human override.** Needs actor identity, approver, reason and expiry, which the orchestrator's manual check result does not structurally enforce.
- **Arrival decisions (3): evidence for vendor-management/SLA oversight.** Today they are recomputed from materialisation history, so the decision as of a time is not recorded.
- **Backfill/re-derivation requests (7, part): evidence of "what was derived, and why it changed".** Should record requester, reason and range.
- **Discovery cursors (5): not evidence in themselves.** The delivery ledger is the evidence; cursor history helps explain gaps only.
- **Concurrency limits (6) and schedules on/off (7): change-management evidence at most.** GitOps history covers them if they are declared in git. Runtime UI toggles are not covered by git, which is an argument for 7b.
- Retention: regulated record-keeping periods for asset managers are typically multi-year (from memory, **unsourced, not verified here**). If that holds, 60-day or 365-day orchestrator retention could not serve as the record of evidence.

### Gaps
- I fetched no regulatory text (e.g. MiFID II record-keeping, SEC 17a-4/204-2, BCBS 239, DORA, or BaFin MaRisk/BAIT for a German firm), so classifying these as "audit evidence" is wholly inference. Required retention periods are unsourced.
- I found no practitioner case study from a regulated asset manager describing an auditor's finding on orchestrator-held evidence.
