# Spec faithfulness and enforcement

## 1. Question

A library's core promise is a store with a stable API and stable observable
behaviour over several backends. Its behaviour is first decided in **prose
observation records**: per operation, a set of decisions, each with a concrete
scenario, options, a recommendation, the decision and a consistency note. The
records are the expectations, in the sense of expectation-driven design and
user acceptance testing.

From the records, mostly agents will produce a **normative spec**, **formal
models** and an **executable reference model**, plus tests.

**Assume the observation records are complete.** How can such a pipeline make
sure, as early as possible, that the spec and what is built from it are:

1. **Faithful**: the spec says what the prose says, nothing lost, added or
   reinterpreted. Checked against the prose itself, with the aim of
   *proving it wrong early*, not confirming it.
2. **Conflict-free**: no two clauses contradict, within one operation or
   across operations, also as clauses accumulate over time.
3. **Satisfiable**: at least one implementation can meet all clauses together,
   and no clause holds only vacuously.
4. **Enforceable**: two separate test families bind it.
   - **Spec-enforcing tests**: derived from the spec's clauses.
   - **Expectation tests**: derived from the prose records, independently of
     the spec, so that a misreading carried into the spec is caught, not
     confirmed.

The target of all tests in scope is the **executable reference model**.

## 2. Context (kept minimal on purpose)

- Each record decision has an axis it answers. Axes fix a *normative form*:
  - formula over one instant;
  - case table, which must be complete and disjoint;
  - frame (the unchanged set);
  - termination under a stated timeout assumption;
  - state × operation transition table for handed-out objects;
  - environment actions (concurrent caller, out-of-band actor, faults,
    cancellation);
  - history predicate over interval operations;
  - failure category, phase, effect and retry tables;
  - a register of deliberate non-promises;
  - variation points with a normal value and declared deviations per backend.
- Non-commitment is typed: *unspecified* (one of a stated set), *optional*,
  *deliberately not promised*, *profile-declared*, *indeterminate*.
  *Undefined* is not allowed.
- Formal layers currently in use or planned:
  - structured Markdown spec;
  - Dafny for per-call contracts;
  - TLA+ for lifetime, environment and bounded liveness;
  - Alloy and Lean 4 for static structure;
  - Python with pytest and Hypothesis.

  **This set is not fixed.** The research may recommend adding, dropping or
  replacing layers or tools.
- Observed failure modes so far, in prose records written and reviewed with
  agents:
  - decision text that went beyond what was actually asked and answered;
  - tables in different decisions that disagree with each other;
  - consistency checks that passed but missed a contradiction found later in
    review.

  These show the risk class the same translation step carries.
- Cross-backend conformance testing against real backends is **out of scope**
  here. It is a later task.

## 3. Already settled: build on, do not re-survey

A prior report, "Black box boundary spec methods (verified)", settled the
points below. Treat them as baseline. Challenge one only with new full-text
evidence, and say so explicitly.

- **Form rule.** Choose the checkable form by what a claim quantifies over:
  - finite case split → table checked complete and disjoint (or ACSL
    `complete`/`disjoint behaviors`);
  - value domain → executable oracle plus property tests;
  - call sequences on one resource → state-transition table plus stateful
    model-based tests;
  - interleavings → history predicate plus history checker, and a model
    checker for protocol design;
  - meta-property → proof;
  - profiles → typed schema plus one parameterised suite.
- **Contract shape.** One assume–guarantee contract in the Design-by-Contract
  lineage:
  - abstract state;
  - per-call cases;
  - typestate;
  - one environment clause;
  - history predicates;
  - narrow-only variation points (Liskov–Wing, SQL-92 GR 5, WebAssembly 3.0
    profiles).
- **Method families surveyed:**
  - DbC/JML/ACSL/Dafny/Larch/Spec#;
  - VDM/Z/B;
  - typestate and interface automata;
  - rely- and assume-guarantee, linearizability, TLA+/P;
  - client-centric consistency (Adya, Viotti–Vukolić, Crooks, Terry);
  - SCR tables and EARS;
  - ioco and MBT;
  - executable reference models (ShardStore, Cedar).

  Their industrial figures are verified.
- **Checking landscape.** What each form proves alone; ioco's treatment of
  unspecified versus nondeterministic outputs; history checkers (Elle,
  Porcupine, Knossos) and their cost.
- **Agent evidence:**
  - agents conform well to fixed, machine-checked specs (Vericoding,
    DafnyBench);
  - they game editable checks or checks stricter than the spec (ImpossibleBench,
    EvilGenie, Verus spec edits);
  - specs derived from code confirm the code (SpecGen);
  - intent-derived postconditions find bugs (nl2postcond);
  - triangular cross-checks help (Clover);
  - sampled-solution disagreement signals ambiguity (ClarifyGPT);
  - notation alone does not beat prose;
  - LLM-written system-level TLA+ is weak and grading-sensitive.
- **Seeds proposed there but not evidenced:**
  - one counterexample history per clause, kept as a *mutant reference model*
    the suite must kill;
  - at least two *witness* implementations with different profile values as
    a satisfiability argument;
  - a reference model that returns sets of allowed outcomes risks blow-up
    (ShardStore used a has-failed relaxation instead).
- **Items the prior report could not re-check.** They are in scope here
  where T3 needs them: Cirstea et al. (TLA+ trace validation), TraceLink,
  PObserve, Porcupine, arXiv 2409.14301 (multi-grained specs).

## 4. Tracks

One notes file per track. T1 to T4 in depth. T5 is minimal.

### T1. Faithfulness: prose → spec, proved wrong early

- How is a formalization validated against its natural-language source, as
  opposed to verified against itself? Look at:
  - back-translation and round-trip;
  - independent dual formalization plus equivalence or difference checking;
  - paraphrase review;
  - structured or controlled requirement languages used *as an intermediate
    step* (FRET/FRETish, EARS, Gherkin, decision tables), not as the final
    notation.
- Autoformalization of requirements and specs by LLMs: nl2spec, NL2LTL,
  NL2CTL, Req2LTL, SpecGen-style and others. What does each measure as
  "correct", and does that measure faithfulness to intent?
- **Validation by exhibition.** Animation, simulation and witness generation:
  ProB, Alloy instances, TLC and Apalache traces, Quint simulation, Hypothesis
  shrunk cases. Each turns a spec into concrete scenarios that a human or an
  independent agent can reject against the prose. Evidence that this finds
  translation errors, and at what cost.
- Clause-level faithfulness checks. How is it detected that a clause says
  *more* than its source decision (added commitment) or *less* (lost case)?
  What role can the record's own scenarios and options play as checks?
- Where in this step a human must look, and what is the smallest artefact
  that makes their check effective.

### T2. Conflicts and satisfiability

- Consistency across clauses written in **different forms**: tables,
  contracts, transition systems, history predicates, profile schemas.
  Multi-paradigm consistency rules (van Lamsweerde) and any implemented
  approach.
- Incremental consistency as operations and clauses accumulate. Cost and
  practice.
- **Realizability** of requirement sets (FRET's realizability analysis, GR(1)
  and reactive-synthesis checks) and what transfers to a library API with
  environment actions.
- **Vacuity and non-triviality**: vacuity detection in model checking, specs
  satisfied trivially, weak-spec findings in verification benchmarks. Gates
  that catch them.
- Satisfiability of contracts with SMT (Dafny, Why3, Frama-C) and of
  structural axioms with Alloy and Lean: what a "consistent" result does and
  does not show.
- The reference model, and two or more witness models, as constructive
  satisfiability evidence: what they prove, what they miss, and how many
  witnesses and how different they must be.

### T3. Two test families on the reference model

- **Spec-enforcing tests:**
  - tests generated from formal models (Quint and Modelator MBT, TLA+-based
    test generation, Dafny test generation, P);
  - contract → property tests;
  - stateful model-based testing;
  - history checking of concurrent histories on the reference model;
  - the environment's fault and cancellation actions as generated operations.
- **Expectation tests:**
  - specification by example, ATDD, BDD and acceptance testing used for
    *independent* derivation from prose;
  - how to keep this family from being derived from the spec or the model;
  - evidence that independently derived oracles catch more than spec-derived
    ones.
- **Conformance between layers:** formal model ↔ reference model ↔ spec.
  Differential random testing (Cedar), trace validation (Cirstea et al.,
  PObserve, TraceLink), refinement checks. Which pairs need a bridge, and
  which bridge is cheapest for which form.
- Oracles for non-commitment. Tests that accept exactly the allowed set
  (unspecified, indeterminate, profile-declared), neither stricter nor looser.
  Bounded outcome sets versus relaxation flags.

### T4. Adequacy and traceability

- Record decision → clause → model element → test links as **checkable
  data**, with gates that fail on a dangling or orphan link. Tools and
  evidence: Doorstop, sphinx-needs, OSLC, requirement-to-test trace
  recovery, LLM trace-link recovery accuracy.
- **Mutation of the spec and the models.** Mutate a clause, a model or the
  reference model, and require some test in the right family to fail:
  specification mutation, model mutation for TLA+/Alloy/Dafny, mutation
  testing of Python models (mutmut, cosmic-ray). Evidence that mutation score
  tracks real fault detection for specs.
- Coverage measures that fit:
  - clause coverage;
  - scenario coverage;
  - model state and transition coverage;
  - coverage of each non-commitment branch;
  - adequacy measures for property-based tests (generator coverage,
    distribution checks).
- How T1–T4 checks compose into one gate sequence, and which ones must run
  before any further step may start (*fail early*).

### T5. Independence (minimal)

Only as far as T1–T4 need it:
- common-mode error when one agent or prompt lineage reads, specifies,
  models and tests;
- evidence on independent derivations (N-version), adversarial or refuter
  roles, and the limits of LLM self-checking and LLM-as-judge for spec
  faithfulness.

No pipeline or organisation design beyond that.

## 5. Disconfirming searches

Run each and report the result:

- (a) Evidence that formal or structured intermediates **do not** improve
  faithfulness to natural-language intent over careful prose review.
- (b) Evidence that model-based or mutation-based adequacy measures fail to
  predict real defects for specs or models.
- (c) Any published pipeline that already does prose → spec → model →
  reference model with faithfulness gates. If one exists, compare against it
  instead of synthesising.

## 6. Evidence rules

- Verdicts rest on full texts. Search extracts are leads only. Label a source
  whose full text could not be fetched as **[unreachable]**, and your own
  reasoning as *Inference*.
- Grades:
  - A: peer-reviewed or measured. A-pre: arXiv preprint. A-workshop: workshop
    paper.
  - B: documented industrial practice with data, or normative standards and
    official docs.
  - C: practitioner report without data.
  - D: opinion or marketing.
- For each method, state whether **agents** were measured doing that step,
  with which result. Mark a method "human-only evidence" otherwise.
- Prefer measured figures. Give n, setting and what "correct" meant.

## 7. Deliverable

`reports/Spec faithfulness and enforcement.md`:

1. **Kernsatz**: at most three sentences.
2. **Per track (T1–T4)**:
   - the options with their evidence and grade;
   - what each catches and misses;
   - cost;
   - agent applicability.
3. **A check map.** For each normative form in § 2, which faithfulness,
   consistency, satisfiability and enforcement check applies, and at which
   point it can fail earliest.
4. **Candidate pipelines.** Two or three alternatives, kept open on layers
   and tools, each with:
   - its gate sequence;
   - its expected failure modes;
   - what a small trial on one operation would measure.

   No single prescribed pipeline.
5. **Open questions and verification debt** (unreachable, not re-checked).
6. **Sources** with grades.

## 8. Delivery

- Branch `research/spec-faithfulness-and-enforcement` from origin/main.
- Title: `Spec faithfulness and enforcement`.
- Follow the repository's CLAUDE.md for layout and running.
