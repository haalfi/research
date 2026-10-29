# T1 Faithfulness: prose → spec, proved wrong early

Scope: how a formalization is validated against its natural-language (NL) source rather than against itself, and what carries over to an agent-driven pipeline (prose observation records → normative spec, formal models). Grades follow brief §6. "Full text" means I read the paper body myself (arXiv HTML/PDF, NTRS PDF, author PDF), not only an abstract. "[abstract only]" and "[unreachable]" mark weaker grounding. Items already settled in brief §3 (SpecGen, nl2postcond, Clover, ClarifyGPT, Vericoding/DafnyBench, "notation alone does not beat prose", SCR tables/EARS as method families) are not re-surveyed. Where new evidence qualifies one of them, it is flagged **[§3 qualification]**.

Agent-measurement legend: **AGENT-MEASURED** means LLMs/agents were measured doing the step. **HUMAN-ONLY** means only humans did the step.

---

## Q1. Back-translation / round-trip, independent dual formalization plus equivalence/difference checking, paraphrase review

### Takeaway
Round-trip and dual formalization catch *divergent* readings well. By construction they miss *shared* misreadings: if both directions or both formalizers make the same omission, the check passes, and every full-text source that discusses the point says so. Equivalence checkers are high-precision but low-recall (about 98% precision, 48% recall for Lean statements), so "not proven equivalent" says much less than "proven equivalent". The best measured variant pairs dual or multiple formalization with *difference witnesses*: concrete traces on which the candidates disagree, which a judge (human or LLM) then rejects against the prose.

### Cited Findings
**Round-trip (formal → NL → formal, equivalence check).** AGENT-MEASURED.
- Amrollahi, Lopez, Barrett, "Faithful Autoformalization via Roundtrip Verification and Repair", arXiv 2604.25031 v3 (Stanford). Grade **A-pre**, full text.
  - Setting: Texas statutes, 150 Transportation Code rules and 77 Parks & Wildlife rules, formalized into many-sorted FOL and checked with Z3.
  - Procedure: T1 formalize; T2 back-translate to NL; T3 re-formalize; Z3 checks y_orig ≡ y_rt. The authors treat equivalence as *necessary, not sufficient* for faithfulness.
  - Results: equivalence before repair was 44.7–67.1%. After a diagnose-and-repair loop (K=3) it was 78.9–85.7%, and 90.7%/94.7% when GPT generated and Claude diagnosed. Models: Claude Opus 4.6, GPT-5.2.
  - What "correct" meant: Z3 equivalence of the two encodings. Faithfulness was checked only post hoc, by (a) BART-MNLI drift between the source and the back-translation (non-equivalent rules showed 1.4×–2.5× more drift, pooled 1.78×) and (b) **one annotator on 25 rules**. That annotator found 1 minor error among the 14 equivalent rules and 3 among the 11 non-equivalent rules, none of them "unfaithful". Diagnosis agreed with the annotator on 7/11.
  - Stated blind spots: errors shared by both formalizations ("if T1 drops a conjunct and T3 reproduces the omission, the check passes"), and stable but wrong fixed points. 26 rules were never repaired (missing schema predicates, exception clauses, compound conditions).
  - Diagnosis collapse: GPT blamed stage T1 in 83–97% of iterations until the prompt was changed.
  - Cost: 7.2 LLM calls per repair (Full) vs 19.9 (Regenerate). No false-positive or false-negative rates are reported.
  - [Source](https://arxiv.org/abs/2604.25031)
- FormalRx (Wang et al., ICML 2026) argues that binary NL–FL verdicts hide where a translation fails. It proposes a 28-category hierarchical error taxonomy with localization and correction. The trained 8B diagnoser reports verdict F1 0.88, categorization F1 0.71, localization 0.75 and correction 0.73 on 56,287 annotated pairs (math domain). Grade **A** [abstract only: the page I could read gives no back-translation numbers]. [Source](https://arxiv.org/abs/2607.04655)

**Equivalence checking against a second (reference) formalization: precision vs recall.** AGENT-MEASURED (LLM formalizations, symbolic checker).
- Poiroux, Weiss, Kunčak, Bosselut, EMNLP 2025, "Reliable Evaluation and Benchmarks for Statement Autoformalization". Grade **A**, full text.
  - Data: ProofNetVerif, 3,752 Lean formal–informal pairs with human binary semantic-equivalence labels. "Correct" = semantically equivalent to the NL statement, as judged by manual annotation.
  - Instance-level agreement of the symbolic equivalence metric with human labels:
    - BEqL: precision 100.0, recall 30.9, F1 47.2.
    - BEq+: precision 98.0, recall 48.3, F1 64.7.
  - At benchmark level the metrics track aggregate accuracy well (BEq+ Kendall 0.872 over 65 model/method points). The type-check rate correlates poorly (Kendall 0.560) and "can not be used as a substitute for human evaluation".
  - [Source](https://arxiv.org/abs/2406.07222)
- FormalAlign (Lu et al., ICLR 2025): a learned NL↔Lean alignment scorer. Grade **A**, full text.
  - Negatives are *synthetic* rule-based mutations: constant change, exponent change, new variable, type change, = vs ≤ swap, random pairing.
  - Human experts matched ground truth 79.58% of the time, FormalAlign 65.00%, and an LLM-as-judge baseline was lowest.
  - Precision gap against GPT-4 as a judge: GPT-4 precision was 26–51% at 88–95% recall, i.e. the LLM judge over-accepts misaligned pairs.
  - Cost: 80 items took a human about 3 h and FormalAlign under 2 min.
  - [Source](https://arxiv.org/abs/2410.10135)

**Multiple independent formalizations with difference witnesses.** AGENT-MEASURED.
- NeuroSTAR (Saha, Woodlief, Elbaum, Dwyer), arXiv 2609.03161. Grade **A-pre**, full text.
  - Method: several LLM generators produce LTLf candidates. Each is compiled to a DFA, and difference automata yield **witness traces on which the candidates disagree**. An LLM judge panel (Kimi K2.5, majority vote) decides whether each trace should be kept or added, and the feedback drives refinement.
  - Benchmarks (equivalence to gold LTLf via Spot): ConfoNLf 87.8% vs 86.2% for n-shot prompting; strict variants 96.4% and 100%.
  - Reference-free driving-law study: 108 sections. The *shortest violating trace* of each generated formula was judged by two authors, with a third on disagreement. 89/106 (83.9%) were judged valid violations. The authors note this is **only a necessary condition**, because accepted traces are not checked.
  - Stated blind spot: convergence when all generators agree "even if they might be wrong together" is an unverified assumption. The dominant failure was a missing atomic-proposition vocabulary.
  - Data hygiene: they removed 31% of ConfoNL/SynthNL pairs as temporally ambiguous. *Inference*: public NL→LTL gold sets themselves contain unfaithful or ambiguous labels.
  - [Source](https://arxiv.org/abs/2609.03161)

**Independent dual human formalization.** HUMAN-ONLY.
- Easterbrook & Callahan, "Formal methods for V&V of partial specifications: an experience report", RE'97 (NASA/WVU IV&V, Space Station FDIR requirements). Grade **A** (older; full text via NTRS scan).
  - Four people independently translated one FDIR requirement into Leveson AND/OR tables and produced **four different answers**. The answers differed in the number of conditions (rows) and in the activating combinations.
  - The authors: it "would be difficult to discover that our four subjects had different interpretations … without asking them to re-write it". Comparing tables was "much easier" than comparing versions of the prose. The process "was remarkably good at identifying ambiguities".
  - They also report that "fidelity … between the informal and formal specifications is difficult to guarantee" and that IV&V analysis value "is entirely dependent on how faithful the formal model is".
  - n = 4 subjects, 1 requirement, no statistics.
  - [Source](https://ntrs.nasa.gov/api/citations/19970007163/downloads/19970007163.pdf)
- Saarland tech report fb14-96-06 on "complementary specification": two teams specified a lexical analyzer, and per the search extract both specifications contained conceptual errors, and comparison cannot catch shared errors. **[unreachable]**: 503 and a bot wall. [Source](https://jahrbib.sulb.uni-saarland.de/bitstream/20.500.11880/25859/1/fb14-96-06.pdf)
- Brilliant/Knight/Leveson N-version specification debugging: lead only, from a secondary mailing-list post. **[unreachable]**, grade D as cited. [Source](https://lists.techfak.uni-bielefeld.de/pipermail/systemsafety/2017-October/003454.html)

**Paraphrase review (formal → NL explanation read by a human).** HUMAN-ONLY, with partly LLM-generated input in Req2LTL.
- FRET's generated English and diagram explanations, plus its simulator, were "instrumental in ensuring that the FRETISH requirements captured our intended semantics" in the Lockheed Martin challenge case study (Mavridou et al., RE 2020). See Q4 for the concrete misreading caught. Grade **A** (case study), full text. [Source](https://ntrs.nasa.gov/citations/20205000433)
- Humans misread formal text when asked to paraphrase it (Greenman et al., Programming 2023, see Q4): 15–24% of LTL→English answers were wrong. Paraphrase review is therefore only as good as the reader's grasp of the notation. [Source](https://arxiv.org/abs/2211.01677)

### Inferences
- *Inference*: every round-trip or dual-formalization source flags the same weakness, so the main threat to faithfulness is a misreading shared across readers. That matches the brief's observed failure mode "decision text that went beyond what was actually asked". An agent pipeline that uses the same model or prompt lineage for both legs raises the risk of shared errors (see T5).
- *Inference*: use equivalence results asymmetrically. A proven equivalence between two independently produced formalizations is strong evidence of *agreement*, though not of faithfulness. A failed proof is weak evidence of disagreement (about 50% recall in Lean). The productive output is a *difference witness*, a concrete case on which the two disagree, because the case can be checked against the prose directly.
- **[§3 qualification]** Clover-style triangular cross-checks ("help") need the caveat that triangulation agreement does not establish faithfulness when the legs share a reading. The roundtrip paper's own human audit shows equivalence and faithfulness only loosely coupled (1/14 vs 3/11 minor errors, n = 25, single annotator).

### Gaps
- No controlled study measures recall of *shared* misreadings for round-trip or dual formalization against an independent gold. All evidence of the blind spot is argued or anecdotal.
- No measured study of human paraphrase review of an LLM-produced spec against its source, with seeded defects, was found.
- Kamsties et al. (2001) on ambiguities being under-reported during formalization: search extract only, **[unreachable]**.

---

## Q2. Controlled/structured requirement languages as an intermediate step (FRET/FRETish, EARS, Gherkin, decision tables)

### Takeaway
Structured intermediates have measured benefit mainly where the intermediate is *decomposed* and then *mechanically translated*, as in Req2LTL's LLM → tree IR → rule-based LTL step. Executable example tables (Fit) improved comprehension in a small experiment. Evidence that EARS or templates improve faithfulness to intent, as opposed to form quality, is thin. FRET practitioners report that rewriting NL into FRETish is not always straightforward.

### Cited Findings
- **Req2LTL** (ASE 2025; arXiv 2512.17334). Grade **A**, full text. AGENT-MEASURED.
  - Method: an LLM decomposes each requirement into a tree IR ("OnionL"), which deterministic rules translate to LTL. Machine validation checks arity, AP placement, field compatibility and legal scope nesting. Spot checks syntax.
  - Data: 112 industrial aerospace requirements (63% nested two or more levels deep). Gold formulas came from two independent annotators, expert discussion and senior-engineer review.
  - Industrial "exact match" (GPT-4o): 88.4% vs 65.2% for NL2TL, 56.3% for nl2spec, 55.4% for NL2LTL, 43.8% zero-shot. DeepSeek-V3: 86.6%.
  - On academic sets NL2TL ≈ Req2LTL (about 95–96%), so the gain is on complex industrial text.
  - What "correct" meant: the paper is internally inconsistent. One section says exact string match without normalization; another says two human experts judged each pair. **No equivalence checker** was used. Syntax validity of 100% follows from rule-based synthesis.
  - Errors eliminated by the IR: temporal misinterpretation, conditional confusion, loss of nesting, AP binding. Residual: ambiguity and context omission.
  - With an optional Mermaid visualization, engineers fixed **13 of 112** semantically wrong formulas in about 10 minutes (human-in-loop; not part of the headline numbers).
  - Confidential data; one domain; no variance reported.
  - [Source](https://arxiv.org/abs/2512.17334)
- **AeroReq2LTL** (arXiv 2604.21715, overlapping authors) uses a data dictionary and a template requirement language and reports 85% precision and 88% recall on aerospace requirements. **[abstract/search extract only]**, A-pre. [Source](https://arxiv.org/abs/2604.21715)
- **FRET / FRETish, Lockheed Martin challenges** (Mavridou et al., RE 2020). Grade **A** case study, full text. HUMAN-ONLY.
  - Coverage: 69 of 74 requirements captured; 2 were "unclear … even with the help of the domain expert".
  - Only 7 of FRET's 112 template keys were used; one key covered 75% of formalizations.
  - The authors: "Even though FRETISH is aimed at being intuitive, it was not always straightforward to turn natural language requirements into FRETISH".
  - Analysis exposed "requirement ambiguities, undefined parts in the models, and small bugs in the checkers". Some counterexamples "uncovered conflicting requirements" without needing the model.
  - [Source](https://ntrs.nasa.gov/citations/20205000433)
- **Executable example tables (Fit), as a supplement to prose.** HUMAN-ONLY.
  - Ricca, Torchiano, Ceccato, Tonella, "Talking Tests", IWPSE 2007. Grade **A-workshop**, full text.
    - Design: 15 master's students, 6 requirements, each requirement given with or without Fit tables.
    - Result: correctness of answers about requirements was significantly better with Fit tables (overall p = 7.5e-05; per-requirement Fisher p from 0.0069 to 0.04 on several items, one item reversed). The time difference was not significant (7'48" without vs similar with; p = 0.45).
    - [Source](https://profs.scienze.univr.it/ceccato/papers/2007/iwpse2007.pdf)
  - The 2009 IST journal follow-up (two experiments, Trento and Torino) reports that Fit "helps in the understanding of requirements without requiring a significant additional effort". Grade **A**, **[abstract only]**. [Source](https://profs.scienze.univr.it/ceccato/papers/2009/ist2009.html)
- **Requirement templates (EARS, Adv-EARS, Boilerplates, MASTeR, SPIDER)**: Großer, Rukavitsyna, Jürjens, REJ 2024. Grade **A**, **[abstract/search extract only; Springer behind login]**.
  - 1,764 requirements; all templates except SPIDER had positive effects on quality characteristics vs free text, with similar effect sizes.
  - A user experiment (n = 43) found templates need substantial training and domain knowledge.
  - The measured characteristics appear to be ISO 29148-style form qualities, not faithfulness to a source intent (*Inference* from the extract).
  - [Source](https://link.springer.com/article/10.1007/s00766-024-00427-0)
- **Tables as the comparison medium** (Easterbrook & Callahan RE'97, Q1): independent AND/OR-table rewrites made disagreements locatable row by row. [Source](https://ntrs.nasa.gov/api/citations/19970007163/downloads/19970007163.pdf)

**Disconfirming search (a): structured intermediates do not improve faithfulness over careful prose review.**
- Result: no study was found showing *no* improvement in faithfulness. Also no study was found that measures faithfulness (not form quality) of EARS, Gherkin or templates against careful prose review.
- The closest cautionary evidence:
  - FRET authors: translating into FRETISH "not always straightforward".
  - Großer et al.: templates require substantial training.
  - Greenman et al.: English→LTL authoring error rates of 28–47% even among experts (Q4).
  - Settled §3 item "notation alone does not beat prose" stands; nothing found contradicts it.
- Evidence for benefit comes from (i) decomposition plus deterministic translation (Req2LTL) and (ii) example tables (Fit), not from the notation itself.

### Inferences
- *Inference*: Req2LTL's gain plausibly comes from forcing explicit structure (scope, condition, timing, response as separate slots) that an LLM fills locally, followed by a non-LLM step. This maps onto the brief's axis-typed normative forms: each record decision → typed slot structure (case table rows, frame set, transition cells) → mechanical rendering into Dafny/TLA+/Alloy. The rendering step can then be checked syntactically, and the human or independent agent only reviews the slot values.
- *Inference*: Fit and Gherkin tables earn their value as *examples attached to prose*, which is what the records' scenarios already are. That supports treating scenarios as executable checks (Q5) more than adopting a new controlled language.

### Gaps
- No controlled evidence that EARS or Gherkin raise faithfulness to intent. Mavin et al. 2009 (EARS) is a single case study I did not re-read; EARS is §3-settled.
- Decision tables as intermediates: no new faithfulness measurement beyond §3 (SCR/ACSL completeness and disjointness).
- NL2CTL (ICFEM 2024): fine-tuned T5 reached 46.4% vs 2% few-shot on a synthetic LLM-generated dataset, per the search extract. **[unreachable full text]**. [Source](https://pure.ecnu.edu.cn/en/publications/nl2ctl-automatic-generation-offormal-requirements-specifications-/)

---

## Q3. LLM autoformalization of requirements/specs: what "correct" meant, and whether it reflects faithfulness to intent

### Takeaway
Most papers score against a gold formula made by the authors, either by syntactic or exact match (weak) or by automata/SMT equivalence (strong for the gold, but the gold is itself a human reading). Very few measure faithfulness to *intent* without a gold. Those that do use human judgement on small samples, test- or witness-based necessary conditions, or NLI proxies. Headline accuracies are therefore upper bounds on agreement with one reader, not on faithfulness.

### Cited Findings
Summary of systems, n, setting and the meaning of "correct" (all AGENT-MEASURED):

| System | n / setting | "Correct" meant | Faithfulness to intent? | Grade |
|---|---|---|---|---|
| nl2spec (Cosler et al., CAV 2023) | 36 one-sentence NL specs written by 5 experts to be hard; APs a–e | Matches the **expert's intended meaning**; no alternative reading of ambiguous input accepted (human judgement) | Closest to intent, but tiny n and authors judged | A |
| Req2LTL (ASE 2025) | 112 aerospace reqs plus academic sets | Exact match / two-expert agreement with a double-annotated gold (inconsistent) | Agreement with gold readers | A |
| NeuroSTAR (2026) | 4 public LTLf sets; 108 law sections | Spot equivalence to gold; reference-free: human-judged shortest violating trace | Witness check = **necessary only** | A-pre |
| Roundtrip/Barrett (2026) | 227 statutes | Z3 equivalence of formalize vs re-formalize | Self-consistency, not intent; 25-rule human audit | A-pre |
| Lahiri (FMCAD 2024) | MBPP-DFY, 153 problems with specs, 64 run | Spec holds on all I/O tests (soundness) plus fraction of output mutants rejected (completeness) | Tests as proxy for intent; human labels wrong/weak/strong | A |
| Poiroux et al. (EMNLP 2025) | ProofNet#, RLM25, ProofNetVerif 3,752 | Human semantic-equivalence labels; BEq+ as a proxy | Human judgement | A |
| FormalAlign (ICLR 2025) | FormL4, MiniF2F | Separation of gold vs synthetic mutants | Synthetic negatives only | A |
| Cunha & Macedo (2025/26) | 43 Alloy4Fun reqs, many wrong human specs | Do LLM-made tests from NL reject known-wrong specs? | Bug detection against real human errors | A-pre |
| NL2CTL (ICFEM 2024) | Synthetic LLM-made NL–CTL pairs | Accuracy vs synthetic gold | Weak | [unreachable] |

Details:
- **nl2spec** (full text). Grade **A**.
  - Results on the 36-instance expert set:
    - NL2LTL (rasa) 1/36 (2.7%); fine-tuned T5 2/36 (5.5%); nl2spec+Bloom 5/36 (13.8%).
    - nl2spec+Codex initial 16/36 (44.4%); with in-distribution prompt 21/36 (58.3%); **interactive sub-translation editing 31/36 (86.1%)** at 1.86 loops on average for the fixed ones (1.4 overall).
    - 5 instances had to be translated by hand.
  - At least 9/36 instances were ambiguous: operator precedence, e.g. "a holds until b holds or always a holds", and semantic ambiguity, e.g. "b must hold in the next two steps" read as X X b vs b ∨ X b. They were resolved by editing the visible sub-translation fragment.
  - Author-run interaction, not an independent user study of fixing.
  - [Source](https://arxiv.org/abs/2303.04864)
- **Lahiri, FMCAD 2024** (full text). Grade **A**.
  - Defects surfaced by symbolic testing of specs:
    - too-weak specs (==> where <==> was needed; upper bound only; non-negative count only);
    - a misread intent (RemoveDuplicates kept one copy instead of removing all duplicated items);
    - human-labelled "strong" specs failing because the *tests* had transcription errors (25 vs 125).
  - No overall agreement percentage is given. The method assumes a high-quality test suite.
  - [Source](https://arxiv.org/abs/2406.09757)
- **Coins** (Yang et al., arXiv 2608.13077): Rocq specs for HumanEval, scored by instantiating specs on trusted tests and discharging proof obligations. Argues that proof failure is "inherently ambiguous" and test-instantiated reasoning is "more faithful and discriminative". **A-pre, [abstract only]**. [Source](https://arxiv.org/abs/2608.13077)
- **Hahn et al.** (arXiv 2206.01962), NL→regex/FOL/LTL with language models: abstract read only. The metric definition (syntactic vs semantic) is not confirmed. **[abstract only]**. [Source](https://arxiv.org/abs/2206.01962)
- **Gold-label quality is itself a faithfulness problem.** NeuroSTAR removed 48% of pooled benchmark data (temporal ambiguity, wrong or trivial labels). Lahiri found test-transcription errors in the human reference. Poiroux et al. built ProofNet# as a *corrected* ProofNet. [NeuroSTAR](https://arxiv.org/abs/2609.03161); [Lahiri](https://arxiv.org/abs/2406.09757); [Poiroux](https://arxiv.org/abs/2406.07222)
- Settled §3 items nl2postcond (intent-derived postconditions find bugs) and SpecGen (code-derived specs confirm code) are consistent with the above and not re-surveyed.

### Inferences
- *Inference*: metric strength runs from weakest to strongest as: syntax valid < exact match < equivalence to one gold < human intent judgement < detects real seeded/human errors. Only the last two speak to faithfulness. For the pipeline, the analogue of "detects real errors" is: tests derived from the prose record reject deliberately wrong spec variants (spec mutants), see Q5/T4.
- *Inference*: no gold formula exists in the brief's setting (records are the only truth). Reference-free techniques are therefore the relevant class: round-trip, multi-generator difference witnesses, test- or scenario-based checks, and human judgement of exhibited cases. Each is necessary-only, so they should be stacked, not chosen between.

### Gaps
- None of these papers formalize *library API decisions* with typed non-commitment (unspecified, optional, profile-declared). Transfer is by analogy only.
- NL2LTL (Fuggitti & Chakraborti, AAAI 2023 demo) own metric not re-read; it appears only as a weak baseline in Req2LTL and nl2spec.
- No paper measures the precision of an LLM *judge* against human labels on spec-to-NL faithfulness in a software-requirements setting. FormalAlign (math) shows GPT-4 precision of 26–51%.

---

## Q4. Validation by exhibition (animation, simulation, witnesses, instances, shrunk examples)

### Takeaway
Exhibiting concrete scenarios has strong qualitative support and some quantitative support. Its known asymmetry is that a reviewer sees what the spec *allows* (under-constraint: an unexpected scenario appears) but rarely notices what it *forbids* (over-constraint: an expected scenario never appears among hundreds). Humans also misjudge trace satisfaction for subtle operators. Exhibition works best when scenarios are *targeted*: given positive and negative cases from the source, difference witnesses between candidates, and shortest violating traces. Browsing raw instances does not.

### Cited Findings
- **FRET simulator caught a real misreading** (Mavridou et al., RE 2020; full text, grade **A**). HUMAN-ONLY.
  - The first FRETISH version of requirement AP-003c required the response only when the condition *became* true. Simulating a two-step trace showed the requirement holding where the authors expected a violation, so they rewrote it as an always-implication (v2). A further hidden mode sub-property was then made explicit (v3).
  - Counterexample simulation also helped separate faulty requirements from faulty models, and COCOSPEC modes were used for vacuity checks.
  - No counts of misreadings caught; effort not quantified.
  - [Source](https://ntrs.nasa.gov/citations/20205000433)
- **Under- vs over-constraint asymmetry in Alloy** (Jovanovic & Sullivan, SEFM 2024, LNCS 15280; full text, grade **A**). HUMAN-ONLY, novices.
  - Corpus: over 93,000 Alloy4Fun submissions checked against an oracle for semantic equivalence.
  - Correct 25.4%. Faulty 45.3%: both over- and under-constrained 23.28%, the rest split between over and under. Syntax/type errors 29.28%.
  - Authors: "To detect an underconstrained error … the user needs to observe a scenario that they did not expect"; "To detect an overconstrained error … the user needs to realize that an expected scenario was never present. Since Alloy commands can produce hundreds of scenarios, this places a high burden on the user."
  - They cite a user study in which novice and expert modelers "struggle to refine a faulty formula given an incorrectly produced scenario". Only 10.86% of faulty submissions were repairable by single mutations.
  - [Source](https://par.nsf.gov/servlets/purl/10615156)
- **Humans misjudge LTL on traces and in translation** (Greenman, Saarinen, Nelson, Krishnamurthi, Programming 2023; full text, grade **A**). HUMAN-ONLY.
  - Design: four rounds over two years; learners and FM/robotics researchers; trace-satisfaction, LTL→English and English→LTL questions; English→LTL checked for *semantic* equality.
  - LTL→English incorrect: 23% (R2), 15% (R3, experts), 24% (R4).
  - English→LTL incorrect: 47%, 28%, 47%, the highest direction.
  - Common misconceptions: WeakU (U read as weak until; half of R2, 9/11 of R4), ImplicitG/ImplicitF (dropping or adding G/F), BadStateIndex.
  - The authors add traces because "traces help in both directions". Tool use "will not automatically catch mistakes. Both the system-under-test and the formula could be incorrect in the same way".
  - [Source](https://arxiv.org/abs/2211.01677)
- **LLM-generated scenarios as validation tests, before formalization** (Cunha & Macedo, arXiv 2510.23350 v2; full text, grade **A-pre**). AGENT-MEASURED.
  - Setup: from the NL requirement plus the domain model, *without seeing any spec*, GPT-5 writes N positive tests (instances that must be allowed) and N negative tests (instances that must be refused) as Alloy run commands.
  - Evaluation: 43 requirements; wrong human specs per requirement 28–848 (mean 157).
  - Wrong-spec detection, by N: about 62% at N=1, 83% at N=2, 90% at N=3, 93.6% at N=5.
  - Invalid (wrong) tests: about 3.9% (30/774 over three runs), more often negative tests.
  - Model valid-test rates at N=3: GPT-5 96%, Gemini 2.5 Pro 81%, Claude Opus 4.1 76%, GPT-5 Mini 67%. Cost about $3.5 per 258 tests.
  - Limits: educational and structural models only; prompts tuned on GPT-5; some negative-test failures stem from requirements ambiguous to humans.
  - [Source](https://arxiv.org/abs/2510.23350)
- **Difference witnesses judged by an LLM panel, and shortest violating traces judged by humans** (NeuroSTAR, Q1). AGENT-MEASURED for the judging. 83.9% of shortest violating traces were valid on 106 law sections; a necessary condition only. [Source](https://arxiv.org/abs/2609.03161)
- **Req2LTL visualization**: with Mermaid diagrams, engineers fixed 13/112 semantically wrong formulas in about 10 min (human-in-loop). [Source](https://arxiv.org/abs/2512.17334)
- **Quint `run` / witnesses** (official docs; grade **B**).
  - The simulator samples executions. `--witnesses` reports how many traces reach a state satisfying a property that should hold *sometimes*, e.g. 7,094 of 10,000.
  - Negating a witness and passing it as `--invariant` makes the simulator print a concrete trace reaching it. `--seed` reproduces a run; `--verbosity=3` shows full executions.
  - No evidence on error-finding rates.
  - [Source](https://quint.sh/docs/checking-properties)
- **Alloy output forms**: a Springer human-factors study found most output forms "fail to be effective, and in some cases even actively mislead users" (at most 8 valid responses). Grade A, **[search extract only]**. [Source](https://link.springer.com/doi/10.1007/978-3-319-66197-1_11)
- **ProB / Event-B animation** (Mashkoor & Jacquot, REJ 2017, Verify-Transform-Animate): needs transformation because animators cannot execute many constructs. Its evaluation section could not be read (Anubis bot wall). **[unreachable]**. [Source](https://doi.org/10.1007/s00766-016-0246-6)

### Inferences
- *Inference*: generic exhibition (browse instances) has low yield against over-constraint, which here is a *lost case* or *added commitment that forbids allowed behaviour*. Targeted exhibition fixes that: ask the tool whether *this* scenario from the record is allowed (positive) and whether *this* rejected-option behaviour is refused (negative). Cunha & Macedo is the closest measured analogue, and it is agent-run and spec-blind.
- *Inference*: per form,
  - TLA+/Quint: one witness per record scenario (a reachability query, i.e. negated invariant) and one violating trace per rejected option.
  - Alloy: `run {scenario} for …` must be SAT; `run {rejected-option instance}` must be UNSAT.
  - Dafny: a scenario becomes a concrete call that must verify; the rejected option becomes an assertion that must fail.
  - Hypothesis: shrunk counterexamples become prose-checkable cases for value-domain clauses.
  
  These need no new tooling, only the record's own cases.
- *Inference*: presenting a judge with a *pair* of formalizations' difference witness concentrates attention on the exact point of divergence. That is cheaper than reviewing each spec whole, and both NeuroSTAR (automated) and Easterbrook (manual) point in this direction.

### Gaps
- No experiment measures detection rates of *translation* errors via TLC/Apalache traces, ProB animation or Hypothesis shrinking specifically. The evidence is case studies (FRET) and an Alloy corpus.
- No cost data in person-hours for exhibition-based validation beyond Req2LTL's about 10 min for 13 fixes and the FormalAlign reference point (human about 3 h per 80 NL–FL pairs).
- Whether an LLM can reliably judge exhibited traces against API prose is unmeasured. NeuroSTAR uses an LLM panel without reporting its standalone precision.

---

## Q5. Clause-level faithfulness: added commitments and lost cases; the record's scenarios and options as tests

### Takeaway
"Says more" and "says less" map onto the classic under- and over-constraint pair: more permissive (lost commitment) vs more restrictive (added commitment). Over-constraint is the harder one to see by inspection. The strongest measured mechanism is spec-blind positive and negative examples derived from the NL source, which then must be accepted or refused by the spec (Cunha & Macedo: about 90% of wrong specs caught at 3+3 tests per requirement, about 4% bad tests). The record's scenarios and rejected options are ready-made sources for those examples. Both "weak" and "misread" spec defects show up when specs are executed on concrete I/O (Lahiri).

### Cited Findings
- **Two-sided defect classes with concrete prevalence**: in Alloy4Fun, both-over-and-under 23.28%, with under and over each a large share of faulty models. The defining test for each is scenario presence or absence. [Jovanovic & Sullivan](https://par.nsf.gov/servlets/purl/10615156)
- **LLM ImplicitG/ImplicitF analogue in humans**: misconceptions that "either ignore or introduce" a G or F quantifier are exactly lost-case and added-commitment errors at operator level. They were common in all populations. [Greenman et al.](https://arxiv.org/abs/2211.01677)
- **Positive and negative tests from NL, before the spec exists, catch both directions.** Positive tests (must be SAT) catch over-constraint; negative tests (must be UNSAT) catch under-constraint. Detection rose from about 62% at N=1 to about 94% at N=5. Negative tests were more error-prone to generate. [Cunha & Macedo](https://arxiv.org/abs/2510.23350)
- **Soundness + completeness scoring of a spec on concrete I/O.**
  - The spec must accept every correct output (else it over-constrains or is wrong) and should reject mutated outputs (else it is too weak).
  - Completeness threshold of about 0.66 separated human-labelled strong from weak specs in most cases.
  - Weak specs found: implication instead of biconditional, upper bound only.
  - [Lahiri](https://arxiv.org/abs/2406.09757)
- **Mutant-based negatives used to train or evaluate alignment checkers**: constant, exponent, variable, type, relational swaps. Synthetic, so they may not reflect real LLM errors (authors' stated limitation). [FormalAlign](https://arxiv.org/abs/2410.10135)
- **Shortest violating trace as an "added commitment" probe**: if the spec's minimal violation is not a violation of the source, the spec forbids something the source allows. 17/106 law sections failed this (NeuroSTAR). [NeuroSTAR](https://arxiv.org/abs/2609.03161)
- **Residual error class after structure is imposed is "ambiguity / context omission"** (Req2LTL). The roundtrip paper's unrepaired rules were dominated by exception clauses, compound conditions and missing predicates. These are exactly where clauses silently drop or add cases. [Req2LTL](https://arxiv.org/abs/2512.17334); [Roundtrip](https://arxiv.org/abs/2604.25031)
- **Vacuity check during formalization**: COCOSPEC modes were used for vacuity checking in the FRET study (preconditions that can never be met). [Mavridou et al.](https://ntrs.nasa.gov/citations/20205000433)

### Inferences
- *Inference*, proposed record-derived checks. None is measured as such; each is the nearest analogue of a measured mechanism.
  1. **Scenario derivability (positive)**: every record scenario's expected outcome must be *permitted* by the spec clause, and *entailed* where the decision is a commitment. A failure means a lost or reinterpreted case. Analogue: Cunha & Macedo positive tests; Lahiri soundness.
  2. **Rejected-option refutation (negative)**: for each option the record rejected, its distinguishing behaviour must be *refused* by the spec. A failure means under-constraint, the decision not captured. Analogue: negative tests; mutant rejection.
  3. **Added-commitment probe**: for each clause, generate the minimal behaviour it forbids (shortest violating trace, Alloy UNSAT core, Dafny failing assertion) and ask a spec-blind judge whether the record forbids it. "No" or "not addressed" flags the brief's observed failure "decision text that went beyond what was asked". Analogue: NeuroSTAR witness check.
  4. **Non-commitment typing check**: for clauses typed *unspecified (one of a set)*, both a positive scenario per allowed outcome *and* a negative scenario for an outcome outside the set. *Deliberately not promised* items must produce at least two witnesses with different outcomes (else the spec silently committed). This extends checks 1–2 to the typed non-commitment of brief §2 and needs at least two witnesses, consistent with the §3 seed "two witness implementations".
- *Inference*: scenarios from the record are written by the same author as the decisions, so they share that author's reading. They test spec-vs-record faithfulness, not record correctness. That is in scope, since records are assumed complete.
- *Inference*: generated tests come out wrong about 4% of the time, more often negative ones (Cunha & Macedo), so a failing check needs a triage step (test wrong vs spec wrong) before it blocks.

### Gaps
- No literature found that uses a requirement's *rejected alternatives* explicitly as negative test cases for a formalization. The mapping above is *Inference*.
- Classic inspection literature on omission/commission defects (Basili PBR; defect taxonomies with "omission", "extraneous information") was not re-read in full. The search surfaced PBR replications without omission-specific figures; Regnell et al. 2000 found multiple perspectives may not raise coverage over single-perspective reading (search extract only). [PBR replication lead](https://core.ac.uk/works/31885195)
- No measured study of clause-level "says more/less" detection on API-style specs with typed non-commitment.

---

## Q6. Where a human must look, and the smallest artefact that makes the check effective

### Takeaway
Across the sources, effective human checks were made on small, concrete artefacts: a visible sub-translation fragment (nl2spec), a two-step simulated trace (FRET), a table row (Easterbrook), a diagram of the formula tree (Req2LTL), a shortest violating trace or a difference witness (NeuroSTAR). Humans are unreliable at reading formulas directly (15–47% error) and at noticing absent scenarios. They should be asked yes/no questions on single concrete cases tied to one source sentence, not asked to review a spec.

### Cited Findings
- **Fragment-level editing**: 15 of 20 initially wrong nl2spec translations were fixed by editing sub-translation fragments, at 1.86 loops on average; only 5 needed full manual formalization. [nl2spec](https://arxiv.org/abs/2303.04864)
- **Diagram of the structured IR**: 13/112 errors fixed in about 10 min via Mermaid visualization. [Req2LTL](https://arxiv.org/abs/2512.17334)
- **Two-step simulation trace with a red/green requirement row** revealed a trigger-vs-always misreading. [FRET LMCPS](https://ntrs.nasa.gov/citations/20205000433)
- **Table rows** made four divergent readings locatable, and "the resulting tables are very readable … much easier to compare … than … the informal specification". [Easterbrook & Callahan](https://ntrs.nasa.gov/api/citations/19970007163/downloads/19970007163.pdf)
- **Shortest violating trace** as the unit of human judgement: two authors per section, a third on disagreement, "valid only when sure". [NeuroSTAR](https://arxiv.org/abs/2609.03161)
- **Fit example tables next to prose** raised correct answers on requirement questions without significant time cost (n = 15). [Talking Tests](https://profs.scienze.univr.it/ceccato/papers/2007/iwpse2007.pdf)
- **Humans should not be the formula readers**: LTL→English wrong 15–24%, English→LTL wrong 28–47%, including expert researchers. [Greenman et al.](https://arxiv.org/abs/2211.01677)
- **Humans miss absent scenarios** among hundreds of instances (over-constraint). [Jovanovic & Sullivan](https://par.nsf.gov/servlets/purl/10615156)
- **LLM judges as substitutes**: GPT-4 as a math alignment judge had low precision (26–51%); human experts 79.6% vs FormalAlign 65.0% agreement with ground truth. [FormalAlign](https://arxiv.org/abs/2410.10135)
- **Cost reference**: one human took about 3 h to judge 80 NL–formal pairs. [FormalAlign](https://arxiv.org/abs/2410.10135)

**Disconfirming search (c): a published pipeline already doing prose → spec → model → reference model with faithfulness gates.**
- Result: none found.
- The nearest are partial:
  - FRET → COCOSIM: NL → FRETish → pmLTL → Lustre monitors on Simulink, with explanation and simulation gates; no reference-model test families.
  - Req2LTL: NL → IR → LTL, with machine validation and optional human diagram review.
  - Roundtrip/Barrett: NL → FOL with round-trip gate and repair.
  - NeuroSTAR: NL → LTLf with multi-generator difference-witness gate.
  - Cunha & Macedo: NL → tests before the spec; the spec must pass them.
- [FRET LMCPS](https://ntrs.nasa.gov/citations/20205000433); [Req2LTL](https://arxiv.org/abs/2512.17334); [Roundtrip](https://arxiv.org/abs/2604.25031); [NeuroSTAR](https://arxiv.org/abs/2609.03161); [Cunha & Macedo](https://arxiv.org/abs/2510.23350)

### Inferences
- *Inference*, the smallest effective artefact per check, for the brief's forms:
  - formula over one instant / value domain: a 1-row example (inputs → allowed outputs) plus the Hypothesis-shrunk counterexample, each linked to the record scenario ID;
  - case table: the single row (or the missing row) where two independent tables disagree;
  - transition table and environment actions: the shortest TLC/Apalache/Quint trace reaching or violating the clause, at most about 5 steps (FRET used 2);
  - frame: the one state variable the spec lets change (or forbids changing) against the record;
  - non-promise register: two witness outcomes shown side by side.
  
  Each is presented with the one source sentence, as a yes/no/"not addressed" question to a spec-blind judge (human, or an independent agent with human spot-check).
- *Inference*: human attention belongs (1) on difference witnesses that independent agents could not resolve, (2) on every "not addressed" answer to an added-commitment probe (the brief's observed over-reach failure), and (3) on a random audit sample of agent-judged witnesses. The latter is needed because the measured LLM-judge precision is low in the one domain where it was measured.
- *Inference*: in the brief's sense, gates that can fail earliest are those needing only the record and the spec text:
  1. Record scenarios and rejected options rendered as positive and negative checks *before* the spec is written (Cunha & Macedo order).
  2. Dual independent slot-filling of the normative form, then a mechanical diff.
  3. Exhibition after the formal model exists.

### Gaps
- No study compares artefact types (trace vs table vs paraphrase) head-to-head for human detection of translation errors.
- No cost model in person-minutes per clause for witness review in a software-API setting.
- Unreachable or abstract-only items to re-check in a verification run: Saarland complementary-specification report; Mashkoor & Jacquot REJ 2017 §7; Ricca et al. IST 2009; Großer et al. REJ 2024; FormalRx full text; Kamsties et al. 2001; NL2CTL ICFEM 2024; AeroReq2LTL; Alloy output-forms study (LNCS 10.1007/978-3-319-66197-1_11); Brilliant/Knight/Leveson.
