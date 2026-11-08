# Verification notes

Method: 3 independent verifiers per track (lenses: fidelity, overreach, currency), each re-reading the cited full text and trying to refute every claim of the track. A claim is KILLED on >=2 refutes, CONTESTED on 1 refute, VERIFIED on >=2 supports with no refute.

Result: Counter({'VERIFIED': 208, 'CONTESTED': 3, 'KILLED': 1})

Per-claim verdicts and all verifier qualifications:

## 01-C1 - CONTESTED (2S/1R/0U)

POSIX permits read() to return fewer than nbyte bytes on success for exactly enumerated reasons: fewer bytes left in file, signal interruption, or pipe/FIFO/special file with fewer bytes immediately available.

- REFUTE [overreach] POSIX.1-2024 read() DESCRIPTION (downloaded full text) says 'The value returned may be less than nbyte if ...' and then lists three conditions, followed by 'For example, a read() from a file associated with a terminal may return one typed line'. The text is permissive. It never says 'only if', and it does not present the list as exhaustive. The same page gives other ways a read can come back short: 'no data transfer shall occur past the offset maximum' for regular files; nbyte > {SSIZE_MAX} is implementation-defined; a socket read is 'equivalent to recv()'; shared and typed memory objects are unspecified. Calling the list 'exactly enumerated' (exclusive) is material overreach.
- [fidelity] POSIX says the value 'may be less than nbyte if...'. It does not say 'only if', so calling the list 'exactly enumerated' or exhaustive goes beyond the text.
- [overreach] POSIX names three conditions under which read() 'may' return fewer than nbyte bytes: fewer bytes left in the file, interruption by a signal, or a pipe/FIFO/special file with fewer bytes immediately available. The text does not say the list is exhaustive. Other clauses also allow short or implementation-defined counts (the offset maximum, nbyte > SSIZE_MAX, sockets via recv()).
- [currency] POSIX words this permissively ('may be less than nbyte if ...'). It does not say the list is exhaustive, so 'exactly enumerated' overstates the text. Separately, results for nbyte > SSIZE_MAX are implementation-defined.

## 01-C2 - VERIFIED (3S/0R/0U)

POSIX requires read() to return 0 when the starting position is at or after end-of-file, but the result of subsequent reads on device special files is implementation-defined.

- [overreach] For device special files, POSIX leaves later reads implementation-defined. It does not require that EOF be non-sticky; it just does not require EOF to be sticky.
- [currency] 'EOF is not sticky for devices' is an inference. The spec only says that later reads on device special files are implementation-defined.

## 01-C3 - VERIFIED (3S/0R/0U)

POSIX mandates that a read interrupted by a signal after transferring data returns the partial byte count (BSD/FIPS 151 behavior), and -1/EINTR only if no data was read; the rationale notes buffering implementations may still return EINTR because data movement into the user buffer can be deferred.


## 01-C4 - VERIFIED (3S/0R/0U)

POSIX requires that unwritten portions of a regular file before EOF read as zero bytes.


## 01-C5 - VERIFIED (3S/0R/0U)

POSIX defines a hole as a zero-valued region, does not require all zero runs to be reported as holes, and requires every seekable file to have a virtual hole at its current size.

- [overreach] More precisely, a hole is a contiguous zero-valued region. Not every zero region needs to be reported as one.

## 01-C6 - VERIFIED (3S/0R/0U)

POSIX lists EIO for physical I/O errors only as a 'may fail' condition and declares hardware-error behavior out of scope; file offset after an error is unspecified.

- [fidelity] A separate EIO case is a 'shall fail' condition: a background process reading its controlling terminal. Only physical I/O errors are 'may fail'.
- [overreach] The out-of-scope statement and the unspecified offset both come from the informative RATIONALE, not from normative text.

## 01-C7 - VERIFIED (3S/0R/0U)

POSIX §2.9.7 requires read(), readv(), pread(), write(), lseek() and related calls on file descriptors to be mutually atomic in their specified effects: each call sees all or none of the other's effects.

- [overreach] The requirement carries the 'Except where specified otherwise' qualifier, is stated for two threads, and is limited to files in the file hierarchy.

## 01-C8 - VERIFIED (3S/0R/0U)

Linux did not satisfy POSIX read offset atomicity before 3.14: concurrent reads through a shared open file description could obtain overlapping data.

- [currency] The man page frames this against POSIX.1-2008 §2.9.7 wording ('regular files or symbolic links'), not Issue 8.

## 01-C9 - VERIFIED (3S/0R/0U)

POSIX requires mmap to zero-fill the partial last page and deliver SIGBUS for references to whole pages beyond the end of the object; SIGBUS on other mapped-object errors is permitted but not required.

- [overreach] The required SIGBUS covers references within the mapped range [pa, pa+len) to whole pages past the end of the object.

## 01-C10 - VERIFIED (3S/0R/0U)

On Linux, O_DIRECT alignment restrictions vary by filesystem and kernel and misaligned O_DIRECT I/O may either fail with EINVAL or silently fall back to buffered I/O.

- [overreach] The word 'silently' is not in the source. The man page also says alignment restrictions may be absent entirely.

## 01-C11 - VERIFIED (3S/0R/0U)

Linux SA_RESTART/EINTR semantics apply only to 'slow' devices; local disk reads are not interrupted by signals.

- [fidelity] The slow-device condition is stated only for read/readv/write/writev/ioctl. Other listed calls (wait, socket calls, flock and others) are also interruptible, whatever the device.
- [overreach] Say instead: for read/readv/write/writev/ioctl, Linux applies SA_RESTART/EINTR only to 'slow' devices (terminals, pipes, sockets), and local disk I/O is not interrupted by signal handlers. Other syscalls (open on a FIFO, wait, sockets, locks, etc.) have their own rules.
- [currency] The man page refers to signal-handler interruption only. Fatal signals can still end killable waits, and network filesystems are a separate case.

## 01-C12 - VERIFIED (3S/0R/0U)

After a failed buffered writeback on Linux, filesystems usually discard and mark affected pages clean, so a later read may return something other than the written data.

- [fidelity] The quote is in roughly the third paragraph, not the second.
- [overreach] Hedge this as the LWN 2018 characterization. Rebello et al. (2020) found that ext4/XFS keep the latest data in clean pages until eviction, so the read returns different data only after eviction (Btrfs reverts at once).
- [currency] The OpenBSD/NetBSD statement is about failing to report errors, not explicitly about discarding pages. LWN reader comments say FreeBSD keeps the pages dirty instead.

## 01-C13 - VERIFIED (3S/0R/0U)

Empirically, after fsync failure ext4 and XFS keep the latest unpersisted data in clean page-cache pages (reads see new data until eviction, then old on-disk contents), whereas Btrfs reverts in-memory state to the on-disk state.

- [overreach] The finding is for data-block write faults on Linux 5.2.11 under fault injection.

## 01-C14 - VERIFIED (3S/0R/0U)

Linux errseq_t guarantees that every open file descriptor gets an error on the first fsync after a writeback error; the mechanism targets sync calls, not read().

- [fidelity] The article describes Jeff Layton's patch set at the proposal stage. The version >= 4.13 comes from the 2018 LWN article, not this one.
- [overreach] The source describes Jeff Layton's proposed patch set: each open file description (struct file) gets the error on its first fsync after a writeback error, in filesystems converted to the scheme (FS_WB_ERRSEQ). The 'not read()' scoping and the 4.13 version come from inference or other sources.
- [currency] The article describes Jeff Layton's patch set before it was merged (merged for 4.13), and 'reliably' is the design goal stated there. 'Targets sync calls, not read()' is inference. Later kernels changed the open-time sampling so that a not-yet-seen error is still reported (recalled from memory, not checked against a source). Treat the 'every open fd' guarantee as covering fds opened before the error.

## 01-C15 - VERIFIED (3S/0R/0U)

Windows signals EOF differently by handle mode: synchronous ReadFile returns TRUE with zero bytes read; asynchronous EOF is GetOverlappedResult FALSE with ERROR_HANDLE_EOF.

- [fidelity] The page also notes that asynchronous EOF can show up on the initial ReadFile call, which returns FALSE with ERROR_HANDLE_EOF.
- [overreach] In asynchronous mode, EOF can also show up immediately as ReadFile returning FALSE with ERROR_HANDLE_EOF on the initiating call, not only through GetOverlappedResult.
- [currency] The page's sample also shows that ReadFile itself can return FALSE with ERROR_HANDLE_EOF on the initiating async call.

## 01-C16 - VERIFIED (3S/0R/0U)

On Windows, a zero-byte successful ReadFile on a pipe means the writer wrote zero bytes (not EOF); a closed anonymous-pipe writer yields FALSE/ERROR_BROKEN_PIPE, and ReadFile fails if it overlaps a byte range locked by another process.


## 01-C17 - VERIFIED (3S/0R/0U)

Windows unbuffered (FILE_FLAG_NO_BUFFERING) reads require sizes and offsets that are integer multiples of the volume sector size; buffer address alignment may not be enforced depending on disk.

- [overreach] This applies to seekable devices such as files; named pipes and comm devices may have no alignment requirement.
- [currency] Sizes and offsets must be multiples of the volume sector size. Buffer alignment is to the physical sector size, a distinct value.

## 01-C18 - VERIFIED (3S/0R/0U)

Windows marks files whose data is not locally present; reading a RECALL_ON_DATA_ACCESS file triggers fetching content from a remote store.

- [fidelity] The source puts it as reading being 'more expensive than normal, e.g. it will cause at least some of the file/directory content to be fetched'. That is an example, not an unconditional trigger.
- [overreach] The doc says a read is 'more expensive than normal, e.g.' at least some content is fetched remotely. The file may be partly local, so not every read necessarily triggers a fetch.
- [currency] The doc's wording is softer: reading 'will be more expensive than normal, e.g. it will cause at least some of the ... content to be fetched'. It says this attribute only kernel-mode callers can set.

## 02-C1 - VERIFIED (3S/0R/0U)

In ISO C, fgetc returns the same value (EOF) for both end-of-file and a read error. The two are distinguished only through the per-stream end-of-file and error indicators (feof/ferror).

- [overreach] The footnote says the two can be told apart with feof/ferror. It does not say this is the only way. It is also informative footnote text, not normative. Also, EOF comes back whenever the EOF indicator is already set, not only on reaching end-of-file.
- [currency] N1570 (C11) has been superseded by C17 and C23 (ISO/IEC 9899:2024). The C23 draft N3220 keeps the text unchanged but renumbers it as §7.23.7.1, footnote 336. Cite the C23 location, or say the citation is to C11.

## 02-C2 - VERIFIED (3S/0R/0U)

ISO C makes the file position indeterminate after a fread error and leaves the value of a partially read element indeterminate. A short fread count can mean either a read error or end-of-file.

- [currency] In C23 (N3220 §7.23.8.1) this is renumbered and the wording changes from 'value' to 'representation is indeterminate'. The meaning is unchanged.

## 02-C3 - VERIFIED (3S/0R/0U)

ISO C binary streams must round-trip data, but they may have an implementation-defined number of null characters appended at the end. The length observed on read need not equal the length written.

- [overreach] The round-trip guarantee holds only 'under the same implementation'. The only allowed difference in length is trailing null characters, an implementation-defined number of them.
- [currency] In C23 this is §7.23.2p3.

## 02-C4 - VERIFIED (3S/0R/0U)

POSIX read() may return fewer than nbyte bytes when fewer bytes remain, when interrupted by a signal after some data was transferred, or for pipes, FIFOs and special files. An interrupt before any data gives -1/EINTR.

- [overreach] For pipes, FIFOs and special files, the condition is fewer than nbyte bytes immediately available. Being that kind of file is not by itself the cause.

## 02-C5 - VERIFIED (3S/0R/0U)

POSIX deliberately leaves the file offset unspecified after read() returns an error, and treats hardware-error behaviour as out of scope.

- [overreach] This is informative rationale. It also says the offset 'clearly' should not change for immediately detected errors such as EAGAIN, and that many implementations update it after an interrupt or a hardware error.

## 02-C6 - VERIFIED (3S/0R/0U)

Go's io.Reader contract allows one Read call to return n>0 bytes together with a non-nil error, including EOF, and requires callers to process those bytes before looking at the error.

- [fidelity] The doc says callers 'should' process the bytes first, not 'must', so it is strong guidance rather than a hard requirement.
- [overreach] The doc says callers 'should' process the bytes first, which is a convention. It is not phrased as a hard requirement. Returning the error in the same call is one of two allowed behaviours; the other is returning it on the next call.
- [currency] Precisely: the error may come from the same call or from a later call with n == 0, so n>0 together with an error is allowed but not required.

## 02-C7 - VERIFIED (3S/0R/0U)

In Go, a Read returning 0 bytes and a nil error does not indicate EOF. EOF is reserved for a graceful end of input, and an EOF inside a structured stream should be reported as ErrUnexpectedEOF or a more detailed error.


## 02-C8 - VERIFIED (3S/0R/0U)

Go io.ReadFull returns EOF only if no bytes were read and ErrUnexpectedEOF if EOF came after a partial read. It drops any error that arrives once len(buf) bytes have been read.


## 02-C9 - VERIFIED (3S/0R/0U)

Rust's Read::read requires that an Err return means no bytes were read. Ok(0) means EOF or an empty buffer, and is not necessarily permanent (a File can return more data after it is appended to).

- [overreach] This is a documented contract on implementors of a safe trait, so the compiler does not enforce it.
- [currency] On current main the trait docs live in library/alloc/src/io/read.rs (std re-exports it). The wording is unchanged.

## 02-C10 - VERIFIED (3S/0R/0U)

Rust read_exact returns ErrorKind::UnexpectedEof if end of file comes before the buffer is full. The buffer contents and the number of bytes consumed are unspecified on error.

- [overreach] The number of bytes consumed is unspecified but bounded: never more than needed to fill the buffer. Interrupted errors are retried, not returned.

## 02-C11 - VERIFIED (3S/0R/0U)

Java InputStream.read(byte[],int,int) may read fewer than len bytes and returns -1 only at end of stream. Its default implementation catches an IOException raised after the first byte and treats it as end of file, returning a short count.

- [overreach] The catch-and-treat-as-EOF behaviour is @implSpec for InputStream's own default implementation. Subclasses that override the method, which the doc encourages, need not do this. Also, len==0 returns 0.
- [currency] Minor: it also returns 0 when len == 0. The exception is passed on if the first read() fails.

## 02-C12 - VERIFIED (3S/0R/0U)

Java signals an unexpected end of stream with EOFException (e.g., DataInputStream.readFully), but readNBytes(byte[],int,int) returns a short count instead of throwing when the end is reached early.

- [fidelity] The DataInputStream.readFully example is not in the cited files; DataInputStream.java was not checked.
- [overreach] Java uses EOFException mainly in data input streams. Its own doc says many other input operations return a special value at end of stream instead, so it is not Java's general way of signalling an unexpected end.

## 02-C13 - VERIFIED (3S/0R/0U)

Python RawIOBase.read encodes three outcomes: 0 bytes (with size != 0) means EOF, None means no data in non-blocking mode, and a short result can follow from a short OS call even after EINTR retries.


## 02-C14 - VERIFIED (3S/0R/0U)

.NET Stream.Read returns 0 only when zero bytes were requested or no more data is expected, may return fewer bytes before the end of the stream, and leaves the position unchanged if an exception occurs.

- [overreach] The unchanged position is stated in remarks that describe what implementations do. Nothing shows it is checked or enforced, as the claim's applicability already notes.

## 02-C15 - VERIFIED (3S/0R/0U)

Node.js stream.finished reports a premature close as an error. Since v14, a Readable that emits 'close' before 'end' produces ERR_STREAM_PREMATURE_CLOSE.


## 02-C16 - VERIFIED (3S/0R/0U)

In the WHATWG Streams standard, reader.read() fulfills with done:true when the stream closes and rejects when it errors. A BYOB read with min may get fewer elements than requested when the stream closes.

- [fidelity] The methods are in subsections §4.4.3 and §4.5.3, not §4.4 itself.
- [overreach] Minor: for a BYOB read, closing fulfills with {value: newView, done: true}, not value undefined. A canceled reader also fulfills with done:true, so done:true does not always mean the stream closed normally.
- [currency] The BYOB read on close fulfills with { value: newView, done: true }, not value undefined. The default-reader quote applies only to ReadableStreamDefaultReader.

## 02-C17 - VERIFIED (3S/0R/0U)

RFC 9112 states that a close-delimited HTTP/1.1 message cannot be told apart from a truncated one. Chunked or Content-Length framing makes incompleteness detectable.

- [overreach] The RFC says this about close-delimited response messages. §8 also says such a response, if its header section arrived intact, 'is considered complete unless an error was indicated by the underlying connection' (for example a TLS incomplete close). So the RFC treats it as complete by default, not as indeterminate.

## 02-C18 - VERIFIED (3S/0R/0U)

TLS 1.3 requires close_notify before closing the write side, because a transport-level close without it leaves the receiver unable to know that all sent data arrived (a truncation attack).

- [fidelity] The MUST has an exception: a party that has already sent an error alert need not send close_notify. The RFC states the requirement and the truncation risk side by side; 'because' is a fair reading, not its wording.
- [overreach] The MUST has an exception: it does not apply if the party has already sent an error alert. The RFC states the truncation reason and the requirement side by side and does not write an explicit 'because'.
- [currency] RFC 8446 is superseded by RFC 9846 (July 2026), which keeps the §6.1 text unchanged. Cite RFC 9846 §6.1 as the current TLS 1.3 specification.

## 03-C1 - VERIFIED (3S/0R/0U)

In NVMe, when a read fails with an error such as Unrecovered Read Error or End-to-end Guard Check Error, the controller may either stop DMA or put the erroneous data into host memory anyway. The host is required to ignore that buffer.

- [currency] Base 2.1 is no longer the current revision. The text is unchanged in Base 2.4 (July 2026), so the citation could be updated to 2.4.

## 03-C2 - VERIFIED (3S/0R/0U)

NVMe defines distinct Media and Data Integrity status codes for reads: 81h Unrecovered Read Error, 82h/83h/84h/88h end-to-end Guard, Application Tag, Reference Tag and Storage Tag check errors, and 87h Deallocated or Unwritten Logical Block. A separate DNR bit says whether resubmitting the command is expected to fail.

- [overreach] The 82h-84h and 88h end-to-end check codes are not specific to reads; they also apply to writes (section 9.2 gives End-to-end Guard and Application Tag Check Error as write-error examples). 87h belongs to the NVM Command Set. DNR is a general status-field bit, not one tied to media errors.
- [currency] In the current Base 2.4 the table is Figure 107, not Figure 106. The status codes and DNR semantics are unchanged.

## 03-C3 - VERIFIED (3S/0R/0U)

NVMe Read Recovery Level offers 16 levels that trade read completion time against the amount of error recovery. Level 4 (the default, nominal recovery) and Level 15 ('Fast Fail', minimum recovery) are mandatory. How these levels interact with the per-command Limited Retry bit is implementation specific.

- [overreach] Levels 4 and 15 are mandatory only for controllers that support Read Recovery Levels (CTRATT RRLVLS=1), which is itself optional. The other 14 levels are optional ('may be supported').
- [currency] The levels are mandatory only if Read Recovery Levels are supported, which is optional. Base 2.4 is now current, with the same text.

## 03-C4 - VERIFIED (3S/0R/0U)

In NVMe, if the DULBE error is not enabled, a read of a deallocated or unwritten block returns all 00h if DLFEAT.DRB=001b, all FFh if DRB=010b, and either all 00h or all FFh if DRB=000b. The value must stay the same on repeated reads until the block is written.

- [overreach] The listed values apply to user data and metadata excluding protection information. The determinism rule is worded for a 'deallocated logical block'.
- [currency] NVM Command Set 1.3 (July 2026) is current and the text there is the same.

## 03-C5 - VERIFIED (3S/0R/0U)

On NVMe, the protection information returned for a deallocated or unwritten block has its Application, Storage and Reference Tag fields set to FFh, which marks the PI as not to be checked. For Type 1/2 namespaces, an Application Tag of FFFFh disables all PI checks whatever PRCHK says.

- [fidelity] The Guard field of a deallocated block is either FFh or a valid CRC; only the Storage, Application and Reference Tags are always FFh.
- [overreach] The Guard field of a deallocated block is set to FFh or to the CRC of the returned data. The Storage Tag is set to FFh only 'if defined'.
- [currency] The Storage Tag is set to FFh only if present. The Guard may be FFh or a valid CRC. In NVM CS 1.3 the disable rule also overrides the STC (Storage Tag Check) field.

## 03-C6 - VERIFIED (3S/0R/0U)

NVMe AWUPF/NAWUPF guarantees that after a power failure or error interrupts a write no larger than AWUPF that does not cross an atomic boundary, later reads return either all old data or all new data. Beyond that limit, nothing is guaranteed about the data later reads return.

- [overreach] The guarantee applies to the interrupted command's own LBA range. In Multiple Atomicity Mode (section 2.1.4.5), a boundary-crossing write is atomic per subrange rather than wholly unguaranteed.
- [currency] Section 2.1.4.4 / 2.1.4.5 add a caveat: in Multiple Atomicity Mode (NVM CS 1.1+), atomicity is still guaranteed per atomic LBA subrange on a torn write. So 'nothing is guaranteed' beyond AWUPF holds for Single Atomicity Mode. In NVM CS 1.3, fused Compare and Write uses ACWU/NACWU instead.

## 03-C7 - VERIFIED (3S/0R/0U)

In NVMe, a read issued after a write completes without error must return that write's data, not an older version. The exception is when a volatile write cache is enabled, FUA is not set, no flush completed, and main power is lost without a shutdown.

- [fidelity] Condition a) also requires that the controller supports a volatile write cache; condition d) concerns flushes completed before shutdown complete is reported.
- [overreach] Even when all five conditions hold, only locations still in the volatile cache and not yet written to non-volatile media 'may return older data'. The flush condition is limited to flushes for the same namespace as the write.
- [currency] Condition (d) is narrower than 'no flush completed': it requires that no flush for the same namespace completed before shutdown complete was reported. Also, the exception allows older data only for locations still in the volatile cache.

## 03-C8 - VERIFIED (3S/0R/0U)

SCSI SBC-3 classes an unrecovered read error under sense key MEDIUM ERROR or HARDWARE ERROR and a recovered read error under RECOVERED ERROR. The sense INFORMATION field carries the LBA of the unrecovered block, or the LBA of the last recovered error.

- [overreach] Working draft only. When fixed-format sense data cannot hold the LBA (e.g., an 8-byte LBA), VALID is set to zero.
- [currency] This is a 2005 pre-revision proposal. SBC-3 was later approved, and SBC-4 and later supersede it. I did not check the current approved text because T10 drafts are member-restricted.

## 03-C9 - VERIFIED (3S/0R/0U)

The SCSI Read-Write Error Recovery mode page lets the host allow data to reach the buffer without a clean outcome. TB=1 transfers an unrecovered block before CHECK CONDITION with vendor-specific contents. RC=1 lets the device send erroneous or fabricated data so the data flow stays continuous.

- [overreach] The RC=1 fabrication is stated as an implication ('This implies ... may'), not an explicit permission. RC takes priority over conflicting bits in that byte.
- [currency] This is an early working draft. Later SBC revisions were not checked.

## 03-C10 - VERIFIED (3S/0R/0U)

SCSI SBC-3 says that when a write is interrupted by power loss or a medium or hardware error, the affected blocks are indeterminate, and later reads may return old data, new data, or vendor-specific data.

- [overreach] The text covers commands performing write operations that are being processed at the time of the failure. Working draft.
- [currency] This is an early working draft, now superseded by approved SBC-3 and SBC-4. Later SBC revisions add atomic write features (e.g., WRITE ATOMIC in SBC-4), so the remark that SCSI has no atomicity unit applies only to this 2005 text (inference).

## 03-C11 - VERIFIED (3S/0R/0U)

In SCSI, a deferred error (response code 71h/73h) reports a condition from an earlier command that already returned GOOD status. A command terminated to report a deferred error was not itself processed.

- [fidelity] The earlier command returned GOOD, CONDITION MET, INTERMEDIATE or INTERMEDIATE-CONDITION MET status, not only GOOD.
- [overreach] The earlier command may have returned GOOD, CONDITION MET or an INTERMEDIATE status, not only GOOD. The source is vendor documentation, not SPC.
- [currency] The claim's own wording ('for which GOOD ... status has already been returned') is fine. It is vendor text mirroring SPC; SPC-4 or SPC-5 itself was not checked.

## 03-C12 - VERIFIED (3S/0R/0U)

In SCSI protection information, the Guard is a CRC-16 (G(x)=18BB7h) over the user data. An Application Tag of FFFFh disables checking of all PI for that block, and a PI check failure on read is reported with sense key ABORTED COMMAND (for example LOGICAL BLOCK GUARD CHECK FAILED).

- [overreach] Working draft (2005). Later SBC-3 revisions refined the escape conditions (e.g., Type 3 also requires the Ref Tag to be FFFFFFFFh), so the unconditional FFFFh rule reflects this early draft.
- [currency] In this 2005 draft, App Tag FFFFh disables all checks unconditionally. Later SBC-3 and SBC-4 make this depend on protection type: for Type 3, the Reference Tag must also be FFFFFFFFh, matching NVMe. That is inference from later-standard knowledge, not verified here. Treat the unconditional rule as draft-specific.

## 03-C13 - VERIFIED (3S/0R/0U)

In ATA, if Trim is supported without DRAT, each read of a trimmed block may return different data. With DRAT the data becomes deterministic, set to any value if RZAT=0 or zeroed if RZAT=1. In every case the data must not come from data the host sent for any other LBA.

- [overreach] 'Deterministic' is defined as: after a read completes, the block becomes determinate and subsequent reads return the same data. The spec also says a DSM Trim may actually trim 'none, some, or all' of the requested LBAs, so the behaviour applies only to LBAs that were actually trimmed.
- [currency] This is a working draft from a third-party mirror, and ACS-4 and ACS-5 supersede it. Not verified against ACS-5.

## 03-C14 - VERIFIED (3S/0R/0U)

ATA reports an unrecoverable read through error-field bits: UNCORRECTABLE ERROR for uncorrectable data, and INTERFACE CRC (with ABORT) for an Ultra DMA transfer CRC error. READ DMA EXT returns the LBA of the first unrecoverable error.

- [overreach] Per 6.8.2, that LBA is the first unrecoverable error encountered 'prior to or during' the command and 'may be outside the LBA range of the command'. The data already transferred is indeterminate. INTERFACE CRC may also apply to Multiword DMA and PIO transfers.
- [currency] Per 7.22.5, 'The validity of the data transferred is indeterminate.' This is a working draft; ACS-5 is current.

## 03-C15 - VERIFIED (3S/0R/0U)

The ATA SCT Error Recovery Control Read Command Timer sets an upper limit, in 100 ms units, on the total time a device spends processing a read command. A value of zero means all available error recovery is performed.

- [overreach] For NCQ commands with in-order data delivery, the timer starts when the device begins processing the command, not when the command is sent.
- [currency] This is a working draft; ACS-5 is current and was not checked.

## 03-C16 - VERIFIED (3S/0R/0U)

In ATA, WRITE UNCORRECTABLE EXT in pseudo mode (55h) makes later reads fail for every logical sector in the same physical block, after full normal error recovery and with error logging. Flagged mode (AAh) affects only the specified sectors. The attribute persists across power and reset events until the sector is written.

- [fidelity] In pseudo mode, full recovery may be cut short by an error recovery control timeout (8.3.3). A write clears only the written logical sector, not the other sectors in the same physical block.
- [overreach] Pseudo-mode recovery runs to completion unless an SCT error recovery control timeout fires first. A successful write clears the attribute only for the written logical sectors, not for other sectors in the same physical sector. Flagged mode 'should not' perform error logging.
- [currency] In pseudo mode, error recovery runs 'to the fullest extent' unless an SCT ERC timeout ends it first. This is a working draft.

## 03-C17 - VERIFIED (3S/0R/0U)

For SD cards, data after a discard is 'don't care': the previously written data may still be read back partially or fully. Data after an erase is all '0' or all '1' depending on the vendor, as reported by SCR DATA_STAT_AFTER_ERASE.

- [overreach] 'Don't care' is a duty on the host. DISCARD is supported only for SDHC/SDXC and not over SPI; a card without DISCARD support executes ERASE instead.
- [currency] Per the spec, discard is supported only on SDHC/SDXC cards, not over SPI, and is optional (DISCARD_SUPPORT bit).

## 03-C18 - VERIFIED (3S/0R/0U)

Field data from 1.53 million disk drives over 41 months showed more than 400,000 checksum mismatches. These were detected by storage-system checksums on read and had no indication from the drive. The causes include bit corruption in the data path, torn writes and misdirected writes.

- [overreach] Table 1 and section 2.3 list these as 'possible causes'; the paper also notes that 'In many cases, the cause of corruption cannot be identified'. The causes include hardware and software anywhere in the storage stack (shelf firmware, memory, adapters, software bugs), not only the drive. The cause given is 'data content corrupted by components within the data path', not specifically bit-level corruption. The data covers NetApp production and development systems.
- [currency] The paper attributes corruption to the whole storage stack (drives, adapters, firmware, software), not only the drives.

## 04-C1 - VERIFIED (3S/0R/0U)

In NetApp field data, a latent sector error is a read or write failure of a sector, or an uncorrectable ECC error, that destroys the sector's prior content. It is distinct from not-ready-condition errors and from recovered errors, where the read succeeds after disk-level retry or ECC. 3.45% of 1.53M disks developed at least one LSE in 32 months.

- [overreach] The quoted LSE definition sits in the Sec. 2 background box, not in Sec. 2.2. 3.45% is for this NetApp population and is a lower bound, not a general HDD rate.

## 04-C2 - VERIFIED (3S/0R/0U)

Most LSEs are found by background verify (scrub) operations rather than by application reads: 86.6% (nearline) and 61.5% (enterprise) via verify, against 13.4% and 19.1% via reads.

- [fidelity] Say that the figures are averages across disk models, and that writes find 19.3% of enterprise LSEs.
- [overreach] For enterprise disks, verify is a majority (61.5%), but writes (19.3%) find about as many as reads (19.1%). The split depends on scrub policy and workload and varies widely across models.
- [currency] For completeness: writes discover 19.3% of enterprise LSEs and 0% of nearline LSEs.

## 04-C3 - VERIFIED (3S/0R/0U)

LSEs show spatial locality: for most disk models, the probability of another LSE within a 10 MB logical radius of an existing one is about 0.5.

- [fidelity] The source puts it as 0.5, and more than 0.6 for many models, i.e. at least about 0.5 rather than 'about 0.5'.
- [overreach] The source says 'is 0.5' and more than 0.6 for many models, so 'about 0.5' is better read as 'at least about 0.5'.
- [currency] The paper says 0.5 for most models and more than 0.6 for many, so 'about 0.5' should read 'at least about 0.5'.

## 04-C4 - VERIFIED (3S/0R/0U)

In a storage stack with block checksums, silent data corruption is classified by how it is detected: checksum mismatch (on any disk read), identity discrepancy (on a file-system read) and parity inconsistency (on a data scrub). Each class has listed possible causes: bit-level corruption, torn, lost or misdirected writes, memory corruption, bad parity calculation.

- [fidelity] The quote comes from Sec. 1 (Introduction); Sec. 2.3 holds the detailed class definitions. The paper's wording for the parity case is 'processor miscalculations' (and software bugs), not 'bad parity calculation'. The paper speaks of data content corrupted in the data path rather than 'bit-level corruption'.
- [overreach] The classification belongs to the NetApp stack's detection mechanisms, not to any storage stack with block checksums. The source's list of PI causes also includes processor miscalculation and software bugs.
- [currency] Strictly, the causes listed per class are: checksum mismatch = bit-level corruption, torn write, misdirected write; identity discrepancy = lost or misdirected write; parity inconsistency = memory corruption, lost write, bad parity calculation.

## 04-C5 - VERIFIED (3S/0R/0U)

Over 41 months, 0.86% of 358k nearline disks and 0.065% of 1.17M enterprise disks developed checksum mismatches, about 400,000 in total. That is roughly an order of magnitude less often than latent sector errors.

- [overreach] 'An order of magnitude less often' compares the per-disk probability of developing the error, not event counts. Both figures are lower bounds for detected corruption in this NetApp population.
- [currency] The paper says 'more than 400,000', not 'about 400,000'.

## 04-C6 - VERIFIED (3S/0R/0U)

Checksum mismatches are strongly spatially correlated at block granularity: on disks with at least 2 mismatches, an average of 3.4 consecutive blocks are affected, and beyond consecutive blocks there is little spatial locality. Some specific block numbers are corrupted across many disks of one model.

- [fidelity] The claim's 'applicability' field is wrong: the paper says the block-number effect was seen for model E-1, and it explicitly verified that 'other disk models did not develop multiple checksum mismatches for the same set of block numbers'. So it was not 'E-1 and others'. Also, the text adds that some spatial locality remains even when consecutive mismatches are left out.
- [overreach] 'Beyond consecutive blocks there is little spatial locality' overstates this: the authors note that locality remains even when consecutive cases are excluded. The applicability phrase 'model E-1 and others' is inaccurate for the same-block-numbers-across-disks effect, which was specific to E-1.
- [currency] The applicability note is wrong: Sec. 6.1.1 says the effect was observed for model 'E-1' and that 'other disk models did not develop multiple checksum mismatches for the same set of block numbers'. It was not seen in 'E-1 and others'.

## 04-C7 - VERIFIED (3S/0R/0U)

RAID reconstruction itself encounters checksum mismatches (about 8% of mismatches in nearline disks) despite biweekly scrubbing. So data read during recovery can be corrupt and can cause data loss.

- [fidelity] The source calls the outcome a 'possibility of real data loss', not certain loss.
- [overreach] The source does not directly measure data loss. 'Can cause data loss' is inference: a mismatch found during single-parity reconstruction cannot be repaired from parity.
- [currency] 'Can cause data loss' is the authors' implication, not a measured outcome.

## 04-C8 - VERIFIED (3S/0R/0U)

LSE arrivals on a drive are bursty and fit a Poisson model poorly. For 55-85% of drives, all errors within a year after the first fall in a single 2-week scrub interval, and a Pareto distribution fits the error counts better than a Poisson one.

- [currency] The Poisson/Pareto fit is in Sec. 3.3 (on the spatial-distribution page, just before 3.4), not in Sec. 3.4 itself. The 55-85% figure is in Sec. 3.4.

## 04-C9 - VERIFIED (3S/0R/0U)

In Google's flash fleet, final read errors (read errors that persist after retries) are the most common non-transparent error. They affect 20-63% of drives and 2-6 per 1,000 drive days, are almost always ECC-uncorrectable bit corruption, and retries rarely fix them.

- [fidelity] The quoted sentence itself hedges ('likely because'); the stronger 'almost exclusively' wording is in Sec. 3.1. Sec. 3's summary sentence calls uncorrectable errors the most common non-transparent type, so the paper is inconsistent on this point.
- [overreach] 'Almost always ECC-uncorrectable' is the authors' inference from the correlation with UE counts. 'Retries rarely fix them' holds by definition for final errors. The source's point is that read errors are rarely recovered by retry.
- [currency] The numbers come from the paper's text, but its own Table 2 differs: per drive, final read errors range from 10.9% (eMLC-A) to 62.7%, and per drive day from about 0.17 to 4.4 per 1,000. The 2-6 per 1,000 drive days matches the uncorrectable-error row better, and Sec. 11 attributes 2-6/1,000 to uncorrectable errors. Treat the ranges as approximate.

## 04-C10 - VERIFIED (3S/0R/0U)

In field data, uncorrectable flash errors are uncorrelated with the number of reads (correlation coefficients below 0.02), while correctable errors correlate strongly with reads (Spearman above 0.9). UBER, which is normalized by bits read, is therefore not a meaningful field metric.

- [overreach] The finding is per drive-month in Google's fleet. The source keeps the caveat that UBER may be meaningful in controlled experiments.

## 04-C11 - VERIFIED (3S/0R/0U)

At Facebook, 4.2%-34.1% of SSDs per platform reported SSD-uncorrectable (host-correctable) errors, with errors heavily concentrated: the top 10% of SSDs account for over 80% of the errors. No statistically significant dependence of failure rate on data read was found on the read-heavy platform.

- [overreach] The 'no dependence on reads' result is for Platform E only. Platform D was also read-heavy but was confounded by early-failure effects.
- [currency] The read-volume finding is reported specifically for Platform E (read-heavy, diverse utilization).

## 04-C12 - VERIFIED (3S/0R/0U)

NAND flash read disturb is a mechanism in which reading cells shifts the threshold voltages of other unread cells in the same block upward. Controllers mitigate it with read reclaim, using vendor-specified maximum read counts per block, and compensate voltage shifts with read-retry, which repeatedly rereads at different reference voltages and raises read latency.

- [fidelity] The source says 'some flash vendors' specify maximum read counts, so not all controllers rely on vendor limits. Read reclaim appears in the refresh discussion of Sec. 5.3 according to the claim's locator; in the text extraction it sits close to Sec. 5.4.
- [overreach] Only 'some' vendors specify maximum read counts. Read reclaim and read-retry are described as mechanisms that exist or have been proposed, not as something all controllers do. Read-retry compensates threshold shifts from all error types, not just read disturb. Upward shift is the general behavior, with an exception for the highest TLC state.
- [currency] 'Some flash vendors' specify a maximum read count; it is not a universal vendor specification.

## 04-C13 - VERIFIED (3S/0R/0U)

In Google's server fleet, DRAM errors, defined as bits read differently from how they were last written, occur at 25,000-70,000 FIT per Mbit. More than 8% of DIMMs are affected per year, and 1.3% of machines see uncorrectable errors per year.

- [fidelity] The FIT range describes mostly correctable errors. Elsewhere the paper gives 25,000-75,000 FIT per Mbit (Sec. 7 and the conclusions).
- [overreach] The FIT range is an average per-DIMM correctable-error rate, skewed by heavy-tailed DIMMs: the median is 778-25,000, and the conclusions state the range as 25,000-75,000. 'More than 8% of DIMMs' refers to correctable errors.

## 04-C14 - VERIFIED (3S/0R/0U)

At CERN, a write-then-read-back pattern probe on about 3000 nodes found 500 errors on 100 nodes in about 5 weeks, about 80% of them 64 KB-region corruptions. A check of file checksums found 22 mismatches in 33,700 files (about 1 in 1500), which shows that corruption got past the layered ECC/CRC protections without being reported.

- [fidelity] The source bases the statement 'protection mechanisms don't work 100%' on the disk probe (item 1), not on the file-checksum check: 'The fact that the disk probe reports regularly corruption errors as described in point 1 shows clearly...'. The claim should tie that inference to the probe.
- [overreach] The source bases the statement that 'the protection mechanisms don't work 100% / errors not reported' on the disk probe results (item 1), not on the CASTOR file-checksum check. The 22/33,700 figure is used to estimate a byte error rate (about 3e-7) for non-compressed files.
- [currency] In the document, the 'protection mechanisms don't work 100%' conclusion is drawn from the disk-probe results (item 1). It is not drawn from the file-checksum test.

## 04-C15 - VERIFIED (3S/0R/0U)

A model-checking analysis of parity-RAID protection designs, under single-error fault models (latent sector errors, corruption, torn, lost and misdirected writes), found flaws in every scheme examined. Outcomes were classed as data recovery, data loss (an error is reported) and corrupt data (returned undetected), and the analysis identified 'parity pollution'.

- [overreach] 'Every scheme' means every real-system scheme examined. The authors then construct a scheme that addresses all the issues found.

## 04-C16 - VERIFIED (3S/0R/0U)

In NetApp enterprise SSDs, 13.54% of replacements were due to lost writes. These are detected when a 4K WAFL block read from the SSD is inconsistent with its signature (attributes and version number), and the authors say it is unclear whether the drive or another layer is to blame.

- [fidelity] The source says 'somewhat less clear', which is a bit weaker than 'unclear'. The 13.54% is normalized on the assumption that the missing reasons are spread proportionately.
- [overreach] 13.54% is normalized on the assumption that the 40% of replacements with a missing reason are spread proportionately. The source says 'somewhat less clear', not that it is unknowable.
- [currency] 13.54% is the share of replacements that have a recorded reason type (40% are missing). It is not the share of all replacements.

## 04-C17 - VERIFIED (3S/0R/0U)

In accelerated aging of recordable optical discs, end of life is defined as the first uncorrectable error (CD E32 or DVD PO). The CD and DVD specifications allow no E32 or PO errors and cap BLER at 220 per second and PI Sum8 at 280.

- [fidelity] In practice the study tracks the maximum BLER/PI Sum8 as a stand-in for degradation rather than measuring the first E32/PO event directly.
- [overreach] The paper offers first uncorrectable error as a possible end-of-life definition but does not use it as its end-point. The accelerated-aging analysis tracks the maximum BLER (CD) and PI Sum8 (DVD) error rates as indicators.

## 05-C1 - VERIFIED (3S/0R/0U)

Under the fail-partial failure model, storage failures manifest in three ways: entire disk failure, block failure (latent sector errors), and block corruption; block corruption is silent: the storage subsystem returns bad data on a read with no error.


## 05-C2 - VERIFIED (3S/0R/0U)

The IRON taxonomy classifies a file system's failure policy by detection level (Zero, ErrorCode, Sanity, Redundancy) and recovery level (Zero, Propagate, Stop, Guess, Retry, Repair, Remap, Redundancy); R_Guess returns a guess at block contents that could be wrong while hiding the failure.


## 05-C3 - VERIFIED (3S/0R/0U)

In all four file systems tested (ext3, ReiserFS, JFS, NTFS), a misdirected or phantom write could yield a properly formatted but incorrect block that passed sanity checks and was used.

- [overreach] The evidence comes from type-aware corruption injection, not from reproducing actual misdirected or phantom writes. The authors themselves say NTFS testing was incomplete (closed source; "more thorough testing of NTFS is needed"). Wording like "would accept a well-formed but wrong block" is closer to what was shown than "a misdirected/phantom write yielded".

## 05-C4 - VERIFIED (3S/0R/0U)

A checksum stored together with the block it covers cannot detect lost (phantom) or misdirected writes: after a lost write the old data and old checksum remain consistent, so a later read verifies and returns stale data.

- [overreach] The source's condition is that data and checksum are written together in one disk request (block-level checksum). The claim should keep that condition; it was shown by model checking a single RAID stripe.
- [currency] For misdirected writes, cite Sec. 4.3 (Block checksums) as well as Sec. 4.4.

## 05-C5 - VERIFIED (3S/0R/0U)

Storage protection outcomes for an error fall into three classes: data recovery (detected and repaired), data loss (detected, not recoverable, error reported to user), and corrupt data (undetected, corrupt data returned to user); every examined real-world parity-RAID protection scheme had flaws under single-error conditions.

- [overreach] "Every examined scheme" means the published protection schemes as the authors modeled them, under one error per stripe; real systems may have unpublished protections.
- [currency] The paper says it evaluates 'approaches taken by a number of real systems', meaning published designs as modeled, not the deployed systems themselves. The claim's qualification already says this.

## 05-C6 - VERIFIED (3S/0R/0U)

In a 41-month study of 1.53 million production disks, 0.86% of nearline and 0.065% of enterprise-class disks developed at least one checksum mismatch, with over 400,000 mismatches in total, 8% found during RAID reconstruction.


## 05-C7 - VERIFIED (3S/0R/0U)

Different corruption classes are only visible at particular read points: checksum mismatches on any block read, identity discrepancies (from lost or misdirected writes) only during file-system reads, and parity inconsistencies only during scrubs; disk firmware has been observed acknowledging writes never written to stable media.

- [overreach] The read-point restrictions describe the studied NetApp system's detection mechanisms (RAID block checksum, file-system block identity, RAID parity scrub). They are not a general property of corruption classes, so the claim should be scoped to that system rather than stated as "different corruption classes are only visible...".

## 05-C8 - VERIFIED (3S/0R/0U)

Under disk-corruption fault injection, ZFS never returned bad data to the user because block-pointer checksums detected all corruptions; when all ditto copies were corrupt and no in-memory copy existed, ZFS reported an error instead of recovering.

- [fidelity] Locator should be Sec. 4.3 (On-disk data integrity), Observations 1 and 5; Sec. 5 is in-memory integrity.
- [overreach] The locator is wrong: these are Sec. 4.3 (disk corruption), not Sec. 5. The faults were random single-bit flips. Observation 5 is shown for file-system metadata such as directory ZAP blocks. Single-copy data blocks also give an error rather than recovery (Observation 3).

## 05-C9 - VERIFIED (3S/0R/0U)

ZFS verifies a block's checksum only when reading it from disk; later reads served from the page cache are not verified, so in-memory corruption is returned to readers, and corruption before flush gets a fresh checksum and later passes verification.

- [fidelity] Locator should be Sec. 5.3, Observations 1 and 3 (memory corruption), not Sec. 6.
- [overreach] The locator is Sec. 5 (memory corruption), not Sec. 6. The results come from injected single-bit flips into in-memory blocks in the OpenSolaris-era ZFS studied (the authors' "page cache" refers to that implementation's cache).
- [currency] The paper's 'page cache' is the ZFS ARC. The finding is about OpenSolaris-era ZFS. The claim gives no evidence for current OpenZFS releases, so treat it as historical unless checked again (inference).

## 05-C10 - VERIFIED (3S/0R/0U)

Error propagation in Linux 2.6 file systems and storage drivers is often incomplete: 1153 of 9022 error-propagating calls (13%) drop the error code, write errors are neglected more often than read errors, and all synchronous-read error codes were saved and checked (violations on reads were in readahead/async read).

- [overreach] The synchronous-read finding comes from Table 4, which covers read-type callees in file-system code only, not storage drivers. Both counts are static call-site counts. The paper is internally inconsistent: Table 4 shows 26 bad read calls while the caption and text say 29.
- [currency] Gives the exact version, Linux 2.6.15.4. The read/sync finding (Table 4) covers file-system code.

## 05-C11 - VERIFIED (3S/0R/0U)

ext4 (and XFS) have no user-data checksums and return a corrupted underlying block to applications without error, while btrfs and ZFS turn the same corruption into a read error; EIO on read from latent sector errors can happen on ext4, XFS, ZFS and btrfs.

- [overreach] These file-system behaviours are background statements that motivate the paper's fault model (emulated through errfs), not results measured on ext4, XFS, btrfs or ZFS. The source's example causes are lost or misdirected writes.

## 05-C12 - VERIFIED (3S/0R/0U)

Replicated distributed storage systems do not consistently use redundancy to recover from a single local file-system fault (corruption with zeros or junk, or EIO); a single fault can cause user-visible corruption, data loss or unavailability, e.g. RethinkDB silently returning corrupted data.


## 05-C13 - VERIFIED (3S/0R/0U)

After a failed fsync, ext4, XFS and Btrfs all mark the affected pages clean; ext4/XFS readers see the new (unpersisted) data while it is cached and the original on-disk contents after eviction, while Btrfs reverts the page so readers never see the failed write.

- [overreach] This was shown for a single injected data-block write failure. In some cases the behaviour differs: XFS shuts down and ext4/Btrfs remount read-only on certain metadata or journal block failures.

## 05-C14 - VERIFIED (3S/0R/0U)

Linux's generic writeback error tracking reports a writeback error to fsync on every file description open when the error occurred, and after reporting, later sync calls on the same descriptor return 0 unless new errors occur.

- [fidelity] Doc phrases the post-report behavior normatively ('should return 0').
- [overreach] The document states this as expected behaviour ("should") and as what the generic infrastructure provides. Filesystems opt in through mapping_set_error and file_check_and_advance_wb_err, so it is not a guarantee for every Linux filesystem.

## 05-C15 - VERIFIED (3S/0R/0U)

POSIX requires that after a successful write() to a regular file, any successful read() of the modified bytes returns the written data until they are modified again, and that unwritten parts before end-of-file read as zero bytes; EIO for a physical I/O error is only a 'may fail' condition for read().

- [fidelity] read()'s 'shall fail' list also contains an [EIO] entry for the background-process-group/orphaned case; the physical I/O error EIO is a 'may fail'.
- [currency] read() also has a mandatory EIO, but only for background process groups reading a controlling terminal. A physical I/O error is optional, as the claim says.

## 05-C16 - VERIFIED (3S/0R/0U)

Non-atomic appends can leave a file whose size was updated without its data reaching disk, so a post-crash read sees garbage; atomic appends are not provided by ext2 or by the writeback modes of ext3, ext4 and reiserfs.

- [overreach] The garbage state is a possible crash state, not an observed one, and the persistence-property results come from the empirical Block Order Breaker (BOB) tool, which is not exhaustive.

## 05-C17 - VERIFIED (3S/0R/0U)

The end-to-end argument holds that a function like reliable file transfer can be completely and correctly implemented only at the endpoints; lower-layer checks are at most performance enhancements, because data can be wrong on read from disk or corrupted during buffering.

- [overreach] The paper says an incomplete lower-level version "may be useful as a performance enhancement". It does not say lower-layer checks are "at most" that in every case. It is a design argument, with the communication system as the lower layer.
- [currency] The paper says the function needs the knowledge and help of the application at the endpoints, and that a lower-layer version 'may be useful as a performance enhancement'. That is weaker than 'at most performance enhancements'.

## 05-C18 - VERIFIED (3S/0R/0U)

btrfs checksums both data and metadata by default, computing checksums before writing and verifying them after reading from the device; an O_DIRECT buffer changed by user space before writeback ends can cause a data checksum mismatch.

- [fidelity] Current doc also mentions kernel 7.3 bouncing the direct IO buffer as a later mitigation.
- [overreach] Add the kernel 7.3 bounce-buffer mitigation to the applicability field. The O_DIRECT issue applies only to inodes that require data checksums (not NODATASUM).
- [currency] The claim's applicability note is out of date. The current doc says that from kernel 7.3 btrfs bounces the direct-I/O buffer for inodes with data checksums instead of falling back to buffered I/O. The 6.14 fallback is no longer the latest mitigation.

## 06-C1 - VERIFIED (3S/0R/0U)

For a single-writer safe register, a read not concurrent with any write returns the most recently written value, but a read overlapping a write may return any value in the register's domain, even one never written.


## 06-C2 - VERIFIED (3S/0R/0U)

A regular register restricts a read overlapping writes to the value before the first overlapping write or one of the values being written, yet permits two successive reads overlapping the same write to return new then old; an atomic register forbids this inversion.


## 06-C3 - VERIFIED (3S/0R/0U)

Sequential consistency requires only that the execution be equivalent to some single sequential order consistent with each processor's program order; it imposes no real-time ordering between processors.

- [overreach] State explicitly that 'no real-time ordering' is inferred from what the definition leaves out; Lamport does not say it directly.
- [currency] 'Imposes no real-time ordering between processors' is an inference from the definition. Lamport does not say it in the text.

## 06-C4 - VERIFIED (3S/0R/0U)

A history is linearizable iff, after possibly completing some pending operations, it is equivalent to a legal sequential history whose order respects the real-time precedence of non-overlapping operations; pending operations may already have taken effect.

- [fidelity] The definition reads 'extended (by appending zero or more response events)' and then restricts to complete(H'). Pending operations without an appended response are dropped.
- [overreach] More precisely: H is extended by appending responses for some pending invocations, and the pending invocations that remain are discarded (treated as not having taken effect).
- [currency] More exactly, H is extended by appending responses for some pending invocations, and the remaining pending invocations are then discarded via complete(H').

## 06-C5 - VERIFIED (3S/0R/0U)

Linearizability is a local property (a history is linearizable iff its projection on each object is), unlike sequential consistency and serializability.


## 06-C6 - VERIFIED (3S/0R/0U)

Under the Read Your Writes session guarantee, a read must be served by a server state that includes all prior writes of the session, but it is not guaranteed to return the session's previously written value because writes from outside the session may be visible.


## 06-C7 - VERIFIED (3S/0R/0U)

Monotonic Reads requires that the writes relevant to an earlier read in a session be contained in the database state of the server serving any later read in that session.


## 06-C8 - VERIFIED (3S/0R/0U)

Under the strict ANSI anomaly interpretations, a dirty read lets a transaction read a value that is later rolled back and thus never existed; Berenson et al. distinguish broad (P) phenomena that forbid possibly-anomalous histories from strict (A) anomalies.

- [currency] The 'never existed' wording comes from the ANSI English definition of P1 as restated in Sec 2.2. A1 (the strict anomaly) formalizes the case where T1 aborts and T2 commits.

## 06-C9 - VERIFIED (3S/0R/0U)

Read skew (A5A) occurs when a transaction reads x, another transaction updates x and y and commits, and the first transaction then reads y, observing an inconsistent state; Snapshot Isolation precludes A5A but admits write skew.

- [fidelity] Locator: A5A/A5B are defined in Sec. 4.2 (Snapshot Isolation) of the paper, not in Sec. 5. Sec. 5 is 'Summary and Conclusions'.
- [overreach] Read skew means T1 MAY observe an inconsistent state (relative to a constraint C() between x and y). The anomaly is the history pattern, not a guaranteed inconsistency.
- [currency] Locator: A5A and A5B are defined in Sec. 4 (4.1/4.2), not Sec. 5.

## 06-C10 - VERIFIED (3S/0R/0U)

Adya defines implementation-independent read phenomena G1a (a committed transaction read data written by an aborted transaction) and G1b (a committed transaction read a non-final version written by another transaction), which constrain only committed transactions.


## 06-C11 - VERIFIED (3S/0R/0U)

Eventual consistency constrains only convergence of replicas in the absence of further updates and gives no recency or ordering guarantee for reads.

- [fidelity] The clause 'in the absence of further updates' is not in the quoted sentence. It is standard framing, not text from the locator.

## 06-C12 - VERIFIED (3S/0R/0U)

Under Delta-atomicity a read may return either the value of the last preceding write or the value of a write that returned up to Delta time units ago; with Delta = 0 timed serial consistency is linearizable.

- [currency] This is secondary reporting of Golab et al. 2011. The survey notes that Golab et al. 2014 later proposed Gamma-atomicity as a more robust metric.

## 06-C13 - VERIFIED (3S/0R/0U)

Read-your-writes cannot be provided by a highly available system that must serve clients at any non-failing replica during partitions, but becomes achievable under sticky availability; no recency bound (including linearizability) is enforceable under an indefinitely long partition.

- [overreach] The impossibility applies to systems that stay available during the partition: 'recency bounds are not enforceable by HAT systems'. A system that gives up availability can still enforce linearizability.

## 06-C14 - VERIFIED (3S/0R/0U)

In Dynamo-style partial-quorum stores, staleness is probabilistic and measured empirically as small: production latency models showed consistent reads within tens of milliseconds, e.g., 1.85 ms vs 45.5 ms wait for 99.9% consistent reads after moving from spinning disks to SSDs.

- [fidelity] These results come from PBS modeling and Monte Carlo simulation on production latency distributions, not from direct staleness measurement in production.
- [overreach] Staleness was predicted via PBS Monte Carlo models fed with production latency distributions, not measured directly. The source says 'frequently within tens of milliseconds'. Some workloads (e.g. YMMR at R=W=1: 1364 ms t-visibility) need over a second. The 1.85/45.5 ms figures are specific to LinkedIn SSD vs disk at R=W=1.
- [currency] The figures come from PBS model predictions driven by production latency distributions, not direct empirical staleness measurements. The 1.85/45.5 ms example is in Sec. 1, not the abstract. An extended journal version also exists (VLDB Journal 2014).

## 06-C15 - VERIFIED (3S/0R/0U)

POSIX requires that after write() to a regular file returns successfully, any successful read() of each modified byte position returns the written data until modified again, and that read()/write() and related calls on regular files are all-or-nothing visible to each other across threads.

- [overreach] The atomicity rule covers 'the effects specified in POSIX.1-2017' for the functions listed in 2.9.7, on regular files and symbolic links. It is not general all-or-nothing visibility of every byte for every operation.
- [currency] Superseded: the current standard is IEEE Std 1003.1-2024 (Issue 8). There, XSH 2.9.7 no longer restricts the atomicity rule to regular files and symbolic links. It applies to file descriptors open to files in the file hierarchy, with an 'Except where specified otherwise' carve-out. Cite Issue 8, or note the change.

## 06-C16 - VERIFIED (3S/0R/0U)

NFSv4 does not offer POSIX-style immediate cross-client visibility: absent delegations, clients must revalidate cached data via the change attribute at OPEN and flush modified data before CLOSE, i.e., close-to-open semantics.

- [fidelity] The phrase 'close-to-open' does not appear in RFC 7530 Sec. 10.3.1. That label comes from RFC 8881, per the qualification.
- [overreach] RFC 7530 makes revalidation mandatory at least for OPENs with DENY=WRITE or BOTH, and optional for DENY=NONE opens. The 'close-to-open' label and the 'does not offer POSIX-style visibility' framing are inferences supported by RFC 8881 Sec 13.10 (NFSv4.1), not wording in RFC 7530.
- [currency] RFC 7530 requires revalidation at least at OPENs with DENY=WRITE or BOTH. Revalidating at every OPEN, including DENY=NONE, is optional ('Clients may choose ...'), so the rule is weaker than strict close-to-open at every open.

## 06-C17 - VERIFIED (3S/0R/0U)

Amazon S3 documents per-key strong read-after-write consistency and atomic single-key replacement: a GET concurrent with an overwrite returns either old or new data but never partial data, concurrent PUTs resolve by latest timestamp, and there is no cross-key atomicity.

- [currency] The page still says S3 'does not support object locking for concurrent writers'. S3 has since added conditional writes (If-None-Match/If-Match), which can serialize concurrent PUTs. The claim does not depend on this.

## 06-C18 - VERIFIED (3S/0R/0U)

Google Cloud Storage documents strongly consistent object read-after-write, but publicly readable cached objects may return stale data until their Cache-Control lifetime expires (default up to 60 minutes), and access grants/revocations are eventually consistent.

- [overreach] 'Default up to 60 minutes' applies only when no Cache-Control lifetime is specified for a publicly accessible object.

## 07-C1 - VERIFIED (3S/0R/0U)

HTTP range support is optional: a server may ignore Range and answer with a normal 200 full response, and even a 206 may contain only a subset of the requested ranges, so the client must inspect Content-Range to know what it received.

- [overreach] RFC 9110 says a 206 may carry 'a subset of the data requested', not only a subset of the requested ranges. So a single range can also come back partly filled. The RFC also says origin servers and caches 'ought to support byte ranges when possible'. Range support is optional, but the RFC encourages it.

## 07-C2 - VERIFIED (3S/0R/0U)

Clients cannot rely on receiving 416 for an unsatisfiable range; many servers return the full representation with 200 instead.


## 07-C3 - VERIFIED (3S/0R/0U)

If-Range lets a resuming reader avoid splicing bytes from different versions: if the validator does not match, the server sends the entire new representation instead of the range; weak entity tags are forbidden in If-Range.

- [overreach] The weak-ETag ban is a requirement on clients ('MUST NOT generate'). A server that receives one still applies strong comparison, which makes the condition false. If-Range also accepts an HTTP-date, but only when the client has no entity tag and the date is a strong validator.
- [currency] Strictly, the weak-ETag ban is a client generation requirement ('MUST NOT generate'). Separately, the server only sends the range when a strong comparison matches.

## 07-C4 - VERIFIED (3S/0R/0U)

In HTTP/1.1 a response with Content-Length is incomplete if fewer octets arrive; a close-delimited response (no Content-Length, no chunked) is considered complete unless the transport signals an error, so truncation can be undetectable at the HTTP layer.

- [overreach] Over TLS, the missing closure alert does let a client detect truncation of a close-delimited response. 'Undetectable at the HTTP layer' holds mainly for cleartext TCP, or when the client ignores incomplete-close signals.
- [currency] RFC 9112 is now updated by RFC 9931 (2026), but that update does not affect this claim.

## 07-C5 - VERIFIED (3S/0R/0U)

In HTTP/2 a mismatch between content-length and the sum of DATA frame payloads makes the response malformed, and clients must not accept it.

- [overreach] Responses defined as having no content are exempt: 204, 304 and responses to HEAD. The same section notes that endpoints which process messages progressively may already have acted on some data before they detect the malformation.
- [currency] Exception: responses defined to have no content (204, 304, HEAD) may carry a non-zero content-length.

## 07-C6 - VERIFIED (3S/0R/0U)

GET is safe and idempotent, so it may be retried automatically after a communication failure, but the retried response may differ from the original.

- [overreach] The RFC's permission to retry automatically covers a failure 'before the client is able to read the server's response'. The claim leaves out that condition. A mid-body failure during a streaming read is not spelled out, though a GET is still idempotent. Idempotence also covers only the effect the user requested; servers may still log requests or have other side effects.

## 07-C7 - VERIFIED (3S/0R/0U)

A cache must not deliver a partial response to a client without marking it 206, and may combine stored ranges only if they share the same strong validator.

- [overreach] Combining ranges also requires the cache to meet the client requirements in RFC 9110 Sec 15.3.7.3.

## 07-C8 - VERIFIED (3S/0R/0U)

An NFSv4.1 READ may legally return fewer bytes than requested with eof FALSE (a 'short read'), e.g. due to concurrent truncation, reduced transfer size or server resource exhaustion; reading at or past end-of-file returns NFS4_OK with zero bytes and eof TRUE.

- [overreach] The RFC's guidance that the client 'should send another READ' is a SHOULD-level recommendation. The listed causes are examples, not an exhaustive list.

## 07-C9 - VERIFIED (3S/0R/0U)

NFSv4.1 provides only close-to-open data cache consistency, and client cache validation must use the change attribute because time_modify changes only at time_delta granularity and can mark stale data valid.

- [fidelity] The exact locator is Section 13.10. Section 10.3.1 makes these rules apply only 'in the absence of an OPEN delegation'.
- [overreach] The claim leaves out conditions that matter. The rules in Sec 10.3.1 apply only without an OPEN delegation (Sec 10.4). Sec 10.3.2 adds flush and revalidate rules around byte-range locks, which give consistency stronger than close-to-open for locking clients. Say instead: 'absent delegations or locks, NFSv4.1 gives close-to-open semantics'. The quoted sentence comes from the pNFS Sec 13.10 context.
- [currency] The spec requires validation to include the change attribute, not to use it exclusively. Close-to-open applies absent delegations; byte-range locking (Section 10.3.2) gives further cache rules.

## 07-C10 - VERIFIED (3S/0R/0U)

In SMB2, if the underlying store returns fewer bytes than the client-specified MinimumCount, the server must fail the READ with STATUS_END_OF_FILE rather than return a short buffer.


## 07-C11 - VERIFIED (3S/0R/0U)

iSCSI signals a short data transfer in the SCSI Response via the Residual Underflow (U) flag with a Residual Count of bytes not transferred.

- [overreach] For a bidirectional command, the U/Residual Count gives the write residual. A read shortfall is signalled by the u flag (bit 4) and the Bidirectional Read Residual Count. Status and residual can also arrive in the final Data-In PDU with the S bit set, without a separate SCSI Response PDU.

## 07-C12 - VERIFIED (3S/0R/0U)

Amazon S3 GetObject on objects in Glacier Flexible Retrieval, Glacier Deep Archive or Intelligent-Tiering archive access tiers fails with InvalidObjectState (HTTP 403) until a copy is restored with RestoreObject.

- [currency] The HTTP 403 status is not stated on the cited GetObject page. It comes from the S3 error-code list, which could not be fetched to confirm (it redirects). Cite that list separately for the 403. The cited page also names both Intelligent-Tiering Archive Access and Deep Archive Access tiers.

## 07-C13 - VERIFIED (3S/0R/0U)

Amazon S3 states that single-key updates are atomic so a concurrent GET returns either old or new data but never partial or corrupt data, and reads started after a successful PUT response return the new data.


## 07-C14 - VERIFIED (3S/0R/0U)

Amazon S3 may return HTTP 503 slowdown responses at high sustained request rates (typically >5,000 requests/s to a small number of objects) and temporarily while it scales; clients are expected to retry with exponential backoff.


## 07-C15 - VERIFIED (3S/0R/0U)

Google Cloud Storage server-supplied checksums cover the complete stored object, so HTTP Range responses and decompressively transcoded downloads cannot be validated against them; gRPC ranged reads are the exception with per-chunk CRC32C.


## 07-C16 - VERIFIED (3S/0R/0U)

When GCS decompressive transcoding applies, a Range header is silently ignored and the entire object is served.


## 07-C17 - VERIFIED (3S/0R/0U)

Azure Storage uses snapshot isolation within a partition so reads concurrent with writes return a consistent snapshot, and the blob ETag changes on every write.

- [overreach] The guarantee holds 'within a single partition', and the claim text leaves that out. It applies to each read operation. Consistency across several separate ranged reads that span a write is not stated and needs If-Match on the ETag.
- [currency] The doc scopes snapshot isolation to reads concurrent with writes 'within a single partition'.

## 07-C18 - VERIFIED (3S/0R/0U)

Measured Internet traces showed TCP checksum failures between 1 in 1,100 and 1 in 32,000 packets despite link CRCs, with an estimated undetected-error rate of roughly 1 in 16 million to 10 billion packets, motivating application-level checksums.

- [overreach] The paper says 'some applications' should use application-level checksums. The undetected-error estimate covers data-bearing segments in four specific traces.
- [currency] The figures are dated (traces from 1998-2000). The conclusion section gives a looser 'between one packet in 10 billion and one packet in a few millions'.

## 08-C1 - VERIFIED (3S/0R/0U)

Avizienis et al. classify service failure modes along four viewpoints: failure domain, detectability, consistency, and consequences.

- [overreach] In the TR PDF the passage sits just above the page-13 footer, so the locator is about p.12-13.

## 08-C2 - VERIFIED (3S/0R/0U)

In the failure-domain viewpoint, content failures and timing failures (early or late) are distinct. When both content and timing are wrong, the failure is a halt (with silent failure as a special case) or an erratic failure.


## 08-C3 - VERIFIED (3S/0R/0U)

Avizienis et al. call a failure signaled when detecting mechanisms raise a warning signal, and unsignaled otherwise. The detectors themselves can fail in two ways: false alarm or unsignaled failure.


## 08-C4 - VERIFIED (3S/0R/0U)

Inconsistent failures, where different users perceive incorrect service differently and some may perceive correct service, are what Avizienis et al. identify with Byzantine failures. The consistency viewpoint applies only when a system has two or more users.

- [currency] The paper says inconsistent failures are 'usually called' Byzantine failures, following Lamport et al., which is a naming convention rather than the authors' own identification.

## 08-C5 - VERIFIED (3S/0R/0U)

In Avizienis et al.'s definition, 'fail-stop' (fail-halt) systems fail only by halting 'to an acceptable extent'. This is a probabilistic design target, not an absolute property.

- [fidelity] The phrase 'probabilistic design target' is the reviewer's interpretation of 'to an acceptable extent'. It should be labeled as inference.
- [overreach] Calling it a 'probabilistic design target, not an absolute property' is the reviewer's inference. The text says 'to an acceptable extent' and frames fail-controlled systems as a design and specification goal, but it never uses the word 'probabilistic' about fail-halt. Label the second sentence as inference.
- [currency] 'Probabilistic design target' is the claimant's reading. The paper says 'to an acceptable extent' and does not use the word probabilistic in this definition, so label this as inference.

## 08-C6 - VERIFIED (3S/0R/0U)

Avizienis et al. call faults whose activation is not systematically reproducible elusive (soft) faults. Elusive development faults and transient physical faults are grouped as intermittent faults, whose errors are termed soft errors.


## 08-C7 - CONTESTED (2S/1R/0U)

Two processors reading the same nonfaulty input while it changes can obtain different values, and a faulty input can be interpreted differently by different readers. Only agreement among the readers, not a hardware fix such as reading the same wire, can guarantee that they use the same value.

- REFUTE [overreach] I checked Lamport, Shostak and Pease (1982) §6, p.397. The text does say a nonfaulty input read while it is changing can give different values. But for that case it says: 'This can only be prevented by synchronizing the reads with the advancing of the clock.' The 'no way to guarantee ... except by having the processors communicate among themselves to solve the Byzantine Generals Problem' sentence is restricted to 'a possibly faulty input device' (the marginal-signal-on-the-same-wire case). The claim drops that condition and extends the only-agreement conclusion to the nonfaulty changing-input case, where the source names read synchronization as the remedy.
- [fidelity] The claim that only agreement can guarantee the same value applies to a possibly faulty input. For a nonfaulty but changing input, the paper's remedy is to synchronize the reads with the change.
- [overreach] For a nonfaulty input that changes during the read, Lamport says synchronizing the reads with the change prevents the divergence. Only for a possibly faulty input (e.g. a marginal signal on a shared wire) does agreement among the readers (a Byzantine Generals solution) become the only guarantee that they use the same value, and even then not that the value is correct.
- [currency] The 'only agreement' statement covers a possibly faulty input device. For a nonfaulty input read while it changes, the paper says the discrepancy 'can only be prevented by synchronizing the reads' (p.397). It also notes that median-based majority keeps values within the input's range (p.398).

## 08-C8 - VERIFIED (3S/0R/0U)

Schneider defines a fail-stop processor by three properties: Halt on Failure, Failure Status, and Stable Storage. Under the last, stable storage contents are unaffected by any failure and can always be read by any processor, while volatile storage is lost.


## 08-C9 - VERIFIED (3S/0R/0U)

Lampson and Sturgis model a disk read Get as returning (good, data) or looksBad. A soft read error (good page, looksBad) is an expected error. A persistent read error (nR successive looksBad within TR) and an undetected error (bad page reported good, or wrong data reported good) are disasters, outside the guarantee.

- [overreach] A soft read error counts as an expected error only while it stays within the nR/TR bound. Beyond that bound it becomes the persistent-read-error disaster.
- [currency] Footnote 1 says the paper was 'circulated in several drafts, but it was never published'. Much of its material appeared in LNCS 105 (Springer, 1981). Cite it as an unpublished 1979 Xerox PARC manuscript, with LNCS 105 as the published version.

## 08-C10 - VERIFIED (3S/0R/0U)

Lampson and Sturgis's CarefulGet retries Get up to n times, n being the bound on soft read errors, and so eliminates soft read errors. StableGet reads a second, non-decay-related careful page if the first is bad, giving clients stable storage with no failure modes to handle, absent disasters.

- [overreach] StableGet alone does not give the guarantee. The two-page invariant also needs StablePut's ordered CarefulPuts and the Cleanup action, run after every crash and at least every unit decay time TD. Without Cleanup, two decays could leave both pages bad.

## 08-C11 - VERIFIED (3S/0R/0U)

The fail-partial disk model has three manifestations: entire disk failure (classic fail-stop if permanent), block failure (latent sector errors), and block corruption, which is silent because the subsystem returns bad data on a read. Failures may be sticky or transient.


## 08-C12 - VERIFIED (3S/0R/0U)

Fault injection showed that commodity file systems (ext3, ReiserFS, JFS, NTFS) handle read failures and corruption with 'illogical inconsistency'. For example, JFS reads the alternate superblock on a read failure of the primary but not when it deems the primary corrupted.

- [fidelity] Figure 2, which the inconsistency finding points to, covers ext3, ReiserFS and JFS. NTFS was analyzed separately and less fully.
- [overreach] The paper criticizes undesirable, likely unintentional inconsistency. It notes that some logical inconsistency, such as extra redundancy for important structures, could be good.

## 08-C13 - VERIFIED (3S/0R/0U)

Huang et al. define gray failure as differential observability: a system experiences gray failure when at least one app observes it as unhealthy while the system's observer considers it healthy. Crash and fail-stop failures fall in the quadrant where both observe failure.


## 08-C14 - VERIFIED (3S/0R/0U)

In 101 fail-slow hardware incident reports from 12 institutions, fail-stop, fail-partial and fail-transient faults converted into fail-slow faults. Masking by retry or remapping becomes a 'double-edged sword' when transient failures recur frequently.

- [fidelity] In §3.2 the masking mechanisms named for the double-edged-sword point are retry and repair (ECC/parity). Remapping of bad sectors comes up under the fail-partial conversion, not under the double-edged-sword sentence.
- [overreach] The paper says these faults 'can convert', with examples. It does not say every such fault converted.
- [currency] An extended version was published in ACM Transactions on Storage (2018). The FAST'18 paper is still a valid citation.

## 08-C15 - VERIFIED (3S/0R/0U)

Gunawi et al. report that SSD reads on worn flash may need repeated retries at different voltage thresholds, with up to 4 retries observed in the field. Pages failing ECC are reconstructed via RAIN with N-1 extra reads, which turns read errors into read latency.

- [overreach] 'Turns read errors into read latency' paraphrases the paper's fail-slow framing rather than quoting it. The paper adds that the N-1 reads may themselves retry, and that LDPC in TLC SSDs lengthens reconstruction.
- [currency] 'Turns read errors into read latency' is a fair inference from the fail-slow framing, but it is not the paper's wording.

## 08-C16 - VERIFIED (3S/0R/0U)

Gunawi et al. classify fail-slow symptoms into four kinds: permanent slowdown, transient slowdown, partial slowdown, and transient stop. Time to detect was minutes in 1% of cases, hours in 13%, days in 13%, weeks in 11%, months in 17%, and unknown in 45%.

- [overreach] The percentages describe the 101 collected reports, not a field-wide rate.

## 08-C17 - VERIFIED (3S/0R/0U)

For reads, the same underlying block corruption reaches applications differently depending on the local file system: ext4 returns corrupted data as-is, while btrfs and ZFS convert it to an I/O error. Lost or misdirected writes can make reads return zeros or junk without any error on file systems without user-data checksums.


## 08-C18 - VERIFIED (3S/0R/0U)

Across eight replicated storage systems, a single file-system fault (a corruption or read/write error on one block of one node) could cause data loss, corruption or unavailability. Redundancy was not consistently used to recover.

- [fidelity] The fault model also includes space errors (ENOSPC/EDQUOT), not only corruption and read/write errors.
- [overreach] These outcomes were observed across the eight systems collectively. Not every system showed every outcome. The fault model also covers space errors (ENOSPC/EDQUOT).
- [currency] The results apply only to the 2016-era versions tested. An extended version appeared in ACM Transactions on Storage (2017), and later releases may behave differently.

## 09-C1 - VERIFIED (3S/0R/0U)

In large fan-out services, component tail latency is amplified at the service level: in a measured Google service the 99th-percentile latency for one leaf request was 10ms while the 99th-percentile latency for all leaf requests to finish was 140ms.

- [fidelity] The paper measures the 10ms figure 'for a single random request to finish, measured at the root'. It does not say per leaf. The same passage also gives 70ms for 95% of requests to finish.

## 09-C2 - VERIFIED (3S/0R/0U)

Issuing a hedged duplicate read after a short delay sharply cuts tail latency at small extra load: for a BigTable read of 1,000 keys over 100 servers, hedging after 10ms reduced 99.9th-percentile latency from 1,800ms to 74ms with 2% more requests.

- [overreach] These numbers come from one Google benchmark, and the source warns that naive hedging adds unacceptable load. 'At small extra load' holds for the deferred-hedge variant, not for hedging in general.

## 09-C3 - VERIFIED (3S/0R/0U)

In a field study of 458,482 disks and 4,069 SSDs, a drive was at least 2x slower than its RAID-group peers' median in about 0.2% (disk) and 0.6% (SSD) of drive hours, and RAID groups had at least one such slow drive 1.5% and 2.2% of the time.

- [fidelity] The paper says 'more than 2x slower', not 'at least 2x'.
- [overreach] The source says 'more than 2x' (Si >= 2 against the RAID-group median), measured in hourly drive and RAID hours, in one vendor's (NetApp) customer deployments.
- [currency] The source wording is 'more than 2x slower'. The metric is Si>=2, so 'at least 2x' also fits.

## 09-C4 - VERIFIED (3S/0R/0U)

Drive slowdowns are mostly not explained by workload imbalance and are usually not accompanied by any drive-reported event (they are 'silent').

- [overreach] 'Workload imbalance' here means only I/O size or rate imbalance as measured hourly.

## 09-C5 - VERIFIED (3S/0R/0U)

Slowdowns persist and recur: 40% of slow disks and 35% of slow SSDs remain unstable for more than one hour, and 90%/85% of slowdowns recur on the same day as the previous occurrence.


## 09-C6 - VERIFIED (3S/0R/0U)

Hardware can be 'fail-slow' (functional but degraded), and masking of frequent transient errors via retry/ECC/repair turns error handling cost into the normal-case latency.

- [overreach] The source talks about common-case 'performance' (throughput or latency), and only when the errors are frequent. The evidence is anecdotal reports from 101 incidents.
- [currency] The section is titled '3.2 Fault Conversions to Fail-Slow'. 'Fail-transient to fail-slow' is a bullet within it.

## 09-C7 - VERIFIED (3S/0R/0U)

SSD reads of worn or corrupted pages incur extra latency from read retries at different voltage thresholds and, if ECC fails, RAIN reconstruction requiring N-1 additional reads; up to 4 retries were observed in the field.


## 09-C8 - VERIFIED (3S/0R/0U)

Under background write load, SSD garbage collection blocks reads: in simulation with 5K writes/s noise reads were 15x, 19x and 96x slower than no-GC at the 90th, 95th and 99th percentiles, and larger reads suffer disproportionately because any GC-blocked page stalls the whole read.

- [overreach] The section-2 motivating measurements (15x/19x/96x) were taken on a real Samsung SM951 SSD, not in simulation. Simulation and emulation (SSDSim, VSSIM++) were used only to evaluate TTFLASH. The claim's 'in simulation' and the 'not measured on commercial firmware' qualification are wrong for these numbers. The mechanism and the numbers are correct.

## 09-C9 - VERIFIED (3S/0R/0U)

On drive-managed SMR disks, a logically sequential read of a region partially overwritten (newer copies in the persistent cache) is physically fragmented: the head seeks to the cache and back, so read latency depends on write history.

- [overreach] This applies to drive-managed SMR with a disk-based persistent cache. 'Read latency depends on write history' is a fair inference, but it is not the paper's wording.

## 09-C10 - VERIFIED (3S/0R/0U)

Disk read service time is dominated, for modeling accuracy, by the drive's caching/read-ahead behavior: ignoring it gave a 112% relative demerit versus 20% for the transfer model and 9% for seek/head-switch costs; a constant-time model is off by 35% of mean I/O time.

- [fidelity] The demerits apply to modeling overall I/O time across traced workloads (reads and writes), not read service time specifically. 'Dominated' overstates it: the paper calls caching 'the most important feature to model'.
- [overreach] Read this as 'the most important feature to model'. The 112% comes from a different drive (HP 97560, with read-ahead and immediate reporting of writes) than the 20%/9% figures (C2200A, no cache). It covers all I/Os in the traces, not reads alone, on early-1990s HP drives.
- [currency] The figures come from different drives: the 35% constant-model demerit is for the HP C2200A and the 112% no-caching demerit is for the HP 97560. 'Dominated' is the reviewer's paraphrase of 'most important feature to model'.

## 09-C11 - VERIFIED (3S/0R/0U)

Disk read-ahead is a policy trade-off: it lets sequential reads run at full bandwidth but aggressive read-ahead delays unrelated random reads because head/track switches cannot be aborted; drive read-cache behavior on partial hits is poorly specified.


## 09-C12 - VERIFIED (3S/0R/0U)

POSIX aio_read returns once the request is queued, not when data is delivered; errors may surface either synchronously at call time or later as the operation's error status, which reads EINPROGRESS until completion, and cancellation yields ECANCELED.

- [fidelity] ECANCELED applies specifically to an explicit aio_cancel() request.
- [overreach] 'Not when data is delivered' is too strong: the standard only requires a return once the request is queued or initiated. ECANCELED is specified for an explicit aio_cancel() request.

## 09-C13 - VERIFIED (3S/0R/0U)

In Linux io_uring, read completions are unordered relative to submission order, per-request errors are delivered in the completion queue entry rather than the syscall, and a linked timeout cancels a read that does not complete in time (-ETIME on the timeout).

- [overreach] The link timeout only attempts cancellation (-ETIME means 'attempted canceled'). The same man page says disk I/O already started cannot be cancelled, so a timed-out disk read may still run to completion. Completions are unordered unless links or drain are used.

## 09-C14 - VERIFIED (3S/0R/0U)

On Windows, a read on a handle opened for overlapped I/O may complete synchronously (e.g., cache hits, NTFS compression/encryption, cache-manager saturation), so applications must handle both synchronous and asynchronous completion; ERROR_IO_PENDING is not a failure.


## 09-C15 - VERIFIED (3S/0R/0U)

Linux readahead/posix_fadvise access-pattern hints are non-binding: readahead only avoids blocking if issued early enough and pages are not evicted, may itself block on metadata, and POSIX_FADV_RANDOM disables readahead while POSIX_FADV_SEQUENTIAL doubles the window.

- [overreach] The man page says 'not binding' only for posix_fadvise. The window effects are Linux-specific and apply to the whole file, not just the advised range.

## 09-C16 - VERIFIED (3S/0R/0U)

In the Linux SCSI midlayer a timed-out command (e.g., a read) is aborted and then either retried, if retries remain, the device is still online and REQ_FAILFAST is not set, or terminated with DID_TIME_OUT; a driver may instead extend the timer.

- [fidelity] The online/REQ_FAILFAST conditions come from the EH completion path (§2.1, scsi_eh_flush_done_q), not the §1.3 async-abort sentence, which conditions only on retries. The claim merges the two paths.
- [overreach] The claim mixes two paths. The retry-or-DID_TIME_OUT outcome needs the async abort to succeed. If it fails, or is not scheduled (abort already tried, retries exhausted, EH deadline expired), the command enters full SCSI EH, which can escalate to device, bus or host resets and offlining. The online/REQ_FAILFAST conditions belong to that EH path.
- [currency] The claim merges two paths. After a successful async abort, the doc's only stated condition is retries not exhausted. The online and REQ_FAILFAST conditions belong to the full EH path (section 2.1), which runs if the abort fails or is not attempted. That path covers both retries and error completion, not only DID_TIME_OUT.

## 09-C17 - VERIFIED (3S/0R/0U)

Objects in S3 Glacier Flexible Retrieval / Deep Archive cannot be read directly: GetObject returns InvalidObjectState (HTTP 403) until a temporary restored copy exists, and restore typically takes 1-5 minutes (Expedited, <250MB) to 3-5 hours (Standard) or up to 12/48 hours for Deep Archive.

- [overreach] These are 'typically' figures. Expedited is not offered for Deep Archive. Bulk is 5-12 h for Flexible Retrieval. Objects over 5 TB take longer (a 50 TB object can take up to 48 h), and Expedited requests may be refused without provisioned capacity.
- [currency] The source wording for Expedited is objects 'under 250 megabytes'. Flexible Retrieval Bulk (5-12 hours) is omitted.

## 09-C18 - VERIFIED (3S/0R/0U)

An Azure blob in the archive tier is offline and unreadable until rehydrated to an online tier; standard-priority rehydration may take up to 15 hours (objects <10 GB), high priority under one hour, cannot be cancelled once started, and the blob's tier remains archive during rehydration.

- [fidelity] The non-cancellation and 'tier remains archive' statements are stated for the Set Blob Tier method specifically.
- [overreach] The timelines are hedged with 'might', and high priority can exceed one hour. The no-cancel rule is stated for Set Blob Tier. With Copy Blob, the source stays archived and the new copy shows tier 'archive' until done. The 10 GiB/hour account-level limit stretches bulk timelines.
- [currency] The non-cancellation statement is made for Set Blob Tier rehydration specifically. For Copy Blob, the source blob is unchanged and the destination blob's tier shows archive until the copy completes.

## 10-C1 - VERIFIED (3S/0R/0U)

Below channel capacity, coding can make the frequency of errors arbitrarily small, but not zero. The result is asymptotic and shows only that such a code exists. Above capacity, no encoding gets the equivocation below H - C.

- [fidelity] Shannon does not say 'but not zero'; that wording is the reviewer's gloss on 'arbitrarily small'. Also, the H − C bound applies when H > C. §14 calls the proof 'not a pure existence proof' but says it 'has some of the deficiencies of such proofs'.
- [overreach] 'But not zero' is our inference. Shannon only says 'arbitrarily small' and never says zero error is impossible; some channels, e.g. noiseless ones, can reach zero error. It should read 'arbitrarily small (Theorem 11 does not promise zero)'. Also, Shannon calls his demonstration 'not a pure existence proof' that still shares the deficiencies of one. The theorem's condition is H ≤ C (entropy rate against capacity).
- [currency] Small precision points. Shannon's condition is H ≤ C ('at or below capacity'). Above capacity he says the equivocation can be brought down to H − C + ε, but never below H − C. On p.? (line ~1496) Shannon calls the demonstration 'not a pure existence proof' but says it has the same deficiencies as one.

## 10-C2 - VERIFIED (3S/0R/0U)

In the binary erasure channel, the receiver gets a distinct symbol '?' in place of the bit, so the position of the loss is known. Its capacity is exactly 1 - f. In the binary symmetric channel, a flipped bit gives no such marker.

- [currency] The locator heading should be §9.3 'Noisy channels' (the list 'Some useful model channels' sits inside it). The quoted sentence is in the solution to exercise 9.13, not the main text.

## 10-C3 - VERIFIED (3S/0R/0U)

A deletion channel is different from an erasure channel: the receiver gets no sign of which bits were deleted. The capacity of the i.i.d. binary deletion channel has no known closed form. It is known to be at least (1 - p)/9.

- [overreach] 'No known closed form' was true as of the 2009 survey, which also says there was no efficient numerical method. It should be dated.
- [currency] Say that the (1 − p)/9 bound is current as of 2009. Later papers may have tightened the bounds on deletion-channel capacity; this check did not look at them.

## 10-C4 - VERIFIED (3S/0R/0U)

Synchronization-error channels (insertions, deletions, timing errors) are poorly understood in theory. In practice, synchronization is handled by timing recovery separate from coding, not by codes.

- [fidelity] The survey says synchronization was handled separately 'in the past' and that 'this may be changing'. 'Not by codes' overstates the survey's 'rarely if ever'.
- [overreach] The source puts the separate timing recovery 'in the past' and says coding is 'rarely if ever' used for synchronization. That is not an absolute 'not by codes'. It also notes that codes for synchronization 'have been suggested for disk drives' and that this 'may be changing'. The claim should be dated to 2009 and softened to 'rarely'.
- [currency] The source puts the timing-recovery point in the past tense ('In the past ... has been handled separately') and says 'this may be changing'. The present-tense claim describes things as of 2009 and should say so.

## 10-C5 - VERIFIED (3S/0R/0U)

For a bounded-distance decoder, reading a codeword has three outcomes: correct decoding (at most t errors), decoder failure (no codeword found, so the failure is detected), and decoder error (a different codeword is found, so the error is undetected). If the error count is more than t but less than d - t, the result is always failure.

- [fidelity] 'Detected' and 'undetected' are the reviewer's labels, though they match the report's usage ('probability of undetected word error').
- [overreach] The source assumes 2t < d − 1. Calling a failure 'detected' and an error 'undetected' is the standard reading, which §I supports.
- [currency] The paper assumes 2t < d − 1 (OCR shows 'It < d - 1'). The terms 'detected' and 'undetected' are the claim's gloss; the paper speaks of 'undetected word error'.

## 10-C6 - VERIFIED (3S/0R/0U)

For an MDS code such as Reed-Solomon, used with a bounded-distance decoder on a channel where all error patterns of the same weight are equally likely, the conditional probability of decoder error given more than t errors is less than 1/t!. For the (255,223) Voyager code it is below 3e-14.

- [fidelity] The 1/t! bound needs code length n ≤ q − 1. The abstract states it for 'a t error-correcting Reed-Solomon code of length q - 1 over GF(q)', and eqs. (9)/(10) carry the condition n ≤ q − 1. The claim leaves this condition out.
- [overreach] The simple 1/t! bound needs n ≤ q − 1 (e.g. RS length q − 1) as well as MDS + bounded-distance + equiprobable error patterns of each weight. For a general MDS code, the source's main result is the sharper Q'-type bound (eq. 7-8), not 1/t!.
- [currency] The simple 1/t! form (eq. 9, Appendix) needs n ≤ q − 1, which is true for RS codes of length q − 1. Strictly, the bound is for u ≥ d − t errors; for t < u < d − t, PE = 0. So it is not a bound that holds for every MDS code without conditions.

## 10-C7 - VERIFIED (3S/0R/0U)

Iterative LDPC decoding (halting when all checks pass) separates detected errors, where the maximum number of iterations is reached without a valid decoding, from undetected errors, where a valid codeword is found that is not the true one. A fixed-iteration practice blurs this distinction.

- [overreach] MacKay attributes the fixed-iteration practice to the turbo-code community. It is his recommended procedure for Gallager/LDPC simulation; he does not describe it as flash controller practice.

## 10-C8 - VERIFIED (3S/0R/0U)

A CRC's Hamming distance (HD) at a given data-word length is the minimum number of bit inversions that can give an undetected error. HD depends on the polynomial and the length. At 48 bits, CCITT-16 (0x8810) gives only HD=4, while 0xC86C gives HD=6.

- [overreach] HD here is measured for random independent errors on a BSC, which is the paper's chosen metric.
- [currency] 0x8810 and 0xC86C are in Koopman's implicit-+1 notation, not the conventional polynomial form. Koopman's later online CRC zoo tables update and extend these results.

## 10-C9 - VERIFIED (3S/0R/0U)

The common assumption that an r-bit check has undetected-error probability at most 2^-r does not hold for many shortened cyclic codes. The T10 data-integrity 16-bit CRC (0x18BB7) was chosen because it is a 'proper' code, with Pud(N,p) ≤ Pud(N,0.5) for all p ≤ 0.5.

- [currency] This is an INCITS T10 committee working document (r0), not the ratified standard. The polynomial was adopted as the PI guard CRC in SBC-2/SBC-3 and later, and is usually written 0x8BB7 (CRC-16/T10-DIF). The doc also justifies the choice by burst-error behaviour.

## 10-C10 - KILLED (0S/3R/0U)

In storage erasure coding, a sector whose embedded correction information is exceeded is seen by the storage system as an erasure, meaning its location is known. Erasure codes can be more powerful than ECCs for silent corruption because the location of the failure is known.

- REFUTE [fidelity] Plank ;login: primer, Introduction: the first quote is verbatim, so the first sentence of the claim is supported. The second sentence misstates the source. Plank contrasts erasures with communication errors 'when bits are corrupted silently in a message. This differs from an erasure, because the location of the corruption is unknown. The fact that erasures expose the location of the failure allows for erasure codes to be more powerful than ECCs'. He does not say erasure codes are more powerful 'for silent corruption'. Silent corruption is exactly the unknown-location case that erasure codes do not address.
- REFUTE [overreach] Plank ;login: primer, Introduction: 'when too many bits are flipped ... the storage system sees this as an erasure'. That part is supported. But Plank contrasts silent corruption in communications ('the location of the corruption is unknown') with erasures. He says 'erasures expose the location of the failure', which 'allows for erasure codes to be more powerful than ECCs'. He also notes that disk sectors can become 'silently corrupted'.
- REFUTE [currency] Plank, ;login: 38(6) Dec 2013, Introduction. The first sentence is supported: a sector whose ECC is exceeded is seen 'as an erasure: the storage is gone!'. The second sentence turns the source around. Plank says that in communications, errors are bits 'corrupted silently', which 'differs from an erasure, because the location of the corruption is unknown'. He then says 'erasures expose the location of the failure', which 'allows for erasure codes to be more powerful than ECCs'. So the advantage applies to erasures, whose location is known, not to silent corruption.
- [fidelity] Plank says erasure codes can be more powerful than ECCs because erasures expose the failure's location. Silent corruption, where the location is unknown, is the error (ECC) case, not the erasure case.
- [overreach] The second sentence turns the source around. Erasure codes are more powerful than ECCs because they handle erasures, whose location is known. Silent corruption has an unknown location, so the advantage does not apply to it. The claim should read: 'Erasure codes can be more powerful than ECCs because erasures expose the failure location; silent corruption, whose location is unknown, is the ECC problem, not the erasure problem.'
- [currency] Fix the wording: 'Erasure codes can be more powerful than ECCs because erasures expose the location of the failure. Silent corruption, where the location is unknown, is the ECC (error-correction) problem, not the erasure problem.'

## 10-C11 - VERIFIED (3S/0R/0U)

PMDS codes are designed under an explicit assumption: a sector hard error (internal ECC exceeded) is a detected erasure. The authors also say that sector ECC can miscorrect and is usually reinforced by a CRC, and that hard errors are silent until the sector is accessed.

- [fidelity] The paper says the ECC's own detection 'may not be sufficient, hence it often needs to be reinforced by the CRC'. That is 'often', not 'usually'.
- [overreach] The source says hard errors occur 'mainly' when ECC is exceeded and that ECC is 'normally' or 'often' reinforced by a CRC. Those are hedged statements, not universal ones.
- [currency] The v2 arXiv version (2014) came after the 2013 journal publication, so cite the IEEE TIT version as the version of record.

## 10-C12 - VERIFIED (3S/0R/0U)

Windows Azure Storage treats an offline fragment, and a read that looks like it will take too long, as an erasure. It reconstructs the data from other fragments and returns whichever result arrives first. Its LRC can decode every failure pattern that is information-theoretically decodable (the Maximally Recoverable property).

- [fidelity] The MR text is in §2.2 (Fault Tolerance), not just §2 generally.
- [overreach] The slow read is handled by a parallel reconstruction while the original read continues ('effectively treating' the node as offline). It is not purely an erasure. MR comes from the specific choice of coding coefficients for the (6,2,2) LRC and its family.
- [currency] The source says WAS treats the slow node 'as if it was offline'. Calling that an 'erasure' is the claim's reading, which is reasonable but not the source's word. The MR guarantee is stated for the coding-equation design, for example (6,2,2).

## 10-C13 - VERIFIED (3S/0R/0U)

In LDPC-based SSDs, a read first uses hard-decision sensing and decoding, and uses soft-decision sensing only if hard decoding fails. Sensing latency grows linearly with the number of quantization levels, so the effort to decode a read shows up as read latency.

- [overreach] The hard-then-soft sequence is the paper's baseline design ('our basic structure'), not a general property of LDPC SSDs. The paper's own look-ahead technique starts soft sensing before hard decoding finishes. It should read 'in the baseline LDPC-SSD design described by Zhao et al.'
- [currency] The two-step flow is what the paper calls 'our basic structure for LDPC-based SSDs', i.e. the authors' model, not a survey of shipping controllers. The paper then proposes progressive sensing to cut the latency overhead, so the claim describes the baseline it improves on.

## 10-C14 - VERIFIED (3S/0R/0U)

Flash read-retry re-reads with different read reference voltages until ECC succeeds or the available voltages run out. If retry, NAC and superpage parity recovery all fail, the controller reports an uncorrectable error to the host. Retry can significantly increase read latency.

- [overreach] §6.1 calls this 'an example flow' and says 'many controllers' invoke read-retry. It is illustrative, and the order and steps vary by controller. The retry limit is a controller parameter.
- [currency] In §6.1 the flow is specific to BCH (Algorithm 1). The LDPC flow in §6.2 differs, with soft decoding steps.

## 10-C15 - VERIFIED (3S/0R/0U)

In a DNA storage channel, the input is an unordered multiset of molecules and the output is independent sampling followed by insertions, deletions and substitutions. Experiments show that errors within molecules come mainly from synthesis and sequencing, while handling and storage cause whole-sequence loss.

- [overreach] The multiset/sampling channel is described as 'a good abstraction' of the system, not as a measured fact. The conclusion also credits decay with a smaller share of within-molecule errors. Handling and storage cause 'a significant loss of sequences', not all of it.
- [currency] The source says 'multiset' and that the molecules are 'stored in an unordered way'. It also says DNA data is read 'by sampling', so the read output is sampled, not the whole pool. Cite Sci. Rep. 9:9663 (2019) as the version of record.

## 10-C16 - VERIFIED (3S/0R/0U)

Enterprise HDD vendor specs state the non-recoverable read error rate as a sector event per bits read (1 sector per 10E15), with no stated test method and no undetected-error rate.

- [fidelity] The data sheet has three wordings, not one: '1 sector per 10E15', '<1 in 10E15' and, for some SAS models, 'Non-recoverable Read Errors per Bits Read, Max 1 per 10E16'. Generalizing to 'enterprise HDD vendor specs' goes beyond this single Seagate document.
- [overreach] This is one Seagate data sheet, not 'enterprise HDD vendor specs' in general. Even within it, the 10K/15K performance models give '1 per 10E16, Max' without 'sector'. The claim should be limited to the Exos nearline models in this sheet.
- [currency] The same document is not uniform. Some SAS models (pp. ~9-10, the 2.5-inch/10K family) list 'Non-recoverable Read Errors per Bits Read, Max 1 per 10E16'. So 'vendor specs state 1 sector per 10E15' should be qualified: the figure and its wording vary by model (1 sector per 10E15, <1 in 10E15, max 1 per 10E16).

## 11-C1 - VERIFIED (3S/0R/0U)

Intel MCA defines an SRAR (software recoverable action required) uncorrected recoverable error as one detected and raised at the point of consumption in the execution flow, which software must handle before scheduling another stream of execution on that processor. Shutdown is recommended if no address is logged.

- [fidelity] The shutdown recommendation applies when both MISCV and ADDRV are clear, not just when no address is logged.
- [overreach] 'No address logged' should read 'MISCV and ADDRV are not set', meaning no additional error information in MCi_MISC and MCi_ADDR. Note too that an unknown MCACOD requires a bugcheck (Table 18-7).
- [currency] 'No address logged' should read as 'MISCV and ADDRV not set', meaning no IA32_MCi_MISC/ADDR information is available.

## 11-C2 - VERIFIED (3S/0R/0U)

In Intel MCA, the SRAO and UCNA classes describe corrupted data that has not been consumed. Recovery for these classes is optional or not required.

- [overreach] Optional SRAO recovery is still MCA-error-code specific. For a known MCACOD, Table 18-7 lists 'take specific recovery action'.

## 11-C3 - VERIFIED (3S/0R/0U)

Intel recoverable SRAR errors split into recoverable-continuable (RIPV=1, EIPV=1) and recoverable-not-continuable (RIPV=0). Restarting the interrupted context without fixing the error usually causes another SRAR on the same instruction.

- [overreach] The 'another SRAR' sentence is stated for the recoverable-continuable case. Restarting at all requires that software first fix the error. In the not-continuable case, software must terminate the interrupted stream.
- [currency] Locator: Table 18-21 is in sec. 18.10.3.2 'Architecturally Defined SRAR Errors', not sec. 18.6.x.

## 11-C4 - VERIFIED (3S/0R/0U)

ACPI ARS lets the platform report uncorrectable persistent-memory errors so system software can avoid accessing them. If a range is read before the OS has processed the ARS data, default platform error handling such as a Machine Check may occur.

- [fidelity] The source says 'accessed', not just 'read'.
- [overreach] The source says 'accessed', not 'read'. The Machine Check sentence sits in the paragraph about the 0x81 notification and OSPM possibly ignoring it.
- [currency] ACPI 6.6 is the current revision and keeps the same wording, so 6.6 could be cited as well.

## 11-C5 - VERIFIED (3S/0R/0U)

ACPI permits Clear Uncorrectable Error on a range only if the range is retired or valid data is written before it is read. If clearing is unsupported or fails, the OS should keep blocking access to the range.

- [fidelity] This is 'should' guidance to OSPM, not a formal permission rule. 'permits ... only if' overstates the normative strength.
- [overreach] 'ACPI permits ... only if' overstates the strength. ACPI recommends ('OSPM should only issue'), it does not set a permission rule. Platform support for Clear Uncorrectable Error is optional.

## 11-C6 - VERIFIED (3S/0R/0U)

Arm RAS defines a poisoned value as one marked in error so that a later access detects it as a detected error. Poison is the mechanism for deferring an error, which is then reported at the point of consumption.

- [fidelity] The spec calls poison 'a common technique' for deferring an error, not the only mechanism.
- [overreach] Arm calls poison 'a common technique' to defer an error, not 'the mechanism'. Deferral is defined more broadly as hardware making forward progress without consuming the error. It is reported at the point of consumption only if it is later consumed.
- [currency] D.d is the latest standalone issue I saw. Later Arm ARM (DDI 0487) releases may now carry the RAS extension rules, so check them for current wording. This is inference; I did not verify it.

## 11-C7 - VERIFIED (3S/0R/0U)

Under Arm RAS, a synchronous External abort can record only the PE error states Uncontainable (UC), Recoverable (UER) or Restartable (UEO). Unrecoverable (UEU) and Corrected (CE) are not supported for this exception type.

- [fidelity] This applies to exceptions taken to AArch64 state. An External abort to AArch32 has no syndrome.
- [overreach] The claim must keep 'taken to AArch64 state': for an External abort to AArch32, no PE error state syndrome is recorded. Deferred (DE) and uncategorized are also unsupported. An SError carries CE only to AArch64, not to AArch32.

## 11-C8 - VERIFIED (3S/0R/0U)

SNIA NPM (draft 1.2a) holds that only errors that are instruction-precise, data-contained and live-reported allow real-time recovery. Any other error requires the application to restart with crash recovery.

- [fidelity] The source says 'will require that the application restart'. The 'with crash recovery' framing comes from the preceding paragraph.
- [overreach] The draft's footer misprints 'Version 1.12a', but the title page reads 1.2a. The draft disclaims use as reference material ('work in progress').
- [currency] Cite the final SNIA NPM v1.2 Technical Position (June 19, 2017) instead of the 1.2a draft. The text is unchanged, and the qualification 'final v1.2 was unreachable' is wrong. The draft's footer also misprints the version as '1.12a'.

## 11-C9 - VERIFIED (3S/0R/0U)

SNIA NPM draft 1.2a defines PRECISE as an exception delivered during the LOAD instruction that caused the memory error. Without PRECISE, an application cannot assume that data from a LOAD is valid. ERROR_UNIT = 0 means memory errors are not contained.

- [fidelity] The pages are 89-90 by the printed footers, not 88-89.
- [currency] Prefer citing the final SNIA NPM v1.2 (June 2017). The pages run to 88-90 rather than 88-89.

## 11-C10 - VERIFIED (3S/0R/0U)

Linux reports memory errors to user space as SIGBUS with si_code BUS_MCEERR_AR (error consumed, action required) or BUS_MCEERR_AO (detected but not consumed, action optional). si_addr_lsb gives the extent of the corruption, and both are Linux-specific extensions.

- [overreach] si_addr_lsb gives the extent indirectly, as the least significant bit of the reported address (for example log2(page size) for a whole corrupted page).
- [currency] Authority/currency: the mkerrisk GitHub repo is an unmaintained mirror. Cite the canonical git.kernel.org man-pages tree (path man/man2/sigaction.2), which keeps the same text.

## 11-C11 - VERIFIED (3S/0R/0U)

In Linux the default for memory-error-unaware applications is late kill: SIGBUS is sent only when the application touches the corrupted page. Early kill is opt-in, and vm.memory_failure_recovery=0 makes every memory failure panic.

- [fidelity] The doc notes that some pages are always handled as late kill.
- [overreach] Late kill is the system-wide default for all processes, not a default reserved for error-unaware applications. The doc also notes 'some pages are always handled as late kill'.
- [currency] The doc also notes that some pages are always handled as late kill.

## 11-C12 - VERIFIED (3S/0R/0U)

In Linux the same pmem media error surfaces differently by access path. A DAX mmap fault on a badblock or latent error gives SIGBUS. A read() through the pmem driver, or a DAX read hitting a known bad range, returns an I/O error (EIO), and the kernel copy (copy_mc_to_kernel) reports the number of bytes it could not copy.

- [fidelity] The EIO half comes from the source code, not from the documentation, as the claim's own qualifications note.
- [overreach] In copy_mc.c the plain-memcpy fallback happens when neither copy_mc_fragile nor ERMS is enabled. It is not tied directly to CONFIG_X86_MCE in that file.
- [currency] The copy_mc qualification is imprecise. With CONFIG_X86_MCE=n only the 'fragile' variant is disabled, and copy_mc_to_kernel still uses copy_mc_enhanced_fast_string on ERMS CPUs. It falls back to plain memcpy only when the fragile key is not enabled and the CPU lacks ERMS. Also, a DAX read that is cut short mid-copy can return a short read or -EFAULT rather than -EIO.

## 11-C13 - VERIFIED (3S/0R/0U)

NOVA-Fortis assumes that loads to a poisoned region cause an MCE and that all data in the poison radius is lost. Poison persists across failures. The Intel poison radius is 64 B, but Linux reports 512-B regions, and undetectable errors silently return invalid data.

- [fidelity] Linux reports the 512-byte regions 'after boot'. The silent-invalid-data point is stated as an assumption about the ECC controller.
- [overreach] The silent-invalid-data behavior and the MCE-on-load behavior are stated as assumptions. The 64 B and 512 B figures are scoped to Intel processors with Linux circa 4.10, as the paper notes.
- [currency] These are 2017 (Linux 4.10-era) design assumptions. Linux badblocks still use 512-B sectors.

## 11-C14 - VERIFIED (3S/0R/0U)

On first-generation Intel Optane DC PMM, random loads take about 305 ns, roughly 3x local DRAM. Sequential loads are about 2x faster because the module merges adjacent requests into 256-B internal accesses.

- [fidelity] The merging into 256-B accesses is the authors' inference ('indicates'), not a direct measurement.
- [overreach] The merging is the authors' inference ('This result indicates'), not a measured mechanism. 'Because' should become 'which the authors attribute to'. The 305 vs 81 ns ratio is about 3.8x.
- [currency] For a peer-reviewed source on the same platform, the authors' FAST 2020 paper (Yang et al., 'An Empirical Guide to the Behavior and Use of Scalable Persistent Memory') is the archival counterpart.

## 11-C15 - VERIFIED (3S/0R/0U)

Field data from the Cielo and Hopper HPC systems show that SEC-DED ECC can let DRAM errors go undetected, potentially causing silent data corruption, at up to 20 FIT per DRAM device. Counting errors instead of faults can produce wrong reliability conclusions.

- [overreach] The undetected-error figure is a projection from Cielo's logged corrected errors under chipkill, not an observed SEC-DED failure. It is not based on Hopper. It assumes errors over 2 bits are undetectable, it depends strongly on vendor (21.7 / 1.8 / 0.2 FIT), and it is phrased as 'may'.
- [currency] The 20 FIT figure is an estimated upper bound derived from the observed fault modes, not a directly observed rate. 'Field data show' slightly overstates it, and 'may... up to' is how the paper puts it.

## 11-C16 - VERIFIED (3S/0R/0U)

Under the Px86 model, persistent memory reads after a crash and recovery can observe states that are impossible in normal executions, for example x=0, y=1 after program-ordered writes x:=1; y:=1. This is because persist order is separate from store order.

- [overreach] The claim should keep the condition: x and y are distinct locations and no explicit persist (flush/flushopt/wb) or fence is used. For a single location, store order and persist order coincide.
- [currency] Locator: this is in sec. 2.2 'The Px86 Model: An Intuitive Account' (Fig. 1a), not sec. 1. The example assumes x and y are on different cache lines, since per location the store and persist orders coincide.

## 12-C1 - VERIFIED (3S/0R/0U)

Under fork consistency, a dishonest server can make a reader miss another user's modification. The only undetectable attack is forking or discarding users' views, and it becomes detectable once the forked users see each other's later operations.

- [fidelity] The quote and the detectability sentence are in Sec. 3.2, p.123, not the Sec. 3 intro on p.122. The paper describes the undetectable attack as the server 'simply discard[ing] A's changes', which forks the users.
- [overreach] The 'only undetectable attack' guarantee covers files written by honest users only. Sec. 3.1 says a server that colludes with, or holds the keys of, compromised users can change any file those users can write. Detection also requires that the forked users communicate or see each other's later operations; the paper does not claim this happens automatically.

## 12-C2 - VERIFIED (3S/0R/0U)

SUNDR gives weaker freshness guarantees than replicated BFT storage, because a malicious server can fork file system state. A trusted 'time stamp box' that rewrites one file every 5 seconds limits how long an inconsistency can last.

- [overreach] The comparison is with BFS specifically. It holds only 'if users have no other evidence of each other's on-line activity'. The time stamp box is a proposed option ('one can use'), not part of SUNDR as built. It bounds the partition window only for users who see the box's updates.
- [currency] The time stamp box is a suggested option ('could'), not an implemented component. The paper frames it as avoiding 'a trusted machine on the critical path'. The comparison is specifically against BFS, the Castro-Liskov BFT file system.

## 12-C3 - VERIFIED (3S/0R/0U)

No protocol that emulates SWMR registers on a Byzantine server with fork-linearizability is wait-free. Even when the server is correct, some execution has an operation, such as a read, that cannot complete until another client takes steps.

- [fidelity] The theorem says 'an operation'. 'Such as a read' comes from the intuition paragraph, not the theorem statement.
- [currency] Theorem 1 also implies Corollary 2 (no obstruction-free emulation when clients may crash). Later papers bypass the bound with weak fork-linearizability.

## 12-C4 - VERIFIED (3S/0R/0U)

No protocol can emulate more than one SWMR register on a Byzantine server with sequential consistency. A faulty server can show 'split-brain' behavior and return old values to reads.

- [currency] In the proof, the stale value is the initial value (bottom), not an arbitrary older write.

## 12-C5 - VERIFIED (3S/0R/0U)

With a faulty untrusted provider, linearizability cannot be ensured, because the server may answer a read with an outdated value. Weak fork-linearizability lets the last operation of each client violate real-time order. Every fork-linearizable history is also weakly fork-linearizable, and weak fork-linearizability permits wait-free protocols.

- [overreach] The impossibility of linearizability applies when the provider is faulty. FAUST still requires linearizability and wait-freedom when the provider is correct.
- [currency] Wait-freedom is guaranteed only when the server is correct. The published version is SIAM J. Comput. 40(2), 2011.

## 12-C6 - VERIFIED (3S/0R/0U)

With masking quorums, a read accepts only a value reported by at least f+1 servers. A masking quorum system for threshold f exists iff n > 4f. For self-verifying data, such as signed values, dissemination quorums need only n > 3f. The resulting read semantics is a safe variable: a read that overlaps a write may return a failure value.

- [overreach] The f+1 acceptance rule is the threshold special case. The general rule accepts a value vouched for by a server set not contained in any fail-prone set, then picks the highest timestamp among accepted values. In the dissemination variant the read instead discards unverifiable pairs and takes the highest timestamp.
- [currency] The n>4f bound applies to masking quorum systems with this protocol, not to Byzantine storage in general. Later work (e.g., Martin-Alvisi-Dahlin, Minimal Byzantine Storage, 2002) reaches 3f+1 for generic data with different protocols. The general read rule is a set of servers not contained in any fail-prone set; f+1 is the threshold case.

## 12-C7 - VERIFIED (3S/0R/0U)

A rollback attack gives a protected module an old state snapshot that is internally consistent and cryptographically sound. Confidentiality and integrity protection therefore do not ensure state continuity. A rollback attack is distinct from a replay attack.

- [fidelity] The PDF at the cited URL lists only Parno, Lorch, Douceur and Mickens as authors; McCune is not on it.
- [overreach] That confidentiality and integrity protection do not ensure state continuity is drawn from the paper's statement that prior schemes doing exactly that are vulnerable to rollback. The paper does not state it as a general theorem.

## 12-C8 - VERIFIED (3S/0R/0U)

A trusted-monotonic-counter defense against rollback is not crash-resilient. A crash between the counter increment and the persistent state write leaves the module permanently unusable. TPM NVRAM endures only about 100,000 write cycles, so one write per second would exhaust it in under 28 hours.

- [overreach] The crash-resilience flaw is shown for the naive strawman design (increment, then persist). The ~100,000-cycle figure is an expected endurance, not a value the authors measured; only the NVRAM read and write latencies were measured. The track's applicability note wrongly calls the endurance figure a measurement.
- [currency] The ~100,000 figure is an expected endurance figure, not a measurement. The measured values in the paper are latencies (reads 9.8-14.8 ms, writes 33.9-82.4 ms).

## 12-C9 - VERIFIED (3S/0R/0U)

SGX sealing does not prevent rollback. A malicious OS can substitute older sealed data, or route reads to a second enclave instance that holds outdated state (a forking attack). SGX monotonic counter writes measured 80-250 ms, and the write limit is reached within a few days of continuous use.

- [overreach] The 80-250 ms latency and the wear-out after about one million writes come from the authors' own experiments on their SGX platforms; Intel does not document these limits.
- [currency] Currency, from background knowledge (not checked in this run): Intel later deprecated the SGX Platform Services monotonic counters and removed SGX from client CPUs, so the counter measurements are historical. Appendix B / the paper puts wear-out at about one million writes.

## 12-C10 - VERIFIED (3S/0R/0U)

dm-verity checks hashes on demand during disk access and fails the I/O if a block cannot be verified up to the root hash. Configuration can weaken this: ignore_corruption lets reads proceed normally, and check_at_most_once detects only offline tampering, not online tampering.

- [currency] The current doc also lists restart_on_corruption, panic_on_corruption and restart/panic_on_error modes. These change the failure action, not the I/O-fail default.

## 12-C11 - VERIFIED (3S/0R/0U)

fs-verity re-verifies file data against a Merkle tree each time it is paged in. Reads of mismatching data fail with EIO for read() and SIGBUS for mmap. DAX is unsupported because it would bypass verification. On its own, fs-verity provides only detection of accidental corruption.

- [overreach] 'Only accidental corruption' describes fs-verity used without any scheme to authenticate its file hashes. The doc says it is primarily meant to support authentication of malicious modifications through trusted userspace or built-in signatures, and that re-verification on page-in defeats runtime changes by malicious disk firmware.
- [currency] The current doc also says direct I/O falls back to buffered I/O.

## 12-C12 - VERIFIED (3S/0R/0U)

A double-fetch bug occurs when the kernel reads the same user-space value twice, expecting it to be identical, while a concurrent thread can change it between the reads. In a static study of Linux the authors found 90 double fetches, 57 of them in drivers. Across Linux, FreeBSD and Android they found six previously unknown bugs, three of them exploitable.

- [overreach] The 90 are double-fetch situations, i.e. candidates found by pattern matching and inspected by hand. Most are benign, so they are not 90 bugs. The definition requires that the kernel uses the value as well as reads it twice.
- [currency] The 90/57 counts are for Linux 4.5 specifically, found with a pattern-based static analysis (Coccinelle).

## 12-C13 - VERIFIED (3S/0R/0U)

Binding a file by name is late and transient, re-resolved at every reference. Binding by descriptor is early and permanent. Reference by name between check and use creates the TOCTTOU race, which cannot be eliminated without kernel modification.

- [overreach] The claim concerns UNIX system call interfaces as of 1995. Bishop also says the problem 'can be greatly ameliorated' without kernel changes, for example by checking trustworthiness or dropping privileges so the race becomes harmless. Later descriptor-relative calls such as openat/fstat are the kind of kernel change he proposed.
- [currency] Currency: the 'requires kernel modification' point was true for 1995 UNIX. From background knowledge (not checked in this run), modern kernels and POSIX provide descriptor-relative and no-follow interfaces (fchown/fchmod/fstat, *at() calls, O_NOFOLLOW, Linux openat2 RESOLVE_* flags). This is the kind of kernel change Bishop called for, so the race can now be avoided without changing the kernel further.

## 12-C14 - VERIFIED (3S/0R/0U)

Repeatedly reading (activating) one DRAM row can corrupt data in nearby rows. Disturbance errors were found in 110 of 129 commodity modules, with as few as 139K accesses needed to induce one, and were triggered by a user-level program on Intel and AMD systems.

- [overreach] The 110/129 and 139K figures come from the FPGA-based characterization of DDR3 modules made between 2008 and 2014. The Intel/AMD user-level demonstration is a separate proof of concept.
- [currency] Currency, from background knowledge (not checked in this run): later studies such as Kim et al. ISCA 2020 ('Revisiting RowHammer') report much lower thresholds on DDR4/LPDDR4, around 10K activations. TRRespass (2020) showed DDR4 TRR can be bypassed. So 139K is a DDR3-era figure.

## 12-C15 - VERIFIED (3S/0R/0U)

In MLC NAND flash, reading one row shifts the threshold voltages of unread cells in other rows of the same block (read disturb). The probability of read-disturb errors rises with wear-out and with pass-through voltage.

- [overreach] The source says the pass-through voltage 'can shift' unread cells, a cumulative effect over many reads. A single read does not deterministically shift them.
- [currency] These are planar 2Y-nm MLC results. 3D NAND read disturb behaves differently and was characterized in later work.

## 12-C16 - VERIFIED (3S/0R/0U)

PDP argues that detecting modification or deletion only when data is accessed may be too late for archives, where little data is read. Random block sampling detects 1% deletion of a 10,000-block file with more than 99% probability by challenging 460 blocks.

- [overreach] The 460-block figure assumes the server deleted at least 1% of the blocks and the challenged blocks are chosen at random. Smaller corruptions need more samples.

## 12-C17 - VERIFIED (3S/0R/0U)

A proof of retrievability lets an archive prove that the user can recover the whole file without the user downloading it. Small corruptions may escape sentinel checks but are repaired by error-correcting codes, while large corruptions are detected with high probability.

- [overreach] The small-versus-large corruption behaviour belongs to the paper's own sentinel-plus-error-correction construction. It is not a property of all POR schemes.
- [currency] The sentinel scheme supports only a bounded number of challenges. Later POR schemes (e.g., Shacham-Waters 2008) are the current baseline.

## 12-C18 - CONTESTED (2S/1R/0U)

PREMIS defines a fixity check as comparing a message digest computed earlier with one computed later. It specifies that 'message digest' means a cryptographic hash, not a CRC checksum, and says fixity does not address integrity or authenticity. OAIS, in contrast, gives a CRC as its example of Fixity Information and requires random verification by Archival Storage.

- REFUTE [overreach] PREMIS 3.0, 1.5.2 usage note: verbatim on comparing an earlier and a later digest, and on 'message digest' meaning a cryptographic hash. The special topic says fixity 'does not address the object's integrity or authenticity'. However, PREMIS's own messageDigestAlgorithm examples (1.5.2.1) list Adler-32, a non-cryptographic checksum, beside MD5 and SHA. OAIS CCSDS 650.0-M-2 (fetched) defines Fixity Information with a CRC example, but Sec. 4.1.1.3 says the procedures 'should provide for random verification of the integrity of Data Objects using CRCs or some other error checking mechanism'.
- [fidelity] OAIS says Archival Storage procedures 'should provide for' random verification. That is a recommendation, not a strict requirement.
- [overreach] PREMIS's parenthetical about cryptographic hashes is a terminology note, not a constraint: its own example algorithms include Adler-32, so the PREMIS-versus-OAIS (hash versus CRC) contrast is overstated. OAIS 'should provide for' random verification is a recommendation, not a requirement, and it allows CRCs 'or some other error checking mechanism'.
- [currency] OAIS 650.0-M-2 is superseded by 650.0-M-3 (Dec 2024). M-3's glossary definition of Fixity Information drops the CRC example. Its text now gives 'Cyclic Redundancy Check (CRC) codes, checksums, or message digests' as examples, so the CRC-vs-hash contrast is weaker under the current OAIS. Also, OAIS says Archival Storage procedures 'should provide for' random verification; it is a recommendation, not a requirement.

## 12-C19 - VERIFIED (3S/0R/0U)

LOCKSS detects and repairs damage in unread preserved content through infrequent, rate-limited peer opinion polls on content hashes. It assumes cheap storage is unreliable and avoids long-term secrets. Polls are scheduled often enough that random undetected damage does not significantly affect readers.

- [overreach] The poll rate is a design goal of the protocol, supported only by simulation; it is not an empirically established outcome. The source does not limit polling to unread content. Polls cover all preserved content whether or not it has been read.
- [currency] The protocol was later revised (ACM TOCS 2005 version and later LOCKSS releases), and the results are simulation-based.
