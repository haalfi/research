# Follow-up track 2: Auto Loader replay and three Databricks doc conflicts

Method: a verification agent fetched every page in full on 2026-11-07, and each returned HTTP 200.
- **Dates:** the "Last updated" line on docs.databricks.com, `updated_at` on learn.microsoft.com, or
  "published at" on kb.databricks.com.
- **KB search:** about 30 keyword queries against kb.databricks.com `/search.json`, plus a scan of the
  KB sitemap (1,110 URLs).
- **Release notes:** platform notes Jan 2025 to Nov 2026, and DBR 18, 18.1, 18.2 and 19.
- **Not used:** community posts or search extracts.

Labels: **documented** / **inferred**.

## Q1. Re-ingesting files Auto Loader already processed (A8)

- **documented (negative)**: No KB article, release note or options entry gives a way to:
  - replay files that were already processed;
  - edit or remove entries in the checkpoint, RocksDB or `cloud_files_state`;
  - re-run an existing stream for a date range.

  The only KB article about "reprocessing" concerns Kafka offsets.
- **documented (KB)**, after checkpoint loss: "For failed runs, start with a new checkpoint and use
  the `modifiedAfter` option to the stream to ingest files that have a modification timestamp after a
  specific timestamp."
  - https://kb.databricks.com/en_US/streaming/auto-loader-failures-with-javaiofilenotfoundexception-for-sst-and-log-files
    (2024-11-04).
- **documented (KB)**: "Use cloud_files_state to identify any files that have been processed more
  than once." That article uses the function to detect duplicates, not to change state.
  - https://kb.databricks.com/en_US/streaming/duplicates-appearing-in-auto-loader-with-file-notification-feature-despite-set-backfill-interval
    (2024-12-12).
- **documented (KB)**: `spark.databricks.cloudFiles.missingMetadataFile.writeNew=true` regenerates a
  missing checkpoint metadata file. It does not replay files.
  - https://kb.databricks.com/en_US/streaming/auto-loader-job-fails-saying-metadata-file-is-missing-from-checkpoint-directory-
    (2024-11-06).
- **documented (KB)**: Directory listing can miss new files when names stop sorting in order. The fix
  is file notification mode or `cloudFiles.useIncrementalListing=false`.
  - https://kb.databricks.com/en_US/streaming/auto-loader-fails-to-pick-up-new-files-when-using-directory-listing-mode
    (2024-09-12).
- **documented**: `cloudFiles.listOnStart` "performs a full directory listing when the stream starts,
  instead of starting with the continuation token ... Use this option to recover from errors".
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/options (2026-11-05).
  - **inferred**: This option changes how files are found. Nothing says it re-ingests files already
    recorded in the checkpoint.
- **documented**: Auto Loader items in the release notes, Jan 2025 to Nov 2026:
  - file events Public Preview (2025-05-05);
  - `useManagedFileEvents` ungated (2025-09-16);
  - Auto Loader with file events GA (2025-12-10);
  - file events on by default for new external locations (2026-02-12);
  - type widening (2026-03);
  - XML GA (2026-10).

  The DBR 18/18.1/18.2/19 notes add a `discovery_mode` column to `cloud_files_state` and new metrics.
  None of these is a reprocess option.
- **inferred conclusion**: The first-party routes are:
  - a **new checkpoint**, optionally bounded with `modifiedAfter`;
  - `allowOverwrites`, for changed files only;
  - side effects of changing `maxFileAge`.

  None is a supported replay procedure. Re-landing files under a new path (first report, A8) remains
  inference.

## Q2a. Do file-arrival triggers require file events?

- **documented**: The trigger page lists file events as recommended, and gives limits for locations
  without them (50 jobs, 10,000 files).
  - https://docs.databricks.com/aws/en/jobs/file-arrival-triggers (2026-11-06). The Azure mirror is
    the same (2026-11-06).
- **documented**: The best-practices page says "Requires file events to be enabled".
  - https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/best-practices
    (2026-10-07). The Azure mirror is the same.
- **documented (release note, 2025-06-25)**: "File arrival triggers with file events allow a higher
  trigger limit (1,000 per workspace) and removes the 10,000 files per trigger limit."
  - https://docs.databricks.com/aws/en/release-notes/product/2025/june
  - **New fact:** the workspace limit with file events is 1,000 triggers.
- **documented (release note, 2026-02-12)**: "File events are now enabled by default when you create
  new external locations."
  - https://docs.databricks.com/aws/en/release-notes/product/2026/february
- **documented (negative)**: No release note makes file events required.
- **inferred resolution**: **Recommended, not required.** The trigger page is the dedicated
  reference, is newer, and documents behaviour without file events. The best-practices wording
  overstates the requirement.

## Q2b. What is the default for `cloudFiles.useManagedFileEvents`?

- **documented (DBR 18.1 release notes)**: "Auto Loader uses file events by default when loading from
  an external location with file events enabled ... File events aren't used if your stream code sets
  useIncrementalListing or useNotifications. To use directory listing instead, set
  useManagedFileEvents to false."
  - https://docs.databricks.com/aws/en/release-notes/runtime/18.1 (2026-10-28; release March 2026).
  - The DBR 18 LTS notes repeat it under 2026-03-11:
    https://docs.databricks.com/aws/en/release-notes/runtime/18 (2026-11-04).
- **documented**: The file-events FAQ gives the value `if_available` from DBR 18.1.
  - https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/file-events-faq (2026-09-11).
- **documented**: The options page still lists the default as `false`, with valid values true/false,
  and has no note about DBR 18.1 (2026-11-05).
- **inferred resolution**: **On DBR 18.1 and later, Auto Loader uses file events by default where the
  location has them.**
  - The release note settles it. The options table looks stale.
  - The literal value `if_available` appears only in the FAQ.
  - Setting `useIncrementalListing` or `useNotifications` silently turns file events off.

## Q2c. How many times are job tasks retried by default?

- **documented**: "For most configurations, the default setting does not retry any tasks on task
  failure. Serverless jobs auto-optimize retries by default ... Continuous jobs use an exponential
  backoff retry policy."
  - https://docs.databricks.com/aws/en/jobs/configure-task (2026-11-05).
- **documented**: In the API, `max_retries` defaults to 0.
- **documented**: Serverless auto-optimization "retries failed tasks" and is on by default. **No retry
  count is given.**
  - https://docs.databricks.com/aws/en/jobs/run-serverless-jobs (2026-11-06).
- **documented**: Continuous jobs retry with exponential backoff, up to "three for a single task job".
  - https://docs.databricks.com/aws/en/jobs/continuous (2026-11-06).
- **documented**: The notifications page says "By default, tasks are retried three times" (2026-11-06).
- **inferred resolution**:
  - Scheduled or file-arrival jobs on classic compute default to **0 retries**.
  - Serverless jobs retry an **undocumented** number of times unless auto-optimization is turned off.
  - "Three" matches continuous jobs only.
  - The notifications sentence remains unreconciled in the docs.

## Gaps

- No first-party replay procedure exists, and nothing edits per-file state. Coverage is limited: the
  KB was searched by keyword only, and release notes before 2025 were not checked.
- The retry count for serverless auto-optimization is undocumented.
- No first-party page corrects the "Requires file events" wording or the options-table default.
