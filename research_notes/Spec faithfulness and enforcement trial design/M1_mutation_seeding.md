# M1: Mutation analysis and fault-seeding methodology for the one-operation trial (brief §3 items 2 and 5; threats in §7)

Scope: experimental method only. This strand covers how to seed misreadings into the spec and the layers derived from it (models, reference model R), how to keep seeded faults realistic, how to handle equivalent mutants and intended weaknesses, how to label ground truth, and how to calibrate the six misreading classes. It does not re-survey spec methods.

Grades follow the earlier briefs: A (peer-reviewed main venue), A-pre (preprint), A-workshop, B, C, D. FT = full text read (y / partial / n). TA = tool or method authors evaluating their own work. Own calculations are labelled "own calculation". Own reasoning is labelled *Inference*.

Source access in this run:
- Full texts read (in part or whole): Papadakis et al. 2019 survey; Just et al. FSE 2014; Chekam et al. ICSE 2017 (abstract, introduction, related-work table); Wang et al. (LLM mutation study); Tian et al. ISSTA 2024; Meta ACH (FSE Companion 2025); LLMorpheus; Petrović et al. ICSE 2021; Gopinath et al. ISSRE 2014; Walia & Carver IST 2009; Méndez Fernández et al. (NaPiRE risk paper).
- **[unreachable]** in this run, because of TLS chain errors from the hosts, 503 responses or closed access: Andrews, Briand & Labiche ICSE 2005 (Carleton PDF 503; Semantic Scholar: CLOSED); Andrews et al. TSE 2006 (CLOSED); Papadakis et al. ISSTA 2016 "Threats to the validity of mutation-based test assessment" (orbilu TLS error); Papadakis et al. ICSE 2015 TCE; Kurtz et al. 2014 "Mutant subsumption graphs"; Hutchins et al. ICSE 1994 (CLOSED); Black, Okun & Yesha ASE 2000 (TLS error); Lutz RE 1993 (NTRS 404); Hayes ISSRE 2003 (403).
- Not attempted: Mills 1972; Offutt et al. 1996 (sufficient operators); Basili & Weiss 1981; Kamsties; Krippendorff's primary text.
- Where an unreachable paper's claims are used, they come from a full-text secondary source, and that source is named.

---

## Q1. Fault-seeding methodology and its validity threats (classic mutation-analysis literature)

### Takeaway
The mutation literature's own checklist applies almost unchanged to a misreading-seeding trial:
- justify the operators (here: the misreading classes);
- control redundant and subsumed mutants;
- control test-suite size and strength;
- do not rely on the Clean Program Assumption;
- repeat stochastic generation;
- state the granularity.

The most consequential translation is the Clean Program Assumption (CPA). Spec-derived oracles must be **regenerated from each seeded (misread) spec**. Generating them once from the clean spec and running them against seeded artifacts would build in exactly the inflation the trial is meant to measure (*Inference*, from Chekam 2017 and the Papadakis survey §9.6).

### Cited Findings
- **Seven-point checklist** for using mutation in controlled experiments ([Papadakis et al. 2019, "Mutation Testing Advances: An Analysis and Survey", Advances in Computers 112, author copy](https://mutationtesting.uni.lu/survey.pdf); B, peer-reviewed survey chapter; FT y §5.3, §9, §10). The seven points:
  1. Mutant selection: "Explain the choice of mutant operators".
  2. Tool: give the exact version and transformation rules ("more than a quarter of the empirical studies does not report such details").
  3. Mutant redundancy: "use techniques like TCE … to remove the duplicate mutants … or a dynamic approximation of the disjoint mutation score … (in case the interest is on comparing test techniques)".
  4. Test suite choice and size.
  5. Clean Program Assumption.
  6. Multiple experimental repetitions.
  7. Granularity of reported results.
- **Subsumed-mutant threat** (same survey §9.3, which summarises Papadakis et al. ISSTA 2016 **[unreachable]**):
  - redundant mutants "can bias experimental results (approximately 60% for arbitrary experiments)";
  - disjoint mutants were ≈9 % of all mutants (Kintis), minimal mutants 1.2 % (Ammann) and 4 % (Kurtz et al., mutant subsumption graphs **[unreachable]**, via survey);
  - "researchers should identify and discard as many subsumed mutants as possible before conducting any test assessment";
  - Algorithm 1 (dynamic disjoint set) removes live and duplicate mutants, then greedily picks the mutant that subsumes the most others, using the kill matrix of the available tests.
- **Test-suite strength** (survey §9.4, summarising Chekam et al.):
  - "there is no practical difference between test criteria when relatively low-strength test suites are used";
  - a criterion's superiority "is only observable using stronger test suites";
  - test-suite size is a further confounder to control.
- **Repetitions** (survey §9.4/§10, citing Delamaro & Offutt, not read): when a full design is too expensive, research "suggests that it is preferable" to choose few subjects with many repetitions over many subjects with few repetitions.
- **Clean Program Assumption, primary source** ([Chekam et al., ICSE 2017, UCL author copy](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf); A; FT partial: abstract, introduction, related-work table).
  - "Most previous studies rely on the Clean Program Assumption, that a test suite will obtain similar coverage for both faulty and fixed ('clean') program versions … the Clean Program Assumption does not always hold."
  - With a methodology that recomputes test suites per faulty version (CoREBench real faults; 83,100 tests per their Table I row), "strong mutation testing has the highest fault revelation of four widely-used criteria" and "fault revelation starts to increase significantly only once relatively high levels of coverage are attained" (threshold behaviour).
- **Are mutants a valid substitute for real faults?** ([Just et al., FSE 2014](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf); A; FT y §2–3, §5).
  - Setting: 357 real faults, 5 Java programs, 230,000 mutants. "73% of real faults are coupled to the mutants generated by commonly used mutation operators".
  - 27 % (95/357) were not coupled. Of these, 25 needed stronger operators (statement deletion, argument swap/omission, similar library method) and 7 needed new operators. The rest showed a general limitation: "17% of real faults, mostly involving algorithmic changes or code deletion, are not coupled to any mutants".
  - Uncoupled categories include context sensitivity and "Violation of pre/post conditions or invariants".
  - Their related-work summary of Andrews et al. ICSE 2005 **[unreachable]**: "hand-seeded faults are not a good substitute for real faults, but … mutants are". That study was limited because "only one of the eight studied programs (Space) contained real faults" and it "considered only 10% of the generated mutants". Namin & Kakarla's replication with another tool "came to a different conclusion".
- **Hand-seeded fault sets can be biased by selection and by the seeder's knowledge** ([Gopinath, Jensen & Groce, ISSRE 2014](https://rahul.gopinath.org/resources/issre2014/gopinath2014mutations.pdf); A; FT partial: abstract and related work).
  - "the students who seeded the faults had knowledge of mutation analysis which may have biased the seeded faults (thus resulting in high correlation between seeded faults and mutants)".
  - The Siemens faults "originally from Hutchins et al. [**unreachable**] were confounded by their selection criteria which eliminated the majority of faults as being either too easy or too hard to detect".
  - "a typical fault involves about three to four tokens, and is seldom equivalent to any traditional mutation operator".
- **Correlation between mutation score and real-fault detection is not settled**: the survey (§9.1) says evidence that mutants behave like real faults is "only preliminary … contradicted by other studies" ([Papadakis et al. 2019](https://mutationtesting.uni.lu/survey.pdf)).
- **Industrial coupling evidence** ([Petrović et al., ICSE 2021, arXiv 2103.07189](https://arxiv.org/pdf/2103.07189); A; FT partial §IV-C). About 15 M mutants. "Mutants are coupled with 70% of high-priority bugs" (1043 of 1502), and coupled bugs are "usually coupled to more than one" mutant.

### Inferences
- **M1-R1 (CPA translated: seed upstream, regenerate downstream).** *Inference* from Chekam 2017 (A, FT partial) and survey §9.6 (B, FT y).
  - The trial's central claim is that spec-derived oracles *inherit* misreadings. A seeded misreading must therefore be planted in the spec, and every spec-derived layer must be regenerated from the seeded spec, per seeded version and per pipeline: models, R where the pipeline derives R from the spec, and the spec-enforcing tests.
  - Seeding only into R and running a clean-spec-derived test suite is the CPA analogue. It can only overstate the spec-enforcing family.
  - The cheaper R-only seeding is still useful as a separate stratum ("implementation misreading"). It must be reported separately and never pooled with spec-level seeds.
  - *Can show at small n*: whether the propagation effect exists at all; even a handful of seeds that the spec family catches only under CPA would demonstrate it.
  - *Cannot show*: its size in general.
  - Cost driver: one pipeline regeneration per seed per pipeline.
- **M1-R2 (subsumption control).** Survey §9.3 / §10 item 3 (B, FT y).
  - Compute and report both the raw kill rate and a dynamic-disjoint kill rate per family. Algorithm 1 runs over the union kill matrix of all families' tests.
  - Caveat (*Inference*): at 30–60 seeds the disjoint set may contain only a handful of items, and it depends on which tests exist. Treat it as a sensitivity analysis, not the primary measure.
  - Before running anything, remove seeds that are textually or semantically duplicate (two seeders producing the same misreading). This is the trivial-equivalence analogue of TCE.
- **M1-R3 (equalise suite size and strength).** Survey §9.4 and Chekam's threshold finding (A).
  - Compare families at equal test counts. This confirms the verified edition's R17, "per-family kill compared at equal test counts (G8)".
  - Also report each family's strength on a common yardstick, e.g. kill rate on a fixed set of R-level operator mutants, before comparing seeded-misreading kills.
  - Below threshold strength, a "no difference" result is uninformative. It must not count as refuting the central claim.
- **M1-R4 (repetitions of stochastic generation).** Survey §10 item 6 (B, FT y; Delamaro & Offutt via survey, not read).
  - With one operation (one subject), generate each LLM-produced family several times (e.g. 3–5 independent sessions per arm) and analyse per-seed detection probability across repetitions. Single-shot kill/no-kill would be the alternative.
  - *Inference*: this is the "few subjects, many repetitions" option, the only one available to a single-operation trial.
- **M1-R5 (pre-register inclusion; never filter by difficulty after seeing results).** From Gopinath's critique of the Hutchins selection (A; Hutchins **[unreachable]**).
  - Inclusion criteria for seeds (well-formed, one class, one locus) are fixed and applied before any family is run. Seeds are never dropped for being "too easy" or "too hard" after kill data exist.
- **M1-R6 (expect a non-coupled residue).** Just 2014 (A, FT y) found 17 % of real faults coupled to no mutant, mostly algorithmic or deletion faults, plus pre/post-condition and invariant violations.
  - *Inference*: the misreading classes most like "violated invariants across tables" (cross-table contradiction) and "algorithm changed" (reinterpreted option) are the least likely to be represented by simple, local seeds.
  - Such classes should be seeded as whole-clause rewrites, not token edits.

### Gaps
- Papadakis ISSTA 2016, Andrews ICSE 2005 / TSE 2006, Kurtz 2014, TCE ICSE 2015 and Hutchins 1994: full texts **[unreachable]**. Their claims are taken only via full-text secondary sources (survey; Just; Gopinath), so exact figures, e.g. Andrews's detection-ratio statistics, are not reported here.
- Mills error seeding (capture–recapture estimate of remaining faults) and Offutt et al. on sufficient operators: not fetched.
  - *Inference*: Mills's estimator assumes seeded and real faults are equally detectable, which is precisely what Q2 says is unproven. The trial should not report "estimated remaining misreadings".
- No source studies mutation or seeding at the level of natural-language-derived *specifications* with CPA control. Black, Okun & Yesha's specification-mutation operators (ASE 2000) were **[unreachable]**.

---

## Q2. Human vs. tool vs. LLM-seeded faults, and how to check realism

### Takeaway
- LLM-generated mutants are measurably closer to real bugs than rule-based ones on Java benchmarks, but they bring more duplicates, non-compilable output and equivalent mutants. Hand-seeded faults carry seeder-knowledge and selection bias.
- Realism should therefore be checked, not assumed, in three ways:
  1. against held-out **real** misreadings, using a coupling or Ochiai-style overlap of failing checks;
  2. by blinded expert rating with an agreement statistic;
  3. by comparing the class distribution with whatever real distribution exists.
- No source gives a validated realism check for *spec-level* misreadings.

### Cited Findings
- **LLM vs rule-based mutants: realism and cost** ([Wang, Chen, Deng, Lin, Harman, Papadakis & Zhang, "A Comprehensive Study on Large Language Models for Mutation Testing", arXiv 2406.09843 v5, Jan 2026, TOSEM template with placeholder DOI](https://arxiv.org/pdf/2406.09843); A-pre (TOSEM acceptance not verified); FT y §3; Papadakis and Harman are co-authors of LLMorpheus/ACH-adjacent work, so not fully independent).
  - Setting: 851 real bugs (605 Defects4J 2.0, 246 ConDefects).
  - LLM approaches "reach a detection rate of 76.47%, compared to 44.15% for rule-based techniques". The cost: "worse non-compilability, duplication, and equivalent mutant rates by 32.73, 9.38, and 3.64 percentage points".
  - Realism measures used:
    - Real Bug Detection Rate: a bug counts as "detected" if at least one mutant fails the same tests (following Just et al.).
    - Ochiai coefficient between failing-test sets, |fT_m ∩ fT_b| / √(|fT_m|·|fT_b|), with "high Ochiai" at ≥ 0.8 (following Ojdanic et al.).
    - Coupling rate: the share of de-duplicated mutants whose killing tests overlap the bug-triggering tests.
  - Data leakage is acknowledged: Defects4J bugs predate the LLMs' training.
- **LLMorpheus** ([Tip, Bell & Schäfer, arXiv 2404.09952; TSE 2025 per Semantic Scholar DOI 10.1109/TSE.2025.3562025](https://arxiv.org/pdf/2404.09952); A; FT y §4–5; TA).
  - Two authors independently coded up to 50 surviving mutants per project as "equivalent", "not equivalent" or "unknown", then met to resolve.
  - Of 517 survivors, 403 (78 %) were not equivalent, 105 (20 %) equivalent and 9 (2 %) unknown.
  - "Unknown" was used where "it was truly impossible to determine whether or not this change impacted the correctness of the program as intended by its developers" (e.g. console.error → console.warn; changed error messages).
  - Results vary with temperature: "mostly the same mutants" at temperature 0, "mostly different mutants at temperature" 1.0.
- **Meta ACH** ([Foster, Gulati, Harman et al., "Mutation-Guided LLM-based Test Generation at Meta", FSE Companion '25, arXiv 2501.12862](https://arxiv.org/pdf/2501.12862); A (industry track); FT partial §1, §4–5; TA).
  - Setting: 10,795 Kotlin classes; 9,095 mutants; 571 tests; engineers accepted 73 % of reviewed tests.
  - The LLM mutant generator produced many trivially equivalent mutants: "25% of the mutants generated are trivially syntactically equivalent", against "typically around 10% to 15% for rule-based approaches".
  - It also injected "misleading" comments, e.g. "// Introduce a bug by not checking …", that make no executable change.
- **Seeder knowledge bias**: students who seeded faults "had knowledge of mutation analysis which may have biased the seeded faults" ([Gopinath et al. 2014](https://rahul.gopinath.org/resources/issre2014/gopinath2014mutations.pdf); A; FT partial).
- **Real fault shape** (Gopinath et al. 2014, same source): a typical real fault spans "about three to four tokens". Their summary of Durães & Madeira (668 faults, 9 C projects; not read): "64% of the faults were due to missing constructs, 33% due to changes, and only 2.7% were due to extraneous constructs".
- **Earlier report baseline** (deep-dive §2.1 table, verbatim): "Leinonen et al. (A-pre; FT partial): GPT-4o buggy submissions match real failure *distributions* (8,598 real submissions) … Matches failure distributions, not misconceptions". Also: "About 30 % of wheat failures are good-faith misunderstandings … 'The experts (course staff) missed most of these'" (Making Hay). These support realism checks against real misreadings over expert intuition alone.

### Inferences
- **M1-R7 (who seeds: both, as a factor).** *Inference* built on Wang et al. (A-pre), Gopinath 2014 (A) and Making Hay (via the deep dive).
  - Use two seeding sources, recorded as an analysis factor:
    - (a) a human seeder who has **not** seen the test families, gate definitions or arm assignments (avoids seeder-knowledge bias);
    - (b) an LLM seeder from a provider lineage used by **neither** arm.
  - The deep dive's correlated-error caution (Kim et al.) implies that a seeder sharing a lineage with an arm would plant misreadings that arm is predisposed to make, or to miss.
  - Report kills per seeder source. If the families' ranking flips between sources, the result is seeder-dependent.
  - *Small n*: a flip is detectable only as a gross pattern.
- **M1-R8 (held-out real misreadings as the primary realism anchor).** *Inference*.
  - The brief lists three real failure modes from earlier records: "decision text that went beyond what was answered; tables that disagree; consistency checks that passed but missed a contradiction".
  - Each real instance that can be reconstructed becomes a held-out item. Seeders never see it, and it is scored separately.
  - Realism measure, adapted from Just and Wang: a real misreading is *coupled* to the seeded set if some seeded misreading is killed by a subset of the checks that kill the real one. Also report the Ochiai overlap between failing-check sets, with ≥ 0.8 marked "high", carried over from Wang's code-level threshold. That threshold is unvalidated for spec checks.
  - *Small n*: with perhaps 3–10 real items this is descriptive only. "No real item is coupled" is a strong warning. "All are coupled" is weak support.
- **M1-R9 (blinded realism rating).** *Inference*, with agreement thresholds from Q4.
  - Mix real and seeded misreadings, stripped of provenance, and ask two raters for (i) a plausibility rating and (ii) a guess of "real or seeded".
  - Near-chance discrimination supports realism. High discrimination shows seeds are recognisably artificial.
  - Use a fixed rubric, e.g. "could a careful reader of the records plausibly produce this?"
- **M1-R10 (seed shape).** *Inference* from Gopinath 2014 and Just 2014 (A).
  - Prefer clause- or row-level misreadings over single-token edits. Expect omissions to dominate in reality (Durães via Gopinath: 64 % missing constructs; Q5).
  - LLM seeders must be prompted to change behaviour, not to annotate. Pre-filter seeds that only add comments or rationale text: ACH's "misleading comment" artefact.

### Gaps
- No study found that measures the realism of seeded misreadings in *specifications or requirements* against real misreadings. All realism metrics found (coupling, Ochiai, detection rate) are code-level.
- "Mutant naturalness" (Jimenez et al. ICST 2018) and Ojdanic et al. (semantic similarity of artificial and real faults) were not fetched. The Ochiai threshold is taken via Wang et al.
- Gopinath's "How hard does mutation analysis have to be, anyway?" (ISSRE 2015): author URL returned 404; not read.

---

## Q3. Equivalent mutants and intended weaknesses: detection, triage budget, "killable" denominators

### Takeaway
- Equivalence is undecidable. Practice is:
  1. cheap conservative filters first (duplicate or trivial equivalence);
  2. then human adjudication with a three-way label, equivalent / not equivalent / unknown;
  3. with LLM detectors used only to *prioritise*. Prompted general LLMs reached only ≈0.54–0.56 macro-F1 on a balanced benchmark.
- For this trial, "equivalent" splits into:
  - **allowed variant**: the seeded text stays within the records' non-commitments, so it is *not* a misreading;
  - **intended weakness**;
  - **unknown**.
- The denominator should be reported three ways.

### Cited Findings
- **TCE and static heuristics** (survey §5.3.1, [Papadakis et al. 2019](https://mutationtesting.uni.lu/survey.pdf); B; FT y; TCE ICSE 2015 **[unreachable]**).
  - "Detecting equivalent mutants is a well-known undecidable problem". TCE declares equivalence "only for the mutants that their compiled object code is identical" and identifies "at least 30% of all the equivalent mutants".
  - TCE finds duplicates at 21 % (C) and 5.4 % (Java) of mutants, and "is conservative as all declared redundancies are guaranteed".
  - Kintis & Malevris use data-flow patterns (survey summary).
- **LLM equivalent-mutant detection** ([Tian et al., ISSTA 2024, arXiv 2408.01760](https://arxiv.org/pdf/2408.01760); A; FT partial: abstract, §3, Tables 2–3).
  - Setting: 3,302 method-level Java mutant pairs, ≈50 % equivalent; macro-averaged metrics.
  - TCE (Soot): P 51.26 %, R 51.81 %, F1 50.80 %.
  - GPT-4 zero-shot: P 67.42 %, R 53.76 %, F1 53.61 %. Few-shot: P 67.02 %, R 55.18 %, F1 55.90 %.
  - Fine-tuned UniXCoder: P 94.33 %, R 81.81 %, F1 86.58 %. "code embedding strategies outperform prompting strategies".
- **Meta ACH equivalence agent** ([arXiv 2501.12862 §5](https://arxiv.org/pdf/2501.12862); A industry; FT partial; TA).
  - Ground truth comes from manual analysis of about 100 sampled mutants per platform, judged under *weak* mutation ("we do not need to consider failed error propagation").
  - Precision 0.79 / recall 0.47 when "unsure" counts as equivalent. Precision 0.97 / recall 0.44 when "unsure" counts as non-equivalent.
  - Precision 0.95 / recall 0.96 after rule-based pre-processing (strip comments; lexical identity).
  - The authors caution that this reflects "the kind of mutants the detector needs to judge", not general skill: the generator makes changes that are obviously semantic or obviously equivalent.
- **Manual equivalence labelling protocol and cost** ([Wang et al. §3.2.3](https://arxiv.org/pdf/2406.09843); A-pre; FT y).
  - Random sample per approach at "95% confidence level with a 10% margin of error" (≈96 mutants).
  - "Two authors independently evaluate". Tests are run first: 860 of 1,437 were killed, "the remaining 577 were manually checked".
  - It "took approximately thirteen hours per person". Cohen's κ = 0.8, with disagreements resolved by discussion.
  - Equivalent-mutant rates: 1.0–2.1 % for PIT/Major and ≈3–6 % for LLM approaches (up to 10.6 %).
  - Own calculation: 13 h × 60 / 577 ≈ 1.35 person-minutes per manually checked mutant, for code-level Java mutants.
- **Three-way label with "unknown" for intent-dependent cases** ([LLMorpheus §5](https://arxiv.org/pdf/2404.09952); A; FT y): 2 % unknown, 20 % equivalent among survivors (Q2).
- **Earlier reports' baseline** (verbatim):
  - Verified edition, MutDafny row: "284 survivors reviewed: 77 weak-spec hints, 157 equivalent, 50 inconclusive" and "~18 min/file".
  - First report: "About 18 min per file; 1.7 min per survivor".
  - IronSpec row: "13 of 61 surviving mutants intended weaknesses".
  - First report §2.2 inference: "Survivors that map to a registered non-promise are auto-classified "intended", which shrinks IronSpec/MutDafny-style triage."
  - Verified R17 overturn condition: "equivalent-mutant triage costing more than the findings (MutDafny: 157 of 284 equivalent)".

### Inferences
- **M1-R11 (three-stage triage).** *Inference* built on the survey (TCE), ACH and Tian.
  1. **Trivial-equivalence filter, before anything runs**: textual identity after normalisation; seeds that only change rationale or comment text; seeds whose changed clause is not referenced by any check. This is the ACH and TCE analogue; it is conservative and cheap.
  2. **Register screen.** A seed that maps onto an entry in the spec's non-commitment register (an allowed outcome set, or a "deliberately not promised" item) is *provisionally* labelled "allowed variant".
     - It is still adjudicated by humans: the first report's auto-classification is an untested inference.
     - The audited agreement between register auto-labels and human labels is a measure in its own right; report its precision and recall.
  3. **Human adjudication** of every remaining unkilled seed, with a three-way label (misreading / allowed variant / unknown) following LLMorpheus. An LLM detector may order the queue but never removes items.
     - Tian's prompted-GPT-4 F1 ≈ 0.55 (A) and ACH's recall 0.47 (A, TA) say an LLM screen would drop many items that are actually killable or actually misreadings.
  - *Small n*: every seed can be adjudicated (n ≤ ~60), so no sampling is needed. That removes the sampling error Wang had to accept.
- **M1-R12 (seeding happens before killing: label every seed, not only survivors).** *Inference*.
  - Unlike code mutation, the "is it a misreading?" label should be given to **all** seeds before any family runs, blind to outcomes. A killed seed that is actually an allowed variant shows an **over-strict** check, not a kill.
  - This is the deep dive's validity side ("the suite accepts every wheat"). It joins brief §3 item 4 (over-strict tests) to ground truth.
- **M1-R13 (denominators).** *Inference* from the survey's requirement to remove equivalents and from LLMorpheus's "unknown".
  - Report kill rate as:
    - (a) kills / adjudicated misreadings (primary, the "killable" denominator);
    - (b) unknowns counted as misreadings (lower bound);
    - (c) unknowns excluded (upper bound).
  - Report kills of seeds labelled "allowed variant" separately, as over-strict detections (false alarms against ground truth).
  - Never report kills / all seeds.
- **M1-R14 (triage budget).** *Inference*, with anchors: Wang ≈1.35 min per code mutant per rater (own calculation); MutDafny 1.7 min per survivor (earlier report); IronSpec 13/61 intended.
  - Spec-level misreadings need reading the records and the register, so budget 5–10 person-minutes per seed per rater, plus about 30 % for adjudication meetings. This is unsourced.
  - At 48 seeds × 2 raters × 7.5 min ≈ 12 person-hours, plus about 3–4 h adjudication (own calculation from the assumed rate).
  - Stop rule: if the calibration batch (first 10 seeds) takes more than twice the budgeted time per seed, cut seeds per class before cutting the second rater.
- **M1-R15 (strong vs weak sense).** ACH judged equivalence under *weak* mutation.
  - *Inference*: the trial needs the *strong* sense, i.e. whether the misreading can change any observable behaviour allowed or forbidden by the records. A seed that changes the spec text but no behaviour reachable under the declared environment is "unknown" or "allowed", not a miss.

### Gaps
- No precision or recall figure exists for LLM equivalence judgement on *specification* or requirements text. Tian's and ACH's figures are code-level, and ACH's are TA and tied to its own generator's mutant style.
- Kintis et al.'s equivalence-heuristic papers were not read directly.
- Triage minutes per spec-level seed: no source. The 5–10 min figure is *Inference*.

---

## Q4. Ground truth: labelling protocol, blinding, agreement thresholds, "misreading" vs "allowed variant"

### Takeaway
- Use two independent raters who are blind to arm, family and gate outcome. Calibrate on a pilot batch, then adjudicate disagreements with a third person or by recorded discussion.
- Report Cohen's κ (two raters) or Krippendorff's α, using the conventional α ≥ 0.800 "rely" and ≥ 0.667 "tentative" bands. The primary-source wording for those bands was not verified in this run.
- The comparable code-mutation studies reached κ = 0.8 with two authors. None of them was blinded to the technique.
- The misreading vs allowed-variant decision should be made **against the records plus the non-commitment register only**, never against the spec under test.

### Cited Findings
- **Two-rater labelling with κ** ([Wang et al. §3.2.3](https://arxiv.org/pdf/2406.09843); A-pre; FT y): "Two authors independently evaluate … Cohen's kappa coefficient (κ) … overall κ value of 0.8 … In cases of disagreement, both authors conducted thorough discussions … labeling results are available at our repo."
- **Two coders + meeting + "unknown" category** ([LLMorpheus §5](https://arxiv.org/pdf/2404.09952); A; FT y). They report no κ in the text read.
- **ACH**: ground truth from manual analysis; a column marks cases where "the human assessor had to think noticeably longer" ("equivalence is not obvious"). The text read suggests a single assessor ([arXiv 2501.12862 §5](https://arxiv.org/pdf/2501.12862); A industry; FT partial).
- **Krippendorff thresholds**: "rely on data with reliabilities α ≥ 0.800, consider data with 0.800 > α ≥ 0.667 only to draw tentative conclusions, and discard data whose agreement measures α < 0.667"; the minimum acceptable α "should be chosen according to the importance of the conclusions" ([Wikipedia, Krippendorff's alpha](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha); D, secondary).
  - Krippendorff's computation note ([Computing Krippendorff's Alpha-Reliability](https://www.asc.upenn.edu/sites/default/files/2021-03/Computing%20Krippendorff%27s%20Alpha-Reliability.pdf); B; FT y) gives worked examples (e.g. α = 0.815 ordinal) but does not contain the threshold text.
  - Primary wording (Content Analysis textbook): **[unreachable / not attempted]**.
- **Blinding**: the deep dive's Examplar note warns that a student "may be overly tempted to intentionally write failing assertions to discover what the behavior of wheats is" (deep dive §2.1, verbatim). Hidden ground truth is the norm in wheat/chaff evaluation.
- **Earlier report baseline on allowed variants** (deep dive §3.1, verbatim): "allowed variants = ≥ 2 wheats that differ on every non-promised item, or NonDex-style perturbation. Report RejectLegal and DetectFault together. Wheats and chaffs themselves reviewed for over-constraint".

### Inferences
- **M1-R16 (labelling protocol).** *Inference*; agreement practice from Wang and LLMorpheus.
  1. **Rater pool**: two raters who did not write the spec, the seeds or any test family. The single maintainer is a known threat (brief §3 item 7). If only the maintainer is available, one rater must be external or an LLM from a third lineage, and its agreement with the human is reported as a *judge-precision* measure (brief §3 item 4), not as ground truth.
  2. **Materials**: the records (prose decisions, scenarios, rejected options) and the non-commitment register, plus the seeded diff. Raters do not see the spec under test (avoids anchoring), the arm, the family, or kill outcomes.
  3. **Label set per seed**: {misreading of class c, allowed variant, unknown}, with a free-text pointer to the record clause relied on.
  4. **Calibration**: label 8–10 pilot seeds, not used in analysis; discuss; refine the rubric; freeze it.
  5. **Main labelling**: independent; then κ (or α). Disagreements go to a third adjudicator, or to a recorded discussion if no third person exists.
  6. **Threshold**: aim for α/κ ≥ 0.80. Between 0.667 and 0.80, report results as tentative. Below 0.667, the class definitions are not operational: revise and re-label, without touching kill data.
  - *Small n*: own reasoning only, as no κ-CI computation was run here. With ~50 items, κ's confidence interval is wide, roughly ±0.15. Report the CI, not just the point estimate.
- **M1-R17 (operational rule: misreading vs allowed variant).** *Inference*, tied to the verified and deep-dive register design.
  - A seed is an **allowed variant** iff every behaviour it permits or forbids differently from the clean spec lies inside a register entry: an unspecified set, where the variant picks another allowed member, or a deliberately-not-promised item.
  - It is a **misreading** if it permits a behaviour the records forbid, forbids one they require, or changes the *type* of a non-commitment.
  - Wrong non-commitment type is itself one of the six classes. So changing "unspecified set" to "deliberately not promised" is a misreading even when every concrete outcome stays allowed.
  - Edge cases go to "unknown". LLMorpheus's "intended by its developers" ambiguity is the code-level analogue.
- **M1-R18 (label the held-out real items the same way)**, mixed into the same rating batch, so real and seeded items share one labelling process (M1-R9).

### Gaps
- No source found blinds raters to the *technique* when labelling mutants. Blinding here is *Inference* from general experimental practice and from Examplar's hidden wheats.
- Exact Krippendorff wording and page: primary unreachable. Landis & Koch κ bands were not fetched.
- No source gives inter-rater agreement for classifying *requirements* misreadings into fine classes. Walia & Carver's taxonomy experiments (below) were not checked for κ.

---

## Q5. A misreading taxonomy for the six classes, and calibration of seeding proportions

### Takeaway
- No requirements-defect taxonomy found here gives empirical frequencies that map onto the six required classes. Walia & Carver's taxonomy classifies human *error causes* (people / process / documentation), not defect shapes, and the SLR gives no frequencies.
- The only frequency signals found point the same way: omission dominates.
  - Requirements problems (NaPiRE): incomplete or hidden requirements cited by 48 % of 228 companies, inconsistent requirements by 19 %.
  - Code faults (Durães & Madeira via Gopinath): 64 % missing constructs vs 2.7 % extraneous.
- Recommendation: **stratified, equal allocation per class** for per-class detection estimates, plus a secondary frequency-weighted aggregate that up-weights "lost case". Both choices are *Inference*.

### Cited Findings
- **Walia & Carver taxonomy** ([Walia & Carver, IST 51 (2009) 1087–1109, course-hosted copy](https://www.cin.ufpe.br/~in1037/AllFinal/SE63%20Walia%202009.pdf); A; FT partial §4–5).
  - Error classes were grouped "into three high-level types: people errors, process errors, and documentation errors". Grouping was done by "similar characteristics (symptoms)", keeping classes "as orthogonal as possible".
  - Each class comes with an example error and the resulting fault. One example: "Fault: An extraneous requirement is included …" (traceability error class).
  - The SLR reports where errors come from (causal analysis, empirical studies, cognitive psychology). In the parts read, it gives no occurrence frequencies per class.
  - Psychology-derived categories it lists: "Omission errors (something is left out), commission errors …".
- **NaPiRE cross-company data** ([Méndez Fernández et al., "On Evidence-based Risk Management in Requirements Engineering", arXiv 1707.00144](https://arxiv.org/pdf/1707.00144); A-pre/B, venue not verified in this run; FT partial §2–3, Table 1). Setting: 228 companies, share of respondents citing each problem among their top problems:
  - "Incomplete and / or hidden requirements 109 (48%)";
  - "Underspecified requirements that are too abstract 76 (33%)";
  - "Inconsistent requirements 44 (19%)";
  - "incomplete requirements dominate the list of top 10 problems".
  - These are *problems perceived by practitioners*, not counted defects.
- **Code-level fault shape**: Durães & Madeira (668 faults; not read), via [Gopinath et al. 2014](https://rahul.gopinath.org/resources/issre2014/gopinath2014mutations.pdf) (A, FT partial): "64% … missing constructs, 33% due to changes, and only 2.7% … extraneous constructs".
- **Uncoupled real-fault types** ([Just et al. 2014 §3.2](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf); A; FT y): code deletion, algorithmic changes, context sensitivity and "Violation of pre/post conditions or invariants" are the categories simple mutants miss.
- **Earlier report baseline** (deep dive D1-R3, verbatim): "Conceptual chaffs: one per rejected option and per plausible clause misreading. Each must be killed. Mine failures for unanticipated chaffs". Also from the deep dive: "a documented rejected option is an *expert-designed chaff*. It covers anticipated misreadings, misses ones that only show up in practice, and is sometimes never triggered."
- **Unreachable / not attempted** for frequency calibration: Basili & Weiss 1981 (requirements change data), Lutz RE 1993 (safety-critical interface errors; abstract via search only), Hayes ISSRE 2003 (NASA requirement fault taxonomy, 403), Kamsties (ambiguity).

### Inferences
- **M1-R19 (mapping the six classes onto generic defect types).** *Inference*.

  | Required class | Generic type | Closest real-mode anchor in the earlier records (brief §2) | Seed shape |
  |---|---|---|---|
  | Lost case | Omission (Walia "omission"; NaPiRE "incomplete") | — | Delete a case-table row or a scenario-derived branch |
  | Added commitment | Commission / extraneous | "decision text that went beyond what was answered" | Fix a value or order the records leave open |
  | Reinterpreted option (rejected option adopted) | Incorrect fact / algorithmic | — (D1-R3 chaff) | Replace the clause with the documented rejected alternative |
  | Wrong non-commitment type | Incorrect fact (meta-level) | — | Change "unspecified set" to "not promised", or the reverse |
  | Wrong environment exposure | Interface error (Lutz's interface emphasis, abstract only) | — | Expose or hide an environment action or failure the records scope differently |
  | Cross-table contradiction | Inconsistency (NaPiRE 19 %) | "tables that disagree"; "consistency checks that passed but missed a contradiction" | Change one table cell so the case table and the state × operation table disagree |

- **M1-R20 (allocation).** *Inference*.
  - The trial's questions are per family and per gate. With six classes, frequency-matched allocation would leave rare classes with 1–2 seeds and no estimate.
  - Use **equal allocation**, e.g. 6–10 seeds per class (36–60 in total), split across human and LLM seeders.
  - Report a **secondary aggregate** reweighted so that omission ("lost case") carries more weight, citing NaPiRE (48 % vs 19 %) and Durães (64 % missing). State plainly that no source gives frequencies for the six classes themselves.
- **M1-R21 (seed realism per class).** *Inference*.
  - Classes with an anchor in real records (added commitment; cross-table contradiction) get held-out real items (M1-R8).
  - Classes without one (wrong non-commitment type; wrong environment exposure) are flagged in the report as "realism unanchored".
- **M1-R22 (first-order seeds, plus a few combinations).** *Inference* from the coupling literature (Just 2014; Petrović 2021).
  - One misreading per seeded version, so that the first gate to fail and the killing family can be attributed.
  - Add a small set (e.g. 4–6) of two-class combinations to check coupling: is a combination killed whenever its components are?
  - *Small n*: descriptive only.

### Gaps
- No frequency data for the six classes, or for any requirements taxonomy at clause level, was found in full text.
- Walia & Carver's later controlled experiments (Walia & Carver 2010/2013) and Hayes's NASA taxonomy might give occurrence counts; not read.
- Kamsties's ambiguity taxonomy: not fetched.

---

## Sample-size notes for the seeding design (own calculation; supports brief §3 item 6)

These are own calculations in pure Python, not taken from a source. Per-seed detection by two families is a paired binary outcome, so the exact McNemar test on discordant seeds applies.
- **Discordant splits needed** for two-sided p < 0.05 (exact binomial on discordant pairs): 6 discordant → 6:0; 8 → 8:0; 10 → 9:1; 12 → 10:2; 15 → 12:3; 20 → 15:5. With 5 or fewer discordant seeds, significance is impossible.
- **Power of the exact McNemar test**:

  | Scenario | n = 24 | n = 36 | n = 48 | n = 60 | n = 90 | n = 120 |
  |---|---|---|---|---|---|---|
  | (a) only family X kills 25 % of seeds, only family Y kills 5 % | 0.28 | 0.51 | 0.68 | 0.80 | 0.94 | 0.99 |
  | (b) 20 % vs 10 % | 0.06 | 0.12 | 0.17 | 0.22 | 0.33 | 0.45 |
  | (c) 15 % vs 5 % | 0.06 | 0.14 | 0.23 | 0.31 | 0.49 | 0.63 |

- **95 % Wilson intervals for a kill rate**:
  - observed 50 %: n = 12 → 0.25–0.75; n = 36 → 0.34–0.66; n = 60 → 0.38–0.62;
  - observed 0/n: n = 24 → upper bound 0.14; n = 60 → 0.06.
- *Inference*:
  - 36–60 seeds detect only a **large** asymmetry, such as the central claim holding strongly (expectation family alone catches ≥ 20–25 % of seeds that the spec family misses, and the reverse is rare).
  - Moderate asymmetries are not detectable at this n.
  - Per-class (6–10 seeds) and per-gate figures are descriptive.
  - Repetitions (M1-R4) help estimate per-seed detection probability, but they do not raise the number of independent seeds.

---

## What this strand cannot settle

- **Seeded vs real spec misreadings.** No source measures whether seeded spec misreadings behave like real ones. All realism evidence (Just; Wang; Petrović; Gopinath) is code-level, Java/C/Go, with code mutants. The held-out real set from earlier records will be small, so realism stays partly unanchored, especially for wrong non-commitment type and wrong environment exposure.
- **Class proportions.** No empirical frequency exists for the six classes. Allocation is a design choice, not a calibration.
- **Triage minutes per spec-level seed.** Unsourced. The anchors are code-level, Dafny-level or tool-author figures.
- **LLM equivalence judges on spec text.** Their precision and recall are unknown. Code-level figures (Tian; ACH) do not transfer by default.
- **Statistical power.** At a feasible n (36–60) only large family differences are detectable (own calculation). A null result does not refute the central claim unless both families are shown to be above threshold strength (Chekam threshold effect).
- **Krippendorff thresholds.** Taken from a secondary source. The primary wording was not verified.
- **Unreachable classic papers.** Andrews 2005/2006, Papadakis ISSTA 2016, Kurtz 2014, TCE 2015, Hutchins 1994, Black/Okun/Yesha 2000, Lutz 1993 and Hayes 2003 were unreachable. Their content enters only via full-text secondary summaries.

## Self-check (possible misreadings of the briefs, reports or sources)

1. **Scope.** The brief's §3 item 2 asks for "a held-out set of *real* misreadings if any exist". I assumed the three failure modes listed in brief §2 can be reconstructed into concrete items. If the earlier records hold only descriptions, not reproducible artefacts, M1-R8 reduces to a qualitative check.
2. **CPA translation (M1-R1).** This is my analogy. Chekam's CPA concerns test suites and coverage measured on clean vs faulty *programs*. Applying it to "spec-derived oracles generated from clean vs seeded spec" is *Inference*, not Chekam's claim.
3. **The 60 % figure** ("redundant mutants can bias experimental results (approximately 60% for arbitrary experiments)") is the survey's summary of ISSTA 2016, which I could not read. Its exact definition (the probability that conclusions change) is unverified.
4. **Wang et al. grade.** The PDF uses the TOSEM template with a placeholder DOI. I graded it A-pre, because acceptance was not verified. Two of its authors (Papadakis, Harman) also author the survey and ACH, so these sources are not independent of each other.
5. **ACH single assessor.** I read "the human assessor" as one person. The text may not state the rater count explicitly. Its precision and recall are under *weak* mutation and tied to its own generator, so they are TA.
6. **Tian et al. metrics** are macro-averaged over a roughly balanced benchmark. Precision and recall at a realistic equivalent-mutant prevalence (a few % to 20 %) would differ. I did not recompute them.
7. **NaPiRE percentages** are respondents citing a problem, not defect counts. I use them only as a directional signal for omission dominance.
8. **Walia & Carver.** I read sections 4–5 partially and found no frequency tables. Frequencies could exist in parts not read, e.g. appendices, though the paper is an SLR building a taxonomy.
9. **Earlier report quotes.** I quoted MutDafny and IronSpec figures from the verified edition and the first report, not from MutDafny or IronSpec themselves. The first report's "1.7 min per survivor" does not appear in the verified edition's row, which gives "~18 min/file". I have not checked which is current.
10. **Power figures** assume independent seeds and a fixed discordance probability. Seeds by the same seeder, or within one class, are likely correlated, so real power is lower.
