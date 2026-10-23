# Research report: specifying observable behaviour at a black-box boundary

> **Provenance.** An independent second run on the same brief as the run on
> branch `research/black-box-boundary-spec`. It was run in ChatGPT deep
> research on 2026-10-23, not in this repository. Shared result:
> https://chatgpt.com/s/t_6adb2684b1ec8191a63dd80f34ab1e86. Extracted from the
> share page's rendered Markdown. Link tags became Markdown links and layout
> markup was removed. Its inline citation markers pointed at internal search
> references and could not be resolved, so they were dropped; the reference
> table at the end is the only source list. The report itself grades no
> sources and records no verification pass. The brief is
> `briefs/Black box boundary spec methods (second run).md`, a byte-identical
> copy of the first run's input.

Research scope: specification theory, contract design, model-based conformance, and empirical evidence from AI coding agents. Sources reviewed through 23 October 2026.

## Executive conclusion

**The strongest foundation is a category-directed behavioural contract, grounded in Design by Contract and given its deeper semantics by observable traces, environment assumptions, and behavioural refinement.**

It should not be one large formal specification, one collection of axioms, one machine-readable schema, or one set of tests.

The method should have five characteristics:

1. **One normative boundary contract:** independently stated obligations about what an observer may see, not how implementations achieve them.
2. **Category-specific forms:** state predicates for structure, relations for input/output behaviour, transition rules for resource lifetimes, and histories or temporal properties for concurrency.
3. **Explicit environment assumptions:** named observers and outside actions, including interference and failures, are part of the contract's domain.
4. **Bounded declarative profiles:** each implementation reality selects values from explicitly defined variation points; profiles do not introduce independent versions of the contract.
5. **Independent conformance evidence:** each normative claim has a counterexample and a checking obligation. Tests, executable models, and proofs are selected according to what the claim needs.

The core distinction is between **the specification's authority, its representation, and its verification**. These are related but should not be collapsed.

A human-readable clause can be authoritative without being executable. An executable model can be valuable without being a complete contract. A test can check a contract without defining it.

### Theoretical basis

This recommendation combines established methods rather than proposing a new foundational formalism.

| Established method | Contribution to this problem | Limitation |
|---|---|---|
| Design by Contract | Caller assumptions, supplier guarantees, and invariants | Ordinary pre/postconditions are insufficient for cross-call histories |
| Abstract data types and relational specifications | Implementation-independent meaning of operations | A relation for one call does not capture every temporal guarantee |
| I/O automata and interface automata | Observable actions, environmental interference, assumptions and guarantees | A complete automaton for every operation is unnecessarily expensive |
| Trace semantics and behavioural refinement | Which observable histories are permitted, prohibited, or required | Untimed traces alone cannot express every failure, progress, or resource property |
| Model-based conformance testing | Systematic checking of a black-box implementation against an independent model | Test executions provide evidence, not universal correctness |
| Temporal logic and formal refinement | Precise treatment of safety, progress, and concurrency | Modelling expertise and proof cost can exceed the needs of simple clauses |

These foundations are not interchangeable. Eiffel's Design by Contract explains obligations between a caller and supplier. De Alfaro and Henzinger's interface automata explicitly distinguish assumptions about the environment from component guarantees. Herlihy and Wing's linearizability uses invocation/response histories to formulate a particular concurrency guarantee. Tretmans' `ioco` theory supplies a formal approach to black-box conformance testing. 

**The principal research finding is therefore not that the project needs a more powerful specification language. It needs a disciplined rule for choosing the weakest adequate form for each category, while preserving a common observational meaning across those forms.**

That is the foundation for the recommendations below.

## 1. What is being specified?

The object of specification is not the implementation, and not merely a mapping from arguments to return values.

It is the library's **externally observable behaviour in an admissible environment, under a declared profile**.

That distinction matters because the boundary exposes more than completed calls. It exposes the order of events, whether effects survive failures, which resources remain usable, and what different observers can establish.

### 1.1 The observational model

The foundation should explicitly name three roles:

| Observer or actor | Relevant observations and actions |
|---|---|
| **Caller A** | Invokes operations; receives results or errors; can use and release resources; can observe effects through later calls |
| **Concurrent caller B** | Invokes overlapping operations; receives independently ordered outcomes; may detect inconsistencies between observations |
| **External actor X** | Reads or changes the underlying store independently of the library, subject to stated environmental assumptions |

A and B are observers of the library API. X has a different role: it can cause environmental changes, and may independently observe effects at the underlying store. What X can observe must be defined separately from what A and B can observe.

This resembles the I/O automata model of Lynch and Tuttle, which distinguishes actions controlled by a component from actions controlled by its environment. Interface automata extend this perspective by expressing the assumptions an interface makes about acceptable environmental actions. 

A conceptual event vocabulary might include:

```text
A invokes operation
B invokes operation
X changes external state
A receives result
B receives error
A uses resource
A releases resource
```

This is not an implementation design. The events represent potentially observable occurrences. It is also not a decision that these events must have any particular ordering.

The foundation must decide which ordering constraints are guaranteed, which are conditional, and which are not specified.

### 1.2 A minimal mathematical interpretation

Let:

- \(p\) be a declared reality profile;
- \(E_p\) be the set of admissible environmental behaviours;
- \(O\) be the named observer set;
- \(H\) be a complete execution history, including any relevant internal events;
- \(\pi_O(H)\) be the history projected onto events visible to those observers;
- \(C_p\) be the set of permitted observable histories under profile \(p\).

Then a core safety-conformance condition is:

\[
\forall e\in E_p:
\quad
\operatorname{Obs}(\operatorname{Impl}\parallel e)
\subseteq C_p(e)
\]

In words: for every environment satisfying the declared assumptions, the implementation must produce only behaviour permitted by the contract for its profile.

This is a synthesis of trace-based refinement and assume/guarantee contract reasoning, not a proposal that the project write this formula in every spec.

The subset relationship has two important consequences.

First, the contract may permit multiple outcomes without demanding that every implementation produce every outcome. Permitted nondeterminism is different from a required behaviour.

Second, the contract must not accidentally guarantee behaviour merely because one implementation happens to exhibit it.

**Progress requires separate treatment.** A safety trace model can forbid bad completed outcomes but may allow an operation never to complete. If eventual completion, deadlock freedom, or a deadline is promised, that requires an additional progress or timed obligation and explicit environmental assumptions.

CSP's distinct trace and failures-divergence refinement models, as well as TLA's distinction between safety and liveness, provide established foundations for making that separation. 

### 1.3 Three meanings that must not be confused

| Status | Meaning | Consequence |
|---|---|---|
| **Required** | Every conforming implementation must satisfy this claim under its stated conditions | Violation is a contract failure |
| **Permitted** | This behaviour is allowed, possibly among other behaviours | A caller cannot infer that it will always occur |
| **Unspecified** | The contract deliberately imposes no additional constraint on this dimension | The implementation may vary, subject to all other obligations |

A fourth status, **undecided**, is useful during research and drafting. It is not a finished specification.

For example, no latency guarantee does not imply that latency is invisible. It means that the normative contract provides no upper latency bound. Nor does it remove a separately specified ordering or resource-safety guarantee.

The same discipline applies to request counts, memory usage, buffering, retries, caching, and internal scheduling.

An explicit `UNSPECIFIED` declaration is valuable even though it does not constrain the implementation. It constrains the authors, tests, and downstream documentation against silently inventing a promise.

---

## 2. Category → level → form

This is the central design decision.

A category identifies **the kind of claim being made**, not the file in which it happens to appear or the operation that happens to motivate it.

A single operation may be governed by several categories. Those categories should not be collapsed into one oversized operation specification.

### 2.1 Recommended category taxonomy

| Category | Correct abstraction level | Observer / time / environment / reality binding | Preferred normative form |
|---|---|---|---|
| **S — Structure** | Valid states and identity relationships at one instant | No observers or time; reality-independent | Axioms and mathematical predicates |
| **V — Values and relations** | Valid inputs, outputs, equality, normalization or relations between values | Logical input/output observation; normally no temporal environment | Equations, predicates, or relational definitions |
| **C — Single-call obligations** | Trigger, admissible call, outcome and effects attributable to an operation | Named caller, call boundary, relevant before/after conditions | Atomic structured prose clauses, with decision tables for cases |
| **F — Errors and partial failure** | Classification of failures, visibility, effect certainty and retry-relevant facts | Caller plus any observer that can detect effects; distinguish failure phases | Classification/decision tables plus individual obligations |
| **L — Resource lifecycle** | Legal observable transitions during the lifetime of a returned object or handle | Resource holder and possibly other observers; explicitly temporal | Transition table or protocol state machine |
| **E — Environment assumptions** | External actions and conditions under which guarantees apply | A, B and X; interference and failure scenarios | Assume/guarantee clauses and an external-action vocabulary |
| **H — Cross-observer histories** | Allowed ordering, consistency, visibility and progress properties | Several observers, time, overlapping events and environment | History predicates; lightweight formal model when necessary |
| **P — Reality profiles** | Selection of predefined variation points and capabilities | Reality-bound, but without implementation mechanisms | Schema-validated profile data referencing common rules |
| **U — Explicitly unspecified dimensions** | The limits of the contract's promises | Only enough context to identify the dimension and scope | Explicit non-promise register with stable identifiers |

The precise names are a project decision. The separation is the important result.

These categories follow several established distinctions: state invariants versus pre/postconditions in Design by Contract; data relations versus labelled transitions in model-based specifications; component assumptions versus guarantees in interface automata; and trace properties versus progress properties in temporal specification. 

The key boundary is between C and L/H. A single-call rule describes one operation. A lifecycle rule describes which sequences of actions are legal over time. A history rule describes relations across observers and overlapping actions.

Neither of the latter should be reduced to a collection of independent postconditions.

### 2.2 Where error classification belongs

Error classification is worth separating as a category even though a particular rule may be expressed as a postcondition.

The reason is not that errors require a unique mathematical theory. It is that partial failure introduces independent questions:

- What is reported to the caller?
- At what externally distinguishable phase can failure be reported?
- What can observers conclude about whether an effect occurred?
- Can a returned resource remain valid?
- Does the failure tell the caller whether retrying could repeat an effect?

A single error name does not answer those questions.

A classification table is useful for enumerating combinations, but any temporal or cross-observer assertion discovered in the table should refer to a rule owned by the lifecycle or history category.

This preserves one home per rule.

### 2.3 Established specification forms and their appropriate scope

**Structured prose** is stronger than informal prose when it uses a constrained pattern. The established EARS (*Easy Approach to Requirements Syntax*) family provides ubiquitous, state-driven, event-driven, optional-feature, and unwanted-behaviour forms. It was developed at Rolls-Royce and published in 2009. A pattern such as “While [condition], when [event], the system shall [response]” makes triggers and conditions explicit. But it does not, by itself, define a complete concurrency semantics. 

**Decision tables** are particularly suitable for enumerated classifications and mutually exclusive cases. Their advantage is inspection of missing or conflicting case coverage. Their weakness is temporal behaviour: a table of outcomes says little about what happens across several calls.

**Schema-validated data** excels at structural correctness: required fields, enumerated values, references, types, and bounded configurations. A schema can establish that a profile has a valid shape. It cannot establish that the profile's behavioural promises are true of an implementation.

**Executable reference models** are valuable for stateful behaviour. They allow sequences of operations to be evaluated against a simpler, implementation-independent description. Their largest danger is becoming a second implementation that silently chooses among unspecified outcomes.

**Property-based and model-based tests** are mechanisms for producing conformance evidence, not automatically authoritative specifications. QuickCheck pioneered generative testing of stated properties; tools such as Hypothesis also support generating sequences of actions against rule-based state machines. 

**Formal languages** offer stronger semantics and deeper checking, but their value depends on the category. A small relational definition may be entirely adequate for a value rule. A concurrent protocol with subtle interference or progress conditions may justify a labelled transition system, CSP, or TLA+. A full formal model for a simple error classification may add little confidence relative to its cost.

### 2.4 Form ranking

The following rankings are my recommendations for this project, not experimentally established rankings of all specification languages.

The six form families are:

- **SP:** structured prose
- **DT:** decision tables
- **SD:** schema-validated data
- **RM:** executable reference models
- **PT:** property-based or model-based tests
- **FL:** lightweight or full formal languages

The rankings concern suitability as an *authoritative form*. PT is consequently ranked lower where it is most valuable as an independent verifier.

| Category | Ranked choices, preferred first | Reason for first choice |
|---|---|---|
| S — Structure | FL → SP → DT → SD → PT → RM | Concise predicates express timeless structural constraints directly |
| V — Values | FL → DT → SP → SD → PT → RM | Equations and relations express meaning without a running process |
| C — Single calls | SP → DT → FL → SD → RM → PT | Small conditional obligations are reviewable without a full machine |
| F — Failures | DT → SP → FL → SD → RM → PT | Enumerated cases and outcome certainty need systematic coverage |
| L — Lifecycles | DT → FL → RM → SP → PT → SD | Legal states and transitions should be visible to reviewers |
| E — Environment | SP → FL → DT → SD → RM → PT | Assumptions should be explicit before choosing a machine |
| H — Histories | FL → RM → DT → SP → PT → SD | Temporal and cross-observer constraints need unambiguous semantics |
| P — Profiles | SD → DT → SP → FL → PT → RM | Bounded configuration is fundamentally a data-validation problem |
| U — Non-promises | DT → SP → SD → FL → PT → RM | Explicit dimensions and scopes are more useful than a behavioural model |

For history rules, “FL first” means selecting a precise history property or small mathematical model when the guarantee requires one. It does **not** mean mandating a complete TLA+ specification for every concurrency-related sentence.

For structure, the existing axioms remain the foundation. No migration is justified by the behavioural categories.

### 2.5 What each form actually checks

| Form | What can be checked directly | What still needs something else | Relative authoring/maintenance cost |
|---|---|---|---|
| Structured prose | Syntax conventions, IDs, required clause fields, references, terminology | Semantic consistency, completeness, implementation conformance | Low |
| Decision tables | Case coverage over enumerated conditions, overlaps, missing entries | Truth of the claims, unmodelled conditions, temporal relationships | Low–medium |
| Schema data | Structural validity, types, enum values, valid references, some cross-field constraints | Actual runtime behaviour and meaning of the field values | Low–medium |
| Executable model | Reachable states, permitted transitions, bounded invariants, oracle outputs | Fidelity to intended contract; exhaustive behaviour beyond explored state space | Medium–high |
| Property/model-based tests | Violations discovered on generated inputs or histories; shrinking counterexamples | Universal correctness; adequacy and independence of test oracles | Medium–high |
| Formal language | Defined logical properties, satisfiability, bounded model checking; sometimes proofs | Whether the formalization captures intent; implementation correspondence unless separately established | Medium–very high |

A form being machine-readable is not the same as being semantically checkable. A passing schema validator does not prove a behavioural guarantee, and a successful model checker does not establish that the implementation matches its model.

### 2.6 The selection rule

For every new claim, apply this rule in order:

  
    **1. Classify the claim's subject**

    State · Value · Call · Failure · Lifecycle · Environment · History · Profile · Non-promise
  
  
    
  
  
    **2. Choose the minimum necessary observational level**

    Add observers, temporal order, environmental assumptions, and reality binding only when the claim requires them
  
  
    
  
  
    **3. Select the least costly form that preserves meaning**

    Predicate · Clause · Table · Transition relation · History property · Profile schema
  
  
    
  
  
    **4. Assign an independent checking obligation**

    Schema lint · Decision coverage · Property test · State-machine test · History checker · Model checking · Proof
  
  
    
  
  
    **5. Escalate the form only if a specific ambiguity or unchecked property remains**

    Do not formalize merely because a formal language is available
  

The decisive question is:

**What is the smallest model of observation needed to distinguish a conforming behaviour from a counterexample?**

If one instant suffices, do not add a timeline. If one call suffices, do not build a lifecycle machine. If independent calls cannot establish the claim, move to histories. If a difference is only the selection of a declared capability, put it in a profile rather than duplicating the behaviour rule.

This rule resolves the tension between a sufficiently precise foundation and the costs of maintaining it.

## 3. One contract with declared reality profiles

The recommended approach is **parameterized contract refinement**, with the practical configuration ideas of software product-line feature modelling.

Feature modelling has an established literature on representing commonalities, variation points, cardinalities, and legal configurations. Czarnecki, Helsen, and Eisenecker's work provides a theoretical basis for constraining the permitted combinations rather than treating each product variant as a separate specification. 

### 3.1 The contract architecture

  
    **Common boundary contract**

    Universal behaviour claims · Shared predicates · Observable event definitions
  
  
    
  
  
    **Declared variation points**

    Allowed dimensions · Allowed values · Constraints · References to boundary rules
  
  
    
  
  
    {#each ["Profile A","Profile B","Profile C"] as p}
      
        
          {p}
          Validated selections only
        
      
    {/each}
  
  
    
  
  
    **One profile-parameterized conformance suite**

    The same boundary obligations, instantiated and checked for each supported profile
  

A compact way to express the design is:

\[
C(p)=C_{\mathrm{common}}\cap C_{\mathrm{variation}}(p)
\]

Every supported reality must satisfy the common contract. The selected profile then restricts which additional behaviours are admissible or guaranteed.

The important rules are these:

- The common contract defines the semantics of every variation point.
- The profile chooses only from the declared vocabulary.
- Profiles cannot override an unconditional common guarantee.
- A profile must be identifiable to a caller before the caller relies on a profile-specific promise.
- An implementation cannot declare itself conforming merely by choosing a weaker, unapproved profile.

For a concrete profile, schema validation checks that its configuration is legal. Behavioural conformance checks whether its implementation actually meets the resulting obligations.

### 3.2 What must not appear in profiles

A profile should not introduce arbitrary normative prose such as "For this backend, operations usually behave differently when ..."

That is an escape hatch from the common contract.

If a reality requires a newly recognized difference, the review process must either place it inside an existing variation point or decide whether a new variation point is justified.

This makes variation a bounded architectural decision, not an accumulation of implementation exceptions.

### 3.3 Three distinctions to preserve

**Optional guarantee versus selectable guarantee.** A behaviour being permitted but not required is different from a profile selecting a declared guarantee.

**Unsupported capability versus unspecified behaviour.** An unsupported capability is a stated profile fact. An unspecified timing or buffering detail is a deliberate absence of a normative constraint.

**Identical promises versus identical observations.** Different realities can exhibit different performance or scheduling behaviour without violating a common contract if those dimensions are explicitly unspecified. What must remain identical is the set of universal obligations, not every incidental observation.

An intentional semantic difference, by contrast, requires a declared and externally identifiable profile value.

This reconciles a single stable API with implementations that have genuinely different capabilities.

---

## 4. Checking from outside the black box

A black-box conformance method should examine the system at the exposed boundary, without deriving expected behaviour from its implementation.

For every normative claim, the checker needs:

1. An independently defined oracle.
2. A way to establish or record the claim's preconditions.
3. A way to induce the relevant operations and environmental changes.
4. A way to observe a violating result or history.
5. A stated limit on what successful checks establish.

### 4.1 Match verification technique to claim category

| Contract category | Appropriate independent check | Important limit |
|---|---|---|
| Structure | Property tests generating valid and invalid abstract states | Test data may miss cases |
| Value relations | Property-based and metamorphic tests against the stated relation | Must not obtain expected results from the implementation itself |
| Single-call obligations | Boundary conformance tests, generated input partitions, effect observations | May not establish interference-sensitive guarantees |
| Failure classification | Error-outcome matrix, externally induced failures, observable effect checks | Some fault phases may be uncontrollable from outside |
| Resource lifecycle | Model-based sequences of acquire/use/release actions | Finite sequences do not prove all possible lifetimes |
| Environment assumptions | Controlled outside actor, recorded interventions and assumption validation | Cannot claim a violation if the environment broke the contract's assumptions |
| Cross-observer histories | Concurrent clients, event histories, history checking and fault injection | Finite tests cannot prove arbitrary concurrency correctness |
| Profiles | Schema validation, allowed-value checks, shared suite under every profile | Passing configuration validation is not behavioural evidence |
| Unspecified dimensions | Static audit for forbidden accidental promises | No positive runtime test is appropriate where no promise exists |

The original QuickCheck work and later state-machine-testing systems justify property and sequence generation. Tretmans' model-based testing theory supplies the more general idea of checking observed inputs, outputs, and permitted responses against a separate behavioural model. 

### 4.2 The role of concurrent history checking

For concurrency, the recorded evidence needs to preserve which caller invoked which operation, when invocations and responses occurred relative to one another, and what observations each caller received.

If the selected guarantee is linearizability, a checker can ask whether the observed concurrent history admits a legal sequential explanation respecting real-time precedence.

Herlihy and Wing established that correctness condition in 1990. Tools such as Knossos attempt to check recorded histories against a sequential abstract model. Knossos also explicitly represents indeterminate outcomes, including timed-out operations whose effect is uncertain. 

**Linearizability is a candidate guarantee, not a default assumption.** The contract must first decide whether it promises linearizability, a weaker consistency property, or no particular cross-caller ordering.

A sequential reference model is also not sufficient, by itself, for guarantees involving direct external-store modification. The environment model must account for X's actions.

### 4.3 Partial failure must preserve uncertainty

The checker should distinguish at least the following *types of evidence*, without assuming which the library will promise:

| Observation | What it establishes |
|---|---|
| Explicit successful completion | The contract's stated success obligations apply |
| Explicit failed completion with a specified no-effect guarantee | The particular guaranteed absence of effects can be checked |
| Failed completion without an effect guarantee | The reported failure alone does not establish whether an effect occurred |
| Call with no observed response | The operation remains pending or unobserved; its effect is not automatically known |

A model must not quietly replace uncertainty with success or failure.

That is especially important when agents generate tests: an attractive, deterministic oracle can be stronger than the actual contract.

### 4.4 Safety, progress, and timing need different checks

A finite counterexample can disprove a safety property. For example, one observed history may demonstrate that a promised ordering was violated.

An assertion that an operation will *eventually* finish is different. Failure to finish in a finite test interval does not, by itself, refute an unbounded eventuality.

If no latency deadline is specified, a harness timeout is an operational limitation of the test, not automatically a contract violation.

Progress guarantees therefore need one of three things: a specified bound, additional justified environment/fairness assumptions combined with formal reasoning, or explicitly limited test evidence.

This distinction is essential to prevent tests from silently manufacturing latency promises.

### 4.5 What formal verification adds

A small formal model can be particularly valuable when the question concerns combinations of concurrent events that are difficult to enumerate manually.

For example, model checking can explore bounded interleavings and test invariants. A suitable proof can establish properties more generally, subject to the assumptions of the model and proof system.

But **proving the model internally consistent is not proof that the black-box implementation conforms to it**. That correspondence needs separate evidence or a refinement proof connecting the implementation and abstraction.

The FDR tool's CSP refinement checks illustrate the value of formal trace and failure reasoning. TLA+ provides another established way to express safety and temporal properties. Neither removes the need to validate the abstraction boundary. 

---

## 5. Agentic coding evidence

The evidence supports some concrete practices quite strongly. It does **not** establish a universal ranking of prose, tables, YAML, state machines, and formal languages for coding agents.

That distinction matters: benchmark performance can establish that a particular treatment improves a particular task, without proving that the associated format is generally superior.

### 5.1 Measured findings

The following are measured results reported by the cited researchers. Results from different studies and benchmarks are not directly comparable.

  
    
      **Intermediate contract reasoning improved generated tests**

      Controlled comparison
    
    
      +9.8 pp
      bug-detection rate
    
    Google's 2026 *Grounding AI Agents in Contracts* study found that having an agent first articulate preconditions, postconditions, and undefined behaviours improved bug detection by 9.8 percentage points (p = 0.0352) and branch coverage by 2.5 percentage points (p = 0.0034), compared with direct test generation.

    Scope: test generation for production bugs, not an experiment comparing competing boundary specification languages. The intermediate specs were inferred from code, so this is evidence for the value of explicit reasoning, not a justification for deriving authoritative rules from implementations. 
  
  
  
    
      **Agents could implement more than they could verify**

      Benchmark
    
    
      
        82%
        Reference tests passed by generated implementations
      
      
        &lt;60%
        Mutation scores of agent-generated test suites
      
    
    ETH Zürich's October 2026 *TestSuiteBench* evaluates 165 applications with detailed behavioural specifications and systematically constructed mutations. Agent-generated test suites had mutation scores below 60% even though 88% of generated tests passed on the reference implementations.

    These are different metrics, not two measurements of the same task. The result demonstrates a substantive weakness in independent checking, despite plausible generated tests. 
  
  
  
    
      **Repository instruction files did not generally improve task success**

      Empirical evaluation
    
    
      +20%+
      inference cost
    
    Gloaguen and colleagues' 2026 evaluation of `AGENTS.md` files found no general improvement in successful task completion across the tested configurations, while inference cost increased by more than 20%.

    The agents often followed the instructions. The finding concerns unnecessary context, not a demonstrated disadvantage of authoritative specification files. 
  
  
  
    
      **The agreement between task statements and tests is a measurable problem**

      Evaluation audit
    
    
      ~30%
      of SWE-bench Pro tasks estimated broken
    
    OpenAI's July 2026 audit identified overly strict tests, underspecified task statements, weak test coverage, and misleading requirements. Its two review paths identified 27.4% and 34.1% of the public benchmark tasks as broken.

    Particularly relevant: tests can reject behaviourally valid implementations because they enforce implementation details, or require behaviour that the task never specified. 
  

### 5.2 Additional evidence and counterweights

**Generating formal specifications remains difficult.** Le-Cong, Le, and Murray's ACL 2025 *FormalBench* found that models performed better on simple control flow than on complex constructs such as loops and were not reliably invariant under semantics-preserving transformations. This cautions against treating agent-authored formalizations as automatically trustworthy. 

**Formal verification can nevertheless be productive on suitable tasks.** A 2025 vericoding benchmark reported different success rates across Lean, Verus/Rust and Dafny tasks (27%, 44%, and 82% respectively). Those results show task- and language-dependent capabilities; they do not imply that full formal specification is the cheapest or most reliable everyday contract form. 

**Long-horizon consistency remains challenging.** SWE-EVO evaluated 48 software-evolution tasks spanning an average of 21 files. In the reported comparison, the selected agent configuration resolved 21% of SWE-EVO tasks versus 65% on SWE-bench Verified. This is not a causal experiment on duplicated specification rules, but it is evidence that substantial coordinated evolution remains harder than isolated fixes. 

**More specification paperwork is not automatically better.** An October 2026 empirical study of 88,052 pull requests found no supported overall defect-reduction benefit for the specification artifacts it measured. Crucially, those artifacts were mainly issue or ticket references, not generated outputs of spec-driven development tools. The authors explicitly say such tool adoption remains untested by their study. 

### 5.3 What can actually be concluded about forms?

| Practice | Evidence-supported assessment |
|---|---|
| Explicit small pre/postcondition reasoning before test generation | Direct positive experimental evidence |
| Detailed, independently reviewed acceptance expectations | Supported by benchmark audits showing harmful mismatches |
| Independent oracles and mutation testing | Strong rationale from measured weaknesses in generated suites |
| Minimal, relevant agent instructions | Supported by repository-context evaluations |
| One rule referenced from multiple places | Sound maintainability recommendation; direct causal agent evidence remains limited |
| Structured prose over unrestricted prose | Established requirements-engineering rationale; limited direct agent-specific comparisons |
| Tables for enumerated cases | Strong method-level rationale; insufficient evidence for universal agent superiority |
| Schema-validated profiles | Structural correctness is mechanically enforceable; no universal agent success result established |
| Full formal languages for every behavioural specification | Not justified by available empirical evidence |
| Agents inferring authoritative requirements from source code | Unsuitable for this project's stated goal, regardless of whether inference can help generate diagnostic tests |

The proper conclusion is narrower than "agents work best with YAML" or "agents work best with tests."

**Agents benefit from explicit, bounded, checkable obligations. The choice of representation still depends on the semantic category.**

### 5.4 Reported practice, kept separate from results

Specification-driven development tools, `AGENTS.md` conventions, and structured prompting workflows have made requirements-first development an increasingly visible practice.

Practitioner reports commonly recommend decomposition, intermediate plans, and tests. They are useful sources of workflow ideas, but are not controlled evidence that a particular document format produces the most correct implementations.

The project's own P1–P5 lessons are also relevant design evidence, but they should be treated as prior project experience, not as independently measured general laws.

One lesson deserves particular emphasis: an agent describing the existing implementation may produce polished but incorrect specifications. The right test of a foundation is whether an unprimed agent, given only the foundational rules and the public API surface, can reason about what is required without reverse-engineering current behaviour into new guarantees.

---

## 6. How the foundation should be worked out

The axiom project's strongest precedent is its **per-clause decision, counterexample, and check** discipline.

I recommend making this an explicit lifecycle for behavioural clauses.

### 6.1 The clause record

A normative behavioural unit should contain the following information, whether displayed as a small Markdown section or stored in a structured record.

| Field | Purpose |
|---|---|
| Stable ID | Provides one durable home for the claim |
| Category | Determines the allowed abstraction level and preferred form |
| Decision | Records precisely what is being guaranteed, permitted or excluded |
| Assumptions | Identifies the conditions under which the rule applies |
| Observers | States who can distinguish compliance from noncompliance |
| Profile reference | Points to a declared variation point, or declares none |
| Counterexample | Gives a minimal externally observable violation |
| Check | Identifies a concrete conformance check, model check, proof obligation, or checking limitation |
| Rationale | Records why the guarantee is justified at the boundary |
| Status | Proposed, accepted, undecided, or superseded |

The **normative claim** and its metadata must remain distinct. Metadata should not contain a second free-text version of the requirement.

A neutral template might be:

```text
ID: BC-___
Category: ___
Decision: ___
Assumptions: ___
Observers: ___
Normative claim: ___
Profile reference: ___
Counterexample: ___
Check: ___
Checking limitation: ___
Rationale: ___
Status: ___
```

This is an authoring and review template, not a demand that every category use this notation as its authoritative semantics.

For a relation, the normative claim may be a formula. For a lifecycle, it may reference one transition in a transition table. For a history guarantee, it may reference a formal history property.

### 6.2 A disciplined decision process

  
    
      1
    
    
      **Identify the question without consulting implementation behaviour.**

      Formulate the observable distinction that callers need resolved. Identify whether it concerns a single value, one call, a lifetime, interference, or a reality variation.
    
  
  
    
      2
    
    
      **Choose the normative decision.**

      Decide whether the behaviour is universally required, profile-dependent, permitted but not required, or intentionally unspecified. Do not fill gaps using implementation guesses.
    
  
  
    
      3
    
    
      **Select form according to category and observational scope.**

      Use the category decision rule. Separate any claim that needs a different observer or temporal level.
    
  
  
    
      4
    
    
      **Write a counterexample before producing an implementation test.**

      State a possible externally observable result or history that would contradict the rule. If no counterexample can be articulated, determine whether the rule is non-normative, redundant, or insufficiently precise.
    
  
  
    
      5
    
    
      **Name the independent checker and its limits.**

      Define how a black-box implementation will be examined. If the property needs a model or proof, say so. If it cannot currently be checked, record that limitation and leave its acceptance explicitly unresolved under P4.
    
  
  
    
      6
    
    
      **Audit consistency and accidental promises.**

      Check for contradictory clauses, duplicated rules, undeclared profile differences, mechanism language, accidental timing promises, and tests that expect more than the contract.
    
  

This process is intentionally more important than the document syntax.

### 6.3 Checks at three different levels

**Specification validation** should check document and schema integrity: unique identifiers, category declarations, required fields, reference integrity, profile enum values, and absence of duplicated normative homes.

**Semantic validation** should check whether rules can coexist: conflicting outcome classifications, unreachable resource transitions, impossible profile combinations, contradictory guarantees, and whether an alleged counterexample is actually prohibited.

**Implementation conformance** should check the black-box implementation against accepted normative obligations, using a harness that applies only the relevant environmental assumptions and selected profile.

Each layer establishes something different. None should report that all guarantees are proven merely because its own checks pass.

### 6.4 Preventing specification drift in agent workflows

The most useful practical control is to make the contract the starting point of both implementation and verification, without making implementation-generated tests authoritative.

A suggested workflow is:

  
    
      
        **Implementation agent**

        Reads accepted rules and profile; proposes code
      
    
    
      
        **Verification agent**

        Reads accepted rules and counterexamples; proposes independent checks
      
    
  
  
    
  
  
    **Contract-focused review**

    Reject checks that assume undeclared behaviour and code changes that redefine the contract
  
  
    
  
  
    **Conformance evidence**

    Black-box results · Counterexample histories · Coverage and mutation results · Explicit limitations
  

This separation is especially important given the TestSuiteBench evidence: agents can produce implementations that satisfy many reference tests while struggling to create strong test suites from the same specifications.

An independently reviewed oracle is not optional merely because the implementation agent reports that its tests pass.

### 6.5 Criteria for accepting a foundational clause

A clause is ready for inclusion when its category and level are correct, it expresses only observable behaviour, and its normative language is unambiguous. The clause must own one claim, reuse shared predicates by reference, avoid undeclared reality differences, and carry a counterexample with an explicit checking route.

Use a consistent vocabulary of requirement strength. RFC 2119 and RFC 8174 offer well-known conventions for normative `MUST`, `SHOULD`, and `MAY`, although they do not themselves supply the semantics of a stateful behavioural contract. 

A deliberate non-promise should have its own recorded scope, rather than being hidden as an ambiguous omission.

---

## 7. Decisions the research supports

| Decision | Recommendation | Confidence |
|---|---|---|
| Foundational approach | Design by Contract combined with observational trace/refinement semantics | High — established theoretical basis |
| Abstraction selection | Category first, then minimum necessary observation level, then form | High — strong methodological synthesis |
| Default authoring | Atomic structured prose plus tables, relations, and transition specifications where appropriate | Medium-high — sound fit, limited direct agent comparisons |
| Environment | Named observers and explicit external-action assumptions | High — essential for the stated problem |
| Failure handling | Outcome classification separated from effect certainty and lifecycle/history semantics | High — necessary to avoid ambiguous partial failure |
| Variation | One contract with schema-constrained, visible variation points and validated profiles | High — established variability principles |
| Formal modelling | Escalate selectively for hard state-space, interference and progress questions | High — established capabilities; cost varies |
| Tests as the contract | Reject | High — mismatch and coverage evidence |
| Code-derived foundations | Reject | High — violates the project's authority and black-box principles |
| Agent-created checking | Use, but independently validate its oracles | High — direct empirical evidence of limitations |
| Preferred concrete file format | Do not mandate one format across all categories | High as a design conclusion; exact tooling remains project-specific |

## 8. What is established, and what still needs project validation?

The foundational theories are mature. They establish that behaviour can be specified independently of implementations, that environments and interleavings can be modelled, and that conformance can be framed as a relationship between observed behaviour and permitted behaviour.

The agent evidence is more limited.

It supports intermediate contract reasoning, explicit coverage of behavioural boundaries, independent oracle review, and resistance to excessive contextual instructions. It also shows that writing specifications and writing good tests are distinct capabilities.

It does not prove that one document format is uniformly easiest for agents to maintain, nor that a specific formal language produces the most reliable end-to-end development workflow.

A small local evaluation would therefore be justified *after* the category policy is adopted. The comparison should hold the behavioural decisions fixed while changing only the form, using unprimed agents and independently checked tasks. Useful outcomes include omitted obligations, invented guarantees, counterexample quality, implementation correctness, test mutation scores, and cross-file rule drift.

That would test the project-specific agent question without allowing the existing implementation to dictate the foundation.

## 9. Final recommendation

Adopt the following policy as the basis of the foundational specification method:

  Category-directed behavioural contracts

  A foundational boundary specification states obligations over externally observable behaviour, conditional on declared environmental assumptions and a visible reality profile.

  Each claim belongs to exactly one semantic category. That category determines the minimum necessary abstraction level and preferred normative form.

  Structure is expressed as state axioms. Value semantics use relations. Single-call obligations use atomic conditional clauses. Failure classifications use decision tables. Resource lifetimes use transition specifications. Concurrent and environmental guarantees use histories and temporal properties. Profiles select only declared variation points. Deliberately unspecified dimensions are recorded explicitly.

  Normative claims are independent of implementation mechanisms. Shared rules are defined once and referenced. Every claim carries a counterexample and an identified checking obligation; unresolved checking limitations remain visible.

  Executable models, generated tests, and formal proofs are validation instruments selected according to the claims they can establish. None silently becomes the governing contract.

The research supports this as a well-grounded **method for choosing and working out foundational behavioural specifications**, rather than merely a recommendation for a formatting convention.

It preserves the standing of the existing structural axioms without importing their notation into categories where it does not belong. It also keeps implementation realities in their proper role: evidence for profile decisions, not sources of specification authority.

### Selected foundational references

| Reference | Principal reason to retain it |
|---|---|
| [Eiffel — Design by Contract](https://www.eiffel.org/doc/eiffel/ET-_Design_by_Contract_%28tm%29%2C_Assertions_and_Exceptions) | Caller assumptions, supplier obligations, and invariants |
| [Lynch & Tuttle — An Introduction to Input/Output Automata (1989)](https://groups.csail.mit.edu/tds/papers/Lynch/CWI89.pdf) | Input/output actions and explicit environment interaction |
| [De Alfaro & Henzinger — Interface Automata (2001)](https://research-explorer.ista.ac.at/record/4622) | Assume/guarantee interfaces and compatibility |
| [Herlihy & Wing — Linearizability (1990)](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf) | Cross-caller histories and an established concurrency correctness condition |
| [FDR — CSP Refinement](https://www.cs.ox.ac.uk/projects/concurrency-tools/fdr-2.94-html-manual/fdr2manual_5.html) | Trace, failure and divergence-based specification checking |
| [Tretmans — Model-Based Testing with Labelled Transition Systems (2008)](https://link.springer.com/chapter/10.1007/978-3-540-78917-8_1) | Black-box conformance against behavioural models |
| [Mavin — EARS](https://alistairmavin.com/ears/) | Lightweight structured requirements patterns |
| [Egashira et al. — TestSuiteBench (2026)](https://www.sri.inf.ethz.ch/publications/egashira2026testsuitebench) | Measured limitations of agent-created test suites |
| [Tufano et al. — Grounding AI Agents in Contracts (2026)](https://research.google/pubs/grounding-ai-agents-in-contracts-an-empirical-evaluation-of-spec-driven-test-generation/) | Controlled evidence for intermediate contract reasoning |
| [OpenAI — Separating Signal from Noise in Coding Evaluations (2026)](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) | Evidence of test/specification mismatch and invented implementation constraints |

The resulting method answers **how foundational behaviour is specified, varied, and checked**. It leaves all individual operational guarantees—success, failure, consistency, resource life, and external visibility—to be decided through that method rather than assuming them in advance.

---

If you want, I can:

- Explain how to implement category-specific behavioral contracts
- Describe how to create and validate reality profile schemas
- Outline steps for black-box conformance checking