# Round 1 synthesis (workflow output)

Output of the synthesis step of the deep-research workflow, 2026-11-21. It used only claims that survived the three-vote verification. Source ids (S0 to S22) refer to the track notes.

Stats: {"angles": 5, "sourcesFetched": 23, "claimsExtracted": 115, "claimsVerified": 25, "confirmed": 23, "killed": 2, "unverified": 0, "afterSynthesis": 11, "urlDupes": 0, "budgetDropped": 7, "agentCalls": 105}

## Summary

The verified evidence does not identify any local OCR engine or model that delivers exact numeric recovery on degraded scans: the best systems measured on degraded images reproduced only about 93-95% of numeric spans verbatim, and general benchmark rank did not predict numeric exactness across engines. The most defensible approach (inference from the evidence, not a published result for statements) is therefore to keep the Tesseract/OCRmyPDF pipeline, attack its documented weak points with cheap controlled experiments (table segmentation and PSM, dictionary settings, binarisation and unpaper cleaning, glyph size), and add a second, architecturally different reader (RapidOCR/PP-OCR via OCRmyPDF 17.14+) used mainly as a disagreement detector, not as a replacement. Because per-character errors compound (5% character error gives about a 26% chance of a wrong six-digit field and a 95% chance of at least one wrong field in a ten-number table) and because voting cannot fix or even detect errors shared by all readers, fully automatic exactness cannot be assured; rows should be accepted only when independent readings agree and format and arithmetic constraints hold, with everything else routed to human review. Several parts of the brief (template registration and rule removal for gap months, confidence calibration, evaluation protocol, verification of description text and punctuation) are not covered by any surviving claim and remain recommendations by inference or open questions. The brief's stated constraints and previous experiments were not supplied, so offline, CPU-only, Docker and positional-parser constraints are assumptions.

## Findings

### F0 (confidence: high; vote: 3-0 (claims 0, 3))

Failure analysis, segmentation: table layout is a documented Tesseract weakness, and page segmentation mode is a cheap, controllable variable. The Tesseract docs say it has a known problem recognising text/data in tables without custom segmentation or layout analysis. OCRmyPDF forwards a PSM via --tesseract-pagesegmode (it passes none by default, so Tesseract's PSM 3 applies); PSM 4, 6, 7, 11 and 13 are usable, while 0, 1, 2 and 12 are documented as incompatible. The maintainers warn that non-default modes usually make things worse unless the page structure is known. For this task (inference): segmentation failure is a prime suspect for dropped, merged or misordered cells, and it can be isolated by comparing full-page OCR against OCR of pre-cropped rows or cells (PSM 6/7) on the same image.

Evidence and limits: Both statements were read in full on the official docs and cross-checked against source code (OCRmyPDF passes --psm only when set; Tesseract CLI default is PSM_AUTO). Neither source gives measurements, names statements, or endorses a specific PSM for tables; the linked remedies (ruling-line removal, cell cropping with OpenCV) are third-party proposals. Incompatibility of OSD modes is documented, not enforced by the CLI. Experiment: run PSM 3, 4, 6 and 11 on full pages and PSM 7 on row crops, then count missing/merged tokens separately from character substitutions.

Sources: https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html, https://ocrmypdf.readthedocs.io/en/latest/advanced.html

### F1 (confidence: medium; vote: 3-0 (claims 1, 4))

Quick win to test, dictionaries and character constraints: for non-prose content the Tesseract docs say disabling both dictionaries (load_system_dawg and load_freq_dawg = false) should increase recognition, and that user words, user patterns and tessedit_char_whitelist can help further. OCRmyPDF exposes this through --tesseract-config and documents a no-dictionary example for documents with few real words, while warning that some parameter combinations break Tesseract or OCRmyPDF's assumptions. This is untested vendor guidance, not evidence of a gain: it carries no benchmark, appears to date from the legacy engine, and LSTM whitelist support was added only in a later release.

Evidence and limits: Quotes verified verbatim on both official doc pages. Limitations found by verifiers: the Tesseract section links to tess3-era pages; the release notes list LSTM whitelist/blacklist support as a later addition; mailing-list reports of no effect are search-extract leads only; the two language_model_penalty_* parameters in the OCRmyPDF example may have little effect under --oem 1 (verifier's recollection, not source-verified). Only the whitelist is a true constraint, and it is suited to cropped amount/date fields, not whole pages containing descriptions. Experiment: A/B the config file on the paired page with --oem 1, scoring amounts, dates and descriptions separately, since dictionary removal could help numerics and hurt descriptions.

Sources: https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html, https://ocrmypdf.readthedocs.io/en/latest/advanced.html

### F2 (confidence: high; vote: 3-0 (claims 2, 8))

Failure analysis, preprocessing artefacts: binarisation and cleaning are plausible sources of lost small marks, and both can be inspected. Tesseract's default is a single global Otsu threshold, which the docs say can be suboptimal on uneven backgrounds; 5.0.0 added Adaptive Otsu and Sauvola (thresholding_method 1 and 2). The binarised image can be dumped with tessedit_write_images; on 5.x the file is <outputbase>.processed.tif (tessinput.tif is the 4.x name). OCRmyPDF warns that --remove-background, --deskew, --clean and --clean-final can remove desirable content on poor scans; --clean applies unpaper only to the OCR input, so marks can vanish from what the OCR sees with no visible change in the output PDF.

Evidence and limits: Doc quotes verified and confirmed in source code (thresholding_method default Otsu, absent at 4.1.1; make_intermediate_images builds a separate OCR image for --clean). Two qualifiers: (1) the dumped image is what layout analysis uses, while the LSTM recogniser reads line crops from the grey/original image when available, so a bad dump indicates segmentation problems and a clean dump does not rule out recognition errors; (2) the docs give no frequency of content loss and no example of deleted punctuation, so harm to decimal separators or minus signs on these statements is a hypothesis. Experiment: toggle --clean and each thresholding method one at a time, diff the dumped images around known commas, periods and signs, and score field exactness.

Sources: https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html, https://ocrmypdf.readthedocs.io/en/latest/cookbook.html

### F3 (confidence: medium; vote: 3-0 (claim 9); 2-1 (claim 10))

Failure analysis, glyph size: recognition depends non-monotonically on character size, so both under-resolution and over-upscaling are candidate causes. Archived official guidance says accuracy drops below 10pt at 300 dpi and rapidly below 8pt; x-height of about 20 px is typical at 10pt/300 dpi, below 10 px accurate results are unlikely, and below about 8 px text is mostly removed as noise. For the LSTM engine the same FAQ reports a maximum useful x-height of roughly 30 px. The optimum for this task, especially for digits, must be measured, not assumed.

Evidence and limits: Quotes verified verbatim; the page archives the FAQ for Tesseract 2.x-4.00alpha (2018) and the current FAQ does not repeat it, though the current ImproveQuality page still links to it. The lower bound was written for the legacy engine (transfer to LSTM is inference). The upper bound is hedged in the source and rests on a mailing-list thread that could not be read (unreachable); search-extract leads suggest the thread measured capital-letter height rather than x-height, and that one poster needed about 92 px digits to eliminate errors, which conflicts with a universal 30 px ceiling. Experiment: measure x-height and digit height in pixels on the scans, then rescale the same page to several target heights and plot exact-field accuracy for amounts and dates.

Sources: https://tesseract-ocr.github.io/tessdoc/tess3/FAQ-Old.html

### F4 (confidence: high; vote: 3-0 (claims 5, 6, 7))

Promising experimental change: RapidOCR (PaddleOCR PP-OCR models on ONNX Runtime, CPU) is now a drop-in second engine inside OCRmyPDF (--ocr-engine rapidocr, since 17.14.0), runs offline with the bundled PP-OCRv6 model for English and about 45 Latin-script languages, and needs no Tesseract. Its claimed advantage on numbers and table cells is an unquantified documentation assertion, and it has a documented failure mode on exactly the small marks this task cares about: pages whose longer side exceeds 2000 px are downscaled by default (about 180 dpi for a 300 dpi Letter page), and 17.14.2 fixed lost thin characters and misread digits yet still kept only 222 of 229 '<' signs on one table.

Evidence and limits: All integration facts verified against docs, release notes, PyPI and plugin source (DEFAULT_MAX_SIDE_LEN = 2000; the shrunk image is used for recognition as well as detection). Costs are the maintainers' estimates: roughly 4x Tesseract CPU time, about 1.2 GB memory per worker (about 2 GB at 4000 px), about 340 MB added by the extra (docs say about 500 MB for the Docker image). Constraints: official Docker images exclude it and only the Ubuntu image can be extended; only the fpdf2 renderer is supported (sandwich is rejected); with --rotate-pages an orientation model must be pre-fetched for a fully offline image. The feature was under two weeks old at verification (three releases in eight days), so maturity is low. No source compares it with Tesseract numerically. Whether its word boxes suit the existing positional parser is untested. Experiment: build the custom image, run both engines on the paired page with --rapidocr-max-side-len raised to native resolution, and compare exact-field accuracy plus the overlap of their errors.

Sources: https://ocrmypdf.readthedocs.io/en/latest/cookbook.html

### F5 (confidence: high; vote: 3-0 (claims 11, 14, 16, 17))

General OCR benchmark rank does not predict exact numeric accuracy or transfer to a specific document type, so engine choice must be decided on the user's own statements. On 60 degraded phone photos of printed reports, PaddleOCR and docTR had almost identical CER (0.111 vs 0.108) but very different verbatim numeric-span accuracy (0.674 vs 0.884); Tesseract had worse CER (0.189) but a higher numeric point estimate than PaddleOCR (0.756). Across five document benchmarks no engine was consistently best. PP-OCRv5's headline OmniDocBench advantage over Tesseract (0.067 vs 0.324 edit distance) shrinks to 0.058 vs 0.096 on English, because Tesseract's overall figure is driven by Chinese (0.551).

Evidence and limits: Three independent primary sources read in full. Qualifiers: in the clinical-report study only the docTR-vs-PaddleOCR numeric difference is statistically supported (Tesseract-vs-PaddleOCR intervals overlap), CER there was computed after removing punctuation while numeric spans keep it, and within one engine CER and numeric accuracy do correlate. The multi-benchmark study confounds dataset with language, uses n=50 per set, is a work-in-progress preprint, and Tesseract was never best in any column. The PP-OCRv5 paper is a vendor preprint; its comparison rows are copied from the OmniDocBench repository, its overall column appears to be the mean of EN and ZH, and it omits an older PaddleOCR row that would score better. Correction carried forward: Tesseract's 0.984 is the 'Horizontal' (vertical-layout) column, not Rotate90 (0.117). None of the benchmarks contain bank or card statements or flatbed-degraded scans.

Sources: https://arxiv.org/abs/2511.13523, https://www.alphaxiv.org/abs/2607.16203.md, https://arxiv.org/abs/2603.24373

### F6 (confidence: medium; vote: 3-0 (claim 15))

Architectural alternative with limits: compact multimodal models run locally were the most accurate on numbers in the one degraded-image study, but still far from exact and not CPU-feasible. Qwen-2.5 VL, Phi-4 MM and InternVL-3.5-4B reproduced 92.7-95.0% of numeric spans verbatim (best upper 95% bound 0.979), i.e. a miss rate of about 1 in 14 to 1 in 20, and no evaluated system approached exact numeric recovery. They are a possible third reader on a GPU host, not a route to unattended exactness.

Evidence and limits: Table values confirmed in both the arXiv version and the peer-reviewed EACL 2026 Industry Track version. Qualifiers: a miss means no verbatim match after alignment (attached punctuation differences count), so it is not always a misread digit; the setting was zero-shot whole-page transcription of phone photos with no preprocessing or field cropping, so the figures are not an upper bound for a tuned pipeline; the models needed about 17-18 GiB of VRAM and 11-67 s per image; newer or OCR-specialised models were not tested. Generative models add a failure mode that conventional OCR lacks (plausible but unprinted values); the supporting reference for that was seen only as a search extract. Such models also give no word boxes for a positional parser (inference). Single source, single domain.

Sources: https://arxiv.org/abs/2511.13523

### F7 (confidence: high; vote: 3-0 (claim 21))

Exactness cannot be assumed from high character accuracy: small character error rates compound into frequent field and near-certain table-level errors. Under an independent-error model, 95% character accuracy gives at least one error in 95.4% of tables of ten six-digit numbers; the corresponding per-field probability is 1 - 0.95^6 = 26.5%. At 99.9% character accuracy the same table still contains an error in about 5.8% of cases. This is why every amount needs an independent check, and why (inference) a statement-level balance check, which can pass when errors offset or fall in non-summed fields such as dates and descriptions, is not sufficient on its own.

Evidence and limits: The 95.4% figure is the paper's own back-of-envelope binomial calculation (60 trials), recomputed by the verifier; it is a table-level probability, and the 26.5% per-field and 5.8% figures are verifier arithmetic under the same model. Real OCR errors cluster, so independence overstates the share of fields affected at a given character error rate. The 95% input is illustrative, not a measured rate for any engine. The statement about balance checks is reasoning consistent with the brief, not a finding from a source.

Sources: https://arxiv.org/pdf/2204.00052

### F8 (confidence: medium; vote: 3-0 (claims 18, 19, 20, 22))

Verification by redundancy: combining several independent readings reduces errors and, more usefully here, exposes them as disagreements, but it cannot correct or detect errors that all readers share. Five OCRopus models trained on different folds and combined by majority vote cut character errors by 8-35% relative to the best single model on seven early printed books, with confidence-weighted voting adding a further small gain. A practitioner's guide for balance-sheet digitisation describes word-level then right-aligned character-level voting that can recover a number every engine misread, provided errors are idiosyncratic and each engine finds the token. A 2013 paper applies the same idea within one engine by OCRing several global-threshold binarisations of one grayscale image. Missing or heavily degraded glyphs are misread by every voter and cannot be restored by voting; unanimous misreads also produce no disagreement signal.

Evidence and limits: The voting figures were checked against Table IV of the paper (the paper's prose says 16% for the best model, contradicting its own table; the confidence-voting increment was not significant for two books). That evidence is for book-specific LSTM models on historical print with 1.6-12.7% baseline CER; transfer to Tesseract, to heterogeneous engines and to near-zero-error digit fields is a hypothesis, and the authors' explanation of the shrinking gain is an expectation, not a measured residual analysis. The balance-sheet guide gives a worked example and the authors' experience, with no quantitative ablation, and mostly concerns cloud engines; right-alignment fails if a trailing digit is dropped. The multi-threshold method rests on the abstract only (full text closed, dblp unreachable), predates LSTM engines, and two claims carrying its quantitative results were refuted in verification, so no numbers from it are used. Experiment: on the paired page, measure how many wrong fields each of the following flags as a disagreement, and how many wrong fields pass unanimously: Tesseract vs RapidOCR; Tesseract at two or three thresholds or scales.

Sources: https://arxiv.org/abs/1711.09670, https://arxiv.org/pdf/2204.00052, https://dblp.org/rec/conf/drr/LundKR13

### F9 (confidence: medium; vote: 3-0 (claims 12, 13))

Low priority: a post-hoc classifier that re-checks visually similar characters is weakly supported for this task. In its own evaluation only 53.8% of baseline errors (169 of 314; Tesseract 30 of 59) were single-character substitutions within its confusable set; insertions, deletions, transpositions and segmentation errors (such as 'rn' read as 'm' or '13' as 'B') are out of reach because it inherits the OCR engine's character boxes. All results are on synthetically rendered, clean-background strings, with font-family overlap between training and evaluation, and the authors state that performance on scanned or degraded images remains to be established.

Evidence and limits: Full text of a one-month-old, non-peer-reviewed preprint; the limits are the authors' own statements. Within the reachable set the paper reports an 87.3% correction rate and a 2.3% false-correction rate, which matters because a false correction on an amount is an undetected error. The Tesseract share rests on 59 errors. For statements, a dropped decimal separator or minus sign is a deletion, which this class of method cannot address at all.

Sources: https://arxiv.org/abs/2610.22726

### F10 (confidence: low; vote: synthesis of claims 0-22; not separately voted)

Prioritised recommendation (synthesis and inference; no source tested this on statements). Quick wins, all config-level and compatible with the existing positional parser: (1) dump and inspect the binarised image and turn off --clean/--remove-background unless shown harmless; (2) A/B thresholding methods; (3) A/B a no-dictionary config; (4) measure glyph height and test rescaling; (5) test PSM 4/6/11 and row-cropped PSM 7. Promising experiments: targeted re-recognition of cropped amount and date cells with a restricted character set; RapidOCR at native resolution as an independent second reader; multi-threshold or multi-scale re-reads of the same engine. Architectural alternative: a local vision-language model as a third reader where a GPU exists. Workflow: auto-accept a row only when independent readings agree exactly and field formats and statement arithmetic hold; send every disagreement, format violation and low-confidence field to a human with the image crop; treat description text and unanimous-agreement fields as unverified unless spot-checked.

Evidence and limits: Each element is derived from the findings above, but the ordering, the expected benefit and the acceptance rule are judgement, not published results. Known weaknesses of the workflow: unanimous misreads pass silently (bounded only by sampling audits); correlated errors between engines that share preprocessing reduce the value of agreement; RapidOCR integration is immature; no surviving claim addresses confidence calibration, so 'low-confidence' thresholds must be calibrated locally. The paired electronic original should be used only to score experiments, never to tune templates or thresholds that are then evaluated on the same document.

Sources: https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html, https://ocrmypdf.readthedocs.io/en/latest/advanced.html, https://ocrmypdf.readthedocs.io/en/latest/cookbook.html, https://arxiv.org/abs/2511.13523, https://arxiv.org/abs/1711.09670, https://arxiv.org/pdf/2204.00052

## Caveats

Coverage gaps: no surviving claim addresses research question 4 (layout templates, registration, ruling-line removal for gap months, overfitting to the paired document) or question 5 (evaluation protocol, confidence calibration, undetected-error rate, review effort), and none addresses how to verify description text or small punctuation beyond showing that these are fragile. Recommendations in those areas are inference and are labelled as such.

Assumptions: the brief's 'stated technical and privacy constraints' and 'previous experiments' were not supplied. Offline, CPU-only, Docker, a positional parser fed by word boxes, ruled tables and European number formats are assumed, not known. A finding may duplicate or contradict an experiment the user has already run.

Evidence strength: nothing here was measured on credit-card or bank statements. The Tesseract and OCRmyPDF material is maintainer guidance without benchmarks, some of it written for the legacy engine. The numeric-accuracy evidence comes from one study of 60 phone photos of clinical reports. Voting evidence comes from historical print with book-specific models. Three sources are non-peer-reviewed preprints (2607.16203, 2610.22726, and the vendor-authored 2603.24373). The multi-threshold paper (Lund et al. 2013) was read at abstract level only; its dblp page and full text were unreachable, and two claims carrying its quantitative results were refuted (0-3 and 1-2), so those numbers are excluded. The Google Groups thread behind the 30 px upper bound was unreachable; details from it are search-extract leads.

Corrections applied to the input claims: the binarised dump is <outputbase>.processed.tif on Tesseract 5.x (tessinput.tif is 4.x only); Tesseract's 0.984 OmniDocBench figure is the 'Horizontal' layout column, not Rotate90; the 95.4% compounding figure is table-level (per-field is 26.5%); the compact-VLM miss rate is about 1 in 14 to 1 in 20, and a miss is a non-verbatim span, not necessarily a wrong digit.

Time sensitivity: the RapidOCR engine in OCRmyPDF was released on 2026-11-08 and had three releases in eight days as of 2026-11-21; defaults, costs and bugs may change quickly. Model and benchmark figures for PP-OCR and vision-language models date quickly.

Process: this step synthesised verified claims only; no new sources were read and no experiments were run.

## Open questions

- On the actual statements, how are the remaining errors distributed across missing image information, binarisation or cleaning loss, segmentation, character substitution, coordinate assignment and parsing, as measured by the cropped-cell, dumped-image and config A/B experiments?
- How correlated are Tesseract and RapidOCR (and multi-threshold Tesseract re-reads) errors on these scans, i.e. what share of wrong fields is flagged by disagreement and what share passes unanimously and undetected?
- Can ruling lines be removed and columns registered using only information in the gap-month scans themselves (for example a template derived from printed layout features), and how should this be validated without tuning on the paired electronic original?
- Are Tesseract and RapidOCR word or character confidences calibrated well enough on amounts, dates, signs and decimal separators to set a review threshold, and what independent evidence, if any, can verify description text and small punctuation that no arithmetic constraint covers?

## Refuted in verification

- (0-3) Combination is done at the text level by aligning the OCR outputs of the differently thresholded images into a word lattice of alternatives. The lattice (oracle) word error rate was 7.6% with two thresholds and 6.8% with five, i.e. the correct word is present among the alternatives far more often than in any single OCR output (baseline WER 13.8% or higher), and most of the oracle gain comes from the second threshold. Source: https://dblp.org/rec/conf/drr/LundKR13
- (1-2) After committing to a single hypothesis from the lattice (using the selection method of Lund et al. 2011), the achieved WER was 8.41%, versus 13.8% or higher for single-binarization OCR on the same corpus. The realized result (8.41%) is worse than the lattice oracle bound (6.8%), so automatic selection does not recover all of the information the lattice contains. Source: https://dblp.org/rec/conf/drr/LundKR13

## Orchestrator note

The verification budget covered 25 of 115 extracted claims. Tracks 4 and 5 (verification and calibration; templates, registration and evaluation) had almost no voted claims, which is why the synthesis reports no evidence for research questions 4 and 5. A second round verifies those claims against the full texts and searches the remaining gaps.
