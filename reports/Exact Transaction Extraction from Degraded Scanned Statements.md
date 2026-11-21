# Exact Transaction Extraction from Degraded Scanned Statements

Research date: 2026-11-21. Brief: `briefs/Exact Transaction Extraction from Degraded Scanned Statements.md`. Notes: `research_notes/Exact Transaction Extraction from Degraded Scanned Statements/`.

## Bottom line

1. **No local engine is shown to give exact numbers on degraded images.** In the one study that measured verbatim numeric accuracy on degraded pages, the best conventional engine reproduced 88% of numeric spans and the best local vision-language models 93 to 95% [8]. Plan for detection and targeted review, not for unattended exactness.
2. **Layout, not character recognition, is the largest documented loss in table reading.** On clean numeric tables Tesseract 5.3 read 90.9% of digits but placed only 69.0% of numbers in the right cell; re-filing the same words into columns fitted to their right edges raised that to 83.4% [11]. This supports anchor-relative zonal OCR as the architecture.
3. **Anchor-relative zonal OCR is the recommended architecture.** During this research the user reported that such a pipeline already solved the extraction on their data. That result was not seen or verified here.
4. **What remains is assurance.** A passed balance check certifies the sum, not the rows [11]. Tesseract's confidence is not a calibrated probability [6][13]. Reading twice with the same engine does not give independent errors [11]. Visual proofreading by a person is a weak control [20].
5. **Recommended gate:** auto-accept a row only when two different readers agree exactly, field grammars hold, and the arithmetic reconciles at the smallest printed block. Everything else goes to a person who keys the field blind from the image crop.
6. **Recommended proof:** build ground truth for a sample of real gap-month pages by independent double keying, freeze the pipeline, and report exact-row accuracy, coverage, and an upper bound on the undetected error rate.

## Scope, assumptions and evidence labels

The brief refers to "stated technical and privacy constraints" and "previous experiments" that were not supplied. Assumed, not known: fully local processing, Docker, probably CPU only, a positional parser fed by word boxes, ruled tables, possibly European number formats, and one month available as both scan and electronic original (the paired month).

Nothing below was measured on card or bank statements. Each statement carries one of these labels:

- **Verified:** read in full text and checked by at least one adversarial verifier (three votes in round 1, one or two in round 2).
- **Single reader:** read in full text by one agent; the adversarial check was stopped when the user asked to finish.
- **Inference:** reasoning for this task, not a published result.
- **Unreachable:** the source could not be read; not used as evidence.

Two planned gap tracks were stopped before they returned: (a) cell crops versus full-page OCR and ruling-line removal on machine print, (b) font-specific fine-tuning on real scans and the effect of scan resolution. Statements in those areas rest on round 1 evidence only.

## 1. Failure analysis

| Cause | Signature | Experiment that isolates it |
|---|---|---|
| Information missing in the image | A person cannot read the crop unambiguously; every reader and threshold fails on the same glyph. Voting cannot recover such glyphs [14] (verified). | Blind human keying of the failing crops; rescan and compare. |
| Preprocessing artefact | Mark present in the grey image, absent in the binarised or cleaned one. OCRmyPDF warns that `--clean`, `--remove-background` and `--deskew` can remove content on poor scans; `--clean` changes only the OCR input, so the loss is invisible in the output PDF [3] (verified). | Dump the binarised image (`tessedit_write_images`; `.processed.tif` on Tesseract 5), toggle each option and `thresholding_method` 0/1/2, diff around known commas, points and signs [1]. The dump shows what layout analysis sees; the LSTM recogniser reads grey line crops, so a clean dump does not clear recognition. |
| Segmentation | Tokens missing, merged or misordered, but correct when the row is cropped. Tesseract documents a known problem with tables [1] (verified). | Full page versus row crops with PSM 7 and a border of about 10 px [1]; count missing and merged tokens separately from substitutions. |
| Character recognition | Crop readable, box correct, text wrong. Can be token-specific: one user saw `1.5` lose its point while `1.6` to `1.9` were read correctly, and PSM 6 did not help [7] (verified anecdote, 2018 pre-release build). | Same crop at several scales and with a second engine; error counts per character class (digits, `.`, `,`, `-`, `+`). |
| Layout and coordinates | Text right, cell wrong [11]. OCRmyPDF's text-layer renderer changed in 17.0, and custom unpaper arguments can reposition text [2] (verified). | Feed the parser from hOCR or TSV instead of the PDF text layer; score "token correct anywhere on the page" against "token in the right field". |
| Parsing | Tokens right and in place, value wrong (sign convention, decimal comma, wrapped description). | Feed the parser the electronic original's words and boxes. Any remaining error is a parser error (inference). |

Glyph size is a further recognition variable. Archived Tesseract guidance puts typical x-height at about 20 px for 10 pt at 300 dpi, calls results below 10 px unlikely to be accurate, and reports degradation for the LSTM engine above roughly 30 px [4] (verified, but legacy-era and hedged). Measure x-height on the scans before upscaling.

## 2. Candidate approaches

### Anchor-relative zonal OCR (adopted by the user)

- **Mechanism addressed:** segmentation and cell assignment.
- **Evidence:** the 69.0% to 83.4% correct-cell gain for Tesseract from column re-filing alone, with docTR going from 83.7% to 97.9% [11] (verified; historical election tables, not statements). The Tesseract docs recommend a non-default PSM and a small border for cropped regions [1].
- **Limits and new failure modes (inference unless cited):**
  - A global transform leaves local residuals. In a print-and-scan calibration the maximum error after projective registration was ±4 px per coordinate [18] (verified). Zones need tolerance.
  - A zone that is slightly off clips a trailing sign or leading digit. Check for ink touching the crop border.
  - Row detection that depends on reading a date drops the row when the date is misread. Cross-check against a geometric row count.
  - The LSTM character whitelist needs Tesseract 4.1.0 or later [5] (verified). It is a decode-time filter, and by one reading of the source it can drop a glyph instead of substituting an allowed one [6] (single reader, inference from code).
- **Not supported:** learned template-generalisation models such as the invoice-anatomy paper the user raised [27]. Its full text was unreachable. From the abstract it targets field labelling on unseen templates, which is a different problem from exact characters on one issuer's layout (inference).

### Config-level checks on the Tesseract reader

All are cheap, compatible with the positional parser, and unmeasured for this task.

- **Cleaning and thresholding:** turn off `--clean` and `--remove-background` unless shown harmless; A/B Otsu, adaptive Otsu and Sauvola [1][3].
- **Dictionaries:** the docs say disabling `load_system_dawg` and `load_freq_dawg` should help non-prose text [1][2] (verified as documentation; no benchmark). Score amounts and descriptions separately, since the effect may differ.
- **Page segmentation mode:** only relevant where full-page OCR is still used; maintainers warn that non-default modes usually make things worse unless the structure is known [2].

### Second, different reader for disagreement detection

- **Mechanism addressed:** undetected recognition errors, including descriptions.
- **Evidence:** combining five separately trained models cut character errors by 8 to 35% relative to the best single model on historical print, and disagreement was proposed as an attention signal [14] (verified). A second pass by the same kind of reader "adds evidence without making errors independent" [11] (verified), so the second reader should differ in architecture.
- **Candidates:**
  - **RapidOCR (PP-OCR models on ONNX Runtime):** selectable inside OCRmyPDF since 17.14.0, offline, CPU [3] (verified). It downscales pages above 2000 px on the long side by default, costs about four times Tesseract's CPU time and about 1.2 GB per worker, is absent from the official Docker images, and was under two weeks old at research time. Its claimed advantage on numbers is an unquantified documentation statement.
  - **docTR:** best conventional engine on verbatim numbers in [8] (0.884 against Tesseract 0.756 and PaddleOCR 0.674) and the best-calibrated open-source engine in [12] (ECE 2.5 to 5.4 against 11.5 to 22.6 for PaddleOCR) (verified). CPU cost and integration with the parser were not checked.
- **Benchmark rank does not decide this:** no engine was consistently best across five document benchmarks [9], and PP-OCRv5's edit-distance lead over Tesseract shrinks from 0.067 against 0.324 overall to 0.058 against 0.096 on English text [10] (verified). Choose on your own scans.
- **Experiment:** on the dev set, count wrong fields flagged by disagreement and wrong fields that pass unanimously. The second number is the one that matters.
- **Limit:** unanimous misreads are invisible.

### Alternatives with weaker support

- **Re-reading with one engine at several thresholds or scales:** cheap, but the readings are correlated. The supporting paper was read at abstract level only and its numbers were refuted in verification [22].
- **Font-specific fine-tuning of Tesseract:** the official guide says it "may work" with little data for an unusual font, must start from `tessdata_best`, and over-fits if trained too long [16] (verified). Its worked example is on synthetic renders. No evidence on real degraded scans was obtained.
- **Local vision-language model as a third reader:** 92.7 to 95.0% of numeric spans verbatim, 17 GiB or more of GPU memory, 11 to 67 s per image, no word boxes, and failure modes such as transcribing unprinted text [8] (verified).
- **Confusable-character reclassifier:** only about half of baseline errors were in reach, the evaluation was on clean synthetic strings, and it made 2.3% false corrections [21] (verified). Low priority; a dropped point or sign is a deletion, which it cannot address.
- **Ruling-line removal:** mask-based removal erases strokes that overlap lines; a stroke-preserving method exists but cuts thin strokes and can mistake machine print for dashed lines [17] (verified; 1995, handprint forms). Cropping inside cells avoids the problem (inference).

## 3. Exactness and verification

### Hard constraints

- **Field grammar:** a fixed amount format makes a dropped decimal separator detectable; a dropped sign is not detectable by grammar (inference).
- **Arithmetic:** for a correctly scoped column, a sum check detects every pattern with exactly one wrong number and misses every compensating pattern and every swap within the column. The authors call a pass "a certificate about sums and not about cells" [11] (verified). The guarantee assumes no missing or extra rows.
- **Smaller blocks are safer:** printed subtotals shrink the undetectable set to errors that compensate within one group [11] (verified). For statements, use per-page subtotals, running balances, and the previous month's closing balance where printed (inference).
- **Not covered at all:** dates and descriptions.

### Probabilistic evidence

- **Reader agreement:** see section 2.
- **Tesseract confidence:** the word value is a linear map of the worst character's certainty, not a trained probability [6] (single reader, source code). No measured calibration study for the LSTM engine was found. For the legacy engine, no threshold gave pooled word precision above about 95% on 10 documents, and thresholds did not transfer between documents [13] (verified).
- **Other engines:** a tuned confidence threshold alone detected errors with F1 of 0.22 to 0.57 for docTR, PaddleOCR and three cloud engines [12] (verified). Confidence ranks pages by quality better than it identifies a wrong word.
- **Merchant lexicon:** an exact match of a description against strings from other months' electronic statements is strong evidence (inference). A conservative version of this idea reached zero errors on 843 accepted words, but only 6% coverage, and it abstains on any word with a one-character neighbour in the lexicon [13] (verified). Use the lexicon to accept, not to auto-correct.

### Not independently verifiable

- Descriptions outside the lexicon, and punctuation inside descriptions.
- Any field where all readers agree on the same misreading.
- Amounts hidden by compensating errors.

For these, the only check is an independent reading. Rule-based substitutions (letter O to zero and similar) can introduce false corrections and should be benchmarked one by one [15] (verified).

### Human review

In a randomised study with 195 participants, visual checking left about 30 times as many errors as double entry and was not significantly better than no checking [20] (abstract only; full text unreachable). Have the reviewer key the flagged field blind from the crop and compare it with the OCR value, so that person and machine act as two independent entries (inference).

## 4. Working without the electronic original

**Available for a real gap month:**

- The scan itself: header text, ruling lines, right edges of the amount column, printed totals.
- Layout knowledge from other months' electronic statements: column order, labels, number formats. Layouts can change over the years.
- A merchant lexicon from other months.
- The adjacent months' balances.

**Risks of overfitting to the paired month:**

- Tuning zones, thresholds or PSM on it and then reporting accuracy on it.
- Registering scans to the electronic original. Per-character registration achieves one-pixel ground truth but needs the original, so it is a tool for building ground truth, not for extraction [18] (verified).
- Fine-tuning a recogniser on its glyphs, or building the lexicon from its original.

For learned extraction models, removing template overlap between training and test sets lowered average F1 on SROIE from 94.34 to 85.60 [25] (single reader). Transfer to hand-tuned pipelines is inference.

## 5. Evaluation

**Metrics:**

- **Exact-field rate** per field type and **exact-row rate** (all fields of a row correct), after a declared normalisation.
- **Row recall and precision:** missing and spurious rows, by aligning extracted rows to the reference.
- **Coverage:** share of rows auto-accepted. **Selective risk:** error rate among accepted rows [23] (single reader). This is the undetected error rate.
- **Review effort:** flagged fields per statement and minutes per statement.
- **Per-character-class error changes** for every pipeline change, because a net gain can hide new errors: one preprocessing change improved 30 confusion pairs and worsened 11 [17] (verified).

Do not use character error rate or similarity scores as the headline. Table models scoring 0.98 on a cell-similarity metric had 81% exact tables [26] (single reader), and engines with near-identical character error differed widely on verbatim numbers [8].

**Bounding the undetected error rate:** with zero errors in n audited accepted fields, the 95% upper bound is about 3/n: 300 fields bound the rate at 1%, about 3,000 at 0.1% [24] (single reader). Rows on one page are not independent, so resample by page.

**Test data without contamination:**

1. **Real gap-month pages, double keyed:** two independent manual entries, reconciled. This is the only reference with real degradation and no electronic original.
2. **Print and scan** other electronic months on the same equipment for development data. Print-and-scan pages are only a subset of real degradation [18].
3. **Synthetic degradation (Augraphy):** unlimited volume, but its realism is supported only qualitatively [19] (verified).
4. **The paired month:** score it once, after the configuration is frozen.

## 6. Comparison and recommendation

| Approach | Addresses | Evidence | Cost | Parser fit | Priority |
|---|---|---|---|---|---|
| Anchor-relative zonal OCR | Segmentation, cell assignment | Verified, other domain; user reports success | Own code | Native | Done |
| Arithmetic at smallest block plus field grammar | Single amount errors, dropped separators | Verified theory | Low | Native | 1 |
| Second different reader, agreement gate | Undetected errors, descriptions | Verified for voting; independence unmeasured here | New engine in image; about 4x CPU for RapidOCR | Needs box mapping | 2 |
| Double-keyed gap-month test set | Proof of exactness | Standard statistics | Human time | n/a | 3 |
| Blind keying of flagged fields | Review quality | Abstract only | Human time | n/a | 4 |
| Config checks (cleaning, thresholding, dictionaries) | Preprocessing, recognition | Documentation only | Minutes | Native | 5 |
| Merchant lexicon as accept signal | Descriptions | Inference plus [13] | Low | Native | 6 |
| Fine-tuning, VLM reader, reclassifier | Recognition | Weak or costly | High | Poor to moderate | Only if the gate flags too much |

**Workflow:**

1. Extract with the zonal pipeline.
2. Read every field a second time with a different engine on the same crops.
3. Accept a row only if readings agree exactly, grammars hold, the row count matches the geometric count, and the block arithmetic reconciles.
4. Route everything else to blind keying from the crop.
5. Audit a random sample of accepted rows each batch and track the bound from section 5.

## Sources

1. Tesseract documentation, Improving the quality of the output. https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
2. OCRmyPDF documentation, Advanced features. https://ocrmypdf.readthedocs.io/en/latest/advanced.html
3. OCRmyPDF documentation, Cookbook (17.14.2). https://ocrmypdf.readthedocs.io/en/latest/cookbook.html
4. Tesseract archived FAQ. https://tesseract-ocr.github.io/tessdoc/tess3/FAQ-Old.html
5. Tesseract release notes (4.1.0) and issue 751. https://raw.githubusercontent.com/tesseract-ocr/tessdoc/main/ReleaseNotes.md ; https://github.com/tesseract-ocr/tesseract/issues/751
6. Tesseract source code (`ltrresultiterator.cpp`, `recodebeam.cpp`, `linerec.cpp`). https://raw.githubusercontent.com/tesseract-ocr/tesseract/main/src/ccmain/ltrresultiterator.cpp
7. tesseract-ocr mailing list, dropped decimal points, 2018 to 2019. https://www.mail-archive.com/tesseract-ocr@googlegroups.com/msg16255.html
8. OCR and multimodal models on degraded photographs of clinical reports, 2025. https://arxiv.org/abs/2511.13523
9. OCR engine selection across five benchmarks, 2026 preprint. https://www.alphaxiv.org/abs/2607.16203.md
10. PP-OCRv5, 2026 vendor preprint. https://arxiv.org/abs/2603.24373
11. Zhou and Snyder, table reading with sum checks, 2026 preprint. https://arxiv.org/abs/2610.17448
12. Hemmer et al., OCR confidence and error detection, 2024. https://arxiv.org/abs/2409.04117
13. Kae, Huang and Learned-Miller, UMass technical report UM-CS-2009-031. https://web.cs.umass.edu/publication/docs/2009/UM-CS-2009-031.pdf
14. Reul et al., cross-fold training and voting, 2017. https://arxiv.org/abs/1711.09670
15. Correia and Luck, digitising historical balance sheet data, 2022. https://arxiv.org/pdf/2204.00052
16. Tesseract 4.00 training guide. https://github.com/tesseract-ocr/tessdoc/blob/main/tess4/TrainingTesseract-4.00.md
17. Garris, NISTIR 5687, 1995. https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir5687.pdf
18. Kanungo and Haralick, automatic character ground truth, ICPR 1996. https://www.haralick.org/conferences/automatic_generation_character_groundtruth_closed_loop.pdf
19. Augraphy, 2022. https://arxiv.org/abs/2208.14558
20. Barchard and Pace 2011, abstract only. https://online210.psych.wisc.edu/wp-content/uploads/PSY-210_Unit_Materials/PSY-210_Unit05_Materials/Barchard_abstract_CHB_2011.pdf
21. Confusable-character verification layer, 2026 preprint. https://arxiv.org/abs/2610.22726
22. Lund, Kennard and Ringger 2013, abstract only. https://dblp.org/rec/conf/drr/LundKR13
23. Geifman and El-Yaniv, selective classification, 2017. https://arxiv.org/pdf/1705.08500
24. Hanley and Lippman-Hand, JAMA 1983. https://jhanley.biostat.mcgill.ca/Reprints/If_Nothing_Goes_1983.pdf
25. Laatiri et al., template leakage in SROIE and FUNSD, 2023. https://arxiv.org/pdf/2304.14936
26. Smock et al., PubTables-1M, 2022. https://arxiv.org/pdf/2110.00061
27. Hamri, Devanne, Weber and Hassenforder 2024, unreachable. https://doi.org/10.1155/2024/7599415
