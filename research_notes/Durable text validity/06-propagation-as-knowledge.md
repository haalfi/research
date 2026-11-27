# Track t06: Propagation of unfounded claims as knowledge (Q4; C7, C6)

Track question: how does an unfounded claim become accepted knowledge through derived texts, repetition or
generated text, and what has been *shown* to stop it? Mechanisms of spread are kept apart from measured
countermeasures. All figures below are quoted from the text read; locators given.

## 1. Scope and searches run

Retrieval: arXiv PDFs, Europe PMC full-text XML, author/institutional PDFs (NSF PAR, USC, EPFL, MIT IDE, usask,
UPenn), pdftotext; WebFetch for one PMC page (captcha blocks curl). Searches (WebSearch, standard):
- Brashier Eliseev Marsh "An initial accuracy focus prevents illusory truth" pdf
- Fazio Brashier Payne Marsh 2015 "Knowledge does not protect against illusory truth" pdf
- Dechêne et al. 2010 "The truth about the truth" meta-analysis pdf
- Walter & Tukachinsky 2020 continued influence meta-analysis pdf; same with "repeated" "time lag" full text
- Ecker et al. 2022 "psychological drivers of misinformation belief" pdf
- Lewandowsky et al. 2012 "Misinformation and its correction" pdf
- Zhang et al. "empirical study of obsolete answers on Stack Overflow" pdf
- Fischer et al. "Stack Overflow Considered Harmful?" pdf
- Kumar, West, Leskovec Wikipedia hoaxes pdf; Priedhorsky "Creating, destroying, and restoring value in Wikipedia"
- Thompson & Hanley "Science is shaped by Wikipedia" pdf
- citogenesis empirical study Wikipedia circular reporting
- Furman, Jensen, Murray retractions citations decline; Hsiao & Schneider 2021 continued use of retracted papers
- LLM-generated unit tests assert buggy behaviour regression oracle (excluding Konstantinou, already covered)
- Mondal et al. bug propagation through code cloning pdf
- illusory truth effect domain experts expertise protect
Direct downloads (no search): arXiv 2305.13534, 2410.08044, 2404.01268, 2109.07958, 2307.02394, 2212.10003,
1910.01321, cond-mat/0212043, 2404.01413, 2310.20501, 2305.13661, 2303.11455, 2306.03438, 1806.07659, 2310.13548,
2305.17493, 1903.12282, 1710.03135, 1901.01327, 2607.22883, 2610.11835, 2601.05542; PMC2714656, PMC4627914,
PMC5599002, PMC4232290, PMC9166874, PMC11269175, PMC10484980.

## 2. Findings

### A. Derived text: citation as a propagation channel (mechanisms)

- **Claim: citation alone can turn a hypothesis into "fact"; a citation network can build authority for a claim
  its primary data do not support.** Greenberg SA (2009) "How citation distortions create unfounded authority:
  analysis of a citation network", BMJ 339:b2680. https://europepmc.org/article/PMC/PMC2714656
  TYPE first-hand study (single-claim case, n=242 papers, 675 citations). ACCESS full text read.
  Locator: Abstract: "Unfounded authority was established by citation bias against papers that refuted or weakened
  the belief; amplification, the marked expansion of the belief system by papers presenting no data addressing it;
  and forms of invention such as the conversion of hypothesis into fact through citation alone." Results: "The
  supportive papers received 94% of the 214 citations to these primary data, whereas the six papers containing data
  that weakened or refuted the claim received only 6%." Fig 3 caption: eight key papers (seven from one group)
  through which "97% of all network traffic passes". Discussion: animal models built on the claim "can then be
  circularly used to amplify claim"; the same distortions recur in NIH-funded grant text (FOIA). Detection: Fig 6
  says finding authorities/amplification "require only computational algorithms", but identifying which papers hold
  data and identifying invention "requires careful reading of paper content".
  Bearing: strong FOR C7 (an inference recorded once is later read as fact; derived work agrees with it; network
  consistency grows while the evidential base does not). Also C1 (citation resolves but the claim is unchecked).

- **Claim: most citers copy references rather than consult the source.** Simkin MV, Roychowdhury VP (2003)
  "Read before you cite!", arXiv cond-mat/0212043 (Complex Systems 14, 2003). TYPE first-hand study (model fitted to
  misprint propagation). ACCESS full text read. Locator: Abstract: "Our estimate is only about 20% of citers read the
  original"; Fig 1: of 196 misprints in citations to one paper, 45 distinct; "The most popular misprint propagated 78
  times"; later refined model gives "R ≈ 0.17". Note the generous definition of "reader" (consulted a trusted
  source). Bearing: FOR C7/C6 (copying derived text without returning to the source is the norm); identical-misprint
  propagation is itself a detectable signature of copying.

- **Claim: quotation (content) errors in citations are common.** Jergas H, Baethge C (2015) "Quotation accuracy in
  medical journal articles—a systematic review and meta-analysis", PeerJ 3:e1364. PMC4627914. TYPE review/secondary
  (meta-analysis of 28 studies). ACCESS full text read. Locator: Abstract Results: "major, minor and total
  quotation error rates of 11,9%, 95% CI [8.4, 16.6] 11.5% [8.3, 15.7], and 25.4% [19.5, 32.4]"; "Indirect
  references accounted for less than one sixth of all quotation problems"; heterogeneity large (I² up to 98%).
  Mogull SA (2017) "Accuracy of cited 'facts' in medical research articles: A review of study methodology and
  recalculation of quotation error rate", PLoS ONE 12:e0184727. PMC5599002. TYPE review/secondary. ACCESS full text
  read. Locator: Results/Table 4: primary analysis "14.5 (Content Errors)" (10.5% to 18.6% 95% CI); "Of the content
  errors, 64.8% ... are major errors"; improper secondary citation rate 10.4%. Bearing: FOR C2 (misrepresentation
  with a resolving reference) and C1 (reference checks pass while content is wrong). Note the two reviews disagree on
  the rate (25.4% vs 14.5%) mainly through inclusion criteria; both are substantial.

- **Claim: "academic urban legends" spread via secondary sources and grow an impressive but circular reference
  list.** Rekdal OB (2014) "Academic urban legends", Social Studies of Science 44(4):638–654. PMC4232290. TYPE
  first-hand case study (historical tracing). ACCESS full text read. Locator: traces the spinach decimal-point story
  to Hamblin (1981, BMJ), who "does not provide a reference to support his claim"; asked later, Hamblin "could not
  remember, but ... was sure he had not made it up" (via Sutton 2010). Describes citing many secondary sources that
  "all refer back to the same single sentence", an "academic confidence trick" not exposed "until readers took the
  time to look up the sources". Bearing: FOR C7 (a debunking story itself became an unfounded legend; repetition
  across reputable venues produced apparent corroboration). Single case; mechanism not quantified.

- **Claim: retraction does not stop citation; almost no later citing text records the retraction.** Hsiao T-K,
  Schneider J (2021) "Continued use of retracted papers...", Quantitative Science Studies 2(4):1144–1169.
  PMC9520488. TYPE first-hand study (7,813 retracted papers; 13,252 post-retraction citation contexts). ACCESS full
  text read (via fetch tool; PMC blocks curl). Locator: Abstract: "only 722 (5.4%) citation contexts acknowledged
  the retraction"; "retraction did not change the way the retracted papers were cited"; "old retracted papers
  stopped being cited as time progressed"; §5: "the vast majority (94.6%) of postretraction citations did not
  document the retraction". Bearing: FOR C2 (lost validity produces no signal in derived text) and C7; partial
  AGAINST (slow decay of citation to old retracted papers is a weak self-correction).

- **Claim: retraction causes a large citation decline.** Furman JL, Jensen K, Murray F (2012) Research Policy
  41(2):276–290. TYPE first-hand study. ACCESS abstract/record only (MIT DSpace returned 429; CORE 403). A secondary
  blog gives "65%" decline; not verified, not reported as a finding here. Bearing: potential AGAINST C7 (formal
  retraction works partially); unverified.

- **Claim: encyclopedia text propagates into the scientific literature without citation.** Thompson N, Hanley D
  (2017/2018) "Science is shaped by Wikipedia: evidence from a randomized control trial", MIT Sloan WP / SSRN
  3039505. https://ide.mit.edu/wp-content/uploads/2017/10/SSRN-id3039505.pdf TYPE first-hand study (RCT: new
  chemistry articles randomly added to Wikipedia or withheld). ACCESS full text read (2017 version). Locator:
  Abstract: "Wikipedia influencing roughly one in every three hundred words in related scientific journal articles"
  (a later version is reported with a different figure; I read only the 2017 version). Introduction: the effect is
  "largely absent" from academic citations. Bearing: FOR C7 mechanism (a derived, uncited text shapes primary
  literature: the channel citogenesis needs). Not a measure of error propagation.

- **Citogenesis / circular reporting (Wikipedia → press → Wikipedia).** Search found only the Wikipedia list of
  incidents, xkcd 978 (coinage, 2011) and journalism. TYPE practitioner report. ACCESS not used as evidence. No
  empirical prevalence study found (see §4).

### B. Repetition (mechanisms and measured countermeasures)

- **Claim: repetition raises perceived truth even when the reader knows the correct answer.** Fazio LK, Brashier NM,
  Payne BK, Marsh EJ (2015) "Knowledge does not protect against illusory truth", JEP: General 144(5):993–1002.
  https://typeset.io/pdf/knowledge-does-not-protect-against-illusory-truth-4e11jui99s.pdf (third-party copy of the
  published PDF). TYPE first-hand study. ACCESS full text read. Locator: Abstract: "illusory truth effects occurred
  even when participants knew better. Multinomial modeling demonstrated that participants sometimes rely on fluency
  even if knowledge is also available"; Exp. 1 results: "knowledge did not interact with repetition"; the
  fluency-conditional model fit "G2 (df = 3) = 2.54, p = .47". Intro on expertise: Srull (1983) experts showed a
  "numerically smaller" effect (no statistics); Arkes, Hackett & Boehm (1989) found "expertise increased
  susceptibility". Bearing: FOR C7 (repetition of a derived claim adds credence independent of evidence); against
  the disconfirming hypothesis that knowledgeable readers are immune.

- **Claim: the evidence base for illusory truth is narrow (trivia, single session).** Henderson EL, Westwood SJ,
  Simons DJ (2022) "A reproducible systematic map of research on the illusory truth effect", Psychonomic Bulletin &
  Review 29:1065–1088. PMC9166874. TYPE review/secondary. ACCESS full text read. Locator: Results: "trivia statements
  (135 or 75%)"; "almost all studies (167 or 92%) used a single session and ... one exposure (173 or 96%)"; notes
  prior knowledge "does not provide total protection from the effect". Also reports (search lead) that the Dechêne
  2010 coded data could not be obtained (not located in my read; treat as lead). Bearing: tempers external validity
  of the repetition evidence for durable-text settings with expert, repeated, task-driven reading (contested scope).

- **Measured countermeasure: an initial accuracy focus prevents illusory truth, but only for known facts.** Brashier
  NM, Eliseev ED, Marsh EJ (2020) "An initial accuracy focus prevents illusory truth", Cognition 194:104054. Author
  manuscript https://par.nsf.gov/servlets/purl/10190136. TYPE first-hand study (4 experiments). ACCESS full text read.
  Locator: Abstract: "Focusing on accuracy at exposure (giving initial truth ratings) wiped out the illusion later,
  but only when participants held relevant knowledge. This selective benefit persisted over a delay"; Exp. 4: two-day
  delay; General Discussion: "illusory truth only occurred for unknown items, where participants had no knowledge to
  activate". Bearing: the one measured stop for repetition, and it requires that the reader already holds the
  correct knowledge and evaluates at first exposure. For durable text where the reader lacks the ground truth
  (the usual case for a decision or a reason), it does not apply (inference).

- **Dechêne et al. (2010) meta-analysis, PSPR 14(2):238–257.** ACCESS abstract/record only (no legitimate open copy
  found). Effect size d = .39 appears only in a search extract; not reported as verified.

### C. Correction of misinformation (continued influence; measured countermeasures)

- **Claim: retractions reduce but rarely eliminate reliance on misinformation; three measured aids.** Lewandowsky S,
  Ecker UKH, Seifert CM, Schwarz N, Cook J (2012) "Misinformation and its correction: continued influence and
  successful debiasing", PSPI 13(3):106–131. https://dornsife.usc.edu/norbert-schwarz/wp-content/uploads/sites/231/2023/11/12_pspi_lewandowsky_et_al_misinformation.pdf
  TYPE review/secondary. ACCESS full text read. Locator: "retractions rarely, if ever, have the intended effect of
  eliminating reliance on misinformation"; three remedies: "(a) ... be warned about the potentially misleading
  nature of forthcoming information before it is presented; (b) corrections can be repeated to strengthen their
  efficacy; and (c) corrections can be accompanied by alternative explanations ... thus preventing causal gaps";
  caveat that repeated retractions "do not further reduce reliance on weakly encoded misinformation".
- **Ecker UKH, Lewandowsky S, Cook J, et al. (2022) "The psychological drivers of misinformation belief and its
  resistance to correction", Nature Reviews Psychology 1:13–29.** Published PDF via
  https://typeset.io/pdf/the-psychological-drivers-of-misinformation-belief-and-its-2x2d8re6.pdf (nature.com
  paywalled; CORE AAM 403). TYPE review/secondary. ACCESS full text read. Locator: Debunking section: "direct
  corrections are effective in reducing — although frequently not eliminating — reliance on the misinformation";
  "The beneficial effects of debunking can last several weeks ... although the effects can wear off quicker";
  Practical implications: "no intervention can be fully effective or reach everyone"; "simple retractions will be
  insufficient"; an alternative explanation that is "causal, plausible, simple and memorable" reduces recall of the
  retracted claim. Box 2: familiarity backfire "does not typically" occur; "explicit reminders of misinformation
  enhance the effect of corrections"; worldview backfire "limited". Bearing: corrections are a measured, partial
  stop; a correction that names the error and supplies the replacement works better than a bare retraction (maps to
  a supersession record that says what replaces what, inference).
- **Walter N, Tukachinsky R (2020) meta-analysis, Communication Research 47(2):155–177.** ACCESS abstract only
  (Chapman repository 403). Abstract (search extract): 32 studies, N = 6,527, correction "does not entirely
  eliminate the effect of misinformation"; less effective when the misinformation came from a credible source, was
  repeated before correction, or after a time lag. Not verified; reported as lead.
- **Claim (disconfirming of correction efficacy): debunking science-relevant misinformation was on average not
  successful.** Chan MS, Albarracín D (2023) "A meta-analysis of correction effects in science-relevant
  misinformation", Nature Human Behaviour (2023), doi 10.1038/s41562-023-01623-8 (volume/pages not checked). https://asc.upenn.edu/sites/default/files/2023-06/A%20meta-analysis%20of%20correction%20effects%20in%20science-relevant%20misinformation.pdf
  TYPE review/secondary (205 effect sizes, 74 reports, N = 60,861). ACCESS full text read (accepted version).
  Locator: Abstract: "attempts to debunk science-relevant misinformation were, on average, not successful (d = 0.19,
  P = 0.131, 95% confidence interval −0.06 to 0.43)"; corrections fared better "when they were detailed". Bearing:
  FOR C7 (once accepted, scientific-looking claims resist correction); against any assumption that correction
  restores validity.

### D. Generated text (mechanisms)

- **Claim: a model commits to an early error and generates further false claims to stay consistent with it, though
  it can recognise those claims as false in isolation.** Zhang M, Press O, Merrill W, Liu A, Smith NA (2023/2024)
  "How language model hallucinations can snowball", arXiv 2305.13534 (later venue not checked). TYPE first-hand study. ACCESS full
  text read. Locator: Abstract: "ChatGPT and GPT-4 can identify 67% and 87% of their own mistakes, respectively";
  §3.4: average accuracy ChatGPT "39.87%", GPT-4 "16.6%"; §4.1 with "Let's think step by step" GPT-4 "still has a
  high overall snowballed hallucination rate at 94.90% averaged across tasks"; §4.2 temperature 0.6/0.9 leaves rates
  "similarly high". Bearing: strong FOR C7 at the level of one generation (internal consistency with prior output
  outranks correctness) and C6 (a plausible justification is generated for an unfounded commitment). Measured
  partial stop: checking each claim in a separate context (fresh session) catches most snowballed claims.
- **Claim: indiscriminate training on generated data causes irreversible loss of the tails of the original
  distribution.** Shumailov I, Shumaylov Z, Zhao Y, Papernot N, Anderson R, Gal Y (2024) "AI models collapse when
  trained on recursively generated data", Nature 631:755–759. PMC11269175. TYPE first-hand study. ACCESS full text
  read. Locator: Abstract: "indiscriminate use of model-generated content in training causes irreversible defects
  ... tails of the original content distribution disappear"; LLM experiment: "preservation of the original data
  allows for better model fine-tuning and leads to only minor degradation"; Discussion: provenance "it is unclear how
  content generated by LLMs can be tracked at scale". Bearing: FOR C7 analogue (outputs become narrower, more
  self-similar, i.e. more consistent, while fidelity falls).
- **Disconfirming / measured countermeasure: accumulating real and synthetic data avoids collapse.** Gerstgrasser M,
  Schaeffer R, et al. (2024) "Is model collapse inevitable? Breaking the curse of recursion by accumulating real and
  synthetic data", arXiv 2404.01413. TYPE first-hand study (+ theory). ACCESS full text read. Locator: Abstract:
  "replacing the original real data by each generation's synthetic data does indeed tend towards model collapse,
  then demonstrate that accumulating the successive generations of synthetic data alongside the original real data
  avoids model collapse"; linear model: "test error has a finite upper bound independent of the number of
  iterations". Bearing: AGAINST an unconditional C7 reading; the stop is retaining the original (ground) source
  alongside derived material. Maps to "keep the primary record and never replace it with derived text" (inference).
- **Claim: models reproduce popular misconceptions learned from human text; larger models were less truthful.** Lin
  S, Hilton J, Evans O (2022) "TruthfulQA", ACL 2022, arXiv 2109.07958. TYPE first-hand study (benchmark). ACCESS
  full text read. Locator: Abstract: "The best model was truthful on 58% of questions, while human performance was
  94%"; "The largest models were generally the least truthful". Bearing: FOR C7 (repetition in the corpus becomes
  the model's "knowledge"). Dated models (GPT-3 era).
- **Claim: models accept false premises in the question.** Kim N, Htut PM, Bowman SR, Petty J (2023) "(QA)²:
  Question answering with questionable assumptions", ACL 2023, arXiv 2212.10003. TYPE first-hand study. ACCESS full
  text read. Locator: §1: best models "at 56% human-judged abstractive QA acceptability, and 64% and 72% on the
  binary classification subtasks of questionable assumption detection and verification". Hu S et al. (2023) "Won't
  get fooled again: answering questions with false premises", ACL 2023, arXiv 2307.02394 (FalseQA, 2,365 FPQs).
  ACCESS full text read. Locator: Abstract: PLMs "already possess the knowledge required to rebut such questions";
  they "are capable of discriminating FPQs by fine-tuning on moderate numbers (e.g., 256) of examples". Bearing: FOR
  C6 (an agent answers inside the premise it was given, e.g. a text's unfounded assumption); measured stop exists
  but is training-time and benchmark-bound.
- **Claim: assistants defer to a user's stated belief and repeat the user's mistakes.** Sharma M et al. (2024)
  "Towards understanding sycophancy in language models", ICLR 2024, arXiv 2310.13548. TYPE first-hand study. ACCESS
  full text read. Locator: §3.3: "The user suggesting an incorrect answer can reduce accuracy by up to 27% (LLaMA 2)";
  §3.2: "Claude 1.3 wrongly admits mistakes on 98% of questions"; §3.4: with a misattributed poem the assistants
  "frequently provide responses that use the incorrect attribution" though they can attribute correctly. Bearing:
  FOR C6/C7 (a premise in the input, such as a recorded inference, is carried forward rather than checked).
- **Claim: LLM-generated text enters Wikipedia; flagged pages are lower quality.** Brooks C, Eggert S, Peskoff D
  (2024) "The rise of AI-generated content in Wikipedia", arXiv 2410.08044 (venue not checked). TYPE first-hand study.
  ACCESS full text read. Locator: §5: "we estimate that 4.36% of 2,909 English Wikipedia articles created in August
  2024 contain significant AI-generated content" (thresholds at ≤1% FPR on pre-March-2022 pages); "AI-generated ones
  use fewer references and are less integrated"; "Most of the 45 pages are flagged by moderators and bots with some
  warning"; §5.4: an AI article "can be translated and propagated into other languages". Bearing: FOR C6
  (accumulation of plausible text); partial AGAINST (community flags and deletes many such pages). Detector-based
  lower bound.
- **Claim: LLM-modified prose is widespread in papers.** Liang W et al. (2024) "Mapping the increasing use of LLMs in
  scientific papers", arXiv 2404.01268 (venue not checked). TYPE first-hand study (950,965 papers). ACCESS full text read.
  Locator: Abstract: "largest and fastest growth observed in Computer Science papers (up to 17.5%)"; Mathematics and
  Nature portfolio "up to 6.3%". Bearing: C6 prevalence only; says nothing about whether the modified content is
  wrong.
- **Claim: LLMs fabricate references, a direct route to invented authority.** Walters WH, Wilder EI (2023)
  "Fabrication and errors in the bibliographic citations generated by ChatGPT", Scientific Reports 13:14045.
  PMC10484980. TYPE first-hand study. ACCESS full text read. Locator: Abstract: "55% of the GPT-3.5 citations but
  just 18% of the GPT-4 citations are fabricated. Likewise, 43% of the real (non-fabricated) GPT-3.5 citations but
  just 24% of the real GPT-4 citations include substantive citation errors." Bearing: FOR C6 (invented support that
  later reads as recorded authority, cf. Greenberg's "invention").
- **Claim: neural retrievers rank LLM-generated documents above human ones ("source bias").** Dai S et al. (2024)
  "Neural retrievers are biased towards LLM-generated content", KDD 2024, arXiv 2310.20501. TYPE first-hand study.
  ACCESS full text read. Locator: Abstract: "neural retrieval models tend to rank LLM-generated documents higher";
  extends to re-rankers; a "debiased constraint" mitigates it "in different degrees". Bearing: FOR C6/C7 mechanism
  (generated text is preferentially found by the next agent).
- **Claim: LLM-generated misinformation in a corpus degrades downstream QA; defences are partial.** Pan Y et al.
  (2023) "On the risk of misinformation pollution with large language models", Findings EMNLP 2023, arXiv
  2305.13661. TYPE first-hand study. ACCESS full text read. Locator: Abstract: "significant degradation (up to 87%) in
  the performance of ODQA systems"; §4: drops "from 14% to 54% for DPR-based models and ... from 20% to 87% for
  BM25-based models"; §5: in-domain detectors "consistently deliver high AUROC" but assume the generator is known;
  vigilant prompting "yielded inconsistent outcomes"; voting "necessitates additional resources". Bearing: FOR C6/C7;
  shows the shape of measured countermeasures (detector, prompt instruction, redundancy) and that the text-only
  instruction is the weakest (relevant to C8, inference).

### E. Software analogue (derived code and tests)

- **Claim: insecure Q&A snippets propagate into production apps; security warnings in comments did not reduce
  copying.** Fischer F, Böttinger K, Xiao H, Stransky C, Acar Y, Backes M, Fahl S (2017) "Stack Overflow considered
  harmful? The impact of copy&paste on Android application security", IEEE S&P 2017, arXiv 1710.03135. TYPE
  first-hand study. ACCESS full text read. Locator: Abstract: "15.4% of the 1.3 million Android applications we
  analyzed, contained security-related code snippets from Stack Overflow. Out of these 97.9% contain at least one
  insecure code snippet." §V "Impact on copy and paste" / Table X: higher score and view count go with more copying;
  "Snippets that have been commented with security warnings are copied more often into applications than those
  without"; top offending snippet "copied 180,388 times despite of being commented with warnings". Bearing: strong
  FOR C7 and C8 (a textual warning attached to the text did not stop propagation; correlational).
- **Claim: community signals (score, views, reputation) do not separate secure from insecure advice.** Chen M,
  Fischer F, Meng N, Wang X, Grossklags J (2019) "How reliable is the crowdsourced knowledge of security
  implementation?", ICSE 2019, arXiv 1901.01327. TYPE first-hand study. ACCESS full text read. Locator: Abstract:
  "insecure ones had higher view counts (36,508 vs. 18,713), received a higher score (14 vs. 5), and had
  significantly more duplicates (3.8 vs. 3.0) on average. 34% of the posts provided by highly reputable so-called
  trusted users were insecure." Bearing: FOR C7 (popularity and duplication grow while correctness does not);
  AGAINST reliance on reputation or voting as a validity signal.
- **Measured countermeasure: nudges at the point of reuse.** Fischer F, Xiao H, Kao C-Y, Stachelscheid Y, Johnson B,
  Razar D, Fawkesley P, Buckley N, Böttinger K, Muntean P, Grossklags J (2019) "Stack Overflow considered helpful!
  Deep learning security nudges towards stronger cryptography", USENIX Security 2019.
  https://www.usenix.org/system/files/sec19-fischer.pdf TYPE first-hand study (classifier + user study). ACCESS full
  text read. Locator: Abstract: "For 99.37% of insecure code examples on Stack Overflow, similar alternatives are
  available"; classifier "AUC-ROC of 0.992"; §user study: "nudged participants provided significantly more secure
  solutions, while achieving the same level of functionality as the control group". Bearing: a measured stop that
  acts when the reader is about to reuse text, by ranking and pointing to a validated alternative, not by adding a
  warning sentence. Lab study; agents not measured.
- **Claim: vulnerable C++ snippets migrate to GitHub and are rarely fixed downstream.** Verdi M, Sami A, Akhondali J,
  Khomh F, Uddin G, Karami Motlagh A (2020) "An empirical study of C++ vulnerabilities in crowd-sourced code
  examples", IEEE TSE, arXiv 1910.01321. TYPE first-hand study. ACCESS full text read. Locator: Abstract: of 72,483
  reviewed snippets used on GitHub, 99 vulnerable; "reused in a total of 2859 GitHub projects"; "Many ... are still
  not corrected on Stack Overflow"; RQ2.2: "Among the 287 GitHub files that we checked, vulnerabilities were
  corrected in 34 files and the other 253 GitHub files still had vulnerabilities". A warning browser extension was
  built; no user evaluation found in the text. Bearing: FOR C2/C7 (copies diverge from any later fix of the source).
- **Claim: Q&A answers go stale without signal and are seldom updated.** Zhang H, Wang S, Chen T-H, Zou Y, Hassan AE
  (2021) "An empirical study of obsolete answers on Stack Overflow", IEEE TSE 47(4), arXiv 1903.12282. TYPE
  first-hand study. ACCESS full text read. Locator: Abstract: "More than half of the obsolete answers (58.4%) were
  probably already obsolete when they were first posted"; "When an obsolete answer is observed, only a small
  proportion (20.5%) of such answers are ever updated"; §4: "44.1% of the studied obsolete answers are the accepted
  answers"; upper bound "49.8% ... were either updated ... or added with new answers". Bearing: FOR C2 (validity lost
  through a dependency change) and AGAINST "self-correction is fast" for Q&A. Obsolescence here is identified from
  user comments, so the observed set is those someone noticed.
- **Claim: code copied to Q&A goes outdated; notified answerers often do not fix.** Ragkhitwetsagul C, Krinke J,
  Paixao M, Bianco G, Oliveto R (2019) "Toxic code snippets on Stack Overflow", IEEE TSE, arXiv 1806.07659. TYPE
  first-hand study (surveys + clone detection). ACCESS full text read. Locator: Abstract: "131 participants (65%) have
  ever been notified of outdated code and 26 of them (20%) rarely or never fix the code"; of 153 clones copied from
  Qualitas projects to Stack Overflow "100 of them (66%) to be outdated, of which 10 were buggy". Bearing: FOR C2/C6
  (copies of one fact diverge; notification is not resolution, cf. C5 finding ≠ resolving).
- **Claim: code cloning propagates bugs.** Mondal M, Roy B, Roy CK, Schneider KA (2019) "An empirical study on bug
  propagation through code cloning", JSS 158:110407. Preprint https://clones.usask.ca/pubfiles/articles/MMondalBugProposationJSS.pdf
  TYPE first-hand study (7 systems). ACCESS full text read (preprint). Locator: Abstract: "overall 18.42% of the
  clone fragments that experience bugfixes contain propagated bugs"; more likely for clones "created in the same
  commit". Bearing: FOR C7 (derived copies carry the defect).
- **Claim: code LLMs reproduce known bugs.** Jesse K, Ahmed T, Devanbu PT, Morgan E (2023) "Large language models and
  simple, stupid bugs", MSR 2023, arXiv 2303.11455. TYPE first-hand study. ACCESS full text read. Locator: Abstract:
  Codex "do[es] produce known, verbatim SStuBs as much as 2x as likely than known, verbatim correct code"; Intro:
  SStuB fixes "take around 240 days". Dinh T et al. (2023) "Large language models of code fail at completing code
  with potential bugs", NeurIPS 2023, arXiv 2306.03438. ACCESS full text read. Locator: Abstract: passing rates of
  CodeGen-2B-mono "drop more than 50% given a single potential bug in the context"; post-hoc mitigations leave "a
  significant gap". Bearing: FOR C7 (a defect in context or corpus is continued rather than corrected).
- **Claim: LLM-generated tests prompted with buggy code assert the bug, and the effect is measurable.** Zhao J, Zhou
  S, Cohen E (2026) "Evaluating and mitigating the misguidance effect of buggy code in LLM-generated unit tests",
  Proc. ACM Softw. Eng. 3 (ISSTA 2026), arXiv 2607.22883. TYPE first-hand study. ACCESS full text read. Locator: RQ1
  results table "Total Average": misguided tests (assert incorrect behaviour) 137.69 (3.84%) with buggy code vs 16.46
  (0.46%) with fixed code; effective (bug-revealing) tests "104.15 on average (2.98%) when prompted with buggy code.
  When given the corresponding fixed code, this rises to 304.08 (8.51%), nearly a threefold increase." Measured
  countermeasure: two-step "specification-based" prompting (LLM derives a docstring of intended behaviour, which
  then replaces the code in the test prompt) "significantly reduces misguided tests while improving bug-detection
  rates"; it also "blocks bug propagation into generated docstrings ... for a considerable fraction". Bearing: FOR C7
  (tests derived from the artifact agree with its defect); the stop is to derive the check from a statement of
  intent rather than from the implementation, which only partly works when that statement is itself derived.
- **Claim: fault-enforcing LLM regression tests persist and accumulate across project evolution.** Charoosaei M,
  Richter C, Papadakis M (2026) "On the risks of using LLM-generated tests for regression testing", arXiv 2610.11835.
  TYPE first-hand study (145 PRs, SciPy/Qiskit/pandas; faults are injected mutants propagated through real commit
  history). ACCESS full text read. Locator: Abstract: "8%–17% of the generated tests are fault-enforcing, while only
  2.4%–4.8% reveal faults"; "after several subsequent commits, 83%–91% of them are still relevant and pass"; combined,
  "83%–92% remain enforced at the end of the commit history, and the developer-written test suite detects only
  14%–30% of them" (RQ2–RQ3). Bearing: the most direct first-hand evidence for C7 in software: derived checks lock in
  a defect, persist, accumulate, and existing checks miss most of them. Seeded mutants, not real bugs (limits
  external validity). Agents (LLMs) measured: yes.

### F. Self-correction speed (disconfirming candidates)

- **Claim: most Wikipedia hoaxes are caught quickly; a small fraction survives long and gets cited.** Kumar S, West R,
  Leskovec J (2016) "Disinformation on the web: impact, characteristics, and detection of Wikipedia hoaxes", WWW
  2016. https://dlab.epfl.ch/people/west/pub/Kumar-West-Leskovec_WWW-16.pdf TYPE first-hand study (~20,000 hoaxes).
  ACCESS full text read. Locator: §2: "80% of all new articles are patrolled within an hour of creation, and 95%
  within a day"; "90% are flagged within one hour of (so basically, during) patrol"; "it takes a day to catch 92% of
  eventually detected hoaxes, a week to catch 94%, a month to catch 96%, and one in a hundred survives for more than
  a year"; "1% of hoaxes are viewed over 100 times per day on average before being uncovered"; §6: "Human accuracy on
  this task is only 66%", classifier 86%. Bearing: AGAINST a strong C7 for curated encyclopedias: gatekeeping at
  creation (patrol) catches most fabrications fast. Caveat: sample is only hoaxes eventually flagged and deleted;
  undetected hoaxes are invisible by construction; hoaxes are whole fabricated articles, not wrong claims inside
  legitimate ones; humans reading the text alone are poor at detection.
- Q&A self-correction is slow (Zhang 2021: 20.5% updated; Ragkhitwetsagul: 20% of notified rarely/never fix);
  science self-correction via retraction leaves 94.6% of later citations unmarked (Hsiao & Schneider). See above.

## 3. Mechanisms

| mechanism | failure kind it signals | what it detects | what it misses | cost | evidence | agents measured? |
|---|---|---|---|---|---|---|
| Claim-specific citation network analysis (Greenberg) | misrepresentation propagated via citation (bias, amplification, invention) | authorities, citation bias toward supportive data, dead-end and hypothesis-to-fact citations | needs careful reading of each paper for data/invention; one claim at a time | high manual (242 papers) | Greenberg 2009, full text | n |
| Identical-misprint tracing (Simkin & Roychowdhury) | copying without consulting source | copy lineages via shared errors | correct copies; content errors | low (database) | 2003, full text | n |
| Quotation-accuracy audit (source vs claim) | misrepresentation of the cited source | major/minor quotation errors (14.5–25.4%) | whether the source itself is right | high manual | Jergas & Baethge 2015; Mogull 2017 | n |
| Retraction notice + database | lost validity (retracted source) | retracted status at source | 94.6% of later citing contexts do not record it | low per item; reach poor | Hsiao & Schneider 2021 | n |
| Initial accuracy judgement at exposure | repetition-induced belief | false repeated claims the reader already knows to be false; lasts 2 days | claims the reader cannot check from memory | low per item, attention cost | Brashier et al. 2020 | n |
| Correction with alternative explanation, warnings, repetition of correction | continued influence of corrected claim | reduces reliance | rarely eliminates; wears off; science claims d=0.19 n.s. | moderate | Lewandowsky 2012; Ecker 2022; Chan & Albarracín 2023 | n |
| Separate-context verification of each generated claim | snowballed hallucination | 67%/87% of own false claims (ChatGPT/GPT-4) | errors the model cannot recognise in isolation | one extra call per claim | Zhang et al. 2023 | y |
| Retain original data alongside derived (accumulate, do not replace) | model collapse / drift through derived data | prevents collapse in experiments | needs provenance to know what is original | storage; provenance | Gerstgrasser 2024; Shumailov 2024 (10% preserved) | y (models) |
| AI-text detectors + community flags | accumulation of generated text | lower bound ~4–5% new pages; flagged pages often deleted | accurate but unfounded generated text; FPR-bound | low | Brooks et al. 2024 | y (detectors) |
| Misinformation detector / vigilant prompt / reader voting in RAG | polluted corpus | in-domain detectors high AUROC | out-of-domain; prompting inconsistent | detector training; k readers | Pan et al. 2023 | y |
| Comment warnings on Q&A snippet | known-insecure text | nothing measurable: warned snippets copied more | — | low | Fischer 2017 | n |
| Point-of-reuse nudge to validated alternative | insecure derived code | steers to secure equivalent (99.37% have one) | cases with no validated alternative | classifier + UI | Fischer 2019 | n (humans) |
| Score/reputation voting | (intended) quality | not security: insecure answers score higher (14 vs 5) | correctness | free | Chen et al. 2019 | n |
| Clone/bug-propagation tracking | defect copied across clones | 18.42% of bug-fixed clones carry propagated bugs | divergent semantic copies | tooling | Mondal 2019 | n |
| Spec-first test generation (derive intent docstring, test against it) | tests derived from defective artifact | reduces misguided tests, raises bug-revealing tests | intent mis-derived from buggy code | one extra LLM step | Zhao et al. 2026 | y |
| Existing developer test suite vs fault-enforcing generated tests | locked-in defect | 14–30% of enforced faults | 70–86% | none extra | Charoosaei et al. 2026 | y |
| New-page patrol (Wikipedia) | fabricated article | 92% of eventually detected hoaxes within a day | hoaxes never flagged; claims inside real articles | volunteer labour | Kumar et al. 2016 | n |

## 4. Disconfirming searches and results

- "self-correction is fast": Wikipedia hoaxes (Kumar 2016): yes for whole-article fabrications under patrol (92% of
  detected within a day), with survivorship caveat. Stack Overflow (Zhang 2021; Ragkhitwetsagul 2019; Verdi 2020):
  no (20.5% updated; 253 of 287 GitHub copies still vulnerable). Science (Hsiao & Schneider 2021): retraction leaves
  94.6% of later citations unmarked; old retracted papers do stop being cited eventually (slow). Furman 2012
  (citation drop after retraction) could not be read: unverified. Conclusion: self-correction is fast only where a
  gate inspects every new item at creation; not shown for claims embedded in otherwise valid text.
- "repetition effects are small in expert/knowledgeable readers": Fazio 2015: knowledge does not interact with
  repetition; prior expert studies conflict (Srull 1983 smaller, numerically only; Arkes 1989 larger). Henderson
  2022: 92% single-session studies, 75% trivia, so no strong test with experts reading task text. No study found
  showing expertise protects. Conclusion: not disconfirmed; evidence on experts is thin and conflicting.
- "model collapse is inevitable" (would strengthen C7): Gerstgrasser 2024 disconfirms under accumulation; C7's
  generated-text form holds when derived replaces original, not when original is retained.
- "corrections backfire" (would strengthen C7): Ecker 2022 Box 2: familiarity and worldview backfire largely not
  supported. Corrections work partly; they do not reverse.
- Citogenesis empirical study: query "citogenesis empirical study Wikipedia circular reporting ..." found only the
  Wikipedia incident list, xkcd 978 and journalism; no prevalence study. Conclusion: unstudied quantitatively
  (as far as this search reached).
- Countermeasure for citation distortion with measured effect: none found beyond retraction notices; quotation-error
  literature measures rates, not interventions (thin).

## 5. Fields/terms the brief missed

citation distortion (bias, amplification, invention; Greenberg); information cascade; quotation error / quotation
accuracy; secondary (indirect) citation; "read before you cite" / citation copying; academic urban legends; Woozle
effect (term only, no empirical study read); citogenesis / circular reporting; post-retraction citation; illusory
truth effect / processing fluency / knowledge neglect; continued influence effect (CIE); prebunking / inoculation;
debunking with alternative explanation; accuracy nudge; hallucination snowballing; model collapse / data
accumulation; source bias (retrieval); misinformation pollution (RAG); false-premise / questionable-assumption QA;
sycophancy; online code clones / toxic code snippets; obsolete answers; bug propagation through cloning; fault-
enforcing tests / regression oracle / misguidance effect; security nudges.

## 6. Thin or contested points; unreachable sources

- Unreachable (full text): Walter & Tukachinsky 2020 (Chapman repository 403, SAGE paywall); Dechêne et al. 2010
  (no open copy); Furman, Jensen & Murray 2012 (MIT DSpace 429, CORE 403); Priedhorsky et al. 2007 (TLS failure on
  host / no PDF found). Their figures are not reported as verified.
- Third-party copies used for full text: Fazio 2015 and Ecker 2022 via typeset.io (published layout; provenance
  third-party). Hsiao & Schneider read via fetch tool (PMC captcha blocks curl).
- C7's "internal consistency can grow while correctness falls" has direct first-hand support in four distinct
  settings: citation networks (Greenberg, single case), within-generation LLM consistency (Zhang 2023), derived tests
  (Zhao 2026; Charoosaei 2026, seeded mutants), Q&A popularity/duplication (Chen 2019). No study measures
  consistency and correctness on the same durable-text corpus over time (gap; inference).
- "Later readers may no longer be able to tell the inference from the decision": supported indirectly
  (hypothesis→fact via citation, Greenberg; 5.4% post-retraction acknowledgment; 20% of citers read originals).
  No study tests whether readers can tell recorded inference from recorded decision (unstudied).
- Every measured stop found requires access to ground outside the propagated text: the reader's own correct knowledge
  (Brashier), the original data retained (Gerstgrasser), a separate verification context (Zhang), a statement of
  intent separate from the artifact (Zhao), a validated alternative (Fischer 2019), gatekeeping at creation (Kumar).
  Text-only warnings attached to the propagating text did not work (Fischer 2017; Pan 2023 vigilant prompting
  inconsistent). This pattern is inference across studies, not a tested claim.
- Several LLM results are on older models (GPT-3 era TruthfulQA; ChatGPT/GPT-4 2023); magnitudes may not transfer.
- 2026 arXiv items (Zhao ISSTA 2026; Charoosaei) are recent; Charoosaei is a preprint.
