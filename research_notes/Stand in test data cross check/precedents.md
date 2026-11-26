# Precedents cited by the external report: Lu/Miklau/Gupta (private synthetic databases for system evaluation) and the NHS England Artificial Data Pilot

Scope: verify two precedents that the unverified external report (`external_report_unverified.md`, lines 29, 130–147, 203, 802–804, 960–993) cites, and that earlier runs missed or could not reach. Research date: 2026-11-26. Labels: **[documented]** = full text read; **[lead]** = search extract or metadata only; **[inferred]** = my inference; **[unreachable]**; **[vendor]** = self-description by the producer.

Downloads are in the scratchpad under `p3a_lu/`, `p3a_cites/`, `p3a_nhs/`, `p3a_nhsweb/` and `p3a_irg/`.

---

## 1. Lu, Miklau & Gupta: what the paper is and how it works

### Takeaway
The external report's title and year are wrong. Two Miklau-group papers exist:
- **2011:** a short workshop paper, Gupta, Miklau & Polyzotis, "Private Database Synthesis for Outsourced System Evaluation" (AMW 2011).
- **2014:** the full paper, Lu, Miklau & Gupta, "Generating Private Synthetic Databases for Untrusted System Evaluation" (IEEE ICDE 2014, pp. 652–663).

No paper is titled "…for Database Application Testing". That phrase belongs to an earlier, non-DP paper by Wu et al. (2007), which both Miklau papers cite.

The method is close to the brief's problem:
1. The data owner derives counting queries (intermediate cardinalities of the query plans) from a SQL workload.
2. These are answered under differential privacy (DP) with the matrix mechanism, extended to multi-table schemas.
3. Only the noisy statistics, an obfuscated isomorphic schema and an obfuscated workload are released.
4. The untrusted party samples synthetic databases from these. It never touches the real data.

"Utility" means performance fidelity, not answer accuracy: optimizer estimated cost and actual running time, evaluated on PostgreSQL with TPC-H and skewed TPC-H. It is a research prototype. I found no public code.

### Cited Findings

**Identity and bibliography**
- **[documented]** Miklau's publications page lists "Generating Private Synthetic Databases for Untrusted System Evaluation", Wentian Lu, Gerome Miklau and Vani Gupta, ICDE 2014, with the PDF at `assets/pubs/dp/lu2014generating.pdf`. — [Miklau publications](https://people.cs.umass.edu/~miklau/publications.html) (accessed 2026-11-26)
- **[documented]** The same page lists, under 2011, "Private Database Synthesis for Outsourced System Evaluation", Vani Gupta, Gerome Miklau and Neoklis Polyzotis, Alberto Mendelzon International Workshop on Foundations of Data Management (AMW) 2011, PDF `Gupta11Private.pdf`. — [Miklau publications](https://people.cs.umass.edu/~miklau/publications.html)
- **[documented]** The ICDE paper calls itself "a significant extension to preliminary work [14]", where [14] is the AMW 2011 paper. — [Lu et al. 2014 PDF](https://people.cs.umass.edu/~miklau/assets/pubs/dp/lu2014generating.pdf)
- **[lead]** OpenAlex metadata for the ICDE paper:
  - OpenAlex ID W2028628865; DOI 10.1109/ICDE.2014.6816689.
  - Publication date 2014-03-01; pages 652–663; "2014 IEEE 30th International Conference on Data Engineering".
  - 28 citations (OpenAlex). The AMW paper is W2405382494, with 8 citations.
  - Source: [OpenAlex W2028628865](https://api.openalex.org/works/W2028628865)
- **[documented]** Both papers cite Wu, Wang, Guo & Zheng, "Privacy preserving database generation for database application testing", *Fundamenta Informaticae* 78(4):595–612, 2007. Its title is the closest match to the external report's "Generating Private Synthetic Databases for Database Application Testing".
  - Lu et al. describe Wu et al. as using "cell suppression and perturbation". They say it "cannot satisfy differential privacy and is susceptible to the previously-documented attacks on anonymization schemes".
  - Sources: [Gupta et al. 2011 PDF](https://people.cs.umass.edu/~miklau/assets/pubs/dp/Gupta11Private.pdf); [Lu et al. 2014 PDF](https://people.cs.umass.edu/~miklau/assets/pubs/dp/lu2014generating.pdf)

**AMW 2011 workshop paper (Gupta, Miklau, Polyzotis)**
- **[documented]** Setting: "secure outsourced system evaluation" (performance tuning, index selection, row- versus column-store choices) by an untrusted third party.
- **[documented]** What is released:
  - An isomorphic schema S′ with obfuscated table and column names. Key and foreign-key (FK) constraints are kept, and domains may be generalised (example: salary 25,000–200,000 becomes 0–500,000).
  - A workload W′ whose query constants are mapped to the new domain.
  - DP statistics ST′. "We do not release a surrogate dataset in place of D."
- **[documented]** Column models, chosen by the owner to fit the workload:
  - null model (domain only);
  - number of distinct values;
  - one-dimensional histogram;
  - joint histogram;
  - FK frequency model (fan-out).

  Columns with no released joint statistic are generated as independent. The joint-histogram generator was not implemented.
- **[documented]** Privacy: (ε, δ)-DP using the Gaussian mechanism. Accuracy is improved with the matrix mechanism (histograms) and with consistency post-processing (FK frequencies).
  - The paper notes that per-tuple DP does not protect population aggregates such as table size or sales count. It proposes "group privacy" for k tuples, and says that otherwise "it may not be feasible to accomplish safe workload release."
- **[documented]** Accuracy metric: cost(W, D) against cost(W′, D′). Candidate costs are "query result cardinality, estimated execution metrics (time or IOs), actual execution metrics (time or IOs), qualitative aspects of the query execution plans, and properties of index usage."
  - Error is split into *modeling error*, caused by the choice of statistics, and *perturbation error*, caused by DP noise.
- **[documented]** Experiments: TPC-H SF1 on Postgres 8.1, measuring only query result cardinality.
  - Three tables were synthesised (Orders, Lineitem, Customer), with FK models and 1-D histograms on predicate columns.
  - Result-size ratios, private model against truth:
    - Q1–Q4 (join, or a single range condition): about 1.00.
    - Q5 (three range conditions across tables): 0.20.
    - For comparison, the Postgres optimizer's own estimate ratio was up to 4.19 (Q3).
  - The authors attribute the Q5 failure to the FK generator modelling "out-degree" but not correlation with attributes of the referenced table.
  - Source: [Gupta et al. 2011 PDF](https://people.cs.umass.edu/~miklau/assets/pubs/dp/Gupta11Private.pdf)

**ICDE 2014 full paper (Lu, Miklau, Gupta)**
- **[documented]** Goal: synthesise "in a provably private manner, a relational database instance that matches the performance properties of the original database, especially with respect to a given target workload", preserving "IO counts, results sizes, and execution times".
- **[documented]** Pipeline (Fig. 1):
  1. The owner selects a model Q, a set of counting queries, from the schema and workload.
  2. The owner perturbs Q's answers to get a DP model Q′.
  3. The owner releases S′, W′ and Q′. The analyst samples one or more synthetic instances, and can scale them up.

  The sampling steps "use the private perturbed model as input and make no further use of the original database."
- **[documented]** Model selection: counting queries are taken from intermediate operator cardinalities across all possible query trees of each workload query, "similar to Arasu et al [1]".
  - Γi(W) is the set of i-way join counts.
  - The models form a spectrum: Null Model (table sizes only), C1TM (single-table predicates), C2TM (up to 2-way joins), C3TM, and Saturated Model (all intermediate counts).
  - More descriptive models need more noise.
  - The paper restricts itself to key/FK joins and acyclic schema graphs.
- **[documented]** Multi-relation DP:
  - One table is the "protected entity" (TPC-H Customer). Neighbouring databases differ by a cascading deletion of one entity and its descendants (orders, line items) and the ancestors it references.
  - Sensitivity is scaled by a "df value" computed from *propagation constraints* K(X,Y), the maximum fan-out.
  - Entities whose fan-out exceeds K are only "partially protected".
  - Example: with K(C,O)=41 and K(O,L)=7, the sensitivity of a single Lineitem count is 287. With the true sTPC-H maximum of 15,935 orders per customer it would be 15,935×7.
  - Setting K=41 fully protects 99.764% of customers in sTPC-H.
- **[documented]** Perturbation:
  - Each table is encoded as a "denormalized data vector" that includes ancestor attributes, to keep noisy answers consistent.
  - A unit mechanism (the matrix mechanism of Li & Miklau) runs per data vector under sequential and parallel composition. A heuristic O(n³) partition search allocates the privacy budget.
- **[documented]** Sampling: noisy models may be "non-realizable", meaning no instance satisfies them. A linear-time approximation raises cell counts minimally (instead of a quadratic program), then sampling follows "standard methods proposed from literature (e.g. [1])". The realization step took "less than a couple of seconds".
- **[documented]** Evaluation setup:
  - Data: TPC-H SF1 (uniform) and skewed sTPC-H (Zipf z=1.25).
  - Workload: TPC-H templates 1, 3, 6 and 10 with varied parameters, up to 4-way joins.
  - Privacy: ε = 1 and 0.1, δ = 0.01.
  - Metrics on PostgreSQL: optimizer **estimated cost** and actual **running time**, as relative error against the original database.
- **[documented]** Results:
  - All workload-aware models beat the Null Model. C2TM and C3TM are best without privacy.
  - At ε=1, the DP models show "very small" loss compared with non-private models.
  - At ε=0.1, "only C2TM can stay in sub-20% for both metrics". C3TM's extra noise "ruins the benefit of having more information".
  - Protecting only 90% of customers roughly halves C2TM perturbation error on sTPC-H.
  - Queries outside the workload: no-join and 2-way joins match the workload's utility. For more than 3 joins "the result becomes unpredictable", mainly because of model error.
  - Attributes not in the workload are random. The example given is customer age, generated uniformly between 1 and 100.
- **[documented]** Limitations the authors state:
  - DP "does not offer protection for the population". Where population aggregates such as revenue or customer counts are sensitive, "accurate and private database synthesis is likely to be impossible".
  - Only one protected entity is handled; multiple entities are future work.
  - The propagation constraint K is itself potentially sensitive.
  - Source: [Lu et al. 2014 PDF](https://people.cs.umass.edu/~miklau/assets/pubs/dp/lu2014generating.pdf)
- **[documented]** Code: neither PDF contains a code or repository link; the only URL is tpc.org. The publications page entry links only the PDF. — [Lu et al. 2014 PDF](https://people.cs.umass.edu/~miklau/assets/pubs/dp/lu2014generating.pdf); [Miklau publications](https://people.cs.umass.edu/~miklau/publications.html)

**Related Miklau-group work (leads unless stated)**
- **[documented]** Miklau's homepage (2026) describes him as Adjunct Professor at UMass and Principal Staff Software Engineer at LinkedIn, and as co-founder of Tumult Labs. Tumult Analytics/Core moved to OpenDP in October 2025.
  - It highlights DP synthetic data via graphical models, specifically PGM and **AIM**, "one of the leading approaches to differentially private synthetic data generation", and NIST challenge winners. — [Miklau homepage](https://people.cs.umass.edu/~miklau/)
- **[lead]** PrivateSQL (Kotsogiannis, Tao, He, …, Hay, Miklau; PVLDB 12(11), 2019) cites Lu et al. per OpenAlex and Semantic Scholar. It is a DP SQL engine over multi-relation databases built on precomputed private synopses, a related but different goal (answer accuracy). I did not read it. — [OpenAlex citing list](https://api.openalex.org/works?filter=cites:W2028628865)

### Inferences
- **[inferred]** The external report's citation is a conflation: its title wording, the AMW 2011 year, and the umass.edu host. The substance it attributes ("explicitly connects privacy-preserving database synthesis with application workload fidelity") fits both Miklau papers.
- **[inferred]** Fit to the brief's protection boundary is strong at the architecture level:
  - Computation inside, and only DP statistics plus an obfuscated schema and workload leave.
  - The generator outside never touches records.
  - The utility criterion is performance and plan fidelity on a given workload.

  Limits for the brief:
  - Statistics are tied to a known SQL workload, and attributes outside it are random.
  - Only key/FK joins, acyclic schemas and a single protected entity are handled.
  - No correctness-testing notion (edge cases, value formats, invalid data).
  - No maintained code.
- **[inferred]** The paper's warning that DP does not protect population aggregates matters for a platform whose table sizes or volumes may themselves be confidential (for example, business volumes).

### Gaps
- I did not retrieve the IEEE Xplore landing page. Venue and pages rest on OpenAlex metadata plus the author PDF.
- Exact per-model error numbers in Fig. 9 to Fig. 11 are in charts that pdftotext did not extract, so only the textual statements are reported.
- Wu et al. (2007 and the companion paper) were not read. Their method is known only through Lu et al.'s description.

---

## 2. Citation chain of Lu et al. 2014 (and Gupta et al. 2011)

### Takeaway
The chain is small (OpenAlex: 27 citing works for ICDE 2014, 8 for AMW 2011). It leads mostly into **DP relational synthesis** (PrivLava 2023, IRG 2026, DataSynthesizer) and **DP SQL engines** (Flex 2018, PrivateSQL 2019), not into workload-aware test-database generation.

The main workload-aware generators already documented in this repository, **Touchstone (2018) and SAM (2022), do not cite it** (full-text check). I found **no follow-up that extends *private* workload-aware generation for system testing**. Lu et al. remain the main DP-for-performance-testing precedent in this chain.

Maintained code exists only for the DP-synthesis follow-ups: PrivLava (Apache-2.0) and IRG (no licence file).

### Cited Findings

**Citing works**
- **[lead]** OpenAlex `cites:W2028628865` returns 27 works (26 were listed). Semantic Scholar returns 21. The relevant ones, classified:

| Work | Year/venue | Class | Cites Lu as | Status |
|---|---|---|---|---|
| PrivLava (Cai, Xiao, Cormode) | Proc. ACM Manag. Data (SIGMOD) 2023 | DP relational synthesis (FK-aware) | "inapplicable": preserves query cost, not answers | **[documented]**, read in full |
| IRG (Li et al.) | KDD 2026 (arXiv 2312.15187v4) | Relational synthesis, general purpose, not DP | "[37] integrates differential privacy into RDB generation" | **[documented]**, abstract and related work read |
| Flex / "Towards practical DP for SQL queries" (Johnson, Near, Song) | PVLDB 2018 | DP SQL query engine | performance-similar data, "do not propose a mechanism for answering queries" | **[documented]**, citation context read |
| PrivateSQL (Kotsogiannis et al., incl. Miklau) | PVLDB 2019 | DP SQL engine via private synopses | — | **[lead]** |
| DataSynthesizer (Ping, Stoyanovich, Howe) | SSDBM 2017 | DP single-table synthesis | — | **[lead]**. Already documented in this repo (MIT, Pre-Alpha) |
| Dscaler (Zhang, Tay) | PVLDB 2016 | Workload-agnostic DB scaling for testing | — | **[lead]**. Also cites AMW 2011 |
| ReX (Buda et al.) | Information Systems 2017 | DB extrapolation | — | **[lead]** |
| "Reversing statistics for scalable test databases generation" (Shen, Antova; NCSU / Pivotal) | DBTest 2013 (published 2013-06-24) | Test DB generation from optimizer statistics, no real rows | cites AMW 2011 | **[lead]**, not read |
| "Towards a Benchmark for Learned Systems" | ICDE Workshops 2021 | Benchmarking | cites AMW 2011 | **[lead]** |
| Differential Privacy for Databases (survey) | Foundations and Trends in Databases 2021 | Survey | — | **[lead]** |

- Sources:
  - [OpenAlex cites:W2028628865](https://api.openalex.org/works?filter=cites:W2028628865) (queried 2026-11-26)
  - [OpenAlex cites:W2405382494](https://api.openalex.org/works?filter=cites:W2405382494)
  - [Semantic Scholar citations](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICDE.2014.6816689/citations)
  - [OpenAlex, Reversing statistics](https://api.openalex.org/works/doi:10.1145/2479440.2479445)

**Workload-aware generators that do not cite it**
- **[documented]** The full texts of Touchstone (USENIX ATC 2018) and SAM (SIGMOD 2022 camera-ready) contain no reference to Lu/Miklau (grep of the extracted texts, which include their reference lists). This is evidence of absence for these two papers only.
  - Hydra, Mirage and DBRepro were not checked.
  - Sources: [Touchstone PDF](https://www.usenix.org/system/files/conference/atc18/atc18-li-yuming.pdf); [SAM PDF](https://jamesyang2333.github.io/files/SAM_Camera_Ready_v1.pdf)

**PrivLava, read in full**
- **[documented]** Claims to be "the first DP solution for synthesizing relational data with foreign key constraints".
  - It models each FK with graphical models plus a latent variable, for example a household "type" Z that drives household attributes, household size and members.
  - It supports FK DAGs and a mix of public and private relations.
  - Neighbouring databases remove one primary-private tuple plus all dependent tuples. FK multiplicity is bounded by τ; in the experiments τ is set to the 99% quantile of group sizes.
- **[documented]** Utility is the **accuracy of aggregate queries**, not performance:
  - Census data (California and Île-de-France, household × person) with 10,000 random counting queries.
  - A revised TPC-H, with injected inter-relational correlations, about 4×10⁶ lineitems and 1×10⁶ orders, and 8 TPC-H aggregate queries.
  - PrivLava beats PrivMRF, PrivBayes, PB-PGM and a denormalisation baseline. Accuracy degrades at small ε for low-selectivity queries (Q17 depends on 0.01% of lineitems).
  - It processes a large benchmark "in a matter of hours".
- **[documented]** On Lu et al.: they "preserve the costs of queries in Q, instead of the accuracy of the query results. Therefore, the solution in [30] is inapplicable in our setting."
  - Source: [PrivLava arXiv 2304.04545](https://arxiv.org/pdf/2304.04545)
- **[lead]** Code: GitHub search finds `caicre/PrivLava`, Apache-2.0, last pushed 2025-12-31. Repository metadata only; I did not clone or inspect it. — GitHub search API, queried 2026-11-26

**IRG**
- **[documented]** IRG ("incremental relational generator") handles composite keys, sequential correlation and indirectly connected tables with modular generative and predictive models. It names software testing at various scales as a use case.
  - It is general-purpose and does **not** provide DP. It cites Lu et al. and ezGen as "specialized works" excluded from baselines.
  - Code: github.com/li-jiayu-ljy/irg.
  - Source: [IRG arXiv 2312.15187v4, 14 Dec 2025](https://arxiv.org/pdf/2312.15187)
- **[documented]** Repository clone (2026-11-26): last commit 2026-02-18 ("Update synthesizer.py"). It has Makefile, main.py, baselines, datasets and requirements.txt, and **no LICENSE file** at the root, which implies no open-source grant.

**Flex**
- **[documented]** Flex characterises Lu et al. as "generating differentially private synthetic data such that queries with joins have similar performance characteristics, but not necessarily similar answers". — [arXiv 1706.09479](https://arxiv.org/pdf/1706.09479)

### Inferences
- **[inferred]** The descendants divide by goal:
  - The DB-systems testing community (Touchstone, SAM, Hydra) took up workload-aware cardinality constraints from Arasu et al. and QAGen, mostly without a formal privacy layer.
  - The DP community took up multi-relation DP and synthesis for answer accuracy (PrivLava, PrivateSQL, Flex).

  No work in this chain combines DP release with performance and plan-fidelity generation for testing, so Lu et al. 2014 is still the closest such combination found.
- **[inferred]** For a design, the combination is buildable from parts: Lu et al.'s privacy layer (multi-table DP with FK-bounded sensitivity) applied to the cardinality constraints that Touchstone or SAM consume. The gap lies in this integration, not in a missing component.

### Gaps
- The full texts of Dscaler, ReX, Reversing statistics (DBTest 2013, ACM DL) and PrivateSQL were not read. The ACM DL was not attempted, given its known Cloudflare blocking.
- Hydra, Mirage and DBRepro were not checked for citations of Lu et al.
- Google Scholar was not used, so its citation count, typically higher, is unknown.
- PrivLava's repository contents (runnable state, README) were not inspected.

---

## 3. NHS England Artificial Data Pilot / Artificial Data Generator

### Takeaway
The official page, read in full via a mirror, and the code, read via a public copy of the repository (MIT, © 2022 NHS Digital), confirm the architecture:
1. A metadata scraper builds column-by-column frequency tables inside the protected Databricks/DAE scope.
2. Small-number suppression (<5) and rounding to 5 are applied.
3. A manual review follows, using a checklist approved by the Statistical Disclosure Control Panel and signed off by a senior manager.
4. The reviewed metadata is moved to a scope the generator can read.
5. The generator samples each field independently and post-processes (date ordering, dummy IDs).

Three artificial HES datasets were published (A&E, APC and Outpatient; files dated February 2023), each as a 10,000-row sample and a 1-million-row full file.

The official NHSDigital GitHub repository no longer answers anonymous clones. The code's last commit was 2023-05-26, so it is unmaintained.

A nuance the external report misses: the code also releases **patient→episode cardinality distributions** and **per-patient demographic value-pattern distributions**. So "no relationships preserved" holds for relationships between fields, not for all structure.

### Cited Findings

**Official page: "Artificial data pilot – NHS England Digital"**

The page reads "Last edited: 20 August 2026". digital.nhs.uk returned 403 directly. The text was read from `nhsd-proxy.openprescribing.net`, a proxy mirror of digital.nhs.uk run by OpenPrescribing (Bennett Institute), so provenance is a third-party mirror of the official page. The Wayback Machine snapshot (2026-07-19) exists, but fetching it failed with a connection reset. — [mirror of digital.nhs.uk/services/artificial-data](https://nhsd-proxy.openprescribing.net/services/artificial-data); original URL [digital.nhs.uk/services/artificial-data](https://digital.nhs.uk/services/artificial-data) **[unreachable directly]**

- **[documented]** "We are piloting this new service with a limited number of artificial data sets."
  - Purpose: to help users understand "columns, data types and approximate value ranges".
  - "…can be used to improve understanding of data sets and data platforms, and for building and testing data pipelines, they cannot be used to analyse data."
  - Benefits include: "Users can develop and test code prior to accessing real data".
- **[documented]** "This artificial data represents the formatting, structure and volume of the original data set. It does not preserve relationships between fields".
  - Also: "Statistical relationships between columns are not preserved … Most records generated in such a way would be unrealistic", for example a geriatrics department with age 5.
- **[documented]** "There are currently 3 artificial data sets available from Hospital Episode Statistics (HES)." "A sample data set contains 10,000 rows and a full data set contains a million rows."
  - Files: A&E sample 24.3 MB / full 2.4 GB; APC sample 43.9 MB / full 4.3 GB; OP sample 28.5 MB / full 2.8 GB.
  - File names are `artificial_hes_{ae,apc,op}_202302_v1_{sample,full}.zip`.
- **[documented]** Process:
  - Two steps: a "metadata scraper" creates "a national level, aggregated, anonymous summary". The "data generator" randomly samples from it.
  - "Between these 2 steps, the anonymous aggregates are reviewed and signed-off via a process agreed with our chief statistician and Statistical Disclosure Control Panel".
  - The diagram text: each real-data scope holds a single dataset, and "Aggregate data is blocked from exiting the scope where it was created if the checks are not passed."
- **[documented]** Aggregation:
  - "aggregated on a column-by-column basis … frequency tables of unique values in each column. … key identifiers (such as patient ID) are removed and small numbers are suppressed".
  - Example: the aggregates allow "the number of female patients or the number of 49-year-old patients … but not the number of 49-year-old females."
  - Generation: "sampling from anonymous univariate frequency distributions".
- **[documented]** Post-processing: "randomly generated birth and death dates may be swapped to ensure sensible ordering". Then "randomly generated dummy values for identifying fields (such as 'patient' ID')… based on template patterns structured to ensure unrealistic values with the correct properties (for example, data type and length)."
- **[documented]** Legal framing: "Records in artificial data relate to fictitious patients, so do not constitute personal data under UK GDPR." The page links "the code" to `https://github.com/NHSDigital/artificial-data-generator`.
- **[documented]** HES user notice (496 bytes, same mirror): artificial HES "is unsuitable for testing HES developments and cannot be used for HES assurance purposes", and "there are differences in the aggregate statistics between artificial HES and real HES." — [artificial_hes_user_notice.txt (mirror)](https://nhsd-proxy.openprescribing.net/binaries/content/assets/website-assets/services/artificial-data/artificial_hes_user_notice.txt)
- **[documented]** The data files are still served. A HEAD request for the OP sample zip returned 200, Content-Length 29,920,912, Last-Modified "Tue, 07 Feb 2023 09:13:00 GMT". — [OP sample zip](https://files.digital.nhs.uk/assets/Services/Artificial%20data/Artificial%20HES%20final/artificial_hes_op_202302_v1_sample.zip)

**Repository**
- **[unreachable]** `git ls-remote` of `github.com/NHSDigital/artificial-data-generator` and `NHSDigital/artificial-data-plug-and-play` asks for credentials, which GitHub does for private, renamed or deleted repositories. Public repositories (for example ns-rse's) clone without credentials. Whether the original was deleted or made private cannot be determined.
- **[lead]** GitHub search lists several forks with `pushed_at` 2023-05-26, including `nhsfork/artificial-data-generator`, created as a fork on 2026-05-05. This suggests the upstream was still forkable in May 2026.
  - `ns-rse/artificial-data-generator` is MIT, with description "Pipelines for generating large volumes of anonymous artificial data that share some of the characteristics of real NHS data".
  - `uk-gov-mirror/nhsdigital.artificial-data-plug-and-play` is MIT, pushed 2023-08-25.
  - Source: GitHub search API, 2026-11-26
- **[documented]** Clone of `ns-rse/artificial-data-generator` (2026-11-26):
  - 5 commits, by Alistair Jones, from 2022-10-04 ("Initial commit") to **2023-05-26** ("Update README.md").
  - LICENSE: "MIT License, Copyright (c) 2022 NHS Digital". The README says documentation is © Crown copyright under OGL v3.
  - README: "maintained by the NHS Digital Data Science team". It runs as Databricks notebooks on **Databricks Runtime 6.6**. "We have plans to pull out the core logic into a Python package… we're not there yet!"
  - Source: [ns-rse/artificial-data-generator README](https://raw.githubusercontent.com/ns-rse/artificial-data-generator/main/README.md)
- **[documented]** Isolation design (README and docs/artificial_data_admin_guide.md):
  - Separate "Code Promotion" jobs: `artificial_hes_meta` (scrape), `iuod_artificial_data_admin` (moves reviewed metadata "from the sensitive to non-sensitive scope after review and sign-off") and `iuod_artificial_data_generator`.
  - "It is not possible for the pipelines that generate artificial data to read from any sensitive data."
  - "Approved human users will only have access to access aggregates for review, not to the underlying record-level data."
  - Review is against "a checklist that was approved by the Statistical Disclosure Control Panel, chaired by the Chief Statistician", with outcomes "signed-off by a senior manager".
  - docs/artificial_data_user_notice.md adds: "It is crucial to note that artificial data is not synthetic data". It also states approval by the SIRO, Caldicott Guardian, DPO and dataset IAOs, and that "A full DPIA has been completed and is available upon request."
- **[documented]** Disclosure parameters in code (`scraper_pipelines/hes/constants/disclosure_control_parameters.py`): `HES_FREQUENCY_ROUNDING = 5`, `HES_MIN_FREQUENCY = 5`.
  - In `aggregation_parameters.py`, a value is dropped if its *actual* count is below 5. The comment reads: "Using rounded weights could let potentially disclosive values through!" Surviving counts are rounded to the nearest 5.
  - This applies to categorical, discrete and date frequencies.
  - Continuous fields are released as the approximate 2nd–99th percentiles (min/max excluded), with no count suppression in that function.
- **[documented]** Fields excluded from scraping (`excluded_fields.py`):
  - ID fields: PSEUDO_HESID, SUSRECID, AEKEY, EPIKEY, ATTENDNO, ATTENDKEY, ATTENDID and PREFERER.
  - Derived fields: DIAG_3_*, OPERTN_3_*, the concat and count fields, and STARTAGE. These are regenerated by derivation after generation (`with_derived_fields`).
- **[documented]** Structure beyond univariate frequencies, in code:
  - (a) `relationship_summariser.py` releases the "frequency distributions of cardinal relationships between primary key and foreign key", meaning how many episodes per patient. The generator's `relationship_generator` uses it to create patient→episode IDs. This second-stage aggregation has no rounding or minimum-frequency filter in code, so it relies on manual review **[inferred from code]**.
  - (b) `demographic_field_summarisers.py` releases, for sex, ethnicity and date of birth, the distribution of per-patient value patterns across visits, so that "the patterns of 'errors' that we would see in real data are represented". Rounding and minimum frequency of 5 apply.
  - (c) Post-processing orders APC dates (ELECDATE, ADMIDATE, EPISTART, EPIEND, DISDATE).
  - The default generator parameter is `n_patients: 100`. The 10k and 1M sizes are not in code.
  - Source: [ns-rse/artificial-data-generator](https://raw.githubusercontent.com/ns-rse/artificial-data-generator/main/README.md) (files read locally)

### Inferences
- **[inferred]** For the brief, this is a well-documented governance pattern:
  - one dataset per scope;
  - aggregates only;
  - small-number suppression plus rounding;
  - human SDC checklist review and sign-off;
  - a physical scope move;
  - a generator that cannot read source data;
  - an explicit user notice of limitations.

  Its statistical model, though, is near the "dummy data" end of the spectrum. Stated by NHS itself, it is unsuitable for testing HES developments or for assurance, and aggregates differ from real HES. It answers "structure, types, value ranges, volume" testing, not performance or relationship-dependent correctness testing.
- **[inferred]** The patient→episode cardinality and the per-patient inconsistency patterns show that NHS did release limited *relational* aggregates (join fan-out, recording-error patterns) under the same review. This is a precedent that fan-out histograms can pass an SDC review, which is the same statistic Lu et al.'s FK model and Touchstone's join constraints need.
- **[inferred]** The code has been effectively frozen since May 2023 and is tied to Databricks Runtime 6.6 notebooks (Spark 2.4-era). The official repository link on the live page is dead for anonymous access, so reuse would mean forking an archived copy.

### Gaps
- I could not read the official page directly or through the Wayback Machine (connection reset) or the UK Government Web Archive (405/403). The text rests on the OpenPrescribing proxy mirror, whose "Last edited: 20 August 2026" matches a live page.
- The SDC checklist itself was not found. The DPIA is "available upon request", not published.
- Whether more datasets were added after HES is unknown. The page still says "3 artificial data sets" as of August 2026.
- I did not verify that `ns-rse` is byte-identical to the upstream. The matching last-commit date with the true forks and the NHS Digital copyright support it **[inferred]**.
- The released zip contents (actual row counts and columns) were not downloaded or inspected.

---

## 4. Verdicts on the external report's claims, and comparison with precedents already in the repo

### Takeaway
On the NHS pilot, the external report is accurate in substance. Its one omission is the limited relational aggregates (patient→episode fan-out), and it misreports maintenance only mildly ("unconfirmed"; in fact dormant since 2023-05 with the repository now unreachable). On Lu/Miklau/Gupta, its bibliographic details are wrong but the characterisation is right.

Against Simulacrum, OpenSAFELY and IAB-FDZ:
- The NHS generator sits between OpenSAFELY (schema-only dummy data) and Simulacrum (reviewed multi-dimensional cubes of at least 50 patients). It shares Simulacrum's "aggregate inside, reviewed, sample outside" shape but has much lower dimensionality.
- Lu et al. adds what none of the healthcare precedents offer: a formal (DP) guarantee and a workload- and performance-fidelity target.

### Cited Findings

**Claim verdicts**

| # | External-report claim | Verdict | Evidence |
|---|---|---|---|
| 1 | "Generating Private Synthetic Databases for Database Application Testing, 2011", people.cs.umass.edu | **Partially confirmed** (title wrong, year conflated) | The real titles are "Private Database Synthesis for Outsourced System Evaluation" (AMW 2011) and "Generating Private Synthetic Databases for Untrusted System Evaluation" (ICDE 2014). The "…Database Application Testing" wording is Wu et al. 2007 (non-DP). [documented] [Miklau publications](https://people.cs.umass.edu/~miklau/publications.html) |
| 2 | "Research dating back to 2011 explicitly treats query cardinalities, execution plans, resource consumption and execution time as measures of synthetic database utility" | **Confirmed** for 2011 as *candidate* metrics. The 2011 experiment measured cardinality only; the 2014 paper measured estimated cost and running time | AMW 2011 §2.5 lists cardinality, estimated/actual time or IOs, plans and index usage. [documented] [Gupta 2011](https://people.cs.umass.edu/~miklau/assets/pubs/dp/Gupta11Private.pdf); [Lu 2014](https://people.cs.umass.edu/~miklau/assets/pubs/dp/lu2014generating.pdf) |
| 3 | "Explicitly connects privacy-preserving database synthesis with application workload fidelity" | **Confirmed** | Workload-derived counting queries under multi-relation DP. [documented] [Lu 2014](https://people.cs.umass.edu/~miklau/assets/pubs/dp/lu2014generating.pdf) |
| 4 | NHS: production-data aggregation step | **Confirmed** | Metadata scraper, column by column, in the real-data scope. [documented] [page mirror](https://nhsd-proxy.openprescribing.net/services/artificial-data) |
| 5 | NHS: formal disclosure review | **Confirmed** | Review and sign-off via a process agreed with the Chief Statistician and the SDC Panel; checklist; senior-manager sign-off. [documented] page and repo |
| 6 | NHS: separate generation step without access to real records | **Confirmed** (vendor self-description backed by code structure) | "It is not possible for the pipelines that generate artificial data to read from any sensitive data"; separate Code Promotion job scopes. [documented, vendor] repo README |
| 7 | NHS: explicitly supports building and testing data pipelines | **Confirmed** | "for building and testing data pipelines". [documented] page |
| 8 | 10,000-row samples and million-row datasets | **Confirmed** | "A sample data set contains 10,000 rows and a full data set contains a million rows." [documented] page |
| 9 | Independently sampled frequency distributions | **Confirmed**, with a nuance | "univariate frequency distributions"; continuous fields use percentiles; patient→episode fan-out and per-patient demographic patterns are also sampled. [documented] page and code |
| 10 | Basic post-processing and dummy identifiers | **Confirmed** | Date-order swaps; template-pattern dummy IDs "to ensure unrealistic values". [documented] page |
| 11 | NHS explicitly acknowledges relationships between fields are not preserved; deliberate | **Confirmed** | "It does not preserve relationships between fields"; the README says "excluding cross-dependencies between fields to prevent risks of reidentification". [documented] |
| 12 | "MIT-licensed reference implementation; pilot, current code maintenance unconfirmed" | **Confirmed / sharpened** | MIT © 2022 NHS Digital; last commit 2023-05-26; the official repository is now not anonymously reachable; still labelled "pilot" in August 2026. [documented] clone of a public copy; [lead] fork metadata |
| 13 | "Real rows needed only for profiling. Approved distributions leave." | **Confirmed** | As 4–6. [documented] |
| 14 | "Its architecture is instead substantiated by the official NHS methodology" (repository retrieval failed) | **Confirmed**; the code is now also verified | This run read both the page (mirror) and the code (public copy). |

**Comparison with precedents already documented** (from `research_notes/Synthetic stand in test data/neighbouring_fields.md`, read only)
- **[documented, prior run]** Simulacrum:
  - Aggregation inside into "data cubes based on at least 50 patient records", which were judged safe and released; synthetic records are sampled from the cubes.
  - The schema is identical to the Cancer Analysis System, with a code-submission loop and ISB output checking.
  - Source: [Simulacrum method page](https://simulacrum.healthdatainsight.org.uk/?p=3940), as recorded in neighbouring_fields.md
- **[documented, prior run]** OpenSAFELY: dummy data from the dataset definition alone. No real-data statistics leave for dummy generation. — [OpenSAFELY dummy data how-to](https://docs.opensafely.org/ehrql/how-to/dummy-data/)
- **[documented, prior run]** IAB-FDZ test data: built from real rows by sampling, swapping and micro-aggregation. That would breach an aggregates-only rule. — [IAB Hilfe_Testdaten_e.pdf](https://doku.iab.de/fdz/ba/Hilfe_Testdaten_e.pdf)

### Inferences
- **[inferred]** Ranking on the brief's two axes, protection boundary and behavioural fidelity:

| Precedent | What leaves the protected side | Formal guarantee | Fidelity target | Joint / relational structure | Maintained code |
|---|---|---|---|---|---|
| OpenSAFELY dummy data | Nothing (schema/definition only) | n/a | Code runs unchanged | Only what the definition implies | Yes (prior run) |
| NHS Artificial Data | Univariate frequencies (<5 suppressed, rounded to 5), percentiles, patient→episode fan-out, demographic patterns; SDC-reviewed | No (rule-based SDC plus manual review) | Structure, types, ranges, volume; pipeline building | Fan-out only; no cross-field | No (frozen 2023-05) |
| Simulacrum | Multi-dimensional cubes (≥50 patients); reviewed and released | No (threshold plus ISB review) | Query-writing and feasibility; schema parity | Within-cube joint distributions | Data releases to 2023 (prior run) |
| Lu/Miklau/Gupta 2014 | DP answers to workload-derived counting queries (incl. join cardinalities), plus obfuscated schema and workload | Yes: (ε, δ)-DP per protected entity, FK-bounded | Query cost, plans, running time for a given workload | Up to i-way join cardinalities on workload predicates | No public code |
| IAB-FDZ test files | Perturbed real rows | No | Code testing | Partial | n/a |

- **[inferred]** For the brief, the NHS pilot is the best *operational and governance* precedent:
  - per-dataset scopes, a reviewed hand-off of aggregates, and a generator that cannot read source data;
  - explicit limitation notices;
  - published 10k and 1M sizes for development and volume testing.

  Lu et al. is the best *methodological* precedent for "behaves like real data for performance testing", with a formal guarantee. Neither covers cross-source entity semantics or correctness edge cases. Combining NHS-style governance with Lu-style DP workload statistics, fed to a Touchstone or SAM-style generator, is a design inference, not a documented system.
- **[inferred]** The NHS's own "unsuitable for testing HES developments" caveat is direct evidence that independent-marginal generation is too weak for testing the data platform's own transformations. This matches the external report's "statistical model is insufficient" judgement.

### Gaps
- No source reports any organisation adopting Lu et al.'s method in production. That is absence of evidence: I searched only the citation graph.
- I did not check whether NHS England has a successor service (for example within the NHS England Secure Data Environment) that replaced the pilot. The page was still live in August 2026.
