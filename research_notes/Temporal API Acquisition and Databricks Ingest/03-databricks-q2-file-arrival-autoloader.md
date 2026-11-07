# Track 3: File-arrival triggers and Auto Loader (Q2)

Method: a verification agent downloaded each first-party page in full on 2026-11-07 and read the
relevant sections. Labels: **documented** / **reported** / **inferred**. "Last updated" dates are
those shown on the pages.

| Key | URL | Last updated |
|---|---|---|
| FAT | https://docs.databricks.com/aws/en/jobs/file-arrival-triggers | 2026-11-06 |
| FAT-Az | https://learn.microsoft.com/en-us/azure/databricks/jobs/file-arrival-triggers | ms.date 2026-11-06 |
| OPTS | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/options | 2026-11-05 |
| FAQ | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/faq | 2026-10-22 |
| PROD | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/production | 2026-11-05 |
| FNM | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-notification-mode | 2026-10-07 |
| FEX | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-events-explained | 2026-10-07 |
| BP | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/best-practices | 2026-10-07 |
| DLM | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/directory-listing-mode | 2026-09-11 |
| DET | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-detection-modes | 2026-09-11 |
| PAT | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/patterns | 2026-09-11 |
| CS | https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/clean-source | 2026-09-11 |
| CFS | https://docs.databricks.com/aws/en/sql/language-manual/functions/cloud_files_state | 2026-09-11 |
| EXTLOC | https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/manage-external-locations | 2026-11-04 |
| FEFAQ | https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/file-events-faq | 2026-09-11 |
| SQLC | https://docs.databricks.com/aws/en/jobs/trigger-sql-conditions | 2026-11-06 |

No page was unreachable.

## Q2a. What file-arrival triggers require of the storage

- **documented** (FAT): The workspace must have Unity Catalog, and the location must be a UC volume or a UC external location: "You must use a storage location that is either a volume or an external location configured in Unity Catalog."
- **documented** (FAT): Managed file events are recommended. Enabling them requires the external location's owner or the MANAGE privilege. Volumes on such a location inherit file events.
  - **Conflict:** BP says the trigger "Requires file events to be enabled".
- **documented** (FAT): The user needs READ on the storage location and CAN MANAGE on the job.
- **documented** (FAT): The trigger makes a best-effort check about once a minute: "make a best effort to check for new files every minute". It checks recursively, and the path takes no wildcards.
- **documented** (FAT): The path must not contain external tables or the managed locations of catalogs and schemas.
- **documented** (FAT): "Only new files trigger runs. Overwriting an existing file with a file of the same name does not trigger a run."
  - With file events, a modification whose metadata is older than the retention window counts as a new arrival.
  - Databricks suggests immutable files.
- **documented** (FAT, FAT-Az): Without file events, a workspace allows at most 50 such jobs, and each configured subpath may hold at most 10,000 files.
  - With file events there is no file-count limit, but "Triggers can error on time out when there are too many extraneous file updates".
- **documented** (FAT): Two timing settings, which can be combined:
  - "Wait after last change" debounces: "each new arrival resets the timer".
  - "Minimum time between triggers" is a cooldown that starts after a run completes.
- **documented** (FAT): On S3 and GCS, a missing path is evaluated "with no error".
- **documented** (SQLC, Beta): A SQL condition can gate whether a fired trigger starts a run.
- **documented** (EXTLOC): File events have their own limits.
  - The cache holds metadata only for files modified in the last 7 days.
  - Throughput is 2,000 files per second.
  - File events need a UC external location object.
- **documented** (FAT): The documented consumer is Auto Loader, run with `availableNow` and `useManagedFileEvents=true`, with the checkpoint outside the watched path. This gives exactly-once processing; `foreachBatch` gives only at-least-once.

## Q2b. Replaying processed files without resetting the checkpoint

- **documented** (FAQ): The FAQ has no "reprocess files" entry, and no first-party page gives a replay or reprocess procedure.
- **documented** (FAQ): Auto Loader identifies a file by its path. With `allowOverwrites=true` it also compares the last-modified time and then reprocesses the whole file. Caveats on that page:
  - No guarantee which intermediate version is processed.
  - Duplicates are the user's job to handle.
  - Databricks recommends immutable files and `allowOverwrites=false`.
- **documented** (FAQ): Changing `allowOverwrites` on a file-events stream invalidates the continuation token. The documented recovery is `listOnStart=true` plus `validateOptions=false`.
- **documented** (OPTS): `includeExistingFiles` is evaluated only on a stream's first start.
- **documented** (PROD, OPTS): `backfillInterval` skips files that were already processed, and it must not be used with managed file events.
- **documented** (PROD, BP): Reprocessing through `cloudFiles.maxFileAge` (minimum 14 days) is presented as a risk, not a tool.
  - **Correction to the lead:** the 7-day `maxFileAge` belongs to the generic file-stream options, not to Auto Loader.
- **documented** (FAQ): "Changing the checkpoint location effectively means that you have abandoned the previous stream and started a new stream."
  - **inferred:** A separate replay stream with its own checkpoint would leave the main checkpoint untouched. No page names this as a pattern. BP says to use separate checkpoints for each stream and source directory.
- **inferred**, with documented support (identity by path; CS says files moved inside the source path are "ingested again"): Copying a file to a new path, such as a `replay/<run>/` prefix, would make Auto Loader ingest it again and would count as a new file for the trigger. No page offers this as a replay method.
- **documented** (DLM): In directory listing mode, the input path can be changed without a new checkpoint. File notification mode does not support this.
- **documented** (CFS): `cloud_files_state()` reads per-file state. No documented API edits or removes that state.

## Q2c. Does a trigger on a manifest written last fit?

- **documented** (FAT): The trigger cannot be scoped to a file name or suffix. It has no wildcards, and its only settings are location, cooldown and debounce.
  - **inferred:** Every data file can fire the trigger, not only the manifest. The documented tools for holding a run back are the debounce and the SQL condition (Beta).
- **documented** (PAT): Auto Loader filters by suffix with `pathGlobFilter`: "The path only provides a prefix filter."
- **documented** (OPTS): In DBR 19+, `ignoredPathSegmentRegex` defaults to `^[._]`, which skips `_` and `.` names, "including Spark-internal marker files such as _SUCCESS".
  - **inferred:** A manifest named `_manifest.json` would be invisible to Auto Loader by default.
- **documented** (DET, FNM): "Auto Loader does not guarantee the order in which files are discovered or processed".
  - **inferred:** "Manifest last" gives no ordering guarantee once files reach Auto Loader.
- **inferred**: A manifest-driven reader would use `pathGlobFilter` to stream only manifests, then open the files each manifest lists, for example in `foreachBatch`. Two documented limits apply:
  - It would be at-least-once.
  - Files opened through a manifest are not tracked in the Auto Loader checkpoint.
- **documented** (DET, FNM, FEX): Detection-mode requirements:
  - File events need UC and DBR 14.3 LTS or later, and are not supported on Azure Blob Storage.
  - UC volumes support directory listing (DBR 13.3+) and file events (14.3+).
  - A stream on file events should run at least every 7 days, or it relists.
- **documented, pages disagree**: The `useManagedFileEvents` default is `if_available` from DBR 18.1 (FEFAQ), but `false` (OPTS).
- **Gap**: No Databricks doc covers manifest, marker or claim-check patterns for Auto Loader or file-arrival triggers.

## Gaps

- No replay procedure, and no API to reset per-file state.
- No doc on manifest or marker patterns.
- No doc on whether the trigger ignores `_`- or `.`-prefixed files.
- No definition of a "new file" for the trigger beyond the overwrite rule.
- Trigger behaviour while a run is still in progress is not covered.
- Two pairs of pages conflict:
  - FAT and BP disagree on whether file events are required or only recommended.
  - OPTS and FEFAQ disagree on the `useManagedFileEvents` default.
