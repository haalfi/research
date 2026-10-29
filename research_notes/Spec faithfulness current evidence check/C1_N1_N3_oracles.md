# C1: N1 (LLM2Alloy) and N3 (contrapuntal languages): oracle leads

Scope: brief §3 leads N1 and N3; brief §1 question 1; §5 checks (a) and (c); verdicts on the §8 Kernsatz rewrite and pipeline additions 2 and 3. No search went beyond resolving these two leads. Downloads are in `/tmp/claude-0/-home-user-research/8464aabb-24d6-53c7-af9a-cc609bb4c0f8/scratchpad/c1/` (n1.pdf, n3.pdf and their text extracts). Every old-text quotation below was checked against the report file.

Abbreviations follow the branch: [V] verified edition, [DD] deep dive, [S] summary, [TD] trial design, [PA] prior-art check. TA = the authors evaluate their own tool. FT = full text read.

---

## N1: LLM2Alloy (ICST 2026)

### Takeaway
LLM2Alloy is a real, 5-page exploratory ICST 2026 paper (n = 2 libraries, one LLM, 3 runs per prompt, 1 bug found). **It does not measure the central claim.** Its arms are two documentation routes (README → Alloy → tests and README → tests directly) plus a code route (source → Alloy → tests). Its one finding is an **implementation bug**, a missing duplicate-name guard in Flipper. No arm derives oracles from a spec that misreads the prose, and no spec misreadings were seeded. **Answer to §1 Q1 for LLM2Alloy: no.**

### Citation, grade, FT
- **Corrected citation**: Tasmim Rashid, Muhammad Zubair Malik (North Dakota State University), "LLM2Alloy: Investigating LLM-Generated Formal Specifications for Automated Test Derivation in Production Software", *2026 IEEE International Conference on Software Testing, Verification and Validation (ICST)*, Daejeon, 18–22 May 2026, pp. 717–721, DOI 10.1109/ICST69053.2026.00092 — [Crossref](https://api.crossref.org/works/10.1109/icst69053.2026.00092). Author version: arXiv 2607.18555v1, 20 Jul 2026 — [arXiv](https://arxiv.org/abs/2607.18555); [PDF](https://arxiv.org/pdf/2607.18555).
- **Exists as cited?** Yes. The lead names no authors. The CSDL ID `2iasUM9RFHa` / `330800a717` matches pp. 717 of the ICST volume. The arXiv *metadata* title reads "LM2Alloy", while the PDF and Crossref read "LLM2Alloy", an arXiv metadata typo — [arXiv API](https://export.arxiv.org/api/query?id_list=2607.18555).
- **Grade: A** (peer-reviewed ICST main-volume short paper; venue verified via Crossref). The track (e.g. new ideas or short papers) was not verified, because the CSDL page renders only through JavaScript and returned no content to WebFetch.
- **FT: y** (arXiv author version, 5 pages, read in full). The IEEE version of record was not read. Pages and title match, but text differences cannot be excluded.

### Cited Findings: what was measured
- **Pipeline (Fig. 1, §3.1).** "Documentation and source code are independently translated into Alloy specs by GPT-4o; each spec generates a pytest suite executed against the real library." Three prompts: README → Alloy (Prompt 1), "Reverse-engineer an Alloy specification from this code" (Prompt 2), and Alloy → pytest "that validate ONLY the constraints defined in this spec against the real library" (Prompt 3) — [arXiv PDF §3.4](https://arxiv.org/pdf/2607.18555).
- **The Alloy Analyzer was never run.** The Alloy text is only an intermediate prompt artefact. "integrating the Alloy Analyzer for automated counterexample generation" is listed as future work (§6) — [arXiv PDF](https://arxiv.org/pdf/2607.18555).
- **Agents.** GPT-4o through the web interface, in fresh chat sessions, "with no API calls". "We made no manual corrections to any generated specification or test. The only human judgement involved was deciding which README sections and source files to include in each prompt" (§3.1, §3.3) — [arXiv PDF](https://arxiv.org/pdf/2607.18555).
- **n.** Two libraries: Flipper (feature flags) and Cerberus (dict validation). "Each prompt was submitted three times in separate sessions." Test count was unconstrained. "This is a proof-of-concept study, not a statistical one" (§3.5, §4.1) — [arXiv PDF](https://arxiv.org/pdf/2607.18555).
- **What "correct" or "found" meant.** A generated test failing against the real library = "exposed a constraint violation" (Table 1). There were no seeded faults, no mutation score (recommended only as future work, §5.4), and no human labelling of test validity. The bug was not confirmed by maintainers: "The duplicate-name bug has not yet been submitted as a pull request" (§5.3) — [arXiv PDF](https://arxiv.org/pdf/2607.18555).
- **Flipper result (Table 1, §4.2–4.4).**
  - Requirements spec: mean 8.0 tests (SD 2.6), 1 failure, bug found.
  - Code spec: mean 6.7 tests (SD 0.5), 0 failures, bug not found.
  - The README spec models uniqueness as a `pred` and guards `Create` with `not Exists`. The code spec models it as a `fact`, "assumed unconditionally true and therefore never tested."
  - The bug: `create()` "never calls exists() before writing to the store." README: "Each feature flag is identified by a unique name."
  — [arXiv PDF](https://arxiv.org/pdf/2607.18555)
- **Baseline (§4.4).** README → pytest directly, "using a prompt comparable in specificity to Prompts 1 and 3 combined" (the prompt text is not given). "Across three runs, the baseline produced 37 tests consistently, all of which passed, and achieved 68% branch coverage … Not a single test touched the uniqueness constraint, and the duplicate-name bug went undetected every time." The Alloy route produced `test_create_duplicate_name_fails` "in all three runs" — [arXiv PDF](https://arxiv.org/pdf/2607.18555).
- **Cerberus (§4.5).** The code spec "unified [strings and lists] under a SizedVal abstraction" and produced "two additional tests covering list-length constraints." "All 34 Cerberus tests passed." No defect was found. Table 2 gives per-run counts of 16/18/4 (requirements) and 18/22/13 (code); 34 matches run 1 only (16 + 18), which is not stated — [arXiv PDF](https://arxiv.org/pdf/2607.18555).
- **Stability.** Code prompts had mean SD 2.15 versus 5.0 for documentation prompts (§4.6) — [arXiv PDF](https://arxiv.org/pdf/2607.18555).
- **TA**: yes, the authors evaluate their own pipeline. Threats (§5.4): "Two libraries are enough for a proof-of-concept, but we cannot claim that the results generalise" — [arXiv PDF](https://arxiv.org/pdf/2607.18555).

### §5 check (a)
**Two documentation routes (plus a code route) on an implementation bug. It is not prose-derived versus spec-derived oracles on spec misreadings.**
- Both compared prose arms (README → Alloy → tests and README → tests) derive from the *same prose*. The comparison isolates the effect of a formal intermediate on *which documented constraints get tested*.
- The code arm derives from the *implementation*, not from a spec that reads the prose.
- No human or agent-written spec misreads the README. The defect sits in the code. There are no seeded misreadings and no S⁺-style comparator ([TD §2.0]).
- n = 1 defect, 1 library, 1 model, no statistics.

### Inferences
- *Inference*: the nearest link to the branch is the code arm. A model reverse-engineered from an implementation encoded the implementation's omission as an assumption (`fact`) and so never tested it. This is one more n = 1 instance of the mechanism the branch already holds ("A misreading in the source propagates into every layer (confirmed by IronSpec, Fonseca I1, Sail vs Spike)" [S §3]). It also fits the rule that expectation checks must not be derived from R (G0 import ban, D5-R2). It adds no measured yield.
- *Inference*: the direct README → tests arm is itself *prose-derived*, and it missed a constraint the README states in one sentence, in 3/3 runs. So a prose-derived oracle does not by default test the stated constraints; how the checks are elicited matters. This weakly agrees with the branch's per-clause obligation design (R11: "Harness imposes one test obligation per clause ID") and with drafting record checks per scenario. It is n = 1, the baseline prompt is not published, and it does not change R1 or R11.
- *Inference*: the "pred vs fact divergence" signal is a structural diff between two derived models. It resembles Pipeline B's "Dual independent slot-filling … then a mechanical diff" [V §4], but one leg is derived from code, which the branch's information-flow design forbids for expectation artefacts.

### Transfer
*Analogous* for the defect class (library API behaviour: uniqueness on `create`). For the central claim it gives *no* evidence, not even analogous: the comparison it makes is a different one.

### Delta
- [V §1] Kernsatz, last sentence (verbatim): "That prose-derived oracles catch spec misreadings that spec-derived ones miss has no head-to-head measurement, and a small trial on one operation can measure it." **No change. The sentence stays true.**
- [S §1] item 3 (verbatim): "**The central claim is still unmeasured**: that prose-derived oracles catch spec misreadings that spec-derived oracles miss." **No change.**
- [S §5] Q1 (verbatim): "Do record-derived oracles catch misreadings that every spec-only check misses?" **Stays open**; TD H1 is still the settling measurement.
- R1, R11, R13: no confidence change.

### Gaps
- IEEE version of record not read; the paper track was not verified.
- The baseline prompt text is not published.
- The Flipper bug could not be checked against the repository: raw.githubusercontent.com returned 404 for `flipper/client.py` on `master`, `main` and `develop`. It stands on the paper's quoted code only [unverified by this run].

---

## N3: Dai et al., "Validating Autoformalized Specifications via Contrapuntal Languages"

### Takeaway
N3 is an oracle-free **spec-acceptance** method. The same LLM formalises the NL intent in two synthesised, structurally incompatible sugared languages over SMT-LIB, and a spec is accepted only if Z3 proves the two formalisations equivalent. In effect it is dual formalisation with forced representational diversity.

The "positive tests from reference executions, negative tests from mutant outputs, Z3 admits each pair" mechanism that the other tool describes is the paper's **evaluation method**, adopted from Endres et al. and Lahiri (FMCAD 2024). It is not the proposed check.
- §5(c), first part: **yes, the positives are code-derived** (reference executions).
- §5(c), second part: as a scenario-derivability gate, it adds nothing the branch lacks. The admit-a-pair check is already in G2, with Lahiri as its analogue.

What N3 does add is a measurement that deliberately different representations *reduce but do not remove* shared errors.

### Citation, grade, FT
- **Corrected citation**: Yihan Dai, Xuanlin Liu, Haoxiang Jia, Tianchi Li, **Xin Zhang, Sergey Mechtaev** (Peking University; Liu: Nankai University), "Validating Autoformalized Specifications via Contrapuntal Languages", arXiv 2610.30059v1 [cs.SE], 21 Oct 2026 — [arXiv API](https://export.arxiv.org/api/query?id_list=2610.30059); [PDF](https://arxiv.org/pdf/2610.30059v1). The brief lists only four of the six authors.
- **Exists as cited?** Yes (the title matches).
- **Grade: A-pre** (no venue stated in the arXiv metadata or the PDF).
- **FT: y** (25 pages incl. supplement). The figshare artefact was not inspected.

### Cited Findings
- **What "contrapuntal" means.** "pairs of task-specific formal languages, each designed to express the intended specification, yet admitting no structure-preserving translation between them. An LLM formalizes the intent independently in each language, and we accept a specification only if a solver proves the two formalizations equivalent." The name comes "after musical counterpoint, where independent melodies combine into one harmony" (abstract, §4) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **How the languages are built.** 10 LLM-sampled seed specs are cut into fragments, which become constructs (syntactic sugar over SMT-LIB FOL). Z3/MaxSat chooses cuts so that every seed is expressible in both languages (adequacy) with no same-shaped sugarings (non-isomorphism) (§4–5) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Setting.**
  - Benchmarks: HumanEval+ (161 tasks with mutants) and LiveCodeBench (175 tasks), single pure functions, pre/postcondition in SMT-LIB.
  - Models: GPT-5.4 mini and Qwen3.6-Flash with thinking off and on.
  - Budget: 30 responses per task for every method.
  - Baselines: direct generation, plurality voting (Symbolic Equivalence, Li et al. NeurIPS 2024), and round-trip verification (Amrollahi et al., arXiv 2604.25031, which is lead N4 / "Roundtrip" on this branch) (§6) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Evaluation ("correct").** "Neither benchmark provides reference formal specifications, so, following prior behavioral evaluations [8, 29, 30], we evaluate specifications on input–output pairs: positive tests from reference executions and negative tests from mutant outputs … Z3 checks whether the specification's pre- and postconditions, with the variables bound to the pair, are satisfiable."
  - "A negative test kills its mutant if the pair is rejected while the input satisfies the precondition, so that an overly restrictive precondition does not count as a kill."
  - Unknown solver results count "as neither a pass nor a kill"; τ-completeness tolerates unknowns.
  - Mutants: 779 on HumanEval+ (GPT-5.5-generated single-bug variants, 4.84 per task); 2,587 on LCB (1,618 real wrong submissions + 969 generated).
  - Correct = τ-complete and kills every evaluated mutant (§6) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Results (Table 1, §6.1).** The paired task-level bootstrap gain in Avg. CR over round-trip verification is 22.13 points at τ = 0.8 (95 % simultaneous CI [6.67, 37.60]); over plurality voting it is 22.79 points ([7.57, 38.00]). Abstract: "+12.0% on HumanEval+ and 42.9% on LiveCodeBench" (relative) over the strongest baseline; MKR|C of 98.6 % / 96.2 % versus 92.8 % / 78.3 % — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Coverage cost.** The share of tasks with any accepted spec is 29.81 % (HEP) and 8.76 % (LCB), against seed availability (an upper bound on correct acceptance) of 39.17 % and 12.97 %. Round-trip reaches 64.60 % / 52.00 % and plurality 73.27 % / 48.77 %; "they must accept incorrect specifications for many tasks" (§6.1) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Ablation (RQ2).** Random seed split into two languages (no contrapuntality) gives −15 % CR and −34.5 % Avg. CR, relative (§6.2) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Correlated errors (RQ3).** Error coincidence (among pairs of incorrect specs, the share that are equivalent) falls "from 25.23% for single-language pairs to 21.88% for cross-language pairs on HumanEval+, and from 10.07% to 5.72% on LiveCodeBench" (§6.3) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Residual shared errors (RQ5).** "contrapuntal languages' false-positive failures accounted for 38.9% of all 216 failures … the two languages still share the same seed formalizations and therefore cannot eliminate correlated errors completely" (§6.5) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **Ambiguity case (n = 1, HumanEval/154).** The two languages' dominant classes disagreed on the empty second word. This exposed a boundary case the description leaves open; "cross-language disagreement can surface plausible alternatives, not determine which matches the user's intent" (§6.6, §7) — [PDF](https://arxiv.org/pdf/2610.30059v1).
- **TA**: yes. Kim et al. 2025 (correlated errors) is cited as motivation [15]. Lahiri FMCAD 2024 [16] and Endres et al. [8] are cited as the source of the evaluation method. **Spec-Harness (Misu … Lahiri, arXiv 2604.00280) is not cited** (reference list, pp. 19–21) — [PDF](https://arxiv.org/pdf/2610.30059v1).

### §5 check (c)
- **Are positives code-derived?** **Yes.** Positives are reference-implementation outputs; negatives are outputs of buggy program variants. Both are code-anchored, as in Lahiri FMCAD 2024 and Spec-Harness (L4, [PA] "measured against the **implementation**"). They are, however, the *evaluation harness*, not the proposed validator.
- **Can it serve as the spec-blind scenario-derivability gate?**
  - The *admit-a-pair* mechanism can, but the branch already has it. [V §3] check map, verbatim: "Scenario derivability; rejected-option refutation; added-commitment probe via failing Dafny assertion or Hypothesis-shrunk case shown with the source sentence (Cunha & Macedo; Lahiri)". [V §2] item 1, verbatim: "**Scenario derivability**: each record scenario's outcome must be permitted by the clause, and entailed where the decision commits. Analogue: Cunha & Macedo positives; Lahiri soundness."
  - Replacing reference executions with record scenarios (positives) and rejected-option outputs (negatives) is exactly R1/R2.
  - N3 gives no evidence for record-derived pairs. Its pairs come from code, and its negatives are LLM- or contest-generated program bugs, not rejected design alternatives.
  - The admit check tests only *permit*. "Entailed where the decision commits" needs an extra uniqueness or forcing query, which N3 does not do (*Inference*).
  - The contrapuntal *method itself* is not a scenario gate. It checks agreement between two formalisations and never consults scenarios. On the branch it maps to Pipeline B's dual slot-filling / G2 difference witnesses, not to scenario derivability (*Inference*).

### Inferences
- *Inference*: two operational details from N3's harness carry over to G2 and R2 cheaply. Neither is a recommendation change:
  1. A negative counts as refuted only if the precondition admits the input. Otherwise an over-strict precondition "refutes" every rejected option vacuously, a G5-style vacuity hole.
  2. Solver *unknown* counts as neither pass nor refutation.
- *Inference*: RQ3 and RQ5 are a measured instance (pure functions, TA, A-pre) of the branch's position that dual formalisation misses shared misreadings. Forcing different representations cut error coincidence only from 25.2 % to 21.9 % on HumanEval+. 38.9 % of the 216 failures were wrong specs accepted by solver-proved agreement. This supports in direction, but does not raise, the Kernsatz *Inference* that independence needs deliberately different derivations, and it confirms that agreement checks stay necessary-only.
- *Inference*: the HumanEval/154 case is a single example of a difference witness exposing an ambiguity the prose leaves open. It matches the branch's routing of difference witnesses to a human ([V §4] item 2), but is not a measurement.

### Transfer
*Analogous*: single pure-function FOL contracts with no state, environment or non-commitments. It is the same domain class as Lahiri/Spec-Harness and claimcheck's Dafny slice.

### Delta
- [V §2.1] core finding (verbatim): "Round-trip and dual formalization catch *divergent* readings. By construction they miss *shared* misreadings, as Roundtrip, NeuroSTAR and Clover each state". **Confirmed and now measured** (residual error coincidence of 21.9 % / 5.7 % under forced diversity; 38.9 % false-positive share). It is a corroborating citation, A-pre, TA. No confidence change.
- [V §1] Kernsatz (verbatim): "Round-trip, dual-formalization, compile/verify and witness-validity checks are necessary-only and blind to misreadings both legs share". **No change.** N3 qualifies "blind" only in degree: representational diversity reduces shared errors somewhat. "Necessary-only" stands.
- [V Part 3] R2 (verbatim): "Use rejected options as negatives | inference (no source does this) | low". **No change.** N3 uses program mutants, not rejected options; "no source does this" stands.
- R1 and the G2 check-map cell: no change. The Lahiri analogue is already cited; N3 only re-uses it.
- P-B (Pipeline B, "low for agent translation"): no change. *Inference*: contrapuntal languages are a candidate way to make B's two slot-filling lineages differ by representation rather than by provider, but nothing measures this on stateful specs.

### Gaps
- No venue; figshare artefact not inspected; no human labels of intent (reference outputs stand in for intent, which the authors acknowledge in §7).
- HumanEval+ mutants are LLM-generated (~5 per task), so "sound" means killing a small, generated mutant set.
- No transfer to stateful or temporal clauses is measured.

---

## Verdicts on the other tool's proposed edits

**Kernsatz rewrite: reject.**
- Proposed: "Direct evidence remains limited, but a 2026 exploratory study found that a documentation-derived Alloy specification pipeline exposed a documented-behaviour violation missed by direct documentation-to-test generation in all three runs; broader head-to-head evidence across domains is still lacking."
- Each factual clause is accurate about LLM2Alloy. Placed in the sentence about the central claim, though, it implies a head-to-head measurement that does not exist. The two compared arms are both documentation-derived. The fault is an implementation bug, not a spec misreading. No spec-derived oracle arm exists.
- "Direct evidence remains limited" wrongly suggests some direct evidence exists. The [V §1] sentence "…has no head-to-head measurement, and a small trial on one operation can measure it" remains exactly true and should stay.
- If LLM2Alloy is mentioned at all, it belongs in a related-work or nearest-analogue line, not in the Kernsatz. A suggested line: "LLM2Alloy (ICST 2026, A, n = 1 bug, TA) compares two documentation routes on an implementation bug; it does not measure prose- vs spec-derived oracles on spec misreadings."

**Pipeline addition 2 ("treat documentation-derived and code-derived specifications as complementary … supports your dual-derivation recommendation"): reject.**
1. The branch has no code-derived spec route, and its information-flow design forbids one for expectation artefacts. R is built after the spec, and the expectation tests may not import R (G0, D5-R2). Its "dual" derivations are (i) two lineages slot-filling from the *prose* (Pipeline B) and (ii) two test families separated by information flow. Neither derives from code.
2. LLM2Alloy's own evidence *for* the code route is two extra passing tests on Cerberus (no fault found). Its evidence *against* the code route is that it missed the Flipper bug by encoding the code's omission as a `fact`.
3. "Different sources expose different classes of omitted constraints" generalises from one observation per library, with one model.

Usable remainder (no recommendation change): a one-line corroborating anecdote for the existing rule that oracles must not be derived from R.

**Pipeline addition 3 ("add a computable input–output oracle check … positive tests from reference executions and negative tests from mutant outputs, with Z3 checking whether pre/postconditions admit each pair"): adopt with changes. In substance this is already adopted, so it is no new addition.**
1. **Re-attribute.** The pair-admission check is N3's evaluation method, taken from Endres et al. and Lahiri FMCAD 2024. The branch already uses it as the analogue for scenario derivability ([V §2] item 1; [V §3] check map; [PA] L4). N3's own contribution is contrapuntal dual formalisation, which is a different check.
2. **Change the source of the pairs.** Reference executions are code-derived. For the spec-blind gate, pairs must come from record scenarios (positives) and rejected options (negatives), which is R1/R2 as written. R2 stays "inference (no source does this) | low".
3. **Optionally adopt two harness rules as G2 implementation details** (*Inference*, not recommendation changes):
   - a negative counts as refuted only if the precondition admits its input;
   - solver unknown counts as neither pass nor refutation.

   Note also that pair admission tests *permit* only. "Entailed where the decision commits" needs an extra query.

The Kernsatz rewrite's companion claim ("claimcheck + LLM2Alloy … move … prose-versus-spec-derived oracle comparison … from purely inferred to empirically supported") is **rejected** for the LLM2Alloy half, for the reasons above. claimcheck is outside this note's scope; it was settled in [PA] as L2.

## Answer to brief §1 question 1 (for N1 and N3)

- **LLM2Alloy: no.** It compares two documentation routes and one code route on one implementation bug. No spec misreads the prose, no misreadings are seeded, and no spec-derived oracle arm exists.
- **N3: no.** It compares spec-acceptance strategies (direct, plurality, round-trip, contrapuntal) against code-derived I/O pairs. No arm derives oracles from the prose independently of the spec.

## Verification debt

- LLM2Alloy: the IEEE version of record and its track label (main volume per Crossref; short paper by length); the baseline prompt text; independent confirmation of the Flipper bug (repository file not reachable at the tried paths; no maintainer response yet).
- N3: venue (none yet); figshare artefact; whether the RQ3 drop in error coincidence has a CI (none reported).
- Neither lead was checked for later versions beyond arXiv v1.

## Self-check

- Full texts read for both leads (N1: arXiv author version; N3: arXiv v1 incl. supplement). No verdict rests on a search snippet. The WebSearch hit for "LM2Alloy" was used only to locate arXiv 2607.18555.
- Old-text quotes were copied from the report files ([V] line 81, line 89, the R2 row at line 708, the §3 check-map cell at line 384, the §2 item at line 106; [S] §1 item 3 and §5 Q1).
- Corrections to the brief: N1 has authors Rashid & Malik, a DOI, and an arXiv twin. N3 has six authors, not four. The mechanism the brief attributes to N3 is its evaluation, not its method.
- No git commands were run in the repo, nothing else in the repo was written, and downloads stayed in the scratchpad `c1/`. The one curl to an undocumented CSDL API was blocked by the permission system and not retried.
- Possible bias: verdicts lean conservative (reject or no change), consistent with the brief's evidence rules. The strongest counter-reading is that LLM2Alloy's code arm is a "spec that inherits a blind spot". I rejected that because the code arm is not a reading of the prose and the comparison is n = 1.
