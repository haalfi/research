# Disclosure risk of data characterisations and synthetic data, controls, OSS tools, regulatory framing, and licensed reference data

Research date: 2026-11-26. Not legal advice.

Labels on every claim:
- **[D]** documented: the full text was retrieved and the cited passage was read (key passages pulled out with text search, not every page read end to end).
- **[L]** lead only: search-engine extract; the primary text was not read.
- **[U]** unreachable: the primary source was tried and could not be retrieved.
- **[I]** inference by this researcher.
- **[V]** vendor marketing or a vendor-authored claim.

Package dates come from the PyPI JSON API, the CRAN database (crandb.r-pkg.org) and blobless `git clone` of the GitHub repos (tag and last-commit dates), all read on 2026-11-26 **[D]**.

---

## 1. Attacks and risks: what aggregates, statistics, synthetic data and released models disclose

### Takeaway
Aggregates are not safe because they are aggregates. With enough accurate answers, the underlying records can be rebuilt (Dinur–Nissim; the US Census 2010 reconstruction rebuilt every record in 70% of census blocks from published tables). Synthetic data without DP leaks through outliers, and through linear-reconstruction attribute inference on ordinary records. Optimiser statistics (MCV lists, histogram bounds, min/max) contain actual data values and are treated as sensitive by PostgreSQL itself.

### Cited Findings

**Reconstruction from aggregates**
- **[D]** Dwork & Roth's textbook states the "Fundamental Law of Information Recovery": "overly accurate answers to too many questions will destroy privacy in a spectacular way". It credits "the first reconstruction attacks" to Dinur and Nissim. Definition 8.1 calls a mechanism "blatantly non-private" if an adversary can build a candidate database that agrees with the real one in all but o(n) entries. Theorem 8.1: with distortion bounded by E, an adversary can reconstruct the database to within 4E positions; "a privacy mechanism adding noise with magnitude always bounded by, say, n/401, permits an adversary to correctly reconstruct 99% of the entries". Theorem 8.2: a linear number of ±1 questions reconstructs almost the whole database if the curator answers at least ½+η of them within absolute error o(√n). — [Dwork & Roth, *The Algorithmic Foundations of Differential Privacy*, FnT-TCS 9(3–4), 2014](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)
- **[U]** The original Dinur & Nissim, "Revealing information while preserving privacy" (PODS 2003), did not download (the ACM DL and a PSU mirror returned HTML, not a PDF). It is cited here only through Dwork & Roth above. — [ACM DL 10.1145/773153.773173](https://dl.acm.org/doi/10.1145/773153.773173)
- **[D]** Dwork & Roth on differencing and query auditing: an auditor "may be on the lookout for pairs of queries that would constitute a differencing attack", but "refusing to answer a query is itself disclosive", and auditing "can be computationally infeasible". "Summary Statistics are Not 'Safe.'" — [Dwork & Roth 2014](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)
- **[D]** US Census 2010 reconstruction: "The 2010 Census published more than 150 billion aggregate statistics in 180 table sets." Using "only 34 of the published table sets, we reconstructed microdata records including five variables (census block, sex, age, race, and ethnicity)". "An attacker using our methods can verify that all records in 70% of all census blocks (97 million people) are perfectly reconstructed." Re-identification studies confirm that an attacker can "correctly infer the actual census response on race and ethnicity for 3.4 million vulnerable population uniques … with 95% accuracy". The paper says the assumption "that tabular data are inherently less disclosive than their underlying microdata is fundamentally flawed". It frames the goal of disclosure limitation as "leave-one-out" reasoning: preventing inferences the attacker could not have made had the subject's record not been used. — [Abowd et al., "A Simulated Reconstruction and Reidentification Attack on the 2010 U.S. Census", arXiv:2312.11283v3, 28 Jul 2025; HDSR, DOI 10.1162/99608f92.4a1ebf70 (just accepted)](https://arxiv.org/abs/2312.11283)
- **[D]** Cell suppression is fragile: "an arbitrarily large part of the suppression pattern can be unraveled if an attacker knows the value of a single cell that the system assumed was not known, which can occur either as prior knowledge or because some other group did a cell-suppressed release of overlapping data but didn't suppress the same cells." — [Abowd et al., "The 2020 Census Disclosure Avoidance System TopDown Algorithm", arXiv:2204.08986 (HDSR 2022)](https://arxiv.org/abs/2204.08986)

**Synthetic data: membership, attribute and linkage inference**
- **[D]** Stadler, Oprisanu & Troncoso: "synthetic data either does not prevent inference attacks or does not retain data utility … synthetic data does not provide a better tradeoff between privacy and utility than traditional anonymisation techniques". The privacy gain is "hard to predict" and "highly variable". The paper defines a linkability (membership) game, with shadow-model attacks on outlier target records. Its conclusion: a data holder cannot predict the minimum privacy gain, because that depends on which features an adversary targets and whether the generator preserved them. It also says implicit privacy protection "does not protect outlier records". — [Stadler et al., "Synthetic Data – Anonymisation Groundhog Day", arXiv:2011.07018v6, 24 Jan 2022 (USENIX Security 2022)](https://arxiv.org/abs/2011.07018)
- **[D]** Annamalai, Gadotti & Rocher propose an attribute inference attack "based on linear reconstruction methods for aggregate statistics, which target all records in the dataset, not only outliers". They evaluate it on probabilistic graphical models, GANs and DP synthetic data generators (SDGs). Their findings:
  - "current SDG methods cannot consistently provide sufficient privacy protection against inference attacks while retaining reasonable utility".
  - The best method was a DP SDG, and only "in very specific settings".
  - Prior attacks "can underestimate the privacy risk … by up to 10 percentage points", so empirical evaluation needs multiple attacks.
  - Releasing larger synthetic datasets increases leakage.
  - "synthetic data on its own should not be seen as an all encompassing solution".
  — [Annamalai et al., "A Linear Reconstruction Approach for Attribute Inference Attacks against Synthetic Data", arXiv:2301.10053v3, 9 May 2024](https://arxiv.org/abs/2301.10053). The venue (USENIX Security 2024) is **[I]**; it was not confirmed in the text read.
- **[D]** TAPAS: "Since synthetic records are not linked to real persons, this intuitively prevents classical re-identification attacks. However, this is insufficient to protect privacy." It is a toolbox of attacks (generalisations of prior work plus new attacks) with a threat-modelling framework. Authors are from the Alan Turing Institute and the ONS. — [Houssiau et al., "TAPAS: a Toolbox for Adversarial Privacy Auditing of Synthetic Data", arXiv:2211.06550v1, 12 Nov 2022](https://arxiv.org/abs/2211.06550)
- **[D]** NIST SP 800-226 privacy hazard: "Synthetic data generated without differential privacy may be susceptible to privacy attacks." — [NIST SP 800-226, March 2025](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)
- **[D]** NIST SP 800-226 privacy hazard: "In differentially private bar charts, revealing the bar chart bins may violate privacy." This applies directly to histograms whose bin edges are taken from the data. — [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)

**Optimiser statistics (min/max, MCV lists, distinct counts, histograms)**
- **[D]** PostgreSQL documentation: "pg_statistic should not be readable by the public, since even statistical information about a table's contents might be considered sensitive. (Example: minimum and maximum values of a salary column might be quite interesting.)" The `pg_stats` view "allows access only to rows of pg_statistic that correspond to tables the user has permission to read". — [PostgreSQL docs, pg_statistic (current)](https://www.postgresql.org/docs/current/catalog-pg-statistic.html); [pg_stats](https://www.postgresql.org/docs/current/view-pg-stats.html)
- **[D]** `pg_stats` columns:
  - `most_common_vals` is "A list of the most common values in the column", with `most_common_freqs` giving their frequencies.
  - `histogram_bounds` is "A list of values that divide the column's values into groups of approximately equal population".
  - `n_distinct` = -1 indicates a unique column.
  — [PostgreSQL docs, pg_stats](https://www.postgresql.org/docs/current/view-pg-stats.html)
- **[D]** CVE-2017-7484, "selectivity estimators bypass SELECT privilege checks", fixed in 9.2.21–9.6.3 (2017-05-11). — [PostgreSQL security advisory](https://www.postgresql.org/support/security/CVE-2017-7484/)
- **[D]** CVE-2019-10130, "Selectivity estimators bypass row security policies": "PostgreSQL maintains statistics for tables by sampling data available in columns … a user … could craft a leaky operator that could read whatever data had been sampled from that column. If this happened to include values from rows that the user is forbidden to see by a row security policy, the user could effectively bypass the policy." Fixed 2019-05-09 (9.5.17–11.3). — [PostgreSQL security advisory](https://www.postgresql.org/support/security/CVE-2019-10130/)

**Small cells, differencing, outliers (output-checking view)**
- **[D]** SACRO guide on thresholds and differencing:
  - The threshold is "The minimum number of observations that a statistic should be based on". "3 is used in textbooks as it is the only value with a clear statistical justification. Most organisations now use a higher value (5 or 10) to (a) provide a margin of error and (b) to protect against differencing."
  - Residual degrees of freedom of 10 has been "widely used as the minimum" since Brandt et al. (2010).
  - Differencing example: mean earnings in a village of 16 people are £49,125; omitting the top earner gives £32,400 for the other 15, and "the difference … creates an implicit statistic about the additional observation".
  - The guide also lists dominance, class disclosure, structural zeros and model saturation as risks.
  — [Ritchie et al., *The SACRO guide to statistical output checking*, SACRO WP1 deliverable, Oct 2023, Zenodo 10.5281/zenodo.10054629](https://zenodo.org/records/10282526/files/The%20SACRO%20guide%20to%20statistical%20output%20checking.pdf)
- **[I]** Arithmetic on the SACRO example: 16×49,125 − 15×32,400 = £300,000, the excluded person's exact earnings.
- **[D]** SACRO guide on graphs: "Graphs do not present new issues. In theory, every graph can be represented as a table … a pie chart or a histogram are clearly just one-way tabulations". — [SACRO guide, Oct 2023](https://zenodo.org/records/10282526/files/The%20SACRO%20guide%20to%20statistical%20output%20checking.pdf)

**Leakage through a released generative model**
- **[D]** Stadler et al. say that when a trained model, rather than only its samples, is shared, the threat model widens to include white-box attacks. They treat black-box access to a single synthetic dataset as the data-sharing scenario. — [Stadler et al. 2022](https://arxiv.org/abs/2011.07018)
- **[D]** NIST: "Machine learning techniques do not automatically protect privacy." — [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)

### Inferences
- **[I]** For the platform in the brief, every "characterisation" export is a set of query answers. Marginals, per-column histograms, distinct-value lists, MCV lists, min/max, null rates, cross-tabs and fitted model parameters all count toward the Dinur–Nissim budget. Without noise, enough of them reconstructs records, and joint cross-tabs on quasi-identifiers do so fastest (Census 2010 used 34 table sets).
- **[I]** Raw optimiser statistics (`pg_stats`, or MySQL/Oracle/Spark column stats) are disclosive by design: MCV lists and histogram bounds are real values, and min/max are real extremes, often outliers such as the highest salary or rarest code. Exporting them unmodified is equivalent to exporting samples of records. Any export of planner statistics should be regenerated from noised or coarsened data, or replaced by DP histograms with data-independent bin edges (per the NIST bar-chart hazard).
- **[I]** Multi-source entity overlap makes linkage and differencing worse: when several sources describe the same entity, the same individual enters several aggregates, which amplifies their contribution. The DP "unit of privacy" has to be the real-world entity (person or household) after entity resolution, not the source row. NIST lists "Guarantees with different units of privacy are not directly comparable" and "When bounding user contributions, additional noise must be added to ensure user-level privacy" as hazards **[D]**.

### Gaps
- No full text was read for Shokri-style model membership inference or for "linkage" papers beyond Stadler and TAPAS (ML training is out of scope).
- I found no peer-reviewed paper specifically on reconstruction from exported DBMS optimiser statistics. The PostgreSQL docs and CVEs are the primary evidence.

---

## 2. Repeated releases: composition, budgets over time, continual release, agency practice

### Takeaway
Under DP, privacy loss adds up across releases, so a budget must be set for the life of the data and tracked. Streaming or continual-release mechanisms exist for repeated updates. Traditional SDC has no composition theorem; agencies counter differencing across overlapping tables with perturbation (ONS cell key) and swapping. Releasing non-DP outputs alongside DP outputs voids the DP accounting for that data.

### Cited Findings
- **[D]** NIST: "Differential privacy is compositional, meaning that the 'total privacy reduction' of multiple data releases can be considered to ensure that it does not get too large over time." Example: 10 analyses with εᵢ = 0.1 each give a total budget of ε = 1. Post-processing invariance and group privacy are listed as further properties. — [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)
- **[D]** NIST privacy hazards relevant to repeated releases:
  - "The use of differential privacy does not mitigate privacy risks associated with other (non-differentially private) releases based on the same underlying data" (Sec. 2.6).
  - "Large values of ε may not provide meaningful privacy."
  - With (ε, δ)-DP, "set δ ≤ 1/n²" because of possible catastrophic failure.
  - Event-level privacy (as opposed to person-level) "can result in surprisingly weak privacy guarantees".
  — [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)
- **[D]** NIST also says the interactive query-answering model carries more risk than a one-off data release, because queries are not known in advance. — [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)
- **[D]** NIST SP 800-226 is final, "Date Published: March 2025". Authors: Joseph Near (Univ. of Vermont), David Darais (Galois), Naomi Lefkovitz (NIST), Gary Howarth (NIST). — [NIST CSRC publication page](https://csrc.nist.gov/pubs/sp/800/226/final)
- **[D]** Dwork & Roth §12.3 on continual observation: "Many applications of data analysis involve repeated computations … the system is required to continually produce outputs. We therefore need techniques for achieving differential privacy under continual observation". It defines event-level vs user-level adjacency. The counter construction uses a tree of interval noise values (about log T noise terms), so error grows only polylogarithmically in T. Appendix B covers advanced composition (Theorem 3.20), which beats the linear factor of k. — [Dwork & Roth 2014](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)
- **[D]** Census 2020 TopDown Algorithm (TDA): it "creates noisy versions of key queries on the data, referred to as measurements, using zero-Concentrated Differential Privacy". Invariants are "statistics that the Census Bureau has determined, as matter of policy, to exclude from the privacy-loss accounting". The final production setting for the redistricting data was ρ = 2.63 (zCDP), and "No single point on [the (ε,δ) curve] summarizes the value of rho completely". DP mechanisms "do not degrade under post-processing", avoiding accurate reconstruction "if agencies reasonably control their expended privacy-loss budget". — [Abowd et al., TDA, arXiv:2204.08986](https://arxiv.org/abs/2204.08986)
- **[D]** The Census follow-up paper shows that 2020-style DP releases defeat its reconstruction attack. The 2010 disclosure methods (swapping plus tabular rules) did not. — [Abowd et al., arXiv:2312.11283v3](https://arxiv.org/abs/2312.11283)
- **[D]** ONS Census 2021 used three protections:
  - "targeted record swapping … the geographies were changed for between 7% and 10% of households, and for between 2% and 5% of individuals in communal establishments";
  - "a cell key method to protect against disclosure by differencing by adding 'noise' to every dataset … a typical dataset would have around 14% of cell counts perturbed by a small amount, and small counts were more likely to have been perturbed than large counts";
  - disclosure rules to prevent very sparse datasets in the flexible table builder.
  — [ONS, "Protecting personal data in Census 2021 results"](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/protectingpersonaldataincensus2021results)
- **[D]** SACRO: thresholds of 5 or 10 are used partly "to protect against differencing". This is a heuristic, not a bound. — [SACRO guide](https://zenodo.org/records/10282526/files/The%20SACRO%20guide%20to%20statistical%20output%20checking.pdf)

### Inferences
- **[I]** For "test data that behaves like real data" refreshed over time, there are two viable patterns:
  - (a) A one-off DP synthetic snapshot or measurement set per schema version, with a fixed lifetime budget. Later dev and test data is post-processed from it at no extra privacy cost.
  - (b) Periodic DP refreshes with a ledger of ε or ρ per entity, summed by composition, and possibly a continual-release mechanism for growing counts.
  Pattern (a) is far cheaper in budget. Each re-characterisation of the same records spends budget again.
- **[I]** Mixing a DP characterisation with any exact export (exact row counts, exact distinct counts, exact min/max) of the same data breaks the DP accounting, per NIST §2.6. Invariants must be few and deliberate, as in TDA (whose invariants were policy choices outside the accounting).
- **[I]** Cell-key perturbation (ONS, ABS) gives consistent noise for the same cell across tables and releases, which blunts differencing. It has no formal composition bound.

### Gaps
- Census Bureau web pages on the 2020 privacy-loss budget allocations returned 404 or were not found at the URLs tried. The ρ = 2.63 figure is from the TDA paper only.
- No full text was read on Eurostat or UNECE guidance for repeated or overlapping tables (the Hundepool et al. *Handbook on SDC* was not retrieved).

---

## 3. Controls: SDC methods, output checking (Five Safes / TRE), and SDC tools

### Takeaway
Classic SDC (thresholds, suppression, rounding, top/bottom coding, k-anonymity-family generalisation, swapping, cell-key noise) is mature and well tooled: sdcMicro, sdcTable, tau-Argus, ARX, ACRO and synthpop are all active in 2025–26, while mu-Argus is dormant. It offers heuristic, attack-specific protection with no composition guarantee. Output checking (SACRO/ACRO, statbarns) is the established TRE pattern for deciding what may leave.

### Cited Findings
- **[D]** ACRO "supports the semi-automated checking of research outputs (SACRO) for privacy disclosure within secure data environments". It sits over analysis tools that produce tables, plots and statistical models, and it:
  - identifies potentially disclosive outputs "against a range of commonly used disclosure tests";
  - applies optional mitigation;
  - reports reasons;
  - produces summary documents for TRE staff.
  The SACRO-Viewer GUI supports human checkers, and an R wrapper (ACRO-R) is available. The README cites IEEE DOI 10.1109/TP.2025.3566052. — [ACRO README (raw.githubusercontent.com)](https://raw.githubusercontent.com/AI-SDC/ACRO/main/README.md)
- **[D]** ACRO release history on PyPI: first release 0.0.1 on 2022-10-12, then 1.0.0 (2026-08-10), 1.0.2 (2026-08-28) and 1.1.0 (2026-11-05). Actively maintained. — [PyPI acro](https://pypi.org/project/acro/)
- **[D]** The SACRO guide (Oct 2023) introduces the "statbarn" model, first presented 18 May 2023 and then to the UNECE/Eurostat Expert Group on Statistical Data Confidentiality (Wiesbaden, Sept 2023). A final version was announced for March 2024. It covers principles-based vs rules-based output SDC and "Active Researcher Management". — [SACRO guide](https://zenodo.org/records/10282526/files/The%20SACRO%20guide%20to%20statistical%20output%20checking.pdf)
- **[L]** outputchecking.org says that as of July 2025, 14 statbarns had been identified and 12 fully described. It gives "any frequency must be based on at least five observations" as an example rule, and says SACRO was originally commissioned by Eurostat in 2020. — [outputchecking.org](https://outputchecking.org/?p=42)
- **[D]** synthpop now has disclosure measures. `disclosure()` computes identity disclosure for a set of quasi-identifier keys and attribute disclosure for a target variable, and `multi.disclosure()` wraps it. The authors recommend "RepU (replicated uniques) for identity disclosure and DiSCO (Disclosive in Synthetic Correct Original) for attribute disclosure", both as % of original records and comparable to the same measures on the original data. They flag apparent disclosures that come from relationships "expected to be known to anyone familiar with its features". — [Raab, Nowok & Dibben, "Practical privacy metrics for synthetic data", arXiv:2406.16826v6, 1 Sep 2026](https://arxiv.org/abs/2406.16826)
- **[D]** Anonymeter (Statice) quantifies "singling out, linkability, and inference risks, which are the three key indicators of factual anonymization according to data protection regulations, such as the European General Data Protection Regulation (GDPR)". — [Giomi et al., arXiv:2211.10459v1, 18 Nov 2022](https://arxiv.org/abs/2211.10459). **[V]** The authors' claim to be the first "legally aligned" evaluation is a vendor-authored claim.
- **[D]** ONS Census 2021 combined targeted record swapping, the cell key method and table-builder sparsity rules (see §2). — [ONS](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/protectingpersonaldataincensus2021results)

**SDC tool maintenance (as of 2026-11-26) [D]**

| Tool | Latest release (date) | Last commit | Notes |
|---|---|---|---|
| sdcMicro (R, microdata SDC) | 5.8.2 on CRAN (2026-06-12) | — | Maintainer Matthias Templ; [CRAN](https://cran.r-project.org/package=sdcMicro), [repo](https://github.com/sdcTools/sdcMicro) |
| sdcTable (R, tabular suppression) | 0.34.1 on CRAN (2026-11-12) | — | Maintainer Bernhard Meindl; [CRAN](https://cran.r-project.org/package=sdcTable) |
| synthpop (R) | 1.9-3 on CRAN (2026-09-10) | — | Maintainer Beata Nowok; [CRAN](https://cran.r-project.org/package=synthpop) |
| tau-Argus (tabular) | tag v4.2.5.2 (2024-08-14) | 2026-04-01 | [repo](https://github.com/sdcTools/tauargus) |
| mu-Argus (microdata) | tag v5.1.7b4 (2024-03-13) | 2024-03-13 | Dormant since 2024; [repo](https://github.com/sdcTools/muargus) |
| ARX (k-anonymity, l-diversity, t-closeness etc.) | v3.9.2 (2025-09-12) | 2025-10-01 | Previous release v3.9.1 was 2022-11-15, so releases are infrequent; [repo](https://github.com/arx-deidentifier/arx) |
| Anonymeter | 1.1.0 on PyPI (2026-07-23) | 2026-07-23 | Earlier releases 1.0.0 (2024-02-02) and git tag v1.0.1 (2025-11-18), which is not on PyPI; Clear BSD licence; [PyPI](https://pypi.org/project/anonymeter/) |
| TAPAS (alan-turing-institute/privacy-sdg-toolbox) | no tags | 2023-09-06 | Dormant / research code; [repo](https://github.com/alan-turing-institute/privacy-sdg-toolbox) |
| ACRO | 1.1.0 (2026-11-05) | — | Active (see above) |

### Inferences
- **[I]** For a "what may leave the protected environment" gate, the TRE output-checking model maps directly onto the platform:
  - Treat each export (aggregate table, stats profile, synthetic set, model) as an output under review.
  - Apply threshold, dominance and differencing rules (SACRO statbarns; ACRO for automated checks).
  - Keep an auditable log.
  ACRO's checks target tables, regression output and plots. It does not appear to cover DBMS-statistics exports or synthetic datasets, and that coverage is unverified.
- **[I]** k-anonymity, l-diversity and t-closeness (ARX, sdcMicro) protect a single release against record linkage on chosen quasi-identifiers. They do not compose across releases and do not stop reconstruction from many aggregates (§1). They suit a one-off "structurally realistic" test extract better than a stream of characterisations.
- **[I]** Synthetic-data risk metrics (Anonymeter, synthpop RepU/DiSCO, TAPAS) are evaluations, not guarantees. Annamalai et al. showed single attacks can under-estimate risk by up to 10 percentage points, so use several metrics and attacks, and treat a pass as necessary but not sufficient.

### Gaps
- GSS/ONS output-checking guidance and the Five Safes primary texts were not retrieved; the SACRO guide was used instead.
- The ARX feature list and the tau-Argus/mu-Argus manuals were not read; capabilities are named from general knowledge **[I]**.
- I did not verify the reported CNIL assessment of Anonymeter.

---

## 4. Controls: differential privacy libraries, NIST guidance, Census TDA, and maintenance state

### Takeaway
Mature OSS DP stacks exist and are maintained in 2026. OpenDP, the organisation behind the OpenDP Library, SmartNoise SQL/Synth and Tumult Analytics, is the centre of gravity. The Tumult Labs team joined LinkedIn (announced 31 Mar 2025) and OpenDP took over Tumult's libraries. Google DP and PipelineDP are active; IBM diffprivlib is slow-moving. NIST SP 800-226 (final, March 2025) is the evaluation guide.

### Cited Findings
- **[D]** LinkedIn press release, "Welcoming members of the Tumult Labs team to LinkedIn" (published Mar 31, 2025): "members of the Tumult Labs team will be joining LinkedIn. They bring deep expertise in differential privacy and algorithmic fairness". — [LinkedIn Pressroom, 31 Mar 2025](https://news.linkedin.com/2025/linkedin_update_engineering_march2025)
- **[D]** Tumult Analytics README: "Tumult Analytics — an OpenDP project … originally developed by Tumult Labs, and joined the OpenDP project after the Tumult Labs team joined LinkedIn." It is built on Tumult Core (now at github.com/opendp/tumult-core) and installs as `pip install tmlt.analytics`. It requires Spark per its docs. — [README, opendp/tumult-analytics](https://raw.githubusercontent.com/opendp/tumult-analytics/main/README.md)
- **[L]** Search extracts say Tumult Labs would sunset "its current form" within 90 days, that OpenDP took over maintenance, and that only select team members joined LinkedIn. The financial terms were undisclosed and Wilson Sonsini advised LinkedIn. — [WSGR](https://www.wsgr.com/en/insights/wilson-sonsini-advises-linkedin-on-transaction-with-tumult-labs.html); [opendp.org news](https://opendp.org/news-events)
- **[D]** The OpenDP news page lists "Announcing OpenDP Library v0.16.0" (8 Oct 2026). It also has a 23 Sep 2026 post on "OpenDP Core Team evolution (and new job opening for a Director!)", which mentions "a challenging 2025 (including several months in which most…" (truncated). Both point to some organisational turbulence in 2025. — [OpenDP News & Events](https://opendp.org/news-events)
- **[D]** NIST SP 800-226 privacy hazards for tool selection:
  - "Avoid custom … implementations of differentially private algorithms, and use well-tested libraries."
  - "Implementing … mechanisms in terms of infinite-precision real numbers" is hazardous (floating-point attacks).
  - "Current deep learning-based approaches for differentially private synthetic data produce significantly lower quality data than approaches based on marginals."
  §3.6 describes DP synthetic data via marginals.
  — [NIST SP 800-226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf)
- **[D]** The Census TDA uses zCDP measurements plus post-processing, with invariants. Its author list includes Tumult Labs. — [arXiv:2204.08986](https://arxiv.org/abs/2204.08986)

**DP tool maintenance (as of 2026-11-26) [D]**

| Library | Latest release (date) | Last commit | Notes |
|---|---|---|---|
| OpenDP Library (Rust/Python) | 0.16.0 (2026-10-06) | — | Nightly alphas to 2026-11-22; MIT; [PyPI](https://pypi.org/project/opendp/) |
| SmartNoise SQL | 1.0.10 (2026-04-14) | — | MIT; [PyPI](https://pypi.org/project/smartnoise-sql/) |
| SmartNoise Synth (MWEM, MST, AIM, PATE-CTGAN, etc.) | 1.0.8 (2026-04-15) | smartnoise-sdk repo 2026-04-21 | Releases about yearly in 2024–26; [PyPI](https://pypi.org/project/smartnoise-synth/). Synthesizer list is **[I]** from general knowledge, not verified this session |
| Tumult Analytics | 0.21.0 (2026-06-30) | 2026-11-24 | Previous release 0.20.2 (2025-09-11) |
| Tumult Core | 0.20.0 (2026-10-20) | — | [PyPI](https://pypi.org/project/tmlt.core/) |
| Google differential-privacy (C++/Go/Java, Privacy on Beam) | v4.1.0 (2026-02-04) | 2026-11-20 | [repo](https://github.com/google/differential-privacy) |
| PipelineDP (Python, Beam/Spark) | 0.3.1 (2026-06-19) | 2026-11-06 | No release between 0.2.2rc2 (2023-11-22) and 0.3.0rc1 (2026-04-01); [PyPI](https://pypi.org/project/pipeline-dp/) |
| PyDP (OpenMined wrapper of Google DP) | 1.1.5 (2026-05-11) | — | [PyPI](https://pypi.org/project/python-dp/) |
| IBM diffprivlib | 0.6.6 (2025-04-10) | 2026-11-23 | No release since April 2025; MIT; [PyPI](https://pypi.org/project/diffprivlib/) |

### Inferences
- **[I]** Fit to the brief (characterise inside, generate test data outside):
  - Inside the protected environment, compute DP marginals or measurements with OpenDP, Tumult Analytics (Spark-scale, privacy-ID / entity-level contributions) or SmartNoise SQL.
  - Or fit a marginal-based DP synthesiser (SmartNoise Synth MST/AIM) and export only the DP synthetic data or measurements.
  - Generate test data outside by post-processing, which costs no extra privacy.
  This matches NIST's advice that marginal-based DP synthetic data beats deep-learning DP synthesis for tabular data.
- **[I]** Tumult Analytics' per-privacy-ID accounting fits the many-sources-one-entity issue, provided entity resolution happens inside the protected environment before measurement. This is inferred from the library design; its docs were not re-read this session.
- **[I]** Ownership risk: Tumult's original company no longer develops it. OpenDP maintains it, and OpenDP itself reported a difficult 2025. Releases nonetheless continued in 2026 (0.21.0 Analytics, 0.20.0 Core).

### Gaps
- The SmartNoise Synth synthesizer list and the OpenDP v0.16 feature notes were not read.
- The Census Bureau's own disclosure-avoidance documentation pages (census.gov) returned "Page not found" at the URLs tried.

---

## 5. Regulatory framing: anonymisation vs pseudonymisation; synthetic data and aggregates under GDPR / UK GDPR

### Takeaway
In EU and UK law, data is anonymous only if identification risk is reduced to a remote or insignificant level by means reasonably likely to be used. Pseudonymised data stays personal data for anyone who can re-identify with additional information. The EDPB 01/2025 pseudonymisation guidelines (consultation version, Jan 2025) and the ICO's anonymisation guidance (published 28 Mar 2025, now under review after the Data (Use and Access) Act) both say so. The CJEU (EDPS v SRB, 4 Sep 2025) reportedly accepted that pseudonymised data may be non-personal for a recipient without reasonable means of re-identification; that rests on search extracts only. Synthetic data and aggregates can be anonymous only after a context-specific risk assessment.

### Cited Findings
- **[D]** EDPB Guidelines 01/2025 on Pseudonymisation, "Adopted on 16 January 2025", version for public consultation: "Pseudonymised data, which could be attributed to a natural person by the use of additional information, is to be considered information on an identifiable natural person, and is therefore personal. This statement also holds true if pseudonymised data and additional information are not in the hands of the same person. Even if all additional information retained by the pseudonymising controller has been erased, the pseudonymised data can be considered anonymous only if the conditions for anonymity are met." — [EDPB Guidelines 01/2025 v1 PDF](https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf)
- **[D]** EDPB consultation page: feedback period "17 January - 14 March 2025"; the only document offered is "Guidelines 01/2025 v1". — [EDPB consultation page](https://www.edpb.europa.eu/our-work-tools/documents/public-consultations/2025/guidelines-012025-pseudonymisation_en)
- **[L]** A search extract says the consultation ran to 28 February 2025, which conflicts with the page above. A law firm expected a final version later in 2025.
- **[D]** ICO anonymisation guidance: "28 March 2025 – this guidance was published." It says to "reduce the risks of identifying people to a sufficiently remote level that the information is effectively anonymised". The page now states: "Due to the changes made by the Data (Use and Access) Act, this guidance is under review and may be subject to change". The ICO plans page says DUAA work forced it to deprioritise or withdraw some planned guidance. — [ICO, Anonymisation – About this guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/about-this-guidance/); [ICO plans for guidance](https://ico.org.uk/about-the-ico/what-we-do/our-plans-for-new-and-updated-guidance/)
- **[L]/[U]** CJEU, Case C-413/23 P, EDPS v SRB, judgment of 4 September 2025. Per commentators:
  - The Court set aside General Court T-557/20 and referred the case back.
  - It rejected the EDPS view that pseudonymised data is always personal data for every recipient.
  - It held that identifiability for the controller's duty to inform is assessed from the disclosing controller's perspective at the time of collection.
  - Commentators stress the bar for treating data as non-personal remains high.
  The judgment text was unreachable (curia and EUR-Lex returned empty content to the fetcher). — [Official Journal C/2025/5551 (not read)](https://eur-lex.europa.eu/eli/C/2025/5551/oj/eng); [Inside Privacy commentary](https://www.insideprivacy.com/eu-data-protection/eu-court-of-justice-clarifies-the-concept-of-personal-data-in-the-context-of-a-transfer-of-pseudonymized-data-to-third-parties/); [Stalla-Bourdillon, PDP 26(1)](https://cris.vub.be/ws/portalfiles/portal/138144662/Between_nuance_and_caution_how_to_read_the_CJEU_s_judgment_in_EDPS_v_SRB_by_Sophie_Stalla-Bourdillon_Privacy_Data_Protection_Volume_26_Issue_1.pdf)
- **[L]/[U]** EDPS TechSonar on synthetic data (the page returned 403): "a privacy assurance assessment should be performed to ensure that the resulting synthetic data is not actual personal data". It notes outliers may be missed and biases reproduced. An EDPS blog notes that whether synthetic data counts as personal data "is still debated". — [EDPS TechSonar: Synthetic data](https://edps.europa.eu/press-publications/publications/techsonar/synthetic-data_en); [EDPS blog](https://edps.europa.eu/press-publications/press-news/blog/future-privacy-synthetic_en)
- **[D]** Anonymeter operationalises the Article 29 WP / GDPR anonymisation criteria of singling out, linkability and inference. — [arXiv:2211.10459](https://arxiv.org/abs/2211.10459)
- **[D]** The Census reconstruction paper treats published aggregates as capable of confidentiality-violating inference (leave-one-out), not as automatically safe. — [arXiv:2312.11283](https://arxiv.org/abs/2312.11283)

### Inferences
- **[I]** Aggregates and synthetic data leaving the protected environment are not anonymous by construction. A documented identifiability assessment is needed per release type: means reasonably likely, attacker knowledge, uniqueness, linkage with the other sources that describe the same entities. Evidence would include DP parameters, or SDC rule compliance plus attack-based metrics (Anonymeter, synthpop disclosure, TAPAS-style attacks).
- **[I]** If the EDPS v SRB reading is right, dev and test recipients outside the protected environment with no access to keys or source data may be in a better position. But per the EDPB, even erasing the keys does not make pseudonymised data anonymous unless the anonymity conditions are met. Hashing or tokenising identifiers in test copies is therefore pseudonymisation, and those copies remain personal data for the platform operator.
- **[I]** UK position: the ICO guidance of 28 Mar 2025 is the current reference, but it is flagged as under review because of the DUAA 2025.

### Gaps
- Whether the EDPB adopted a final post-consultation version of 01/2025 by Nov 2026 is unconfirmed: the EDPB guidelines listing URL returned "Not found", and the consultation page shows only v1.
- No EDPB anonymisation guidelines (long announced) were found or read.
- The full text of the SRB judgment was unreachable.

---

## 6. Licensed reference data: is it a separate constraint, and do aggregates or synthetic copies count as derived works?

### Takeaway
Yes. Licensed reference data is a separate constraint from privacy, set by contract and database rights rather than by identifiability, and licences define "derived" material broadly. Under ODbL, extracting a "Substantial" part into a new database makes a Derivative Database (share-alike when used publicly). A query result such as a chart or statistic is a "Produced Work" (attribution only), and use inside an organisation and its contractors is not "Public". SNOMED CT lets licensees create and use Derivatives but restricts distribution by territory and through sub-licences. Exchange market-data policies make derived data creation a licensed (often non-display, fee-liable) use, whatever the copyright position. Not legal advice.

### Cited Findings
**OpenStreetMap / ODbL 1.0 [D]** ([ODbL 1.0 text](https://opendatacommons.org/licenses/odbl/1-0/))
- "Derivative Database" means "a database based upon the Database, and includes any translation, adaptation, arrangement, modification, or any other alteration of the Database or of a Substantial part of the Contents. This includes … Extracting or Re-utilising the whole or a Substantial part of the Contents in a new Database."
- "Produced Work" means "a work (such as an image, audiovisual material, text, or sounds) resulting from using the whole or a Substantial part of the Contents (via a search or other query) from this Database [or] a Derivative Database".
- "Publicly" means "to Persons other than You or under Your control by either more than 50% ownership or by the power to direct their activities (such as contracting with an independent consultant)". Use "internally within an organisation is not to the public".
- §4.3: creating and using a Produced Work does not require the §4.2 notice, but public use of a Produced Work requires a notice that content came from the database.
- §4.6: if you Publicly Use a Derivative Database, or a Produced Work from one, you must offer the entire Derivative Database or the alterations / "method of making the alterations … (such as an algorithm)" in machine-readable form.

**OSMF "Substantial" guideline [D]**
- Extractions of "Less than 100 Features" are treated as non-substantial (if one-off and not repeated). More than 100 features is non-substantial only if the extraction is non-systematic and based on qualitative criteria. "The systematic extraction of all eating places within an area … would be considered to be systematic." Features relating to an area of up to 1,000 inhabitants are also covered. — [OSMF Licence/Community Guidelines/Substantial – Guideline](https://wiki.osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline)

**SNOMED CT Affiliate Licence [D]** ([SNOMED CT Affiliate License Agreement, NHS TRUD copy, licence id 4; version date not shown in extracted text](https://isd.hscic.gov.uk/trud/users/guest/filters/0/licence/4))
- "Derivative" means "a work consisting of (a) SNOMED CT Content … together with (b) either (i) additional properties and/or information about such SNOMED CT content; and/or (ii) any set of relationships between that SNOMED CT Content and content of other nomenclature … and includes a Cross-Map and a Sub-Set".
- Clause 2.1 grants rights to use the International Release, "create Extensions and Derivatives … and use and modify" them, and incorporate it into Licensee Products distributed under sub-licence.
- Clause 2.2.4 allows public-facing systems "including browsers and data analysis systems" only if "users of those systems are not able to extract any substantial portion of SNOMED CT".
- Use and distribution in a Non-Member Territory carries fees and conditions (clauses 7 and 9). Clause 9.3 requires notice to the Licensor before exercising rights in a new Non-Member Territory.

**Exchange market data**
- **[D]** Cboe Europe Market Data Policy (effective 1 Aug 2026, published 7 Apr 2026):
  - Non-display rights are required for listed uses "whether or not the Market Data Client creates Derived Works with the Data".
  - "Financial Products" are instruments "derived in whole or in part from the Data".
  - "Internal use of Delayed and Historical Data, including … research is not subject to Fees and does not require a Data Agreement".
  - External value-added historical services are fee-liable.
  - A "Development Waiver" exists for new vendors' lead time.
  — [Cboe Europe Data Policy, Aug 2026](https://cdn.cboe.com/resources/participant_resources/Cboe_Europe_Data_Policy_August_2026.pdf)
- **[D]** Deutsche Börse Market Data Policy Guidelines & FAQ v3.0: where derived data (e.g. iNAVs) is calculated on behalf of a third party, that third party needs a Non-Display Data Usage licence. — [Deutsche Börse FAQ v3.0](https://www.mds.deutsche-boerse.com/resource/blob/5322802/8a82ea41893249520d1b5fb4878c8dad/data/Market%20Data%20Policy%20Guidelines%20and%20FAQ_V3_0.pdf)
- **[L]** Exchange policies commonly define Derived Data broadly as "any data … derived from or based on the Data". Common restrictions limit it to non-display use, require separate Derived Data licences or fees, and restrict recipients. Some exchanges distinguish internal (non-fee-liable) creation from external distribution. — [MarketsMedia](https://articles.marketsmedia.com/complexities-expand-in-market-data-licensing); [JSE General Data Use Policy](https://www.jse.co.za/sites/default/files/media/documents/2%20General%20Data%20Use%20Policy_v2.pdf)

### Inferences
- **[I]** Classify each reference source by its licence vocabulary before any characterisation leaves the protected environment:
  - (a) Copying actual reference values, such as code lists, concept IDs, instrument identifiers or address records, into synthetic test data is extraction or re-use of Contents. It is likely a Derivative Database (ODbL), a Derivative or Sub-Set (SNOMED) or Derived Data (market data).
  - (b) Aggregate statistics such as counts by category, value-length distributions or null rates sit closer to ODbL "Produced Work" or non-substantial extracts. But exchange contracts can still cover any data "derived from or based on" theirs.
  - (c) Structure only (schema, formats, check-digit rules, cardinality ranges) is the lowest risk.
- **[I]** Dev and test environments of the same organisation or its contractors are likely "not Public" under ODbL, so share-alike would not trigger. They may still fall outside a contract's licensed site, users or territory (SNOMED territories; market data "licensed environment" terms). The licensed-environment boundary may differ from the privacy boundary.
- **[I]** Practical approaches, in order of preference:
  1. Use public or open substitutes: freely published code standards, OSM under ODbL with attribution, and public test vectors.
  2. Reproduce only structure and statistics, with fake values that keep format and validity rules but not real codes.
  3. Obtain vendor test or development licences or waivers (e.g. the Cboe Development Waiver) or confirm in writing that dev and test copies are covered.
  4. Record per-source licence classification next to the privacy classification in the export gate.
- **[I]** Privacy and licence controls are independent. A DP synthetic copy of licensed reference data can be privacy-safe and still breach the licence, because DP does not reduce the extraction of real code values that are themselves the licensed content.

### Gaps
- ISO 3166 / ISO code licensing: the iso.org page returned no usable content (60 bytes). Licensing of the ISO 3166 database and the free use of codes is unverified.
- Postal address files (e.g. Royal Mail PAF) were not researched.
- Financial data vendor (as opposed to exchange) licences, such as Bloomberg or LSEG, were not read; these are commercial terms, typically under NDA.
- No court decision or regulator text was found on whether DP synthetic data counts as a "derived work" under copyright or the EU sui generis database right. This is an open legal question.
