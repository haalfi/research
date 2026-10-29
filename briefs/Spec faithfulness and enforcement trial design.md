# Spec faithfulness and enforcement trial design

## 1. Task

Design, but do not run, a small trial on **one operation** that directly
measures the central claim the earlier reports left unmeasured:

> Oracles derived from the prose records catch spec misreadings that oracles
> derived from the spec miss.

Also compare the candidate pipelines' gates on the same faults.

Read first:
- the earlier brief;
- `reports/Spec faithfulness and enforcement.md`;
- its verified and deep-dive editions if they exist on this branch;
- their notes.

Prefer the latest edition where they differ.

Research here means experimental method only:
- mutation analysis methodology;
- fault seeding and its validity threats;
- equivalent-mutant handling;
- evaluation protocols for LLM-generated tests and specs;
- sample-size reasoning for small n.

Do not re-survey spec methods.

## 2. Known weaknesses the design must account for

- **Thin evidence for the design's assumptions.** Spec-blind
  positive/negative checks rest on one A-pre study in a structural domain.
  Per-family mutant kills and the allowed-variant check are unmeasured
  inference.
- **Correlated LLM errors.** They are stronger within one provider and among
  more accurate models, so separating lineages by swapping models may not
  give independence.
- **Seeded faults may not resemble real misreadings.** The earlier records
  show real failure modes:
  - decision text that went beyond what was answered;
  - tables that disagree;
  - consistency checks that passed but missed a contradiction.
- **Over-strict tests.** Expectation tests can fix values a decision leaves
  open.
- **Equivalent mutants and intended weaknesses** dominate triage costs in
  comparable studies (IronSpec, MutDafny).

## 3. What the design must specify

1. **Choice of the operation**, by criteria only. It must exercise:
   - a case table;
   - a state × operation table;
   - environment actions;
   - a history predicate;
   - non-commitment types;
   - profiles.
2. **A misreading taxonomy and seeding protocol.** At least:
   - lost case;
   - added commitment;
   - reinterpreted option (a rejected option adopted);
   - wrong non-commitment type;
   - wrong environment exposure;
   - cross-table contradiction.

   Specify who seeds (an independent lineage, a human, or both), how many,
   the realism checks, and a held-out set of *real* misreadings if any exist.
3. **The arms.** Spec-enforcing family only; expectation family only; both.
   Include **Pipelines A, B and C**, or a justified subset. Specify:
   - each arm's information flow, i.e. who sees what;
   - lineage and model assignment;
   - how independence is verified, not just assumed.
4. **Measures per gate and per arm:**
   - first gate to fail;
   - kills per family;
   - false alarms;
   - over-strict tests (allowed-variant check);
   - judge precision against human labels;
   - human minutes;
   - compute cost.
5. **Ground truth.** How "is a misreading" and "is an allowed variant" are
   decided, by whom, and blind to which arm.
6. **Sample size and analysis.** What n gives a usable signal. Which
   comparisons are planned. What result would refute the central claim.
7. **Threats to validity** and their mitigations: seeding realism, single
   operation, single maintainer, model drift, tool bugs.
8. **Budget and stop rules.** Hours, tokens and calendar time. When to stop
   early.

## 4. Self-qualification (mandatory)

The run must state and qualify its own design:

- **Every design choice** cites its methodological source (grade, full
  text read) or is labelled *Inference*.
- **Confidence per measure**: what it can and cannot show at the planned n.
- **Baseline challenges.** Quote the earlier report verbatim before any
  challenge to it.
- **Sections required:**
  - "What this design cannot show";
  - "Self-check": possible misreadings of the briefs or reports by this run.

## 5. Deliverable

`reports/Spec faithfulness and enforcement trial design.md`:

1. **Kernsatz**: at most three sentences.
2. **Trial protocol**: the § 3 items, ready to execute.
3. **Pre-registered hypotheses and refutation criteria.**
4. **Threats, limits and self-check** (§ 4).
5. **Sources** with grades.

## 6. Evidence rules

The same as the earlier brief §6:
- full texts only;
- **[unreachable]** and *Inference* labels;
- grades A, A-pre, A-workshop, B, C, D.

## 7. Delivery

- Branch: `research/spec-faithfulness-and-enforcement` (existing topic
  branch).
- Title: `Spec faithfulness and enforcement trial design`.
- Follow the repository's CLAUDE.md.
