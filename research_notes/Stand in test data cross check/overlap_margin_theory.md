# What released overlap and margin counts imply about, and disclose about, the cross-source presence table; status of relational DP synthesis (DPSynth, JMLR 2026)

Labels: **[documented]** = full text, or the primary file or repo itself, was read. **[documented: abstract]** = only the abstract or landing page was read. **[lead]** = search extract only. **[inferred]** = my reasoning from documented items. **[theoretical]** = a mathematical result, proven in the cited paper or checked by me through enumeration. **[unreachable]** = could not be retrieved. Retrieval date for all items: 2026-11-26.

Scratch scripts (not in the repo): `/tmp/claude-0/-home-user-research/ff1944a8-a88f-543f-abeb-c6de43b3e2ac/scratchpad/p3c_scripts/overlap.py`, `.../p3c_scripts/k4.py` and `.../p3c_scripts/k4b.py`. All were run with `python3 -I`.

## Q1. Non-identifiability: do pairwise overlaps of k ≥ 3 sources determine higher-order overlaps?

### Takeaway
The external report's example is arithmetically correct. Three sources of 100 each, with every pair sharing 50, are consistent with any triple overlap t from 0 to 50 and a union of 150 + t, so a union of 150 (t = 0) and a union of 200 (t = 50) are both possible.

There is one caveat the report omits. For k = 3, if the total number of distinct entities (the union) is released too, inclusion–exclusion fixes the triple overlap. Non-identifiability given sizes, pairs **and** union starts at k = 4.

The general object is the 2^k presence/absence contingency table: 2^k − 1 observable cells, plus the "dark" all-absent cell. Released source sizes and intersections are linear functions of it (its margins). They constrain the table without determining it, except when sparsity forces a unique solution.

### Cited Findings
- **Worked example, k = 3 [theoretical; checked by me].**
  - Population 1 has cells {AB-only 50, AC-only 50, BC-only 50}.
  - Population 2 has cells {ABC 50, A-only 50, B-only 50, C-only 50}.
  - Both give sizes (100, 100, 100) and pairwise intersections (50, 50, 50).
  - Their triples are 0 and 50, and their unions are 150 and 200.
  - Inclusion–exclusion gives 300 − 150 + 0 = 150 and 300 − 150 + 50 = 200, which matches a direct count.
  - The full feasible family is triple = t, pair-only cells = 50 − t, single-only cells = t, for t = 0…50, with union = 150 + t.
  - The Fréchet-type bounds on the triple given sizes and pairs are max(0, n12 + n13 − n1, …) = 0 ≤ t ≤ min(n12, n13, n23) = 50. Enumeration confirms this range.
  - Source: my script `p3c_scripts/overlap.py` (output: "pop1 … triple 0 union 150 IE 150"; "pop2 … triple 50 union 200 IE 200"; "feasible t range 0 50").
- **The same data are the standard MSE data structure [documented].**
  - "if t = 4 the capture history {1, 3} … N13, is the number of individuals which are observed on both lists 1 and 3 but not on lists 2 or 4 … N∅ is the dark figure of individuals which are not captured on any list, and therefore cannot be observed. The observed data give rise to the 2^t − 1 values {Nω : ω ≠ ∅}".
  - The intersection counts N*ω are defined as sums of the cells Nψ over ψ ⊇ ω. These are exactly the "pairwise overlap" quantities a release would contain, so the released overlap counts are linear functions (margins) of the 2^t table.
  - Source: [Chan, Silverman & Vincent, "Multiple Systems Estimation for Sparse Capture Data: Inferential Challenges when there are Non-Overlapping Lists", arXiv:1902.05156v4, 14 Dec 2019 (JASA 2021)](https://arxiv.org/abs/1902.05156).
- **Rcapture uses the same data structure [documented].** "With t capture occasions of the experiment, 2^t − 1 capture histories ω are observable", and ω0 is "the unobservable capture history of zero capture". — [Baillargeon & Rivest, "Rcapture: Loglinear Models for Capture-Recapture in R", JSS 19(5), April 2007](https://www.jstatsoft.org/article/view/v019i05)
- **k = 4: sizes, pairs and union still do not determine the table [theoretical; checked by me].**
  - Setup: 4 sources, each of size 32; all 6 pairwise intersections equal 14; union 65.
  - Exhaustive integer enumeration finds **1,662** distinct presence tables consistent with these numbers.
  - The 4-way intersection ranges over 0–7, and each "exactly three sources" cell ranges over 0–10.
  - Reason: there are C(4,3) + C(4,4) = 5 unknown higher-order cells and only one extra equation (the union).
  - In general, sizes, pairs and union leave 2^k − 1 − k − C(k,2) − 1 linear degrees of freedom. That is 0 for k = 3, 4 for k = 4 and 15 for k = 5.
  - Source: my script `p3c_scripts/k4b.py`.
- **Log-linear framing of the same point [documented].**
  - "there are 2^t parameters αθ … There are only 2^t − 1 observable data points … without placing constraints on the αθ parameters, the model is not identifiable."
  - The standard fix is to "set all coefficients indexed by third- or higher-order histories to zero". With all two-list terms the parameter count is 1 + t + ½t(t − 1) ≤ 2^t − 1 for t ≥ 3.
  - Higher-order structure is therefore *assumed*, not estimated.
  - Source: [Chan, Silverman & Vincent 2019, §2.2](https://arxiv.org/abs/1902.05156).

### Inferences
- **[inferred]** For a stand-in generator, releasing only source sizes and pairwise overlaps leaves the higher-order overlap (entities in 3+ sources) free. A generator calibrated to those numbers will pick one table from the feasible set: for example the maximum-entropy one, or the one implied by a pairwise log-linear model (the MSE no-higher-order-interaction assumption). Reconciliation and dedup workloads depend on how many entities sit in 3+ sources, so this choice matters for test fidelity.
- **[inferred]** Two cheap counts carry a lot of information for k = 3: the union and the triple. For k ≥ 4, reproducing higher-order overlap needs either the 2^k − 1 cell table or chosen higher-order margins.
- **[inferred]** Sources with their own identifiers, coverage and reporting delays make the presence table snapshot-dependent. An entity's pattern changes as delayed sources catch up. Each released table therefore has to be tied to an as-of date and a linkage version, and successive snapshots are a differencing risk (see Q4).

### Gaps
- I did not find a published source that states the "union pins k = 3" caveat in exactly these terms. It follows directly from inclusion–exclusion and is labelled theoretical (checked by me).

## Q2. Fréchet bounds and generalisations; disclosure auditing of released margins; tools

### Takeaway
Given a set of released margins, every cell of the full table has a sharp integer lower and upper bound. When the bounds are tight on a small cell, that cell is disclosed.

Closed forms exist in two cases:
- the margins are the sufficient statistics of a **decomposable** log-linear model: Dobra & Fienberg 2000, with upper bound = min over clique margins and lower bound = max(0, Σ clique margins − Σ separator margins);
- the table is a **dichotomous k-way table with all (k − 1)-way margins fixed** (Dobra–Karr–Sanil 2003). This is exactly the shape of a presence/absence table.

Otherwise the generalized shuttle algorithm, or integer or linear programming, is needed. LP bounds are valid but can be non-sharp or fractional.

Agency tools that compute such bounds are sdcTable's `attack()` (LP via HiGHS) and τ-Argus's audit (external LP solver). They audit suppression patterns, not arbitrary sets of released margins.

### Cited Findings
- **Dobra & Fienberg (2000), the paper and its disclosure framing [documented].**
  - Citation: Dobra & Fienberg, "Bounds for cell entries in contingency tables given marginal totals and decomposable graphs", *PNAS* 97(22):11885–11892, 24 Oct 2000, doi:10.1073/pnas.97.22.11885 ([PMC17264](https://pmc.ncbi.nlm.nih.gov/articles/PMC17264); NISS TR 108, Oct 2000, [PDF](https://www.niss.org/sites/default/files/technicalreports/tr108.pdf)).
  - Abstract: bounds "play important roles in a number of practical problems, including statistical disclosure limitation, computer tomography, mass transportation, cell suppression, and data swapping". Some features of the Fréchet bounds "are well known, intuitive, and regularly used by those working on disclosure limitation methods, especially those for two-dimensional tables". The paper "provides the actual theory and proofs for the special case of decomposable loglinear models", with an extension to reducible graphs.
  - Disclosure mechanism: "if a cell count is small and the upper bound is 'close' to the lower bound, the intruder knows with certainty that there is only a small number of individuals possessing the characteristics corresponding to the cell". The authors also note Fienberg's "intimate link" between these bounds and the MLE under the log-linear model whose minimal sufficient statistics are the margins.
- **Dobra & Fienberg (2000), sharpness and computation [documented].**
  - For connected decomposable graphs (Theorem 6), "these are sharp bounds for the cells in the contingency table n_K given the marginals".
  - Reducible graphs are handled by combining the bounds of the maximal prime subgraphs.
  - In non-decomposable cases "we have no choice but to employ iterative methods such as the simplex algorithm". The general problem is described as typically NP-complete.
  - Buzzigoli & Giusti's "shuttle" algorithm "does not achieve the sharp bounds in as computationally efficient fashion as we can by using the formula directly".
  - The PMC text renders the formulas as images. I took the explicit formula from Dobra–Karr–Sanil, below.
  - Source: [PMC17264](https://pmc.ncbi.nlm.nih.gov/articles/PMC17264).
- **Dobra, Karr & Sanil (2003), the paper and the NISS systems [documented].**
  - Citation: Dobra, Karr & Sanil, "Preserving confidentiality of high-dimensional tabulated data: Statistical and computational issues", *Statistics and Computing* 13(4):363–370, 2003 (NISS TR 130, Nov 2002) ([author PDF](https://sites.stat.washington.edu/adobra/Files/Papers/ADstatcomp2003.pdf)).
  - It gives a "form of the shuttle algorithm that computes sharp bounds on (small, confidentiality threatening) cells in the full table from arbitrary sets of released marginals".
  - Context: many sub-tables are not releasable "because either on their own or in conjunction with other sub-tables they provide too much information about the full table. Often … 'too much information' means that small count (and therefore high risk …) cells can be bounded too accurately on the basis of the released sub-tables."
  - NISS built "table servers" (live) and "optimal tabular releases" (static sets of sub-tables chosen to maximise information subject to a risk limit).
- **Dobra, Karr & Sanil (2003), Theorem 1 and sharp cases [documented].**
  - Theorem 1, for decomposable models with cliques C1…Cp and separators S2…Sp:
    - sharp upper bound U(i) = min{ n_j(i_Cj) : j = 1…p };
    - sharp lower bound L(i) = max{ Σ_j n_j(i_Cj) − Σ_{j≥2} n_Sj(i_Sj), 0 }.
  - "when the fixed marginals define a decomposable graphical model, pairwise consistency of marginals implies the existence of a feasible table."
  - The shuttle bounds are always valid (the sharp bounds lie inside them) and are sharp in two cases: "dichotomous k-dimensional tables with all (k − 1)-dimensional marginals fixed, and when the fixed marginals are the minimal sufficient statistics of a decomposable log-linear model".
  - An extended procedure enumerates feasible integer tables and adjusts the shuttle bounds to sharp integer bounds.
- **Dobra, Karr & Sanil (2003), LP versus integer bounds [documented].** Example 2 (a 2×2×2×2 table with all six 2-way margins fixed):
  - "There is only one table consistent with this set of two-way marginals, so for all the cells … the sharp integer upper and lower bounds are equal to the actual cell entries."
  - The LP (simplex) bounds differ from the sharp integer bound for every cell. "In some cases, the simplex algorithm produced fractional bounds. In other cases … these bounds are not sharp."
- **sdcTable [documented].**
  - Status: version 0.34.1, published 2026-11-12, maintainer Bernhard Meindl ([CRAN sdcTable](https://cran.r-project.org/package=sdcTable)).
  - `attack()`: "compute lower and upper bounds for a given sdcProblem instance … the current suppression pattern is used when calculating solutions of the attacker's problem". It returns `low`, `up` and `protected` (TRUE if `up − low` exceeds a threshold, default 1e-8).
  - It solves the attacker problems with the `highs` LP solver (`highs::highs_solver`, minimise and maximise), per the source `R/attack.R` in sdcTable_0.34.1.tar.gz.
- **sdcTable, LP relaxation [inferred].** grep found no integrality setting in `attack.R`, so these are continuous LP bounds. Per Dobra–Karr–Sanil, such bounds can be wider than the sharp integer bounds, which means they can understate disclosure.
- **τ-Argus [documented].** "an audit procedure is available to check quality of any secondary suppression pattern". "Some methods for secondary suppression (the modular and the optimal), but also the audit procedure require an external linear programming solver" (Xpress, CPLEX or the free SoPlex). — [τ-Argus manual, "A tour of τ-Argus" (Quarto conversion)](https://julienjamme.github.io/manual_tau_argus_to_quarto/03_A_tour_of_tauargus.html)
- **Two-set Fréchet bound applied to sources [theoretical; standard inequality, checked by me in `overlap.py` for the triple].** For sources i and j within a known universe U: max(0, n_i + n_j − U) ≤ n_ij ≤ min(n_i, n_j). For the triple given pairs: max(0, n_ij + n_ik − n_i over all i) ≤ n_ijk ≤ min(n_ij, n_ik, n_jk).

### Inferences
- **[inferred] A presence/absence table is the favourable case for exact auditing.**
  - It is dichotomous, so Dobra–Karr–Sanil's sharp-shuttle result applies when all (k − 1)-way margins are released.
  - If the released margins form a decomposable model (for example a chain or tree of pairwise overlaps A–B, B–C, C–D with their separators), Theorem 1 gives closed-form sharp bounds for every cell.
  - Example: releasing only the A∩B, B∩C and C∩D tables gives a decomposable chain.
  - Releasing **all** pairwise margins for k ≥ 3 is non-decomposable (a cycle), so it needs the shuttle algorithm, IP or enumeration. For k ≤ ~10 the 2^k cells are few enough to enumerate or solve exactly.
- **[inferred] An audit procedure for any proposed overlap release.** Before release:
  1. compute sharp integer bounds for every cell of the 2^k presence table, given the full set of overlap and coverage counts to be released (including earlier releases);
  2. flag any cell whose bounds pin a count below the threshold (for example 1–9), or pin 0 next to a small positive margin.
  - Off-the-shelf sdcTable and τ-Argus audit *suppression patterns* using LP. They are not designed to audit an arbitrary set of intersection counts and give LP (possibly non-sharp) bounds. A small purpose-built integer check is likely needed (exhaustive enumeration as in `k4.py` for small k; an IP solver otherwise).
- **[inferred] Sparse data are the dangerous case.** In my sparse k = 4 example (`p3c_scripts/k4.py`: sizes 10 each; pairs 5, 3, 2, 2, 3, 5; union 26), exactly **one** integer table is consistent with the released sizes, pairs and union. Every cell is disclosed, including "exactly in sources 1 and 3: 1 entity" and "in all four: 2". The released counts look aggregate, but the zeros force the solution.

### Gaps
- Fienberg & Slavković on tables with fixed margins and integer programming: I did not retrieve a full text in this track **[gap]**.
- Dobra 2001/2002/2003 (thesis; Bernoulli 2003 Markov bases; NISS TR 116, Jan 2001) were seen only as search extracts **[lead]**: [NISS TR116](https://www.niss.org/sites/default/files/technicalreports/tr116.pdf).
- I found no maintained standalone "bounds" package that implements the generalized shuttle algorithm. None was located; this is not proof that none exists.
- I did not find which agencies currently run sharp-bound audits on released *overlap* tables specifically. The NISS table-server work, ca. 2002–2003, is the documented precedent.

## Q3. Capture–recapture / multiple-systems estimation as the model of several sources observing the same entities

### Takeaway
MSE is the established statistical model for "k sources with different coverage observing overlapping entities". It fits a Poisson log-linear model to the 2^k − 1 observed presence cells. It must assume the highest-order interactions are zero (identifiability), and it models dependence between sources with two-list terms.

The sufficient statistics of the pairwise model are the source sizes, the pairwise intersections and the observed total. That is a principled answer to "which margins to release": exactly the margins a pairwise log-linear model needs, accepting that higher-order overlap is then model-implied.

On maintenance: Rcapture (2022), SparseMSE (2019) and LCMCR (2023) are on CRAN, but none has had a release in the last ~3 years.

### Cited Findings
- **Model form [documented].**
  - "Nω ∼ Poisson(μω) with log μω = Σ_{θ⊆ω} αθ". "the estimate of the total population size will be N*∅ + exp α̂∅".
  - Highest-order terms are set to zero. "Model choice then reduces to deciding which two-list coefficients to include."
  - Sparse or absent overlaps cause trouble: "contingency tables with zero entries … may lead to cases where … the maximum likelihood estimate … may not exist or may not be identifiable". In modern-slavery data it "appears to be the norm rather than the exception that there will be pairs of lists between which there is no observed overlap".
  - Source: [Chan, Silverman & Vincent 2019](https://arxiv.org/abs/1902.05156).
- **Confidentiality context of real MSE work [documented].** "data are often highly anonymized for reasons of confidentiality and security. Typically, those analyzing the data may not know anything about a list other than an uninformative label, because the collation between lists is carried out by a single trusted individual or agency … there may be no further information available, beyond simply the number of overlapping cases". This matches the brief's set-up: linkage inside, counts out. — [Chan et al. 2019](https://arxiv.org/abs/1902.05156)
- **Home Office application [documented: landing page].** Silverman (Home Office Chief Scientific Adviser), "Modern Slavery: an application of multiple systems estimation", 29 Nov 2014. "By analysing the overlaps between cases that come to attention through various sources … an estimate of between 10 thousand and 13 thousand … potential victims in the UK in 2013." — [GOV.UK](https://www.gov.uk/government/publications/modern-slavery-an-application-of-multiple-systems-estimation). Chan et al. state that this MSE "was a key component of the strategy (Home Office, 2014) leading to the UK Modern Slavery Act 2015" **[documented]**.
- **Rcapture [documented].** Rcapture fits closed-population log-linear models (M0, Mt, Mh, Mth and others) and user design matrices (`closedp.mX`) "by carrying out a Poisson regression with the R function glm". `closedp.mX` "allows, for instance, fitting a model with an interaction between two capture occasions". — [Baillargeon & Rivest, JSS 19(5), Apr 2007](https://www.jstatsoft.org/article/view/v019i05)
- **Package maintenance [documented: CRAN pages and DESCRIPTION files].**
  - **Rcapture:** 1.4-4, published 2022-05-04, maintainer Louis-Paul Rivest ([CRAN](https://cran.r-project.org/package=Rcapture)).
  - **SparseMSE:** 2.0.1, published 2019-12-15, maintainer Lax Chan. It "explicitly handles situations where there are pairs of lists which have no observed individuals in common" ([CRAN](https://cran.r-project.org/package=SparseMSE)).
  - **LCMCR:** 0.4.14, published 2023-12-13, maintainer Daniel Manrique-Vallier, "Bayesian Non-Parametric Latent-Class Capture-Recapture". CRAN flags "[email to maintainer is undeliverable]". CRAN checks show OK or NOTE only (no errors) on current R-devel flavours ([CRAN](https://cran.r-project.org/package=LCMCR); [checks](https://cran.r-project.org/web/checks/check_results_LCMCR.html)). The archive shows 0.4.13 on 2023-05-24 and 0.4 in 2016.

### Inferences
- **[inferred; theoretical, from the exponential-family form of the model]** The pairwise Poisson log-linear model has minimal sufficient statistics N*i (source sizes), N*ij (pairwise intersections) and N*∅ (total observed). These are exactly the "coverage and overlap counts" one would release.
  - Release {sizes, all pairwise overlaps, total distinct} and the generator outside can fit the same pairwise MSE model a statistician would fit inside, and sample a consistent 2^k table from it.
  - This reproduces the pairwise dependence between sources but **imposes** zero higher-order interaction. The real 3+-source overlap is not reproduced unless chosen 3-way margins are also released.
- **[inferred]** MSE adds a second piece of information: the estimated dark figure (entities in no source). For a stand-in generator this tells how many "latent" entities exist that could later appear when a new or delayed source arrives.
- **[inferred]** MSE assumes a closed population over the observation window. Sources with reporting delays break this unless counts are taken at a common as-of date with a lag allowance. It is an analysis model, not a generator, but its fitted model can drive one.
- **[inferred]** Package maintenance: all three are stable but not actively developed. Rcapture and LCMCR pass CRAN checks; LCMCR's maintainer address bounces. They are suitable for analysis inside the environment, not as dependencies with an active upstream.

### Gaps
- I did not read the Home Office 2014 PDF itself (number of lists, model chosen); only the GOV.UK landing page.
- I did not check ONS use of MSE (for example for population estimates from admin data).
- I did not review Bird & King (2018, *Annual Review of Statistics*) on MSE practice.

## Q4. What such releases disclose; DP release of the 2^k table or margins

### Takeaway
The disclosure units are the cells of the presence table. A small cell ("one entity found only in sources B and D") identifies a rare linkage pattern. It can be pinned by tight sharp bounds even when only margins are released (Q2). Snapshots taken over time difference into individual changes.

Under DP with the entity as the unit, the full 2^k presence table has L1 sensitivity 1, because each entity falls in exactly one cell. Any set of margins (overlaps) can then be derived by post-processing. Releasing many intersection counts directly costs sensitivity that grows with the number of intersections each entity is in.

### Cited Findings
- **Tight bounds on small cells [documented].** Bounds that tightly pin a small cell disclose it. Dobra & Fienberg: "if a cell count is small and the upper bound is 'close' to the lower bound, the intruder knows with certainty …" ([PMC17264](https://pmc.ncbi.nlm.nih.gov/articles/PMC17264)). Dobra–Karr–Sanil: "small count … cells can be bounded too accurately on the basis of the released sub-tables" ([2003](https://sites.stat.washington.edu/adobra/Files/Papers/ADstatcomp2003.pdf)).
- **Differencing, thresholds, reconstruction and the entity-level DP unit [documented in earlier notes; not redone].** See `/home/user/research/research_notes/Synthetic stand in test data/disclosure_and_licensing.md`: the SACRO differencing example and thresholds of 5–10; the ONS cell key; Dinur–Nissim reconstruction; NIST's "unit of privacy" hazard; and the earlier inference that the DP unit must be the resolved real-world entity, not the source row.
- **Marginal-based DP synthesis [documented in earlier notes; not redone].** Private-PGM/mbi estimates a model from noisy marginal measurements alone, with MST, AIM and MWEM built on it. See `/home/user/research/research_notes/Synthetic stand in test data/generation_methods_and_tools.md` Q1.

### Inferences
- **[inferred; theoretical, standard DP sensitivity]** Release choices under DP with entity as the unit:
  - **Full 2^k − 1 cell table.** One entity changes exactly one cell, so L1 sensitivity = 1 and L2 sensitivity = 1. Every intersection, source size and union can then be computed from the noisy table as post-processing, at no extra privacy cost.
  - **Selected intersection counts.** An entity present in m sources contributes to C(m,2) pairwise counts, so the sensitivity of releasing all pairwise counts is C(k,2) in the worst case.
  - For small k (say ≤ 10, 1,023 cells) the noisy full table is likely the better release. For larger k, measure chosen margins (for example via MST/AIM's selection) and fit with Private-PGM, which accepts the presence bits as k binary attributes.
- **[inferred]** Treat presence bits as ordinary binary attributes of a per-entity record (the root table, after entity resolution inside). The cross-source overlap problem then reduces to marginal synthesis on k binary columns plus whatever entity attributes are needed. The marginal-synthesis tooling in the earlier notes applies unchanged.
- **[inferred]** Without DP: release only margins whose sharp integer bounds (Q2) leave every small cell unpinned; suppress or coarsen rare patterns (for example collapse sources into "≥ 3 other sources"); and audit each new release jointly with all earlier ones. The joint constraint set grows with every release, so a table safe on its own may not be safe alongside its predecessor (the differencing case).
- **[inferred]** Coverage and delay counts (for example "entities in A appearing in B within d days") are further margins of a time-extended table. They add constraints and so must enter the same audit.
- **[inferred]** The licensed-reference-data dimension: when a source is licensed, its size and its overlaps with other sources may themselves be licence-restricted figures. This is separate from privacy, as in the earlier disclosure notes.

### Gaps
- I found no published guidance specifically on DP or SDC release of record-linkage overlap tables between administrative sources. Theory is transferred from general contingency-table work.

## Q5. Status of DPSynth (google-parfait/dpsynth), the JMLR 2026 relational DP paper, and PrivPetal

### Takeaway
**DPSynth** exists:
- Apache-2.0; 284 commits from 2026-05-22 to 2026-11-23; version string 0.5.0; not on PyPI.
- Its README says it is "under active development" and working "toward a stable release".
- The relational module (`dpsynth.relational`, from Aug 2026) is labelled "EARLY EXPERIMENTAL … not yet recommended for production". It supports tree-shaped foreign-key hierarchies only (multiple parents and cycles are rejected). It builds on mbi/AIM/MST and on PrivPetal-style permutation modelling.

**The JMLR paper** exists:
- Alim, Wang, Gulati, Srivastava & Azizan, JMLR 27(158):1–50, 2026; arXiv 2405.18670, first posted 29 May 2024 under the title "Adapting Differentially Private Synthetic Data to Relational Databases".
- It has research code at azizanlab/dp-relational: 74 commits, last 2025-07-07, **no licence file**.

### Cited Findings
- **DPSynth repo facts [documented: `git clone` of https://github.com/google-parfait/dpsynth, inspected 2026-11-26].**
  - Licence and version: LICENSE is Apache License 2.0. `dpsynth/__init__.py` has `__version__ = '0.5.0'`.
  - History: first commit 2026-05-22 ("Initialize main branch"); HEAD 3711e35, 2026-11-23 ("Surface examples guide in ReadTheDocs …"); 284 commits. Top committer: Ryan McKenna, 199 commits. He is also the author of Private-PGM, per that repo in the earlier notes.
  - Not published: `https://pypi.org/pypi/dpsynth/json` returned HTTP 404 **[documented]**, so there is no PyPI release under that name.
- **DPSynth README [documented].**
  - "**This library is under active development.** … Standard tabular data settings (categorical and numerical attributes, single-table schemas) are the most mature and well-tested … newer modalities in experimental and research modules are still being developed". "Thank you for your patience as we build toward a stable release!"
  - Modalities: discrete, tabular, "Relational (Multi-Table): Multi-table databases with foreign-key hierarchies and referential integrity (`dpsynth.relational`)", nested, sequence, text.
  - "both produce synthetic data using the same underlying mathematical principles (marginal measurement + Private-PGM inference)".
  - Docs on ReadTheDocs ([dpsynth.readthedocs.io](https://dpsynth.readthedocs.io/en/latest/)); I did not fetch the rendered docs, only the repo `docs/` folder listing.
- **DPSynth CHANGELOG, [Unreleased] [documented].** "Relational (multi-table) synthesis: Exposed `MultiTableConfig`, `MultiTableMechanism`, and `ForeignKeyRelation` at top-level API … with foreign-key integrity …, including an end-to-end California Census housing example."
- **`dpsynth/relational/README.md` [documented].**
  - "**UNDER ACTIVE DEVELOPMENT / EXPERIMENTAL**: This module is in an early experimental stage … APIs, internal interfaces, and algorithms are subject to breaking changes. It is not yet recommended for production use."
  - Privacy unit: "privacy is protected at the **root parent record** (e.g. the household)".
  - Method: "Cascading Relational Synthesis … table-by-table down foreign-key hierarchy trees"; "Permutation Modeling … inspired by PrivPetal ([Cai et al., 2025](https://arxiv.org/abs/2503.22970))"; "Reuses existing discrete mechanisms (e.g. AIM, MST) and the `mbi` (Private-PGM) graphical model engine".
  - The API is headed "Planned API" and uses `ForeignKeyRelation(…, max_children_per_parent=5)`.
- **DPSynth code limitations [documented].**
  - `domain.py` raises "Child table … has multiple parents", and raises on cycles and self-references, so only trees or forests are supported.
  - `synthesizer.py`: "For simplicity, user-defined constraints are not supported yet."
  - The relational module's first commits are 2026-08-17/18 (skeleton; DAG sort; per-root sensitivity weights w = 1/k_eff with cascading truncation).
- **JMLR paper [documented: JMLR abstract page and code README; full paper not read].**
  - Citation: "Differentially Private Synthetic Data Generation for Relational Databases", Kaveh Alim, Hao Wang, Ojas Gulati, Akash Srivastava, Navid Azizan, *JMLR* 27(158):1−50, 2026 ([JMLR](https://www.jmlr.org/papers/v27/25-0136.html)).
  - Method (abstract): "the first-of-its-kind algorithm that can be combined with any existing DP mechanisms to generate synthetic relational databases. Our algorithm iteratively refines the relationship between individual synthetic tables to minimize their approximation errors in terms of low-order marginal distributions while maintaining referential integrity … eliminates the need to flatten a relational database into a master table … We provide both DP and theoretical utility guarantees" ([code README, quoting the abstract](https://github.com/azizanlab/dp-relational)).
  - arXiv 2405.18670 v1 was submitted 29 May 2024 ([arXiv](https://arxiv.org/abs/2405.18670)). The ar5iv/v1 title was "Adapting Differentially Private Synthetic Data to Relational Databases" **[lead: search result titles]**.
  - An MIT thesis by Kaveh Alimohammadi with the same title (2025) is in DSpace **[lead]** ([DSpace](https://dspace.mit.edu/handle/1721.1/163540)).
- **JMLR code repo [documented: `git clone` of https://github.com/azizanlab/dp-relational].**
  - History: 74 commits, 2024-04-12 → 2025-07-07. **No LICENSE file.**
  - README: titled "(v0.1.0)". Individual tables are generated "using `smartnoise-synth` synthesizers", then a `cross_generation_strategy` "iteratively refine[s] the synthetic tables based on the relationships between them".
  - Dependencies include `torch` "with GPU support!" and `mosek` ("may be possible to safely remove"). Experiments use IPUMS and MovieLens scripts.
- **PrivPetal [documented in earlier notes, abstract only; not redone].** arXiv 2503.22970, 2025-03-29, "Relational Data Synthesis via Permutation Relations" (see `generation_methods_and_tools.md`). New in this track: DPSynth's relational module cites PrivPetal as the inspiration for its permutation modelling **[documented]**. I did not check whether standalone PrivPetal code exists.

### Inferences
- **[inferred]** For cross-source overlap, a DPSynth relational schema such as Entity (root) → per-source record tables (one child table per source, each with a single parent) fits the tree restriction. Privacy is at the root entity, as the earlier notes recommend.
  - Whether per-source child presence is correlated across sibling child tables (A vs B presence) depends on the permutation/sibling modelling. I have not verified that.
  - The simpler route is to put the k presence bits on the root table, so that the 2^k table is a root-level marginal measured by AIM/MST.
- **[inferred]** The dp-relational research code has no licence. Legally it is all-rights-reserved and should not be used beyond reading. It is not maintained (last commit 2025-07) and needs GPU torch, so it is a reference implementation of the paper, not a tool.
- **[inferred]** DPSynth is not on PyPI, and its relational API is called "Planned" in its own README. Any adoption would pin a git commit. Its single-table and discrete paths (mbi-based) are the mature part and overlap with the earlier mbi/SmartNoise recommendations.

### Gaps
- I did not read the full JMLR paper: the method details, which DP mechanisms were combined, and the utility theorems are as stated in the abstract only.
- I did not run DPSynth or its California Census example.
- I did not verify the dpsynth ReadTheDocs pages as rendered.

## Q6. Verdicts on the external report's claims (sections 1.2, 2.2, 11.1)

### Takeaway
The overlap example is confirmed, but it omits the "union fixes k = 3" caveat. The DPSynth and JMLR 2026 claims are confirmed. The report does not mention that the JMLR code has no licence, or that DPSynth's relational module supports tree-shaped schemas only.

### Cited Findings
**Section 1.2**

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1.2-a | "Even knowing every pairwise overlap does not necessarily determine how many entities occur in all three sources" | **Confirmed**, with a caveat **[theoretical]** | True given sizes and pairs. If the union (distinct total) is also known, k = 3 is fully determined by inclusion–exclusion. For k ≥ 4 it remains undetermined even with the union (1,662 tables in my k = 4 example). See Q1. |
| 1.2-b | Example: 3 × 100, pairs 50 → 150 unique / none in all three, vs 200 unique / 50 in all three | **Confirmed** (arithmetic) | `overlap.py`: both have identical sizes and pairs; the unions are 150 and 200. The full family is union = 150 + t, t ∈ [0, 50]. |
| 1.2-c | "the complete overlap distribution may itself become too large and disclosive. A selected set of intersections or a conditional coverage model is needed." | **Partially confirmed** | The size claim holds: 2^k − 1 cells. "Disclosive" is backed by Dobra–Fienberg and Dobra–Karr–Sanil (small cells pinned by bounds) [documented]. A selected set of intersections is the MSE practice (pairwise log-linear model) [documented]. However, a selected set can itself pin cells: in my sparse k = 4 example, sizes, pairs and union determine the whole table uniquely. "Selected intersections" is not automatically safe and needs a sharp-bounds audit [inferred]. |
| 1.2-d | ONS 2019 synthetic data pilot recommends concentrating on needed relationships | **Not checked in this track** | Outside this track's scope. |

**Section 2.2**

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 2.2-a | DPSynth (google-parfait/dpsynth): "Emerging open-source research library; explicitly working towards a stable release" | **Confirmed** | Apache-2.0; README says "build toward a stable release" and "under active development"; v0.5.0; no PyPI release; first commit 2026-05-22, last 2026-11-23. |
| 2.2-b | DPSynth "Supports DP synthesis, including experimental relational capabilities" | **Confirmed** | The relational README says "EARLY EXPERIMENTAL … not yet recommended for production use". It supports only tree-shaped FK hierarchies: multiple parents and cycles are rejected, and user constraints are not supported. The report does not mention the tree restriction. |
| 2.2-c | DPSynth "Real inputs remain inside" | **Inferred / consistent** | The `CalibratedMechanism.__call__(rng, data)` design runs on the sensitive data and emits synthetic tables plus a `dp_event`. This is a deployment choice, not a library property. |
| 2.2-d | PrivLava: "Academic implementation accompanying a 2023 paper" | **Unverifiable here** | Earlier notes: arXiv 2304.04545 (2023-04-10), "I found no packaged code". Not rechecked in this track, so the existence of an implementation is unconfirmed. |
| 2.2-e | PrivPetal (2025) exists | **Confirmed** | arXiv 2503.22970, 2025-03-29 (earlier notes); cited by DPSynth relational. |
| 2.2-f | "Differentially Private Synthetic Data Generation for Relational Databases (JMLR, 2026)" | **Confirmed** | JMLR 27(158):1–50, 2026; Alim, Wang, Gulati, Srivastava, Azizan; arXiv since 2024-05-29. Code exists (azizanlab/dp-relational) but has no licence and was last updated 2025-07-07. The report does not mention this. |
| 2.2-g | synthpop "version 1.9-3, September 2026" | **Confirmed** | CRAN Date/Publication 2026-09-10; matches the earlier notes. "Original paper 2016" was not checked here. |

**Section 11.1**

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 11.1-a | "Relational DP synthesis — Emerging — PrivLava, DPSynth" | **Partially confirmed** | "Emerging" fits: DPSynth relational is experimental, and the JMLR code is an unlicensed research prototype. Listing PrivLava as a candidate tool is not supported: no packaged code was found. The list omits the JMLR dp-relational code. |
| 11.1-b | "Multi-source entity simulation — Custom integration" | **Confirmed as inference** | No tool found in this track generates multi-source presence patterns from released overlap margins. MSE packages (Rcapture, SparseMSE, LCMCR) fit models for analysis but are not generators, and their last CRAN releases were 2019–2023. Marginal synthesis (mbi) can do it if presence bits are modelled as attributes [inferred]. |

### Inferences
- **[inferred]** What the report most needs to add: a sharp-integer-bounds audit of every proposed overlap release, cumulative across releases; and an explicit modelling assumption for 3+-source overlap when only pairwise counts are released (the MSE zero-higher-order-interaction default).

### Gaps
- Claims 1.2-d and 2.2-d were not verified in this track (see above).
