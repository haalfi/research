# Test whether record-derived oracles really catch more

Trial design (not run) for the central claim the earlier editions left unmeasured: "Oracles derived from the prose records catch spec misreadings that oracles derived from the spec miss." This edition builds on `reports/Spec faithfulness and enforcement deep dive.md` (gates G0–G9 incl. G4a–G4d; Pipelines A, B, C/C′). It also uses the verified edition and the first report where the deep dive is silent. Inputs are three method notes in `research_notes/Spec faithfulness and enforcement trial design/`: M1 (mutation and seeding), M2 (LLM evaluation protocols) and M3 (small-n statistics). IDs such as "M1-R11" point to recommendations in those notes.

**Conventions.**
- Grades: A / A-pre / A-workshop / B / C / D. **FT** = full text read (y / partial / n). **[unreachable]** = not fetched; such a source is used only through a named full-text secondary source.
- *Inference* = this run's reasoning. **Own calc** = computations by the note authors (M1–M3) or by this synthesis. This synthesis's own checks used scipy in a scratchpad venv, seed 20261029.
- Lineages are abstract: providers **X, Y, Z, W**. People are **P1** (the maintainer), **P2** (an external second person) and **P3** (an optional adjudicator).
- **E** = expectation family (record-derived oracles). **S** = spec-derived oracles. **p10** = share of seeded misreadings caught by E and missed by S; **p01** the reverse; **delta** = p10 − p01.

---

## 1 Kernsatz

On one operation, 60 seeded spec-level misreadings (10 per class) are planted upstream and every spec-derived layer is **regenerated from the misread artefact**; the primary measure is the share of human-confirmed misreadings caught by record-derived oracles and missed by **every** spec-only check (G3–G5 and G9 included, not just spec-enforcing tests), counted as support only if the record-derived suite also passes held-out allowed-variant implementations. Equal-count expectation vs spec-enforcing kills is a secondary hypothesis and Pipelines A/B/C′ are compared descriptively on the same faults. At this n the trial can confirm a large effect (true p10 ≥ 0.20 → support with probability 0.93, own calc) or refute the claim for this operation (≤ 1 E-only catch in 60), but cannot rank pipelines, certify lineage independence, or speak to other operations.

---

## 2 Trial protocol

### 2.0 Why the primary hypothesis is reframed (M3's near-triviality point)

M3 (*Inference*): "S is derived from the spec, and a seeded misreading lives in the spec. A faithful S therefore encodes the misreading and can catch it only through internal inconsistency … Expect p01 ≈ 0 … the McNemar test reduces to 'is p10 > 0'." I accept this. Three consequences shape the design (all *Inference*):

1. **The comparator is the whole spec-only side.** Comparing expectation tests with spec-enforcing tests alone is a straw man. The question that matters is whether anything spec-derived catches the misreading. The comparator **S⁺** is therefore every check that never consults the records:
   - G0 and G3;
   - G4 and G4a/G4b;
   - G5, G6 and G9;
   - the spec-enforcing tests.

   S⁺ can catch cross-table contradictions (G3/G4), wrong environment exposure (G4a) and regeneration drift (G6). So p01 is no longer zero by construction, and the test is **severe** in Mayo's sense, quoted by Ernst & Baldassarre (A; FT y): E could fail.
2. **Estimation, not significance.** The primary estimand is the **size of p10** with a Clopper–Pearson (CP) interval, compared against pre-set margins. M3 recommends planning "for the precision of p10 and p00, not only for the McNemar power". delta with a mid-p McNemar test is secondary.
3. **A validity condition is part of the primary.** An E suite that fails on everything "catches" every seed. Support therefore also requires that E's residual over-strictness on **held-out** allowed-variant wheats stays under a ceiling (condition V, §3). This answers brief §2's "Over-strict tests" directly.

The literal comparison (expectation tests vs spec-enforcing tests at equal test counts) is kept as **H3**. It is the verified edition's G8 and the operational test of its R17 overturn condition, quoted in §4.4.

### 2.1 Choice of the operation (criteria only)

| # | Criterion (must hold) | Why | Basis |
|---|---|---|---|
| O1 | Has ≥ 1 complete/disjoint **case table** with ≥ 4 rows | Lost case and cross-table contradiction need rows | Brief §3.1; M1-R19 seed shapes |
| O2 | Has a **state × operation** table over a handed-out object, ≥ 3 states | Seeds of the transition-cell type; G3 missing-cell check | Brief §3.1; verified check map |
| O3 | Has ≥ 2 **environment actions**, at least one fault or cancellation and one concurrent or out-of-band actor | "Wrong environment exposure" class; G4a/G4b exercised | Brief §3.1; deep dive §2.4 |
| O4 | Is or contains an **interval operation** governed by a history predicate | History-form seeds; Porcupine-route G6 | Brief §3.1; deep dive R-D3-2 |
| O5 | Uses ≥ 3 of the 5 **non-commitment types**, including *unspecified* and *deliberately not promised* | "Wrong non-commitment type" class; wheats need non-promised dimensions | Earlier brief §2; deep dive D1-R1 |
| O6 | Has ≥ 2 **profile** values with a declared deviation | Profile seeds; G4a per profile value | Earlier brief §2; deep dive §3.1 |
| O7 | Offers ≥ 60 **distinct seed loci**: clause or row sites where a class-c misreading is expressible without overlapping another seed's locus | 10 seeds per class without reuse | *Inference*; M1-R20 |
| O8 | Its records are complete and **frozen** at a revision hash, and were reviewed by P1 | The earlier brief assumes complete records; ground truth needs a fixed reference | Earlier brief §1; RR1 "exactly replicate" (Empirical Standards RR, B; FT y) |
| O9 | Has ≥ 1 documented **past real misreading** of the three brief §2 modes, reconstructible as an artefact | Held-out realism anchor | M1-R8 |
| O10 | Not used in earlier own trials or public reports | Contamination | M2-R5; Sallou (A-workshop; FT y) |
| O11 | A Python R with a Hypothesis state machine is feasible | Pipeline A G6 stack | Deep dive R-D3-1 |

Procedure (*Inference*, following the Empirical Standards' "justifies selection of experimental objects" and "explains the sampling strategy", B; FT y):
- P1 scores every candidate operation on O1–O11 before any seeding.
- If several qualify, one is drawn at random and the draw is logged. This keeps the choice from favouring an operation on which E is known to do well.
- If none qualifies, record which criterion failed. Do not relax O1–O6, because each one feeds a misreading class.

### 2.2 Misreading taxonomy and seeding protocol

**Unit.** A seed is defined **semantically**, once: "record clause r is read as r′, class c". It is then rendered in four forms:
- Pipeline A's typed-slot spec;
- Pipeline B's first slot-filling;
- Pipeline C′'s Quint source;
- an R patch, **R_seed**, shared by all pipelines.

Seeding is upstream and every spec-derived layer is regenerated from the seeded form. This is M1-R1, the Clean Program Assumption translated (Chekam, A; FT partial; Papadakis survey §9.6, B; FT y; the translation is *Inference*). Spec-derived oracles generated once from the clean spec are kept only as a **CPA-control** to show how much a naive design inflates S.

| Class | Generic type | Seed shape (clause- or row-level, behaviour-changing) | Real-mode anchor (brief §2) | Predicted strongest catcher (sign prediction, §3.3) |
|---|---|---|---|---|
| C1 Lost case | Omission | Delete a case-table row or a scenario branch; R_seed falls through to a default | — (NaPiRE: incomplete requirements top problem) | E |
| C2 Added commitment | Commission | Fix a value or order the records leave open | "decision text that went beyond what was answered" | E (only if E tests the open dimension by membership) |
| C3 Reinterpreted option | Rejected option adopted | Replace the clause with the record's documented rejected alternative | — (D1-R3 conceptual chaff) | E |
| C4 Wrong non-commitment type | Meta-level fact | Retag *unspecified* as *deliberately not promised*, or the reverse; R_seed realises the changed set | — | Neither (pre-registered "hard" class) |
| C5 Wrong environment exposure | Interface | Expose or hide an environment action or fault the records scope differently | — | Tie or S⁺ (G4a) |
| C6 Cross-table contradiction | Inconsistency | Change one cell so that the case table and the state × operation (or failure) table disagree | "tables that disagree"; "consistency checks that passed but missed a contradiction" | S⁺ (G3/G4/G4a) |

Basis: M1-R19 (mapping is *Inference*); Walia & Carver (A; FT partial) for the omission/commission vocabulary; NaPiRE (A-pre/B; FT partial) as a directional signal only; Just 2014 (A; FT y) for C3 and C6 being whole-clause rewrites, because invariant and algorithmic faults are the ones simple mutants miss (M1-R6, R10).

**Who seeds, and how many.**

| Set | Count | Seeders | Purpose |
|---|---|---|---|
| Pilot | 10 (≈ 2 per class, C4 or C5 once) | Mixed | Estimate p10, within-seed run correlation rho, minutes. **Excluded** from confirmatory analysis |
| Confirmatory misreadings | **60** (10 per class); 90 if the pilot rule in §2.6 fires | 5 per class by a **human seeder** (P2, or P3 if P2 rates); 5 per class by **LLM seeder Z** | Primary and secondary estimands |
| Spec-level allowed-variant seeds | 12 (2 per class shape) | 6 human, 6 Z | False alarms of spec- and record-side gates; tests the label process |
| R-level wheats | 2 screening + **24 held-out** | P2 writes; Z drafts, P2 completes | Screening (Pipeline A G2) vs measuring residual over-strictness (V) |
| Two-class combinations | 5 | Z | Coupling check (M1-R22), descriptive |
| Held-out **real** misreadings | All reconstructible, expected 3–10 | From records (O9) plus natural deviations found while auditing X's clean spec | Realism anchor; scored separately |
| Optional R-only stratum | 12 | Z | "Implementation misreading", never pooled (M1-R1) |

Seeders and models:
- The human seeder must not have seen the test families, the gate definitions or the arm assignments. This guards against seeder-knowledge bias (Gopinath, A; FT partial).
- Z is a provider used by **neither** arm (M1-R7, *Inference* from the correlated-error evidence of Kim et al., A; FT y).
- Seeder source is an analysis factor. If the ranking of the families flips between seeders, the result is seeder-dependent.

**Inclusion and filtering, frozen before any family runs.** These rules follow M1-R2, R5, R10 and R11 stage 1, and ACH's "misleading comment" artefact (A, industry; FT partial).
- Each seeder over-generates 1.5× per class.
- A seed is kept only if all of these hold:
  - well-formed, with one class and one locus;
  - it changes behaviour: R_seed and R_clean disagree on some Hypothesis-generated input inside the seeded clause's domain and on none outside it;
  - the four renderings agree, judged by a seeder-side reviewer who is not a rater;
  - it is not a comment- or rationale-only change;
  - it is not a duplicate of another seed after normalisation.
- The required count is then **drawn at random** per class, never by difficulty. This follows Gopinath's critique of Hutchins' selection; Hutchins is [unreachable].
- Seed order is randomised once, so that a stop at n/2 leaves a random half (M3 Q4).

**Realism checks.** None is validated for spec-level faults (M1 Q2 gap). All are reported, none is gating.
1. **Coupling to real items** (M1-R8, adapted from Just 2014 and Wang et al., A-pre; FT y). A real misreading is *coupled* if some seed is killed by a subset of the checks that kill it. Report Ochiai overlap of failing-check sets, with "high" at ≥ 0.8. That threshold is Wang's code-level one and is unvalidated here.
2. **Blinded realism rating** (M1-R9, R18). About 40 items, real and seeded mixed and stripped of provenance, go to both raters. Each item gets a plausibility rating and a "real or seeded?" guess. Near-chance discrimination supports realism.
3. **Class flags** (M1-R21). C4 and C5 have no real-mode anchor and are reported as "realism unanchored".
4. **Regeneration reversion.** If S⁺ catches a seed only because the regenerated model silently restored the record reading (a G6 mismatch at the seeded locus), report it separately. This is a sign the seed is unnatural (*Inference*).

### 2.3 Arms, information flow, lineages, independence verification

**Arms.** The brief's three family arms are **scoring rules over one set of runs**:
- E only;
- S only, reported both as S⁺ and as spec-enforcing tests only;
- both = E ∪ S⁺.

"Both" adds exactly p10 to S⁺. Both ⊇ S⁺ by construction, so p01(both vs S⁺) = 0 and McNemar is degenerate there (M3 Q1). It is reported as an estimate only.

**Pipelines.** A, B and **C′** are included. The literal C (Dafny → Python with a back-end DRT leg) is an optional extension only. The deep dive found it unrunnable in its environment and found 9 soundness bugs in the Dafny back-ends, with Python implicated (R-D3-3; ICST 2024, A). Its "R itself" variant collapses into A (deep dive §3.3). The subset is *Inference*.

**E-core is seed-independent.** The record-derived check set and the expectation suite never see the spec, so they are generated **once per run**, frozen, and executed against every R_seed. Only S-side layers are regenerated per seed (*Inference*). This makes E cheap and identical across pipelines.

| Pipeline | Seed injected into | S-side, regenerated per seed × run (lineage X, sees seeded artefact only) | E-side (record-derived) |
|---|---|---|---|
| **A** | Typed-slot spec | SMT encoding for G4/G4a/G4b; TLA+ for environment and history forms; spec-enforcing tests (Hypothesis `RuleBasedStateMachine`, contract → property); G0, G3, G5, G6 (vs R_seed), G7 (spec part), G9 | E-core (screened against 2 wheats, G2a); G2 added-commitment probe per changed clause by spec-blind judge W |
| **B** | First slot-filling (lineage X) | Common-logic translation of the seeded filling: G3, G4, G4a–G4c; G4d bounded run if under 1 h; G5; spec tests | Second slot-filling by Y from records (seed-independent, k = 3); diff witness at the seeded locus confirmed by judge W; E-core |
| **C′** | Quint source | Quint simulation and invariants; G4a as a contract query; G5; `--mbt` traces replayed against R_seed (G6); spec tests from traces | Regenerated prose from the seeded source, diffed against records by judge W; independent property set by Y (seed-independent) checked against the seeded source; DRT of R_seed vs **R2**, a second executable built by Y from records and screened like E; E-core |

**Who sees what.**

| Role | Lineage / person | Sees | Never sees | Sessions |
|---|---|---|---|---|
| Clean spec / filling / Quint source; R_clean | X | Records | E artefacts | Preparation, once; audited by P1 against records (deviations become *natural* real items) |
| Per-seed S-side regenerator | X | Seeded artefact, tool docs | Records, seed class, other seeds, E artefacts | Fresh per seed × pipeline × run |
| E-core author | Y | Records, register | Spec, models, R, seeds | Fresh, records-only read scope; prompts frozen and hashed **before the spec exists** (M2-R11); k = 5 |
| Same-lineage E control | X | Records only | As E-core | Fresh, k = 5. Tests whether swapping lineage matters |
| B second filling; C′ property set; R2 | Y | Records | Spec, source, R | Once (k = 3; R2 k = 1, screened) |
| LLM seeder | Z | Records, clean artefacts, taxonomy, inclusion rules | Test families, gates, arm assignment | Per batch |
| Judges (G2 probe; B diff; C′ prose diff) | W | Record clause plus candidate clause, order swapped | Arm, generator identity | 2 orders × k = 3 (M2-R12) |
| Ground-truth raters | P1 and P2 (P3 adjudicates) | Records, register, plain-language seed description and behaviour difference | Spec under test, arm, family, outcomes, judge verdicts | Blind batches, random order |
| Analyst | P1 | Dataset with arms relabelled A/B/C, frozen script | Key, until the analysis is frozen | Once |

Lineage rules (M2-R6):
- X, Y, Z and W come from different developers and, where possible, different base architectures (Kim et al., A; FT y; Goel et al., A; FT partial). Their evidence is from multiple-choice tasks, so the transfer is *Inference*.
- **Fallback with three providers.** W := Y. Judges then share a lineage with E-core, and that correlation is reported.
- **With two providers.** Human seeds only. The trial then cannot speak to lineage separation, and this is stated in the report.

**Independence is verified, not assumed.**

| Layer | Check | Can show | Cannot show | Basis |
|---|---|---|---|---|
| Information flow | File-system read scope per session; static import ban (G0); runtime trace of every tool call; canary GUIDs and invented helper names in spec, models and R, grepped in all E artefacts and traces | Verbatim or logged access. Any forbidden read **excludes that session** | Paraphrased leakage; shared training data; the operator channel | M2-R10; BIG-bench canaries (A; FT partial); Baltes §5.4–5.5 (A; FT y); deep dive D5-R2 |
| Operator channel | Byte-compare E prompts with the frozen, hashed file | Prompt edits after the spec existed | Unlogged hints | M2-R11 (*Inference*) |
| Outcome dependence | Per-seed caught/missed vectors for E vs S⁺, E vs E-control, Y-judge vs E. Geirhos error-consistency κ with a permutation null from the observed marginals | At n = 60 only gross dependence: the null band is about [−0.28, 0.27] at n = 50, acc 0.6 (own calc, M2). Report "dependence not detected", never "independent" | Moderate correlation | Goel §2 (A); M2-R7 |
| Shared derivation | Kill-set Jaccard against its chance value r₁r₂/(r₁ + r₂ − r₁r₂); identical (input, expected) pairs across families | Overlap beyond chance | Semantic copying | M2-R9 |
| Shared misreading | Share of seeds for which some E test **asserts the seeded reading**, i.e. E adopted the misreading. Compare E-core (Y) with the E-control (X) | Whether lineage swap changes adoption | Generality; Kim's both-wrong metric is not testable at this n (null band about [0, 1]) | M2-R8; Kim (A) |

### 2.4 Measures per gate and per arm

All gates run on every seeded version in **non-blocking mode**. "First gate to fail" is then derived from each pipeline's gate order, so that the full kill matrix exists (*Inference*).

| Measure | Definition | Reported per | Basis |
|---|---|---|---|
| **Catch** | A check fails on the seeded artefacts **and** passes on the clean artefacts and on the screening wheats. Run-level catches collapse to seed level by majority: ≥ 3/5 for E-core, ≥ 2/3 for the S side. "Caught in any run" is reported alongside | Seed × family × pipeline | M2-R1, R2; M3 Q1 (no pooling of runs) |
| **Attribution audit** | For 30 random catches, a human confirms that the failing assertion concerns the seeded clause | Family | *Inference* |
| **First gate to fail** | Earliest gate, in pipeline order, whose majority verdict fails | Seed × pipeline; class × pipeline table | Verified §4 cross-pipeline design |
| **Kills per family** | p10, p01, p11, p00 (E vs S⁺; E vs spec tests); raw and dynamic-disjoint kill rate (Algorithm 1 over the union kill matrix, as a sensitivity analysis) | Family, class, seeder | M1-R2; Papadakis survey §9.3 (B; FT y) |
| **Denominators** | Kills ÷ adjudicated misreadings (primary). Lower bound: "unknown" counted as misreading. Upper bound: "unknown" excluded. **Never** kills ÷ all seeds | All rates | M1-R13; LLMorpheus three-way label (A; FT y) |
| **Strength yardstick** | Kill rate of each family on 30 R-level operator mutants of R_clean, de-duplicated and adjudicated three-way | Family | M1-R3; Chekam threshold effect (A) |
| **False alarms** | (a) Baseline: checks failing on clean artefacts, before screening. (b) Catches of spec-level allowed-variant seeds. (c) Failures on clean artefacts per judge | Family, gate | M1-R12; deep dive G8 |
| **Over-strict tests** | Tests failing ≥ 1 of 24 **held-out** wheats; **RejectLegal** (share of held-out wheats rejected by the suite) reported with DetectFault. Contrast screening by 1 vs 2 wheats | Family, run | Deep dive D1-R1, D5-R3; ICER 2018 (A; FT y; TA) |
| **Judge precision / recall** | Stratified sample of 30 "violation" and 30 "fine" verdicts per judge role, built before results. Two blind raters. Wilson intervals with a CP check, weighted back by sampling fractions. Swap consistency; repetition stability | Judge role | M2-R12, R13; Zheng (A); CodeJudgeBench (A-pre); Shi (A); Thakur (A-workshop) |
| **Register auto-label audit** | Precision and recall of "maps to a register entry ⇒ allowed" against human labels | Class | M1-R11 stage 2; challenge §4.4 |
| **Human minutes** | Harness event log from "item displayed" to "verdict recorded", by category: seed, realise, label, adjudicate, triage test failure, judge calibration, harness fix. Protocol reading is timed separately. No think-aloud while timed. Item order randomised across arms | Gate, category, person | M2-R15; Ko et al. (A; FT y) |
| **Compute cost** | Tokens in, out and cached; list price on the day; wall-clock; tool calls. Fixed (prompt iteration, harness) separate from variable. Mean and range over runs. "Cost per caught misreading" only shown next to the count | Session, arm, pipeline | M2-R16; Kapoor (A-pre; FT partial); Baltes §5.8 (A) |
| **CPA inflation** | Catches by S generated from the **clean** spec on R_seed, minus catches by the regenerated S | Pipeline | M1-R1 |

### 2.5 Ground truth

Every seed and every wheat is labelled **before any family runs**, blind to outcomes (M1-R12). A killed seed that turns out to be an allowed variant is then an over-strict check, not a kill.

- **Label set.** {misreading of class c, allowed variant, unknown}, plus a pointer to the record clause relied on (M1-R16; LLMorpheus).
- **Operational rule** (M1-R17, *Inference*):
  - A seed is an **allowed variant** iff every behaviour it changes lies inside a register entry: another member of an unspecified set, or a deliberately-not-promised item.
  - It is a **misreading** if it permits what the records forbid, forbids what they require, or **changes a non-commitment's type**. A C4 seed is a misreading even if every concrete outcome stays allowed.
  - Behaviour unreachable under the declared environment is labelled "unknown". This is the strong sense of mutation, not the weak one (M1-R15).
- **Who labels.**
  - P1 and P2 label independently. P3 adjudicates; failing a P3, a recorded discussion decides.
  - A human seed is not labelled by its own seeder. If P2 seeded it, P1 plus an LLM rater of lineage W label it. W's agreement is reported as judge precision, **not** as ground truth (M1-R16.1).
  - With only one human available, every label-dependent measure is downgraded to "single-rater, unvalidated" (M2-R14).
- **What raters see.** Records, the register, and a plain-language description of the seed with its behaviour difference. They do not see the spec under test, the arm, the family, outcomes or judge verdicts. Zheng et al. found that showing human raters the judge's verdict changed their choice in 34 % of disagreements (A; FT partial).
- **Anonymisation.** Model names, file names and style markers are stripped from every artefact shown, which is formatted uniformly, and items get random IDs (M2 Q6; Romano et al., A; FT partial).
- **Rounds and thresholds** (Baltes §5.7, A; FT y).
  - The rubric is frozen after the 10 pilot items.
  - Rate in groups; compute Krippendorff's α and percent agreement per group; continue until α > 0.8 is sustained for 2–3 groups.
  - α < 0.667 means the class definitions are not operational. Revise them and re-label without touching kill data. α from 0.667 to 0.8 means results are tentative.
- **Uncertainty in α.** Report α with an interval. Own calc: with κ ≈ 0.8 and n = 60 items, the 95 % sampling range is about 0.56–0.95, wider than M1's rough "±0.15". A single point estimate near 0.8 is therefore not decisive, which is one reason for the sustained-rounds rule.
- **Top-up.** If fewer than 54 of the 60 confirmatory seeds are adjudicated misreadings, draw replacements at random from the same class's reserve and label them. Labelling precedes all runs, so the top-up is outcome-blind (*Inference*).
- **Blinding check.** After labelling, raters guess the arm for 20 random items. Report accuracy against chance with a Wilson interval (M2 Q6, *Inference* from clinical practice). Residual risk: P1 designed the arms, and Romano's interviewees judge blinding "less feasible" within one group.

### 2.6 Sample size and analysis

**n.**
- 60 confirmatory misreadings: 10 per class, 5 human and 5 LLM.
- **Pilot rule, fixed before registration.** If the pilot's p10 estimate is below 0.15, use n = 90 (15 per class).

Why 60 (all own calc unless stated):
- It is the smallest n at which a null result bounds p10 near the margin. With ≤ 1 E-only catch in 60, the two-sided CP upper bound is 0.089, so **refutation is attainable**.
- Support (CP lower bound ≥ 0.05) needs ≥ 8 E-only catches. Its probability is 0.25 at true p10 = 0.10, 0.70 at 0.15, 0.93 at 0.20 and 0.99 at 0.25.
- Classes of 10 are **descriptive only**: 5/10 gives CP [0.19, 0.81] (M3).

**Runs per configuration.**
- E-core: k = 5. It is generated once, so this is cheap.
- S side: k = 3 per seed × pipeline. Miller's variance factor (1 + 2/K)/3 makes the gain from K = 3 to K = 5 small (A-pre; FT y).
- Conditional rule: if the pilot estimates within-seed correlation rho > 0.8, S uses k = 1 (M3).
- Judges: k = 3 per verdict.

**Reconciling M1, M2 and M3.**

| Quantity | M1 | M2 | M3 | Choice and reason |
|---|---|---|---|---|
| Power at n = 36/48/60, 25 % E-only vs 5 % S-only | 0.51 / 0.68 / 0.80 (exact McNemar) | 0.50 / 0.67 / – (0.88 at n = 72) | Grid in psi/pi: psi 0.3, pi 0.8 gives 0.46/0.55 at n = 40 and 0.68/0.75 at 60 (exact/mid-p) | Recomputed here: exact 0.506 / 0.675 / 0.797, mid-p 0.609 / 0.755 / 0.851. **M1 and M2 agree.** M3's lower figures are for pi = 0.80, not 0.833. They are consistent, not conflicting. These figures matter less under the reframed, estimation-first primary |
| Primary test | Exact McNemar | Exact | Mid-p | **Mid-p** for H2. Fagerland et al. (A; FT y) recommend against the exact conditional test "in any situation" |
| Unit and aggregation | Per-seed probability over runs | Majority ≥ 3/5; "any run" separately | Fault-level rates primary; majority secondary | **Majority** for p10, since the estimand is binary per seed. Fault-level rate differences (paired t or sign test, cluster bootstrap) as sensitivity. Never pool runs: pooling inflates type I error to 0.11–0.32 (M3 sim) |
| Runs per configuration | 3–5 | 5 | 3–5; 1 if rho > 0.8 | E 5, S 3, conditional 1 (above) |
| Krippendorff bands | Wikipedia (D); primary wording unverified | Baltes §5.7 (A; FT y) | – | Use **Baltes**, which states the same bands from an A source. The D citation is dropped |
| κ precision | "roughly ±0.15" (own reasoning) | Wilson half-widths for judges | – | Own sim: about ±0.2 at n = 60 |
| Zero-catch upper bound, n = 60 | 0.06 (Wilson) | – | 0.049 (rule of three, one-sided) | **Two-sided CP 0.060** throughout; all criteria use two-sided CP |
| n | 36–60 | (not set) | ≥ 60, 80–120 preferred | 60, rising to 90 by the pilot rule. 80–120 is unaffordable in human labelling (§2.8) and adds little to an estimation-first primary |
| Interim look | – | – | O'Brien–Fleming plus Bayesian futility; efficacy looks "nearly useless" at psi ≤ 0.2, n ≤ 60 | **Futility only** (§2.8) |

**Planned comparisons.** These form a fixed sequence (H1 → H2 → H3), each at α = 0.05, stopping at the first non-rejection. That keeps family-wise α without splitting it (M3 Q2; *Inference*, since Holm and gatekeeping texts were not fetched).
- **H1** (primary): p10(E-core vs S⁺_A) jointly with V, using Pipeline A's S⁺. Pipeline A carries G4a/G4b (deep dive §3.3).
- **H2**: delta(E-core vs S⁺_A) > 0, mid-p McNemar.
- **H3**: p10(expectation tests vs spec-enforcing tests, Pipeline A) at **equal test counts**: 200 random subsamples to the smaller suite's size, with per-seed catch probability averaged. This follows the verified edition's G8 and M1-R3.

**Exploratory analyses,** reported with CP intervals and no confirmatory claims. Ten gates × three pipelines × six classes is 180 cells for about 60 seeds (M3).
- S⁺ unioned across A, B and C′ (the most severe comparator);
- per-pipeline p10 and first-gate-to-fail tables;
- per-class signs (§3.3) and per-seeder results;
- E-core vs E-control (lineage effect);
- CPA inflation;
- judge precision;
- register audit;
- realism coupling;
- minutes and cost.

**Blind analysis.**
- The script is frozen and hashed before unblinding, then run on A/B/C-relabelled data (Romano's account of Fucci et al.).
- Deviations are logged and **never justified by the data** (Empirical Standards RR, B; FT y).
- Pre-registration is a timestamped commit on the topic branch before the first confirmatory run (Ernst & Baldassarre, A; FT y).

### 2.7 Threats to validity and mitigations

| Threat | Mechanism | Mitigation in this design | Residual |
|---|---|---|---|
| **Seeding realism** | Seeds may not resemble real misreadings. Hand seeds carry seeder knowledge; LLM seeds bring duplicates, equivalents and comment-only edits (Gopinath, A; Wang, A-pre; ACH, A) | Two seeder sources as a factor; clause-level, behaviour-changing shapes; frozen inclusion and random draw; coupling and Ochiai to held-out real items; blinded real-vs-seeded rating; C4/C5 flagged unanchored; regeneration-reversion count | No validated spec-level realism metric exists (M1). The real set is 3–10 items, descriptive only |
| **Single operation** | Between-operation variance cannot be estimated; every interval is conditional on the operation (M3 Q5) | Operation drawn at random among qualifying candidates; claims worded "on operation X with protocol P"; replication plan: a 2nd operation, then a 2nd seeding lineage, protocol frozen (M3) | The dominant limit. No number of seeds fixes it |
| **Single maintainer** | P1 writes the records, picks the operation, labels and analyses. The operator can leak; blinding is weak within one group (Romano, A) | P2 as second rater and human seeder; P1 never labels P1-seeded items (none planned); frozen hashed prompts; blinding check; blind analysis | Cannot be removed. Stated in §4.1 |
| **Model drift** | Hosted models change; a format change moved one provider's executable-code rate from >50 % to 10 % (Chen et al., A; FT y) | Dated snapshot IDs; returned model string logged on every call; abort the configuration on change; runs of (arm × pipeline × run) blocks interleaved in random order; 5-seed **drift probe** at the start and end; runs confined to ≤ 2 weeks (M2-R17) | Subtle drift at n = 5 probe items |
| **Tool and harness bugs** | Extraction or formatting failures read as misses; flaky tests; young interop tools (deep dive: `itf-py` crash, `--mbt` labels) | Pre-flight sanity before any arm and after any harness change: known-good R passes; each family fails ≥ 2 hand-made known-bad R; identical artefact gives identical verdicts; second independent extractor on 10 replies; "does not compile or collect" is a **harness category**, never a miss (M2-R17) | Bugs in shared tooling, e.g. the SMT encoder, bias all pipelines alike |
| Correlated LLM errors | Same-developer and more accurate models agree more when wrong (Kim, A) | X ≠ Y ≠ Z ≠ W; E-control measures the lineage effect; outcome-level κ and adoption checks (§2.3) | Independence cannot be certified at n = 60 |
| Suite size and strength | Size drives kill counts; below threshold strength, criteria do not differ (Papadakis survey; Chekam) | H3 at equal counts; strength yardstick; a null is **uninformative** if either family kills < 50 % of yardstick mutants (threshold *Inference*) | The yardstick is R-level, not spec-level |
| CPA inflation | S built from the clean spec would "catch" what it never could (M1-R1) | Per-seed regeneration; CPA-control reported | None for this threat |
| Contamination | Public look-alike APIs; earlier reports | O10; canaries; optional renamed metamorphic copy for one E run (Sallou) | Training-data overlap undetectable |
| Learning effects in timing | One rater speeds up over time | Random item order across arms; first 10 items timed as calibration | Times generalise to no one else |

### 2.8 Budget and stop rules

Every figure below is either **derived** from stated counts or labelled an **assumption** (A1–A9).

| Item | Derivation | Person-hours |
|---|---|---|
| Operation scoring, records freeze, register audit | A1: 4 h | 4 |
| Audit of clean artefacts against records; natural misreadings logged | A2: 6 h | 6 |
| Human seeding | 44 seeds (half of 10 + 60 + 12 + 5, plus 1.5× over-generation absorbed) × 15 min (A3) | 11 |
| Realisation review (4 renderings agree) | 87 seeds × 3 pipeline forms × 3 min (A4) | 13 |
| Ground-truth labelling | (97 items + 26 wheats) × 2 raters × 7.5 min (A5 = M1-R14's 5–10 min, unsourced) = 30.8 h, + 30 % adjudication | 40 |
| Judge calibration | 3 roles × 60 verdicts × 2 raters × 3 min (A6) | 18 |
| Triage of checks failing on clean artefacts or screening wheats | ≈ 100 tests × 3 min (A7) | 5 |
| Attribution audit; realism rating; blinding check | 30 × 5 min + 40 × 2 × 3 min + 20 × 1 min | 7 |
| Harness build and sanity runs (fixed cost) | A8: 16–24 h | 20 |
| Pre-registration, analysis, write-up | A9: 12 h | 12 |
| **Total** | | **≈ 136 h** (P1 ≈ 80, P2 ≈ 50, P3 ≈ 6) |

Compute, all assumptions:
- Variable cost:
  - one S-side session ≈ 200k input + 40k output tokens;
  - one judge call ≈ 10k tokens;
  - one seeder rendering ≈ 50k tokens.
- **Full tier.** 87 seeds × 3 pipelines × k = 3 = 783 S sessions ≈ 188 M tokens. Judges: 87 × 3 × 3 × 2 orders × 3 reps ≈ 4,700 calls ≈ 47 M. E-core, E-control, B second filling, C′ property set and R2 ≈ 25 sessions ≈ 8 M. Seeding ≈ 13 M. **Total ≈ 256 M tokens.**
- **Core tier** (Pipeline A only; enough for H1–H3) ≈ 90 M tokens.
- Dollars = tokens × the price on the day. Illustratively, an assumed blended $4 per M tokens gives about $1,000 for the full tier and $360 for the core tier. Caching is not counted.
- Agent wall-clock: assuming 10 min per S session, 783 sessions ≈ 130 agent-hours, or about 16 h at 8 parallel sessions.

Calendar (*Inference*), 6 weeks:

| Week | Work |
|---|---|
| 1 | Operation, freeze, harness, clean artefacts |
| 2 | Seeding, labelling, pilot |
| 3 | Pilot analysis; registration commit |
| 4–5 | Confirmatory runs, interleaved and within ≤ 2 weeks for drift |
| 6 | Unblinding and report |

Human hours are the binding constraint. If only about 80 h are available, run the **core tier**: H1–H3 stay confirmatory and the pipeline comparison is dropped.

**Stop rules.**

| Rule | Trigger | Action | Counts as a look? | Basis |
|---|---|---|---|---|
| S1 Pre-flight | Any sanity check fails: harness, non-empty seed diff, clean artefacts pass both families, read-scope/import ban, model pins resolve | Abort, fix, log the deviation | No | M3 Q4; M2-R17; RR standard |
| S2 Calibration overrun | The first 10 labelled items take > 2× A5 per item | Cut seeds per class (to 8, n = 48, stated as reduced power) **before** dropping the second rater | No | M1-R14 |
| S3 Label reliability | α < 0.667 after two revision rounds | Stop. The taxonomy is not operational; report the taxonomy failure | No | Baltes §5.7 |
| S4 Protocol violation | A forbidden read in > 10 % of E sessions (A: threshold) | Stop and redesign isolation; violating sessions are always excluded | No | M2-R10 |
| S5 Futility | At n/2 = 30 confirmatory seeds, **0** E-only catches. CP upper bound 0.116; own calc: fires with probability 0.22 if true p10 = 0.05 and 0.001 if p10 = 0.20 | Stop; report "not supported, futility" | Yes (the only look) | M3 Q4, adapted to the p10 estimand |
| S6 Budget | Token use > 1.5× estimate, or human hours > 1.3× | Analyse at achieved n with the registered method; label the trial "budget-truncated" | No | M3 Q4 |
| S7 Drift | A pinned model is withdrawn or its returned ID changes | Stop that configuration; completed seeds form the trial; never mix versions | No | M3 Q4; Chen |

No efficacy stop. Under pi ≈ 1, an efficacy stop is near-certain early on and biases the estimate upward (Lakens, A; FT y). The estimand is the size of p10, not its existence.

---

## 3 Pre-registered hypotheses and refutation criteria

### 3.1 Confirmatory (fixed sequence H1 → H2 → H3; two-sided 95 % CP unless stated)

| ID | Hypothesis | Decision rule (n = 60) |
|---|---|---|
| **H1** | Record-derived oracles (E-core) catch real misreadings that every spec-only check of Pipeline A (S⁺_A) misses | **Supported** if the CP lower bound of p10 ≥ 0.05 (≥ 8 of 60) **and V holds** |
| **V** | E-core is not over-strict on legal behaviour | RejectLegal of the screened E-core suite on 24 held-out wheats has CP upper ≤ 0.25 (≤ 1 of 24: upper 0.211; 2/24 gives 0.270 and fails). Majority over 5 runs |
| **H2** | E-core catches more than S⁺_A overall | delta > 0, mid-p McNemar, α = 0.05; delta reported with a 95 % CI |
| **H3** | At equal test counts, expectation tests catch misreadings that spec-enforcing tests miss (verified G8) | CP lower bound of p10_narrow ≥ 0.05 on the subsample-averaged majority catch |

### 3.2 Refutation and outcome categories

| Code | Condition | Reading |
|---|---|---|
| **R1 Refuted (this operation)** | CP upper of p10 < 0.10 (≤ 1 of 60) **and** CI upper of delta < 0.05 **and** both families pass the strength yardstick (≥ 50 %) | "On operation X, record-derived oracles add < 10 % over all spec-only checks." Refutes the central claim's practical value here |
| **R1′ Uninformative null** | p10 low, but a family fails the yardstick or α < 0.8 | Not a refutation (Chekam threshold) |
| **R2 Inconclusive** | Neither supported nor refuted (2–7 of 60) | Report the estimate; no claim |
| **R3 Supported** | H1 and V | "Supported on seeded misreadings of operation X" |
| **R3′ Supported but over-strict** | H1 holds, V fails | **Not** support. E's catches may be over-strictness. Report the gap |
| **R4 External-validity guard** | The E-only catch rate on held-out real items (if ≥ 5) has a CP interval that excludes the seeded estimate | The seeded result is not generalised, even to this operation |
| **R5 Seeder dependence** | The sign of p10 − p01 differs between human and LLM seeds | The result is seeder-dependent; report both |

Severity in Mayo's sense, via Ernst & Baldassarre (A): the comparator includes the checks most likely to beat E (G3/G4a on C5/C6), and the registered predictions below can fail.

### 3.3 Exploratory sign predictions (registered, not tested for significance)

| Prediction | Falsified if |
|---|---|
| P1: p10 > p01 for C1, C2 and C3 | p01 ≥ p10 in any of them |
| P2: p01 ≥ p10 for C6; S⁺ first fails at G3/G4/G4a | E wins C6 |
| P3: C4 is caught by neither family in ≥ 50 % of seeds | Either family catches > 50 % |
| P4: E-control (lineage X) adopts seeded misreadings no less often than E-core (Y), i.e. lineage swap adds little | E-core adopts clearly less, with CIs not overlapping |
| P5: CPA inflation > 0 for S | Zero inflation |
| P6: Screening against 2 wheats leaves fewer over-strict tests than 1 wheat (deep dive D1-R1 overturn test) | Equal or more |
| P7: Register auto-labels have precision < 1 on C4 seeds | Precision 1 |
| P8: First gate to fail is earlier in B than in A for C6 | Not earlier |

---

## 4 Threats, limits and self-check

### 4.1 What this design cannot show

- **Real-misreading detection in general.** The confirmatory set is seeded, and no validated realism metric exists for spec-level faults. The held-out real set (3–10 items) is descriptive.
- **Any other operation, maintainer, project or model generation.** Between-operation variance is unestimated, and all intervals are conditional on operation X.
- **That lineages are independent.** Only gross dependence (|κ| ≳ 0.3–0.4) is detectable at n = 60.
- **A ranking of Pipelines A, B and C′,** or of gates. These are exploratory, with cells of ≤ 10 seeds. The literal Pipeline C is not tested unless the optional extension runs.
- **Equivalence or "no difference".** Bayes factors for a null stay < 5 even at d = 30 discordant seeds (M3).
- **Why E wins,** if it does. There is no mechanism measure beyond class signs.
- **Generalisable human-time costs.** One or two people, with learning effects.
- **Realism of classes C4 and C5,** which have no real anchor.
- **Leakage through paraphrase, training data or the operator.**
- **Detection of small effects.** If true p10 = 0.10, support has only a 25 % chance at n = 60.

### 4.2 Confidence per measure at the planned n

| Measure | Can show | Cannot show |
|---|---|---|
| p10 (E vs S⁺) | A large effect (≥ 0.20, P(support) 0.93), or a near-absence (≤ 1/60, upper bound 0.089) | The exact size (95 % CI width ≈ 0.23 at p10 = 0.25: 15/60 gives [0.15, 0.38]) |
| delta, McNemar | A direction when p01 is small | Small differences (p10 0.20 vs p01 0.10 has power ≈ 0.2 at n = 60; M1 table) |
| Per-class rates | Gross patterns (0/10 vs 10/10) | Ordering of classes (5/10: CP [0.19, 0.81]) |
| First gate to fail | Which gate dominates a class | Ranking of close gates |
| False alarms / RejectLegal (24 wheats) | "Under ≈ 21 %" at ≤ 1 failure | 2 % vs 5 % (M3: needs 40–60 probes for "< 7–10 %") |
| Over-strict tests, 1 vs 2 wheats | A gross reduction, as in ICER 2018 | A small one |
| Judge precision (30 per stratum) | Clearly bad (< 0.75) or clearly good (27/30: Wilson [0.74, 0.97]) | Differences between judges < 0.2 |
| Register audit | Systematic mislabelling of C4 | Precision on rare entries |
| κ and α | Gross failure of the taxonomy | Fine reliability (±0.2) |
| Error-consistency κ | Gross dependence | Independence |
| Human minutes; compute | Order of magnitude for this operation and these people | Generalisable cost; future prices (tokens are the stable unit) |
| Realism coupling | "No real item coupled" is a strong warning | "All coupled" is weak support |

### 4.3 Brief §2 weaknesses and how the design responds

| Weakness (brief §2) | Response |
|---|---|
| Thin evidence: "Spec-blind positive/negative checks rest on one A-pre study in a structural domain. Per-family mutant kills and the allowed-variant check are unmeasured inference." | H1 measures spec-blind record checks on a **behavioural** operation, with environment and history forms. H3 measures per-family kills. V and P6 measure the allowed-variant check. All are seeded and on one operation. The grade discrepancy is in §4.5 |
| Correlated LLM errors | Four lineages; same-lineage E-control; outcome-level κ; adoption-of-misreading counts (§2.3). Reported as "dependence not detected" at best |
| Seeded faults may not resemble real misreadings | Classes C2 and C6 mirror the three real modes; held-out real items, including natural deviations of lineage X; coupling; blinded rating; R4 guard |
| Over-strict tests | Membership predicates for open dimensions (deep dive D1-R2); held-out wheats; V as a **joint** condition for support; allowed-variant spec seeds |
| Equivalent mutants and intended weaknesses (IronSpec, MutDafny) | All seeds labelled before running; trivial-equivalence filter; register screen audited, not trusted; three-way human label; three denominators; LLM equivalence detectors only order the queue (Tian: prompted F1 ≈ 0.55, A; ACH recall 0.47, A, TA) |

### 4.4 Baseline challenges (quoted verbatim first)

1. **Auto-classification of survivors.**
   - The first report, §2.2: "Survivors that map to a registered non-promise are auto-classified "intended", which shrinks IronSpec/MutDafny-style triage."
   - Kept in the verified check map and the deep dive: "survivors mapping to the register auto-classified "intended"".
   - **Challenged** (*Inference*). Class C4 (wrong non-commitment type) produces seeds that *do* map to a register entry and are still misreadings. Auto-classification would hide exactly that class. The design treats the register label as provisional and measures its precision and recall (P7).
2. **"1.7 min per survivor" vs "~18 min/file".**
   - First report MutDafny row: "About 18 min per file; 1.7 min per survivor".
   - Verified edition: "~18 min/file".
   - The source note T4 reads: "Cost: about 18 minutes per file on average, and about 1.7 minutes of manual review per surviving mutant."
   - **Resolved as an omission, not a conflict.** Both figures come from the same note. The verified audit (V5-45) re-checked the counts (284 survivors from 24 files) but not the times, and the verified row simply dropped the per-survivor figure.
   - Own calc: 18 min × 24 files ÷ 284 survivors ≈ 1.5 min per survivor, close to 1.7. Both are plausibly the same manual effort in two units.
   - Unverified: whether "per file" includes tool runtime. MutDafny was not re-read in this run.
   - Neither figure is used for budgeting. Spec-level seeds need record reading, so A5 assumes 5–10 min, above the code-level anchors (Wang ≈ 1.35 min per mutant, own calc in M1; MutDafny ≈ 1.5–1.7).
3. **Verified edition, Pipeline A small trial.** "Seed 10–20 clause mutants that contradict the record (lost case, added commitment, reinterpreted option), regenerate R, and count kills per family at equal test counts."
   - **Challenged** on two points.
   - **(a) n.** With 20 seeds and zero E-only catches the CP upper bound is 0.168. ≤ 5 discordant seeds can never reach significance (M1, M3). 10–20 seeds can neither refute nor support.
   - **(b) Regeneration.** Regenerating R alone, with spec tests not regenerated from the seeded spec, is the CPA analogue and overstates S (M1-R1). Here every spec-derived layer is regenerated.
4. **Verified edition, cross-pipeline design.** "That yields the first direct measurement of whether prose-derived oracles catch what spec-derived ones miss." **Qualified.** It does so only for *seeded* misreadings on *one* operation, and only against the full spec-only side, given M3's near-triviality argument (§2.0).
5. **Verified R17 overturn condition.** "Seeded misreadings killed by both families near 100 % (no discrimination), or equivalent-mutant triage costing more than the findings (MutDafny: 157 of 284 equivalent)."
   - **Operationalised**, not challenged. H3 tests the first half.
   - Labelling minutes per adjudicated misreading, compared with minutes per E-only catch, tests the second half (exploratory).
6. **Verified edition on judges.** "the gate is calibrated on a human-labelled sample and recalibrated when the generating models change." **Qualified** (M2). At 30 labels per stratum, calibration bounds precision only to about ±0.1–0.2. Kaufman et al. (A-pre; FT partial) report 49 % human accuracy on incorrect assertions, so a single human labeller is not gold.
7. **Verified edition: "Swapping provider reduces correlation but does not remove it."** Adopted. P4 tests it on this operation.

### 4.5 Self-check: possible misreadings of the briefs, reports or notes by this run

1. **Reframing the comparator.** The brief's arms say "spec-enforcing family only". Making S⁺, all spec-only gates, the primary comparator may go beyond what the brief intended. The literal comparison is kept as H3. If the brief meant only tests, H3 is the answer and H1 is an addition.
2. **"Arms" as scoring rules.** I read "both" as the union of outcomes from shared runs, not as a separately generated configuration. If a jointly generated suite was meant, interaction effects are not measured.
3. **The brief's grade.** The brief says "one A-pre study". The verified edition raised Cunha & Macedo to A (FM 2026): "Grades raised to A: Cunha & Macedo (FM 2026)". I follow the verified edition. The design is unaffected.
4. **Pipeline C subset.** Dropping literal C follows the deep dive's strict reading of "single executable source". Under the looser reading in its §5.5, C′ *is* Pipeline C, and the subset is complete.
5. **E-core shared across pipelines.** This assumes that Pipelines A, B and C′ would deploy the same record-derived suite. In the verified edition, Pipeline A's record-derived set is written "before the spec exists", while B and C have their own expectation suites. Sharing one suite is an economy (*Inference*) that removes pipeline differences on the E side by design. Pipeline-specific E-side gates are scored separately.
6. **R_seed shared across pipelines.** One R patch per seed assumes R is built from the spec, not regenerated per pipeline. That isolates the oracles but does not test R-building fidelity.
7. **Held-out real items.** This assumes the three brief §2 modes can be reconstructed as artefacts (M1 self-check 1). If the records hold only descriptions, the real set reduces to natural deviations of lineage X, and R4 may never trigger.
8. **Thresholds** (0.05 and 0.10 margins, 0.25 RejectLegal ceiling, 50 % yardstick, 10 % violation stop) are design choices (*Inference*). No source fixes them.
9. **Budget assumptions A1–A9** are unsourced. The labelling rate dominates the total.
10. **Note limits inherited.**
    - Connor, Lachin, Holm, Brown–Cai–DasGupta, Andrews 2005, Papadakis ISSTA 2016, Hutchins and Sigweni–Shepperd are [unreachable]. Nothing load-bearing rests on them: intervals and power are own calculations.
    - The Empirical Standards' Experiments standard formally covers human-participant studies, so it is applied by analogy (M3).
    - The CPA translation is the note author's analogy, not Chekam's claim.
11. **Futility rule S5.** It is an adaptation by this run of M3's discordance-based rule to the p10 estimand. Its operating characteristics are computed here only for the stop probability, not for the overall error rates.

---

## 5 Sources with grades

FT reflects the note that read the source. Sources used only through earlier editions keep those editions' grades.

| Source | Grade | FT | Used for |
|---|---|---|---|
| Papadakis et al., "Mutation Testing Advances", Adv. Computers 112, [author copy](https://mutationtesting.uni.lu/survey.pdf) | B | y (§5.3, §9, §10) | Seven-point checklist; subsumption; strength; repetitions |
| Chekam et al., ICSE 2017, [PDF](https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf) | A | partial | Clean Program Assumption; threshold effect |
| Just et al., FSE 2014, [PDF](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf) | A | y | Coupling; uncoupled fault types |
| Gopinath, Jensen & Groce, ISSRE 2014, [PDF](https://rahul.gopinath.org/resources/issre2014/gopinath2014mutations.pdf) | A | partial | Seeder bias; selection bias; fault shape |
| Petrović et al., ICSE 2021, [arXiv 2103.07189](https://arxiv.org/pdf/2103.07189) | A | partial | Industrial coupling |
| Wang et al., LLMs for mutation testing, [arXiv 2406.09843](https://arxiv.org/pdf/2406.09843) | A-pre | y | LLM vs rule mutants; Ochiai; labelling cost; κ = 0.8 |
| Tip, Bell & Schäfer, LLMorpheus, [arXiv 2404.09952](https://arxiv.org/pdf/2404.09952) | A | y | Three-way label incl. "unknown" |
| Foster et al., Meta ACH, FSE Companion 2025, [arXiv 2501.12862](https://arxiv.org/pdf/2501.12862) | A (industry; TA) | partial | Trivially equivalent mutants; misleading comments; detector P/R |
| Tian et al., ISSTA 2024, [arXiv 2408.01760](https://arxiv.org/pdf/2408.01760) | A | partial | LLM equivalence detection F1 |
| Walia & Carver, IST 2009, [PDF](https://www.cin.ufpe.br/~in1037/AllFinal/SE63%20Walia%202009.pdf) | A | partial | Omission/commission vocabulary |
| Méndez Fernández et al., NaPiRE risk, [arXiv 1707.00144](https://arxiv.org/pdf/1707.00144) | A-pre/B | partial | Omission dominance (direction only) |
| Krippendorff, Computing α, [PDF](https://www.asc.upenn.edu/sites/default/files/2021-03/Computing%20Krippendorff%27s%20Alpha-Reliability.pdf) | B | y | α computation |
| Wikipedia, Krippendorff's alpha, [page](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha) | D | y | Superseded by Baltes §5.7 |
| Ouyang et al., TOSEM, [arXiv 2308.02828](https://arxiv.org/abs/2308.02828) | A | y | Non-determinism; 5 runs; low temperature |
| Atil et al., Eval4NLP 2025, [arXiv 2408.04667](https://arxiv.org/abs/2408.04667) | A-workshop | y (arXiv v5) | Variation at temperature 0 |
| Renze & Guven, Findings EMNLP 2024, [arXiv 2402.05201](https://arxiv.org/abs/2402.05201) | A | partial | Temperature effect (MCQA) |
| Sallou, Durieux & Panichella, ICSE-NIER 2024, [arXiv 2312.08055](https://arxiv.org/abs/2312.08055) | A-workshop | y | Repeated runs; metadata; renaming check |
| Baltes et al., LLM guidelines, EMSE accepted, [arXiv 2508.15503](https://arxiv.org/abs/2508.15503) | A | y (§§5.2–5.8) | Reporting pack; repetitions; judge validation rounds; α bands; cost |
| Kapoor et al., AI Agents That Matter, [arXiv 2407.01502](https://arxiv.org/abs/2407.01502) | A-pre | partial (§§1–3) | Cost accounting; 5 runs |
| Srivastava et al., BIG-bench, TMLR, [arXiv 2206.04615](https://arxiv.org/abs/2206.04615) | A | partial (canary) | Canary mechanism |
| Kim et al., Correlated Errors in LLMs, ICML 2025, [arXiv 2506.07962](https://arxiv.org/abs/2506.07962) | A | y | Lineage correlation; judge inflation |
| Goel et al., ICML 2025, [arXiv 2502.04313](https://arxiv.org/abs/2502.04313) | A | partial (§2) | Error-consistency κ |
| Zheng et al., MT-Bench, NeurIPS 2023, [arXiv 2306.05685](https://arxiv.org/abs/2306.05685) | A | partial | Swap protocol; 34 % change of mind |
| Jiang et al., CodeJudgeBench, [arXiv 2507.10535](https://arxiv.org/abs/2507.10535) | A-pre | partial | Test-generation judging hardest; order effects |
| Shi et al., AACL-IJCNLP 2025, [arXiv 2406.07791](https://arxiv.org/abs/2406.07791) | A | partial | Position bias; double-blind judging |
| Thakur et al., GEM 2025, [arXiv 2406.12624](https://arxiv.org/abs/2406.12624) | A-workshop | partial | Beyond percent agreement; leniency |
| Brown, Cai & DasGupta, Stat. Sci. 2001, [DOI](https://doi.org/10.1214/ss/1009213286) | A | n [unreachable] | Not relied on |
| Ko, LaToza & Burnett, EMSE 2015, [PDF](https://faculty.washington.edu/ajko/papers/Ko2013SEToolEvaluations.pdf) | A | y | Time-on-task definition |
| Chen, Zaharia & Zou, HDSR 2024, [arXiv 2307.09009](https://arxiv.org/abs/2307.09009) | A | y | Drift; format-induced harness failure |
| Romano et al., Euromicro SEAA 2020, [arXiv 2008.12528](https://arxiv.org/abs/2008.12528) | A | partial | Blind extraction and analysis; single-group limit |
| Sigweni & Shepperd, EASE 2015, [record](https://core.ac.uk/download/30339829.pdf) | A | n [unreachable] | Not relied on |
| Fagerland, Lydersen & Laake, BMC MRM 2013, [article](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91) | A | y | Mid-p McNemar |
| Connor 1987; Lachin 1992 | A | n [unreachable] | Not relied on (own enumeration instead) |
| Furia, Feldt & Torkar, IEEE TSE, [arXiv 1811.05422](https://arxiv.org/abs/1811.05422) | A | y | Prior sensitivity; multiplicity |
| Miller, Error Bars for Evals, [arXiv 2411.00640](https://arxiv.org/abs/2411.00640) | A-pre | y | Clustered errors; resampling gain; no pooling |
| ACM SIGSOFT Empirical Standards: [Experiments](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/standards/Experiments.md), [Registered Reports](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/RegisteredReports.md), [Sampling](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/Sampling.md), Benchmarking, Engineering Research, Quantitative Simulation | B | y | Pre-registration contents; deviations; object selection; repetitions |
| Kitchenham et al., EMSE 2017, [article](https://link.springer.com/article/10.1007/s10664-016-9437-5) | A | y | Effect sizes with CIs |
| de Oliveira Neto et al., JSS 2019, [arXiv 1706.00933](https://arxiv.org/abs/1706.00933) | A | y | Rarity of a priori power analysis |
| Ernst & Baldassarre, EMSE 2023, [DOI](https://doi.org/10.1007/s10664-022-10277-5) | A (editorial) | y | Registered reports; severity |
| Lakens 2014, Eur. J. Soc. Psych. (OSF author version) | A | y | Sequential looks; bias on early stop |
| Andrews et al. ICSE 2005; Papadakis et al. ISSTA 2016; Hutchins et al. ICSE 1994; Kurtz et al. 2014 | A | n [unreachable] | Only via Just, the Papadakis survey and Gopinath |
| Wrenn, Krishnamurthi & Fisler, ICER 2018, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/wkf-who-tests-testers/paper.pdf) | A (TA) | y (deep dive) | Single vs multiple wheats |
| Wrenn & Krishnamurthi, Examplar, ICER 2019, [PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/wk-examplar/paper.pdf) | A (TA) | y (deep dive) | Wheats for underspecified behaviour; hidden wheats |
| Cunha & Macedo, FM 2026, [arXiv 2510.23350](https://arxiv.org/abs/2510.23350) | A | y (earlier editions) | The spec-blind check evidence the trial tests |
| Konstantinou, Tambon & Papadakis, [arXiv 2607.05139](https://arxiv.org/abs/2607.05139) | A-pre | y (deep dive) | Fresh records-only session |
| Taherkhani et al., ConVerTest, ICST 2026, [arXiv 2602.10522](https://arxiv.org/abs/2602.10522) | A (TA) | y (deep dive) | Added commitments in invalid tests; allowed-variant filter |
| Goldweber et al., IronSpec, OSDI 2024, [USENIX](https://www.usenix.org/system/files/osdi24-goldweber.pdf) | A (TA) | y (earlier editions) | Intended weaknesses (13 of 61) |
| Amaral et al., MutDafny, [arXiv 2511.15403](https://arxiv.org/pdf/2511.15403) | A-pre (TA) | y (earlier editions; not re-read here) | Equivalent-mutant share; triage time |
| Kaufman et al., [arXiv 2607.08885](https://arxiv.org/abs/2607.08885) | A-pre | partial | Human accuracy on incorrect assertions |
| Donaldson et al., ICST 2024, [PDF](https://www.doc.ic.ac.uk/~afd/papers/2024/ICST.pdf) | A (TA) | y (deep dive) | Reason to drop literal Pipeline C |
| Own calculations: M1 (power, Wilson), M2 (κ, Jaccard and Kim null bands; Wilson/CP), M3 (power grid, Bayes, clustered runs, sequential), this synthesis (power recheck, CP thresholds, futility, κ spread) | own calc | n/a (scratchpad scripts) | Sample size, decision rules, stop rules |
