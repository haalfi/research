# Temporal API Acquisition and Databricks Ingest

Brief: [`briefs/Temporal API Acquisition and Databricks Ingest.md`](../briefs/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest.md)
Notes: [`research_notes/Temporal API Acquisition and Databricks Ingest/`](../research_notes/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest/), tracks 01–05.
Research date: 2026-11-07. Every source was accessed on that date. Page dates are the
"last updated" dates the pages show; docs.temporal.io pages show none.

Labels:
- **[D] documented**: first-party docs, read in full.
- **[R] reported**: practitioner or case-study write-up.
- **[I] inferred**: our reasoning from documented facts.

## Bottom line

1. **Temporal for API acquisition holds, provided response bytes never pass through Temporal payloads.**
   - The limits are 2 MB per payload, 4 MB per request, and 50 MB or 51,200 events per history. [D]
   - Temporal documents the claim check as the fix. [D]
   - The proposal, where an activity writes bytes and a manifest, is the application-level form of
     Temporal's own advice: "Pass an identifier for the data, such as a primary key or path". [D]
2. **Q0 verdict: Option A (Temporal) for the paged no-past-date pull and the long-running vendor
   job.** For plain REST pulls it is a near tie. See the Q0 section.
3. **"Trigger on the manifest written last" fails as stated.**
   - A file-arrival trigger fires on any new file under its path. It cannot filter by name or
     wildcard. [D]
   - From DBR 19, Auto Loader skips `_`-prefixed files by default. [D]
   - Auto Loader does not guarantee file order. [D]
   - It holds only if manifests are kept apart from data files, or the trigger is debounced or
     gated. [I]
4. **No documented way exists to replay processed files without a new checkpoint.** Re-landing
   files under a new path works by inference, because Auto Loader identifies a file by its path. [I]
5. **Databricks makes no explicit recommendation for API sources.**
   - Its general guidance says to keep bronze raw and loosely typed, and to land raw data in UC
     volumes. [D]
   - Its API tooling writes straight to tables. [D]
   - "Parsed payloads straight to bronze" conflicts with the raw-fidelity guidance. [I]
6. **Handoffs use documented primitives on each side, but neither vendor documents a
   Temporal → Databricks or Temporal → Dagster pattern.** [D, negative finding]

---

## Q0. Temporal (A) or Databricks job (B) for the API pulls?

Option A: a Temporal workflow writes raw bytes and a manifest into the landing zone.
Option B: a Databricks job writes raw payloads to a UC volume, and Auto Loader picks them up.

### Facts each option rests on

| Dimension | A: Temporal | B: Databricks job |
|---|---|---|
| Retry unit | One activity, i.e. one call or one page. Retry is on by default, with backoff 1 s × 2.0 up to 100 s and **unlimited attempts**. Non-retryable errors are set by a flag where the error is thrown, or by a list of types on the policy. [D] | One task, i.e. a whole rerun. `max_retries` defaults to 0, and `retry_on_timeout` defaults to false. Serverless jobs "auto-optimize retries by default". The notifications page contradicts this with "retried three times". [D] |
| Progress across a retry | Heartbeat details carry progress into the retry. Continue-As-New carries a cursor. [D] | No progress across a task retry. Streaming custom readers can replay offsets only if reads are deterministic. [D] |
| Long waits | Asynchronous Activity Completion: the activity is completed later, from anywhere. Heartbeat timeouts are short for long activities. [D] Holding no compute while waiting is [I]. | No documented pattern for waiting hours on an external job. Serverless runs stop at 7 days and are not retried. [D] |
| Secrets | Workers run in your environment: "access to your compute resources and secrets stays with you". [D] | Secret scopes or UC secrets (per-secret grants, audited). UC HTTP connections: schema level is GA, and the token is limited to its host. [D] |
| Egress | Egress leaves from the org's worker network. The docs cover only worker → Temporal Cloud. [I] | Serverless egress control needs the Enterprise tier. In restricted mode, every API FQDN must be on the allowlist. Classic compute uses VPC and firewall. [D] |
| Late / missing | Schedules: overlap defaults to Skip; catchup window defaults to 1 year (minimum 10 s); can pause on failure; backfill. Start-to-Close timeout is recommended; the schedule-to-start metric can be watched. No recipe for spotting a late or missing run. [D] | Notifications on failure and on a duration threshold, via `RUN_DURATION_SECONDS` health rules. Table freshness is learned from commit history. "Data for date X missing" needs custom logic. [D] |
| Operating effort | The org already runs Temporal (brief). Large payloads add work: History limits force Continue-As-New or batching. [D] | One platform, one job type. Run history is kept 60 days. [D] |

No first-hand source compares the operating effort of the two options for a small team. The
operating-effort row is therefore [I] beyond the facts it cites.

### Per source type [I, built on the [D] facts above]

| Source type | Winner | Why |
|---|---|---|
| Plain REST pull | **Tie.** A if API secrets and egress already sit with the Temporal workers; B if the team wants pulls on one platform and has Enterprise-tier egress control or open classic egress. | Both retry adequately. A retries per call and supports non-retryable errors. B reruns the whole task, so the whole pull must be idempotent. |
| Paged pull that cannot answer for a past date | **A** | Losing a page cannot be repaired by re-querying. A retries per page, carries the cursor in heartbeat or Continue-As-New state, and can persist each page's bytes before moving the cursor. B's task-level retry restarts from the top. Its streaming-reader replay model assumes a deterministic re-read, which this source cannot give. **Condition:** write the bytes before the cursor advances. Temporal's batch-iterator samples pass records through History, so they are not enough on their own. |
| Long-running vendor job (start, wait hours, read) | **A** | Temporal documents async completion and heartbeat timeouts for long activities. Databricks documents no wait pattern, and a polling task holds compute and is capped at 7 days on serverless. B works only as two jobs (start job, then poll-and-read job), which is [I]. |
| SFTP / blob drops | **Neither applies** | These are not API pulls. Files land directly, and the file-arrival plus Auto Loader path handles them (Q2). Databricks also lists SFTP among its own ingestion sources [D]. Whether Temporal should copy SFTP files into the landing zone is outside Q0. |

**Q0 verdict: Option A holds**, on these conditions:
- **Bytes outside payloads:** response bytes leave the activity only as files, and the workflow
  carries only paths.
- **Order of writes:** the manifest is written after the bytes it lists.
- **Retry caps:** every activity has an explicit maximum-attempts cap and a list of non-retryable
  error types.
- **Paged source:** each page is persisted before the cursor advances.

Option B wins only for re-queryable plain REST pulls, and only where the org prefers to keep
secrets and egress inside Databricks rather than in Temporal workers.

---

## Q1. Temporal for bulk acquisition

### Limits [D]

Sources:
- https://docs.temporal.io/cloud/limits
- https://docs.temporal.io/self-hosted-guide/defaults
- https://docs.temporal.io/troubleshooting/blob-size-limit-error
- https://docs.temporal.io/kb/temporal-platform-limits-sheet

| Limit | Value |
|---|---|
| Payload (each Workflow or Activity input and result) | Warns at 512 KB (the AI Cookbook says 256 KB). Fails at 2 MB. Fixed on Cloud; a configurable default when self-hosted. |
| gRPC request (all payloads plus command metadata) | 4 MB. Scheduling many activities in one workflow task can exceed it even when each payload is small (`GRPC_MESSAGE_TOO_LARGE`). |
| Event History | Warns at 10 MB or 10,240 events. Terminates the run at 50 MB or 51,200 events. |
| In-flight activities per run | 2,000. Aim for about 2,000 history events (https://docs.temporal.io/design-patterns/batch-iterator). |

### Is the claim check the documented pattern? Yes. [D]

- **Temporal's own words:** Temporal calls the claim check "the most reliable way to avoid hitting
  payload size limits" (troubleshooting page).
- **Worker best practices:** "store that data external to Temporal in a database or file system.
  Pass an identifier for the data, such as a primary key or path"
  (https://docs.temporal.io/best-practices/worker).
- **Built-in form:** External Storage offloads payloads above a threshold (256 KiB by default) to S3
  or GCS. It is **Public Preview**: "APIs and configuration may change before General Availability"
  (https://docs.temporal.io/external-storage). In Python it ships from SDK 1.25, and the S3 driver
  is marked experimental.
- **The proposal is the application-level form:** an activity writes the files itself. It does not
  depend on the preview feature. [I]
- **Duplicates:** activities run at least once, so the landing zone can receive duplicate files or
  manifests. Downstream must be idempotent (batch-iterator page). [D]

### Long-running external jobs and paged pulls of unknown length

- **Long-running jobs, async completion [D]:** "Asynchronous Activity Completion" lets an Activity
  return without completing. A Temporal Client can then heartbeat it and complete it "from anywhere"
  (https://docs.temporal.io/activity-execution).
  - Long-running activities should use "a relatively short Heartbeat Timeout and a frequent
    Heartbeat" (https://docs.temporal.io/encyclopedia/detecting-activity-failures).
  - Applying this to a vendor job is [I]. The verification vote was 2-1, because the page does not
    mention vendor jobs.
  - A polling activity with retries or timers is an alternative that no source checked in this run
    confirms.
- **Paged pulls [D]:** the documented patterns are Batch Iterator plus Continue-As-New. Each run
  fetches one page in an Activity, carries a cursor as minimal state, and stops when a page comes
  back shorter than `pageSize`. There is no total-count mechanism.
  - Sources: https://docs.temporal.io/design-patterns/batch-iterator,
    https://docs.temporal.io/design-patterns/continue-as-new.
  - The docs do not cover a source that cannot be re-queried. Gap.

### Non-retryable errors [D]

Source: https://docs.temporal.io/design-patterns/non-retryable-errors,
https://docs.temporal.io/encyclopedia/retry-policies

- **(1) Flag at the throw site:**
  - Python `ApplicationError(non_retryable=True)`
  - Go `NewNonRetryableApplicationError`
  - Java `ApplicationFailure.newNonRetryableFailure`
  - TypeScript `ApplicationFailure.nonRetryable`
- **(2) Type list on the RetryPolicy** (`non_retryable_error_types`): it matches the failure type,
  not the message, and is empty by default.
- **Temporal's advice:** "Combine both mechanisms".
- **Defaults:** Activity retries are unlimited by default. Workflows are not retried by default.
- **Mapping to today [I]:** a feed's pre-checks and retry policy map onto non-retryable errors and a
  per-activity policy with an explicit cap.

### Evidence of Temporal used for ingestion: reported, with no byte volumes

- **Loop [R]** (https://loop.com/engineering-blog/temporal-at-loop---evolution-and-scaling,
  2026-03-19):
  - One early production workflow was "Parcel CSV file ingestion to Snowflake".
  - Its workflows coordinate "external APIs, databases, S3, Snowflake, and third-party EDI
    networks".
  - Scale is ">1 billion billable actions per month".
- **Messari [R]** (https://temporal.io/resources/case-studies/messari, 2024-04-15): Temporal was
  used to "improve the reliability of their data ingestion pipeline", replacing cron jobs and
  hand-written retry logic.
- **ANZ Bank [R]** (guest post, https://temporal.io/blog/the-foundation-why-temporal-for-a-data-pipeline,
  2026-07-23):
  - The pipeline is bucket → Pub/Sub → Temporal, with PII checks and a vector DB.
  - "No direct nor indirect PII should appear in the Temporal Web UI".
  - The workflows pass paths, not data. This is [I] from the post's code.
- **Temporal's own docs [D]** list "Data and AI pipelines" as a use case
  (https://docs.temporal.io/evaluate/use-cases-design-patterns).
- **Gap:** no source gives byte volumes or says outright where the bytes are stored.

---

## Q2. File-arrival triggers and Auto Loader

Track 3 has the full quotes. Main sources:
- FAT: https://docs.databricks.com/aws/en/jobs/file-arrival-triggers (2026-11-06)
- Auto Loader options: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/options (2026-11-05)
- Auto Loader FAQ: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/faq (2026-10-22)

### What the trigger requires of the storage [D, FAT unless noted]

- **Location and permissions:**
  - The workspace must have Unity Catalog enabled.
  - The location must be a UC **volume or external location**.
  - It must not contain external tables or catalog or schema managed locations.
  - The user needs READ on the location and CAN MANAGE on the job.
- **File events:** "Databricks recommends" managed file events. Enabling them needs the owner or
  MANAGE privilege. One Auto Loader best-practices page says file events are *required*
  (https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/best-practices,
  2026-10-07), so the pages conflict.
- **Without file events:** at most 50 such jobs per workspace, and at most 10,000 files per watched
  path.
- **With file events:**
  - No file-count limit, but triggers can time out on "too many extraneous file updates".
  - The events cache covers 7 days, and throughput tops out at 2,000 files/s
    (https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/manage-external-locations,
    2026-11-04).
  - File events are not supported on Azure Blob Storage
    (https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-detection-modes).
- **Checking:** best effort, about once a minute; checks subfolders recursively; no wildcards in the
  path.
- **What counts as new:**
  - "Only new files trigger runs". Overwriting a file under the same name does not.
  - With file events, a modification whose metadata is older than the retention window counts as a
    new file. Databricks suggests immutable files.
- **Timing controls:**
  - "Wait after last change" (debounce; every arrival resets it).
  - "Minimum time between triggers" (cooldown).
  - A SQL-condition gate on whether to run (**Beta**,
    https://docs.databricks.com/aws/en/jobs/trigger-sql-conditions).
- **Documented consumer:** Auto Loader with `availableNow` and file events gives exactly-once
  processing. `foreachBatch` gives only at-least-once.

### Replay without resetting the checkpoint

**No first-party procedure exists.** [D, negative: the FAQ has no "reprocess" entry] What is
documented:

- **Identity:** Auto Loader identifies a file by its path. `allowOverwrites=true` also compares
  modification time and reprocesses the whole file. Databricks recommends immutable files and
  `allowOverwrites=false`. Toggling the option on a file-events stream invalidates the continuation
  token. [D]
- **Options that do not replay [D]:**
  - `includeExistingFiles` applies only on a stream's first start.
  - `backfillInterval` skips files already processed and cannot be combined with file events.
  - Reprocessing through `maxFileAge` (minimum 14 days) is described as a risk, not a tool.
- **New checkpoint:** "Changing the checkpoint location effectively means that you have abandoned
  the previous stream and started a new stream." [D]
- **Changing the source path:** in directory-listing mode the source path can change without a new
  checkpoint. File notification mode does not allow this. [D]
- **`cloud_files_state()`:** it reads per-file state. No API edits that state. [D]
- **Workable routes [I]:**
  - (a) Copy the files to a new path such as `replay/<run>/`. Auto Loader identifies files by path,
    and they count as new for the trigger.
  - (b) Run a separate replay stream with its own checkpoint. Databricks advises separate
    checkpoints per stream and source directory.

### Does a trigger on a manifest written last fit? Not as stated.

- **The trigger fires on everything:** it cannot be scoped to a name or suffix, so every data file
  can fire it, not only the manifest. [D + I]
- **Hidden files:** from DBR 19, `ignoredPathSegmentRegex` defaults to `^[._]`, which skips
  `_SUCCESS`-style names. A manifest named `_manifest.json` is invisible to Auto Loader unless that
  setting changes. [D]
- **Filtering and order:** Auto Loader can filter manifests with `pathGlobFilter` ("The path only
  provides a prefix filter"). It "does not guarantee the order in which files are discovered or
  processed". [D]
- **Undocumented pattern:** no Databricks doc covers manifest, marker or claim-check patterns. [D,
  negative]
- **When it fits [I]:**
  - Manifests go in their own prefix and the trigger watches only that prefix. Alternatively, the
    trigger is debounced or SQL-gated.
  - A manifest reader then either opens the files each manifest lists (via `foreachBatch`:
    at-least-once, and the listed files are not tracked in the Auto Loader checkpoint), or Auto
    Loader ingests the data files directly and the manifest serves as a completeness check.

---

## Q3. API sources on Databricks

### Does Databricks recommend landing files first or writing straight to bronze?

**Neither, explicitly.** A search of about 6,400 sitemap URLs found no REST-API ingestion guidance
page.

What is documented:
- **Bronze guidance [D]** (https://docs.databricks.com/aws/en/lakehouse/medallion, 2026-10-29):
  - Bronze "maintains the raw state of the data source in its original formats".
  - "Databricks recommends storing most fields as string, VARIANT, or binary".
  - The medallion pattern is "a recommended best practice but not a requirement".
- **Landing guidance [D]** (https://docs.databricks.com/aws/en/lakehouse-architecture/deployment-guide/delta-lake,
  2026-10-29):
  - "Use Unity Catalog volumes for landing raw data before bronze ingestion".
  - "Don't skip bronze layer (always preserve raw data as source of truth)".
  - The landing zone itself is optional ("Pipelines in larger organizations often have...").
- **API tooling writes straight to tables [D]:**
  - Lakeflow Connect custom connectors: **Beta**
    (https://docs.databricks.com/aws/en/ingestion/custom-connectors, 2026-10-22).
  - The PySpark Python Data Source API, which names REST APIs. It needs DBR 15.4+, and UC HTTP
    connection credentials need 18.1+ (https://docs.databricks.com/aws/en/pyspark/datasources,
    2026-11-04).
  - Zerobus, which is push-only
    (https://docs.databricks.com/aws/en/ingestion/zerobus-overview).
  - The "start with the most managed layer" advice
    (https://docs.databricks.com/aws/en/ingestion/overview, 2026-11-05).
- **Our reading [I]:**
  - The leaning ("parsed payloads straight to bronze") matches the connector tooling but works
    against the raw-fidelity and loose-typing guidance.
  - Landing raw files matches the deployment guide.

### One file-based path or two paths? [I, on these documented facts]

The facts:
- **Auto Loader schema handling:**
  - Text formats are inferred as strings.
  - `addNewColumns` fails the stream once and resumes on restart.
  - `rescue` mode never fails the stream.
  - The rescued-data column records the source file path
    (https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema,
    2026-11-05).
- **Lineage and replay:** the `_metadata` file path and modification time support lineage, and
  `cleanSource` MOVE archives processed files (best-practices page).
- **Run history:** kept 60 days (https://docs.databricks.com/aws/en/jobs/monitor).

What follows:
- **One file path** gives one replay and audit story, one schema-drift and rescue mechanism, and
  file-level provenance. Byte-level replay matters most for the paged source that cannot answer for
  a past date.
- **Two paths** double the schema-drift handling, idempotency design and alerting. A direct path
  loses the original bytes unless the raw body is stored as a string, VARIANT or binary column.
- **No first-party comparison of one path against two exists.**

---

## Q4. Handoffs

### Temporal → Databricks

- **Active run-now handoff [D]:** `POST /api/2.2/jobs/run-now`, or `jobs.run_now` in the Python SDK.
  It takes `job_parameters`, `only`, `queue`, and an **`idempotency_token`** of at most 64
  characters ("exactly one run is launched with that idempotency token").
  - Source: https://raw.githubusercontent.com/databricks/databricks-sdk-py/main/databricks/sdk/service/jobs.py
    (SDK v0.162.0, 2026-11-05).
  - The REST reference page body was not read; the field semantics come from the first-party SDK
    docstrings.
  - Concurrency: the default maximum is 1 concurrent run, and runs over the limit are skipped unless
    queueing is on (queued up to 48 h) (https://docs.databricks.com/aws/en/jobs/advanced,
    2026-11-05).
- **Passive handoff [D]:** the file-arrival trigger (Q2).
- **No first-party Temporal → Databricks ingestion pattern exists [D, negative]:**
  - 0 hits for "databricks" in `temporalio/samples-{python,go,java,typescript,dotnet}` (commits
    2026-11-03) or `temporalio/documentation` (2026-11-06).
  - 0 hits on community.temporal.io.
  - The one joint item is a Databricks blog post on Temporal and Lakebase *agents*, with no Jobs
    calls (https://www.databricks.com/blog/build-durable-agents-temporal-and-lakebase, 2026-09-08).
- **Activity-side form [I]:** an activity calls run-now with a token derived from the manifest ID,
  then polls the run.

### Temporal → Dagster (interim)

- **Push from Temporal [D]:**
  - `DagsterInstance.report_runless_asset_event(...)` accepts materializations, observations and
    check evaluations
    (https://raw.githubusercontent.com/dagster-io/dagster/master/python_modules/dagster/dagster/_core/instance/instance.py;
    https://dagster.io/docs/api/dagster/external-assets-instance-api, 1.12.8).
  - The External assets REST API has `POST /report_asset_materialization/`, `/report_asset_check/`
    and `/report_asset_observation/`. OSS needs no auth header; Dagster+ needs a token
    (https://dagster.io/docs/api/rest-apis/external-assets-rest-api).
- **Pull from Dagster [D]:**
  - A sensor can "regularly poll the external system".
  - Run keys deduplicate ("skip processing requests with previously used run keys"), and cursors
    hold state.
  - The documented examples poll a directory or SFTP, not a database ledger
    (https://dagster.io/docs/guides/automate/sensors,
    https://dagster.io/docs/guides/build/assets/external-assets).
- **GraphQL [D]:** `launchRun` exists but is "still evolving and is subject to breaking changes"
  (https://dagster.io/docs/guides/operate/graphql).
- **No first-party Temporal–Dagster pairing exists [D, negative]:**
  - 0 hits in the Temporal repos.
  - Only passing mentions on the forum.
  - Third-party posts (hoop.dev, Kinde) were not relied on.
- **Interim design [I]:** "Dagster reads the manifest and a ledger row" fits the documented sensor
  model (a cursor over manifests, with run key = manifest ID). The ledger-table poll itself has no
  documented example.

---

## Assumptions and verdicts

| # | Assumption (from the brief) | Verdict | Basis | What it changes |
|---|---|---|---|---|
| A1 | Temporal is suitable for API data acquisition | **Holds if** bytes never pass through payloads or history | 2 MB / 4 MB / 50 MB / 51,200-event limits [D]. Reported ingestion use, no volumes [R]. | Workflows carry only paths and small metadata. Size History for Continue-As-New. |
| A2 | A claim check is the documented pattern | **Holds** | Troubleshooting page, worker best practices, External Storage [D] | Prefer the application-level claim check (activity writes files) over External Storage while that feature is Public Preview. |
| A3 | Long-running vendor jobs fit Temporal | **Holds** (fit is [I]) | Async completion, heartbeat timeouts [D] | Set Start-to-Close, Schedule-to-Close and Heartbeat timeouts for hours. The default Schedule-to-Close is unlimited. |
| A4 | Paged pull with unknown page count fits Temporal | **Holds if** each page's bytes are persisted before the cursor advances | Batch Iterator / Continue-As-New, stop on a short page [D]. No-past-date sources not covered [gap]. | The documented samples return records through History; for this source, write bytes per page and carry only the cursor. |
| A5 | Per-feed retry policy and cheap pre-checks carry over | **Holds if** every activity has an explicit max-attempts cap | Retries unlimited by default; non-retryable flag and type list [D] | A failed pre-check raises a non-retryable error [I]. |
| A6 | Files with a contract land in a zone; a file-arrival job runs Auto Loader into bronze | **Holds if** the landing zone is a UC volume or external location with file events, within the trigger limits | FAT requirements and limits [D] | Without file events: 50 jobs per workspace and 10,000 files per path. Volumes on Azure Blob cannot use file events. |
| A7 | Trigger on a manifest written last | **Fails as stated. Holds if** manifests sit in their own watched prefix (or the trigger is debounced or SQL-gated) and are not `_`-prefixed | No name filter or wildcards; `^[._]` skipped from DBR 19; no order guarantee; no manifest pattern documented [D] | Path layout must separate manifests. A manifest-driven reader is at-least-once and outside the Auto Loader checkpoint [I]. |
| A8 | Processed files can be replayed without resetting the checkpoint | **Holds only by inference** (copy to a new path, or a separate replay stream) | No documented procedure; path identity; new checkpoint = new stream [D] | Define replay as "re-land under a new path" and make bronze writes idempotent. |
| A9 | Every source takes one file path into Databricks | **Holds** (not contradicted; not explicitly recommended) | Raw bronze and "land in volumes" guidance [D]; Databricks API tooling goes direct to tables [D] | Departs from Databricks' connector style, but matches its raw-fidelity guidance. |
| A10 | API leaning: a scheduled Databricks job writes parsed payloads straight to bronze | **Holds if** the raw body is kept (file or string/VARIANT/binary column). **Fails** for the paged no-past-date source if only parsed output is kept. | Medallion bronze guidance [D]; source cannot be re-queried [brief] → [I] | Parsing at acquisition gives up replay for non-re-queryable sources. |
| A11 | Q0: Temporal rather than a Databricks job does the API pulls | **Holds** for the paged and long-running sources. **Tie** for plain REST. | Q0 tables [D + I] | Option B stays viable for re-queryable plain pulls. |
| A12 | Temporal → Databricks handoff via the landing zone (file-arrival), or run-now | **Holds** (each side documented, no joint pattern) | FAT, run-now with idempotency_token [D]; no Temporal↔Databricks doc [D, negative] | If run-now is used, derive the token from the manifest ID, and plan max concurrent runs or queueing. |
| A13 | Interim: Dagster reads the manifest and a ledger row | **Holds** (primitives documented, no joint pattern) | Sensors with cursors and run keys; external-assets REST/instance API [D]; no Temporal↔Dagster doc [D, negative] | A ledger-table poll is undocumented but ordinary sensor code. Alternatively, Temporal pushes materializations [I]. |

---

## Where first-hand evidence is missing

- **Ingestion evidence:** no byte-volume evidence for Temporal-based ingestion. The case studies give
  action counts only.
- **No-past-date sources:** neither vendor covers a paged source that cannot be re-queried.
- **Databricks gaps:** no Databricks page covers:
  - API-specific landing guidance;
  - a comparison of one ingest path against two;
  - waiting hours on an external job;
  - replay without a new checkpoint;
  - manifest or marker files.
- **Doc conflicts:**
  - Is the file-events setting required or only recommended for file-arrival triggers? (FAT vs best
    practices)
  - The `useManagedFileEvents` default: `if_available` from DBR 18.1 (file events FAQ) vs `false`
    (options page).
  - Task retry default: none (configure-task and API) vs three (notifications).
- **No joint patterns:** no first-party Temporal → Databricks or Temporal → Dagster integration doc.
  The GitHub org-wide search in this session was restricted, so this rests on 5 cloned sample repos,
  the docs repo, the forum and web search.
- **Operating effort:** no source compares the two options' operating effort for a small team.
- **Not read:**
  - Temporal's "missed schedule actions" troubleshooting page.
  - The Databricks run-now REST reference body; SDK docstrings were used instead.
- **Unclear trigger behaviour:** whether one trigger run covers many files or one file, and how the
  trigger treats `_`-prefixed files.

## Method

1. **Workflow run:** a 5-angle deep-research run (`wf_d4ed6c0d-99f`) fetched 23 sources and
   extracted 112 claims. The 25 claims it verified with three votes each all concerned Temporal, and
   all were confirmed (track 01).
2. **Leads:** its Databricks and Dagster claims fell outside the verification budget and were kept as
   leads only (track 02).
3. **Full-text tracks:** three tracks then re-read the first-party pages in full and confirmed or
   corrected each lead (tracks 03–05).
4. **Corrections recorded there:**
   - The FAQ has no "reprocess" entry.
   - The 7-day `maxFileAge` belongs to generic file streams, not Auto Loader.
   - The deployment-guide quote reads "before bronze ingestion".
