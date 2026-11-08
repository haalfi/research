# Track 04: Empirical field studies of read errors and corruption in storage media

Scope: field studies (and some lab and theory sources that matter for them) of what a storage device
or stack returns when data is read: explicit errors, retried or corrected reads, and silently
corrupted data. Terms are kept as each source uses them. Any inference of mine is marked **[inference]**.

Download dir (not in the repo): `/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/media-error-field-studies/`
I extracted text with `pdftotext -layout` and read it in the relevant sections listed below.

## 1. Sources consulted

| # | Source | Type | Access | Sections read |
|---|---|---|---|---|
| S1 | Bairavasundaram, Goodson, Pasupathy, Schindler. "An Analysis of Latent Sector Errors in Disk Drives." SIGMETRICS 2007. research.cs.wisc.edu/adsl/Publications/latent-sigmetrics07.pdf | peer-reviewed field study | FULL TEXT | Abstract, Table 1, §2 (2.2-2.4), §3.2-3.3, §4.2, §5.2-5.5 |
| S2 | Bairavasundaram, Goodson, Schroeder, Arpaci-Dusseau, Arpaci-Dusseau. "An Analysis of Data Corruption in the Storage Stack." FAST 2008. usenix.org/legacy/event/fast08/tech/full_papers/bairavasundaram/bairavasundaram.pdf | peer-reviewed field study | FULL TEXT | Abstract, §1, §2.2-2.3 (Table 1), §3, §4.1, §4.3.3-4.6 (Table 2), §5, §6.1.1 |
| S3 | Schroeder, Damouras, Gill. "Understanding latent sector errors and how to protect against them." FAST 2010. usenix.org/legacy/events/fast10/tech/full_papers/schroeder.pdf | peer-reviewed field study plus statistical modelling | FULL TEXT | Abstract, §1, §2, §3.3-3.4, §5.1-5.2 |
| S4 | Schroeder, Lagisetty, Merchant. "Flash Reliability in Production: The Expected and the Unexpected." FAST 2016. usenix.org/system/files/conference/fast16/fast16-papers-schroeder.pdf | peer-reviewed field study (Google) | FULL TEXT | Abstract, §2, §3 (Table 2), §4.2.3-4.2.5, §5.1-5.4, §6.1, §8 |
| S5 | Meza, Wu, Kumar, Mutlu. "A Large-Scale Study of Flash Memory Failures in the Field." SIGMETRICS 2015. users.ece.cmu.edu/~omutlu/pub/flash-memory-failures-in-the-field-at-facebook_sigmetrics15.pdf | peer-reviewed field study (Facebook) | FULL TEXT | Abstract, Table 1, §2.2-2.5, §3.2, §4.2, §6 (limitations) |
| S6 | Maneas, Mahdaviani, Emami, Schroeder. "A Study of SSD Reliability in Large Scale Enterprise Storage Deployments." FAST 2020. usenix.org/system/files/fast20-maneas.pdf | peer-reviewed field study (NetApp) | FULL TEXT | Abstract, §2, §4 (Table 2), §5.6-5.7 (skimmed) |
| S7 | Narayanan et al. "SSD Failures in Datacenters: What? When? and Why?" SYSTOR 2016. microsoft.com/en-us/research/wp-content/uploads/2016/08/a7-narayanan.pdf | peer-reviewed field study (Microsoft) | FULL TEXT | Abstract, §1 contributions, §3.2-3.3 (Table 3) |
| S8 | Schroeder, Pinheiro, Weber. "DRAM Errors in the Wild: A Large-Scale Field Study." SIGMETRICS 2009. cs.toronto.edu/~bianca/papers/sigmetrics09.pdf | peer-reviewed field study (Google) | FULL TEXT | Abstract, §1, §2.1-2.3, §3.1-3.2 |
| S9 | Panzer-Steindel, B. "Data integrity." CERN/IT, Draft 1.3, 8 April 2007. indico.cern.ch/event/13797/.../Data_integrity_v3.pdf | internal engineering report (not peer-reviewed) | FULL TEXT | whole document |
| S10 | Schroeder, Gibson. "Disk failures in the real world: What does an MTTF of 1,000,000 hours mean to you?" FAST 2007 | peer-reviewed field study | FULL TEXT (only the abstract/introduction used) | Abstract, §1-2 |
| S11 | Pinheiro, Weber, Barroso. "Failure Trends in a Large Disk Drive Population." FAST 2007 | peer-reviewed field study (Google) | FULL TEXT (§3.5 used) | §3.5.1-3.5.2 |
| S12 | Jiang, Hu, Zhou, Kanevsky. "Are Disks the Dominant Contributor for Storage Failures?" FAST 2008 | peer-reviewed field study (NetApp) | FULL TEXT | Abstract, §1, §2.3 |
| S13 | Krioukov et al. "Parity Lost and Parity Regained." FAST 2008 | peer-reviewed formal analysis (model checking) | FULL TEXT | Abstract, §1, §2.2-2.3, §3 intro |
| S14 | Cai, Ghose, Haratsch, Luo, Mutlu. "Error Characterization, Mitigation, and Recovery in Flash-Memory-Based Solid-State Drives." Proc. IEEE 105(9), 2017. arXiv:1706.08642v3 | peer-reviewed survey plus lab characterization | FULL TEXT (arXiv) | §4.4, §4.5, §4.6, §5.4, §8 intro |
| S15 | Slattery, Lu, Zheng, Byers, Tang. "Stability Comparison of Recordable Optical Discs." J. Res. NIST 109(5), 2004. nvlpubs.nist.gov/nistpubs/jres/109/5/j95sla.pdf | peer-reviewed accelerated-aging lab study | FULL TEXT | §1-3 |
| U1 | NERSC tape reliability audit (eScholarship qt5wp6d6rd) | field study (tape) | **UNREACHABLE** (the PDF came back with an empty 202 body; the landing page rendered empty) | none; no claims based on it |
| U2 | NERSC LTUG 2013 T10KC slides; WGBH LTO-4 Code4Lib 2015; Quantum IEEE TV talk; mptapes.com | presentations and vendor material | NOT READ (found only as search leads) | none |

## 2. Extracted findings (verbatim quotes with locators)

### S1 Bairavasundaram et al. 2007: latent sector errors (NetApp, 1.53M disks, 32 months)
- Definition (§2.2), three mutually exclusive error types:
  - "Latent Sector Errors This error occurs when a particular disk sector cannot be read or written, or when there is an uncorrectable ECC error. Any data previously stored in the sector is lost."
  - "Not-Ready-Condition Errors ... the disk drive is not ready to handle a command from the host ... They are often resolved by waiting and retrying."
  - "Recovered Errors These 'errors' are returned by disks when an access to a sector required disk-level retry or error-correction to retrieve the data. Although the operation completed successfully and returned the data, they may serve as a warning."
- Signalling (§2.2): on a latent sector error, "SCSI returns status code Check condition with the sense key Medium error (0x03)".
- Read/write asymmetry in repair (§2.3): "Sparing and re-mapping can only occur on detected write errors; read errors require higher-level mechanisms such as RAID reconstruction to obtain the lost data."
- Incidence (§5.2): "53,820 (3.45%) disks develop one or more latent sector errors over the period of 32 months"; by class, "about 8.5% of all nearline disks ... while only 1.9% of all enterprise class disks".
- Spatial locality (§5.4.2, Obs. 10): "for most disk models the probability of other latent sector errors within a 10 MB radius of an existing error is 0.5."
- Temporal locality (Obs. 12): "for 54.8% of nearline error disks and 62.0% of enterprise class error disks, at least one additional error is developed within one month of the first ever error."
- Discovery (§5.5, Obs. 13): "86.6% of all latent sector errors in nearline disks and 61.5% ... in enterprise class disks are discovered by verify operations, while reads discover 13.4% ... and 19.1%".
- Methodology limit (§4.2): "Our study of error rate observations reflects lower bounds." Testing before shipment and automatic remapping in nearline drives hide some errors.
- Correlation (Obs. 15): for nearline disks, P(LSE | not-ready-condition) = 0.38 against an unconditional 0.085.

### S2 Bairavasundaram et al. 2008: silent data corruption (same population, 41 months)
- Definition (§1): "silent data corruption, where the data is silently corrupted with no indication from the drive that an error has occurred."
- Classification by detection mechanism (Table 1, §2.3), in the paper's words: "We classify data corruption into three categories based on how it is discovered":
  - Checksum mismatch (CM): causes "Bit-level corruption; torn write; misdirected write"; detected by the "RAID block checksum" on "Any disk read".
  - Identity discrepancy (ID): causes "Lost or misdirected write"; detected by "File system-level block identity" on "File system read".
  - Parity inconsistency (PI): causes "Memory corruption; lost write; bad parity calculation"; detected by "RAID parity mismatch" during a "Data scrub". PI is "a mismatch between the parity computed from data blocks and the parity stored on disk despite the individual checksums being valid."
- Definitions of the write faults behind them: lost write, "a write destined for disk is not written but thought of as written"; torn write, "only a portion of the data block is written successfully"; misdirected write, "the data is written to either the wrong disk or the wrong location on disk".
- Rates (§4.1): "3088 of the 358,000 nearline disks (0.86%) and 767 of the 1.17 million enterprise class disks (0.065%)". For corrupt disks, "the mean number of mismatches per disk is 104, the median is 3 and the mode ... is 1".
- Locality (Obs. 10): "Much of the observed locality is due to consecutive disk blocks developing corruption." "on average 3.4 consecutive blocks are affected."
- Discovery (§4.5): scrubbing finds "about 49% of checksum mismatches in nearline disks ... and 73% ... in enterprise class disks"; "RAID reconstruction discovers about 8% of the checksum mismatches in nearline disks."
- Block-number dependence (§6.1.1): "specific block numbers could be much more likely to experience corruption than other block numbers", which suggests "hardware or firmware bugs that affect specific sets of block numbers".
- Compared with LSEs (§4.6, Table 2): "The probability of developing checksum mismatches is about an order of magnitude smaller than that for latent sector errors."
- Caveat on cause attribution (§2.3): "In many cases, the cause of corruption cannot be identified."

### S3 Schroeder, Damouras, Gill 2010 (subset of S1 data)
- Definition: "Latent sector errors (LSEs) refer to the situation where particular sectors on a drive become inaccessible."
- Latency in detection (§2): "The timestamps in our data refer to the time when the error was detected, not necessarily when it first happened."
- Burstiness and the Poisson assumption (§3.4): "for 55–85% of drives, all errors are concentrated in the same 2-week period"; "We fitted a Poisson distribution ... and found the Poisson distribution to be a poor fit in both cases ... a Pareto distribution is a much better fit."
- Spatial skew (§3.3): "between 20% and 50% of all errors are located in the first 10% of the drive's logical sector space."
- Assumption about reads (§5.1): "it seems unlikely that the read frequency in a system (in contrast to the write frequency) would have a major impact on errors". The authors add: "we are hesitant to assume that the scrub frequency has zero impact on the error rate." This is the authors' judgement, not a measurement.

### S4 Schroeder, Lagisetty, Merchant 2016 (Google flash, 6 years, 10 models)
- Error taxonomy (§2-3). Transparent: correctable error, read error ("experiences a (non-ECC) error, but after retrying it succeeds"), write error, erase error. Non-transparent: "Uncorrectable error: A read operation encounters more corrupted bits than the ECC can correct"; "Final read error: ... even after retries the error persists"; final write error, meta error, "Timeout error: An operation timed out after 3 seconds", response error.
- Severity: "some of these errors (final read error, uncorrectable error, meta error) lead to data loss, unless there is redundancy at higher levels".
- Prevalence (§3.1): "between 20-63% of drives experience at least one such [final read] error and between 2-6 out of 1,000 drive days are affected"; final read errors are "almost exclusively due to bit corruptions beyond what the ECC can correct". Correctable errors affect "the majority of drive days (61-90%)".
- Retries rarely help reads (§3.2): "Errors encountered during a read operations are rarely transparent, likely because they are due to bit corruption beyond what ECC can correct, a problem that is not fixable through retries."
- UBER critique (§5.1): "We find no evidence for a correlation between the number of reads and the number of uncorrectable errors. The correlation coefficients are below 0.02". The conclusion: "UBER is not a meaningful metric". In contrast, correctable errors correlate with reads (Spearman > 0.9).
- RBER does not predict UEs (§4.2.5, §5.2): "there is no significant correlation between uncorrectable errors and RBER".
- Read disturb (§4.2.3): "there are drive models, where the effect of read disturb is significant enough to affect RBER". However (§5.4): "read disturb errors, write disturb errors or incomplete erase operations are not a major factor in the development of UEs."
- Compared with HDDs (§8): flash has a lower replacement rate, but "they experience significantly higher rates of uncorrectable errors than hard disk drives."

### S5 Meza et al. 2015 (Facebook flash, about 4 years, snapshot data)
- Operational definition (§2.2): results cover only "SSD-uncorrectable but host-correctable errors ... We refer to the occurrence of such uncorrectable errors in an SSD as an SSD failure."
- Incidence (§3.2): "between 4.2% and 34.1% of the SSDs ... reporting uncorrectable errors"; "the top 10% of SSDs with the most errors have over 80% of all uncorrectable errors"; the distribution is close to a "Weibull distribution with a shape parameter of 0.3".
- Read disturb (§4.2): "the effect of read-induced errors in the SSDs we examine is not predominant compared to other effects such as write-induced errors."
- Limitations (§2.5, §6): the data is a single snapshot with no time series; "We did not examine the rate of data loss"; the error-correction scheme with host forwarding "may not be employed on other SSDs (and may not even be possible for some SSDs, such as those that use the NVMe interface)".

### S6 Maneas et al. 2020 (NetApp enterprise SSDs, about 1.4M drives, 30 months)
- Replacement-reason taxonomy (Table 2), grouped into severity categories A-D with the recovery action and the scope of data affected. Category B, "Lost Writes": "A lost write is detected when the contents of a 4K WAFL block (read from the SSD) are inconsistent based on its signature, which includes attributes and version number" (13.54% of replacements). Category A, "SCSI Error" (32.78%): "these errors could be due to ECC errors originating from the drive's DRAM".
- Attribution caveat: "it is somewhat less clear whether it is the drive or other layers in the stack that are to blame for the lost write."

### S7 Narayanan et al. 2016 (Microsoft, >500k SSDs, about 3 years)
- Symptoms from SMART: "Four symptoms - Data Errors (Uncorrectable and CRC), Sector Reallocations, Program/Erase Failures and SATA Downshift".
- "CRC and Uncorrectable errors: These events stem from data errors in media or errors in the communication link. Even if such symptoms may not necessarily propagate to higher levels because of ECC ... they could have performance consequences."
- UBER (Table 3) ranges from 1.24e-14 to 1.27e-11 per device by model. The UBER here counts SSD-uncorrectable errors that "can be host-correctable". The paper reports UBER "is still at least an order of magnitude higher than the target rates".

### S8 Schroeder, Pinheiro, Weber 2009 (DRAM, Google)
- Definition (§1): "A memory error is an event that leads to the logical state of one or multiple bits being read differently from how they were last written." Soft errors "randomly corrupt bits but do not leave physical damage"; hard errors "corrupt bits in a repeatable manner because of a physical defect".
- Rates: "25,000 to 70,000 errors per billion device hours per Mbit and more than 8% of DIMMs affected by errors per year"; "1.3% of machines are affected by uncorrectable errors per year".
- Limit (§2.3): the infrastructure "does not allow us to reliably distinguish these types of errors [hard vs soft]". The claim that hard errors dominate is therefore an inference from the authors' statistical analysis.

### S9 Panzer-Steindel 2007 (CERN, internal report)
- Write-then-read probe (§1): it "writes a ~2 GB file containing special bit patterns and afterwards reads the file back and compares the patterns ... About 5 weeks of running on 3000 nodes revealed 500 errors on 100 nodes."
- Error shapes observed: single bit errors (10%), "sector- or page-sized regions of corrupted data (10%)", and "64k regions of corrupted data ... (80% of all errors)", linked to a disk-firmware problem.
- RAID read path: "The RAID controllers don't check the 'parity' when reading data from RAID 5 file systems."
- End-to-end measurement: "33700 files were checked (~8.7 TB) and 22 mismatches found ... one bad file in 1500 files". For compressed files, "with a likelihood of 99.8 % a SINGLE bit error makes the whole file unreadable".
- Conclusion: "the different protection mechanisms don't work 100% , i.e. not every errors in the data flow is correctly treated and reported to the upper layers."
- Status: Draft 1.3, an internal report that was not peer-reviewed. The causes it gives are the author's attributions.

### S10 Schroeder & Gibson 2007 / S11 Pinheiro et al. 2007 (disk replacement context)
- S10: "annual disk replacement rates typically exceed 1%, with 2-4% common and up to 13% observed on some systems", against a datasheet-implied AFR of "at most 0.88%".
- S11 §3.5.1: "After the first scan error, drives are 39 times more likely to fail within 60 days than drives without scan errors." Scan errors come from background surface scans by the drive itself. Fewer than 2% of drives showed them.

### S12 Jiang et al. 2008 (storage subsystem failures, about 1.8M disks)
- Failure types along the I/O path (§2.3): Disk Failure; Physical Interconnect Failure ("affected disks appear to be missing from the system"); Protocol Failure ("disks are visible to the storage layer but I/O requests are not correctly responded by disks"); Performance Failure ("a disk cannot serve I/O requests in a timely manner ... mainly caused by partial failures, such as unstable connectivity or when disks are heavily loaded with disk-level recovery").
- Abstract: "disk failures ... contribute to 20-55% of storage subsystem failures".

### S13 Krioukov et al. 2008 (formal, model checking)
- Error outcomes (§2.3): "Data recovery: ... detects the error, and uses parity to successfully recover data"; "Data loss: ... detects the error, but is unable to successfully recover data. In this case, the storage system reports an error to the user"; "Corrupt data: ... does not detect the error, and therefore returns corrupt data to the user."
- Parity pollution: "corrupt data in one block of a stripe spreads to other blocks through various parity calculations". Analysing real systems under single-error conditions, the authors "find flaws in every scheme".

### S14 Cai et al. 2017 (Proc. IEEE; lab characterization plus survey)
- Five major error sources (§4): P/E cycling, program, cell-to-cell program interference, data retention, read disturb.
- "Retention errors are caused by charge leakage over time after a flash cell is programmed, and are the dominant source of flash memory errors" (§4.4).
- "Read disturb is a phenomenon in NAND flash memory where reading data from a flash cell can cause the threshold voltages of other (unread) cells in the same block to shift to a higher value" (§4.5).
- Read-retry (§5.4): the controller rereads with different read reference voltages "until it either successfully reads the data ... or is unable to correctly read the data using all of the read reference voltages", and this "can significantly increase the overall read operation latency".
- Read reclaim: "some flash vendors specify a maximum number of tolerable reads for a flash block, at which point read reclaim rewrites the data to a new block".
- §4.6 summarizes the field studies: read disturb and incomplete erase "have yet to become a major source of uncorrectable errors at the system level."

### S15 Slattery et al. 2004 (NIST; optical, accelerated aging)
- End-of-life definition: "The end of life of a disc can be defined as the time when an uncorrectable error occurs. Although the disc may still be readable after this point, some information has been lost."
- Thresholds from the CD/DVD specifications: "BLER may be a maximum of 220 per second"; "E32 errors represent lost data and therefore no E32 errors are allowed"; for DVD, "PI Sum8 may have a maximum of 280 PI errors" and "no PO errors are permitted".
- Applicability: "The error rates are not representative of discs stored in typical, normal or ideal storage conditions." The sample was "too small" for a life-expectancy estimate.

## 3. Models and classifications found in the sources (none are mine)
1. **NetApp HDD error triad** (S1): latent sector error, not-ready-condition error, recovered error. The three are mutually exclusive and defined by the SCSI error code.
2. **Corruption classes by detection mechanism** (S2): checksum mismatch, identity discrepancy, parity inconsistency. Each is tied to a detecting operation: any read, a file-system read, or a scrub.
3. **Write-fault vocabulary** (S2, S13): lost write, torn write, misdirected write, plus bit-level corruption. These faults happen at write time but only show up when the data is read.
4. **Error outcome trichotomy** (S13): data recovery, data loss (an error is reported), corrupt data (wrong data is returned with no error).
5. **Transparent vs non-transparent flash errors** (S4): correctable, retry-recovered read/write, and erase errors on one side; uncorrectable, final read/write, meta, timeout, and response errors on the other.
6. **Soft vs hard memory errors; CE vs UE** (S8).
7. **Storage-subsystem failure types along the I/O path** (S12): disk, physical interconnect, protocol, performance.
8. **Five NAND error sources** (S14). Mitigation for reads: read-retry, refresh, read reclaim.
9. **Statistical models of LSE arrival** (S3): Pareto fits better than the commonly assumed Poisson. **Error count per SSD** (S5) is close to Weibull with shape 0.3.
10. **SSD replacement-reason categories A-D**, with recovery action and scope (S6).
11. **Optical media error metrics from the specifications** (S15): BLER/E32 for CD, PI/PO for DVD, with end of life defined as the first uncorrectable error.

## 4. Convergences
- Errors cluster in space and time. Disk LSEs cluster within 10 MB (S1). Checksum mismatches hit consecutive blocks (S2). LSE bursts fall within 2 weeks (S3). Subsystem failures are bursty (S12). Flash errors concentrate on a few devices, with the top 10% of SSDs holding more than 80% of UEs (S5). The independent-Poisson assumption is contradicted in every case where it was tested (S3).
- A device that has had one error is a strong predictor of more: S1 (Obs. 9, 12), S4 (prior errors and bad blocks), S11 (scan errors), S7 (symptoms come before failure).
- Errors are latent: they are found only when the data is read, often by scrubbing rather than by the application (S1: >60% via verify; S2: 49-73% via scrub). Detection time is not occurrence time (S3).
- Device-level ECC and error reporting do not cover everything. Silent corruptions get past drive ECC and are caught only by end-to-end checks such as checksums or identity information (S2, S9). Lost writes come back as stale but internally consistent data, which only identity or version checks catch (S2, S6).
- Field rates exceed datasheet or lab expectations: replacement rates (S10, S7), DRAM error rates (S8), and UBER above target (S7).

## 5. Contradictions and tensions
- **Read disturb in the field.** S5 (Facebook) says read-induced errors are "not predominant". S4 (Google) finds read disturb significant enough to affect RBER for some models, but not a factor for UEs. S14 (lab) characterizes read disturb as a real mechanism. These may be compatible, because they measure different things (RBER vs UE vs failure incidence) **[inference]**.
- **UBER as a metric.** S4 argues UBER is "not a meaningful metric" in the field because UEs do not scale with reads. S5 and S7 still report UBER per platform or model. In S5 and S7, UBER counts SSD-uncorrectable but host-correctable errors, which is a different numerator.
- **Measured vs vendor BER** (S9). The disk verify found about 300 errors against about 850 expected from the vendor BER. ECC memory errors were "4 orders of magnitude lower than expected", though the author warns that IPMI reporting may be incomplete. Whether vendor figures are conservative or optimistic depends on the component, and on how complete the reporting is.
- **SLC vs MLC.** S4 finds no evidence that SLC is more reliable in the field within typical lifetimes, which contradicts the common expectation (noted only, outside the core scope).
- **Enterprise vs nearline.** Enterprise disks are less likely to get a first error, but once they have one they get as many further errors (S1) or more (S2).

## 6. Gaps
- COVERAGE-GAP: tape field studies. The NERSC tape audit (eScholarship) was UNREACHABLE. Other tape sources were found only as search leads (vendor and practitioner talks) and were not read. No tape claims are made.
- COVERAGE-GAP: Maneas et al. 2022 (ACM TOS extension) and Maneas et al. on RAID-group correlations were not retrieved.
- COVERAGE-GAP: later DRAM studies (e.g., Sridharan et al. ASPLOS 2015, Hwang et al. ASPLOS 2012) and NVMe-era SSD field studies (e.g., Alibaba/Tencent studies after 2020) were not read.
- GENUINE-GAP: most field studies cannot observe corruption that no layer detects. All reported silent-corruption rates are counts of corruption that was detected, and S1 and S2 say explicitly that they are lower bounds.
- GENUINE-GAP: S5 and S6 report no data-loss rate at the application level. S5 says "We did not examine the rate of data loss".
- GENUINE-GAP: no source separates occurrence time from detection time beyond the bound set by the scrub interval (S3).
- GENUINE-GAP: none of the large field studies covers optical media. S15 is an accelerated lab test whose authors disclaim applicability to real storage conditions.
- GENUINE-GAP: cause attribution is often impossible. S2 says "In many cases, the cause of corruption cannot be identified". S6 says lost-write blame is unclear.
- Methodology limits shared by most of the studies: fleets from a single vendor or operator, proprietary firmware, anonymized models, survivor bias from drive removal (S1, S2), and errors the device masks internally being invisible (S1: nearline write remaps).
