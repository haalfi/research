# Spec faithfulness prior-art check

A verification run on nine leads (L1–L9) that another tool produced. Each lead is checked against its full text for what it shows and for whether it changes a recommendation on this branch or in the record-quality report. Inputs:
- the notes in `research_notes/Spec faithfulness prior-art check/`: P1 (L1, L8), P2 (L2, L3, L6), P3 (L4, L5, L7, L9);
- this branch's reports, cited as [S] summary, [DD] deep dive, [V] verified edition and [TD] trial design;
- the record-quality report `Observation record completeness and consistency.md` (branch `research/observation-record-quality`, read-only copy, read with the maintainer's permission), cited as [ORQ §x].

Every quotation of old text below was checked against the report file itself, not against the notes.

**Labels.**
- Grades: A, A-pre, A-workshop, B, C, D.
- FT = full text read.
- TA = the authors evaluate their own tool.
- Transfer: *direct* = library or API behaviour specs; *analogous* = other spec domains; *inference*.
- *Inference* marks this run's own reasoning.

---

## 1. Kernsatz

**No recommendation changes.** Two texts that report search results need qualifying, and neither qualification is a recommendation change:
- [V §2.6(c)]'s list of nearest pipelines gains Lim et al. (FM 2026, a human A ≡ R gate that stops at the formal model) and ARSENAL (no gate against the prose).
- [V §5] Q3's "All measurements are maths/Lean" is no longer strictly true, because claimcheck adds a Dafny slice. Judge precision against human labels on API specs is still unmeasured.

C-GRiD (L1) is the only lead that turns verifier counterexamples into questions for a stakeholder, but it does not measure that step. Both of its oracles are simulated from the ground truth. On a code reading of its pre-acceptance replication package, the questions do not affect the reported recall. So [ORQ §5] Q5 ("Class 4 discovery is unmeasured") stands.

---

## 2. One row per lead

### 2a. Citation, grade, measured result, agents, transfer

| # | Corrected citation | Grade; FT | Measured result (n; setting; what "correct" meant; baseline; TA) | Agents (LLMs) | Transfer |
|---|---|---|---|---|---|
| **L1** | O. Tibermacine, C. Tibermacine, "Neuro-symbolic Requirements Elicitation: Utilizing Formal Verification Counterexamples as Contextual Prompts", *ASE 2026*, pp. 613–623, DOI 10.1145/3832783.3834379 ([Crossref](https://api.crossref.org/works/10.1145/3832783.3834379); [HAL PDF](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)). The lead's title is truncated; the "paper 49" URL returned 404. The paper is listed in the [research-track program](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | **A**; FT y (HAL author copy; the ACM PDF returned 403). Replication package ([Zenodo 10.5281/zenodo.19222714](https://zenodo.org/api/records/19222714)) partly read: code inspected, not run | **Setting.** 10 TLA+ specs from the literature. Controlled constraint removal: 1–3 constraints deleted per configuration, 20 configurations, one run per oracle. **"Correct".** "Constraint recovery recall" = the share of *removed formal constraints* that reappear. The authors state they "do not measure the recovery of unstated informal stakeholder requirements" nor the NL → TLA+ translation. **Results.** 79.2 % recall with a perfect oracle, 70.8 % with a noisy one (75 % correct / 15 % ambiguous / 10 % mutated). The authors call the noise model "a stress test of the loop's error-recovery mechanism rather than … a model of human behaviour"; the abstract's phrase "realistic interaction settings" contradicts that. Only 2 of 20 runs per oracle ended in a clean verification. **Baselines.** On a 6-spec subset: Gen-Once 2.8 %, Auto-Repair 0.0 %, against C-GRiD 65.3 %. **TA**: yes | Per the paper, llama-3.3-70b synthesises the initial model V0, refines it and writes fallback questions. Per the archived code, the reported C-GRiD runs use **no LLM** (see the qualification below). The only LLM result is the Gen-Once baseline, at 2.8 % | *Analogous* (TLA+ transition systems). The question step has no measured result to transfer |
| **L2** | M. Amster, O. An, H. Baker, F. Graciolli, S. Henniger, N. Amin, "claimcheck: Measuring and Improving Specification Faithfulness", arXiv 2610.17358v1, Oct 2026. PDF footer: NeurIPS 2026 Workshop on AI for Verifiable Coding ([arXiv](https://arxiv.org/abs/2610.17358)) | **A-workshop** (acceptance self-reported); FT y | **Setting.** 3,234 rows: Dafny 362 (CloverBench, 62 textbook programs; docstring = requirement), and PutnamBench theorem statements in Lean 1,296, Isabelle 920 and Rocq 656. **"Correct".** Labels come from how each row was built: Clover mutation classes, Dafny- or Lean-proved control rewrites, and semantic mutation rules. **No human intent labels.** **Results.** Two blind steps (informalise without seeing the requirement, then judge without seeing the artifact) reach macro recall of **87.9–93.1**, against 79.6–84.0 for a direct single-call judge and 83.0–88.9 for that call given the same rewrite list. In ablations, letting the informaliser see the requirement costs 0.8–3.0 points, and letting the judge see the artifact costs 1.4–4.5. All 182 defective Dafny rows still verify. **Precision against humans is not reported.** **TA**: yes | Both steps are done by LLMs (claude-haiku-4.5, then claude-sonnet-4.6). The gain is "substitutive rather than additive" across models | *Analogous*: single pure-function contracts, no state, no environment, no non-commitments |
| **L3** | Z. Lim, B. Wu, Y. S. Teo, S.-W. Lin, Y. Li, "Shift-Left Requirements Verification: Integrating LLMs and Formal Methods for Automotive Systems", *FM 2026*, LNCS 16557, pp. 631–650, DOI 10.1007/978-3-032-26220-2_31 ([Crossref](https://api.crossref.org/works/10.1007/978-3-032-26220-2_31); [Springer PDF](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)) | **A**; FT y (20-page chapter plus the authors' 72-page appendix from the [supplementary site](https://sites.google.com/view/shift-left-requirement-supp)) | **Setting.** Three proprietary automotive cases (23, 56 and 83 requirements), one model (Claude 4.5 Sonnet) with FDR4, five runs each. **RQ1 (M ⊨ A synthesis success)**: 5/5, 4/5, 2/5. **RQ2 (A ≡ R)**: CS1 only, 23 assertions, three expert reviewers; **the expert verdicts are the label**. The main text gives 14/5/4 (approve/minor/major) and calls confidence scores strongly correlated with correctness, without a test. The appendix's per-assertion Table 7 gives 8/9/6, its §J.3 and §J.4 give yet other counts, and only 10 of 23 verdicts were unanimous. **RQ3**: 29 defect-derived properties, 23 failed and were "confirmed" by experts; 1/1 known defect found. **Cost**: 10–35 min, $1.80–7.80, under 1 h of expert time per project. **TA**: yes, with two industry co-authors | LLMs do the formalisation and the CEGAR repair (40–100 % success). The A ≡ R step is human, aided by an LLM back-translation that **sees the requirement** (appendix prompt L.6) | *Analogous* (reactive CSP models) |
| **L4** | Misu, Lopes, Ma, Li (UC Irvine), Lahiri (Microsoft Research), "Spec-Harness: Assessing and Guiding LLM-Synthesized Formal Specifications Beyond Verifiability", arXiv 2604.00280**v3**, Oct 2026. v1 (Mar 2026) was titled "VeriAct: Beyond Verifiability …" and had three authors ([abs](https://arxiv.org/abs/2604.00280); [v3 PDF](https://arxiv.org/pdf/2604.00280v3)) | **A-pre**; FT y (v1 and v3) | **"Correct and complete"** is measured against the **implementation**: test pairs come from "a known-correct execution of P", and completeness = rejecting output mutants. **Results.** Of 14,936 verified JML specs, 35.6 % reach Post-Harness@0.75. The harness agreed with blind human adequacy ratings on **67 of 100** specs. In the v3 agent loop, scored on a feedback suite that shares no pair with the evaluation suite, gains are +3 to +16 points, significant for Codex on both benchmarks and Claude Code on one. **VeriAct's own gains are not significant** (p = 0.18–0.45), and verification rates fall. v1's +5 / +12 % had no stated separation between feedback and scoring pairs. **TA**: yes; Lahiri (FMCAD 2024, already cited on the branch) is a co-author | LLM agents write the specs; verifier and harness check them | *Analogous*, close to direct for the mechanism (method contracts) |
| **L5** | F.-C. Chang et al. (NTU, MediaTek), "SpecLoop: An Agentic RTL-to-Specification Framework with Formal Verification Feedback Loop", arXiv 2603.02895v1, Mar 2026 ([PDF](https://arxiv.org/pdf/2603.02895)) | **A-pre**; FT y | **Loop.** RTL → NL spec → RTL rebuilt from the spec alone → Yosys EQY equivalence (SAT, depth 10) against the **original RTL**. **"Correct"** = a strong model rebuilds RTL from the spec that passes the existing testbenches (the RR score), i.e. checked against the code, not intent. **Setting and results.** Six models, three runs each; task counts not given. Full counterexample diagnosis ranks first in 9 of 12 settings, against 4 for pass/fail only, often within one std. EQY-passing specs reached RR = 1 in 81.3–91 % of cases, unverified ones in 34.6–45.2 %. **TA**: yes | LLMs write the spec, rebuild the RTL and diagnose failures | *Analogous* (hardware; code → prose direction) |
| **L6** | S. Nair, A. Vempaty, J. Liu, A. Jagmohan, "Beyond Type-checking: Towards Holistic Evaluation of Formal Specification Generation", arXiv 2610.10604v1, Oct 2026; arXiv comment: accepted at the NeurIPS 2026 Workshop on AI for Verifiable Coding ([arXiv](https://arxiv.org/abs/2610.10604)) | **A-workshop** (acceptance self-reported); FT y | **Setting.** 350 Lean tasks (VERINA 189, CLEVER 161), four spec-generation configurations on GPT-5.6. **"Bidirectional implication"** = BEq+: Lean proof search for candidate ⊢ reference and reference ⊢ candidate against **the dataset's reference spec**; failure counts as inconclusive. **Results.** BEq+ succeeded at 0.000–0.021 on VERINA and 0.000 on CLEVER. 76.1 % of behavioural non-passes carried harness errors. The authors: "Reference agreement and finite tests do not establish fidelity to the natural-language requirement." **TA**: for their own evaluation framework | An LLM generates the specs; the equivalence step is proof search | *Analogous* (Lean, pure functions) |
| **L7** | S. Ghosh, D. Elenius, W. Li, P. Lincoln, N. Shankar, W. Steiner, "ARSENAL: Automatic Requirements Specification Extraction from Natural Language", *NFM 2016*, LNCS, pp. 41–46, DOI 10.1007/978-3-319-40648-0_4. Extended version arXiv 1403.3142v3 (2016); earlier DTIC report ADA611691 (2014) ([arXiv v3](https://arxiv.org/pdf/1403.3142); [Crossref DTIC](https://api.crossref.org/works/10.21236/ada611691)) | NFM: **A**, venue verified, not read. arXiv v3: **A-pre**, FT y. DTIC: **B, [unreachable]** | **Pipeline.** Rule-based NLP → LTL → LTL satisfiability → SAL model checking → GR(1) realizability with counterstrategy-guided assumption mining → synthesis. **NLP accuracy.** F = 0.63 on 188 held-out sentences. "Correct" = partial-credit sub-formula matches to **one gold formula** (typed Levenshtein distance); the annotators are not stated. **Case studies**: two, n = 1 each, qualitative; the model is checked against a theorem that ARSENAL itself translated from NL (M ⊨ A). **TA**: yes | **None** (2014–2016 rule-based pipeline) | *Analogous* (avionics, medical, Ethernet FSMs) |
| **L8** | L. C. Cordeiro, "Formal Verification of LLM-Generated Code", invited talk, FATTW 2026 (co-located with ASE 2026), 30 slides ([slides](https://ssvlab.github.io/lucasccordeiro/talks/fattw2026_slides.pdf)). Underlying papers: Tihanyi et al., *AST 2025* (ESBMC-AI) ([PDF](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf)); Wang, Farrell, Cordeiro, Zhao, *RE 2025* (SpecVerify) ([arXiv 2507.04857](https://arxiv.org/pdf/2507.04857)) | Slides **C**, FT y. ESBMC-AI **A**, FT y (two-column extraction). SpecVerify **A**, FT partial | **No source has a counterexample-versus-error-message ablation.** ESBMC-AI compares verifier output (violation, line, stack trace and counterexample together) with **no** verifier output: "approximately 31 − 37%" against "80% to 90%" accuracy on C vulnerability repair; the n for the unassisted condition was not found. SpecVerify replays counterexamples by the authors, to adjudicate verdicts. The slides' "18 fixes merged upstream" were made by human maintainers, with no comparison condition. **TA**: yes | ESBMC-AI: GPT-4o patches. SpecVerify: Claude 3.5 Sonnet and GPT-4o write assertions. Neither isolates feedback format | *Analogous* at most; the claim itself is *inference* only |
| **L9** | `danielrosehill/Spec-Standard-Research`, `docs/prior-art-survey.md` ([raw](https://raw.githubusercontent.com/danielrosehill/Spec-Standard-Research/main/docs/prior-art-survey.md)); `ashbrener/spec-kit-atlas`, `README.md` and `examples/generated/RESULT.md` ([raw README](https://raw.githubusercontent.com/ashbrener/spec-kit-atlas/main/README.md); [raw RESULT](https://raw.githubusercontent.com/ashbrener/spec-kit-atlas/main/examples/generated/RESULT.md)) | **D** both; FT y | **Survey.** "Two-stage pipeline … then deterministic code", which the survey itself labels "reported". Its only faithfulness-relevant primary source is OnionL, which **is Req2LTL** ([arXiv 2512.17334](https://arxiv.org/abs/2512.17334)), already verified on this branch. SLOT ([arXiv 2505.04016](https://arxiv.org/abs/2505.04016), A-pre, abstract only) measures schema conformance. **Atlas.** The "fail-closed faithfulness gate" **cites no primary source**. It checks that provenance resolves (presence), not entailment. Its one self-reported run includes "Codex cross-model review … Ran five rounds … VERDICT: faithful (0/0/0)". n = 1 | Atlas: agents extract; the gate is deterministic. Nothing measured | *Inference* |

**C-GRiD replication package: required qualification.** The following findings come from **reading the code, not running it, in a pre-acceptance package**. Zenodo holds one version, dated 2026-03-25; the paper was accepted 2026-06-18.
- **The oracle returns the removed constraint verbatim.** The `GroundTruthOracle` used for the `cgrd` runs returns the removed ground-truth `Constraint` object ("Return actual GT!") and uses the question text only to choose an option index. `core/spec_refiner.py` appends that constraint verbatim.
- **No LLM takes part in the C-GRiD runs.** The runner passes no LLM to them, and `core/question_gen.py` imports none. An LLM generator is used only by the Gen-Once baseline.
- **The noisy oracle is the same oracle plus a random roll.**
- The archived `results.csv` reproduces 79.2 % and 70.8 % exactly.
- *Inference*: in the archived implementation, recall counts how many TLC counterexamples occur before the removed constraints run out. Question wording cannot affect it.
- An unarchived LLM-based variant cannot be excluded, but no evidence of one was found ([Zenodo](https://zenodo.org/api/records/19222714)).

### 2b. Delta per lead (old text quoted verbatim from the report file)

| # | Delta | Old text (verbatim) and verdict |
|---|---|---|
| **L1** | **Confirms the form, adds no evidence** | [V §2.1]: "*Inference*: ask humans yes / no / "not addressed" questions on one concrete case tied to one record sentence. Route to them (a) unresolved difference witnesses, (b) every "not addressed" answer from the added-commitment probe, and (c) a random audit of agent-judged witnesses." **No change.** C-GRiD is a published *design* precedent for one concrete-case yes/no question per counterexample, but the question step is unmeasured, so this stays *Inference*. C-GRiD's polarity design (allowed → relax, disallowed → add) has no "not addressed" answer. **Also no change** to [ORQ §5] Q5 (see §4) or to [DD §4] new question 4: "False-alarm rate of invariant-relative one-step checks (unreachable counterexample states) on realistic specs." C-GRiD reports no spurious-counterexample rate |
| **L2** | **Qualifies an open-question text; confirms R3 and R4 in direction** | [V §5] Q3: "3. What is the precision of LLM faithfulness judges on API or behaviour specs? All measurements are maths/Lean; the correlation data are MCQ." **Text qualification**: claimcheck adds a Dafny program-contract slice. The question stays open: there is no precision against human labels, and nothing on API specs. [V Part 3] R3: "Added-commitment probe judged spec-blind; every "not addressed" goes to a human \| inference + analogous (NeuroSTAR) \| low". R4: "Cross-family judges must agree to accept; human on rejection; calibrate and recalibrate on model change \| analogous (maths/Lean judges; MCQ correlation) \| low–medium". **Confirmed in direction, confidence unchanged.** claimcheck's blinding ablations are measured support for keeping a judge blind to what anchors it (R3's spec-blindness). Its model sweep supports "recalibrate on model change" (R4). It tests no cross-family rule. It is TA, workshop-level, construction-labelled and mostly maths |
| **L3** | **Qualifies a search-result text; no change to recommendations** | [V §2.6(c)]: "**(c) Is there a published pipeline doing prose → spec → model → reference model with faithfulness gates?** *Result: none found by the earlier run's search* (a search result, not proof of absence)". **Stands** for the full chain to a reference model. **Text qualification**: add Lim et al. to the nearest pipelines (prose → assertions → CSP model, a human A ≡ R gate, no R layer). In the same section, "Agents are measured in none of the closely fitting pipelines." becomes true only of *faithfulness*: Lim et al. measure agents on synthesis success (M ⊨ A). **No change** to Pipeline A ([DD §3.3]); see §4(c) for the comparison |
| **L4** | **Confirms; adds a qualifier for harness-scored loops** | [V §2.1] row: "Lahiri, FMCAD 2024 (A): 64 of 153 MBPP-DFY specs analysable. Soundness = admits reference output; completeness = rejects mutated outputs". **Confirmed** by a larger Java replication that shares an author, so it is not independent. [V Part 3] R19: "Spec-strength mutation (G9) \| analogous (IronSpec, single source) \| medium–low". **Supported, confidence unchanged**: the source is not independent and anchors on code, not prose. *Inference*: v1 → v3 shows that an agent loop optimising a harness score must be scored on a suite it never saw. This already matches the branch's information-flow design (held-out wheats in [TD]) |
| **L5** | **Confirms** | [V §2.1]: "Round-trip and dual formalization catch *divergent* readings. By construction they miss *shared* misreadings". SpecLoop catches divergence only relative to its anchor, which is code. [V §4] Pipeline C step 3: "G2 diffs the generated prose against the records clause by clause (SpecTec-style back-generation used as a round-trip check)." SpecLoop measures the *source → prose → source* half, not the prose-versus-records diff. **No change.** It does not trigger R-D3-4's overturn condition, "Round-trip diffs alone catching as many seeded misreadings as an independent property set", because no seeded misreadings were used |
| **L6** | **Confirms** | [V §2.1]: "From weakest to strongest metric (*Inference*): syntax valid < exact match < equivalence to one gold < human intent judgement < detection of real errors." **No change.** L6's authors place reference equivalence below intent themselves. New detail: BEq+ to gold succeeded in ≤ 2.1 % of tasks, so "inconclusive" dominates |
| **L7** | **Qualifies a search-result text; confirms P-B's failure mode** | [V §2.6(c)], quoted under L3: **stands**. ARSENAL is end-to-end but has no gate against the prose. **Text qualification**: list it next to "**FRET** leaves prose → FRETish to the human." [S §3] Pipeline B: "The translation is itself a faithfulness step." Illustrated by F = 0.63 for a 2014 rule-based translator. [V Part 3] R7: "rt-consistency / realizability with environment actions, plus well-separation (G4) \| inference by analogy (FRET, GR(1)); no library application \| low". One more qualitative GR(1) case (n = 1, TA); **no change** |
| **L8** | **No change** | No recommendation rests on counterexample-versus-message feedback to agents. Nearest is the [V §3] check-map cell "added-commitment probe via failing Dafny assertion or Hypothesis-shrunk case shown with the source sentence (Cunha & Macedo; Lahiri)". It is neither confirmed nor overturned |
| **L9** | **Confirms existing texts; no change** | [V §2.6(a)]: "Measured benefit comes from decomposition plus deterministic translation (Req2LTL)". The survey's claim leads back to this same source. [DD §5.1] D5-R4: "Require decision/scenario citations; reject uncited or unknown-ID assertions; a valid citation is not evidence of no added commitment". The atlas gate is exactly the first half, with no evidence. Its strength is that of [S §2] G1, "Dangling or orphan links. Presence only, not binding", and of R16's "low for G1 catching added commitments" |

**Two flagged readings, settled.**
- **L3's "five-round cross-model review … 'faithful' as a gated verdict" is not in the FM 2026 paper.** P2 searched the 20-page chapter and the 72-page appendix:
  - "five" occurs only as "Each case study is run five times for consistency";
  - "faithful" occurs once, in the A ≡ R sentence;
  - every experiment uses one model.
  The wording does occur in spec-kit-atlas `RESULT.md` ("Codex cross-model review … Ran five rounds … VERDICT: faithful (0/0/0)"). The lead therefore attaches L9's D-grade example output to L3's citation. That the absence is real rests on the full text. *How* the other tool conflated the two is *Inference*. Residual caveat: the appendix read is the authors' version, not checked against Springer's ESM.
- **"Held-back judge gates" (brief §1 Q2).** No branch report contains the phrase: a search of all five reports for "held back", "held-back" and "withheld" found nothing. This run adopts P2's reading as the best available mapping: the judge gates whose trust is withheld until calibration. That covers R3, R4, the [V §2.5] *Inference* ("the gate is calibrated on a human-labelled sample and recalibrated when the generating models change"), [DD §3.3] Pipeline A step 5 ("added-commitment probes to a spec-blind judge"), and [S §5] Q8 / [TD §2.4] calibration. **The verdict does not depend on the mapping.** No lead reports judge precision against human labels on any specification, so no judge gate under any reading gains confidence.

---

## 3. Changed recommendations

**None.** No recommendation's text, confidence or overturn condition changes.

**Text qualifications of search results and open questions.** These are not recommendation changes; they leave the earlier reports untouched and apply from this report on.

| Location | Old text (verbatim) | Qualified text | Reason |
|---|---|---|---|
| [V §2.6(c)], nearest pipelines | "**FRET** leaves prose → FRETish to the human." | Add: "**Lim et al.** (FM 2026, A; TA) run prose → CSP assertions → model, with an LLM CEGAR repair loop (M ⊨ A) and a **human** expert A ≡ R gate per requirement–assertion pair, then freeze the approved assertions. No reference-model layer. The A ≡ R step is measured only as expert outcome counts on 23 assertions, inconsistently reported. **ARSENAL** (NFM 2016, A; arXiv v3 A-pre; TA) automates prose → LTL → SAL with satisfiability, model checking and GR(1) realizability gates, and leaves faithfulness to the user." | L3 and L7 full texts |
| [V §2.6(c)] | "Agents are measured in none of the closely fitting pipelines." | "Agents are measured for faithfulness in none of the closely fitting pipelines. Lim et al. measure agent synthesis success (M ⊨ A) only." | L3 RQ1 |
| [V §5] Q3 | "All measurements are maths/Lean; the correlation data are MCQ." | "All measurements are maths/Lean or single textbook Dafny contracts (claimcheck, A-workshop, TA, construction labels, recall only); none reports precision against human labels on API or behaviour specs; the correlation data are MCQ." | L2 |

**Candidate additions (*Inference*, not adopted).** None is measured, so none meets the branch's bar for a recommendation.
- **(i) Assertion freeze.** Once a clause or formal assertion passes G2 and human review, agents repairing a model may not edit it, and any edit re-enters G2. Lim et al. name "assertion weakening" as the risk of a CEGAR loop and freeze assertions, without measuring the effect.
- **(ii) A blind-informalisation arm in [TD]'s judge calibration**: informalise without the record, then compare. Motivated by claimcheck's ablations.
- **(iii) Held-out scoring for harness-optimising agent loops.** Motivated by Spec-Harness v1 → v3.

---

## 4. Answers to brief §1 and the §5 disconfirming checks

### §1 Q1: is there a measured method that turns verifier counterexamples into questions for the decision-maker?

**No.** C-GRiD does exactly this by design: TLC counterexamples go through four fixed templates (MissingGuard, RaceCondition, Deadlock, LogicError fallback), and each becomes a yes/no question about one concrete case ([HAL PDF §3.5](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)). Its evaluation does not measure the question step:
- no human took part, and both oracles read the ground truth;
- on the code reading qualified in §2a, the questions cannot affect the score;
- the authors defer "controlled user studies" to future work.

Even a measured C-GRiD would not reach [ORQ §5] Q5, verbatim: "**Class 4 discovery is unmeasured.** No technique for finding questions no checklist raises has a surviving measurement. Caller-use reading and STPA guide-words are proposals." By the authors' own account, "a missing requirement that refers to a domain variable not present in the current state space cannot produce a counterexample and will never be surfaced". *Inference*: that is the same blind spot [ORQ §2 T1] gives for slot grids, "slots the template lacks (class 4)". C-GRiD's nearest counterpart in the record-quality design is the [ORQ §3] obstacle test per decision, not class 4 discovery.

The other near misses are weaker still:
- Lim et al.'s RQ3 gap reports turn FDR4 counterexamples into stakeholder decisions (accept, mitigate, reject, defer), but they are generated from a historical-defect database (an external checklist) and only expert-confirmed (23/23, 1/1 known defect) ([FM 2026 §3.3, §4.4](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf)).
- ARSENAL's assumption mining asks the user to accept or reject candidate assumptions in one qualitative case ([arXiv v3 §3.3](https://arxiv.org/pdf/1403.3142)).
- SpecLoop and Spec-Harness feed counterexamples to LLMs, not humans.

**[ORQ §5] Q5 is unchanged, and so is [ORQ §4]'s stopping rule.** It still covers class 4 "only by the caller-use reader". [ORQ §5] Q4 (fidelity judges on design dialogs) is also unchanged: no lead tests dialogs.

### §1 Q2: is there a measured A ≡ R check of a formal artifact against its NL source?

**Partly, and only from L2.** claimcheck is the one measured automated A ≡ R check. Macro recall is 87.9–93.1 against 79.6–84.0 for a direct judge, but only against construction labels, and with no precision against human labels ([arXiv 2610.17358](https://arxiv.org/pdf/2610.17358v1)). *Inference*: on the Dafny slice, the implied precision of a "disputed" verdict is about 0.92 against construction labels at ~50 % prevalence. That figure is own arithmetic and is not comparable with FormalAlign's 26–51 % at 21 negatives per positive.

The other leads do not measure A ≡ R:
- Lim et al. state the M ⊨ A / A ≡ R split verbatim and gate A ≡ R by humans, but measure only expert outcomes on 23 assertions.
- L6 is gold agreement.
- L4 and L5 check against code.
- L7 checks partial-credit similarity to one gold formula.

**Bearing on the judge gates (R3, R4, [S §5] Q8).** Direction confirmed, confidence unchanged. The deciding measurement is still [TD]'s calibration on human-labelled API-spec verdicts (30 "violation" + 30 "fine" per judge role).

### §1 Q3: does any lead show a published end-to-end pipeline with faithfulness gates against the prose?

**Not through to a reference model.** Lim et al. are the nearest: a published prose → formal-model pipeline with a **human** A ≡ R gate against the prose. ARSENAL is end-to-end with no such gate. SpecLoop runs in the reverse direction (code → prose → code), gated against code. The spec-kit-atlas gate is a presence check with n = 1. [V §2.6(c)] **stands**, qualified as in §3.

### §5(a): do L2, L3 or L6 measure faithfulness against intent?

**None does.**

| Lead | What it actually measures |
|---|---|
| L2 | Agreement with **construction labels**: a gold original plus mutation rules and proved-equivalent rewrites. The authors concede that the semantic labels "rest on the rule that produced them" |
| L3 | **Expert judgement only.** The three reviewers' verdicts are the label, with no gold, no seeded errors and inconsistent counts, so the gate's miss rate cannot be computed |
| L6 | Agreement with a **gold reference spec**, explicitly "not … fidelity to the natural-language requirement" |

### §5(b): does L1's recall survive a realistic stakeholder?

**Not tested.** Both oracles are simulated and read the ground truth. The noisy oracle changed little: all ten k = 3 rows are identical across oracles. The authors list "the oracle assumption" as the main construct-validity threat.

**Does question generation depend on a correct initial model?** **Yes, in the evaluation.** V0 is the correct ground-truth model minus 1–3 constraints, and NL → TLA+ translation is excluded. The authors call this "the most important gap in this evaluation". By design, discovery also depends on the model's variables and the depth bound k = 15. In 2 of 20 runs the reduced spec already satisfied Φ, so no question was raised and recall was 0 %. The design's answer for a wrong initial model, "symmetric resolution", rests on one illustrative episode ([HAL PDF §3.6, §4, §5.2.1](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf)).

### §5(c): is L3 or L7 a published pipeline with a faithfulness gate against the prose?

- **L3: partly yes.** It has a human gate and no reference-model layer.
- **L7: no.** It is a pipeline, but it has no gate against the prose.

Comparison with Pipeline A as given in [DD §3.3] and [V §4] (*Inference*):

| Concern | Pipeline A | Lim et al. (L3) | ARSENAL (L7) |
|---|---|---|---|
| Independent prose-derived check, before the formal artifact | Step 2: record-derived check set, in a fresh records-only session under a file-system read scope, before the spec | None. Back-translation sees requirement *and* assertion. claimcheck measured that setting as worse (−0.8 to −3.0 macro recall) | None |
| Faithfulness gate against prose | G2: record checks run against each clause, plus added-commitment probes to a spec-blind judge | Human Approve/Modify/Reject per requirement–assertion pair, aided by back-translation and an LLM confidence score | None at run time. Offline F = 0.63 against gold formulas |
| Screening of the checks themselves | ≥ 2 wheats plus chaffs (G2 a–c, D1-R1, D1-R3) | None | None |
| Lineage separation | Separate lineages; spec-blind judge | One model for translation, repair, back-translation and confidence; independence comes only from the human reviewers | No LLM; one deterministic rule chain |
| Consistency, realizability | G3, G4, G4a/G4b | FDR4 refinement (M ⊨ A) | LTL satisfiability (≈ G4), GR(1) realizability with assumption mining (≈ G4d, R7) |
| Vacuity before trusting passes | G5 | None | None |
| Guard against agents weakening assertions | Not named for the formal core; G2 keeps record checks fixed | **Approved assertions frozen; only model refinement allowed afterwards** | n/a |
| Reference model and conformance | R built; G6–G8 | Stops at the formal model | Stops at the model (Verilog synthesis optional) |
| Measurement | Not run (trial designed) | Synthesis success 40–100 %; A ≡ R as expert counts on 23 assertions | F = 0.63, n = 188; two n = 1 case studies |

**Net.** Neither challenges Pipeline A's structure. Lim et al. contribute one design element Pipeline A lacks: the freeze, candidate (i) in §3. ARSENAL resembles Pipeline B's front half, without B's dual slot-filling and diff.

---

## 5. Verification debt

**C-GRiD (L1)**
- The oracle and no-LLM findings rest on a static reading of a pre-acceptance package. TLC and Groq were unavailable, so nothing was run. Confirm by running the package or by asking the authors.
- `MetricsCalculator.semantic_match` (the "strict semantic matching") was not read.
- The ASE "paper 49" URL is unresolved; existence is confirmed via Crossref, HAL and the program listing.

**Workshop acceptance (L2, L6).** Self-reported in the PDF footer and the arXiv comment; not checked on OpenReview or the workshop site.

**Lim et al. (L3)**
- The appendix read is the authors' Google Drive version, not compared with Springer's ESM.
- The 14/5/4 vs 8/9/6 inconsistency is reported as read and has not been raised with the authors.
- Whether the reviewers were independent of the authors is not stated.

**claimcheck (L2)**
- The repository was not inspected (per-class confusion matrices, an earlier SQL slice).
- The ≈ 0.92 precision figure is own arithmetic and ignores up to 12 unanswered rows.

**Nair et al. (L6).** Whether the VERINA and CLEVER references are human-written was not verified.

**Spec-Harness (L4).** v2 was not read; only v1 and v3 were compared. The v1 → v3 contrast compares different populations.

**SpecLoop (L5).** Task counts are absent from the paper. The 9-vs-4 ranking was not recomputed from Table III.

**ARSENAL (L7)**
- The DTIC report is **[unreachable]**.
- The NFM 2016 paper was venue-verified but not read.
- arXiv v1 and v2 were not compared with v3.
- The gold-formula annotators are not stated.

**L8**
- The n, model and protocol behind ESBMC-AI's "31–37 %" were not located in the extracted text.
- SpecVerify was read partially.
- The FATTW workshop page was not fetched.

**L9.** SLOT was read as abstract only; the SoLM blog was not read. Neither bears on any recommendation.

**Unopened leads, out of scope.** Li, Dworkin & Seshia 2011 (counterstrategy-guided assumption mining, cited by ARSENAL) and ARTEMIS (ICSE 2026, distinguishing traces for stakeholder validation, cited by C-GRiD) are possible §1 Q1 and Q2 leads. They were not opened, per the brief's no-new-search rule.

**Reading of the brief.** The mapping of "held-back judge gates" in §2b is this run's reading. The verdict holds under any mapping.

---

## 6. Sources with grades

| Source | Grade | FT | Role | Flag |
|---|---|---|---|---|
| Tibermacine & Tibermacine, ASE 2026, [HAL](https://hal.science/hal-05794580/file/CGRiD_Paper_ASE26.pdf), [Crossref](https://api.crossref.org/works/10.1145/3832783.3834379) | A | y | L1 | TA |
| C-GRiD replication package, [Zenodo](https://zenodo.org/api/records/19222714) | — (artifact) | code read, not run; pre-acceptance | L1 | TA |
| Amster et al., claimcheck, [arXiv 2610.17358](https://arxiv.org/abs/2610.17358) | A-workshop (self-reported) | y | L2 | TA |
| Lim et al., FM 2026, [Springer](https://link.springer.com/content/pdf/10.1007/978-3-032-26220-2_31.pdf); [supplementary appendix](https://sites.google.com/view/shift-left-requirement-supp) | A | y (chapter + 72-page author appendix) | L3 | TA; industry co-authors |
| Misu, Lopes, Ma, Li, Lahiri, Spec-Harness (v1: VeriAct), [arXiv 2604.00280](https://arxiv.org/abs/2604.00280) | A-pre | y (v1, v3) | L4 | TA; shares author with Lahiri FMCAD 2024 |
| Chang et al., SpecLoop, [arXiv 2603.02895](https://arxiv.org/pdf/2603.02895) | A-pre | y | L5 | TA |
| Nair, Vempaty, Liu, Jagmohan, [arXiv 2610.10604](https://arxiv.org/abs/2610.10604) | A-workshop (self-reported) | y | L6 | TA (framework) |
| Ghosh et al., ARSENAL, NFM 2016, [Crossref](https://api.crossref.org/works/10.1007/978-3-319-40648-0_4) | A | n (venue verified) | L7 | TA |
| Ghosh et al., ARSENAL, [arXiv 1403.3142v3](https://arxiv.org/pdf/1403.3142) | A-pre | y | L7 | TA |
| Ghosh et al., DTIC ADA611691, [Crossref](https://api.crossref.org/works/10.21236/ada611691) | B | [unreachable] | L7 | TA |
| Cordeiro, FATTW 2026 slides, [PDF](https://ssvlab.github.io/lucasccordeiro/talks/fattw2026_slides.pdf) | C | y | L8 | own group's work |
| Tihanyi et al., ESBMC-AI, AST 2025, [PDF](https://ssvlab.github.io/lucasccordeiro/papers/ast2025.pdf) | A | y (extraction caveat) | L8 | TA |
| Wang, Farrell, Cordeiro, Zhao, SpecVerify, RE 2025, [arXiv 2507.04857](https://arxiv.org/pdf/2507.04857) | A | partial | L8 | TA |
| Rosehill, Spec-Standard-Research survey, [raw](https://raw.githubusercontent.com/danielrosehill/Spec-Standard-Research/main/docs/prior-art-survey.md) | D | y | L9 | — |
| ashbrener, spec-kit-atlas, [README](https://raw.githubusercontent.com/ashbrener/spec-kit-atlas/main/README.md), [RESULT](https://raw.githubusercontent.com/ashbrener/spec-kit-atlas/main/examples/generated/RESULT.md) | D | y | L9; source of L3's misattributed wording | TA, n = 1 |
| Ma et al., Req2LTL (OnionL), ASE 2025, [arXiv 2512.17334](https://arxiv.org/abs/2512.17334) | A | abstract here; full text earlier on this branch [V §2.1] | L9 resolution | TA |
| Wang et al., SLOT, [arXiv 2505.04016](https://arxiv.org/abs/2505.04016) | A-pre (venue unverified) | abstract only | L9 | — |
| [ORQ] Observation record completeness and consistency (other branch, read-only copy) | branch report | y (§2 T1, §3, §4, §5) | Q1 baseline | — |
