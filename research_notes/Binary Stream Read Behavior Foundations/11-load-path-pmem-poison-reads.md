# Track 11: Byte-addressable and memory-mapped reads (PMem/CXL load semantics, poison, machine checks, SIGBUS)

Track id: 11-11-load-path-pmem-poison-reads. Retrieved 2026-11-08. Downloads are in the scratchpad:
/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/11-load-path-pmem-poison-reads/

## Sources and access status

| # | Source | Type | Access |
|---|--------|------|--------|
| S1 | Intel 64 and IA-32 SDM Vol. 3 (Order 325384-093US, Sep 2026), ch. 18 Machine-Check Architecture (18.6.x UCR, Table 18-21) | normative (vendor architecture spec) | full text (cdrdv2.intel.com/v1/dl/getContent/671447) |
| S2 | ACPI 6.5, sec. 9.19.7.2 Address Range Scrubbing (ARS) Overview (NVDIMM root device DSMs) | normative | full section (uefi.org/specs/ACPI/6.5/09_...html) |
| S3 | Arm ARM Supplement RAS, ARM DDI 0587 D.d (2022), sec. 1.1-1.3, 2.3 | normative (vendor architecture spec) | full text (documentation-service.arm.com/static/63185614f72fad1903828eda) |
| S4 | SNIA NVM Programming Model v1.2a Working Draft (Mar 22 2017), sec. 10.1.2, 10.3.10-10.3.12 | normative-draft (explicitly "work in progress") | full text. FINAL v1.2 PDF: UNREACHABLE (404 at snia.org final path) |
| S5 | Linux Documentation/mm/hwpoison.rst (Kleen 2009, master) | implementation-doc | full |
| S6 | Linux Documentation/filesystems/dax.rst, "Handling Media Errors" | implementation-doc | full |
| S7 | man-pages sigaction(2) (mkerrisk/man-pages master), si_code BUS_MCEERR_AR/AO, si_addr_lsb | implementation-doc | full |
| S8 | Linux mm/memory-failure.c kill_proc() (master) | implementation (source) | full |
| S9 | Linux drivers/nvdimm/pmem.c (read_pmem, pmem_do_read, __pmem_direct_access, pmem_recovery_write); fs/dax.c dax_iomap_iter; include/linux/dax.h dax_mem2blk_err | implementation (source) | full |
| S10 | Linux arch/x86/lib/copy_mc.c copy_mc_to_kernel kernel-doc | implementation (source) | full |
| S11 | Linux Documentation/ABI/testing/sysfs-bus-cxl (trigger_poison_list); drivers/cxl/cxlmem.h (Get Poison List structs) | implementation-doc | full |
| S12 | Xu et al., NOVA-Fortis, SOSP 2017 (lrita.github.io mirror of the author PDF; cseweb.ucsd.edu failed TLS chain) | peer-reviewed (system design + fault model) | full text, 19 pp |
| S13 | Izraelevitz et al., Basic Performance Measurements of the Intel Optane DC PMM, arXiv:1903.05714v3 | engineering-evidence (tech report, not peer-reviewed) | full text |
| S14 | Sridharan et al., Memory Errors in Modern Systems, ASPLOS 2015 (pages.cs.wisc.edu course mirror) | peer-reviewed-empirical | full text |
| S15 | Raad, Wickerson, Neiger, Vafeiadis, Persistency semantics of the Intel-x86 architecture (Px86), POPL 2020 | theoretical | full text (plv.mpi-sws.org) |

Unreachable / not obtained:
- CXL 3.x specification (Get Poison List, Media Error Record, viral): UNREACHABLE (distributed via CXL Consortium portal behind registration; no public copy found). Only Linux structures citing it (S11) were read; those are implementation, not the spec.
- SNIA NVM PM v1.2 final: UNREACHABLE (404). Draft 1.2a used instead and labelled as draft.
- JEDEC JESD79-5 (DDR5 on-die ECC, ECS): NOT ATTEMPTED / gated (JEDEC login). COVERAGE-GAP.
- Pelley et al., Memory Persistency, ISCA 2014: UNREACHABLE at tried URL (umich 404); not pursued further.
- Sridharan ASPLOS 2015 at cs.virginia.edu: 403; obtained from wisc mirror.

## Extracted findings

### S1 Intel SDM Vol. 3, ch. 18
- 18.6 (UCR): "UCR errors are uncorrected errors that have been detected and signaled but have not corrupted the processor context... UCR error reporting provides an error containment mechanism for data poisoning."
- Recovery support is discoverable: "When IA32_MCG_CAP[24] is set, this indicates that the processor supports software error recovery. When this bit is clear ... the primary responsibility of the machine check handler is logging ... and shutting down the system."
- 18.6.3 UCR Error Classification (three classes, verbatim terms):
  - UCNA: "not signaled via a machine check exception and, instead, is reported ... as a corrected machine check error ... data in the system is corrupted, but the data has not been consumed" (UC=1, PCC=0, S=0, AR=0).
  - SRAO: "System software recovery action is optional ... the data has not been consumed and the processor state is valid" (UC=1, PCC=0, S=1, EN=1, AR=0).
  - SRAR: "requires system software to take a recovery action on this processor before scheduling another stream of execution ... the error was detected and raised at the point of the consumption in the execution flow" (AR=1). "If MISCV and ADDRV are not set, it is recommended that system software shutdown the system."
- PCC bit 57: "the state of the processor might have been corrupted ... reliable restarting of the processor may not be possible."
- SRAR data load: "For all defined SRAR errors, the ADDRV and MISCV flags ... are set ... the address LSB information in the IA32_MCi_MISC register should indicate the lowest valid address bit". Table 18-21: Recoverable-continuable (RIPV=1, EIPV=1) vs Recoverable-not-continuable (RIPV=0). "Restarting without rectifying the error condition will result in most cases with another SRAR error on the same instruction."
- MCE broadcast: "MCE signal is broadcast to all logical processors ... except when the processor supports LMCE and LMCE is enabled".

### S2 ACPI 6.5 sec. 9.19.7.2 ARS
- "ARS allows the platform to communicate memory errors to system software. This capability allows system software to prevent accesses to addresses with uncorrectable errors in memory."
- Notification 0x81 "Unconsumed Uncorrectable Memory Error Detected Notification"; "If the memory range is accessed before OSPM can process the ARS data, default platform error handing sequences, such as Machine Check, may occur."
- "Only one scrub can be in progress system wide"; "When a new address range scrub operation is started, the previous ARS results are lost."; ARS can stop prematurely with partial results.
- Clear Uncorrectable Error: "OSPM should only issue the Clear Uncorrectable Error function ... if that the address range has been retired from further use or if valid error-free data is written to the range before those locations are read. If ... not supported ... or ... fails, the OSPM should continue to prevent accesses".

### S3 Arm RAS Supplement DDI 0587 D.d
- 1.1: "An error is the deviation from correct service ... A fault is the cause of the error." "Errors that are present but not detected are latent errors or undetected errors." "In a system with no error detection, all errors are latent errors and are silently propagated".
- 1.2.3: "A value is poisoned in the state of a component if it is marked as being in error, such that a subsequent access of the state will detect the value is so marked and is treated as a detected error." "Poison is used to defer an error." "The state of a component becomes infected when the component consumes an uncorrected error that updates the state."
- 1.2.4: containable/uncontainable; "If the component cannot determine whether ... then the component treats the detected uncorrected error as uncontainable"; "Reporting an error as containable allows software to contain the error. This does not mean that hardware has contained the error."
- 1.3.2 deferral: "An error is deferred by hardware if hardware can make forward progress without consuming the error ... The fault might become masked later ... because the corrupt value is overwritten before it is consumed ... If the deferred error is later consumed, then the error is reported at the point of consumption."
- 2.3.1: PE error states UC, UEU, UER, UEO, CE. "When a synchronous External abort exception is taken to AArch64 state, the PE records the PE error state in ESR_ELx.SET as ... Uncontainable (UC). Recoverable state (UER). Restartable state (UEO). Other values ... are not supported by synchronous External abort".

### S4 SNIA NPM v1.2a (draft) 10.1.2 / 10.3.10-12
- Three error properties: "instruction precision", "data containment", "live reporting". "only instruction-precise, data-contained, live-reported errors are real-time recoverable. Any other kind of error (imprecise, or precise and data-uncontained) will require that the application restart."
- Traditional storage reads: "reads always have the properties of instruction precision and data containment." Unbuffered write errors surface only on "a subsequent synchronization and read operation".
- Memory path: "some hosts may simply crash with an unhandled exception upon detection of a memory error. Other hosts may not have error-detection capabilities at all, resulting in propagation of memory corruption". "Memory errors may be propagated to applications via an error signal (typically SIGBUS on POSIX systems)".
- 10.3.10 PRECISE: "'precise' means that the exception is immediately delivered during the instruction that generated the memory error. Notably, this refers only to LOAD instructions." "Without the PRECISE property, an application cannot assume that the data from a LOAD is valid." PRECISE is distinct from LIVE.
- 10.3.11 ERROR_UNIT: "the minimal amount of data that the platform can identify as being in an unusable or otherwise unknown state. A value of 0 indicates that memory errors are not contained."

### S5-S10 Linux
- hwpoison.rst: early kill "Send SIGBUS to the application as soon as the error is detected"; late kill "Send SIGBUS when the application runs into the corrupted page. This is best for memory error unaware applications and default"; sysctl vm.memory_failure_recovery=0 "All memory failures cause a panic." "Most kernel internal objects cannot be recovered, only LRU pages for now."
- sigaction(2): "BUS_MCEERR_AR ... Hardware memory error consumed on a machine check; action required." "BUS_MCEERR_AO ... detected in process but not consumed; action optional." si_addr_lsb "indicates the least significant bit of the reported address and therefore the extent of the corruption"; "BUS_MCEERR_* and si_addr_lsb are Linux-specific extensions."
- memory-failure.c kill_proc: AR via force_sig_mceerr only if MF_ACTION_REQUIRED and t == current; others get BUS_MCEERR_AO "if they have PF_MCE_EARLY set".
- dax.rst Handling Media Errors: badblocks list per pmem device; "If we fault at such location, or one with a latent error not yet discovered, the application can expect to receive a SIGBUS." Clearing by writing via driver (ACPI clear_poison DSM), delete/truncate/hole-punch.
- pmem.c: pmem_do_read returns BLK_STS_IOERR if is_bad_pmem(); read_pmem uses copy_mc_to_kernel and returns BLK_STS_IOERR if any bytes remain. __pmem_direct_access returns -EHWPOISON for bad range unless DAX_RECOVERY_WRITE. dax.h: dax_mem2blk_err maps -EHWPOISON to -EIO. fs/dax.c dax_iomap_iter: recovery only "if (map_len == -EHWPOISON && iov_iter_rw(iter) == WRITE)"; on short transfer "if (xfer < map_len) break;" (short read). pmem_recovery_write comment: "A competing pread thread will be held off during the recovery process since data read back might not be valid".
- copy_mc.c: copy_mc_to_kernel "memory copy that handles source exceptions ... Return 0 for success, or number of bytes not copied if there was an exception." Fragile variant to avoid "accessing poison across 2 cachelines with a single instruction". Without CONFIG_X86_MCE no careful copying.

### S11 CXL in Linux
- trigger_poison_list: "The list consists of addresses that are poisoned, or would result in poison if accessed, and the source of the poison." cxlmem.h: record length "in units of 64 bytes"; flags MORE, OVERFLOW, SCANNING; sources UNKNOWN/EXTERNAL/INTERNAL/INJECTED/VENDOR (comments cite CXL 3.0 8.2.9.8.4.x). Spec itself UNREACHABLE.

### S12 NOVA-Fortis
- Fault model 4.1: "Loads to poisoned addresses cause an MCE, and all the data in the PR is lost. The poisoned status of a PR persists across system failures ... On Intel processors the poison radius is 64 bytes (one cache line), but after boot, Linux reports poisoned regions at 512-byte granularity". Assumes controller "silently returns invalid data for undetectable errors". "Intel processors do not provide a mechanism for detecting store failures". Uses memcpy_mcsafe() for all NVMM reads. "In rare cases (e.g., an MCE occurring during a page fault), MCEs are not recoverable". DAX-mmap users "take on responsibility for detecting and recovering from both media errors (which appear as SIGBUS in user space) and scribbles." Checksums/parity not valid while pages mapped read/write.

### S13 Izraelevitz et al.
- "The read latency of random Optane DC memory loads is 305 ns This latency is about 3x slower than local DRAM." Sequential 2x better: "Optane DC PMMs merge adjacent requests into a single 256 byte access." Media granularity 256 B; AIT translation for wear-leveling and bad-block management. Device-specific (Optane gen 1, discontinued).

### S14 Sridharan et al. ASPLOS 2015
- Fault vs error terminology (citing Avizienis et al.): errors "may also go uncorrected, or in the worst case, completely undetected (i.e., silent)." "SEC-DED ECC ... may result in undetected errors (which may cause silent data corruption) at a rate of up to 20 FIT per DRAM device". "counting errors instead of faults ... can lead to incorrect conclusions". Field data: Cielo/Hopper DRAM (not PMem).

### S15 Px86 (POPL 2020)
- "The Intel-x86 architecture follows a relaxed, buffered persistency model." Post-crash reads may observe states "not possible during normal (non-crashing) executions" (x=0, y=1); "the store order ... is separate from the persist order". Theoretical model, relies on Intel docs and discussions with Intel (Neiger co-author).

## Existing models/classifications found (source terminology)
- Intel MCA UCR classes: UCNA / SRAO / SRAR (+ corrected, fatal PCC=1); SRAR recoverable-continuable vs not-continuable.
- Arm RAS: fault/error/failure; latent/undetected; infected/poisoned; containable/uncontainable; deferred error; PE error states UC/UEU/UER/UEO/CE.
- SNIA NPM: three error properties (instruction precision, data containment, live reporting); real-time recovery vs restart with crash recovery; platform attributes PRECISE, ERROR_UNIT, MAPPED_SUPPORT, LIVE_SUPPORT.
- Linux hwpoison: early kill vs late kill vs panic; BUS_MCEERR_AR vs BUS_MCEERR_AO.
- Px86: store order vs persist order (buffered, relaxed persistency).

## Convergences
- "Consumption" is the pivot across Intel (SRAR "at the point of the consumption"), Arm (deferred error "reported at the point of consumption"), Linux (AR "consumed" vs AO "not consumed"), ACPI ("Unconsumed Uncorrectable Memory Error"). Poison = deferral marker (Arm explicit; Intel "containment mechanism for data poisoning").
- Background discovery path (ACPI ARS, CXL poison list, SRAO/AO, Linux badblocks) vs foreground consumption path (SRAR/AR SIGBUS, copy_mc short copy -> EIO).
- Same media fault presents differently by access path (inference from S6, S9, S12): read() through pmem driver -> EIO (block-style, precise/contained per SNIA); DAX mmap load -> SIGBUS BUS_MCEERR_AR; kernel read via copy_mc -> short copy -> -EIO / short read.

## Contradictions / tensions
- Granularity: NOVA-Fortis says Intel poison radius 64 B but Linux reports 512 B (sector badblocks); CXL lists in 64-B units; si_addr_lsb often page (man page example log2(page size)); SDM gives an address LSB field. Containment unit is platform/software-dependent (SNIA ERROR_UNIT).
- hwpoison.rst says error unhandled is "safe to just ignore ... because no corruption has been consumed yet" (background), whereas SNIA warns non-detecting hosts propagate corruption silently; Sridharan quantifies undetected errors (SEC-DED up to 20 FIT/device). Detection is not universal.
- dax.rst lists "architectures which have virtually mapped caches such as ARM" as not working correctly for DAX; Arm RAS gives a synchronous external abort path. Scope differs (DAX caching vs error reporting) - not a direct contradiction.
- Linux recovery-write path exists only for writes; reads of poisoned DAX range return -EIO (no read-side recovery) - convention of the implementation, not a guarantee.

## Gaps
- COVERAGE-GAP: CXL 3.x spec text (poison, viral, Media Error Record) unreachable.
- COVERAGE-GAP: JEDEC DDR5 on-die ECC/ECS not read.
- COVERAGE-GAP: Pelley ISCA 2014 not read; SNIA v1.2 final not read (draft used).
- GENUINE-GAP (per NOVA-Fortis, 2017): "there have been no (publicly-available) studies of error behaviors in emerging NVMM technologies." Not re-verified against later literature by this track.
- GENUINE-GAP (inference): no normative cross-vendor spec found that defines poison granularity visible to applications; it is per-platform.
