# Prior-art map and terminology: making tests on fictional data exercise implementation logic and expose real-data defects

Track: prior-art map, terminology, citation chains, systematic reviews, industrial case studies, and directly comparable solutions.

Status labels used on every claim:
- **[documented]**: I read the full text, or the relevant full-text sections retrieved as PDF text.
- **[lead]**: abstract or metadata only (OpenAlex record or search extract). Not enough to rest a verdict on.
- **[vendor]**: vendor marketing or a vendor-sponsored survey.
- **[blog]**: engineering blog or project decision record (practice report, not peer reviewed).
- **[inferred]**: my own inference.
- **[unreachable]**: I tried the full text and could not get it.

Evidence-class labels for approaches: **EST** (established in practice), **EXP** (experimentally demonstrated in a research evaluation), **PROP** (research proposal, position paper, or research direction).

Method note: the Semantic Scholar API returned HTTP 429 for every query in this session, so I built citation chains from OpenAlex (api.openalex.org) metadata and abstracts and from the reference lists of the full texts I read. orbilu.uni.lu (University of Luxembourg repository) timed out or returned 503, so the Soltana ASE 2017 and Di Nardo TOSEM 2017 full texts were **[unreachable]**. I read the Soltana et al. TOSEM 2020 arXiv version instead.

Correction to the brief: "kb-anonymity" (Budi, Lo, Jiang, Lucia) was published at **PLDI 2011**, not ICSE 2011 (DOI 10.1145/1993498.1993551). The OpenAlex record and the reference list of Masserini et al. 2024 both say so. "Lucia et al. 2012" is the follow-up "kbe-anonymity" paper at ASE 2012.

---

## Which terms do neighbouring communities use, and how do their citation chains connect?

### Takeaway
No single name or community covers this problem. It is spread across at least seven literatures, each with its own vocabulary:
1. privacy-preserving testing and debugging ("test data anonymization", "behaviour-preserving anonymization", "test outsourcing")
2. database-application testing ("test database generation", "database-state generation", "test database reduction")
3. testing data-intensive / DISC / big-data systems
4. field testing ("ex-vivo", "in-vivo", "offline field testing")
5. production-driven test generation and test amplification
6. ETL / data-warehouse testing ("balancing tests", "source-to-target validation")
7. statistical / usage-based testing ("operational profile", "statistical testing", "synthetic test data")

Record-linkage evaluation and official-statistics synthetic-data practice form two more adjacent, non-SE communities. Felderer et al. (2019) state outright that "testing of data-intensive systems is not yet an established and clearly-defined term".

### Cited Findings

**Terminology by community, with anchor works**

**Privacy-preserving testing and debugging (the "privacy vs. testing utility" chain).**

- Castro, Costa & Martin, "Better bug reporting with better privacy", ASPLOS 2008. They generate new inputs that satisfy the path conditions to the failure but are "otherwise unrelated with the original inputs". The abstract reports error reports "revealing almost no private information". Status: **[lead]**. Class: EXP. — [OpenAlex/DOI 10.1145/1346281.1346322](https://doi.org/10.1145/1346281.1346322)
- Clause & Orso, "Camouflage: automated anonymization of field data", ICSE 2011. Given a failure-inducing input I, they generate I′ that differs from I but causes the same failure. The abstract reports that for the inputs considered "I and I′ shared no sensitive information". Status: **[lead]**. Class: EXP. — [DOI 10.1145/1985793.1985797](https://doi.org/10.1145/1985793.1985797)
- Budi, Lo, Jiang & Lucia, "kb-anonymity: a model for anonymized behaviour-preserving test and debugging data", PLDI 2011. Combines k-anonymity with "program behavior preservation" so that the released data drives the same program behaviour. Its motivating case is a client's collected input data, e.g. a healthcare provider's patient records, which "cannot be released to third-party development houses". Status: **[lead]**. Class: EXP. — [DOI 10.1145/1993498.1993551](https://doi.org/10.1145/1993498.1993551)
- Masserini et al. 2024 (full text) characterise kb-anonymity as using "symbolic execution and k-anonymity to generate anonymized database tuples that do not alter the behavior of the program". They add that it "is limited to numbers and programs whose code is accessible and analyzable with symbolic execution". They also name the path-relaxing successors MultiPathPrivacy and RESPA. Status: **[documented]**. — [arXiv 2402.07460](https://arxiv.org/pdf/2402.07460)
- Lucia, Lo, Jiang & Budi, "kbe-anonymity: test data anonymization for evolving programs", ASE 2012. Shows that applying kb-anonymity repeatedly across program versions creates a cross-referencing privacy risk, and fixes it. Evaluated on three Java programs. Status: **[lead]**. Class: EXP. — [DOI 10.1145/2351676.2351718](https://doi.org/10.1145/2351676.2351718)
- Grechanik, Csallner, Fu & Xie, "Is data privacy always good for software testing?", ISSRE 2010. Status: **[documented]**. Class: EXP. — [author PDF](https://ranger.uta.edu/~csallner/papers/grechanik10is.pdf)
  - Coins the framing "database-centric applications (DCAs)" and "test outsourcing".
  - Argues that "fake data lacks many of the intricate semantic connections among the original data elements".
  - Result: with k-anonymity (Datafly or their guided approach), "for k ≥ 7, test coverage drops to less than 30% from the original coverage of more than 70%".
  - Caveats: the evaluation uses four small Java programs (0.8–4.3K NCLOC: HealthCare, RiskIt, DurboDax, UnixUsage). It measures coverage, not defects found. The authors list small subject size as a threat to validity.
- Taneja, Grechanik, Ghani & Xie, "Testing software in age of data privacy: a balancing act" (PRIEST), ESEC/FSE 2011. Anonymizes data "based on their effect on corresponding DCAs" to keep coverage. Status: **[lead]**. Class: EXP. — [DOI 10.1145/2025113.2025143](https://doi.org/10.1145/2025113.2025143)
- Li, Grechanik, Poshyvanyk et al., "Sanitizing and Minimizing Databases for Software Application Test Outsourcing" (PISTIS), ICST 2014. Program-analysis-weighted clustering replaces records with centroid objects. Coverage "stays within a close range to its original level" in experiments with two applications. Status: **[lead]**. Class: EXP. — [DOI 10.1109/icst.2014.36](https://doi.org/10.1109/icst.2014.36)
- Masserini, Ginelli, Micucci, Briola & Mariani, "Anonymizing Test Data in Android: Does It Hurt?", AST 2024. Studies five database-style privacy-preserving techniques on 19 input-dependent failures in 17 Android apps, measuring whether failures can still be reproduced. It recommends its SCD Local Suppression for strings and Local Suppression or Noise Addition for numbers. Status: **[documented]**. Class: EXP. — [arXiv 2402.07460](https://arxiv.org/pdf/2402.07460)
- Neighbouring chain on privatising shared SE data for defect prediction: Peters, Menzies et al., "Balancing Privacy and Utility in Cross-Company Defect Prediction", TSE 2013 (CLIFF/MORPH). It shares the "privacy vs. utility" vocabulary, but its utility target is defect-predictor accuracy, not test inputs. Status: **[lead]**. — [DOI 10.1109/tse.2013.6](https://doi.org/10.1109/tse.2013.6)

**Database-application testing ("test database generation", "database state").**

- Emmi, Majumdar & Sen, "Dynamic test input generation for database applications", ISSTA 2007. Concolic execution generates both program inputs and "suitable database records". Status: **[lead]**. Class: EXP. — [DOI 10.1145/1273463.1273484](https://doi.org/10.1145/1273463.1273484)
- Binnig, Kossmann, Lo & Özsu, "QAGen: generating query-aware test databases", SIGMOD 2007. Aimed at DBMS testing. Status: **[lead]**. — [DOI 10.1145/1247480.1247520](https://doi.org/10.1145/1247480.1247520)
- Arasu, Kaushik & Li, "Data generation using declarative constraints", SIGMOD 2011. Motivated by "database system and application testing, data masking, and benchmarking". Status: **[lead]**. — [DOI 10.1145/1989323.1989395](https://doi.org/10.1145/1989323.1989395)
- Castelein, Aniche, Soltani, Panichella & van Deursen, "Search-based test data generation for SQL queries" (EvoSQL), ICSE 2018. Status: **[lead]**. Class: EXP. — [DOI 10.1145/3180155.3180202](https://doi.org/10.1145/3180155.3180202)
- Arcuri & Galeotti, "Handling SQL Databases in Automated System Test Generation", TOSEM 2020 (EvoMaster). Status: **[lead]**. Class: EXP. — [DOI 10.1145/3391533](https://doi.org/10.1145/3391533)
- Tuya, de la Riva, Suárez-Cabal & Blanco, "Coverage-Aware Test Database Reduction", TSE 2016. Reduces an initial (possibly production) database to a subset that keeps the same SQL coverage. Evaluated on "two real life applications and a well-known database benchmark". Status: **[lead]**; the full text is at the uniovi repository, but my fetch returned an HTML landing page. Class: EXP. — [DOI 10.1109/tse.2016.2519032](https://doi.org/10.1109/tse.2016.2519032)
- Yan, Nath & Lu, "Generating Test Databases for Database-Backed Applications" (DBGriller), ICSE 2023. Status: **[documented]**. Class: EXP. — [NSF PAR PDF](https://par.nsf.gov/servlets/purl/10447174)
  - In a study of 30 applications, conditions of "more than half of the branches" depend on the database. Existing tests "with developer provided test databases, cover only 55% of the DB-dependent branches".
  - Using a crash oracle, DBGriller found 34 unhandled-exception cases in 6 apps: 22 actual bugs, 12 confirmed by developers, 3 fixed. 4 were false positives caused by constraint-violating test databases.
- The search extracts also surfaced DOMINO and SchemaAnalyst (Alsharif, Kapfhammer, McMinn) for relational-schema test data, and X-Data for killing SQL mutants. Status: **[lead]**. — [search extract; arXiv 1411.6704 "Data Generation for Testing and Grading SQL Queries"](https://arxiv.org/pdf/1411.6704)

**Testing data-intensive / DISC / big-data systems.**

- Felderer, Russo & Auer, "On Testing Data-Intensive Software Systems", Springer chapter 2019 (in *Security and Quality in Cyber-Physical Systems Engineering*). Status: **[documented]**. — [arXiv 1903.09413](https://arxiv.org/pdf/1903.09413)
  - It lists "Difficult Generation of Adequate, High-Quality Data" as a QA challenge: "data provided for testing should represent realistic and application-specific data in order to meaningfully test a data-intensive system", which "makes test data generation and management a challenging task".
  - The challenge list builds on Hummel et al., "A Collection of Software Engineering Challenges for Big Data System Development", SEAA 2018, which lists 26 challenges. Status of Hummel et al.: **[lead]**. — [DOI 10.1109/seaa.2018.00066](https://doi.org/10.1109/seaa.2018.00066)
- Gulzar, Mardani, Musuvathi & Kim, "White-box testing of big data analytics with complex user-defined functions" (BigTest), ESEC/FSE 2019. Status: **[documented]**. Class: EXP. — [author PDF](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)
  - "Despite ultra-large scale input data size, real world DISC applications are often significantly skewed and inadequate in terms of test coverage, leaving 34% of Joint Dataflow and UDF (JDU) paths untested."
  - "Only few of the data records (order of tens) are actually required to achieve the same JDU coverage as the entire production data."
  - It reveals 2x more injected faults than the prior approach (Sedge).
  - "The common industry practice for testing these applications remains running them locally on randomly sampled inputs, which obviously does not flush out bugs hiding in corner cases."
- Morán, de la Riva & Tuya, "Testing data transformations in MapReduce programs" (MRFlow), A-TEST 2015. Uses data-flow criteria over input-to-output transformations, motivated by "poor quality data" from varied sources. Status: **[lead]**. Class: EXP. — [DOI 10.1145/2804322.2804326](https://doi.org/10.1145/2804322.2804326)

**Field testing ("ex-vivo", "in-vivo", "offline").**

- Bertolino et al., "A Survey of Field-based Testing Techniques", ACM Computing Surveys 2021. Status: **[documented]**. — [CNR repository PDF](https://iris.cnr.it/bitstream/20.500.14243/401252/2/prod_453662-doc_174541.pdf)
  - It defines **ex-vivo testing** as "any type of software testing performed in-house using information extracted from the field". It calls ex-vivo testing "very useful for the testing of applications processing large amounts of structured data that are costly and/or difficult to build artificially".
  - It defines **offline field testing** as testing "in the production environment on an instance of the SUT different from the one that is operational".
  - It explicitly excludes field-failure-reproduction work (BugRedux/F3-style crash-based generation) as debugging, not field testing.
- Orso, Apiwattanapong & Harrold, "Leveraging field data for impact analysis and regression testing", ESEC/FSE 2003 (Gamma). Status: **[lead]**. — [DOI 10.1145/940071.940089](https://doi.org/10.1145/940071.940089)
- Elbaum & Hardojo assessed techniques for enhancing a test suite with field data from profiling a web application, as summarised by Bertolino et al. 2021. Status: **[lead]**; the primary source was not retrieved. — [Bertolino et al. CNR PDF](https://iris.cnr.it/bitstream/20.500.14243/401252/2/prod_453662-doc_174541.pdf)

**Production-driven test generation / test amplification.**

- Danglot et al., "A snowballing literature study on test amplification", JSS 2019. Status: **[documented]**. — [arXiv 1705.10692](https://arxiv.org/pdf/1705.10692)
  - It coins "test amplification", with the keywords "test augmentation; test optimization; test regeneration".
  - It notes "missing terminological consensus".
  - Its seeds came from 70 DBLP hits, of which 4 were selected, followed by backward and forward snowballing.
- Tiwari, Zhang, Monperrus & Baudry, "Production Monitoring to Improve Test Suites" (Pankti), IEEE Trans. Reliability 2021/22. Generates differential unit tests and oracles from production executions. Status: **[lead]**. Class: EXP. — [arXiv 2012.01198](https://arxiv.org/pdf/2012.01198)
- Tiwari et al., "Mimicking Production Behavior With Generated Mocks" (RICK), TSE 2024. Status: **[lead]**. Class: EXP. — [DOI 10.1109/tse.2024.3458448](https://doi.org/10.1109/tse.2024.3458448)
- Wang & Orso, "Mimicking User Behavior to Improve In-House Test Suites" (Replica), ICSE 2019 companion. Uses field data to guide symbolic execution toward behaviours not exercised in-house. Status: **[lead]**. Class: EXP. — [DOI 10.1109/icse-companion.2019.00133](https://doi.org/10.1109/icse-companion.2019.00133)

**Statistical / usage-based testing ("operational profile").**

- Musa, "Operational profiles in software-reliability engineering", IEEE Software 1993. "Using an operational profile to guide testing ensures that ... the most-used operations will have received the most testing." Status: **[lead]**. Class: EST (reliability engineering practice). — [DOI 10.1109/52.199724](https://doi.org/10.1109/52.199724)
- Soltana, Sabetzadeh & Briand, "Synthetic data generation for statistical testing", ASE 2017. Generates a "synthetic population of citizens' records for testing a public administration IT system" that is statistically representative and logically valid. Status: **[lead]**; the full text was **[unreachable]**. Class: EXP. — [DOI 10.1109/ase.2017.8115698](https://doi.org/10.1109/ase.2017.8115698)

**Model-based / field-data-based data processing system testing (Briand group, SnT Luxembourg).**

- Di Nardo, Pastore & Briand, "Generating Complex and Faulty Test Data through Model-Based Mutation Analysis", ICST 2015. Mutates field data, guided by a UML/OCL data model, to produce faulty inputs for a satellite data-acquisition system. Status: **[lead]**. Class: EXP. — [DOI 10.1109/icst.2015.7102589](https://doi.org/10.1109/icst.2015.7102589)
- Di Nardo, Pastore & Briand, "Augmenting Field Data for Testing Systems Subject to Incremental Requirements Changes", TOSEM 2017. Starts from "When testing data processing systems, software engineers often use real-world data to perform system-level testing". It modifies field data so it covers new requirements, and reports more coverage than tests written by experienced engineers. Status: **[lead]**; the full text was **[unreachable]**. Class: EXP. — [DOI 10.1145/3053430](https://doi.org/10.1145/3053430)
- Soltana, Sabetzadeh & Briand, "Practical Constraint Solving for Generating System Test Data", TOSEM 2020 (PLEDGE). Gives the triad that real data is "(1) incomplete ... (2) incompatible ... (3) inaccessible ... Because of these factors, system testing is done, by and large, using synthetic data". It is evaluated on three industrial case studies, one being the Government of Luxembourg personal income tax system. Status: **[documented]**. Class: EXP. — [arXiv 1902.00397](https://arxiv.org/pdf/1902.00397)
- Shan & Zhu, "Generating structurally complex test cases by data mutation", The Computer Journal 2007/09. "Data mutation" generates many test inputs from a few seeds. Status: **[lead]**. — [DOI 10.1093/comjnl/bxm043](https://doi.org/10.1093/comjnl/bxm043)

**ETL / data-warehouse testing.**

- Golfarelli & Rizzi, "A comprehensive approach to data warehouse testing", DOLAP 2009. Says that "not much has been said about data warehouse testing". Status: **[lead]**. — [DOI 10.1145/1651291.1651295](https://doi.org/10.1145/1651291.1651295)
- Homayouni (MSc thesis, Colorado State, 2018) and the companion IDEAS 2018 paper. Status: **[documented]** for the thesis abstract and summary pages. Class: EXP. — [thesis PDF](https://mountainscholar.org/bitstream/10217/189268/1/Homayouni_colostate_0053N_14638.pdf)
  - "Balancing tests" are generated from source-to-target mappings and check that data in the target warehouse is consistent with the sources.
  - Evaluated on a health data warehouse (Health Data Compass, University of Colorado Anschutz). It "can find previously undetected real faults in the ETL implementation".
  - Mutation analysis was run "on mock source data".

**Data validation ("unit tests for data").**

- Schelter et al., "Automating large-scale data quality verification", VLDB 2018 (Amazon; known as Deequ). Provides a "declarative API ... enables 'unit tests' for data". It validates data, not code. Status: **[lead]**. Class: EST (deployed in production per the abstract). — [DOI 10.14778/3229863.3229867](https://doi.org/10.14778/3229863.3229867)
- Foidl, Golendukhina, Ramler & Felderer, "Data pipeline quality: Influencing factors, root causes of data-related issues, and processing problem areas for developers", JSS 2024. A taxonomy of 41 factors from a multivocal literature review, 8 expert interviews, and GitHub/Stack Overflow mining. Status: **[lead]**. — [DOI 10.1016/j.jss.2023.111855](https://doi.org/10.1016/j.jss.2023.111855)

**Record linkage / entity resolution evaluation (non-SE community).**

- Christen & Vatsalan, "Flexible and extensible generation and corruption of personal data", CIKM 2013 (GeCo). Says "privacy concerns make it challenging to obtain real" personal data for evaluating record matching and de-duplication. Status: **[lead]**; the full text at ANU was **[unreachable]** (connection failure). — [DOI 10.1145/2505515.2507815](https://doi.org/10.1145/2505515.2507815)
- Lam, Boyd, Linacre, Blackburn & Harron, "Generating synthetic identifiers to support development and evaluation of data linkage methods", Int. J. Population Data Science 9(1), July 2024. Status: **[documented]** (abstract and introduction). — [UCL Discovery PDF](https://discovery.ucl.ac.uk/10194216/1/ijpds-09-2389.pdf)
  - They measured real within-person identifier disagreement in ALSPAC: 18% of surnames and 12% of forenames.
  - Synthetic identifiers reproduced linkage-quality metrics within 0.13–0.55% for missed matches and 0.00–0.04% for false matches.
  - "Replicating dependencies between attribute values ..., identifier disagreements ... and their patterns" made the synthetic data useful.

**Official statistics ("synthetic data spectrum").**

- ONS Methodology Working Paper 16, "Synthetic data pilot" (Bates, Špakulová, Dove, Mealor). Undated; references from 2017, so I infer late 2017 to 2018. Status: **[documented]** via WebFetch. — [ONS](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)
  - It defines a six-level spectrum. Level 1, "synthetic structural", is "for very basic code testing, no analytical value, no disclosure risk". Level 2, "synthetic valid", is "for advanced code testing ... minimal disclosure risk".
  - The higher levels range up to a "replica" intended for secure facilities.

**The term "test data management".** This is predominantly a practitioner and vendor term, covering masking, subsetting and provisioning of production copies.
- The Perforce/Delphix 2026 report (518 respondents) lists "relying heavily on production data copies (25%)" and long access lead times (22%) as top challenges. Status: **[vendor]**, search extract. — [Perforce](https://www.perforce.com/resources/pdx/state-of-test-data-management-report/quality-paradox)
- The K2view 2025 report claims that 7% of companies are fully compliant in testing. Status: **[vendor]**, search extract. — [K2view](https://www.k2view.com/2025-state-of-test-data-management/)
- Fischbach et al., ESEM 2020: an interview study with 18 practitioners from 12 companies that lists test data as one of six problematic test artifacts. Status: **[lead]**. — [arXiv 2009.01722](https://arxiv.org/pdf/2009.01722)

### Inferences
- **[inferred]** The most direct terminological match for "tests on fictional data miss defects that real data exposes" comes from the privacy chain (Grechanik 2010, then PRIEST 2011, then PISTIS 2014, alongside kb-/kbe-anonymity 2011/2012). These papers frame "testing utility" as preserved code coverage or program-path behaviour. None of them frames utility as detected defects on real data. Their direction is "release transformed real data outward", which matches the stated setting (only approved derived information may leave). Their subjects are small open-source Java DCAs.
- **[inferred]** "Ex-vivo testing" (Bertolino et al. 2021) is the best-defined umbrella term for "in-house tests informed by production information". "Offline field testing" fits running tests in the protected environment. The search terms "data-centric testing" and "production-like test data" did not surface any academic anchor of their own. "Production-like" appears mainly in industry and position papers (e.g. Behjati et al. 2024).
- **[inferred]** Record-linkage evaluation uses "synthetic data with known ground truth" to measure linkage *quality*, not to find implementation defects. Its corruption models (GeCo; Lam et al. 2024's dependency between identifier errors and attributes) are the closest available descriptions of how real multi-source identifier messiness looks. Using them for defect detection is an untested transfer.
- **[inferred]** Citation-chain structure as seen in the full texts:
  - Masserini 2024 cites kb-anonymity and Castro 2008.
  - The Bertolino 2021 survey cites the Elbaum/Hardojo and Morán/Tuya ex-vivo works.
  - Felderer 2019 builds on Hummel 2018.
  - Danglot 2019 is the hub for amplification.
  - The privacy chain and the database-test-generation chain rarely appear to cite each other. This is based only on the reference lists I saw (Grechanik 2010 and Masserini 2024); I did not do a systematic citation analysis.

### Gaps
- I could not run a Semantic Scholar forward-citation crawl (HTTP 429), so I cannot report what currently cites Grechanik 2010, kb-anonymity or BigTest.
- I found no dedicated academic term or paper chain for "testing of entity resolution implementations" (as opposed to evaluating ER quality), for "reconciliation testing", or for "incremental-processing correctness testing" in data platforms. This is absence of evidence from my searches, not proof that the topics are unaddressed.
- Shadow testing, traffic replay and dark launching were not investigated in this track.
- Primary sources on field failure reproduction (BugRedux, Jin & Orso ICSE 2012; F3, ISSTA 2013) were not retrieved. They are cited here only through Bertolino et al.'s description.

---

## Which systematic literature reviews / mapping studies anchor the field?

### Takeaway
There are SLRs or surveys for field testing (2021), test amplification (2019), big-data testing (2022/23), big-data QA (2020), data-warehouse testing (a 2018 survey chapter), and, most on point, synthetic test data without access to real raw data (2026). None of them targets "fictional fixtures missing real-data defects in data platforms" directly. The 2026 review concludes that most privacy-preserving test-data methods **require access to real data**, and that **test-data evolution** is largely unaddressed. I did not find an SLR specifically on database-application test data generation, or on privacy-preserving software testing.

### Cited Findings

**Tammisto, Shah, Rodriguez & Pfahl, "The challenge of generating and evolving real-life like synthetic test data without accessing real-world raw data – a Systematic Review".** Published in Expert Systems (Wiley), 2026, DOI 10.1111/exsy.70164; arXiv 6 Feb 2026. Status: **[documented]**. — [arXiv 2602.06609](https://arxiv.org/pdf/2602.06609)
- Context: Estonian e-Government X-Road data services, where pre-production tests run without production data.
- It follows Kitchenham's method. The search returned 1,013 records (IEEE Xplore 210, ACM DL 402, Scopus 401). Data were extracted from 75 publications, yielding 37 approaches.
- "A common prerequisite for using these methods and tools is direct access to real-life data". 29 included publications were excluded because they used real data as generation input.
- Nine approaches came closest. Most of these are rule-based generation, plus one Successive Random Addition method, one rendering-tool approach and one simulation approach. None covered all four research-question facets, and none supports data evolution.
- "Synthetic test data evolution is a field that has not received much attention."

**Bertolino et al., "A Survey of Field-based Testing Techniques", ACM CSUR 2021.** Status: **[documented]**. — [CNR PDF](https://iris.cnr.it/bitstream/20.500.14243/401252/2/prod_453662-doc_174541.pdf)
- Describes itself as the "first systematic survey" of field testing: 80 studies.
- "Ex-vivo testing strategies are still largely under-explored."
- "In-vivo testing approaches heavily rely on data from the final production environment."
- "Privacy and security issues are still largely unaddressed. Only 8 studies out of 80 (10%) address such aspects."
- "Most ex-vivo and offline field testing approaches focus on functional requirements."

**Danglot et al., "A snowballing literature study on test amplification", JSS 2019** (arXiv v4, 2022). Status: **[documented]**. — [arXiv 1705.10692](https://arxiv.org/pdf/1705.10692)
- Four categories: adding new tests as variants of existing ones; synthesizing new tests with respect to changes; modifying test execution; modifying existing test code.
- The papers in its summary table were published 2003–2017.
- It reports no terminological consensus.

**Arshad, Alsamhi & Afzal, "Big Data Testing Techniques: Taxonomy, Challenges and Future Trends", CMC 74(2), 2023** (issue published 31 Oct 2022). Status: **[documented]** via WebFetch of the HTML full text (first 100k characters). — [TechScience](https://www.techscience.com/cmc/v74n2/50213/html)
- An SLR of 2010–2021 literature. The search returned 1,975 records, narrowed to 41 primary studies.
- Combinatorial testing was the most-applied test-data technique.
- ETL testing challenges come mainly from volume and from "discrepancies in transformed and transmitted data". Manual validation was the bottleneck.
- Most challenges arise in MapReduce validation.

**Zhang et al. (exact author list not verified), "Quality Assurance Technologies of Big Data Applications: A Systematic Literature Review", Applied Sciences 10(22), 2020.** 83 primary studies. Status: **[lead]**. — [MDPI PDF](https://www.mdpi.com/2076-3417/10/22/8052/pdf?version=1605263855)

**Felderer, Russo & Auer 2019.** An *exploratory*, explicitly non-systematic literature study. A Google Scholar + IEEE search for "Data-Intensive System" AND "Software Testing" returned 133 papers, of which 16 were relevant; 117 of 133 were false positives. Status: **[documented]**. — [arXiv 1903.09413](https://arxiv.org/pdf/1903.09413)

**Homayouni, Ghosh & Ray, "Data Warehouse Testing", Advances in Computers vol. 112, 2018/19.** A survey chapter with a classification framework for DW testing approaches. Status: **[lead]**; the chapter full text was not retrieved, and the companion thesis was read. — [O'Reilly listing](https://www.oreilly.com/library/view/advances-in-computers/9780128151228/S0065245817300578.xhtml); [thesis](https://mountainscholar.org/bitstream/10217/189268/1/Homayouni_colostate_0053N_14638.pdf)

**IoTBDS 2024, "Overcoming the Complexity of Quality Assurance for Big Data".** Described in the search extract as an SLR of testing/QA for big-data systems. Status: **[lead]**. — [SciTePress](https://scitepress.org/publishedPapers/2024/127421/pdf/index.html)

**A FedCSIS (vol. 35) survey of two decades of test data generation, which states that it is *not* an SLR.** Status: **[lead]**. — [annals-csis](https://annals-csis.org/Volume_35/drp/9829.html)

**Foidl et al., JSS 2024.** A multivocal literature review of data-pipeline quality: 41 influencing factors. Status: **[lead]**. — [DOI 10.1016/j.jss.2023.111855](https://doi.org/10.1016/j.jss.2023.111855)

### Inferences
- **[inferred]** Two reviews converge on two key gaps:
  - Bertolino 2021: ex-vivo testing is under-explored, and privacy is addressed in 10% of studies.
  - Tammisto 2026: methods usually need real data, and evolution is missing.
  - Together they suggest that the combination "real data stays inside, only derived artefacts leave, fixtures must keep up with changing sources" sits in an under-reviewed intersection.
- **[inferred]** That intersection is not empty. kb-anonymity, PISTIS, Tuya's reduction, BigTest's minimisation and Lam et al.'s synthetic identifiers each produce a *derived* artefact from real data inside a protected setting. No review groups them together.
- **[inferred]** The big-data testing SLRs (Arshad 2022/23; Applied Sciences 2020) are organised by technique and V-characteristics, not by the fixture-realism problem. They are useful for terminology, but less so as evidence on this specific defect class.

### Gaps
- I found no SLR or mapping study dedicated to (a) test data generation for database applications, (b) privacy-preserving software testing as a whole, or (c) testing of non-ML data pipelines / ETL after 2018. The searches returned unrelated SLRs. This is absence from my searches only; IEEE Xplore, ACM DL and Scopus were not queried directly.
- The full texts of the Homayouni et al. 2018 chapter, the Applied Sciences 2020 SLR and the IoTBDS 2024 SLR were not read. Their headline findings are leads only.

---

## Which industrial case studies and engineering reports address this exact problem?

### Takeaway
Peer-reviewed industrial evidence on *fictional fixtures missing real-data defects in data platforms* is thin. The closest are:
- Briand-group case studies with SnT industrial partners: the Luxembourg tax system and a satellite data-acquisition system (SES).
- A health data warehouse thesis (Homayouni 2018).
- A Norwegian tax-administration / national-registry position paper (2024).
- The Estonian X-Road motivation in Tammisto 2026.

Practice reports (blogs and ADRs) document a recurring failure mode, fabricated data not matching production nullability and distribution. They also document a recurring workaround, running the pipeline on *sampled production data*, but give no defect counts. Most "case studies" found are vendor marketing.

### Cited Findings

**Peer-reviewed or academic, with industrial context**

- Soltana, Sabetzadeh & Briand, TOSEM 2020 (PLEDGE). Three industrial case studies. Case material includes the Government of Luxembourg personal income tax system test data model (UML/OCL). The motivating triad is that real data is "incomplete", "incompatible", or "inaccessible ... due to ... data protection and privacy". Status: **[documented]**. Class: EXP. — [arXiv 1902.00397](https://arxiv.org/pdf/1902.00397)
- Soltana et al., ASE 2017. "A realistic evaluation ... where we generate a synthetic population of citizens' records for testing a public administration IT system." Status: **[lead]**. — [DOI 10.1109/ase.2017.8115698](https://doi.org/10.1109/ase.2017.8115698)
- Di Nardo et al., ICST 2015 and TOSEM 2017. A satellite data-acquisition system, with field data mutated or augmented. The tests "achieve more code coverage than the test cases implemented by experienced software engineers". Status: **[lead]**. — [ICST 2015](https://doi.org/10.1109/icst.2015.7102589); [TOSEM 2017](https://doi.org/10.1145/3053430)
- Homayouni 2018 thesis. A health data warehouse with sources "with different data models running on different platforms". Balancing tests "can find previously undetected real faults in the ETL implementation". Status: **[documented]** (abstract and summary). — [thesis PDF](https://mountainscholar.org/bitstream/10217/189268/1/Homayouni_colostate_0053N_14638.pdf)
- Behjati, Arisholm, Bedregal & Tan, "Synthetic Test Data Generation Using Recurrent Neural Networks: A Position Paper", arXiv July 2024 (venue not verified). Status: **[documented]**. Class: PROP. — [arXiv 2407.05410](https://arxiv.org/pdf/2407.05410)
  - Authors are from Testify AS and Skatteetaten (the Norwegian Tax Administration).
  - Context: a shared integration-test environment around the Norwegian National Registry. "Many organizations, particularly within the public sectors, are not allowed to use production data for testing."
  - They compare anonymized and synthetic data. Anonymization suits streaming new production data and "may better resemble the real data", but is vulnerable to linking attacks, and "it is not easy to downscale or upscale the dataset".
  - The LSTM generator was evaluated only in preliminary experiments.
- Tammisto et al. 2026. The motivating industrial problem is that "there is no test data in Estonia that is dedicated to testing applications that use X-Road data service responses", while much X-Road production traffic is sensitive. Status: **[documented]**. — [arXiv 2602.06609](https://arxiv.org/pdf/2602.06609)
- Grechanik et al. 2010. Industrial framing from Accenture Technology Labs co-authors: owners of DCAs (banks, insurers, government) outsource testing but cannot share data, and fake data "trigger exceptions ... that would not occur when the DCAs are tested with original data". This is argued, not measured. Status: **[documented]**. — [author PDF](https://ranger.uta.edu/~csallner/papers/grechanik10is.pdf)
- BigTest (Microsoft Research / UCLA). The paper asserts, without a measured industrial survey, that common industry practice is to test locally on randomly sampled inputs. Status: **[documented]**. — [author PDF](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)

**Official statistics and public sector (guidance and policy)**

- The ONS synthetic data pilot (c. 2017–18, inferred date) defines levels 1–2 as suitable for code testing, with no analytical value. Status: **[documented]**. — [ONS WP16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)
- The ONS synthetic data policy: synthetic data can substitute "in testing ... when real data is inaccessible", and "It should be expected that synthetic data will not accurately reflect all properties of the real data." Status: **[lead]**. — [ONS policy](https://www.ons.gov.uk/aboutus/transparencyandgovernance/datastrategy/datapolicies/syntheticdatapolicy)
- The ONS Data Science Campus: "mock and low-fidelity data are commonly used for testing data processing pipelines". Status: **[lead]**. — [ONS DSC](https://datasciencecampus.ons.gov.uk/projects/synthetic-data-for-public-good)
- The Statistics Canada starter guide (from the UNECE/HLG-MOS guide) lists "testing software" as a synthetic-data use case. Status: **[lead]**. — [StatCan](https://www.statcan.gc.ca/en/data-science/network/synthetic-data)
- CBS (Statistics Netherlands) 2023 says synthetic data are useful for testing new IT systems. Status: **[lead]**. — [CBS](https://www.cbs.nl/en-gb/corporate/2023/20/synthetic-data-opens-up-possibilities-in-the-statistical-field)
- The Welsh Government Data Science Unit uses a DummyData approach for testing pipelines. Status: **[lead]**. — [wgdsu](https://wgdsu.github.io/DummyData)
- A UK ICO case study describes a bank using third-party generated synthetic data to test a vulnerable-customer detection system. This is a regulator publication; the system is ML-adjacent. Status: **[lead]**. — [ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/case-studies/synthetic-data-to-test-the-effectiveness-of-a-vulnerable-persons-detection-system-in-financial-services)

**Engineering blogs and decision records (practice reports)**

- GetYourGuide (Jean Carlo Machado, 7 Dec 2023), "DDataflow". Status: **[blog]**, documented via WebFetch. Class: EST (in-house). — [GetYourGuide](https://www.getyourguide.careers/posts/ddataflow-a-tool-for-data-end-to-end-tests-for-machine-learning-pipelines)
  - They tried unit tests with synthetic data but found them hard to get right. Synthetic scenarios "may not resemble production", and failures arise "at the integration of components rather than in their units".
  - They now sample production data in CI.
  - It is used in "a majority of our production data products". No defect counts are given.
- Every Cure ADR, "Improve testing through sampling" (page footer date July 2026; decision date not stated). Status: **[blog]**, documented via WebFetch. — [Every Cure docs](https://docs.dev.everycure.org/infrastructure/architecture_decision_records/improve_testing_through_sampling/)
  - The Data Fabricator generates schema-matching synthetic data but misses errors due to drift. "The biggest issue ... is related to non-nullable columns in fabricated data, while being nullable in production."
  - Decision: update fabricator parameters from production, semi-automatically, and run on a production sample that preserves ground-truth-pair proportions.
- Google Cloud Dataflow docs recommend unit tests on small reference datasets and a preproduction project mirroring production for end-to-end checks. This is vendor documentation describing practice. Status: **[lead]**. — [Google Cloud docs](https://docs.cloud.google.com/dataflow/docs/guides/develop-and-test-pipelines)

**Vendor material (capability references only)**

- Synthesized (a Deutsche Bank case claiming an 80% cut in provisioning time), IBM Optim (de-identifying cloned multi-TB production databases), EPI-USE (anonymizing a 2TB SAP system for external test teams), and a Tricentis deck (a quoted 95% drop in test-environment cost). All **[vendor]**, search extracts only. — [Synthesized](https://synthesized.io/case-studies/modernizing-qa-with-compliant-scalable-test-data-infrastructure); [IBM](https://public.dhe.ibm.com/software/fr/c2_im3.pdf); [EPI-USE](https://www.epiuselabs.com/snop-success-story?hsLang=de); [Tricentis via SlideShare](https://de.slideshare.net/ChelseaFrischknecht/test-data-management-the-underestimated-pain)
- Wells Fargo with the MIT-IBM lab describes masking production data and temporarily bringing production data into test environments, and flags the risk of real data leaking into synthetic output. Status: **[lead]**. — [MIT-IBM](https://mitibm.mit.edu/?p=10704)

### Inferences
- **[inferred]** The practice reports (GetYourGuide, Every Cure) name concrete fixture-realism failure modes: nullability mismatch, distribution drift, and integration-level failures. These match the brief's concern. Their remedy, running tests on sampled production data, assumes that tests can run where production data lives. That is compatible with the stated protected environment, but it moves the defect *signal* rather than the fixtures outside.
- **[inferred]** The strongest industrial data points are public-sector (Luxembourg, Norway, Estonia, UK ONS) and health (Colorado HDW). I found no peer-reviewed bank or insurer case study. Bank and insurer evidence is vendor marketing or regulator case studies.

### Gaps
- I found no peer-reviewed industrial study that *quantifies* how many defects were missed by hand-written fixtures and later exposed by real data in a data platform. The practice reports are qualitative.
- No large-tech engineering blog (e.g. Netflix, Uber, Airbnb, Shopify) on this exact problem was retrieved in this track. This is not evidence that none exists.
- The Wells Fargo, Deutsche Bank and IBM materials were not read in full.

---

## Which approaches are directly comparable to the stated problem, and which are only neighbouring techniques?

### Takeaway
"Directly comparable" here means an approach that uses real data (or its properties) inside a protected boundary to produce derived test artefacts or verdicts, with the aim of exercising implementation logic or detecting defects. Approaches that meet this:
- behaviour/coverage-preserving anonymization: kb-anonymity, PRIEST, PISTIS
- coverage-preserving reduction or minimisation of production data: Tuya 2016, BigTest
- failure-preserving input transformation: Castro 2008, Camouflage, Masserini 2024
- field-data augmentation or mutation: Di Nardo 2015/2017
- coverage-driven test-database generation from developer seeds: DBGriller
- source-to-target balancing tests: Homayouni

All of these are **experimentally demonstrated** on small or few subjects. None is established in practice as a named method. Established practice consists of production-copy masking and subsetting ("test data management"), running pipelines on sampled production data, data validation checks, and operational-profile testing. Their bearing on defect detection in multi-source entity resolution or reconciliation is **inferred**.

### Cited Findings

**Directly comparable (the target is test effectiveness of derived or synthetic data relative to real data)**

| Approach | What leaves / what is produced | Evidence of effect | Class | Status |
|---|---|---|---|---|
| Grechanik et al. ISSRE 2010 (guided k-anonymity) | anonymized DB | coverage >70% → <30% at k ≥ 7; small Java DCAs | EXP | [documented] |
| PRIEST (Taneja et al. FSE 2011) | DB anonymized by effect on program | coverage "preserved at a higher level" | EXP | [lead] |
| kb-anonymity (PLDI 2011); kbe-anonymity (ASE 2012) | behaviour-preserving replaced tuples | path coverage maintained; 3 Java programs (kbe) | EXP | [lead] |
| PISTIS (ICST 2014) | sanitized + minimized DB (centroids) | coverage "close" to original, 2 apps | EXP | [lead] |
| Castro et al. ASPLOS 2008; Camouflage ICSE 2011 | failure-inducing input with same path / same failure | bugs reproduced, little or no private info | EXP | [lead] |
| Masserini et al. AST 2024 | anonymized failure data (Android) | reproduction rates by technique, 19 failures | EXP | [documented] |
| Coverage-aware test DB reduction (Tuya et al. TSE 2016) | small subset with same SQL coverage | large reduction, 2 real apps + benchmark | EXP | [lead] |
| BigTest (FSE 2019) | synthesized minimal inputs for Spark-style dataflows | production data leaves 34% JDU paths untested; tens of records match full-data coverage; 2x injected faults | EXP | [documented] |
| DBGriller (ICSE 2023) | mutated test DB states from developer seeds | developer DBs cover 55% of DB-dependent branches; 22 real bugs (12 confirmed) | EXP | [documented] |
| Di Nardo et al. ICST 2015 / TOSEM 2017 | mutated or augmented field data | more coverage than engineer-written tests (satellite system) | EXP | [lead] |
| Homayouni 2018 (balancing tests) | source-to-target assertions | real ETL faults found in a health DW | EXP | [documented] |
| Lam et al. IJPDS 2024 (synthetic identifiers) | synthetic identifiers replicating error dependencies | linkage metrics within 0.13–0.55% (missed) / 0.00–0.04% (false) | EXP (evaluation-quality target, not defects) | [documented] |

Sources: [Grechanik](https://ranger.uta.edu/~csallner/papers/grechanik10is.pdf); [PRIEST](https://doi.org/10.1145/2025113.2025143); [kb](https://doi.org/10.1145/1993498.1993551); [kbe](https://doi.org/10.1145/2351676.2351718); [PISTIS](https://doi.org/10.1109/icst.2014.36); [Castro](https://doi.org/10.1145/1346281.1346322); [Camouflage](https://doi.org/10.1145/1985793.1985797); [Masserini](https://arxiv.org/pdf/2402.07460); [Tuya](https://doi.org/10.1109/tse.2016.2519032); [BigTest](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf); [DBGriller](https://par.nsf.gov/servlets/purl/10447174); [Di Nardo 2015](https://doi.org/10.1109/icst.2015.7102589); [Di Nardo 2017](https://doi.org/10.1145/3053430); [Homayouni](https://mountainscholar.org/bitstream/10217/189268/1/Homayouni_colostate_0053N_14638.pdf); [Lam](https://discovery.ucl.ac.uk/10194216/1/ijpds-09-2389.pdf)

**Neighbouring techniques (applicability to the stated problem only inferred)**

- **Synthetic generation without real data.** Rule-based or constraint-based generators (PLEDGE; the nine closest approaches in Tammisto 2026), SQL-query test data generation (EvoSQL), and DBMS-oriented generators (QAGen, DataSynth). These target coverage or constraint satisfaction from schemas and models. They do not target realism of multi-source discrepancies. Status: **[documented]** for PLEDGE and Tammisto, **[lead]** for the rest. — [PLEDGE](https://arxiv.org/pdf/1902.00397); [Tammisto](https://arxiv.org/pdf/2602.06609); [EvoSQL](https://doi.org/10.1145/3180155.3180202); [QAGen](https://doi.org/10.1145/1247480.1247520); [DataSynth](https://doi.org/10.1145/1989323.1989395)
- **Statistical / operational-profile testing.** Musa 1993; Soltana ASE 2017. These target reliability estimation through usage-representative data. The brief puts statistical resemblance out of scope as an end. Status: **[lead]**. — [Musa](https://doi.org/10.1109/52.199724); [Soltana 2017](https://doi.org/10.1109/ase.2017.8115698)
- **Production-driven test generation / amplification.** Pankti, RICK, Replica, Gamma. These capture production executions to create unit tests or mocks. They assume that captured objects can be used in-house, and their privacy handling is not part of their design per the abstracts. Status: **[lead]**. — [Pankti](https://arxiv.org/pdf/2012.01198); [RICK](https://doi.org/10.1109/tse.2024.3458448); [Replica](https://doi.org/10.1109/icse-companion.2019.00133); [Gamma](https://doi.org/10.1145/940071.940089)
- **Data validation in production.** Deequ / "unit tests for data". These check the data, not the code that transforms it. Status: **[lead]**. — [Schelter et al. VLDB 2018](https://doi.org/10.14778/3229863.3229867)
- **Record-linkage synthetic generators** (FEBRL/GeCo lineage). These are designed for evaluating linkage algorithm quality, not for finding implementation defects. Status: **[lead]**. — [GeCo CIKM 2013](https://doi.org/10.1145/2505515.2507815)
- **Sampling production data in CI** (GetYourGuide, Every Cure). Practice, with qualitative reported benefit. Status: **[blog]**. — [GetYourGuide](https://www.getyourguide.careers/posts/ddataflow-a-tool-for-data-end-to-end-tests-for-machine-learning-pipelines); [Every Cure](https://docs.dev.everycure.org/infrastructure/architecture_decision_records/improve_testing_through_sampling/)

**Results that run against the assumption that real data is a sufficient oracle for adequacy**
- BigTest shows that the *entire production dataset* left 34% of JDU paths untested. "Using the entire big data for testing does not necessarily" achieve the best coverage. Status: **[documented]**. — [BigTest](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)
- Soltana et al. list "incomplete" real data, meaning insufficient to exercise every behaviour, as a reason to synthesize. Status: **[documented]**. — [arXiv 1902.00397](https://arxiv.org/pdf/1902.00397)

### Inferences
- **[inferred]** The stated problem has two halves that the literature treats separately:
  - (a) fictional fixtures miss real-data behaviours. The evidence is DBGriller's 55% coverage of DB-dependent branches by developer fixtures, Grechanik's coverage loss, and the nullability and drift failures in the practice reports.
  - (b) real data itself under-exercises logic. The evidence is BigTest's 34% and Soltana's "incomplete".
  - A comparable solution therefore probably needs both real-data-derived information and systematic generation. This is an engineering inference, not a demonstrated result.
- **[inferred]** None of the directly comparable approaches was evaluated on a multi-source entity-resolution or reconciliation pipeline with differing identifiers, coverage and reporting delays. The nearest are Homayouni's multi-source health DW (ETL balancing), Lam et al.'s identifier-error modelling (linkage evaluation), and BigTest's dataflow programs. Transfer to the brief's setting is inferred.
- **[inferred]** Most directly comparable approaches assume white-box program analysis of the system under test (symbolic or concolic execution, program slicing, branch projection). This matches the brief, since the implementation logic is owned. But it constrains which approaches can run inside a protected environment, which may lack such tooling.
- **[inferred]** Nearly all evidence is coverage-based (code, path, branch, JDU, SQL coverage). Defect evidence is limited: DBGriller's 22 bugs, Homayouni's "previously undetected real faults", BigTest's injected faults, and Castro/Camouflage's reproduction of known failures. The link from preserved coverage to preserved defect detection is assumed rather than demonstrated in the privacy chain.

### Gaps
- No approach found addresses *temporal* aspects such as reporting delays, late-arriving records or incremental reprocessing in fixture realism. Tammisto 2026's finding that "evolution" is unaddressed is the nearest documented gap statement.
- Many directly comparable works were read only as abstracts: PRIEST, kb/kbe-anonymity, PISTIS, Tuya 2016, Castro, Camouflage, Di Nardo. Their numeric results beyond the abstracts are unverified.
- I could not establish whether any of the experimental approaches has industrial adoption beyond the research evaluation. I found no adoption reports, which is absence of evidence only.
