# Track t04: engineering fields: assurance cases, traceability, design rationale, documentation decay, SATD

Brief questions 1, 2, 3, 6. Claims C1, C2, C5, C7, C8.
Downloads: scratchpad `dl/t04/` (not in repo). "pdf p." = page of the PDF file. Otherwise the printed page or section is given.

## 1. Scope and searches run

Searches (arXiv API, NASA NTRS API, Europe PMC, figshare API, web search):
- arXiv: `ti:"Assurance 2.0"`; `au:Rushby AND ti:assurance`; `defeaters AND assurance`; `"safety case" AND maintenance`;
  `"self-admitted technical debt" AND removal`; `"code-comment inconsistencies"`; `rationale AND commit AND Linux`;
  `ti:"design rationale"`; `"architectural knowledge" AND vaporization`; `traceability AND decay`;
  `ti:"traceability in the wild"`; `"assurance case" AND LLM AND review`; `"safety case" AND empirical AND practitioners` (no hits).
- NTRS: "taxonomy of fallacies in system safety arguments"; "quantifying confidence in assurance arguments";
  "assurance case evaluation"; "safety case"; "dynamic safety cases through-life".
- Web: Leveson 2011 safety cases; Rinehart/Knight/Rowanhill NASA CR; Nimrod Review PDF; Kelly & McDermid 1999;
  Goodenough/Weinstock/Klein eliminative argumentation; "suspect links" traceability empirical; DOORS suspect links / link validity;
  traceability decay evidence; Aghajani 2019; Lethbridge/Singer/Forward 2003; Wen et al. 2019; SATD removal (Maldonado 2017,
  Zampetti 2018, Bavota & Russo 2016); Tang et al. 2006; Ko/DeLine/Venolia 2007; Al Safwan & Servant 2019; Nisbett & Wilson 1977;
  Shahbazian et al. RecovAr; de la Vara et al. 2016; Sujan et al. 2016; Fluri et al. 2007.

## 2. Findings

### A. Assurance and safety cases

**A1. Nimrod Review: a reviewed, signed-off safety case was not valid. Its open points were marked but not acted on, and it rested on a premise that its own guidance told authors to assume.**
- Source: Haddon-Cave C. (2009). *The Nimrod Review*, HC 1025, UK House of Commons.
  https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/229037/1025.pdf
- TYPE: first-hand study (public inquiry, evidence-based). ACCESS: full text read (chapters 9, 10A and 11 searched and read in part; 587 pages).
- Locators and quotes:
  - Ch.10A Summary para 7 (pdf p.194, printed p.189): "All three phases of the Nimrod Safety Case were fatally undermined by an
    assumption ... that the Nimrod was 'safe anyway', because the Nimrod fleet had successfully flown for 30 years, and they were
    merely documenting something which they already knew. The Nimrod Safety Case became essentially a paperwork and 'tick-box' exercise."
  - Para 9(1): "over 40% of the hazards remained "Open" and over 30% of the hazards remained "Unclassified". All these hazards had a
    potential severity rating of "Catastrophic"." The hazard that probably caused the loss (H73) was among them (para 9(3)).
  - Para 10: BAE represented that all hazards had been "appropriately identified, assessed and addressed" and "deliberately did not
    disclose ... the known figures for the large proportion of hazards which it had left "Open" and "Unclassified"".
  - Para 11 (pdf p.195): the IPT and QinetiQ agreed to "'sign off' the final Reports without sufficient inquiry, or asking for any
    underlying material, or even carefully reading the final Reports themselves".
  - Para 12: the IPT then "sentence[d] the remaining 43 out of 105 hazards which had been left "Open" ... on a manifestly inadequate,
    incorrect and unsatisfactory basis".
  - Ch.11 Summary para 3 (pdf p.263): "riddled with errors. It missed the key dangers. It was essentially a 'paperwork' exercise.
    It was virtually worthless as a safety tool."
  - Para 9.58 (pdf p.182): the guidance BP1201 (Annex C, Phase 1 strategy) told authors to "make the basic assumption that the
    aircraft is already operating to acceptable levels of safety and determine that level of safety." The reviewer comments:
    "Any genuine assessment should, however, be a matter of engineering judgment, not assumption. Otherwise, the process is self-defeating."
    Para 11.7: this "encourages 'documenting' the past rather than carrying out a fresh assessment".
  - Ch.11 fn.39 (pdf p.288): a Design Signatory's signature "was merely to ensure compliance with Design Engineering procedure DE101
    and did not relate to technical content."
- Bearing:
  - C2 (FOR): a misrepresentation ("all hazards ... addressed") did not show to the people who signed off.
  - C5 (FOR, strong): a premise nobody checked, inherited from guidance text. Finding and marking ("Open") were separate from
    resolving, and the owner's resolution was inadequate.
  - C7 (FOR): a premise in guidance text was carried into the derived safety case as if it were knowledge.
  - C8 (FOR): a sign-off and a mandated document did not establish that the analysis was done.
  - Q6: open points were marked, and the marks did not lead to action.

**A2. NASA review of whether assurance cases "work": supportive, but the evidence is mostly expert opinion and advocates. It is the strongest source against reading C1/C8 as "assurance cases fail".**
- Source: Rinehart D.J., Knight J.C., Rowanhill J. (2017). *Understanding What It Means for Assurance Cases to "Work"*.
  NASA/CR-2017-219582. https://ntrs.nasa.gov/citations/20170003806
- TYPE: review/secondary, plus interviews with 11 sources (A–K). ACCESS: full text read (relevant sections).
- Locators:
  - pdf p.27 quotes Hopkins (2012): "There are huge difficulties in trying to assemble empirical data on the effectiveness of safety
    case regimes ... quantitative cost-benefit analysis cannot be carried out."
  - Interviewee belief is "a dominant belief among practitioners", with the caveat "many of these practitioners are advocates of the method" (pdf p.27–28).
  - Nimrod case study §5.1.3.5 (pdf p.31–32): "fairly typical practitioners can fail to achieve assurance using safety case methods",
    but "it would be taking the evidence too far to say that the Nimrod example invalidates the perceived general benefit";
    "superficial compliance ... is a common threat to many assurance methods".
  - pdf p.36: Leveson's confirmation-bias concern "is only a serious threat when regulators do not provide an effective counter-balance".
  - Conclusion (pdf p.64): "Though we did not find a plethora of supporting evidence, we found far less contradicting evidence (virtually none)."
- Bearing: AGAINST a strong C1/C8 reading, because a competent independent assessor is a check that can fail. Evidence of efficacy is thin, as the report concedes.

**A3. Cross-industry review: no empirical evidence that safety-case regulation is more effective. "Paper exercise" and maintenance problems recur.**
- Source: Sujan M.A., Habli I., Kelly T.P., Pozzi S., Johnson C.W. (2016). "Should healthcare providers do safety cases? Lessons from a
  cross-industry review of safety case practices." *Safety Science* 84:181–189. https://eprints.whiterose.ac.uk/94390/
- TYPE: review/secondary (six UK industries). ACCESS: full text read.
- Locators:
  - §3.2.5 (pdf p.7): "there is no empirical evidence that regulation based upon a safety case approach is more effective than
    regulation that does not require the explicit production of safety cases".
  - Table, Defence row (pdf p.5): "Risk of complacency ... safety case development appears to have become a 'paper exercise' ...
    the focus ... has been on maintaining safety case argumentation rather than maintaining the safety of the system".
  - Petrochemical row: "ideally, safety reports would be living documents ... reports often run to several hundred pages ... It may be
    challenging to sustain such a level of effort without regulatory pressure."
- Bearing: C1 (FOR, weakly). C8 (FOR): the regime requires the text, but the text does not show that the safety work behind it happened.

**A4. Wilkinson's review of Leveson 2011 disputes her strongest empirical claim.**
- Source: Wilkinson P. (n.d., c.2013). Review of Leveson "The use of Safety Cases in Certification and Regulation". US CSB.
  https://www.csb.gov/assets/1/7/Wilkinson_Review_of_Leveson_Paper.pdf
- TYPE: practitioner report (critique). ACCESS: full text read.
- Locator (p.1): Leveson's statement that safety-case industries "have experienced much higher accident rates, such as offshore oil
  exploration and production" "does not appear to be substantiated and is not borne out by the published data (in the North Sea for example)".
  Wilkinson agrees there is "a lack of a rigorous evidential basis on which to judge the efficacy of safety cases".
  On confirmation bias, he points to "rigorous challenge to the documented safety case by a regulator" as the counter.
- Bearing: CONTESTED. Both sides agree that efficacy is unmeasured.
- Leveson (2011) ESD-WP-2011-13 itself: UNREACHABLE (dspace.mit.edu HTTP 429; sunnyday.mit.edu 503 and timeout).
  Her points are known only via Wilkinson, Rinehart and Hawkins 2025 (A9). Do not cite her wording as verified.

**A5. Reviewers of real safety arguments found many fallacies, and two reviewers disagreed widely.**
- Source: Greenwell W.S., Knight J.C., Holloway C.M., Pease J.J. (2006). "A Taxonomy of Fallacies in System Safety Arguments." ISSC 2006.
  NTRS 20060027794. https://ntrs.nasa.gov/citations/20060027794
- TYPE: first-hand study (2 reviewers, 3 public safety cases). ACCESS: full text read.
- Locators (pp.1–4, Tables 1–3):
  - EUR RVSM safety case (GSN part, 9 pages): Reviewer A 15, Reviewer B 18, combined total 29 fallacies (Table 1). Of the four
    premises for "sufficient direct evidence of [flight crew] training design validity", "only one ... pertains to the claim".
  - "the disparity between the results of each reviewer is significant". Their "fallacious use of language" instances "did not overlap".
  - EUR Whole Airspace: total 14 (Table 3). Opalinus Clay: reviewer B found none, reviewer A 3 (one later judged valid).
- Bearing:
  - C2 (FOR): published safety arguments contained relevance fallacies that the text did not signal.
  - C1 (FOR): review is a reading, and reviewers diverge.
  - Caveat: the RVSM and Whole Airspace cases were preliminary, and n=3.

**A6. Proposed quantitative confidence measures for assurance arguments are unvalidated and can give implausible results.**
- Source: Graydon P.J., Holloway C.M. (2016). *An Investigation of Proposed Techniques for Quantifying Confidence in Assurance
  Arguments*. NASA/TM-2016-219195. https://ntrs.nasa.gov/citations/20160006526
- TYPE: review plus counterexample analysis. ACCESS: full text read (abstract, §4).
- Locators:
  - Abstract (pdf p.5): "We know of little evidence to suggest that any proposed technique would deliver trustworthy results when
    implemented by system safety practitioners. Proponents do not usually assess the efficacy of their techniques through controlled
    experiment or historical study ... proposed techniques can deliver implausible results in some cases."
  - §4.3.1 (pdf p.20): "None of the surveyed papers shows this" (that the properties of the underlying theory entail accurate results).
  - Bloomfield & Rushby (A7) summarise the study as 12 proposals (5 BBN, 5 Dempster-Shafer-like, 2 other).
- Bearing: C1 (FOR). Even the "check" layered on an argument (a confidence score) lacks a demonstrated failure semantics.

**A7. Assurance 2.0 and eliminative argumentation: defeaters as an explicit, recorded search for doubt. Its authors concede it is not demonstrated in practice.**
- Sources:
  - Bloomfield R., Rushby J. (2020). "Assurance 2.0: A Manifesto." arXiv:2004.10474.
  - Bloomfield & Rushby (2024). "Defeaters and Eliminative Argumentation in Assurance 2.0." SRI-CSL-2024-01, arXiv:2405.15800.
  - Goodenough J.B., Weinstock C.B., Klein A.Z. (2015). *Eliminative Argumentation: A Basis for Arguing Confidence in System
    Properties*. CMU/SEI-2015-TR-005. https://doi.org/10.1184/R1/6573413.v1
- TYPE: standard-like method proposals (no outcome evaluation). ACCESS: full text read (relevant sections).
- Locators:
  - Manifesto §1 (p.1–2): "Competent and diligent external reviewers are good defenses against confirmation bias, but are typically
    involved only periodically and mostly toward the end of the development of a case."
  - Defeaters report §2 (pp.4–5): a refuted or addressed defeater is "retained as a kind of commentary to assist future developers and
    evaluators". The narrative "may be difficult to understand (because the context is changed in the modified case)".
    The evidence-incorporation block records "presence of the evidence, not its merit".
  - SEI TR §3.1 (pdf p.50): "assurance cases ... are inherently defeasible ... A confidence map can reflect only what is known at a
    particular time ... The concepts help in developing sound and complete arguments but do not guarantee that such arguments have been
    produced. We expect that this framework will help trained individuals ... reach agreement that all usefully important defeaters
    have been identified; of course, this remains to be demonstrated."
- Bearing:
  - Q3: this is the most developed mechanism for giving an argument text a signal that can fail. Each defeater is a stated way the claim could be false.
  - C1 (nuance): a check is defined, but the check is still a reading.
  - C4-adjacent: the method has no stopping rule for the defeater search, and the authors concede that.
  - C5: a recorded challenge history is the "record made at the time" for why an argument has its shape.

**A8. Safety case maintenance after change: the dependency structure is the mechanism. Standards demand revision but say little about how.**
- Source: Kelly T.P., McDermid J.A. (1999). "A Systematic Approach to Safety Case Maintenance." SAFECOMP'99, LNCS 1698.
  https://www.scsc.uk/documents/acwg/tpk/A_Systematic_Approach_to_Safety_Case_Maintenance.pdf
- TYPE: method proposal, informed by "discussions with Rolls-Royce safety engineers"; no evaluation data. ACCESS: full text read.
- Locators:
  - §1 (p.1–2) quotes the UK Railways (Safety Case) Regulations 1994 reg.6(1), "shall revise its contents whenever it is appropriate",
    and Def Stan 00-55 §4.7.1. Standards "offer little advice on how such operations can be carried out". Changes must be found
    "through the morass of poorly structured documentation ... Subjectivity plays a greater role in safety case maintenance than is desirable."
  - §2: "Some changes ... may seem innocuous at first ... but actually have a significant impact". "context is often assumed knowledge
    and assumptions are often implicit."
  - §9: impact assessment "cannot be performed mechanically ... The role of the tool is to pessimistically prompt the engineer".
- Bearing:
  - C2 (FOR): a change need not signal its impact.
  - C8 (FOR): a regulation requires revision but cannot make revision happen.
  - Q3: the GSN dependency trace flags candidates, and judgment decides.

**A9. Safety-case critique summary and "dialectic history" as a record.**
- Source: Hawkins R. (2025). "Developing Compelling Safety Cases." arXiv:2502.00911.
- TYPE: method proposal / review. ACCESS: full text read (§1, §5).
- Locators:
  - pp.3–4 summarise Leveson's critiques: "Confirmation bias", "After-the-fact assurance", and "Paperwork exercise", where a case
    becomes "shelf-ware".
  - pdf p.19: "huge value in maintaining the history of the challenge and counter-challenge ... If this dialectic history is lost, it
    is less clear to the reader why the safety argument approach adopted ... was chosen".
- Bearing: C5. Practitioners treat the recorded challenge history as the way to tell why an argument has its form. This is an argument, not evidence.

**A10. Version-manifest proposal for out-of-date safety evidence.**
- Source: Jaradat O., Graydon P., Bate I. (2014). "An Approach to Maintaining Safety Case Evidence After A System Change." arXiv:1404.6846.
- TYPE: proposal, illustrative example only. ACCESS: full text read.
- Locator (§II): annotate each solution with an "input manifest identifying the inputs (including version)". This allows automated
  checks such as "identify out-of-date evidence by searching for input manifests m = {(a1,v1)...} and artefact versions (a,v) such that
  ∃i • a = ai ∧ v > vi". The paper also notes that "existing safety claims might be nonsense, no longer reflect operational intent, or be
  contradicted by new data", and the version check does not detect these.
- Bearing: Q3 mechanism. It detects a changed dependency version, not semantic invalidity.

**A11. Dynamic safety cases (through-life): monitors tied to claims, and update rules.**
- Source: Denney E., Pai G., Habli I. (2015). "Dynamic Safety Cases for Through-Life Safety Assurance." ICSE NIER. NTRS 20150011054.
- TYPE: proposal (framework and illustrative UAS example). ACCESS: full text read.
- Locator (Fig.1, §II–III): the framework comprises a "collection of monitors providing the link between the [operational data and the
  argument]" and "update rules triggering actions in response". The paper notes "there is insufficient clarity on evolving the safety
  reasoning based on monitored data". No evaluation.
- Bearing: Q3 mechanism (a signal from the world into the text). It covers only what can be monitored. Unevaluated.

**A12. Industrial survey: safety-evidence change impact analysis is mostly done fully by hand.**
- Source: de la Vara J.L., Borg M., Wnuk K., Moonen L. (2016). "An Industrial Survey of Safety Evidence Change Impact Analysis
  Practice." *IEEE TSE* 42(12):1095–1117. Preprint: https://web-backend.simula.no/sites/default/files/publications/files/iasurvey_tse_preprint.pdf
- TYPE: first-hand study (survey, 97 valid responses, 16 domains, 28 countries, 47 standards). ACCESS: full text read (abstract, results headings).
- Locator (abstract, pdf p.1): respondents "had most often performed safety evidence change impact analysis during system
  development, from system specifications, and fully manually. No commercial change impact analysis tool was reported as used for all
  artefact types and insufficient tool support was the most frequent challenge ... the evolution of safety cases should probably be
  better managed". The challenge list includes "Insufficient confidence by assessor or certifier".
- Bearing: C1/C2 (FOR). Even in regulated domains, the validity of evidence after change rests on manual reading.

**A13. LLMs used to find defeaters (agents measured).**
- Source: Gohar U., Hunter M.C., Lutz R.R., Cohen M.B. (2024). "CoDefeater: Using LLMs To Find Defeaters in Assurance Cases." arXiv:2407.13717.
- TYPE: first-hand study (2 real assurance cases: LHC MPS and an sUAS battery case; GPT-3.5 zero-shot). ACCESS: full text read.
- Locator (§4.1, Fig.5): the model "completely identified more than half of all defeaters and partially identified more than a third in
  both datasets. Fewer than 15% of the defeaters created by human analysts were not identified at all". Cohen's kappa 0.81 between coders.
  For the sUAS case, the output gave "five novel defeaters", each "feasible upon further investigation". The authors also note
  "creative, redundant, and far-fetched" output.
- Bearing: Q3/Q6 (agents measured: y). LLM doubt-generation can surface missed doubts. Ground truth was the defeaters humans had already recorded, n=2.
- Related, ACCESS abstract only: Yu et al. (2025) "LLMs as Judges: Toward The Automatic Review of GSN-compliant Assurance Cases",
  arXiv:2511.02203. The abstract says "human reviewers are still needed to refine the reviews LLMs yield".
  Gohar et al. (2025) arXiv:2502.00238 is a literature-derived defeater taxonomy with seven categories (full text skimmed, method only).

### B. Requirements traceability and change impact

**B1. "Suspect link" / link-validity capability (reference only: which capability exists).**
- Source: IBM Engineering Lifecycle Management 7.0.3 documentation, "Link validity".
  https://www.ibm.com/docs/SSYMRC_7.0.3/com.ibm.jazz.vvc.doc/topics/c_linkval.html
- TYPE: standard/vendor documentation (commercial product used as a capability reference). ACCESS: full text read via WebFetch (summarised quotes).
- What it says:
  - A link is set suspect when a change touches an attribute "explicitly marked as Affects Link Validity".
  - Links are "suspect when they are new or unknown". It is "not a date-based check".
  - Clearing: "A person must verify whether the contents of both artifacts satisfy the intended meaning of the link".
  - An administrator can configure test-case links to be set Valid "automatically when a test case is approved".
  - Metadata changes and unmarked attributes do not trigger suspicion.
- Bearing:
  - Q3: this is the only widely deployed mechanism found that turns an upstream change into a flag on dependent text.
  - C1: the clearing step is a human reading.
  - C8: auto-clearing on approval shows a flag being cleared by a process event rather than by a check.

**B2. No empirical study of suspect-link handling found** (see §4). The traceability literature itself records how thin practice evidence is:
- Ruiz M., Hu J.Y., Dalpiaz F. (2023). "Why don't we trace? A study on the barriers to software traceability in practice."
  *Requirements Engineering* 28:619–637. https://digitalcollection.zhaw.ch/bitstream/11475/30590/1/2023_Ruiz-etal_Why-dont-we-trace_RequirementsEngineering.pdf
  - TYPE: first-hand study (survey of 55 practitioners, 14 interviews). ACCESS: full text read (abstract, intro).
  - Locator (abstract): "We have little evidence regarding how creating, managing, and using traceability links vary ... Traceability
    is mainly performed manually". Intro: manual traceability "often leads to trace links that quickly become outdated [23]".
- Mäder P., Gotel O. (2012). "Towards automated traceability maintenance." *JSS* 85(10). Europe PMC PMC3587459.
  - TYPE: method plus experiment. ACCESS: full text read (intro, §§1–2, 6 headings).
  - Locator (§1–2): "less attention has been paid to ensuring this traceability remains correct over time. This is the problem of
    traceability decay"; "Without maintenance, traceability relations ... get lost or represent false dependencies."
- Bearing: C2 (FOR). Q3: rule-based trace maintenance exists for UML models.

**B3. Engineers' "no impact" judgements in change impact analysis rest on trust in experience, not on checks.**
- Source: Borg M., Alégroth E., Runeson P. (2017). "Software Engineers' Information Seeking Behavior in Change Impact Analysis – An
  Interview Study." ICPC 2017. arXiv:1703.01897.
- TYPE: first-hand study (14 interviews, safety-critical company). ACCESS: full text read (results).
- Locators (§V, pdf p.5–8):
  - "Three out of 14 Ints (A, E, G) regard traceability" as very useful.
  - One interviewee "often accepts [trace links] although he questions their completeness".
  - A manager: "Our developers are skilled, if they say no impact I trust them". Another: "You must have completed many CIAs to know
    when answering that 'no impact' is reasonable."
- Bearing: C1 (FOR). The text that certifies "no impact" is itself unchecked. C8: the required CIA text does not establish that the analysis was done.

**B4. Incomplete traces in practice.**
- Rath M., Rendall J., Guo J.L.C., Cleland-Huang J., Mäder P. (2018). "Traceability in the Wild: Automatically Augmenting Incomplete Trace
  Links." ICSE 2018. arXiv:1804.02433.
  - TYPE: first-hand study (OSS projects). ACCESS: full text read (abstract, §2).
  - Locator: "on average only 60% of the commits" are linked to issues (abstract). §2: "approximately 43.3% of improvements and 42.4% of
    bugs have no commits associated with them". Unlinked commits ranged from "15% ... in Derby" to "approximately 76% ... in Maven".
- Fucci D., Alégroth E., Axelsson T. (2022). "When Traceability Goes Awry: an Industrial Experience Report." arXiv:2206.04462 (JSS).
  - TYPE: practitioner/experience report. ACCESS: full text read (§1–2).
  - Locator §1: "quality inflation": "the perceived mismatch between the organization level of quality assurance activities and the actual
    observed quality". Requirement-to-test "traces were generally lacking and ... reverse engineering these traces ... was not only
    time-consuming but also, in most cases, not possible". §2 adds that the success of DOORS-type tools is "tied to how rigorously they are used".
- Bearing:
  - C2 (FOR): links that would carry a change signal are often absent.
  - C7 (FOR, inference): QA artifacts asserting quality diverged from observed quality ("quality inflation").

### C. Design rationale and architectural knowledge

**C1-r. Contemporaneous rationale is often not recorded, especially alternatives and constraints.**
- Source: Al Safwan K., Servant F. (2019). "Decomposing the Rationale of Code Commits: The Software Developer's Perspective." ESEC/FSE 2019.
  https://people.cs.vt.edu/~khsaf/public/papers/fse19.pdf
- TYPE: first-hand study (20 interviews, 24 survey responses; self-report). ACCESS: full text read (RQ3–RQ4, discussion).
- Locator (pdf p.9): "The rarely recorded components were: alternatives, selected alternative, maturity stage, and constraints — even
  when developers need to find them on average multiple times per year (alternatives) and per month (remaining ones)." Also: "even if
  developers claim to frequently record rationale in general, there are many components of it that they are in fact not recording".
  Threats section: conclusions drawn "based on recollected memories".
- Bearing: C5 (FOR). The parts of a reason that distinguish it (alternatives, constraints) are the parts least recorded.

**C2-r. Survey of architects: most claim to document rationale, but "why chosen over alternatives" usually is not.**
- Source: Tang A., Babar M.A., Gorton I., Han J. (2005/2006). *A Survey of Architecture Design Rationale*. Swinburne TR SUTICT-TR2005.02
  (journal version JSS 79(12) 2006). https://figshare.swinburne.edu.au/articles/report/A_survey_of_architecture_design_rationale/26269849
- TYPE: first-hand study (survey, 81 valid responses; self-report). ACCESS: full text read (TR version, not the JSS version).
- Locators:
  - p.10 (pdf p.12): "62.9% of the respondents replied that they completely document DR"; "27.2% ... never or seldom document design
    weakness". The authors conclude "the reasons about why a design is chosen and why it is better than alternative designs are usually
    not documented".
  - Table 8 (pdf p.13): reasons for not documenting are "No time/budget 60.5%", "No standards 42%", "No suitable tool 29.6%", "Not useful 9.9%".
  - The questionnaire includes Q23 "I forget the reasons that justify my designs after a period of time". Its results are only in
    appendix charts, and the text says they are deferred to a separate paper, so no figure is reported here.
- Bearing: C5 (FOR, self-report). The partly disconfirming element is that self-reported documentation is high.

**C3-r. Disconfirming: in the Linux kernel OOM-killer component, almost every commit message carries rationale.**
- Source: Dhaouadi M., Oakes B.J., Famelis M. (2024). "Rationale Dataset and Analysis for the Commit Messages of the Linux Kernel
  Out-of-Memory Killer." ICPC 2024. arXiv:2403.18832.
- TYPE: first-hand study (366 commits, labelled). ACCESS: full text read (RQ1–RQ4).
- Locator: "98.9% of commits in our dataset contain sentences with rationale information", and average rationale density is
  "61.43%" (§4). The authors suggest that "the culture in the Linux kernel is sufficient to maintain the level of" rationale.
- Bearing: AGAINST a universal reading of "rationale vaporizes". Where strong review norms require a "why" in every commit, a
  contemporaneous record exists. It does not show the recorded reason was the deciding one.

**C4-r. Rationale-recovery studies have no ground truth for "the reason that decided". Validity is judged by readers' plausibility ratings.**
- Shahbazian A., Lee Y.K., Le D., Brun Y., Medvidovic N. (2018). "Recovering Architectural Design Decisions." ICSA 2018. Preprint arXiv:1704.04798.
  - TYPE: first-hand study (tool evaluation). ACCESS: full text read (§IV).
  - Locator (§IV-B, pdf p.7): "design decisions are not generally documented, hence a "ground-truth" for our analyses was not readily
    available". Validity was assessed against criteria by "Two PhD students". Recovered "rationales" are issue texts linked to changes.
- Zhou X., Li R., Liang P., et al. (2025). "Using LLMs in Generating Design Rationale for Software Architecture Decisions." arXiv:2504.20781 (v3).
  - TYPE: first-hand study (100 SO/GitHub architecture problems, 5 LLMs, 3 prompting strategies; 6 practitioner interviews). ACCESS: full text read (abstract, §5–6).
  - Locator (abstract): against expert-provided DR as ground truth, "Precision ... ranges from 0.267 to 0.278, Recall from 0.627 to
    0.715". "64.45% to 69.42% of the arguments of DR not mentioned by human experts are also helpful", "4.12% to 4.87% ... uncertain
    correctness", and "1.59% to 3.24% ... potentially misleading".
  - §6 (pdf p.29): the expert DR "are not necessarily the only correct answers and may be incomplete".
  - Interviews: no practitioner would "fully trust it without human validation".
- Bearing:
  - C5 (FOR). INFERENCE from the two texts: the field evaluates recovered rationale by plausibility to raters. Its methods therefore
    cannot tell recovered from reconstructed reasons.
  - C6 (FOR, agents measured: y): LLM-generated rationale is mostly arguments that no recorded decider gave, and the evaluation
    counts them as "helpful".

**C5-r. Not reached:** Ko, DeLine & Venolia (2007) "Information needs in collocated software development teams" (ICSE). Author PDF
returned 403 and the MSR page was blocked. Its abstract (via search) says design questions about the intent behind code were hardest
to satisfy. UNREACHABLE; lead only.
Nisbett & Wilson (1977) on post-hoc verbal reports (the psychology base for "reconstructed reason"): Cloudflare/HTML on all mirrors. UNREACHABLE.

### D. Documentation and comment decay

**D1. Out-of-date documentation is common, and practitioners still find it useful. This is the main disconfirming source for "cost".**
- Source: Lethbridge T.C., Singer J., Forward A. (2003). "How Software Engineers Use Documentation: The State of the Practice."
  *IEEE Software* 20(6):35–39. https://courses.cs.duke.edu//cps196.1/fall11/classwork/Lethbridge-Singer-Forward-2003.pdf
- TYPE: first-hand study (interviews at 13 sites; 14-week shadowing; survey of 48). ACCESS: full text read.
- Locators:
  - p.36: 44% somewhat agreed and 24% strongly agreed that "Documentation is always outdated relative to the current state of a
    software system" (n=45). Only 25 of 48 answered the update-latency question, and "SEs rarely update the documents" except test/quality docs.
  - p.37: 53% somewhat and 28% strongly agreed that documentation "can be useful, even though it might not always be the most up-to-date".
    "The more abstract a piece of documentation, the more likely SEs were to consider it accurate". Accuracy correlated with
    consultation for testing/quality and low-level design docs, but "Specifications ... 0.03" (Table 1).
  - p.38: documentation was consulted "only 3 percent of the time: 12 times over 357 logged events". The authors also write "evidence
    hints that the fault lies mostly with poor management and failure to gather requirements, not with out-of-date or incomplete
    documentation". That sentence is an assertion without data in this paper.
  - Sidebar: "A considerable fraction of documentation is untrustworthy."
- Related: Forward & Lethbridge (2002), "The relevance of software documentation, tools and technologies: a survey", DocEng 2002
  (full text downloaded; Table 2 modes "Rarely" for requirements/spec/design docs). This is the same survey data.
- Bearing:
  - C2 (FOR): docs go stale without signal.
  - AGAINST a strong cost claim: readers discount stale detail and rely on abstract text that stays valid. Readers act as their own staleness filter.
  - C1 (FOR): the reader's trust judgment is the only check.

**D2. A taxonomy of documentation issues with an explicit "lost validity after change" class.**
- Source: Aghajani E., Nagy C., Vega-Márquez O.L., Linares-Vásquez M., Moreno L., Bavota G., Lanza M. (2019). "Software Documentation
  Issues Unveiled." ICSE 2019. https://emadpres.github.io/pdfs/icse2019.pdf
- TYPE: first-hand study (878 artifacts from mailing lists, SO, issues, PRs; 162 issue types). ACCESS: full text read (§III-A).
- Locator (pdf p.6):
  - "Up-to-dateness (190). A document is outdated when it is not in sync with other parts of a system. Up-to-dateness differs from
    'Correctness' and 'Completeness' in that the information was correct and complete before a change was introduced."
  - "Up-to-dateness problems account for 39% of issues related to documentation content. In 21% of these cases, the inconsistency
    appeared to be between a system's behavior and its description".
  - Completeness: 268. Correctness: 72.
- Bearing: C2 (FOR, strong). This is the second failure kind of C2, named and counted, and distinct from misrepresentation (correctness).
- Aghajani et al. 2020 (ICSE, practitioners' perspective): UNREACHABLE (inf.usi.ch Cloudflare).

**D3. Comments made stale by changes elsewhere: a mechanical check catches them at scale. Maintainers had missed them for years.**
- Source: Sun K., Lyu Y., Ma X., Kuang H., Widyasari R., Zhang H., Ma X., Lawall J., Lo D. (2026). "We Must Have Missed This Comment:
  Detecting and Repairing Stale Function References in Linux Kernel Comments." ASE 2026. arXiv:2608.03734.
- TYPE: first-hand study plus tool (LLM-assisted repair; agents measured: y). ACCESS: full text read (abstract, §1, Table 4).
- Locators:
  - Abstract: "a comment becomes outdated because the function it mentions has been refactored or removed independently elsewhere".
    On v6.18-rc1, "ReCite detects 869 stale references". In a sample of 200 repairs, "178 (89.0%) provide useful repair guidance, with
    85 (42.5%) directly applicable". "Of our 75 submitted patches, 50 have been accepted."
  - §1: a maintainer replied, "We must have missed this comment ... a few years ago". The study covers "5,442" unresolved
    function-form symbols from "8,258 mentions".
- Bearing:
  - C1: confirms "a machine can check whether a reference resolves". The same check misses comments whose referent still exists but whose claim changed.
  - C2 (FOR): dependency change without signal, in one of the most heavily reviewed codebases.
- Related: Hata H., Treude C., Kula R.G., Ishio T. (2019). "9.6 Million Links in Source Code Comments: Purpose, Evolution, and Decay."
  ICSE 2019. arXiv:1901.07440. Full text read (abstract, RQ6). "Links are rarely updated, but many link targets evolve. Almost 10% of
  the links included in source code comments are dead". Summary box: "Links are rarely updated (less than 9%)".

**D4. Code-comment inconsistency and bugs: a modest association that is strongest just after the inconsistency appears.**
- Source: Radmanesh S., Imani A., Ahmed I., Moshirpour M. (2024). "Investigating the Impact of Code Comment Inconsistency on Bug
  Introducing." arXiv:2409.10781.
- TYPE: first-hand study (GPT-3.5 as the inconsistency detector; agents used as instrument). ACCESS: full text read (abstract, §§4–5 headings).
- Locator (abstract): "inconsistent changes are around 1.5 times more likely to lead to a bug-introducing commit than consistent
  changes"; "the impact ... is highest immediately after the inconsistency is introduced and diminishes over time".
- Bearing: C2 cost (FOR, but modest). The detector is an LLM, so the measurement inherits its error.
- Wen F., Nagy C., Bavota G., Lanza M. (2019). "A Large-Scale Empirical Study on Code-Comment Inconsistencies." ICPC 2019: UNREACHABLE (Cloudflare).
- Fluri B., Würsch M., Gall H. (2007). "Do Code and Comments Co-Evolve?" WCRE 2007: ABSTRACT ONLY. Via search snippet: "97% of
  comment changes are done in the same revision as the associated source code change". This would be partly disconfirming, but it is not verified.

### E. Self-admitted technical debt: marked open points and what happens to the marks

**E1. Marks of open points vanish without resolution, and removal is rarely recorded.**
- Source: Zampetti F., Serebrenik A., Di Penta M. (2018). "Was Self-Admitted Technical Debt Removal a Real Removal? An In-Depth
  Perspective." MSR 2018. https://aserebre.win.tue.nl/MSR2018-Fiorella.pdf
- TYPE: first-hand study (5 Java OSS projects; Maldonado et al. dataset). ACCESS: full text read (abstract, §§1–3, Table 2).
- Locators:
  - Abstract: "(i) between 20% and 50% of SATD comments are accidentally removed while entire classes or methods are dropped,
    (ii) 8% of the SATD removal is acknowledged in commit messages".
  - §1: earlier studies "interpreted [removal] as removal of the comments reflecting SATD rather than removal of the code affected".
  - §1: "between 25% and 72% of SATD comments are removed by the same developers that have introduced them".
  - §1: a Maldonado survey figure: "64% of SATD is removed when fixing bugs".
  - Table 2 gives per-project SATD and removal counts (column semantics not fully verified, so no figures are taken from it).
- Bearing:
  - C5 (FOR): a marked open point can disappear without a decision. The absence of the mark does not mean resolution.
  - Q6: removal of the mark is mostly unrecorded.
- Maldonado E., Abdalkareem R., Shihab E., Serebrenik A. (2017). "An Empirical Study on the Removal of SATD." ICSME 2017.
  Author PDF not found; ABSTRACT/secondary only. A search summary reports a median SATD survival of about 18–172 days; this is not verified.
- Bavota G., Russo B. (2016). MSR 2016: NOT REACHED (no open PDF found). Secondary summaries give "approximately 57%" removed; not verified.

**E2. Clarification-request TODOs are mostly "resolved" by deleting the question. "On-hold" debt waits on external events that nobody tracks.**
- Source: Maipradit R., Treude C., Hata H., Matsumoto K. (2020). "Wait For It: Identifying 'On-Hold' Self-Admitted Technical Debt."
  *EMSE*. arXiv:1901.09511.
- TYPE: first-hand study (335 SATD comments coded; classifier). ACCESS: full text read (§§1–3).
- Locators:
  - §3 (pdf p.11): "out of 43 comments which we coded as clarification request, 33 (77%) were "resolved" by simply deleting the comment
    (e.g., the comment "TODO why zero?" was removed ... without further explanation". Also "all comments of developers explaining
    technical debt were removed without addressing the debt."
  - §1: "it is unrealistic to assume that developers will be able to keep track of all self-admitted technical debt and of events that
    signal that certain self-admitted technical debt is now ready to be addressed". The classifier reaches AUC 0.83.
- Bearing:
  - Q6/C5 (FOR, strong, small n): a question marked in text was mostly closed by deleting it, not by answering it.
  - C2 (FOR): an on-hold condition ("if the Spring bug ... is resolved") can be met upstream, and nothing signals it in the text.
  - Q3: a mechanism exists, namely extracting the condition and watching for it.

## 3. Mechanisms

| Mechanism | Failure kind it signals | What it detects | What it misses | Cost | Evidence | Agents measured? |
|---|---|---|---|---|---|---|
| Defeaters / eliminative argumentation (Assurance 2.0, SEI) | misrepresentation (gaps, unsupported steps); some invalidity if doubts are re-raised | stated doubts and whether each has a subcase | unidentified defeaters, which the authors concede; no stopping rule; the resolution narrative goes stale after change | high (expert effort) | method papers only; "remains to be demonstrated" (A7) | partly: CoDefeater, GPT-3.5 zero-shot, more than half of human defeaters fully found (A13) |
| Independent safety assessor / regulator challenge | misrepresentation | depends on diligence | sign-off without reading (Nimrod, A1) | high | expert opinion only (A2–A4) | n |
| Quantified confidence (BBN, Dempster-Shafer) | overconfidence | n/a | can give implausible results; unvalidated (A6) | medium | counterexamples (A6) | n |
| GSN dependency trace for change impact (Kelly & McDermid) | lost validity after change | candidate impacted nodes, flagged pessimistically | implicit context and assumptions; judgment still decides | medium; tool needed | proposal; Rolls-Royce discussions (A8) | n |
| Evidence version manifests (Jaradat et al.) | lost validity (stale evidence) | evidence built from older artifact versions | claims that are now "nonsense" or contradicted by data; unversioned dependencies | low once recorded | proposal (A10) | n |
| Dynamic safety case monitors and update rules | lost validity in operation | monitored claim violations | anything not monitored; reasoning updates unclear | high | proposal (A11) | n |
| Suspect links / link validity (DOORS-type) | lost validity after upstream change | a change to marked attributes of a linked artifact | changes to unmarked attributes; missing links (30–76% of commits unlinked, B4); semantic drift; auto-clear on approval | low to flag, human to clear | vendor docs only; no empirical study found (B1, B2) | n |
| Rule-based trace maintenance (Mäder & Gotel) | trace decay | recognised edit patterns in UML models | changes outside the rule catalogue | medium | experiment (B2) | n |
| Reference resolution (ReCite; dead-link check) | lost validity: referent removed or renamed | unresolved symbols and dead URLs | a referent that exists but changed meaning; prose claims | low | 869 stale references in Linux; 50 of 75 patches accepted; about 10% of comment links dead (D3) | y (LLM repair) |
| LLM code-comment consistency check | lost validity, misrepresentation | inconsistent comment/code pairs | depends on LLM accuracy; local pairs only | low | used as instrument; OR about 1.5 for bugs (D4) | y |
| SATD markers (TODO/FIXME) and on-hold detection | open point marked | presence of marked debt; extractable wait-conditions | silent deletion of the mark (77% of clarification requests; 20–50% accidental removal) | low | E1, E2 | n |
| Contemporaneous rationale in commit messages (norm) | reconstructed rationale | presence of a "why" at the time | whether the stated why was the deciding one | low per commit; needs culture | Linux OOM 98.9% (C3-r) | n |
| Rationale recovery from history (RecovAr) / LLM DR generation | missing rationale | plausible decision-to-issue links / plausible arguments | the original reason: no ground truth (C4-r) | low | PhD-student ratings; LLM precision about 0.27 against expert DR | y (LLM) |
| Recorded "dialectic history" of challenges (Hawkins) | reconstructed rationale (why the argument has its form) | which challenges were considered | challenges never raised | medium; volume grows | argument only (A9) | n |

## 4. Disconfirming searches and results

- **Q: Evidence that assurance cases reliably signal invalidity after change, or work in practice.**
  - Found: Rinehart et al. 2017. Supportive expert opinion and "virtually none" contradicting evidence, Eurotunnel's record, and the
    Hopkins quote that effectiveness cannot be measured (A2). Wilkinson disputes Leveson's accident-rate claim (A4).
  - Conclusion: no outcome study shows that assurance cases detect invalidity. The strongest counter-evidence is expert consensus.
    "No check that can fail" overstates where a competent regulator challenges the case. "No check whose reliability is measured" is supported.
- **Q: Empirical study of suspect-link effectiveness, or clearing behaviour ("suspect link fatigue").**
  - Searches: "suspect links" traceability empirical; DOORS suspect links. Found only vendor docs, forum posts and a USPTO patent (not read).
  - Conclusion: no evidence either way. It is unstudied.
- **Q: Traceability decay rate measurements.**
  - Found: decay is named (Mäder & Gotel 2012) and "outdated quickly" is asserted (Ruiz 2023 citing [23]). No rate study was found.
    Mäder & Egyed is baseline and was not re-surveyed.
- **Q: Outdated docs cause little cost.**
  - Found: Lethbridge et al. 2003. Stale docs remain useful, readers rely on abstract docs, and blame lies "mostly" with management.
    That last point is asserted without data (D1).
  - Radmanesh 2024: inconsistency is associated with bugs, but modestly (about 1.5 times), and the effect decays over time (D4).
  - Conclusion: cost is real but moderate and context-dependent. Readers partly compensate for staleness. C2's "none needs to show"
    holds, but harm is not shown to be large on average.
- **Q: Rationale is recorded where norms require it (against "vaporization").**
  - Found: Linux OOM-killer, 98.9% of commits contain rationale (C3-r). Tang: 62.9% claim to document DR fully (self-report).
  - Conclusion: vaporization is context-dependent. Even where rationale is recorded, no study verifies that it is the deciding reason.
- **Q: Do code and comments co-evolve (against C2)?**
  - Fluri 2007 abstract: 97% of comment changes occur with code changes. This does not measure how many code changes leave comments
    stale. ABSTRACT ONLY, not verified.

## 5. Fields and terms the brief missed

- **Assurance/safety cases**: "defeaters" (rebutting, undercutting, undermining); "eliminative argumentation"; "residual doubt";
  "countercase"; "dialectic history"; "confidence arguments"; "safety case maintenance" (damage and recovery phases); "dynamic safety
  cases" / "through-life assurance"; "safety evidence change impact analysis" (SECIA); "implicit safety case" (Nimrod); "shelf-ware",
  "paper safety", "tick-box".
- **Traceability**: "link validity" / "suspicion profiles" (ELM); "traceability decay"; "trace maintenance"; "quality inflation"
  (Fucci et al.); "change impact analysis (CIA) reports" as unverified durable text.
- **Documentation**: "up-to-dateness" vs "correctness" vs "completeness" (Aghajani taxonomy, which maps onto C2's first two kinds);
  "externally induced staleness" (ReCite); "link rot in comments".
- **SATD**: "on-hold SATD" (the text waits on an external event); "accidental SATD removal"; clarification TODOs deleted unanswered.
- **Rationale**: "rationale density"; "architectural knowledge vaporization" (Jansen & Bosch; not read); "decision recovery"
  (RecovAr); "post-hoc rationalization" / verbal-report validity (psychology, Nisbett & Wilson; unreachable).

## 6. Thin or contested points; unreachable sources

- **Thin:**
  - The efficacy of every assurance mechanism here (defeaters, assessor review, confidence quantification) is unmeasured by outcome.
  - Suspect-link effectiveness is unstudied.
  - Rationale-recovery validity has no ground truth by construction.
  - The SATD clarification-deletion figure is small n (43).
  - CoDefeater is n=2 cases.
- **Contested:** whether safety cases are net positive (Leveson vs Wilkinson/Rinehart). Whether stale documentation is costly (Lethbridge vs Radmanesh/Aghajani).
- **Suggested rewordings (from this track):**
  - C1: "What a text says is generally held to no check whose reliability has been measured; where checks exist (independent
    challenge, defeater search, suspect flags) the decisive step is a human reading, and sign-off can occur without it (Nimrod)."
  - C5 (rationale clause): add "studies that recover rationale have no ground truth for the deciding reason and judge it by
    plausibility, so their success does not establish recovery".
- **Unreachable:**
  - Leveson 2011 ESD-WP-2011-13 (DSpace 429; sunnyday 503/timeout).
  - Wen et al. 2019 ICPC and Aghajani et al. 2020 ICSE (inf.usi.ch Cloudflare).
  - Ko et al. 2007 (403).
  - Nisbett & Wilson 1977 (Cloudflare mirrors).
  - Goodenough et al. 2013 ICSE NIER on DTIC (HTML page); the SEI 2015 TR was read instead.
  - Maldonado et al. 2017 and Bavota & Russo 2016 (no open PDF found).
  - Fluri et al. 2007 (abstract only).
  - Jansen & Bosch 2005, Kruchten/Lago/van Vliet 2006, Burge & Brown, Lee 1997: not attempted for lack of time. They are conceptual,
    and their empirical content is covered by Tang, Al Safwan and RecovAr.
