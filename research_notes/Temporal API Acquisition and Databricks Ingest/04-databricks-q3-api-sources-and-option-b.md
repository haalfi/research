# Track 4: API sources on Databricks (Q3) and Databricks-side facts for Q0 Option B

Method: a verification agent fetched every page below in full from docs.databricks.com on 2026-11-07.
None was unreachable. Dates are the "last updated" dates the pages show.
Labels: **documented** / **reported** / **inferred**.

**Bottom line (inferred from the documented set):** Databricks gives **no explicit recommendation
for REST API sources**, either to land raw files first or to write straight to bronze.
- The one "land first" statement is general ingestion guidance.
- Every documented REST-API path writes records straight to tables: custom connectors, PySpark
  data sources, managed SaaS connectors and Zerobus.

## Q3a. Land raw files first, or write straight to bronze?

- **documented**, from https://docs.databricks.com/aws/en/lakehouse/medallion (2026-10-29):
  - Bronze "Contains and maintains the raw state of the data source in its original formats" and
    "Enables reprocessing and auditing by retaining all historical data."
  - "Databricks recommends storing most fields as string, VARIANT, or binary to protect against
    unexpected schema changes."
  - "Databricks does not recommend writing to silver tables directly from ingestion."
  - The medallion pattern is "a recommended best practice but not a requirement".
  - REST APIs are not among the bronze sources the page lists.
- **documented**, from https://docs.databricks.com/aws/en/lakehouse-architecture/deployment-guide/delta-lake
  (2026-10-29):
  - "Use Unity Catalog volumes for landing raw data before bronze ingestion." This sits in the
    general ingestion best practices.
  - The same list says: "Implement idempotent ingestion to handle retries safely"; "Configure
    retention policies for landing zone data"; "Don't skip bronze layer (always preserve raw data
    as source of truth)".
  - The landing zone is optional: "Pipelines in larger organizations often have an additional
    landing zone".
  - "Custom ingestion pipelines ... using Lakeflow pipelines or notebooks" come with no landing
    requirement.
- **documented**, from https://docs.databricks.com/aws/en/ingestion/overview (2026-11-05):
  - "Databricks recommends starting with the most managed layer".
  - A DIY section covers writing your own connectors.
  - The SQL/Spark ingestion table on /ingestion/ (2026-10-15) has no REST API row.
- **documented**, from https://docs.databricks.com/aws/en/ingestion/custom-connectors (2026-10-22):
  - Lakeflow Connect custom connectors are **Beta**.
  - `read_table` yields records plus the next offset, and output goes straight to destination tables.
- **documented**, from https://docs.databricks.com/aws/en/ingestion/community-connectors (2026-09-11):
  - Community connectors are **Beta** and "not backed by Databricks SLAs".
- **documented**, from https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/ (2026-11-03):
  - Managed connectors retry with exponential backoff and store the cursor position.
  - SaaS connectors call the source from serverless compute. Under a Restricted network policy, the
    source's API domains must be allowlisted.
- **documented**, from https://docs.databricks.com/aws/en/pyspark/datasources (2026-11-04):
  - The PySpark Python Data Source API names "REST APIs" as a target.
  - It needs DBR 15.4 LTS+ or serverless env v2.
  - UC HTTP connection credential injection needs DBR 18.1+, with the token kept as a Databricks
    secret.
  - The page shows no release-stage label.
- **documented**, from https://docs.databricks.com/aws/en/query-federation/http (2026-10-29):
  - UC HTTP connections are **GA** at schema level and **Public Preview** at metastore level.
  - They need DBR 15.4+ and are available only in Model Serving regions.
  - The `http_request` function is **deprecated** and "not for high-volume batch queries".
- **documented**, from https://docs.databricks.com/aws/en/ingestion/zerobus-overview (2026-10-01):
  - Zerobus is push-based and "writes data straight into Unity Catalog Delta tables".
  - "For data already landed as files in cloud storage, use Auto Loader."
  - **inferred**: Zerobus does not help with pulls.
- **inferred**:
  - Writing parsed payloads straight to bronze matches the connector tooling, but works against the
    medallion advice to keep raw fidelity and loose types.
  - Landing raw files (Option B, or Temporal's claim-check bytes) matches the deployment guide.

## Q3b. One file-based path or two paths?

- **documented**, from https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema (2026-11-05):
  - JSON, CSV and XML columns are inferred as strings.
  - `addNewColumns` fails the stream once, and it resumes on restart.
  - `rescue` mode never fails the stream.
  - The rescued-data column records the source file path.
- **documented**, from https://docs.databricks.com/aws/en/ingestion/variant (2026-09-11):
  - `singleVariantColumn` "is robust to most ingestion scenarios".
  - It does no schema evolution and has no rescued-data column.
- **documented**, from the best-practices (2026-10-07) and production (2026-11-05) pages:
  - Capture `_metadata.file_path` and `file_modification_time`.
  - Archive processed files with `cleanSource` MOVE.
  - Never put lifecycle policies on checkpoints.
- **documented**, from https://docs.databricks.com/aws/en/jobs/monitor (2026-11-05):
  - "Databricks retains run history for 60 days".
- **inferred**:
  - One file path gives one replay and audit story, one schema and rescue mechanism, and file-level
    provenance. That matters most for the paged source that cannot answer for a past date.
  - Two paths double the schema-drift, idempotency and alerting designs.
  - A direct path loses the original bytes unless the raw body is stored in a column.
  - Databricks does not compare one path with two anywhere.

## Q0 Option B: retries, timeouts and long waits

- **documented**, from the Jobs API create reference (undated):
  - `max_retries` defaults to 0; -1 means retry indefinitely.
  - `min_retry_interval_millis` defaults to an immediate retry.
  - `retry_on_timeout` defaults to false.
  - `timeout_seconds` defaults to 0, meaning no timeout.
- **documented**, from https://docs.databricks.com/aws/en/jobs/configure-task (2026-11-05):
  - "For most configurations, the default setting does not retry any tasks on task failure."
  - "Serverless jobs auto-optimize retries by default."
  - The timeout applies to each retry.
  - **Conflict:** https://docs.databricks.com/aws/en/jobs/notifications (2026-11-06) says "By default,
    tasks are retried three times".
- **documented**, from https://docs.databricks.com/aws/en/jobs/run-serverless-jobs (2026-11-06):
  - Turn auto-optimization off for jobs "that must be executed at most once, for example, jobs that
    are not idempotent."
  - Standard performance mode has a startup of 4 to 6 minutes.
- **documented**, from https://docs.databricks.com/aws/en/compute/serverless/limitations (2026-11-05):
  - "Serverless compute has a maximum runtime of 7 days. Runs that exceed 7 days are terminated ...
    and are not retried."
- **documented**, from the configure-job page (2026-11-06):
  - Maximum concurrent runs defaults to 1.
  - With queueing on, a run waits up to 48 hours.
- **not documented**: how to wait hours on an external vendor job.
  - **inferred**: either a polling task that holds compute while it waits, or a split into a start
    job and a poll-and-read job.

## Q0 Option B: secrets and egress

- **documented**, from https://docs.databricks.com/aws/en/security/secrets/ (2026-11-06) and its
  unity-catalog-secrets page (2026-11-06):
  - Workspace secret scopes grant permissions per scope.
  - UC secrets grant per secret and audit every read.
  - UC secrets need serverless env 4+ or DBR 17.3 LTS+ for dbutils.
  - UC secrets backed by AWS Secrets Manager are **Beta**.
- **documented**, from the http page:
  - "Tokens are restricted to the host_name specified."
  - Traffic goes through the serverless compute plane.
  - OAuth token requests come from the control plane.
- **documented**, from https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-services/service-credentials (2026-10-27):
  - Service credentials are for cloud services, not generic REST APIs.
- **documented**, from https://docs.databricks.com/aws/en/security/network/serverless-network-security/network-policies (2026-10-23):
  - Serverless egress control requires the **Enterprise tier**.
  - Restricted mode allows only UC locations plus the listed FQDNs, and has a dry-run mode.
- **documented**, from https://docs.databricks.com/aws/en/security/network/classic/ (2026-10-08) and the
  data-exfiltration-protection page (2026-03-31):
  - Classic egress is limited through a customer-managed VPC and a firewall or proxy.
  - These pages give an overview only.

## Q0 Option B: late and missing detection

- **documented**, from https://docs.databricks.com/aws/en/jobs/notifications (2026-11-06):
  - Notifications fire on Start, Success, Failure, a duration threshold and streaming backlog.
  - They go to email, Slack, Teams, PagerDuty or webhooks.
  - Job-level notifications are not sent on task retries.
  - Backlog alerts are not supported for pipeline tasks.
- **documented**, from configure-task and the bundles resources page (2026-11-05):
  - Health rules use `RUN_DURATION_SECONDS` and the STREAMING_BACKLOG_* metrics.
  - Streaming observability is **Public Preview**.
- **documented**, from https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/anomaly-detection/ (2026-11-02):
  - Freshness is predicted per table from commit history, and a late table is marked stale.
  - Completeness is a 24-hour row count.
  - "event freshness is not supported".
  - **inferred**: an explicit "data for date X missing" check has to be custom.

## Gaps

- No Databricks comparison of raw-first against parsed-to-bronze for APIs, or of one path against
  two.
- No documented pattern for waiting hours on a vendor job.
- The docs contradict each other on the task-retry default.
- No maximum runtime found for classic compute.
- No step-by-step guide for classic egress.
- Release stage missing for Databricks-managed UC secrets, core serverless egress control and core
  anomaly detection.
