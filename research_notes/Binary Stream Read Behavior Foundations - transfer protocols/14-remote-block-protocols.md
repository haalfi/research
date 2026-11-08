# Track 14: Remote and networked block-storage protocols

Scope: what can happen when data is READ through remote block protocols (NBD, NVMe over Fabrics / NVMe/TCP, iSCSI, iSER, AoE, multipath layers, Ceph RADOS), plus field studies of interconnect and transport failures.
Method: full texts downloaded to the scratchpad (`dl2/remote-block-protocols/`). PDFs converted with pdftotext and searched with grep/sed. Search-engine extracts were used only to find sources. No AI-generated summary (including WebFetch output) is used as evidence. All fetches were made on 2026-11-08.

## 1. Sources and access status

| # | Source | Kind | Access | Notes |
|---|---|---|---|---|
| S1 | NBD protocol, `doc/proto.md`, NetworkBlockDevice/nbd master (raw.githubusercontent.com) | Project protocol document (de facto, NOT IETF/ISO-ratified). Uses RFC 2119 keywords. | FULL TEXT | Self-described as documenting the protocol "as it is currently implemented in the Linux kernel and in the reference implementation"; "does not come with any form of warranty". It is the authoritative project spec, but not a ratified standard. |
| S2 | NVM Express TCP Transport Specification, Rev 1.1 (2024-08-05, ratified) | Normative (NVMe consortium) | FULL TEXT (42 pp) | |
| S3 | NVM Express Base Specification, Rev 2.1 (2024-08-05, ratified) | Normative | FULL TEXT (searched: Fig. 100 status field, generic status 22h, path-related status Fig. 107, §8.1.2 ANA host considerations, §9.6 Communication Loss Handling) | 11.7 MB. Only the sections listed were read. |
| S4 | RFC 7143, iSCSI (Consolidated), April 2014 | Normative (Standards Track) | FULL TEXT (§7.1.4–7.2.1, 7.8–7.9, 13.1, 13.18–13.20 read) | |
| S5 | RFC 7145, iSER, April 2014 | Normative (Standards Track) | FULL TEXT (§1 summary, 5/6.1, 7.3.11, 10.1) | |
| S6 | RFC 3385, iSCSI CRC/Checksum Considerations | Informational RFC | FULL TEXT (skimmed) | Background for CRC32C choice. No claim rests on it. |
| S7 | Jiang, Hu, Zhou, Kanevsky, "Are Disks the Dominant Contributor for Storage Failures?", FAST 2008 | Peer-reviewed empirical | FULL TEXT | |
| S8 | Bairavasundaram et al., "An Analysis of Data Corruption in the Storage Stack", FAST 2008 | Peer-reviewed empirical | FULL TEXT (§1–3 read) | Not specific to a network protocol. Used only for context; see §4. |
| S9 | Stone & Partridge, "When the CRC and TCP Checksum Disagree", SIGCOMM 2000 | Peer-reviewed empirical | FULL TEXT (abstract, §1–2) | |
| S10 | Linux `drivers/nvme/host/multipath.c` and `core.c` (torvalds/linux master, fetched 2026-11-08) | Implementation (source code) | FULL TEXT (relevant functions) | Behaviour of one implementation at one revision, not a guarantee. |
| S11 | Linux `Documentation/admin-guide/nvme-multipath.rst` | Implementation doc | FULL TEXT | Covers path-selection policies only. Nothing on in-flight failover semantics. |
| S12 | Linux `Documentation/admin-guide/device-mapper/dm-multipath.rst` | Implementation doc | UNREACHABLE (404 at that path) | dm-multipath failover semantics were not covered. |
| S13 | Linux `drivers/block/aoe/aoecmd.c` and `Documentation/admin-guide/aoe/aoe.rst` | Implementation | FULL TEXT (parameters only) | |
| S14 | AoE specification AoEr11 (Coraid / Brantley Coile) | Vendor protocol spec | UNREACHABLE (support.coraid.com and thebrantleycoilecompany.com gave proxy 502; web.archive.org reset connections; coraid.com returned an HTML stub) | No claims are based on it. |
| S15 | Ceph librados C API docs (docs.ceph.com/en/latest/rados/api/librados/) | Official implementation doc | FULL TEXT (rados_read and rados_aio_read entries) | |
| S16 | Ceph RBD exclusive-locks doc | Official doc | Downloaded but not used (concerns writers/locking) | |
| S17 | T10 SRP / FCP-4/5, T11 FC-NVMe drafts | Normative drafts | UNREACHABLE / NOT PUBLIC (the URL fetched turned out to be unrelated ADI meeting minutes; current T10/T11 drafts require membership) | COVERAGE-GAP |

## 2. Findings (verbatim quotes with locators)

### 2.1 NBD (S1): de facto protocol document

**F1. Simple replies cannot express partial reads, and an error after the header forces a disconnect.**
proto.md, "Structured reply chunk message": "it is not possible to support partial reads or early errors (the command must succeed or fail as a whole; no payload is sent if *error* was set, but if *error* is zero and a later error is detected before *length* bytes are returned, the server must initiate a hard disconnect)".
`NBD_CMD_READ`, simple replies: "If an error occurs while reading after the server has already sent out the reply header with an error field set to zero (i.e., signalling no error), the server MUST immediately initiate a hard disconnect; it MUST NOT send any further data to the client."
→ With simple replies, the only signal of a mid-read failure is a TCP close. The bytes already received cannot be told apart from good data except by the absence of the remaining *length* bytes. Truncation is detectable only because the client knows the requested length *(inference)*.

**F2. Without negotiation the reply stream is not self-describing.**
"it is impossible to tell by reading the server traffic in isolation whether a data field will be present". Structured replies carry a length field so that "the overall server traffic" can be divided "into individual reply messages" in a context-free way.

**F3. Structured READ replies: chunk reassembly, ordering and the final flag.**
`NBD_CMD_READ`: the server "MAY send the content chunks in any order (the client MUST reassemble content chunks into the correct order), and MAY send additional content chunks even after reporting an error chunk." When no error is detected, the server "MUST send enough data chunks to cover the entire region". It must not mark a content chunk final "if it would still be possible to detect an error while transmitting the chunk".
Once structured replies are negotiated, the server "MUST NOT use a simple reply for `NBD_CMD_READ`".

**F4. Two error-chunk semantics for reads.**
`NBD_REPLY_TYPE_ERROR`: "the client MAY NOT make any assumptions about partial success".
In READ: "An error chunk of type `NBD_REPLY_TYPE_ERROR` implies that the client MAY NOT make any assumptions about validity of data chunks (whether sent before or after the error chunk)". `NBD_REPLY_TYPE_ERROR_OFFSET` "represents that an error occurred at a given offset ... the client can use this offset to determine if request had any partial success."
On error, the server "MUST still complete the transmission of any current chunk (it MUST use padding bytes which SHOULD be zero ...)". So padding bytes can arrive inside a data chunk that is later flagged as errored.
"A structured reply is considered successful only if it did not contain any error chunks, although the client MAY be able to determine partial success based on the chunks received."

**F5. Holes.** `NBD_REPLY_TYPE_OFFSET_HOLE` represents bytes that "read as all zeroes". The server may send it in place of data.

**F6. Reply ordering.** "Replies need not be sent in the same order as requests ... structured reply chunks from one request may be interleaved with reply messages from other requests". Correlation is by the opaque cookie (formerly called "handle").

**F7. Out-of-range reads and error values.**
Error values: "Originally, error messages were defined as the value of `errno` on the system running the server; however ... these values are in fact not well-defined, and therefore not entirely portable." The defined set is EPERM, EIO, ENOMEM, EINVAL, ENOSPC, EOVERFLOW, ENOTSUP and ESHUTDOWN.
The server "SHOULD return `NBD_EINVAL` if it receives a read or trim request including one or more sectors beyond the size of the device". "Which error to return in any other case is not specified by the NBD protocol." "The client SHOULD treat an unexpected error value as if it had been `NBD_EINVAL`, rather than disconnecting".
→ NBD has no EOF or short-read concept. A read past the export size is an error, unlike the NFSv4.1 eof flag [prior 07-C8].
The error codes are not classified as transient or permanent. The exceptions are ESHUTDOWN, which tells the client to disconnect ("If the client receives an `NBD_ESHUTDOWN` error it MUST initiate a soft disconnect"), and EOVERFLOW: a client "should be prepared to retry with smaller requests if a large request fails".

**F8. BLOCK_STATUS may be truncated.** "the server MAY return fewer descriptors in the reply than would be required to fully specify the whole range of requested information to the client, if looking up the information would be too resource-intensive for the server, so long as at least one extent is returned."

**F9. Multi-connection visibility.** `NBD_FLAG_CAN_MULTI_CONN`: "In the absence of this flag, clients SHOULD NOT multiplex their commands over more than one connection to the export." With the flag, FLUSH/FUA effects "MUST be visible across all connections".
The spec defines no read-versus-concurrent-write atomicity *(searched; none found)*.

**F10. Unknown reply types.** "If the client receives an unknown or unexpected type, other than an *error chunk*, it MUST initiate a hard disconnect." Unknown types with bit 15 set mark the reply as errored, but transmission may continue.

**F11. Reconnect.** proto.md does not define reconnection or resumption: a grep for "reconnect" finds nothing. Terminating transmission is either a soft disconnect (`NBD_CMD_DISC`) or a hard disconnect. Any re-reading after reconnect is a client policy *(inference from absence)*.

### 2.2 NVMe/TCP (S2) and NVMe Base (S3): normative

**F12. C2HData ordering and offsets.** §3.3.2.1: "The first C2HData PDU of a command shall start with an offset of zero and subsequent C2HData PDUs for the command shall transfer data sequentially to the end of the data buffer". "Reception of a non-contiguous C2HData PDU is treated as a fatal transport error". "C2HData PDUs for a command shall be sent in-order for a command but may be arbitrarily interleaved with other unrelated PDUs".
→ This is the opposite of NBD structured replies (F3), where chunks may arrive in any order.

**F13. End of read data and success signalling.** "C2HData PDUs contain a LAST_PDU bit that is set to '1' in the last PDU of a command data transfer". If the SUCCESS bit is set, "no Response Capsule is sent by the controller for the command and the host synthesizes a Completion Queue Entry". This is allowed "only if the controller supports disabling Submission Queue Head Pointer (SQHD) updates." SUCCESS without LAST_PDU is a fatal transport error.

**F14. Digests.** §3.3.1.1: HDGST and DDGST are optional and negotiated. They "are calculated using the CRC32C algorithm".

**F15. Header vs data digest errors.** §3.5: "A PDU Header digest error impacts TCP byte stream synchronization ... the host shall treat the error as a fatal transport error". "A PDU data digest error impacts the integrity of PDU data but does not impact the TCP byte stream synchronization ... When a host detects a data digest error in a C2HData PDU, that host shall continue processing C2HData PDUs associated with the command and when the command processing has completed, if a successful status was returned by the controller, the host shall fail the command with a non-fatal transport error."

**F16. Fatal vs non-fatal transport errors.** "NVMe/TCP transport fatal errors are handled by terminating the connection." Non-fatal: "These commands are likely to complete successfully if retried. When a non-fatal transport error is detected, affected commands are completed with a Transient Transport Error status code".
Fatal Error Status values (H2CTermReq): Invalid PDU Header Field, PDU Sequence Error, Header Digest Error, Data Transfer Out of Range, R2T Limit Exceeded, Unsupported Parameter.

**F17. Transient → persistent escalation.** Base 2.1, generic status 22h: "Transient Transport Error: A transient transport error was detected. If the command is retried on the same controller, the command is likely to succeed. A command that fails with a transient transport error four or more times should be treated as a persistent transport error that is not likely to succeed if retried on the same controller."

**F18. DNR and CRD.** Fig. 100: DNR "If this bit is set to '1', then this bit indicates that if the same command is re-submitted to any controller in the NVM subsystem, then that re-submitted command is expected to fail." CRD selects CRDT1–3: "The host should not retry the command until at least the amount of time indicated by the selected field has elapsed. It is not an error for the host to retry the command prior to that time."

**F19. Path-related status and ANA.** §(Path Related Status): "In a multipath environment, unless otherwise specified, errors of this type should be retried using a different path, if one is available."
- Asymmetric Access Inaccessible / Persistent Loss: "The command should not be re-submitted to the same controller."
- Asymmetric Access Transition: "The requested function should be retried after the transition is complete."
- Host Pathing Error (70h) and Command Aborted By Host (71h) are host-detected.
- §8.1.2 (Informative): the host should prefer ANA Optimized, then Non-Optimized controllers.

**F20. Keep Alive.** NVMe/TCP §3.4: "The NVMe/TCP Transport requires the use of the Keep Alive Timer feature ... The minimum should be set large enough to account for any transient fabric interconnect failures". It recommends that the TCP keepalive timeout exceed the NVMe KATO.

**F21. Communication loss and read retry.** Base §9.6:
- "A controller may detect a loss of communication at a different time (e.g., later) than the host".
- Before treating commands as dead, the host waits 2*KATT (command-based) or 3*KATT (traffic-based), then CQT or about 10 s.
- §9.6.3.1: "a read command addressed to a specific location (e.g., LBA) in a namespace is an idempotent command."
- §9.6.3.2.1: "A host may retry any outstanding command that is an Unrestricted Retry command immediately after communication loss without determining whether further controller processing of that outstanding command is possible." NVM Read is the example of Unrestricted Retry. Write is a Delayed Retry command.
- Note: the definition of the results of an idempotent command excludes "transient status codes or error conditions".

### 2.3 iSCSI (S4) and iSER (S5): normative

**F22. Error recovery levels.** RFC 7143 §7.1.5:
- Recovery classes are "within a command", "within a connection", "connection recovery" and "session recovery".
- ERL 0 = session recovery; 1 = digest failure recovery (+0); 2 = connection recovery (+1).
- "Implementations MUST support error recovery level "0", while the rest are OPTIONAL to implement."
- "The lower of the two exchanged values is the operational ErrorRecoveryLevel for the session." The default is 0 (§13.20).
- §7.1.4.4: session recovery means "terminating all outstanding SCSI commands with an appropriate SCSI service response at the initiator".
- §7.1.4.3 (ERL 2): on TCP connection failure, commands in progress are reassigned using "TASK REASSIGN". A command is in progress "as long as it has not received a response or a Data-In PDU including status."

**F23. Data-In digest error at the initiator.** §7.8: "When an initiator receives any iSCSI PDU with a payload digest error, it MUST discard the PDU. If the discarded PDU is an iSCSI data PDU, the initiator MUST do one of the following: a) Request the desired data PDU through SNACK ... b) Abort the task and terminate the command with an error."
If the SNACK is rejected after status was sent, the initiator "MUST wait for the status to be received and then discard it, so as to internally signal the completion with CHECK CONDITION Status and an iSCSI Condition of "Protocol Service CRC error"".
Header digest error: "it MUST either discard the header and all data up to the beginning of a later PDU or close the connection."
§7.9: an out-of-order DataSN "means that the initiator must have detected a header or payload digest error on one or more earlier R2T/data PDUs."

**F24. Digest scope.** §13.1: "Default is None for both HeaderDigest and DataDigest." "Digests enable the checking of end-to-end, non-cryptographic data integrity beyond the integrity checks provided by the link layers and the covering of the whole communication path, including all elements that may change the network-level PDUs, such as routers, switches, and proxies." CRC32C is mandatory to implement. "These digest options only have error detection significance."

**F25. Ordering keys.** §13.18 DataPDUInOrder (default Yes): "data PDUs within sequences have to be at continuously increasing addresses and overlays are forbidden." §13.19: with DataSequenceInOrder=Yes "an initiator may at most request retransmission for the last read data sequence."

**F26. Retry is not re-read.** §7.2.1: "Retry MUST NOT be used for reasons other than plugging command sequence gaps and, in particular, cannot be used for requesting PDU retransmissions from a target." "the usage of SNACK is OPTIONAL."

**F27. iSER delegates integrity and ordering to RDMA.** RFC 7145 §5/6.1: "When the RDMAExtensions key is negotiated to "Yes", the HeaderDigest and the DataDigest keys MUST be negotiated to "None" ... RCaP is responsible for providing error detection that is at least as good as a 32-bit CRC". "all SCSI Read data are sent using RDMA Write Messages instead of the SCSI Data-In PDUs".
§7.3.11: "there are no digest errors ... there are no sequence errors when the connection is in iSER-assisted mode. Therefore, the iSCSI layer MUST NOT send SNACK Request PDUs."
§1: "The iSCSI error recovery hierarchy defined in [iSCSI] is fully supported by iSER."

### 2.4 Implementations

**F28. Linux NVMe native multipath (S10, source code at master 2026-11-08).**
`nvme_decide_disposition()` in core.c:
- returns COMPLETE (the error goes to the caller) if `blk_noretry_request`, if the DNR bit is set, or if `retries >= nvme_max_retries` (default `static u8 nvme_max_retries = 5;`);
- for multipath requests, returns FAILOVER on `nvme_is_path_error(status)` or a dying queue;
- otherwise returns RETRY.

`nvme_failover_req()`: "If we got back an ANA error, we know the controller is alive but not ready to serve this namespace. Kick of a re-read of the ANA information page, and just try any other available path for now." The bios are stolen to the head's requeue list.

`nvme_ns_head_submit_bio`: "no usable path - requeuing I/O" while some path is available (e.g., a controller is RESETTING or CONNECTING). Otherwise: "no available path - failing I/O" (`bio_io_error`).
→ The caller sees an in-flight read as delayed (requeued), not failed, until no path is "available" *(reading of code; one revision)*.

**F29. Linux AoE driver (S13).** Parameter `aoe_deadsecs = 60 * 3`, "After aoe_deadsecs seconds, give up and fail dev." Retransmission is driver-timed. The protocol spec (S14) was UNREACHABLE, so what the AoE spec itself says about reads, retransmission or errors is unknown here.

**F30. Ceph librados (S15).** `rados_read(... size_t len, uint64_t off)`: "Returns: number of bytes read on success, negative error code on failure". `rados_aio_read`: "The return value of the completion will be number of bytes read on success". The read is from the snapshot set by `rados_ioctx_snap_set_read()`.
→ The return-count convention allows short reads, in POSIX style. The doc does not state what a read past the object end returns *(not stated in text read)*.

### 2.5 Empirical

**F31. Jiang et al. FAST'08 (S7).**
- Data: about 39,000 NetApp systems, 1.8M disks, 44 months.
- "physical interconnects and protocol stacks also account for significant percentages of storage subsystem failures". Physical interconnect failures are 27–68% of storage subsystem failures.
- Definitions: "When physical interconnect failures happen, affected disks appear to be missing from the system." Protocol failure: "disks are visible to the storage layer but I/O requests are not correctly responded by disks." Performance failure: "a disk cannot serve I/O requests in a timely manner while none of previous three types of failures are detected".
- Finding (7): "Storage subsystems configured with network redundancy mechanisms experience much lower (30-40% lower) AFR than other systems. AFR for physical interconnects is reduced by 50-60%."
- Applicability: FC-attached disk shelves behind storage heads (back-end interconnect), not host-to-array iSCSI/NVMe-oF.

**F32. Stone & Partridge SIGCOMM'00 (S9).** "between 1 packet in 1,100 and 1 packet in 32,000 fails the TCP checksum, even on links where link-level CRCs should catch all but 1 in 4 billion errors". "we conclude that the checksum will fail to detect errors for roughly 1 in 16 million to 10 billion packets". "some applications should employ application-level checksums or equivalents."
This is the empirical motivation consistent with the iSCSI and NVMe/TCP CRC32C digests (F14, F24). The RFCs' own citation of this paper was not verified here.

**F33. Bairavasundaram et al. FAST'08 (S8), context only.** A checksum mismatch may come from "data content corrupted by components within the data path". The study explicitly excludes "transport corruptions reported as SCSI transport errors". It therefore gives no rate for network-transport corruption.

## 3. Existing models and classifications (source terminology preserved)

- **iSCSI recovery classes and ErrorRecoveryLevel 0/1/2 hierarchy** (RFC 7143 §7.1.4–7.1.5). Normative, negotiated per session (minimum wins). Only ERL 0 is mandatory.
- **NVMe/TCP fatal vs non-fatal transport errors** (TCP Transport 1.1 §3.5). A fatal error terminates the connection; a non-fatal error gives Transient Transport Error and a likely retry success. Fatal Error Status enumeration.
- **NVMe status taxonomy elements**: Status Code Type (generic / command-specific / media / path-related), the DNR bit, CRD/CRDT1–3, and the "four or more times" rule for transient → persistent (Base 2.1).
- **NVMe ANA states**: Optimized, Non-Optimized, Inaccessible, Persistent Loss, Change, with mapped status codes (Base 2.1 §8.1).
- **NVMe command retry categories after communication loss**: Unrestricted Retry, Delayed Retry, State-Dependent Retry; idempotent vs non-idempotent (Base 2.1 §9.6.3).
- **NBD reply model**: simple reply vs structured reply; content chunks (OFFSET_DATA, OFFSET_HOLE) vs error chunks (ERROR, ERROR_OFFSET); soft vs hard disconnect (proto.md). This is a de facto spec.
- **Jiang et al. failure types**: disk failure, physical interconnect failure, protocol failure, performance failure (empirical classification).
- **Bairavasundaram et al. corruption classes**: checksum mismatch, identity discrepancy, parity inconsistency (context).

## 4. Convergences and contradictions

Between sources in this track:
- **Ordering of read data.**
  - NVMe/TCP C2HData must be in order per command [F12]. A non-contiguous PDU is fatal.
  - NBD structured chunks may be in any order and the client reassembles them [F3].
  - iSCSI makes ordering negotiable (DataPDUInOrder, DataSequenceInOrder) [F25].
  - iSER relies on RCaP in-order delivery [F27].

  These are design differences, not a conflict.
- **Data digest error handling differs.**
  - NVMe/TCP: always non-fatal. The host fails the whole command, with no per-PDU retransmission [F15].
  - iSCSI ERL≥1: SNACK retransmission of the PDU is possible; otherwise abort [F23].
  - iSER: digests are absent by design [F27].
  - NBD: defines no digest at all and relies on TCP/TLS *(inference from absence: grep of proto.md for digest/CRC finds none)*.
- **Header digest error.** NVMe/TCP: always fatal. iSCSI: discard up to a later PDU (needs Sync and Steering) or close. Both say the cause is unreliable length fields.
- **Mid-read failure.** NBD simple reply: hard disconnect, with no way to signal partial success [F1]. NBD structured: per-offset errors are possible [F4]. NVMe: no partial-success signal in the sources read. The command fails as a unit, and a host-detected data digest error overrides a successful status [F15].
- **Truncation.** NBD BLOCK_STATUS may legitimately return less than requested [F8], while NBD READ must cover the whole range when no error occurs [F3]. Within one protocol, metadata reads and data reads differ.

With the prior report (`reports/Binary Stream Read Behavior Foundations.md`, §B.7 and §D):
- **Converges with D.1.1** ("Completion status and data correctness are separate"):
  - The NVMe/TCP host must fail a command that the controller reported as successful if a C2HData digest failed [F15].
  - NBD ERROR chunks invalidate data chunks sent before them [F4].
  - Stone & Partridge [F32] is the same evidence base as the prior report's 07-C18 (TCP checksums miss errors).
- **Converges with D.1.2** (detectability depends on where the check sits):
  - iSCSI digests are explicitly meant to cover routers, switches and proxies beyond link CRCs [F24].
  - iSER moves the check into RCaP [F27].
  - NVMe/TCP digests are optional and negotiated, so whether they are present is configuration-dependent [F14].
- **Diverges from or extends D.1.4** (partial results normal in most read interfaces):
  - NBD READ never returns a short successful read. Out-of-range reads are NBD_EINVAL [F7], and a partial outcome exists only as error chunks plus content chunks [F4].
  - NVMe/TCP likewise has no short-success notion in the text read.
  - So these block protocols sit with SMB2's MinimumCount style (07-C10) rather than with NFSv4.1 short reads (07-C8). iSCSI residual underflow (07-C11) is the SCSI-layer exception.
  - librados returns a byte count [F30], aligning with the POSIX style (01-C1).
- **Extends D.3 "Data together with an error":** NBD structured replies explicitly allow valid data chunks alongside an ERROR_OFFSET chunk [F4]. This is a block-protocol instance of Go-style "n>0 with error" (02-C6). NVMe/TCP and NBD simple replies do not allow it.
- **Extends 07-C6** (GET idempotent and auto-retryable): NVMe Base classifies Read as idempotent, Unrestricted Retry [F21]. iSCSI retry has a narrower meaning (plugging CmdSN gaps only) [F26].
- **Extends D.1.5** (masking turns errors into latency): Linux NVMe multipath requeues I/O while any path is resetting or connecting [F28]. NVMe CRD imposes retry delays [F18]. AoE fails the device after `aoe_deadsecs` [F29]. All are implementation or policy knobs.
- No contradiction with any prior-report claim was found.

## 5. Gaps

- **COVERAGE-GAP**: Fibre Channel FCP-4/FCP-5 (FCP_RSP residuals, sequence-level error recovery), FC-NVMe and SRP. The T10/T11 drafts were not publicly reachable.
- **COVERAGE-GAP**: NVMe over Fabrics RDMA transport binding and FC transport binding were not read. The NVMe-oF reconnect/controller-reset sections of Base 2.1 (§3.3, 3.9 Keep Alive details) were read only via §9.6 cross-references.
- **COVERAGE-GAP**: AoE specification UNREACHABLE (S14). dm-multipath doc UNREACHABLE at the path tried (S12); `queue_if_no_path` semantics were not verified.
- **COVERAGE-GAP**: The Ceph RBD read path (librbd, read from replica vs primary, `rbd_read` semantics beyond librados) and RADOS consistency were not read in depth.
- **COVERAGE-GAP**: NBD experimental extensions (EXTENDED_HEADERS, RESIZE) live on separate branches of the nbd repository. They were not read because they belong to other branches of an external repo and are labeled experimental.
- **GENUINE-GAP (as far as searched)**: No peer-reviewed field study of data corruption or truncation rates specifically on iSCSI, NVMe/TCP or NBD read paths was found. Jiang et al. covers FC back-end interconnects. Bairavasundaram explicitly excludes transport-reported corruptions.
- **GENUINE-GAP**: Neither NBD proto.md nor the NVMe/TCP transport spec defines read atomicity against a concurrent write on another connection or path. NBD MULTI_CONN only addresses flush/FUA visibility.
- **GENUINE-GAP**: The NBD spec defines no resume/reconnect semantics [F11]. Behaviour after a hard disconnect mid-read is left to clients.
