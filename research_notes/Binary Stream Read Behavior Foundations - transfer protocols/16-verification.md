# Verification notes

Method: 3 independent verifiers per track (lenses: fidelity, overreach, currency), each re-reading the cited full text and trying to refute every claim of the track. A claim is KILLED on >=2 refutes, CONTESTED on 1 refute, VERIFIED on >=2 supports with no refute.

Result: Counter({'VERIFIED': 64, 'CONTESTED': 2})

Per-claim verdicts and all verifier qualifications:

## 13-C1 - VERIFIED (3S/0R/0U)

In FTP stream mode with file structure, end of file is signalled only by the sender closing the data connection, and every byte is data; there is no in-band EOF marker.


## 13-C2 - VERIFIED (3S/0R/0U)

FTP block mode defines a descriptor flag that marks a block as 'suspected errors', so data can be delivered while flagged as unreliable. It sits alongside the EOF, EOR and restart-marker flags.


## 13-C3 - VERIFIED (3S/0R/0U)

FTP has no mechanism of its own to detect lost or corrupted bits; it delegates this to TCP. Its restart procedure is defined only for block and compressed modes.

- [overreach] Restart being 'defined only for the block and compressed modes' holds for base RFC 959 only. RFC 3659 later adds STREAM-mode restart via REST plus an octet offset. The claim should be dated to RFC 959.

## 13-C4 - VERIFIED (3S/0R/0U)

FTP reply codes formally separate transient negative completions (4yz, the request may be repeated unchanged) from permanent ones (5yz, repeating it is discouraged). The RFC itself concedes that 'transient' is hard to define.


## 13-C5 - VERIFIED (3S/0R/0U)

The FTP SIZE command must return the exact number of octets that would be transmitted, and that number depends on the current TYPE, MODE and STRU. It is not necessarily the stored file size.


## 13-C6 - VERIFIED (3S/0R/0U)

RFC 3659 defines restart in STREAM mode as an octet offset. Such an offset is an unambiguous restart point only in STREAM mode, because in other modes the same file can be sent as different octet sequences.


## 13-C7 - VERIFIED (3S/0R/0U)

FTP offers no in-transfer detection of source changes. Before resuming a retrieval, RFC 3659 only recommends a heuristic comparison of modification times (MDTM or the MLST 'modify' fact).

- [overreach] RFC 3659 says the user-FTP 'can use' MDTM or the 'modify' fact, and that clients 'should usually' record the time before the initial RETR. That is permissive wording, not a formal recommendation. The heuristic covers STOR too (comparing against the partial file's MDTM). 'No in-transfer detection' is an inference, not something the RFC states.

## 13-C8 - VERIFIED (3S/0R/0U)

With FTPS protection level Clear (PROT C), the data connection has no integrity protection at all. RFC 4217 contains no normative text on detecting truncation of a protected data connection; it only illustrates TLSshutdown before close.


## 13-C9 - VERIFIED (3S/0R/0U)

In SFTP version 3, a READ returns as many bytes as the server can read up to len. EOF or an error before any data yields SSH_FXP_STATUS. Full reads are 'guaranteed' only for normal disk files; device files may return fewer bytes.


## 13-C10 - VERIFIED (3S/0R/0U)

SFTP places no restriction on the order in which responses to outstanding requests are delivered; replies are matched by request id. Overlapping read/write requests on the same file must behave as if they were serialized.


## 13-C11 - VERIFIED (3S/0R/0U)

In SFTP v3, SSH_FX_CONNECTION_LOST and SSH_FX_NO_CONNECTION are client-local pseudo-errors that servers must not send. SSH_FX_EOF signals that no more data is available, and SSH_FX_FAILURE is a generic catch-all. No transient/permanent class distinction exists.


## 13-C12 - VERIFIED (3S/0R/0U)

SFTP version 6 explicitly allows short READ replies (at EOF, on error, or when server buffers are limited). It adds an optional end-of-file flag so clients need not spend a round trip telling EOF apart from other short-read causes. This is a version difference from v3.

- [overreach] v3 already let reads return fewer bytes for files that are not normal disk files, such as device files. The version difference is that v6 allows short replies more broadly (EOF, error, limited server buffers), adds the optional end-of-file flag and adds the max-read-size guarantee. Short reads themselves are not new.

## 13-C13 - VERIFIED (3S/0R/0U)

OpenSSH implements only SFTP v3 (draft -02) plus extensions. Its documentation states that servers usually answer reads larger than max-read-length with shorter DATA packets, and may sever the connection if limits are exceeded.


## 13-C14 - CONTESTED (2S/1R/0U)

The OpenSSH sftp client re-requests the remainder after a short DATA reply, treats any non-EOF status as a read error, and truncates the local file to the highest contiguous offset on interrupt or error. It refuses to resume a download if the server reordered replies.

- REFUTE [overreach] sftp-client.c sftp_download, lines ~1855-1864: `if (reordered && resume_flag && (read_error || write_error || interrupted)) { error(...); }` is followed directly by `ftruncate(local_fd, highwater)`. It is a diagnostic after a failure, not a refusal gate.
- [fidelity] The client does not actively refuse a resume. When resume_flag is set, an error or interrupt occurred, and reordering was seen, it only logs error("Unable to resume download ... server reordered requests"). It still truncates at highwater, and does so unconditionally with inplace_flag.
- [overreach] The re-request, non-EOF-is-error, contiguous truncation, 'more data than asked' fatal and second zero-length fatal behaviours are all correct. But the client does not refuse to resume. When a transfer with resume_flag set fails or is interrupted after replies arrived out of order, it only logs 'Unable to resume download ... server reordered requests' and still truncates to highwater. No code path blocks a later resume. Truncation also happens unconditionally with the in-place flag.
- [currency] The 'server reordered requests' error is printed only when the transfer was reordered, resume is on, and an error or interrupt occurred. It warns that the partial file cannot be resumed reliably; the client still truncates to highwater rather than refusing a resume up front. Truncation also happens unconditionally when writing in place (inplace_flag).

## 13-C15 - VERIFIED (3S/0R/0U)

The legacy scp protocol let a hostile server send filenames that did not match the client's request (CVE-2019-6111). OpenSSH describes the protocol as outdated and not readily fixable; the client-side mitigation can falsely reject files because client and server wildcard expansion may differ.


## 13-C16 - VERIFIED (3S/0R/0U)

TFTP signals end of transfer by a DATA packet shorter than the block size. A sender that times out after the final DATA packet cannot tell whether the transfer succeeded.

- [overreach] RFC 1350 fixes the block size at 512, so its rule is 'a data packet of less than 512 bytes'. The no-retransmission point for ERROR is in both §2 and §7.

## 13-C17 - VERIFIED (3S/0R/0U)

With the TFTP blksize option, a file whose size is an exact multiple of the block size ends with an extra zero-length DATA packet. The final-packet rule is unchanged: data shorter than the negotiated blocksize ends the transfer.


## 13-C18 - VERIFIED (3S/0R/0U)

The TFTP 'Sorcerer's Apprentice Syndrome' (retransmitting on duplicate ACKs) does not corrupt the file but can cause excessive duplication and time-outs. RFC 1123 requires the fix.

- [overreach] RFC 1123 says the bug 'may cause' excessive retransmission, which 'may cause' a timeout. It is a possibility, not a certainty.

## 13-C19 - VERIFIED (3S/0R/0U)

A 9P Rread may return fewer bytes than requested. A read at or beyond the file size returns a count of zero. Atomic transfer size is bounded only by the iounit reported at open.

- [fidelity] The source says iounit, 'if non-zero, reports the maximum size that is guaranteed to be transferred atomically'. That is a guarantee of atomicity up to iounit, not 'bounded only by' it, and iounit may be zero. I did not check the intro(5) items in the applicability note.
- [overreach] read(5) does not say atomic transfer is 'bounded only by' iounit. It says iounit, if non-zero, reports the maximum size that is guaranteed to be transferred atomically. That is a guarantee, and when iounit is 0 none is given here. Message size limits can also split one read call into several messages. Directory reads follow different rules: whole entries only, sequential offsets.
- [currency] read(5) says the iounit from open(5) 'if non-zero, reports the maximum size that is guaranteed to be transferred atomically'. It is a guarantee that applies only when the value is non-zero, so 'bounded only by the iounit' overstates it; implementations may also split a read across several messages because of message-size limits.

## 13-C20 - VERIFIED (3S/0R/0U)

In BitTorrent, each fixed-size piece (the last may be shorter) is verified against a SHA1 hash from the metainfo. A peer announces a piece with 'have' only after it has checked the hash.


## 13-C21 - VERIFIED (3S/0R/0U)

rsync normally verifies each transferred file with a whole-file checksum computed during transfer, unless checksum-choice=none is forced. However, --append does not verify existing receiver content, and before rsync 3.0.0 --append behaved like --append-verify (a version difference).


## 13-C22 - VERIFIED (3S/0R/0U)

In four years of Globus logs, 27,251 of 3,312,102 transfers with integrity checking had at least one checksum error (about 1 in 121), and at least one checksum failure occurred per 1.26 TB. Changes to files during transfer cannot be distinguished from corruption.


## 13-C23 - VERIFIED (3S/0R/0U)

End-to-end file-transfer checksum verification that rereads files usually hits the page cache. It therefore fails to detect injected undetected disk read and write errors for files smaller than memory; RIVA fixes this by invalidating cached pages.

- [fidelity] The injected faults are undetected write errors (UWEs) only. The abstract says 'robustness ... against undetected disk write errors', and §5.2.2 / Fig. 10 inject UWEs. Read errors were not injected. Also, the §2.3 motivating experiment monitors page misses and does not inject faults; the fault injection is in §5.2.2.
- [overreach] The injected faults are only undetected write errors (UWEs, in the 'extreme-injection' test). Read-error (URE) cases are argued analytically, not injected. The 273-file / 274 GB experiment measured page misses (cache behaviour), not detection. The abstract says existing methods miss injected errors 'for almost all file sizes', and the paper concedes RIVA may fail if several I/O operations are corrupted. RIVA invalidates pages with munmap, checking with mincore.
- [currency] The fault-injection experiments mainly inject undetected write errors (the abstract says 'robustness... against undetected disk write errors'). The 273-file motivating experiment measures page misses and injects no faults. The vulnerability to read errors is argued, not shown by injection, so 'injected undetected disk read and write errors' overstates what was tested. The source is the NSF PAR accepted manuscript.

## 14-C1 - VERIFIED (3S/0R/0U)

Under NBD simple replies, a read cannot report partial success. If an error is detected after a zero-error reply header has been sent, the server must hard-disconnect and send no more data.

- [overreach] Minor: if the error is known before the header is sent, the server SHOULD set the error code and MAY disconnect; if it does not disconnect it MUST NOT send any payload. Only an error found after a zero-error header forces an immediate hard disconnect.
- [currency] The applicability note mislabels the document. proto.md belongs to the NetworkBlockDevice/nbd project; it is not 'a project document of the Linux kernel'. Also, the simple-reply rule applies only when neither structured replies nor the newer experimental NBD_OPT_EXTENDED_HEADERS have been negotiated.

## 14-C2 - VERIFIED (3S/0R/0U)

With NBD structured replies, read content chunks may arrive in any order and must be reassembled by the client. Further content chunks may follow an error chunk. When no error occurs, the server must cover the whole requested range.

- [overreach] Two conditions are left out. If the client sets NBD_CMD_FLAG_DF, the server MUST send at most one content chunk, so there is no reordering. Chunks also MUST NOT overlap earlier content or error chunks, and MUST NOT fall outside the requested range. Sending content chunks after an error chunk is a MAY, not something to expect.

## 14-C3 - VERIFIED (3S/0R/0U)

NBD distinguishes two read-error semantics. NBD_REPLY_TYPE_ERROR invalidates all data chunks of the reply, whether sent before or after it. NBD_REPLY_TYPE_ERROR_OFFSET localises the error, so partial success can be determined.

- [fidelity] The quote is in the NBD_CMD_READ section, not the 'Structured reply types' definitions, though NBD_REPLY_TYPE_ERROR's own definition (around line 1901) also says 'the client MAY NOT make any assumptions about partial success'. Partial success can be determined only when every error carries an offset; the spec says a server SHOULD NOT mix the two error types.
- [overreach] Partial success can be worked out only conditionally. The text reads 'As long as all errors are accompanied by offsets, the client MAY assume' that data chunks with no later error offset are valid, and that uncovered portions are invalid. The server SHOULD NOT mix offset errors with a generic error. Also, any error chunk makes the reply unsuccessful overall.

## 14-C4 - VERIFIED (3S/0R/0U)

NBD replies may be returned out of request order, and chunks of different requests may be interleaved. Correlation is by a client-chosen opaque cookie.

- [overreach] The spec adds that 'there may be constraints that prevent arbitrary reordering of structured reply chunks within a given reply'. Clients SHOULD (not MUST) use distinct cookies for pending requests.

## 14-C5 - VERIFIED (3S/0R/0U)

NBD has no end-of-file or short-read outcome for READ. A read extending beyond the export size SHOULD fail with NBD_EINVAL. The error values are a small errno-derived set without a transient/permanent classification.

- [fidelity] The quote continues '...or if a read or write request is not aligned to advertised minimum block sizes', so EINVAL also covers misalignment.
- [overreach] 'No EOF/short-read outcome' is an inference from the spec saying nothing on it; label it as inference. The spec does attach handling hints to some codes: for NBD_EOVERFLOW 'a client should be prepared to retry with smaller requests', and on NBD_ESHUTDOWN the client MUST initiate a disconnect. That is retry guidance, even though there is no formal classification.
- [currency] 'No EOF/short-read outcome' and 'no transient/permanent classification' are inferences from what the spec omits; the spec states neither. NBD_ESHUTDOWN and the hint to retry after NBD_EOVERFLOW are informal retry signals.

## 14-C6 - VERIFIED (3S/0R/0U)

An NBD BLOCK_STATUS reply may legitimately cover less of the requested range than asked, as long as at least one extent is returned.

- [overreach] The claim leaves out the stated condition: the MAY applies 'if looking up the information would be too resource-intensive for the server'. Servers SHOULD NOT send more than 2^20 extents per chunk 'even if this requires that the server truncate the response'. NBD_CMD_FLAG_REQ_ONE also limits the reply to one extent.

## 14-C7 - VERIFIED (3S/0R/0U)

In NVMe/TCP, the C2HData PDUs carrying read data must have strictly sequential offsets from 0 within a command. A non-contiguous PDU is a fatal transport error. PDUs of different commands may interleave.

- [currency] Rev 1.1 is superseded. Rev 1.2 (Aug 2025) and Rev 1.3 (2026-07-31, retitled 'NVMe over TCP Transport Specification') followed; Rev 1.3 keeps the same §3.3.2.1 text.

## 14-C8 - VERIFIED (3S/0R/0U)

In NVMe/TCP, a header digest error is always fatal and terminates the connection. A data digest error in read data is non-fatal, but the host must fail the command even if the controller returned success.

- [overreach] 'Fail the command with a non-fatal transport error' means completing it with Transient Transport Error status (per §3.5). Termination is through a TermReq exchange, with a fallback 30-second timeout or a TCP reset.
- [currency] Current revision is NVMe over TCP Rev 1.3 (2026-07-31); the text is unchanged.

## 14-C9 - VERIFIED (3S/0R/0U)

NVMe defines Transient Transport Error as likely to succeed on retry on the same controller. After four or more such failures the command should be treated as a persistent transport error.

- [overreach] The four-or-more rule is a 'should' recommendation, not a requirement.
- [currency] Base 2.1 is superseded: Base 2.2 (2025-03), 2.3 (2025-08) and 2.4 (2026-07-31) followed. The wording is unchanged in 2.4.

## 14-C10 - VERIFIED (3S/0R/0U)

In NVMe, the DNR bit marks a command as expected to fail on resubmission to any controller in the subsystem. The CRD field selects a minimum retry delay, which is advisory: retrying earlier is not an error.

- [overreach] CRD is meaningful only when DNR is cleared and the host set ACRE to 1h; otherwise the field is reserved. CRD 00b means zero delay.
- [currency] In Base 2.4 the Status Field figure is Figure 101, not Figure 100. Base 2.1 is superseded by 2.4 (2026-07-31), with the same text.

## 14-C11 - VERIFIED (3S/0R/0U)

NVMe Path Related Status errors should be retried on a different path if one is available. ANA Inaccessible and Persistent Loss mean the command should not be resubmitted to the same controller. ANA Transition means retry after the transition completes.

- [fidelity] Figure 107's 00h Internal Path Error is an exception: its retry follows the DNR bit.
- [overreach] The retry-on-another-path rule is qualified by 'unless otherwise specified'. Internal Path Error (00h) instead defers to the DNR bit. All of these are 'should' recommendations.
- [currency] In Base 2.4 this is Figure 108. Also, 00h Internal Path Error defers to the DNR bit, so 'unless otherwise specified' carries weight.

## 14-C12 - VERIFIED (3S/0R/0U)

After communication loss, NVMe classifies a Read as idempotent and an Unrestricted Retry command. Such a command may be retried immediately without determining whether the original is still being processed. Writes are Delayed Retry commands.

- [fidelity] A Read counts as Unrestricted Retry only if the CCC, NIC, NCC and LBCC effects bits are all cleared. The spec gives Read and Write as examples ('e.g.'), not an absolute classification, and Write is Delayed Retry 'except as described in section 9.6.3.2.2' (when it can affect other hosts).
- [overreach] This is a categorisation with conditions, not a fixed property of Read. A command counts as Unrestricted Retry only if it is idempotent, changes nothing beyond ancillary state, and has CCC/NIC/NCC/LBCC cleared in the Commands Supported and Effects log. Writes are Delayed Retry 'except as described in section 9.6.3.2.2': a write that can affect other hosts becomes State-Dependent Retry. Retry is a host 'may', and the procedures are 'strongly recommended', not mandated.
- [currency] Fine points: a Read is Unrestricted only if CCC/NIC/NCC/LBCC are all cleared in its Commands Supported and Effects entry. A Write is Delayed Retry 'except as described in 9.6.3.2.2', i.e. not when it can affect other hosts. Also note that writes are idempotent too. Base 2.1 is superseded by 2.4.

## 14-C13 - VERIFIED (3S/0R/0U)

iSCSI error recovery is a negotiated three-level hierarchy (ERL 0 session recovery, 1 digest failure recovery, 2 connection recovery). Only level 0 is mandatory, and the session operates at the lower of the two offered values.

- [fidelity] The RFC labels level 0 'Session failure recovery' rather than 'session recovery'; this is minor.
- [overreach] Level 1 'digest failure recovery' covers both within-connection and within-command recovery classes. Each level is a superset of the levels below it.
- [currency] Level 1 is named 'Digest failure recovery' (within-connection plus within-command classes). The hierarchy diagram calls level 0 'Session failure recovery'; the table calls it 'Session recovery class'.

## 14-C14 - VERIFIED (3S/0R/0U)

An iSCSI initiator receiving a Data-In PDU with a payload digest error must discard it and either request it through SNACK or abort the task. If the SNACK is rejected after status was sent, the command completes with CHECK CONDITION 'Protocol Service CRC error'.

- [fidelity] The CHECK CONDITION is signalled internally by the initiator, which discards the target's status; the target does not send it in this case.
- [overreach] In case a.2 the initiator must wait for the status and discard it, signalling the CHECK CONDITION internally. If status was not yet sent, the target terminates the command with 'SNACK rejected' instead. Either party may also escalate to session recovery.
- [currency] It is the initiator that internally signals the CHECK CONDITION 'Protocol Service CRC error' completion (the target takes no further action). If the SNACK is rejected before status is sent, the target terminates with 'SNACK rejected'. The task can also be escalated to session recovery.

## 14-C15 - VERIFIED (3S/0R/0U)

iSCSI digests default to None. When enabled, they are CRC32C error-detection checks that cover the whole path including routers, switches and proxies, beyond link-layer checks.

- [overreach] 'When enabled, they are CRC32C' is too broad. CRC32C is the only standard algorithm that MUST be implemented, but 'Private or public extension algorithms MAY also be negotiated for digests'. The digests are non-cryptographic.

## 14-C16 - VERIFIED (3S/0R/0U)

With iSER (iSCSI over RDMA), iSCSI digests must be None, integrity is delegated to the RDMA-capable protocol, read data travels as RDMA Writes, and SNACK must not be used. The stated reason is that no digest or sequence errors occur.

- [overreach] The stated reason is limited to the iSCSI layer in iSER-assisted mode: no iSCSI digest errors because digests are None, and no sequence errors because RCaP delivers in order. Integrity errors are still possible; RCaP is responsible for them. RFC 7145 otherwise says the iSCSI error recovery hierarchy 'is fully supported'.

## 14-C17 - VERIFIED (3S/0R/0U)

In a field study of about 39,000 storage systems, physical interconnect failures made up 27-68% of storage subsystem failures. Systems with redundant interconnects (multipathing) had 30-40% lower subsystem AFR.

- [overreach] In this paper 'physical interconnects' explicitly include shelf enclosures (backplanes, power, cooling, cables, HBAs), not just links. 27-68% is a range across system classes. The applicability caveat (NetApp FC back-end, not host-to-array networks) is correct and important.
- [currency] The paper's 'physical interconnects' explicitly include shelf enclosures (backplanes, power), not only cables and HBAs.

## 14-C18 - VERIFIED (3S/0R/0U)

Internet traces show that the TCP checksum fails to detect errors in roughly 1 in 16 million to 10 billion packets. The authors recommend application-level checksums for some applications.

- [overreach] The 1-in-16M-to-10B figure is the authors' estimate from analysis of the errors observed in the traces, not an undetected-error rate measured directly. The traces directly show checksum failures (detected errors) of 1 in 1,100 to 1 in 32,000 packets. 'Recommend' is slightly strong; the paper says 'strongly suggests'.

## 14-C19 - VERIFIED (3S/0R/0U)

The Linux NVMe host driver fails a request without retry if DNR is set or the retry count reaches nvme_max_retries (default 5). It fails over multipath requests with path errors to another path, and requeues I/O rather than failing it while any path is still resetting or connecting.

- [fidelity] The requeue-while-connecting behaviour is conditional. CONNECTING counts as available only if NVME_NSHEAD_FAIL_ON_CTRL_LOSS is not set, and controllers whose failfast timer has expired are skipped. Requests flagged no-retry (blk_noretry_request) also fail without retry.
- [overreach] The CONNECTING case counts only when NVME_NSHEAD_FAIL_ON_CTRL_LOSS is not set. Controllers with NVME_CTRL_FAILFAST_EXPIRED are skipped. A LIVE controller in ANA change state also counts, and delayed_removal_secs can keep I/O requeued. blk_noretry_request (failfast) requests are also failed without retry. All of this is at one source revision.
- [currency] In current master the requeue rule has conditions. A CONNECTING path counts only if NVME_NSHEAD_FAIL_ON_CTRL_LOSS is not set. FAILFAST_EXPIRED controllers are skipped. A LIVE controller in an ANA-change state also counts. With delayed_removal_secs (queue_if_no_path), I/O is requeued even when no path is resetting or connecting. Failover is also triggered when the queue is dying, and the DNR and retry-count checks come before the failover decision.

## 14-C20 - VERIFIED (3S/0R/0U)

A Ceph librados read returns the number of bytes read on success, a byte-count convention that admits short results, and it reads from the snapshot selected on the I/O context.

- [fidelity] The doc does not say that short results can occur; 'admits short results' is an inference from the byte-count return value. rados_aio_read() itself returns 0 on success, and the byte count comes from the completion. The snapshot applies only if one was set with rados_ioctx_snap_set_read().
- [overreach] 'Admits short results' is inference from the byte-count return value; the docs do not state when fewer than len bytes come back. rados_aio_read's own return value is 0 on success; the byte count is the completion's return value. The snapshot applies only if one was set; LIBRADOS_SNAP_HEAD means normal reads.
- [currency] 'Admits short results' is an inference from the byte-count return value; the docs do not explicitly describe short reads, for example a read past the object end.

## 15-C1 - VERIFIED (3S/0R/0U)

OpenDAL ErrorKind defines Conflict as a resource-state conflict that explicitly does not indicate retry safety.

- [overreach] Conflict is a recent addition (RFC-8145, 2026). Calling it part of a long-standing taxonomy would overstate it.

## 15-C2 - VERIFIED (3S/0R/0U)

OpenDAL ErrorStatus Permanent forbids retry and is the default status of a new Error.

- [fidelity] ErrorStatus is a private enum (no `pub`), so callers do not see it directly as a type.

## 15-C3 - VERIFIED (3S/0R/0U)

OpenDAL defines a Persistent status for errors that were temporary but survived retries.

- [overreach] Persistent is a SHOULD NOT. It is not a prohibition the way Permanent's MUST never is.

## 15-C4 - VERIFIED (3S/0R/0U)

RFC-8145 states that error kind and retry status are independent classification axes.

- [overreach] The RFC says this while defining Conflict/ConditionNotMatch. It is an RFC design statement, not a general spec for all ErrorKinds, though ErrorStatus is a separate field in the code.

## 15-C5 - VERIFIED (3S/0R/0U)

RFC-8145 requires services to classify by native error code and operation context before falling back to HTTP status.

- [fidelity] The RFC states this as a description ('Services classify...'), not with RFC-2119 'MUST' wording, so 'requires' is a slight overstatement.
- [overreach] The RFC states this as a declarative rule plus an 'initial mappings' table. It uses no MUST, so 'requires' is slightly strong.

## 15-C6 - VERIFIED (3S/0R/0U)

RFC-8145 defines set_temporary as safe replay of the same method at the receiving layer, not eventual success of a broader workflow.


## 15-C7 - VERIFIED (3S/0R/0U)

OpenDAL's service-implementation guide mandates returning structured errors with the correct ErrorKind.

- [overreach] This is a contributor guide (rustdoc). It does not define what 'correct' means for each backend and nothing enforces it in code.

## 15-C8 - VERIFIED (3S/0R/0U)

OpenDAL's S3 service maps NoSuchBucket (HTTP 404) to ConfigInvalid, not NotFound, via error-code-first classification.

- [overreach] Precisely: the status is mapped first, then a recognised native error code overrides it. This is S3-service-specific code, not a general OpenDAL property.

## 15-C9 - VERIFIED (3S/0R/0U)

OpenDAL maps any unrecognised std::io error kind to Unexpected marked temporary (retryable).

- [fidelity] UnexpectedEof is not caught by the wildcard. Line 38 maps Interrupted, UnexpectedEof, TimedOut and WouldBlock to (Unexpected, true) by name, so the result is the same as the wildcard.
- [overreach] UnexpectedEof is listed explicitly alongside Interrupted/TimedOut/WouldBlock rather than falling through '_', but the result is the same: Unexpected + temporary.

## 15-C10 - VERIFIED (3S/0R/0U)

Hadoop's FSDataInputStream spec permits read(buffer) to return fewer bytes than requested, down to one, but requires blocking until at least one byte.

- [overreach] The postconditions return -1 at EOF and 0 when length==0, so the at-least-1 range applies only when data is available.

## 15-C11 - VERIFIED (3S/0R/0U)

Hadoop's spec leaves destination buffer contents undefined after a failed positioned read.


## 15-C12 - VERIFIED (3S/0R/0U)

Hadoop's spec allows named exceptions to be raised as subclasses but never superclasses.


## 15-C13 - VERIFIED (3S/0R/0U)

Hadoop's spec states no retryability classification; it only permits retry under happens-before constraints.

- [fidelity] Treat the 'no retryability classification' half as an absence finding for introduction.md only, not for the whole spec.
- [overreach] 'Only permits retry under happens-before constraints' overreaches for the spec as a whole. Other pages set operation-specific retry rules: abortable.md says 'The stream MUST retry any remote calls needed to force the abort outcome' and 'SHOULD NOT retry cleanup operations'; outputstream.md says close() 'MUST NOT retry the write'; bulkdelete.md notes weak idempotency on retries. So the spec has per-operation retry obligations but no retry axis on errors.

## 15-C14 - VERIFIED (3S/0R/0U)

Hadoop's S3A connector maps HTTP 416 to RangeNotSatisfiableEOFException and its retry policy marks that class fail.

- [overreach] This is behaviour of the S3A connector on trunk only, not of the Hadoop FileSystem spec.

## 15-C15 - VERIFIED (3S/0R/0U)

The Hadoop FileSystem specification describes itself as incomplete, including on failure modes.

- [overreach] On failure modes the text is softer than the claim: it says covered operations 'may' have minor issues with failure modes. It does not say failure modes are systematically missing.

## 15-C16 - VERIFIED (3S/0R/0U)

Arrow object_store's Error enum has a Generic variant defined as the fallback when no other variant matches.

- [overreach] I checked main and did not confirm the version/commit pin (0.14.2, c216edef).

## 15-C17 - VERIFIED (3S/0R/0U)

object_store's generic HTTP mapping turns HTTP 409 Conflict into Error::AlreadyExists.

- [fidelity] retry.rs also has an opt-in retry_on_conflict flag (line 431) that retries 409 at the transport level.
- [overreach] This is the shared client fallback. Individual store implementations may map errors before it runs. Separately, the retry loop can retry 409 when retry_on_conflict is set.

## 15-C18 - VERIFIED (3S/0R/0U)

object_store's HttpErrorKind documents retry behaviour per variant, retrying Timeout only for idempotent requests.

- [fidelity] Interrupted also says it is retried only if the request is idempotent.
- [overreach] Interrupted shares the idempotent-only rule with Timeout, so Timeout is not the only such variant. This axis is HTTP transport level and separate from crate::Error.

## 15-C19 - VERIFIED (3S/0R/0U)

object_store states it mirrors object store APIs with stateless operations rather than cursor-based file interfaces.


## 15-C20 - CONTESTED (2S/1R/0U)

fsspec defines only two custom exception classes, neither a storage outcome taxonomy.

- REFUTE [overreach] Only fsspec/exceptions.py defines exactly two classes (BlocksizeMismatchError(ValueError), FSTimeoutError(asyncio.TimeoutError)). A shallow clone at 12c823b shows the wider package defines more custom exceptions: ReferenceNotReachable (implementations/reference.py:35), DatabricksException (implementations/dbfs.py:13), TransferDone (implementations/ftp.py:348), FSSpecCoroutineCancel (asyn.py:1186).
- [overreach] fsspec's exceptions.py defines only two custom exception classes. Other custom exceptions in the package are local to modules or implementations, and none of them forms a storage outcome taxonomy.
- [currency] Narrow the claim: fsspec/exceptions.py defines only two custom exceptions, but the package defines others elsewhere (ReferenceNotReachable in implementations/reference.py, DatabricksException in implementations/dbfs.py, TransferDone in implementations/ftp.py, FSSpecCoroutineCancel in asyn.py). Each is local to one implementation and none forms a taxonomy, so the NOT FOUND conclusion stands.

## 15-C21 - VERIFIED (3S/0R/0U)

fsspec's retryable-status set for HTTP is local to the HTTP implementation.

- [fidelity] The set is a default that callers can override with the HTTPFileSystem retry_statuses parameter (line 210).
- [overreach] Callers can override it via the retry_statuses parameter (line 210).

## 15-C22 - VERIFIED (3S/0R/0U)

Go CDK blob drivers must report a gcerrors.ErrorCode for errors they return.

- [fidelity] The doc uses 'should return', not 'must'. Strictly, the obligation is that drivers implement the ErrorCode method, which is required by the interface.
- [overreach] Implementing ErrorCode is mandatory because it is an interface method, but the doc wording is 'should return', and the doc does not dictate which code to use for each error.

## 15-C23 - VERIFIED (3S/0R/0U)

rclone's fserrors defines an optional Retrier interface signalling high-level retry.

- [overreach] Retrier is one of three optional retry-hint interfaces (with NoRetrier and NoLowLevelRetrier). It is not an outcome taxonomy.
