# Temporal API Acquisition and Databricks Ingest alternatives follow-up

This report follows three earlier reports on this branch, which are unchanged: the original report, the
follow-up and the governance follow-up.

- **Brief:** [`briefs/Temporal API Acquisition and Databricks Ingest alternatives follow-up.md`](../briefs/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest%20alternatives%20follow-up.md).
  It includes the Perplexity answer verbatim, as leads only.
- **Notes:** tracks 01–03 in [`research_notes/Temporal API Acquisition and Databricks Ingest alternatives follow-up/`](../research_notes/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest%20alternatives%20follow-up/).
- **Date and method:** research ran on 2026-11-09. Every verdict rests on full first-party texts:
  - Prefect and Dagster: doc sources from repos at their 2026-11-06/07 HEADs.
  - Temporal: docs repo at its 2026-11-06/08 HEADs.
  - Microsoft and Databricks: learn.microsoft.com pages, with dates as shown on each page.
- **Labels:** **[D]** documented, **[R]** reported, **[I]** inferred. "OSS" means the free self-hosted
  product; "paid" means Prefect Cloud or Dagster+.
- **Temporal's side** comes from the earlier reports on this branch and from Temporal's own docs. It was
  not re-checked in track 3.

## Bottom line

1. **No alternative matches Temporal on the two hard source types without hand-built patterns.**
   - Paged pull that cannot be re-queried: Prefect, Dagster, Fabric Data Factory (Fabric DF) and Azure
     Data Factory (ADF) all restart from the beginning of a step or activity. Each needs per-page
     persistence written by the team. [D + I]
   - Multi-hour vendor job:
     - Prefect and Dagster document no durable timer. [D, absence]
     - Fabric caps an activity at 24 h. Its own pages conflict, with one saying 7 days. [D]
     - ADF can wait up to 7 days through Web 202 async or Webhook callbacks, billed per hour. [D]
   - The first report's Q0 verdict stands: Temporal for these two source types.
2. **Some alternatives win elsewhere:**
   - **Operating effort:** a single Prefect server needs "essentially no setup". Temporal itself says
     self-hosting takes "significant engineering and ongoing effort". [D]
   - **SFTP:** ADF's SFTP connector is GA and mature. It has key and MFA auth, binary copy,
     delete-after-copy and per-file resume. Databricks' own SFTP connector is still Public Preview. [D]
   - **SFTP and blob drops:** Dagster's asset model with an SFTP sensor is its own documented example. [D]
3. **The Perplexity claims (H-F) hold in part and fail in two places:**
   - **OneLake fails as the landing zone.** "OneLake paths don't support file event notifications", and
     OneLake external locations are a Public Preview meant for managed storage. [D]
   - **The REST connector does not land raw bytes.** It is JSON-only. Only the HTTP connector in Binary
     mode lands responses byte for byte, and that connector has no OAuth support. [D]
   - **Paged pulls restart from page 1.** "copy activity rerun starts from the beginning". [D]
   - **What holds:** ADF works for SFTP and single-response REST, landing in ADLS Gen2, if the
     FlushWithClose test passes and Team 2 accepts writes that bypass Unity Catalog.
4. **Dagster is today's tool.** Staying on Dagster with no second orchestrator **holds if** the team
   accepts two hand-built patterns. Both are assembled from documented parts, but no doc describes them.
   [I]
   - A cursor written to storage inside each paged asset.
   - A sensor that starts the vendor job, then polls it, then reads the result.

---

## Comparison matrix

Each cell compares the tool with Temporal. Temporal's own column is a summary of the earlier reports.

| Criterion | Temporal (baseline) | Prefect OSS | Dagster OSS | Fabric DF | ADF |
|---|---|---|---|---|---|
| **Plain REST** | Per-activity retry, typed non-retryable errors [D] | **tie**. Task retries with backoff and jitter; non-retry uses a `retry_condition_fn` predicate on tasks only [D] | **tie**. `RetryPolicy` with backoff and jitter; `Failure(allow_retries=False)` [D] | **tie**. Byte-exact only through HTTP Binary, auth Anonymous or Basic [D] | **tie or win**. HTTP Binary with auth headers; file names built from expressions; no OAuth [D] |
| **Paged, cannot be re-queried** | Heartbeat details and Continue-As-New carry the cursor; the activity resumes on another worker [D] | **loses**. Possible with one task per page, persisted results (off by default) and an INPUTS cache or transaction key [D]. A crash leaves the run terminal ("Crashed"). Zombie detection is automatic only on paid Cloud [D]. No auto-resume [I] | **loses narrowly**. The step is the smallest unit that re-executes [D]. Cursor checkpointing is hand-built inside the asset [I] | **loses**. No per-page sink write. A hand-built Until loop runs into the 24 h activity cap [D] | **loses**. "rerun starts from the beginning" [D]. A hand-built Until loop with per-page HTTP Binary copies is possible [I] |
| **Multi-hour vendor job** | Infrequent polling through activity retries; durable timers that use no worker resources [D] | **loses**. `pause_flow_run` blocks a process (default timeout 1 h). `suspend_flow_run` releases it but needs an external resume [D]. No durable timer [I] | **loses**. The documented example sleeps inside the asset. Sensors time out at 60 s, and work over 3 min is "not the correct tool". Resume needs K8s or Docker [D]. No durable timer [I] | **loses**. 24 h activity cap (pages conflict: 24 h vs 7 days); webhook timeout not documented [D] | **tie up to 7 days**. Web 202 async "upto 7 day", Webhook callback, Until up to 90 days (conflicts with the 7-day activity limit); billed per external-activity hour [D] |
| **SFTP / blob drops** | Ordinary polling workflow [I] | **tie** [I]. Webhooks are paid-only [D] | **wins slightly**. External assets and an SFTP sensor are its documented example [D] | **loses or tie**. Basic auth only; no delete-after-copy [D] | **wins**. Key or MFA auth, binary copy, delete-after-copy, last-modified filter, per-file resume (GA) [D] |
| **Operating effort, small team** | Self-hosted: 4 services, fixed shard count, a separate Visibility store, "significant engineering and ongoing effort". Cloud: $50 per million Actions; AWS and GCP only (Azure not checked) [D] | **wins** on a single node: SQLite default, "essentially no setup". HA needs Postgres, Redis and a load balancer [D] | **mixed**. The daemon cannot be replicated (single point of failure). Monitoring and resume need K8s or Docker [D]. The team already runs Dagster [brief] | **wins** on infrastructure, since it is SaaS. Needs F-SKU capacity for trusted workspace access. Managed VNet and private endpoints are "To be determined" [D] | **wins** on infrastructure, since it is PaaS. Managed VNet IR or self-hosted IR [D] |
| **Secrets and egress** | Workers and secrets stay in your environment [D] | Hybrid model with workers in your environment; Secret block encrypted [D] | Runs in your environment; `EnvVar` keeps values out of the UI [D] | Key Vault references; a private vault needs a gateway; the VNet gateway does not refresh OAuth tokens [D] | Key Vault-linked services; managed VNet private endpoints [D] |
| **Late and missing detection** | Schedules with a catch-up window and overlap policy; missed-catch-up metric and alert recipe [D] | **slight loss**. Late state and OSS proactive triggers [D]. Metric triggers, SLAs and zombie detection are paid-only [D]. Catch-up was removed in 3.1 [R] | **loses**. Catch-up only for partitioned schedules (max 5). Freshness policies are a preview. Alerts are paid; OSS has run-status sensors [D] | **loses**. Backfill not supported; interval schedules are a preview; alerts via Activator and the Monitoring hub (preview) [D] | **tie**. Tumbling-window triggers backfill and chain dependencies (GA); Azure Monitor failure metrics [D] |
| **Fit with the landing contract** | Activity code writes through the Files API or ADLS [I]. No lineage [D] | Code writes through the Files API or ADLS. `prefect-azure` blob blocks [D]. Asset lineage is paid-only [D] | Writes raw bytes in the asset with `ADLS2Resource`; skip I/O managers [D]. OSS lineage through external assets [D] | Writes to ADLS as a workspace identity, **bypassing UC** [D]. No volume or Files API connector [D]. FlushWithClose undocumented | Writes to ADLS as a managed identity, **bypassing UC** [D]. No volume connector [D]. FlushWithClose undocumented |

Sources are cited in the notes files 01–03. The most important ones:

- Prefect:
  - https://docs.prefect.io/v3/advanced/detect-zombie-flows
  - https://docs.prefect.io/v3/api-ref/python/prefect-flow_runs
  - https://docs.prefect.io/v3/concepts/server
- Dagster:
  - https://dagster.io/docs/deployment/troubleshooting/sensor-timeouts
  - https://dagster.io/docs/deployment/execution/run-monitoring
  - https://dagster.io/docs/deployment/oss/oss-deployment-architecture
- Azure Data Factory:
  - https://learn.microsoft.com/en-us/azure/data-factory/connector-rest
  - https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview
  - https://learn.microsoft.com/en-us/azure/data-factory/connector-sftp
- Fabric Data Factory:
  - https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-limitations
- Azure Databricks:
  - https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/external-locations-onelake
- Temporal:
  - https://docs.temporal.io/self-hosted-guide/production-checklist

## Hypothesis verdicts

### H2.1: Prefect offers better ergonomics and lower operating effort, with trade-offs on long polling

**Holds if** all three conditions below are met.

- **Lower operating effort:** documented for a single Prefect server.
- **Better ergonomics:** rests only on Prefect's own claims. [I]
- **The polling "trade-off" is understated. It is a confirmed gap** [D + I]:
  - no durable timer;
  - a crashed run is terminal;
  - resuming page by page needs persistence (off by default) plus the right cache policy.
- **"Event-sourced history" is the wrong axis.** Prefect does not replay history. Its real costs are
  how it resumes and how its database grows.

Conditions:
1. Source type 3 is rebuilt as split flows, or as suspend plus an external resume.
2. Source type 2 uses persisted, cached pages plus a self-built zombie automation.
3. The team accepts having no catch-up semantics.

**Fails** for source types 2 and 3 otherwise.

### H2.2, wait-loop half: pure Dagster may struggle with long vendor waits

**Holds, qualified.**

- Dagster has no durable timer. Its documented wait holds a run, and sensors are unsuitable for long
  evaluations. [D]
- The struggle is operating cost and fragility, not impossibility. [I]

### Scope Item 3: pure Dagster without a secondary orchestrator

**Holds if** all three conditions below are met.

1. Paged assets write their cursor to storage.
2. Vendor waits use a split pattern (start job, then a sensor with a cursor and `run_key`, then read the
   result) with the job ID persisted. The alternative is a long-running step on K8s or Docker with
   `dagster/max_runtime` and run monitoring.
3. The team accepts a single daemon with no failover.

**Fails** if native durable timers are required.

### H2.2, lineage half

Answered in the governance follow-up: lineage holds inside Dagster, and fails in UC without a bridge.

### H-F: Fabric DF or ADF can replace extraction and raw landing for SFTP and simple REST

**Holds if, and fails in part.**

**Fails** for two cases:
- the paged source that cannot be re-queried;
- OneLake as the landing zone.

**Holds** for SFTP through ADF, for single-response REST, and for blob drops, on five conditions:
1. The HTTP connector writes Binary into ADLS Gen2. Not the REST connector, and not OneLake.
2. File names are unique.
3. A test confirms that the ADF or Fabric sink emits FlushWithClose. This is undocumented.
4. Team 2 accepts that a non-Databricks identity writes directly, bypassing UC.
5. On Fabric: an F SKU, and acceptance that managed VNet and private endpoints are still "To be
   determined".

Within this pair, **ADF is the stronger choice today**. Fabric trails it on all four of these
(documented):
- SFTP auth and delete-after-copy;
- timeouts (24 h cap);
- tumbling-window backfill;
- private networking.

Perplexity's line that "Temporal remains stronger" for stateful extraction matches the evidence. [I]

### Logic Apps (side note)

- **Documented strengths:** 90-day stateful runs, async polling and Until loops. That makes it a credible
  option for the long vendor job.
- **Pagination:** HTTP pagination follows nextLink only and returns a single message.
- **ADLS writes:** it reaches ADLS Gen2 only through the Blob connector (≤ 50 MB per write), so
  FlushWithClose is doubtful. [I]
- **Not assessed in depth:** the SFTP connector was not analysed.

## What this changes

- **Q0 verdict (first report): unchanged.** Temporal stays the choice for the paged source and the
  long-running vendor job. None of the alternatives covers them without hand-built patterns. [D + I]
- **SFTP drops:** ADF is the strongest documented option among those checked. That fills the gap where
  the first report said "neither option applies". The cost is direct ADLS writes outside UC, which the
  governance report flagged as route c.
- **Plain REST pulls stay a near tie.** With a small team the deciding factor is operating effort, not
  features. A team already running Dagster, or a single Prefect server, avoids running a Temporal
  cluster for these. That is inference. Nothing compares the tools independently.
- **Landing zone:** ADLS Gen2 as a UC external location, confirmed. OneLake is ruled out for this
  design. [D]
- **The real decision is "one tool or two".** [I]
  - **One tool:** Temporal for all API sources, accepting its operating cost, or Temporal Cloud if an
    Azure region is acceptable (not checked).
  - **Two tools:** keep Dagster (the incumbent) or ADF for simple pulls and SFTP, plus Temporal for the
    two hard source types.
  - **Dagster only:** accept the hand-built cursor and sensor patterns.

  The evidence does not choose between these. It depends on how much operating effort the team can
  carry and how often the hard source types fail in practice.

## Gaps

- **No independent evidence:** nothing compares ergonomics or operating effort across these tools. Every
  such claim comes from the vendors.
- **Needs a workspace test:**
  - whether ADF or Fabric sink writes emit FlushWithClose, and whether they overwrite an existing file
    or fail;
  - whether the REST "as-is" output is byte-identical.
- **Unresolved doc conflicts:**
  - Fabric activity timeout: 24 h vs 7 days.
  - ADF: Until's 90 days vs the 7-day activity limit.
  - Fabric SFTP authentication.
- **Inferred only:** the Prefect and Dagster split patterns for vendor waits, and Prefect resuming by
  skipping cached pages.
- **Not checked:**
  - Temporal Cloud on Azure;
  - Prefect Cloud and Dagster+ pricing;
  - the Logic Apps SFTP connector;
  - the GA date of Databricks' SFTP connector.
- **Still open from earlier reports:** the trigger and lineage workspace tests.
