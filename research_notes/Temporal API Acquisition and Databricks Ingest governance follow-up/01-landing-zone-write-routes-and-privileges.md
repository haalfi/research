# Governance track 1: How an external writer reaches the landing zone, privileges, audit, network

## Method

- A verification agent read every page in full on 2026-11-08 (Azure first).
- All pages returned HTTP 200 unless marked otherwise.
- Dates are each page's "Last updated" (ms.date). The Files API reference is undated.
- `…` = https://learn.microsoft.com/en-us/azure/databricks.
- Labels: **documented** / **inferred** / **not confirmed**.

## Q1. Write routes for a writer outside Databricks

### (a) Files API / SDK (governed by Unity Catalog)

- **documented**: Files API 2.0 upload: "PUT /api/2.0/fs/files{file_path} Uploads a file of up to 5 GiB"
  - Status: **Public Preview**.
  - Default is overwrite: "If true or unspecified, an existing file will be overwritten."
  - Source: https://docs.databricks.com/api/azure/workspace/files/upload (undated).
- **documented**: Files API 3.0 (**Beta**). A workspace admin must turn it on from the Previews page.
  - It uses a separate host: `<workspace-id>.storage.<region>.<domain>`.
  - Multipart upload: parts of at least 5 MiB and at most 4000 MiB, up to 10,000 parts.
  - Conditional create: "If-None-Match: * uploads the file only if no file exists at the path."
  - Source: …/volumes/files-api (2026-10-27).
- **documented**: Python SDK `w.files.upload`: from v0.72.0, files are supported up to the cloud storage maximum.
  - Exception: "If an Azure storage account has a firewall enabled, there is a 5 GB file size limit."
  - Source: …/dev-tools/sdk-python (2026-09-11).
- **documented**: Authentication.
  - OAuth M2M is preferred for service principals; tokens are valid for 1 hour (…/dev-tools/auth/oauth-m2m, 2026-10-30).
  - Use Entra service principal authentication only when you also need other Azure resources (…/dev-tools/auth/azure-sp, 2026-09-11).
- **not confirmed**: That Entra tokens work on the Files API 3.0 host.

### (b) Direct writes to the cloud path under an external volume (not governed by Unity Catalog)

- **documented**: Databricks recommends external volumes for this case, but says governance then has to come from outside.
  - "Databricks recommends using external volumes to store non-tabular data files that are read or written by external systems … Unity Catalog doesn't govern reads and writes performed directly against cloud object storage from external systems, so you must apply additional governance outside Azure Databricks".
  - The external governance it describes is credential vending, or cloud IAM aligned with UC grants.
  - Source: …/volumes/ (2026-10-12). The AWS page has the same text.
- **documented**: Warnings against direct access.
  - Direct ADLS access to UC-governed containers "bypasses Unity Catalog. This exposes data to over-permissioning, exfiltration, and unauthorized access, while complicating auditing" (…/connect/unity-catalog/, 2026-09-11).
  - "limit the number of users with direct access" (…/data-governance/unity-catalog/best-practices, 2026-10-30).
- **documented**: The WRITE FILES privilege description: "Databricks recommends against writing files directly to cloud object storage. Instead, manage write access … using volumes and the WRITE VOLUME privilege." (…/data-governance/unity-catalog/access-control/privileges-reference, 2026-11-06)
- **documented**: There is a middle route, **volume credential vending** (**Public Preview**).
  - "temporary, scoped credentials"
  - Requires EXTERNAL USE SCHEMA + READ VOLUME, and also WRITE VOLUME for writes.
  - Endpoint: `POST /api/2.0/unity-catalog/temporary-volume-credentials`.
  - Source: …/external-access/credential-vending (2026-11-06).

### (c) Managed volumes

- **documented**: Credential vending: "Managed volumes are supported for read access only. External volumes support both read and write access." (credential-vending page)
- **documented**: Managed volumes: "All access goes through UC" (…/volumes/).
  - Best practices: "Do not use a container that can be accessed from outside of Unity Catalog" for managed storage.
- **inferred**: An outside writer can reach a managed volume only through Databricks interfaces: the Files API, SDK, CLI, or SQL `PUT INTO`.

## Q2. Managed vs external volumes

- **documented**: DROP behaviour.
  - Dropping a managed volume deletes its files.
  - Dropping an external volume removes only the definition.
  - Source: …/data-governance/unity-catalog/managed-versus-external (2026-10-30).
- **documented**: Volumes can be recovered for 7 days after a drop. Managed files are purged between 7 and about 30 days.
  - Sources: …/volumes/utility-commands (2026-11-05); …/data-governance/unity-catalog/object-storage-lifecycle (2026-11-05).
- **documented**: UC best practices (2026-10-30).
  - "Use managed volumes: For most use cases".
  - "Use external volumes: To register landing areas for raw data produced by external systems … To register staging locations for ingestion, for example, using Auto Loader".
  - "For ingestion use cases in which the data is copied to another location (for example, using Auto Loader or COPY INTO) use external volumes."
  - "never create external volumes or tables at the root of an external location."

## Q3. Unity Catalog privileges

- **documented**: Writing to a volume.
  - The volume privileges page requires USE CATALOG, USE SCHEMA, **READ VOLUME, WRITE VOLUME** (…/volumes/privileges, 2026-09-11).
  - **Conflict**: the UI upload page lists only WRITE VOLUME + USE SCHEMA + USE CATALOG (…/volumes/volume-files, 2026-10-27).
  - **inferred**: Grant READ VOLUME too.
- **documented**: External location privileges (privileges-reference).
  - READ FILES "is also required for write operations on external locations".
  - "WRITE FILES requires READ FILES".
  - CREATE EXTERNAL VOLUME allows creating volumes on the location.
  - MANAGE allows managing grants, transferring ownership and deleting without being the owner. "ALL PRIVILEGES does not include the MANAGE privilege."
  - "Only the catalog owner can grant" EXTERNAL USE SCHEMA.
- **documented**: Access by path to an external volume is "governed by the privileges granted on the volume, not the privileges granted on the external location" (utility-commands).
- **documented**: Who can grant on a volume: the owners of the catalog, schema or volume, or anyone with MANAGE on any of them (…/volumes/privileges).
- **documented**: The Auto Loader UC example assumes READ FILES on the source location, plus READ FILES, WRITE FILES and CREATE TABLE on the checkpoint/target location. "Databricks recommends always storing checkpoint and schema evolution information in storage locations managed by Unity Catalog." (…/ingestion/cloud-object-storage/auto-loader/unity-catalog, 2026-09-11)
  - **inferred**: Reading from a volume needs READ VOLUME. No list of grants specific to volumes was found.
- **documented**: File-arrival trigger.
  - Requires "READ permission on the storage location and CAN MANAGE permissions on the job". The exact UC privilege is not named.
  - To enable file events you must be the owner of the external location or hold MANAGE on it. Volumes on that location inherit file events.
  - Source: …/jobs/file-arrival-triggers (2026-11-06).
- **documented**: Azure roles the storage credential needs for file events (…/connect/unity-catalog/cloud-storage/manage-external-locations, 2026-11-04).
  - Storage Blob Data Contributor.
  - Storage Queue Data Contributor.
  - Storage Account Contributor, plus **EventGrid Data Contributor** on the resource group, for automatic setup.
  - "Allow trusted Microsoft services" must be enabled.
  - **Conflict**: …/connect/unity-catalog/cloud-storage/external-locations-adls (2026-10-14) names **EventGrid EventSubscription Contributor** instead. Unresolved.

## Q4. Audit

- **documented**: Files API and volume UI operations are logged under `service_name = filesystem`.
  - Events include filesPut (path, receivedSize), filesDelete, filesGet and directories*.
  - Also logged: `generateTemporaryVolumeCredential`, and `cloudStorageMetadata` (listObjects, validateFileEventsPermissions) for Auto Loader and triggers.
  - Source: …/admin/account-settings/audit-logs (2026-11-05).
- **inferred**: Direct writes (route b) do not appear in Databricks audit logs. No page states this outright.
  - Supporting quote: "UC doesn't govern reads and writes performed directly against cloud object storage".
- **documented**: Azure Storage resource logs "aren't collected and stored until you create a diagnostic setting" (https://learn.microsoft.com/en-us/azure/storage/blobs/monitor-blob-storage, 2026-07-15).

## Q5. Network

- **documented**: Files API 3.0 network requirements (Beta).
  - It "requires network connectivity from your network to Azure Databricks and from Azure Databricks to your storage".
  - With front-end Private Link, a second front-end private link is needed "for performance-intensive services".
  - If the storage account is behind a firewall: add it to a Network Security Perimeter (NSP) and allowlist the AzureDatabricksServerless service tag. Serverless network billing applies.
  - Source: …/volumes/files-api; …/security/network/front-end/service-direct-privatelink (2026-11-06).
- **documented**: Workspace ingress controls.
  - IP access lists gate access to workspace APIs. With Private Link they apply only to requests over the internet.
  - Context-based ingress (GA) applies together with IP access lists, and can "Constrain high-value service principals to high-trust networks only".
  - Sources: …/security/network/front-end/ip-access-list (2026-11-04); …/security/network/front-end/context-based-ingress (2026-11-06).
- **documented**: Serverless egress control "manages outbound network connections from your serverless compute resources. For ingress control, see Context-based ingress control." UC external locations are allowed by default. (…/security/network/serverless-network-security/network-policies, 2026-10-23)
- **inferred**: Team 2's egress policy does not gate Team 1's inbound Files API writes; ingress controls, IP access lists and Private Link do.
- **not confirmed**: Whether a restricted network policy affects the hop from Files API 3.0 to storage.
- **documented**: Storage accounts used as external locations "must have a hierarchical namespace". If public access is disabled, "Allow Azure trusted services" must be enabled. (…/connect/unity-catalog/cloud-storage/external-locations-adls)
- **inferred**: For route (b), the writer itself must get through the storage firewall or private endpoint. This is ordinary Azure behaviour, not documented by Databricks.

## Q6. Detection (file-arrival trigger and file events)

- **documented**: Triggers can watch the root of an external location or volume.
  - Auto Loader on a UC volume: directory listing from DBR 13.3+, file events from DBR 14.3+. Classic notifications without file events are unsupported.
  - Sources: file-arrival-triggers; …/ingestion/cloud-object-storage/auto-loader/file-detection-modes (2026-09-11).
- **documented**: Behaviour around writes (file-arrival-triggers; manage-external-locations).
  - "Only new files trigger runs. Overwriting an existing file with a file of the same name does not trigger a run." This matters because the Files API overwrites by default.
  - "adding content to an existing empty file triggers a run".
  - "File events listens for the FlushWithClose event to process a file. Some Azure API usage may not emit this event, which could delay file discovery."
  - Uploading through `Azure.Storage.Blobs` "can cause high latency during file event ingestion".
  - Azure Blob Storage (no HNS) is not supported.
- **documented**: Event Grid on HNS accounts (https://learn.microsoft.com/en-us/azure/event-grid/event-schema-blob-storage, 2025-10-21).
  - BlobCreated fires on CreateFile + FlushWithClose. BlobRenamed fires on RenameFile.
  - "filter the event for the FlushWithClose REST API call" to make sure a file is fully committed.
- **documented**: Classic notification mode supports RenameFile. A provided queue must subscribe to BlobRenamed and DirectoryRenamed. (…/auto-loader/file-notification-mode; manage-external-locations)
- **inferred**: Files API uploads are detected like any new file. Not explicitly documented.
- **inferred**: How managed file events treat a rename is undocumented. Writing under the final name once, or staging outside the watched path and then renaming in, is the safer pattern.
- **AWS/GCP differences (documented)**:
  - File events use SQS/SNS/EventBridge with an IAM policy.
  - Files API 3.0 allowlists the "Databricks serverless OrgPath".
  - On S3, ObjectCreated fires for both put and multipart uploads. On GCS the event is OBJECT_FINALIZE.

## Gaps

- **Conflicts:**
  - Event Grid role name: EventGrid Data Contributor vs EventSubscription Contributor.
  - Volume write grants: with or without READ VOLUME.
- **Not documented:**
  - Which exact UC privilege the trigger's "READ" means.
  - Whether Files API writes emit FlushWithClose or fire triggers.
  - How managed file events treat a rename.
  - The effect of the egress policy on Files API 3.0.
  - Entra tokens on the 3.0 host.
  - An explicit Databricks statement that route (b) writes are absent from Databricks audit logs.
- **Status:** No GA for Files API 2.0 upload (still Public Preview). Files API 3.0 is Beta.
- **Wrong URLs:** Four guessed URLs returned 404; their pages were found under the URLs cited above.
