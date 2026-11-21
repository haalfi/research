Research objective
Determine the most reliable practical approach for extracting transaction data exactly from degraded scanned credit-card statements, under the stated technical and privacy constraints.
The current Tesseract/OCRmyPDF pipeline is a working baseline, not a mandated architecture. Previous experiments are evidence of what has and has not worked so far, not proof that related approaches cannot work.
Prioritize exact recovery of dates, signed amounts, currencies, and descriptions. Also prioritize reliable detection of errors that cannot be automatically corrected.
The solution must work on statement months for which no corresponding electronic original exists.
Research questions

1. Failure analysis: What are the likely causes of the remaining errors? Distinguish missing information in the image, preprocessing artifacts, segmentation failures, character recognition errors, layout/coordinate errors, and downstream parsing errors. Which experiments can distinguish these causes?
2. Candidate solutions: What established techniques offer the greatest potential improvement? Consider image acquisition, preprocessing, OCR configuration and models, targeted field recognition, alternative local OCR engines, layout-aware processing, and constrained post-processing. Do not limit the investigation to these examples.
3. Exactness and verification: How can fields be validated, corrected, or flagged for human review? Distinguish hard constraints, probabilistic evidence, and information that cannot be independently verified. Pay particular attention to description text and small punctuation marks.
4. Generalization: How can the pipeline operate without the matching electronic original? Investigate reusable layout templates, registration, and rule removal using only information available for real gap months. Identify approaches that risk overfitting to the paired test document.
5. Evaluation: How should end-to-end accuracy be measured? Include exact-field and exact-row matches, false-positive and false-negative errors, confidence calibration, undetected error rates, and manual review effort. Explain how to test on representative degraded scans without contaminating the evaluation with reference data.
6. Practical recommendation: Compare promising solutions by expected accuracy, feasibility, computational and installation requirements, maintainability, and compatibility with the existing positional parser and offline Docker environment.

Requested research output
Provide an evidence-based, prioritized recommendation rather than a broad catalogue of OCR technologies.
For each promising approach, explain:

* What failure mechanism it addresses.
* What evidence supports its effectiveness, distinguishing published results from hypotheses specific to this task.
* How it could integrate with the existing pipeline.
* What small, controlled experiment would verify its usefulness.
* What limitations or new failure modes it introduces.

Identify quick wins, promising experimental changes, and potentially worthwhile architectural alternatives.
Do not assume that higher general OCR benchmark accuracy implies higher exact-field accuracy on these statements. Do not assume that an arithmetic balance check guarantees that every individual transaction is correct.
If fully automatic exact extraction cannot be assured, recommend a workflow that minimizes undetected errors and human verification effort.
