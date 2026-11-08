# Governance track 2: Who owns the schema, and how the two teams' controls fit together

## Method

A verification agent read full pages from learn.microsoft.com/azure/databricks on 2026-11-08 (HTTP 200).
It compared the matching AWS and GCP pages for egress, secrets and the Auto Loader schema.
Dates are each page's ms.date. Labels: **documented** / **inferred**.
`…` = https://learn.microsoft.com/en-us/azure/databricks.

Renamed features (documented):
- "Declarative Automation Bundles (formerly known as Databricks Asset Bundles)" (…/dev-tools/bundles/faqs, 2026-11-05).
- "Serverless usage policies" (page at /admin/usage/budget-policies, **Public Preview**).

## Q1. How Auto Loader handles schema

Source: …/ingestion/cloud-object-storage/auto-loader/schema (2026-11-05), unless noted. The AWS and GCP pages are identical.

### Where the schema is stored

- **documented**: `cloudFiles.schemaLocation` turns on inference and evolution. The schema is stored in `_schemas` under that path.
- **documented**: Store the checkpoint "with the stream's output, not its source data… such as a dedicated Unity Catalog volume" (…/auto-loader/best-practices, 2026-10-07).
- **documented**: In Lakeflow pipelines, Databricks manages the schema location. The event log location doubles as the schema location (…/ldp/monitor-event-logs, 2026-11-03).
- **inferred**: Whoever can write the schemaLocation path or manage the job controls the stored schema. If Team 2 owns the job and the checkpoint volume, Team 2 controls the schema.
- **documented**: To roll back a bad schema change, "Contact Databricks support for help." (…/auto-loader/faq, 2026-10-22)

### Schema hints

- **documented**: `cloudFiles.schemaHints` is an inline SQL-DDL string. It can add columns, and it is ignored if a full schema is provided.
- **documented**: The options reference has no option for a schema-hints file (…/spark/api-options, 2026-11-05).

### Evolution modes

| Mode | Documented behaviour |
|---|---|
| `addNewColumns` (default when no schema is given) | "Stream fails with an UnknownFieldException after Auto Loader adds the new columns … Restarting the stream resumes processing". Existing column types do not change. Databricks recommends Jobs auto-restart. |
| `addNewColumnsWithTypeWidening` | **Public Preview**, DBR 16.4+. Needs `delta.enableTypeWidening`. Type changes it cannot widen go to rescued data. |
| `rescue` | "never evolves the schema and the stream does not fail … records all new columns in the rescued data column." |
| `failOnNewColumns` | "Stream fails and does not restart unless you update the provided schema or remove the offending data file." Best practices: "Strict schema contract required → failOnNewColumns". |
| `none` (default when a schema is given) | New columns are ignored silently and not rescued unless `rescuedDataColumn` is set. |

- **documented**: The docs conflict on restarts. The concept page says "Fail with a manual restart required" (…/data-engineering/schema-evolution, 2026-11-06), while the schema page recommends auto-restart.
- **documented**: The options page lists the modes without type widening.

### Rescued data, type inference, VARIANT

- **documented**: `_rescued_data` is added on inference. It holds unparsed fields plus the source file path.
- **documented**: `inferColumnTypes` defaults to false, so JSON, CSV and XML columns become strings.
- **documented**: VARIANT / `singleVariantColumn`: "no schema evolution occurs during ingestion and rescuedDataColumn is not supported".
  - Requires DBR 15.3+ for JSON and 16.4+ for XML and CSV. Records are capped at 16 MB.
  - Source: …/ingestion/variant, 2026-09-11.
- **documented**: Best practices: "Arbitrary or unpredictable schema → Ingest as Variant type".

### Restarts in pipelines and streaming jobs

- **documented**: Streaming tables in Lakeflow pipelines handle new columns by default: "The query automatically restarts to resolve the schema mismatch." (schema-evolution)
  - Pipeline updates started from Jobs or the API retry automatically for "specific recoverable errors" (…/ldp/updates, 2026-09-11).
  - **inferred**: That this covers Auto Loader's UnknownFieldException is not stated.
- **documented**: For streaming jobs, "Some capabilities, including schema evolution, require that Structured Streaming workloads retry automatically."
  - In multi-task continuous jobs, "The failed stream can stay down while the job appears healthy."
  - Source: …/structured-streaming/production, 2026-11-05.

### Detecting drift

- **documented**: Changes in `_schemas` "indicate that schema evolution has occurred. You can poll this directory from a separate monitoring job." A restart alone is not proof of drift. (…/auto-loader/observability, 2026-09-11)
- **inferred**: Under `addNewColumns`, added columns are not rescued. A `_rescued_data IS NULL` check catches type and case mismatches, not added columns. Added columns show up as changes in `_schemas` plus a failed or retried run.

## Q2. Data contracts and expectations

- **documented**: Expectations have three actions:
  - warn (the default);
  - `ON VIOLATION DROP ROW`;
  - `ON VIOLATION FAIL UPDATE` ("Manual intervention is required").

  They cannot call external services or reference other tables. Source: …/ldp/expectations (2026-10-26).
- **documented**: Bronze guard: "verify that _rescued_data and _corrupt_record are NULL … Non-NULL values signal schema drift". (best-practices)
- **documented**: A central expectation repository: "Store expectation definitions separately from pipeline logic… using a Delta table or dictionary". "Dynamically loading expectations from a file is not supported in SQL." (…/ldp/expectation-patterns, 2026-10-26)
  - **inferred**: Team 1 could own the rules table and Team 2's pipeline could read it. The docs do not frame this as cross-team.
- **documented**: Comments on UC objects.
  - Editing a catalog, schema or volume comment needs owner or MANAGE.
  - Anyone with BROWSE can read comments.
  - Source: …/comments/ (2026-11-06).
- **documented**: Governed tags are account-level tags with set keys and values and controlled assigners (…/database-objects/tags, 2026-10-26).
- **documented**: Anomaly detection checks freshness and completeness, not schema. It needs MANAGE on the schema or catalog. Results go to `system.data_quality_monitoring.table_results`.
  - Source: …/data-quality-monitoring/anomaly-detection/, 2026-11-02.
- **documented (absence)**: No page in the Azure Databricks TOC (6,492 entries) covers a "data contract".

## Q3. Cross-team operating model

- **documented**: Governance models are centralised, decentralised, federated and hybrid. "Start with federated governance for most organizations (balances control and agility)."
  - Domain-based catalogs suit data mesh, but "Use environment-based catalogs as the default for most organizations".
  - Hub and spoke: "Spoke catalogs: Contain domain-specific data owned and managed by business units"; "Use volumes to access landing, raw, or unstructured data".
  - Source: …/lakehouse-architecture/deployment-guide/unity-catalog, 2026-10-29.
- **documented**: Another page says "Domain-based catalogs (recommended)", so the two pages disagree on the default (…/lakehouse-architecture/data-governance/best-practices, 2026-10-29).
- **documented**: UC best practices (…/data-governance/unity-catalog/best-practices, 2026-10-30):
  - "Use groups to assign ownership"; "Use service principals to run jobs".
  - "create a schema per team"; catalogs follow "environment scope, team, business unit".
  - External volumes are for landing data from external systems.
  - "Grant the ability to create external locations only to administrators"; "Don't grant general READ FILES or WRITE FILES permissions on external locations to end users."
- **documented**: Workspace-catalog binding allows read-only access from a workspace (…/workspace-catalog-binding, 2026-09-11).
  - Workspace strategy: "Do not create separate workspaces for individual teams" (…/deployment-guide/workspace-strategy, 2026-10-29).
- **inferred**: No page gives a RACI for "the platform team runs ingestion of a domain team's files". The brief's split fits the federated and hub-and-spoke models.

## Q4. Team 2 controls over domain code; separating the run identity from code ownership

### Compute and usage policies

- **documented**: Compute policies are an admin tool, enforced on jobs compute right away. They can fix `spark_conf`, `init_scripts` and `cluster_type`.
  - Sources: …/admin/clusters/policies (2026-09-28); …/policy-definition (2026-10-01).
- **documented**: Serverless usage policies attribute spend through tags; they do not cap it. They are **Public Preview** and set up by an admin.

### Serverless egress

- **documented**: Network policies are set at account level and deny by default. Only account admins manage them, and they need the Premium tier.
  - At most 100 FQDNs can be allowlisted.
  - "Implicit allowlisting for Unity Catalog connections is deprecated."
  - Denials are logged to `system.access.outbound_network`, and a dry-run mode exists.
  - Sources: …/network-policies (2026-10-23); …/manage-network-policies (2026-11-05). Blocked destinations are Public Preview.
- **inferred**: Egress policy affects Team 1's vendor calls only if that code runs on Databricks serverless. Classic compute egress (VNet/NSG) was not researched.

### Secrets and connections

- **documented**: Workspace secret scopes have scope-level ACLs only. UC secrets support READ SECRET / REFERENCE SECRET grants.
  - UC secrets need serverless env 4+ or DBR 17.3 LTS+. Azure Key Vault-backed UC secrets are **Beta**.
  - "Create a schema for each application, environment, or team, and grant CREATE SECRET privileges on the schema".
  - Sources: …/security/secrets/ and …/secrets/best-practices (2026-11-06).
- **documented**: UC HTTP connections are governed by USE CONNECTION and route through serverless. Schema-level connections are GA; metastore-level ones are Public Preview. (…/query-federation/http, 2026-10-29)

### Run identity vs code ownership

- **documented**: Run-as is separate from the owner: "Databricks recommends changing the Run as user to a service principal". It can also be an account group.
  - The page contradicts itself on groups as owners.
  - Source: …/jobs/privileges, 2026-11-05.
- **documented**: Jobs can run code from a remote Git repo pinned to a branch, tag or commit. Every run records the SHA, and "All tasks in a job must reference the same commit". Git folders are for development only. (…/jobs/git, 2026-11-05)
  - **inferred**: Team 1 can own the repo while Team 2 owns the job and its run-as service principal.
- **documented**: Bundles can separate the deploy identity from the run identity, for jobs and pipelines only. "Non-admins can only set this field to their own email." Deploy to an immutable, read-only folder.
  - Sources: …/dev-tools/bundles/run-as (2026-10-07); …/bundles/permissions (2026-09-11).
- **documented**: Pipeline run-as can be changed (…/ldp/privileges, 2026-10-01). It conflicts with "A pipeline runs updates with its owner's credentials" (ldp/monitor-event-logs).

## Q5. Who receives failure signals

### Job notifications

- **documented**: Notifications need CAN MANAGE or IS OWNER on the job.
  - Job-level notifications are not sent on task retries.
  - Each event type allows at most 3 system destinations.
  - Source: …/jobs/notifications, 2026-11-06.
- **documented**: Only workspace admins create system destinations, which are then "available to all users" (…/admin/workspace-settings/notification-destinations, 2026-10-15).
- **documented**: CAN VIEW "Can view job run results, including details, history, and status." (jobs/privileges)
- **inferred**: Team 2, with CAN MANAGE, adds Team 1's destination. Team 1, with CAN VIEW, cannot add it.

### File-arrival triggers

- **documented**: "To be notified if a file arrival trigger fails to evaluate, configure email or system destination notifications on job failure." Detection on Azure relies on FlushWithClose, and overwrites do not trigger runs.
  - Source: …/jobs/file-arrival-triggers, 2026-11-06.

### System tables

- **documented**: `system.lakeflow.job_run_timeline` and `job_task_run_timeline` hold `result_state` and `termination_code`.
  - They are regional, typically lag by up to about an hour, and are retained for 395 days.
  - An admin grants USE CATALOG, USE SCHEMA and SELECT.
  - Sources: …/admin/system-tables/jobs (2026-11-06); …/admin/system-tables/ (2026-11-04).
- **inferred**: Granting SELECT to Team 1 exposes every job in the region. A Team 2 view filtered by job_id is the obvious fix, but it is undocumented.

### Pipeline event log and alerts

- **documented**: "By default, only the pipeline's run-as user can query the event log table". Share it through a view (ldp/monitor-event-logs).
  - CAN VIEW lets someone open a pipeline. Driver logs are visible only to the owner and admins by default.
- **documented**: Auto Loader alerting: "Use Databricks SQL alerts or pipeline notifications to detect problems". (…/auto-loader/observability)

## Gaps

- No page states the pipeline restarts on Auto Loader's UnknownFieldException.
- The docs conflict on manual vs automatic restart.
- No documented schema-hints file or data-contract feature.
- No ownership rule for `_schemas` beyond normal path privileges.
- No cross-team RACI.
- No pattern for row-level access to system tables.
- No status label is shown for:
  - Databricks-managed UC secrets
  - run-as group
  - core data quality monitoring
  - base egress control
- Classic egress was not researched.
- Only three pages per cloud were compared against AWS and GCP.
