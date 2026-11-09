# Follow-up brief: Alternatives for API acquisition (Track 2, extended)

## Source of this brief

This run carries out the Track 2 work that the governance follow-up brief deferred. That brief is
`briefs/Temporal API Acquisition and Databricks Ingest governance follow-up.md`, Track 2 and Scope
Items 2–3.

Extensions decided on 2026-11-09:

- **Fabric and Azure Data Factory:** the user shared an answer from Perplexity that proposes Fabric
  Data Factory or Azure Data Factory for extraction and raw landing. It is reproduced verbatim below
  as **leads only**.
- **The assistant's view** of that answer is recorded in the session. In short:
  - Treat Fabric and Azure Data Factory as another external writer under the landing contract.
  - Verify these points before relying on them: OneLake as a Unity Catalog external location;
    byte-exact landing; failure behaviour during pagination; long waits; how they write to ADLS;
    GA status; SFTP compared with Databricks' own SFTP ingestion.
- **User decisions:**
  - Q1, run Fabric/ADF together with Track 2 or separately: "same run".
  - Q2, Fabric Data Factory only or Azure Data Factory as well: "both".

## Candidates

- Temporal (the proposal under test, as the baseline)
- Prefect OSS
- Dagster OSS ("pure Dagster" asset model)
- Fabric Data Factory and Azure Data Factory
- Azure Logic Apps (short side note only)

## Comparison grid

The same grid as the first report's Q0, plus fit with the landing contract.

- **Source types:**
  - plain REST pull;
  - paged REST pull that cannot answer for a past date;
  - long-running vendor job (start, wait hours, read the result);
  - SFTP and blob drops.
- **Criteria:**
  - retries;
  - secrets and egress;
  - operating effort for a small team;
  - detecting late and missing data;
  - fit with the landing contract:
    - raw bytes preserved;
    - immutable new file names, no overwrites;
    - ADLS writes complete with FlushWithClose;
    - a manifest written last;
    - the write route (Files API, credential vending, or direct ADLS).

## Hypotheses to test

These come from the governance brief.

- **H2.1:** Prefect gives Team 1 better Python-native ergonomics with less operating overhead than
  Temporal. It may trade away multi-day stateful polling and event-sourced history.
- **H2.2:** Pure Dagster software-defined assets can replace the hybrid model. It gives end-to-end
  lineage but may struggle with long, non-deterministic vendor waits. The lineage half was answered
  in the governance follow-up.
- **H-F:** Fabric Data Factory or Azure Data Factory can replace extraction and raw landing for SFTP
  and simple REST pulls. Temporal stays for stateful extraction. This hypothesis comes from the
  Perplexity answer.

## Constraints

These carry over from earlier briefs:
- Azure ADLS Gen2 with HNS preferred, while keeping the cloud open.
- Team 2 runs Auto Loader and the file-arrival job.
- Team 2 enforces strict egress and secrets rules inside the workspace.
- Prefer open-source tools and documented API contracts.
- Labels: [D] documented / [R] reported / [I] inferred.
- Out of scope: compliance retention.

---

## Lead material: Perplexity answer as shared by the user on 2026-11-09 (verbatim)

Yes—**Microsoft Fabric can replace the “ingest directly into Databricks raw tier” pattern** for API and SFTP sources. The cleanest native-Azure design is: **Fabric Data Factory lands immutable raw files/JSON in OneLake (or ADLS Gen2), then Databricks consumes it via Auto Loader / streaming tables into Unity Catalog bronze**. This keeps Unity Catalog as the governed analytical layer while removing Databricks as the extraction engine. [learn.microsoft](http://www.learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/azure-databricks-modern-analytics-architecture)

## Recommended architecture

```text
APIs / SFTP
    │
    ├─ Fabric Data Factory (Copy job / pipeline / Dataflow Gen2)
    │        └─ land raw payload + metadata in OneLake or ADLS
    │
    ├─ Databricks Auto Loader / Lakeflow pipeline
    │        └─ bronze Unity Catalog tables (raw, append-only)
    │
    └─ Databricks silver/gold transformations
             └─ Unity Catalog governed tables
```

Use **Fabric as the ingestion/landing layer**, not as a replacement for Unity Catalog governance. Fabric’s Data Factory supports both **REST** and **SFTP** connectors, and its pipelines/copy jobs can land data into Fabric lakehouses or storage; Databricks can then incrementally ingest those files. [learn.microsoft](http://www.learn.microsoft.com/en-ie/fabric/data-factory/connector-overview)

## Why this is a good fit

| Concern | Fabric-native approach | Databricks-only approach |
|---|---|---|
| API extraction | Fabric Data Factory REST connector or Logic Apps HTTP action; land JSON/NDJSON raw | Databricks notebooks/jobs call APIs directly |
| SFTP batch | Fabric SFTP connector, ADF SFTP connector, or Logic Apps SFTP connector | Databricks job uses SSH/SFTP libraries |
| Raw-tier ownership | OneLake/ADLS immutable landing zone | Databricks Volumes / cloud storage |
| Unity Catalog governance | Preserved: Databricks ingests from landing zone and registers tables in UC | Native |
| Orchestration | Fabric pipelines, schedules, dependencies | Lakeflow Jobs / Workflows |
| Complex long-running workflows | Possible, but less expressive | Temporal remains stronger |
| Operational simplicity | Higher for standard extract-load patterns | Higher control for custom logic |

Fabric and Databricks both use Delta Parquet, and Fabric can access Unity Catalog-managed tables through OneLake shortcuts/mirroring, so the two platforms are designed to coexist rather than compete. [learn.microsoft](https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/small-medium-modern-data-platform)

## For API sources

Use **Fabric Data Factory** when the API is a straightforward scheduled pull:

- Use the **REST connector** in a Fabric pipeline or Dataflow Gen2 to call the endpoint, handle pagination where supported, and write raw responses to OneLake/ADLS.
- Preserve the original response as JSON/NDJSON plus ingestion metadata: source, request ID, extraction window, page/token, response hash, ingestion timestamp, and schema version.
- Let Databricks Auto Loader ingest the landed files into a **bronze streaming table** in Unity Catalog.

Fabric explicitly supports REST as a connector for Dataflow Gen2 and pipelines/copy jobs. [learn.microsoft](http://www.learn.microsoft.com/en-ie/fabric/data-factory/connector-overview)

Use **Azure Logic Apps** when the API workflow needs richer control—OAuth token refresh, retries, batching, conditional paging, callbacks, or multiple systems—because it provides HTTP actions and workflow primitives. Logic Apps supports custom REST/API integrations and can be used where no prebuilt connector exists. [learn.microsoft](http://learn.microsoft.com/en-us/azure//logic-apps/logic-apps-create-api-app)

## For SFTP batches

For SFTP, **Fabric Data Factory** is usually the simplest native option: its SFTP connector supports copy activities and can use basic authentication; it also supports on-premises/VNet connectivity scenarios. [learn.microsoft](http://learn.microsoft.com/fr-fr/fabric/data-factory/connector-sftp-overview)

A robust pattern is:

1. Fabric Data Factory copies the inbound file unchanged to a raw landing container, ideally partitioned by `source/system/interface/ingest_date`.
2. Write a manifest or use file arrival events to identify new files.
3. Databricks Auto Loader incrementally reads the new files and writes immutable bronze records to Unity Catalog.
4. Databricks performs schema evolution, deduplication, validation, and silver/gold modeling.

Databricks specifically recommends Auto Loader for incrementally processing new files arriving in ADLS Gen2, and it supports CSV, JSON, XML, Parquet, Avro, and other common batch formats. [learn.microsoft](http://www.learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/reference)

## Where Temporal still wins

Do **not** use Temporal merely to schedule copies. Use it if your ingestion has workflow characteristics that Fabric pipelines and Databricks Jobs do not express cleanly:

- Multi-step API workflows with resumable state, compensating actions, or human approval.
- Long-running extraction across many pages, cursor windows, rate-limit backoff, and partial-failure recovery.
- Complex fan-out/fan-in across many source systems with per-source retry semantics.
- Need for durable workflow history, versioned business logic, and deterministic replay.

If you adopt Temporal, keep its responsibility narrow: **orchestrate extraction and delivery to the immutable raw landing zone**. Do not make Temporal the transformation engine or the system of record. Databricks should still own bronze/silver/gold and Unity Catalog governance; Fabric can remain the landing/UI/orchestration layer if desired. Databricks documents Lakeflow Jobs for orchestrating multi-task pipelines and Unity Catalog for access control, audit, and lineage. [learn.microsoft](http://www.learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/reference)

## Practical recommendation

For your stated sources, I would choose:

| Scenario | Recommended design |
|---|---|
| Mostly scheduled API pulls and SFTP files | **Fabric Data Factory → OneLake/ADLS raw → Databricks Auto Loader → Unity Catalog bronze** |
| API with OAuth, pagination, retries, and multi-step logic | **Azure Logic Apps or Temporal → raw landing zone → Databricks Auto Loader → Unity Catalog** |
| Many heterogeneous APIs, complex recovery semantics | **Temporal for extraction orchestration → raw landing zone → Databricks** |
| Need Fabric reporting close to ingestion | **Fabric landing + Databricks UC bronze/silver/gold + Fabric shortcut/mirroring for consumption** |
| Need minimal moving parts and already standardized on Databricks | **Databricks Jobs + Auto Loader + Unity Catalog**, with a thin extraction service if APIs need custom logic |

## Important caveat

Avoid having Fabric write directly into Databricks-managed Unity Catalog tables as the primary raw tier. It creates a tighter coupling and can blur ownership of raw data. Instead, make the **landing zone the contract**: immutable files with metadata, then let Databricks own the bronze Unity Catalog tables.

Fabric can read Unity Catalog-managed data through OneLake shortcuts, but Microsoft notes limitations around downstream Unity Catalog security policies in that access path; use catalog publishing, Power BI, or Databricks notebooks where stricter governance is required. [learn.microsoft](https://learn.microsoft.com/en-us/azure/databricks/partners/bi/fabric-mirror)

**Bottom line:** Fabric is a strong native Azure replacement for the *extraction and raw-landing* portion, especially for SFTP and simple REST APIs. Keep Databricks + Unity Catalog for bronze/silver/gold and governance. Use Temporal only where durable, stateful extraction workflows genuinely justify it. [learn.microsoft](http://www.learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/azure-databricks-modern-analytics-architecture)
