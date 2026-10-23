# Changelog: Black box boundary spec methods

v1 is the commit tagged `report-v1` (`reports/Black box boundary spec methods.md` there); v2 is the current report.

## v2 (2026-10-22): full-text verification pass

This is the corrected edition of the report. A verification pass on 2026-10-22 checked its claims against full texts. Each item below says whether the **evidence changed** (substantive) or the item was **restyled or re-cited** with no change of conclusion. IDs refer to `research_notes/Black box boundary spec methods/2-verification/verification_log.md`.

**Kernsatz (the opening paragraph and § 1)**
- *Substantive (the evidence changed, the conclusion did not).* "No published rule maps specification category to level to form" now reads **"no validated rule"**. Disconfirming search (a) found coarse published heuristics: van Lamsweerde 2000, NASA-GB-002-95/001-97 and Wing 1990. They map the kind of behaviour, or the purpose of analysis, to a specification paradigm, and they agree with the quantifier rule. The rule is therefore a refinement of published heuristics, not a synthesis with no precedent (T1-Q7).
- *Substantive (a factual correction).* Cedar's credit is corrected. ShardStore found crash-consistency and concurrency bugs. Cedar found validator-soundness, termination, parser and evaluator divergences, and none of them was a crash or concurrency bug (T3-20).
- *Substantive (figure).* "Agents conform well to fixed specs" is now anchored on the best single model, which solved 67.5 % of Dafny tasks. The 82.2 % figure is the nine-model union (T5-01). The direction of the finding is unchanged.
- *Substantive (evidence added, direction unchanged).* "No controlled study shows that any written format helps agents more than another" still holds as worded. The broader claim that no format study exists is narrowed. Three controlled single-shot LLM comparisons exist: VeCoGen (A), the Gherkin pilot (A, weak) and a compact-encoding null result (A-pre). None shows a notation beating prose, and none covers agents, EARS or decision tables (T5-33).
- *Substantive, minor.* History predicates are now stated over **operations with an invocation–response interval**, because interval models exist (T2-15, T2-19). Variation-point values come from published **partial orders**, not lattices (T4-09).
- *Restyled.* § 1 is compressed to three sentences, as brief § 9.1 requires. The Carrizo citation now says that "little validation" refers to earlier elicitation-selection frameworks (T1-01). The Darlington and SCR table claims now cite the alternate primaries that were actually read (T1-10, T3-02).

**Form rule (§ 2.3)**
- *Substantive (provenance).* The rule now refines published coarse heuristics, and no validated rule exists. Its content is unchanged (T1-Q7).
- *Substantive (new evidence).* Completeness and disjointness of a finite case split can also be machine-checked in a contract language, through ACSL `complete behaviors` and `disjoint behaviors`. The check belongs to the case split, not to tabular notation. A table remains the default companion.
- *Substantive (an inference weakened).* Interleaving claims may range over interval operations. A whole-stream read can be recorded as **one interval operation** unless the claim allows mixed versions. Per-chunk recording is no longer mandatory (T2-23).
- *Substantive (new evidence).* The profile row must now say whether a profile is a **static record or a runtime probe**, and it must note that a probe's "false" may mean "unknown" (WebAssembly 3.0, Hadoop PathCapabilities; T4-23, T4-13).
- *Restyled.* The ShardStore principle is now quoted exactly (T1-36). In step 4, Burckhardt's eventual visibility is confirmed in substance, and "standard example" is marked as inference (T1-37).

**Scorecard (§ 7.1)**
- *Substantive (score lowered).* Row e, running example: ● becomes ◐. ShardStore did **not** use sets of outcomes: it rejected them because they "blow up quickly" and used a has-failed flag instead. It also did not check concurrent crashing executions (T3-18).
- *Substantive (figure fix, score unchanged).* Row c, P5: 8.6 % is the figure for the 25 open-weight models. The best frontier figures are GPT-5 at 26.9 % TLC passes on 26 specs and Opus 4.5 at 16 % on TLA+-Bench, and both are sensitive to grading (T5-07, T5-08). The row's running-example cell now cites existing interval and environment models. Its cost note adds Lamport's remark that open-system specs are "seldom" written.
- *Substantive (reinterpretation, score unchanged).* Row g, P5: "ambiguity → hacking (EvilGenie)" becomes "**a suite stricter than, or contradicting, the spec → hard-coding**". EvilGenie's "ambiguous" set is 9 problems with spec–test conflicts (T5-16).
- *Substantive wording, scores unchanged.* Row d now refers to a partial order with incomparable values, and its hard-case cell adds "O2 vs O3 not distinguished" (T2-20, T4-09).
- *Re-cited, scores unchanged.* Row g, P3: HADOOP-13502 introduced two guarantee flags and kept `is-blobstore` as an informational flag (T4-14). Row h now gives the Gherkin pilot's actual result and its peer-reviewed status (T5-27). Row i now cites the 67.5 % single-model rate. Row a gains a cost note from Estler et al.: contracts in practice are mostly null checks.

**Shortlist (§ 7.2) and bake-off (§ 7.3)**
- *Composition unchanged; substantive in the expected failures.*
  - Shortlist 1: its reference model "returning allowed-outcome sets" is marked as inference, with ShardStore's blow-up warning. The concurrent-crash cell is named as unchecked in the best-evidenced practice. "Lattice" becomes partial order. The S3 and Hadoop FSDataInputStream wordings are offered as two witness profile values (inference).
  - Shortlist 2: the agent-authoring figures are corrected. Two cost signals are added: Lamport's "seldom", and the substep-linearizability warning that interval-sequential specs are hard to write (A-pre). The CACM 2025 quote is marked unverifiable.
  - Shortlist 3: "ambiguity → reward hacking" becomes "a suite stricter than the contract invites hard-coding". Hadoop's own suite excludes concurrency. AUTOSAR's "optionally" is marked as not re-checked.
- *Substantive (figures and criteria).* The cost baseline moves from 14 % to **12–13 % of the code base (≈ 20 % of the implementation, reference models ≈ 1 %)**, and Cedar's 3.4 : 1 proof-to-model ratio is added (T3-12, T3-Q3). New criteria: an EvilGenie-style case (a clause that allows a set of outcomes, checked by a single-outcome test) under tamper resistance; "kind labels gate no test" under profile isolation; request-or-refuse and static-versus-runtime profiles under expressiveness.

**Variation rule (§ 4)**
- *Substantive.* The narrow-only rule gains **direct normative precedent**: SQL-92 SET TRANSACTION General Rule 5, and WebAssembly 3.0 profiles that "do not add syntax or alter behaviour" (T4-09, T4-23).
- *Substantive.* Three additions to the composite rule. Narrowing is judged against a stated reference set of excluded behaviours, because the order is partial (Berenson: REPEATABLE READ »« SI). Profiles are declared static or runtime-probed. A fourth mechanism is added: a caller-requested guarantee that the implementation must honour or refuse (Hadoop PathHandle, SQL SET TRANSACTION, JDBC).
- *Re-cited.* HADOOP-13502 replaced `is-blobstore` for test gating with two flags, `create-overwrites-directory` and `create-visibility-delayed`, and kept `is-blobstore` as informational. HADOOP-13501 was closed Won't Fix (T4-14). PEP 3116's buffered strengthening is superseded: current Python docs declare a two-valued variation point instead (T4-05).

**Other corrections that do not move a conclusion:**
- ShardStore's overhead comparison is "3–10×", not "2–10×" (T3-13).
- The ShardStore quote is "our validation checks can miss bugs" (T3-15).
- Jepsen `:info` comes from the Jepsen tutorial, not the README (T1-24).
- The C11 terms come from N1570, not WG23 N0245 (T1-22).
- The JML frame default differs between versions of JML (T1-12).
- Only I/O automata are input-enabled; CSP processes can refuse events (T2-06).
- The Cosmos DB spec explained and proposed a fix for an outage; it did not fix it (T2-09).
- Updated agent figures:
  - AGENTS.md shows no significant effect on success (A-workshop; T5-23).
  - TiCoder is now cited from its TSE 2024 figures (T5-11).
  - nl2postcond found 64 bugs from 70 methods (T5-09).
  - The oracle study now says "below 50 % in some cases" (T5-18).
- The C compiler post names no line-count ceiling (T5-29).
- Barr et al. classify oracles; they do not rank them (T3-22).
- ioco is now cited to Tretmans 2008 (T3-06).
- Grade changes:
  - Up: Vericoding, When Prompts Go Wrong, the Gherkin pilot, the buggy-code oracle study and Lüttgen & Vogler.
  - Down: OMG UML14-209, NetBSD PR 58929, the JML tech report, the NRL SCR reports and the Lynch retrospective.
  - AGENTS.md is regraded as A-workshop.
- 17 of the 23 † items lost their mark; 4 keep it in part and 2 in full (see § 8.1).

