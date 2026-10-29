# Observation record completeness and consistency

Brief: `briefs/Observation record completeness and consistency.md`. Notes:
`research_notes/Observation record completeness and consistency/` (T0 own
trials with their scripts, T1 to T5, verification log). Test material:
`haalfi/remote-store` at `eb08d990e`: OP-01's record, the axes, audit-025 and
RFC-0028.

## 1. Kernsatz

Most of what the current review asks a reader to judge can become
mechanical: slots per Environment row × step and per declared table domain,
a typed claim for every closed list, unconditioned rule and adopted option
checked against every other claim on every amendment, and each Decision
claim aligned to a span of its answer. What stays judged is the extraction
itself, validated only by a second independent extraction, and the
candidates the mechanical checks raise; measured LLM conflict and fidelity
judges are too weak to be more than lead generators. A record is not done
when a round finds nothing or when two same-kind readers overlap (no
capture-recapture estimator was accurate below four inspectors, and on
OP-01 two LLM readers' overlap implied 0.2 remaining just before a reviewer
of another kind found four); stop on per-kind gates calibrated by seeded
defects, after the mechanical checks are clean.

## 2. Per track

Agent applicability uses the brief's wording: either agents were measured
on that step (with the result), or the method is "human-only evidence".

### T1. Completeness

| Option | Evidence, grade | Catches | Misses | Cost | Agents |
|---|---|---|---|---|---|
| **Slot per required item** (fill, or mark not applicable with a reason), pushed down from axes to cells: Environment row × step s1 to s4 (AX-7), Environment row × AX-10 to AX-13 | Leveson 2000, A (3-0) | empty slots, mechanically | wrong fillings; slots the template lacks (class 4) | low: a script over a declared grid | human-only evidence |
| **Table completeness over declared domains** (settled, SCR) | settled | gaps and overlaps in a table | the Environment list: "they do not guarantee that all assumptions about the environment have been specified" (Leveson 2000) | low once domains are declared | settled earlier |
| **STPA guide-words over controllers O1, O2, O3, world and runtime** (not provided, provided, too early or too late, stopped too soon) to generate candidate Environment rows | Abdulkhaleq & Wagner, A-pre (3-0): recall 0.443 vs FMEA 0.326 vs FTA 0.231; n = 3 student groups of 7 | missing environment actions and timing variants | over half of a reference set, even for the best method | about 25% more time than FMEA | human-only evidence |
| **Obstacle test per decision**: does a candidate action, with the domain, falsify a decided outcome? | van Lamsweerde & Letier, A (2-1); claims of certified completeness and validation refuted 0-3 | whether a candidate action is relevant | completeness; needs each decision as a condition | high per decision | human-only evidence |
| **Caller-use reading** (write a usage scenario per handed-out object, form and familiar idiom) for questions no axis raises | *Inference* from OP-01: C7 and G1 to G4 came from this kind of reading (audit-025 § 5) | class 4 questions | anything not tied to use | one reader | not measured |
| **Axis-escape rate across records**: per late item, does any axis question ask it literally? | *Inference*; OP-01 before RFC-0028 P4: 5 of 13 items (C7, G1 to G4) | weak axes, over time | nothing within one record | low | not measured |

Findings:

- The settled table check cannot certify the Environment.
- The one measured enumeration method (STPA) recalled under half of a
  reference set.
- No surviving source measures a technique that surfaces questions **no**
  checklist raises.
- How a checklist is validated for coverage has no surviving evidence. The
  axis-escape rate is a proposal.

OP-01's late Environment finds fit STPA's shape: O3 actions and world
states the list did not name, such as O44 (metadata only), O21 (`a` and
`a/b` together) and O43 (a second host's cache). That fit is *Inference*.

### T2. Internal consistency

| Option | Evidence, grade | Catches | Misses | Measured | Agents |
|---|---|---|---|---|---|
| Checklist reading | Porter, Votta & Basili 1995, A (3-0) | some defects | no better than ad hoc | — | human-only evidence |
| PBR vs checklist, individual | Fabbri et al. TR, B/C (3-0) | — | no significant technique effect; the document effect is significant | 11.7% vs 13.8% of known defects per reader | human-only evidence |
| Scenario (defect-class) reading | Porter et al. 1995, A | more than checklist in one study | replications failed to reproduce it (lead, not verified) | — | human-only evidence |
| Pairwise NLI conflict detection | Fazelnia et al. RE 2024, A-pre (3-0) | two-statement conflicts | composite conflicts, by construction | F1 22 to 55%; P 19% at R 80% (Library) | NLI model |
| Pairwise or whole-set LLM | same; ALICE, A; SAT-LLM, A-workshop | a few composite conflicts (GPT-4: 25%) | most conflicts | GPT-3.5 F1 9 to 30%; GPT-4 R 0.31; GPT-3 found 0 of 26 industrial | yes, 2023-24 models |
| LLM extraction to logic, then solver (MUS) | SAT-LLM, A-workshop; ALICE, A (3-0); **authors evaluating their own tools** | composite conflicts | extraction errors, **unmeasured in every source** | SAT-LLM P 1.00, R 0.83 (n = 15 sets); ALICE 65% recall at 94% precision on 26 industrial | yes |
| **Typed claim register** (own proposal): `Closed(list, domain)`, `Rule(condition → outcome)`, `Adopts(decision, option text)`, `Member(x, domain)`; check Closed × Member, Rule × outcome, Adopts × later claims | own trial on OP-01, lexical precursor only | the four OP-01 shapes the brief names | anything the extraction misses | lexical version: 4 of 7 known extent defects | not measured |
| **Re-run on every edit** (structured rationale) | SEURAT, Burge 2005, A: checks re-run "whenever an alternative or one of its arguments is modified" | contradicted selections; one argument for and against; a selected alternative opposed by another | prose | no yield measured | human-only evidence |

**Own trial (T0, `own_trial_op01.py`).**

- The authors' consistency checks named 61 of 946 decision pairs. They
  covered **4 of the 27 known defect pairs** in O14 to O44, and caught none
  of those four. This measures class 1.
- Selecting pairs by shared vocabulary kept 24 of 27 known pairs only at
  368 of 946 pairs judged.
- The misses were *general clauses* that share no vocabulary with what they
  govern: D1's parity against D12 and D13, and D33's principle against D28.
- A lexical "only/every" register missed every extent defect stated as a
  table row, a table read as complete, or an unquantified rule (O28, O33,
  O37).

**Disconfirming search (a): partly confirmed.** Checklist reading did not
beat ad hoc reading. PBR did not beat checklist reading per reader in the
surviving replication. Scenario reading had one positive study and failed
replications. The document mattered more than the technique.

**Disconfirming search (b): largely confirmed for the measured setups.**

- Pairwise detectors ran at precision 19 to 67%. On the hardest datasets
  that means three to five false alarms per real conflict (*Inference* from
  precision and recall; neither paper analysed false positives).
- Only the solver hybrids had high precision, in small studies their own
  authors ran. All models are 2023-24.

### T3. Fidelity to the dialog

| Option | Evidence, grade | Catches | Misses | Measured | Agents |
|---|---|---|---|---|---|
| Asked-line pairing (in place) | — | missing or ambiguous pairs | content beyond the answer | — | script |
| LLM judge, decision vs dialog | TofuEval, A: open-source judges at 50 to 60% balanced accuracy; GPT-4 best, 64.9 to 90.3; main-topic errors 10 to 20 points harder for GPT-4 | added facts | implied, on-topic additions, which are the record's case | GPT-3.5 detected 50% of extrinsic-information errors | yes |
| Non-LLM factuality metrics (AlignScore, SummaC, QAFactEval) | TofuEval, A; Ramprasad et al., A | extrinsic additions, with higher recall than LLM judges | false alarms; QAFactEval span F1 8.54 on LLM dialog summaries | as stated | metric models |
| Few-shot LLM span detector | Ramprasad et al. ACL 2024, A; **authors evaluating their own tool** | about a third of inconsistent spans | two thirds | span F1 33.22 (P 35.6, R 31.1) | yes, ChatGPT |
| **Claim-to-span alignment** (own proposal): split the Decision into atomic claims; each needs a span in the answer or in the option the answer chose | *Inference* | claims with no source span | claims with a misleading span | untested | not measured |
| **Dialog-to-record diff** where the log copies option text verbatim | *Inference* from O40 | dropped option text | paraphrased drops | untested; mechanical | not measured |

Base rates:

- About 23% of GPT-4 dialog summaries had an inconsistency, and about 38%
  of errors were "circumstantial inference": implied, not stated (A, 3-0).
- In TofuEval, 14.4 to 27.8% of summary sentences were inconsistent.
  "Extrinsic information" made up about half of the inconsistent sentences,
  a share the verifier computed from the released data.
- GADR (A-pre, authors' own tool) observed the same mechanism in an LLM
  agent writing ADRs from meeting transcripts. It "transformed tentative
  discussions into accepted decisions", imported figures from retrieved
  ADRs, and its self-critique loop had no check against the transcript.
- *Inference:* OP-01's class 2 (O14 to O16, O31, O33, O36, O37) is
  circumstantial inference on the dialog's **main topic**, the case the
  measured judges handle worst. An LLM fidelity judge yields leads, not
  verdicts.

### T4. Stopping

| Option | Evidence, grade | Accuracy | Conditions | Agents |
|---|---|---|---|---|
| Capture-recapture, Mh-JK | Briand, El Emam, Freimut, Laitenberger, TSE 2000, A; Petersson et al. JSS 2004, A | below 4 inspectors: "no estimator yields satisfactory results" (±20%). Mh-JE median RE −52% at k = 2 and −27% at k = 3. At 4 or more, Mh-type models had median RE 5 to 16% | at least 4 inspectors; independence; closure; a mature, homogeneous team; seeded defects (matching trivial) | human-only evidence |
| Chao estimators | same | acceptable median at k = 2 to 3, but occasional large overestimates; Mth-Chao undefined at k = 2; Mh-Chao fails without a defect found by exactly two | — | human-only evidence |
| Calibration from historical error | Briand et al. | "does not work" | — | human-only evidence |
| Process with decision points from estimates (A: after preparation; B: after meeting) | Petersson et al., A | one industrial trial reported | estimates are input, "not solely" decisive | human-only evidence |
| CR over LLM judges | Kansal 2026, C (not peer-reviewed; label errors, not software) | calibrated (97% coverage on planted errors) but the real-data interval was 102 to 797 against 181 | 3 current models plus one non-LLM method | yes: "not precise enough to be useful" |
| **Own trial**: Chapman over OP-01's two unprimed readers | own trial, `own_trial_op01_capture.py` | readers found 13 and 12, 11 shared, so N̂ = 14.2 and about 0.2 remain. The primed review then found 4 more (O41 to O44). RFC-0028's two runs: N̂ = 4 against at least 6 known | k = 2, one model family, one brief | yes |

**Disconfirming search (c): confirmed.** With two to four inspectors,
capture-recapture is unreliable and biased low. Miller 1998, not read, is
the only dissent (some models acceptable at 3).

What breaks for LLM readers (*Inference*, supported by the own trial):

- Same-model readers given one brief are positively dependent, which
  inflates the overlap and biases N̂ down.
- Class 3 and class 4 defects have detection probability near zero for an
  unprimed reader, so no overlap among such readers estimates them.
- k = 2 is the worst case in the measured literature.
- Matching LLM findings as "the same defect" is a judged step.
- A record edited between rounds breaks closure.

### T5. Diversity (minimal)

- Human perspectives: PBR teams (Designer, Tester, User) covered more of the
  union than three usual readers. Team detection 79.3 vs 48.2% and 85.3 vs
  62.4% in 1995 (p 0.0007 and 0.039); the pilot was not significant (Basili
  et al. 1996, A, the authors' own technique). The effect comes from defects
  only one perspective found.
- Models: four passes of one model added about a third more finds over one
  pass. Four different models beat four passes of the best model slightly
  (68 vs 65 CVEs) and at lower cost (HoF-Bench, A-pre, code, own scaffold).
- No study covers document or requirements review with LLM ensembles.
- For the record (*Inference*):
  - Assign readers **different kinds**: defect class, perspective or
    ground. Use more than one model within a kind.
  - Estimate **within** a kind, never across kinds.

### Disconfirming search (d): a published process exists, with no yield data

- **SEURAT** (Burge 2005, A) checks recorded design rationale for
  completeness and consistency by inference over a structured
  representation.
  - Syntactic checks: no reason for selection, selection contradicted, no
    selected alternative, too many selected, missing sub-decisions, and an
    unanswered question flagged "as soon as the question is created".
  - Semantic checks: the same argument for and against, a presupposed
    alternative not selected, a selected alternative opposed by another
    selected one, a violated requirement.
  - Knowledge-base check: "Tradeoff Missing".
  - Checks re-run on every modification.
  - Its evaluation (20 subjects, 10 vs 10) measured maintenance time, not
    defects found, and subjects ignored the warnings.
- **Comparison with the project's step:**
  - SEURAT's checks need the structure the record lacks. Each maps onto a
    record element: an unsourced Recommendation; a Decision whose own
    option reads against it; open items; consistency against the ground.
  - Its key difference is **when** checks run: on every edit, not once by
    the author (class 1) or once at the End.
  - It has no fidelity check (class 2) and no implementation check
    (class 3).
  - Its "Tradeoff Missing" is a class 4 device, limited to a declared
    knowledge base.
- **Petersson et al.'s** inspection process is the published stopping
  process (§ 4).
- No other surviving source checks decision records before specification:
  - Ahmeti et al. (ECSA 2024, abstract only) has no review step.
  - The Rationale Capture Cycle is **[unreachable]**.
  - GADR and Quasar (arXiv 2601.19693; criteria-based LLM scoring, deviation
    27% and 43% against two architects) check presence or quality, not
    consistency.

## 3. Check map

Columns: **C** completeness, **K** consistency, **F** fidelity. **M** means
mechanical (a script, given a declared grid or an extraction) and **J**
means judged (a reader or agent). **In** means it can run during the design
session, with the maintainer present; **After** means only after it.
"Extraction" is the typed claim register of T2, built twice by different
agents and diffed (the only validation available, see § 5).

| Element | Check | Kind | When |
|---|---|---|---|
| **Environment** | C: slot grid of rows × steps s1 to s4, each cell an exposure or "none" with a reason (Leveson) | M | In |
| | C: STPA guide-words over O1, O2, O3, world and runtime generate candidate rows; each candidate is kept, rejected with a reason, or deferred (obstacle test) | J | In (generation); After (primed, for backend actions such as O43 and O44) |
| | K: every Environment ID a decision names exists; every row is cited by AX-7 or marked not exposed | M | In |
| | F: each row "decided in the first dialog" or "added by D*n*" pairs with that dialog | M | In |
| **Decision** (as a unit) | C: every axis question is answered by a decision or an open item (Axis status) | M | In |
| | K: the whole-record pass. Run on **every amendment**, not once (SEURAT), over the extraction: Closed × Member, Rule × outcome, Adopts × later claims; plus every **general clause** (D1 parity, D10 frame, D27 and D33 principles) against every decision | M over extraction; J for extraction and for verdicts | In |
| | K: two readers of **different defect classes** (contradiction or extent; reason against outcome), one model each | J | After |
| **Decision text vs Asked lines** | F: Asked lines pair (in place) | M | In |
| | F: claim-to-span alignment. Every atomic claim needs a span in the answer or the chosen option; unspanned claims are candidates | M once claims are split; J to split and to rule | In (the maintainer answers each candidate at once) |
| **Adopted option** (by label) | F: the option's full text is printed beside the Decision (in place since RFC-0028 run 2) and enters the extraction as `Adopts` | M | In |
| | K: Adopts × every later Rule or Closed claim (C2 and O29 were of this kind; no reader run found C2) | M over extraction | In |
| | F: dialog-to-record diff of option text where the log copies it verbatim (O40) | M | In |
| **Outcome partition (AX-3)** | C, K: the settled table check over a **declared** pre-state domain. The table states its domain as a header row naming the enumeration it partitions | M | In |
| **State × operation (AX-6)** | C: every (state, method) cell filled. Methods are taken from the handed-out object's declared method list (AX-1), so `read1`, `tell` and `readable` cannot be skipped (O25) | M | In |
| | K: each cell's failure category against AX-10; each transition's trigger against AX-11 phases (O36) | M over extraction | In |
| **Failure category (AX-10)** | C: rows = Environment rows × phases, plus caller errors and cancellation; empty rows are findings (O14, O37, O39) | M | In |
| | K: per cause, one category across backends, or a variation point (O22) | J | After (primed) |
| **Failure phase (AX-11)** | C: each failure from AX-10 has a phase row; every list "surfaces from the open" or "from a read" is a `Closed` claim | M | In |
| **Retry (AX-13)** | C: one column per AX-10 row; a missing row is a finding (O37) | M | In |
| **Non-promise register (AX-14)** | K: no row contradicts an adopted option or a Decision (O29); every behaviour a decision leaves to a backend is registered or made a variation point (O31) | M over extraction | In |
| | C: caller-use reading. Each familiar idiom a caller would infer (a line read, a timeout as cancellation) is a row or a decision | J | In |
| **Variation points (AX-15)** | C: every claim whose truth differs by backend has a row; a count ("four variation points") is a `Closed` claim | M over extraction | In |
| | K, F against backends: does a backend, SDK or runtime make a claim false, two-valued or costly? | J (primed) | After |
| **Axis status** | C: each row's decisions and open items match the decisions' axis tags and the items' dependents | M | In |
| **Open items** | C: each item names the decisions it blocks, and those decisions' axis rows list it | M | In |
| | K: summaries of decisions in items (O11 against D38's list, O38) are `Closed` claims checked against the decision | M over extraction | In |
| **Consistency-check lines** | K: replaced as evidence by the whole-record pass; kept as the author's note only. 4 of 27 known defect pairs were named in them, and none was caught (own trial) | — | — |

The pattern: everything that compares two places in the record can run
**in** the session, because the extraction and the grids are mechanical.
What needs the outside world (backends, SDKs, runtimes) or a fresh reader
of another kind runs **after**.

## 4. Stopping rule

*Inference*, built from Briand et al., Petersson et al. and the own trials.
It has not been validated.

**A record is ready for its spec when all of the following hold:**

1. **Mechanical gates are clean.**
   - Every slot of every grid in § 3 is filled.
   - Each table passes the domain check.
   - The two extractions' diff is resolved.
   - Every Closed × Member, Rule × outcome and Adopts × later conflict is
     decided or an open item.
   - Every Decision claim has a source span or a decided reopen.
   - These are counts, so "done" here means zero, not "nothing found".
2. **Per reviewer kind, a seeded-defect check passes.** The kinds are
   consistency reader, fidelity reader, caller-use reader and primed
   backend reviewer.
   - Before the review, a script plants *s* defects of the kind's class in a
     copy of the record. Examples: add a member to a closed list in a later
     decision; reword an adopted option; add an unasked claim to a Decision.
   - Each kind's readers (at least two models) review the seeded copy.
   - Let *p* be the share of seeds found and *n* the number of real
     findings that survive a re-read. The estimate of real defects left for
     that kind is n(1 − p)/p, if seeds are as hard as real defects.
   - Proceed when, for each kind, p ≥ 0.8 and the estimate is below one
     defect of blocking severity.
   - If p is below the bar, the kind's readers or brief change before the
     estimate counts.
3. **A new kind finds no blocking defect.** The last round uses a reviewer
   kind not used before on this record: another model family, another
   perspective, or another ground. It may yield notes, not reopens.
4. **Capture-recapture only as a cross-check, and only within a kind with at
   least 4 captures.** An Mh-JK estimate is admissible with four or more
   independent readers of one kind. Below that, the measured error is −27%
   to −52%, so it must not be used.

**Assumptions.**

- Seeded defects are as hard to find as real ones of the same class.
  Seeding literature was not read in this run, so this is unverified.
- Readers of one kind are exchangeable within the kind.
- The record does not change between a kind's captures.
- Matching findings to seeds is unambiguous. Seeds are planted at known
  lines.
- The four kinds cover the defect classes that matter. Class 4 is covered
  only by the caller-use reader.

**What would invalidate it.**

- Spec writing or modelling finds a record defect of a class that passed
  its kind's gate. That shows the seeds were easier than real defects, or
  that a class is missing.
- The axis-escape rate (T1) does not fall across OP-02, OP-03 and later
  records. Then class 4 has no reliable gate.
- Two extractions agree but a reader still finds a contradiction in what
  both extracted the same way. That is a shared misreading, the settled
  limit of dual formalization.
- A model or brief change moves a kind's seed recall p by more than its
  run-to-run spread. Then the kind must be recalibrated.

**Cost.** Mechanical gates are cheap after a one-time extraction schema.
Seeding needs a seeding script per class and one extra review run per kind.
Rule 4 needs four readers per kind, so it is optional.

## 5. Open questions and verification debt

1. **Extraction error is unmeasured everywhere.** No source measured what
   LLM extraction into logic or tables introduces or hides. The proposal
   rests on dual extraction, whose limit is shared misreadings (settled).
   Debt: run two extractions of OP-01 and measure their diff against
   O14 to O44.
2. **The typed claim register is untested.** Only its lexical precursor
   ran: 4 of 7 known extent defects. Debt: implement `Closed`, `Rule`,
   `Adopts` and `Member` extraction on OP-01 at `c58ee74` (audit-025's
   commit, before the O17 to O44 items were found) and score it against
   O17 to O44.
3. **Seeded-defect calibration for LLM readers is unverified.** Mills-style
   seeding was not read in this run, and seeds may be easier than real
   defects. Debt: plant seeds in OP-01 and measure each reader kind's seed
   recall against its recall of the known items.
4. **Fidelity judges on design dialogs.** Every measured number is on
   chit-chat, interviews or council meetings. None is on design dialogs
   whose answers are short and whose decisions are their main topic.
5. **Class 4 discovery is unmeasured.** No technique for finding
   questions no checklist raises has a surviving measurement. Caller-use
   reading and STPA guide-words are proposals.
6. **O27 to O44 have not been classified by axis escape.** Without that,
   RFC-0028 P4's effect on the axes is unknown.
7. **2023-24 models.** All LLM conflict and fidelity figures predate
   current models. They may understate current judges, or overstate them on
   design text.
8. **Unread or unreachable:** Eick et al. 1992 **[unreachable]**; Heimdahl &
   Leveson 1996 RSML **[unreachable]** in full text; Miller 1998 (some CR
   models acceptable at 3 inspectors) not read; the failed replications of
   scenario reading (Fusaro 1997, Miller 1998, Sandahl 1998) are leads only;
   DPM curve fitting is a lead only.
9. **The own-trial vocabulary lists were written after reading the open
   items.** That leaks the known set into check B and favours it. The known
   set (O14 to O44) is itself incomplete. The RFC-0028 runs raised
   candidates outside it that remain unverified, and this run's own trials
   produced no new candidate findings.

## 6. Sources

| Source | Grade | Used for | Notes |
|---|---|---|---|
| Leveson, Completeness in formal specification language design for process-control systems, FMSP 2000 | A | T1 | human-only evidence |
| van Lamsweerde & Letier, Handling obstacles in goal-oriented requirements engineering, TSE 2000; retrospective (UCL Discovery) | A | T1 | validation and completeness claims refuted 0-3 |
| Abdulkhaleq & Wagner, controlled experiment STPA vs FMEA vs FTA, arXiv 1612.00330 | A-pre | T1 | 3 student groups; coverage figures inconsistent |
| MIT S.M. thesis, STPA vs FMEA on TomoTherapy, DSpace 1721.1/113531 | B/C | T1 | single analyst; not voted |
| Heimdahl & Leveson, Completeness and consistency in hierarchical state-based requirements, TSE 1996 | — | T1 | **[unreachable]** |
| Porter, Votta & Basili, Comparing detection methods for software requirements inspections, TSE 21(6) 1995 | A | T2 | human-only evidence |
| Fabbri et al., PBR replications, ICMC-USP TR-225 | B/C | T2 | unrefereed |
| Fazelnia, Koscinski, Herzog, Mirakhorli, Lessons from the use of NLI in RE tasks, RE 2024, arXiv 2405.05135 | A-pre | T2 | datasets built by the authors |
| Gärtner & Göhlich, ALICE, Automated Software Engineering 31:49, 2024 | A | T2 | authors' own tool |
| Fazelnia, Mirakhorli, Bagheri, SAT-LLM, NSF PAR 10574434 | A-workshop | T2 | authors' own tool; n = 15 sets |
| Burge, SEURAT, WPI PhD dissertation 2005 | A | T2, (d) | author's own tool; no yield measured |
| Ramprasad, Ferracane, Lipton, Analyzing LLM behavior in dialogue summarization, ACL 2024, arXiv 2406.03487 | A | T3 | detector is the authors' own |
| Tang et al., TofuEval, NAACL 2024 | A | T3 | sentence range corrected to 14.4 to 27.8% |
| Costa da Silva & Gama, GADR, arXiv 2608.17694 (SBES 2026 header) | A-pre | T3, (d) | authors' own tool |
| Elberzhager, Gerbershagen, Ginkel, LLM evaluation of architecture documents (Quasar), arXiv 2601.19693 | A-pre | (d) | authors' own tool |
| Briand, El Emam, Freimut, Laitenberger, A comprehensive evaluation of capture-recapture models, TSE 26(6) 2000 (read as NRC ERB-1084) | A | T4 | human-only evidence |
| Briand, El Emam, Freimut, Laitenberger, ISERN-97-22 | A-workshop | T4 | earlier version |
| Petersson, Thelin, Runeson, Wohlin, Capture-recapture in software inspections after 10 years research, JSS 72, 2004 | A | T4 | |
| Eick, Loader, Long, Votta, Vander Wiel, ICSE 1992 | — | T4 | **[unreachable]** |
| Kansal, How many label errors are left?, 2026 (GitHub/Zenodo) | C | T4 | not peer-reviewed; not software |
| Calboreanu, Context engineering, arXiv 2604.04258 | C/D | T4 | interpretive use only |
| Basili et al., The empirical investigation of perspective-based reading, EMSE 1(2) 1996 | A | T5 | authors' own technique |
| Simecek et al., HoF-Bench, arXiv 2607.27030 | A-pre | T5 | authors' own scaffold |
| Kumar, Bararia, Raj, arXiv 2606.15689 | A-pre | T5 | internally inconsistent; not used |
| Ahmeti, Linder, Groner, Wohlrab, ADRs in practice, ECSA 2024 | — | (d) | abstract only, **[unreachable]** as full text |
| Rationale Capture Cycle (Utrecht repository) | — | (d) | **[unreachable]** |
| Dalhousie CSCI 3130 design-review rubric, 2011 | D | (d) | course assignment |
| haalfi/remote-store at `eb08d990e`: OP-01 record, axes, audit-025, RFC-0028 | test material | all | own trials; open items O14 to O44 as the known set |
| Own trials: `own_trial_op01.py`, `own_trial_op01_capture.py` | own trial | T2, T4 | scripts committed in the notes folder |
