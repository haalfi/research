# Alternatives track 3: Fabric Data Factory, Azure Data Factory, Logic Apps

## Method

A verification agent read full first-party Microsoft and Databricks pages on 2026-11-09. Dates are each
page's "Last updated on" value.

Labels: **documented** / **inferred** / **not confirmed**.

Fabric Data Factory (Fabric DF) and Azure Data Factory (ADF) are covered separately.

## 1. Landing responses byte for byte

### REST connector

- **documented (ADF)**: The REST connector supports JSON responses only.
  - "Only response payload in JSON is supported."
  - It sets "Accept: application/json".
  - "Pagination isn't supported for REST API responses where the top-level structure is a JSON array."
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/connector-rest (2026-07-29).
- **documented (ADF)**: "Export JSON response as-is" uses default schema mapping. No guarantee of byte preservation is stated.
- **documented (ADF)**: REST is not on the Binary-format connector list ("Amazon S3, … HTTP, … SFTP"). Also: "you can only copy from Binary dataset to Binary dataset."
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/format-binary (2025-03-31).
- **inferred**: The REST connector therefore writes through a JSON sink and re-serialises the response (https://learn.microsoft.com/en-us/azure/data-factory/format-json). Whether the output is byte-identical is not confirmed.
- **documented (Fabric)**: Same JSON-only wording.
  - Source: https://learn.microsoft.com/en-us/fabric/data-factory/connector-rest-copy-activity (2026-06-16).

### HTTP connector

- **documented (ADF)**: "Copy the HTTP response as-is", and Binary format is supported.
  - Authentication: Anonymous, Basic, Digest, Windows, ClientCertificate, plus authHeaders. No OAuth2 or managed identity.
  - No pagination.
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/connector-http (2026-06-29).
- **documented (Fabric)**: The HTTP connector supports Binary and works as a source only.
  - Authentication: Anonymous or Basic (copy page); the overview lists Basic only.
  - Sources: https://learn.microsoft.com/en-us/fabric/data-factory/connector-http (2026-03-13); …/connector-http-overview (2025-09-16).
- **inferred**: The only documented byte-preserving route is HTTP (Binary) to ADLS Gen2 (Binary), with one request per copy run.

### One file per response

- **documented**: The `fileName` property takes expressions, for example `@concat(...)`, `utcnow()`, `@pipeline().RunId` (Fabric).
  - Sources: https://learn.microsoft.com/en-us/azure/data-factory/connector-azure-data-lake-storage (2025-07-25); …/control-flow-expression-language-functions; https://learn.microsoft.com/en-us/fabric/data-factory/expression-language.
- **inferred**: One file per page needs an Until loop that runs one HTTP-Binary copy per page.
- **not confirmed**: Whether the sink overwrites or fails when the file name already exists.

## 2. Pagination and retries

- **documented (ADF)**: Pagination rules support AbsoluteUrl, QueryParameters, Headers, EndCondition, MaxRequestNumber, SupportRFC5988 and RANGE. The connector stops on HTTP 204 or when a rule returns null.
  - Fabric links to the same rules.
- **documented (ADF)**: "Copy activity supports resume from last failed run when you copy large size of files as-is with binary format between file-based stores … For other scenarios than binary file copy, copy activity rerun starts from the beginning."
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview (2025-09-30).
  - **inferred**: A failed REST pagination therefore restarts at page 1, with no checkpoint per page.
  - **not confirmed**: Whether Fabric behaves the same.
- **documented (ADF)**: Activity policy. Timeout defaults to 12 h; retry defaults to 0; the retry interval defaults to 30 s. A retry reruns the whole activity.
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities (2026-06-17).
- **documented (Fabric)**: Retries can be set from 1 to 1000, with fixed or increasing delays. "Retry conditions (preview)" let a retry apply only to specific errors.
  - Source: https://learn.microsoft.com/en-us/fabric/data-factory/activity-retries (2026-08-14).

## 3. Long waits

### ADF

- **documented (ADF)**: Until has a timeout that defaults to 7 days, with a maximum of 90 days. "If an inner activity fails, the Until activity doesn't stop."
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/control-flow-until-activity (2026-08-04).
  - **Conflict**: The limits page gives a "Maximum timeout for pipeline activity runs" of 7 days.
  - Source: https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits (2026-08-04).
- **documented (ADF)**: Web activity.
  - Synchronous response timeout: at most 10 minutes.
  - With the 202 async pattern it "continues to wait without timing out (upto 7 day)".
  - Responses must be JSON, at most 4 MB.
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/control-flow-web-activity (2026-08-04).
- **documented (ADF)**: Webhook activity calls back via callBackUri. Timeout defaults to 10 min; no maximum is stated.
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/control-flow-webhook-activity.
- **documented (ADF)**: Billing is per activity run and per integration-runtime hour, "prorated by the minute and rounded up". External activities, which include Web, are billed per hour.
  - Source: https://azure.microsoft.com/en-us/pricing/details/data-factory/data-pipeline/.

### Fabric

- **documented (Fabric)**: Two pages conflict on the activity timeout.
  - The limits page says "Maximum timeout for pipeline activity runs | 24 hours" (https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-limitations, 2026-08-09).
  - The activity overview says "maximum is seven days" (https://learn.microsoft.com/en-us/fabric/data-factory/activity-overview).
  - Unresolved; 24 h is the conservative reading.
- **documented (Fabric)**: The Until, Wait, Web and Webhook pages give no timeout values. Webhook "only supports the POST method".
- **documented (Fabric)**: Cost is "0.0056 CU hours for each non-copy activity run". Data movement is 1.5 CU hours per throughput-optimization unit-hour.
  - Source: https://learn.microsoft.com/en-us/fabric/data-factory/pricing-pipelines (2026-06-25).
  - **not confirmed**: Whether waiting time is billed.

## 4. Writing to ADLS Gen2 for Databricks

### Identities and firewalled storage

- **documented (ADF)**: Authentication options: account key, SAS, service principal, or a system- or user-assigned managed identity.
  - With "Allow trusted Microsoft services" on the storage account, a managed identity is required.
  - A managed virtual network uses private endpoints and "protects against data exfiltration".
  - Sources: connector-azure-data-lake-storage; https://learn.microsoft.com/en-us/azure/data-factory/managed-virtual-network-private-endpoint (2026-07-30).
- **documented (Fabric)**: Authentication options: account key, organizational account, SAS, service principal, or workspace identity.
  - Workspace identity is GA. For pipelines it is supported only "for Copy, Lookup, and GetMetadata activities".
  - Sources: https://learn.microsoft.com/en-us/fabric/data-factory/connector-azure-data-lake-storage-gen2-overview; https://learn.microsoft.com/en-us/fabric/security/workspace-identity (2026-09-17).
- **documented (Fabric)**: Trusted workspace access is GA, but "only … in purchased Microsoft Fabric capacities (F SKUs)", and its resource rules can be created only through ARM or PowerShell.
  - Source: https://learn.microsoft.com/en-us/fabric/security/security-trusted-workspace-access (2026-08-13).
- **documented (Fabric)**: Managed virtual networks and private endpoints are listed as "To be determined".
  - Source: https://learn.microsoft.com/en-us/fabric/data-factory/compare-fabric-data-factory-and-azure-data-factory (2026-10-05).

### How the sink writes

- **documented**: The sink settings cover only copyBehavior, blockSizeInMB ("Block Blobs") and metadata. Nothing is said about FlushWithClose, BlobCreated or temp-file-then-rename. Temp-file rename is documented only for an SFTP sink.
- **documented (Databricks)**: "Some Azure API usage may not emit this event" (FlushWithClose). The Blobs library "can cause high latency".
  - Source: https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations (2026-11-04).
- **inferred**: The "Block Blobs" wording hints that the sink uses block uploads through the Blob API.
- **Gap**: Whether ADF or Fabric sink writes emit FlushWithClose. **Must be tested.**

### Governance and UC volumes

- **documented**: Direct ADLS access by managed identities "bypasses Unity Catalog".
  - Source: https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/ (2026-09-11).
- **documented**: Writes into Databricks go only to **tables**, through a cluster: ADF's Azure Databricks Delta Lake connector and Fabric's Azure Databricks connector (Fabric copy authenticates with a PAT only). No UC volume target or Files API connector is documented.
  - Sources: https://learn.microsoft.com/en-us/azure/data-factory/connector-azure-databricks-delta-lake; https://learn.microsoft.com/en-us/fabric/data-factory/connector-azure-databricks-copy-activity.

## 5. OneLake as the landing zone

- **documented**: The Azure storage comparison table marks OneLake "X" for "Supported by Unity Catalog" and "X" for storage events.
  - Source: https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/ (2026-09-11).
- **documented**: Release note of 2026-11-02: "OneLake external locations are now in Public Preview", for use as managed storage.
  - Source: https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/november.
- **documented (Public Preview)**: The OneLake external-location feature page says:
  - "OneLake paths don't support file event notifications."
  - It is intended as managed storage for a catalog.
  - "Do not add users, groups, or other service principals. Anyone in the role can read and write the data directly, outside Unity Catalog governance."
  - It requires DBR 18.1 or later.
  - Source: https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/external-locations-onelake.
- **documented**: OneLake catalog federation is GA since 2026-06-17, and "Data access is read-only."
  - Source: https://learn.microsoft.com/en-us/azure/databricks/query-federation/onelake (2026-11-05).
- **inferred**: OneLake does not fit as the landing zone. It has no file events, it is designed for managed storage, and an external writer would bypass governance. Use ADLS Gen2.
- **not confirmed**: Whether file-arrival triggers or Auto Loader directory listing work on OneLake.

## 6. SFTP

- **documented (ADF)**: The SFTP connector, GA:
  - Authentication: Basic, SshPublicKey, MultiFactor, plus a host-key fingerprint.
  - Binary copy.
  - `deleteFilesAfterCompletion`, per file and for binary copy only.
  - Filtering by `modifiedDatetimeStart` / `modifiedDatetimeEnd`.
  - Per-file resume.
  - "Move after completion" exists only in mapping data flow.
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/connector-sftp (2026-07-29).
- **documented (Fabric)**:
  - The overview lists Basic authentication only.
  - The copy activity offers "Filter by last modified", Binary, and "Upload with temp file".
  - It has no delete-after-completion option; a separate Delete activity is needed.
  - Sources: https://learn.microsoft.com/en-us/fabric/data-factory/connector-sftp-overview (2025-09-16); …/connector-sftp-copy-activity (2026-06-25).
  - **Conflict**: The comparison page claims "All your popular ADF authentication methods work in Fabric".
- **documented (Databricks)**: The Lakeflow Connect SFTP connector is **Public Preview** (release note 2025-11-13; no GA note found).
  - It "extends Auto Loader … exactly-once".
  - Authentication is a PEM private key or a password. Requires DBR 17.3 or later.
  - "cleanSource … is not supported"; "Writing back to an SFTP server is not supported."
  - Source: https://learn.microsoft.com/en-us/azure/databricks/ingestion/sftp (2026-10-06).
  - **inferred**: It runs inside the workspace, so the SFTP host must be on the egress allowlist.

## 7. Secrets, network, cost

- **documented (ADF)**: Key Vault credentials are retrieved "when executing an activity". Self-hosted and managed-VNet integration runtimes are available.
  - Source: https://learn.microsoft.com/en-us/azure/data-factory/store-credentials-in-key-vault.
- **documented (Fabric)**: Key Vault references are configured in Manage Connections. A private vault requires a gateway with line of sight to it.
  - The VNet data gateway needs a P, F or A4+ SKU. With OAuth2 it "doesn't support refreshing tokens automatically".
  - Sources: https://learn.microsoft.com/en-us/fabric/data-factory/azure-key-vault-reference-overview (2026-09-10); https://learn.microsoft.com/en-us/data-integration/vnet/overview (2025-11-10).
- **documented**: Cost meters. ADF bills orchestration activity runs, DIU hours and vCore hours (https://learn.microsoft.com/en-us/azure/data-factory/pricing-concepts). Fabric bills CU rates, and "Microsoft can change consumption rates at any time."

## 8. Detecting late and missing runs

- **documented (ADF)**: Azure Monitor metrics: PipelineFailedRuns, ActivityFailedRuns, TriggerFailedRuns and PipelineElapsedTimeRuns.
  - Tumbling window triggers (GA) can start in the past to backfill, retry 0 by default, support reruns, and can depend on each other.
  - Sources: https://learn.microsoft.com/en-us/azure/data-factory/monitor-metrics-alerts; …/how-to-create-tumbling-window-trigger; …/tumbling-window-trigger-dependency.
- **documented (Fabric)**:
  - "tumbling window is only partially implemented … backfill isn't yet supported."
  - Interval-based schedules are a preview.
  - Alerts come from Outlook or Teams activities, the Monitoring hub alerts tab (preview), and Activator rules on job events.
  - Sources: limitations page; https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs; …/create-alerts-for-pipeline-runs.

## 9. Logic Apps (short)

- **documented**: Limits:
  - Run duration: 90 days for Consumption and Standard stateful runs; 5 minutes for Standard stateless runs.
  - Outbound HTTP timeout: 120 s (Consumption) or 225 s (Standard). The docs say to use async polling or Until for longer work.
  - Until: up to 5,000 iterations, default timeout PT1H.
  - Retries: 4 by default, at most 90.
  - Source: https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config.
- **documented**: HTTP pagination follows nextLink only, and returns the pages "as a single message".
  - Source: https://learn.microsoft.com/en-us/azure/connectors/connectors-native-http.
- **documented**: The Data Lake connector supports Gen1 only. ADLS Gen2 is reached through the Blob connector, with writes of 50 MB or less.
  - Source: https://learn.microsoft.com/en-us/connectors/azuredatalake/.
  - **inferred**: That means the Blob API, so FlushWithClose may not be emitted.

## Verdicts per source type

The comparison is with Temporal. Temporal's side was not re-checked in this track, so every
comparison with it is [I].

| Source type | Fabric DF | ADF | Logic Apps |
|---|---|---|---|
| Plain REST, one response | tie. Byte-exact only through HTTP Binary, which allows Anonymous or Basic auth only. | wins or tie. HTTP Binary with authHeaders and dynamic file names; no OAuth. | tie. FlushWithClose unknown. |
| Paged, cannot be re-queried | **loses**. No per-page write; a rerun starts from the beginning (ADF statement). A hand-built Until loop is limited to 24 h. | **loses**. "rerun starts from the beginning". An Until loop with per-page HTTP Binary copies can be hand-built. | loses or tie. Hand-built loop; built-in pagination returns a single message. |
| Long vendor job | **loses**. 24 h activity cap (conflicting pages); webhook timeout undocumented. | tie for waits under 7 days. Web 202 async, Webhook callback; billed per external-activity hour. | tie. 90-day runs, async polling. |
| SFTP | loses or tie. Basic auth only; no delete-after-copy. | **wins**. Key or MFA auth, binary copy, delete, filters, resume. Databricks' own SFTP connector is still Public Preview. | Not assessed. |
| Blob drops | tie | tie | tie |

**Verdict on H-F: holds only if, and fails in part.**

It **fails** for the paged source that cannot be re-queried, and for OneLake as the landing zone.

It **holds if all five conditions are met**, for SFTP through ADF, single-response REST and blob drops:
1. The HTTP connector writes Binary to ADLS Gen2, not through the REST connector and not to OneLake.
2. File names are unique.
3. A test confirms that the sink emits FlushWithClose.
4. The team accepts that writes from non-Databricks identities bypass Unity Catalog.
5. On Fabric, it runs on an F SKU and accepts that managed virtual networks and private endpoints are still "To be determined".

## Gaps

- **FlushWithClose:** whether the sink emits it, and whether it uses temp-file-then-rename.
- **Sink behaviour:** overwrite versus fail on an existing file name.
- **REST "as-is" output:** whether it is byte-identical, and how multiple pages are laid out.
- **Fabric:** timeouts for Until, Wait, Web and Webhook; the 24 h versus 7-day conflict; resume behaviour; whether waiting time is billed.
- **ADF:**
  - Until's 90-day maximum against the 7-day activity limit;
  - the maximum duration of a pipeline run;
  - the maximum Webhook timeout.
- **OneLake:** whether triggers or Auto Loader directory listing work on it.
- **Databricks:** the GA date of the SFTP connector.
- **Not checked:** the Logic Apps SFTP connector (fetched but not analysed); Temporal's side.
