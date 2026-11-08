# Governance track 3: Lineage and how each orchestrator fits the boundary

## Method

A verification agent read the following on 2026-11-08:

- **Databricks:** full text of the AWS and Azure (learn.microsoft.com) pages.
- **Orchestrator docs:** sources from shallow clones of four repos, because the live Prefect and Dagster pages render client-side:
  - temporalio/documentation (HEAD 2026-11-06)
  - PrefectHQ/prefect (2026-11-06)
  - dagster-io/dagster (2026-11-07)
  - OpenLineage/OpenLineage (2026-11-06)
- **Package versions:** the PyPI JSON API.

Labels: **documented** / **reported** / **inferred**.

## Q1. Unity Catalog lineage

- **documented** (GA, included with UC): lineage is captured automatically, down to column level. "Nodes can represent tables and views, ML model versions, external assets, and file paths."
  - Source: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/data-lineage (2026-11-04)
  - AWS version: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage
- **documented**: capture covers only Spark DataFrame and Databricks SQL interfaces.
- **documented**: for path references, Catalog Explorer and the lineage API show no column lineage. The `system.access.column_lineage` table does record it, "with the path in source_path or target_path".
- **documented** (https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/lineage, 2026-11-04): what the system tables hold.
  - `source_path` holds the cloud location, for example `abfss://…`.
  - `source_type` is one of TABLE, PATH, VIEW, MATERIALIZED_VIEW, METRIC_VIEW or STREAMING_TABLE.
  - `entity_metadata` names the job, notebook or pipeline.
  - Coverage is partial: "subset of all read/write events … Records are only emitted when lineage can be inferred."
- **documented**: retention.
  - System tables keep a 395-day rolling window.
  - Catalog Explorer and the API keep lineage captured after 2024-09-01 indefinitely.
- **not documented**: whether Auto Loader reads from `/Volumes/...` appear as PATH nodes, or whether `source_path` holds the `/Volumes` path or the underlying `abfss://` URI. **inferred** from the "file paths" wording only. Needs a test.
- **inferred**: files that Team 1 uploads through the Files API produce no automatic lineage, because capture needs Spark or DBSQL execution on Databricks.

## Q2. UC external lineage (formerly "Bring your own lineage")

- **documented**: external systems can be registered as external metadata and linked to UC tables, paths, models or other external objects. This works through the UI, the REST API or the SDK, with column mappings and properties.
  - Source: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/external-lineage (2026-10-07)
- **documented**: endpoints and SDK calls.
  - REST: `POST /api/2.0/lineage-tracking/external-metadata` and `.../external-lineage`.
  - SDK: `w.external_metadata.create_external_metadata` and `w.external_lineage.create_external_lineage_relationship`.
  - `system_type` has 23 values, including `OTHER`, and none for Temporal, Prefect or Dagster.
  - API reference: https://docs.databricks.com/api/workspace/externalmetadata
- **documented**: status.
  - Public Preview from 2025-06-27; GA from 2026-06-08 ("External lineage (formerly Bring Your Own Lineage) in Unity Catalog is now generally available"): https://docs.databricks.com/aws/en/release-notes/product/2026/june
  - **Conflict:** the API reference still labels its fields Public Preview.
- **documented**: limitations.
  - "External lineage is not recorded in the lineage system tables".
  - Caps per metastore: 10,000 external metadata objects and 100,000 relationships.
- **documented (absence)**: Databricks documents no way to ingest OpenLineage into UC. It appears in no page of the 6,402-URL AWS sitemap and in no Microsoft Learn result.
  - **inferred**: any bridge would be custom code calling the External Lineage API.

## Q3. Lineage features in each orchestrator

### Temporal

- **documented (absence)**: no lineage feature. The docs repo (802 pages) has 0 hits for lineage, OpenLineage or databricks, and OpenLineage lists no Temporal integration.
- **documented**: two ways to attach metadata, neither of them lineage.
  - Search Attributes: indexed, "stored unencrypted in the Visibility store" (https://docs.temporal.io/search-attribute).
  - Memo: non-indexed, 40 KB on Cloud (https://docs.temporal.io/workflow-execution).
- **inferred**: lineage would need custom calls to the UC External Lineage API from an activity.

### Prefect

- **documented**: Assets and asset lineage are marked Cloud-only, with a "Prefect Cloud" badge.
  - What they are: "Assets in Prefect represent any outcome or output of your Prefect workflows. They provide an interface to model all forms of data and model lineage."
  - How you use them: `@materialize("s3://…")`, `asset_deps`, `Asset.add_metadata()`.
  - Source: https://docs.prefect.io/v3/concepts/assets
  - **inferred**: the module ships in the OSS package, but the docs mark the feature Cloud-only.
- **documented** (OSS): Artifacts such as `create_link_artifact` and table or markdown artifacts.
- **reported**: OpenLineage support is unofficial and pre-release.
  - PyPI `openlineage-prefect` is at 0.0.1b22 (2026-10-12).
  - The package's source link points to a directory that does not exist on OpenLineage main.
  - PR "integrations: add Prefect integration" (opened 2026-05-02) is still open.

### Dagster

- **documented** (OSS): external assets bring assets that other systems orchestrate into one lineage graph. Example: "Files in a data lake that are populated by a bespoke internal tool"; "an external system must inform Dagster when an external asset is updated."
  - Runtime metadata comes from `MaterializeResult(metadata=…)`.
  - Source: https://docs.dagster.io/guides/build/assets/external-assets
- **documented**: "Viewing column-level lineage in the UI is a Dagster+ feature". OSS can still emit the `dagster/column_lineage` metadata.
  - Source: https://docs.dagster.io/guides/build/assets/metadata-and-tags/column-level-lineage
- **documented**: OpenLineage status.
  - The old integration in the OpenLineage repo was removed in OL 1.39.0 (2025-10-07). The last `openlineage-dagster` release was 1.38.0.
  - The replacement, `dagster-openlineage`, is "a community-maintained integration": 0.2.1 (2026-05-22), requires Dagster ≥1.11.6.
  - It works through an `OpenLineageEventLogStorage` wrapper (OSS) and an `openlineage_sensor`.
  - Source: https://docs.dagster.io/integrations/libraries/openlineage

## Q4. Databricks integration in each orchestrator

- **Temporal**
  - **documented (absence)**: no Databricks integration.
  - **inferred**: ordinary activity code using databricks-sdk or REST. Latest SDK: temporalio 1.35.0 (2026-10-28).
- **Prefect**
  - **documented**: `prefect-databricks` is "Maintained by Prefect". 0.4.2 (2026-07-15), Jobs API 2.1.
  - What it does: "Trigger an existing Databricks job and wait for it to complete — the flagship use case". `jobs_runs_submit_by_id_and_wait_for_completion` calls `jobs_run_now` and polls (`max_wait_seconds`, `poll_frequency_seconds`).
  - Auth: PAT or service principal (Azure `tenant_id`).
  - No lineage features and no UC volume features.
  - Source: https://docs.prefect.io/integrations/prefect-databricks
- **Dagster**
  - **documented**: `dagster-databricks` is "dagster-supported". 0.29.29 (2026-11-05), with dagster 1.13.29.
  - It offers Databricks Connect, Pipes, DatabricksAssetBundleComponent and DatabricksWorkspaceComponent.
  - Pipes: "Submit Databricks jobs and stream logs/metadata back to Dagster". `PipesDatabricksServerlessClient` "uses a Unity Catalog Volume as the message transport layer".
  - The `run_job` for existing jobs is **Preview**: "not considered ready for production use".
  - The Databricks side can call `pipes.report_asset_materialization(metadata=…)`.
  - Without Pipes, use `client.jobs.run_now(job_id=...).result()`.
  - A "Dagster Databricks Connection (Dagster+ only)" discovers UC tables.
  - Source: https://docs.dagster.io/integrations/libraries/databricks

## Q5. How each orchestrator lands files

- **Databricks side (documented)**
  - Files API 2.0 upload: Public Preview, 5 GiB.
  - Files API 3.0: Beta since 2026-10-23.
  - SDK `w.files.upload` / `upload_from`: up to the cloud maximum from SDK v0.72.0. databricks-sdk 0.162.0 (2026-11-05) carries the PyPI classifier "4 - Beta".
- **Temporal**
  - **documented**: External Storage (S3 and GCS drivers, Public Preview) offloads payloads. It is not for landing data.
  - **inferred**: landing files is ordinary activity code.
- **Prefect**
  - **documented**: `prefect-azure` 0.4.13 (2026-09-08): "read and write Azure Blob Storage", via `blob_storage_upload` and `AzureBlobStorageContainer.upload_from_path`.
  - **documented**: `prefect-aws` 0.7.12 provides the `S3Bucket` block.
  - There is no UC volume block. **inferred**: databricks-sdk in task code.
- **Dagster**
  - **documented**: `dagster-azure` 0.29.29: `ADLS2Resource` ("ADLS2 is our primary focus").
  - There is no documented resource for landing files in a UC volume.
  - **inferred** from source code: dagster-databricks uses `FilesAPI.upload`, but only for Pipes messages.

## Gaps

1. Whether Auto Loader reads from `/Volumes/...` appear in the lineage system tables as PATH, and in what form. Needs a test.
2. External lineage is not in the system tables, so lineage from the API source to the landed file is visible only in Catalog Explorer and the API.
3. No documented OpenLineage ingestion into UC, so every orchestrator needs custom External Lineage API calls.
4. Prefect's OpenLineage support is unofficial. The PR body returned 403 in this session.
5. Who maintains dagster-openlineage is unverified beyond the "community-maintained" label.
6. The Prefect and Dagster pages show no dates. Quotes come from the repo HEADs listed above.
7. GA status of the Files API 2.0 upload is unresolved.
