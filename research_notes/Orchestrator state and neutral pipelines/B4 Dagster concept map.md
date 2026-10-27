# B4 Dagster concept map (Dagster OSS side, as of 1.13.x)

Scope: the Dagster OSS equivalent of 19 orchestration concepts, with the exact API name, the version it appeared in, its status in 1.13.x, whether it is OSS or Dagster+ only, and the semantics that matter when mapping to another orchestrator. Databricks is out of scope.

## Method and source conventions

### Takeaway
Most claims rest on two kinds of source. The first is Dagster's own changelog (CHANGES.md). The second is the docs tree in a sparse clone of dagster-io/dagster master (commit 8b9a41d, 2026-10-27, CHANGES.md up to 1.13.27), checked against live dagster.io/docs API pages. Release dates come from the PyPI JSON. Every row marks its claims as documented or inferred.

### Cited Findings
- **Changelog sources.**
  - Current CHANGES.md: it starts at 1.1.8. The raw master file has the same 7,117 lines as the clone. — [CHANGES.md master](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - Older versions (0.5.x to 1.1.7): taken from the changelog at tag 1.1.7. — [CHANGES.md @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
  - How headings map to releases. In CHANGES.md a heading such as "Major changes since 1.X.0" or "Changes since 1.X.last" is the release note of the *next* minor .0 release. For example, "Major changes since 1.10.0" is the 1.11.0 note and "Changes since 1.10.21" is also 1.11.0. Old "Since 1.0.17" means 1.1.0 and "Since 1.1.21" means 1.2.0. The "since version" values below use this mapping. That reading is an inference from the heading layout; it is not stated anywhere.
- **Release dates (PyPI upload dates).** — [PyPI dagster JSON](https://pypi.org/pypi/dagster/json)

  | Version | Date | Version | Date |
  |---|---|---|---|
  | 0.7.5 | 2020-03-20 | 1.3.6 | 2023-05-25 |
  | 0.8.0 | 2020-06-11 | 1.4.6 | 2023-08-17 |
  | 0.9.3 | 2020-08-21 | 1.4.12 | 2023-09-07 |
  | 0.9.18 | 2020-11-05 | 1.4.17 | 2023-09-28 |
  | 0.10.0 | 2021-01-15 | 1.5.0 | 2023-10-02 |
  | 0.11.10 | 2021-05-21 | 1.5.3 | 2023-10-12 |
  | 0.11.12 | 2021-06-03 | 1.5.4 | 2023-10-19 |
  | 0.11.13 | 2021-06-11 | 1.6.0 | 2024-01-11 |
  | 0.12.0 | 2021-07-08 | 1.6.4 | 2024-02-08 |
  | 0.12.3 | 2021-07-23 | 1.6.12 | 2024-03-21 |
  | 0.12.12 | 2021-09-24 | 1.7.0 | 2024-04-04 |
  | 0.13.10 | 2021-12-02 | 1.7.6 | 2024-05-16 |
  | 0.14.0 | 2022-02-17 | 1.8.0 | 2024-08-08 |
  | 0.15.5 | 2022-07-07 | 1.8.12 | 2024-10-17 |
  | 0.15.6 | 2022-07-14 | 1.9.0 | 2024-11-01 |
  | 1.0.0 | 2022-08-05 | 1.9.1 | 2024-11-08 |
  | 1.0.6 | 2022-08-26 | 1.9.12 | 2025-02-10 |
  | 1.1.0 / 1.1.1 | 2022-11-18 | 1.10.0 | 2025-02-13 |
  | 1.1.18 | 2023-02-09 | 1.10.8 | 2025-04-03 |
  | 1.1.21 | 2023-03-02 | 1.10.18 | 2025-05-29 |
  | 1.2.0 | 2023-03-09 | 1.11.0 | 2025-06-26 |
  | 1.2.4 | 2023-03-29 | 1.12.0 | 2025-10-30 |
  | 1.3.0 | 2023-04-19 | 1.12.19 | 2026-03-12 |
  |  |  | 1.12.22 | 2026-04-02 |
  |  |  | 1.13.0 | 2026-04-09 |
  |  |  | 1.13.27 | 2026-10-26 (latest) |

- **Docs URLs.** docs.dagster.io now returns a 308 redirect to dagster.io/docs. Docs paths below are given against the clone at commit 8b9a41d (docs/docs/...) and the matching live URL. — [redirect observed on fetch of docs.dagster.io/guides/observe/asset-freshness-policies](https://dagster.io/docs/guides/observe/asset-freshness-policies)
- **What the status labels mean.**
  - "Preview" means "not considered ready for production use … APIs may change". — [_Preview.md partial](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/partials/_Preview.md)
  - "Beta" means "still being tested and may change"; API pages add "may have breaking changes in minor version releases". — [_Beta.md partial](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/partials/_Beta.md)
  - "No label" below means the live API page shows no lifecycle badge. I treat that as GA. That reading is an inference.
- **Age flag.** Anything first shipped before about 2024-10-27 is marked **[>2y]**. These features are older than two years, so their semantics have had time to change.

### Inferences
- The ".0 release note" reading of the changelog headings is inferred from how they are laid out. Exact intro versions for features before 0.12 (sensors, K8sRunLauncher, S3ComputeLogManager) are lower bounds, taken from the earliest changelog mention.

### Gaps
- The API reference pages in the clone (docs/docs/api/dagster, api-lifecycle) were empty in the sparse checkout. Status labels therefore come from live dagster.io/docs pages, which showed version 1.13.27. The core Python definitions (python_modules/dagster/dagster/_core/definitions) were not in the sparse clone, so no `@beta`/`@preview` decorators were read in source.

## Concept map table (concept | Dagster OSS equivalent | since | status in 1.13.x | OSS vs Dagster+ | semantics caveats)

### Takeaway
All 19 concepts have an OSS equivalent except unified alerting (row 18), and OSS has no built-in alert on freshness breaches (row 11). Both are Dagster+ alert-policy features. Several pieces are non-GA in 1.13.x: partitioned asset checks, virtual assets and job-level automation conditions are preview; MultiPartitionMapping, `@observable_source_asset` and the `backfill_policy` parameter are beta. FreshnessPolicy has conflicting labels (GA in the changelog, preview in the docs).

### Cited Findings

| # | Concept | Dagster OSS equivalent (API) | Since (date) | Status in 1.13.x | OSS vs Dagster+ | Semantics caveats |
|---|---|---|---|---|---|---|
| 1 | Asset as unit, with deps | `@asset`, `AssetSpec`, `AssetDep`, `deps=[...]`, `Definitions` | `@asset` experimental 0.12.12 (2021-09) [>2y]; `AssetDep` 1.4.17 (2023-09); `AssetSpec`/`AssetDep`/`MaterializeResult` stable 1.6.0 (2024-01) | GA (no label); `SourceAsset` deprecated (removal in 2.0); single-`AssetKey` `deps` removed 1.13.0 | OSS | Assets are keyed by `AssetKey`. Deps are asset-to-asset, not task-to-task. 1.13.0 adds preview `is_virtual` for views |
| 2 | One step, many assets | `@multi_asset(specs=[AssetSpec...])`, `AssetOut`, `@graph_multi_asset` | Changelog first mentions `@multi_asset` in 0.13.10 (2021-12) [>2y]; `AssetSpec` on multi_asset 1.4.17 | GA (only the `resource_defs` param is beta) | OSS | It runs as one op/step. Retry from asset failure inside a multi-asset step came in 1.11.0. Since 1.12.0, `step_dependency_config.require_upstream_step_success=False` lets downstream steps start before the whole multi-asset step finishes. Blocking checks inside a multi-asset must be enforced by the multi-asset itself (row 4) |
| 3 | Observed external source | `AssetSpec` passed to `Definitions` (external asset); `@observable_source_asset` returning `DataVersion`/`ObserveResult`; sensors that emit `SensorResult(asset_events=[AssetObservation/AssetMaterialization])`; REST `report_asset_materialization` / `report_asset_observation` | `observable_source_asset` 1.1.0 (2022-11) [>2y]; `external_assets_from_specs` 1.5.3 (2023-10) [>2y], removed 1.13.0 in favour of plain `AssetSpec`; REST materialization 1.5.3, observation 1.5.5 | `AssetSpec` GA; `@observable_source_asset` **beta**; `SourceAsset` **deprecated**; `auto_observe_interval_minutes` **removed 1.13.0** | OSS (REST needs a token only on Dagster+) | Dagster cannot materialize or schedule external assets; something external must report events. New FreshnessPolicies are **not supported on observable source assets**. External assets do not trigger Dagster+ asset-health alerts |
| 4 | DQ checks; blocking | `@asset_check`, `@multi_asset_check`, `AssetCheckSpec`, `AssetCheckResult`, `AssetCheckSeverity`, `blocking=True`; `AutomationCondition.all_deps_blocking_checks_passed()` | `@asset_check` 1.4.12 (2023-09, experimental) [>2y]; `blocking` 1.6.4 (2024-02) [>2y]; `all_deps_blocking_checks_passed` 1.8.12 (2024-10) | Core check APIs GA (no label); **partitioned checks preview** (1.13.0); `build_column_schema_change_checks` / `build_metadata_bounds_checks` **beta** | OSS (check alerting is Dagster+) | `blocking` only gates **downstream assets in the same run**, and only on an ERROR-severity *failed* result. No result emitted means downstream proceeds with a warning. Across runs, gating needs `all_deps_blocking_checks_passed` in an AutomationCondition. Inside a multi-asset, the multi-asset must enforce it itself |
| 5 | Manual / human check result | UI "Report Execution" dialog (moved to a "Report evaluation" dropdown); REST `POST /report_asset_check/`; GraphQL params type `ReportAssetCheckEvaluationsParams` (assetKey, checkName, passed, severity, serializedMetadata, partitionKeys, description) | REST 1.5.4 (2023-10) [>2y]; UI dialog 1.12.19 (2026-03); dropdown 1.12.22 (2026-04); GraphQL type present in master | GA as far as the docs show (no label) | OSS and Dagster+ (auth header only on Dagster+) | Results are recorded as **runless** `ASSET_CHECK_EVALUATION` events with no run attached. Partition keys are supported. In the UI this is permission-gated (`hasReportRunlessAssetEventPermission`) |
| 6 | Partitions and mappings | `DailyPartitionsDefinition` / `TimeWindowPartitionsDefinition`, `StaticPartitionsDefinition`, `MultiPartitionsDefinition`, `DynamicPartitionsDefinition`; `TimeWindowPartitionMapping(start_offset, end_offset)`, `MultiPartitionMapping`, `MultiToSingleDimensionPartitionMapping`, `StaticPartitionMapping`, `SpecificPartitionsPartitionMapping`, `AllPartitionMapping`, `LastPartitionMapping`, `IdentityPartitionMapping` | Static ≤0.13.10 [>2y]; `PartitionMapping` family 0.15.6 (2022-07, experimental) [>2y]; Multi and Dynamic 1.1.0 (2022-11, experimental) [>2y]; TWPM offsets 1.1.7/1.2.0 [>2y]; `MultiPartitionMapping` 1.2.4 (2023-03) [>2y]; time-partition `exclusions` 1.12.0 | Partition defs GA (no label); **`MultiPartitionMapping` and `MultiToSingleDimensionPartitionMapping` beta**; TWPM `allow_nonexistent_upstream_partitions` beta; `DynamicPartitionsDefinition(partition_fn)` deprecated | OSS | Custom `PartitionMapping` subclasses are **not supported**. The docs recommend at most 100,000 partitions per asset. Since 1.10.10, a TWPM between time partitions in different timezones fails validation. Dynamic partitions are added at runtime through the instance, sensors or the UI |
| 7 | Backfills: run per partition vs one run per range | `BackfillPolicy.single_run()`, `BackfillPolicy.multi_run(max_partitions_per_run=1)`; asset backfill daemon | BackfillPolicy first mentioned 1.4.8 (2023) [>2y]; UI single-run toggle removed in 1.5; GA 1.10.18 (2025-05) | Changelog: **GA**. Live API page: `@asset(backfill_policy=)` labelled **beta**, and constructing `BackfillPolicy` directly "not recommended as the API is subject to change". The sources **conflict** | OSS | `single_run` means the asset code must handle a partition *range*. Since 1.9.7, mixed-policy selections are allowed. Since 1.12.0, run config can be supplied to backfills. Declarative Automation emits backfills when more than one partition is requested, so the BackfillPolicy is honoured (1.9.0) |
| 8 | Cron schedule over partitions | `build_schedule_from_partitioned_job(job, ...)`; alternative `AutomationCondition.on_cron()` | ≤0.15.5 (2022-07) [>2y]; multi-partition with a time dimension 1.2.2; static-partitioned jobs 1.6.4; `owners` 1.13.7 | GA (no label) | OSS | The cron is derived from the time-partition definition, and combining it with a non-standard cron plus `minute_of_hour` errors (1.2.5). For static partitions it fans out runs (inference from the 1.6.4 note) |
| 9 | Event-driven trigger with cursor | `@sensor` with `context.cursor` / `context.update_cursor()`; `@asset_sensor`; `SensorResult` | Sensors ≤0.10.0 (2021-01) [>2y]; cursor 0.11.10 (2021-05) [>2y]; asset sensors 0.12.0 [>2y] | GA; `MultiAssetSensorDefinition` **superseded**; `last_run_key` deprecated | OSS | The cursor is a string held in Dagster instance storage. Sensors are polled by the daemon. Run keys de-duplicate runs |
| 10 | Declarative "run when upstream changes or a cron tick passes" | `AutomationCondition` (`eager()`, `on_cron()`, `on_missing()`, composable operators), evaluated by `AutomationConditionSensorDefinition` / `default_automation_condition_sensor` | Experimental 1.8.0 (2024-08); `AutoMaterializePolicy` deprecated 1.8.0; "no longer experimental" in 1.9.0 (2024-11-01) | GA for asset-level; **job-level conditions preview**; "look-through virtual assets" preview | OSS (needs the daemon and the sensor toggled on) | The default sensor must be **turned on in the UI**. Runs get the tag `dagster/from_automation_condition`. `newly_updated` fires on an observation only when the data version changes (1.7.13) |
| 11 | Freshness and breach alerting | New `FreshnessPolicy` (time-window `fail_window`/`warn_window`; cron `deadline_cron`/`lower_bound_delta`/`timezone`), `apply_freshness_policy`, `map_asset_specs`; FreshnessDaemon; legacy `LegacyFreshnessPolicy`; superseded `build_last_update_freshness_checks`, `build_time_partition_freshness_checks`, `build_sensor_for_freshness_checks` | New FP 1.11.0 (2025-06, preview); "GA" 1.12.0 (2025-10); old FP deprecated 1.7.0 and renamed to Legacy 1.11.0; legacy params removed from `@observable_source_asset`/`AssetsDefinition` 1.13.0; freshness checks 1.7.0 [>2y], superseded 1.12.0; `freshness_policy_sensor` removed 1.9.0 | **Conflict**: changelog 1.12.0 says GA with the daemon on by default; the live docs page (1.13.27) still says "not enabled by default while in preview … under active development". Freshness checks: **superseded** | Evaluation is OSS. **Alerting on a breach is Dagster+ only** (alert policy "Asset freshness") | In OSS the daemon writes runless `FreshnessStateChange` events (PASS/WARN/FAIL/UNKNOWN). OSS has no built-in notifier for those events (see row 18). Not supported on observable source assets |
| 12 | Concurrency pools / per-group run limits | `pool="..."` on `@asset`/`@op`/`@multi_asset_check`; `dagster instance concurrency set <pool> <n>`; `concurrency.pools.default_limit` / `.granularity: op\|run`; `concurrency.runs.tag_concurrency_limits` (with `applyLimitPerUniqueValue`); executor-level `tag_concurrency_limits` (within a run) | Global op concurrency experimental 1.4.x [>2y]; `pool` arg 1.9.12 (2025-02); run blocking default 1.10.0; QueuedRunCoordinator 0.9.18 [>2y]; run tag limits ≤0.12.0 [>2y]; executor tag limits 1.1.8 [>2y] | GA (no label) | OSS (`dagster.yaml`) and Dagster+ (deployment settings) | Granularity defaults to `op`, which limits ops across runs but not run count. Slots from a cancelled run **are not freed** unless `run_monitoring.free_slots_after_run_end_seconds` is set; with limit 1 this can deadlock. Run queue config moved under `concurrency` in 1.9.12 |
| 13 | Per-run container isolation, secrets per step | `K8sRunLauncher` (one pod per run); `k8s_job_executor` (one pod per step) with `step_k8s_config` / `per_step_k8s_config`; `dagster-k8s/config` tag on job or op/asset (`container_config`, `pod_spec_config`, `pod_template_spec_metadata`, `job_spec_config`, `job_metadata`, `merge_behavior`); Helm `envSecrets` / launcher `env_secrets` | K8sRunLauncher ≤0.7.5 (2020-03) [>2y]; `dagster-k8s/config` 0.9.3 (2020-08) [>2y]; `k8s_job_executor` 0.11.13 (2021-06) [>2y]; `step_k8s_config` 1.4.6 [>2y]; `per_step_k8s_config` 1.9.1 (2024-11) | GA (no label) | OSS (Dagster+ Hybrid agents use similar config) | Job-level `dagster-k8s/config` is **not** propagated to step pods under `k8s_job_executor`; use `step_k8s_config` or op-level tags. Merge is DEEP by default since 1.7.0 (was SHALLOW). Per-step secrets come through the op tag's `container_config` env/envFrom (inference, see notes) |
| 14 | Per-step retries with policy | `RetryPolicy(max_retries, delay, backoff=Backoff.EXPONENTIAL/LINEAR, jitter=Jitter.FULL/PLUS_MINUS)`, `RetryRequested`, `Failure(allow_retries=False)`; run retries `dagster/max_retries`, `dagster/retry_strategy` (`FROM_FAILURE`/`ALL_STEPS`/`FROM_ASSET_FAILURE`), `dagster/retry_on_asset_or_op_failure` | RetryPolicy 0.11.10 (2021-05) [>2y]; Backoff/Jitter 0.11.12 (2021-06) [>2y]; run retries 1.2.0 (2023-03) [>2y]; `retry_on_op_or_asset_failures` 1.6.7 [>2y] | GA | OSS (run retries enabled in `dagster.yaml` `run_retries`) | Op retries and run retries can both fire on the same failure unless `retry_on_asset_or_op_failure=false`. Run retries are executed by a daemon (event log consumer) |
| 15 | Code/data versions and staleness | `code_version=` on `@asset`/`AssetSpec`; `DataVersion` (returned on `Output`/`MaterializeResult`/observation); UI "Unsynced" status and "Materialize unsynced"; `RunRequest(stale_assets_only=True)`; `AutomationCondition` code-version conditions | op_version/`LogicalVersion` 1.1.0/1.1.1 (2022-11) [>2y]; renamed `DataVersion` 1.2.0 [>2y]; staleness causes in UI 1.1.21; `stale_assets_only` 1.1.10 [>2y] | `code_version` GA (no label); `DataVersion` label not verified | OSS | With no `code_version`, the run ID stands in, so every run counts as new code. The default data version is a hash of the code version plus input data versions. Staleness is shown and can be used for selection; it does not auto-trigger runs by itself. Virtual assets (preview) take part in staleness |
| 16 | Source to dbt lineage as one graph | `dagster-dbt`: `DbtProjectComponent` (YAML `type: dagster_dbt.DbtProjectComponent`), `@dbt_assets` + `DbtCliResource` + `DagsterDbtTranslator`; dbt `sources.yml` `meta.dagster.asset_key` links upstream assets; dbt tests become asset checks | `load_assets_from_dbt_project` 0.12.12 (2021-09) [>2y]; `@dbt_assets` 1.3.6 (2023-05) [>2y]; `DbtProjectComponent` in dagster-dbt 1.10.8 (2025-04), reworked 1.10.11/12; Components GA 1.12.0 | Components GA; dbt Fusion support **preview**; dbt views as virtual assets (1.13.0) tie to preview virtual assets | OSS | `DbtProjectComponent` is state-backed (manifest compiled and cached; on by default in 1.13.0). dbt tests with error severity are modelled as **blocking** checks (1.11.0). Fusion has no column-level lineage |
| 17 | Run metadata per materialisation, read back | `MaterializeResult(metadata={"dagster/row_count": int, "dagster/column_schema": TableSchema})`; dbt `fetch_row_counts()` / `fetch_column_metadata()`; read via the asset catalog / GraphQL / instance event-log APIs | `dagster/column_schema` key 1.6.12 (2024-03, experimental then) [>2y]; `dagster/row_count` standardised 1.7.6 (2024-05) [>2y] | Keys documented in the metadata reference without a label; `build_column_schema_change_checks` / `build_metadata_bounds_checks` **beta** | OSS | Metadata is attached to each event in the event log. The same keys can come from observations too (1.12.11 UI fix). Since 1.13.26 the dbt fetch helpers log a warning instead of failing |
| 18 | One alert stream: failed runs, checks, freshness, trigger failures | OSS: `@run_failure_sensor`, `@run_status_sensor`, `make_slack_on_run_failure_sensor` (dagster-slack), `make_apprise_on_run_failure_sensor`, plus custom sensors. Dagster+: **alert policies** (asset health, materialization, checks, freshness, run, code location, automation tick failure, agent downtime, insights) and webhooks (Early Access) | `run_status_sensor` 0.12.3 (2021-07) [>2y]; `run_failure_sensor` ≤0.13.4 [>2y]; Dagster+ asset/check alert policies 1.5.3 (experimental then) | OSS run sensors GA; Dagster+ alerts GA, with Insights-metric and credit-budget alert types experimental and webhooks Early Access | **One stream is Dagster+ only.** In OSS only run status has built-in sensors | The OSS API reference documents no built-in sensor for check failures, freshness changes or sensor/schedule tick failures. OSS users build them on the event log (inference). Dagster+ health alerts fire once per state change; automation alerts fire only on a success-to-failure change |
| 19 | Step logs to object storage | `compute_logs:` in `dagster.yaml`: `LocalComputeLogManager` (default), `NoOpComputeLogManager`, `dagster_aws.s3.S3ComputeLogManager`, `dagster_gcp.gcs.GCSComputeLogManager`, `dagster_azure.blob.AzureBlobComputeLogManager` | S3ComputeLogManager ≤0.8.0 (2020-06) [>2y]; `show_url_only` 1.3.3 [>2y] | GA | OSS (Dagster+ has its own log handling) | Captures raw stdout/stderr per step (structured events go to the event log, not here). `skip_empty_files` exists for S3 (0.15.x). `show_url_only` shows a link instead of the content |

### Inferences
- Treating "no lifecycle badge on the live API page" as GA is an inference; Dagster does not say so explicitly.

### Gaps
- Exact intro versions for `@multi_asset`, `DailyPartitionsDefinition`, `@sensor`, `run_failure_sensor`, `K8sRunLauncher` and `S3ComputeLogManager` are lower bounds (earliest changelog mention), not confirmed introductions.

## Notes per row: assets, multi-assets, external assets (rows 1-3)

### Takeaway
The asset-centric model has been in Dagster since 2021 (experimental in 0.12.12) and was stabilised around 1.5/1.6. External sources are now modelled as plain `AssetSpec`s, fed by sensors or the REST API. `@observable_source_asset` survives as beta, and `SourceAsset` is deprecated.

### Cited Findings
- **Row 1.**
  - 0.12.12 "Added experimental `@asset` decorator and `build_assets_job` APIs to construct asset-based jobs". — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
  - 1.4.17 added `AssetDep` and `AssetSpec` for `@multi_asset`; 1.6.0 marked "`MaterializeResult`, `AssetSpec`, and `AssetDep` now marked stable". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - 1.13.0 breaking changes: removed single-`AssetKey` `deps` support, removed `external_asset_from_spec(s)` ("Use `AssetSpec` inputs directly to `Definitions(...)`"), removed `auto_observe_interval_minutes`. — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - 1.13.0: "(Preview) Added support for virtual assets … `is_virtual`". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 2.**
  - 0.13.10: "`@asset` and `@multi_asset` decorator now return `AssetsDefinition` objects". — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
  - 1.11.0 (the "Major changes since 1.10.0" section) added "Retry from asset failure with multi-assets". 1.12.0 added `step_dependency_config` with `require_upstream_step_success`. — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - Live API page: `@multi_asset` has no label; only `resource_defs` is beta. — [Assets API](https://dagster.io/docs/api/dagster/assets)
- **Row 3.**
  - `observable_source_asset` arrived in 1.1.0, returning a `LogicalVersion`. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
  - `LogicalVersion` was renamed `DataVersion` in 1.2.0; `ObserveResult` arrived in 1.6.5. — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - Live labels: `@observable_source_asset` and `@multi_observable_source_asset` are beta ("may have breaking changes in minor version releases"); `SourceAsset` is deprecated ("will be removed in version 2.0.0. Use AssetSpec instead"). — [Assets API](https://dagster.io/docs/api/dagster/assets)
  - External assets docs: "Dagster can't materialize external assets directly or put them in a schedule … an external system must inform Dagster". Two options are documented: "Pulling external assets events with sensors" and "Pushing … using Dagster's REST API". — [external-assets.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/assets/external-assets.md)
  - REST endpoints `report_asset_materialization` (1.5.3), `report_asset_check` (1.5.4) and `report_asset_observation` (1.5.5) are "runless". The REST doc lists OSS URLs; the auth header is "Required only for Dagster+". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md); [rest-api.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/api/rest-api.md)

### Inferences
- **(Inferred, labelled.)** "Observed external source" as an asset node with data versions that drive downstream conditions is the Dagster model. A neutral schema with a "source asset with observation function" is really Dagster's `observable_source_asset`.

### Gaps
- The version that introduced `@multi_asset` was not pinned down; 0.13.10 is its earliest changelog mention.

## Notes per row: asset checks, blocking, manual results (rows 4-5)

### Takeaway
`blocking=True` is a within-run gate on downstream steps for ERROR-severity failures. Across runs it only has an effect if downstream automation uses `AutomationCondition.all_deps_blocking_checks_passed()`. Manual results go in as runless check-evaluation events, through REST (since 1.5.4), GraphQL, or a UI dialog that is new in 1.12.19.

### Cited Findings
- **When blocking arrived.** 1.6.4: "`@asset_check` now has a `blocking` parameter. When this is enabled, if the check fails with severity `ERROR` then any downstream assets in the same run won't execute". 1.7.0 ("Major Changes since 1.6.0"): "causes downstream assets in the same run to be skipped". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Docstrings.** `@asset_check(blocking)`: "runs that include this check and any downstream assets … will wait for this check … If the check fails with severity AssetCheckSeverity.ERROR, then the downstream assets won't execute." `AssetCheckSpec(blocking)`: "If this AssetCheckSpec is used in a multi-asset, that multi-asset is responsible for enforcing that downstream assets within the same step do not execute … gating applies only to _failed_ check results; if no result is emitted for the check, downstream execution proceeds and a warning is logged." — [Asset checks API](https://dagster.io/docs/api/dagster/asset-checks)
- **Gating across runs.** 1.8.12: "Added a new `AutomationCondition.all_deps_blocking_checks_passed` condition, which can be used to prevent materialization when any upstream blocking checks have failed." — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Default when not blocking.** The guide says: "By default, if a parent's asset check fails during a run, the run will continue and downstream assets will be materialized." — [asset-checks.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/test/asset-checks.md)
- **Partitioned checks** are labelled Preview in the guide and listed under 1.13.0 major changes. — [asset-checks.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/test/asset-checks.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **History of blocking behaviour.**
  - 1.10.20 fixed blocking halting a step on the first failure before other outputs were emitted.
  - 1.11.0: "dbt tests with error severity are now modeled as blocking asset checks".
  - 1.7.0 removed `build_asset_with_blocking_check`.
  - Before 1.6.4, blocking was done through `@graph_asset` with a check that raised an exception (1.4.13).
  - — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Practitioner report (first-hand), GitHub issue #25112, Dagster 1.8 on Dagster Cloud.** A failing dbt test blocked a downstream dbt model but not a downstream Python asset. No maintainer reply. The issue was relabelled feature request and closed "not planned" as stale on 2026-09-28. — [issue #25112](https://github.com/dagster-io/dagster/issues/25112)
- **Older search lead (not verified in full text).** A snippet from older docs said "Assets with an AutoMaterializePolicy currently do not respect blocking asset checks". — [search lead: docs.dagster.io/concepts/asset-checks](https://docs.dagster.io/concepts/asset-checks)
- **Row 5, UI.** 1.12.19: "Added a 'Report Execution' dialog to the asset checks detail view, allowing users to manually record check evaluation results." 1.12.22: "The 'Report evaluation' action for asset checks has been moved to a consolidated dropdown menu." — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 5, GraphQL.** Master has `GrapheneReportAssetCheckEvaluationsParams` (`assetKey`, `checkName`, `passed`, `severity`, `serializedMetadata`, `partitionKeys`, `description`), and the mutation calls `report_asset_check_evaluation` once per partition key. The UI permission is `hasReportRunlessAssetEventPermission`. — [inputs.py @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/python_modules/dagster-graphql/dagster_graphql/schema/inputs.py); [mutation.py @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/python_modules/dagster-graphql/dagster_graphql/schema/roots/mutation.py); [asset_graph.py @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/python_modules/dagster-graphql/dagster_graphql/schema/asset_graph.py)
- **Row 5, REST.** `POST /report_asset_check/` "Records an `AssetCheckEvaluation` event for an external asset". OSS URL: `https://dagster.my-org.com/report_asset_check`. — [rest-api.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/api/rest-api.md)

### Inferences
- **(Inferred.)** Blocking does not cross run boundaries. The docstring and changelog wording ("in the same run") imply that a downstream asset materialized in a later run (schedule, sensor, manual launch) is not blocked unless its AutomationCondition includes `all_deps_blocking_checks_passed()`. Whether a manually reported failing result (row 5) counts for `all_deps_blocking_checks_passed` was not verified in source.
- **(Inferred, labelled.)** "Blocking check" as a property of the check that gates the asset graph is Dagster-specific.

### Gaps
- The exact GraphQL mutation field name (`reportAssetCheckEvaluations` is likely) was not confirmed; only the params type and resolver were read.
- Whether the REST doc states the REST endpoint works for non-external (Dagster-materialized) assets was not checked; the docs say "for an external asset".

## Notes per row: partitions, backfills, partitioned schedules (rows 6-8)

### Takeaway
All the partition types and mappings exist in OSS. MultiPartitionMapping and MultiToSingleDimensionPartitionMapping are still beta, and custom mappings are unsupported. BackfillPolicy single-run vs multi-run is documented, but its status is inconsistent (changelog GA vs live API beta label).

### Cited Findings
- **Partition definitions.**
  - 1.1.0 major changes: `DynamicPartitionsDefinition` "(experimental)". `MultiPartitionsDefinition` (experimental) appeared in the 1.1.0 notes, with an optional schema migration. — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md); [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
  - The partitioning guide's example uses two dimensions (`date` and `region`). — [partitioning-assets.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/partitions-and-backfills/partitioning-assets.md)
- **Mappings.**
  - 0.15.6: `PartitionMapping`, `IdentityPartitionMapping`, `AllPartitionMapping`, `LastPartitionMapping` exposed, "currently marked experimental". 1.2.4: "(experimental) Added partition mapping … between different `MultiPartitionsDefinitions`". — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - TimeWindowPartitionMapping history: offsets in 1.1.7/1.2.0; cross-definition offsets "expressed in units of downstream partitions" in 1.7.4; `allow_nonexistent_upstream_partitions` in 1.3.10; mismatched timezones fail validation in 1.10.10. — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - Live labels:
    - `MultiPartitionMapping` and `MultiToSingleDimensionPartitionMapping` are beta.
    - TWPM's `allow_nonexistent_upstream_partitions` is beta.
    - Other partition defs and mappings carry no label.
    - `DynamicPartitionsDefinition.partition_fn` is deprecated (removal in 2.0.0).
    - The docs recommend "100,000 partitions or fewer".
    - — [Partitions API](https://dagster.io/docs/api/dagster/partitions)
  - "custom `PartitionMapping` and overriding `PartitionMapping` outside of Dagster is not currently supported." — [defining-dependencies-between-partitioned-assets.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/partitions-and-backfills/defining-dependencies-between-partitioned-assets.md)
  - 1.12.0: time-window partition `exclusions` (cron strings or datetimes) for custom calendars. — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 7, backfills.**
  - "Dagster supports backfills that execute as a single run that covers a range of partitions"; set `backfill_policy` to `single_run`. The UI "Launch as…" toggle was removed in 1.5. — [backfilling-data.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/partitions-and-backfills/backfilling-data.md)
  - 1.10.18: "`BackfillPolicy` is now marked as generally available (GA)". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
  - **Conflict.** The live API reference marks the `@asset(backfill_policy=)` parameter "beta" and says "Constructing an BackfillPolicy directly is not recommended as the API is subject to change". `multi_run(max_partitions_per_run)` defaults to 1. — [Partitions API](https://dagster.io/docs/api/dagster/partitions); [Assets API](https://dagster.io/docs/api/dagster/assets)
- **Row 8.** `build_schedule_from_partitioned_job` changelog trail:
  - 0.15.5 fix (so it existed by then)
  - MultiPartitions with a time dimension in 1.2.2
  - static partitions in 1.6.4
  - `owners` in 1.13.7
  - no lifecycle label on the live page
  - — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md); [Schedules/sensors API](https://dagster.io/docs/api/dagster/schedules-sensors)

### Inferences
- **(Inferred, from memory, not verified in this run.)** `MultiPartitionsDefinition` is limited to exactly two dimensions. The docs example shows two, but no text stating the limit was found in this run.
- **(Inferred, labelled.)** Partition *mappings* between differently partitioned assets (TWPM offsets, multi-to-single dimension) are a Dagster-specific idea. A neutral model with typed partition mappings is Dagster's model.

### Gaps
- Exact intro versions of `DailyPartitionsDefinition` and `StaticPartitionsDefinition` are pre-0.13.10 and not pinned.

## Notes per row: sensors, Declarative Automation, freshness (rows 9-11)

### Takeaway
Polling sensors with cursors are old and stable (0.10/0.11). Declarative Automation (`AutomationCondition`) has been GA since 1.9.0 and has replaced `AutoMaterializePolicy`. The new `FreshnessPolicy` is evaluated in OSS, but sources disagree on whether it is GA. Alerting on a freshness breach is a Dagster+ alert policy; OSS has no built-in notifier.

### Cited Findings
- **Row 9.** 0.11.10: "Sensors can now set a string cursor using `context.update_cursor(str_value)` that is persisted across evaluations … available on the context as `context.cursor`." The 0.10.0 notes already link a schedules/sensors overview. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
- **Row 9, live labels.** `MultiAssetSensorDefinition` is "superseded"; `last_run_key` is deprecated; core `sensor`/cursor carry no label. — [Schedules/sensors API](https://dagster.io/docs/api/dagster/schedules-sensors)
- **Row 10, history.**
  - 1.8.0 ("Major changes since 1.7.0"): "[Experimental] You can now add `AutomationCondition`s … drop-in replacement" for auto-materialize policies.
  - 1.8.0 also: "`AutoMaterializePolicy` has been marked as deprecated in favor of `AutomationCondition`", and the sensor was renamed `AutomationConditionSensorDefinition`, with a default `default_automation_condition_sensor` per code location.
  - 1.9.0 ("Major changes since 1.8.0"): "Declarative Automation … is no longer experimental."
  - — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 10, docs.** Users must "toggle on the **default_automation_condition_sensor** sensor" in the UI. Job conditions ("Automation conditions can also be attached to asset jobs") are labelled Preview, as is the "Resolving dependencies through virtual assets" section of the eager guide. — [declarative-automation/index.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/automate/declarative-automation/index.md); [automation-condition-reference.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/automate/declarative-automation/automation-condition-reference.md); [automating-jobs.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/automate/declarative-automation/automating-jobs.md)
- **Row 11, new FreshnessPolicy.**
  - 1.11.0: a new `FreshnessPolicy` replaces the deprecated one, which was renamed `LegacyFreshnessPolicy`; "under active development".
  - 1.12.0: "FreshnessPolicies GA … (previously Preview) … supersede the `LegacyFreshnessPolicy` API … as well as freshness checks". Exported from top-level `dagster`. "The `FreshnessDaemon` now runs by default".
  - 1.13.0: removed `legacy_freshness_policy` from `@observable_source_asset` and `legacy_freshness_policies_by_output_name` from `AssetsDefinition`.
  - — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 11, conflicting status.** The live docs page (showing 1.13.27) and the clone both say: "Freshness policies are under active development. You may encounter feature gaps and the APIs may change." They also say: "Freshness policies are not enabled by default while in preview. To use them in open source … `freshness: enabled: True`". Other content on the same page:
  - Two types: time window (`fail_window`, `warn_window`, at least 60 s) and cron (`deadline_cron`, `lower_bound_delta`, `timezone`).
  - Limitation: "not currently supported for source observable assets … and cacheable assets".
  - Alerts are pointed to the Dagster+ "Alerts" page.
  - "Freshness policies have superseded freshness checks since the 1.12 release."
  - — [asset-freshness-policies.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/observe/asset-freshness-policies.md); [live page](https://dagster.io/docs/guides/observe/asset-freshness-policies)
  - This contradicts the 1.12.0 changelog's "GA" and "runs by default". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 11, OSS mechanics.** `FreshnessDaemon` in OSS computes the state per asset and emits a `FreshnessStateChange` runless event through `instance._report_runless_asset_event` when the state changes. — [_daemon/freshness.py @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/python_modules/dagster/dagster/_daemon/freshness.py)
- **Row 11, freshness checks history.**
  - `build_last_update_freshness_checks` and `build_time_partition_freshness_checks` arrived in 1.7.0. They gained a `blocking` parameter in 1.10.10 and were marked superseded in 1.12.0.
  - The live API labels `build_last_update_freshness_checks` and `build_sensor_for_freshness_checks` "superseded".
  - `freshness_policy_sensor` was removed in 1.9.0.
  - Legacy `FreshnessPolicy` was deprecated in 1.7.0 ("For monitoring freshness, use freshness checks instead").
  - — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md); [Asset checks API](https://dagster.io/docs/api/dagster/asset-checks)
- **Row 11, Dagster+ alerting.** The "Asset freshness" alert type ("Failure, warning, or passing") is a Dagster+ alert policy, available on Serverless and Hybrid. — [alert-policy-types.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/observe/alerts/alert-policy-types.md)

### Inferences
- **(Inferred.)** To alert on a freshness breach in OSS today, a user would write a custom sensor that reads `FreshnessStateChange` events from the event log, or keep using the superseded freshness checks with a sensor or job-failure path. No built-in OSS mechanism was found.
- **(Inferred.)** The 1.12 GA claim vs the "preview / not enabled by default" docs text is most likely stale docs. The mapping should state both and check `dagster.yaml` behaviour in the target deployment.
- **(Inferred, labelled.)** Declarative `AutomationCondition` trees (eager, on_cron, on_missing, any_deps_updated…) are a Dagster-specific idea. A neutral "run when upstream changes OR cron tick" condition expressed as a composable condition tree is Dagster's model.

### Gaps
- The default minimum interval for sensors was not verified in this run.

## Notes per row: concurrency, isolation, retries (rows 12-14)

### Takeaway
Pools (1.9.12+) limit op/asset execution across runs, or limit runs when granularity is `run`. Run tag concurrency limits limit run groups. Both are OSS through `dagster.yaml`. Kubernetes gives one pod per run (K8sRunLauncher) or one pod per step (k8s_job_executor), with per-op `dagster-k8s/config`. Retries come at two independent levels: op RetryPolicy and run retries.

### Cited Findings
- **Row 12, pools in the changelog.** 1.9.12: "Adds a top-level argument `pool` to asset/op definitions to replace the use of op tags to specify concurrency conditions"; run-granularity enforcement; run queue config moved into the `concurrency` setting. 1.10.0: run blocking for pools on by default. 1.12.9: Helm `concurrency` setting. 1.12.4: "/" allowed in pool names. — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 12, pools in the docs.** `concurrency.pools.default_limit`, `dagster instance concurrency set database 1`, `granularity: 'run'` (default `op`). Warning: "Dagster does not automatically free concurrency pool slots when a run is cancelled or fails … With a pool limit of 1, a single cancelled run will permanently deadlock all future runs". Fix: `run_monitoring.free_slots_after_run_end_seconds`. — [concurrency-pools.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/operate/managing-concurrency/concurrency-pools.md)
- **Row 12, run tag limits.** `concurrency.runs.tag_concurrency_limits` with `key`/`value`/`limit`, `applyLimitPerUniqueValue`, and the auto tag `dagster/code_location`. — [run-tag-limits.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/operate/managing-concurrency/run-tag-limits.md)
- **Row 12, older history.** `QueuedRunCoordinator` 0.9.18; `tag_concurrency_limits` by 0.12.0; executor `tag_concurrency_limits` within a run 1.1.8. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 13, Kubernetes config.**
  - The `dagster-k8s/config` tag on a job works with `K8sRunLauncher`/`CeleryK8sRunLauncher`. Its keys are `container_config`, `pod_spec_config`, `pod_template_spec_metadata`, `job_spec_config`, `job_metadata`.
  - Under `k8s_job_executor`, job-level config "will _not_ be propagated to any of those step pods. Use the `step_k8s_config` field". An op-level `dagster-k8s/config` tag controls a specific op.
  - Merge is DEEP by default; "before version 1.7.0, the default merge behavior was `SHALLOW`".
  - — [customizing-your-deployment.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/deployment/oss/deployment-options/kubernetes/customizing-your-deployment.md)
- **Row 13, history.** `dagster-k8s/config` 0.9.3; `k8s_job_executor` added 0.11.13 ("executes solids in separate kubernetes jobs"); usable without K8sRunLauncher since 1.3.6; `step_k8s_config` 1.4.6; `per_step_k8s_config` 1.9.1; Helm `env_secrets` → `envSecrets` in 0.10.0. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 14, op retries.** `RetryPolicy`, `Backoff`, `Jitter`, `RetryRequested`. "When a `RetryPolicy` is attached to an op or asset, every exception triggers a retry by default". Use `Failure(allow_retries=False)` to bypass. — [op-retries.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/ops/op-retries.md)
- **Row 14, op retries history.** `RetryPolicy` 0.11.10; backoff/jitter 0.11.12. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
- **Row 14, run retries.** In OSS they are enabled in `dagster.yaml`, with tags `dagster/max_retries`, `dagster/retry_strategy` (default `FROM_FAILURE`), `dagster/retry_on_asset_or_op_failure`, and a `FROM_ASSET_FAILURE` strategy. — [run-retries.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/deployment/execution/run-retries.md)
- **Row 14, run retries history.** Run retries 1.2.0; `retry_on_op_or_asset_failures` 1.6.7; 1.13.2 fix to run retries "not executed by the event log consumer daemon". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)

### Inferences
- **(Inferred.)** Per-vendor secrets per step means setting `env`/`envFrom` with a `secretRef` inside `container_config` of an op/asset-level `dagster-k8s/config` tag under `k8s_job_executor`. This follows from the documented passthrough of the Kubernetes container spec; no Dagster doc example of `envFrom` was read. Under K8sRunLauncher alone (one pod per run), secrets are per run, not per step.
- Pools are not unique to Dagster (Airflow has pools), so this row is not flagged as Dagster-specific.

### Gaps
- No practitioner report was gathered on deadlocks from pool slot leaks beyond the vendor warning.

## Notes per row: versions/staleness, dbt lineage, metadata (rows 15-17)

### Takeaway
Staleness ("Unsynced") comes from `code_version` plus `DataVersion` provenance, and has existed since 1.1 (late 2022). dbt lineage joins the asset graph through `DbtProjectComponent` / `@dbt_assets`, with dbt sources mapped to upstream asset keys. Row-count and schema metadata live under standard `dagster/*` keys on each event.

### Cited Findings
- **Row 15, history.** 1.1.0/1.1.1: "You can now version your asset ops and source assets to help you track which of your assets are stale". 1.2.0: `LogicalVersion` renamed `DataVersion`; user-computed `DataVersion`s can be returned on `Output`. 1.1.10: `RunRequest` `stale_assets_only`. 1.3.14: `get_latest_materialization_code_versions`. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 15, docs.** Without a `code_version`, "Dagster assumes a different code version on every run, which it represents with the run ID". The `data_version` "is a hash of the code version together with the data versions of any inputs". The "Unsynced" label "can appear for three reasons", and the UI offers "Materialize unsynced". — [asset-versioning-and-caching.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/assets/asset-versioning-and-caching.md)
- **Row 15, virtual assets.** 1.13.0: virtual assets (preview) "are supported in staleness calculations, execution planning, and declarative automation". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 16, history.** `load_assets_from_dbt_project` 0.12.12; `@dbt_assets` 1.3.6; `DbtProjectComponent` relocated into `dagster-dbt` 1.10.8; reworked YAML schema (`project`, `translation`) 1.10.11/1.10.12; `cli_args` 1.11.8; Components and `dg` GA in 1.12.0; state-backed components default in 1.13.0. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 16, docs.** `DbtProjectComponent` "is a state-backed component, which compiles and caches your dbt project's manifest". Upstream assets connect through dbt `sources.yml` `meta.dagster.asset_key`. "Dagster supports the dbt Fusion engine as of the 1.11.5 release. Support is in preview … no supported column-level metadata or column lineage." — [dbt/index.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/integrations/libraries/dbt/index.md)
- **Row 17, metadata keys.** `dagster/column_schema` (Type `TableSchema`) and `dagster/row_count` (`int`) are listed in the metadata key reference. — [metadata-and-tags/index.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/assets/metadata-and-tags/index.md); [table-metadata.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/build/assets/metadata-and-tags/table-metadata.md)
- **Row 17, history.**
  - 1.6.12: "[experimental] The metadata key for specifying column schema … changed from `"columns"` to `"dagster/column_schema"`".
  - 1.7.6: "Standardized table row count metadata … to `dagster/row_count`".
  - 1.12.11: UI fix for row_count coming from observations.
  - 1.13.26: dbt `fetch_row_counts()` / `fetch_column_metadata()` no longer fail the step.
  - — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)

### Inferences
- **(Inferred.)** Reading metadata back later uses the event log, via the UI asset catalog, GraphQL, or `DagsterInstance` event-record APIs. The exact Python method names were not verified in this run.
- **(Inferred, labelled.)** Staleness built on `code_version` + `DataVersion` provenance is a Dagster-specific idea. A neutral "stale if code or upstream data version changed" field is Dagster's model.
- **(Inferred, labelled.)** dbt-models-as-assets is not unique to Dagster, but `meta.dagster.asset_key` is Dagster's binding.

### Gaps
- Whether `DataVersion` carries a lifecycle label was not visible on the fetched API page; it was truncated at 100k characters.

## Notes per row: alerting stream and compute logs (rows 18-19)

### Takeaway
OSS has built-in sensors only for run status, plus Slack/Apprise helpers. A single alert stream covering runs, checks, freshness and automation tick failures is the Dagster+ alert-policy feature. Step stdout/stderr goes to object storage through compute log managers configured in `dagster.yaml`, in OSS.

### Cited Findings
- **Row 18, OSS run sensors.** 0.12.3: "Introduced a new decorator `@run_status_sensor`". Slack run-failure sensors existed by 0.13.4. — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md)
- **Row 18, OSS API reference.** No built-in sensor fires on asset check failures or freshness state changes. `run_failure_sensor`/`run_status_sensor` have no label, but their `monitor_all_repositories` is deprecated. — [Schedules/sensors API](https://dagster.io/docs/api/dagster/schedules-sensors)
- **Row 18, OSS check alerting.** The asset checks guide: "If you are using Dagster+, you can choose to alert on asset checks." For OSS, its example runs checks in a separate job and uses "a sensor … to send an email alert when the asset check job fails". — [asset-checks.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/test/asset-checks.md)
- **Row 18, Dagster+ alerts.**
  - Section title "Alerts (Dagster+)".
  - Policy types:
    - Asset: health, materializations, checks, freshness, metrics
    - Run
    - Code location
    - Automation ("tick failure … for schedules or sensors")
    - Agent downtime
    - Insights metric (Experimental)
    - Credit budget (Experimental)
  - Automation alerts fire only on a success-to-failure change. Health alerts notify once per state change.
  - — [alerts/index.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/observe/alerts/index.md); [alert-policy-types.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/observe/alerts/alert-policy-types.md)
  - Webhook alert notifications are "Early Access", with a domain whitelist. — [labs/webhook-alerts/index.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/guides/labs/webhook-alerts/index.md)
  - 1.5.3: "Alert policies can now be set on assets + asset checks (currently experimental)". — [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)
- **Row 19, docs.** `compute_logs` "Controls the capture and persistence of raw stdout and stderr". Options: `LocalComputeLogManager` (default), `NoOpComputeLogManager`, `AzureBlobComputeLogManager`, `GCSComputeLogManager`, `S3ComputeLogManager`. — [oss-instance-configuration.md @8b9a41d](https://github.com/dagster-io/dagster/blob/8b9a41d/docs/docs/deployment/oss/oss-instance-configuration.md)
- **Row 19, history.**
  - 0.8.0: S3ComputeLogManager endpoint override.
  - 0.15.x: `skip_empty_files`.
  - 1.3.3: `show_url_only: true`.
  - 1.3.8: streaming upload of compute logs to Dagster Cloud.
  - — [CHANGES @1.1.7](https://raw.githubusercontent.com/dagster-io/dagster/1.1.7/CHANGES.md); [CHANGES.md](https://raw.githubusercontent.com/dagster-io/dagster/master/CHANGES.md)

### Inferences
- **(Inferred.)** In OSS, a "single stream" can be assembled from:
  - a `run_failure_sensor`
  - a custom sensor over `ASSET_CHECK_EVALUATION` events
  - a custom sensor over `FreshnessStateChange` events
  
  Sensor and schedule tick failures in OSS appear only in the UI and daemon logs; no hook for them was found.
- **(Inferred, labelled.)** "Asset health" (aggregating materialization, check and freshness state into healthy/warning/degraded) is a Dagster+ concept. A neutral model with an "asset health" alert target is Dagster+'s model.

### Gaps
- The `upload_interval` setting of S3ComputeLogManager and its default were not verified.
- No OSS feature for alerting on tick failures was confirmed either way beyond the API page review.

## Rows where the "neutral" concept is really Dagster's model (inferred, labelled)

### Takeaway
Seven of the 19 concepts are framed in Dagster-native terms. A "neutral" model that uses them inherits Dagster semantics, which another orchestrator may have no equivalent for. All of these flags are inference.

### Cited Findings
- Each flag below rests on the cited row notes above. The flag itself is inference.

### Inferences
- **Row 1 (asset as unit of definition, deps between assets).** This is Dagster's "software-defined asset" model, experimental from 0.12.12. Task-centric orchestrators model tasks and infer data from them.
- **Row 3 (observable source asset with data version).** The observation function returning a `DataVersion` that drives downstream automation is Dagster's model.
- **Row 4 (blocking checks).** Gating on ERROR severity inside a run, plus a separate automation condition across runs, is a Dagster idea. The within-run-only limit matters when mapping.
- **Row 5 (manual check result).** "Runless events" (materializations, observations or check results recorded without a run) is a Dagster event-log concept.
- **Row 6 (partition mappings between differently partitioned assets).** This is Dagster's model, especially multi-dimension and time-offset mappings, some of which are beta.
- **Row 10 (AutomationCondition trees).** A Dagster-specific declarative language; job-level use is preview.
- **Row 11 (freshness policy, time-window vs cron with warn/fail).** Dagster's model. It is unstable in labelling, and alerting on it is Dagster+.
- **Row 15 (staleness from code_version + data_version provenance).** Dagster's model.
- **Rows 18 and 11, partly.** "Asset health" and freshness alerting are Dagster+ (commercial) concepts, not OSS.

### Gaps
- None beyond those listed per row.
