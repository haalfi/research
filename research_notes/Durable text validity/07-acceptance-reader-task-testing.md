# Track t07: acceptance criteria, reader/task testing, sign-off, V&V of procedures

Question 5 (how fields decide a text is good enough to rely on, and with what evidence). Claims C1, C4 (baseline: only new
full-text evidence that challenges "review has no stopping rule"), C8.

## 1. Scope and searches run

Queries (WebSearch unless noted; OpenAlex / Europe PMC / NASA NTRS / eCFR APIs used to locate full texts):
- `Raynor 2007 Health Technology Assessment "user testing" written medicine information systematic review hta11050`
- `user testing patient information leaflet 16 of 20 participants success criterion critique sample size statistical`
- `De Jong Schellens "Toward a document evaluation methodology" validity reliability evaluation methods pdf`
- `Lentz De Jong "expert-focused and reader-focused" text evaluation compared problems detected pdf`
- `"plus-minus method" document evaluation number of readers problems detected sample size de Jong pdf`
- `NUREG-0899 "Guidelines for the Preparation of Emergency Operating Procedures" pdf verification validation` (+ variant with walk-through/simulator)
- `NUREG-1358 lessons learned special inspection program emergency operating procedures deficiencies verification validation`
- `emergency operating procedure validation simulator discrepancies found number of procedure errors identified study nuclear`
- NTRS API `Degani Wiener checklist`
- `Watine "conflict between guideline methodologic quality and recommendation validity" AGREE`
- OpenAlex: AGREE II development part 1; GRADE reproducibility; capture-recapture software inspections (3 queries)
- `study package leaflets that passed readability user testing still comprehension problems patients EU marketed leaflets evaluation`
- `Fuchs "The way forward in package insert user tests from a CRO's perspective" ...`
- `Faulkner 2003 "Beyond the five-user assumption" ...`
- `ISO/IEC/IEEE 26513:2017 "requirements for testers and reviewers of information for users" scope`
- `Sless Communication Research Institute diagnostic testing ... 81% consumer medicine information Australia` (nothing relevant returned)
- eCFR API: 21 CFR 820.40 (2024-01-01 version), 21 CFR 211.100 (2025-01-01); FDA "Inspection Observations" FY2024 spreadsheet.

## 2. Findings

### A. Medicine leaflets: an explicit, measured acceptance criterion for a text exists

**A1. EU readability guideline gives a numeric, per-question pass criterion for a leaflet.**
- Source: European Commission, DG Enterprise and Industry, *Guideline on the readability of the labelling and package leaflet of medicinal products for human use*, Revision 1, 12 Jan 2009 (in operation 12 Jun 2009; supersedes 29 Sep 1998 version). https://health.ec.europa.eu/system/files/2016-11/2009_01_12_readability_guideline_final_en_0.pdf
- TYPE: standard (regulatory guideline). ACCESS: full text read.
- Locators/quotes:
  - Ch.3 s.1 quotes Directive 2001/83/EC Art. 59(3) as amended by 2004/27/EC: "The package leaflet shall reflect the results of consultations with target patient groups to ensure that it is legible, clear and easy to use." Art. 61(1): results "shall also be provided to the competent authority". Art. 63(2): leaflet must enable "the users to act appropriately".
  - Ch.3 s.3.1: user testing "is a development tool ... Testing itself does not improve the quality of the information but it will indicate where there are problem areas which should be rectified." Must be done on a full mock-up as supplied. s.3.2: other methods acceptable if justified, "case-by-case".
  - Ch.3 s.7: authorities look for "evidence that people who are likely to rely on the package leaflet can understand it and act appropriately"; evidence must show they "can pick out the relevant information, interpret this and describe the action they would take"; "The key information will need to be defined prior to the consultation by the marketing authorisation holder".
  - Annex (explicitly "for illustrative purposes only") s.3: pilot of 3-6; "repeat tests until you have satisfactory data from a group of 10 participants"; final 10 more, i.e. 20 on the final leaflet. s.4: usually 12-15 questions, "phrased differently from the text", random order, "include a set of expected correct answers".
  - Annex s.5 "SUCCESS CRITERIA" (pp.26-27): "A satisfactory test outcome ... is when the information requested within the package leaflet can be found by 90% of test participants, of whom 90% can show that they understand it. That means to have 16 out of 20 participants able to find the information and answer each question correctly and act appropriately ... The success criteria will need to be achieved with each question. Results cannot be aggregated." Also: "Drafting easy or trivial questions simply with an aim of ensuring success must not occur." Different performance methods may have different criteria, judged "case-by-case".
- Bearing: **against C4 as worded** ("without acceptance criteria stated for a text, review has no criterion"): here a criterion is stated, numeric, per item, and gives a stop point for test-revise cycles. **For C1 partially**: the criterion tests finding/understanding of key facts the applicant chooses; it does not test whether the leaflet's content is correct. Note 90% x 90% = 81%, but the operational figure is 16/20 = 80% (internal arithmetic inconsistency in the guideline; noted also by secondary sources).

**A2. Operating characteristic of the 16/20 rule (my computation).**
- TYPE: inference (binomial arithmetic, independence assumed). ACCESS: n/a.
- Exact (Clopper-Pearson) 95% CI for 16/20 = 0.563 to 0.943. P(a question with true success rate 0.70 passes) = 0.238; at 0.80 = 0.630; at 0.90 = 0.957. If 15 questions each had true rate 0.90, P(all pass) = 0.516 (independence assumed).
- Bearing: the rule is a weak certificate for any single question (a question at 70% passes about a quarter of the time) but the no-aggregation clause makes passing a whole leaflet demanding. The criterion measures against a question set the applicant defines, so its coverage is bounded by that set (C3/C5 relevance: what is not asked is not tested).

**A3. User testing found defects in documents that had already passed expert/ethics review; criterion-guided revision transferred to an independent sample.**
- Source: Knapp P, Raynor DK, Silcock J, Parkinson B. "Can user testing of a clinical trial patient information sheet make it fit-for-purpose? - a randomized controlled trial." *BMC Medicine* 2011;9:89. doi:10.1186/1741-7015-9-89. PMC3152894.
- TYPE: first-hand study (developmental user testing + parallel-group RCT). ACCESS: full text read (Europe PMC XML).
- Locators: Background: in three earlier studies "the existing sheets (which had been approved by NHS research ethics committees) were flawed in their ability to allow people to find and understand important aspects of the trial in relation to safety, efficacy, consent and practical details." Developmental phase: original AML16 sheet, 20 participants: "3 questions (7, 17, 21) had significant problems, with fewer than 16 of 20 participants being able to find the answer and show understanding. Only 3 of the 20 participants (15%) ... clear round". After two revisions (50 participants over three rounds): "On only 1 of the 21 questions did fewer than 16 out of 20 participants find and show understanding". RCT (Abstract/Results): 123 randomised (116 interviewed); "66% of participants who read the revised PIS were able to show understanding of all aspects of the trial, compared with 15% of those reading the original version (Odds Ratio 11.2; Chi-square = 31.5 p < .001)"; 87.1% preferred revised.
- COI noted in paper: authors linked to Luto Research (user-testing company) / design services.
- Bearing: **for C1/C4** (sign-off by an ethics committee did not detect reader-failure defects that a task test found); **against C4's strong form** (an explicit criterion + task test + revision converged in three rounds and the improvement held in an independent randomised sample). Also illustrates C3.

**A4. Same pattern, Phase 3 IVF trial sheet.**
- Source: Knapp P, Raynor DK, Silcock J, Parkinson B. "Performance-based readability testing of participant information for a Phase 3 IVF trial." *Trials* 2009;10:79. PMC2743679.
- TYPE: first-hand study. ACCESS: full text read.
- Locator (Results, "Original information sheet"): "Answers to three of the 21 questions were found and understood by fewer than 80% of the 20 participants"; "In total 30 (of 420) question items were not understood"; "Only 2 of the 20 participants were able to find and show understanding of all 21". Revised version preferred by 18/20.
- Bearing: as A3 (smaller, uncontrolled).

**A5. The acceptance gate is bypassed by later changes and covers only new texts (EC-commissioned evaluation).**
- Source: van Dijk L, Patrício Monteiro S, Vervloet M, de Bie J, Raynor DK. *Study on the Package Leaflets and the Summaries of Product Characteristics of Medicinal Products for Human Use (PIL-S study)*. European Union, July 2014. https://health.ec.europa.eu/system/files/2016-11/pil_s_0.pdf
- TYPE: review/secondary (literature review + stakeholder survey/consultation, commissioned by EC). ACCESS: full text read.
- Locators: Conclusion 3 (pp.9-10): "Sometimes last minute changes in the information are required by the authorising body which are not then subject to user testing"; user testing "in only one language is required. Yet ... lay language is sometimes translated back to more formal language". s.3.2.2 (p.31): "only one paper tried to examine the impact of the legislative change in 2005" (ref 26: Beime B, Menges K, *Pharmaceut Reg Affairs* 2012;1:120, German PILs) and found a "trend towards improvement" but the effect is "'barely recognisable' by patients, as only new products on the market need to be tested in most EU countries such as Germany". s.6.3.3 (p.86): a communication expert questions whether current readability tests are "optimally suited to check and confirm whether or not a text is really 'readable'".
- Bearing: **for C2** (validity established at one version is not re-established when the text changes after the gate; translations not tested) and for C1 in practice; shows the measured criterion's scope gap. Evidence of the regulation's real-world effect is thin (one German study, read here only as summarised).

**A6. Systematic review (HTA) excluded user-testing studies from its effectiveness evidence and judged testing of predesigned leaflets of limited impact.**
- Source: Raynor DK, Blenkinsopp A, Knapp P, et al. "A systematic review of quantitative and qualitative research on the role and effectiveness of written information available to patients about individual medicines." *Health Technology Assessment* 2007;11(5). doi:10.3310/hta11050. PDF via https://njl-admin.nihr.ac.uk/document/download/2001459
- TYPE: review/secondary. ACCESS: full text read.
- Locators: inclusion criteria (methods appendix): effectiveness designs "But not: (a) user testing studies (b) application of readability formulae". Conclusions, "Regulatory authorities" (p.87): "User testing is an important change ... However, without consumer involvement in content setting and development, testing a predesigned leaflet will, although useful, be of limited impact."
- Bearing: user testing tests usability of chosen content, not choice/correctness of content (supports C1/C5 framing: the test can pass a text that says the wrong or insufficient thing). Note authors' COI (LUTO Research) declared on front matter.

**A7. Critique of EU user-testing policy (sample diversity, sponsor-run tests, translations).**
- Source: Pelizzari N. "The Challenges for EU User Testing Policies for Patient Information Leaflets." *IJERPH* 2024;21(10):1301. PMC11507276.
- TYPE: review/secondary (qualitative document analysis; author notes reliance on secondary data). ACCESS: full text read.
- Locators: s.4.2: "When pharmaceutical companies conduct their own user testing, there is a potential for conflict of interest"; independent third-party testing "seldom mandated"; s.4.4: lack of protocols for translated PILs. No new empirical data.
- Bearing: criterion exists, but who applies it and on what sample is not controlled (C8-adjacent: the requirement does not enforce its own faithful application). Weak evidence (secondary).

**A8. Patient comprehension of original vs redesigned leaflets (German PAINT survey).**
- Source: Fuchs J. (PAINT-Consult), conference abstract, German Medical Science GMS, gaa2006 meeting. https://www.egms.de/static/en/meetings/gaa2006/06gaa02.shtml
- TYPE: first-hand study. ACCESS: abstract/record only.
- Reported (abstract): 1,105 / 1,051 respondents; correct answers 92.6-94.4% for redesigned "replicas" vs 74.7-85.8% for five original inserts; dosage instructions most misunderstood. Lead only.

### B. Document evaluation research (reader-focused vs expert review)

**B1. Technical writers do not predict reader problems; little agreement among experts.**
- Source: de Jong MDT, Lentz LR. "Expert judgements versus reader feedback: a comparison of text evaluation techniques." *Journal of Technical Writing and Communication* 1996;26(4):507-519. Record: https://research.utwente.nl/en/publications/expert-judgements-versus-reader-feedback-a-comparison-of-text-eva/
- TYPE: first-hand study. ACCESS: abstract/record only (no OA full text found).
- Abstract: 15 technical writers vs 30 target readers (plus-minus method, questionnaire, user protocols) on a public information brochure: "The results of both kinds of text evaluation show little overlap. The technical writers only predicted a small proportion of the reader feedback, and produced a lot of new problem detections. In addition, there was little agreement among the technical writers".
- Bearing: for C1/C3/C4 (expert review is not a reliable proxy for reader testing; reviewers disagree). Unverified in full text.

**B2. Key review on validity/reliability and sample size of evaluation methods.**
- Source: de Jong M, Schellens PJ. "Toward a document evaluation methodology: what does research tell us about the validity and reliability of evaluation methods?" *IEEE Transactions on Professional Communication* 2000;43(3):242-260. doi:10.1109/47.867941.
- TYPE: review/secondary. ACCESS: abstract/record only (OpenAlex: closed; Twente record has no file; CiteSeerX connection reset).
- Abstract: four lines of research: "validity of evaluation methods, sample composition, sample size, and the implementation of evaluation results during revision". Content not verified. UNREACHABLE in full text.

**B3. One reader-focused pretest of one text yields ~150 distinct problems.**
- Source: Lentz L, de Jong M. "In welke termen denken lezers over tekstproblemen?" *Tijdschrift voor Taalbeheersing* 2003;25(3). DBNL: https://dbnl.org/tekst/_tij009200301_01/_tij009200301_01_0025.php
- TYPE: first-hand study (secondary use of earlier pretest data). ACCESS: full text read (Dutch).
- Locator s.2.1: "De pretest met Focus leverde 148 verschillende problemen op; de plus-en-minmethode leverde 157 problemen op" (one text each).
- Bearing: for C4 (reader feedback produces more problems than can be acted on; selection among them needs its own criterion).

**B4. Usability problem discovery: the "5 users" stopping heuristic is unreliable.**
- Source: Faulkner L. "Beyond the five-user assumption: benefits of increased sample sizes in usability testing." *Behavior Research Methods, Instruments, & Computers* 2003;35(3):379-383. doi:10.3758/BF03195514.
- TYPE: first-hand study (60 users, resampling, web application, not a document). ACCESS: full text read.
- Locators: Abstract: "Some of the randomly selected sets of 5 participants found 99% of the problems; other sets found only 55%. With 10 users, the lowest percentage of problems revealed by any one set was increased to 80%, and with 20 users, to 95%." Results: 5 users mean 85% (SD 9.3, 95% CI ±18.5%); 10 users 95% (SD 3.2, ±6.4). Discussion: "Each usability problem has its own probability of being found".
- Bearing: **partial challenge to C4**: sample-size stopping rules exist for test-based evaluation, but their guarantee is relative to the problems that the full 60-user sample found, with wide variance. Applies to documentation usability testing by analogy (inference).

### C. Document inspection: a statistical stopping rule exists (capture-recapture)

**C1-cr. Capture-recapture estimation of remaining defects as a reinspection criterion for requirements documents.**
- Source: Briand LC, El Emam K, Freimut BG, Laitenberger O. "A comprehensive evaluation of capture-recapture models for estimating software defect content." *IEEE TSE* 2000;26(6). doi:10.1109/32.852741. Read as Fraunhofer IESE report version: https://publica.fraunhofer.de/bitstreams/f511cb63-4185-4028-8af6-c3cd921f1a32/download
- TYPE: first-hand study (real inspection data). ACCESS: full text read (IESE report; PDF text is character-shifted; digits not recoverable, so no figures reported from it).
- Locators: Abstract: "An important requirement to control the inspection of software artifacts is to be able to decide, based on objective information, whether inspection can stop or whether it should continue"; "models are strongly affected by the number of inspectors ... When the number of inspectors is too small, no model is sufficiently accurate and underestimation may be substantial"; recommends the Mh model with Jackknife estimator. Introduction: alternative rules (historical benchmark; upper/lower defect-density thresholds) — the threshold approach "raises the risk that inspectors are tempted to only find a passing number of defects regardless of the document's quality". Data section: "The artifacts under study were requirement documents" (two generic ATM/parking garage documents; two NASA GSFC functional specifications in natural language). Conclusions: estimators mostly underestimate; models "ought not be used for less than three inspectors" with perspective-based reading (ad hoc minimum also stated, number not recoverable).
- Bearing: **the strongest new challenge to C4 ("review has no stopping rule")**: software engineering has a studied, objective stopping rule for reviewing natural-language documents. Limits: it estimates the remaining defects of the kinds the inspectors can detect (correlated blind spots stay invisible, cf. Kim et al. already covered), it underestimates, and it needs >=3-4 independent reviewers. So "no stopping rule" should become "no stopping rule that bounds undetectable defects; available rules estimate only what the reviewers could have found".
- Lead not read: Petersson H, Thelin T, Runeson P, Wohlin C. "Capture-recapture in software inspections after 10 years research - theory, evaluation and application." *JSS* 2004 (doi:10.1016/S0164-1212(03)00090-6). ACCESS: record only.

### D. Nuclear emergency operating procedures: V&V as a required gate

**D1. NUREG-0899 defines V&V objectives for EOPs; methods; no numeric pass criterion.**
- Source: US NRC, NUREG-0899, *Guidelines for the Preparation of Emergency Operating Procedures: Resolution of Comments on NUREG-0799*, August 1982. ADAMS ML102560007 (scanned; read as page images).
- TYPE: standard (regulatory guidance). ACCESS: full text read for ss.2.6, 3.3.5 (pp.4, 9-10) and TOC.
- Locators: s.2.6 (p.4): "'validation' and 'verification' have been used to describe the processes by which procedures are evaluated against a set of objectives ... The distinction between validation and verification has not been consistent and clearcut". s.3.3.5 (p.9): "After EOPs have been developed they must undergo a process of validation/verification ... to establish the accuracy of information and/or instructions, to determine that the procedures can be accurately and efficiently carried out, and to demonstrate that the procedures are adequate to mitigate transients and accidents." s.3.3.5.1 (pp.9-10): methods: simulator (plant-specific or generic), control room walk-throughs, desk top reviews, seminars and workshops, computer modelling; objectives (a) technically correct, (b) written correctly per writer's guide, (c) "usable, i.e., they can be understood and followed without confusion, delays, errors, etc.", (d) correspondence with control room/plant hardware, (e) language compatible with staff qualifications, (f) "a high level of assurance that the procedures will work". "item 'd' above can only be adequately addressed using control room/plant walk-throughs, while item 'f' should be addressed using an approach that includes simulation." s.3.3.5.2: correct discrepancies by changing "the control room, the procedures, the staffing, the training, or some combination". (A copy on the INL TMI-2 site states compliance is not required; that copy was not reachable, 502, so this is not verified here.)
- Bearing: a field where a procedure text must pass a test that can fail (walk-through and simulation against hardware and scenarios): **against C1's generality**; but objectives are qualitative (no stated pass threshold) — **consistent with C4**. Objective (d) is a check of text against the world that only physical walk-through achieves.

**D2. Regulator's inspections found V&V and writer's-guide application inadequate at "many" plants a decade later.**
- Source: US NRC Information Notice 92-76, "Issuance of Supplement 1 to NUREG-1358, 'Lessons learned from the special inspection program for emergency operating procedures (conducted October 1988 - September 1991)'", 13 Nov 1992. ADAMS ML031190761.
- TYPE: practitioner report (regulator's inspection findings). ACCESS: full text read (3 pp., page images).
- Locators: p.1: "the staff found continuing deficiencies in the EOP programs at a number of plants"; NUREG-1358 (April 1989) issued "to reiterate the critical elements ... described in NUREG-0899". p.2: "many licensee EOP programs were found to have one or more of the following weaknesses": incl. "2. inadequate implementation of the EOP writer's guide or inadequate guidance provided in the writer's guide", "3. inadequate verification and validation of the EOPs and EOP support procedures", "5. failure to adequately control the EOP revision process". Resulting errors: "lack of appropriate instruments to conduct the actions specified", "incorrect, unnecessary, or incomplete procedural steps", "references to actions that cannot be accomplished because of environmental conditions or equipment failures", "overly complex procedural steps or misleading logic", "excessive or incorrect transitions". p.3: "Deficiencies in EOPs have also been a factor in unsatisfactory operator performance during requalification examinations." No counts of plants given.
- Bearing: **for C8** (a written writer's guide and a V&V requirement did not ensure their own application), **for C1/C2** (procedures referenced instruments/actions that did not exist or could not be done; i.e. misrepresentation of the plant), and **against "sign-off reliably catches defects"**. NUREG-1358 itself and Supp.1: UNREACHABLE (not fetched).

**D3. NUREG-0711 Rev 3 (2012): ISV requires pre-stated pass/fail criteria with stated basis; validation is by sample.**
- Source: US NRC, NUREG-0711 Rev. 3, *Human Factors Engineering Program Review Model*, Nov 2012. ADAMS ML12324A013.
- TYPE: standard (regulatory review model). ACCESS: full text read (relevant sections).
- Locators: s.9.4 Procedure Development, criterion (6): "Verify that the procedures are correct, and can be carried out by plant personnel. Wherever possible, this should include a walkdown ... on a full-scope simulator, or in the facility itself. Where a walkdown is not possible, a tabletop verification may be used"; "Validate the use of procedures in a simulation of the integrated system"; "When procedures are modified ... verify the adequacy of their content, format, and integration ... validate procedures when a modification substantially changes personnel tasks significant to plant safety." s.11.4.3.5: "Pass/fail measures are those used to determine whether the design is or is not validated. Diagnostic measures are used to better understand personnel performance"; s.11.4.3.5.1 (4): "The applicant should identify the specific criterion for each measure used to judge the acceptability of performance and describe its basis"; Table 11-2 bases: Requirement, Benchmark, Norm, Expert Judgment; (5) identify whether each measure is pass/fail or diagnostic. s.11 intro: reviews "can involve hundreds or thousands of individual HSIs, and it is impractical and unnecessary to review all of them. Therefore, the applicant can employ a sampling strategy".
- Bearing: **against C4 as worded**: an explicit, pre-stated acceptance criterion requirement exists for validating procedures (as part of the integrated system), including re-validation triggered by change (a change-triggered re-check: bears on C2). Limits: criteria are on scenario performance over a sample of operating conditions, not on the text's claims exhaustively; "Expert Judgment" is an allowed criterion basis.

**D4. Practitioner account of an EOP integrated system validation with pre-established acceptance criteria.**
- Source: Moyano de las Heras N, Arroyo Zapata A, Hervás Martín FB (Tecnatom). "Experiences in Systematic Approach to Procedures Validation in Simulator." NENE 2021, Bled, paper 501. https://www.djs.si/nene2021/proceedings/pdf/NENE2021_501.pdf
- TYPE: practitioner report. ACCESS: full text read.
- Locators: s.4: "the specific acceptance criteria for the results of the Integrates System Validation activity were established as follows": plant parameters stable/trending as expected; procedures reach final status "in a reasonable sequence and time, according to the Operation Sequence Diagrams"; new-equipment actions performed correctly; "Time Critical and Time Sensitive Actions ... performed in less time than the prescribed time". s.5: "The Review and Analysis activities resulted in several comments ... Most of them were accepted and implemented"; ISV "results ... were positive as the pre-established acceptance criteria for each scenario were met". No counts of discrepancies given; 20 EOPs reviewed.
- Bearing: shows the criterion in use (against C4 in this field); also shows criteria mix measured (times) and judged ("reasonable sequence"). No evidence on whether ISV misses defects.

### E. Aviation checklists: approval without design criteria; checklist presence does not ensure use

**E1. Degani & Wiener, NASA CR-177549 (1990).**
- Source: Degani A, Wiener EL. *Human Factors of Flight-Deck Checklists: The Normal Checklist*. NASA Contractor Report 177549 (NTRS 19910017830). https://ntrs.nasa.gov/api/citations/19910017830/downloads/19910017830.pdf
- TYPE: review/secondary + field study (interviews, observations, NTSB/ASRS records). ACCESS: full text read.
- Locators: s.1 (p.3): three accidents in 15 months where checklist misuse was a probable cause (Air New Orleans BAe J-31; NW255 MD-80 no-flap/no-slat; Delta 1141 B-727); second author testified "that he did not know of any human factors research on how a checklist should be designed" (NTSB 1988a p.62). s.3.2.2 (pp.22-23): FAR 121.315 "does not comment about the concept, method, type, philosophy, or presentation of the checklist ... It leaves almost all aspects of checklist construction for the airline to design and the POI to approve or disapprove"; for Part 135 "There is no formal approval of checklist changes"; "With the vague and non-specific nature of FAR 121.315, and with no FAA internal guidelines for checklist design criteria, the POI has almost total authority over the approval of the checklist. He or she may approve or dismiss it according to his or her own philosophy". Manufacturer checklist "fine tuning" in flight testing (p.22). s.6.4.4 (p.44): ASRS #58147 "First Officer forgot to read flap setting on pre-takeoff checklist ... he had become a little complacent"; Air New Orleans crew "failed to comply with the BEFORE TAKEOFF checklist".
- Bearing: **for C4** (sign-off by one approver without stated criteria) and **for C8** (a checklist present in the cockpit did not establish its application; accidents attributed to checklist non-use/misuse). Dated (1990); later FAA guidance (AC 120-71 etc.) not read.
- Lead not read: Degani & Wiener, "Cockpit checklists: concepts, design, and use", *Human Factors* 1993;35(2) (NTRS 19930068509, no PDF).

### F. Sign-off and document control as standards

**F1. US device QS regulation 21 CFR 820.40 (text in force to 2 Feb 2026): approval "for adequacy" with no criterion of adequacy.**
- Source: eCFR, 21 CFR 820.40 as of 2024-01-01 (superseded by the QMSR incorporating ISO 13485:2016 from 2 Feb 2026). https://www.ecfr.gov/
- TYPE: standard (regulation). ACCESS: full text read.
- Quote: "designate an individual(s) to review for adequacy and approve prior to issuance all documents ... The approval, including the date and signature ... shall be documented ... all obsolete documents shall be promptly removed from all points of use or otherwise prevented from unintended use." (b) changes reviewed and approved by same function; change records.
- Bearing: **for C4** (the sign-off gate names no acceptance criterion for content; "adequacy" is left to the approver) and shows regulated control of obsolescence (a mechanism against stale text, C2). ISO 9001:2015 cl. 7.5.2/7.5.3 (review and approval "for suitability and adequacy"; control of obsolete documented information): NOT READ (paywalled); wording from memory only, treat as unverified.

**F2. 21 CFR 211.100: drug production procedures must be approved by the QC unit and followed.**
- Source: eCFR 21 CFR 211.100 (2025-01-01). TYPE: standard. ACCESS: full text read.
- Quote: (a) procedures "shall be drafted, reviewed, and approved by the appropriate organizational units and reviewed and approved by the quality control unit"; (b) "shall be followed ... and shall be documented at the time of performance. Any deviation ... shall be recorded and justified."

**F3. FDA FY2024 inspection observations: failure to have/follow written procedures is the most frequent drug citation.**
- Source: FDA, "Inspection Observations", FY2024 spreadsheet (inspections ending 10/1/2023-9/30/2024). https://www.fda.gov/media/185090/download?attachment
- TYPE: practitioner report (regulator's administrative data). ACCESS: full data read.
- Figures (sheet "Drugs", column Frequency): 21 CFR 211.22(d) "Procedures not in writing, fully followed" = 201 (rank 1 of all drug cites; total drug observations 2,483; drug FDA-483s issued 561 per Summary sheet); 211.100(a) "Absence of Written Procedures" = 126 (rank 3); 211.100(b) "SOPs not followed / documented" = 14; 211.166(a) "Written program not followed" = 16. Devices: 820.40 "Procedures not adequately established or maintained" = 32; 820.40(a) "Not approved or obsolete document retrieval" ("Documents that were [not approved] [obsolete] were observed at a location where they [could be] [are being] used") = 2. Summary sheet caveat: not all 483s are in the system.
- Bearing: **for C8**: in a regime where approved written procedures are mandatory, not following them is among the most cited deficiencies. Caveat: 211.22(d) merges "not in writing" and "not fully followed"; cannot be split. Obsolete-document citations are rare in the data, which does not show that document control prevents obsolete use (inspection detects only what inspectors see).

### G. Guideline appraisal and certainty statements

**G1. AGREE appraises development process/reporting, not recommendation validity; reliability needs several raters.**
- Source: Brouwers MC, Kho ME, Browman GP, et al. "Development of the AGREE II, part 1: performance, usefulness and areas for improvement." *CMAJ* 2010;182(10):1045-52. PMC2900328.
- TYPE: first-hand study (instrument development). ACCESS: full text read via fetch-tool extraction only (PMC HTML blocked by captcha; eutils returned front matter only; Europe PMC 500). Treat figures as provisional.
- Extracted: Introduction: AGREE designed to "assess the process of guideline development and reporting"; original 7-point scale: "The number of appraisers required to reach a level of inter-rater reliability of 0.7 ranged from two to five across domains"; Table 3 single-rater ICCs reported as 0.30 (rigour) to 0.57 (applicability), with R up to 6 for rigour (conflicts with the "two to five" sentence; unresolved); "this study was not specifically designed or powered to be a reliability study"; current norm "four independent reviewers".
- Bearing: for C1 (appraisal of a guideline text checks how it was made, not whether what it says is right), and for C4 (single reviewer unreliable).

**G2. Methodological quality and recommendation validity diverge.**
- Source: Watine J, Friedberg B, Nagy E, et al. "Conflict between guideline methodologic quality and recommendation validity: a potential problem for practitioners." *Clin Chem* 2006;52(1):65-72. doi:10.1373/clinchem.2005.056952.
- TYPE: first-hand study. ACCESS: abstract/record only (publisher 403 Cloudflare).
- Abstract (via search extract): 11 NSCLC lab-test guidelines; guidelines "with the best methodologic quality were not necessarily the most valid in their recommendations, and conversely". UNVERIFIED in full text.
- Bearing: if confirmed, strong for C1 (process-based acceptance does not test content).

**G3. GRADE certainty ratings are reproducible with trained raters.**
- Source: Mustafa RA, Santesso N, Brozek J, et al. "The GRADE approach is reproducible in assessing the quality of evidence of quantitative evidence syntheses." *J Clin Epidemiol* 2013;66(7):736-42. doi:10.1016/j.jclinepi.2013.02.004. Repository record: http://repositorio.uchile.cl/handle/2250/123518
- TYPE: first-hand study. ACCESS: abstract/record only (PDF link returned HTML).
- Abstract (via fetch extraction): IRR for two individual raters without GRADE 0.31 (students) and 0.27 (GRADE members); with GRADE 0.66 and 0.72; consensus did not improve reliability.
- Bearing: an explicit certainty statement attached to a text can be assigned reliably; it states confidence in evidence, not the text's fidelity to it (C1 context). Unverified.

### H. Software user documentation standard

**H1. ISO/IEC/IEEE 26513:2017, Requirements for testers and reviewers of information for users.**
- Source: ISO/IEC/IEEE 26513:2017 (preview: https://www.vde-verlag.de/iec-normen/preview-pdf/info_isoiecieee26513%7Bed1.0%7Den.pdf).
- TYPE: standard. ACCESS: preview only (scope, TOC); body not read.
- Scope s.1: "specifies processes for use in testing and reviewing of user documentation"; "provides the minimum requirements for testing and reviewing user documentation (Clause 7)"; "usability testing of the documentation is likely to identify additional operational concerns or misunderstandings of end users." TOC: 6.4 "Documentation evaluation criteria", 7.3 "System test of documentation", 7.4.3 "Measures and metrics for documentation usability testing goals", 7.2 "Configuration change review". Whether it sets numeric acceptance criteria: NOT KNOWN.

## 3. Mechanisms

| mechanism | failure kind it signals | what it detects | what it misses | cost | evidence | agents measured? |
|---|---|---|---|---|---|---|
| Performance-based user testing with per-question criterion (EU PIL, 16/20) | misread; text unusable for reader | key facts not found/understood by target readers; navigation failures | content correctness; facts not chosen as questions; later regulator edits; translations; legacy texts | ~20-50 interviews, 45 min each, iterative rounds | A1, A3, A4, A5 | n |
| Expert/ethics committee sign-off | any, by judgment | what reviewers notice | reader-failure defects (A3); low agreement among experts (B1) | low | A3, B1, F1 | n |
| Plus-minus / reader protocol pretest | misread; missing information | many reader-perceived problems (~150 per text, B3) | which to act on; correctness | moderate | B1, B3 | n |
| Usability sample-size rule (5/10/20 users) | misread / unusable | share of problems discoverable by the full sample | low-probability problems; problems outside tested tasks | per-user sessions | B4 | n |
| Capture-recapture over independent inspectors | misrepresentation/defects detectable by reviewers | estimate of remaining detectable defects -> stop/reinspect | defects no reviewer can detect; underestimates; needs >=3-4 inspectors | multiple independent reviews | C1-cr | n |
| EOP verification (desk/tabletop vs writer's guide, technical guidelines) | misrepresentation of guidelines; format | deviations from technical basis and writer's guide | whether actions are physically possible; usability under stress | moderate | D1, D3 | n |
| EOP walk-through in plant/control room | text vs world mismatch (dependency) | referenced instruments/controls missing, mislabelled, inaccessible | dynamic scenarios | moderate-high | D1 (objective d), D2 | n |
| Simulator validation / ISV with pass/fail criteria | instruction fails to produce intended outcome | timing, flowpath, omissions, workload on sampled scenarios | unsampled conditions; criteria based on expert judgment | high (crews, simulator) | D1, D3, D4 | n |
| Change-triggered re-verification/re-validation | validity loss on change | modified procedures (NUREG-0711 9.4(6)) | changes not recognised as substantial; PIL post-test edits (A5) | per change | D3, A5 | n |
| Document control (approval, obsolete removal) | stale text in use | unapproved/obsolete copies found at point of use | content adequacy; whether text is followed | low-moderate | F1, F3 | n |
| Process appraisal (AGREE II) | weak development process | reporting/process gaps | recommendation validity (G2, unverified) | 2-4 appraisers | G1, G2 | n |
| Certainty grading (GRADE) | overstated confidence | confidence in body of evidence, reliably between trained raters | whether text reflects that evidence | trained raters | G3 | n |

No source in this track measured AI agents using any of these mechanisms.

## 4. Disconfirming searches and results

- Sought: fields where an explicit acceptance criterion for a text exists and is measured to work. Found: EU PIL 16/20 per-question criterion (A1) with RCT evidence that criterion-guided revision improves comprehension in an independent sample (A3); NUREG-0711 pass/fail criteria with stated bases for procedure validation (D3) and a practitioner ISV applying them (D4). Conclusion: C4's "without acceptance criteria stated for a text" describes most fields but not these; in these, the criterion is stated, though it covers a chosen question/scenario sample, not the whole text.
- Sought: a stopping rule for review. Found: capture-recapture estimation for inspections of natural-language requirements documents (C1-cr), and sample-size rules for usability testing (B4). Both bound only what the reviewers/testers could detect and show wide error at small n. Conclusion: C4 should be reworded rather than kept absolute.
- Sought: evidence that sign-off/review reliably catch defects. Found the opposite: ethics-approved sheets failed user tests (A3); technical writers predicted little of reader feedback (B1, abstract); NRC inspections found inadequate V&V and writer's-guide implementation at many plants (D2); checklist approval by a single inspector without criteria (E1). No positive evidence found.
- Sought: evidence that a passed user test means real-world comprehension. Found only weak evidence: the effect of the 2005 requirement "barely recognisable" in one German study (A5, secondary); EC study says comprehension "can be improved". No study found linking the 16/20 pass to real-use outcomes. Gap.
- Sought: origin and critique of the 90%/90% criterion (Sless/Australian CMI). Search returned nothing relevant. Unresolved.
- Sought: evidence that document control prevents use of obsolete documents. Found only FDA citation counts (obsolete-at-point-of-use cited twice in FY2024 device data), which cannot show prevention. Not established either way.

## 5. Fields/terms the brief missed

- "Performance-based readability testing", "user testing" / "readability user testing", "bridging" (EU PILs: reuse of a tested leaflet's results for similar leaflets; not read here, Norwegian agency page as lead), "consultation with target patient groups".
- "Diagnostic vs pass/fail measures", "Integrated System Validation (ISV)", "sampling of operational conditions", "task support verification", "Procedures Generation Package", "writer's guide" (nuclear HFE).
- "Capture-recapture" / "defect content estimation" / "reinspection decision" (software inspection).
- "Problem discovery rate", "five-user assumption" (usability sample-size).
- "Formative text evaluation", "plus-minus method", "reader-focused vs expert-focused evaluation" (document design, Dutch school: de Jong, Lentz, Schellens, Pander Maat).
- "Document control", "obsolete documents at point of use", FDA "Form 483 observations" as administrative data on procedure non-adherence.
- "Recommendation validity" vs "methodologic quality" (guideline appraisal).

## 6. Thin or contested points; unreachable sources

- Unreachable full texts: de Jong & Schellens 2000 (IEEE TPC; closed), de Jong & Lentz 1996 (JTWC), Watine et al. 2006 (Clin Chem, Cloudflare 403), Mustafa et al. 2013 GRADE IRR (repository PDF link returned HTML), NUREG-1358 and its Supplement 1 (not fetched), Degani & Wiener 1993 Human Factors paper, Fuchs 2010 Drug Inf J, Beime & Menges 2012, Petersson et al. 2004 JSS, Pander Maat & Lentz 2010 (PEC), ISO 9001:2015 and ISO/IEC/IEEE 26513 bodies, Sless (not found).
- AGREE (G1) figures came through a fetch-tool extraction with an internal inconsistency (2-5 vs 6 raters); verify before citing numbers.
- Briand et al. (C1-cr): numbers unrecoverable from the character-shifted PDF; only qualitative conclusions reported.
- PIL criterion: guideline Annex is "illustrative"; national agencies apply it flexibly (MHRA, Norway per search extracts, not read). Arithmetic 90%x90%=81% vs 16/20=80%.
- Evidence that user testing improves real-world outcomes (not test comprehension) is thin; strongest controlled study (A3) is by authors with a commercial interest in user testing (declared).
- FDA 211.22(d) count merges "not in writing" with "not fully followed".
- NUREG-0899 status statement ("compliance will not be required") seen only in a search extract of the INL copy; not verified.
