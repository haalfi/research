# Track 01: deep-research workflow, verified claims

Run: deep-research workflow (5 search angles, 24 sources fetched, 119 claims extracted, 25 verified by 3-vote adversarial check; 20 confirmed, 5 refuted).
A claim survives with at most 1 of 3 refuting votes. Rendered verbatim from the workflow result; refuted claims are in 02.

## Workflow summary

The verified evidence firmly supports one part of the problem statement: durable text loses validity when what it depends on changes, and nothing in the text shows it. This holds for clinical evidence syntheses (Shojania et al. 2007: 57% of 100 reviews acquired an updating signal, median 5.5 years, 7% already at publication), clinical guidelines (Martinez Garcia et al. 2014: about 1 in 5 recommendations out of date after 3 years) and software architecture documentation (Feilkas et al. 2009: 9-19% of dependencies undocumented, 70-90% of mismatches being documentation flaws). The bold claim that what a text says is 'generally held to no check that can fail' is contested rather than established. Other fields have built signals that can fail and that sit on or beside the text: update-status labels with reasons, 'date of last search' stamps in living reviews, assurance-case defeaters with an open/closed status, version manifests on safety evidence, and nightly architecture conformance checks. Each covers only what was recorded or made mechanical, and most were proposed without being evaluated. The verified set also supports, more weakly, that recovered rationale has no ground truth to check against (RecovAr) and that review is the dominant, perhaps over-relied-on, check on assurance-case text. It gives no verified evidence on the brief's questions about propagation (Q4), acceptance criteria and user testing (Q5), finding missing decisions (Q6), LLM agents (Q7), legal citators or retraction systems. The statement's claims on those points therefore stay unstudied in this run, not refuted.

## Verified findings (after merging duplicates)

### W1 (high; vote 3-0 on all four merged claims ([0],[1],[2],[3]))

Evidence syntheses go out of date quickly, and their conclusions can be out of date when first published. In a cohort of 100 high-quality quantitative systematic reviews (published 1995-2005, indexed in ACP Journal Club), 57% (95% CI 47-67%) acquired a signal for updating, with a median of 5.5 years (CI 4.6-7.6) free of a signal. 23% had a signal within 2 years, 15% within 1 year, and 7% (CI 3-14%) already had one at publication. Median lag from search to publication was 0.6 years for Cochrane reviews, 1.1 years for technical reports and 1.3 years for journal reviews. [First-hand study; supports the 'loss of validity when a dependency changes' failure kind.]

Sources: https://pubmed.ncbi.nlm.nih.gov/17638714/ · https://www.ncbi.nlm.nih.gov/books/NBK44099/

Evidence and qualifications: Shojania KG, Sampson M, Ansari MT et al., 'How quickly do systematic reviews go out of date? A survival analysis', Ann Intern Med 2007;147:224-33, and its companion AHRQ report 'Updating Systematic Reviews' (Report No. 07-0087, 2007; PMID 20734512). Both are the same study in two venues, so this is one dataset, not two independent replications. Verifiers matched every figure word for word in the abstracts, reached through E-utilities and Europe PMC; the NCBI Bookshelf page was behind a reCAPTCHA. Qualifications: (a) a 'signal for updating' is an operational proxy (a change in significance, a relative change of at least 50% in effect size on a primary or mortality outcome, or a qualitative change such as new harms) and does not show that the conclusion became wrong. (b) Signals were judged without content experts. (c) Much early staleness is publication lag: measured from the end of the search, only 4% had a signal within 1 year and 11% within 2 years. (d) The sample is narrow: drug, device and procedure reviews of RCTs only. (e) The data are old but are a historical measurement.

### W2 (high; vote 3-0 ([5],[6]))

Clinical guideline recommendations lose validity at a measurable rate. Of 113 recommendations randomly sampled from 4 Spanish National Health System guidelines, 92.0% (95% CI 86.9-97.0) were still valid at 1 year, 85.7% at 2 years, 81.3% at 3 years and 77.8% at 4 years. The authors conclude that about 1 in 5 is out of date after 3 years and that waiting more than 3 years to review a guideline is 'potentially too long'. [First-hand retrospective cohort study with Kaplan-Meier analysis. The 3-year interval is the authors' interpretation and was not tested as an intervention.]

Sources: https://www.cmaj.ca/content/early/2014/09/08/cmaj.140547 · https://pmc.ncbi.nlm.nih.gov/articles/PMC4216254/

Evidence and qualifications: Martinez Garcia L et al., 'The validity of recommendations from clinical guidelines: a survival analysis', CMAJ 2014;186(16):1211-1219. The verifier read the full text on PMC; the cmaj.ca page returned 403. 'Valid' is operational: the recommendation has no linked key reference (RCT or systematic review) that could trigger an update, as judged by 2 clinical experts and 1 methodologist. The clock starts at the original literature search date, not at publication. Limitations: 4 guidelines from one country; the strategy was not applied prospectively. The result agrees in direction with Shekelle et al. (JAMA 2001), which the verifier cited as background only. Together with the Shojania finding, this gives two independent clinical datasets showing silent loss of validity.

### W3 (medium; vote 3-0 ([4]; related interpretation in [6]))

Neither fixed review intervals nor features of the text predict when it becomes invalid. No feature of the original review significantly predicted an updating signal within 2 years, so the authors favour surveillance for new evidence over blanket schedules ('every two years will miss a substantial number of important signals'). This bears directly on expiry and re-review dates as a validity-tracking mechanism: a date-based signal misses early invalidation. [First-hand study finding plus the authors' recommendation.]

Sources: https://www.ncbi.nlm.nih.gov/books/NBK44099/ · https://pubmed.ncbi.nlm.nih.gov/17638714/ · https://www.cmaj.ca/content/early/2014/09/08/cmaj.140547

Evidence and qualifications: The AHRQ report's Results and Conclusions: features such as cardiovascular topic (HR 3.26 in AHRQ, 2.70 in Annals), heterogeneity (HR 2.23/2.15) and a new trial larger than the previous largest affected overall survival, but none predicted a signal within 2 years. The quantitative signal is checkable; the qualitative signals rest on judgment. The authors also say definitive recommendations on update frequency cannot be made and that frequent updating is costly. Medium because the recommendation rests on one study and the comparison of surveillance with intervals was not tested. Martinez Garcia's 3-year ceiling is consistent with it but likewise untested. Inference: date-based expiry is a signal that fails late rather than one tied to the dependency change.

### W4 (medium; vote 3-0 ([7],[8],[9]))

Evidence-synthesis fields have standardised currency signals recorded with the text, and these can fail. (1) Update status with a stated rationale ('No update planned' / 'Up to date' / 'Update pending'), assigned through a three-step framework: assess currency, identify new methods, studies or information, then assess the effect on findings or credibility. (2) Living systematic reviews show end users the date of the last search and that no new evidence was found, even when the content has not changed, under a working currency limit of at most six months, with most pilots searching at least monthly and publishing results within another month. The authors concede there is no empirical evidence on what currency end users need. [Standard / consensus methods guidance, not empirical evaluation.]

Sources: https://openaccess.sgul.ac.uk/108506/1/bmj.i3507.full.pdf · https://discovery.ucl.ac.uk/id/eprint/10025041/1/Thomas_LSR overview paper final - revised.pdf

Evidence and qualifications: Garner et al., 'When and how to update systematic reviews: consensus and checklist', BMJ 2016;354:i3507 (Fig 1 decision framework with Update status and Rationale columns). Elliott, Synnot, Turner ... Thomas, 'Living systematic review 1: Introduction', J Clin Epidemiol 2017 (author manuscript): 'it is important to make available to end users the date of last search and the information that no additional evidence was identified'; 'we propose ... a maximum of six months'. Both full texts were read. Qualifications: the BMJ paper says status and rationale are 'reported' but does not explicitly require them on the document itself. That the dated stamp 'fails visibly' as it ages is the claimant's inference, not tested. A related claim, that Cochrane applies update decisions informally and inconsistently, was refuted 0-3, so this run did not establish how consistently these signals are applied in practice.

### W5 (medium; vote 3-0 ([10],[11],[12]))

Assurance 2.0 gives the judgement behind a durable safety argument a status that can fail and be checked. Doubts are recorded as defeaters and each is developed into a subcase that confirms or refutes it. An unrefuted defeater stays 'active' and keeps the case 'open', unless it is explicitly accepted and justified as a residual risk. Unsupported claims and disconnected subarguments also keep the case open, and the Clarissa/ASCE tool propagates this status to the top claim. The authors' premise is that human judgement of a positive argument is fallible and prone to confirmation bias. Their remedy is skeptical debate, with aspects of it recorded for later developers and assessors. [Standard / method proposal from the method's authors; no empirical evaluation.]

Sources: https://www.csl.sri.com/~rushby/abstracts/defeaters24 · https://arxiv.org/abs/2405.15800

Evidence and qualifications: Bloomfield, Netkachova and Rushby, 'Defeaters and Eliminative Argumentation in Assurance 2.0', SRI-CSL-2024-01 / arXiv:2405.15800 (full text read). p.26: 'Unrefuted or true defeaters may be explicitly accepted and justified as residual risks; otherwise they are said to be active ... An assurance argument that has active defeaters or is incomplete ... is said to be open.' Medium: the source fully establishes what the method is, but whether it works is unstudied. Coverage gaps: only doubts someone records produce a signal (inference), and whether a subcase refutes a doubt still rests on human reading of narrative justifications. This partly cuts against the statement's 'no check that can fail': the mechanism exists for recorded doubts, while the reading inside it is not itself checked, which supports the statement's second sentence on that point.

### W6 (low; vote 3-0 ([13]))

In practice, peer or independent review is the dominant check on assurance-case text, and quantitative confidence methods are rarely used. All 19 interviewed practitioners had used review to gain confidence in an assurance case. Only 2 (11%) had used a quantitative confidence method on a real system, and 13 (68%) knew of such methods but had not used one. One practitioner said review is relied on 'probably more ... than I'm comfortable with'. [First-hand interview study.]

Sources: https://arxiv.org/pdf/2411.03657

Evidence and qualifications: Diemert, Shortt and Weber (University of Victoria), 'How do practitioners gain confidence in assurance cases?', arXiv:2411.03657, 2024 (full text read). Defeaters were also common (12/19, 63%), and 5/19 described deeper 'interrogation'-style review, so 'review' spans practices of very different depth. The sample is small and self-selected and the paper is a preprint. A companion claim from the same paper, that dialectic methods lack a stopping rule and practitioners name this as a barrier (support for 'review has no stopping rule'), was refuted 1-2. That statement claim is therefore not supported by verified evidence in this run.

### W7 (medium; vote 3-0 ([14],[15]))

In safety assurance, a change to the system, its operation or its environment can invalidate evidence and claims without making them visibly wrong. Evidence can reflect old artefacts or assumptions, and claims can become nonsense or be contradicted by new data. Change impact analysis is traditionally manual. [Expert assertion in a short position paper; not measured.]

Sources: https://arxiv.org/pdf/1404.6846

Evidence and qualifications: Jaradat, Graydon and Bate, 'An Approach to Maintaining Safety Case Evidence After A System Change', arXiv:1404.6846, 2014 (2 pages, full text read): 'This analysis is traditionally done by hand ...'; 'Evidence might no longer support the developers' claims because it reflects old development artefacts or old assumptions'. A verifier noted that the wider safety-case maintenance literature agrees, e.g. Kelly and McDermid 1999, cited from background only. Medium because the claim is conceptual and widely held, though this source measures nothing. The paper shows the invalidity goes unseen only when version and provenance information is not recorded, not that it must go unseen, which fits the statement's 'need not produce any signal'.

### W8 (low; vote 3-0 ([16]))

A mechanism, in the manner of make, has been proposed to give safety evidence a staleness signal that can fail. Each evidence element is annotated with an evidence version and an input manifest of artefact versions, and each artefact reference in a goal or context element with a version. A check flags evidence as out of date when a cited artefact is newer than its manifest records, and can also flag dependent goals. Later traceability tools reportedly mark elements as revise, recheck or reuse. [Standard/method proposal; the authors had not implemented or evaluated it.]

Sources: https://arxiv.org/pdf/1404.6846

Evidence and qualifications: Same paper, Section II and Related Work: 'We can identify out-of-date evidence by searching for input manifests ... such that ∃i • a = ai ∧ v > vi ... make does this. Our contribution lies in applying this idea to safety arguments'. The conclusion says feasibility and value were not studied. What it covers: dependency version changes, if annotations are kept current by hand. What it misses: whether a change actually invalidates the claim (a syntactic check that will produce false positives), transitive dependencies, and any dependency nobody annotated. GSN-IA, Kokaly et al. SAFECOMP 2017 and GAGE are leads only and were not read in full.

### W9 (medium; vote 3-0 ([17]))

Architecture documentation in industry drifts silently from the code, mostly by the documentation going stale rather than the code violating it. In three MunichRE C# systems (2-6 years old, 317-495 kLOC), 9-19% of implemented dependencies did not conform to the documented architecture. 72-90% of the mismatches were documentation flaws and 10-28% were code violations. The documentation, the code and individual developers' understanding each diverged from the intended architecture. [First-hand industrial case study.]

Sources: https://wwwbroy.in.tum.de/publ/papers/2009_icpc_feilkas.pdf

Evidence and qualifications: Feilkas, Ratiu and Juergens, 'The Loss of Architectural Knowledge during System Evolution: An Industrial Case Study', ICPC 2009 (full text read; Tables 2 and 5). Qualifications: System C's 19% is after a data-binding policy was added (42% before). Many documentation flaws came from insights during implementation, not later change. The intended architecture was reconstructed in developer interviews, which produced disagreement. The study covers one company and .NET only. Mapping this to 'loss of validity when a dependency changes' is inference. Project C developers knew the documentation was outdated, so the signal existed in people's heads, not in the text. A related claim that documentation went stale with no signal and became a 'dead artifact' was refuted 1-2, so the interview-based causal account is not verified here.

### W10 (low; vote 3-0 ([18]))

Counter-evidence for the mechanical part: making the documentation checkable fixed drift for what it covered. The architecture documentation was turned into a machine-checkable XML specification and checked nightly against the code. It stayed in sync for about a year in Project A, with setup taking about 5 days per project. The authors state the gap: where documentation and code agree but both differ from intent, the method detects nothing. [First-hand case study, informal follow-up.]

Sources: https://wwwbroy.in.tum.de/publ/papers/2009_icpc_feilkas.pdf

Evidence and qualifications: Same paper: 'The architecture description in XML form stayed up-to-date ... about a year in case of Project A'. The one-year result is unmeasured ('at least for the time we stayed in contact'), and Project A had only four architectural changes that year. Only structure and dependency rules became checkable; prose and rationale did not, and the check runs on a new formal artefact rather than on the text itself. Leads not read in full (Buckley et al. 2015 on Reflexion Modelling: fewer than 50% of violations removed after 4+ months, and practitioners preferring to change the model; reports of low adoption) suggest the result may not generalise. Supports a scoped reading of the statement: checks that can fail exist for the mechanical part, and the gap between text and intent remains.

### W11 (medium; vote 3-0 ([19]))

Design rationale is typically not documented ('knowledge vaporization'), so recovered decisions have no ground truth. RecovAr's recovered architectural decisions were judged by two PhD students on rationale clarity and cohesion and on consequence association and tractability, without consulting the original architects. This shows that the step from recovered text to its check is itself an unchecked reading. That a recovered reason cannot be told apart from a reconstructed one is inference. [First-hand study; the link to the statement is inference.]

Sources: https://www.cs.washington.edu/homes/brun/pubs/pubs/Shahbazian18icsa.pdf · https://people.cs.umass.edu/~brun/pubs/pubs/Shahbazian18icsa.pdf

Evidence and qualifications: Shahbazian, Lee, Le, Brun and Medvidovic, 'Recovering Architectural Design Decisions', ICSA 2018 (full text read via the UMass mirror; the cited UW URL returns 404). Section IV-B: 'architectural design decisions are not generally documented, hence a ground-truth for our analyses was not readily available ... Two PhD students carried out the analysis'; any criterion needing the original architects scored 0. Qualifications: the paper shows confirmation was not attempted, not that it is impossible. The recovered rationales come from issue-tracker text written at the time of the change, so they are partly records made at the time rather than pure reconstructions.

### W12 (medium; vote Synthesis of 3-0 claims [4],[7],[8],[10],[12],[16],[18])

Cross-cutting synthesis: the statement's claim that what a text says is 'generally held to no check that can fail' is contested, not established. Fields that rest on durable text have built signals that can fail: update status with rationale, 'last searched' dates and currency limits, defeater-driven open/closed status, version manifests, and conformance checks against a formalised specification. Each covers only (a) dependencies or doubts someone recorded, or (b) the part of the content that was made mechanical. Each depends on human upkeep or human reading at its core. None detects agreement between text and artefact where both have departed from intent. Where effectiveness was measured at all, it was measured informally. [Inference across the findings above.]

Sources: https://www.ncbi.nlm.nih.gov/books/NBK44099/ · https://openaccess.sgul.ac.uk/108506/1/bmj.i3507.full.pdf · https://discovery.ucl.ac.uk/id/eprint/10025041/1/Thomas_LSR overview paper final - revised.pdf · https://www.csl.sri.com/~rushby/abstracts/defeaters24 · https://arxiv.org/pdf/1404.6846 · https://wwwbroy.in.tum.de/publ/papers/2009_icpc_feilkas.pdf

Evidence and qualifications: The statement's own qualifier, 'generally', and its second sentence (the step from sentence to check is itself a reading that is rarely checked) survive. The categorical reading does not: several mechanisms give failable signals. Coverage gaps named in the sources themselves: Feilkas (documentation and code agree, both wrong), Jaradat (annotations kept by hand, syntactic only, unevaluated), Bloomfield (judgment of subcases is unchecked), Elliott (no evidence on the currency users need), Shojania (fixed intervals miss early signals). Martinez Garcia's validity was established only by an external exhaustive search; the claim that nothing in the text signalled it was refuted 1-2 as a reading of the abstract, so that point stays inference.

## Caveats (workflow)

Coverage is narrow relative to the brief. The 20 verified claims come from 7 sources and address mainly Q1 (names: systematic review updating, guideline validity, living systematic reviews, assurance cases and defeaters, safety case change impact analysis, architectural drift and knowledge vaporization), part of Q2 and Q3. Nothing was verified on: legal citators (Shepard's/KeyCite), retraction notices or the Retraction Watch database, citation distortion or illusory truth (Q4), model collapse, patient leaflet user testing and documentation acceptance criteria (Q5), detecting missing decisions (Q6), or LLM agents and knowledge conflicts (Q7). Absence of findings there means unstudied in this run, not refuted.

Several statement claims stay unsupported by verified evidence: 'review has no stopping rule' (the one supporting claim was refuted 1-2), 'the costly defects are mostly misrepresentations beneath the wording', 'agents make plausible text cheap', 'a defect propagates as knowledge' and 'an instruction cannot enforce itself'.

Source strength: the two Shojania sources are one study, so the 'high' rating on finding 1 rests on one dataset, corroborated in direction by Martinez Garcia. Most mechanism findings rest on single method or position papers by their own proponents, with no effectiveness data. The Feilkas, Diemert and RecovAr findings are each single studies with small or single-company samples.

Validity measures are operational proxies: a 'signal for updating' or a linked 'key reference' indicates a potential need to update, not a confirmed wrong conclusion. This matters for the 'not a real cost' disconfirming question. An unverified lead (Cochrane pregnancy reviews, PMID 20644625: conclusions revised in only 3.7% of updates) suggests many updates do not change conclusions, and it was not read in full.

Time sensitivity: the clinical cohorts date from 1995-2009 and the architecture study from 2009, before living reviews and LLM-generated text became common. They are valid as historical measurements but may not reflect current rates.

Several links from the sources to the problem statement's wording, e.g. 'fails visibly' and 'recovered vs reconstructed', are labelled inference.

## Open questions (workflow)

- Do the mechanisms that give a text a signal that can fail (update-status labels, last-searched dates, defeater open/closed status, version manifests, conformance checks) reduce how often readers act on invalid text, and how often do the signals themselves go stale or prove wrong? None of the verified sources measured this.
- How often does a validity signal correspond to a material change in what a reader should do? Shojania and Martinez Garcia measure potential need to update, and the unverified Cochrane lead suggests few updates change conclusions. This decides whether silent invalidation is a large real cost or mostly a nominal one.
- Do legal citators, retraction databases and assurance-case confidence arguments catch the case these sources leave uncovered, where the text and its dependency agree with each other but both depart from intent or truth? Is there first-hand evidence on how far unfounded claims propagate through derived texts?
- How do LLM agents treat superseded or contradictory durable text and rationale they reconstruct themselves (the brief's Q7)? Can an agent used as a verifier grounded outside the text reach a check that can fail, beyond the mechanical part?

## Sources fetched

| URL | quality | angle | claims |
|---|---|---|---|
| https://pubmed.ncbi.nlm.nih.gov/17638714/ | primary | Validity tracking for durable text in other fields (living reviews, guideline expiry, legal citators) | 5 |
| https://www.ncbi.nlm.nih.gov/books/NBK44099/ | primary | Validity tracking for durable text in other fields (living reviews, guideline expiry, legal citators) | 5 |
| https://www.cmaj.ca/content/early/2014/09/08/cmaj.140547 | primary | Validity tracking for durable text in other fields (living reviews, guideline expiry, legal citators) | 4 |
| https://openaccess.sgul.ac.uk/108506/1/bmj.i3507.full.pdf | primary | Validity tracking for durable text in other fields (living reviews, guideline expiry, legal citators) | 5 |
| https://www.llrx.com/2019/04/is-it-a-good-case-can-you-rely-on-bcite-keycite-and-shepards-to-tell-you/ | secondary | Validity tracking for durable text in other fields (living reviews, guideline expiry, legal citators) | 5 |
| https://discovery.ucl.ac.uk/id/eprint/10025041/1/Thomas_LSR overview paper final - revised.pdf | primary | Validity tracking for durable text in other fields (living reviews, guideline expiry, legal citators) | 5 |
| https://www.csl.sri.com/~rushby/abstracts/defeaters24 | primary | Assurance cases, defeaters and design rationale decay | 5 |
| https://arxiv.org/pdf/2411.03657 | primary | Assurance cases, defeaters and design rationale decay | 5 |
| https://arxiv.org/pdf/1404.6846 | primary | Assurance cases, defeaters and design rationale decay | 5 |
| https://wwwbroy.in.tum.de/publ/papers/2009_icpc_feilkas.pdf | primary | Assurance cases, defeaters and design rationale decay | 5 |
| https://www.cs.washington.edu/homes/brun/pubs/pubs/Shahbazian18icsa.pdf | primary | Assurance cases, defeaters and design rationale decay | 5 |
| https://arxiv.org/pdf/2607.06039 | primary | Assurance cases, defeaters and design rationale decay | 5 |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656/ | primary | Propagation of unfounded claims via citation, retraction and generated text | 5 |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9520488/ | primary | Propagation of unfounded claims via citation, retraction and generated text | 5 |
| https://www.pure.ed.ac.uk/ws/portalfiles/portal/460496122/ShumailovEtalNature2024AIModelsCollapseWhen.pdf | primary | Propagation of unfounded claims via citation, retraction and generated text | 5 |
| https://arxiv.org/abs/2404.01413 | primary | Propagation of unfounded claims via citation, retraction and generated text | 5 |
| https://arxiv.org/abs/2505.05410 | primary | LLM agents reading stale, conflicting or rationalised text (first-hand) | 5 |
| https://arxiv.org/abs/2503.08679 | primary | LLM agents reading stale, conflicting or rationalised text (first-hand) | 5 |
| https://arxiv.org/abs/2403.08319 | secondary | LLM agents reading stale, conflicting or rationalised text (first-hand) | 5 |
| https://aclanthology.org/2026.eacl-long.310 | primary | LLM agents reading stale, conflicting or rationalised text (first-hand) | 5 |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3152894/ | primary | Acceptance testing of text and disconfirming evidence | 5 |
| https://eprints.whiterose.ac.uk/128038/1/European%20Public%20Assessment%20Report%20%28EPAR%29%20summaries%20for%20the%20public%3A%20are%20they%20fit%20for%20purpose%3F%20A%20user-testing%20study.pdf | primary | Acceptance testing of text and disconfirming evidence | 5 |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11507276/ | secondary | Acceptance testing of text and disconfirming evidence | 5 |
| https://courses.cs.duke.edu//cps196.1/fall11/classwork/Lethbridge-Singer-Forward-2003.pdf | primary | Acceptance testing of text and disconfirming evidence | 5 |

## Stats

```
{
 "angles": 5,
 "sourcesFetched": 24,
 "claimsExtracted": 119,
 "claimsVerified": 25,
 "confirmed": 20,
 "killed": 5,
 "unverified": 0,
 "afterSynthesis": 12,
 "urlDupes": 0,
 "budgetDropped": 6,
 "agentCalls": 106
}
```
