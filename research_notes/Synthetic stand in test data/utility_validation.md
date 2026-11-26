# Utility validation for synthetic stand-in data: validation and verification servers, utility metrics, workload comparison, shadow runs

Labels used throughout: **[documented]** means the full text or primary page was read. **[lead]** means only a search extract or abstract was seen, so verdicts must not rest on it. **[inferred]** is my reasoning. **[vendor marketing]** is a vendor claim. **[unreachable]** means the source could not be fetched from this session.

Access notes for the report writer:
- **Unreachable hosts.** www2.vrdc.cornell.edu (Cornell Synthetic Data Server page) did not resolve, so the network policy blocks it. dsl.cds.iisc.ac.in (Hydra papers) gave curl code 000 and WebFetch 503. assets.fcsm.gov (Tyagi 2024 FCSM deck) gave code 000.
- **Partly unreachable.** The Urban Institute landing pages loaded, but the white-paper PDFs did not.
- **GitHub API unavailable.** The GitHub API was blocked for these repos (HTTP 403, repository not enabled). Maintenance state therefore comes from PyPI and CRAN release metadata (fetched 2026-11-26) and from README files on raw.githubusercontent.com.

## Q1. Official-statistics practice: how is "develop on synthetic, run on real, release checked results" actually run?

### Takeaway
The workflow is long-established but staff-heavy and fragile:
- **The basic loop.** Analysts write code on a public or low-barrier synthetic file with the same structure as the confidential file. Agency staff run that code inside on the confidential "gold standard" file. Only disclosure-reviewed outputs come back, by email, after days to weeks.
- **US status.** The flagship US services are paused (SIPP Synthetic Beta, SSB) or were moved off Cornell's Synthetic Data Server, which ended in September 2022. Urban Institute's validation server aims to automate disclosure review with differential privacy, and is still a prototype (v2.0, September 2024).
- **UK status.** UK pilots (ONS, ADR UK) use low-fidelity synthetic data to prepare code for the Secure Research Service, with no formal validation step.
- **Utility verdicts.** Where utility on real data was actually measured, for example the SynLBD model transplanted to Canada and Germany, standard metrics showed significant differences. Code-portability value and inferential-validity value are separate questions.

### Cited Findings

**US Census Bureau: SIPP Synthetic Beta (SSB)** — [Census SSB page](https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html), last revised 17 Nov 2026 [documented]
- **Status.** "The SIPP Synthetic Beta (SSB) is temporarily on pause". No resumption date is given.
- **Content.** The current version is 7.0 (Dec 2018), with administrative records through 2014. The SSB links SIPP respondents to SSA and IRS W-2 and benefit records.
- **Access.** Approval depends only on whether the file holds the variables needed. Census "generally expects to be able to approve applications within five business days". The file is delivered over SecureFTP as four files of about 3–4 GB in SAS or Stata format.
- **Validation workflow.** Users are strongly urged "not to publish results produced from the SSB without first requesting" validation.
  - Census staff run the submitted program on the confidential *Completed Gold Standard File*, on internal Census computers. The service is free "as resources permit".
  - Programs must already run without error on the synthetic file. They must be SAS 9.4 M8 or Stata/SE 18.0 compatible and use Linux paths.
  - The user files a Clearance Request Memo describing the output they want, then uploads through a send-a-file link. Uploads are processed twice a month.
  - Output must follow Census disclosure rules and rounding rules, and is reviewed by Census staff.
  - Released products are reported to ORES/SSA and SOI/IRS.
  - Turnaround is "as little as 7 business days" for clean, simple code. Errors, small samples or an incomplete memo cause longer delays.
- **Contradiction to reconcile.** Barrientos et al. (2023) say that "until September 2022" the Census Bureau validated analyses for SynLBD and SSB "via the Synthetic Data Server at Cornell University" — [arXiv 2110.12055v3, 30 Jun 2023](https://arxiv.org/pdf/2110.12055v3.pdf) [documented]. The current Census page instead describes direct SecureFTP distribution and in-house validation. **[inferred]** Cornell's SDS stopped being the access route in 2022, Census took distribution and validation in-house, and that service is now paused. The Cornell SDS page itself is [unreachable].

**US Census Bureau: Synthetic Longitudinal Business Database (SynLBD)**
- **Validation guidance.** "The SynLBD has not been fully validated". "Unless validated, there is no guarantee results from the SynLBD reflect results from the underlying confidential data". Researchers are "strongly encouraged to request result validation". Validation "Is free, as resources permit" and "Follows established protocol" — [Census SynLBD Analytic Validity, rev. 12 Feb 2025](https://www.census.gov/programs-surveys/ces/data/public-use-data/synthetic-longitudinal-business-database/analytic-validity.html) [documented]
- **History.** SynLBD was released in 2011 to "an easily web-accessible computing environment (Abowd and Vilhuber 2010), and combined with a validation mechanism … a remotely accessible data server, combined with a validation server". Researchers "can later validate their model-based inferences on the full confidential microdata" — [Alam, Dostie, Drechsler, Vilhuber 2020](https://zenodo.org/records/3832173/files/AlamDostieDrechslerVilhuber_20200518.pdf) [documented]
- **Older archived page.** An archived SynLBD "validating results" page exists at [UNT web archive, 2013](https://webarchive.library.unt.edu/web/20130226000932/http:/www.census.gov/ces/dataproducts/synlbd/validatingresults.html) [lead; not read]

**Statistics Canada and IAB Germany: SynLBD model transplanted** — [Alam et al., 18 May 2020](https://zenodo.org/records/3832173/files/AlamDostieDrechslerVilhuber_20200518.pdf) [documented]
- **Experiment.** The exact SynLBD synthesis code was applied to Canada's LEAP and Germany's Establishment History Panel (BHP). "All results were reviewed for disclosure risks by their respective custodians, and released to the authors." This is a real instance of utility computed inside and only reviewed results exported.
- **Canadian access route.** CDER at Statistics Canada (created 2011) uses "limits on tabular outputs, centralized vetting, monitoring of program logs". Its interface means "actual observations cannot be viewed".
- **German access route.** IAB business data are onsite-only, after ministry approval.
- **Utility checks used.** Univariate time series (employment, entry and exit rates, job creation and destruction), distributions by industry over time, a dynamic panel growth model, confidence-interval overlap (CIO) and pMSE.
- **CIO is useless at scale.** CIO was computed but "not … useful". With millions of records, "confidence intervals (almost) never overlap even when the estimates … are quite close."
- **pMSE always rejects at scale.** pMSE was 0.0121 for Canada (0.0041 for manufacturing) and 0.0013 for Germany. The pMSE ratios (657 to 10,958) and standardized pMSE (2,897 to 135,526) are huge. "The expected pMSE is quite sensitive to sample size N … it is quite likely to reject the null of equivalence given this test's very high power."
- **Conclusion.** "Utility evaluations show significant differences between each country's synthetic and confidential data … the synthetic data do not reliably lead to the same modeling decisions." The German data did better, possibly because it covered fewer and larger industries.

**Urban Institute and Tax Policy Center: synthetic tax PUF plus validation server**
- **2018 proposal** — [Burman et al., TPC, 2018, presented at the IRS/TPC conference on 20 Jun 2018](https://www.taxpolicycenter.org/sites/default/files/publication/156011/safely_expanding_research_access_to_administrative_tax_data_creating_a_synthetic_public_use_file_and_a_validation_server_0.pdf) [documented]
  - Researchers would "submit statistical programs to run on a subset of the confidential administrative data … The structure of the administrative dataset would be the same as for the synthetic data, so programs that are developed using the PUF would work on the confidential data with minimal alteration. The IRS would review programs and output".
  - The proposal includes a fee "to defray costs and discourage data mining" and draws on a "privacy budget" concept: "Once exhausted, no further queries are permitted."
  - **Specific utility by workload.** The team would run the Tax Policy Center microsimulation model on the synthetic PUF, the INSOLE and the current PUF. They would compare revenue, marginal tax rates and burden distributions using "confidence interval overlap, confidence interval length ratios, and difference in means". This is a clear example of evaluating utility by running a production workload on both data sets.
- **Validation server prototypes.** v1 is "A Privacy-Preserving Validation Server Prototype" (Taylor, MacDonald, Ueyama, Bowen; 30 Sep 2021). v2.0 is by Tyagi, Taylor, MacDonald, Tamaroff, Miller, Williams, Bowen (11 Sep 2024). It aims to offer "a testable solution to government agencies" that would "improve and automate statistical disclosure control" — [Urban v1](https://www.urban.org/research/publication/privacy-preserving-validation-server-prototype), [Urban v2](https://www.urban.org/research/publication/privacy-preserving-validation-server-version-2) [landing pages documented; PDFs not retrieved, so architecture details are unverified]
- **Feasibility of DP queries** — [Barrientos, Williams, Snoke, Bowen, arXiv 2110.12055v3, 30 Jun 2023](https://arxiv.org/pdf/2110.12055v3.pdf) [documented]
  - A validation server "allows users to submit and run statistical queries on the confidential (validation) data after the users have developed their queries using theory or public data".
  - Today "agency staff must still review the queries for disclosure risks, which can delay releasing the results". DP composition "could use the privacy-loss accounting … to replace manual review".
  - **Finding:** "DP methods are feasible for simple, univariate statistics but struggle to produce accurate regression estimates and confidence intervals".
  - **Terminology.** Validation servers are distinguished from *verification servers*, "which allow users to verify public data estimates against the confidential data without return[ing] confidential estimates" (citing Barrientos et al. 2018).
- **2024 programme overviews.** A 2024 IRS SOI overview by MacDonald describes the three-tier design (synthetic data for code development plus a validation server) — [IRS 2024 deck](https://irs.gov/pub/irs-soi/24conpan-validation-server-overview-mcdonald.pdf) [lead: WebFetch returned 404; the search extract said a researcher "can analyze confidential data without seeing them"]. A Survey of Earned Doctorates synthetic-data project, led by Urban, mentions specific-utility metrics and validation — [America's DataHub](https://americasdatahub.org/?p=2899) [lead].

**Verification measures**
- Lin and Reiter (3 Apr 2024) define verification measures as gauges of how similar an analyst's synthetic-data estimates are to the confidential ones. They "leak information about the confidential records", so agencies "may wish to apply disclosure control". The paper gives a DP verification measure for survey-weighted totals and means under complex designs — [arXiv 2404.02519](https://arxiv.org/abs/2404.02519) [abstract documented]
- **[inferred]** For the platform, a verification measure is the minimal kind of export. It is a bounded score, for example "the synthetic-data estimate falls within X% of the real estimate" or a CI-overlap fraction, rather than the real estimate itself.

**UK: ONS and ADR UK**
- **ONS Methodology Working Paper 16, synthetic data pilot** — [ONS](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot) (undated; case-study data are 2017 Q2 LFS) [documented]
  - Defines a six-level fidelity spectrum:
    1. Structural
    2. Valid
    3. Plausible
    4. Multivariate plausible
    5. Multivariate detailed
    6. Replica
  - Levels 1 and 2 are meant "for code testing".
  - The prototype LFS file has 88,801 records and was built with synthpop CART, targeting level 2 to 3. Its geography was assigned at random.
  - Its purpose is to let researchers "develop code in advance" before Secure Research Service (SRS) access.
  - No user validation step and no quantitative utility results are reported. Verification servers are mentioned only in general terms.
- **LEO synthetic data, ADR UK blog** — [ADR UK, 14 Apr 2026](https://www.adruk.org/news-publications/news-blogs/longitudinal-education-outcomes-synthetic-data-what-is-it-and-why-is-it-useful-1/) [documented]
  - A "small synthetic (or 'dummy') version" with all tables and most variable names. It keeps averages, medians and missingness shares.
  - The real data "inside the SRS is only available via SQL server" while the synthetic data come as files, so code may need adapting.
  - The authors admit it "is not perfect". There is no formal validation; feedback goes to the LEO team.
  - **[inferred]** This is a cautionary example: a format mismatch between the synthetic file and the protected source undermines the "same code runs inside" premise.
- **Other UK leads** [lead]: [UKDS: evaluating benefits, costs and utility of synthetic data](https://ukdataservice.ac.uk/about/research-and-development/evaluating-the-benefits-costs-and-utility-of-synthetic-data/); an ADR UK/ESRC call of up to £375k to evaluate uptake and utility of synthetic data in TREs; and the ASHE synthetic pilot. None was read in full.

### Inferences
- **The pattern that recurs.** Every official-statistics scheme found has the same three parts:
  1. A structure-identical synthetic file.
  2. Code that must run cleanly on the synthetic file first.
  3. Staff (or, prospectively, DP-automated) execution inside, with output checking before release.

  The cost driver is manual output review. That is why Urban pursues DP automation, and why Census turnaround is weeks with twice-monthly batches.
- **What the platform can borrow.** For the platform, "staff" can be an automated CI job inside the protected environment running a pinned pipeline version. Output checking can be rule-based for a fixed, pre-approved set of summary shapes: counts, rates and quantiles with thresholds and rounding. This is easier than research validation because the workload is known in advance [inferred].
- **Metrics at platform scale.** The CIO and pMSE problems at millions of rows (Alam et al.) mean hypothesis-test utility metrics will always "fail" at platform scale. Use effect-size metrics instead (absolute or relative difference, Q-error, TVD), with tolerances agreed in advance [inferred from documented finding].

### Gaps
- Eurostat: no primary source found on synthetic data plus validation practice. I searched only lightly; this is not a confirmed absence.
- Statistics Canada: beyond the CDER and LEAP experiment (Alam et al.), no StatCan-run validation or verification service was found.
- Cornell SDS documentation and the exact 2022 end of SDS-based validation are [unreachable] or second-hand only (Barrientos et al. 2023).
- Urban validation server v1 and v2 architecture is not verified, because the PDFs and the FCSM 2024 deck were unreachable. That covers what is submitted, the tech stack, DP mechanisms and per-query budget.
- Barrientos et al. (2018), the verification server for US federal employees data, was not read.

## Q2. Utility metrics and tools: which need real rows side by side (run inside) and which need only aggregates?

### Takeaway
- **General vs specific utility.** The literature splits utility into *general* utility (distributional similarity, for example pMSE) and *specific* utility (similarity of the results of particular analyses, for example CI overlap of fitted-model coefficients) — [Snoke et al. 2016/2018](https://arxiv.org/abs/1604.06651).
- **Every major OSS tool expects real and synthetic data frames together**, so as packaged it must run inside the protected environment. These are SDMetrics, SynthEval, synthcity, Urban's syntheval, synthpop and SDNist.
- **Which metrics survive an aggregate-only export.** Metrics that are functions of low-order marginals or of model outputs can be computed outside if the real-side aggregates are exported. These are TVD and Hellinger on categorical counts, k-way marginal error, utility.tab-style table pMSE, quantile and moment differences, correlation matrices, and CI overlap from (estimate, SE).
- **Metrics that need inside execution.** Classifier-based pMSE and detection, MMD, PCA, nearest-neighbour distances, KS on raw continuous values, and TSTR need row-level co-location.

### Cited Findings
- **Definitions** — [Snoke, Raab, Nowok, Dibben, Slavkovic, arXiv 1604.06651, v2 19 Jun 2017](https://arxiv.org/abs/1604.06651) [abstract documented]
  - General utility asks whether synthetic data "have a distribution that is comparable to that of the original data".
  - Specific utility is "the similarity of results of analyses from the synthetic data and the original data".
  - The paper adapts pMSE to synthetic data and derives its null distribution.
- **synthpop (R)** — [Raab, Nowok, Dibben, synthpop utility vignette, 10 Sep 2026](https://cran.r-project.org/web/packages/synthpop/vignettes/utility.pdf) [documented]; CRAN version 1.9-3, published 10 Sep 2026, maintainer B. Nowok — [crandb](https://crandb.r-pkg.org/synthpop)
  - `utility.gen()` fits a propensity model (logistic or CART) on stacked original plus synthetic rows. It needs both datasets at row level.
  - `utility.tab()` and `utility.tables()` compare one-way, two-way and three-way tables of original and synthetic data and report pMSE, S_pMSE and other table statistics.
  - "Comparing tables of original and synthetic data can be framed as a prediction model, where the propensity score for records in each cell is the ratio of the synthetic counts to the sum of the original and synthetic counts. For synthetic data where all variables are categorical, a comparison of n-way tables is equivalent to fitting a propensity score model by logistic regression including all interactions up to order n."
  - `compare()` gives per-variable plots plus S_pMSE.
  - **[inferred]** Table-based utility can in principle be computed from exported cross-tabulations of the real data, an aggregate-only export. The function's API as written takes the original data frame, though.
- **SDMetrics (DataCebo/SDV)** [documented, README]; PyPI 0.33.1, uploaded 25 Nov 2026 (active); README badge says "Development Status 2 - Pre-Alpha" — [README](https://raw.githubusercontent.com/sdv-dev/SDMetrics/main/README.md), [PyPI](https://pypi.org/project/sdmetrics/)
  - "Evaluates synthetic data by comparing it to the real data". `QualityReport().generate(real_data, synthetic_data, metadata)` gives Column Shapes and Column Pair Trends scores.
  - Single metrics include `BoundaryAdherence(real_col, synth_col)` and `NewRowSynthesis`.
  - Reports can be saved as .pkl "and share[d] with your team".
  - **[inferred]** The pickled report contains derived scores. It should be inspected before export, because a pickle may carry more than intended.
  - **Licence:** SDV/SDMetrics use the Business Source License, which is not OSI open source [inferred from prior knowledge; licence field empty on PyPI, so verify].
- **SynthEval (Lautrup et al.)** — [README](https://raw.githubusercontent.com/schneiderkamplab/syntheval/main/README.md) [documented]; paper in Data Mining and Knowledge Discovery 39(1), 2024; PyPI 1.7.3, 23 Oct 2026 (active)
  - Requires `df_real`, an optional holdout and `df_fake` with identical columns. A CLI takes real and synthetic CSV paths.
  - **Utility metrics:** dimension-wise means, PCA, CI overlap (`cio`), correlation-matrix difference, mutual-information difference, KS and TVD, Hellinger, pMSE, AUROC difference, classification accuracy (TRTR/TSTR), feature-importance overlap, quantile MSE and MMD.
  - **Privacy metrics:** NNDR, DCR, hitting rate, epsilon-identifiability, MIA and attribute disclosure.
  - **Fairness metric:** statistical parity.
- **synthcity (van der Schaar lab)** — [README](https://raw.githubusercontent.com/vanderschaarlab/synthcity/main/README.md) [documented]; PyPI 0.2.12, 8 May 2025, Apache-2.0. **[inferred]** Maintenance has slowed, with no release for about 18 months.
  - Statistical metrics: Jensen–Shannon, Wasserstein, PRDC and alpha-precision/beta-recall/authenticity.
  - Performance (TSTR-style) metrics: XGB, linear and MLP.
  - Detection metrics: GMM, XGB, MLP and linear classifiers that "differentiate the synthetic data from the real data".
- **Urban Institute `syntheval` (R)** — [README](https://raw.githubusercontent.com/UrbanInstitute/syntheval/main/README.md) [documented]; GitHub-only install ("still under active development before we release our first major version, 0.1.0"); companion `tidysynthesis` on CRAN 0.1.3, 16 Mar 2026, maintainer A. R. Williams (Urban) — [crandb](https://crandb.r-pkg.org/tidysynthesis)
  - Core input is `eval_data(conf_data=…, synth_data=…)`.
  - Metrics: proportions, means and totals, percentiles, KS distance, co-occurrence, correlations, coefficient overlap and discriminant-based metrics, with grouping and weighting.
- **NIST SDNist v2.5, "Deidentified Data Report Tool"** — [README](https://raw.githubusercontent.com/usnistgov/SDNist/main/README.md) [documented]; PyPI latest is 2.4 (2 Feb 2024) while the README says v2.5, so v2.5 is on GitHub release only [inferred]. The README says "being actively developed" and the project is the official package for the NIST Collaborative Research Cycle (CRC).
  - **Constraint:** "This version of SDNist only supports using the NIST ACS Data Excerpts". It is a benchmark harness, not a general tool for arbitrary schemas.
  - **[inferred]** It is useful as a reference report layout (k-marginal scores, pairwise correlations, PCA, linear-regression comparisons, privacy checks), not as a drop-in.
- **Anonymeter** — [README](https://raw.githubusercontent.com/statice/anonymeter/main/README.md) [README fetched; summary from PyPI]
  - Privacy only: singling-out, linkability and inference risk. PyPI 1.1.0, 23 Jul 2026, Clear BSD licence, with Anonos IP LLC as copyright holder.
  - Out of scope for utility. It also needs real rows inside.
- **SynthGauge (UK ONS Data Science Campus)** — [PyPI](https://pypi.org/project/synthgauge/) [metadata only]
  - Evaluation package, last release 2.2.0 on 12 Oct 2022. **[inferred]** Stale.
- **TabSynDex** — no PyPI package found [gap]. The single-score index is from Chundawat et al. 2022 (not read).
- **pMSE weaknesses at scale** are documented in Alam et al. 2020 (see Q1).

### Inferences
Table: what must leave the protected environment, per metric family [inferred, built from documented metric definitions].

| Metric family | Inputs from the real side | Can run outside with an aggregate export? |
|---|---|---|
| Per-marginal TVD and Hellinger (categorical); k-way marginal error (NIST-style) | Counts per cell of 1-, 2- or k-way tables | Yes. Export cell counts with small-cell suppression or noise. |
| synthpop `utility.tab` table pMSE and S_pMSE | Same n-way counts | Yes, mathematically. The API needs adapting. |
| KS and Wasserstein (continuous) | The full empirical CDF, or a quantile sketch | Approximately, from exported deciles or percentiles or a binned histogram (Wasserstein on bins). Exact KS needs raw values. |
| Moments, quantiles, missingness rates, distinct counts | Scalars | Yes. |
| Correlation, mutual-information and co-occurrence matrices | Pairwise statistics | Yes. |
| CI overlap and coefficient overlap (specific utility) | (estimate, SE) per coefficient from the same model run inside | Yes. This is the validation-server pattern. |
| Verification measure (Lin and Reiter) | A bounded similarity score only | Yes. It leaks least. |
| Classifier pMSE, detection, MMD, PCA, PRDC, alpha-precision | Real rows co-located with synthetic rows | No. Run inside and export only the score. |
| DCR, NNDR, MIA, Anonymeter (privacy) | Real rows | No. Run inside. |
| TSTR / ML efficacy | Real holdout rows | No. Run inside. |

- **Practical design.** Run SynthEval, SDMetrics or syntheval inside on (real, synthetic) and export only the scalar scores and per-column scores. Separately export a fixed "characterisation" of low-order marginals, which other researchers cover, so the outside team can track drift without re-entering.
- **Licensing.** Prefer SynthEval (BSD-style? verify), synthpop (GPL) or Urban syntheval for permissive or open licences. SDMetrics carries BSL constraints [inferred; verify licences].

### Gaps
- SynthEval's and Urban syntheval's licences were not verified, and neither was SDMetrics' exact current licence.
- TabSynDex: no implementation or maintenance state found.
- I did not verify whether any tool natively accepts aggregate-only real-side inputs. None of the READMEs read suggests so.

## Q3. Workload-based usefulness for a data platform: query results, cardinalities, plans and performance

### Takeaway
- **Database research measures realism by running a workload on both databases.** The workload-preserving generators QAGen, Touchstone, Hydra and SAM are judged by comparing per-query (often per-operator) cardinalities, Q-error on held-out queries, and query latency between the real and synthetic database.
- **Hydra-style systems explicitly ship only annotated query plans and metadata, no data, out of the client site.** This maps directly onto the platform's "only derived information leaves" constraint.
- **Benchmark-realism work shows uniform, independent generators make optimisers look unrealistically good.** Leis et al. show that TPC-style generators share the optimiser's own uniformity and independence assumptions. Vogelsgesang et al. show that real BI data differ, for example with string keys and skew.
- So hand-written or naive synthetic test data will systematically understate performance and correctness problems.

### Cited Findings
- **Leis, Gubichev, Mirchev, Boncz, Kemper, Neumann, "How Good Are Query Optimizers, Really?"** — [PVLDB 9(3), 2015](https://www.vldb.org/pvldb/vol9/p204-leis.pdf) [documented]
  - TPC-H, TPC-DS and SSB "are not good benchmarks for the cardinality estimation component of query optimizers … the data generators are using the very same simplifying assumptions (uniformity, independence, principle of inclusion) that query optimizers make. Real-world data sets, in contrast, are full of correlations and non-uniform data distributions".
  - "PostgreSQL's simple cardinality estimator indeed works unrealistically well for TPC-H." "Clearly, the TPC-H query workload does not present many hard challenges for cardinality estimators. In contrast, our workload contains queries that routinely lead to severe overestimation and underestimation errors".
  - The paper introduced JOB on IMDB (21 tables, 3.6 GB, May 2013 snapshot).
- **Vogelsgesang et al., "Get Real: How Benchmarks Fail to Represent the Real World"** — [DBTest 2018](https://cs.cit.tum.de/fileadmin/w00cfj/dis/papers/getreal.pdf) [lead: PDF download failed to parse; facts from search extract]
  - The study analysed more than 60k Tableau BI repositories and more than 1M generated queries.
  - Findings: TPC-H uses integer keys while real data "mostly features strings as keys", and "75% of the queries are metadata queries".
- **SAM, Yang, Wu, Cong, Zhang, He** — [SIGMOD 2022, pp. 1542–1555, author camera-ready](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf) [documented]; code at github.com/Jamesyang2333/SAM (not checked)
  - **Motivation.** Cloud providers "may need to benchmark DBMS without access to the underlying data". They "leverage a query workload, which contains a set of queries and the corresponding cardinalities, to generate a synthetic database with similar query performance."
  - **Evaluation (A1, fidelity).** Q-error of the input-query cardinalities on the generated versus the original database. For IMDB this was measured on 1,000 sampled constraints out of a 100K workload.
  - **Evaluation (A2, closeness).** Cross-entropy against the original, and Q-error on an *independent test query set*, which "measures how well the generated database recovers the joint data distribution and generalizes to unseen queries".
  - **Performance deviation.** "Performance deviation is defined as the difference in query latency between the synthetic database and the original database". It was measured on PostgreSQL 12.0, with JOB-light (70 queries, up to 5-way joins) as the test set for IMDB.
  - **Baseline:** PGM-based generation.
- **Hydra and HF-Hydra (IISc DSL: Sanghi, Haritsa et al.)** [lead: papers unreachable; based on search extracts of the TR-2017-01, EDBT 2018, PVLDB 11(12) 2018 demo and TR-2021-01]
  - Workload-dependent regeneration makes a synthetic database that behaves like the client's on a known workload.
  - Each plan operator's output is annotated with its row cardinality ("volumetric similarity"). The generator satisfies these cardinality constraints using LP over region partitions.
  - Plan equivalence is a *precondition*, ensured via plan forcing or metadata matching, not something verified.
  - A tiny workload-dependent "database summary" generates data of any size on the fly. A reported example is 100 GB TPC-DS from 131 queries.
  - Sources: [Hydra project page](https://dsl.cds.iisc.ac.in/projects/HYDRA/), [EDBT 2018 PDF](https://dsl.cds.iisc.ac.in/publications/conference/hydra_edbt.pdf), [TR-2021-01 HF-Hydra](https://dsl.cds.iisc.ac.in/publications/report/TR/TR-2021-01.pdf) [all unreachable from this session]
- **Touchstone, Li, Zhang, Yang, Zhang, Zhou** — [USENIX ATC 2018, pp. 575–586](https://www.usenix.org/conference/atc18/presentation/li-yuming) [lead: abstract only]
  - Query-aware generation that satisfies query cardinality constraints. It reports about 1000x speed-up on TPC-H "without losing accuracy".
  - A TKDE 2022 extension adds outer and non-equi joins.
  - A 2023 Berkeley report (ezGen) says Touchstone fails on some real-world application workloads and complex queries — [EECS-2023-124](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2023/EECS-2023-124.html) [lead]
- **Mirage, PilotScope, Amazon Redset "Why TPC is not enough" (VLDB 2024)**: not researched in this track [gap].

### Inferences
- **Direct analogue for the platform.** Per-operator cardinality annotation (Hydra) and per-query cardinality plus Q-error (SAM) correspond to *row counts per pipeline stage* and *per-step selectivities*. Examples are rows in, rows after a filter, rows after a join and rows rejected. These are exactly the derived aggregates the platform may export.

  Proposed workload-fidelity vector, computed by running the same pipeline version inside on real data and outside on synthetic data [inferred]:
  1. Row counts per stage and per source; Q-error between real and synthetic per stage.
  2. Data-quality rule outcomes, as the pass/fail rate per rule per source.
  3. Join match rates per join key and per source pair, including unmatched-left and unmatched-right shares. This matters given multiple sources with their own identifiers and coverage.
  4. Entity-resolution statistics: candidate-pair counts after blocking, match/non-match/possible counts, cluster-size distribution, and the share of entities seen in 1, 2 or k sources.
  5. Reject and error rates by error type.
  6. Lateness and delay distributions per source (arrival lag quantiles).
  7. Performance: plan shape hashes, or join order and operator types; execution time per stage; peak memory; spill bytes; shuffle sizes. Compare on a normalised basis, for example time per million rows, because hardware differs.
- **Q-error as the default fidelity metric.** Q-error, max(a/b, b/a), is a good scale-free fidelity metric for counts and rates and avoids the pMSE/CIO scale problem. Thresholds should be set per stage [inferred].
- **Synthetic data shaped by the stage-wise aggregates.** Since Hydra and SAM *generate* data from such cardinality annotations, the exported stage-wise aggregates can feed the next synthesis round, not only validate it. This closes a loop analogous to Abowd and Schmutte's idea of improving synthetic files from submitted programs, which Burman et al. (2018) cite as possibly infeasible computationally [inferred plus documented citation].
- **Plan equivalence is an assumption, not a check.** Plan equivalence should be checked explicitly, by exporting EXPLAIN plan fingerprints from inside, not assumed (Hydra assumes it) [inferred].

### Gaps
- No full text was read for Hydra or HF-Hydra, Touchstone or Get Real. Their claims are leads only.
- No paper was found that evaluates synthetic data for *ETL or entity-resolution pipelines* with stage-wise metrics. The vector above is my construction.
- Maintenance state of the Touchstone, Hydra and SAM code was not checked (GitHub API blocked). These are research prototypes, and active maintenance is unlikely [inferred].

## Q4. Differential testing and shadow runs: same pipeline inside on real data and outside on synthetic data; what summaries are safe to export

### Takeaway
- **No documented engineering-blog source was read** that describes running a data pipeline on real data inside a protected zone and on synthetic data outside, then comparing exported summaries.
- **What industry practice was found is shadow or parallel runs on production data**, comparing old and new pipeline outputs. Examples are Segment's row-parity comparison, Yelp's staging pipeline, Totango's shadow diff gate and Twitter's Diffy. That is *version-vs-version on real data* rather than *real-vs-synthetic*, and all were seen only as search leads.
- **The official-statistics validation-server pattern is the closest documented analogue.** The required ingredients are: identical code, identical schema, inside execution, and output checking of summaries, with optional DP or verification-measure output.

### Cited Findings
- **Validation servers** run user-developed code on confidential data and return disclosure-checked outputs (Census SSB, Burman et al. 2018, Barrientos et al. 2023; see Q1) [documented].
- **Verification servers** return only a similarity indicator, never the confidential estimate (Barrientos et al. 2023 footnote). Lin and Reiter note verification measures still leak, and give a DP version [documented; arXiv abstract].
- **DP for summaries.** DP is "feasible for simple, univariate statistics" but struggles for regressions and CIs — [Barrientos et al. 2023](https://arxiv.org/pdf/2110.12055v3.pdf) [documented]. **[inferred]** This favours exporting counts, rates and quantiles, which are the kind of summaries a pipeline test needs, over model outputs.
- **Industry shadow and parity testing** [lead only; not read]:
  - Segment, "Comparing billions of rows per day": row-by-row parity between old and new pipeline. The URL now redirects to a Twilio blog index, so it is [unreachable] at the original URL — [segment.com](https://segment.com/blog/comparing-billions-of-rows-per-day)
  - Yelp Engineering (May 2025): staging pipeline running alongside production on production data — [Yelp](https://engineeringblog.yelp.com/2025/05/revenue-automation-series-testing-an-integration-with-third-party-system.html)
  - Totango slides: shadow-mode diff across customer datasets as a deploy gate — [SlideShare](https://www2.slideshare.net/oraboy/how-totango-uses-apache-spark)
  - Twitter Diffy: second-hand description only — [helpmetest.com](https://helpmetest.com/blog/diffy-shadow-mode-testing/)
  - Advice to measure a run-vs-itself "noise floor" before diffing — [Arize glossary](https://arize.com/glossary/shadow-testing-llms-agents/) (vendor content)
- **Uber, Netflix, Meta and Airbnb.** No primary blog post on synthetic data for pipeline testing was found in one search [gap].

### Inferences
Proposed protocol, assembled from the documented pieces [inferred]:
1. Pin a pipeline version (commit hash plus config) and a synthetic dataset version.
2. An inside CI runner executes the pipeline on a real snapshot. The outside CI executes the same version on the synthetic data.
3. Both runs emit the same fixed "test-summary schema": the workload-fidelity vector from Q3 plus selected utility scores from Q2, computed inside.
4. An automated output checker inside applies rules before release:
   - minimum cell counts and small-count suppression;
   - rounding;
   - no row-level values or identifiers;
   - no free-text error messages, since these can echo real field values;
   - coarse quantiles only;
   - a cap on query frequency or differencing across releases (the privacy-budget idea from Burman et al. 2018 and Barrientos et al. 2023);
   - optionally DP noise on counts.
5. Outside, compare real and synthetic summaries with Q-error and absolute-difference tolerances. Repeat the real run twice, or on two snapshots, to establish a noise floor first.
6. Treat persistent gaps as synthesis defects and feed them back into the generator.

Notes on the protocol:
- **Highest-leak outputs.** Error and reject outputs and ER cluster-size tails are the highest-risk exports, because rare categories and singleton clusters can identify entities. Suppress or bucket them [inferred; disclosure control is covered in depth by another researcher].
- **Licensed reference data.** Licensed reference data may allow richer exports than personal data, subject to licence terms. Derived-statistics clauses need checking [inferred].
- **Performance metrics.** Times, memory and spill reveal little about individuals but can reveal volumes. They are generally low-risk, but row counts per source may be commercially sensitive under licences [inferred].

### Gaps
- No full-text engineering blog was read for real-vs-synthetic differential pipeline testing. The industry examples are leads, and none is real-vs-synthetic.
- No source was found on formal output-checking rules for pipeline test summaries specifically. This is SDC territory (SDC = statistical disclosure control), deferred to the disclosure-control researcher.
- Commercial "test data management" or synthetic-data vendors (e.g. Tonic, Gretel, MOSTLY AI) were not researched. Any capability claims would be [vendor marketing].
