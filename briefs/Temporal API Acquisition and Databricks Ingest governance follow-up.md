Follow-Up Research Brief: Evaluating Orchestration Alternatives & Governance Boundaries for API Ingestion
To: Author of Temporal API Acquisition and Databricks Ingest

Date: November 8, 2026

Subject: Follow-up research scope on orchestration alternatives (Prefect, Pure Dagster) and governance boundary design across split teams

1. Context & Objectives
The initial research reports evaluated Temporal (Option A) vs. Databricks Jobs (Option B) for API data acquisition and ingestion into Databricks Lakehouse storage.

Subsequent architectural and organizational analysis introduced two key factors that expand the research scope:

1. Organizational/Governance Split: The data platform is operated under a split-ownership model:

   * Team 1 (Domain / Ingest / Data Owner): Owns vendor API handling, business logic, payload semantics, and pipeline code in Databricks (Workspace).

   * Team 2 (Central Data Platform Governance): Governs the core Databricks platform, Unity Catalog (UC) infrastructure, cluster policies, security, and cost guardrails.

2. Alternative Orchestration Patterns: The need to evaluate open-source alternatives to Temporal (specifically Prefect and a Pure Dagster asset model) through the dual lens of data lineage and split-team operational friction.

This brief outlines the follow-up research required to refine the architectural recommendation.

2. Research Questions & Hypotheses
Track 1: Governance & Handoff Boundary Design (Team 1 ↔ Team 2)

* Q1.1: What is the optimal technical contract between Team 1's ingestion compute and Team 2's Unity Catalog environment?

   * Hypothesis: Isolating Team 1’s ingestion state engine (Temporal or Prefect workers) outside Databricks compute—and landing raw payloads into Team 2-governed Unity Catalog Volumes—minimizes platform security risk while preserving Team 1's deployment agility.

* Q1.2: How should permissions, file-arrival triggers, and Auto Loader be configured across team boundaries?

   * Focus: Specific UC volume access controls (`WRITE` for Team 1 worker service principals, `READ`/`MANAGE` for Team 2 Auto Loader jobs), file event configuration, and schema management responsibilities.

Track 2: Open-Source Orchestrator Alternatives (Prefect & Pure Dagster)

* Q2.1: How does Prefect compare to Temporal for Team 1's domain-led API acquisition?

   * Hypothesis: Prefect provides superior Python-native developer ergonomics for Team 1 with lower operational overhead than a Temporal cluster, but may require trade-offs in multi-day stateful polling or extreme event-sourced history handling.

* Q2.2: Can a "Pure Dagster" Software-Defined Asset (SDA) architecture replace the hybrid model?

   * Hypothesis: Defining extraction and transformation as unified Dagster assets delivers end-to-end data lineage across team boundaries, but may struggle with long-running, non-deterministic vendor wait loops compared to Temporal's code-as-workflow paradigm.

3. Required Research Deliverables
Please conduct a targeted pass on the following four scope items and deliver an updated research note:

Scope Item 1: Unity Catalog Handoff & Governance Specification

* Define the recommended Unity Catalog storage hierarchy (External Locations vs. Managed Volumes) for the landing zone.

* Document exact permission sets required for Team 1's API worker service principal vs. Team 2's platform service principal.

* Address schema drift ownership: Which team handles schema evolution (`addNewColumns` vs. `rescue`) in Auto Loader when Team 1 updates vendor API pulls?

Scope Item 2: Prefect vs. Temporal Comparison (Domain Team Lens)

* Compare Prefect (Core/Open-Source) against Temporal specifically for:

   * Paged, non-requeryable API pulls.

   * Long-running vendor jobs (polling loops with backoff).

   * Infrastructure operating effort for a single domain engineering team.

   * Integration with Databricks execution APIs (`databricks-sdk` / `run-now`).

Scope Item 3: Pure Dagster Asset Ingestion Evaluation

* Assess whether Dagster Software-Defined Assets can natively model paged REST pulls and raw byte landing without introducing a secondary orchestrator.

* Map how Dagster asset metadata and sensors bridge the gap between Team 1's extraction assets and Team 2's Databricks transformation pipelines.

* Document any anti-patterns or gaps when using Dagster for multi-hour asynchronous vendor polling.

Scope Item 4: End-to-End Lineage & Observability Strategy

* Compare how each architectural combination (Temporal + Databricks, Prefect + Databricks, Pure Dagster) captures end-to-end data lineage from API source payload down to Delta Lake bronze/silver tables.

4. Methodology & Constraints

* Labels: Continue tagging claims as [D] documented (first-party docs), [R] reported (practitioner case studies), or [I] inferred (analytical conclusions).

* Focus: Prioritize open-source tools and documented API contracts over proprietary enterprise features.

* Constraints: Assume Team 2 enforces strict egress controls and secret management rules inside the central Databricks workspace.

---

## Decisions recorded on 2026-11-08 (user answers to the assistant's scoping questions)

- **Ownership:** Auto Loader and the file-arrival job belong to the data platform and are run and
  governed by Team 2. Auto Loader is a Databricks Runtime component.
- **Cloud:** Azure ADLS Gen2 with hierarchical namespace (HNS) is preferred. The cloud stays open,
  so differences on AWS or GCP should be noted.
- **Scope of this run:**
  - Track 1 (Scope Item 1) in full.
  - The parts of Track 2 that touch the boundary, for Temporal, Prefect and Dagster: whether each
    can write under the landing contract, its documented Databricks integration, and its lineage
    support.
  - Scope Item 4 (lineage).
  - The full Track 2 comparison (Scope Items 2 and 3: paged pulls, long-running jobs, operating
    effort) is deferred to a later run.
- **Lifted exclusion:** this brief lifts the original brief's exclusion of "other orchestrators".
