# Track 12: Reads from untrusted or adversarial storage

Scope: freshness, rollback, fork consistency, TOCTOU/double-fetch, read-induced disturbance, remote possession proofs, and archival fixity as the "periodic read of bits nobody reads".
Downloads: `/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/12-adversarial-untrusted-storage-reads/` (PDFs converted with pdftotext; quotes below copied from those text extractions).

## 1. Sources consulted and access status

| # | Source | URL read | Access | Type |
|---|---|---|---|---|
| S1 | Li, Krohn, Mazieres, Shasha. Secure Untrusted Data Repository (SUNDR). OSDI 2004 | usenix.org/legacy/events/osdi04/tech/full_papers/li_j/li_j.pdf | full text | peer-reviewed system + proof claim |
| S2 | Cachin, Shelat, Shraer. Efficient Fork-Linearizable Access to Untrusted Shared Memory. PODC 2007 | csaws.cs.technion.ac.il/~shralex/fp147-cachin.pdf | full text (author copy) | theoretical |
| S3 | Cachin, Keidar, Shraer. Fail-Aware Untrusted Storage. SICOMP version (author copy dated 25 Jan 2011; prelim. DSN 2009) | people.csail.mit.edu/idish/ftp/faust-sicomp.pdf | full text | theoretical |
| S4 | Malkhi, Reiter. Byzantine quorum systems. Distributed Computing 11:203-213, 1998 | ilyasergey.net/CS6213/_static/03-bft/byzquorums.pdf (course mirror of publisher PDF) | full text | theoretical |
| S5 | Parno, Lorch, Douceur, Mickens, McCune. Memoir: Practical State Continuity for Protected Modules. IEEE S&P 2011 | andrew.cmu.edu/user/bparno/papers/memoir.pdf | full text | peer-reviewed system |
| S6 | Matetic et al. ROTE: Rollback Protection for Trusted Execution. USENIX Security 2017 | usenix.org/system/files/conference/usenixsecurity17/sec17-matetic.pdf | full text | peer-reviewed system + measurement |
| S7 | Linux kernel docs, dm-verity (Documentation/admin-guide/device-mapper/verity.rst, master, fetched 2026-11-08) | raw.githubusercontent.com/torvalds/linux/master/... | full text | implementation-doc |
| S8 | Linux kernel docs, fs-verity (Documentation/filesystems/fsverity.rst, master, fetched 2026-11-08) | raw.githubusercontent.com/torvalds/linux/master/... | full text | implementation-doc |
| S9 | Wang, Krinke, Lu, Li, Dodier-Lazaro. How Double-Fetch Situations turn into Double-Fetch Vulnerabilities. USENIX Security 2017 | usenix.org/system/files/conference/usenixsecurity17/sec17-wang.pdf | full text | peer-reviewed empirical |
| S10 | Bishop. Race Conditions, Files, and Security Flaws; or the Tortoise and the Hare Redux. UC Davis CSE-95-8, Sept 1995 (tech-report precursor of Bishop & Dilger, Computing Systems 9(2), 1996) | seclab.cs.ucdavis.edu/projects/vulnerabilities/scriv/ucd-ecs-95-08.pdf | full text of the TR; the 1996 journal version itself NOT read | engineering/analysis |
| S11 | Kim et al. Flipping Bits in Memory Without Accessing Them. ISCA 2014 | users.ece.cmu.edu/~yoonguk/papers/kim-isca14.pdf | full text | peer-reviewed empirical |
| S12 | Cai, Luo, Ghose, Haratsch, Mai, Mutlu. Read Disturb Errors in MLC NAND Flash Memory. DSN 2015 | users.ece.cmu.edu/~omutlu/pub/flash-read-disturb-errors_dsn15.pdf | full text | peer-reviewed empirical |
| S13 | Juels, Kaliski. PORs: Proofs of Retrievability for Large Files. (preprint Aug 2007, 22 pp; CCS 2007) | arijuels.com/wp-content/uploads/2013/09/JK07.pdf | full text (preprint) | theoretical/crypto |
| S14 | Ateniese et al. Provable Data Possession at Untrusted Stores. CCS 2007 | people.eecs.berkeley.edu/~dawnsong/papers/p598-ateniese.pdf | full text (conference version) | theoretical/crypto + experiments |
| S15 | Maniatis, Roussopoulos, Giuli, Rosenthal, Baker, Muliadi. Preserving Peer Replicas By Rate-Limited Sampled Voting in LOCKSS (arXiv cs/0303026v3, long version of SOSP 2003) | arxiv.org/pdf/cs/0303026 | full text | peer-reviewed system + simulation |
| S16 | PREMIS Data Dictionary for Preservation Metadata, version 3.0, June 2015 | loc.gov/standards/premis/v3/premis-3-0-final.pdf | full text (relevant sections) | normative (community standard) |
| S17 | CCSDS 650.0-M-2 Reference Model for an OAIS (Magenta Book, June 2012; = ISO 14721:2012) | public.ccsds.org/Pubs/650x0m2.pdf | full text (relevant sections) | normative |

Unreachable / not read:
- Mazieres and Shasha, Building secure file systems out of Byzantine storage, PODC 2002: author URLs tried (scs.stanford.edu ...mazieres:fork.pdf/.ps) returned 404. UNREACHABLE; known only via S2/S3 citations.
- IACR ePrint 2007/202 (PDP full version) and 2007/243: 403 (site block). Conference version of PDP read instead; POR preprint read from author site.
- Merkle 1987 (A digital signature based on a conventional encryption function) and Tamassia 2003 (Authenticated data structures): not attempted for time; COVERAGE-GAP. Merkle-tree usage is documented here only via S7/S8.
- ISO 16363 / CCSDS 652.0-M-1 (TDR audit): not attempted; COVERAGE-GAP.
- LOCKSS ACM TOCS 2005 version: not read; arXiv long SOSP version used.
- Bishop & Dilger 1996 journal paper: not read; Bishop 1995 TR read.
- Evil-USB / malicious-firmware access-pattern-dependent content: no primary source read; COVERAGE-GAP.
- Cai et al. HPCA 2017 (Vulnerabilities in MLC NAND flash: program interference and read disturb attacks/exploitation): not read; COVERAGE-GAP.

## 2. Extracted findings (verbatim quotes, locators)

### Fork consistency / untrusted single server
- S1 SUNDR, §3 intro (p.122): "under fork consistency, a dishonest server could cause a fetch by a user A to miss a modify by B. However, either user will detect the attack upon seeing a subsequent operation by the other. Thus, to perpetuate the deception, the server must fork the two user's views of the file system."
- S1 §3.2 (p.123): "Fork consistency is the strongest notion of integrity possible without on-line trusted parties. ... If B doesn't know whether A has accessed the file system, it cannot detect an attack in which the server simply discards A's changes. Fork consistency implies this is the only type of undetectable attack by the server on file integrity or consistency."
  - Note: "strongest possible" is asserted in prose by the authors, not proved in this paper (proof of SUNDR achieving fork consistency is cited to [17]).
- S1 §3.2: freshness bounded via a "time stamp box" with permission to write a single file, updated "every 5 seconds".
- S1 §8 (Related work): "SUNDR provides weaker freshness guarantees than BFS, because of the possibility that a malicious SUNDR server can fork the file system state".
- S1 §9: "the server cannot tamper with, inject, re-order, or suppress file writes in any other way."
- S2 abstract: "the server might complete a write operation of one client, but respond with stale data to another client." ... "We also prove that in every such protocol, a reader must wait for a concurrent writer." ... fork-linearizability "is neither stronger nor weaker than sequential consistency."
- S2 Theorem 1 (§3.1): "Let P be a protocol for emulating n ≥ 1 SWMR registers on a Byzantine server S with fork-linearizability. Then there is an execution of P where S is correct and an operation of some client cannot complete unless another client takes some steps." Followed by: "no fork-linearizable emulation of n ≥ 1 SWMR registers on a Byzantine server is wait-free."
- S2 Theorem 4: "There is no protocol that emulates n > 1 SWMR registers on a Byzantine server with sequential consistency." (split-brain execution where reads return ⊥ / old values).
- S3 §1: "Linearizability cannot be ensured either, since the server may respond with an outdated return value to a client, omitting more recent update operations that affected its state." and "it is impossible to guarantee that every operation is live, as the server can simply ignore client requests."
- S3 §4.1 Def. 7 (Fork-linearizability): views π_i preserve real-time order; "(No-join) For every client Cj and every operation o ∈ πi ∩ πj, it holds that πi|o = πj|o." Fork-*-linearizability (Li & Mazieres) replaces no-join with at-most-one-join.
- S3 §4.2 Def. 8 (Weak fork-linearizability): weak real-time order (last op of each client exempt), explicit causal consistency, at-most-one-join. "every fork-linearizable history is also weakly fork-linearizable." Fig. 3 example: C2 reads r2(X1)→⊥ after w1(X1,u) completed, then reads u.
- S3 abstract/§1: FAUST "guarantees consistency (linearizability) and liveness (wait-freedom) of all operations" when provider correct, is always causally consistent, and gives "accurate and complete consistency and failure detection"; stable operations notified asynchronously.

### Byzantine replicated storage
- S4 §4: masking quorums; "every pair of quorums intersect in at least 2f + 1 elements, and thus in f + 1 correct ones. If a read operation accepts only a value returned by at least f + 1 servers, then any accepted value was returned by at least one correct server." Corollary 4.4: masking quorum system exists for threshold f "iff n > 4f". Corollary 5.5 (dissemination, self-verifying data e.g. signed values): "iff n > 3f". Read semantics: "the protocol above implements a multi-writer multi-reader safe variable"; "A failure value (⊥) may be returned when some write overlaps a read operation."
  - Dissemination servers "can fail to redistribute but cannot undetectably alter" self-verifying data (Summary).

### Rollback of sealed state
- S5 Memoir abstract: integrity+confidentiality insufficient "since, e.g., software may err if its state is rolled back to a correct but stale version." §I: "In a rollback attack, untrusted code violates the safety of state continuity by providing the TCB with an old state snapshot. The snapshot is internally consistent and cryptographically sound, but running the module on that snapshot incorrectly ignores the module's execution history." Distinguished from replay: "In a rollback attack, the recipient's state itself is reverted to a prior state."
- S5 §I: monotonic-counter strawman not crash-resilient: "if the computer crashes between the increment of the trusted counter and the persistent write of the new module state, the module becomes unusable."
- S5 §II-B adversary: "full control over the bulk persistent storage facilities on the machine, meaning he can modify, delete, and retrieve old versions of any data placed in bulk storage."
- S5 §II-C: TPM NVRAM read 9.8–14.8 ms, write 33.9–82.4 ms, ~100,000 write cycles; "Writing to NVRAM once every second would exhaust its write cycles in less than 28 hours."
- S6 ROTE §1: "In a rollback attack a malicious OS replaces the latest sealed data with an older encrypted and authenticated version. Enclaves cannot easily detect this replay, because the processor is unable to maintain persistent state across enclave executions". Forking variant: "create two instances of the same enclave and route update requests to one instance and read requests to the other." §2.3: "The OS reads data from the second instance me ← Read(i2) which has an outdated state". SGX counter writes measured "slow (80-250 ms)"; limit "reached within just few days of continuous system use". ROTE property "all-or-nothing rollback"; abstract: "the only way to violate integrity is to reset all participating platforms to their initial state."

### Read-path verification (implementation docs)
- S7 dm-verity: "This target is read-only." Theory of operation: "all hashes will be verified on-demand during disk access. If they cannot be verified up to the root node of the tree, the root hash, then the I/O will fail." Root hash "should be trusted as there is no other authenticity" (parameter description). Corruption-response options: ignore_corruption ("Log corrupted blocks, but allow read operations to proceed normally"), restart_on_corruption, panic_on_corruption, restart_on_error, panic_on_error; FEC via RS(255,k). check_at_most_once: "only offline tampering of the data device's content will be detected, not online tampering."
- S8 fs-verity, §Use cases: "By itself, fs-verity only provides integrity protection, i.e. detection of accidental (non-malicious) corruption." ... "Unlike an ahead-of-time hash, fs-verity also re-verifies data each time it's paged in. This ensures that malicious disk firmware can't undetectably change the contents of the file at runtime." §Accessing verity files: "Reads of data that doesn't match the verity Merkle tree will fail with EIO (for read()) or SIGBUS (for mmap() reads)." Direct I/O falls back to buffered; DAX unsupported "because this would circumvent the data verification." Implementation section: verification before folio marked Uptodate; hash blocks may be cached.
  - Tension (inference): "re-verifies data each time it's paged in" — data cached in the page cache is not re-read from the device, so verification is per page-in, not per read() call.

### TOCTOU / double-fetch
- S10 Bishop TR, Detailed Discussion: by name "the binding is both late and transient (as it is done anew at each reference)"; by descriptor "the binding is both early and permanent." Conclusion: "time-of-check to time-of-use flaw (TOCTTOU flaw) and was first identified in 1974"; "Absent kernel modification, one cannot eliminate the problem".
- S9 abstract: "we identified 90 double fetches in the Linux kernel. 57 of these occur in drivers"; "six previously unknown double-fetch bugs, four of them in drivers, three of which are exploitable double-fetch vulnerabilities." §1: "A double-fetch bug occurs when the kernel reads and uses the same value that resides in the user space twice (expecting it to be identical both times), while a concurrently running user thread can modify the value in the time window between the two kernel reads." §2 classification: benign double fetch / harmful double fetch (double-fetch bug) / double-fetch vulnerability.

### Reads that damage other data
- S11 abstract: "By reading from the same address in DRAM, we show that it is possible to corrupt data in nearby addresses." "110 out of 129" modules; "as few as 139K accesses to induce an error"; "up to one in every 1.7K cells is susceptible"; user-level program on Intel/AMD.
- S12 abstract: "read disturb, where a read to one row of cells impacts the threshold voltages of unread flash cells in different rows of the same block." Finding: "probability of read disturb errors increases with both higher wear-out and higher pass-through voltage levels." Mitigation +21% endurance; recovery reduces RBER by 36%. The paper is a reliability characterization; no attack/adversary model found (grep for attack/malicious/security found none relevant).

### Possession / retrievability without reading everything
- S13 POR abstract: "A POR scheme enables an archive or back-up service (prover) to produce a concise proof that a user (verifier) can retrieve a target file F". Sentinel scheme + ECC; Example 1: three random bit corruptions likely undetected by POR but repaired by ECC; Example 2: 20% corruption detected "with probability about 1/5" per sentinel.
- S14 PDP §1: "It is insufficient to detect that data have been modified or deleted when accessing the data, because it may be too late to recover lost or damaged data. Archival storage servers retain tremendous amounts of data, little of which are accessed." "for a file with n = 10,000 blocks, if S has deleted 1% of the blocks, then C can detect server misbehavior with probability greater than 99% by asking proof of possession for only 460 randomly selected blocks (representing 4.6% of n)."

### Archival fixity and auditing
- S17 OAIS §1.7.2: "Fixity Information: The information which documents the mechanisms that ensure that the Content Information object has not been altered in an undocumented manner. An example is a Cyclical Redundancy Check (CRC) code for a file." §4.1.1.3 Archival Storage: "The Error Checking function provides statistically acceptable assurance that no components of the AIP are corrupted in Archival Storage or during any internal Archival Storage data transfer." ... "The storage facility procedures should provide for random verification of the integrity of Data Objects using CRCs or some other error checking mechanism." §4.2.1.4.2: Fixity Information "does not include the integrity preserving mechanisms provided by the OAIS underlying services, error protection supplied by the media and device drivers".
- S16 PREMIS 3.0, 1.5.2 fixity usage notes (PDF p.69): "To perform a fixity check, a message digest calculated at some earlier time is compared with a message digest calculated at a later time. If the digests are the same, the object was not altered in the interim." The term "checksum" "is more correctly used for the product of a cyclical redundancy check (CRC), whereas the term 'message digest' refers to the result of a cryptographic hash function, which is what is referred to here." Fixity check recorded as an Event. Special topic (PDF p.268): fixity "does not address the object's integrity or authenticity". Glossary (PDF p.280): "Fixity: Property of a Digital Object that indicates it has not changed between two points in time."
- S15 LOCKSS §2: "Cheap storage is unreliable." "No long-term secrets." "Use inertia." §3: peers vote on "the hash of a specified part of the content"; publishers "do not currently sign the material they distribute". §4.2.3: "Loyal peers call polls autonomously and infrequently, but often enough to prevent random undetected damage from affecting readers significantly." Abstract: goal that adversaries "have only a small probability of causing irrecoverable damage before being detected."

## 3. Existing models / classifications found (source terminology)
- Consistency hierarchy for single untrusted server: linearizability (correct server) ⊃ fork-linearizability (= fork consistency; no-join) ⊂ weak fork-linearizability; fork-*-linearizability (at-most-one-join); fetch-modify consistency (SUNDR). Impossibility results: no wait-free fork-linearizable emulation (S2 Thm 1); no sequentially-consistent emulation on a Byzantine server (S2 Thm 4).
- Fail-aware untrusted service (S3): operation completion vs stability notification vs failure notification.
- Byzantine quorum classes (S4): masking (n>4f), dissemination for self-verifying data (n>3f), opaque masking; read semantics = safe variable.
- State continuity = safety + liveness (S5); rollback vs replay distinction (S5); rollback vs forking attack (S6); all-or-nothing rollback (S6).
- Name binding: late+transient vs early+permanent (S10); TOCTTOU.
- Double fetch: benign / harmful (bug) / vulnerability (S9).
- Disturbance errors (DRAM, S11); read disturb (NAND, S12).
- PDP vs POR (S13/S14): possession-by-sampling vs retrievability via ECC + sentinels/MACs (POR as a proof of knowledge variant with extractor).
- Archival: Fixity Information (OAIS) / fixity, fixity check event (PREMIS); OAIS Error Checking function; LOCKSS opinion polls with rate limiting.

## 4. Convergences
- Integrity is not freshness: SUNDR (server can discard A's changes undetectably), Memoir ("correct but stale version"), ROTE (older authenticated sealed data), FAUST ("outdated return value") all say authenticated content can still be stale. Detection of staleness requires trusted state (counter/NVRAM), an online trusted party (time-stamp box, consistency server), replication (ROTE, BQS), or client-to-client communication.
- Forking/split-brain appears in both untrusted-storage theory (S1-S3) and TEEs (S6 forking attack via two enclave instances) — independent literatures, same concept (inference: convergence noted, not stated by sources jointly; ROTE does use "forking attack").
- Read-path verification at granularity of the read (dm-verity/fs-verity per block, SUNDR per fetch) vs detection by periodic sampled audit when nobody reads (PDP, POR, OAIS random verification, LOCKSS polls).

## 5. Contradictions / tensions
- OAIS gives a CRC as the example of Fixity Information; PREMIS says "message digest" means a cryptographic hash and that "checksum" is more correctly the CRC product. CRC gives no protection against a deliberate modifier (inference).
- fs-verity: "By itself, fs-verity only provides integrity protection, i.e. detection of accidental (non-malicious) corruption" vs same doc: re-verification "ensures that malicious disk firmware can't undetectably change the contents of the file at runtime." Reconcilable: malicious-firmware protection assumes the file digest is authenticated by another mechanism (inference).
- dm-verity default behavior fails the I/O, yet ignore_corruption lets reads "proceed normally"; check_at_most_once trades online-tamper detection. A "verified" device's read guarantee depends on configuration.
- Lead framing "flash read-disturb exploitation (Cai et al., DSN 2015)": the DSN 2015 paper is a reliability characterization with no adversary model; exploitation is in other work not read here.
- SUNDR claims fork consistency is "the strongest notion of integrity possible without on-line trusted parties"; later work (S2, S3) shows fork-linearizability forces blocking even with a correct server, and introduces weaker notions to regain wait-freedom: the "strongest" notion has a liveness cost.
- PDP: detecting modification at access time "may be too late"; dm-verity/fs-verity rely precisely on access-time detection. Different threat goals (recoverability vs not consuming bad data).

## 6. Gaps
- GENUINE-GAP (inference, within sources read): none of the fixity standards (OAIS, PREMIS) define fixity against an adversary who can alter both object and stored digest; LOCKSS addresses this with replication/voting, not the standards.
- GENUINE-GAP: no source read gives a read-semantics model for access-pattern-dependent malicious devices (content that changes depending on whether it is being verified vs consumed).
- COVERAGE-GAP: Merkle 1987, Tamassia 2003, Mazieres & Shasha 2002, ISO 16363, LOCKSS TOCS 2005, Bishop & Dilger 1996 journal, evil-USB/firmware work, Cai et al. HPCA 2017, Rowhammer exploitation (Seaborn/Dullien), Flip Feng Shui, TPM 2.0 NV counters spec.
