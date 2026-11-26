# Real executions expose what fictional fixtures miss

No published work fully solves the stated problem: making entirely fictional fixtures expose the defects that real data exposes in a multi-source platform with entity resolution, reconciliation and incremental processing. The problem has instead been attacked in pieces, across at least seven literatures and under different names. These include test-data anonymisation and "behaviour-preserving" anonymisation, test database generation, testing of data-intensive (DISC) applications, ex-vivo and offline field testing, test amplification, and ETL "balancing tests".

The closest solutions share one documented principle. **They measure and derive inside the boundary.** The same instrumented code runs on real data and on fixtures, and the two are compared on what they exercise or kill: coverage, SQL test requirements, invariants and mutants. Only derived artefacts leave: gap lists, counts, or solver-generated inputs that follow a real execution path.

The evidence that this matters is concrete but comes from small studies:

- **Developer-supplied test databases** covered only **55% of database-dependent branches** across 30 applications (DBGriller, ICSE 2023).
- **In-house tests** missed **52.6% of the temporal invariants** observed in the field (Wang, Brun and Orso, ICST 2017).
- **Full production data** itself left **34% of Spark dataflow paths** unexercised, while **tens of synthesised records** matched its coverage (BigTest, ESEC/FSE 2019).

Real data is therefore a guide to adequacy, not an oracle of it.

Every directly comparable approach has been demonstrated experimentally, but only on small or few subjects: Java database applications, C utilities, Android apps, Spark benchmarks and one health data warehouse. None has been evaluated on entity resolution, reconciliation or delivery-sequence logic, and none has documented industrial adoption. Established practice does something else. It tests on real data inside the protected environment (shadow runs, write-audit-publish, data-quality checks), or it gives up on fictional fixtures and runs on sampled production data.

Two limits are evidence, not gaps:

- Theory gives no partition- or criterion-based guarantee that fixtures are equivalent to real inputs for unknown faults (Hamlet and Taylor 1990).
- Failure-preserving transformation cannot in general leak zero information. Camouflage still revealed about 30% of input bits on average.

The other open problems are absences of evidence in the literature searched, not demonstrations that they cannot be solved. They are adequacy criteria specific to entity resolution and reconciliation, temporal realism in fixtures, relational-aware tooling that reduces and then anonymises, and disclosure accounting for repeated pass/fail releases.

## How to read the evidence in this report

Every substantive claim carries a label taken from the research notes. **[D]** means a research track read the full text, or the relevant full section, of the primary source. **[A]** means only the abstract, or the abstract plus targeted passages, of a downloaded full text was read. **[L]** means a lead: search extract, metadata or a secondary citation only, which is not enough to rest a verdict on. **[B]** marks an engineering blog, architecture decision record or project documentation read in full: a practice report, not a controlled study. **[V]** marks an unverified vendor or rights-holder claim. **[U]** means the source was unreachable. **[I]** marks an engineering inference drawn in the notes or in this synthesis.

Where it matters, claims are also typed by evidence kind: *theoretical result*, *empirical finding*, *documented practice*, *engineering inference* or *unverified vendor claim*. Approaches are classed **EST** (established in practice), **EXP** (experimentally demonstrated in a research evaluation) or **PROP** (proposal or position paper).

**Where tracks disagreed, this report uses the stronger evidence:**

- **Camouflage (Clause and Orso).** Two tracks read it as abstract-only. Two others read the full study in the 2009 Georgia Tech technical report and in Clause's May 2011 thesis chapter. This report uses those full texts [D]; the ICSE 2011 version itself was not retrieved.
- **PRIEST and PISTIS.** One track had abstracts only. Another read the author PDFs, which are used here [D].
- **Grechanik et al. 2010.** Read in full by two tracks [D], overriding a third track's abstract-level reading.
- **Inozemtseva and Holmes 2014.** One track found it unreachable, but another read it at cs.ubc.ca [D].
- **Papadakis et al. 2018.** A lead in one track, read in full in another [D].
- **mutmut's licence.** Recorded as BSD-3-Clause in one track and inferred as BSD-style from the copyright header in another. This report says BSD-style.
- **BigTest's fault benchmark.** Described as "31 faulty DISC applications" in two tracks and as seeded faults "in 7 programs" in a third. This report reads both as one benchmark of manually seeded faulty versions.
- **Masserini et al.'s 41% figure.** Two tracks attribute it to numeric local suppression and one to generalisation. This report follows the two that agree.

**Corrections to the citations supplied with the brief** (all from the notes):

| Cited as | Correct |
|---|---|
| kb-anonymity, ICSE 2011 | **PLDI 2011**, pp. 447–457, DOI 10.1145/1993498.1993551 ([SMU record](https://ink.library.smu.edu.sg/sis_research/1390)) |
| "Lucia et al. 2012" | **kbe-anonymity**, ASE 2012, the evolving-programs follow-up ([DOI](https://doi.org/10.1145/2351676.2351718)) |
| BigTest, ICSE 2019 | **ESEC/FSE 2019** ([author PDF](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)) |
| Eder et al., ICSM 2013 | **AST 2013** workshop at ICSE ([TUM PDF](https://wwwbroy.in.tum.de/publ/papers/AST13Hauptmann.pdf)) |
| SQLSolver, 2024 | **PACMMOD 1(4), SIGMOD, December 2023** ([NSF PAR](https://par.nsf.gov/servlets/purl/10548354)) |
| EvoSQL with Zaidman | Castelein, Aniche, Soltani, Panichella, van Deursen, ICSE 2018; Zaidman is not an author ([TU Delft](https://repository.tudelft.nl/record/uuid:90a6431f-f78f-4ac3-bf87-c052cd9cd5d4)) |
| "Li et al." (sanitising databases) | PISTIS, Li, Grechanik, Poshyvanyk et al., ICST 2014 ([author PDF](https://www.cs.wm.edu/~denys/pubs/ICST'14-PISTIS-CRC.pdf)) |
| "Lin & Reiter verification server" | Lin & Reiter, "Differentially Private Verification of Survey-Weighted Estimates", arXiv 2404.02519, April 2024 ([arXiv](https://arxiv.org/abs/2404.02519)) |

Several primary sources stayed unreachable: Castro et al. 2008 (full text), kb- and kbe-anonymity, Soltana et al. ASE 2017, Di Nardo et al. TOSEM 2017, Hydra, F3, Olston et al. 2009, and the CJEU BHB judgment text. Claims resting on them are labelled accordingly.

The earlier report on the same platform, *Synthetic stand in test data*, had a different objective, statistical resemblance. It is used here only as background for questions 7 and 8, and its framing is not adopted.

## 1. Seven literatures solve pieces of the problem, and none owns it

The problem has no single name. Felderer, Russo and Auer state outright that "testing of data-intensive systems is not yet an established and clearly-defined term". Their exploratory search returned 133 papers, of which 117 were false positives ([Felderer et al. 2019, arXiv 1903.09413](https://arxiv.org/pdf/1903.09413)) [D]. Danglot et al.'s snowballing review of test amplification likewise reports "missing terminological consensus" ([Danglot et al., JSS 2019](https://arxiv.org/pdf/1705.10692)) [D].

The relevant work is spread across seven software-engineering communities, plus two adjacent fields: record-linkage evaluation and official statistics. The privacy and database-generation chains rarely cite each other. That observation rests only on the reference lists the prior-art track read, not on a systematic citation analysis [I].

| Community | Terms to search | Anchor works | Strongest status |
|---|---|---|---|
| Privacy-preserving testing and debugging | test data anonymisation, behaviour-preserving anonymisation, test outsourcing, "database-centric applications" | Castro et al. ASPLOS 2008; Grechanik et al. ISSRE 2010; Camouflage ICSE 2011; kb-anonymity PLDI 2011; PRIEST FSE 2011; kbe-anonymity ASE 2012; PISTIS ICST 2014; Masserini et al. AST 2024 | EXP |
| Database-application testing | test database generation, database-state generation, test database reduction, SQL coverage | Emmi et al. ISSTA 2007; SQLFpc STVR 2010; Tuya et al. TSE 2016; EvoSQL ICSE 2018; EvoMaster TOSEM 2020; DBGriller ICSE 2023 | EXP |
| Data-intensive / DISC / big-data testing | JDU paths, dataflow testing, DISC applications | BigTest FSE 2019; BigFuzz ASE 2020; BigSift SoCC 2017; Holey 2026 | EXP |
| Field testing | ex-vivo, in-vivo, offline field testing | Bertolino et al. CSUR 2021 (survey of 80 studies); Orso et al. 2003 (Gamma) | EXP |
| Production-driven generation and amplification | test amplification, production monitoring, carving | Danglot et al. JSS 2019; Pankti 2021; RICK TSE 2024; Replica 2019; Elbaum carving TSE 2009 | EXP |
| ETL / warehouse testing | balancing tests, source-to-target validation | Golfarelli & Rizzi DOLAP 2009; Homayouni 2018 | EXP (one thesis) |
| Statistical / usage-based testing | operational profile, statistical testing | Musa 1989/1993; Soltana et al. ASE 2017 | EST (reliability practice) |
| Record-linkage evaluation (non-SE) | synthetic identifiers, data corruption models | GeCo CIKM 2013; Lam et al. IJPDS 2024 | evaluation-quality target, not defects |
| Official statistics (non-SE) | synthetic data spectrum, "synthetic structural/valid" | ONS Working Paper 16 | documented guidance |

Bertolino et al. define the best umbrella term. **Ex-vivo testing** is "any type of software testing performed in-house using information extracted from the field", and they call it "very useful for the testing of applications processing large amounts of structured data that are costly and/or difficult to build artificially". **Offline field testing**, which runs "in the production environment on an instance of the SUT different from the one that is operational", fits tests executed inside the protected environment. The same survey finds that "ex-vivo testing strategies are still largely under-explored" and that only **8 of 80 studies (10%)** address privacy or security ([Bertolino et al., ACM CSUR 2021](https://iris.cnr.it/bitstream/20.500.14243/401252/2/prod_453662-doc_174541.pdf)) [D].

The review closest to the brief is Tammisto et al.'s 2026 systematic review of synthetic test data generated without access to real raw data. It screened 1,013 records and extracted 37 approaches from 75 publications. Its conclusions are that "a common prerequisite for using these methods and tools is direct access to real-life data", that 29 publications had to be excluded because they used real data as generation input, and that "synthetic test data evolution is a field that has not received much attention" ([Tammisto et al., Expert Systems 2026, arXiv 2602.06609](https://arxiv.org/pdf/2602.06609)) [D].

The most direct statement of the brief's problem is still Grechanik et al.'s. They argue that "fake data lacks many of the intricate semantic connections among the original data elements". They also show that k-anonymity at k ≥ 7 dropped test coverage "to less than 30% from the original coverage of more than 70%", although only on four Java programs of 0.8–4.3K NCLOC and measuring coverage rather than defects ([Grechanik et al., ISSRE 2010](https://ranger.uta.edu/~csallner/papers/grechanik10is.pdf)) [D, empirical].

The established, experimental and proposal tiers separate cleanly. **Established in practice** are four things:

- masking and subsetting production copies, a practitioner and vendor field known as "test data management";
- running pipelines on sampled production data;
- data validation checks;
- operational-profile testing.

None of these is evaluated for defect detection in multi-source entity resolution. **Experimentally demonstrated** are all the directly comparable research approaches: behaviour- or coverage-preserving anonymisation, coverage-preserving reduction, failure-preserving input transformation, field-data mutation, test-database generation and balancing tests. **Proposals** include the Norwegian Tax Administration and Testify position paper on recurrent-neural-network generation, which reports only preliminary experiments ([Behjati et al., arXiv 2407.05410, 2024](https://arxiv.org/pdf/2407.05410)) [D, PROP], and the model-driven approach to entity-reconciliation testing (A-TEST 2016, below).

Peer-reviewed industrial evidence comes mainly from the public sector and health. The Luxembourg tax system appears in PLEDGE, a satellite data-acquisition system in Di Nardo et al., the Norwegian National Registry in Behjati et al., Estonian X-Road services in Tammisto et al., and a University of Colorado health data warehouse in Homayouni's thesis. The prior-art track found no peer-reviewed bank or insurer case study; that material was vendor marketing [V].

Two practice reports describe the failure mode in the brief's own terms:

- **GetYourGuide** tried unit tests on synthetic data and found that scenarios "may not resemble production" and that failures arise "at the integration of components rather than in their units". It now samples production data in CI ([GetYourGuide DDataflow, 7 Dec 2023](https://www.getyourguide.careers/posts/ddataflow-a-tool-for-data-end-to-end-tests-for-machine-learning-pipelines)) [B].
- **Every Cure** found that its schema-matching data fabricator missed drift, and that "the biggest issue … is related to non-nullable columns in fabricated data, while being nullable in production". It decided to update fabricator parameters from production, semi-automatically, and to run on a production sample ([Every Cure ADR](https://docs.dev.everycure.org/infrastructure/architecture_decision_records/improve_testing_through_sampling/)) [B]. The page footer is dated July 2026; the decision date is not stated.

Neither report gives defect counts. The full prior-art catalogue, split into directly comparable and neighbouring approaches, follows the nine questions.

## 2. Coverage locates unexercised logic; mutation and oracle metrics expose weak tests

### Data-logic coverage criteria exist, but coverage predicts fault detection only weakly

SQL-specific adequacy is well defined. **SQLFpc** applies masking MC/DC to SQL and covers "selection, joining, grouping, aggregations, subqueries, case expressions and null values". It handles NULLs explicitly and treats outer joins through "outer increments". Its test requirements are "coverage rules" that "are executable and able to determine whether the different situations expressed by the test requirements are covered by the test data". Executed queries can be captured with DBMS tracing or p6spy. The supporting evidence is a mutant-based case study by the criterion's own authors ([Tuya, Suárez-Cabal & de la Riva, STVR 2010](https://giis.uniovi.es/testing/papers/stvr-2010-sqlfpc.pdf)) [D].

Because the rules are queries that return covered or not-covered, they could run on real data inside the boundary, and only rule identifiers and flags would need to leave [I]. The adequacy track found no maintained, packaged SQLFpc tool and no independent validation against real SQL faults [D: gap].

For Spark-style programs, BigTest's **Joint Dataflow and UDF (JDU) path** criterion is the analogue ([Gulzar et al., ESEC/FSE 2019](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)) [D]. dbt-coverage, by contrast, "checks your dbt project for missing documentation and tests". It measures whether tests are attached, not whether logic is exercised ([dbt-coverage README](https://raw.githubusercontent.com/slidoapp/dbt-coverage/main/README.md)) [D].

Whether coverage predicts defect detection is the crux, and the answer is "weakly":

- **Inozemtseva and Holmes** generated 31,000 suites over five systems of up to 724,000 lines. They found "a low to moderate correlation between the coverage of a test suite and its effectiveness when its size is controlled for", and that "using a fixed coverage value as a quality target is unlikely to produce an effective test suite" ([ICSE 2014](https://cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf)) [D, empirical, mutant-measured].
- **Chekam et al.** removed the "Clean Program Assumption" and used real C faults. They found that "for statement, branch and weak mutation testing … increased coverage has little or no effect on fault revelation". Strong mutation had the highest fault revelation, but only above a threshold ([ICSE 2017](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)) [D, empirical].

The defensible reading is that coverage targets find *unexercised* logic. They do not certify fault-detection ability [I, consistent with both papers].

### Mutation analysis is the best available proxy, with known blind spots

Mutation is the most studied adequacy proxy, and its validity is contested:

- **Just et al.** used 357 Defects4J faults. They found mutant detection correlates with real-fault detection "independently of code coverage". Only **73% of real faults** are coupled to common mutants, 10% need stronger operators, and **17% are not coupled at all** ([FSE 2014](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)) [D].
- **Papadakis et al.** found that once suite size is controlled, "all correlations between mutation scores and real fault detection are weak". Choosing suites by mutation score still beats random suites of equal size, so mutants are good guidance but weak predictors ([ICSE 2018](https://coinse.github.io/publications/pdfs/Papadakis2018aa.pdf)) [D].
- **Google's data** covers almost 15 million mutants. It shows developers exposed to mutants "write more tests" and gives "evidence that mutants are indeed coupled with real faults". It also says exhaustive mutation of a large code base is "impracticable" ([Petrović et al., ICSE 2021](https://arxiv.org/pdf/2103.07189)) [D].

Equivalent and other ineffective mutants carry a measurable cost. In schema mutation they make up **up to 24%** of mutants and changed the score of 33 of 34 schemas ([McMinn et al., TSE 2019](https://eprints.whiterose.ac.uk/126146/1/ineffective-mutants.pdf)) [D].

Data-platform operator sets are thin. Three families exist:

- SQL query mutation, in the SQLFpc line of work.
- Schema-constraint mutation (SchemaAnalyst).
- RDD-only dataflow mutation for Spark (TRANSMUT-Spark). It has 15 data-flow and transformation operators, including filter and distinct deletion, and reduction rules for equivalent mutants. It supports Scala 2.12 only and is not published to a repository ([de Souza Neto et al., arXiv 2108.02589](https://arxiv.org/pdf/2108.02589); [README](https://raw.githubusercontent.com/jbsneto-ppgsc-ufrn/transmut-spark/master/README.md)) [D].

No mutation tool was found for PySpark DataFrames, pandas transformations or dbt SQL [D: gap].

Two kinds of mutation also need to be kept apart:

- **Code mutation** asks whether fixtures plus assertions distinguish the program from faulty variants. This is the question the validity studies address.
- **Data mutation** asks whether validators detect corrupted rows. No validity study of data mutation as a test-adequacy criterion was found [I].

### Oracle adequacy and vacuous passes are measurable

Coverage says nothing about whether results are checked, and three metrics target that gap:

- **Checked coverage** (Schuler and Zeller) takes the dynamic slice of statements that actually influence an oracle. They note that "it is perfectly possible to achieve a 100% coverage and still not have any result checked", and found checked coverage more sensitive to oracle quality than mutation in seven projects ([ICST 2011](https://www.st.cs.uni-saarland.de/publications/files/schuler-icst-2011.pdf)) [D]. It needs dynamic slicing, which exists for Java but was not found for SQL or Spark [I].
- **Pseudo-tested methods** are covered methods whose body can be deleted without any test failing. They made up **6–72% of methods (mean 35.48%)** in Niedermayr et al. ([CSED 2016](https://arxiv.org/pdf/1611.07163)) [D], and exist in all 21 projects studied by Vera-Pérez et al. ([EMSE 2019](https://arxiv.org/pdf/1807.05030)) [D]. PIT's Descartes engine detects them [D].
- **Assertion count and assertion coverage** correlate strongly with mutation-measured effectiveness ([Zhang & Mesbah, FSE 2015](https://people.ece.ubc.ca/amesbah/resources/papers/fse15.pdf)) [D]. A later study reportedly disputes this [L].

Data tooling has a structural vacuous-pass mode. A dbt data test is a query that returns violating rows, and "if the test returns zero rows, your assertion passes" ([dbt data tests](https://docs.getdbt.com/docs/build/data-tests)) [D]. Every generic test (unique, not_null, relationships) therefore passes on an empty model, and so does any check over fixtures whose join keys never match. Only a non-emptiness assertion, or a mutation that empties an upstream input, separates "no violations" from "nothing tested" [I]. Whether pandera, Great Expectations or Soda behave the same way on zero rows was not verified [D: gap].

### Separating inadequate inputs, inadequate assertions and wrong implementations

The standard decomposition is Reachability–Infection–Propagation(–Revealability), also known as Voas's PIE ([L] for the originals). Tools implement its first cut directly. PIT reports "No coverage" when no test reached the mutated line, which points to inadequate input. It reports "Survived" when the line was reached but the mutant went undetected, which points to propagation or oracle inadequacy, or to an equivalent mutant ([PIT basic concepts](https://pitest.org/quickstart/basic_concepts/)) [D].

Reneri automates the second cut. It splits undetected extreme mutations into no-infection (inputs too weak), no-propagation, and weak-oracle. In **63% of cases** the existing tests did infect the program state, so most misses were observability or oracle problems, "there is no dominant root cause", and its suggestions led to tests detecting 77% of previously undetected transformations ([Vera-Pérez et al., arXiv 1909.04770](https://arxiv.org/pdf/1909.04770)) [D]. Weak kills versus strong kills is a practical infection-versus-propagation split ([Chekam et al. 2017](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)) [D].

On 386 real bugs, failed error propagation was "negligible" at unit level but "increases substantially" for system-level inputs ([arXiv 2011.10787](https://arxiv.org/pdf/2011.10787)) [D]. That matters for end-to-end pipeline fixtures, where a later deduplication or aggregation can overwrite an earlier corruption. It argues for per-stage assertions [I].

Applied to a data platform, the notes infer a four-way triage [I]:

- **Not covered.** An uncovered mutant, rule or SQLFpc requirement names the missing data situation.
- **Covered but masked.** The mutant changed an intermediate table but not the asserted output: assert on intermediates or compare whole tables.
- **Failing on the original program.** A failure under a fixture the specification agrees with is an implementation error or a wrong expectation. Telling these apart needs an independent specification, such as the business-rule MC/DC of Blanco, Tuya and Seco, built so that tests can expose faults where "the implementation does not fulfil the system specification" ([arXiv 2304.12671](https://arxiv.org/pdf/2304.12671)) [D].
- **Equivalent mutant.** A survivor that no input can kill is a cost, not a defect.

Chekam et al.'s finding that adequacy measured on one program version may not hold for the faulty version warns against reading adequacy from a single snapshot ([ICSE 2017](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)) [D].

### Data-specific adequacy is thin

Combinatorial t-way coverage measurement scores any existing fixture table as "the proportion of t-way combinations of n variables for which all variable-values configurations are fully covered" ([NIST IR 7878, 2012](https://nvlpubs.nist.gov/nistpubs/ir/2012/NIST.IR.7878.pdf)) [D]. Run over binned variables such as source, null pattern, identifier type and delay bucket, on real data inside and on fixtures outside, it would yield a list of combinations that are present in real data and absent from the fixtures. That list is an aggregate and still needs small-cell review [I].

The only adequacy-oriented work on entity reconciliation is a position-level paper. Blanco et al.'s A-TEST 2016 "first approach" derives test requirements for reconciliation applications from business rules and reports no defect-detection results ([A-TEST 2016](https://giis.uniovi.es/testing/papers/a-test-2016-testing-entity-reconciliation.pdf)) [D, PROP]. Entity-resolution literature otherwise measures accuracy against truth sets, which is a different question. A 2017 paper warns that error rates from rules designed on a truth set "may not necessarily translate well to the full dataset" ([UALR ICIQ 2017](https://ualr.edu/informationquality/p12-iciq2017-the-challenges-of-truth-sets)) [L]. A 2026 preprint proposes "divergence witnesses" for faults in sameness rules ([arXiv 2607.20729](https://arxiv.org/pdf/2607.20729)) [L].

No validated adequacy criterion was found for ETL, entity-resolution matching, incremental processing or late-arriving data [D: gap, absence of evidence].

## 3. Path conditions and call sequences carry behaviour without records, but only for known failures

### Captured signals, from least to most disclosing

The literature documents a spectrum of execution information that has been captured where the data lives and used to build or improve tests elsewhere.

| Signal captured inside | Representative work | What it enabled | What it reveals | Evidence |
|---|---|---|---|---|
| Execution frequency per code region | Google Productive Coverage; Musa operational profile | Prioritising untested code by production use; selecting tests by usage | Aggregate counts only | [D] industrial RCT; [D] Musa 1989 |
| Crash stack trace | STAR; EvoCrash | Crash reproduction: 59.6% exploited (STAR, 52 crashes); 85% (EvoCrash, 54 crashes) vs 33% for coverage-driven EvoSuite | Call stack | [A], [D] |
| Call sequence | BugRedux | 16 of 17 field failures reproduced; 1–50% overhead | "Unlikely to reveal" values (anecdotal) | [D] |
| Field invariant violations + call sequences | Replica / VASE | Covered 56.0% of untested field invariants vs 4.7% for random KLEE | Behaviour, plus observed value domains (VASE) | [D] |
| Path condition of a failing run | Castro et al.; Camouflage; ReMoTe | New input on the same failing path; all 170 Camouflage inputs reproduced | ~30% of input bits on average; constants on branches | [L] Castro; [D] Camouflage, ReMoTe |
| Attribute-to-branch mapping | PRIEST; PISTIS; kb-anonymity | Anonymisation that preserves coverage or behaviour | Swapped real values or centroids leave | [D], [D], [L] |
| Query plans with per-operator cardinalities | Hydra | Regenerated database matching operator row counts (volumetric target) | Exact counts plus predicate constants | [L], [U] full text |
| Serialised production objects | Pankti; RICK; PROZE; carving | Differential, mock-based or parameterised unit tests | Real argument values | [D], [D], [A], [A] |
| Mutated or augmented field data | Di Nardo et al. ICST 2015 / TOSEM 2017 | Faulty or requirement-covering inputs for a satellite system | Field data itself | [L], [U] |

Sources: [Productive Coverage, ICSE-SEIP 2024](https://homes.cs.washington.edu/~rjust/publ/productive_coverage_icse_2024.pdf); [Musa & Ackerman 1989](https://www.rose-hulman.edu/class/csse/csse376/Resources/musa.pdf); [STAR, TSE 2015](https://people.csail.mit.edu/hunkim/papers/chen-tse2015.pdf); [EvoCrash, TSE 2018](https://pure.tudelft.nl/ws/files/72125983/08502801.pdf); [BugRedux TR](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2011/git-cercs-11-06.pdf); [Wang thesis 2019](https://repository.gatech.edu/server/api/core/bitstreams/fbbb8c33-f80f-4852-afda-249c1cb047a4/content); [Castro et al.](https://doi.org/10.1145/1346281.1346322); [Camouflage TR](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf); [ReMoTe](https://infoscience.epfl.ch/record/186762/files/main.pdf); [PRIEST](https://cdn.sanity.io/files/ku3lep2e/production/b448b278e0967a3a039f49eebe06870146e93839.pdf?dl=); [PISTIS](https://www.cs.wm.edu/~denys/pubs/ICST'14-PISTIS-CRC.pdf); [kb-anonymity](https://doi.org/10.1145/1993498.1993551); [Hydra](https://dsl.cds.iisc.ac.in/publications/conference/hydra_vldb.pdf); [Pankti](https://arxiv.org/pdf/2012.01198); [RICK](https://arxiv.org/pdf/2208.01321); [PROZE](https://arxiv.org/pdf/2407.00768); [Di Nardo 2015](https://doi.org/10.1109/icst.2015.7102589); [Di Nardo 2017](https://doi.org/10.1145/3053430).

### Camouflage: the strongest result on the record-free end

Camouflage is the most fully documented work in this group. It replays a captured failing execution, symbolically executes it to get the path condition φ, and picks an input that satisfies φ, still causes the failure, and "reveals as little information about I as possible". On 170 inputs (NanoXML, printtokens, Columba, htmlparser), every sanitised input reproduced its failure. Generating the path condition took 162–533 s on average ([Clause & Orso TR GIT-CERCS-09-14](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf)) [D].

The authors rejected statistics-preserving database anonymisation as "not suitable for our scenario" because "the conditions for reproducing a failure are typically very specific" [D]. That is the clearest documented answer to whether execution capture can substitute for statistical characterisation, and the answer is yes, for reproducing a known failure.

### BugRedux: how much to capture

BugRedux supplies a calibration of signal level. Point-of-failure and call-stack guidance were insufficient for 4 of 17 failures. In grep, gzip, htget and aspell, call-stack guidance produced executions with the same stack that did not fail. Complete branch traces "provide too much guidance", produce solver-intractable constraints, and carry 8–1,066% overhead. Call sequences were the sweet spot ([Jin & Orso TR](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2011/git-cercs-11-06.pdf)) [D].

### Field-driven generation beats coverage-driven generation

Coverage-driven generation is a poor proxy for field behaviour:

- Wang, Brun and Orso found that EvoSuite augmentation "slightly improved the test suites in terms of coverage, but not at all in terms of killed mutants and behavioral invariants". Some code exercised by both tests and the field "was used in a behaviorally different way" ([ICST 2017](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf)) [D].
- EvoCrash's authors conclude that "coverage-based test generation lacks adequate guidance for crash reproduction" ([TSE 2018](https://pure.tudelft.nl/ws/files/72125983/08502801.pdf)) [D].

### Value-level anonymisation of real inputs loses reproducibility

Masserini et al. applied five anonymisation techniques to 19 failures in 17 Android apps ([AST 2024](https://arxiv.org/pdf/2402.07460)) [D]. Reproduction success was:

- **11–19%** for plain local suppression of strings;
- **49%** on average for special-character-driven suppression;
- **41%** for numeric local suppression;
- **up to 63%** when more of the original value was disclosed.

Cases where only a tiny value domain triggers the bug, such as 29 February, fell below 10%.

### What must be captured

What has to be captured depends on the goal [I]:

- **Reproducing a known failure:** a path condition or call sequence. A crash type plus stack trace suffices for many Java crashes.
- **Finding untested field behaviour:** invariant violations or call orders. Replica's instrumented build averaged 13% overhead.
- **Steering where tests are written:** frequency counts, as in Productive Coverage.

PRIEST adds the data-specific piece. Program analysis maps each database attribute to the branches it controls; its example is `if (nationality == "Palauan" && age > 60)`. Branch-hit counts over that mapping are the information a fixture builder would want. PRIEST computes the mapping inside but releases swapped data, not counts ([PRIEST](https://cdn.sanity.io/files/ku3lep2e/production/b448b278e0967a3a039f49eebe06870146e93839.pdf?dl=)) [D; the use of counts is I].

PRIEST also documents the industrial setting. Interviews at IBM, Accenture, two health insurers, a biopharma firm, two supermarket chains and three banks found that "current test data anonymization is manual, laborious, and error-prone", and describe "cleanroom testing" with monitored testers and no network or USB access [D, documented practice]. That is the brief's protected environment.

### Data-platform signals: no evidence either way

No peer-reviewed study or documented engineering practice was found that uses data-quality rule hit counts, reject-reason counts or entity-resolution decision statistics, captured inside, to build fixtures outside [D: gap]. This is absence of evidence. The only practitioner material proposes inventorying rules and the "edge cases that actually break them", scoring the catch rate, and refreshing fixtures from production failures, with no evaluation ([DataMagnet blog, 2026](https://www.datamagnet.co/post/synthetic-data-testing-data-quality-rules/)) [V].

### Can execution capture replace statistical characterisation?

The evidence supports a layered answer [I]:

- **Reproducing known failures:** execution capture is documented to be sufficient.
- **Exposing untested field behaviour:** behavioural abstractions outperform coverage, shown on small C and Java programs.
- **Broadly exposing unknown defects in multi-source relational pipelines:** no study compares execution-capture fixtures with statistically characterised data either way.

Execution capture says which paths real data took. It does not describe cross-source joint structure, such as duplicates across sources, identifier collisions and reporting delays, that has not yet triggered a distinct path. It also says nothing about paths no real record has taken yet [I]. The brief's question therefore remains open, not answered negatively.

## 4. Generators handle relational state and missing joins; none handles ambiguous identity or delivery order

### White-box database generators

White-box concolic methods generate both program inputs and the database records that drive query-dependent paths. Emmi, Majumdar and Sen capture concrete SQL at run time because it "cannot be inferred precisely by statically looking" at the code. Their solver may fail where arithmetic and string constraints interact ([ISSTA 2007](https://typeset.io/pdf/dynamic-test-input-generation-for-database-applications-1hfczwa77z.pdf)) [D]. Pan, Wu and Xie generate inputs for an *existing* database state ([Pan dissertation](https://ninercommons.charlotte.edu/record/1287/files/Pan_uncc_0694D_10385.pdf)) [A; empirical claims L]. That is the setting closest to running against protected data [I]. No maintained release of either was found.

XData generates datasets that kill SQL query mutants:

- It covers join type, missing join conditions, comparison operators, aggregation and DISTINCT, LIKE, HAVING, NULLs and some subqueries.
- It worked for 17 of 22 TPC-H and university queries.
- ORDER BY mutations "in general, cannot be caught" by datasets alone.
- On 14 student assignments, its datasets outperformed predefined datasets and teaching-assistant grading.

([Chandra et al., arXiv 1411.6704](https://arxiv.org/pdf/1411.6704)) [D]. No public repository was found [D: absence].

DBGriller is the most directly relevant recent result. It mutates developer-provided test databases to cover database-dependent branches. Using a crash oracle it found 34 unhandled-exception cases in 6 applications: **22 actual bugs, 12 confirmed by developers, 3 fixed**, plus 4 false positives caused by test databases that violated constraints ([Yan, Nath & Lu, ICSE 2023](https://par.nsf.gov/servlets/purl/10447174)) [D].

### Search-based generation

EvoMaster is the only maintained OSS tool found that co-generates multi-table relational state, with foreign-key closure, alongside operation sequences against a running service [I from D]. Its generated INSERTs respect primary, foreign, unique and check constraints. Generating SQL data directly raised coverage by up to **+16.5%** and found "7 new unique" faults across five open-source APIs ([Arcuri & Galeotti, TOSEM 2020](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications/2020_tosem.pdf)) [D]. Two qualifications apply:

- The SQL heuristics alone helped significantly on only 2 of 5 SUTs.
- On the industrial API, "SQL heuristics do not help the search if the SUT code dealing with SQL is not even reached due to failed input validation" [D, unsuccessful].

Its oracle is generic (5xx responses, schema mismatches, security), so a reconciliation error that returns 200 goes undetected without user-written assertions [I].

EvoSQL, which works at the level of a single query, fully covered **98.6%** of 2,135 real queries, against 6.5% for random search ([ICSE 2018](https://repository.tudelft.nl/file/File_6c2d74fc-0c7b-4248-b0a8-decdf4360c20)) [D]. It has been dormant since 2019. SchemaAnalyst, which targets schema constraints, has been dormant since 2021.

### Dataflow generators

BigTest symbolically executes UDFs and models dataflow operators logically. It explicitly generates join "terminating cases": keys only on the left, only on the right, or on neither side, because "the output can contain rows with null entries, which are an important source of bugs". It also models `flatMap`/`reduce` collections and string-split constraints, with loops unrolled to a bound K (default 2) ([BigTest](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf)) [D]. These terminating cases are the closest documented mechanism for systematically generating missing-record and partial-coverage cases across sources. They still assume a single key equality and have no notion of ambiguous identity [I].

BigFuzz rewrites Spark programs into framework-independent equivalents and applies schema-aware mutations drawn from a study of common Spark and Hadoop error types. It detected **80.6% more seeded errors than BigTest** on 52 error-seeded versions of 12 applications ([Zhang et al., ASE 2020](http://web.cs.ucla.edu/~miryung/Publications/ase2020-bigfuzz.pdf)) [D]. Byte-level random mutation "can hardly generate meaningful data" [D]. Both tools are research prototypes, last committed in 2022 and 2021.

### Grammar, constraint and property-based tools

These tools are maintained, but cross-record relations must be written by hand:

- **FANDANGO** evolves inputs against grammars with quantified constraints and Python expressions ([Fandango reference](https://raw.githubusercontent.com/fandango-fuzzer/fandango/main/docs/_static/fandango.pdf)) [D].
- **Hypothesis stateful testing** provides `Bundle`s, "a named collection of generated values that can be reused by other operations". They establish a universe of keys, so later records reference earlier identifiers, duplicates recur across "sources", and delete-then-reference sequences arise ([Hypothesis stateful docs](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/master/hypothesis/docs/stateful.rst)) [D; ER application I].

None of these ships a relational or foreign-key model [D].

### Temporal and stateful checking

The strongest defect evidence for history-based checking is **Elle**. It chooses operations, such as list-append, whose observations reveal version order. It "revealed anomalies in every system we tested", and "almost all of these anomalies were previously unknown" ([Kingsbury & Alvaro, VLDB 2020](https://arxiv.org/pdf/2003.10554)) [D]. Model-based tools exist (GraphWalker, fMBT, Modelator for TLA+), but no application of them to CDC, watermarking or late-arriving data in pipelines was found [D: gap].

The nearest transferable pattern is incremental-view-maintenance testing. Its invariant is that incremental results "must be identical to recomputing the query from scratch", checked in a shadow mode and with random SQL generation ([pg_trickle blog](https://pgxn.org/dist/pg_trickle/0.37.0/blog/shadow-mode-correctness-fuzzing.html)) [L/V].

### Coverage of the brief's concerns, and what each tool needs

| Brief concern | Best documented mechanism | Evidence | Status |
|---|---|---|---|
| Relational, multi-table state | EvoMaster INSERT genes with FK closure; XData/EvoSQL per query | +16.5% coverage, 7 faults; 98.6% query coverage | [D] |
| Missing records / partial coverage | BigTest join terminating cases; XData outer-join mutants | 2x seeded faults vs Sedge | [D] |
| Conflicts and ambiguous identities | none found | — | gap |
| Temporal dependencies, delivery sequences | Hypothesis/QuickCheck state machines; Elle-style histories | Elle: anomalies in all 4 databases tested | [D] for databases; pipelines gap |
| Database-dependent branches from seeds | DBGriller | 22 real bugs, 12 confirmed | [D] |

Every approach needs either source code or instrumentation (concolic methods, BigTest, BigFuzz, white-box EvoMaster), or a hand-written specification (grammar, schema, state model, TLA+). **None of the documented tools needs real rows.** Several can use real rows or an existing database state as seeds or context: Pan et al., BigFuzz seeds, and EvoMaster against a pre-populated database [D/I]. No source documents a deployment where a generator runs on protected data and exports only derived artefacts [D: gap].

## 5. Independent evaluation rests on real-fault replay, and equivalence to real inputs cannot be proven

### Non-circular scoring means real faults the method was not tuned on

The accepted non-circular test of a generation method is to count the real, developer-fixed faults it detects in an artefact it was not tuned on. The fault counts as detected only if the test passes on the fixed version and fails on the buggy one, with reruns to remove flaky tests ([Shamshiri et al., ASE 2015](http://www.evosuite.org/wp-content/papercite-data/pdf/ase15_faults.pdf)) [D].

Applied to Defects4J's 357 faults, Randoop, EvoSuite and AgitarOne together detected 55.7% of faults, but individual generated suites detected only **19.9%**. Many faulty statements were covered without the fault being revealed, and 15.2% of generated tests were flaky [D]. Benchmarks assembled automatically from CI can mislead: only 112 of 3,091 BugSwarm pairs (3.6%) were suitable for fault-localisation or repair studies ([Durieux & Abreu 2019](https://arxiv.org/pdf/1905.09375)) [D].

Coverage as the optimisation target can hurt. Gay et al. report coverage-directed generation up to 93.4% worse than random on some systems ([TSE 2015](https://conservancy.umn.edu/bitstream/handle/11299/217451/15covrisks.pdf?sequence=1)) [L].

Circularity also appears inside the best data-pipeline results. BigFuzz's mutation operators and its seeded faults come from the same error taxonomy, so generator and evaluation share one criterion [I]. The notes infer three scoring tiers [I]:

- real historical faults of the codebase itself, replayed fixed-versus-buggy;
- faults injected with operators taken from a taxonomy not used to build the fixtures;
- mutation score, only with suite size controlled.

Practitioners rarely evaluate generators independently. Among 30 Jane Street property-based-testing users, effectiveness was judged mainly by inspecting example outputs (8/30), then code coverage (2/30) and property coverage (1/30), and "the difficulty of evaluating their effectiveness" was a main complaint ([Goldstein et al., ICSE 2024](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice.pdf)) [D].

### Evidence that generated data finds real, previously unseen defects

That evidence is strong for engines and weak for application pipelines:

- **SQLancer's pivoted query synthesis** reported 123 bugs in SQLite, MySQL and PostgreSQL, of which 99 were fixed or verified ([Rigger & Su, OSDI 2020](https://arxiv.org/pdf/2001.04174)) [D].
- **Holey** found 17 previously unknown wrong-result bugs in Spark and Flink. 9 of them need relations that existing SQL oracles do not state, SQLancer found none of the 17, and there were 37 false alarms. Replayed against 178 historical Spark "correctness" issues, it could express properties for 55 of the 65 testable ones. That is an expressiveness check, not reproduction ([Wu et al., arXiv 2606.11132](https://arxiv.org/pdf/2606.11132)) [D].
- **Yuan et al.'s error-handling checker** found bugs of which 143 were fixed or confirmed ([OSDI 2014](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-yuan.pdf)) [D].
- **Application-level pipeline tools** (BigTest, BigFuzz) report only seeded faults.
- **EvoMaster at Meituan** reported up to 210 "potential faults", with a fix rate of "around 10%" ([Zhang, Arcuri et al. 2022](https://arxiv.org/pdf/2208.03988)) [D].
- **Property-based testing** at Jane Street: 10 of 30 participants said it found bugs other methods had not (self-report) [D].

All of this is tool-author evidence. Developer confirmations are the main external check. No independent replication of BigTest, BigFuzz or Holey was found [D: gap].

The strongest unseen-defect evidence comes from oracles that do not need the right output for a realistic input: metamorphic and pivot relations, differential properties and error-handling checks. Fictional fixtures cannot carry real expected outputs out of the protected environment, but relations such as order-insensitivity, idempotent reprocessing and incremental-equals-full-recompute can be checked on both sides [I].

### What defects fixtures must expose

The one large production study of data-parallel jobs is Li et al.'s analysis of 200 SCOPE failures at Microsoft. It found that **84.5%** were caused by "defects in data processing rather than defects in code logic", that 62% were row-level failures "mainly caused by exceptional data", that 93% of fixes left processing logic unchanged, and that one job failed after 13.6 hours on unhandled nulls. The study excludes jobs that produced wrong results, because no oracles were available ([Li et al., ICSE SEIP 2013](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/icse13seip.pdf)) [D]. The 84.5% is therefore a crash-failure share. It is not a share of all defects [I].

Repository mining agrees on the location of problems. Incorrect data types are the top root cause (33%), data cleaning the most frequent stage (35%), and integration and ingestion account for 47% of developer questions ([Foidl et al., arXiv 2309.07067; JSS 2024](https://arxiv.org/pdf/2309.07067)) [D].

Distributed systems show sequence dependence. In Yuan et al.'s study, 74% of failures are deterministic given the right input sequence, most need no more than 3 input events, and 77% are reproducible by a unit test ([OSDI 2014](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-yuan.pdf)) [D].

No empirical defect study specific to entity resolution, reconciliation or incremental processing was found [D: gap].

### Equivalence to real inputs is ruled out by theory and depends on the behaviour model

No general equivalence guarantee is possible:

- Hamlet and Taylor show that partition testing pays off only when partitions are "narrowly based on expected failures", and that "if the right subdomains are the ones that find the unknown faults, those subdomains are equally unknown" ([TSE 1990](https://gwern.net/doc/cs/algorithm/1990-hamlet.pdf)) [D, theoretical].
- Proportional sampling is the only partition strategy proven, under its model's assumptions, never to be worse than random ([Chen, Tse & Yu 2001](https://i.cs.hku.hk/~tse/Papers/2000s/typssTR.pdf)) [D secondary, theoretical].
- Böhme and Paul bound when systematic testing beats random testing on efficiency. To show correctness on 90% of inputs against a 10 ms random test, a systematic technique must take under 41 ms per input ([FSE 2014](https://www.st.cs.uni-saarland.de/~boehme/paper/FSE14.pdf)) [D, theoretical].

Empirically, measured equivalence depends entirely on the behaviour model. Wang et al.'s field-versus-test gap was 6–8% under coverage models but **52.6%** under invariants ([ICST 2017](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf)) [D].

Running fictional and real data through the same instrumented code inside can establish exact set differences: branches, JDU paths, rules fired, invariants and mutants killed [I, shown feasible by Wang 2017 and BigTest]. It cannot establish three things [I, grounded in Hamlet & Taylor, Just 2014 and Li 2013]:

- equivalence with respect to faults not yet known;
- detection of the roughly 17% of real faults that are not coupled to any mutant;
- detection of silent wrong results where no oracle exists.

It also cannot show that equivalence persists after schema or source changes. No study was found that compares fixtures with real data through the same pipeline code on rule-firing or mutation-kill equivalence [D: gap].

## 6. Reduction works inside the boundary, but its output is still real data

### The interestingness-oracle model and its tools

All mainstream reducers share one model. A black-box "interestingness" oracle is re-run on ever-smaller candidates until the failure stops reproducing.

- **ddmin** gives **1-minimality**, meaning that removing any single change makes the failure disappear, with a quadratic worst case. It reduced 95 Mozilla user actions to 3 and 896 lines of HTML to 1, in 139 runs ([Zeller & Hildebrandt, TSE 2002](https://www.st.cs.uni-saarland.de/papers/tse2002/tse2002.pdf)) [D, theoretical bound and empirical].
- **Structure-aware reducers** produce smaller and more often valid outputs. HDD needs "orders of magnitude fewer test cases" ([ICSE 2006](https://web.cs.ucdavis.edu/~su/publications/icse06-hdd.pdf)) [D]. C-Reduce's outputs are more than 25 times smaller than its comparators', and its authors conclude that "effective program reduction requires more than straightforward delta debugging" ([PLDI 2012](https://users.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf)) [D]. Perses produces outputs 45% the size of HDD's ([ICSE 2018](https://web.cs.ucdavis.edu/~su/publications/perses.pdf)) [A].
- **Hypothesis** reduces the generator's choice sequence. Every shrunk case is therefore one the generator could have produced, which "significantly mitigates … the test-case validity problem". Its outputs are not as small as C-Reduce's ([MacIver & Donaldson, ECOOP 2020](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf)) [D]. This cannot shrink a real production extract, which has no choice sequence [I].
- **SQL reducers** remain experimental. SQLancer's ddmin and AST reducers are off by default, and reproducers exist only for two oracles ([SQLancer docs](https://raw.githubusercontent.com/sqlancer/sqlancer/main/docs/testCaseReduction.md)) [D]. SQLess reports a 72.45% simplification rate on the PINOLO dataset ([ISSTA 2024](https://matafeiyanll.github.io/paper/Issta24.pdf)) [A].

**No maintained OSS tool reduces multi-table relational data while respecting keys** [D: absence]. Flat ddmin wastes runs on candidates that keep a child row after its parent is removed. Schema-graph-guided reduction in the style of HDD is the closest analogue, but it is undocumented as a tool [I].

### Provenance-first reduction for pipelines

Two research methods use provenance to reduce pipeline inputs:

- **BigSift** combines Spark lineage with delta debugging. In one case it cut more than a billion records to **15** in 208 s, where plain DD took 12,395 s ([Gulzar et al., SoCC 2017](https://people.cs.vt.edu/~gulzar/assets/pdf/socc17-final244-acmpaginated.pdf)) [D]. It has been dormant since 2021.
- **Miao, Roy and Yang** find the smallest sub-database D′ ⊆ D on which two queries disagree. The problem is NP-hard in general, and they solve it with provenance plus a solver ([SIGMOD 2019](https://arxiv.org/pdf/1904.04467)) [D].

That second framing fits reconciliation and entity-resolution defects, with the previous pipeline version or a reference computation as the second query [I]. Both methods assume a static input. For incremental processing the reduction unit must include batch and delivery boundaries [I].

### Event and delivery sequences

DEMi minimised buggy Raft and Spark executions to **1×–4.6×** the optimal size. For example, raft-45 went from 2,160 events to 23 against an optimum of 22. That required about 14,000 lines of interposition code to control message and timer delivery ([Scott et al., NSDI 2016](https://www.usenix.org/system/files/conference/nsdi16/nsdi16-paper-scott.pdf)) [D]. A pipeline whose delivery order and delays come from logged timestamps can usually be replayed deterministically, so plain ddmin over the delivery list covers most of DEMi's stages. Reordering reducers could create sequences that cannot happen in production [I].

### Preserving defect-detection power

Reducing to "still fails" carries two documented risks:

- **Slippage**, where the reduced input triggers a different bug. It hit "23% of reduced JavaScript test cases" and is "difficult to avoid for silent bugs such as those that cause a compiler to emit incorrect code" ([Chen et al., PLDI 2013](https://users.cs.utah.edu/~regehr/papers/pldi13.pdf)) [D].
- **Lost general power.** Delta-debugged suites "often have little power for detecting new faults" ([Groce et al., ICST 2014](https://collections.lib.utah.edu/dl_files/8e/ea/8eea2537954679d0e007f1ad9620167d40d6772e.pdf)) [D].

Reducing with respect to coverage ("cause reduction") gave a SpiderMonkey suite almost 4× faster that detected more distinct faults months later. For YAFFS2 it kept more than 99% of mutant kills [D]. In test-suite reduction, reducing on statement coverage loses up to 20.5% of killed mutants, while reducing on killed mutants loses none, at an 11.9-percentage-point size cost ([Shi et al., FSE 2014](https://mir.cs.illinois.edu/awshi2/publications/FSE2014.pdf)) [D].

Data-platform defects are mostly silent wrong-output bugs, the class where slippage is hardest to avoid. The oracle should therefore check a specific signature, such as a particular output row, key or assertion, rather than "output differs". The reduction criterion should be compound: still fails, and still covers the same rules or kills the same mutants [I, from compiler and Java evidence, not pipelines].

### Reduce, then replace values

Every reducer runs offline against a local oracle, so all of them could run inside the protected environment. The output is still real data [I]. The documented ways to turn it into a releasable fixture are failure-preserving substitution: path-condition regeneration (Castro [L], Camouflage [D]) and syntactic retention (Masserini's special-character-driven suppression [D]). Miao et al. deliberately keep D′ ⊆ D to preserve real values for readability [D], which runs directly against anonymisation.

The notes infer an order of operations [I]: reduce inside first, then substitute values in the few remaining records, re-running the same oracle after each substitution. For entity resolution, substitution must preserve relations, not just values: identifier equality across sources, similarity bands, date order and delay offsets.

**No OSS implementation of "reduce, replace, re-check" for tabular data was found**, and no documented industrial practice of it either [D: absence].

## 7. Gap detection is mature for code change and immature for data change

### Gaps against code change

The industrial evidence that untested changes concentrate field defects comes from test gap analysis. In a Munich Re system, only **44% and 45%** of changed methods were tested in two releases, yet changed-untested methods held 43% and 40% of bugs and had the highest per-method bug probability. The authors caution that "the number of bugs we found is too small to derive generalizable results" ([Eder et al., AST 2013](https://wwwbroy.in.tum.de/publ/papers/AST13Hauptmann.pdf)) [D].

The vendor whitepaper restates the result as "five times more error-prone". It names configuration-level changes as a blind spot, and says "green" only means executed ([Juergens & Pagano 2016](https://teamscale.com/hubfs/26978363/Publications/2016-did-we-test-the-right-thing-experiences-with-test-gap-analysis-in-practice.pdf?hsLang=en)) [D/V]. That blind spot matches matching thresholds, mapping tables and SQL kept in configuration [I]. Developers rated only 18.2% of 110 ticket-level test gaps critical ([Rott et al. 2018](https://arxiv.org/pdf/1804.07599)) [D], and automated risk ranking matched expert assessment ([Haas et al., TSE 2025](https://www.se.cs.uni-saarland.de/publications/docs/HSJ+25.pdf)) [A].

Diff coverage answers "was the change executed?" (diff-cover; Codecov patch status as a capability reference). Diff-based mutation answers "would the tests notice?" Only the second tests whether a fixture's *values* are rich enough [I].

Google's experience is the main documented unsuccessful-then-successful arc. Developers first rated **85%** of surfaced mutants unproductive. Suppressing "arid" nodes and limiting to one mutant per line raised the productive share to **89%**, at a median of 7 mutants per changelist against 820 for traditional generation ([Petrović et al., arXiv 2102.11378](https://arxiv.org/pdf/2102.11378)) [D].

Incremental mutation caches are explicitly blind to fixture changes. PIT's incremental mode is "experimental" and its assumption "currently unproven" ([PIT](https://pitest.org/quickstart/incremental_analysis/)) [D]. StrykerJS does not detect changes to files other than mutated and test files ([Stryker docs](https://stryker-mutator.io/docs/stryker-js/incremental/)) [D]. Replacing a fixture therefore needs a forced full run [I].

Regression test selection is the inverse tool: it reduces what runs and does not find gaps. Manual selection by developers was unsafe 74% of the time ([Gligoric PhD thesis](https://users.ece.utexas.edu/~gligoric/papers/Gligoric15PhD.pdf)) [A]. dbt's `state:modified` selection "rel[ies] on your models being idempotent" ([dbt docs](https://docs.getdbt.com/reference/node-selection/state-selection)) [D].

### Gaps against data change

Field-versus-test gaps are measured for general software:

- Wang et al.'s gaps, described in sections 3 and 5 [D].
- Gazzola et al. found that 70% of field faults are "intrinsically hard to detect at design-time". Their "Unknown Application Condition" category, for example a folder name ending in a blank, is the software-testing name for new value categories that appear only in production ([arXiv 1708.09494](https://arxiv.org/pdf/1708.09494)) [D].

The clearest industrial practice of feeding aggregated production execution back into gap prioritisation is Google's Productive Coverage. Each AST node is scored by log2(1 + CPU-seconds), with a 0.01 CPU-second floor. A three-month randomised experiment over about 58,000 changelists reported meaningful test-quality improvement and fewer defects introduced ([Ivanković et al., ICSE-SEIP 2024](https://homes.cs.washington.edu/~rjust/publ/productive_coverage_icse_2024.pdf)) [D]. A 2021 defensive publication describes diffing production input usage against integration-test inputs "in a privacy-compliant manner" for schemas that change over time ([TDCommons #4113](https://www.tdcommons.org/dpubs_series/4113)) [L].

**No documented practice was found that exports rule-hit or branch-hit diffs from a protected data environment to flag fixture gaps** [D: absence]. Coverage files hold paths, line numbers and counts, not values, which makes them plausible "approved derived information". Small counts still leak [I].

Schema co-evolution studies show that schemas change frequently and force code changes, with 80% of changes falling in 20–30% of tables ([Qiu, Li & Su, FSE 2013](https://www.cs.ucdavis.edu/~su/publications/fse13-db-study.pdf)) [A]. No study measures how schema changes break test fixtures [D: gap].

The field-data augmentation line is the one research approach aimed at evolution. Di Nardo et al. modify field data to cover new requirements [L, full text U]. Tammisto et al.'s review found no approach that supports data evolution [D].

### Renewal and its oracle risk

Renewal tooling falls into three families:

- **Snapshot, golden and approval tools.** syrupy, pytest-regressions, inline-snapshot, ApprovalTests and insta regenerate expectations on a flag and rely on human diff review.
- **Test repair.** ReAssert repaired 29 of 37 failures [L]. TaRGET reached 66.1% exact match on 45,373 repairs [A].
- **Regenerated suites.** Randoop at ABB needed "just 4 edits to accommodate 2 years and 3 public versions of changes". It also disables assertions that fail at generation time, which weakens the oracle ([Robinson et al., ASE 2011](https://homes.cs.washington.edu/~mernst/pubs/maintainable-tests-ase2011.pdf)) [D].

All three share one risk: the update step rewrites the oracle to match current behaviour. Only Jest documents a hard guard. Snapshots "are not automatically written when Jest is run in a CI system without explicitly passing --updateSnapshot" ([Jest docs](https://jestjs.io/docs/snapshot-testing)) [D]. syrupy offers `--snapshot-update-new-only` and fails on unused snapshots by default ([syrupy README](https://raw.githubusercontent.com/syrupy-project/syrupy/main/README.md)) [D]. Snapshot suites killed 1.3× more mutants, but practitioners report "reviewing large result sets and managing false positives" as hurdles ([arXiv 2610.29549](https://arxiv.org/abs/2610.29549)) [A].

SQLMesh's `create_test` is the data-specific case. It copies input rows from the warehouse and computes expected output by running the current model, so it pins existing bugs. Generated inside the protected environment, its fixtures would contain real rows ([SQLMesh tests](https://sqlmesh.readthedocs.io/en/stable/concepts/tests/)) [D; consequences I].

When the input is refreshed real data, a regeneration diff mixes data change with logic change. One documented-pattern answer is to regenerate under old and new code against the same pinned input and review the diff [I].

### Reproducing historical failures

Fuzzing ecosystems hold the most complete practice. Go writes a failing input into `testdata/fuzz`, where it "will now be run by default with go test, serving as a regression test" ([go.dev](https://go.dev/doc/security/fuzz/)) [D]. ClusterFuzz and OSS-Fuzz deduplicate, minimise, bisect, and recheck fixed testcases automatically, and keep access-controlled daily corpus backups ([OSS-Fuzz corpora](https://raw.githubusercontent.com/google/oss-fuzz/master/docs/advanced-topics/corpora.md)) [D].

For a protected environment, the blocking issue is that the reproducer *is* the data. Real-data reproducers must stay in a protected corpus, or be minimised and transformed before leaving. No source documents that transformation step [I].

Determinism needs more than a seed:

- Order dependency causes 59% of Python flaky tests, and 95% confidence that a passing test is not flaky needs 170 reruns ([Gruber et al., ICST 2021](https://arxiv.org/pdf/2101.09077)) [A].
- "Unsynchronized seeds" across several random-number generators made tests flaky ([Parry et al., TOSEM 2022](https://o-parry.github.io/papers/2021a.pdf)) [A].

The earlier report adds the reproducibility layering for generated data. Hypothesis's example database "is best thought of as a cache" that may be dropped on upgrade, `@reproduce_failure` breaks across versions, and `@example` always runs ([Hypothesis API reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html)) [D]. The durable form of a historical failure is therefore an explicit minimal fixture. Seed, generator version and configuration, recorded together, regenerate larger datasets only while the old generator still runs ([earlier report](Synthetic%20stand%20in%20test%20data.md)) [I].

One evolution risk is specific to production-derived fixtures. Re-applying kb-anonymity across program versions creates a cross-referencing privacy risk, which is why kbe-anonymity exists ([Lucia et al., ASE 2012](https://doi.org/10.1145/2351676.2351718)) [L].

## 8. Every artefact leaks something, pass/fail oracles leak adaptively, and licences bind independently

### Measured leakage exists only for failure inputs and crash reports

Castro et al.'s bound is documented through their patent. "If a fraction [α] of the byte strings having the same size as the original input satisfy the conditions, the error report reveals −log2([α]) bits", and the user may then choose whether to send it ([US 8,122,436 B2, published 2012-02-21](https://patents.google.com/patent/US8122436B2/en)) [D, theoretical metric]. The bound assumes a uniform prior. It does not bound an adversary with auxiliary knowledge [I].

Camouflage measured residual leakage after deliberate path-preserving anonymisation:

- On average **30.6% of input bits** were revealed (range 2.3–76.5%), and **30% of the input** stayed unchanged (range 1.5–65%).
- The authors conclude "it is generally impossible to generate fully anonymized inputs".
- Compared with a re-implementation of Castro's method over 20 faults, Camouflage revealed 30% fewer bits and 40% less residue, "with the caveat of a potential implementation bias".
- Sensitivity was judged only by the author's inspection.

Sources: [Clause thesis, May 2011](https://repository.gatech.edu/server/api/core/bitstreams/c1cdccd9-cb7c-42c9-abf1-3e390dd74618/content); [CERCS TR 2009](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf) [D, empirical]. The technical report's introduction gives a "≈60% … to ≈2%" range that conflicts with its own §4.4. This report uses §4.4.

ReMoTe confirms the mechanism. Fields compared against constants, such as status codes, had no alternative values, so they leak exactly [D].

Crash artefacts leak in practice:

- **Browser crash reports.** Mining 2.5 million "partially anonymized" reports found more than 20,000 session and token IDs, 600 passwords and about 9,000 email addresses, mostly in URL and free-text fields ([Satvat & Saxena, arXiv 1808.01718](https://arxiv.org/abs/1808.01718)) [D].
- **Scrash** removes annotated sensitive data from core files. It explicitly does not handle control-flow leakage, because "the program counter and call stack can leak information on the state of sensitive variables" ([USENIX Security 2003](https://www.usenix.org/legacy/events/sec03/tech/full_papers/broadwell/broadwell.pdf)) [D].
- **Microsoft WER** "does not have sufficient metadata to locate and filter possible PII". It relies on minimising heap collection and on access policy ([Glerum et al., SOSP 2009](https://www.sigops.org/s/conferences/sosp/2009/papers/glerum-sosp09.pdf)) [D, documented practice].

PostgreSQL `EXPLAIN ANALYZE` prints actual row counts, "Rows Removed by Filter" and the filter predicates ([PostgreSQL docs](https://www.postgresql.org/docs/current/using-explain.html)) [D]. An exported plan is therefore a bundle of exact counting-query answers plus literals [I]. The earlier report covers the same hazard for optimiser statistics: PostgreSQL warns that `pg_statistic` "should not be readable by the public" ([PostgreSQL pg_statistic](https://www.postgresql.org/docs/current/catalog-pg-statistic.html)) [D].

**Coverage vectors, mutation-kill matrices, assertion messages and rule-hit counts have no dedicated disclosure measurement** [D: gap]. The notes bound them by inference [I]:

- Any artefact that is a deterministic function of the execution on a record reveals no more than the full trace.
- One bit can still be decisive for a predicate such as `diagnosis == X`.
- Each entry in a mutation-kill matrix is a threshold query. A boundary mutant from `x < c` to `x <= c` reveals whether a real value equals c.
- Assertion messages that print "expected … but was …" release real values verbatim (general knowledge, not verified in the notes).
- A minimised failing fixture proves that a record with the triggering property exists, keeps all triggering values, and can be linked through another source describing the same entity.

### Repeated and interactive releases make the developer an adaptive query analyst

When tests run inside and only pass/fail or counts come out, each run is a query and each pass/fail is one bit. A test asserting `record[i].salary < c` admits binary search in about log2(range) runs [I].

The statistical-database literature is clear on the risks:

- Refusals leak, which is the premise of simulatable auditing ([Kenthapadi, Mishra & Nissim, PODS 2005](https://seclab.cs.georgetown.edu/bibliography/DBLP_conf/pods/KenthapadiMN05.html)) [L]; the earlier notes record the same point from Dwork and Roth [D].
- Trackers defeat query-set-size restriction (Denning 1979) [U; content I from general knowledge].

The documented analogues come from verification servers and ML leaderboards:

- **Verification servers.** Barrientos et al. state that "verification measures leak information about the confidential data" and make them ε-differentially private. They acknowledge that budget exhaustion and fair allocation "have yet to be addressed in production settings" ([NBER WP 23534, June 2017](https://www.nber.org/papers/w23534.pdf)) [D]. Lin and Reiter give a differentially private verification measure ([arXiv 2404.02519, April 2024](https://arxiv.org/abs/2404.02519)) [D].
- **Leaderboards.** Blum and Hardt show that Kaggle's heuristics (rate limits and rounded scores) degrade as √k in the number of submissions, while their Ladder mechanism degrades as O((log k / n)^{1/3}) ([arXiv 1502.04585, ICML 2015](https://arxiv.org/abs/1502.04585)) [D, theoretical]. Thresholdout allows "the validation of a large number of adaptively chosen hypotheses, while provably avoiding overfitting" ([Dwork et al., arXiv 1506.02629](https://arxiv.org/abs/1506.02629)) [D].
- **Interactive DP SQL.** PrivateSQL fixes total privacy loss across an analyst's queries, with an entity-level privacy unit across foreign keys ([Kotsogiannis et al., PVLDB 2019](https://www.vldb.org/pvldb/vol12/p1371-kotsogiannis.pdf)) [D].
- **Agency guidance.** NIST SP 800-188 says interactive query interfaces need noise or staff review and should "log both queries and query results", and that "the query interface alone will not protect privacy" ([NIST SP 800-188, Sept 2023](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf)) [D].

Under DP, losses compose and cannot be recovered. Exact non-DP releases from the same data void the accounting ([earlier report](Synthetic%20stand%20in%20test%20data.md); [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)) [D]. Aggregates are not inherently safe: the Census Bureau reconstructed all records in 70% of 2010 census blocks from published tables ([Abowd et al., arXiv 2312.11283](https://arxiv.org/abs/2312.11283)) [D, via the earlier report].

No paper on differentially private software testing, or DP on test pass/fail outcomes, was found [D: gap].

### Established bounding methods, ranked by the guarantee they give

Disclosure-bounding methods fall into four classes by strength of guarantee [I, synthesised from D sources]:

- **Formal (differential privacy).** Available for counts and verification measures. Not available for an individual failing fixture: one real record cannot be released under DP; only a DP-generated stand-in can.
- **Information-theoretic but non-adversarial.** Castro's bits bound.
- **Syntactic.** k-anonymity and kb-anonymity, with no composition across releases.
- **Procedural.** The Five Safes and output checking.

NIST SP 800-188 sets the standards baseline. It defines "test data" that may "include extreme values that are not in the original data". It says realistic test data is safe only if "not developed using confidential data or a model based on the confidential data". It also warns that masking tools give "minimal privacy protection" and should not be "the sole mechanism to ensure confidentiality in non-public data sharing" ([NIST SP 800-188](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf)) [D]. ISO/IEC 20889 and 27559 were unreachable [U].

The documented operational model that matches "run inside, approved derivatives out" is OpenSAFELY:

- Code is developed and "tested and perfected/improved on a dummy dataset" outside, then run inside.
- Outputs and logs stay in the secure environment, behind Airlock.
- Every release undergoes "dual independent checking by trained output-checkers".
- Counts of 7 or fewer are redacted and the rest rounded to 5.
- For repeated reports, it advises rounding across the whole report and waiting for "enough change in the underlying study population" before re-releasing.
- Error logs are released only "in exceptional circumstances", after minimisation.

Sources: [OpenSAFELY docs](https://raw.githubusercontent.com/opensafely/documentation/main/docs/how-opensafely-works.md); [SDC rules](https://raw.githubusercontent.com/opensafely/documentation/main/docs/outputs/sdc.md); [file release](https://raw.githubusercontent.com/opensafely/documentation/main/docs/outputs/requesting-file-release.md) [D, documented practice].

Mapped onto a test regime, the documented analogues suggest four controls [I]:

- Run only reviewed, versioned suites, with no ad hoc assertions.
- Release pass/fail per suite, with rounded counts and messages held back.
- Check outputs by hand and log what was released.
- Use DP or Ladder-style release where volume is high.

Automated gates must decide from the query alone, never from the outcome, or the refusal leaks [I]. Late-arriving source batches act as natural differencing between successive runs [I].

### Licensed reference data is a separate test from privacy

Licence and database-right constraints govern extraction and re-utilisation of content. Privacy constraints govern identifiability. The two are independent [I, from D sources].

EU Database Directive Art. 7 protects against extraction of "a substantial part" of a database. Art. 7(5) forbids "repeated and systematic extraction … of insubstantial parts" that conflicts with normal exploitation ([Directive 96/9/EC Art. 7](https://www.legislation.gov.uk/eudr/1996/9/article/7/adopted)) [D]. Commentary on BHB v William Hill frames the test as whether the "cumulative effect" reconstitutes a substantial part ([5RB summary](https://www.5rb.com/?p=5151)) [L]. A CI job that exports a few *different* licensed records per run, every day, is the risky pattern. A fixed, small, versioned fixture set is the safer one [I].

Licence terms vary widely:

- **Royal Mail PAF (2019 licence).** It allows copies "reasonably necessary for … system testing purposes", requires a data supply agreement, caps trial responses at 100 address records, and forbids "Data Extraction" into new databases ([PAF licence 2019](https://www.poweredbypaf.com/wp-content/uploads/2019/06/paf-data-solutions-provider-licence-2019-1.pdf)) [D]. Whether this is the current version is unverified.
- **ICD-11.** CC BY-ND 3.0 IGO. Incorporation into software is permitted only if code, title and URI travel together, and crosswalks need a separate WHO agreement ([WHO ICD-11 licence](https://icd.who.int/en/docs/icd11-license.pdf)) [D].
- **GLEIF LEI data.** CC0 ([GLEIF terms](https://www.gleif.org/en/meta/lei-data-terms-of-use)) [D].
- **FIGI identifiers.** Dedicated to the public domain ([OpenFIGI ToS, 27 Nov 2018](https://www.openfigi.com/docs/terms-of-service)) [D/V].
- **ISO 4217 lists.** Published "free of charge", with no reuse licence found ([SIX](https://www.six-group.com/en/products-services/financial-information/data-standards.html)) [D].
- **ODbL, SNOMED CT and exchange market-data policies.** Covered in the earlier report: SNOMED treats sub-sets and cross-maps as derivatives ([SNOMED CT Affiliate Licence](https://isd.hscic.gov.uk/trud/users/guest/filters/0/licence/4)) [D].

The practical consequence is that every artefact leaving the environment faces two independent tests. A fixture with real PAF addresses and synthetic people may pass the privacy test and fail the licence test. A fixture with a real person's attributes and CC0 LEIs passes the licence test and may fail the privacy test. DP noise does not cure a licence breach, and rule-hit counts keyed by licensed code values disclose the code list itself [I].

No licence clause or court decision on exporting *test fixtures*, as distinct from test copies, was found [D: gap]. LOINC, ISO 3166, LSEG, S&P, D&B and Deutsche Post terms were not obtained [U].

## 9. Real-data checks inside and specification methods outside substitute for realism in specific defect classes

### Checks on real data inside the boundary

The alternatives with the most documented use run checks on real data inside the boundary and export only aggregates:

- **Uber's Hive-to-Spark migration.** About 18,000 workflows were shadow-run and validated through row counts, then row-level checksums, then consistent hash-keyed sampling. It surfaced engine-semantics defects, such as `regexp_like` returning null versus false and VARCHAR truncation. Floating-point aggregates, JSON ordering and non-deterministic functions needed workarounds that "weren't foolproof" ([Uber, 2025-06-12](https://www.uber.com/us/en/blog/how-uber-migrated-from-hive-to-spark-sql-for-etl-workloads/)) [B].
- **Meta's ingestion migration.** It compared row count and checksum per partition between shadow and production, then reversed the shadow for rollback ([Meta, 2026-05-12](https://engineering.fb.com/2026/05/12/data-infrastructure/migrating-data-ingestion-systems-at-meta-scale/)) [B].
- **Uber's data-quality platform.** It runs about 18,000 tests per day across more than 2,000 datasets and reports catching "around 90% of data quality incidents". No precision or recall is given and the denominator is undefined ([Uber, 2021-08-05](https://www.uber.com/blog/operational-excellence-data-quality/)) [B].
- **Write-audit-publish.** Documented in Apache Iceberg: writes go to an audit branch that is validated, then fast-forwarded ([Iceberg branching](https://raw.githubusercontent.com/apache/iceberg/main/docs/docs/branching.md)) [D]. Netflix's originating use is a lead [L].
- **Deequ.** Compiles declarative constraints to Spark aggregations and computes metrics incrementally, but does not measure how many code defects its checks catch ([Schelter et al., PVLDB 2018](https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf)) [D].

Two documented practices conflict with a strict export rule: Uber's sampled rows and Meta's logged "example mismatched rows". In a protected setting these would have to stay inside or be replaced by key hashes [I].

Shadow and diff runs detect *change* relative to a baseline. A bug shared by both versions passes [I].

Conservation invariants are cheap to check inside and export as counts. Examples are that every source record maps to exactly one entity or an explicit unmatched bucket, and that per-source contributions sum to target totals. They catch loss, duplication and double counting, and miss count-preserving mis-merges [I]. ABC and reconciliation frameworks have only practitioner and vendor support ([Varigence](https://www.varigence.com/blog/row-counts-lie-column-control-totals)) [V].

### Specification and static methods outside

Specification and static methods need no data at all:

- **TLA+ at AWS** found 3 bugs in DynamoDB replication (some needing 35-step traces), 2 in S3 and 3 in EBS. One "had passed unnoticed through extensive design reviews, code reviews, and testing". Engineers got useful results within 2–3 weeks of learning ([Newcombe et al., 2014](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf)) [D].
- **MongoDB** shows both outcomes. Model-based trace-checking of the server's replication protocol was **abandoned after 10 weeks** by two engineers, because "no initial infrastructure investment can make the marginal cost of trace-checking additional specifications cheap". Model-based test generation for Realm Sync's merge rules took 4 weeks. It produced 4,913 tests with **100% branch coverage, against 21% for 36 handwritten tests and 92% for AFL**, and found a non-termination bug in mature code ([Davis et al., PVLDB 2020](https://arxiv.org/pdf/2006.00915)) [D].
- **SQL equivalence checkers** are improving fast but cover limited fragments and are prototypes:
  - VeriEQL supports 77.1% of LeetCode queries and disproves 14.9% of pairs, where "testing tools can disprove <1%" ([OOPSLA 2024](https://arxiv.org/pdf/2403.03193)) [D].
  - QED verifies 299 of 444 Calcite rewrite pairs ([PVLDB 2024](https://vldb.org/pvldb/vol17/p3602-wang.pdf)) [D].
  - SQLSolver proves 346 of 359 pairs ([PACMMOD Dec 2023](https://par.nsf.gov/servlets/purl/10548354)) [D].
  - Cosette is deprecated in favour of QED [D].
- **Typed dataframes and schema validation** (Pandera, which can also generate data through Hypothesis strategies) target the dominant root-cause class: data types, 33% in Foidl et al. ([Pandera docs](https://raw.githubusercontent.com/unionai-oss/pandera/main/docs/source/data_synthesis_strategies.md)) [D; the targeting is I].

### Property-based and differential testing

Property-based and differential testing need no realistic fixtures. Differential properties were "by far the most widely implemented kind of property" at Jane Street (17/30). The documented cost is generators that satisfy preconditions: 17 of 30 participants needed them, and the work was called "tedious" or "high-effort". 5 of 30 still wanted "realistic" data ([Goldstein et al., ICSE 2024](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice.pdf)) [D].

Plausible properties for entity resolution and incremental processing are inferred, not evaluated:

- idempotent re-runs;
- incremental result equal to a full recompute;
- invariance to input order;
- monotonic linking;
- round-trip identifier mapping.

The incremental-equals-full relation can also run inside on real data and export a single boolean [I].

### Assertions

Assertion evidence is modest. Methods with asserts had "significantly fewer defects", with a "small (but significant)" effect, in 100 C/C++ projects ([Casalnuovo et al., ICSE 2015](https://www.cs.ucdavis.edu/~filkov/papers/assert-main.pdf)) [A]. An industrial replication found "only limited evidence" ([Counsell et al. 2017](https://arxiv.org/pdf/2104.01514)) [A].

### When the alternatives are preferable

No source compares any of these with fixture-based testing on the same defects [D: gap]. From the case reports, the notes infer when each is preferable [I]:

- **Real-data checks inside** when the defect class depends on real-data variety: nulls, encodings, engine semantics, coverage gaps between sources.
- **Formal models** when it depends on rare interleavings or late-data ordering.
- **Differential or equivalence checking** when a trusted previous version exists and the change is a refactor.
- **Fixtures** for fast local feedback on anticipated cases.

AWS explicitly treats formal methods as complementary to testing [D]. No approach is documented replacing fixtures outright.

Several approaches have documented failures or retreats:

- MongoDB's trace-checking [D].
- datafold/data-diff, discontinued on 17 May 2024 ([README](https://raw.githubusercontent.com/datafold/data-diff/master/README.md)) [D].
- Airbnb's heavyweight Midas certification, reportedly lightened because of its cost ([Airbnb DQS post](https://medium.com/airbnb-engineering/data-quality-score-the-next-chapter-of-data-quality-at-airbnb-851dccda19c3)) [L/U].
- Soda Core v4's move to the Elastic License 2.0 ([LICENSE](https://raw.githubusercontent.com/sodadata/soda-core/main/LICENSE)) [D].

## Prior-art catalogue

### Directly comparable solutions: real data or its properties used inside a boundary to produce derived test artefacts aimed at exercising logic or detecting defects

| Approach | Original problem | Method | Applications | Empirical results | Limitations | Relevance to the constraints | Status |
|---|---|---|---|---|---|---|---|
| Grechanik et al., ISSRE 2010 | Outsourced testing of database-centric applications without sharing data | Program-analysis-guided selective k-anonymity | 4 small Java DCAs (0.8–4.3K NCLOC) | Coverage >70% falls to <30% at k ≥ 7 with standard k-anonymity; guided approach better for k ≤ 6 | Coverage only; small subjects; real values still leave | Quantifies the cost of value-blind anonymisation | EXP [D] |
| PRIEST, FSE 2011 | Same | Attribute-to-branch analysis plus guessing-anonymity data swapping | DurboDax, UnixUsage, RiskIt, N2A | DurboDax coverage 72%→57% as privacy rises; estimator error 2.0–8.3% | Swapped real values leave | Attribute-to-branch mapping is the information a fixture builder needs | EXP [D] |
| kb-anonymity, PLDI 2011; kbe-anonymity, ASE 2012 | Release of client data to third-party developers | Symbolic execution plus k-anonymity to generate tuples with the same behaviour; kbe handles program versions | 3 Java programs (kbe) | Path behaviour preserved (abstract) | "Limited to numbers and programs whose code is accessible and analyzable with symbolic execution" | Only work naming the repeated-release risk across versions | EXP [L]; limitation [D] via Masserini |
| PISTIS, ICST 2014 | Sanitising and minimising databases for outsourced tests | Weighted clustering; release centroids | DurboDax, RiskIt | Coverage "within a close range"; random deletion worsens coverage | Centroids derive from real records; low baseline coverage | Combines minimisation and sanitisation | EXP [D] |
| Castro et al., ASPLOS 2008 | Bug reports without private data | Path-condition solving for a new input | Binaries | "Almost no private information" (abstract) | Not public; full text unreachable | Origin of the −log2(α) bits metric | EXP [L]; metric [D] via patent |
| Camouflage, TR 2009 / ICSE 2011 | Anonymising failure-inducing field data | Path-condition solving with relaxation | 170 inputs, 4 Java subjects | 100% of failures reproduced; 30.6% bits and 30% residue on average | Known failures only; determinism and solver completeness assumed; manual sensitivity judgement | Strongest record-free reproduction result | EXP [D] |
| ReMoTe (Andrica & Candea) | k-anonymous Android traces | Concolic alternatives for server responses | PocketCampus | >100 alternatives for some fields, none for constant-compared or floating-point fields | Mobile traces | Shows which fields leak exactly | EXP [D] |
| Masserini et al., AST 2024 | Cost of anonymising failure data | 5 SDC techniques on traces | 19 failures, 17 Android apps | 11–63% reproduction by technique | Android, single-record failures | Measured privacy–reproducibility curve | EXP [D] |
| Tuya et al., TSE 2016 | Smaller test databases with the same SQL coverage | Coverage-aware reduction | 2 real applications plus a benchmark | Large reduction (abstract) | Full text not read | Reduction of a production database inside | EXP [L] |
| BigTest, ESEC/FSE 2019 | Testing DISC applications with UDFs | Symbolic execution of UDFs plus logical operator models | Spark benchmark, seeded faults | Production leaves 34% of JDU paths untested; tens of records match its coverage; 2x seeded faults vs Sedge; 194x CPU saving | Seeded faults; dormant prototype; single-key joins | Shows real data is not an adequacy oracle | EXP [D] |
| DBGriller, ICSE 2023 | Test databases for database-backed applications | Mutate developer test databases toward DB-dependent branches | 30 applications | Developer databases cover 55% of DB-dependent branches; 22 real bugs, 12 confirmed, 3 fixed | Crash oracle; 4 false positives | Direct evidence that hand fixtures are thin | EXP [D] |
| Di Nardo et al., ICST 2015 / TOSEM 2017 | Testing data-processing systems with field data | Model-based mutation or augmentation of field data | Satellite data acquisition | More coverage than engineer-written tests (abstract) | Full texts unreachable | Field-data evolution for new requirements | EXP [L] |
| Homayouni 2018 | ETL correctness in a warehouse | Balancing tests generated from source-to-target mappings | Health Data Compass warehouse | "Previously undetected real faults" found; mutation analysis on mock source data | One thesis; numbers not extracted | Closest to multi-source reconciliation | EXP [D, abstract and summary] |
| Lam et al., IJPDS 2024 | Evaluating linkage methods without real identifiers | Synthetic identifiers that replicate error dependencies | ALSPAC | Linkage metrics within 0.13–0.55% (missed) and 0.00–0.04% (false); real disagreement 18% of surnames, 12% of forenames | Linkage-quality target, not defect detection | Best documented model of real identifier messiness | EXP [A] |
| Replica / VASE, 2019 | In-house tests not representative of the field | Field invariant violations plus guided symbolic execution | TSL, grep, sed, gzip | 56.0% of untested field invariants vs 4.7% for KLEE | Solver timeouts on nested conditions; privacy claimed, not measured | Behavioural signals beyond coverage | EXP [D] |
| Productive Coverage, Google, ICSE-SEIP 2024 | Actionability of coverage | Production CPU-sample frequency to rank uncovered code | Google monorepo, RCT | Meaningful test-quality gain; fewer defects introduced | Code frequency only, not data | Aggregate production signal steering test writing | EST at Google [D] |

Sources: as cited in sections 1–8; [Lam et al.](https://discovery.ucl.ac.uk/10194216/1/ijpds-09-2389.pdf); [Homayouni thesis](https://mountainscholar.org/bitstream/10217/189268/1/Homayouni_colostate_0053N_14638.pdf); [Tuya et al. 2016](https://doi.org/10.1109/tse.2016.2519032).

### Neighbouring techniques: applicability to the brief only inferred

| Technique | What it was built for | Why applicability is only inferred | Status |
|---|---|---|---|
| Rule- and constraint-based generation (PLEDGE; the nine closest approaches in Tammisto 2026) | Valid system test data from UML/OCL or rules; PLEDGE gives the "incomplete, incompatible, inaccessible" triad for real data ([Soltana et al., TOSEM 2020](https://arxiv.org/pdf/1902.00397)) | Targets constraint satisfaction, not multi-source discrepancy realism | EXP [D] |
| SQL and query test generation (EvoSQL, XData, QAGen, DataSynth) | Query predicate coverage, mutant killing, DBMS testing | Single query or single consistent state | EXP [D]/[L] |
| Search-based system test generation with SQL (EvoMaster) | REST/GraphQL/RPC services | Generic oracle; JVM only | EXP; tool active [D] |
| Coverage-guided dataflow fuzzing (BigFuzz) | Spark applications | Circular evaluation; dormant | EXP [D] |
| Statistical / operational-profile testing (Musa; Soltana ASE 2017) | Reliability estimation | Resemblance as an objective is out of scope | EST/EXP [D]/[L] |
| Production carving and monitoring (Pankti, RICK, PROZE, Elbaum carving) | Unit tests from production objects | Real values become fixtures | EXP [D]/[A] |
| Crash reproduction (BugRedux, ESD, STAR, EvoCrash, Botsing) | Reproducing field crashes | Crashes, not wrong results; C or Java only | EXP [D]/[A] |
| Data validation (Deequ, dbt tests, GX) | Checking data, not code | No defect-detection measurement | EST [D] |
| Record-linkage generators (GeCo, Febrl) | Linkage quality evaluation | Not designed for defect finding; GeCo full text unreachable | [L] |
| History checkers and model-based testing (Elle, Modelator, GraphWalker) | Database isolation; model conformance | No pipeline or late-data application found | EXP/EST [D] |
| Reducers (ddmin, HDD, Perses, C-Reduce, SQLess, BigSift, DEMi) | Compiler, DBMS and distributed bugs | No relational-key-aware reducer; output is real data | EXP/EST [D] |
| Production sampling in CI (GetYourGuide, Every Cure) | Pipeline tests that resemble production | Moves the defect signal, not the fixtures; no counts | EST in-house [B] |
| Official-statistics synthetic spectrum (ONS levels 1–2) | Code testing with "no analytical value" and "minimal disclosure risk" ([ONS WP16](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)) | Guidance, not defect evidence | documented guidance [D] |

## Open-source tools

Maintenance dates are as recorded by the tracks on 2026-11-26, from PyPI, Maven Central, npm or crates.io, or from the last commit in a shallow `git clone`. The GitHub API was blocked, so stars and archive flags were not checked. For every tool in these tables, real rows are needed only if the tool is run inside the protected environment against real data. What leaves is then the tool's report. That report is an artefact subject to the disclosure analysis in section 8 [I]. Computational cost is documented only where noted.

### Adequacy measurement

| Tool | Capability | Maintenance | Licence | Relational / stateful | Needs | What would leave if run inside |
|---|---|---|---|---|---|---|
| PIT (+ Descartes) | JVM mutation; extreme mutation for pseudo-tested methods | 1.30.2, 2026-11-05; Descartes 1.3.4, 2025-09-19 | Apache-2.0; LGPL | No data model | Bytecode | Mutant IDs and statuses; kill matrix is a threshold-query channel |
| Stryker4s / StrykerJS | Scala / JS mutation; JS incremental mode | 1.1.1, 2026-07-30; 10.1.1, 2026-10-23 | Apache-2.0 | No | Source | Same |
| mutmut / cosmic-ray / poodle | Python mutation | 3.8.1, 2026-10-28 / 8.9.0, 2026-11-10 / 1.4.0, 2026-10-31 | BSD-style / MIT / MIT | No; SQL strings inside code are not mutated | Source; coverage.py | Same |
| pytest-gremlins | Python mutation | 1.15.0, 2026-11-26 (first release 2026-01-27) | MIT | No | Source | Same |
| mutatest, MutPy | Python mutation | Stale (2022-02-20; 2019-11-17) | MIT; Apache-2.0 | — | — | — |
| TRANSMUT-Spark | 15 Spark RDD dataflow operators | MIT (©2020); unpublished, build locally | MIT | RDD only, Scala 2.12 | sbt 1.3+ | Same |
| SchemaAnalyst | Schema-constraint mutation and data generation | Last commit 2021-03-24 | GPL-3.0 | Schema constraints | DDL | Mutation score |
| SQLFpc / test4data | MC/DC coverage rules for SQL | Tool state unverified | — | Joins, NULLs, outer joins | SQL text, schema | Rule IDs and covered flags |
| dbt-coverage | Presence of docs and tests | 0.5.0, 2026-10-07 | MIT | — | dbt manifest | Not a logic-coverage measure |
| coverage.py contexts / diff-cover | Per-test line attribution; coverage of the diff | coverage.py 7.17.5 docs; diff-cover 11.0.4, 2026-11-19 | — / Apache-2.0 | — | Python / any coverage XML | Paths, lines, counts |

### Generation

| Tool | Capability | Maintenance | Licence | Relational / stateful | Needs | Cost / notes |
|---|---|---|---|---|---|---|
| EvoMaster | Search-based API tests with SQL/MongoDB state genes | Last commit 2026-11-26; tag v6.2.0 | LGPL-3.0 | Multi-table INSERTs with FK closure; operation sequences | JVM agent, hand-written driver | Generic oracle; one-off driver cost [I] |
| EvoSQL | Per-query data for SQLFpc targets | Last commit 2019-08-24 | Apache-2.0 | Single query | Query, schema | Performance falls as targets rise |
| BigTest | Symbolic Spark+UDF input generation | Last commit 2022-08-05 | No LICENSE file found | Join terminating cases | UDF source, JPF | 194x CPU saving vs full data |
| BigFuzz | Coverage-guided Spark fuzzing | Last commit 2021-09-16 | LICENSE present, type unchecked | Schema-aware | Program rewrite | 78–1,477x faster than random fuzzing |
| XData | Mutant-killing SQL datasets | No public repo found | Unknown | Per query | Query, schema | — |
| Hypothesis (+ hypothesis-jsonschema) | PBT with stateful Bundles | 6.170.17, 2026-11-20; 0.23.2, 2026-10-27 | MPL-2.0 | Keys shared through Bundles; no FK model | Strategies | — |
| FANDANGO / ISLa | Grammar plus quantified constraints | 1.3.2, 2026-11-25 / last commit 2024-07-01 | EUPL-1.2 / GPL-3.0 | One document per dataset | Grammar | Scaling untested |
| Schemathesis | OpenAPI/GraphQL PBT | 4.34.2, 2026-11-24 | MIT | API level | Schema | — |
| quickcheck-state-machine | Stateful and parallel PBT (Haskell) | Last commit 2026-05-18 | BSD-style | Sequences, races | Model | — |
| GraphWalker / fMBT / Modelator | Model-based testing; TLA+ traces | 2026-10-17 / 2026-01-14 / 2025-03-12 | MIT / LGPL-2.1 / Apache-2.0 | Sequences | Model | — |
| Jepsen + Elle | History-based isolation checking | Elle last commit 2026-10-16 | EPL-2.0 | Transaction histories | Workload, consistency model | — |
| Pankti / RICK | Tests from production objects | Last commit 2024-11-01 | MIT | Objects | JVM instrumentation | Broadleaf CPU 16.4%→41.8% |
| Botsing | EvoCrash crash reproduction | Last commit 2021-04-07 | Apache-2.0 | — | Stack trace, bytecode | Unmaintained |
| Pynguin / EvoSuite | Unit-test generation | 0.49.0.dev0, 2026-10-16 / Maven 1.0.6, 2018-04-05 | MIT / — | — | Source | — |
| Daikon | Invariant inference | Last commit 2026-11-25 | MIT-style | — | Traces | — |
| recordlinkage / splink / dedupe | ER implementations (capability references) | 0.16, 2023-07-20 / 5.0.0, 2026-09-28 / last commit 2025-07-28 | BSD-3 / MIT / MIT | — | — | Not generators |

### Reduction

| Tool | Capability | Maintenance | Licence | Relational / stateful |
|---|---|---|---|---|
| picire / picireny | Parallel ddmin; HDD over ANTLR grammars | 26.11, 2026-11-10 / 21.8, 2021-08-25 (commit 2025-11-23) | BSD-3 / BSD | Any serialisation; no key awareness |
| Perses / C-Reduce / C-Vise | Grammar-guided / pass-based reducers | Commits 2026-11-24 / 2024-06-01 / 2026-11-23 | GPL-3.0 / NCSA-style / follows C-Reduce | No |
| Shrink Ray / treereduce / Lithium / ddSMT | Multiformat and tree reducers | 26.9.13.0, 2026-09-13 / 2026-11-23 / 4.0.0, 2024-11-12 / 2.0.6, 2025-06-30 | MIT / MIT / MPL-2.0 / MIT | No |
| halfempty | Parallel minimiser | Dormant since 2020-12-24 | Apache-2.0 | No |
| SQLancer reducers | ddmin over statements; AST reducer, including INSERT-row removal | Last commit 2026-11-15; reducers experimental | MIT | Rows within INSERTs |
| BigSift | Provenance plus DD for Spark | Last commit 2021-09-29 | No LICENSE | Lineage |
| DEMi | Distributed-trace minimisation | Last commit 2016-03-12 | BSD-style | Message schedules |
| Hypothesis / proptest / Hedgehog / QuickCheck | Integrated or internal shrinking | Active (2026) | MPL-2.0 / Apache-2.0 / — / — | Generated sequences only |

### Evolution, renewal and in-environment alternatives

| Tool | Capability | Maintenance | Licence | Notes |
|---|---|---|---|---|
| syrupy / pytest-regressions / inline-snapshot / ApprovalTests / insta | Snapshot and golden renewal | 7.0.3, 2026-11-21 / 2.11.0, 2026-05-25 / 0.37.0, 2026-11-18 / 21.1.0, 2026-11-22 / 1.49.0, 2026-10-03 | MIT / MIT / MIT / Apache-2.0 / Apache-2.0 | Update flags rewrite the oracle; syrupy's new-only mode and unused-snapshot failure |
| vcrpy | Record and replay | 9.4.2, 2026-11-02 | MIT | No time-based re-record |
| Ekstazi / STARTS | Regression test selection | 2018-03-20 (dormant) / 1.4, 2023-01-21 | — | Inverse of gap finding |
| dbt-core / SQLMesh | Static-fixture unit tests; state selection; `create_test` copies warehouse rows | 1.12.7, 2026-11-12 / 0.236.4, 2026-10-22 | Apache-2.0 | `create_test` inside would contain real rows |
| Pandera | Dataframe schemas plus Hypothesis strategies | 0.36.0, 2026-11-10 | MIT | Outside, no data |
| Great Expectations / pydeequ / Soda Core | Data checks | 1.25.0, 2026-11-12 / 1.7.0, 2026-09-14 / 4.32.0, 2026-11-25 | Apache-2.0 / Apache-2.0 / ELv2 (v4) | Zero-row behaviour unverified |
| datacompy / reladiff / data-diff | Table diff | 1.2.0, 2026-10-27 / 0.6.0, 2025-03-04 / discontinued 2024-05-17 | Apache / MIT / MIT | Diff counts can leave; sampled rows cannot |
| sqlglot / SQLFluff | Parse, transpile, semantic diff / lint | 30.35.0, 2026-11-24 / 4.5.0, 2026-10-30 | MIT | No defect evidence for SQLFluff |
| QED, VeriEQL, SQLSolver | SQL equivalence | Repository maintenance unknown; Cosette deprecated | — | Counterexample databases from schema only |
| Iceberg WAP | Audit branch before publish | Current docs | Apache | Gate result only |

## Comparative assessment

| Approach family | Maturity | Evidence of real defect detection | Suitability for complex structured inputs | Disclosure implications | Maintenance burden |
|---|---|---|---|---|---|
| Hand-written fixtures (baseline) | Mature | Developer databases cover 55% of DB-dependent branches; 35% of methods pseudo-tested on average | Low; much simpler than real data | None | Grows with schema change; regression tests often skipped |
| Behaviour-preserving anonymisation (PRIEST, kb-anonymity, PISTIS) | EXP, no adoption found | Coverage preservation only | Relational DCAs, numbers mainly | Real or derived values leave; no composition | Needs program analysis per version; kbe shows re-release risk |
| Path-condition regeneration (Castro, Camouflage) | EXP | Reproduces known failures, 170/170 | File or record inputs; no SQL/Spark engine | ~30% of bits revealed; constants leak | Symbolic execution infrastructure |
| White-box DB / dataflow generation (DBGriller, BigTest, BigFuzz, XData) | EXP; prototypes mostly dormant | DBGriller 22 real bugs; others seeded | Relational and dataflow; no identity ambiguity | Can run outside on schema or code alone | High integration cost; pinned old stacks |
| Search-based system generation (EvoMaster) | EXP, maintained, one industrial study | 7 new faults on OSS APIs; ~10% fix rate at Meituan | Multi-table relational state | Can run outside | Driver per service |
| PBT / model-based / history checking | Mature tools; industrial practice | Elle: anomalies in all 4 DBs; MongoDB 100% branch and 1 bug; Jane Street self-report | Sequences and keys by hand | None outside | Generator writing "tedious"/"high-effort" |
| Production-informed generation (Replica, Pankti, Productive Coverage) | EXP; Productive Coverage EST at Google | Replica: invariant and mutant gains; Productive Coverage: fewer defects introduced | General code, not data | Frequencies low risk; objects high risk | Field instrumentation: Replica 13% average overhead; Pankti raised Broadleaf CPU from 16.4% to 41.8% |
| Reduction (ddmin family, BigSift, DEMi, SQL reducers) | Mature for programs; experimental for SQL/data | Slippage 23% (JS); cause reduction keeps detection | No key-aware relational reducer | Output is real data | Oracle runs × pipeline runtime |
| Adequacy measurement inside (coverage, SQLFpc, mutation on real data) | Tools mature; data-platform operators thin | Mutation coupled to 73% of real faults | Depends on operators | Counts and kill matrices are query channels | Equivalent mutants up to 24%; Google needed heavy filtering |
| Real-data checks inside (shadow, WAP, DQ, reconciliation) | EST in large organisations | Self-reported incident share; engine-semantics defects found | Full real variety | Aggregates fine; example rows not | Tolerance and canonicalisation workarounds; run-length latency |
| Formal and equivalence methods outside | TLA+ industrial; SQL equivalence prototypes | AWS 8 bugs across 3 systems; VeriEQL found bugs in MySQL and Calcite | Design and SQL fragments, not ER | None | Weeks per spec; trace-checking abandoned at scale |

Documented unsuccessful or retreated-from approaches:

- Coverage-driven augmentation failed to close field-behaviour gaps ([Wang 2017](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf)).
- SQL heuristics did not help where input validation blocked the code that touches SQL ([EvoMaster](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications/2020_tosem.pdf)).
- Value-level anonymisation of failure traces reproduced as little as 11–19% ([Masserini 2024](https://arxiv.org/pdf/2402.07460)).
- Statistics-preserving anonymisation was rejected for failure reproduction ([Camouflage](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf)).
- Complete branch traces were too much guidance for symbolic replay ([BugRedux](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2011/git-cercs-11-06.pdf)).
- Schema-matching fabricated data missed production nullability and drift ([Every Cure](https://docs.dev.everycure.org/infrastructure/architecture_decision_records/improve_testing_through_sampling/)).
- Raw diff mutation output was 85% unproductive until filtered ([Google](https://arxiv.org/pdf/2102.11378)).
- Trace-checking was abandoned at MongoDB ([Davis et al.](https://arxiv.org/pdf/2006.00915)).
- OSS data-diff was discontinued ([data-diff](https://raw.githubusercontent.com/datafold/data-diff/master/README.md)).
- Airbnb's heavyweight certification was lightened ([L]).

## Synthesis

**Has the problem been addressed?** Partially, and never under the brief's own framing. The closest terminology is ex-vivo and offline field testing for the setting, privacy-preserving testing and test-data anonymisation for the export constraint, test database generation and DISC testing for the generation side, and test amplification for production-driven improvement. The prior-art track infers that the brief's combination sits in an under-reviewed intersection: real data stays inside, only derived artefacts leave, and fixtures must track changing sources. Two reviews point that way. Bertolino et al. find ex-vivo testing under-explored, with privacy addressed in 10% of studies. Tammisto et al. find that methods usually need real data and that evolution is unaddressed [I from D].

**The closest existing solutions** are DBGriller, BigTest and its siblings, Camouflage and the PRIEST/PISTIS/kb-anonymity line, Homayouni's balancing tests, and OpenSAFELY's operating model. Respectively, they offer:

- test databases mutated toward uncovered database-dependent branches;
- minimal dataflow inputs matched to production path coverage;
- record-free inputs that follow a real failing path;
- anonymisation that preserves coverage or behaviour;
- source-to-target assertions that found real ETL faults;
- a documented regime of dummy data outside, execution inside and checked releases.

None was evaluated on entity resolution, conflicting multi-source identities or delivery sequences.

**What can be adopted directly** is the tooling and practice that does not depend on the missing evidence:

- mutation, extreme-mutation and coverage tools to separate thin inputs from weak assertions (PIT/Descartes, mutmut, cosmic-ray);
- non-emptiness checks against the documented zero-row vacuous pass;
- PBT and stateful generators for keys, duplicates and sequences (Hypothesis, quickcheck-state-machine);
- the fuzzing-corpus discipline for regression fixtures;
- snapshot tools with CI write-guards;
- shadow, differential and write-audit-publish runs inside that export counts;
- OpenSAFELY-style output checking, with redaction thresholds and rounding for repeated releases;
- independent licence review of any exported fixture.

**What requires adaptation:**

- Adequacy measures must run inside on real data and export only flags or counts: SQLFpc rules, t-way combination coverage, rule-firing sets, mutation kill sets. No source documents this for data platforms.
- Reducers must become key-aware, and must be followed by value substitution re-checked against the oracle.
- Path-condition approaches would need symbolic models of SQL and Spark semantics. BigTest has such a model only for its own operator set.
- Mutation operator sets must extend to DataFrame and dbt SQL.
- Shadow-run practices that log example rows must replace them with key hashes.

All of these adaptations are engineering inferences from the notes. None is documented.

**What genuinely remains unresolved splits into two kinds.** Some limits rest on *evidence or theory*:

- No criterion-based guarantee of equivalence to real inputs for unknown faults (Hamlet and Taylor).
- About 17% of real faults are uncoupled from mutants (Just et al.).
- Zero-leakage failure-preserving transformation is impossible in general (Camouflage).
- Interactive pass/fail oracles leak adaptively, and heuristic controls degrade as √k (Blum and Hardt).
- Finite DP budgets are exhausted, with allocation unresolved in production (Barrientos et al.).
- Trace-checking a large existing system did not pay off (MongoDB).

Others are *absences of evidence* in the searched literature, which do not show that a solution is impossible:

- adequacy criteria and defect studies for entity resolution, reconciliation and incremental processing;
- any generator that handles ambiguous identities and conflicts;
- generation of late, corrected, duplicated or out-of-order deliveries for pipelines;
- use of rule-hit or entity-resolution statistics to steer fixtures;
- a relational-aware reduce-then-anonymise tool;
- disclosure measurements for coverage vectors, kill matrices and rule-hit counts;
- DP applied to test outcomes;
- studies of how schema change breaks fixtures;
- a real-fault benchmark for ETL or entity-resolution code;
- any independent replication of the data-pipeline generators.

## Conclusion

The field's most useful lesson cuts against the brief's premise that fixtures are weak only because they are simpler than real data. Both directions of inadequacy are documented. Hand-written fixtures miss behaviour that real data triggers: database-dependent branches, nullability, field invariants. Real data in turn leaves a third of dataflow paths unexercised and cannot supply oracles for silent wrong results. Resemblance to real data is therefore the wrong target in both directions. What the evidence supports is comparing the two through the same instrumented code, using a behaviour model richer than line coverage, and scoring the result against faults that were not used to build the fixtures. The defects that matter most for entity resolution and reconciliation are silent mis-merges and count-preserving mismatches. They are exactly where slippage, uncoupled mutants and missing oracles concentrate, which is why relation-based oracles and conservation checks recur across otherwise unrelated literatures.

The second lesson is that the protected environment changes what "test result" means. Once tests run inside, every coverage flag, kill bit, plan count, assertion message and minimised fixture is a release. Repeated CI runs make the outside developer an adaptive analyst and the CI pipeline a repeated extractor of licensed content. The test pipeline therefore needs governance of the kind statistical agencies and trusted research environments already practise: reviewed code, aggregated and rounded outputs, logged releases, and separate licence clearance. The test engineering literature has largely not yet supplied that governance.

## Sources and dates

Grouped by evidence type. Dates are publication dates unless marked as retrieval or last-update dates. Labels as defined at the top.

| Date | Source | Type | Label |
|---|---|---|---|
| 1989 | [Musa & Ackerman, "Quantifying Software Validation", IEEE Software](https://www.rose-hulman.edu/class/csse/csse376/Resources/musa.pdf) | theoretical/practice | D |
| Dec 1990 | [Hamlet & Taylor, "Partition Testing Does Not Inspire Confidence", TSE](https://gwern.net/doc/cs/algorithm/1990-hamlet.pdf) | theoretical | D |
| 2001 | [Chen, Tse & Yu, proportional sampling compendium (TR)](https://i.cs.hku.hk/~tse/Papers/2000s/typssTR.pdf) | theoretical synthesis | D (secondary for originals) |
| 2002 | [Zeller & Hildebrandt, ddmin, TSE](https://www.st.cs.uni-saarland.de/papers/tse2002/tse2002.pdf) | algorithm + empirical | D |
| 2003 | [Broadwell et al., Scrash, USENIX Security](https://www.usenix.org/legacy/events/sec03/tech/full_papers/broadwell/broadwell.pdf) | design + empirical | D |
| 2006 | [Misherghi & Su, HDD, ICSE](https://web.cs.ucdavis.edu/~su/publications/icse06-hdd.pdf) | empirical | D |
| 2007 | [Emmi, Majumdar & Sen, ISSTA](https://typeset.io/pdf/dynamic-test-input-generation-for-database-applications-1hfczwa77z.pdf) | empirical | D (approach sections) |
| 2008 | [Castro, Costa & Martin, ASPLOS](https://doi.org/10.1145/1346281.1346322) | empirical | L |
| 2009 | [Clause & Orso, Camouflage TR GIT-CERCS-09-14](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf) | empirical | D |
| 2009 | [Glerum et al., WER, SOSP](https://www.sigops.org/s/conferences/sosp/2009/papers/glerum-sosp09.pdf) | documented practice | D |
| 2009 | [Elbaum et al., test carving, TSE](https://www.cs.uoregon.edu/events/icse2009/specialSessions/Carving%20and%20Replaying%20Differential%20Unit%20Test%20Cases%20from%20System%20Test%20Cases.pdf) | empirical | A |
| Sept 2010 | [Tuya et al., SQLFpc, STVR](https://giis.uniovi.es/testing/papers/stvr-2010-sqlfpc.pdf) | criterion + case study | D |
| 2010 | [Grechanik et al., ISSRE](https://ranger.uta.edu/~csallner/papers/grechanik10is.pdf) | empirical | D |
| May 2011 | [Clause, PhD thesis, Georgia Tech](https://repository.gatech.edu/server/api/core/bitstreams/c1cdccd9-cb7c-42c9-abf1-3e390dd74618/content) | empirical | D |
| 2011 | [Taneja et al., PRIEST, FSE](https://cdn.sanity.io/files/ku3lep2e/production/b448b278e0967a3a039f49eebe06870146e93839.pdf?dl=) | empirical + interviews | D |
| 2011 | [Budi et al., kb-anonymity, PLDI](https://doi.org/10.1145/1993498.1993551) | empirical | L |
| 2011 | [Schuler & Zeller, checked coverage, ICST](https://www.st.cs.uni-saarland.de/publications/files/schuler-icst-2011.pdf) | empirical | D |
| 2011 | [Robinson et al., Randoop at ABB, ASE](https://homes.cs.washington.edu/~mernst/pubs/maintainable-tests-ase2011.pdf) | industrial empirical | D |
| 2012 | [Lucia et al., kbe-anonymity, ASE](https://doi.org/10.1145/2351676.2351718) | empirical | L |
| 2012 | [Jin & Orso, BugRedux TR / ICSE](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2011/git-cercs-11-06.pdf) | empirical | D |
| 2012 | [Regehr et al., C-Reduce, PLDI](https://users.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf) | empirical | D |
| 2012 | [NIST IR 7878, combinatorial coverage](https://nvlpubs.nist.gov/nistpubs/ir/2012/NIST.IR.7878.pdf) | method | D |
| 21 Feb 2012 | [US 8,122,436 B2, privacy-enhanced error reports](https://patents.google.com/patent/US8122436B2/en) | theoretical metric | D |
| 2013 | [Chen et al., "Taming compiler fuzzers", PLDI](https://users.cs.utah.edu/~regehr/papers/pldi13.pdf) | empirical | D |
| 2013 | [Li et al., SCOPE failures, ICSE SEIP](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/icse13seip.pdf) | industrial empirical | D |
| 2013 | [Eder et al., test gap analysis, AST](https://wwwbroy.in.tum.de/publ/papers/AST13Hauptmann.pdf) | industrial empirical | D |
| 2013 | [Qiu, Li & Su, schema co-evolution, FSE](https://www.cs.ucdavis.edu/~su/publications/fse13-db-study.pdf) | empirical | A |
| c. 2013 | [Andrica & Candea, ReMoTe, EPFL](https://infoscience.epfl.ch/record/186762/files/main.pdf) | empirical | D |
| 2014 | [Li et al., PISTIS, ICST](https://www.cs.wm.edu/~denys/pubs/ICST'14-PISTIS-CRC.pdf) | empirical | D |
| 2014 | [Inozemtseva & Holmes, ICSE](https://cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf) | empirical | D |
| 2014 | [Just et al., mutants vs real faults, FSE](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf) | empirical | D |
| 2014 | [Groce et al., cause reduction, ICST](https://collections.lib.utah.edu/dl_files/8e/ea/8eea2537954679d0e007f1ad9620167d40d6772e.pdf) | empirical | D |
| 2014 | [Shi et al., test-suite reduction, FSE](https://mir.cs.illinois.edu/awshi2/publications/FSE2014.pdf) | empirical | D |
| 2014 | [Böhme & Paul, efficiency of automated testing, FSE](https://www.st.cs.uni-saarland.de/~boehme/paper/FSE14.pdf) | theoretical | D |
| 2014 | [Yuan et al., "Simple Testing Can Prevent Most Critical Failures", OSDI](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-yuan.pdf) | empirical | D |
| 2014 | [Luo et al., flaky tests, FSE](https://huang.isis.vanderbilt.edu/cs8395/paper/flakytest.pdf) | empirical | D |
| 29 Sept 2014 | [Newcombe et al., formal methods at AWS](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) | industrial practice | D |
| 2015 | [Chandra et al., XData, VLDB J. (arXiv 1411.6704)](https://arxiv.org/pdf/1411.6704) | empirical | D |
| 2015 | [Shamshiri et al., generated tests vs real faults, ASE](http://www.evosuite.org/wp-content/papercite-data/pdf/ase15_faults.pdf) | empirical | D |
| 2015 | [Gay et al., coverage risks, TSE](https://conservancy.umn.edu/bitstream/handle/11299/217451/15covrisks.pdf?sequence=1) | empirical | L |
| 2015 | [Zhang & Mesbah, assertions, FSE](https://people.ece.ubc.ca/amesbah/resources/papers/fse15.pdf) | empirical | D |
| 2015 | [Casalnuovo et al., assert use, ICSE](https://www.cs.ucdavis.edu/~filkov/papers/assert-main.pdf) | empirical | A |
| 2015 | [Blum & Hardt, Ladder, ICML (arXiv 1502.04585)](https://arxiv.org/abs/1502.04585) | theoretical | D |
| 2015 | [Dwork et al., holdout reuse (arXiv 1506.02629)](https://arxiv.org/abs/1506.02629) | theoretical | D |
| 2015 | [Chen & Kim, STAR, TSE](https://people.csail.mit.edu/hunkim/papers/chen-tse2015.pdf) | empirical | A |
| 2016 | [Niedermayr et al., pseudo-tested methods, CSED](https://arxiv.org/pdf/1611.07163) | empirical | D |
| 2016 | [Blanco et al., entity reconciliation testing, A-TEST](https://giis.uniovi.es/testing/papers/a-test-2016-testing-entity-reconciliation.pdf) | proposal | D |
| 2016 | [Scott et al., DEMi, NSDI](https://www.usenix.org/system/files/conference/nsdi16/nsdi16-paper-scott.pdf) | empirical | D |
| 2016 | [Juergens & Pagano, TGA whitepaper (CQSE)](https://teamscale.com/hubfs/26978363/Publications/2016-did-we-test-the-right-thing-experiences-with-test-gap-analysis-in-practice.pdf?hsLang=en) | vendor practice | D/V |
| 2016 | [Tuya et al., coverage-aware test DB reduction, TSE](https://doi.org/10.1109/tse.2016.2519032) | empirical | L |
| 2017 | [Wang, Brun & Orso, field vs tests, ICST](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf) | empirical | D |
| 2017 | [Chekam et al., ICSE](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf) | empirical | D |
| 2017 | [Gulzar et al., BigSift, SoCC](https://people.cs.vt.edu/~gulzar/assets/pdf/socc17-final244-acmpaginated.pdf) | empirical | D |
| 2017 | [Gazzola et al., field failures (arXiv 1708.09494)](https://arxiv.org/pdf/1708.09494) | empirical | D |
| June 2017 | [Barrientos et al., NBER WP 23534](https://www.nber.org/papers/w23534.pdf) | method + practice | D |
| c. 2017–18 (inferred) | [ONS Working Paper 16, synthetic data pilot](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot) | guidance | D |
| 2018 | [Castelein et al., EvoSQL, ICSE](https://repository.tudelft.nl/file/File_6c2d74fc-0c7b-4248-b0a8-decdf4360c20) | empirical | D |
| 2018 | [Papadakis et al., ICSE](https://coinse.github.io/publications/pdfs/Papadakis2018aa.pdf) | empirical | D |
| 2018 | [Schelter et al., Deequ, PVLDB](https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf) | system + evaluation | D |
| 2018 | [Petrović & Ivanković, mutation at Google, ICSE-SEIP](https://research.google.com/pubs/archive/46584.pdf) | industrial practice | D |
| 2018 | [Soltani et al., EvoCrash, TSE](https://pure.tudelft.nl/ws/files/72125983/08502801.pdf) | empirical | D |
| 2018 | [Homayouni, MSc thesis, Colorado State](https://mountainscholar.org/bitstream/10217/189268/1/Homayouni_colostate_0053N_14638.pdf) | empirical | D (abstract/summary) |
| 2018 | [Rott et al., ticket coverage (arXiv 1804.07599)](https://arxiv.org/pdf/1804.07599) | industrial empirical | D |
| 2018 | [Sun et al., Perses, ICSE](https://web.cs.ucdavis.edu/~su/publications/perses.pdf) | empirical | A |
| Aug 2018 | [Satvat & Saxena, crash reports (arXiv 1808.01718)](https://arxiv.org/abs/1808.01718) | empirical | D |
| 2019 | [Gulzar et al., BigTest, ESEC/FSE](http://web.cs.ucla.edu/~miryung/Publications/fse2019-bigtest.pdf) | empirical | D |
| 2019 | [Danglot et al., test amplification, JSS](https://arxiv.org/pdf/1705.10692) | review | D |
| 2019 | [Felderer et al., testing data-intensive systems](https://arxiv.org/pdf/1903.09413) | exploratory review | D |
| 2019 | [Miao, Roy & Yang, smallest counterexample DB, SIGMOD](https://arxiv.org/pdf/1904.04467) | algorithm + evaluation | D |
| 2019 | [McMinn et al., ineffective mutants, TSE](https://eprints.whiterose.ac.uk/126146/1/ineffective-mutants.pdf) | empirical | D |
| 2019 | [Vera-Pérez et al., pseudo-tested methods, EMSE](https://arxiv.org/pdf/1807.05030) | empirical | D |
| Sept 2019 | [Vera-Pérez et al., Reneri (arXiv 1909.04770)](https://arxiv.org/pdf/1909.04770) | empirical | D |
| Dec 2019 | [Wang, PhD thesis (Replica, VASE), Georgia Tech](https://repository.gatech.edu/server/api/core/bitstreams/fbbb8c33-f80f-4852-afda-249c1cb047a4/content) | empirical | D |
| 2019 | [Kotsogiannis et al., PrivateSQL, PVLDB](https://www.vldb.org/pvldb/vol12/p1371-kotsogiannis.pdf) | system + evaluation | D |
| 2020 | [Arcuri & Galeotti, EvoMaster SQL, TOSEM](https://raw.githubusercontent.com/WebFuzzing/EvoMaster/master/docs/publications/2020_tosem.pdf) | empirical | D |
| 2020 | [Soltana et al., PLEDGE, TOSEM](https://arxiv.org/pdf/1902.00397) | industrial empirical | D |
| 2020 | [Kingsbury & Alvaro, Elle, VLDB](https://arxiv.org/pdf/2003.10554) | theory + empirical | D |
| 2020 | [Davis et al., eXtreme Modelling at MongoDB, PVLDB](https://arxiv.org/pdf/2006.00915) | industrial empirical | D |
| 2020 | [Zhang et al., BigFuzz, ASE](http://web.cs.ucla.edu/~miryung/Publications/ase2020-bigfuzz.pdf) | empirical | D |
| 2020 | [MacIver & Donaldson, internal reduction, ECOOP](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.13/LIPIcs.ECOOP.2020.13.pdf) | empirical | D |
| 2020 | [Rigger & Su, pivoted query synthesis, OSDI](https://arxiv.org/pdf/2001.04174) | empirical | D |
| 2021 | [Bertolino et al., field-testing survey, ACM CSUR](https://iris.cnr.it/bitstream/20.500.14243/401252/2/prod_453662-doc_174541.pdf) | systematic survey | D |
| 2021 | [Petrović et al., mutation at Google (arXiv 2102.11378)](https://arxiv.org/pdf/2102.11378) | industrial empirical | D |
| 2021 | [Petrović et al., ICSE (arXiv 2103.07189)](https://arxiv.org/pdf/2103.07189) | industrial empirical | D |
| 2021 | [Tiwari et al., Pankti, IEEE Trans. Reliability](https://arxiv.org/pdf/2012.01198) | empirical | D |
| 2021 | [Gruber et al., Python flaky tests, ICST](https://arxiv.org/pdf/2101.09077) | empirical | A |
| 1 Mar 2021 | [Gao et al., TDCommons #4113](https://www.tdcommons.org/dpubs_series/4113) | defensive publication | L |
| 5 Aug 2021 | [Uber, data quality platform](https://www.uber.com/blog/operational-excellence-data-quality/) | practice | B |
| 2021 / 2022 | [de Souza Neto et al., TRANSMUT-Spark](https://arxiv.org/pdf/2108.02589) | tool + empirical | D |
| 2022 | [Parry et al., flaky test survey, TOSEM](https://o-parry.github.io/papers/2021a.pdf) | review | A |
| 2022 | [Zhang, Arcuri et al., EvoMaster at Meituan](https://arxiv.org/pdf/2208.03988) | industrial empirical | D |
| 2022/23 | [Arshad et al., big-data testing SLR, CMC](https://www.techscience.com/cmc/v74n2/50213/html) | systematic review | D |
| 2023 | [Yan, Nath & Lu, DBGriller, ICSE](https://par.nsf.gov/servlets/purl/10447174) | empirical | D |
| 2023 | [Blanco, Tuya & Seco, business-rule MCDC (arXiv 2304.12671)](https://arxiv.org/pdf/2304.12671) | method + case | D |
| 2023 | [Foidl et al., data pipeline quality (arXiv 2309.07067; JSS 2024)](https://arxiv.org/pdf/2309.07067) | empirical + MLR | D |
| Sept 2023 | [NIST SP 800-188](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf) | standard/guidance | D |
| Dec 2023 | [Ding et al., SQLSolver, PACMMOD/SIGMOD](https://par.nsf.gov/servlets/purl/10548354) | empirical | D |
| 7 Dec 2023 | [GetYourGuide, DDataflow](https://www.getyourguide.careers/posts/ddataflow-a-tool-for-data-end-to-end-tests-for-machine-learning-pipelines) | practice | B |
| 2024 | [Masserini et al., AST (arXiv 2402.07460)](https://arxiv.org/pdf/2402.07460) | empirical | D |
| 2024 | [Goldstein et al., PBT in practice, ICSE](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice.pdf) | interview study | D |
| 2024 | [Ivanković et al., Productive Coverage, ICSE-SEIP](https://homes.cs.washington.edu/~rjust/publ/productive_coverage_icse_2024.pdf) | industrial RCT | D |
| 2024 | [He et al., VeriEQL, OOPSLA](https://arxiv.org/pdf/2403.03193) | empirical | D |
| 2024 | [Wang, Pan & Cheung, QED, PVLDB](https://vldb.org/pvldb/vol17/p3602-wang.pdf) | empirical | D |
| 2024 | [Lin & Reiter, DP verification (arXiv 2404.02519)](https://arxiv.org/abs/2404.02519) | method | D |
| 2024 | [Lin et al., SQLess, ISSTA](https://matafeiyanll.github.io/paper/Issta24.pdf) | empirical | A |
| July 2024 | [Lam et al., synthetic identifiers, IJPDS](https://discovery.ucl.ac.uk/10194216/1/ijpds-09-2389.pdf) | empirical | A |
| July 2024 | [Behjati et al., position paper (arXiv 2407.05410)](https://arxiv.org/pdf/2407.05410) | proposal | D |
| 2024 | [Tiwari et al., RICK, TSE](https://arxiv.org/pdf/2208.01321) | empirical | D |
| 17 May 2024 | [datafold/data-diff discontinuation notice](https://raw.githubusercontent.com/datafold/data-diff/master/README.md) | project notice | D |
| 2025 | [Haas et al., risk-prioritised test gaps, TSE](https://www.se.cs.uni-saarland.de/publications/docs/HSJ+25.pdf) | industrial empirical | A |
| 12 Jun 2025 | [Uber, Hive to Spark SQL migration](https://www.uber.com/us/en/blog/how-uber-migrated-from-hive-to-spark-sql-for-etl-workloads/) | practice | B |
| Feb 2026 | [Tammisto et al., SLR, Expert Systems (arXiv 2602.06609)](https://arxiv.org/pdf/2602.06609) | systematic review | D |
| 12 May 2026 | [Meta, ingestion migration](https://engineering.fb.com/2026/05/12/data-infrastructure/migrating-data-ingestion-systems-at-meta-scale/) | practice | B |
| Oct 2026 | [Wu et al., Holey (arXiv 2606.11132 v2)](https://arxiv.org/pdf/2606.11132) | empirical | D |
| Oct 2026 | [Snapshot testing study (arXiv 2610.29549)](https://arxiv.org/abs/2610.29549) | empirical | A |
| footer July 2026 | [Every Cure ADR, testing through sampling](https://docs.dev.everycure.org/infrastructure/architecture_decision_records/improve_testing_through_sampling/) | practice | B |
| retrieved 2026-11-25 | [OpenSAFELY documentation (workflow, SDC, release)](https://raw.githubusercontent.com/opensafely/documentation/main/docs/outputs/sdc.md) | documented practice | D |
| 1996 (as adopted) | [EU Database Directive 96/9/EC, Art. 7](https://www.legislation.gov.uk/eudr/1996/9/article/7/adopted) | law | D |
| July 2005 | [BHB v William Hill, EWCA Civ 863](https://caselaw.nationalarchives.gov.uk/ewca/civ/2005/863) | case law | D (CJEU text U) |
| 2019 (PDF 25 Mar) | [Royal Mail PAF Data Solutions Provider Licence](https://www.poweredbypaf.com/wp-content/uploads/2019/06/paf-data-solutions-provider-licence-2019-1.pdf) | licence | D |
| 2020 | [WHO ICD-11 licence](https://icd.who.int/en/docs/icd11-license.pdf) | licence | D |
| current | [GLEIF LEI data terms](https://www.gleif.org/en/meta/lei-data-terms-of-use); [OpenFIGI ToS, 27 Nov 2018](https://www.openfigi.com/docs/terms-of-service); [SIX ISO 4217](https://www.six-group.com/en/products-services/financial-information/data-standards.html) | licence / rights-holder | D / V |
| 2026 | [DataMagnet blog](https://www.datamagnet.co/post/synthetic-data-testing-data-quality-rules/); [Varigence](https://www.varigence.com/blog/row-counts-lie-column-control-totals) | vendor claims | V |
| — | [Earlier report, Synthetic stand in test data](Synthetic%20stand%20in%20test%20data.md) (background for sections 7–8 only) | prior synthesis | — |
