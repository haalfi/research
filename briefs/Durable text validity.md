# Research brief: durable text acted on without its validity being established

## Goal

Test the problem statement below against published evidence, before anyone designs a remedy. We want to learn which of its claims are established, contested or unstudied, under which names other fields already study the same problem, and which mechanisms anywhere give durable text a signal that can fail. We want to build on what exists rather than invent, and we want the strongest evidence against the statement as much as the evidence for it.

## Context

- Durable text lives in git and changes through reviewed pull requests. AI agents write and review a large share of it and act on it as instructions and as authority.
- For questions 6 and 7, build on the earlier run on branch `research/explicit-engineering-contracts`; you may read that branch.
- For the claims "What a text must say depends on its reader" and "Review has no stopping rule", the findings marked verified in https://raw.githubusercontent.com/haalfi/remote-store/master/sdd/research/research-appropriate-level-of-detail.md are the baseline. Challenge one only with new full-text evidence, and say so.
- For questions 3 and 6, the detection mechanisms and their warrant in https://raw.githubusercontent.com/haalfi/remote-store/master/sdd/research/research-inconsistency-detection-multi-artifact.md (§§ 1–3) are the baseline; don't survey them again.

## The statement under test

See `Problem statement v0.4` appended at the end of this brief, verbatim.

## Questions

1. Under which names and in which fields is this problem studied, in and beyond software? Examples, not a complete list: design rationale, documentation decay, assurance cases, legislative drafting and consolidation, clinical guideline maintenance, living systematic reviews, citation and retraction propagation, organisational memory.
2. For each bold claim of the statement: established, contested or unstudied? Give the strongest evidence on each side.
3. For each failure kind the statement names, and any it misses: which mechanisms give a text a signal that can fail, and what does each cover and miss? Include how fields whose work rests on durable text track whether a text is still valid after what it depends on has changed.
4. How does an unfounded claim become accepted knowledge through derived texts, repetition or generated text, and what has been shown to stop it?
5. Beyond the baseline: how do fields decide that a text is good enough to rely on (acceptance criteria, reader or task testing, sign-off), and with what evidence?
6. What is known about finding missing decisions and unmarked open points in text, by readers or tools, separately from resolving them?
7. First-hand evidence on AI agents reading durable text as authority: superseded or contradictory text, invented rationale, and agents used as verifiers grounded outside the text.

## Bring back

- Per question: findings with sources and dates, each marked first-hand study, standard, practitioner report or inference. Say where evidence is thin or contested.
- Per bold claim: a verdict with the strongest source for and against, and a suggested rewording where the evidence demands one.
- A map of mechanisms by failure kind: what each detects, what it misses, its cost, and whether agents were measured using it.
- Fields and terms we have missed.
- Disconfirming searches, each reported: evidence that this problem is solved somewhere, and evidence that it is not a real cost.

## Out of scope

- Style, readability and length of text as goals.
- Ambiguity taxonomies and terminology management, already covered by earlier runs.
- Verbosity of agents in conversation.
- Designing our process or choosing our remedy.
- Commercial products, except as a reference for which capabilities exist.

## Delivery

- Branch `research/durable-text-validity` from origin/main, title `Durable text validity`.
- Verdicts rest on full texts. Don't invent figures. Follow the repository's CLAUDE.md for layout and running.

---

## Problem statement v0.4

# Problem: durable text is acted on without its validity being established

Durable text is any text that outlives the work that wrote it and that a reader, human or agent, acts on later, wherever it is kept. It carries facts, decisions, reasons and instructions, and later work is built on what it says. Each kind is right in a different way: a fact by matching the world, a decision by having been made by the person who owns it, a reason by being what decided, an instruction by producing the intended outcome when followed. A text can record something correctly that is no longer valid to act on, such as a decision since superseded.

**What a text says is generally held to no check that can fail.** A machine can check what is mechanical, such as whether a reference resolves. Code can be held to repeatable tests that fail; what durable text says is generally held to no equivalent check. Where a claim can be checked against evidence, the step from the sentence to the check is itself a reading, and that reading is rarely checked in turn.

**A text goes wrong in at least three ways, and none needs to show.** It can misrepresent what is known, decided or intended. It can lose its validity, because what it depends on changes, and that change need not produce any signal in the text. It can be misread: the text is correct and current, and the reader derives the wrong action from it. Each can occur without the others, and the reader acting on the text can proceed without noticing any of them.

**What a text must say depends on its reader.** A text can be true and still not usable by the reader who acts on it. What it must say depends on that reader's knowledge and task, and that reader is usually absent while it is written. The writer's knowledge can conceal what the text leaves out, because the writer supplies what a later reader may not have.

**Review has no stopping rule.** A correction is usually new text with new claims, which the next reading judges again. Without acceptance criteria stated for a text, review has no criterion for when the text is good enough. A text fails by holding too little as well as too much, and a correction in either direction can cause the other.

**The costly defects are mostly misrepresentations beneath the wording:** decisions nobody made, commitments that contradict each other, premises nobody checked. Such a defect may show as an unclear sentence, which invites a wording fix that hides it, or not show at all: a clear sentence can state a decision nobody made, and two clear texts can contradict each other. Finding such a defect and resolving it are separate. A reader or an agent can find it and can mark what is undecided; only the owner of a decision can make it, so that person's attention limits how fast decisions are made. Without a record made at the time, a recovered reason often cannot be told apart from a reconstructed one.

**Agents make plausible text cheap, and can act on it without a trace.** Finished-looking text can accumulate, copies of one fact can diverge, and outdated text can stay where the next reader finds it. An agent can act on a plausible reading without establishing that it is the intended one, resolve a contradiction without exposing it, and supply a missing reason that later reads as recorded intent.

**A defect propagates as knowledge.** Durable text is often the basis for further durable text, code and tests. An inference recorded once can be read later as a decision, and the work built on it, its tests included, can agree with it. Internal consistency can grow while correctness falls, and later readers may no longer be able to tell the inference from the decision.

**An instruction cannot enforce itself.** A countermeasure written as text depends on the same reading it is meant to govern. Its presence does not establish its application.

**Not the problem:** an agent's verbosity in conversation, length as such, and natural language itself.
