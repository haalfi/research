# Temporal API Acquisition and Databricks Ingest governance follow-up

This report follows the earlier reports on this branch, which are unchanged:
[`Temporal API Acquisition and Databricks Ingest.md`](Temporal%20API%20Acquisition%20and%20Databricks%20Ingest.md)
and [`… follow-up.md`](Temporal%20API%20Acquisition%20and%20Databricks%20Ingest%20follow-up.md).

- Brief, with the scoping decisions of 2026-11-08: [`briefs/Temporal API Acquisition and Databricks Ingest governance follow-up.md`](../briefs/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest%20governance%20follow-up.md)
- Notes, tracks 01–03: [`research_notes/Temporal API Acquisition and Databricks Ingest governance follow-up/`](../research_notes/Temporal%20API%20Acquisition%20and%20Databricks%20Ingest%20governance%20follow-up/)
- Research date: 2026-11-08. Azure first (ADLS Gen2 with hierarchical namespace). Differences on AWS and GCP are noted where they were checked.
- Labels:
  - **[D] documented**: first-party sources, read in full.
  - **[R] reported**: practitioner or third-party sources.
  - **[I] inferred**: our reasoning.

## Scope of this run

Covered in this run:
- **Track 1.** Scope Item 1 in full: the UC handoff and governance between Team 1 (domain) and Team 2 (platform).
- **Track 2, boundary parts only.** For Temporal, Prefect and Dagster: whether each can write under the landing contract, its documented Databricks integration, and its lineage features.
- **Scope Item 4.** Lineage.

Settled before the run:
- Auto Loader and the file-arrival job belong to the data platform and are run by Team 2. Auto Loader is a Databricks Runtime component, not part of open-source Spark.
- Deferred to the next run: the full Track 2 comparison (paged pulls, long vendor waits, operating effort).

## Bottom line

1. **Q1.1 holds if Team 1 writes through Unity Catalog. It fails as a security claim if Team 1 writes straight to ADLS with its own Azure rights.**
   - Databricks recommends external volumes for "landing areas for raw data produced by external systems". [D]
   - It also says Unity Catalog "doesn't govern reads and writes performed directly against cloud object storage from external systems". [D]
   - So the write route decides the claim, not where the workers run.
2. **Team 2's egress constraint does not touch Team 1's uploads.**
   - Serverless egress control covers outbound traffic only. [D]
   - Team 1's writes are inbound and pass through ingress controls: IP access lists, context-based ingress and Private Link. [D]
   - The constraint would bind Team 1 only if its vendor calls ran on Databricks serverless. [I]
3. **The privilege names in the brief need correcting:**
   - Team 1: `USE CATALOG`, `USE SCHEMA`, `WRITE VOLUME`, and also `READ VOLUME`. The docs disagree on whether READ VOLUME is required.
   - Team 2: owner or `MANAGE` on the external location to turn on file events, plus `CAN MANAGE` on the job. [D]
4. **Schema evolution is controlled by whoever owns the job and the schema location.** With Team 2 owning both, that is Team 2. [I from D]
   - Under the default mode `addNewColumns`, a change Team 1 makes fails Team 2's stream until it restarts. [D]
   - No Databricks page assigns this to a team, and no "data contract" feature exists. [D, absence]
5. **End-to-end lineage needs custom work in every combination.**
   - UC records bronze → silver automatically. [D]
   - Nothing records API source → landed file automatically. Linking them takes UC External Lineage (GA 2026-06-08), which is not written to the lineage system tables. [D]
   - No orchestrator feeds UC lineage out of the box. [D, absence]

---

## Scope Item 1: UC handoff and governance

### Storage hierarchy for the landing zone

- **[D] Use an external volume.** Databricks' UC best practices say: "Use external volumes: To register landing areas for raw data produced by external systems … To register staging locations for ingestion, for example, using Auto Loader".
  - Also: "For ingestion use cases in which the data is copied to another location (for example, using Auto Loader or COPY INTO) use external volumes".
  - Also: "never create external volumes or tables at the root of an external location".
  - Source: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/best-practices (2026-10-30).
- **[D] Managed volumes are for most other uses.** "All access goes through UC", and vended credentials can only read them ("Managed volumes are supported for read access only").
  - Sources: …/volumes/ (2026-10-12); …/external-access/credential-vending (2026-11-06).
  - Dropping a managed volume deletes its files. Dropping an external volume does not. (…/data-governance/unity-catalog/managed-versus-external, 2026-10-30)
- **[D] Requirements on the external location:**
  - The storage account "must have a hierarchical namespace". (…/connect/unity-catalog/cloud-storage/external-locations-adls, 2026-10-14)
  - File events are not supported on Azure Blob Storage without HNS. (…/manage-external-locations, 2026-11-04)
- **[D] The governance model fits.**
  - Federated governance is the recommended start.
  - In hub and spoke, spoke catalogs are "owned and managed by business units", and the guide says: "Use volumes to access landing, raw, or unstructured data".
  - Source: …/lakehouse-architecture/deployment-guide/unity-catalog (2026-10-29).
  - "Grant the ability to create external locations only to administrators". (UC best practices)
- **[I] Implied hierarchy:**
  - Team 2 owns the storage credential and the external location.
  - The landing external volume lives in a domain or landing schema below a sub-path, never at the location's root.
  - Checkpoints and schema locations go in a separate volume that only Team 2 can write. Databricks says to keep the checkpoint "with the stream's output, not its source data". [D]

### How Team 1's workers write: the deciding choice

| Route | How it works | Governed by UC | Audit | Network | Maturity |
|---|---|---|---|---|---|
| **a. Files API / SDK as a Team 1 service principal** | `PUT /api/2.0/fs/files/Volumes/...`, or `w.files.upload`. Auth by OAuth M2M, which Databricks prefers. | Yes. Works for both managed and external volumes. | `filesystem` service, `filesPut` with path and size. [D] | The worker must reach the workspace; IP access lists, context-based ingress and Private Link apply. [D] | Files API 2.0 upload is **Public Preview**, capped at 5 GiB per file. 3.0 (multipart, `If-None-Match: *`) is **Beta**, needs an admin toggle and uses a separate host. The SDK reaches the cloud maximum from v0.72, but only 5 GB behind an Azure storage firewall. [D] |
| **b. Credential vending** | `POST /api/2.0/unity-catalog/temporary-volume-credentials`, then a direct ADLS write with a temporary, scoped credential. | Access is granted by UC (`EXTERNAL USE SCHEMA` plus READ/WRITE VOLUME). Works for external volumes only. | `generateTemporaryVolumeCredential`. [D] The writes themselves appear in storage logs only [I]. | The worker must reach both the workspace and the storage account. [I] | **Public Preview**. [D] |
| **c. Direct ADLS write under Team 1's own Azure RBAC** | Any Azure SDK writes to the path behind the external volume. | **No.** "Unity Catalog doesn't govern reads and writes performed directly against cloud object storage from external systems". Databricks warns that this "bypasses Unity Catalog. This exposes data to over-permissioning, exfiltration…". [D] | Not in Databricks audit logs [I]. Azure Storage logs are off until a diagnostic setting is created. [D] | Storage firewall or private endpoint for the writer. [I] | Mature on Azure, outside Databricks. |

Sources:
- https://docs.databricks.com/api/azure/workspace/files/upload (undated)
- …/volumes/files-api (2026-10-27)
- …/dev-tools/sdk-python (2026-09-11)
- …/external-access/credential-vending (2026-11-06)
- …/connect/unity-catalog/ (2026-09-11)
- …/admin/account-settings/audit-logs (2026-11-05)
- …/security/network/front-end/ip-access-list (2026-11-04)

**[I] Verdict on Q1.1.**
- Routes a and b fulfil the hypothesis. Route a is simpler: one hop, and audited per file.
- Route c lets Team 1 run with any tool, but it moves governance out of UC into Azure RBAC, which works against the "minimizes platform security risk" part.
- Route a's maturity risk is real: the upload API is still Preview, and the large-file path is Beta.

### Behaviour that affects Team 1's writes

- **[D] Overwrites do not trigger runs.** "Only new files trigger runs. Overwriting an existing file with a file of the same name does not trigger a run." The Files API overwrites by default ("If true or unspecified").
- **[D] Detection waits for FlushWithClose.** "File events listens for the FlushWithClose event to process a file. Some Azure API usage may not emit this event, which could delay file discovery." Uploads through `Azure.Storage.Blobs` "can cause high latency".
- **[D] Event Grid confirms the same.** On HNS accounts, BlobCreated fires on CreateFile + FlushWithClose. (https://learn.microsoft.com/en-us/azure/event-grid/event-schema-blob-storage, 2025-10-21)
- **[I] How files should be written:**
  - every file under a new, immutable name;
  - no write-then-rename inside the watched path (how managed file events treat a rename is undocumented);
  - for route c, a client that ends with FlushWithClose, such as the ADLS Data Lake API.
- **[I] Not documented:** whether a Files API upload emits FlushWithClose. The volume upload page simply lists file-arrival triggers as the next step.

### Permission sets

| Principal | Grants | Basis |
|---|---|---|
| **Team 1 worker service principal (route a)** | `USE CATALOG` on the landing catalog; `USE SCHEMA` on the landing schema; `WRITE VOLUME` **and** `READ VOLUME` on the landing volume. | [D] The volume privileges page lists READ+WRITE VOLUME for "Create, delete, or update files" (…/volumes/privileges, 2026-09-11). The UI upload page lists WRITE VOLUME only (…/volumes/volume-files, 2026-10-27), so the docs conflict. Grant both [I]. |
| Team 1 worker service principal (route b) | The route-a grants, plus `EXTERNAL USE SCHEMA`, which only the catalog owner can grant. | [D] credential-vending; privileges-reference (2026-11-06) |
| Team 1 group | `CAN VIEW` on Team 2's job; read on a filtered view of the job and Auto Loader status. Not CAN MANAGE. | [D] CAN VIEW "Can view job run results". [I] The filtered view is undocumented, and granting SELECT on `system.lakeflow` would expose every job in the region. |
| **Team 2 job run-as service principal** | `USE CATALOG`/`USE SCHEMA`; `READ VOLUME` on the landing volume; `READ VOLUME`+`WRITE VOLUME` on the checkpoint/schema volume; `CREATE TABLE` and ownership or `MODIFY` on bronze. | [D] The Auto Loader UC example uses READ FILES on the source and READ/WRITE FILES + CREATE TABLE on the checkpoint and target location (…/auto-loader/unity-catalog, 2026-09-11). [I] That is mapped here to volume privileges; no volume-specific list exists. |
| **Team 2 platform group** (owns the external location and the job) | Owner of, or `MANAGE` on, the external location (needed to turn on file events); `CREATE EXTERNAL VOLUME`; `CAN MANAGE` on the job; "READ permission on the storage location" for the trigger. | [D] …/jobs/file-arrival-triggers (2026-11-06). The trigger page does not say which UC privilege "READ" means. |
| **Storage credential (Azure managed identity)** | Storage Blob Data Contributor; Storage Queue Data Contributor; for automatic file-events setup, Storage Account Contributor plus an Event Grid role on the resource group. | [D] …/manage-external-locations (2026-11-04) names **EventGrid Data Contributor**. …/external-locations-adls (2026-10-14) names **EventGrid EventSubscription Contributor**. Unresolved. |
| Who can grant | Owners of the catalog, schema or volume, or anyone with `MANAGE` on any of them. "ALL PRIVILEGES does not include the MANAGE privilege." | [D] …/volumes/privileges; privileges-reference |

Guidance that fits the team split [D] (UC best practices; …/jobs/privileges, 2026-11-05):
- "Use groups to assign ownership".
- "Use service principals to run jobs".
- "create a schema per team".
- "Databricks recommends changing the Run as user to a service principal, so that privileges can be controlled separately from the owner's privileges".

### Can Team 1 own code that runs in Team 2's job?

- **[D] Git-sourced jobs.** A job can run code from a remote Git repo pinned to a branch, tag or commit. The SHA is recorded per run, and "All tasks in a job must reference the same commit". (…/jobs/git, 2026-11-05)
- **[D] Bundles.** Declarative Automation Bundles (formerly Databricks Asset Bundles) can separate the identity that deploys from the identity that runs, for jobs and pipelines only. Non-admins can set `run_as` only to themselves. Databricks advises deploying to an immutable folder. (…/dev-tools/bundles/run-as, 2026-10-07)
- **[I] What that allows:** Team 1 can own the repository, for example bronze-to-silver logic or an expectation rules table, while Team 2 owns the job, its run-as identity and its deployment.

### Schema drift: who handles schema evolution

What the docs say [D] (…/auto-loader/schema, 2026-11-05, the same on AWS and GCP; best-practices, 2026-10-07):

| Mode | What happens when Team 1 adds a field |
|---|---|
| `addNewColumns` (default when no schema is given) | "Stream fails with an UnknownFieldException … Restarting the stream resumes processing". This depends on automatic retry. In multi-task continuous jobs, "The failed stream can stay down while the job appears healthy." |
| `addNewColumnsWithTypeWidening` | Same as above, plus type widening. **Public Preview**, DBR 16.4+. |
| `rescue` | "never evolves the schema and the stream does not fail". New fields land in `_rescued_data` along with the source file path. |
| `failOnNewColumns` | Hard stop until the schema is updated or the file is removed. The docs pair it with "Strict schema contract required". |
| `none` (default when a schema is given) | New columns are dropped silently. |
| VARIANT / `singleVariantColumn` | No evolution and no rescue. The docs recommend it for "Arbitrary or unpredictable schema". |

Other documented facts:
- **Ownership:** the schema lives in `_schemas` under `cloudFiles.schemaLocation`. In Lakeflow pipelines, Databricks manages that location.
- **Rollback:** "Contact Databricks support for help."
- **Detecting drift:** watch for changes in `_schemas`, and use expectations that `_rescued_data` and `_corrupt_record` are NULL.
- **Contracts:** no data-contract feature exists. The nearest documented mechanisms are:
  - inline `schemaHints`;
  - a central expectation rules table ("Store expectation definitions separately from pipeline logic … using a Delta table");
  - UC comments and governed tags.

  Sources: …/ldp/expectation-patterns (2026-10-26); …/database-objects/tags (2026-10-26).
- **Restarts:** the docs disagree on whether restarts are automatic or manual (…/data-engineering/schema-evolution vs the schema page).

**[I] Answer to "which team handles schema evolution":**
- **Team 2 operates it** in every case, because it owns the job, the schema location and the restart.
- **Team 1 must announce changes**, because it changes the vendor pulls.
- **How much they need to coordinate depends on the mode:**
  - With `addNewColumns`, every Team 1 change becomes a Team 2 incident, at least a failed run and a restart. It needs advance notice or automatic retry.
  - With `rescue` or VARIANT, bronze stays up regardless. Team 1 can then own the bronze → silver parsing (a Git-sourced task or a rules table), and schema meaning stays with the team that understands the payload.
  - `failOnNewColumns` makes the contract strict, and the cost is an outage on every change.
- **No first-party page assigns this.** The above is an operating-model inference, not documented guidance.

### Failure signals across the team boundary

- **[D] Notifications.**
  - Editing notifications needs CAN MANAGE or IS OWNER. Only workspace admins create system destinations, which are then "available to all users".
  - Job-level notifications are not sent on task retries.
  - Trigger evaluation failures surface through job-failure notifications.
  - Sources: …/jobs/notifications (2026-11-06); …/admin/workspace-settings/notification-destinations (2026-10-15).
- **[D] System tables.** `system.lakeflow.job_run_timeline` holds `result_state`, is regional, typically lags by up to about an hour, and keeps 395 days. Access is granted by an admin on the whole system schema. (…/admin/system-tables/jobs, 2026-11-06)
- **[I] What Team 2 should provide:** add Team 1's destination to its job's task-failure notifications, and publish a view filtered by job ID. Team 1, with CAN VIEW, cannot set these up itself.

---

## Scope Item 4: End-to-end lineage

### What UC records [D]

Sources: …/data-governance/unity-catalog/data-lineage (2026-11-04); …/admin/system-tables/lineage (2026-11-04).

- **Automatic capture:**
  - UC captures lineage for Spark DataFrame and DBSQL work, down to column level.
  - "Nodes can represent tables and views, ML model versions, external assets, and file paths".
  - `system.access.table_lineage` and `column_lineage` carry `source_type = PATH` and `source_path`, for example `abfss://…`.
- **Limits:**
  - The tables cover a "subset of all read/write events … only emitted when lineage can be inferred".
  - They keep 395 days. Catalog Explorer and the API keep lineage captured after 2024-09-01 indefinitely.
- **Not documented:** whether Auto Loader reads from `/Volumes/...` appear as PATH, and in which form. Needs a test.
- **[I] Team 1's uploads leave no automatic lineage,** because capture requires work running on Databricks.

### Linking outside systems [D]

Source: …/data-governance/unity-catalog/external-lineage (2026-10-07); release note https://docs.databricks.com/aws/en/release-notes/product/2026/june.

- **External lineage** registers outside systems as external metadata and links them to UC tables or paths, through the UI, REST (`/api/2.0/lineage-tracking/external-metadata`, `/external-lineage`) or SDK.
- **Status:** GA since 2026-06-08 per the release note. The API reference still says Public Preview.
- **Limits:** "External lineage is not recorded in the lineage system tables". Caps are 10,000 objects and 100,000 relationships per metastore. `system_type` has no value for Temporal, Prefect or Dagster, so `OTHER` would be used [I].
- **OpenLineage:** Databricks documents no way to ingest OpenLineage into UC. [D, absence]

### By combination

| Combination | API source → landed file | Landed file → bronze → silver | Inside the orchestrator | Effort [I] |
|---|---|---|---|---|
| **Temporal + Databricks** | Nothing built in. Temporal has no lineage feature and no Databricks integration [D, absence]. Search Attributes (indexed, "stored unencrypted") and Memo (40 KB on Cloud) carry metadata only [D]. | UC automatic (bronze → silver). File → bronze as PATH, untested. | Only the manifest and ledger row [I]. | Custom activity that calls the UC External Lineage API per feed or manifest. The manifest is the natural record. |
| **Prefect (OSS) + Databricks** | Asset lineage (`@materialize`, `asset_deps`) is **Prefect Cloud only** [D]. OSS has Artifacts, for example `create_link_artifact` [D]. OpenLineage exists only as an unofficial beta, `openlineage-prefect` 0.0.1b22, with its PR unmerged [R]. | Same as above. `prefect-databricks` 0.4.2 ("Maintained by Prefect") runs run-now and waits [D]; it does no lineage. | Artifacts only on OSS. | Custom External Lineage calls, the same as for Temporal. Paid tier for native asset lineage. |
| **Pure Dagster** | External assets bring files "populated by a bespoke internal tool" into one graph (OSS) [D]. Runtime metadata comes from `MaterializeResult`. | `dagster-databricks` 0.29.29: Pipes reports materializations back from Databricks; the serverless client uses a UC volume as transport [D]. `run_job` for existing jobs is **Preview** [D]. UC still records bronze → silver itself. | Full asset graph in OSS. The column-lineage UI is Dagster+ only [D]. | Lineage is unified **inside Dagster**. Getting it into UC still takes custom External Lineage calls or OpenLineage. `dagster-openlineage` 0.2.1 is "community-maintained", and UC cannot ingest OpenLineage anyway. |

Sources:
- https://docs.temporal.io/search-attribute; https://docs.temporal.io/workflow-execution
- https://docs.prefect.io/v3/concepts/assets; https://docs.prefect.io/integrations/prefect-databricks
- https://docs.dagster.io/guides/build/assets/external-assets
- https://docs.dagster.io/integrations/libraries/databricks
- https://docs.dagster.io/integrations/libraries/openlineage

Package versions are from PyPI on 2026-11-08.

**[I] Partial verdict on Q2.2's lineage claim.** "Unified Dagster assets deliver end-to-end data lineage across team boundaries" **holds only inside Dagster's graph**. Two further caveats:
- Team 2 owns the Auto Loader job, so Dagster can show it only as an external or Pipes-reported asset, unless Team 2 also runs Dagster.
- UC, Team 2's system of record, still needs a bridge.

The long-running-wait half of Q2.2 is deferred.

---

## Track 2, boundary parts: does each orchestrator fit the landing contract?

| | Temporal | Prefect OSS | Dagster OSS |
|---|---|---|---|
| Write to a UC volume (route a) | Ordinary activity code with `databricks-sdk` [I] | No UC-volume block; `databricks-sdk` in a task [I] | No documented resource for landing files in a volume [D]; `databricks-sdk` in an asset [I] |
| Write to ADLS (routes b and c) | Activity code [I] | `prefect-azure` 0.4.13 blob blocks [D] | `dagster-azure` 0.29.29 `ADLS2Resource` [D] |
| Trigger a Databricks job | Activity calls run-now with an idempotency token [I] (from the first report) | `prefect-databricks` run-now and wait [D] | `dagster-databricks`: `run_now(...).result()` or Pipes [D] |
| Report back from Databricks | Polling, or a signal from a webhook [I] | Polls the run status [D] | Pipes `report_asset_materialization` [D] |
| Lineage into UC | Custom [I] | Custom [I] | Custom [I] |

**[I] How the contract shapes the comparison.**
- The landing contract does not depend on the orchestrator. All three can write under route a or route c with ordinary code.
- The boundary differences that matter: Prefect and Dagster have maintained Databricks integrations and Temporal has none. Dagster alone can show externally produced files and Databricks results in one open-source graph.
- None of this decides Track 2. The paged-pull and long-wait criteria do, and they are deferred.

---

## Hypotheses and assumptions

| # | Hypothesis or assumption | Verdict | What it changes |
|---|---|---|---|
| H1.1 | Workers outside Databricks, landing in Team 2-governed UC volumes, minimise platform risk and keep Team 1 agile | **Holds if** writes go through UC (Files API or credential vending) into an **external** volume. **Fails** as a security claim under direct ADLS RBAC (route c). | Choose the write route explicitly. Accept the Preview status of the Files API upload or of credential vending, or govern route c in Azure. |
| H1.1b | Team 2's strict egress constrains the design | **Does not apply** to Team 1's external workers. **Holds** only for code on Databricks serverless (account-admin network policy, at most 100 FQDNs). | Team 2's levers for Team 1 are ingress controls (IP lists, context-based ingress, Private Link), not egress. |
| H1.2 | Privileges `WRITE` for Team 1, `READ`/`MANAGE` for Team 2 | **Holds with corrections**. The names are `WRITE VOLUME` + `READ VOLUME` (+ `USE CATALOG`/`USE SCHEMA`). `MANAGE` belongs on the external location, for file events. `CAN MANAGE` belongs on the job. | Use the permission table above. Two doc conflicts remain open: READ VOLUME for writers, and the Event Grid role name. |
| H1.2b | File-arrival trigger plus file events fit uploads from outside Databricks | **Holds if** files are new and immutable (no overwrite, no rename inside the watched path) and the Azure writes complete with FlushWithClose. | The Files API's default `overwrite` must be avoided by using new names. Whether Files API uploads emit FlushWithClose is undocumented. |
| H1.2c | Schema-management responsibility can be assigned | **Holds by inference only.** Team 2 operates evolution. The mode decides how much Team 1 has to coordinate. | Choosing `rescue` or VARIANT at bronze separates the teams. The default `addNewColumns` couples them through stream failures. |
| H2.2 (lineage half) | Pure Dagster gives end-to-end lineage across teams | **Holds if** "end to end" means inside Dagster. **Fails** for lineage in UC without a custom bridge. | Lineage into UC is custom work for every orchestrator. |
| S4 | Any combination delivers source-to-silver lineage out of the box | **Fails** for all three | Budget an External Lineage writer, keyed on the manifest. It is not visible in the lineage system tables. |

## Gaps

- **Doc conflicts:**
  - READ VOLUME for volume writers (privileges page vs UI upload page).
  - The Event Grid role name for automatic file events.
  - Groups as job owners.
  - Pipeline run-as vs owner credentials.
  - Default catalog pattern: environment vs domain.
  - Manual vs automatic restart on schema change.
- **Not documented:**
  - Whether Files API uploads emit FlushWithClose or fire triggers.
  - How managed file events treat a rename.
  - Whether Auto Loader reads from `/Volumes` appear in the lineage tables, and in which form.
  - The exact UC privilege behind "READ" for triggers.
  - Whether Entra tokens work on the Files API 3.0 host.
  - The effect of the egress policy on Files API 3.0's own route to storage.
  - Row-level access to system tables.
  - A cross-team RACI.
  - A data-contract feature.
  - Who owns `_schemas` beyond ordinary path privileges.
- **Maturity:** Files API upload (Public Preview), Files API 3.0 (Beta), credential vending (Public Preview), and Dagster Pipes `run_job` (Preview). The External Lineage GA status conflicts with its API reference.
- **Not researched:** egress from classic compute (VNet/NSG). AWS and GCP were compared on only a few pages.
- **Workspace tests** would settle the trigger and lineage questions:
  - Files API upload → trigger.
  - `/Volumes` read → lineage row.
  - Rename behaviour.
- **Deferred to the next run (Track 2):**
  - Prefect vs Temporal on paged pulls, long vendor waits and operating effort.
  - Pure Dagster for multi-hour waits.
