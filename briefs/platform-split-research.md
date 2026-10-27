# Research brief: separating pipelines from their orchestrator in a data ingestion platform

## How to use this brief

This brief asks for an **options study**, not a recommendation. For each research question, map the
solutions that real teams and tools use, say what each one costs and when it stops working, and grade
the evidence behind every claim. The choice is made later, by the platform team, against its own code.

The context below is fact: constraints the options have to fit. It deliberately leaves out the team's
current design and its candidate answers. Don't guess at them, and don't let one option become the
frame for the others.

## Context (given)

- **Domain:** a regulated financial institution, asset-management operations. Auditability matters:
  what was received, when, from whom, and what was derived from it must be reconstructable.
- **Platform vs consumers:** a shared data platform serves consumer domains (business applications
  and their own transformations). That split is given and outside this study.
- **Scale:** one small platform team; roughly 30+ external feeds and 5 consumer domains expected, from
  about a dozen feeds and two domains today. The numbers are rough. Options that only pay off at
  large-organisation scale should say so.
- **Feeds:** vendor HTTP APIs, SFTP file drops and scheduled file deliveries, with daily and intraday
  cadences. Every delivery's bytes are kept; re-runs must be idempotent.
- **Stack:** Python; dbt for SQL transformations; Postgres; a DuckLake lakehouse (Postgres catalog,
  object storage); Kubernetes, deployed through GitOps.
- **Orchestration today:** Dagster OSS. All pipelines ship in one image and one code location; each
  run gets its own pod.
- **Orchestration later:** a Databricks environment is being built up and is the likely future home
  for orchestration and compute. Whether storage moves too (for example to Delta / Unity Catalog) is
  open.
- **Migration mode:** feed by feed. For a period, both orchestrators run feeds against the same
  platform, and consumers must not be able to tell which one ran a given feed.
- **Durable workflows:** Temporal is decided as the engine for long-running, stateful business
  workflows, including sagas with compensating steps. Workflows are code owned by domain services; the
  engine is platform infrastructure and owns no business logic. It is expected to matter for ingest
  sources run as services and for domain services. **It is not the data-pipeline orchestrator and is
  not to be evaluated as one.**
- **Repository layout:** today a single monorepo holds the platform code, the pipelines and their
  tests. **This is a premise to challenge, not a constraint** (RQ5).

### Problems observed in the current platform

These are symptoms, stated so that the options can be tested against them. They are not diagnoses.

- Feed logic accumulates in orchestrator-specific code, so much of it can only be tested by running
  the orchestrator.
- The same landing steps are written again for each feed, and a fix to one copy misses the others.
- Shapes specific to one vendor have leaked into the generic lake layer.
- Data-quality checks live in several engines (SQL tests, orchestrator checks, library validators)
  with different outcome semantics.
- Adding a feed means a release of the image that carries every feed.

## Terms

| term | meaning in this brief |
|---|---|
| **ingest source** | acquisition from one external system: the client, credentials, protocol and fetch schedule. May run outside the platform and deliver its results to it. |
| **core** | feed-agnostic platform mechanics: landing, archiving, the lake's layers and schemas, shared checks. |
| **pipeline** (or feed) | one source's steps from delivered bytes to the platform's standardized layer, built from core. |
| **orchestrator** | the machinery that schedules, triggers, runs, retries and observes pipelines. |
| **consumer** | a domain that reads the platform's published layers. Out of scope. |

The questions are about where the lines between these fall and what crosses them. If the evidence
says the terms themselves are cut in the wrong place, say so.

## Research questions

### RQ1: Orchestration capability vs pipelining capability

What does an orchestrator provide (scheduling, event triggers, partitions and backfills, dependency
graph, lineage, data-quality checks, retries, run isolation, observability, a catalog), and which of
those belong to the pipeline definition instead?

- What patterns keep pipeline definitions orchestrator-neutral, and what does each give up: features
  lost to a lowest common denominator, or an in-house abstraction layer the team then has to maintain?
- Where should pipeline logic live so it is testable without running any orchestrator?
- Which orchestrator features are worth binding to directly, because rebuilding them would cost more
  than a later migration?

### RQ2: Orchestrator lifecycle and replacement

- How do teams upgrade the orchestrator, including major versions, without touching pipeline code or
  re-releasing every pipeline?
- How do teams move pipelines from one orchestrator to another feed by feed, with both running at
  once against the same storage? Name real migrations where possible, especially into Databricks.
- Which state is the orchestrator's and has to migrate or be given up: run history, materialisation
  and partition records, check results, schedules and cursors? Which state should never have lived in
  the orchestrator in the first place?

### RQ3: The new-pipeline acceptance test

The target: a developer can **develop, test, gate (CI) and deploy** a new pipeline without changing
core or orchestrator code, only consuming them.

- Which designs meet that, and under what preconditions (declarative definitions, plugin or
  registration mechanisms, templates or factories, separate deploy units)?
- How is such a pipeline tested and gated in isolation, and what still has to be tested against the
  shared platform?
- When a source arrives with a genuinely new shape (a protocol or delivery pattern core does not yet
  support), how does core grow without breaking the target for the pipelines already there?
- How independently can pipelines be deployed, and what does that cost in images, versions and
  compatibility between pipeline and core?

### RQ4: Ingest sources outside the platform

Acquisition (talking to the vendor) may run outside the platform, as a service, and deliver results
to it.

- What handoff contracts exist between an acquisition service and a platform's landing zone (object
  drop plus manifest, event notification, API push, platform pull), and what does each guarantee about
  completeness, ordering, replay and evidence?
- Who owns retries, vendor outages, late or partial deliveries, and the "is everything here?"
  decision: the source or the platform?
- How does this split interact with RQ2 (two orchestrators) and RQ3 (a new pipeline without core
  changes)?
- Where does a durable-workflow engine (see Context) fit on the acquisition side, and what belongs
  there rather than in pipeline orchestration?

### RQ5: Repository, package and deploy-unit topology

Challenge the monorepo. For core, an orchestrator adapter layer, the pipelines and the ingest
sources:

- What are the options (one monorepo, one repo per layer, one repo per source or pipeline, published
  packages with version contracts), and how does each affect RQ2 and RQ3?
- How do platform teams of this size keep compatibility between core versions and many pipelines,
  for example by version pinning, contract tests or a compatibility matrix?
- What breaks first under each option, and at what scale?

### RQ6: Reference list of capabilities

Not a design question. Give a list of the capabilities that ingestion platforms commonly separate,
each marked with the layer it usually sits in (ingest source, core, pipeline, orchestrator) and where
practice disagrees. Examples include transport, delivery declaration, archive, raw load, schema drift,
completeness, quality checks, scheduling, lineage, publication and retention. The team will sort its
own code against this list.

## Out of scope

- The design of consumer domains, and the platform/consumer split itself.
- Temporal or other durable-workflow engines as the pipeline orchestrator.
- A broad orchestrator market comparison. Dagster (today) and Databricks (later) are given; other
  tools are relevant only as sources of precedent for a pattern.
- Organisation design and team topologies beyond what an option directly requires.

## What to deliver

For each of RQ1 to RQ5, a catalogue of options. Each option gives:

- **mechanism:** how it works, concretely enough to sketch.
- **requires:** preconditions in tooling, discipline and team skills.
- **gives / costs:** against the context and the observed problems above.
- **failure modes:** how it typically goes wrong, and the early warning sign.
- **exit cost:** how hard it is to back out of or move on from, especially towards Databricks.
- **evidence:** each claim graded:
  - **first-hand:** a practitioner report or case study with an outcome.
  - **documented:** vendor documentation or a specification, with the product version and date.
  - **inferred:** your reasoning, labelled as such.

Then:

- **Cross-question dependencies:** where choosing one option in one RQ constrains another.
- **RQ6:** the capability list as a table.
- **Open:** what the research could not answer, and what evidence would settle it.

Orchestrator features change quickly. Give versions and dates for Dagster and Databricks features,
and flag anything in preview or not generally available, and anything older than about two years.
**Do not give an overall recommendation or ranking.**
