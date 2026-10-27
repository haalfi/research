# Follow-up: two targeted tracks

Same context, terms and delivery rules as the original brief: options with mechanism, preconditions,
trade-offs, failure modes and exit cost; every claim graded first-hand, documented (with version and
date) or inferred; no overall recommendation or ranking. Run Track A first.

## Track A: Orchestrator-held state, and running two orchestrators at once

Today the pipelines keep part of their own operational state inside the orchestrator's event log and
run records, and pipeline decisions read it back. The kinds of state involved:

1. **Gate verdicts carried across re-executions.** A blocking check's failure must still block a
   re-execution of the downstream step, which is found by walking the run's parent lineage.
2. **"Has this delivery landed?"** Read from the orchestrator's materialisation records and their
   metadata.
3. **Deadline and arrival decisions.** "Is this expected delivery late or missing?", derived from
   materialisation history.
4. **Operator acknowledgements.** A human marks a known failure as accepted, stored as a manual check
   result in the orchestrator.
5. **Discovery cursors.** Which partitions or files have already been picked up: sensor cursors plus
   the materialised-partition set.
6. **Concurrency limits.** Pool limits held as orchestrator runtime state, which a pipeline step reads
   back and refuses on.
7. **Schedules and their on/off state, and backfill progress.**

Questions:

- **A1.** For each kind of state above, what are the options for where it lives: in the orchestrator,
  in a platform-owned ledger (for example delivery, verdict or acknowledgement tables in the
  warehouse), or derived from the data itself? What does each option cost? Name the patterns
  practitioners use, such as a delivery or arrival ledger, an audit table of check results, or
  watermark tables.
- **A2.** Which of these kinds of state can be exported from the orchestrator or rebuilt elsewhere,
  and which are lost when it is replaced? Dagster OSS is the current orchestrator: say what its
  instance storage and APIs allow, with version.
- **A3.** Two orchestrators running feed by feed against one shared storage platform. Give real
  reports where possible, and cover:
  - how each feed's ownership is switched over
  - how the double run of a feed is prevented
  - how cross-feed dependencies are handled when the upstream and downstream feeds sit on different
    orchestrators
  - how consumers stay unaware of the move
- **A4.** If operational state moves out of the orchestrator, what does the orchestrator still need to
  know, and what does that cost in features lost (for example its native lineage, check UI or
  freshness views)?

## Track B: Keeping pipeline definitions orchestrator-neutral

- **B1.** Where should a pipeline's logic live so that it runs and is tested without any orchestrator?
  Cover plain-library logic called by thin orchestrator wrappers, and declarative pipeline
  definitions (configuration or code) that an adapter compiles into orchestrator objects. Name the
  connector or extract-load contracts that separate the source side from the run side (for example
  dlt, Singer/Meltano, Airbyte-style protocols), and say what each puts on which side of the line.
- **B2.** In-house abstraction layers over an orchestrator: give practitioner reports with outcomes.
  Did the layer survive an orchestrator change? Did it become a maintained inner framework? What was
  the warning sign? Reports of abandoned layers count as much as successful ones.
- **B3.** Which orchestrator features are usually worth binding to directly, because a neutral
  re-implementation would cost more than a later migration? Which are usually not?
- **B4.** A concept mapping, to test whether a "neutral" pipeline model is really just the current
  orchestrator's model. For each concept below, give the equivalent in **Dagster OSS** and in
  **Databricks** (Lakeflow Jobs, Lakeflow Declarative Pipelines, Unity Catalog, Asset Bundles), with
  product version and GA status. Mark each concept where one side has no equivalent, or where the
  equivalent has different semantics.

  | concept the pipelines use today |
  |---|
  | a data asset as the unit of definition, with dependencies between assets |
  | one step producing several assets |
  | an observed external source that the platform does not produce (a drop zone, a vendor's job state) |
  | data-quality checks attached to an asset, including blocking checks that stop downstream work |
  | a manual check result recorded by a human |
  | partitions: daily, time-window, static, two-dimensional, and a mapping between them |
  | backfills: one run per partition, or one run for a range |
  | cron schedules over partitions |
  | event-driven triggers (polling sensors with a cursor) |
  | declarative "run when upstream changes or a cron tick passes" conditions |
  | freshness expectations, and alerting on a breach |
  | named concurrency pools and per-group run limits |
  | per-run isolation in its own container, with per-vendor secrets injected per step |
  | retries with policy, per step |
  | code versions or data versions that decide whether an asset is stale |
  | lineage from source to SQL transformations (dbt) as one graph |
  | run metadata on each materialisation (row counts, schema), read back later |
  | one alerting stream for failed runs, failed checks, freshness breaches and failing triggers |
  | step logs uploaded to object storage |

- **B5.** Lakeflow Declarative Pipelines defines pipelines, expectations and lineage itself. If a
  platform's pipelines must stay neutral, what is the cost of running them on Databricks without
  Declarative Pipelines, for example plain jobs calling library code? And what is the cost of
  adopting Declarative Pipelines and treating the pipeline definition as Databricks-specific?
