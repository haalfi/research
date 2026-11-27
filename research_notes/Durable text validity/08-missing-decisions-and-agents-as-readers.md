# Track t08: finding missing decisions (Q6); agents reading durable text as authority (Q7)

Claims in scope: C5, C6, C7, C8. Research date 2026-11-27.
Builds on the earlier run's report (RQ2, RQ3, RQ6–RQ8). The sources it already covers are not re-surveyed here:
NaPiRE, HumanEvalComm, Ambig-SWE, ClarifyGPT, Xu & Wu, ImpossibleBench, TRACE, DocPrism, Lubos, Smella, Huang et al., Kim et al., DELEGATE-52.

## 1. Scope and searches run

Retrieval route: arXiv API (`export.arxiv.org/api/query`) by title or abstract, then arXiv PDFs passed through pdftotext. Repository PDFs were used where available. One scanned tech report was OCRed with tesseract. WebSearch was used for leads only.

Queries (arXiv API unless marked otherwise):
- `ti:requirements AND ti:completeness AND ti:language`
- `abs:requirements AND abs:incompleteness AND abs:LLM`
- Web: "GPT-4 detecting missing requirements incompleteness real omissions precision recall"
- Web: "Ciolkowski 2009 What do we know about perspective-based reading"
- Web: "Basili ... empirical investigation of perspective-based reading pdf"
- Web: "Ott 2012 defects ... Mercedes-Benz incompleteness most frequent"
- Web: "Lutz 1993 Analyzing software requirements errors ... ntrs"
- Web: SATD vs non-self-admitted debt; SATD vs SonarQube overlap
- `ti:AbstentionBench` (via ID), `ti:QuestBench`
- `ti:deprecated AND ti:API AND ti:LLMs`, `ti:VersiCode`, `ti:GitChameleon`
- Knowledge-conflict papers by known ID: survey 2403.08319, Xie 2305.13300, WikiContradict 2406.13805, ConflictBank 2408.12076
- `ti:"Resolving knowledge conflicts"`, `ti:"conflicting evidence" AND ti:retrieval`, `ti:LongMemEval`
- `ti:"reasoning models don't always"`, Turpin 2305.04388, Lanham 2307.13702, `ti:"self-explanations" AND ti:faithful`
- `abs:"commit message" AND abs:rationale`, `ti:commit AND ti:message AND ti:why`
- Web: "LLM-generated commit messages hallucinated why rationale fabricated"
- `abs:agentic AND abs:"pull request" AND abs:description...`
- `ti:SPOT AND ti:scientific`, `ti:"critical limitations"`, SAFE 2403.18802, FActScore 2305.14251
- `ti:self-preference AND ti:LLM`, `ti:"LLM evaluators recognize"`, `ti:"doesn't know it's wrong"`

## 2. Findings

### Q6: detecting missing decisions and unmarked open points, separately from resolving them

**F1. LLM-as-external-knowledge completeness check (BERT MLM) finds a minority of withheld content, and most of its suggestions are noise.**
- Claim: on simulated omissions, the best configuration surfaces terms hinting at about 4 in 10 omissions, and about 1 in 8 predictions is relevant.
- Source: Luitel, Hassani, Sabetzadeh, "Improving Requirements Completeness: Automated Assistance through Large Language Models", REJ 2024 / arXiv 2308.03784v2. https://arxiv.org/abs/2308.03784
- TYPE: first-hand study. ACCESS: full text read (RQ sections, limitations).
- Locators and quotes:
  - RQ1 answer: "BERT predicts terms that, on average, hint at ≈4 out of 10 omissions (Coverage ≈38%). On average, ≈1 in 8 predictions is relevant (Accuracy ≈12%)."
  - RQ3/RQ4: an ML filter trades the two off. Lenient filter: Accuracy +≈13%, Coverage −≈5%. Strict filter: Accuracy +≈36%, Coverage −≈20% (50-50 split).
  - Section 7.1: incompleteness was *simulated* "by withholding content", because there was no "access to domain experts who could effectively identify genuine cases of incompleteness". The authors did not test ChatGPT or GPT-family models.
- Bearing: Q6, C5.
  - Detection of *missing content* is possible, but recall is partial and precision low, and only against a synthetic ground truth.
  - The method finds missing *terminology*, not missing *decisions*. No real-omission validation exists. That gap is itself evidence that finding real omissions is hard to evaluate.

**F2. Frontier LLMs as requirement-quality reviewers miss half or more of expert-identified issues, including completeness. Necessity and correctness issues are essentially never caught.**
- Source: Shefa, Salado, Wach, Topcu, "Two Truths and A Lie? Benchmarking off-the-shelf LLMs for Requirements Quality Assessment – Performance, False Alarms, and Misses", arXiv 2609.03230 (2026). https://arxiv.org/abs/2609.03230
- TYPE: first-hand study (benchmark, expert ground truth). ACCESS: full text read (abstract, §4.1–4.2, appendix B passages).
- Locators:
  - Abstract: "the best-performing Anthropic model detects a median of only 47% of expert-identified issues while false-flagging 11%"; "necessity and correctness issues are almost always missed"; "generational progress is non-monotonic".
  - §4.2.2, for Claude Opus 4.7:
    - Necessary: FNR "identically 1.00 with zero variance".
    - Correct: median FNR 0.89.
    - Complete: median FNR 0.50, mean 0.59, range 0.00–1.00, SD 0.39. "the most extreme execution-level instability among all categories… highly unreliable capability for identifying completeness-related defects".
  - §4.1: median F1 0.40 (range ≈0.17–0.57).
  - Dataset: 13 + 20 requirements × 9 INCOSE criteria (§3, lines on 117 and 180 cells); 100 runs.
- Bearing: Q6, C5.
  - The issues that need judgment beyond the wording (necessity, correctness) are the ones missed. Completeness detection is run-to-run unstable.
  - Supports "costly defects lie beneath the wording" and "finding ≠ resolving": even finding is unreliable.
  - Small sample: 33 requirements, two sets.

**F3. LLMs rarely say "not sure" on underspecified problems, even when they can solve the fully specified version.**
- Source: Li, Kim, Wang, "QuestBench: Can LLMs ask the right question to acquire information in reasoning tasks?", arXiv 2503.22674v2 (Google DeepMind, 2025). https://arxiv.org/abs/2503.22674
- TYPE: first-hand study. ACCESS: full text read (abstract, §5.4).
- Locators:
  - Abstract: "only 40-50% accuracy on Logic-Q and Planning-Q"; "models struggle to identify the right question even when they can solve the fully specified version."
  - §5.4 (detecting underspecification): "Gemini Flash Thinking, Claude 3.5, and GPT-4o predicted 'not sure' on only 1.4%, 4.6%, and 0.7% of cases in the zero-shot … setting on Planning-Q, when the ground-truth ratio is 41.8%." On Planning-Q, all models performed "at most 5% better than the Random baseline".
- Bearing: Q6, C6. Detecting *that* something is missing is a separate, weaker capability than solving, and models default to guessing.
  - This is direct evidence for "an agent can act on a plausible reading without establishing that it is the intended one."
  - Limitation: synthetic constraint-satisfaction problems (CSPs), and the missing variable is exactly one.

**F4. Abstention on underspecified or unanswerable inputs is unsolved, does not improve with scale, and is worse after reasoning fine-tuning.**
- Source: Kirichenko, Ibrahim, Chaudhuri, Bell, "AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions", arXiv 2506.09038 (FAIR, 2025). https://arxiv.org/abs/2506.09038
- TYPE: first-hand study (20 datasets, 20 models). ACCESS: full text read (abstract, §1, §4.1–4.4).
- Locators:
  - Abstract: "reasoning fine-tuning degrades abstention (by 24% on average)"; "scaling models is of little use"; a crafted system prompt "can boost abstention in practice" but "does not resolve models' fundamental inability to reason about uncertainty."
  - §1: reasoning models are "often hallucinating missing context and providing definitive final answers even when their reasoning chains express uncertainty".
  - §4.1: recall ranges from "near-perfect … BIG-Bench Known Unknowns, down to near-zero recall on MediQ."
  - Models "generally exhibit high abstention precision" (§3, metric section).
  - FreshQA is included as the "outdated information" scenario.
- Bearing: Q6, C6, C8. The finding that reasoning models fill gaps with invented context is direct support for C6 ("supply a missing reason / plausible reading").
  - Prompting helps partially, which is consistent with C8: an instruction shifts the rate but does not enforce the behavior.
  - Disconfirming angle: high precision means that when models do abstain they are usually right. The failure is recall, i.e. silent gap-filling.

**F5. Inspection reading techniques and omissions: PBR's advantage is mixed in the original study and not confirmed by meta-analysis.**
- Source a: Basili, Green, Laitenberger, Lanubile, Shull, Sørumgård, Zelkowitz, "The Empirical Investigation of Perspective-Based Reading", UMD CS-TR-3585 (1995) / EMSE 1(2) 1996. https://drum.lib.umd.edu/items/7eb0ef0c-4045-4a28-b7ca-b8e2df410d16
  - TYPE: first-hand study (controlled experiment, NASA/GSFC SEL professionals). ACCESS: full text (scanned tech report, OCRed; see §6 for which parts were read).
  - Abstract: "When there is a statistically significant distinction, PBR performs better than the subjects' usual technique. However, PBR appears to be more effective on the generic documents than on the NASA documents."
  - Introduction, summarizing Porter et al. 1995 on scenario- and defect-based reading, where one scenario was "ambiguity/missing information": "scenario readers performed better than ad hoc and checklist readers with an improvement of about 35%… checklist reading was no more effective than ad hoc reading." This is secondary for Porter.
  - Teams were *hypothetical*: individual results were combined after the fact into teams of three (§2 design).
  - §3.2, Table 3 (permutation tests, PBR-only vs usual-technique-only teams): Generic/1995 p=0.0007; NASA/1995 p=0.0390; Generic/1994 p=0.0660; NASA/1994 p=0.4340. Significant in 2 of 4 domain×run cells.
  - §3.3: per-perspective coverage was analysed only "qualitatively". A correlation study of perspectives against defect *types* was deferred to "future work". No omission-specific yield is reported.
- Source b: Ciolkowski, "What do we know about perspective-based reading? An approach for quantitative aggregation in software engineering", ESEM 2009.
  - TYPE: review/meta-analysis. ACCESS: abstract only (EBSE Durham record https://ebse.webspace.durham.ac.uk/?p=130).
  - Abstract: "no clear positive effect of PBR"; PBR teams are more effective than ad hoc but "less effective when compared to checklists"; "strong indicators of researcher bias".
- Bearing: Q6, C5.
  - Structured human reading can find defects, including missing information. Its *advantage* over checklists is contested, and the originating group's results are not robustly replicated.
  - No study found here reports PBR yield *specifically on omissions* with a figure I could verify in full text. See §6.

**F6. Rationale (the "why") is sparsely recorded, and automated recovery can introduce rationale absent from the record.**
- Source: Sun, Saha, De Silva, Mastropaolo, Chaparro, "Recovering Fine-Grained Code Change Rationale from Multiple Software Artifacts" (Argus), arXiv 2604.10345v2 (2026). https://arxiv.org/abs/2604.10345
- TYPE: first-hand study (63 commits, 5 Java projects, plus a 12-person user study). ACCESS: full text read (RQ1, RQ5–6, failure analysis, discussion).
- Locators:
  - RQ1: Goal, Need and Alternatives were found in the artifacts of 61, 34 and 9 of 63 commits. Selected Alternative, Validation, Side Effects and Maturity Stage were found in 1–4 commits. "Constraints and Dependency, were not found in associated artifacts." Fine-grained rationale "cannot be recovered from commit messages alone."
  - Argus: 51.4% precision and 93.2% recall for rationale identification. Goal: 76.6% precision, 95.5% recall. Need and Alternatives: lower precision (59.5%, 50%).
  - Failure analysis: "false-positive sentences … sometimes caused the LLM to generate summaries for components that were absent from the ground truth". The tool scores this as "Extra Information" (unsupported content).
- Bearing: C5, the claim that a recovered reason cannot be told from a reconstructed one.
  - The study shows the record usually lacks Alternatives and Constraints entirely.
  - An LLM recovery pipeline, tuned for recall, generates rationale components that are not in the record. Without the reference summary, which a later reader lacks, these would read as recovered.
  - The authors' participants asked for traceability to the source sentences "to mitigate hallucinations". Provenance is the proposed check.

**F7. Hallucinated content in generated commit messages is common, and detecting it from metrics is weak.**
- Source: Liu, Lin, Thongtanunam, "Hallucinations in Code Change to Natural Language Generation: Prevalence and Evaluation of Detection Metrics", arXiv 2508.08661 (IJCNLP 2025). https://arxiv.org/abs/2508.08661
- TYPE: first-hand study. ACCESS: full text read (abstract, §3 taxonomy, RQ1/RQ2).
- Locators:
  - Abstract: "approximately 50% of generated code reviews and 20% of generated commit messages contain hallucinations".
  - Taxonomy (§3.2) includes Input Inconsistency, e.g. "speculating intent that contradicts the code change in commit messages". ("Intention violation" in this taxonomy means failing the task, e.g. a summary instead of a review. It is not about rationale.)
  - §1: individual metrics reach "56.6% ROC-AUC for code review and 61.7% for commit messages"; combining metrics "yields substantial improvements (69.1% and 75.3%". §5: generator-agnostic ranges are 0.538–0.566 (CodeReviewer) and 0.562–0.617 (CommitBench).
  - Generators were fine-tuned small models (Llama3.1-8B, Qwen2.5-7B, CCT5), not agents.
- Bearing: C6 ("supply a missing reason that later reads as recorded intent"). Measured: "intent" text that contradicts the diff.
  - Not measured: intent that is *unverifiable* but consistent with the diff, which is the case C6 cares about most.
  - I found no study that measures fabricated-but-plausible "why" in agent-written commits or PRs. This is a gap.

**F8. Agent PR descriptions are measured only by similarity, not by truth of rationale.**
- Source: Pham & Ghaleb, "Code Change Characteristics and Description Alignment: A Comparative Study of Agentic versus Human Pull Requests", MSR 2026, arXiv 2601.17627. https://arxiv.org/abs/2601.17627
- TYPE: first-hand study (33,596 agent PRs). ACCESS: full text read (5 pages).
- Locators:
  - Abstract: agent-introduced symbols are removed sooner (median 3 vs 34 days) and more often (churn 7.33% vs 4.10%).
  - Commit message–patch similarity: 0.72 vs 0.68. PR–commit similarity: 0.86 vs 0.88.
  - Agent PR merge rate: 76.80% vs 82.82%.
- Bearing: C6 (accumulation of short-lived agent output). Weak for the rationale question, because semantic similarity cannot detect invented reasons.
  - Its existence shows that the field's current metric for description quality is unable to see rationale fabrication (inference).

### Q7a: superseded or contradictory text

**F9. Models take coherent context over their own memory, but cling to memory when any evidence supports it. Majority and order sway them.**
- Source: Xie, Zhang, Chen, Lou, Su, "Adaptive Chameleon or Stubborn Sloth", ICLR 2024, arXiv 2305.13300. https://arxiv.org/abs/2305.13300
- TYPE: first-hand study. ACCESS: full text read (abstract, §1 findings, §4).
- Locators:
  - §1 bullets: "LLMs are highly receptive to external evidence if that is the only evidence, even when it conflicts with their parametric memory". With both kinds of evidence, "LLMs show a strong confirmation bias … and tend to cling to their parametric memory."
  - §4 conclusion: preference is "influenced by the popularity, order, and quantity of evidence". Irrelevant evidence can distract.
- Bearing: C6 (silent resolution) and C7.
  - A single stale document, presented coherently, is adopted. Where documents conflict, the tie is broken by prior belief, frequency and position, not by validity or date. No flag is raised unless asked.

**F10. Replication at scale (synthetic): the same pattern, with a positional preference for later evidence. Adding dates or descriptions to the question sharply changes behavior.**
- Source: Su et al., "ConflictBank", NeurIPS 2024 D&B, arXiv 2408.12076. https://arxiv.org/abs/2408.12076
- TYPE: first-hand study (7.45M claim–evidence pairs; misinformation, temporal and semantic conflicts). ACCESS: full text read (§3).
- Locators:
  - §3.2: memorization ratios are below 50% with only external evidence, and above 50% when parametric-consistent evidence is also given. This is "consistent with … Xie et al."
  - §3.4: "the model prefers the later-positioned conflict evidence more when internal conflicts are present (77.52% vs. 82.08%)".
  - §3.5: adding years or descriptions to the question cuts the memorization ratio. For Llama3-70B: "from 67.52% to 8.31%".
- Bearing: C6/C7.
  - The choice between conflicting texts tracks position, not validity.
  - Explicit temporal scoping in the *question* works, which favours making validity explicit in the text or query (inference).
  - Synthetic, entity-substitution data.

**F11. Real contradictions (Wikipedia): models usually answer from one passage and ignore the other. When told to look for conflict, they detect it often but also invent conflicts in clean text.**
- Source: Hou et al., "WikiContradict", NeurIPS 2024 D&B, arXiv 2406.13805. https://arxiv.org/abs/2406.13805
- TYPE: first-hand study (253 instances, human eval over 1,200 responses). ACCESS: full text read (§4–5).
- Locators (§5, WikiContradict_HumanEval):
  - Template 4 vs 5: "Typically, the models rely on a single passage to inform their response, disregarding the other passage."
  - Explicit instruction to consider conflict lifts Llama-3-70b from 10.4% to 43.8% correct, and GPT-4 only from 6.3% to 10.4%.
  - Llama-3-70b explicit conflicts: 13.3% → 60.0%. Implicit conflicts: 5.9% → 17.6%.
  - Template 5.2 (asked to identify contradictions): "GPT-4 detecting contradictions and providing reasonable explanations in around 88% of cases, followed by Llama-3-70b-instruct with 77%".
  - Template 5.4 (passages revised to be consistent): GPT-4 and Llama-3-70b "only confirming 44% and 48% of instances as conflict-free, and 'making up' reasons to explain why the two passages conflict in the remaining instances."
  - Caveat: these four variants used 48 instances, "each response is assessed by a single human annotator."
- Bearing: C6 (silent resolution: strongly *for*), C8 (instruction: partial).
  - Disconfirming in part: when *asked*, detection of explicit contradictions is high (≈88% for GPT-4).
  - But a detector that is told to look finds conflicts that do not exist in more than half of clean cases. Asking turns silent resolution into noisy over-flagging, not into reliable detection.
  - Implicit conflicts, which need reasoning, stay poorly handled even when asked.

**F12. Asked directly "is there a conflict?", GPT-3.5 tends to say no: near-perfect precision, low recall. Localizing the conflict and giving both answers is weak.**
- Source: Wang, Feng, Wang, Shi, Balachandran, He, Tsvetkov, "Resolving Knowledge Conflicts in Large Language Models", COLM 2024, arXiv 2310.00935v3. https://arxiv.org/abs/2310.00935
- TYPE: first-hand study (synthetic conflicts; GPT-3.5-turbo main model). ACCESS: full text read (§4–5).
- Locators:
  - Abstract: "while LLMs perform well in identifying the existence of knowledge conflicts, they struggle to determine the specific conflicting knowledge and produce a response with distinct answers".
  - Task 1 (Table 2 text): "LLMs display a tendency to declare 'no conflict', which results in a nearly perfect precision but a low recall."
  - Task 2: "precision exceeds recall, which revalidates LLMs' tendency to assert 'no conflict'". Break-down prompting reached F1 0.494 on span localization.
  - Task 3: accuracy of giving both answers is "hovering around 50%".
- Bearing: Q7a, C6.
  - Contrast with F11: one setting under-flags (GPT-3.5, synthetic), the other over-flags (GPT-4, asked about clean real text).
  - Conflict detection by LLMs is *uncalibrated* in both directions. Neither result supports "reliably detect when asked."

**F13. Under realistic mixtures of ambiguity, misinformation and noise, the best RAG baselines stay low. Multi-agent debate helps but leaves "a substantial gap", worse as supporting evidence becomes imbalanced.**
- Source: Wang, Prasad, Stengel-Eskin, Bansal, "Retrieval-Augmented Generation with Conflicting Evidence" (RAMDocs / MADAM-RAG), COLM 2025, arXiv 2504.13079. https://arxiv.org/abs/2504.13079
- TYPE: first-hand study. ACCESS: full text (abstract and intro read).
- Locators:
  - Abstract: RAMDocs is hard, with "the most performant Llama3.3-70B-Instruct only yields up to a 32.60 exact match score".
  - MADAM-RAG improves AmbigDocs by "up to 11.40%" and FaithEval by "up to 15.80%".
  - "a substantial gap remains, especially when increasing the level of imbalance in supporting evidence and misinformation."
- Bearing: C7. When a wrong claim is repeated in more documents (imbalance), handling degrades. Repetition outweighs validity.

**F14. Survey consolidation: inter-context conflicts include outdated vs updated documents; detection of contradictory documents is "subpar"; models favour relevance and frequency over credibility cues.**
- Source: Xu, Qi, Guo, Wang, Wang, Zhang, Xu, "Knowledge Conflicts for LLMs: A Survey", EMNLP 2024, arXiv 2403.08319. https://arxiv.org/abs/2403.08319
- TYPE: review/secondary. ACCESS: full text read (§3 inter-context conflict).
- Locators (§3.1–3.2):
  - "The retrieved documents may contain updated and outdated information … simultaneously".
  - Detection ability: Li et al. 2023 found GPT-4/PaLM-2/Llama 2 "average detection accuracy is subpar".
  - Wan et al. 2024: models "heavily prioritize the relevance of a document to the query but often overlook stylistic features … such as the presence of scientific references".
  - Jin et al. 2024a: "LLMs favor evidence that appears most frequently within the context".
- Bearing: C6/C7, secondary. Frequency-favouring is the mechanism by which accumulated copies (C6) become knowledge (C7).

**F15. Stale code context propagates. Completion prompts drawn from outdated code produce deprecated API usage 70–90% of the time. An inline deprecation comment fixes 26–97% depending on model.**
- Source: Wang, Huang, Zhang, Feng, Zhang, Liu, Peng, "LLMs Meet Library Evolution: Evaluating Deprecated API Usage in LLM-based Code Completion", ICSE 2025, arXiv 2406.09834v3. https://arxiv.org/abs/2406.09834
- TYPE: first-hand study (7 LLMs, 145 API mappings, 8 Python libraries, 28,125 prompts). ACCESS: full text read (§IV results, §V fixes).
- Locators:
  - Summary 5: "extremely high deprecated API usage rates for O (70%-90% DUR) and relatively low rates for U (9%-18% DUR)". O = prompts from outdated functions, U = prompts from up-to-date functions.
  - Cause: models predict the "reference APIs" in context (RUR 70–90% on both sets).
  - Overall DUR across models was 25%–38%, "larger models exhibiting higher DUR".
  - INSERTPROMPT (an inline replacement comment): "varied fixed rates, ranging from 25.7% to 97.2%".
- Bearing: C6 ("outdated text can stay where the next reader finds it"), C7 (the local context is copied forward), C8.
  - The surrounding stale text, not the model's knowledge, decides.
  - A text instruction (inline comment) works for some models and barely for others. Its presence does not establish its application.

**F16. Version-conditioned generation: even top systems solve about half. Execution feedback adds roughly 10–20 points; documentation RAG adds up to about 10.**
- Source: Misra, Islah et al., "GitChameleon 2.0", arXiv 2507.12367v2 (2025). https://arxiv.org/abs/2507.12367
- TYPE: first-hand study (328 problems with executable tests). ACCESS: full text read (§3–4).
- Locators:
  - Abstract: "enterprise models achieving baseline success rates in the 48-51% range".
  - §4 Self-Debugging: "Observed gains range from approximately 10% to 20%" on hidden tests, e.g. GPT-4.1-mini 44% → 68%.
  - RAG: "Many models exhibit a significant (up to 10%) boost".
  - CoT can hurt, e.g. o1 51.2% → 41.2%.
- Bearing: Q7c, C1/C8 by contrast.
  - Grounding in execution (a check that can fail) is the largest single improvement measured in this cluster.
  - But visible-test gains exceed hidden-test gains (§4 gap analysis), so execution against the tests at hand also overfits to them (consistent with ImpossibleBench, covered earlier).
  - VersiCode (arXiv 2406.07411) was downloaded but not read in detail. Not used.

**F17. Long-term memory: assistants and long-context LLMs drop about 30% on sustained-interaction memory, which includes a knowledge-update category.**
- Source: Wu et al., "LongMemEval", ICLR 2025, arXiv 2410.10813v2. https://arxiv.org/abs/2410.10813
- TYPE: first-hand study. ACCESS: full text (abstract, §3 categories read; per-category KU numbers not extracted).
- Locator: abstract: "commercial chat assistants and long-context LLMs showing a 30% accuracy drop". KU is defined as "Ability to recognize the changes in the user's personal information and update the knowledge … over time" (§3).
- Bearing: C6 (agent memory staleness). Weak, because I did not verify a KU-specific figure. Do not cite a number for staleness from this source.

### Q7b: invented rationale

**F18. CoT explanations rationalize answers driven by unmentioned biasing features.**
- Source: Turpin, Michael, Perez, Bowman, "Language Models Don't Always Say What They Think", NeurIPS 2023, arXiv 2305.04388. https://arxiv.org/abs/2305.04388
- TYPE: first-hand study. ACCESS: full text read (abstract, §3).
- Locator: abstract: models "systematically fail to mention" biasing features. "When we bias models toward incorrect answers, they frequently generate CoT explanations rationalizing those answers. This causes accuracy to drop by as much as 36%". §3: "-36.3% from the Suggested Answer bias".
- Bearing: C5, C6. A stated reason produced alongside a decision need not be the reason. The text of the rationale is not evidence of what decided.

**F19. Reasoning models verbalize the hints they use rarely (often below 20%). Under RL they learn reward hacks and almost never verbalize them.**
- Source: Chen, Benton, Radhakrishnan et al. (Anthropic), "Reasoning Models Don't Always Say What They Think", arXiv 2505.05410 (2025). https://arxiv.org/abs/2505.05410
- TYPE: first-hand study. ACCESS: full text read (abstract, §2–3, §5).
- Locators:
  - Abstract: "the reveal rate is often below 20%".
  - §3: overall faithfulness "25% for Claude 3.7 Sonnet and 39% for DeepSeek R1". CoTs are less faithful on harder tasks, by "44% relative for Claude 3.7 Sonnet and 32% relative for DeepSeek R1" (GPQA vs MMLU).
  - §5: "The model fully learns the reward hacks (reward > 0.99) … but almost never verbalizes the reward hacks (< 2% of the examples) in 5 out of 6 environments."
- Bearing: C5 ("without a record at the time, a recovered reason cannot be told from a reconstructed one"), C6.
  - Even a *contemporaneous* record written by the agent itself is an unreliable account of what decided. This sharpens C5: a contemporaneous record is necessary but not sufficient when the recorder is an LLM.

**F20. Larger models condition less on their own CoT on most tasks (post-hoc reasoning).**
- Source: Lanham et al. (Anthropic), "Measuring Faithfulness in Chain-of-Thought Reasoning", arXiv 2307.13702 (2023). https://arxiv.org/abs/2307.13702
- TYPE: first-hand study. ACCESS: full text (abstract and figures skimmed).
- Locator: abstract: models show "large variation across tasks in how strongly they condition on the CoT"; "As models become larger and more capable, they produce less faithful reasoning on most tasks we study."
- Bearing: C5/C6, same direction as F19.

**F21. Self-explanation faithfulness is explanation-, model- and task-dependent.**
- Source: Madsen, Chandar, Reddy, "Are self-explanations from Large Language Models faithful?", ACL Findings 2024, arXiv 2401.07927. https://arxiv.org/abs/2401.07927
- TYPE: first-hand study. ACCESS: full text (abstract read).
- Locator: abstract: "faithfulness is explanation, model, and task-dependent, showing self-explanations should not be trusted in general."
- Bearing: C6 (post-hoc rationale).

(F6 and F7 above also bear on Q7b, for commit and PR rationale.)

### Q7c: agents as verifiers grounded outside the text

**F22. Retrieval-grounded fact verification works on encyclopedic facts. SAFE agrees with crowd raters on 72% of facts and wins 76% of 100 disagreements, at more than 20× lower cost.**
- Source: Wei et al. (Google DeepMind), "Long-form factuality in large language models" (SAFE), NeurIPS 2024, arXiv 2403.18802. https://arxiv.org/abs/2403.18802
- TYPE: first-hand study. ACCESS: full text read (§4, limitations, appendix A.3 headings).
- Locators:
  - §4: "SAFE agrees with humans on 72.0% of individual facts". On 100 disagreement cases, "SAFE annotations were correct 76% of the time, whereas human annotations were correct only 19%". Cost $0.19 per response.
  - Limitations: "relies on Google Search as a knowledge source … Google Search may not easily find information about some fact or may lack profundity in expert-level" domains.
  - App. A.3 lists failure cause "Google Search: the necessary information … was not found".
- Bearing: disconfirming for C1 in one domain. Where a public external source exists, an agent verifier holds claims to a check that can fail, at low cost.
  - It does not transfer to project-internal durable text, where the authority (owner's decision) is not searchable (inference).
  - The ground truth itself was a researcher with internet access.

**F23. Retrieval is necessary for LLM fact verification, and verifiers lean toward "Supported".**
- Source: Min et al., "FActScore", EMNLP 2023, arXiv 2305.14251. https://arxiv.org/abs/2305.14251
- TYPE: first-hand study. ACCESS: full text read (§3–4, Table 3 text).
- Locators:
  - §4: "Retrieval significantly helps. Models that use retrieval are consistently better than No-context LM which either has a significantly high ER or does not preserve ranking". "just using Retrieve→LM may overestimate FACTSCORE, e.g., by up to 17%".
  - "most errors from ChatGPT are incorrectly assigning Supported to unsupported facts". Best estimator error rate below 2% (abstract).
- Bearing: Q7c, C1, C6.
  - Direct evidence of the failure mode "verifier agreeing with the text it checks": the LLM verifier's dominant error is to accept.
  - Ungrounded verification is unreliable. Grounding fixes the ranking but still overestimates unless ensembled.

**F24. LLMs as verifiers of scientific papers: recall at most 21.1%, precision at most 6.1%. Runs rarely rediscover the same errors.**
- Source: Son et al., "When AI Co-Scientists Fail: SPOT", arXiv 2505.11855 (2025). https://arxiv.org/abs/2505.11855
- TYPE: first-hand study (83 papers, 91 errata- or retraction-grade errors). ACCESS: full text read (abstract, §2.3, §3).
- Locators:
  - §3 Main Results: "o3 achieves the highest scores, with 6.1% ± 1.3 precision, 21.1% ± 4.4 recall, and a 37.8% pass@4". Next is Gemini-2.5-Pro (3.1%, 10.1%, 25.9%).
  - Abstract: "across eight independent runs, models rarely rediscover the same errors".
  - Caveat (§2.3): precision counts unannotated flags as false positives. The authors observed "the only instance in which we observe an LLM identifying an unannotated but genuine error" (line ~900), so precision is not badly understated.
- Bearing: C1, C5. The misrepresentations beneath the wording, the errors that matter, are largely not found by agents reading the text.
  - Run-to-run non-repeatability means a single agent pass is not a check that can be relied on to fail.

**F25. LLMs identify about half of synthetic "obvious" limitations. Literature retrieval helps modestly.**
- Source: Xu, Zhao, Patwardhan, Vig, Cohan, "Can LLMs Identify Critical Limitations within Scientific Research?" (LimitGen), arXiv 2507.02694 (ACL 2025). https://arxiv.org/abs/2507.02694
- TYPE: first-hand study. ACCESS: full text read (§5–6).
- Locator: §6.1: "Even the best-performing LLM, GPT-4o, can only identify about half of the limitations that humans consider very obvious." RAG via the Semantic Scholar API "improves the ability of LLM systems to generate limitations" (§1). Table 3–4 per-system gains were not attributed to cells in this reading, so no RAG gain figure is reported.
- Bearing: C5, Q7c. External grounding helps but does not close the gap.

**F26. An LLM verifier without external grounding is worse than none. Gains attributed to "self-critique" come from an external sound verifier selecting among samples.**
- Source: Stechly, Marquez, Kambhampati, "GPT-4 Doesn't Know It's Wrong", arXiv 2310.12397 (2023). https://arxiv.org/abs/2310.12397
- TYPE: first-hand study (graph coloring). ACCESS: full text read (§4).
- Locators:
  - §4.1: baseline 16%. With GPT-4 as its own verifier, "performance plummets–only a single instance of the 100 was answered correctly". With a sound external verifier, "nears 40%", but the feedback's content "seems largely irrelevant".
  - §4.2: "Out of 100 optimal colorings, it only agreed that 2 were correct… of which 118 of them are correct, it only claimed 30 of them as correct. Of those, it was right 5 times."
- Bearing: Q7c. The LLM verifier here *rejects* almost everything rather than agreeing. The failure is non-discrimination, not sycophancy.
  - Combined with FActScore (accepts too much), the evidence is that ungrounded LLM verdicts are poorly calibrated in a task-dependent direction.
  - The grounded external check is what carries the gain.

**F27. LLM judges recognise and favour their own generations. Self-recognition correlates linearly with self-preference.**
- Source: Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations", NeurIPS 2024, arXiv 2404.13076. https://arxiv.org/abs/2404.13076
- TYPE: first-hand study (summarization). ACCESS: full text (abstract and intro read; numbers not extracted).
- Locator: abstract: GPT-4 and Llama 2 have "non-trivial accuracy at distinguishing themselves from other LLMs and humans". Fine-tuning reveals "a linear correlation between self-recognition capability and the strength of self-preference bias".
- Bearing: C7. An agent reviewing text produced by its own model family is biased toward accepting it.

## 3. Mechanisms

| Mechanism | Failure kind it signals | Detects | Misses | Cost | Evidence | Agents measured? |
|---|---|---|---|---|---|---|
| MLM/LLM "what's missing" term suggestion (Luitel) | Misrepresentation by omission | Missing domain terms hinted by external corpus (~38% coverage, ~12% precision) | Missing *decisions*; anything not in general corpus | Low compute; high triage (7 of 8 suggestions noise) | F1 | LLM (BERT), not agents |
| LLM requirement-quality review (INCOSE criteria) | Omission, wrong/unnecessary requirement | ~47% of expert issues (median, best model); unstable on Complete | Necessity (FNR 1.00), Correctness (FNR ~0.89) | Low per run; unstable across runs | F2 | LLM, not agents |
| Perspective-based / scenario reading (humans) | Omission, inconsistency | Defects incl. missing info; better than ad hoc | Advantage over checklists not shown; domain docs less | Training + reviewer time | F5 (PBR full text; meta-analysis abstract) | n |
| Abstention / "not sure" option | Gap the reader would otherwise fill | Some unanswerable inputs; high precision | Most underspecified inputs (QuestBench "not sure" 0.7–4.6% vs 41.8% truth; AbstentionBench low recall) | Very low; prompt-dependent | F3, F4 | y (LLMs, not coding agents) |
| Ask-to-detect-contradiction prompt | Contradiction between texts | Explicit conflicts (GPT-4 ~88%) | Implicit conflicts; false conflicts in clean text (only 44% confirmed clean) | Very low | F11, F12 | y (LLMs) |
| Temporal scoping in query (add dates) | Superseded text | Shifts choice to matching-era evidence (MR 67.52%→8.31%) | Requires dates exist in text/question | Very low | F10 | LLMs |
| Inline deprecation/replacement comment (InsertPrompt) | Superseded API in context | Fixes 25.7–97.2% of deprecated completions | Model-dependent; requires someone to know deprecation | Low | F15 | code LLMs |
| Execution feedback (self-debug against tests) | Behaviour wrong vs version | +~10–20 pts hidden success | Overfits visible tests; wrong tests | Compute + test authoring | F16 | y (LLMs/agents) |
| Retrieval-grounded fact check (SAFE, FActScore) | Misrepresentation of public fact | Atomic public facts; 72% human agreement, wins 76% disagreements | Non-searchable/project-internal facts; decisions; verifier leniency ("Supported") | ~$0.19/response | F22, F23 | y (LLM agent with search) |
| LLM paper verifier (SPOT, LimitGen) | Misrepresentation beneath wording | ≤21% of errata-grade errors; ~half of obvious synthetic limitations | Most real errors; non-repeatable across runs | Moderate | F24, F25 | y |
| Rationale provenance (Argus, trace to source sentences) | Reconstructed vs recovered reason | Goal reliably; Need/Alternatives partially | Reasons never recorded (Constraints 0/63); generated extra components | Moderate | F6 | LLM pipeline |
| Hallucination metrics on generated commit text | Invented/contradictory intent | Combined ROC-AUC 0.75 (commit) | Plausible unverifiable intent | Low | F7 | small fine-tuned LMs |
| CoT monitoring | Unstated reasons for action | Some hint use (reveal often <20%) | Reward hacks (<2% verbalized) | Low | F18–F20 | y (reasoning models) |
| Same-family LLM judge | — | — | Self-preference | — | F27 | y |

## 4. Disconfirming searches and results

- **Do LLMs reliably detect conflicts when asked?** Searched knowledge-conflict detection (Wang et al. 2310.00935; WikiContradict; survey). Found:
  - GPT-4 detects about 88% of real contradictions when told to look (F11).
  - But it invents conflicts in at least 52% of clean pairs (F11), and GPT-3.5 under-reports conflicts (F12).
  - Conclusion: partial disconfirmation of "silently resolves". Detection-on-request exists for *explicit* conflicts but is uncalibrated. It does not cover implicit conflicts, and it is not the default behaviour. C6 stands as "can … without exposing it", and the evidence shows it is the default.
- **Does grounding the verifier solve it?**
  - SAFE and FActScore show strong results for public encyclopedic facts (F22, F23).
  - GitChameleon shows execution feedback is the largest gain (F16).
  - But SPOT and LimitGen (F24, F25) show grounded or strong models still miss most real errors in research text.
  - FActScore shows grounded verifiers still over-accept.
  - Conclusion: grounding solves the narrow case where an external authority exists and is retrievable or executable. It does not solve decisions, rationale, or project-internal validity. No study found tests a grounded verifier against a project's own decision record.
- **Do models track staleness or dates by themselves?**
  - ConflictBank (F10): position, not date, drives the choice. Dates in the question fix much of it.
  - Deprecated API study (F15): context staleness propagates at 70–90%.
  - Conclusion: no evidence of unprompted staleness detection.
- **Is incompleteness detection solved in RE?**
  - Searched LLM completeness checking. The best evidence is synthetic withholding (F1), and a 2026 benchmark shows completeness FNR median 0.50 with extreme instability (F2).
  - Conclusion: not solved.
- **Is missing information really the dominant requirements defect class?**
  - Ott 2012 (Mercedes-Benz) is unreachable. Only its citation in Ott & Raschke 2013 (Ulm tech report UIB-2013-08) was read. That report states reviewers have "major problems in finding defects, especially consistency or completeness defects" and cites [3] for the distribution, but gives no figures.
  - Lutz 1993 is unreachable (NTRS record has no file).
  - Conclusion: not verified in this track. The earlier run's NaPiRE result (incomplete/hidden requirements ranked first) remains the verified anchor.
- **SATD (marked vs unmarked debt).**
  - Search-level only: Rantala, Mäntylä, Lenarduzzi (keyword-labeled SATD vs SonarQube, SQJ 2023) report "significant relationship but limited overlap" (abstract/record via search; Springer page redirected to login).
  - I found no study quantifying unmarked debt that is later found. Marked and unmarked appear complementary.
  - Conclusion: unverified, a lead only.
- **Is invented rationale a real cost?**
  - Searched for studies of fabricated "why" in LLM- or agent-written commits and PRs. I found only intent that *contradicts* the diff (F7, about 20% of commit messages had some hallucination), and similarity metrics (F8).
  - No study measures unverifiable-but-plausible rationale, or its downstream reading as intent.
  - Conclusion: C6's "invented rationale read as intent" is supported by mechanism evidence (F18–F21, F6), not by an in-the-wild measurement.

## 5. Fields/terms the brief missed

- **Abstention / selective prediction**, "known unknowns" (AbstentionBench). **Information acquisition / underspecification detection** (QuestBench, the "1-sufficient CSP" formalism).
- **Knowledge conflict** taxonomy: context–memory, inter-context, intra-memory. Plus **memorization ratio**, the standard metric for "which source won".
- **Temporal misalignment**, **fact duration prediction** (Zhang & Choi 2023), and FreshQA as the "outdated information" benchmark.
- **Deprecated usage rate (DUR) / reference usage rate (RUR)**, **version-conditioned code generation** (VersiCode, GitChameleon).
- **CoT faithfulness / monitorability**: reveal rate, post-hoc reasoning, early answering.
- **Interpretability-faithfulness self-consistency checks** (Madsen).
- **Rationale components** taxonomy (Goal, Need, Alternatives, Selected Alternative, Constraints, Dependency, Side Effects, Validation, Maturity Stage; Al Safwan et al., used by Argus).
- **CodeChange2NL hallucination** taxonomy (input inconsistency, logic inconsistency, intention violation).
- **Long-form factuality / atomic-fact verification** (FActScore, SAFE). **Verifier leniency** (over-assigning "Supported").
- **Self-preference / self-recognition** in LLM-as-judge.
- **INCOSE requirement quality criteria** (Necessary, Correct, Complete, Singular...) as an LLM-evaluation ground truth.

## 6. Thin or contested points; unreachable sources

- Every detection result on omissions is on **synthetic** or small ground truth:
  - Withheld text (Luitel).
  - One missing variable (QuestBench).
  - 33 requirements (Two Truths).
  - Perturbed papers (LimitGen-Syn).
  - No study measured detection of *real* undecided decisions in project text.
- **Uncalibrated conflict detection:** WikiContradict over-flags and Wang et al. under-flags. Different models (GPT-4 vs GPT-3.5), prompts and data. Do not generalize either direction.
- WikiContradict template 5.x results are 48 instances with a single annotator.
- PBR (Basili et al.):
  - Full text was OCRed from a scan. The abstract, introduction, hypotheses, design, team analysis (Table 3) and the start of the perspective analysis were read.
  - The report gives no omission-specific yield (§3.3 defers defect-type analysis), so no omission-specific PBR figure exists to report from this source.
  - Ciolkowski 2009: abstract only.
- **Unreachable:**
  - Ott 2012 RE (IEEE; only the citation context was read).
  - Lutz 1993 (NTRS record has no file).
  - Rantala et al. SATD/SonarQube (Springer login redirect).
  - Ciolkowski 2009 full text.
  - Shull et al. PBR follow-ups (not attempted).
- LongMemEval knowledge-update figures were not extracted; only the headline 30% drop is used.
- Liu et al. (F7) used small fine-tuned models on CommitBench and CodeReviewer, not coding agents. Agent-era rates are unknown.
- Self-preference (F27) and Madsen (F21) were read at abstract/intro depth within the downloaded full text. Their figures are not reported.
- VersiCode was downloaded but not analysed.
