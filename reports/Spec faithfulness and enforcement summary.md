# Spec faithfulness and enforcement: where things stand (summary)

This summary consolidates four existing reports. It adds no new research and edits nothing earlier. Where the reports differ, the deep dive takes precedence over the verified edition, and the verified edition over the original. The trial design is a separate protocol. Citation keys:
- **[O]**: `reports/Spec faithfulness and enforcement.md` (original, superseded);
- **[V]**: `… verified.md`;
- **[DD]**: `… deep dive.md`;
- **[TD]**: `… trial design.md`.

Grades (A / A-pre / B …), *Inference* labels and transfer labels (*direct* = library/API behaviour specs, *analogous* = other spec domains, *inference*) are carried over from the cited report.

---

## 1. Current position

1. The earlier search found no published pipeline that runs prose records → spec → formal models → reference model with gates for faithfulness to the prose. That is a search result, not proof of absence [V §1, §2.6(c)]. The design is therefore assembled from analogues: spec-blind record checks written before the spec and screened against ≥ 2 allowed-variant "wheats"; cross-clause consistency that includes a per-operation response-existence check (G4a); and two test families separated by information flow, with kills compared at equal test counts [V §1; DD §1, §3].
2. **No recommendation rests on direct evidence of effectiveness for library or API behaviour specs.** Direct evidence exists only for mechanisms (Hypothesis, NonDex, link tooling and the like). The "own trials" are illustrative toys with n = 1 [V Part 3 §3.1; DD §5.1, §5.4].
3. **The central claim is still unmeasured**: that prose-derived oracles catch spec misreadings that spec-derived oracles miss. A one-operation trial is designed but has not been run. At n = 60 it could confirm a large effect (support with probability 0.93 if true p10 ≥ 0.20; own calc) or refute the claim for that one operation. It could not rank pipelines [V §1; TD §1].
4. Several sub-questions each rest on one source [DD §5.2, §5.3]:
   - Cunha & Macedo is the only study of spec-blind NL → test generation against wrong specs. Its 90 % is a per-requirement mean on Alloy structural models, and it presupposes a hidden correct oracle.
   - The benefit of multi-wheat screening comes only from the Brown PLT group, evaluating its own tools (TA).
   - The fresh-session effect (+11.7 %) comes from one A-pre study, on code, not specs.
   - Fonseca is the only independent source on where bridge defects sit.
5. Most confidences are medium to low (*Inference* from analogues). The "high" ratings attach to mechanisms or logic: table completeness, the rt-consistency relabel, running relaxed checks unrelaxed, and gate ordering. None attaches to measured yield [V Part 3 §3.1; DD §5.1].

## 2. Current gate sequence (G0–G9, as updated by the deep dive)

Ordering rules [V §2.4; DD §3.2]:
- Each gate blocks the next stage for the clause it covers.
- G5 must pass before any model-checking pass is trusted, and before a G4a *pass* is trusted, because a contradictory Inv makes G4a pass vacuously.
- G8 and G9 must follow G6.
- In Pipeline A, G0–G5 run before R is built, and the record check set exists before the spec does [DD §3.3].

"Blocks?" marks gates that must pass before later steps start. Confidence and transfer come from the recommendation IDs given. All gate cells are *Inference* that maps analogous evidence onto the brief's forms [V §3; DD §3].

| Gate | Checks | Catches | Earliest-failure role (forms) | Confidence; transfer | Blocks? |
|---|---|---|---|---|---|
| **G0** ID/schema lint (+ import ban) | IDs, form, typed non-commitment, declared domains. **New**: the expectation-test directory may not import R, spec helpers or models [DD §3.2] | Malformed or untyped slots; accidental access (leaky) | Variation points / profiles [V §3] | High for link mechanics, *direct* tooling (R16) [V 3.1]. Import ban: medium mechanism, low effect, *direct* toy (D5-R2) [DD §5.1] | Yes |
| **G1** Upward trace | Clause ↔ `decision~rev`; `OUTDATED` | Dangling or orphan links. Presence only, not binding | — | High mechanics; low for catching added commitments (R16) [V 3.1] | Yes |
| **G2** Faithfulness exhibition | Rejected scenario witnesses; rejected-option refutation; added-commitment probe. **New**: (a) record checks screened against ≥ 2 wheats; (b) conceptual chaffs must be killed; (c) chaffs that reject valid behaviour flagged; temporal clauses by candidate differencing [DD §3.2] | Lost, added or reinterpreted content; over-strict record checks | Formula over one instant (record checks drafted before the spec); register of non-promises; case-table slot-filling diff [V §3; DD §3.1] | Medium, *analogous* (R1, D1-R1). Rejected options as negatives: low, *inference*, unsourced (R2). Chaffs: low–medium (D1-R3) [DD §3.4, §5.1] | Yes |
| **G3** Form-local | Tables complete/disjoint; missing transition cells | Coverage gaps, some of them in the records themselves (Heitmeyer) | Case table; state × operation table; failure tables (G3 + G4a) [V §3; DD §3.1] | High (mechanism), *analogous*, decidable (R6) [V 3.1] | Yes |
| **G4** Conjunction | Unsat cores in k-subsets | Direct contradictions | Frame; history predicate if modelled in TLA+ [V §3] | Medium, *analogous*, all TA (R5) [V 3.1] | Yes |
| **G4a** Response existence | Per operation, relative to Inv: ∀ request ∃ allowed response; optionally per mode cell or profile value | Conflicts that plain SAT passes, e.g. a 3-clause error-precedence conflict (own trial) | Environment actions, every edit; cross-table failure conflicts [DD §3.1] | **Medium**, *analogous*; own trial is *inference* (D4-R1). Never applied to a store API [DD §2.4] | Yes, per edit (seconds) |
| **G4b** Inv preservation | Every environment action and allowed response preserves Inv | Invalid Inv under the environment | Supports G4a | Low–medium, *analogous* (D4-R4); no measured yield [DD §5.5 #10] | Yes |
| **G4c** Bounded confirmation | G4a counterexamples checked for reachability (TLC; Apalache with an explicit ∃) | Spurious counterexamples from unreachable Inv-states | Triage for G4a | Low–medium (D4-R4) | Yes |
| **G4d** Full checks | Full realizability for multi-step clauses; rt-consistency **for timed patterns only**; well-separation | Multi-step and timing conflicts | Termination under timeout (with G5) [V §3; DD §3] | Low, *inference* by analogy (R7). rt relabel itself: high (D4-R3) [DD §3.4] | No: nightly (hours) |
| **G5** Vacuity | Mutated invariant must yield a counterexample; smoke tests; sanity flags | Vacuous passes | Termination in the model (G4/G5) | Medium, *analogous* (R8). Order: high logical (R20) | Yes; before trusting G4/G4a passes |
| **G6** F ↔ R conformance | DRT/replay; trace validation. **New** `alpha` checks: Inv asserted before `alpha`; anti-identity; R mutants on non-projected fields; relaxed comparisons also run unrelaxed; membership where S leaves choices open [DD §3.2] | Model ↔ R divergence; partial-projection false passes | History predicate if not modelled; TraceLink-class termination defects [V §3] | Medium, *analogous* (R12, D2-R1). Run unrelaxed: high (D2-R4). Hypothesis driver: medium–high, *direct* mechanism. CrossHair low, **advisory** (R-D3-1) | Yes (CrossHair non-blocking) |
| **G7** Downward trace + coverage | Clause/scenario/row/branch coverage; generator health. **New**: per-action distribution statistics [DD §3.2] | Missing tests; omitted operations | — (presence check, not adequacy) | Medium–high, *analogous* (R18) | Yes |
| **G8** Per-family kill + allowed variants | R mutants killed by both families at equal test counts; tests failing a wheat; RejectLegal reported with DetectFault | Holes in either family; over-strict tests | Over-strict expectation tests (register) [DD §3.1] | Kill gate: low–medium, *inference* (R17). Allowed variants: medium (R15, D5-R3) | After G6 |
| **G9** Spec-strength mutation | A stronger clause variant still passes | Too-weak clauses | — | Medium–low, *analogous*, single source IronSpec (R19) | After G6 |

## 3. Pipelines A, B, C and C′

The deep dive keeps C′. All precedents are *analogous*, none on a library or API spec [V §4].

| Pipeline | Gate sequence (compressed) | Main failure modes | Feasibility today | Confidence |
|---|---|---|---|---|
| **A** Record-anchored, light formal core | G0 → record-derived check set written in a fresh records-only session under a file-system read scope, before the spec → spec → G1 → G2 (after screening against 2 wheats and a chaff set) → G3, G4, G4a/G4b, G5 → R built; G6 with a Hypothesis `RuleBasedStateMachine` driver, icontract/deal contracts, CrossHair advisory → G7, G8 → TLA+ only for environment and history forms, with histories checked via Porcupine (subprocess) or a calibrated detangle [DD §3.3] | ~4 % wrong tests *against one oracle*; the over-strict share is unbounded until multiple wheats screen it. Shared misreadings. Weaker cross-form conflict detection than B, partly recovered by G4a. Wheats or chaffs themselves wrong; curation cost grows with the variant space [V §4; DD §3.3] | Feasible in pure Python [DD §2.3] | Low–medium (P-A) [V 3.1] |
| **B** Common-logic consistency core | G0 → dual independent slot-filling + diff → G1 → one shared typed signature → G3 → G4, **G4a–G4c per edit**, **G4d nightly** → G5 → cores and witnesses kept as fixtures → G6–G9 [V §4; DD §3.3] | The translation is itself a faithfulness step. Solver UNKNOWN or timeouts. Mode variables defeat variable-sharing partitions of full runs (hours) but not the one-step G4a (seconds). Spurious G4a counterexamples (triaged by G4c). Unknowns under quantified invariants over handles. Costly initial formalisation [V §4; DD §3.3] | One-step checks measured in seconds by analogues (ProB 1.07–2.32 s on 855 guards; AGREE ≤ 1.762 s) [DD §2.4]. Agent translation rests on one short paper (n = 55) [V §4] | Medium for conflict detection; low for agent translation (P-B) [V 3.1] |
| **C** literal single source | Dafny → Python (pinned) + mandatory back-end DRT leg (Python vs C#/Java build) → prose/models generated → G2 prose diff → independent property set (mandatory) → expectation suite + N-version DRT → G5, G8/G9 [DD §3.3] | A misreading in the source propagates into every layer (confirmed by IronSpec, Fonseca I1, Sail vs Spike). Back-end miscompilation: 9 soundness bugs, Python implicated. The DRT leg cannot catch front-end errors [DD §2.3, §3.3] | Not run (no dotnet); readability and performance unmeasured [DD §5.4] | Low–medium (P-C) [DD §3.4] |
| **C′** Quint source + bridged R | Quint as executable source → seeded `--mbt` traces replayed against a separately written Python R through the split `alpha`, with an owned ITF decoder → G4a as a contract query → rest as C [DD §3.3] | Replay covers only simulator-reachable paths. Young interop tooling (`itf-py` crash; `--mbt` experimental) [DD §3.3] | Toy trial worked: 0/50 divergences for the correct R, 20/50 for a seeded R [DD §2.3] | Low–medium. If "single source" means one *formal* source, C′ *is* C [DD §2.6 #2, §5.5] |

## 4. What changed across editions

- **Cedar "§3 challenge" refuted as a misreading** of the earlier brief, which never tied Cedar to Dafny. **Porcupine challenge downgraded** to a qualification: one comparison, by competing-tool authors (CB), and no neutral benchmark [V Part 1 S1, S2].
- **Cunha & Macedo restated.**
  - [V S4]: a 90 % per-requirement mean (88 % pooled) over the 36 of 43 requirements with complete valid suites; one LLM; Alloy structural models; student-written wrong specs; regraded from A-pre to **A** (FM 2026).
  - [DD §2.1]: validity rests on a hidden oracle acting as a single wheat. The ~4 % wrong-test rate therefore does not bound over-strictness where records leave behaviour open (*Inference*). No temporal replication exists.
- **Independence weakened.**
  - Kills must be compared at equal test counts (Papadakis: r ≈ 0.05–0.20 with suite size controlled).
  - Information-flow isolation is necessary but not sufficient (Knight; Eckhardt & Lee).
  - LLM error correlation is measured only on multiple-choice tasks.
  [V S6–S8]
- **G4 split; G4a added; rt-consistency relabelled.** The ∀∃ check becomes a per-operation, Inv-relative one-step query, raised from low to medium. rt-consistency has no input/output split and is relabelled a timing check (high). Full realizability stays low [DD §2.4, §3.2, §3.4 R7].
- **`alpha` split.** "Reviewed `alpha`" as *the* cheapest decision becomes a reviewed, versioned observation relation plus a checked projection. The environment/fault model, logging and spec strength get equal review weight, because no independent source puts bridge defects in an abstraction function [DD §2.2, §2.6 #1, §3.4 R12].
- **Wheat/chaff screening added at G2**, and allowed variants at G8 are ≥ 2 wheats or NonDex-style perturbation. Evidence: single wheat → multiple wheats cut trusted suites, e.g. Nile 28 → 0 % (TA, deterministic functions) [DD §2.1, §3.1].
- **Pipeline C reshaped.** "R itself" is dropped because it collapses into A. The literal form is Dafny → Python with back-end DRT; the practical form is C′ (Quint) [DD §3.3].
- **Trial hypothesis reframed.**
  - The comparator becomes S⁺, every spec-only check, because spec tests regenerated from a misread spec catch it almost never.
  - The primary measure becomes an estimate of p10 with a validity condition V on held-out wheats.
  - The verified edition's 10–20-seed trial is rejected as unable to support or refute.
  - Auto-classifying register survivors as "intended" is challenged, because it would hide class C4.
  [TD §2.0, §4.4]

## 5. Top open questions and the measurement that would settle each

| # | Question | Settling measurement |
|---|---|---|
| 1 | Do record-derived oracles catch misreadings that every spec-only check misses? [V §5 Q1] | TD H1. **Support** if the CP lower bound of p10 ≥ 0.05 (≥ 8/60) *and* V holds. **Refute** for that operation if ≤ 1/60, the delta CI upper bound is < 0.05 and both families pass the strength yardstick [TD §3.1–3.2] |
| 2 | Does multi-wheat screening beat single-wheat screening on a stateful API, and how many wheats are needed? [DD §4; V §5 Q4] | TD P6: over-strict tests after 1 vs 2 wheats, checked on 24 held-out wheats (RejectLegal). The count needed stays open [TD §3.3; DD §4] |
| 3 | Does Cunha & Macedo's spec-blind result hold for temporal behaviour? | Run their protocol on the Alloy4Fun Trash/Train temporal sets against μAlloyτ's 90.8 % (D1-R6, "the single most useful new measurement") [DD §4] |
| 4 | Are G4a failures on a realistic store API mostly real or spurious, and do G4b/G4c add findings? [DD §4 new 4; V §5 Q5] | False-alarm rate of G4a with G4c confirmation on the trial operation, whose criterion O3 forces environment actions. First gate to fail for C5/C6 seeds (P2, P8; exploratory) [TD §2.1, §3.3] |
| 5 | How large is spec → test common-mode error, and does swapping lineage help? [V §5 Q14; DD §4] | E-core vs same-lineage E-control: adoption of seeded misreadings (P4) and outcome κ. Only gross dependence is detectable at n = 60 [TD §2.3, §4.1] |
| 6 | How often is `alpha` itself wrong in a test-based bridge, especially when agents write it? [DD §4 new 3] | False passes from R mutants on non-projected fields under agent-written projections vs with the D2-R2 checks (D2-R2 overturn condition). Not covered by the trial [DD §5.1] |
| 7 | Can register auto-labels be trusted, especially for wrong non-commitment types? | Precision and recall of "maps to a register entry ⇒ allowed" against human labels (P7) [TD §2.4, §3.3] |
| 8 | How precise are LLM faithfulness judges on API specs? [V §5 Q3] | 30 "violation" + 30 "fine" verdicts per judge role, two blind raters. This shows only clearly bad (< 0.75) or clearly good judges [TD §2.4, §4.2] |

## 6. Reading map

| Document | Holds | Status | Read for |
|---|---|---|---|
| `reports/Spec faithfulness and enforcement.md` [O] | First synthesis of T1–T5, the check map, Pipelines A–C | **Superseded** by [V] | Only to diff against [V]. Its Kernsatz overstates several claims (see V Part 1) |
| `reports/… verified.md` [V] | Corrected baseline: 160 checked claims; findings per track; disconfirming searches; gates G0–G9; check map; Pipelines A–C; open questions; source grades; confidences | **Current baseline**; §2.4, §3, §4 and Part 3 are partly updated by [DD §3] | What changed: Part 1. Evidence per method: §2.1–2.5. Disconfirming searches: §2.6. Open questions and debt: §5. Grades: §6. Recommendations and overturn findings: Part 3 §3.1 |
| `reports/… deep dive.md` [DD] | Wheats/chaffs (D1), `alpha` (D2), Python and single source (D3), response existence (D4), expectation independence (D5); updates to the check map, gates, pipelines and confidences | **Current, latest** | Current gates and pipelines: §3. Confidences: §5.1. Single-source dependencies: §5.2. Independence flags: §5.3. New debt: §4 |
| `reports/… trial design.md` [TD] | Protocol for a one-operation trial (60 seeds, 6 misreading classes, S⁺ comparator, H1–H3, budget ≈ 136 person-hours) | **Protocol, not run** | Why the hypothesis was reframed: §2.0. Seeds: §2.2. Information flow: §2.3. Decision rules: §3. Limits: §4.1–4.2 |
| `research_notes/Spec faithfulness and enforcement/` | T1–T5 track notes | Inputs to [O] | Details behind [O] |
| `research_notes/… verified/` (V1–V5, `verification_log.md`) | Verbatim evidence quotes; log of 160 rows (93 confirmed, 51 corrected, 2 refuted, 1 not found, 13 unverifiable) | Inputs to [V] | Checking any claim by log ID (e.g. V1-10) |
| `research_notes/… deep dive/` (D1–D5) | Track notes; own-trial details | Inputs to [DD] | Recommendation IDs (D1-R1 …) and own-trial set-ups |
| `research_notes/… trial design/` (M1–M3) | Mutation seeding, LLM evaluation protocols, small-n statistics | Inputs to [TD] | Power calculations and seeding rules (M1-R…, M3) |
