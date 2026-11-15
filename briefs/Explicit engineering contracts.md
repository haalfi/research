Research brief: Explicit, unambiguous engineering contracts across repository artifacts
Goal
Find evidence-based practices for ensuring that engineering intent is explicit, consistently represented, and unambiguously interpretable within and across documentation, specifications, source code, and tests.
The target is a repository in which:

* Each term has one intended meaning within its defined scope.
* Each normative statement has one operational interpretation.
* Decisions, constraints, assumptions, and obligations are explicit rather than silently inferred.
* Different artifacts describing or implementing the same behavior agree on the intended contract.
* Readers and AI coding agents can identify the authority for a requirement or implementation choice.
* Missing decisions, contradictory requirements, and unjustified assumptions are discoverable before they propagate into implementation and tests.

The goal is not to eliminate every possible linguistic interpretation or document every trivial implementation detail. It is to eliminate materially consequential ambiguity and implicit assumptions, particularly those that can produce divergent implementations, incorrect tests, or silently invented behavior.
Produce a minimal, practical set of writing, specification, review, and repository practices for a small engineering team. Evaluate their effectiveness against the cost of introducing and maintaining them.
Context
Repository and workflow

* A docs-as-code repository containing Markdown documentation and specifications, source code, and automated tests.
* Changes are reviewed in git pull requests.
* AI coding agents perform a substantial share of writing, implementation, testing, and review.
* Agents also interpret existing repository artifacts as instructions and sources of authority.
* Requirements and design decisions can be represented, referenced, implemented, or tested in multiple artifacts.

Existing controls
Current writing rules focus on durability:

* A statement should remain valid over time.
* Each fact should have one authoritative home.

These rules do not adequately address interpretation, explicit assumptions, behavioral consistency, or the propagation of decisions across artifact boundaries.
Intended adoption
Prefer lightweight controls that scale with the consequences of an error:

1. Every artifact: Basic clarity, explicit-assumption, and local-consistency rules appropriate to prose, specifications, code, or tests.
2. Normative artifacts and their implementations: Defined terminology, explicit authority, stable identifiers where useful, and checks for contract consistency across related artifacts.
3. Large or high-impact normative changes, on request: Independent-reader and cross-artifact interpretation tests, including review for missing decisions and unsupported assumptions.

These tiers are an initial deployment hypothesis, not a fixed solution. Research may recommend changing their boundaries.
The rules must remain practical for a small engineering team. Author effort, maintenance burden, review noise, and defects introduced by the controls are first-class costs.
Observed pattern: one-document pilot
A pilot on an approximately 1,200-line design document found:

* Words with multiple senses in use.
* Near-synonyms whose equivalence or distinction was unclear.
* Defined terms used inconsistently with their definitions.
* Approximately 40 undefined terms of art.
* Approximately 90 instances of "declared" without a named source.
* Approximately 110 positional references such as "step 3" or "above".
* Pronouns resolving to unintended nouns.
* Unclear distinctions between normative rules and descriptive statements.

The interventions that removed defects were:

* A terminology registry with systematic renaming, requiring substantial author decisions.
* Stable IDs and anchor links.
* Sentence-level precision rules.
* Independent LLM readers paraphrasing rules, with divergent interpretations triggering review.

Every correction round introduced some new defects. Independent readers also exposed missing substantive decisions, not only ambiguous wording.
Interpretation of the pilot: These findings illustrate specific failure mechanisms. They do not establish that the problem is limited to prose or to a single document.
The wider concern is that similar ambiguity, incompleteness, inconsistent terminology, and implicit assumptions occur throughout the repository and across documentation, specifications, source code, and tests.
The research must therefore investigate both local ambiguity and cross-artifact contract integrity.
Research questions
1. Taxonomy: what can go wrong?
Which established classifications best describe failures of interpretation and agreement within and across engineering artifacts?
Distinguish at least:

* Lexical ambiguity: A word or symbol has multiple plausible meanings.
* Referential ambiguity: A name or reference may identify different entities or authorities.
* Syntactic or scope ambiguity: A statement permits different structural or logical interpretations.
* Behavioral ambiguity: Multiple materially different behaviors satisfy the apparent requirement.
* Underspecification: A decision necessary for correct behavior is absent.
* Implicit assumptions: Behavior depends on an unstated premise, default, convention, or inferred decision.
* Inconsistency: Two artifacts prescribe or assume incompatible meanings, constraints, or behaviors.
* Drift: An artifact ceases to reflect an authoritative decision after changes elsewhere.

Investigate which categories are well established in requirements engineering, software engineering, and related research.
Which are most frequent or consequential? Which can writing rules prevent, and which require structural, process, or verification controls?
Do not treat ambiguity, incompleteness, contradiction, and implementation error as interchangeable, even when they interact.
2. Explicit assumptions and specification completeness
What practices help ensure that decisions and assumptions affecting system behavior are made explicit rather than silently supplied by implementers, reviewers, tests, or AI agents?
Investigate:

* How requirements engineering distinguishes intentional degrees of freedom from accidental underspecification.
* How to identify implementation choices requiring an explicit decision.
* How to record environmental assumptions, defaults, preconditions, invariants, and exceptional behavior.
* How to distinguish an assumption from a requirement, derived consequence, or implementation freedom.
* How to make hidden dependencies and inferred obligations reviewable.
* Whether scenarios, counterexamples, boundary cases, decision tables, or structured requirement forms reveal missing decisions.
* How to prevent tests from legitimizing behavior whose correctness was never established.

Seek a practical criterion for determining which assumptions must be explicit, without requiring exhaustive specification of every implementation detail.
3. Authority and consistency across artifacts
How do mature engineering projects maintain a coherent contract across documentation, specifications, source code, and tests?
Investigate:

* How to establish which artifact owns a particular definition, requirement, constraint, or behavioral decision.
* How to distinguish authoritative requirements from derived implementations, examples, observations, and verification artifacts.
* How to recognize disagreements without automatically treating source code or passing tests as authoritative.
* How to handle cases where code and tests agree with each other but both rely on an unspecified assumption.
* How to identify outdated requirements or tests after changes.
* How to manage intentional differences in abstraction or detail between representations.
* How to identify and resolve conflicts without introducing excessive duplication or synchronization work.

Distinguish single ownership of a decision from unnecessarily forcing all representations of that decision into one artifact.
Evaluate lightweight forms of requirements traceability and contract verification against their maintenance costs.
4. Terminology and identity management
What practices maintain stable meanings and identities within and across repository artifacts?
Compare:

* Local terms sections.
* Project-wide glossaries.
* Named concepts and stable identifiers.
* Links and references to authoritative definitions.
* Code-level naming conventions.
* Shared vocabulary across specifications, source, and tests.

Investigate:

* How definitions remain synchronized with actual use.
* How terminology changes propagate across artifacts.
* How to distinguish intentional synonyms from accidental competing names.
* How to handle context-dependent meanings without imposing artificial global uniqueness.
* How mature projects prevent glossary drift and contradictory definitions.
* Whether machine-checkable terminology controls provide meaningful benefits.

Assess both the defects prevented and the author decisions, migrations, and ongoing maintenance required.
5. Unambiguous normative statements
What writing and specification conventions reduce materially different interpretations of individual requirements?
Investigate evidence for:

* Controlled vocabulary.
* Requirement templates.
* Sentence-level precision rules.
* Explicit subjects, conditions, quantifiers, and scope.
* Stable references to named entities and requirements.
* Explicit distinction between normative requirements, rationale, examples, assumptions, and recommendations.
* RFC 2119-style keywords, structural separation, and alternative normative conventions.

Determine which controls genuinely improve interpretation and which merely increase formality or verbosity.
Examine how such conventions work when source code and tests must implement or verify the stated requirements.
6. Independent interpretation and cross-artifact review
What evidence supports independent readers as detectors of ambiguity, incompleteness, and contract disagreement?
Consider human reviewers, LLM readers, paraphrase tests, diagnostic back-translation, and independently derived behavioral interpretations.
Investigate methods in which reviewers independently:

* Interpret a requirement.
* Identify its assumptions and dependencies.
* Derive expected behavior or test cases.
* Compare their interpretations with one another.
* Compare a specification's intended behavior with source code and tests.
* Identify implementation or testing choices not justified by an authoritative requirement.

Assess precision, recall, review cost, reproducibility, and known failure modes where evidence exists.
Particular attention should go to false confidence arising when:

* Multiple readers share the same unstated assumption.
* Multiple agents make the same unsupported inference.
* Code and tests agree but the specification is incomplete.
* Paraphrases differ linguistically without differing operationally.
* Automated reviewers mistake intentional implementation freedom for a defect.

Determine when independent interpretation should be routine, selective, or reserved for high-impact audits.
7. Automated detection and repository checks
Which indicators of ambiguity, inconsistency, drift, and implicit assumptions are reliable enough for automated or advisory checks?
Investigate:

* Requirement-smell detectors.
* Prose linters with custom vocabularies.
* Undefined or inconsistently used terms.
* Ambiguous references and unstable positional links.
* Missing or inconsistent normative identifiers.
* Traceability and cross-reference checks.
* Specification-to-test and specification-to-code consistency analysis.
* Static analysis, contract checking, and relevant test techniques.
* LLM-based checks for missing assumptions, contradictory statements, or unsupported behavioral decisions.

Distinguish:

* Deterministic checks suitable for CI enforcement.
* Heuristic checks suitable for advisory CI.
* Semantic questions requiring author or reviewer judgment.

Assess false-positive burden, coverage, maintenance effort, and the risk of automated checks creating superficial compliance without genuine correctness.
8. AI coding agents as readers and authors
What evidence exists about how ambiguity, incomplete requirements, inconsistent artifacts, and implicit assumptions affect LLM coding agents?
Investigate:

* Which ambiguities most often lead to incorrect implementation choices.
* How agents resolve contradictions between docs, specs, code, and tests.
* How agents behave when required decisions are missing.
* Whether agents tend to adopt existing behavior or tests as implicit authority.
* Which instruction structures encourage agents to identify missing decisions instead of inventing them.
* Whether explicit terminology, traceable authority, structured requirements, or independent interpretation improve outcomes.
* Whether multiple-agent agreement reduces errors or simply reproduces shared assumptions.

Distinguish first-hand evidence from coding-agent studies from indirect evidence from general LLM or human requirements research.
9. Precision, readability, and author cost
How should precision and explicitness be balanced against readability, information density, and maintainability?
Investigate:

* When adding explicit information improves interpretation.
* When repetition or elaboration introduces new ambiguity.
* When concise use of well-defined context is safe.
* How to prevent excessive cross-referencing and identifier overhead.
* How verbosity affects human comprehension and AI-agent consumption.
* When a local explanation is preferable to a distant authoritative reference.
* How to keep specifications useful without attempting exhaustive formalization.

Seek a practical conflict-resolution principle rather than independent style rules that may contradict one another.
10. Failure modes and diminishing returns
Which controls create new errors, drift, unnecessary work, or false confidence?
Examine:

* Glossary proliferation.
* Excessive requirements traceability.
* Redundant definitions.
* Identifier and link maintenance.
* Overly restrictive language rules.
* Template-driven but incomplete requirements.
* Passing tests mistaken for specification completeness.
* LLM reviewers repeatedly introducing new defects through rewrites.
* Automated checks that encourage compliance with surface patterns rather than underlying meaning.

Identify stopping criteria and circumstances in which a control should be avoided or applied selectively.
Research method
Prioritize evidence from:

* Requirements engineering and specification quality.
* Software design and architecture documentation.
* Requirements traceability and consistency management.
* Formal and lightweight specification methods.
* Empirical software engineering.
* Technical communication and controlled natural language.
* LLM-based software development and agent evaluation.

Use primary sources where possible.
For each material finding:

* Provide a source link and year.
* Identify whether it is a first-hand empirical study, standard, practitioner report/opinion, or reasoned inference.
* Describe what was actually measured.
* State limitations and transferability to a small docs-as-code repository.
* Identify thin, contested, or absent evidence.

Do not assume evidence about sentence-level clarity proves improvements in cross-artifact correctness.
Do not invent quantitative benefits, precision/recall results, or cost estimates.
Deliverables
A. Findings by research question
Provide concise findings, cited sources, evidence strength, and unresolved questions.
Distinguish established results from plausible but unvalidated engineering practices.
B. Ranked shortlist of interventions
Rank practices by expected reduction in consequential interpretation and contract defects relative to total author, reviewer, and maintenance cost.
For each practice, report:

* Defect types addressed.
* Whether it works within artifacts, across artifacts, or both.
* Evidence strength.
* Expected benefit, qualitatively unless measured.
* Initial and ongoing costs.
* Automation feasibility.
* False-positive burden and possible new defects.
* Recommended adoption tier.

Explain uncertainty rather than manufacturing a precise ranking.
C. Proposed minimal repository ruleset
Propose a practical set of rules across three tiers:
Tier 1 — All artifacts
Lightweight practices that prevent ambiguity, unstated behavioral assumptions, and local inconsistencies without imposing substantial overhead.
Tier 2 — Normative artifacts and related implementations
Practices establishing authoritative definitions and decisions, stable identities, explicit assumptions, and traceable agreement between specifications, source code, and tests.
Tier 3 — Large or high-impact changes, on request
Independent interpretation and cross-artifact reviews that detect divergent meanings, missing decisions, unsupported assumptions, and inconsistent behavior.
For each rule include:

* Actionable wording.
* Defect prevented or detected.
* A realistic before/after example, using multiple artifacts where relevant.
* Author and maintenance cost.
* Automation or review mechanism.
* Evidence strength.
* Known limitations.

Prefer a small number of high-value rules over comprehensive process machinery.
D. Cross-artifact verification procedure
Propose a lightweight, repeatable review procedure that answers:

1. What behavior or constraint is intended?
2. Where is that intent authoritative?
3. What assumptions must hold?
4. Which decisions are explicitly specified, and which remain intentionally open?
5. Do the related documentation, specifications, source code, and tests agree?
6. Has any artifact introduced a behavioral decision that lacks authority?
7. What remains ambiguous, inconsistent, or underspecified?

The procedure should be usable by a human reviewer or AI coding agent during a pull request, without requiring full formal verification.
E. Practices not recommended
Identify attractive but disproportionately costly, fragile, or unsupported practices.
Explain when they may nevertheless become worthwhile.
F. Tool shortlist
Identify usable tools for terminology, prose, requirements, links, traceability, and cross-artifact consistency checks.
For each include:

* Detection capabilities.
* Markdown, source code, test, and CI integration where applicable.
* License.
* Maintenance status and verification date.
* Known limitations.
* Recommendation for adoption, evaluation, or rejection.

Distinguish actively maintained tools from prototypes and abandoned projects.
Out of scope

* Readability scores as optimization targets.
* General style guides without precision or contract-consistency value.
* Translation and localization as goals.
* Broad prompt-engineering advice unrelated to the engineering contract.
* Replacing Markdown or the existing development workflow wholesale.
* Mandating exhaustive formal specification or verification.

Lightweight formal techniques may be evaluated where they offer practical value.
Decision criterion
The research should ultimately answer:
What is the smallest maintainable set of practices that makes consequential engineering decisions explicit, prevents divergent interpretations, and preserves one coherent behavioral contract across documentation, specifications, source code, and tests?
Favor practices that reveal missing decisions and prevent wrong behavior over those that merely standardize wording or make artifacts look internally consistent.
Distinguish genuine agreement on an explicitly established contract from apparent agreement built on shared but unjustified assumptions.
Where evidence is insufficient, recommend a focused local experiment rather than treating a practice as proven.
