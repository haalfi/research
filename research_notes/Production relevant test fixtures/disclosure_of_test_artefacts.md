# Disclosure from production-derived test artefacts, repeated/interactive releases, testing-specific controls, and licensed reference data vs privacy

Research date: 2026-11-26. Not legal advice.

This file only covers what the earlier notes left out. The earlier notes, `research_notes/Synthetic stand in test data/disclosure_and_licensing.md`, already cover reconstruction from aggregates (Dinur–Nissim, Census 2010/TopDown), DP composition, SDC tools, DP libraries, EDPB/ICO framing, ODbL/SNOMED/exchange market-data licences, and optimiser-statistics leakage. Here they are only referred to, not repeated.

Labels on every claim:
- **[D]** documented: I retrieved the full text and read the cited passage, pulling key passages with text search rather than reading every page.
- **[L]** lead only: search-engine extract or abstract; I did not read the primary text.
- **[U]** unreachable: I tried the primary source and could not retrieve it.
- **[I]** inference by this researcher (engineering inference unless stated otherwise).
- **[V]** vendor or rights-holder claim.

Evidence types are also tagged where useful: *theoretical result*, *empirical finding*, *documented practice*.

---

## 1. What test artefacts reveal about the underlying records (path conditions, coverage, failing inputs, minimised fixtures, traces, logs, crash reports, query plans, rule-hit counts)

### Takeaway
The only artefacts with *measured* leakage are failure-reproducing inputs derived from real inputs (Castro et al. 2008; Clause & Orso 2009–2011) and crash reports (Scrash 2003; WER 2009; the Satvat & Saxena browser crash-report study 2018).
- Even inputs made with path-condition-preserving anonymisation still revealed on average about 30% of the original input's bits, with about 30% of the input left unchanged ("residue"). The range across subjects was 2.3–76.5%.
- Real crash-report corpora contained passwords, session tokens and email addresses in the thousands.
- Coverage vectors, mutation-kill matrices, assertion messages, query plans with actual row counts and rule-hit counts have **no dedicated disclosure measurements** that I could find. Their leakage follows from the documented results by inference. Each one is a function of the execution path or a counting query, so each is bounded above by what the path or count reveals, but none of them is zero.

### Cited Findings

**Path conditions in bug reports: the bits-revealed metric (Castro, Costa & Martin, ASPLOS 2008)**
- **[U]** I could not read the ASPLOS 2008 paper (DOI 10.1145/1346281.1346322):
  - The EPFL copy now redirects (301) to epfl-lara.github.io.
  - The research.microsoft.com URL returns HTML.
  - Semantic Scholar marks it "CLOSED".
  — [MSR publication page](https://www.microsoft.com/en-us/research/publication/better-bug-reporting-with-better-privacy/)
- **[L]** Search extracts of the paper say:
  - it generates new inputs that follow the same execution path to the failure but are otherwise unrelated to the original;
  - its Microsoft Word example reveals only 0.2% of the original document's bits;
  - if a fraction α of same-size inputs satisfy the path conditions, the report reveals −log2(α) bits;
  - "reproducing bugs while revealing almost no private information".
  Per-application numbers were not verified.
- **[D]** *Theoretical metric.* The authors' own patent (US 8,122,436 B2, "Privacy enhanced error reports"; inventors Costa, Castro, Martin; Microsoft; priority 2007-11-16, published 2012-02-21) states:
  - "if a fraction [α] of the byte strings having the same size as the original input satisfy the conditions, the error report reveals −log2([α]) bits about the original input".
  - If the set contains only the original byte string, "the report reveals all the information about the original input".
  - "a lower bound on [α] is an upper bound on the number of revealed bits". The system computes "an upper bound on the number of bits that are revealed" overall and per input byte, "to provide the user with additional information".
  - The user "may then be given the option to send the report to the vendor or not".
  — [Google Patents US8122436B2](https://patents.google.com/patent/US8122436B2/en)
- **[D]** Clause's thesis describes the Castro approach: dynamic symbolic execution along the failing path gives path condition φ, and a solver picks another satisfying input. "because it may not be possible to remove all sensitive information, users are typically given an opportunity to inspect I′ before it is sent to developers." — [Clause, *Enabling and Supporting the Debugging of Software Failures*, PhD thesis, Georgia Tech, May 2011, §4 (p. 49)](https://repository.gatech.edu/server/api/core/bitstreams/c1cdccd9-cb7c-42c9-abf1-3e390dd74618/content)

**Residual information after path-preserving anonymisation (Clause & Orso: CERCS TR 2009; ICSE 2011 "Camouflage")**
- **[U]** The ICSE 2011 paper PDF on cc.gatech.edu returned HTML (a moved or removed page). Its contents are taken from the May 2011 thesis chapter and the 2009 tech report, which present the same study. — [ICSE 2011 listing](https://2011.icse-conferences.org/content/camouflage-automated-anonymization-field-data.html)
- **[D]** *Empirical finding.* Study design and metrics:
  - The study used "170 failure-inducing inputs" from NanoXML, printtokens, Columba's address book and htmlparser.
  - Two metrics:
    - "bits of information revealed", where an input reveals Σ|log2(xi)| bits, with xi the number of solutions for input element i;
    - "residue", "essentially the number of inputs that remain unchanged after anonymization".
  - Residue is needed because the bits metric "fails to indicate that half of the input is unchanged".
  — [Clause thesis, May 2011, §4.4.4](https://repository.gatech.edu/server/api/core/bitstreams/c1cdccd9-cb7c-42c9-abf1-3e390dd74618/content); [Clause & Orso, "Automated Sanitization of Field Data", GT-CERCS-09-14, 2009](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf)
- **[D]** *Empirical finding.* Results:
  - "the average percentage of bits of information revealed ranges from 2.3% to 76.5%, with an average of 30.6%, and the average percentage of residue ranges from 1.5% to 65%, with an average of 30%."
  - "these results confirm that it is generally impossible to generate fully anonymized inputs".
  - Strength "can vary widely even among different inputs that trigger the same fault".
  - Example of the bits metric: when solutions for 5 characters grow from 10 to 200, revealed information drops "from 63.3 bits to 41.7 bits".
  — [Clause thesis 2011](https://repository.gatech.edu/server/api/core/bitstreams/c1cdccd9-cb7c-42c9-abf1-3e390dd74618/content); [CERCS TR 2009](https://cercs.gatech.edu/www.cercs.gatech.edu/tech-reports/tr2009/git-cercs-09-14.pdf)
- **[D]** Sensitivity was judged only by the author's manual inspection: "For all 170 anonymized inputs, I found that they did not reveal any information that I believe to be sensitive". The judgement is qualitative and author-made. — [Clause thesis 2011, §4.4.5](https://repository.gatech.edu/server/api/core/bitstreams/c1cdccd9-cb7c-42c9-abf1-3e390dd74618/content)
- **[D]** Comparison with a re-implementation of the Castro approach (in Java on JPF, because "their implementation … is not publicly available"): across 20 faults, Camouflage's inputs "revealed 30% less bits of information and contained 40% less residue", "With the caveat of a potential implementation bias". — [Clause thesis 2011, §4.4.6](https://repository.gatech.edu/server/api/core/bitstreams/c1cdccd9-cb7c-42c9-abf1-3e390dd74618/content)

**kb-anonymity and kbe-anonymity (Budi, Lo, Jiang & Lucia)**
- **[L]** Venue correction: kb-anonymity was published at **PLDI 2011** (pp. 447–457, DOI 10.1145/1993498.1993551), not ICSE 2011 as the brief says. The model combines k-anonymity with a requirement that replaced data exhibit "the same kind of program behavior" as the original, because "simply masking sensitive values alone may not be sufficient, as the correlation among fields in the data can reveal the masked information". — [SMU InK record](https://ink.library.smu.edu.sg/sis_research/1390); [BibSLEIGH](https://bibtex.github.io/PLDI-2011-BudiLJL.html). Full text **[U]**: Semantic Scholar marks it closed and the SMU page gave no PDF link.
- **[L]** The "Lucia et al. 2012" item is **kbe-anonymity: Test Data Anonymization for Evolving Programs** (ASE 2012). Its abstract says that if kb-anonymity "is repeatedly applied for evolving programs a privacy risk emerges", which kbe-anonymity addresses. This is a *repeated-release* problem specific to test data. — [SMU InK 1572](https://ink.library.smu.edu.sg/sis_research/1572). Full text **[U]**.
- **[D]** A secondary description from a 2024 paper: kb-anonymity "exploits symbolic execution and k-anonymity to generate anonymized database tuples that do not alter the behavior of the program … The approach is limited to numbers and programs whose code is accessible and analyzable with symbolic execution". — [Masserini et al., "Anonymizing Test Data in Android: Does It Hurt?", AST 2024, arXiv:2402.07460](https://arxiv.org/abs/2402.07460)

**Privacy vs test coverage (Grechanik, Csallner, Fu & Xie, ISSRE 2010)**
- **[D]** *Empirical finding.*
  - "a popular data anonymization algorithm called k–anonymity seriously degrades test coverage of DCAs [database-centric applications]".
  - "for k ≤ 6 it is possible to retain a higher test coverage with our approach [program-analysis-guided selective k-anonymity] than with … Datafly".
  - "for k ≥ 7, test coverage drops to less than 30% from the original coverage of more than 70%".
  - Their motivation: testing of DCAs is outsourced, and "test centers report worse code coverage and fewer uncovered bugs" with fake data.
  — [Grechanik et al., "Is Data Privacy Always Good For Software Testing?", ISSRE 2010 (author PDF)](https://ranger.uta.edu/~csallner/papers/grechanik10is.pdf)
- **[I]** This is the inverse of the disclosure question. Coverage depends on the real values. So a coverage vector computed on real data carries information that k-anonymisation destroys, and that information is about the records.

**Failure reproducibility vs anonymisation of field inputs (Masserini et al., AST 2024)**
- **[D]** *Empirical finding.* The study covers 19 bugs in 17 Android apps and five techniques: Local Suppression, Special-Char-Driven (SCD) Local Suppression, Global Recoding, Rounding and Noise Addition. Results:
  - String Local Suppression had a reproduction success of 11–19%.
  - SCD Local Suppression had a mean of 49%. It works "by just disclosing a syntactic information … (i.e., the presence of a special character)".
  - Numeric Local Suppression reached 41%. Perturbing or approximating techniques reached "up to 63% … at the cost of disclosing some information about the original value".
  - String Local Suppression needed "close to 60" generate-and-run attempts on average, and up to 299, for 95% reproduction probability.
  — [arXiv:2402.07460v1, 12 Feb 2024](https://arxiv.org/abs/2402.07460)
- **[I]** This is a documented privacy–reproducibility trade-off curve. Each extra retained attribute of the real input (special-char presence, interval, rounded value) is disclosure bought for reproducibility.

**Crash reports, core files and stack traces**
- **[D]** *Documented design + empirical finding.* Scrash (USENIX Security 2003) on what it covers:
  - Crash reports contain "part or all of the call stack, processor registers, and heap contents".
  - Scrash moves `$sensitive`-annotated data (plus CQual-inferred flows) into a separate region that is erased before the core file is sent.
  - It explicitly does **not** handle control-flow leakage: "the program counter and call stack can leak information on the state of sensitive variables". In its example, if branch b executed, "an adversary can infer that the password does not start with a lower case letter". The paper says "Eliminating control flow privacy leaks … while retaining enough information for debugging is difficult, so Scrash ignores such vulnerabilities", and that registers and "even the entire call stack" would be unavailable in a system that guarded against it.
- **[D]** Scrash measurements: type inference marked 24% (gnomecal), 10% (J-Pilot) and 59% (ssh) of stack variables as possibly sensitive.
  — [Broadwell, Harren & Sastry, "Scrash: A System for Generating Secure Crash Information", USENIX Security 2003](https://www.usenix.org/legacy/events/sec03/tech/full_papers/broadwell/broadwell.pdf)
- **[D]** *Documented practice (Microsoft WER, SOSP 2009).*
  - WER "zeros serial numbers and other known unique identifiers".
  - It is opt-in, "All consent requests default to negative".
  - "Because WER does not have sufficient metadata to locate and filter possible PII from collected stack or heap data, we minimize the collection of heap data and apply company data-access policies that restrict the use of WER data strictly to debugging".
  - Minidumps contain "registers from each processor, the stack of each thread".
  So WER manages residual PII through minimisation and access policy, not filtering.
  — [Glerum et al., "Debugging in the (Very) Large: Ten Years of Implementation and Experience", SOSP 2009](https://www.sigops.org/s/conferences/sosp/2009/papers/glerum-sosp09.pdf)
- **[D]** *Empirical finding.*
  - Mining "2.5 million partially anonymized crash reports" released by a major browser over six years found "more than 20,000 sessions and token IDs, 600 passwords, 9,000 email addresses" (9,139 emails in §4) "and an enormous amount of contact information", mostly via URL and free-text description fields.
  - The proposed client-side keyword masking was 100% successful on 500 URLs and 500 descriptions tested, with URL "readability" (crash still replicable) over 92%.
  — [Satvat & Saxena, "Crashing Privacy: An Autopsy of a Web Browser's Leaked Crash Reports", arXiv:1808.01718, 6 Aug 2018](https://arxiv.org/abs/1808.01718)

**Logs and error logs (documented practice in a TRE)**
- **[D]** OpenSAFELY:
  - Job outputs and logs "are only visible via Airlock in the secure environment to avoid disclosure of potentially sensitive information".
  - "log files that reveal information about the underlying data, should also be checked and redacted if necessary. It is very unlikely that outputs such as log files should be required for publication outside the secure environment".
  - Error logs "should only be requested for output in exceptional circumstances … you must minimise any data required: make a copy of the log file and delete all data items that are not necessary".
  — [OpenSAFELY docs: jobs-site.md; outputs/sdc.md; outputs/requesting-file-release.md (repo HEAD 2026-11-25)](https://raw.githubusercontent.com/opensafely/documentation/main/docs/outputs/requesting-file-release.md)

**Telemetry / counters**
- **[D]** *Theoretical + deployed.*
  - Per-round LDP "degrade[s] rapidly when telemetry is collected regularly". T independent ε-LDP reports give indistinguishability "by a factor of up to e^{Tε}".
  - The fix is 1-bit mechanisms plus α-point rounding plus memoisation plus output perturbation. It was "deployed by Microsoft … starting with Windows Insiders in Windows 10 Fall Creators Update".
  — [Ding, Kulkarni & Yekhanin, "Collecting Telemetry Data Privately", NeurIPS 2017, arXiv:1712.01524](https://arxiv.org/abs/1712.01524)
- **[D]** RAPPOR (Google, Chrome; CCS 2014):
  - Memoisation ("Permanent randomized response") allows "ln(3)-differential privacy even with an infinite number of responses".
  - Without it, "if 75 out of 100 responses are 'Yes' … the true answer will have been 'No' in a vanishingly unlikely 1.39 × 10⁻²⁴ fraction of cases".
  - Memoisation protects longitudinally "only in cases when the underlying true value does not change or changes in an uncorrelated fashion".
  — [Erlingsson, Pihur & Korolova, arXiv:1407.6981](https://arxiv.org/abs/1407.6981)

**Query plans with actual row counts**
- **[D]** *Documented behaviour.* PostgreSQL `EXPLAIN ANALYZE` prints, per plan node:
  - actual row counts (e.g. "actual time=0.030..1.995 rows=7000.00 loops=1");
  - "Rows Removed by Filter: 3000";
  - hash "Buckets … Memory Usage", "Sort Method … Memory";
  - the filter predicate itself (e.g. "Filter: (ten < 7)").
  — [PostgreSQL 19 docs, "Using EXPLAIN" §14.1 (Nov 2026)](https://www.postgresql.org/docs/current/using-explain.html)
- **[I]** Each plan node's actual row count is the exact answer to a counting query: the predicate conjunction at that node over real data. A plan exported from the protected environment is therefore a bundle of exact counts, plus any literal values used in predicates. It belongs with the aggregate exports in the earlier notes (Dinur–Nissim budget) and should not be treated as "metadata".

### Inferences
- **[I] A general bound.** For any artefact that is a deterministic function f of the execution on a real record r, the artefact reveals no more about r than the full execution trace does (data-processing inequality). This covers branch-coverage vectors, the set of covered statements, which assertion failed, the exception type and stack frames.
  - Castro's −log2(α) is the bound for the full path condition. A coverage *set* is a coarsening of the path, so it reveals at most that much, and often far less. Loop counts and branch order are lost.
  - Even one bit can be decisive when the predicate is sensitive or rare, for example `if diagnosis == X` or `if income > 1e6`. Scrash's password example shows this. No paper I found measures coverage-vector leakage directly. This is absence of evidence, not evidence of safety.
- **[I] Mutation-kill matrix.** Entry (mutant m, test t) is a 1-bit function of real record r: does mutant m's output differ from the original's on r? A matrix of M mutants × N real-record tests releases up to M·N adaptively chosen bits. Mutants on predicates such as `x < c` → `x <= c` reveal whether a real value equals the boundary constant exactly. This is a classic reconstruction channel: every boundary mutant is a threshold query. [I] from Castro's bit-counting and Dinur–Nissim (earlier notes).
- **[I] Assertion messages and logs.** Frameworks commonly render both sides of a failed equality, for example JUnit-style "expected:<…> but was:<…>" (general knowledge, not verified this session). These render the real value from the protected record verbatim. Like Satvat & Saxena's free-text fields, they are a primary disclosure, not an inferential one. OpenSAFELY's rule (keep logs inside, minimise before release) is the documented practice.
- **[I] Minimised failing fixture derived from a real record** (for example ddmin-style reduction):
  - (a) *Membership / existence:* the fixture's existence proves at least one production record has the failure-triggering property. If that property is unique (say a rare code combination or an outlier date), it singles out a record.
  - (b) *Attribute disclosure:* minimisation keeps exactly the failure-relevant values, the "residue". Clause & Orso measured residue averaging 30% even after deliberate anonymisation, so plain minimisation without anonymisation keeps all of the triggering values.
  - (c) *Linkage:* in a multi-source platform, a residue of identifier-like fields (source ID, LEI, date pairs) can be linked back through another source that describes the same entity.
  Mitigation patterns with evidence behind them: regenerate through the path condition (Castro/Camouflage); retain only syntactic features (Masserini SCD); release only after output checking (OpenSAFELY). None gives a formal bound against an adversary with auxiliary knowledge.
- **[I] Rule-hit counts and failing-input signatures** (for example counts of records failing each validation rule, per source, per day) are counting queries over real data. Small counts are small cells. Successive counts difference to single records. The output-checking thresholds and rounding in §3 apply directly.

### Gaps
- Castro et al.'s per-application numbers are lead only; the full text was unreachable. The bits metric itself is documented via the patent.
- The full texts of kb-anonymity (PLDI 2011) and kbe-anonymity (ASE 2012) were unreachable, so I have no measured numbers for them.
- I found no peer-reviewed measurement of disclosure from branch-coverage vectors, mutation-kill matrices, EXPLAIN ANALYZE output or assertion messages. These rest on inference.
- I found no study of membership inference specifically on minimised failing examples (delta debugging).

---

## 2. Repeated and interactive releases: auditing, trackers, verification servers, pass/fail oracles, controls

### Takeaway
- When tests run inside the protected environment and only pass/fail, counts or messages come out, the outside developer is an *interactive query analyst*. Each test run is a query, and each pass/fail is one bit.
- The statistical-database literature shows that adaptive queries defeat naive restriction. Query-set-size control is defeated by trackers. Auditing is hard, and refusals themselves leak, which is why "simulatable auditing" exists. These classic results are lead only in this session; the full texts were unreachable.
- The closest *documented* analogues are verification servers and ML leaderboards:
  - Barrientos/Reiter 2017–18 and Lin & Reiter 2024 state that "verification measures leak information about the confidential data" and use DP with a finite budget.
  - Blum & Hardt 2015 document that leaderboard scores leak holdout labels to adaptive submitters, and that Kaggle's heuristic controls (rate limits, rounding of scores) degrade as √k in the number of submissions. Their Ladder mechanism grows only as (log k)^{1/3}.
- NIST SP 800-188 (Sept 2023) gives agency-level guidance: interactive query interfaces need DP or staff review, plus logging of queries and results.

### Cited Findings
- **[L]/[U]** Kenthapadi, Mishra & Nissim, "Simulatable Auditing", PODS 2005, pp. 118–127, DOI 10.1145/1065167.1065183. The abstract (search extract) says offline auditing "cannot be directly used to solve the online auditing problem since query denials may leak information". The paper proposes a model where denials are decided using only past queries and answers, so they provably leak nothing, and gives auditors for sum and max queries and a probabilistic partial-compromise notion for sums. — [DBLP/Georgetown bibliography entry](https://seclab.cs.georgetown.edu/bibliography/DBLP_conf/pods/KenthapadiMN05.html). Full text unreachable (the Stanford author URL was gone).
- **[D]** The refusal-leaks point is confirmed in a read text: auditing must watch for differencing pairs, but "refusing to answer a query is itself disclosive". — Dwork & Roth 2014, as recorded in the earlier notes file.
- **[U]** Denning's tracker paper ("The Tracker: A Threat to Statistical Database Security", TODS 1979) and Dobkin, Jones & Lipton ("Secure Databases: Protection Against User Influence", TODS 4(1), 1979, DOI 10.1145/320064.320068) were not retrieved. The ACM DL returned HTML. Semantic Scholar lists Dobkin et al. as BRONZE open access at the ACM DL. — [Semantic Scholar record via API](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/320064.320068). **[I]** from general knowledge, not verified this session: a tracker pads a small target query set with a known general set, so query-set-size restriction alone does not prevent disclosure. Dobkin et al. bound how many queries are needed to compromise a value under overlap restrictions.
- **[D]** *Verification servers (documented practice + method).*
  - "Verification servers provide an automated means to provide … feedback" on synthetic-data analyses.
  - "the agency must account for a crucial fact: verification measures leak information about the confidential data (Reiter et al., 2009; McClure and Reiter, 2012). Clever data snoopers could submit queries that, perhaps in combination with other information, allow them to estimate confidential values too accurately."
  - Their remedy: make verification measures ε-DP so "we can quantify and track the total privacy leakage".
  - "If one follows ε-DP strictly, at some point the total privacy budget … will be exhausted, at which point no new analysis results may be released. With a finite budget, one has to decide who gets access … These raise complicated issues of fairness … which have yet to be addressed in production settings."
  - Applied to US OPM federal employee data.
  — [Barrientos et al., "A Framework for Sharing Confidential Research Data, Applied to Investigating Differential Pay by Race in the U.S. Government", NBER WP 23534, June 2017 (later Annals of Applied Statistics 2018 per search extract [L])](https://www.nber.org/papers/w23534.pdf)
- **[D]** Lin & Reiter: verification measures "leak information about the confidential records, so that agencies may wish to apply disclosure control methods to the released verification measures". They present a DP verification measure for survey-weighted estimates. — [Lin & Reiter, "Differentially Private Verification of Survey-Weighted Estimates", arXiv:2404.02519v1, 3 Apr 2024](https://arxiv.org/abs/2404.02519). This is the "Lin & Reiter verification server" named in the brief.
- **[L]** Remote analysis systems: O'Keefe & Chipperfield summarise "known attack methods on remote analysis system outputs, focussing on exploratory data analysis and linear regression" and the matching protective measures. — [O'Keefe & Chipperfield, *International Statistical Review* 81(3):426–455, 2013 (RePEc abstract)](https://ideas.repec.org/a/bla/istatr/v81y2013i3p426-455.html). Full text **[U]**: the core.ac.uk link returned HTML.
- **[D]** *Adaptive oracle leakage: the leaderboard analogue.*
  - "any submission might incorporate statistical information about the withheld class labels that was revealed by the score of previous submissions".
  - "To mitigate this problem Kaggle primarily restricts the rate of re-submission and to some extent the numerical precision of the released scores".
  - These are "poorly understood heuristics such as limiting the bit precision of answers and the rate of re-submission".
  - Under their attack, Kaggle-style error "scales with the number of submissions as √k". Ladder's error is O((log k / n)^{1/3}), with a lower bound of Ω((log k / n)^{1/2}).
  — [Blum & Hardt, "The Ladder: A Reliable Leaderboard for Machine Learning Competitions", arXiv:1502.04585, Feb 2015 (ICML 2015)](https://arxiv.org/abs/1502.04585)
- **[D]** Reusing a holdout "adaptively multiple times can easily lead to overfitting to the holdout set itself". The paper gives an algorithm (Thresholdout, DP-based) that "enables the validation of a large number of adaptively chosen hypotheses, while provably avoiding overfitting". — [Dwork, Feldman, Hardt, Pitassi, Reingold & Roth, "Generalization in Adaptive Data Analysis and Holdout Reuse", arXiv:1506.02629v2, Sep 2015 (NeurIPS 2015)](https://arxiv.org/abs/1506.02629)
- **[D]** *Interactive DP SQL with a fixed budget.* PrivateSQL "ensures a fixed privacy loss across all the queries posed by the analyst by answering queries on private synopses generated from several views", with policies that let "the data owner … flexibly specify entities in the schema that need privacy" (for example person vs household), across foreign keys. On "a workload of more than 3,600 queries … for 50% of the queries PrivateSQL offers at least 1,000× better error rates than solutions adapted from prior work". — [Kotsogiannis et al., PVLDB 12(11):1371–1384, 2019](https://www.vldb.org/pvldb/vol12/p1371-kotsogiannis.pdf)
- **[D]** *NIST SP 800-188 (September 2023, approved 2023-09-07), §4.5 Interactive Query Interface.*
  - Results on actual data can be noised (possibly DP), or "individual queries can be reviewed by agency staff".
  - Queries can run on synthetic data, with the agency warning if results "deviate significantly from the queries run on the actual data (ensuring that the warning itself does not compromise the privacy of some individual)".
  - "A significant privacy risk with interactive queries is that each query results in additional privacy loss … the query interface alone will not protect privacy".
  - Query interfaces should "log both queries and query results in order to deter and detect malicious use".
  - With a finite budget the controller must add noise, accept risk, or cease answering.
  - Synthetic data lets the budget "be spent on creating the synthetic dataset rather than on responding to interactive queries".
  — [NIST SP 800-188](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf)
- **[D]** *Repeated-release practice in a TRE (OpenSAFELY).*
  - "When producing repeated reports … a small change … (N to N+1) … should be routinely avoided … use rounding across the entire report (to the nearest 5, 7, or 10). Rounding eliminates the need for output checkers to compare different versions".
  - After adding a code to a codelist, re-running "may result in small changes … that can be disclosive, ie, <=7 individuals have the new code … you may need to wait until there has been enough change in the underlying study population".
  - "If you are likely to release data multiple times … use rounding … and/or a threshold substantially higher than 5".
  — [OpenSAFELY docs, outputs/sdc.md (HEAD 2026-11-25)](https://raw.githubusercontent.com/opensafely/documentation/main/docs/outputs/sdc.md)
- **[D]** Repeated anonymisation for evolving code is itself a named risk (kbe-anonymity abstract, §1, [L]). For telemetry, memoisation is the documented fix for repeated collection (Ding et al.; RAPPOR, §1, [D]).

### Inferences
- **[I] Pass/fail oracle = adaptive bit queries.** If an outside developer can submit arbitrary test code (or test parameters) to run against real data and see pass/fail:
  - One test `assert record[i].salary < c` is one threshold query, so binary search recovers a value in about log2(range) runs.
  - A test that loops over all records and fails iff any record satisfies P is an existence query on P.
  This is "differencing via code submission" in the limit: unrestricted code makes each run a fully expressive query. Rate limits and coarse outputs slow this down but do not bound it (Blum & Hardt's √k result for rounding plus rate limits is the closest documented quantification).
- **[I] Control hierarchy**, from documented analogues to the brief's setting:
  - (1) *Restrict what code runs.* Run only reviewed, versioned test suites (OpenSAFELY runs only committed code from GitHub). Do not allow ad hoc assertions.
  - (2) *Restrict what leaves.* Aggregate pass/fail per suite, round counts, suppress small cells, and hold back raw messages, logs and stack traces (OpenSAFELY Level 4 / Airlock).
  - (3) *Human output checking* of anything else, with logs of queries and results (NIST 800-188; OpenSAFELY dual independent checking).
  - (4) *Formal accounting* where the volume is high. Use DP on released counts (PrivateSQL-style fixed budget, entity-level privacy unit), or Ladder/Thresholdout-style mechanisms that release a result only when it changes materially. These turn the √k degradation into roughly log k. Budget exhaustion and fair allocation are acknowledged as unsolved in production (Barrientos et al.).
- **[I]** Simulatable auditing's lesson applies to automated gates: a gate that refuses to release a test result *because* the result would be disclosive leaks through the refusal. Gating decisions must depend only on the query (test code, past releases), not on the real outcome. Alternatively, use a randomised gate.
- **[I]** In the multi-source setting, reporting delays act as natural differencing. A re-run after one source's late batch arrives isolates that batch's records. OpenSAFELY's "wait until there has been enough change" and "round across the entire report" are the documented counter-patterns.

### Gaps
- I did not read the full texts of Denning 1979, Dobkin–Jones–Lipton 1979, Kenthapadi–Mishra–Nissim 2005, O'Keefe & Chipperfield 2013, or McClure & Reiter 2012 (the verification-server attack paper).
- I found no paper on "differentially private software testing" or DP on test pass/fail outcomes as such. The closest analogues are Ladder/Thresholdout (ML holdouts) and DP verification servers. This is absence of evidence. A dedicated search for "DP debugging" did not happen this session.
- Software-analytics privacy (Peters & Menzies MORPH/LACE2, ICSE 2012/2015) is lead only. Search extracts say a 2024 EMSE replication found privacy scores of 89–99% "at the cost of decreased performance". — [Malik, Adams & Hassan, EMSE 2024 (not read)](https://mcis.cs.queensu.ca/publications/2024/emse_akshat_within.pdf); [LACE2 page](https://llayman.github.io/publications/peters-2015/). These target sharing defect *datasets*, not test outcomes.

---

## 3. Established methods bounding disclosure in software testing (test data anonymisation, standards, Five Safes, OpenSAFELY output checking)

### Takeaway
- *Formal-ish methods specific to test data* exist only as research prototypes with empirical, not formal, bounds: Castro's path-condition regeneration, Camouflage, kb/kbe-anonymity, MultiPathPrivacy/RESPA.
- *Standards* treat test data generically:
  - NIST SP 800-188 (2023) distinguishes "test data" and "realistic test data". Realistic test data is safe only if "not developed using confidential data or a model based on the confidential data". It warns that data-masking tools give "minimal privacy protection" and should not be "the sole mechanism to ensure confidentiality in non-public data sharing".
  - ISO/IEC 20889:2018 (de-identification terminology and techniques) could not be read.
- The *documented operational model* that fits "run inside, approved derivatives leave" is the Five Safes plus TRE output checking. OpenSAFELY is the clearest instance: code developed on dummy data outside and run only inside; all outputs and logs kept in the secure zone; two trained checkers per release; counts ≤7 redacted then rounded to 5.

### Cited Findings
- **[D]** NIST SP 800-188, Table 3 and §4.4.2–4.4.3:
  - "Test data … resemble the original dataset in terms of structure and the range of values but … there is no attempt to ensure that inferences drawn on the test data will be like those drawn on the original data. Test data may also include extreme values that are not in the original data but are present for testing software".
  - Names should be "conspicuously non-natural", for example "FIRSTNAME1 LASTNAME2".
  - "Provided that the realistic test data are not developed using confidential data or a model based on the confidential data, realistic test data will not compromise the content of confidential data".
  — [NIST SP 800-188, Garfinkel, Near, Dajani, Singer & Guttman, Sept 2023](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf)
- **[D]** NIST SP 800-188 §5.2.3, Data Masking Tools: masking tools "can remove or replace designated fields … while maintaining relationships between tables … but generally cannot identify or modify quasi-identifiers in a manner consistent with a privacy policy or risk analysis. Data masking tools were developed to allow software developers and testers access to datasets that contain realistic test data while providing minimal privacy protection. Absent additional controls or data manipulations, data masking tools should not be used for the de-identification of datasets that are intended for public release nor as the sole mechanism to ensure confidentiality in non-public data sharing." — [NIST SP 800-188](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf)
- **[D]** NIST SP 800-188 §3.5 recommends a repeatable methodology "such as The Five Safes". It defines a "data access system" broadly, as "any mechanism that allows outsiders to gain access to the agency's confidential data". The five dimensions are Safe projects, people, data, settings and outputs ("Are the statistical results non-disclosive?"). The reviews of each dimension "are independent of the others". — [NIST SP 800-188](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf)
- **[D]** SP 800-188 references ISO/IEC 20889:2018 ("Privacy enhancing data de-identification terminology and classification of techniques", title partly from the reference list and partly **[I]**) and ISO/IEC 27559:2022 (de-identification framework). — [NIST SP 800-188 references](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf). **[U]** iso.org/standard/69373.html returned a Cloudflare challenge, and the standard is paywalled. Its content is not verified here.
- **[D]** *OpenSAFELY workflow (documented practice; docs repo HEAD 2026-11-25).*
  - Researchers "write and test their ehrQL and analytical code … in Github before it is run in the Secure Zone … The code can be tested and perfected/improved on a dummy dataset."
  - "Each job will either succeed or fail. In either case, the output and log files are only visible via Airlock in the secure environment".
  - Level 4 holds aggregated outputs and "the automatically created log files of each action/script … for debugging purposes".
  - "No files are released from the secure environment without undergoing dual independent checking by trained output-checkers".
  — [how-opensafely-works.md](https://raw.githubusercontent.com/opensafely/documentation/main/docs/how-opensafely-works.md); [jobs-site.md](https://raw.githubusercontent.com/opensafely/documentation/main/docs/jobs-site.md); [security-levels.md](https://raw.githubusercontent.com/opensafely/documentation/main/docs/security-levels.md)
- **[D]** *OpenSAFELY SDC rules.*
  - "any statistic describing 7 or fewer patients, either directly or indirectly, should be redacted"; then "round to the nearest 5".
  - The reason for 7: the earlier rule of redacting ≤5 combined with rounding to 5 "led to occassions where counts of 5 could be inferred to be either 6 or 7".
  - Max/min values "often relate to one or two individuals … and so should be avoided".
  - Zero or 100% counts "can be disclosive".
  - Midpoint-6 rounding is used for rates.
  - About 25% of rejected outputs are rejected for insufficient context.
  — [outputs/sdc.md](https://raw.githubusercontent.com/opensafely/documentation/main/docs/outputs/sdc.md); [outputs/output-checking.md](https://raw.githubusercontent.com/opensafely/documentation/main/docs/outputs/output-checking.md)
- **[D]** *Research methods with empirical evaluation:*
  - Castro et al. bits metric (patent, §1);
  - Camouflage: 30.6% average bits revealed, 30% residue, n=170 (§1);
  - Masserini et al.: five SDC techniques applied to failure inputs (§1);
  - Grechanik et al.: k-anonymity vs coverage (§1).
  Masserini et al. also list "MultiPathPrivacy [11] and RESPA [12]", which "weaken the requirement about preserving the same execution path". — [arXiv:2402.07460](https://arxiv.org/abs/2402.07460) (MultiPathPrivacy and RESPA themselves not read [L]).
- **[D]** Earlier notes (not repeated here) cover SDC tools, SACRO/ACRO output checking, and statbarns.

### Inferences
- **[I] Classification of methods by guarantee:**
  - (a) *Formal* (DP): available for counts and verification measures (PrivateSQL, Barrientos/Lin–Reiter, Ding/RAPPOR). Not available for individual failing fixtures. A single real record cannot be released with DP; only a DP-generated stand-in can.
  - (b) *Information-theoretic but non-adversarial*: the Castro bits bound measures the solution-space size given the path condition, assuming a uniform prior. It does not bound an adversary with auxiliary knowledge, which my reading of the patent text supports.
  - (c) *Syntactic* (k-anonymity, kb-anonymity): no composition across releases. kbe-anonymity exists precisely because of re-release.
  - (d) *Procedural* (Five Safes, output checking): human judgement, rule-of-thumb thresholds, logged decisions.
  For the brief, (d) is the backbone. (a) applies to aggregate test metrics. (b)/(c) apply to the rare case where a real failing record must be turned into a fixture.
- **[I] Fit to the brief.** OpenSAFELY is a documented instance of "development outside on dummy data, execution inside, approved derivatives out". Test suites map onto it as follows:
  - pass/fail per test is a Level-4 output;
  - logs and stack traces stay in Airlock;
  - fixtures derived from real failures are exceptional releases that need minimisation, path-condition regeneration or syntactic abstraction, plus dual checking.
- **[I]** NIST 800-188's caution that masking tools give "minimal privacy protection" undercuts a common practice: copying production to test via masking, then treating the copy as non-sensitive. Under the earlier notes' EDPB framing, masked copies are pseudonymised personal data.

### Gaps
- ISO/IEC 20889:2018 and ISO/IEC 27559:2022 texts are unreachable (paywalled / Cloudflare).
- The Five Safes primary texts (Desai, Ritchie & Welpton 2016) were not read; SP 800-188's summary is used instead.
- I found no standard that specifically addresses test artefacts (coverage, logs, traces) as disclosure outputs. OpenSAFELY's treatment of logs is the closest documented practice.

---

## 4. Licensed reference data vs privacy: test use, fixtures from licensed codes, exporting minimised fixtures

### Takeaway
- Licence and database-right constraints are about **extraction, copying and re-utilisation of content**, judged by *substantial part*, by *repeated and systematic extraction of insubstantial parts* (Art. 7(5)), and by contract terms. Privacy constraints are about **identifiability**. The two are independent.
- A fixture can be fully anonymous and still breach a licence, for example by copying PAF addresses or ICD-11 content without codes and URIs. A fixture can also be licence-clean and still disclosive.
- Several common reference sets are open:
  - GLEIF LEI data is CC0;
  - FIGI identifiers are dedicated to the public domain by Bloomberg;
  - ISO 4217 lists are published "free of charge" by SIX;
  - ICD-11 is CC BY-ND 3.0 IGO, with WHO conditions.
- Others restrict copying with explicit test carve-outs. Royal Mail PAF allows copies "reasonably necessary for back-up, security, business continuity and system testing purposes" but requires a data supply agreement, caps trial responses, and bans Data Extraction in some contexts.
- Test/dev-specific clauses for LSEG, S&P, D&B, Deutsche Post and LOINC were not obtained.

### Cited Findings

**EU Database Directive 96/9/EC (original text as adopted, via legislation.gov.uk) [D]** ([Art. 7](https://www.legislation.gov.uk/eudr/1996/9/article/7/adopted); [Art. 8](https://www.legislation.gov.uk/eudr/1996/9/article/8/adopted); [Art. 15](https://www.legislation.gov.uk/eudr/1996/9/article/15/adopted))
- Art. 7(1): the maker of a database showing "qualitatively and/or quantitatively a substantial investment in either the obtaining, verification or presentation of the contents" may "prevent extraction and/or re-utilization of the whole or of a substantial part, evaluated qualitatively and/or quantitatively".
- Art. 7(2)(a): "'extraction' shall mean the permanent or temporary transfer of all or a substantial part of the contents of a database to another medium by any means or in any form".
- Art. 7(2)(b): "'re-utilization' shall mean any form of making available to the public".
- Art. 7(4): the right applies "irrespective of the eligibility of that database for protection by copyright".
- Art. 7(5): "The repeated and systematic extraction and/or re-utilization of insubstantial parts of the contents of the database implying acts which conflict with a normal exploitation of that database or which unreasonably prejudice the legitimate interests of the maker of the database shall not be permitted."
- Art. 8(1): the maker of a database "made available to the public" "may not prevent a lawful user … from extracting and/or re-utilizing insubstantial parts … for any purposes whatsoever". Art. 15 makes contrary contract terms "null and void".
- Note: the EUR-Lex HTML and PDF returned empty to the fetcher. The legislation.gov.uk "original (as adopted)" version was used. Later EU amendments, if any, were not checked.

**BHB v William Hill (C-203/02)**
- **[U]** The EUR-Lex and curia judgment texts returned empty content.
- **[D]** The Court of Appeal applying the ruling quotes the ECJ: "The resources used to draw up a list of horses in a race and to carry out checks in that connection do not constitute investment in the obtaining and verification of the contents of the database in which that list appears." It holds that "the question under Art.7(5) as to whether illegitimate 'small but regular helpings' were being taken does not arise". — [BHB v William Hill [2005] EWCA Civ 863 (July 2005), National Archives Find Case Law](https://caselaw.nationalarchives.gov.uk/ewca/civ/2005/863)
- **[L]** Commentary on the ECJ judgment (9 Nov 2004, ECLI:EU:C:2004:695): Art. 7(5) catches repeated insubstantial extractions whose "cumulative effect" would reconstitute "the whole or a substantial part" of the database. William Hill's extractions did not do so. — [5RB case summary](https://www.5rb.com/?p=5151); [Pinsent Masons Out-Law guide](https://www.pinsentmasons.com/out-law/guides/british-horseracing-board-v-william-hill)

**Royal Mail PAF Data Solutions Provider Licence (PDF created 25 Mar 2019) [D]** ([poweredbypaf.com PDF](https://www.poweredbypaf.com/wp-content/uploads/2019/06/paf-data-solutions-provider-licence-2019-1.pdf); retrieved via the fetch tool because curl hit a Cloudflare page)
- 1.2: "You may not use PAF® Data under this Licence unless you also have a valid data supply agreement".
- 3.7: except as permitted, licensees must not "copy, reproduce, extract, reutilise or publish PAF® Data or any of it".
- 3.9: licensees "may (without breaching the other restrictions in this clause) make copies of PAF® Data so far as reasonably necessary for back-up, security, business continuity and system testing purposes".
- 13.2: sub-contractors may use PAF Data "to the extent necessary for … the creation and development of your Solutions … for your own business purposes … and not those of your sub-contractor".
- End User Terms 2(a): no copies except "reasonably necessary for back-up, security, business continuity and system testing purposes".
- "Data Extraction" means "the extraction of PAF® Data or any part of it for the generation of new address records in a new or existing database". Elsewhere: "Data Extraction is not permitted".
- Schedule 3 (Promotion/Trial):
  - trial access is limited to 3 months, after which the solution must be destroyed or returned within 10 working days;
  - website trials may be used "for the purposes of the testing of its functionality, capacity or performance", provided responses "are used for those purposes only";
  - no response may exceed the "Maximum Data Return", defined as "100 address records".
- **[L]** A current Royal Mail page reportedly offers microbusinesses (<9 employees, <£2m turnover) free PAF data for one year "for the purpose of developing your addressing Solutions". — [poweredbypaf.com search extract](https://www.poweredbypaf.com/licence-our-products/licence-agreements/pricing/pricing-essentials-microbuisness/). Whether the 2019 licence is still the current version is unverified.

**WHO ICD-11 / ICF / ICHI Terms of Use and License Agreement [D]** ([icd11-license.pdf, © WHO 2020](https://icd.who.int/en/docs/icd11-license.pdf))
- 1.2: licensed "under the Creative Commons Attribution-NoDerivs 3.0 IGO license … you are NOT permitted to make 'adaptations'".
- 1.2.2: "WHO does not consider incorporation of the Classifications into a software product to be an 'adaptation'", provided you do not reproduce or distribute them "in part or whole without the Classifications' codes" or "without the Classifications URIs", or under a different name or without attribution.
- 1.2.3: "Incorporation of Classifications into a software product, in data transmission and storage must include Classifications code, title and URI".
- 1.2.4: mapping or crosswalks "are not covered … and are subject to a separate written agreement from WHO".

**GLEIF LEI data [D]** ([GLEIF LEI Data Terms of Use](https://www.gleif.org/en/meta/lei-data-terms-of-use))
- "The data available through the Access Service are provided under the CC0 licence".
- GLEIF reserves the right to suspend or modify the Access Service against uses that "threaten to undermine" GLEIS principles.
- The Terms of Use (which cover the access service, not the data licence) set liquidated damages of "CHF 100'000 for any single case of non-compliance".

**OpenFIGI Terms of Service (last updated 27 Nov 2018) [D/V]** ([OpenFIGI ToS](https://www.openfigi.com/docs/terms-of-service))
- Bloomberg "dedicat[es] … FIGI Identifiers to the public domain".
- "FIGI Identifiers may be freely reproduced, distributed, transmitted, used, modified, built upon, or otherwise exploited by anyone for any purpose, commercial or non-commercial".
- The dedication covers identifiers, not necessarily "Related Security Descriptions", which carry a separate disclaimer. That scope reading is **[I]**.

**ISO 4217 [D]**
- SIX, as "Secretariat of the Maintenance Agency for ISO 4217", says: "We maintain the code lists, update them and make them available online and free of charge". The page offers List One/Two/Three in XLS and XML. — [SIX Financial Data Standards page](https://www.six-group.com/en/products-services/financial-information/data-standards.html)
- No reuse licence text was found on the page, so free availability does not settle what reuse is allowed **[I]**.
- ISO 3166 licensing was not resolved: iso.org was Cloudflare-blocked **[U]**.

**Not obtained**
- **[U]** LOINC licence (loinc.org returned 403/Cloudflare).
- LSEG/Refinitiv, S&P, Dun & Bradstreet and Deutsche Post Datafactory licence texts were not attempted. **[I]** These are commercial terms usually under NDA. Earlier notes covered exchange market-data policies (Cboe, Deutsche Börse).

### Inferences
- **[I] Two independent tests for every artefact leaving the protected environment.**
  - (P) *Privacy:* could it identify or reveal a person or confidential record? (§§1–3).
  - (L) *Licence:* does it contain licensed content, or derive from it in a way the licence or the database right controls?
  Exporting a minimised fixture can fail either test. A fixture with real PAF addresses but synthetic people passes (P) and may fail (L). A fixture with a real person's attributes but CC0 LEIs passes (L) and may fail (P).
- **[I] Test use inside the licence boundary** is often expressly allowed. PAF clause 3.9 permits "system testing" copies, and its sub-contractor clause covers "creation and development". Those copies still count against the licence's other limits: no display to the public, no transfer, no Data Extraction into new databases. Development outside the protected environment by the same licensee or its contractors appears covered. A minimised fixture committed to a public or shared repository would be "publish[ing]" (3.7) and would fall outside the carve-out.
- **[I] Art. 7(5) matters for test pipelines.** Each fixture holds an insubstantial number of records, but CI that exports a few licensed records per run, every day, for years, is "repeated and systematic" extraction. Under the BHB commentary the test is whether the cumulative effect reconstitutes a substantial part. A fixture generator that samples *different* real reference records per run is the risky pattern. A fixed, small, versioned fixture set is the safer one. Art. 8 and Art. 15 protect insubstantial extraction by lawful users of databases "made available to the public", but whether a B2B licensed feed counts as "made available to the public" is unresolved here **[I]**.
- **[I] Fixtures from licensed codes.**
  - *ICD-11:* using real codes in fixtures is incorporation into software, permitted if code, title and URI travel together. Truncated or relabelled code lists (for example "first 50 codes without URIs") may breach 1.2.2. Crosswalks between ICD and other code systems need a separate WHO agreement.
  - *SNOMED* (earlier notes): extraction of a "substantial portion" by users is restricted, and there are territory limits.
  - *GLEIF/FIGI/ISO 4217:* lowest licence risk. Prefer them for identifier-shaped fixtures.
- **[I] Privacy controls do not cure licence issues, and vice versa.** DP noise on counts by licensed category is likely a "Produced Work"-like output (earlier notes). A failing fixture containing a real licensed value is extraction of content regardless of how it was anonymised. Rule-hit counts keyed by licensed code values disclose the code list itself if exported. That counts as non-substantial or substantial depending on cardinality.

### Gaps
- The full CJEU BHB judgment text was unreachable, so the "cumulative effect" wording is lead only. Later CJEU cases (Innoweb C-202/12, CV-Online Latvia C-762/19) were not read.
- The current, rather than 2019, PAF licence version is unverified. The LOINC, ISO 3166, LSEG, S&P, D&B and Deutsche Post terms were not obtained.
- I found no licence clause that specifically addresses *exporting test fixtures* as distinct from test copies, and no court decision on whether test fixtures count as extraction.
