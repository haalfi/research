# Track 09: Timing, latency and access-pattern behavior of reads across media and tiers

Scope: what the literature and normative/implementation documents say about *when* and *how fast*
a read outcome is observed: latency distributions and tails, device-internal causes of slow reads,
access-pattern (sequential vs random, readahead) effects, offline/archive tiers needing restore
before read, asynchronous completion semantics, and timeouts as an outcome.

Downloads: `/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/read-timing-performance-access/`
(text extracted with pdftotext / a tag-stripper run with `python3 -I`).

Evidence-type labels: NORMATIVE (standard), PEER-REVIEWED-EMPIRICAL, THEORETICAL, IMPLEMENTATION-DOC,
ENGINEERING-EVIDENCE. "Inference" marks my own reasoning, not the source's.

---

## 1. Sources consulted and access status

| # | Source | Type | Access |
|---|--------|------|--------|
| S1 | Dean, J. & Barroso, L.A. "The Tail at Scale." CACM 56(2):74-80, 2013. doi:10.1145/2408776.2408794. Author-hosted PDF https://www.barroso.org/publications/TheTailAtScale.pdf | engineering-evidence (Google measurements, magazine article, not a controlled study) | FULL TEXT (cacm.acm.org returned 403; author copy read) |
| S2 | Hao, M. et al. "The Tail at Store: A Revelation from Millions of Hours of Disk and SSD Deployments." USENIX FAST '16. https://www.usenix.org/system/files/conference/fast16/fast16-papers-hao.pdf | peer-reviewed-empirical | FULL TEXT |
| S3 | Gunawi, H.S. et al. "Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems." USENIX FAST '18. https://www.usenix.org/system/files/conference/fast18/fast18-gunawi.pdf | peer-reviewed (qualitative, 101 incident reports) | FULL TEXT |
| S4 | Yan, S. et al. "Tiny-Tail Flash: Near-Perfect Elimination of Garbage Collection Tail Latencies in NAND SSDs." USENIX FAST '17. https://www.usenix.org/system/files/conference/fast17/fast17-yan.pdf | peer-reviewed-empirical (simulation/emulation) | FULL TEXT (sections 1-3 read closely) |
| S5 | Aghayev, A. & Desnoyers, P. "Skylight—A Window on Shingled Disk Operation." USENIX FAST '15. https://www.usenix.org/system/files/conference/fast15/fast15-paper-aghayev.pdf | peer-reviewed-empirical | FULL TEXT |
| S6 | Ruemmler, C. & Wilkes, J. "An Introduction to Disk Drive Modeling." IEEE Computer 27(3):17-28, 1994. Course-mirror PDF https://pages.cs.wisc.edu/~dusseau/Classes/CS537-F05/Readings/ruemmler94introduction.pdf (HP Labs URL reset; author-prepared version noting it may differ from published copy) | peer-reviewed (model + trace calibration) | FULL TEXT |
| S7 | He, J. et al. "The Unwritten Contract of Solid State Drives." EuroSys '17. https://pages.cs.wisc.edu/~jhe/eurosys17-he.pdf | peer-reviewed (simulation over real traces) | FULL TEXT (sections 1, 3 read closely) |
| S8 | IEEE Std 1003.1-2024 / Open Group Base Specifications Issue 8, `aio_read()` https://pubs.opengroup.org/onlinepubs/9799919799/functions/aio_read.html | normative | FULL TEXT of section |
| S9 | Same, `aio_error()` https://pubs.opengroup.org/onlinepubs/9799919799/functions/aio_error.html | normative | FULL TEXT of section |
| S10 | Linux man-pages `io_uring_enter(2)` https://man7.org/linux/man-pages/man2/io_uring_enter.2.html | implementation-doc | FULL TEXT |
| S11 | Linux man-pages `readahead(2)` and `posix_fadvise(2)` (man7.org) | implementation-doc (posix_fadvise also POSIX-specified; only Linux page read) | FULL TEXT |
| S12 | Microsoft Learn "Synchronous and Asynchronous I/O"; "Asynchronous disk I/O appears as synchronous on Windows"; `ReadFile` reference | implementation-doc | FULL TEXT |
| S13 | Linux kernel docs "SCSI EH" https://www.kernel.org/doc/html/latest/scsi/scsi_eh.html | implementation-doc | FULL TEXT (sections 1.2-2.1) |
| S14 | AWS S3 User Guide "Restoring an archived object", "Understanding archive retrieval options"; S3 API Reference `GetObject` | implementation-doc (service documentation; "typically" figures are not SLAs) | FULL TEXT |
| S15 | Microsoft Learn "Blob rehydration from the archive tier" https://learn.microsoft.com/en-us/azure/storage/blobs/archive-rehydrate-overview | implementation-doc | FULL TEXT |
| S16 | SNIA LTFS Format Specification v2.5.1 (SNIA Standard; = ISO/IEC 20919) https://www.snia.org/sites/default/files/technical-work/ltfs/release/SNIA-LTFS-Format-2-5-1-Standard.pdf | normative (format, not timing) | FULL TEXT (searched; sections 3, 4.1, 6.x, 9.2 read) |

Unreachable / not used as evidence:
- Hillyer & Silberschatz, "On the Modeling and Performance Characteristics of a Serpentine Tape Drive," SIGMETRICS 1996 — dl.acm.org 403 (cloudflare-style site block). UNREACHABLE. (US patent 5,845,316 by same authors located but not read.)
- Chen, Koufaty, Zhang, "Understanding Intrinsic Characteristics and System Implications of Flash Memory based SSDs," SIGMETRICS 2009 — OSU TR URL 403. UNREACHABLE.
- cacm.acm.org copy of S1 — 403 (author copy used instead).
- HP Labs copy of S6 — connection reset; mirror used.
- No LTO vendor locate/load-time specification read (coverage gap).

---

## 2. Extracted findings (with verbatim quotes and locators)

### 2.1 Latency tails and their amplification (S1, Dean & Barroso 2013)
- Fan-out amplification (illustrative arithmetic, then measured): "consider a system where each server typically responds in 10ms but with a 99th-percentile latency of one second ... If a user request must collect responses from 100 such servers in parallel, then 63% of user requests will take more than one second" (p.76, "Component-Level Variability Amplified by Scale"). The 63% is 1-0.99^100 under an implicit independence assumption (inference).
- Measured Google service (Table 1): "The 99th-percentile latency for a single random request to finish, measured at the root, is 10ms. However, the 99th-percentile latency for all requests to finish is 140ms".
- Sources of variability listed include storage: "Solid-state storage devices provide very fast random read access, but the need to periodically garbage collect a large number of data blocks can increase read latency by a factor of 100 with even a modest level of write activity" (p.75-76, "Why Variability Exists"). Also energy management: power-saving modes "add additional latency when moving from inactive to active modes."
- Hedged requests on reads: "in a Google benchmark that reads the values for 1,000 keys stored in a BigTable table distributed across 100 different servers, sending a hedging request after a 10ms delay reduces the 99.9th-percentile latency for retrieving all 1,000 values from 1,800ms to 74ms while sending just 2% more requests."
- Tied requests on file-system reads (Table 2): "sending a tied request that does cross-server cancellation to another file system replica following 1ms reduces median latency by 16% and is increasingly effective along the tail ... achieving nearly 40% reduction at the 99.9th-percentile latency"; disk-utilization overhead "less than 1%".
- Rationale stated: "the source of latency is often not inherent in the particular request but rather due to other forms of interference."
- Methodology limits: magazine article; benchmarks are Google-internal, configuration details sparse; not peer-reviewed controlled experiments.

### 2.2 Field study of drive slowdowns (S2, Hao et al. FAST'16)
- Dataset: "over 450,000 disks and 4,000 SSDs over 87 days for an overall total of 857 million (disk) and 7 million (SSD) drive hours" (Abstract).
- Definitions: slowdown ratio Si = Li / Lmed (drive hourly average latency over RAID-group median); "we define 'slow' (unstable) drive hour when Si ≥ 2" (§1, Table 2).
- Finding #1: "0.2% of the time, a disk is more than 2x slower than its peer drives in the same RAID group (and 0.6% for SSD)" (Abstract; §4.1.1 gives 0.22%/0.58%).
- RAID tails: "disk and SSD-based RAIDs experience at least one slow drive (i.e., storage tail) 1.5% and 2.2% of the time" (Abstract).
- Persistence/locality: "40% and 35% of slow disks and SSDs respectively remain unstable for more than one hour ... 90% of disk and 85% of SSD slowdowns occur on the same day of the previous occurrence" (§1 summary).
- Extremes: "we observe several slowdown incidents as large as 2-4 orders of magnitude."
- Root cause / silence: "more than 95% of slowdown periods cannot be attributed to I/O size or rate imbalance" (Finding #8); "Slowdown is a 'silent' performance fault. A large majority of slowdowns are not accompanied with any explicit drive events" (Finding #9).
- Read relevance: ToleRAID proposal reads around a slow drive via parity ("tail-tolerant RAID can read" from parity drives, §5).
- Limitations stated by authors: "The first limitation of our dataset is the hourly aggregation, preventing us from performing micro analysis" (§6); read and write slowdowns merged ("we merge read and write slowdowns as I/O slowdown", §3.4); SSD dataset two orders smaller; single vendor's (NetApp) deployments; median-based metric.

### 2.3 Fail-slow hardware (S3, Gunawi et al. FAST'18)
- Defines fail-slow: "hardware that is still running and functional but in a degraded mode, slower than its expected performance" (§1), contrasted with fail-stop, fail-partial, fail-transient, corruption, byzantine.
- Examples: "disk throughput can drop by three orders of magnitude to 100 KB/s due to vibration, SSD operations can stall for seconds due to firmware bugs".
- Fault conversion (§3.2): masking transient errors costs time: "because error masking is not a free operation (e.g., retry delays, repair costs), when the errors are not rare, the masking overhead becomes the common case performance."
- Read-specific mechanisms (§4): SSD "Read retries with different voltages ... We observed as high as 4 retries in the field"; RAIN reconstruction "if the RAIN stripe width is N, N−1 additional reads must be generated to reconstruct the corrupt page"; disks: "media failures that forced the disks to retry every read operation multiple times before returning to the OS"; firmware: "a disk controller delayed I/O requests for tens of seconds"; "a single bad disk exhausted the RAID card resources causing many IO timeouts".
- Symptom classes (§3.3): "permanent slowdown, transient slowdown (up-and-down performance), partial slowdown (degradation of sub-components), and transient stop (e.g., occasional reboots)."
- Limitations: "the major limitation of our methodology: the lack of quantitative analysis" (§7) — anecdotal reports, no frequency estimates.

### 2.4 GC-blocked reads in SSDs (S4, Yan et al. FAST'17)
- "A GC operation causes long delays as the SSD cannot serve (blocks) incoming I/Os. Due to an ongoing GC, read latency variance can increase by 100×" (§1, citing others).
- Own measurement (simulated, §2): "with 5 KWPS noise, read operations become 15×, 19×, and 96× slower compared to no-GC scenarios, at 90th, 95th and 99th percentiles, respectively."
- Read-size effect: "at 85th percentile, a 64-KB read is 4× slower than a 32-KB read ... if a single page of a large read is blocked by a GC, the entire read cannot complete; as read size increases, the probability of one of the pages being blocked by GC also increases."
- Base vs TTFLASH: base "suffers from 5.6–138.2× GC-induced slowdowns" at 99–99.99th pct vs "only 1.0 to 2.6×" for TTFLASH.
- Limitation: results from SSDSim and QEMU/VSSIM emulation, not commercial firmware; depends on intra-plane copyback and RAIN.

### 2.5 SMR fragmented reads (S5, Aghayev & Desnoyers FAST'15)
- Drive-managed SMR uses a Shingle Translation Layer with a persistent cache of recently written data (§2).
- "When sequentially reading a region in an SMR drive, if the cache contains newer version of some of the blocks in the region, the head has to seek to the persistent cache and back, physically fragmenting a logically sequential read." (§4.4)
- Measured: in emulated SMR with multiple disk caches, "all having the same 10 ms average latency"; Seagate-SMR head video shows head "seeks back and forth between the OD and near-center and between the OD and the ID ... occasionally missing a rotation."
- Also (§4.2, persistent-cache tests): reading the same blocks back "in the written order" took ≈10 ms per block after asynchronous (volatile-cache-enabled) writes ("The contiguous placement also explains the 10 ms latency when reading blocks in the written order") but ≈5 ms after synchronous writes ("explains the 5 ms latency when reading blocks in the written order") — read latency depends on how the data was written (internal write placement), not just on LBA order.
- Limitation: two real drives (Seagate 5 TB/8 TB) plus emulations; kernel read-ahead disabled for tests ("Unless otherwise stated, we disabled kernel read-ahead").

### 2.6 Disk drive modeling and read-ahead (S6, Ruemmler & Wilkes 1994)
- Model accuracy metric: "demerit figure" = RMS horizontal distance between real and modeled service-time distributions.
- "By far the most important feature to model is the data-caching characteristics of the disk (112 percent relative demerit if this is ignored). The next most important features ... the data transfer model ... (20 percent demerit), and the seek-time and head-switching costs (9 percent demerit)." (Conclusions)
- Constant-time model: "Even using the mean I/O time rather than a fixed estimate results in a demerit factor that is 35 percent of the average I/O time."
- Read-ahead: "(Without readahead, two back-to-back reads would be delayed by almost a full revolution ...)"; "Aggressive read-ahead is optimal for sequential access, but it degrades random accesses because head and track switches typically cannot be aborted once initiated".
- Under-specification: read caching "is one of the least well specified areas of disk system behavior. For example, a read that partially hits in the cache may be partially serviced by the cache ... or it may simply bypass the cache altogether."
- "Average" seek time "can be misleading" since "independent seeks are rare in practice."
- Zoning: burst transfer rate on HP C2240 "varies from 3.1 megabytes per second at the inner zone to 5.3 MBps at the outermost zone".
- Limitation: 1990s HP drives (C2200A, 97560), HP-UX traces; mirror is a pre-publication version.

### 2.7 SSD "unwritten contract" (S7, He et al. EuroSys'17)
- Five rules; relevant to reads: "Request Scale: SSD clients should issue large data requests or multiple concurrent requests. A small request scale leads to low resource utilization and reduces immediate and sustainable performance" (§3.1); "Locality rule: SSD clients should access with locality. Workloads without locality can incur a poor immediate performance because frequent cache misses lead to many translation-related reads and writes" (§3.2).
- Finding: "some applications issue only a limited number of small read requests" (§1). Also "simple workload classifications (e.g., random vs. sequential writes) are orthogonal to important rules".
- Builds on Schlosser & Ganger's unwritten contract for HDDs (not read).
- Limitation: simulation (WiscSee) under traces; "rules" are performance conventions, not guarantees.

### 2.8 POSIX asynchronous read (S8, S9) — NORMATIVE
- `aio_read`: "The function call shall return when the read request has been initiated or queued to the file or device (even when the data cannot be delivered immediately)."
- Two-phase error detection: listed conditions "may be detected synchronously at the time of the call to aio_read(), or asynchronously"; if asynchronous, "the return status of the asynchronous operation is set to -1, and the error status ... is set to the corresponding value."
- Cancellation as outcome: "[ECANCELED] The requested I/O was canceled before the I/O completed due to an explicit aio_cancel() request."
- "After a successful call to enqueue an asynchronous I/O operation, the value of the file offset for the file is unspecified."
- `aio_error`: "If the operation has not yet completed, then the error status shall be equal to [EINPROGRESS]."
- Observation: POSIX aio_read defines no timeout for the operation itself (inference from absence in the section read).

### 2.9 Linux io_uring (S10) — IMPLEMENTATION-DOC
- Ordering: "while I/O is initiated in the order in which it appears in the submission queue, completions are unordered" (IORING_OP_FSYNC entry); ordering requires linked SQEs, IOSQE_IO_DRAIN, or waiting for CQEs.
- Error channel: "The errors related to a submission queue entry will be returned through a completion queue entry ... rather than through the system call itself."
- Timeout as an outcome: IORING_OP_LINK_TIMEOUT "will cancel the linked command, unless the linked command completes before the timeout. The timeout will complete with -ETIME if the timer expired and the linked request was attempted canceled, or -ECANCELED if the timer got canceled because of completion of the linked request." Clock: CLOCK_MONOTONIC.

### 2.10 Windows overlapped I/O (S12) — IMPLEMENTATION-DOC
- "the system reserves the right to make an operation synchronous if it needs to. So it is best if you write the program to correctly handle an I/O operation that may be completed either synchronously or asynchronously."
- Causes of synchronous completion: NTFS compression ("all operations are made synchronous"), NTFS encryption, extending writes, cache hits ("an I/O request can be completed immediately when the data is cached in memory"), cache-manager saturation on many non-cached reads.
- ReadFile: "The GetLastError code ERROR_IO_PENDING is not a failure; it designates the read operation is pending completion asynchronously." With completion ports "a completion packet will also be sent even though the I/O operation completed immediately."
- Cache behaviour depends on access pattern: FILE_FLAG_SEQUENTIAL_SCAN vs FILE_FLAG_RANDOM_ACCESS; FILE_FLAG_NO_BUFFERING "is the best way to guarantee that I/O requests are asynchronous".
- Communications devices: ReadFile behavior "is determined by the current communication time-out"; "Unpredictable results can occur if you fail to set the time-out values."

### 2.11 Linux readahead / posix_fadvise (S11) — IMPLEMENTATION-DOC
- `readahead()`: subsequent reads "will be satisfied from the cache, and not block on disk I/O (assuming the readahead was initiated early enough and that other activity on the system did not in the meantime flush pages from the cache)." BUGS: "it may block while it reads the filesystem metadata needed to locate the requested blocks."
- `posix_fadvise`: "The advice is not binding; it merely constitutes an expectation on behalf of the application." Linux: "POSIX_FADV_SEQUENTIAL doubles this size, and POSIX_FADV_RANDOM disables file readahead entirely." WILLNEED: "The amount of data read may be decreased by the kernel depending on virtual memory load."

### 2.12 Linux SCSI error handling / timeouts (S13) — IMPLEMENTATION-DOC
- On timeout `scsi_timeout()` may call `eh_timed_out()` returning SCSI_EH_RESET_TIMER ("more time is required ... Timer is restarted"), SCSI_EH_NOT_HANDLED, or SCSI_EH_DONE.
- "If the abort is successful the command will either be retried (if the number of retries is not exhausted) or terminated with DID_TIME_OUT."
- "scmds are retried iff its sdev is still online (not offlined during EH), REQ_FAILFAST is not set and ++scmd->retries is less than scmd->allowed."
- So a timed-out read can become: success after retry, DID_TIME_OUT failure, or failure after device offlining (inference summarising the documented paths).

### 2.13 Archive tiers requiring restore/rehydration (S14, S15) — IMPLEMENTATION-DOC
- S3: "objects that are stored in the S3 Glacier Flexible Retrieval or S3 Glacier Deep Archive storage classes are not immediately accessible. To access an object in these storage classes, you must restore a temporary copy of the object to its S3 bucket for a specified duration (number of days)."
- GetObject error: "InvalidObjectState — Object is archived and inaccessible until restored." "HTTP Status Code: 403".
- Restore state visible via head-object `Restore: ongoing-request="true"` / `ongoing-request="false", expiry-date=...`; completion event `s3:ObjectRestore:Completed`.
- Retrieval times ("typically"): Expedited "Objects under 250 megabytes in size are typically made available within 1–5 minutes"; Standard "typically finish within 3–5 hours" (Flexible Retrieval) and "within 12 hours" (Deep Archive); Bulk 5–12 h / within 48 h. ">5 TB ... a 50-terabyte S3 Glacier Flexible Retrieval object could take up to 48 hours".
- Restored copy expires: "stored only for the number of days that you specify."
- Azure: "An archived blob is offline and can't be read or modified. To access its data, first rehydrate the blob to an online tier". Standard priority "might take up to 15 hours to complete for objects under 10 GB"; High "might complete in less than one hour for objects under 10 GB". "The 10 GiB/hour limit applies at the storage account level ... they do not scale linearly for bulk operations." "You can't cancel a Set Blob Tier request after it starts. During rehydration, the blob's access tier remains archive." Copy Blob: "The new blob might appear in the parent container before rehydration is complete, but its tier remains archive."

### 2.14 LTFS (S16) — NORMATIVE (format)
- Targets "Direct file and partial file recall from sequential access media" (§3 usage).
- Extents: examples "are always displayed in file offset order, but they may appear in any order on a partition, or even in different partitions" (§6.3). Inference: a logically sequential file read on tape may require repositioning between partitions/extents; the spec does not state timing.
- Sparse regions "are not stored on the storage media and are implicitly filled with bytes containing the value zero (0x00)" (§4.1.23).
- accesstime "may contain the date and time when the content of the file was last read. Implementers ... may choose to avoid or otherwise minimize recording Index updates that only change the accesstime element" (§9.2.x) — reading may (optionally) cause metadata writes.
- No timing/latency requirements in LTFS (searched for latency/locate/seek: none normative).

---

## 3. Existing models / classifications found
- Tail-tolerance techniques (S1): hedged requests, tied requests, micro-partitions, selective replication, latency-induced probation, good-enough responses, canary requests. "Tail-tolerant" by analogy to fault-tolerant.
- Drive slowdown model (S2): Si = Li/Lmed; slow hour Si≥2 (or 1.5); RAID tail T^k (k-th largest slowdown); "tail hour" = RAID hour with T1 ≥ 2.
- Fault models (S3): fail-stop, fail-partial, fail-transient, corruption, byzantine, and fail-slow; fail-slow symptom classes: permanent, transient, partial slowdown, transient stop; fault conversion between classes.
- GC blocking granularity (S4): controller-blocking, channel-blocking, plane-blocking GC.
- Disk model components (S6): mechanism (seek, rotation, head switch, zoning, track skew, sparing), controller (bus, fence, caching/read-ahead, immediate reporting); "demerit figure" accuracy metric.
- SSD unwritten contract (S7): Request Scale, Locality, Aligned Sequentiality, Grouping by Death Time, Uniform Data Lifetime.
- SMR (S5, citing T10/T13 drafts): drive-managed, host-aware (sequential-write-preferred), host-managed (sequential-write-required).
- Async read state machine (S8/S9/S10/S12): queued/in-progress (EINPROGRESS / ERROR_IO_PENDING) → completed success (bytes) | error | canceled (ECANCELED) | timed out (io_uring -ETIME on link timeout; SCSI DID_TIME_OUT).
- Archive tier state (S14/S15): archived/offline → restore pending (ongoing-request=true / tier remains archive) → restored/online (with expiry for S3 Glacier copies).

## 4. Convergences
- SSD GC as read-latency cause: S1 ("factor of 100"), S4 (simulation, up to 138× at 99.99th), S3 (heavy GC in partially-failing SSD), S2 (cites GC; MLC>SLC slowdowns). Note S1 and S4 both partly rest on the same earlier citations; independence of evidence is limited.
- Interference rather than inherent request cost causes tails: S1 (explicit) and S2 (>95% not attributable to workload imbalance; "internal characteristics" of drives).
- Error masking (retry/ECC/reconstruction) converts correctness problems into latency: S3, S13 (SCSI retries), S2 (sector re-reads).
- Read latency depends on history/layout not visible in the interface: S5 (SMR persistent cache), S6 (read cache under-specified), S7 (FTL translation cache), S14/S15 (tier state).
- "Asynchronous" APIs may complete synchronously; completion observed via a separate channel: S8, S10, S12.

## 5. Contradictions / tensions
- Magnitude of GC effect: S1 says "factor of 100 with even a modest level of write activity" (general statement, citing others); S4's simulated base case yields 15× at p90 and 96× at p99 under 5 KWPS; S2 field data at hourly-average granularity shows 2x slowdowns only 0.58% of SSD hours. These measure different things (per-I/O percentile vs hourly mean relative to peers), so not a direct contradiction but a granularity mismatch.
- Workload blame: common belief that slow drives are busier drives is refuted in S2 (Finding #8). S7 by contrast emphasises that client access patterns (request scale, locality) drive SSD performance. Different questions (relative peer slowdown vs absolute throughput).
- Read-ahead benefit: S6 says aggressive read-ahead degrades random access; S11 Linux FADV_RANDOM disables readahead; S5 notes SMR fragmented reads defeat sequential assumptions — the "sequential is fast" convention is conditional.
- S14 timeline examples ("typically") are not guarantees; Azure explicitly says single-blob timelines "do not scale linearly".

## 6. Gaps
- COVERAGE-GAP: Tape locate/load latency models (Hillyer & Silberschatz 1996, LTO vendor specs) unreachable or not found; LTFS spec contains no timing.
- COVERAGE-GAP: Optical media and robotic library mount latency: no source read.
- COVERAGE-GAP: Chen/Koufaty/Zhang 2009 SSD read/write interference measurements unreachable.
- COVERAGE-GAP: NVMe/SATA normative command timeout semantics (e.g., NVMe spec abort/timeout) not read in this track (see track 03 possibly).
- GENUINE-GAP (per S2 §6 and S3 §7): no large-scale per-I/O (sub-hour) field latency distributions for reads specifically; S2 merges reads and writes; S3 lacks quantitative frequencies.
- GENUINE-GAP (per S2 §6): SMR-based RAID read performance in the field unstudied as of 2016.
- GENUINE-GAP (S6): drive read-cache policy is "one of the least well specified areas" — no normative spec of partial cache hits.
- Inference: none of the normative async APIs read (POSIX aio) defines a per-operation deadline; timeouts are layered on by implementations (io_uring link timeout, SCSI EH) or applications.
