# T5. Reviewer diversity (minimal)

Verified in a separate pass; see `verification-log.md`.

## Diverse perspectives vs readers of one kind (humans)

### Basili et al., "The empirical investigation of perspective-based reading", EMSE 1(2) 1996 — A; the authors developed PBR

- NASA/GSFC professionals (n = 12, then 13 or 14), the same documents and
  seeded defects as Briand et al. (T4).
- Nominal teams of 3: PBR teams were one Designer, one Tester and one User.
  Comparison teams were any 3 readers using their usual technique. Team
  detection rate:

| Run / documents | Usual | PBR | p |
|---|---|---|---|
| Pilot / generic | 44.3 | 52.9 | 0.066 |
| Pilot / NASA | 30.1 | 31.3 | 0.434 |
| 1995 / generic | 48.2 | 79.3 | 0.0007 |
| 1995 / NASA | 62.4 | 85.3 | 0.039 |

- Individually, only 1995 generic was significant (24.6 vs 32.1). The gain
  is a **coverage** effect of the union: "in generic documents there were a
  number of defects which were found by only one of the perspectives".
- Confounds: PBR was always applied on day 2 (learning), and the teams
  were simulated.
- The replication in T2 (Fabbri et al., technical report) found no
  individual effect. Its team-level null claim was refuted in verification,
  so the team-level evidence stands with Basili 1996 alone.
- Human-only evidence.

## Diverse models vs repeated sampling of one model

### Simecek et al., HoF-Bench, arXiv 2607.27030 (2026) — A-pre; authors evaluate their own scaffold

- Vulnerability rediscovery (95 CVEs). One pass each from four leading
  models covered an expected 68 CVEs. Four passes of the strongest single
  model covered 65. Twelve passes across three cheap models covered 70, at
  about half the cost.
- Going from one to four passes of one model added 12 to 20 CVEs. One pass
  recovered 68% of what four passes found.
- Small gain and no confidence interval. Code, not documents.

### Kumar, Bararia, Raj, arXiv 2606.15689 (2026) — A-pre; counter-example, unreliable

- "Ensembles hurt F1. The models largely detect the same bugs". The
  reported union recall falls below a member's recall, which is impossible
  by definition, so the table is internally inconsistent.

### Not found

- No study of LLM model diversity vs repeated sampling for **requirements
  or document** review.

## What T2 to T4 need from this

*Inference:*

- For **coverage** (T2), human evidence favours readers with different
  assigned perspectives or defect classes over identical readers. The
  effect is in the union, and is large on some documents and absent on
  others.
- For agents, repeated sampling of one model does add finds (HoF-Bench:
  about a third more over four passes), and model diversity adds a little
  more per cost. Both results come from code, from the tool's own authors.
- For **estimation** (T4), diversity cuts both ways. Diverse readers
  violate CR's equal-catchability and independence assumptions in
  different ways. Diversity across kinds (unprimed vs primed) makes the
  per-kind populations disjoint, so CR must be applied **within** a kind.
  It cannot be applied across kinds.
- The OP-01 data fit this. Two readers of one kind overlapped on 11 of
  14. A reader of another kind (primed) found 4 items outside both.
  RFC-0028's two runs of one reader, with and without the adopted option
  text beside each Decision, found different subsets (C1 in one only).
