# Track 1: Workflow, adversarially verified claims

Source: deep-research workflow (5 search angles, 22 sources fetched, 102 claims extracted, 25 verified by 3-vote, 23 confirmed, 2 refuted). Notes are kept as the workflow returned them.

## Summary

23 claims survived verification, and they reduce to five findings, all from primary sources. (1) The most cited and most consequential requirements problems in practice are incomplete or hidden requirements and communication flaws, not wording problems. NaPiRE (2017): incomplete or hidden requirements were cited by 48% of 228 companies, while terminological problems did not reach the top 10. The Berry/Kamsties handbook (2003) also separates ambiguities that writing rules can fix from domain ambiguities that only a reader with domain knowledge or the missing information can catch. So writing rules help only partly. Most protection has to come from structural controls (explicit assumptions, defaults and failure cases) and from process controls (an independent interpretation, clarification). (2) Requirement templates such as EARS and boilerplates make wording better and expose gaps. They do not supply the missing decisions, and they cost real training effort. The evidence is an author-run case study, one 2024 benchmark read only as an abstract, and a 10-person experiment. (3) Automated smell detection is a cheap supplement to review, not a gate. Smella measured 59% precision and 82% recall, with high variation. (4) Several studies agree that code LLMs and agents fill underspecified or contradictory specs with their own assumptions instead of asking. Resolution drops sharply (SWE-bench Verified with Claude Sonnet 4.5: 70.8% to 54.8%) and mostly comes back when clarification is built in. Contradictions between examples and prose get the fewest questions. (5) Comparing independent interpretations (several readers, paraphrase back to the author, or several sampled solutions as in ClarifyGPT) is described as the most effective way to find ambiguity, but also the most expensive. It cannot catch an assumption that every reader or sample shares. No verified evidence survived for traceability, drift, glossaries, Vale/lint tools, long-context effects, or the diminishing returns of controls. Recommendations in those areas would rest on inference.

## Verified findings

### F1 (confidence medium, vote 3-0)

RQ1 (taxonomy, frequency and consequence): The established expert taxonomy has four overlapping classes of linguistic ambiguity: lexical, syntactic, semantic and pragmatic. Vagueness and generality are treated as related, and language error is filed under pragmatic ambiguity. A second split separates language ambiguities, which any careful reader can spot, from software-engineering ambiguities, which depend on domain knowledge or missing information. The pump example ('water level remains above 100 meters for more than 4 seconds') has at least four readings. The engineers silently chose the unsafe one, and the handbook authors did not notice it either. Implication (inference): writing rules address only the language class. Domain and underspecification ambiguities need structural controls (stated assumptions, defined aggregation and boundaries) and review by someone with domain knowledge.

Sources: https://cs.uwaterloo.ca/~dberry/handbook/ambiguityHandbook.pdf

Evidence: Berry, Kamsties & Krieger, 2003 handbook (expert taxonomy, not a frequency study). Verified verbatim against the full text, vote 3-0 on two claims. The two-way split is adopted from Schneider, Martin & Tsai, and the pump example comes from Parnas et al. Transferability to a small docs-as-code repo: conceptual only, but the warning about silent unsafe interpretation carries over directly to agent-written code.

### F2 (confidence medium, vote 3-0)

RQ1 (what is most frequent in practice): In NaPiRE (228 companies, 10 countries, each respondent picking the top 5 of 21 predefined problems), incomplete or hidden requirements were cited most often (109, 48%). Next came communication flaws with the customer (93, 41%), then moving targets and underspecified requirements (76 each, 33%). Inconsistent requirements were 9th (44, 19%), and terminological problems did not reach the top 10. Frequency is not the same as consequence. Respondents linked communication flaws to project failure slightly more often (45) than incomplete requirements (43), and moving targets far more often (39) than underspecified requirements (28) at equal frequency. Implication (inference): for a small team, the biggest risks are missing decisions and requirements that change unnoticed (drift), not terminology. Controls should put completeness and change-tracking ahead of wording rules.

Sources: https://arxiv.org/abs/1611.10288

Evidence: Méndez Fernández et al., Empirical Software Engineering 2017, survey data from about 2014-2015 (empirical survey). Figures verified in Table 9 of the full text. The counts measure how often a problem was cited in a respondent's top 5, not how often it occurred. Links to failure are respondents' own judgments. The survey predates AI agents.

### F3 (confidence medium, vote 3-0)

RQ5 (templates and EARS): EARS (Mavin et al., RE'09) offers a small structural ruleset aimed at eight common problems, including ambiguity, vagueness and complexity. It asserts that all natural-language requirements fit one of five templates. The original evidence is one industrial case study run by the authors (aero-engine control requirements), with no controlled design and no quantitative results in the abstract. A 2024 benchmark (Großer et al.) compared 1764 requirements rewritten in five template systems against free text. Every system except SPIDER had positive effects on all seven quality characteristics, and effect sizes were similar across systems. In the same paper, a user experiment with 43 participants, mostly students, found that templates need substantial prior training and that domain knowledge matters whether or not a template is used. A small experiment (n=10, 3 requirements, PLC domain, 2025) found that people wrote EARS easily. The most common problem was that the source requirements were incomplete, not the syntax. Implication (inference): templates are a modest, low-cost aid for trigger, state and response statements. They make gaps visible but do not fill them, and requiring them everywhere imposes a training cost.

Sources: https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/, https://link.springer.com/article/10.1007/s00766-024-00427-0, https://www.es.mdu.se/pdf_publications/7171.pdf

Evidence: Three primary sources, all voted 3-0: a 2009 case study, a 2024 benchmark plus student experiment, and a 2025 small experiment. The Großer result rests on the Crossref abstract only (the full text was behind a challenge page), so significance and effect sizes are unverified, and 'positive effects' may be the authors' own quality ratings rather than downstream defect outcomes. Two related claims about the Salari study were refuted: that EARS selection forced gaps to be resolved (0-3), and that differing pattern choices showed EARS lacks a single interpretation (1-2). Do not cite either. Calling the training need an author/reviewer cost is inference.

### F4 (confidence medium, vote 3-0)

RQ5/RQ7 (automated smell detection): Requirements Smells are a lightweight static analysis, adapted from code smells and based on ISO 29148 quality criteria, meant to run as soon as requirements are written. The authors position it as a supplement to review that handles obvious issues so reviewers can focus on domain-specific ones. The Smella prototype reached 59% average precision and 82% average recall, with high variation across three industrial contexts and one university context. Roughly 4 in 10 flags were false positives, and some smells were poorly defined. Implication (inference): lexical smell checks such as weak words, vague quantifiers or passive voice suit advisory output, for example non-blocking Vale warnings. They are a poor fit for a blocking CI gate, where false positives would push authors toward surface compliance.

Sources: https://arxiv.org/abs/1611.08847

Evidence: Femmer et al., JSS 2017 (empirical study, evaluated by the tool's own developers, who call for independent replication). The study predates LLM-based detectors. Precision depends on how each smell is defined, and the study does not measure whether correctly flagged smells mattered to practitioners.

### F5 (confidence high, vote 3-0 / 2-1)

RQ8 (AI coding agents and underspecification): Several independent benchmarks agree that LLMs and agents rarely ask for clarification and instead commit to an assumption. HumanEvalComm (2024-era models; 164 HumanEval problems turned into 762 ambiguous, inconsistent or incomplete variants): more than 60% of responses went straight to code, and over 80% for most models, even though models were explicitly allowed to ask. Pass@1 fell 35-52% and Test Pass Rate 17-35% (relative drops; significance cutoff p<0.1, no multiple-comparison correction). A follow-up paper by the same authors (2025) restates this as more than 63% non-clarification. Ambig-SWE (ICLR 2026): agents struggle to tell well-specified from underspecified issues (Claude Sonnet models were the exception, at 84-89% accuracy), and without explicit prompting they almost never interact. With a simulated user, resolution improves by up to 74% (relative, best model). Edwards & Schuster (2026 preprint; OpenHands on 500 underspecified SWE-bench Verified issues): removing details cut Claude Sonnet 4.5 from 70.8% to 54.8% and Kimi K2.6 from 72.8% to 55.4%. A separate Intent Agent that can interrupt the coding agent to ask questions recovered 69.4%. A single agent prompted to check for ambiguity reached only 61.2%, while a single agent told up front that the issue was incomplete reached 70.4% (but failed on Kimi, at 47.2%). Implication (inference): an agent treats whatever the repository says as the whole contract, so an unstated decision becomes an implementation choice with no record. Missing decisions must be either stated or explicitly marked open (for example, an 'Open questions' block that agents are told to stop on).

Sources: https://arxiv.org/pdf/2406.00215, https://arxiv.org/html/2504.16331v2, https://arxiv.org/abs/2502.13069v3, https://www.alphaxiv.org/abs/2603.26233.md

Evidence: Four primary sources from three research groups; votes 3-0 except the Ambig-SWE 'never ask' claim (2-1). Limitations: underspecification was synthetic (manually edited HumanEval problems, or GPT-4o summaries of SWE-bench issues), the users were simulated LLMs that held the full spec (an optimistic upper bound), HumanEvalComm tested only 2024 small and mid-size models, and Edwards & Schuster is an unreviewed preprint with one scaffold and a 100-iteration cap. Transfer to real repository tasks is plausible but untested.

### F6 (confidence medium, vote 3-0)

RQ6/RQ8 (contradictions between examples and prose): In HumanEvalComm, inconsistency (example outputs that contradict the description) drew the lowest clarification rate of the three defect types for ChatGPT and the DeepSeek models. The authors suggest that detecting it needs stronger reasoning. Incompleteness gave the lowest Pass@1 (12.8%-46.95%). Inconsistency nevertheless had the highest Pass@1, because models sometimes produced correct code without asking. Implication (inference): when examples, tests and prose disagree in a repo, an agent is likely to pick one silently. Cross-artifact consistency therefore has to be checked explicitly, by a person or a dedicated check, and the agent's silence cannot be taken as agreement.

Sources: https://arxiv.org/pdf/2406.00215

Evidence: Single primary peer-reviewed study (ACM TOSEM 2025), vote 3-0, verifier confidence medium. The pattern was not uniform: for CodeLlama and CodeQwen, incompleteness had the lowest clarification rate. 'Tests' here means docstring examples, not test suites. The tasks are single functions.

### F7 (confidence medium, vote 3-0)

RQ6 (independent interpretation): Comparing the interpretations of several stakeholders, and paraphrasing an interpretation back to the author, are called 'perhaps the most effective' ways to find ambiguity. They are also the most expensive, so the handbook says they are justified only when undetected ambiguity would cost at least as much. This is the authors' judgment, with no measurement. ClarifyGPT (FSE 2024) automates a version of this: it samples several solutions, runs them on generated inputs, and treats differing outputs as a sign of ambiguity. Only then does it ask targeted questions and regenerate. With 10 human participants answering the questions, GPT-4's Pass@1 on MBPP-sanitized rose from 70.96% to 80.80% (and on MBPP-ET from 51.52% to 60.19%). Inference: checking for disagreement cannot reveal an assumption every sample shares, the same common-mode limit known from N-version programming. So agreement between agents, or between code and tests written from the same text, is weak evidence that the spec is correct.

Sources: https://cs.uwaterloo.ca/~dberry/handbook/ambiguityHandbook.pdf, https://2024.esec-fse.org/details/fse-2024-research-papers/89/ClarifyGPT-A-Framework-for-Enhancing-LLM-based-Code-Generation-via-Requirements-Clarification

Evidence: The handbook gives expert judgment only. ClarifyGPT is a peer-reviewed empirical study, but its human study is small (n=10, students and developers) and covers short, self-contained Python tasks. The paper does not report how accurate the ambiguity detector itself is. The shared-assumption limit is inference from the design. Knight & Leveson 1986 was not among the verified sources.

## Refuted (do not cite)

- (0-3) Applying the EARS templates exposed missing decisions in the natural-language requirements, such as failure handling and startup/default/safe states. Participants could not pick a template until those gaps were resolved, so templating worked as a way to find underspecification. — https://www.es.mdu.se/pdf_publications/7171.pdf
- (1-2) Different participants mapped the same requirement to different EARS patterns (ubiquitous, event-driven, state-driven, unwanted behavior) depending on how they read it. The authors call this flexibility, but it also shows that EARS does not guarantee a single interpretation. The choice of pattern affected which tests were derived, for example 'shall not' forms led to tests of unwanted behavior only. — https://www.es.mdu.se/pdf_publications/7171.pdf

## Caveats

Coverage is uneven. The verified claims address RQ1, RQ5, RQ6, RQ8 and part of RQ7 (smells). Nothing survived verification for RQ2 (Jackson/Zave assumptions, decision tables, the test-oracle problem), RQ3 (ADRs, documentation drift, code-comment inconsistency, the Egyed and Mäder traceability experiments), RQ4 (glossaries, identifier naming, DDD), RQ9 (verbosity, long-context degradation), RQ10 (diminishing returns), RFC 2119/8174, ISO 29148, AGENTS.md studies, Knight & Leveson, or the tool shortlist (licenses and 2026 maintenance status were not verified). Any ruleset, PR procedure or tool recommendation in those areas is inference or practitioner judgment and must be labeled that way. Confidence rubric: a single primary peer-reviewed source with a unanimous vote is rated medium rather than low, because source quality was high. High is used only where several independent primary sources converge. Source weaknesses: the Großer et al. 2024 result rests on the Crossref abstract, not the full text. The EARS evidence is a 2009 author-run case study plus small student or n=10 samples. Smella was evaluated by its own developers. Edwards & Schuster 2026 is an unreviewed preprint. HumanEvalComm used a lenient p<0.1 cutoff and 2024 small and mid-size models. All the agent benchmarks used synthetic underspecification and simulated users, so the recovery figures are optimistic. Percentages such as 74% and 35-52% are relative, not percentage points. Time sensitivity: agent clarification behavior is changing quickly, and 2024 model results may overstate current failure rates, while the 2026 SWE-bench results show the problem persists for frontier models. NaPiRE data is from about 2014-2015. No quantitative benefit of any repository writing rule for a small docs-as-code team was found, so none should be claimed.

## Open questions

- Does marking unresolved decisions in-repo (an 'Open questions' or 'Assumptions' block that agents are instructed to stop on) actually make coding agents ask or halt on real, not synthetic, underspecified tasks, and at what false-stop cost?
- How often do code and tests generated by the same agent or model from the same text encode the same unstated assumption? In other words, how large is the common-mode effect for agent-written tests versus independently derived tests?
- Is there any empirical measurement of documentation, spec or test drift and its detection cost in small docs-as-code repos, and of lightweight ID-and-link traceability, that would justify, or argue against, CI-enforced trace checks?
- Do modern LLM-based requirement smell or ambiguity checkers achieve meaningfully better precision than Smella's 59% without encouraging surface-compliance rewrites?

## Sources

| URL | quality | angle | claims |
|---|---|---|---|
| https://cs.uwaterloo.ca/~dberry/handbook/ambiguityHandbook.pdf | primary | Academic RE: ambiguity taxonomy and requirement smells | 5 |
| https://arxiv.org/abs/1611.08847 | primary | Academic RE: ambiguity taxonomy and requirement smells | 5 |
| https://link.springer.com/article/10.1007/s00766-024-00427-0 | primary | Academic RE: ambiguity taxonomy and requirement smells | 5 |
| https://arxiv.org/abs/1611.10288 | primary | Academic RE: ambiguity taxonomy and requirement smells | 5 |
| https://www.es.mdu.se/pdf_publications/7171.pdf | primary | Academic RE: ambiguity taxonomy and requirement smells | 5 |
| https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/ | primary | Academic RE: ambiguity taxonomy and requirement smells | 5 |
| https://arxiv.org/abs/2502.13069v3 | primary | AI coding agents and underspecified tasks | 5 |
| https://arxiv.org/pdf/2406.00215 | primary | AI coding agents and underspecified tasks | 5 |
| https://2024.esec-fse.org/details/fse-2024-research-papers/89/ClarifyGPT-A-Framework-for-Enhancing-LLM-based-Code-Generation-via-Requirements-Clarification | primary | AI coding agents and underspecified tasks | 4 |
| https://www.alphaxiv.org/abs/2603.26233.md | primary | AI coding agents and underspecified tasks | 5 |
| https://arxiv.org/html/2504.16331v2 | primary | AI coding agents and underspecified tasks | 5 |
| https://link.springer.com/10.1007/s10664-023-10397-6 | primary | Documentation drift and cross-artifact consistency | 5 |
| https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f/full | primary | Documentation drift and cross-artifact consistency | 4 |
| https://www.inf.usi.ch/faculty/lanza/PUBS/P/Wen2019a.pdf | unreliable | Documentation drift and cross-artifact consistency | 0 |
| https://arxiv.org/abs/2403.00251v1 | primary | Documentation drift and cross-artifact consistency | 5 |
| https://strictdoc.readthedocs.io/en/stable/strictdoc_01_user_guide.html | primary | Practitioner docs-as-code tooling | 5 |
| https://sphinx-needs.readthedocs.io/en/stable/changelog.html | primary | Practitioner docs-as-code tooling | 5 |
| https://github.com/itsallcode/openfasttrace/blob/main/doc/user_guide.md | primary | Practitioner docs-as-code tooling | 5 |
| https://docs.vale.sh/topics/readme.md | primary | Practitioner docs-as-code tooling | 5 |
| https://arxiv.org/abs/2602.11988 | primary | Contrarian: costs and failure modes of controls | 5 |
| https://arxiv.org/abs/2601.20404 | primary | Contrarian: costs and failure modes of controls | 4 |
| https://research.trychroma.com/context-rot | primary | Contrarian: costs and failure modes of controls | 5 |
