# T3 verification: requirements-boundary methods, conformance/model-based testing, executable reference models, checking from outside

Scope: report `reports/Black box boundary spec methods.md` § 3.6 (l. 236–249), § 3.7 (l. 250–259), § 3.8 (l. 260–270), § 3.10 (l. 277–291), § 5 (l. 330–374), the matching § 8.2 source rows, and the ShardStore/Cedar/SQLite mentions in § 1, § 2.2, § 2.3 and § 7.3 that rest on the same sources.

Method: every verdict below comes from a full text downloaded on 2026-10-22 into `/tmp/claude-0/-home-user-research/6eb654f9-be93-5692-960f-f1941dafeecc/scratchpad/dl_t3/` and read with `pdftotext`. No verdict rests on a search extract. Where the cited host failed, I tried alternates. Grades follow the brief: A = peer-reviewed or measured study, B = industrial practice with data, C = practitioner report without data, D = opinion or marketing.

Hosts that failed: apps.dtic.mil (403), discovery.ucl.ac.uk (403), eweek.com (403), jamasoftware.com (403), cacm.acm.org and cacmb4.acm.org (403), dl.acm.org (403, per the brief), procon.bg (503 twice), repositoriosdigitales.mincyt.gob.ar (connection reset), ri.conicet.gov.ar (timeout), www.cis.upenn.edu (TLS chain failure with curl, 503 with WebFetch), www.cs.utexas.edu and web.eecs.umich.edu (TLS chain failure), api.github.com for TorXakis (session policy 403; I used an anonymous `git clone` instead).

Alternates that worked: ShardStore from cdn.amazon.science; Barr et al. from Harman's UCL staff page; Tretmans 2008 from the Radboud repository; Darlington from Lawford et al. (McMaster); Spec Explorer from Grieskamp's 2008 SambaXP slides; SCR from Heitmeyer's 2010 Marktoberdorf slides.

## Q1. Claim-by-claim verdicts (§ 3.6, 3.7, 3.8, 3.10, 5)

### Takeaway
The core results hold: ShardStore's 16 issues, Cedar's 4 + 21 bugs, ioco's out-set and quiescence semantics, the Barr four-way classification, Femmer's 59 % / 82 %, and SQLite's 590×.

Four corrections matter for the report:
1. ShardStore's validation code is 12–13 % of the code base, not "about 14 %".
2. Formal-verification overhead is quoted as "3–10×", not "2–10×".
3. The quote "we can still miss bugs" is not in the paper.
4. ShardStore explicitly rejected tracking *sets* of model states after injected failures. The report's § 3.10 and § 5 imply otherwise.

Cedar was published at FSE Companion 2024, not OOPSLA. Barr et al. do not rank oracle types. The ioco claims should cite Tretmans 2008, not arXiv 1403.7260.

### Cited Findings

| ID | Report location | Claim (short) | Source URL actually read | Verdict | Correction / quote |
|---|---|---|---|---|---|
| T3-01 | § 3.6 l. 239; § 8.2 l. 578 | Four-variable model: REQ over monitored/controlled quantities, NAT = environment constraints (NRL SCR overview, A) | https://apps.dtic.mil/sti/pdfs/ADA465161.pdf → 403. Alternate read: https://asimod.in.tum.de/2010/slides/heitmeyer/Heitmeyer2-Markt2010.pdf | **Unverifiable from the cited source** (apps.dtic.mil 403). Substance supported by the author's own slides (C) | Slides: "NAT: All possible behaviors satisfying natural laws, constraints on the system env"; "REQ: All acceptable system behaviors"; "Set of monitored variables … Set of controlled variables". Parnas–Madey (SCP 1995) full text not reached: the McMaster record has metadata only, and Elsevier was not tried. **Grade:** an NRL technical overview is not peer-reviewed, so grade it B/C unless a peer-reviewed version is cited |
| T3-02 | § 3.6 l. 240; § 5 table l. 341; § 8.2 l. 580 | Heitmeyer & Labaw: SCR tables make completeness and disjointness checks automatic; quote "spent too much of their time and effort checking for simple, application-independent properties" (A) | https://apps.dtic.mil/sti/pdfs/ADA276077.pdf → 403. Journal version ADA465574 → 403. Alternate: Heitmeyer 2010 slides (above); Lawford et al. (T3-03) | **Quote unverifiable** (apps.dtic.mil 403). **Mechanism confirmed** from alternates | Slides: consistency checking "checks spec for application-independent properties, including properties required of the tables", "Analyzing Disjointness and Coverage" (each pair of cells c1 ∧ c2 = false; c1 ∨ … ∨ cn = true). Lawford et al.: PVS's COND construct "causes PVS to automatically generate Disjointness and Completeness" proof obligations. A search extract says the quote is Heitmeyer & Labaw *quoting Parnas*; not verified. **Grade:** NRL Formal Report NRL/FR/5540-93-9586 is a technical report (B/C). A for this claim needs the peer-reviewed TOSEM 1996 version (Heitmeyer, Jeffords, Labaw), which I did not reach |
| T3-03 | § 3.6 l. 241; § 8.2 l. 581 | Darlington: tables for requirements and code, PVS proofs, under regulatory pressure (Lawford & Wassyng, A) | https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf → 503 (twice). Alternate read: https://www.cas.mcmaster.ca/~lawford/papers/tables.pdf (Lawford, Froebel, Moum, "Application of Tabular Methods to the Specification and Verification of a Nuclear Reactor Shutdown System", dated 2001) | Cited source **unverifiable**. **Confirmed, with one wording correction**, from the alternate | Alternate: the SDV procedure uses "tabular notation in both the requirements and design documents"; the SESM tools generate PVS input; "This change in focus was necessitated by regulatory requirements"; earlier applications "required at least some reverse engineering of existing requirements documents". Say "requirements and **design**" unless the 2012 paper says code. The 2001 PDF names no venue. Grade it A only if the journal version is cited |
| T3-04 | § 3.6 l. 242; § 8.2 l. 582 | EARS: five templates; single Rolls-Royce case; numbers unretrieved (A-weak) | https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/ (record and abstract only) | **Partly confirmed**; numbers still unverifiable (RE'09 full text not reached) | Abstract: "A small set of structural rules was developed to address eight common requirement problems including ambiguity, complexity and vagueness. The ruleset allows all natural language requirements to be expressed in one of five simple templates. The ruleset was applied whilst extracting aero engine control system requirements from an airworthiness regulation document … qualitative and quantitative improvements". RE'09, pp. 317–322. The abstract does not name Rolls-Royce. A-weak stands |
| T3-05 | § 3.6 l. 242; § 8.2 l. 583 | Jama "drastic" improvement, D | https://www.jamasoftware.com/blog/… → 403 | **Unverifiable** (jamasoftware.com 403) | Grade D is unaffected: it is vendor material either way |
| T3-06 | § 3.7 l. 252; § 2.4 l. 123; § 8.2 l. 609 | ioco: after every spec trace the implementation may produce only outputs the spec allows; quiescence δ counts as an output; unspecified inputs free; nondeterministic outputs a set (arXiv 1403.7260, A) | https://arxiv.org/pdf/1403.7260 (Beohar & Mousavi, MBT 2014, EPTCS 141); https://repository.ubn.ru.nl/bitstream/handle/2066/72680/72680.pdf (Tretmans 2008, publisher's version) | **Confirmed**, but the **citation should be corrected** | 1403.7260 confirms δ "modeling quiescence", the test hypothesis ("the behavior of the IUT can be expressed by an input-output transition system, which is unknown to the tester"), and "comparing them with the possible outputs prescribed by the model". It does **not** state that unspecified inputs are free. Tretmans 2008 states all of it: out(i after σ) ⊆ out(s after σ) "but only if σ is a suspension trace of the specification"; "an implementation may have additional features"; for a non-input-enabled spec, "?but·?but·?but is an underspecified trace, and any behaviour is allowed after it". Caveat: ioco and uioco differ on traces that are underspecified only along some nondeterministic branches. Cite Tretmans 2008 (A) as primary |
| T3-07 | § 5 l. 351–352 | Testers approximate δ with timeouts, an engineering assumption outside the theory | Tretmans 2008 (above) | **Confirmed** | "Theoretically, this means that the tester has to wait for an infinite amount of time … More practically, one could think of θ as being implemented as the expiration of a time-out. Of course, care should be taken when choosing such a (finite) time-out value" |
| T3-08 | § 3.7 l. 254; § 8.2 l. 610 | Grieskamp et al. 2011: MBT "works and scales, provided it is accompanied by sound tool support and clear methodological guidance" (A) | Record → connection reset; https://ri.conicet.gov.ar/handle/11336/15937 → timeout; CACM 2011 → 403 | **Unverifiable** (mincyt.gob.ar connection reset; ri.conicet.gov.ar timeout; cacm.acm.org 403) | STVR 21(1), 2011, per a search extract (not counted). Grade A is plausible for STVR, but the quote is unverified |
| T3-09 | § 3.7 l. 254; § 8.2 l. 611 | "250 person-years" (eWeek, D/C) | eweek.com → 403. Alternate read: https://sambaxp.org/archive_data/sxp08/SambaXP2008-DATA/00-05-Wolfgang_Grieskamp-MBT.pdf | **Unverifiable** (eweek.com 403). Related figures found in Grieskamp's own slides (C) | Slides (2008-04-17): "250+ protocols in Windows alone (~ 30,000 pages of documentation)"; "Current investment ~280 vendor employees for parser and test suite development ~50 Microsoft employees for management and tools infrastructure". *Inference:* "250" also appears as the protocol count, so "250 person-years" may be a conflation. Treat it as unsupported |
| T3-10 | § 3.7 l. 254; § 8.2 l. 612 | Hughes et al., ICST 2016: stateful QuickCheck found Dropbox problems without visibility of internal choices (A) | cis.upenn.edu → TLS failure / 503; chalmers.se alternate → 404 | **Unverifiable** (www.cis.upenn.edu TLS/503) | Indirect: Tretmans & van de Laar 2019 re-ran the case with TorXakis ("Model-Based Testing with TorXakis: The Mysteries of Dropbox Revisited", CECIIS 2019), cited in https://arxiv.org/pdf/2102.00378 |
| T3-11 | § 3.8 l. 264; § 2.2 l. 61 | ShardStore: 16 issues prevented (A) | https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf | **Confirmed** | Abstract: "prevented 16 issues from reaching production, including subtle crash consistency and concurrency problems". Fig. 5 breakdown: #1–5 functional correctness, #6–10 crash consistency, #11–16 concurrency |
| T3-12 | § 3.8 l. 264 ("about 14 % added code"); § 2.2 l. 61 ("spec and harness about 14 % of the codebase"); § 7.3 l. 528 ("ShardStore baseline ≈ 14 %") | Size of the validation artefacts | same PDF | **Corrected** | § 8.2: the reference models and validation harnesses "are only 13% of the total code base and 20% of the size of the implementation code". Intro: "the combined property definitions and test harnesses comprise 12% of the ShardStore code base". Fig. 6 (Rust LOC): implementation 44,048; unit and integration tests 19,540; reference models 450; functional-correctness checks 4,860; crash-consistency checks 2,661; concurrency checks 901; total 72,460. My arithmetic: (450 + 4,860 + 2,661 + 901) / 72,460 = 12.2 %; / 44,048 = 20.1 %. The reference models alone are ≈ 1 % of the implementation ("small executable specifications (1% of the implementation code)") |
| T3-13 | § 3.8 l. 264 | "against 2–10× for full verification" | same PDF | **Corrected** | "an overhead that compares favorably to formal verification approaches that report 3–10× overhead [8, 18, 49]". VeriBetrKV: "7 lines of proof for every line of implementation" |
| T3-14 | § 3.8 l. 264 | Engineers without a formal-methods background maintained it | same PDF | **Confirmed, with detail** | "led initially by two formal methods experts working full-time for nine months and a third expert who joined for three months … most work on them has been taken over by the ShardStore engineering team, none of whom have any prior formal methods experience"; "18% of the lines of code in the test harnesses were last edited by a non-formal-methods expert according to git blame"; three engineers each wrote >100 lines; four engineers wrote new stateless model-checking harnesses |
| T3-15 | § 3.8 l. 264; § 5 l. 338 | Quote: "we can still miss bugs" | same PDF | **Not found verbatim**; substance confirmed | Actual text: "our validation checks can miss bugs—their reporting success does not mean the code is correct, only that they could not find a bug" (§ 8.3). Also: "we can miss bugs these systems would have caught" (§ 9). And: "we were willing to accept weaker correctness guarantees than full formal verification". They know of one bug the checks should have caught but did not; it was caught in code review |
| T3-16 | § 2.3 l. 82 | Quoted principle "decompose correctness into independent properties, check each with the most suitable tool, use executable reference models as the specification" | same PDF | **Corrected** (a paraphrase shown as a quote) | Abstract: "Our approach decomposes correctness into independent properties, each checked by the most appropriate tool, and develops executable reference models as specifications to be checked against the implementation." |
| T3-17 | § 3.8 l. 268 | ShardStore's scope is a single node | same PDF | **Confirmed** | Title: "…a Key-Value Storage Node". S3 "replicates object data across multiple storage nodes, so single-node crash consistency issues do not cause data loss" |
| T3-18 | § 3.10 l. 290 (reference model: "sets of outcomes", "via fault shims"); § 5 l. 357 ("ShardStore's injected IO failures against a reference model"); § 5 l. 369 recipe ("reference model that returns sets of allowed outcomes") | ShardStore mechanism (†) | same PDF | **Partly refuted**: injection confirmed; "sets of outcomes" is not ShardStore's practice | ShardStore injects failures as generated operations ("FailDiskOnce(ExtentId) causes the next IO to the chosen extent to fail") into an in-memory disk. It then **relaxes** equivalence instead of computing outcome sets: "One solution would be to track all possible states of the reference model after a failure, but this blows up quickly in the face of multiple failures … Instead, the harness tracks a simple 'has failed' flag". Under that flag, a Get "is allowed to fail by returning no data, but is never allowed to return the wrong data". The models also "omit other implementation failures (IO errors, resource exhaustion, etc.)". The "sets of allowed outcomes" design in § 5 is therefore the report's own inference, and ShardStore names its cost. Other mechanism details in Q2 |
| T3-19 | § 3.8 l. 265; § 2.2 l. 62; § 5 l. 337 | Cedar: proofs over a Lean model plus differential random testing of the Rust code; 4 bugs by proof, 21 by DRT/PBT (A) | https://arxiv.org/pdf/2407.01688 | **Confirmed**; **venue corrected** | "While carrying out proofs, we found and fixed 4 bugs in Cedar's policy validator, and DRT and PBT helped us find and fix 21 additional bugs in various parts of Cedar." Venue: "FSE Companion '24, July 15–19, 2024, Porto de Galinhas" (industry paper), not OOPSLA. Grade A (peer-reviewed industry track) stands. Effort figures in Q3 |
| T3-20 | § 1 Kernsatz l. 3 | "Executable reference models with property-based and model-based testing found crash and concurrency bugs at AWS ShardStore and Cedar" | ShardStore and Cedar PDFs | **Corrected** (misattributed for Cedar) | ShardStore: crash-consistency and concurrency issues. Cedar's bugs were in the validator (one non-termination, three soundness), parser, formatter, IP-address handling and namespace interpretation (Table 3). None is a crash or concurrency bug |
| T3-21 | § 5 table l. 340; § 8.2 l. 584 | Structured prose: "nothing mechanical; smells at most" (Femmer et al., A†) | https://arxiv.org/pdf/1611.08847 (preprint accepted at JSS, doi 10.1016/j.jss.2016.02.047) | **Confirmed; drop the †; grade A stands** | Figures in Q4. Abstract: "average precision of 59% at an average recall of 82% with high variation" |
| T3-22 | § 5 l. 365; § 8.2 l. 619 | Barr et al., TSE 2015: survey "puts specified oracles (models, contracts) ahead of derived oracles (other versions, metamorphic relations) and implicit oracles (crashes, leaks)" (A, classification †) | http://www0.cs.ucl.ac.uk/staff/M.Harman/tse-oracle.pdf (UCL Discovery → 403) | Classification **confirmed** (drop the †); **"puts … ahead" not found in source** | Details in Q5. The survey orders its sections, but nothing in it ranks one class above another. Rewrite as "classifies" |
| T3-23 | § 2.2 l. 78; § 8.2 l. 587 | SQLite: the checkable artefact is executable (sqlite.org/testing, B) | https://sqlite.org/testing.html | **Confirmed**; the 590× ratio is now verified | Figures in Q6 |
| T3-24 | § 5 l. 347 | Unspecified inputs free; nondeterministic outputs checked against a set | Tretmans 2008 | **Confirmed** (see T3-06) | Cite Tretmans 2008 instead of 1403.7260 |
| T3-25 | § 5 table l. 345 | Model-checked spec (TLA+, P, Alloy): safety and liveness within bounds | https://alloytools.org/alloy6.html | **Confirmed for Alloy 6** (tool docs, C) | Alloy 6 adds "linear-time temporal logic with past connectives"; "Instances are now traces … lasso traces". Before Alloy 6, behaviour needed explicitly modelled traces. TLA+ and P were not checked here |
| T3-26 | § 3.10 l. 287 | Four-variable / SCR / EARS row graded "A / A-weak" | see T3-01 to T3-04 | **Grade at risk** | The SCR sources cited are NRL technical reports (B/C), and their full texts are unreachable. A rests on Darlington (Lawford et al.), which supports tables plus PVS. Cite the TOSEM 1996 consistency-checking paper to keep A for SCR |
| T3-27 | § 3.10 l. 289 | ioco / MBT / stateful PBT row, A | T3-06 to T3-10 | ioco **A confirmed** (Tretmans 2008). Spec Explorer and Dropbox claims **unverifiable** | The row's A rests on the theory. The industrial-scale evidence is, for now, only Grieskamp's C-grade slides |
| T3-28 | § 3.10 l. 290 | Executable reference model row: "Unspecified: sets of outcomes"; "Profiles: parameterised model" | ShardStore and Cedar PDFs | **Not found in sources** (both are inference) | Neither paper parameterises its model by deployment profile. ShardStore relaxes equivalence (T3-18) |

### Inferences
- *Inference:* the ShardStore cost figure moves from "≈ 14 %" to "12–13 % of the code base (≈ 20 % of the implementation); the reference models themselves ≈ 1 %". The cost claim gets slightly stronger, not weaker.
- *Inference:* the report's § 5 recipe ("an executable reference model that returns sets of allowed outcomes, including 'indeterminate'") is not what ShardStore did. ShardStore reports that full outcome-set tracking "blows up quickly in the face of multiple failures". The recipe has to say either how it bounds the set, or adopt ShardStore's "has failed" relaxation with a separate "never wrong data" invariant.
- *Inference:* ShardStore states that it does "not currently check properties of concurrent crashing executions because we have not found an effective automated approach". That is exactly the running example's hard case: a failure while another writer is active and a handle is open. The best-evidenced reference-model practice therefore leaves that cell unchecked.

### Gaps
- Unverifiable, full text unreachable: NRL SCR overview and Heitmeyer & Labaw (apps.dtic.mil 403); Lawford & Wassyng 2012 (procon.bg 503); Grieskamp et al. 2011 STVR and CACM (mincyt reset, conicet timeout, cacm 403); eWeek and Jama (403); Hughes et al. ICST 2016 (cis.upenn.edu TLS/503); Parnas–Madey SCP 1995 and Zave–Jackson TOSEM 1997 (not attempted beyond the record pages; Elsevier and ACM are paywalled or 403); EARS RE'09 full text (IEEE, not reached).

## Q2. ShardStore (Bornholt et al., SOSP 2021): reference-model mechanism and figures

### Takeaway
ShardStore's specification is ≈ 450 lines of Rust reference models (about 1 % of a 44 kLOC implementation). They are checked by three different mechanisms, one per property class: PBT for functional correctness, PBT with dirty reboots for crash consistency, and stateless model checking for linearizability. The models leave failures out on purpose, and conformance is relaxed after an injected failure. Concurrent crashing executions are not checked.

### Cited Findings
All from [ShardStore SOSP 2021 PDF](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf) (A):
- **Reference models.** Each is written in Rust against the same interface as the component. For example, the LSM-tree index's model "is a hash map". The models are reused "as mock implementations for ShardStore unit tests, effectively requiring engineers to update the reference model specifications themselves". A reference model "defines the allowed sequential, crash-free behaviors of a component".
- **Failures are left out of the models.** "we found it very difficult to enforce strict equality for failures … we choose to omit other implementation failures (IO errors, resource exhaustion, etc.) from the models … precluding us from reasoning about most availability or performance properties."
- **Why the same language as the code.** The authors considered Alloy, Promela and P, but chose Rust "to minimize the cognitive burden of learning a new language" and to keep the models maintained by the team.
- **Three-way decomposition of durability.**
  - Sequential crash-free executions are checked by direct equivalence (§ 4).
  - Sequential crashing executions are checked by "extend[ing] the reference model to define which data can be lost after a crash" (§ 5).
  - Concurrent crash-free executions use "separate reference models and check linearizability" (§ 6).
  - "We do not currently check properties of concurrent crashing executions."
- **Functional correctness.** Property-based tests (`#[proptest]`) generate operation sequences and apply each to both the model and the implementation. Coverage is improved by "argument bias", which tilts choices toward corner cases. The authors warn that biasing "introduces the risk of baking our assumptions into" the tests.
- **Failure injection.** Failure operations join the operation alphabet (e.g. `FailDiskOnce(ExtentId)`). After a failure, a "has failed" flag relaxes the equivalence check: a failed Get may return no data but never wrong data. Tracking all possible model states was rejected because it "blows up quickly". Tests run "with and without failure injection enabled" so that the relaxation does not hide other bugs.
- **Crash consistency.** Each mutating operation returns a `Dependency` that can be polled for persistence. Two properties are checked:
  1. *Persistence*: "if a dependency says an operation has persisted before a crash, it should be readable after a crash (unless superseded…)".
  2. *Forward progress*: "after a non-crashing shutdown, every operation's dependency should indicate it is persistent".

  The checks are driven by a generated `DirtyReboot(RebootType)` operation.
- **Concurrency.** Two stateless model checkers are used. Loom soundly checks "all interleavings of small, correctness-critical code". Shuttle "randomly check[s] interleavings of larger test harnesses to which Loom does not scale".
- **Figures.**
  - 16 issues prevented: 5 functional, 5 crash consistency, 6 concurrency (Fig. 5).
  - Validation artefacts are 12 % (intro) or 13 % (§ 8.2) of the code base, and 20 % of implementation size.
  - Fig. 6 LOC: implementation 44,048; unit and integration tests 19,540; reference models 450; functional checks 4,860; crash checks 2,661; concurrency checks 901; total 72,460.
  - Formal verification is said to report 3–10× overhead.
  - Initial effort: 2 FM experts × 9 months + 1 × 3 months.
  - 18 % of harness lines were last edited by non-FM engineers.
- **Limits.** "our validation checks can miss bugs". They know of one bug the checks missed, which manual code review caught.

### Inferences
- *Inference:* for the boundary spec, ShardStore supports "reference model + stateful PBT + fault operations in the alphabet" as practice. It does not support "the model returns sets of allowed outcomes after faults". There it chose a weaker, cheaper relaxation plus a never-wrong-data invariant.
- *Inference:* ShardStore's models are per-component and sequential. Multi-observer behaviour enters only through linearizability against a separate model. No out-of-band store actor is modelled.

### Gaps
- No per-issue effort or time-to-detection data; the paper says diagnosis "remains a developer-intensive manual effort".

## Q3. Cedar (verification-guided development) effort figures

### Takeaway
The paper gives size and run-time figures but no person-month figures. Lean models are about a tenth the size of the Rust code they model. Proofs are 3.4× the model. Proof checking takes about 3 minutes.

### Cited Findings
All from [Disselkoen et al., "How We Built Cedar: A Verification-Guided Approach", FSE Companion '24, arXiv 2407.01688](https://arxiv.org/pdf/2407.01688) (A):
- **Table 1 (LOC).**
  - Lean model 1,673 in total: custom sets/maps 244, evaluator/authorizer 897, validator 532.
  - Lean proofs 5,714 in total: 681 / 347 / 4,686 for the same components.
  - Rust production 15,693 in total: parser 4,114, evaluator/authorizer 4,877, validator 6,702.
  - Rust tests 20,458; Rust other 31,391.
  - "The Lean models are an order of magnitude smaller than their Rust counterparts." The parser is not modelled.
- "Our total proof-to-model ratio is roughly 3.4 : 1." "It takes about 3 minutes to check all proofs and compile models for execution." Median execution time is 6 µs for the Lean authorizer and 10 µs for Rust.
- **Bugs.** Proofs found 4 bugs: one non-termination bug in the validator definition, found via termination proofs, and "three other bugs while attempting to carry out the validator soundness proof". DRT and PBT found 21, listed in Table 2/3. Examples: octal IPv4 accepted by Rust but not by the model; IPv4-embedded IPv6; parsing of `like` patterns.
- **DRT setup.** Daily on ECS, 4 vCPU and 8 GB per target, 6 h each, "millions of inputs". "We do not have a particular reason for the 6 hour duration."
- **Generator quality.** "35.5% of the when condition-expressions generated by the type-directed ABAC policy generator … are boolean literals". A new expression generator brought this to 9.7 %.
- **Missed bugs.** DRT "did not discover the non-termination bug". It also cannot find bugs "outside the scope of the test generators", for example parser bugs triggered by malformed policies.

### Inferences
- *Inference:* for the matrix's cost column, Cedar shows that proof costs about 3.4 lines per model line on top of a model that is about 10 % of the code. DRT is cheap to run but only as good as its generators. It missed a bug that proof found.

### Gaps
- No person-months, team size or calendar time for the models or proofs.

## Q4. Femmer et al., requirements smells: actual figures

### Takeaway
Femmer et al. define eight smells from the ISO 29148 language criteria. Average precision is 0.59 (0.48 over all inspected findings) and average recall is 0.82, with precision ranging from 0.26 to 0.96 by smell. The study covered three industrial contexts plus 51 student artefacts.

### Cited Findings
All from [Femmer, Méndez Fernández, Wagner, Eder, "Rapid Quality Assurance with Requirements Smells", JSS 2017 (arXiv 1611.08847)](https://arxiv.org/pdf/1611.08847) (A):
- **Smells.** ISO 29148 language criteria "which we use to define eight smells". The tool is Smella.
- **Study.** Three industrial contexts (Daimler AG, Wacker Chemie AG, TechDivision GmbH) plus an academic one: "51 requirements artifacts created by students". Corpus: 266,432 words and 11,608 findings, about 43.6 per 1,000 words (Table 6).
- **Precision (Table 7, 616 findings inspected).**

  | Smell | Precision |
  |---|---|
  | Subjective language | 0.96 |
  | Ambiguous adverbs/adjectives | 0.81 |
  | Loophole | 0.72 |
  | Non-verifiable term | 0.70 |
  | Superlative | 0.49 |
  | Comparative | 0.48 |
  | Negative words | 0.33 |
  | Vague pronouns | 0.26 |
  | Average | 0.59 |
  | Overall | 0.48 (293 of 616) |

- **Recall.** Measured on a sample of about 16,200 words with 200 manually identified findings: average 0.82. Four of the five investigated smells score 0.84–0.95. Superlatives score 0.5 on few data points. The four ambiguity-related smells were analysed "as if it was one smell".
- **Practitioner view.** For the 20 findings discussed with TechDivision, practitioners "considered 65% of the findings as relevant", "have not been aware of 45%", and "would act on 50%".

### Inferences
- *Inference:* the report's "smells at most" for structured prose stands. Smell detection is a mechanical check on prose, but a noisy one: overall precision 0.48.

### Gaps
- None for the figures. Smells check phrasing, not semantics; the paper makes no semantic claim.

## Q5. Barr et al., "The Oracle Problem in Software Testing: A Survey" (TSE 2015): its classification

### Takeaway
The survey classifies oracle work into four categories: specified, derived, implicit, and no automated oracle (reducing human effort). It does not rank them.

### Cited Findings
All from the [author copy, www0.cs.ucl.ac.uk](http://www0.cs.ucl.ac.uk/staff/M.Harman/tse-oracle.pdf) (A):
- **The four categories.** "We classify work on test oracles into four categories: specified test oracles (317), derived test oracles (245), implicit test oracles (76), and no test oracle (56), which handles the lack of a test oracle". The numbers are publication counts. The categories map to §§ 4–7: oracles "can be specified", "can be derived", "can be built from implicit information", and "no automatable oracle is available, yet it is still possible to reduce human effort".
- **Specified oracles** fall into "four broad categories: model-based specification languages, state transition systems, assertions and contracts, and algebraic specifications".
- **Derived oracles** "involve artefacts from which a test oracle may be derived — for instance, a previous version of the system". The search terms were specification inference and mining, API mining, metamorphic testing, regression testing and program documentation. Pseudo-oracles also fall here.
- **Implicit oracles** refer to "the detection of 'obvious' faults such as a program crash". The search terms covered null pointers, deadlock/livelock/race, memory leaks, crashes, performance/load, fuzzing and anomaly detection.

### Inferences
- *Inference:* the report's use of the classes is correct. The phrase "puts specified oracles ahead of" should become "distinguishes", because the paper makes no ranking claim.

### Gaps
- None.

## Q6. SQLite test-code ratio (current page)

### Takeaway
sqlite.org/testing.html still states 590× as much test code as library code. The figure is dated to version 3.42.0 (2023-05-16).

### Cited Findings
All from [sqlite.org/testing.html](https://sqlite.org/testing.html), fetched 2026-10-22 (B):
- **Ratio.** "As of version 3.42.0 (2023-05-16), the SQLite library consists of approximately 155.8 KSLOC of C code … the project has 590 times as much test code and test scripts - 92053.1 KSLOC."
- **TH3.** "TH3 consists of about 76.9 MB or 1055.4 KSLOC of C code implementing 50362 distinct test cases … a full-coverage test runs about 2.4 million different test instances". TH3 is proprietary and gives 100 % branch coverage and 100 % MC/DC of the core.
- **TCL tests.** 51,445 distinct test cases in 1,390 files.
- **SLT (SQL Logic Test).** Compares SQLite against "PostgreSQL, MySQL, Microsoft SQL Server, and Oracle 10g. SLT runs 7.2 million queries comprising 1.12GB of test data". This is differential testing across engines.
- **Fuzzing.** "We still maintain 100% MC/DC of the core SQLite code, but most testing CPU cycles are now devoted to fuzzing". dbsqlfuzz runs "about one billion test mutations per day".

### Inferences
- *Inference:* SLT is the industrial example of differential testing across realities (§ 5). Each query has one deterministic result, which avoids the nondeterminism problem the report raises.

### Gaps
- The page does not say whether the 590× ratio has been updated since 3.42.0.

## Q7. TorXakis: what it is, ioco basis, current status

### Takeaway
TorXakis is an open-source (BSD-3) model-based testing tool written in Haskell. It uses SMT solvers, and ioco is the only implementation relation it implements. The repository still gets maintenance commits (latest 2025-06-20) at changelog version v0.9.0. No industrial data was found.

### Cited Findings
- README: "`TorXakis` is a tool for Model Based Testing", BSD3. It is written in Haskell and "needs an SMT solver, such as cvc4 or Z3". (C, project docs) — [README](https://raw.githubusercontent.com/TorXakis/TorXakis/develop/README.md)
- ioco is the only implementation relation in the code: `data ImpRel = IOCO -- or IocoDelta -- ioco without quiescence; not implemented yet -- or IocoTick -- ioco with clock tick`; `"param_ImpRel" … -- implementation relation; currently only IOCO`. Simulator input completion defaults to `ANGELIC`. (C, source) — [ParamCore.hs](https://github.com/TorXakis/torxakis/blob/develop/sys/coreenv/src/ParamCore.hs), read from an anonymous shallow clone
- Status: the latest commit on `develop` is fe920cd, 2025-06-20, "Updates Haskell LTS version to 18.28 (#977)". The CHANGELOG's latest entry is v0.9.0 (LPE operations, bug fixes). (C) — [CHANGELOG](https://github.com/TorXakis/torxakis/blob/develop/CHANGELOG.md)
- TorXakis was used to re-test Dropbox (Tretmans & van de Laar, CECIIS 2019). It "provides limited support for internal nondeterminism … enumerates all possible values of internally generated data, until finding a corresponding case that matches the tester's observation". (A-pre, a peer's description) — [arXiv 2102.00378](https://arxiv.org/pdf/2102.00378)

### Inferences
- *Inference:* TorXakis is the reference ioco tool, but its process-algebra input (LOTOS-like) and its limited handling of internal nondeterminism make it a weak fit for specifying the running example's environment. It is evidence for the theory, not for industrial scale.

### Gaps
- The CECIIS 2019 paper and the GitHub releases page were not read (GitHub web and API returned 403 to curl). No industrial defect or effort data was found.

## Q8. Spec Explorer: published industrial data

### Takeaway
Only Grieskamp's own 2008 slides (C) were reachable. They give programme scale and staffing but no defect yield or effort per protocol. The STVR 2011 and CACM 2011 full texts were unreachable, so the "works and scales" quote and any measured MBT-versus-traditional comparison remain unverified.

### Cited Findings
- "250+ protocols in Windows alone (~ 30,000 pages of documentation)". "Current investment ~280 vendor employees for parser and test suite development ~50 Microsoft employees for management and tools infrastructure". Vendors in India and China do clean-room test-suite development. (C) — [Grieskamp, SambaXP 2008 slides](https://sambaxp.org/archive_data/sxp08/SambaXP2008-DATA/00-05-Wolfgang_Grieskamp-MBT.pdf)
- Method on the slides: requirements are gathered "from spec alone"; "Any ambiguity or clarity issue filed as TDI"; "Windows-specific behavior listed as separate requirements"; the requirement spec is the input to model design. An adapter interface separates test control (methods) from observation (events), with pluggable adapters for different server setups and transports. (C) — same slides

### Inferences
- *Inference:* "Windows-specific behavior listed as separate requirements" is a documented industrial instance of keeping per-reality detail apart from the base contract (P3). It is C-grade and comes with no outcome data.
- *Inference:* the adapter split (methods = control, events = observation) is the MBT counterpart of naming the observers at the boundary.

### Gaps
- No defects-found, person-years or MBT-versus-manual productivity figures could be read from a full text (cacm.acm.org 403, ri.conicet.gov.ar timeout, mincyt.gob.ar reset, eweek.com 403).

## Q9. Disconfirming search (b), partial: controlled studies of spec formats for human comprehension or defects

### Takeaway
I found no controlled study comparing EARS, prose, Gherkin and tables for human comprehension or defect rates. What exists either studies one notation with no comparison arm, or varies defects within prose. The report's statement that no format comparison exists survives for humans as well. I came across no LLM study in this pass.

### Cited Findings
- Salari, Enoiu, Afzal, Seceleanu (Mälardalen): "a controlled experiment that asks the participants to write 3 given requirements using EARS syntax". There were 10 subjects: four industrial engineers and six researchers and managers. The study observes which patterns people chose and the difficulties they met, with no prose or table control arm. (A-weak, small n) — [MDH PDF](https://www.ipr.mdu.se/pdf_publications/6673.pdf)
- Frattini et al. (EMSE, arXiv 2401.01154): a controlled experiment with 25 participants who built domain models from four natural-language requirements. "the use of passive voice only has a minor impact … ambiguous pronouns … shows a strong effect … ambiguous pronouns lead to incorrect associations in domain models". This varies defects within prose, not formats. (A) — [arXiv 2401.01154](https://arxiv.org/pdf/2401.01154v2)
- Mund, Femmer, Méndez Fernández, Eckhardt (2017): survey plus controlled experiment on whether SRS quality defects matter. "defects hampering the pragmatic quality do not seem to be as relevant as initially thought". This is about defects, not formats. (A) — [arXiv 1702.07656](https://arxiv.org/pdf/1702.07656)
- Leads seen only in search extracts, not verified and not counted: two experiments on SysML requirement diagrams (87 participants) reporting better comprehension with diagrams, and an experiment comparing natural language with activity diagrams.

### Inferences
- *Inference:* Frattini's strong effect of ambiguous pronouns sits beside Femmer's lowest precision for the vague-pronoun smell (0.26). The defect class that matters most to readers is the one that is hardest to detect mechanically in prose.

### Gaps
- The SysML-diagram and activity-diagram experiments were not fetched. No table-versus-prose experiment was found.

## Q10. Effect on the Kernsatz, form rule, scorecard and shortlist

### Takeaway
Nothing here overturns the Kernsatz, the quantifier-based form rule, or the shortlist. One Kernsatz clause has to be reworded (Cedar). The cost baseline changes (14 % → 12–13 %). The "sets of outcomes" design for faults has to be marked as inference with a known cost, because the main source did the opposite.

### Cited Findings
- **Kernsatz (l. 3), restyle with a factual correction.** "found crash and concurrency bugs at AWS ShardStore and Cedar" should read: crash-consistency and concurrency bugs at ShardStore; validator-soundness, parser and evaluator divergences at Cedar. — [ShardStore](https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf); [Cedar](https://arxiv.org/pdf/2407.01688)
- **Form rule (§ 2.3), unchanged.** The ShardStore principle it cites is confirmed in substance; only the quotation needs exact wording (T3-16).
- **Scorecard row e (l. 433) and § 7.3 cost baseline (l. 528), corrected figures.**
  - Use "12–13 % of code base, ≈ 20 % of implementation, models ≈ 1 %" instead of ≈ 14 %.
  - Row e's "● all three, with sets of outcomes" claims more than ShardStore shows. ShardStore relaxed equivalence after faults and did not check concurrent crashing executions. That combination is the running example's hardest case.
- **§ 5 recipe, unchanged as inference.** Annotate the "sets of allowed outcomes" step: ShardStore found full state-set tracking "blows up quickly in the face of multiple failures" and used a "has failed" relaxation with a never-wrong-data invariant.
- **Restyled only (no change of conclusion):**
  - Cedar venue → FSE Companion '24.
  - Barr "puts ahead" → "classifies".
  - ioco citation → Tretmans 2008.
  - ShardStore quote "we can still miss bugs" → the exact § 8.3 wording.
  - "2–10×" → "3–10×".
  - Darlington "requirements and code" → "requirements and design" (per the 2001 paper).
  - Drop † on Femmer, Barr and the ShardStore mechanism details (now verified).
- **Grades.**
  - SCR sources cited as A are NRL technical reports (B/C) and could not be read. The A for tables should rest on Darlington/PVS (Lawford et al.) or on the TOSEM 1996 paper, which was not reached.
  - Spec Explorer scale evidence currently stands at C (slides). The A-graded STVR quote is unverified.
  - The "250 person-years" figure is unsupported and should be dropped or kept at D.

### Inferences
- *Inference:* table completeness and disjointness checking (SCR, PVS COND obligations) is confirmed in mechanism by two independent sources. The shortlist's reliance on it is unaffected, even though the cited DTIC reports could not be read.

### Gaps
- See Q1 Gaps for every source that could not be reached.
