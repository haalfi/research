# M2: Evaluation protocols for LLM-generated tests, specs and models (trial-design brief §3 items 3, 4, 5, 7, 8)

Scope: experimental method only, for running and measuring arms in which LLM agents of different lineages write spec-enforcing tests, expectation tests, specs and models. No spec methods are re-surveyed.

Conventions: grades A / A-pre / A-workshop / B / C / D. "FT" = full text read (yes / partial / no). **[unreachable]** = full text not fetched, lead only. *Inference* = my own reasoning, not a source finding. "Own calculation" = computed in this run (scipy 1.18.1 / statsmodels in a scratchpad venv; script `/tmp/claude-0/-home-user-research/8464aabb-24d6-53c7-af9a-cc609bb4c0f8/scratchpad/m2calc/calc.py`). Recommendations are numbered M2-R1 to M2-R17. Each one says what it can and cannot show at small n.

Grading notes: ICSE-NIER (4–5-page new-ideas track) is graded A-workshop. GEM and Eval4NLP are ACL workshops (A-workshop). Euromicro SEAA is graded A (peer-reviewed conference). Where no venue could be confirmed through arXiv metadata or Crossref, the grade is A-pre.

---

## Q1. Repeated sampling, variance and reporting standards (runs per configuration, temperature, seeds, contamination, version pinning, prompts, cost)

### Takeaway
Temperature 0 and a fixed seed do **not** make hosted LLMs deterministic. Single runs are therefore not admissible evidence for one arm's kill count. The SE guidelines (Baltes, Wagner et al., EMSE, accepted) require that model version, configuration, date, all prompts and (as a should) traces and token/dollar cost be reported, and that repetitions be repeated and the number of repetitions justified. **No source gives a fixed "right" number of runs.** The studies read used 5 runs (Ouyang; Kapoor), 10 runs (Sallou; Atil) and 3 runs (PBT-Bench, cited in the verified edition).

### Cited Findings
- **Ouyang, Zhang, Harman, Wang, "An Empirical Study of the Non-determinism of ChatGPT in Code Generation", TOSEM (DOI 10.1145/3697010, issued 2025) (A; FT yes).** They made 5 requests per task on 829 problems (CodeContests, APPS, HumanEval). At default temperature 1, "the ratio of coding tasks with zero equal test output across different requests is 75.76%, 51.00%, and 47.56%". The "maximum difference of the test pass rate reaches 1.00 for all three datasets, and accounts for 39.63% of the problems in HumanEval". "Setting the temperature to 0 does not guarantee determinism in code generation, although it indeed brings less non-determinism". Only 21.1 % of 76 surveyed LLM code-generation papers considered non-determinism. Recommendation: "researchers can report the average results, variance, or distribution from multiple requests". Test pass rates were similar across temperatures 0, 0.5 and 1, so "low temperature might be a better choice given the comparable test pass rate" — [arXiv 2308.02828](https://arxiv.org/abs/2308.02828)
- **Atil et al., "Non-Determinism of 'Deterministic' LLM Settings" (arXiv v5; published as "…System Settings in Hosted Environments", Eval4NLP 2025, DOI 10.18653/v1/2025.eval4nlp-1.12) (A-workshop; FT yes, arXiv version).** Five LLMs, 8 tasks, 10 runs at temperature 0, top-p 1 and a fixed seed showed "accuracy variations up to 15% across naturally occurring runs with a gap of best possible performance to worst possible performance up to 70%". "None of the LLMs consistently delivers repeatable accuracy across all tasks, much less identical output strings." They propose TARr@N (identical raw output across N runs) and TARa@N (identical parsed answer across N runs) — [arXiv 2408.04667](https://arxiv.org/abs/2408.04667)
- **Renze & Guven, Findings of EMNLP 2024 (A; FT abstract and setup).** On MCQA problems, nine LLMs: "changes in temperature from 0.0 to 1.0 do not have a statistically significant impact on LLM performance for problem-solving tasks". This is MCQA, not code or test generation — [arXiv 2402.05201](https://arxiv.org/abs/2402.05201)
- **Sallou, Durieux, Panichella, ICSE-NIER 2024 (A-workshop; FT yes).** "Running the LLMs' inference only once is insufficient to ensure reproducibility … we argue in favor of conducting multiple replication runs and using variability metrics". Their showcase queried ChatGPT-3.5 "ten times over different days" for JUnit tests: Math-5 had 70 % branch coverage with an IQR of 27.5 % and between 1 and 2 failing tests; Chart-11 had between 1 and 5 failing tests. Metadata to provide: model version and seed, exact prompts, date of query, output-variability metrics, scope. Leakage mitigations: metamorphic (renamed or obfuscated) inputs, multiple data sources, and code clone detection of generated tests against online code. After renaming in Math-5, ChatGPT "always created non-compiling tests" — [arXiv 2312.08055](https://arxiv.org/abs/2312.08055)
- **Baltes, Angermeir, …, Prechelt, Ralph, van Tonder, Wagner, "Guidelines for Empirical Studies in SE involving LLMs", EMSE accepted manuscript (arXiv v8, Sep 2026) (A; FT yes for §§5.2, 5.4, 5.5, 5.7, 5.8)** (the llm-guidelines.org text).
  - §5.2, "must": "report the exact LLM model or tool version, configuration, and date of study execution". A temperature of 0 is not "a guarantee of reproducibility".
  - §5.3, "must": "publish all prompts as supplementary material" and state which prompt was used for which model.
  - §5.4, "should": full interaction logs and runtime traces, covering "tool name, arguments, result, ordering" and which skills, context files and subagents "were activated". Ronanki et al. are cited as an example of uploading full answers to Zenodo.
  - §5.5: "experiments should be repeated; the result distribution should then be reported using descriptive statistics … Researchers should justify the number of experiment repetitions, for example through a power analysis or by monitoring convergence of descriptive statistics". McNemar's test is named for binary outcomes. When scores vary across raters or across runs of an LLM judge, report "the distribution of ratings per item rather than only aggregated point estimates".
  - Contamination: a held-out subset, "canary strings, that is, unique markers that downstream tools can later search for in model outputs", and checks against training corpora.
  - §5.8: "Cost accounting tracks resource consumption by reporting tokens, service costs, or hardware specifications."
  - [arXiv 2508.15503](https://arxiv.org/abs/2508.15503)
- **Kapoor, Stroebl, Siegel, Nadgir, Narayanan, "AI Agents That Matter" (A-pre; venue not verified; FT §§1–3).** "Useful agent evaluations must control for cost"; accuracy "can be improved by scientifically meaningless methods such as retrying". They "measure dollar costs instead of using proxies", separate fixed (tuning) from variable (per-run token) costs, and "run each agent five times and report the mean accuracy and the mean total cost" — [arXiv 2407.01502](https://arxiv.org/abs/2407.01502)
- **Srivastava et al., BIG-bench, TMLR (A; FT the canary section).** All task files carry a canary GUID "intended to help researchers filter BIG-bench data out of web-scraped training corpora" and support "post-hoc diagnosis of whether BIG-bench data was used in model training" — [arXiv 2206.04615](https://arxiv.org/abs/2206.04615)

### Inferences
- **M2-R1 (runs per configuration).** Run each (arm × generating model) configuration **k = 5 independent sessions** at the provider's lowest temperature, with the seed logged. Report the per-misreading kill frequency (0–5 of 5), not the best run. Sources: Ouyang (A, FT) and Kapoor (A-pre, FT) use 5; Atil uses 10. *Inference* for the choice of 5 over 10: cost. *Can show*: whether a kill is stable (5/5) or a sampling accident (1/5). *Cannot show*: a precise per-configuration kill probability. A Wilson 95 % interval for 5/5 is [0.57, 1.00] (own calculation, same method as Q3). k = 5 is a stability screen, not an estimate. Baltes §5.5 asks that k be justified. The justification here is cost plus the stability-screen purpose, stated as such.
- **M2-R2 (unit of analysis).** The seeded misreading, not the run, is the unit of analysis. Collapse the k runs per misreading to "caught by the arm's majority (≥ 3/5)", and report "caught in any run" separately. This avoids pseudo-replication: runs of one model on one item are not independent observations. *Inference*. It follows Baltes §5.5's per-item distribution advice.
- **M2-R3 (temperature).** Prefer temperature 0 or the provider minimum for generating arms. Keep a decoding setting fixed **within** a lineage across arms, so that arm and temperature are not confounded. Sources: Ouyang (pass rates comparable at low temperature) and Renze (no significant effect for 0–1, MCQA only). *Cannot show*: that temperature does not change *which* misreadings are caught. No source measures that.
- **M2-R4 (reporting pack).** Release a reporting pack covering the model ID string as returned by the API, the date and time of every call, all prompts and templates, the read-scope manifest per session, full session traces, and tokens in, tokens out and dollars per session. Sources: Baltes §§5.2–5.4, 5.8 (A, FT) and Sallou (A-workshop, FT). This is a reproducibility requirement, not evidence for any hypothesis.
- **M2-R5 (contamination).** The operation's records are private project artefacts. Pre-training contamination is therefore unlikely for the records themselves. *Inference*: the residual risks are (a) public look-alike APIs and (b) the earlier reports, if they are public on GitHub. Mitigation: rename domain identifiers in a metamorphic copy of the operation and run one arm on both copies (Sallou's renaming check). *Can show*: a large drop on the renamed copy signals reliance on memorised context. *Cannot show* the absence of contamination.

### Gaps
- No source gives a power-analytic or convergence-based number of runs for *test-generation* arms. Baltes §5.5 asks for justification but gives no number.
- Ronanki et al. are known to me only as Baltes's reporting example. Their own paper was not read.
- Benchmark-contamination detectors for private, non-benchmark artefacts were not searched beyond the canary and renaming mechanisms.

---

## Q2. Lineage and model assignment: making arms independent and *verifying* independence

### Takeaway
Kim et al.'s measure, agreement when both models are wrong compared with chance, needs categorical wrong answers and many items on which both models fail. At a trial size of 20–50 seeded misreadings, the number of items both arms miss is typically 1–8, and the chance band covers almost [0, 1] (own calculation). The measure is **not usable as a decision statistic at this n**. The accuracy-adjusted **error-consistency κ** (Geirhos; extended as CAPA by Goel et al., ICML 2025) works on the per-item caught/missed vectors the trial already produces. Even so, at n = 30 only |κ| ≳ 0.35–0.40 is distinguishable from independence. Overlap (kill-set Jaccard) must be compared against its chance value given kill rates, not against 0. Leakage checks (canaries, read-scope logs) detect only verbatim and logged access.

### Cited Findings
- **Kim, Garg, Peng, Garg, "Correlated Errors in Large Language Models", ICML 2025, PMLR 267 (A; FT yes).** The metric is the "agreement rate when both models err". It is chosen to "reduce confounding based on model accuracy: two independently accurate models will agree on a large fraction of questions in which they both give the correct answer". The chance baseline under uniform random wrong answers is 1/3 on HELM (3 wrong options) and 0.127 on HuggingFace, where the paper gives the formula Σ_k p_k/(k−1) over questions with k options. Results: 0.423 (HF) and 0.6 (HELM), with "100% of pairs on HuggingFace; 97.5% on Helm" above baseline. "Models by the same developer, using the same base architecture, and having similar sizes are all associated with higher agreement"; "more accurate models … are more correlated". The features explain 34–62 % of the variation. Some unexpected pairs (google/text-unicorn@001 and writer/palmyra-x-v3) agree on 0.9987 of joint errors "with no publicly stated direct relationship". Judges "systematically inflate the accuracy of models that are less accurate than itself". The authors note that Goel et al.'s metric "may be preferable when such probabilities are available" — [arXiv 2506.07962](https://arxiv.org/abs/2506.07962)
- **Goel et al., "Great Models Think Alike and this Undermines AI Oversight", ICML 2025, PMLR 267 (A; FT §2).** Error consistency (Geirhos et al., 2020) uses c_obs, the fraction of items where both models are correct or both are wrong, and c_exp = acc1·acc2 + (1−acc1)(1−acc2). κ = (c_obs − c_exp)/(1 − c_exp), "similar to Cohen's κ". Two of its limits: it counts different wrong answers as agreement, and it ignores probabilities. CAPA (κp) fixes both using output probabilities. They report that LLM-as-judge favours similar models and that "model errors are getting more correlated as capabilities increase" — [arXiv 2502.04313](https://arxiv.org/abs/2502.04313)
- **Own calculation (null distributions under true independence, 20,000 simulations each).**
  - *Error-consistency κ*, two independent arms, each catching a given misreading with probability acc. The 95 % null range is [−0.34, 0.36] at n = 30, acc = 0.6; [−0.27, 0.38] at n = 30, acc = 0.8; [−0.28, 0.27] at n = 50, acc = 0.6; and [−0.18, 0.20] at n = 100, acc = 0.8.
  - *Agreement-when-both-wrong* (Kim), k equally likely wrong options. At n = 30, acc = 0.8, the median number of items both arms miss is 1, and the 95 % null band is [0, 1] for k = 2, 3 and 5. At n = 50, acc = 0.6, the median is 8 jointly missed items, and the band is [0.00, 0.71] for k = 3.
  - *Kill-set Jaccard*, M mutants, independent kills at rate r per family. The expected Jaccard is r²/(2r − r²): 0.33 at r = 0.5 and 0.67 at r = 0.8. The 95 % band is [0.48, 0.83] at M = 30, r = 0.8, and [0.58, 0.75] at M = 120, r = 0.8.
- **Sallou et al. (A-workshop; FT yes)** recommend "well-established code clone detection techniques" to check generated tests against existing code — [arXiv 2312.08055](https://arxiv.org/abs/2312.08055). Their purpose is training-data leakage, not inter-arm overlap.
- **Baltes et al. §5.5 (A; FT yes)**: canary strings as "unique markers that downstream tools can later search for in model outputs"; **§5.4**: runtime traces should record every tool call with its arguments and results, and "which configured artifacts … were activated" — [arXiv 2508.15503](https://arxiv.org/abs/2508.15503)
- **Earlier report, quoted verbatim before qualification.** The verified edition (Table row) reads: "When both models are wrong they pick the same wrong answer 0.423 (chance 0.127) and 0.60 (chance 1/3) of the time". This run confirms these figures against the full text. The verified edition also reads: "Swapping provider reduces correlation but does not remove it." Kim's regression supports a same-developer effect. The size of the residual cross-provider correlation for *test or spec writing* is not measured by Kim (MCQ only).

### Inferences
- **M2-R6 (lineage assignment).** Assign the spec/model lineage and the expectation-test lineage to **different developers and different base architectures**. Avoid pairing two frontier models when a deliberately weaker or differently trained model is available for one family. Sources: Kim's regression (same developer, architecture and size raise error agreement; accuracy raises it) and Goel (A, FT). This is *Inference* in transfer, because both papers measure MCQ, not test generation. *Cannot show*: that cross-provider assignment yields independence. Kim's unexplained 0.9987 pair shows that provenance alone is no guarantee.
- **M2-R7 (verify, don't assume: primary independence statistic).** For each pair of arms, build the n-length binary vectors "misreading caught (majority of k runs)". Report:
  - (a) the 2×2 table (both caught, only A, only B, neither);
  - (b) Geirhos error consistency κ with a bootstrap or exact-permutation 95 % interval;
  - (c) the permutation null computed from the observed marginal catch rates. This is the own-calculation procedure above, applied to the real data.

  Source: Goel §2 (A, FT) for the formula. *Inference* for its use on seeded-misreading vectors. *Can show at n ≈ 30*: gross dependence (κ ≳ 0.4) or gross complementarity (κ ≲ −0.35). *Cannot show*: "independent" in a positive sense. A κ inside the null band is compatible with moderate correlation, and the trial should say "dependence not detected", never "independent".
- **M2-R8 (Kim's measure: report only descriptively).** Kim's measure needs a categorical *wrong answer*. In this trial the natural analogue is the **same wrong expected value** or the **same misreading adopted**, among items both arms got wrong. Report the raw count, for example "3 of 4 joint misses share the same wrong expected value", with the chance rate stated only where the space of plausible wrong values is enumerable (e.g. a case table with 3 alternative outcomes). Do not test it at this n (own calculation: the null band is ~[0, 1]). *Inference*.
- **M2-R9 (overlap of generated oracles).** Report kill-set Jaccard per family pair **together with** its independence expectation r₁r₂/(r₁ + r₂ − r₁r₂) and a permutation band (own calculation). A Jaccard of 0.7 at kill rates of 0.8 is chance-level, not evidence of shared derivation. Add assertion-level overlap as a descriptive check: identical (input, expected-output) pairs across families, normalised for formatting, plus an off-the-shelf clone detector on the test code (Sallou's clone-detection suggestion, repurposed; *Inference*). *Cannot show*: semantic copying, i.e. the same misreading phrased differently. Only the error-consistency analysis on misreadings addresses that.
- **M2-R10 (leakage checks).**
  - (a) Embed **canary tokens** in the spec, the models and R: unique GUID-like identifiers in comments, plus distinctive invented constant or helper names. Grep every expectation-family artefact and session trace for them. Mechanism source: BIG-bench (A) and Baltes §5.5 (A). Their use for intra-study leakage is *Inference*.
  - (b) Record the **read scope** per session from the harness's runtime trace (Baltes §5.4) and from OS-level file-access logs. Report any read of a forbidden path as a protocol violation that excludes that session.
  - (c) Keep the earlier deep-dive layers: the import ban and the file-system read scope. Quoted verbatim: "in a fresh session holding only the records, enforced by a file-system read scope (R, spec and models not mounted). Import ban and runtime guard as backup".

  *Can show*: verbatim or logged access. *Cannot show*: paraphrased leakage, leakage through shared training data, or leakage through the human operator, who sees both sides. The single-maintainer threat in brief §2 is exactly that last channel.
- **M2-R11 (operator channel).** Prepare all prompts for the expectation family **before** the spec exists, freeze and hash them, and run that family in a session whose prompt can be byte-compared with the frozen file. *Inference*. It limits but cannot remove operator leakage through prompt edits.

### Gaps
- No study measures correlated errors of LLMs on **test or spec generation** (as opposed to MCQ) across lineages. The deep dive's D5 found none, and this run found none either.
- I found no validated assertion-level similarity metric for test oracles. Code clone detectors measure syntax, not oracle semantics. No source was read on this.
- CAPA needs output probabilities, which hosted chat APIs often do not expose for long generations. The probabilistic variant is therefore probably unavailable (*Inference*).

---

## Q3. LLM-as-judge versus human labels: estimating judge precision and recall on small labelled samples

### Takeaway
Judge studies agree on three protocol elements: order or position swapping (call twice and accept only consistent verdicts), chance-corrected agreement rather than raw percent agreement, and human reference labels built by ≥ 2 raters to a reliability threshold. Judges are also lenient: they favour "correct" verdicts and inflate the accuracy of weaker, correlated models. At the trial's likely label counts (20–50 judge verdicts per class), Wilson 95 % intervals are ±0.12 to ±0.20 wide. A judge's precision can only be bounded coarsely, not compared between judges.

### Cited Findings
- **Zheng et al., MT-Bench / Chatbot Arena, NeurIPS 2023 (A; FT §§3–4).** Biases: position, verbosity and self-enhancement. Swap protocol: "A conservative approach is to call a judge twice by swapping the order of two answers and only declare a win when an answer is preferred in both orders. If the results are inconsistent after swapping, we can call it a tie." Few-shot examples raised GPT-4 consistency "from 65.0% to 77.5%". GPT-4 agreed with humans 85 % (setup S2, no ties) against 81 % human–human. Humans "deemed GPT-4's judgments reasonable in 75% of cases and are even willing to change their choices in 34% of cases" when shown GPT-4's judgment. *Inference*: showing raters the judge's verdict contaminates the labels — [arXiv 2306.05685](https://arxiv.org/abs/2306.05685)
- **Jiang et al., CodeJudgeBench (A-pre; no venue found; FT §§4–5).** 26 judges on code generation, repair and **unit-test generation**. "Judging the correctness of unit test generation is the most challenging". Each pair was "evaluated twice", with the good response alternately in position A and B, and the results averaged. Order swaps changed accuracy by "up to 14%". Non-thinking models scored "below 60%, approaching the random guess baseline of 50%". Judge accuracy varied with which LLM wrote the code: judges "may not base their assessments solely on code correctness" — [arXiv 2507.10535](https://arxiv.org/abs/2507.10535)
- **Shi et al., "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge", AACL-IJCNLP 2025 (A; FT abstract + §2).** Three metrics: repetition stability, position consistency and preference fairness. 15 judges, ~150,000 instances. Position bias "is not due to random chance", "varies significantly across judges and tasks", and is "strongly affected by the quality gap between solutions". Their setting is double-blind: candidate identities are hidden from judges — [arXiv 2406.07791](https://arxiv.org/abs/2406.07791)
- **Thakur et al., "Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges", GEM 2025 workshop (A-workshop; FT §§3, 6, App. B).** They recommend "metrics beyond percent agreement, as judges with high agreement can still assign vastly different scores". They switched from Cohen's κ to Scott's π because of "well-documented theoretical issues", and recommend "computing both percent agreement and Scott's π, paired with qualitative analysis". On leniency: "P+ for most models is significantly higher than 0.5", i.e. a tendency to judge "correct" when in doubt. Some judges are "easily fooled by dummy answers like 'Yes' and 'Sure'" and are "better at detecting completely incorrect answers than partially incorrect ones" — [arXiv 2406.12624](https://arxiv.org/abs/2406.12624)
- **Kim et al. ICML 2025 (A; FT yes)**: each judge "systematically inflates the accuracy of models that are less accurate than itself, due to correlated errors" — [arXiv 2506.07962](https://arxiv.org/abs/2506.07962)
- **Baltes et al. §5.7 (A; FT yes)**: "inter-model agreement … such as Krippendorff's α > 0.8. Such agreement is necessary but not sufficient. High inter-model agreement can reflect shared model biases … validate a sample against human experts". The human reference procedure: randomly order objects into groups judged in "one to three hours". Two or three experts build decision rules jointly on the first group, then iterate independent rating, IRA/IRR, discussion and rule updates until α > 0.8 is "sustained for two to three groups", after which "it is permissible to continue with a single rater". Krippendorff's thresholds: discard data at α < 0.667, treat 0.667–0.8 as tentative, require ≥ 0.8 for reliable data — [arXiv 2508.15503](https://arxiv.org/abs/2508.15503)
- **Brown, Cai, DasGupta, "Interval Estimation for a Binomial Proportion", Statistical Science 16(2) 2001, DOI 10.1214/ss/1009213286 (A; [unreachable]: Project Euclid and UPenn returned HTML or 403).** A search extract (lead only) says they recommend Wilson or Jeffreys for small n and Agresti–Coull for larger n. Not verified against the full text — [DOI](https://doi.org/10.1214/ss/1009213286)
- **Own calculation (Wilson / Clopper–Pearson 95 %).**
  - 18/20 → Wilson [0.70, 0.97], CP [0.68, 0.99]
  - 27/30 → [0.74, 0.97] / [0.73, 0.98]
  - 45/50 → [0.79, 0.96] / [0.78, 0.97]
  - 9/10 → [0.60, 0.98] / [0.55, 1.00]
  - 0/20 → upper bound 0.16 / 0.17
  - 0/30 → upper bound 0.11 / 0.12
  - Labels needed for a Wilson half-width ≤ 0.10: n = 34 at p̂ = 0.9, n = 60 at p̂ = 0.8, n = 93 at p̂ = 0.5. For ≤ 0.15: 15, 26 and 39.
- **Earlier report, quoted verbatim.** Verified edition: "Best supported: cross-family judges must agree to accept, rejections go to a human, and the gate is calibrated on a human-labelled sample and recalibrated when the generating models change." The deep dive cites Kaufman et al. (A-pre, abstract + intro): "74 % accuracy on correct vs 49 % on incorrect assertions" by 86 programmers. **Qualification, not refutation:** "calibrated on a human-labelled sample" is sound, but at plausible sample sizes the calibration bounds precision only to roughly ±0.1–0.2 (own calculation). Kaufman's figure warns that the human labels themselves can be wrong on incorrect assertions, so a single human labeller is not a gold standard.

### Inferences
- **M2-R12 (judge protocol).**
  - (i) Each judge call is made twice, with candidate or clause order swapped (pairwise) or with item order randomised (pointwise). A verdict counts only if both calls agree; otherwise it is "inconsistent → human". Sources: Zheng (A), CodeJudgeBench (A-pre) and Shi (A), all FT.
  - (ii) Arm identity and the generating model are hidden from the judge (Shi's double-blind setting).
  - (iii) The judge lineage differs from both the artefact's generator and the spec lineage (Kim's inflation result).
  - (iv) Fix the judge's decoding settings, run each verdict k = 3 times, and report repetition stability (Shi; Baltes §5.5 per-item distribution).
- **M2-R13 (calibration set and judge precision/recall).**
  - Build the calibration set **before** looking at arm results: a stratified random sample of judge verdicts, half judged "violation / added commitment" and half judged "fine", with ≥ 30 per stratum where budget allows.
  - Two human raters label it independently, blind to the judge verdict and to the arm (Zheng's 34 % change-of-mind effect argues for hiding the judge verdict).
  - Report judge precision (P(human says violation | judge says violation)) and recall (P(judge says violation | human says violation)) with **Wilson** intervals, and Clopper–Pearson as a conservative check. Recall needs the human-positive set, so sample also from judge-negatives. Weight the strata back by their sampling fractions.
  - Report rater agreement as percent agreement plus Krippendorff's α or Scott's π (Thakur; Baltes). Cohen's κ may be added for comparability.
  - *Can show at n ≈ 30 per stratum*: whether precision is clearly high (lower bound ≳ 0.75 with 27/30) or clearly unusable (upper bound < 0.7). *Cannot show*: a difference between two judges of less than ~0.2, or precision on rare misreading types (fewer than 5 items each).
- **M2-R14 (human-label reliability as a gate).** Follow Baltes §5.7's round procedure for the ground-truth raters, who decide "is a misreading" and "is an allowed variant". Pre-register α ≥ 0.8 as reliable and 0.667–0.8 as "tentative", and report α per round. *Inference*: in a single-maintainer project the second rater is the scarce resource. If only one human is available, say so and downgrade every label-dependent measure to "single-rater, unvalidated". This follows from Baltes's "two or three human experts" and Kaufman's 49 % accuracy on incorrect assertions.

### Gaps
- No judge study found evaluates judges on **spec-faithfulness or added-commitment detection** against prose records. CodeJudgeBench's TestGen split (input–output pairs) is the closest, and it is *analogous* only.
- Brown, Cai & DasGupta is [unreachable]. The Wilson recommendation is cited only as a search lead. The interval computations above stand on their own as own calculations.
- I did not read a source on the kappa paradox under skewed prevalence beyond Thakur's appendix pointer (Pontius & Millones 2011; Chicco et al. 2021 [unreachable]).

---

## Q4. Human-time and compute-cost measurement

### Takeaway
Time on task needs a predefined start event, end event and success criterion. It trades off against quality, so measure both. For compute, report dollars and tokens per session (variable cost) separately from setup or tuning (fixed cost), with means over repeated runs. I found no SE source that directly compares think-aloud with silent timed tasks for time measurement.

### Cited Findings
- **Ko, LaToza, Burnett, "A practical guide to controlled experiments of software engineering tools with human participants", EMSE 20 (2015), DOI 10.1007/s10664-013-9279-3 (A; FT yes, author's copy).** Time on task requires defining "(1) when a task starts and ends and (2) who will determine when the participant has finished". Reading time for instructions adds variability. Unlimited pre-reading lets participants "start planning a solution, artificially decreasing the amount of time on task". The end of a task depends on whether the developer knows they succeeded. "Time on task and success on task trade off with each other … it is helpful to measure both". Time limits can cause ceiling effects. Think-aloud is mentioned only for piloting surveys — [author PDF](https://faculty.washington.edu/ajko/papers/Ko2013SEToolEvaluations.pdf)
- **Kapoor et al. (A-pre; FT §§2–3)**: dollar costs rather than proxies; "Fixed costs are one-time expenses incurred when optimizing the agent's hyperparameters (temperate, prompt, etc.) … Variable costs are incurred each time the agent is run and depend on the number of input and output tokens"; accuracy and cost reported as a Pareto frontier over 5 runs — [arXiv 2407.01502](https://arxiv.org/abs/2407.01502)
- **Baltes et al. §5.8 (A; FT yes)**: "Cost accounting tracks resource consumption by reporting tokens, service costs, or hardware specifications"; "Repeating experiments increases reliability but also energy consumption, requiring trade-offs" — [arXiv 2508.15503](https://arxiv.org/abs/2508.15503)

### Inferences
- **M2-R15 (human minutes).**
  - Log human minutes per gate and per arm with a **task-event log**: start and stop timestamps written by the harness when an item enters and leaves a human's queue, plus a one-line category (triage equivalent mutant / adjudicate expectation-test failure / label allowed variant / fix harness).
  - Define the start as "item displayed" and the end as "verdict recorded". Exclude reading the protocol, which is timed once and separately (Ko's start/end rule).
  - Record verdict quality alongside, via agreement with the second rater on the double-labelled subset (Ko's trade-off).
  - Do not use think-aloud during timed adjudication. *Inference*: think-aloud adds verbalisation time, and no source here quantifies the effect. Use think-aloud only in a separate, untimed pilot of the labelling guide.
  - *Can show*: the order of magnitude of triage cost per item type for one maintainer. *Cannot show*: generalisable human-time costs. The sample is one person, with learning effects across arms. Randomise item order across arms to spread learning (*Inference*).
- **M2-R16 (compute cost).** Per session, record input, output and cached tokens, the provider's list price on the date of the run, wall-clock time and the number of tool calls. Report dollars per arm as mean and range over the k runs. Report fixed costs (prompt iteration, harness debugging) separately. Report "cost per caught misreading" only next to the catch count, never alone. Sources: Kapoor (A-pre); Baltes §5.8 (A). *Cannot show*: future cost. Prices change, so report tokens as the stable quantity.

### Gaps
- No SE study was found that compares think-aloud with silent timing on the same tasks. The claim that think-aloud inflates time is *Inference*.
- No source gives human-triage time norms for LLM-generated test failures. The deep dive's IronSpec and MutDafny triage figures belong to the mutation strand.

---

## Q5. Model drift and tool-bug threats

### Takeaway
The "same" hosted model can change within months. In Chen et al.'s data a mere output-format change (Markdown fences) moved GPT-4's "directly executable" code from > 50 % to 10 %. That is simultaneously a drift effect and a **harness** effect: post-processing restored correctness to 70 %. Pin dated snapshots, record the returned model ID per call, keep a re-run subset as a drift probe, and validate the harness on known-good and known-bad artefacts before any arm runs.

### Cited Findings
- **Chen, Zaharia, Zou, "How Is ChatGPT's Behavior Changing over Time?", Harvard Data Science Review 2024, DOI 10.1162/99608f92.5317da47 (A; FT yes, arXiv v3).** They compared the March 2023 and June 2023 API snapshots at temperature 0.1. GPT-4 prime identification fell from 84 % to 51 %. Code: on 50 recent LeetCode easy problems, chosen to avoid contamination, "over 50% generations of GPT-4 were directly executable in March, but only 10% in June". One cause: the June version added "```python" fences. "After additional post-processing that removes the non-code text … GPT-4's performance increased from 52% to 70%". "This type of shift in formatting behavior can be particularly challenging to detect when LLM's generated code is used inside a larger software pipeline." They call for "continuous monitoring" — [arXiv 2307.09009](https://arxiv.org/abs/2307.09009)
- **Sallou et al. (A-workshop; FT yes)**: "Model Evolution Unpredictability … distinguishing whether the improvements claimed … are the result of changes to the LLMs' models or due to the novelty of the contribution becomes a complex task". Providers should use versioning that distinguishes major from minor revisions. They also cite OpenAI's seed feature, "although deterministic answer is not fully guaranteed" — [arXiv 2312.08055](https://arxiv.org/abs/2312.08055)
- **Baltes et al. §5.2 (A; FT yes)**: version, configuration and date are a "must". Temperature 0 is no guarantee. Archive raw outputs — [arXiv 2508.15503](https://arxiv.org/abs/2508.15503)
- **Earlier report, quoted verbatim (verified edition):** the gate is "recalibrated when the generating models change". Consistent with the drift evidence. No challenge.

### Inferences
- **M2-R17 (drift and harness controls).**
  - (a) Use dated snapshot IDs only, and log the model string returned on every response. Abort and restart a configuration if the string changes mid-trial.
  - (b) **Interleave arms in time**: randomise the run order of (arm × model × run) blocks across the calendar window, so that a provider change cannot coincide with one arm.
  - (c) **Drift probe**: a fixed set of ~5 misreadings is re-run for every model at the start and the end of the window. Report any change in catch pattern, using exact McNemar on the probe as a descriptive flag, not a test.
  - (d) **Harness sanity runs** before any arm and after any harness change:
    - the known-good R plus a correct test suite must pass;
    - each family's suite must fail on ≥ 2 hand-made known-bad R variants (one per misreading class);
    - the identical artefact run twice must give identical verdicts (tests non-flaky);
    - post-processing (code extraction from replies) is checked differentially: raw-reply extraction versus a second, independently written extractor on 10 replies.
  - (e) Treat every "test does not compile or collect" as a harness category, not as a miss, and report it separately (the Chen formatting case).

  Sources: Chen (A, FT), Sallou (A-workshop) and Baltes (A). The specific sanity set is *Inference*, mirroring the deep dive's wheat/chaff screening at the harness level. *Can show*: gross drift or harness breakage. *Cannot show*: subtle drift in which misreadings are caught at n = 5 probe items.

### Gaps
- No source quantifies drift of pinned (dated) snapshots, as opposed to floating aliases. Chen compared two different dated snapshots, which shows that version changes matter, not that a pinned snapshot drifts.
- No source on differential testing of LLM-evaluation harnesses specifically was found. The harness sanity protocol is *Inference*.

---

## Q6. Blinding ground-truth raters to arm

### Takeaway
SE blinding practice is rare. It consists of blind data extraction (the extractor is unaware of hypotheses and treatment) and blind analysis (groups relabelled A/B, variables renamed DV1, and so on, then unblinded after analysis). Interviewed SE experts note that blinding needs at least two people and is weak when both belong to the same group, which is the single-maintainer situation.

### Cited Findings
- **Romano, Fucci, Scanniello, Baldassarre, "Researcher Bias in Software Engineering Experiments: a Qualitative Investigation", Euromicro SEAA 2020 (A; FT §§II, results on blinding).** Blinding means "concealing research design elements (e.g., treatment assignment or research hypotheses) from individuals involved". "Few researchers have applied blinding in SE studies so far": Fucci et al. (blind extraction and analysis, a TDD replication) and Sigweni & Shepperd (blind analysis). In the Fucci procedure, the extractor "was not aware of the experimental goal, hypotheses, treatment assignment, and design". Analysts worked on "a sanitized dataset … the TDD and TLD groups became the A and B groups … PROD was renamed as DV1", and the "hidden information was revealed" after analysis. Drawback: blind extraction "requires at least two people" and "seems to be less feasible when both study executor and data extractor belong to the same research group"; a collaboration between two groups is preferable — [arXiv 2008.12528](https://arxiv.org/abs/2008.12528)
- **Sigweni & Shepperd, "Using blind analysis for software engineering experiments", EASE 2015 (A; [unreachable]: core.ac.uk returned HTML).** A search summary (lead only) says they found blinding "fairly simple" and argue it should become standard — [core.ac.uk record](https://core.ac.uk/download/30339829.pdf)
- **Shi et al. (A; FT §2)**: judge evaluation run "in a double-blind setting. The identities of the candidate models are hidden from the LLM judges" — [arXiv 2406.07791](https://arxiv.org/abs/2406.07791)
- **Zheng et al. (A; FT)**: showing humans the GPT-4 judgment changed their choice in 34 % of disagreements — [arXiv 2306.05685](https://arxiv.org/abs/2306.05685)

### Inferences
- **Blinding protocol (part of M2-R13/R14).**
  - (1) **Artefact anonymisation.** Strip model names, arm names, session IDs and lineage-specific stylistic markers (header comments, docstring templates, file names) from every artefact shown to raters. Normalise formatting with a code formatter. Expectation and spec tests differ in kind (record citation versus clause ID), so *Inference*: raters judging "is this failure a real misreading?" should see only the **behaviour in question** (input, observed output, record excerpt, spec excerpt), not the test code, wherever possible.
  - (2) **Randomised IDs.** Every item gets a random ID from a key file held by the harness, or by a second person if one exists. Present items in random order, mixed across arms.
  - (3) **Blind analysis.** Run the planned analysis script on data with arms relabelled A/B/C before unblinding, as in Romano's description of Fucci.
  - (4) **Hide judge verdicts** from human raters (Zheng's 34 %).
  - (5) **Blinding check.** After labelling, raters guess the arm for a random 20 items. Report the guess accuracy against chance (1/number of arms) with a Wilson interval. *Inference*: this is standard in clinical trials. No SE source read here prescribes it.

  *Can show*: whether blinding was broken in gross terms. *Cannot show* blinding in a single-maintainer setting where the maintainer also designed the arms. Romano's experts say blinding is "less feasible" within one group. That residual risk must be stated.

### Gaps
- Sigweni & Shepperd and Fucci et al. ESEM 2016 were not read in full ([unreachable] or not attempted). Their exact procedures are known only through Romano et al.'s description.
- No SE source on blinding raters to *LLM lineage* specifically. Stylistic fingerprints of model families could unblind raters, but no study of that was found (*Inference* only).

---

## What this strand cannot settle

- **Whether any lineage assignment gives independence on test or spec writing.** All correlated-error measurements read here (Kim, Goel) are MCQ, so transfer is *Inference*. At n ≈ 30 seeded misreadings the trial can detect only gross dependence: κ beyond ~±0.35–0.4 (own calculation). Kim's both-wrong agreement cannot be estimated meaningfully at this n.
- **A defensible fixed number of runs.** Sources use 3, 5 or 10. M2-R1's k = 5 is a cost-driven stability screen.
- **The arm comparison's power.** That belongs to the sample-size strand. As context only (own calculation, exact two-sided McNemar at α = 0.05 on per-misreading paired catch/miss):
  - With 25 % of misreadings caught only by the expectation family and 5 % only by the spec family, power is 0.29 at n = 24, 0.50 at n = 36, 0.67 at n = 48 and 0.88 at n = 72.
  - At 35 % versus 5 %, power is 0.57, 0.82, 0.93 and 0.99.
  - With zero discordant pairs in the other direction, at least 6 one-sided discordant misreadings are needed for p < 0.05 (6/6: p = 0.031; 5/5: p = 0.063).
- **Judge precision differences between judges**, or per misreading type. The CIs are too wide below ~30–60 labels per stratum.
- **Generalisable human-time costs** from one maintainer.
- **Leakage through paraphrase, training data or the operator.** Canaries and read-scope logs detect only verbatim or logged access.
- **Drift inside a pinned snapshot.** No source measured it.

## Self-check (possible misreadings of the briefs, reports or sources)

1. **Kim et al.'s chance baseline.** The verified edition writes "chance 1/3" for HELM, and the full text confirms it (3 wrong options). For HuggingFace the text gives 0.127 from a mixture formula. I represented both correctly as far as I can tell. My claim that the metric is unusable at small n is an own simulation under uniform wrong options and could understate usability if wrong options are highly non-uniform. Under non-uniform options, though, the chance baseline is itself unknown.
2. **Geirhos κ versus CAPA.** I recommend binary error consistency, not CAPA. Goel et al. argue CAPA is better because κ counts different wrong answers as agreement. In this trial the per-item outcome is binary (caught / missed), so that criticism matters less. It still applies when both arms "miss" for different reasons, so the κ may overstate similarity.
3. **Atil et al.** I read the arXiv v5. The Eval4NLP 2025 version has a different title, "…System Settings in Hosted Environments", and its figures may differ.
4. **CodeJudgeBench and Kapoor et al.** have no confirmed venue in my checks (A-pre). Kapoor may have since appeared in a journal, which I did not verify. The Semantic Scholar API rate-limited me.
5. **Grading choices.** ICSE-NIER is graded A-workshop and SEAA A. The earlier reports never graded either venue, so these choices may be inconsistent with their conventions.
6. **Baltes et al. is a living document** (arXiv v8, Sep 2026, "accepted manuscript"). The llm-guidelines.org web version may differ in wording. I quoted the arXiv PDF.
7. **Brown–Cai–DasGupta and Sigweni–Shepperd are [unreachable].** Nothing load-bearing rests on them. The CIs are own calculations, and the blinding procedure comes from Romano et al. (FT).
8. **Scope.** The brief asks for items 3, 4, 5, 7 and 8. I covered measurement protocol aspects of these (information flow verification, judge precision, human minutes, compute, ground-truth blinding, drift and tool threats, budget-relevant cost logging). I did **not** set stop rules or hour and token budgets (item 8 proper), the misreading taxonomy (item 2) or sample size (item 6). The McNemar figures are context for the sample-size strand, not a recommendation.
9. **"Spec-enforcing" versus "expectation" family.** I assumed, following the deep dive, that the expectation family sees records only and the spec-enforcing family sees the spec. If the trial-design brief intends different visibility, M2-R10/R11 need adjusting.
