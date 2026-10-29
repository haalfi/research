# T2 Conflicts and satisfiability

Scope: brief §4 T2. Grades per brief §6: A, A-pre, A-workshop, B, C, D. **[unreachable]** means the full text could not be fetched, so the item is a lead only. *Inference* marks my own reasoning. Every method below carries an **Agents:** line saying whether LLMs or agents were measured doing that step. Items in brief §3 (form rule, contract shape, ACSL `complete`/`disjoint behaviors` as the table form, Vericoding/ImpossibleBench agent findings) are not re-surveyed. Where a §3 item is touched with new full-text evidence, it is flagged **[§3-challenge]** or **[§3-extends]**.

All full texts were downloaded to the scratchpad and read with pdftotext. Search snippets are used only where marked.

---

## 1. Consistency across clauses written in different forms (tables, contracts, transition systems, history predicates, profile schemas)

### Takeaway
Every working cross-form consistency checker I found translates all clauses into **one common logic** (Duration Calculus → phase-event automata → Boogie; FRETish → pmLTL → Lustre; class diagram + temporal logic → first-order temporal logic → SMT/model checking; patterns → TCTL → SMT-LIB). It then checks that the **conjunction** is satisfiable and returns a **minimal inconsistent subset** as the diagnosis. This is the Zave–Jackson "conjunction as composition" idea put into practice. The best industrial evidence is Bosch with Hanfor/ReqCheck: about 310 findings, 100 of them major, on requirements that had already been reviewed manually several times. Plain consistency is too weak, though. Every mature tool adds **stronger notions**: rt-inconsistency (a design choice that can paint the system into a corner), vacuity, realizability against the environment, and goal *divergence* under a boundary condition. Agent evidence is thin. One preprint finds that LLM-only conflict detection misses most conflicts (recall 0.31), while LLM translation plus SMT reaches recall 0.83 on n=55 requirements.

### Cited Findings

**Common-logic conjunction checkers (implemented, measured)**
- **ReqCheck / Ultimate ReqAnalyzer (Langenfeld, Dietsch, Westphal, Hoenicke, Post, RE 2019). Grade A.**
  - Requirements are written in a restricted English pattern grammar with Duration Calculus semantics. They are compiled to phase-event automata, then to a Boogie program, and checked by a software model checker for **consistency, rt-consistency and vacuity**.
  - Definitions: "A set of requirements is consistent if [there is an] interpretation satisfying all requirements in the set." rt-inconsistency is a property "that implies but is not equivalent to general consistency": there is a finite run after which no continuation satisfies all requirements. A requirement is vacuous "if the behaviour it specifies cannot be triggered in a system satisfying all requirements."
  - Bosch: ten device requirement sets (50 to 701 requirements). Analysis times ran from 1m33s to 4h14m. Device 8 had 263 requirements, 6 vacuous, 73 rt-inconsistencies, 18 timeouts, 3h58m.
  - "From the ca. 310 results of the tool, 100 were classified as major issues, although the requirements had been reviewed manually several times before". "nearly 70% of our findings (including questions, typos, duplications, type issues) have resulted in a fix in the requirements, while the rest resulted in changes to the formalisation."
  - Pairwise and k-subset checking gives partial results under per-subset resource limits. The scalability gain comes from not building the parallel product of automata.
  - [Source](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)
  - **Agents:** human-only evidence. Formalisation was done by trained people.
- **Hanfor (Becker et al., REFSQ 2021 tools track). Grade A-workshop.**
  - A process tool for formalisation by "workers" and a "supervisor".
  - Back-end ReqCheck "checks for inconsistency, rt-inconsistency, and vacuity" and returns "a minimal core set of inconsistent requirements, a timing diagram, and the set of vacuous requirements".
  - Used on "industrial requirements sets of between 20 and 1000 raw requirements from the automotive and railway domain".
  - It explicitly does **not** use NLP to automate formalisation: "the DLP is about human natural language processing, not automatic NLP".
  - [Source](https://ultimate-pa.github.io/hanfor/references/publications/hanfor-semantic-requirements-review-at-scale.pdf)
  - **Agents:** human-only.
- **EuRailCheck / Cimatti, Roveri, Susi, Tonetta (FMA 2010, EPTCS). Grade A-workshop.**
  - Requirements are fragmented, then formalised in a UML class diagram, which serves as the signature, plus first-order temporal/hybrid logic. Everything is checked in one logic with three checks:
    1. **logical consistency**: "two formalized requirement fragments mandate mutually incompatible behaviors";
    2. **scenario compatibility**: "reduced to … checking the consistency of the set of … fragments with the constraint describing the scenario";
    3. **property entailment**: consistency with the negated property.
  - Output is a witness trace on success, or a "minimal inconsistent subset" on failure.
  - When a check fails, "two causes are possible: … the formalization is not correct … or … there is a flaw in the informal specification." This is a direct statement that a consistency failure cannot by itself separate a translation error from a source error.
  - Applied to ETCS requirements. [Source](https://arxiv.org/pdf/1003.1741v1.pdf). The ASE 2009 claim of "almost thirty railway experts" is a search snippet only, **[unreachable]**.
  - **Agents:** human-only.
- **PROPAS / SMT-based consistency (Filipovikj, Rodriguez-Navas, Nyberg [Scania], Seceleanu). Grade A** (peer-reviewed per MDH listing; exact venue not verified).
  - Pattern-based TCTL requirements are translated to first-order logic and then to SMT-LIB/Z3. An UNSAT result yields an unsat core as the minimal inconsistent set.
  - On the Scania Fuel Level Display (FLD) the full set returned SAT after a quantifier-mitigation step. Validation was by **fault injection**: "All of the injected faults have been detected by Z3."
  - Universal quantifiers needed a pessimistic encoding to avoid solver UNKNOWN or false positives.
  - [Source](https://www.es.mdh.se/pdf_publications/4980.pdf)
  - **Agents:** human-only.
- **Model-checking vs SMT consistency (ECEASST vol. 75, 2018).** Snippet only: "no significant difference in analysis time" for invariants; the main difference was modelling effort. **[unreachable]**, lead. [Source](https://journal.ub.tu-berlin.de/eceasst/article/view/1054)

**Goal-conflict / divergence (van Lamsweerde lineage)**
- **van Lamsweerde & Letier, "From Object Orientation to Goal Orientation" (Monterey Workshop, LNCS, 2003). Grade A-workshop.**
  - Worked divergence example: two goals "are in fact not logically inconsistent; however, they become inconsistent when the plant is in start-up or cool down phase and the water pressure is below 'Low'". The boundary condition is ◊((NormalStartUp ∨ NormalCoolDown) ∧ WaterPressure < 'Low'). Resolution is by weakening one goal.
  - Obstacle: O obstructs G iff {O, Dom} ⊨ ¬G and Dom ⊭ ¬O.
  - Describes a "multiparadigm, 'multi-button' framework" combining semi-formal, qualitative and formal reasoning, and a mapping of KAOS models to SCR tables.
  - It gives **no measured data** on detection rates.
  - [Source](https://webperso.info.ucl.ac.be/~avl/files/avl-MontereyLNCS.pdf)
  - **Agents:** human-only.
  - The original van Lamsweerde, Darimont & Letier, IEEE TSE 24(11) 1998, is **[unreachable]**.
- **Degiovanni et al., ASE 2018 (genetic algorithm for goal-conflict identification). Grade A.**
  - Restates divergence formally as a boundary condition BC with {Dom, BC, G1..Gn} ⊨ false (logical inconsistency), {Dom, BC, G−i} ⊭ false for each i (minimality), and BC ≠ ¬(G1∧…∧Gn) (non-triviality).
  - Uses an LTL satisfiability checker as fitness and finds BCs that pattern- and tableau-based methods cannot.
  - [Source](https://nmaguirre.github.io/assets/pdf/ase2018.pdf)
  - A 2022 follow-up notes the GA approach is "not complete", its efficiency "seems modest", and computed BCs "may not be quite useful for debugging". [Source](https://arxiv.org/pdf/2203.12903) (A-pre; critique read in full text).
  - **Agents:** human-only.
- **ACoRe (Carvalho, Degiovanni et al., arXiv 2303.05213). A-pre.**
  - Automated conflict *resolution* by multi-objective search over LTL repairs, assessed on "25 requirements specifications taken from the literature".
  - Produces resolutions that "resemble specification repairs manually provided".
  - [Source](https://arxiv.org/pdf/2303.05213)
  - **Agents:** no LLMs, search-based.

**Viewpoints / inconsistency management**
- **Nuseibeh, Easterbrook, Russo, "Leveraging inconsistency in software development", IEEE Computer 33(4), 2000. Grade A** (peer-reviewed magazine, qualitative case studies, no measures).
  - "incremental or localized consistency strategies do not guarantee global consistency"; "in the general case the problem is truly intractable."
  - Three case studies (ISS command-and-control requirements, a deep-space probe controller) were all in "a mixture of prose, tables, flowcharts, and other diagrams". The method in each was "to re-represent and restructure the specifications more precisely, more formally".
  - Some inconsistencies are deliberately **tolerated** as a risk-based decision and must be re-evaluated when parameters change. The Ariane-4→5 reuse is the cautionary example.
  - "it is often possible to deny the inconsistency at the pragmatic level … such a denial questions the formalization of either the description itself or the consistency rules."
  - [Source](https://typeset.io/pdf/leveraging-inconsistency-in-software-development-4me5sgffk1.pdf)
  - **Agents:** human-only.
- **Zave & Jackson, "Conjunction as Composition", TOSEM 2(4) 1993.** **[unreachable]**. Abstract only: partial specifications in different languages are combined by giving them a common semantic domain, typically translation into predicate logic, and composing by conjunction. [Source](https://scilit.com/publications/23142cc505be037b2c93ffa7b13451aa)

**Agents doing conflict detection**
- **SAT-LLM (Fazelnia, Mirakhorli, Bagheri, 2024 preprint on NSF PAR). Grade A-pre.**
  - Dataset: 55 requirements (a Broker system) containing 15 conflicting subsets, 4 of them composite (three or more requirements).
  - ChatGPT (GPT-4) alone "detected 33% of conflicting requirement sets": 36% of direct pairs and 25% of composite conflicts, with precision 0.85, recall 0.31, F1 0.46.
  - SAT-LLM (GPT-4 translates to FOL, then Z3 MUS/MSS enumeration): precision 1.00, recall 0.83, F1 0.91.
  - "Correct" means a conflicting requirement identified together with its counterpart, against an injected and labelled ground truth.
  - [Source](https://par.nsf.gov/servlets/purl/10574434)
  - **Agents: measured.**

### Inferences
- *Inference:* For the brief's mix of forms (instant formulas, case tables, frames, transition tables, history predicates, failure tables, profile schemas), the evidenced pattern is: give each form a **translation into one shared logic over one shared signature** (the abstract state of the §3 contract), assert the conjunction, and check SAT with unsat-core extraction. Hanfor's type inference across requirements and EuRailCheck's class diagram as signature both show that a **shared typed vocabulary** catches cheap cross-form errors before any semantic check.
- *Inference:* "Tables in different decisions that disagree" (a brief §2 failure mode) is exactly a pairwise or small-subset inconsistency. ReqCheck's k-subset strategy (k=2 first) is the evidenced way to localise it. "Consistency checks that passed but missed a contradiction" maps to the gap between plain SAT and the stronger notions (rt-consistency, vacuity, divergence under a boundary condition, realizability). Bosch's 73 rt-inconsistencies in one 263-requirement set were invisible to plain consistency.
- *Inference:* Divergence is the right model for "consistent in general, contradictory in a reachable corner". For a store API, examples include a frame clause saying X unchanged and a fault table saying X reset, both under a cancellation-during-write boundary condition. A satisfiability check that does not enumerate environment states will pass such a pair.

### Gaps
- No implemented tool was found that checks consistency **across heterogeneous native notations** (e.g., a TLA+ module against a Dafny contract against an Alloy model) without first re-expressing them in one logic. Every tool found is single-logic at the core.
- Heitmeyer, Jeffords, Labaw, TOSEM 1996 (SCR consistency checker) and the SCR toolset reports on DTIC returned HTTP 403: **[unreachable]**. The claim "found many errors human reviewers missed" is a search snippet only.
- KAOS/Objectiver industrial conflict-detection rates: none found.

---

## 2. Table completeness/disjointness checking (SCR, TableWise, ACSL, decision-table checkers) and cost

### Takeaway
Completeness/disjointness checking of finite case tables is cheap and mature. BDD-, SMT- and geometric checks run in milliseconds to seconds even for about 1,500-row tables. The hard parts are elsewhere:
- getting the table's guard predicates over the **shared** state vocabulary, so that tables from different decisions can be checked against each other;
- reporting **maximal** overlaps instead of floods of redundant pairs.

**[§3-extends]** The form rule's "table checked complete and disjoint" is cheap per table. Cross-table disagreement needs the conjunction check from Q1.

### Cited Findings
- **DMN decision tables (Calvanese, Dumas, Laurson, Maggi, Montali, Teinemaa, arXiv 1603.07466 / BPM 2016). A-pre version read; venue not verified.**
  - Overlap detection maps to overlapping hyper-rectangles; missing-rule detection maps to the uncovered space. Both use sweep-based algorithms.
  - Nine tables of about 500, 1,000 and 1,500 rules with 3, 5 and 7 columns, with 10% rules perturbed. Missing-rule detection ran 160 ms to 18.3 s; overlap detection ran 200 ms to 30.7 s.
  - Reported sets: e.g., 812 maximal overlapping rule sets vs 23,115 reported by the Signavio-style algorithm, for a 1,492-rule table.
  - [Source](https://arxiv.org/pdf/1603.07466)
  - **Agents:** human-only.
- **TableWise (Odyssey Research Associates for Honeywell, NASA project page). Grade C** (archived project page, no data).
  - "uses a generalization of Binary Decision Diagrams to determine if a particular table is exclusive (…at most one action…) and exhaustive (…at least one action…)"; it also generates Ada code and documentation.
  - [Source](https://shemesh.larc.nasa.gov/fm/oldfm/fm-old-sw-ver-tablewise.html)
  - **Agents:** none.
- **SCR consistency checker (Heitmeyer et al., TOSEM 1996). [unreachable]** (DTIC 403).
  - Snippet: it checks condition tables for coverage and disjointness, and mode transition tables for disjointness, on the A-7 OFP specification. [Lead](https://www.bohrium.com/paper-details/automated-consistency-checking-of-requirements-specifications/811737767825375232-2450)
- **ACSL `complete behaviors`/`disjoint behaviors`.** Settled in brief §3, not re-surveyed. Frama-C/WP smoke tests (Q4) are the complementary check that a behavior's `assumes` is reachable at all.

### Inferences
- *Inference:* Table checking costs nothing compared with authoring. The gate should run on every edit. For the failure/phase/effect/retry tables and the state × operation transition table, the cheap per-table check is the **first** gate that can fail.
- *Inference:* Disjointness inside one table does not imply consistency with another table indexed by the same state. The two tables must be conjoined over the shared abstract state (Q1). Report maximal conflicting sets, following the DMN result, so that agents and reviewers are not flooded.

### Gaps
- No measured study of table checking on *agent-written* tables was found.
- SCR cost figures were not recoverable (DTIC 403).

---

## 3. Incremental consistency as clauses accumulate

### Takeaway
There is little direct evidence. The usable facts:
- Requirement-set analysis at Bosch was re-run as requirements evolved. Changes were "formalised in mere minutes", but whole-module analysis took hours.
- Compositional decomposition (FRET SCCs) and monotonicity (unrealizable cores) are the evidenced ways to keep re-checks cheap and local.
- Smoke-test and proof caches cut re-check cost in Frama-C.
- Nuseibeh et al. warn that local or incremental checks do not guarantee global consistency.

So incremental checking should be used for speed, with a periodic full-conjunction check as the actual gate.

### Cited Findings
- **Bosch / ReqAnalyzer (RE 2019). A.**
  - "updating the formalized requirements proved to be very fast… New changes are usually formalised in mere minutes. This allows for an effective introduction of automatic regression analysis on requirement sets".
  - Analysis time "is manageable, although there is room for further improvement by, e.g., introducing techniques from regression verification to reuse results from previous analysis runs". In other words, incremental reuse was **not** implemented.
  - Full-module runs on the largest sets took about 4 h.
  - [Source](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)
- **Hanfor. A-workshop.** "If a new version of the raw requirements is submitted by the client, Hanfor automatically identifies changed, added, or removed requirements, changes their status and tags them for re-review." [Source](https://ultimate-pa.github.io/hanfor/references/publications/hanfor-semantic-requirements-review-at-scale.pdf)
- **FRET compositional realizability (Mavridou et al., FM 2021). A.**
  - Requirements are partitioned into connected components of a "requirements graph" (an edge where two requirements share a state variable). Proven: realizable iff every partition is realizable.
  - Speed-ups: LMCPS FSM 1524.82 s → under 7 s (JSyn-vg); QFCS FCC 53.31 s → 4.12 s (JSyn); REG 99.52 s → 5.72 s.
  - Failures: decomposition yielded a single SCC for 3 of 12 benchmarks, "connected through mode variables".
  - [Source](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf)
  - **Agents:** human-only.
- **Unrealizable cores (Maoz & Shalom, ICSE 2021). A.** QuickCore exploits "monotonicity of unrealizability" and incremental computation. [Source](https://arxiv.org/pdf/2103.00297)
- **Frama-C/WP smoke tests (Blanchard et al., TAP 2024). A.** Cost is mitigated by "prover caches". Users "generally turn smoke test verification off during specification and proof debugging, and only turn smoke tests on for nightly builds and final proof replay". [Source](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf)
- **Nuseibeh et al. 2000. A.** "incremental or localized consistency strategies do not guarantee global consistency." [Source](https://typeset.io/pdf/leveraging-inconsistency-in-software-development-4me5sgffk1.pdf)
- **Leads only (not read in full):**
  - Leino & Wüstholz, "Fine-grained caching of verification results", CAV 2015 (Dafny/Boogie re-verifies only code affected by an edit). PDF fetch failed: **[unreachable]**. [Lead](https://www.microsoft.com/en-us/research/?p=342581)
  - iProperty (ICSE 2014, property differencing for incremental checking): snippet only, **[unreachable]**.
  - SMT `push/pop` vs `check-sat-assuming` (ICLP 2020): snippet only, **[unreachable]**.

### Inferences
- *Inference:* A workable regime has three parts:
  1. on each new clause, run (a) its per-form check, (b) a pairwise or k-subset conjunction against clauses sharing a variable (the FRET requirements-graph partition gives "sharing" a precise meaning), and (c) re-run vacuity for clauses whose antecedents it touches;
  2. nightly, or before any downstream step, run the full conjunction, rt/realizability checks and smoke tests;
  3. keep every past unsat core and minimal witness as a **regression fixture**, so a reintroduced contradiction fails fast.
  The shared-variable partition also tells which earlier clauses a new one can possibly contradict.
- *Inference:* Mode-like variables (handle state, backend profile, lifecycle phase) will connect almost every clause, as they did in FRET's GPCA/NN/TSM. Decomposition alone will not keep checks local for a store API. Per-mode slicing is suggested by FRET authors as future work, so it is unevidenced.

### Gaps
- No measured study was found of incremental requirements-consistency checking cost over a project lifetime (clause count vs check time vs defects caught).
- No study of agents maintaining consistency as clauses accumulate.

---

## 4. Realizability: FRET, GR(1)/Spectra, adversarial environment; transfer to a library API

### Takeaway
"Realizable" means: there exists an implementation that, **for every environment input allowed by the assumptions**, keeps all guarantees forever. Formally this is the greatest fixed point Viable(s) = ∀a. A(s,a) ⇒ ∃s′. G(s,a,s′) ∧ Viable(s′), with Realizable = ∃s. G_I(s) ∧ Viable(s). It is strictly stronger than consistency (satisfiable conjunction), and catches clause sets that only an implementation with control over the environment could meet. Tools exist: FRET with JKind/Kind 2, and Spectra for GR(1) with unrealizable-core diagnosis. Their evidence comes from embedded and control specs, and solvers return "unknown" on non-linear arithmetic.

The most transferable empirical warning is **non-well-separation**: in 60 of 79 GR(1) specs, the system could satisfy the spec by forcing the environment to violate its assumptions. That is a realizability-level vacuity.

### Cited Findings
- **Definition (FRET, FM 2021). A.**
  - "An AG contract is realizable if there exists a system implementation that satisfies the contract guarantees for all assumption-complying stimuli provided by the environment… any behavior following an environmental input that violates the contract's assumptions is unrestricted".
  - Uses JSyn and JSyn-vg over linear integer and real arithmetic. "the overall problem of realizability checking is undecidable."
  - Variables must be classified as **inputs** (environment) or **outputs/state** (system).
  - Twelve benchmarks with 4 to 190 requirements. Results included realizable, unrealizable, **unknown** (EB "due to non-linearities for both JSyn and JSyn-vg") and 12 h timeouts.
  - Liquid mixer: compositional checking localised the conflict to [LM-001] and [LM-009].
  - [Source](https://ntrs.nasa.gov/api/citations/20210015352/downloads/FM2021_CR_Compositional_Realizability_in_FRET%20(6).pdf)
  - **Agents:** human-only.
- **FRET diagnosis (Katis, Mavridou, Giannakopoulou, Pressburger, Schumann, CAV 2022, "Capture, Analyze, Diagnose").** Abstract via search: "visualization of conflicts between requirements and simulation of counterexamples". Full text **[unreachable]** (not fetched). [Lead](https://www.doi.org/10.1007/978-3-031-13188-2_24)
- **Unrealizable cores (Maoz & Shalom, ICSE 2021, Spectra). A.**
  - Corpus: SYNTECH15/17, "227 specifications of 10 autonomous Lego robots, written by 3rd year undergraduate computer science students", of which 40 were unrealizable (14 + 26), plus AMBA and GENBUF.
  - "Most SYNTECH specifications have multiple cores. Specifications with over 50 cores exist in each set". Punch computes all cores faster than a naive top-down algorithm.
  - [Source](https://arxiv.org/pdf/2103.00297)
  - **Agents:** human-only. Specs were written by students.
- **Well-separation (Maoz & Ringert, ESEC/FSE 2016). A.**
  - "One way a controller may satisfy the specification is by preventing the environment from satisfying the assumptions, without satisfying the guarantees… specifications that allow it are called non-well-separated."
  - On 79 student specifications, "only 19 out of 79 environment specifications were found to be well-separated", and assumption violation "can be forced from all initial positions" in 41 of 79.
  - Even under the tool's strict-realizability semantics, only 15 of the 60 became safe w.r.t. guarantees, and 5 of those "trivially… because the safety guarantees are unrealizable".
  - Non-well-separated cores were mostly one or two assumptions.
  - [Source](https://zenodo.org/api/records/6577097/files/well-separation-fse16.pdf/content)
  - **Agents:** human-only.
- **Hanfor/ReqCheck rt-consistency** is a timed relative of realizability without an input/output split. It asks whether the system can reach a state from which no continuation satisfies all requirements. Bosch found 4 to 109 rt-inconsistencies per device set. [Source](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)
- **van Lamsweerde & Letier (A-workshop).** Obstacle analysis is the goal-level analogue: "First-sketch specifications… tend to be over-ideal; they are likely to be violated from time to time in the running system due to unexpected behavior of agents." [Source](https://webperso.info.ucl.ac.be/~avl/files/avl-MontereyLNCS.pdf)

### Inferences (transfer to a library API with environment actions)
- *Inference:* Mapping:
  - environment = concurrent callers, out-of-band actors, injected faults, cancellations, timeouts;
  - system = the store's responses and state updates.
  A clause set is **unrealizable** if some environment schedule allowed by the environment clause forces two guarantees to clash. For example, "a completed write is visible to every later read" and "cancellation leaves no partial effect" clash under cancel-after-commit-before-ack unless a non-commitment (*indeterminate*) is declared. Plain SAT finds *one* happy history and passes. A realizability or rt-consistency check quantifies over all environment moves.
- *Inference:* For a library, a full GR(1)/LTL synthesis check is usually unnecessary and often infeasible (data domains, unbounded callers). Cheaper evidenced proxies:
  1. bounded rt-consistency / deadlock-freedom of the conjoined spec in a model checker (TLC/Apalache) with environment actions as free transitions. This is the TLA+ "no deadlock" plus "every reachable state has an allowed response for every allowed environment action" check. *Inference* by analogy with rt-consistency.
  2. FRET-style SCC partitioning to keep the check per resource.
  3. A **well-separation check**: the environment clause must be satisfiable *independently of* the store's choices. The store must not be able to make an assumption false, e.g., "callers never cancel after timeout" when the store controls the timeout. Maoz–Ringert's 60/79 rate says this mistake is common even among trained authors.
- *Inference:* Assume–guarantee realizability presupposes a clean input/output split. For a library, the brief's typed non-commitment register supplies it: *unspecified* / *indeterminate* outcomes are system choices, and environment actions are inputs. Misclassifying a non-commitment as an environment input makes a spec look realizable when it is not, and the reverse.
- *Inference:* Concurrency adds a dimension GR(1) tools do not model natively: interleaving and linearization points. The transferable part is the game view (∀ environment ∃ response). History-predicate checking belongs to T3.

### Gaps
- No study was found applying realizability checking to a **software library / storage API** spec. All evidence is embedded, robotics or student GR(1) specs.
- **Agents:** I found no measured study of LLMs writing realizable specs or repairing unrealizable ones in the full texts read.

---

## 5. Vacuity and non-triviality: detection, weak-spec findings, gates

### Takeaway
Vacuity is common and real.
- IBM: "typically 20% of specifications pass vacuously during the first formal-verification runs" (Beer et al. 1997, quoted in Kupferman–Vardi).
- Bosch: 1 to 6 vacuous requirements per set.
- GR(1): 60 of 79 specs non-well-separated.
- LLM verification benchmarks show **weak specs** as the dominant failure: about 9% of specs too weak plus 15% poorly translated in Vericoding, conditioned on success; 52% of failures in ReForm; RL agents actively drift to weak specs when rewarded only by verifier success.

Effective gates come in two kinds, and both are needed:
- **Structural (reachability/contradiction) gates**: Frama-C `-wp-smoke-tests`, Dafny `--warn-contradictory-assumptions`/`--warn-redundant-assumptions` and proof-dependency coverage, TLC "action never enabled", Alloy `run` non-empty, Lean `#print axioms`.
- **Semantic-strength gates**: interesting witnesses (Kupferman–Vardi), spec mutation and negative tests ("spectests", Lahiri's symbolic tests), subset or strength comparison against an independent reference spec.

Structural gates catch contradiction and dead code. Only the semantic gates catch "consistent but too weak".

### Cited Findings

**Classical vacuity**
- **Kupferman & Vardi, CHARME 1999 (STTT 2003). Grade A.**
  - Quoting Beer et al. 1997: "typically 20% of specifications pass vacuously during the first formal-verification runs of a new hardware design, and … vacuous passes always point to a real problem in either the design or its specification or environment."
  - KV vacuity: a spec is non-vacuous if every subformula affects its truth value. Detection reduces to model-checking ϕ with subformulas replaced by true or false, at cost O(|ϕ| · C_M(|ϕ|)).
  - An **interesting witness** is a run that satisfies ϕ non-vacuously, e.g., a run with req and grant for AG(req → AF grant).
  - [Source](https://typeset.io/pdf/vacuity-detection-in-temporal-model-checking-290v578apa.pdf)
  - Beer et al. CAV 1997 original: **[unreachable]**; the 20% figure is secondhand via KV.
  - **Agents:** human-only.
- **Requirement-set vacuity (ReqCheck, RE 2019). A.** {req1, req4} is vacuous because req1 forbids A, so req4's trigger never occurs. Bosch device sets had 1 to 6 vacuous requirements. A vacuous requirement is either unnecessary or reveals "requirements [that] erroneously cause the vacuity". [Source](https://people.irisa.fr/Nicolas.Markey/PDF/Papers/re2019-LDWHP.pdf)

**Deductive-verification gates**
- **Frama-C/WP smoke tests (Blanchard, Correnson, Djoudi, Kosmatov, TAP 2024). Grade A.**
  - A `false` proof obligation is generated at "smoking" nodes (requires, assumes, calls, code, loops). Expected SAT means reachable. UNSAT means "dead code or a proven inconsistency in the program specifications". UNKNOWN gives "no guarantee": "smoke test verification is an incomplete process… a test rather than a proof."
  - Thales JavaCard VM: over 7,000 lines of C, over 30,000 lines of ACSL, EAL7. The 2,350 generated smoke tests (363 dead-requires, 150 dead-assumes, 732 dead-call, 1,089 dead-code, 16 dead-loop) cost about 20 min, ≈8%, on top of a more-than-4 h proof of more than 80,000 VCs.
  - Smoke tests "found internal soundness bugs of WP… inside its standard logic library which contains many axioms"; the authors then turned "most of our axioms into proper lemmas or Coq realizations".
  - [Source](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf)
  - **Agents:** human-only.
- **Dafny proof dependencies (Tomb, Dafny blog, Oct 2023, Dafny ≥ 4.4). Grade B.**
  - A goal proved without using the goal itself is "proved … vacuously… because the assumptions in scope… are contradictory, or that location is unreachable". Assumptions never used are redundant. Statements not in any proof dependency are "unconstrained by the verification".
  - Example: a bodiless `Find` whose `ensures start < i < end` is false for adjacent indices lets a caller prove a false assertion.
  - [Source](https://dafny.org/blog/2023/10/27/proof-dependencies/)
- **Dafny wiki "Cautionary Tales". Grade C.**
  - Contradictory `reads`/`modifies` specs on external classes: "Dafny will exploit such contradictions".
  - Advice: "A good way to 'smoke test' proofs is to change some postcondition to its negation and see if the proof still works". The worked example of a precedence error passed verification with `res.Some?` replaced by `res.None?`.
  - [Source](https://raw.githubusercontent.com/wiki/dafny-lang/dafny/Cautionary-Tales.md)
- **ProofPulse (Silva, Martins, Mendes, arXiv 2608.30818, 2026). A-pre.**
  - Three-valued proof coverage (essential / auxiliary / irrelevant) from Dafny unsat cores.
  - "Evaluated against an oracle of 252 programs from the dafny-synthesis benchmark… high-precision signal for specification weaknesses, particularly unnecessary preconditions and vacuous proofs"; "perfect precision for precondition classification" with unsat-core minimisation. "it cannot fully capture semantic intent."
  - [Source](https://arxiv.org/pdf/2608.30818)
  - **Agents:** the programs come from an LLM-synthesis benchmark. The tool is not an agent.

**Weak-spec findings in LLM verification benchmarks [§3-extends Vericoding/DafnyBench]**
- **Vericoding (arXiv 2509.22908). A-pre.**
  - Manual inspection: 5 random successes per language and source.
  - "Dafny exhibited no issues (except for redundant lemmas), with LLMs correctly giving trivial solutions when the specs were weak. Verus showed many weak specs due to spec translation issues… conditioned on vericoding success, roughly 9% of the specs were too weak and another 15% had poor translations."
  - An LLM-as-judge was used to catch `ensures true` substitutions in translated specs. A "handful" of specs admitted trivial solutions from "lossy LLM transpilation or … incomplete human-authored specifications".
  - [Source](https://arxiv.org/pdf/2509.22908)
  - **Agents: measured.**
- **AlgoVeri (arXiv 2602.09464). A-pre.** Criticises Vericoding's Dafny/Verus specs for some tasks: "They only require the result to be within the array bounds (0 ≤ result ≤ Length)… A model could satisfy these specs by simply returning 0." [Source](https://arxiv.org/html/2602.09464v2)
  - *Note:* this partly **[§3-challenge]**s the reading of Vericoding as a "fixed, machine-checked spec" benchmark. Some of its specs are vacuous-strength, so pass rates overstate conformance on those tasks.
- **ReForm (arXiv 2507.16331). A-pre.**
  - RL on Dafny spec generation: "the model exploits the verification reward by issuing weak specifications that trivially satisfy the verifier… omitting unverifiable clauses and producing trivial specifications".
  - Fix: a **subset reward**, where the spec must be at least as strong as ground truth, with weaker preconditions and stronger postconditions, checked formally.
  - In 115 analysed failures of ReForm-3B-RL on Python2Dafny: weak specs 60 (52.2%), unverifiable 51 (44.3%), trivial 4 (3.5%).
  - [Source](https://arxiv.org/pdf/2507.16331)
  - **Agents: measured.**
- **SpecRL (Huang, Zhang, Sun, Sun, Xiong, arXiv 2604.05820; header says IEEE TSE 2026, acceptance not verified). A-pre.**
  - "verification can prove that a specification is sound for the implementation, yet it cannot tell whether the specification is too weak."
  - Builds "spectests" (implementation-impossible input/output pairs) and rewards specs by the fraction rejected. On DafnyComp-Spec, a 7B model gained +49.96% verification success and +26.46% completeness relative over SFT.
  - [Source](https://arxiv.org/pdf/2604.05820)
  - **Agents: measured.**
- **Lahiri, FMCAD 2024. Grade A.**
  - Symbolic testing of specs: **correctness** means the spec admits the reference output on each test; **completeness** means the spec rejects mutated outputs (up to 5 mutants per test). Implemented as a 400-line script.
  - Of 153 MBPP-DFY specs, 64 could be analysed. Manual labels mostly agreed. The tool found at least 3 specs labelled STRONG that were weaker than precise ones (task ids 2, 145, 161), and 3 specs labelled STRONG that failed correctness because of copy errors in tests (e.g., the cube of 5 recorded as 25).
  - [Source](https://arxiv.org/pdf/2406.09757)
  - **Agents: measured.** GPT-4-generated specs among those evaluated.

**Other gates (tool docs)**
- **Alloy tutorial. Grade B.** "no counterexample found. Assertion may be valid… there are no counter examples… within a scope of 5". Bounded; a `run` yielding an instance is constructive evidence of non-emptiness within scope. [Source](https://alloytools.org/tutorials/online/maintext-FS-2.html)
- **TLC coverage.** Search and practitioner threads only: the Toolbox profiler marks actions never enabled; the warning depends on disjunct order when invariants fail early. **[unreachable]** for official docs. Grade C (lead). [Lead](https://discuss.tlapl.us/msg04701.html)

### Inferences
- *Inference:* Gate ladder for the brief's layers:
  1. per clause, an **interesting witness**: an Alloy `run`, a TLC/Apalache trace or a Hypothesis example in which the clause's antecedent fires and its consequent is observable (KV);
  2. per contract, Dafny contradictory/redundant-assumption warnings and Frama-C-style smoke tests, plus a "negate the postcondition, must fail" check;
  3. per model, TLC coverage with zero never-enabled actions and zero dead disjuncts;
  4. per Lean development, `#print axioms` ⊆ the standard set;
  5. a **strength gate**: spec mutants or spectests built from the prose records' scenarios, where wrong outcomes taken from the record's rejected options must be rejected by the spec.
  Step 5 is the only one that catches consistent-but-weak.
- *Inference:* The record format gives step 5 for free. Each decision's concrete scenario is a positive test, and each *rejected option* is a natural negative ("spectest"). A spec that admits a rejected option is too weak or misreads the decision. This links T2 to T1/T3.
- *Inference:* Agents rewarded on "verifies" drift toward weak specs (ReForm). Any agent-facing gate must include a strength criterion that is **not editable by the agent**. This is consistent with the §3 ImpossibleBench/EvilGenie finding.

### Gaps
- No study was found measuring how often LLM-written **TLA+** or **Alloy** models are vacuous (never-enabled actions, empty instances).
- The Beer et al. 1997 figure is secondhand. The Dafny proof-dependency warning has no published false-positive or false-negative rates (ProofPulse is the nearest).

---

## 6. What a "consistent" SMT / Alloy / Lean result does and does not show; reference model plus witness models as constructive satisfiability evidence

### Takeaway
- An **SMT "verified"** result shows that each obligation follows from its assumptions. It does **not** show the assumptions are satisfiable: bodiless or `{:axiom}` contracts and `assume` are taken on faith.
- A **smoke test** is incomplete (UNKNOWN ≠ consistent).
- An **Alloy instance** is real but **bounded** evidence of satisfiability. "No instance" or "no counterexample" is scope-relative.
- **Lean** "cannot check whether new axioms are consistent". Only `#print axioms` audits dependence.
- The strongest satisfiability evidence is **constructive**: an implementation that verifies against the full contract, plus independent implementations that interoperate.

Standards bodies encode this as a gate: W3C "independent interoperable implementations of each feature", IETF "at least two independent interoperating implementations", WebAssembly "two or more Web VMs" plus a reference interpreter passing the test suite. Watt's mechanisation of the Wasm spec found errors that made the type system "originally unsound". No source states *how many* or *how different* witnesses suffice; two independent implementations is a convention, not a measured threshold.

### Cited Findings

**What SMT/deductive "consistent" means**
- **Dafny reference manual, `{:axiom}`. Grade B.** "the post-condition may be assumed to be true without proof. In that case also the body… may be omitted… only prevents Dafny from verifying that the body matches the post-condition. Dafny still verifies the well-formedness of pre-conditions, of post-conditions". Well-formedness ≠ satisfiability. [Source](https://raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/Attributes.md)
- **Dafny blog (B).** An unsatisfiable `ensures` on a bodiless method lets callers prove `assert xs[i] == 42` falsely. [Source](https://dafny.org/blog/2023/10/27/proof-dependencies/)
- **Frama-C/WP (A).** UNSAT on a smoke test means "proven inconsistency"; "when the SMT solver replies UNKNOWN, we have no guarantee"; "it is not complete and is similar to testing… can we ever be sure that our programs are proved well enough?" [Source](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf)
- **SpecRL (A-pre).** Verification establishes soundness relative to the implementation, "yet it cannot tell whether the specification is too weak". [Source](https://arxiv.org/pdf/2604.05820)

**Alloy and Lean**
- **Alloy (B).** Results are scope-bounded: "no counterexample found. Assertion may be valid" within scope 5. [Source](https://alloytools.org/tutorials/online/maintext-FS-2.html)
- **Lean 4 reference, Axioms (B).**
  - "Any proof that relies on an axiom can be trusted only to the extent that the axiom is both true and consistent with the other axioms used. By their very nature, Lean cannot check whether new axioms are consistent"; `axiom false_is_true : False` proves `2 = 5`.
  - "Lean automatically tracks the axioms that each proof depends on so that they can be audited" via `#print axioms`, including `sorryAx` and `native_decide` auxiliary axioms.
  - [Source](https://lean-lang.org/doc/reference/latest/Axioms/)
- **Frama-C team (A).** After smoke tests found WP library inconsistencies: "we have decided to turn most of our axioms into proper lemmas or Coq realizations". This is practice evidence for replacing axioms with definitions plus lemmas, i.e., a model, wherever possible. [Source](https://allan-blanchard.fr/publis/bcdk_tap_2024.pdf)

**Constructive witnesses and multiple implementations**
- **W3C Process (current), §6.3.2. Grade B.** "Implementation experience is required to show that a specification is sufficiently clear, complete, and relevant… to ensure that independent interoperable implementations of each feature of the specification will be realized." The Team considers "is each feature… implemented", "are there independent interoperable implementations", "are there implementations created by people other than the authors". [Source](https://www.w3.org/policies/process/)
- **IETF RFC 6410 (2011). Grade B.**
  - Internet Standard requires "(1) There are at least two independent interoperating implementations with widespread deployment and successful operational experience… (3) There are no unused features in the specification that greatly increase implementation complexity".
  - RFC 2026 previously required "a report that documents interoperability between at least two implementations from different code bases" for Draft Standard.
  - [Source](https://www.rfc-editor.org/rfc/rfc6410.txt)
- **WebAssembly CG phases. Grade B.** Phase 4 entry: "Two or more Web VMs have implemented the feature and pass the test suite… The spec document has been fully updated… The reference interpreter has been fully updated… and passes the test suite." [Source](https://raw.githubusercontent.com/WebAssembly/meetings/main/process/phases.md)
- **Watt, CPP 2018 (Isabelle mechanisation of Wasm). Grade A.**
  - "we identified several errors in the official specification which were acknowledged and fixed by members of the working group. In some cases, these errors meant that the type system was originally unsound."
  - These errors had survived multiple engine implementations and the reference interpreter.
  - [Source](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf)
  - **Agents:** human-only.
- **Constructive witness in requirement tools.**
  - EuRailCheck returns "a trace witnessing the consistency" on success. [Source](https://arxiv.org/pdf/1003.1741v1.pdf)
  - KV's interesting witness is a run that satisfies the spec *non-vacuously*. [Source](https://typeset.io/pdf/vacuity-detection-in-temporal-model-checking-290v578apa.pdf)
- **Vericoding (A-pre).** Weak specs "still make perfectly valid vericoding tasks, just different tasks than originally intended". A passing implementation is a witness of satisfiability, **not** of adequacy. [Source](https://arxiv.org/pdf/2509.22908)

### Inferences
- *Inference:* What witnesses prove and miss:
  - One **reference model** that passes all spec-enforcing checks proves the conjunction is satisfiable, at least on the tested or verified domain. For a Dafny contract with a verified body, that holds on all inputs.
  - It does not prove that each non-commitment branch is realisable. If the reference always picks outcome A of an *unspecified* {A, B}, the spec could forbid B by accident and nobody would notice.
  - It does not prove **realizability** under all environment schedules, only for the schedules exercised, and it does not prove non-vacuity.
  - **Two or more witnesses** add evidence only along dimensions where they **differ**. The Maoz–Ringert and KV results imply witnesses must be chosen to *exercise* antecedents (interesting witnesses), not just to exist.
- *Inference:* How many and how different (proposal; not measured anywhere):
  - at least one witness per **profile/variation-point value** declared (the normal value plus each declared deviation);
  - for each *unspecified*/*indeterminate* set, a witness choosing each allowed outcome at least once (a "branch-covering witness set");
  - for environment actions, witnesses that survive adversarial schedules (fault, cancel, concurrent caller), checked by the history checker.
  This turns the brief §3 seed ("≥2 witnesses with different profile values") into a coverage criterion over the non-commitment register instead of a fixed count of 2.
- *Inference:* The standards evidence is about **clarity and interoperability**, not logical satisfiability. Two independent implementations interoperating shows the prose is implementable *and* read the same way by two teams, which is closer to T1/T5 independence. The Wasm case shows the limit: several interoperating engines plus a reference interpreter did not reveal type-system unsoundness that mechanised proof found. Witnesses complement satisfiability and soundness proofs but do not replace them.
- *Inference:* For Lean structural axioms, prefer `def` + `theorem` over `axiom`. Gate on `#print axioms` showing only Lean's standard axioms. For Alloy, treat "instance found" as evidence and "no instance" as scope-relative. Record the scope with the result.

### Gaps
- **Not found:** any measured study of how many independent implementations or witness models are needed to expose spec contradictions or ambiguities, i.e., a defect yield per additional implementation. The W3C/IETF/Wasm "two" is convention.
- Watt & Rao, "Two Mechanisations of WebAssembly 1.0" (FM 2021), would be direct evidence of dual formalisation cross-checking. Not fetched: **[unreachable]** lead.
- Liskov–Wing as a satisfiability criterion: no new full-text evidence beyond brief §3.
- **Agents:** no study measured agents building multiple diverse witness implementations for satisfiability.

### Source grade list (T2)
| Source | Grade | Full text | Agents measured |
|---|---|---|---|
| Langenfeld et al., Scalable Analysis of Real-Time Requirements, RE 2019 | A | yes | no |
| Becker et al., Hanfor, REFSQ 2021 tools | A-workshop | yes | no |
| Mavridou et al., Compositional Realizability in FRET, FM 2021 | A | yes (NTRS) | no |
| Katis et al., Capture, Analyze, Diagnose, CAV 2022 | A | **[unreachable]** | – |
| Maoz & Shalom, Unrealizable Cores, ICSE 2021 | A | yes (arXiv) | no |
| Maoz & Ringert, Well-Separation of GR(1), FSE 2016 | A | yes (Zenodo) | no |
| Kupferman & Vardi, Vacuity Detection, CHARME 1999 | A | yes | no |
| Beer et al., CAV 1997 | A | **[unreachable]** (quoted via KV) | – |
| Blanchard et al., No Smoke without Fire, TAP 2024 | A | yes | no |
| Dafny blog, Proof dependencies (2023) | B | yes | no |
| Dafny reference manual, {:axiom} | B | yes | no |
| Dafny wiki, Cautionary Tales | C | yes | no |
| Lean 4 reference, Axioms | B | yes | no |
| Alloy tutorial | B | yes | no |
| ProofPulse, arXiv 2608.30818 | A-pre | yes | no (LLM-benchmark programs) |
| Vericoding, arXiv 2509.22908 | A-pre | yes | yes |
| AlgoVeri, arXiv 2602.09464 | A-pre | yes (grep) | yes |
| ReForm, arXiv 2507.16331 | A-pre | yes | yes |
| SpecRL, arXiv 2604.05820 | A-pre | yes | yes |
| Lahiri, FMCAD 2024 | A | yes | yes (GPT-4 specs) |
| SAT-LLM, Fazelnia et al. 2024 | A-pre | yes | yes |
| Cimatti et al., FMA 2010 (EuRailCheck) | A-workshop | yes | no |
| Filipovikj et al., PROPAS | A (venue unverified) | yes | no |
| Calvanese et al., DMN decision tables | A-pre | yes | no |
| TableWise NASA page | C | yes | no |
| Heitmeyer et al., SCR TOSEM 1996 | A | **[unreachable]** (DTIC 403) | – |
| van Lamsweerde & Letier, Monterey 2002/LNCS | A-workshop | yes | no |
| van Lamsweerde et al., TSE 1998 | A | **[unreachable]** | – |
| Degiovanni et al., ASE 2018 | A | yes | no |
| Boundary-condition critique, arXiv 2203.12903 | A-pre | yes (grep) | no |
| ACoRe, arXiv 2303.05213 | A-pre | yes (abstract/intro) | no |
| Nuseibeh, Easterbrook, Russo, IEEE Computer 2000 | A | yes | no |
| Zave & Jackson, TOSEM 1993 | A | **[unreachable]** | – |
| W3C Process | B | yes | – |
| RFC 6410 | B | yes | – |
| WebAssembly phases.md | B | yes | – |
| Watt, CPP 2018 | A | yes | no |
| Leino & Wüstholz CAV 2015; iProperty ICSE 2014; ICLP 2020 push/pop; ECEASST 2018 | – | **[unreachable]** leads | – |
