# Research brief: API data acquisition on Temporal, file-arrival ingest on Databricks

## Goal

Test the assumptions behind a proposed ingestion architecture against first-hand documentation and
published practice. For each assumption, give a verdict (holds / holds if … / fails) and say what it
changes. Do not redesign the architecture.

## Context

- **Temporal** is the organisation's orchestrator for API integration. Using it for data acquisition
  is the proposal under test.
- **Databricks** is the target platform. Its proposed ingest works like this:
  - Files arrive with a contract in a landing zone.
  - A file-arrival-triggered job runs Auto Loader into bronze.
  - For APIs, the leaning is a scheduled Databricks job that writes parsed payloads straight to
    bronze.
- **Today:** Dagster runs Python ingestion. Each feed archives the raw response bytes first, then
  writes a manifest last. Each feed has cheap pre-checks before it calls a source, and its own retry
  policy.
- **Source types:**
  - plain REST pulls;
  - a paged REST pull that cannot answer for a past date;
  - a long-running vendor job (start it, wait hours, read the result);
  - SFTP and blob-storage file drops.
- **Proposal:**
  - Temporal workflows fetch from the APIs and write the bytes and a manifest as files into the landing
    zone, using a claim check.
  - From there, every source takes the same single file path into Databricks.
  - Until Databricks ingest exists, Dagster reads the manifest and a ledger row instead.

## Questions

**Q0. Temporal or Databricks for the API pulls?**
- Option A: a Temporal workflow writes the files into the landing zone.
- Option B: a Databricks job writes the raw payloads as files to a volume, then Auto Loader picks them
  up.

Compare them per source type on:
- retries;
- secrets and egress;
- operating effort for a small team;
- late and missing detection.

Say when each one wins.

**Q1. Temporal for bulk acquisition.**
- What are the current payload and history limits?
- Is a claim check the documented pattern?
- How are long-running external jobs modelled, and how are paged pulls with an unknown page count?
- How are non-retryable errors expressed?
- Is there evidence of Temporal used for data ingestion?

**Q2. File-arrival triggers and Auto Loader.**
- What do file-arrival triggers require of the storage?
- How can already processed files be replayed without resetting the checkpoint?
- Does triggering on a manifest written last fit?

**Q3. API sources on Databricks.**
- What does Databricks currently recommend: landing files first, or writing straight to bronze?
- What are the trade-offs of one file-based ingest path against two paths?

**Q4. Handoffs.**
- What are the documented Temporal → Databricks patterns, for example a job run-now call or a
  file-arrival trigger?
- What are the documented Temporal → Dagster patterns for an interim period?

## Bring back

- For each answer: sources with links and dates, each claim labelled documented, reported or
  inferred.
- A Q0 verdict.
- A table of the assumptions with their verdicts.
- Where first-hand evidence is missing, say so rather than filling the gap.

## Out of scope

- Whether to run Temporal or Databricks at all.
- Other orchestrators.
- Compliance retention.
