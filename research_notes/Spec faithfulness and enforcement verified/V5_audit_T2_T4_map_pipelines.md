# V5 audit: §2.2 (T2), §2.3 (T3), §2.4 (T4), §3 check map and §4 candidate pipelines

Scope: the earlier report `reports/Spec faithfulness and enforcement.md`, sections §2.2–§2.4, §3 and §4. Each claim was compared first with the earlier notes (T2, T3a, T3b, T4) and then with the cited full text. Out of scope, as assigned to other verifiers: PBT-Bench, SysMoBench, TLA+-Bench, Req2LTL, Gay et al., Mäder & Egyed, FormalAlign, AlgoVeri, PROPAS, the DMN venue, the Cirstea venue, the CCF venue, OmniLink/Porcupine, the Cedar §3 challenge, Papadakis 2018, Knight & Leveson, Beer et al., Heitmeyer, Selby, plus all of §1, §2.1 and §2.5–§2.7.

Method: 43 full texts were downloaded to `scratchpad/v5/` and read with pdftotext and grep, plus targeted reads of the results sections. Venues were checked against PDF headers and the Crossref API, because DBLP served a bot-check page (HTTP 202 HTML) and could not be used. Grades follow the brief: A / A-pre / A-workshop / B / C / D. *Inference* marks this run's own reasoning.

---

## Q1. Are the §2.2–§2.4 figures, venues and grades carried by the notes and the full texts, at the stated strength?

### Takeaway
Most figures are carried exactly by both the notes and the full texts. Eight need correction, and the corrections cluster where a figure carries a recommendation or a §3 qualification:
- Vericoding's 9 %/15 % covers all three languages, not Verus only; the report inserted "[Verus]" into the quote.
- MutDafny's weak specs: 4 of 5 were in LLM-generated programs, not 3, and only 1 of those 4 was new. MutDafny's v2 also changed the mutant totals.
- Maoz–Ringert's 60/79 counts revisions of six student-team specifications, not 79 independent specs; under the semantics the students' tool actually used, 40 of 79 remain exploitable.
- Bosch's set sizes and run times have wrong minima (26 requirements and 48 s, not 50 and 1m33s).
- SAT-LLM is a published ASE 2024 paper (grade A, short), not a preprint, and its dataset is the authors' own.
- Watt CPP 2018 does not say the errors "survived engines and the reference interpreter".
- Mocket's "9 bugs" are 7 implementation bugs plus 2 bugs in the official Raft spec.
- Meta ACH's 73 % is the acceptance rate among tests engineers reviewed, not among all 571.

Several confirmed figures also need a strength caveat: the Frama-C JCVM smoke-test failures were all spurious, Maaz's $9.93 is an upper bound, Leveson's authors warn against ranking check types, and Cedar's 9.7 % comes from a different generator.

### Cited Findings
- **Bosch / Ultimate ReqAnalyzer, RE 2019.**
  - Table II lists ten device sets from Dev. 1 (26 requirements, 48 s) to Dev. 10 (701 requirements, 4h 14m 12s).
  - The report's "50–701 requirements" and "1m33s–4h14m" therefore have wrong minima. 1m33s is Dev. 3 (53 requirements). The error originates in the T2 notes.
  - Dev. 8 is confirmed: 263 requirements, 6 vacuous, 73 rt-inconsistencies, 18 timeouts, 3h 58m 36s.
  - Confirmed quotes: "From the ca. 310 results of the tool, 100 were classified as major issues, although the requirements had been reviewed manually several times before". "nearly 70% of our findings (including questions, typos, duplications, type issues) have resulted in a fix in the requirements, while the rest resulted in changes to the formalisation." "New changes are usually formalised in mere minutes". There is "room for further improvement by, e.g., introducing techniques from regression verification to reuse results".
  - The paper also says the remaining results "currently await classification", and that the initial formalisation "requires substantial effort (in the case-study, there are ca. 5000 different observables declared …)".
  - Authors are the tool's developers plus a Bosch co-author.
  - [RE 2019 PDF](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)
- **SAT-LLM (Fazelnia, Mirakhorli, Bagheri).**
  - Published: Crossref gives "Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering" (ASE 2024), DOI 10.1145/3691620.3695302, so grade **A**, not A-pre. It is a short paper reporting "early experiments" and "preliminary results"; the track was not verified.
  - Figures confirmed: 55 requirements in 15 conflicting subsets, four of them composite. ChatGPT (GPT-4) alone: "Precision of 0.85, Recall of 0.31, and an F1 score of 0.46". SAT-LLM: "Precision of 1.00, Recall of 0.83, and an F1 score of 0.91".
  - Independence: the dataset is the authors' own (Fazelnia et al. [16], a Broker system of 45 requirements and 12 conflict subsets), "expanded … by adding 10 requirements, specifically targeting three Composite-Negation conflicting sets". Composite conflicts are exactly where SAT-LLM's advantage is largest (100 % of composite sets vs 25 %).
  - [NSF PAR PDF](https://par.nsf.gov/servlets/purl/10574434)
- **DMN tables (arXiv 1603.07466).** Table 2: missing-rule detection 160 ms to 18,263 ms; overlap detection 200 ms to 30,736 ms. Table 3: for 1,492 rules × 3 columns, 812 overlapping rule sets vs 23,115 for "Signavio" (the report's "naive algorithm" is Signavio's editor algorithm). Confirmed. The venue was not checked (assigned elsewhere). [arXiv](https://arxiv.org/pdf/1603.07466)
- **FRET compositional realizability, FM 2021.**
  - LMCPS FSM: monolithic 1524.82 s; compositional 3.51 s and 6.74 s. "allowed us to reduce the total analysis time from 1524.82s to less …". Confirmed.
  - "unknown" due to non-linearities and the 12 h timeout are confirmed.
  - Three specs (LMCPS NN, LMCPS TSM, Infusion Manager) returned a single SCC. "One reason that contributed to the unsuccessful decomposition was that requirements were connected through mode variables": mode variables are one contributing reason, not the sole one.
  - Tool authors (NASA FRET team).
  - [NTRS PDF](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf)
- **Maoz & Ringert, FSE 2016** (full text via the figshare open-access copy; the Zenodo URL in the notes returned 403).
  - "only 19 out of 79 environment specifications were found to be well-separated"; non-well-separation was detected for 60, and could be forced "from all initial positions (P-all) (41 out of 79 specifications)". These figures are confirmed.
  - The corpus, however, is "a total of 86 specifications for six robots with 2 to 26 revisions per robot. Seven committed specifications were syntactically invalid. The 79 valid specifications…", written by "six teams of two or three" undergraduate students. So n is 79 *revisions* of six projects, not 79 independent specifications.
  - The students' tool "implements the more robust strict realizability semantics", and under it "20 specifications … prevent forced assumption violations (5 trivially by unrealizable safety guarantees)". The report's "in 60 the system could win by forcing the environment to violate its assumptions" therefore overstates the case for the semantics actually in use. The paper defines non-well-separation as the environment *can be forced* to violate its assumptions.
  - The T2 notes' "common even among trained authors" is not supported: the authors are undergraduates.
  - Tool authors.
  - [figshare](https://figshare.com/articles/conference_contribution/On_Well-Separation_of_GR_1_Specifications/10223099)
- **Spectra unrealizable cores, ICSE 2021.** "227 specifications of 10 autonomous Lego robots, written by 3rd year undergraduate computer science students"; 14 + 26 = 40 unrealizable. Confirmed. These are also revision histories. Tool authors. [arXiv](https://arxiv.org/pdf/2103.00297)
- **Frama-C/WP smoke tests, TAP 2024** (LNCS, confirmed via Crossref).
  - JCVM at Thales: "over 7,000 lines of C", "more than 30,000 lines of ACSL", EAL7. Proof "over 4 hours … for more than 80,000 verification conditions". "Overall, only a 20min (i.e., ≈8%) overhead". 2,350 smoke tests. All confirmed.
  - Not stated in the report: "2,350 smoke tests were generated and 37 of them were proved to be failing … All failing smoke tests belong to the dead-code category and are justified by the assumptions … They are spurious alarms". The JCVM data is therefore evidence of *cost* and of qualitative guidance ("effectively guided the initial steps"), not of a measured detection yield.
  - "We also found internal soundness bugs of WP thanks to smoke tests … we have decided to turn most of our axioms into proper lemmas or Coq realizations" is confirmed.
  - Tool authors (CEA and Thales).
  - [PDF](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf)
- **Vericoding (arXiv 2509.22908)**, verbatim: "Dafny exhibited no issues (except for redundant lemmas), with LLMs correctly giving trivial solutions when the specs were weak. Verus showed many weak specs due to spec translation issues … Lean displayed occasional redundant lemma additions … and had some weak specs from the original sources. **Across Dafny, Verus and Lean**, conditioned on vericoding success, roughly 9% of the specs were too weak and another 15% had poor translations."
  - The sample was "5 randomly chosen successful vericoding outputs for each language and data source".
  - The report's "roughly 9% of the [Verus] specs" and its "found Dafny clean" are misreadings. "No issues" for Dafny refers to *LLM cheating behaviour*, and the same sentence says Dafny specs were weak in places.
  - The T2 notes' ellipsis dropped the "Across Dafny, Verus and Lean" clause, and the report then added "[Verus]". This is a writer-level distortion of an already truncated quote.
  - [arXiv](https://arxiv.org/pdf/2509.22908)
- **ReForm (arXiv 2507.16331).** "Out of the 115 analyzed failure cases … Weak specifications: 60 cases (52.2%) … Unverifiable specifications: 51 cases (44.3%) … Trivial specifications: 4 cases (3.5%)". Confirmed. Grade A-pre. [arXiv](https://arxiv.org/pdf/2507.16331)
- **Watt, CPP 2018.** "we identified several errors in the official specification which were acknowledged and fixed by members of the working group. In some cases, these errors meant that the type system was originally unsound." Confirmed. No sentence says the errors had "survived engines and the reference interpreter". That clause first appears in the T2 notes and should be labelled *Inference*. [PDF](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf)
- **Wasm phases and RFC 6410.** Phase 4 says "Two or more Web VMs have implemented the feature and pass the test suite (where applicable)"; RFC 6410 says "at least two independent interoperating implementations". Confirmed (B). [phases.md](https://raw.githubusercontent.com/WebAssembly/meetings/main/process/phases.md); [RFC 6410](https://www.rfc-editor.org/rfc/rfc6410.txt)
- **MongoDB, PVLDB 2020** (Crossref: PVLDB, May 2020).
  - MBTCG: "generated 4,913 C++ test cases". "36 handwritten C++ test cases covered 18 of the 86 branches (21%)". AFL "covered 79 of 86 branches (92%) after approximately 8 million total executions". Generated tests "covered all 86 branches (100%)". "a single engineer to spend one month" (Table: 2 + 2 weeks = 4 weeks). "the bug had faithfully been tran[scribed]". All confirmed.
  - MBTC: "implemented by two engineers in 10 weeks", "we abandoned the project after 10 weeks", "Bugs in post-processing could mask implementation bugs". All confirmed.
  - Practitioner self-report by MongoDB engineers, peer reviewed.
  - [arXiv](https://arxiv.org/pdf/2006.00915)
- **Mocket, EuroSys '23** (header confirmed).
  - "we find 7 bugs, among which 3 bugs are confirmed as previously unknown bugs, and 4 are known bugs. Besides, we find that 2 inconsistencies … are caused by specification bugs in the official Raft specification". The report's "9 bugs … including 2 in the official Raft TLA+ spec" sums correctly but merges the categories.
  - Annotations of 151, 152 and 134 LOC are confirmed.
  - Tool authors.
  - [PDF](https://gaoyu-cn.github.io/paper/2023-eurosys-mocket.pdf)
- **Remix, EuroSys '25.** "The conformance checking is unsound … only check safety properties"; "six severe bugs"; "within 40 person-hours". Confirmed. Tool authors. [arXiv](https://arxiv.org/pdf/2409.14301)
- **Cirstea et al.** "In all cases, trace validation quickly identified executions …"; "too imprecise logs may even lead to erroneous traces being accepted"; "we only have anecdotal evidence" (on effort). Confirmed. Authors include the TLC maintainers. [arXiv](https://arxiv.org/pdf/2404.16075)
- **CCF (arXiv 2406.17455).** "approximately two engineer-months, spread over four months", which included TLC enhancements and diagnosis. Consistency spec: "approximately one engineer-week, spread over a two-week period". DFS under 1 s vs "about an hour with BFS"; "six bugs". All confirmed. Microsoft authors on their own system. [arXiv](https://arxiv.org/pdf/2406.17455)
- **TraceLink, PACMPL 9 OOPSLA2 (Oct 2025)** (header confirmed). "9 previously undetected" bugs; "fixing those inaccuracies did not change the out[come]" of model checking. Timeout-model and failure-detector rows are confirmed. Tool authors. [PDF](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf)
- **Cedar, FSE Companion 2024** (Crossref).
  - Table 1 totals confirmed: Lean model 1,673; Rust production 15,693.
  - "differential and property testing have uncovered 21 bugs"; proofs "found and fixed 4 bugs in Cedar's policy validator". Confirmed.
  - "4 vCPUs … for 6 hours" confirmed; DRT "did not discover the non-termination bug" confirmed.
  - "35.5% of the when condition-expressions generated by the type-directed ABAC policy generator … are boolean literals" is confirmed. The 9.7 % belongs to a *newly added* expression generator ("we added a new input generator"), not to a repaired ABAC generator, so the report's "cut to 9.7 % with a new generator" is a slight overstatement.
  - String-size feature dropped: confirmed.
  - AWS authors on their own system.
  - [arXiv](https://arxiv.org/pdf/2407.01688)
- **Vikram et al. (arXiv 2307.04346).** "40 Python" API methods; a valid and sound PBT "in 2.4 samples"; GPT-4 covered "21% of properties extractable from API documentation". Confirmed. No venue ("Conference'17" template), so A-pre. Property coverage is the authors' own metric. [arXiv](https://arxiv.org/pdf/2307.04346)
- **Maaz et al., NeurIPS 2025 DL4Code workshop** (A-workshop confirmed).
  - "56.0% (95% CI: 42.2%, 69.8%)" valid; "$5.56/bug report … $9.93/valid bug". Confirmed.
  - Caveats in the full text: the sample was n = 50 "from the top 80% by score" under an LLM-graded rubric; initial κ = 0.31; the authors call $9.93 "an upper bound on the real-world cost".
  - Affiliations: Anthropic and MATS; the co-author Hatfield-Dodds is a Hypothesis maintainer. This is a vendor-affiliated evaluation of its own agent.
  - [arXiv](https://arxiv.org/pdf/2510.09907)
- **Leveson et al., TSE 1990.** "Nineteen % … by specification-based checks, 43 % by code reading, and 38% by code-based checks"; "Only 12% (4 out of 34) of the effective checks were formulated … after looking at the requirements specification alone." Confirmed.
  - Same paragraph: "It would be inappropriate (and even misleading) to claim that checks of one type are more effective than others based on our data."
  - The spec-only checks were written *before* code access (a sequential design), so the comparison is confounded by order.
  - [typeset copy](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf)
- **Zhao et al., PACMSE 3 ISSTA (Oct 2026).** Misguided tests 137.69 (3.84 %) vs 16.46 (0.46 %); effective 104.15 (2.98 %) vs 304.08 (8.51 %); docstring mitigation lifts effective tests "from 104.15 to 186.77". Confirmed. 233 defects. [arXiv](https://arxiv.org/pdf/2607.22883)
- **Konstantinou et al.** MUT+TP: 43.02 % vs 35.72 %. Confirmed. A-pre. [arXiv](https://arxiv.org/abs/2410.21136)
- **Mathews & Nagappan.** CodiumAI and CoverUp "reject such tests during their generation process, with 470 and 400 such tests being discarded"; filtering tools "systematically retain these bug-validating tests". The report's wording is confirmed.
  - The notes' 59.6 % and 68.1 % have different denominators: 171/287 samples vs 62/91 produced suites. CoverUp "failed to generate a test suite for 196 cases (68.3%)".
  - [arXiv](https://arxiv.org/pdf/2412.14137)
- **TiCoder, IEEE TSE 2024** (Crossref). n = 15 programmers; "average absolute improvement of 45.97% in the pass@1" with "an idealized proxy for a user feedback". Confirmed. Microsoft authors on their own workflow. [arXiv](https://arxiv.org/pdf/2404.10100)
- **Non-commitment oracle mechanisms (B).** All confirmed:
  - Wasm `( either <result_pat>+ ) ;; alternative results` and `nan:canonical`; relaxed SIMD "globally chooses a fixed projection for each operator";
  - sqllogictest `nosort`/`rowsort`/`valuesort`, `skipif`/`onlyif`;
  - JSON Schema `optional/`, which "currently conflates many reasons";
  - POSIX result codes "taken from IEEE … (IEEE 1003.3-1991)", including UNRESOLVED and UNSUPPORTED.
  - [Wasm README](https://raw.githubusercontent.com/WebAssembly/spec/main/interpreter/README.md); [relaxed SIMD](https://raw.githubusercontent.com/WebAssembly/relaxed-simd/main/proposals/relaxed-simd/Overview.md); [sqllogictest](https://raw.githubusercontent.com/gregrahn/sqllogictest/master/about.wiki); [JSON Schema](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/README.md); [LTP](https://raw.githubusercontent.com/linux-test-project/ltp/master/testcases/open_posix_testsuite/Documentation/HOWTO_ResultCodes)
- **NonDex.** The JPF 2016 workshop paper says "we found 60 bugs in open-source projects and 110 bugs in student homework submissions", reporting the authors' "recent work" (ICST 2016). The figure is second-hand within a workshop paper by the tool authors. [PDF](https://mir.cs.illinois.edu/gyori/pubs/jpf16.pdf)
- **PatchDiff, ICSE 2026** (Crossref). 29.6 %, 46.8 %, 27.3 %, 28.6 %, and "inflates the resolution rates … by 6.4 absolute percent[age points]". Confirmed. The authors' own tool, applied to third-party agents' patches. [arXiv](https://arxiv.org/abs/2503.15223)
- **LiSSA, ICSE 2025** (Crossref).
  - Table III (GPT-4o, top-20) best F1: SMOS .423, eTour .526, iTrust .290, Dronology RE .273, Dronology DD .254. The report's "roughly 0.25–0.53" is confirmed.
  - Not said in the report: LiSSA does not beat all baselines (eTour FTLR_OPT .548; SMOS VSM_OPT .422).
  - Tool authors.
  - [KIT PDF](https://publikationen.bibliothek.kit.edu/1000179816/164563088)
- **IronSpec (OSDI 2024 per acknowledgements).**
  - "the discovery of ten specification bugs across all six real-world verified systems" (all three components together).
  - The Table 3 alive-mutation column sums to 61. "we consider 13 to be" false positives.
  - Time ranges from 3 s to 191 min. STP suites took "a few hours to multiple days".
  - All confirmed. Tool authors.
  - [NSF PAR](https://par.nsf.gov//servlets/purl/10550356)
- **MutDafny (arXiv 2511.15403).**
  - v1 says "112,810 mutants", Total row "31,515 (27.94%)" survived, average score 79 %. These match the report.
  - **v2 (current) says "118,458 mutants", "30,459 surviving", average 82 %.**
  - Both versions: 284 reviewed survivors, 77 weak-spec hints, 157 equivalent, 5 weaknesses. "The remaining programs were generated by LLMs … Misu et al. [45] … report one of the weaknesses … the remaining three that went unnoticed … two of the weaknesses had previously been detected by Endres et al. [20], the third one being a new discovery."
  - So **4 of 5** weak specs were in LLM-generated programs (one repo, bst4copy, was the fifth). Of those four, only one was new. The report's "3 of them in LLM-generated programs" is wrong; it conflates "three that went unnoticed".
  - Tool authors.
  - [v1](https://arxiv.org/pdf/2511.15403v1); [current](https://arxiv.org/pdf/2511.15403)
- **Jovanovic, Patwary, Sullivan, FormaliSE 2025** (Crossref: "Refining Alloy-Based Mutation Operators to Reflect Common Mistakes"). 25,180 unique faulty submissions; correct 10.96 % (17.72 %); detect 91.78 % (95.79 %). Confirmed. Sullivan co-authored μAlloy (tool-author flag). [PDF](https://allisonius.github.io/files/FormaliSE2025.pdf)
- **Just et al., FSE 2014.** 357 real faults; coupling "for 73% of real faults"; "17% of real faults are" not coupled; 10 % need improved operators. Confirmed. Just authored the Major mutation framework used in the study (partial flag). [PDF](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)
- **Chekam et al., ICSE 2017.** "strong mutation testing has the highest" fault revelation; the Clean Program Assumption "does not always hold". Confirmed. [PDF](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)
- **Google (Petrović et al., arXiv 2103.07189).** "almost 15 million mutants", "six" years, "evidence that mutants are indeed coupled with real faults", developers "write more tests". Confirmed. Google authors on their own deployment. [arXiv](https://arxiv.org/abs/2103.07189)
- **Hughes, "How to Specify It!"** "Validity properties miss many bugs (five of eight)"; "prop UnionModel fails after only 8.4 tests" vs "50 tests on average"; 79.2 %. Confirmed. QuickCheck's author on his own approach. [Chalmers PDF](https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf)
- **Goldstein et al., ICSE 2024** (Crossref). "Mutation Testing (7/30)", "Example Inspection (8/30)", "Code Coverage (2/30)". Confirmed. [PDF](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf)
- **Wang et al., TOSEM 2025** (header: ACM Trans. Softw. Eng. Methodol., January 2025). 851 real bugs; "76.47%, compared to 44.15% for rule-[based]". Confirmed. [arXiv](https://arxiv.org/pdf/2406.09843)
- **Meta ACH.**
  - "10,795 Android Kotlin classes … 9,095 mutants and 571 privacy-hardening test cases". Confirmed.
  - The 73 % is from "test-a-thons where engineers accepted 73% of its tests", i.e. "an acceptance rate of 73% from the engineers who reviewed them". The denominator is the reviewed subset, not all 571.
  - P 0.79 / R 0.47 (0.95 / 0.96 with preprocessing). Confirmed.
  - Meta authors on their own tool.
  - [arXiv](https://arxiv.org/pdf/2501.12862)
- **Trace tooling (B).**
  - OFT `LinkStatus.java` defines `OUTDATED`, `AMBIGUOUS` and `ORPHANED`; `quiet` gives "no output (in case only the return code is used)"; `direct_failures` lists "non-transitive defects".
  - Doorstop flags a "suspect link" when the parent fingerprint changes and `doorstop clear` clears it.
  - Doorstop's "exits 1 on failure" is not in `validation.md`; the notes cite the CLI source, which was not re-read.
  - [OFT LinkStatus](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/api/src/main/java/org/itsallcode/openfasttrace/api/core/LinkStatus.java); [OFT CLI](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/oft_command_line.md); [Doorstop](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/docs/cli/validation.md)

### Inferences
- *Inference:* The Vericoding correction strengthens the earlier report's §3 qualification, because weak specs occur in Dafny too. The "Dafny clean" carve-out should be dropped. See the baseline quote in Notes.
- *Inference:* The Maoz–Ringert correction weakens the check-map claim "(60/79 GR(1) specs failed this)". The evidence is six student projects in revision history, and 40/79 under the semantics actually in use. Well-separation stays a cheap, well-defined check (median 15 ms in the paper). Its *prevalence* figure is weak evidence.
- *Inference:* The MutDafny correction changes the reading "LLM-written Dafny specs carry weak postconditions that verification passed". The weaknesses were real, but three of the four had been found before by other spec-quality methods (Misu manual inspection; Endres et al.). MutDafny confirms existing detection more than it shows unique yield.
- *Inference:* The Frama-C JCVM case shows that smoke tests are affordable (≈8 %). It does not show they catch spec inconsistencies in industrial specs: all 37 failures there were spurious. The catch evidence is the WP-library axiom bugs plus illustrative examples.

### Gaps
- MutDafny: the report cites v1, but v2 is the current version. Which totals to cite is an editorial choice. Use v2 and note that v1 differs.
- The Doorstop exit code was not re-checked against its CLI source.
- Not re-checked by this run although inside §2.2–§2.4: Hanfor, EuRailCheck, van Lamsweerde & Letier, Degiovanni et al. and its 2022 critique, Nuseibeh et al., ProofPulse, SpecRL, Lahiri FMCAD, the Dafny/Lean/Alloy docs, the W3C Process, Kupferman–Vardi, P# FAST 2016, the Quint/Apalache posts, DTest, icontract-hypothesis, FoundationDB, Ricca, Karpurapu, Sami, AToMIC, the BDD mapping, Canedo, NL2Contract, TLA-Prover, mutmut, TLC coverage docs, QuickCheck and Hypothesis API docs. The brief's priority list did not name them. The earlier notes record full-text reads for most of them.

---

## Q2. Independence: tool authors evaluating their own tool, and vendor posts

### Takeaway
Almost every measured figure that carries a §3 or §4 recommendation comes from tool authors or from vendors reporting their own systems. The exceptions are Zhao, Konstantinou, Mathews & Nagappan, Leveson, Chekam, Goldstein, the Wang TOSEM LLM-mutant study, and Just in part. Of these, only Zhao and Leveson bear on the expectation-family recommendations, and neither measures prose-derived against spec-derived oracles.

### Cited Findings
- **Tool authors on their own tool:**
  - Bosch/ReqAnalyzer (Ultimate team);
  - FRET (NASA);
  - Spectra and well-separation (Maoz group);
  - Frama-C smoke tests (CEA with Thales);
  - SAT-LLM (own method on own dataset);
  - Mocket; Remix; TraceLink; Cirstea et al. (TLC maintainers); NonDex; PatchDiff; LiSSA; IronSpec; MutDafny;
  - μAlloy operators (Sullivan co-author); QuickCheck/Hughes; Meta ACH; TiCoder; Vikram (own metric).
  - Sources as in Q1.
- **Vendor or practitioner self-reports on their own systems** (peer reviewed): MongoDB (PVLDB), CCF/Microsoft, Cedar/AWS, Google mutation, Meta ACH. Maaz et al. is Anthropic-affiliated with a Hypothesis maintainer (workshop). Sources as in Q1.
- **No tool-author or vendor conflict found:** Zhao et al.; Konstantinou et al.; Mathews & Nagappan; Leveson et al.; Chekam et al.; Goldstein et al.; Wang et al. (TOSEM evaluates others' tools alongside LLM approaches); Watt (independent mechanisers of others' spec).

### Inferences
- *Inference:* No neutral benchmark exists for the conflict, realizability and vacuity tools as a group. Bosch's "100 major of ca. 310" and FRET's speed-ups are author-run case studies; SAT-LLM ran on its authors' own expanded dataset. The §4 Pipeline B precedents therefore rest on author-reported efficacy.

### Gaps
- No independent replication was found for IronSpec, MutDafny, Mocket, TraceLink or Remix in the texts read.

---

## Q3. §3 check map and §4 pipelines: transfer label, confidence, overturning finding, single-source cells

Transfer labels follow the brief:
- *direct*: evidence on library or API behaviour specs;
- *analogous*: other spec domains;
- *inference*: this run's or the earlier report's reasoning.

The earlier report marks every §3 cell as *Inference* that maps mechanisms onto forms. Below, each label names the evidence under that inference. "Single source" means the cell's evidence rests on one study.

### Takeaway
No §3 cell and no §4 gate rests on *direct* evidence of *effectiveness* for library or API behaviour specs. Direct evidence exists only for **mechanisms**:
- POSIX, sqllogictest and JSON Schema verdicts and sorts;
- NonDex perturbation of underdetermined Java library specs;
- Hypothesis stateful testing and contract → property tooling;
- Vikram's LLM PBTs from Python API documentation, which shows weak coverage (21 %).

Everything else is analogous: embedded or automotive requirements, distributed protocols, Dafny or Alloy benchmarks, Java code mutation. The highest-confidence cells are per-table complete/disjoint checks and the non-commitment oracle verdicts; their mechanisms are decidable or established. The lowest are the frame divergence check, realizability with environment actions for a store API, the per-family kill gate, and every claim about faithfulness to the prose.

### §3 check map, per row

| Row / check stated | Transfer | Confidence | Single source? | One finding that would overturn it |
|---|---|---|---|---|
| Formula over one instant: faithfulness (scenario derivability, rejected-option refutation, added-commitment probe) | analogous (Cunha & Macedo: Alloy, student errors; Lahiri: MBPP-Dafny; T1 sources not re-checked here) + inference (rejected options as negatives) | low–medium | Rejected-option use: no source (inference) | A one-operation trial in which record-derived positive and negative checks kill under half of seeded clause misreadings, or have a false-alarm rate above their kill rate |
| Formula: consistency (SMT conjunction over shared abstract state, unsat core; Dafny assumption warnings) | analogous (Bosch, PROPAS, SAT-LLM n = 55) | medium | No | Store-API contracts with quantifiers over handed-out objects return UNKNOWN or time out for most k-subsets (PROPAS needed a pessimistic quantifier encoding; Bosch had 18 timeouts in one set) |
| Formula: satisfiability (interesting witness; verified R body; negate postcondition; output-mutation spectests) | analogous (Kupferman–Vardi; Dafny docs; SpecRL A-pre) | medium | Spectests: SpecRL only | Spectests built from records rejected by a weak but faithful spec at the same rate as by a misread one (no discrimination) |
| Formula: enforcement (contract → Hypothesis property; scenario I/O; rejected-option mutant) | direct tooling (icontract-hypothesis, Hypothesis docs; B, no effectiveness data) + analogous (Cedar's rare-input miss) | medium | Cedar's miss is one anecdote | Contract-derived properties on R killing no more clause mutants than scenario literals alone |
| Earliest failure "before the spec" | inference | low | — | Record-derived checks drafted before the spec turning out mostly over-strict (scenarios fix values that decisions leave open), so they cannot gate |
| Case table: per-table complete/disjoint | analogous (DMN A-pre, timings only; ACSL in §3 baseline) | **high** for the mechanism, medium for cost transfer | Timing: DMN only | Table guards that need non-linear or unbounded predicates over abstract state, so completeness is undecidable or UNKNOWN |
| Case table: cross-table conjunction, maximal overlaps | analogous (Bosch k-subsets; DMN maximal sets) + inference | medium | — | Conjoined cross-table checks finding nothing that row-scenario expectation tests did not already catch |
| Case table: dual slot-filling diff (Easterbrook) | T1 source, not re-checked; analogous | low–medium | Likely single | Two agent lineages agreeing on wrong rows at a rate similar to their disagreement rate (correlated misreading) |
| Frame: divergence vs effect, failure and cancellation tables under a boundary condition | analogous (van Lamsweerde & Letier: A-workshop, no detection data; Degiovanni ASE 2018: search, "not complete") + inference | **low** | Yes: no measured detection anywhere | Plain conjunction with environment states enumerated (bounded TLC) already catching all seeded frame/effect clashes, so divergence search is unnecessary; or search too slow to gate |
| Frame: full-state snapshot through `alpha` | analogous (Mocket, Quint Connect state comparison) + inference | medium | — | Hidden R state outside `alpha` accounting for most surviving frame mutants |
| Termination: well-separation check | analogous; single source (Maoz–Ringert: 79 *revisions* of six student projects; 60 non-WS, 40 under strict semantics) | medium for the check, **low** for "60/79" as a prevalence argument | **Yes** | Library timeout assumptions that cannot be cleanly split into environment inputs and system outputs, so the check is inapplicable; or a trial finding no non-well-separated assumptions in records |
| Termination: TraceLink-class timeout bugs at G6; DRT misses non-termination | analogous (TraceLink: tool authors, PGo only; Cedar: one bug) | medium–low | Each single | R's timeouts are deterministic and explicit, so the "always/never fires" class cannot arise |
| State × operation table: missing cell (G3); TLC never-enabled; Alloy `run` non-empty | analogous / B docs | **high** (mechanism) | — | Cell-completeness passing while typestate and failure tables still disagree (needs G4, so G3 is not the earliest useful gate) |
| State × operation: Hypothesis `RuleBasedStateMachine` or model-generated per-step replay | direct tooling (Hypothesis docs, B) + analogous (MongoDB MBTCG: one 1 kLOC function, 100 % branch coverage; Mocket) | medium | MBTCG yield: MongoDB only | Per-step replay from the model finding no clause mutant that Hypothesis stateful tests on R miss, making the model-generated leg redundant |
| Environment actions: rt-consistency / realizability with environment actions as free transitions; well-separation | **inference** by analogy (FRET, Bosch rt-consistency, GR(1)); no library or storage application found | **low** | — | Bounded TLC/Apalache with free environment actions exploding beyond feasible bounds for one operation with handed-out objects; or finding nothing plain model checking misses |
| Environment actions: faults and cancellation as first-class generated actions | analogous (Remix, CCF `IsFault`, P#, FoundationDB B) | medium | — | Fault actions in the alphabet producing mostly infeasible schedules on a single-process Python R |
| History predicate: Porcupine-style check against sequential R; OmniLink for weaker predicates | analogous (assigned elsewhere; not re-checked) | medium | OmniLink single | Unspecified outcomes making R's sequential mode nondeterministic, so a linearizability check needs set-valued models (blow-up, §3 seed) |
| Failure tables: per-table check, fault actions, history bridge for retries | analogous (as case table + environment) | medium | — | Retries × concurrency conflicts escaping both the table and the history checks in a seeded trial |
| Register of non-promises: two witnesses per entry; allowed-variant check | **direct** for the perturbation mechanism (NonDex on Java library underdetermined specs: A-workshop, tool authors, 60/110 bugs second-hand) + inference | medium | **Yes** (NonDex) | Perturbing R on a non-promised dimension, which violates other clauses (the dimensions are not independent), so over-strictness cannot be isolated |
| Variation points / profiles: parametrised suite, UNSUPPORTED, per-profile expected sets | **direct** mechanisms (POSIX 1003.3 codes, JSON Schema `optional/`, sqllogictest `skipif`/`onlyif`; B, no effectiveness data) | **high** (mechanism) | — | Profile values interacting (non-orthogonal), so per-value suites miss pairwise conflicts |
| Profiles: "one witness per profile value", not a fixed two | **inference** (no source measures yield per witness; Watt's "survived engines" is an inference, not a finding) | low–medium | — | A trial showing a second, differently built witness finding more ambiguities than per-profile witnesses built by the same lineage |

### §4 gate sequence (§2.4 table), per gate

| Gate | Transfer | Confidence | Single source? | One finding that would overturn it |
|---|---|---|---|---|
| G0 ID/schema lint | direct tooling (OFT, sphinx-needs, Doorstop: B) | high | — | Lint false failures dominating agent iterations (no data either way) |
| G1 upward trace (orphan = added commitment, missing = lost case) | direct tooling + **inference** for the faithfulness reading | high for orphan or dangling detection; **low** for catching added commitments | — | Seeded added commitments that carry a plausible decision link and all pass G1 (a link proves existence, not binding) |
| G2 faithfulness exhibition | T1 (not re-checked here); analogous + inference | low–medium | — | Witness review by a spec-blind judge missing most seeded misreadings |
| G3 form-local checks | analogous (DMN); decidable | high | Timing: DMN only | As in the case-table row |
| G4 cross-clause consistency and satisfiability (unsat core, rt/realizability, well-separation) | analogous (Bosch, FRET, SAT-LLM, Maoz–Ringert); all tool-author evaluations | medium | Well-separation single | Translating history predicates and typestate into one logic proving infeasible, or translation errors dominating findings (the EuRailCheck caveat) |
| G5 vacuity and non-triviality | analogous (Frama-C: cost ≈8 %, but 37/37 JCVM failures spurious; ReForm; Kupferman–Vardi) | medium | — | Vacuity gates on agent-written TLA+/Dafny for this domain flagging mostly intended non-commitments (high false-alarm rate) |
| "G5 must precede trusting a model-checking pass" | inference (logical) | high | — | — |
| G6 F ↔ R conformance (DRT, replay, trace validation) | analogous (Cedar, MongoDB, Mocket, Cirstea, CCF, TraceLink) | medium | — | DRT and replay between an agent-written model and an agent-written R from the same clauses showing zero disagreements on seeded misreadings (common mode) |
| G6 cost "minutes" | inference (CCF's 1 week to 2 months and MongoDB's 10 weeks are human build costs on large systems) | low | — | — |
| G7 downward trace and coverage | direct tooling (B) + analogous (Chekam threshold; Hughes n = 8 bugs; Goldstein) | medium (necessary-only) | Hughes single | — |
| G8 per-family mutant kill + allowed-variant check | **inference**; building blocks analogous (MutDafny, IronSpec) and direct (NonDex) | **low–medium** | No study of the gate itself | Seeded clause misreadings killed by both families at near 100 % (no discrimination), or equivalent-mutant triage costing more than the findings are worth (MutDafny: 157 of 284 equivalent) |
| G9 spec-strength mutation | analogous (IronSpec: tool authors; 13 of 61 survivors intended; 3 s to 191 min) | medium–low | Yes (IronSpec) | Survivors on a store-API spec being dominated by intended non-commitments even after register-based auto-classification |
| Order "G8/G9 after G6" | inference consistent with IronSpec ("only if the system has a passing proof") | medium | — | — |

### §4 pipelines

| Pipeline / stated element | Transfer | Confidence | Single source? | One finding that would overturn it |
|---|---|---|---|---|
| A: record-derived check set by a records-only lineage *before* the spec | analogous (TiCoder: n = 15, idealised proxy, code generation; Fit: n = 13 students; Cunha & Macedo not re-checked) + inference | low–medium | — | The central trial: prose-derived checks killing seeded misreadings no better than spec-derived tests (the report says this is unmeasured) |
| A: expected failure "about 4 % wrong generated tests" | analogous (Cunha & Macedo; not re-checked here) | — | Yes | — |
| A: "weaker cross-form conflict detection than B" | inference | low | — | — |
| B: dual slot-filling + common-logic conjunction + rt/realizability + well-separation | analogous (Bosch, EuRailCheck, SAT-LLM, FRET; author-run) | medium for conflict detection; **low** for agent translation (SAT-LLM: one ASE short paper, own dataset, n = 55) | Agent leg: single | LLM translation into the shared signature introducing more false conflicts than the conflicts it finds on the brief's real records |
| B: comparison point "Bosch roughly 70/30" | analogous; confirmed, but tool-author self-report from an ongoing case study, with some results "await[ing] classification" | medium | Yes | — |
| B: "Bosch: 18 timeouts in one set; FRET unknown on non-linear arithmetic" | analogous; confirmed | high (as a failure-mode statement) | — | — |
| C: single executable source + independent property set + second executable with DRT | analogous (Cedar verified; SpecTec, Arm ASL, JEST not re-checked here) | low–medium | Cedar's feature-drop anecdote single | The second executable, built from records, converging on the first one's reading, with near-zero DRT disagreements on seeded misreadings |
| Cross-pipeline trial design | inference | — | — | — |

### Inferences
- *Inference:* The §4 recommendations most exposed to a single overturning datum are G8 (no study), the frame divergence check (no detection data), and environment-action realizability (no library application). All three are *inference* with analogous building blocks, so they should be labelled low confidence in the corrected edition.
- *Inference:* The direct evidence in the report (POSIX, sqllogictest, JSON Schema, NonDex, Hypothesis, Vikram) supports oracle *form*, not oracle *yield*. Vikram's 21 % property coverage is the only direct measurement of agent behaviour on API specs, and it argues for harness-imposed per-clause obligations. The report already draws that conclusion.

### Gaps
- No source measures any §3 cell's detection rate on a library or API behaviour spec.
- The T1 sources behind the faithfulness columns and Pipelines A and C (Cunha & Macedo, Easterbrook, SpecTec, Arm/Reid, JEST, Lahiri) were not re-checked by V5.

---

## Verification log entries

| ID | Report location + verbatim claim | Verdict | Corrected text (if any) | Grade | Full text read | n and setting | Independence flag | Evidence (quote + page/section) |
|---|---|---|---|---|---|---|---|---|
| V5-01 | §2.2 table: "'ca. 310 results … 100 were classified as major issues, although the requirements had been reviewed manually several times before'" | confirmed | — | A (RE 2019) | yes | 10 Bosch device sets, automotive | tool authors (+ Bosch co-author) | §VI.C: "From the ca. 310 results of the tool, 100 were classified as major issues…"; "remaining results … await classification" |
| V5-02 | §2.2: "Ten device sets of 50–701 requirements" | corrected | "Ten device sets of 26–701 requirements" | A | yes | Table II | tool authors | Table II: Dev. 1 = 26 req.; Dev. 10 = 701 |
| V5-03 | §2.2: "Nearly 70% of findings led to requirement fixes, the rest to formalisation changes" | confirmed | add "(including questions, typos, duplications, type issues)" | A | yes | Bosch | tool authors | §VI.C: "nearly 70% of our findings (including questions, typos, duplications, type issues) have resulted in a fix in the requirements" |
| V5-04 | §2.2: "One 263-requirement set had 6 vacuous requirements, 73 rt-inconsistencies, 18 timeouts, and took 3h58m" | confirmed | — | A | yes | Dev. 8 | tool authors | Table II: "Dev. 8 263 234 6 73 18 3h 58m 36s" |
| V5-05 | §2.2 Cost: "1m33s–4h14m per full run" | corrected | "48 s – 4h14m per full run" | A | yes | Table II | tool authors | Dev. 1 "48s"; Dev. 3 "1m 33s"; Dev. 10 "4h 14m 12s" |
| V5-06 | §2.2 Cost / Incremental: "Minutes to formalise a change; no result reuse implemented" | confirmed | add: initial formalisation "requires substantial effort" (ca. 5000 observables) | A | yes | Bosch | tool authors | §VI.C: "New changes are usually formalised in mere minutes"; "room for further improvement … reuse results from previous analysis runs" |
| V5-07 | §2.2: "SAT-LLM (A-pre). 55 requirements with 15 injected conflicting subsets (4 composite). LLM alone: P 0.85, R 0.31. LLM→FOL + Z3: P 1.00, R 0.83" | corrected (grade) | "SAT-LLM, ASE 2024 short paper (A; 'early experiments'); dataset is the authors' own, expanded with 10 requirements targeting composite conflicts" | A | yes | 55 req., Broker system, GPT-4 | tool authors on own dataset | Header DOI 10.1145/3691620.3695302 (Crossref: Proc. 39th ASE); §3.1 "expanded the dataset by adding 10 requirements, specifically targeting three Composite-Negation conflicting sets"; RQ1/RQ2 boxes |
| V5-08 | §2.2: "missing-rule check 160 ms–18.3 s, overlap check 200 ms–30.7 s. Reported 812 maximal overlapping rule sets vs 23,115 from a naive algorithm" | confirmed | "naive" = Signavio's algorithm | A-pre (venue not checked) | yes | 9 tables, ~500–1,500 rules | none noted | Table 2; Table 3: "812 … Signavio … 23 115" |
| V5-09 | §2.2: "LMCPS FSM 1524.82 s → under 7 s … 'unknown' … 12 h timeouts; 3 of 12 benchmarks collapsed to one component via mode variables" | confirmed (nuance) | "…single SCC; mode variables named as one contributing reason" | A | yes | 12 NASA/industrial benchmarks | tool authors | Table: "LMCPS FSM … 1524.82 3.51 6.74"; "One reason that contributed … mode variables" |
| V5-10 | §2.2: "Spectra … 227 student GR(1) specs, 40 unrealizable, many with multiple cores" | confirmed (nuance) | specs are revision histories of 10 robots | A | yes | SYNTECH15/17 | tool authors | §6: "227 specifications of 10 autonomous Lego robots … 3rd year undergraduate"; 14 + 26 unrealizable |
| V5-11 | §2.2: "only 19 of 79 student specs well-separated, i.e. in 60 the system could win by forcing the environment to violate its assumptions" | corrected | "19 of 79 committed revisions (six undergraduate team projects) were well-separated; under the strict realizability semantics the students' tool used, 20 of 79 prevented forced assumption violations (5 trivially), leaving 40" | A (FSE 2016) | yes (figshare) | 79 valid revisions of 6 projects | tool authors | §7: "86 specifications for six robots with 2 to 26 revisions per robot"; "only 19 out of 79"; "With strict realizability semantics 20 specifications … prevent forced assumption violations (5 trivially …)" |
| V5-12 | §3 check map, Termination row: "(60/79 GR(1) specs failed this)" | corrected | "(60 of 79 revisions of six student projects; 40 under strict realizability)" | A | yes | as V5-11 | tool authors | as V5-11 |
| V5-13 | §2.2: "Thales JavaCard VM, 2,350 smoke tests for about 20 min (≈8%) on top of a more-than-4 h proof; they also found unsound axioms in WP's own library" | confirmed (strength caveat) | add "37 smoke tests failed on JCVM, all spurious dead-code alarms" | A (TAP 2024) | yes | JCVM, EAL7 | tool authors (CEA + Thales) | §4: "only a 20min (i.e., ≈8%) overhead"; "2,350 smoke tests were generated and 37 of them were proved to be failing … They are spurious alarms" |
| V5-14 | §2.2: "ReForm … of 115 failures, 52.2% weak specs, 44.3% unverifiable, 3.5% trivial" | confirmed | — | A-pre | yes | 115 ReForm-3B-RL failures | tool authors | Failure analysis: "Weak specifications: 60 cases (52.2%) … 51 cases (44.3%) … 4 cases (3.5%)" |
| V5-15 | §2.2 [§3 qualification]: "Vericoding's own manual inspection found Dafny clean, but 'conditioned on vericoding success, roughly 9% of the [Verus] specs were too weak and another 15% had poor translations'" | corrected | "'Across Dafny, Verus and Lean, conditioned on vericoding success, roughly 9% of the specs were too weak and another 15% had poor translations' (5 random successes per language and source). Dafny's 'no issues' refers to LLM cheating, with 'LLMs correctly giving trivial solutions when the specs were weak'" | A-pre | yes | 5 samples per language × source | benchmark authors | Manual inspection paragraph, verbatim as in the left column |
| V5-16 | §2.2: "Watt, CPP 2018 (A): mechanisation found errors that made the Wasm type system 'originally unsound', which had survived engines and the reference interpreter" | corrected | drop "which had survived engines and the reference interpreter", or label it *Inference* | A | yes | Isabelle mechanisation | none (independent of spec authors) | §1: "In some cases, these meant that the type system was originally unsound"; no statement on engines or the interpreter missing the errors |
| V5-17 | §2.2: WebAssembly phase 4 "two or more Web VMs"; RFC 6410 "at least two independent interoperating implementations" | confirmed | — | B | yes | process docs | none | phases.md l. 92; RFC 6410 §2.2 |
| V5-18 | §2.2: "MutDafny found 3 of its 5 weak specs in an LLM-generated set" | corrected | "4 of 5 weak specs were in LLM-generated programs (Misu et al.); of these, Misu had reported 1 and Endres et al. 2 earlier, so 1 was new" | A-pre | yes (v1 and v2) | 24 files, 284 survivors | tool authors | §6.3: "The remaining programs were generated by LLMs … report one of the weaknesses … the remaining three that went unnoticed … two … previously detected by Endres et al. … the third one being a new discovery" |
| V5-19 | §2.3.1: "4,913 generated C++ tests covered 86/86 branches, vs 18 for 36 handwritten tests and 79 for about 8 M AFL runs … 'had faithfully been transcribed from C++ to TLA+'" | confirmed | — | A (PVLDB 2020) | yes | 1 kLOC OT merge function | vendor self-report | §5.2: "generated 4,913 C++ test cases … 18 of the 86 branches (21%) … 79 of 86 branches (92%) … all 86 branches (100%)" |
| V5-20 | §2.3.1 Cost: "1 engineer, 4 weeks" | confirmed | — | A | yes | MongoDB Realm Sync | vendor self-report | "a single engineer to spend one month"; table "Total 4 weeks" |
| V5-21 | §2.3.2: "MongoDB MBTC (A): 2 engineers, 10 weeks, abandoned; 'Bugs in post-processing could mask implementation bugs'" | confirmed | — | A | yes | MongoDB Server | vendor self-report | "implemented by two engineers in 10 weeks"; "abandoned the project after 10 weeks"; §6 quote |
| V5-22 | §2.3.1: "Mocket … 9 bugs in Xraft, Raft-java, ZooKeeper, including 2 in the official Raft TLA+ spec. Mapping annotations 134–152 LOC" | corrected (wording) | "7 implementation bugs (3 previously unknown, 4 known) plus 2 spec bugs in the official Raft TLA+ spec" | A (EuroSys '23) | yes | 3 Java systems | tool authors | §1: "we find 7 bugs … Besides, we find that 2 inconsistencies … are caused by specification bugs"; Table 1: 151/152/134 |
| V5-23 | §2.3.1: "Remix, EuroSys 2025 … 6 severe ZooKeeper bugs … 'The conformance checking is unsound … We only check safety' … Within 40 person-hours" | confirmed | — | A | yes | ZooKeeper | tool authors | Abstract "six severe bugs"; §3.5 "Limitation. The conformance checking is unsound"; §5 "within 40 person-hours" |
| V5-24 | §2.3.2: Cirstea "'in all cases' found unmatched executions. 'Too imprecise logs may even lead to erroneous traces being accepted.'" | confirmed | — | A-pre (venue not checked) | yes | 6 case studies | tool authors (TLC maintainers) | §5 "In all cases, trace validation quickly identified…"; §6 "too imprecise logs …" |
| V5-25 | §2.3.2: CCF "6 bugs …; first consensus trace spec about 2 engineer-months, later consistency spec about 1 engineer-week; DFS under 1 s vs about 1 h with BFS" | confirmed | add "2 months included building TLC support" | A/A-pre (venue not checked) | yes | CCF, 63 kLoC | vendor self-report | §6.2.2 "approximately two engineer-months, spread over four months"; "approximately one engineer-week"; DFS vs "about an hour with BFS" |
| V5-26 | §2.3.2: "TraceLink, OOPSLA 2025 … 9 bugs … fixes 'did not change the outcome of model checking'" | confirmed | — | A (PACMPL 9 OOPSLA2) | yes | dqueue, locksvc, raftkvs | tool authors | Abstract "9 previously undetected"; §9 "fixing those inaccuracies did not change the out[come]" |
| V5-27 | §2.3.2: Cedar "Lean model 1,673 LOC vs Rust production 15,693. DRT + PBT found 21 bugs, proofs 4 more. Each target fuzzed 6 h/day on 4 vCPU. DRT missed a non-termination bug" | confirmed | — | A (FSE Companion 2024) | yes | Cedar | vendor self-report | Table 1 "Total 1673 5714 15693…"; §4.3 "uncovered 21 bugs"; "4 vCPUs … 6 hours"; "did not discover the non-termination bug" |
| V5-28 | §2.3.2: "Generator bias: 35.5% of `when` conditions were boolean literals, cut to 9.7% with a new generator" | corrected (nuance) | "…; an added expression generator produced 9.7% boolean literals" | A | yes | Cedar DRT | vendor self-report | §4.3 "35.5% … type-directed ABAC policy generator"; "we added a new input generator … only 9.7%" |
| V5-29 | §2.3.2: Cedar string-size DRT failure "led to dropping a language feature" | confirmed | — | A | yes | Cedar | vendor self-report | §4.3 "We eventually dropped this feature" |
| V5-30 | §2.3.1: "Vikram et al. (A-pre): n = 40 API methods; valid and sound PBT in 2.4 samples; best model covered 21% of documented properties" | confirmed | — | A-pre | yes | 40 Python library API methods | authors' own metric | Abstract: "40 Python … 2.4 samples … 21% of properties extractable from API documentation" |
| V5-31 | §2.3.1: "Agentic PBT (A-workshop): 100 packages, 56% of n = 50 sampled reports valid, $9.93 per valid bug" | confirmed (strength caveat) | add "n = 50 from the top 80% by LLM rubric score; κ = 0.31; authors call $9.93 an upper bound" | A-workshop (NeurIPS 2025 DL4Code) | yes | 100 Python packages | vendor-affiliated (Anthropic; Hypothesis maintainer) | §3 "randomly sampled n = 50 bug reports from the top 80% by score"; §4 "$9.93/valid bug. This is an upper bound" |
| V5-32 | §2.3.3: "Leveson et al. 1990 TSE (A): 24 students; spec-only self-checks found 19% of detected faults, and only 4 of 34 effective checks (12%) came from the spec alone" | confirmed (strength caveat) | add the authors' caveat and the order confound | A | yes | 24 graduate students, LIP | none | p. 436: "Nineteen % … 43 % … 38%"; "Only 12% (4 out of 34)"; "inappropriate (and even misleading) to claim that checks of one type are more effective" |
| V5-33 | §2.3.3: "Zhao et al. ISSTA 2026 (A): 233 Defects4J defects, 13 LLMs … 3.84% misguided vs 0.46% …; effective 2.98% vs 8.51% … 104.15 → 186.77" | confirmed | — | A (PACMSE 3 ISSTA) | yes | 318 focal methods, 233 defects | none | §RQ1 "137.69 misguided tests (3.84%) … 16.46 (0.46%)"; "304.08 (8.51%)"; mitigation "from 104.15 to 186.77" |
| V5-34 | §2.3.3: "Konstantinou et al. (A-pre): accuracy drops on buggy code, e.g. 43.02% → 35.72%" | confirmed | — | A-pre | yes | 24 Java repos | none | Table row "MUT + TP 43.02% 35.72%" |
| V5-35 | §2.3.3: "Mathews & Nagappan (A-pre): tools that keep only passing tests discard bug-revealing ones" | confirmed | — | A-pre | yes | 287 buggy Python programs | none | §IV: "both CodiumAI and CoverUp reject such tests … 470 and 400 such tests being discarded" |
| V5-36 | §2.3.3: "TiCoder, IEEE TSE 2024 (A): n = 15 … with an idealised oracle proxy, +45.97% pass@1 within 5 interactions" | confirmed | — | A | yes | 15 programmers; MBPP/HumanEval | tool authors | Abstract "15 programmers … idealized proxy … 45.97%" |
| V5-37 | §2.3.4: Wasm `either` and NaN patterns; relaxed SIMD "fixed projection" | confirmed | — | B | yes | official docs | none | README l. 478 "( either <result_pat>+ ) ;; alternative results"; Overview l. 69 |
| V5-38 | §2.3.4: sqllogictest `rowsort`/`valuesort`, `skipif`/`onlyif` | confirmed | — | B | yes | docs mirror | none | about.wiki l. 173–182, 229–230 |
| V5-39 | §2.3.4: "JSON Schema separates `optional/` tests" | confirmed | — | B | yes | README | none | l. 87 |
| V5-40 | §2.3.4: "POSIX (IEEE 1003.3) has the verdicts UNSUPPORTED and UNRESOLVED" | confirmed | — | B | yes | LTP HOWTO | none | "taken from IEEE … (IEEE 1003.3-1991)"; PTS_UNRESOLVED, PTS_UNSUPPORTED |
| V5-41 | §2.3.4: "NonDex … found 60 open-source and 110 student bugs (A-workshop; human-only)" | confirmed (second-hand) | "as reported by the tool authors from their ICST 2016 paper" | A-workshop | yes | Java library underdetermined specs | tool authors | Abstract/§1: "we found 60 bugs in open-source projects and 110 bugs in student homework submissions" |
| V5-42 | §2.3.4: "PatchDiff (ICSE 2026, A) … 29.6% … 27.3% … inflated by 6.4 points" | confirmed | — | A | yes | 3 agents, SWE-bench Verified | tool authors (judging third-party agents) | Abstract/§1: "29.6% … 27.3% … 6.4 absolute percent points" |
| V5-43 | §2.4: "LiSSA (A) reached best F1 of roughly 0.25–0.53 on five requirement → code benchmarks … 'to be applicable in practice'" | confirmed (nuance) | add "not better than the best IR baseline on every benchmark (eTour FTLR_OPT .548)" | A (ICSE 2025) | yes | 5 benchmarks, GPT-4o | tool authors | Table III best F1 .423/.526/.290/.273/.254; abstract quote |
| V5-44 | §2.4: "IronSpec, OSDI 2024 (A): 14 specs; 10 author-confirmed spec bugs in 6 real systems; 13 of 61 surviving mutants were intended weaknesses; mutation runs 'only if the system has a passing proof'; 3 s to 80–191 min; STP suites take hours to days" | confirmed | — | A | yes | 14 specs | tool authors | §1 "ten specification bugs across all six real-world verified systems"; Table 3 alive column sums to 61, times 3 s–191 min; §6 "we consider 13 to be …"; "a few hours to multiple days" |
| V5-45 | §2.4: "MutDafny (A-pre): 794 programs, 112,810 mutants; 284 survivors reviewed: 77 weak-spec, 157 equivalent, 50 inconclusive; 5 weak specs …" | confirmed for v1; corrected for v2 | "v2: 118,458 mutants, 30,459 survivors, average mutation score 82% (v1: 112,810; 27.94%; 79%)" | A-pre | yes (v1 + v2) | 794 Dafny programs | tool authors | v1 Table "Total 112,810 … 31,515 (27.94%)"; v2 §6.3 "a total of 118,458 mutants", "From the 30,459 surviving mutants" |
| V5-46 | §2.4: "Jovanovic … FormaliSE 2025 (A): 25,180 … reproduce only 10.96% (17.72%) … detect 91.78% (95.79%)" | confirmed | — | A | yes | Alloy4Fun, novices | partial: Sullivan co-authored μAlloy | Tables: "TOTAL 25180 2760 10.96 4462 17.72"; "TOTAL 25180 23111 91.78 24119 95.79" |
| V5-47 | §2.4: "Google, about 15 M mutants over 6 years: mutants coupled to real high-priority faults, and developers wrote more and stronger tests (A)" | confirmed | — | A (ICSE-SEIP 2021) | yes | Google code review | vendor self-report | Abstract: "15 million mutants … mutants are indeed coupled with real faults"; "six years" |
| V5-48 | §2.4: "LLM-generated mutants: Wang et al. TOSEM 2025 (A): 851 real Java bugs; 76.47% vs 44.15%" | confirmed | — | A | yes | Defects4J + ConDefects | none (evaluates others' tools) | Abstract |
| V5-49 | §2.4: "Meta ACH (A): 9,095 mutants, 571 tests, 73% accepted; LLM equivalent-mutant detector P 0.79 / R 0.47" | corrected (nuance) | "73% of the tests reviewed by engineers in test-a-thons were accepted" | A (FSE Companion 2025, per notes) | yes | 10,795 Kotlin classes | vendor self-report, tool authors | Abstract: "test-a-thons where engineers accepted 73% of its tests"; §1 "acceptance rate of 73% from the engineers who reviewed them" |
| V5-50 | §2.4: "Just et al.: 73% of 357 real faults coupled to mutants and 17% to none" | confirmed | — | A | yes | 5 Java programs | partial (Major author) | §1 bullets: "for 73% of real faults"; "17% of real faults are not coupled" |
| V5-51 | §2.4: "Strong mutation had the highest fault revelation of four criteria, once the clean-program assumption is avoided (Chekam et al., A)" | confirmed | — | A | yes | CoREBench | none | Abstract: "strong mutation testing has the highest fault revelation" |
| V5-52 | §2.4: "Hughes (A; human-only): BST with 8 planted bugs, validity properties missed 5/8; model-based properties found the union bug in 8.4 tests vs 50; key absent in 79.2% of a million tests" | confirmed | — | A | yes | 1 data structure, 8 bugs | tool author (QuickCheck) | §6: "Validity properties miss many bugs (five of eight)"; "50 tests on average, while prop UnionModel fails after only 8.4 tests" |
| V5-53 | §2.4: "Goldstein et al. (A; 30 interviews at one firm): mutation 7/30, example inspection 8/30, code coverage 2/30" | confirmed | — | A (ICSE 2024) | yes | Jane Street | none | §5: "Mutation Testing (7/30) … Example Inspection (8/30) … Code Coverage (2/30)" |
| V5-54 | §2.4: OFT `ORPHANED`, `OUTDATED`, `AMBIGUOUS`, quiet mode; Doorstop suspect links, "exits 1 on failure" | confirmed (exit code unverifiable here) | — | B | yes (docs/source) | tool docs | none | LinkStatus.java l. 20–32; CLI doc "quiet - no output (in case only the return code is used)"; Doorstop validation.md suspect links; exit code not in that doc |
| V5-55 | §4 Pipeline B: "Bosch reported roughly 70/30 as its comparison point" | confirmed (caveat) | add "tool-author self-report, ongoing case study, part of the results unclassified" | A | yes | Bosch | tool authors | as V5-03 |
| V5-56 | §4 Pipeline B: "Solver UNKNOWN or timeouts (Bosch: 18 timeouts in one set; FRET: 'unknown' on non-linear arithmetic)" | confirmed | — | A | yes | Bosch Dev. 8; FRET EB | tool authors | Table II; FRET "returned 'unknown' due to non-linearities" |
| V5-57 | §2.2 Witnesses: "No source measures the defect yield per additional implementation. 'Two' is a convention." | confirmed (as absence, within sources read) | — | — | yes (W3C, RFC, phases, Watt) | — | — | No yield data in any of the four |

---

## Notes

**Baseline quote before the Vericoding qualification.** The earlier brief §3 says verbatim, under "Agent evidence:": "agents conform well to fixed, machine-checked specs (Vericoding, DafnyBench);". The earlier report's §3 qualification contradicts the implicit assumption that the fixed specs were adequate. V5's correction (V5-15) does not challenge the baseline sentence itself: agents do conform to the fixed specs. It corrects the qualification's evidence. The weak or poorly translated specs (≈9 % + 15 % of successes) are reported across Dafny, Verus *and* Lean, not only Verus. The qualification therefore stands and applies to the Dafny half of the baseline too. The "found Dafny clean" carve-out should be removed.

**Baseline quote before the witness qualification.** The earlier brief §3 lists, under "Seeds proposed there but not evidenced": "at least two *witness* implementations with different profile values as a satisfiability argument;". The earlier report replaces this with a coverage criterion (*Inference*). V5 finds no new full-text evidence for or against that replacement: W3C, RFC 6410, the Wasm phases and Watt give no yield per witness. The supporting clause that Wasm errors "survived engines and the reference interpreter" is not in Watt (V5-16). The replacement therefore remains *Inference* and is not a §3 challenge.

**Notes-vs-report distortion pattern.**
1. Report errors inherited from wrong notes: Bosch minima (V5-02, V5-05); Watt's "survived engines" (V5-16); MutDafny's "3 of 5 LLM" (V5-18); the trained-authors framing in the T2 notes (feeding V5-11 and V5-12).
2. Distortion introduced by the report writer: Vericoding "[Verus]" (V5-15), added to a quote the notes had already truncated.
3. Grade error in both notes and report: SAT-LLM A-pre (V5-07).
4. Simplifications that drop a stated denominator or caveat: Mocket, Cedar 9.7 %, Meta ACH 73 %, Maaz upper bound, Frama-C spurious failures, Leveson caveat.

**Notes-level errors not carried into the report.** T2 notes §5 say "Bosch: 1 to 6 vacuous requirements per set". Only Dev. 8–10 had any (6, 2, 1); seven sets had none. The T2 notes also say "4 to 109 rt-inconsistencies per device set"; the true range is 0–109 (Dev. 3 and Dev. 10 have "no"). The T3b and T3a notes' Mathews figures use different denominators.

**Versioning.** MutDafny v2 (current arXiv) changed the totals. The report cited the v1 HTML. Both versions agree on 284 / 77 / 157 / 5.

**What V5 did not do.**
- It did not re-check the T2–T4 items listed under Q1 Gaps.
- It did not verify the venues of DMN, Cirstea or CCF (assigned elsewhere). It did not query DBLP, which returned a bot check; Crossref and PDF headers were used instead.
- It did not re-check the T1 sources behind §3's faithfulness column or Pipelines A and C.
- It ran no trial.

## Self-check
- **Scope reading.** "Skip sources assigned to others" was read as also skipping the Cedar §3 challenge and Porcupine cost, though both sit in §2.3. Cedar *figures* (V5-27 to V5-29) were still checked, because the brief lists "Cedar 21 bugs and 35.5% trivial". If that list was meant to exclude all Cedar material, V5-27 to V5-29 duplicate another verifier's work.
- **"Direct" transfer label.** POSIX, sqllogictest, JSON Schema and NonDex were treated as *direct* (library or API behaviour specs). Cedar (an authorization-language library) and the MongoDB merge function were treated as *analogous*. A stricter or looser reading of "library/API behaviour specs" would move them.
- **SAT-LLM track.** The grade A rests on Crossref placing it in the ASE 2024 proceedings. That it is a short or NIER paper is inferred from its length and wording; the track was not confirmed.
- **Maoz–Ringert, "40 under strict semantics".** This is derived as 60 − 20 from the paper's Fig. 5 description ("20 specifications in the dotted middle box prevent forced assumption violations"). The paper does not print "40".
- **MutDafny, "only 1 new".** Read from "two of the weaknesses had previously been detected by Endres et al., the third one being a new discovery". The bst4copy weakness may also be new; its novelty is not stated.
- **Bosch minima.** These depend on reading Table II from a two-column layout extraction. Dev. 1's "26 … 48s" row was read from the right-hand table and checked against the column header order (ID, R., RT., Vac., rt-inc., TO, Time).
- **LiSSA best F1.** Values were taken from Table III's GPT-4o rows; layout extraction could misalign columns. The values match the T4 notes independently.
- **Frama-C "all spurious".** Applies to the JCVM snapshot reported in Fig. 5 only. The paper also says smoke tests "effectively guided the initial steps of verification" without counts.
