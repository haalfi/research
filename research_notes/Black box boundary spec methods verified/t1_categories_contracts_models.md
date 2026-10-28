# T1 verification: categories, levels and forms (§ 1, § 2.1–2.4), contract languages (§ 3.1), model-oriented methods (§ 3.2), lifecycle methods (§ 3.3)

Method note. Every verdict below comes from a full text (or, for API docs, the full page) downloaded this session with curl into `/tmp/claude-0/-home-user-research/6eb654f9-be93-5692-960f-f1941dafeecc/scratchpad/dl_t1/` and read as text (pdftotext, or HTML stripped by `python3 -I`). There are two exceptions, both marked: the Zave page (curl connection reset; read through WebFetch, which returns a model summary) and Wing 1990 (a scanned PDF with no text layer; pages rendered as images and read). Where a host failed I tried alternate copies first. "Unverifiable" means every copy I tried failed; no verdict rests on search extracts. Grades follow the brief: A peer-reviewed or measured, B documented industrial practice with data (the report also files normative standards and official docs under B), C practitioner report without data, D opinion or marketing. *Inference* marks my own reasoning.

Hosts that failed this session (each one tried more than once):
- cs.ucf.edu: TLS "self-signed certificate in certificate chain"; WebFetch returned 503. This blocks the Larch FAQ and JML RM ch. 9.
- cs.utexas.edu and cis.upenn.edu: TLS "unable to get local issuer". Alternate copies worked.
- web.archive.org: connection reset.
- pamelazave.com: connection reset (read through WebFetch).
- procon.bg: 503.
- apps.dtic.mil: 403.
- nowpublishers.com: 403 (Burckhardt read from MSR instead).
- hub.hku.hk: 403.
- dblp.org: 202 Anubis bot challenge.
- opus.bibliothek.uni-augsburg.de: reset (LMCS version used instead).
- researchgate.net: 403.
- sciencedirect.com: 403.
- iso.org: 403.
- event-b.org: self-signed certificate.
- kluedo.ub.rptu.de: reset.

---

## Q1. Which claims in § 1, § 2.1–2.4 and § 3.1–3.3 survive the full texts?

### Takeaway
The core claims survive. Problems found:
- **One citation is wrong:** the "Parnas–Madey" record is a 2010 Parnas-only chapter.
- **One figure is wrong:** ShardStore's "about 14% of the codebase" is not in the paper.
- **One quotation is misworded:** ShardStore's principle is paraphrased inside quote marks.
- **Two claims are attributed to the wrong page:** Jepsen `:info` is not in the README, and Hadoop's `open()` MUST is in `filesystem.html`, not `openfile.html`.
- **One claim is overgeneralised:** "every major kernel closes unconditionally".
- **One grade conflict needs restating:** the JML frame default differs between manual editions, not between the manual and slides.
- **Several grades are too high:** an OMG issue-tracker entry, a NetBSD bug report and a JML tech report are graded as if they were standards or peer-reviewed papers.

None of this touches the quantifier rule or the categories.

### Cited Findings

Verification table. "Line" refers to `reports/Black box boundary spec methods.md` as checked out.

| ID | Report location | Claim (short) | Source URL actually read | Verdict | Correction / quote |
|---|---|---|---|---|---|
| T1-01 | § 0 / Kernsatz para, l. 3; § 8.2 | Selection frameworks cover elicitation and have "little validation" (Carrizo et al., WER 2008, A) | https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf | confirmed, with nuance | The paper is "Study of Elicitation Techniques Adequacy" (Carrizo, Dieste, Juristo; 11th WER). "Little validation" refers to *earlier* frameworks: "Maiden and Rugg [10] and Davis and Hickey [27] … propose theoretical frameworks … However, there has been little validation of these proposals and their practical application is not evident." Carrizo et al. then propose their own framework, built from the literature. Grade A is acceptable (peer-reviewed workshop), but it is a literature-derived framework, not a measured study. |
| T1-02 | § 2.1 l. 21; § 8.2 | Parnas–Madey four-variable model, REQ/NAT/IN/OUT, monitored/controlled ([McMaster record](https://experts.mcmaster.ca/scholarly-works/2169098), A) | https://experts.mcmaster.ca/scholarly-works/2169098 | **corrected (wrong citation)** | Record 2169098 is **D. L. Parnas (sole author), "From requirements to architecture", *Frontiers in AI and Applications* vol. 217, pp. 3–36, 2010** (DOI 10.3233/978-1-60750-629-4-3). Its abstract does mention "A description of a four-variable model that is practical for software requirements documentation", but it mentions neither REQ/NAT/IN/OUT nor monitored/controlled. The intended source, Parnas & Madey, *Sci. Comput. Program.* 25 (1995), is **unverifiable: full text unreachable** (sciencedirect.com 403; NRL overview on apps.dtic.mil 403). There is secondary support for monitored/controlled variables in the A-7 model: NASA-GB-001-97 says the A-7 model "differentiates inputs, outputs, and state values by explicitly identifying monitored, control, and state variables" (https://ntrs.nasa.gov/api/citations/19980227975/downloads/19980227975.pdf). |
| T1-03 | § 2.1 l. 21; § 8.2 | Zave–Jackson: requirements describe the environment ([Zave FRE page](https://pamelazave.com/fre.html), A) | https://pamelazave.com/fre.html (WebFetch; curl reset) | confirmed (page summary only) | The page says "when it comes to requirements, the environment is not the most important thing--it is the *only* thing." It is the author's summary page, not the TOSEM paper; the A grade belongs to the paper, which was not read. The S, K ⊢ R relation is **not on the page**. Jackson states the equivalent in a full text: "machine specification ∧ domain properties ⇒ requirement" ([Jackson, Problem Analysis and Structure, Marktoberdorf 2000](https://stuff.mit.edu/afs/sipb/user/golem/papers/898/mj-marktoberdorf.pdf)). |
| T1-04 | § 2.1 l. 22; § 3.1 l. 164; § 8.2 | Larch two tiers: a state-free shared tier and a per-language interface tier of "first-order predicates over two states" ([Larch FAQ](https://www.cs.ucf.edu/~leavens/larch-faq.html); SRC RR-58, A/B) | https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf | confirmed (two-tier); FAQ wording unverifiable | RR-58: "Each Larch specification has components written in two languages: one that is designed for a specific programming language and another that is independent of any programming language." Interface languages deal "with what can be observed about the behavior of components", including "exception handling". The CLU example states an error case inline: `ensures v_post = addW(...) except when w ∈ v signals duplicate ensures v_post = v`. The FAQ wording "predicates over two states" is **unverifiable: full text unreachable** (cs.ucf.edu TLS chain error; WebFetch 503; web.archive.org reset). Grade: RR-58 is a DEC SRC tech report and the official language report. By the report's own convention that is B; it is not A. |
| T1-05 | § 2.1 l. 22 (†) | TLA+ open specifications and Event-B refinement split state from time | Abadi–Lamport Composing page and Conjoining PDF (T1-06); https://wiki.event-b.org/index.php/Event-B_Language | TLA+ part confirmed; Event-B part unverifiable | The TLA+ open specification "is simply E implies M" (T1-06). For Event-B, the wiki page is only an index; the event-b.org sample chapters and Rodin handbook failed (self-signed certificate). **Unverifiable: full text unreachable (event-b.org, TLS).** Keep the †. |
| T1-06 | § 2.1 l. 24; § 1 | Assume–guarantee puts E in one place ([Abadi & Lamport, Composing](https://www.microsoft.com/en-us/research/publication/composing-specifications/), A) | https://www.microsoft.com/en-us/research/publication/composing-specifications/ | confirmed | Lamport's note on the publication page: "The specification is simply E implies M, where E specifies what we assume of the environment and M specifies what the system guarantees." |
| T1-07 | § 2.1 l. 24 | I/O automata treat environment inputs as always enabled ([Lynch retrospective](https://arxiv.org/pdf/2502.20468), A) | https://arxiv.org/pdf/2502.20468 | confirmed | "I/O Automata are input-enabled, which means that any input action may occur from any automaton state, in other words, an automaton cannot block its inputs." The document is a 2025 arXiv retrospective by Lynch. The peer-reviewed sources are the original I/O-automata papers; A is acceptable as an author account, but it is not peer-reviewed itself (strictly A-pre). |
| T1-08 | § 2.1 l. 24 | P closes systems with environment "ghost machines" ([Desai et al., PLDI 2013](https://www.microsoft.com/en-us/research/publication/p-safe-asynchronous-event-driven-programming-2/), A) | https://microsoft.com/en-us/research/wp-content/uploads/2016/02/pldi212_desai.pdf | confirmed | "The environment is composed of ghost machines which are used only during verification"; "Ghost machines are erased during compilation to executable code". |
| T1-09 | § 2.1 table K1 (†) | ASM/Event-B state space as the precedent for K1 | Börger ground-model paper: three guessed unipi.it URLs (404) | unverifiable: full text unreachable | No open copy found. Keep the †. |
| T1-10 | § 2.1 table K2; § 2.2 l. 65; § 8.2 | Parnas tables at Darlington ([Lawford & Wassyng](https://procon.bg/system/files/28.18_Lawford_Wassyng.pdf), A) | procon.bg (503, twice); alternate https://www.cas.mcmaster.ca/~lawford/papers/tables.pdf | cited copy unverifiable; claim confirmed in an alternate primary | Lawford, Froebel & Moum, "Application of Tabular Methods to the Specification and Verification of a Nuclear Reactor Shutdown System" (2001) describes the Darlington SDS Redesign: tabular methods with PVS, which "automatically generate Disjointness and Completeness" proof obligations ("Disjointness: requires that the columns (rows) do not overlap … Completeness: requires that at least one column (row) is applicable to every …"). Its remark about "reverse engineering of existing requirements documents into the chosen formalism" describes *other* industrial applications, not Darlington. The notes' claim that the original Darlington project "had to reverse-engineer tabular specs" stays unverified (it rests on the unread Lawford & Wassyng). |
| T1-11 | § 2.1 table K3; § 3.1 l. 162 | JML `normal_behavior`/`exceptional_behavior`, `signals_only`, `assignable` ([JML RM ch. 9](https://www.cs.ucf.edu/~leavens/JML/jmlrefman/jmlrefman_9.html), B) | Cited page unreachable (cs.ucf.edu TLS). Read instead: https://www.openjml.org/documentation/JML_Reference_Manual.pdf (2nd ed. draft, Cok, Leavens, Ulbrich, 29 Apr 2026) and JML TR 98-06j (https://dr.lib.iastate.edu/server/api/core/bitstreams/72cd0b58-b6f9-4094-af5a-50fab5251960/content) | confirmed against the 2nd-edition draft | 2nd ed.: a `normal_behavior` "is a shorthand for a behavior that contains the clauses: signals (Exception e) false; signals_only \nothing;". An `exceptional_behavior` "may not contain an <ensures-clause>. It is a shorthand for a behavior that contains the clause ensures false;". **Correction to the notes:** "The default <signals-only-clause> lists all the exceptions that are in the Java method declaration's throws clause **plus java.lang.RuntimeException**." |
| T1-12 | § 3.1 l. 162 | "The sources conflict on JML's frame default, and the manual is preferred" | Same two JML texts | **corrected (conflict restated)** | The conflict is **between JML versions**, not between the manual and the slides. TR 98-06j (2000): "in a non-lightweight specification … the meaning of an omitted modifiable clause is that nothing can be modified" (`\nothing`; "very strict, as even benevolent side effects are disallowed"). 2nd-ed. draft (2026): "the default specification of a method also includes assignable \everything". So the current manual does use `\everything` for default specs. Also of note: JML has an explicit `\not_specified` value for omitted clauses in lightweight specs, a published precedent for brief § 3.2 ("unspecified is a statement"). |
| T1-13 | § 2.1 table K4; § 3.3 l. 185; § 8.2 | Typestate detects "syntactically legal but semantically undefined execution sequences" ([DBLP](https://dblp.org/pid/41/5885), A) | DBLP returned an Anubis challenge (202). Read instead: https://research.ibm.com/publications/typestate-a-programming-language-concept-for-enhancing-software-reliability | confirmed (quote verbatim) | The abstract: "Typestate tracking … enhances program reliability by detecting at compile-time syntactically legal but semantically undefined execution sequences. These include … reading a variable before it has been initialized, dereferencing a pointer after the dynamic object has been deallocated". Cite the IBM page or the TSE DOI, not DBLP. |
| T1-14 | § 2.1 table K4; § 3.3 l. 187; § 8.2 | UML protocol state machines attach a guard, trigger and postcondition per transition; protocol states need not match internal states ([OMG UML14-209](https://issues.omg.org/issues/UML14-209), B) | https://issues.omg.org/issues/UML14-209 | second half confirmed; first half not found in this source; **grade too high** | The issue (by Conrad Bock, NIST; closed) says: "Protocol machines are a client-side view, independent of the internal behavior machine of the instance. This means the protocol states are not necessarily the same as the internal states". It quotes the spec: pre/post conditions "are expressed at the operation level, and therefore do not provide a synthetic overview at the classifier level". The guard/trigger/postcondition anatomy is **not stated** in this issue; it would need the UML spec itself. Grade: an issue-tracker entry is a C, not a normative B. |
| T1-15 | § 2.1 table K5 | Jepsen nemesis ([Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md), C) | Same URL | confirmed | "a special *nemesis* process introduces faults into the system". |
| T1-16 | § 2.1 table K6 | Linearizability, session guarantees, client-centric isolation (A) | https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf; https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf; https://par.nsf.gov/biblio/10077635 | confirmed (as precedents) | Herlihy & Wing: "A sequential specification for an object is a prefix-closed set of …"; histories "are linearizable with respect to some sequential specification". Terry et al. define "Read Your Writes, Monotonic Reads, Writes Follow Reads, and Monotonic Writes". For Crooks et al., only the bibliographic record was read (PODC 2017, pp. 73–82): no definitions checked. Keep "(definitions †)". |
| T1-17 | § 2.1 table K7 | Error categories defined by the caller's recovery action ([gRPC](https://grpc.io/docs/guides/status-codes/), B) | https://grpc.io/docs/guides/status-codes/ | confirmed | "(a) Use UNAVAILABLE if the client can retry just the failing call. (b) Use ABORTED if the client should retry at a higher level … (c) Use FAILED_PRECONDITION if the client should not retry until the system state has been explicitly fixed." Spec# offers a stronger published precedent (gap section Q3). |
| T1-18 | § 2.1 table K7 | Rust `ErrorKind` as an extensible set (B) | https://doc.rust-lang.org/nightly/std/io/enum.ErrorKind.html | confirmed | `#[non_exhaustive] pub enum ErrorKind`; "Non-exhaustive enums could have additional variants added in future." |
| T1-19 | § 2.1 table K8 | POSIX option constants as profile values (B) | https://www.gaertner.de/~neitzel/susv3/basedefs/unistd.h.html | confirmed | "If a symbolic constant is defined with the value -1, the option is not supported. … If a symbolic constant is defined with a value greater than zero, the option shall always be supported". Runtime query via `sysconf()` etc. |
| T1-20 | § 2.1 table K8 | W3C variability dimensions (B) | https://www.w3.org/TR/spec-variability/ | confirmed | "seven dimensions of variability", including "Discretionary items - Deliberate and explicit grants of discretion by the specification to the implementations … error handling, etc." It is a W3C Note: normative guidance, not data. B by the report's convention. |
| T1-21 | § 2.1 table K8 | Hadoop contract XML as a profile (B) | https://hadoop.apache.org/docs/r3.1.2/hadoop-project-dist/hadoop-common/filesystem/testing.html | confirmed | "driven entirely by a Hadoop XML configuration file … such as contract/localfs.xml. Having the XML file define all FileSystem options makes the listing of FileSystem behaviors immediately visible." For example, `ContractOptions.IS_CASE_SENSITIVE` and `SUPPORTS_UNIX_PERMISSIONS`. |
| T1-22 | § 2.1 l. 48 | Four strengths of non-commitment, "C11 § 3.4 as quoted by WG23 N0245" (B) | https://www.open-std.org/JTC1/SC22/WG23/docs/ISO-IECJTC1-SC22-WG23_N0245-revised-c-langague-annex-2010-03-23.pdf; https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf | **corrected (source wording)** | N0245 **paraphrases**; it does not quote § 3.4. Its definition of implementation-defined behaviour also **omits the documentation duty**: "unspecified behaviour where the resulting behaviour is chosen by the implementation". Cite C11 itself (N1570 draft): § 3.4.1 implementation-defined behavior "unspecified behavior where each implementation documents how the choice is made"; § 3.4.3 undefined behavior "…for which this International Standard imposes no requirements"; § 3.4.4 unspecified behavior "…provides two or more possibilities and imposes no further requirements on which is chosen in any instance". Note that C11 § 3.19.2 already uses "indeterminate value" ("either an unspecified value or a trap representation"), a *different* meaning from the report's "indeterminate" outcome. |
| T1-23 | § 2.1 l. 48 | RFC 2119 MAY = optional, with a duty to interoperate (B) | https://www.rfc-editor.org/rfc/rfc2119.txt | confirmed | "MAY … mean that an item is truly optional. One vendor may choose to include the item … An implementation which does not include a particular option MUST be prepared to interoperate with another implementation which does include the option, though perhaps with reduced functionality." |
| T1-24 | § 2.1 l. 52 | "indeterminate" = Jepsen's `:info` ([Jepsen README](https://cdn.jsdelivr.net/gh/jepsen-io/jepsen@main/README.md), C) | README (no `:info`); https://raw.githubusercontent.com/jepsen-io/jepsen/main/doc/tutorial/03-client.md | **not found in cited source; confirmed elsewhere** | The README never mentions `:info`. The official tutorial does: "type `:ok` if the operation succeeded, `:fail` if it didn't take place, or `:info` if we're not sure"; "Jepsen will interpret the exception as an indeterminate `:info` result, and allow that it might or might not have taken place." Re-cite to the tutorial (C). |
| T1-25 | § 2.1 l. 53 | PEP 3116: "may return a short read without any particular reason" as the precedent for "deliberately not promised" (B) | https://peps.python.org/pep-3116/ | confirmed verbatim, **context narrows it** | The full sentence: "raw reads may return a short read without any particular reason; buffered reads will only return a short read if EOF is reached; and raw writes may return a short count …, while buffered writes will raise IOError when not all bytes could be written or buffered." So the non-promise applies to the **raw** layer only. The buffered layer *does* promise. The precedent stands, but it is per-layer. |
| T1-26 | § 2.1 l. 55 | Python prefers a defined error for use-after-close ([CPython iobase.c](https://chromium.googlesource.com/external/github.com/python/cpython/+/39f6a0489fcc815a578d27dfee2feea003c896f8/Modules/_io/iobase.c), B) | Same file (gitiles `?format=TEXT`, base64-decoded) | confirmed | `PyErr_SetString(PyExc_ValueError, "I/O operation on closed file.");` (two sites). The Java half of the sentence is not supported by this citation (see T1-41 for CME). |
| T1-27 | § 2.2 l. 61 | ShardStore: 16 issues prevented; "spec and harness about 14% of the codebase" (A) | https://cdn.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf (cs.utexas.edu TLS failed) | 16 confirmed; **14% corrected** | "Our work has prevented 16 issues from reaching production, including subtle crash consistency and concurrency problems". Figure 6 (lines of Rust): implementation 44,048; unit and integration tests 19,540; **reference models 450**; functional correctness checks 4,860; crash consistency checks 2,661; concurrency checks 901; total 72,460. Spec plus validation = 8,872 lines, which is **12.2% of all code** (or ≈20% relative to the implementation). The reference models alone are ≈1% of the implementation. Also: "18% of the total reference model and test harness code has been written by the engineering team". No 14% figure appears. |
| T1-28 | § 2.2 l. 62 | Cedar: 4 bugs found by proof, 21 by DRT/PBT (A) | https://arxiv.org/pdf/2407.01688 | confirmed | "While carrying out proofs, we found and fixed 4 bugs in Cedar's policy validator, and DRT and PBT helped us find and fix 21 additional bugs in various parts of Cedar." Venue: FSE Companion 2024, DOI 10.1145/3663529.3663854. "Millions of inputs" also confirmed. |
| T1-29 | § 2.2 l. 63; matrix K6 | AWS TLA+: 10 systems, 2–3 weeks to learn (B) | https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf | confirmed; **edition note** | "So far we have used TLA+ on 10 large complex real-world systems. In every case TLA+ has added significant value …"; "learn TLA+ from scratch and get useful results in 2 to 3 weeks". The MIT-hosted file is the **29 Sept 2014** version, not the CACM 2015 text; label it accordingly. It also says "We now have 7 teams using TLA+". |
| T1-30 | § 2.2 l. 64 | AUTOSAR QuickCheck: more than 3,000 pages, more than 200 issues (A/B) | https://research.chalmers.se/en/publication/219899 | confirmed (abstract only) | "We translated over 3000 pages of textual specifications into QuickCheck models … This exposed over 200 issues … Compared to an earlier manual approach, ours is more efficient, more effective, and more …". The full paper was not linked from the record. The counts are self-reported. |
| T1-31 | § 2.2 l. 65; § 8.2 | Heitmeyer & Labaw: reviewers spent effort on application-independent checks (A) | https://apps.dtic.mil/sti/pdfs/ADA276077.pdf | **unverifiable: full text unreachable (apps.dtic.mil, 403)** | The citeseerx alternate also failed. |
| T1-32 | § 2.2 matrix K2 | PBT idioms; generators are hard ([Goldstein et al.](https://cis.upenn.edu/~bcpierce/papers/icse24-pbt-in-practice), A) | https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf (upenn TLS failed) | confirmed | "data from 30 in-depth interviews with experienced users of PBT at Jane Street"; "most uses fall into a relatively small number of high-leverage idioms"; generators "can be nontrivial to write"; participants report "struggling to generate distributions of test" inputs. |
| T1-33 | § 2.2 matrix K6 | Prose ambiguity at Cosmos DB (A/B) | https://arxiv.org/pdf/2210.13661 | confirmed | Behaviours "were previously poorly understood outside of the Cosmos DB development team, even informally, leading to data consistency errors in Microsoft products"; "we were able to raise two key issues in Cosmos DB's public-facing documentation"; "the 2 person-month development process". ICSE-SEIP 2023, so A. |
| T1-34 | § 2.2 matrix K6 | History checking is NP-complete in general; Elle is polynomial for isolation (A) | https://arxiv.org/pdf/2003.10554 | confirmed | "Serializability checking is also (in general) NP-complete"; Knossos "remains fundamentally NP-complete"; for Adya-style anomalies "we can check these properties in linear time … cycle detection is solvable in O(vertices + edges) time". |
| T1-35 | § 2.2 l. 78 | Mechanised Wasm semantics found real errors in the prose spec (A); SQLite (B) | https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf; https://spiral.imperial.ac.uk/entities/publication/ecf384fa-0800-4dc3-b5ef-a5aac822610e; https://sqlite.org/testing.html | confirmed | Watt: errors in the official specification "which were acknowledged"; "identified and assisted in fixing several errors in the official" spec. Imperial record: "discovered and helped fix several errors in the WebAssembly specification". SQLite testing.html: "590 times as much test code and test scripts" (outside this track's section, but now confirmed). |
| T1-36 | § 2.3 l. 82 | ShardStore principle, given in quotes: "decompose correctness into independent properties, check each with the most suitable tool, use executable reference models as the specification" | ShardStore PDF (T1-27) | **corrected (wording)** | Actual text: "Our approach decomposes correctness into independent properties, each checked by the most appropriate tool, and develops executable reference models as specifications to be checked against the implementation." Either quote this exactly or drop the quote marks. |
| T1-37 | § 2.3 l. 115 | Burckhardt: unbounded eventual visibility is the standard claim that no finite history can refute (A) | https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/final-printversion-10-5-14.pdf (nowpublishers 403) | confirmed in substance; "standard example" is inference | Def. 5.1: a completed operation e must eventually become visible; "almost all operations that start after e has returned (i.e. all but finitely many) must see e." Def. 7.12: a safety property's "membership can always be refuted by a finite prefix"; a liveness property holds if "any finite execution can be extended to an execution that satisfies the property". The book does not call eventual visibility "the standard example". |
| T1-38 | § 2.4 l. 123 | ioco judges conformance on traces, including quiescence δ ([arXiv 1403.7260](https://arxiv.org/pdf/1403.7260), A) | Same URL | confirmed; secondary for ioco | "δ is the special action label modeling quiescence". The paper is Beohar & Mousavi, "Spinal Test Suites for Software Product Lines" (an SPL paper), not an ioco primary. Tretmans would be the primary. A is acceptable (EPTCS workshop). |
| T1-39 | § 2.4 l. 123 | Consistency frameworks judge predicates over histories ([Viotti & Vukolić](https://arxiv.org/pdf/1512.00168), A) | Same URL | confirmed | "we adopt the notion of history, i.e., the set of operations of a given execution … abstract executions augment histories with orderings". |
| T1-40 | § 2.4 l. 125 | AugmenTest: an assertion must pass on the original and fail on a mutant (A-pre) | https://arxiv.org/html/2501.17461v1 | confirmed | "If the test passes on the original class but fails on the buggy we consider the assertion to be a correct one (a true positive)." Still cited as arXiv v1, so A-pre stays (track T5 owns publication status). |
| T1-41 | § 2.4 l. 128 | Abadi–Lamport "M holds one step longer than E", to forbid contracts that a later environment violation could excuse (A) | https://microsoft.com/en-us/research/uploads/prod/2016/12/Conjoining-Specifications.pdf | confirmed; motive slightly restated | TOPLAS 17(3), 1995: "we interpret the specification that M is guaranteed under assumption E as the formula E −+▷ M, which means that M holds at least one step longer than E does"; "the guarantee M can become false only after the assumption E becomes false". The Composing page states the motive: E ⇒ M "allows behaviors in which the system violates its guarantee and the environment later violates its assumption–behaviors that no correct implementation could allow". The paper's own use is sound circular composition. The report's gloss is fair. |
| T1-42 | § 2.4 l. 134–135 | Hadoop: `open()` MUST check existence; `openFile()` MAY defer to first `read()` ([openfile.html](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/filesystem/openfile.html), B) | openfile.html; https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/filesystem/filesystem.html | confirmed; **source split** | The `open()` MUST is in **filesystem.html**, not openfile.html: "Implementations MUST check for the presence of the file at the time of creation. This does not imply that the file and its data is still at the time of the following read()". openfile.html: "The returned stream MAY implement a lazy open where file non-existence or access permission failures may not surface until the first read()". It adds that file-specific preconditions "MUST NOT be checked here" in `openFile()` itself. filesystem.html also says that whether the stream sees later changes "is an implementation detail" (relevant to K6). |
| T1-43 | § 2.4 l. 144 | `Closeable` versus `AutoCloseable` idempotence (B) | https://cs-214.epfl.ch/jdk-21.0.9-docs/api/java.base/java/lang/AutoCloseable.html | confirmed | "unlike the close method of Closeable, this close method is not required to be idempotent … implementers of this interface are strongly encouraged to make their close methods idempotent." |
| T1-44 | § 2.4 l. 145 | Use-after-close or concurrent modification detected best-effort ([CME Javadoc](https://cr.openjdk.org/~alanb/sc-jdk26/api/java.base/java/util/ConcurrentModificationException.html), B) | Same URL | confirmed | "Fail-fast operations throw ConcurrentModificationException on a best-effort basis. Therefore, it would be wrong to write a program that depended on this exception for its correctness". |
| T1-45 | § 2.4 l. 147 | Metamorphic relations need no full oracle ([Chen et al.](https://hub.hku.hk/handle/10722/254895), A) | hub.hku.hk 403; alternate https://arxiv.org/abs/2002.12543 | confirmed via the original MT report | Chen, Cheung & Yiu (HKUST TR 1998, posted to arXiv 2020): the technique "can be used in the absence of test oracles". The cited HKU record (presumably the CSUR 2018 review) was unreachable. |
| T1-46 | § 3.1 l. 161 | Meyer built components on "carefully designed contracts" (A, conceptual) | https://www.kth.se/social/files/59526bfb56be5b4f17000807/meyer-92-contracts.pdf | confirmed | Sidebar: "This article shows how to reduce bugs by building software components on the basis of carefully designed contracts." Reliability is "the combination of correctness and robustness". IEEE Computer 1992 is a magazine article without data. "A (conceptual)" is generous; the rubric's A means peer-reviewed *or measured*. |
| T1-47 | § 3.1 l. 161 | Eiffel: a routine fulfils its contract or fails into its caller (B) | https://www.eiffel.org/doc/solutions/Exception_Mechanism | confirmed | "It can return the instance to a stable state and retry the entire routine … It can fail, causing an exception in its caller"; "If the rescue clause exits without issuing a retry instruction, then the routine fails." Also: "Out of the approximately 2000 classes in the delivered Eiffel libraries, there are only 16 occurrences" of rescue/retry. |
| T1-48 | § 3.1 l. 162; § 8.2 | JML design paper ([Leavens et al.](https://dr.lib.iastate.edu/cs_techreports/136), A) | Same record plus its PDF bitstream | content confirmed; **citation and grade corrected** | The record is **TR #98-06j** (June 1998, revised to May 2000), not the 2006 SIGSOFT SEN paper. Abstract: JML "uses Eiffel-style assertion syntax combined with the model-based approach to specifications typified by VDM and Larch … supports quantifiers, specification-only variables, frame conditions". A tech report is not peer-reviewed: grade B or C, or cite the SEN 2006 version as A (not read). |
| T1-49 | § 3.1 l. 163 | Dafny `modifies`/`reads`, `old()`, `fresh()` (C) | https://dafny.org/v4.3.0/DafnyCheatsheet.pdf | confirmed | The cheatsheet lists `modifies …`, `reads …`, `old(o)`, `unchanged(o)`, `fresh(o)`. |
| T1-50 | § 3.2 l. 179 (†) | VDM-SL ext and errs, Z error schemas, B nondeterministic substitutions | See gap Q4 | **now confirmed from primary manuals** (VDM, Z, B); Event-B and ASM still unverifiable | Details and quotes in Q4. The † can be dropped for VDM, Z and B. |
| T1-51 | § 3.3 l. 186 | DeLine & Fähndrich: modular typestate for objects; aliasing via linear types (A) | https://www.microsoft.com/en-us/research/publication/typestates-for-objects/ | confirmed | "We handle aliasing by adapting our previous work on practical linear types developed in the context of the Vault system"; the model "permits subclasses to extend the interpretation of typestates". |
| T1-52 | § 3.3 l. 187 | Class contracts generated mechanically from PSMs ([UCC](https://research.ucc.ie/en/publications/generating-class-contracts-from-deterministic-uml-protocol-statem/), A) | Same URL | confirmed | Porres & Rauf (2010): "A generated class contract defines a pre- and post-condition for each operation that triggers a transition in the state machine … can be used as a behavioral interface, for documentation, run-time checking and test case generation." |
| T1-53 | § 3.3 l. 188 | Session types type a protocol (A) | https://www.etaps.org/2019/test-of-time-award | confirmed | "Session types are type-theoretic specifications of communication protocols, allowing protocol implementations to be verified by static type-checking." An award page is a C-type page about an A paper. |
| T1-54 | § 3.3 l. 189 | Interface automata: input assumptions and output guarantees; alternating refinement (A) | https://research-explorer.ista.ac.at/record/4622 | confirmed | "both input assumptions about the order in which the methods of a component are called, and output guarantees …"; "one interface refines another if it has weaker input assumptions, and stronger output guarantees"; compatibility is optimistic, "if there is some environment that can make them work together". |
| T1-55 | § 3.3 l. 191; § 8.2 | Interface automata cannot *require* an output ([Lüttgen & Vogler TR 2012](https://opus.bibliothek.uni-augsburg.de/opus4/files/2006/TR_2012_09.pdf), A/C) | TR host reset; read instead the peer-reviewed version, https://arxiv.org/pdf/1306.3050v2 (LMCS 9(3:4), 2013) | confirmed; **upgrade to A** with the LMCS citation | "an output in a specification can always be ignored in an implementation. In particular, a component that consumes all inputs but never produces any output satisfies any interface." Same paper: modal transition systems "distinguish between may- and must-transitions and thus … express mandatory outputs" (IOMTS, Larsen, Nyman & Wąsowski). An existing mechanism for required outputs. |
| T1-56 | § 3.3 l. 195; § 8.2 | POSIX leaves the descriptor's state unspecified after an interrupted `close` (B); "every major kernel closes unconditionally" ([NetBSD PR 58929](https://gnats.netbsd.org/58929), B) | https://man.archlinux.org/man/close.3p.en; https://gnats.netbsd.org/58929 | first half confirmed; **second half corrected; grade lowered** | close(3p) (POSIX.1-2017 text): interrupted close "shall return -1 with errno set to [EINTR] and the state of fildes is unspecified"; the same for EIO. The PR reporter checked **five systems**: "On every OS I checked (NetBSD, FreeBSD, OpenBSD, Linux, illumos), … the descriptor is closed, unconditionally". macOS and Windows were not covered, so "every major kernel" overstates it. POSIX.1-2024 now makes the outcome unspecified among EINTR (open), EINPROGRESS (closed) or success, with `posix_close()`/`POSIX_CLOSE_RESTART`. A bug report is C, not B. |
| T1-57 | § 3.3 l. 196 | Rust drop-based close swallows close-time errors ([LWN](https://lwn.net/Articles/1009302), C; [async_fs](https://docs.rs/async-fs/1.1.2/async_fs/struct.File.html), B) | Both URLs | confirmed; **source type** | The LWN URL is a **reader comment** (by farnz, Feb 2025), not an LWN article. It says `std::fs::File` "closes itself on drop. But that means that it swallows errors". C at best. async_fs: "Files are automatically closed when they get dropped and any errors detected on closing are ignored. Use the sync_all() method before dropping". |
| T1-58 | § 3.1 grade line, l. ~175 | "No measured study of these methods on multi-backend library specs was found" | Estler et al. (gap Q5) | stands | Estler et al. 2014 is a measured study of contract *usage*, not of multi-backend specs. The statement stays true, but § 3.1 can now cite one measured A source (Q5). |

### Inferences
- *Inference:* None of the corrections changes a category, a level or the quantifier rule. They are citation hygiene, one wrong figure, and a few grades that were too high.
- *Inference:* T1-25 (PEP 3116 is per-layer) and T1-42 (Hadoop `open()` versus `openFile()` live in two different documents) both show that a "non-promise" or a deferred-error freedom often holds at one layer or entry point and not another. That supports the report's insistence on named variation points over prose.

### Gaps
- Unverifiable, full text unreachable: Parnas & Madey 1995 (sciencedirect 403, DTIC 403); Heitmeyer & Labaw (DTIC 403); Lawford & Wassyng ISIJ (procon.bg 503); Larch FAQ and JML RM ch. 9 (cs.ucf.edu TLS); Event-B chapters (event-b.org TLS); Börger ground model (no open copy found); Crooks et al. full text (only the NSF record read); AUTOSAR full paper (only the Chalmers abstract read).

---

## Q2. Do the § 8.2 grades for these sections fit the brief's rubric?

### Takeaway
Most fit. Five should move down and one up. The report's convention of grading official docs as B is applied to things that are not official docs.

### Cited Findings
- **OMG UML14-209: B → C.** It is an issue-tracker entry by one submitter, not the UML specification — [OMG](https://issues.omg.org/issues/UML14-209)
- **NetBSD PR 58929: B → C.** A bug report; its five-OS survey is one person's check — [NetBSD](https://gnats.netbsd.org/58929)
- **Leavens, Baker, Ruby record: A → B/C.** The linked item is tech report 98-06j, not the SEN paper — [Iowa State](https://dr.lib.iastate.edu/cs_techreports/136)
- **Larch FAQ / SRC RR-58: A/B → B.** Both are an official language report and FAQ, not peer-reviewed — [RR-58](https://ftp.mirrorservice.org/sites/www.bitsavers.org/pdf/dec/tech_reports/SRC-RR-58.pdf)
- **Parnas–Madey "record": A, but the link must change.** It points to a 2010 Parnas chapter — [McMaster](https://experts.mcmaster.ca/scholarly-works/2169098)
- **Lüttgen & Vogler: A/C → A** if re-cited to LMCS 9(3:4) 2013 — [arXiv 1306.3050](https://arxiv.org/pdf/1306.3050v2)
- **Lynch retrospective: A → A-pre** (strictly). It is an arXiv author retrospective — [arXiv 2502.20468](https://arxiv.org/pdf/2502.20468)
- **Newcombe et al. (B)** fits: an industrial report with counts. Label the MIT file as the 2014 version — [MIT copy](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf)
- **Carrizo et al. (A)** fits as a peer-reviewed workshop paper. Note that it is not a measured validation — [WER 2008](https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf)

### Inferences
- *Inference:* No grade change moves a C or D above an A or B claim in these sections. The changes do not alter which evidence carries the conclusions.

### Gaps
- Whether the Crooks and AUTOSAR full texts support the specific definitions and counts beyond their records stays open.

---

## Q3. Gap: how do ACSL, Spec# and .NET Code Contracts specify error and abnormal outcomes?

### Takeaway
There are three distinct published patterns:
- **ACSL**, for C without exceptions: errors are *named behaviors* over return values and `errno`, with checkable `complete behaviors` and `disjoint behaviors` clauses. `exits` covers only program termination.
- **Spec#**: exceptions form a *classification by who is at fault and whether the caller should recover*. Checked exceptions are admissible failures; unchecked exceptions are client failures or program errors. A `throws E ensures P` clause gives exceptional postconditions.
- **Code Contracts**: `EnsuresOnThrow<T>`. This is a postcondition-on-throw without a closed throws set.

### Cited Findings
- **ACSL behaviors (B, official manual v1.24).**
  - A behavior has `assumes`, and the semantics require `\old(Ai) ==> Ei`.
  - Completeness is optional and stated explicitly: `complete behaviors b1,…,bn;` "specifies that the set of behaviors … is complete i.e. that R && AR ==> (A1 || A2 || ... || An)".
  - Disjointness is also optional: `disjoint behaviors` means "for all distinct i and j, R && AR ==> ! (Ai && Aj)".
  - Source: [ACSL manual](https://frama-c.com/download/acsl.pdf)
- **ACSL error handling (B).**
  - "Since C has no exceptions, ACSL does not use exceptional specifications. Instead, C programmers typically signal errors by returning special values … it is sufficient to write an appropriate postcondition: ensures \result == error_value || normal_postcondition;"
  - The manual's `bsearch` example uses named behaviors `success` and `failure`.
  - Source: [ACSL manual, App. A.3](https://frama-c.com/download/acsl.pdf)
- **ACSL abrupt termination (B).**
  - "The ensures clause … does not constrain the post-state when the annotated function or statement terminates abruptly."
  - `exits E` covers termination of the program (e.g. `exit()`), with `\exit_status`.
  - Defaults: "Missing requires and ensures clauses default to \true. Missing exits clauses default to \false. If no assigns clause is given, it remains unspecified."
  - Source: [ACSL manual §§ 2.3.5, 2.10](https://frama-c.com/download/acsl.pdf)
- **Spec# exception classification (A, CASSIS 2004, LNCS).**
  - "A client failure occurs when a method is invoked under an illegal condition, that is, when the method's precondition is not satisfied. We further refine provider failures into admissible failures and observed program errors. An admissible failure occurs when a method is not able to complete its intended operation …"
  - "The set of admissible failures is part of the contract between callers and implementations."
  - "we expect correct programs to catch and handle admissible failures"; "Admissible failures are signaled with checked exceptions, whereas client failures and observed program errors are signaled using unchecked exceptions."
  - Source: [Barnett, Leino, Schulte, The Spec# Programming System: An Overview](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/TheSpecSharpProgrammingSystem28CASSIS200429.pdf)
- **Spec# exceptional postconditions (A).**
  - "Spec# allows a throws declaration to be combined with a postcondition that takes effect in the event that the exception is thrown", e.g. `throws EndOfFileException ensures a.Count == old(a.Count);`.
  - "A throws clause in Spec# can only mention checked exceptions."
  - The compiler enforces the throws set "by a conservative control-flow analysis".
  - `otherwise` clauses name the unchecked exception for a violated precondition.
  - Source: [same](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/TheSpecSharpProgrammingSystem28CASSIS200429.pdf)
- **.NET Code Contracts (B, official docs).**
  - `Contract.EnsuresOnThrow<TException>(bool)` "specifies a postcondition that is expected to be true when the enclosing method or property terminates abnormally and an exception of type TException is thrown"; "You must use the binary rewriter for run-time enforcement".
  - Guidance: "using the type Exception for T requires the method to guarantee the condition regardless of the type of exception that is thrown, even if it is a stack overflow … You should use exceptional postconditions only for specific exceptions".
  - Status: "Code contracts aren't supported in .NET 5+ (including .NET Core versions)."
  - Sources: [EnsuresOnThrow API](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.contracts.contract.ensuresonthrow); [Code Contracts overview](https://learn.microsoft.com/en-us/dotnet/framework/debug-trace-profile/code-contracts)
- The Code Contracts user manual PDF (raw.githubusercontent.com/microsoft/CodeContracts …/UserDoc.pdf) returned 404, so only the learn.microsoft.com pages were read.

### Inferences
- *Inference:* Spec#'s client / admissible / program-error split is a **published precedent for K7's "error categories defined by the caller's recovery action"**, and it is stronger than gRPC's because it is tied to the contract. The § 2.1 table could cite it.
- *Inference:* ACSL's `complete behaviors` / `disjoint behaviors` is a published, *machine-checked* form of exactly the case-split completeness and disjointness the report assigns to tables (K3, K7). It is evidence that this check does not require tabular notation; it is a property of a case split in any form.
- *Inference:* None of the three can state a failure that surfaces after the call returned. That confirms § 3.1's "Limits" paragraph.

### Gaps
- The Spec# CACM 2011 retrospective (krml196.pdf) was downloaded but not searched for usage figures. The full Code Contracts user manual was not found.

---

## Q4. Gap: how do VDM-SL, Z and B treat error handling?

### Takeaway
All three are now verified from primary manuals. Each of the three gives one error idiom:
- **VDM-SL**: a dedicated `errs` clause that names error conditions as pre/post pairs, and *explicitly does not commit to a signalling mechanism*. `ext rd/wr` frames.
- **Z**: a total ("robust") operation built by schema disjunction of the normal case with error schemas, each reporting a value and leaving the state unchanged (Ξ).
- **B**: preconditions as caller obligations whose violation means the substitution need not terminate, and nondeterminism via `CHOICE` and `ANY`. B has no error construct; errors are ordinary outputs.

### Cited Findings
- **VDM `errs` (B, Overture VDM-10 Language Manual, TR-001, 2020).**
  - "The exceptions clause can be used to describe how an operation should deal with error situations. The rationale … is to give the user the ability to separate the exceptional cases from the normal cases. The specification using exceptions does not give any commitment as to how exceptions are to be signalled".
  - Form: `errs COND1: c1 -> r1 … CONDn: cn -> rn`. The ci act "as pre-conditions for the different kinds of errors" and the ri as post-conditions.
  - "An operation definition making use of an errs clause essentially gets an effective pre-condition which is a disjunction of the original pre-condition and all the condition expressions".
  - "the exception clauses indicate that the operation being specified takes responsibility for error handling when an exception condition is satisfied. Hence normally exception clauses and pre-conditions do not overlap."
  - Example: `DEQUEUE() e:[Elem] ext wr q : Queue … errs QUEUE_EMPTY: q = [] -> q = q~ and e = nil`.
  - Source: [VDM-10 Language Manual](https://raw.githubusercontent.com/overturetool/documentation/master/documentation/VDM10LangMan/VDM10_lang_man.pdf)
- **VDM `ext` frames (B).** "The externals field lists the state/instance variables that the operation will manipulate. The state/instance variables listed after the reserved word rd can only be read whereas the operation can both read and write the variables listed after wr." — [same](https://raw.githubusercontent.com/overturetool/documentation/master/documentation/VDM10LangMan/VDM10_lang_man.pdf)
- **Z robust operations (A/B, Spivey, *The Z Notation: A Reference Manual*, 2nd ed.).**
  - "we can describe, separately from the first specification, the errors which might be detected and the desired responses to them, then use the operations of the Z schema calculus to combine the two descriptions into a stronger specification".
  - `REPORT ::= ok | already_known | not_known`; `AlreadyKnown ≙ [ΞBirthdayBook; name?; result! | name? ∈ known ∧ result! = already_known]`; `RAddBirthday ≙ (AddBirthday ∧ Success) ∨ AlreadyKnown`.
  - "The declaration ΞBirthdayBook specifies that if the error occurs, the state of the system should not change"; "The operation RAddBirthday must terminate whatever its input."
  - "the code for normal operation and error handling might be thoroughly mingled. This is an example of the abstraction which is possible…"
  - Source: [Spivey ZRM](https://spivey.oriel.ox.ac.uk/wiki/files/zrm/zrm.pdf)
- **B preconditions and nondeterminism (B, Atelier B "B Language Reference Manual" v1.8.10, ClearSy).**
  - `[PRE P THEN S END] R ⇔ P ∧ [S] R`; "If the precondition is not proved, then the substitution does not end … the performance described by a substitution with precondition is guaranteed only if the usage context of the use of the precondition is true."
  - The manual distinguishes PRE from IF: the first "is only usable if the predicate is valid, whereas the second is always performed".
  - `CHOICE S1 OR … OR Sn END` "enables defining a finite number of possible behaviors without specifying which will in fact be implemented. It therefore defines a non deterministic behavior."
  - `ANY X WHERE P THEN S END`: "If a number of values satisfy predicate P, the substitution does not specify which one is effectively chosen"; "The substitution ANY is not an implementation substitution".
  - Source: [B Language Reference Manual](https://www.atelierb.eu/wp-content/uploads/2023/10/b-language-reference-manual.pdf)
- **Event-B and ASM:** unverifiable (event-b.org self-signed certificate; no open Börger copy). The Event-B wiki page read is an index only — [wiki.event-b.org](https://wiki.event-b.org/index.php/Event-B_Language)

### Inferences
- *Inference:* VDM's "does not give any commitment as to how exceptions are to be signalled" is a published precedent for the report's split between K7 (error category) and the profile-level mapping from mechanism to category.
- *Inference:* Z's ΞState-in-error-schemas pattern is a direct, decades-old form for "a failed call leaves observable state unchanged". It is one candidate wording a K3 unit could adopt once the semantics are decided. This is not a semantic recommendation.
- *Inference:* B's PRE-as-abort is the "undefined" strength of § 2.1. The report's inference that "undefined" is almost always wrong at a black-box boundary corresponds to preferring Z/VDM-style total operations (or B's IF) over B's PRE for boundary operations.

### Gaps
- Abrial's B-Book itself was not read; the Atelier B manual stands in. ISO/IEC 13817-1 (VDM-SL standard) was not read (ISO is paywalled and returned 403).

---

## Q5. Gap: Estler et al. 2014, "Contracts in Practice": what figures does it report?

### Takeaway
This is a measured study (A) of 21 contract-using projects. Its findings:
- Contracts are common (over 33% of routines or classes in most projects), stable over time, and changed far less often than implementations.
- The contracts written are overwhelmingly simple null/Void checks, and quantifiers are almost never used.
- There are **no data on exceptional postconditions**.

### Cited Findings
- Scope: "an extensive empirical analysis of 21 contract-equipped Eiffel, C#, and Java projects totaling more than 260 million lines of code over 7700 revisions". Inclusion required at least 30 revisions and contracts on at least 5% of elements — [arXiv 1211.4775v6 (FM 2014)](https://arxiv.org/pdf/1211.4775)
- "the percentage of program elements that include contracts is above 33% for most projects and tends to be stable over time". "in 7 of the 21 analyzed projects, on average 50% or more of the public routines have some specification (pre- or postcondition); in 14 projects, 35% or more"; "in 9 projects, 33% or more of the classes have an invariant; in 10 projects, 12% or less" — [same](https://arxiv.org/pdf/1211.4775)
- "there is no strong preference for a certain type of contract element", but preconditions "tend to be larger (have more clauses) than postconditions" — [same](https://arxiv.org/pdf/1211.4775)
- "Void/null checks are by far the most used": in Eiffel 36%–93% of preconditions; in C# 80%–96% of preconditions; in Java 88%–100% of preconditions. "quantifications are very rarely used: practically never in pre- or postconditions; and very sparsely (1%–10% of invariants)". `old` is absent in C#, at most 2%–3% in Java, and up to 39% of postconditions in some Eiffel projects. "The overwhelming majority of contracts involves Void/null checks." — [same](https://arxiv.org/pdf/1211.4775)
- "Specifications are quite stable compared to implementations: a routine's body may change often, but its contracts will change infrequently." When contracts change, strengthening is more frequent than weakening (pre: p < 0.02; post: p < 0.015; invariants: p = 0.18, not significant), with "smallish" effect sizes (Cohen's d ≈ 0.4, 0.42, 0.18) — [same](https://arxiv.org/pdf/1211.4775)
- A search of the full text found no measurement of exception or exceptional-postcondition usage — [same](https://arxiv.org/pdf/1211.4775)

### Inferences
- *Inference:* In practice, contract notations are used mostly for shallow claims. The rich features the report relies on for K3 (model fields, frames, quantified postconditions) are rarely written. That is a cost signal for any shortlist entry that makes contract notation the main checkable artefact.
- *Inference:* "contracts change infrequently compared with bodies" is weak support for the report's frozen-spec stance, but only for human-written code, not agents.

### Gaps
- The study is pre-LLM and covers open-source projects only. There are no data on multi-backend libraries or on error clauses.

---

## Q6. Gap: EARS (Mavin et al., RE'09): what figures does the paper report?

### Takeaway
**Unverifiable: full text unreachable.** The figures behind "qualitative and quantitative improvements" stay unknown.

### Cited Findings
- Copies tried:
  - ResearchGate PDF: 403.
  - Semantic Scholar marks the paper `"openAccessPdf": {"status": "CLOSED"}`.
  - IEEE Xplore 5328509: 202 bot challenge.
  - The Manchester record has no PDF.
  - CORE: Cloudflare redirect.
  - Sources: [Semantic Scholar API](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/RE.2009.9?fields=title,openAccessPdf,externalIds); [Manchester record](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/)
- Record text (the abstract, read in full):
  - "A small set of structural rules was developed to address eight common requirement problems including ambiguity, complexity and vagueness. The ruleset allows all natural language requirements to be expressed in one of five simple templates. The ruleset was applied whilst extracting aero engine control system requirements from an airworthiness regulation document. The results of this case study show qualitative and quantitative improvements compared with a conventional textual requirements specification."
  - Proc. RE'09, pp. 317–322. Authors per DBLP key conf/re/MavinWHN09.
  - Source: [Manchester record](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/)
- Author's own guide (C; originator, no data):
  - Gives the generic order "While <optional pre-condition>, when <optional trigger>, the <system name> shall <system response>".
  - Patterns: ubiquitous, state-driven (While), event-driven (When), optional-feature (Where) and unwanted-behaviour ("If <trigger>, then the <system name> shall <system response>"), plus Complex combinations.
  - It asserts "EARS reduces or even eliminates common problems found in natural language requirements" without figures.
  - Source: [alistairmavin.com/ears](https://alistairmavin.com/ears/)

### Inferences
- *Inference:* The "reduces or even eliminates" wording the report attributes to vendor material (Jama, D) also appears on the originator's own page. It is still unbacked by figures here, and the grade of the claim does not change.
- *Inference:* The EARS "If … then" template is the only built-in slot for error behaviour. It has no structure for error *categories* or for errors that surface later. That is consistent with the matrix's "+ … ambiguity remains" for K4 prose.

### Gaps
- The RE'09 numbers (problem counts before and after, number of requirements) remain unknown.

---

## Q7. Disconfirming search (a): is there any published rule or guideline that maps specification category or claim type to a notation or form?

### Takeaway
**Partly disconfirmed.** No published, *validated* category → level → form rule was found, and that part of the report's claim stands. But at least three peer-reviewed or official sources publish *guidelines* that map the kind of behaviour or the purpose of analysis to a specification paradigm or level of formality. The report's flat "No published rule maps specification category to level to form … searched … found none" should be softened to "no validated rule; coarse published heuristics exist and agree with the quantifier rule".

### Cited Findings
- **van Lamsweerde, "Formal Specification: a Roadmap", ICSE 2000 FoSE (A, peer-reviewed, conceptual).**
  - "each paradigm above has some built-in semantic bias in order to be useful. State-based and functional specifications focus on sequential behaviors while providing rich structures for defining complex objects. They are thus better targeted at transactional systems. Conversely, history-based, transition-based specifications and operational specifications focus on concurrent behaviors … They are thus better targeted at reactive systems."
  - "To be useful, a formal system must have a limited domain of applicability … A BNF-style specification would be most appropriate for this domain but clearly inappropriate for the domain of process-control systems. There is thus no point in looking for a universal specification technique."
  - "Since no single paradigm will ever serve all purposes due to semantic biases, frameworks are needed in which multiple paradigms can be combined … The various facets then need to be linked through consistency rules".
  - Source: [Univ. Iowa course copy](https://homepage.cs.uiowa.edu/~tinelli/classes/5810/Fall20/Papers/vLam00.pdf)
- **NASA-GB-002-95, Formal Methods Guidebook vol. I (graded B/C: official agency guidance, no outcome data).**
  - "Type of Analysis/Formal Method: The type of analysis, i.e., the reasons for applying FM, determine the most appropriate level of formalization and the most suitable FM and FM tools."
  - "The choice of FM tool, if any, should be directly determined by the application profile generated by evaluating the five preceding factors."
  - "FM … are best suited to analyzing complex problems … and less suited for numerical algorithms".
  - Source: [NASA-GB-002-95 copy](https://www.fing.edu.uy/inco/grupos/mf/TPPSF/Bibliografia/fmguide1.pdf)
- **NASA-GB-001-97, vol. II (B/C).**
  - Modeling phase: "Evaluate potential mathematical representations, considering … the computational model, and explicit (implicit) representation of state and time … Select the mathematical representation most suitable for the application."
  - Worked example: the dependency of current on prior events requires "a state- or trace-based model".
  - Source: [NTRS PDF](https://ntrs.nasa.gov/api/citations/19980227975/downloads/19980227975.pdf)
- **Wing, "A Specifier's Introduction to Formal Methods", IEEE Computer 23(9), 1990 (A, conceptual; scanned PDF read as page images).**
  - Languages are classified by semantic domain: abstract-data-type languages (algebras, theories, programs) versus concurrent and distributed system languages (state sequences, event sequences, synchronization trees, partial orders, state machines).
  - "An advocate of a particular formal method should tell potential users the method's domain of applicability. For example, a formal method might be applicable for describing sequential programs but not parallel ones, or for describing message-passing distributed systems but not transaction-based distributed databases."
  - Wing also notes that "any intentional incompleteness can be captured succinctly as a parameter in the interface".
  - Source: [Wing90a.pdf](https://www.cs.cmu.edu/~wing/publications/Wing90a.pdf)
- **Jackson, problem frames (A/C).** Frames map a *problem class* to a "frame concern" and to the kinds of description needed (domain properties, requirement, machine specification), not to a notation. "Each problem frame has a basic associated frame concern that must be addressed". The paper prescribes no notation per frame — [Jackson 2000](https://stuff.mit.edu/afs/sipb/user/golem/papers/898/mj-marktoberdorf.pdf)
- **Carrizo et al.** map *elicitation* techniques to project attributes, not specification forms (T1-01) — [WER 2008](https://www.inf.puc-rio.br/wer/WERpapers/artigos/artigos_WER08/carrizo.pdf)
- **Unreachable or paywalled, not assessed:**
  - ISO/IEC/IEEE 29148 (iso.org 403);
  - RTCA DO-333 (only a sales page returned);
  - Kotonya & Sommerville (book, no open copy tried);
  - Ardis et al., "A framework for evaluating specification methods for reactive systems" (ICSE 1995 / TSE 1996; no open copy found);
  - Univ. Kaiserslautern "Catalogue of Criteria for Evaluating Formal Methods" (kluedo.ub.rptu.de connection reset).
  - Source for the Ardis bibliographic details: [DBLP via search](https://dblp.uni-trier.de/pid/50/4628.html)

### Inferences
- *Inference:* The published heuristics (sequential/transactional → state-based or functional; concurrent/reactive → history- or transition-based; "type of analysis determines level of formality and method"; "state and time representation decides the model") **agree with** the report's quantifier rule. They cover roughly K3 against K4–K6, at coarser grain. The rule is therefore better described as "a refinement of published coarse heuristics" than as a synthesis with no precedent. This strengthens rather than weakens § 2.3.
- *Inference:* None of these sources is validated by outcome data, and none goes down to the eight-category level or binds level to observers, environment and reality. The report's narrower claim, that no *validated* rule exists at this granularity, survives.
- *Inference:* van Lamsweerde's "multiparadigm … linked through consistency rules" is a published precedent for the report's "one normative unit plus a checkable companion per category".

### Gaps
- ISO 29148, DO-333 and Kotonya & Sommerville were not read. Any of them could contain a notation-per-requirement-type table. 29148 was reported in the earlier notes as having none, but that was not verified here.

---

## Q8. Findings that would change the Kernsatz, the form rule (§ 2.3), the scorecard or the shortlist, and what is merely restyled

### Takeaway
Nothing here overturns the Kernsatz or the rule. One sentence of § 1/§ 2.3 should change, and the rest is citation and grade repair.

### Cited Findings
- **Changes wording of the Kernsatz preamble and § 2.3:** "No published rule maps specification category to level to form … found none" should become "no *validated* rule; published coarse heuristics (van Lamsweerde 2000; NASA-GB-002-95; Wing 1990) map kind of behaviour or analysis purpose to paradigm and agree with the quantifier rule" — [van Lamsweerde](https://homepage.cs.uiowa.edu/~tinelli/classes/5810/Fall20/Papers/vLam00.pdf); [NASA-GB-002-95](https://www.fing.edu.uy/inco/grupos/mf/TPPSF/Bibliografia/fmguide1.pdf); [Wing 1990](https://www.cs.cmu.edu/~wing/publications/Wing90a.pdf)
- **Strengthens the form rule (§ 2.2/§ 2.3):** ACSL's `complete behaviors` / `disjoint behaviors` show that case-split completeness and disjointness are machine-checkable in a contract language, not only in tables — [ACSL](https://frama-c.com/download/acsl.pdf)
- **Strengthens K7:** Spec#'s contract-tied split of client, admissible and program-error failures defines error categories by caller recovery, and VDM `errs` "does not give any commitment as to how exceptions are to be signalled" — [Spec#](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/TheSpecSharpProgrammingSystem28CASSIS200429.pdf); [VDM-10 LangMan](https://raw.githubusercontent.com/overturetool/documentation/master/documentation/VDM10LangMan/VDM10_lang_man.pdf)
- **Scorecard and cost signal for contract-centred shortlist entries:** real-world contracts are overwhelmingly null checks and quantifiers almost never appear — [Estler et al.](https://arxiv.org/pdf/1211.4775)
- **§ 3.2 can lose its † for VDM, Z and B** (Q4). Event-B and ASM keep it.
- **Merely restyled or corrected, no conclusion change:**
  - the ShardStore percentage (12.2% of code, not 14%) and the quote wording (T1-27, T1-36);
  - the Parnas citation (T1-02);
  - the C11 source (T1-22);
  - the Jepsen `:info` source (T1-24);
  - the Hadoop `open()` source (T1-42);
  - the JML default stated as a version difference, and `signals_only` including RuntimeException (T1-11, T1-12);
  - the NetBSD "every major kernel" claim (T1-56);
  - the LWN comment (T1-57);
  - the PEP 3116 layer nuance (T1-25);
  - grade changes in Q2.

### Inferences
- *Inference:* The interface-automata limit (outputs cannot be required) has a published remedy in modal and IOMTS interface theories. § 3.3's "liveness needs a separate mechanism" could name it. This does not affect the shortlist — [Lüttgen & Vogler, LMCS 2013](https://arxiv.org/pdf/1306.3050v2)

### Gaps
- The EARS figures and the Parnas–Madey, Heitmeyer & Labaw and Lawford & Wassyng full texts remain unread (hosts blocked or paywalled). Their claims keep their current hedges.
