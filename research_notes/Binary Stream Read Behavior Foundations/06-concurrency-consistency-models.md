# Track 06: Consistency and concurrency models governing what a read may return

Scope: exact definitions, from primary sources, of which values a READ may return under concurrency,
staleness and replication. No new taxonomy is proposed here; source terminology is kept.
Downloads: `/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/concurrency-consistency-models/`

## 1. Sources consulted and access status

| # | Source | Type | Access | Copy read |
|---|--------|------|--------|-----------|
| S1 | Lamport, "On Interprocess Communication" (SRC report Dec 1985; Distributed Computing 1(2), 1986) | theoretical | FULL TEXT | lamport.azurewebsites.net/pubs/interprocess.pdf |
| S2 | Lamport, "How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs", IEEE Trans. Computers C-28(9), 1979 | theoretical | FULL TEXT (2 pp.) | lamport.azurewebsites.net/pubs/multi.pdf |
| S3 | Herlihy & Wing, "Linearizability: A Correctness Condition for Concurrent Objects", ACM TOPLAS 12(3), 1990 | theoretical, peer-reviewed | FULL TEXT | cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf |
| S4 | Terry, Demers, Petersen, Spreitzer, Theimer, Welch, "Session Guarantees for Weakly Consistent Replicated Data", PDIS 1994 | peer-reviewed (design + definitions) | FULL TEXT | pages.cs.wisc.edu/~remzi/Classes/739/Fall2016/Papers/bayou-sessions94.pdf (utexas/cornell copies failed TLS; MSR copy 403) |
| S5 | Berenson, Bernstein, Gray, Melton, O'Neil, O'Neil, "A Critique of ANSI SQL Isolation Levels", SIGMOD 1995 (MSR-TR-95-51) | peer-reviewed, theoretical | FULL TEXT | arXiv cs/0701157 |
| S6 | Adya, "Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions", MIT PhD thesis 1999 (MIT-LCS-TR-786) | theoretical | FULL TEXT | publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-786.pdf (pmg.csail.mit.edu reset) |
| S7 | Viotti & Vukolic, "Consistency in Non-Transactional Distributed Storage Systems", ACM CSUR 49(1), 2016 | survey | FULL TEXT (arXiv v4) | arXiv 1512.00168 |
| S8 | Bailis, Davidson, Fekete, Ghodsi, Hellerstein, Stoica, "Highly Available Transactions: Virtues and Limitations", VLDB 2014 (extended arXiv v2) | peer-reviewed, theoretical + empirical | FULL TEXT | arXiv 1302.0309 |
| S9 | Bailis, Venkataraman, Franklin, Hellerstein, Stoica, "Probabilistically Bounded Staleness for Practical Partial Quorums", VLDB 2012 | peer-reviewed empirical/theory | FULL TEXT (abstract + Sec 1-3 read) | arXiv 1204.6082 |
| S10 | Vogels, "Eventually Consistent", ACM Queue 6(6) 2008 / CACM 52(1) 2009 | engineering essay | FULL TEXT via author's blog copy ("Eventually Consistent - Revisited"); queue.acm.org returned 403 | allthingsdistributed.com/2008/12/eventually_consistent.html |
| S11 | POSIX.1-2017 (Open Group Base Specs Issue 7, 2018 ed.): read(), write(), XSH 2.9.7 | normative | FULL TEXT of sections | pubs.opengroup.org/onlinepubs/9699919799/ |
| S12 | RFC 7530 (NFSv4), Sec 10.3.1 "Data Caching and OPENs" | normative (Standards Track) | FULL TEXT of section | rfc-editor.org/rfc/rfc7530.txt |
| S13 | RFC 8881 (NFSv4.1), Sec 13.10 | normative | FULL TEXT of section | rfc-editor.org/rfc/rfc8881.txt |
| S14 | AWS, Amazon S3 User Guide, "Amazon S3 data consistency model" (fetched 2026-11-08) | implementation doc | FULL TEXT | docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel |
| S15 | Google Cloud Storage docs, "Consistency" (fetched 2026-11-08) | implementation doc | FULL TEXT | cloud.google.com/storage/docs/consistency |
| S16 | Microsoft Learn, "Managing concurrency in Blob storage" (fetched 2026-11-08) | implementation doc | FULL TEXT | learn.microsoft.com/en-us/azure/storage/blobs/concurrency-manage |
| S17 | Jepsen, "Consistency Models" reference pages (index, linearizable, read-your-writes) | secondary engineering reference | FULL TEXT | jepsen.io/consistency/models |
| U1 | Gilbert & Lynch 2002 "Brewer's conjecture..." | - | UNREACHABLE in practice: PDF downloaded (CMU course copy) but text extraction produced unreadable font encoding; no claims based on it | users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf |
| U2 | Adya, Liskov, O'Neil ICDE 2000 "Generalized isolation level definitions" | - | UNREACHABLE (connection reset); thesis S6 used instead | pmg.csail.mit.edu/papers/icde00.pdf |

## 2. Extracted findings (verbatim quotes, locators)

### S1 Lamport 1986 – safe / regular / atomic registers (single writer)
Locator: Part II, Sec. 4 "The Nature of Asynchronous Communication", report pp. 19–21.
- Model assumption: "Writes cannot overlap (be concurrent with) one another because there is only one writer, and overlapping reads are assumed not to affect one another, so the only case left to consider is a read overlapping one or more writes."
- Safe: "a read not concurrent with any write obtains the correct value—that is, the most recently written one. No assumption is made about the value obtained by a read that overlaps a write, except that it must obtain one of the possible values of the register." Example: values {1,2,3}; a read overlapping a write 1->2 "could obtain any of these values, including 3."
- Regular: "a read that overlaps a write obtains either the old or new value ... More generally, a read that overlaps any series of writes obtains either the value before the first of the writes or one of the values being written."
- Atomic: "reads and writes behave as if they occur in some definite order."
- New-old inversion: "if two successive reads overlap the same write, then a regular register allows the first read to obtain the new value and the second read the old value, while this is forbidden with an atomic register."
- No assumption on process speed: "No such assumptions are made here about process speeds."
- Lamport: "These are the only three general classes of register that I have been able to think of."

### S2 Lamport 1979 – sequential consistency
Locator: p. 690, opening paragraphs.
- "the result of any execution is the same as if the operations of all the processors were executed in some sequential order, and the operations of each individual processor appear in this sequence in the order specified by its program. A multiprocessor satisfying this condition will be called sequentially consistent."
- Requirements R1 (each processor issues memory requests in program order) and R2 (single FIFO queue per memory module) given as sufficient implementation conditions.

### S3 Herlihy & Wing 1990 – linearizability
Locators: abstract; Sec 2.2 (p. 469); Sec 3.1 (Theorem 1).
- Abstract: "Linearizability provides the illusion that each operation applied by concurrent processes takes effect instantaneously at some point between its invocation and its response".
- Definition: "A history H is linearizable if it can be extended (by appending zero or more response events) to some history H' such that: L1: complete(H') is equivalent to some legal sequential history S, and L2: <H ⊆ <S." L2 "states that this apparent sequential interleaving respects the real-time precedence ordering of operations."
- Pending operations: "extending H to H' captures the notion that some pending invocations may have taken effect even though their responses have not yet been returned".
- Nondeterminism: "there may be more than one linearization S."
- Locality (Theorem 1): "H is linearizable if and only if, for each object x, H|x is linearizable." Contrast in Sec 1: "Unlike alternative correctness conditions such as sequential consistency or serializability, linearizability is a local property".
- Nonblocking: "processes invoking totally-defined operations are never forced to wait."

### S4 Terry et al. 1994 – session guarantees
Locators: Sec 1 (summary list), Sec 3.1 RYW, Sec 3.2 MR, 3.3 WFR, 3.4 MW.
- Summary: "Read Your Writes - read operations reflect previous writes. Monotonic Reads - successive reads reflect a nondecreasing set of writes. Writes Follow Reads - writes are propagated after reads on which they depend. Monotonic Writes - writes are propagated after writes that logically precede them."
- "These properties are 'guaranteed' in the sense that either the storage system ensures them for each read and write operation belonging to a session, or else it informs the calling application that the guarantee cannot be met."
- "RYW-guarantee: If Read R follows Write W in a session and R is performed at server S at time t, then W is included in DB(S,t)."
- Important qualification: "Applications are not guaranteed that a Read following a Write to the same data item will return the previously written value. In particular, Reads within the session may see other Writes that are performed outside the session."
- "MR-guarantee: If Read R1 occurs before R2 in a session and R1 accesses server S1 at time t1 and R2 accesses server S2 at time t2, then RelevantWrites(S1,t1,R1) is a subset of DB(S2,t2)."
- Context (Sec 1): weak consistency involves "lazy propagation of updates between servers and the possibility for clients to see inconsistent values when reading data from different replicas." Sessions "are not intended to correspond to atomic transactions".

### S5 Berenson et al. 1995 – ANSI phenomena critique
Locators: Sec 2.2 (P1–P3, broad vs strict), Table 1, Sec 4.2 (Snapshot Isolation), Sec 5 (A5A).
- P1 Dirty Read (English): "Transaction T1 modifies a data item. Another transaction T2 then reads that data item before T1 performs a COMMIT or ROLLBACK. If T1 then performs a ROLLBACK, T2 has read a data item that was never committed and so never really existed."
- P2 Fuzzy Read: "If T1 then attempts to reread the data item, it receives a modified value or discovers that the data item has been deleted."
- Broad vs strict: "P1: w1[x]...r2[x]...((c1 or a1) and (c2 or a2) in any order)"; "A1: w1[x]...r2[x]...(a1 and c2 in any order)". "Interpretation (2.2) specifies a phenomenon that might lead to an anomaly, while (2.1) specifies an actual anomaly."
- A5A Read Skew: "Suppose transaction T1 reads x, and then a second transaction T2 updates x and y to new values and commits. If now T1 reads y, it may see an inconsistent state". "A5A: r1[x]...w2[x]...w2[y]...c2...r1[y]...(c1 or a1)".
- Snapshot Isolation: transaction "reads data from a snapshot of the (committed) data as of the time the transaction started"; "never blocked attempting a read as long as the snapshot data from its Start-Timestamp can be maintained"; SI does not permit read skew (A5A) but admits write skew (A5B).

### S6 Adya 1999 – generalized (implementation-independent) phenomena
Locators: Abstract; Ch. 2 (preventative vs anomaly); Ch. 3 pp. 47–48 (G1a/G1b); Ch. 4 (G-single, PL-2+).
- Aim: "the first implementation-independent specifications of existing ANSI isolation levels".
- Critique of preventative interpretation: "the preventative interpretation is overly restrictive since it rules out serializable" histories and "disallows optimistic and multi-version mechanisms."
- "G1a: Aborted Reads. A history H exhibits phenomenon G1a if it contains an aborted transaction Ti and a committed transaction Tj such that Tj has read some object (maybe via a predicate) modified by Ti."
- "G1b: Intermediate Reads. A history H exhibits phenomenon G1b if it contains a committed transaction Tj that has read a version of object x ... written by transaction Ti that was not Ti's final modification of x."
- "G1b does not constrain the behavior of uncommitted transactions."
- "G-single: Single Anti-dependency Cycles ... DSG(H) contains a directed cycle with exactly one anti-dependency edge. Level PL-2+ proscribes G1 and G-single."

### S7 Viotti & Vukolic 2016 – survey
Locators: Abstract/Sec 1; Sec 2 (vis, ar relations); Sec 3.2 (weak/eventual); Sec 3.6 (staleness-based).
- Scope: "We overview more than 50 different consistency notions" and give "a partial order among different consistency predicates".
- Formal framework: "vis (visibility) is an acyclic natural relation that accounts for the propagation of write operations"; "ar (arbitration) is a total order on operations of the history that specifies how the system resolves conflicts".
- Weak consistency: "a weakly consistent system does not guarantee that reads return the most recent value written, and several (often underspecified) requirements have to be satisfied for a value to be returned."
- Eventual: "if no new write operations are invoked on the object, eventually all reads will return the same value." ... "it does not provide any guarantees about recency and ordering of operations."
- Staleness-based: "staleness based models allow reads to return old, stale written values"; "two common metrics are employed to measure staleness: (real) time and data (object) versions." "according to Δ-atomicity read operations may return either the value written by the last preceding write, or the value of a write operation returned up to Δ time units ago." "a timed serial consistent execution with Δ = 0 would in fact be linearizable."

### S8 Bailis et al. HAT
Locators: Abstract; Sec 5.1.3 (sticky); Sec 5.2.2 (Unachievable Recency Guarantees).
- "Read your writes requires that whenever a client reads a given data item after updating it, the read returns the updated value (or a value that overwrote the previously written value)."
- "Read your writes is not achievable in a highly available system." ... "if the client remains sticky with the server that executed T1, then we can disallow this scenario."
- "an indefinitely long partition can force an available system to violate any recency bound, so recency bounds are not enforceable by HAT systems". Linearizability "states that reads will return the last completed write to a data item".
- Achievable without availability loss: Read Committed, MAV, etc.; unachievable: preventing Lost Update / Write Skew and recency.

### S9 Bailis et al. PBS (empirical/theoretical staleness)
Locators: Abstract; Sec 1.
- PBS defines "t-visibility, or 'how eventual is eventual consistency?'" and "k-staleness, or 'how consistent is eventual consistency?'".
- Empirical: "eventually consistent systems frequently return consistent data within tens of milliseconds"; "switching from spinning disks to solid-state drives dramatically improved staleness (e.g., 1.85ms versus 45.5ms wait time for a 99.9% probability of consistent reads)". Applicability: Dynamo-style partial quorums, production latency distributions from LinkedIn/Yammer; probabilistic, not a guarantee.

### S10 Vogels 2008/2009
- Strong: "After the update completes, any subsequent access (by A, B, or C) will return the updated value."
- Weak: "The system does not guarantee that subsequent accesses will return the updated value ... The period between the update and the moment when it is guaranteed that any observer will always see the updated value is dubbed the inconsistency window."
- Eventual: "if no new updates are made to the object, eventually all accesses will return the last updated value."
- Quorum rule: "If W+R > N, then the write set and the read set always overlap and one can guarantee strong consistency." "If W+R <= N, then the system is vulnerable to reading from nodes that have not yet received the updates."
- Failover: "if the primary fails before the logs are shipped, reading from the promoted backup will produce old, inconsistent values."
- Evidence type: engineering essay, informal definitions.

### S11 POSIX.1-2017
- write(), DESCRIPTION: "After a write() to a regular file has successfully returned: Any successful read() from each byte position in the file that was modified by that write shall return the data specified by the write() for that position until such byte positions are again modified."
- XSH 2.9.7 Thread Interactions with Regular File Operations: listed functions incl. read(), pread(), readv(), write() "shall be atomic with respect to each other in the effects specified in POSIX.1-2017 when they operate on regular files or symbolic links ... If two threads each call one of these functions, each call shall either see all of the specified effects of the other call, or none of them."
- read() RATIONALE (informative, not normative): "I/O is intended to be atomic to ordinary files and pipes and FIFOs. Atomic means that all the bytes from a single operation that started out together end up together, without interleaving from other I/O operations. ... terminals are explicitly ... excepted ... The behavior for other device types is also left unspecified". Also: "there could be no guarantee of atomicity of reads of {PIPE_BUF} or any other size" for pipes/FIFOs.
- write(): pipe writes <= PIPE_BUF "shall not be interleaved"; larger "may have data interleaved, on arbitrary boundaries".

### S12/S13 NFSv4 / NFSv4.1 RFCs
- RFC 7530 Sec 10.3.1: "NFSv4 clients should not provide cached data to applications ... when it would not be valid to obtain or modify that same data via a READ or WRITE operation." In the absence of delegation: "cached data present on a client must be revalidated after doing an OPEN" (via change attribute) and "modified data must be flushed to the server before closing a file OPENed for write." Validation "must be done at least when the client's OPEN operation includes DENY=WRITE or BOTH". Warning that using time_modify "runs the risk of the client incorrectly marking stale data as valid."
- RFC 8881 Sec 13.10: "The NFSv4.1 protocol only provides close-to-open file data cache semantics; meaning that when the file is closed, all modified data is written to the server. When a subsequent OPEN of the file is done, the change attribute is inspected". Same section: a pNFS data server may return short read/EOF for an extended file; "the client will interpret such a response as a hole in the file, and the NFS client will substitute zeroes for the data."

### S14 Amazon S3 (implementation doc)
- "Amazon S3 provides strong read-after-write consistency for PUT and DELETE requests of objects in your Amazon S3 bucket in all AWS Regions."
- "Updates to a single key are atomic. ... you will get either the old data or the new data, but never partial or corrupt data."
- "Any read (GET or LIST request) that is initiated following the receipt of a successful PUT response will return the data written by the PUT request."
- Concurrent writes: "If two PUT requests are simultaneously made to the same key, the request with the latest timestamp wins." ; "Amazon S3 internally uses last-writer-wins semantics". "There is no way to make atomic updates across keys." "Bucket configurations have an eventual consistency model."
- Overlap example: "W2 does not finish before the start of R1. Therefore, R1 might return color = ruby or color = garnet."

### S15 Google Cloud Storage (implementation doc)
- "you never receive a 404 Not Found response or stale data for an object read-after-write or object read-after-metadata-update operation, even for buckets located in dual-regions or multi-regions." Unavailability case: "attempts to access the object return a retryable 500 error response."
- "Cached objects that are publicly readable might not exhibit strong consistency. ... the cached object is not updated or deleted until its cache lifetime expires." Default: "a publicly accessible object can be cached for up to 60 minutes."
- Eventually consistent: "Granting access to or revoking access from resources. Recreating buckets after deletion."

### S16 Azure Blob storage (implementation doc)
- "a strong consistency model that guarantees that after the service performs an insert or update operation, subsequent read or list operations return the latest update."
- "Azure Storage uses snapshot isolation to allow read operations concurrently with write operations within a single partition. Snapshot isolation guarantees that all read operations return a consistent snapshot of the data even while updates are occurring."
- ETag / If-Match; mismatch returns "HTTP status code 412 (Precondition Failed)".

### S17 Jepsen
- Hierarchy (adapted from Bailis et al. and Viotti & Vukolic): "strict serializable implies both serializability and linearizability, linearizability implies sequential consistency". "When we say that model x implies y, we mean that for every history where x holds, y does too".
- Linearizable page: "This model cannot be totally or sticky available"; "Linearizability is a single-object model, but the scope of 'an object' varies."
- RYW page: "read your writes does not apply to operations performed by different processes." Secondary source; used only to document its hierarchy/claims.

## 3. Existing models / classifications found
1. Lamport register hierarchy: safe < regular < atomic (single-writer; plus boolean/multivalued, single/multi-reader dimensions).
2. Sequential consistency (Lamport 1979): total order consistent with program order, no real-time constraint.
3. Linearizability (Herlihy & Wing): sequential order + real-time order; local; nonblocking. (Equivalent in effect to Lamport's atomic register for read/write registers; inference supported by HAT and Viotti treating safe/regular as weaker variants.)
4. Session guarantees (Terry 1994): RYW, MR, WFR, MW; defined over DB(S,t) server state; combine to causal (per HAT, Sec 5.1.3).
5. Vogels client-side taxonomy: strong / weak / eventual, with variants causal, RYW, session, monotonic read, monotonic write; server-side N/W/R quorum.
6. ANSI phenomena P0-P3, A1-A3, A5A read skew, A5B write skew, Snapshot Isolation (Berenson).
7. Adya generalized phenomena G0, G1a, G1b, G1c, G-single, PL-levels (DSG-based).
8. Viotti & Vukolic partial order of >50 non-transactional models, axiomatized by vis/ar relations; staleness families (Δ-atomicity, timed, bounded staleness, k-atomicity, PBS).
9. HAT classification: highly available / sticky available / unavailable models.
10. PBS: probabilistic k-staleness, t-visibility (WARS model).
11. NFS close-to-open cache semantics (normative); POSIX read-after-write per byte position + 2.9.7 all-or-nothing visibility between threads.
12. Cloud object store models: per-key strong read-after-write, single-key atomic replacement, last-writer-wins, eventual for config/ACL, cache exceptions.

## 4. Convergences
- Three formal sources (Lamport 1986, Herlihy & Wing, Viotti) agree the key question is what a read overlapping a write may return; the answer ranges from "any possible value" (safe) to "old or new" (regular) to "consistent with a single total order respecting real time" (atomic/linearizable).
- Object-store docs (S3 "old data or the new data, but never partial"; S3 overlap example "R1 might return ruby or garnet") describe per-key behavior matching regular/atomic-style semantics. Inference: the docs do not say whether two sequential overlapping reads can see new-then-old (the regular vs atomic distinction); this remains unspecified in the vendor text.
- Eventual consistency defined only as convergence in absence of updates (Vogels, Viotti), with no recency bound; HAT proves recency bounds cannot be enforced under indefinite partition.

## 5. Contradictions / tensions
- RYW wording differs: Terry "Applications are not guaranteed that a Read following a Write to the same data item will return the previously written value" (other writes may intervene) vs Vogels "always accesses the updated value and will never see an older value"; HAT adds "(or a value that overwrote the previously written value)". Vogels also calls RYW "a special case of the causal consistency model" while HAT says causal = combination of all session guarantees.
- "Strong consistency" in Vogels ("after the update completes, any subsequent access") says nothing about reads concurrent with the update, unlike linearizability.
- Vogels' "W+R > N ... one can guarantee strong consistency" is an engineering rule; the formal sources treat linearizability as requiring more than quorum overlap (inference: under concurrent writes/read repair, overlap alone does not give atomicity; not verified from a full text in this track). PBS treats W+R<=N as probabilistic.
- "Snapshot isolation" in Azure docs refers to single-partition read snapshots; Berenson's SI is a multi-version transactional level permitting write skew. Same term, different scope.
- Berenson's preventative (broad) interpretation vs Adya's claim that it is overly restrictive and excludes optimistic/multiversion schemes.
- POSIX atomicity of read() for regular files: the normative 2.9.7 states all-or-nothing effects between threads, but the "atomic ... without interleaving" sentence is in RATIONALE (informative) and excludes terminals and other devices.
- Viotti attributes the first definition of eventual consistency to Terry et al. 1994; the session-guarantees paper read here does not itself define "eventual consistency" in the text read (the term appears in the companion Bayou literature). Flag: attribution not verified.

## 6. Gaps
- COVERAGE-GAP: Gilbert & Lynch 2002 (CAP) unreadable; Adya ICDE 2000 unreachable (thesis used).
- COVERAGE-GAP: Lamport 1986 Part I formal precedence model not extracted in detail.
- COVERAGE-GAP: Linux/ext4 or other kernel docs on concurrent read/write tearing (outside POSIX) not consulted.
- GENUINE-GAP (inference): vendor object-store docs give informal statements, no formal model (no linearizability statement, no definition of behaviour for ranged/partial GETs racing with overwrite, beyond "never partial").
- GENUINE-GAP (inference): NFS close-to-open defines only open/close points; reads between those points on different clients are not constrained by RFC text read here.
- GENUINE-GAP: no source here addresses multi-object reads of a byte stream spanning multiple keys/blocks except S3 "no way to make atomic updates across keys" and transactional literature.
