# Follow-up 2: one correction, two tracks

Same rules as before: options with mechanism, preconditions, trade-offs, failure modes and exit cost;
every claim graded first-hand, documented (with version and date) or inferred; no recommendation.

## Correction to the context: the storage premise was wrong

The original brief described the storage as "Postgres; a DuckLake lakehouse (Postgres catalog,
object storage)". That was inaccurate. The facts:

- **The lake is plain Postgres.** The raw, standardized and curated layers are ordinary Postgres
  tables in one database, built by Python loaders and dbt (dbt-postgres). There is no lakehouse
  table format in use. A DuckLake catalog database is provisioned but nothing reads or writes it.
- **The byte archive is object storage** (Azure Blob): every delivery's bytes, with a manifest
  written last.
- **Operational records already live in Postgres**, in a separate schema: delivery offers (what
  arrived in a drop zone), delivery expectations and a publication calendar, a reconciliation view
  between them, field-presence and file-inventory tables, a run log and dataset assertions for the
  curated layer. What is not stored there today: check-verdict history, operator waivers with an
  actor, discovery cursors, feed ownership, backfill requests.
- **An earlier, still-open decision prefers plain Python ingestion over dlt.** Treat dlt, Singer,
  Meltano and Airbyte as precedent for where state lives, not as candidates the team would adopt.

Every conclusion of the earlier reports that rests on DuckLake no longer holds. In particular:
consumer unawareness (C1–C5), "Databricks joins only as a runner of DuckDB code", the dlt
destination reset, and "UC lineage misses DuckLake tables".

## Track C: Databricks against a Postgres lake

- **C1.** How does Databricks read and write data that stays in Postgres? Cover Lakehouse Federation
  (query federation) to Postgres, Lakeflow Connect for Postgres (CDC ingestion), JDBC from jobs, and
  anything newer. For each: GA or preview status with date, read-only or read-write, pushdown,
  freshness, whether Unity Catalog lineage and governance see the tables, and the cost model.
- **C2.** What network path does Databricks compute need to reach a Postgres server inside a
  private Azure network, for serverless compute and for classic compute? Private Link, network
  connectivity configurations, serverless egress control: GA status, date, and what has to be
  provisioned on each side.
- **C3.** Can Databricks triggers fire on a Postgres change? Table-update and file-arrival triggers
  watch Unity Catalog objects only. What are the documented options: a federated table, a CDC-ingested
  table, a marker file in a volume, or polling? What latency and failure modes does each have?
- **C4.** Re-run the consumer-unawareness question (C1–C5 in the earlier report) with Postgres as
  the shared store. Both orchestrators write the same Postgres tables, and consumers read Postgres
  views. What breaks, and which options from the earlier report still apply?
- **C5.** If storage later moves to Delta or Unity Catalog, what are the documented migration paths
  from Postgres, and how does a period with two stores (Postgres plus Unity Catalog) work for
  consumers?

## Track D: evidence and retention duties for orchestration state

The context is a Swiss regulated asset manager. Which records must it keep, and for how long?

- **D1.** Under Swiss rules (FINMA circulars on operational risks and resilience, outsourcing and
  record-keeping, and the Swiss Code of Obligations retention period), plus EU rules where a Swiss
  asset manager is commonly in scope (MiFID II record-keeping, DORA ICT logging): what retention
  periods and evidence requirements apply to:
  - records of data received from external vendors (what, when, from whom)
  - evidence that a control operated (a data-quality check passed or failed)
  - human overrides of a control (who, when, why, approved by whom)
  - job and run logs of the data platform
- **D2.** Which of these duties is met by keeping operational logs in a vendor tool (an
  orchestrator's run history, for example 60 days), and which needs a record the firm controls?
  Cite the requirement text, not secondary summaries, where possible.
- **D3.** Mark clearly what needs legal or compliance confirmation. This track informs a design and
  is not legal advice.
