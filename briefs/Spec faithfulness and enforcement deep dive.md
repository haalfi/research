# Spec faithfulness and enforcement deep dive

## 1. Task

Close the gaps the earlier report left. The earlier report is
`reports/Spec faithfulness and enforcement.md`, and it has a verified
edition if one exists on this branch. Prefer the verified edition where the
two differ.

Read the earlier brief, the report or reports, and their notes first. Do not
re-survey what they settle. Build on them, and challenge a point only with new
full-text evidence, quoting the point verbatim.

The setting stays abstract on purpose:
- prose observation records, each decision with scenarios, options and the
  decision;
- a normative spec;
- formal models;
- an **executable reference model in Python**;
- two test families: spec-enforcing and expectation tests.

Real backends are out of scope.

## 2. Known weaknesses of the earlier report

These motivate the tracks below.

- **Its core mechanism rests on one study.** The mechanism is spec-blind
  positive and negative checks derived from the prose, with rejected options
  used as negatives. The study is Cunha & Macedo (A-pre): Alloy, structural
  specs, student errors. Using rejected options as negatives is the report's
  own inference.
- **Weak domain transfer.** Most evidence comes from LTL/FRET requirements,
  maths in Lean and Alloy teaching. Transfer to a library API behaviour spec
  is inference throughout.
- **It names a reviewed abstraction function** `alpha(reference-model state
  → spec state)` as "the single cheapest structural decision", and the likely
  place agents cut corners. It does not research it.
- **It concedes that mode variables defeat partitioned consistency checks**
  for a store API (handle state, profile, lifecycle), and that GR(1)
  realizability fits neither data nor interleavings. It offers no
  alternative.
- **Python-native tools were not fetched** (CrossHair, deal). A single
  executable source for Pipeline C was left open.
- **It misread its own brief once** (a spurious Cedar "challenge"). Treat
  every baseline challenge with the same care.

## 3. Tracks

One notes file per track.

### D1. Examples-first validation against correct and wrong implementations

- **Wheats and chaffs:**
  - Wrenn & Krishnamurthi's Examplar and its follow-ups;
  - Forge's `example` and `test expect`;
  - Alloy4Fun follow-ups;
  - any similar method for checking examples or tests against correct and
    deliberately wrong implementations or specs.
- **Measured results:**
  - detection of wrong specs or tests;
  - over-strict examples;
  - cost;
  - agent use.
- **Transfer to behaviour specs.** Evidence for temporal, stateful or
  concurrent behaviour, not only structure. Does the mechanism carry the
  allowed-variant check (no test fails on an allowed variant) and the
  forbidden-variant check (some test fails on each disallowed variant)?
- **Replication of Cunha & Macedo**, or a measured equivalent, in any
  behavioural domain.
- **Rejected alternatives as negatives.** Any study that derives negative
  tests from documented design alternatives or decision records.

### D2. The abstraction function between reference model and spec

- How abstraction functions and refinement mappings are written, reviewed
  and validated in practice. Look at ShardStore, Cedar, IronFleet and
  Verdi-style refinement, TLA+ refinement mappings, and Hypothesis or
  QuickCheck model-based tests with an explicit abstraction.
- Failure modes of the abstraction function itself, and checks for it:
  - surjectivity and coverage;
  - observational equivalence;
  - hidden state outside it;
  - agent-written mappings.
- Keeping it stable as the spec grows.

### D3. Python-native and single-source options

- CrossHair, deal, icontract and icontract-hypothesis, Hypothesis stateful
  testing, and Python history checkers or Porcupine bindings: capability,
  maturity and measured effectiveness.
- **One executable source.** For each of Dafny compiled to Python, Lean,
  Quint and P, whether it can serve as the reference model or generate it.
  Measure:
  - fidelity of the generated code;
  - performance;
  - usability as an oracle.
- Which choice makes **Pipeline A** (light formal core) or **Pipeline C**
  (single source plus an independent check set) feasible.

### D4. Consistency for data-rich APIs with environment actions

- Alternatives to GR(1) realizability for "for every environment move,
  some allowed response exists": TLA+/Apalache `ENABLED` and deadlock checks,
  rt-consistency, Alloy temporal checks, SMT over bounded traces.
  Precedents on APIs or storage systems.
- How mode variables are handled without losing locality, or evidence that
  only full runs work. Cost at scale: tens of operations × tens of clauses.

### D5. Independence of the expectation family (minimal)

- Mechanisms for enforcing information flow in agent pipelines:
  - context isolation;
  - read scopes;
  - lint that no expected value is computed by the reference model;
  - detectors for added commitments in LLM-written acceptance tests.
- Measured results only. No organisation design.

## 4. Disconfirming searches

- (a) Evidence that examples-first validation fails, or is too costly, for
  behaviour specs.
- (b) Evidence that a reviewed abstraction function does *not* reduce
  bridge defects.
- (c) Evidence that single-source pipelines miss more intent errors than
  separately authored layers.

## 5. Self-qualification (mandatory)

The run must state and qualify its own findings:

- **Every finding** carries:
  - grade;
  - full text read (yes or no);
  - n and setting;
  - what "correct" meant;
  - a **transfer label**: *direct* (library or API behaviour specs),
    *analogous* (other spec domains) or *inference*.
- **Source independence.** Flag tool authors evaluating their own tool, and
  vendor posts.
- **Baseline challenges.** Quote the challenged text verbatim before any
  challenge or qualification of the earlier reports.
- **Every recommendation** gets confidence high, medium or low, the
  load-bearing sources it depends on, and the one finding that would overturn
  it.
- **Coverage gaps.** Name any track or sub-question where only one source
  carries the answer.
- **Sections required:**
  - "What this run did not do";
  - "Self-check": possible misreadings of the brief or a source by this run.

## 6. Deliverable

`reports/Spec faithfulness and enforcement deep dive.md`:

1. **Kernsatz**: at most three sentences, qualified.
2. **Per track (D1–D5)**: for each option, its evidence, what it catches and
   misses, cost, agent applicability and transfer label.
3. **Updates to the earlier report:**
   - check map;
   - gate sequence;
   - Pipelines A, B and C.

   State which cells change and why.
4. **Open questions and verification debt.**
5. **Self-check and limits** (§ 5).
6. **Sources** with grades.

## 7. Evidence rules

The same as the earlier brief §6:
- full texts only;
- **[unreachable]** and *Inference* labels;
- grades A, A-pre, A-workshop, B, C, D;
- agent applicability stated per method.

## 8. Delivery

- Branch: `research/spec-faithfulness-and-enforcement` (existing topic
  branch).
- Title: `Spec faithfulness and enforcement deep dive`.
- Follow the repository's CLAUDE.md.
