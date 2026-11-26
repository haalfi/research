# Non-circular evaluation of synthetic data and generated test fixtures: held-out workloads, time splits and later observation windows

Scope: precedents and methodology for calibrating a generator (or model) on one observation window or workload set, then evaluating it on held-out workloads and a later window. The aim is to judge the external report's proposal (section 12): "calibrate the generators using one observation window and evaluate them against an independent set of workloads and a subsequent production observation window". The section 3 claims are checked as well.

Labels: **[documented]** = full text, or the relevant full section, read in this session; **[lead]** = search extract or abstract only; **[inferred]** = my reasoning; **[unreachable]** = could not be retrieved; **[vendor]** = provider claim. Earlier repository notes (read-only) already cover SAM's metric definitions and the Hydra, Touchstone, Mirage and DBRepro inputs: `research_notes/Synthetic stand in test data/utility_validation.md` and `characteristics_and_benchmark_generators.md`. They are not repeated here except where the held-out design matters.

Retrieval log:
- Full texts were read via arXiv, author pages and NIST/Cornell repositories. Each download went to its own `p3d_*` scratchpad subdirectory and was converted with pdftotext.
- Unreachable: dsl.cds.iisc.ac.in (HF-Hydra DASFAA 2021 PDF: curl code 000), eprints.iisc.ac.in (403), etd.iisc.ac.in (502), and the nber.org chapter (403, site-side).
- The dblp API returned non-JSON.

---

## 1. Database generation: workload-aware generators and learned cardinality estimators evaluated on held-out queries, data drift and workload drift

### Takeaway
Holding out queries is an established practice in workload-aware database generation and in learned cardinality estimation. SAM's papers separate "fidelity" (the input constraints) from "closeness" (independent test queries) explicitly. MSCN, Negi et al. and Wang et al. test generalisation to structurally different workloads, to temporally older data (IMDb-1950) and to appended data. However, none of the generator papers read evaluates a generated database against a *later production observation window*. The held-out sets come from the same static snapshot. A time split for a synthetic database generator is therefore an extension of existing practice, not a replication of it.

### Cited Findings
- **SAM (Yang et al., SIGMOD 2022, pp. 1542–1555, DOI 10.1145/3514221.3526168)** [documented: experimental setup and findings read] — [author camera-ready PDF](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf)
  - **Two evaluation aspects.** Aspect 1, "fidelity", is Q-error on the *input* query constraints, sampled to 1,000 of the 100K for IMDB. Aspect 2, "closeness", is cross-entropy plus "Q-Error on an independent test query set", which "measures how well the generated database recovers the joint data distribution and generalizes to unseen queries". This is an explicit, published separation of fit-to-targets from held-out evaluation.
  - **Held-out design, single relations.** On the single-relation datasets (Census, DMV), "the test query workloads are randomly generated with the same procedure as the input query workloads but are ensured to have no duplicate query". The test set is therefore i.i.d. from the same generator, not a different workload.
  - **Held-out design, IMDB.** The input workload is the public MSCN training set: 100K queries with 0–2 joins. The test set is JOB-light (70 queries). "While MSCN training queries only contain joins of up to three relations, JOB-light contains a variety of join queries involving up to five relations". This is a structurally out-of-distribution held-out workload.
  - **Performance deviation.** Query-latency difference is measured on an independent test workload in PostgreSQL 12.0.
  - **Results.** The authors state "(F4) SAM can well generalize to unseen queries while PGM cannot", reporting "at least two orders of magnitude smaller error at all percentiles" on IMDB. SAM achieves "20×, 80× and 40× smaller performance deviation at median, 75th and 90th percentile" on JOB-light versus the PGM baseline.
  - **SAM's JOB-light Q-errors.** Parsed from PDF text and apparently Table 6: median 2.29, 75th 5.39, 90th 27.78, mean 2776, max 2·10^5. The heavy tail persists even for the best method. These are author benchmarks against a single baseline.
- **MSCN (Kipf et al., CIDR 2019, 13–16 Jan 2019)** [documented: sections 4.4–4.5 and 5 read] — [arXiv 1809.00677](https://arxiv.org/abs/1809.00677)
  - **Training set.** 100,000 random queries with 0–2 joins.
  - **"scale" workload.** This tests "queries with three and four joins without having seen such queries during training". The 95th-percentile q-error rises from 7.66 to 38.6 (2→3 joins) and to 2,397 with four joins (PostgreSQL: 78.0 and 4,077). "58 out of the 500 queries in this workload exceed the maximum cardinality seen during training".
  - **JOB-light.** This shows generalisation "to a workload that was not generated by our query generator". The 95th-percentile q-error is 362 vs PostgreSQL 1104 (parsed from table text, approximate), or 115 without five queries above the training cardinality range.
  - **Authors' own limit.** "generalizing to queries that are not in the vicinity of the training data remains challenging".
- **Wang et al., "Are We Ready For Learned Cardinality Estimation?" (PVLDB 14(9), 2021)** [documented: sections 4.1 setup and 5 read] — [arXiv 2012.06743](https://arxiv.org/abs/2012.06743)
  - **Static setting.** A "unified workload generator" produces queries: 100K training queries for the query-driven methods, a 10K validation set and 10K test queries. So static-setting test queries come from the same generator as training queries [documented setup; the i.i.d. reading is inferred].
  - **Dynamic setting (section 5).** "We append 20% new data to the original dataset and apply our workload generation method to the updated data to general 10K test queries". The appended data is constructed to have "different correlation characteristics": each column of a copy is sorted to maximise pairwise Spearman correlation and 20% of those tuples are appended. This is *synthetic injected drift*, not an observed later window.
  - **Findings.** "Learned methods cannot catch up with fast data updates. MSCN, LW-NN, Naru, and DeepDB return large error in dynamic environments". "DBMSs have more stable performance than learned methods". For example, at T = 50 min on DMV, "DBMS-A outperforms DeepDB by about 100× since the updated DeepDB model cannot capture correlation change well."
  - **Relevance [inferred].** A model that excels on held-out queries from the calibration snapshot can lose that advantage once the data changes. This is the failure a later-window evaluation is designed to expose.
- **Negi et al., "Robust Query Driven Cardinality Estimation under Changing Workloads" (PVLDB 16(6): 1520–1533, 2023)** [documented: abstract and sections 3, 6.1–6.3 read] — [NSF PAR full text](https://par.nsf.gov/servlets/purl/10495282)
  - **Drift taxonomy.** After training "the model is fixed" and is evaluated on new queries that differ by: "a) New queries have same templates, and only the filter constants change. b) New queries include filters on new columns, new join graphs (new combination of tables), or entirely new tables. c) New queries, and their cardinalities, are on updated data."
  - **Splits used.**
    - Train on JOBLight-train and test on JOB/CEB (cross-workload).
    - Ten 50–50 train/test splits within JOB, described as "an example of a workload drift scenario as well because each JOB query has a slightly different template".
    - A **temporal data split**: "models trained on CEB template 1a with ground truth data from IMDb-1950, and tested on unseen queries from the same template" on the full IMDb. Standard MSCN "gets much worse than PostgreSQL when trained on 1950 data".
  - **Abstract.** Query-driven models "can suffer unpredictably bad performance under workload drift, i.e., if the query pattern or data changes". Their robust variant "never perform[s] worse than PostgreSQL".
  - **Relevance [inferred].** This is the closest database-side precedent for "calibrate on an earlier window, evaluate on a later state of the same data". It concerns cardinality models, not data generators.
- **HF-Hydra (Sanghi, Santhanam, Haritsa, "Towards Generating HiFi Databases", DASFAA 2021, LNCS pp. 105–112, DOI 10.1007/978-3-030-73194-6_8; Crossref metadata checked)** [lead: search extract only; PDF unreachable]
  - Its motivation, as reported in search extracts, is that Hydra "suffers poor accuracy on unseen queries". HF-Hydra adds metadata constraints and multiple candidate summaries. It reportedly improves volumetric similarity on filter constraints of unseen queries by >30% (UMBRAE metric) on TPC-DS-based experiments — [DASFAA PDF (unreachable)](https://dsl.cds.iisc.ac.in/publications/conference/DASFAA_2021.pdf), [TR-2021-01 (unreachable)](https://dsl.cds.iisc.ac.in/publications/report/TR/TR-2021-01.pdf).
  - If confirmed, this is a direct example of a held-out-query evaluation exposing overfitting of a workload-aware generator to its input workload.
- **Touchstone, Mirage, DBRepro.** Held-out-query evaluation sections were not read in this track. Earlier notes cover their inputs and plan-consistency benchmarks only (`characteristics_and_benchmark_generators.md`) [gap].

### Inferences
- **Two distinct held-out designs.**
  - (a) i.i.d. held-out queries from the same query generator (SAM single-relation, Wang static). These test interpolation within the calibrated query distribution.
  - (b) Structurally different workloads (SAM/MSCN on JOB-light, Negi JOB/CEB). These test extrapolation.
  - The proposal's "independent set of workloads" should mean (b), with templates, join graphs or columns not used in calibration. Fresh constants on the same templates (Negi's case a) would mostly reproduce (a).
- **No later-window evaluation of generators.** No read paper evaluates a synthetic database generator against a later real snapshot. Wang (injected drift) and Negi (IMDb-1950) do so for cardinality models. This is absence of evidence from the papers read, not evidence that no one has done it.
- **Same metrics fit the protected-environment constraint.** The metrics used (Q-error per query, latency deviation per query, cross-entropy) are aggregates. They can be computed inside the protected environment and exported as derived summaries, consistent with the brief's constraint.

### Gaps
- Full texts of Hydra/HF-Hydra (IISc hosts unreachable), Touchstone's and Mirage's evaluation sections, and Kim et al. "Learned cardinality estimation: an in-depth study" (SIGMOD 2022) were not read.
- No paper was found that evaluates a workload-aware generator on queries arriving *after* calibration in a real production log.

---

## 2. Official statistics: synthetic data evaluated on analyses not anticipated at synthesis, on other periods, or via validation of real user analyses

### Takeaway
The official-statistics literature states plainly that synthesisers cannot know future analyses. Snoke et al. warn that specific-utility checks that mirror the synthesis model can falsely reassure. Their remedy is general plus specific utility used in tandem, not a time split. Two real precedents exist:
- **Validation of real users' unplanned analyses.** The Census/Cornell Synthetic Data Server ran these against confidential data with disclosure review. Agreement was often poor: the median confidence-interval overlap was 0 for SynLBD in initial results.
- **Cross-period scoring.** The NIST 2018–19 DP synthetic data challenge scored methods on data from different years or states than those used for development.

I found no published validation of SynLBD (or similar) forward against a later release year (absence of evidence).

### Cited Findings
- **Snoke, Raab, Nowok, Dibben, Slavković, "General and specific utility measures for synthetic data"**: *JRSS Series A* 181(3): 663–688, 2018, DOI 10.1111/rssa.12358 (Crossref metadata checked: published 7 Mar 2018). I read the arXiv v2 of 19 Jun 2017, not the journal typeset version [documented] — [arXiv 1604.06651](https://arxiv.org/abs/1604.06651)
  - **On unknown analyses.** When an agency "prepares synthetic data for a user they will not know, except in very general terms, what analyses will be carried out". "When the synthesizer does have some knowledge of the models that the analyst has in mind and bases the synthesis on these models, this may falsely reassure the analyst that their model is the correct one. When the generative model that informs the synthesis adheres too closely to the proposed utility model, the validity checks such as the existence of other interactions will not be apparent in the synthesized data".
  - **On specific utility.** "It is impossible to compare every possible specific analyses researchers may wish to perform using the synthetic data, and in some cases, the specific utility may be misleading, particularly [if] the utility models are similar to models included in the synthesis. The general utility and specific utility should be used in tandem along with data visualizations and marginal distribution checks".
  - **Methods.**
    - General utility: propensity-score mean-squared error (pMSE) and its ratio/standardised forms.
    - Specific utility: confidence-interval overlap and standardised coefficient difference, implemented in synthpop's `compare.fit.synds()`-style functions.
    - Worked examples: SHeS and I-CeM. In the SHeS example, the logistic pMSE with main effects only "does not discriminate between the synthesis methods".
  - **Nature of the paper.** The paper does not prescribe evaluating on analyses held out from synthesis as a protocol, nor any time split. Its argument is that general measures help *because* the specific analyses are unknown [documented, by reading the full text].
- **Census/Cornell Synthetic Data Server: Vilhuber and Abowd, "Usage and outcomes of the Synthetic Data Server", slides, May 2016** [documented: full slides read] — [Cornell eCommons PDF](https://ecommons.cornell.edu/server/api/core/bitstreams/0d52578a-0a7f-4eff-8be1-83cc9d1bfffa/content)
  - **Validation procedure.** "No restrictions on type of model to be estimated". Validated results "must pass disclosure-avoidance analysis". Users provide all programs and inputs; validation turnaround is about one week.
  - **Uptake.** SynLBD: "5 out of 79 projects have requested validation" (as of 2015-08-10). SSB: "about 10 out of about 100".
  - **Initial overlap results** (interval-overlap measure J_k, synthetic vs confidential CIs; parsed from slide text, column alignment approximate):
    - SynLBD, all models: mean 0.206, median 0, 75th percentile 0.504.
    - SSB, two users: mean 0.49 and 0.39, median 0.54 and 0.52, with 82.4% and 73.2% of estimates having overlap > 0.
  - **Bertrand et al. (SSB) case.** The confidential data show "a distinct break in the distribution of couples when the wife's income surpassed 50%". There was "No such break in the synthetic data".
  - **Stated downside.** The approach "will not work for non-congenial designs (f.i. regression discontinuity)".
  - **Relevance [inferred].** This is the closest real precedent for *unanticipated analyses run inside the protected environment, with only reviewed results leaving*. Its results show that unplanned analyses can expose features the synthesiser never modelled.
- **Census SynLBD analytic-validity page.** It says "The SynLBD has not been fully validated" and encourages result validation. It was already documented in earlier notes and not re-read here — [Census](https://www.census.gov/programs-surveys/ces/data/public-use-data/synthetic-longitudinal-business-database/analytic-validity.html) [lead in this track; documented in `utility_validation.md`].
- **Barrientos et al., "Providing access to confidential research data through synthesis and verification" (Annals of Applied Statistics 12(2): 1124–1156, 2018; Crossref checked)** [documented: abstract and introduction read via arXiv v2, 16 Jun 2018] — [arXiv 1705.07872](https://arxiv.org/abs/1705.07872)
  - The system pairs fully synthetic longitudinal data with "a verification server that allows them to assess the quality of inferences from the synthetic data". Verification measures are "designed to satisfy differential privacy".
  - The application is longitudinal (US federal employees, models of pay gaps "over time").
  - It is a verification-of-user-analyses design, not a later-window design.
- **NIST PSCR Differential Privacy Synthetic Data Challenge (Nov 2018 – May 2019), as analysed by Bowen and Snoke** (*Journal of Privacy and Confidentiality* 11(1), 2021, DOI 10.29012/jpc.748; Crossref checked) [documented: sections 2–4 and conclusions read] — [arXiv 1911.12704](https://arxiv.org/abs/1911.12704)
  - **Design.** "Each match provided the contestants with a real-world data set to train and develop their DP methods that were identical in structure and variables to the real-world test data used for final scoring". "NIST PSCR challenge organizers applied the differentially private synthetic data methods to the test data for final scoring".
  - **Training and scoring data by match** (Table 2):
    - Match 1: trained on 2017 SFFD calls, scored on 2016.
    - Match 2: trained on 2016, scored on 2006 and 2017.
    - Match 3: trained on Colorado PUMS, scored on Arizona and Vermont PUMS.
  - **Leakage caveat.** "NIST PSCR announced the metric criteria at the start of each match, so the competitors could modify their approach based on the scoring metrics". The *data* were held out but the *evaluation analyses* were known in advance.
  - **Relevance [inferred].** This is a documented cross-period and cross-region design. It evaluates the *method* (re-run on the scoring data), not a synthetic dataset generated from window t and scored against window t+1.
- **Search for temporal holdouts.** Searches for synthetic data validated against a later census, wave or year found only spatial holdouts and same-period holdout records, e.g. a geographic hold-out state in a 2026 synthetic-population preprint and holdout-based assessment in Frontiers in Big Data 2021 — [arXiv 2608.12768](https://arxiv.org/pdf/2608.12768), [Frontiers 2021](https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2021.679939/pdf) [lead: not read].

### Inferences
- **The official-statistics analogue of a held-out workload** is the *validation server or verification server* run inside the agency on analyses chosen by users after release. It is established, and it reports both successes and failures. Its weakness for the platform use case is that the analyses arrive ad hoc and are few (5 of 79 SynLBD projects), not as a designed held-out battery.
- **Snoke et al.'s warning supports independence.** The warning about "utility models similar to models included in the synthesis" directly supports the report's circularity point. Snoke's remedy (general utility) differs from the report's (independent workloads and a later window), so the two are complementary, not the same claim.

### Gaps
- No source was found that validates SynLBD, SSB or the UK longitudinal-study synthetic extracts forward against later confidential years. The Kinney, Reiter and Miranda SynLBD 2.0 paper (Stat. J. IAOS 30(2), 2014) and the CES-WP-14-12 working paper were not read — [RTI listing](https://www.rti.org/publication/synlbd-20) [lead].
- The full Vilhuber and Abowd working paper is marked "do not cite" and was not used.

---

## 3. Software testing and empirical software engineering: time-aware evaluation, held-out versions and leakage

### Takeaway
Time-respecting evaluation is well established in software analytics, security ML and industrial test selection:
- train strictly on the past and evaluate on the future (TESSERACT C1, Bangash, Facebook predictive test selection);
- prefer walk-forward over cross-validation (Falessi);
- re-evaluate per window, because conclusions are not stable over time.

Generated-test evaluation on Defects4J uses a "generate on the fixed version, run on the buggy version" regression scenario. Detection of real faults was partial: 55.7% of faults in aggregate, 19.9% of individual suites.

### Cited Findings
- **TESSERACT (Pendlebury, Pierazzi, Jordaney, Kinder, Cavallaro, USENIX Security 2019; arXiv v4 12 Sep 2019)** [documented: sections 1, 3 and 4.1–4.2 read] — [arXiv 1807.07838](https://arxiv.org/abs/1807.07838); a [USENIX Security '19 presentation page](https://www.usenix.org/conference/usenixsecurity19/presentation/pendlebury) exists (HTTP 200; not read)
  - **Biases.** Results are "commonly inflated due to two pervasive sources of experimental bias": spatial bias (unrepresentative train/test distributions) and "temporal bias caused by incorrect time splits of training and testing sets, leading to impossible configurations".
  - **Constraints.**
    - "C1) Temporal training consistency. All the objects in the training must be strictly temporally precedent to the testing ones"; "its violation inflates the results by including future knowledge".
    - "C2) Temporal gw/mw windows consistency. In every testing slot of size Δ, all test objects must be from the same time window".
    - "C3) Realistic malware-to-goodware ratio in testing".
  - **AUT metric.** AUT (area under the performance-over-time curve) summarises decay over the test windows.
  - **Results.** On 129K apps (Jan 2014 – Dec 2016; train 2014, test 2015–2016), "performance can decrease up to 50% in practice". AUT(F1, 24m) is 0.58, 0.32 and 0.64 for the three classifiers, lower than their 10-fold F1.
- **Bangash, Sahar, Hindle, Ali, "On the time-based conclusion stability of cross-project defect prediction models"** (*Empirical Software Engineering* 25(6): 5047–5083, 2020, DOI 10.1007/s10664-020-09878-9; Crossref checked; arXiv v3 7 Aug 2020) [documented: abstract, introduction and conclusion read] — [arXiv 1911.06348](https://arxiv.org/abs/1911.06348)
  - It uses "a time-aware evaluation approach where models are trained only on the past, and evaluations are executed only on the future".
  - Performance in F-score, AUC and MCC "varies and their results are not consistent". "The next release of a product, which is significantly different from its prior release, may drastically change defect prediction performance".
  - The conclusion finds rankings from Herbold et al.'s benchmark "are not stable across different periods of time", with SD ≥ 0.05 in F-score, MCC and G-measure. Researchers should "couch their claims of performance within the contexts of their evaluation".
- **Falessi, Huang, Narayana, Thai, Turhan, "On the need of preserving order of data when validating within-project defect classifiers"** (*EMSE* 25(6): 4805–4830, 2020, DOI 10.1007/s10664-020-09868-x) [documented: abstract of the latest arXiv version read; journal pages per search extract] — [arXiv 1809.01510](https://arxiv.org/abs/1809.01510)
  - **Ground truth and design.** The last release is used as ground truth. Nine classifiers on 2 industry and 13 open projects are validated by 10-fold CV, bootstrap and walk-forward.
  - **Results.** "walk-forward outperforms both 10-fold cross-validation and bootstrap statistically in all three accuracy metrics". "all techniques resulted to be more prone to overestimate than to underestimate". "the defect rate resulted in changing between the second and first half in both industry projects and 83% of open-source datasets".
  - **Version discrepancy.** An earlier preprint version (search extract) reported AUC differences of [−0.20, 0.22] and statistical differences in 45% of cases. I did not verify these against the journal version [lead].
- **Machalica, Samylkin, Porth, Chandra, "Predictive Test Selection" (Facebook; arXiv v2 29 May 2019; ICSE-SEIP 2019 venue per my recollection, not verified here)** [documented: abstract and section IV.C–D read] — [arXiv 1810.05286](https://arxiv.org/abs/1810.05286)
  - **Time split.** "We use strategy s* trained on past code changes to select tests for changes created in the future. Therefore, when calibrating s* and evaluating its performance we must use test results not included in the training dataset. We split collected data, such that test outcomes recorded for changes submitted during the most recent week fall into the testing dataset". This "closely replicates how the model is going to be used in practice".
  - **Ground truth.** Recall requires running *all* dependent tests on a sample of changes ("learning test runs"), deferred to off-peak hours. About a quarter of changes are sampled.
  - **Limit and response.** "Since we evaluate the model's performance on only one week worth of test outcomes, we cannot guarantee it remains unchanged for a much longer period of time". The model is retrained weekly, with an assertion gate (e.g. "SelectionRate(s*) < 0.3 for TestRecall(s*) = 0.9") and human investigation if the gate fails.
  - **Deployed result.** The authors report that the deployed strategy "reduces the total infrastructure cost of testing code changes by a factor of two, while guaranteeing that over 95% of individual test failures and over 99.9% of faulty changes are still reported" [documented; author/vendor-side claim about its own production].
- **Shamshiri, Just, Rojas, Fraser, McMinn, Arcuri, "Do Automatically Generated Unit Tests Find Real Faults?" (ASE 2015)** [documented: abstract and methodology read] — [author PDF](https://homes.cs.washington.edu/~rjust/publ/unit_test_generation_effectiveness_ase_2015.pdf)
  - **Setup.** "Test suites are generated with all tools on the fixed version, and executed on the buggy version … we are considering a regression testing scenario, where a developer would apply test generation to guard against future faults". The subjects are 357 Defects4J faults from five projects.
  - **Results.** "Although the automatically generated test suites detected 55.7% of the faults overall, only 19.9% of all the individual test suites … actually detected a fault."
- **Jimenez et al. (FSE 2019).** "Time-aware" vulnerability-prediction evaluation was not read [gap].

### Inferences
- **Transferable rules for the platform's proposal:**
  - C1: calibration observations strictly precede evaluation observations.
  - C2: evaluate per fixed window, not pooled.
  - C3: evaluation windows keep the realistic production mix (of workloads, entity types and incident classes) rather than an enriched one.
  - Walk-forward, i.e. several successive windows, rather than one split, because single-period conclusions are unstable (Bangash, Falessi).
  - A standing re-evaluation gate per window (Machalica).
- **Ground truth and cost.** Machalica's "learning test runs" show that ground truth for later-window evaluation must be paid for deliberately: run the full reference workload on a sample, inside the environment.
- **What the Defects4J design tests.** Its "fixed → buggy" design tests detection of *known, historically reintroduced* faults, not of unknown future faults. A test-data analogue (reproduce historical incident classes) is likewise backward-looking.

### Gaps
- Regression-test-selection studies with explicit temporal leakage analysis beyond Facebook (e.g. Elsner et al. ISSTA 2021, Bertolino et al. ICSE 2020) were not read.
- No software-testing paper was found that evaluates *generated test data* (as opposed to generated tests or prediction models) on a later production window.

---

## 4. Drift-aware evaluation of synthetic data: generated from period t, evaluated against t+1

### Takeaway
I found no study that fits a synthetic-data or synthetic-database generator on period t and scores the generated data against real period t+1. This is absence of evidence from targeted searches and the papers read, not evidence of absence. The closest documented precedents are:
- the NIST challenge's cross-year scoring of synthesis *methods*;
- Negi et al.'s IMDb-1950 → full-IMDb evaluation of cardinality *models*;
- Wang et al.'s injected-drift evaluation;
- prediction-model "temporal validation" methodology (TRIPOD) and security/software-analytics time splits.

### Cited Findings
- **TRIPOD Explanation and Elaboration (Moons et al., *Annals of Internal Medicine* 162(1): W1–W73, 2015)** [documented: introduction and validation passages read] — [Elsevier-hosted full PDF](https://legacyfileshare.elsevier.com/promis_misc/XKME_TRIPOD_Guidelines_moreinfo.pdf)
  - **Random splits.** "Randomly splitting a single data set into model development and model validation data sets … is often, yet erroneously, believed to be a form of external validation. However, this approach is a weak and inefficient form of internal validation".
  - **Time splits.** "splitting by time and developing a model using data from one period and evaluating its performance using the data from the other period (temporal validation) is a stronger approach. With a single data set, temporal splitting and model validation can be considered intermediate between internal and external validation."
  - **External validation.** External validation may use data "sampled from a later period (temporal or narrow validation)". "Reduced performance is more likely in a different geographic or setting validation, by different investigators, than in a temporal validation by the same investigators".
- **NIST PSCR DP challenge.** Methods developed on 2016/2017 San Francisco fire-call data were scored on other years (2006, 2016, 2017), and Colorado-developed methods on Arizona/Vermont. The organisers ran the methods on the sequestered scoring data — [Bowen and Snoke, arXiv 1911.12704](https://arxiv.org/abs/1911.12704) [documented].
- **Negi et al.** trained on IMDb-1950 ground truth and tested on full IMDb: the standard model degraded below PostgreSQL, the robust one did not — [NSF PAR](https://par.nsf.gov/servlets/purl/10495282) [documented].
- **Wang et al.** appended 20% of rows with deliberately different correlations and regenerated the test queries: learned estimators degraded, DBMS estimators stayed stable — [arXiv 2012.06743](https://arxiv.org/abs/2012.06743) [documented].
- **Adjacent leads.** TabReD argues that tabular benchmarks should use time-based splits because rankings change versus random splits. Seq2Synth (2026 preprint) reports that generators with near-perfect static fidelity can break temporal constraints — [TabReD arXiv 2406.19380](https://arxiv.org/html/2406.19380v4), [Seq2Synth arXiv 2607.15606](https://arxiv.org/pdf/2607.15606) [lead: search extracts only].

### Inferences
- **Two distinct cross-period designs:**
  - (i) *Method transfer*: re-run the generator's fitting on window t+1 (NIST). This tests whether the calibration *procedure* generalises.
  - (ii) *Artefact staleness*: keep the data generated from window t and compare it with real window t+1. This tests how fast a released characterisation goes stale.
  - The external report's wording ("calibrate … using one observation window and evaluate them against … a subsequent production observation window") reads as (ii). Both are worth running; they answer different renewal questions.
- **Prior drift-detection notes.** The drift-detection notes in `temporal_drift_renewal.md` (earlier track) address detecting change. They do not establish that a generated artefact remains fit for purpose, which only (ii) measures.

### Gaps
- NIST CRC, NIST 2020 Temporal Map challenge and synthetic-EHR temporal generalisation studies were not read.
- No longitudinal official-statistics synthetic product with forward-in-time validation was found.

---

## 5. What a time-split / held-out-workload evaluation establishes and does not establish

### Takeaway
Combining held-out workloads with a later window establishes two things: that the generator is not merely reproducing its fitting targets, and how quickly fidelity decays under real production change. It is a strong but bounded form of evidence. TRIPOD calls the same-team temporal split "intermediate between internal and external validation". It does not establish fidelity for workloads or faults outside the evaluated set, nor equivalence for unknown future failure mechanisms.

### Cited Findings
- **TRIPOD on strength.** Temporal validation is stronger than a random split but "intermediate between internal and external". Larger drops are more likely under geographic or setting changes than under temporal validation by the same investigators — [TRIPOD E&E](https://legacyfileshare.elsevier.com/promis_misc/XKME_TRIPOD_Guidelines_moreinfo.pdf) [documented].
- **Single splits are not conclusions.** Conclusions from one period can reverse in the next (Bangash), and order-preserving walk-forward is less optimistic than CV (Falessi) — [arXiv 1911.06348](https://arxiv.org/abs/1911.06348); [arXiv 1809.01510](https://arxiv.org/abs/1809.01510) [documented].
- **Evaluation-set leakage through announced metrics.** In the NIST challenge, announced metrics let competitors "modify their approach based on the scoring metrics" — [Bowen and Snoke](https://arxiv.org/abs/1911.12704) [documented]. Likewise, Snoke et al. warn that specific utility "may be misleading" when the utility models resemble the synthesis models — [arXiv 1604.06651](https://arxiv.org/abs/1604.06651) [documented].
- **Held-out success is distribution-bound.** MSCN: "generalizing to queries that are not in the vicinity of the training data remains challenging". Queries exceeding the training cardinality range drove large errors — [arXiv 1809.00677](https://arxiv.org/abs/1809.00677) [documented].
- **Unplanned analyses can find what the synthesiser never modelled.** The SSB lacked the 50% income-share discontinuity. The verification approach "will not work for non-congenial designs" — [Vilhuber and Abowd 2016](https://ecommons.cornell.edu/server/api/core/bitstreams/0d52578a-0a7f-4eff-8be1-83cc9d1bfffa/content) [documented].
- **Fault-detection evidence is partial and backward-looking.** Generated suites detect 55.7% of known Defects4J faults collectively and 19.9% individually — [Shamshiri et al. 2015](https://homes.cs.washington.edu/~rjust/publ/unit_test_generation_effectiveness_ase_2015.pdf) [documented].
- **One window does not certify later windows.** "we cannot guarantee it remains unchanged for a much longer period of time" — hence weekly re-evaluation — [Machalica et al.](https://arxiv.org/abs/1810.05286) [documented].

### Inferences
- **What it establishes:**
  - (1) whether fidelity on *non-calibrated* workloads is close to fidelity on calibrated ones, i.e. overfitting to the characterisation;
  - (2) the decay rate of fidelity from window t to t+1, i.e. drift sensitivity and a renewal interval;
  - (3) that the calibration and evaluation pipeline can run inside the boundary and export only aggregates, as the NIST and SDS precedents did.
- **What it does not establish:**
  - fidelity for workloads and templates absent from both sets;
  - behaviour under drift larger than the t→t+1 change observed;
  - detection of unknown future fault classes, because historical-incident reproduction is a regression scenario;
  - correctness, as opposed to behavioural similarity (the external report's own caveat in 3.4);
  - generality from one window pair, given conclusion instability.
- **Confounding.** A single "calibrate on t, test on independent workloads in t+1" cell confounds overfitting with drift. A 2×2 design separates them: calibration vs held-out workloads, crossed with window t vs t+1. Calibration workloads in t+1 isolate drift; held-out workloads in t isolate overfitting.
- **Keep evaluation workloads private.** Evaluation workloads and metrics should be fixed before calibration but withheld from whoever tunes the generator (the NIST lesson). Otherwise they become fitting targets and the evaluation is circular again.
- **Repeat over windows.** Repeat walk-forward over several windows (TESSERACT AUT-style summary across windows) rather than one split.
- **Disclosure budget.** Each window's exported aggregates add to cumulative disclosure. The evaluation design therefore interacts with the privacy budget (cf. external report section 4.3). This was not researched here.

### Gaps
- No empirical study quantifies how well held-out-workload fidelity of synthetic test data predicts real defect-detection or capacity-planning outcomes.

---

## 6. Verdicts on external report claims (sections 3 and 12)

### Takeaway
The circularity argument and the Snoke et al. citation are confirmed. The general/specific utility framing is accurate, though "use-specific" is the report's wording. The section 12 proposal is consistent with established time-split and held-out methodology, which the report does not cite. I found no published precedent for applying it to synthetic test data or generated databases against a later production window. The claim about what it would reveal is partially confirmed, with a confounding caveat.

### Cited Findings
| # | Claim (external report) | Verdict | Basis |
|---|---|---|---|
| 1 | §3: "A major weakness of many synthetic-data evaluations is circularity". A generator fitted to twenty distributions and evaluated on them "shows that the fitting procedure worked" | **Partially confirmed** | The mechanism is documented: Snoke et al. warn that specific utility "may be misleading, particularly [if] the utility models are similar to models included in the synthesis" ([arXiv 1604.06651](https://arxiv.org/abs/1604.06651)). SAM separates input-constraint "fidelity" from independent-test "closeness" ([SAM PDF](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf)). "Many" (prevalence) is unverified. |
| 2 | §3: official statistics distinguishes general from use-specific utility; "Snoke et al. (2018) provide established methods for both" | **Confirmed** | The publication is JRSS-A 181(3): 663–688, 2018, DOI 10.1111/rssa.12358 (Crossref). It covers pMSE (general) and CI overlap plus standardised difference (specific), implemented in synthpop. The paper's term is "specific utility" ([arXiv](https://arxiv.org/abs/1604.06651)). Snoke et al. do not address held-out or later-window evaluation. |
| 3 | §3.1 level 3, "Independent statistics: measurements not supplied to the generator", tests whether the generator "generalise[s] beyond its fitting targets" | **Partially confirmed** | Precedent exists in database generation: SAM's independent test set "generalizes to unseen queries"; HF-Hydra was motivated by Hydra's unseen-query accuracy [lead]. The six-level framework itself is the report's synthesis [inferred]. |
| 4 | §3.2: executing a reference workload inside the protected environment "is the most important independent validation mechanism" | **Unverifiable as a ranking; mechanism confirmed** | The Census/Cornell SDS validated user analyses on confidential data with disclosure review, and NIST ran methods on sequestered data ([SDS slides](https://ecommons.cornell.edu/server/api/core/bitstreams/0d52578a-0a7f-4eff-8be1-83cc9d1bfffa/content); [Bowen and Snoke](https://arxiv.org/abs/1911.12704)). "Most important" is opinion. |
| 5 | §3.4: "There is no general utility score that substitutes for a representative platform workload" | **Partially confirmed** | Snoke et al.: "impossible to compare every possible specific analyses". Logistic pMSE with main effects failed to discriminate synthesis methods in SHeS. But Snoke argues general utility is *needed because* analyses are unknown, so both are needed, not one substituting for the other. |
| 6 | §12: "calibrate the generators using one observation window and evaluate them against an independent set of workloads and a subsequent production observation window" | **Partially confirmed (sound and consistent with established methodology; no direct precedent found for synthetic test data)** | Methodology: TRIPOD temporal validation, TESSERACT C1/C2, Bangash, Falessi walk-forward, Machalica's most-recent-week split. Held-out workloads for generators: SAM (documented), HF-Hydra (lead). Cross-period: NIST challenge (method transfer), Negi IMDb-1950 (cardinality models). No paper found evaluating a synthetic database/test-data generator against a later real window (absence of evidence). The report cites no precedent for it. |
| 7 | §12: this "would reveal both overfitting to the chosen characterisation and sensitivity to production changes" | **Partially confirmed** | Held-out workloads reveal overfitting (SAM, MSCN, HF-Hydra lead). Later data reveals drift sensitivity (Wang, Negi, TESSERACT). [Inferred caveat] A single combined cell confounds the two; a 2×2 design (workload set × window) is needed. Both effects are bounded by the evaluated workloads and window pair (Bangash; TRIPOD "intermediate" strength). |
| 8 | §3.4: synthpop provides "general and analysis-specific utility measures" ("Active September 2026 release") | **Partially confirmed / release date unverifiable** | Snoke et al. state that the CI-overlap and standardised-difference measures are implemented in synthpop. Release activity was not checked here. |

### Inferences
- **Suggested upgrades to the proposal**, derived from the sources above [inferred]:
  - Pre-register and withhold the evaluation workloads.
  - Use templates or join graphs absent from calibration.
  - Run walk-forward over several windows.
  - Separate drift from overfitting with a 2×2 design.
  - Budget ground-truth runs inside the boundary, as in Machalica's learning runs.
  - Count each window's exports against the disclosure budget.

### Gaps
- HF-Hydra, Hydra, Touchstone and Mirage held-out evaluation sections were not read (unreachable or out of budget). Verdicts 3 and 6 rest on SAM, MSCN and Negi for the database side.
