# Track 01: Operating-system read interfaces and their normative semantics

Downloads: /tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/os-file-read-semantics/
All sources below were fetched and read in full text (relevant sections) unless marked otherwise.

## Sources consulted (access status)

| # | Source | Type | Access |
|---|--------|------|--------|
| S1 | The Open Group / IEEE, POSIX.1-2024 (SUSv5, Issue 8), read()/pread() — https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html | normative (+ informative RATIONALE) | full text |
| S2 | POSIX.1-2024 System Interfaces ch.2, §2.9.7 "Thread Interactions with File Operations" — .../functions/V2_chap02.html | normative | full text of §2.9.7 |
| S3 | POSIX.1-2024 lseek() (SEEK_HOLE/SEEK_DATA) — .../functions/lseek.html | normative | full text |
| S4 | POSIX.1-2024 write() — .../functions/write.html | normative | full text (read-after-write, PIPE_BUF) |
| S5 | POSIX.1-2024 mmap() — .../functions/mmap.html | normative | full text |
| S6 | Linux man-pages read(2) — https://man7.org/linux/man-pages/man2/read.2.html | implementation doc | full text |
| S7 | Linux man-pages readv(2) | implementation doc | full text |
| S8 | Linux man-pages mmap(2) | implementation doc | full text |
| S9 | Linux man-pages open(2) (O_DIRECT NOTES) | implementation doc | full text |
| S10 | Linux man-pages signal(7) (SA_RESTART, slow devices) | implementation doc | full text |
| S11 | Linux man-pages pipe(7) | implementation doc | full text |
| S12 | Linux man-pages readahead(2) | implementation doc | full text |
| S13 | Linux kernel Documentation/core-api/errseq.rst (raw.githubusercontent.com) | implementation doc | full text (head) |
| S14 | J. Corbet, "Improved block-layer error handling", LWN, 2017-06-02 https://lwn.net/Articles/724307/ | engineering journalism | full text |
| S15 | J. Corbet, "PostgreSQL's fsync() surprise", LWN, 2018-04-18 https://lwn.net/Articles/752063/ | engineering journalism | full text |
| S16 | Microsoft Learn, ReadFile function (fileapi.h) | implementation doc | full text |
| S17 | Microsoft Learn, "Testing for the End of a File" | implementation doc | full text |
| S18 | Microsoft Learn, "File Buffering" (FILE_FLAG_NO_BUFFERING) | implementation doc | full text |
| S19 | Microsoft Learn, "File Attribute Constants" | implementation doc | full text |
| S20 | Rebello et al., "Can Applications Recover from fsync Failures?", USENIX ATC 2020, https://www.usenix.org/system/files/atc20-rebello.pdf | peer-reviewed empirical | full text (§1, §3.3) |
| — | Linux vfs.rst, lseek(2), fsync(2) man pages | fetched, skimmed only; no claims based on them |

## Extracted findings

### POSIX.1-2024 read() (S1), DESCRIPTION / ERRORS / RATIONALE
- Short reads are permitted outcomes, enumerated: "The value returned may be less than nbyte if the number of bytes left in the file is less than nbyte, if the read() request was interrupted by a signal, or if the file is a pipe or FIFO or special file and has fewer than nbyte bytes immediately available for reading."
- EOF: "No data transfer shall occur past the current end-of-file. If the starting position is at or after the end-of-file, 0 shall be returned. If the file refers to a device special file, the result of subsequent read() requests is implementation-defined."
- Interruption: "If a read() is interrupted by a signal before it reads any data, it shall return -1 with errno set to [EINTR]. If a read() is interrupted by a signal after it has successfully read some data, it shall return the number of bytes read." RATIONALE: POSIX chose BSD/FIPS 151 behaviour over AT&T's (-1/EINTR after partial transfer). RATIONALE also: an implementation that buffers may move data "at the latest possible moment", so an interrupt "may not cause read() to return a partial byte count, but rather to return -1 and set errno to [EINTR]."
- Unwritten regions: "If any portion of a regular file prior to the end-of-file has not been written, read() shall return bytes with value 0."
- Pipes/FIFOs: empty pipe with no writer -> return 0 (EOF); with writer and O_NONBLOCK -> -1/EAGAIN; else block. "The behavior of multiple concurrent reads on the same pipe, FIFO, or terminal device is unspecified."
- EIO: "may fail if: [EIO] A physical I/O error has occurred." (a "may fail", not "shall fail").
- EOVERFLOW: regular file, nbyte>0, start before EOF and >= offset maximum of the open file description.
- File offset after error is unspecified (RATIONALE: "there are too many cases").
- Hardware errors out of scope: "It is considered beyond the scope of this volume of POSIX.1-2024 to describe what happens in the case of hardware errors."
- Atomicity intent (RATIONALE, informative): "I/O is intended to be atomic to ordinary files and pipes and FIFOs. Atomic means that all the bytes from a single operation that started out together end up together, without interleaving from other I/O operations." Terminals excepted.
- Pipe read atomicity explicitly not guaranteed: "there could be no guarantee of atomicity of reads of {PIPE_BUF} or any other size".
- pread(): "equivalent to read(), except that it shall read from a given position in the file without changing the file offset"; ESPIPE on non-seekable files.
- O_RSYNC with O_DSYNC/O_SYNC [SIO option]: reads complete as synchronized I/O data/file integrity completion.

### POSIX.1-2024 §2.9.7 (S2)
- read(), readv(), pread(), write(), lseek() etc. "shall be atomic with respect to each other in the effects specified in POSIX.1-2024 when they operate on file descriptors that are open, or being opened, to files in the file hierarchy ... each call shall either see all of the specified effects of the other call, or none of them." Note: heading in Issue 8 is "Thread Interactions with File Operations" and wording begins "Except where specified otherwise"; Linux read(2) BUGS quotes the older POSIX.1-2008 wording ("Thread Interactions with Regular File Operations", "regular files or symbolic links").

### POSIX.1-2024 write() (S4)
- Read-after-write: "After a write() to a regular file has successfully returned: Any successful read() from each byte position in the file that was modified by that write shall return the data specified by the write() for that position until such byte positions are again modified." (Inference: this is stated about the abstract file, not about durable media; contrast S15/S20.)
- PIPE_BUF atomicity applies to writes; "atomicity is guaranteed according to the amount requested, not the amount written."

### POSIX.1-2024 lseek() (S3): holes
- "A hole is a contiguous region of bytes within a file, all having the value of zero. Not all bytes with the value zero need belong to a hole; however, all seekable files shall have a virtual hole starting at the current size of the file, whether or not the file is sparse."
- RATIONALE: "Not all file systems support holes, and even where sparse files are supported, not all contiguous blocks of zero bytes are required to be recognized as a hole."

### POSIX.1-2024 mmap() (S5)
- "The system shall always zero-fill any partial page at the end of an object. ... References within the address range ... to whole pages following the end of an object shall result in delivery of a SIGBUS signal." "An implementation may generate SIGBUS signals when a reference would cause an error in the mapped object, such as out-of-space condition."

### Linux read(2), readv(2), signal(7), pipe(7), readahead(2), open(2) (S6-S12)
- read(2): "It is not an error if this number is smaller than the number of bytes requested". Linux caps transfer: "read() (and similar system calls) will transfer at most 0x7ffff000 (2,147,479,552) bytes" on 32- and 64-bit.
- read(2) EIO causes include "low-level I/O error while reading from a disk or tape" and on networked filesystems a lost advisory lock.
- read(2) EINVAL for O_DIRECT misalignment of buf, count or offset.
- read(2) BUGS: before Linux 3.14 concurrent read() on a shared open file description was not atomic w.r.t. offset update; "the reads in the two processes might (incorrectly) overlap in the blocks of data that they obtained. This problem was fixed in Linux 3.14."
- NFS: atime may not update due to client attribute caching.
- readv(2): "readv() is guaranteed to read a contiguous block of data from the file, regardless of read operations performed in other threads or processes"; buffers filled in array order and may not all be filled. RWF_NOWAIT for preadv2 returns partial or EAGAIN; BUGS: may return 0 even when not at EOF.
- signal(7): SA_RESTART restarts read() on "slow" devices (terminal, pipe, socket); partial transfer returns success; "a (local) disk is not a slow device according to this definition; I/O operations on disk devices are not interrupted by signals."
- open(2) O_DIRECT NOTES: alignment "vary by filesystem and kernel version and might be absent entirely. The handling of misaligned O_DIRECT I/Os also varies; they can either fail with EINVAL or fall back to buffered I/O." STATX_DIOALIGN since 6.1. Mixing O_DIRECT with buffered I/O or mmap discouraged; NFS O_DIRECT bypasses only client cache.
- mmap(2): SIGBUS on "access to a page of the buffer that lies beyond the end of the mapped file"; MAP_PRIVATE: "It is unspecified whether changes made to the file after the mmap() call are visible in the mapped region."
- readahead(2): hint-only; benefit holds "assuming the readahead was initiated early enough and that other activity on the system did not in the meantime flush pages from the cache"; whole pages; does not read beyond EOF; offset unchanged.

### Linux writeback-error reporting (S13-S15) and empirical study (S20)
- errseq_t: 32-bit, errno in low bits, counter, "SF" sampled flag; watchers keep cursor. Initial use for fsync/fdatasync/msync/sync_file_range (i.e. not read()).
- LWN 2017: with errseq_t "any application that holds an open file descriptor will reliably get an error return on the first fsync() call that is made after a writeback error occurs."
- LWN 2018: failed buffered writeback "usually includes discarding the data in the affected pages and marking them as being clean. So a read of the blocks that were just written will likely return something other than the data that was written." Errors before open() not seen by later fsync (4.13+). OpenBSD/NetBSD also can fail to report write errors.
- Rebello et al. ATC'20: ext4/XFS/Btrfs all mark pages clean after fsync failure; ext4 and XFS keep latest (unpersisted) copy in page cache, Btrfs reverts in-memory state; reads served from cache see new content, after eviction reads see old on-disk content ("non-overwritten block").

### Windows (S16-S19)
- Synchronous ReadFile at EOF: "ReadFile returns TRUE and sets the variable pointed to by the lpNumberOfBytesRead parameter to zero" (S17).
- Asynchronous: "the end-of-file indicator ... is when GetOverlappedResult returns FALSE and GetLastError returns ERROR_HANDLE_EOF" (S17). ReadFile page: read beginning at/after EOF "fails with the error ERROR_HANDLE_EOF"; read extending past EOF succeeds with bytes read before EOF (placed in the FILE_FLAG_OVERLAPPED conditions block).
- ReadFile returns when: requested bytes read; a write completes on pipe write end; async; error. Pipes: ERROR_BROKEN_PIPE when write handle closed (contrast POSIX 0); message-mode named pipe ERROR_MORE_DATA; zero bytes with TRUE on pipe means writer wrote zero bytes (so 0 is not EOF on pipes).
- Byte-range lock overlap: "If part of a file is locked by another process and the read operation overlaps the locked portion, this function fails." (Mandatory locking; contrast POSIX advisory locks.)
- Async handle: OVERLAPPED offset not auto-updated; buffer must not be touched until completion. Cancelled I/O completes with ERROR_OPERATION_ABORTED.
- FILE_FLAG_NO_BUFFERING: sizes and offsets "must be for a number of bytes that is an integer multiple of the volume sector size"; buffer addresses "should be physical sector-aligned ... Depending on the disk, this requirement may not be enforced."
- Attributes: FILE_ATTRIBUTE_OFFLINE "The data of a file is not available immediately ... physically moved to offline storage"; FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS: "Reading the file ... will cause at least some of the file/directory content to be fetched from a remote store."

## Existing models / classifications found
- POSIX file-type partition for read semantics: regular files (seekable; EOF=0; holes read as zero), pipes/FIFOs, sockets (read == recv no flags), terminals, device special files (implementation-defined after EOF), shared/typed memory objects (unspecified).
- POSIX three-tier normativity vocabulary: "shall" / "implementation-defined" / "unspecified" / "may fail"; plus informative RATIONALE.
- POSIX synchronized I/O completion: "data integrity completion" vs "file integrity completion" (O_RSYNC).
- Linux signal(7) "slow device" vs disk classification for interruptibility.
- Windows synchronous vs asynchronous (overlapped) handle model, with distinct EOF signalling.
- Windows logical vs physical sector distinction for unbuffered I/O.
- errseq_t "watcher/cursor" model for error reporting (writeback; not reads).
- Rebello et al. fault taxonomy: data-block, metadata-block, journal-block failures; outcomes "non-overwritten block", hole, unavailability.

## Convergences
- POSIX, Linux and Windows all permit fewer bytes than requested at EOF and signal EOF by zero bytes (synchronous); the caller must loop.
- Unwritten/hole regions read as zeros (POSIX read/lseek; Windows sparse attribute exists, but read-of-sparse-region semantics not verified in this track).
- Direct/unbuffered I/O imposes alignment constraints on both Linux and Windows, enforcement varies.

## Contradictions / tensions
- POSIX §2.9.7 requires read()/read() offset atomicity; Linux violated it before 3.14 (S6 BUGS).
- POSIX write() read-after-write guarantee vs Linux behaviour after writeback failure: page cache may serve unpersisted data then revert to old disk contents after eviction (S15, S20). Not a formal contradiction (POSIX excludes hardware errors from scope) but a semantic gap.
- Windows docs internally ambiguous: ReadFile says a read at/after EOF "fails with ERROR_HANDLE_EOF" while "Testing for the End of a File" says synchronous reads return TRUE with 0 bytes; the ReadFile statement is located in the overlapped-handle conditions list (inference: applies to async).
- POSIX empty-pipe-no-writer -> 0 vs Windows anonymous pipe -> FALSE/ERROR_BROKEN_PIPE; Windows TRUE/0 on pipe means zero-length write, not EOF.
- POSIX RATIONALE: EINTR possible even after some internal data movement; Linux signal(7): disk reads not interrupted at all.
- Btrfs vs ext4/XFS read content after fsync failure differ (S20).

## Gaps
- GENUINE-GAP: POSIX explicitly declines to specify behaviour on hardware/unrecoverable errors; no normative statement on what read returns after a failed writeback.
- GENUINE-GAP: no portable normative way to query direct-I/O alignment (Linux STATX_DIOALIGN 6.1+, Windows IOCTL).
- COVERAGE-GAP: macOS/FreeBSD read(2) and F_NOCACHE; Windows read semantics of sparse ranges and placeholder (Cloud Files) recall failures; Linux mmap SIGBUS on I/O error (mmap(2) text only mentions beyond-EOF); io_uring short reads; NFS close-to-open consistency (likely another track).
