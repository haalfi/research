# V4: Remaining verification-debt items (brief §3 items 5–8)

Scope: the verification brief §3 items 5 (NASA IV&V ROI), 6 (DTest, NFM 2023), 7 (AWS "Systems Correctness Practices", CACM 2025), and 8 (the rest of the earlier report's §5 debt table, excluding the items assigned to other researchers). Downloads are in the scratchpad subfolder `v4/`. Earlier report = `reports/Spec faithfulness and enforcement.md`. No §3 challenge or qualification is raised in this file (see Notes).

## 5. NASA IV&V return-on-investment data

### Takeaway
None of the IV&V ROI sources this run could read measures the effect of *independently deriving tests*. They count errors that IV&V found, or they model cost savings from assumed cost-to-fix multipliers. The Dabney ROI papers themselves are [unreachable]. No conclusion of the earlier report changes. The earlier notes' gap ("No measured data found on IV&V or Cleanroom separating the independence effect from the rest of the method") stands.

### Cited Findings
- **Neal, McCaugherty, Joshi, Callahan, "A case study of IV&V cost effectiveness"** (NASA/WVU, NTRS 19980027712; full text read as NTRS OCR text). Setting: IV&V of the Space Shuttle Day-of-Launch I-Load Update (DoLILU) project. The study analysed 100 of 109 IV&V issue reports (DITRs). "Out of the 695 errors detected, about 15% of them were found in phase 1, 6% in phase 2, 20% in phase 3, 3% in phase 5, and over half (57%) were found in phase 4." The study counts only errors found by IV&V: "the errors reported here are only those found by IV&V." Its stated limitations: "It was not possible to determine actual costs … the savings from finding errors earlier in the life cycle are based on previous studies instead of being based on empirical data from this study", and "This was a first attempt". — [NTRS 19980027712](https://ntrs.nasa.gov/api/citations/19980027712/downloads/19980027712.txt)
- **Hunt (Dulos Inc.), "An approach to Return on Investment (ROI) for Independent Verification and Validation"**, NASA IV&V workshop slides, 2012 (full text read; grade C). The slides state: "NASA PAE 2008 Study show ROI values from 1.5 to 12; but says, 'There is a wide range of opinions and studies regarding the cost effectiveness of IV&V. The study team was unable to identify a common methodology for calculating ROI…'". They also note that "Most analyses of ROI assume that defects would not have been found until fielding – therefore they apply the 100 rule". They cite the Dabney/Barber/Ohi COCOMO-II paper (2006) and Rogers et al. (NASA, 2000) as sources of the "2 to 10 times" ROI figure. — [NASA slides](https://www.nasa.gov/wp-content/uploads/2016/10/1-4a-ivv_conference_bob_hunt_dulos_kalman.pdf)
- **"Adding Value to the Software Development Process: A Study in Independent Verification and Validation"** (Virginia Tech CS technical report, 1998, funded by NASA Langley). Abstract only: the PostScript full text downloaded but its font encoding could not be decoded, so the full text is [unreachable]. Per the abstract, two development groups worked from the same requirements, and only one had an IV&V contingent. That group "detected errors earlier", "required significantly less time to remove those faults", and produced a system that was "substantially more robust". n and effect sizes are unverifiable. — [VTechWorks](https://vtechworks.lib.vt.edu/items/844d3189-cfc3-45d5-9b43-88fb49764472)
- **Dabney, Barber, Ohi**, "Estimating direct return on investment of independent verification and validation" (IASTED SEA 2004, pp. 394–399), and the COCOMO-II version (2006): **[unreachable]**. Only bibliographic records were found (researchr, isc.ac). NTRS returned no hit for "Dabney" or "COCOMO IV&V". — [researchr](https://researchr.org/publication/DabneyBO04)

### Inferences
- *Inference*: IV&V ROI figures (1.5–12×, 2–10×) are cost models built on assumed fix-cost multipliers. Even where they are measured (DoLILU), they count what one independent team found, with no counterfactual and no separation of "independent derivation" from "extra reviewers, earlier review". They cannot support or refute the earlier report's claim that expectation tests must be derived independently of the spec. The report already rests that claim on Leveson et al. 1990, Arm/Reid 2017 and JEST, and none of that changes.
- *Inference*: the VT two-group design is the only IV&V study found with a control group. It is human-only, and its full text could not be decoded.

### Gaps
- The Dabney 2004/2006 full texts, the Rogers et al. 2000 NASA ROI case study, the NASA PAE 2008 study, and the VT 1998 full text were not obtained.

## 6. Fedchin et al., NFM 2023 (DTest), and later `generate-tests` evaluations

### Takeaway
The full text was obtained through the cdn.amazon.science mirror. DTest is **implementation-coverage-directed**: it injects trap assertions into Boogie blocks of the *implementation*. Postconditions are used as runtime oracles (`expect`). The earlier report's phrase "Statement/path coverage of the contract" is therefore wrong and needs correcting. A 2026 follow-up, DSpec2Test (A-pre, by the tool's authors), adds a spec-driven black-box mode to `dafny generate-tests`. On 131 killable implementation mutants it kills 93.9%, against 82.4% for DTest's block mode. This is the first measured evidence that clause-derived Dafny tests complement implementation-derived ones. It supports, and does not change, §2.3.1.

### Cited Findings
- DTest "repurposes the Dafny verifier to automatically generate DUnit test cases that achieve desired coverage". It "systematically injects trivially failing trap assertions (meaning assert false) into the Boogie code" and "converts method postconditions into runtime oracles" (§1). — [Fedchin et al., NFM 2023, author/AWS copy](https://cdn.amazon.science/b9/d4/eeb4fe1a47609f75956dd6fbc0c6/a-toolkit-for-automated-testing-of-dafny.pdf)
- Evaluation subjects (§5): the Dafny utilities library DUTIL (1,382 LOC) and the Dafny part of the AWS Encryption SDK (ESDK, 4,596 LOC). "DTest took 158 minutes to generate 918 tests for the 436 methods". Coverage on the compiled C# (Table 1): DUTIL 79% statement / 84% branch; ESDK 62% statement / 58% branch. ESDK developers target "80% statement and 35% branch coverage for their manually written unit tests". — same source
- Oracle strength (§5.1): "Of the 918 tests … 85 are unreliable"; "Overall, half of the generated tests have no return value check due to absence of postconditions". The only behavioural finding reported is a test that ran indefinitely, which uncovered "an external library behaving differently from the developers' expectations". — same source
- Test-suite size (§5.2, Table 2, 9 methods): the greedy approach is "within two tests of minimal for four of the methods, and it never generates more than three times the minimal number of tests". — same source
- Target languages: the evaluation compiles to C# only. There is no Python target and no agent involvement. Of the 10 authors, 5 are AWS employees, so the paper is tool authors evaluating their own tool.
- **DSpec2Test** (Pinto, Silva, Faria, Mendes; arXiv 2609.29713, Aug 2026; DOI 10.1145/3832783.3834629, venue not verified; A-pre; full text read). It "extends Dafny's generate-tests command with a new black-box mode based on Disjunctive Normal Form (DNF) equivalence class partitioning and optional Boundary Value Analysis", deriving tests "without considering implementation details". It describes DTest as implementation-based: "DTest targets code coverage".
  - Setting: 20 DafnyBench programs, 17 supported by both modes; MutDafny implementation mutants; Dafny 4.11.0.
  - Of 170 mutants, after removing 22 non-compiling and 17 equivalent ones, 131 were "realistically-killable".
  - Results (Table 2): "Spec_bva kills 123 (93.9%), Block kills 108 (82.4%); the union covers 125 (95.4%), with Spec_bva uniquely killing 17, Block uniquely killing 2, and only 6 mutants killed by neither tool". Timeouts were credited as kills.
  - Neither mode supports mutable state (arrays, class fields).
  - The authors evaluate their own tool. — [arXiv 2609.29713](https://arxiv.org/pdf/2609.29713v1)

### Inferences
- *Inference*: the earlier report's DTest row should read: catches "uncaught runtime errors and postcondition violations on inputs that reach implementation blocks or branches". DTest gives no coverage *of the contract*, and for methods without postconditions it gives no oracle at all. "No Dafny → Python bridge evidence" stays true.
- *Inference (analogous)*: DSpec2Test is direct evidence for the report's "spec-enforcing tests derived from the spec's clauses" family in a Dafny setting. Clause-partition tests killed 17 implementation mutants that implementation-coverage tests missed. The mutants are implementation faults, not spec misreadings, so the figures say nothing about faithfulness to prose.

### Gaps
- The POPL 2024 Dafny-workshop "Dafny Test Generation" talk and the Fedchin 2026 Tufts PhD thesis were not read. The thesis PDF link was found but not fetched, for time.

## 7. AWS "Systems Correctness Practices at Amazon Web Services" (Brooker & Desai)

### Takeaway
Still **[unreachable]**. queue.acm.org, cacm.acm.org and dl.acm.org (DOIs 10.1145/3712057 and 10.1145/3729175) all returned 403. web.archive.org is not fetchable, and no arXiv copy or brooker.co.za copy exists. The only primary text read is Desai's one-page FMCAD 2025 keynote abstract (B, vendor). It confirms the list of practices but gives no figures and no ordering. The earlier report's "AWS's ordering (CACM 2025) is [unreachable]" remains correct.

### Cited Findings
- FMCAD 2025 talk abstract (Desai, AWS; CC-BY; full text read, 1 page): "AWS has adopted model checking, fuzzing, property-based testing, fault-injection testing, deterministic simulation, event-based simulation, and runtime validation of execution traces. Formal methods have been an important part of the development process – perhaps most importantly, formal specifications as oracles or monitors that provide the correct answers for many of AWS's testing practices." — [reposiTUm FMCAD 2025](https://repositum.tuwien.at/handle/20.500.12708/219530)
- Bibliographic: per a library catalogue extract, the article appeared in CACM 68(6), June 2025, pp. 38–42. This is a search lead, not verified against the full text. — [hebis record](https://karla.hds.hebis.de/EdsRecord/buh%252C185687583)
- Search extracts (leads only, not verified) say the article describes deterministic simulation as running a distributed system on a single-threaded simulator that controls scheduling, timing and message order; names the open-sourced shuttle and turmoil projects; and says PObserve (2023) validates logs against P specs in testing and production.

### Inferences
- *Inference*: the abstract's "formal specifications as oracles or monitors" matches the report's use of a spec-derived reference model as oracle. As a vendor talk abstract it carries no measured data, so no claim changes.

### Gaps
- Article full text, any figures, and any gate ordering.

## 8. Remaining §5 debt-table rows

### Takeaway
Of the 17 row groups attempted, 7 were obtained in full or through a replacement full text: Katis CAV 2022, Leino–Wüstholz CAV 2015, Staats/Whalen/Rajan/Heimdahl (UFC follow-up), Huo & Clause (via the author's dissertation), Watt et al. FM 2021, Mashkoor & Jacquot (HAL), and Melnik & Maurer 2007 as a replacement for Melnik 2006. Two of them correct the earlier notes:
- **UFC coverage**: requirements coverage and antecedent coverage suites found *fewer* faults than random suites of the same size; UFC beat random in only 3 of 4 systems.
- **Watt et al. FM 2021**: it is *not* a dual-formalisation cross-check.

No Kernsatz or §4 conclusion is overturned. The UFC result strengthens §2.6(b) ("strong for coverage targets") and qualifies the G7 clause-coverage gate. Ten row groups remain unreachable (listed under Gaps).

### Cited Findings
- **Katis, Mavridou, Giannakopoulou, Pressburger, Schumann, CAV 2022** (A; full text via Springer open access). Three case studies, FSM (13 requirements), Lift Plus Cruise (11) and Infusion Manager; no timing or user study.
  - Gacek et al. had attributed the Infusion Manager unrealizability to G1 vs G7. "However, FRET's diagnostic procedure provided a different answer, identifying 8 minimal unrealizable cores. Furthermore, the assumed conflict between requirements G1 and G7 does not really exist… a realization still exists" (§6).
  - LPC: realizability checking "yielded non-sensical counterexamples". The cause was a `pre` operator "undefined at the initial state", which was fixed with new operators (§6.1).
  - "a single execution trace is not enough to truly understand interactions between requirements", hence simulation of conflicts (§5). — [Springer OA](https://link.springer.com/content/pdf/10.1007/978-3-031-13188-2_24.pdf)
- **Leino & Wüstholz, CAV 2015** (A; author copy). Eight unscripted expert Dafny IDE sessions, "up to 255 individual program snapshots".
  - Fig. 5, session 0: 4,395.3 s with no caching, 315.3 s with basic caching, 277.5 s with fine-grained caching.
  - Fine-grained caching was "42 % faster for session 3 and on average 17 % faster compared to the basic caching". Basic caching gave "more than an order of magnitude for many sessions" (§4). — [MSR PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/krml245.pdf)
- **Whalen, Rajan, Heimdahl, Miller, ISSTA 2006**: the original is [unreachable] (UMN conservancy 403). The replacement full text is the follow-up **Staats, Whalen, Rajan, Heimdahl, "Coverage Metrics for Requirements-Based Testing: Evaluation of Effectiveness"** (UMN report; A-pre, not peer-reviewed).
  - Setting: four industrial avionics systems (Simulink → Lustre), 600 mutants each, auto-generated suites, 15,000 combinations.
  - "The majority of test suites satisfying a coverage metric provide worse fault finding than random test suites of similar size, and thus H1 is not statistically supported."
  - "test suites satisfying UFC coverage outperform random test suites 75% of the time (3 of 4 case examples)".
  - "random test suites always outperform test suites satisfying requirements and antecedent coverage with statistical significance".
  - Table 1, DWM 2: UFC vs random −42.0% (§5–6). — [UMN conservancy](https://conservancy.umn.edu/server/api/core/bitstreams/a533c3cb-0812-4e95-b113-7d221af01318/content). The Rajan PhD thesis with the metric definitions was downloaded but not read: [scispace copy](https://scispace.com/pdf/coverage-metrics-for-requirements-based-testing-f7013xhwt5.pdf).
- **Huo & Clause, FSE 2014**: the paper itself is [unreachable] (UT Dallas host TLS chain error; WebFetch 503). The figures were confirmed from **Huo's PhD dissertation** (Univ. of Delaware 2017, Ch. 3, Table 3.1).
  - Setting: 20 Java applications, 13,609 tests, 4,718 executable.
  - Brittle assertions: 405 reports, 164 "TP". Unused inputs: 3,060 reports, 1,618 "TP". "TP" means reports that survive the tool's automated mutation-based filter (§3.7), not manual confirmation.
  - Quote: "In total, it detected 164 tests that contain at least one brittle assertion and 1,618 tests that contain unused inputs." — [UDSpace](https://udspace.udel.edu/items/751e4abc-141b-4795-9bbe-4d56cc8fa965)
- **Watt, Rao, Pichon-Pharabod, Bodin, Gardner, FM 2021** (A; author copy).
  - It presents two mechanisations, Isabelle and Coq, each proving type soundness. It reports **no** cross-comparison of the two and no discrepancies found between them.
  - Spec bugs are credited only to Watt's earlier single mechanisation: it "found bugs in the original specification, fixed before its publication".
  - The Isabelle interpreter passes the official suite of "~17,810 tests". — [author PDF](https://www.cl.cam.ac.uk/~jp622/two_wasm.pdf)
- **Mashkoor & Jacquot, REJ 2017** (A; HAL submitted version, Jan 2016). Three Event-B case studies: land transport, landing gear, platooning.
  - The evaluation (§VII) is qualitative, against criteria from Breuer et al. (coverage, efficiency, sophistication) and interactivity, transparency and operational equivalence. It gives no detection rates.
  - One reported finding: "The major breakthrough of the animation activity was the discovery of oscillation in the platoon … an undesirable feature." — [HAL hal-01262115](https://hal.science/hal-01262115/document)
- **Melnik, Maurer, Chiasson, Agile 2006**: [unreachable]. Replacement: **Melnik & Maurer, XP 2007, "Multiple perspectives on executable acceptance test-driven development"** (open access; A-workshop short paper; full text read).
  - Setting: one industrial project, three interviewees.
  - "about 40% of all FIT test pages were written by the Customer, 30% by developers, and the remaining 30% by testers".
  - The Customer: "in practice, it was best if the Customer wrote acceptance tests. This is related to the fact that going from a general description to a test has some fluidity in interpretation."
  - Writing FIT tests "helped the Customer and the team to discover a lot of missing pieces or inconsistencies in a story". — [scispace copy](https://scispace.com/pdf/multiple-perspectives-on-executable-acceptance-test-driven-2gjlzftall.pdf)
- **Finney 1996**: abstract only (Greenwich eprint, no file). "students already trained in discrete mathematics and the specification notation performed very poorly". No n. — [GALA](https://gala.gre.ac.uk/id/eprint/25)
- **Snook & Harrison 2004**: abstract only. The Southampton thesis PDF returned 401 (restricted). — [eprints](https://eprints.soton.ac.uk/260170)

### Inferences
- *Inference (analogous)*: the UFC result supports the report's "coverage as necessary-condition gates, never as targets". It sharpens G7: "clause without spec test" (requirements coverage) is a presence check only. Auto-generated one-test-per-clause suites did worse than random tests of equal size. If clause coverage is used as an adequacy signal, it needs a UFC- or MC/DC-like per-condition criterion, plus the per-family mutant kill (G8).
- *Inference*: Katis et al. is a concrete instance of the brief's failure mode "consistency checks that passed but missed a contradiction", in reverse: a published human diagnosis of a conflict was wrong, and the tool's minimal cores corrected it. This supports the report's T2 core finding (minimal cores; realizability over plain SAT) as an anecdote, not as a rate.
- *Inference*: Watt et al. FM 2021 should not be cited as dual-formalisation evidence. Open question 2 (recall of dual formalisation) stays open.
- *Inference*: Leino–Wüstholz gives adjacent evidence for open question 7, on incremental *verification* cost, not *consistency* cost. Re-checking only affected entities cut IDE re-verification time by more than 10× in many sessions.

### Gaps (rows still unreachable after trying author copies)
- **Ricca et al. ICSE 2008 / IST 2009**: Ceccato paper paths 404, Sannio IRIS copy marked unavailable, ACM/Elsevier paywalls. The effort disagreement between the abstracts stays unresolved.
- **Black, Okun, Yesha ASE 2000; Ammann & Black**: UMBC and UNT-archive hosts fail TLS verification (incomplete chain), WebFetch returns 503, hissa.nist.gov returns 403.
- **van Lamsweerde, Darimont, Letier TSE 1998**: only 2-page course slides found.
- **Zave & Jackson TOSEM 1993**: no copy found; pamelazave.com returned 406.
- **Saarland fb14-96-06**: 403 again.
- **Hughes, AUTOSAR (ICSTW 2015), Dropbox (ICST 2016), "Experiences with QuickCheck" (2016)**: upenn TLS chain failure, WebFetch 503, Chalmers file endpoints 500.
- **Snook & Harrison 2004; Finney 1996**: abstracts only.
- **DO-178C secondary claims**: not attempted (standard is paywalled; out of time).
- **Dabney et al. ROI; AWS CACM 2025**: see §5 and §7.

## Verification log entries

| ID | Report location + verbatim claim | Verdict | Corrected text (if any) | Grade | Full text read | n and setting | Independence flag | Evidence (quote + page/section) |
|---|---|---|---|---|---|---|---|---|
| V4-01 | §5 debt table: "NASA IV&V ROI data \| T3 \| not retrieved" (no report claim rests on it; notes T3b: "No measured data found on IV&V or Cleanroom separating the independence effect") | confirmed (gap stands) | "IV&V ROI data retrieved in part: one NASA case study (DoLILU, 695 IV&V-found errors, no counterfactual, no cost data) and a 2012 summary (ROI 1.5–12, 'unable to identify a common methodology'); Dabney ROI papers [unreachable]. None isolates independent test derivation." | B (Neal et al.); C (Hunt slides) | yes (NTRS text; slides); VT 1998 abstract only | 1 project, 100 DITRs, 695 errors (Shuttle DoLILU); human-only | none (NASA/WVU IV&V staff evaluating own programme: partial) | Neal et al. Conclusion: "savings … are based on previous studies instead of being based on empirical data from this study"; Hunt slide 7: "unable to identify a common methodology for calculating ROI" |
| V4-02 | §5: "Dabney ROI" (brief item 5) | unverifiable | — | — | no [unreachable] | — | — | Only bibliographic records (researchr DabneyBO04); NTRS search empty |
| V4-03 | §2.3.1 row "Dafny test generation (DTest) \| NFM 2023 paper [unreachable]; author page (B): coverage-directed inputs … \| Statement/path coverage of the contract \| No oracle beyond the contract" | corrected | "DTest (NFM 2023, A; full text): verifier-driven inputs reaching *implementation* blocks/branches; postconditions compiled to runtime `expect` oracles; half of 918 generated tests had no return-value check (no postcondition). DUTIL 79%/84%, ESDK 62%/58% statement/branch on C#; 158 min for 436 methods. Catches runtime errors and postcondition violations; misses anything the contract does not state; no Python target." | A | yes | 2 Dafny projects (1,382 + 4,596 LOC), 436 methods, 918 tests; C# only; no agents | tool authors evaluating own tool (Tufts/AWS/BYU) | §1: "converts method postconditions into runtime oracles"; §5.1 Table 1; §5.1: "half of the generated tests have no return value check due to absence of postconditions" |
| V4-04 | §2.3.1 DTest row, "Agents: None found" | confirmed | — | A | yes | as V4-03 | tool authors | No LLM or agent use in the paper |
| V4-05 | (new, replacement source for brief item 6 "later generate-tests evaluation") | new evidence (supports §2.3.1) | "DSpec2Test (A-pre, 2026) adds a spec-driven black-box mode to `dafny generate-tests`: 93.9% vs 82.4% (DTest Block) kills on 131 killable MutDafny mutants; union 95.4%; 17 unique kills by the spec mode." | A-pre (venue of DOI 10.1145/3832783.3834629 not verified) | yes | 17 DafnyBench programs, 131 killable implementation mutants; no agents | tool authors evaluating own tool | §3.2 Table 2: "Spec_bva kills 123 (93.9%), Block kills 108 (82.4%); the union covers 125 (95.4%)" |
| V4-06 | §2.4: "AWS's ordering (CACM 2025) is [unreachable]"; §5 row "AWS 'Systems Correctness Practices' CACM 2025 \| [unreachable] (403)" | confirmed (still unreachable) | — | B (FMCAD talk abstract, vendor) | no for the article; yes for the 1-page abstract | — | vendor | FMCAD 2025 abstract: "formal specifications as oracles or monitors that provide the correct answers for many of AWS's testing practices"; queue/cacm/dl.acm all 403 |
| V4-07 | §5 row "Katis et al. CAV 2022 (FRET diagnosis) \| T2 \| [unreachable]"; notes T2: abstract "visualization of conflicts … and simulation of counterexamples" | confirmed (now full text) + adds anecdote | add to §2.2: "FRET's minimal-core diagnosis overturned a published human attribution of unrealizability (8 minimal cores; the assumed G1–G7 conflict 'does not really exist')" | A | yes | 3 case studies (13, 11, n/a requirements); no timings, no user study; human-only | tool authors (NASA FRET team) | §6.2: "identifying 8 minimal unrealizable cores. Furthermore, the assumed conflict between requirements G1 and G7 does not really exist" |
| V4-08 | §5 row "Leino & Wüstholz CAV 2015 … \| T2 \| [unreachable]"; notes T2: "Dafny/Boogie re-verifies only code affected by an edit" | confirmed | — | A | yes | 8 recorded expert Dafny IDE sessions, 7–255 snapshots | tool authors | §4: "on average 17 % faster compared to the basic caching"; Fig. 5 session 0: 4,395.3 s → 315.3 s → 277.5 s |
| V4-09 | §5 row "Whalen et al. ISSTA 2006 + follow-up (UFC coverage) \| T4 \| [unreachable]"; notes T4: follow-up "reportedly found that only UFC 'was consistently a good measure of test suite adequacy'" | corrected | "Follow-up (Staats et al., UMN report, A-pre): auto-generated suites satisfying requirements or antecedent coverage found fewer faults than equal-size random suites (significant); UFC suites beat random in 3 of 4 avionics systems (DWM 2: −42%). ISSTA 2006 original still [unreachable]." | A-pre (report); ISSTA original A [unreachable] | yes (follow-up); no (ISSTA) | 4 industrial avionics systems, 600 mutants each, 25×25 resamples; human-only, auto-generated tests | tool/metric authors evaluating own metrics | §5.1: "random test suites always outperform test suites satisfying requirements and antecedent coverage with statistical significance"; Table 1 DWM 2 UFC:UFC-RAN −42.0% |
| V4-10 | §5 row "Huo & Clause FSE 2014 \| T3 \| [unreachable]"; notes T3b: "reportedly 164 tests with brittle assertions and 1,618 with unused inputs (secondary listing, unverified)" | confirmed (via author's dissertation; FSE text itself unreachable) | "164 tests with brittle assertions and 1,618 with unused inputs among 4,718 executable tests in 20 Java applications; 'TP' = reports surviving the automated filter, not manually confirmed" | A-pre (dissertation); FSE A [unreachable] | yes (dissertation Ch. 3) | 20 Java apps, 13,609 tests (4,718 executable); human-written tests | tool authors | Diss. §3.8.4: "In total, it detected 164 tests that contain at least one brittle assertion and 1,618 tests that contain unused inputs"; Table 3.1 |
| V4-11 | §5 row "Watt & Rao FM 2021 (two Wasm mechanisations) \| T2 \| [unreachable]"; notes T2: "would be direct evidence of dual formalisation cross-checking" | refuted (for the notes' expectation) | "Watt et al. FM 2021 presents two mechanisations (Isabelle, Coq), each with its own soundness proof; it reports no cross-comparison and no discrepancies; it is not dual-formalisation evidence." | A | yes | Wasm 1.0; Isabelle interpreter passes ~17,810 official tests | none | Abstract: earlier mechanisation "found bugs in the original specification"; §5: "~17,810 tests, which we pass without error"; no comparison section |
| V4-12 | §2.3.1 (Watt CPP 2018, earlier read): "mechanisation found errors that made the Wasm type system 'originally unsound'" | confirmed (consistent with FM 2021 abstract) | — | A | yes (FM 2021) | — | none | FM 2021 abstract: "found bugs in the original specification, fixed before its publication" |
| V4-13 | §5 row "Mashkoor & Jacquot REJ 2017 (ProB animation evaluation) \| T1 \| [unreachable]" | confirmed (now full text; no quantitative data) | "Evaluation is qualitative (criteria-based); 3 Event-B case studies; animation revealed one undesirable behaviour (platoon oscillation). No detection rates." | A (read as HAL submitted version) | yes | 3 case studies; human-only | tool/method authors | §VII criteria list; §VI-C: "discovery of oscillation in the platoon … an undesirable feature" |
| V4-14 | §5 row "Melnik et al. Agile 2006; Haugset & Stålhane \| T3 \| [unreachable] / not fetched" | unverifiable (2006); replacement read | "Melnik & Maurer XP 2007 (A-workshop): 1 project, 3 interviewees; customer wrote ~40% of FIT pages; writing FIT tests surfaced 'missing pieces or inconsistencies in a story'. No counts." | A-workshop | yes (2007); no (2006) | 1 industrial project, 3 respondents; human-only | none | §3: "going from a general description to a test has some fluidity in interpretation" |
| V4-15 | §5 row "Ricca et al. ICSE 2008; IST 2009 \| T1/T3 \| [unreachable] / abstract only; abstracts disagree on effort" | unverifiable | — | A (if confirmed) | no [unreachable] | — | — | Author paths 404; Sannio repository marks file unavailable |
| V4-16 | §5 row "Black, Okun, Yesha ASE 2000; Ammann & Black \| T4 \| [unreachable]" | unverifiable | — | A (if confirmed) | no [unreachable] | — | — | UMBC/UNT TLS chain failure; WebFetch 503; hissa 403 |
| V4-17 | §5 rows "van Lamsweerde, Darimont, Letier TSE 1998"; "Zave & Jackson TOSEM 1993"; "Saarland tech report fb14-96-06" | unverifiable | — | A / A / B (if confirmed) | no [unreachable] | — | — | No author copy found; Saarland 403 |
| V4-18 | §5 row "Hughes: AUTOSAR, Dropbox, 'Experiences with QuickCheck' \| T3 \| [unreachable]"; §2.3.1 "Hughes' AUTOSAR/Dropbox reports [unreachable]" | unverifiable | — | A (if confirmed) | no [unreachable] | — | — | upenn TLS failure; Chalmers file 500 |
| V4-19 | §2.6(a): "Snook & Harrison and Finney are [unreachable]" | confirmed (abstracts only) | — | A (if confirmed) | no (abstracts) | Finney: n not given | — | Finney abstract: "performed very poorly"; Snook thesis 401 |
| V4-20 | §5 row "DO-178C (RTCA) text …" | not attempted this run | — | — | no | — | — | Out of time; standard paywalled |

## Notes

- **No §3 challenge or qualification is raised.** Nothing in V4 contradicts a brief §3 baseline point. The closest contact is with the §3 checking-landscape and form-rule baseline. Quoted verbatim: "Form rule. Choose the checkable form by what a claim quantifies over: finite case split → table checked complete and disjoint …; value domain → executable oracle plus property tests". The UFC finding (V4-09) concerns coverage adequacy of tests over LTL requirements. It does not contradict the form rule, so it is recorded as evidence for §2.6(b) and G7, not as a §3 qualification.
- **Changes the corrected report should make:**
  1. Rewrite the DTest row (V4-03) and cite DSpec2Test as A-pre supporting evidence (V4-05).
  2. Add the UFC result to §2.4 "Coverage that fits" and §2.6(b) (V4-09). Suggested text: "Requirements-level coverage on LTL requirements: auto-generated suites satisfying requirements or antecedent coverage found fewer faults than random suites of the same size; UFC beat random in 3 of 4 avionics systems (Staats et al., A-pre). A one-test-per-clause gate is therefore a presence check, not an adequacy signal." Transfer: analogous.
  3. Add the Katis anecdote to §2.2 realizability (V4-07).
  4. Remove any suggestion that Watt et al. FM 2021 is dual-formalisation evidence (V4-11). The report itself only lists it as debt, so only the debt table changes.
  5. Move the debt rows now read (V4-07, -08, -09, -10, -11, -13, and -14 as a replacement) out of the unreachable table.
- **Kernsatz and §4:** none of the V4 items touches the Kernsatz claims. The IV&V data does not bear on "prose-derived oracles catch spec misreadings that spec-derived ones miss", which stays unmeasured. In Pipeline C, the UFC finding argues against using clause coverage alone as G7's adequacy criterion. The report already does not, because it pairs coverage with G8 mutant kills.
- **Agent applicability:** none of the V4 full texts measures agents (LLMs).
- **Transfer labels:**
  - DTest/DSpec2Test: *analogous* (Dafny per-call contracts, close to the brief's Dafny layer).
  - UFC: *analogous* (avionics reactive systems).
  - Huo & Clause: *analogous* (Java unit tests).
  - Katis: *analogous*.
  - IV&V: *analogous*, human-only, weak.

## Self-check

- **AWS article:** I may have conflated the ACM Queue and CACM versions; both returned 403, so neither was read. The FMCAD item is a talk abstract by one author, not the article.
- **Huo & Clause:** the figures come from the 2017 dissertation, which I assumed reproduces the FSE 2014 study. The numbers match the secondary listing, but the FSE text itself was not read.
- **Whalen et al.:** the follow-up read is a UMN report that states no peer-review venue. I graded it A-pre. A later peer-reviewed version may exist with different numbers. The ISSTA 2006 definitions were not re-read; the Rajan thesis was downloaded but not read.
- **DoLILU:** the NTRS OCR text is garbled in Table 1, so I used only the prose figures (695 errors; 15/6/20/57/3% by phase).
- **DSpec2Test venue:** not verified; DBLP returned a bot wall during this run.
- **Mashkoor & Jacquot:** I read the HAL *submitted* version (Jan 2016); the published REJ text may differ in §VII.
- **Brief scope:** I treated "later Dafny `generate-tests` evaluation" as permitting one replacement source (DSpec2Test). The brief's "Scope is verification … except where a claim can only be settled by a replacement source" may be read more narrowly.
- **Skipped items:** I skipped NonDex, SWE-bench Verified, μAlloy, Großer, NL2CTL, PROPAS/DMN and the other §5 rows not named in my assignment's item 8 list. DO-178C was not attempted.
