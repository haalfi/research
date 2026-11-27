# Durable text validity

Brief: [briefs/Durable text validity.md](../briefs/Durable%20text%20validity.md).
Notes: [research_notes/Durable text validity/](../research_notes/Durable%20text%20validity/).
Research date: 2026-11-27. Branch: `research/durable-text-validity`.

The report tests problem statement v0.4 against published evidence. It does not design a remedy.
Claim labels C1–C8 are the statement's bold claims, in order (see § A).

## Evidence labels

| Label | Meaning |
|---|---|
| **V** | Checked by the workflow's 3-vote adversarial verification against the source text (notes 01). **V(abs)** means the voters matched the figures against an abstract only. |
| **F** | Full text read in a single pass by one research track (notes 03–08). Not adversarially verified. **F(fetch)** means the text was read through a fetch tool that returns extracted quotes, not grepped. |
| **A** | Abstract, record, or secondary report only. A lead, not a verdict. |
| **E** | Finding of an earlier run (`research/explicit-engineering-contracts`, or a baseline record named in the brief), cited with that run's label. |
| **I** | Inference by this report. Not measured anywhere. |

Each source also has a type: **study** (first-hand empirical), **standard** (regulation, guideline, method definition), **practitioner** (report, case record, database), or **review** (secondary synthesis).
Where a figure appears, it was found in the text read. Ranges are as the sources state them.

## Bottom line

- **Loss of validity without a signal is the best-established claim.** It is measured in clinical guidelines and reviews, case law, statutes, architecture documents, code comments and decision-support rules. In each case the change happened in a different text or system, and nothing appeared in the dependent text. Typically the dependent text learns of it years later, by chance, or never.
- **"No check that can fail" is too strong as written.** Checks that can fail exist in several fields:
  - EU leaflet user testing with a per-question pass rule;
  - nuclear procedure walk-throughs and simulator validation with pre-stated pass/fail criteria;
  - assurance-case defeaters with an open/closed status;
  - legal citators;
  - living-review "last searched" stamps;
  - nightly architecture conformance checks.

  The defensible claim is narrower: no such check has measured reliability on the content of a text, and at its core each rests on a human reading.
- **The failure kind the statement misses is false assurance.** A signal says "valid" when the text is not. Examples:
  - a citator green flag;
  - a signed-off safety case with 40% of hazards still open;
  - a "Changes to legislation" box still inside its update lag;
  - a retrieval tool that drops a red-flagged citation but keeps the statement.

  The signal that a text is valid is itself durable text, and it decays.
- **Propagation is well evidenced.**
  - In science, a claim spreads through citation (Greenberg 2009).
  - Retraction notices reach almost no citing text: 5.4% of post-retraction citations acknowledge the retraction.
  - Retracted trials reached 157 guideline documents.
  - In software, generated tests lock in seeded faults, and insecure snippets keep spreading despite written warnings.

  "Internal consistency grows while correctness falls" is shown in four separate settings. No study measures consistency and correctness on the same corpus over time.
- **Agents reproduce each failure on benchmarks.** They:
  - resolve contradictions silently;
  - prefer a text by its position and frequency, not its validity;
  - rarely say information is missing;
  - follow stale context;
  - state reasons that were not what decided;
  - verify well only where an external authority (a search result, an execution) can settle the claim.

  No in-the-wild study measures invented rationale later read as recorded intent.
- **The strongest evidence against the statement is about cost, not existence.**
  - Most dependent texts stay valid after most dependency changes: 4–9% of updated Cochrane reviews changed conclusions, and 96% of recalculated meta-analyses stayed within the original confidence interval.
  - Out-of-date documentation is still judged useful.
  - The minority that flips cannot be identified in advance.
- **Two baseline claims need narrowing, not withdrawal.**
  - "Review has no stopping rule" is contradicted by new full-text evidence in two fields that state criteria, and by capture-recapture estimation in software inspection. Each criterion covers only the questions or scenarios chosen, or the defects reviewers can see.
  - "What a text must say depends on its reader" found no new challenge.
- **Written countermeasures work partially and are not self-applying.**
  - Inline deprecation comments, precedence sentences and abort options measurably shift agent behaviour.
  - Writer's guides, checklists and comment warnings were demonstrably present and not applied.
  - So C8 holds as stated, but it does not license "text instructions don't work".

---

## A. Verdicts on the bold claims

| # | Claim (short) | Verdict | Strongest for | Strongest against |
|---|---|---|---|---|
| C1 | What a text says is held to no check that can fail | **Contested** as categorical; **established** as "no check of measured reliability, and a reading at the core" | Hellyer 2018 citator misses [F]; Nimrod Review 2009 [F]; Diemert et al. 2024 review dominant [V] | EC readability guideline 2009 16/20 rule [F]; NUREG-0711 pass/fail validation [F]; Feilkas et al. 2009 conformance check [V]; Assurance 2.0 defeaters [V] |
| C2 | Three failure kinds, none needs to show | **Established** for each kind; **incomplete** (misses false assurance, divergent copies, non-application) | Shojania 2007 [V(abs)]; Martínez García 2014 [V]; Christiansen & Eskridge 2014 [F]; Wright et al. 2016 [F]; Aghajani et al. 2019 [F] | Cost evidence: French 2005, Bashir 2018, Graña 2025 [F]; Lethbridge et al. 2003 [F] |
| C3 | What a text must say depends on its reader | **Established** (baseline holds; no new full-text challenge) | Baseline verified rows 1–3, 12 [E]; Knapp et al. 2011: ethics-approved sheets failed readers [F] | None found in full text |
| C4 | Review has no stopping rule | **Contested** by new full-text evidence; true for most fields, false where a criterion is stated | Degani & Wiener 1990: no checklist design criteria [F]; 21 CFR 820.40 "adequacy" with no criterion [F]; baseline § 6.3 [E] | EC 2009 per-question 16/20 [F]; Knapp et al. 2011 RCT [F]; Briand et al. 2000 capture-recapture [F]; NUREG-0711 Rev. 3 [F] |
| C5 | Costly defects are mostly beneath the wording; finding ≠ resolving; owner bottleneck; recovered ≠ reconstructed | **Mixed.** "Mostly" is **unstudied** as a cost ranking. Finding ≠ resolving is **established**. Owner bottleneck is **inference with indirect support**. Recovered vs reconstructed is **established and stronger than stated** | Nimrod open hazards [F]; SATD clarification TODOs deleted unanswered [F]; RecovAr no ground truth [V]; Chen et al. 2025 unfaithful CoT [F] | NaPiRE ranks incomplete/hidden requirements first, but by mention frequency, not cost [E] |
| C6 | Agents make plausible text cheap and act on it without a trace | **Established on benchmarks; unstudied in the wild** for the downstream "read as intent" step | WikiContradict, Xie et al. 2024, ConflictBank [F]; QuestBench [F]; Wang et al. 2025 deprecated APIs [F]; Magesh et al. 2024 [F] | GPT-4 detects ~88% of explicit contradictions when asked [F]; precedence sentence and abort option shift behaviour [E] |
| C7 | A defect propagates as knowledge; consistency grows while correctness falls | **Established** in science, law and software; "readers cannot tell inference from decision" **unstudied** directly | Greenberg 2009 [F]; Xu et al. 2025 VITALITY [F]; Charoosaei et al. 2026 [F]; Zhao et al. 2026 [F]; Broughman & Widiss 2017 [F] | Gerstgrasser et al. 2024 retaining originals prevents collapse [F]; Kumar et al. 2016 hoax patrol [F]; Bakker 2024 / Graña 2025 robustness [F] |
| C8 | An instruction cannot enforce itself | **Established** as stated; contested if read as "written countermeasures are ineffective" | NRC IN 92-76 writer's guide not implemented [F]; Fischer et al. 2017 warned snippets copied more [F]; FDA FY2024 211.22(d) rank 1 [F]; Nimrod BP1201 [F] | Wang et al. 2025 inline deprecation comment fixes 25.7–97.2% [F]; Xu & Wu precedence sentence → 91.4% [E]; ImpossibleBench abort option 54% → 9% [E] |

### C1 — "What a text says is generally held to no check that can fail"

- **For.**
  - **Citators: Hellyer 2018** (*Law Library Journal* 110:449) [F, study]. Citators are the most mature validity signal on durable text anywhere. Of 309 clearly negative citing relationships, Shepard's failed to identify 33%, KeyCite 38% and BCite 72% (Table 1). All three agreed on negative treatment in only 53 of 357 relationships (¶48). Shepard's mislabelled 3 of 4 U.S. Supreme Court overrulings (¶58). No citator marks a label as uncertain.
  - **Sign-off: The Nimrod Review** (Haddon-Cave 2009, HC 1025, ch. 10A paras 7–12) [F, practitioner/inquiry]. A reviewed and signed-off safety case was "virtually worthless". "Over 40%" of hazards were still "Open", including the one behind the loss, and signatories approved "without ... even carefully reading the final Reports".
  - **Review in practice: Diemert, Shortt & Weber 2024** (arXiv 2411.03657) [V, study, n=19 interviews]. All 19 practitioners relied on review. Only 2 had used a quantitative confidence method on a real system. One relied on review "probably more ... than I'm comfortable with".
  - **Configuration change: Wright et al. 2016** (JAMIA 23:1068) [F, study]. An alert stopped firing when a drug code changed from 40 to 7099. It was found by chance four years later, after about 9,774 missed firings. None of 29 informatics leads was fully confident their processes would catch such failures.
- **Against.** Checks that can fail on what a text says exist:
  - **EU leaflets:** the user-testing rule: 90% of readers find each key fact and 90% of those understand it, "16 out of 20 participants", per question, with "Results cannot be aggregated" [F, standard; EC readability guideline Rev. 1, 2009, Annex § 5].
  - **Nuclear procedures:** emergency procedures are checked by control-room walk-throughs for match to hardware (NUREG-0899, 1982). Validation uses pass/fail criteria stated in advance (NUREG-0711 Rev. 3, 2012) [F, standard].
  - **Assurance cases:** Assurance 2.0 keeps a case "open" while a defeater is active, and the tool propagates that status to the top claim (Bloomfield, Netkachova & Rushby 2024, arXiv 2405.15800, p. 26) [V, standard/method].
  - **Architecture documents:** an architecture description turned into a machine-checkable specification stayed in sync with nightly checks for about a year (Feilkas, Ratiu & Juergens, ICPC 2009) [V, study].
- **The second sentence survives everywhere.** The step from sentence to check is itself a reading:
  - Hellyer's ground truth is his own reading, and the vendors dispute it [F].
  - Whether a subcase refutes a defeater "rests on human reading of narrative justifications" [V].
  - DOORS-type suspect links: "A person must verify" (IBM ELM documentation) [F, practitioner].
  - The Cochrane update consensus: "Mechanical rules appear unworkable" (Garner et al. 2016, BMJ 354:i3507) [F].
  - The leaflet test checks findability and comprehension of facts the applicant chose, not whether they are correct [F].
- **Verdict.** Contested in the categorical reading; established in the reading below.
- **Rewording:** "What a text says is generally held to no check whose reliability has been measured. Where checks exist, they cover only the claims, questions or dependencies someone chose to record. The decisive step in each is a human reading, and sign-off can pass without it."

### C2 — "A text goes wrong in at least three ways, and none needs to show"

- **Misrepresentation, established.**
  - Quotation errors in citations run at 25.4% (Jergas & Baethge 2015, PeerJ) and 14.5% (Mogull 2017) [F, review].
  - A hypothesis became "fact" through citation alone (Greenberg 2009, BMJ 339:b2680) [F, study].
  - Two reviewers of real safety cases found 29 and 14 fallacies in two of them, and their findings diverged (Greenwell et al. 2006, ISSC) [F, study].
- **Loss of validity without signal, established in six fields.**

  | Field | Finding | Source | Label |
  |---|---|---|---|
  | Systematic reviews | 57% acquired an updating signal, median 5.5 years; 7% already had one at publication | Shojania et al. 2007, Ann Intern Med 147:224 | V(abs), study |
  | Clinical guidelines | 81.3% of recommendations still valid at 3 years, 77.8% at 4 | Martínez García et al. 2014, CMAJ, PMC4216254 | V, study |
  | Statutes | Congressional overrides are flagged in Westlaw on average just under 6 years after enactment; roughly 10% to a third never; about half of "superseded by statute" leads are not overrides | Christiansen & Eskridge 2014, Texas L. Rev. 92:1317, p. 1328, 1343 | F, study |
  | Case law | After an override, citations continue at 89% of prior levels; after a judicial overruling they fall to 58% | Broughman & Widiss 2017, J. Legal Stud. 46, p. 60 | F, study |
  | Architecture docs | 9–19% of dependencies undocumented; 72–90% of mismatches were documentation flaws | Feilkas et al. 2009 | V, study |
  | Software docs | "Up-to-dateness" accounts for 39% (190 of 878) of documentation-content issues | Aghajani et al., ICSE 2019 | F, study |
  | Code comments | 869 stale function references in comments, caused by changes elsewhere; 50 of 75 fix patches accepted | Sun et al., ASE 2026, arXiv 2608.03734 | F, study |
  | Decision support | The drug-code change above | Wright et al. 2016 | F, study |

  Invalid statutes stay printed and occasionally enforced (Wasserman 2021, "Zombie Laws", Lewis & Clark L. Rev. 25:1047; Johnson 2022, Geo. L.J. 111:95) [F, review/practitioner].
- **Misreading, established.**
  - With the full overruling opinion in context, the best models named the overruled case 73% (Gemini-Pro) and 71% (GPT-5) of the time (Zhang, Savelka & Ashley, JURIX 2025, arXiv 2510.20941) [F, study].
  - Before user testing, 15% of readers of an ethics-approved trial information sheet showed full understanding, against 66% after revision (Knapp et al. 2011, BMC Med 9:89) [F, study].
- **Against (cost, not existence).**
  - Only 9% (French et al. 2005, BMC Med Res Methodol 5:33) and 4% (Bashir et al. 2018, Syst Rev 7:195) of updated Cochrane reviews changed conclusions [F].
  - 80% of class I cardiology recommendations were retained, under 1% reversed (Neuman et al. 2014, JAMA 311:2092) [F].
  - 96% of recalculated meta-analyses stayed within the original CI after removing retracted studies (Graña Possamai et al. 2025, JAMA Intern Med) [F(fetch)].
  - Out-of-date documentation is still judged useful (Lethbridge, Singer & Forward 2003, IEEE Software) [F].
  - But the minority that flips cannot be predicted: in French et al., predictors are "only known after the update" [F], and in Shojania, no review feature predicted a signal within 2 years [V].
- **Failure kinds the statement misses.**
  - **False assurance:** a validity signal that is wrong or stale. Examples are citator mislabels, sign-off without reading, LSRs that stop updating without a retirement notice (Akl et al. 2023 [A]), suspect links auto-cleared on approval [F], and a retrieval tool that keeps an overruled proposition but drops its citation (Magesh et al. 2024, arXiv 2405.20362) [F].
  - **Divergent copies:**
    - Generic drug labels diverged from the brand label for 68% of multi-manufacturer drugs (Duke et al. 2013 [A]).
    - Only 5% of web copies of retracted papers carry a retraction statement (Davis 2012, JMLA 100:184) [F].
    - EU consolidated texts disclaim legal effect (unreachable).
  - **Non-application:** a correct, current text that is not consulted or followed. Courts and businesses often ignore the written contract (Macaulay 1963, Am. Sociol. Rev. 28:55) [F]. "Procedures not in writing, fully followed" is the most cited FDA drug observation in FY2024 [F]. The statement treats this only under C8.
  - **Invalid at writing:** 7% of reviews had a signal at publication because of publication lag (Shojania [V(abs)]). The text loses validity before anyone reads it.
- **Verdict.** Established; the list of kinds is incomplete.
- **Rewording:** add false assurance as a fourth kind, and say that copies of one text can diverge with no signal in either.

### C3 — "What a text must say depends on its reader" (baseline)

- **Baseline.** The verified findings of `research-appropriate-level-of-detail.md` stand: Grice and Nickerson verified; curse of knowledge verified; Kalyuga et al. 1998; Charney, Reder & Wells 1988; Rozenblit & Keil [E].
- **No new full-text evidence challenges the claim.**
- **New supporting evidence.** Knapp et al. 2011 [F]: research ethics committees approved information sheets that then failed reader testing. That is the writer- or reviewer-side knowledge concealing a gap, as the claim's last sentence says.
- **Leads, abstract only.** De Jong & Lentz 1996 (J Tech Writ Commun 26:507): 15 technical writers predicted little of 30 readers' feedback. De Jong & Schellens 2000 (IEEE TPC 43:242) [A].
- **Verdict.** Established. No rewording needed.

### C4 — "Review has no stopping rule" (baseline; challenged with new full-text evidence)

This challenges a baseline claim, as the brief allows, and rests only on full texts read in this run.

- **Against.**
  - **EU leaflet test:** the rule applies per question, 16 of 20 participants, and results cannot be aggregated (EC 2009 guideline, Annex § 5) [F, standard].
  - **The leaflet test works as a stopping rule in a trial.** Knapp et al. 2011 [F, RCT]: revision against the 16/20 rule converged, and comprehension held in an independent sample. Full understanding was 66% for the revised sheet against 15% for the original (OR 11.2). The authors declare a commercial interest in user testing.
  - **Nuclear procedures:** NUREG-0711 Rev. 3 requires pass/fail criteria stated in advance with their basis, and re-validation when a change substantially alters safety tasks [F, standard].
  - **Software inspection:** capture-recapture estimates the defects remaining in inspected natural-language requirements documents, to decide between stopping and reinspecting (Briand et al. 2000, IEEE TSE 26(6), read as the Fraunhofer IESE report) [F, study]. It usually underestimates and needs 3–4 independent inspectors. The report warns that fixed defect-count thresholds tempt inspectors "to only find a passing number of defects". The numeric results could not be recovered from the encoded PDF.
  - **Usability testing:** sample-size rules exist, but 5 users found as little as 55% of the problems all 60 users found (Faulkner 2003, BRMIC 35:379; a web application, not a document) [F, study].
- **For.**
  - **Checklists:** there were "no FAA internal guidelines for checklist design criteria", so an inspector approved checklists by "his or her own philosophy" (Degani & Wiener 1990, NASA CR-177549) [F, practitioner].
  - **Medical devices:** 21 CFR 820.40 required review "for adequacy" with no stated criterion [F, standard].
  - **Local:** the baseline measured local prose review diverging over seventeen commits [E].
  - **Assurance cases:** a workflow claim that practitioners name a missing stopping rule for defeater methods was **refuted 1–2** (notes 02, R4). This run therefore found no verified external support for C4 from assurance cases.
- **Gaps in every stopping rule found.** Last-minute changes required by the authorising body are not user-tested, and only one language is tested (EC PIL-S study 2014) [F]. Validation covers a sample of scenarios. Capture-recapture counts only defects that some inspector can see.
- **Verdict.** Contested.
- **Rewording:** "Most fields state no acceptance criterion for a text, so review has no stopping rule. Where a criterion or stopping rule exists (leaflet user testing, procedure validation, defect-content estimation), it covers only the questions, scenarios or defects the reviewers chose or could detect, and a later edit can escape it."

### C5 — "The costly defects are mostly misrepresentations beneath the wording"

- **"Mostly" (cost ranking): unstudied.**
  - The best frequency evidence is NaPiRE (incomplete or hidden requirements ranked first) [E, V in the earlier run]. It measures how often a problem was named, not its cost.
  - Aghajani's taxonomy counts issue types, not cost [F].
  - No source ranked defect kinds in durable text by consequence.
- **Defects beneath clear wording, supported.**
  - The Nimrod guidance text told authors to "make the basic assumption that the aircraft is already operating to acceptable levels of safety" (para 9.58) [F]. That is an unchecked premise written clearly into an instruction.
  - Hypothesis turned into fact through clear citing sentences (Greenberg) [F].
- **Finding ≠ resolving, established.**
  - Hazards were marked "Open" and stayed open (Nimrod) [F].
  - 33 of 43 "clarification request" TODOs (77%) were "resolved" by deleting the comment (Maipradit et al. 2020, EMSE, arXiv 1901.09511) [F, study].
  - 20–50% of self-admitted debt comments disappear by accident; 8% of removals are mentioned in commit messages (Zampetti, Serebrenik & Di Penta, MSR 2018) [F, study].
  - Marking an open point does not route it to an owner.
- **Owner's attention as the bottleneck: inference with indirect support.**
  - Only 7.6% of 344 eligible UK Acts (2005–2017) got post-legislative scrutiny (Caygill, via the Hansard Society) [A].
  - Overdue statutory post-implementation reviews stalled at 47 (Regulatory Policy Committee, May 2026) [F, practitioner].
  - NICE surveillance runs "subject to constraints on capacity" [F, standard].
  - None of these measures a decision owner's attention directly.
- **Recovered vs reconstructed reason: established, and stronger than the claim.**
  - RecovAr's recovered decisions were judged by two PhD students without the original architects, because "a ground-truth ... was not readily available" (Shahbazian et al., ICSA 2018) [V, study].
  - LLM-generated design rationale reached precision 0.267–0.278 against expert answers (Zhou et al. 2025, arXiv 2504.20781) [F].
  - The Argus pipeline generated rationale components absent from the record; Constraints were recorded in 0 of 63 commits (Sun et al. 2026, arXiv 2604.10345) [F].
  - A record made at the time is not enough when a model writes it. Reasoning models revealed a hint they used often in under 20% of cases, and reward hacks were verbalised in under 2% of examples in 5 of 6 environments (Chen et al. 2025, arXiv 2505.05410) [F, study].
  - The norm can work for humans: 98.9% of 366 Linux OOM-killer commits carry rationale (Dhaouadi et al. 2024) [F]. No study checks that a recorded reason was the deciding one.
- **Verdict.** Mixed (see table).
- **Rewording:**
  - Drop or qualify "mostly". Say "the defects found to matter in the cases studied", or state the ranking as a hypothesis.
  - Extend the last sentence: "Even a record made at the time may not state what decided, when its writer is a model or is reconstructing."

### C6 — "Agents make plausible text cheap, and can act on it without a trace"

- **Cheap accumulation.** An estimated 4.36% of 2,909 new English Wikipedia articles were AI-generated (Brooks, Eggert & Peskoff 2024, arXiv 2410.08044) [F]. LLM-modified prose is widespread in papers (Liang et al. 2024) [F].
- **Acting on a plausible reading.**
  - On underspecified problems the models said "not sure" in 0.7–4.6% of cases, against a true underspecification rate of 41.8% (QuestBench, Li, Kim & Wang 2025, arXiv 2503.22674, § 5.4) [F].
  - Reasoning fine-tuning cut abstention by 24% on average (AbstentionBench, arXiv 2506.09038) [F].
  - Earlier run: agents rarely ask (HumanEvalComm, Ambig-SWE) [E, V].
- **Silent contradiction resolution.**
  - Models "rely on a single passage" (WikiContradict, NeurIPS 2024 D&B, arXiv 2406.13805) [F].
  - A lone document is adopted, but under conflict the model clings to its own memory (Xie et al., ICLR 2024, arXiv 2305.13300) [F].
  - Position decides more than date; adding dates to the question dropped the memorisation rate from 67.52% to 8.31% (ConflictBank, arXiv 2408.12076) [F].
- **Stale text found and followed.**
  - Prompts taken from outdated code produced deprecated API usage 70–90% of the time (Wang et al., ICSE 2025, arXiv 2406.09834) [F].
  - Earlier run: a stale instruction file was followed in 90.1% of choices [E].
- **Without a trace.** Westlaw's AI tool stated propositions from overruled cases while dropping the citation (Magesh et al.) [F].
- **Invented rationale.**
  - About 20% of generated commit messages contain hallucinations (Liu, Lin & Thongtanunam, arXiv 2508.08661; small fine-tuned models, not agents) [F].
  - Unfaithful explanations (Turpin et al., NeurIPS 2023: biased explanations cost up to 36% accuracy) [F].
  - **Gap:** no study measures plausible-but-unverifiable "why" text written by agents and later read as intent.
- **Against.**
  - When asked, GPT-4 detects about 88% of explicit contradictions [F]. But it confirmed only 44% of clean pairs as conflict-free and invented reasons in the rest (WikiContradict template 5.x, 48 instances, single annotator) [F]. GPT-3.5 under-flags (Wang et al., COLM 2024) [F].
  - Detection on request is uncalibrated in both directions, and it is not the default behaviour.
- **Verdict.** Established on benchmarks; the downstream "read as intent" step is unstudied in the wild.
- **Rewording:** none for the mechanism. Mark "later reads as recorded intent" as unmeasured.

### C7 — "A defect propagates as knowledge"

- **Science.**
  - In Greenberg's 242-paper network, supportive papers received 94% of the 214 citations to primary data. 95% of citation paths ran through four reviews. The same distortions appeared in NIH-funded grant proposals [F].
  - About 20% of citers read the original (Simkin & Roychowdhury 2003, from misprint propagation) [F].
- **Retraction.**
  - Only 5.4% of 13,252 post-retraction citations acknowledge the retraction (Hsiao & Schneider 2021, QSS 2:1144) [F(fetch)].
  - 83% of post-retraction citations are positive (Bar-Ilan & Halevi 2017) [F].
  - 1,330 retracted trials reached 847 systematic reviews and, through them, 157 guideline documents. Removing them changed direction or significance in 20.6% of meta-analyses (Xu et al. 2025, BMJ 389:e082068, VITALITY) [F].
  - Only 1 of 68 citing guidelines and reviews was reassessed (Avenell et al. 2019, BMJ Open) [F].
- **Software.**
  - **Fault-enforcing tests:** across 145 PRs in SciPy, Qiskit and pandas, 8–17% of LLM regression tests enforced a seeded fault. 83–92% of those were still enforced at the end of the history, and developer tests caught 14–30% (Charoosaei, Richter & Papadakis 2026, arXiv 2610.11835; seeded mutants, preprint) [F].
  - **Tests copy bugs:** given buggy code, LLMs wrote 3.84% bug-asserting tests, against 0.46% given the fixed code (Zhao, Zhou & Cohen, ISSTA 2026, arXiv 2607.22883) [F].
  - **Insecure snippets:** a Stack Overflow snippet was copied 180,388 times despite security warnings (Fischer et al., IEEE S&P 2017) [F]. Insecure answers scored higher than secure ones (Chen et al., ICSE 2019) [F]. 253 of 287 copied GitHub files still held the vulnerability (Verdi et al., TSE 2020) [F].
- **Generated text.**
  - ChatGPT and GPT-4 recognise 67% and 87% of their own false claims in a separate session, yet produce them to stay consistent (Zhang et al. 2023, arXiv 2305.13534) [F].
  - A user's wrong suggestion cut accuracy by up to 27% (Sharma et al., ICLR 2024) [F].
  - Model collapse occurs when generated data replaces the original (Shumailov et al. 2024, Nature 631:755) [F].
- **Law.** Overridden precedent keeps being cited (Broughman & Widiss) [F].
- **Against.**
  - Collapse is avoided when the original data are kept (Gerstgrasser et al. 2024, arXiv 2404.01413) [F].
  - Wikipedia catches 92% of the hoaxes it eventually detects within a day, through new-page patrol (Kumar, West & Leskovec, WWW 2016) [F]. These are whole fake articles, and survivors are unobservable.
  - Most meta-analyses are robust to individual retractions (Bakker 2024; Graña 2025) [F].
- **Unstudied.** Whether readers can tell a recorded inference from a recorded decision. Only indirect support: hypothesis to fact by citation; 5.4% acknowledgment of retractions.
- **Verdict.** Established; the inference-versus-decision clause is unstudied.
- **Rewording:** keep it. Qualify the last clause as a hypothesis.

### C8 — "An instruction cannot enforce itself"

- **For.**
  - **Nuclear procedures:** NRC inspections found "inadequate implementation of the EOP writer's guide" at many plants (IN 92-76, 1992) [F, practitioner].
  - **Aviation:** accidents were linked to checklists that existed but were misused or skipped (Degani & Wiener 1990) [F].
  - **Drug manufacturing:** 21 CFR 211.22(d), "Procedures not in writing, fully followed", was cited 201 times, rank 1 of 2,483 drug observations, in FDA FY2024 data [F, practitioner]. The citation merges "not written" with "not followed".
  - **Stack Overflow:** snippets with security warnings were copied more often (Fischer 2017) [F].
  - **Nimrod:** guidance text propagated an unchecked premise into the safety case [F].
- **Against (partial effect).**
  - An inline deprecation comment fixed 25.7–97.2% of deprecated completions, depending on the model (Wang et al. 2025) [F].
  - A precedence sentence moved agents to 91.4% code-following (Xu & Wu, earlier run) [E].
  - An explicit abort option cut ImpossibleBench gaming from 54% to 9% (earlier run) [E].
  - A point-of-reuse nudge steered developers to a validated secure alternative (Fischer et al., USENIX Security 2019) [F].
- **Pattern (inference, not tested by any one study).** Every measured countermeasure against propagation draws on something outside the propagated text: the reader's own knowledge (Brashier et al. 2020), retained original data (Gerstgrasser), a separate verification context (Zhang 2023), a separate statement of intent (Zhao 2026), a validated alternative (Fischer 2019), or a gate at creation (Kumar). Warnings written into the propagating text did not work (Fischer 2017), and vigilant prompting was inconsistent (Pan et al. 2023) [F].
- **Verdict.** Established as stated.
- **Rewording:** "An instruction cannot enforce itself: it shifts behaviour by a measurable but variable amount, and its presence does not establish its application."

---

## B. Findings by question

### Q1 — Names and fields

| Field | Name for the problem | Key sources (label) |
|---|---|---|
| Clinical guidelines | validity / obsolescence of recommendations; **surveillance**; update status; retirement; living guidelines; medical reversal | Shekelle 2001 [A]; Martínez García 2014 [V]; Neuman 2014 [F]; NICE PMG49 2025 [F]; Vernooij 2014 [F] |
| Systematic reviews | **signals for updating**; living systematic reviews; currency | Shojania 2007 [V(abs)]; Garner 2016 [F/V]; Elliott 2014/2017 [F/V]; Ahmadzai 2013 [F]; Millard 2019 [F] |
| Research integrity | post-retraction citation; persistence of error; evidence-ecosystem contamination; biblioremediation; expression of concern | Hsiao & Schneider 2021; Avenell 2019; Xu 2025; Davis 2012; Peterson 2010 [F]; RISRS 2022 [F] |
| Citation studies | **citation distortion** (bias, amplification, invention); quotation error; academic urban legends; read-before-you-cite | Greenberg 2009; Jergas & Baethge 2015; Simkin & Roychowdhury 2003 [F] |
| Law | **case validation**, negative treatment, citators; overrides vs overrulings, **shadow precedent**; **zombie laws**, dead crimes, desuetude; outstanding effects, revised legislation; post-legislative scrutiny; sunset and review clauses | Hellyer 2018; Christiansen & Eskridge 2014; Broughman & Widiss 2017; Wasserman 2021 [F] |
| Safety assurance | assurance cases; **defeaters**, eliminative argumentation, residual doubt; confidence arguments; **safety case maintenance**; dynamic / through-life safety cases; safety evidence change impact analysis | Bloomfield et al. 2024 [V]; Kelly & McDermid 1999 [F]; Denney, Pai & Habli 2015 [F]; de la Vara et al. 2016 [F]; Jaradat et al. 2014 [V] |
| Requirements engineering | traceability decay, **suspect links**, link validity; requirements completeness | Mäder & Gotel 2012 [F]; IBM ELM docs [F]; Luitel et al. 2024 [F] |
| Software architecture | **architectural knowledge vaporization**; architecture erosion / drift; decision recovery | Feilkas et al. 2009 [V]; Shahbazian et al. 2018 [V]; Tang et al. 2006 [F] |
| Software documentation | **up-to-dateness**; documentation issues; code–comment inconsistency; stale references; self-admitted technical debt (SATD), on-hold SATD | Aghajani 2019; Sun 2026; Radmanesh 2024; Zampetti 2018; Maipradit 2020 [F] |
| Clinical informatics | CDS knowledge management; terminology change impact; malfunction detection | Wright et al. 2016 [F] |
| Drug regulation | labelling consistency; user (readability) testing; bridging | Duke 2013 [A]; EC 2009 guideline [F] |
| Nuclear and aviation human factors | procedure verification and validation; writer's guide; integrated system validation; checklist design | NUREG-0899, NUREG-0711 [F]; Degani & Wiener 1990 [F] |
| Quality management | document control; obsolete documents at point of use | 21 CFR 211/820; FDA inspection observations [F] |
| Psychology | illusory truth effect; continued influence effect; post-hoc rationalisation | Fazio 2015; Lewandowsky 2012; Ecker 2022 [F]; Nisbett & Wilson 1977 (unreachable) |
| Organisation studies | organisational memory; **knowledge depreciation**; organisational forgetting; rule obsolescence; "paper deal vs real deal" | Argote, Beckman & Epple 1990 [F]; Macaulay 1963 [F]; Walsh & Ungson 1991 (unreachable) |
| ML / NLP | knowledge conflicts (context–memory, inter-context); temporal misalignment; abstention; hallucination snowballing; model collapse; CoT faithfulness; sycophancy; source bias; misinformation pollution | Xu et al. survey 2024 [F]; Xie 2024; Zhang 2023; Shumailov 2024; Chen 2025 [F] |

### Q2 — Bold claims

See § A.

### Q3 — Mechanisms by failure kind

See § C for the map. Three cross-field findings stand out.

1. **Signals sit at the source, not on the dependents** (I, from F evidence in five fields).
   - A retraction notice, a new trial, an overruling and a changed drug code all produce a signal where the change happens.
   - Dependent texts learn of it only through forward-citation searches, done ad hoc and at high cost (VITALITY used 60 trained volunteers [F]), or through editorial back-labelling years later (Christiansen & Eskridge [F]), or by chance (Wright [F]).
   - Where recommendation-to-evidence mapping is missing, as in ACC/AHA guidelines before 2008 [F], there is nothing to trigger a recheck.
2. **Date-based signals fail late.** Shojania: no review feature predicted a signal within 2 years, and "every two years will miss a substantial number of important signals" [V]. Fixed review dates of 2–5 years dominate guideline handbooks (Vernooij 2014) [F].
3. **Signals that need upkeep decay.**
   - Living reviews lag: 42% lag by more than 3 times their stated interval, and none declare retirement (Akl 2023) [A].
   - Statutory review deadlines are missed (RPC 2026) [F].
   - Suspect links can be set to "valid" automatically when a test case is approved (IBM ELM) [F].
   - No empirical study of how teams handle suspect links was found (unstudied).

### Q4 — How unfounded claims become knowledge, and what stops it

- **Mechanisms of spread.**
  - **Citation:** bias, amplification, invention (Greenberg [F]); copying references without reading (Simkin & Roychowdhury [F]); quotation errors at 14.5–25.4% [F].
  - **Repetition:** knowing the right answer does not protect against the illusory truth effect (Fazio et al. 2015, JEP:G 144:993) [F]. 92% of illusory-truth studies ran in a single session and 75% used trivia (Henderson et al. 2022) [F]. Evidence for expert readers is thin and conflicting.
  - **Correction:** corrections reduce reliance but rarely eliminate it (Lewandowsky et al. 2012, PSPI 13:106; Ecker et al. 2022, Nat Rev Psychol) [F]. Debunking science-relevant claims was not successful on average (d = 0.19, p = 0.131; Chan & Albarracín 2023, Nat Hum Behav) [F]. Backfire effects are mostly unsupported (Ecker 2022) [F].
  - **Generated text:** snowballing, sycophancy and false-premise acceptance [F]. Retrievers rank LLM-written documents higher (Dai et al. 2024) [F]. LLM-written misinformation in a corpus cut QA performance by up to 87% (Pan et al. 2023) [F].
  - **Software:** clones carry propagated bugs; 18.42% of bug-fixed clones did (Mondal et al. 2019) [F]. Tests copy bugs (Zhao 2026; Charoosaei 2026) [F]. Only 20.5% of obsolete Stack Overflow answers are ever updated (Zhang et al., TSE 2021) [F].
- **What has been shown to stop or slow it** (first-hand, measured).

  | Countermeasure | Effect and limit | Source |
  |---|---|---|
  | Retraction notice | Citations fell to less than half against matched controls | Kühberger 2022, PLoS One [F] |
  | | Contested: no long-term effect in an uncontrolled pre-post design | Candal-Pedreira 2020 [F] |
  | Accuracy judgement at first exposure | Prevents illusory truth only for claims the reader already knows to be false; lasted two days | Brashier et al. 2020, Cognition [F] |
  | Alternative-explanation corrections, warnings, repeated corrections | Reduce but do not remove reliance | Lewandowsky 2012; Ecker 2022 [F] |
  | Separate-context verification of each claim | Catches 67–87% of a model's own snowballed errors | Zhang 2023 [F] |
  | Retaining original data | Prevents model collapse | Gerstgrasser 2024 [F] |
  | Spec-first test generation (write an intent docstring, generate tests from it) | Fewer misguided tests, more bug-revealing ones | Zhao 2026 [F] |
  | Point-of-reuse nudge to a validated alternative | Steers developers to the secure equivalent | Fischer 2019 [F] |
  | Gate at creation | Catches whole-article hoaxes | Kumar 2016 [F] |
- **Unstudied.**
  - The effect of reference-manager retraction flags (Zotero, EndNote, Papers) on citing behaviour. RISRS agrees [F].
  - Whether citing papers adopt corrected values after an erratum.
  - The prevalence of citogenesis (search found only incident lists).

### Q5 — How fields decide a text is good enough to rely on

- **Stated, measured criteria exist in two places.**
  - **EU leaflet user testing** (EC 2009 guideline [F]): a per-question 16/20 rule, with RCT evidence of effect (Knapp 2011 [F]). Note that 90% × 90% is 81% while 16/20 is 80%. By this report's binomial calculation [I], the 95% CI for 16/20 is about 0.56–0.94.
  - **Nuclear emergency procedure verification and validation** (NUREG-0899 1982; NUREG-0711 Rev. 3 2012 [F]): desk verification against a writer's guide, walk-throughs for hardware match, simulator validation with pre-stated pass/fail criteria, and re-validation on substantial change. A practitioner paper shows pre-set criteria in use at Krško (Tecnatom, NENE 2021) [F].
- **Sign-off without a criterion fails measurably.**
  - Ethics-approved sheets failed reader tests (Knapp 2011) [F].
  - Many plants had "inadequate verification and validation" (IN 92-76) [F].
  - Checklists were approved without design criteria (Degani & Wiener) [F].
  - The Nimrod signatories did not read the reports [F].
- **Process appraisal is not validity.**
  - AGREE II appraises how a guideline was made, not whether its recommendations are right. A single rater is unreliable; the figures came through a fetch with an internal inconsistency, so verify before citing (Brouwers et al. 2010) [F(fetch)].
  - Watine 2006 found methodological quality and recommendation validity can conflict [A].
  - GRADE grades certainty of evidence reproducibly between trained raters (Mustafa 2013) [A].
- **Reader testing.**
  - Formative reader protocols such as the plus-minus method surface many reader-perceived problems, but give no rule for which to act on (de Jong & Schellens tradition) [A/F; Lentz & de Jong 2003 F].
  - Five-user samples are an unreliable stopping point (Faulkner 2003) [F].
- **Evidence gaps.**
  - No study links a passed leaflet test to real-world outcomes. One German study found the 2005 requirement's effect "barely recognisable" to patients, as summarised in PIL-S 2014 [F, secondary].
  - No source measured agents applying any of these mechanisms.

### Q6 — Finding missing decisions and unmarked open points

Building on the earlier run (RQ2, RQ6, RQ7), which found missing decisions are the most consequential failure and that only the author can say whether a freedom is intended [E].

- **Tools detect omissions poorly, and every result rests on synthetic or small ground truth.**
  - BERT/LLM term suggestion surfaced about 38% of simulated omissions; about 12% of suggestions were relevant (Luitel, Hassani & Sabetzadeh, REJ 2024, arXiv 2308.03784) [F].
  - The best model found a median 47% of expert-identified issues across 33 requirements. Miss rate was 1.00 for Necessity and about 0.89 for Correctness. For Completeness it was 0.50, and very unstable across runs (Shefa et al. 2026, arXiv 2609.03230) [F].
  - QuestBench and AbstentionBench (C6) show models rarely flag missing information [F].
- **Human reading techniques have a mixed record.**
  - Perspective-based reading teams beat others in only 2 of 4 domain-by-run cells, with no omission-specific yield reported (Basili et al. 1996 technical report, OCRed) [F].
  - A meta-analysis found "no clear positive effect" and "strong indicators of researcher bias" (Ciolkowski 2009) [A].
- **Marked open points are not stable.** Clarification TODOs are deleted unanswered, and debt comments disappear by accident (Maipradit 2020; Zampetti 2018) [F]. Marked and unmarked debt overlap little (Rantala et al. 2023) [A]. No study quantifies unmarked open points found later.
- **Assurance cases.**
  - In CoDefeater, GPT-3.5 zero-shot fully found more than half of the defeaters human analysts had recorded in two real assurance cases, and proposed five new feasible ones (Gohar et al. 2024, arXiv 2407.13717) [F, n = 2 cases].
  - A defeater list is a record of open doubts, but finding all defeaters "remains to be demonstrated" (SEI 2015) [F].
- **Detection versus resolution** (from C5).
  - The evidence separates the two: detection rates exist, but no study measures how often detected open points reach an owner and get decided.
  - The closest data are Nimrod (43 of 105 open hazards "sentence[d]" on a "manifestly inadequate" basis) and the SATD deletion rates [F].
- **Unreachable:** Ott 2012 (missing information as the dominant defect class) and Lutz 1993. "Missing information dominates" therefore rests on the earlier run's NaPiRE result [E].

### Q7 — Agents reading durable text as authority

Building on the earlier run's RQ3 and RQ8 [E: Xu & Wu, ImpossibleBench, HumanEvalComm, Ambig-SWE, TRACE].

- **(a) Superseded or contradictory text.** See C6 for the general benchmarks. Legal and clinical results:

  | Domain | Finding | Source |
  |---|---|---|
  | Law, general models | Zero-shot hallucination rates of 0.810 (GPT-4) to 0.972 (Llama 2) on the year a Supreme Court case was overruled. Asked when a never-overruled case was overruled, GPT-4 answered 53% of the time. Judging whether two cases agree was about chance | Dahl et al. 2024, *J. Legal Analysis*, arXiv 2401.01301 [F] |
  | Law, retrieval tools | Hallucinate 17–33% of the time. Lexis+ AI applied *Casey* after *Dobbs*. Inapplicable authority accounts for 0.23–0.38 of hallucinations; overruled authority is not separated (Table 6) | Magesh et al. 2024, arXiv 2405.20362 [F] |
  | Law, overruling opinion in context | Best 73% (C2) | Zhang, Savelka & Ashley 2025 [F] |
  | Law, treatment labels | Best 79.1% on coarse labels against Hellyer's annotations | Demir & Canbaz 2026, arXiv 2605.17691 [F] |
  | Court records | 2,367 cases (27 Nov 2026). By item: fabricated 3,850, misrepresented 1,965, false quotes 1,129, "outdated advice" 41 (overturned case law 21, repealed law 20). Either stale authority is rare in sanctioned filings or courts detect it far less; the data cannot tell which | Charlotin AI Hallucination Cases Database [F, practitioner] |
  | Retraction status | ChatGPT 4o-mini never once mentioned that an article was retracted, in 6,510 quality ratings, and affirmed about two-thirds of claims taken from retracted papers | Thelwall et al. 2025, *Learned Publishing* 38(4) [F] |
  | Memory updates | Knowledge-update questions show about a 30% drop (headline only) | LongMemEval (ICLR 2025) [F] |
  | Version-aware code | Execution feedback gains about 10–20 points | GitChameleon 2.0 [F] |
- **(b) Invented rationale.** See C5 and C6: Turpin 2023, Chen 2025, Lanham 2023 [F], Argus 2026 [F], Liu 2025 [F]. Self-explanation faithfulness depends on model and task (Madsen et al. 2024) [F, read at intro depth]. Pull-request descriptions written by agents versus humans were compared for alignment (Pham & Ghaleb, MSR 2026) [F]. No study measures downstream reading of agent-written rationale as intent.
- **(c) Agents as verifiers grounded outside the text.**
  - **External authority helps.**
    - SAFE agreed with human raters on 72% of atomic facts and was right in 76% of disagreements, at about $0.19 per response (Wei et al., NeurIPS 2024) [F].
    - Execution feedback is the largest gain for version-dependent code (GitChameleon) [F].
    - Gains in plan verification came from a sound external verifier; GPT-4 checking its own work fell from 16% to 1% (Stechly, Marquez & Kambhampati 2023) [F].
  - **Without an external authority it does not.**
    - The best verifier reached 21.1% recall and 6.1% precision on errata-grade errors in papers, and runs rarely rediscovered the same errors (SPOT, arXiv 2505.11855) [F].
    - About half of "very obvious" synthetic limitations were found (LimitGen, ACL 2025) [F].
    - Grounded verifiers over-assign "Supported" (FActScore) [F].
    - LLM judges favour their own generations (Panickssery et al., NeurIPS 2024) [F].
    - Agreement between models is weak evidence (earlier run: Kim et al. 2025) [E].
  - **Gap.** No study tests a grounded verifier against a project's own decision record, the case the statement is about.

---

## C. Mechanism map by failure kind

The baseline mechanisms E1–E11 of `research-inconsistency-detection-multi-artifact.md` §§ 1–3 are not repeated here. Their warrant classes still apply: construction, measurement, mandate. "Agents?" means an agent or LLM was measured using or failing the mechanism.

| Failure kind | Mechanism (field) | Detects | Misses | Cost | Evidence | Agents? |
|---|---|---|---|---|---|---|
| **Loss of validity** | Fixed review / expiry date (guidelines, 2–5 yr) | Nothing specific; forces a re-look | Early invalidation; texts invalid at publication | Low per text | Shojania [V(abs)]; Vernooij [F] | n |
| | Surveillance with update signals (Ottawa, RAND; NICE; AHRQ) | New evidence that plausibly shifts conclusions | Judgment variance; not validated against actual updates; capacity-bound | Moderate, repeated | Ahmadzai 2013; Garner 2016 [F] | n |
| | Living review with "last searched" stamp and currency limit | New studies within the search | Staleness when the living process stops; no retirement notice | High, monthly | Elliott 2017 [V]; Millard 2019 [F]; Akl 2023 [A] | n |
| | Citator flags (case law) | Explicit overrulings, mostly | 33–72% of negative treatment missed; no uncertainty shown | Editorial labour | Hellyer 2018 [F] | y, via legal AI (Magesh, Zhang) |
| | "Superseded by statute" back-labelling | Overrides, once some later text says so | Years of lag; 10%–⅓ never flagged | Editorial | Christiansen & Eskridge [F] | n |
| | Per-provision outstanding-effects box (legislation.gov.uk) | Known pending amendments | 4–8 week window; no accuracy audit found | Editorial team | Official FAQ [F] | n |
| | Statutory review / sunset clause | Forces a decision by a date | Missed deadlines; renewal by inertia | Department time | RPC 2026 [F]; Jones & Quandt 2025 [F, advocacy-affiliated] | n |
| | Suspect links (requirements tools) | Change to marked attributes of a linked artifact | Unlinked dependencies; semantic drift; auto-clear | Low to flag, human to clear | Vendor docs only [F] | n |
| | Evidence version manifest (safety cases) | Evidence built from older artifact versions | Whether the change matters; unannotated dependencies | Low once recorded | Jaradat 2014 [V], proposal | n |
| | GSN dependency trace / dynamic safety case monitors | Candidate impacted nodes; monitored claim violations | Implicit assumptions; unmonitored claims | Medium–high | Kelly & McDermid 1999; Denney 2015 [F], proposals | n |
| | Reference resolution (stale-reference repair) | Removed or renamed referents | A referent that exists but changed meaning | Low | Sun et al. 2026 [F] | y (LLM repair) |
| | Nightly conformance check against a formal architecture spec | Dependency-rule violations | Prose, rationale; text and code agreeing but both wrong | ~5 days setup | Feilkas 2009 [V] | n |
| | CDS regression tests / firing-rate anomaly detection | Rules that stop firing | Recommended, not evaluated | Moderate | Wright 2016 [F] | n |
| | Temporal scoping (dates in the query) | Shifts model to era-matching evidence | Needs dates in text | Very low | ConflictBank [F] | y |
| | Inline deprecation comment | Superseded API in context | Model-dependent; someone must know | Low | Wang et al. 2025 [F] | y |
| **Misrepresentation** (incl. omission, contradiction, unfounded premise) | Defeaters / eliminative argumentation (Assurance 2.0, SEI) | Recorded doubts without a refuting subcase | Unrecorded doubts; subcase judgment is a reading | High (expert) | Bloomfield 2024 [V]; SEI 2015 [F] | y (CoDefeater) |
| | Independent assessor / regulator challenge | Depends on diligence | Sign-off without reading | High | Nimrod [F]; Rinehart 2017 [F] | n |
| | Quantified confidence (BBN, Dempster-Shafer) | — | Implausible results; unvalidated | Medium | Graydon & Holloway 2016 [F] | n |
| | Capture-recapture over independent inspectors | Estimate of remaining detectable defects → stop/reinspect | Undetectable defects; underestimates | ≥3–4 independent reviews | Briand 2000 [F] | n |
| | Claim-specific citation network analysis | Citation bias, amplification, invention | One claim at a time; needs careful reading | High manual | Greenberg 2009 [F] | n |
| | Quotation-accuracy audit | Source misquoted | Whether the source is right | High manual | Jergas & Baethge; Mogull [F] | n |
| | Trustworthiness screening (INSPECT-SR, REAPPRAISE) | Integrity red flags before inclusion | Unvalidated | Moderate | VITALITY [F], named only | n |
| | LLM requirement-quality / completeness review | ~38–47% of omissions or issues | Necessity, correctness; unstable runs | Low per run; high triage | Luitel 2024; Shefa 2026 [F] | y |
| | Ask-to-detect-contradiction prompt | ~88% of explicit conflicts | Implicit conflicts; false conflicts in clean text | Very low | WikiContradict; Wang 2024 [F] | y |
| | Retrieval-grounded fact check (SAFE, FActScore) | Public atomic facts | Project-internal facts, decisions; leniency | ~$0.19/response | Wei 2024; Min 2023 [F] | y |
| | LLM paper verifier (SPOT, LimitGen) | ≤21% of errata-grade errors | Most real errors; non-repeatable | Moderate | SPOT; LimitGen [F] | y |
| **Misreading** | Performance-based user testing, per-question criterion (EU leaflets) | Key facts not found or understood | Correctness; unchosen facts; later edits; translations | ~20–50 interviews per round | EC 2009; Knapp 2011 [F] | n |
| | Procedure walk-through and simulator validation with pass/fail criteria (nuclear) | Text–world mismatch; actions impossible; timing | Unsampled conditions | High | NUREG-0899; NUREG-0711; Tecnatom 2021 [F] | n |
| | Usability sample-size rule | Share of discoverable problems | Rare problems; untested tasks | Per session | Faulkner 2003 [F] | n |
| | Independent interpretation by several readers (baseline E10/earlier RQ6) | Divergent readings | Correlated errors | High | [E] | y [E] |
| **Propagation** | Retraction notice / database / PubMed flag | Retracted status at source | 94.6% of citing contexts; 95% of web copies | Low | Hsiao & Schneider; Davis [F] | y (fails: Thelwall) |
| | Reference-manager retraction flag | Retracted items in a library | No measured effect | Near zero | RISRS [F] | n |
| | Forward-citation contamination search + re-analysis | Dependent reviews/guidelines; effect change | Ad hoc; supplements | High (60 volunteers) | VITALITY [F] | n |
| | Retained original alongside derived | Prevents collapse | Needs provenance | Storage | Gerstgrasser [F] | y (models) |
| | Spec-first test generation | Fewer bug-locking tests | Intent mis-derived from buggy code | One LLM step | Zhao 2026 [F] | y |
| | Point-of-reuse nudge to validated alternative | Insecure reuse | No validated alternative | Classifier + UI | Fischer 2019 [F] | n |
| | Patrol / gate at creation | Whole-article hoaxes | Claims inside valid text | Volunteer labour | Kumar 2016 [F] | n |
| **Reconstructed rationale** | Contemporaneous rationale norm (commit messages) | Presence of a "why" | Whether it was the deciding why | Low per commit | Dhaouadi 2024 [F] | n |
| | Rationale recovery (RecovAr; LLM DR generation; Argus) | Plausible decision links and arguments | The original reason; no ground truth | Low | Shahbazian 2018 [V]; Argus [F] | y |
| | CoT monitoring | Some hint use | Reward hacks (<2% verbalised) | Low | Chen 2025 [F] | y |
| **False assurance** (new kind) | Change-triggered re-validation (NUREG-0711 § 9.4) | Modified procedures | Changes not recognised as substantial | Per change | NUREG-0711 [F] | n |
| | Document control (approval, obsolete removal) | Obsolete copies at point of use | Content adequacy; adherence | Low–moderate | 21 CFR 211/820; FDA data [F] | n |
| | Citator / RAG red-flag suppression | Removes flagged citation | Keeps the statement; removes the trace | Design choice | Magesh 2024 [F] | y |
| **Non-application** | Inspection of adherence (FDA 483 observations, NRC EOP inspections) | Procedures not followed | Only what inspectors sample | High | FDA FY2024; IN 92-76 [F] | n |

---

## D. Fields and terms the brief missed

Each term below was found in full text by a track unless marked.

- **Clinical and science:**
  - surveillance; signals for updating; update status; retirement; living guidelines; medical reversal [A];
  - persistence of contradicted claims (Tatsioni & Ioannidis) [A];
  - citation distortion (bias, amplification, transmutation, back-door invention, the lens effect); biblioremediation; persistence of error;
  - evidence-ecosystem contamination chain; expression of concern; Crossmark / NISO CORREC; paper mills;
  - trustworthiness screening (INSPECT-SR); CDS knowledge management and terminology change impact.
- **Law:**
  - shadow precedent; overrides vs overrulings; implied overruling; case validation; negative treatment;
  - zombie laws, dead crimes, desuetude; outstanding effects; point-in-time versions;
  - post-legislative scrutiny (PLS); post-implementation review (PIR); statutory review requirement; regulatory stock;
  - contra-factual bias (accepting a false premise such as "this case was overruled").
- **Assurance:**
  - defeaters (rebutting, undercutting, undermining); eliminative argumentation; residual doubt; countercase; dialectic history; confidence arguments;
  - safety case maintenance (damage and recovery phases); dynamic / through-life assurance; safety evidence change impact analysis (SECIA);
  - "paper safety" / "shelf-ware" (Nimrod).
- **Requirements and software:**
  - link validity, suspicion profiles; traceability decay; trace maintenance;
  - up-to-dateness vs correctness vs completeness (Aghajani; this maps onto the first two of C2's kinds); externally induced staleness; link rot in comments;
  - on-hold SATD; accidental SATD removal; rationale components (Goal, Need, Alternatives, Constraints …);
  - capture-recapture / defect content estimation; fault-enforcing tests; misguidance effect.
- **Human factors and quality:**
  - performance-based readability testing; bridging (EU leaflets) [A];
  - integrated system validation (ISV); writer's guide; procedures generation package;
  - document control; obsolete documents at point of use;
  - reader-focused vs expert-focused text evaluation; plus-minus method.
- **Psychology and organisations:**
  - continued influence effect; prebunking / inoculation; accuracy nudge; processing fluency;
  - knowledge depreciation; organisational forgetting; rule obsolescence [A]; "paper deal vs real deal".
- **ML/NLP:**
  - knowledge conflict (context–memory, inter-context, intra-memory) and memorisation ratio; temporal misalignment; fact duration prediction; FreshQA;
  - abstention / selective prediction; information acquisition (QuestBench);
  - deprecated usage rate; version-conditioned code generation;
  - CoT faithfulness / monitorability; verifier leniency; self-preference;
  - hallucination snowballing; source bias; misinformation pollution; model collapse vs data accumulation.

---

## E. Disconfirming searches

Each search below was run by at least one track and reported in its notes.

### Is the problem solved somewhere?

| Search | Result | Conclusion |
|---|---|---|
| Systematic-review update signals validated against a gold standard | Ottawa method partly validated; AHRQ surveillance not validated; Cochrane reviews were not updated faster when signals appeared (Bashir 2018); "Mechanical rules appear unworkable" (Garner 2016) [F] | Not solved. Judgment-based, unknown sensitivity |
| Citators with low miss rates | Only Spriggs & Hansford 2000 calls Shepard's "quite reliable" [A]; vendors dispute Hellyer's ground truth. Full texts show substantial misses and lags [F] | Not solved |
| An official consolidated-law service that signals pending changes | legislation.gov.uk per-provision box with a stated lag [F]; no accuracy audit found | Closest to solved; unaudited |
| Assurance cases reliably signal invalidity after change | No outcome study; expert consensus "virtually none" contradicting evidence (Rinehart 2017) [F]; Sujan 2016 "no empirical evidence" [F] | Unstudied by outcome |
| Empirical study of suspect-link handling | Vendor docs, forums and a patent only | Unstudied |
| Explicit acceptance criterion measured to work | EU leaflets (Knapp 2011 RCT) and nuclear procedure validation [F] | **Partly solved** in these two fields, within the sample tested. Contradicts the categorical C4 |
| Stopping rule for review | Capture-recapture (Briand 2000); usability sample sizes (Faulkner 2003) [F] | Exists, with bounded coverage |
| Self-correction is fast | Wikipedia whole-article hoaxes: yes, under patrol (Kumar 2016). Stack Overflow, retraction, overrides: no [F] | Fast only with a gate at creation |
| LLMs detect conflicts reliably when asked | ~88% explicit, but uncalibrated both ways (WikiContradict; Wang 2024) [F] | Partial; not default behaviour |
| Grounded verifiers solve it | Yes for public facts and executable code; no for research errors, decisions, project-internal validity [F] | Solved only where an external authority exists |
| Models track staleness unprompted | Position drives the choice, not date (ConflictBank); stale code context followed 70–90% (Wang 2025) [F] | No evidence |
| Requirements incompleteness detection solved | Best evidence synthetic; completeness miss rate median 0.50, unstable [F] | Not solved |
| Reference-manager retraction flags reduce citing | No effect study found; RISRS agrees [F] | Unstudied |

### Is it not a real cost?

| Search | Result | Conclusion |
|---|---|---|
| Updated reviews rarely change conclusions | 9% (French 2005), 4% (Bashir 2018); 80% of class I recommendations retained, <1% reversed (Neuman 2014) [F] | **Strongest evidence against a large cost**, but the flipping minority is unpredictable |
| Removing retracted studies rarely changes meta-analyses | 96% within the original CI (Graña 2025) [F(fetch)]; "robust to individual retractions" (Bakker 2024) [F]; but 20.6% changed direction or significance among affected meta-analyses (VITALITY) and harm concentrates where few studies exist (OR 2.63 at ≤10 vs ≥20 studies) [F] | Mostly robust; concentrated harm |
| Post-retraction citations are mostly perfunctory or negative | Rejected: 83% positive (Bar-Ilan & Halevi 2017) [F] | Not disconfirmed |
| Outdated documentation causes little cost | Still judged useful (Lethbridge 2003) [F]; comment inconsistency raises bug-introducing commits about 1.5×, decaying over time (Radmanesh 2024) [F] | Real but moderate and context-dependent |
| Stale law or policy rarely causes harm | Hallucination database: "outdated advice" about 1% of items [F]; Macaulay: written contracts often ignored [F]; but overridden precedent cited at 89% [F] | Persistence shown; harm shown only anecdotally |
| Corrections backfire (would strengthen C7) | Mostly unsupported (Ecker 2022) [F] | Corrections partly work |
| Model collapse is inevitable (would strengthen C7) | No, if originals are kept (Gerstgrasser 2024) [F] | C7's generated-text form needs "when derived replaces original" |
| Rationale vaporization universal | 98.9% of Linux OOM commits carry rationale (Dhaouadi 2024) [F] | Context-dependent; recorded ≠ deciding unverified |
| Expertise protects against repetition | No study shows it; evidence thin and conflicting (Fazio 2015; Henderson 2022) [F] | Not disconfirmed |

---

## F. Limitations

- **Verification depth differs by source.**
  - Twenty claims passed 3-vote adversarial verification (notes 01). Five were refuted (notes 02) and are not used as support.
  - Everything labelled F was read once by one track and not cross-checked. Several F(fetch) texts were read through a tool that returns extracted quotes.
  - Treat F figures as the track's reading; spot-check before reuse.
- **Abstract-only figures.** Shekelle 2001 and Shojania 2007 figures rest on abstracts (the verifiers matched Shojania's figures word for word in the abstracts). Also abstract-only: Akl 2023, Kataoka 2022, Mott 2019, Duke 2013, Ciolkowski 2009, Spriggs & Hansford 2000, Watine 2006, de Jong & Lentz 1996, de Jong & Schellens 2000, Mustafa 2013, Rantala 2023.
- **Unreachable** (named in the notes):
  - Leveson 2011 (her points are known only through critics);
  - Wen et al. 2019; Aghajani et al. 2020; Ko et al. 2007; Nisbett & Wilson 1977;
  - Ott 2012; Lutz 1993;
  - Walsh & Ungson 1991; de Holan & Phillips 2004; Caygill's own texts;
  - EUR-Lex consolidation notice; Walter & Tukachinsky 2020; Dechêne 2010; Furman et al. 2012.
- **Synthetic ground truth.** Every omission-detection result rests on synthetic or small ground truth. No study measured detection of real undecided decisions in project text.
- **Many recent preprints.** Several agent results are 2025–2026 preprints (Charoosaei, Shefa, Argus, Demir & Canbaz) or use older models (GPT-3.5/4-era TruthfulQA, snowballing). Magnitudes may not transfer.
- **No measurement in the brief's setting.** No source measured durable text in git under reviewed pull requests with agents as authors and readers. Every transfer to that setting is inference.
- **Not done.** Per the brief, no remedy is proposed and the process is not designed.
