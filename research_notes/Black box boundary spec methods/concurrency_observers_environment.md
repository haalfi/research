# Specifying behaviour at a black-box API boundary under concurrency, named observers and an explicit environment model

Method note: every claim links a URL. Direct page fetching was blocked in this session (DNS/proxy 403), so claims were checked through search-engine extracts of the primary sources (abstracts, publisher pages, author PDFs). Where I fell back on bibliographic knowledge without a search extract, the claim is marked "[not re-verified]". Own reasoning is marked **Inference**. Source grades: A = peer-reviewed or measured; B = documented industrial practice with data; C = practitioner report without data; D = opinion or marketing.

Running example used in the inferences (no semantics decided here): `open(key) -> stream`. Observers: O1 = the calling code, O2 = a second concurrent caller, O3 = an external actor that changes the store outside the library. Hard cases: H1 = a concurrent write or external mutation while the stream is open; H2 = a failure after `open` has returned.

---

## Q1. Interface/contract families: rely-guarantee, assume-guarantee (Abadi–Lamport, Benveniste et al.), linearizability ("sequential spec + consistency condition"), CSL briefly

### Takeaway
The most reusable structural idea is to split the contract in two: an **assumption about the environment** (what O2 and O3 may do) and a **guarantee by the component** (what O1 observes). Abadi–Lamport and Benveniste et al. give this split a precise meaning that composes. Linearizability adds a second split: a **sequential specification** of the API, plus a **consistency condition** saying how concurrent histories map onto it. Together they give a "one sequential spec, several consistency conditions" template that fits multiple backends.

### Cited Findings
- **Rely-guarantee (Jones 1983).** "Tentative steps toward a development method for interfering programs", TOPLAS 5(4) 1983. A specification adds two conditions to pre/post: a *rely* condition (state changes other processes may make, i.e. interference the component tolerates) and a *guarantee* condition (state changes the component itself makes) — [ACM DL doi:10.1145/69575.69577](https://doi.org/10.1145/69575.69577) [not re-verified; grade A]. Benveniste et al. list "rely/guarantee reasoning" as one of the framework instances their contract meta-theory covers — [now publishers EDA-053](https://nowpublishers.com/article/Details/EDA-053) (A).
- **Assume-guarantee, Abadi & Lamport.** "Composing Specifications" (TOPLAS 1993) writes an open-system specification as E ⇒ M, with E the assumptions on the environment and M what the system guarantees — [MSR page](https://www.microsoft.com/en-us/research/publication/composing-specifications/) (A). "Conjoining Specifications" (TOPLAS 17(3):507–534, 1995) fixes a weakness of plain E ⇒ M: under that form the system may break M first and the environment break E afterwards. The paper therefore uses a form in which M must keep holding at least one step longer than E holds ("E –+> M"). It proves one theorem for decomposing closed-system specs and one for composing open-system specs — [MSR PDF](https://microsoft.com/en-us/research/uploads/prod/2016/12/Conjoining-Specifications.pdf); [MSR page](https://www.microsoft.com/en-us/research/publication/conjoining-specifications/) (A).
- **Contracts for System Design (Benveniste et al., FnT EDA 12(2–3):124–400, 2018, DOI 10.1561/1000000053).** Builds a meta-theory of contracts with refinement, composition and conjunction. Specific frameworks are instances of it: assume/guarantee contracts (§5), synchronous Moore interfaces, rely/guarantee, and interface theories — [now publishers](https://nowpublishers.com/article/Details/EDA-053); [Aalborg record](https://vbn.aau.dk/en/publications/contracts-for-system-design) (A). An FME review warns that the framework chapters are dense and are not tutorials — [FME Europe review](https://fmeurope.org/2020/10/30/book-review-contracts-for-system-design) (C).
  - Contracts in this tradition have operators for *conjunction* (several viewpoints on one component, each with its own A/G pair) and *refinement* (C' refines C if C' assumes no more and guarantees no less) — [now publishers EDA-053](https://nowpublishers.com/article/Details/EDA-053) [operator details from the monograph's framework, not re-verified line by line; A].
- **Linearizability (Herlihy & Wing, TOPLAS 12(3):463–492, 1990).** Each operation appears to take effect at a single instant between its invocation and its response. Correctness is defined *relative to a sequential specification*: every concurrent history must be equivalent to some legal sequential history that preserves real-time order. So pre/postconditions of the sequential object remain the spec of record — [Herlihy & Wing PDF](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf) (A). Linearizability is *local* (compositional per object), a property the paper contrasts with sequential consistency/serializability — [Herlihy & Wing PDF](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf) (A; locality theorem not quoted in extract). Checking it in general is NP-complete, and Jepsen's Knossos checker "taps out" at a few hundred operations — [Morning Paper on Elle](https://blog.acolyer.org/2020/11/23/elle/) (C, summarising the A paper).
- **Concurrent separation logic (brief).** O'Hearn's CSL ("Resources, concurrency, and local reasoning", TCS 2007) reasons about ownership transfer of heap regions between threads via resource invariants. It is code-level and aimed at proving an implementation, not at stating a black-box contract — [doi:10.1016/j.tcs.2006.12.035](https://doi.org/10.1016/j.tcs.2006.12.035) [not re-verified; A].

### Inferences
- **Inference:** Assume-guarantee maps directly onto the three observers. The **assumption** E names what O2 and O3 may do: O2 may call any API operation concurrently, and O3 may mutate or delete the entity at any time. The **guarantee** M names what O1 sees. Because the backends are "realities", each backend could be a *refinement* of a common weakest contract, so stronger backends guarantee more under the same assumption, or assume less. That fits P3 (keep per-backend detail apart) and P2 (the common contract is the one home for shared rules).
- **Inference:** The Abadi–Lamport "M holds one step longer than E" point matters for H1 and H2. It forbids a vacuous contract in which the library's misbehaviour (say, a stream yielding mixed bytes) is excused by a *later* environment violation.
- **Inference:** Linearizability fits single-shot operations. A stream is a *long-lived* operation: `open` plus N reads plus `close`. Herlihy–Wing has to decide whether the whole stream is one operation (snapshot semantics) or each chunk read is one (possible torn reads). That decision is semantic, and the framework only forces it to be explicit. That is a P1-compatible effect.
- **Inference:** CSL fails P5 as a boundary-spec method because it needs implementation structure. Keep it to the "how" layer.

### Gaps
- I could not retrieve full text for Jones 1983 or the exact Abadi–Lamport composition theorem hypotheses. The bibliographic and abstract-level claims are solid, but details beyond them are not.
- I found no source that applies assume-guarantee contracts to a *streaming* read API specifically.

---

## Q2. Consistency-model specification frameworks: how they name observers/sessions, state guarantees as predicates over histories, and build hierarchies

### Takeaway
The mature line (Adya → Burckhardt → Viotti & Vukolić → Crooks et al.) defines guarantees as **predicates over histories** of client-observed events. It names observers as **sessions or processes** and adds abstract relations (visibility, arbitration, dependency graphs) to interpret the history. Models form a **partial order by strength**, which gives a ready-made "weaker/stronger variant" lattice. Client-centric formulations (Crooks; Terry's session guarantees) are the ones that fit a black-box boundary, because they mention only what clients can observe.

### Cited Findings
- **Adya (MIT PhD 1999, MIT/LCS/TR-786).** Existing isolation definitions were "either imprecise or they disallow efficient implementation techniques such as optimism". Adya gives what he calls the first *implementation-independent* specifications of the ANSI isolation levels — [DSpace@MIT](https://dspace.mit.edu/handle/1721.1/149899); [PDF mirror](https://www.aphyr.com/data/posts/294/adya-phd.pdf) (A). The levels are defined as forbidden cycles/phenomena (G0, G1a–c, G2…) in a direct serialization graph over committed transactions — [Adya PDF](https://www.aphyr.com/data/posts/294/adya-phd.pdf) [phenomenon names from knowledge, not in extract].
- **Elle (Kingsbury & Alvaro, PVLDB 14(3):268–280).** Makes Adya-style specs *checkable from black-box observations*. It infers an Adya dependency graph from client-observed histories and detects every Adya anomaly except predicate ones. Workloads are chosen so that read values reveal version order — [VLDB](https://www.vldb.org/pvldb/volumes/14/paper/Elle%3A%20Inferring%20Isolation%20Anomalies%20from%20Experimental%20Observations); [arXiv 2003.10554](https://arxiv.org/abs/2003.10554) (A).
- **Viotti & Vukolić, ACM CSUR 49(1) 2016, DOI 10.1145/2926965.** Surveys 50+ non-transactional consistency notions, defines them precisely where earlier definitions were ambiguous, and arranges them in a *partial order by semantic strength*, mapped to real systems. The scope is single-object, non-transactional operations — [arXiv 1512.00168](https://arxiv.org/pdf/1512.00168); [EURECOM record](https://www.eurecom.fr/en/node/4903210) (A). The framework follows Burckhardt: a history H of operations with session/process order and real-time order, interpreted through an abstract execution — [arXiv 1512.00168](https://arxiv.org/pdf/1512.00168) [formalism detail from knowledge; A].
- **Burckhardt, "Principles of Eventual Consistency" (FnT PL 1(1–2):1–150, 2014, DOI 10.1561/2500000011).** States its goal as supplying *principles* for saying what a consistency protocol guarantees and for proving or refuting such claims — [now publishers PGL-011](https://nowpublishers.com/article/Details/PGL-011) (A). An abstract execution is a triple (H, vis, ar). Visibility is acyclic (which operations an operation "saw"). Arbitration is a total order resolving conflicts. Visibility does not imply arbitration — [MSR PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/article.pdf); summaries in [Acute Cloud Types arXiv 1905.11762](https://arxiv.org/pdf/1905.11762) (A). Guarantees are axioms over (H, vis, ar). The canonical ones are "eventual visibility" (each op is eventually visible to all but finitely many ops), read-my-writes (session order ⊆ vis), and so on — [MSR PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/article.pdf) [axiom names from knowledge].
- **Crooks, Pu, Alvisi, Clement, "Seeing is Believing: A Client-Centric Specification of Database Isolation", PODC 2017:73–82, DOI 10.1145/3087801.3087802.** Defines isolation levels purely in terms of the *states* that client transactions observe ("read states"), with no reference to internal histories or dependency graphs. It unifies consistency and isolation — [NSF PAR](https://par.nsf.gov/biblio/10077635); arXiv precursor "A Unified Model for Consistency and Isolation via States" [arXiv 1609.06670](https://arxiv.org/pdf/1609.06670) (A). [Abstract-level detail on "read states" from knowledge; the extract confirmed only the bibliography.]
- **Session guarantees (Terry, Demers, Petersen, Spreitzer, Theimer, Welch, PDIS 1994:140–149).** Four per-session guarantees: Read Your Writes, Monotonic Reads, Writes Follow Reads, Monotonic Writes. Their stated aim is to give each application a view consistent with its *own* actions even when it reads and writes through different servers. An application either gets the guarantee for its session or is *told* it cannot be met. The cost is reduced availability — [PDF (Wisconsin)](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf); [Cornell copy](https://www.cs.cornell.edu/courses/cs734/2000FA/cached%20papers/SessionGuaranteesPDIS_1.html) (A).

### Inferences
- **Inference (observers):** These frameworks name observers in three ways:
  - (a) *process/session identifiers* on events: O1 and O2 are distinct sessions;
  - (b) *relations* among events: session order, real-time order, visibility;
  - (c) in Crooks, the *read state* each transaction observes.
  O3 (the external actor) can be modelled as just another session whose writes appear in the history but which the library never sees. That is exactly how Jepsen-style checkers treat any client — [Elle](https://arxiv.org/abs/2003.10554).
- **Inference (lattice):** Viotti–Vukolić's partial order is the closest published artefact to "one contract with weaker/stronger variants". A backend would be specified by *which predicates it satisfies*, and the API-level contract would be the meet (weakest) of all backends. Session guarantees are a clean, orthogonal set of four Boolean properties, which is easy for P3 and P4: each one is checkable on a history.
- **Inference (running example):** For H1, the relevant question is whether the bytes yielded by one stream come from a single version, i.e. whether all chunk-reads of one stream share a read state (Crooks) or the same visibility set. That is a predicate over the history, so P4 can name a history checker (Elle/Knossos-style) as its check.
- **Inference (unspecified):** Burckhardt's eventual visibility is a liveness-like axiom with *no bound*. It cannot be falsified by any finite history. A spec that adopts it must state explicitly that it is untestable as stated, or add a bounded variant (e.g. "probabilistically bounded staleness"; not researched here).

### Gaps
- I could not confirm Crooks et al.'s exact formal definitions or Burckhardt's exact axiom list from primary text in this session.
- These frameworks model *operations as atomic events*. None of the sources found treats a long-lived read stream as an operation with an extent (open … close). This is a real gap for the running example.

---

## Q3. Temporal/trace specs: TLA+ with environment actions, I/O automata, CSP refinement, P — how "the environment may do X" and crash/failure are stated

### Takeaway
All four state the environment as **explicit nondeterministic actions** that the system cannot block:
- TLA+: environment sub-actions in Next, or E ⇒ M open specs;
- I/O automata: input actions are always enabled;
- CSP: the environment is the process composed in parallel, and refinement is checked over traces/failures;
- P: nondeterministic environment/"ghost" machines that close the system for testing.

Crashes are modelled the same way, as environment-controlled actions such as crash, restart, message loss or external mutation. Liveness ("eventually") is a separate fairness clause.

### Cited Findings
- **TLA+ open-system specs.** Abadi–Lamport define an open specification as E ⇒ M (or E –+> M), where E constrains the environment's steps — [Composing Specifications](https://www.microsoft.com/en-us/research/publication/composing-specifications/); [Conjoining Specifications PDF](https://microsoft.com/en-us/research/uploads/prod/2016/12/Conjoining-Specifications.pdf) (A). Lamport's *Specifying Systems* treats interface specs, open-system specs and the separation of safety and fairness (liveness) — [Specifying Systems book page](https://lamport.azurewebsites.net/tla/book.html) [not re-verified; A].
- **Cosmos DB TLA+ (Hackett, Rowe, Kuppe, ICSE-SEIP 2023).** Specifies *user-facing behaviours* rather than internals, yielding a smaller model than prior Cosmos DB specs that covers a wider range of user-observable behaviour. Many of these behaviours were poorly understood outside the Cosmos DB team and had caused data-consistency errors in dependent Microsoft products. The model surfaced two issues in Cosmos DB's public documentation (since fixed) and provided a fix for a high-impact outage in another Azure service — [arXiv 2210.13661](https://arxiv.org/pdf/2210.13661); [ICSE SEIP listing](https://conf.researchr.org/details/icse-2023/icse-2023-SEIP/3/Understanding-Inconsistency-in-Azure-Cosmos-DB-with-TLA-) (A/B).
- **I/O automata (Lynch & Tuttle 1987).** Actions are partitioned into input, output and internal. Automata are *input-enabled*: any input can occur in any state, so the environment controls when inputs happen and the automaton only defines its reaction — [Wikipedia: I/O automaton](https://en.wikipedia.org/wiki/Input/output_automaton) (C); [Lynch retrospective arXiv 2502.20468](https://arxiv.org/pdf/2502.20468) (A); [original MIT LCS TR-387 / DTIC](https://apps.dtic.mil/sti/pdfs/ADA210831.pdf) (A). Process algebras emulate input-enabledness by adding default transitions — [arXiv 0911.3299](https://arxiv.org/pdf/0911.3299) (A). Crash is typically modelled as an input action "crash_i" after which the process stops producing outputs (standard in Lynch's *Distributed Algorithms*) [not re-verified].
- **CSP / refinement.** Specifications and implementations are both processes. Correctness is refinement (traces, stable failures, failures-divergences), which captures what the system may *refuse*. Hoare's book — [usingcsp.com](http://www.usingcsp.com/) [not re-verified; A]. In the Benveniste meta-theory, interface theories and refinement are instances of the same contract algebra — [now publishers EDA-053](https://nowpublishers.com/article/Details/EDA-053) (A).
- **P language (Desai et al., PLDI 2013).**
  - Systems are interacting state machines exchanging events.
  - The *environment is specified as nondeterministic ghost machines* that close the system for testing and are erased at compile time; a type system guarantees the erasure preserves semantics.
  - The defaults are a safety check for unhandled events and a liveness check for events deferred forever.
  - P was used for the core USB driver stack in Windows 8.

  Sources: [MSR publication](https://www.microsoft.com/en-us/research/publication/p-safe-asynchronous-event-driven-programming-2/); [PLDI PDF](https://microsoft.com/en-us/research/wp-content/uploads/2016/02/pldi212_desai.pdf) (A). Desai describes event-driven systems as hard because of "interleavings of events and failures" — [CSAIL talk abstract](https://www.csail.mit.edu/event/p-modular-and-safe-event-driven-programming) (C).
- **P at AWS.** Brooker & Desai (CACM 68(6), 2025) report that many engineers struggled to become productive with TLA+, which motivated adopting P (state-machine-based). It is used alongside property-based testing, fault-injection testing and deterministic simulation — [CACM](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services); [ACM Queue](https://queue.acm.org/detail.cfm?id=3712057) (B).

### Inferences
- **Inference:** "The environment may do X" has the same shape in every family: an action, enabled at all times (or under a stated precondition), that the component cannot refuse. For the running example this would be `ExternalWrite(key)`, `ExternalDelete(key)` and `ConcurrentCall(O2, op)`, plus failure actions such as `BackendUnavailable` and `ConnectionDrop`. These would be listed in **one place**, the environment model, satisfying P2.
- **Inference:** H2 (failure after return) is naturally an environment action that interleaves between `open`'s response and a later `read`. Trace formalisms make "what O1 may observe after this action" a first-class question, because the trace contains the action. Pre/post specs alone cannot express it.
- **Inference:** In both TLA+ and P, fairness and liveness are stated separately from safety. That lets "eventually visible with no bound" be written honestly as a fairness assumption that no finite test can refute (relevant to P4).
- **Inference:** The Cosmos DB result is the closest published analogue to this project. It is a spec of the *client-observable* boundary of a multi-consistency-level service, written to remove documentation ambiguity.

### Gaps
- I did not retrieve primary text on how *Specifying Systems* phrases interface/environment separation (chapter-level detail), or on CSP's failure semantics for crashes.
- The exact P mechanism for failure injection (e.g. a nondeterministic `$`/`choose` in environment machines) is not confirmed from primary docs in this session.

---

## Q4. Industrial uses with data (AWS TLA+, S3 strong consistency, ShardStore, Cosmos DB, MongoDB/Jepsen, S3 consistency docs)

### Takeaway
There is strong industrial evidence (grade B, some A) that executable or model-checkable specs of *observable behaviour* find real bugs and documentation errors:
- ShardStore: 16 issues prevented;
- Cosmos DB: 2 documentation fixes plus an outage fix;
- AWS: TLA+ on ~10 large systems from 2011;
- Jepsen/Elle: SI violations found even at the strongest MongoDB settings.

Vendor boundary statements (S3) are prose, phrased as client-observable ordering guarantees with explicit carve-outs for concurrent writers.

### Cited Findings
- **Newcombe et al., "How Amazon Web Services Uses Formal Methods", CACM 58(4), 2015.** Since 2011 AWS engineers used TLA+ specification and model checking on difficult design problems in critical systems. A draft-era summary reports use on 10 large, complex real-world systems — [CACM](https://cacm.acm.org/magazines/2015/4/184701-how-amazon-web-services-uses-formal-methods/fulltext); [2014 draft PDF](https://6826.csail.mit.edu/2019/papers/formal-methods-amazon.pdf); [Morning Paper summary](https://blog.acolyer.org/2014/11/24/use-of-formal-methods-at-amazon-web-services/) (B). (A specific DynamoDB "35-step trace" claim could not be confirmed in this session's extracts and should not be cited without checking the PDF.)
- **Brooker & Desai, "Systems Correctness Practices at AWS", CACM 2025.** Covers TLA+, P, property-based testing, fault injection and deterministic simulation as a portfolio — [CACM](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services) (B).
- **S3 strong consistency, formal work.** Amazon Science says a proof of S3's strong consistency was done at the *distributed-protocol* level, and notes such proofs cover protocols, not necessarily server code — [Amazon Science: Automated reasoning's scientific frontiers](https://www.amazon.science/blog/automated-reasonings-scientific-frontiers) (B). The AWS Storage Blog describes how automated reasoning is applied at S3 — [AWS Storage Blog](https://aws.amazon.com/blogs/storage/how-automated-reasoning-helps-us-innovate-at-s3-scale) (B). Claims that formal proofs run on each commit to the consistency index subsystem come from a journalist interview — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-aws-s3-is-built) (C).
- **ShardStore (Bornholt et al., SOSP 2021, best paper).**
  - Uses *executable reference models* written in Rust as the specification.
  - Decomposes correctness into independent properties, each checked by the most appropriate tool: property-based conformance testing, crash-consistency checking, and stateless model checking for concurrency.
  - Prevented 16 issues from reaching production, including subtle crash-consistency and concurrency bugs.
  - The spec and harness added about 14% to the codebase, against the 2–10x the authors cite as typical of full verification.
  - The authors accept weaker guarantees than full verification ("we can still miss bugs").

  Sources: [paper PDF](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf); [Amazon Science blog](https://www.amazon.science/blog/aws-team-wins-best-paper-award-for-work-on-automated-reasoning) (A; 16 is self-reported).
- **Cosmos DB TLA+.** See Q3. User-facing spec; two public-doc issues fixed; outage fix in a dependent service — [arXiv 2210.13661](https://arxiv.org/pdf/2210.13661) (A/B).
- **MongoDB 4.2.6 (Jepsen, May 2020).**
  - Snapshot isolation was violated even at the strongest read/write concerns: read skew, cyclic information flow, duplicate writes, internal-consistency violations.
  - The `snapshot` read concern did not guarantee a snapshot unless it was paired with write concern `majority`.
  - Single-document operations looked linearizable only with `linearizable` read and `majority` write concern.
  - Causal sessions did not give causal consistency by default.
  - MongoDB said the behaviour was as designed and updated its documentation.

  Sources: [Jepsen analysis](https://jepsen.io/analyses/mongodb-4.2.6); [Jepsen blog](https://jepsen.io/blog/2020-05-15-mongodb-4.2.6) (A-ish: measured, independent, not peer-reviewed; grade B/A). MongoDB's own page says majority write concern became the default in 5.0 — [mongodb.com/jepsen](https://mongodb.com/jepsen) (D/B, vendor).
- **S3 consistency documentation (vendor phrasing example).**
  - The official product page states strong read-after-write consistency for PUT of new objects, overwrites and deletes. After a successful write, subsequent reads, *and LIST*, reflect it — [aws.amazon.com/s3/consistency](https://aws.amazon.com/s3/consistency/) (D/B, vendor).
  - Concurrency carve-outs as reported second-hand from the User Guide: S3 "does not support object locking for concurrent writers"; overlapping PUTs to the same key resolve last-writer-wins by timestamp; the order in which S3 receives concurrent requests is not predictable — [AWS re:Post](https://repost.aws/zh-Hans/questions/QUrlRsYX5iT2GmWBrZofcw0w/s3-strong-consistency-implications) (C); [third-party analysis](https://hidekazu-konishi.com/entry/how_amazon_s3_achieves_consistency_and_durability.html) (C).
  - The official User Guide page ("Amazon S3 data consistency model", under [docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)) could not be fetched here, so the exact wording is unverified.
- **Cosmos DB consistency docs** state five named levels (strong, bounded staleness, session, consistent prefix, eventual) as an ordered spectrum — [Microsoft Learn: consistency levels](https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels) [not re-verified; vendor D/B]. The Hackett et al. TLA+ work exists because this prose was ambiguous to dependent teams — [arXiv 2210.13661](https://arxiv.org/pdf/2210.13661) (A).

### Inferences
- **Inference:** The S3 statement shows how vendors phrase a boundary guarantee:
  - (1) observers are implicit ("subsequent read requests"), not named;
  - (2) ordering is defined by *completion of the write* relative to *start of the read*, i.e. real-time order as in linearizability;
  - (3) concurrent writers are handled by an explicit carve-out (LWW, no locking, unpredictable order) rather than by a semantics;
  - (4) bucket configuration and other side paths have separate, weaker statements (reported second-hand).

  Naming O1/O2/O3 explicitly would remove the ambiguity that the Cosmos DB paper found in comparable vendor prose.
- **Inference:** ShardStore's "executable reference model + per-property best-fit checker" matches P4 well, because every property names its checker, and P5, because the reference model is usable without the implementation. Its scope is a single node, though, not multiple external observers.
- **Inference:** Jepsen shows why an explicit environment matters. MongoDB's anomalies appeared only under faults such as partitions and node failures, which are environment actions. A spec without them would have been vacuously met.
- **Inference (H1 for vendors):** None of the vendor statements found addresses an object being overwritten *while a GET is streaming*. That is a common silent area in boundary docs.

### Gaps
- Verbatim official S3 User Guide consistency wording, including statements about concurrent GET during PUT and about bucket-config eventual consistency, is not verified.
- No published quantitative study was found comparing defect rates of boundary specs with internal specs.
- The DynamoDB-specific numbers from Newcombe et al. are unverified.

---

## Q5. Handling "unspecified" (e.g. unbounded eventual visibility) and fit to P1–P5

### Takeaway
The frameworks handle "unspecified" in three distinct ways:
1. **Nondeterminism**: the spec allows a set of outcomes (TLA+/IOA/P environment choice; LWW with unpredictable order in S3).
2. **Liveness without bound**: Burckhardt's eventual visibility; TLA+ fairness. This is unfalsifiable by finite tests.
3. **Explicit refusal**: Terry's "the application is told the guarantee cannot be met".

Fit to the principles is best for assume-guarantee contracts combined with client-centric history predicates and an explicit environment action list, with conformance checked by executable models or history checkers.

### Cited Findings
- **Unbounded eventual visibility.** Burckhardt formalises eventual consistency as an axiom on abstract executions, separate from safety axioms — [Burckhardt FnT](https://nowpublishers.com/article/Details/PGL-011); [MSR PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/article.pdf) (A). In TLA+ and P, liveness is stated via fairness or liveness monitors separate from safety; P's default liveness check flags events deferred forever — [P PLDI 2013](https://www.microsoft.com/en-us/research/publication/p-safe-asynchronous-event-driven-programming-2/) (A).
- **Nondeterministic outcomes.** In linearizability, *any* legal sequential history consistent with real-time order is acceptable, so the spec is a set of allowed outcomes — [Herlihy & Wing](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf) (A). S3's unpredictable ordering of concurrent writers is a vendor instance of the same idea — [re:Post](https://repost.aws/zh-Hans/questions/QUrlRsYX5iT2GmWBrZofcw0w/s3-strong-consistency-implications) (C).
- **Explicit refusal/notification.** In session guarantees, the application either gets the guarantee or is informed it cannot be provided — [Terry et al. 1994](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf) (A).
- **Partial failure in checkers.** Jepsen histories record operations whose outcome is unknown, e.g. timeouts, as *indeterminate* ("info"). Checkers must allow them to have taken effect or not — [Elle arXiv](https://arxiv.org/abs/2003.10554) (A) [the "info"/indeterminate treatment is standard Jepsen practice; mechanism detail from knowledge].
- **Weaker guarantees knowingly accepted.** ShardStore explicitly trades completeness for cost (≈14% code, can still miss bugs) — [ShardStore paper](https://www.cs.utexas.edu/%7Ebornholt/papers/shardstore-sosp21.pdf) (A).

### Inferences: principle fit matrix (own assessment)
| Method | P1 what-not-how | P2 one home per rule | P3 per-backend apart | P4 claim names check | P5 usable w/o impl | Partial failure |
|---|---|---|---|---|---|---|
| Rely-guarantee | good (interference as relation) | good (rely = env in one place) | medium | weak (proof-oriented) | good | not native; add failure to rely |
| Assume-guarantee contracts (Abadi–Lamport; Benveniste) | good | very good (environment E in one place; conjunction of viewpoints) | very good (refinement between backend contracts) | medium (needs a model checker or tests) | good | env actions inside E |
| Linearizability (seq spec + condition) | good | good (seq spec is the single home) | good (swap condition per backend) | good (Knossos/Porcupine-style checkers; NP-complete) | very good | pending ops may or may not take effect |
| Adya / Elle | good (client-observed) | good | good (levels as forbidden phenomena) | very good (Elle) | very good | indeterminate ops |
| Burckhardt / Viotti–Vukolić | good | good | very good (partial order of predicates) | medium (liveness not testable) | good | via visibility; liveness unbounded |
| Crooks client-centric | very good (only observed states) | good | good | medium | very good | not central |
| Session guarantees | very good | good | very good (4 Boolean properties) | good | very good | "told it cannot be met" |
| TLA+ open spec | good if spec is user-facing (Cosmos DB) | good | good (one module per backend refining a common one) | good (TLC on model, not impl) | good | env actions + fairness |
| I/O automata | good | good (inputs = env) | good | medium | good | crash as input |
| CSP refinement | good | good | good (refinement checks) | good (FDR, on model) | good | refusals/failures semantics |
| P | medium (models tend toward design) | good (env machines) | good | good (systematic testing; in AWS practice) | medium | env machines inject failures |
| Executable reference model (ShardStore) | medium (model is code) | good | good | very good | good | crash-consistency checking |

- **Inference:** No single family covers all five principles. The most defensible combination in the literature is:
  - (a) an assume-guarantee frame whose environment E names O2/O3 actions and failure actions;
  - (b) a sequential spec of the API, with per-backend consistency conditions drawn from the Viotti–Vukolić/session-guarantee vocabulary;
  - (c) each predicate tied to a history checker (Elle/Knossos-style) or an executable reference model, as P4 requires.

  This is a synthesis, not a published method.
- **Inference:** Stream semantics (H1) need an extension that none of the surveyed frameworks provides off the shelf: an operation with an extent, or a decomposition into per-chunk operations plus a cross-chunk predicate. This should be flagged as a known modelling decision, not inherited.

### Gaps
- I found no published method that explicitly names a third, *out-of-band* observer (O3) that bypasses the API. All frameworks treat it as just another client or session. Whether that is adequate (O3 may not respect the library's metadata or locking conventions) is open.
- I found no comparative empirical study across these method families on specification-defect rates.
