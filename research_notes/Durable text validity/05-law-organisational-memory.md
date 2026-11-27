# Track t05: Law and organisations: how fields built on durable text signal that a text is still valid

Brief questions 1, 3, 5, 7. Claims C1, C2, C5, C7 (some bearing on C6).
All downloads are in the scratchpad `dl/t05/`. Every figure below was taken from a full text I read, unless marked otherwise.

## 1. Scope and searches run

Searches (web), in order:
- Hellyer "Evaluating Shepard's, KeyCite, and BCite for Case Validation Accuracy" pdf
- Mart "The Algorithm as a Human Artifact" Law Library Journal pdf
- Magesh "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools" arxiv
- empirical study statutes declared unconstitutional remain on the books ... "zombie" law review
- Chin Hartley "Still on the Books: Jim Crow ..." pdf
- Widiss "Undermining Congressional Overrides" Hydra problem pdf
- "This text is meant purely as a documentation tool and has no legal effect" (EU consolidation disclaimer); same with "Union's institutions do not assume any liability"
- empirical review clauses EU legislation EPRS rolling check-list
- post-legislative scrutiny UK memoranda empirical Caygill; WFD "Post-legislative scrutiny in the UK Parliament"
- sunset clauses empirical evidence renewed automatically without review
- Argote Beckman Epple 1990 persistence and transfer of learning pdf
- audit hospital policies past review date percentage (organisational policy staleness)
- de Holan Phillips 2004 organizational forgetting pdf; Walsh Ungson 1991 organizational memory pdf
- Schulz "Impermanent institutionalization" rule obsolescence
- WorldCC value erosion, post-signature obligations; Macaulay non-contractual relations; relational contracts
- benchmark LLMs identify overruled precedent / "good law" (found Zhang et al. 2025; Demir & Canbaz 2026)
- Spriggs & Hansford 2000 reliability of Shepard's
- courts continue to cite overruled / overridden precedent (found Broughman & Widiss 2017)
- Planned Parenthood Arizona v. Mayes 2024 opinion pdf (1864 statute revived)
- RPC post-implementation reviews overdue (UK statutory review clauses)

Direct fetches: AALL (Hellyer), arXiv (Magesh, Dahl, Zhang, Demir), CourtListener (Mata), damiencharlotin.com, Lewis & Clark L. Rev. (Wasserman), Georgetown L.J. (Johnson), Texas L. Rev. (Christiansen & Eskridge), Indiana repository (Broughman & Widiss), legislation.gov.uk/help, Hansard Society blog, RPC blog, Springer OA (Jones & Quandt), JSTOR copy (Argote et al.; Macaulay).

## 2. Findings

### A. Legal citators: the main signal that case law is still valid, and how often it is wrong

- **F1. Commercial citators miss or mislabel about a third or more of negative treatment, and agree with one another rarely.**
  Source: Paul Hellyer, 2018, "Evaluating Shepard's, KeyCite, and BCite for Case Validation Accuracy", Law Library Journal 110:4, 449–476. https://www.aallnet.org/wp-content/uploads/2018/12/LLJ_110n4_02_hellyer.pdf
  TYPE: first-hand study. ACCESS: full text read.
  Sample (¶24, ¶48–50): every citing relationship to the 73 published Ninth Circuit decisions of January 1984 that at least one citator labelled negative. That gives 357 relationships. The author judged 21 not negative and 27 ambiguous, leaving 309 clearly negative.
  Table 1 (p. 465): share of the 309 that each citator failed to identify correctly.

  | Citator | Omitted, or labelled positive/neutral | Labelled negative but wrongly described | Total failures |
  |---|---|---|---|
  | Shepard's | 85 (28%) | 18 (6%) | 103 (33%) |
  | KeyCite | 105 (34%) | 11 (4%) | 116 (38%) |
  | BCite | 211 (68%) | 11 (4%) | 222 (72%) |

  - Agreement between citators (¶48): "all three citators agree that there was negative treatment only 53 times. This means that in 85% of these citing relationships, the three citators do not agree on whether there was negative treatment." They substantively agree on the type of treatment "only 11% of the time". The conclusion (¶80) puts it as "for almost 90% of the negative labels reviewed here, at least one citator conflicts with another."
  - False negative flags (¶52): 12% of Shepard's negative labels were incorrect, 11% of KeyCite's and 15% of BCite's. Errors are asymmetric (¶53): "The citators are much more likely to label a negative reference as positive than label a positive reference as negative ... the first type ... may lead users to cite invalid case law."
  - Overrulings by the U.S. Supreme Court (¶58): the dataset has four. "Shepard's mislabeled three of them, while KeyCite mislabeled two and BCite mislabeled one."
  - Undercount (¶55): "I would not have caught any negative treatment that all three citators missed ... The performance rates presented here may underestimate the extent of the problem."
  - No uncertainty shown (¶49): "none of the citators labeled any of the citing relationships as ambiguous ... the results you get depend mainly on which citator you happen to be using."
  - Vendor response (¶73): Thomson Reuters said analysing opinions "does not lend itself to an 'objectively correct' interpretation."
  - Earlier studies, as Hellyer reports them (¶8, ¶12): Taylor 2000 found that, assuming every negative label was right, Shepard's missed 23% and KeyCite 25%. A Westlaw expert panel (Dabney) was unanimous "only about half the time".

  Bearing: C1 (FOR). The best-established failable validity check for legal text is itself unreliable, and it presents its verdict as fact. C2 (FOR). A case can lose validity, and the signal meant to show that is often absent. Q3: a mechanism map entry. Q5: the conclusion (¶81) says "Relying only on a citator's treatment symbols is a risky strategy". It is the strongest evidence AGAINST "citators make validity checking reliable".

- **F2. Citators flag statutory overrides late, sometimes never, and often wrongly.**
  Source: Matthew R. Christiansen and William N. Eskridge Jr., 2014, "Congressional Overrides of Supreme Court Statutory Interpretation Decisions, 1967–2011", Texas Law Review 92:1317. https://texaslawreview.org/wp-content/uploads/2015/08/EskridgeChristiansen-92-6.pdf
  TYPE: first-hand study (the citator is used as an instrument). ACCESS: full text read.
  - How flags arise (p. 1342): "Although Westlaw will sometimes mark a case as superseded directly by statute, it relies primarily on judicial decisions and administrative documents that indicate that the case has been superseded."
  - Lag (p. 1343): "the average number of years between the enactment of the override and its identification on Westlaw was just under six years". For overrides from the 100th Congress on, it was "just under four years".
  - Never flagged: for the 100th–105th Congresses, "only ten percent of overrides were not identified on Westlaw". For the 106th Congress on, "A little less than a third ... have not yet been identified". Footnote 128: "56 cases are not identified as overridden by Westlaw".
  - Example: the override of FDA v. Brown & Williamson by the 2009 Tobacco Control Act "still did not appear as superseded by statute as this Article went to print in mid-2014".
  - False flags (p. 1328): of the "superseded by statute" leads, "About half the time, they were not overrides".

  Bearing: C2 (FOR, strongly). A change in what the text depends on, here an Act of Congress, leaves no signal on the dependent text, the precedent, until some later reader writes one. Q3: the signal is derived from later reader-written text, not from the change itself.

- **F3. Courts keep citing overridden precedent almost as before. The authors attribute this to missing signals.**
  Source: Brian J. Broughman and Deborah A. Widiss, 2017, "After the Override: An Empirical Analysis of Shadow Precedent", Journal of Legal Studies 46:51–. https://www.repository.law.indiana.edu/facpub/2545
  TYPE: first-hand study (difference-in-differences on citation counts and Shepard's signals). ACCESS: full text read.
  - Signals (p. 53, p. 59): overrulings are "immediately 'red flag[ged]'". By contrast, "a case generally will not be identified as superseded by a statute until a court issues a decision that makes this connection; consequently, there is often a multiyear lag".
  - Citation after the event (p. 60). "Shadow-precedent score" is post-event annual net citations as a share of pre-event citations.

    | Group | n | Mean | Median |
    |---|---|---|---|
    | Overridden by Congress | 132 | 89% | 71% |
    | Overruled by a court | 49 | 58% | 56% |
    | Control | 113 | 97% | 86% |

  - Abstract: ongoing citation "may be driven more by information failure or ambiguity than by ideological disagreements".
  - Footnote 7, citing Widiss 2015 on the ADAAA: "lower courts regularly continue to cite the overridden precedents as controlling law. Some of these lower-court decisions make no mention of the ADAAA".

  Bearing: C2 and C7 (FOR). Text that has lost its validity keeps propagating as authority through new judicial text. The authors' causal attribution to information failure is their inference.

- **F4. Disconfirming lead, not verified: Shepard's coding is "quite reliable".**
  Source: James F. Spriggs II and Thomas G. Hansford, 2000, "Measuring Legal Change: The Reliability and Validity of Shepard's Citations", Political Research Quarterly 53(2):327–341. https://sites.ucmerced.edu/hansford/publications/measuring-legal-change-reliability-and-validity-shepards-citations
  TYPE: first-hand study. ACCESS: abstract/record only.
  The abstract says "Shepard's coding of legal treatment is quite reliable, though there is some notable variance across Shepard's treatment categories."
  Bearing: against F1, but on different terms. It measures intercoder reliability for Supreme Court treatment as a research measure, not completeness of negative-treatment flags. It cannot be weighed against Hellyer without the full text.

### B. Legislative text: consolidation, "zombie" statutes, review and sunset clauses

- **F5. A statute held unconstitutional stays in the code, and repeal is slow and partial.**
  Source: Howard M. Wasserman, 2021, "Zombie Laws", Lewis & Clark Law Review 25:1047. https://law.lclark.edu/live/files/32777-254-wasserman-article
  TYPE: review/secondary (doctrinal). ACCESS: full text read.
  - Abstract: "A judicial declaration of constitutional invalidity does not erase a challenged law ... it remains on the books and may be enforced".
  - Examples (p. 1072): anti-miscegenation laws were invalidated in 1967, "but it took more than 30 years for South Carolina (1998) and Alabama (2000) to repeal". "Six years after Obergefell ... prohibitions on same-sex marriage remain in 30 state constitutions." The Lawrence sodomy ban "remained on the Texas statute books as of 2019". Virginia's 2019 commission identified "dozens of zombie laws".
  - Wasserman cites Chin et al., 2006 MSU L. Rev. 457 ("Still on the Books"); I could not reach it.

  Bearing: C2 (FOR). The authoritative text shows no mark of its invalidity; the signal lives elsewhere, in case law. This is inference from examples, not a prevalence study. It also bears on validity being relational and reversible: after Dobbs, pre-Roe bans became enforceable again (lead: Planned Parenthood Arizona v. Mayes, 545 P.3d 892 (Ariz. 2024); opinion PDF unreachable, 404).

- **F6. Laws still valid on paper but dead in practice are used selectively.**
  Source: Joel S. Johnson, 2022, "Dealing with Dead Crimes", Georgetown Law Journal 111:95. https://www.law.georgetown.edu/georgetown-law-journal/wp-content/uploads/sites/26/2022/11/Johnson-Dealing-with-Dead-Crimes.pdf
  TYPE: review/secondary. ACCESS: full text read.
  - Examples: an Idaho prosecutor in the late 1990s "charged eight pregnant high[-school girls]" under an unenforced fornication statute, and "most of the girls prosecuted were arrested after applying for public assistance". In 2004 a Virginia man was convicted under "a previously unenforced state adultery" law. The cases are reported from secondary sources.

  Bearing: C2, a variant. Here the text remains formally valid but its social premise has changed. Harm arises from acting on a text whose premise has gone. This is evidence that stale law does cause harm, anecdotal only.

- **F7. The UK revised-legislation service shows a signal that can fail, with a stated lag.**
  Source: The National Archives, legislation.gov.uk Help/FAQ (accessed 2026-11-27). https://www.legislation.gov.uk/help
  TYPE: standard/practitioner (official service documentation). ACCESS: full page read.
  - "Our aim is to update revised legislation with new amendments within a maximum of three months of the coming into force date ... In all cases, the 'changes to legislation' message tells you if there are any outstanding effects to the provision you are viewing."
  - The Changes to Legislation facility is updated "only after a series of preparatory editorial processes ... typically take from four to eight weeks".
  - On EU-origin law: "It will not be possible to complete all of the relevant updates within the usual timeframe."
  - Coverage: "All secondary legislation made from 2018 onwards is kept up to date. We are working to bring secondary legislation made before 2018 up to date."

  Bearing: Q3. This is the clearest case found of a text carrying an explicit "known pending changes" signal, with a published service level. Its window (4–8 weeks) is stated, so the signal can be wrong during that window. No accuracy audit was found.

- **F8. EU consolidated texts are disclaimed as having no legal effect.**
  Source: EUR-Lex consolidation notice. https://eur-lex.europa.eu/content/legis/avis_consolidation.html
  TYPE: standard. ACCESS: UNREACHABLE. EUR-Lex returned HTTP 202 with an empty body to curl and fetch; this is the site, not the network.
  The wording "meant purely as a documentation tool and has no legal effect" was seen only in search extracts. Lead only; do not cite as verified.

- **F9. Post-legislative scrutiny in the UK rarely happens.**
  Source: Edward Chesterman, Hansard Society blog, 12 Nov 2020, "Did you get the memo? Post-legislative scrutiny and the case of judicial review". https://www.hansardsociety.org.uk/blog/did-you-get-the-memo-post-legislative-scrutiny-and-the-case-of-judicial
  TYPE: review/secondary, reporting Caygill's research. ACCESS: full blog read. Caygill's own texts were unreachable (NTU repository 403, Newcastle thesis 202-empty).
  - Coverage: "out of 344 eligible Acts passed between the start of the 2005 Parliament and the 2017 general election, only 7.6% underwent either formal or informal post-legislative scrutiny. Committees ... conducted some form of post-legislative scrutiny in 61 instances, of which only 20 were formal PLS inquiries."
  - Uptake: of recommendations in 17 PLS reports from 2005 to 2016, "61% were either rejected or ignored or received an indeterminate response". Acceptance fell "from 52% for ... 'small' government actions, to zero for ... 'large'".
  - Case in point: PLS "has not yet been conducted" on the Criminal Justice and Courts Act 2015 even as a new review began.

  Bearing: C5 (FOR). Finding is not resolving, and the owner's attention limits action. Q5: a review obligation written in text does not establish that review takes place (also C8).

- **F10. Statutory review clauses go unmet in the UK.**
  Sources: Regulatory Policy Committee blog, 1 Dec 2025 (https://rpc.blog.gov.uk/2025/12/01/post-implementation-reviews-update-on-progress-across-government/) and 12 May 2026 "Progress stalls on post-implementation reviews" (https://rpc.blog.gov.uk/2026/05/12/progress-stalls-on-post-implementation-reviews/).
  TYPE: practitioner report (official body). ACCESS: full text read.
  - A PIR counts as outstanding if not undertaken "by the fifth anniversary of the introduction of the regulation". Reviews are a "statutory obligation" under the Small Business, Enterprise and Employment Act 2015, ss. 28–31.
  - Overdue PIRs fell "from over 80 to 47" between April and December 2025, and "the number still stands at 47" in May 2026. DfT went "down from 36 in April" to 9. Several departments "missed" their own committed deadlines.
  - No denominator (total PIRs due) was found.

  Bearing: C8 and C5 (FOR). A review clause gives the text an expiry signal, but whether review happens depends on someone's attention and external pressure; here the pressure was public naming.

- **F11. Sunset clauses: evidence of effect is weak, and renewals tend to become routine.**
  Source: Tanner Jones and Ryan Quandt, 2025, "An iridescent sunset: An empirical analysis of sunset legislation", Journal of Regulatory Economics 68:85–123. https://link.springer.com/content/pdf/10.1007/s11149-025-09498-5.pdf
  TYPE: first-hand study (DiD/SCM on state GDP), plus a literature review. ACCESS: full text read. Caveat: the authors are affiliated with the Cicero Institute (advocacy) and Vulcan Technologies.
  - Literature summary (abstract): "empirical studies have yet to find that sunset legislation improves efficiency or decreases waste. Rather, agencies seem to be renewed from the political inertia that they were meant to overcome."
  - History (p. 87–88): "By 1990, at least four states had repealed across-the-board sunset statutes". Legislatures "often reauthorized agencies with concentrated constituencies".
  - Their own estimate: a $14,000 GDP per capita increase (59.8%) under DiD. With SCM, robust only for Tennessee.
  - Discussion: effects attenuate, consistent with "renewal becomes routine; reviews become pro forma". That is their interpretation.

  Bearing: Q3 and Q5. An automatic-lapse default is a signal that cannot be left silent, but the review it forces tends towards rubber-stamping. It is mixed evidence; I would not rely on the GDP estimate.

### C. Legal AI reading superseded or overruled law (Q7)

- **F12. General LLMs perform badly on whether a case was overruled.**
  Source: Matthew Dahl, Varun Magesh, Mirac Suzgun and Daniel E. Ho, 2024, "Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models", Journal of Legal Analysis (arXiv:2401.01301v2). https://arxiv.org/abs/2401.01301
  TYPE: first-hand study. ACCESS: full text read.
  - Overall (abstract): "LLMs hallucinate at least 58% of the time".
  - "Overruling year" task (Table 4, SCOTUS cases explicitly overruled, n=279, zero-shot hallucination rates): GPT-4 0.810, GPT-3.5 0.919, PaLM 2 0.858, Llama 2 0.972. A false overruling premise (asking for the overruling year of a case never overruled, Table 6, zero-shot): GPT-4 0.531, GPT-3.5 0.821, PaLM 2 1.000, Llama 2 0.027.
  - "Doctrinal agreement" (whether two cases agree, ground truth from Shepard's, Table 5): 0.449–0.500, about chance.
  - Case age (§5.1.5): "LLMs' peak performance may lag several years behind the current state of the doctrine."

  Bearing: C2 and C6 (FOR). Models do not know that an authority has lost validity, and accept false premises that it has. It measures models without retrieval.

- **F13. Commercial legal research AI with retrieval still hallucinates and cites overruled law as good law.**
  Source: Varun Magesh, Faiz Surani, Matthew Dahl, Mirac Suzgun, Christopher D. Manning and Daniel E. Ho, 2024/2025, "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools", arXiv:2405.20362 (the PDF read is stamped v1; it includes Westlaw AI-AR); J. Empirical Legal Studies 22:216–242 (2025). https://arxiv.org/abs/2405.20362
  TYPE: first-hand study, preregistered. ACCESS: full text read (arXiv version; the JELS version was not read, and its figures may differ slightly).
  - Overall: the tools "each hallucinate between 17% and 33% of the time" (abstract). Accuracy: Lexis+ AI 65%, Westlaw AI-AR 42%, Ask Practical Law AI 19–20% (Fig. 4).
  - Query set (Table 2): 70 of 202 queries (34.7%) are "Jurisdiction or time-specific", covering "overturned cases, or new developments".
  - Overruled-authority errors: there is no separate rate for citing overruled authority. "Inapplicable authority" covers wrong jurisdiction, statute or court, or overruled authority. Its share among hallucinated responses (Table 6) is Lexis 0.38, Westlaw 0.23, Practical Law 0.34.
  - Worked examples (Fig. 2): Lexis+ AI applied Casey's undue-burden standard after Dobbs. Lexis+ AI "describes a rule established in Arturo D. as good law, with citation to the case that actually overrules Arturo D." Westlaw stated "a proposition based on an overruled or reversed case, without citing the case". The authors infer that this is suppression of red-flagged citations, which "impedes verification of the claims most likely to be false" (§6.2, fn. 21).
  - On the assumptions behind retrieval: RAG evaluations assume retrieved documents are "authoritative and applicable, an assumption that is not true in the legal setting ... Legal documents often contain outdated information".

  Bearing: C6 (FOR). An agent with access to a citator-backed corpus still reads superseded text as authority, and a design choice can remove the trace (the citation) of the stale source. Q7: first-hand.

- **F14. Even with the overruling opinion in context, frontier models often fail to name what it overruled.**
  Source: Li Zhang, Jaromir Savelka and Kevin Ashley, 2025, "Do LLMs Truly 'Understand' When a Precedent Is Overruled?", JURIX 2025, arXiv:2510.20941. https://arxiv.org/abs/2510.20941
  TYPE: first-hand study. ACCESS: full text read.
  - Data: 236 SCOTUS overruling cases; the full text of the overruling opinion is supplied in context (median 17,607 words).
  - Task 1, open-ended "which case(s) was overruled": best results were Gemini-Pro 73.31% (173/236) and GPT-5 71.19% (168/236). Errors include confusing cases that are merely mentioned with the overruled one, and hallucinating cases "neither cited in the text nor overruled".
  - Task 2, closed verification: GPT-5 75.42%, with "55 cases as 'False'" (false negatives). Gemini-Pro 42.37%, with 131 abstentions.
  - Task 3, a temporally impossible reversal: GPT-5 and Gemini-Pro both 100%.
  - Era sensitivity: some models were at 0% on the oldest interval (Table 3).
  - LLM-as-judge: GPT-4o agreed with human experts on 98% of a 10% sample.

  Bearing: C2, the misreading arm (FOR). The signal is present in the text and the agent still misreads it. Q7.

- **F15. LLMs classifying negative treatment, tested on Hellyer's annotations.**
  Source: M. Mikail Demir and M. Abdullah Canbaz, 2026, "Validate Your Authority: Benchmarking LLMs on Multi-Label Precedent Treatment Classification", arXiv:2605.17691. https://arxiv.org/abs/2605.17691
  TYPE: first-hand study. ACCESS: full text read.
  - Data: Hellyer's 2018 annotations, excluding ambiguous items, give 329 relationships. The paper's corpus table shows 239. More than 19% of relationships have more than one acceptable label.
  - Best accuracy: Gemini 2.5 Flash 79.1% on the high-level schema; GPT-5-mini 67.7% on the fine-grained schema.
  - The authors note that "there is a ceiling to how high any model's accuracy can be on this task" because of subjectivity.

  Bearing: Q3 and Q7. Agents are measured as validity checkers against a human-graded set. Error remains roughly at citator level. This is my inference: the scores are not directly comparable to Hellyer's citator miss rates.

- **F16. Courts sanction lawyers who file fabricated citations, and checking with the same tool failed.**
  Source: Mata v. Avianca, Inc., No. 22-cv-1461 (PKC), S.D.N.Y., Opinion and Order on Sanctions, ECF 54, 22 June 2023 (Castel, J.). https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0_3.pdf
  TYPE: practitioner record (judicial decision). ACCESS: full text read.
  - p. 1: respondents "abandoned their responsibilities when they submitted non-existent judicial opinions with fake quotes and citations created by the artificial intelligence tool ChatGPT, then continued to stand by the fake opinions after judicial orders called their existence into question."
  - Findings ¶45: Schwartz asked ChatGPT "Is Varghese a real case" and "Are the other cases you provided fake". It "responded that it had supplied 'real' authorities that could be found through Westlaw, LexisNexis and the Federal Reporter."
  - Sanction: "A penalty of $5,000 is jointly and severally imposed".

  Bearing: Q7. The verifier was grounded inside the generating system, so verification failed. C1: Rule 11 is the external check that failed late, through the opposing party and the court. The case concerns fabrication, not staleness.

- **F17. Court decisions on AI hallucinations record stale law rarely; fabrication dominates.**
  Source: Damien Charlotin, AI Hallucination Cases Database (accessed 2026-11-27; page says "Last updated: 27 November 2026"). https://www.damiencharlotin.com/hallucinations/
  TYPE: practitioner report / capability reference (curated database, CC BY 4.0). ACCESS: full page and embedded JSON read.
  - Size: "2367 cases identified so far". It covers decisions where a court "explicitly found (or implied) that a party relied on hallucinated content".
  - By case (filter counts): Fabricated 1935, Misrepresented 1006, False Quotes 618, Outdated Advice 38. Subcategories: Overturned Case Law 19, Repealed Law 19.
  - By item (graph JSON, n_items 6985): Fabricated 3850, Misrepresented 1965, False Quotes 1129, Outdated Advice 41. Subcategories: Overturned Case Law 21, Repealed Law 20.
  - Parties: Pro Se Litigant 1350, Lawyer 952. Monetary sanctions: 408.

  Bearing: C2 and C5. The record of court-detected AI failures is dominated by fabrication (the check that fails is "does the citation resolve"), then misrepresentation. Stale-law failures are about 1% of items. This is my inference: either stale authority is rare, or courts detect it far less than non-existent authority. The database cannot tell the two apart, so it is weak disconfirmation at best. Misrepresentation, which is beneath the wording, runs at about half the fabrication count.

### D. Organisational memory and contracts

- **F18. Organisational knowledge depreciates fast.**
  Source: Linda Argote, Sara L. Beckman and Dennis Epple, 1990, "The Persistence and Transfer of Learning in Industrial Settings", Management Science 36(2):140–154 (JSTOR copy via typeset.io).
  TYPE: first-hand study (Liberty Ship yards, monthly data). ACCESS: full text read.
  - p. 146: "A value of λ = 0.75 implies that, from a stock of knowledge available at the beginning of a year, only 3.2% (0.75^12) would remain one year later ... Even with a value of λ as high as 0.90, only 28% ... would remain".
  - Turnover did not explain it. Conclusion (p. 151): depreciation "might also result from lost or inadequate organizational records". The Steinway example: a discontinued piano was rebuilt from a disassembled instrument and a foreman's "black book".

  Bearing: C5 (indirect). Without records made at the time, knowledge is reconstructed. It measures productive knowledge, not text validity: here records are the remedy, not the hazard. Opposite direction to C2: knowledge decays faster than text, so text can outlive the knowledge needed to tell whether it still holds. That last point is inference.

- **F19. Contracts: the "paper deal" diverges from the "real deal", and parties seldom consult it.**
  Source: Stewart Macaulay, 1963, "Non-Contractual Relations in Business: A Preliminary Study", American Sociological Review 28:55–67 (JSTOR copy at masonlec.org). https://masonlec.org/site/rte_uploads/files/Macaulay%20class%202%20background.pdf
  TYPE: first-hand study (interviews with 68 businessmen and lawyers from 43 companies and 6 law firms, plus a review of one firm's order records). ACCESS: full text read.
  - Order records: orders where "no agreement on terms and conditions was reached or no contract was formed" were 75.0% (1953), 69.4% (1954), 71.5% (1955) and 59.5% (1956).
  - On disputes: parties "often ... will never refer to the agreement but will negotiate a solution when the problem arises apparently as if there had never been any original contract".

  Bearing: a disconfirming nuance for C2 and C6. When readers do not act on the durable text, its staleness costs little. The problem bites where text is acted on as authority, as with agents. Applying this to agents is inference.

- **F20. Contract value lost after signature (vendor/association figures).**
  Source: WorldCC/Ironclad and WorldCC/CCM figures, roughly 9–11% of contract value.
  TYPE: practitioner report. ACCESS: abstract/record only (press releases via search). Not verified; do not cite figures.

## 3. Mechanisms

| Mechanism | Failure kind it signals | What it detects | What it misses | Cost | Evidence | Agents measured? |
|---|---|---|---|---|---|---|
| Citator flags (Shepard's, KeyCite, BCite) | Loss of validity (judicial dependency changed) | Explicit overrulings, mostly; negative treatment in citing cases | 28–68% of negative treatment omitted or mislabelled; 3 of 4 SCOTUS overrulings mislabelled by Shepard's; no ambiguity shown (F1) | Editorial labour; subscription | Hellyer 2018 (full) | n (citator); y via F15 |
| Citator "superseded by statute" | Loss of validity (statutory dependency changed) | Overrides, once some court or agency document says so | Lag of just under 4–6 years; about 10% to a third never flagged; about half of flags are not overrides (F2) | As above | Christiansen & Eskridge 2014 (full) | n |
| Red flag suppression in a RAG tool | Loss of validity | Removes red-flagged citations | Statement stays, citation goes, so the trace is gone (F13) | Design choice | Magesh et al. (full) | y |
| Official revised-text service with a "Changes to legislation" box (legislation.gov.uk) | Loss of validity (amendment) | Known outstanding effects, per provision | 4–8 week window; pre-2018 secondary legislation; EU-origin backlog (F7) | Editorial team | Official FAQ (full) | n |
| Consolidated-text disclaimer (EUR-Lex) | Misrepresentation risk of a derived copy | Nothing; it disclaims, it does not detect | Everything | Very low | Unreachable (F8) | n |
| Judicial invalidation without repeal | Loss of validity | Court's judgment binds courts | The statute text itself carries no mark; it stays enforceable (F5) | Legislative time to repeal | Wasserman 2021 (full) | n |
| Post-legislative scrutiny memoranda and inquiries | Misrepresentation of effect; obsolescence | Whether an Act met its objectives | 7.6% of eligible Acts reviewed (2005–17); 61% of recommendations rejected, ignored or indeterminate (F9) | Committee time | Hansard Society reporting Caygill (secondary) | n |
| Statutory review clause / PIR deadline | Obsolescence | Forces a review by year 5 | Over 80, then 47, overdue; compliance driven by naming (F10) | Department analysis | RPC 2025–26 (full) | n |
| Sunset (automatic lapse) | Obsolescence | Forces a decision to continue | Renewal by inertia, pro forma review (F11) | Review commission | Jones & Quandt 2025 (full; advocacy-affiliated) | n |
| Rule 11 / court sanctions | Fabrication; misrepresentation | Non-existent cites, false quotes (resolution failures) | Stale but real authority is rarely recorded (F17) | Litigation cost; sanctions | Mata (full); Charlotin DB (full) | y (as cause) |
| LLM as overruling or treatment checker | Loss of validity; misreading | Overruling relationships with text in context | 27–29% miss even for best models; false negatives; era bias (F14, F15) | Low per query | Zhang 2025; Demir 2026 (full) | y |

## 4. Disconfirming searches and results

- **Do citators make legal validity checking reliable (low miss rates)?**
  Searched for Hellyer, Taylor, Dabney, Spriggs & Hansford, and the LexisNexis rebuttal.
  Found: Spriggs & Hansford (2000) report Shepard's coding as "quite reliable" (abstract only, F4). LexisNexis marketing claims Shepard's outperforms KeyCite (vendor material, not read).
  Conclusion: no full-text study shows low miss rates for negative treatment. The best full-text evidence (Hellyer, Taylor as reported, Christiansen & Eskridge) shows substantial misses and lags. Contested only in the sense that the vendors dispute Hellyer's ground truth ("subjective determinations").
- **Does stale law or policy rarely cause harm?**
  Searched for zombie laws, dead crimes, overridden precedents and the hallucination database categories.
  Found: Charlotin's database records "Outdated Advice" in about 1% of items (F17). Macaulay shows parties often ignore the written contract (F19). Hellyer ¶57 says some misses are "trivial".
  Counter-evidence: Broughman & Widiss (F3) show courts continue to cite overridden precedent at 89% of prior levels. Johnson (F6) and Wasserman (F5) document enforcement or the threat of it.
  Conclusion: there is no measure of harm rates. Persistence of stale authority is well shown; its downstream cost is shown only anecdotally. Low counts in court records are confounded by detection.
- **Is the problem solved somewhere?**
  Searched for legislation.gov.uk and EUR-Lex consolidation.
  Found: the closest is the UK revised-legislation service's per-provision outstanding-effects box with a stated lag (F7). No accuracy audit of it was found.
- **Do sunset or review clauses actually trigger review?**
  Searched for sunset empirical evidence, UK PLS and RPC PIRs.
  Found: they trigger some review, often late or pro forma (F9–F11). No study gives a rate at which review clauses were honoured on time with a denominator.
- **Hospital or organisational policy staleness prevalence.**
  Searched for audits of policies past their review date. Found only vendor pages and an HSE Ireland audit PDF (404).
  Conclusion: unstudied, as far as I found.

## 5. Fields and terms the brief missed

- "Shadow precedent" and congressional "overrides" versus "overrulings" (Widiss; Christiansen & Eskridge). This is the legal name for a text losing validity through a change in a different text, without a signal.
- "Zombie laws" and "zombie state constitutional provisions" (Wasserman; Brady 2021, Wisconsin L. Rev., not read). Also "dead crimes" and desuetude (Johnson).
- "Case validation" and "negative treatment" as the citator field's terms. "Superseded by statute", "overruling recognized by" and "implied overruling" are label types with known failure modes.
- "Outstanding effects" and "revised legislation" (UK). "Point-in-time" versions.
- Post-legislative scrutiny (PLS), post-implementation review (PIR), and the "statutory review requirement" (SBEE Act 2015 ss. 28–31). Also "regulatory accumulation" and "regulatory stock".
- "Knowledge depreciation" and "organizational forgetting" (Argote; de Holan & Phillips). Also rule "obsolescence" and "impermanent institutionalization" (Schulz 1998, 2003; abstract only).
- "Paper deal versus real deal" (Macaulay). Also contract "value erosion" and "obligation management" (practitioner).
- "Contra-factual bias" (Dahl et al.): accepting a false premise, such as "this case was overruled".

## 6. Thin or contested points; unreachable sources

- **Unreachable:**
  - Mart 2017 (Colorado PDF 503; CORE 403). It concerns search algorithms rather than validity and is off-target in any case.
  - Chin et al. 2006, "Still on the Books".
  - EUR-Lex consolidation notice (202, empty).
  - Caygill thesis and papers (403 or 202).
  - Walsh & Ungson 1991; de Holan & Phillips 2004; Schulz 1998 and 2003 (no open full text).
  - Widiss 2014 "Identifying Congressional Overrides Should Not Be This Hard" and Widiss 2015 on the ADAAA (cited via F3 only).
  - Planned Parenthood Arizona v. Mayes opinion (404).
  - Spriggs & Hansford 2000 (abstract only).
- **Contested:** Hellyer's ground truth is his own reading. The vendors dispute it, and Dabney's panel was unanimous only about half the time. Validity of case law is partly a judgement, so the "check that can fail" is itself interpretive (C1's second sentence). Both sides of this agree that the citators present their labels without uncertainty.
- **Thin:**
  - There is no study of how often lawyers actually rely on stale authority, or of the harm.
  - The Charlotin category counts depend on one curator's coding.
  - Magesh et al. do not isolate an overruled-authority rate.
  - Zhang et al. and Demir & Canbaz are small (n=236, n=239) and Demir & Canbaz is recent (2026).
  - The sunset GDP study comes from advocacy-affiliated authors.
- **Inference flagged:** applying Macaulay and Argote to agents reading text as authority; reading the low "Outdated Advice" count as a detection gap.
