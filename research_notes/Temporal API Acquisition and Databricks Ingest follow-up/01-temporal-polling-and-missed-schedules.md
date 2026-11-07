# Follow-up track 1: Temporal polling for long-running jobs, and missed Schedule actions

Method:
- Quotes come from the full text of `temporalio/documentation`, the source of docs.temporal.io. Clone
  at commit `3fcf3f3`, dated 2026-11-06. All quoted files carry that last-commit date.
- Every live URL cited returned HTTP 200 on 2026-11-07. Three key sentences were checked against the
  live HTML and found there.
- The pages are undated, so all are cited "undated, accessed 2026-11-07".
- URLs are relative to https://docs.temporal.io.
- Labels: **documented** / **inferred**.

## Q1. Modelling the long-running vendor job (assumption A3)

### Polling patterns: /design-patterns/polling (repo `docs/design-patterns/polling.mdx`)

- **documented**: The page targets this case: "a long-running job in a third-party system, a status
  check that has to be repeated until it changes."
- **documented**: Three strategies:
  - "Frequent Polling (1 second or faster): Loop inside an Activity with heartbeats."
  - "Infrequent Polling (1 minute or slower): Use Activity retries with fixed backoff."
  - "Periodic Sequence: Use Child Workflows for complex polling sequences."
- **documented**: Infrequent polling "is a good fit for batch job completion checks, long-running
  external processes, rate-limited APIs, and operations that may take hours or days."
- **documented**: Frequent polling "is not a good fit for long-running operations (hours or days)".
  The page also warns: "Using frequent polling for hour-long operations wastes resources."
- **documented**: Mechanics of infrequent polling:
  - "use Activity retries with a backoff coefficient of 1. The Activity throws an exception when the
    external service is not ready, and Temporal retries after the configured interval".
  - "The initial interval of 60 seconds sets the polling frequency."
  - The Python sample uses `start_to_close_timeout=2s`, `backoff_coefficient=1` and
    `initial_interval=60s`.
- **documented**: "Retries do not add events to the Workflow history, keeping it small." The page
  rates its history impact as "Minimal". /evaluate/cloud/actions agrees: "Intermediate retry attempts
  do not produce separate history events."
- **documented**: The page says to avoid a timer loop in the Workflow:
  - Its comparison table lists "Workflow Timer Loop | Any | High | Medium | Avoid this approach".
  - "Workflow timers instead of proper polling patterns bloats history."
- **documented**: Bound the polling: "Polling indefinitely without max attempts or a deadline risks
  runaway Workflows." Two related best practices:
  - "Use backoff for error cases (not normal polling)".
  - "If the external service supports callbacks, use async completion instead."
- **documented**: The periodic-sequence variant uses "Child Workflows with Continue-As-New" for
  "very long-running polls requiring Continue-As-New".

### Async completion compared with Signals and polling: /activity-execution (repo `docs/encyclopedia/activities/activity-execution.mdx`)

- **documented**: If you cannot change the external system, "you can poll (#3), or if the external
  system can reliably call a webhook ... you can write a webhook handler that sends a Signal to the
  Workflow (#2)."
- **documented**: Risk of Async Completion with a long Start-To-Close timeout: if the Worker dies
  during hand-off, "the Activity won't be retried for a week". With Signals and a one-minute
  Start-To-Close, "the Activity will be retried in a minute."
- **documented**: "retries can cause a remote service using the Task Token to end up with an invalid
  one". The page's remedy is to pass the Activity ID and Workflow ID instead.

### Durable timers and resources: /workflow-execution/timers-delays and /develop/python/workflows/timers

- **documented**: "Timers in Temporal are persisted, meaning that even if your Worker or Temporal
  Service is down when the time period completes ... the call that is awaiting the Timer ... will
  resolve".
- **documented**: "Workers consume no additional resources while waiting for a Timer to fire, so a
  single Worker can await millions of Timers concurrently."
- **documented**: A timer can be "as short as one second or as long as several years". Treat the
  duration "as a minimum time".
- **documented** (Python page): "it does not tie up the process"; "A Workflow can sleep for months."
- **inferred**: The docs do not say whether a Worker must stay up during a timer. They say only "no
  additional resources" and that the timer resolves once a Worker is back.

### Cost while waiting on Temporal Cloud: /evaluate/cloud/actions and /cloud/pricing

- **documented**: Billed Actions:
  - "Timer started" (including implicit timers for timeouts).
  - "Activity started or retried".
  - A heartbeat, but only when it reaches the server ("default throttle is 80% of the Heartbeat
    Timeout").
- **documented**: An open execution is in Active Storage; a closed one is in Retained Storage.
- **inferred**: Infrequent polling at 60 s costs about 60 Actions per waited hour, plus Active Storage
  for as long as the Workflow is open.

### Limits relevant to waiting

- **documented** (/workflow-execution/limits): History is limited to 51,200 events or 50 MB. Pending
  operations are limited to 2,000 each of Activities, Child Workflows, Signals and Cancellation
  requests. Timers are not in that list.
- **documented** (/encyclopedia/detecting-activity-failures):
  - "The Start-To-Close Timeout has no default value of its own."
  - Set it "longer than the maximum possible time"; for long activities, also use heartbeats.
  - Schedule-To-Close defaults to ∞.
  - The Heartbeat Timeout is capped at Start-To-Close.
  - Default heartbeat throttle is 30 s; maximum is 60 s.
- **documented** (/design-patterns/long-running-activity): Set the Heartbeat Timeout to "2-3x the
  expected heartbeat interval". Cancellation propagates only at heartbeat cadence.
- **inferred**: For a vendor job that runs for hours, the documented fit is:
  - one start Activity;
  - one poll Activity that retries with backoff coefficient 1 at minute-scale intervals and has an
    explicit Schedule-To-Close or maximum-attempts deadline.

  If the vendor can call a webhook, a Signal is the documented alternative. Async completion carries
  the long-timeout risk described above.

## Q2. Missed Schedule actions: /troubleshooting/schedule-missed-actions (repo `docs/troubleshooting/schedule-missed-actions.mdx`)

### Causes

- **documented**: "A scheduled time does not guarantee that a Workflow Execution starts. An Action can
  be skipped by an Overlap Policy, expire outside the Catchup Window, exceed an internal buffer limit,
  or fail when the Service attempts to start the Workflow Execution."
- **documented**: The default `Skip` policy discards overlaps: "Skipped Actions are not retained for
  later execution."
- **documented**: Other causes:
  - The `BufferAll` buffer is limited to "approximately 1,000 per Schedule"; it is not "an unlimited
    durable queue".
  - `CancelOther` can push a replacement run past the Catchup Window.
  - `AllowAll` keeps adding concurrency.
  - Outages longer than the Catchup Window.
  - Namespace rate limiting.

### Detection

- **documented**: "The Temporal Service emits a counter each time it skips a scheduled Action because
  it could not run it within the configured Catchup Window. Alert on any non-zero value."
  - Cloud: `temporal_cloud_v1_schedule_missed_catchup_window_count`.
  - Self-hosted: `schedule_missed_catchup_window`.
- **documented**: The metric is scoped to the Namespace, not to a Schedule. To find the Schedule,
  run `DescribeSchedule` and look at `info.missedCatchupWindow`, `overlapSkipped`, `bufferDropped`,
  `recentActions` and `runningWorkflows`.
- **documented** (/cloud/metrics/openmetrics/metrics-reference):
  - `schedule_overlap_skipped_count`, labelled with the policy.
  - `schedule_action_e2e_delay_p50/p95/p99`: "total delay from an execution's scheduled time to actual
    start".
  - The missed-window metric "is not emitted for backfills".
  - `schedule_rate_limited_count` is deprecated.
- **documented** (/references/service-metrics): Self-hosted also emits `schedule_rate_limited`,
  `schedule_buffer_overruns` and `schedule_action_success`.

### Remedies

- **documented**: "Widen the Catchup Window ... Revisit the Overlap Policy ... Increase Namespace
  throughput limits ... Backfill the missed interval". Backfills are not limited by the Catchup
  Window (/schedule).
- **inferred**: To catch late runs on Cloud, alert on `schedule_action_e2e_delay` above a threshold.
  To catch missing runs, alert on a non-zero missed-catchup or overlap-skipped count. The docs
  recommend only the missed-catchup alert.
- **inferred**: These metrics catch runs that never started. A run that starts but delivers no data
  (for example, a vendor job that never finishes) still needs the deadline and timeouts above.

## Gaps

- The docs say nothing specific about vendor jobs that run for hours. The fit comes from the
  polling page's "hours or days".
- No guidance on choosing the overall deadline for infrequent polling.
- No documented maximum timer duration, and no limit on pending timers.
- The docs do not say whether a Worker must be running while a timer is pending.
- Not read: SDK metrics, per-SDK async-completion pages, Cloud limits page.
