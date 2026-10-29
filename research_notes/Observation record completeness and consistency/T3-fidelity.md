# T3. Fidelity of a decision to its elicitation dialog

Votes are confirm-refute from three adversarial verifiers over full texts.
Items marked *pending* were extracted from full text by the workflow but
dropped by its verification budget. They were re-checked by a separate
verification pass; see `T4-T5-verification.md`.

## 1. Base rate: how often an LLM condensing a dialog adds content

### Ramprasad, Ferracane, Lipton, "Analyzing LLM behavior in dialogue summarization" (ACL 2024; arXiv 2406.03487) — A

- About **23% of GPT-4 summaries** of SAMSum and DialogSum dialogs contained
  an inconsistency under span-level human annotation (over 30% pooled across
  LLMs). (vote 3-0 / 2-1)
- About **38% of LLM errors are "circumstantial inference"**: "inferred
  supplemental information, not explicitly stated in the content". It is the
  largest category the text quantifies. The paper does not call it the
  largest overall.
- Human labels are themselves imperfect: two expert annotators reached
  66.94% pairwise span F1. Any recall measured against them is capped
  accordingly.
- Setting: chit-chat dialogs, not design sessions; GPT-4 and Alpaca-13B.

*Inference for the record:* circumstantial inference is failure class 2's
shape. OP-01's O14 to O16, O31, O33, O36 and O37 are all text "which its
dialog did not ask": a list, a table row, a sentence or a table read as
complete, each a plausible consequence of the answer but not the answer.
An added-commitment check should look for **implied** commitments, not
invented facts.

### TofuEval (Tang et al., NAACL 2024) — A, pending

- Averaged over five LLMs, 17.5 to 27.8% of summary sentences and 30.4 to
  46.0% of summaries of MediaSum and MeetingBank dialogs were factually
  inconsistent (professional annotators, 1,479 summaries).
- Only single-sentence errors were annotated, so its detector figures do
  not cover cross-statement fidelity errors.

## 2. Detectors: how well do automatic or LLM judges find added content?

### Ramprasad et al. (as above) — A; authors evaluating their own detector

- QAFactEval: span F1 **8.54** (P 7.49, R 9.91), binary balanced accuracy
  39.84.
- The authors' few-shot ChatGPT mixture-of-experts span detector: span F1
  **33.22** (P 35.60, R 31.14), balanced accuracy 70.27. (vote 3-0)
- Agents measured: ChatGPT-era. Current models may do better.

### TofuEval — A, pending

- Open-source LLM evaluators: 50 to 60% balanced accuracy (50% is trivial).
  GPT-4 was best, at about 65 to 68% on main-topic summaries.
- Non-LLM metrics (AlignScore, SummaC, QAFactEval) had higher recall than
  every LLM evaluator across error types.
- Errors on the **main topic** of a dialog were about 10% harder to detect
  (GPT-4: 10 to 20% gap). The authors' reason: main-topic errors are less
  often extrinsic, newly added information, which detectors find most easily.

*Inference:* a decision **is** the main topic of its dialog. So the case that
matters, a decision going one step beyond the answer on the very question
asked, is the hardest one for a detector. An LLM fidelity judge comparing a
Decision with its Asked line should be expected to miss most of these. Its
output is leads for a human, never a verdict.

## 3. Agents writing decision records from dialog

### LLM agent turning meeting transcripts into ADRs (arXiv 2601.19693 or 2608.17694; see verification) — A-pre, pending

- Expert review found the agent "transformed tentative discussions into
  accepted decisions" and inserted unsupported claims. RAG enrichment brought
  in "500 concurrent connections and 5000+ Daily Active Users", which came
  from a retrieved external ADR, not the transcript.
- No hallucination or faithfulness rate was measured. Users' quality ratings
  (52 of 55 agreed with the extracted decision) came from students rating
  their own projects.
- Its self-check is an extract-critique loop (overlap, fragmentation,
  missing items, noise, scope duplicates). It contains **no check against the
  transcript**.

*Inference:* this is the same mechanism as OP-01's class 2, observed in
another pipeline. Upgrading a tentative answer to a decision, and importing
content from retrieved context, are the two shapes to check for.

## 4. Requirements traceability to elicitation sources

- No surviving source measures traceability from a requirement back to an
  interview or transcript excerpt for **fidelity**, as distinct from link
  presence. The project's pairing script already establishes link presence
  (an Asked line per decision, quote matching). What remains is the content
  check.

## 5. What a fidelity check on a record can be

*Inference, built on the above and on OP-01:*

1. **Mechanical (in place):** each Decision has Asked lines that pair with
   answered dialogs (`observe_dialogs.py`).
2. **Mechanical, new: claim-to-answer span alignment.** Split the Decision
   bullet into atomic claims, a judged step. For each claim, require a span
   in the answer, or in the option text the answer adopts, that it restates.
   A claim with no span is a **candidate added commitment**. This turns
   "does the decision go beyond the dialog" into "which claim has no source
   span". That is easier to check and to disagree about. Its error rate is
   unmeasured.
3. **Judged:** for each candidate, a reader decides whether the claim is a
   restatement, a necessary consequence, or a new commitment. Only the last
   is a defect. Expect low precision (T3 §2), so budget the human time for
   it.
4. **The reverse direction: dropped content.** O40 is a fidelity defect of
   the other kind: dialog option text ("on Local the third is
   NotADirectoryError ...") that the record's option and recommendation do
   not carry. Span alignment run from the dialog to the record finds these:
   each option sentence in the dialog must appear in the record's option.
   That check is mechanical where the log says the text was copied
   "verbatim", as the OP-01 log does. A diff is enough, with no judge.
5. **Adopted-by-reference text.** When a Decision adopts option (a) by
   label, the option's full text becomes the decision's claim. It must pass
   both the fidelity check (was the whole option what the answer chose?) and
   the consistency check (T2's `Adopts` claims). C2 and O29 were both
   adopted-option wording, and in RFC-0028's measurement no run found C2.

## Catches and misses (summary)

| Option | Catches | Misses | Measured | Agents measured |
|---|---|---|---|---|
| Asked-line pairing (in place) | missing or ambiguous pairing | content beyond the answer | n/a | script |
| LLM judge, decision vs dialog | some added content | most main-topic, implied additions | balanced acc. 65 to 70% (GPT-4 or ChatGPT-MoE); span F1 ≤ 33 | yes, 2023-24 models |
| Non-LLM factuality metrics | extrinsic additions; higher recall than LLM judges | implied commitments | span F1 8.5 (QAFactEval) | metric models |
| Claim-to-span alignment (own proposal) | claims with no source span | claims with a misleading span | untested | no |
| Dialog-to-record diff where copying is verbatim | dropped option text (O40's class) | paraphrased drops | untested; mechanical | no |
