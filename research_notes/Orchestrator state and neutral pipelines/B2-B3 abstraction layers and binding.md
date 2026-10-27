# B2-B3: In-house abstraction layers over orchestrators, and which features to bind to directly

Research date: 2026-10-27. Grades used: **first-hand** = practitioner report with outcome (full text fetched); **documented** = vendor or project doc, full text fetched, with version/date where shown; **claim-only** = practitioner abstract or README with no outcome reported; **inferred** = my reasoning, labelled. Anything over about 2 years old is flagged **[>2y]**.

Coverage caveat: about 17 tool calls. Several sources named in the brief were **not checked**: Airbnb, Lyft, Shopify, Uber, Zalando, ING/banks, gusty, Ploomber, ZenML, Prefect-to-Dagster moves, Netflix Maestro full text, and Metaflow's Airflow and Databricks plugin details. They appear under Gaps; nothing is assumed about them.

## B2: Practitioner outcomes of orchestrator-neutral layers, DSLs, DAG generators and multi-backend frameworks

### Takeaway
Only one fetched practitioner source reports an outcome from an orchestrator change: Spotify (2022) left Luigi/Flo. That case does not show an abstraction layer surviving the change. It is a regret signal against shipping orchestration logic as an in-container library. Etsy's boundary-layer (a YAML-to-Airflow DSL) is the only fetched first-party case where a layer supported a migration (Oozie to Airflow), and even there the evidence is the project README, not an outcome report. Vendor docs for multi-backend frameworks (Metaflow, Kedro) say outright that non-primary backends get a reduced or untested feature set.

### Cited Findings

**Spotify, Luigi/Flo to Flyte (first-hand, published 2022-03-14, [>2y])**
- Spotify ran about 20,000 batch pipelines daily, defined in 1,000+ repos and owned by 300+ teams. Most were built on two in-house or OSS libraries, Luigi (Python) and Flo (Java). The team decided in 2019 to move away from them. — [Spotify Engineering, "Why We Switched Our Data Orchestration Service", G. Perchais](https://engineering.atspotify.com/2022/3/why-we-switched-our-data-orchestration-service)
- Problems they named with the library approach:
  - The platform team had to build and maintain the same capabilities in two libraries.
  - Upgrades depended on users ("users don't always upgrade to the latest version"), which made it "hard for us, as a platform team, to roll out fixes and new instrumentation".
  - Workflow containers were a black box: task graphs became visible only at runtime, and "a portion of GKE cluster time is spent polling for missing dependencies".
  - Platform automation such as opt-in downstream backfills and event-triggered actions was hard to build without that visibility.
  — [same](https://engineering.atspotify.com/2022/3/why-we-switched-our-data-orchestration-service)
- How it worked: each workflow was packaged with its tasks, libraries and logic into a Docker image, and Styx (the scheduler) started that image on GKE. — [same](https://engineering.atspotify.com/2022/3/why-we-switched-our-data-orchestration-service)
- Target model:
  - orchestration runs in a managed service;
  - task code runs in a platform-controlled environment;
  - users author with a thin SDK the platform distributes.

  The article calls this a move "from the library/tool paradigm to build the orchestration logic into a service". Flyte was chosen partly because its entity model resembles Luigi/Flo ("eases migration"). During the transition, workflows are registered in both Flyte Admin and Styx. — [same](https://engineering.atspotify.com/2022/3/why-we-switched-our-data-orchestration-service)
- Outcome at publication: the migration was **not complete** ("we still need to migrate all the existing ones from Luigi to Flyte"). The article gives no quantitative outcome and promises a follow-up post on mechanics. — [same](https://engineering.atspotify.com/2022/3/why-we-switched-our-data-orchestration-service)
- Lead only, not fetched: Spotify's 2026 "Honk" posts describe coding agents migrating about 1,800 data pipelines and datasets. That may be the end state of this story, but it is unverified. — [Spotify Engineering, Honk Part 4 (2026-04)](https://engineering.atspotify.com/2026/4/background-coding-agents-dataset-migrations-honk-part-4); [The Stack summary](https://www.thestack.technology/how-spotify-used-agents-to-migrate-1-800-data-pipelines-and-save-10-weeks-of-dev-work/)

**Etsy boundary-layer, YAML DSL compiled to Airflow (claim-only from the README; blog post unreachable)**
- What it does:
  - Builds Airflow DAGs from YAML.
  - Adds things Airflow lacks: DAG-scoped managed resources (for example, ephemeral Dataproc clusters), schema-based type checking of operator arguments, before/after operator groups, DAG pruning, and pre-deploy checks for cycles and duplicate task names.
  - Every Etsy DAG is defined in boundary-layer rather than raw Python, and it is "the core of our fully self-service deployment process".
  - "our migration from Oozie to Airflow relied heavily on boundary-layer's included conversion tool".
  - Etsy-specific customizations live in an internal pip plugin, not in the core.

  — [boundary-layer README (raw.githubusercontent, etsy/boundary-layer master)](https://raw.githubusercontent.com/etsy/boundary-layer/master/README.md); repo pointer: [GitHub etsy/boundary-layer](https://github.com/eap/boundary-layer)
- **Unreachable:** the Etsy Code as Craft post returned 403 and archive.org was blocked for the fetch tool. Its date and any outcome detail are not verified. — [Etsy Code as Craft](https://www.etsy.com/codeascraft/boundary-layer-declarative-airflow-workflows)
- Not verified: whether the repo is still maintained or archived. The GitHub API call returned no usable data.
- Note: the layer targets only Airflow. Its conversion tool was a one-off importer from Oozie, not a multi-backend runtime. The README says nothing about whether it survived any later orchestrator change.

**Vinted, Airflow abstraction plus Python code generator (claim-only; talk abstract, PyData Amsterdam 2025-09-26)**
- Vinted has "over 20 decentralized data teams". The abstract presents a "user-friendly abstraction layer built on Apache Airflow, enhanced by a Python code generator" that the speakers say "simplifies upgrades and migrations", removes scheduler complexity, and standardizes development. It promises guidance on "scheduler-agnostic architectures".
- No numbers or outcomes are given, and no transcript or slides were fetched. — [PyData Amsterdam 2025, O. Ligthart & R. Loredo](https://cfp.pydata.org/pydata-amsterdam-2025/speaker/FWEWYJ)

**DAG-authoring abstraction as a vendor-promoted pattern (documented, talk abstract)**
- An Astronomer advocate's Airflow Summit 2026 talk covers "decoupling pipeline logic from authoring". It surveys native Python, DAG Factory (declarative YAML), Blueprint (templates) and AI-assisted authoring. It reports no outcomes. — [Airflow Summit 2026, V. Janz](https://airflowsummit.org/sessions/2026/the-rise-of-abstraction-in-dag-authoring-from-yaml-to-minecraft/)
- dag-factory is maintained by Astronomer. Version requirements differ across PyPI listings and the Astronomer guide (older listing: Airflow 1.10+; a later variant: Airflow 2.9.1+). Exact current versions were not verified. — [Astronomer docs](https://www.astronomer.io/docs/airflow/2.x/dag-factory.md); [PyPI dag-factory 0.11.1](https://pypi.org/project/dag-factory/0.11.1)
- **Unreachable content:** an Airflow Summit 2024 talk, "Streamlining DAG Creation with YAML in Large Organizations". The PDF is image-only and could not be read. A search-engine extract (lead only) says it covers a YAML learning curve, a need for automated operator-to-YAML mapping and a YAML validator, and "machine-generated DAGs" as a challenge. — [slides PDF](https://airflowsummit.org/slides/2024/25-Streamlining-DAG-Creation-with-YAML-in-Large-Organizations.pdf)

**Multi-backend frameworks: what the vendors themselves say (documented)**
- Metaflow production docs (no version or date on the page) list four deployment targets: Argo Workflows, AWS Step Functions, Apache Airflow and Kubeflow. Step Functions has "a more limited feature set". For Airflow and Kubeflow, "the feature set is more limited"; those integrations are positioned as useful mainly when the orchestrator is already deployed. Databricks is not listed as a target on this page. — [Metaflow docs, Scheduling Metaflow Flows](https://docs.metaflow.org/production/scheduling-metaflow-flows/introduction)
- Kedro deploy docs ("stable"; no version number shown, fetched 2026-10-27) list these targets: Airflow, SageMaker, EMR Serverless, Step Functions, Azure, Dagster, Dask, Databricks, Kubeflow, Prefect, Vertex AI, plus Argo Workflows and AWS Batch as "legacy". The legacy pages "have not been tested against recent Kedro releases and we cannot guarantee them". — [Kedro docs, Deploy](https://docs.kedro.org/en/stable/deploy/index.html)
- kedro-airflow README (0.5.x on PyPI):
  - `kedro airflow create` generates a DAG file, which you copy into the Airflow DAGs folder; the Kedro project is then installed in the executor environment.
  - Older limitations: all datasets must be declared in catalog.yml and reachable from workers, and MemoryDataSet and Spark datasets are unsupported. Older READMEs had a `deploy` command that later ones drop.
  - Seen via search summary of the PyPI pages; the individual versions were not cross-checked. — [PyPI kedro-airflow 0.5.1](https://pypi.org/project/kedro-airflow/0.5.1); [PyPI kedro-airflow 0.2.0](https://pypi.org/project/kedro-airflow/0.2.0)
- Apache Hamilton is "an effort undergoing incubation at The Apache Software Foundation". Its integrations page lists Airflow, Dagster, Prefect and Kedro but does not say whether Hamilton runs inside or replaces them. The specific Airflow integration page returned 404. — [Hamilton integrations](https://hamilton.apache.org/integrations/)

**Migration tooling from the target-orchestrator side (documented)**
- Dagster docs (version selector "Latest (1.13.27)", (c) 2026) offer Airlift for incremental Airflow-to-Dagster migration at task or DAG level, with custom proxy operators per DAG.
- A search-engine extract of the Dagster migration guide says that if DAGs are "dynamically generated from a higher-level API or DSL (e.g. yaml), the migration will be more straightforward", and that customized implementations need more investment. The fetched page versions did **not** contain that sentence (the landing page was navigation only), so treat it as a **lead, not verified**. — [Dagster Airflow reference](https://dagster.io/docs/integrations/airflow/reference); [Dagster migrating-to-dagster](https://dagster.io/docs/integrations/airflow/migrating-to-dagster)
- Dagster also markets "declarative YAML-style workflows via Dagster Components". This is vendor marketing; no date on the page. — [Dagster blog, Airflow migration](https://dagster.io/blog/dagster-airflow-migration)

### Options catalogue (synthesis; grade per row)

| Pattern | Mechanism | Requires | Gives / costs | Failure modes and early warning sign | Exit cost toward Databricks |
|---|---|---|---|---|---|
| **Thin wrapper library** (helpers/factories inside the orchestrator's own API) | Shared Python package that emits the orchestrator's native objects (Dagster assets/jobs, Airflow DAGs) from a per-feed spec | Ownership of one package; semver; CI | Gives: removes copy-pasted landing steps cheaply; native UI, backfills and retries kept. Costs: orchestrator types still appear in feed code | Wrapper logic runs inside every feed's image, so platform fixes depend on feed upgrades. Warning sign: version skew across feeds, platform unable to roll out fixes or instrumentation (Spotify, first-hand **[>2y]**). | Inferred: medium. Feed logic in plain functions ports; the wrapper's emit side must be rewritten for Databricks Jobs. |
| **Internal DSL / compiler** (YAML or config, code-generated DAGs; boundary-layer, dag-factory, Vinted generator) | Declarative feed spec, validated, compiled to orchestrator code | Schema plus validator; codegen ownership; docs for the DSL | Gives: self-service, pre-deploy checks, one choke point for a re-target (Etsy used a converter for Oozie to Airflow; claim-only). Costs: YAML learning curve; generated-DAG debugging (2024 slide extract, lead only) | Failure modes: the DSL grows toward a general programming language; features in the DSL that the backend lacks (Etsy added managed resources and pruning). Warning sign (inferred): DSL tickets ask for loops, conditionals or escape hatches into raw Python. | Inferred: low to medium if the spec holds only feed facts (source, schedule, schema, checks). High if it encodes orchestrator semantics such as sensors and trigger rules. |
| **Framework with multiple orchestrator backends** (Kedro, Metaflow, Hamilton, ZenML-style) | Pipelines authored in the framework; plugins compile to or run on orchestrators | Adopting a third-party framework and its release cadence; plugin per target | Gives: the framework owns portability. Costs: non-primary backends get a "more limited feature set" (Metaflow docs); some targets "legacy… cannot guarantee" (Kedro docs) | Warning signs: the plugin you need for the target is listed as legacy, community-only or untested; dataset or runtime restrictions (kedro-airflow: no MemoryDataSet or Spark datasets in older READMEs). | Documented that Kedro lists a Databricks target; Metaflow's fetched page lists none. Not verified: the plugins' feature depth. |
| **No layer: direct binding** (feeds written natively in Dagster; later rewritten in Databricks) | Feed code uses orchestrator APIs directly | Nothing extra | Gives: full native features, no inner framework to maintain. Costs: rewrite per feed at migration; current symptom of feed logic stuck in orchestrator code | Warning sign: business rules, landing steps and DQ copied per feed and living in orchestrator decorators (the context symptoms). | Inferred: high per feed, linear in feed count (12 to 30+). Mitigated if logic moves into plain Python or dbt modules regardless of layer. |

### Inferences
- Inferred: the fetched evidence fits a split rather than a choice of layer. Keep pipeline logic in plain modules (Python, dbt) that do not import the orchestrator, plus a thin, orchestrator-native shell. Spotify's regret was about orchestration logic shipped inside user images. Vendor docs show that multi-backend frameworks lose features on non-primary backends.
- Inferred: "adding a feed = release of an image with all feeds" is the same structural issue Spotify described. Orchestration and platform code are bundled with feed code, so platform changes need feed releases and vice versa.
- Inferred: a declarative feed spec (source, schema, schedule, checks) is easier to re-target than a generic DAG DSL. The spec describes the feed, not the orchestrator.

### Gaps
- No fetched first-hand report of an in-house neutral layer that survived a real orchestrator change (for example, Airflow to Dagster or to Databricks). The Spotify outcome was incomplete at publication.
- Not checked: Airbnb, Lyft, Shopify, Uber, Zalando, ING/bank blogs, gusty, Ploomber, ZenML, Netflix Maestro (only secondary summaries seen; not used), Prefect-to-Dagster retrospectives, and "inner-platform effect" critiques (no direct source found).
- Unreachable: Etsy Code as Craft post (403; archive.org blocked); Airflow Summit 2024 YAML slides (image-only PDF).
- Metaflow-on-Databricks status, kedro-databricks plugin version and maintainer, and Hamilton's runtime relationship to orchestrators: not verified.

## B3: Which orchestrator features to bind to directly vs keep neutral

### Takeaway
Little direct evidence exists. The strongest is first-hand: Spotify found that platform-level features (backfills, event triggers, instrumentation, dependency visibility) need the orchestrator to see the graph, and it moved them into a managed service rather than a library. Vendor docs show portable frameworks dropping orchestrator features on secondary backends. Most rows below are therefore **inferred**.

### Cited Findings
- Spotify: downstream backfills, event-triggered actions and lineage instrumentation were hard without the orchestrator seeing tasks before execution. The platform could not roll out fixes or instrumentation through a library. — [Spotify 2022 [>2y]](https://engineering.atspotify.com/2022/3/why-we-switched-our-data-orchestration-service)
- Metaflow on Step Functions, Airflow and Kubeflow has "a more limited feature set" than on Argo, its Kubernetes-native target. — [Metaflow docs](https://docs.metaflow.org/production/scheduling-metaflow-flows/introduction)
- Kedro's Argo and AWS Batch targets are "legacy… not tested against recent Kedro releases". — [Kedro docs](https://docs.kedro.org/en/stable/deploy/index.html)
- Etsy's DSL re-implemented DAG-scoped managed resources and pre-deploy validation on top of Airflow. This is an example of a layer taking on runtime features (claim-only). — [boundary-layer README](https://raw.githubusercontent.com/etsy/boundary-layer/master/README.md)

### B3 table

| Feature | Bind directly? | Why | Evidence grade |
|---|---|---|---|
| Scheduling UI, run history, launchpad | Bind | Rebuilding a UI costs far more than re-learning a new one at migration | Inferred |
| Backfill machinery | Bind | Needs graph visibility at the orchestrator; Spotify could not offer downstream backfills from a library | First-hand (Spotify) **[>2y]** plus inferred |
| Partition status / materialization tracking | Bind, but keep partition *keys* as plain feed data (dates, vendor file IDs) | Status lives in the orchestrator's store and does not port; the key scheme can | Inferred |
| Run isolation / K8s launching | Bind | Infrastructure-specific; Databricks Jobs has its own compute model, so a neutral launcher duplicates both | Inferred |
| Retries / timeouts | Bind (declare per feed in the spec, map to native) | Cheap to re-map; re-implementing retries in-task hides them from the orchestrator | Inferred |
| Logs, alerting | Bind for transport; keep alert *rules and owners* in the feed spec | Native log capture is free; routing rules are business data | Inferred |
| Lineage graph / asset graph UI | Bind | Same graph-visibility argument as backfills; Spotify lacked lineage unless workflows were instrumented | First-hand (Spotify) partial, plus inferred |
| Asset checks UI | Bind the *display*; keep check *logic* neutral (dbt tests, SQL or Python functions) | Addresses "DQ in several engines": one check definition, surfaced natively | Inferred |
| Sensors / event triggers | Bind (mechanism); keep the trigger *condition* as data | Event plumbing is orchestrator-specific; Spotify wanted event triggers in the service | First-hand (Spotify) partial, plus inferred |
| State the pipeline decides on (watermarks, processed-file ledgers) | Neutral (own table in Postgres or DuckLake) | Must survive a dual-run migration and be read by both orchestrators | Inferred (Track A covers this in depth) |
| Business rules, vendor-shape mapping | Neutral | Must not live in orchestrator code (the context symptom); portable as plain modules or dbt | Inferred |
| IO formats / landing steps | Neutral shared library | Copy-paste is the symptom; no orchestrator feature is lost | Inferred |
| Multi-backend portability via framework plugins | Treat as a risk, not a feature | Docs show reduced or legacy feature sets on secondary backends | Documented (Metaflow, Kedro; no versions on pages) |

### Inferences
- Inferred: binding cost depends on where the line sits. Orchestrator features that need the run graph or runtime (backfills, partition status, launch, UI, lineage) are expensive to rebuild neutrally. Feed facts and decisions (rules, state, formats, check logic) are cheap to keep neutral and expensive to extract later.

### Gaps
- No fetched source quantifies the cost of re-implementing backfill or partition machinery versus migrating it.
- Databricks Jobs feature parity with Dagster (partitions, asset checks, backfills): not fetched in this track. It should come from Databricks docs with version and date, and preview flags need checking.
