# Track 2: Workflow, extracted but not 3-vote verified

Claims that fetch agents extracted from full texts but that the verify phase did not reach (budget cut) or that were not sampled for verification. Single-pass extraction only: treat them as leads until checked again. The report labels them 'extracted, unverified' unless track 3/4/5 re-checked them.

## https://cs.uwaterloo.ca/~dberry/handbook/ambiguityHandbook.pdf

Date: 2025-02-18 (v1); v3 2026-02-21; ICLR 2026; quality: primary

- On Ambig-SWE, an underspecified variant of SWE-Bench Verified with GPT-4o-generated synthetic underspecified issues, letting agents interact with a simulated user improves resolution by up to 74% over non-interactive settings on underspecified inputs.
- LLM agents have trouble telling well-specified instructions from underspecified ones, and without explicit prompting they almost never ask clarifying questions, even when the input is severely underspecified.
- Underspecification detection varies widely by model. Claude Sonnet 4 and Sonnet 3.5 reach 89% and 84% accuracy. Qwen 3 Coder never interacts (100% FNR), while Llama 3.1 over-interacts, with a false-positive rate of 0.95 under moderate prompting.
- Even with interaction, agents recover only part of full-specification performance: up to 80-89% for Claude models, but only 59% for Deepseek and 54% for Llama 3.1. Clarification does not fully replace a complete spec.
- Some agents fill missing information from internal knowledge or guesses rather than asking or exploring. This can inflate benchmark scores in the underspecified (Hidden) setting. Limitations: the simulated user may be more cooperative than real users, detection is measured only in the first three turns, and the ambiguity is synthetic.

## https://arxiv.org/abs/1611.08847

Date: 2024-07 (ESEC/FSE 2024, July 15-19, 2024; arXiv preprint 2310.10996 first posted 2023-10-17); quality: primary

- ClarifyGPT decides whether a requirement is ambiguous by checking code consistency: it samples several solutions from the LLM and treats disagreement among them as a sign of ambiguity. Only when that check fires does it generate targeted clarifying questions, refine the requirement from the answers, and regenerate the code with the same LLM. This is an independent-interpretation check: different readings of the spec produce different code. (Inference: the check cannot catch an ambiguity that all samples resolve the same way, because they share the same assumption.)
- In a human study with 10 participants answering the clarifying questions, ClarifyGPT raised GPT-4's Pass@1 on MBPP-sanitized from 70.96% to 80.80%. Limitations: a small sample, and short self-contained Python function tasks rather than repository-scale agent work, so the result transfers to a docs-as-code repo only weakly.
- In automated evaluation, the user's answers come from an LLM simulation rather than people. The arXiv abstract reports that ClarifyGPT raises average Pass@1 across four benchmarks from 68.02% to 75.75% for GPT-4 and from 58.55% to 67.22% for ChatGPT. The FSE 2024 page reports five benchmarks instead: 62.43% to 69.60% for GPT-4 and 54.32% to 62.37% for ChatGPT. The two versions disagree, so cite the published FSE numbers. The simulated users may overstate the gain.
- The paper states its premise outright: LLMs' code-generation accuracy suffers when they get ambiguous requirements and do not detect them and ask for clarification. In the evaluated setting, resolving the ambiguity before generation, by asking targeted questions, measurably improves functional correctness. This supports the practice of making missing decisions discoverable before implementation.

## https://link.springer.com/article/10.1007/s00766-024-00427-0

Date: 2025-01-27 (arXiv v3; published in ACM TOSEM); quality: primary

- Code LLMs usually generate code instead of asking clarifying questions when a problem description has been deliberately made ambiguous, inconsistent or incomplete. More than 60% of responses go straight to code.
- Modifying the 164 HumanEval problems into 762 ambiguous, inconsistent or incomplete variants lowers most Code LLMs' Pass@1 by 35-52% and Test Pass Rate by 17-35%, with statistical significance in over 75% of the comparisons. The paper's significance cutoff is p<0.1.
- Of the three defect types, inconsistency (examples or tests that contradict the description) gets the fewest clarifying questions. Incompleteness gives the lowest Pass@1, 12.8%-46.95% across models. So contradictions between the examples and the prose often pass without comment.
- The Okanagan agent, built on ChatGPT 3.5, explicitly checks for ambiguous parts before writing the final code. Compared with the plain models, it raises Communication Rate by an absolute 58%, Good Question Rate by 38%, Pass@1 by 8% and Test Pass Rate by 7%.
- The authors list these limitations: the manual problem modifications are subjective, the metrics depend on an LLM-based evaluator, and results were not tested on any other dataset. This limits how far the findings transfer beyond small HumanEval-style Python functions.

## https://arxiv.org/abs/1611.10288

Date: 2026-03 (arXiv 2603.26233; v3 dated 7 Sep 2026); quality: primary

- On an underspecified variant of SWE-bench Verified (500 issues with details removed by GPT-4o summarization; OpenHands agent), removing issue details cut the Claude Sonnet 4.5 resolve rate from 70.8% (FULL) to 54.8% (HIDDEN, no interaction). Kimi K2.6 fell from 72.8% to 55.4%.
- A multi-agent scaffold, in which a separate Intent Agent watches for underspecification and can stop the main coding agent to ask the (simulated) user, recovered most of the lost performance: 69.4% resolve rate against 70.8% with a full spec. A single agent merely prompted to check for ambiguity reached only 61.2%.
- Telling the agent to always ask questions first got a high resolve rate with Claude (70.4%) by asking on nearly every task: it queried on 496 of 500 tasks. With Kimi K2.6 the same strategy did worse than no interaction at all (47.2% vs 55.4% HIDDEN). Clarification prompting does not transfer reliably between models.
- How well agents judge when to ask varies by model. Claude UA-MULTI asked more often on harder tasks (+9.28% ask rate on medium vs easy tasks). Kimi UA-MULTI asked on 82.99%-100% of tasks at every difficulty level and averaged 8.71 queries per task, against 3.06 for Claude.
- The results rest on a GPT-5.1 user simulator limited to three turns. The authors note simulated users may be unnaturally cooperative, so the gains may overstate what happens with real humans. The multi-agent scaffold also costs more: $3.50 vs $2.03 per task for Claude.

## https://www.es.mdu.se/pdf_publications/7171.pdf

Date: 2025-09-26 (v2; v1 April 2025); quality: primary

- Citing HumanEvalComm, the paper says code LLMs produce code without asking for needed clarification in more than 63% of ambiguous, incomplete or inconsistent problem statements. The task wording is left underspecified and the model fills the gap with its own assumptions instead of raising them.
- On HumanEvalComm, instruction-tuning DeepSeek Coder 7B on synthetic clarify-aware data raised the communication rate, meaning how often the model asks a question instead of writing code, from 24.12% to 63.61%. The rates were scored by a GPT-4o-mini judge.
- A GPT-4o-mini judge rated 51.93% of ClarifyCoder's clarifying questions as good, against 23.03% for DeepSeek Chat. Clarification-seeking can therefore be trained, but the paper reports no human validation beyond a 100-sample check.
- Training for clarification did not hurt code generation on clear requirements. On HumanEval, the answer-only-loss variant scored 74.85% Pass@1, against 73.62% for the base DeepSeek Coder.
- Code written after a clarification round was worse. In category 1a, ClarifyCoder's second-round Pass@1 was 23.71% against 48.05% for the baseline. A model that is better at asking questions is therefore not automatically better at turning the answers into correct code. All results are preliminary and come from synthetic data at the 7B scale.

## https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/

Date: 2003-11 (Version 1.0, November 2003); quality: primary

- The handbook classifies linguistic ambiguity into four broad classes: lexical, syntactic (structural), semantic, and pragmatic. The classes overlap, and it treats vagueness/generality and 'language error' as related categories. This is an expert taxonomy, not an empirical frequency study.
- It separates language ambiguities, which any careful reader can spot and writing rules can address, from software-engineering ambiguities. The second kind depends on domain knowledge or missing information and can only be found by readers with domain knowledge. The pump example: 'water level remains above 100 meters for more than 4 seconds' allows at least four interpretations, and the engineers silently assumed one of them, which was unsafe.
- Comparing several stakeholders' independent interpretations, and paraphrasing an interpretation back to the author, are called perhaps the most effective ways to find ambiguity. The handbook also says they cost the most, so they are justified only when undetected ambiguity would cost at least as much. This is the authors' judgment, and no measurements are given.
- Unrecognized (unconscious) disambiguation means a reader takes the first meaning that comes to mind as the only one. Citing Gause, the handbook ranks it among the top five sources of requirements failure. It also warns that an ambiguous SRS can lead implementors to work under different assumptions, each confident they are correct.
- Documentation controls: glossaries reduce lexical ambiguity, but creating and validating them takes considerable effort. In the authors' Tamagotchi experiment with 58 students, a term's meaning could still shift (polysemy) despite a glossary. Adding context such as rationale, fit criteria/test cases and inverse requirements is recommended to narrow the possible interpretations.

## https://arxiv.org/abs/2502.13069v3

Date: 2016-11-27 (arXiv v1); JSS 2017, DOI 10.1016/j.jss.2016.02.047; quality: primary

- Automated requirements smell detection with the Smella prototype achieved an average precision of 59% and an average recall of 82%, with high variation across cases. This is a measured result from cases in three industrial contexts and one university context, so roughly 4 in 10 flags are false positives.
- Requirements Smells are a lightweight static analysis, adapted from code smells and based on ISO 29148 quality violations, meant to run as soon as requirements are written. The authors position it as a supplement to reviews, not a replacement for them.
- Some smell categories could not be clearly told apart in practice, so the smell definitions themselves are ambiguous and need refinement.
- Practitioners in the evaluation reported more awareness of quality defects. This benefit is qualitative and self-reported, not a measured reduction in defects.
- The motivation is that poor requirements quality is costly when iterations are long and feedback arrives late, which argues for rapid automated checks while requirements are being written.

## https://arxiv.org/pdf/2406.00215

Date: 2024-08-18; quality: primary

- Großer, Ahmadian, Rukavitsyna, Ramadan and Jürjens (Requirements Engineering journal, 2024, 'Benchmarking requirement template systems: comparing appropriateness, usability, and expressiveness') compared free-text requirements against versions rewritten in five template systems (EARS, Adv-EARS, Boilerplates, MASTeR, SPIDER). Across 1764 requirements and seven quality characteristics, every template system except SPIDER had positive effects on all characteristics. The Springer page was behind a JS challenge, so this and the other claims rest on the abstract retrieved from Crossref, not the full text.
- In a user experiment with 43 participants, mostly students, comparing MASTeR and EARS for reading and writing, the authors found that templates need substantial prior training, and that understanding and writing requirements depends on deep domain knowledge and experience whether or not a template is used. This is evidence of real author and reviewer cost. The student sample limits how far it transfers to practitioners.
- No template system was a clear winner. MASTeR scored best overall, but the effect sizes of the systems were mostly similar, so the evidence does not favour one particular template (for example EARS over the others).
- MASTeR and Boilerplates (Rupp-style) offer the most variants for phrasing requirements and scored best on completeness. Analysis of the systems' meta-models against the Bunge-Wand-Weber ontology showed different levels of formality, modularity and expressiveness.
- The authors say earlier studies of template effectiveness each looked at a single notation, so before this benchmark there was no systematic comparative evidence on the quality benefits of templates. This marks the earlier evidence base as thin.

## https://2024.esec-fse.org/details/fse-2024-research-papers/89/ClarifyGPT-A-Framework-for-Enhancing-LLM-based-Code-Generation-via-Requirements-Clarification

Date: 2016-11-27 (arXiv v1); Empirical Software Engineering 2017, DOI 10.1007/s10664-016-9451-7; quality: primary

- In the NaPiRE survey of 228 companies in 10 countries, respondents picked their five most critical problems from 21 predefined RE problems. 'Incomplete and/or hidden requirements' was cited most often (109, 48%). Next came communication flaws between the project team and the customer (93, 41%), then moving targets and underspecified requirements (76 each, 33%). Inconsistent requirements were 9th (44, 19%). 'Terminological problems' was on the 21-item list but did not reach the top 10.
- Frequency and consequence differ. Respondents linked communication flaws with the customer to project failure more often (45 times) than incomplete or hidden requirements (43), even though incomplete requirements were cited more often. Moving targets were linked to failure more often (39) than underspecified requirements (28), although both had the same frequency (76).
- Incomplete and/or hidden requirements was the only problem consistently in the top 3 across all clusters of process model (agile vs plan-driven) and company size (small/medium/large).
- The most-cited causes of RE problems were organisational and skill-related: lack of time (18%), lack of experience of RE team members (18%) and weak qualification of RE team members (14%). No cause was cited by more than 20% of the organisations overall. The authors report that lack of experience leads mainly to incomplete/hidden requirements and to underspecified requirements.
- The evidence is self-reported perception, not measured defect data. The authors also say that their closed questions and the coding of qualitative answers limit validity. This weakens how far the rankings transfer to defect frequency in a small docs-as-code or AI-agent setting.

## https://www.alphaxiv.org/abs/2603.26233.md

Date: 2025 (SN Computer Science 6:314; received 21 Nov 2023, accepted 27 Feb 2025); quality: primary

- In a small controlled experiment (10 participants with limited EARS experience, 3 short natural-language requirements, one hour after an EARS lesson), participants rewrote requirements in EARS easily, and the most common problem was that the source requirements were incomplete, not that the syntax was hard to use.
- Applying the EARS templates exposed missing decisions in the natural-language requirements, such as failure handling and startup/default/safe states. Participants could not pick a template until those gaps were resolved, so templating worked as a way to find underspecification.
- Different participants mapped the same requirement to different EARS patterns (ubiquitous, event-driven, state-driven, unwanted behavior) depending on how they read it. The authors call this flexibility, but it also shows that EARS does not guarantee a single interpretation. The choice of pattern affected which tests were derived, for example 'shall not' forms led to tests of unwanted behavior only.
- Participants were unsure whether to use one EARS template or several to cover both positive and negative behavior, and found it hard to tell from the requirements which system perspective or level (system vs subsystem) was meant.
- The authors admit major validity limits: only 10 participants and 3 short, low-complexity requirements; the authors themselves turned the EARS requirements into test cases, which may bias results; challenges were captured only roughly through think-aloud. Their claimed effectiveness against manual industrial PLC testing (for example 26 Test Actions) comes from a single case study, not a controlled comparison.

## https://arxiv.org/html/2504.16331v2

Date: 2009; quality: primary

- EARS proposes a small structural ruleset meant to address eight common problems in natural-language requirements, including ambiguity, complexity and vagueness.
- EARS claims that all natural-language requirements can be written in one of five simple templates.
- The evidence is a single industrial case study: aero engine control system requirements extracted from an airworthiness regulation document. It is not a controlled experiment, and the abstract gives no numbers.
- The authors argue that constrained natural language is better than non-textual notations, because translating requirements into a new notation can introduce errors and adds training overhead.
- The authors cite training cost as a reason to prefer a lightweight template approach over new notations.

## https://link.springer.com/10.1007/s10664-023-10397-6

Date: 2022-12-02 (arXiv preprint v1); published in Empirical Software Engineering 2023/2024; quality: primary

- In a current-state snapshot, 28.9% of the top-1000 GitHub projects had at least one outdated code element reference in their README/wiki documentation, compared with 5.4% of Google projects. Outdated references made up 3.9% of all detected references in the top-1000 set.
- Over the full project history, 82.3% of sampled top-1000 projects and 29.7% of Google projects had outdated code element references at some point. Outdated references often persist: about 55% (top-1000) and 45% (Google) were still present one month later, and many lasted for years.
- Outdated references were resolved by changing the code about as often as by changing the docs. In the top-1000 set, 47.6% of resolutions changed the source code, 39.1% updated the documentation and 13.3% deleted the documentation.
- The regex-based detector (DOCER) produces false positives that maintainers must verify by hand. Of 15 projects that received issues, 4 responded positively and 4 called the reports false positives; 5 of the 19 reported instances were fixed.
- The approach catches only references to code elements that no longer exist anywhere in the source. It cannot detect semantically outdated documentation whose referenced elements still exist, and it was not integrated into CI; a GitHub Action is listed only as future work.

## https://dl.gi.de/items/690677a5-bbad-45af-8843-2380ea5ee92f/full

Date: 2016-02 (SE 2016 summary of EMSE 2015 paper); quality: primary

- In a controlled experiment with 71 subjects re-performing real maintenance tasks on two third-party projects, half the tasks were done with requirements traceability and half without.
- Subjects with traceability were on average 24% faster on a given maintenance task.
- Subjects with traceability produced on average 50% more correct solutions. Solutions were sketched on paper, so the study measured problem solving rather than programming, which limits how far the result transfers to real implementation work.
- The authors conclude that traceability saves effort and improves maintenance quality. The record is the 2-page Software Engineering 2016 (LNI P-252) summary of the EMSE journal paper. The fetched page gives only the abstract, so trace-creation cost, statistical tests and limitations could not be checked from it.

## https://www.inf.usi.ch/faculty/lanza/PUBS/P/Wen2019a.pdf

Date: 2024-03-01; quality: primary

- A learning-based detector (CoCC), trained on features from code and comments before and after a change, detects outdated code comments at over 90% precision. The random forest variant reached about 92.1% precision, 78.9% recall and 0.850 F1 on Java, which means roughly a fifth of outdated comments were missed.
- The evaluation dataset held 49,648 code-comment pairs from 40,247 commits of open-source projects. CoCC beat the baselines on every metric: a rule-based approach scored about 0.405 F1, and the prior OCD tool recalled only about 12.5% of outdated method comments.
- Applied to recent commits of open-source projects, CoCC flagged 39 outdated comments in 900 commits (14 of them repeats). The authors confirmed 23 of the 25 distinct flagged comments as outdated. So outdated comments do occur in practice after code changes, but at a low rate per commit.
- The detector only examines changes inside the linked code-comment pair, and it links code to comments with heuristics. A change elsewhere that makes a comment or document stale, which is the cross-artifact drift a docs-as-code repo faces, is therefore not detected.
- Performance carries over to a second language with a small drop: about 89.4% precision, 75.7% recall and 0.820 F1 on Python, against about 92.1% precision, 78.9% recall and 0.850 F1 on Java.

## https://arxiv.org/abs/2403.00251v1

Date: 2019; quality: unreliable


## https://strictdoc.readthedocs.io/en/stable/strictdoc_01_user_guide.html

Date: 2026-10-22; quality: primary

- StrictDoc is a text-based (docs-as-code) requirements management tool. It accepts SDoc and Markdown input, and Markdown support is labelled experimental.
- StrictDoc enforces structural validation on requirement relations: circular parent/child references raise validation errors. Its default grammar also requires a STATEMENT or TITLE field on each node.
- StrictDoc supports Parent, Child and File relation types. Its traceability between requirements and source files is labelled experimental, and parsing SDoc nodes from source comments works only for C/C++ and Rust.
- StrictDoc puts no constraint on UID format, and it shows parent/child links only when both linked requirements have a UID. The team therefore has to define its own ID convention.
- The docs (version 0.30.4, built 2026-10-22) say the project is under active maintenance. They also state that the web interface is work-in-progress and the web server is not hardened. Export targets include HTML, RST, ReqIF, PDF, JSON and Excel, and the grammar can be extended with custom fields.

## https://sphinx-needs.readthedocs.io/en/stable/changelog.html

Date: 2026-11-04; quality: primary

- Sphinx-Needs was actively maintained as of late 2026. The latest release on the page is 9.2.0, dated 04.11.2026 (4 November 2026), and 9.1.0 came out on 22.10.2026.
- Sphinx-Needs 9.2.0 lets a need type declare how many incoming links it must receive (back_links) and the shape of its IDs (id_regex). Both are machine-checkable traceability and stable-ID constraints. A constraint can also carry a severity, so a violation is reported rather than failing the build.
- Sphinx-Needs 9.2.0 records where each need's text came from (marked provisional), and filters can read this as c.source. It also adds link types that derive the far ends of a chain, plus a 'summary' link type that marks a shortcut across the trace.
- Recent releases have breaking changes that add maintenance cost. 9.2.0 deprecates add_need, which 10.0 removes, and needs ub-project 1.2.0. In 9.1.0, the built-in GitHub services are registered only when needs_services names them.
- Sphinx-Needs 9.2.0 reports configuration problems as named warnings (e.g. needs.config, needs.type_conflict). Two names that differ only in case stop the build.

## https://github.com/itsallcode/openfasttrace/blob/main/doc/user_guide.md

Date: None; quality: primary

- Vale is an open-source command-line linter for prose that checks writing style rather than grammatical correctness, and it ships no built-in advice of its own: every rule comes from styles the team configures.
- Teams write custom Vale rules as YAML files, with optional regular expressions, through an extension system. A 'substitution' rule uses a 'swap' map to flag a disallowed term and suggest the preferred one, and it can match case-insensitively. This lets a team enforce its terminology automatically.
- Setting a Vale rule's severity to 'error' fails the CI build. So a rule can run as a hard check or, at lower severities, as an advisory one. An official GitHub Action exists for running Vale.
- Vale understands markup structure. It ignores block and inline code by default and uses an NLP library, which reduces false positives on code identifiers inside Markdown docs.
- Vale is 100% open source under the MIT license.

## https://docs.vale.sh/topics/readme.md

Date: Undated living doc; repository HEAD checked 2026-10-18; quality: primary

- OpenFastTrace (GPL-3.0) is a requirement tracing tool that works on Markdown spec items plus coverage tags put in source code, so it fits a docs-as-code repo. The URL given has moved: it is now doc/user_guide/user_guide.md, an index page linking to sub-pages.
- OFT spots drift between a spec and the code or tests derived from it through revision numbers. Raising a spec item's revision voids every existing coverage link, so coverage that still names the older revision is reported as 'Outdated', which fails the trace.
- The tool sorts each link into a fixed status. Outdated (covers an older revision), Predated (covers a newer one) and Orphaned (covers an item that does not exist) all count as failures. The guide calls outdated-coverage detection one of OFT's most useful safeguards. This is the vendor's own view, with no measured data behind it.
- Drift detection only works if authors raise the revision by hand when the meaning of an item changes. OFT cannot catch a semantic change made without a revision bump. This limitation is my inference from how the revision mechanism is described.
- Spec items state which artifact types must cover them (for example 'Needs: impl, utest'), so the trace can report missing coverage. Tracing with an artifact type filter removes coverage requirements outside the filter, and the trace can then pass even though downstream artifacts are missing. That makes this a possible false-completeness trap.

## https://arxiv.org/abs/2602.11988

Date: 2026-02-12 (v1; revised v2 2026-06-23, v3 2026-09-29); quality: primary

- On SWE-bench tasks with LLM-generated context files, and on a new set of issues from repositories that have developer-committed context files, adding repository-level context files such as AGENTS.md does not generally raise coding-agent task success rates. The abstract reports this null result across several LLMs and agents, and for both generated and developer-written files.
- Context files raise agent inference cost by more than 20% on average. This is a measured cost of the control, and it is not offset by a general gain in success.
- Coding agents follow instructions written in context files. Compliance is high, but it does not turn into higher task success. That gap is evidence of surface compliance: following an instruction is not the same as getting the outcome right.
- Repository overviews in context files do not help agents, even though they are popular and model providers recommend them. Generic descriptive context is a low-value control.
- Context files are useful mainly for stating non-standard coding practices, meaning repo-specific conventions an agent cannot infer. The authors advise evaluating any context file rigorously before deploying it.

## https://arxiv.org/abs/2601.20404

Date: 2026-01-28 (v1); revised 2026-03-30 (v2); quality: primary

- In a paired experiment on 10 repositories and 124 small PR tasks, running OpenAI Codex (gpt-5.2-codex) with the repository's AGENTS.md present was associated with a 28.64% lower median wall-clock runtime than running it without the file (mean 162.94s vs 129.91s, Wilcoxon p<0.05).
- With AGENTS.md present, output token consumption fell by 16.58% at the median (median 2,925 to 2,440; mean 5,744.81 to 4,591.46). Input and total tokens fell by about 9-10% at the mean, but those reductions were not reported as statistically significant.
- The paper did not evaluate output correctness or quality. 'Comparable task completion' rests only on a manual sanity check of 50 sampled tasks, which confirmed the outputs were non-empty and non-trivial. So the study shows efficiency effects, not effects on correctness or alignment with the contract.
- The results may not generalize. The study used one agent and one model, tasks limited to 100 LoC or less and 5 files or less (code-only changes), and at most 15 PRs per repository. Some task descriptions were generated by an LLM (gpt-oss-120b).

## https://research.trychroma.com/context-rot

Date: 2025-07-14; quality: primary

- Across 18 frontier and open models (Claude 4/3.x, GPT-4.1/4o/o3, Gemini 2.5, Qwen3), LLM performance becomes less reliable as input length grows, even on deliberately simple retrieval/replication tasks where task difficulty is held constant.
- On LongMemEval (306 prompts), every tested model scored significantly higher with a focused ~300-token prompt containing only relevant content than with the full ~113k-token prompt; thinking modes narrowed but did not close the gap. This bears on local explanation vs. loading large distant context for agents.
- Topically related but non-answering distractor passages reduce accuracy; a single distractor lowers accuracy below the needle-only baseline and four distractors compound the drop. Inference: near-duplicate or outdated related text in a repo (stale docs, similar sections) could mislead agents.
- Degradation with input length is steeper when the question and the relevant passage have low semantic similarity, meaning the wording does not match. Inference: when spec terms differ from the terms used in a task, retrieval from long context becomes less reliable.
- Counterintuitively, haystacks whose sentences were randomly shuffled gave better needle retrieval than logically coherent haystacks, consistently across all 18 models. The study is limited to two haystack topics, gives no explanation of the mechanism, and uses synthetic tasks.

