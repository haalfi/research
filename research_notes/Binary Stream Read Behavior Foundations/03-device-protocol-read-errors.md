# Track 03: Block-device command sets and how they report read outcomes

Scope: what block-device command sets (NVMe, SCSI/T10 SBC/SPC, ATA/T13 ACS, SD) say about the outcome of a READ:
error reporting classes, recovered vs. unrecovered outcomes, retry and recovery-time control, data returned for
deallocated/unmapped/trimmed blocks, protection-information (PI/DIF) checks on read, torn-write/atomicity guarantees
as seen by later reads, and whether erroneous data can reach the host buffer. Terminology is the sources' own.

Evidence classes used: N = normative standard text (ratified or working draft, as labelled); P = peer-reviewed empirical;
I = implementation documentation / source code. Inference is marked **[inference]**.

## 1. Sources consulted and access status

| # | Source | Class | Access | Notes |
|---|---|---|---|---|
| S1 | NVM Express NVM Command Set Specification, Rev 1.1, 2024-08-05 (Ratified). nvmexpress.org PDF | N (ratified) | full text read (sections cited) | §2.1.4 atomicity, §3.1 status values, §3.3.3.2.1 deallocated blocks, §4.1.3.2 Error Recovery feature, §5.3 end-to-end protection |
| S2 | NVM Express Base Specification, Rev 2.1, 2024-08-05 (Ratified). nvmexpress.org PDF | N (ratified) | full text read (sections cited) | Fig 100 status field (DNR), Fig 106 Media and Data Integrity Errors, §9.2 Media and Data Error Handling, Read Recovery Level section (p.546) |
| S3 | T10/05-344r0, "Proposed SBC-3 Revision 00" (SCSI Block Commands-3 working draft, 9 Sep 2005), t10.org/ftp | N (early working draft, NOT the approved standard) | full text read (sections cited) | §4.9 write failures, §4.10 caches/deferred errors, §4.13 error reporting, §4.16 PI model, §5.14 READ LONG, §6.3.4 Read-Write Error Recovery mode page, Table 29 RDPROTECT |
| S4 | T10/08-149r4, F. Knight, "SBC-3 Thin Provisioning Commands", 4 Nov 2008 | N-proposal (proposal text, not approved standard) | full text read | mapped/unmapped LBA states, TPRZ bit |
| S5 | T13/2161-D ACS-3 (ATA/ATAPI Command Set-3) Working Draft Rev 5, 28 Oct 2013 (mirror at people.freebsd.org) | N (working draft) | full text read (sections cited) | §6.3 error field bits, §6.8.2, §7.5.3.2 TRIM / Table 33, §7.22 READ DMA EXT, §7.71 WRITE UNCORRECTABLE EXT, §8.3.3 SCT ERC, A.11.5.2.2/.8 |
| S6 | SD Specifications Part 1 Physical Layer Simplified Specification v9.10, 1 Dec 2023, SD Card Association | N (simplified public version) | full text read (sections cited) | §4.3.3 Data Read, §4.3.5 Erase/Discard, card status bits table |
| S7 | Seagate, SCSI Commands Reference Manual, 100293068 Rev J, Oct 2016 | I (vendor implementation of SPC/SBC) | full text read (sections cited) | §2.4.1.3/2.4.1.4 current vs deferred, Table 28 sense key descriptions. Used as proxy for SPC-4 text (SPC-4 drafts not obtained) |
| S8 | T10 "SCSI Sense Keys" list (t10.org/lists/2sensekey.htm) and ASC/ASCQ list (t10.org/lists/asc-num.txt) | registry list; page itself states "not officially part of the SCSI standards" | full text read | code values only |
| S9 | Linux kernel `Documentation/block/data-integrity.rst`, `include/linux/blk_types.h`, `drivers/nvme/host/core.c` (master, fetched 2026-11-08 via raw.githubusercontent.com) | I | full text read (functions cited) | OS mapping of device status to block-layer status |
| S10 | Bairavasundaram, Goodson, Schroeder, Arpaci-Dusseau, Arpaci-Dusseau, "An Analysis of Data Corruption in the Storage Stack", USENIX FAST 2008 | P | abstract, §1, §2.x corruption classes read; remaining sections only skimmed | empirical: corruption not signalled by drive |
| U1 | T13 e08137 DRAT proposal (t13.org) | — | UNREACHABLE (HTTP 404 at guessed URL) | ACS-3 text used instead |
| U2 | Current SPC-4/SPC-5, SBC-4/SBC-5 drafts | — | NOT OBTAINED (T10 drafts are member-access; not attempted further) | COVERAGE-GAP: current sense-data and logical block provisioning text (LBPRZ, ANC_SUP) not read |
| U3 | JEDEC eMMC (JESD84-B51) | — | NOT OBTAINED (registration-walled; not attempted) | COVERAGE-GAP |
| U4 | Libata `libata-eh.c`, `libata-scsi.c`, `ata.h`, `scsi_lib.c` | I | downloaded, not analysed | not used for claims |

## 2. Extracted findings (verbatim quotes, locators)

### 2.1 NVMe — status reporting for reads (S1, S2)

- **Status code type for media errors.** S2 Fig 106 "Status Code – Media and Data Integrity Error Values":
  "81h Unrecovered Read Error: The read data could not be recovered from the media."
  "82h End-to-end Guard Check Error: The command was aborted due to an end-to-end guard check failure."
  83h Application Tag, 84h Reference Tag, 88h Storage Tag check errors; "87h Deallocated or Unwritten Logical Block".
- **Data in host buffer on read error.** S2 §9.2 Media and Data Error Handling: "If a read error occurs during the
  processing of a command, (e.g., End-to-end Guard Check Error, Unrecovered Read Error), the controller may either stop
  the DMA transfer into the memory or transfer the erroneous data to the memory. The host shall ignore the data in the
  memory locations for commands that complete with such error conditions."
- **Retry advisability.** S2 Fig 100, bit 31 Do Not Retry (DNR): "If this bit is set to '1', then this bit indicates that if the
  same command is re-submitted to any controller in the NVM subsystem, then that re-submitted command is expected to
  fail. If this bit is cleared to '0', then this bit indicates that the same command may succeed if retried. If a command
  is aborted due to time limited error recovery ..., this bit should be cleared to '0'."
- **Limited Retry (per command).** S1 §3.1 / Fig 26 etc.: "Limited Retry (LR): If this bit is set to '1', then the controller
  should apply limited retry efforts. If this bit is cleared to '0', then the controller should apply all available error
  recovery means ..." ; "If the host does not specify a time limit should be applied, then the controller should apply all
  error recovery means to complete the operation." (note: "should", not "shall").
- **Error Recovery feature (FID 05h).** S1 §4.1.3.2 Fig 96: TLER "Indicates a limited retry timeout value in 100 millisecond
  units ... The timeout starts when error recovery actions have started ... A value of 0h indicates that there is no
  timeout. Note: This mechanism is primarily intended for use by host software that may have alternate means of
  recovering the data." DULBE default "shall be '0'".
- **Read Recovery Level.** S2 Read Recovery Level section, p.546: "balances the completion time for read commands and the
  amount of error recovery applied to those read commands ... There are 16 levels ... Level 0, if supported, provides the
  maximum amount of recovery. Level 4 is a mandatory level that provides a nominal amount of recovery and is the default
  level. Level 15 is a mandatory level that provides the minimum amount of recovery and is referred to as the 'Fast Fail'
  level." and "Interactions between the Read Recovery Level and the Limited Retry (LR) field in I/O commands are
  implementation specific."
- **Verify vs Read error equivalence not required.** S1 Verify command section: "the error that results from integrity
  checks may differ from the error that would result from reading (e.g., there is no requirement that the Verify and Read
  commands return the same error)."
- **Host-induced unrecovered read.** S1 Write Uncorrectable command: "When the specified logical block(s) are read after this
  operation, a failure is returned with Unrecovered Read Error status. To clear the invalid logical block status, a write
  operation is performed on those logical blocks."
- Observation (not found): I found no NVMe per-command "recovered error" completion status analogous to SCSI RECOVERED
  ERROR in Fig 106. **[inference / absence-of-evidence — searched Fig 106 only]**

### 2.2 NVMe — deallocated or unwritten blocks (S1 §3.3.3.2.1)

- Definition: "A logical block that has never been written to, or which has been deallocated using the Dataset Management
  command, the Write Zeroes command or the Sanitize command is called a deallocated or unwritten logical block."
- Values: "If the Deallocated or Unwritten Logical error is not enabled, the values read from a deallocated or unwritten block
  and its metadata (excluding protection information) shall be: all bytes cleared to 0h if the Deallocation Read Behavior
  (DRB) field in the DLFEAT field is set to 001b; all bytes set to FFh if the DRB field is set to 010b; or either all bytes
  cleared to 0h or all bytes set to FFh if the DRB field is cleared to 000b."
- Determinism: "The value read from a deallocated logical block shall be deterministic; specifically, the value returned by
  subsequent reads of that logical block shall be the same until a write operation occurs to that logical block."
  "Read operations and Verify operations do not affect the deallocation status of a logical block."
- PI on deallocated blocks: Guard "set to FFh or set to the CRC for the value read"; Storage/Application/Reference Tag
  "set to FFh (indicating the protection information shall not be checked)."
- Error option: "any User Data Read Access Command that includes a deallocated or unwritten logical block shall abort with the
  Deallocated or Unwritten Logical Block status code. Note: Legacy software may not handle an error for this case."
- Cross-reference in the spec itself: "The operation of the Deallocate function is similar to the ATA DATA SET MANAGEMENT with
  Trim feature described in ACS-5 and SCSI UNMAP command described in SBC-4."

### 2.3 NVMe — atomicity and what later reads return (S1 §2.1.4)

- AWUN/NAWUN (§2.1.4.2): "If a write command is submitted that has a size less than or equal to the AWUN/NAWUN value and the
  write command does not cross an atomic boundary ..., then the host is guaranteed that the write command is atomic to the
  NVM with respect to other read or write commands." "AWUN/NAWUN does not have any applicability to write errors caused by
  power failure or other error conditions".
- AWUPF/NAWUPF (§2.1.4.3) defines torn write: "A torn write is a write operation where only some of the logical blocks that are
  supposed to be written contiguously are actually stored on the NVM, leaving the target logical blocks in an indeterminate
  state in which some logical blocks contain original data and some logical blocks contain new data". Guarantee: "subsequent
  read commands for the logical blocks associated with the write command shall return one of the following: All old data
  ...; or All new data". Beyond the limit: "there is no guarantee of the data returned on subsequent reads".
  Informative Fig 7 lists "D D" (neither old nor new) as an Invalid Result within the AWUPF limit.
- Backward compatibility floor: "the controller shall set AWUN, AWUPF, and ACWU to 0h (1 LBA)" when not guaranteeing across
  boundaries (0-based => 1 LBA).
- Non-volatile requirement (§2.1.4.3.2): "After a write command has completed without error, reads for that location which are
  subsequently submitted and return data, shall return the data that was written by that write command and not an older
  version of the data from previous write commands with the following exception:" volatile write cache enabled, FUA not set,
  no flush completed, main power loss without shutdown.

### 2.4 NVMe — end-to-end protection on reads (S1 §5.3)

- Read with PRACT=0: "As the logical block data and metadata pass through the controller, the protection information within the
  metadata is checked. If a protection information check error is detected, the command completes with the status code of the
  error detected (i.e., End-to-end Guard Check Error, End-to-end Application Tag Check Error, End-to-end Storage Tag Check
  Error, or End-to-end Reference Tag Check Error)." (§5.3.2.2)
- PRCHK selects which fields are checked: GRDCHK, ATCHK, RTCHK, "If this bit is cleared to '0', then the Guard field is not
  checked." (Fig 11)
- Escape values (§5.3.3 Control of PI checking): "If the namespace is formatted for Type 1 or Type 2 protection, then all protection
  information checks are disabled regardless of the state of the PRCHK field when the protection information Application Tag
  has a value of FFFFh." Type 3: when App Tag and Ref Tag have all bits set to '1'.
- Compatibility: "The NVM Express interface supports the same end-to-end protection types defined in the SCSI Protection
  information model specified in SBC-4." DIF vs DIX distinction is location of PI (contiguous vs separate buffer).

### 2.5 SCSI SBC-3 (early draft) — read error reporting (S3)

- §4.13.1 Table 4 "Example error conditions": "Unrecovered read error — MEDIUM ERROR or HARDWARE ERROR"; "Recovered read error —
  RECOVERED ERROR"; "Over-run or other error that might be resolved by repeating the command — ABORTED COMMAND". Table states
  "The list does not provide an exhaustive enumeration".
- Deferred errors: "Some errors may occur after the completion status has already been reported. For such errors, SPC-4 defines a
  deferred error reporting mechanism."
- LBA localisation: "When a recovered read error is reported, the INFORMATION field of the sense data shall contain the LBA of the
  last recovered error during the transfer." "When an unrecovered read error is reported, the INFORMATION field of the sense data
  shall contain the LBA of the unrecovered logical block."
- §4.9 Write failures: data being written when power lost/medium or hardware error "is indeterminate. When accessed by a command
  performing a read or verify operation ..., the device server may return old data, new data, or vendor-specific data in those
  logical blocks."
- §4.10 Caches: write-back caching errors "may be reported as a deferred error on a later command"; "Even with write-back caching
  disabled, undetected write errors may occur."
- §6.3.4 Read-Write Error Recovery mode page:
  - TB: "A TB bit set to one specifies that the device server shall transfer a logical block to the data-in buffer before returning
    CHECK CONDITION status if the logical block is not recovered within the recovery limits specified. The data returned in this
    case is vendor-specific."
  - RC: "RC bit set to zero specifies that error recovery operations that cause delays are acceptable during the data transfer. Data
    shall not be fabricated." / "An RC bit set to one ... implies that the device server may send data that is erroneous or
    fabricated in order to maintain a continuous flow of data." NOTE 25: "The RC bit may be used in image processing, audio, or
    video applications."
  - EER: "An EER bit set to one may imply an increase in the probability of error mis-detection or mis-correction."
  - PER: "A PER bit set to zero specifies that the device server shall not report recovered errors".
  - DCR: "A DCR bit set to one specifies that ECC ... shall not be used for data error recovery."
  - ARRE: automatic read reallocation "shall then be performed only if the device server successfully recovers the data."
  - Also READ RETRY COUNT, RECOVERY TIME LIMIT fields; Table 105 enumerates EER/PER/DTE/DCR combos (e.g. 0100: "shall return
    CHECK CONDITION status with the sense key set to RECOVERED ERROR at the completion of a command during which any recoverable
    error occurs").
- §5.14 READ LONG: transfers vendor-specific data incl. "user data or transformed user data; protection information ...; and any
  additional information (e.g., ECC bytes)." "A correct (CORRCT) bit set to zero specifies that a logical block be read without any
  correction made by the device server." "The values in the Read-Write Error Recovery mode page ... do not apply to this command."
- §4.16 PI model: guard = CRC16, G(x)=18BB7h, over USER DATA; "A LOGICAL BLOCK APPLICATION TAG field set to FFFFh disables checking
  of all protection information for the logical block." Reference tag = low 4 bytes of LBA (Type 1 style) incrementing.
- Table 29 RDPROTECT footnote d: "If an error is reported, the sense key shall be set to ABORTED COMMAND." ASC on guard failure:
  "LOGICAL BLOCK GUARD CHECK FAILED"; footnote f: "If multiple errors occur, the selection of which error to report is not defined
  by this standard."
- Definition from S4 (glossary carried in proposal): "unrecovered error: An error for which a device server is unable to read or write a
  logical block within the recovery limits specified in the Read-Write Error Recovery mode page ... and the Verify Error Recovery mode
  page".

### 2.6 SCSI — sense keys, current vs deferred (S7, S8)

- S7 Table 28: "RECOVERED ERROR: Indicates that the command completed successfully, with some recovery action performed by the device
  server. ... When multiple recovered errors occur during one command, the choice of which error to report (e.g., first, last, most
  severe) is vendor specific." "NOT READY: Indicates that the logical unit is not accessible." "MEDIUM ERROR: ... non-recovered error
  condition that may have been caused by a flaw in the medium or an error in the recorded data. This sense key may also be returned if
  the device server is unable to distinguish between a flaw in the medium and a specific hardware failure (i.e., sense key 4h)."
  "ABORTED COMMAND: ... The application client may be able to recover by trying the command again."
- S7 §2.4.1.4: "Response codes 71h and 73h (deferred error) indicate that the sense data returned is the result of an error or exception
  condition that occurred during processing of a previous command for which GOOD, CONDITION MET, INTERMEDIATE, and INTERMEDIATE-
  CONDITION MET status has already been returned." "If the task terminates with CHECK CONDITION status and the sense data describes a
  deferred error, the command for the terminated task shall not have been processed."
- S8 ASC/ASCQ (registry list, not normative per its own disclaimer): 11h/00h UNRECOVERED READ ERROR; 11h/01h READ RETRIES EXHAUSTED;
  11h/0Ah MISCORRECTED ERROR; 11h/14h READ ERROR - LBA MARKED BAD BY APPLICATION CLIENT; 18h/00h RECOVERED DATA WITH ERROR
  CORRECTION APPLIED; 18h/02h RECOVERED DATA - DATA AUTO-REALLOCATED; 10h/01h-03h LOGICAL BLOCK GUARD/APPLICATION TAG/REFERENCE TAG
  CHECK FAILED; 04h/xx LOGICAL UNIT NOT READY ...

### 2.7 SCSI thin provisioning — unmapped reads (S4, proposal)

- "TP2: Mapped state ... Data and protection information read from a LBA in the mapped state shall be the data and protection information
  that was most recently written to that LBA."
- "TP1: Unmapped state ... Data and protection information provided during a read operation ... from a LBA in the unmapped state: a) shall
  not be retrieved from data that was previously written to any other LBA, and b) shall not change until a subsequent write command to that
  logical block successfully completes".
- "A TPRZ (thin provisioning read zeros) bit set to one indicates that the data returned for a read operation of a LBA that is in the unmapped
  state will return zeros. A TPRZ bit set to zero indicates that the data returned ... is not defined by this standard."
- (Later standards renamed to LBPRZ; not verified here — COVERAGE-GAP U2.)

### 2.8 ATA ACS-3 (S5)

- §6.3.9: "The UNCORRECTABLE ERROR bit shall be set to one if the data contains an uncorrectable error."
- §6.3.7: "The INTERFACE CRC bit shall be set to one if an interface CRC error occurred during an Ultra DMA data transfer. ... If the
  INTERFACE CRC bit is set to one, the ABORT bit is set to one."
- §6.3.5 ID NOT FOUND: "a user-addressable address was not found".
- §6.8.2 / §7.22.5 READ DMA EXT error outputs: "LBA of First Unrecoverable Error".
- §7.5.3.2 Table 33 Trim related interactions: DRAT=0 → "non-deterministic read after trim behavior: Each read command to the logical
  block may return different data." DRAT=1,RZAT=0 → "deterministic read after trim behavior with data set to any value"; DRAT=1,RZAT=1 →
  "with data cleared to zero". Footnote b: "After a read command has completed processing, the data in that logical block becomes
  determinate (i.e., subsequent read commands to that logical block shall return the same data)." Plus: "The data read from an LBA that
  has been trimmed shall not be retrieved from data that was previously received from a host addressed to any other LBA."
- A.11.5.2.8: "If the DRAT SUPPORTED bit is set to one and the RZAT SUPPORTED bit is cleared to zero, then a read operation after a Trim
  operation may have words set to any value."
- §7.71 WRITE UNCORRECTABLE EXT: pseudo uncorrectable (55h) applies to "any of the logical sectors that are contained in the physical
  block of the specified logical sector"; read then performs "normal error recovery to the fullest extent" and logs like a real
  Uncorrectable error; flagged (AAh) marks only the specified logical sectors and "should not perform error logging". Attribute
  "shall remain set during the processing of all power and reset events".
- §8.3.3 SCT Error Recovery Control: Read Command Timer: "the RECOVERY TIME LIMIT field specifies the upper limit of the amount of time a
  device shall processes a read command in total"; zero → "the device shall perform all available error recovery procedures";
  "These timers do not apply to streaming commands ... or to NCQ commands ... if out-of-order data delivery is enabled."

### 2.9 SD Physical Layer Simplified v9.10 (S6)

- Card status bit 21: "CARD_ECC_FAILED ... Card internal ECC was applied but failed to correct the data." Bit 20 CC_ERROR "Internal card
  controller error"; bit 19 ERROR "A general or an unknown error occurred during the operation."
- §4.3.3: "The payload for block oriented data transfer is protected by 1 or 4 bits CRC check sum"; "The Read operation from SD Memory Card
  may be interrupted by turning the power off. The SD Memory Card ensures that data is not destroyed during all the conditions except write
  or erase operations issued by the host even in the event of sudden shut down or removal."
- §4.3.5.1: "The data at the card after an erase operation is either '0' or '1', depends on the card vendor. The SCR register bit
  DATA_STAT_AFTER_ERASE (bit 55) defines whether it is '0' or '1'."
- §4.3.5.2 Discard: "The contents of a region where the discard function has been applied shall be treated as 'don't care' by host. After
  discard operation the previously written data may be partially or fully read by the host, depending on the card implementation."

### 2.10 Linux implementation mapping (S9)

- `nvme_error_status()` maps NVME_SC_READ_ERROR, NVME_SC_UNWRITTEN_BLOCK, NVME_SC_COMPARE_FAILED, NVME_SC_ACCESS_DENIED, NVME_SC_WRITE_FAULT,
  NVME_SC_READ_ONLY → `BLK_STS_MEDIUM`; GUARD/APPTAG/REFTAG/INVALID_PI → `BLK_STS_PROTECTION`; default → `BLK_STS_IOERR`.
- `blk_path_error()`: BLK_STS_MEDIUM and BLK_STS_PROTECTION return false ("retrying failover path will not help").
- data-integrity.rst: "the detection of the corruption is done at read time which could potentially be months after the data was written";
  DIX = separation of data and integrity-metadata buffers, outside T10/T13 scope.

### 2.11 Empirical: corruption the device does not report (S10)

- Abstract/§1: "silent data corruption, where the data is silently corrupted with no indication from the drive that an error has occurred."
  "We find more than 400,000 instances of checksum mismatches over the 41-month period" (1.53 million drives).
- §2 classes: Checksum mismatch causes "(i) data content corrupted by components within the data path, or (ii) a torn write ... or (iii) a
  misdirected write"; Identity discrepancy causes "(i) a lost write ... or (ii) a misdirected write". Checksum mismatches "can be detected
  anytime a disk block is read". Detection is by storage-system checksums above the drive, i.e., the device returned good status.

## 3. Existing models / classifications found (source terminology)

1. **NVMe Status Code Type taxonomy** (S2): Generic Command Status / Command Specific / Media and Data Integrity Errors / Path Related; plus
   DNR, More, CRD bits. Read-relevant: 81h Unrecovered Read Error, 82h–84h/88h end-to-end tag check errors, 87h Deallocated or Unwritten.
2. **SCSI sense key + ASC/ASCQ model** (S3, S7, S8): sense key (coarse class), ASC/ASCQ (specific condition), response code current
   (70h/72h) vs deferred (71h/73h); INFORMATION field carrying the LBA.
3. **SCSI Read-Write Error Recovery mode page** (S3 §6.3.4): host-tunable policy space (AWRE, ARRE, TB, RC, EER, PER, DTE, DCR, retry
   counts, recovery time limit), with Table 105 giving combined semantics.
4. **Protection Information model** (S3 §4.16; S1 §5.3): Guard (CRC), Application Tag, Reference Tag (+ NVMe Storage Tag); Types 1/2/3;
   DIF vs DIX placement; escape tag values disabling checks.
5. **Logical block provisioning states**: SCSI mapped/unmapped state machine (S4); NVMe deallocated or unwritten + DLFEAT/DRB (S1);
   ATA non-deterministic / deterministic read after trim, DRAT/RZAT (S5); SD erase (DATA_STAT_AFTER_ERASE) vs discard ("don't care") (S6).
6. **Atomicity parameters** (S1 §2.1.4): AWUN/NAWUN (concurrency atomicity), AWUPF/NAWUPF (power-fail atomicity, "torn write"),
   atomic boundaries (NABSN/NABSPF/NABO), Single vs Multiple Atomicity Mode.
7. **Recovery effort controls**: NVMe LR bit + TLER + Read Recovery Level (0..15, 15 = Fast Fail); ATA SCT ERC Read Command Timer;
   SCSI READ RETRY COUNT / RECOVERY TIME LIMIT / EER.
8. **Corruption classes** (S10, empirical): checksum mismatches, identity discrepancies, parity inconsistencies; causes: bit corruption,
   torn writes, misdirected writes, lost writes.

## 4. Convergences

- All three block command sets specify that a read that cannot be recovered is reported as an explicit failure with an error class
  (NVMe 81h; SCSI MEDIUM ERROR / HARDWARE ERROR with 11h ASC; ATA UNCORRECTABLE ERROR bit; SD CARD_ECC_FAILED), and SCSI/ATA identify the
  failing LBA (SCSI INFORMATION field; ATA "LBA of First Unrecoverable Error").
- All provide host control over how much recovery effort a read gets (NVMe LR/TLER/RRL; ATA SCT ERC; SCSI mode page), with explicit notes
  that limited recovery is intended for hosts with alternate recovery (NVMe TLER note).
- NVMe, ATA (DRAT) and SCSI (TP proposal) converge on "same value on repeated reads until next write" for deallocated/trimmed/unmapped
  blocks, and ATA and SCSI both prohibit returning data written to *other* LBAs.
- SCSI and NVMe PI share the FFFFh application-tag escape that disables all checks (Type 1/2), and NVMe deallocated blocks return FFh tags
  "indicating the protection information shall not be checked" **[inference: reads of deallocated blocks therefore bypass PI verification
  on NVMe]**.
- Both NVMe and SCSI permit erroneous/vendor-specific data to land in the host buffer on a failed read (NVMe §9.2 "transfer the erroneous
  data"; SCSI TB=1), and both put the burden on the host (NVMe "host shall ignore").
- Device-induced known-bad blocks: NVMe Write Uncorrectable, ATA WRITE UNCORRECTABLE EXT, SCSI ASC 11h/14h "LBA MARKED BAD BY APPLICATION
  CLIENT" -> reads deterministically fail until rewritten.

## 5. Contradictions / divergences

- **Deallocated/trimmed read values differ by command set**: NVMe restricts values to all-0h or all-FFh (even when DRB=000b) and always
  deterministic; ATA without DRAT allows "Each read command to the logical block may return different data", and with DRAT/no RZAT "any
  value"; SCSI (proposal) TPRZ=0 "not defined by this standard" but stable; SD discard permits "previously written data may be partially or
  fully read". So "read after deallocate returns zeros" is a per-device capability, not a cross-technology guarantee.
- **Torn-write read outcomes**: NVMe guarantees all-old-or-all-new only within AWUPF and atomic boundaries (default floor 1 LBA); SCSI SBC-3
  draft allows "old data, new data, or vendor-specific data" after interrupted writes; S10 empirically observes torn writes detected only by
  higher-level checksums.
- **Recovered outcomes visibility**: SCSI can surface RECOVERED ERROR per command (PER=1) and chooses which of multiple recovered errors to
  report vendor-specifically; NVMe Fig 106 has no recovered-error completion code (absence noted, inference). Linux maps NVMe statuses into
  coarse BLK_STS_* classes, collapsing Deallocated/Unwritten and Unrecovered Read Error into BLK_STS_MEDIUM (implementation).
- **PI check failure class**: SCSI reports PI read failures with sense key ABORTED COMMAND (RDPROTECT footnote d) — a class S7 describes as
  possibly recoverable by retry — while NVMe puts them under Media and Data Integrity Errors and Linux treats them as non-path-retryable
  (BLK_STS_PROTECTION).
- **"Fabricated" data as a legitimate mode**: SCSI RC=1 explicitly allows erroneous or fabricated data without error indication for
  continuous flow, which contradicts any assumption that a GOOD read always returns stored data.
- **Read-after-write guarantee exception**: NVMe's non-volatile requirement is explicitly lifted under volatile write cache + no FUA + no flush
  + power loss; SCSI write-back cache errors may become deferred errors reported on a later, unrelated command.

## 6. Gaps

- COVERAGE-GAP: current SPC-5/SBC-5 text (LBPRZ, ANC_SUP, current deferred-error rules, sense-data descriptor details) not read; SBC-3 r0 and
  the 08-149r4 proposal are older working texts and may differ from approved standards.
- COVERAGE-GAP: ACS-4/ACS-5 (current ATA) not read; ACS-3 r5 draft used. T13 e08137 DRAT proposal unreachable.
- COVERAGE-GAP: JEDEC eMMC/UFS (sanitize/discard/trim read-back semantics, ECC reporting) not obtained.
- COVERAGE-GAP: NVMe Zoned Namespace (reads beyond write pointer) and Key-Value command sets not examined.
- GENUINE-GAP (as far as read here): none of the command-set specs quantify the probability of mis-correction or of undetected (silent) error
  returned with good status; SCSI only notes EER may "increase ... the probability of error mis-detection or mis-correction". Empirical
  prevalence comes from field studies (S10), not specs.
- GENUINE-GAP (as far as read here): specs do not define cross-command-set equivalence of recovered/unrecovered classes; mappings (e.g. SAT,
  NVMe-SCSI translation, Linux blk_status) are implementation artefacts.
