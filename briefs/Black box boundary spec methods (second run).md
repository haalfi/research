# Research brief: a method for specifying observable behaviour at a black-box boundary

## 1. Purpose

Find a well-founded, established method for writing **specifications of
observable behaviour at a black-box boundary**, and combine it with what
agentic coding has shown about which specification forms agents implement,
check and keep consistent reliably. The result decides how this project writes
its foundational specs. It does not decide what any operation means.

## 2. The problem, abstractly

A library exposes one API. Behind it sit several independent realities that
differ in what they can guarantee. Callers must be able to rely on behaviour
that is the same across those realities, except where a difference is declared
and visible.

The library's implementation is treated as a **black box**. The foundation is
what an observer can see at the boundary: results, errors, effects, timing of
failure, the life of resources handed out, and what other observers see. Specs
inside the box (internal layers, adapters, sessions) will follow later; they are
bound to the boundary and never govern it.

An existing foundation shows the intended standing: a short set of axioms that
define the structure the API addresses (a rooted tree of named folders and
items, one key per entity). The boundary spec should play the same role for
behaviour that the axioms play for structure.

**Category decides level and form.** Every spec belongs to a category, and the
category fixes how abstract the spec is and which form it takes. The research
must not carry one category's form over to another. The tree axioms are a
structure spec. They are deliberately abstract and deliberately not tied to
reality or to observers: one instant, no operations, no environment. That is
right for structure, and it is why an axiomatic form fits them. Specs of
observable behaviour are a different category. They have to deal with
observers, time, environment and per-reality profiles, so they need a different
level and very likely a different form. The research should therefore deliver
a way to go from category to level of abstraction to form, not a single
format. And its best model for how a foundation gets worked out is the
research behind the axioms: a decision per clause, a counterexample per
clause, and checks. The axiom spec's notation is not that model.

## 3. Framing the research must respect

1. **Observers are named.** At minimum: the calling code, a second concurrent
   caller, and an actor that changes the underlying store outside the library.
   Consistency and concurrency are only observable across several observers, so
   an explicit environment model (what the outside world may do) belongs to the
   foundation.
2. **"Unspecified" is a statement.** Latency, request counts, memory and
   buffering are observable but often deliberately not promised. The method
   must make the deliberate absence of a promise explicit.
3. **The boundary is parameterised.** Some guarantees differ by reality. The
   method must express "one contract, plus a declared profile" without forking
   the contract per reality.
4. **Real-world behaviour is evidence, not method.** How real storage systems
   behave feeds profiles; it does not choose the specification method.

## 4. Lessons, stated as principles

This project learned these the hard way. They are requirements on the method,
not designs to copy.

- **P1. A spec states what, never how.** Once mechanism enters a spec,
  contradictions follow.
- **P2. One claim per unit, one home per rule.** Large units and copied rules
  drift apart. Shared rules and predicates are defined once and referenced.
- **P3. Detail that varies by reality is bounded and kept apart.** Per-reality
  detail inside the contract grows without limit.
- **P4. A claim nothing checks is undecided.** Every claim names how it is
  checked, or states that it can't be. Figures and claims of extent are
  derived, never restated.
- **P5. The method must work unprimed.** Agents shown an implementation drift
  toward describing it.

## 5. Research questions

1. **Method.** Which well-founded methods specify behaviour at a black-box
   boundary, anchored in Design by Contract? How do they handle observers,
   environment and partial failure? Find the candidates; this brief does not
   prescribe them.
2. **Category, then level, then form. This is the core question.**
   a. **Categories.** Which spec categories does a black-box boundary need
      (for example structure, a function from input to output, a single call,
      a resource's life from open to close, behaviour under a concurrent
      environment, error classification, a profile)? How do established
      methods draw these lines?
   b. **Level.** For each category, what is the right level of abstraction,
      and how far is it bound to observers, time, environment and reality?
   c. **Form.** For each category at that level, which form fits best? The
      candidates are structured prose patterns, tables, schema-validated data,
      executable reference models, property-based or model-based tests, and
      lightweight or full formal languages. Rank each by what it makes
      checkable and what it costs.
   d. **Rule.** State a rule that takes a new spec from its category to its
      level and form, so the choice is made by rule rather than by habit.
3. **Variation.** How is one contract stated with declared profiles, without
   forking the contract per reality?
4. **Checking from outside.** What does a form check by itself, and what needs
   a model or proof? How is an implementation checked against the boundary as
   a black box?
5. **Agentic evidence.** Which forms let coding agents implement and check
   reliably, and which invite drift, contradiction or invented guarantees? Keep
   measured results apart from reported experience.

## 6. Running example

Use one operation throughout: open an entity by key for reading and return a
binary stream the caller consumes and closes. It raises the hard cases: a
failure after the call returned, a concurrent writer, and a resource that
outlives the call. **Do not decide its semantics.** Use it to test whether a
method can state them once they are decided.

## 7. Scope

**In scope:** specification methods, categories with their levels and forms,
variation by profile, checking from outside, and agentic evidence.

**Out of scope:** designing this library's semantics, choosing a format (that
is a later bake-off), storage-system internals, and this project's existing
specs, code and tests.

## 8. Constraints

- **Inputs:** this brief, public sources, and Appendix A, an excerpt of the
  research behind the axioms, provided as an example of the method: how the problem
  was stated, why each clause is there, the decisions taken, and the
  non-goals. Its notation, the axioms themselves, its comparison with storage
  models and its formalization advice are left out on purpose. Read the
  excerpt for method, not for form or content. Nothing else from the project,
  and not the axiom spec itself.
- **Evidence grading:** grade every source A (peer-reviewed or measured study),
  B (documented industrial practice with data), C (practitioner report, no
  data) or D (opinion or marketing). Don't let C or D outweigh A or B.
- **Industrial practice** counts as evidence, graded like any other source.
  Storage case studies get no privileged place.
- **Citations:** link every claim to its source. Mark your own inference as
  inference.
- **Honesty about gaps:** say where the evidence is thin, especially on agents.

## 9. Deliverable

A research report in Markdown:

1. **Kernsatz.** The answer in at most three sentences.
2. **Categories, levels and forms.** The categories with their level of
   abstraction, the category × form matrix (what each cell makes checkable and
   what it costs), and the rule from § 5.2 d.
3. **Method survey.** Per method family: what it states, its limits, its fit
   to § 3 and § 4, and its evidence grade.
4. **Variation.** How each candidate meets § 3.3.
5. **Checking from outside.** What each form checks by itself, and how an
   implementation is checked as a black box.
6. **Agentic findings.** Graded, measured and reported results kept apart.
7. **Scorecard and shortlist.** Each candidate scored against P1 to P5, and 2
   or 3 combinations of method and form for the bake-off: why each is on the
   list, what it is expected to fail at, how to encode the running example,
   and the criteria the bake-off scores on.
8. **Open questions and sources**, with each source's grade.

---

## Appendix A. Method example: research behind a structure foundation

**Editor's note.** This is an excerpt, provided to show a *method*: how the
problem was stated, why each clause is there (one breaking structure per
clause), which decisions were taken against which alternatives, and what was
left out on purpose. The notation, the axioms themselves, a comparison with
storage models, and the formalization advice are omitted. References to
omitted sections (§ 2 to § 4, § 7, § 9, § 10) and to clause names (AX-n, L-n,
D1) are left as written; read them for their pattern, not their content.

---

### A.1. Problem Statement

A store holds folders and items under one root, each addressed by a key. That
structure is written down in several places as a consequence (a tree type, a
validity predicate, prose in an RFC), but its defining assumptions are not
stated once, set-theoretically, with evidence that they are consistent and that
none of them is redundant or missing.

This document does that, and only that. It is deliberately independent of any
backend, any filesystem or object-store convention, and any operation. The
decision it informs is how the model is formalized next (§10).

**What is claimed.** A small set of axioms (§3) describes the finite and
infinite structures that are "a rooted tree whose nodes are folders or items,
whose non-root nodes carry a name, with unique names among siblings". §5 gives,
for each clause of each axiom, a structure that satisfies every other clause
and breaks that one, which is the evidence the clause does work. §7 lists what
should follow from the axioms; § 10 records their machine checks.

---

### A.5. Why each axiom is there

In every row below, **name(r) = ε, and every other name not stated is a
distinct element of N, unless the row says otherwise**; U, F, I and C are given
in full. Each structure satisfies every axiom clause except the one named,
checked against all eight axioms. AX-1 and AX-7 are conjunctions and have a row
per clause. AX-4's existence half has no row because it is not an axiom (D1).

| Clause broken | Structure | What goes wrong |
|---|---|---|
| AX-1, disjoint | U = {r, x}, F = {r, x}, I = {x}, C = {(r, x)} | x is both a folder and an item. |
| AX-1, covering | U = {r, x}, F = {r}, I = ∅, C = {(r, x)} | x is neither a folder nor an item. Nothing else derives its type; L5 and L6 lose their meaning for it. |
| AX-2 | U = {r}, F = ∅, I = {r}, C = ∅ | The root is an item and cannot contain anything. |
| AX-3 | U = {r, x, y}, F = {r}, I = {x, y}, C = {(r, x), (x, y)} | An item contains an entity. |
| AX-4 | U = {r, a, b, x}, F = {r, a, b}, I = {x}, C = {(r, a), (r, b), (a, x), (b, x)} | x has two containers, hence two chains and two Keys. |
| AX-5 | U = {r, p}, F = {r, p}, I = ∅, C = {(r, p), (p, r)} | The root has a container. Every non-root has exactly one container and is reachable, yet the structure is a cycle through r. |
| AX-6 | U = {r, g₁, g₂}, F = U, I = ∅, C = {(g₁, g₂), (g₂, g₁)} | Every non-root has exactly one container and r has none, but g₁ and g₂ form a detached cycle that no chain from r reaches. |
| AX-7, name(r) = ε | U = {r}, F = {r}, I = ∅, C = ∅, name(r) = `z` | The root has a non-empty name. Nothing in §4 uses name(r), so no consequence fails; only the correspondence of L6, where it would be free data. This clause is a normalization, not a source of any property of Key. |
| AX-7, non-empty | U = {r, x}, F = {r}, I = {x}, C = {(r, x)}, name(x) = ε | Key(x) = ε = Key(r): two entities share a Key. |
| AX-7, no `/` | U = {r, w, a, b}, F = U, I = ∅, C = {(r, w), (r, a), (a, b)}, name(w) = `a/b`, name(a) = `a`, name(b) = `b` | w and b both have Key `a/b`. |
| AX-8 | U = {r, x, y}, F = {r}, I = {x, y}, C = {(r, x), (r, y)}, name(x) = name(y) | Two children of r with one name, hence one Key. |

**Witness models** (consistency evidence; no row above is a model of AX-1 to
AX-8). In each, name(r) = ε and every other name is the one given.

- **W0.** U = {r}, F = {r}, I = ∅, C = ∅. The smallest model; every axiom that
  quantifies over a pair of children holds only vacuously.
- **W1.** U = {r, d, f}, F = {r, d}, I = {f}, C = {(r, d), (d, f)}, name(d) = `d`,
  name(f) = `f`. Keys: ε, `d`, `d/f`.
- **W2.** U = {r, d, e, f}, F = {r, d, e}, I = {f}, C = {(r, d), (d, e), (d, f)},
  name(d) = `d`, name(e) = `e`, name(f) = `f`. Keys: ε, `d`, `d/e`, `d/f`. Here
  AX-8 is exercised by a folder with two differently named children, and `e`
  is an empty non-root folder.

A third kind of evidence, that the axioms *imply* what they are meant to, is
the lemma list in §7.

---

### A.6. Decisions taken

| Decision | Chosen | Alternative and what it would change |
|---|---|---|
| Files and folders share one name namespace | Shared (AX-8 over all children) | Typed keys (`a` against `a/`): the label alphabet becomes names × {item, folder}, the trailing `/` becomes a type marker, and AX-8 holds per kind. The same trie structure over a richer alphabet. |
| `a/` as an input spelling | Not a Key of anything | Treating `a/` as a second spelling of folder `a` would be an alias, which this model leaves out. |
| Empty folders | First-class entities | Folders existing only as prefixes of items would add an axiom: every non-root folder has a descendant item. |
| Name alphabet | Non-empty, no `/` | `.` and `..` are ordinary names. Treating `.` as an alias of the containing folder, or `..` as moving to the parent, is navigation and belongs outside the axioms. |
| Finiteness | Not assumed | Adding it would exclude infinite stores. It would not be needed for induction on depth, which AX-6 already supports. |
| Scope | Static structure only | Create, delete, move and copy are a second pass. |

---

### A.8. Non-goals

- Operations and state change (create, delete, move, copy, list).
- Navigation: `.`, `..`, normalization, aliases.
- Any backend, filesystem, or network behavior.
- Links, permissions, metadata, content.
