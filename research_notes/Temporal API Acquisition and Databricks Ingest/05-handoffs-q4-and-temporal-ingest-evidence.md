# Track 5: Handoffs (Q4), Temporal for ingestion (Q1e), Temporal-side Q0 facts

Method: a verification agent read the sources on 2026-11-07. Some pages were read as raw first-party
source files, where quotes are exact:
- Databricks SDK `jobs.py`, latest release v0.162.0 (2026-11-05)
- `temporalio/documentation` at its 2026-11-06 commit
- Dagster `instance.py` on master

Pages read through WebFetch may have quotes cut after about 125 characters.
Labels: **documented** / **reported** / **inferred**.

## Q4a. Temporal → Databricks

- **documented**: Run-now is `POST /api/2.2/jobs/run-now`, called in the SDK as `jobs.run_now(job_id, idempotency_token, job_parameters, only, queue, ...)`.
  - https://raw.githubusercontent.com/databricks/databricks-sdk-py/main/databricks/sdk/service/jobs.py (v0.162.0, 2026-11-05).
  - The REST reference body was not read; field semantics come from the SDK docstrings.
- **documented** idempotency_token: "If a run with the provided token already exists, the request does not create a new run but returns the ID of the existing run instead." Also "exactly one run is launched with that idempotency token", and the token is at most 64 characters. (jobs.py)
- **documented** job_parameters: these override the job's defaults. Per-task `notebook_params` and `python_params` are deprecated in favour of job parameters. (jobs.py)
- **documented** `only`: runs a subset of tasks. Source: https://docs.databricks.com/gcp/en/jobs/run-now (2026-09-11).
- **documented**: Concurrency and queueing (https://docs.databricks.com/aws/en/jobs/advanced, 2026-11-05):
  - Default max concurrent runs is 1, and "Databricks skips the run if the job has already reached its maximum number of active runs."
  - With queueing on, a run is "queued for up to 48 hours". Queueing is on by default for UI jobs created after 2024-04-15.
  - Databricks recommends one concurrent run per job (run-now page).
- **documented**: The passive alternative is a file-arrival trigger. See track 3; https://docs.databricks.com/aws/en/jobs/file-arrival-triggers (2026-11-06).
- **documented** (adjacent only): A Databricks blog pairs Temporal with Lakebase for durable agents, not for ingestion or Jobs. Its sample repo `temporal-sa/temporal-lakebase-agent` makes no Jobs API calls.
  - https://www.databricks.com/blog/build-durable-agents-temporal-and-lakebase (2026-09-08).
- **documented (negative)**: I found no first-party Temporal → Databricks ingestion or Jobs handoff in any form: doc, sample or blog.
  - `temporalio/samples-{python,go,java,typescript,dotnet}` (2026-11-03) and `temporalio/documentation` (2026-11-06): 0 hits for "databricks".
  - community.temporal.io: 0 topics.
  - temporal.io mentions Databricks only in passing, as a destination for exported history.
- **reported, not read**: A third-party hoop.dev post on Temporal calling the Databricks API. Not relied on.
- **inferred**: A Temporal activity would call run-now with a deterministic idempotency_token derived from the manifest ID, then poll the run status. No doc describes this.

## Q4b. Temporal → Dagster (interim)

- **documented**: `DagsterInstance.report_runless_asset_event(...)` accepts AssetMaterialization, AssetObservation, AssetCheckEvaluation and freshness events: "Record an event log entry related to assets that does not belong to a Dagster run."
  - https://raw.githubusercontent.com/dagster-io/dagster/master/python_modules/dagster/dagster/_core/instance/instance.py
  - https://dagster.io/docs/api/dagster/external-assets-instance-api (1.12.8)
- **documented**: The External assets REST API has three endpoints: `POST /report_asset_materialization/{key}`, `/report_asset_check/` and `/report_asset_observation/`.
  - Materialization takes optional metadata, data_version and partition.
  - The check endpoint requires `passed` and `check_name`.
  - No auth header is needed on Dagster OSS; Dagster+ needs `Dagster-Cloud-Api-Token`.
  - https://dagster.io/docs/api/rest-apis/external-assets-rest-api ; https://dagster.io/docs/guides/build/assets/external-assets
- **documented**: A sensor can "regularly poll the external system and pull information about the external asset into Dagster". The guide's example polls SFTP.
  - Run keys dedupe: "Dagster will skip processing requests with previously used run keys".
  - Cursors hold custom state.
  - A sensor is not enabled on deploy unless its default status is RUNNING.
  - The cursor example lists a directory by modified time. No example polls a ledger table.
  - https://dagster.io/docs/guides/automate/sensors (1.12.8)
- **documented**: `@asset_sensor` watches materializations. The docs do not say whether events reported through the REST API trigger it.
  - https://dagster.io/docs/guides/automate/asset-sensors
- **documented**: The GraphQL `launchRun` mutation and `DagsterGraphQLClient.submit_job_execution` exist. Dagster warns: "The GraphQL API is still evolving and is subject to breaking changes."
  - https://dagster.io/docs/guides/operate/graphql
- **documented (negative)**: I found no first-party doc, sample or blog that pairs Temporal with Dagster.
  - 0 hits in the Temporal sample and documentation repos.
  - Two forum topics mention Dagster only in passing (t/2293, 2021-06-02; t/13084, 2024-08-06).
  - Limitation: the org-wide GitHub search in this session was restricted.
- **reported, not read in full**: hoop.dev and Kinde articles pair Dagster with Temporal. These are third-party sources and were not relied on.

## Q1e. Temporal used for data ingestion

- **reported**: Loop, in its engineering blog (2026-03-19, Oxford Wang):
  - One early production workflow was "Parcel CSV file ingestion to Snowflake".
  - Invoices carry "up to hundreds of thousands of charges".
  - Load is ">1 billion billable actions per month".
  - Workflows coordinate "external APIs, databases, S3, Snowflake, and third-party EDI networks".
  - No byte volumes are given, and the post does not say where bytes travel.
  - https://loop.com/engineering-blog/temporal-at-loop---evolution-and-scaling
- **reported**: Messari case study (2024-04-15). The use case is labelled "Data pipeline". The aim was to "improve the reliability of their data ingestion pipeline", replacing cron jobs and hand-built retry logic. No volumes are given, and it does not say where bytes travel.
  - https://temporal.io/resources/case-studies/messari
- **reported**: ANZ Bank guest post on temporal.io (2026-07-23):
  - CSV files land in a bucket, arrive via a Pub/Sub event, and go through PII checks, classification, embeddings and a vector DB.
  - "No direct nor indirect PII should appear in the Temporal Web UI."
  - **inferred** from its code: workflows pass paths and IDs, not data.
  - https://temporal.io/blog/the-foundation-why-temporal-for-a-data-pipeline
- **reported**: A Temporal blog (2024-04-22) calls Temporal "a great fit for automating data engineering processes" and cites Neosync and Descript.
  - https://temporal.io/blog/ai-ml-and-data-engineering-workflows-with-temporal
- **documented**: The Temporal docs list "Data and AI pipelines" as a use case, pointing to Fan-out Child Workflows, Batch Iterator and Sliding Window.
  - https://docs.temporal.io/evaluate/use-cases-design-patterns
- **documented**: Worker best practices:
  - "A Workflow Execution may be terminated if any single payload exceeds 2 MB or if the entire Event History exceeds 50 MB."
  - "store that data external to Temporal in a database or file system. Pass an identifier for the data, such as a primary key or path".
  - https://docs.temporal.io/best-practices/worker
- **documented**: The docs contain no statement that Temporal is "not for bulk data". The guidance is the limits plus the claim check.
- **reported**: In a forum thread, a user runs ETL chains in which activities read and write the target tables directly, so data never returns to the workflow. Temporal staff replied: "a good use case!"
  - https://community.temporal.io/t/8104 (2023-05)

## Q0, Temporal side

- **documented** Schedules (https://docs.temporal.io/schedule):
  - The default Overlap Policy is `Skip`.
  - "The Catchup Window controls how late an automated Action can be taken. The default is one year". It can be set as low as 10 s.
  - A run that ends in failure or timeout can auto-pause the schedule ("pause on failure").
  - Backfill runs the actions of a past period now.
- **documented** Activity timeouts (https://docs.temporal.io/encyclopedia/detecting-activity-failures):
  - "We strongly recommend setting a Start-To-Close Timeout."
  - Schedule-To-Start and Schedule-To-Close both default to ∞.
  - Instead of a Schedule-To-Start timeout, the docs suggest watching the `temporal_activity_schedule_to_start_latency` metric.
  - For long-running activities they recommend "a relatively short Heartbeat Timeout and a frequent Heartbeat". Heartbeat details carry progress across retries.
- **documented** Workflow timeouts: "we generally do not recommend setting Workflow Timeouts". The Execution Timeout default is ∞.
  - https://docs.temporal.io/encyclopedia/detecting-workflow-failures
- **inferred**: The docs give no recipe for detecting a late or missing scheduled run. Combining a short catchup window, pause-on-failure, timeouts and metrics is our construction.
- **documented**: "Temporal Cloud does not execute your application code. Workers run in your environment ... access to your compute resources and secrets stays with you."
  - https://docs.temporal.io/evaluate/cloud
- **inferred**: Egress to the source APIs therefore leaves from the org's worker network. The docs cover only egress from workers to Temporal Cloud.

## Gaps

- The run-now REST reference body was not read; field semantics come from the SDK docstrings.
- No doc says whether REST-reported Dagster events trigger asset sensors.
- No Dagster example polls a ledger table.
- No doc gives a cap on queued Databricks runs, or says whether a file-arrival trigger runs once per file or per batch.
- No case study gives byte volumes or states where bytes are stored.
- docs.temporal.io pages are undated.
- The Temporal page on missed schedule actions was not read.
