# P3: L4 (VeriAct / Spec-Harness), L5 (SpecLoop), L7 (ARSENAL), L9 (two-stage JSON; fail-closed provenance gates)

Scope: verification of four leads from `briefs/Spec faithfulness prior-art check.md` §3. Downloads in `/tmp/claude-0/-home-user-research/8464aabb-24d6-53c7-af9a-cc609bb4c0f8/scratchpad/p3/`. Recommendation IDs and verbatim old text come from `reports/Spec faithfulness and enforcement summary.md`, `… deep dive.md` [DD] and `… verified.md` [V]. Grades follow the brief: A, A-pre, A-workshop, B, C, D. TA = the authors evaluate their own tool. Short version: **none of the four leads changes a recommendation.** L4 and L5 check a spec against *code*, not prose. L7 is a published end-to-end pipeline, but it has no gate for faithfulness to the prose. L9's two-stage claim leads back to Req2LTL, which this branch already uses, and its fail-closed gate cites no primary source.

---

## L4: VeriAct (arXiv 2604.00280)

**Exists as cited?** Partly. The arXiv ID is right, but the paper has been retitled and reauthored across versions (arXiv abstract page, submission history: v1 31 Mar 2026, v2 8 Sep 2026, v3 9 Oct 2026; [abs](https://arxiv.org/abs/2604.00280)).
- v1: Misu, Ma, Lopes (UC Irvine), "VeriAct: Beyond Verifiability – Agentic Synthesis of Correct and Complete Formal Specifications" ([v1 PDF](https://arxiv.org/pdf/2604.00280v1)).
- v3 (current): Misu, Lopes, Ma, Li (UC Irvine), **Lahiri (Microsoft Research)**, "Spec-Harness: Assessing and Guiding LLM-Synthesized Formal Specifications Beyond Verifiability" ([v3 PDF](https://arxiv.org/pdf/2604.00280v3)). In v3, VeriAct is no longer the contribution. It is one of three agents used to test Spec-Harness as a feedback signal.
- **Corrected citation**: Misu, Lopes, Ma, Li, Lahiri. *Spec-Harness: Assessing and Guiding LLM-Synthesized Formal Specifications Beyond Verifiability*. arXiv 2604.00280v3, Oct 2026 (v1 titled "VeriAct: …"). The arXiv record shows no venue or journal reference.

**Grade**: A-pre. **Full text read**: y for both v1 and v3 (method, metrics, RQ3, RQ4, threats). Tables and figures were read from the extracted text.

**What "correct and complete" means (key question).** It is measured **against the implementation's behaviour, not against a gold spec and not against intent**. The authors define T as "a set of valid input–output test pairs, i.e., pairs produced by a known-correct execution of P" (v1 §5; v3 §5.4).
- **PostCorr**: the share of valid pairs (i, o) for which the Hoare triple {true} x:=i; y:=o {φ} holds.
- **PostComp**: the share of output mutants (o±δ and the like) that φ rejects.
- **PreCorr / PreComp**: the same idea for the precondition, over valid inputs and over invalid inputs (inputs that make the method throw).
- The checks run in OpenJML on a stub with pinned values, not by executing the code ([v1](https://arxiv.org/pdf/2604.00280v1); [v3](https://arxiv.org/pdf/2604.00280v3)).
- v1 counts a spec as "meaningfully verified" (MVR) when PostCorr ≥ 0.50 and PostComp ≥ 0.50. v3 uses Post-Harness@0.75.
- v3 builds the tests from the reference implementation. Candidate inputs come from parameter boundary values and from a search that keeps inputs killing new Major mutants of the reference implementation. "A normal return gives a valid pair, and an exception or a timeout gives a candidate invalid input" (v3 §5.4).
- The authors' own framing (v3 abstract): passing a verifier "only confirms that an implementation is consistent with a specification, not that the specification is meaningful".

**What was measured.**
- *Benchmarks*: SpecGenBench (120 Java methods) and FormalBench (662 after cleaning). RQ4 uses FormalBench-120, a sample of 120 tasks. Class and method names are normalised to `Solution`/`solve()` so that names cannot leak intent (v1 §3.2; v3 §3.2).
- *RQ1/RQ3 (v3)*: 14,936 verified specifications from classical tools (Daikon, Houdini) and prompt-based approaches (SpecGen, AutoSpec, FormalBench prompts; six LLMs).
  - 22.7 % (3,395) have no postcondition.
  - 5.6 % came with code the model had changed.
  - Only 35.6 % reach PostCorr and PostComp ≥ 0.75.
  - Houdini has the highest verification rate, "but it verifies mostly through preconditions that admit no valid input" (v3 abstract, §4, Conclusion).
  - v1 figures: Houdini VR 86 % → MVR 2 % on SpecGenBench and 54 % → 0 % on FormalBench (v1 §5.4.2).
- *Instrument validation (v3 §5.6)*: two PhD-student raters, blind to approach and scores, rated 100 verified specifications and 64 single checks.
  - Agreement between raters before discussion: κ = 0.93 on completeness and κ = 0.75 on adequacy.
  - Agreement of the harness with the raters' consensus: PreCorr κ = 0.72, PreComp κ = 0.70; PostComp vs completeness ρ = 0.64.
  - **Post-Harness@0.75 matches the human adequacy judgement for 67 of 100 specifications.**
  - FormalBench's CR correlates better (ρ = 0.72 vs 0.45 on 55 specs), but only 27 % of its detections come from the postcondition rejecting the mutant.
- *RQ4, the agent loop*:
  - **v1** (GPT-4o, up to three verify → error analysis → Spec-Harness cycles): "+5 % improvement in MVR on SpecGenBench … +12 %" on FormalBench over the best prompt-optimised configurations. v1 does not state that the feedback test pairs were kept apart from the scoring pairs (`max_pairs=5`, v1 §7).
  - **v3** has a held-out design. Three agents run with and without a `run_spec_harness` tool, with 10 tool calls per task: Claude Code 2.1.284 with Sonnet 4.6, and Codex and VeriAct with gpt-6.1-sol. The harness scores on a feedback suite that "shares no pair with the evaluation suite". Results for Post-Harness@0.75:
    - SpecGenBench: Claude Code 0.52 → 0.62, Codex 0.60 → 0.75, VeriAct 0.57 → 0.63.
    - FormalBench-120: 0.23 → 0.28, 0.25 → 0.41, 0.25 → 0.28.
    - Significant (exact McNemar, p ≤ 0.005) only for Codex on both benchmarks and Claude Code on SpecGenBench. The other three runs give p = 0.18–0.45, **including both VeriAct runs**.
    - Verification rates fall with the harness: Claude Code 0.86 → 0.74 and 0.68 → 0.45; VeriAct 0.87 → 0.68 on FormalBench-120.
    - Each agent ran once per task ([v3 §6, Table 5, Threats](https://arxiv.org/pdf/2604.00280v3)).
- *TA*: yes. The authors built both Spec-Harness and VeriAct. In v3, Lahiri, whose FMCAD 2024 metric the branch already cites (V §2.1 "Concrete-I/O soundness + completeness"), is a co-author. Spec-Harness explicitly "brings this idea to JML" (v3 Related Work). **So it is not independent of Lahiri FMCAD 2024.**

**Agents**: yes. LLM agents write the specs. The verifier and the harness do the checking, and the stopping rule is a harness threshold. Result: the harness signal helps on held-out tests by 3–16 points, significantly for two of three agents. The authors' own agent VeriAct shows the smallest, non-significant gains.

**Transfer**: *analogous*, close to direct for the mechanism. The specs are method contracts on small Java algorithm methods (benchmark code, not library or API docs). The concrete-I/O stub plus output-mutant mechanism would port to Python contracts (*Inference*).

**Delta.**
- **No change.** L4 measures the strength and correctness of a spec relative to the code it was derived from. That is M-side adequacy, the "SpecGen-style" setting, not A ≡ R.
- **Confirms** the V §2.1 row "Concrete-I/O soundness + completeness of a spec | Lahiri, FMCAD 2024 (A) … Soundness = admits reference output; completeness = rejects mutated outputs". It does so with a larger Java replication, but by an overlapping author.
- **Supports** R19 ("Spec-strength mutation (G9) | analogous (IronSpec, single source) | medium–low") as a second, non-independent source showing that verifier acceptance hides weak specs. This is not enough to raise the confidence, because the source shares Lahiri and checks against code.
- **Adds one qualifier** for any agent loop that optimises a harness score: **score on a suite the agent never saw.** v1's +5/+12 % without that separation became 3–16 points, mostly non-significant, under v3's held-out design (*Inference* from comparing v1 and v3; the populations differ, so this is not a controlled comparison).
- **Bounds** any adequacy proxy: the harness verdict agreed with blind human adequacy ratings on only 67/100 specifications.

---

## L5: SpecLoop (arXiv 2603.02895)

**Exists as cited?** Yes. Fu-Chieh Chang, Yu-Hsin Yang, Hung-Ming Huang (National Taiwan University), Yun-Chia Hsu, Yin-Yu Lin, Ming-Fang Tsai, Chun-Chih Yang (MediaTek), Pei-Yuan Wu (NTU). "SpecLoop: An Agentic RTL-to-Specification Framework with Formal Verification Feedback Loop". arXiv 2603.02895v1 [cs.AR], 3 Mar 2026. The arXiv record shows no venue ([abs](https://arxiv.org/abs/2603.02895); [PDF](https://arxiv.org/pdf/2603.02895)).

**Grade**: A-pre. **Full text read**: y (6 pages).

**What the loop does.**
1. An LLM writes a structured natural-language spec from the RTL (fixed fields; Verilog forbidden in the spec).
2. The **same** LLM, as "RTL reconstructor", rebuilds RTL from the spec alone.
3. The rebuilt RTL is compiled, then compared with the **original RTL** by Yosys EQY ("SAT backend and a depth bound of 10").
4. Counterexamples go back to the spec generator, never to the reconstructor ("information hiding … they can reveal details of the original RTL"). The generator is prompted to classify each failure as spec inaccuracy, spec ambiguity or reconstruction limitation.
5. Budget: three spec generations, each with up to two reconstruction retries ([§III, §IV-D](https://arxiv.org/pdf/2603.02895)).

**What was measured.**
- Benchmarks: VerilogEval ("toy-level modules") and RTLLM ("larger designs"). **The paper gives no task counts.**
- Metric: the RR score of Huang et al. A frontier model (GPT-5 Codex) reconstructs RTL from the spec, and the score is the testbench pass rate. **"Correct" therefore means the spec carries enough information for a strong model to rebuild RTL that passes the existing testbenches.** It is checked against the code's behaviour, not against design intent.
- Six models; three runs each; mean ± std (Table III). Examples:
  - VerilogEval: DeepSeek-V3.1 0.865 (single round) → 0.908 (pass/fail-only) → 0.940 (full diagnosis); GLM-4.6 0.906 → 0.921 → 0.934.
  - RTLLM gains are smaller, sometimes zero or negative: Qwen3-Coder-480B 0.767 → 0.787 → 0.767; Llama4-Scout 0.667 → 0.727 → 0.687.
- Full diagnosis (counterexamples) ranks first in 9 of 12 model × dataset settings, and pass/fail-only in 4 (as stated in §V-A).
- Specs that passed EQY within budget reached RR = 1 in 81.3–91 % of cases. Specs left unverified reached it in 34.6–45.2 % (Fig. 3, four models).
- One qualitative example: an asynchronous vs synchronous reset misread, fixed after one counterexample (Fig. 4).
- Baselines: single-round (Huang et al.'s protocol, reproduced) and a pass/fail-only verifier.
- *TA*: yes.
- Limitations stated by the authors: results depend on the reconstructor and on bounded checking ("fixed depth"); feedback parsing is heuristic.

**Agents**: yes. LLMs write the spec, rebuild the RTL and diagnose failures. EQY is the only non-LLM check.

**Is the round trip a faithfulness check of the spec against the original RTL?** Yes, and only that.
- The anchor is the **code** (original RTL), not prose or intent. The authors frame it this way: equivalence "shows the specification is detailed enough for the reconstructed RTL to be functionally equivalent to the original" (§III-C).
- *Inference*: this is a sufficiency (information-content) check of code → prose. It cannot tell a faithful description of a buggy RTL from a correct spec. That is the "specs derived from code confirm the code" limitation, the same failure mode V §2.6(a) / V line 372 reinforce for SpecGen and nl2postcond.
- *Inference*, a contrast with V §2.1 Roundtrip (Amrollahi et al.):
  - Roundtrip anchors on a *re-formalization* of NL. Its legs can share a misreading and still agree.
  - SpecLoop anchors on the formal source itself. Divergence from the RTL in either leg shows up (up to depth 10), so it does not suffer that particular shared-misreading blindness *with respect to the code*.
  - What it misses instead: (a) a spec that is wrong but which the reconstructor "corrects" from its own priors (generator and reconstructor are the same model, so shared priors are likely); (b) extra wrong statements the reconstructor ignores; (c) any gap between RTL and intent.
- **None of these is measured in the paper.**

**Transfer**: *analogous* (hardware RTL; code → prose direction).

**Delta.**
- **No change.**
- **Confirms** V §2.1, verbatim: "Round-trip and dual formalization catch *divergent* readings. By construction they miss *shared* misreadings". SpecLoop catches divergence only relative to its anchor, and that anchor is code.
- Relevant to Pipeline C's back-generation leg. V §4 Pipeline C step, verbatim: "G2 diffs the generated prose against the records clause by clause (SpecTec-style back-generation used as a round-trip check)."
  - SpecLoop is a measured instance of the *source → prose → source* half: a check that generated prose is sufficient to reconstruct the single source.
  - It does not address the *prose vs records* diff, which is the faithfulness-to-intent part.
- It does **not** trigger the R-D3-4 overturn condition ("Round-trip diffs alone catching as many seeded misreadings as an independent property set"), because no seeded misreadings were used.
- Small support for "counterexamples beat pass/fail as feedback to an LLM" (9 vs 4 top rankings). The differences between variants are often within one std (Table III), so this is weak.

---

## L7: ARSENAL (DTIC ADA611691)

**Which ARSENAL documents exist (Crossref + arXiv API):**
1. **DTIC report**: Ghosh, Shankar, Lincoln, Elenius, Li, Steiner (Crossref spells him "Wilfrid Steiener"). "Automatic Requirements Specification Extraction from Natural Language (ARSENAL)". DTIC, Oct 2014, DOI 10.21236/ADA611691 ([Crossref](https://api.crossref.org/works/10.21236/ada611691)). **[unreachable]**: DTIC is blocked here, and the content was not read.
2. **arXiv**: Ghosh, Elenius, Li, Lincoln, Shankar (CSL, SRI International), Steiner (TTTech). "ARSENAL: Automatic Requirements Specification Extraction from Natural Language". arXiv 1403.3142 [cs.CL]; v1 13 Mar 2014, v2 14 Jul 2014, **v3 20 Apr 2016** (14 pages) ([abs](https://arxiv.org/abs/1403.3142); [PDF v3](https://arxiv.org/pdf/1403.3142)). **Full text read: y (v3).**
3. **NFM 2016**: same six authors and title. NASA Formal Methods 2016, LNCS, pp. 41–46, DOI 10.1007/978-3-319-40648-0_4 ([Crossref](https://api.crossref.org/works/10.1007/978-3-319-40648-0_4)). Venue verified; **full text not read** (6-page short paper). *Inference*: arXiv v3 (April 2016, 14 pp.) is the extended version of the NFM paper. Neither document says so.

**Corrected citation**: Ghosh, Elenius, Li, Lincoln, Shankar, Steiner. "ARSENAL: Automatic Requirements Specification Extraction from Natural Language". NFM 2016, LNCS, pp. 41–46; extended version arXiv 1403.3142v3; earlier DTIC technical report ADA611691 (2014).

**Grade**: NFM paper A, but not read. arXiv v3, which was read: A-pre. DTIC report: B (technical report), unreachable.

**What the pipeline does (arXiv v3 §2–3).**
- **No LLMs.** The NLP stage uses the Stanford dependency parser, hand-written preprocessing and "type rules", an IR table and a predicate graph, then recursive expression-translation rules to LTL. Type inference assigns SAL types.
- **FM stage**: an LTL satisfiability (consistency) check via Büchi-automaton emptiness. If unsatisfiable, "we report this inconsistency to the ARSENAL end-user". Then a SAL transition-system model is built, SAL model checking is run (counterexamples "presented to the user"), and GR(1) realizability is checked. "Counterstrategy-guided assumption mining" adds assumptions "until either the specification is realizable or all the recommendations are rejected by the user". Verilog can be synthesised.
- The authors acknowledge that an unsatisfiable result "can be due to errors in the specification or due to errors in the NLP stage". No gate tells the two apart. The "user interaction" box in the architecture is the only route.

**What was measured (arXiv v3 §4).**
- **NLP-stage accuracy against gold formulas.** 300 sentences in total: 112 for tuning (FAA, TTE) and 188 held out. The test set comprises TTE 72, EUR 11, GPCA 70, LTLMop 35 sentences; F 0.65 / 0.58 / 0.62 / 0.64, **overall F = 0.63**.
  - "Correct" = precision and recall over *sub-formula matches* between the generated formula and a ground-truth annotated formula, using a "Typed Levenshtein distance" with variable renaming free (cost 0).
  - This is **partial-credit syntactic similarity to one gold formula**. It is neither semantic equivalence nor intent.
  - Who annotated the gold formulas is not stated.
- **Perturbation robustness** (Table 2): the share of perturbed sentences whose "output formula was correct", with the judge unstated.
  - TTE (36 sentences): And→Or 16 perturbed, 87 %; Is→Is not 17, 100 %.
  - FAA-Isolette (42 sentences): And→Or 13, 92 %; Is→Is not 13, 92 %; If-A-then-B → B-if-A 40, 65 %.
- **Case studies, n = 1 each, qualitative.**
  - FAA-Isolette regulator: the generated SAL model satisfied a theorem that ARSENAL itself generated from an NL sentence. After a sentence was added for the FAILED→INIT transition, SAL "quickly produced a counterexample" ("found the injected inconsistency"). GR(1) synthesis reported unrealizable, and ARSENAL proposed the assumption `G !(Regulator_Status=1 & Regulator_Init_Timeout=1)`. After the NL was rewritten, the spec became realizable.
  - TTEthernet synchronisation FSM: a model generated "automatically", and a theorem was supplied by the TTEthernet documentation's creators.
  - The authors say the experiment "seeks to evaluate if ARSENAL can faithfully generate the transition system", but the evidence offered is model checking a property ARSENAL also translated from NL: M ⊨ A, not A ≡ R.
- *TA*: yes, SRI authors evaluating their own tool. Steiner (TTTech) is co-author and domain owner for TTE.

**Agents**: none. ARSENAL is a rule-based NLP pipeline from 2014–2016.

**Transfer**: *analogous* (avionics, medical-device and Ethernet requirements; FSM-style models).

**Brief §5(c) answer.** Is ARSENAL a published pipeline with a faithfulness gate against the prose? **It is a published end-to-end pipeline, but it has no faithfulness gate against the prose.**
- Its gates are LTL satisfiability (A-internal), SAL model checking (M ⊨ A) and GR(1) realizability (A-internal, with environment assumptions).
- Faithfulness to the prose is measured only **offline**, as partial-credit similarity to gold formulas (F = 0.63 on 188 sentences). In operation it is left to "iterations with a human in the loop" (§6). The paper describes no step that shows the user a formula, paraphrase or witness tied to a sentence and asks whether it matches.

**Comparison with Pipeline A ([DD §3.3]).**
- Pipeline A puts a spec-blind, record-derived check set *before* the spec and gates faithfulness at G2 ("record checks screened against ≥ 2 wheats; conceptual chaffs must be killed …").
- ARSENAL has no counterpart to G2 and none to the "written before the spec, in a fresh records-only session" isolation.
- Its gates map instead onto Pipeline B's consistency core:
  - LTL satisfiability ≈ G4 conjunction.
  - GR(1) realizability with assumption mining ≈ G4d full realizability (R7).
  - Model checking of generated theorems ≈ an M ⊨ A pass that would need G5 vacuity first. ARSENAL has no vacuity step.
- Its translation is a single deterministic rule chain. That is a "structured intermediate + mechanical translation" design like Req2LTL, but rule-based, without an LLM and without dual formalisation.
- *Inference*: ARSENAL is an early instance of Pipeline B's front half without B's dual slot-filling and diff. It supports P-B's own failure-mode text, verbatim: "The translation is itself a faithfulness step". ARSENAL's 0.63 F shows how lossy that step was for a 2014 rule-based translator.

**Delta.**
- **No change.**
- V §2.6(c), verbatim: "*Result: none found by the earlier run's search* (a search result, not proof of absence)". **This stands.** ARSENAL runs prose → formal model (→ synthesis) with no gate against the prose.
- *Suggested addition, not a change*: list ARSENAL among the "nearest pipelines" in V §2.6(c), next to "**FRET** leaves prose → FRETish to the human". ARSENAL automates prose → LTL/SAL and likewise leaves faithfulness to the human.
- R7 ("rt-consistency / realizability with environment actions, plus well-separation (G4) | inference by analogy (FRET, GR(1)); no library application | low"): ARSENAL adds one more qualitative GR(1) case (n = 1, TA). No change in confidence.

---

## L9: "Two-stage constrained JSON, then deterministic translation" as preferred practice; provenance gates that fail closed

**Sources as cited.** Both repositories exist and were cloned with `git clone --depth 1` into the scratchpad. Both are **grade D**: personal repositories, generated survey and tool README, no review.
- `danielrosehill/Spec-Standard-Research`, HEAD 9f5ccae, 2026-07-28: `docs/prior-art-survey.md` (≈ 2,500 words) ([raw](https://raw.githubusercontent.com/danielrosehill/Spec-Standard-Research/main/docs/prior-art-survey.md)).
- `ashbrener/spec-kit-atlas`, HEAD 5433e3a, 2026-08-18: `README.md`, `examples/generated/RESULT.md` ([raw README](https://raw.githubusercontent.com/ashbrener/spec-kit-atlas/main/README.md); [raw RESULT](https://raw.githubusercontent.com/ashbrener/spec-kit-atlas/main/examples/generated/RESULT.md)).

**Claim 1: two-stage constrained JSON.**
- Source: survey §5. "The consistent architectural finding across this literature is the **two-stage pipeline**: an LLM emits a constrained intermediate JSON representation, then deterministic code converts it onward — chosen because it avoids parsing prose or regex-matching model output, and because schema validation can then check completeness." The survey itself labels it "**reported**". The summary table attributes it to "SLOT / SoLM / OnionL".
- Primary sources it cites:
  - **OnionL (Ma et al.)**, given without a link in §5, but the reference list links "NL→LTL hierarchical decomposition (arXiv 2512.17334)". Resolved through the arXiv API: OnionL is the hierarchical intermediate representation of **Req2LTL**, by Zhi Ma, Cheng Wen, Zhexin Su, Xiao Liang, Cong Tian, Shengchao Qin, Mengfei Yang. Abstract: "a hierarchical intermediate representation called OnionL … combines [LLMs] with deterministic rule-based synthesis … 88.4 % semantic accuracy" ([arXiv 2512.17334](https://arxiv.org/abs/2512.17334)). **This branch has already verified it in full** (V §2.1, "Structured intermediate + mechanical translation | Req2LTL, ASE 2025 (A; TA)", V1-25, V2-08). The survey's "follow-up … schema as a structural prior" also matches Req2LTL's description (*Inference*).
  - **SLOT**: Wang et al., arXiv 2505.04016. Abstract only: a fine-tuned small model maps unstructured LLM output onto a JSON schema; "schema accuracy (99.5 %) and content similarity (94.0 %)" ([arXiv 2505.04016](https://arxiv.org/abs/2505.04016)). Grade A-pre (venue unverified); **abstract only**. It measures schema conformance and content similarity to a reference output, not faithfulness of a formalisation to requirements. It is not evidence for the claim as it bears on this branch.
  - **SoLM**: an Amazon Science blog post (C), not read. Per the survey, it is a schema-specific model.
  - nl2spec and Property Specification Patterns are also listed, but not for this claim.
- **Verdict**: the only primary source behind "two-stage … then deterministic translation" that bears on faithfulness is Req2LTL, which this branch already uses. "Preferred practice" is the survey author's synthesis (D), not a measured comparison.

**Claim 2: provenance gates that fail closed.**
- Source: spec-kit-atlas README. "deterministic Python scripts carry parsing, the **fail-closed faithfulness gate**"; "A deterministic gate rejects any claim whose provenance doesn't resolve, any ungrounded block, any empty callout, or a missing scope note. Faithfulness is *code-enforced*, not model-promised".
- **It cites no primary source.** No paper, DOI or arXiv link supports the gate design (grep over all `.md`, `.yml`, `.html`).
- Its "measurement" is one self-reported run (`RESULT.md`): 222 fragments → 42 claims; `verify.py` → "PASS (0 violations)"; plus a "Codex cross-model review — adversarial human-in-the-loop. Ran five rounds" with issues 10 → 8 → 4 → 2 → 0 and "VERDICT: faithful (0/0/0)". n = 1, TA, D.
- What the gate checks: that each claim's locator resolves to a real corpus fragment. That is a **presence/provenance check, not a check that the claim is entailed by its source**.
- *Inference*: this is the same strength as this branch's G1, verbatim: "**G1** Upward trace | Clause ↔ `decision~rev`; `OUTDATED` | Dangling or orphan links. Presence only, not binding". It is also R16's caveat, verbatim: "low for G1 catching added commitments".

**Grade**: D for both repositories. Req2LTL is A (already on the branch). SLOT is A-pre (abstract only).

**Full text read**: y for the survey and the atlas README/RESULT. Abstract only for Req2LTL here (the branch read it in full earlier) and for SLOT.

**Agents**: atlas uses agents for extraction and reconciliation, and the gate is deterministic. Nothing is measured beyond n = 1.

**Transfer**: *inference* (atlas documents spec repositories; no evaluation).

**Delta.**
- **No change.**
- Claim 1 points back to evidence the branch already holds. V §2.6(a), verbatim: "Measured benefit comes from decomposition plus deterministic translation (Req2LTL)".
- Claim 2 has no primary source. Its gate is a G1-strength presence check.
- **Cross-lead flag for the report writer (L3, not mine)**: the brief's L3 claim "a cross-model review run for five rounds with 'faithful' as a gated verdict" matches spec-kit-atlas `RESULT.md` almost word for word ("Ran five rounds … VERDICT: faithful (0/0/0)"). The other tool may have merged the spec-kit-atlas example into the L3 Springer-chapter citation. Whoever checks L3 should confirm whether the chapter itself reports a five-round review (*Inference*; I did not open L3).

SpecVerify, NL2Spec and OnionL: only OnionL was needed (it resolves to Req2LTL, above). SpecVerify and NL2Spec were not needed for L4, L5, L7 or L9 and were not searched.

---

## Answers bearing on brief §1 questions

1. **Measured method that turns verifier counterexamples into questions for the decision-maker?** Not among these leads.
   - SpecLoop and VeriAct/Spec-Harness feed counterexamples and scores to an **LLM**, not a human.
     - SpecLoop: full diagnosis vs pass/fail ranks first in 9 vs 4 of 12 settings, often within one std ([arXiv 2603.02895](https://arxiv.org/pdf/2603.02895)).
     - Spec-Harness: +3 to +16 points on held-out tests ([arXiv 2604.00280v3](https://arxiv.org/pdf/2604.00280v3)).
   - ARSENAL is the nearest. Unsatisfiability reports and SAL counterexamples are "presented to the user", and counterstrategy-guided assumption mining proposes candidate assumptions that the user accepts or rejects. That is a verifier-derived *question* to a human: "may we assume ¬(Status ∧ Timeout)?". It appears in **one qualitative case study, with no measurement** ([arXiv 1403.3142v3 §3.3, §4.3](https://arxiv.org/pdf/1403.3142)).
   - *Inference*: the assumption-mining method ARSENAL cites ([LDS11] = Li, Dworkin, Seshia 2011) is a lead for "turning counterexamples into questions" that this run did not open (out of scope).
   - SpecLoop's prompt makes the LLM triage each failure as "spec inaccuracy / spec ambiguity / reconstruction limitation". That is an automated ambiguity triage, not measured separately.
2. **Measured faithfulness check of a formal artefact against its NL source (A ≡ R)?** No.
   - L4 measures spec vs **code** behaviour (test pairs from a known-correct execution).
   - L5 measures spec vs **code** (equivalence of rebuilt RTL to the original, bounded at depth 10; RR = testbench pass).
   - L7 measures formula vs **one gold formula** by partial-credit sub-formula similarity (F = 0.63, n = 188), which is not semantic equivalence and not intent.
   - L9 measures nothing.
   - For §5(a)-style classification: L7 is "agreement with a gold formula"; L4 and L5 are "agreement with the implementation".
3. **Published end-to-end pipeline with faithfulness gates against the prose?** No.
   - ARSENAL is a published end-to-end pipeline (NL → LTL → SAL model → model checking/realizability → synthesis; NFM 2016 + arXiv v3). Its gates are internal consistency, M ⊨ A and realizability. Faithfulness to the prose is left to the user. V §2.6(c) stands; ARSENAL could be added to its list of nearest pipelines.
   - SpecLoop is end-to-end in the reverse direction (code → prose → code), gated against code.
   - spec-kit-atlas has a "fail-closed faithfulness gate" that only checks that provenance resolves, n = 1, D.

## Verification debt

- **ARSENAL DTIC report ADA611691 [unreachable]**. It may contain evaluations beyond arXiv v3, such as more corpora or user studies. The NFM 2016 short paper was venue-verified but not read. arXiv v1/v2 (2014) were not compared with v3.
- **ARSENAL**: the annotators of the gold formulas and the judge of "output formula was correct" in Table 2 are not stated in v3.
- **SpecLoop**: task counts for VerilogEval and RTLLM are not given in the paper and were not checked. The 9-of-12 / 4-of-12 ranking counts are the authors' statement; I did not recompute them from Table III, whose stds often overlap.
- **Spec-Harness v2** (Sep 2026) was not read. I compared only v1 and v3. The v1 claims (+5 % / +12 % MVR) are superseded by v3's held-out design. Anyone citing "VeriAct" from v1 should cite v3.
- **SLOT**: abstract only, venue unverified. **SoLM** blog not read. Neither bears on any recommendation.
- [LDS11] counterstrategy-guided assumption mining was not opened (§1 Q1 lead only).

## Self-check

- *Possible misreading of the lead text*: the brief's L4 phrase "until verifiable, correct and complete" is v1's wording. The current version reframes the paper as an evaluation instrument (Spec-Harness) and reports that the authors' own agent VeriAct gains least, non-significantly. I report both rather than choosing one.
- *"Correct and complete" against code*: I read T ("pairs produced by a known-correct execution of P") as making the reference implementation the oracle. v3 §5.4 confirms the reference implementation labels the pairs. There is no NL docstring input, and names are normalised away, so intent is not an input.
- *SpecLoop's shared-misreading claim*: my contrast with Roundtrip (anchor = formal source, so no leg-sharing blindness with respect to the code) is *Inference* from the architecture. The paper does not discuss it. The same model serves as generator and reconstructor, so a spec error "repaired" by the reconstructor's priors would go unseen. That is also *Inference*, not measured.
- *ARSENAL versions*: I treat arXiv v3 as the extended NFM 2016 paper because they share authors and title and appeared the same month. Neither document says so.
- *ARSENAL vs Pipeline A/B mapping* is *Inference*. The gate correspondences (LTL-SAT ≈ G4, GR(1) ≈ G4d) are functional analogies.
- *L9/L3 overlap*: the five-round "faithful" review is in spec-kit-atlas RESULT.md. Whether L3's chapter also contains it is unverified by me.
- I ran no git commands in the repository and wrote nothing there except this notes file. Repository clones and PDFs are in the scratchpad `p3/`.
