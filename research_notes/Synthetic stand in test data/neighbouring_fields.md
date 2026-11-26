# Neighbouring fields: realistic stand-in structured data without exposing real data

Retrieval date for all sources: 2026-11-26. Evidence labels:
- **[documented]**: I read the full text, or the full primary page or file.
- **[lead]**: search-result or abstract text only. This is not a verdict.
- **[inferred]**: my reasoning.
- **[vendor marketing]**: the claim comes from the tool vendor.
- **[unreachable]**: I could not retrieve the source.

Maintenance state comes from cloning each repo (`git clone --bare --depth 1`) and reading the last commit date. It also uses the PyPI JSON API and crandb.r-pkg.org, all queried 2026-11-26. The GitHub REST API was not available in this session.

## Official statistics: terminology, dummy/test files for remote execution, and how close they are to real data

### Takeaway
Official statistics has the most explicit vocabulary for this problem.
- The CBS July 2026 terminology paper defines a ladder of terms: arbitrary, dummy, random, **simulated**, synthetic (fully or partially).
- The ONS synthetic data spectrum has six levels, from structural to replica.

Under the CBS definitions, data generated only from metadata plus high-level aggregates is **"simulated data", not "synthetic data"**. CBS also advises releasing the aggregates themselves rather than a simulated file.

Real remote-execution test files are built from **real rows** by sampling, swapping and micro-aggregation. Examples are the IAB-FDZ "Testdaten" and the ONS LFS pilot. They are good code-testing stand-ins but would breach an aggregates-only rule.

### Cited Findings

**Terminology and history**
- **[documented]** CBS discussion paper, Turner, Stoel & de Wolf, "Synthetic Data Terminology in Official Statistics", July 2026.
  - It is an internally reviewed preprint ahead of journal publication.
  - It traces synthetic data to Rubin (1993): multiple imputation used to replace microdata releases. This extended Little (1993) on masking parts of records with synthetic values.
  - It cites Reiter & Raghunathan (2007) for the combining rules that allow valid inference from multiple synthetic datasets. It points to Drechsler & Haensch (2024) for a fuller history.
  - [CBS 2026 PDF](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf); [CBS landing page](https://www.cbs.nl/en-gb/background/2026/31/synthetic-data-terminology-in-official-statistics)
- **[documented]** CBS 2026 definitions, ranked by how much real-data information each one captures:
  - **Arbitrary data**: no real-world information at all. CBS advises against the terms "fake" and "mock" data.
  - **Dummy data**: a placeholder that uses only metadata, such as categories and integer ranges. The paper cites OpenSAFELY (2021) as an example. Outliers and new categories in the real data are not necessarily represented.
  - **Random data** (also "fictitious"): theory-driven parameters.
  - **Simulated data**: "metadata and high-level aggregate statistics from previously collected real-world data, enriched with expert knowledge and/or literature knowledge … does not include data-generation models that use unit-level real-world data".
  - **Synthetic data**: unit-level data from a model *estimated on real microdata*. It can be fully synthetic, partially synthetic, or **hybrid** (a weighted mix of original and synthetic). Partially synthetic and hybrid data keep the same number of units as the real data, which affects disclosure risk.
  - Source: [CBS 2026 PDF](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)
- **[documented]** CBS 2026 classes agent-based-model output as *synthetic*, not simulated. The reason given is that "fine-tuning and validating sound agent-based models require intensive use of real-world data on the unit level". [CBS 2026 PDF](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)
- **[documented]** CBS 2026 recommends that when only high-level summary statistics are used, the office should release the summary statistics directly. This lets general SDC be applied to the statistics and makes the file's limits obvious. CBS also warns that labelling simulated data "synthetic" raises false expectations of fidelity, and leads to a different, more labour-intensive SDC review. [CBS 2026 PDF](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)
- **[documented]** CBS 2026 names a terminology trap: "dummy data" means metadata-only placeholders to one community, but can mean carefully built, sensitive synthetic data to another. [CBS 2026 PDF](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)

**The ONS synthetic data spectrum and the LFS pilot**
- **[documented]** ONS Methodology Working Paper 16, "Synthetic data pilot", defines six levels:
  1. *Synthetic structural*: variable names and types only. No disclosure risk. For basic code testing.
  2. *Synthetic valid*: formats and plausible record-level combinations that pass the same validation checks as real data. Built from metadata and open sources. Minimal risk. For advanced code testing.
  3. *Synthetically-augmented plausible*: built from real data. Univariate distributions are kept, with smoothing. Non-negligible risk.
  4. *Augmented multivariate plausible*: high risk.
  5. *Augmented multivariate detailed*: very high risk.
  6. *Augmented replica*: extremely high risk. Probably only usable inside a secure facility.
  - Source: [ONS WP16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)
  - The page shows no publication date. Its references end in October 2017 and it uses Q2 2017 LFS data, so I infer a date of about 2018.
- **[documented]** How the ONS pilot was built:
  - It synthesised the Q2 2017 Labour Force Survey *inside the Secure Research Service*: 88,801 records, 22 characteristic variables and 6 geographic variables.
  - Characteristics used CART via R synthpop, with at most two predictors per variable and grouped age as a universal predictor.
  - Variables with under 80% response became presence flags, with a random observed category drawn when present.
  - Geography was not modelled. A random output area was drawn from open ONS lookups.
  - The result is level 2–3, intended for code testing before going to the secure lab.
  - The paper notes that working from univariate frequency tables alone would probably give only level 1, "with poorer control over illogical combinations".
  - Source: [ONS WP16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)

**IAB-FDZ test data (Germany)**
- **[documented]** BA Employment Panel test data:
  - Built by sampling, micro-aggregation and anonymisation of the original data. "Certain variable distributions were simulated; furthermore, a number of individuals were also invented."
  - Marginal distributions are kept "as far as possible", and joint distributions are kept for named variable groups, such as reason-of-notification × wage × transition-zone.
  - For profession, nationality and industry, **every value occurring in a wave appears at least once in the test wave**, which deliberately distorts those marginals. A test variable only takes values that occur in the original wave.
  - Age and wage are smoothed, so there are no extremes.
  - The data are not consistent over time: a person's gender can change between waves.
  - Sensitive variables appear un-aggregated, unlike in the real data.
  - "Non-workable evaluation programs that appear not to have been tested in advance using the available test data will not be considered and will be returned."
  - The document is undated.
  - Source: [IAB Hilfe_Testdaten_e.pdf](https://doku.iab.de/fdz/ba/Hilfe_Testdaten_e.pdf)
- **[documented]** SIAB test data:
  - It is a 1.1% random sample of SIAB, treated with a "data swapping" algorithm. Values are drawn from the overall sample distribution within defined clusters (per variable, data source and validity period).
  - Univariate distributions are kept "in virtually the same form". Relationships across clusters are lost.
  - The chronological order and overlap of episodes across sources is kept. Dates are slightly modified, and person-to-establishment allocation is randomly modified.
  - Derived auxiliary variables are regenerated after anonymisation.
  - There are 161,271 observations on 19,543 fictitious individuals. Only people with fewer than 20 observations are included, and people with employment-only histories are excluded.
  - Its purpose is to let users prepare programs and then send them for **remote execution** or bring them to a guest stay.
  - Source: [IAB SIAB_Testdaten_en.pdf](https://doku.iab.de/fdz/siab/SIAB_Testdaten_en.pdf)
- **[lead]** A Springer chapter on LEED test data states the aim of keeping skip patterns, logical constraints and longitudinal relationships, so that code "runs on the original data without modification". [Springer chapter](https://rd.springer.com/chapter/10.1007/978-3-642-33627-0_13)

**CMS Medicare synthetic files (US)**
- **[documented]** CMS 2008–2010 DE-SynPUF:
  - It has five file types: beneficiary summary, inpatient, outpatient, carrier and Part D events. These are released as 20 samples.
  - It was designed for "the very highest degree of protection". DESYNPUF_ID is a cryptographic identifier.
  - It has "very limited inferential research value". Programs built on it should work on CMS Limited Data Sets.
  - Its stated uses are software development, training researchers before they request real data, and data-mining innovation.
  - The synthesis method is not described on the page.
  - Source: [CMS DE-SynPUF page](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf)

**UK guidance on synthetic data for trusted research environments**
- **[lead]** UK Data Service guidance:
  - Synthetic data supports familiarisation with data structure and coding without secure access.
  - Synthetic data are "not inherently 'safe' simply because they are not real".
  - Files must be unambiguously labelled as synthetic.
  - Source: [UKDS synthetic data collections](https://ukdataservice.ac.uk/learning-hub/data-producer-support/special-contexts-and-additional-considerations/syntheticdatacollections/)
- **[lead]** ADR UK frames synthetic data as letting analysis development run in parallel with the access application, which shortens time to results. The ONS SRS is one environment being evaluated. [ADR UK project](https://www.adruk.org/our-work/browse-all-projects/evaluating-the-benefits-costs-and-utility-of-synthetic-data/)
- **[lead]** arXiv 2111.06301, on code for trusted research environments, recommends shipping a small dummy dataset with the same columns and types as the original alongside the code. [arXiv 2111.06301](https://arxiv.org/pdf/2111.06301)

**Software**
- **[documented]** R `synthpop` (SDC synthesis, not population synthesis): CRAN 1.9-3, published 2026-09-10. Maintained. [crandb synthpop](https://crandb.r-pkg.org/synthpop)
- **[documented]** R `sdcMicro`: CRAN 5.8.2, published 2026-06-12. Last GitHub commit 2026-11-21. Maintained. [crandb sdcMicro](https://crandb.r-pkg.org/sdcMicro); [sdcTools/sdcMicro](https://github.com/sdcTools/sdcMicro)

### Inferences
- **[inferred]** The CBS 2026 ladder fits the platform's aggregates-only rule exactly. A generator outside the protected environment, driven only by released aggregates and metadata, produces **"simulated data"** in CBS terms. Its realism is capped by which aggregates are released. The CBS view supports a design in which the *aggregate characterisation itself* is the reviewed, SDC-checked release artefact, and the generator is ordinary code outside.
- **[inferred]** In ONS terms, an aggregates-only generator can reach level 2 ("valid": passes validation, plausible combinations) using metadata and open sources. Releasing selected univariate and bivariate aggregates under SDC pushes it toward level 3–4 behaviour. Levels 3–6 in ONS's own sense come from unit records, so aggregates-only output would not formally be "augmented".
- **[inferred]** Two IAB tricks transfer directly to a test-data generator:
  - Guaranteeing every category value occurring in the real data appears at least once (code-path coverage).
  - Accepting distorted marginals as the price of that coverage.

  The IAB "test before you submit" rule is also a direct governance analogue: code that fails on the stand-in is rejected before it reaches the protected environment.
- **[inferred]** IAB SIAB and ONS LFS stand-ins are derived from real rows (sampled, swapped, or modelled with CART). They would violate an aggregates-only rule even though they are labelled anonymous. The transferable part is the *structural requirements*, not the methods: episode ordering across sources, regenerated derived variables, and missing-value codes.

### Gaps
- **[unreachable]** I did not read the full text of the UNECE "Synthetic Data for Official Statistics: A Starter Guide" (ECE/CES/STAT/2022/6). The UN Digital Library file URL returned HTML, not the PDF. Only the record and search snippets were seen: it was led by Kate Burnett-Isaacs (Statistics Canada) under the HLG-MOS, © 2022. I found no "later update" beyond the CBS 2026 paper. [UN record](https://digitallibrary.un.org/record/4027270); [UN iLibrary methods chapter](https://www.un-ilibrary.org/content/books/9789210021708c005)
- I found no primary documentation of dummy or test files for Statistics Netherlands Remote Access, DST Denmark, ABS DataLab or the UK ONS SRS standard offer. The CBS search returned only generic synthetic-data pages and service catalogues, which I did not read.
- I did not read the original papers by Rubin (1993), Little (1993), Reiter or Raghunathan. They are cited here via CBS 2026.

## Microsimulation and population synthesis: building entity-level populations from marginal tables

### Takeaway
Population synthesis is the most directly transferable field for "generate entities from a characterisation". It fits marginal control totals at one or more geographic or entity levels, using IPF, IPU or entropy-maximising list balancing. The weights are then integerised (LP or quasirandom sampling) to emit households and persons.

Most tools want a *seed sample* of real microdata, so an aggregates-only setting needs a seedless method such as humanleague's QIS, or a synthetic seed. Maintained tools:
- **PopulationSim** (active, 2026)
- **humanleague** (Python active; R maintenance-only)
- **mipfp** (R)
- **simPop** (GitHub active in 2026; last CRAN release 2024)

UDST `synthpop` (Python) and `ipfn` are dormant.

### Cited Findings
- **[documented]** PopulationSim's method and inputs:
  - It uses "entropy maximization based list balancing to match controls specified at various geographic levels". It converts weights to integers by linear programming, then expands the seed sample.
  - Its inputs are a seed sample (typically Census PUMS or a household travel survey) and controls (household- or person-level distributions for geographies such as block groups, TAZs or counties).
  - Its outputs are household and person tables, plus optional multi-way distributions and final survey weights.
  - The docs page fetched was labelled version 0.5.1.
  - Source: [PopulationSim docs](https://activitysim.github.io/populationsim/)
- **[documented]** PopulationSim maintenance: PyPI 0.10.0 uploaded 2025-11-03. Last commit 2026-11-05 ("restore documentation publishing and modernize CI"). It originated at Oregon DOT. [PyPI populationsim](https://pypi.org/pypi/populationsim/json); [ActivitySim/populationsim](https://github.com/ActivitySim/populationsim)
- **[documented]** ActivitySim: PyPI 1.6.0, uploaded 2026-09-17. [PyPI activitysim](https://pypi.org/pypi/activitysim/json)
- **[documented]** humanleague:
  - It does "microsynthesising populations from marginal and (optionally) seed data" in C++, with IPF, Quasirandom Integer Sampling (QIS, **no seed population**), and QISI (QIS of a dynamic IPF solution).
  - QISI "generates high-entropy integral populations", supports multiple populations for sensitivity analysis, and "goes some way to address the 'empty cells' issues" of plain IPF.
  - It supports arbitrary dimensionality, plus an integerisation algorithm constrained to all marginal sums.
  - "Ongoing development is for the python version only. R development is currently maintenance-only."
  - Maintenance: PyPI 2.4.5 on 2026-08-29; CRAN 2.3.2 on 2024-10-23; last commit 2026-10-26.
  - Sources: [virgesmith/humanleague README](https://raw.githubusercontent.com/virgesmith/humanleague/main/README.md); [PyPI humanleague](https://pypi.org/pypi/humanleague/json); [crandb humanleague](https://crandb.r-pkg.org/humanleague)
- **[documented]** mipfp (multidimensional IPF and alternatives, R): CRAN 3.2.3, published 2026-08-22. [crandb mipfp](https://crandb.r-pkg.org/mipfp)
- **[documented]** ipfn (Python N-dimensional IPF): PyPI 1.4.4, 2021-12-30. Dormant. [PyPI ipfn](https://pypi.org/pypi/ipfn/json)
- **[documented]** simPop ("Simulation of Complex Synthetic Data Information"; Templ, Kowarik, Meindl et al., Statistics Austria):
  - CRAN 2.1.3, published 2024-01-08.
  - GitHub DESCRIPTION is at 2.1.4 (dated 2024-01-05). Last commit 2026-01-20 ("fix bug when using xgboost and simCategorical()").
  - So it is maintained on GitHub, with a stale CRAN release.
  - Sources: [crandb simPop](https://crandb.r-pkg.org/simPop); [statistikat/simPop](https://github.com/statistikat/simPop)
- **[documented]** UDST synthpop (Python population synthesis, a different package from R synthpop): last commit 2021-10-28; PyPI "synthpop" 0.1.1 on 2018-11-13. Dormant. Note the name collision. [UDST/synthpop](https://github.com/UDST/synthpop); [PyPI synthpop](https://pypi.org/pypi/synthpop/json)
- **[documented]** OpenFisca-core ("a versatile microsimulation free software"): PyPI 46.1.0 uploaded 2026-11-24. Last commit 2026-11-24. Very active. [PyPI openfisca-core](https://pypi.org/pypi/openfisca-core/json); [openfisca/openfisca-core](https://github.com/openfisca/openfisca-core)
- **[documented]** CBS 2026 cites Chapuis et al. (2022) for agent-based generation of demographic microdata, and deems the output synthetic because calibration uses unit data. [CBS 2026 PDF](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)

### Inferences
- **[inferred]** Mapping to the platform:
  - **Marginal and joint control tables** are an SDC-checkable characterisation that can leave the protected environment, such as cross-tabs with minimum cell sizes.
  - Fitting them is a well-understood problem: IPF, entropy list balancing, LP integerisation.
  - **Multi-level controls** (household plus person in PopulationSim) map onto multi-entity schemas such as organisation plus person plus account. These fit parent and child counts jointly.
- **[inferred]** The seed sample is the key incompatibility. PopulationSim, IPU-style tools and most IPF uses reweight a real seed sample, which cannot leave the protected environment. There are two aggregates-only options:
  - (a) Seedless synthesis, such as humanleague QIS, or IPF from a uniform or structural-zero seed.
  - (b) A synthetic seed from a metadata-only generator, reweighted to released marginals.
- **[inferred]** Structural zeros (impossible combinations) must be supplied as metadata or rules, because aggregates alone often cannot distinguish a structural zero from a suppressed small cell. This echoes the ONS observation that univariate tables give "poorer control over illogical combinations".
- **[inferred]** OpenFisca's YAML test cases (hand-specified entity situations with expected outputs) are close to the platform's current hand-written tests. They are a pattern for *assertion* fixtures, not realistic volume data. **Not verified in its docs.**

### Gaps
- I did not research EUROMOD input-data handling, MOSAIC or MITOS, spatial microsimulation (simulated annealing or combinatorial optimisation literature, for example Lovelace & Dumont), or IPU (Ye et al. 2009) from primary texts. No claims are made on them.
- I did not read the simPop method details (the JSS paper). PopulationSim's docs page shows 0.5.1 while PyPI is 0.10.0, so its algorithm description may be stale.

## Healthcare: Synthea, OMOP/Eunomia, Simulacrum, OpenSAFELY dummy data, CPRD, NHS artificial data

### Takeaway
Healthcare has the two strongest analogues.
- **Simulacrum** (NHS England / Health Data Insight): inside the protected environment, pseudonymised registry records are aggregated into **"data cubes" of at least 50 patients**. The cubes are anonymous and were publicly released for v1.0.0. Synthetic patients, tumours and treatments are then sampled from the cubes. The data model is identical to the real Cancer Analysis System, so researchers write PL/SQL against Simulacrum, and NCRAS runs it on real data and checks outputs against the ISB anonymisation standard.
- **OpenSAFELY** generates **dummy data from the dataset definition alone**. Code is written locally and re-run unchanged inside the secure environment.

**Synthea** is the reference for *knowledge-driven* simulation from published statistics (state-machine modules, no real rows). It is very actively maintained, but its realism is weak when validated.

### Cited Findings

**Simulacrum**
- **[documented]** Generation method (HDI "Synthetic data generation method" page):
  - The source is pseudonymised NDRS records from the Cancer Analysis System, with name, date of birth, address and NHS number removed beforehand.
  - Relationships (for example age × cancer type) are found with "computational methods and domain knowledge".
  - Data are aggregated into data cubes "based on at least 50 patient records". These cubes are "anonymous and safe to release" and were publicly released alongside v1.0.0.
  - Synthetic patient, tumour and treatment characteristics are "randomly chosen from the relevant data cube". Because values are sampled, "the procedure cannot be reversed".
  - For rarer cancers, records "may not look realistic".
  - The page links a methodology white paper (file name "Methodology-Overview-Nov18"), which I did not read.
  - Source: [Simulacrum method page](https://simulacrum.healthdatainsight.org.uk/?p=3940)
- **[documented]** Simulacrum versions:

  | Version | Released | Coverage | Notes |
  |---|---|---|---|
  | v1.1.0 | 2018 | Diagnoses 2013–2015, tumours plus SACT | |
  | v1.2.0 | 2021 | Diagnoses 2013–2017 | |
  | v2.0.0 beta | 2022 | Tumour, SACT, radiotherapy, somatic gene testing | |
  | v2.1.0 | April 2023 | Diagnoses 2016–2019 | "Updates to the synthetic data generation method" that improve some statistical properties |

  - The new method is not named. v1 and v2 are freely downloadable.
  - Sources: [Simulacrum versions](https://simulacrum.healthdatainsight.org.uk/about-the-simulacrum/simulacrum-versions/); [Simulacrum home](https://simulacrum.healthdatainsight.org.uk/)
- **[documented]** PHE/NCRAS "Guide to using the Simulacrum and submitting code" (June 2020), part 1: what the data are for.
  - "Because the Simulacrum data model is the same as the real one … [it] can be used to write and test queries that … could be run on the real data."
  - "The more complex the data query the more approximate the results."
  - It is *not* for epidemiological questions. Its uses are feasibility checks (is a drug recorded?), field completeness, cohort definition, choosing data items for an ODR request, and ML test data.
  - Supplying "working and appropriately structured PL/SQL code" reduces extraction time and cost.
  - Source: [NCRAS guide PDF](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/893386/NCRAS_guide_to_using_the_Simulacrum_and_submitting_code.pdf)
- **[documented]** NCRAS guide (June 2020), part 2: submitting code to run on real data.
  - CAS runs Oracle, so submitted code must be PL/SQL for extraction, with R or Stata for modelling.
  - Code can target an aggregate release or a depersonalised row-level release.
  - NCRAS Enquiries releases only anonymous data meeting the ISB Anonymisation Standard. The researcher must show, by running the query on Simulacrum, that the output would meet it. For individual-level data the typical route is "Plan 3": weak k-anonymity. The assessment is reviewed by an NCRAS analyst and the Caldicott Guardian.
  - Requests are only accepted if running and checking take under 3 hours of analyst time. Otherwise they go to HDI (with IQVIA) or the ODR.
  - Source: [NCRAS guide PDF](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/893386/NCRAS_guide_to_using_the_Simulacrum_and_submitting_code.pdf)
- **[documented]** The NCRAS guide notes a real-versus-synthetic discrepancy: simulated SACT is linked to tumours only at patient level (LINKNUMBER). The real data use an NCRAS tumour-linkage algorithm based on a −31-day window, dates and site, which is not reproduced. [NCRAS guide PDF](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/893386/NCRAS_guide_to_using_the_Simulacrum_and_submitting_code.pdf)

**OpenSAFELY**
- **[documented]** OpenSAFELY ehrQL dummy data:
  - "ehrQL will use the dataset definition to set up dummy data and generate matching patients". The default is 10 patients, changed with `configure_dummy_data(population_size=1000)`.
  - Users can instead supply a dummy dataset (CSV, CSV.gz or Arrow, via `--dummy-data-file`) or per-table dummy tables (`--dummy-tables`, `create-dummy-tables`). ehrQL validates their column names, types and categorical values.
  - OpenSAFELY "doesn't allow direct access to individual patient records". The same command yields real data when run inside the secure environment.
  - Source: [OpenSAFELY dummy data how-to](https://docs.opensafely.org/ehrql/how-to/dummy-data/)
- **[documented]** OpenSAFELY outputs are released through "Airlock" after applying SDC and a review process. I read only the index page; the rules themselves were not read. [OpenSAFELY outputs](https://docs.opensafely.org/outputs/)

**Synthea**
- **[documented]** Synthea (Walonoski et al., JAMIA 25(3):230–238; online 30 Aug 2017, print March 2018), method:
  - It simulates lifespans from birth to death. Census data configures the population.
  - Disease and treatment logic are JSON state machines (the "Generic Module Framework"), evaluated each 7-day timestep.
  - It follows the **PADARSER** principle: publicly available data instead of real records. Sources include US Census, CDC prevalence and incidence, NIH reports, Global Burden of Disease, and clinical care maps and guidelines.
  - Where statistics were missing, transition probabilities were tuned to give realistic aggregates.
  - Source: [PMC7651916](https://pmc.ncbi.nlm.nih.gov/articles/PMC7651916/). I read this via a fetch summary of the full text.
- **[documented]** Synthea's initial validation covered only the type 2 diabetes modules.
  - Several outputs were far off, for example amputation and kidney-failure rates.
  - Probabilities were re-tuned, and reruns still under- or over-estimated some outcomes.
  - The authors limit it to non-clinical uses: software development, testing and training.
  - Known simplifications: perfect adherence, perfect clinicians, unlimited capacity, and no claims or financial data in the 2017 paper.
  - Source: [PMC7651916](https://pmc.ncbi.nlm.nih.gov/articles/PMC7651916/). The magnitudes came from the fetch summary, so re-check the exact figures before quoting them.
- **[documented]** Synthea today:
  - Requires JDK 17+. Defaults to Massachusetts Census demographics.
  - Exports FHIR R4/STU3/DSTU2, Bulk FHIR ndjson, C-CDA, CSV and CPCDS.
  - Last commit 2026-11-25. Very active.
  - Source: [synthetichealth/synthea README](https://raw.githubusercontent.com/synthetichealth/synthea/master/README.md)

**OMOP / Eunomia**
- **[documented]** Eunomia (OHDSI HADES):
  - A "standard dataset manager for sample OMOP CDM datasets" for testing and demos, including the Book of OHDSI exercises.
  - The default dataset is GiBleed in CDM v5.5, with 2,694 persons in the README example. It runs in R on SQLite.
  - CRAN 2.2.0, published 2026-10-12. Datasets are hosted in EunomiaDatasets (last commit 2026-10-07).
  - Sources: [OHDSI/Eunomia README](https://raw.githubusercontent.com/OHDSI/Eunomia/main/README.md); [crandb Eunomia](https://crandb.r-pkg.org/Eunomia); [OHDSI/EunomiaDatasets](https://github.com/OHDSI/EunomiaDatasets)

**CPRD (leads only)**
- **[lead]** CPRD/MHRA offers "high-fidelity" synthetic datasets (for example cardiovascular risk and COVID-19 symptoms) and a separate "medium-fidelity" CPRD Aurum sample. [UCL slides, P. Myles](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/6-puja-myles.pdf)
- **[lead]** The high-fidelity datasets are generated with Bayesian networks, or probabilistic graphical models, learned from real CPRD data and then sampled. [Tucker et al. 2020, PMC7653933](https://pmc.ncbi.nlm.nih.gov/articles/PMC7653933); [NHS AI Lab summary](https://transform.england.nhs.uk/ai-lab/explore-all-resources/develop-ai/practical-lessons-from-generating-synthetic-healthcare-data-with-bayesian-networks/)

### Inferences
- **[inferred]** Simulacrum is the closest published analogue to the platform constraint.
  - Statistics are computed **inside** the protected environment.
  - The **intermediate aggregate** artefact (data cubes, with a ≥50 threshold) is the thing judged safe, and was itself released.
  - Generation is sampling from those aggregates.
  - The **schema is kept identical** to production so that code is portable.
  - There is a **code-submission loop** with output checking.

  Transferable elements: a minimum-count threshold per aggregate cell, schema parity, and explicitly documenting what the stand-in does *not* reproduce (for example tumour linkage logic).
- **[inferred]** Strictly, Simulacrum cubes are derived from unit records, but only aggregates leave, which is exactly the platform's rule. Under CBS 2026 terms, the output is closer to "simulated data" (aggregate-driven) than to "synthetic data", although HDI calls it synthetic.
- **[inferred]** The OpenSAFELY pattern is the lowest-risk baseline:
  - Dummy data is generated from the *query or schema definition* (CBS "dummy data"; ONS level 1–2).
  - It is optionally overridden with hand-made fixtures, which are validated against the schema.

  A platform could combine schema-driven generation (always available) with aggregate-driven parameterisation (when released aggregates exist).
- **[inferred]** Synthea shows that knowledge-driven simulation from public statistics produces structurally rich, longitudinal, multi-table records with zero disclosure risk. Its aggregate fidelity can be badly off until it is validated against real aggregates. That validation step is itself an aggregates-only check that could run inside the protected environment.

### Gaps
- **[unreachable]** NHS England / NHS Digital "artificial data" service: digital.nhs.uk returned 403. I could not document how it is generated or what metadata leaves.
- **[unreachable]** The CPRD synthetic data page returned 403. The Tucker et al. CPRD-hosted preprint also returned 403. Only search leads exist.
- I did not read the Simulacrum white paper (Nov 2018) or the description of the v2.1.0 method change. I did not find the cube dimensions.
- I did not research the MIMIC demo or FDA/EMA positions.
- I did not verify the provenance of Eunomia's GiBleed dataset (whether it is Synthea-derived).
- I did not read OpenSAFELY's SDC rules for releases.

## Financial crime and transaction simulation: PaySim, BankSim, AMLSim, AMLworld

### Takeaway
All four tools are agent-based simulators driven by **parameter files that are themselves aggregates**.
- PaySim's phase-2 inputs were aggregated transaction logs: hourly count, sum, mean and standard deviation per transaction type, plus client-profile and balance histograms.
- BankSim used aggregated data from a Spanish bank.
- AMLSim takes degree distributions, account-group and typology specifications.
- AMLworld was calibrated to *public* aggregates (Federal Reserve, IRS, DoL) and its generator is **not** open-sourced.

PaySim (last commit 2021) and AMLSim (last commit 2022) are dormant, but their parameter-file designs transfer well.

### Cited Findings
- **[documented]** PaySim README:
  - Phase 1 used scenario predictions.
  - In phase 2 the team "got access to transactional financial logs of the system and developed a new version of the simulator which uses aggregated transactional data".
  - It is cited as Lopez-Rojas, Elmir & Axelsson, EMSS 2016.
  - Last commit 2021-05-30.
  - Source: [EdgarLopezPhD/PaySim README](https://raw.githubusercontent.com/EdgarLopezPhD/PaySim/master/README.md)
- **[documented]** PaySim parameter files (read from the repo):
  - `aggregatedTransactions.csv`: columns action, month, day, hour, count, sum, avg, std, step. Example: CASH_IN hour 1 has count 5189 and avg 155041.
  - `clientsProfiles.csv`: action, maxCount, minCount, averageAmount, stdAmount, freq.
  - `initialBalancesDistribution.csv`: binned percentages.
  - Also `overdraftLimits.csv`, `maxOccurrencesPerClient.csv` and typology graphs (`DrugNetworkOne.graphml`).
  - Properties include nbSteps=720, nbClients=20000, nbFraudsters=1000, nbMerchants=34749 and fraudProbability=0.001.
  - Source: [PaySim repo](https://github.com/EdgarLopezPhD/PaySim)
- **[lead]** NTNU 2017 chapter "Bootstrapping the PaySim Financial Simulator for Open Source": the parameter files "were initially extracted as aggregated information from the original data which is sensitive to share". The chapter bootstraps them from synthetic output so they can be shared. [NTNU Open](https://ntnuopen.ntnu.no/ntnu-xmlui/handle/11250/2588208)
- **[lead]** BankSim (Lopez-Rojas & Axelsson, EMSS 2014): its input is a sample of aggregated transactional data from a bank in Spain. The output contains no personal information. The calibration procedure was not seen. [EMSS 2014 proceeding](https://msc-les.org/proceedings/emss/emss2014/emss2014_144.html)
- **[documented]** AMLSim (IBM; Suzumura & Kanezashi):
  - A multi-agent AML simulator on Java 8 / MASON with Python graph generation. Python dependencies are pinned to old versions (networkx 1.11, matplotlib 2.2.3).
  - Inputs:
    - `accounts.csv`: count, min/max balance, country, business_type, bank_id.
    - `degree.csv`: in- and out-degree sequence.
    - `alertPatterns.csv`: count, type (fan_in, fan_out, cycle…), min/max accounts, min/max amount, min/max period, bank_id, is_sar.
    - `transactionType.csv`, and an `is_aggregated_accounts` flag.
  - Last commit 2022-02-14. Dormant.
  - Source: [IBM/AMLSim README](https://raw.githubusercontent.com/IBM/AMLSim/master/README.md)
- **[documented]** AMLworld paper, part 1: model and calibration (Altman et al., "Realistic Synthetic Financial Transactions for Anti-Money Laundering Models", arXiv 2306.16424, v1 22 Jun 2023, v3 25 Jan 2024).
  - Agents are individuals, corporations, partnerships, sole proprietors and banks. It models the full placement, layering and integration cycle, with 8 AMLSim typologies and 9 criminal-source types.
  - Realism is checked against public aggregates: Federal Reserve transactions per account and payment-format mix, IRS 2018 salary and pension data, 62.5% salaried (DoL participation) and 18.3% pension.
  - Laundering motif frequency is about 1 in 21,000, compared with the real-data figure of about 1 in 21,440 from Starnini et al.
  - Source: [arXiv HTML v3](https://arxiv.org/html/2306.16424v3)
- **[documented]** AMLworld paper, part 2: datasets, code and privacy argument.
  - Datasets come in Small, Medium and Large (5M–180M transactions) in HI and LI illicit-ratio variants.
  - "What we have open-sourced is a set of data – not the code to generate the data." The data are on Kaggle. The GNN code is in IBM/Multi-GNN (last commit 2024-02-13).
  - Privacy argument: no real transactions seed the generator.
  - Sources: [arXiv HTML v3](https://arxiv.org/html/2306.16424v3); [IBM/Multi-GNN](https://github.com/IBM/Multi-GNN)

### Inferences
- **[inferred]** The PaySim and AMLSim parameter-file pattern is a concrete, proven "characterisation format" that could leave a protected environment:
  - Time-bucketed count, sum, mean and standard deviation per event type.
  - Binned histograms of balances.
  - Per-profile frequency tables.
  - Degree distributions for relationship graphs.

  Each is an aggregate, can have small-cell suppression applied, and drives an entity-level simulator outside. The NTNU bootstrapping chapter shows that even these aggregates were treated as too sensitive to share openly, so SDC on the aggregates is still needed.
- **[inferred]** Degree-distribution files (AMLSim) are a direct template for characterising *relationships between entities*, such as how many accounts per customer or how many records per entity per source. Releasing in- and out-degree histograms is a compact aggregate that preserves graph shape.
- **[inferred]** Injected "typologies" (fan-in, cycle…) correspond to deliberately planted edge cases in test data. For the platform, the analogue is planted cross-source anomalies: conflicting identifiers, late-arriving records, duplicates.

### Gaps
- I did not read the full PaySim EMSS 2016 or BankSim EMSS 2014 papers. I did not verify the exact calibration procedure (which moments were matched, goodness-of-fit tests). I found no maintained BankSim repository.
- I did not confirm NeurIPS 2023 Datasets & Benchmarks acceptance from the text read: the arXiv text says "datasets and benchmarks" submission, and the remaining ~3% of the HTML was not read.

## Software test-data management: masking, subsetting and why they do not fit an aggregates-only rule

### Takeaway
TDM tools copy **real rows**, then mask them or take referentially intact subsets. Their output therefore contains transformed production data and cannot leave an aggregates-only protected environment. Their *techniques* still transfer: FK-graph traversal and topological ordering, deterministic hash-based transformations for cross-table consistency, and constraint-aware generation.

Maintained open-source tools: **Jailer**, **Greenmask**, **PostgreSQL Anonymizer** (all with commits in November 2026). **Condenser** is dormant (2023). **Neosync** was acquired by Grow Therapy and its repo states it is no longer actively maintained.

### Cited Findings
- **[documented]** Jailer:
  - Creates "referentially intact subsets of production databases". It exports topologically sorted SQL-DML, JSON, YAML, XML or DbUnit.
  - Works with any JDBC database. Now includes AI subsetting and query assistants.
  - Last commit 2026-11-24 (17.3.3.1).
  - Source: [Wisser/Jailer README](https://raw.githubusercontent.com/Wisser/Jailer/master/README.md)
- **[documented]** Greenmask:
  - Logical dump, anonymisation, synthetic generation and restore. PostgreSQL support is "production ready" and MySQL is in beta.
  - Subsetting handles cyclic and polymorphic references.
  - **Deterministic transformation** uses hash engines ("consistent output for the same input").
  - Dynamic parameters keep cross-column logic (for example `created_at < updated_at`). It also supports conditional transforms and transformation inheritance to partitions and FK references.
  - Last commit 2026-11-25.
  - Source: [GreenmaskIO/greenmask README](https://raw.githubusercontent.com/GreenmaskIO/greenmask/main/README.md)
- **[documented]** PostgreSQL Anonymizer (Dalibo):
  - Masking rules are declared in DDL ("anonymization by design").
  - Six methods: anonymous dumps, static, dynamic, replica masking, masking views and masking data wrappers.
  - Functions include randomisation, faking, partial scrambling, shuffling, noise and generalisation. It also offers PII detection.
  - Last commit 2026-11-25 on GitLab.
  - Source: [dalibo/postgresql_anonymizer](https://gitlab.com/dalibo/postgresql_anonymizer)
- **[documented]** Condenser (Tonic AI):
  - Config-driven subsetting for Postgres and MySQL from `initial_targets` (a percentage or a WHERE clause), with `dependency_breaks` for cycles.
  - It says it is good up to about 10 GB and points to a premium product for larger databases. **[vendor marketing]** for the premium claim.
  - Last commit 2023-05-18. Dormant.
  - Source: [TonicAI/condenser README](https://raw.githubusercontent.com/TonicAI/condenser/master/README.md)
- **[documented]** Neosync:
  - The README carries the disclaimer "Neosync has been acquired by Grow Therapy … this repository is no longer actively maintained".
  - Last commit 2025-08-30 ("adds acquired disclaimer").
  - Its stated use cases, before the acquisition, include "Safely test code against production data" and hydrating staging with "production-like data". **[vendor marketing]**
  - Source: [nucleuscloud/neosync README](https://raw.githubusercontent.com/nucleuscloud/neosync/main/README.md)

### Inferences
- **[inferred]** Why masking and subsetting fail an aggregates-only rule:
  - Every output row corresponds one-to-one to a real row.
  - Non-masked columns, row counts, join structure and rare combinations survive.
  - Deterministic masking preserves linkability by design.

  This makes the output "partially synthetic" or "hybrid" at best in CBS 2026 terms, which "retain the same number of units … having implications for disclosure risk". It is not derived aggregate information. For licensed reference data, redistributing masked copies may also breach licence terms (not verified against any licence).
- **[inferred]** Techniques that transfer to an aggregates-driven generator:
  - **FK-graph traversal with topological ordering** (Jailer, Condenser) for generating parent before child and emitting load-ordered fixtures.
  - **Deterministic keyed hashing** (Greenmask) to keep the *same synthetic entity* consistent across tables and across sources. This is useful for simulating several sources describing the same entity with different identifiers.
  - **Declarative per-column rules in the schema** (PostgreSQL Anonymizer) as a pattern for declaring generation rules next to the schema.
  - **Dynamic or conditional parameters** for cross-column constraints.
- **[inferred]** Masking tools could still run *inside* the protected environment to produce internal-only test copies. That fits the rule only if those copies never leave.

### Gaps
- I could not locate the "pg_subsetter" repository: candidate URLs were not found. Its status is unverified.
- I did not research Tonic or Delphix capabilities (commercial; reference only).

## Other fields, missed terms, and what transfers to a multi-source data platform

### Takeaway
I verified no other field in depth: geospatial small-area synthesis, smart-meter, telecom CDR, supply chain and education. Four things the brief does not name are worth adding:
1. **OpenSAFELY** and the wider **TRE / "code-to-data"** practice, with "dummy data" generated from the query definition.
2. The **CBS 2026 "simulated data" vs "synthetic data"** distinction.
3. The **ONS synthetic data spectrum** levels.
4. **Simulacrum-style "data cubes"** and **PaySim/AMLSim-style "parameter files"** as named forms of an aggregate characterisation.

### Cited Findings
- **[documented]** Terms found, with sources:
  - "simulated data", "dummy data", "arbitrary data", "random/fictitious data" and "hybrid data": [CBS 2026](https://www.cbs.nl/-/media/_pdf/2026/31/turner-et-al-2026-synthetic-data-terminology.pdf)
  - "synthetic structural/valid", "synthetically-augmented": [ONS WP16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)
  - "Testdaten" / test data for remote execution: [IAB SIAB](https://doku.iab.de/fdz/siab/SIAB_Testdaten_en.pdf)
  - "data cubes": [Simulacrum](https://simulacrum.healthdatainsight.org.uk/?p=3940)
  - "PADARSER" and "Generic Module Framework": [Synthea JAMIA](https://pmc.ncbi.nlm.nih.gov/articles/PMC7651916/)
  - "list balancing": [PopulationSim](https://activitysim.github.io/populationsim/)
  - "microsynthesis" and "quasirandom integer sampling": [humanleague](https://raw.githubusercontent.com/virgesmith/humanleague/main/README.md)
  - "dummy tables" and "Airlock": [OpenSAFELY](https://docs.opensafely.org/ehrql/how-to/dummy-data/)
  - "parameter files" and "typologies": [PaySim repo](https://github.com/EdgarLopezPhD/PaySim)
  - "data entrepreneurs' synthetic PUF": [CMS](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf)
- **[documented]** A mature open-source reference for model-based multi-table synthesis from real data (out of scope here, because it trains on real rows): SDV, PyPI 2.2.0 uploaded 2026-11-06. [PyPI sdv](https://pypi.org/pypi/sdv/json)

### Inferences
- **[inferred]** A cross-field pattern for the platform, with a source for each step:
  1. Keep the stand-in's schema identical to production (Simulacrum, OpenSAFELY, DE-SynPUF "programs should work on LDS").
  2. Generate a baseline from schema and metadata alone (OpenSAFELY dummy data; ONS levels 1–2).
  3. Compute an SDC-checked aggregate characterisation inside the protected environment. Forms include marginal and joint tables with a minimum cell count (Simulacrum ≥50), time-bucketed count/sum/mean/sd (PaySim), and degree or cardinality histograms (AMLSim). Review it as the release artefact (CBS 2026).
  4. Outside, fit an entity-level population to those aggregates with IPF, entropy list balancing or QIS, and integerise (PopulationSim, humanleague).
  5. Add knowledge-driven event or state-machine logic for behaviour over time (Synthea modules, PaySim/AMLSim agents).
  6. Plant deliberate edge cases, both typologies and category coverage (AMLSim alert patterns; IAB "every value at least once").
  7. Validate by running the same aggregate queries on the stand-in and, inside the protected environment, on the real data, then compare (Synthea's validation; Simulacrum's code loop).
  8. Gate code promotion: code must run on the stand-in before submission (IAB; NCRAS).
- **[inferred]** **Multi-source entity overlap is not directly covered by any tool found.** That means several sources describing the same entities with different identifiers, coverage and delays. The nearest techniques are:
  - Greenmask's deterministic hashing, for consistent identities across tables.
  - SIAB test data keeping episode ordering and overlap across data sources.
  - Simulacrum's patient-level linkage between registry and SACT tables, with its documented failure to reproduce real tumour linkage.

  A platform would need to release *overlap aggregates*, such as the share of entities present in each pair of sources, the identifier-mismatch rates and the delay distributions per source. This is an inference, not a found method.
- **[inferred]** Agent-based or event simulation (Synthea, PaySim, AMLworld) gives realistic *temporal and relational* behaviour. Its realism depends on calibration effort, and CBS 2026 argues proper calibration needs unit-level access. In an aggregates-only setting, the calibration loop must be: run the comparison inside, release only the fit statistics.

### Gaps
- I did not research geospatial or census small-area synthetic data beyond microsimulation tools, nor energy smart-meter, telecom CDR, supply-chain simulators, data "digital twins" or education data. No claims are made. They are candidates for a follow-up only if a transferable method is needed.
- I did not verify Statistics Netherlands RA, DST, ABS DataLab or ONS SRS dummy-file practice.
