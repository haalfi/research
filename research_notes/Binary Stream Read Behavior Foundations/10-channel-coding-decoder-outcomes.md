# Track 10: Coding and channel theory of reads (erasure, error and synchronization channels; decoder outcome classes)

Scope: what channel coding theory and coded-storage literature say can happen when a stored binary stream is read back
through a noisy medium plus a decoder. Terminology is kept as each source uses it. Where I connect sources, that is
marked INFERENCE.

Download dir (not in repo): /tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/10-channel-coding-decoder-outcomes/

## 1. Sources consulted and access status

| # | Source | Type | Access |
|---|--------|------|--------|
| S1 | C. E. Shannon, "A Mathematical Theory of Communication", BSTJ 27, 1948 (reprint with corrections), people.math.harvard.edu/~ctm/.../entropy.pdf | foundational theory | full text read (Part II, Theorems 10-11) |
| S2 | D. J. C. MacKay, *Information Theory, Inference, and Learning Algorithms*, CUP 2003, author on-screen PDF inference.org.uk/mackay/itprnn/book.pdf | textbook (theory) | full text available; read §9.3 (model channels), §9.5 Solutions (BEC capacity), §13.2 (bounded-distance decoder), Ch. 47 (LDPC detected/undetected errors) |
| S3 | R. J. McEliece, L. Swanson, "On the Decoder Error Probability for Reed-Solomon Codes", JPL TDA Progress Report 42-84 (1985); journal version IEEE Trans. IT 32(5), 1986 | theoretical (peer-reviewed in journal form) | full text read (NTRS 19860013319) |
| S4 | P. Koopman, T. Chakravarty, "Cyclic Redundancy Code (CRC) Polynomial Selection For Embedded Networks", DSN 2004 (author preprint) | peer-reviewed (analytical/exhaustive evaluation) | full text read |
| S5 | P. Thaler, "16-bit CRC polynomial selection", T10/03-290r0, 2003 | standards-committee working document (not the normative standard text) | full text read |
| S6 | J. Coomes, "SBC 32 Byte Commands for End-to-End Data Protection", T10/03-307r1, 2003 | standards-committee proposal (not final SBC text) | full text read |
| S7 | J. S. Plank, "Erasure Codes for Storage Systems: A Brief Primer", ;login: 38(6), Dec 2013 | tutorial (practitioner magazine, author is primary researcher) | full text read |
| S8 | M. Blaum, J. L. Hafner, S. Hetzler, "Partial-MDS Codes and their Application to RAID Type of Architectures", arXiv:1205.0997v2 (IEEE Trans. IT 2013) | theoretical / peer-reviewed | full text read (§1, §2, §8) |
| S9 | M. Blaum, J. S. Plank, "Construction of two SD Codes", arXiv:1305.1221 (2013) | theoretical (preprint) | full text read (abstract, §1) |
| S10 | C. Huang et al., "Erasure Coding in Windows Azure Storage", USENIX ATC 2012 | peer-reviewed systems + implementation | full text read (§1, §2) |
| S11 | K. Zhao et al., "LDPC-in-SSD: Making Advanced Error Correction Codes Work Effectively in Solid State Drives", FAST 2013 | peer-reviewed (simulation) | full text read (abstract, §1, §2) |
| S12 | Y. Cai, S. Ghose, E. F. Haratsch, Y. Luo, O. Mutlu, "Error Characterization, Mitigation, and Recovery in Flash-Memory-Based SSDs", Proc. IEEE 105(9), 2017, arXiv:1706.08642 | peer-reviewed survey | full text read (§2.x ECC, §5.2 NAC, §5.4 Read-Retry, §6.1) |
| S13 | M. Mitzenmacher, "A Survey of Results for Deletion Channels and Related Synchronization Channels", Probability Surveys 6:1-33, 2009 (author PDF DelSurvey.pdf) | peer-reviewed survey (theory) | full text read (§1, §8.1) |
| S14 | R. Heckel, G. Mikutis, R. N. Grass, "A Characterization of the DNA Data Storage Channel", arXiv:1803.03322 (Sci. Rep. 9, 2019) | peer-reviewed empirical | full text read (abstract, §1, §3.2.3) |
| S15 | Seagate Exos data sheet DS2046.1-2512 (2025) | vendor implementation doc | full text read (spec tables) |
| S16 | Y. Cassuto, J. Bruck, "Miscorrection Probability Beyond the Minimum Distance", ISIT 2004 (1-page abstract) | theory (extended abstract) | full text read (one page) |
| U1 | V. I. Levenshtein, "Binary codes capable of correcting deletions, insertions, and reversals", Sov. Phys. Dokl. 10(8), 1966 | theory | UNREACHABLE as text (nymity.ch PDF is an image scan, no OCR available); no claims based on it |
| U2 | JEDEC JESD218 / JESD219, and JEDEC dictionary entry "uncorrectable bit error rate (UBER)" | normative | UNREACHABLE (jedec.org returned 403 to curl and WebFetch; standard requires login). UBER 10^-15 appears only second-hand via S12 |
| U3 | J. S. Plank, M. Blaum, J. L. Hafner, "SD Codes", FAST 2013 | peer-reviewed | UNREACHABLE (USENIX withdrew the paper "because of a dispute over its contents"; web.eecs.utk.edu TLS failed / 503). Used S7 and S9 instead |
| U4 | MacWilliams & Sloane, *The Theory of Error-Correcting Codes*; Berlekamp, *Algebraic Coding Theory* | theory (books) | UNREACHABLE (no open full text found); not used |
| U5 | IEEE 1619 (XTS-AES); T10 SBC-3/4 final PI clauses | normative | UNREACHABLE (paywalled / member-only); only T10 committee documents S5, S6 used |
| U6 | Wolf & Blakeney 1988; Wolf & Chun 1994 (undetected error of shortened CRCs) | peer-reviewed | not obtained; cited only as quoted inside S5 |

## 2. Extracted findings (verbatim quotes with locators)

### 2.1 Channel models (what a read may deliver per symbol)

- S1 Shannon, Part II, Theorem 11: "If H ≤ C there exists a coding system such that the output of the source can be
  transmitted over the channel with an arbitrarily small frequency of errors (or an arbitrarily small equivocation)."
  and "There is no method of encoding which gives an equivocation less than H − C." Note: an asymptotic existence
  result ("arbitrarily small", not zero); Shannon himself notes the proof is "not by exhibiting a coding method".
- S1 Shannon, Theorem 10 (correction channel): "If the correction channel has a capacity equal to Hy(x) it is possible
  to so encode the correction data as to send it over this channel and correct all but an arbitrarily small fraction
  of the errors."
- S2 MacKay §9.3 "Some useful model channels": BSC "P(y = 0 | x = 0) = 1 − f ; P(y = 0 | x = 1) = f"; BEC
  "AX = {0, 1}. AY = {0, ?, 1}" with "P(y = ? | x = 0) = f"; Z channel "P(y = 0 | x = 0) = 1; P(y = 0 | x = 1) = f".
- S2 MacKay §9 solutions (eq. 9.43): "The binary erasure channel fails a fraction f of the time. Its capacity is
  precisely 1 − f, which is the fraction of the time that the channel is reliable." BSC capacity 1 − H2(f) (eq. 9.38).
- S2 MacKay Exercise 11.8: q-ary erasure channel "is a good model for packets transmitted over the internet, which
  are either received reliably or are lost." Exercise 11.9 explicitly links RAID to erasure channels.
- S13 Mitzenmacher §1: "A deletion channel should not be confused with an erasure channel. With an erasure channel,
  when n bits are sent, n symbols are received; a third symbol, often denoted by '?', is obtained at the receiver to
  denote an erasure. In contrast, with a deletion channel, there is no sign of which bits have been deleted."
- S13 §1: capacity of the i.i.d. binary deletion channel: "Surprisingly, we do not know. Currently, we have no
  closed-form expression for the capacity"; "the capacity for the binary deletion channel is at least (1 − p)/9 for
  every value of p".
- S13 §1: "channels with synchronization errors, including both insertions and deletions as well as more general
  timing errors, are simply not adequately understood by current theory." Also: "even the model we suggest assumes
  some high-level synchronization, as both sender and receiver know that n bits are being sent", and "In the past,
  symbol synchronization has been handled separately from coding, using timing recovery techniques"; "codes for
  synchronization have been suggested for disk drives".
- S13 §8.1 sticky channels: "channels that independently duplicates each transmitted symbol a random number of times
  at the receiver".
- S14 Heckel et al. §1: DNA storage channel abstraction "view the input as a multiset of M DNA molecules of length L,
  and the output as sampling N times independently from the multiset, and then disturbing the sampled molecules with
  insertions, deletions, and substitutions". Abstract: data "stored in an unordered way, and can only be read by
  sampling from this DNA pool". Abstract finding: "errors within molecules are mainly due to synthesis and
  sequencing, while imperfections in handling and storage lead to a significant loss of sequences."
- S14 §3.2.3: "out of the reads that have correct target length, in all datasets, the substitution errors dominate by
  far. In the overall error probabilities, the deletions dominate."

### 2.2 Decoder outcome classes

- S3 McEliece & Swanson, abstract: "By definition, 'decoder error' occurs when the decoder finds a codeword other than
  the transmitted codeword, this is in contrast to 'decoder failure,' which occurs when the decoder fails to find any
  codeword at all."
- S3 §I: bounded distance decoder "looks for a codeword within distance t of the received word; if there is such a
  codeword, the decoder finds it, and if not, the decoder reports 'failure.'" "If the transmitted codeword suffers t
  or fewer errors, it will be decoded correctly. If, on the other hand, it suffers more than t errors, one of two
  things can happen." "If the number of errors exceeds t, but is less than d − t, then PF = 1 and PE = 0".
- S3 main result (assumptions: MDS code, bounded-distance decoder, channel where "all error patterns of the same
  weight are equiprobable, for example, a q-ary symmetric channel"): "if more than t errors occur, the probability of
  decoder error is less than 1/t!"; Voyager (255,223) RS: "the probability of decoder error given a word error is
  smaller than 3 × 10^-14. Thus, in a typical operating region with probability 10^-5 of word error, the probability
  of undetected word error is about 10^-19."
- S2 MacKay §13.2: "A bounded-distance decoder is a decoder that returns the closest codeword to a received binary
  vector r if the distance from r to that codeword is less than or equal to t; otherwise it returns a failure
  message." and "bounded-distance decoders cannot reach the Shannon limit of the binary symmetric channel; only a
  decoder that often corrects more than t errors can do this."
- S2 MacKay Ch. 47 (LDPC, p.561-562): decoder declares "a failure if some maximum number of iterations ... occurs
  without successful decoding"; "'undetected' errors occur if the decoder finds an x̂ satisfying Hx̂ = z mod 2 that is
  not equal to the true x. 'Detected' errors occur if the algorithm runs for the maximum number of iterations without
  finding a valid decoding." Also: fixed-iteration practice "blurs the distinction between undetected and detected
  errors."
- S16 Cassuto & Bruck: list decoding beyond t: "The miscorrection probability of a list decoder is the probability that
  the decoder will have at least one non-causal codeword in its decoding sphere." (Lower bound is main result.)

### 2.3 Error detection (CRC) strength

- S4 Koopman & Chakravarty §1: HD "is the minimum possible number of bit inversions that must be injected into a
  message to create an error that is undetectable by that message's CRC-based Frame Check Sequence"; "if a CRC
  polynomial has HD=6 ... there are no possible combinations of 1-, 2-, 3-, 4-, nor 5-bit errors ... that can result
  in an undetected error, but there is at least one combination of 6-bit errors" (paraphrase of tail; verbatim head
  confirmed). §2: "there is a small, but finite, probability that a data corruption that inverts a sufficient number
  of bits in just the right pattern will occur and lead to an undetectable error."
- S4 Table 1 (48-bit data word): CCITT-16 0x8810 HD=4 (84 undetected 4-bit patterns); [Baicheva00] 0xC86C HD=6.
  Text: CCITT-16 "only provides HD=4 at this length". Fault model assumption: "HD for random independent errors on a
  binary symmetric channel is usually the primary factor considered"; "there does not seem to be any authoritative
  characterization of faults in embedded networks." Pud figures computed "at an assumed Bit Error Rate (BER) of 10^-6".
  Also "Many polynomials are good for short words but poor at long words" (HD depends on data word length).
- S5 T10/03-290r0 (choice of 0x18BB7 as the T10 data-integrity 16-bit CRC), quoting Wolf & Blakeney: "Often, it is
  assumed that the probability of undetected error for error detection codes is upper bounded by 2^-r ... This upper
  bound is not correct for many codes, however, especially shortened cyclic codes." Definition: "A code is termed
  'proper' if it retains the desired behavior of Pud(N,p) ≤ Pud(N,0.5) for any p 0 ≤ p ≤ 0.5". Rationale: "A proper
  CRC polynomial was chosen for Data Integrity to give predictable performance for error detection for burst and bit
  errors for all BERs." Also: "when we protect a 512 byte data block with a 16-bit CRC we are using a shortened cyclic
  code."
- S6 T10/03-307r1: reference tag: "The DATA BLOCK REFERENCE TAG field is ... set to the least significant four bytes
  of the logical block address"; "The device server may compare the DATA BLOCK REFERENCE TAG read from the medium with
  this value as enabled by the RDPROTECT field." Also READ (32): "The most recent data value written in the addressed
  logical block shall be returned". (Committee proposal, not ratified text.)

### 2.4 From sector/device read failure to erasure at a higher code

- S7 Plank primer, intro: "disk sectors are embedded with extra-correcting information so that a few flipped bits may
  be tolerated; however, when too many bits are flipped, or when physical components fail, the storage system sees
  this as an erasure: the storage is gone!" and "In communications, errors arise when bits are corrupted silently in a
  message. This differs from an erasure, because the location of the corruption is unknown. The fact that erasures
  expose the location of the failure allows for erasure codes to be more powerful than ECCs". Final section: SD codes
  match "the mixed failure modes of today's disks, where sector failures accumulate over time, unnoticed until a disk
  failure requires that they be read for recovery."
- S8 Blaum, Hafner, Hetzler §1: "From a coding point of view, the model of failures corresponds to erasures, i.e.,
  errors whose location is known"; "A hard error occurs mainly when the internal ECC of a sector is exceeded";
  "Normally, the ECC is coupled with a Cyclic Redundancy Code (CRC), which detects the situation when the ECC
  miscorrects (the ECC has an inherent detection capability that may not be sufficient, hence it often needs to be
  reinforced by the CRC)"; "We will assume instead that a hard error means that the information in a sector is lost
  (an erased sector) and that we can detect this situation." "hard errors, which in general are silent: their
  existence is unknown until the sectors are accessed." Definition 2.1: an (r; s) PMDS code can "correct up to sj + r
  erasures in each row".
- S9 Blaum & Plank abstract: "an SD code dedicates entire disks, plus individual sectors to erasure coding. The code
  then tolerates combinations of disk and sector errors, rather than solely disk errors." Also "It is been an open
  problem to construct general codes that have the SD property, and previous work has relied on Monte Carlo searches."
- S10 Huang et al. §1: during upgrades "A data fragment may be offline for seconds to a few minutes"; "if there is an
  on-demand read from a client to a fragment on the storage node being upgraded, WAS reads from enough fragments in
  order to dynamically reconstruct the data"; and "if it looks like the read to a data fragment is going to take too
  long, WAS in parallel tries to perform a reconstruction of the data fragment (effectively treating the storage node
  with the original data fragment as if it was offline) and return to the client whichever of the two results is
  faster." §2: Maximally Recoverable: LRC "can decode any failure pattern which is information-theoretically
  decodable"; e.g. "It is impossible to decode 3 data fragments from merely 2 parity fragments, regardless of coding
  equations. These types of failure patterns are called information-theoretically non-decodable."

### 2.5 Flash: read as quantized sensing + iterative decoding + retry

- S11 Zhao et al. abstract/§1: "If memory sensing uses only one quantization level between two adjacent storage
  states, it is called hard-decision memory sensing; if more than one quantization levels are used ..., it is called
  soft-decision memory sensing." "NAND flash memory read latency is proportional to the memory sensing precision";
  §2: "NAND flash memory sensing latency is linearly proportional to the number of sensing quantization levels."
  §1: hard-decision LDPC gives "a very low decoding failure probability (e.g., 10^-15 and below) at the early lifetime
  of flash memory and can even have a reasonable decoding failure probability (e.g., 10^-2) at the late lifetime";
  "upon a read request, SSDs always first execute hard-decision memory sensing and decoding, and only when
  hard-decision LDPC code decoding fails, execute soft-decision memory sensing and decoding."
- S12 Cai et al. §5.4: "During read-retry, the SSD controller first reads the data out of NAND flash memory with the
  default read reference voltage. It then sends the data for error correction. If ECC successfully corrects the errors
  in the data, the read operation succeeds. Otherwise, the SSD controller reads the memory again with a different read
  reference voltage. The controller repeats these steps until it either successfully reads the data ... or is unable
  to correctly read the data using all of the read reference voltages". "it can significantly increase the overall
  read operation latency due to the multiple read attempts it causes".
- S12 §6.1 (BCH flow): after read-retry, NAC, then "superpage-level parity recovery ... Whenever data is successfully
  decoded or recovered, the data is sent to the host (and it is also reprogrammed into a new physical page ...).
  Otherwise, the SSD controller reports an uncorrectable error to the host."
- S12 §2 (ECC): ECC engines "correct data with a relatively high raw bit error rate (e.g., between 10^-3 and 10^-2)
  and return data to the host at an error rate that meets traditional data storage reliability requirements (e.g., a
  post-correction error rate of 10^-15 in the JEDEC standard [74])." (Second-hand pointer to JEDEC; JEDEC itself
  unreachable.)

### 2.6 Vendor reliability specification

- S15 Seagate Exos data sheet: "Non-recoverable Read Errors per Bits Read 1 sector per 10E15" (some models: "<1 in
  10E15"). The unit is a sector event per bits read; no confidence, test method, or undetected-error rate is stated in
  the data sheet. (Vendor spec; not a guarantee about any single read.)

## 3. Existing models / classifications found

1. Discrete memoryless channel models (Shannon S1; MacKay S2 §9.3): BSC (substitution, location unknown), BEC (symbol
   replaced by '?', location known), Z channel (asymmetric, one input never flips), q-ary erasure channel (packet
   either received or lost). Capacity: BEC 1 − f, BSC 1 − H2(f).
2. Synchronization channels (S13): i.i.d. deletion channel, insertion/deletion channels, sticky (duplication)
   channels; distinguished from erasure by absence of a position marker; capacity unknown in closed form.
3. DNA storage channel (S14): unordered multiset in, independent sampling out, plus per-molecule insertions,
   deletions, substitutions; whole-molecule loss.
4. Bounded-distance decoder outcome trichotomy (S3, S2 §13.2): correct decoding / decoder failure (detected) /
   decoder error (undetected; miscorrection). Iterative decoders (S2 Ch.47): success / detected error (max iterations,
   syndrome not satisfied) / undetected error (valid but wrong codeword). List decoders: miscorrection probability
   (S16).
5. Error-detection strength model (S4, S5): Hamming distance as function of data-word length; Pud at assumed BER;
   "proper" codes (Pud monotone up to p = 0.5).
6. Erasure-code failure-pattern classes (S10): information-theoretically decodable vs non-decodable patterns; MR
   property. PMDS/SD (S8, S9): erasures per row (sector) plus whole devices.
7. Flash read pipeline (S11, S12): hard-decision sensing -> decode -> (fail) soft-decision / read-retry with
   shifted Vref -> NAC -> superpage parity -> report uncorrectable.

## 4. Convergences

- S7, S8 and S9 converge that a sector whose internal ECC is exceeded is handed to the array-level code as an erasure
  (location known) - but S8 states this as an explicit modeling ASSUMPTION ("We will assume instead ... and that we can
  detect this situation") and notes the internal ECC can miscorrect, requiring a CRC.
- S3, S2 and S16 agree that beyond the guaranteed radius two different outcomes exist (failure vs error/miscorrection)
  and that the split is probabilistic and code/channel dependent.
- S11 and S12 agree that flash read latency grows with decoding effort (sensing precision, number of retries); a read
  outcome includes a latency dimension, not only a correct/incorrect value. S10 likewise treats a slow read as an
  erasure to be reconstructed. INFERENCE: across HDD-array, cloud and flash literature, "erasure" at a higher layer is
  produced by both lower-layer detected failure and by timeout/unavailability.

## 5. Contradictions / tensions

- Engineering rule of thumb "Pud ≤ 2^-r" for an r-bit check is stated to be incorrect for many shortened cyclic codes
  (S5 quoting Wolf & Blakeney). S4 likewise shows HD of widely used polynomials varies with data-word length
  (CCITT-16 HD=4 at 48 bits vs alternatives HD=6).
- Erasure assumption vs miscorrection: storage erasure-code papers (S8) assume all sector failures are detected; the
  same paper concedes ECC miscorrection exists. The decoder-error literature (S3) quantifies a nonzero undetected
  rate. These are compatible only if the CRC (or other check) residual is treated as negligible - an assumption, not a
  guarantee.
- "10^-15" appears in three different senses: a JEDEC post-correction error rate (S12, second-hand), a hard-decision
  LDPC decoding failure probability (S11, illustrative "e.g."), and a vendor "1 sector per 10E15 bits read"
  non-recoverable read rate (S15). These are not the same metric.
- MacKay (S2 §13.2) criticises "worst-case-ism" of bounded-distance decoding; storage reliability arguments built on
  guaranteed correction radius t are thus conservative w.r.t. modern decoders but do not bound undetected errors.

## 6. Gaps

- COVERAGE-GAP: JEDEC JESD218/JESD219 text (UBER definition, retention conditions) unreachable (403/login).
- COVERAGE-GAP: Levenshtein 1966 (scanned, not text-extractable here); claims about Levenshtein distance/codes rest
  only on S13/S14 usage.
- COVERAGE-GAP: MacWilliams-Sloane and Berlekamp books (undetected-error bounds; errors-and-erasures RS decoding
  condition 2e + f < d) not read in full text; not claimed.
- COVERAGE-GAP: IEEE 1619 XTS (no integrity in storage encryption) and ratified T10 SBC PI clauses unreachable.
- COVERAGE-GAP: Plank/Blaum/Hafner FAST 2013 SD paper withdrawn by USENIX; content via S7/S9 only.
- GENUINE-GAP (per S13): no closed-form capacity and few practical codes for deletion/insertion channels; S13 says
  "in practice coding is rarely if ever considered as a viable solution to synchronization."
- GENUINE-GAP (per S4): "there does not seem to be any authoritative characterization of faults in embedded
  networks"; CRC strength figures rest on BSC/independent-error assumptions.
- GENUINE-GAP (per S3): "It would be nice to have a uniform lower bound on the PE(u)'s, but we have been unable to
  find one."
- INFERENCE gap: none of the sources read gives an end-to-end bound that composes the device ECC miscorrection rate,
  the CRC residual, and the array-code erasure assumption into one undetected-read probability.
