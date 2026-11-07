# Temporal API Acquisition and Databricks Ingest follow-up

This report follows up [`reports/Temporal API Acquisition and Databricks Ingest.md`](Temporal%20API%20Acquisition%20and%20Databricks%20Ingest.md).
That report is unchanged, so the two can be diffed.

- Brief: [`briefs/Temporal API Acquisition and Databricks Ingest follow-up.md`](../briefs/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest%20follow-up.md)
- Notes: [`research_notes/Temporal API Acquisition and Databricks Ingest follow-up/`](../research_notes/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest%20follow-up/)
- Research date: 2026-11-07.

Labels:
- **[D] documented**: first-party sources read in full.
- **[I] inferred**: our reasoning from documented facts.

## Scope

This was a short pass on four open points:

1. How Temporal models the long-running vendor job (A3).
2. How Temporal detects late or missing scheduled runs.
3. How Auto Loader can replay processed files (A8).
4. Three conflicts between Databricks pages (A6).

Sources:
- **Temporal**: the full text of `temporalio/documentation`, the source of docs.temporal.io (commit
  `3fcf3f3`, 2026-11-06), with key sentences checked against the live pages.
- **Databricks**: docs.databricks.com, the Azure mirror, kb.databricks.com, and release notes from
  Jan 2025 to Nov 2026.

## Verdict changes

| # | Assumption | First report | Follow-up | Change |
|---|---|---|---|---|
| A3 | Long-running vendor jobs fit Temporal | Holds (fit inferred; built on async completion) | **Holds, now documented.** The fit is Temporal's *infrequent polling* pattern, with an explicit deadline. | Model the job as a start activity plus a poll activity that retries at a fixed interval of about 60 s. Do not use async completion or a timer loop. |
| A6 | Landing zone plus file-arrival job | Holds if UC volume or external location with file events; limits 50 jobs / 10,000 files without file events | **Holds if, conditions sharpened.** File events are recommended, not required. With file events the limit is 1,000 triggers per workspace. New external locations have file events on by default (since 2026-02-12). On DBR 18.1+, Auto Loader uses file events by default. | Check that the landing location has file events, because older locations may not. Do not set `useIncrementalListing` or `useNotifications`, which turn file events off. |
| A8 | Processed files can be replayed without resetting the checkpoint | Holds only by inference | **Unchanged: holds only by inference.** Neither the KB nor the release notes describe a replay method. The only first-party route is a new checkpoint, optionally bounded by `modifiedAfter`. | Replay stays "re-land under a new path" or "separate stream with its own checkpoint". Settling it needs a test in a workspace. |
| A5 / Q0 | Retries on the Databricks side (Option B) | Default retry count contradicted between pages | **Resolved for scheduled jobs:** classic compute defaults to 0 retries. Serverless retries an undocumented number of times. "Three" applies to continuous jobs. | Set retries explicitly on every task. On serverless, turn off auto-optimization for jobs that are not idempotent. |
| Q0 | Late and missing detection on Temporal | No documented recipe | **Documented recipe exists**, with one limit (a started run that never delivers data is not caught). | See section 2. |

The Q0 verdict stands. The follow-up makes Option A's case for the long-running vendor job stronger:
Temporal documents a pattern for waits of "hours or days", and Databricks still documents none.

---

## 1. The long-running vendor job (A3)

Source: https://docs.temporal.io/design-patterns/polling (repo `docs/design-patterns/polling.mdx`).
Undated; the repo commit is 2026-11-06.

### What Temporal documents

- **[D] The page targets this case:** "a long-running job in a third-party system, a status check
  that has to be repeated until it changes."
- **[D] Three strategies:**
  - Frequent: "Loop inside an Activity with heartbeats".
  - Infrequent: "Use Activity retries with fixed backoff".
  - Periodic sequence: "Child Workflows with Continue-As-New".
- **[D] Infrequent polling for long waits:** it "is a good fit for batch job completion checks,
  long-running external processes, rate-limited APIs, and operations that may take hours or days."
  - Mechanism: "use Activity retries with a backoff coefficient of 1 ... The initial interval of 60
    seconds sets the polling frequency."
  - Effect on history: "Retries do not add events to the Workflow history, keeping it small."
- **[D] Frequent polling for hour-long jobs:** "Using frequent polling for hour-long operations wastes
  resources."
- **[D] Timer loop in the Workflow:** the page says "Avoid this approach" because it "bloats history".
- **[D] Deadline:** "Polling indefinitely without max attempts or a deadline risks runaway
  Workflows." Start-To-Close "has no default value of its own". Schedule-To-Close defaults to ∞
  (https://docs.temporal.io/encyclopedia/detecting-activity-failures).

### How async completion compares

Source: https://docs.temporal.io/activity-execution.

- **[D] Long-timeout risk:** with a one-week Start-To-Close, if the Worker dies during the hand-off,
  "the Activity won't be retried for a week".
- **[D] Signals as an alternative:** when the vendor can call a webhook, a webhook handler that sends
  a Signal is documented. With a one-minute Start-To-Close, "the Activity will be retried in a
  minute".
- **[D] Stale tokens:** "retries can cause a remote service using the Task Token to end up with an
  invalid one".

### Timers and cost

- **[D] Timers:** "Workers consume no additional resources while waiting for a Timer to fire"
  (https://docs.temporal.io/workflow-execution/timers-delays).
- **[D] Billing on Temporal Cloud:** each retry and each timer is a billable Action
  (https://docs.temporal.io/evaluate/cloud/actions).
- **[I] Cost of polling:** about 60 Actions per waited hour at a 60 s interval, plus Active Storage
  while the run is open.

### What this means for A3

**[I]** The documented model is:
- a start activity;
- a poll activity with `backoff_coefficient=1`, a minute-scale `initial_interval`, and an explicit
  Schedule-To-Close or `maximum_attempts` as the overall deadline;
- then a read activity that writes the result bytes (claim check).

The first report based A3 on async completion. Temporal's own guidance prefers polling or Signals
for external systems the team does not control.

**Gap:** the docs give no rule for choosing the overall deadline.

---

## 2. Late or missing runs on the Temporal side

Source: https://docs.temporal.io/troubleshooting/schedule-missed-actions (repo
`docs/troubleshooting/schedule-missed-actions.mdx`).

### Causes [D]

- "A scheduled time does not guarantee that a Workflow Execution starts. An Action can be skipped by
  an Overlap Policy, expire outside the Catchup Window, exceed an internal buffer limit, or fail when
  the Service attempts to start the Workflow Execution."
- Under the default `Skip`, overlapping actions are discarded: "Skipped Actions are not retained for
  later execution."
- `BufferAll` is limited to "approximately 1,000 per Schedule".
- Namespace rate limiting.

### Detection [D]

- **Missed runs:** "Alert on any non-zero value" of the missed-catchup-window counter.
  - Temporal Cloud: `temporal_cloud_v1_schedule_missed_catchup_window_count`.
  - Self-hosted: `schedule_missed_catchup_window`.
- **Scope:** the metric covers a whole Namespace. To find the Schedule, run `DescribeSchedule` and
  check `missedCatchupWindow`, `overlapSkipped`, `bufferDropped` and `recentActions`.
- **More Cloud metrics** (https://docs.temporal.io/cloud/metrics/openmetrics/metrics-reference):
  - `schedule_overlap_skipped_count`;
  - `schedule_action_e2e_delay_p50/p95/p99`, the "total delay from an execution's scheduled time to
    actual start";
  - the missed-window metric "is not emitted for backfills".

### Remedies [D]

- "Widen the Catchup Window ... Revisit the Overlap Policy ... Increase Namespace throughput limits
  ... Backfill the missed interval".

### What this means [I]

- **Late runs:** alert when `schedule_action_e2e_delay` crosses a threshold.
- **Missed runs:** alert on a non-zero missed-catchup count or overlap-skipped count.
- **Limit:** these metrics catch runs that never *started*. A run that started but never delivered
  data, for example a vendor job that never finishes, is caught only by the polling deadline in
  section 1. With `Skip`, a hung run also silently swallows the next scheduled runs. That shows up
  only in `overlap_skipped`.

---

## 3. Replay in Auto Loader (A8)

- **[D, negative] No first-party replay procedure exists.**
  - Searched: about 30 keyword queries against kb.databricks.com, a scan of its 1,110-URL sitemap,
    and platform and DBR release notes from Jan 2025 to Nov 2026.
  - None describes a way to replay files that were already processed, to edit or remove
    checkpoint, RocksDB or `cloud_files_state` entries, or to re-run a date range.
- **[D] The KB recovery route is a new checkpoint:** "start with a new checkpoint and use the
  `modifiedAfter` option to the stream to ingest files that have a modification timestamp after a
  specific timestamp"
  (https://kb.databricks.com/en_US/streaming/auto-loader-failures-with-javaiofilenotfoundexception-for-sst-and-log-files,
  2024-11-04).
- **[D] `cloud_files_state` reads state only:** the KB uses it "to identify any files that have been
  processed more than once"
  (https://kb.databricks.com/en_US/streaming/duplicates-appearing-in-auto-loader-with-file-notification-feature-despite-set-backfill-interval,
  2024-12-12).
- **[D] `cloudFiles.listOnStart` is for error recovery:** it forces a full listing instead of the
  continuation token
  (https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/options,
  2026-11-05).
  - **[I]** Nothing says it re-ingests files already in state.
- **[I] Verdict unchanged.** Copying files to a new path, or a separate stream with its own
  checkpoint, are the workable routes. Only a test in a workspace confirms them.
- **Coverage limit:** the KB was searched by keyword only, and release notes before 2025 were not
  checked.

---

## 4. Databricks page conflicts

### File events: required or recommended?

**Resolved: recommended.** [D + I]

- The file-arrival trigger page (2026-11-06) recommends file events and documents limits for
  locations without them.
- The best-practices page (2026-10-07) says "Requires file events to be enabled".
- No release note makes file events required.
- Release note 2025-06-25: "File arrival triggers with file events allow a higher trigger limit
  (1,000 per workspace) and removes the 10,000 files per trigger limit."
  (https://docs.databricks.com/aws/en/release-notes/product/2025/june)
- Release note 2026-02-12: "File events are now enabled by default when you create new external
  locations." (https://docs.databricks.com/aws/en/release-notes/product/2026/february)

**[I]** The dedicated, newer trigger page is authoritative.

### Default for `useManagedFileEvents`

**Resolved for DBR 18.1+: Auto Loader uses file events by default.** [D + I]

- DBR 18.1 release notes: "Auto Loader uses file events by default when loading from an external
  location with file events enabled ... File events aren't used if your stream code sets
  useIncrementalListing or useNotifications."
  (https://docs.databricks.com/aws/en/release-notes/runtime/18.1, 2026-10-28; release March 2026)
- The file-events FAQ agrees.
- The options table (2026-11-05) still lists `false` and looks stale.

### Default task retries

**Resolved for scheduled jobs.** [D + I]

- "For most configurations, the default setting does not retry any tasks on task failure"
  (https://docs.databricks.com/aws/en/jobs/configure-task, 2026-11-05). The API default for
  `max_retries` is 0.
- Serverless auto-optimization "retries failed tasks" and is on by default, but **no count is
  documented** (https://docs.databricks.com/aws/en/jobs/run-serverless-jobs, 2026-11-06).
- Continuous jobs retry with exponential backoff, up to "three for a single task job"
  (https://docs.databricks.com/aws/en/jobs/continuous, 2026-11-06).

**[I]** The notifications page's "retried three times" matches continuous jobs only. The docs do not
correct it.

---

## Still open

- **Temporal:** no documented rule for choosing the overall deadline of infrequent polling.
- **Auto Loader replay:** settling A8 needs a test in a workspace. So does trigger behaviour on
  `_`-prefixed files and batching, from the first report.
- **Serverless retries:** the retry count for serverless auto-optimization is undocumented.
- **Coverage:** the KB search was by keyword only. Release notes before 2025 were not checked.
