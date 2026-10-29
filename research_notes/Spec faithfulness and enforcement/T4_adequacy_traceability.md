# T4 Adequacy and traceability (plus disconfirming search §5(b))

Scope: trace links as checkable data; mutation of specs, models and the reference model as an adequacy measure; coverage measures that fit; how T1–T4 checks compose into a fail-early gate sequence; agent/LLM measurements for each. Grades follow brief §6 (A / A-pre / A-workshop / B / C / D). **[unreachable]** = full text not fetched, so the item is a lead only. *Inference* = my reasoning. Items from brief §3 are not re-surveyed.

Full texts read (local extracts in the scratchpad, not in the repo): IronSpec (OSDI'24), MutDafny (arXiv 2511.15403), Jovanovic/Patwary/Sullivan (FormaliSE'25), Just et al. (FSE'14), Inozemtseva & Holmes (ICSE'14), Chekam et al. (ICSE'17), Gay et al. (TSE'15, author preprint, first 6 pages only), Petrović et al. (ICSE-SEIP'21), Meta ACH (FSE Companion'25), Wang et al. (TOSEM'25, LLM mutation), LiSSA (ICSE'25), Goldstein et al. (ICSE'24), Hughes "How to Specify It!" (TFP'19), TLA+-Bench (arXiv 2607.23425), TLA-Prover (arXiv 2606.06133), SpecRL (arXiv 2604.05820), Richter & Wehrheim NL2Contract (arXiv 2510.12702). Tool docs or source read: sphinx-needs configuration, Doorstop validation docs and CLI source, OpenFastTrace console report docs and `LinkStatus.java`, QuickCheck Haddock, Hypothesis API docs, TLC coverage wiki, mutmut README.

---

## Q1. Trace links (decision → clause → model element → test) as checkable data, with gates that fail on dangling or orphan links; LLM trace-link recovery accuracy

### Takeaway
Mature open-source tools already treat traces as typed, versioned data and can fail a CI build on a dangling link, a missing downstream coverage link, a duplicate ID or a stale (outdated) link. OpenFastTrace and sphinx-needs are the closest fit for a record → clause → model → test chain. Automated trace-link *recovery*, whether IR or LLM, reaches only about 0.2–0.6 F1 on requirement → code benchmarks, so it can audit links but cannot be the source of truth. Links should be written when each artefact is created and then machine-checked. The one measured benefit of traceability (Mäder & Egyed, n = 71 people) is human-only evidence.

### Cited Findings
**Tools: what each checks and how it fails a build (all B, official docs or source):**
- **OpenFastTrace (OFT)** gives each specification item an ID of the form `type~name~revision`. An item declares which artefact types must cover it (e.g. `(impl, utest)`). The tracer reports `-impl` for a missing coverage type and `+itest` for unrequested coverage. It also reports `not ok (transitive)` when the item is covered but something it covers is defective, and `[has N duplicates]` for duplicate IDs. — [OFT console tracing report](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/console_tracing_report.md)
- OFT link statuses, from the source enum: `COVERS`, `PREDATED` (covers a newer revision), `OUTDATED` (covers an older revision), `AMBIGUOUS` (two items with the same ID), `UNWANTED` (covers an item that needs no coverage), `ORPHANED` ("an item covers a non-existing item"), `COVERED_SHALLOW`, `COVERED_UNWANTED`, `COVERED_PREDATED`, `COVERED_OUTDATED`, `DUPLICATE`. — [OFT LinkStatus.java](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/api/src/main/java/org/itsallcode/openfasttrace/api/core/LinkStatus.java)
- OFT has a `quiet` report verbosity "in case only the return code is used", so it is designed as a CI gate. Other verbosities include `failures` and `direct_failures`, the latter separating non-transitive defects. — [OFT command line](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/oft_command_line.md)
  - *Inference:* the revision field in OFT IDs (`~1`) suits this pipeline. When a record decision is revised, every clause, model element and test still citing the old revision becomes `OUTDATED`. That gives a mechanical stale-link gate for spec evolution.
- **sphinx-needs** offers `needs_warnings` (filter strings or functions that "define a not allowed behavior", e.g. `"type == 'req' and not status"`). Building with Sphinx `-W` turns any raised warning into a failure. `needs_constraints` checks each need and attaches a severity. `needs_constraint_failed_options` maps a severity to `on_fail: ["break"]`, which "breaks the build process and raises a NeedsConstraintFailed Exception", or to `warn` or `style`. — [sphinx-needs configuration](https://sphinx-needs.readthedocs.io/en/latest/configuration.html)
- sphinx-needs link types carry `allow_dead_links` (default False, so "referenced, but not found" needs raise a warning). They can also restrict `target_types` (a wrong-type target is reported as `needs.link_target_type`) and set schema link counts (`minItems`/`maxItems`), reported as `sn_schema_violation.link_fail`. `needs_id_required` and `needs_id_regex` enforce explicit IDs in a set format. — [sphinx-needs configuration](https://sphinx-needs.readthedocs.io/en/latest/configuration.html)
  - *Inference:* an orphan check ("every clause must have at least one incoming test link") fits in a `needs_warnings` filter over back-links. A "test must link to at least one clause" check is a `minItems: 1` schema rule. Both fail under `-W`.
- **Doorstop** stores each item as a YAML file under version control. Its validation levels are:
  - ERROR: "An item's link is an invalid or unknown UID", an inactive parent link, a missing external reference.
  - WARNING: a suspect link (the parent fingerprint differs from the one recorded in the link), unreviewed changes, "A normative, non-derived item in a child document has no links", a parent item with no links from child documents, cycles, self-links.
  - `--strict-child-check` requires every parent to be linked from every child document. `--error-all` promotes warnings to errors. The CLI calls `sys.exit(1)` when validation fails.
  - Suspect links are cleared explicitly with `doorstop clear`.
  — [Doorstop validation docs](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/docs/cli/validation.md); [Doorstop CLI source](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/doorstop/cli/main.py)
  - *Inference:* Doorstop's fingerprinted suspect links put a review step into the gate. When a record decision changes, every downstream clause is flagged until someone re-reviews and clears it.
- **StrictDoc** shows parent and child links only when both items have UIDs. Circular references produce validation errors. Its statistics include "Non-root-level requirements not connected to any parent requirement". The fetched page did not document source-file (`@relation`) or test-report traceability validation, nor whether broken links fail the build. — [StrictDoc user guide](https://strictdoc.readthedocs.io/en/stable/stable/docs/strictdoc_01_user_guide.html) (B, partial)
- OSLC, ReqIF/Reqflow: not fetched in this run (gap).

**Industrial practice:**
- DO-178C added "Trace Data" as required life-cycle data (§11.21), expects bidirectional traceability from system requirements to software requirements, design, code and tests, and requires that test cases used for structural coverage trace to requirements (6.4.4.1.d). — secondary sources only: [captronic DO-178C slides](https://cdn2.captronic.fr/docrestreint.api/1965/bd928409c03c6b8918b1c33c81ca9d8ba9f3617c/pdf/Presentation_DO-178C_ACG.pdf), [QA Systems slides](https://www.slideshare.net/slideshow/automated-low-level-requirements-testing-for-do178c/240142230) (C). The RTCA text is [unreachable] (paywalled). ISO 26262 traceability practice was not fetched (gap).
- **Measured benefit of traceability:** Mäder & Egyed (EMSE 2015) ran a controlled experiment with 71 subjects re-performing real maintenance tasks on two third-party systems, half the tasks with traceability and half without. With traceability, subjects "performed on average 24% faster" and "created on average 50% more correct solutions". — [GI SE 2016 abstract of the EMSE paper](https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f/full) (A, abstract only; the EMSE full text is [unreachable] behind a paywall). Human-only evidence. Trace *maintenance* cost was not measured there, and I found no full-text source with trace-maintenance cost data (gap).

**Trace-link recovery (IR and LLM):**
- **LiSSA** (Fuchß et al., ICSE 2025, A) uses RAG with GPT-4o and GPT-4o-mini for three tasks: requirements → code, architecture documentation → code, architecture documentation → architecture models. Requirements → code results with GPT-4o and top-20 retrieval:
  - Benchmarks: SMOS, eTour, iTrust, Dronology RE and Dronology DD (58–211 source artefacts each).
  - Best LiSSA F1 per benchmark is roughly 0.29–0.53: eTour 0.526 (P 0.409, R 0.734); iTrust 0.290; Dronology RE 0.273; Dronology DD 0.254; SMOS 0.42.
  - IR baselines: VSM_opt F1 0.131–0.483 and LSI_opt F1 0.135–0.453. The prior state of the art, FTLR_opt, reaches F1 0.144–0.548.
  - "Correct" means agreement with each dataset's gold-standard links.
  - The authors conclude that "further research is required to improve the performance of RAG-based approaches to be applicable in practice."
  — [LiSSA PDF (KIT)](https://publikationen.bibliothek.kit.edu/1000179816/164563088)
- A KIT master's thesis (2025) found that adding context helped, but that the agentic approach "currently fall[s] short of traditional IR-based techniques" on both precision and recall. — [Klemens thesis, KIT](https://publikationen.bibliothek.kit.edu/1000190417/174831090) (D/thesis; seen only via abstract)
- Leads not verified in full text: Fuchß et al. (AIRE'25) report that LLM ensembles reach F2 comparable to IR but lag in precision ([fuchss.org](https://fuchss.org/conferences/aire25/)). TraceLLM reports F2 rising from 0.43 to 0.70 on CM1 with enriched prompts. Rodriguez, Dearstyne & Cleland-Huang, "Prompts Matter" (RE'23 workshop, A-workshop), report that small prompt wording changes and artefact order change the outputs ([arXiv 2308.00229](https://arxiv.org/pdf/2308.00229); downloaded, not analysed in depth).
- Requirement → **test** and NL decision → **formal clause** recovery: I found no LLM accuracy study for these link types (gap). Every LLM TLR figure above is requirement/documentation → code or → architecture model.

**Agents measured?** Yes, for trace *recovery* (LiSSA, AIRE'25, TraceLLM): F1 is roughly 0.2–0.55 on code benchmarks, recall-leaning. Not measured for *authoring* links at artefact-creation time, nor for decision → clause or clause → test links.

### Inferences
- *Inference:* the reliable design writes each link when the artefact is made (the clause cites `decision~X~rev`, the test cites `clause~Y~rev`) and lets a deterministic tracer (OFT, sphinx-needs or Doorstop) fail on `ORPHANED`, dead, missing-coverage, `OUTDATED` and duplicate links. LLM recovery belongs only in an *audit* role: flag a probable missing link, for example a test whose text matches a clause it does not cite. Given precision ≤ 0.6, a human or a second check must confirm each flag.
- *Inference:* a link gate shows only that links *exist* and are not stale. It does not show that the linked test actually binds the clause. That second question belongs to mutation (Q2): mutate the clause or the reference model and check that the linked test fails.

### Gaps
- OSLC, ReqIF/Reqflow, Polarion/DOORS practice: not fetched.
- No full-text figures on trace maintenance cost (DO-178C / ISO 26262).
- No LLM trace-recovery study for requirement → test or prose → formal clause.
- StrictDoc's link-validation and fail-on-broken-link behaviour is unconfirmed.

---

## Q2. Mutation of the spec, the models and the reference model (IronSpec, MutDafny, MuAlloy, TLA+, Python), and mutating the reference model so that both test families must kill mutants

### Takeaway
Spec mutation works and is cheap at small scale, and it finds real spec bugs.
- **IronSpec** (Dafny) found spec weaknesses in verified systems, though 13 of its 61 surviving mutations were intended weaknesses (false positives).
- **MutDafny** (implementation mutation used to expose weak specs) found 5 weak specs in 794 programs, but most survivors needed manual triage.
- **μAlloy's mutant-killing test suites** detected 91.8% of 25,180 real faulty Alloy4Fun models, even though its operators could *reproduce* only 11% of those faults.
- For **TLA+**, there is no mature tool. The new LLM benchmarks use a simple "replace the invariant with TRUE / mutate the invariant" vacuity probe, and it removes most LLM "passes".

No study tests the brief's seed directly (one mutant reference model per clause, which both test families must kill). The closest analogues mutate the implementation or outputs and require the spec or contract to reject them.

### Cited Findings
**Dafny spec mutation: IronSpec** (Goldweber et al., OSDI 2024, A) — [NSF PAR PDF](https://par.nsf.gov//servlets/purl/10550356)
- Three components: an Automatic Sanity Checker (e.g. HIGH flag "None of the postconditions depend on any of the input"; MED flag for postconditions that constrain only some fields of a complex output); Spec-Testing Proofs (STPs, unit-test-like lemmas for concrete values); and spec mutation testing.
- Mutation runs "only if the system has a passing proof".
  - Operators: LOR, ROR, COI, UOR, ENO, VNOR, plus new SOR (set membership) and HOR (heap).
  - Each mutant goes through three passes. (1) Logical redundancy: discard the mutant if it is equivalent to or weaker than the original, checked by an automatically generated lemma `∀p. S′(p) ⇒ S(p)`. (2) Vacuity: discard it if it makes the caller vacuous, checked along the full call path. (3) Full proof: the mutant stays "alive" if the whole proof still passes with the stronger spec, meaning the spec is weaker than the implementation.
  - Survivors are arranged in a DAG, and only its roots are shown.
- Evaluation covered 14 specs: 6 in-house, 2 from Abreu et al., and 6 real systems (QBFT, DVT, TrueSat, Eth2.0, daisy-nfsd, AWS Encryption SDK).
  - In total, 10 spec bugs across the 6 real systems, all confirmed by their authors.
  - The Automatic Sanity Checker alone found 5 bugs in 3 specs: only TS1 came from a HIGH flag; the other four were found "in less than an hour" each from MED flags.
  - STPs: all bugs introduced into the contrived specs were found by 70 STPs, of which 30% needed about 1.7 extra proof lines. In QBFT, STPs found 3 bugs that cancelled each other out (two made the spec weaker, one stronger).
- Mutation testing gave hints that led to spec bugs in 2 verified codebases (DVT, daisy-nfsd).
  - Of 61 surviving mutations across all specs, 13 were false positives: the weakness was intended.
  - Runtime ranged from 3 s on small specs to 80–191 min for QBFT/DVT, dominated by re-running the full proof. Mutant counts per target ranged from 11 to 197.
  - Manual effort: a full STP suite took "a few hours to multiple days" for QBFT/DVT. Focused STPs per surviving mutation took "tens of minutes to hours". The daisy-nfsd bug took 1–2 h end to end.
- Agents measured? No: human-only evidence.

**MutDafny** (Amaral, Mendes, Campos, arXiv Nov 2025, A-pre) — [arXiv 2511.15403](https://arxiv.org/html/2511.15403v1)
- It mutates the *implementation*: if a mutant still verifies, the spec is weak.
- 32 operators: 22 adapted from other tools, 10 mined from 1,475 Dafny bug-fix commits.
- Corpus: 794 programs (743 DafnyBench, 17 AWS Encryption SDK, 34 Dafny-EVM).
- 112,810 mutants: 63.65% killed, 27.94% survived, 9,019 invalid; average mutation score 79%.
- Manual review of 284 survivors from 24 files: 77 pointed to weak specs, 157 were equivalent, 50 were inconclusive. That yielded 5 distinct weak specifications in 5 programs ("roughly one every 241 lines of code").
- Cost: about 18 minutes per file on average, and about 1.7 minutes of manual review per surviving mutant.
- 3 of the 5 weak-spec programs came from an **LLM-generated** set (Misu et al. 2024). This is indirect agent evidence: LLM-written Dafny specs carried weak postconditions that verification passed.
- IronSpec, as described by MutDafny, detected 2 spec faults across 14 Dafny methods.

**Alloy model mutation: μAlloy / AUnit**
- μAlloy (Wang, Sullivan, Khurshid, ICSE 2018 demo, A-workshop; demo paper [unreachable], described via Jovanovic et al.) generates AST-level mutants, prunes equivalent ones with the Analyzer, generates an AUnit test that kills each non-equivalent mutant, and reports a mutation score.
- Jovanovic, Patwary & Sullivan (FormaliSE 2025, A) used Alloy4Fun: 97,755 submissions over 17 models, deduplicated to **25,180 unique faulty submissions**. Results:
  - μAlloy's original first-order operators can *correct* (produce a mutant equivalent to the oracle solution) only **10.96%** of real faulty models. With new operators derived from common mistakes, the figure is **17.72%**.
  - Yet the mutant-killing test suites **detect 91.78%** of the faulty submissions with the original operators and **95.79%** with the new ones. Detection was weakest on the most complex models (cv_v1, cv_v2, trainstation_ltl): the new operators bring these to at least 88.49%.
  - The authors: "fault detection and correct[ion] are not tightly coupled for Alloy models". Real user mistakes are often second-order (e.g. writing `a in b` for `some a & b`). Second-order mutants overlap real mistakes well but cost too much (over 1,600 per predicate).
  - Threat to validity: novice users only.
  — [FormaliSE'25 PDF](https://allisonius.github.io/files/FormaliSE2025.pdf)
- μAlloyτ (temporal Alloy, SoSyM 2025) was seen only in a search extract (lead).

**TLA+ spec mutation**
- I found no dedicated TLA+ mutation tool or study of TLC mutant-kill rates.
- Two 2026 LLM benchmarks use mutation as a *vacuity gate*:
  - **TLA+-Bench** (arXiv 2607.23425, A-pre): for each spec that passes TLC, "replace every checked safety invariant named by the configuration with the literal TRUE and re-run TLC". Of 30 TLC-passing outputs, 18 were testable and **only 5 of the 18** survived the probe; the paper calls the rest vacuous. Across all 300 outputs (3 frontier models × 100 specs), the mutation-surviving rate was **1.7%**, against a 10.0% default "correct" rate and 4.0% "substantive". The authors' wording of the probe is internally hard to parse (it says a pass "survives when the mutated run still fails"), so the exact mechanics should be re-checked. The 1.7% figure is stated as a conservative lower bound. Per-model plain TLC-correct rates: Claude Opus 4.5 16%, Gemini-2.5-pro 10%, GPT-5 4%. — [arXiv 2607.23425](https://arxiv.org/pdf/2607.23425)
  - **TLA-Prover** (arXiv 2606.06133, A-pre) defines tiers: Bronze (parses), Silver (no warnings), Gold (passes TLC), Diamond (Gold, *and* an automated AST-level mutation of the invariant must make TLC produce a counterexample). The stated aim is to catch "always-true" invariants such as `TypeOK == TRUE`. Across 25 LLMs the best public baseline reached 8.6% semantic model-check. The fine-tuned 20B model reached 9/30 at both Gold and Diamond (DPO variant: 20% Diamond). — [arXiv 2606.06133](https://arxiv.org/pdf/2606.06133)
- Black/Okun/Yesha (ASE 2000; spec mutation operators for model-checker test generation) and Ammann & Black: full texts [unreachable] (UMBC host returned 503, NIST mirror had a TLS error). A search extract says the method mutates the spec and uses a model checker to compare mutants with the original, either to generate tests (counterexamples) or to evaluate coverage, and that the operators form a detection hierarchy. Lead only.

**Mutating the implementation or reference model to measure spec/contract completeness (closest analogues to the brief's seed)**
- **NL2Contract** (Richter & Wehrheim, arXiv 2510.12702, A-pre) approximates contract completeness with "buggy code mutants" of the reference implementation. A verifier given a verification-sound LLM-generated contract "can discriminate over three-quarters of the buggy code mutants". Agents measured: yes, LLMs write the contract, and the mutants measure its completeness. — [arXiv 2510.12702](https://arxiv.org/pdf/2510.12702)
- **SpecRL** (arXiv 2604.05820, A-pre) builds "spectests": real inputs paired with *mutated* outputs that the implementation cannot produce (e.g. returning 100 for max of [3,1,4,1,5]). It rewards specs by the fraction of spectests they reject. On DafnyComp-Spec, the 7B model gained +49.96% (relative) in verification success and +26.46% in completeness over SFT. — [arXiv 2604.05820](https://arxiv.org/pdf/2604.05820)
- *Inference:* SpecRL's output-mutation spectests are the cheapest form of "mutant reference model per clause" for value-domain clauses. Keep the input, perturb the output, and require that (a) the spec rejects it and (b) some test in each family fails against a reference model patched to return it.

**Python mutation tools**
- **mutmut** (B, README) mutates literals, operators and `break`/`continue`, and runs pytest. It selects relevant tests per function, works incrementally (only changed functions are re-tested; stop and resume), can drop mutants that fail `mypy`/`pyrefly` type checks, has a TUI browser, and exports CI stats (`export-cicd-stats`). It needs POSIX fork. — [mutmut README](https://raw.githubusercontent.com/boxed/mutmut/main/README.rst)
- cosmic-ray and mutatest were not fetched (gap).
- Industrial scale: Google showed surviving mutants in code review over 6 years with about 15 million mutants. Developers exposed to mutants wrote more tests and stronger ones, and mutants were coupled to past real high-priority faults. — [Petrović, Ivanković, Fraser, Just, ICSE-SEIP 2021, arXiv 2103.07189](https://arxiv.org/abs/2103.07189) (A)

**LLM-generated mutants (agents doing the mutation step)**
- Wang et al. (TOSEM 2025, A) used 851 real Java bugs (Defects4J 2.0: 605; ConDefects: 246) and over 701,400 mutants. LLM-generated mutants reached a 76.47% real-bug detection rate against 44.15% for rule-based tools (1.75×). LLMut with DeepSeek-671b reached 91.1%, against PIT 40.1%, Major 66.9% and LEAM 63.9%. The best coupling rate was 52% (LLMorpheus). The cost is worse compilability and more duplicate and equivalent mutants. — [arXiv 2406.09843](https://arxiv.org/pdf/2406.09843)
- Meta ACH (FSE Companion 2025, A): an agentic LLM tool that generates issue-specific mutants (privacy faults) and then tests that kill them. Applied to 10,795 Android Kotlin classes, it produced 9,095 mutants and 571 tests. Engineers accepted 73% of the tests, and 36% were judged privacy-relevant. The LLM equivalent-mutant detector had precision 0.79 and recall 0.47 (0.95/0.96 with preprocessing). — [arXiv 2501.12862](https://arxiv.org/pdf/2501.12862)

### Inferences
- *Inference:* two kinds of mutant answer different questions.
  - **Spec/model mutants** (IronSpec style: stronger variants of a clause, killed by the proof or by the reference model) ask whether the clause is weaker than intended.
  - **Reference-model mutants** (MutDafny, NL2Contract and SpecRL style) ask whether the tests and the spec bind behaviour.
  - The brief's seed needs the second kind with a *per-family* kill requirement: for each clause-linked mutant of the reference model, at least one spec-enforcing test **and** at least one expectation test must fail. A mutant killed by only one family is a finding. If only spec tests kill it, the expectation family has a hole. If only expectation tests kill it, the spec or clause may be missing something, which is a faithfulness signal.
- *Inference:* triage cost dominates. IronSpec saw 13 of 61 survivors intended, and MutDafny 157 of 284 equivalent. A survivor that maps to a typed non-commitment (unspecified, optional, deliberately not promised) should be auto-classified "intended" by consulting the non-promise register. That shrinks manual triage and turns the register into checkable data.
- *Inference:* the Alloy4Fun result (11% reproduced but 92% detected) suggests that simple first-order operators already yield discriminating test suites for declarative models. Operator realism matters less for adequacy than for repair.

### Gaps
- No TLA+ or P mutation tool with published kill rates. No Lean 4 spec-mutation study found.
- No study of mutating an executable *reference model* (as opposed to an implementation) with a requirement that two independent test families both kill.
- Black/Okun/Yesha and Ammann/Black full texts unreachable.
- cosmic-ray and mutatest docs not fetched.

---

## Q3. Does mutation score track real fault detection, and specifically for specs and models?

### Takeaway
For code, mutants are coupled to most real faults (73% in Just et al.), and mutant detection correlates with real-fault detection. That correlation is **weak once test-suite size is controlled** (Papadakis et al. 2018, abstract only), but mutation-guided suites still beat random suites of equal size. Strong mutation reveals more real faults than statement or branch coverage (Chekam et al.). For **models**, the only large real-fault evidence is Alloy4Fun: mutant-killing AUnit suites detect about 92% of 25,180 real faulty models. For Dafny/TLA+ specs, evidence is case-based (IronSpec, MutDafny), not correlational.

### Cited Findings
- **Just et al.** (FSE 2014, A) studied 357 real faults in 5 open-source Java programs (321 KLOC), over 230,000 mutants, and both developer-written and generated suites. They found "a statistically significant correlation between mutant detection and real fault detection, independently of code coverage". Coupling held for 73% of real faults. 10% of faults needed a new or stronger operator, and 17% were not coupled to any mutant (an inherent limit). — [Just et al. PDF](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)
- **Papadakis, Shin, Yoo, Bae** (ICSE 2018, A) used CoreBench (C) and Defects4J (Java). Per search extracts, the correlations are weak once suite size is controlled. Even so, suites ranked high by mutation score detect significantly more faults than random suites of the same size, and mutants "can guide" testing despite the weak correlation. — [ICSE 2018 listing](https://conf.researchr.org/details/icse-2018/icse-2018-Technical-Papers/78/Are-Mutation-Scores-Correlated-with-Real-Fault-Detection-A-Large-Scale-Empirical-stu) **[unreachable]**: core.ac.uk returned 403 and the UCL/uni.lu copies failed, so the coefficients are unverified.
- **Chekam, Papadakis, Le Traon, Harman** (ICSE 2017, A) used CoREBench real faults (Make, Grep, Findutils, Coreutils), developer tests and KLEE-generated tests. They show that the "Clean Program Assumption" (coverage measured on the fixed program equals coverage on the faulty one) does not always hold. Avoiding it, "strong mutation testing has the highest fault revelation of four widely-used criteria" (statement, branch, weak mutation, strong mutation). Fault revelation "starts to increase significantly only once relatively high levels of coverage are attained" (a threshold effect). — [Chekam ICSE'17 PDF (UCL)](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)
- **Petrović et al.** (ICSE-SEIP 2021, A), at Google with about 15M mutants over 6 years: analysing fixes of real high-priority bugs gave "evidence that mutants are indeed coupled with real faults". — [arXiv 2103.07189](https://arxiv.org/abs/2103.07189)
- **Specs/models:**
  - Alloy4Fun real faulty models: μAlloy's mutant-killing AUnit tests detect 91.78% (95.79% with new operators). — [FormaliSE'25](https://allisonius.github.io/files/FormaliSE2025.pdf) (A)
  - Dafny: IronSpec surviving mutations led to real, author-confirmed spec bugs in 2 of 6 real systems ([IronSpec](https://par.nsf.gov//servlets/purl/10550356)). MutDafny found 5 weak specs (77 of 284 reviewed survivors pointed at weak specs) ([MutDafny](https://arxiv.org/html/2511.15403v1)). These are hit counts, not correlations with fault detection.

### Inferences
- *Inference:* use mutation score as a **guide to find holes**, not as a numeric target. That is the reading consistent with Papadakis 2018 (weak correlation once size is controlled) and with Petrović 2021 (behavioural benefit). Each surviving clause-linked mutant should map to a concrete test to write or a recorded "intended" decision.
- *Inference:* the coupling figure (73% coupled, 17% never coupled) gives an expected blind spot. Some real misreadings of the prose will not be single-token mutations of a clause. The independent expectation family (T3) is the hedge against that, not more operators.

### Gaps
- Papadakis 2018 coefficients unverified (full text unreachable).
- No correlational study of mutation score against real faults for TLA+, Dafny, Lean or Python reference models.
- Papadakis et al. 2019 survey (Advances in Computers) not fetched.

---

## Q4. Disconfirming search §5(b): evidence that model-based or mutation-based adequacy measures fail to predict real defects for specs or models

### Takeaway
**Result: partial disconfirmation, strongest for coverage criteria, weaker for mutation.**
- Structural coverage criteria, *including on industrial avionics models* (Simulink/Lustre-type Rockwell Collins systems), can be a poor predictor of fault finding. Suites generated to satisfy MC/DC often found *fewer* faults than random suites of equal size (up to 40.6% fewer).
- Coverage correlates only low-to-moderately with effectiveness once suite size is controlled.
- Mutation-score correlation with real faults is weak once size is controlled (abstract-level).
- For declarative models, mutant operators do not resemble real errors (11%), yet mutant-killing suites still detect 92% of real faults.
- I found **no** study showing that model-mutation adequacy fails to predict real spec/model defects. I also found no study showing it succeeds, beyond Alloy4Fun.

### Cited Findings
- **Gay, Staats, Whalen, Heimdahl** (IEEE TSE 2015, A) studied 7 industrial critical systems: 4 Rockwell Collins systems, a NASA system, and 2 infusion-pump subsystems.
  - Tests were generated by counterexample-based generation or random generation to satisfy condition, decision, MC/DC and Observable MC/DC (OMC/DC), and compared with random suites of equal size.
  - Effectiveness was measured by mutation analysis, plus real faults for 2 systems, under output-only and maximal oracles.
  - Findings: "coverage criteria satisfaction alone can be a poor indication of fault finding effectiveness, with inconsistent results between the seven case examples (and random test suites of equal size often providing similar—or even higher—levels of fault finding)". For 3 of 4 criteria, on 4 industrial systems, generated suites performed significantly worse than random (up to 40.6% fewer faults with an output-only oracle). Random suites reduced to a coverage-providing subset found up to 13.5% more faults than coverage-generated suites.
  - OMC/DC, which accounts for oracle observability, partly fixes this.
  — [Gay et al. author preprint](https://www.greggay.com/pdf/15covrisks.pdf) (only the first pages extracted; details from the abstract and introduction)
  - Relevance: these are *model-level* systems from model-based development. This is direct evidence that a model coverage metric used as a target can mislead.
- **Inozemtseva & Holmes** (ICSE 2014, A) generated 31,000 suites for 5 Java systems (up to 724 KLOC). "Low to moderate correlation between coverage and effectiveness when the number of test cases in the suite is controlled for". Also, "stronger forms of coverage do not provide greater insight" (statement, decision and modified condition coverage all assessed). Coverage "should not be used as a quality target". Caveat: effectiveness was itself measured by **mutants**, not real faults. — [Inozemtseva & Holmes PDF](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf)
- **Papadakis et al.** (ICSE 2018, A): mutation-score correlation with real faults is weak when suite size is controlled. — [ICSE listing](https://conf.researchr.org/details/icse-2018/icse-2018-Technical-Papers/78/Are-Mutation-Scores-Correlated-with-Real-Fault-Detection-A-Large-Scale-Empirical-stu) [unreachable full text]
- **Chekam et al.** (ICSE 2017, A): prior coverage/fault studies were biased by the Clean Program Assumption. Fault revelation rises only at high coverage levels, so moderate coverage targets say little. — [Chekam PDF](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)
- **Just et al.** (FSE 2014, A): 17% of real faults are not coupled to any mutant. — [Just et al.](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)
- **Alloy:** μAlloy operators reproduce only 10.96% of real faulty models, yet detect 91.78% (Jovanovic et al. 2025, A). This partly *disconfirms* operator realism and partly *confirms* adequacy. — [FormaliSE'25](https://allisonius.github.io/files/FormaliSE2025.pdf)
- **Requirements coverage on formal requirements:** Whalen, Rajan, Heimdahl, Miller (ISSTA 2006) defined requirements, antecedent and Unique-First-Cause (UFC) coverage over LTL requirements. A follow-up evaluation report reportedly found that only UFC "was consistently a good measure of test suite adequacy". Both full texts [unreachable] (UMN conservancy 403); search extracts only, lead. — [ISSTA'06 listing](https://experts.umn.edu/en/publications/coverage-metrics-for-requirements-based-testing/)
- **Vacuity of model-checked specs written by LLMs:** in TLA+-Bench, most TLC "passes" were vacuous under invariant mutation (5 of 18 testable survived). A model-checking pass is therefore itself a poor adequacy signal unless paired with a mutation probe. — [arXiv 2607.23425](https://arxiv.org/pdf/2607.23425) (A-pre)

### Inferences
- *Inference:* the disconfirming evidence hits coverage *targets* (MC/DC, statement or branch, model coverage used to generate tests) much harder than mutation. For this pipeline: clause, scenario, state and transition coverage should be **necessary-condition checks** ("every clause, scenario and non-commitment branch is hit at least once"), never optimisation targets. Mutation-based kill requirements are the better adequacy signal but still need the independent expectation family.
- *Inference:* the Gay et al. lesson about oracles (OMC/DC works because it requires the effect to reach an *observed* output) carries over directly. A reference-model test that reaches a clause but does not assert on the clause's observable effect is coverage without detection. Mutation detects that case; coverage does not.

### Gaps
- No study found of TLC/Apalache state or action coverage, or Quint/P coverage, against real spec defects.
- No study of Hypothesis/QuickCheck coverage annotations against real-fault detection.
- MC/DC critique beyond Gay et al. (e.g. Rajan/Whalen/Heimdahl ICSE 2008 on model structure) not fetched.

---

## Q5. Coverage measures that fit: clause, scenario, model state/transition, non-commitment branch, property-based-test adequacy

### Takeaway
Fail-able coverage checks exist off the shelf for model actions (TLC coverage: actions that never fire) and for PBT input distributions (QuickCheck `cover` + `checkCoverage` fails a property on statistically sound grounds). Hypothesis offers `event`/`target`/statistics as *reports* only, so a gate must be built on top. Practitioners rarely measure PBT adequacy: at Jane Street, mutation 7/30, example inspection 8/30, code coverage 2/30. Hughes's measured example shows that label distributions expose wasted test effort (about 80% of keys absent), and that model-based properties find bugs fastest. Clause, scenario and non-commitment-branch coverage have no dedicated tool. *Inference:* they fall out of trace data (Q1) plus Hypothesis events or QuickCheck labels named after clause and branch IDs.

### Cited Findings
- **TLC coverage** reports, per action and sub-action, the number of distinct states discovered and the evaluation cost, as `count:cost`. Its stated purpose is to identify "actions that never run (potential errors)". It does not report `Next` itself (it splits disjuncts) or `ASSUME`. — [TLA+ wiki, using:coverage](https://docs.tlapl.us/_export/raw/using:coverage) (B; the page is marked draft). In simulation mode, distinct-state counts per worker need `-Dtlc2.tool.Simulator.extendedStatistics=true` and are approximate (HyperLogLog) — [tlaplus discuss, msg06742](https://discuss.tlapl.us/msg06742.html) (C).
- **QuickCheck** (B, Haddock): `label`, `tabulate`, `cover :: Double -> Bool -> String -> prop` and `coverTable` declare required percentages. Normally "a failed coverage check does not cause the property to fail". `checkCoverage` "uses a statistical test to account for the role of luck… It will run as many tests as needed until it is sure about whether the coverage requirements are met. If a coverage requirement is not met, the property fails". `checkCoverageWith Confidence{certainty, tolerance}` tunes it. — [QuickCheck docs](https://hackage.haskell.org/package/QuickCheck-2.14.3/docs/Test-QuickCheck.html)
- **Hypothesis** (B, API docs):
  - `event()` marks custom events, whose percentages appear under `--hypothesis-show-statistics` and in observability output. Statistics also report invalid test cases and filter retries (e.g. "54.55%, Retried draw … to satisfy filter").
  - `target()` steers generation towards higher scores. It is "noticeable above max_examples=1000".
  - I found no built-in fail-on-insufficient-coverage equivalent to `checkCoverage`.
  — [Hypothesis API reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html)
  - *Inference:* a gate needs a wrapper that reads the observability output or statistics and asserts minimum event frequencies.
- **Hughes, "How to Specify It!"** (TFP 2019, LNCS 2020, A), on a BST with 8 planted bugs:
  - Validity properties miss 5 of 8 bugs. Every bug is found by at least one postcondition, metamorphic property and model-based property.
  - Model-based properties find every bug in their operation and fail fastest: union bug in 8.4 tests on average against 50 for the logically equivalent postcondition, measured over 1,000 seeded runs per property and bug.
  - An invalid generator (bug #2) causes false failures across properties, "This is why prop ArbitraryValid is so important".
  - A `label` measurement over a million tests showed the key was absent from the tree in 79.2% of cases. Generation was then retuned to balance present and absent keys.
  — [Hughes PDF (Chalmers)](https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf). Human-only evidence; n = 8 bugs, 1 data structure.
- **Goldstein et al., "Property-Based Testing in Practice"** (ICSE 2024, A): 30 interviews (31 participants) at Jane Street. Participants "struggl[ed] to generate distributions of test data" and "lamented the lack of visible feedback" on testing effectiveness. How they validated PBT tests: mutation testing 7/30, example inspection 8/30, code coverage 2/30, property coverage 1/30. 3 of 11 stopped improving properties after seeing a couple of bugs caught. Research opportunities RO6/RO7: better tools for evaluating testing effectiveness and generator distributions. — [Goldstein et al. PDF](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf). Human-only evidence (qualitative).
- **Requirements-level coverage** on formalised requirements (requirements, antecedent and UFC coverage over LTL; Whalen et al. ISSTA'06) — [listing](https://experts.umn.edu/en/publications/coverage-metrics-for-requirements-based-testing/), [unreachable] full text. This is the closest published analogue to "clause coverage" with a defined subsumption hierarchy (UFC strongest).
- Quint and P coverage features: not fetched (gap).

**Agents measured?** Not for coverage design or coverage-gated PBT. No study found of LLMs writing `cover`/`event` requirements or tuning generators for distribution targets (gap).

### Inferences
- *Inference:* a fitting set of coverage gates for this pipeline, each a necessary condition only:
  1. **Clause coverage:** every clause ID has at least one linked spec-enforcing test (an OFT `utest` coverage type or a sphinx-needs back-link).
  2. **Scenario coverage:** every record scenario has at least one linked expectation test. Same mechanism, different artefact type, so OFT can require `(stest, etest)` per decision.
  3. **Case-table row coverage:** every row of each complete-and-disjoint case table is hit, via `event("clause:C12/row:3")` or QuickCheck `cover 1 (row==3) "C12.r3"` + `checkCoverage`.
  4. **Non-commitment branch coverage:** for each unspecified, optional, profile-declared or indeterminate point, the oracle's accept-set branch is exercised for *each* allowed outcome at least once. A Hypothesis event per outcome value, with an asserted minimum frequency.
  5. **Model action coverage:** TLC coverage with zero never-fired actions. The same for state-transition tables in the reference model: every (state, operation) cell is hit by stateful tests.
  6. **Generator health:** invalid-case and filter-retry rates under a threshold, from Hypothesis statistics, plus a validity property run first (Hughes).
- *Inference:* none of these predict faults on their own (Q4). They exist to make "a clause or branch was never exercised" a hard failure early and cheaply, before the more expensive mutation stage.

### Gaps
- No evaluation of non-commitment-branch coverage anywhere.
- No Quint/P coverage docs fetched.
- No tool for scenario coverage besides generic trace tools.
- No evidence on LLMs writing coverage annotations.

---

## Q6. How T1–T4 checks compose into one gate sequence, and which must pass before later steps start (fail early)

### Takeaway
I found no published pipeline with ordered gates spanning prose → spec → model → reference model → two test families. The published orderings are partial:
- tiered LLM-spec gates: parse → no warnings → model-check pass → mutation-sensitive (TLA-Prover);
- IronSpec's rule that spec mutation runs only after a passing proof, with cheap sanity checks first;
- Hughes's rule that the generator-validity property runs before others to avoid false failures;
- DO-178C's requirement that trace data be produced and verified as life-cycle data.

AWS's ordered use of methods (design-time TLA+/P, then PBT, then runtime PObserve) could not be verified (403). A composed sequence is therefore *inference*, anchored on these orderings and on cost data (seconds for link checks, minutes to hours for mutation).

### Cited Findings
- **TLA-Prover tiers:** Bronze (parses) < Silver (no warnings) < Gold (passes TLC) < Diamond (an invariant mutation must produce a TLC counterexample). Each tier presupposes the previous one. "Gold and Diamond coincide at every checkpoint" after training, which the authors read as Diamond preventing the trivial-property failure mode. — [arXiv 2606.06133](https://arxiv.org/pdf/2606.06133) (A-pre)
- **TLA+-Bench grading regimes**, in order of strictness: configuration-aware 18.7% → default 10.0% → substantive (the pass must exercise behaviour) 4.0% → mutation-surviving 1.7%. Each stricter gate removes passes the previous one accepted. — [arXiv 2607.23425](https://arxiv.org/pdf/2607.23425) (A-pre)
- **IronSpec ordering:** cheap automatic sanity checks first (seconds), then STPs, then mutation "only if the system has a passing proof". Within mutation: logical-redundancy pass → vacuity pass → full proof. Cost scales with full-proof time (about 1 h for one QBFT proof run). — [IronSpec](https://par.nsf.gov//servlets/purl/10550356) (A)
- **Hughes:** run `prop_ArbitraryValid` first, because an invalid generator makes unrelated properties fail. — [Hughes](https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf) (A)
- **OFT transitive defects:** an item covered correctly but covering a defective item is `not ok (transitive)`, and `direct_failures` reports only root causes. That gives upstream-first fixing order. — [OFT docs](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/console_tracing_report.md) (B)
- **Doorstop suspect links:** a change upstream flags every downstream link until it is re-reviewed (`doorstop clear`). This works as a change-triggered gate. — [Doorstop validation](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/docs/cli/validation.md) (B)
- **DO-178C:** trace data is required life-cycle data. Structural-coverage tests must trace to requirements. — secondary sources (C), standard [unreachable].
- An arXiv preprint describes a "lean and highly-automated" DO-178C/DO-331 model-based process with an autopilot case study, but its abstract gives no gate ordering or measured data. — [arXiv 2010.06505](https://arxiv.org/abs/2010.06505) (A-pre, abstract only)
- **AWS "Systems Correctness Practices"** (Brooker & Desai, CACM 2025): TLA+ and P for design, PObserve checking production logs against P specs, PBT (ShardStore), fuzzing. — [CACM](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services) **[unreachable]** (403; search extract only), so ordering and figures are unverified.

### Inferences
*Inference* (proposed gate sequence, cheapest and most upstream first; each gate blocks the next stage for the affected clause or operation, not the whole project):

| # | Gate (track) | Fails on | Typical cost | Blocks |
|---|---|---|---|---|
| G0 | ID/schema lint (T4) | missing or duplicate IDs, malformed normative form, missing non-commitment type | seconds | everything |
| G1 | Upward trace (T4) | clause without a `decision~rev` link (orphan or added commitment), decision without a clause (lost case), `OUTDATED` link | seconds | spec review |
| G2 | Faithfulness exhibition (T1) | rejected witness scenario or back-translation | human or agent minutes per clause | modelling |
| G3 | Form-local checks (T2) | case table not complete or not disjoint; transition table cell missing | seconds | modelling |
| G4 | Cross-clause consistency and satisfiability (T2) | SMT/Alloy unsat, Dafny contract inconsistency, realizability | seconds to minutes | modelling |
| G5 | Vacuity and non-triviality (T2/T4) | model passes with invariant replaced by TRUE; IronSpec-style sanity flags; mutated invariant not caught | seconds to minutes | reference-model build |
| G6 | Model ↔ reference-model conformance (T3) | differential or trace-validation mismatch | minutes | test-family work |
| G7 | Downward trace and coverage (T4) | clause without a spec-test link, scenario without an expectation-test link, never-fired TLC action, uncovered table row or non-commitment branch, generator invalid rate too high | seconds (link) to minutes (coverage run) | mutation stage |
| G8 | Per-family mutation kill (T4) | a clause-linked reference-model mutant not killed by **both** families, unless it maps to a registered non-promise | minutes to hours | release of spec version |
| G9 | Spec-strength mutation (T4, IronSpec style) | a stronger variant of a clause still passes all proofs and tests (weaker than intended) | minutes to hours; needs G4–G6 green | release |

- *Inference:* G1 and G7 are separate gates on purpose. Upward links catch added or lost commitments early, before modelling. Downward links can only be checked once tests exist.
- *Inference:* G5 must come before trusting any model-checking pass (TLA+-Bench, TLA-Prover). G8 and G9 must come after G6, since mutating a reference model that does not conform to the formal model measures the wrong thing. This matches IronSpec's "only if the proof passes".
- *Inference:* G8's per-family requirement is the operational form of T3 independence. Its failure pattern (killed by one family only) is a diagnostic signal routed back to T1.

### Gaps
- No published end-to-end ordered pipeline matching the brief, consistent with §5(c), which T1/T5 notes also cover.
- AWS practice article unreachable.
- DO-178C objective tables not read in the original.
- No cost data for running such a sequence per operation.

---

## Q7. Summary: were agents/LLMs measured doing each T4 step?

### Takeaway
LLMs have been measured on trace-link recovery (moderate, F1 ≈ 0.2–0.55 on code benchmarks), on generating mutants (better real-bug coupling than rule-based tools on Java), on mutant-killing test generation at Meta (73% acceptance), and on the *output* side of spec mutation (most LLM TLA+ passes are vacuous; LLM-written Dafny specs carry weak postconditions that mutation exposes). Agents have **not** been measured authoring trace links, designing coverage requirements, triaging surviving spec mutants, or running a per-family mutant gate.

### Cited Findings
- Trace recovery: LiSSA (GPT-4o), best F1 0.25–0.53 across 5 requirement → code benchmarks. — [LiSSA](https://publikationen.bibliothek.kit.edu/1000179816/164563088) (A)
- Mutant generation by LLMs: 76.47% against 44.15% real-bug detection over 851 real Java bugs. — [Wang et al. TOSEM'25](https://arxiv.org/pdf/2406.09843) (A)
- Agentic mutation-guided test generation: Meta ACH, 9,095 mutants, 571 tests, 73% accepted; LLM equivalent-mutant detection P 0.79 / R 0.47. — [ACH](https://arxiv.org/pdf/2501.12862) (A)
- LLM-written TLA+ under a mutation/vacuity probe: 1.7% of 300 outputs survive (against 10% plain TLC-correct). — [TLA+-Bench](https://arxiv.org/pdf/2607.23425) (A-pre). TLA-Prover: 25 LLMs, best baseline 8.6% model-check; fine-tuned model 30% Gold = Diamond on 30 problems. — [TLA-Prover](https://arxiv.org/pdf/2606.06133) (A-pre)
- LLM-written contracts measured by code mutants: a verification-sound contract discriminates more than three-quarters of buggy mutants. — [NL2Contract](https://arxiv.org/pdf/2510.12702) (A-pre). SpecRL: output-mutation spectests as an RL reward improve completeness by 26.46% relative. — [SpecRL](https://arxiv.org/pdf/2604.05820) (A-pre)
- MutDafny: 3 of 5 discovered weak specs were in LLM-generated Dafny programs. — [MutDafny](https://arxiv.org/html/2511.15403v1) (A-pre)
- Human-only: IronSpec (spec mutation and STPs), μAlloy/Alloy4Fun, Hughes (property types and labels), Goldstein (PBT adequacy practice), Mäder & Egyed (trace benefit), Gay et al. (coverage criteria), all trace tools.

### Inferences
- *Inference:* the agent evidence supports making mutation probes *mandatory* gates on agent-written specs and models. Without them, agent "passes" are mostly vacuous (TLA+-Bench) or weak (MutDafny). Gates must stay non-editable by the producing agent, consistent with the §3 baseline on agents gaming editable checks.
- *Inference:* LLM equivalent-mutant detection (ACH: P 0.79 / R 0.47 raw) is a usable *pre-filter* for survivor triage. It is not a replacement for checking against the non-promise register.

### Gaps
- No measurement of agents authoring or maintaining trace links.
- No measurement of agents triaging IronSpec-style survivors or writing STPs.
- No measurement of agents writing coverage requirements (`cover`/`event`).
- No measurement of agents operating a per-family kill gate.
