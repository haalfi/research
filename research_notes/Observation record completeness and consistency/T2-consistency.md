# T2. Internal consistency of semi-structured prose

Votes are confirm-refute from three adversarial verifiers over full texts.

## 1. Inspection reading techniques

### Porter, Votta & Basili, "Comparing detection methods for software requirements inspections" (TSE 21(6) 1995) — A

- Checklist reviewers were **no more effective** than ad hoc reviewers.
  Scenario-based reading, where each reader hunts one defect class, had a
  higher fault detection rate than both. (vote 3-0)
- n: 48 graduate students in 16 three-person teams, 2 SRS documents (WLMS,
  CRUISE). "Correct" meant faults seeded or known in the documents.
- **Refuted (1-2):** that scenario readers were better on their *targeted*
  classes and no worse on others. The mechanism is not established.
- External replications did not reproduce the scenario advantage (Fusaro et
  al. 1997; Miller et al. 1998; Sandahl et al. 1998). A verifier noted this;
  it was not verified from full text here.
- Human-only evidence.

### Fabbri et al., PBR vs checklist replications (ICMC-USP TR-225, via UMD) — B/C, unrefereed technical report

- No significant technique effect on individual effectiveness (p = 0.404,
  0.202, 0.144 pooled). The **document** effect was significant (p = 0.0059,
  0.0419, 0.0009). Individual effectiveness was low under both techniques:
  11.7% vs 13.8% of known defects. (vote 3-0)
- **Refuted (0-3):** the team-level null result (nominal teams of 9).
- Human-only evidence.

### Disconfirming search (a): result

**Partly confirmed.** Checklist reading does not reliably beat ad hoc
reading. PBR did not beat checklist reading individually in the replication
that survived. Scenario reading had one positive original study, and the
replications cited by a verifier failed to reproduce it. In these studies,
which document is read matters more than how it is read.

*Inference for agent readers:* RFC-0028's reader brief is already a
defect-class brief: contradiction, extent, reason against outcome, dialog
coverage. That is scenario-based reading compressed into one reader. The
evidence favours a narrow class per reader over one reader with four
classes. It does not show that splitting classes across readers raises the
union, so splitting is a hypothesis to test on OP-01, not a finding. No
study of mixed prose-and-table documents was found.

## 2. Contradiction detection by LLMs and NLI

### Fazelnia, Koscinski, Herzog, Mirakhorli, "Lessons from the use of NLI in RE tasks" (RE 2024; arXiv 2405.05135) — A-pre

- Zero-shot, cross-project conflict detection. 7 projects, 469
  requirements, 136 conflicting pairs. A RoBERTa NLI model beat ChatGPT
  (GPT-3.5) on F1 in every project: **22 to 55% vs 9 to 30%** (unweighted
  means about 37% vs 15%). (vote 3-0)
- NLI on Library: 80% recall at 19% precision. On ETCS: 50% recall at 27%
  precision. ChatGPT recall: 6 to 23%.
- "NLI could not detect composite conflicts caused due inter-dependencies
  among more than two requirements." An LLM given all the requirements found
  some composite conflicts. (vote 3-0 / 2-1)
- The NLI model was fine-tuned leave-one-project-out. The authors built the
  datasets. Agents measured: GPT-3.5.

### Gärtner & Göhlich, ALICE (Automated Software Engineering 31:49, 2024) — A

- A formal-logic decision tree (7 questions) with an LLM. 87 curated pairs:
  accuracy 72%, recall 75%, precision 83%, against a GPT-3 yes/no baseline
  at 47 / 32 / 80. 1071 industrial pairs: 17 of 26 contradictions found
  (65%; the paper says 60%) at 94% precision. The GPT-3 baseline found 0 of
  26, with 4 false positives. (vote 3-0)
- ALICE decides only pairwise contradiction. Exclusions defined elsewhere in
  the document are out of scope.
- **Tool authors evaluating their own tool**, against a weak baseline.
  Agents measured: GPT-3.

### Fazelnia, Mirakhorli, Bagheri, SAT-LLM (short paper; NSF PAR 10574434) — A-workshop

- GPT-4 translates requirements into first-order logic, and Z3 finds minimal
  unsatisfiable subsets. On 55 Broker requirements (15 conflict sets, 4
  composite): **P 1.00, R 0.83, F1 0.91**. Direct GPT-4 prompting: P 0.85,
  R 0.31, F1 0.46. Direct GPT-4 found 36% of two-requirement conflicts and
  25% of composite ones. (vote 3-0)
- n = 15 conflict sets, one tuned prompt, no repeated runs. **Tool authors
  evaluating their own tool.** The extraction step (requirements into FOL)
  was **not validated separately**.

### Disconfirming search (b): result

**Largely confirmed for the setups measured.** Pairwise detectors, NLI or
2023-era LLM, ran at precision 19 to 67% and recall 6 to 80%. On the hardest
datasets a reviewer would read three to five false alarms per real conflict.
Neither paper analysed false positives. The false-alarm reading is
*Inference* from reported precision and recall. The hybrid (LLM extraction
plus a solver) had high precision, but only in self-evaluated small studies.
All models are 2023 to 2024 vintage. Current models may do better or worse.

### Pairwise vs three or more statements

- By construction, pairwise checks miss composite conflicts (NLI, ALICE).
  Whole-set prompting recovered some (GPT-4: 25% of composite). A solver over
  extracted logic recovered most (SAT-LLM: MUS over all statements).
- **Own trial, OP-01** (`T0-own-trial-op01.md`): of the 27 known defect
  pairs, at least one involves a *general clause* sharing almost no
  vocabulary with what it governs. Examples: D1's "both forms behave alike"
  against D12 and D13 (O41), and D33's typing principle against D28 and D38
  (O22). Some known items are inherently three-way: O28 rests on D22, D31,
  D42 and D43 together, and O14 on D19, D20, D34 and D35. Pairwise selection
  by shared vocabulary kept 24 of 27 known pairs only at 368 of 946 pairs
  judged.

## 3. Extracting the record into a structured form

- SAT-LLM and ALICE both extract into logic and then check mechanically.
  Neither measured the extraction step. **Errors introduced or hidden by
  extraction are unmeasured in every surviving source.**
- Settled earlier (round-trip and dual formalization): two independent
  extractions catch divergent readings and miss shared ones. That is the
  only available validation of an extraction step. Here it means extracting
  twice, by two agents with different prompts or models, and diffing the
  claim sets.
- One acknowledged extraction loss in this run: Quasar (arXiv 2601.19693, verified;
  see T3 and report) filtered sections by keyword before LLM scoring, "This
  means that some information may have been lost."

### Own trial: what lexical extraction loses (`T0-own-trial-op01.md`)

A lexical extent register over OP-01's Decision, Options and Recommendation
text gave 114 sentences in 42 decisions. It held 4 of 7 known extent defects.
It missed all three that were:

- an **implicit universal**: D22, "the read that needs it fails with the
  changed category", with no quantifier (O28);
- a **table row**: D34, "E1 to E5 against a pinned stream | changed" (O33);
- a **table read as complete**: D38's caller-level table (O37).

*Inference:* an extraction that tracks claims of extent must produce typed
claims, not sentences:

- `Closed(list, domain)`: a list or table read as complete over a named
  domain, such as "categories surfacing from a stream read" or "O3 actions".
- `Rule(condition → outcome)`: every unconditioned rule is a universal over
  its condition.
- `Adopts(decision, option text)`: the option's text, verbatim, as a claim
  of the decision.
- `Member(x, domain)`: every decision that names x in a context of that
  domain.

Then: every `Member` against every `Closed` of the same domain, every `Rule`
against every outcome for the same condition, and every `Adopts` against
every later `Rule` or `Closed`. These checks are mechanical once extracted.
Extraction is the judged step and must be validated by dual extraction.

## 4. Claims of extent and adopted-by-reference text: published techniques

- **SEURAT** (Burge, WPI PhD thesis 2005): consistency checks over
  *structured* rationale, re-run on every edit, such as "selection
  contradicted" and "opposed by a selected alternative". Its "Tradeoff
  Missing" flags a one-sided argument against a declared knowledge base.
  Verified in full text (§7.3); its evaluation (20 subjects) did not measure defect yield. It works on structured rationale, not
  prose. Its evaluation did not measure defect yield (see report § (d)).
- No surviving source tracks "only" or "every" claims or adopted option text
  specifically. RFC-0028's evidence table is the only measurement: C2 (an
  adopted option's wording against an earlier decision) was found by no run.

## Catches and misses (summary)

| Option | Catches | Misses | Precision / recall | Agents measured |
|---|---|---|---|---|
| Checklist reading | some defects | — ; no better than ad hoc | 11.7 to 13.8% individual | human-only evidence |
| Scenario (defect-class) reading | more defects than checklist in one study | replications failed | — | human-only evidence |
| Pairwise NLI | two-statement conflicts | composite conflicts; context elsewhere | P 19 to 67%, R 50 to 80% | NLI model |
| Pairwise or whole-set LLM (2023) | some composite | most conflicts | F1 9 to 30% (GPT-3.5); R 0.31 (GPT-4) | yes |
| LLM to logic to solver | composite via MUS | extraction errors (unmeasured) | P 1.00, R 0.83, n = 15 sets, self-evaluated | yes |
| Typed extent register (own proposal) | Closed × Member, Rule × outcome, Adopts × later | anything the extraction misses | untested; lexical version 4 of 7 | no |
