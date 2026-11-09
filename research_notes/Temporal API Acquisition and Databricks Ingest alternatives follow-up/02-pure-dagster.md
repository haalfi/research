# Alternatives track 2: Pure Dagster compared with Temporal

## Method

A verification agent read the full text of the first-party docs on 2026-11-09. It worked from a
shallow clone of `dagster-io/dagster` at HEAD `55208da` (2026-11-07; CHANGES.md is at 1.13.29).

- `docs.dagster.io` now redirects (308) to `https://dagster.io/docs/...`.
- Quotes marked "live ✓" were checked against the live page.
- No page shows a date, so all are "undated, accessed 2026-11-09".
- Repo paths are relative to `docs/docs/` unless noted.
- No reported or community sources were used.

Labels: **documented** / **inferred**. OSS means open source; D+ means Dagster+ (paid).

## 1. Retries, re-execution, checkpointing, partitions

- **documented (OSS)**: `RetryPolicy(max_retries, delay, backoff, jitter)` can be set on an op, an invocation or a job. "Retry policies also work for asset jobs." Every exception triggers a retry by default. `Failure(allow_retries=False)` "bypass[es] the retry policy". Source: dagster.io/docs/guides/build/ops/op-retries (live ✓).
- **documented**: `RetryRequested(max_retries=1, seconds_to_wait=None)` decides retries from code. Source: `python_modules/dagster/dagster/_core/definitions/events.py`.
- **inferred**: A step waiting in `up_for_retry` stays inside an active run. Retries therefore cannot replace Temporal's infrequent polling, which holds no worker while it waits.
- **documented**: Run retries.
  - OSS needs `run_retries: {enabled: true, ...}` in `dagster.yaml`; D+ has them on by default. They also cover a crashed run process.
  - `FROM_FAILURE` (the default) skips ops that succeeded but "requires an I/O manager that can access outputs from other runs".
  - `FROM_ASSET_FAILURE` + `retry_on_asset_or_op_failure: false` excludes assets already materialized.
  - "the op retry count will reset for each retried run".
  - Source: dagster.io/docs/deployment/execution/run-retries (live ✓).
- **inferred**: Dagster documents no checkpoint inside a step. The step is the smallest unit it re-executes. A paged pull that cannot be re-queried must persist each page plus its cursor itself, in user code, or model pages or dates as partitions. Dagster has no equivalent of Temporal's heartbeat details.
- **documented**: Partitions can be time-based, static, 2-D or dynamic; the docs "recommend limiting … to 100,000 or fewer" per asset. `BackfillPolicy.single_run` exists. Source: dagster.io/docs/guides/build/partitions-and-backfills/partitioning-assets.

## 2. Long waits on an external job

- **documented**: Dagster's own example polls by sleeping inside the asset: `while True: … retrieve(job_id) … time.sleep(30)`. The page says: "after we submit it, we will want to the asset to poll and wait for it to succeed". Source: dagster.io/docs/examples/full-pipelines/llm-fine-tuning/open-ai-job (live ✓).
  - **inferred**: The run worker is held for the whole wait. The job ID is not persisted durably, so a restart submits the job again.
- **documented**: Pipes: "User code should handle launching, polling, and termination of the external process here". Source: `integrations/external-pipelines/dagster-pipes-details-and-customization.md`.
- **documented**: Sensors poll "at regular intervals". `minimum_interval_seconds` is a minimum. `run_key` deduplicates runs, and cursors keep state between evaluations. Source: dagster.io/docs/guides/automate/sensors.
- **documented**: Sensor timeouts (dagster.io/docs/deployment/troubleshooting/sensor-timeouts, live ✓):
  - "The default sensor timeout is 60 seconds".
  - Raising it is "a last resort".
  - "if evaluations require more than 3 minutes to complete, a sensor may not be the correct tool".
  - "Sensors are best used for frequently evaluating small amounts of data to kick off real work down the line."
- **inferred**: A two-step pattern can be built from documented primitives: asset A submits the job and records its ID; a sensor polls with a cursor and `run_key`; asset B reads the result. No first-party page describes it.
- **documented**: Run timeouts and run monitoring:
  - "By default, Dagster jobs have no automatic timeout."
  - `dagster/max_runtime` takes effect only with run monitoring enabled. OSS needs `run_monitoring: enabled: true`; D+ has it always on.
  - Crash detection "only works when using a run launcher other than the `DefaultRunLauncher`".
  - Resume is supported only with the K8s or Docker launcher and executor.
  - Without monitoring, a run "could be left hanging in STARTED status".
  - Sources: dagster.io/docs/deployment/execution/job-timeouts and /run-monitoring (live ✓).
- **inferred**, from `step_delegating_executor.py`: A resumed run re-runs an unhealthy step from the beginning.
- **documented**: Concurrency pools. Without `free_slots_after_run_end_seconds`, "cancelled or failed runs will hold their concurrency slots indefinitely".
- **inferred**: Dagster has no durable timer.

## 3. Landing raw bytes and manifests

- **documented**: I/O managers "aren't required … nor are they the best option in all scenarios". They are a poor fit when "Your pipeline manages I/O on its own". In that case, use `deps`. Source: dagster.io/docs/guides/build/io-managers (live ✓).
  - The ADLS2 I/O manager "Stores outputs as pickle files".
- **documented**: `ADLS2Resource` "Contains a client for both the Data Lake and Blob APIs". It authenticates with a SAS, an account key or `DefaultAzureCredential`. Source: `python_modules/libraries/dagster-azure/.../adls2/resources.py`.
- **inferred**: Writing raw bytes first and the manifest last, with create-only writes, is ordinary Azure SDK code inside the asset. `MaterializeResult` carries the path and hash as metadata. Dagster places no constraint on this.
- **documented**: External assets cover "Files in a data lake populated by a bespoke internal tool" and "A CSV file delivered daily by SFTP". Their status reaches Dagster by a sensor pull or a REST push. Source: dagster.io/docs/guides/build/assets/external-assets (live ✓).

## 4. Operating effort for self-hosted OSS

- **documented**: Replicas per service. The webserver "can have one or more replicas"; for the daemon, replicas are "Not supported."; each code location server can run only one replica. Storage is SQLite by default, or Postgres. Source: dagster.io/docs/deployment/oss/oss-deployment-architecture (live ✓).
- **documented**: Use "only a single `dagster-daemon` process". A single-machine deployment is "suitable for small-scale deployments or for testing purposes".
- **documented**: Schedules, sensors, the run queue and run monitoring "require a long-running `dagster-daemon` process". Source: `deployment/execution/dagster-daemon.md`.
- **inferred**: The daemon is a single point of failure. Run monitoring and resume need K8s or Docker. The docs offer no HA guide for the daemon.

## 5. Detecting late or missing data

- **documented**: Freshness policies.
  - They are labelled "Dagster+" but can be enabled in OSS with `freshness: enabled: True`. They are a preview: "APIs may change".
  - Two kinds: time window (`fail_window`/`warn_window`) and cron.
  - They superseded freshness checks in 1.12 and do not support `SourceAsset`s.
  - Source: dagster.io/docs/guides/observe/asset-freshness-policies (live ✓).
- **documented**, from the `scheduler.py` docstrings: Schedule catch-up after downtime.
  - `max_catchup_runs` defaults to 5 and applies to partitioned schedules only.
  - For a non-partitioned `@schedule`, "only the most recent execution time will be considered".
  - `max_tick_retries` defaults to 0.
  - The migration guide says: "Airflow's `catchup=True` … Dagster doesn't have a direct equivalent".
- **documented (OSS)**: `run_status_sensor` can "send alerts to a monitoring service on run failure".
- **documented (D+ only)**: Alert policies cover run success, failure and time limits, plus freshness. A default policy flags runs longer than 24 hours.
- **inferred**: OSS has no missed-run metrics comparable to Temporal's.

## 6. Secrets and egress

- **documented**: With `EnvVar`, the value "won't be visible in the UI"; with `os.getenv`, it is visible. Source: dagster.io/docs/guides/operate/configuration/using-environment-variables-and-secrets (live ✓).
- **documented (D+ Hybrid)**: "your code never leaves your environment". In OSS, everything runs on your own infrastructure.

## 7. Team 2's Databricks job

- **documented**: `DatabricksWorkspaceComponent` (preview) "triggers a job run … and monitors it". `DatabricksAssetBundleComponent` is also preview.
  - **inferred**: Both conflict with Team 2 owning the trigger.
- **documented (D+, Early Access)**: The Databricks Connection syncs UC metadata and emits materializations when a table updates. It polls every minute. Source: `guides/labs/connections/databricks.md` (live ✓).
- **inferred (OSS)**: To observe without controlling, model the bronze table as an external `AssetSpec` and write a custom sensor that polls the Databricks run or table status.

## Verdict per source type: Pure Dagster against Temporal

| Source type | Verdict | Basis |
|---|---|---|
| Plain REST pull | tie | [D] RetryPolicy, non-retryable `Failure`, schedules, partitions |
| Paged pull that cannot be re-queried | loses (narrowly) | [D] The step is the smallest re-execution unit. [I] Cursor checkpointing is hand-written; there is no heartbeat-details equivalent. |
| Multi-hour vendor job | loses | [D] The documented example sleeps in the asset. Sensors stop at 60 s, and anything over 3 minutes is "not the correct tool". Resume needs K8s or Docker. [I] No durable timer; the split pattern has to be hand-built. |
| SFTP / blob drops | wins (slightly) | [D] The external-asset SFTP sensor example, plus the asset catalog and lineage |

**H2.2, wait-loop half: holds, with qualification.**
- [D] Dagster has no durable timer, the documented wait holds a run, and sensors are unsuitable for long evaluations.
- [I] "Struggle" here means operating cost and fragility, not impossibility.

**"Without a secondary orchestrator": holds if** the team accepts two hand-built pieces:
- the split sensor pattern with a persisted job ID, or a long-running step on K8s or Docker with max_runtime and run monitoring;
- cursor checkpointing inside the asset for paged pulls.

**Fails if** native durable timers or per-page resume inside a step are required.

## Gaps

- The two-step vendor pattern is not documented anywhere.
- Which step state survives a resume is inferred from source code.
- No doc covers daemon HA.
- Not checked: whether OSS freshness policies can notify anyone without D+ alerts.
- Pipes `run_job` was not re-checked.
- No documented maximum for retry delay or `max_runtime`.
