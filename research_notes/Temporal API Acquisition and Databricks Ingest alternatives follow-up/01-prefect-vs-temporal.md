# Alternatives track 1: Prefect 3.x OSS compared with Temporal

## Method

A verification agent read full first-party documentation on 2026-11-09, taken from shallow clones of two repos:

- `PrefectHQ/prefect` at `b0479c0` (2026-11-06; latest release notes are OSS 3.9.2).
- `temporalio/documentation` at `7754e61` (2026-11-08).

Prefect's live pages render client-side, so every quote comes from the repo sources. Live URLs are given, but those pages were not fetched. The pages are undated: "undated, accessed 2026-11-09".

Labels: **documented** / **reported** / **inferred**. "Cloud only" means Prefect Cloud (paid).

## 1. Retries, persistence, resuming, non-retryable errors

- **documented (OSS)**: Flow retries apply "when the flow raises an exception or returns a `Failed` state". Task retries are configured separately. Options:
  - `retry_delay_seconds` (a single value or a list), `exponential_backoff`, `retry_jitter_factor`;
  - global defaults.

  Source: https://docs.prefect.io/v3/how-to-guides/workflows/retries
- **documented (OSS)**: Prefect has no non-retryable error type. It uses a predicate: "If a callable passed to `retry_condition_fn` returns `True`, the task will be retried. Otherwise, the task will exit with an exception". The example skips 401 and 404. This works on tasks only.
  - **reported**: The 3.9 release notes include "Fix silently skipped task retries in `retry_condition_fn`" (#23397).
- **documented (OSS)**: Results are not persisted by default. "By default these results are not persisted". To persist them, set `persist_result=True` or `PREFECT_RESULTS_PERSIST_BY_DEFAULT`. With ephemeral infrastructure, the default local storage "does not persist results across runs", so remote storage such as Azure Blob Storage is recommended. Source: https://docs.prefect.io/v3/advanced/results
- **documented (OSS)**: "Caching requires result persistence, which is off by default."
  - The default key is "the inputs … the code definition … the prevailing flow run ID".
  - Policies: `DEFAULT`, `INPUTS`, `TASK_SOURCE`, `FLOW_PARAMETERS`, `NO_CACHE`, `RUN_ID`.
  - Purpose: caching should "ensure that your pipelines are idempotent when retrying".

  Source: https://docs.prefect.io/v3/concepts/caching
- **documented (OSS)**: A retried flow run "keeps its original ID and parameters". A retried parent reuses a nested flow's result if it was persisted.
- **documented (OSS)**: Transactions. "A transaction runs at most one time, and produces a result record upon completion at a unique address". Commit modes are `LAZY`, `EAGER` and `OFF`. However, "`EAGER` alone does not guarantee that a task body executes only once." Source: https://docs.prefect.io/v3/advanced/transactions
- **inferred**: A paged pull can skip pages it already fetched under these conditions:
  - each page is one task;
  - results are persisted to remote storage;
  - the cache key is deterministic (`INPUTS` or `DEFAULT` within the same run).

  No page states this outright.

## 2. Long waits, timeouts, crashes

- **documented (OSS)**: `pause_flow_run` "Pauses the current flow run by blocking execution until resumed". The timeout defaults to 1 h and polling to every 10 s. Source: https://docs.prefect.io/v3/api-ref/python/prefect-flow_runs
- **documented (OSS)**: `suspend_flow_run` lets the flow "exit" at the next task and "tears down infrastructure". It needs a deployment and `persist_result`. It has no timeout by default.
  - States: Suspended means "The run code has stopped executing and the process has exited."
  - **reported**: The 3.6 release notes include "Remove default timeout on `suspend_flow_run`".
- **documented (OSS)**: Automations offer `resume-flow-run` and `suspend-flow-run` actions to everyone (OSS and Cloud). `resume_flow_run()` can also be called from code. Source: https://docs.prefect.io/v3/concepts/automations
- **inferred**: Prefect has **no durable timer**. The options for an hour-long vendor job are:
  - a scheduled poller that calls `resume_flow_run`;
  - an automation driven by events;
  - a start flow plus a separate flow that collects the result;
  - `time.sleep` or `pause_flow_run`, both of which hold a process.

  After a resume, the flow re-executes from the top, and tasks that already completed are served from cache.
- **documented (OSS)**: `timeout_seconds` on a flow marks it failed, but "Flow execution may continue until the next task is called". A sync task timeout "cannot interrupt blocking operations" such as `time.sleep()`. Source: https://docs.prefect.io/v3/how-to-guides/workflows/write-and-run
- **documented**: Crashes are terminal. Crashed is "a terminal state … infrastructure issue".
  - Zombie runs can "appear stuck in a `Running` state". Heartbeats default to every 180 s.
  - Automatic marking of stuck runs as Crashed is **Cloud only** ("This managed automation is only available in Prefect Cloud"). OSS users must build that automation themselves.

  Source: https://docs.prefect.io/v3/advanced/detect-zombie-flows
- **inferred**: A crashed run is not resumed or restarted automatically. Flow `retries` are documented only for exceptions and the Failed state. Temporal, by contrast, continues the work on another worker.

## 3. Paged pulls with an unknown page count

- **documented (OSS)**: Native Python control flow ("while loops") and tasks created at runtime are supported. `.map()` and `.submit()` exist. Source: https://docs.prefect.io/v3/get-started
- **inferred**: A cursor of unknown length needs a sequential `while` loop of task calls.
- **documented**: OSS documents no limit on task runs per flow. The database-maintenance guide names the `task_run` and state-history tables as the ones that grow large and asks for monitoring of bloat and autovacuum. Source: https://docs.prefect.io/v3/advanced/database-maintenance
- **inferred**: Prefect has no Continue-As-New and does not need one. Growth of the database becomes the operator's job instead.

## 4. Operating effort, self-hosted

- **documented**: Prefect. Source: https://docs.prefect.io/v3/concepts/server ; https://docs.prefect.io/v3/advanced/self-hosted ; https://docs.prefect.io/v3/how-to-guides/self-hosted/docker-compose
  - "SQLite (default): Recommended for lightweight, single-server deployments … requires essentially no setup"
  - PostgreSQL 14.9+ with `pg_trgm` "Best for production use, high availability".
  - Multiple servers need PostgreSQL, Redis and a load balancer.
  - The Docker Compose example runs 5 services.
  - Cloud adds RBAC, audit logs and SSO.
- **documented**: Prefect workers are "lightweight polling services" that need outbound HTTPS only. Push work pools and managed pools are Cloud only.
- **documented**: Temporal. Source: https://docs.temporal.io/temporal-service/temporal-server ; https://docs.temporal.io/temporal-service/persistence ; https://docs.temporal.io/self-hosted-guide/production-checklist
  - Four services (Frontend, History, Matching, Worker). Production runs each one separately.
  - The History shard count "cannot be changed".
  - Persistence is Cassandra, PostgreSQL or MySQL. SQLite is for development and testing only.
  - You operate the Visibility store yourself.
  - Temporal says self-hosting "takes significant engineering and ongoing effort".
- **documented**: Temporal Cloud runs on AWS and GCP at "$50 per million Actions". Source: https://docs.temporal.io/evaluate/cloud
  - Azure availability was not checked.
- **inferred**: On a single node, Prefect clearly wins. The difference narrows with high availability, though Prefect still has fewer moving parts.

## 5. Detecting late and missing runs

- **documented (OSS)**: The scheduler only creates runs: at most 100 runs and 100 days ahead.
  - A run is Late once its start time passes without it moving to Pending (15 s by default), "Typically means that a worker did not pick up the run."
  - Source: https://docs.prefect.io/v3/concepts/schedules ; https://docs.prefect.io/v3/concepts/states
- **reported**: The 3.1 release notes include "Remove `max_active_runs` and `catchup` fields".
  - **inferred**: Prefect has no catch-up window.
  - **documented**: The closest equivalent to an overlap policy is the deployment's `concurrency_limit` with `collision_strategy` set to `ENQUEUE` or `CANCEL_NEW`.
- **documented (OSS)**: Proactive triggers fire on a missing event. Example: "if a `prefect.flow-run.Completed` event is not seen within 60 seconds". **Metric triggers are Cloud only.** Source: https://docs.prefect.io/v3/concepts/event-triggers
- **documented (Cloud only)**: SLAs ("only available in Prefect Cloud", experimental). Webhooks, `send-email-notification` and incidents are also Cloud only. The OSS `send-notification` action works through notification blocks.

## 6. Secrets and egress

- **documented (OSS)**: The Secret block is "encrypted at rest". Variables "are not Encrypted". Source: https://docs.prefect.io/v3/how-to-guides/configuration/store-secrets
- **documented**: Hybrid model: "your flow code stays within your storage and execution infrastructure". Workers need only outbound HTTPS on port 443.

## 7. Databricks

- **documented**: `prefect-databricks` 0.4.2 offers "Trigger an existing Databricks job and wait for it to complete". This matches the earlier finding.
  - **inferred**: The wait runs inside a live flow process.

## Verdict per source type

| Source type | Prefect compared with Temporal | Basis |
|---|---|---|
| Plain REST pull | Tie on retries; Prefect plausibly better on ergonomics | [D] / [I] |
| Paged pull that cannot be re-queried | **Prefect loses** | [D] It can be built with one task per page, persisted results and an INPUTS cache or transaction. [D] But a crash is terminal, and in OSS zombie detection must be built by hand. [I] There is no automatic resume. |
| Multi-hour vendor job | **Prefect loses** | [D] `pause_flow_run` blocks; `suspend_flow_run` needs an external resume. [I] No durable timer. |
| SFTP / blob drops | Tie | [I] Both poll on a schedule. [D] Webhooks are Cloud only. [reported] Prefect has no catch-up. |
| Operating effort | **Prefect wins** on a single node; the gap narrows with HA | [D] |
| Late and missing detection | Tie to slight loss | [D] Metric triggers, SLAs and zombie detection are Cloud only. [I] There are no catch-up or missed-run metrics. |

**Verdict on H2.1: holds if.**

- **Lower operating overhead**: holds for a single Prefect server.
- **Ergonomics**: rests only on Prefect's own claims [I].
- **"Trade-offs in multi-day stateful polling"**: this is understated. It is a **confirmed gap**:
  - no durable timer;
  - crashes are terminal;
  - resuming page by page needs opt-in persistence plus the right cache policy.
- **"Event-sourced history handling"**: this is the wrong axis. Prefect does not replay history. Its real costs are resume semantics and database growth.
- **Overall**: H2.1 holds only if Team 1 accepts three things:
  1. rebuilding source type 3 as split flows or as suspend plus an external resume;
  2. a self-built zombie automation plus persisted, cached pages for type 2;
  3. no catch-up semantics.

  Otherwise it fails for source types 2 and 3.

## Gaps

- **Not fetched**: the live pages.
- **Inferred, not stated in the docs**:
  - that a retried flow skips completed tasks;
  - whether Crashed runs are ever retried automatically;
  - whether Late runs execute after an outage.
- **Not documented**: a limit on task runs per flow.
- **Not verified**:
  - whether an OSS automation can act as a timer;
  - what the removed `catchup` field did.
- **Not checked**:
  - Temporal Cloud availability on Azure;
  - Prefect Cloud pricing;
  - prefect-azure result storage on ADLS.
- **No independent source**: nothing compares the two tools on ergonomics or operating effort.
