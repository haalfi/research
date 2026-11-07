# Track 1: Temporal for bulk acquisition (Q1)

Source: deep-research workflow run `wf_d4ed6c0d-99f`, 2026-11-07. 23 sources fetched, 112 claims extracted, top 25 verified 3-vote (25 confirmed, 0 refuted). All surviving claims are Temporal-side.

Labels: **documented** = stated in first-party docs; **reported** = practitioner write-up; **inferred** = our reasoning.

## F1 (high, vote 3-0 (merged claims 1, 3, 6, 12, part of 9))

Documented: Temporal limits each payload, meaning each Workflow or Activity argument and return value. It warns at 512 KB and fails the operation at 2 MB. The limit is fixed at 2 MB on Temporal Cloud and is a configurable default of 2 MB on self-hosted. The AI Cookbook table gives the warning level as 256 KB, not 512 KB. Inferred: raw API response bytes above about 2 MB cannot pass through workflow or activity inputs and outputs, which supports the assumption that response bytes stay outside Temporal.

Evidence: Several first-party pages agree, and every vote was 3-0. One says: 'The default and recommended limit is 2 MB ... fixed at 2 MB on Temporal Cloud ... Payloads that exceed this limit fail the operation.' The self-hosted defaults page gives a warning at 512 KB and ErrBlobSizeExceedsLimit at 2 MB. The pages differ only on the warning level: 512 KB on the limits sheet, 256 KB in the cookbook. All checked 2026-11-07.

- https://docs.temporal.io/external-storage
- https://docs.temporal.io/self-hosted-guide/defaults
- https://docs.temporal.io/troubleshooting/blob-size-limit-error
- https://docs.temporal.io/kb/temporal-platform-limits-sheet
- https://docs.temporal.io/cloud/limits
- https://docs.temporal.io/ai-cookbook/claim-check-pattern-python

## F2 (high, vote 3-0 (claim 7, part of 9))

Documented: gRPC limits each request to 4 MB. The limit covers all payload data and command metadata in that request, and 4 MB is also the limit per Event History transaction. A workflow task that schedules many activities in one request can exceed it even when every payload is under 2 MB. The SDK then reports GRPC_MESSAGE_TOO_LARGE and the execution is terminated.

Evidence: The troubleshooting page says: 'enforces a 4 MB limit on each request. This limit applies to the full request, including all payload data and command metadata.' Checked 2026-11-07.

- https://docs.temporal.io/troubleshooting/blob-size-limit-error
- https://docs.temporal.io/cloud/limits
- https://docs.temporal.io/self-hosted-guide/defaults

## F3 (high, vote 3-0 (merged claims 4, 5, 9, 13, 14, 15, 20))

Documented: Event History is capped at 50 MB or 51,200 events, whichever comes first. It warns at 10 MB or 10,240 events. Passing either cap terminates the Workflow Execution. On Cloud the caps cannot be changed. On self-hosted they are defaults (HistorySizeLimitError/Warn and HistoryCountLimitError/Warn). Temporal also limits a run to 2,000 incomplete Activities by default and recommends keeping history to about 2,000 events. Inferred: a run that schedules one activity per page reaches the cap after a few thousand to about ten thousand pages, so paged pulls need Continue-As-New or batching.

Evidence: Batch Iterator page: 'A single Workflow run is limited to 51,200 history events (aim for 2,000) and 2,000 in-flight Activities.' Limits sheet: 'Warns at 10 MB and errors at 50 MB, which terminates the Workflow Execution.'

- https://docs.temporal.io/self-hosted-guide/defaults
- https://docs.temporal.io/kb/temporal-platform-limits-sheet
- https://docs.temporal.io/cloud/limits
- https://docs.temporal.io/design-patterns/batch-iterator
- https://docs.temporal.io/workflow-execution/limits
- https://docs.temporal.io/design-patterns/continue-as-new

## F4 (high, vote 3-0 (merged claims 0, 8, 10))

Documented: Temporal names the claim check as a pattern. Large data goes to an object store such as S3, and only a reference passes through the Workflow. Temporal calls it 'the most reliable way to avoid hitting payload size limits'. There are two ways to implement it. One is the built-in External Storage feature, which offloads payloads that reach a threshold, by default 256 KiB, through S3 or GCS drivers. The other is a custom PayloadCodec; the cookbook sample keys payloads by UUID and keeps payloads under 20 KB inline. Inferred: this is a claim check at the SDK level. The proposal is a claim check at the application level, where an activity writes the bytes and a manifest into the landing zone. Temporal's docs support the principle behind the proposal but do not describe that application-level form.

Evidence: External Storage page: 'offloads payloads to an external store (such as Amazon S3) and passes a small reference token through the Event History instead. ... This is called the claim check pattern.' The cookbook page was last updated 21 Oct 2026.

- https://docs.temporal.io/external-storage
- https://docs.temporal.io/troubleshooting/blob-size-limit-error
- https://docs.temporal.io/ai-cookbook/claim-check-pattern-python
- https://docs.temporal.io/develop/python/data-handling/external-storage.md

## F5 (high, vote 3-0 (merged claims 2, 11))

Documented: External Storage, the built-in claim check, is in Public Preview and not GA. Its APIs and configuration may change. In Python it arrived in SDK 1.25, and the S3 driver is marked experimental. Inferred: if the proposal used External Storage, it would depend on a preview feature. An application-level claim check written in an activity does not have that dependency.

Evidence: Page banner: 'Currently in: Public Preview. APIs and configuration may change before General Availability.' No source found shows it as GA on 2026-11-07.

- https://docs.temporal.io/external-storage
- https://docs.temporal.io/ai-cookbook/claim-check-pattern-python
- https://temporal.io/changelog/external-storage-public-preview

## F6 (high, vote 3-0 (merged claims 16, 21))

Documented: For paged pulls with an unknown page count, Temporal documents the Batch Iterator / Continue-As-New pattern. Each run fetches one page or batch through an Activity, updates an offset or cursor, and continues as new with that cursor as state. The workflow stops when a page comes back shorter than the page size. There is no total-count mechanism. Inferred: the documented examples pass records through history as Activity results, so for raw bytes this pattern has to be combined with a claim check. The docs do not cover a source that cannot answer for a past date. Resuming from a cursor assumes the source will return the same page later, which that source type does not guarantee.

Evidence: 'Check whether the returned page is shorter than `pageSize` before continuing.' 'The Workflow fetches a batch of records, processes each one, and updates the cursor.' The sample code continues only while the page is full.

- https://docs.temporal.io/design-patterns/batch-iterator
- https://docs.temporal.io/design-patterns/continue-as-new
- https://docs.temporal.io/design-patterns/batch-processing-patterns

## F7 (medium, vote 2-1 (claim 19))

Documented: Asynchronous Activity Completion lets an Activity function return without completing the Activity. A Temporal Client can later heartbeat it and complete it from anywhere. Inferred: this fits the source type 'start the vendor job, wait hours, read the result'. Start-to-Close, Schedule-to-Close and Heartbeat timeouts must be sized for hours, and whatever completes the Activity needs the task token or the Activity ID. Polling with retries or timers is another option; the verifiers noted it, but no source in this run confirms it.

Evidence: 'Asynchronous Activity Completion is a feature that enables an Activity Function to return without causing the Activity Execution to complete. ... The Temporal Client can then be used from anywhere to both Heartbeat ... and eventually complete the Activity Execution.' The vote was split because the page does not name vendor jobs, so the fit is inferred.

- https://docs.temporal.io/activity-execution

## F8 (high, vote 3-0 (merged claims 17, 18, 23, 24))

Documented: Temporal gives two ways to mark an error as non-retryable. (1) At the throw site, set the non-retryable flag on the application error: Python ApplicationError(non_retryable=True), Go NewNonRetryableApplicationError, Java ApplicationFailure.newNonRetryableFailure, TypeScript ApplicationFailure.nonRetryable. Such an error is never retried, whatever the policy says. (2) At the call site, list error type names in the RetryPolicy: non_retryable_error_types, NonRetryableErrorTypes, setDoNotRetry, nonRetryableErrorTypes. This list matches the Application Failure's type field, not the message, and is empty by default. Temporal recommends using both. Inferred: this covers the per-feed retry policies and cheap pre-checks used today, for example raising a non-retryable error when a pre-check fails.

Evidence: 'Use the SDK's `ApplicationError` (or equivalent) with the non-retryable flag.' 'Combine both mechanisms for defence in depth.' 'Non-Retryable Errors specify errors that shouldn't be retried. By default, none are specified.'

- https://docs.temporal.io/design-patterns/non-retryable-errors
- https://docs.temporal.io/encyclopedia/retry-policies

## F9 (high, vote 3-0 (claim 22))

Documented: Activities have a Retry Policy by default: 1 s initial interval, backoff 2.0, 100 s maximum interval, unlimited attempts. Workflow Executions are not retried by default, and Temporal calls giving them a retry policy uncommon. Inferred: a feed's retry policy belongs on its fetch activities, and every feed needs an explicit cap, because the default retries without limit.

Evidence: 'Activities in Temporal are associated with a Retry Policy by default, while Workflows are not.' The defaults table lists maximum attempts 0, meaning unlimited.

- https://docs.temporal.io/encyclopedia/retry-policies

## F10 (high, vote n/a)

Gap, no surviving first-hand evidence: Q0 (Temporal against a Databricks job for API pulls, per source type), Q2 (what file-arrival triggers require of the storage, how to replay files without resetting the Auto Loader checkpoint, whether a manifest written last fits), Q3 (Databricks guidance on landing files first or writing straight to bronze), Q4 (handoff patterns from Temporal to Databricks and from Temporal to Dagster), and published evidence of Temporal used for data ingestion. A Q0 verdict and verdicts on the Databricks-side assumptions cannot be given from this evidence set.

Evidence: No claim among the 25 surviving claims cites Databricks or Dagster documentation, or a published case of Temporal used for ingestion.


## Caveats

Evidence covers only Q1, the Temporal side, and comes entirely from Temporal's first-party documentation. Every check ran on 2026-11-07, and most pages carry no date. External Storage is in Public Preview, so its thresholds, drivers and APIs may change. The payload warning level differs between pages: 512 KB on the limits sheet and the self-hosted defaults, 256 KB in the AI Cookbook. On self-hosted, the limits are configurable defaults. On Cloud they are fixed. The claim-check sample is an AI Cookbook recipe written for LLM chat history, not an ingestion guide, and its 20 KB inline threshold is a sample default. The fit of Asynchronous Activity Completion to long-running vendor jobs is inference, and its vote was split 2-1. The links from history caps to page limits and from the cursor pattern to raw bytes are inference too. No Databricks, Dagster or ingestion-case-study sources survived verification. Q0, Q2, Q3 and Q4 are therefore unanswered and must not be filled from memory. The brief's Q0 verdict and its table of assumption verdicts can only be partly filled from this set.

## Open questions handed to later tracks

- What do Databricks file-arrival triggers require of the storage, for example Unity Catalog external locations or volumes and file-count limits? Can Auto Loader replay already processed files without resetting the checkpoint, and does a trigger on a manifest written last fit?
- What does Databricks currently recommend for API sources: land raw files in a volume first, or write parsed payloads straight to bronze? How do the two options compare per source type on retries, secrets and egress, and late or missing detection?
- Is there a documented or reported handoff from Temporal to Databricks (Jobs run-now from an activity, or a file-arrival trigger), and from Temporal to Dagster (sensors on the manifest or ledger, or the Dagster API) for the interim period?
- Is there published first-hand evidence of Temporal used for bulk data ingestion? How should a paged source that cannot answer for a past date be made safe to resume when Continue-As-New depends on re-reading pages?

## Sources fetched (all accessed 2026-11-07)

- https://docs.temporal.io/external-storage (primary; Temporal limits and claim check (Q1))
- https://docs.temporal.io/self-hosted-guide/defaults (primary; Temporal limits and claim check (Q1))
- https://docs.temporal.io/troubleshooting/blob-size-limit-error (primary; Temporal limits and claim check (Q1))
- https://docs.temporal.io/ai-cookbook/claim-check-pattern-python (primary; Temporal limits and claim check (Q1))
- https://temporal.io/kb/temporal-platform-limits-sheet (primary; Temporal limits and claim check (Q1))
- https://community.temporal.io/t/history-size-exceeds-warn-limit-scheduled-workflow/10651 (forum; Temporal limits and claim check (Q1))
- https://docs.temporal.io/design-patterns/batch-iterator (primary; Temporal long-running jobs, pagination, non-retryable errors (Q1))
- https://docs.temporal.io/design-patterns/non-retryable-errors (primary; Temporal long-running jobs, pagination, non-retryable errors (Q1))
- https://docs.temporal.io/activity-execution (primary; Temporal long-running jobs, pagination, non-retryable errors (Q1))
- https://docs.temporal.io/design-patterns/continue-as-new (primary; Temporal long-running jobs, pagination, non-retryable errors (Q1))
- https://docs.temporal.io/encyclopedia/retry-policies (primary; Temporal long-running jobs, pagination, non-retryable errors (Q1))
- https://temporal.io/blog/very-long-running-workflows (blog; Temporal long-running jobs, pagination, non-retryable errors (Q1))
- https://docs.databricks.com/aws/en/jobs/file-arrival-triggers (primary; Databricks file arrival triggers and Auto Loader replay (Q2))
- https://learn.microsoft.com/en-in/azure/Databricks/jobs/file-arrival-triggers (primary; Databricks file arrival triggers and Auto Loader replay (Q2))
- https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/options.html (primary; Databricks file arrival triggers and Auto Loader replay (Q2))
- https://docs.databricks.com/aws/en/lakehouse-architecture/deployment-guide/delta-lake (primary; Databricks API ingestion recommendation (Q3/Q0 Option B))
- https://docs.databricks.com/aws/en/lakehouse/medallion.html (primary; Databricks API ingestion recommendation (Q3/Q0 Option B))
- https://docs.databricks.com/aws/pyspark/datasources (primary; Databricks API ingestion recommendation (Q3/Q0 Option B))
- https://docs.databricks.com/aws/en/ingestion/custom-connectors (primary; Databricks API ingestion recommendation (Q3/Q0 Option B))
- https://loop.com/engineering-blog/temporal-at-loop---evolution-and-scaling (blog; Practitioner evidence and handoffs (Q1/Q4))
- https://temporal.io/resources/case-studies/messari (secondary; Practitioner evidence and handoffs (Q1/Q4))
- https://docs.databricks.com/gcp/en/jobs/run-now (primary; Practitioner evidence and handoffs (Q1/Q4))
- https://docs.dagster.io/api/dagster/external-assets-instance-api (primary; Practitioner evidence and handoffs (Q1/Q4))
