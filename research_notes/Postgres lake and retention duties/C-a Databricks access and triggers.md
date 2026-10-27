# C-a Databricks (Azure) access to Postgres-resident data, and triggers on Postgres change

Scope: how Azure Databricks reads and writes data that stays in an ordinary Postgres database (the lake is plain Postgres in a private Azure network), and whether Databricks job triggers can fire on a Postgres change. Today is 2026-10-27.

Method and grading:
- **[doc]** = vendor documentation, full page fetched by curl from learn.microsoft.com, with the page's visible "Last updated on" date. Raw copies are in the scratchpad at /tmp/claude-0/-home-user-research/4186d93d-8167-5da8-8671-71d874b0981f/scratchpad/ca-dbx/.
- **[rn]** = Azure Databricks release notes, full monthly pages for 2025-11 through 2026-10, fetched.
- **[inf]** = my inference, labelled as such.
- **[first-hand]** = practitioner report with an outcome. **I found none.** One search turned up only vendor docs plus a DZone tutorial (dzone.com/articles/lakeflow-connect-postgresql-integration-tutorial), and that page returned 403, so it is unreachable and was not used.
- Date conflict: the brief says the table-update trigger page was updated 2026-10-02. The page I fetched shows "Last updated on 2026-10-05", and its metadata says updated_at 2026-10-06. Only these later dates were seen. The file-arrival page shows 2026-10-07, which matches the brief.
- Pricing page (databricks.com/product/pricing/lakeflow-connect): fetched, but the price table is rendered by JavaScript and no DBU rates could be extracted. **Unreachable for rates.**

## C1: How Databricks reads and writes Postgres-resident data (options catalogue)

### Takeaway
Six Databricks mechanisms touch an external Postgres. Two are read-only:
- Lakehouse Federation, also called query federation (GA).
- Lakeflow Connect, as the CDC connector (Public Preview, by enrolment) or the query-based connector (GA 2026-05-29). Both copy into UC streaming tables.

Three can write:
- JDBC with a Unity Catalog JDBC connection (GA 2026-10-02 on DBR 19+, serverless, SQL warehouse 2025.40+).
- Plain `spark.read/write.jdbc` with no UC object; its doc page is marked "legacy … not officially endorsed".
- psycopg from job code; no Databricks doc, so this is inference.

The sixth is Lakebase. It is a *Databricks-managed* Postgres, separate from the existing server. Its synced tables (GA) do reverse ETL from UC Delta tables *into Lakebase*, and its Change Data Feed (Public Preview) does Lakebase to Delta. Neither targets an existing Azure Database for PostgreSQL server. UC governance is strongest for foreign catalogs and ingested streaming tables, coarse (connection level only) for UC JDBC connections, and absent for raw JDBC and psycopg.

### Cited Findings

**Option 1: Lakehouse Federation, query federation to PostgreSQL** (GA; no preview label on the page)
- Mechanism and requires:
  - A UC *connection* (`CREATE CONNECTION … TYPE postgresql`, with host, port, user, password; secrets are recommended) and a *foreign catalog* (`CREATE FOREIGN CATALOG … USING CONNECTION … OPTIONS (database '…')`) that mirrors one Postgres database.
  - Compute must be DBR 13.3 LTS+ in Standard or Dedicated access mode, or a Pro or serverless SQL warehouse at 2023.40+.
  - Creating these needs the CREATE CONNECTION privilege, and CREATE CATALOG plus CREATE FOREIGN CATALOG on the connection.
  - TLS is always on. The optional `userProvidedServerCertificate` setting verifies a private-CA certificate, and sslmode can be verify-full or verify-ca.
  - Source: [doc] [Run federated queries on PostgreSQL, updated 2026-10-06](https://learn.microsoft.com/en-us/azure/databricks/query-federation/postgresql)
- Pushdown:
  - Pushed down on all compute: filters, projections, limit, offset, aggregates, arithmetic, boolean and bitwise operators, sort with limit, and TABLESAMPLE.
  - Date, math and string functions are pushed down only partially (in filter expressions).
  - **Join pushdown is Public Preview** (DBR 17.2+ or SQL warehouse, enabled by a Previews toggle). **Window functions are not pushed down.**
  - Source: [doc] [same page, 2026-10-06](https://learn.microsoft.com/en-us/azure/databricks/query-federation/postgresql)
- Type mapping caveats: timestamps map to TimestampType unless `preferTimestampNTZ=true`, json/jsonb/money become StringType, and "limited array types are supported." — [doc] [same page](https://learn.microsoft.com/en-us/azure/databricks/query-federation/postgresql)
- Read or write: **"Not supported (read-only)"** for query federation. The only writable foreign tables are federated legacy Hive metastores. — [doc] [Connect to external databases and catalogs, updated 2026-09-29](https://learn.microsoft.com/en-us/azure/databricks/query-federation/index); [doc] [Lakehouse Federation (database-federation), updated 2026-09-18](https://learn.microsoft.com/en-us/azure/databricks/query-federation/database-federation)
- Freshness: live. Queries run partly in Databricks and partly on the remote database. Databricks positions it for "ad hoc reporting, BI, and proof-of-concept access to operational databases" and recommends Lakeflow Connect "if performance on higher data volumes and lower latency are priorities". — [doc] [index, 2026-09-29](https://learn.microsoft.com/en-us/azure/databricks/query-federation/index)
- Performance limits:
  - Result Cache and Disk Cache are **not** supported for federated queries.
  - Connection throttling follows the Databricks SQL concurrent query limit, and there is "no limit across warehouses per connection".
  - Metadata refresh can slow the first query.
  - Databricks recommends materialized views over foreign tables for loading data.
  - Source: [doc] [database-federation, 2026-09-18](https://learn.microsoft.com/en-us/azure/databricks/query-federation/database-federation)
  - `fetchSize` turns on batched reads, but they are not parallel. Parallel reads use `numPartitions`/`partitionColumn`/`lowerBound`/`upperBound`. Parallel reads do not work on a Databricks view over a federated table; the view must be created in the source database. — [doc] [Performance recommendations, updated 2026-10-23](https://learn.microsoft.com/en-us/azure/databricks/query-federation/performance-recommendations)
- Governance:
  - The foreign catalog gives "table-level access controls". The overview also lists "fine-grained access control, data lineage, and search" as advantages of federation. — [doc] [index](https://learn.microsoft.com/en-us/azure/databricks/query-federation/index); [doc] [database-federation](https://learn.microsoft.com/en-us/azure/databricks/query-federation/database-federation)
  - Table and column comment sync onto foreign tables is **Beta** (2026-06-17). — [rn] [June 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/june)
  - The row filter and column mask page mentions foreign tables only for OpenSharing *recipients* ("can apply row filters and column masks only to shared tables and foreign tables"). It neither confirms nor excludes a provider-side row filter on a federated Postgres table. — [doc] [Row filters and column masks, updated 2026-10-09](https://learn.microsoft.com/en-us/azure/databricks/tables/row-and-column-filters)
- `remote_query` TVF: runs native Postgres SQL through the same connection.
  - It needs USE CONNECTION, or SELECT on a view that wraps it; the view runs with the owner's privileges.
  - Pushdown toggles exist (`pushdown.limit.enabled` and others).
  - Databricks suggests wrapping it in a view to "track lineage".
  - The lineage page says table-valued functions are not captured in lineage.
  - Source: [doc] [remote_query, updated 2026-10-09](https://learn.microsoft.com/en-us/azure/databricks/query-federation/remote-queries); [doc] [Data lineage, updated 2026-10-27](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/data-lineage)
- Networking for a private Postgres:
  - From **classic** compute, use Private Link between the database VNet and the Databricks compute VNet, or allowlist or firewall rules.
  - From **serverless**, the federation networking page names only "Azure Private Link for the SQL Server connector".
  - Source: [doc] [Networking recommendations for Lakehouse Federation, updated 2026-10-13](https://learn.microsoft.com/en-us/azure/databricks/query-federation/networking)
  - Serverless can reach VNet resources through an NCC private endpoint to an Azure Load Balancer plus a Private Link Service. — [doc] [Configure private connectivity to resources in your VNet, updated 2026-10-16](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/pl-to-internal-network)
  - The NCC private endpoint page text I fetched does not name Azure Database for PostgreSQL as a supported resource. — [doc] [Serverless private link, updated 2026-10-16](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-private-link)
- Cost model: DBUs for the querying compute plus remote database CPU and I/O for every query, since there is no cache. — [doc] [database-federation](https://learn.microsoft.com/en-us/azure/databricks/query-federation/database-federation)
- Failure modes and early warning signs [inf]:
  - Heavy or unpushed queries (window functions, joins without the preview) pull rows over JDBC and load the operational Postgres. Warning sign: long-running SELECTs from the Databricks role in `pg_stat_activity`.
  - No cache means repeated BI queries hit Postgres every time.
- Exit cost [inf]: low. The connection and catalog are metadata. Queries that use three-part names (`fcat.schema.table`) need repointing if storage moves to Delta.

**Option 2a: Lakeflow Connect PostgreSQL CDC connector** (**Public Preview**, "reach out to your Databricks account team to enroll")
- Status:
  - Release note 2025-12-16: "fully-managed PostgreSQL connector in Lakeflow Connect is in Public Preview", covering RDS, Aurora, Azure Database for PostgreSQL, Cloud SQL and on-prem. — [rn] [December 2025](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2025/december)
  - Still marked Public Preview on every connector page fetched, with updates 2026-09-11 through 2026-10-09. — [doc] [Source setup, 2026-09-11](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-source-setup); [doc] [Overview, 2026-10-09](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql)
- Supported flavours:
  - PostgreSQL 13+, including "Azure Database for PostgreSQL, Azure virtual machines", and on-prem through ExpressRoute or VPN.
  - Azure Flexible Server: "logical replication is supported on all tiers". Single Server: only General Purpose and Memory Optimized tiers.
  - **On Azure Database for PostgreSQL, `max_slot_wal_keep_size` is read-only and fixed at -1 (infinite).**
  - Source: [doc] [PostgreSQL connector limitations, 2026-09-11](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits)
- Requires on the source:
  - `wal_level=logical` (usually a restart).
  - A replication user with the REPLICATION privilege plus SELECT.
  - REPLICA IDENTITY DEFAULT if the table has a primary key and no TOASTable columns; FULL otherwise, including tables without a primary key.
  - A publication per database, created by the table owner or a superuser (`FOR ALL TABLES` needs superuser).
  - One logical slot per database, `pgoutput` plugin only, plus capacity in `max_replication_slots` and `max_wal_senders`.
  - Username and password auth only.
  - Replication from the primary only.
  - Source: [doc] [Source setup, 2026-09-11](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-source-setup); [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits)
- Architecture and gateway:
  - An **ingestion gateway** extracts snapshot and change data into a UC staging volume. An ingestion pipeline applies it to destination **streaming tables**, with SCD type 1 or SCD type 2 history tracking.
  - **The gateway runs on classic compute and must run continuously** "to prevent WAL bloat". One gateway per pipeline, and gateways cannot be shared.
  - The ingestion pipeline is serverless and scheduled. **Continuous mode is not supported**, and Databricks recommends at least 5 minutes between runs.
  - The gateway needs at least 8 cores, and Databricks recommends the smallest worker nodes.
  - Source: [doc] [Ingest data from PostgreSQL (pipeline), 2026-10-06](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-pipeline); [doc] [FAQ, 2026-09-11](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-faq); [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits)
- Read or write: read-only from Postgres, as a copy into Delta streaming tables. — [doc] [pipeline](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-pipeline)
- Freshness [inf]: the floor is the pipeline schedule (5 minutes or more is recommended) plus serverless start-up. After the first start the gateway may still be extracting, and "it can take a few runs … to have all of the data extracted and applied". — [doc] [FAQ](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-faq)
- Governance [inf]: the destinations are ordinary UC streaming tables, so UC permissions, lineage, and table-update triggers apply to the *copies*. The Postgres originals stay outside UC.
- Cost model:
  - Always-on classic gateway VM DBUs plus VM cost, serverless pipeline DBUs per run, staging volume storage, and Postgres WAL retention and WAL sender load.
  - Docs claim logical replication captures changes "without requiring triggers or significant overhead on the source database".
  - Rates are **unreachable** (pricing page rendered by JavaScript).
  - Source: [doc] [Source setup](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-source-setup); [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits)
- Failure modes and early warning signs:
  - **WAL bloat or disk-full on the source** if the gateway stops or lags. Deleted pipelines do **not** drop their slots.
    - Warning sign: retained WAL per slot and `active=false` in `pg_replication_slots`. Docs give the monitoring SQL. — [doc] [Maintain PostgreSQL ingestion pipelines, 2026-10-09](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-maintenance)
    - On Azure the WAL cap cannot be set (fixed -1), so the guard has to come from monitoring. [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits); the monitoring-only conclusion is [inf].
  - **Failover or primary replacement loses the slot**: a "slot not found" error "requires a full refresh of all tables in the pipeline". — [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits). [inf] This matters for Flexible Server HA failover.
  - **Schema change**: inline DDL tracking is "currently on hold for stabilization". Without it, schema changes force a full refresh of the affected tables. Even with it, type changes, renames, primary key changes, and adding or removing partitions need a full refresh. — [doc] [Source setup](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-source-setup); [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits)
  - **Staging retention**: staging data is deleted after 25 days and removed after 30. A pipeline that has not succeeded for 25 days or more "might result in data gaps". — [doc] [maintenance](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-maintenance)
  - **Type fidelity**:
    - TIMESTAMP without time zone is ingested **as string**, and so are TIME, TIMETZ, MONEY, and user-defined or extension types.
    - NUMERIC with precision above 38 becomes string, and NaN becomes null at precision 38 or less.
    - Two tables with the same name in different schemas cannot share a pipeline.
    - Databricks recommends 250 tables or fewer per pipeline.
    - Source: [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits)
  - A deleted source table does not delete its destination table. — [doc] [limits](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-limits)
- Exit cost [inf]: drop the publication and slot, and revert `wal_level` and replica identity if no longer wanted (a restart). Streaming tables with SCD2 history become owned Delta data, so leaving means either keeping or exporting them.

**Option 2b: Lakeflow Connect query-based connector** (Public Preview 2026-04-15, **GA 2026-05-29**; PostgreSQL is a listed source)
- Status. — [rn] [April 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/april); [rn] [May 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/may)
- Mechanism:
  - Queries the source for rows whose cursor column is above the previous high-water mark. The cursor is a monotonically increasing timestamp or integer.
  - Re-reads a short window below the high-water mark for late commits.
  - No gateway and no staging volume. Scheduled, not continuous.
  - Captures only the latest state, not intermediate states.
  - Soft deletes are tracked via `deletion_condition`; the page says hard-delete tracking is also supported.
  - Can ingest from a UC foreign catalog (`ingest_from_uc_foreign_catalog: true`).
  - Serverless by default, classic also supported.
  - "Can place more load on the source database compared to CDC connectors."
  - Source: [doc] [Query-based connectors overview, updated 2026-09-18](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/query-based-overview)
- Requires: a cursor column on each table. Serverless needs network connectivity to the source, the same issue as federation. — [doc] [same](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/query-based-overview)
- Failure modes and warning signs [inf]:
  - A non-monotonic cursor, such as an `updated_at` set by app clock or rows backfilled with old timestamps, silently skips rows. Warning sign: row-count drift against the source.
  - Source load grows with table size if the cursor is not indexed.

**Option 3: JDBC Unity Catalog connection (read and write)**
- Status:
  - Beta 2025-11-13. — [rn] [November 2025](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2025/november)
  - **GA 2026-10-02** on serverless, DBR 19+ and SQL warehouse 2025.40+, with SSL certificates. OAuth M2M is still Beta. — [rn] [October 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/october)
  - DBR 17.3 LTS through 18 is Public Preview. Serverless SQL warehouses also need the "Enable networking for isolated workloads in Serverless SQL Warehouses" preview. — [doc] [JDBC connection, updated 2026-10-05](https://learn.microsoft.com/en-us/azure/databricks/connect/jdbc-connection)
- Mechanism:
  - A UC securable holds the driver JAR (loaded from a UC volume), the URL, and credentials hidden from users.
  - `externalOptionsAllowList` limits which Spark options users may set; users can never set url or host.
  - Used through the Spark Data Source API (read **and write**) or remote query (read).
- Governance: "governance only at the connection level", not table level. — [doc] [JDBC connection](https://learn.microsoft.com/en-us/azure/databricks/connect/jdbc-connection)
- Pushdown: only the explicit `query` option. "Neither JDBC nor PySpark data sources expose statistics to the query optimizer." — [doc] [JDBC connection](https://learn.microsoft.com/en-us/azure/databricks/connect/jdbc-connection)
- Databricks guidance: recommends federation for supported databases, and names "you need to write to the data source using Spark (query federation doesn't support writes)" as a reason to use JDBC. — [doc] [JDBC connection](https://learn.microsoft.com/en-us/azure/databricks/connect/jdbc-connection)
- Failure modes [inf]:
  - Spark JDBC writes in `append` or `overwrite` mode are not transactional across partitions, so a failed task can leave partial writes.
  - Overwrite drops or truncates the target.
  - Warning signs: duplicate keys after retries, or row counts that do not match the job's input.

**Option 4: Plain `spark.read/write.format("jdbc")` and psycopg in job code**
- The Azure Databricks pages on JDBC and on querying PostgreSQL carry the banner: "The legacy query federation documentation has been retired and might not be updated. The configurations … are not officially endorsed or tested by Databricks. If Lakehouse Federation supports your source database, Databricks recommends using that instead." Both are dated **2025-06-12**, which is over a year old. — [doc] [Query databases using JDBC, 2025-06-12](https://learn.microsoft.com/en-us/azure/databricks/connect/external-systems/jdbc); [doc] [Query PostgreSQL with Azure Databricks, 2025-06-12](https://learn.microsoft.com/en-us/azure/databricks/connect/external-systems/postgresql)
- Reads and writes: `.write.mode("append")` and `.mode("overwrite")` are shown. Reads use one thread by default. The page advises setting `numPartitions` and warns "Be wary of setting this value above 50", because concurrent queries can "overwhelm" application databases. — [doc] [JDBC, 2025-06-12](https://learn.microsoft.com/en-us/azure/databricks/connect/external-systems/jdbc)
- psycopg: no Databricks doc fetched. [inf] It is ordinary Python in a notebook, Python wheel or script task. Postgres sees it as a normal client; there is no Databricks governance, lineage, or audit beyond the job run log.
- Governance [inf]: credentials sit in secrets, and UC sees neither the tables nor lineage. Of the three write paths, this one most resembles today's Dagster loaders and dbt-postgres runs, which already write to the same Postgres.

**Option 5: Lakebase (Databricks-managed Postgres): synced tables (reverse ETL) and Lakebase Change Data Feed**
- What it is: "a fully managed Postgres database integrated into the Databricks platform", with autoscaling, scale-to-zero, branches, read replicas, instant restore and HA. — [doc] [Lakebase Postgres, updated 2026-10-09](https://learn.microsoft.com/en-us/azure/databricks/oltp/index)
- Synced tables:
  - Reverse ETL from UC **managed or external Delta** tables into a **Lakebase** Postgres table, read-only for applications.
  - "Synced tables are generally available"; the LTAP Direct Writes option is **Beta**.
  - Modes: Snapshot, a full copy each time; Triggered, incremental via Change Data Feed (expensive below 5-minute intervals); Continuous, with "seconds of latency", "highest cost" and a 15-second minimum interval.
  - Each sync uses up to 16 Lakebase connections.
  - Source: [doc] [Sync tables, updated 2026-10-22](https://learn.microsoft.com/en-us/azure/databricks/oltp/instances/sync-data/sync-table)
- Lakebase Change Data Feed: **Public Preview**. It captures inserts, updates and deletes on a *Lakebase* table from the WAL into UC managed Delta tables `lb_<table>_history`, needs REPLICA IDENTITY FULL, and is configured per schema. — [doc] [Lakebase CDF, updated 2026-10-05](https://learn.microsoft.com/en-us/azure/databricks/oltp/projects/lakehouse-sync)
- Lakebase Provisioned vs Autoscaling: newly created projects are Autoscaling. The private-preview "Forward ETL" on Provisioned was replaced by CDF. "Lakebase GA pricing applies after the upgrade." — [doc] [Upgrade to Autoscaling, 2026-10-09](https://learn.microsoft.com/en-us/azure/databricks/oltp/upgrade-to-autoscaling)
- Networking and costs:
  - Inbound Private Link to Lakebase Autoscaling went GA 2026-09-28. — [rn] [September 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/september)
  - Egress across regions or to the public internet from Lakebase is charged from 2026-07-22. — [rn] [July 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/july)
- Relevance [inf]: synced tables write only into Lakebase, never into an existing Azure Database for PostgreSQL Flexible Server, and they need a Delta source. They are not a reverse-ETL path into today's lake. Lakebase is relevant only if the Postgres database itself moved into Lakebase. Then CDF (preview) would give a Delta change history and, through it, table-update triggers.
- Exit cost [inf]: Lakebase is Postgres, so `pg_dump` and logical replication out are possible in principle. Branching, CDF, and synced tables are Databricks-specific.

**Federation write support:** none found. Every fetched federation page says read-only, and the only exception is a federated Hive metastore. — [doc] [database-federation, 2026-09-18](https://learn.microsoft.com/en-us/azure/databricks/query-federation/database-federation)

### Inferences
- In-place read/write against the existing Postgres has a split governance trade-off [inf]. Governed reads go through federation (table-level UC grants), with lineage claimed in the overview doc. Writes go only through JDBC paths (UC JDBC connection: connection-level governance; raw JDBC/psycopg: none). So during a Dagster-to-Databricks coexistence, Postgres stays the single writer target and UC sees writes only coarsely.
- [inf] The Postgres sits in a private VNet. Classic (VNet-injected) compute is the documented path for federation and the CDC gateway, and the gateway is always classic anyway. The serverless path to a private Flexible Server would go through an NCC private endpoint. Either Azure Database for PostgreSQL is a supported sub-resource (not confirmed in the fetched text) or it goes via a load balancer plus Private Link Service; both need validating.
- [inf] For CDC on Azure Flexible Server, WAL accumulation is unbounded by configuration (fixed -1). An alert on `pg_replication_slots` retained WAL is therefore the only early warning before the source disk fills. Each HA failover needs a full refresh of the pipeline.
- [inf] CDC copies live in Delta, so the lake would exist twice. Postgres stays the system of record and Delta holds a lagged replica, which matters for which copy reconciliation and assertions run against.

### Gaps
- DBU rates for Lakeflow Connect gateway and pipeline, federation, synced tables and Lakebase: the pricing page is JavaScript-rendered, so rates are unreachable.
- Whether provider-side row filters, column masks, or ABAC policies can be attached to a federated Postgres foreign table: not stated in the fetched pages.
- Whether foreign-table reads show as lineage-graph nodes, and whether system access audit logs record federated query text: the overview claims "data lineage". The lineage page (2026-10-27) does not mention foreign tables, and I did not fetch the audit-log reference.
- Whether Azure Database for PostgreSQL Flexible Server is a supported NCC private endpoint resource for serverless: the supported-resources table was not present in the fetched text.
- Any GA date or GA roadmap for the PostgreSQL CDC connector: none found.
- Practitioner reports with outcomes for any of these options on Azure Postgres: none found. The one tutorial (DZone) returned 403.

## C3: Can Databricks job triggers fire on a Postgres change?

### Takeaway
No native trigger watches an external Postgres. Table-update triggers watch only UC Delta/Iceberg-managed tables, Delta external tables, materialized views, streaming tables, supported views, OpenSharing objects and system tables. The table-update doc says explicitly that views depending on federated tables or non-UC tables are not supported, and that creating such a trigger "still succeed[s], but no job runs are triggered". A foreign table is not in the supported list (that is inference from the list). File-arrival triggers watch UC volumes and external locations only. So a Postgres change can start a job in four ways:
- indirectly, through a CDC-ingested streaming table;
- through a producer-written marker file in ADLS or a volume;
- through an external call to Jobs run-now (from an outbox or LISTEN/NOTIFY relay);
- through polling, on a schedule or as a continuous job.

### Cited Findings
- **Table-update trigger sources** (docs show "Last updated on 2026-10-05", metadata 2026-10-06; the brief's date 2026-10-02 does not match):
  - Supported sources: "Unity Catalog Delta and Iceberg managed tables, Unity Catalog external tables backed by Delta Lake, materialized views, streaming tables, and Unity Catalog views or metric views that depend on supported tables", plus OpenSharing objects and system tables.
  - Views explicitly not supported: those using `read_files`, those that "depend on tables that are not in Unity Catalog", and those that "depend on federated tables". "Creation of triggers for views containing unsupported dependencies still succeed, but no job runs are triggered."
  - Limits: up to 10 tables per trigger, a 1,000-job limit for locations without file events, and two debounce settings ("Minimum time between triggers", "Wait after last change").
  - It passes `{{job.trigger.table_update.updated_tables}}` and per-table commit_timestamp and version parameters.
  - The Run-as principal needs SELECT; otherwise "the trigger fails to evaluate and the job does not run".
  - No extra cost beyond the cloud cost of listing.
  - Source: [doc] [Trigger jobs when source tables are updated, 2026-10-05](https://learn.microsoft.com/en-us/azure/databricks/jobs/trigger-table-update)
- Release-note history:
  - View sources added 2025-11-17. — [rn] [November 2025](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2025/november)
  - OpenSharing and system-table sources: Beta 2026-06-03, then GA 2026-09-30. — [rn] [June 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/june); [rn] [September 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/september)
- **Foreign table as a direct source**: foreign (federated) tables are absent from the supported list, and views over them are explicitly excluded. [inf] A direct foreign-table trigger is therefore not supported. I found no doc sentence that addresses foreign tables directly, and I did not test it.
- **CDC streaming table as trigger source** [doc + inf]:
  - Lakeflow Connect writes to streaming tables, and streaming tables are a supported trigger source. — [doc] [pipeline](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-pipeline); [doc] [trigger-table-update](https://learn.microsoft.com/en-us/azure/databricks/jobs/trigger-table-update)
  - [inf] Latency is the ingestion pipeline schedule (5 minutes or more recommended, continuous not supported) plus serverless start-up plus trigger evaluation and debounce. — [doc] [FAQ](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-faq)
  - Failure modes:
    - The CDC connector is still Public Preview.
    - A full refresh after failover or a schema change rewrites the table and fires a burst of runs [inf].
    - A partial initial load can fire a downstream run on incomplete data. — [doc] [FAQ](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/postgresql-faq)
  - The same holds for a query-based (GA) connector streaming table [inf].
  - A materialized view over a foreign table, which Databricks recommends for loading federated data, is also a supported source, since MVs are listed. [doc] [database-federation](https://learn.microsoft.com/en-us/azure/databricks/query-federation/database-federation); [doc] [trigger-table-update](https://learn.microsoft.com/en-us/azure/databricks/jobs/trigger-table-update). [inf] It fires only when the MV is refreshed, which itself needs a schedule, so this is polling in disguise.
- **File-arrival trigger on a marker file** (updated 2026-10-07):
  - Watches "the root of a Unity Catalog external location or volume, or a subpath", recursively.
  - "Best effort to check for new files every minute."
  - "Only new files trigger runs. Overwriting an existing file with a file of the same name does not trigger a run."
  - Azure: file events listen for FlushWithClose, and "some Azure API usage may not emit this event, which could delay file discovery".
  - Without file events: at most 50 jobs per workspace and at most 10,000 files in the watched path.
  - With file events: no file-count limit, but "triggers can error on time out when there are too many extraneous file updates".
  - A modification outside the rolling retention period is treated as a new file.
  - The path may not contain external tables or managed locations, and no wildcards are allowed.
  - Same debounce options as table-update triggers. No extra cost beyond listing.
  - Source: [doc] [Trigger jobs when new files arrive, 2026-10-07](https://learn.microsoft.com/en-us/azure/databricks/jobs/file-arrival-triggers)
  - [inf] The existing Blob byte archive already writes "a manifest written last" per delivery. If that container or prefix is registered as a UC external location, the manifest is a ready-made marker. Constraints: names must be unique (no overwrite) and FlushWithClose must be emitted by the writer. Warning signs: a manifest present but no run (missing FlushWithClose), and trigger error state (too much churn on the root).
- **Polling on a schedule**: a supported trigger type. — [doc] [Automate jobs with schedules and triggers, updated 2026-10-23](https://learn.microsoft.com/en-us/azure/databricks/jobs/triggers). [inf] The job reads a watermark from the Postgres run log or outbox (via federation or JDBC) and exits cheaply if nothing changed. Latency is the schedule period plus start-up. Cost is a compute start per poll, which matters with classic clusters.
- **Continuous job**:
  - "Only one running instance", and the gap between runs "should be less than 60 seconds".
  - No task dependencies. Retries use exponential backoff instead of retry policies.
  - On serverless, only bounded Structured Streaming triggers such as `AvailableNow` are supported; `ProcessingTime` and `Continuous` are not.
  - Source: [doc] [Run jobs continuously, updated 2026-09-11](https://learn.microsoft.com/en-us/azure/databricks/jobs/continuous)
  - [inf] It can host a long-lived psycopg `LISTEN` loop or an outbox poller, at the cost of always-on compute.
- **Outbox or LISTEN/NOTIFY to Jobs API run-now**:
  - Jobs can be "triggered manually with the Run now button or programmatically using other orchestration tools". — [doc] [triggers, 2026-10-23](https://learn.microsoft.com/en-us/azure/databricks/jobs/triggers)
  - The continuous-jobs page also references the Jobs API run-now request. — [doc] [continuous](https://learn.microsoft.com/en-us/azure/databricks/jobs/continuous)
  - [inf] This needs a relay process outside Databricks (for example a small service on the existing Kubernetes cluster, or Dagster itself during coexistence). The relay either LISTENs or polls an outbox table and calls run-now with a service principal token.
  - [inf] Failure modes: NOTIFY is not durable. Notifications are lost if the listener is disconnected, so an outbox table plus idempotent dispatch is the durable variant. Run-now calls are skipped when max concurrent runs is exceeded ("Runs are skipped when they exceed the configured max concurrency"). — [doc] [triggers](https://learn.microsoft.com/en-us/azure/databricks/jobs/triggers)
  - Warning signs [inf]: outbox rows not marked dispatched, and skipped runs in the job run history.
  - I did not fetch Postgres LISTEN/NOTIFY docs in this track, so their semantics here are inference from general knowledge.

### Inferences
- [inf] Latency options:
  - Run-now from an outbox or relay: seconds, plus job start-up.
  - File arrival: about 1 minute best effort, plus FlushWithClose caveats.
  - Table update on a CDC streaming table: about 5 minutes or more (ingestion schedule) plus evaluation.
  - Schedule polling: the poll period.
  - Continuous job: under 60 seconds between runs, but always on.
  - None of these is a documented latency SLA. The only documented figures are "every minute" (file arrival), "<60 seconds" (continuous gap), and "5 minutes" (CDC pipeline recommendation).
- [inf] Exit cost:
  - Triggers are job-level settings and cheap to change.
  - The CDC-streaming-table route adds the full Lakeflow Connect exit cost (slot, publication, replica identity).
  - The marker-file route reuses the existing Blob manifest convention, so it survives a later Delta/UC move unchanged.
  - The outbox route keeps the event contract inside Postgres, so it is orchestrator-neutral (Dagster sensors could read the same outbox).
- [inf] If storage later moves to Delta/UC, table-update triggers become directly usable on the curated tables themselves, and the Postgres-specific workarounds fall away.

### Gaps
- No doc sentence explicitly says "foreign tables cannot be table-update trigger sources". The conclusion rests on their absence from the supported list and on the explicit exclusion of views over federated tables. Untested.
- No measured latency for table-update trigger evaluation was found; the doc gives none.
- No practitioner reports with outcomes for any trigger pattern against Postgres.
- Postgres LISTEN/NOTIFY durability semantics were not fetched in this track (inference only).
- Jobs API run-now reference page not fetched; its existence is from the triggers and continuous pages.
