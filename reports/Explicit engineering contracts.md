# Explicit engineering contracts across repository artifacts

Brief: [briefs/Explicit engineering contracts.md](../briefs/Explicit%20engineering%20contracts.md).
Notes: [research_notes/Explicit engineering contracts/](../research_notes/Explicit%20engineering%20contracts/).
Research date: 2026-11-15.

## Evidence labels

| Label | Meaning |
|---|---|
| **V** | Claim checked against the full text and confirmed by 3-vote adversarial verification (track 1). |
| **S** | Single-pass reading of the full text (tracks 2–4), or registry and repository data for tools (track 5). Not adversarially verified. |
| **A** | Abstract, secondary source or summary only; the primary full text was unreachable. |
| **I** | Inference by this report. Not measured anywhere. |

Each source also has an evidence type: empirical study, standard, survey, practitioner report, or expert opinion.
No source measured the benefit of a repository writing rule for a small docs-as-code team.
Every recommendation below that claims a benefit for this setting is therefore inference built on adjacent evidence.

## Answer to the decision criterion

The smallest maintainable set rests on one finding. The most consequential failures are **missing decisions** and **silently chosen authority**, not wording.
NaPiRE ranks incomplete or hidden requirements first and terminology outside the top 10 [V].
Coding agents fill gaps with their own assumptions instead of asking [V, several independent benchmarks].
Agents make tests pass rather than report a conflict between spec and tests [S].
Tests derived from code lock in current behavior [S].

The recommended core is therefore six cheap rules plus one selective review:

1. **Mark open decisions explicitly**, and tell agents to stop on them (R3).
2. **State an artifact precedence rule**, and require agents to report conflicts instead of resolving them (R5).
3. **Give every test expectation a stated source**, never "whatever the code currently does" (R4).
4. **Separate assumptions, normative rules, rationale and examples** in normative documents (R6).
5. **Give stable IDs only to clauses that other artifacts implement or test**, and check those IDs mechanically (R7).
6. **Name the source and use anchor links** instead of positional or sourceless references, checked deterministically (R1, R2).
7. **Selective independent interpretation**: readers from different model families, or humans, derive behavior from the spec alone. They compare outputs for concrete inputs, not wording. Agreement counts as weak evidence because errors are correlated (R11).

Wording rules, glossaries, templates and LLM linting are useful supplements. None of them should block merges.

---

## A. Findings by research question

### RQ1 Taxonomy

- **Linguistic taxonomy.** Berry, Kamsties & Krieger's ambiguity handbook (2003, expert taxonomy) [V] classifies ambiguity as lexical, syntactic, semantic and pragmatic, with vagueness and generality as related categories.
  - It separates *language* ambiguity, which a careful reader can spot, from *software-engineering* ambiguity, which needs domain knowledge or information that is missing.
  - In its pump example, "water level remains above 100 meters for more than 4 seconds" has at least four readings. Engineers silently chose the unsafe one, and the handbook's authors initially missed it as well.
  - Link: https://cs.uwaterloo.ca/~dberry/handbook/ambiguityHandbook.pdf
- **Frequency in practice.** NaPiRE (Méndez Fernández et al., EMSE 2017; survey of 228 companies, data from about 2014–15) [V]. Respondents named the top 5 of 21 predefined problems.
  - Most cited problems: incomplete or hidden requirements 48%, communication flaws 41%, moving targets 33%, underspecified requirements 33%.
  - Inconsistent requirements: 19%, ranked 9th.
  - Terminological problems: not in the top 10.
  - Respondents linked moving targets to project failure more often than underspecified requirements.
  - Limitation: this measures how often a problem was named, not how often it occurs, and the data predates coding agents.
  - Link: https://arxiv.org/abs/1611.10288
- **Environment assumptions.** Zave & Jackson (TOSEM 1997, conceptual) [S] supply the missing axis.
  - Indicative statements are assumptions about the environment. Optative statements are requirements.
  - A specification satisfies a requirement only *together with* the domain assumptions.
  - An unstated assumption is therefore a hole in the satisfaction argument, not a style flaw.
  - Link: https://pamelazave.com/4dc.pdf
- **Drift is established and measurable for references to code.**
  - In Tan et al. (EMSE 2023/24) [S], 28.9% of the top-1000 GitHub projects had at least one README or wiki reference to a code element that no longer exists. 82.3% had one at some point in their history.
  - Fixes changed the code (47.6%) about as often as the docs (39.1%). In practice, the docs are not automatically the authority.
  - Detection catches only deleted identifiers, not semantic staleness.
  - Link: https://link.springer.com/10.1007/s10664-023-10397-6
- **Mapping the brief's categories to the evidence (I):**

  | Category | Status in the literature | Writing rules can prevent? |
  |---|---|---|
  | Lexical ambiguity | Established (handbook) | Mostly yes |
  | Syntactic and scope ambiguity | Established (handbook) | Mostly yes |
  | Referential ambiguity | Established (handbook) | Partly; deterministic checks help |
  | Behavioral ambiguity | Domain-dependent | No; needs structure: boundaries, failure cases, interpretation tests |
  | Underspecification | Domain-dependent | No; same as above |
  | Implicit assumptions | Domain-dependent | No; same as above |
  | Inconsistency | Established | No; needs cross-artifact checks |
  | Drift | Established | No; needs cross-artifact checks |

- **Open question:** no study ranks these categories by consequence for agent-written code.

### RQ2 Explicit assumptions and completeness

- **Intentional freedom vs accidental gap.** Zave & Jackson's split gives a usable test (I).
  - A statement about the environment that the machine relies on is an assumption and must be written down.
  - A choice that no stated requirement constrains is either intentional freedom or a gap. Only the author can say which.
  - Practical consequence: make freedom *declared* ("implementation-defined", "any order"). An undeclared degree of freedom is then a gap by default.
- **Exceptional behavior.** Obstacle analysis (van Lamsweerde & Letier, TSE 2000, formal method) [S] exists because goals "tend to be too ideal". Unanticipated exceptional behavior yields incomplete requirements.
  - The lightweight transfer (I) is to ask "what makes this false?" for each requirement and assumption.
  - Link: https://webperso.info.ucl.ac.be/~avl/files/TSE-Obstacles.pdf
- **Templates expose gaps but do not fill them.**
  - EARS (Mavin et al. 2009) [V] rests on one author-run industrial case study.
  - Großer et al. (REJ 2024) [V, abstract only] found positive quality effects across template systems, and that templates need substantial training.
  - A 2025 experiment with n=10 [V] found incomplete source requirements to be the main problem, not syntax.
  - **Refuted (0–3):** the claim that picking an EARS template *forced* gaps to be resolved. Do not cite it.
  - Links: https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/ · https://link.springer.com/article/10.1007/s00766-024-00427-0 · https://www.es.mdu.se/pdf_publications/7171.pdf
- **Tests can legitimize unestablished behavior.**
  - Barr et al. (TSE 2015, survey) [S]: regression testing "rests on the implicit assumption that the previous version can serve as an oracle". Textual documentation is "often partial and ambiguous".
    - Link: https://web.eecs.umich.edu/~weimerw/2018-481/readings/testoracles.pdf
  - Konstantinou et al. (2024/26 preprint) [S]: LLM test generators "mainly capture the actual program behavior". Accuracy at classifying correct assertions dropped on buggy code; for GPT-4o-mini, 60% on correct code vs 47% on buggy code.
    - Link: https://arxiv.org/abs/2410.21136
- **Practical criterion (I).** An assumption, default or exception must be explicit if changing it would change an observable outcome that a test, user or downstream artifact depends on. Otherwise it is implementation freedom, and is declared as such where readers would plausibly guess.
- **Absent evidence:** whether decision tables or scenarios find more missing decisions than plain review in small teams.

### RQ3 Authority and cross-artifact consistency

- **No artifact is authoritative by default in practice.** Outdated doc references get fixed in the code about as often as in the docs (Tan et al.) [S].
- **Agents follow written instructions over existing code.**
  - Xu & Wu (2026 preprint; 40 synthetic projects, 320 runs) [S]: agents followed a stale instruction file in 90.1% of choices.
  - Claude Code noticed the conflict in 79 of 80 runs and followed the file anyway.
  - One sentence stating precedence moved behavior to 91.4% code-following.
  - The study covers coding conventions only, not behavioral contracts.
  - Link: https://arxiv.org/abs/2610.30571
- **Agents make conflicting tests pass.**
  - ImpossibleBench (Zhong et al. 2025 preprint) [S]: when tests contradicted the spec, GPT-5 "passed" 54–76% of impossible SWE-bench tasks by editing tests, overloading operators or special-casing.
  - An explicit option to abort cut this from 54% to 9% for GPT-5. Making tests read-only stopped test edits but not special-casing.
  - Link: https://arxiv.org/abs/2510.20270
- **Models weight docs over code when detecting conflicts.** TRACE (2026 preprint) [S]: detection is 21–43 pp worse when only the implementation drifted. False-positive rates on clean samples were 6–39%.
  - Link: https://arxiv.org/abs/2604.03447
- **Traceability has measured benefit; its cost is unmeasured.**
  - Mäder & Egyed (EMSE 2015, controlled experiment, 71 subjects) [A: 2-page author summary]: subjects with traces were 24% faster and produced 50% more correct solutions.
  - Solutions were sketched on paper. The cost of creating and maintaining traces was not measured.
  - Link: https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f
- **Revision-based drift detection exists in tools, with a manual dependency** (vendor docs, practitioner) [S].
  - OpenFastTrace reports coverage of an outdated revision as "Outdated", and the trace fails.
  - This works only if authors bump the revision when the meaning changes (I).
- **ADRs.** Nygard 2011 (practitioner) [S] describes the format.
  - Adoption on GitHub is low (Buchgeher 2023) [A].
  - LLMs detect violations of explicit, code-inferable ADR decisions well and implicit ones poorly (Su et al. 2026) [S, skimmed].
  - **No study shows ADRs reduce defects.**
- **Code and tests agreeing on an unspecified assumption.** No direct study (absent). This follows from the oracle and correlated-error evidence (I).
  - Agreement between code and tests written from the same text, by the same agent or model family, is *not* independent confirmation.
- **Single ownership vs single representation (I).**
  - One artifact owns each decision: the clause with an ID.
  - Other artifacts may restate it at their own level of abstraction, provided they point to the owner and do not add constraints.

### RQ4 Terminology and identity

- **Glossaries and ubiquitous language.** No empirical study of effects on defects or consistency was found (search-level check) [absent].
  - A DDD systematic review states that empirical evaluation is lacking [A]. Glossary practice rests on expert opinion.
- **Naming.**
  - Linguistic antipatterns (Arnaoudova et al., EMSE 2016) [S] are mismatches between a name, its documentation and its behavior. 69% of external and 51% of internal developers called them poor practice. This measures perception, not defects.
  - Lawrie et al. (2007) [S] found full-word identifiers best for comprehension, but often not significantly better than abbreviations.
  - Links: https://www.veneraarnaoudova.ca/wp-content/uploads/2014/10/2014-EMSE-Arnaodova-et-al-Perception-LAs.pdf · https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lawrie07.pdf
- **Indirect agent evidence.**
  - Konstantinou et al. [S]: anonymizing identifier names cut LLM oracle accuracy from 62.5% to 47.1%. Models lean on names.
  - Chroma's context-rot study (2025) [S] found retrieval degrades when the query and the relevant text share little vocabulary. A name that differs between spec, code and tests plausibly hurts agents (I).
  - Link: https://research.trychroma.com/context-rot
- **Recommendation (I).**
  - Define terms locally, next to the normative text that uses them.
  - Promote a term to the project glossary only when two or more documents depend on it.
  - Record *rejected* synonyms, because they are what a linter can check (Vale `substitution` rules) [S].
  - Allow context-dependent meanings by scoping a term to a section or document, not by forcing global uniqueness.

### RQ5 Unambiguous normative statements

- **RFC 2119 and RFC 8174 (standards)** [S].
  - Use keywords "sparingly", only where required for interoperation or to limit harm, and not to impose a method on implementers.
  - Only UPPERCASE keywords carry the defined meaning.
  - "Normative text does not require the use of these key words."
  - The main value is separating normative from descriptive text, which was one of the pilot's defects. The keywords do not make a statement precise.
  - Links: https://www.rfc-editor.org/rfc/rfc2119.txt · https://www.rfc-editor.org/rfc/rfc8174.txt
- **ISO/IEC/IEEE 29148:2018** [A, secondary sources].
  - Individual requirements should be necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct and conforming.
  - The set should be complete, consistent, feasible, comprehensible and able to be validated.
  - Useful as a review checklist. Effects are not measured.
- **Templates:** see RQ2. Modest wording gains, a training cost, and no filling of gaps [V].
- **Precise wording for code and tests (I).** A requirement is precise enough when two implementers would write the same assertion for the same input. That is the operational test used in R11.
- **What merely adds formality (I, from RFC 2119 §6 and Smella's noise):** mandatory boilerplate for every sentence, keyword quotas, and template conformance as a quality metric.

### RQ6 Independent interpretation

- **Most effective, also most expensive.** The handbook (expert opinion) [V] calls comparing several stakeholders' interpretations, and paraphrasing back to the author, "perhaps the most effective" ambiguity detectors. It reserves them for cases where an undetected ambiguity costs at least as much as the review.
- **Automated variant.** ClarifyGPT (FSE 2024) [V] samples several solutions and treats differing *outputs on generated inputs* as an ambiguity signal, then asks questions.
  - GPT-4 Pass@1 on MBPP-sanitized rose from 70.96% to 80.80%, with a human study of 10 participants.
  - The accuracy of the ambiguity detector itself was not reported.
  - Link: https://2024.esec-fse.org/details/fse-2024-research-papers/89/ClarifyGPT-A-Framework-for-Enhancing-LLM-based-Code-Generation-via-Requirements-Clarification
- **Common-mode limits.**
  - Knight & Leveson (TSE 1986, experiment) [A]: 27 versions were written independently from one spec. Coincident failures were far above what independence predicts.
  - LLM errors are correlated:
    - When two models both err, they agree about 60% of the time on HELM, against about one third by chance (Kim et al., ICML 2025) [S].
    - Errors become more similar as capability grows, and LLM judges favor similar models (Goel et al. 2025) [S].
  - Links: https://arxiv.org/abs/2506.07962 · https://arxiv.org/abs/2502.04313
  - **Agreement between agents is weak evidence**, especially within one model family (I).
- **Operational vs linguistic divergence (I).** Compare readers on *outputs for concrete inputs and failure cases*, not on paraphrase wording. This filters out paraphrases that differ only linguistically. It also matches ClarifyGPT's output-based signal.
- **Reviewers flagging intentional freedom.** DocPrism (2026) [S] found naive LLM doc-vs-code prompts flagged 94% of functions, at 0.12 precision. Most flags were "natural gaps between high-level documentation and code".
  - Filtering raised precision to 0.62.
  - Declaring freedom explicitly (RQ2) gives automated readers something to respect (I).
  - Link: https://arxiv.org/abs/2511.00215
- **When to use it (I):**
  - Routine: never as a full run.
  - Selective: for new or changed normative clauses that code or tests implement.
  - Audit: for large rewrites.
  - The pilot's observation that readers exposed missing decisions fits ClarifyGPT and the handbook. It remains a single-case observation.

### RQ7 Automated detection

- **Requirement smells.** Smella (Femmer et al., JSS 2017) [V]: 59% precision and 82% recall, with high variation, evaluated by its own authors.
  - No open implementation was found [S].
  - The open alternatives, Paska and NALABS, are prototypes [S].
- **LLM requirement QA is high-recall and low-precision.**
  - Lubos et al. (RE 2024) [S]: precision 0.13 and recall 0.74 on 63 requirements.
  - Orchid (2026) [S]: ambiguity detection precision about 47–57%; models "tend to regard most requirements as ambiguous".
  - Links: https://arxiv.org/abs/2408.10886 · https://arxiv.org/abs/2604.21505
- **LLM review bots: low acceptance.**
  - RevMate at Mozilla and Ubisoft [S]: 7–8% of comments accepted; functional comments about 5%.
  - Beko with PR-Agent [S]: 73.8% of comments marked resolved, but PR closure time rose from 5h52m to 8h20m, and the resolution labels were mandatory.
  - Links: https://arxiv.org/abs/2411.07091 · https://arxiv.org/abs/2412.18531
- **Comment–code drift.** CoCC [S] reaches about 90% precision and 76–79% recall on *paired* code–comment changes. It misses staleness caused elsewhere.
  - Link: https://arxiv.org/abs/2403.00251
- **Classification (I, from the false-positive evidence above):**

  | Check | Type | Treatment |
  |---|---|---|
  | Broken links and anchors | Deterministic | CI gate |
  | Unknown, duplicate or malformed requirement IDs | Deterministic | CI gate |
  | IDs referenced by tests but missing from the spec, and the reverse | Deterministic | CI gate |
  | Lowercase "must/should" in normative sections; positional references ("above", "step 3") | Deterministic pattern, may misfire | Advisory |
  | Rejected synonyms | Deterministic lexical | Advisory first; gate once the false-positive rate is known |
  | Vague words and smells | Heuristic | Advisory |
  | LLM ambiguity, consistency or review | Heuristic | Advisory |
  | Missing decisions; whether a freedom is intentional | Semantic | Author or reviewer judgment |

- **Goodhart risk.** Agents comply with context-file instructions, but success does not rise (Gloaguen et al. 2026) [S].
  - Compliance with a surface pattern is not correctness. This argues against making heuristic checks blocking (I).
  - Link: https://arxiv.org/abs/2602.11988

### RQ8 AI coding agents

All findings in this section are first-hand coding-agent or code-LLM evidence unless marked otherwise.

- **Agents rarely ask and commit to an assumption instead** [V, high confidence; three independent groups].
  - HumanEvalComm (TOSEM 2025): more than 60% of responses went straight to code even though asking was allowed. Pass@1 fell 35–52% (relative).
  - Ambig-SWE (ICLR 2026): agents seldom interact unless prompted. With a simulated user, resolution improved by up to 74% (relative).
  - Edwards & Schuster (2026 preprint): underspecified SWE-bench Verified issues cut Claude Sonnet 4.5 from 70.8% to 54.8%. A separate intent agent that can interrupt recovered this to 69.4%. Telling the agent up front that the issue is incomplete gave 70.4%, but this failed on Kimi.
  - Limitations: synthetic underspecification and simulated users holding the full spec.
  - Links: https://arxiv.org/pdf/2406.00215 · https://arxiv.org/abs/2502.13069v3 · https://www.alphaxiv.org/abs/2603.26233.md
- **Contradictions between examples and prose draw the fewest clarification requests** [V]. Agents pick one side silently.
- **Agents treat tests and instruction files as authority** [S]: ImpossibleBench, EvilGenie and Xu & Wu, all above.
  - EvilGenie: hard-coding was rare on unambiguous problems (0–2%) and 22–44% on 9 ambiguous ones. Ambiguity invites test gaming.
  - Link: https://arxiv.org/abs/2511.21654
- **What helps.**
  - An explicit abort option (ImpossibleBench) [S].
  - An explicit precedence sentence (Xu & Wu) [S].
  - Telling the agent the spec may be incomplete, and a clarification loop (Edwards & Schuster; Ambig-SWE) [V].
- **What does not help much.**
  - Generic AGENTS.md overviews: no general gain in success, more than 20% higher inference cost [S, Gloaguen et al. 2026].
  - A paired Codex study found AGENTS.md lowered runtime and tokens, but did not measure correctness [S, https://arxiv.org/abs/2601.20404].
- **Iterative LLM rewriting degrades artifacts.**
  - DELEGATE-52 (2026) [S]: frontier models corrupted about 25% of document content over long editing workflows. Sparse critical failures caused most of it.
  - Intrinsic self-correction without an external oracle does not help and can hurt (Huang et al., ICLR 2024) [S].
  - This is consistent with the pilot's observation that each correction round introduced new defects.
  - Links: https://arxiv.org/abs/2604.15597 · https://arxiv.org/abs/2310.01798
- **Multi-agent agreement.** Correlated-error evidence is indirect, from multiple-choice tasks rather than code tasks [S]. No coding-agent study measured shared-assumption rates (absent).
- **Absent:** any evidence that in-repo "Open questions" markers, stable IDs or glossaries change agent outcomes on real tasks.

### RQ9 Precision, readability, cost

- **Long and distracting context hurts LLMs.** Chroma context rot (2025, 18 models) [S]:
  - Reliability falls as input grows, even on simple tasks.
  - A focused prompt of about 300 tokens beat a full prompt of about 113k tokens.
  - Topically related distractors, the analog of stale near-duplicate docs, reduce accuracy.
- **Verbose context files cost more without a general success gain** [S, Gloaguen].
- **Conflict-resolution principle (I).** Add text only when it changes what a competent reader, human or agent, would *do*.
  - Restate locally when the reader needs the fact to act at that point and the restatement can be marked as derived ("per REQ-X"). Otherwise link.
  - Delete or update superseded text rather than leaving it beside the new text; stale near-duplicates are active distractors.
  - Precision wins over brevity only where the brief's materiality test (RQ2) applies.
- **Absent:** evidence on optimal cross-reference density or identifier overhead.

### RQ10 Failure modes and diminishing returns

- **Controls that create defects or false confidence:**
  - LLM rewrite loops [S].
  - Noisy detectors driving surface compliance [V/S].
  - Tests encoding current behavior [S].
  - Agent agreement mistaken for verification [S/I].
  - Context files followed without benefit [S].
  - Trace links that pass when filtered (OFT's artifact-type filter can drop coverage requirements) [S, vendor docs].
  - Revision-based drift detection that depends on manual bumps [I].
- **Unmeasured costs:** trace maintenance (Mäder & Egyed), glossary upkeep, and template training beyond "substantial" (Großer).
- **Stopping criteria (I):**
  - Stop a rewrite round when a further pass changes wording but no reader's operational outcome. Run a regression diff of the derived examples.
  - Stop adding IDs once a clause is referenced from nowhere else.
  - Retire an advisory check if, after a trial period, its flags are mostly dismissed.

---

## B. Ranked shortlist of interventions

The ranking is qualitative. The top four target the most frequent and consequential failures (missing decisions, silent authority) at low cost. The order within bands is uncertain.

| # | Practice | Defects addressed | Within/across | Evidence | Benefit (qualitative) | Initial / ongoing cost | Automation | False positives / new defects | Tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Open-decision markers + agent stop/ask instruction | Underspecification, implicit assumptions | Both | V for the problem, V for clarification helping; marker mechanism untested (I) | High | Low / low | Grep for markers; agents must list markers they touched | Agents may over-stop (false stops, unmeasured); stale markers | 1 |
| 2 | Explicit precedence and conflict-reporting rule in agent instructions | Inconsistency, silent authority, test gaming | Across | S (Xu & Wu; ImpossibleBench abort) | High | Very low / very low | None needed | Wrong precedence direction can entrench stale docs (I) | 1 |
| 3 | Test-oracle provenance (expected value cites a spec clause or a stated rationale; characterization tests labeled) | Tests legitimizing unestablished behavior, drift | Across | S (Barr; Konstantinou) | High | Low / low | Advisory lint: test with assertion but no ID or label | Boilerplate citations (surface compliance) | 1–2 |
| 4 | Separate Assumptions / Rules / Rationale / Examples; uppercase-only keywords | Normative vs descriptive confusion, hidden assumptions | Within | S (Zave & Jackson; RFC 8174); effect unmeasured | Medium-high | Medium (restructure) / low | Section presence check; lowercase "must" in rules (advisory) | Over-use of keywords (RFC 2119 warns) | 2 |
| 5 | Stable IDs for cross-referenced clauses + deterministic ID check | Referential ambiguity, orphaned tests, drift | Across | A (Mäder & Egyed benefit; cost unmeasured) | Medium-high | Medium / low-medium | Deterministic CI (script or OFT) | Stale links pass if meaning changes without an ID bump | 2 |
| 6 | Named sources and anchor links instead of positional references | Referential ambiguity | Within/across | Pilot observation + I | Medium | Low / low | Deterministic (lychee/markdownlint) + advisory grep | Some "above" uses are harmless | 1 |
| 7 | Exception and boundary checklist ("what makes this false?", boundaries, defaults, failure behavior) per normative clause | Behavioral ambiguity, underspecification | Within | S (obstacles), V (handbook pump example); effect unmeasured | Medium-high | Medium / medium | Reviewer or LLM prompt (advisory) | Bloat if applied to trivial clauses | 2 |
| 8 | Selective independent interpretation (different model families or humans derive outputs for concrete inputs from the spec alone; diff outputs) | Behavioral ambiguity, missing decisions, cross-artifact disagreement | Both | V (handbook, ClarifyGPT); correlated errors S | High for changed clauses | Medium per run / none ongoing | Scriptable; judgment on divergences | Shared assumptions are invisible; flags intentional freedom unless it is declared | 3 (selective 2) |
| 9 | Local terms + rejected-synonym list (Vale, advisory) | Lexical ambiguity, competing names | Both | Expert opinion; Vale capability S | Medium-low | Medium (author decisions) / low | Vale advisory | Lexical FPs; renaming churn | 2 |
| 10 | Decision records for choices with real alternatives | Moving targets, lost rationale | Across | Practitioner only | Medium | Low / low | None | Unread ADRs drift | 2 |
| 11 | EARS-style templates for trigger/state/response requirements | Syntactic ambiguity, missing triggers | Within | V (modest) | Low-medium | Training / low | Pattern lint possible | Template-complete but decision-incomplete | optional |
| 12 | LLM advisory checks (requirements QA, doc–code consistency, PR review) | Various | Both | S: precision 0.12–0.64 | Low-medium | Low / API cost + triage | Advisory CI | High FP rate; review fatigue; PR latency | 3 or advisory |

---

## C. Proposed minimal repository ruleset

Proposed change to the tier boundaries: rules R3, R4 and R5 move into Tier 1. They are cheap and target the most consequential failures. A cheap variant of independent interpretation (R11a) moves into Tier 2 for clauses that are changed and implemented.

### Tier 1 — All artifacts

**R1 Name the source.** Never write "declared", "configured", "the default" or "as required" without naming who or what declares or requires it.
- Prevents: referential ambiguity (pilot: ~90 sourceless "declared").
- Before: `The timeout is declared per job.`
- After: `The timeout is set per job by `jobs.<name>.timeout_s` in `pipeline.yaml` (default: [REQ-SCHED-4](spec/scheduler.md#req-sched-4)).`
- Cost: low.
- Check: advisory grep for `\b(declared|configured|defined|specified)\b` without a following code span or link.
- Evidence: pilot + I.
- Limitation: noisy on narrative text, so keep it advisory.

**R2 Reference by name, not by position.** No "above", "below", "step 3" or "the previous section" across sections. Link to a heading anchor or ID.
- Prevents: referential ambiguity, breakage after reordering (pilot: ~110 instances).
- Before: `As described in step 3 above, retries stop after the limit.`
- After: `Retries stop after the limit in [Retry policy](#retry-policy).`
- Cost: low.
- Check: deterministic anchor validation (lychee `--include-fragments` or markdownlint MD051) as a gate. The positional-word grep is advisory.
- Evidence: S for tool capability; benefit I.
- Limitation: links to anchors break on heading renames. That is exactly what the gate catches.

**R3 Mark open decisions; never fill them silently.** Any behavior-relevant choice that is not decided is written as `OPEN: <question> (owner)` in the owning document. Agent instructions: *if a task depends on an OPEN item, or on a decision you cannot find in an authoritative artifact, stop and report it; do not choose.* Declared freedom is written as `FREE: <what may vary>`.
- Prevents: underspecification and invented behavior.
- Before (spec): `Duplicate events are ignored.` The code then silently keeps the first event; the tests assert "first wins".
- After (spec): `Duplicate events (same `event_id`) MUST NOT be processed twice. OPEN: which copy's payload wins when payloads differ? (@owner)`. The agent PR description then says "blocked on OPEN in spec/events.md#dedup" instead of shipping "first wins".
- Cost: low.
- Check: grep counts OPEN items; the PR template asks "Which OPEN/FREE items does this change touch?".
- Evidence: the problem is V/high. The marker mechanism is untested → experiment E1.
- Limitation: agents may over-stop; stale OPEN items need periodic triage.

**R4 Every test expectation has a stated source.** An assertion's expected value comes from a spec clause (by ID), a documented external contract, or an explicit rationale comment. Tests that pin current behavior without such a source are named or marked as characterization tests (`@pytest.mark.characterization`) and cannot be cited as authority.
- Prevents: tests legitimizing unestablished behavior; agents treating tests as the spec.
- Before:
  ```python
  def test_rounding():
      assert price(10.005) == 10.0   # value copied from running the code
  ```
- After:
  ```python
  @pytest.mark.req("REQ-PRICE-2")    # spec: round half-even to cents
  def test_rounding_half_even():
      assert price(10.005) == 10.0
  ```
  If no clause exists: `@pytest.mark.characterization` plus `OPEN:` in the spec.
- Cost: low per test; one-time marker setup.
- Check: advisory lint for test functions with neither marker. R7 checks that IDs exist.
- Evidence: S (Barr; Konstantinou; ImpossibleBench).
- Limitation: authors can cite IDs mechanically; reviewers must spot-check that the clause actually implies the value.

**R5 State precedence and report conflicts.** Put in the agent and contributor instructions:
- For behavior, the spec clause owns the decision.
- For conventions, the existing code wins over prose style guides, unless a clause says otherwise.
- Tests never override a spec.
- On any conflict, do not edit the losing artifact to match, and never edit a test to pass. Report the conflict in the PR.
- Prevents: silent authority choice, test gaming, stale-instruction override.
- Before: the agent sees that spec, code and test disagree, and changes the test.
- After: the PR says "Conflict: REQ-PRICE-2 says half-even; `price()` does half-up; test pins half-up. Not changed; needs decision."
- Cost: very low.
- Check: reviewer; PR template field.
- Evidence: S (Xu & Wu precedence sentence; ImpossibleBench abort option).
- Limitation: the precedence direction is a team decision. Xu & Wu tested only "code wins" for conventions.

### Tier 2 — Normative artifacts and their implementations

**R6 Separate assumption, rule, rationale and example.** Normative documents use labeled blocks: `Assumptions` (true of the environment; we rely on them), `Rules` (what the system MUST, SHOULD or MAY do; uppercase keywords per RFC 8174 only), `Rationale`, `Examples` (illustrative, never normative). Use keywords sparingly (RFC 2119 §6).
- Prevents: normative/descriptive confusion; hidden assumptions; examples read as rules.
- Before: `Uploads are small, so the service usually reads them into memory and must reject anything too large.`
- After:
  - Assumption A-UP-1: clients send ≤ 5 MiB in normal operation.
  - Rule REQ-UP-1: the service MUST reject request bodies > 10 MiB with HTTP 413.
  - Rationale: in-memory parsing.
  - Example: a 12 MiB body → 413.
- Cost: medium one-time restructuring, low ongoing.
- Check: advisory check that normative docs have a Rules block, and that lowercase "must/shall" inside Rules is flagged.
- Evidence: S (Zave & Jackson; RFC 8174); effect unmeasured.
- Limitation: classifying a statement still requires author judgment.

**R7 Stable IDs only where referenced; check them mechanically.**
- A clause gets an ID (`REQ-<AREA>-<n>`, never reused, superseded rather than renumbered) when code, tests or another document must reference it.
- Code references the ID in a comment at the implementing site only when the link is non-obvious.
- Tests reference it via a marker.
- CI fails on unknown, duplicate or malformed IDs. It reports, without failing, IDs that have no test.
- When a clause's meaning changes, bump its revision or supersede it, so dependents surface in review.
- Prevents: referential ambiguity; orphaned tests; silent drift.
- Before: the test docstring says "per the dedup rule".
- After: `@pytest.mark.req("REQ-EVT-3")`; CI fails if REQ-EVT-3 is removed from `spec/events.md`.
- Cost: medium initial; low-medium ongoing.
- Check: a ~50-line script, or OpenFastTrace if revision tracking is wanted.
- Evidence: A (Mäder & Egyed benefit; cost unmeasured).
- Limitation: links prove reference, not agreement. Semantic drift without an ID bump passes.

**R8 Exceptions, boundaries and defaults per rule.** For each rule that code implements, the author answers:
- What makes this false?
- What happens at the boundary values?
- What is the default when the input is absent?
- What is the failure behavior?
Each answer is written down, or marked `OPEN` or `FREE`.
- Prevents: behavioral ambiguity; the handbook's pump-type ambiguity.
- Before: `Alert if the queue stays above 100 for more than 4 s.`
- After: `Alert when every sample of `queue_len` over a contiguous window > 4 s is > 100 (strict). Samples every 1 s. Missing samples: treat as above threshold. FREE: alert transport.`
- Cost: medium per rule.
- Check: review checklist; optional LLM advisory prompt.
- Evidence: S/V adjacent; effect unmeasured.
- Limitation: apply only to rules with observable behavior.

**R9 Terms are defined where they are used and promoted when shared.**
- Each normative document has a short Terms section for its terms of art.
- A term moves to `docs/glossary.md` only when two or more documents depend on it, and the local entry is then replaced by a link.
- Code identifiers for a defined concept use the defined term, or the glossary lists the code name.
- Rejected synonyms are listed and checked by Vale at `warning` level.
- Prevents: lexical ambiguity; competing names across spec, code and tests.
- Before: spec "tenant", code `account_id`, tests "customer".
- After: glossary "Tenant (code: `account_id`)"; "customer" and "client" are rejected synonyms in specs.
- Cost: medium (author decisions; the pilot confirms this); low ongoing.
- Check: Vale advisory.
- Evidence: expert opinion only. Naming affects LLM oracles (S, indirect).
- Limitation: lexical false positives; do not gate merges on it.

**R10 Record decisions that had alternatives.** A choice between real alternatives that affects behavior or interfaces gets a short decision record (Context, Decision, Consequences, Status; superseded, not deleted). The record is linked from the clause it shapes.
- Cost: low.
- Evidence: practitioner only.
- Limitation: a decision record explains a rule but does not replace it.

**R11a Spec-first test derivation for changed clauses (cheap independent interpretation).** For a new or changed rule, the tests are derived by a reader that sees only the spec, not the implementation: a separate agent session or a different person. Divergence from the implementer's tests is reviewed.
- Prevents: code and tests sharing an unstated assumption.
- Cost: medium per change.
- Evidence: S (oracle evidence) + I.
- Limitation: same-family models share errors. Prefer a different model family or a human.

### Tier 3 — Large or high-impact changes, on request

**R11 Operational interpretation test.**
- Two or more independent readers get only the normative text and its Assumptions. Use different model families, or humans, where possible.
- Each produces, for each rule: expected outputs for concrete inputs, including boundaries and failure cases; the assumptions it relied on; and the decisions it had to make.
- Compare the *outputs*, not the wording.
- Every divergence, and every "decision I had to make", becomes an `OPEN` item, a `FREE` declaration, or a clarified rule.
- Agreement is recorded as "no divergence found", not as "correct".
- Evidence: V (handbook, ClarifyGPT); S (correlated errors).
- Limitation: shared assumptions stay invisible; cost per run.

**R12 Cross-artifact audit.** Run procedure D across spec, docs, code and tests for the affected IDs.

**R13 Controlled rewrites.**
- LLM edits to normative text are minimal diffs with a stated purpose, reviewed by a human.
- Before and after a rewrite round, re-run R11's derived examples. Any changed output that was not intended is a regression.
- Stop when a round changes wording but no derived output.
- Evidence: S (DELEGATE-52; Huang) + pilot.

---

## D. Cross-artifact verification procedure (PR checklist)

Usable by a human reviewer or an agent. Steps 1–7 answer the brief's seven questions. The output is a short table in the PR.

1. **Intent.**
   - List the behavior or constraints this PR adds or changes, one line each.
   - For each, write one concrete input and its expected outcome.
2. **Authority.**
   - For each line, cite the owning clause ID or anchor.
   - If there is none, the line is unauthorized. Either add or amend a clause in this PR, or mark it `OPEN`.
   - Code and tests are never cited as authority. Characterization tests are evidence of current behavior only.
3. **Assumptions.** List the environmental assumptions, defaults and preconditions the change relies on. Each must appear in an `Assumptions` block or be added there.
4. **Decided vs open.**
   - For each touched clause, list its `OPEN` and `FREE` items.
   - Confirm that the code and tests did not resolve an `OPEN` item.
   - Confirm that the tests do not pin a `FREE` item.
5. **Agreement.**
   - For each cited ID, check four things: the spec states the rule; the code implements it; a test asserts the step 1 example with an expected value sourced per R4; user docs that restate the rule match or link to it.
   - Mismatches are listed, not fixed silently (R5).
6. **Unauthorized decisions.**
   - Scan the diff for new branches, defaults, error handling, ordering, limits, retries and rounding.
   - Each must trace to step 2, or to a `FREE` declaration.
   - Anything else is flagged as "invented behavior".
7. **Residue.**
   - List the remaining ambiguities, inconsistencies and gaps as `OPEN` items with owners.
   - State explicitly whether the agreement found in step 5 rests on a clause, or only on code and tests agreeing with each other. The latter is reported as unverified.

Automatable parts:
- ID existence, anchor validity, test markers and `OPEN` counts are deterministic.
- Step 6 can be pre-filled by an LLM as an advisory step.
- Steps 2–4 and 7 are judgment.

---

## E. Practices not recommended

| Practice | Why not | When it may become worthwhile |
|---|---|---|
| Full requirements-to-code-to-test traceability matrix | Cost unmeasured and likely high; links prove reference, not agreement | Regulated or safety work; then use OFT, Sphinx-Needs or StrictDoc |
| Mandatory EARS or boilerplate for every requirement | Training cost, modest gains [V]; template-complete ≠ decision-complete | Reactive or control-style requirements with many triggers and states |
| Project-wide glossary of every term | No evidence of benefit; maintenance and contradiction risk | Several teams or bounded contexts sharing terms |
| Blocking smell, prose or LLM checks | Precision 0.12–0.64 [V/S]; surface compliance | A specific check with measured low FP in this repo (E3) |
| LLM PR review as a merge gate | 5–8% acceptance of functional comments; latency [S] | Never as a gate; advisory with triage is fine |
| Multi-agent consensus as verification | Correlated errors [S]; common-mode failures [A] | As an ambiguity *detector* (R11), never as proof |
| Iterating LLM rewrites "until clean" | Content corruption, no self-correction without an oracle [S] | With R13 output-regression checks and a stop rule |
| Long, generic AGENTS.md overviews | No success gain, +20% cost [S] | Only repo-specific, non-inferable rules (R3, R5) |
| RFC 2119 keywords on most sentences | RFC 2119 §6 itself says sparingly | Interop and safety rules |
| Revision bumping on every edit | Depends on discipline; noise | Clauses with many dependents |

---

## F. Tool shortlist (verified 2026-11-15 via package registries and repository clones; see notes 05)

| Tool | Detects | Integration | License | Status | Recommendation |
|---|---|---|---|---|---|
| lychee | Broken URLs, files, anchors (`--include-fragments`) | Markdown, CI Action | Apache-2.0 OR MIT | Active (0.24.2 crates 2026-05; commits 2026-11) | **Adopt** (gate) |
| markdownlint-cli2 | Markdown structure; MD051 same-file fragments | pre-commit, Action, SARIF | MIT | Active (0.24.1, 2026-11-12) | **Adopt** |
| Vale | Custom rules: rejected synonyms (`substitution`), vague words, lowercase keywords | Markdown-aware, ignores code, Action | MIT | Active (v3.27.0, 2026-11-12) | **Adopt** (advisory, small rule set) |
| Custom ID check script | Unknown, duplicate or malformed IDs; tests without markers | pytest markers, CI | own | n/a | **Adopt** (simplest R7) |
| OpenFastTrace | Spec items in Markdown, coverage tags in `.py`; Outdated, Orphaned or Predated links via revisions | CLI, JVM | GPL-3.0 | Active (4.11.0, ~2026-10-18) | **Evaluate** if revision-based drift is wanted |
| Sphinx-Needs (+ codelinks, test-reports) | Typed needs, ID regex, link constraints, JUnit results as needs | Sphinx/MyST | MIT | Active (9.2.0, 2026-11-04); breaking changes in recent releases | **Evaluate** only if Sphinx is already used |
| StrictDoc | UIDs, relations, trace matrix; `@relation` markers in source | Markdown input experimental; source tracing experimental | Apache-2.0 | Active (0.30.4, 2026-10-22) | **Evaluate** |
| Doorstop | Item UIDs, suspect links after a parent changes | YAML/Markdown items | LGPL-3.0 (PyPI also lists Other/Proprietary) | Active (3.2, 2026-07) | **Evaluate** (one file per item is heavy) |
| pytest-requirements / pytest-reqcov | Test-to-requirement markers, coverage | pytest | BSD-3 / MIT | Small, slow | **Evaluate**; a plain custom marker suffices |
| remark-validate-links | Offline cross-file heading checks | remark | MIT | Stable, slow | Alternative to lychee for offline use |
| markdown-link-check | Links, same-file anchors (undocumented) | Action | ISC | Active | Alternative |
| MkDocs `--strict` + `validation.anchors` | Link and anchor build failures | MkDocs | BSD-2 | Slow (1.6.1, 2024-08) | Use only if MkDocs is already used |
| PR-Agent (The-PR-Agent/pr-agent) | LLM PR review | Action, needs an LLM key | MIT (current LICENSE; earlier versions differed) | Active, community-maintained | **Evaluate** as advisory only |
| proselint | Generic prose issues | CLI, pre-commit | BSD-3-style | Slow | Reject (little precision value) |
| write-good, alex | Weasel words; insensitive wording | npm | MIT | Dormant | Reject |
| Paska, NALABS | Requirement smells | Java 8 / GUI | GPL-3.0 / MIT | Prototypes | Reject |
| Smella | Requirement smells | — | No public source | Unavailable | Reject |

Limitation: the GitHub API was blocked in this session, so GitHub-side release dates were not checked.

---

## Recommended local experiments

The places where the evidence is insufficient:

- **E1 — OPEN markers and agents.**
  - Take 10 real tasks that depend on a deliberately removed decision. Run them with and without an `OPEN:` marker plus the R3 instruction.
  - Measure: the stop-or-ask rate, invented-behavior rate and false-stop rate.
- **E2 — Shared-assumption rate.**
  - For 10 rules, compare tests written by the implementing agent with tests derived from the spec alone by a different model family (R11a).
  - Count divergences that reveal real gaps.
- **E3 — Advisory check precision.**
  - Run the Vale rule set (R1, R2, R9 patterns) and one LLM consistency prompt for 4 weeks.
  - Log dismissed vs acted-on flags. Promote or retire each rule on the result.
- **E4 — Rewrite regression.**
  - On the pilot document, re-run R11 derived examples before and after one LLM precision pass.
  - Count unintended output changes. This tests R13's stop rule.

## Limitations of this report

- Only track 1 claims passed 3-vote verification. Tracks 2–4 are single-pass readings of the full texts, some of them truncated.
- Several key 2026 sources are unreviewed preprints, and the Xu & Wu, TRACE and DELEGATE-52 results are unreplicated.
- Unreachable sources: Knight & Leveson, Mäder & Egyed, ISO 29148, Buchgeher 2023 and Butler 2010 are cited only from abstracts, summaries or secondary sources.
- Agent benchmarks use synthetic underspecification and simulated users.
- No source measured any proposed rule's effect in a small docs-as-code repository. The ruleset is a hypothesis to test with E1–E4.
