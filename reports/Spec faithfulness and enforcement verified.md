# Prove the spec wrong before building on it (verified edition)

This edition checks every load-bearing claim of the earlier report "Prove the spec wrong before building on it" against full texts (160 log rows: 93 confirmed, 51 corrected, 2 refuted, 1 not found, 13 unverifiable). The design it recommends survives. Most corrections are "right number, missing qualifier". **Two baseline challenges fall.** The Cedar "§3 challenge" was a misreading of the earlier brief. The Porcupine "§3 challenge" rests on one preprint by competing-tool authors and is now a qualification. **The Kernsatz is restated at the strength the full texts carry.** The headline "about 90 % with three tests" holds only as a per-requirement mean for one LLM on Alloy structural models with student-written wrong specs (now graded A, FM 2026). "LLM errors are correlated" is a multiple-choice finding. "No published pipeline" is a search result. New full texts sharpen two recommendations:
- Papadakis et al. show that mutation kills must be compared at equal suite size.
- Knight's NASA report and Eckhardt & Lee show that separately written versions still fail together on hard inputs. Information-flow isolation is therefore necessary but not sufficient.

The central claim, that prose-derived oracles catch spec misreadings that spec-derived ones miss, is still unmeasured. No recommendation rests on *direct* evidence of effectiveness for library or API behaviour specs.

The consolidated log is `research_notes/Spec faithfulness and enforcement verified/verification_log.md`. IDs in brackets (e.g. V1-10) point to its rows.

---

# Part 1. What changed in this edition

## 1.1 Substantive changes

These change a conclusion, a recommendation, a baseline status, or what a figure means.

| # | Earlier report said | This edition says | Log IDs |
|---|---|---|---|
| S1 | **[§3 challenge]** Cedar's models are Lean, not Dafny | **Refuted as a misreading of the earlier brief.** The brief never tied Cedar to Dafny (quoted in §2.7). The challenge is removed. The §3 point is **confirmed**, with a detail: Cedar's current models are Lean, and an earlier formalization was Dafny (repo READMEs, B) | V1-01, V1-02 |
| S2 | **[§3 challenge]** Porcupine cost; OmniLink "the first independent comparison" | **Downgraded to [§3 qualification].** OmniLink's authors build competing TLA+ checkers. No neutral benchmark was found. Cost depends on history shape | V1-05, V1-07, V1-08 |
| S3 | Kernsatz: "No published pipeline …" stated as fact | Stated as the earlier run's search result | V1-09 |
| S4 | Kernsatz/§2.1: "caught about 90 % of wrong specs with three tests" (A-pre) | Per-requirement mean 90 % (pooled 88 %), over the 36 of 43 requirements with a complete valid suite; one LLM; Alloy structural domain models; student-written wrong specs; **grade A** (FM 2026). The same study shows the shared-misreading limit (the "colleagues" case) | V1-10, V1-11 |
| S5 | Kernsatz: every reference-free check is "necessary-only" | Round-trip, dual formalization, compile/verify and witness checks are necessary-only. **LLM judges are not even that**: they over-accept *and* over-reject | V1-14 |
| S6 | Kernsatz: "LLM errors are correlated across models"; "independence must come from the derivation path … rather than from swapping models" | Correlation is measured on multiple-choice benchmarks. Swapping provider reduces it but not enough on its own; that conclusion is *Inference* | V1-12, V1-15 |
| S7 | Kernsatz: independence "verified by per-family mutant kills" | Kills compared **at equal test counts**. Kills guide gap-finding but do not measure real-fault detection (Papadakis: r ≈ 0.05–0.20 with size controlled) | V3-01–V3-04 |
| S8 | Independence "enforced by information flow" | Necessary, not sufficient. Separately written versions fail together on hard inputs (Knight NASA report, B; Eckhardt & Lee TM, B). Hard cases need deliberately different derivations | V3-05, V3-06, V3-08 |
| S9 | [§3 qualification] Vericoding: "found Dafny clean … 9 % of the [Verus] specs too weak, 15 % poor translations" | The 9 % + 15 % is pooled across Dafny, Verus and Lean (5 sampled successes per language and source). The "Dafny clean" carve-out is removed, so the qualification also covers Dafny | V1-46, V5-15 |
| S10 | AlgoVeri shows "some" Vericoding specs accept "return 0" | One worked problem (LIS), two languages, competing-benchmark authors, no count | V2-19 |
| S11 | MutDafny: "3 of its 5 weak specs in an LLM-generated set" | 4 of 5 were in LLM-generated programs; 3 of those 4 had been found earlier by other methods | V5-18 |
| S12 | Well-separation: "only 19 of 79 student specs … in 60 the system could win" | 79 *revisions* of six undergraduate projects; 40 of 79 under the strict semantics the students' tool used. The prevalence argument is weak; the check itself stays cheap | V5-11, V5-12 |
| S13 | TLA+-Bench: "only 5 survived invariant→TRUE"; "LLM TLA+ mostly vacuous" | As worded, the probe's survival criterion cannot show that an invariant constrains behaviour (*Inference*). The 5/18 and 1.7 % are the paper's counts, not a vacuity rate. No reliable TLA+ vacuity rate exists | V2-06, V2-07 |
| S14 | PBT-Bench: "a frontier model stops after exposing a single bug" | One model under an open-ended prompt; one "cover the specification" instruction adds +41.5 pp. This supports harness-imposed obligations, not "agents cannot cover a spec" | V2-01, V2-02 |
| S15 | SysMoBench: conformance "at most 15.38 % on Etcd Raft" across agents | Only one LLM reached conformance scoring on Etcd Raft at all (7.69 % / 15.38 %); grade A (ICLR 2026) | V2-04, V2-05 |
| S16 | Gay et al.: "up to 40.6 % fewer" (first pages only) | Full text: up to −59.2 % (Table 4), on the 4 Rockwell systems only. On the NASA and pump systems, and for OMC/DC throughout, generated suites matched or beat random | V2-10, V2-11 |
| S17 | (not in report) | **UFC follow-up added**: suites satisfying requirements or antecedent coverage lost to equal-size random suites. A one-test-per-clause gate is a presence check, not an adequacy signal | V4-09 |
| S18 | DTest: "Statement/path coverage of the contract"; NFM 2023 [unreachable] | Full text (A): coverage of the *implementation*, with postconditions as runtime oracles. DSpec2Test (A-pre) adds a spec-driven mode with 17 unique mutant kills | V4-03, V4-05 |
| S19 | §2.6(c): projects found real spec bugs, "Cedar about two dozen" | Cedar's 25 bugs are implementation-vs-model bugs (4 by proofs, 21 by DRT/PBT), not spec-vs-intent | V1-04 |
| S20 | Watt CPP 2018: errors "survived engines and the reference interpreter" | Clause removed; it is not in the paper | V5-16 |
| S21 | Jovanovic & Sullivan: over-constraint "harder to spot" stated as a finding | It is the authors' argument, not a measurement | V1-18 |
| S22 | Beyond Compilation: "only 4 of 54 rejections were real errors" | That figure is a two-stage *LLM* review's classification, not a human one | V1-31 |
| S23 | Beer et al.: "20 % of specifications pass vacuously" (second-hand) | FMSD 2001 full text: an IBM experience estimate with no n, from the RuleBase authors; plus about 10 % of non-vacuous passes reveal a problem via an interesting witness | V3-09 |
| S24 | Frama-C smoke tests as detection evidence | All 37 JCVM smoke-test failures were spurious: evidence of cost (≈8 %), not of industrial detection yield | V5-13 |
| S25 | Leveson 1990: spec-only checks found 19 % | The authors call ranking check types "inappropriate (and even misleading)"; spec-only checks were written first (order confound) | V5-32 |
| S26 | (not in report) | **Heitmeyer added** (A): an SCR complete/disjoint checker found 17 real coverage errors that two review teams missed, in 245 s. Coverage needs declared value domains | V3-10 |
| S27 | (notes) Cleanroom as evidence for independent testing | Removed: both arms of Selby et al. had the same independent testing | V3-11 |
| S28 | Watt et al. FM 2021 expected to be dual-formalization evidence (debt) | Refuted: two mechanisations, no cross-comparison | V4-11 |
| S29 | (not in report) | **Katis CAV 2022 added**: FRET's minimal cores overturned a published human diagnosis of unrealizability (anecdote) | V4-07 |
| S30 | Arm 2017: property set "written from the NL manual" | Written from the NL manual, recent bugs and discussion with architects | V1-41 |
| S31 | Bosch: "50–701 requirements", "1m33s–4h14m" | 26–701; 48 s – 4h14m | V5-02, V5-05 |
| S32 | Mäder & Egyed figures (abstract only) | Still **unverifiable** at full-text level. Consistent with the authors' 2-page summary: 461 task solutions were *sketched on paper*, not implemented | V2-12, V2-13 |

## 1.2 Restyled, grade-only and qualifier changes

These change no conclusion.

| Change | Log IDs |
|---|---|
| Grades raised to A: Cunha & Macedo (FM 2026), Cedar FSE (FSE Companion 2024), FormalAlign (ICLR 2025), SysMoBench (ICLR 2026), AlgoVeri (ICML 2026), Cirstea et al. (SEFM 2024), CCF (NSDI 2025), DMN (BPM 2016), SAT-LLM (ASE 2024, short), Jin & Chen (ASE journal 2026), Choi et al. (NeurIPS 2025), DTest (NFM 2023) | V1-03, V1-10, V1-36, V1-38, V2-04, V2-14, V2-16–V2-19, V4-03, V5-07 |
| PROPAS venue verified (ACM SIGAPP ACR 17(4)); number of injected faults not stated | V2-15 |
| Req2LTL "inconsistent definition" resolved: two metrics on two datasets | V2-08, V2-09 |
| Roundtrip cost: 6.1–26.4 calls per repair across runs, not one cell; annotator is an author | V1-19 |
| NeuroSTAR: "up to 48.43 %" filtered, for listed reasons; majority-of-raters protocol; tool authors | V1-22 |
| Greenman: rounds 2–4, not four rounds | V1-24 |
| DMN comparator is Signavio's checker, not a "naive algorithm" | V2-16, V5-08 |
| Mocket: 7 implementation + 2 spec bugs; Cedar 9.7 % from an added generator; Meta ACH 73 % of *reviewed* tests; Maaz $9.93 an upper bound (n = 50 from the top 80 %); MutDafny v2 totals; LiSSA not best everywhere; FRET mode variables "one reason"; Spectra specs are revision histories; Bosch 70 % includes typos and questions, initial formalisation costly | V5-03, V5-06, V5-09, V5-10, V5-22, V5-28, V5-31, V5-43, V5-45, V5-49 |
| OmniLink bugs: 1 in BAT, 1 in ConcurrentQueue (not WiredTiger) | V1-06 |
| Clover qualification re-sourced to Clover's own appendix | V1-45 |
| Independence flags added (vendor, tool authors, competing benchmark) throughout | all |
| Debt rows resolved or re-labelled (Katis, Leino–Wüstholz, Huo & Clause, Mashkoor & Jacquot, Melnik & Maurer 2007, Heitmeyer, Selby, Papadakis, Beer, IV&V, AWS) | V3-*, V4-* |

---

# Part 2. Corrected report

Grades follow the brief: A, A-pre, A-workshop, B, C, D. **[unreachable]** means the full text was not fetched, so the item is a lead only. *Inference* marks reasoning that is not itself a finding of any source. Every method states whether **agents** (LLMs) were measured doing that step. If they were not, it says "human-only evidence". Measured figures give n, setting, and what "correct" meant. Independence flags: **TA** = tool or method authors on their own tool; **V** = vendor self-report; **CB** = competing-tool or competing-benchmark authors. The earlier brief's §3 baseline is taken as given. Before any remaining **[§3 qualification]**, the baseline text is quoted verbatim, followed by what exactly it contradicts.

## §1 Kernsatz

The earlier run's search found no published pipeline that runs prose records → spec → formal models → executable reference model with gates that check faithfulness to the prose, so the best-supported design is assembled from analogues: turn each record's scenarios and rejected options into spec-blind positive and negative checks before the spec exists (in the one measured analogue, Cunha & Macedo, FM 2026, A, on Alloy structural domain models with student-written wrong specs and one LLM, three tests of each kind detected on average 90 % of wrong specs per requirement over the 36 of 43 requirements with a complete valid suite, 88 % pooled), conjoin all normative forms over one shared vocabulary to check conflicts, vacuity and satisfiability over environment moves, and bind the reference model with two test families separated by information flow and compared by per-family mutant kills at equal test counts. Round-trip, dual-formalization, compile/verify and witness-validity checks are necessary-only and blind to misreadings both legs share, LLM judges both over-accept and over-reject, LLM errors are correlated on multiple-choice benchmarks (more so within a provider; Kim et al., ICML 2025), and separately written program versions fail together on hard inputs (Knight, NASA report, B), so by *Inference* independence needs deliberately different derivations, not only separate writers or swapped models. That prose-derived oracles catch spec misreadings that spec-derived ones miss has no head-to-head measurement, and a small trial on one operation can measure it.

---

## §2 Findings per track

### 2.1 T1 Faithfulness: prose → spec, proved wrong early

**Core finding.** Round-trip and dual formalization catch *divergent* readings. By construction they miss *shared* misreadings, as Roundtrip, NeuroSTAR and Clover each state ([Roundtrip](https://arxiv.org/abs/2604.25031); [NeuroSTAR](https://arxiv.org/abs/2609.03161); [Clover App. A.4.1](https://arxiv.org/abs/2310.17807)) [V1-17]. The strongest measured mechanism that needs no gold formula derives concrete positive and negative examples from the NL source without seeing the spec, then requires the spec to accept the positives and refuse the negatives ([Cunha & Macedo, FM 2026](https://arxiv.org/abs/2510.23350)) [V1-10]. Exhibition (traces, instances, witnesses) shows under-constraint as an unexpected scenario. Jovanovic & Sullivan *argue*, without measuring it, that over-constraint is harder, because the user must notice an expected scenario that never appears among "hundreds" ([source](https://par.nsf.gov/servlets/purl/10615156)) [V1-18].

| Option | Evidence (grade; n, setting, "correct") | Catches | Misses | Cost | Agents |
|---|---|---|---|---|---|
| **Round-trip**: formalize → back-translate → re-formalize → equivalence | Amrollahi, Lopez, Barrett (A-pre). 227 Texas statutes (150 traffic + 77 wildlife), many-sorted FOL, Z3. Equivalence 44.7–67.1 % before repair, 78.9–85.7 % after a K=3 diagnose-and-repair loop (90.7 %/94.7 % with cross-provider diagnosis). "Correct" = Z3 equivalence, which the authors call "necessary but not sufficient". Audit: one author with formal-methods training, 25 rules: 1 minor error among 14 equivalent vs 3 among 11 non-equivalent ([source](https://arxiv.org/abs/2604.25031)) [V1-19] | Divergent readings | Omissions shared by both legs; stable wrong fixed points | 6.1–26.4 LLM calls per full repair across six runs; regeneration was cheaper in some runs [V1-19] | Measured |
| **Equivalence against a second formalization** | Poiroux et al., EMNLP 2025 (A). 3,752 Lean pairs with human labels: BEq+ P 98.0 / R 48.3; BEqL P 100 / R 30.9; type-check rate "can not be used as a substitute for human evaluation" ([source](https://arxiv.org/abs/2406.07222)) [V1-20] | Proven equivalence = strong evidence of agreement | Half of true equivalences unproven | Low once both exist | Measured |
| **Independent dual human formalization** | Easterbrook & Callahan, RE'97 (A; TA). Four people, one NASA FDIR requirement → **four different** AND/OR tables. Comparing tables was "much easier" than comparing prose. n = 4, no statistics ([source](https://ntrs.nasa.gov/api/citations/19970007163/downloads/19970007163.pdf)) [V1-21]. Watt et al. FM 2021 is **not** dual-formalization evidence: its two mechanisations were never cross-compared [V4-11] | Ambiguity, row by row | Shared errors | One extra formalization | Human-only evidence |
| **Multiple generators + difference witnesses + judge** | NeuroSTAR (A-pre; TA). 87.8 % vs 86.2 % equivalence to gold on filtered ConfoNLf. On 108 driving-law sections, 89/106 (83.9 %) shortest violating traces were judged valid by a majority of author raters (two, a third on disagreement): a necessary condition only ([source](https://arxiv.org/abs/2609.03161)) [V1-22] | Divergence, shown as a checkable case | Generators "can produce the same wrong formula together" | Several generations + automata | Measured (judge precision not reported) |
| **Paraphrase / explanation review** | FRET Lockheed Martin case (A; TA): explanations were "instrumental" in ensuring FRETish captured intended semantics ([source](https://ntrs.nasa.gov/citations/20205000433)) [V1-23]. Greenman et al. (A): across survey rounds 2–4 (students, 29 researchers, talk-aloud), LTL→English 15–24 % wrong, English→LTL 28–47 % wrong (semantic equality) ([source](https://arxiv.org/abs/2211.01677)) [V1-24] | Misreadings visible to a reader | Shared errors; operator misconceptions | Human minutes per requirement | Human-only evidence |
| **Structured intermediate + mechanical translation** | Req2LTL, ASE 2025 (A; TA). 112 industrial aerospace requirements, GPT-4o: 88.4 % vs 65.2 % (NL2TL), 56.3 % (nl2spec), 55.4 % (NL2LTL), 43.8 % zero-shot (DeepSeek-V3: 86.6 %). "Correct" on this set = two experts independently agree on semantic equivalence to a gold formula. String match was used only on academic sets. No automatic equivalence checker. The 13/112 formulas engineers fixed in ~10 min with a diagram view are outside the headline numbers ([source](https://arxiv.org/abs/2512.17334)) [V1-25, V2-08]. FRET: 69/74 requirements captured; FRETish rewriting "not always straightforward" (A) | Temporal/conditional confusion, lost nesting | Residual ambiguity, context omission | Template training (Großer et al.: abstract only) | Measured (Req2LTL); FRET human-only |
| **Example tables next to prose** | Ricca et al., IWPSE 2007 (A-workshop): 15 students, 6 requirements; more correct answers with Fit tables (p = 7.5e-05); time difference not significant (p = 0.45), though the authors say tables "tend to involve additional effort" ([source](https://profs.scienze.univr.it/ceccato/papers/2007/iwpse2007.pdf)) [V1-26] | Comprehension errors | Not a check of a formalization | Low | Human-only evidence |
| **Targeted exhibition** | FRET simulator exposed the AP-003c trigger-vs-always misreading (A, no counts). Alloy4Fun, 93,283 submissions: 25.4 % correct, 45.3 % faulty, 23.28 % both over- and under-constrained (A) ([source](https://par.nsf.gov/servlets/purl/10615156)) [V1-27]. Quint `--witnesses` (B, no error data) ([source](https://quint.sh/docs/checking-properties)). Mashkoor & Jacquot (A): animation of three Event-B models, qualitative only; it found one undesirable platoon oscillation ([source](https://hal.science/hal-01262115/document)) [V4-13] | Under-constraint | Over-constraint when browsing (argued) | Low per trace | Human-only evidence |
| **Spec-blind positive/negative tests from NL, before the spec** | Cunha & Macedo, **FM 2026 (A)** ([source](https://arxiv.org/abs/2510.23350); [venue](https://conf.researchr.org/details/fm-2026/fm-2026-research-paper/14/Validating-Formal-Specifications-with-LLM-generated-Test-Cases)). From NL + Alloy domain model, without the spec, GPT-5 (few-shot) writes N positive and N negative instances. 43 structural requirements from 4 Alloy4Fun models; 28–848 (mean 157) distinct wrong student specs per requirement. "Detected" = at least one of the 2N tests gives an unexpected result. Mean per-requirement detection: 62 % (N=1), 83 % (N=2), 90 % (N=3), 93.6 % (N=5), counted only over requirements with complete valid suites (41/34/36/35/35 of 43). Pooled N=3: 88.1 % (verifier's arithmetic). 30/774 tests (3.9 %) wrong; 13 of 14 oracle errors were negatives, concentrated in 3 ambiguous requirements. The LLM repeated the students' misreading of "colleagues" in all 3 runs. Valid-test rate at N=3: 67–96 % across four models. ~$3.5 per 258 tests [V1-10, V1-11] | Lost cases (positives fail) and missing constraints (negatives pass), against real human errors | Readings the LLM shares with the spec writer; structural specs only | Cheap | Measured |
| **Concrete-I/O soundness + completeness of a spec** | Lahiri, FMCAD 2024 (A): 64 of 153 MBPP-DFY specs analysable. Soundness = admits reference output; completeness = rejects mutated outputs; ~0.66 separated strong from weak; found weak specs, one misread intent, transcription errors (25 vs 125) ([source](https://arxiv.org/abs/2406.09757)) [V1-29] | Weak specs; misreadings | Depends on test quality | 400-line script | Measured |
| **LLM judge of NL↔formal alignment** | FormalAlign, **ICLR 2025 (A; TA)** ([source](https://arxiv.org/abs/2410.10135); [OpenReview](https://openreview.net/forum?id=B5RrIFMqbe)): human experts 79.58 %, trained scorer 65.00 %. A GPT-4 judge had **26–51 % precision at 88–95 % recall** on sets with 21 synthetic negatives per positive, which depresses precision. ~3 h per 80 pairs for humans [V1-30, V2-14]. Beyond Compilation (A-pre; TA): 227 NL→Lean statements, 8 systems. Accepting only when two cross-family judges agree matched the human majority on 54/59 audited cases (91.5 %, 95 % CI 81.6–96.3) but rejected some faithful outputs (negative confirmation 10/13). Compilation overstated faithfulness by 1.3–29.5 points ([source](https://arxiv.org/pdf/2606.31002)) [V1-31, V1-14] | Gross misalignment | Shared readings; over-rejection; judge aging (§2.5) | Low per item | Measured (maths only) |

**Clause-level "says more / says less".** "Says more" (an added commitment) is over-constraint. "Says less" (a lost case) is under-constraint. Humans make exactly these operator-level errors ("ImplicitG/ImplicitF") ([Greenman et al.](https://arxiv.org/abs/2211.01677)). *Inference*: four record-derived checks follow. None is measured as such.
1. **Scenario derivability**: each record scenario's outcome must be permitted by the clause, and entailed where the decision commits. Analogue: Cunha & Macedo positives; Lahiri soundness.
2. **Rejected-option refutation**: the distinguishing behaviour of each rejected option must be refused. Analogue: negatives; mutant rejection. No source uses rejected alternatives as negatives; that mapping is *Inference*.
3. **Added-commitment probe**: generate the minimal behaviour a clause forbids (shortest violating trace, UNSAT core, failing Dafny assertion) and ask a spec-blind judge whether the record forbids it. Analogue: NeuroSTAR, where 17/106 traces were judged invalid.
4. **Non-commitment typing**: an *unspecified* set needs one positive per allowed outcome and a negative outside the set. A *deliberately not promised* item needs two witnesses with different outcomes.

Cunha & Macedo also bound this approach. Their test writer repeated a human misreading. So record-derived checks catch only the misreadings the check writer does not share [V1-11].

**Where a human must look.** Effective human checks in the sources were all made on small concrete artefacts:
- a sub-translation fragment (nl2spec: 15 of 20 initially wrong translations fixed by the authors editing fragments, 1.86 loops on average; [source](https://arxiv.org/abs/2303.04864)) [V1-28];
- a two-step trace (FRET);
- a table row (Easterbrook);
- a formula-tree diagram (Req2LTL);
- a shortest violating trace (NeuroSTAR).

*Inference*: ask humans yes / no / "not addressed" questions on one concrete case tied to one record sentence. Route to them (a) unresolved difference witnesses, (b) every "not addressed" answer from the added-commitment probe, and (c) a random audit of agent-judged witnesses.

**[§3 qualification] Clover triangulation.** Earlier brief §3, verbatim: "triangular cross-checks help (Clover);". This qualification does not contradict "help". It bounds it: agreement among legs that share a reading does not establish faithfulness. Clover's own authors state that "if the docstring, annotations, and code all miss the same edge case, the error cannot be detected" ([Clover App. A.4.1](https://arxiv.org/abs/2310.17807)). Roundtrip's audit shows equivalence and faithfulness only loosely coupled (1/14 vs 3/11, n = 25, one author-annotator) [V1-45].

**What "correct" meant.** From weakest to strongest metric (*Inference*): syntax valid < exact match < equivalence to one gold < human intent judgement < detection of real errors. Gold sets are themselves unreliable:
- NeuroSTAR's filtering removed up to 48.43 % of entries (train–test contamination, trivial formulae, temporal ambiguity, LTLf incompatibility) [V1-22].
- Lahiri found transcription errors in the human reference.
- ProofNet# exists because ProofNet needed correction.

nl2spec is closest to intent: 36 instances from 5 experts, 31/36 (86.1 %) after interactive fragment editing, judged by the authors, at least 9/36 ambiguous [V1-28].

### 2.2 T2 Conflicts and satisfiability

**Core finding.** Every working cross-form consistency checker found translates all clauses into **one common logic over one shared signature**, checks the conjunction, and returns a **minimal inconsistent subset**. Mature tools go beyond plain satisfiability to rt-inconsistency, vacuity, realizability against the environment, or divergence under a boundary condition. Those stronger notions are the evidenced answer to the brief's "consistency checks that passed but missed a contradiction" (*Inference*). Every efficacy figure below is from tool authors evaluating their own tool. No neutral benchmark exists for this tool class [V5 Q2].

| Option | Evidence (grade; n, setting) | Catches | Misses | Cost | Agents |
|---|---|---|---|---|---|
| **Common-logic conjunction + minimal inconsistent subset** | Bosch / Ultimate ReqAnalyzer, RE 2019 (A; TA + Bosch co-author): ten device sets of **26–701** requirements. "From the ca. 310 results … 100 were classified as major issues, although the requirements had been reviewed manually several times before"; the rest "await classification". "Nearly 70 % of our findings (including questions, typos, duplications, type issues)" led to requirement fixes, the rest to formalisation changes. The 263-requirement set had 6 vacuous requirements, 73 rt-inconsistencies, 18 timeouts, 3h58m ([source](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)) [V5-01–V5-06]. Hanfor (A-workshop): minimal core, timing diagram, vacuous requirements ([source](https://ultimate-pa.github.io/hanfor/references/publications/hanfor-semantic-requirements-review-at-scale.pdf)). EuRailCheck (A-workshop): a failure "cannot by itself separate" formalisation error from informal-spec flaw ([source](https://arxiv.org/pdf/1003.1741v1.pdf)). PROPAS at Scania, **ACM SIGAPP ACR 17(4) (A; TA)**: "All of the injected faults have been detected by Z3"; the number injected is not stated ([source](https://www.es.mdh.se/pdf_publications/4980.pdf)) [V2-15]. Katis et al., CAV 2022 (A; TA): FRET's diagnosis found 8 minimal unrealizable cores in Infusion Manager and showed a published human attribution (G1 vs G7) wrong ([source](https://link.springer.com/content/pdf/10.1007/978-3-031-13188-2_24.pdf)) [V4-07] | Contradictions across forms; k-subset localisation | Divergence in unenumerated environment states; translation errors | Changes formalised "in mere minutes", but initial formalisation "requires substantial effort" (~5,000 observables); **48 s – 4h14m** per full run; no result reuse [V5-05, V5-06] | Human-only evidence |
| **LLM translation + SMT vs LLM alone** | SAT-LLM, **ASE 2024 short paper (A; TA)**: 55 requirements, 15 conflicting subsets (4 composite), on the authors' own dataset expanded with 10 composite-conflict requirements. GPT-4 alone: P 0.85, R 0.31. LLM→FOL + Z3 MUS/MSS: **P 1.00, R 0.83**; the advantage is largest on composite conflicts ([source](https://par.nsf.gov/servlets/purl/10574434)) [V5-07] | Composite conflicts LLM reading misses | Translation errors | Low | Measured (one study, own dataset) |
| **Table completeness/disjointness** | DMN tables, **BPM 2016 (A; TA)**, ~500–1,500 rules: missing-rule check 160 ms–18.3 s, overlap check 200 ms–30.7 s; 812 maximal overlapping sets vs 23,115 reported by Signavio's checker (figures from the arXiv version) ([source](https://arxiv.org/pdf/1603.07466)) [V2-16, V5-08]. **Heitmeyer, Jeffords, Labaw, TOSEM 1996 (A; TA)**: on the revised A-7 OFP requirements, after review by two teams, the SCR checker found 19 coverage findings in 36 condition tables (17 real errors) and 57 disjointness findings in 3 mode-transition tables of 700 rows ("a few probably are not"), in 245 s total. Coverage errors need type information "not in the table" ([source](http://dslab.konkuk.ac.kr/class/2010/10RE/Automated%20Consistency%20Checking%20of%20Requirements%20Specification.pdf)) [V3-10]. TableWise (C) ([source](https://shemesh.larc.nasa.gov/fm/oldfm/fm-old-sw-ver-tablewise.html)) | Gaps and overlaps inside one table; errors reviewers missed; some inherited from the prose itself (Heitmeyer) | Disagreement *between* tables; gaps where value domains are undeclared | Negligible; every edit | Human-only evidence |
| **Divergence / boundary conditions** | van Lamsweerde & Letier (A-workshop; no detection data) ([source](https://webperso.info.ucl.ac.be/~avl/files/avl-MontereyLNCS.pdf)). Degiovanni et al. ASE 2018 (A) ([source](https://nmaguirre.github.io/assets/pdf/ase2018.pdf)); critique: "not complete" (A-pre) ([source](https://arxiv.org/pdf/2203.12903)). Not re-checked in this run | Consistent but contradictory in a corner | Completeness | Search cost | Human-only evidence |
| **Realizability / rt-consistency** | FRET compositional realizability, FM 2021 (A; TA): LMCPS FSM 1524.82 s → 3.51 s / 6.74 s; "unknown" on non-linear arithmetic; 12 h timeouts; three specs stayed one component, with mode variables named as **one** contributing reason ([source](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf)) [V5-09]. Spectra cores (A; TA): 227 GR(1) specs (revision histories of 10 student robot projects), 40 unrealizable ([source](https://arxiv.org/pdf/2103.00297)) [V5-10]. **Well-separation** (A; TA): 19 of 79 committed *revisions* of six undergraduate projects were well-separated. Under the strict realizability semantics the students' tool used, 40 of 79 still let the system force assumption violations (derived as 60 − 20). Median check time 15 ms ([source](https://figshare.com/articles/conference_contribution/On_Well-Separation_of_GR_1_Specifications/10223099)) [V5-11] | Clause sets that hold only if the implementation controls the environment | Undecidable in general; data domains; interleavings | Seconds to hours; needs an input/output split | Human-only evidence; no LLM study found |
| **Structural vacuity gates** | Beer et al., FMSD 2001 (A venue; TA), full text: from "several years of experience" at IBM with RuleBase, "typically 20% of formulas are found to be trivially valid" in first runs on a new hardware design. About 10 % of non-vacuous passes reveal a problem when the interesting witness is examined. An experience estimate with no n ([source](https://www.cs.toronto.edu/~chechik/courses05/csc2108/beer01.pdf)); the CAV 1997 wording is confirmed via two citing texts ([Post et al.](https://jochen-hoenicke.de/docs/php11-re.pdf)) [V3-09]. Frama-C/WP smoke tests, TAP 2024 (A; TA): JCVM at Thales, 2,350 smoke tests for ~20 min (≈8 %) on a >4 h proof. **All 37 failures there were spurious** dead-code alarms. The smoke tests also found unsound axioms in WP's own library ([source](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf)) [V5-13]. Dafny proof dependencies (B) ([source](https://dafny.org/blog/2023/10/27/proof-dependencies/)). ProofPulse (A-pre; not re-checked) ([source](https://arxiv.org/pdf/2608.30818)) | Contradictory assumptions, dead antecedents | Consistent-but-weak specs | Low (≈8 %) | Human-only evidence |
| **Semantic-strength gates** | Lahiri (A, above). SpecRL (A-pre; not re-checked): spectests as reward ([source](https://arxiv.org/pdf/2604.05820)). ReForm (A-pre; TA): of 115 failures, 52.2 % weak, 44.3 % unverifiable, 3.5 % trivial ([source](https://arxiv.org/pdf/2507.16331)) [V5-14] | Consistent but too weak | Needs an independent source of negatives | Low | Measured |
| **Constructive witnesses** | W3C Process; RFC 6410 ("at least two independent interoperating implementations"); Wasm phase 4 ("Two or more Web VMs") (B) ([W3C](https://www.w3.org/policies/process/); [RFC 6410](https://www.rfc-editor.org/rfc/rfc6410.txt); [phases](https://raw.githubusercontent.com/WebAssembly/meetings/main/process/phases.md)) [V5-17]. Watt, CPP 2018 (A): mechanisation found errors that meant "the type system was originally unsound" ([source](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf)) [V5-16, V4-12] | Satisfiability on the exercised domain | Non-vacuity; unexercised branches; soundness | One build per witness | Human-only evidence |

**What a "consistent" result does not show.** An SMT "verified" result does not show that the assumptions are satisfiable. `{:axiom}` and bodiless contracts are taken on faith; Dafny "still verifies the well-formedness" only (B) ([source](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/Attributes.md)). Alloy results are scope-bounded (B) ([source](https://alloytools.org/tutorials/online/maintext-FS-2.html)). Lean "cannot check whether new axioms are consistent", so the gate is `#print axioms` (B) ([source](https://lean-lang.org/doc/reference/latest/Axioms/)). After its smoke tests found inconsistencies, the Frama-C team turned "most of our axioms into proper lemmas or Coq realizations" (A).

**Incremental consistency.** Bosch did not implement result reuse, and full runs took up to hours (A). Hanfor tags changed requirements for re-review (A-workshop). FRET's partitions keep checks local unless requirements connect, with mode variables one reason (A). Nuseibeh et al.: "incremental or localized consistency strategies do not guarantee global consistency" (A) ([source](https://typeset.io/pdf/leveraging-inconsistency-in-software-development-4me5sgffk1.pdf)). Adjacent evidence on incremental *verification*, not consistency: in eight expert Dafny IDE sessions, caching cut re-verification by more than 10× in many sessions (session 0: 4,395.3 s → 315.3 s → 277.5 s) ([Leino & Wüstholz, CAV 2015, A; TA](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/krml245.pdf)) [V4-08]. *Inference*: on each new clause, run its per-form check, a k-subset conjunction against clauses sharing a variable, and vacuity for the antecedents it touches. Run the full conjunction, rt/realizability checks and smoke tests nightly or before any downstream step. Keep every unsat core as a regression fixture. Expect handle state, profile and lifecycle phase to act as connecting mode variables for a store API. Declare value domains in the checked artefact, since completeness depends on them (Heitmeyer).

**Witnesses: how many and how different.** No source read measures defect yield per additional implementation; "two" is a convention [V5-57]. Earlier brief §3, verbatim, under "Seeds proposed there but not evidenced": "at least two *witness* implementations with different profile values as a satisfiability argument;". The replacement below has no new full-text evidence for or against it, so it is *Inference* and not a §3 challenge. Replace "≥2 witnesses" with a coverage criterion:
- one witness per profile value;
- for each unspecified or indeterminate set, witnesses that between them choose every allowed outcome;
- witnesses that survive adversarial environment schedules.

**[§3 qualification] Vericoding / DafnyBench.** Earlier brief §3, verbatim: "agents conform well to fixed, machine-checked specs (Vericoding, DafnyBench);". This does not contradict the claim that agents conform to the fixed spec. It contradicts the implicit premise that the fixed specs encode the intended behaviour. Vericoding's own manual check sampled 5 random successes per language and source: "Across Dafny, Verus and Lean, conditioned on vericoding success, roughly 9% of the specs were too weak and another 15% had poor translations". Verus had the most weak specs. Dafny's "no issues" refers to LLM cheating behaviour, with "LLMs correctly giving trivial solutions when the specs were weak" (A-pre; TA) ([source](https://arxiv.org/pdf/2509.22908)) [V1-46, V5-15]. AlgoVeri, **ICML 2026 (A; CB)**, gives one worked case: Vericoding's Dafny and Verus LIS specs require only 0 ≤ result ≤ length, so "a model could satisfy these specs by simply returning 0". It counts no others ([source](https://arxiv.org/abs/2602.09464)) [V2-19]. MutDafny (A-pre; TA) found 5 weak specs, **4 of them in LLM-generated programs**; 3 of those 4 had been found earlier by manual inspection or by Endres et al. ([source](https://arxiv.org/pdf/2511.15403)) [V5-18]. Pass rates therefore overstate conformance to *intended* behaviour wherever the fixed spec is weak.

### 2.3 T3 Two test families on the reference model

#### 2.3.1 Spec-enforcing tests

**Core finding.** Model-generated tests replayed step by step, comparing state after each action, are cheap and strong when the target is small and close in granularity to the model. That is the position of a Python reference model. The decisive variable is granularity distance, not the tool (*Inference*). Model-generated tests inherit the model's blind spots and enforce spec → model only.

| Option | Evidence (grade; n, setting) | Catches | Misses | Cost | Agents |
|---|---|---|---|---|---|
| **TLA+ → test-case generation** | MongoDB Realm Sync, PVLDB 2020 (A; V): 1 kLOC merge function, spec transcribed from code. 4,913 generated tests covered **86/86 branches**, vs 18 for 36 handwritten tests and 79 for ~8 M AFL runs. The model checker, not the tests, found a non-terminating merge rule that "had faithfully been transcribed" ([source](https://arxiv.org/abs/2006.00915)) [V5-19] | Divergence on enumerable state | Bugs shared by spec and code | 1 engineer, 4 weeks [V5-20] | Human-only evidence |
| **State-space-guided testing** | Mocket, EuroSys 2023 (A; TA): **7 implementation bugs** (3 new, 4 known) in Xraft, Raft-java, ZooKeeper, **plus 2 bugs in the official Raft TLA+ spec**; annotations 134–152 LOC ([source](https://gaoyu-cn.github.io/paper/2023-eurosys-mocket.pdf)) [V5-22] | Divergence per action | Unmodelled behaviour | Hundreds of LOC | Human-only evidence |
| **Multi-grained conformance replay** | Remix, EuroSys 2025 (A; TA): 6 severe ZooKeeper bugs mainly via model checking; "The conformance checking is unsound … only check safety" ([source](https://arxiv.org/abs/2409.14301)) [V5-23] | Spec ↔ code drift | Liveness | ≤40 person-hours per mixed-grain spec | Human-only evidence |
| **Quint Connect / Apalache MBT** | Vendor posts and slides (C; V). Emerald: an AI wrote the Quint spec from *code*, ~80 % coverage, one leak, n = 1 ([source](https://quint-lang.org/posts/quint_connect_emerald)). Apalache MBT: no figures ([source](https://conf.tlapl.us/2020/09-Kuprianov_and_Konnov-Model-based_testing_with_TLA_+_and_Apalache-Slides.pdf)). Not re-checked | Divergence | Spec-from-code confirms code (*Inference*) | Low claimed | Agent, C-grade, n = 1 |
| **Dafny test generation** | DTest, Fedchin et al., **NFM 2023 (A; TA)**: verifier-driven inputs that reach *implementation* blocks or branches; postconditions compiled to runtime `expect` oracles. DUTIL (1,382 LOC) 79 %/84 % and ESDK (4,596 LOC) 62 %/58 % statement/branch coverage on C#; 918 tests for 436 methods in 158 min; "half of the generated tests have no return value check due to absence of postconditions" ([source](https://cdn.amazon.science/b9/d4/eeb4fe1a47609f75956dd6fbc0c6/a-toolkit-for-automated-testing-of-dafny.pdf)) [V4-03]. DSpec2Test (A-pre; TA): a spec-driven black-box mode (DNF partitions + boundary values). On 131 killable implementation mutants of 17 DafnyBench programs: 93.9 % vs 82.4 % for DTest's block mode; union 95.4 %; 17 unique kills by the spec mode; no mutable state ([source](https://arxiv.org/pdf/2609.29713v1)) [V4-05] | Runtime errors and postcondition violations on implementation-reaching inputs; clause-partition tests add kills | Anything the contract does not state; no Python target | Minutes to hours | None (no agent study) [V4-04] |
| **P# systematic testing** | FAST 2016 (A; not re-checked): vNext 1, MigratingTable 11, Fabric 1 unconfirmed; environment modelling 2 person-weeks to 5 person-months ([source](https://www.doc.ic.ac.uk/~afd/papers/2016/FAST.pdf)) | Concurrency × failure bugs | Unmodelled faults | Environment modelling | Human-only evidence |
| **Contract → property tests; stateful PBT** | icontract-hypothesis (B, no effectiveness data) ([source](https://raw.githubusercontent.com/mristin/icontract-hypothesis/master/README.rst)); Hypothesis rules, preconditions, invariants, Bundles (B) ([source](https://hypothesis.readthedocs.io/en/latest/stateful.html)). Hughes' AUTOSAR/Dropbox reports [unreachable] [V4-18] | Clause violations on generated inputs | Inherits contract weakness | Mechanical | No agent study |
| **LLM-written PBTs from docs** | Vikram et al. (A-pre; own metric): 40 Python API methods; valid and sound PBT in 2.4 samples; GPT-4 covered **21 %** of documented properties ([source](https://arxiv.org/abs/2307.04346)) [V5-30]. PBT-Bench (A-pre; NeurIPS 2026 acceptance claimed by authors): 100 problems, 40 Python libraries, 365 injected bugs; a bug counts as found if a test fails on the buggy and passes on the fixed version. PBT-prompt recall 42.1–83.4 % across eight LLMs × 3 runs. Under the open-ended "write a test that fails" prompt, one model (Opus 4.8) "stops after exposing one bug" (recall 39.3 %). A prompt including "cover the specification rather than hunt for one bug" adds **+41.5 pp** for it ([source](https://arxiv.org/abs/2605.15229)) [V2-01]. Agentic PBT (A-workshop; **V**: vendor-affiliated, Hypothesis maintainer): 100 packages; 56 % of n = 50 sampled reports valid (sample drawn from the top 80 % by LLM score, κ = 0.31); $9.93 per valid bug, "an upper bound" ([source](https://arxiv.org/abs/2510.09907)) [V5-31] | Many property classes incl. stateful | Spec coverage unless instructed or imposed | Low | Measured |
| **History checking** | Porcupine (README B, blog C; TA): executable sequential model + history; "1,000x–10,000x faster" than Knossos on its own `test_data/jepsen/` ([source](https://raw.githubusercontent.com/anishathalye/porcupine/master/README.md)) [V1-07]. OmniLink (A-pre; **CB**): TLA+ meaning per timeboxed event; agreed with Porcupine on every BAT trace; found 2 previously unknown bugs (1 in BAT, 1 in ConcurrentQueue) ([source](https://arxiv.org/abs/2601.11836)) [V1-06] | Linearizability violations | Only histories generated | NP-complete check | Human-only evidence |
| **Environment actions as generated operations** | Remix fault injection; CCF `IsFault`; TraceLink found timeout and failure-detector model bugs ([source](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf)); FoundationDB "tens of thousands of simulations every night" (B; not re-checked) ([source](https://apple.github.io/foundationdb/testing.html)) | Concurrency + failure bugs; hidden assumptions | Faults outside the alphabet | Environment modelling | Human-only, except Emerald (C) |

**[§3 qualification] Porcupine cost.** Earlier brief §3, verbatim: "**Checking landscape.** What each form proves alone; ioco's treatment of unspecified versus nondeterministic outputs; history checkers (Elle, Porcupine, Knossos) and their cost." OmniLink does not contradict "their cost". It shows that cost depends on history shape, and it comes from competing-tool authors. In their one-system comparison (BAT; 5 threads at 500–450k operations, or 1–50 threads at 100 operations each; 10 traces per length), Porcupine was "significantly faster" on short or many-thread histories. "Past 200k operations with few threads", Porcupine was less consistent and often took "multiple minutes" to reject traces, and from 250k actions it used more memory ([OmniLink §7.4](https://arxiv.org/abs/2601.11836)) [V1-05]. No neutral benchmark was found. Pine (A-pre) builds on Porcupine and matches its speed; it cites Porcupine issue #6 on hangs ([source](https://arxiv.org/pdf/2608.17388)) [V1-08]. *Inference*: for short histories from a Python reference model, this qualification hardly matters.

**Agent applicability.** The measured agent weak spot is *coverage of the spec*. Vikram et al. measured 21 % property coverage. PBT-Bench found one model stopping after one bug under an open prompt, which one whole-spec instruction removed. The remedies are structural ([PBT-Bench](https://arxiv.org/abs/2605.15229); [Konnov slides, C](https://conf.tlapl.us/2026-etaps/konnov-2026.pdf)) [V2-02]. *Inference*: give agents the clause text and ID, never the reference-model source, when they generate spec-enforcing properties, and have the harness impose one test obligation per clause ID. DSpec2Test's 17 unique kills support deriving tests from clauses as well as from implementation coverage, though for implementation faults, not misreadings [V4-05].

#### 2.3.2 Conformance between layers (formal model F ↔ reference model R ↔ spec S)

| Bridge | Evidence (grade) | Strength | Miss | Cost |
|---|---|---|---|---|
| **Differential random testing (DRT)** | Cedar, FSE Companion 2024 (A; V): Lean model 1,673 LOC vs Rust 15,693. DRT + PBT found 21 bugs, proofs 4 more (validator). Each target fuzzed 6 h/day on 4 vCPU. DRT missed a non-termination bug. 35.5 % of `when` conditions from the type-directed ABAC generator were boolean literals; an *added* expression generator produced 9.7 %. One DRT failure (string size) surfaced a spec ambiguity and **led to dropping a feature** ([source](https://arxiv.org/abs/2407.01688)) [V5-27–V5-29] | Output equality on generated inputs | Rare inputs; outside the generators | Cheap once executable |
| **Trace validation (impl → model)** | Cirstea et al., **SEFM 2024 (A; TA, TLC maintainers)**: "In all cases" unmatched executions found; **"too imprecise logs may even lead to erroneous traces being accepted"**; effort evidence "anecdotal" ([source](https://arxiv.org/abs/2404.16075); [DOI](https://doi.org/10.1007/978-3-031-77382-2_8)) [V2-17, V5-24]. CCF, **NSDI 2025 (A; V)**: 6 bugs; first consensus trace spec ~2 engineer-months over four months (including TLC enhancements), later consistency spec ~1 engineer-week; DFS validation <1 s vs ~1 h BFS ([source](https://arxiv.org/abs/2406.17455)) [V2-18, V5-25]. TraceLink, OOPSLA 2025 (A; TA): 9 bugs, all model↔implementation drift or environment assumptions; fixes "did not change the outcome of model checking" ([source](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf)) [V5-26] | "Everything R did, F allows" | F behaviour R never exercised | 1 week to 2 months |
| **Negative result** | MongoDB MBTC (A; V): 2 engineers, 10 weeks, abandoned; "Bugs in post-processing could mask implementation bugs" ([source](https://arxiv.org/abs/2006.00915)) [V5-21] | — | Large, coarse targets | High |
| **PObserve** | P docs (B): log-based monitoring, no measured data ([source](https://p-org.github.io/P/advanced/pobserve/pobserve)) | — | — | — |
| **Refinement checks** | No full-text bridge evidence | — | — | — |

**Cedar's model layer (earlier "[§3 challenge]" withdrawn).** Earlier brief §3, verbatim, under "Method families surveyed": "DbC/JML/ACSL/Dafny/Larch/Spec#;" … "executable reference models (ShardStore, Cedar)." Earlier brief §2, verbatim: "Dafny for per-call contracts;". No sentence links Cedar to Dafny, so the earlier run's challenge "Cedar's models are Lean, not Dafny" contradicted nothing. It was **a misreading of the brief by the earlier run** and is removed [V1-01]. For the record, the FSE paper says "We wrote models of the Cedar evaluator, authorizer, and validator in Lean" ([source](https://arxiv.org/abs/2407.01688)). The cedar-spec release/2.0.x–3.0.x READMEs describe "the Dafny formalization of Cedar" (B; V) ([2.0.x](https://raw.githubusercontent.com/cedar-policy/cedar-spec/release/2.0.x/README.md); [main](https://raw.githubusercontent.com/cedar-policy/cedar-spec/main/README.md)). The date and reason of the switch are undocumented in the sources read [V1-02].

*Inference*: three conclusions follow.
1. Only F ↔ R has measured mechanical bridges. S ↔ F and S ↔ R need clause-ID traceability plus T1 and expectation methods.
2. A complete bridge needs both directions (Konnov's slides, C): replay F → R plus trace validation R → F, or DRT plus coverage.
3. R is deterministic and fully observable, so full-state logging removes Cirstea's false-acceptance risk.

A reviewed, versioned abstraction function `alpha(R_state) → spec_state` is the cheapest structural decision, and the place agents are likely to cut corners ("do not trust the generated harness – TODOs and bugs inside", [Konnov, C](https://conf.tlapl.us/2026-etaps/konnov-2026.pdf)). A failing bridge should route back to the clause (the Cedar lesson), not be fixed in whichever layer is easier (the MongoDB anti-pattern).

**Agents in bridges.** SysMoBench, **ICLR 2026 (A; TA for its mapping component)**: 11 artefacts; three agents on four LLMs; best of five runs; at most three repair iterations ([source](https://arxiv.org/abs/2509.23130); [OpenReview](https://openreview.net/forum?id=SAeaTz8YoM)). Conformance is the share of instrumented code actions trace-validated without error.
- On the Asterinas spinlock, all 8 agent/LLM pairs reached 80–100 %.
- On Etcd Raft, **only one LLM (Claude-Sonnet-4) reached conformance scoring at all**: 7.69 % (basic modelling) and 15.38 % (code translation). The other six pairs failed syntax or runtime checks. *Inference*: these are about 1/13 and 2/13 actions.
- The authors "inspected the LLM-assisted mapping … and found the results to be correct", with no error rate given [V2-04].

Konnov (C, n = 2): an AI-written TFTP harness took ~1 week and ~200 premium requests and found 2 bugs; for ZooKeeper, "sometimes, AI tools cut corners badly". NL → TLA+ over 30 LLMs and 205 specs: up to 8.6 % semantically correct (A-pre, abstract only) ([source](https://arxiv.org/abs/2606.05792)). All of this reinforces the §3 baseline "LLM-written system-level TLA+ is weak and grading-sensitive"; it is no challenge.

#### 2.3.3 Expectation tests (independent of spec and model)

**Core finding.** Evidence that intent-derived oracles beat *code*-derived ones is solid for LLMs. Evidence that prose-derived oracles beat *spec*-derived ones, the brief's actual claim, **was not found**. Human evidence shows requirement-only checks catching a minority of *implementation* faults, with the authors warning against ranking check types. IV&V return-on-investment data does not isolate independent derivation either: the DoLILU case counted 695 IV&V-found errors with no counterfactual, and the 1.5–12 ROI range is model-based ([Neal et al., B](https://ntrs.nasa.gov/api/citations/19980027712/downloads/19980027712.txt); [Hunt, C](https://www.nasa.gov/wp-content/uploads/2016/10/1-4a-ivv_conference_bob_hunt_dulos_kalman.pdf)) [V4-01]. Cleanroom (Selby et al.) is no evidence for independent test families, because both arms had the same independent testing ([source](http://www.cs.umd.edu/~basili/publications/journals/J33.pdf)) [V3-11].

| Option | Evidence (grade; n, setting, "correct") | Catches | Misses | Agents |
|---|---|---|---|---|
| **Specification by example / ATDD / BDD** | Ricca et al. 2007 ECEASST (A-workshop): 13 students; correctness judged by a *separate* acceptance suite ([source](https://profs.scienze.univr.it/ceccato/papers/2007/evol2007.pdf)). Melnik & Maurer, XP 2007 (A-workshop): 1 project, 3 interviewees; writing FIT tests surfaced "missing pieces or inconsistencies in a story"; "going from a general description to a test has some fluidity in interpretation" ([source](https://scispace.com/pdf/multiple-perspectives-on-executable-acceptance-test-driven-2gjlzftall.pdf)) [V4-14]. BDD mapping, 166 papers (A): "acute shortage of metrics" ([source](https://arxiv.org/abs/2305.05567)) | Implementer misunderstanding; story gaps | No count of spec misreadings caught | Human-only evidence |
| **LLM Gherkin / acceptance tests** | Karpurapu et al. (A-pre): "correct" = Gherkin-lint syntax ([source](https://arxiv.org/pdf/2403.14965)). Sami et al. (A-pre): 62/65 found tests "useful"; authors praise tests that "extend beyond the explicit requirements" ([source](https://arxiv.org/pdf/2504.07244)). AToMIC (A-pre): inputs include code ([source](https://arxiv.org/pdf/2510.18861)). Not re-checked | Overlooked scenarios (perceived) | **Added commitments presented as a feature** | Measured (syntax/usefulness only) |
| **Tests as intent clarification** | TiCoder, IEEE TSE 2024 (A; TA): n = 15 programmers; +45.97 % pass@1 with an idealised oracle proxy ([source](https://arxiv.org/pdf/2404.10100)) [V5-36] | Misreading exposed by one concrete test | Proxy idealised | Measured |
| **Independence by information hiding** | Leveson et al. 1990 TSE (A): 24 students; spec-only self-checks found 19 % of detected faults (43 % code reading, 38 % code-based); 4 of 34 effective checks (12 %) came from the spec alone. The authors: "inappropriate (and even misleading) to claim that checks of one type are more effective"; spec-only checks were written before code access (order confound) ([source](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf)) [V5-32] | Different faults than voting | Implementation faults (minority) | Human-only evidence |
| **LLM oracle pull toward observed behaviour** | Zhao et al. ISSTA 2026 (A): 233 Defects4J defects, 13 LLMs. Shown buggy code: 3.84 % misguided tests vs 0.46 % with fixed code; effective 2.98 % vs 8.51 %. An LLM-generated spec docstring lifted effective tests 104.15 → 186.77 ([source](https://arxiv.org/pdf/2607.22883)) [V5-33, V1-51]. Konstantinou et al. (A-pre): 43.02 % → 35.72 % ([source](https://arxiv.org/abs/2410.21136)) [V5-34]. Mathews & Nagappan (A-pre): CodiumAI and CoverUp discarded 470 and 400 bug-revealing tests ([source](https://arxiv.org/abs/2412.14137)) [V5-35] | Mechanism of confirmation | — | Measured |
| **Oracle anchoring** | Canedo (A-pre, single author, one system; not re-checked): a state-anchored oracle "cannot fail"; re-anchoring recovered 8 of 46 surviving mutants ([source](https://arxiv.org/pdf/2608.17214)) | Lint target | n = 1 system | Human-only evidence |

*Inference*: define independence by **information flow**. The expectation-test writer reads records only and never sees the spec, models or reference model. No expected value may be computed by calling R or a spec-derived helper. Canedo's anchoring predicate becomes a dataflow/import lint. Information flow is **necessary but not sufficient**. Knight's data locate correlated failures in inputs that are hard for everyone: "various different and apparently unrelated faults were triggered by the same special situation in the input" ([Knight, NASA report, B](https://ntrs.nasa.gov/api/citations/19870002808/downloads/19870002808.pdf)) [V3-08]. Hard record scenarios (boundaries, special cases) therefore need a deliberately different derivation, for example explicit enumeration of special cases from the records, not just a second writer. Do not drop expectation tests because they fail on R: a failure is a finding to adjudicate (record, spec, model or test). Require every expectation test to cite its decision and scenario, and flag any assertion not traceable to that decision as an added commitment (the Sami et al. effect).

#### 2.3.4 Oracles for non-commitment

Mature conformance suites encode typed non-commitment in the oracle language (all B, official docs; confirmed [V5-37–V5-40]):
- WebAssembly `assert_return` with `either` and NaN patterns ([README](https://raw.githubusercontent.com/WebAssembly/spec/main/interpreter/README.md)); relaxed SIMD "globally chooses a fixed projection" ([Overview](https://raw.githubusercontent.com/WebAssembly/relaxed-simd/main/proposals/relaxed-simd/Overview.md)).
- sqllogictest `rowsort`/`valuesort` and `skipif`/`onlyif` ([about.wiki](https://raw.githubusercontent.com/gregrahn/sqllogictest/master/about.wiki)).
- JSON Schema `optional/`, which "currently conflates many reasons" ([README](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/README.md)).
- POSIX (IEEE 1003.3) UNSUPPORTED and UNRESOLVED ([LTP](https://raw.githubusercontent.com/linux-test-project/ltp/master/testcases/open_posix_testsuite/Documentation/HOWTO_ResultCodes)).

NonDex explores allowed behaviours of underdetermined Java library specs. Its authors report 60 open-source and 110 student bugs from their ICST 2016 paper (A-workshop; TA; human-only) ([source](https://mir.cs.illinois.edu/gyori/pubs/jpf16.pdf)) [V5-41]. PatchDiff (ICSE 2026, A; TA judging third-party agents): 29.6 % of "plausible" SWE-bench Verified patches diverge from ground truth; 27.3 % of divergences "adapt more behavior"; resolution rates inflated by 6.4 points ([source](https://arxiv.org/abs/2503.15223)) [V5-42].

| Non-commitment type | Oracle mechanism with precedent (*Inference* mapping) |
|---|---|
| Unspecified (one of a set) | `either` set when small; predicate when large; canonicalisation for ordering; a cross-call consistency test if stability is promised |
| Optional | Opt-in suite, verdict UNSUPPORTED; must still fail if claimed and wrong |
| Deliberately not promised | Assert nothing on the dimension, plus a NonDex-style perturbing R: any test that then fails is over-strict |
| Profile-declared | One suite parameterised by profile value with per-profile expected sets (§3 rule) |
| Indeterminate | Accept "took effect" and "did not"; an UNRESOLVED-like verdict must not count as a pass |

*Inference*: bound each family from both sides on R. The **allowed-variant check** requires every test to pass on R variants that make different allowed choices. The **forbidden-variant check** requires that, for each per-decision mutant making a disallowed choice, some test in the right family fails. Expectation tests are the most prone to over-strictness. Predicates and canonical forms are the default the precedents suggest; ShardStore-style relaxation flags are kept for unknowable state. No study compares outcome sets with relaxation flags.

### 2.4 T4 Adequacy and traceability

**Trace links as checkable data** (B; official docs or source [V5-54]):
- **OpenFastTrace** reports missing coverage, `ORPHANED`, `OUTDATED`, `AMBIGUOUS` and duplicate IDs, and has a quiet, return-code-only mode ([report](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/console_tracing_report.md); [LinkStatus](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/api/src/main/java/org/itsallcode/openfasttrace/api/core/LinkStatus.java)).
- **sphinx-needs** fails on dead links and schema link counts under `-W` ([config](https://sphinx-needs.readthedocs.io/en/latest/configuration.html)).
- **Doorstop** flags suspect links when the parent fingerprint changes ([validation](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/docs/cli/validation.md)). Its exit code on failure is not in that document and was not re-checked against the CLI source.

Measured benefit (Mäder & Egyed, EMSE 2015, A): the EMSE full text is **[unreachable]**, so the figures are **unverifiable** at full-text level. They match the authors' 2-page SE 2016 summary: 71 practitioners and students, 8 maintenance tasks on Gantt Project and iTrust, randomly assigned with or without traceability. The 461 task solutions were **recorded on paper, not implemented**, and were scored against the original developers' solutions. With traceability, subjects were 24 % faster and produced 50 % more correct solutions ([summary](https://dl.gi.de/bitstreams/b9fc3267-9d74-4127-ab3a-2a512de7ed2c/download)). Human-only [V2-12]. LLM trace recovery: LiSSA, ICSE 2025 (A; TA), best F1 0.25–0.53 on five requirement → code benchmarks. It does not beat the best IR baseline everywhere (eTour .548), and the authors say more research is needed "to be applicable in practice" ([source](https://publikationen.bibliothek.kit.edu/1000179816/164563088)) [V5-43]. *Inference*: write links when each artefact is created (revision in the ID), gate deterministically, and use LLM recovery only to audit. A link gate shows that links exist, not that they bind.

**Mutation of spec, models and reference model.**

| Option | Evidence (grade; n, setting) | Catches | Misses / triage | Cost | Agents |
|---|---|---|---|---|---|
| **Dafny spec mutation + sanity checks + spec-testing proofs** | IronSpec, OSDI 2024 (A; TA): 14 specs; 10 spec bugs across 6 real systems; 13 of 61 surviving mutants intended weaknesses; mutation runs "only if the system has a passing proof" ([source](https://par.nsf.gov//servlets/purl/10550356)) [V5-44] | Specs weaker than intended | Intended weakness as false positives | 3 s to 191 min; STP suites hours to days | Human-only evidence |
| **Implementation mutation exposing weak specs** | MutDafny (A-pre; TA): 794 programs; current v2 has 118,458 mutants, 30,459 survivors, mean score 82 % (v1: 112,810; 79 %). 284 survivors reviewed: 77 weak-spec hints, 157 equivalent, 50 inconclusive. 5 weak specs, 4 in LLM-generated programs, 1 of those new ([source](https://arxiv.org/pdf/2511.15403)) [V5-45, V5-18] | Weak postconditions | Equivalent-mutant triage dominates | ~18 min/file | Indirect (LLM-written specs) |
| **Alloy model mutation** | Jovanovic, Patwary, Sullivan, FormaliSE 2025 (A; partial TA, μAlloy co-author): 25,180 real faulty Alloy4Fun models; mutants reproduce 10.96 % (17.72 %), but mutant-killing suites **detect 91.78 %** (95.79 %) ([source](https://allisonius.github.io/files/FormaliSE2025.pdf)) [V5-46] | Real model faults | Novices only | Low | Human-only evidence |
| **TLA+ invariant mutation** | TLA+-Bench (A-pre; TA): 300 outputs (3 models × 100 specs), 30 pass TLC. The probe replaces each checked safety invariant with TRUE and re-runs TLC; 12 temporal-only passes are scored non-surviving, 18 are testable, 5 "survive" (5/300 = 1.7 %, "a conservative lower bound rather than a direct vacuity measurement"). Survival is defined as "the mutated run still fails". *Inference*: an invariant replaced by TRUE cannot itself fail, so as worded the probe does not show that the invariant constrains behaviour. Treat the counts as the paper's, not as a vacuity rate ([source](https://arxiv.org/pdf/2607.23425)) [V2-06]. TLA-Prover's Diamond tier (A-pre) requires a mutated invariant to *yield* a counterexample, the usual direction ([source](https://arxiv.org/pdf/2606.06133)) | Vacuous model-checking passes (when built as in TLA-Prover) | No TLA+ mutation tool with kill rates | Low | Measured (LLM outputs) |
| **Reference-implementation mutants measure contract completeness** | NL2Contract (A-pre; not re-checked): a verification-sound LLM contract discriminates "over three-quarters" of buggy mutants ([source](https://arxiv.org/pdf/2510.12702)). SpecRL spectests (A-pre) | Weak contracts | — | Low | Measured |
| **Python mutation; mutation at scale** | mutmut (B) ([source](https://raw.githubusercontent.com/boxed/mutmut/main/README.rst)). Google (A; V): ~15 M mutants over 6 years, coupled to real faults; developers wrote more tests ([source](https://arxiv.org/abs/2103.07189)) [V5-47] | Unasserted effects | Equivalent mutants | Incremental | Human-only evidence |
| **LLM-generated mutants** | Wang et al. TOSEM 2025 (A): 851 real Java bugs; 76.47 % vs 44.15 % rule-based ([source](https://arxiv.org/pdf/2406.09843)) [V5-48]. Meta ACH (A; V + TA): 9,095 mutants, 571 tests; engineers accepted **73 % of the tests they reviewed** in test-a-thons; equivalent-mutant detector P 0.79 / R 0.47 ([source](https://arxiv.org/pdf/2501.12862)) [V5-49] | Realistic mutants | Compilability | — | Measured |

No study tests the §3 seed directly (one mutant reference model per clause, killed by the suite). *Inference*: require a **per-family kill**. A clause-linked R mutant killed by only one family is a finding. Killed only by spec tests means a hole in the expectation family. Killed only by expectation tests means a likely faithfulness gap in the clause. **Compare families at equal test counts** (or report kills per test), because suite size alone drives much of the apparent association (Papadakis, below) [V3-04]. Survivors that map to a registered non-promise are auto-classified "intended".

**Does mutation score track real faults?** For code:
- 73 % of 357 real faults were coupled to mutants and 17 % to none ([Just et al., A; partial TA](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf)) [V5-50].
- Strong mutation had the highest fault revelation of four criteria once the clean-program assumption is avoided ([Chekam et al., A](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf)) [V5-51].
- **Papadakis et al., ICSE 2018 (A), now verified** on 68 CoREBench and 231 Defects4J real faults, with 10,000 sampled suites per size group. Correlation is "moderate to strong" (mostly 0.35–0.75) when size varies and "relatively weak (approximately within the range 0.05 to 0.20) when the suite size is controlled". Suites ranked in the top 10 %/25 % by mutation score still beat random suites of equal size: by 11 %/8 % on Defects4J and 46 %/18 % on CoREBench on average, but with significance for only 138/231 and 59/68 faults. "Approximately 1% of all mutants" resemble the real faults ([source](https://typeset.io/pdf/are-mutation-scores-correlated-with-real-fault-detection-a-t9e7f0t5d6.pdf)) [V3-01–V3-03].

For models, Alloy4Fun is the only large real-fault result. *Inference*: use mutation as a hole finder, not a numeric target. Prefer clause- or record-linked mutants over generic operators, given the 1 % relevance figure. The independent expectation family is the hedge against the uncoupled share.

**Coverage that fits (necessary conditions only).**
- TLC coverage reports actions that "never run" (B, wiki draft) ([source](https://docs.tlapl.us/_export/raw/using:coverage)).
- QuickCheck `checkCoverage` fails on statistical grounds (B) ([source](https://hackage.haskell.org/package/QuickCheck-2.14.3/docs/Test-QuickCheck.html)).
- Hypothesis `event`/`target` only report, so a wrapper is needed to gate on them (B) ([source](https://hypothesis.readthedocs.io/en/latest/reference/api.html)).
- Hughes (A; TA): validity properties missed 5/8 planted bugs; model-based properties found the union bug in 8.4 tests vs 50; a label showed the key absent in 79.2 % of tests ([source](https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf)) [V5-52].
- Goldstein et al. (A; 30 interviews at one firm): practitioners validated PBTs by mutation 7/30, example inspection 8/30, code coverage 2/30 ([source](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf)) [V5-53].
- **Requirements-level coverage loses to random at equal size**: on four avionics systems (600 mutants each), auto-generated suites satisfying requirements or antecedent coverage found fewer faults than random suites of the same size, with statistical significance. UFC suites beat random in 3 of 4 systems (DWM 2: −42 %) ([Staats et al., A-pre; TA](https://conservancy.umn.edu/server/api/core/bitstreams/a533c3cb-0812-4e95-b113-7d221af01318/content)) [V4-09].

*Inference*: the coverage gates are clause, scenario, case-table row, non-commitment branch, model action and state × operation cell, plus generator health. A one-test-per-clause gate is a **presence check**, not an adequacy signal. Adequacy needs a per-condition criterion (UFC- or MC/DC-like) plus the per-family kill.

**Gate composition.** No published ordered pipeline matches the brief. The published partial orderings are:
- TLA-Prover tiers;
- IronSpec (sanity → STPs → mutation after a passing proof);
- Hughes (validity property first);
- OFT `direct_failures`;
- Doorstop suspect links.

The AWS CACM 2025 article remains **[unreachable]** (403 on queue, cacm and dl.acm). Desai's FMCAD 2025 talk abstract (B; V) lists AWS's practices, with "formal specifications as oracles or monitors", but gives no figures and no ordering ([source](https://repositum.tuwien.at/handle/20.500.12708/219530)) [V4-06]. *Inference*, proposed sequence; each gate blocks the next stage for the affected clause:

| # | Gate | Fails on | Typical cost |
|---|---|---|---|
| G0 | ID/schema lint | missing or duplicate IDs, malformed form, untyped non-commitment, undeclared value domain | seconds |
| G1 | Upward trace | clause without `decision~rev`, decision without clause, `OUTDATED` (presence only, not binding) | seconds |
| G2 | Faithfulness exhibition | rejected scenario witness, failed rejected-option refutation, "not addressed" on an added-commitment probe | minutes per clause |
| G3 | Form-local checks | table not complete or disjoint; missing transition cell | seconds |
| G4 | Cross-clause consistency and satisfiability | unsat core, contract inconsistency, rt/realizability failure, well-separation failure | seconds to hours |
| G5 | Vacuity and non-triviality | a mutated invariant or model fails to yield a counterexample; smoke tests; sanity flags | seconds to minutes |
| G6 | F ↔ R conformance | DRT or replay mismatch; trace-validation rejection | minutes per run once built; building the bridge costs days to weeks (CCF, MongoDB) |
| G7 | Downward trace and coverage | clause without spec test, scenario without expectation test, never-fired action, uncovered row or branch, generator health (necessary only) | seconds to minutes |
| G8 | Per-family mutant kill + allowed-variant check | R mutant not killed by both families (compared at equal test counts); any test failing on an allowed variant | minutes to hours |
| G9 | Spec-strength mutation | a stronger clause variant still passes all proofs and tests | minutes to hours |

G5 must precede trusting any model-checking pass. G8 and G9 must follow G6, because mutating a non-conforming R measures the wrong thing, as with IronSpec's "only if the proof passes" (*Inference*).

**Agent applicability (T4).** Measured:
- trace recovery (moderate);
- mutant generation (better coupling than rule-based tools);
- mutant-killing test generation (73 % of reviewed tests accepted);
- LLM-written Dafny specs, some weak (MutDafny; Vericoding).

For LLM TLA+, most TLC passes fail TLA+-Bench's mutation probe, whose mechanics are unclear; its "substantive" screen keeps 12 of 30 passes [V2-07]. Not measured: agents authoring links, designing coverage requirements, triaging spec-mutant survivors, or running a per-family kill gate. Gates must be non-editable by the producing agent (§3 baseline).

### 2.5 T5 Independence (minimal)

| Finding | Evidence (grade; n, setting) | Agents |
|---|---|---|
| LLM errors are correlated, more so within one provider and among more accurate models; judges inflate same-provider answers | Kim et al. ICML 2025 (A): **multiple-choice** answers of 349 LLMs on 12,032 questions and 71 LLMs on 14,042 (HELM), plus a résumé-screening case. When both models are wrong they pick the same wrong answer 0.423 (chance 0.127) and 0.60 (chance 1/3) of the time ([source](https://arxiv.org/pdf/2506.07962)) [V1-12, V1-13] | Measured (MCQ) |
| Intrinsic self-correction does not reliably help | Huang et al. ICLR 2024 (A): CommonSenseQA 75.8 → 41.8 after 2 rounds for one model ([source](https://arxiv.org/pdf/2310.01798)) [V1-32]; Kamoi et al. TACL 2024 (A): works with reliable external feedback ([source](https://arxiv.org/pdf/2406.01297)) [V1-33] | Measured |
| Self-preference and judge noise | Panickssery et al. NeurIPS 2024 (A) ([source](https://arxiv.org/pdf/2404.13076)) [V1-34]; CodeJudgeBench (A-pre; ACL 2026 per Semantic Scholar, unconfirmed): order swap changes accuracy by up to 14 % ([source](https://arxiv.org/pdf/2507.10535)) [V1-35]; Jin & Chen, **ASE journal 2026 (A)**: over 700 tasks, LLMs over-reject correct code, worse with explanations ([source](https://arxiv.org/pdf/2603.00539)) [V1-36] | Measured |
| LLM help can hurt prose review | Broccia et al. (A-pre): 34 students as novice inspectors, crossover; LLM support *lowered* smell-detection accuracy ([source](https://arxiv.org/pdf/2608.21298)) [V1-37] | Measured |
| Debate adds little beyond voting | Smit et al. ICML 2024 (A) ([source](https://arxiv.org/pdf/2311.17371)); Choi et al., **NeurIPS 2025 (A)**: majority voting accounts for most gains ([source](https://arxiv.org/pdf/2508.17536)) [V1-38] | Measured |
| Refuters trained on planted bugs work | McAleese et al. (A-pre; **V**, OpenAI on its own critic): caught more inserted bugs than paid reviewers; human + critic teams hallucinated less ([source](https://arxiv.org/pdf/2407.00215)) [V1-39] | Measured (code) |
| Judge aging | Beyond Compilation (A-pre; TA): one judge rejected outputs of two newer systems; a two-stage **LLM** review classified only 4 of 54 rejections as translation errors ([source](https://arxiv.org/pdf/2606.31002)) [V1-31]. MathAtlas (A-pre; TA): faithfulness judges lose accuracy out of domain, n = 200 ([source](https://arxiv.org/pdf/2605.14061)) [V1-40] | Measured |
| An independent, *differently structured* second description finds spec bugs | Arm, Reid OOPSLA 2017 (A; V): properties developed from the NL manual, recently found bugs and discussion with architects found **12 bugs (2 security)** in an extensively tested spec. Low-level rules repeating the spec were judged "not very useful" and "prone to common-mode failure" ([source](https://alastairreid.github.io/papers/oopsla2017-whoguardstheguards.pdf)) [V1-41]. JEST, ICSE 2021 (A; TA): 27 spec bugs, 44 engine bugs in four engines ([source](https://arxiv.org/pdf/2102.07498)) [V1-42] | Human-only evidence |
| Independently written versions fail dependently, yet diversity still helps | Knight & Leveson 1986 TSE **[unreachable]**. Knight's NASA progress report (B), read in full: 27 student versions of one spec, 10^6 random tests each, 45 faults, many correlated fault pairs, where "various different and apparently unrelated faults were triggered by the same special situation in the input". Three-version systems still cut failure probability by about one order of magnitude ([source](https://ntrs.nasa.gov/api/citations/19870002808/downloads/19870002808.pdf)) [V3-05]. Eckhardt & Lee TSE 1985 [unreachable]; NASA TM 86369 (B): failures are independent only if the "intensity of coincident errors" is constant over inputs, "unlikely to hold in most applications"; high intensity can make N-version worse than one version ([source](https://ntrs.nasa.gov/api/citations/19850015006/downloads/19850015006.pdf)) [V3-06]. Littlewood & Miller 1989 [unreachable]; abstract: diverse methodologies decrease simultaneous failure ([source](https://ntrs.nasa.gov/citations/19900036555)) [V3-07] | Human-only evidence (program versions) |

*Inference*: no gate should let a lineage judge its own spec. A single cross-family judge is weakly supported. Best supported: cross-family judges must agree to accept, rejections go to a human, and the gate is calibrated on a human-labelled sample and recalibrated when the generating models change. Because more accurate models have more correlated errors (MCQ evidence), upgrading every agent can *reduce* independence between the spec writer and the expectation-test writer. Swapping provider reduces correlation but does not remove it. Separate writers do not give independent failures either (Knight; Eckhardt & Lee). Independence must therefore come from a **different derivation**, as in Reid's "describe it differently" and Littlewood & Miller's diverse methodologies (abstract-level). Information-flow isolation is the necessary floor.

### 2.6 Disconfirming searches (brief §5)

**(a) Do formal or structured intermediates fail to improve faithfulness over careful prose review?** *Result: no direct disconfirmation found; indirect cautions found.* No full-text study holds intent fixed and shows a formal or structured intermediate doing no better than careful prose review. The cautions:
- Humans misread and miswrite LTL; English → LTL is worst at 28–47 % wrong across survey rounds 2–4 ([Greenman, A](https://arxiv.org/abs/2211.01677)) [V1-24].
- 215 students: PSP > EPL > raw LTL for correctness, with no prose arm ([Czepa, A](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6944266/fullTextXML)) [V1-47].
- Compilation overstates faithfulness by up to 29.5 points ([Beyond Compilation, A-pre](https://arxiv.org/pdf/2606.31002)).
- LLM-assisted inspection got worse ([Broccia, A-pre](https://arxiv.org/pdf/2608.21298)).
- Templates need substantial training (Großer et al., abstract only), and FRETish was "not always straightforward" (A).
- Mavridou et al. (A-pre; TA) claim structured intermediates "significantly improved" LLM accuracy without data, citing a code-translation paper. The same paper reports an independent oracle catching an `optional` vs `weak` error "easily missed during manual inspection" ([source](https://arxiv.org/pdf/2512.15788)) [V1-48].
- Leveson et al. 1990: requirement-only checks found 19 % of detected implementation faults, with the authors' caveat against ranking (A) [V5-32].

Snook & Harrison and Finney remain abstract-only. Finney's abstract says trained students "performed very poorly", with no n ([source](https://gala.gre.ac.uk/id/eprint/25)) [V4-19]. Net: the §3 point "notation alone does not beat prose" is **reinforced, not challenged**. Measured benefit comes from decomposition plus deterministic translation (Req2LTL), example tables (Fit), and formal artefacts *paired with a check against intent*.

**(b) Do model- or mutation-based adequacy measures fail to predict real defects?** *Result: partial disconfirmation, strong for coverage targets, weak for mutation.*
- **Gay et al., TSE 41(8) 2015 (A; partial TA, own OMC/DC), full text**: 7 industrial systems, 4 coverage criteria, effectiveness on seeded mutants (real faults for 2 systems). On the four Rockwell Collins systems with an output-only oracle, suites generated for 3 of the 4 criteria found significantly fewer faults than equal-size random suites. The introduction says "up to 40.6%"; Tables 4–5 show up to −59.2 % (DWM 1, decision) and −48.2 % (DWM 1, MC/DC). On the NASA and two infusion-pump systems, and for OMC/DC throughout, generated suites matched or beat random ([source](https://www.greggay.com/pdf/15covrisks.pdf)) [V2-10].
- Requirements and antecedent coverage suites lost to equal-size random on four avionics systems; UFC beat random in 3 of 4 ([Staats et al., A-pre](https://conservancy.umn.edu/server/api/core/bitstreams/a533c3cb-0812-4e95-b113-7d221af01318/content)) [V4-09].
- Coverage correlates low-to-moderately with effectiveness once size is controlled, with effectiveness measured by mutants ([Inozemtseva & Holmes, A](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf)) [V1-49].
- Mutation-score correlation drops to ~0.05–0.20 with size controlled, yet top-scoring equal-size suites find more real faults for 138/231 and 59/68 faults ([Papadakis, A](https://typeset.io/pdf/are-mutation-scores-correlated-with-real-fault-detection-a-t9e7f0t5d6.pdf)) [V3-02].
- 17 % of real faults are coupled to no mutant (Just, A).
- For declarative models, operators reproduce 11 % of real faults, yet mutant-killing suites detect 92 % (A). This disconfirms operator realism and supports adequacy.

The earlier edition listed the TLA+-Bench "5 of 18" as evidence that a plain model-checking pass is a poor signal. That item is withdrawn as evidence, because the probe's mechanics are unclear [V2-06]. **No** study shows that model-mutation adequacy fails to predict real spec or model defects, and none beyond Alloy4Fun shows that it succeeds. *Inference*: use coverage as necessary-condition gates, never as targets, and mutation as a gap finder compared at equal size, hedged by the independent family.

**(c) Is there a published pipeline doing prose → spec → model → reference model with faithfulness gates?** *Result: none found by the earlier run's search* (a search result, not proof of absence) [V1-09]. The nearest pipelines reverse or collapse the chain:
- **WebAssembly SpecTec** (PLDI 2024, A; TA) generates prose and an interpreter from one DSL. It passes all applicable official Wasm tests and found 10 errors in 5 proposals; faithfulness to intent is checked only via the human-written test suite ([source](https://people.mpi-sws.org/~rossberg/papers/Youn,%20Shin,%20Lee,%20Ryu,%20Breitner,%20Gardner,%20Lindley,%20Pretnar,%20Xiaojia,%20Watt,%20Rossberg%20-%20Bringing%20the%20WebAssembly%20Standard%20up%20to%20Speed%20with%20SpecTec.pdf)) [V1-43].
- **ECMAScript JISET/JEST** blames spec or engine by N-version voting (A; TA) [V1-42].
- **Arm ASL** combines an executable spec, over 11,000 AArch64 validation tests and the 2017 property set; errors were fixed "to match the architects' intent" (A; V) ([source](https://alastairreid.github.io/papers/fmcad2016-trustworthy.pdf)) [V1-44].
- **Cedar** goes design → Lean model → Rust with DRT, with no gate against prose (**A**, FSE Companion 2024 and OOPSLA 2024; V) [V1-03].
- **FRET** leaves prose → FRETish to the human.
- **Req2LTL**, **Roundtrip**, **NeuroSTAR** and **Cunha & Macedo** each cover one NL → formal step.
- **GitHub Spec Kit** runs agents with same-lineage self-review checklists and no data (D/B; V) ([source](https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md)) [V1-50].

Agents are measured in none of the closely fitting pipelines. §4 synthesises, using the Arm/SpecTec/JEST pattern as the comparison point: one executable source, mechanically derived layers, and an independently authored, differently structured check set. Wasm (10), ES11 (27) and Arm (12) found spec bugs where an independent artefact disagreed with the spec. **Cedar's 25 bugs are a different kind**: 4 found by proofs in the validator and 21 by DRT/PBT in production code, all implementation-vs-model ([source](https://arxiv.org/abs/2407.01688)) [V1-04]. That they cluster where an independent artefact disagrees is *Inference*.

### 2.7 Baseline (§3) points touched by full-text evidence

| §3 point (verbatim) | Status in this edition | What exactly is contradicted | Evidence |
|---|---|---|---|
| "executable reference models (ShardStore, Cedar)." | **Confirmed.** The earlier "challenge" is **refuted as a misreading of the earlier brief** | Nothing: §3 names no modelling language for Cedar. Dafny appears in §3 only in "DbC/JML/ACSL/Dafny/Larch/Spec#;" and the benchmark "DafnyBench", and in §2 as "Dafny for per-call contracts;" | [FSE 2024](https://arxiv.org/abs/2407.01688); [cedar-spec 2.0.x README](https://raw.githubusercontent.com/cedar-policy/cedar-spec/release/2.0.x/README.md) [V1-01, V1-02] |
| "agents conform well to fixed, machine-checked specs (Vericoding, DafnyBench);" | **Qualification** (corrected sourcing) | Not conformance to the fixed spec, but the premise that the fixed specs encode intent: ~9 % too weak + 15 % poor translations pooled across Dafny, Verus, Lean; AlgoVeri one case (CB) | [Vericoding](https://arxiv.org/pdf/2509.22908); [AlgoVeri](https://arxiv.org/abs/2602.09464) [V1-46, V5-15, V2-19] |
| "triangular cross-checks help (Clover);" | **Qualification** (valid) | Not "help"; it bounds it: legs sharing a reading cannot detect a shared miss | [Clover A.4.1](https://arxiv.org/abs/2310.17807); [Roundtrip](https://arxiv.org/abs/2604.25031) [V1-45] |
| "history checkers (Elle, Porcupine, Knossos) and their cost." | **Qualification** (was challenge) | Not "their cost"; cost depends on history shape; one comparison by competing-tool authors; no neutral benchmark | [OmniLink](https://arxiv.org/abs/2601.11836) [V1-05, V1-08] |
| Items not re-checked: "Cirstea et al. (TLA+ trace validation), TraceLink, PObserve, Porcupine, arXiv 2409.14301 (multi-grained specs)" | **Re-checked**; PObserve has no data; Cirstea now A (SEFM 2024) | — | §2.3 [V2-17, V5-23, V5-24, V5-26] |
| "notation alone does not beat prose;" / "LLM-written system-level TLA+ is weak and grading-sensitive." / SpecGen / nl2postcond | **Reinforced** | — | §2.6(a); SysMoBench; Zhao et al. [V2-04, V5-33] |
| "SCR tables and EARS" ("Their industrial figures are verified."); "finite case split → table checked complete and disjoint" | **Reinforced** by Heitmeyer (new full text) | — | [Heitmeyer](http://dslab.konkuk.ac.kr/class/2010/10RE/Automated%20Consistency%20Checking%20of%20Requirements%20Specification.pdf) [V3-10] |
| Seeds: mutant reference model; "at least two *witness* implementations …" | **Still unevidenced directly**; replacement criterion is *Inference* | — | §2.2, §2.4 [V5-57] |

---

## §3 Check map per normative form

All cells are *Inference* that maps the cited mechanisms onto the brief's forms. "Earliest" is the first gate (§2.4) at which a defect in that form can fail. "Exp." = expectation family; "Spec." = spec-enforcing family. Transfer and confidence per row are in Part 3.

| Normative form | Faithfulness check | Consistency check | Satisfiability / non-vacuity check | Enforcement (Spec. / Exp. / mutants) | Earliest failure |
|---|---|---|---|---|---|
| **Formula over one instant** | Scenario derivability; rejected-option refutation; added-commitment probe via failing Dafny assertion or Hypothesis-shrunk case shown with the source sentence (Cunha & Macedo; Lahiri) | Conjunction over the shared abstract state (SMT, unsat core); Dafny assumption warnings | Interesting witness; verified R body; "negate the postcondition, must fail"; output-mutation spectests (SpecRL) | Spec.: contract → Hypothesis property and `@invariant`; clause-partition tests (DSpec2Test analogue). Exp.: literal I/O from the scenario. Mutant: R returns a rejected-option output. Miss: rare inputs (Cedar) | **Before the spec** (record pos/neg checks drafted); G2 once the clause exists |
| **Case table (complete, disjoint)** | Dual independent slot-filling, then a row diff (Easterbrook); one scenario per row | Per-table complete/disjoint check (ms–s: DMN; 245 s for a full avionics spec: Heitmeyer) with declared value domains; cross-table conjunction, maximal overlaps | Each row's guard reachable (smoke/vacuity) | Spec.: parametrised row enumeration; row coverage. Exp.: scenario per row. Mutant per row | **G3**, every edit (slot-filling diff at G2). Some gaps come from the records themselves (Heitmeyer) |
| **Frame (unchanged set)** | Show the one state variable the clause lets change or forbids changing | Divergence check vs effect, failure and cancellation tables under a boundary condition; plain SAT misses this | Witness with the frame observable | Spec.: full-state snapshot via `alpha`. Exp.: record scenario asserting untouched state. Mutant: R alters one frame variable. Miss: state outside `alpha` | **G4** (needs environment states enumerated) |
| **Termination under timeout assumption** | Two traces (timeout fires / does not) judged against the record; the timeout stated as an *environment* assumption | Well-separation: the store must not control the assumption (19 of 79 revisions of six student projects were well-separated; 40 of 79 failed under strict semantics) | Bounded liveness in TLC/Apalache; rt-consistency | Spec.: timeouts as explicit actions in F → R replay. Bridge: trace validation exposes "always/never fires" (TraceLink). DRT misses non-termination (Cedar) | **G4/G5** in the model; TraceLink-class at **G6** |
| **State × operation transition table** | Shortest trace per cell from a record scenario; rejected-option cell refused | Every cell defined; consistent with typestate and failure tables | TLC: no never-enabled action, no deadlock; Alloy `run` non-empty | Spec.: Hypothesis `RuleBasedStateMachine` or model-generated per-step replay (Mocket/MBTCG). Exp.: scenario call sequences. Cell coverage gate | **G3** (missing cell) |
| **Environment actions** | Witness trace per environment scenario; classify each non-commitment as system choice vs environment input | rt-consistency / realizability (∀ environment move ∃ allowed response), environment actions as free transitions; well-separation | Witnesses surviving adversarial schedules | Spec.: faults and cancellation as generated actions (Remix, CCF, P#). Exp.: record fault scenarios | **G4** (plain SAT passes; needs the quantified check) |
| **History predicate over interval operations** | Minimal allowed and forbidden history vs the record scenario | Consistency with per-call contracts (linearizability w.r.t. sequential R) | Witness histories; TLA+ model checked non-vacuous | Spec.: R run concurrently, Porcupine-style check against R's sequential mode (fast on short histories; slower past ~200k ops with few threads per one CB comparison); OmniLink/TLA+ for weaker predicates; Elle for isolation. Exp.: concrete histories from scenarios | **G4** if modelled in TLA+, else **G6** |
| **Failure category / phase / effect / retry tables** | Per-row scenario and rejected-option refutation; added-commitment probe per effect cell | Per-table complete/disjoint; cross-table with frame and state tables; retry × concurrency as divergence | Every category reachable; fault-injection points exist in R | Spec.: case-table bridge plus fault actions; retries × concurrency via the history bridge. Exp.: record failure scenarios | **G3** |
| **Register of non-promises** | Two witnesses with different outcomes per entry | No clause commits on the non-promised dimension (register ∧ clauses admit ≥2 outcomes) | Allowed-variant R (NonDex-style) still passes all spec checks | Tests must not assert on the dimension; **allowed-variant check**; survivors mapping to the register auto-classified "intended" | **G2**; over-strict tests at **G8** |
| **Variation points / profiles** | Per-profile scenario; deviations checked narrow-only (§3 Liskov–Wing) | Typed profile schema; each value conjoined separately | One witness per profile value | One parametrised suite with per-profile expected sets; UNSUPPORTED for optional features; fixed-projection consistency test where stability is promised | **G0** (schema lint) |

The non-commitment *types* cut across forms (§2.3.4). Each allowed outcome of each unspecified, profile-declared or indeterminate point needs a coverage event (§2.4).

---

## §4 Candidate pipelines

All three use non-editable gates, information-flow independence for the expectation family, and clause- and decision-revision IDs. They differ in where the formal weight sits. Every precedent below is analogous; none is on a library or API behaviour spec (Part 3).

### Pipeline A: Record-anchored, test-first, light formal core

Precedents: the order in Cunha & Macedo; TiCoder; Fit.

**Gate sequence.**
1. G0 lint of records' typed slots.
2. A **record-derived check set** is produced by lineage B, which sees records only, *before* the spec exists. It contains positive scenarios, rejected-option negatives, and expectation tests, with hard (boundary, special-case) scenarios enumerated by a deliberately different procedure.
3. Lineage A writes the spec as typed slots.
4. G1 upward trace.
5. G2: record-derived checks run against an executable rendering of each clause, plus added-commitment probes to a spec-blind judge.
6. G3 tables; G4 conjunction on shared-variable subsets; G5 vacuity.
7. R built; G6 contract → PBT and state-machine conformance.
8. G7 coverage (presence); G8 per-family kill at equal test counts, plus the allowed-variant check.
9. TLA+ only for environment and history forms, with invariant-mutation probes that must yield counterexamples.

**Expected failure modes.**
- Expectation tests over-strict where a scenario fixes values the decision leaves open (caught by the allowed-variant check).
- About 4 % wrong generated tests, mostly negatives, concentrated on ambiguous requirements (Cunha & Macedo: 30/774; 13 of 14 oracle errors negatives).
- Shared misreadings. Cunha & Macedo's LLM repeated the students' misreading of "colleagues", and correlated lineages make this likelier (Kim et al., MCQ).
- Weaker cross-form conflict detection than Pipeline B (*Inference*).
- Agents stopping early unless the harness imposes per-clause obligations (PBT-Bench, one model, open prompt).

**Small trial on one operation.**
- Seed 10–20 clause mutants that contradict the record (lost case, added commitment, reinterpreted option), regenerate R, and count kills per family at equal test counts. This directly measures the central gap of §2.3.3.
- Rate of wrong tests and judge false alarms.
- Minutes per clause for human witness review.
- Over-strict test count under the allowed-variant R.

### Pipeline B: Common-logic consistency core

Precedents: ReqCheck/Hanfor, EuRailCheck, SAT-LLM, FRET, SCR (Heitmeyer). All efficacy figures are tool-author case studies.

**Gate sequence.**
1. G0 lint, including declared value domains.
2. **Dual independent slot-filling** of every decision by two lineages, then a mechanical diff. Difference witnesses go to a cross-family judge, and to a human on disagreement.
3. G1 trace.
4. Each normative form is translated into **one shared typed signature** in one logic (SMT, Alloy, or TLA+ for temporal parts).
5. G3 per-table checks.
6. G4 conjunction with unsat cores in k-subsets, then rt-consistency/realizability with environment actions as inputs, plus well-separation.
7. G5 vacuity (interesting witnesses, smoke tests).
8. Unsat cores and witnesses kept as regression fixtures.
9. R at the same granularity; G6 replay + trace validation; G7–G9.

**Expected failure modes.**
- The translation into the common logic is itself a faithfulness step; a failure cannot separate translation error from source flaw (EuRailCheck).
- Solver UNKNOWN or timeouts (Bosch: 18 timeouts in one set; FRET: "unknown" on non-linear arithmetic).
- Connected requirements, for example via mode variables, defeat partitioning, so full runs take hours.
- Difference witnesses resolved by correlated judges.
- LLM translation into the shared signature: one short-paper study on its authors' own dataset (SAT-LLM, n = 55).
- Initial formalisation is costly (Bosch: ~5,000 observables).

**Small trial on one operation.**
- Replay the operation's records and count conflicts found against the brief's known history (tables that disagreed; contradictions missed by earlier checks).
- Time per incremental check vs per full check.
- Difference witnesses produced by dual slot-filling, split into genuine ambiguities vs translation noise.
- Share of findings leading to record clarification vs formalisation fixes. Bosch reported roughly 70/30, a tool-author self-report with part of its results unclassified [V5-55].

### Pipeline C: Single executable source plus an independently authored check set

Precedents: SpecTec, Arm ASL 2017, JEST, Cedar.

**Gate sequence.**
1. One executable formal source per operation (R itself, Quint, or Lean; left open).
2. Markdown prose and other models are **generated** from it.
3. G2 diffs the generated prose against the records clause by clause (SpecTec-style back-generation used as a round-trip check).
4. A **differently structured high-level property set** is written from the records by a separate lineage that never sees the source. Reid rejected properties that restate the spec.
5. The property set is checked against the source (proof or model checking).
6. An expectation suite runs on R. An N-version leg uses DRT between R and an independently built second executable model, built *from the records*.
7. G5 vacuity; G8/G9 mutation.

**Expected failure modes.**
- A misreading in the single source propagates consistently into every generated layer; SpecTec can detect it only via the test suite.
- The independent property set drifts toward restating the source (common mode).
- The second executable shares the first's reading if built from the spec. Even when built from the records, it shares hard-input failures (Knight).
- Per-feature cost of keeping one source executable.
- DRT misses rare inputs (Cedar's non-termination bug).

**Small trial on one operation.**
- Disagreements between the property set and the source, and the share that trace to genuine misreadings (Arm found 12 in a heavily tested spec).
- Yield of the prose-regeneration diff.
- DRT disagreements between the two executables, and how many route back to a record ambiguity (the Cedar string-size pattern).
- Author-hours for the property set vs the source.

**Cross-pipeline trial design (*Inference*).** Run all three on the same operation with the same seeded misreading set. Compare per gate: first gate to fail, false-alarm rate, human minutes, and kills per family at equal test counts. That yields the first direct measurement of whether prose-derived oracles catch what spec-derived ones miss.

---

## §5 Open questions and verification debt

**Open questions (no evidence found).**
1. Do prose-derived oracles catch spec misreadings that spec-derived oracles miss? No study compares them on the same faults.
2. What is the recall of round-trip and dual formalization on *shared* misreadings against an independent gold? Watt et al. FM 2021 does not answer it [V4-11].
3. What is the precision of LLM faithfulness judges on API or behaviour specs? All measurements are maths/Lean; the correlation data are MCQ.
4. How many witnesses are needed, and how different must they be?
5. Realizability checking has not been applied to a library or storage API.
6. Agents writing realizable specs, or repairing unrealizable ones, have not been studied.
7. Agents maintaining consistency as clauses accumulate have not been studied, and incremental consistency cost has not been measured. Leino–Wüstholz measures incremental *verification* only.
8. No TLA+, P or Lean spec-mutation tool with published kill rates exists. TLA+-Bench's probe was re-checked and is incoherent as worded, so no reliable TLA+ vacuity rate exists.
9. No per-family kill gate on a reference model has been tested. Nor has any size-controlled study of mutation score vs real faults for spec or model mutants.
10. Outcome-set oracles vs relaxation flags have not been compared.
11. Agents authoring trace links, writing coverage annotations, or triaging spec-mutant survivors have not been measured.
12. No LLM trace recovery figures exist for requirement → test or prose → clause.
13. No refinement-check bridge has been measured; no Alloy/Lean ↔ Python bridge evidence was found.
14. Common-mode error when one LLM writes both spec and tests from the same prose is unmeasured, as is an LLM refuter on spec-vs-prose mutants.
15. No head-to-head comparison of human-review artefacts (trace vs table vs paraphrase) exists.
16. Over-strictness of LLM-written acceptance tests has not been measured.
17. No neutral benchmark of history checkers (Porcupine, Knossos, OmniLink) was found.
18. No study isolates the effect of independent derivation within IV&V or Cleanroom.

**Verification debt after this run.**

| Item | Track | Status now |
|---|---|---|
| Papadakis et al. ICSE 2018 | T4 | **Resolved**: full text, A [V3-01] |
| Knight & Leveson 1986 | T5 | [unreachable]; core claim via Knight NASA report (B) [V3-05] |
| Eckhardt & Lee 1985 | T5 | [unreachable]; NASA TM 86369 read (B) [V3-06] |
| Littlewood & Miller 1989 | T5 | [unreachable]; abstract only [V3-07] |
| Beer et al. CAV 1997 | T2 | CAV text [unreachable]; FMSD 2001 read; experience estimate [V3-09] |
| Heitmeyer et al. TOSEM 1996 | T2 | **Resolved**: full text, A [V3-10] |
| Selby, Basili, Baker TSE 1987 | T3 | Partial (6 of 11 scanned pages); no evidence for independent testing [V3-11] |
| NASA IV&V ROI | T3 | Partly retrieved (DoLILU, Hunt slides); Dabney papers and VT 1998 full text [unreachable] [V4-01, V4-02] |
| Fedchin et al. NFM 2023 (DTest) | T3 | **Resolved**: full text, A [V4-03] |
| AWS "Systems Correctness Practices" CACM 2025 | T3/T4 | [unreachable] (403); FMCAD 2025 abstract only [V4-06] |
| Katis et al. CAV 2022 | T2 | **Resolved** [V4-07] |
| Leino & Wüstholz CAV 2015 | T2 | **Resolved** [V4-08] |
| Whalen et al. ISSTA 2006 | T4 | [unreachable]; follow-up read (A-pre) [V4-09] |
| Huo & Clause FSE 2014 | T3 | [unreachable]; figures via dissertation [V4-10] |
| Watt et al. FM 2021 | T2 | **Resolved**; not dual-formalization evidence [V4-11] |
| Mashkoor & Jacquot REJ 2017 | T1 | **Resolved** (HAL submitted version); qualitative only [V4-13] |
| Melnik et al. Agile 2006 | T3 | [unreachable]; XP 2007 replacement read [V4-14] |
| Ricca et al. ICSE 2008; IST 2009 | T1/T3 | [unreachable]; effort disagreement unresolved [V4-15] |
| Black, Okun, Yesha; Ammann & Black | T4 | [unreachable] [V4-16] |
| van Lamsweerde, Darimont, Letier TSE 1998; Zave & Jackson 1993; Saarland fb14-96-06 | T1/T2 | [unreachable] [V4-17] |
| Hughes: AUTOSAR, Dropbox, "Experiences with QuickCheck" | T3 | [unreachable] [V4-18] |
| Snook & Harrison 2004; Finney 1996 | T5 | Abstracts only [V4-19] |
| DO-178C; ISO 26262; OSLC/ReqIF; StrictDoc failure behaviour | T4 | Not attempted [V4-20] |
| Mäder & Egyed EMSE 2015 | T4 | [unreachable]; author summary read; 71 vs 52 subjects unresolved [V2-12, V2-13] |
| Gay et al.; PBT-Bench; SysMoBench Table 3; TLA+-Bench probe; Req2LTL "correct" | T1/T3/T4 | **Resolved** [V2-01–V2-11] |
| FormalAlign, PROPAS, DMN, Cirstea, CCF, AlgoVeri venues | T1–T3 | **Resolved**, all A [V2-14–V2-19] |
| SAT-LLM track (short/NIER); DSpec2Test venue; CodeJudgeBench ACL 2026; PBT-Bench NeurIPS acceptance | T2/T3/T5 | Not verified |
| DMN BPM camera-ready; Gay TSE published version | T2/T4 | Figures checked against preprints only |
| Doorstop exit code | T4 | Not re-checked against CLI source |
| Kamsties et al. 2001; Brilliant/Knight/Leveson; FormalRx; AeroReq2LTL; Großer et al.; NL2CTL; Alloy output-forms study; Hahn et al.; Coins; PBR/Regnell | T1 | Unchanged from the earlier run (abstract/extract only or [unreachable]); not attempted |
| Zave & Jackson; EuRailCheck "almost thirty experts"; ECEASST 2018; iProperty; ICLP 2020; TLC never-enabled warnings | T2 | Unchanged; not attempted |
| CrossHair, deal; FoundationDB SIGMOD 2021; Jepsen; Coyote; Bisharat et al. (abstract only); NonDex ICST 2016; OpenAI SWE-bench Verified post; Patel & Hierons; Guderlei & Mayer | T3 | Unchanged; not attempted |
| μAlloy demo; cosmic-ray; mutatest; Quint/P coverage docs; AIRE'25; TraceLLM; "Prompts Matter"; Klemens thesis; arXiv 2010.06505; Papadakis 2019 survey | T4 | Unchanged; not attempted |
| Zimmerman RSML; FRET NTRS 20200002241; Kiro; ESMeta; Sail | T5 | Unchanged; not attempted |

---

## §6 Sources with grades

"Agents" = LLMs or agents measured doing the step. Indep.: TA, V, CB as defined above; "—" = none noted. "Log" gives the main row(s); "nr" = not re-checked in this run (the earlier run's full-text read stands).

| Source | Grade | Full text | Agents | Indep. | Log |
|---|---|---|---|---|---|
| Amrollahi, Lopez, Barrett, Roundtrip, [arXiv 2604.25031](https://arxiv.org/abs/2604.25031) | A-pre | yes | yes | — | V1-19 |
| Poiroux et al., EMNLP 2025, [arXiv 2406.07222](https://arxiv.org/abs/2406.07222) | A | yes | yes | — | V1-20 |
| Lu et al., FormalAlign, ICLR 2025, [arXiv 2410.10135](https://arxiv.org/abs/2410.10135) | **A** | yes | yes | TA | V1-30, V2-14 |
| Saha et al., NeuroSTAR, [arXiv 2609.03161](https://arxiv.org/abs/2609.03161) | A-pre | yes | yes | TA | V1-22 |
| Sun et al., Clover, [arXiv 2310.17807](https://arxiv.org/abs/2310.17807) | A-pre/A | yes | yes | TA | V1-45 |
| Easterbrook & Callahan, RE'97, [NTRS](https://ntrs.nasa.gov/api/citations/19970007163/downloads/19970007163.pdf) | A | yes | no | TA | V1-21 |
| Mavridou et al., FRET Lockheed Martin, [NTRS](https://ntrs.nasa.gov/citations/20205000433) | A | yes | no | TA | V1-23 |
| Greenman et al., Programming 2023, [arXiv 2211.01677](https://arxiv.org/abs/2211.01677) | A | yes | no | — | V1-24 |
| Req2LTL, ASE 2025, [arXiv 2512.17334](https://arxiv.org/abs/2512.17334) | A | yes | yes | TA | V1-25, V2-08 |
| Ricca et al., IWPSE 2007, [PDF](https://profs.scienze.univr.it/ceccato/papers/2007/iwpse2007.pdf); ECEASST 2007, [PDF](https://profs.scienze.univr.it/ceccato/papers/2007/evol2007.pdf) | A-workshop | yes | no | — | V1-26; nr |
| Cosler et al., nl2spec, CAV 2023, [arXiv 2303.04864](https://arxiv.org/abs/2303.04864) | A | yes | yes | TA | V1-28 |
| Lahiri, FMCAD 2024, [arXiv 2406.09757](https://arxiv.org/abs/2406.09757) | A | yes | yes | — | V1-29 |
| Cunha & Macedo, FM 2026, [arXiv 2510.23350](https://arxiv.org/abs/2510.23350) | **A** | yes | yes | — | V1-10, V1-11 |
| Jovanovic & Sullivan, SEFM 2024, [PDF](https://par.nsf.gov/servlets/purl/10615156) | A | yes | no | — | V1-18, V1-27 |
| Mashkoor & Jacquot, REJ 2017, [HAL](https://hal.science/hal-01262115/document) | A | yes (submitted version) | no | TA | V4-13 |
| Quint docs, [checking properties](https://quint.sh/docs/checking-properties) | B | yes | — | V | nr |
| Langenfeld et al., Bosch, RE 2019, [PDF](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf) | A | yes | no | TA | V5-01–06 |
| Becker et al., Hanfor, REFSQ 2021, [PDF](https://ultimate-pa.github.io/hanfor/references/publications/hanfor-semantic-requirements-review-at-scale.pdf) | A-workshop | yes | no | TA | nr |
| Cimatti et al., EuRailCheck, [arXiv](https://arxiv.org/pdf/1003.1741v1.pdf) | A-workshop | yes | no | TA | nr |
| Filipovikj et al., PROPAS, ACM SIGAPP ACR 17(4), [PDF](https://www.es.mdh.se/pdf_publications/4980.pdf) | A | yes | no | TA | V2-15 |
| Fazelnia et al., SAT-LLM, ASE 2024, [PDF](https://par.nsf.gov/servlets/purl/10574434) | **A** (short) | yes | yes | TA | V5-07 |
| Calvanese et al., DMN, BPM 2016, [arXiv 1603.07466](https://arxiv.org/pdf/1603.07466) | **A** | yes (arXiv) | no | TA | V2-16, V5-08 |
| Heitmeyer, Jeffords, Labaw, TOSEM 1996, [PDF](http://dslab.konkuk.ac.kr/class/2010/10RE/Automated%20Consistency%20Checking%20of%20Requirements%20Specification.pdf) | A | yes | no | TA | V3-10 |
| TableWise NASA page, [link](https://shemesh.larc.nasa.gov/fm/oldfm/fm-old-sw-ver-tablewise.html) | C | yes | no | TA | nr |
| van Lamsweerde & Letier, [PDF](https://webperso.info.ucl.ac.be/~avl/files/avl-MontereyLNCS.pdf) | A-workshop | yes | no | — | nr |
| Degiovanni et al., ASE 2018, [PDF](https://nmaguirre.github.io/assets/pdf/ase2018.pdf); critique [arXiv 2203.12903](https://arxiv.org/pdf/2203.12903) | A; A-pre | yes | no | TA | nr |
| Nuseibeh, Easterbrook, Russo 2000, [PDF](https://typeset.io/pdf/leveraging-inconsistency-in-software-development-4me5sgffk1.pdf) | A | yes | no | — | nr |
| Mavridou et al., FRET realizability, FM 2021, [NTRS](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf) | A | yes | no | TA | V5-09 |
| Katis et al., CAV 2022, [Springer OA](https://link.springer.com/content/pdf/10.1007/978-3-031-13188-2_24.pdf) | A | yes | no | TA | V4-07 |
| Maoz & Shalom, ICSE 2021, [arXiv 2103.00297](https://arxiv.org/pdf/2103.00297) | A | yes | no | TA | V5-10 |
| Maoz & Ringert, FSE 2016, [figshare](https://figshare.com/articles/conference_contribution/On_Well-Separation_of_GR_1_Specifications/10223099) | A | yes | no | TA | V5-11 |
| Kupferman & Vardi, CHARME 1999, [PDF](https://typeset.io/pdf/vacuity-detection-in-temporal-model-checking-290v578apa.pdf) | A | yes | no | — | nr |
| Beer et al., FMSD 2001, [PDF](https://www.cs.toronto.edu/~chechik/courses05/csc2108/beer01.pdf); CAV 1997 [unreachable] | A venue (figure = experience) | yes / no | no | TA | V3-09 |
| Post, Hoenicke, Podelski, RE 2011, [PDF](https://jochen-hoenicke.de/docs/php11-re.pdf) | A | yes | no | — | V3-09 |
| Blanchard et al., Frama-C smoke tests, TAP 2024, [PDF](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf) | A | yes | no | TA | V5-13 |
| Dafny proof dependencies, [blog](https://dafny.org/blog/2023/10/27/proof-dependencies/); Dafny ref, [Attributes](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/Attributes.md) | B | yes | no | V | nr |
| Dafny wiki Cautionary Tales, [link](https://raw.githubusercontent.com/wiki/dafny-lang/dafny/Cautionary-Tales.md) | C | yes | no | — | nr |
| Lean 4 reference, [Axioms](https://lean-lang.org/doc/reference/latest/Axioms/); Alloy tutorial, [link](https://alloytools.org/tutorials/online/maintext-FS-2.html) | B | yes | — | — | nr |
| Leino & Wüstholz, CAV 2015, [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/krml245.pdf) | A | yes | no | TA | V4-08 |
| ProofPulse, [arXiv 2608.30818](https://arxiv.org/pdf/2608.30818) | A-pre | yes | no | TA | nr |
| Vericoding, [arXiv 2509.22908](https://arxiv.org/pdf/2509.22908) | A-pre | yes | yes | TA | V1-46, V5-15 |
| AlgoVeri, ICML 2026, [arXiv 2602.09464](https://arxiv.org/abs/2602.09464) | **A** | yes (32 pp) | yes | CB | V2-19 |
| ReForm, [arXiv 2507.16331](https://arxiv.org/pdf/2507.16331) | A-pre | yes | yes | TA | V5-14 |
| SpecRL, [arXiv 2604.05820](https://arxiv.org/pdf/2604.05820) | A-pre | yes | yes | TA | nr |
| W3C Process, [link](https://www.w3.org/policies/process/); RFC 6410, [link](https://www.rfc-editor.org/rfc/rfc6410.txt); Wasm phases, [link](https://raw.githubusercontent.com/WebAssembly/meetings/main/process/phases.md) | B | yes | — | — | V5-17 |
| Watt, CPP 2018, [PDF](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf) | A | yes | no | — | V5-16 |
| Watt et al., FM 2021, [PDF](https://www.cl.cam.ac.uk/~jp622/two_wasm.pdf) | A | yes | no | — | V4-11 |
| Davis et al., MongoDB, PVLDB 2020, [arXiv 2006.00915](https://arxiv.org/abs/2006.00915) | A | yes | no | V | V5-19–21 |
| Wang et al., Mocket, EuroSys 2023, [PDF](https://gaoyu-cn.github.io/paper/2023-eurosys-mocket.pdf) | A | yes | no | TA | V5-22 |
| Ouyang et al., Remix, EuroSys 2025, [arXiv 2409.14301](https://arxiv.org/abs/2409.14301) | A | yes | no | TA | V5-23 |
| Kuprianov & Konnov slides, [link](https://conf.tlapl.us/2020/09-Kuprianov_and_Konnov-Model-based_testing_with_TLA_+_and_Apalache-Slides.pdf) | C | yes | no | TA | nr |
| Quint Connect posts, [launch](https://quint-lang.org/posts/quint_connect), [Emerald](https://quint-lang.org/posts/quint_connect_emerald) | C | yes | yes (n = 1) | V | nr |
| Fedchin et al., DTest, NFM 2023, [PDF](https://cdn.amazon.science/b9/d4/eeb4fe1a47609f75956dd6fbc0c6/a-toolkit-for-automated-testing-of-dafny.pdf) | **A** | yes | no | TA (+AWS) | V4-03 |
| Pinto et al., DSpec2Test, [arXiv 2609.29713](https://arxiv.org/pdf/2609.29713v1) | A-pre | yes | no | TA | V4-05 |
| Deligiannis et al., P#, FAST 2016, [PDF](https://www.doc.ic.ac.uk/~afd/papers/2016/FAST.pdf) | A | yes | no | TA | nr |
| PObserve docs, [link](https://p-org.github.io/P/advanced/pobserve/pobserve) | B | yes | no | V | nr |
| icontract-hypothesis, [README](https://raw.githubusercontent.com/mristin/icontract-hypothesis/master/README.rst); Hypothesis, [stateful](https://hypothesis.readthedocs.io/en/latest/stateful.html), [API](https://hypothesis.readthedocs.io/en/latest/reference/api.html) | B | yes | — | — | nr |
| Vikram et al., [arXiv 2307.04346](https://arxiv.org/abs/2307.04346) | A-pre | yes | yes | TA (own metric) | V5-30 |
| Maaz et al., Agentic PBT, NeurIPS 2025 DL4Code, [arXiv 2510.09907](https://arxiv.org/abs/2510.09907) | A-workshop | yes | yes | V | V5-31 |
| PBT-Bench, [arXiv 2605.15229](https://arxiv.org/abs/2605.15229) | A-pre (acceptance claimed) | **yes (full)** | yes | — | V2-01–03 |
| Porcupine, [README](https://raw.githubusercontent.com/anishathalye/porcupine/master/README.md); [blog](https://anishathalye.com/testing-distributed-systems-for-linearizability/) | B; C | yes | no | TA | V1-07 |
| Hackett et al., OmniLink, [arXiv 2601.11836](https://arxiv.org/abs/2601.11836) | A-pre | yes | no | CB | V1-05, V1-06 |
| Pine, [arXiv 2608.17388](https://arxiv.org/pdf/2608.17388) | A-pre | yes | no | builds on Porcupine | V1-08 |
| FoundationDB testing, [link](https://apple.github.io/foundationdb/testing.html) | B | yes | no | V | nr |
| Disselkoen et al., Cedar, FSE Companion 2024, [arXiv 2407.01688](https://arxiv.org/abs/2407.01688) | A | yes | no | V | V1-01, V1-04, V5-27–29 |
| Cedar extended, OOPSLA 2024, [arXiv 2403.04651](https://arxiv.org/pdf/2403.04651) | A | yes | no | V | V1-01, V1-03 |
| cedar-spec READMEs, [2.0.x](https://raw.githubusercontent.com/cedar-policy/cedar-spec/release/2.0.x/README.md), [2.4.x](https://raw.githubusercontent.com/cedar-policy/cedar-spec/release/2.4.x/README.md), [main](https://raw.githubusercontent.com/cedar-policy/cedar-spec/main/README.md); AWS Lean blog, [link](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/) | B | yes | no | V | V1-02 |
| Cirstea, Kuppe, Loillier, Merz, SEFM 2024, [arXiv 2404.16075](https://arxiv.org/abs/2404.16075) | **A** | yes | no | TA | V2-17, V5-24 |
| Howard et al., CCF, NSDI 2025, [arXiv 2406.17455](https://arxiv.org/abs/2406.17455) | **A** | yes | no | V | V2-18, V5-25 |
| Hackett & Beschastnikh, TraceLink, OOPSLA 2025, [PDF](https://www.cs.ubc.ca/~bestchai/papers/oopsla25-trace-link.pdf) | A | yes | no | TA | V5-26 |
| SysMoBench, ICLR 2026, [arXiv 2509.23130](https://arxiv.org/abs/2509.23130) | **A** | yes | yes | TA | V2-04, V2-05 |
| Konnov, TLA+ Community Meeting 2026, [slides](https://conf.tlapl.us/2026-etaps/konnov-2026.pdf) | C | yes | yes (n = 2) | TA | nr |
| Bisharat et al., [arXiv 2606.05792](https://arxiv.org/abs/2606.05792) | A-pre | abstract only | yes | — | nr |
| Binamungu & Maro, BDD mapping, [arXiv 2305.05567](https://arxiv.org/abs/2305.05567) | A | yes | n/a | — | nr |
| Melnik & Maurer, XP 2007, [PDF](https://scispace.com/pdf/multiple-perspectives-on-executable-acceptance-test-driven-2gjlzftall.pdf) | A-workshop | yes | no | — | V4-14 |
| Karpurapu et al., [arXiv 2403.14965](https://arxiv.org/pdf/2403.14965); Sami et al., [arXiv 2504.07244](https://arxiv.org/pdf/2504.07244); AToMIC, [arXiv 2510.18861](https://arxiv.org/pdf/2510.18861) | A-pre | yes | yes | TA | nr |
| Fakhoury et al., TiCoder, TSE 2024, [arXiv 2404.10100](https://arxiv.org/pdf/2404.10100) | A | yes | yes | TA | V5-36 |
| Leveson et al., TSE 1990, [PDF](https://typeset.io/pdf/the-use-of-self-checks-and-voting-in-software-error-trhc4ta53s.pdf) | A | yes | no | — | V5-32 |
| Selby, Basili, Baker, TSE 1987, [PDF](http://www.cs.umd.edu/~basili/publications/journals/J33.pdf) | A | partial (6/11 pp) | no | — (tester was an author) | V3-11, V3-12 |
| Neal et al., IV&V cost effectiveness, [NTRS](https://ntrs.nasa.gov/api/citations/19980027712/downloads/19980027712.txt) | B | yes | no | TA (partial) | V4-01 |
| Hunt, IV&V ROI slides 2012, [PDF](https://www.nasa.gov/wp-content/uploads/2016/10/1-4a-ivv_conference_bob_hunt_dulos_kalman.pdf) | C | yes | no | — | V4-01 |
| Barr et al., TSE 2015, [PDF](https://discovery.ucl.ac.uk/id/eprint/1471263/1/06963470.pdf) | A | yes | n/a | — | nr |
| Konstantinou et al., [arXiv 2410.21136](https://arxiv.org/abs/2410.21136) | A-pre | yes | yes | — | V5-34 |
| Zhao, Zhou, Cohen, ISSTA 2026, [arXiv 2607.22883](https://arxiv.org/pdf/2607.22883) | A | yes | yes | — | V5-33, V1-51 |
| Mathews & Nagappan, [arXiv 2412.14137](https://arxiv.org/abs/2412.14137) | A-pre | yes | yes | — | V5-35 |
| Canedo, [arXiv 2608.17214](https://arxiv.org/pdf/2608.17214) | A-pre | yes | no | — | nr |
| Wang, Pradel, Liu, PatchDiff, ICSE 2026, [arXiv 2503.15223](https://arxiv.org/abs/2503.15223) | A | yes | yes | TA | V5-42 |
| Gyori et al., NonDex, JPF 2016, [PDF](https://mir.cs.illinois.edu/gyori/pubs/jpf16.pdf) | A-workshop | yes | no | TA | V5-41 |
| Wasm interpreter [README](https://raw.githubusercontent.com/WebAssembly/spec/main/interpreter/README.md); relaxed-SIMD [Overview](https://raw.githubusercontent.com/WebAssembly/relaxed-simd/main/proposals/relaxed-simd/Overview.md); sqllogictest [about.wiki](https://raw.githubusercontent.com/gregrahn/sqllogictest/master/about.wiki); JSON-Schema-Test-Suite [README](https://raw.githubusercontent.com/json-schema-org/JSON-Schema-Test-Suite/main/README.md); Open POSIX [result codes](https://raw.githubusercontent.com/linux-test-project/ltp/master/testcases/open_posix_testsuite/Documentation/HOWTO_ResultCodes) | B | yes | — | — | V5-37–40 |
| OpenFastTrace, [report](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/doc/user_guide/reference/console_tracing_report.md), [LinkStatus](https://raw.githubusercontent.com/itsallcode/openfasttrace/main/api/src/main/java/org/itsallcode/openfasttrace/api/core/LinkStatus.java); sphinx-needs, [config](https://sphinx-needs.readthedocs.io/en/latest/configuration.html); Doorstop, [validation](https://raw.githubusercontent.com/doorstop-dev/doorstop/develop/docs/cli/validation.md) | B | yes | — | — | V5-54 |
| StrictDoc guide, [link](https://strictdoc.readthedocs.io/en/stable/stable/docs/strictdoc_01_user_guide.html) | B (partial) | partial | — | — | nr |
| Mäder & Egyed, EMSE 2015, [author summary SE 2016](https://dl.gi.de/bitstreams/b9fc3267-9d74-4127-ab3a-2a512de7ed2c/download) | A | **no** (EMSE [unreachable]) | no | — | V2-12 |
| Fuchß et al., LiSSA, ICSE 2025, [PDF](https://publikationen.bibliothek.kit.edu/1000179816/164563088) | A | yes | yes | TA | V5-43 |
| Goldweber et al., IronSpec, OSDI 2024, [PDF](https://par.nsf.gov//servlets/purl/10550356) | A | yes | no | TA | V5-44 |
| Amaral et al., MutDafny, [arXiv 2511.15403](https://arxiv.org/pdf/2511.15403) | A-pre | yes (v1, v2) | indirect | TA | V5-18, V5-45 |
| Jovanovic, Patwary, Sullivan, FormaliSE 2025, [PDF](https://allisonius.github.io/files/FormaliSE2025.pdf) | A | yes | no | TA (partial) | V5-46 |
| TLA+-Bench, [arXiv 2607.23425](https://arxiv.org/pdf/2607.23425) | A-pre | yes | yes | TA | V2-06, V2-07 |
| TLA-Prover, [arXiv 2606.06133](https://arxiv.org/pdf/2606.06133) | A-pre | yes | yes | TA | nr |
| Richter & Wehrheim, NL2Contract, [arXiv 2510.12702](https://arxiv.org/pdf/2510.12702) | A-pre | yes | yes | TA | nr |
| mutmut, [README](https://raw.githubusercontent.com/boxed/mutmut/main/README.rst) | B | yes | — | — | nr |
| Petrović et al., Google mutation, ICSE-SEIP 2021, [arXiv 2103.07189](https://arxiv.org/abs/2103.07189) | A | yes | no | V | V5-47 |
| Wang et al., TOSEM 2025, [arXiv 2406.09843](https://arxiv.org/pdf/2406.09843) | A | yes | yes | — | V5-48 |
| Meta ACH, [arXiv 2501.12862](https://arxiv.org/pdf/2501.12862) | A | yes | yes | V + TA | V5-49 |
| Just et al., FSE 2014, [PDF](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf) | A | yes | no | TA (partial) | V5-50 |
| Chekam et al., ICSE 2017, [PDF](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf) | A | yes | no | — | V5-51 |
| Papadakis et al., ICSE 2018, [PDF](https://typeset.io/pdf/are-mutation-scores-correlated-with-real-fault-detection-a-t9e7f0t5d6.pdf) | A | **yes** | no | — | V3-01–03 |
| Gay et al., TSE 2015, [preprint](https://www.greggay.com/pdf/15covrisks.pdf) | A | **yes (17 pp)** | no | TA (partial) | V2-10, V2-11 |
| Staats, Whalen, Rajan, Heimdahl, UFC follow-up, [UMN](https://conservancy.umn.edu/server/api/core/bitstreams/a533c3cb-0812-4e95-b113-7d221af01318/content) | A-pre | yes | no | TA | V4-09 |
| Huo, dissertation (Huo & Clause FSE 2014 data), [UDSpace](https://udspace.udel.edu/items/751e4abc-141b-4795-9bbe-4d56cc8fa965) | A-pre | yes (Ch. 3) | no | TA | V4-10 |
| Inozemtseva & Holmes, ICSE 2014, [PDF](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf) | A | yes | no | — | V1-49 |
| TLA+ wiki coverage, [link](https://docs.tlapl.us/_export/raw/using:coverage); QuickCheck Haddock, [link](https://hackage.haskell.org/package/QuickCheck-2.14.3/docs/Test-QuickCheck.html) | B (draft); B | yes | — | — | nr |
| Hughes, How to Specify It!, TFP 2019, [PDF](https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf) | A | yes | no | TA | V5-52 |
| Goldstein et al., ICSE 2024, [PDF](https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf) | A | yes | no | — | V5-53 |
| Desai, FMCAD 2025 talk abstract, [reposiTUm](https://repositum.tuwien.at/handle/20.500.12708/219530) | B | yes (1 p) | no | V | V4-06 |
| Kim et al., ICML 2025, [arXiv 2506.07962](https://arxiv.org/pdf/2506.07962) | A | yes | yes | — | V1-12, V1-13 |
| Huang et al., ICLR 2024, [arXiv 2310.01798](https://arxiv.org/pdf/2310.01798) | A | yes | yes | — | V1-32 |
| Kamoi et al., TACL 2024, [arXiv 2406.01297](https://arxiv.org/pdf/2406.01297) | A | yes | yes | — | V1-33 |
| Panickssery et al., NeurIPS 2024, [arXiv 2404.13076](https://arxiv.org/pdf/2404.13076) | A | yes | yes | — | V1-34 |
| CodeJudgeBench, [arXiv 2507.10535](https://arxiv.org/pdf/2507.10535) | A-pre | yes | yes | — | V1-35 |
| Jin & Chen, ASE journal 2026, [arXiv 2603.00539](https://arxiv.org/pdf/2603.00539) | **A** | yes | yes | — | V1-36 |
| Broccia et al., [arXiv 2608.21298](https://arxiv.org/pdf/2608.21298) | A-pre | yes | yes | — | V1-37 |
| Smit et al., ICML 2024, [arXiv 2311.17371](https://arxiv.org/pdf/2311.17371) | A | yes | yes | — | V1-38 |
| Choi et al., NeurIPS 2025, [arXiv 2508.17536](https://arxiv.org/pdf/2508.17536) | **A** | yes | yes | — | V1-38 |
| McAleese et al., [arXiv 2407.00215](https://arxiv.org/pdf/2407.00215) | A-pre | yes | yes | V | V1-39 |
| Zhang et al., Beyond Compilation, [arXiv 2606.31002](https://arxiv.org/pdf/2606.31002) | A-pre | yes | yes | TA | V1-31 |
| MathAtlas, [arXiv 2605.14061](https://arxiv.org/pdf/2605.14061) | A-pre | yes | yes | TA | V1-40 |
| Mohammad & Sheikh, Faithfulness Gap, [arXiv 2606.16541](https://arxiv.org/pdf/2606.16541) | A-pre (caution) | yes | yes | — | nr |
| Reid, OOPSLA 2017, [PDF](https://alastairreid.github.io/papers/oopsla2017-whoguardstheguards.pdf); FMCAD 2016, [PDF](https://alastairreid.github.io/papers/fmcad2016-trustworthy.pdf) | A | yes | no | V | V1-41, V1-44 |
| JEST, ICSE 2021, [arXiv 2102.07498](https://arxiv.org/pdf/2102.07498) | A | yes | no | TA | V1-42 |
| Youn et al., SpecTec, PLDI 2024, [PDF](https://people.mpi-sws.org/~rossberg/papers/Youn,%20Shin,%20Lee,%20Ryu,%20Breitner,%20Gardner,%20Lindley,%20Pretnar,%20Xiaojia,%20Watt,%20Rossberg%20-%20Bringing%20the%20WebAssembly%20Standard%20up%20to%20Speed%20with%20SpecTec.pdf) | A | yes | no | TA | V1-43 |
| Knight, NASA progress report 1986, [NTRS](https://ntrs.nasa.gov/api/citations/19870002808/downloads/19870002808.pdf); Knight & Leveson TSE 1986 [unreachable] | B; A [unreachable] | yes; no | no | — | V3-05 |
| Eckhardt & Lee, NASA TM 86369, [NTRS](https://ntrs.nasa.gov/api/citations/19850015006/downloads/19850015006.pdf); TSE 1985 [unreachable] | B; A [unreachable] | yes; no | no | — | V3-06 |
| Littlewood & Miller, TSE 1989, [NTRS abstract](https://ntrs.nasa.gov/citations/19900036555) | A (abstract only) | no | no | — | V3-07 |
| Czepa et al., [PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6944266/fullTextXML) | A | yes | no | — | V1-47 |
| Mavridou, Farrell, Vázquez et al. 2025, [arXiv 2512.15788](https://arxiv.org/pdf/2512.15788) | A-pre (claim C-level) | yes | anecdotal | TA | V1-48 |
| Finney 1996, [GALA](https://gala.gre.ac.uk/id/eprint/25) | — (abstract only) | no | no | — | V4-19 |
| GitHub Spec Kit, [spec-driven.md](https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md) | D/B | yes | no data | V | V1-50 |

---

# Part 3. Self-check and limits

## 3.1 Recommendations: transfer, confidence, and the one finding that would overturn each

Transfer: *direct* = evidence on library or API behaviour specs; *analogous* = other spec domains; *inference* = reasoning. No recommendation rests on direct evidence of **effectiveness**. Direct evidence exists only for oracle and tooling **mechanisms**: POSIX, sqllogictest, JSON Schema, NonDex, Hypothesis, and Vikram's LLM PBTs from Python API docs.

| # | Recommendation | Transfer | Confidence | One finding that would overturn it |
|---|---|---|---|---|
| R1 | Record-derived, spec-blind positive scenarios and negatives, drafted before the spec (G2; Pipeline A) | analogous (Cunha & Macedo: Alloy, student specs, one LLM; Lahiri) | medium | A one-operation trial in which record-derived checks kill under half of seeded clause misreadings, or raise more false alarms than kills |
| R2 | Use rejected options as negatives | inference (no source does this) | low | Rejected-option negatives mostly duplicating positive-scenario failures, or mostly over-strict |
| R3 | Added-commitment probe judged spec-blind; every "not addressed" goes to a human | inference + analogous (NeuroSTAR) | low | A spec-blind judge missing most seeded added commitments |
| R4 | Cross-family judges must agree to accept; human on rejection; calibrate and recalibrate on model change | analogous (maths/Lean judges; MCQ correlation) | low–medium | Calibration on human-labelled API-spec clauses showing the two-family rule no more precise than a single judge |
| R5 | Common-logic conjunction with minimal inconsistent subsets; k-subset per edit, full run nightly | analogous (Bosch, PROPAS, SAT-LLM, Heitmeyer; all TA) | medium | Store-API contracts with quantifiers over handed-out objects returning UNKNOWN or timing out for most subsets |
| R6 | Per-table complete/disjoint check with declared value domains (G3) | analogous (DMN, Heitmeyer); decidable | high (mechanism) | Table guards needing non-linear or unbounded predicates, making completeness undecidable |
| R7 | rt-consistency / realizability with environment actions, plus well-separation (G4) | inference by analogy (FRET, GR(1)); no library application | low | Bounded TLC/Apalache with free environment actions infeasible for one operation, or finding nothing plain model checking misses |
| R8 | Vacuity gates before trusting any pass: smoke tests, interesting witnesses, mutated invariant must yield a counterexample (G5) | analogous (Frama-C cost; Beer experience; TLA-Prover; IronSpec) | medium | Vacuity gates on agent-written specs for this domain flagging mostly intended non-commitments |
| R9 | Frame divergence check against effect/failure/cancellation tables | analogous (no detection data) + inference | low | Bounded model checking with enumerated environment states already catching all seeded frame/effect clashes |
| R10 | Witness coverage criterion instead of "≥2 witnesses" | inference | low–medium | A second, differently built witness finding more ambiguities than per-profile witnesses from the same lineage |
| R11 | Harness imposes one test obligation per clause ID; agents get clause text, not R source | direct (Vikram: Python APIs, 21 %) + analogous (PBT-Bench, one model, +41.5 pp) | medium | Per-clause obligations not raising clause coverage or mutant kills over a single whole-spec instruction |
| R12 | F ↔ R bridges in both directions; reviewed `alpha`; full-state logging (G6) | analogous (Cedar, MongoDB, Mocket, Cirstea, CCF, TraceLink) | medium | DRT/replay between an agent-written model and an agent-written R showing zero disagreement on seeded misreadings (common mode) |
| R13 | Expectation family: information-flow isolation + anchoring lint + a deliberately different derivation for hard scenarios | analogous (Leveson, Zhao, Arm, JEST, Knight, Eckhardt & Lee) + inference | low–medium | The central trial: prose-derived checks killing seeded misreadings no better than spec-derived tests |
| R14 | Non-commitment oracles (`either`/predicate/canonicalisation/UNSUPPORTED/UNRESOLVED) | direct (mechanisms) | high (mechanism) | Profile values or non-promised dimensions interacting, so per-value suites miss pairwise conflicts |
| R15 | Allowed-variant check with a NonDex-style perturbing R | direct mechanism (NonDex, single source, second-hand figures) + inference | medium | Perturbing R on a non-promised dimension violating other clauses, so over-strictness cannot be isolated |
| R16 | Trace links written at creation; deterministic G0/G1; LLM recovery only to audit | direct tooling (B) + analogous (LiSSA) | high for link-gate mechanics; low for G1 catching added commitments | Seeded added commitments carrying plausible links all passing G1 |
| R17 | Mutation as gap finder; per-family kill compared at equal test counts (G8) | inference; building blocks analogous (Papadakis, MutDafny, IronSpec, Alloy4Fun) | low–medium | Seeded misreadings killed by both families near 100 % (no discrimination), or equivalent-mutant triage costing more than the findings (MutDafny: 157 of 284 equivalent) |
| R18 | Coverage only as necessary-condition gates; clause coverage = presence check | analogous (Gay, UFC, Inozemtseva, Hughes) | medium–high | Clause-coverage-complete suites beating equal-size random suites on clause mutants of a reference model |
| R19 | Spec-strength mutation (G9) | analogous (IronSpec, single source) | medium–low | Survivors dominated by intended non-commitments even after register-based auto-classification |
| R20 | Gate order: G5 before trusting model checking; G8/G9 after G6 | inference, consistent with IronSpec | high (logical) / medium (order cost) | A non-conforming R yielding the same mutant-kill picture as a conforming one |
| R21 | Porcupine-style history check of R against its sequential mode | analogous (README self-report; OmniLink CB) | medium | Unspecified outcomes making R's sequential mode nondeterministic, forcing set-valued models (blow-up) |
| P-A | Pipeline A as a candidate | analogous + inference | low–medium | As R13 (the central trial) |
| P-B | Pipeline B as a candidate | analogous (author-run case studies) | medium for conflict detection; low for agent translation | LLM translation into the shared signature introducing more false conflicts than it finds on the brief's real records |
| P-C | Pipeline C as a candidate | analogous (Cedar, SpecTec, Arm, JEST) | low–medium | A second executable built from the records converging on the first's reading, with near-zero DRT disagreements on seeded misreadings |

## 3.2 Source-independence flags

- **Tool or method authors evaluating their own tool (TA)**: Bosch/ReqAnalyzer, Hanfor, FRET (case study, realizability, Katis), Spectra and well-separation, Frama-C smoke tests (CEA + Thales), SAT-LLM (own dataset), PROPAS, DMN, Heitmeyer's SCR checker, Beer et al. (RuleBase), Easterbrook & Callahan, NeuroSTAR, Req2LTL, nl2spec, FormalAlign, Beyond Compilation, MathAtlas, Clover (acknowledging a limit), Mocket, Remix, TraceLink, Cirstea et al. (TLC maintainers), NonDex, PatchDiff, LiSSA, IronSpec, MutDafny, DTest, DSpec2Test, Leino–Wüstholz, the UFC metrics, Huo & Clause, μAlloy operators (partial), Just et al. (partial), Gay et al. (partial, OMC/DC), QuickCheck/Hughes, TiCoder, Vikram (own metric), ReForm, Vericoding, TLA+-Bench, SysMoBench (mapping component), JEST, SpecTec, Mashkoor & Jacquot.
- **Vendor posts or vendor self-reports (V)**: Cedar (AWS; FSE, OOPSLA, READMEs, Lean blog), MongoDB (PVLDB), CCF (Microsoft), Google mutation, Meta ACH, Arm/Reid, McAleese (OpenAI on its own critic), Maaz et al. (vendor-affiliated, Hypothesis maintainer), Quint Connect posts, GitHub Spec Kit, Desai's AWS talk abstract, FoundationDB docs, PObserve docs, Dafny blog.
- **Competing tool or benchmark authors (CB)**: OmniLink on Porcupine; AlgoVeri on Vericoding.
- **No conflict noted**: Zhao, Konstantinou, Mathews & Nagappan, Leveson et al., Chekam, Goldstein, Wang TOSEM, Papadakis, Kim, Huang, Kamoi, Panickssery, Smit, Choi, Jin & Chen, Broccia, Greenman, Czepa, Inozemtseva & Holmes, Poiroux, Lahiri, Cunha & Macedo, Watt, Knight's and Eckhardt & Lee's NASA documents.
- **Consequence** (*Inference*): every measured efficacy figure for conflict, realizability and vacuity tools (Pipeline B's precedents) is author-reported. Only Zhao and Leveson bear on the expectation family without conflict, and neither measures prose-derived vs spec-derived oracles.

## 3.3 What this run did not do

- **No new search** beyond replacement sources needed to settle a claim (cedar-spec READMEs, Pine, Clover, Post et al., Knight's and Eckhardt & Lee's NASA documents, DSpec2Test, Staats et al., Huo's dissertation, Melnik & Maurer 2007, the Mäder & Egyed summary, the FMCAD abstract, IV&V documents).
- **Not re-checked** in §2.2–§2.4: Hanfor, EuRailCheck, van Lamsweerde & Letier, Degiovanni et al. and its critique, Nuseibeh et al., ProofPulse, SpecRL, Kupferman–Vardi, P# FAST 2016, the Quint/Apalache posts, icontract-hypothesis, FoundationDB, Ricca ECEASST, Karpurapu, Sami, AToMIC, the BDD mapping, Canedo, NL2Contract, TLA-Prover, mutmut, the TLC coverage, QuickCheck, Hypothesis, Dafny, Lean and Alloy docs, the W3C Process, Konnov's slides, Bisharat et al., Barr et al., Mohammad & Sheikh. These rows carry "nr" in §6; the earlier run's full-text reads stand unverified by this run.
- **Still [unreachable]**: Knight & Leveson 1986, Eckhardt & Lee TSE, Littlewood & Miller, Beer CAV 1997, the AWS CACM article, Mäder & Egyed EMSE, Whalen ISSTA 2006, Huo & Clause FSE, Melnik 2006, Ricca 2008/2009, Black/Okun/Yesha, Ammann & Black, van Lamsweerde et al. 1998, Zave & Jackson, Saarland fb14-96-06, Hughes' industrial reports, the Dabney ROI papers, the VT 1998 IV&V full text, Snook & Harrison, Finney.
- **Not attempted**: DO-178C, NonDex ICST 2016, the OpenAI SWE-bench Verified post, μAlloy, Großer et al., NL2CTL and the other T1 abstract-only leads.
- **DBLP** was blocked by a bot wall for every verifier. Venues come from PDF headers, Crossref, the arXiv API, OpenReview v2, USENIX and Semantic Scholar.
- **Not compared**: published versions against preprints (DMN BPM camera-ready, Gay TSE, Mashkoor REJ, MutDafny v1/v2 beyond totals).
- **Not confirmed**: the SAT-LLM track, DSpec2Test venue, CodeJudgeBench ACL 2026, PBT-Bench NeurIPS acceptance, the Doorstop exit code, the Oxford Knossos slides (lead only).
- **No trial was run.** No new evidence on library or API behaviour specs was produced.
- The synthesis used the earlier report as its base text and the five verification notes as corrections. It did not re-read the earlier T1–T5 notes line by line; where they differ from the report, only the verifiers' findings were applied.

## 3.4 Self-check: where this run may have misread the brief or a source

1. **Earlier brief §3.** "Earlier brief §3" was read as the "Already settled" section of the earlier brief. The Cedar refutation depends on there being no implicit Cedar–Dafny link elsewhere in that brief; none was found, but an intended link the brief never wrote cannot be ruled out. "Cedar used Dafny earlier" rests on repository READMEs (B), not a peer-reviewed text.
2. **Substantive vs restyled.** The split is a judgement. Grade changes were classed as restyled unless they changed a conclusion. One could argue Cunha & Macedo's A-pre → A belongs with the substantive Kernsatz change; it appears in both places.
3. **Verdict classification.** V4-05 (a new supporting source) was counted as confirmed, and V4-06 (AWS still unreachable) as unverifiable. Rows with confirmed figures but changed grade or qualifier were counted as corrected. Other reasonable rules shift a few counts between confirmed and corrected.
4. **Verifier conflicts.** The TLA+-Bench reading follows V2 over the V3 notes. V2's judgement that the probe is incoherent is itself *Inference*: TLC can also fail for deadlock or other configured properties, and the authors may mean a different run outcome. The DMN, Cirstea and CCF grades follow V2's verified venues over V5's unchecked "A-pre".
5. **Computed, not printed.** Several figures are the verifiers' derivations, not values the papers print:
   - Cunha & Macedo pooled 88.1 %;
   - Maoz–Ringert "40 of 79" (60 − 20);
   - SysMoBench "1/13, 2/13";
   - Papadakis "top 10 % → 11 %" (mapped from sentence order).
6. **Partial or replacement sources.** Knight's figures come from Knight's NASA progress report on the Knight–Leveson programs, not the TSE paper. The ~10× three-version figure was originally reported at FTCS-16, which was not read. Eckhardt & Lee was read as NASA TM 86369, not the TSE version. Selby was read on 6 of 11 scanned pages. Mäder & Egyed was read only as a 2-page author summary. Huo & Clause was read via the dissertation. Mashkoor & Jacquot was read as a HAL submitted version.
7. **Layout extraction.** The following were read from layout extraction and could be misaligned:
   - Bosch minima (two-column extraction);
   - Gay et al. −59.2 % (`pdftotext -layout`, page not rendered);
   - Roundtrip calls-per-repair columns;
   - LiSSA F1 values;
   - Greenman figures (taken from the text, not Table 5).
8. **Venue inferences.** SysMoBench was identified with an OpenReview entry whose title differs ("Specifying" vs "Modeling"). The FRET case-study venue (RE 2020) rests on NTRS file names. Cunha & Macedo's FM 2026 venue rests on the conference page and Semantic Scholar; the arXiv PDF has no venue line.
9. **Transfer labels.** POSIX, sqllogictest, JSON Schema, NonDex and Vikram were labelled *direct*; Cedar (an authorization-language library) and MongoDB's merge function were labelled *analogous*. A looser reading of "library/API behaviour specs" would move Cedar to direct.
10. **Model names.** PBT-Bench's single-bug finding concerns one model from the same vendor as the assistant tooling used in this run. The paper's authors are unaffiliated, so no independence flag was set. Model names in this report appear only as facts of the cited studies.
11. **Scope.** Admitting DSpec2Test as a replacement source reads the verification brief's "except where a claim can only be settled by a replacement source" generously. It supports, but does not settle, the DTest row.
12. **Kernsatz length.** The Kernsatz keeps each sentence to what the full texts carry. The first sentence holds the design and its one measured anchor, and reads long as a result.
