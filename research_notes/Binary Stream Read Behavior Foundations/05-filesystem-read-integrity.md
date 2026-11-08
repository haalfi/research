# Track 05: File-system and storage-stack failure handling as observed by readers

Scope: what a reader of a file can observe (error, stale data, zeros, garbage/junk, silent wrong data) because of how file systems and the storage stack detect, transform, propagate or drop lower-level faults. Read behavior is the focus; write/fsync and crash material is included only where it decides what a later read returns.

Downloads: `/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/filesystem-read-integrity/` (PDFs converted with pdftotext; quotes below are from the extracted text, so hyphenation and line breaks may differ slightly from the typeset page).

## Sources consulted (access status)

| # | Source | Type | Access |
|---|--------|------|--------|
| S1 | Prabhakaran, Bairavasundaram, Agrawal, Gunawi, Arpaci-Dusseau, Arpaci-Dusseau. "IRON File Systems." SOSP 2005. research.cs.wisc.edu/adsl/Publications/iron-sosp05.pdf | peer-reviewed empirical + taxonomy | full text |
| S2 | Gunawi, Rubio-González, Arpaci-Dusseau, Arpaci-Dusseau, Liblit. "EIO: Error Handling is Occasionally Correct." FAST 2008. usenix.org legacy full_papers/gunawi | peer-reviewed empirical (static analysis + fault injection) | full text |
| S3 | Zhang, Rajimwale, Arpaci-Dusseau, Arpaci-Dusseau. "End-to-end Data Integrity for File Systems: A ZFS Case Study." FAST 2010 | peer-reviewed empirical (fault injection) | full text |
| S4 | Krioukov, Bairavasundaram, Goodson, Srinivasan, Thelen, Arpaci-Dusseau, Arpaci-Dusseau. "Parity Lost and Parity Regained." FAST 2008 | peer-reviewed, formal (model checking) | full text |
| S5 | Bairavasundaram, Goodson, Schroeder, Arpaci-Dusseau, Arpaci-Dusseau. "An Analysis of Data Corruption in the Storage Stack." FAST 2008 | peer-reviewed field study | full text (followed from S4/S6 citations) |
| S6 | Saltzer, Reed, Clark. "End-to-End Arguments in System Design." ACM TOCS 2(4), 1984 (MIT author copy) | foundational theory/design principle | full text |
| S7 | Ganesan, Alagappan, Arpaci-Dusseau, Arpaci-Dusseau. "Redundancy Does Not Imply Fault Tolerance." FAST 2017 | peer-reviewed empirical (fault injection, errfs) | full text |
| S8 | Pillai et al. "All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications." OSDI 2014 | peer-reviewed empirical | full text (relevant sections 2.1-2.2 read closely) |
| S9 | Rebello, Patel, Alagappan, Arpaci-Dusseau, Arpaci-Dusseau. "Can Applications Recover from fsync Failures?" USENIX ATC 2020 | peer-reviewed empirical | full text (section 3 read closely) |
| S10 | Linux kernel Documentation/filesystems/vfs.rst, section "Handling errors during writeback" (master, fetched 2026-11-08) | implementation doc | full text of section |
| S11 | Linux kernel Documentation/core-api/errseq.rst (master, fetched 2026-11-08) | implementation doc | full text |
| S12 | Linux kernel Documentation/filesystems/ext4/checksums.rst (master) | implementation doc | full text |
| S13 | btrfs-progs Documentation/ch-checksumming.rst (master, fetched 2026-11-08) | implementation doc | full text |
| S14 | POSIX.1-2024 (IEEE Std 1003.1-2024 / Open Group Base Specifications Issue 8): read(), write(), fsync() pages at pubs.opengroup.org/onlinepubs/9799919799/ | normative | full text of the pages |

Not reached in this track (COVERAGE-GAP, not read): OpenZFS official docs on checksum/scrub error reporting; XFS metadata CRC docs; Microsoft ReFS integrity streams docs; Schroeder/Gibson and Bairavasundaram SIGMETRICS 2007 latent sector error study (cited by S4 for the 19%/2% figure; I did not read it, so that figure is a secondary citation only); Rubio-González et al. PLDI 2009 error propagation follow-up; Fryer et al. Recon (FAST 2012) runtime metadata checking; Alagappan et al. PAR / CTRL (protocol-aware recovery, FAST 2018) follow-ups.

## Extracted findings

### S1 IRON File Systems (SOSP 2005)
- Fail-partial failure model, sec. 2.3: "failures manifest themselves in three ways: • Entire disk failure: The entire disk is no longer accessible. If permanent, this is the classic 'fail-stop' failure. • Block failure: One or more blocks are not accessible; often referred to as 'latent sector errors' [33, 34]. • Block corruption: The data within individual blocks is altered. Corruption is particularly insidious because it is silent – the storage subsystem simply returns 'bad' data upon a read."
- Transience, sec. 2.3.1: failures can be "'sticky' (permanent) or 'transient' (temporary)"; "a transport or higher-level software issue might at first cause block failure or corruption; however, the operation could succeed if retried."
- Root-cause vocabulary, sec. 2.2: "'misdirected' writes are writes that place the correct data on the disk but in the wrong location, and 'phantom' writes are" writes reported complete but never written to media.
- IRON detection taxonomy (Table 1, sec. 3.1): D_Zero "No detection / Assumes disk works"; D_ErrorCode "Check return codes from lower levels / Assumes lower level can detect errors"; D_Sanity "Check data structures for consistency"; D_Redundancy "Redundancy over one or more blocks / Detect corruption in end-to-end way".
- IRON recovery taxonomy (Table 2, sec. 3.3): R_Zero "No recovery / Assumes disk works"; R_Propagate "Propagate error / Informs user"; R_Stop "Stop activity (crash, prevent writes) / Limit amount of damage"; R_Guess "Return 'guess' at block contents / Could be wrong; failure hidden"; R_Retry "Handles failures that are transient"; R_Repair "Repair data structs / Could lose data"; R_Remap "Assumes disk informs FS of failures"; R_Redundancy "Block replication or other forms / Enables recovery from loss/corruption".
- "The detection and recovery mechanisms employed by a file system define its failure policy." Taxonomy explicitly "by no means complete".
- Detection frequency, sec. 3.2: lazy (on access) vs eager (scrubbing); "scrubbing typically leverages the return codes explicitly provided by the disk and hence discovers block failure but not corruption."
- Checksum limitation, sec. 3.1: "a checksum that is stored along with the data it checksums will not detect such misdirected or phantom writes."
- End-to-end justification, sec. 3: "the primary reason for detection and recovery within the file system is found in the end-to-end argument [53]".
- Empirical (sec. 5.1, ext3): "To detect read failures, ext3 primarily uses error codes (D_ErrorCode). However, when a write fails, ext3 does not record the error code (D_Zero)". "For read failures, ext3 also often aborts the journal (R_Stop); aborting the journal usually leads to a read-only remount".
- Cross-FS conclusion, sec. 5.6: "Sanity checking is of limited utility ... misdirected and phantom writes lead to cases where the file system could receive a properly formatted (but incorrect) block; the bad block thus passes sanity checks, is used, and can corrupt the file system. Indeed, all file systems we tested exhibit this behavior." Also "all of the file systems used some form of R_Stop when something as innocuous as a read failure occurred". "Redundancy is not used ... none of them apply redundancy to enable recovery from such failures." File systems tested: ext3, ReiserFS, JFS (Linux 2.6), NTFS. Data/metadata injected via a pseudo-device driver (type-aware fault injection).

### S2 EIO (FAST 2008)
- Abstract: "running our EDP analysis on all file systems and 3 major storage device drivers in Linux 2.6, we find that errors are often incorrectly propagated; 1153 calls (13%) drop an error code without handling it." "We confirm that write errors are neglected more often than read errors."
- Table 4 caption: "read errors are handled more correctly than write errors ... The 29 (*) violated read calls are all related to readahead and asynchronous read; in other words, all error codes returned in synchronous reads are being saved and checked."
- Sec. 3.2: JBD "does not properly propagate any block write failures" during journal recovery (journal_recover ignores sync_blockdev's EIO); NFS client "is not informed when a write failure occurs during a sync operation".
- Terminology: "error-broken channel ... the error code is either unsaved, unchecked, or overwritten."
- Applicability: static analysis of Linux 2.6 at that time; counts are of call sites, not of runtime frequency.

### S3 ZFS end-to-end integrity (FAST 2010)
- Disk faults: "Observation 1: ZFS detects all corruptions due to the use of checksums ... bad data was never returned to the user". Observation 5: "ZFS cannot recover from multiple block corruptions affecting all ditto blocks when no in-memory copy exists ... ZFS reported an error."
- Memory faults: abstract "ZFS is less resilient to memory corruption, which can lead to corrupt data being returned to applications or system crashes." Sec. 6: "the checksum is verified only when the block is being read from the disk. Following that, as long as the block stays in the page cache, it is never checked against the checksum ... The result is that ZFS returns bad data to the user on reads." For writes, corruption before flush gets a fresh checksum computed over bad data, so "On subsequent reads of the block, it passes the checksum verification and is returned to the user."
- Preliminary ext2 memory-corruption analysis: "ext2 is also vulnerable to memory corruptions" (sec. 7, preliminary).
- Applicability: ZFS on OpenSolaris at time of study; single-disk and mirrored pool configurations as tested.

### S4 Parity Lost and Parity Regained (FAST 2008)
- Fault vocabulary, sec. 2.2: latent sector errors (disk "returns an explicit error code"), corruptions, torn writes ("writing only a portion of the sectors in a given write request"), lost writes ("return a success code to indicate completion of a write, but not perform the write"), misdirected writes ("the original disk location does not receive the write ... (lost write), while the data in a different location is overwritten").
- Outcome classification, sec. 2.3: "Data recovery: ... detects the error, and uses parity to successfully recover data. • Data loss: ... detects the error, but is unable to successfully recover data. In this case, the storage system reports an error to the user. • Corrupt data: ... does not detect the error, and therefore returns corrupt data to the user."
- Sec. 4.4: "One primary problem with block checksums is that lost writes are not detected ... leaving the old data and checksum intact and valid. On later reads to disk block, checksum verification compares the old data and old checksum which are consistent, thereby not detecting the lost write." (reader observes stale data that verifies.)
- Parity pollution: "corrupt data (the result of a single error) across multiple disks, thus leading to data loss or corruption"; "find flaws in every scheme" examined. Version mirroring + logical and physical identity proposed as a combination that eliminates found problem states.
- Applicability: single RAID stripe, single-error conditions, abstract model of real systems' published protections.

### S5 Analysis of Data Corruption in the Storage Stack (FAST 2008)
- 1.53 million disks, 41 months, NetApp production. Classes: "checksum mismatches, identity discrepancies, and parity inconsistencies".
- "more than 400,000 instances of checksum mismatches ... 8% of which were discovered during RAID reconstruction".
- Sec. 4.1: "3088 of the 358,000 nearline disks (0.86%) and 767 of the 1.17 million enterprise class disks (0.065%)" developed checksum mismatches.
- Detection-point semantics, sec. 2.3: checksum mismatches "can be detected anytime a disk block is read"; identity discrepancies "can be detected only during file system reads"; parity inconsistencies "are detected only during data scrubs". "We are aware of actual cases when the disk firmware replied successfully to a write that was never written to stable media."
- Mismatches show "high spatial and temporal locality" and are not independent across disks in a system.
- Applicability: detection relies on NetApp's 520-byte-sector/data-integrity-segment format; only corruptions detectable by these mechanisms are counted, so undetected corruption is unmeasured (stated by authors: some forms "cannot be identified").

### S6 End-to-end argument (Saltzer, Reed, Clark 1984)
- Principle: "The function in question can completely and correctly be implemented only with the knowledge and help of the application standing at the end points of the communication system ... (Sometimes an incomplete version of the function provided by the communication system may be useful as a performance enhancement.)"
- Careful file transfer, threat 1: "The file, though originally written correctly onto the disk at host A, if read now may contain incorrect data, perhaps because of hardware faults in the disk storage system." Threat 2: software "might make a mistake in buffering and copying the data".
- MIT gateway anecdote: per-hop checksums but "the transmitted data was unprotected while stored in each gateway"; a byte-pair interchange about once per million bytes corrupted source files.
- Note: a design argument, not a formal guarantee.

### S7 Redundancy Does Not Imply Fault Tolerance (FAST 2017)
- Term: "complex failures are known as partial storage faults"; faults the FS hands up are "file-system faults".
- Sec. 2.1/3: "ext4 returns corrupted data as-is to applications if the underlying device block is corrupted ... btrfs transforms an underlying block corruption into a read error." "in the ext family of file systems and XFS, there are no checksums for user data and so it is possible for applications to read such corrupted data, without any errors." "applications can receive EIO on reads when there is an underlying latent sector error ... possible on all commonly used file systems including ext4, XFS, ZFS, and btrfs." btrfs/ZFS: "detection of corruption may be possible but not recovery (unless mounted with special options such as copies=2 in ZFS)".
- Fault model (errfs): corruption "with zeros or junk" on reads, EIO on reads, EIO on writes, ENOSPC/EDQUOT.
- Observation classes: local behavior {Crash, Partial Crash, Retry, Internal Redundancy, Ignore Faulty Data, Log Error, No Detection/Recovery}; global effect {Corruption, Data loss, Read Unavailable, Write Unavailable, Unavailable, Query Failure, Reduced Redundancy, Correct}.
- Findings: "a single file-system fault can cause catastrophic outcomes such as data loss, corruption, and unavailability"; e.g. "RethinkDB silently returns corrupted data"; Redis "does not use checksums" on its data files; crash is the most common reaction when faults are detected.
- Applicability: eight systems (Redis, ZooKeeper, Cassandra, Kafka, RethinkDB, MongoDB, LogCabin, CockroachDB) at studied versions; single fault per run.

### S8 Pillai et al. (OSDI 2014)
- Crash-state vocabulary, sec. 2.1: "If the append is not atomic, for example, it would be possible for the size of the file to be updated without the new data reflected to disk; in this case, the files could contain garbage". Terms "size-atomicity", "content-atomicity", ordering violations; "persistence properties".
- Sec. 2.2.1: "all tested file systems seemingly provide atomic single-sector overwrites: in some cases (e.g., ext3-ordered), this property arises because the underlying disk provides atomic sector writes"; atomic appends are "not provided by ext2 or writeback configurations of ext3, ext4, and reiserfs." Caveat: on byte-atomic media (PCM) "single-sector overwrites will not be atomic."
- Applicability: properties determined empirically with the BOB tool, which "is not complete"; Linux file systems of 2014.

### S9 Rebello et al. (ATC 2020)
- Abstract: "all three file systems mark pages clean after fsync fails"; "the content in said clean pages varies depending on the file system; ext4 and XFS contain the latest copy in memory while Btrfs reverts to the previous consistent state."
- Sec. 3.3.1 (ext4 ordered): "an application that reads any of these failed data blocks while they remain in the page cache will see the newly appended contents; however, when any of those pages are no longer in memory and must be read from disk, applications will read the original block contents."
- Defines "non-overwritten block": "If a block is allocated but not overwritten with the new data". ext4: NOB "in both the middle and end of files"; XFS "only the middle"; Btrfs: holes from fd offset advance.
- XFS: "on a journal-block fault, XFS shuts down the file system entirely ... all subsequent read and write operations fail". Btrfs: "if an application reads the data after this failure, it will never see the failed operation as a temporary state."
- ext4 data mode "does not report an fsync failure immediately in some cases, instead (oddly) failing the subsequent call."
- Marking clean is per-FS writepages behavior, "not due to any behavior inherited from the VFS layer".
- Applicability: Linux kernel at time of study (5.x), single injected block failure, ext4 ordered/data, XFS, Btrfs.

### S10/S11 Linux writeback error docs (implementation doc)
- vfs.rst: "After an error has been reported on one request, subsequent requests on the same file descriptor should return 0, unless further writeback errors have occurred since the previous file synchronization." "the generic writeback error tracking infrastructure in the kernel settles for reporting errors to fsync on all file descriptions that were open at the time that the error occurred."
- errseq.rst: errseq_t is a 32-bit value (counter | SF flag | errno); "there is a risk of collisions if new errors are being recorded frequently, since we have so few bits to use as a counter." Watchers can tell only whether an error occurred since they sampled; "all he can remember is the most recent mistake".
- Relevance to reads: these docs describe how writeback errors reach fsync callers; they say nothing about what subsequent read() returns for the failed pages (that is answered empirically by S9).

### S12 ext4 metadata checksums (implementation doc)
- "Starting in early 2012, metadata checksums were added to all major ext4 and jbd2 data structures. The associated feature flag is metadata_csum." Table lists superblock, MMP, xattrs, directory entries, HTREE, extents, bitmaps, inodes, group descriptors; "Some data structures did not have space to fit a full 32-bit checksum, so only the lower 16 bits are stored." Warning: if directory rebuild is skipped, "your directories will not be protected by a checksum!" No file-data checksum is listed (consistent with S7's statement that ext4 has no user-data checksums).

### S13 btrfs checksumming (implementation doc)
- "Data and metadata are checksummed by default. The checksum is calculated before writing and verified after reading the blocks from devices." Metadata: inline checksum in b-tree node header; data: "detached checksum stored in the checksum tree".
- O_DIRECT caveat: user program modifying the direct-write buffer before writeback finishes "can lead to a data checksum mismatch"; since 6.14 direct writes fall back to buffered for checksummed inodes; NODATASUM flag disables data checksums. CRC32C "not collision-resistant but still good error detection capabilities".

### S14 POSIX.1-2024 (normative)
- write(): "After a write() to a regular file has successfully returned: Any successful read() from each byte position in the file that was modified by that write shall return the data specified by the write() for that position until such byte positions are again modified."
- read(): "If any portion of a regular file prior to the end-of-file has not been written, read() shall return bytes with value 0." read() "may fail if: [EIO] A physical I/O error has occurred." (EIO is a "may fail" condition.)
- fsync(): "If the fsync() function fails, outstanding I/O operations are not guaranteed to have been completed." "The nature of the transfer is implementation-defined." Rationale: "It is explicitly intended that a null implementation is permitted" (when _POSIX_SYNCHRONIZED_IO is not defined; text truncated in extract around this point).

## Existing models / classifications found
1. Fail-partial failure model (S1): entire disk failure / block failure (latent sector error) / block corruption; transient vs sticky; locality.
2. IRON detection and recovery taxonomy (S1): D_Zero, D_ErrorCode, D_Sanity, D_Redundancy; R_Zero, R_Propagate, R_Stop, R_Guess, R_Retry, R_Repair, R_Remap, R_Redundancy; "failure policy"; lazy vs eager detection.
3. Error-outcome classes (S4): data recovery / data loss (error reported) / corrupt data (undetected).
4. Corruption classes by detection mechanism (S5): checksum mismatch / identity discrepancy / parity inconsistency, with where each can be detected (any read / FS read only / scrub only).
5. Disk-write fault vocabulary (S1, S4, S5): latent sector error, corruption/bit rot, torn write, lost (phantom) write, misdirected write.
6. Error-broken channel: unsaved / unchecked / overwritten error codes (S2).
7. Local behavior x global effect matrix (S7); "partial storage faults" vs "file-system faults"; fault injection "zeros or junk".
8. Persistence properties: size-atomicity, content-atomicity, ordering (S8).
9. Non-overwritten block, page clean/dirty after failed fsync, page content latest vs reverted (S9).
10. errseq_t error-cursor model for writeback errors (S11).
11. End-to-end argument (S6).

## Convergences
- Checksums verified on read convert silent corruption into a reported error, but not into correct data unless redundancy exists: S3 (ZFS: E without ditto copies), S7 (btrfs/ZFS return errors; recovery only with copies=2), S4 (data loss outcome = error to user). S13 says btrfs verifies after reading.
- Checksums co-located with data do not detect lost/phantom/misdirected writes: S1 (sec. 3.1) and S4 (sec. 4.4) agree independently; S5 adds identity information for this reason.
- Read errors are handled more consistently than write errors: S1 (ext3) and S2 (Linux-wide static analysis).
- Integrity checks have a scope boundary: data is protected only between check points. S6 (gateway buffers), S3 (page cache after verification), S13 (O_DIRECT buffer modification after checksum). [inference: these are three instances of the same end-to-end limitation; the sources do not themselves link S3/S13 to S6 except S1 and S3 citing the end-to-end idea]
- File systems without data checksums (ext family, XFS) return corrupted content without error: S1 (sanity checks pass properly formatted wrong blocks), S7 (explicit), S12 (only metadata listed).

## Contradictions / tensions
- POSIX write() guarantee (S14: any successful read after a successful write returns the written data) vs S9 empirical: after a failed writeback/fsync on ext4/XFS, a read returns new data while cached and "the original block contents" after eviction. [inference: either the POSIX guarantee is understood to hold only absent I/O errors, or this is non-conforming behavior; POSIX text as read does not state the exception. Not resolved by any source read.]
- S1 (2005) finds file systems "Redundancy is not used"; S3/S13 show ZFS and btrfs now checksum and replicate (ditto blocks, mirrors). Not a contradiction in fact but a change across technology generations; S1's findings apply to ext3/ReiserFS/JFS/NTFS of 2005.
- ZFS: S3 Observation 1 "detects all corruptions" (disk) coexists with "returns bad data" (memory). The guarantee is conditional on the fault location.
- S1 says R_Stop on read failure is overused ("draconian"); S9 shows XFS shuts down on journal fault making "all subsequent read and write operations fail" — a reader can lose access to intact data because of a write failure.

## Gaps
- GENUINE-GAP: no normative standard read here specifies what read() must return for data whose writeback failed, or whether stale data after a failed fsync is permitted. POSIX defines EIO only as a "may fail" condition.
- GENUINE-GAP (per sources): S5 counts only corruption detectable by its mechanisms; the rate of undetected silent corruption delivered to readers is unmeasured.
- COVERAGE-GAP: official OpenZFS docs (checksum error counters, zpool status semantics), XFS metadata CRC (v5) docs, ReFS integrity streams, NTFS current behavior not read.
- COVERAGE-GAP: no SSD/flash-specific file-system read studies read in this track (S7 cites flash studies; not read).
- COVERAGE-GAP: Linux behavior changes after the 2018 fsync/errseq discussion (PostgreSQL "fsyncgate") known only via S9/S10; LWN and mailing-list primary sources not read.
- COVERAGE-GAP: the 19%/2% latent-sector-error figure in S4 cites a SIGMETRICS 2007 paper not read here.
