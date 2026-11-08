# Binary Stream Read Behavior Foundations - transfer protocols

A follow-up to `reports/Binary Stream Read Behavior Foundations.md`. That report is left unchanged so the two can be compared.

- Brief: `briefs/Binary Stream Read Behavior Foundations - transfer protocols.md`
- Notes and verification record: `research_notes/Binary Stream Read Behavior Foundations - transfer protocols/`
- Date: 2026-11-08

The task boundary of the original brief still applies: this report describes existing knowledge and does **not** propose a taxonomy. Track 15 is the exception in kind only. It tests whether certain products already *have* a taxonomy; it does not design one.

---

## 0. Why this follow-up exists, and method

**Coverage gap in the earlier report.** Its §B.7 covered HTTP, NFSv4.1, SMB2, iSCSI residuals and cloud object stores. It left out:

- the file-transfer protocols: FTP/FTPS, SFTP, SCP, TFTP, rsync, 9P and BitTorrent;
- most remote block protocols: NBD, NVMe-oF/NVMe-TCP, iSCSI error recovery, iSER and Ceph RADOS;
- the documented taxonomies of data-access layers, such as Apache OpenDAL.

The earlier report's §F.2 does not list these gaps. The cause was how that research was scoped: the starting leads for each track named no such protocols or products, and no track covered access layers. It does not mean the literature is thin.

**Tracks.**

| Track | Scope |
|---|---|
| 13 | File-transfer and remote file-access protocols |
| 14 | Remote and networked block-storage protocols |
| 15 | Whether data-access layers have a defined, principled, foundational and maintained taxonomy |

For track 15, a taxonomy had to meet four criteria:

- **C1 Defined:** each class has a written definition.
- **C2 Principled:** the axis the classes are sorted on is stated.
- **C3 Foundational:** backends must map onto it, and the mapping is documented and visible in code.
- **C4 Maintained:** there is a design record or versioning.

Each candidate got one verdict: CONFIRMED, PARTIAL or NOT FOUND. Candidates that were only screened got one line each.

**Method.** The same as the earlier report:

- research agents ran at medium effort and read the sources in full;
- each claim was tied to one source the track had read, with a verbatim quote and a locator;
- each claim then went to three verifiers, checking fidelity, overreach and currency;
- a claim is killed on ≥2 refutes and contested on 1.

The tracks compared their findings with the earlier report only after extracting them on their own.

**Outcome.**

- **Claims:** 66 in total: 64 verified, 2 contested, none killed.
- **Sources:** 43 distinct: 34 read in full, 6 partially, 3 unreachable. Unreachable sources carry no claims.

**Conventions.** These are unchanged:

- `[NN-Cn]` refers to the matrix in §E of this report.
- A bare ID in the range 01–12 (for example `07-C4`) refers to the earlier report's matrix.
- *(inference)* marks reasoning that goes beyond what a source says.
- *(verifier-reported)* marks information from the verification pass that no research track re-read.

---

## A. Research landscape (additions)

| # | Body of knowledge | What it contributes to understanding reads | Typical sources | Scope limits |
|---|---|---|---|---|
| 13 | **File-transfer and remote file-access protocols** | How end of data is signalled (connection close, short block, status code), byte transformation, restart offsets, reply-code classes, pipelining, checks for source changes, end-to-end integrity in practice | RFC 959/1123/3659/4217/1350/2347/2348; SFTP drafts -02 and -13; OpenSSH PROTOCOL, source code and release notes; Plan 9 read(5); BEP 3; rsync(1); Liu et al. HPDC 2018; RIVA | SFTP and SCP have no ratified standard; there are almost no field studies |
| 14 | **Remote block-storage protocols** | Read reply models (simple/structured), ordering of read data, digest scope and failure handling, retry categories after loss of communication, path states, error-recovery levels | NBD proto.md; NVMe/TCP Transport and NVMe Base specs; RFC 7143; RFC 7145; Jiang et al. FAST 2008; Linux NVMe host driver; Ceph librados docs | FC/FCP, SRP and AoE texts unreachable; NBD is a project-level spec |
| 15 | **Taxonomies of data-access layers** | Classifications of access outcomes and retryability that are documented and enforced across many backends | OpenDAL source, RFCs and internal docs; Hadoop FileSystem specification; Arrow `object_store` source; fsspec source | Implementation documentation only (source priority 4); recent and still changing |

---

## B. Established concepts and findings

### B.13 File-transfer and remote file-access protocols

**FTP (RFC 959, RFC 3659).**

- **End of file.** In stream mode with file structure, the sender closes the data connection to signal end of file, and every byte is data [13-C1]. A close that happens too early differs from a real end of file only through the control-channel reply: 226 versus 426/451 *(inference, track 13)*.
- **Block mode.** Block mode has a descriptor flag for "suspected errors in data block". With it, data can be delivered while marked unreliable [13-C2]. Block mode is rarely deployed.
- **Integrity.** FTP itself has "no provision for detecting bits lost or scrambled"; it leaves this to TCP [13-C3]. Earlier report 07-C18 shows that TCP checksums miss errors.
- **Restart.** Base RFC 959 defines restart only for block and compressed modes [13-C3]. RFC 3659 later added restart in stream mode by octet offset.
- **Reply codes.** Replies are split into transient negative completions (4yz, which may be repeated unchanged) and permanent ones (5yz). The RFC concedes "It is difficult to assign a meaning to 'transient'" [13-C4].
- **SIZE.** SIZE must report exactly the number of octets that *would be transmitted* under the current TYPE, MODE and STRU settings. This need not equal the stored size [13-C5].
- **Stream-mode restart offsets.** An octet offset is an unambiguous restart point only in stream mode [13-C6]. A misplaced REST may be rejected, deferred or silently ignored.
- **Source changes.** Nothing detects a change to the source during a transfer. Before resuming, RFC 3659 only allows a heuristic: compare modification times (MDTM) [13-C7].

**FTPS (RFC 4217).** With protection level PROT C, the data connection has no integrity protection. RFC 4217 has no normative text on detecting truncation of a protected data connection [13-C8].

**SFTP.** SFTP has no ratified standard. All versions exist only as expired drafts.

- **v3 (draft -02, what OpenSSH implements).**
  - A READ returns up to `len` bytes. End of file, or an error before any data, gives a status reply. Full reads are "guaranteed" only for normal disk files [13-C9].
  - Replies to outstanding requests may arrive in any order and are matched by request id. Overlapping reads and writes must behave as if serialised [13-C10].
  - Status codes include EOF, a generic FAILURE, and the client-local pseudo-errors CONNECTION_LOST and NO_CONNECTION. There is no transient/permanent grouping [13-C11].
- **v6 (draft -13).** v6 allows short replies more broadly (at end of file, on error, or under buffer limits) and adds an optional end-of-file flag. v3 already allowed short reads for files other than normal disk files [13-C12].
- **OpenSSH.** OpenSSH documents that servers usually answer large reads with shorter DATA replies [13-C13]. Its server caps `len` and returns the result of a single read(2). This contradicts the v3 draft's "guaranteed" full read in practice.
- **OpenSSH client (contested claim, corrected).** The client re-requests the remainder after a short reply and treats any status other than EOF as an error. On error or interrupt it truncates the local file to the highest contiguous offset. If replies were reordered, it only *logs* that the download cannot be resumed reliably; it does not refuse [13-C14].

**SCP.** SCP has no specification. OpenSSH calls it "outdated" and not readily fixable. CVE-2019-6111 shows that a hostile server could send files that did not match the client's request. OpenSSH 9.0 made SFTP the default transport [13-C15].

**TFTP.**

- **End of transfer.** A DATA packet shorter than the block size ends the transfer. A sender that times out after the last packet cannot tell whether the transfer succeeded, and ERROR packets are never retransmitted [13-C16].
- **Blocksize option.** With the RFC 2348 blocksize option, a file whose size is an exact multiple of the block size ends with a zero-length DATA packet [13-C17].
- **Sorcerer's Apprentice bug.** This bug "may cause" heavy duplicate traffic and timeouts, but it does not corrupt data. RFC 1123 makes the fix mandatory [13-C18].

**Other protocols.**

- **9P.** An Rread may return fewer bytes than requested, and a read at or past end of file returns zero bytes. The `iounit` value, when non-zero, *guarantees* the size of an atomic transfer [13-C19].
- **BitTorrent.** Each piece is checked against a SHA-1 hash from the metainfo before a peer announces it [13-C20].
- **rsync.** rsync verifies each file with a whole-file checksum computed during the transfer. However, `--append` does not verify content already on the receiver, and before rsync 3.0.0 `--append` behaved like `--append-verify` [13-C21].

**Empirical evidence.**

- **Globus logs.** In four years of Globus/GridFTP logs, about 1 in 121 transfers with integrity checking had at least one checksum error, roughly one failure per 1.26 TB. Changes to a file during transfer cannot be told apart from corruption [13-C22].
- **RIVA.** Checksums computed after a transfer often read from the page cache and so miss undetected disk *write* errors. RIVA's fault-injection tests covered write errors only; read errors were argued analytically [13-C23].

### B.14 Remote and networked block-storage protocols

**NBD** (project-level specification `proto.md`, using RFC 2119 keywords; not ratified by any standards body).

- **Simple replies.** A read cannot report partial success. If an error turns up after a zero-error reply header has been sent, the server must hard-disconnect [14-C1].
- **Structured replies.** Content chunks may arrive in any order. They must not overlap, and with the DF flag at most one chunk is sent. Without an error the whole requested range must be covered [14-C2].
- **Error chunks.**
  - `ERROR` invalidates the entire reply.
  - `ERROR_OFFSET` localises the error. Partial success can then be inferred, but only if every error carries an offset [14-C3].
- **Reply ordering.** Replies may come back out of request order and can be interleaved across requests. Clients correlate them by a cookie [14-C4].
- **No end of file or short read.** NBD has neither for READ. Reads beyond the export, or misaligned reads, SHOULD fail with EINVAL. Error values are errno-derived. A few carry retry hints, such as retrying after EOVERFLOW with smaller requests, but there is no explicit transient/permanent class *(inference from what the spec omits)* [14-C5].
- **BLOCK_STATUS.** A BLOCK_STATUS reply may cover less than the requested range when looking it up would be too costly [14-C6].

**NVMe over TCP and NVMe Base** (NVMe/TCP Rev 1.1 and Base 2.1; *verifier-reported* Rev 1.3 and Base 2.4, 2026, with the same text).

- **Ordering of read data.** The C2HData PDUs that carry read data must have strictly sequential offsets within a command. A gap is a fatal transport error. PDUs of different commands may interleave [14-C7].
- **Digest errors.**
  - A header digest error is fatal and ends the connection.
  - A data digest error in read data fails that command with Transient Transport Error, *even if the controller reported success* [14-C8].
- **Transient Transport Error.** This status is likely to succeed on retry. After four or more failures it "should" be treated as persistent [14-C9].
- **DNR and CRD.** The DNR bit says that resubmitting to *any* controller in the subsystem is expected to fail. CRD gives an advisory retry delay that applies only with ACRE enabled [14-C10].
- **Path errors.** Path-related errors "should" be retried on another path. ANA Inaccessible and ANA Persistent Loss mean the command should not go back to the same controller. ANA Transition means wait for the transition. Internal Path Error defers to DNR [14-C11].
- **Retry after loss of communication.** A Read is an *Unrestricted Retry* command only if certain effects bits are cleared. Writes are Delayed Retry commands [14-C12].

**iSCSI and iSER (RFC 7143, RFC 7145).**

- **Error-recovery levels.** iSCSI error recovery is a negotiated hierarchy of three levels. Only level 0 (session failure recovery) is mandatory, and the session runs at the lower of the two offered levels [14-C13].
- **Data-In digest errors.** On a digest error in a Data-In PDU, the initiator discards the PDU and either requests it again with SNACK (which needs ERL ≥1) or aborts the task. In one branch, the initiator signals CHECK CONDITION "Protocol Service CRC error" internally [14-C14].
- **Digest scope.** Digests default to None. When enabled, they check the whole path, including routers, switches and proxies. CRC32C is the only algorithm implementations must support [14-C15].
- **iSER.** iSER forbids iSCSI digests and SNACK and delegates integrity to the RDMA transport. Its stated reason, that no digest or sequence errors occur, applies to the iSCSI layer only [14-C16].

**Empirical evidence.**

- **Interconnect failures (Jiang et al. 2008).** Physical interconnect failures, a category that includes shelf enclosures, made up 27–68% of storage-subsystem failures. Redundant interconnects lowered the subsystem annual failure rate by 30–40% [14-C17]. These are NetApp FC back-end data, not host-to-array paths.
- **TCP checksums.** The TCP checksum estimate applies to block protocols over TCP that run without digests [14-C18; same source as 07-C18].

**Implementations.**

- **Linux NVMe host driver.** The driver fails a request without retry when DNR is set or the retry count runs out (default 5). It fails path errors over to another path. Under several conditions, it requeues I/O while a path is still resetting or connecting [14-C19].
- **Ceph librados.** A librados read returns a byte count. That this allows short results is an inference; the documentation does not describe short reads. The read comes from the snapshot selected on the I/O context [14-C20].

### B.15 Taxonomies of data-access layers: verdicts

| Candidate | C1 Defined | C2 Principled | C3 Foundational | C4 Maintained | Verdict |
|---|---|---|---|---|---|
| **Apache OpenDAL** | met [15-C1–C3] | met [15-C4, 15-C6] | met, with qualifications [15-C5, 15-C7–C9] | met (RFCs 0044, 0247, 0977, 8145 on errors; 0409, 0627, 2852, 6707, 7700 on capabilities) | **CONFIRMED**, with verifier qualifications (below) |
| **Hadoop FileSystem specification** | partial: read semantics are formally defined, but outcome classes are JDK/Hadoop exceptions named per precondition [15-C10–C12] | partial: rules exist, no retry axis [15-C13] | partial: contract tests enforce the model, but translation of native errors is connector code [15-C14] | partial: a "live document" that calls itself incomplete [15-C15] | **PARTIAL** |
| **Arrow `object_store`** | partial: one-line semantics per variant; a separate transport `HttpErrorKind` with per-variant retry rules [15-C16, 15-C18] | failed: no axis stated; a Generic fallback [15-C16] | partial: mapping visible in code, no documented backend mapping rules [15-C17] | failed: only a CHANGELOG | **PARTIAL** |
| **fsspec** | failed: Python built-in exceptions by convention [15-C20, contested and corrected] | failed | failed at the layer level: retry statuses are local to the HTTP implementation [15-C21] | failed | **NOT FOUND** |
| Go CDK `gcerrors` | screened only: drivers must implement `ErrorCode` [15-C22] | not assessed | not assessed | not assessed | no verdict (strong lead) |
| rclone `fserrors` | screened only: optional retry-hint interfaces [15-C23] | — | — | — | no verdict |
| jclouds, libcloud, Alluxio, JuiceFS, cloud-SDK retry classifiers | not read | | | | coverage gap |

**The OpenDAL taxonomy, as documented.** It has two independent axes, stated in RFC-8145 as "Error kind and retry status remain independent" [15-C4].

1. **`ErrorKind`, why an operation failed.** There are 13 kinds: Unexpected, Unsupported, ConfigInvalid, NotFound, PermissionDenied, IsADirectory, NotADirectory, AlreadyExists, RateLimited, IsSameFile, ConditionNotMatch, RangeNotSatisfied and Conflict (track 15 notes). Each has a written definition. For example, Conflict is a resource-state conflict that "does not indicate whether retrying the same operation is safe" [15-C1].
2. **`ErrorStatus`, retryability.**
   - Permanent: "Users MUST never retry". This is the default for a new error [15-C2].
   - Temporary: `set_temporary()` means the receiving layer "can safely replay the same operation method with its retained state", not that a broader workflow will succeed [15-C6].
   - Persistent: "temporary but persisted after retries", a SHOULD NOT retry [15-C3].

   `ErrorStatus` is a private enum; callers reach it through methods [15-C2].

A third, separate model is the **`Capability`** set together with a conditional-operations specification, which says what a backend supports (track 15 notes).

On mapping:

- **The contributor guide** says "an implementation must" return structured errors with the correct `ErrorKind` [15-C7]. Nothing in the code enforces this, and the guide does not define "correct" per backend.
- **RFC-8145** describes classification by native error code and operation context before any fallback to HTTP status. It states this descriptively, not with MUST [15-C5].
- **In the S3 service code**, the native code `NoSuchBucket` (HTTP 404) maps to ConfigInvalid rather than NotFound [15-C8].
- **Unrecognised or unclassified `std::io` errors,** including UnexpectedEof, Interrupted, TimedOut and WouldBlock, map to Unexpected with status Temporary [15-C9].

**Limits stated in the sources or found by the verifiers.**

- **No class for stream failures.** No kind exists for truncation or a mid-stream failure, so these collapse into Unexpected (track 15 gap; 15-C9).
- **Partial exclusivity.** Exclusivity rules are stated only among the condition, conflict and existence kinds.
- **Recency.** RFC-8145 (Conflict) began on 2026-08-25, and its tracking issue was still a placeholder. The verifiers caution against presenting Conflict as long-standing [15-C1].
- **Stream semantics unread.** OpenDAL's Reader semantics (short reads, retry after partial I/O) were not read (coverage gap).

---

## C. Existing models and classifications (additions)

| Model / classification | Provenance | Purpose and scope | Key assumptions | What it explains about reads | Strengths / limits | Relations |
|---|---|---|---|---|---|---|
| FTP reply-code classes 1yz–5yz | RFC 959 §4.2.1 | Outcomes of control-channel commands | Server and client agree on "transient" | Transient vs permanent negative completion after a retrieval (426, 451, 550) | Formal split; the RFC admits "transient" is hard to define | HTTP status classes (inference); OpenDAL ErrorStatus |
| FTP TYPE × STRU × MODE matrix | RFC 959 §3; RFC 3659 §4–5 | Data representation and transfer | Mostly IMAGE/File/Stream in practice (inference) | How EOF is signalled, byte transformation, restart semantics, meaning of SIZE | Comprehensive; most combinations rarely implemented | Close-delimited framing (07-C4) |
| FTPS PROT levels C/S/E/P | RFC 2228 via RFC 4217 §9 | Data-connection protection | TLS | Whether the read bytes have integrity protection | No truncation semantics | TLS close_notify (02-C18) |
| SFTP status codes, v3 vs v6 | draft-ietf-secsh-filexfer-02 §7; -13 §9.1 | SFTP replies | Expired drafts; OpenSSH implements v3 only | EOF, generic failure, client-local connection loss | No ratified standard; no transient/permanent grouping | NFS/SMB status (B.7) |
| URE/UWE classes of undetected disk errors | RIVA, building on Bairavasundaram and Krioukov | Why post-transfer checksums miss errors | Linux page cache | Cache-served verification hides read and write errors | Fault injection covered UWE only | End-to-end argument (05-C17); ZFS cache (05-C9) |
| NBD simple vs structured replies; ERROR vs ERROR_OFFSET | NBD proto.md | Remote block reads | Project-level specification | All-or-nothing vs chunked, reorderable reads with localised errors | Precise; no integrity check, no reconnect semantics | Go n>0 with error (02-C6), analogue (inference) |
| NVMe/TCP fatal vs non-fatal transport errors | NVMe/TCP spec §3.5 | Transport error handling | Optional digests | Connection loss vs failing a single command, even after the controller reported success | Binary rule; no per-PDU retransmission | 03-C1 (status separate from data) |
| NVMe retry categories after communication loss | NVMe Base §9.6.3 | Host recovery | Idempotence and effects bits | Whether a read may be replayed at once | Conditional categorisation | HTTP idempotent GET (07-C6) |
| NVMe ANA states | NVMe Base §8.1 | Multipath access | Path selection out of scope | Switch path, wait, or stop | — | dm-multipath (unread) |
| iSCSI ErrorRecoveryLevel 0/1/2 | RFC 7143 §7.1.5 | Recovery after digest, connection or session faults | Negotiated, lower level wins | Retransmission of read PDUs vs task abort vs session restart | Only ERL 0 is mandatory | NVMe/TCP model (divergent) |
| Storage-subsystem failure types (disk, interconnect, protocol, performance) | Jiang et al. FAST 2008 | Field classification | NetApp FC back end | Missing disks, wrong answers, untimely service | Large dataset; one vendor | Fail-slow (08-C14); gray failure |
| OpenDAL `ErrorKind` × `ErrorStatus` (+ `Capability`) | apache/opendal error.rs, capability.rs, RFCs, internal docs | Unified access errors across many backends | Backends map honestly; mapping not enforced by code | Why an access failed vs whether it may be replayed | Two stated axes, RFC-maintained; no truncation kind; recent changes | Avižienis viewpoints; OpenDAL's Persistent is defined by exhausted retries, a basis not found in the earlier report's sources *(inference)* |
| Hadoop FileSystem specification read model | hadoop-common filesystem/*.md; contract tests; S3A connector | Formal pre- and postconditions for filesystem APIs | Exception classes as outcomes | Short reads (1..n bytes), −1 at EOF, undefined buffer after a failed positioned read | Formal and tested; no retry axis; self-declared incomplete | POSIX read (01-C1), NVMe undefined buffer (03-C1) |
| Arrow `object_store` Error + `HttpErrorKind` | arrow-rs-object-store source | Stateless object API, deliberately not a cursor-based file interface [15-C19] | Generic fallback | Outcome variants; transport-level retry rules | No stated axis or design record; maps HTTP 409 to AlreadyExists (OpenDAL has a separate Conflict kind) | RFC 9110 validators (07-C3) |

---

## D. Cross-source synthesis with the earlier report

### D.1 Where the new evidence supports the earlier principles

- **Completion status and data correctness are separate** (earlier D.1-1):
  - An NVMe/TCP host must fail a read the controller reported as successful if the data digest fails [14-C8].
  - An NBD `ERROR` chunk invalidates data already sent [14-C3].
  - FTP block mode delivers data flagged "suspected errors" [13-C2].
  - A TFTP sender that times out after the final ACK does not know the outcome [13-C16].
- **Detection depends on where the check sits** (earlier D.1-2):
  - FTP leaves integrity to TCP [13-C3], and TCP misses errors [14-C18 / 07-C18].
  - iSCSI digests check the whole path only when enabled [14-C15], and iSER moves the check to the RDMA transport [14-C16].
  - Post-transfer checksums served from the page cache miss disk errors [13-C23].
  - In the field, about one checksum failure per 1.26 TB was found only by application-level checks [13-C22].
- **End of data is defined by framing** (earlier D.1-3):
  - FTP stream mode signals EOF by closing the connection, the same ambiguity as close-delimited HTTP (07-C4) [13-C1].
  - TFTP uses the short block and an extra zero-length block [13-C16, 13-C17], and SFTP uses an EOF status [13-C11].
  - FTPS adds a normative gap here: RFC 4217 gives no rule for detecting truncation [13-C8].
- **Partial results are usually successes** (earlier D.1-4):
  - SFTP v6, the OpenSSH server and 9P all return short successful reads [13-C12, 13-C13, 13-C19].
  - NBD READ has no short success and fails instead [14-C5], so it sits with SMB2 (07-C10).
  - The SFTP v3 draft's "guaranteed" full read is contradicted by OpenSSH's practice [13-C9, 13-C13].
- **Masking turns errors into latency** (earlier D.1-5). Linux NVMe multipath requeues I/O while paths reconnect [14-C19], and the NVMe CRD field imposes retry delays [14-C10].
- **Mid-stream version change is guarded only locally** (earlier D.1-7). FTP has only a heuristic MDTM check before resuming [13-C7], and 9P has `qid.version`. rsync reports source files that vanished [13-C21]. Globus cannot tell change during transfer from corruption [13-C22].

### D.2 New distinctions the earlier report did not have

1. **Ordering of read data is a protocol design choice, made differently.**
   - NVMe/TCP requires data within a command to arrive in order; a gap is fatal [14-C7].
   - NBD structured replies may arrive in any order and the client reassembles them [14-C2].
   - Replies *between* requests may be reordered in SFTP, NBD and 9P [13-C10, 14-C4, 13-C19].
   - iSCSI makes ordering negotiable (track 14 notes).
2. **What happens to a corrupted read differs.**
   - NVMe/TCP fails the whole command as transient, with no retransmission of the PDU [14-C8].
   - iSCSI at ERL ≥1 retransmits the PDU via SNACK [14-C14].
   - iSER forbids both digests and SNACK [14-C16].
   - NBD has no digest *(inference from absence)*.
3. **Retry semantics are formally specified in places.**
   - NVMe defines Unrestricted, Delayed and State-Dependent retry categories after loss of communication [14-C12].
   - It also defines a recommended limit before a transient error counts as persistent [14-C9], a subsystem-wide do-not-retry bit [14-C10], and path-dependent retry [14-C11].
   - The FTP 4yz/5yz split is an older, explicitly fuzzy version of the same distinction [13-C4].
4. **The bytes received may legitimately differ from the bytes stored.**
   - FTP TYPE ASCII transforms data, and SIZE reports the *transmitted* octet count [13-C5].
   - The earlier report's closest finding is ISO C trailing nulls (02-C3).
5. **Whether partial success can be localised is a protocol choice.** NBD's `ERROR_OFFSET` lets valid chunks stand beside a localised error [14-C3], a block-level parallel to Go's n>0 with error (02-C6). NBD simple replies and NVMe/TCP do not allow this [14-C1, 14-C8].
6. **Persistence as a status reached by exhausting retries.** NVMe treats a transient error as persistent after four or more failures [14-C9], and OpenDAL's `Persistent` status means temporary but persisting after retries [15-C3]. The earlier report's transient vs sticky distinctions (05-C1, 08-C6, 08-C9) are based on the fault, not on retry history *(inference)*.

### D.3 Access-layer taxonomies compared with the classifications in the earlier report

These are relationships the sources support. They are not a merged scheme.

- **Two independent axes.** OpenDAL states that *kind* and *retry status* are independent [15-C4]. Most classifications in the earlier report combine the two:
  - SCSI sense keys mix kind and recoverability (03-C8).
  - NVMe keeps them separate in its own way: status code plus DNR and CRD [14-C10].
  - FTP folds retryability into the reply-code digit [13-C4].
- **Mapping is lossy at abstraction boundaries.** Two examples:
  - OpenDAL maps Rust `UnexpectedEof` and `Interrupted` to Unexpected/Temporary [15-C9]. The earlier report's distinctions between end of stream and unexpected end (02-C9, 02-C10) are lost at this boundary.
  - S3's NoSuchBucket becomes ConfigInvalid [15-C8].

  This matches the earlier observation that the same fault surfaces differently by layer (earlier D.1-9).
- **Divergent mappings of the same HTTP status.** HTTP 409 maps to AlreadyExists in Arrow `object_store` [15-C17]. OpenDAL has a separate Conflict kind and RFC-8145 initial mappings (track 15 notes). Both relate to RFC 9110 conditional requests (07-C3).
- **A formal read contract without an outcome taxonomy.** The Hadoop specification is closest to POSIX in kind: pre- and postconditions with short reads and −1 at EOF [15-C10], and an undefined buffer after a failed positioned read [15-C11], which parallels 03-C1. It deliberately leaves retry classification to connectors [15-C13, 15-C14].
- **No truncation class.** None of the access layers examined defines an outcome class for truncated or mid-stream read failure (track 15 gap). This matches the earlier report's genuine gap F.1-3.

---

## E. Evidence and provenance matrix

The columns and codes are the same as in the earlier report's §E. The *Finding* column shows the claim as extracted; the narrative above uses the corrected reading. The full per-lens record is in `research_notes/Binary Stream Read Behavior Foundations - transfer protocols/16-verification.md`.

| ID | Finding (as extracted) | Source and locator | Type | Verification | Applicability | Qualifications from verification |
|---|---|---|---|---|---|---|
| **13** | **File-transfer and remote file-access protocols** | | | | | |
| 13-C1 | In FTP stream mode with file structure, end of file is signalled only by the sender closing the data connection, and every byte is data; there is no in-band EOF marker. | RFC 959, File Transfer Protocol (Postel & Reynolds, 1985), §3.4.1 Stream Mode; §3.4. <https://www.rfc-editor.org/rfc/rfc959.txt> | N | VERIFIED (3S/0R/0U) | FTP STREAM mode, STRU F (the usual binary retrieval case). Record structure in stream mode instead uses escaped EOR/EOF control codes. |  |
| 13-C2 | FTP block mode defines a descriptor flag that marks a block as 'suspected errors', so data can be delivered while flagged as unreliable. It sits alongside the EOF, EOR and restart-marker flags. | RFC 959, §3.4.2 Block Mode, descriptor codes table. <https://www.rfc-editor.org/rfc/rfc959.txt> | N | VERIFIED (3S/0R/0U) | FTP MODE B only. The RFC states it is 'NOT intended for error control within FTP' but for sites that want all data despite local errors (e.g., tape read errors). |  |
| 13-C3 | FTP has no mechanism of its own to detect lost or corrupted bits; it delegates this to TCP. Its restart procedure is defined only for block and compressed modes. | RFC 959, §3.5 Error Recovery and Restart. <https://www.rfc-editor.org/rfc/rfc959.txt> | N | VERIFIED (3S/0R/0U) | All FTP transfers without extensions. RFC 1123 §4.1.3.4 corrects the 110 restart reply format. | [overreach] Restart being 'defined only for the block and compressed modes' holds for base RFC 959 only. RFC 3659 later adds STREAM-mode restart via REST plus an octet offset. The claim should be dated to RFC 959. |
| 13-C4 | FTP reply codes formally separate transient negative completions (4yz, the request may be repeated unchanged) from permanent ones (5yz, repeating it is discouraged). The RFC itself concedes that 'transient' is hard to define. | RFC 959, §4.2.1, 4yz and 5yz definitions. <https://www.rfc-editor.org/rfc/rfc959.txt> | N | VERIFIED (3S/0R/0U) | FTP control-channel replies to RETR, e.g., 426 'Connection closed; transfer aborted.' and 451 'local error in processing'. |  |
| 13-C5 | The FTP SIZE command must return the exact number of octets that would be transmitted, and that number depends on the current TYPE, MODE and STRU. It is not necessarily the stored file size. | RFC 3659, Extensions to FTP (Hethmon, 2007), §4 File SIZE. <https://www.rfc-editor.org/rfc/rfc3659.txt> | N | VERIFIED (3S/0R/0U) | FTP servers implementing RFC 3659. With TYPE ASCII the value includes CRLF conversion (§5.2). |  |
| 13-C6 | RFC 3659 defines restart in STREAM mode as an octet offset. Such an offset is an unambiguous restart point only in STREAM mode, because in other modes the same file can be sent as different octet sequences. | RFC 3659, §5.1 Restarting in STREAM Mode. <https://www.rfc-editor.org/rfc/rfc3659.txt> | N | VERIFIED (3S/0R/0U) | REST followed by RETR in STREAM mode. For RETR, the client 'bears the responsibility of merging the retrieved data'. |  |
| 13-C7 | FTP offers no in-transfer detection of source changes. Before resuming a retrieval, RFC 3659 only recommends a heuristic comparison of modification times (MDTM or the MLST 'modify' fact). | RFC 3659, §3 File Modification Time (MDTM). <https://www.rfc-editor.org/rfc/rfc3659.txt> | N | VERIFIED (3S/0R/0U) | Resume of RETR or STOR. Because clocks are not synchronised, clients should record MDTM before the initial RETR. | [overreach] RFC 3659 says the user-FTP 'can use' MDTM or the 'modify' fact, and that clients 'should usually' record the time before the initial RETR. That is permissive wording, not a formal recommendation. The heuristic covers STOR too (comparing against the partial file's MDTM). 'No in-transfer detection' is an inference, not something the RFC states. |
| 13-C8 | With FTPS protection level Clear (PROT C), the data connection has no integrity protection at all. RFC 4217 contains no normative text on detecting truncation of a protected data connection; it only illustrates TLSshutdown before close. | RFC 4217, Securing FTP with TLS (2005), §9 Data Connection Security; §12.6-12.7 diagrams. <https://www.rfc-editor.org/rfc/rfc4217.txt> | N | VERIFIED (3S/0R/0U) | FTPS (explicit AUTH TLS). Whether a TCP close without TLS closure is treated as truncation is left to TLS and implementations. |  |
| 13-C9 | In SFTP version 3, a READ returns as many bytes as the server can read up to len. EOF or an error before any data yields SSH_FXP_STATUS. Full reads are 'guaranteed' only for normal disk files; device files may return fewer bytes. | draft-ietf-secsh-filexfer-02 (SFTP v3), expired Internet-Draft, §6.4 Reading and Writing. <https://www.ietf.org/archive/id/draft-ietf-secsh-filexfer-02.txt> | N | VERIFIED (3S/0R/0U) | SFTP protocol version 3, the version OpenSSH implements. This is an expired draft, not a ratified standard. |  |
| 13-C10 | SFTP places no restriction on the order in which responses to outstanding requests are delivered; replies are matched by request id. Overlapping read/write requests on the same file must behave as if they were serialized. | draft-ietf-secsh-filexfer-02, §6.1 Request Synchronization and Reordering. <https://www.ietf.org/archive/id/draft-ietf-secsh-filexfer-02.txt> | N | VERIFIED (3S/0R/0U) | Pipelined SFTP v3 reads (expired draft). The same rule appears in -13 §4.1. |  |
| 13-C11 | In SFTP v3, SSH_FX_CONNECTION_LOST and SSH_FX_NO_CONNECTION are client-local pseudo-errors that servers must not send. SSH_FX_EOF signals that no more data is available, and SSH_FX_FAILURE is a generic catch-all. No transient/permanent class distinction exists. | draft-ietf-secsh-filexfer-02, §7 Responses from the Server to the Client, status codes. <https://www.ietf.org/archive/id/draft-ietf-secsh-filexfer-02.txt> | N | VERIFIED (3S/0R/0U) | SFTP v3 (expired draft). Version 6 (-13) expands the codes to 0-31, including lock conflicts. |  |
| 13-C12 | SFTP version 6 explicitly allows short READ replies (at EOF, on error, or when server buffers are limited). It adds an optional end-of-file flag so clients need not spend a round trip telling EOF apart from other short-read causes. This is a version difference from v3. | draft-ietf-secsh-filexfer-13 (SFTP v6), expired Internet-Draft, §8.2.1 Reading Files; §9.3 Data Response. <https://www.ietf.org/archive/id/draft-ietf-secsh-filexfer-13.txt> | N | VERIFIED (3S/0R/0U) | SFTP v6 servers. Not implemented by OpenSSH (v3 only). With a non-zero max-read-size and length <= max-read-size, a short reply means EOF or error. | [overreach] v3 already let reads return fewer bytes for files that are not normal disk files, such as device files. The version difference is that v6 allows short replies more broadly (EOF, error, limited server buffers), adds the optional end-of-file flag and adds the max-read-size guarantee. Short reads themselves are not new. |
| 13-C13 | OpenSSH implements only SFTP v3 (draft -02) plus extensions. Its documentation states that servers usually answer reads larger than max-read-length with shorter DATA packets, and may sever the connection if limits are exceeded. | OpenSSH PROTOCOL file (openssh-portable), Header; §4.8 limits@openssh.com. <https://raw.githubusercontent.com/openssh/openssh-portable/master/PROTOCOL> | I | VERIFIED (3S/0R/0U) | OpenSSH sftp-server and compatible clients. sftp-server.c caps len at SFTP_MAX_READ_LENGTH and returns the result of a single read(2), giving SSH2_FX_EOF on 0. |  |
| 13-C14 | The OpenSSH sftp client re-requests the remainder after a short DATA reply, treats any non-EOF status as a read error, and truncates the local file to the highest contiguous offset on interrupt or error. It refuses to resume a download if the server reordered replies. | OpenSSH sftp-client.c (sftp_download), sftp_download receive loop and post-loop truncation. <https://raw.githubusercontent.com/openssh/openssh-portable/master/sftp-client.c> | G | CONTESTED (2S/1R/0U) | OpenSSH sftp/scp-over-SFTP downloads (current master). The client also fatals on 'Received more data than asked for' and on a second zero-length DATA reply. | [overreach] The re-request, non-EOF-is-error, contiguous truncation, 'more data than asked' fatal and second zero-length fatal behaviours are all correct. But the client does not refuse to resume. When a transfer with resume_flag set fails or is interrupted after replies arrived out of order, it only logs 'Unable to resume download ... server reordered requests' and still truncates to highwater. No code path blocks a later resume. Truncation also happens unconditionally with the in-place flag. [fidelity] The client does not actively refuse a resume. When resume_flag is set, an error or interrupt occurred, and reordering was seen, it only logs error("Unable to resume download ... server reordered requests"). It still truncates at highwater, and does so unconditionally with inplace_flag. |
| 13-C15 | The legacy scp protocol let a hostile server send filenames that did not match the client's request (CVE-2019-6111). OpenSSH describes the protocol as outdated and not readily fixable; the client-side mitigation can falsely reject files because client and server wildcard expansion may differ. | OpenSSH 8.0 release notes, Security section; Potentially-incompatible changes (scp -T). <https://www.openssh.com/txt/release-8.0> | I | VERIFIED (3S/0R/0U) | scp/rcp protocol (no formal specification). OpenSSH 9.0 switched scp to SFTP by default, keeping legacy via -O; 8.3 notes a desynchronisation in which 'file contents [could] be interpreted as file metadata'. |  |
| 13-C16 | TFTP signals end of transfer by a DATA packet shorter than the block size. A sender that times out after the final DATA packet cannot tell whether the transfer succeeded. | RFC 1350, TFTP Revision 2 (1992), §2 Overview; §6 Normal Termination. <https://www.rfc-editor.org/rfc/rfc1350.txt> | N | VERIFIED (3S/0R/0U) | TFTP lock-step transfers. ERROR packets are not retransmitted, so timeouts must be used to detect errors (§7). | [overreach] RFC 1350 fixes the block size at 512, so its rule is 'a data packet of less than 512 bytes'. The no-retransmission point for ERROR is in both §2 and §7. |
| 13-C17 | With the TFTP blksize option, a file whose size is an exact multiple of the block size ends with an extra zero-length DATA packet. The final-packet rule is unchanged: data shorter than the negotiated blocksize ends the transfer. | RFC 2348, TFTP Blocksize Option, Blocksize Option Specification, final-packet paragraph. <https://www.rfc-editor.org/rfc/rfc2348.txt> | N | VERIFIED (3S/0R/0U) | TFTP with RFC 2347/2348 option negotiation; blksize 8..65464 octets. RFC 7440 windowsize keeps windowsize=1 equivalent to RFC 1350. |  |
| 13-C18 | The TFTP 'Sorcerer's Apprentice Syndrome' (retransmitting on duplicate ACKs) does not corrupt the file but can cause excessive duplication and time-outs. RFC 1123 requires the fix. | RFC 1123, Requirements for Internet Hosts (1989), §4.2.3.1 Sorcerer's Apprentice Syndrome. <https://www.rfc-editor.org/rfc/rfc1123.txt> | N | VERIFIED (3S/0R/0U) | TFTP implementations. Fix (MUST): the sender must never resend the current DATA packet on receipt of a duplicate ACK. | [overreach] RFC 1123 says the bug 'may cause' excessive retransmission, which 'may cause' a timeout. It is a possibility, not a certainty. |
| 13-C19 | A 9P Rread may return fewer bytes than requested. A read at or beyond the file size returns a count of zero. Atomic transfer size is bounded only by the iounit reported at open. | Plan 9 manual, read(5) (9P2000), read(5) DESCRIPTION. <https://9p.io/magic/man2html/5/read> | I | VERIFIED (3S/0R/0U) | 9P2000 (Plan 9). intro(5) adds: replies are matched by tag, failures are Rerror strings, Tversion aborts outstanding I/O, and qid.version is 'typically' incremented on modification. | [overreach] read(5) does not say atomic transfer is 'bounded only by' iounit. It says iounit, if non-zero, reports the maximum size that is guaranteed to be transferred atomically. That is a guarantee, and when iounit is 0 none is given here. Message size limits can also split one read call into several messages. Directory reads follow different rules: whole entries only, sequential offsets. [fidelity] The source says iounit, 'if non-zero, reports the maximum size that is guaranteed to be transferred atomically'. That is a guarantee of atomicity up to iounit, not 'bounded only by' it, and iounit may be zero. I did not check the intro(5) items in the applicability note. |
| 13-C20 | In BitTorrent, each fixed-size piece (the last may be shorter) is verified against a SHA1 hash from the metainfo. A peer announces a piece with 'have' only after it has checked the hash. | BEP 3, The BitTorrent Protocol Specification (Status: Final), Metainfo 'pieces'; peer messages 'have'. <https://www.bittorrent.org/beps/bep_0003.html> | N | VERIFIED (3S/0R/0U) | BitTorrent v1 (BEP process standard, not IETF). The 16 KiB request size is stated as the practice of 'All current implementations', which is a convention. |  |
| 13-C21 | rsync normally verifies each transferred file with a whole-file checksum computed during transfer, unless checksum-choice=none is forced. However, --append does not verify existing receiver content, and before rsync 3.0.0 --append behaved like --append-verify (a version difference). | rsync(1) manual page, --checksum; --append; --append-verify. <https://download.samba.org/pub/rsync/rsync.1> | I | VERIFIED (3S/0R/0U) | rsync 3.x. Exit codes 23 (partial transfer due to error), 24 (vanished source files) and 30 (timeout). By default partial files are deleted on interrupt. |  |
| 13-C22 | In four years of Globus logs, 27,251 of 3,312,102 transfers with integrity checking had at least one checksum error (about 1 in 121), and at least one checksum failure occurred per 1.26 TB. Changes to files during transfer cannot be distinguished from corruption. | Liu, Kettimuthu, Foster, Rao, Cross-geography Scientific Data Transferring Trends and Behavior, HPDC 2018, §4.1 Checksum, encryption, and reliability; Observation 6. <https://lzhengchun.github.io/file/hpdc2018.pdf> | E | VERIFIED (3S/0R/0U) | GridFTP/Globus wide-area science transfers 2014-2017, with application-level 32-bit checksums computed by rereading the files at both ends. |  |
| 13-C23 | End-to-end file-transfer checksum verification that rereads files usually hits the page cache. It therefore fails to detect injected undetected disk read and write errors for files smaller than memory; RIVA fixes this by invalidating cached pages. | Charyyev & Arslan, RIVA: Robust Integrity Verification Algorithm for High-Speed File Transfers (NSF PAR manuscript), Abstract; §2.2-2.3 motivating experiment (273 files, 274 GB). <https://par.nsf.gov/servlets/purl/10130450> | E | VERIFIED (3S/0R/0U) | Linux file transfers with post-transfer checksumming (sequential, block-level, FIVER), with fault injection. | [overreach] The injected faults are only undetected write errors (UWEs, in the 'extreme-injection' test). Read-error (URE) cases are argued analytically, not injected. The 273-file / 274 GB experiment measured page misses (cache behaviour), not detection. The abstract says existing methods miss injected errors 'for almost all file sizes', and the paper concedes RIVA may fail if several I/O operations are corrupted. RIVA invalidates pages with munmap, checking with mincore. [fidelity] The injected faults are undetected write errors (UWEs) only. The abstract says 'robustness ... against undetected disk write errors', and §5.2.2 / Fig. 10 inject UWEs. Read errors were not injected. Also, the §2.3 motivating experiment monitors page misses and does not inject faults; the fault injection is in §5.2.2. |
| **14** | **Remote and networked block-storage protocols** | | | | | |
| 14-C1 | Under NBD simple replies, a read cannot report partial success. If an error is detected after a zero-error reply header has been sent, the server must hard-disconnect and send no more data. | NBD protocol, doc/proto.md (NetworkBlockDevice/nbd master), Transmission > NBD_CMD_READ (0), 'Simple replies'; also 'Structured reply chunk message' intro. <https://raw.githubusercontent.com/NetworkBlockDevice/nbd/master/doc/proto.md> | I | VERIFIED (3S/0R/0U) | NBD sessions without NBD_OPT_STRUCTURED_REPLY. The spec is de facto: a project document of the Linux kernel and reference implementation behaviour, using RFC 2119 keywords, not ratified by any standards body. | [overreach] Minor: if the error is known before the header is sent, the server SHOULD set the error code and MAY disconnect; if it does not disconnect it MUST NOT send any payload. Only an error found after a zero-error header forces an immediate hard disconnect. [currency] The applicability note mislabels the document. proto.md belongs to the NetworkBlockDevice/nbd project; it is not 'a project document of the Linux kernel'. Also, the simple-reply rule applies only when neither structured replies nor the newer experimental NBD_OPT_EXTENDED_HEADERS have been negotiated. |
| 14-C2 | With NBD structured replies, read content chunks may arrive in any order and must be reassembled by the client. Further content chunks may follow an error chunk. When no error occurs, the server must cover the whole requested range. | NBD protocol, doc/proto.md, NBD_CMD_READ (0), 'Structured replies'. <https://raw.githubusercontent.com/NetworkBlockDevice/nbd/master/doc/proto.md> | I | VERIFIED (3S/0R/0U) | NBD after NBD_OPT_STRUCTURED_REPLY negotiation (de facto spec). | [overreach] Two conditions are left out. If the client sets NBD_CMD_FLAG_DF, the server MUST send at most one content chunk, so there is no reordering. Chunks also MUST NOT overlap earlier content or error chunks, and MUST NOT fall outside the requested range. Sending content chunks after an error chunk is a MAY, not something to expect. |
| 14-C3 | NBD distinguishes two read-error semantics. NBD_REPLY_TYPE_ERROR invalidates all data chunks of the reply, whether sent before or after it. NBD_REPLY_TYPE_ERROR_OFFSET localises the error, so partial success can be determined. | NBD protocol, doc/proto.md, NBD_CMD_READ structured replies; Structured reply types NBD_REPLY_TYPE_ERROR / _ERROR_OFFSET. <https://raw.githubusercontent.com/NetworkBlockDevice/nbd/master/doc/proto.md> | I | VERIFIED (3S/0R/0U) | NBD structured replies (de facto spec). | [overreach] Partial success can be worked out only conditionally. The text reads 'As long as all errors are accompanied by offsets, the client MAY assume' that data chunks with no later error offset are valid, and that uncovered portions are invalid. The server SHOULD NOT mix offset errors with a generic error. Also, any error chunk makes the reply unsuccessful overall. [fidelity] The quote is in the NBD_CMD_READ section, not the 'Structured reply types' definitions, though NBD_REPLY_TYPE_ERROR's own definition (around line 1901) also says 'the client MAY NOT make any assumptions about partial success'. Partial success can be determined only when every error carries an offset; the spec says a server SHOULD NOT mix the two error types. |
| 14-C4 | NBD replies may be returned out of request order, and chunks of different requests may be interleaved. Correlation is by a client-chosen opaque cookie. | NBD protocol, doc/proto.md, Protocol phases > Transmission. <https://raw.githubusercontent.com/NetworkBlockDevice/nbd/master/doc/proto.md> | I | VERIFIED (3S/0R/0U) | NBD transmission phase (de facto spec). | [overreach] The spec adds that 'there may be constraints that prevent arbitrary reordering of structured reply chunks within a given reply'. Clients SHOULD (not MUST) use distinct cookies for pending requests. |
| 14-C5 | NBD has no end-of-file or short-read outcome for READ. A read extending beyond the export size SHOULD fail with NBD_EINVAL. The error values are a small errno-derived set without a transient/permanent classification. | NBD protocol, doc/proto.md, Values > Transmission phase > Error values. <https://raw.githubusercontent.com/NetworkBlockDevice/nbd/master/doc/proto.md> | I | VERIFIED (3S/0R/0U) | NBD servers (SHOULD-level, de facto spec). | [overreach] 'No EOF/short-read outcome' is an inference from the spec saying nothing on it; label it as inference. The spec does attach handling hints to some codes: for NBD_EOVERFLOW 'a client should be prepared to retry with smaller requests', and on NBD_ESHUTDOWN the client MUST initiate a disconnect. That is retry guidance, even though there is no formal classification. [fidelity] The quote continues '...or if a read or write request is not aligned to advertised minimum block sizes', so EINVAL also covers misalignment. |
| 14-C6 | An NBD BLOCK_STATUS reply may legitimately cover less of the requested range than asked, as long as at least one extent is returned. | NBD protocol, doc/proto.md, Structured reply types > NBD_REPLY_TYPE_BLOCK_STATUS (5). <https://raw.githubusercontent.com/NetworkBlockDevice/nbd/master/doc/proto.md> | I | VERIFIED (3S/0R/0U) | NBD metadata (block status) queries, not data reads. | [overreach] The claim leaves out the stated condition: the MAY applies 'if looking up the information would be too resource-intensive for the server'. Servers SHOULD NOT send more than 2^20 extents per chunk 'even if this requires that the server truncate the response'. NBD_CMD_FLAG_REQ_ONE also limits the reply to one extent. |
| 14-C7 | In NVMe/TCP, the C2HData PDUs carrying read data must have strictly sequential offsets from 0 within a command. A non-contiguous PDU is a fatal transport error. PDUs of different commands may interleave. | NVM Express TCP Transport Specification, Revision 1.1 (2024-08-05), §3.3.2.1 Controller to Host Command Data Buffer Transfers. <https://nvmexpress.org/wp-content/uploads/NVM-Express-TCP-Transport-Specification-Revision-1.1-2024.08.05-Ratified.pdf> | N | VERIFIED (3S/0R/0U) | NVMe/TCP transport binding. | [currency] Rev 1.1 is superseded. Rev 1.2 (Aug 2025) and Rev 1.3 (2026-07-31, retitled 'NVMe over TCP Transport Specification') followed; Rev 1.3 keeps the same §3.3.2.1 text. |
| 14-C8 | In NVMe/TCP, a header digest error is always fatal and terminates the connection. A data digest error in read data is non-fatal, but the host must fail the command even if the controller returned success. | NVM Express TCP Transport Specification, Revision 1.1, §3.5 Error Handling Model, 'Digest Error handling'. <https://nvmexpress.org/wp-content/uploads/NVM-Express-TCP-Transport-Specification-Revision-1.1-2024.08.05-Ratified.pdf> | N | VERIFIED (3S/0R/0U) | NVMe/TCP connections where DDGST/HDGST were negotiated. Both digests are optional and use CRC32C (§3.3.1.1). | [overreach] 'Fail the command with a non-fatal transport error' means completing it with Transient Transport Error status (per §3.5). Termination is through a TermReq exchange, with a fallback 30-second timeout or a TCP reset. [currency] Current revision is NVMe over TCP Rev 1.3 (2026-07-31); the text is unchanged. |
| 14-C9 | NVMe defines Transient Transport Error as likely to succeed on retry on the same controller. After four or more such failures the command should be treated as a persistent transport error. | NVM Express Base Specification, Revision 2.1, Generic Command Status Values, status code 22h. <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf> | N | VERIFIED (3S/0R/0U) | All NVMe transports (status code semantics). | [overreach] The four-or-more rule is a 'should' recommendation, not a requirement. [currency] Base 2.1 is superseded: Base 2.2 (2025-03), 2.3 (2025-08) and 2.4 (2026-07-31) followed. The wording is unchanged in 2.4. |
| 14-C10 | In NVMe, the DNR bit marks a command as expected to fail on resubmission to any controller in the subsystem. The CRD field selects a minimum retry delay, which is advisory: retrying earlier is not an error. | NVM Express Base Specification, Revision 2.1, Figure 100: Completion Queue Entry: Status Field (bits 31, 29:28). <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf> | N | VERIFIED (3S/0R/0U) | NVMe completions. CRD applies only if the host enabled ACRE. | [overreach] CRD is meaningful only when DNR is cleared and the host set ACRE to 1h; otherwise the field is reserved. CRD 00b means zero delay. [currency] In Base 2.4 the Status Field figure is Figure 101, not Figure 100. Base 2.1 is superseded by 2.4 (2026-07-31), with the same text. |
| 14-C11 | NVMe Path Related Status errors should be retried on a different path if one is available. ANA Inaccessible and Persistent Loss mean the command should not be resubmitted to the same controller. ANA Transition means retry after the transition completes. | NVM Express Base Specification, Revision 2.1, Path Related Status Definition, Figure 107. <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf> | N | VERIFIED (3S/0R/0U) | Multipath NVMe hosts (any transport) with ANA. | [overreach] The retry-on-another-path rule is qualified by 'unless otherwise specified'. Internal Path Error (00h) instead defers to the DNR bit. All of these are 'should' recommendations. [fidelity] Figure 107's 00h Internal Path Error is an exception: its retry follows the DNR bit. |
| 14-C12 | After communication loss, NVMe classifies a Read as idempotent and an Unrestricted Retry command. Such a command may be retried immediately without determining whether the original is still being processed. Writes are Delayed Retry commands. | NVM Express Base Specification, Revision 2.1, §9.6.3.1 Idempotent Commands; §9.6.3.2.1 Unrestricted Retry Commands. <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf> | N | VERIFIED (3S/0R/0U) | NVMe hosts recovering from loss of a controller (Keep Alive Timeout, transport connection termination). | [overreach] This is a categorisation with conditions, not a fixed property of Read. A command counts as Unrestricted Retry only if it is idempotent, changes nothing beyond ancillary state, and has CCC/NIC/NCC/LBCC cleared in the Commands Supported and Effects log. Writes are Delayed Retry 'except as described in section 9.6.3.2.2': a write that can affect other hosts becomes State-Dependent Retry. Retry is a host 'may', and the procedures are 'strongly recommended', not mandated. [fidelity] A Read counts as Unrestricted Retry only if the CCC, NIC, NCC and LBCC effects bits are all cleared. The spec gives Read and Write as examples ('e.g.'), not an absolute classification, and Write is Delayed Retry 'except as described in section 9.6.3.2.2' (when it can affect other hosts). |
| 14-C13 | iSCSI error recovery is a negotiated three-level hierarchy (ERL 0 session recovery, 1 digest failure recovery, 2 connection recovery). Only level 0 is mandatory, and the session operates at the lower of the two offered values. | RFC 7143, iSCSI Protocol (Consolidated), §7.1.5 Error Recovery Hierarchy; §13.20. <https://www.rfc-editor.org/rfc/rfc7143.txt> | N | VERIFIED (3S/0R/0U) | iSCSI sessions. The default ErrorRecoveryLevel is 0. | [overreach] Level 1 'digest failure recovery' covers both within-connection and within-command recovery classes. Each level is a superset of the levels below it. [fidelity] The RFC labels level 0 'Session failure recovery' rather than 'session recovery'; this is minor. |
| 14-C14 | An iSCSI initiator receiving a Data-In PDU with a payload digest error must discard it and either request it through SNACK or abort the task. If the SNACK is rejected after status was sent, the command completes with CHECK CONDITION 'Protocol Service CRC error'. | RFC 7143, §7.8 Digest Errors. <https://www.rfc-editor.org/rfc/rfc7143.txt> | N | VERIFIED (3S/0R/0U) | iSCSI with DataDigest negotiated (default None). SNACK requires ERL >= 1. | [overreach] In case a.2 the initiator must wait for the status and discard it, signalling the CHECK CONDITION internally. If status was not yet sent, the target terminates the command with 'SNACK rejected' instead. Either party may also escalate to session recovery. [fidelity] The CHECK CONDITION is signalled internally by the initiator, which discards the target's status; the target does not send it in this case. |
| 14-C15 | iSCSI digests default to None. When enabled, they are CRC32C error-detection checks that cover the whole path including routers, switches and proxies, beyond link-layer checks. | RFC 7143, §13.1 HeaderDigest and DataDigest. <https://www.rfc-editor.org/rfc/rfc7143.txt> | N | VERIFIED (3S/0R/0U) | iSCSI over TCP. | [overreach] 'When enabled, they are CRC32C' is too broad. CRC32C is the only standard algorithm that MUST be implemented, but 'Private or public extension algorithms MAY also be negotiated for digests'. The digests are non-cryptographic. |
| 14-C16 | With iSER (iSCSI over RDMA), iSCSI digests must be None, integrity is delegated to the RDMA-capable protocol, read data travels as RDMA Writes, and SNACK must not be used. The stated reason is that no digest or sequence errors occur. | RFC 7145, iSCSI Extensions for RDMA (iSER), §6.1 / key negotiation text; §7.3.11 SNACK Request; §10.1.4.2-3. <https://www.rfc-editor.org/rfc/rfc7145.txt> | N | VERIFIED (3S/0R/0U) | iSER-assisted iSCSI connections over iWARP/InfiniBand/RoCE (RCaP). | [overreach] The stated reason is limited to the iSCSI layer in iSER-assisted mode: no iSCSI digest errors because digests are None, and no sequence errors because RCaP delivers in order. Integrity errors are still possible; RCaP is responsible for them. RFC 7145 otherwise says the iSCSI error recovery hierarchy 'is fully supported'. |
| 14-C17 | In a field study of about 39,000 storage systems, physical interconnect failures made up 27-68% of storage subsystem failures. Systems with redundant interconnects (multipathing) had 30-40% lower subsystem AFR. | Jiang, Hu, Zhou, Kanevsky, 'Are Disks the Dominant Contributor for Storage Failures?', FAST 2008, Abstract; §4 Finding (7). <https://www.usenix.org/legacy/event/fast08/tech/full_papers/jiang/jiang.pdf> | E | VERIFIED (3S/0R/0U) | NetApp FC back-end interconnects (storage head to disk shelves), 44 months, 1.8M disks. Not host-to-array iSCSI/NVMe-oF. | [overreach] In this paper 'physical interconnects' explicitly include shelf enclosures (backplanes, power, cooling, cables, HBAs), not just links. 27-68% is a range across system classes. The applicability caveat (NetApp FC back-end, not host-to-array networks) is correct and important. [currency] The paper's 'physical interconnects' explicitly include shelf enclosures (backplanes, power), not only cables and HBAs. |
| 14-C18 | Internet traces show that the TCP checksum fails to detect errors in roughly 1 in 16 million to 10 billion packets. The authors recommend application-level checksums for some applications. | Stone & Partridge, 'When the CRC and TCP Checksum Disagree', SIGCOMM 2000, Abstract. <https://conferences.sigcomm.org/sigcomm/2000/conf/paper/sigcomm2000-9-1.pdf> | E | VERIFIED (3S/0R/0U) | TCP/IP traffic in 1998-2000 traces. Relevant to block protocols over TCP that run without digests (NBD; iSCSI/NVMe-TCP with digests off). | [overreach] The 1-in-16M-to-10B figure is the authors' estimate from analysis of the errors observed in the traces, not an undetected-error rate measured directly. The traces directly show checksum failures (detected errors) of 1 in 1,100 to 1 in 32,000 packets. 'Recommend' is slightly strong; the paper says 'strongly suggests'. |
| 14-C19 | The Linux NVMe host driver fails a request without retry if DNR is set or the retry count reaches nvme_max_retries (default 5). It fails over multipath requests with path errors to another path, and requeues I/O rather than failing it while any path is still resetting or connecting. | Linux kernel drivers/nvme/host/core.c and multipath.c (torvalds/linux master, fetched 2026-11-08), core.c nvme_decide_disposition(), nvme_max_retries; multipath.c nvme_failover_req(), nvme_ns_head_submit_bio(), nvme_available_path(). <https://raw.githubusercontent.com/torvalds/linux/master/drivers/nvme/host/multipath.c> | G | VERIFIED (3S/0R/0U) | Linux native NVMe multipath at one source revision. Not a protocol guarantee. | [overreach] The CONNECTING case counts only when NVME_NSHEAD_FAIL_ON_CTRL_LOSS is not set. Controllers with NVME_CTRL_FAILFAST_EXPIRED are skipped. A LIVE controller in ANA change state also counts, and delayed_removal_secs can keep I/O requeued. blk_noretry_request (failfast) requests are also failed without retry. All of this is at one source revision. [fidelity] The requeue-while-connecting behaviour is conditional. CONNECTING counts as available only if NVME_NSHEAD_FAIL_ON_CTRL_LOSS is not set, and controllers whose failfast timer has expired are skipped. Requests flagged no-retry (blk_noretry_request) also fail without retry. |
| 14-C20 | A Ceph librados read returns the number of bytes read on success, a byte-count convention that admits short results, and it reads from the snapshot selected on the I/O context. | Ceph documentation, librados (C) API, rados_read(); rados_aio_read(). <https://docs.ceph.com/en/latest/rados/api/librados/> | I | VERIFIED (3S/0R/0U) | RADOS object reads via librados (the layer under RBD). | [overreach] 'Admits short results' is inference from the byte-count return value; the docs do not state when fewer than len bytes come back. rados_aio_read's own return value is 0 on success; the byte count is the completion's return value. The snapshot applies only if one was set; LIBRADOS_SNAP_HEAD means normal reads. [fidelity] The doc does not say that short results can occur; 'admits short results' is an inference from the byte-count return value. rados_aio_read() itself returns 0 on success, and the byte count comes from the completion. The snapshot applies only if one was set with rados_ioctx_snap_set_read(). |
| **15** | **Taxonomies of data-access layers** | | | | | |
| 15-C1 | OpenDAL ErrorKind defines Conflict as a resource-state conflict that explicitly does not indicate retry safety. | OpenDAL core/core/src/types/error.rs (commit 532050ac), enum ErrorKind, variant Conflict. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/types/error.rs> | I | VERIFIED (3S/0R/0U) | OpenDAL taxonomy C1 | [overreach] Conflict is a recent addition (RFC-8145, 2026). Calling it part of a long-standing taxonomy would overstate it. |
| 15-C2 | OpenDAL ErrorStatus Permanent forbids retry and is the default status of a new Error. | OpenDAL core/core/src/types/error.rs, enum ErrorStatus::Permanent; Error::new. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/types/error.rs> | I | VERIFIED (3S/0R/0U) | OpenDAL retry axis C1 | [fidelity] ErrorStatus is a private enum (no `pub`), so callers do not see it directly as a type. |
| 15-C3 | OpenDAL defines a Persistent status for errors that were temporary but survived retries. | OpenDAL core/core/src/types/error.rs, enum ErrorStatus::Persistent. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/types/error.rs> | I | VERIFIED (3S/0R/0U) | OpenDAL retry axis; relates to transient/persistent distinction in prior G.1 | [overreach] Persistent is a SHOULD NOT. It is not a prohibition the way Permanent's MUST never is. |
| 15-C4 | RFC-8145 states that error kind and retry status are independent classification axes. | OpenDAL RFC-8145 conflict_error_kind (Start Date 2026-08-25), Summary. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/docs/rfcs/8145_conflict_error_kind.md> | I | VERIFIED (3S/0R/0U) | OpenDAL C2 | [overreach] The RFC says this while defining Conflict/ConditionNotMatch. It is an RFC design statement, not a general spec for all ErrorKinds, though ErrorStatus is a separate field in the code. |
| 15-C5 | RFC-8145 requires services to classify by native error code and operation context before falling back to HTTP status. | OpenDAL RFC-8145, Reference-level explanation, Service error mapping. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/docs/rfcs/8145_conflict_error_kind.md> | I | VERIFIED (3S/0R/0U) | OpenDAL C2/C3 | [overreach] The RFC states this as a declarative rule plus an 'initial mappings' table. It uses no MUST, so 'requires' is slightly strong. [fidelity] The RFC states this as a description ('Services classify...'), not with RFC-2119 'MUST' wording, so 'requires' is a slight overstatement. |
| 15-C6 | RFC-8145 defines set_temporary as safe replay of the same method at the receiving layer, not eventual success of a broader workflow. | OpenDAL RFC-8145, Retry contract. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/docs/rfcs/8145_conflict_error_kind.md> | I | VERIFIED (3S/0R/0U) | OpenDAL C2 |  |
| 15-C7 | OpenDAL's service-implementation guide mandates returning structured errors with the correct ErrorKind. | OpenDAL core/core/src/docs/internals/service.rs, Operation methods, 'An implementation must'. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/docs/internals/service.rs> | I | VERIFIED (3S/0R/0U) | OpenDAL C3 | [overreach] This is a contributor guide (rustdoc). It does not define what 'correct' means for each backend and nothing enforces it in code. |
| 15-C8 | OpenDAL's S3 service maps NoSuchBucket (HTTP 404) to ConfigInvalid, not NotFound, via error-code-first classification. | OpenDAL core/services/s3/src/core.rs, fn parse_s3_error_code. <https://raw.githubusercontent.com/apache/opendal/main/core/services/s3/src/core.rs> | G | VERIFIED (3S/0R/0U) | OpenDAL C3 mapping in code | [overreach] Precisely: the status is mapped first, then a recognised native error code overrides it. This is S3-service-specific code, not a general OpenDAL property. |
| 15-C9 | OpenDAL maps any unrecognised std::io error kind to Unexpected marked temporary (retryable). | OpenDAL core/core/src/raw/std_io_util.rs, fn new_std_io_error. <https://raw.githubusercontent.com/apache/opendal/main/core/core/src/raw/std_io_util.rs> | G | VERIFIED (3S/0R/0U) | OpenDAL C3; limit: UnexpectedEof collapsed into Unexpected | [overreach] UnexpectedEof is listed explicitly alongside Interrupted/TimedOut/WouldBlock rather than falling through '_', but the result is the same: Unexpected + temporary. [fidelity] UnexpectedEof is not caught by the wildcard. Line 38 maps Interrupted, UnexpectedEof, TimedOut and WouldBlock to (Unexpected, true) by name, so the result is the same as the wildcard. |
| 15-C10 | Hadoop's FSDataInputStream spec permits read(buffer) to return fewer bytes than requested, down to one, but requires blocking until at least one byte. | Hadoop filesystem/fsdatainputstream.md (trunk), InputStream.read(buffer[], offset, length), Postconditions. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-common-project/hadoop-common/src/site/markdown/filesystem/fsdatainputstream.md> | N | VERIFIED (3S/0R/0U) | Hadoop read semantics C1 (partial) | [overreach] The postconditions return -1 at EOF and 0 when length==0, so the at-least-1 range applies only when data is available. |
| 15-C11 | Hadoop's spec leaves destination buffer contents undefined after a failed positioned read. | Hadoop fsdatainputstream.md, PositionedReadable, Failure states. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-common-project/hadoop-common/src/site/markdown/filesystem/fsdatainputstream.md> | N | VERIFIED (3S/0R/0U) | Hadoop read outcome semantics |  |
| 15-C12 | Hadoop's spec allows named exceptions to be raised as subclasses but never superclasses. | Hadoop filesystem/introduction.md, Core Expectations, Operations and failures. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-common-project/hadoop-common/src/site/markdown/filesystem/introduction.md> | N | VERIFIED (3S/0R/0U) | Hadoop C2 rule |  |
| 15-C13 | Hadoop's spec states no retryability classification; it only permits retry under happens-before constraints. | Hadoop filesystem/introduction.md, Operations and failures. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-common-project/hadoop-common/src/site/markdown/filesystem/introduction.md> | N | VERIFIED (3S/0R/0U) | Hadoop C2 gap (no retry axis) | [overreach] 'Only permits retry under happens-before constraints' overreaches for the spec as a whole. Other pages set operation-specific retry rules: abortable.md says 'The stream MUST retry any remote calls needed to force the abort outcome' and 'SHOULD NOT retry cleanup operations'; outputstream.md says close() 'MUST NOT retry the write'; bulkdelete.md notes weak idempotency on retries. So the spec has per-operation retry obligations but no retry axis on errors. [fidelity] Treat the 'no retryability classification' half as an absence finding for introduction.md only, not for the whole spec. |
| 15-C14 | Hadoop's S3A connector maps HTTP 416 to RangeNotSatisfiableEOFException and its retry policy marks that class fail. | Hadoop hadoop-aws S3AUtils.java and S3ARetryPolicy.java (trunk), S3AUtils.translateException case SC_416; S3ARetryPolicy policyMap. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-tools/hadoop-aws/src/main/java/org/apache/hadoop/fs/s3a/S3ARetryPolicy.java> | G | VERIFIED (3S/0R/0U) | Hadoop C3: connector-local retry classification, not in spec | [overreach] This is behaviour of the S3A connector on trunk only, not of the Hadoop FileSystem spec. |
| 15-C15 | The Hadoop FileSystem specification describes itself as incomplete, including on failure modes. | Hadoop filesystem/extending.md, opening section. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-common-project/hadoop-common/src/site/markdown/filesystem/extending.md> | N | VERIFIED (3S/0R/0U) | Hadoop C4/limits | [overreach] On failure modes the text is softer than the claim: it says covered operations 'may' have minor issues with failure modes. It does not say failure modes are systematically missing. |
| 15-C16 | Arrow object_store's Error enum has a Generic variant defined as the fallback when no other variant matches. | arrow-rs-object-store src/lib.rs (0.14.2, commit c216edef), pub enum Error, Generic. <https://raw.githubusercontent.com/apache/arrow-rs-object-store/main/src/lib.rs> | I | VERIFIED (3S/0R/0U) | object_store C1/C2 | [overreach] I checked main and did not confirm the version/commit pin (0.14.2, c216edef). |
| 15-C17 | object_store's generic HTTP mapping turns HTTP 409 Conflict into Error::AlreadyExists. | arrow-rs-object-store src/client/retry.rs, impl RetryError, fn error. <https://raw.githubusercontent.com/apache/arrow-rs-object-store/main/src/client/retry.rs> | G | VERIFIED (3S/0R/0U) | object_store C3; contrasts with OpenDAL RFC-8145 | [overreach] This is the shared client fallback. Individual store implementations may map errors before it runs. Separately, the retry loop can retry 409 when retry_on_conflict is set. [fidelity] retry.rs also has an opt-in retry_on_conflict flag (line 431) that retries 409 at the transport level. |
| 15-C18 | object_store's HttpErrorKind documents retry behaviour per variant, retrying Timeout only for idempotent requests. | arrow-rs-object-store src/client/http/connection.rs, pub enum HttpErrorKind, Timeout. <https://raw.githubusercontent.com/apache/arrow-rs-object-store/main/src/client/http/connection.rs> | I | VERIFIED (3S/0R/0U) | object_store retry axis (transport level only) | [overreach] Interrupted shares the idempotent-only rule with Timeout, so Timeout is not the only such variant. This axis is HTTP transport level and separate from crate::Error. [fidelity] Interrupted also says it is retried only if the request is idempotent. |
| 15-C19 | object_store states it mirrors object store APIs with stateless operations rather than cursor-based file interfaces. | arrow-rs-object-store src/lib.rs crate docs, Why not a Filesystem Interface?. <https://raw.githubusercontent.com/apache/arrow-rs-object-store/main/src/lib.rs> | I | VERIFIED (3S/0R/0U) | object_store purpose/scope |  |
| 15-C20 | fsspec defines only two custom exception classes, neither a storage outcome taxonomy. | fsspec fsspec/exceptions.py (commit 12c823bc), whole file. <https://raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/exceptions.py> | G | CONTESTED (2S/1R/0U) | fsspec NOT FOUND | [overreach] fsspec's exceptions.py defines only two custom exception classes. Other custom exceptions in the package are local to modules or implementations, and none of them forms a storage outcome taxonomy. [currency] Narrow the claim: fsspec/exceptions.py defines only two custom exceptions, but the package defines others elsewhere (ReferenceNotReachable in implementations/reference.py, DatabricksException in implementations/dbfs.py, TransferDone in implementations/ftp.py, FSSpecCoroutineCancel in asyn.py). Each is local to one implementation and none forms a taxonomy, so the NOT FOUND conclusion stands. |
| 15-C21 | fsspec's retryable-status set for HTTP is local to the HTTP implementation. | fsspec fsspec/implementations/http.py, module constants, _is_retryable. <https://raw.githubusercontent.com/fsspec/filesystem_spec/master/fsspec/implementations/http.py> | G | VERIFIED (3S/0R/0U) | fsspec C3 failed at layer level | [overreach] Callers can override it via the retry_statuses parameter (line 210). [fidelity] The set is a default that callers can override with the HTTPFileSystem retry_statuses parameter (line 210). |
| 15-C22 | Go CDK blob drivers must report a gcerrors.ErrorCode for errors they return. | go-cloud blob/driver/driver.go, Bucket interface, ErrorCode. <https://raw.githubusercontent.com/google/go-cloud/master/blob/driver/driver.go> | I | VERIFIED (3S/0R/0U) | screening lead only | [overreach] Implementing ErrorCode is mandatory because it is an interface method, but the doc wording is 'should return', and the doc does not dictate which code to use for each error. [fidelity] The doc uses 'should return', not 'must'. Strictly, the obligation is that drivers implement the ErrorCode method, which is required by the interface. |
| 15-C23 | rclone's fserrors defines an optional Retrier interface signalling high-level retry. | rclone fs/fserrors/error.go, Retrier interface comment. <https://raw.githubusercontent.com/rclone/rclone/master/fs/fserrors/error.go> | I | VERIFIED (3S/0R/0U) | screening only | [overreach] Retrier is one of three optional retry-hint interfaces (with NoRetrier and NoLowLevelRetrier). It is not an outcome taxonomy. |

---

## F. Knowledge gaps

### F.1 Gaps in the literature itself

These are gaps the sources read either state or make evident. Items marked *(inference)* are this research's reading.

1. **No ratified standards for SFTP or SCP.** Every SFTP version exists only as an expired draft, and SCP has no specification at all. Evidence about their behaviour therefore comes from implementations, release notes and CVEs [13-C9, 13-C15].
2. **Truncation of a TLS-protected FTP data connection.** RFC 4217 has no normative rule for detecting it [13-C8].
3. **Source changes during a read.** FTP, SFTP v3 and TFTP define no way to detect that the source changed during a single read. FTP's MDTM check before resuming is a heuristic [13-C7].
4. **Read atomicity in remote block protocols.** Neither NBD nor NVMe/TCP defines read atomicity against concurrent writes over other connections or paths. NBD's `CAN_MULTI_CONN` flag covers only flush/FUA visibility (track 14).
5. **NBD reconnect and resume.** NBD defines no reconnect or resume semantics. Recovering after a hard disconnect in the middle of a read is left to client policy (track 14).
6. **Field studies** *(as far as searched)*. No peer-reviewed field study was found of truncation, resume errors or retry outcomes on the read paths of FTP, SFTP, TFTP, iSCSI, NVMe/TCP or NBD. The only empirical integrity data are Globus logs [13-C22] and fault injection [13-C23]. Jiang et al. covers FC back ends only [14-C17].
7. **Access layers.** Within the sources read:
   - no access layer defines an outcome class for a truncated or mid-stream read failure;
   - no access layer states coverage or exclusivity for its full set of kinds. OpenDAL states it only among the condition, conflict and existence kinds (track 15).

### F.2 Gaps in this research's coverage

**Track 13.** These sources were not read:
- RFC 2228, RFC 2428 and the TLS closure text in RFC 8446;
- GridFTP (GFD.20) and MODE Z;
- AFS/Coda and 9P2000.L;
- BitTorrent v2 (BEP 52);
- the rsync wire-protocol internals;
- the deployment status of the SFTP check-file extension.

RIVA's publication venue was not confirmed from the copy read.

**Track 14.**
- Unreachable: Fibre Channel FCP-4/5, FC-NVMe and SRP (T10/T11 drafts not publicly reachable); the ATA over Ethernet specification; the Linux dm-multipath documentation at the path tried.
- Not read in full: the NVMe-oF RDMA and FC bindings, and the NVMe Keep Alive and controller-reset sections.
- Not covered: Ceph RBD beyond librados; NBD's experimental extensions.

**Track 15.**
- **OpenDAL:** the Reader and stream semantics were not read.
- **Go CDK `gcerrors`:** a strong lead, but criteria C2 and C4 were not assessed.
- **Hadoop:** the JIRA history behind the specification was not read.
- **Other candidates not read:** jclouds, libcloud, Alluxio, JuiceFS and cloud-SDK retry classifiers.

**Currency** *(verifier-reported)*. NVMe Base 2.4 and NVMe/TCP Rev 1.3 (2026) have superseded the revisions cited, with the relevant text unchanged.

---

## G. Additions to the foundation for later taxonomy work

This section lists building material and tensions. It does not propose a structure.

### G.1 Further established distinctions

| Distinction (source terms) | Defined by | Scope / caveat |
|---|---|---|
| Transient vs permanent negative completion (4yz/5yz) | RFC 959 [13-C4] | The RFC itself calls "transient" hard to define |
| Kind of failure vs retry status as independent axes; Permanent / Temporary / Persistent | OpenDAL RFC-8145, error.rs [15-C2–C4, 15-C6] | Implementation documentation; recent |
| Transient error turning persistent after N retries; do-not-retry anywhere in the subsystem; retry delay | NVMe Base [14-C9, 14-C10] | "Should"-level recommendations |
| Unrestricted / Delayed / State-Dependent retry after loss of communication | NVMe Base [14-C12] | Conditional on idempotence and effects bits |
| Path-related outcomes (retry on another path; inaccessible; persistent loss; transition) | NVMe ANA [14-C11] | Multipath hosts |
| Fatal transport error vs non-fatal per-command error | NVMe/TCP [14-C8] | Requires the optional digests |
| Error-recovery levels: session, digest, connection | iSCSI [14-C13] | Negotiated; only level 0 mandatory |
| All-or-nothing vs chunked read replies; whole-reply vs localised error | NBD [14-C1–C3] | Project-level specification |
| In-order vs reorderable read data (within a command, across requests) | NVMe/TCP [14-C7]; NBD [14-C2, 14-C4]; SFTP [13-C10] | Per protocol |
| Data flagged as suspect but still delivered | FTP MODE B [13-C2] | Rarely deployed |
| Transmitted octets vs stored octets | FTP SIZE/TYPE [13-C5] | Depends on TYPE, MODE and STRU |
| Data received is bounded by an atomic transfer unit | 9P `iounit` [13-C19]; NVMe AWUPF (03-C6) | Guarantee only when advertised |
| Formal pre- and postconditions on reads, without outcome classes | Hadoop FileSystem specification [15-C10–C13] | Self-declared incomplete |

### G.2 Tensions the new evidence adds

- **Taxonomies that work at different levels.** Protocol-level classes such as FTP reply codes, NVMe status, ANA and iSCSI ERL coexist with access-layer classes such as OpenDAL's, which map from them with loss of information [15-C8, 15-C9]. Any later work has to say at which level its classes apply.
- **The same status mapped differently.** For example, HTTP 409 becomes Conflict or AlreadyExists depending on the layer [15-C17].
- **Retryability defined in different ways.** It is a property of the command in NVMe [14-C12], a property of the status in NVMe and OpenDAL [14-C9, 15-C2], and a fuzzy agreement between parties in FTP [13-C4].
- **De facto vs ratified sources.** Some of the most precise read semantics found here, in NBD and SFTP, come from texts no standards body has ratified. The earlier report's guidance to "not confuse convention with guarantee" applies directly.
- **Structurally weaker detection of truncation.** In unframed, close-delimited transfers (FTP stream mode, FTPS without a truncation rule), truncation is harder to detect than in framed protocols (TFTP, NBD, NVMe/TCP). This adds to the earlier report's gap F.1-2.

---

## H. Annotated primary-source bibliography (additions)

This lists the distinct sources the three tracks consulted, deduplicated by link. Access status:
- *read in full*: supports claims;
- *partially read*: used in part;
- *UNREACHABLE*: no claim rests on it.

Section references and annotations are the tracks' own.

### H.13 File-transfer and remote file-access protocols

- **Postel & Reynolds, RFC 959 File Transfer Protocol, 1985**. <https://www.rfc-editor.org/rfc/rfc959.txt>. *read in full*. Sections: 3.1.1.3, 3.4, 3.5, 4.1.3 ABOR, 4.2, 5.2. Stream/block modes, EOF signalling, TYPE transformation, restart, reply-code classes
- **Braden (ed.), RFC 1123 Requirements for Internet Hosts, 1989**. <https://www.rfc-editor.org/rfc/rfc1123.txt>. *read in full*. Sections: 4.1.3.4, 4.2.3.1. FTP restart reply correction; TFTP Sorcerer's Apprentice fix
- **Hethmon, RFC 3659 Extensions to FTP, 2007**. <https://www.rfc-editor.org/rfc/rfc3659.txt>. *read in full*. Sections: 3, 4, 5, 7.5.2. SIZE exactness, REST STREAM offsets, MDTM-based restart safety, MLST unique fact
- **Ford-Hutchinson, RFC 4217 Securing FTP with TLS, 2005**. <https://www.rfc-editor.org/rfc/rfc4217.txt>. *read in full*. Sections: 9, 12.6-12.7. PROT levels; absence of truncation rule
- **Ylonen & Lehtinen, draft-ietf-secsh-filexfer-02 (SFTP v3), expired I-D, 2001**. <https://www.ietf.org/archive/id/draft-ietf-secsh-filexfer-02.txt>. *read in full*. Sections: 6.1, 6.3, 6.4, 7. READ semantics, binary mode, reply ordering, status codes
- **Galbraith & Saarenmaa, draft-ietf-secsh-filexfer-13 (SFTP v6), expired I-D, 2006**. <https://www.ietf.org/archive/id/draft-ietf-secsh-filexfer-13.txt>. *read in full*. Sections: 8.1.1.3, 8.2.1, 9.1, 9.3. Short-read allowance, end-of-file flag, max-read-size, text mode, byte-range locks
- **Galbraith & Saarenmaa, draft-ietf-secsh-filexfer-extensions-00, expired I-D, 2006**. <https://www.ietf.org/archive/id/draft-ietf-secsh-filexfer-extensions-00.txt>. *partially read*. Sections: 3. check-file per-block hashing extension
- **OpenSSH PROTOCOL file**. <https://raw.githubusercontent.com/openssh/openssh-portable/master/PROTOCOL>. *read in full*. Sections: header, 4.6, 4.8. OpenSSH implements SFTP v3 only; limits extension and short DATA
- **OpenSSH sftp-server.c and sftp-client.c (master)**. <https://raw.githubusercontent.com/openssh/openssh-portable/master/sftp-client.c>. *read in full*. Sections: process_read; sftp_download. Server read cap; client short-read re-request, truncation at highwater, resume refusal on reorder
- **OpenSSH 8.0 / 8.3 / 9.0 release notes**. <https://www.openssh.com/txt/release-8.0>. *read in full*. Sections: security and incompatibility sections (also release-8.3, release-9.0). scp CVE-2019-6111, scp desync, scp to SFTP switch
- **Sollins, RFC 1350 TFTP Revision 2, 1992**. <https://www.rfc-editor.org/rfc/rfc1350.txt>. *read in full*. Sections: 2, 5, 6, 7. Short-block EOF, lock-step ACK, unreliable error packets, completion ambiguity
- **RFC 2347/2348/2349 TFTP options; RFC 7440 Windowsize**. <https://www.rfc-editor.org/rfc/rfc2348.txt>. *read in full*. Sections: option specifications. blksize final-packet rule incl. zero-length packet; tsize; windowsize recovery
- **Dusseault (ed.), RFC 4918 WebDAV, 2007**. <https://www.rfc-editor.org/rfc/rfc4918.txt>. *partially read*. Sections: 6.6, 7, 8.6. Only write locks; locks may disappear; ETags for lost update
- **Tridgell & Mackerras, The rsync algorithm (TR-CS-96-05), HTML edition**. <https://rsync.samba.org/tech_report/node2.html>. *read in full*. Sections: nodes 1-4. Block checksums, short last block, probabilistic strong-checksum match
- **rsync(1) manual page**. <https://download.samba.org/pub/rsync/rsync.1>. *read in full*. Sections: --checksum, --append, --partial, EXIT VALUES. Whole-file verification, quick check, --partial/--append semantics and version difference, exit codes
- **Cohen, BEP 3 The BitTorrent Protocol Specification**. <https://www.bittorrent.org/beps/bep_0003.html>. *read in full*. Sections: metainfo, peer messages. Piece SHA1 verification, 'have' after hash check, request size convention
- **Plan 9 manual read(5), intro(5)**. <https://9p.io/magic/man2html/5/read>. *read in full*. Sections: read(5), intro(5). 9P short reads, zero count at EOF, iounit, tags, Rerror, qid.version
- **Liu, Kettimuthu, Foster, Rao, HPDC 2018**. <https://lzhengchun.github.io/file/hpdc2018.pdf>. *read in full*. Sections: 4.1, Observation 6. Empirical checksum-failure rates in Globus transfers
- **Charyyev & Arslan, RIVA (NSF PAR manuscript)**. <https://par.nsf.gov/servlets/purl/10130450>. *read in full*. Sections: Abstract, 2.1-2.3. Page-cache defeat of end-to-end integrity verification; fault injection

### H.14 Remote and networked block-storage protocols

- **NBD protocol, doc/proto.md, NetworkBlockDevice/nbd (master, fetched 2026-11-08)**. <https://raw.githubusercontent.com/NetworkBlockDevice/nbd/master/doc/proto.md>. *read in full*. Sections: Transmission; NBD_CMD_READ; Structured reply types; Error values; About this file. De facto NBD spec: simple vs structured replies, chunk types, error values, ordering, disconnects, block status, multi-conn.
- **NVM Express TCP Transport Specification, Revision 1.1, 2024-08-05**. <https://nvmexpress.org/wp-content/uploads/NVM-Express-TCP-Transport-Specification-Revision-1.1-2024.08.05-Ratified.pdf>. *read in full*. Sections: §3.3.1.1, §3.3.2.1, §3.4, §3.5, §3.6.2.4. C2HData ordering and offsets, LAST_PDU/SUCCESS, CRC32C digests, fatal vs non-fatal errors, Keep Alive.
- **NVM Express Base Specification, Revision 2.1, 2024-08-05**. <https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf>. *partially read*. Sections: Fig. 100; generic status 22h; Fig. 107; §8.1.2; §9.6. DNR/CRD, Transient Transport Error, path-related status and ANA, communication loss and retry categories.
- **Chadalapaka et al., RFC 7143, iSCSI Protocol (Consolidated), April 2014**. <https://www.rfc-editor.org/rfc/rfc7143.txt>. *read in full*. Sections: §7.1.4-7.2.1, §7.8-7.9, §13.1, §13.18-13.20. Recovery classes and ERL hierarchy, digest error handling, SNACK, ordering keys, retry semantics.
- **Ko & Nezhinsky, RFC 7145, iSCSI Extensions for RDMA (iSER), April 2014**. <https://www.rfc-editor.org/rfc/rfc7145.txt>. *read in full*. Sections: §1 summary, key negotiation, §7.3.11, §10.1. Digests None, RCaP integrity and ordering, no SNACK.
- **Sheinwald et al., RFC 3385, iSCSI CRC/Checksum Considerations (Informational)**. <https://www.rfc-editor.org/rfc/rfc3385.txt>. *read in full*. Sections: skimmed. Background on the CRC32C choice. No claim based on it.
- **Jiang, Hu, Zhou, Kanevsky, Are Disks the Dominant Contributor for Storage Failures?, FAST 2008**. <https://www.usenix.org/legacy/event/fast08/tech/full_papers/jiang/jiang.pdf>. *read in full*. Sections: Abstract, §2.3, Finding 7. Field rates of interconnect and protocol failures and the effect of multipathing.
- **Bairavasundaram et al., An Analysis of Data Corruption in the Storage Stack, FAST 2008**. <https://www.usenix.org/legacy/event/fast08/tech/full_papers/bairavasundaram/bairavasundaram.pdf>. *read in full*. Sections: §1-3. Context only: data-path corruption as a cause of checksum mismatch; transport errors excluded.
- **Stone & Partridge, When the CRC and TCP Checksum Disagree, SIGCOMM 2000**. <https://conferences.sigcomm.org/sigcomm/2000/conf/paper/sigcomm2000-9-1.pdf>. *read in full*. Sections: Abstract, §1-2. TCP checksum undetected-error rates.
- **Linux kernel drivers/nvme/host/multipath.c and core.c (master, 2026-11-08)**. <https://raw.githubusercontent.com/torvalds/linux/master/drivers/nvme/host/multipath.c>. *read in full*. Sections: nvme_failover_req, nvme_ns_head_submit_bio, nvme_available_path, nvme_decide_disposition. Implementation failover, retry and requeue behaviour.
- **Linux Documentation/admin-guide/nvme-multipath.rst**. <https://raw.githubusercontent.com/torvalds/linux/master/Documentation/admin-guide/nvme-multipath.rst>. *read in full*. Sections: all. Path policies only (numa, round-robin, queue-depth).
- **Linux Documentation/admin-guide/device-mapper/dm-multipath.rst**. <https://raw.githubusercontent.com/torvalds/linux/master/Documentation/admin-guide/device-mapper/dm-multipath.rst>. *UNREACHABLE: not used as evidence*. None (404 at this path).
- **Linux drivers/block/aoe/aoecmd.c and aoe.rst**. <https://raw.githubusercontent.com/torvalds/linux/master/drivers/block/aoe/aoecmd.c>. *partially read*. Sections: module parameters, rexmit timer. aoe_deadsecs device-failure timeout.
- **Coraid / Brantley Coile, ATA over Ethernet specification AoEr11**. <http://support.coraid.com/documents/AoEr11.txt>. *UNREACHABLE: not used as evidence*. None (all mirrors failed).
- **Ceph librados C API documentation**. <https://docs.ceph.com/en/latest/rados/api/librados/>. *read in full*. Sections: rados_read, rados_aio_read. rados_read / rados_aio_read return byte count and snapshot context.
- **T10 SRP / FCP-4/5, T11 FC-NVMe drafts**. <https://www.t10.org/drafts.htm>. *UNREACHABLE: not used as evidence*. None. Drafts are not public.

### H.15 Taxonomies of data-access layers

- **Apache OpenDAL source and docs (types/error.rs, capability.rs, docs/internals/service.rs, docs/specs/conditional-operations.md, services/s3/src/core.rs, raw/std_io_util.rs, layers/retry)**. <https://github.com/apache/opendal>. *read in full*. Sections: commit 532050ac. Confirmed two-axis error taxonomy and capability model with mandated mapping
- **OpenDAL RFCs 0044, 0247, 0977, 8145, 0409, 2852, 7700**. <https://github.com/apache/opendal/tree/main/core/core/src/docs/rfcs>. *read in full*. Sections: 0977, 0247, 8145 read in full; others headers/summaries. Design records: axes, retry contract, mapping rules
- **Apache Hadoop FileSystem specification**. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-common-project/hadoop-common/src/site/markdown/filesystem/>. *read in full*. Sections: index, introduction, notation, fsdatainputstream, extending, pathcapabilities, testing. Read model, exception rules, capabilities, incompleteness
- **Hadoop S3A S3AUtils.java, S3ARetryPolicy.java, ContractOptions.java**. <https://raw.githubusercontent.com/apache/hadoop/trunk/hadoop-tools/hadoop-aws/src/main/java/org/apache/hadoop/fs/s3a/>. *read in full*. Sections: translateException, policyMap. Connector-local mapping and retry classification
- **Apache arrow-rs-object-store**. <https://github.com/apache/arrow-rs-object-store>. *read in full*. Sections: src/lib.rs, src/client/retry.rs, src/client/http/connection.rs; v0.14.2. Error enum, HttpErrorKind, status mapping
- **fsspec filesystem_spec**. <https://github.com/fsspec/filesystem_spec>. *read in full*. Sections: exceptions.py, spec.py, implementations/http.py, docs developer.rst, changelog.rst. Absence of layer taxonomy; http retry policy
- **Go CDK gcerr.go and blob/driver/driver.go**. <https://github.com/google/go-cloud>. *partially read*. Sections: ErrorCode constants, Bucket.ErrorCode. Screening lead
- **rclone fs/fserrors/error.go**. <https://github.com/rclone/rclone>. *partially read*. Sections: Retrier, Fataler. Screening: retry-axis interfaces
