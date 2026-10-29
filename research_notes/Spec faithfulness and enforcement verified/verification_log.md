# Verification log: Spec faithfulness and enforcement verified

Consolidated log of all verification rows from the five verification tracks. It checks the earlier report `reports/Spec faithfulness and enforcement.md` against full texts.

**IDs.** `V1-nn` covers baseline challenges, the Kernsatz, §2.1 (T1), §2.5–§2.7. `V2-nn` covers partial-read figures and grade/venue conflicts. `V3-nn` covers verification-debt classics (Papadakis, Knight & Leveson, Eckhardt & Lee, Littlewood & Miller, Beer, Heitmeyer, Selby). `V4-nn` covers the remaining debt (NASA IV&V, DTest, AWS CACM, the rest of the §5 debt table). `V5-nn` audits §2.2–§2.4, the §3 check map and the §4 pipelines. Each ID is unchanged from its source notes file (`V1_…md` to `V5_…md`), where the verbatim evidence quote and page or section are recorded.

**Sorting.** Rows are sorted by the earlier-report section in which the claim appears (§1, §2.1 … §2.7, §3, §4, §5, §6). A claim checked by two verifiers is one row carrying both IDs, with agreement or conflict noted.

**Columns.**
- Verdict is one of confirmed / corrected / not found / refuted / unverifiable.
- Grade follows the brief: A, A-pre, A-workshop, B, C, D.
- FT = full text read (yes / no / partial).
- Independence flag: **TA** = tool or method authors evaluating their own tool; **V** = vendor post or vendor self-report on its own system; **CB** = authors of a competing tool or benchmark; **none** = no conflict noted.

**Verdict counts** (160 IDs; a merged row counts once per ID):

| Verdict | V1 | V2 | V3 | V4 | V5 | Total |
|---|---|---|---|---|---|---|
| confirmed | 32 | 1 | 6 | 9 | 45 | **93** |
| corrected | 17 | 17 | 3 | 2 | 12 | **51** |
| refuted | 1 | 0 | 0 | 1 | 0 | **2** |
| not found | 1 | 0 | 0 | 0 | 0 | **1** |
| unverifiable | 1 | 1 | 3 | 8 | 0 | **13** |
| IDs | 52 | 19 | 12 | 20 | 57 | **160** |

Classification decisions made in consolidation:
- V4-05 is a new replacement source (DSpec2Test) that supports a §2.3.1 claim, so it is counted as confirmed.
- V4-06 (AWS CACM article still unreachable) is counted as unverifiable, because the article's content was not read, even though V4 phrased it "confirmed (still unreachable)".
- V4-20 (DO-178C, not attempted) is counted as unverifiable.
- Rows whose figures were confirmed but whose grade, qualifier or interpretation changed are counted as corrected.

**Verifier conflicts and how they were settled** (details in the rows):
1. **DMN grade**: V2-16 A (BPM 2016, venue verified) vs V5-08 A-pre (venue not checked). → **A** (V2 checked Crossref; V5 did not check).
2. **Cirstea et al. grade**: V2-17 A (SEFM 2024) vs V5-24 A-pre (not checked). → **A**, same reason.
3. **CCF grade**: V2-18 A (NSDI 2025) vs V5-25 A/A-pre (not checked). → **A**.
4. **Vericoding 9 % / 15 %**: V1-46 and V5-15 both read the full text and agree that the figure is pooled across Dafny, Verus and Lean. The V2 notes repeat the earlier "Verus" wording without re-reading it. → **pooled** (V1/V5).
5. **TLA+-Bench "5 of 18"**: V2-06 read §8.7 in full and finds the probe's survival criterion incoherent as worded. The V3 notes (Beer inference) cite "5 of 18" as measured vacuity evidence without re-reading the paper. → **V2**: treat it as the paper's count for a probe with unclear mechanics, not as a vacuity rate.
6. **Items V1 left unverified (V1-52)**: superseded by V2-10 (Gay), V2-06 (TLA+-Bench), V3-01/02 (Papadakis), V3-05 (Knight & Leveson), V5-32 (Leveson 1990), V5-46 (Alloy 11 %/92 %) and V5-50 (Just 17 %). No disagreement, only different coverage.

---

## §1 Kernsatz

| ID | Claim (earlier report, abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V1-09 | "No published pipeline runs prose records → spec → … with gates that check faithfulness to the prose" | corrected (strength) | n/a | n/a | search result | none | Restate as the earlier run's search result, not proof of absence |
| V1-10 | "about 90% of wrong specs with three tests of each kind" (Cunha & Macedo) | corrected (qualifier + grade) | **A** (FM 2026; was A-pre) | yes | 43 reqs, 4 Alloy domain models; N=3: 36 reqs with complete valid suites, 4,395 wrong student specs; GPT-5 few-shot | none | Mean per requirement 90.1 %; pooled 88.1 % (verifier's arithmetic, 1 − 525/4395) |
| V1-12 | "LLM errors are correlated across models" | confirmed (setting qualifier) | A (ICML 2025) | yes | 349 LLMs × 12,032 MCQs; 71 × 14,042 (HELM); 20 LLMs × 1,800 résumé pairs | none | MCQ setting must be stated |
| V1-14 | "Every reference-free faithfulness check … is necessary-only and blind to shared misreadings" | corrected | A / A-pre | yes | Roundtrip, NeuroSTAR, Clover, FormalAlign, Beyond Compilation | none | LLM judges are not even necessary-only: they over-accept and over-reject |
| V1-15 | "independence must come from the derivation path and the artefact rather than from swapping models" | corrected (label) | n/a | yes (Kim) | — | none | Mark *Inference*; swapping provider reduces correlation, but not enough on its own |
| V1-16 | "prose-derived oracles catch spec misreadings that spec-derived ones miss … remains unmeasured" | confirmed (as search result) | n/a | n/a | — | none | Nearest analogues: Arm 2017, JEST, Cunha & Macedo |
| V3-04 | "independence … verified by per-family mutant kills" | corrected (qualification) | A (basis: Papadakis) | yes | code (C, Java), not specs; transfer analogous | none | Compare kills at equal test counts; kills guide gap-finding but do not measure real-fault detection |
| V3-08 | "independence … enforced by information flow"; §2.5 "derivation path and the artefact" | corrected (qualification); direction confirmed | B (NASA report, TM) | yes (NASA docs) | program versions, not specs or tests | none | Separate development ≠ independent failure (hard inputs); isolation is necessary, not sufficient |

## §2.1 T1 Faithfulness

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V1-11 | Cunha & Macedo table row: 62/83/90/93.6 %; 3.9 % wrong tests (30/774); 67–96 % valid at N=3; ~$3.5 per 258 tests | confirmed (qualifier) | A | yes | as V1-10 | none | Add: per-requirement means over 41/34/36/35/35 of 43 reqs; 13 of 14 oracle errors were negatives in 3 ambiguous reqs; the LLM repeated the students' "colleagues" misreading |
| V1-17 | "By construction they miss shared misreadings, and every full-text source … says so" | confirmed | A-pre / A | yes | — | none | Name the sources: Roundtrip, NeuroSTAR, Clover |
| V1-18 | Jovanovic & Sullivan: "Browsing … rarely reveals what it wrongly forbids"; "Over-constraint is the harder one to spot" | corrected (finding → argument) | A (SEFM 2024) | yes | 93,283 Alloy4Fun submissions; detection difficulty not measured | none | It is the authors' argument, not a measurement |
| V1-19 | Roundtrip figures; "1 annotator"; cost "7.2 LLM calls per repair (vs 19.9)" | figures confirmed; cost and annotator corrected → **corrected** | A-pre | yes | 150 Traffic + 77 Wildlife rules; two providers | none | Cost 6.1–26.4 calls across six runs; 7.2 vs 19.9 is one cell. Annotator = one author with FM training |
| V1-20 | Poiroux EMNLP 2025: BEq+ P 98.0 / R 48.3; BEqL P 100 / R 30.9 | confirmed | A | yes | ProofNetVerif 3,752 pairs | none | — |
| V1-21 | Easterbrook & Callahan RE'97: four different tables; "much easier" | confirmed | A | yes (OCR) | 4 people, 1 FDIR requirement | TA (NASA IV&V on own method) | — |
| V1-22 | NeuroSTAR 87.8 vs 86.2; 89/106 "judged valid by two authors"; "removed 48%" | 87.8/86.2 and 89/106 confirmed; rater protocol and 48 % corrected → **corrected** | A-pre | yes | ConfoNLf; 108 Virginia driving-law sections | TA | Majority of author raters (two, a third on disagreement); "up to 48.43 %" for contamination, triviality, temporal ambiguity, LTLf incompatibility |
| V1-23 | FRET explanations "instrumental"; 69/74 | confirmed (wording fix) | A (RE 2020 per NTRS file name) | yes | 10 LM challenges, 74 reqs | TA (FRET team) | — |
| V1-24 | Greenman: "in four rounds … 15–24 % … 28–47 %" | corrected (rounds) | A (Programming 2023) | yes | R1 90 students; R3 29 researchers | none | Figures come from rounds 2–4; round 1 generated the misconceptions |
| V1-25 + V2-08 | Req2LTL 88.4 vs 65.2 / 56.3 / 55.4 / 43.8; 13/112 fixed in ~10 min; "'Correct' is inconsistently defined" | V1-25 figures confirmed; V2-08 definition **corrected** | A (ASE 2025) | yes | 112 industrial aerospace reqs; GPT-4o (DeepSeek-V3 86.6 %) | TA | **Agree.** 88.4 % = two experts agree on semantic equivalence to gold; string match only on academic sets; no automatic equivalence checker; 13/112 is outside the headline numbers |
| V1-26 | Ricca IWPSE 2007: n = 15, p = 7.5e-05, no significant time cost | confirmed | A-workshop | yes | 15 master students, 6 reqs | none | Authors still say Fit "tend to involve additional effort" (p = 0.45) |
| V1-27 | Alloy4Fun: 25.4 % correct, 45.3 % faulty, 23.28 % both | confirmed | A | yes | 93,283 submissions | none | — |
| V1-28 | nl2spec: 15 of 20 fixed, 1.86 loops; 31/36; ≥9/36 ambiguous | confirmed | A (CAV 2023) | yes | 36 instances from 5 experts; Codex | TA | Fixes made by the authors |
| V1-29 | Lahiri FMCAD 2024: 64/153; 0.66 threshold; 25 vs 125; 400-line script | confirmed | A | yes | MBPP-DFY 153 specs | none | — |
| V1-30 + V2-14 | FormalAlign: 79.58 % vs 65.00 %; LLM judge 26–51 % P at 88–95 % R; 3 h per 80 pairs; grade "A per T1; venue not verified" | V1-30 figures confirmed (qualifier); V2-14 grade **corrected** → A | **A** (ICLR 2025 poster) | yes | FormL4, MiniF2F; 21 synthetic negatives per positive | TA | **Agree.** The negative ratio depresses precision |
| V1-31 | Beyond Compilation: 91.5 %; 1.3–29.5 pts; §2.5 "only 4 of 54 rejections (7%) were real errors" | 91.5 % and 1.3–29.5 confirmed; 4/54 **corrected** | A-pre | yes | 227 statements, 8 systems; audit sample n = 59 | TA | 91.5 % on 59 (95 % CI 81.6–96.3); "4 of 54" is a two-stage LLM review's classification, not a human one |
| V1-45 | [§3 qualification] Clover: agreement among legs sharing a reading ≠ faithfulness (source: Roundtrip) | confirmed (valid qualification; source replaced) | A-pre / A | yes | — | TA (Clover authors on own limit) | Better source: Clover App. A.4.1 |

## §2.2 T2 Conflicts and satisfiability

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-01 | Bosch: "ca. 310 results … 100 major issues, although … reviewed manually" | confirmed | A (RE 2019) | yes | 10 Bosch device sets | TA (+ Bosch co-author) | Remaining results "await classification" |
| V5-02 | Bosch: "Ten device sets of 50–701 requirements" | corrected | A | yes | Table II | TA | 26–701 (error from the T2 notes) |
| V5-03 | Bosch: "Nearly 70% of findings led to requirement fixes" | confirmed | A | yes | — | TA | Add "(including questions, typos, duplications, type issues)" |
| V5-04 | Bosch Dev. 8: 263 reqs, 6 vacuous, 73 rt-inc., 18 timeouts, 3h58m | confirmed | A | yes | Dev. 8 | TA | — |
| V5-05 | Bosch cost "1m33s–4h14m per full run" | corrected | A | yes | Table II | TA | 48 s – 4h14m |
| V5-06 | Bosch "Minutes to formalise a change; no result reuse" | confirmed | A | yes | — | TA | Add: initial formalisation "requires substantial effort" (ca. 5,000 observables) |
| V5-07 | SAT-LLM (A-pre): P 0.85 / R 0.31 vs P 1.00 / R 0.83 | corrected (grade) | **A** (ASE 2024, short; track unverified) | yes | 55 reqs, 15 conflict subsets, GPT-4 | TA (own method, own expanded dataset) | Dataset expanded by the authors with 10 composite-conflict reqs, where the advantage is largest |
| V5-08 + V2-16 | DMN: 160 ms–18.3 s; 200 ms–30.7 s; 812 vs 23,115 "naive algorithm"; grade A-pre | figures confirmed; comparator and grade **corrected** | **A** (BPM 2016, LNCS) | yes (arXiv version) | 9 synthetic tables, ~500–1,500 rules | TA | **Conflict on grade**: V5 A-pre (venue not checked) vs V2 A (Crossref). → A. Comparator = Signavio's checker. Figures verified against the arXiv submitted version only |
| V2-15 | PROPAS at Scania (A, venue unverified): all injected faults detected | confirmed + venue verified | A (ACM SIGAPP ACR 17(4), extends SAC'17) | yes | 1 industrial system; number of injected faults not stated | TA (+ Scania co-author) | — |
| V5-09 | FRET compositional: 1524.82 s → <7 s; unknown; 12 h; "3 of 12 collapsed via mode variables" | confirmed (nuance) | A (FM 2021) | yes | 12 benchmarks | TA | Mode variables are one contributing reason, not the only one |
| V5-10 | Spectra: 227 student GR(1) specs, 40 unrealizable | confirmed (nuance) | A (ICSE 2021) | yes | revision histories of 10 robot projects | TA | — |
| V5-11 | Well-separation: "only 19 of 79 student specs … in 60 the system could win by forcing" | corrected | A (FSE 2016) | yes (figshare) | 79 valid revisions of 6 undergraduate projects | TA | 40 of 79 under the strict semantics the students' tool used (derived as 60 − 20) |
| V5-13 | Frama-C smoke tests: 2,350 tests, ≈8 % overhead; WP axiom bugs | confirmed (strength caveat) | A (TAP 2024) | yes | JCVM, EAL7 | TA (CEA + Thales) | 37 JCVM smoke tests failed, all spurious dead-code alarms: evidence of cost, not of detection yield |
| V5-14 | ReForm: 52.2 / 44.3 / 3.5 % of 115 failures | confirmed | A-pre | yes | 115 failure cases | TA | — |
| V3-09 | Kupferman–Vardi quoting Beer 1997: "typically 20% of specifications pass vacuously" | confirmed (context corrected) | A venue; figure = practitioner experience | yes (FMSD 2001); no (CAV 1997) | IBM hardware verification, no n | TA (RuleBase authors) | FMSD wording: "20% of formulas … trivially valid"; plus ~10 % of non-vacuous passes reveal a problem via an interesting witness |
| V5-15 + V1-46 | [§3 qualification] Vericoding "found Dafny clean … roughly 9% of the [Verus] specs too weak … 15% poor translations" | **corrected** (both) | A-pre | yes | 5 random successes per language × source | TA (benchmark authors) | **Agree**: the figure is pooled "Across Dafny, Verus and Lean". Dafny "no issues" refers to LLM cheating. The qualification stands and also covers Dafny. The V2 notes kept the old "Verus" wording without re-reading → overruled |
| V2-19 (+ V1-46) | AlgoVeri: "some Vericoding Dafny/Verus specs accept 'simply returning 0'" (A-pre, read via grep) | corrected (scope + grade) | **A** (ICML 2026 spotlight) | yes (32 pp) | 1 problem (LIS) × 2 languages | **CB** | **Agree** with V1 on the CB flag. One worked example, no count |
| V5-16 (+ V4-12) | Watt CPP 2018: "originally unsound", "which had survived engines and the reference interpreter" | **corrected** (V5); "originally unsound" confirmed (V4-12) | A | yes | Isabelle mechanisation | none | **Agree.** Drop the "survived engines" clause (it originates in the T2 notes) or label it *Inference* |
| V5-17 | Wasm phase 4 "two or more Web VMs"; RFC 6410 "at least two independent interoperating implementations" | confirmed | B | yes | process docs | none | — |
| V5-18 | "MutDafny found 3 of its 5 weak specs in an LLM-generated set" | corrected | A-pre | yes (v1, v2) | 24 files, 284 survivors | TA | 4 of 5 were in LLM-generated programs; 1 of those 4 was new |
| V5-57 | "No source measures the defect yield per additional implementation. 'Two' is a convention." | confirmed (absence within sources read) | — | yes | W3C, RFC, phases, Watt | — | — |

## §2.3.1 Spec-enforcing tests

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-19 | MongoDB MBTCG: 4,913 tests, 86/86 branches vs 18 and 79; "faithfully been transcribed" | confirmed | A (PVLDB 2020) | yes | 1 kLOC merge function | V | — |
| V5-20 | MBTCG cost "1 engineer, 4 weeks" | confirmed | A | yes | — | V | — |
| V5-22 | Mocket: "9 bugs … including 2 in the official Raft TLA+ spec"; 134–152 LOC | corrected (wording) | A (EuroSys '23) | yes | 3 Java systems | TA | 7 implementation bugs (3 new, 4 known) + 2 spec bugs |
| V5-23 | Remix: 6 severe bugs; "unsound … only check safety"; ≤40 person-hours | confirmed | A (EuroSys '25) | yes | ZooKeeper | TA | — |
| V4-03 | DTest: "NFM 2023 paper [unreachable]; author page (B) … Statement/path coverage of the contract" | corrected | **A** (NFM 2023) | yes | 2 Dafny projects (1,382 + 4,596 LOC), 436 methods, 918 tests; C# only | TA (Tufts/AWS/BYU) | Coverage of the *implementation*; postconditions become runtime oracles; half of the tests have no return-value check |
| V4-04 | DTest "Agents: None found" | confirmed | A | yes | as V4-03 | TA | — |
| V4-05 | (new) DSpec2Test, spec-driven `dafny generate-tests` mode | confirmed (new supporting source) | A-pre (DOI venue unverified) | yes | 17 DafnyBench programs, 131 killable mutants | TA | 93.9 % vs 82.4 %; union 95.4 %; 17 unique kills by spec mode |
| V5-30 | Vikram et al.: n = 40 API methods; 2.4 samples; 21 % coverage | confirmed | A-pre | yes | 40 Python API methods | TA (own metric) | — |
| V2-01 | PBT-Bench: 100 problems, 365 bugs, recall 42.1–83.4 %; "stops after exposing a single bug" | corrected (scope) | A-pre (NeurIPS 2026 E&D claimed by authors) | yes (27 pp) | 100 problems, 40 libraries, 365 injected bugs; 8 LLMs × 2 prompts × 3 runs | none | Stopping is one model under the open-ended prompt; one whole-spec instruction adds +41.5 pp |
| V2-02 | "The measured agent weak spot is coverage of the spec (21 %; stopping after one bug)" | corrected (qualify) | A-pre | yes | as V2-01 | none | See V2-01 |
| V5-31 | Agentic PBT: 56 % of n = 50 valid; $9.93 per valid bug | confirmed (strength caveat) | A-workshop (NeurIPS 2025 DL4Code) | yes | 100 Python packages | **V** (vendor-affiliated; Hypothesis maintainer) | Sample from the top 80 % by LLM score; κ = 0.31; $9.93 is an upper bound |
| V1-07 | Porcupine "1,000x–10,000x faster" than Knossos, self-reported | confirmed | B | yes | own `test_data/jepsen/` | TA | — |
| V1-05 | "[§3 challenge] Porcupine cost. OmniLink is the first independent comparison" | corrected → downgraded to **qualification** | A-pre | yes | BAT only; 5 threads, 500–450k ops; 1–50 threads; 10 traces per length | **CB** | OmniLink's authors build competing TLA+ checkers |
| V1-06 | OmniLink "found 2 unknown bugs in WiredTiger/BAT/ConcurrentQueue" | corrected | A-pre | yes | 3 systems | CB | 1 in BAT, 1 in ConcurrentQueue |
| V1-08 | (brief §2.2) neutral Porcupine benchmark | not found | A-pre (Pine) | yes (Pine, 1504.00204, 2410.04581) | — | Pine builds on Porcupine | Pine matches Porcupine's speed; Horn & Kroening do not benchmark Knossos |

## §2.3.2 Conformance between layers

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-27 | Cedar: Lean 1,673 vs Rust 15,693; 21 + 4 bugs; 6 h/day on 4 vCPU; DRT missed non-termination | confirmed | A (FSE Companion 2024) | yes | Cedar | V | Agrees with V1-04 on the counts |
| V5-28 | Cedar: "35.5% … cut to 9.7% with a new generator" | corrected (nuance) | A | yes | Cedar DRT | V | 9.7 % is from an *added* expression generator |
| V5-29 | Cedar string-size failure led to dropping a feature | confirmed | A | yes | — | V | — |
| V1-01 | "[§3 challenge] Cedar's model layer … Lean, not Dafny" | **refuted** (misreading of the brief by the earlier run) | A (FSE); B (README) | yes | n/a | V | Earlier brief §3 names no language for Cedar; §3 status becomes **confirmed** |
| V1-02 | (premise) Dafny earlier in Cedar's history | confirmed (official repo docs only) | B | yes (READMEs, both papers) | n/a | V | cedar-spec release/2.0.x–3.0.x READMEs: "the Dafny formalization of Cedar"; the papers have 0 Dafny mentions |
| V5-24 + V2-17 | Cirstea: "in all cases"; "too imprecise logs …"; grade A-pre | quotes confirmed; grade **corrected** | **A** (SEFM 2024, LNCS) | yes | 6 case studies | TA (TLC maintainers) | **Conflict on grade**: V5 A-pre (not checked) vs V2 A (Crossref). → A |
| V5-25 + V2-18 | CCF: 6 bugs; ~2 engineer-months; ~1 engineer-week; DFS <1 s vs ~1 h; grade A/A-pre | figures confirmed; grade **corrected** | **A** (NSDI 2025) | yes | CCF, 63 kLoC | V (Microsoft) | **Conflict on grade** resolved → A. V5: the 2 months included building TLC support |
| V5-26 | TraceLink: 9 bugs; fixes "did not change the outcome of model checking" | confirmed | A (OOPSLA 2025) | yes | dqueue, locksvc, raftkvs | TA | — |
| V5-21 | MongoDB MBTC: 2 engineers, 10 weeks, abandoned | confirmed | A | yes | MongoDB Server | V | — |
| V2-04 | SysMoBench (A-pre): conformance 80–100 % spinlock, ≤15.38 % Etcd Raft; mapping found correct | corrected (scope + grade) | **A** (ICLR 2026) | yes (Table 3 rendered) | 11 artefacts; Table 3 = 2 artefacts × 2 agents × 4 LLMs | TA (own mapping component) | On Etcd Raft only one LLM reached conformance scoring: 7.69 % and 15.38 % (≈1/13 and 2/13 actions, *Inference*) |

## §2.3.3 Expectation tests

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-32 | Leveson 1990: spec-only checks 19 %; 4 of 34 effective checks (12 %) | confirmed (strength caveat) | A | yes | 24 graduate students | none | Authors: "inappropriate (and even misleading)" to rank check types; spec-only checks came first (order confound). Supersedes V1-52 for this item |
| V5-33 + V1-51 | Zhao ISSTA 2026: 3.84 vs 0.46 %; 2.98 vs 8.51 %; 104.15 → 186.77 | confirmed (both) | A (PACMSE 3) | yes | 318 focal methods, 233 defects, 13 LLMs | none | **Agree.** V1: the mitigating docstring was itself LLM-generated |
| V5-34 | Konstantinou: 43.02 → 35.72 % | confirmed | A-pre | yes | 24 Java repos | none | — |
| V5-35 | Mathews & Nagappan: pass-only filtering discards bug-revealing tests | confirmed | A-pre | yes | 287 buggy Python programs | none | Note different denominators in the notes |
| V5-36 | TiCoder: n = 15; +45.97 % pass@1 with idealised proxy | confirmed | A (TSE 2024) | yes | 15 programmers | TA (Microsoft) | — |

## §2.3.4 Oracles for non-commitment

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-37 | Wasm `either`, NaN patterns; relaxed SIMD fixed projection | confirmed | B | yes | official docs | none | — |
| V5-38 | sqllogictest `rowsort`/`valuesort`, `skipif`/`onlyif` | confirmed | B | yes | docs mirror | none | — |
| V5-39 | JSON Schema `optional/` | confirmed | B | yes | README | none | It "currently conflates many reasons" |
| V5-40 | POSIX 1003.3 UNSUPPORTED / UNRESOLVED | confirmed | B | yes | LTP HOWTO | none | — |
| V5-41 | NonDex: 60 open-source + 110 student bugs | confirmed (second-hand) | A-workshop | yes | Java library underdetermined specs | TA | Reported from the authors' ICST 2016 paper |
| V5-42 | PatchDiff: 29.6 %, 27.3 %, +6.4 pts | confirmed | A (ICSE 2026) | yes | 3 agents, SWE-bench Verified | TA (judging third-party agents) | — |

## §2.4 T4 Adequacy and traceability

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-54 | OFT `ORPHANED`/`OUTDATED`/`AMBIGUOUS`, quiet mode; Doorstop suspect links, "exits 1 on failure" | confirmed (exit code unverifiable here) | B | yes (docs/source) | tool docs | none | Doorstop exit code is not in `validation.md` |
| V2-12 | Mäder & Egyed: 71 subjects, 24 % faster, 50 % more correct (abstract only) | **unverifiable** (EMSE closed) | A | no; 2-pp author summary read | 71 subjects, 461 tasks, 2 Java systems, solutions sketched on paper | none known | Figures consistent with the authors' SE 2016 summary; statistics unverified; a search extract says 52 subjects (unresolved) |
| V5-43 | LiSSA best F1 ~0.25–0.53 | confirmed (nuance) | A (ICSE 2025) | yes | 5 benchmarks, GPT-4o | TA | Not better than the best IR baseline everywhere (eTour .548) |
| V5-44 | IronSpec: 10 spec bugs in 6 systems; 13 of 61 intended; 3 s–191 min | confirmed | A (OSDI 2024) | yes | 14 specs | TA | — |
| V5-45 | MutDafny: 794 programs, 112,810 mutants; 284 / 77 / 157 / 50; 5 weak specs | confirmed for v1; corrected for v2 | A-pre | yes (v1, v2) | 794 Dafny programs | TA | v2: 118,458 mutants, 30,459 survivors, mean 82 % |
| V5-46 | Alloy mutation: 10.96 % (17.72 %) reproduce; 91.78 % (95.79 %) detect | confirmed | A (FormaliSE 2025) | yes | 25,180 faulty novice models | TA (partial: μAlloy co-author) | Supersedes V1-52 for this item |
| V2-06 | TLA+-Bench: of 30 passes, 18 testable, 5 survived invariant→TRUE; 1.7 % vs 10.0 %; "wording needs re-checking" | numbers confirmed; interpretation **corrected** | A-pre | yes (17 pp) | 300 outputs, 3 models × 100 specs | TA (benchmark authors) | As worded ("survives when the mutated run still fails") the probe cannot show the invariant constrains behaviour (*Inference*). **Conflict with the V3 notes**, which used "5 of 18" as measured vacuity evidence without re-reading → V2 chosen. Supersedes V1-52 |
| V2-07 | §5 item 8 "probe wording needs re-checking"; §2.4 agents "vacuity of LLM TLA+ (mostly vacuous)" | corrected | A-pre | yes | as V2-06 | TA | No reliable TLA+ vacuity rate exists; the "substantive" screen keeps 12 of 30 passes |
| V5-47 | Google: ~15 M mutants, 6 years, coupling, more tests | confirmed | A (ICSE-SEIP 2021) | yes | Google code review | V | — |
| V5-48 | Wang TOSEM 2025: 76.47 % vs 44.15 % | confirmed | A | yes | 851 real Java bugs | none | — |
| V5-49 | Meta ACH: 9,095 mutants, 571 tests, "73% accepted"; P 0.79 / R 0.47 | corrected (nuance) | A (FSE Companion 2025, per notes) | yes | 10,795 Kotlin classes | V + TA | 73 % of the tests that engineers reviewed in test-a-thons |
| V5-50 | Just et al.: 73 % of 357 coupled; 17 % none | confirmed | A (FSE 2014) | yes | 5 Java programs | TA (partial: Major author) | Supersedes V1-52 for this item |
| V5-51 | Chekam: strong mutation highest fault revelation | confirmed | A (ICSE 2017) | yes | CoREBench | none | — |
| V3-01 | "Correlation is weak once suite size is controlled (Papadakis 2018, [unreachable])" | confirmed | A (ICSE 2018) | yes | 9 programs; 68 CoREBench + 231 Defects4J faults; 10,000 suites per size group | none | ~0.05–0.20 controlled vs 0.35–0.75 uncontrolled. Supersedes V1-52 |
| V3-03 | *Inference* "mutation as a hole finder, not a numeric target"; notes "mutation-guided suites beat random" | confirmed (report); notes paraphrase corrected | A | yes | as V3-01 | none | Suites were *ranked*, not generated: top 10 %/25 % beat equal-size random by 11 %/8 % (Defects4J), 46 %/18 % (CoREBench) |
| V5-52 | Hughes: validity props miss 5/8; 8.4 vs 50 tests; 79.2 % | confirmed | A (TFP 2019) | yes | 1 BST, 8 bugs | TA (QuickCheck author) | — |
| V5-53 | Goldstein: mutation 7/30, examples 8/30, coverage 2/30 | confirmed | A (ICSE 2024) | yes | 30 interviews, one firm | none | — |
| V4-06 | "AWS's ordering (CACM 2025) is [unreachable]" | **unverifiable** (article still [unreachable]; status confirmed) | B (FMCAD 2025 talk abstract) | no (article); yes (1-pp abstract) | — | V | Abstract lists practices, no figures, no ordering |

## §2.5 T5 Independence

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V1-13 | Kim: 0.423 (0.127), 0.60 (0.33); judges inflate same-provider answers | confirmed | A | yes | as V1-12 | none | — |
| V1-32 | Huang ICLR 2024: CommonSenseQA 75.8 → 41.8 | confirmed | A | yes | GPT-3.5 | none | — |
| V1-33 | Kamoi TACL: works with reliable external feedback | confirmed | A (TACL 2024) | yes | survey | none | — |
| V1-34 | Panickssery NeurIPS 2024 | confirmed (venue via Semantic Scholar) | A | yes | — | none | — |
| V1-35 | CodeJudgeBench: order swap up to 14 % | confirmed (figure) | A-pre (ACL 2026 per S2, unconfirmed) | yes | 26 judges | none | — |
| V1-36 | Jin & Chen (A-pre): over-rejection; explanations worsen it | confirmed; grade **corrected** | **A** (ASE journal 33, 2026) | yes | >700 tasks | none | — |
| V1-37 | Broccia: n = 34; LLM support lowered accuracy | confirmed | A-pre | yes | 34 participants, crossover | none | Students acting as novice inspectors |
| V1-38 | Smit ICML 2024; Choi (A-pre) majority voting explains most gain | Smit confirmed; Choi grade **corrected** | A / **A** (NeurIPS 2025) | yes | debate benchmarks | none | — |
| V1-39 | McAleese: critic beats paid reviewers; teams hallucinate less | confirmed | A-pre | yes | code review tasks | **V** (OpenAI on CriticGPT) | — |
| V1-40 | MathAtlas: judges lose accuracy out of domain | confirmed | A-pre | yes | 200 MA-Align items | TA (benchmark authors) | — |
| V1-41 | Arm 2017: property set "written from the NL manual"; 12 bugs (2 security); restating rules rejected | bug count confirmed; property source **corrected** | A (OOPSLA 2017) | yes | Arm v8-M spec | V (Arm research on own method) | Properties came from the NL manual, recent bugs and discussion with architects; low-level restating rules were "not very useful" and "prone to common-mode failure" |
| V1-42 | JEST: 27 spec bugs, 44 engine bugs | confirmed | A (ICSE 2021) | yes | ES11, 4 engines | TA | — |
| V3-05 (+ V1-52) | "Knight & Leveson 1986 is [unreachable], and its figures were not re-checked" | **unverifiable** (journal text); core claim confirmed via author report | B (NASA report) | no (paper); yes (NTRS 19870002808) | 27 student versions, 10^6 tests each, 45 faults | none | Unrelated faults triggered by the same special inputs; 3-version systems still ~10× fewer failures. KTH summary figures (D) not to be cited |

## §2.6 Disconfirming searches

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V1-47 | (a) Czepa: n = 215, PSP > EPL > LTL; no prose arm | confirmed | A (EMSE) | yes | 215 students | none | — |
| V1-48 | (a) Mavridou et al.: "significantly improved" without data; `optional` vs `weak` | confirmed | A-pre | yes | — | TA (FRET) | — |
| V4-19 | (a) "Snook & Harrison and Finney are [unreachable]" | confirmed (abstracts only) | A (if confirmed) | no | Finney n not given | — | Finney abstract: trained students "performed very poorly" |
| V2-10 (+ V1-52) | (b) Gay et al.: "up to 40.6% fewer … first pages only" | **corrected** | A (TSE 41(8), 2015) | yes (17 pp) | 7 systems, 4 criteria, 2 oracles; mutants (+10 real faults in 2 systems) | TA (partial: own OMC/DC) | Tables show up to −59.2 % (DWM 1, decision); the gap is on 4 Rockwell systems only; NASA/pump systems and OMC/DC matched or beat random |
| V1-49 | (b) Inozemtseva & Holmes: low-to-moderate correlation, size controlled | confirmed | A (ICSE 2014) | yes | Java projects | none | — |
| V3-02 | (b) "Mutation-score correlation is weak once size is controlled (Papadakis 2018, [unreachable])" | confirmed | A | yes | as V3-01 | none | Drop [unreachable]; top-scoring suites still find more faults for 138/231 and 59/68 faults |
| V1-03 | (c) "Cedar goes design → Lean model → Rust … (A-pre)" | corrected (grade) | **A** (FSE Companion 2024; OOPSLA 2024) | yes | n/a | V | Agrees with V5-27 grade |
| V1-04 | (c) "Those projects found real spec bugs (… Cedar about two dozen)" | corrected | A | yes | Cedar: 25 bugs | V | 4 by proofs (validator) + 21 by DRT/PBT in production code: implementation-vs-model, not spec-vs-intent. Counts agree with V5-27 |
| V1-43 | (c) SpecTec: all applicable Wasm 2.0 tests; 10 bugs in 5 proposals | confirmed | A (PLDI 2024) | yes | Wasm 2.0 + 5 proposals | TA | — |
| V1-44 | (c) Arm ASL FMCAD 2016: >11,000 tests; "architects' intent" | confirmed | A | yes | Arm v8-A/M | V | — |
| V1-50 | (c) GitHub Spec Kit: self-review checklists, no data | confirmed | D/B | yes | — | V (vendor doc) | — |

## §2.7 Baseline points (cross-reference)

V1-01 (Cedar, refuted), V1-05 (Porcupine, qualification), V1-45 (Clover, valid qualification) and V5-15 + V1-46 (Vericoding, valid qualification, corrected attribution) are logged above in §2.1, §2.2, §2.3.1 and §2.3.2. No other baseline point was challenged by any verifier. V3, V4 and V5 each quote the relevant §3 lines and state that their findings contradict no baseline point.

## §3 Check map

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-12 | Termination row "(60/79 GR(1) specs failed this)" | corrected | A | yes | as V5-11 | TA | "60 of 79 revisions of six student projects; 40 under strict realizability" |

## §4 Candidate pipelines

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V5-55 | Pipeline B "Bosch reported roughly 70/30" | confirmed (caveat) | A | yes | Bosch | TA | Tool-author self-report, ongoing case study, part unclassified |
| V5-56 | Pipeline B "Bosch: 18 timeouts; FRET 'unknown' on non-linear arithmetic" | confirmed | A | yes | Bosch Dev. 8; FRET | TA | — |

## §5 Open questions and verification debt

| ID | Debt row (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V1-52 | Gay; Papadakis; Just 17 %; Alloy 11/92 %; TLA+ 5/18; Leveson 19 %; Großer; Knight & Leveson | unverifiable by V1 (not re-read) | as earlier | no | — | — | Superseded by V2-10, V3-01/02, V5-50, V5-46, V2-06, V5-32, V3-05; Großer stays abstract only |
| V2-09 | "Req2LTL's definition of 'correct' … internally inconsistent" | corrected | A | yes | — | TA | Resolved: two metrics on two datasets |
| V2-05 | "SysMoBench Table 3 … parsed from text extraction"; §6 "A-pre" | corrected | **A** | yes | — | — | Table 3 confirmed from a rendered page |
| V2-11 | "Gay et al. TSE 2015 … first pages only" | corrected | A | yes | — | — | Full preprint read; TSE 41(8):803–819 |
| V2-13 | "Mäder & Egyed EMSE 2015 … abstract only" | corrected (minor) | A | no | — | — | EMSE [unreachable] (closed); SE 2016 author summary read |
| V3-06 | Eckhardt & Lee [unreachable] | **unverifiable** (TSE); content via NASA TM 86369 | B | yes (TM); no (TSE) | analytical model | none | Independence iff constant "intensity of coincident errors", judged "unlikely to hold"; high intensity can make N-version worse than one version |
| V3-07 | Littlewood & Miller [unreachable] | **unverifiable** | A venue; abstract only | no | analytical model | none | Abstract: diverse methodologies decrease simultaneous failure |
| V3-10 | Heitmeyer TOSEM 1996 [unreachable] | confirmed (now full text) | A | yes | 1 spec (A-7 OFP); 36 condition tables / 98 rows; 3 mode tables / 700 rows | TA | 17 real Coverage errors; 57 Disjointness findings ("a few probably are not"); 245 s; errors two review teams missed |
| V3-11 | Selby, Basili, Baker TSE 1987 [unreachable]; T3b notes: Cleanroom as independence evidence | corrected (notes); report body unaffected | A | partial (6 of 11 pp, scanned) | 15 student teams (10/5), non-randomised | none (tester was an author) | Both arms had the same independent testing, so it is no evidence for independent test families |
| V3-12 | (Selby figures, if cited) | confirmed (strength qualification) | A | partial | as V3-11 | none | Completeness 82.5 vs 60.0 (p = .088); tests 92.5 vs 80.8 % (p = .055) |
| V4-01 | "NASA IV&V ROI data … not retrieved" | confirmed (gap stands) | B (Neal et al.); C (Hunt slides) | yes; VT 1998 abstract only | Shuttle DoLILU: 100 DITRs, 695 IV&V-found errors | TA (partial: NASA/WVU IV&V staff) | ROI 1.5–12 is model-based; no study isolates independent derivation |
| V4-02 | Dabney ROI papers | unverifiable | — | no | — | — | Bibliographic records only |
| V4-07 | Katis CAV 2022 [unreachable] | confirmed (now full text) | A | yes | 3 case studies | TA (FRET team) | FRET found 8 minimal unrealizable cores; the published G1–G7 attribution "does not really exist" |
| V4-08 | Leino & Wüstholz CAV 2015 [unreachable] | confirmed | A | yes | 8 expert Dafny IDE sessions | TA | Caching: 4,395.3 s → 315.3 s → 277.5 s (session 0); fine-grained 17 % faster on average |
| V4-09 | Whalen ISSTA 2006 + follow-up (UFC) [unreachable] | corrected | A-pre (Staats et al. report); ISSTA A [unreachable] | yes (follow-up) | 4 avionics systems, 600 mutants each | TA (own metrics) | Requirements and antecedent coverage suites lost to equal-size random (significant); UFC beat random in 3 of 4 |
| V4-10 | Huo & Clause FSE 2014 [unreachable] | confirmed (via dissertation) | A-pre (dissertation) | yes (diss. Ch. 3) | 20 Java apps, 4,718 executable tests | TA | 164 brittle-assertion tests, 1,618 unused-input tests; "TP" = survived automated filter |
| V4-11 | Watt & Rao FM 2021 (notes: would be dual-formalisation evidence) | **refuted** (the notes' expectation) | A | yes | Wasm 1.0; ~17,810 tests | none | Two mechanisations, no cross-comparison, no discrepancies reported |
| V4-12 | (Watt CPP 2018 "originally unsound") | confirmed | A | yes (FM 2021) | — | none | Merged with V5-16 in §2.2 |
| V4-13 | Mashkoor & Jacquot REJ 2017 [unreachable] | confirmed (now full text; no quantitative data) | A (HAL submitted version) | yes | 3 Event-B case studies | TA | Qualitative evaluation; animation found platoon oscillation |
| V4-14 | Melnik et al. Agile 2006 [unreachable] | unverifiable (2006); replacement read | A-workshop (XP 2007) | yes (2007) | 1 project, 3 interviewees | none | FIT writing surfaced "missing pieces or inconsistencies in a story" |
| V4-15 | Ricca ICSE 2008 / IST 2009 | unverifiable | — | no | — | — | Effort disagreement unresolved |
| V4-16 | Black, Okun, Yesha; Ammann & Black | unverifiable | — | no | — | — | TLS / 403 |
| V4-17 | van Lamsweerde et al. TSE 1998; Zave & Jackson; Saarland fb14-96-06 | unverifiable | — | no | — | — | — |
| V4-18 | Hughes AUTOSAR, Dropbox, "Experiences" | unverifiable | — | no | — | — | — |
| V4-20 | DO-178C | unverifiable (not attempted) | — | no | — | — | Paywalled; out of time |

## §6 Sources

| ID | Claim (abbreviated) | Verdict | Grade | FT | n and setting | Indep. | Merge / note |
|---|---|---|---|---|---|---|---|
| V2-03 | "PBT-Bench … A-pre \| yes (abstract, setup)"; T3a notes "Agents: human-only evidence" | corrected | A-pre (acceptance claimed) | yes (full) | — | none | Agents were measured |
