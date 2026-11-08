# Track 13: File-transfer and remote file-access protocols (READ behaviour)

Scope: what a reader observes when a binary stream is retrieved through FTP (and its extensions), FTPS, SFTP, SCP, TFTP, WebDAV, rsync, 9P and BitTorrent; plus two peer-reviewed empirical studies of transfer integrity.
Remote *block* protocols (NBD, iSCSI, NVMe-oF) are not covered here. NBD proto.md was downloaded but not analysed; leave it to the block-protocol track (COVERAGE-GAP).

Download dir (untrusted copies, not in repo): `/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl2/file-transfer-protocols/`

## 1. Sources and access status

| # | Source | Kind | Access |
|---|---|---|---|
| S1 | RFC 959, FTP (Postel & Reynolds, 1985), STD 9 | normative | full text (rfc-editor.org .txt) |
| S2 | RFC 1123 §4.1.3.4 (FTP restart correction) and §4.2.3.1 (TFTP Sorcerer's Apprentice) | normative | full text |
| S3 | RFC 3659, Extensions to FTP (Hethmon, 2007), Standards Track | normative | full text |
| S4 | RFC 4217, Securing FTP with TLS (2005), Standards Track | normative | full text |
| S5 | draft-ietf-secsh-filexfer-02 (Ylonen & Lehtinen, Oct 2001), SFTP protocol version 3 | **expired Internet-Draft, never an RFC**; de-facto basis of OpenSSH | full text |
| S6 | draft-ietf-secsh-filexfer-13 (Galbraith & Saarenmaa, July 2006), SFTP version 6 | **expired Internet-Draft** | full text |
| S7 | draft-ietf-secsh-filexfer-extensions-00 (Jan 2006), check-file | **expired Internet-Draft** | full text (only §3 skimmed) |
| S8 | OpenSSH `PROTOCOL` file (openssh-portable master) | implementation doc | full text |
| S9 | OpenSSH `sftp-server.c`, `sftp-client.c` (master) | implementation source (primary engineering evidence) | full text of read paths (process_read; sftp_download loop) |
| S10 | OpenSSH 8.0 release notes (CVE-2019-6111) | implementation doc | full text |
| S11 | OpenSSH 8.3 release notes (scp desync) | implementation doc | full text of security section |
| S12 | OpenSSH 9.0 release notes (scp -> SFTP default) | implementation doc | full text |
| S13 | RFC 1350, TFTP rev. 2 (1992), STD 33 | normative | full text |
| S14 | RFC 2347 (option extension), RFC 2348 (blksize), RFC 2349 (tsize), RFC 7440 (windowsize, Standards Track 2015) | normative | full text |
| S15 | RFC 4918, WebDAV (2007) | normative | full text; only §6.6, §7, §8.6 used |
| S16 | Tridgell & Mackerras, "The rsync algorithm" (TR-CS-96-05), HTML edition rsync.samba.org/tech_report (pages dated 1998-11-09) | technical report (foundational algorithm) | full text of nodes 1-4 |
| S17 | rsync(1) man page (download.samba.org, current) | implementation doc | full text (grep + sections read) |
| S18 | BEP 3, The BitTorrent Protocol Specification (Cohen), Status: Final, Type: Standard | community "standard" (BitTorrent.org BEP process, not IETF) | full text |
| S19 | Plan 9 manual read(5), intro(5) (9p.io) | implementation/protocol doc (9P2000) | full text |
| S20 | Liu, Kettimuthu, Foster, Rao, "Cross-geography Scientific Data Transferring Trends and Behavior", HPDC '18 | peer-reviewed empirical | full text (author PDF) |
| S21 | Charyyev & Arslan, "RIVA: Robust Integrity Verification Algorithm for High-Speed File Transfers" (NSF PAR accepted manuscript; IEEE venue not stated in the copy read) | peer-reviewed (venue unconfirmed) empirical/fault-injection | full text |
| S22 | Kettimuthu et al. arXiv 2009.03190 | secondary (only used as the lead to S20) | 2-page PDF fetched; not used for claims |
| - | Tridgell PhD thesis (samba.org/~tridge/phd_thesis.pdf) | thesis | downloaded, not read (no claims) |
| - | NBD proto.md | implementation doc | downloaded, not read (out of track) |
| - | AFS/Coda papers | peer-reviewed | not searched (COVERAGE-GAP) |

No source was blocked. No AI summaries used as evidence; search-engine summaries were used only as leads.

## 2. Findings with verbatim quotes

### FTP (RFC 959, RFC 1123, RFC 3659, RFC 4217)

- **End of data in stream mode = connection close** (S1 §3.4.1): "If the structure is a file structure, the EOF is indicated by the sending host closing the data connection and all bytes are data bytes." Record structure in stream mode uses escape-coded EOR/EOF (0xFF then 1/2/3). §3.4: "All data transfers must be completed with an end-of-file (EOF) which may be explicitly stated or implied by the closing of the data connection." -> In stream/file structure (the common binary case) a premature close is not distinguishable from EOF on the data connection itself; the control-channel reply (226 vs 426/451) is the only discriminator. *(inference from S1 §3.4.1 and §4.2)*
- **Block mode descriptor codes** (S1 §3.4.2): 128 EOR, 64 EOF, 32 "Suspected errors in data block", 16 restart marker. The suspect-data code "is NOT intended for error control within FTP. It is motivated by the desire of sites exchanging certain types of data (e.g., seismic or weather data) to send and receive all the data despite local errors (such as "magnetic tape read errors"), but to indicate in the transmission that certain portions are suspect". A defined "data delivered but flagged unreliable" outcome.
- **No in-protocol integrity** (S1 §3.5): "There is no provision for detecting bits lost or scrambled in data transfer; this level of error control is handled by the TCP." Restart "is defined only for the block and compressed modes of data transfer"; marker information "has meaning only to the sender". RFC 1123 §4.1.3.4 corrects the 110 reply to "110 MARK ssss = rrrr".
- **IMAGE type and padding** (S1 §3.1.1.3): the receiver "must store the data as contiguous bits"; storage "might necessitate the padding of the file ... This padding, which must be all zeros, may occur only at the end of the file ... and there must be a way of identifying the padding bits so that they may be stripped off if the file is retrieved." -> Retrieved IMAGE bytes may differ in length from the original by trailing zero padding unless the server strips it.
- **ASCII transformation** (S1 §3.4): "the sending host will translate its internal end of line or end of record denotation into the representation prescribed ... and the receiving host will perform the inverse translation"; identical systems "might wish to use a binary representation and stream mode".
- **Reply classes** (S1 §4.2.1): 4yz Transient Negative: "the error condition is temporary and the action may be requested again"; RFC admits "It is difficult to assign a meaning to "transient""; rule of thumb: 4yz "if the commands can be repeated without any change in command form or in properties of the User or Server". 5yz Permanent: "The User-process is discouraged from repeating the exact request ... Even some "permanent" error conditions can be corrected". Relevant read-time codes: 426 "Connection closed; transfer aborted.", 451 "Requested action aborted: local error in processing." RETR replies 125/150 then 110, 226, 250, 425, 426, 451.
- **ABOR** (S1 §4.1.3): when a transfer is in progress "the server aborts the FTP service in progress and closes the data connection, returning a 426 reply to indicate that the service request terminated abnormally. The server then sends a 226 reply". 226 then means the ABOR succeeded, not the transfer.
- **226 race rule** (S1 §5.2): "the server sends a reply (226) after closing the data connection ... and the user-PI should wait for one of these replies before issuing a new transfer command."
- **SIZE is exact and representation-dependent** (S3 §4): "the exact number of octets (8 bit bytes) that would be transmitted over the data connection ... This value will change depending on the current STRUcture, MODE, and TYPE"; "Estimates of the file transfer size MUST NOT be returned; only precise information is acceptable."
- **REST in STREAM mode = octet offset** (S3 §5.1): "restart markers can be implied by the octet offset into the data stream ... in other modes than STREAM, the same file can be transferred using quite different octet sequences and yet be reconstructed into the one identical file. Thus an offset into the data stream in transfer modes other than STREAM would not give an unambiguous restart point." §5.3: REST value = "number of octets of the immediately-following transfer to not actually send"; misplaced REST may be errored, applied to next transfer, "or it may silently ignore the inappropriate restart attempt"; out-of-range markers are reported at the following transfer command. RETR+REST: "the client bears the responsibility of merging the retrieved data with the partially retrieved file." S3 also notes "some flaws in the description of the restart mechanism in STD 9, RFC 959" (corrected by RFC 1123).
- **Version change before resume** (S3 §3): "the user-FTP can use the MDTM command or the "modify" fact to check if the modification time of the source file is more recent ... If it is, then most likely the source file has changed, and it would be unsafe to restart"; clients should record MDTM "before the initial RETRieval" because clocks are unsynchronised. MLST "unique" fact identifies the same underlying object (§7.5.2). No in-transfer change detection exists in FTP. *(The guidance is heuristic: "most likely")*
- **FTPS** (S4 §9): PROT C: "the connection is unauthenticated and has no confidentiality or integrity"; PROT P requires TLS on the data connection. The worked examples (§12.6/12.7) show `TLSshutdown()` then `close()` then 226, but RFC 4217 contains no text that requires a receiver to treat a data-connection close without TLS closure as truncation (grep for "close_notify"/"truncat" finds nothing). The truncation-detection rule therefore comes, if at all, from TLS itself (RFC 8446 §6.1, not read in this track). GENUINE-GAP in RFC 4217.

### SFTP (drafts) and OpenSSH implementation

- **Status**: All secsh-filexfer documents are expired Internet-Drafts. S8: "OpenSSH's sftp and sftp-server implement revision 3 of the SSH filexfer protocol described in ... draft-ietf-secsh-filexfer-02.txt. Newer versions of the draft will not be supported, though some features are individually implemented as extensions". So the widely deployed SFTP behaviour rests on a de-facto implementation of an expired draft.
- **v3 READ semantics** (S5 §6.4): "the server will read as many bytes as it can from the file (up to `len'), and return them in a SSH_FXP_DATA message. If an error occurs or EOF is encountered before reading any data, the server will respond with SSH_FXP_STATUS. For normal disk files, it is guaranteed that this will read the specified number of bytes, or up to end of file. For e.g. device files this may return fewer bytes than requested." Short read for regular files thus means EOF in v3 text, but S8 (limits) and S9 contradict this in practice (see below).
- **v3 binary mode** (S5 §6.3): "the file will always be opened in "binary" mode (i.e., no translations between different character sets and newline encodings)."
- **Ordering** (S5 §6.1): requests on the same file must give results "the same as if it had sent the requests one at a time"; "There are no restrictions on the order in which responses to outstanding requests are delivered to the client, except that the server must ensure fairness". §7: request ids are used to match responses.
- **v3 status codes** (S5 §7): SSH_FX_EOF "for SSH_FX_READ it means that no more data is available in the file"; SSH_FX_FAILURE "generic catch-all"; SSH_FX_NO_CONNECTION and SSH_FX_CONNECTION_LOST are "pseudo-error[s] ... (it can only be generated locally by the client, and MUST NOT be returned by servers)". No transient/permanent split exists in v3 codes.
- **v6 (draft -13) read** (S6 §8.2.1): "The server MUST not respond with more data than is specified by the 'length' parameter. However, the server MAY respond with less data if EOF is reached, an error is encountered, or the servers internal buffers can not handle such a large request." With a non-zero `max-read-size` advertised and length <= it, "failure to return 'length' bytes indicates that EOF or an error occurred." §9.3: optional `end-of-file` bool in SSH_FXP_DATA "can help the client avoid a round trip to determine whether a short read was normal (due to EOF) or some other problem (limited server buffer for example.)" Version difference: v3 lacks this flag; v6 explicitly recognises the ambiguity.
- **v6 text mode** (S6 §8.1.1.3): SSH_FXF_TEXT_MODE converts newlines and "the offset field in the read and write functions is ignored". Byte-range locks (SSH_FXF_BLOCK_READ etc., SSH_FX_LOCK_CONFLICT, BYTE_RANGE_LOCK_*) are v6 additions.
- **check-file** (S7 §3): "check-file-handle"/"check-file-name" with offset, length, block-size; "An independent hash MUST be computed over every block in the file." (only extension draft; not implemented by OpenSSH per S8's extension list - inference from absence).
- **OpenSSH limits** (S8 §4.8): "Even if the client requests a larger size, servers will usually respond with a shorter SSH_FXP_DATA packet. Servers SHOULD set this at least to 32768." and "Clients should not attempt to exceed these limits as the server might sever the connection immediately." S9 sftp-server.c process_read: `if (len > SFTP_MAX_READ_LENGTH) ... len = SFTP_MAX_READ_LENGTH;` then a single `read(fd, buf, len)`; `ret == 0` -> SSH2_FX_EOF; otherwise data of length `ret` (so short replies occur at the server cap and whenever read(2) is short).
- **OpenSSH client short-read and reorder handling** (S9 sftp-client.c sftp_download): "Short data block, re-requesting" the remainder; fatal on "Received more data than asked for" and on a second zero-length DATA ("server sent zero data length"); tracks highest contiguous offset; on error/interrupt "Truncate at highest contiguous point to avoid holes on interrupt"; with resume: "Unable to resume download of \"%s\": server reordered requests". Any STATUS other than EOF sets read_error.
- **fsync extension** (S8 §4.6) exists; not read-relevant.

### SCP (no formal specification)

- No RFC or Internet-Draft for the scp/rcp protocol was found; OpenSSH release notes are the primary evidence. S10 (8.0): CVE-2019-6111 "scp(1) did not verify that the filenames that the server sent matched those requested by the client. This could allow a hostile server to create or clobber unexpected local files"; "The scp protocol is outdated, inflexible and not readily fixed. We recommend the use of more modern protocols like sftp and rsync"; client check can misfire because "there is no infallible way for the client's wildcard matching to perfectly reflect the server's" (new -T flag disables checks).
- S11 (8.3): "scp(1) could be become desynchronised if a utimes(2) system call failed. This could allow file contents to be interpreted as file metadata" - an in-band framing weakness: data and metadata share one stream.
- S12 (9.0): "This release switches scp(1) from using the legacy scp/rcp protocol to using the SFTP protocol by default"; legacy via -O. Behavioural differences: no remote-shell globbing, `~user` needs `expand-path@openssh.com`.

### TFTP (RFC 1350, 1123, 2347-2349, 7440)

- **EOF by short block** (S13 §2, §5): "A data packet of less than 512 bytes signals termination of a transfer." "If it is 512 bytes long, the block is not the last block of data; if it is from zero to 511 bytes long, it signals the end of the transfer." Lock-step: each packet "must be acknowledged ... before the next packet can be sent".
- **Completion ambiguity** (S13 §6): "If the sender of the data times out and is not prepared to retransmit any more, the transfer may still have been completed successfully ... It is also possible in this case that the transfer was unsuccessful." The dallying recommendation addresses the lost final ACK.
- **Errors unreliable** (S13 §2, §7): ERROR packets are "not acknowledged, and not retransmitted ... so the other end of the connection may not get it. Therefore timeouts are used to detect such a termination"; "This is only a courtesy".
- **Modes** (S13 §5): netascii (receiver "must translate the data to its own format"), octet, mail (obsolete).
- **blksize** (S14, RFC 2348): 8..65464 octets; "If the amount of data to be transfered is an integral multiple of the blocksize, an extra data packet containing no data is sent to end the transfer." tsize (RFC 2349): server returns file size in OACK on RRQ; client may abort with error code 3. Windowsize (RFC 7440): "Traffic with windowsize = 1 MUST be equivalent to traffic specified by [RFC1350]"; on sequence error DRCV "SHOULD" ACK the last correct block. No data integrity check beyond UDP checksum in any of these (inference from absence).
- **Sorcerer's Apprentice** (S2 §4.2.3.1): "While it does not cause incorrect operation of the transfer (the file will always be transferred correctly if the transfer completes), this bug may cause excessive retransmission, which may cause the transfer to time out." Fix MUST: "the sender ... must never resend the current DATA packet on receipt of a duplicate ACK."

### WebDAV (RFC 4918)

- Read is plain HTTP GET (§9.4). Locks are write locks only: "The write lock is a specific instance of a lock type, and is the only lock type described in this specification." (§7) -> No read-lock; a reader cannot exclude concurrent writes via WebDAV *(inference)*. §6.6: "Clients MUST assume that locks can arbitrarily disappear at any time". §8.6: "ETags are necessary along with locks to avoid the lost-update problem"; "Strong ETags are much more useful for authoring use cases than weak ETags". Version-change detection on read therefore defers to HTTP validators (prior report 07-C3).

### rsync

- Algorithm (S16 node2): receiver "splits the file B into a series of non-overlapping fixed-sized blocks of size S bytes. The last block may be shorter"; weak rolling 32-bit + strong 128-bit MD4 checksum per block. Node4: if the strong checksums match, "we assume that we have found a block of A which matches a block of B. In fact the blocks could be different, but the probability of this is microscopic". (Note: current rsync negotiates checksums; S17 "The checksum used is auto-negotiated between the client and the server".)
- Whole-file verification (S17 --checksum): "rsync normally verifies that each transferred file was correctly reconstructed on the receiving side by checking a whole-file checksum that is generated as the file is transferred"; verification "is off when --checksum-choice=none is forced". Default change detection is "quick check" on size and mtime only.
- Partial/resume: "By default, rsync will delete any partially transferred file if the transfer is interrupted" (--partial keeps it). --append: "updates these growing file in-place without verifying any of the existing content in the file (it only verifies the content that it is appending)"; skips files whose sender size "gets shorter during the send negotiations (rsync warns about a "diminished" file". Version difference: "prior to rsync 3.0.0 (March 2008), the --append option worked like --append-verify" (protocol < 30).
- Exit codes: "23 - Partial transfer due to error", "24 - Partial transfer due to vanished source files", "30 - Timeout in data send/receive".

### 9P (Plan 9)

- read(5): "The count field in the reply indicates the number of bytes returned. This may be less than the requested amount. If the offset field is greater than or equal to the number of bytes in the file, a count of zero will be returned." "Because 9P implementations may limit the size of individual messages, more than one message may be produced by a single read ... The iounit field returned by open(5), if non-zero, reports the maximum size that is guaranteed to be transferred atomically." Directory reads must use offset 0 or the previous offset+count.
- intro(5): tags match replies ("Clients must arrange that no two outstanding messages on the same connection have the same tag"); failure is Rerror with a string `ename` (no numeric class in 9P2000); Tversion "aborts all outstanding I/O on the connection"; qid.version "typically, it is incremented every time the file is modified" (a per-file version for change detection; "typically" = not guaranteed).

### BitTorrent (BEP 3)

- "files are split into fixed-size pieces which are all the same length except for possibly the last one which may be truncated"; `pieces` = concatenated "SHA1 hash of the piece at the corresponding index". 'have' payload is "the index which that downloader just completed and checked the hash of". request length "All current implementations use 2^14 (16 kiB), and close connections which request an amount greater than that" (a convention, stated as observed implementation behaviour).

### Empirical studies

- S20 (Globus logs 2014-2017): "27,251 of the 3,312,102 Globus transfers with integrity checking enabled had at least one checksum error (i.e., one in 121 transfers had at least one checksum error)"; "Observation 6. At least one checksum failure occurs per 1.26 TB."; caveat: "if a user changes a file during a transfer, this action can be reported as an integrity failure. We cannot distinguish this from an actual failure." Rationale cites the 16-bit TCP checksum limits (Stone & Partridge). Globus "rereads the file(s) at the source and at the destination, computes a checksum at each location, and compares".
- S21 RIVA: "existing implementations of end-to-end integrity verification for file transfers fall short to detect undetected disk errors that causes inconsistency between disk and cache memory"; motivating experiment (273 files, 274 GB, 16 GB RAM): only the three larger-than-memory files produced page misses during checksumming; "the state-of-the-art integrity verification algorithms fail to detect the injected errors for almost all file sizes"; they "confirmed that other implementations of integrity verification (i.e. block-level [20] and FIVER [21]) exhibit similar behavior".

## 3. Existing models / classifications (as stated by sources)

- **FTP reply-code classes** (RFC 959 §4.2.1): 1yz Positive Preliminary, 2yz Positive Completion, 3yz Positive Intermediate, 4yz Transient Negative Completion, 5yz Permanent Negative Completion; second digit x0 syntax, x1 information, x2 connections, x3 auth, x5 file system.
- **FTP data representation x structure x mode** (RFC 959 §3.1-3.4): TYPE {ASCII, EBCDIC, IMAGE, LOCAL}, STRU {File, Record, Page}, MODE {Stream, Block, Compressed}; EOF signalling and restartability depend on the combination.
- **FTPS PROT levels** (RFC 2228 via RFC 4217): C Clear, S Safe (integrity), E Confidential, P Private; RFC 4217 uses only C and P.
- **SFTP status codes** v3 (0-8) vs v6 (0-31 incl. lock and quota codes); client-only pseudo-errors.
- **TFTP error codes** (RFC 1350 Appendix): 0-7 (e.g., 1 File not found, 3 Disk full); RFC 2347 adds 8 (option negotiation failed).
- **rsync exit codes** (23/24/30 etc.).
- **RIVA's URE/UWE split**: "Undetected disk errors can be categorized into two groups as undetected read errors (URE) and undetected write errors (UWE)" (S21 §2.1, building on Bairavasundaram/Krioukov).

## 4. Convergences / contradictions

Internal:
- **SFTP v3 text vs deployed practice (contradiction)**: S5 says for normal disk files a READ is "guaranteed" to return the requested bytes or up to EOF; S8 says servers "will usually respond with a shorter SSH_FXP_DATA packet" above max-read-length, and S9 caps len and does a single read(2). The OpenSSH client (S9) re-requests remainders rather than treating short = EOF. S6 (v6) resolves the ambiguity by permitting short replies and adding an end-of-file flag. Reconciliation: the v3 guarantee assumes len within server limits *(inference)*.
- **EOF signalling families**: connection close (FTP stream/file), explicit marker in band (FTP block EOF flag, FTP stream record ESC-2), short block (TFTP), explicit status (SFTP SSH_FX_EOF), zero-count reply (9P, also NFSv4 eof=TRUE in prior report). These are source descriptions, not a new taxonomy.
- **Resume offsets**: unambiguous only when stream bytes = file bytes (RFC 3659 STREAM/IMAGE; SFTP absolute offsets, but text mode ignores offsets in v6; OpenSSH refuses resume if server reordered). Version-change safety before resume is heuristic (MDTM, "most likely").
- **Integrity**: FTP and TFTP delegate to transport (RFC 959 §3.5); rsync, BitTorrent, Globus add application checksums; RIVA shows application checksums may verify cached rather than stored bytes.

With the prior report (Binary Stream Read Behavior Foundations.md, B.7 and D):
- Converges with D.1 #3 (truncation detectable only with framing/expected length; [07-C4] close-delimited HTTP/1.1 messages count as complete): FTP stream/file-structure EOF by close has the same property; TFTP short-block framing and SFTP explicit EOF status are framing-based. Adds FTPS: RFC 4217 itself does not specify close_notify handling (gap), unlike the TLS close_notify point the prior report cites [02-C17/02-C18].
- Converges with D.1 #4 (partial results are normal successes) and [07-C8] NFSv4.1 short read eof=FALSE: SFTP v6 short replies, 9P short counts, OpenSSH limits. SFTP v3 text partially diverges (guaranteed full reads for disk files), analogous to the SMB2 MinimumCount outlier [07-C10] only in spirit.
- Converges with [07-C18] (TCP checksum misses errors) and D.1 #2 (detectability depends on check placement, [05-C17] end-to-end argument): RFC 959 §3.5 relies on TCP; Liu et al. measure a non-negligible checksum-failure rate (1 in 121 transfers); RIVA shows checksum placement relative to the page cache decides detection - a direct file-transfer instance of D.1 #2 and of ZFS cache-hit point [05-C9].
- Converges with D.1 #7 mid-stream version change "guarded locally per protocol (If-Range, ETag, change attribute) [07-C3, 07-C9]": FTP has only pre-resume MDTM/modify heuristics; 9P qid.version; rsync "diminished" files and exit 24; Globus cannot distinguish change-during-transfer from corruption (S20). Extends: none of FTP/SFTP v3/TFTP guard against change *during* a single read.
- Converges with D.1 #1 (status and data correctness separate): FTP block-mode "suspected errors" code delivers data flagged unreliable; TFTP final-ACK timeout leaves outcome unknown.
- D.3 (data together with an error): SFTP v3 never returns data and error in one reply (DATA or STATUS); RFC 959 abort yields 426 after data already delivered - partial data plus error on control channel.
- Error-class model: RFC 959's 4yz/5yz is a formal transient/permanent split, but the RFC itself calls "transient" hard to define; prior report has no FTP-like class split for network protocols (HTTP 503 Slow Down [07-C14] is the nearest).
- Prior report section A/F.2 did not cover these protocols; this track fills that COVERAGE-GAP.

## 5. Gaps

- GENUINE-GAP: RFC 4217 gives no normative rule for detecting a truncated FTPS data connection (TCP FIN without TLS closure); behaviour is left to TLS and implementations.
- GENUINE-GAP: SFTP has no ratified standard; all versions are expired drafts; OpenSSH documents v3 plus extensions only.
- GENUINE-GAP: scp/rcp protocol has no specification; evidence is only implementation release notes and CVEs.
- GENUINE-GAP: FTP, SFTP v3, TFTP have no mechanism to detect source modification during a single read; FTP's pre-resume check is heuristic.
- GENUINE-GAP (as far as searched): no peer-reviewed empirical study found of FTP/SFTP/TFTP truncation or resume errors in the wild; empirical integrity evidence is limited to GridFTP/Globus (S20) and fault injection (S21).
- COVERAGE-GAP: TLS 1.3 (RFC 8446) closure rules, RFC 2228, RFC 2428, RFC 1123 FTP section beyond §4.1.3.4, MODE Z / GridFTP (GFD.20) not read.
- COVERAGE-GAP: AFS/Coda, SMB-over-QUIC, 9P2000.L (Linux v9fs), SFTP check-file deployment status, rsync protocol internals beyond man page, BitTorrent v2 (BEP 52 Merkle hashing) not read.
- COVERAGE-GAP: Remote block protocols (NBD, iSCSI beyond prior report, NVMe-oF) out of this track.
- COVERAGE-GAP: RIVA publication venue not confirmed from the copy read.
