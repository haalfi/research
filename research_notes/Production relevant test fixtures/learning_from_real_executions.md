# Learning from real executions: turning production execution information into fictional test inputs or better tests

Scope note: these notes catalogue approaches that capture execution-level information where the real data lives (paths, path conditions, call sequences, coverage, invariants, stack traces, usage profiles, query-plan cardinalities) and use it to build fictional inputs or better tests outside. Status tags:
- **[documented]**: I read the full text, or the relevant full-text section, myself.
- **[lead]**: the claim comes only from a search extract, abstract metadata or a secondary citation.
- **[inferred]**: my own reasoning, not taken from a source.
- **[unreachable]**: I tried to get the full text and failed.
- **[vendor]**: an unverified claim from a vendor or practitioner blog.

All PDFs were read with `pdftotext` in the scratchpad. Dates are publication dates.

## 1. Privacy-preserving failure and test-input reproduction (path-condition and behaviour-preserving anonymisation)

### Takeaway
One line of work keeps the execution path and throws the record away. It solves the failing run's path condition, or the branch behaviour it exercised, inside the owner's environment, and ships a different input that takes the same path. The original input never leaves:
- Castro et al. 2008
- Camouflage (Clause and Orso)
- kb-anonymity and kbe-anonymity
- ReMoTe (Andrica and Candea)

What does leak is the path condition, which fixes the values that branches depend on. Disclosure was measured as bits revealed, residue, and k-anonymity. Camouflage revealed about 31% of input bits on average and kept about 30% of the input unchanged (residue). It reproduced every failure it was tried on (170 inputs). The leaked information was mostly structural.

A second strand releases sanitised real records: PRIEST, and PISTIS (Li et al.). Original values, or values derived from them, still leave in permuted, swapped or centroid form. That is a different trust model.

### Cited Findings

**Castro, Costa and Martin (ASPLOS 2008)**
- **[lead]** The approach gives vendors "new input values that satisfy the conditions required to make the software follow the same execution path until it fails, but are otherwise unrelated with the original inputs". It also provides "a mechanism to measure the amount of information revealed in an error report", so users can decide whether to submit. The abstract claims "revealing almost no private information" — [OpenAlex abstract, Castro et al. 2008](https://doi.org/10.1145/1346281.1346322).
- **[unreachable]** Full text. The lara.epfl.ch copy returned an HTML page and the MSR URL returned 403. [MSR page](https://www.microsoft.com/en-us/research/publication/better-bug-reporting-with-better-privacy/)
- **[documented, secondary]** Camouflage's related-work section says Castro et al. work on x86 binaries, use conventional symbolic execution, and are not publicly available — [Clause & Orso TR GIT-CERCS-09-14 (2009)](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf).

**Camouflage (Clause and Orso; tech report 2009, published ICSE 2011)**

All findings below are **[documented]** from the TR version, "Camouflage: Automated Sanitization of Field Data". The [ICSE 2011 version](https://researchr.org/publication/ClauseO11) is DOI 10.1145/1985793.1985797 and its full text was not retrieved. Source for all: [TR](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf).
- **Mechanism.**
  - It replays a captured failing execution, symbolically executes it, and computes the path condition φ.
  - It then picks I′ from the inputs satisfying φ, excluding I, so that I′ "(1) still causes f and (2) reveals as little information about I as possible".
  - "Path condition relaxation" optimisations (multi-clause conditionals, switches, array comparisons) enlarge the satisfying set.
- **Assumptions.**
  - An input satisfying φ is assumed to give the same failure.
  - The stated threats are non-determinism and implicit runtime checks.
- **What leaks.**
  - "It is, in general, impossible to construct I′ such that it does not reveal any information about I while still causing the same failure f".
  - The information revealed "tended to be structural in nature (e.g., a specific portion of the input must be surrounded by double quotes)". Values likely to be sensitive were not revealed.
- **Measuring disclosure.**
  - Bits of information revealed: Σ|log2(x_i)|, where x_i is the number of solutions for element i, computed with Martin's over-approximation algorithm.
  - Residue: the share of input elements left unchanged. It was added because the bits metric can fall while large parts of the input stay identical.
- **Subjects.** 170 failure-inducing inputs, from several hundred bytes to over 5 MB:
  - NanoXML (16 faults)
  - Java printtokens (2 faults)
  - Columba address book (1 fault)
  - htmlparser (1 fault)
  - The Columba and htmlparser inputs were hand-built.
- **Results.**
  - Every input was sanitised and reproduced the failure.
  - Path-condition generation averaged 162 s (printtokens) to 533 s (htmlparser).
  - Average bits revealed ranged from 2.3% to 76.5%, overall average 30.6%.
  - Residue ranged from 1.5% to 65%, overall average 30%.
  - A manual qualitative review (RQ3) judged that no sanitised input revealed sensitive information.
  - Internal inconsistency: the intro summary says revealed information ranged from "≈60% (in the worst case) to ≈2%". Section 4.4 says 2.3% to 76.5%.
- **Comparison with Castro.** The authors re-implemented Castro's technique in Java Path Finder (JPF). Camouflage needed slightly more time but revealed "30% less bits" and "40% less residue", with "the caveat of a potential implementation bias".
- **Why classic database anonymisation was rejected.** Approaches that preserve statistical properties by merging or adding noise were judged "not suitable for our scenario" because "the conditions for reproducing a failure are typically very specific".

**kb-anonymity (Budi, Lo, Jiang and Lucia, PLDI 2011)**

Note: the brief says ICSE 2011, but the indexes list it at PLDI 2011, pp. 447–457, DOI 10.1145/1993498.1993551.
- **[lead]** It targets industrial clients' collected input data ("highly valuable as they represent the operations that matter in a client's daily business"). It argues that simply masking values fails, because "correlation among fields in the data can reveal the masked information" and because "masked data may exhibit different behavior in the system". It combines k-anonymity with program-behaviour preservation — [OpenAlex abstract](https://doi.org/10.1145/1993498.1993551); [SMU record](https://ink.library.smu.edu.sg/sis_research/1390).
- **[unreachable]** Full text. The SMU viewcontent PDF returned HTML or 403 to both curl and WebFetch.

**kbe-anonymity (Lucia, Lo, Jiang and Budi, ASE 2012), the "2012 extension"**
- **[lead]** "When multiple versions of the data are cross-referenced, private information could be inferred". Applying kb-anonymity repeatedly to evolving programs is a privacy risk, and kbe-anonymity addresses it. It was evaluated on three Java programs — [OpenAlex abstract](https://doi.org/10.1145/2351676.2351718); [SMU record](https://ink.library.smu.edu.sg/sis_research/1593).

**ReMoTe (Andrica and Candea, EPFL, about 2013)**

All **[documented]**. Source: [EPFL infoscience](https://infoscience.epfl.ch/record/186762/files/main.pdf).
- **Mechanism.** It transforms Android interaction traces so they "provide k-anonymity to users". Concolic execution generates alternative values, such as server responses, that drive the same program decisions. Users are told how much identifying information remains and can veto sharing.
- **Evaluation.** On PocketCampus, some response fields had more than 100 alternatives. Other fields had none, because they were floating point (not supported by the solver) or compared against constants such as a status code.
- [Inferred] So an execution-path approach leaks exactly the fields that branch on constants.

**PRIEST (Taneja, Grechanik, Ghani and Xie, FSE 2011)**

All **[documented]**. Source: [author-uploaded PDF](https://cdn.sanity.io/files/ku3lep2e/production/b448b278e0967a3a039f49eebe06870146e93839.pdf?dl=); DOI 10.1145/2025113.2025143.
- **Setting.** Database-centric applications (DCAs).
- **Mechanism.** Program analysis determines "how values of database attributes affect test coverage". A privacy framework combines guessing-anonymity metrics with data swapping, so "organizations [can] keep original values" while anonymising.
  - **What leaves:** the swapped original values. Real values leave, in permuted form.
- **Documented practice (interviews).** The authors interviewed IBM, Accenture, two health insurers, a biopharma firm, two supermarket chains and three banks. They found "current test data anonymization is manual, laborious, and error-prone".
  - They also describe "cleanroom testing": the DCA and database stay on premises, testers are monitored, and network connections and USB keys are forbidden.
  - [Inferred] This matches the brief's protected-environment setting.
- **Results (Table 6, statement coverage TC versus privacy level PM2).**

  | Subject | TC range as PM2 rises | PM2 range |
  |---|---|---|
  | N2A | stays 49–51% | 0.70–0.83 |
  | DurboDax | 72% to 57% | 0.01–1.00 |
  | UnixUsage | 60% to 56% | — |
  | RiskIt | 57% to 52–53% | — |

  The coverage estimator's error was 2.0%–8.3%.

**Grechanik, Csallner, Fu and Xie (ISSRE 2010)**
- **[lead]** "A popular data anonymization algorithm called k-anonymity seriously degrades test coverage of DCAs". The proposed fix is program-analysis-guided selective k-anonymity — [OpenAlex abstract](https://doi.org/10.1109/issre.2010.13).

**PISTIS (Li, Grechanik and Poshyvanyk, ICST 2014), the "Li et al." work**
- **[documented]** Source: [author PDF](https://www.cs.wm.edu/~denys/pubs/ICST'14-PISTIS-CRC.pdf).
  - Weight-based clustering uses weights from program analysis of how attributes are used. It releases centroid objects per cluster, with association-rule constraints to keep them representative.
  - Claims: "we reduce a large database to a few centroid objects and … test coverage stays within a close range to its original level".
  - Random deletion of records "often leads to significantly worsened test coverages".
  - What leaves: centroids derived from real records.
  - Subjects: DurboDax and RiskIt.
  - Some branch coverages are low even on the original data (19.33% and 12.99%).

**Masserini, Ginelli, Micucci, Briola and Mariani, "Anonymizing Test Data in Android: Does It Hurt?" (AST 2024)**

All **[documented]**. Source: [arXiv 2402.07460](https://arxiv.org/pdf/2402.07460). Reported as the first empirical study of the cost of anonymisation for failure reproduction.
- **Design.**
  - 19 bugs in 17 Android apps.
  - Five generalisation, suppression and perturbation techniques applied to failure traces: Global Recoding, Rounding, Local Suppression, Special-Char-Driven (SCD) Local Suppression, and Noise Addition.
- **Results.**
  - Plain Local Suppression on strings: success rate 11%–19%.
  - SCD Local Suppression, which keeps only special characters: mean 49%.
  - Generalisation had a "noticeable, but not dramatic, impact" (41% success rate).
  - Keeping more information raised success "up to 63%", at the cost of more disclosure.
- **Conclusion.** Strings are best handled with SCD Local Suppression. Numbers are best handled with Local Suppression or Noise Addition.
- This is negative or partial evidence: value-level anonymisation of traces often loses reproducibility.

### Inferences
- **[inferred]** Two trust models should be kept apart in the final report:
  - (a) Path- or behaviour-preserving synthesis. Only constraint-derived fictional inputs leave: Castro, Camouflage, ReMoTe, and the call-sequence synthesis in section 2.
  - (b) Transformed real records leave: PRIEST (swapping), PISTIS (centroids), and classical k-anonymity.

  Only (a) fits a rule that original records never leave. Even (a) leaks the constants and relations on the failing path, as measured by bits and residue.
- **[inferred]** Every documented evaluation is on single programs with file or record inputs (NanoXML, printtokens, Java DCAs, Android apps). None evaluates multi-source entity resolution, incremental or stateful pipelines, or SQL/dataflow engines. Symbolic execution over a SQL or Spark pipeline would need an engine that models the query semantics. That is a gap, not evidence that it is impossible.

### Gaps
- Full texts of Castro 2008 and kb-anonymity 2011 were unreachable, so their disclosure metrics and quantitative results are not verified here.
- I did not find "PRIEST" described as "privacy-preserving test outsourcing" beyond the FSE 2011 paper and its precursor at privacytesting.org, which I did not fetch.
- No study found measures preserved fault-revealing power for faults that were not the observed failure. Camouflage, Castro and kb-anonymity reproduce known failures or preserve coverage. They do not measure detection of new faults.

## 2. Field failure reproduction from limited field data

### Takeaway
The data needed ranges from nothing beyond a crash report (ESD, STAR, EvoCrash) to call sequences (BugRedux, F3).

BugRedux found that call sequences are the "sweet spot":
- 16 of 17 failures reproduced.
- 1%–50% runtime overhead.
- Unlikely to reveal input values.

Point-of-failure or stack trace alone was often insufficient. Complete branch traces gave "too much guidance" and mostly failed in the solver.

Stack-trace-only Java tools reproduce roughly 43%–85% of crashes, depending on the benchmark:
- STAR: 31 of 52 exploited (59.6%), 22 useful (42.3%).
- EvoCrash: 85% on 54 crashes.
- JCrashPack: 43% of 200.

### Cited Findings

**BugRedux (Jin and Orso, ICSE 2012)**

All **[documented]**. Source: [TR GIT-CERCS-11-06](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2011/git-cercs-11-06.pdf); ICSE 2012 pp. 474–484.
- **Mechanism.** It synthesises an execution E′ that mimics field failure F using guided symbolic execution (KLEE-based, C). Intermediate goals come from field data.
- **Data levels compared.**
  - Point of failure (POF)
  - Call stack
  - Call sequence: call sites traversed
  - Complete trace: all branches
- **Subjects.** 17 crash failures in 15 programs from SIR, BugBench and exploit databases (sed, grep, gzip, exim, rsync, xmail, and others). Some programs were excluded because the symbolic engine "could not handle some of the constructs", such as environment and network inputs.
- **Overhead (Table II).**
  - POF and call stack: 0%.
  - Call sequence: 1%–50%.
  - Complete trace: 8%–1066%.
- **Data size (Table III).**
  - Call sequence: 0.7–100.7 KB.
  - Complete trace: up to 14,897 KB.
- **Results.**
  - For seven simple programs, reaching the POF was enough.
  - For grep, gzip, htget and aspell, call-stack guidance produced executions with the same call stack that did not reproduce the failure.
  - Call sequences reproduced 16 of 17 failures.
  - Complete traces "provide too much guidance" and produce long paths with constraints the SMT solver cannot handle.
- **Privacy.** "Call sequences are unlikely to reveal sensitive or confidential information". The authors call this "just anecdotical evidence". No synthesised input matched the original. In ncompress, the original 1,520 "a" characters became more than 1,600 random characters.

**F3 (Jin and Orso, ISSTA 2013)**
- **[lead]** It extends BugRedux to generate multiple failing and passing executions "similar" to the field failure, combined with customised fault localisation. "For all the failures considered, F3 was able to (1) synthesize passing and failing executions and (2) successfull[y localise]…" — [OpenAlex abstract](https://doi.org/10.1145/2483760.2483763).
- **[unreachable]** Full text: the Orso-hosted URLs returned 404.

**ESD execution synthesis (Zamfir and Candea, EuroSys 2010)**
- **[documented, abstract and introduction]** Source: [EPFL PDF](https://dslab.epfl.ch/pubs/esd.pdf).
  - Input is the program plus a bug report or coredump (call stacks of deadlocked threads, and so on).
  - It uses no runtime recording, "thus incurring no runtime overhead".
  - Static analysis plus symbolic execution plus schedule synthesis.
  - It "reproduces on its own several real concurrency and memory safety bugs in less than three minutes".
  - The output is a trace replayable in a debugger, which may contain synthesised inputs (e.g. getchar() returning 'm').

**STAR (Chen and Kim, TSE 2015)**
- **[documented, abstract]** Source: [author PDF](https://people.csail.mit.edu/hunkim/papers/chen-tse2015.pdf).
  - It uses crash stack traces only.
  - Backward symbolic execution computes crash preconditions, and method-sequence composition builds the test.
  - "Without incurring additional runtime overhead".
  - It "successfully exploited 31 (59.6%) of 52 crashes in three open source projects. Among these exploitable crashes, 22 (42.3%) are useful reproductions".

**EvoCrash (Soltani, Panichella and van Deursen, TSE 2018)**

All **[documented]**. Source: [TU Delft PDF](https://pure.tudelft.nl/ws/files/72125983/08502801.pdf).
- **Inputs.** A crash stack trace plus bytecode. Search-based Guided Genetic Algorithm (GGA) on top of EvoSuite.
- **Results on 54 crashes.**
  - More crashes replicated than STAR (+23%), MuCrash (+17%) and JCHARMING (+25%).
  - EvoCrash reproduced 85% versus EvoSuite's 33%. Average time was 145 s versus 391 s.
  - Authors' conclusion: "coverage-based test generation lacks adequate guidance for crash reproduction".
- **Controlled experiment.** 35 master's students: +21% fixes and −15.36% time.
- **Motivation.** Record-replay can mean overhead and "privacy violations since the collected execution data may contain sensitive information".

**JCrashPack benchmark (Soltani et al., EMSE 2020)**
- **[lead]** 200 stack traces, including industrial open-source projects. "EvoCrash successfully reproduced 43% of the crashes". NPE, IllegalArgument and IllegalState were easier than ClassCast and IndexOutOfBounds — [OpenAlex abstract](https://doi.org/10.1007/s10664-019-09762-1).
- **[unreachable]** Springer full text: the redirect needs login.

**Botsing tool**
- **[documented]** It "implements and extends the EvoCrash approach and relies on EvoSuite". Apache-2.0. Last commit 2021-04-07, so effectively unmaintained since 2021. Funded by EU H2020 STAMP — [Botsing README, via git clone](https://github.com/STAMP-project/botsing).

**Field-based testing survey (Bertolino et al., ACM CSUR 2021)**
- **[lead]** "The first systematic survey of field testing approaches over a body of 80 collected studies" — [OpenAlex abstract](https://doi.org/10.1145/3447240).

### Inferences
- **[inferred]** Mapped onto the brief's setting:
  - A stack trace or exception type plus a call sequence, which is non-value information, is the documented low-disclosure, high-yield signal for reproducing crashes.
  - Reproducing wrong output, which is the typical data-platform defect (a wrong merge or a wrong reconciliation), is not covered. BugRedux chose crash faults "for convenience". ESD, STAR and EvoCrash target crashes or deadlocks.
- **[inferred]** Every tool here needs the program under analysis to be amenable to symbolic execution or search: C via KLEE, Java bytecode via EvoSuite. SQL, dbt or Spark transformations are not handled by these tools as published.

### Gaps
- I found no evaluation of crash-reproduction tools on ETL, entity-resolution or reconciliation code, and none for non-crash (wrong-result) failures.
- F3 and JCrashPack full-text numbers were not verified.

## 3. Production-informed test generation, selection and augmentation (operational profiles, carving, production monitoring, field-versus-test comparisons)

### Takeaway
There is direct empirical evidence that in-house tests are not representative of field behaviour. Across four systems (Wang, Brun and Orso, ICST 2017), tests miss:
- 6.2% of statements run in the field
- 7.7% of methods run in the field
- 52.6% of temporal invariants seen in the field

Field-only behaviour kills 8.6% more mutants. Coverage-driven EvoSuite augmentation did not close the mutant or invariant gap.

Techniques that turn field observations into tests:
- **Replica:** field call sequences, invariant violations, then guided symbolic execution. It covered 56% of untested field invariants, versus 4.7% for random KLEE.
- **Pankti, RICK and PROZE:** they serialise production objects into differential, mock-based or parameterised unit tests. These transfer real argument values unless restricted.
- **Carving (Elbaum):** it captures concrete pre-states.
- **Google's Productive Coverage:** production CPU-sampling frequency is used to prioritise untested code.
- **Musa's operational profile:** test selection weighted by usage frequency.

### Cited Findings

**Wang, Brun and Orso, "Behavioral Execution Comparison: Are Tests Representative of Field Behavior?" (ICST 2017)**

All **[documented]**. Source: [UMass PDF](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf).
- **Subjects.**
  - JetUML, deployed to 83 human subjects.
  - Commons IO, Commons Lang and Log4j, exercised by client projects' tests mined from GitHub.
- **Four behaviour models.**
  - Statement coverage
  - Method coverage
  - Mutation (libraries only)
  - kTails temporal invariants via InvariMint
- **Results.**
  - Tests miss 6.2% of field statements and 7.7% of field methods.
  - Field-only behaviour kills 8.6% more mutants.
  - Tests miss 52.6% of field invariants.
  - EvoSuite augmentation "slightly improved the test suites in terms of coverage, but not at all in terms of killed mutants and behavioral invariants".
  - Some code exercised by both tests and the field "was used in a behaviorally different way". For example, users perform operations in a different order.

**Replica and VASE (Qianqian Wang PhD thesis, Georgia Tech, December 2019)**

All **[documented]**. Source: [repository.gatech.edu](https://repository.gatech.edu/server/api/core/bitstreams/fbbb8c33-f80f-4852-afda-249c1cb047a4/content).
- **Replica mechanism.**
  1. It infers invariants from in-house tests.
  2. It ships an instrumented build that records method call sequences in the field and flags invariant violations, i.e. untested behaviour.
  3. It generates tests that hit the same violations with incremental, guided symbolic execution.
- **Privacy claim.** Generated inputs are "potentially quite different from the user inputs, thus mitigating privacy-violation concerns". This is a claim; no disclosure was measured.
- **Field data.** The thesis introduction mentions execution data from 747 real users.
- **Subjects.** TSL generator, grep, sed and gzip.
- **Coverage of field-only invariants.**
  - Replica covered 73.7%, 50.4%, 45.4% and 54.4% respectively (average 56.0%).
  - Random-search KLEE averaged 4.7%: an "11.9 times" improvement.
- **Mutants killed by field executions but not by in-house tests.**
  - Replica killed 79.4% (TSL), 41.4% (sed) and 63.3% (gzip).
  - KLEE averaged 19.5%.
- **Failures.** Replica failed on nested compound conditions, where the solver times out.
- **Overhead.** Field instrumentation averaged 13%, up to 23% (gzip), with "naive" logging.
- **VASE.** It uses observed runtime values: variables with a limited number of observed values, or properties that hold for all observed values. These speed up constraint solving.
  - [Inferred] This is a documented use of captured value domains and boundaries to steer generation.

**Pankti (Tiwari, Zhang, Monperrus and Baudry, IEEE Transactions on Reliability 2021)**

All **[documented]**. Source: [arXiv 2012.01198](https://arxiv.org/pdf/2012.01198).
- **What is captured.** For target methods, it serialises the receiving object, the arguments and the return value with XStream in production. It then generates differential unit tests with derived oracles.
- **Results.**
  - Targets: 86 weakly tested ("pseudo-tested") methods in Jitsi, PDFBox and Broadleaf.
  - Observed 122,194 invocations.
  - Generated 14,222 tests, of which 13,878 (97.6%) pass.
  - Test quality improved for 53 of 86 methods (61.6%).
- **Overhead.**
  - Jitsi CPU 0.1% to 5.5%, memory 338 MB to 902 MB.
  - Broadleaf CPU 16.4% to 41.8%, with +185 ms average HTTP response time.
- **Privacy.** "Object profiles may contain sensitive information, such as user names and passwords". The only mitigation is an auditable list of target methods to instrument.
  - [Inferred] Real values become test fixtures, so this violates a rule that real records must not leave unless the values are synthesised or sanitised.
- **Tool.** MIT licence. The repository also contains RICK. Last commit 2024-11-01 — [README](https://github.com/castor-software/pankti).

**RICK (Tiwari, Monperrus and Baudry; TSE 2024, ICSE 2025 journal-first)**
- **[documented]** It generates tests with mocks, stubs and mock-based oracles from production observations. All tests are executable, and 294 (52.4%) "successfully recreate the complete production context". The authors interviewed 5 industry developers — [arXiv 2208.01321](https://arxiv.org/pdf/2208.01321).

**PROZE (Tiwari et al., 2024)**
- **[documented, abstract]** It collects runtime inputs for target methods "across test and field executions" and turns conventional unit tests into parameterised unit tests:
  - 128 target methods
  - 2,287 PUTs generated
  - 217 "provably valid" over the captured inputs

  Source: [arXiv 2407.00768](https://arxiv.org/pdf/2407.00768).

**Test carving (Elbaum, Chin, Dwyer and Jorde, TSE 2009; FSE 2006 precursor)**
- **[documented, abstract and introduction]** It carves differential unit tests from system test executions, capturing the program state that influences a target unit. Results: carved tests "can be as effective as system test cases in terms of fault detection, but much more efficient in the presence of localized changes" — [PDF](https://www.cs.uoregon.edu/events/icse2009/specialSessions/Carving%20and%20Replaying%20Differential%20Unit%20Test%20Cases%20from%20System%20Test%20Cases.pdf).
- [Inferred] It carves from system tests, not production. Pankti is in effect production carving. Carved pre-states are concrete heap values.

**Profiling deployed software (Elbaum and Diep, TSE 2005)**
- **[lead]** It analysed 1,200 user sessions on a 155 KLOC deployed system to assess field-data-driven test-suite improvement and profiling cost — [abstract page](https://plse.cs.washington.edu/daikon/pubs/ElbaumD2005-abstract.html). Full text returned 403 from core.ac.uk.

**Residual test coverage monitoring (Pavlopoulou and Young, ICSE 1999)**
- **[lead, secondary citation]** It proposes monitoring production for execution of code that was not tested — cited in [a multiple case study](https://www.researchgate.net/publication/221494980_Test_coverage_and_post-verification_defects_A_multiple_case_study).

**Productive Coverage (Ivanković et al., Google, ICSE-SEIP 2024)**

All **[documented]**. Source: [author PDF](https://homes.cs.washington.edu/~rjust/publ/productive_coverage_icse_2024.pdf).
- "Google samples all code running in production".
- Each AST node is scored by log2(1 + CPU-seconds), with a 0.01 CPU-second threshold. The score is combined with similarity to well-tested code and used to flag uncovered code during code review.
- RQ2: "Productive coverage leads to a meaningful improvement in test and code quality, despite a strong baseline".
- This is a documented industrial practice of using production execution frequency, not data values, to steer where tests are written.

**Operational-profile testing (Musa)**
- **[documented]** Musa and Ackerman, "Quantifying Software Validation: When to Stop Testing?" (IEEE Software, 1989). Procedure: "select test cases in proportion to the frequencies specified by the operational profile". It introduces "testing compression": selecting tests so that "repetition is limited, thus eliminating redundancies" — [PDF](https://www.rose-hulman.edu/class/csse/csse376/Resources/musa.pdf).
- **[lead]** Musa, "Operational Profiles in Software-Reliability Engineering", IEEE Software 10(2), 1993 — [record](https://www.scilit.net/publications/715ca10803e745574e3f0c6d1814f5c5).

**Daikon**
- **[lead]** Daikon's output "has been used for generating test cases" and for "checking the validity of data streams". Its invariants depend on "the quality and completeness of the test cases" that produce the traces — [Daikon SCP 2007](https://homes.cs.washington.edu/%7emernst/pubs/daikon-tool-scp2007.pdf).
- **[documented]** Tool maintenance: codespecs/daikon, last commit 2026-11-25, permissive MIT-style LICENSE.txt (verified by git clone).
- I found no paper that runs Daikon on production runs specifically, other than Replica-style invariant-violation checks (above).

### Inferences
- **[inferred]** For the brief's setting, two signals are documented to have value:
  - Aggregate frequency of code-path execution (Productive Coverage, operational profiles). It is low disclosure.
  - Field-only behaviour such as invariant violations and call sequences (Wang 2017, Replica). It is medium disclosure.

  Serialised production objects (Pankti, RICK, PROZE, carving) are high utility but transfer values. They fit only if the protected environment generates the tests and only approved derived outputs leave. Equally, the test code itself would need value synthesis before it leaves.
- **[inferred]** Wang 2017's finding that coverage-guided generation does not reproduce field behaviour, together with EvoCrash's 85% versus 33%, suggests that coverage targets alone are a weak proxy for field-relevant behaviour. Richer behavioural signals (invariants, call orders) carry information that coverage does not.

### Gaps
- No field-versus-test comparison was found for data pipelines or SQL workloads.
- I found no Microsoft or Meta reports on production-versus-test coverage.
- The full texts of Elbaum-Diep and Musa 1993 were not read.

## 4. Data-platform specific: using data-quality rule outcomes, rule-firing counts, entity-resolution statistics or query-plan profiles to steer fixture construction

### Takeaway
I found no peer-reviewed study or documented engineering practice that uses the following counts, captured inside, to build fixtures outside:
- data-quality rule hit counts
- reject-reason counts
- entity-resolution decision statistics

This is absence of evidence, not evidence that the approach fails. The closest documented mechanism is query-plan cardinality capture. Hydra (IISc) ships annotated query plans, not tuples, and regenerates a synthetic database that matches operator cardinalities. Its goal is volumetric and performance similarity, which is out of scope here, and it is a lead only.

DCA-oriented anonymisation (PRIEST, PISTIS, kb-anonymity) is the nearest work on relational data for correctness testing. Practitioner material proposes deriving synthetic edge cases from the inventory of data-quality rules [vendor].

### Cited Findings
- **[lead] Hydra (Sanghi, Haritsa et al., VLDB/EDBT)**
  - Client data is not transferred. The client ships the schema, metadata and workload "with their plans", where "each edge is annotated with the associated cardinality of tuples flowing from one operator to the other".
  - The vendor-side database is generated so that output row counts are nearly identical.
  - The summary is "of negligible size and depends only on the query workload and not on the database scale".
  - Sources: search extract of [Hydra VLDB PDF](https://dsl.cds.iisc.ac.in/publications/conference/hydra_vldb.pdf) and [HF-Hydra TR 2021](https://dsl.cds.iisc.ac.in/publications/report/TR/TR-2021-01.pdf).
  - **[unreachable]** Full text: curl connection failed and WebFetch returned 503.
- **[lead]** HF-Hydra (2021 TR) addresses weaknesses of the original, including data "out of sync with the client meta-data" — same search extract.
- **[documented]** PRIEST's program analysis maps database attributes to the branches they control, for example `if (nationality == "Palauan" && age > 60)`. Replacing Nationality with "Human" causes missed paths and exceptions — [PRIEST](https://cdn.sanity.io/files/ku3lep2e/production/b448b278e0967a3a039f49eebe06870146e93839.pdf?dl=).
  - [Inferred] Attribute-to-branch mapping, plus counts of how often each branch fires on real data, is the information a fixture builder would need. PRIEST computes this inside but releases swapped data, not counts.
- **[vendor]** A 2026 practitioner post advises:
  - inventorying rules and defining "the edge cases that actually break them"
  - generating synthetic data "on purpose"
  - scoring rule catch rate
  - storing fixtures alongside the rules
  - refreshing them from new production failures

  No empirical evaluation — [DataMagnet blog](https://www.datamagnet.co/post/synthetic-data-testing-data-quality-rules/).

### Inferences
- **[inferred]** The signals the brief lists map onto mechanisms that are documented elsewhere:
  - Rule hit counts and reject-reason counts correspond to branch or rule firing frequencies (an operational profile at rule granularity).
  - Entity-resolution decision statistics correspond to branch outcomes of matching predicates.
  - Query-plan profiles correspond to Hydra-style cardinalities.

  What carries over: these are aggregate, non-record outputs, comparable in disclosure to Productive Coverage's CPU-seconds. What does not carry over is any evidence of defect-detection value. None of the documented studies measured whether such counts lead to fault-revealing fixtures.
- **[inferred]** Hydra-style cardinality constraints include predicate constants from the workload. Those constants are a disclosure channel, analogous to the path-condition constants in Camouflage and ReMoTe.

### Gaps
- No documented engineering practice, peer-reviewed or industrial blog, was found for steering fixtures from:
  - data-quality rule outcomes
  - entity-resolution match or non-match statistics
  - reject-reason distributions
- Hydra's full text and any functional (correctness) evaluation were not reached.

## 5. Can execution-level capture substitute for an explicit statistical characterisation of the data?

### Takeaway
For one goal there is evidence that execution-level information is enough without any statistical profile: reproducing a known failure. The evidence is Camouflage, Castro, BugRedux and ReMoTe, together with Camouflage's explicit argument that statistics-preserving anonymisation is "not suitable".

The evidence also says which signal level matters:
- Call sequences beat both call stacks (too little information) and complete branch traces (too much).
- Coverage-oriented generation is a poor proxy for field behaviour (EvoCrash 85% versus EvoSuite 33%; Wang 2017).
- Richer behavioural abstractions (temporal invariants) expose gaps that coverage does not.

For detecting unknown defects, no reviewed study compares execution-capture-based fixtures with statistically characterised synthetic data. Whether one can replace the other is an open question. The literature does not show it either way.

### Cited Findings
- **[documented]** Under its determinism assumption, satisfying the failing path condition reproduces the failure by construction. The authors also state that leaking zero information is in general impossible. Statistics-preserving database anonymisation is "not suitable" because failure conditions "are typically very specific" — [Camouflage TR](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf).
- **[documented]** Signal sufficiency for reproduction: POF and call stack were insufficient for 4 of 17 failures, call sequences reproduced 16 of 17, and complete traces mostly failed to synthesise — [BugRedux TR](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2011/git-cercs-11-06.pdf).
- **[documented]** Coverage versus behaviour: tests with ≥75% statement coverage still miss 52.6% of field invariants, and coverage-driven augmentation does not help on mutants or invariants — [Wang et al. 2017](https://people.cs.umass.edu/~brun/pubs/pubs/Wang17icst.pdf).
- **[documented]** Generation targeted at a specific behaviour beats coverage-based generation: 85% versus 33% — [EvoCrash TSE 2018](https://pure.tudelft.nl/ws/files/72125983/08502801.pdf). Replica covers 56% of untested field invariants versus KLEE's 4.7% — [Wang thesis](https://repository.gatech.edu/server/api/core/bitstreams/fbbb8c33-f80f-4852-afda-249c1cb047a4/content).
- **[documented]** Value-level anonymisation of traces, without path awareness, cuts reproduction to 11%–49% success, depending on technique — [Masserini et al. 2024](https://arxiv.org/pdf/2402.07460).
- **[documented]** For DCAs, behaviour-blind k-anonymity or suppression lowers coverage. Behaviour-aware anonymisation keeps it at a higher level — [PRIEST](https://cdn.sanity.io/files/ku3lep2e/production/b448b278e0967a3a039f49eebe06870146e93839.pdf?dl=); [PISTIS](https://www.cs.wm.edu/~denys/pubs/ICST'14-PISTIS-CRC.pdf).
- **[documented]** Observed value domains and limited-valued variables, a form of captured value boundaries, improve symbolic test generation — VASE in the [Wang thesis](https://repository.gatech.edu/server/api/core/bitstreams/fbbb8c33-f80f-4852-afda-249c1cb047a4/content).

### Inferences
- **[inferred]** The evidence supports a layered reading:
  - (i) For reproducing a known failure, path-level or call-sequence capture is sufficient and statistics are unnecessary. This is documented.
  - (ii) For finding untested field behaviour, behavioural abstractions plus guided generation outperform coverage. This is documented on small C and Java programs.
  - (iii) For broad defect exposure in multi-source relational pipelines, there is no evidence either way. Execution capture tells you which paths the real data takes. It does not describe:
    - cross-record or cross-source joint structure (duplicates across sources, identifier collisions, reporting delays) that has not yet triggered a distinct path
    - paths no real record has taken yet

    A statistical characterisation addresses neither of these directly either.
- **[inferred]** Theory versus empirics:
  - Camouflage's reproduction guarantee is a theoretical property under determinism and solver completeness.
  - All effectiveness numbers come from small benchmark sets (17 failures, 170 inputs, 4 C programs, 4 Java systems, 19 Android bugs).
  - No study measures the disclosure of aggregate counts such as branch frequencies.

### Gaps
- No head-to-head study found compares execution-capture-derived fixtures with statistically profiled synthetic data for defect detection.
- No study found measures how much rule-, branch- or ER-decision counts leak about individual records when combined.
- No evaluation found on stateful or incremental processing, where defects depend on the order and timing of arrivals across sources.
