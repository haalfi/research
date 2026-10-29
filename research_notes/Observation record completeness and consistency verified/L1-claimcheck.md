# L1. claimcheck — verified by the run's author

## Citation and grade

- Amster, An, Baker, Graciolli, Henniger, Amin, "claimcheck: Measuring and
  Improving Specification Faithfulness", arXiv 2610.17358v1, 12 Oct 2026.
  Affiliations: UBA, UPenn, PolicingLab, Midspiral, Harvard.
- Grade **A-pre**.
- Full text read: **y** (arXiv HTML; inline figures recovered from the math
  alttext).
- **Authors evaluating their own tool.** Code is at
  github.com/metareflection/claimcheck. The tool was started at a Claude
  Code hackathon.

## What it does

The check runs in two model calls:

1. An **informalizer** (claude-haiku-4.5) restates the formal artefact in
   English **without seeing the requirement**.
2. A **judge** (claude-sonnet-4.6) compares that restatement with the
   requirement and says whether they "express the same guarantee". In the
   main variant the judge does not see the artefact.

## What was measured

- Benchmark: 3,234 rows.
  - Dafny: 362 rows from CloverBench.
  - Lean 4: 1,296 rows; Isabelle: 920; Rocq: 656, all from PutnamBench.
  - Defective rows are mutations of the requirement or the artefact.
  - A third of the rows (1,029 of 1,854 faithful ones) are
    meaning-preserving rewrites, proved equivalent, so detecting an edit is
    not enough to score.
- "Correct": the label set by construction. A faithful row is the original
  or a proved rewrite. A defective row is a semantic mutation, whose label
  rests on the rule that produced it.
- Metric: macro recall, the mean of faithful-row and defective-row recall
  (balanced accuracy). No precision is reported.
- Baselines:
  - one zero-shot call shown both sides, answering YES or NO;
  - the same call given the judge's rewrite list and error vocabulary
    ("baseline + list").

## Results (Table 2, ± 95% interval)

| | Lean | Isabelle | Rocq | Dafny |
|---|---|---|---|---|
| zero-shot baseline | 79.7 | 81.5 | 79.6 | 84.0 |
| baseline + list | 83.2 | 85.3 | 83.0 | 88.9 |
| claimcheck, judge also sees artefact | 84.8 | 87.2 | 83.5 | 91.7 |
| claimcheck | 87.9 | 91.3 | 88.0 | 93.1 |

- **The claimed figures are confirmed.** claimcheck gains 8.2 to 9.8 points
  over the zero-shot call and 4.2 to 6.0 over the informed call.
- **Most of the gain is on faithful rows.** Faithful-row recall rises from
  66.5–85.6% (list baseline) to 77.8–91.7%.
- **Defective-row recall "moves less".**
  - It rises on Dafny, 92.3 to 94.5%.
  - It falls by up to 3.3 points on Isabelle and Rocq.
  - It falls on Lean, 95.9 to 88.4%.
  - So claimcheck mainly **removes false alarms**; it does not catch more
    defects.
- Paired McNemar tests: claimcheck fixes more errors than it introduces on
  every language (Lean 148 vs 91; Dafny 24 vs 9, p = 0.014).
- **Showing the judge the artefact as well costs 1.4 to 4.5 points**:
  faithful-row recall is 9.9 to 12.0 points lower, so it raises more false
  alarms.
- Ablations (Table 3):
  - Dropping the back-translation costs 2.8 to 6.0 points, and lands below
    the list baseline.
  - **Letting the informalizer see the requirement costs 0.8 to 3.0 points,
    all on the defective side: defective-row recall falls by 6.0 to 8.8
    points.** This is the paper's central mechanism. A restatement written
    with the source in view echoes it, so a near miss reads as a hit.
- **Model sweep** (Table 4; the variant where the judge sees the artefact):
  - Weak judges gain a lot: gpt-5.6-luna +18.6 to 25.2, deepseek-v4-pro
    +6.2 to 27.5.
  - **gemini-3.7-flash already reaches 91.4 to 94.8 in a single call** and
    gains only 0.6 to 3.9, within a point of its list baseline. The authors
    call the gain "substitutive rather than additive".

## Limits stated by the authors

- The benchmark may be too easy. A single call scores 79.6 to 84.0, or
  83.0 to 88.9 with the list.
- On Isabelle and Rocq, `negate` makes up 92% and 83% of the defective rows,
  and it is the easiest defect.
- All artefacts are single contracts or theorem statements, "short enough
  that a requirement and its formalization can be held in view at once".
  Long developments are outside what was measured.

## Agents

Yes. Claude Haiku 4.5 and Sonnet 4.6, gemini-3.7-flash, gpt-5.6-luna and
deepseek-v4-pro, all 2026 models.

## Transfer: analogous

- In claimcheck, a derived artefact is checked against its source. Here the
  derived text is a Decision, and its source is the dialog answer.
- The decision is already prose, not a formal artefact, so whether a
  prose-to-prose restatement keeps the gain is *Inference*.
- The defects differ:
  - claimcheck's defects are mutations, dominated by negation.
  - The record's class 2 defects are implied additions on the dialog's main
    topic. That is subtler than negation, and closer to `forall_to_exists`
    or a loosened bound.

## Delta to the earlier report

1. **T3, the claim-to-span step: qualifies the design. A mechanism is now
   measured; the transfer is not.**
   - The earlier report § 2 T3 reads: "**Claim-to-span alignment** (own
     proposal): split the Decision into atomic claims; each needs a span in
     the answer or in the option the answer chose".
   - Change: the agent that splits the Decision into atomic claims must not
     see the dialog. A judge then compares each claim with the answer and
     sees neither the full Decision nor the dialog's options. That puts
     claimcheck's two measured choices into the record's check:
     - a blind restater (seeing the source costs 6.0 to 8.8 points of
       defect recall);
     - a judge who does not see the derived artefact (seeing it costs
       faithful-row recall).
2. **T3, the LLM judge row: qualifies it. The "judges are weak" picture is
   dated for short, formal, single statements.**
   - The earlier report § 2 T3 reads: "an LLM fidelity judge yields leads,
     not verdicts".
   - A 2026 single call reaches 91 to 95 balanced accuracy on short formal
     statements (gemini-3.7-flash). TofuEval's and Ramprasad's 2023-24
     figures (balanced accuracy 50 to 70) are for dialog summaries.
   - The verdict "leads, not verdicts" **stays** for the record, for three
     reasons:
     - no precision was reported;
     - the defects are mutations, not implied additions;
     - a decision record is long and cross-referenced, which the authors
       name as outside what they measured.
   - It now rests on transfer, not on evidence that current judges are weak.
3. **§ 5 debt item 1 (extraction error unmeasured): adds a measured design
   for validating an extraction.** It does not measure extraction error.
   - The earlier report reads: "No source measured what LLM extraction into
     logic or tables introduces or hides."
   - That still holds.
   - claimcheck gives a design that can validate each extracted claim:
     restate it in English blind to the record, then judge it against the
     record text. This complements dual extraction. Its error rate on
     extraction is unmeasured.
4. **§ 5 debt item 7 (2023-24 models): partly answered, for formal
   statements only.**
