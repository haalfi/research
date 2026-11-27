# Track t03: how health and science track whether a text is still valid after what it depends on changed

Scope: brief questions 1, 3, 4 and 5; claims C1, C2 and C7. The fields are clinical guidelines, systematic reviews (SRs) and living SRs (LSRs), retraction and correction propagation, drug labels, and clinical decision support (CDS) knowledge bases.

ACCESS labels:
- "full text (XML)": the Europe PMC/PMC full-text XML was converted to text and grepped, and the quotes were checked against it.
- "full text (fetch)": the page was read through the fetch tool, which returns model-extracted quotes. Those quotes are faithful as far as can be checked, but they were not grepped by me.

## 1. Scope and searches run

Europe PMC REST title searches (`TITLE:"..."`) for:
- how quickly guidelines become outdated; how quickly SRs go out of date; when and how to update SRs; LSRs (emerging opportunity / feasibility and acceptability / scoping review / methodological survey); living guidelines;
- guidance for updating CPGs; when guidelines should be updated; durability of class I recommendations; "Investing in updating" (Cochrane); surveillance system for updating SRs; time-to-update of SRs;
- citation distortions; impact of papers from retracted research; continued use of retracted papers; post-retraction citations in context; RISRS; self-correction (effect of retraction); retraction after misconduct and citations; impact of retraction on RCT citation; trial retractions and the evidence ecosystem (VITALITY); residue of retractions; inclusion of retracted studies in SRs; retracted RCTs in SRs and CPGs;
- Zotero and retracted items; persistence of error; correction and republication; errata for trial publications; contradicted and initially stronger effects; persistence of contradicted claims; medical reversals;
- CDS malfunctions; consistency of safety labeling of bioequivalent drugs; generic or SmPC label discrepancies (no hits); outdated guidelines and LLMs; retraction and ChatGPT/LLMs.

Web searches:
- "effect of Zotero retraction alert Retraction Watch integration on post-retraction citations measured study" (extended)
- "citing articles reflect errata corrections propagation" (extended)
- "Thelwall ChatGPT retracted articles"
- "NICE surveillance process guide"

Also an arXiv API query: retracted AND "language models".

Direct fetches:
- NICE PMG20 ch. 13 and PMG49 chapters (aims, overview, surveillance reviews)
- the White Rose repository PDF of Thelwall et al. 2025

Blocked:
- NCBI Bookshelf (reCAPTCHA): the AHRQ technical review by Shojania et al. 2007
- the PMC HTML/PDF and Europe PMC PDF render (Cloudflare/reCAPTCHA via curl); the fetch tool worked on PMC HTML
- the CMAJ XML (publisher disallows it)

## 2. Findings

### A. Clinical guidelines: how fast they go stale and how they are tracked

**F1. AHRQ guidelines went out of date while still in circulation.**
- Claim: of 17 AHRQ guidelines, 7 needed a major update, 6 a minor one, 3 were still valid and 1 was undetermined. "about half the guidelines were outdated in 5.8 years (95% CI 5.0-6.6)"; "no more than 90% … still valid" at 3.6 years. The validity check was a one-off research exercise: a survey of panel members (n=170, 71% response) plus literature searches.
- Source: Shekelle PG et al. 2001, "Validity of the AHRQ clinical practice guidelines: how quickly do guidelines become outdated?", JAMA 286:1461. doi:10.1001/jama.286.12.1461
- TYPE: first-hand study. ACCESS: abstract/record only (Europe PMC). The full text is paywalled; not verified.
- Locator: abstract Results. It also says "No published methods are available for assessing whether existing practice guidelines are still valid".
- Bearing: C2 for. The texts stayed in circulation without signal. The study found no routine check that can fail (C1 for, as of 2001).

**F2. Shekelle's update model rests on expert awareness.**
- Claim: the commonest advice was "a scheduled review date"; some guidelines say they will be updated "when new information becomes available". The model proposed rests on the premise that "evidence sufficient to invalidate an existing guideline would, in general, be known to experts in the field". Future steps include "electronic formats that permit excision of outdated recommendations" and clinician feedback. No empirical survival data are in this paper.
- Source: Shekelle P, Eccles MP, Grimshaw JM, Woolf SH 2001, "When should clinical guidelines be updated?", BMJ 323:155. PMC1120790
- TYPE: practitioner report/methods proposal. ACCESS: full text (fetch). The XML is not available; the page is scanned.
- Bearing: Q3. The mechanism is time-based expiry plus expert polling. Its premise (experts know) is an assumption, not tested here.

**F3. About 1 in 5 recommendations was out of date after 3 years (Spanish guidelines).**
- Claim: 113 recommendations from 4 Spanish guidelines. 25 (22.1%) needed updating, linked to 69 key references. Survival was 92.0% at 1 year, 85.7% at 2, 81.3% at 3 and 77.8% at 4. "High-turnover" recommendations (many linked references) were more likely to need updating (18/25). Topic, strength and clinical purpose were not predictive. The authors suggest surveillance every 6–12 months; review at more than 3 years is "potentially too long".
- Source: Martínez García L et al. 2014, "The validity of recommendations from clinical guidelines: a survival analysis", CMAJ 2014. PMC4216254
- TYPE: first-hand study. ACCESS: full text (fetch; the publisher bars XML).
- Locator: Results, "Survival analysis" and "Assessment of recommendations"; Interpretation.
- Bearing: C2 for, with measured staleness. The disconfirming side: 77.8% remained valid at 4 years.

**F4. Class I ACC/AHA recommendations mostly survived; omissions went unexplained.**
- Claim: of 619 class I recommendations in 11 guidelines, 80.0% were retained in the next version, 9.2% downgraded or reversed and 10.8% omitted. The median gap to the next full revision was 6 years (range 4–10). Retention was 90.5% for evidence level A, 81.0% for B and 73.7% for C. "Guideline texts rarely stated the reasons for these omissions". "Prior to 2008, ACC/AHA guidelines did not routinely map individual recommendations to references in the medical literature."
- Source: Neuman MD, Goldstein JN, Cirullo MA, Schwartz JS 2014, "Durability of class I ACC/AHA clinical practice guideline recommendations", JAMA 311:2092. PMC4346183 (author manuscript)
- TYPE: first-hand study. ACCESS: full text (XML).
- Locator: Abstract Results; Results paragraphs 1–3; Discussion paragraphs on omissions and LOE.
- Bearing:
  - Disconfirming for "stale = harmful": 80% retained and <1% reversed.
  - C2 for: silent omission (no reason recorded), and no recommendation-to-evidence links. A dependency map, the precondition for change-triggered checks, was absent before 2008.
  - C5: no record of reasons.

**F5. Guideline handbooks barely describe updating.**
- Claim: 35 guideline handbooks were reviewed. Guidance on identifying new evidence: 31.4%. Guidance on assessing the need for an update: 22.8%. A time frame between updates: 71.4%, most often 2–3 years (40.0%). Five (14.3%) say how to indicate changes in the update; 2 (5.7%) say to post a website notice when an update is needed. "Overall the updating guidance is poorly described." 62.9% include a fixed 2–5 year time frame.
- Source: Vernooij RW, Sanabria AJ, Solà I, Alonso-Coello P, Martínez García L 2014, "Guidance for updating clinical practice guidelines: a systematic review of methodological handbooks", Implement Sci 9:3. PMC3904688
- TYPE: review/secondary (of standards). ACCESS: full text (XML).
- Locator: Abstract; Results "Time between updates", "Assessment of the need for an update"; Discussion.
- Bearing: C1 for. The dominant mechanism is a calendar, not a check that can fail. Q5: the update criteria are mostly unspecified.

**F6. NICE replaced fixed review points with capacity-limited, monitoring-driven reviews.**
- Claim: NICE-wide surveillance (PMG49, 23 Oct 2025) assesses "the impact of new evidence, changes to the health and care system, or other new, relevant information" after guidance is published. Reviews are reactive, triggered by "information identified through monitoring" and carried out "Subject to constraints on capacity", or planned when evidence is uncertain and research is underway. Outcomes include update, amend, retire, incorporate, track, plan a future review or "no further action". A surveillance report records the reasons.
- Source: NICE 2025, "Processes and methods for NICE-wide guidance surveillance" (PMG49), https://www.nice.org.uk/process/pmg49/chapter/surveillance-reviews
- TYPE: standard. ACCESS: full text read for 3 chapters only (the monitoring chapter was not read). An older PMG16 static list with 5-year re-checks is known only from a search snippet and is not verified.
- Bearing:
  - Q3: the mechanism is event-driven, it records a decision and its reasons, and retirement is an explicit outcome.
  - C5: the owner's capacity limits it, and the standard says so explicitly.
  - No effectiveness data were found.

### B. Systematic reviews: obsolescence, update signals and whether signals lead to action

**F7. Signals for updating were frequent and sometimes present at publication.**
- Claim: 100 SRs (1995–2005).
- Signal definitions: a quantitative signal is a change in significance, or a relative change in effect of at least 50%, on a primary or mortality outcome. A qualitative signal covers new harms, changed characterisations, or caveats.
- 57% had a signal. Median survival free of a signal was 5.5 years (95% CI 4.6–7.6). A signal occurred within 2 years for 23%, within 1 year for 15%, and "In 7%, a signal had already occurred at the time of publication."
- Shorter survival went with cardiovascular topics (HR 2.70) and with heterogeneity (HR 2.15).
- Source: Shojania KG et al. 2007, "How quickly do systematic reviews go out of date? A survival analysis", Ann Intern Med 147:224. doi:10.7326/0003-4819-147-4-200708210-00179
- TYPE: first-hand study. ACCESS: abstract/record only (Europe PMC). The AHRQ technical review is on NCBI Bookshelf, which blocked access (reCAPTCHA).
- Bearing:
  - C2 for: texts were invalid on arrival, without signal.
  - Q3: this is the most explicit failable "staleness signal" definition in the field. Limitation per the abstract: "Judgments … made without involving content experts".

**F8. Only 9% of updated Cochrane reviews changed conclusion; predictors were known only after updating.**
- Claim: cohort of Cochrane reviews 1998→2002, n=362. 70% were updated (38% with new studies, 32% with re-run searches but no new studies) and 30% were not updated at all. "Of the 254 updated reviews … only 23 (9%) had a changed conclusion." Predictors of change (narrower CI, change in significance) "are of limited value in predicting which reviews should be updated, since they are only known after the update has taken place." Cited prior work: Koch found 68% of 1268 reviews gave no date for new studies or for changes to conclusions. Bastian & Doust found that for reviews tagged 'updated' "it was often difficult to identify what had changed".
- Source: French SD, McDonald S, McKenzie JE, Green SE 2005, "Investing in updating: how do conclusions change when Cochrane systematic reviews are updated?", BMC Med Res Methodol 5:33. PMC1274326
- TYPE: first-hand study. ACCESS: full text (XML).
- Locator: Abstract Results; Results paragraph 2; Discussion paragraphs 2 and 4; Background paragraph 4.
- Bearing:
  - Strongest disconfirming evidence on cost: most updates change nothing.
  - Supports C2: no ex-ante signal separates the 9%.
  - Also shows the "updated" flag itself is a weak signal: it does not say what changed.

**F9. Cochrane reviews were not updated faster when new evidence appeared.**
- Claim: of 682 Cochrane SRs from 2010, 43% were updated by June 2017. Median update time was 35.4 months; 38% of updates added new trials; 4% (8/204) changed conclusion. There was no clear difference in update timing with a publication signal (25.3 vs 34.4 months, p=0.05) or a trial-completion signal (26.0 vs 32.4, p=0.33). Reviews whose conclusions changed took longer (48.4 vs 32.7 months, p=0.04).
- Source: Bashir R, Surian D, Dunn AG 2018, "Time-to-update of systematic reviews relative to the availability of new evidence", Syst Rev 7:195. PMC6240262
- TYPE: first-hand study. ACCESS: full text (XML).
- Locator: Abstract; Results paragraphs on Fig 4.
- Bearing:
  - C2 and C1 for: even where a signal existed, it did not drive action. Detection did not lead to resolution (C5).
  - Disconfirming on the cost side: 4% changed conclusion.

**F10. AHRQ's SR surveillance system works but has not been validated.**
- Claim: 24 AHRQ SRs were surveilled every 6 months using Ottawa/RAND signals, expert polling and safety alerts. 2 (8%) were rated high priority, 5 (21%) medium and 17 (71%) low. "Neither the STL nor the number of new relevant articles was perfectly associated with a signal". Expert response had a median of 35% in round 1. The system "requires subjective global judgments". The authors call for "validating the surveillance methods against the gold standard of actual review updates in a blinded fashion".
- Source: Ahmadzai N et al. 2013, "A surveillance system to assess the need for updating systematic reviews", Syst Rev 2:104. PMC3874670
- TYPE: first-hand study (operational evaluation). ACCESS: full text (XML).
- Locator: Abstract; Results (expert response); Discussion (limitations, future research).
- Bearing: Q3. A failable signal exists, but its accuracy is unmeasured and it rests on judgment. Against any claim that the problem is "solved".

**F11. Consensus guidance: update decisions are judgments; only partial methods have been checked.**
- Claim: "Mechanical rules appear unworkable". Decisions to update "are judgments made for individual reviews at a particular time". Cochrane moved from updating on new evidence, to every two years, to updating "based on need and priority". The panel proposes standard "update status" terms with a rationale, and says authors "need to report the differences in findings between the original and updated edition". Table 1, Ottawa method: "Will not detect all trials", with "Approach validated for consistency of predicted and actual changes to conclusions; reasonable agreement with RAND method". Table 3 lists Crossref threaded publications linking trials to derivative reviews as "operational".
- Source: Garner P et al. 2016, "When and how to update systematic reviews: consensus and checklist", BMJ 354:i3507. PMC4955793
- TYPE: standard/consensus. ACCESS: full text (XML).
- Locator: Introduction; Summary points; Table 1; "Reporting changes"; Table 3; Concluding remarks.
- Bearing:
  - Q3 and Q5: the update status record is a recorded decision.
  - Disconfirming: the Ottawa method has some validation of predicted against actual conclusion change, so it is a weak but real check that can fail.
  - C1 partly against in this field: checks exist but are acknowledged as incomplete.

### C. Living systematic reviews

**F12. Cochrane's LSR pilots were feasible but workload was the main concern.**
- Claim: 6 pilot LSRs searched monthly to three-monthly. Authors screened 3 to 300 citations per month and spent between 5 minutes and 32 hours per month. Managing editors spent 0 to 3.5 hours and information specialists 30 minutes to 6 hours per month. Main concerns were "managing the ongoing workload"; for example, "Even if eligible studies are not identified the PRISMA still needs to be updated." Copy-editing showed "Dangers of inconsistency … with the potential for copy-editors to rush".
- Source: Millard T et al. 2019, "Feasibility and acceptability of living systematic reviews: results from a mixed-methods evaluation", Syst Rev 8:325. PMC6911272
- TYPE: first-hand study (mixed methods). ACCESS: full text (XML).
- Locator: Abstract; Results "Review progress and workload" (Table 2); Challenges.
- Bearing:
  - Q3: the cost of continuous currency, measured.
  - C6/C2: rushing creates new inconsistency.

**F13. LSRs lag their planned updates and none declared retirement.**
- Claim: 76 LSRs with 279 versions (to April 2021), median 2 versions. The ratio of actual to planned update period had a median of 1.12. 8 of 19 (42%) had gone more than 3× their planned period since the last version. "No LSR included a 'retirement notice' in their latest published version."
- Source: Akl EA et al. 2023, "The life and death of living systematic reviews: a methodological survey", J Clin Epidemiol. doi:10.1016/j.jclinepi.2023.02.005
- TYPE: first-hand study. ACCESS: abstract/record only.
- Bearing: C2 for. A "living" label can itself become a stale claim, and no LSR signalled that it had stopped. The 2025 follow-up (Nevill et al., J Clin Epidemiol, doi:10.1016/j.jclinepi.2025.111904, abstract only) found 168 LSRs, with updating "frequencies and/or triggers" varying widely.

**F14. The LSR proposal argues prioritised updating cannot keep SRs current.**
- Claim: conventional prioritised updating "cannot adequately reduce the inaccuracy caused by out-of-date SRs". Living SRs keep a continuous search running and use version numbers and dates. When a search finds nothing new, "the review can be updated with the date of last search without further review".
- Source: Elliott JH et al. 2014, "Living systematic reviews: an emerging opportunity to narrow the evidence-practice gap", PLoS Med 11:e1001603. PMC3928029
- TYPE: practitioner report/position. ACCESS: full text (XML).
- Bearing: Q3. The design is a dated "still current as of" assertion, which is a check that can fail because a search either does or does not find new studies.

### D. Retraction and correction propagation (C7, Q4)

**F15. Retracted trials distorted guidelines and reviews, and reassessment was rare.**
- Claim: 12 trial reports (later retracted for misconduct) were cited in 1158 publications, including 68 SRs, guidelines and trials. 13 would likely change their findings without them, and 8 were unclear. "By 2018, only one of the 68 citing publications … appeared to have undertaken a reassessment". As of July 2019, only 7 of 12 (58%) were marked retracted on both Ovid Medline and PubMed. 34 of 40 (85%) post-retraction citing publications "expressed no concern". An AHRQ review's four affected reports were "the sole sources of data" for one bisphosphonate claim, and the linked ACP guideline cites them. Concerns had been raised in 2004–2007, but retractions came in 2016–2019. Recommendations include automatic alerts to authors of citing publications, and guideline groups checking Retraction Watch against their reference lists.
- Source: Avenell A, Stewart F, Grey A, Gamble G, Bolland M 2019, "An investigation into the impact and implications of published papers from retracted research: systematic search of affected literature", BMJ Open 9:e031909. PMC6830710
- TYPE: first-hand study. ACCESS: full text (XML).
- Locator: Abstract; Results (first paragraph, the post-retraction citation paragraph, "Effectiveness reviews and guidelines"); Discussion box of recommendations.
- Bearing: C7 strong for: an invalid premise propagates into guidelines. C2: the change at the source gave no signal to dependents. C5: correction is "slow, uncoordinated and inconsistent".

**F16. Retracted trials contaminated thousands of meta-analyses and over 150 guidelines.**
- Claim: 1330 retracted RCTs led to 847 SRs with 3902 replicable meta-analyses. Excluding the retracted trials changed:
  - the direction of effect in 8.4% (95% CI 6.8–10.1)
  - significance in 16.0%
  - both in 3.9%
  - either in 20.6%
  - magnitude by more than 50% in 15.7%

  218 substantially affected meta-analyses (68 SRs) fed into 157 guideline documents. "almost 40% of the reviews included retracted trials after the retraction". The authors also say "Most the systematic reviews that synthesised retracted trials did not make a correction". The burden of later checks "would have to fall on the users". The median time from concern to first journal correction was 22.1 months (cited). Tools named: REAPPRAISE, CPC-TST, TRACT, INSPECT-SR, SpiderCite and retracted.net.
- Source: Xu C et al. 2025, "Investigating the impact of trial retractions on the healthcare evidence ecosystem (VITALITY Study I): retrospective cohort study", BMJ 389:e082068. PMC12015725
- TYPE: first-hand study. ACCESS: full text (XML).
- Locator: Abstract Results; Results "Contaminated evidence in clinical practice guidelines"; Discussion paragraphs 1, 3 and 5.
- Bearing:
  - C7 strongest quantified for.
  - Disconfirming nuance: about 79% of meta-analyses changed neither direction nor significance (the complement of 20.6%, my arithmetic).

**F17. Most meta-analyses survived removal of retracted studies, but SRs were rarely corrected.**
- Claim: 61 SRs in the 25 top general medical journals (2013–2024) included retracted studies. Retraction came after the SR was published in 37 of 50 (74%). 160 of 166 (96%) recalculated estimates stayed within the original CI. Significance changed in 18 (11%). For primary outcomes, estimates moved by at least 50% in 12 of 64 (19%). 11 of 61 (18%) SRs had been republished, retracted or withdrawn. Only one SR mentioned searching Retraction Watch. The detection tool (Feet of Clay Detector) does not scan supplements.
- Source: Graña Possamai C et al. 2025, "Inclusion of retracted studies in systematic reviews and meta-analyses of interventions", JAMA Intern Med. PMC11959482
- TYPE: first-hand study. ACCESS: abstract (Europe PMC) and full text (fetch).
- Bearing: disconfirming. Most pooled estimates are robust. It also shows that a detector for retracted references exists, a check that can fail.

**F18. Most SRs and guidelines citing retracted RCTs were never corrected.**
- Claim: 587 citing documents (525 SRs, 62 CPGs), of which 43% were published after the retraction. "Among 127 articles published citing already retracted RCTs in their evidence synthesis without caution, none corrected themselves". Of those that included later-retracted RCTs, 5% of SRs (9/196) and 5% of CPGs (2/43) corrected or retracted.
- Source: Kataoka Y et al. 2022, "Retracted randomized controlled trials were cited and not corrected in systematic reviews and clinical practice guidelines", J Clin Epidemiol. doi:10.1016/j.jclinepi.2022.06.015
- TYPE: first-hand study. ACCESS: abstract/record only. A medRxiv preprint exists (10.1101/2022.01.30.22270124) but was not read.
- Bearing: C7 and C2 for.

**F19. Only 5.4% of post-retraction citations acknowledged the retraction.**
- Claim: 7,813 PubMed retracted papers; 13,252 post-retraction citation contexts, of which "only 722 (5.4%) … acknowledged the retraction". "retraction did not change the way the retracted papers were cited". Prior studies are summarised in Table 1: van der Vet & Nijveen 3.5%; Schneider et al. 2020 5/112 (4.5%); Budd et al. 2016 4.15%.
- Source: Hsiao T-K, Schneider J 2021, "Continued use of retracted papers: temporal trends in citations and (lack of) awareness of retractions shown in citation contexts in biomedicine", Quant Sci Stud 2(4):1144. PMC9520488
- TYPE: first-hand study. ACCESS: full text (XML).
- Locator: Abstract; Introduction paragraph 4; Section 3.2 / Table 4.
- Bearing: C7 and C2 for. The Schneider et al. 2020 single-paper case is known only through this secondary report.

**F20. Post-retraction citations were mostly positive, not perfunctory.**
- Claim: of 238 post-retraction citations to 15 retracted Elsevier articles, "198 (83%) were positive, 28 neutral (12%) and only 12 (5%) negative". This held even though each article carried a "clear retraction notice". Retracted papers are "almost never flagged" in reference lists.
- Source: Bar-Ilan J, Halevi G 2017, "Post retraction citations in context: a case study", Scientometrics 113:547. PMC5629243
- TYPE: first-hand study (small sample, selected cases). ACCESS: full text (XML).
- Locator: Abstract; Discussion paragraph 1.
- Bearing: directly against the disconfirming hypothesis that post-retraction citations are mostly negative. C7 for.

**F21. Retraction reduces citations by more than half against matched controls, but does not stop them.**
- Claim: retracted papers had a mean of 4.85 citations a year before retraction and 1.93 after. Same-journal, same-year controls went from 3.88 to 4.73, so about 2.8 citations a year were lost. Retraction cut "citations down to less than half"; "retractions decrease citations, but do not eliminate them".
- Source: Kühberger A, Streit D, Scherndl T 2022, "Self-correction in science: the effect of retraction on the frequency of citations", PLoS One 17:e0277814. PMC9728909
- TYPE: first-hand study (matched controls, about 3,240 controls). ACCESS: full text (XML).
- Locator: Results paragraph 1; Discussion paragraph 1.
- Bearing: Q3. A retraction notice is a signal with a measured, partial effect.

**F22. Retraction cut RCT citations by about 23% immediately.**
- Claim: interrupted time series of 218 retracted RCTs. Citations fell 22.9% (95% CI 4.0–38.2) in the month after retraction, then a further 1.9% a month, with no change in matched controls. Authors with many retractions saw a 48.2% drop.
- Source: Mott A, Fairhurst C, Torgerson D 2019, "Assessing the impact of retraction on the citation of randomized controlled trial reports: an interrupted time-series analysis", J Health Serv Res Policy. doi:10.1177/1355819618797965
- TYPE: first-hand study. ACCESS: abstract/record only.
- Note: Avenell 2019 cites Mott as "46% reduction … in the first year". The abstract gives 22.9% plus 1.9% a month. These may be consistent cumulatively (inference), but the 46% figure is not in the abstract.

**F23. A pre-post study without controls found no long-term effect of retraction.**
- Claim: 304 misconduct retractions. Median citations were 2 before retraction and 2 in an equivalent post period, rising to 4 over the total post period. The authors conclude "no association on citations in the long term". Q1-journal papers and highly cited papers dipped first.
- Source: Candal-Pedreira C et al. 2020, "Does retraction after misconduct have an impact on citations? A pre-post study", BMJ Glob Health 5:e003719. PMC7668300
- TYPE: first-hand study (no control group). ACCESS: full text (XML).
- Locator: Abstract; Results Table 2 text.
- Bearing: contested against F21 and F22. The design difference (no matched controls) probably explains the conflict (inference).

**F24. Retraction status is displayed inconsistently; reference-manager flags exist but are unmeasured.**
- Claim: "Many retracted papers are not marked as retracted on publisher and aggregator sites". 75% of retracted papers were in Mendeley libraries (2012). "non-watermarked retracted articles are more cited than watermarked ones". Zotero has flagged retractions since June 2019, Papers since September 2021 and EndNote since November 2021, all using Retraction Watch data. "there are no industry-wide standards for retraction information or its visibility". The authors also say "It is unknown how many publishers systematically surveil bibliographies of submitted manuscripts". Open research questions include whether "retraction metadata … fails to propagate". Next step: NISO CORREC.
- Source: Schneider J, Woods ND, Proescholdt R, RISRS Team 2022, "Reducing the Inadvertent Spread of Retracted Science: recommendations from the RISRS report", Res Integr Peer Rev 7:6. PMC9483880
- TYPE: review/secondary plus a stakeholder consensus. ACCESS: full text (XML).
- Locator: Background paragraphs 3–4; Recommendation 1; Conclusions.
- Bearing:
  - Q3: these mechanisms exist, but no effect measurement of the reference-manager flags is reported.
  - The watermark claim cites Mena et al. 2019 (BJU Int), which I did not read.

**F25. Retracted articles persist on the open web and in personal libraries.**
- Claim: of 1,779 retracted articles, 289 (16.2%) were on non-publisher sites, as 321 copies. "Just 15 (5%) full-article views included a retraction statement." 1,340 (75%) were in Mendeley libraries. The Results give 16 rather than 15; the abstract and Results disagree.
- Source: Davis PM 2012, "The persistence of error: a study of retracted articles on the Internet and in personal libraries", J Med Libr Assoc 100:184. PMC3411255
- TYPE: first-hand study. ACCESS: full text (fetch).
- Bearing: C2 and C6 for. Divergent copies carry no signal.

**F26. Corrected republications were barely preferred over flawed originals for years.**
- Claim: 48 flawed/corrected pairs with 1,064 citations. "53% of post-republication citations … to the republished version, 47% to the original". The difference "does not approach statistical significance until eight to twelve years". MEDLINE linked the corrected version for 33 of 48 (69%) and Web of Science for 2 of 48 (4%). The author calls correction "a marginally effective biblioremediative practice".
- Source: Peterson GM 2010, "The effectiveness of the practice of correction and republication in the biomedical literature", J Med Libr Assoc 98(2). PMC2859270
- TYPE: first-hand study. ACCESS: full text (fetch) and abstract.
- Bearing: corrections do not propagate (brief lead "errata"). C2 and C7 for.

**F27. Errata for trials in drug reviews were often non-trivial and hard to find.**
- Claim: 127 trial articles in 40 CADTH drug SRs had 26 errata describing 38 errors: 6 major, 20 minor and 12 trivial. "No one database contained all the errata." The mean lag was 211 days (range 15–1,036). "Over one-third (9/24) of online articles were uncorrected after errata publication." Cited prior work: "major errors are propagated in other publications, albeit at a lower rate, even after errata have been issued".
- Source: Farrah K, Rabb D 2019, "Errata for trial publications are not uncommon, are frequently not trivial, and can be challenging to access: a retrospective review", J Med Libr Assoc 107:187. PMC6466495
- TYPE: first-hand study. ACCESS: full text (XML).
- Locator: Abstract; Introduction paragraph 1.
- Bearing: C2 for. Even the source text is not updated in 1/3 of cases.

**F28. Citation distortion turned a hypothesis into accepted fact.**
- Claim: in a claim-specific citation network (242 papers, 675 citations, 220,553 supportive citation paths), "supportive papers received 94% of the 214 citations to these primary data". Six critical papers received 6%. "63% of all citation paths … flow through one review paper" and 95% flow through four reviews. Mechanisms named:
  - "citation transmutation — the conversion of hypothesis into fact through the act of citation alone"
  - dead-end citations
  - "back door invention", that is abstracts cited as if they were papers
  - "citation diversion", where 3 citations grew into 7,848 supportive paths

  The same distortions appeared in 8 of 9 NIH-funded grant proposals.
- Source: Greenberg SA 2009, "How citation distortions create unfounded authority: analysis of a citation network", BMJ 339:b2680. PMC2714656
- TYPE: first-hand study (single claim). ACCESS: full text (XML).
- Locator: Results "Citation bias against critical primary data", "Amplification", "Invention", "grant proposals"; Box.
- Bearing:
  - C7 strongest mechanism-level evidence: inference read as fact, and internal consistency (authority) grows while support for correctness does not.
  - Q4: the only remedy shown is a computational counterfactual (removing the bias restores balanced authority), which is not deployed practice.

**F29. Contradicted claims kept getting cited favourably.**
- Claim: contradicted vitamin E claims were still cited favourably in 50% of citing articles in 2005, years after the refuting RCTs. Beta-carotene and estrogen showed similar persistence.
- Source: Tatsioni A, Bonitsis NG, Ioannidis JPA 2007, "Persistence of contradicted claims in the literature", JAMA 298:2517.
- TYPE: first-hand study. ACCESS: abstract/record only.
- Related: Ioannidis 2005 JAMA 294:218 (abstract only). Of 45 highly cited studies claiming effect, 7 (16%) were contradicted and 7 (16%) found stronger effects than later studies. Five of 6 non-randomised studies were contradicted or overstated.
- Bearing: C7 for. Contradiction is the dependency change, and citing texts did not register it.

**F30. ChatGPT 4o-mini never flagged retracted articles.**
- Claim: 217 retracted or concerning high-altmetric articles, each scored 30 times by ChatGPT 4o-mini. "none of its 6510 reports mentioned that the articles were retracted or had relevant errors". 190 got relatively high scores. For 61 claims from retracted articles, the model gave "a definitive yes or a positive response two-thirds of the time".
- Source: Thelwall M et al. 2025, "Does ChatGPT ignore article retractions and other reliability concerns?", Learned Publishing 38(4):e2018. White Rose eprint 229642 (PDF)
- TYPE: first-hand study. ACCESS: full text (PDF, abstract and introduction read).
- Bearing:
  - C6 and C7, agents measured: an LLM reproduces stale or retracted claims without signal.
  - The model was cheap and was not asked about retraction status, per the authors.

**F31. LLMs given a mixed guideline corpus used more superseded vocabulary; stated rationale was often invalid.**
- Claim: 4 open-weight LLMs on sepsis vignettes with a mixed current and superseded (Sepsis-3 vs SIRS) guideline corpus. "injecting guideline context of any kind increased superseded-vocabulary use for every model". The stated rationale was valid in only 53.7% of responses despite near-ceiling conclusion accuracy.
- Source: Yu Y 2026, "Diagnostic accuracy masks outdated reasoning: evaluating LLMs on evolving clinical guidelines", Preprints.org doi:10.20944/preprints202609.1228.v1
- TYPE: first-hand study (single-author preprint, not peer reviewed). ACCESS: abstract/record only.
- Bearing: Q7 lead (superseded text read as authority). This is for the agent track to verify.

### E. Drug labels and clinical decision support (dependency tracking outside publications)

**F32. Generic drug labels diverged from the brand label despite an FDA mandate.**
- Claim: 9105 structured product labels were indexed by NLP. "68% of multi-manufacturer drugs had discrepancies in ADR labeling"; "77.9% of generic manufacturers produced labels differing from brand". Causes included "missing tables, outdated post-marketing reports, and formatting issues".
- Source: Duke J, Friedlin J, Li X 2013, "Consistency in the safety labeling of bioequivalent medications", Pharmacoepidemiol Drug Saf. doi:10.1002/pds.3351
- TYPE: first-hand study. ACCESS: abstract/record only.
- Bearing:
  - C6 for: divergent copies of one fact, a dependent text (generic label) not following its source (brand label).
  - C1: a legal mandate ("identical warnings") is an instruction that did not enforce itself (C8). Automated NLP comparison is a check that can fail and found the divergence.

**F33. Decision-support rules silently broke when a code they depended on changed.**
- Claim: an amiodarone-TSH alert stopped firing for new patients because "in November 2009, the LMR's internal code for amiodarone had been changed from 40 to 7099, but the rule logic in the system was never updated". It was found by chance during a February 2013 demonstration, with an estimated 9,774 missed firings. "two of the malfunctions … went unrecognized for over a year". 93% of responding CMIOs had experienced a malfunction. On confidence that current processes would catch all malfunctions, 0 of 29 were totally confident and 18 of 29 (62%) not very or not at all confident. "users were less likely to report cases of missing CDS alerts". The recommendation: terminology tools "should have the capability to detect and mitigate the downstream impact of terminology changes".
- Source: Wright A et al. 2016, "Analysis of clinical decision support system malfunctions: a case series and survey", JAMIA 23:1068. PMC5070518
- TYPE: first-hand study (case series and survey). ACCESS: full text (XML).
- Locator: Case Study 1; Table (survey); Discussion paragraphs 1–3; Recommendations.
- Bearing:
  - C2 strongest direct example: a dependency changed and the dependent knowledge artefact silently lost validity. A failure of omission is invisible to users.
  - Q3: the remedies are regression tests, impact analysis of terminology changes, and anomaly detection on firing rates.

## 3. Mechanisms

| Mechanism | Failure kind it signals | What it detects | What it misses | Cost | Evidence | Agents measured? |
|---|---|---|---|---|---|---|
| Fixed review or expiry date (2–5 yr) | Lost validity (by proxy of age) | Nothing specific; it forces a re-look | Invalid-at-publication texts (7% of SRs, F7); fast-moving topics; texts between dates | Low per text; whole re-review when due | F1, F5; Shojania 7% at publication | n |
| Surveillance signals (Ottawa: limited search plus significance/≥50% effect change; RAND: journals, FDA, experts) | Lost validity after new evidence | New trials that would plausibly shift conclusions | Trials not in the limited search; non-primary outcomes; judgment variance; low expert response (35%) | Moderate; repeated every 6–12 mo | F7, F10, F11 (partial validation for Ottawa) | n |
| Expert polling of original panel | Lost validity | What panel experts know | Whatever experts don't know (premise untested, F2) | Low to moderate; response-limited | F1 (71% response), F10 (35%) | n |
| NICE reactive/planned surveillance with recorded outcome (incl. retire) | Lost validity, policy change | Monitored events | Whatever monitoring misses; "subject to constraints on capacity" | Moderate; owner capacity | F6 (standard only, no outcome data) | n |
| Living SR (continuous search, versioned "as of" date) | Lost validity | New studies within the search | Staleness when the living process itself stops (42% lag >3×; no retirement notices) | High: 5 min–32 h per month per review | F12, F13, F14 | n |
| "Update status" plus change report between editions | Misreading of an old edition as current | Which edition and what changed | Only as good as authors' reporting (Bastian & Doust: hard to see what changed) | Low | F8, F11 | n |
| Recommendation-to-evidence mapping | Enables dependency-triggered rechecks | Which recommendation rests on which study | Absent pre-2008 at ACC/AHA; guidelines poorly indexed | Moderate at authoring | F4, F15, F16 | n |
| Retraction notice, watermark, PubMed/Medline flag | Misrepresentation at source | Readers who see the publisher/indexed copy | Copies elsewhere (5% of web copies marked); inconsistent indexing (58% marked in both); does not reach citing texts | Low | F15, F21–F25 | n |
| Reference-manager flag (Zotero 2019, Papers/EndNote 2021) | Retracted source in one's library | Retracted items with DOI/PMID matched to Retraction Watch | Items without identifiers; texts already published; no measured effect found | Near zero for users | F24; disconfirming search §4 | n |
| Forward-citation contamination search plus re-analysis excluding retracted trials | Propagated misrepresentation (C7) | Which SRs/guidelines depend on a retracted trial, and the effect change | Done ad hoc by researchers; guidelines poorly indexed; supplements not scanned | High (60 trained volunteers in F16) | F15, F16, F17 | n |
| Retracted-reference detectors (Feet of Clay Detector, retracted.net, SpiderCite) | Retracted dependency in a published text | Retracted refs in reference lists | Supplements; post-detection action is not automatic | Low | F16, F17 | n |
| Trustworthiness screening before inclusion (REAPPRAISE, CPC-TST, TRACT, INSPECT-SR) | Misrepresentation not yet retracted | Integrity red flags | Unvalidated in these texts | Moderate | F16 (named only) | n |
| Sensitivity analysis excluding suspect studies | Propagated misrepresentation | Fragility of pooled result | Requires suspicion first | Low | F15 (Cockayne: OR 0.23 → 0.30, CI 0.05–1.74) | n |
| CDS regression tests, terminology change-impact analysis, firing-rate anomaly detection | Dependency change breaking knowledge artefact | Rules that stop or over-fire | Recommended rather than evaluated; omission is invisible to users | Moderate | F33 | n |
| NLP comparison of dependent labels against source label | Divergent copies | Generic label deviating from brand | Whether the brand label is itself current | Low once built | F32 (abstract) | n |
| LLM used as reader/evaluator | none: it fails to signal | — | Retraction status ignored in 6510/6510 reports | — | F30, F31 | **y** (as failure, not as mechanism) |

## 4. Disconfirming searches and results

1. **Has staleness detection been solved here?** Queries: SR update signals and surveillance validation; Ottawa/RAND validation; living SRs.
   - Found: a partially validated failable signal (Ottawa, F11) and an operational surveillance system (F10).
   - But: there is no validation against a gold standard (F10). Signal-bearing reviews were not updated faster (F9). LSRs lag and never declare retirement (F13). Consensus says "Mechanical rules appear unworkable" (F11).
   - Conclusion: not solved. The best mechanisms are judgment-based checks that can fail, with unknown sensitivity.
2. **Do most stale texts stay valid?** Searched as part of the guideline/SR obsolescence queries.
   - Found:
     - 9% of updated Cochrane reviews changed conclusion (F8); 4% (F9)
     - 71% of AHRQ SRs low priority (F10)
     - 80% of class I recommendations retained, <1% reversed (F4)
     - 96% of recalculated estimates within the original CI (F17); about 79% of affected meta-analyses unchanged in direction/significance (F16)
     - Bakker et al. 2024 (PMC10982619, full text XML, line on post hoc analysis): removing retracted data "did not alter results of most meta-analyses substantially. This suggests that results of systematic reviews are robust to individual retractions"
   - Conclusion: this is the strongest evidence against a cost claim. Most dependent texts stay valid after most dependency changes. The minority that flips cannot be identified in advance (F8: predictors known only after the update; F10: neither elapsed time nor article count predicts). Harm is concentrated where few studies exist (F16: OR 2.63 for direction change at ≤10 vs ≥20 studies).
3. **Are post-retraction citations mostly perfunctory or negative?** Queries: post-retraction citation context.
   - Found the opposite: 83% positive (F20) and 5.4% acknowledging the retraction (F19). Hsiao & Schneider note that high-profile retractions are acknowledged more often (Introduction).
   - Conclusion: the disconfirming hypothesis is rejected for biomedicine, although many citations are in introductions (Hsiao Table 5, F19).
4. **Do retraction notices and reference-manager integrations measurably cut post-retraction citation?** Query: "effect of Zotero retraction alert Retraction Watch integration on post-retraction citations measured study" (extended).
   - Found: retraction notices do measurably reduce citations (F21, F22), with contrary uncontrolled evidence (F23). No study measures the effect of Zotero, EndNote or Papers flags; this matches RISRS (F24). ReTracker (an Illinois Zotero plugin) is a tool paper, not an effect study. An OSF preregistration on correction notices was seen only as a search lead.
   - Conclusion: unstudied.
5. **Are errata and corrections propagated to citing work?** Query: errata and correction propagation.
   - Found: F26 (corrected versions barely preferred for 8+ years) and F27 (1/3 of source articles still uncorrected online). There is no study of whether citing papers adopt the corrected values.
   - Conclusion: propagation is poor at the source; at the citing text it is unstudied.
6. **Does drug-label dependency tracking work?** Query: generic/SmPC label discrepancy and timeliness (Europe PMC, no hits beyond Duke).
   - Found only F32 (abstract).
   - Conclusion: thin evidence.

## 5. Fields and terms the brief missed

- "Surveillance" (NICE, AHRQ EPC): the term of art for checking that a guidance text is still valid.
- "Signals for updating" (Ottawa and RAND methods).
- "Update status" (PUGs).
- "Static list" (NICE PMG16, unverified).
- "Retirement" of guidance or LSRs.
- "Living guidelines".
- "Medical reversal" (Prasad and colleagues; not read).
- "Contradicted claims" and "persistence" (Ioannidis).
- "Citation distortion": bias, amplification, transmutation, back-door invention, diversion, the "lens effect" (Greenberg).
- "Biblioremediation" (Peterson).
- "Persistence of error" (Davis).
- "Evidence ecosystem contamination chain" (VITALITY).
- "Feet of Clay Detector" and the Problematic Paper Screener.
- "Expression of concern".
- Crossmark; NISO CORREC.
- "Knowledge maintenance" (Fu & Schneider 2020, keystone framework; not read).
- "Trustworthiness screening" (INSPECT-SR).
- CDS "knowledge management" and "terminology change impact".
- Structured Product Labeling consistency.
- "Paper mills" as a source of invalid dependencies (172 of the VITALITY retracted trials).

## 6. Thin or contested points; unreachable sources

- **Unreachable or abstract only:**
  - Shekelle 2001 JAMA and Shojania 2007 Ann Intern Med (paywalled; the AHRQ technical review on NCBI Bookshelf was blocked by reCAPTCHA). Their figures are reported from abstracts only.
  - Also abstract only: Akl 2023, Kataoka 2022, Mott 2019, Duke 2013, Tatsioni 2007, Ioannidis 2005 and Yu 2026.
  - Not obtained: Furman, Jensen & Murray 2012 (Research Policy); Fanelli, Wong & Moher 2022 (Account Res); Schneider et al. 2020 (Scientometrics, the 11-year case). The last is known only via the Hsiao and Schneider 2021 Table 1 entry: 5/112 (4.5%) post-retraction citations mentioned the retraction.
- **Contested:** the effect of retraction on later citation. Controlled designs (F21, F22) show reductions; the uncontrolled pre-post design (F23) shows none in the long term. Avenell's "46% in first year" attribution to Mott is not visible in Mott's abstract.
- **Thin:**
  - No measured effect of reference-manager retraction flags, Crossmark, or automatic alerts to citing authors.
  - No data on NICE surveillance outcomes.
  - Drug-label dependency evidence rests on one abstract.
  - Cost per LSR is reported as ranges only.
- **Inference, not shown:** these fields have source-side signals (retraction notice, new trial, code change) but no dependent-side links. The change does not reach texts that depend on it except by ad hoc forward-citation search (F15, F16), the absence of recommendation-to-reference mapping (F4), or chance discovery (F33). That is the specific form C2 takes here.
