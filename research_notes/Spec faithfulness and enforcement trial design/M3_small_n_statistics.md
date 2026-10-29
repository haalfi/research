# M3 Sample size, analysis plan, pre-registration and stop rules for a small single-operation trial

Scope: trial-design brief §3 items 6 ("Sample size and analysis") and 8 ("Budget and stop rules") and §5 item 3 ("Pre-registered hypotheses and refutation criteria"). Experimental method only. Notation used throughout:

- Unit = one seeded misreading (fault) i = 1..n, each scored for both families. **E** is the expectation family (oracles derived from the prose records). **S** is the spec-enforcing family (oracles derived from the spec).
- Paired 2×2 per fault: p11 means both catch, p10 means E catches and S misses, p01 means S catches and E misses, p00 means neither catches.
- **psi** = p10 + p01, the discordant proportion. **pi** = p10 / psi, the share of discordant faults that favour E. **delta** = p10 − p01 = psi·(2·pi − 1).
- The central claim in the brief, verbatim: "Oracles derived from the prose records catch spec misreadings that oracles derived from the spec miss." In this notation it is a claim about p10 (existence and size) and about delta (E better than S).

Source grades and full-text status (FT) are given at first use. "Own calc" means the calculation scripts in the scratchpad m3/calc (power.py, sim.py). Their outputs are in power_out.txt, sim_out.txt and cp_out.txt. They use scipy and statsmodels in a scratchpad venv, with seed 20261029 and 2,000–20,000 simulation replicates.

---

## Q1. Paired binary outcomes per seeded fault: McNemar variants, power and sample size, Bayesian alternatives, equivalence framing; repeated LLM runs

### Takeaway
Use a **paired** analysis on the discordant faults. Use the mid-p McNemar test (or the asymptotic test without continuity correction), not the exact conditional test, and report delta and p10 with CIs. Power depends almost entirely on how many faults turn out discordant and how one-sided they are. Own calcs give these minimum n for 80% power at two-sided α = .05:
- about 40 faults when psi = 0.2 and every discordant fault favours E;
- about 60 faults when psi = 0.2 and pi = 0.9;
- about 80 faults when psi = 0.3 and pi = 0.8;
- 115 to 260 faults when pi is 0.7 or psi is 0.1.

With repeated LLM runs per fault, the fault, not the run, is the unit. Pooling runs as if independent inflates the type-I error to 11–32% in own simulations.

### Cited Findings
- **Fagerland, Lydersen & Laake 2013**, "The McNemar test for binary matched-pairs data: mid-p and asymptotic are better than exact conditional", BMC Med Res Methodol 13:91 (A; FT yes; https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91):
  - Across 9,595 scenarios the mid-p McNemar test "did not violate the nominal level in any of the 9595 scenarios" and "was almost as powerful as the asymptotic test".
  - "The type I error rates of the McNemar exact conditional test are low and barely above 3%, even for as much as 100 matched pairs."
  - The authors "do not recommend use of the McNemar exact conditional test nor the asymptotic test with CC in any situation". They recommend the asymptotic test without continuity correction "if small but frequent violations of the nominal level is acceptable".
  - Their power scenarios covered N = 1..100 pairs.
- **Connor 1987**, "Sample Size for Testing Differences in Proportions for the Paired-Sample Design", Biometrics 43:207 (A; **[unreachable]** behind JSTOR; metadata via Crossref DOI 10.2307/2531961).
  - The formula used in own calc is the one commonly attributed to Connor: n = [z_{α/2}·√psi + z_β·√(psi − delta²)]² / delta². It is taken from memory, **not verified against the full text**.
  - Own calc cross-checked it against exact enumeration (below). Connor's n came out 3–10% below what the exact conditional test needs, and slightly above what mid-p needs.
- **Lachin 1992**, "Power and sample size evaluation for the McNemar test…", Stat Med 11:1239–1251 (A; **[unreachable]**; Crossref DOI 10.1002/sim.4780110909). The content was not read. It is cited only as the standard reference for conditional versus unconditional McNemar power.
- **Own calc, Table 1 (power.py)**. Exact unconditional power: the number of discordant faults d ~ Bin(n, psi), and b | d ~ Bin(d, pi). Each cell gives power for the exact conditional test / the mid-p test, at two-sided α = .05.

| psi | pi | delta | n=20 | n=40 | n=60 | n=80 | n=100 | n=120 |
|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.9 | 0.08 | .01/.02 | .11/.22 | .31/.46 | .52/.64 | .67/.77 | .78/.85 |
| 0.1 | 1.0 | 0.10 | .01/.04 | .21/.37 | .56/.73 | .82/.91 | .94/.98 | .98/.99 |
| 0.2 | 0.7 | 0.08 | .02/.05 | .11/.17 | .19/.26 | .28/.35 | .35/.42 | .42/.49 |
| 0.2 | 0.8 | 0.12 | .05/.11 | .26/.37 | .46/.55 | .62/.70 | .74/.79 | .82/.86 |
| 0.2 | 0.9 | 0.16 | .10/.21 | .52/.65 | .78/.85 | .91/.94 | .97/.98 | .99/.99 |
| 0.2 | 1.0 | 0.20 | .20/.37 | .84/.92 | .99/1.0 | 1/1 | 1/1 | 1/1 |
| 0.3 | 0.7 | 0.12 | .06/.12 | .19/.26 | .32/.39 | .42/.49 | .52/.59 | .62/.68 |
| 0.3 | 0.8 | 0.18 | .15/.25 | .46/.55 | .68/.75 | .82/.86 | .90/.93 | .95/.97 |
| 0.3 | 0.9 | 0.24 | .32/.47 | .79/.86 | .95/.97 | .99/.99 | 1/1 | 1/1 |
| 0.4 | 0.7 | 0.16 | .11/.17 | .28/.35 | .42/.49 | .56/.62 | .68/.73 | .77/.81 |
| 0.4 | 0.8 | 0.24 | .26/.37 | .62/.70 | .82/.86 | .92/.95 | .97/.98 | .99/.99 |

(The full grid, including psi = 0.1 with pi = 0.7 or 0.8 and n = 30, is in power_out.txt.)

- **Own calc, Table 2.** Minimum n for power ≥ 0.8 (two-sided α = .05), given as Connor approximation / exact conditional / mid-p:
  - psi 0.1: pi 0.8 → 216 / 232 / 204; pi 0.9 → 121 / 126 / 108; pi 1.0 → 77 / 78 / 66; pi 0.7 → over 400.
  - psi 0.2: pi 0.7 → 243 / 258 / 238; pi 0.8 → 107 / 116 / 102; pi 0.9 → 59 / 62 / 54; pi 1.0 → 37 / 40 / 34.
  - psi 0.3: pi 0.7 → 162 / 172 / 158; pi 0.8 → 71 / 78 / 68; pi 0.9 → 39 / 42 / 36; pi 1.0 → 24 / 26 / 22.
  - psi 0.4: pi 0.7 → 121 / 130 / 118; pi 0.8 → 53 / 58 / 52; pi 0.9 → 29 / 32 / 26; pi 1.0 → 18 / 20 / 16.
- **Own calc, Table 4.** If every discordant fault favours E, the two-sided exact conditional test first reaches p ≤ .05 at d = 6 discordant faults (p = .031). The mid-p test first reaches it at d = 5 (p = .031). Below about 5–6 discordant faults, no result can be "significant" whatever n is.
- **Own calc, Bayesian (sim.py B1).** Prior Beta(1,1) on pi. The decision rule is P(pi > 0.5 | data) > 0.975. The probability of meeting the rule at the true values (assurance) is:
  - psi 0.2, pi 0.9: n = 40 → .65; n = 60 → .84; n = 80 → .94.
  - psi 0.3, pi 0.8: n = 40 → .55; n = 60 → .75; n = 80 → .87.
  - Under the null (pi = 0.5) the rule fires in 1–3% of trials.

  With a flat prior this behaves almost like the mid-p test. The Bayesian version buys a direct probability statement, not power.
- **Own calc, Bayes factors (sim.py B2).** H1 is pi ~ U(0,1); H0 is pi = 0.5.
  - If all d discordant faults favour E: BF10 = 3.2 at d = 4, 9.1 at d = 6, 28 at d = 8, 93 at d = 10.
  - At a 75:25 split, BF10 stays under 3 until d is about 20 (BF10 = 3.2 at d = 20; 5.9 at d = 30).
  - At a 50:50 split, the evidence for H0 grows slowly: BF01 = 2.7 at d = 10 and 4.5 at d = 30.

  A small trial can therefore give strong Bayes-factor evidence only for a lopsided effect. It can hardly ever give strong evidence of *no* difference.
- **Furia, Feldt & Torkar**, "Bayesian Data Analysis in Empirical Software Engineering Research", IEEE TSE (A; FT yes, arXiv 1811.05422 version; Crossref DOI 10.1109/TSE.2019.2935974):
  - The paper argues that the p-value is "a statistics of the data alone" and that p-value practice has problems with multiple testing (its §4.2.2).
  - It recommends a prior **sensitivity analysis**, whose goal "is not choosing a prior" but showing how conclusions depend on it (§4.3.3).
- **Miller 2024**, "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations", arXiv 2411.00640 (A-pre; Anthropic author; FT yes; https://arxiv.org/abs/2411.00640):
  - It recommends "computing clustered standard errors" when questions come in groups, and "resampling answers" to reduce variance.
  - It recommends analysing "question-level paired differences" because Var_paired = Var_unpaired − 2·Cov/n. Paired differences are "a 'free' reduction in estimator variance".
  - On resampling: "computing a pooled standard error across all KN answers will be inconsistent, as multiple answers to the same question would violate the assumption of independent draws."
  - Variance with K samples per question, uniform-difficulty example: Var(K) = Var(1)·(1 + 2/K)/3. K = 2 cuts variance by 1/3, K = 4 by 1/2, and K = 6 by 5/9. The upper limit on the reduction is 2/3.
  - It gives a minimum-detectable-effect formula that includes ω² + σ²_A/K_A + σ²_B/K_B.
  - In its real-world example, clustered standard errors were up to about 3× the naive ones.
- **Own calc, clustered repeated runs (sim.py C).** Set-up:
  - n faults, k = 5 runs per family per fault.
  - The fault-level catch probability is Beta with mean m and intra-fault correlation rho. The Kish design effect 1 + (k − 1)·rho is printed for orientation; it is a textbook formula, not sourced here.
  - E and S are independent given the fault.

  Results:
  - **Type I** (mE = mS = .5):
    - naive pooled McNemar over n·k run pairs: .11–.14 at rho = .2, .23–.25 at rho = .5, .31–.32 at rho = .8;
    - k = 1 McNemar, per-fault majority-of-k McNemar and the sign test on per-fault rate differences: .02–.04, conservative;
    - paired t-test on fault-level catch rates: .045–.054.
  - **Power** (mE = .6, mS = .4, n = 40):
    - rho = .2: k = 1 McNemar .35, majority .63, sign test .68, paired t .83;
    - rho = .8: .34, .35, .37 and .50.
    - With rho = .2 and n = 80, majority-of-5 reaches .92 against .67 for one run.

  Repeated runs help most when runs disagree a lot within a fault (low rho). They help little when an LLM is near-deterministic per fault (high rho).

### Inferences
- *Inference.* **Primary estimand and test.**
  - Primary estimand: delta = p10 − p01 over seeded misreadings, with a 95% CI. A Newcombe-type or Wald interval for paired differences is suitable; the method was not sourced here.
  - Co-primary estimand: p10 with a Clopper–Pearson CI.
  - Primary test: two-sided mid-p McNemar (Fagerland).
  - Can show: whether E catches more seeded misreadings than S *on this operation and this seed set*.
  - Cannot show: anything about real misreadings, other operations, or why E wins.
- *Inference.* **Structural asymmetry.** S is derived from the spec, and a seeded misreading lives in the spec. A faithful S therefore encodes the misreading and can catch it only through internal inconsistency, such as a cross-table contradiction found by G3/G4. Expect p01 ≈ 0 for most misreading types, so pi ≈ 1.
  - Then psi ≈ p10, and the McNemar test reduces to "is p10 > 0". At n = 40–60 that test is easy to pass (Table 1, pi = 1.0 rows).
  - The informative quantity is the **size of p10**, together with the share of misreadings that **neither** family catches (p00). Plan the sample size for the *precision of p10 and p00*, not only for the McNemar power.
- *Inference.* **What n buys in precision** (own calc E, F and G; Wald or Clopper–Pearson):
  - At n = 60, the 95% CI half-width on delta is about ±0.11 (psi .2, pi .8) to ±0.13 (psi .3, pi .8). At n = 120 it is about ±0.08–0.09.
  - If 0 of n faults show an E-only catch, the 95% upper bound on p10 is 0.139 at n = 20, 0.072 at n = 40, 0.049 at n = 60, and 0.025 at n = 120 (rule of three).
  - So n = 60 is the smallest n at which a null result can bound p10 below 5%.
- *Inference.* **Recommended n.** At least **60 seeded misreadings, about 10 per misreading type for the 6 types in brief §3.2**, with 80–120 preferred.
  - At 10 per type, per-type estimates are almost uninformative. For example, 5/10 gives a Clopper–Pearson CI of [0.19, 0.81], 10/10 gives [0.69, 1], and 0/10 gives [0, 0.31] (own calc, cp_out.txt). Per-type results must therefore be **descriptive only**.
- *Inference.* **Repeated runs.**
  - Use k = 3–5 independent runs per family per fault, with a fixed temperature recorded.
  - Primary analysis: fault-level catch rates (catches/k), compared with a paired test at fault level. Use the paired t or Wilcoxon on fault-level differences, or a cluster bootstrap over faults.
  - Secondary analysis: per-fault majority-of-k fed into McNemar.
  - Never pool runs as independent pairs (own calc C; Miller 2024).
  - GEE or mixed-effects logistic regression with fault as cluster is an alternative. *Not computed here*: at n < 50 clusters, GEE sandwich standard errors are known to be anti-conservative. That point comes from training knowledge, so it is [unsourced] and should be verified or dropped.
  - k = 1 is enough only if a pilot shows rho > 0.8 (near-deterministic outputs).
- *Inference.* **Non-inferiority / equivalence framing.**
  - "Both families" against "S only" is a **union**: both ⊇ S by construction, so p01 = 0 and McNemar is degenerate. Report only p10(both vs S) with a one-sided Clopper–Pearson lower bound. With 8 extra catches out of 80 faults, the 95% CI is [0.044, 0.188] (own calc F).
  - If the claim to defend is "E is not worse than S", pre-specify a non-inferiority margin, e.g. delta > −0.05. A margin that small needs n in the hundreds; the Table 2 trend extrapolates to at least 200 when psi ≥ 0.2.
  - For a one-operation trial, equivalence claims are out of reach (Bayes-factor result above).
- *Inference.* **Covariate for test count.** The verified edition records that kills must be compared **at equal test counts**. Verbatim: "Kills compared **at equal test counts**. Kills guide gap-finding but do not measure real-fault detection (Papadakis: r ≈ 0.05–0.20 with size controlled)" (verified report, S7 row).
  - Either equalise suite sizes by subsampling before scoring, or report delta at matched sizes. Subsampling adds variance, so repeat the subsampling and average per fault.
  - This is a design choice that follows from the earlier report, not a new statistical source.

### Gaps
- Connor 1987, Lachin 1992 and Arcuri & Briand 2011/2014 are **[unreachable]**. The orbilu.uni.lu open-access copy failed TLS (incomplete chain) and then gave HTTP 503 via WebFetch, and ACM returned 403. Their exact recommendations are not reported here. The Connor formula used is from memory and cross-checked only by enumeration.
- No source was found on the intra-fault correlation (rho) of LLM test generators' catch/miss outcomes. A pilot must estimate it.
- The GEE small-sample bias claim is unsourced.

---

## Q2. Multiple comparisons across arms and gates; estimation-first reporting; avoiding p-hacking

### Takeaway
Declare **one** primary confirmatory comparison: E against S on delta. Order a short fixed sequence of secondary confirmatory comparisons, and label every gate or pipeline comparison exploratory and descriptive, reported with CIs. If several comparisons must be confirmatory, Holm at three comparisons raises the needed n by roughly 30–40% (own calc).

### Cited Findings
- **ACM SIGSOFT Empirical Standards, Experiments** (B: community standard, not peer-reviewed as a paper; FT yes; https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/standards/Experiments.md):
  - Essential items include "states formal hypotheses", "uses two-sided hypotheses OR justifies use of one-sided hypotheses", "justifies sample size (e.g. using power analysis)", "reports effects sizes with confidence intervals (if using frequentist approach)" and "reports distribution-appropriate descriptive and inferential statistics; justifies tests used".
  - Listed antipattern: "data analysis technique used does not correspond to the design chosen or data characteristics (e.g. using an independent samples t-test on paired data)".
  - Desirable items: "justifies hypotheses and Bayesian priors (if applicable)", "pre-registration of hypotheses and design", "clearly distinguishes evidence-based results from interpretations and speculation".
  - Scope note: the standard applies to experiments "with human participants". For experiments without human participants it points to "Exploratory Data Science" or "Engineering Research". An all-LLM trial is formally outside its scope and uses it by analogy.
- **Kitchenham et al. 2017**, "Robust Statistical Methods for Empirical Software Engineering", EMSE 22:579–630 (A; FT yes; https://link.springer.com/article/10.1007/s10664-016-9437-5):
  - It recommends robust methods (trimmed means; Cliff's δ "or a robust rank-based ANOVA-like method" for non-normal or ordinal data) and kernel density plots instead of box plots.
  - It agrees "with Arcuri and Briand (2014) that effect sizes are extremely useful".
  - It illustrates CIs adjusted for multiple tests.
- **de Oliveira Neto et al. 2019**, "Evolution of statistical analysis in empirical software engineering research", JSS 156:246–267 (A; FT yes, arXiv 1706.00933 version; Crossref DOI 10.1016/j.jss.2019.07.002):
  - Reviewed 161 papers manually and 5,196 semi-automatically (2001–2015). The authors "confirm existing claims that current ESE practices lack a standard to report practical significance of results".
  - Power analysis was rare: "only seven counts", and where found it "invariably was of a post hoc nature".
- **Furia, Feldt & Torkar** (A; FT yes) see p-value practice as vulnerable under multiple testing (§4.2.2) and favour reporting posterior distributions of effect sizes.
- **Own calc, Table 3.** With Holm across 3 confirmatory comparisons, the smallest p must clear .05/3. Minimum n for 80% power on that comparison (exact conditional test):
  - psi .2: pi .8 → 148 (vs 116 unadjusted); pi .9 → 80 (vs 62).
  - psi .3: pi .8 → 100 (vs 78); pi .9 → 54 (vs 42).
- **Holm 1979** (Scand J Statist) and gatekeeping / fixed-sequence procedures: **not fetched** ([unreachable] in this run). The fixed-sequence logic is described below as *Inference* from standard knowledge.

### Inferences
- *Inference.* **Planned comparison hierarchy (fixed sequence, each at α = .05, stop at the first non-rejection):**
  - **H1**: delta(E vs S) > 0 over all seeded misreadings.
  - **H2**: p10(both vs S) ≥ a pre-set margin, e.g. 0.10, via the one-sided CP lower bound.
  - **H3**: E's false-alarm or over-strict rate on allowed variants is ≤ a pre-set ceiling, via a CP upper bound.

  A fixed sequence keeps family-wise α at .05 without splitting α. The price: if H1 fails, nothing after it is confirmatory.
- *Inference.* **Exploratory only:**
  - pipeline A vs B vs C;
  - first gate to fail (G0–G9);
  - per-misreading-type rates;
  - judge precision;
  - human minutes;
  - compute cost.

  Report counts, proportions with CP CIs, and medians with ranges. Make no confirmatory claims; ten gates by three pipelines by six types is 180 cells for about 60–120 faults.
- *Inference.* **Measures at small n, what each can and cannot show:**
  - *Kills per family*: can show a large asymmetry. Cannot show real-fault detection, since mutant-kill correlation with real faults is weak once size is controlled (Papadakis, via the verified report).
  - *First gate to fail*: can show an ordering of gate yield on this seed set. Cannot rank close gates (CIs overlap at n per gate under 20).
  - *False alarms / over-strict tests*: with 40–60 allowed-variant probes, a 95% CP upper bound can show "under about 7–10%" when 0–1 failures are seen (rule of three gives 3/n). It cannot separate 2% from 5%.
  - *Judge precision against human labels*: 36/40 correct gives CP [0.76, 0.97], and 54/60 gives [0.80, 0.96] (own calc). This is enough to detect a bad judge (under 0.75), not to certify a good one at 0.95.
  - *Human minutes and compute cost*: n = 1 operation, so these are descriptive; no variance estimate across operations exists.
- *Inference.* **Anti-p-hacking rules to pre-register:**
  - analysis code frozen and hashed before unblinding;
  - outcome labels (caught / not caught; misreading / allowed variant) assigned blind to arm;
  - no change of fault set, k or primary test after seeing arm-level outcomes;
  - every unregistered analysis labelled exploratory (Registered Reports standard, Q3).

### Gaps
- No SE-specific source on gatekeeping procedures was read. Holm and gatekeeping were not fetched.
- No source was found that gives standard effect-size magnitudes for "catch rate differences" between oracle families.

---

## Q3. Pre-registration in SE: what it must contain; how to phrase refutation criteria

### Takeaway
SE registered reports run in two stages. The Stage 1 protocol (RR1) holds the hypotheses, operationalised variables, method and analysis pipeline, and it must be detailed enough for an independent researcher to replicate it exactly. Deviations must be justified and must "not [be] justified based on the data". Refutation criteria should be stated as numeric thresholds on pre-specified estimands, including a "practically refuted" bound for a null result.

### Cited Findings
- **ACM SIGSOFT Empirical Standards, Registered Reports** (B; FT yes; https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/RegisteredReports.md):
  - Definition: "Pre-registration refers to depositing the RR1 somewhere publicly visible. Pre-registration aims to prevent hypothesising after results are known, to mitigate unconscious researcher bias in data analysis, and combat publication bias."
  - Applies to "positivist, confirmatory (i.e. hypothesis-testing) studies with tightly-scoped analysis approaches".
  - RR1 essentials: "describes the research method in detail sufficient for an independent researcher to exactly replicate the proposed data collection and analysis procedures"; "the stated hypotheses can be tested with the data the researchers propose to collect". Its footnote example: "presents power analysis; … lists anticipated statistical tests".
  - RR1 desirable: "presents preliminary data (e.g. from a pilot study)"; "includes a conditional structure (e.g. pre-specifying different tests for normal and non-normal distributions)"; "explains how the study will change based on the results of data analysis (i.e. conditional analysis)". The footnote adds that omitting conditional analysis is "extraordinarily risky".
  - RR2 essentials: "adheres precisely to the registered procedures OR: thoroughly justifies all deviations"; "deviations, if any, are _not_ justified based on the data"; "clearly designates as exploratory any unregistered post hoc analyses".
  - Antipatterns: "postdictive deviations from RR1 plan"; "Pre-registrations that are not verifiably committed prior to data collection, e.g. not time-stamped."
  - Invalid RR2 criticism: "results are not statistically significant, novel, relevant or compelling; effect sizes too small".
- **Ernst & Baldassarre 2023**, "Registered reports in software engineering", EMSE 28:55 (A, editorial; FT yes; https://doi.org/10.1007/s10664-022-10277-5):
  - "A pre-registered study is a research protocol, including planned hypotheses, data collection, and data analysis, that is announced—registered—before the study in full is conducted." "Registration is as simple as a blog post, or depositing an official document on a registry server, such as the ones supported by the Open Science Foundation."
  - Stage 1 "includes an introduction to the research topic and rationalization of the research questions/hypotheses, operationalization of variables, methodology and analysis pipelines … Where applicable, pilot data can also be submitted". It is typically 5–6 pages.
  - RR tracks exist at MSR, ICSME and ESEM, with EMSE as the partner journal.
  - The authors cite the ideal of a "severely testable" hypothesis, one where "with high probability, H would not have passed the test so well, were H false" (Mayo & Spanos).
  - In confirmatory studies, "looking at the data and reconstructing an explanation post-hoc is statistically invalid". They name forking paths (Gelman & Loken).
  - On exploratory work: "Changing observations as results emerge is a key part of the inductive nature of the process. Registration still seems to work here."
- **Crossref lead (not read)**: "Towards an OSF-based Registered Report Template for Software Engineering Controlled Experiments", WSESE 2026 workshop, DOI 10.1145/3786149.3788308 (A-workshop; **FT no**). It is a possible template source; its content is unverified.
- The brief also asked for **Neto et al.** If this means de Oliveira Neto et al. 2019 (Q2), that paper covers statistical-practice evolution, not pre-registration. *No separate Neto et al. paper on pre-registration was identified* (see Self-check).

### Inferences
- *Inference.* **Minimum pre-registration contents for this trial**, mapped to RR1 items:
  1. The central claim and estimands (p10, p01, delta, p00) with exact operational definitions of "caught", namely which gate or test fails, at which run.
  2. The fault population: taxonomy, number per type, seeding lineage, realism checks, and the held-out set of real misreadings scored separately.
  3. Arms and information flow.
  4. k runs, models, temperatures and versions.
  5. The blinding procedure for ground-truth labelling.
  6. Primary test (mid-p McNemar on fault-level majority or on k = 1), primary CI method, and the fixed-sequence H1→H3 with α.
  7. Conditional analysis tree: if rho is estimated above 0.8 in the pilot, use k = 1; if fewer than 6 discordant faults are seen, report estimation only.
  8. Stop rules (Q4).
  9. Refutation criteria (below).
  10. A list of exploratory analyses.
  11. Timestamped deposit: a commit hash on the research branch, or OSF.
- *Inference.* **Refutation criteria, phrased against pre-set numbers.** Proposed defaults; the trial designer sets the actual margins.
  - **R1, refuted (strong):** "The central claim is refuted for this operation if the two-sided 95% CI upper bound for delta is below +0.05 **and** the 95% CP upper bound for p10 is below 0.10." At n = 60, zero E-only catches gives an upper bound of 0.049, so R1 is attainable.
  - **R2, not supported (weak):** "The claim is not supported if H1 is not rejected and R1 is not met." This is inconclusive; report it as such, not as refutation.
  - **R3, supported:** "H1 rejected **and** the lower 95% bound for p10 ≥ 0.05."
  - **R4, external-validity guard:** "If the held-out real misreadings (if any) show E-only catches at a rate whose CP CI excludes the seeded-set estimate, the seeded result is not generalised even to this operation."
- *Inference.* Severity in Mayo's sense, quoted by Ernst & Baldassarre, needs a design in which E *could* fail. Include misreading types where E is expected to be weak, such as cross-table contradictions (G3/G4 territory, where S may win). The pre-registration should predict a **per-type direction** as an exploratory, falsifiable sign prediction.

### Gaps
- The exact OSF pre-registration template fields were not read (cos.io not fetched).
- No SE paper was found that pre-registers an LLM test-generation comparison.

---

## Q4. Stop rules: group-sequential and Bayesian stopping; budget and infrastructure stops

### Takeaway
A single pre-planned interim look at n/2 is affordable:
- An O'Brien–Fleming-type boundary keeps α at about .05 and costs almost no power. It stops early for efficacy in 10–38% of trials where a real effect exists.
- A Pocock boundary stops earlier (33–69%) but loses some power.
- A Bayesian futility rule, P(pi > .5) < .2 at n/2, stops about 19% of null trials and almost no real-effect trials.

Infrastructure sanity gates should stop the run **before** any outcome is unblinded and should not count as looks.

### Cited Findings
- **Lakens 2014**, "Performing High-Powered Studies Efficiently with Sequential Analyses", Eur J Soc Psychol (A; FT yes, in-press author version, OSF 10.31234/osf.io/9yegd; Semantic Scholar shows the DOI 10.1002/ejsp.2023):
  - Sequential designs "can easily reduce the sample size of studies by 30% or more".
  - Pocock: "for two planned analyses (one interim and one after all data is collected), the p-value would become .0294 for each analysis".
  - O'Brien–Fleming "sets a high critical value for the first interim analysis … but sets a critical value for the final analysis that is closer to a study without interim looks".
  - Lan–DeMets alpha-spending functions "do not require the number of interim analyses to be specified in advance (as long as the Z-value at one interim analysis does not determine the time until the following analysis)". He also names a linear spending function between Pocock and O'Brien–Fleming.
  - Risks: early stops may land on a "random high". The effect size estimate "needs to be corrected for bias when stopping early". Researchers "can decide to terminate the data collection early for futility" when conditional or predictive power is very low.
  - Repeated looks without correction inflate the Type 1 error (citing Simmons et al. 2011).
- **Own calc (sim.py D).** Two looks at n/2 and n, sign-test z on discordant faults, 20,000 replicates. The constants are standard two-look values: Pocock 2.178 for both looks, matching Lakens' .0294; O'Brien–Fleming 2.797 then 1.977.
  - **Null** (psi .3, pi .5): P(reject) is fixed .052–.054, Pocock .045–.052, O'Brien–Fleming .047–.048.
  - **psi .3, pi .8, n = 100**: P(reject) fixed .94, Pocock .91, O'Brien–Fleming .93. P(stop at n/2) Pocock .58, O'Brien–Fleming .30. E[n] fixed 100, Pocock 71, O'Brien–Fleming 85.
  - **psi .2, pi .9, n = 60**: P(reject) fixed .86, Pocock .80, O'Brien–Fleming .86. E[n] 60, 47 and 57.
  - **Adding the Bayesian futility rule** (Beta(1,1), stop if P(pi > .5) < .2 at n/2):
    - null trials: the futility stop fires in .18–.20, P(reject) falls to .026–.039, and E[n] falls to 54 (n = 60) or 90 (n = 100);
    - real-effect trials: the futility stop fires in ≤ .004 and power is essentially unchanged.
- **Empirical Standards, Benchmarking** (B; FT yes): it requires that the study "assesses stability or reliability using sufficient experiment repetitions" and "transparently reports on problems with executing benchmark runs".
- **Empirical Standards, Quantitative Simulation** (B; FT yes): it requires "number of runs per scenario (in case of using stochastic simulation)" and lists "using a single run instead of multiple runs to experiment with stochastic models" as an antipattern.
- **Empirical Standards, Registered Reports** (B; FT yes): deviations are acceptable when "not postdictive". Its example is dropping a mistranslated item, which is the template for an infrastructure stop.

### Inferences
- *Inference.* **Recommended stop rules:**
  1. **Pre-flight sanity gates (no outcome data seen).** Abort and fix, without counting a look, if any of these fails:
     - harness smoke tests;
     - every seeded fault actually changes the spec artefact (diff non-empty and parseable);
     - the unmutated spec/R passes both families (no false alarm at baseline);
     - the independence checks hold, i.e. the G0 import ban and read-scope logs;
     - model and version pins resolve.

     Log every abort as a deviation (RR standard).
  2. **Interim look at n/2**, by an analyst who receives only the discordant counts. Stop for efficacy if |z| ≥ 2.797 (O'Brien–Fleming); stop for futility if P(pi > .5 | data) < .2. Otherwise continue to n.
  3. **Budget stop.** Hard ceilings on tokens, wall-clock and human minutes, set in the protocol. If a ceiling is reached before n, analyse at the achieved n with the pre-registered method, report it as a "budget-truncated" trial, and label power as reduced.
  4. **Drift stop.** If a pinned model version becomes unavailable mid-trial, stop and treat the completed faults as the trial. Mixing versions breaks the pairing assumption.
- *Inference.* **What sequential stopping can and cannot show here.**
  - It saves 15–30% of faults on average when the effect is real (own calc).
  - It biases the effect estimate upward if a trial stops early (Lakens).
  - The faults must be seeded **before** the trial in a random order, so that stopping at n/2 leaves a random half. If seeding is done in batches by type, the interim half is unbalanced by type. Randomise the order.
- *Inference.* With one operation, the n/2 interim may hold only about 6–10 discordant faults. Below 5–6, no boundary can be crossed (Q1, Table 4), so for psi ≤ 0.2 and n ≤ 60 an interim look is nearly useless. Use only the futility rule there.

### Gaps
- The original Pocock 1977, O'Brien & Fleming 1979, Lan & DeMets 1983 and Jennison & Turnbull texts were not read. The boundary constants come from standard tables, with the Pocock value cross-checked against Lakens' .0294.
- No source on Bayesian stopping specific to SE or LLM evaluation was read.

---

## Q5. Single-case / small-N design and generalisation limits; replication plans

### Takeaway
One operation and one maintainer make this a single-object, quasi-experimental trial. Its statistics generalise only to the *population of seeded misreadings drawn by this seeding protocol on this operation*, and the claims allowed beyond that are analytic, not statistical. Replication should go to a second operation first and a second seeding lineage second, with the protocol frozen.

### Cited Findings
- **Empirical Standards, Sampling** (B; FT yes; https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/Sampling.md):
  - Essential: "explains the goal of sampling (e.g. aiming for representativeness, identifying exceptional cases)"; "explains the sampling strategy".
  - If representativeness is a goal: "states the theoretical population (what would the researcher like to generalize to?)" and "explains how the sample could be biased along the sampling steps".
  - Desirable: "study with identifiable strata: using stratified random rather than simple random sampling".
- **Empirical Standards, Experiments** (B; FT yes):
  - Essential: "justifies selection of experimental objects; acknowledges object-treatment confounds, if any".
  - Invalid criticism: "low external validity".
  - Extraordinary attribute: "reports multiple experiments or replications".
- **Empirical Standards, Engineering Research** (B; FT yes):
  - Antipatterns: "evaluation using a non-experimental (single group, non-repeated) design" and "evaluation using toy examples (sometimes misrepresented as 'case studies')".
  - Invalid criticism: "'Too few experimental subjects' … if few subjects are available in the contribution's domain or the experimental evaluation is part of a more comprehensive validation strategy".
- **Ernst & Baldassarre 2023** (A; FT yes) frame confirmatory replication as testing a finding "with new data (for example, in a startup company)".
- **Miller 2024** (A-pre; FT yes) assumes questions are drawn from a "super-population". It notes that clustered draws need clustered standard errors and suggests reporting "the cluster count alongside the question count".
- **Kim et al.** on correlated LLM errors comes from the earlier reports, via the brief's verbatim weakness: "Correlated LLM errors. They are stronger within one provider and among more accurate models, so separating lineages by swapping models may not give independence." That source was not re-read in this strand.

### Inferences
- *Inference.* **Allowed claims:**
  - "On operation X, with seeding protocol P and models M (versions pinned), E caught delta more seeded misreadings than S (95% CI …)."
  - **Not allowed:** claims about other operations, real misreadings (unless a held-out real set was scored), other maintainers, or other model generations.
  - Misreading type is a stratum. Faults within one operation are clustered by type and by spec region, so the effective n is likely below the nominal n. Report the cluster count, i.e. types × regions (Miller's advice, applied by analogy).
- *Inference.* **Single-maintainer confound.**
  - The maintainer writes the records, picks the operation, and may seed or label. Mitigations:
    - a second labeller on a random ≥ 20% of labels, reporting agreement with a CI;
    - seeding by an independent lineage plus a human subset scored separately (lineage as an exploratory factor);
    - the maintainer blind to the arm at labelling time.
  - It cannot be removed within one trial, so state it in "What this design cannot show".
- *Inference.* **Replication plan, frozen protocol:**
  1. A second operation from the same project, chosen by the same §3.1 criteria. This tests object generality.
  2. A second seeding lineage, a different provider or a human, on the same operation. This tests seed-source dependence, given the Kim et al. correlation concern.
  3. A second maintainer/project if available.

  Combine the replications by fixed-effect meta-analysis of delta only if the protocol is unchanged; otherwise report them side by side.
- *Inference.* At n = 1 operation, between-operation variance is **unestimated**. Any CI is conditional on the operation. This is the dominant limit and no n of faults fixes it.

### Gaps
- Wieringa & Daneva-type literature on analytic generalisation in SE was not read in this strand.
- No source quantifies how much seeded-misreading results transfer to real misreadings in spec work.

---

## Q6. Reporting standards: ACM SIGSOFT Empirical Standards; CONSORT-like checklists for SE

### Takeaway
The closest fit is a combination of standards:
- **Engineering Research** for comparing pipelines as artefacts;
- **Experiments** for the hypotheses, sample-size justification and effect sizes with CIs. It is formally for human participants and is used here by analogy.
- **Benchmarking** and **Quantitative Simulation** for repetitions and runs of stochastic systems;
- **Registered Reports** for pre-registration;
- **Sampling** for the fault set;
- **Open Science** (not read in detail).

The standards' README describes them as SE's analogue of CONSORT and PRISMA. No CONSORT adaptation was read.

### Cited Findings
- **Empirical Standards README** (B; FT yes; https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/README.md): "Evidence standards, like the CONSORT and PRISMA statements in health and medicine … attempt to express specific expectations for one or more types of research." "Unlike some previous attempts, our standards are method-specific."
- **Experiments standard** (B; FT yes): its application limits it to work that "involves human participants" and points elsewhere for experiments without humans. Its essential and antipattern items are quoted in Q2.
- **Engineering Research standard** (B; FT yes): essential items are "empirically evaluates the proposed artifact using … a benchmarking study … or another method for which a clear and convincing rationale is provided" and "clearly indicates which of the above empirical methodology is used". Desirable: "provides supplementary materials including source code … and any input datasets".
- **Benchmarking standard** (B; FT yes): essential items are "describes the experimental setup … in sufficient detail to support independent replication", "assesses stability or reliability using sufficient experiment repetitions and execution duration" and "discusses the construct validity of the benchmark".
- **Quantitative Simulation standard** (B; FT yes): number of runs per scenario, sensitivity analysis for input parameters, and versions of tools and environments.
- **Experiments standard suggested reading** (listed there, not read): Jedlitschka, Ciolkowski & Pfahl 2008, "Reporting Experiments in Software Engineering"; Wohlin et al. 2012, *Experimentation in Software Engineering*.

### Inferences
- *Inference.* **Reporting checklist for the trial**, a CONSORT-like flow adapted from the standards above:
  - **Flow diagram:** seeded → validated (realism checks) → excluded (equivalent or no-op, with reasons) → analysed per arm. Include aborted runs and why.
  - **Per-fault table** in the supplement: type, seeder, catches per family per run.
  - The 2×2 table, delta, p10 and p00 with CIs. Pre-registered and exploratory analyses in separate sections.
  - Model, version, temperature and prompt hashes, plus token counts per arm.
  - Every deviation from RR1 with its justification.
- *Inference.* The "Invalid criticisms" lists, e.g. "not enough participants (unless supported by power analysis)" and "low external validity", can be cited pre-emptively, provided the power analysis in Q1 is included.

### Gaps
- The **Open Science** supplement was downloaded but not analysed.
- No CONSORT or SPIRIT adaptation for SE or LLM evaluation was read.
- The General Standard file path could not be located on raw.githubusercontent.com (404 for the guessed paths).

---

## What this strand cannot settle

- **The actual psi and pi.** Every n above depends on the unknown discordance and its direction. Only a pilot, for example 10–12 faults × k runs, run *before* registration and excluded from the confirmatory set, can estimate psi, pi and the within-fault rho. Without one, plan for the worst plausible case (psi .2, pi .8 → about 100–116 faults).
- **Transfer from seeded to real misreadings.** No statistic in this strand addresses it. It belongs to the seeding-validity strand.
- **Between-operation variance.** It cannot be estimated from one operation at any number of faults.
- **Independence of lineages.** Statistics can test pairwise agreement of family outcomes, but cannot certify independence. Correlated LLM errors (Kim et al., per the earlier reports) may make E and S fail together, which raises p11 and p00 and shrinks psi. That would make the trial underpowered and also misleading.
- **Exact recommendations of Connor 1987, Lachin 1992, Arcuri & Briand 2011/2014 and Holm 1979.** These are [unreachable] here, and the numbers rest on own calculations instead.

## Self-check

- **"Family E" and "family S".** The task names them E and S. I took E to be the expectation family (prose-record-derived) and S the spec-enforcing family, matching brief §3.3 ("Spec-enforcing family only; expectation family only; both"). If E or S were meant as pipelines, the McNemar framing still holds but the labels swap meaning.
- **p01 ≈ 0.** The claim that S rarely catches spec misreadings is *my inference* from how S is derived. If the pipelines' S includes cross-form consistency gates (G3/G4) counted as "S catches", p01 can be substantial for the cross-table-contradiction type. The Q1 grid covers pi 0.7–1.0 for that reason.
- **"Neto et al."** The brief's "Neto et al." may mean a pre-registration paper I did not identify. I used de Oliveira Neto et al. 2019 (JSS) for statistical practice only.
- **Venue checks.**
  - Furia et al.: Crossref lists IEEE TSE with an early-access 2019 date and pages "1-1"; the final volume and issue were not verified.
  - Lakens 2014: read in its "In Press" author version.
  - Miller 2024: an arXiv preprint (A-pre).
- **The Experiments standard covers human-participant experiments only.** Applying it to an all-LLM trial is analogy (*Inference*). The Engineering Research and Benchmarking standards are the formally applicable ones.
- **Own simulations rest on simplifying assumptions.** They assume E and S are independent given the fault (sim C) and use Beta-distributed fault difficulty. Positive E–S correlation at fault level would *raise* power for paired tests and *lower* psi; the net effect is not computed. The O'Brien–Fleming and Pocock constants are standard two-look values, not derived here.
- **No challenge to an earlier report is made in this strand.** The only earlier-report text relied on is the verified edition's "at equal test counts" row, quoted verbatim in Q1, and it is adopted, not challenged.
