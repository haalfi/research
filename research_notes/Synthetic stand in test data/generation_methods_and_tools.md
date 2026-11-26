# Generation methods and OSS tools for synthetic relational test data

Research date: 2026-11-26. Evidence labels used throughout: **[documented]** = full text (README, LICENSE, docs page, changelog, paper PDF or PyPI/CRAN metadata) was read by me; **[inferred]** = my reasoning from documented facts; **[vendor marketing]** = a vendor's own feature claims about its product, not independently checked; **[lead only]** = search-result extract, not verified; **[unreachable]** = I tried and could not get the source.
Method notes: release dates come from the PyPI JSON API (`https://pypi.org/pypi/<pkg>/json`, fetched 2026-11-26). Last-commit dates come from a shallow `git clone` of each repo's default branch on 2026-11-26. The GitHub REST API was not available in this session, so I have no star counts or issue activity.

## Q1. Model families: what is fitted inside, and what artefact would leave the protected environment?

### Takeaway
Only one model family can be fitted entirely from aggregates computed inside, with the model built outside: marginal/graphical-model synthesis (Private-PGM/`mbi`, and MST, AIM and MWEM built on it). In that family the artefact that leaves is a set of (noisy) low-order marginal tables plus a domain description. Every other family (copulas, CART/synthpop, Bayesian networks, GAN/VAE/diffusion/transformer) is fitted on real rows. With those, either a fitted model object leaves (a pickle, a JSON description or network weights) or only synthetic rows leave. The fitted model carries parameters learned from the real rows. How much they reveal is for the privacy track.

### Cited Findings
- **Private-PGM / `mbi` (marginal-based inference).** The model is estimated from measurements alone. The quick-start passes `Domain(["age","sex","income"],[10,2,5])` plus "noisy marginal measurements" (`LinearMeasurement(noisy_marginal, ("age","sex"))`) into `estimation.UniversalAcceleratedMethod().estimate(domain, measurements)`, then calls `model.synthetic_data(rows=1000)`. No raw rows go into the estimator. **[documented]** — [mbi README](https://github.com/ryan112358/private-pgm) (repo HEAD 2026-11-25).
  - Other estimators include MirrorDescent, DualAveraging, InteriorGradient and `MixtureOfProductsEstimator` ("scalable, no graphical model"). `ReweightedDatasetEstimator(seed_data=data)` also exists, but it needs seed rows. **[documented]** — same README.
  - The repo ships the mechanisms `mechanisms/mst.py`, `aim.py`, `mwem+pgm.py`, `adaptive_grid.py`, `jam.py` and `gaussian+appgm.py`. **[documented: file listing]** — [private-pgm repo](https://github.com/ryan112358/private-pgm).
  - Licence Apache-2.0. The PyPI package `mbi` went 1.0.0 (2025-08-08) to 2.1.0 (2026-11-06). **[documented]** — [PyPI mbi](https://pypi.org/pypi/mbi/json).
- **SmartNoise Synth (OpenDP).** It packages "MWEM, MST, DP-CTGAN, PATE-CTGAN, AIM". "MWEM and MST require columns to be categorical … you should discretize them before fitting." Licence MIT. Version 1.0.8 was released 2026-04-15, and the last commit (2026-04-21) is "Update to use latest mbi". **[documented]** — [smartnoise-sdk synth README](https://github.com/opendp/smartnoise-sdk), [PyPI](https://pypi.org/pypi/smartnoise-synth/json).
- **DataSynthesizer (Bayesian network).** It has three modes: random, independent-attribute and correlated-attribute (Bayesian network). The input must be a single 1NF table. With DP turned on it "injects noises into the statistics within active domain that are the values presented in the table". **[documented]** — [DataSynthesizer README](https://github.com/DataResponsibly/DataSynthesizer).
  - The artefact between its describe and generate steps is a JSON "dataset description" file (attribute histograms plus Bayesian-network conditionals). **[inferred]** from the notebook names and the tool's describe/generate split. I did not open the notebooks.
  - MIT. Last PyPI release 0.1.13 (2023-10-18). Last commit 2026-07-15 ("fix-default-rng-seed"). PyPI classifier: "Pre-Alpha". **[documented]** — [PyPI](https://pypi.org/pypi/DataSynthesizer/json).
- **synthpop (R, CART/sequential).** "Most synthesising methods … synthesise from conditional distributions where variables … are synthesised one-by-one using sequential modelling … parametric or classification and regression trees models. Methods that are not sequential … are 'sample', 'ipf', and 'catall'." Version 1.9-3 was published 2026-09-10 under GPL-2 | GPL-3. The CRAN page mentions no multi-table or linked-data features. **[documented]** — [CRAN synthpop](https://cran.r-project.org/package=synthpop).
  - The fitted `syn()` object holds the fitted CART/parametric models, which are built from the real rows. Because the trees can hold leaf values from real rows, the usual pattern is to release only the synthetic rows. **[inferred]**
- **Copulas (Gaussian copula; SDV `GaussianCopulaSynthesizer`).** The fitted object exposes `get_parameters()` and `get_learned_distributions()` (per-column marginal family and parameters). The synthesizer can be saved as a pickle. **[documented]** — [SDV GaussianCopula docs](https://docs.sdv.dev/sdv/modeling/single-table-synthesizers/gaussiancopulasynthesizer).
  - So the candidate artefact here is per-column distribution parameters plus a correlation matrix. **[inferred]**
  - The `copulas` package is BUSL-1.1 (0.15.0, 2026-10-30). **[documented]** — [PyPI copulas](https://pypi.org/pypi/copulas/json).
- **Deep models (brief).**
  - CTGAN: BUSL-1.1, 0.13.0, 2026-10-30 — [PyPI](https://pypi.org/pypi/ctgan/json).
  - TabDDPM: last commit 2023-03-09 — [yandex-research/tab-ddpm](https://github.com/yandex-research/tab-ddpm).
  - TabSyn: last commit 2024-06-20 — [amazon-science/tabsyn](https://github.com/amazon-science/tabsyn).
  - REaLTabFormer: GPT-2/Seq2Seq, MIT, 0.2.4 on 2026-01-04 — [PyPI](https://pypi.org/pypi/realtabformer/json).
  - GReaT (`be-great`): MIT, 0.0.14 on 2026-05-12 — [PyPI](https://pypi.org/pypi/be-great/json).
  - Synthcity (benchmark framework with many generators): Apache-2.0. Last release 0.2.12 (2025-05-08), last commit 2025-06-17 — [PyPI](https://pypi.org/pypi/synthcity/json).
  - All of the above dates and licences are **[documented]**. For all of these models the artefact is network weights trained on real rows. Saving the full model is supported explicitly: REaLTabFormer's last commit is "Allow saving of the full model during training (#101)". **[documented: commit message]**
- **MOSTLY AI engine (TabularARGN, autoregressive).** "Train a generative model once … generate synthetic data samples to your needs: up-sample/down-sample, conditionally generate, rebalance categories, impute …, all within your own compute environment". **[documented]** — [mostlyai-engine README](https://github.com/mostly-ai/mostlyai-engine).
  - The SDK's quick start loads a pre-trained generator from a ZIP file (`…/census/census-generator.zip`). The trained generator is therefore a portable file artefact. **[documented]** — [mostlyai README](https://github.com/mostly-ai/mostlyai).
- **NIST CRC.** The CRC data bundle holds de-identified submissions from 2023–2024 (CSV plus JSON metadata) against the NIST ACS Data Excerpts. The 2025 benchmark subset includes sdcMicro SDC, R synthpop, and SmartNoise AIM and MST at several epsilons. This is a ready-made comparison corpus of what these methods' outputs look like on the same data. **[documented]** — [NIST CRC repo README](https://github.com/usnistgov/privacy_collaborative_research_cycle) (last commit 2026-03-19). Citation: Task, Bhagat, Streat, Howarth, *NIST CRC Data and Metrics Archive*, Feb 2025, doi:10.18434/MDS2-3024.

**Artefact-leaving summary [inferred from the documented APIs above]:**

| Family / tool | Fit input | What could leave | Sample outside from released artefact? |
|---|---|---|---|
| Private-PGM / mbi | domain + marginal tables (noisy or not) | marginals + domain; or the estimated graphical model | Yes. The estimate itself can be run outside, because it needs only the marginals |
| MST / AIM / MWEM (mbi, SmartNoise) | real rows → measure marginals inside | the noisy marginals (or fitted model) | Yes, if you split measure (inside) from estimate+sample (outside). The mbi API supports this split; the SmartNoise `fit` API bundles both steps |
| DataSynthesizer | real single table | JSON description (histograms + BN conditionals) | Yes, generation from the description file |
| SDV GaussianCopula | real rows | pickle; or learned marginal params + correlation | Yes (pickle); params are inspectable |
| synthpop CART | real rows | normally synthetic rows only | Technically yes (R object), but it embeds data-derived trees |
| CTGAN/TVAE/TabDDPM/TabSyn/REaLTabFormer/TabularARGN | real rows | weights file / generator ZIP | Yes; weights trained on real rows |
| Rule-based (Faker etc.) | none / hand-written spec | the spec | n/a |

### Inferences
- The protected environment may release only aggregates. That fits a "measure marginals inside → estimate model outside" pipeline (mbi) best, because the released object is the same kind of thing as other permitted aggregates: count tables. **[inferred]**
- Every other learned family would need the model itself approved as a release, or would need the generation to run inside with only the synthetic rows leaving. **[inferred]**
- mbi and MST/AIM need discrete domains. Continuous columns must be binned, and the bin edges are themselves part of the released characterisation. **[inferred]** from the SmartNoise note on discretising.

### Gaps
- The original PrivBayes code was not checked; its maintenance state is unknown.
- I did not open DataSynthesizer's description-file schema or the mbi docs site, so the exact on-disk formats of those artefacts are not verified.
- TabDDPM and TabSyn licences were not checked; only their last-commit dates.

## Q2. Multi-table / relational synthesis: SDV, MOSTLY AI, REaLTabFormer, ClavaDDPM, RCTGAN, IRG, PrivLava

### Takeaway
SDV Community's only multi-table synthesizer is HMA. It is recommended only for about 5 tables at depth 1. HSA, Independent, DayZ, multi-table conditional sampling and composite keys are SDV Enterprise (commercial). SDV has been under the Business Source License 1.1 since version 0.18.0 (2023-01-24).

The MOSTLY AI SDK and engine are Apache-2.0 and support multi-table data locally. The research systems vary in what they ship:
- REaLTabFormer: parent→child, MIT.
- ClavaDDPM: no licence file.
- RCTGAN: stale since 2023.
- IRG: placeholder code only.
- PrivLava/PrivPetal: papers; I found no packaged code.

### Cited Findings
- **SDV licence change.** SDV 0.17.2 (uploaded 2022-12-08) is "MIT license". SDV 0.18.0 (uploaded 2023-01-24) is "BSL-1.1" with the classifier "License :: Free for non-commercial use". 1.0.0 followed on 2023-03-28. **[documented]** — [PyPI sdv 0.17.2](https://pypi.org/pypi/sdv/0.17.2/json), [PyPI sdv 0.18.0](https://pypi.org/pypi/sdv/0.18.0/json).
  - The change is therefore between Dec 2022 and Jan 2023, first shipped in 0.18.0. **[inferred from per-version metadata]**
  - HISTORY.md does not mention the change. **[documented: grep]**
- **SDV BSL terms (LICENSE file, current main).**
  - Licensor: DataCebo, Inc.
  - Additional Use Grant: "You may make use of the Licensed Work … provided that you do not use the Licensed Work … for a Synthetic Data Service". That term is defined as "a commercial offering that allows third parties (other than your employees and contractors) to access the functionality".
  - "Change Date: Change date is four years from release date"; "Change License: MIT License".
  - "The Business Source License … is not an Open Source license."
  - **[documented]** — [SDV LICENSE](https://github.com/sdv-dev/SDV/blob/main/LICENSE).
  - Implication: internal dev/test use by employees and contractors is within the grant. The SDV 0.18.0 release (Jan 2023) would convert to MIT around Jan 2027. **[inferred]**
- **SDV current state.**
  - SDV 2.0.0 was released 2026-10-15. It brought metadata V2, removal of deprecated APIs, an `ordinal` sdtype, range/null info in metadata, and "Add multi table `sample_scale` method".
  - 2.1.0 followed on 2026-10-30 and 2.2.0 on 2026-11-06. A 1.39.0 maintenance release followed on 2026-11-12, and the last commit was 2026-11-16.
  - **[documented]** — [SDV HISTORY.md](https://github.com/sdv-dev/SDV/blob/main/HISTORY.md), [PyPI](https://pypi.org/pypi/sdv/json).
  - Ecosystem licences: RDT (BUSL-1.1, 2.1.0, 2026-10-30), SDGym (BUSL-1.1, 0.17.0, 2026-11-13) and SDMetrics (MIT, 0.33.1, 2026-11-25). **[documented]** — PyPI JSON for [rdt](https://pypi.org/pypi/rdt/json), [sdgym](https://pypi.org/pypi/sdgym/json), [sdmetrics](https://pypi.org/pypi/sdmetrics/json).
- **SDV Community vs Enterprise (compare page).**
  - Community has GaussianCopula, CTGAN, TVAE, CopulaGAN, PAR (sequential) and "HMA multi-table for limited tables (<5)".
  - Enterprise-only items:
    - "HSA multi-table for unlimited tables"
    - "Independent multi-table for unlimited tables"
    - DayZSynthesizer (single and multi-table)
    - better PK/FK auto-detection
    - "Specify composite keys"
  - Enterprise paid bundles:
    - Targeted Sampling: multi-table conditional sampling; extrapolating outside training ranges.
    - CAG: custom constraints and multi-table constraints such as CarryOverColumns, DenormalizedTable, PolymorphicRelationship.
    - AI Connectors: database import and export.
    - XSynthesizers: XGC, SegmentSynthesizer, BootstrapSynthesizer.
    - Differential Privacy: DPGC and related.
  - **[documented; capability claims are vendor marketing]** — [SDV Compare Features](https://docs.sdv.dev/sdv/explore/compare-features).
- **Multi-table synthesizer table (SDV docs).**
  - HMA (Public): "Up to 5 tables, depth of 1"; learns inter-table patterns and cardinality.
  - HSA (Enterprise): "unlimited tables"; "segment-based algorithm"; `default_num_clusters`; the per-table model can be GaussianCopula, CTGAN, TVAE or CopulaGAN.
  - Independent (Enterprise): learns cardinality but not inter-table patterns.
  - DayZ (Enterprise): referential integrity only, no cardinality learning.
  - "Cardinality refers the number of children each parent has."
  - **[documented]** — [SDV multi-table synthesizers](https://docs.sdv.dev/sdv/multi-table-data/modeling/synthesizers), [HMA page](https://docs.sdv.dev/sdv/modeling/multi-table-synthesizers/hmasynthesizer), [HSA page](https://docs.sdv.dev/sdv/modeling/multi-table-synthesizers/hsasynthesizer).
  - HMA "uses hierarchical ML algorithm … classical statistics" and is "optimized for smaller datasets with around 5 tables and 1 level of depth". Each table is configured with GaussianCopula parameters. Trained synthesizers are saved as a Python pickle. **[documented]** — HMA page.
- **SDV metadata for foreign keys.**
  - SDV metadata describes tables, sdtypes, primary keys and relationships.
  - Metadata can be auto-detected from DataFrames in Community. Better PK/FK detection and composite keys are Enterprise only.
  - **[documented]** — compare page. I did not read the metadata JSON schema page in full.
- **DayZSynthesizer (SDV Enterprise).** It needs a Metadata object and no real data. It "creates values and ranges based on … the min/max range of numerical columns and the possible category values in categorical columns". `set_missing_values` sets null proportions, and locales drive PII values. "This feature is only available for licensed, enterprise users." **[documented]** — [DayZ docs](https://docs.sdv.dev/sdv/single-table-data/modeling/synthesizers/dayzsynthesizer).
  - A DataCebo PoC guide says the output has no statistical similarity to real data. **[lead only]** — [SDV Enterprise PoC 1.2](https://docs.sdv.dev/sdv-enterprise/resources/poc-preparation/step-1/1.2-generate-and-test-with-fake-data).
- **MOSTLY AI SDK (`mostlyai`) and engine.**
  - Both are Apache-2.0 (LICENSE files).
  - The SDK first appeared on PyPI 2023-12-29 (0.0.2) and is now 6.2.1 (2026-10-29).
  - The engine first appeared 2025-01-20 (1.0.0) and is now 2.7.4 (2026-10-29). mostlyai-qa is 1.10.11 (2026-10-09).
  - "LOCAL mode trains and generates synthetic data locally on your own compute resources (default)."
  - **[documented]** — [mostlyai README/LICENSE](https://github.com/mostly-ai/mostlyai), [mostlyai-engine](https://github.com/mostly-ai/mostlyai-engine), [PyPI mostlyai](https://pypi.org/pypi/mostlyai/json), [PyPI engine](https://pypi.org/pypi/mostlyai-engine/json).
  - Feature list, **[vendor marketing]**: "Single-table, multi-table, and time-series", "DNN-based match making for graph relations", "Differential Privacy", "Up-sample to any data volumes", "Conditional simulations based on any columns", "Re-balance underrepresented segments", "Rule-adherence via temperature", "Fully permissive open-source license". The engine supports "optionally provide context data", i.e. parent context for sequential child tables.
  - Engine technical paper: arXiv 2501.12012 (linked from the README). Not read.
- **REaLTabFormer relational.**
  - "first creates a parent table using an autoregressive GPT-2 model, then generates the relational dataset conditioned on the parent table using a sequence-to-sequence (Seq2Seq) model". It uses target masking and a Q_δ statistic to detect overfitting.
  - The API requires a shared `join_on` key column. The parent model is fitted without the key and saved to a directory, then a child model is fitted conditioned on it.
  - One parent→child relation per model pair. Multi-level schemas need chaining. **[inferred]**
  - **[documented]** — [REaLTabFormer README](https://github.com/avsolatorio/REaLTabFormer), [arXiv 2302.02041 (2023-02-04)](https://arxiv.org/abs/2302.02041).
- **ClavaDDPM (NeurIPS 2024).**
  - Targets "tens or hundreds of interconnected tables". The stated aims are scalability and "long-range dependencies, such as correlations between attributes spread across different tables".
  - Users supply CSVs with `<name>_id` columns and a `dataset_meta.json` listing FK relationships and a topological `relation_order`.
  - The repo has no LICENSE file at its root (file listing checked), so by default no rights are granted. The last commit was 2024-10-27.
  - **[documented]** — [arXiv 2405.17724 (2024-05-28)](https://arxiv.org/abs/2405.17724), [ClavaDDPM repo](https://github.com/weipang142857/ClavaDDPM).
- **RC-TGAN.** Conditions the child table's GAN on parent rows and is extended to grandparent influence. **[documented]** — [arXiv 2211.07588 (2022-11-14)](https://arxiv.org/abs/2211.07588).
  - The repo's last commit was 2023-07-06. PyPI `rctgan` has a single release, 1.1 (2025-02-12), with metadata "Apache license" but a classifier saying MIT (inconsistent) and the status "1 - Planning". **[documented]** — [RCTGAN repo](https://github.com/croesuslab/RCTGAN), [PyPI](https://pypi.org/pypi/rctgan/json).
- **IRG (Incremental Relational Generator).** "The project is now in commercial usage, so the full code is not disclosed … some functions are filled with placeholders". Last commit 2026-02-18. **[documented]** — [IRG repo](https://github.com/li-jiayu-ljy/irg). It is not usable as an OSS tool. **[inferred]**
- **PrivLava (arXiv 2304.04545, 2023-04-10).** "Synthesizing Relational Data with Foreign Keys under Differential Privacy". It notes that single-relation methods "are unable to model the complex correlations induced by the foreign keys". **[documented: abstract]** — [arXiv](https://arxiv.org/abs/2304.04545).
- **PrivPetal (arXiv 2503.22970, 2025-03-29).** "Relational Data Synthesis via Permutation Relations". It names PrivLava as "the current state of the art", which "generat[es] random join key attributes". It notes that "if we generate random records for each entity independently, the resulting synthetic data usually fail to exhibit realistic relationships". **[documented: abstract]** — [arXiv](https://arxiv.org/abs/2503.22970).
- **synthpop.** No multi-table features on CRAN. **[documented]** — [CRAN](https://cran.r-project.org/package=synthpop).

### Inferences
- How cardinality is preserved varies by method:
  - SDV HMA/HSA/Independent learn children-per-parent counts explicitly. HMA models them with classical statistics in the parent-level model. **[documented that they learn it; mechanism detail inferred]**
  - REaLTabFormer and RC-TGAN generate the child set conditioned on the parent row, so cardinality is implicit in the sequence length or condition. **[inferred]**
  - ClavaDDPM uses cluster latent variables to carry cross-table correlation. **[documented abstract; mechanism detail not read]**
  - PrivLava/PrivPetal model the join-key distribution under DP. **[documented abstract]**
- For a platform with many source tables, SDV Community HMA (≤5 tables, depth 1) is likely too small. **[inferred]**
- The OSS alternatives that scale are:
  - MOSTLY AI SDK/engine: Apache-2.0, active. Multi-table claims are vendor marketing.
  - ClavaDDPM: research code, no licence.
  - A bespoke per-table pipeline (mbi or copula per table, plus an explicit cardinality model, plus FK assignment). **[inferred]**
- Cross-table correlation beyond parent→child (sibling tables, many-to-many, multiple parents) is a stated weak point. PrivPetal's abstract and ClavaDDPM's "long-range dependencies" framing both say so. **[documented as the papers' motivation]**

### Gaps
- MOSTLY AI multi-table limits (number of tables, number of context FKs per table) were not verified in its docs.
- SDV's HMA cardinality model (which distribution family it uses) was not verified in code.
- PrivLava code availability: I found no repo.
- The ClavaDDPM paper body was not read; only the abstract and the README.

## Q3. Rule/schema-driven generators (no real rows): how far can they get with aggregate-only characterisations?

### Takeaway
Mature, permissively licensed rule-based tools can produce multi-table data with consistent keys and chosen distributions from a hand-written or exported spec:
- Faker (MIT)
- Mimesis (MIT)
- Snowfakery (BSD-3)
- Hypothesis (MPL-2.0)
- dbldatagen (Databricks License: not OSI; check terms)

Getsynth/synth is Apache-2.0 but stalled since 2024-09 and still "Public Alpha". plaitpy has been dead since 2018. Benerator CE (GPL-2 with exceptions) is in bug-fix mode, and its maintainers point users to DATAMIMIC.

None of these tools fits a joint distribution from aggregates. They take per-column distributions and explicit relationships. A characterisation made of marginals, cardinalities and a few conditional tables therefore has to be translated into recipe or spec form. Joint structure beyond what the spec spells out is lost. **[inferred]**

### Cited Findings
- **Faker.** MIT. Releases 2010-12-23 to 40.63.0 (2026-11-20). 530 releases. Status "Production/Stable". **[documented]** — [PyPI Faker](https://pypi.org/pypi/faker/json).
- **Mimesis.** MIT. 22.2.0 released 2026-09-23. **[documented]** — [PyPI mimesis](https://pypi.org/pypi/mimesis/json).
- **Snowfakery.**
  - "a tool for generating fake data that has relations between tables". Recipes are written in YAML. Output goes to stdout or "any database accessible to SQLAlchemy"; it can also write to a Salesforce org via CumulusCI.
  - Relationship features: `friends` ("For every Person created, create two Animals") and `reference` (link to the last-created row of a table or nickname).
  - BSD-3 (Salesforce.com). Stable 4.2.1, with 5.0.0.dev1 uploaded 2026-04-27. Last commit 2026-01-09.
  - **[documented]** — [Snowfakery README/docs](https://github.com/SFDO-Tooling/Snowfakery), [PyPI](https://pypi.org/pypi/snowfakery/json).
- **dbldatagen (Databricks Labs).**
  - Generates with Spark "at scale up to billions of rows within minutes using appropriately sized clusters". It produces "repeatable, predictable data supporting … multiple tables, Change Data Capture, merge and join scenarios with consistency between primary and foreign keys".
  - "Ability to specify a distribution for random data generation". "Generate synthetic data generation code from existing schema or data (experimental)" (`DataAnalyzer`).
  - **[documented: vendor README; scale figure is vendor marketing]** — [dbldatagen README](https://github.com/databrickslabs/dbldatagen).
  - Licence: "Databricks License", Copyright 2020. The text defines use in relation to Databricks Services and the MCSA. It is not an OSI licence. **[documented: LICENSE head]**
  - Last PyPI release 0.4.0.post1 (2024-07-26), but commits continue (2026-10-26). **[documented]** — [PyPI](https://pypi.org/pypi/dbldatagen/json).
- **Synth (getsynth).**
  - "declarative data model … database agnostic … can scale to millions of rows". It can import Postgres, MySQL or MongoDB and "automatically works out the relations, distributions and types". Semantic types come from fake-rs.
  - Status: "Public Alpha"; "Public Beta" and "Public" remain unchecked. Apache-2.0. Last commit 2024-09-27.
  - **[documented]** — [synth README](https://github.com/getsynth/synth).
  - Its import infers a model from real data. Used inside, the exported schema file is the artefact that leaves. **[inferred]**
- **Benerator CE (rapiddweller).**
  - "Maintained for bug fixes and security; open source (GPL v2 with exceptions)".
  - The README promotes migration to DATAMIMIC CE (`pip install datamimic_ce`). It says streaming targets are in DATAMIMIC EE.
  - Last commit 2026-08-09; CHANGELOG 4.0.1 covers converter fixes.
  - **[documented; DATAMIMIC capability claims are vendor marketing]** — [Benerator CE](https://github.com/rapiddweller/rapiddweller-benerator-ce).
- **plaitpy.** MIT. Last release 0.1.1 (2018-01-26) and last commit 2018-01-25. **[documented]** — [PyPI](https://pypi.org/pypi/plaitpy/json), [repo](https://github.com/plaitpy/plaitpy).
- **Hypothesis.** MPL-2.0, 6.170.17 (2026-11-20). hypothesis-jsonschema is MPL-2.0, 0.23.2 (2026-10-27). **[documented]** — [PyPI hypothesis](https://pypi.org/pypi/hypothesis/json), [PyPI hypothesis-jsonschema](https://pypi.org/pypi/hypothesis-jsonschema/json).
  - Hypothesis is a property-based testing engine. Its strategies are built for boundary and shrinking search, not realistic distributions. **[inferred]**
- **SQLSynthGen (Alan Turing Institute).** MIT. Last release 0.4.2 (2023-12-14) and last commit 2023-12-14. **[documented]** — [PyPI](https://pypi.org/pypi/sqlsynthgen/json), [repo](https://github.com/alan-turing-institute/sqlsynthgen).
  - Its design (run aggregate SQL queries inside to produce "source stats", then generate outside from the schema plus the stats) matches this use case directly. **[lead only / from memory: README not read]**
- **DataFiller (Fabien Coelho, PostgreSQL schema-comment-driven).** **[unreachable]** The `zx80/datafiller` clone failed. PyPI's `datafiller` package (CyrilJl, Apache-2.0, 0.4.0, 2026-10-11) is a different project. **[documented]** — [PyPI datafiller](https://pypi.org/pypi/datafiller/json).
- Other packages checked:
  - pydbgen: MIT, single release 2018-03-11 — [PyPI](https://pypi.org/pypi/pydbgen/json).
  - datafaker (gangly): Apache-2.0, last release 2021-08-14 — [PyPI](https://pypi.org/pypi/datafaker/json).
  - **[documented]**

### Inferences
- What aggregate characterisations can drive in rule-based tools **[inferred]**:
  - per-column categorical frequency tables (Snowfakery `random_choice` weights; dbldatagen `values`/`weights`; Faker/Mimesis via custom providers)
  - numeric marginals (dbldatagen distributions; custom code elsewhere)
  - null rates
  - children-per-parent counts (Snowfakery `friends` with a random count; dbldatagen key ranges)
  - FK integrity
- What they cannot drive without hand-coding: multivariate correlations across many columns. A practical hybrid is to fit an mbi model outside from released marginals for the joint attributes, and use Faker, Mimesis or Snowfakery only for identifiers and PII-shaped strings and for the FK skeleton. **[inferred]**
- Licence-wise, avoid relying on dbldatagen outside Databricks until legal reviews the Databricks License. Benerator CE's GPL "with exceptions" also needs review if it is embedded. **[inferred]**

### Gaps
- Mimesis and Faker relational features were not reviewed (they are known to be per-field generators).
- TPC-DS/TPC-H `dsdgen`/`dbgen` scale-factor generators were not checked in this session.
- The SQLSynthGen README was not read, so its aggregate-stats feature is unverified.
- The Snowfakery docs on `--target-number` scaling were not read in full.

## Q4. The same real-world entity across several sources: record-linkage test data generators

### Takeaway
The established pattern comes from Febrl dsgen (2002–2011) and GeCo (Christen & Vatsalan, CIKM 2013), now continued by Gecko (MIT, 2024–2025). It works in two steps:
1. Generate "original" entities from frequency look-up tables.
2. Emit corrupted duplicates per original, with a count drawn from a uniform, Poisson or Zipf distribution, keeping the original→duplicate linkage as a label.

None of the tools I checked models per-source identifier schemes, per-source coverage or reporting delays as first-class settings. Those must be layered on, for example by emitting one view per source with its own ID mapping and sampling inclusion and lag. Splink's `transactions_origin`/`transactions_destination` pair is a small worked example of delay and value drift between two sources.

### Cited Findings
- **Febrl dsgen (`generate.py`, Febrl 0.4.2).**
  - Usage: `python generate.py [output_file] [num_originals] [num_duplicates] [max_duplicate_per_record] [max_modification_per_field] [max_modification_per_record] [distribution]`.
  - The distribution of duplicates per original is "uniform", "poisson" or "zipf". Records "contain randomly created names and addresses (using frequency files), dates, phone numbers, and identifier numbers". Misspelling dictionaries are supported.
  - Copyright 2002–2011 ANU. Dual licence: ANUOS 1.3 or GPL-2+.
  - **[documented]** — [FEBRL fork v0.4.2 (J535D165)](https://github.com/J535D165/FEBRL-fork-v0.4.2), last commit 2016-11-04. Upstream is on [SourceForge](https://sourceforge.net/projects/febrl/) (not checked).
- **GeCo (Christen & Vatsalan, CIKM 2013).**
  - Benefits of synthetic data: "(1) they can be generated with well defined characteristics; (2) it is known which records represent an individual created entity …; (3) the generated data and the generator program itself can be published".
  - Two steps: generate originals, then "the original records are corrupted to form new records, called duplicate records". "More than one duplicate record can be generated for one original record." It can also corrupt an existing dataset.
  - "Each generated original record is given a unique identifier, and each duplicate record is also given a unique identifier". The example sets `num_dup_dist = 'zipf'`. It supports dependencies "between up-to three attributes" and frequency look-up files.
  - **[documented]** — [Christen & Vatsalan 2013 PDF](https://users.cecs.anu.edu.au/~christen/publications/christen2013cikm.pdf).
  - The Python 2.7 code has not been developed since 2013. **[lead only]** — this comes from the gecko project's description surfaced in search.
- **Gecko (`gecko-syndata`, Univ. Medical Center Leipzig).**
  - "a spiritual successor to the GeCo framework … reimplements … for modern Python … NumPy and Pandas". Step 1 generates from frequency tables. Step 2 mutates a copy ("typos, edit errors and other common data sources").
  - MIT. PyPI 0.1.0 (2024-02-08) to 0.6.4 (2024-12-06). Last commit 2025-01-30.
  - **[documented]** — [gecko README](https://github.com/ul-mds/gecko), [PyPI](https://pypi.org/pypi/gecko-syndata/json).
- **Splink (MoJ) datasets.**
  - `fake_1000`: "250 simulated people, with different numbers of duplicates, labelled".
  - `historical_50k`: "based on historical persons scraped from wikidata. Duplicate records are introduced with a variety of errors"; 50,000 rows, 5,156 entities.
  - `febrl3`: 5,000 records, 2,000 originals, max 5 duplicates. `febrl4a`/`febrl4b`: 5,000 originals and one duplicate each, i.e. a two-source linkage task.
  - `transactions_origin`/`transactions_destination`: "each transaction is designed to have a counterpart … There may be a delay between the source and destination account, and the amount may vary due to hidden fees and foreign exchange rates. Memo is sometimes truncated or missing."
  - Splink is MIT, 5.0.0 (2026-09-28), last commit 2026-11-11.
  - **[documented]** — [Splink datasets table](https://github.com/moj-analytical-services/splink/blob/master/docs/includes/generated_files/datasets_table.md), [PyPI splink](https://pypi.org/pypi/splink/json).
  - Conflict: Splink's description says the FEBRL datasets "consist of comparison patterns from an epidemiological cancer study in Germany". That matches the separate Krebsregister dataset, not Febrl. The Febrl datasets are dsgen-synthetic. **[inferred: likely a copy-paste error in Splink metadata]**
  - The `splink_synthetic_data` generator repo could not be cloned. **[unreachable]**
- **recordlinkage toolkit.** BSD-3. Last release 0.16 (2023-07-20) and last commit 2023-07-20. It bundles Febrl datasets 1–4 loaders. **[documented: PyPI/commit]; loaders [from memory, not re-read]** — [PyPI recordlinkage](https://pypi.org/pypi/recordlinkage/json).
- **SERD / "Synthesizing Privacy Preserving Entity Resolution Datasets" (Qin, Chai, Tang, Li, Luo, Li, Zhu; Tsinghua/QCRI).** It works in four steps:
  1. "learn the true similarity distributions of both matching and non-matching entity pairs from real dataset";
  2. synthesise "fake but semantically meaningful entities" with transformers under DP;
  3. add match and non-match labels;
  4. use "entity rejection".
  - Matchers trained on synthetic vs real differ in F1 "within 6% on 3 commonly used ER datasets". **[documented: PDF read]** — [PDF](https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/4-6-Synthesizing_Entity_Resolution_Datasets.pdf).
  - The venue and year are not stated on the pages I extracted. I believe it is ICDE 2023 **[unverified]**.
  - Here the characterisation that leaves is the per-attribute similarity distributions for match and non-match pairs: aggregates of the linkage structure, not of the rows. **[inferred]**
- **Alaska benchmark (arXiv 2101.11259).** A real multi-source ER/schema-matching benchmark with ground truth verified manually by domain experts. **[lead only]** — [arXiv](https://arxiv.org/abs/2101.11259).

### Inferences
- A generator for "the same entity across N sources with their own IDs, coverage and delays" can be assembled from documented parts **[inferred]**:
  1. Generate a ground-truth entity table (mbi or copula from released marginals, or Faker/Gecko frequency tables).
  2. For each source s, sample inclusion with the coverage rate for that source and segment.
  3. Sample the reporting delay from the released delay distribution for that source.
  4. Assign a source-specific identifier (in the source's format; a Faker/regex generator).
  5. Apply source-specific corruption profiles (Gecko/GeCo mutators).
  6. Write a hidden `entity_id ↔ (source, source_id)` crosswalk as the label.
- The aggregates such a generator needs are:
  - coverage per source × segment
  - overlap counts between sources (pairwise or k-way Venn counts)
  - delay histograms
  - error/corruption rates per field and source
  - duplicates-per-entity distribution within a source

  All of these are counts that could be computed inside and released. **[inferred]**
- Febrl, GeCo and Gecko support a duplicate-count distribution but not k-way source overlap. That overlap structure would have to be custom code. **[inferred]**

### Gaps
- The Splink synthetic data generator repo was unreachable.
- I did not search for 2024–2026 multi-source ER generators in depth. The one search found only SERD and Alaska.
- The upstream GeCo download page (dmm.anu.edu.au/geco) was not fetched.
- DSGen as a separately named tool was not identified beyond Febrl dsgen.

## Q5. One characterisation, many sizes: small edge-case-rich sets and large realistic sets from the same model

### Takeaway
Most learned synthesizers decouple size from fit: `sample(num_rows)` in SDV, mbi and SmartNoise; `size=` in MOSTLY AI. Multi-table scaling preserves cardinality via SDV `sample_scale(scale=…)` (HMA in Community).

Over-representing rare cases is supported in two places:
- **SDV single-table conditional sampling (Community).** Multi-table conditional sampling and "extrapolate outside training ranges" are paid Enterprise bundles.
- **MOSTLY AI.** Its `seed`, rebalancing and temperature features are documented in its README (claims are vendor marketing).

Billion-row generation is documented only for Spark-based dbldatagen, a rule-based tool (vendor claim). The realistic route to "1 billion rows at real distributions" is therefore: fit or estimate a model, then sample in parallel batches. This is my inference; no OSS tool I checked documents it end to end.

### Cited Findings
- **SDV sampling.**
  - `sample(num_rows=…)`: "`batch_size` … If you are sampling a large number of rows, setting a smaller batch size allows you to see and save incremental progress". `max_tries_per_batch` exists because "If you have included constraints, it may take multiple batches to create valid data". This is rejection sampling for constraints.
  - `sample_scale(scale=2.5)`: "only available for multi-table synthesizers"; at "`1` … roughly the same size as the original data".
  - **[documented]** — [SDV sample realistic data](https://docs.sdv.dev/sdv/sampling/sample-realistic-data).
  - SDV 2.0.0 (2026-10-15) added the multi-table `sample_scale` in its new form. **[documented]** — [HISTORY.md](https://github.com/sdv-dev/SDV/blob/main/HISTORY.md).
- **SDV conditional sampling.** Single-table: `Condition(num_rows=250, column_values={…})`, "The rest of the synthetic data adapts to the values you provide". This is Community. **[documented]** — [single-table conditional](https://docs.sdv.dev/sdv/sampling/conditional/single-table).
  - Multi-table conditional (`MultiTableCondition`, e.g. "10 resort hotels" plus guests in suites) is "part of the Targeted Sampling bundle, an optional add-on to SDV Enterprise". **[documented]** — [multi-table conditional](https://docs.sdv.dev/sdv/sampling/conditional/multi-table).
- **SDV constraints.** Community has FixedIncrements, FixedCombinations, Inequality, OneHotEncoding and Range. Custom and multi-table constraints are in the paid CAG bundle. **[documented]** — [compare page](https://docs.sdv.dev/sdv/explore/compare-features).
  - 2.2.0 notes: "Multi-table constraints should reject invalid rows after reverse transforming". **[documented]** — HISTORY.md.
- **MOSTLY AI.** `mostly.probe(g, size=1000)` gives "representative synthetic samples". `mostly.probe(g, seed=[{"age":24,"sex":"Male"}]*10_000)` gives "samples based on fixed column values". The README also lists "Re-balance underrepresented segments" and "Up-sample to any data volumes". **[documented API; capability claims vendor marketing]** — [mostlyai README](https://github.com/mostly-ai/mostlyai).
- **mbi.** `model.synthetic_data(rows=N)` takes any N. **[documented]** — [mbi README](https://github.com/ryan112358/private-pgm).
- **Febrl dsgen and GeCo.** Sizes are parameters (num_originals, num_duplicates), and duplicate skew is selectable (uniform, Poisson or Zipf). **[documented]** — see Q4.
- **dbldatagen.** "billions of rows within minutes" on Spark, with "repeatable, predictable data". **[vendor README / marketing]** — [dbldatagen](https://github.com/databrickslabs/dbldatagen).
- **Synth.** "see how your system will scale if your database suddenly has 10x the amount of data". **[documented README]** — [synth](https://github.com/getsynth/synth).

### Inferences
- **Small, edge-case-heavy sets from the same characterisation.** These are best produced by mixing two generators over one schema and spec **[inferred]**:
  - (a) Model-based stratified or conditional sampling with skewed condition weights. Examples: SDV `Condition` per rare category, MOSTLY `seed`, or mbi conditioning by sampling and filtering.
  - (b) Rule-based boundary injection from the released range metadata: min, max, null, empty string, max-length, Unicode, duplicate keys, orphan-FK negative tests, entities present in only one source, maximum delay. Examples are Hypothesis strategies or Faker/Snowfakery recipes using the same column domains.
  - Learned models do not extrapolate beyond training ranges unless asked. SDV sells extrapolation as a bundle. So pure model sampling under-produces boundary values. **[inferred + documented that extrapolation is a paid feature]**
- **Large realistic sets.** Sample from the fitted model in independent seeded batches. That works for mbi, SDV and MOSTLY, though I did not verify parallel APIs. For FK integrity at scale, generate parents first, then children per parent from the cardinality distribution. **[inferred]**
- Rejection sampling for constraints (SDV `max_tries_per_batch`) gets slow when the constraint region is rare. Conditioning is preferable for strongly over-represented edge cases. **[inferred]**

### Gaps
- No OSS tool I checked documents a single "scale factor + edge-case boost" setting over a learned multi-table model.
- Throughput figures for SDV/MOSTLY at 10^8–10^9 rows were not found.
- I did not check whether HMA `sample_scale` re-samples parents or only multiplies row counts.

## Q6. Maintenance state and licences (as of 2026-11-26)

### Takeaway
The actively maintained tools are SDV (BSL), MOSTLY AI SDK/engine (Apache-2.0), mbi/Private-PGM (Apache-2.0), SmartNoise Synth (MIT), synthpop (GPL), Faker/Mimesis (MIT), Hypothesis (MPL-2.0), Splink (MIT) and Snowfakery (BSD-3).

Restrictive or non-OSI licences:
- SDV, RDT, Copulas, CTGAN and SDGym: BUSL-1.1, no "Synthetic Data Service"; each release becomes MIT 4 years after it ships.
- dbldatagen: Databricks License.
- gretel-synthetics: "source-available", "Free To Use But Restricted".
- ydata-sdk: proprietary production licence.
- ClavaDDPM: no licence.
- IRG: code withheld.

Stale or dormant: plaitpy, getsynth/synth, DataSynthesizer releases (2023), recordlinkage (2023), TabDDPM (2023), RCTGAN (2023), SQLSynthGen (2023) and Febrl.

### Cited Findings
PyPI first and last release dates are from `https://pypi.org/pypi/<pkg>/json`; last-commit dates are from a git clone on 2026-11-26. All rows are **[documented]** unless marked.

| Tool | Licence | Latest release (date) | Last commit | Notes |
|---|---|---|---|---|
| SDV | BUSL-1.1 (since 0.18.0, 2023-01-24) | 2.2.0 (2026-11-06); 1.39.0 (2026-11-12) | 2026-11-16 | Community vs Enterprise split |
| RDT / Copulas / CTGAN / SDGym | BUSL-1.1 | 2.1.0 / 0.15.0 / 0.13.0 (all 2026-10-30) / 0.17.0 (2026-11-13) | n/a | DataCebo |
| SDMetrics | MIT | 0.33.1 (2026-11-25) | n/a | |
| mostlyai (SDK) | Apache-2.0 | 6.2.1 (2026-10-29); first 2023-12-29 | 2026-10-29 | LOCAL mode default |
| mostlyai-engine | Apache-2.0 | 2.7.4 (2026-10-29); first 1.0.0 2025-01-20 | 2026-10-29 | TabularARGN |
| mostlyai-qa | Apache-2.0 | 1.10.11 (2026-10-09) | n/a | |
| mbi (Private-PGM) | Apache-2.0 | 2.1.0 (2026-11-06) | 2026-11-25 | MST/AIM mechanisms in repo |
| smartnoise-synth | MIT | 1.0.8 (2026-04-15) | 2026-04-21 | MWEM, MST, AIM, DP-CTGAN, PATE-CTGAN |
| DataSynthesizer | MIT | 0.1.13 (2023-10-18) | 2026-07-15 | "Pre-Alpha" classifier |
| synthpop (R) | GPL-2/GPL-3 | 1.9-3 (2026-09-10) | n/a | [CRAN](https://cran.r-project.org/package=synthpop) |
| REaLTabFormer | MIT | 0.2.4 (2026-01-04) | 2026-01-04 | |
| be-great (GReaT) | MIT | 0.0.14 (2026-05-12) | n/a | |
| synthcity | Apache-2.0 | 0.2.12 (2025-05-08) | 2025-06-17 | |
| TabDDPM | not checked | n/a | 2023-03-09 | research code |
| TabSyn | not checked (LICENSE present) | n/a | 2024-06-20 | research code |
| ClavaDDPM | **no LICENSE file** | n/a | 2024-10-27 | research code |
| RCTGAN | MIT/Apache inconsistent | 1.1 (2025-02-12) | 2023-07-06 | "Planning" status |
| IRG | n/a | n/a | 2026-02-18 | **placeholders; commercial** |
| ydata-synthetic | GPLv3+ (classifier) | 2.0.1 (2026-04-23) | n/a | |
| ydata-sdk | **proprietary "Production License Agreement"** | 3.2.3 (2026-02-27) | n/a | |
| gretel-synthetics | **source-available, "Free To Use But Restricted"** | 0.22.20 (2025-06-24) | n/a | |
| Faker | MIT | 40.63.0 (2026-11-20) | n/a | |
| Mimesis | MIT | 22.2.0 (2026-09-23) | n/a | |
| Snowfakery | BSD-3 | 4.2.1; 5.0.0.dev1 (2026-04-27) | 2026-01-09 | |
| dbldatagen | **Databricks License** | 0.4.0.post1 (2024-07-26) | 2026-10-26 | |
| synth (getsynth) | Apache-2.0 | n/a | 2024-09-27 | Public Alpha |
| Benerator CE | GPL-2 with exceptions | 4.0.1 (CHANGELOG) | 2026-08-09 | bug-fix only; → DATAMIMIC |
| plaitpy | MIT | 0.1.1 (2018-01-26) | 2018-01-25 | dormant |
| SQLSynthGen | MIT | 0.4.2 (2023-12-14) | 2023-12-14 | |
| Hypothesis / hypothesis-jsonschema | MPL-2.0 | 6.170.17 (2026-11-20) / 0.23.2 (2026-10-27) | n/a | |
| Splink | MIT | 5.0.0 (2026-09-28) | 2026-11-11 | labelled ER datasets |
| recordlinkage | BSD-3 | 0.16 (2023-07-20) | 2023-07-20 | |
| gecko-syndata | MIT | 0.6.4 (2024-12-06) | 2025-01-30 | GeCo successor |
| Febrl 0.4.2 (fork) | ANUOS 1.3 or GPL-2+ | n/a | 2016-11-04 | |
| NIST CRC | see repo LICENSE | Data bundle v1.3 | 2026-03-19 | benchmark corpus |

Sources for the table:
- PyPI JSON: [sdv](https://pypi.org/pypi/sdv/json), [mostlyai](https://pypi.org/pypi/mostlyai/json), [mbi](https://pypi.org/pypi/mbi/json), [smartnoise-synth](https://pypi.org/pypi/smartnoise-synth/json), [gretel-synthetics](https://pypi.org/pypi/gretel-synthetics/json), [ydata-sdk](https://pypi.org/pypi/ydata-sdk/json), [ydata-synthetic](https://pypi.org/pypi/ydata-synthetic/json), [faker](https://pypi.org/pypi/faker/json), [snowfakery](https://pypi.org/pypi/snowfakery/json), [dbldatagen](https://pypi.org/pypi/dbldatagen/json), [gecko-syndata](https://pypi.org/pypi/gecko-syndata/json).
- The repos linked in Q1–Q4.

### Inferences
- For a team that wants permissive OSS with multi-table support and an active maintainer, MOSTLY AI's SDK/engine (Apache-2.0) is the main option. SDV under BSL is usable internally (employees and contractors), but its multi-table scalability in Community is capped at HMA. **[inferred]**
- For the aggregates-only constraint, mbi (Apache-2.0, very active) is the best-maintained building block. **[inferred]**

### Gaps
- Without the GitHub API I could not get issue/PR activity or star counts.
- Exact BSL release-to-MIT conversion dates for specific SDV versions were not tabulated.
- The TabSyn and TabDDPM licence texts were not read.
- I did not read the NIST CRC LICENSE terms.
