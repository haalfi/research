# Open items after the verification pass

These are the items the pass could not close. IDs refer to
`research_notes/Black box boundary spec methods/2-verification/verification_log.md`.

## 1. Unverifiable: full text unreachable (15)

| ID | Claim | Blocker |
|---|---|---|
| T1-05 | Event-B half of "state vs time split" (TLA+ half confirmed) | event-b.org cert |
| T1-09 | ASM/Event-B state space as K1 precedent | no open copy (Börger) |
| T1-31 | Heitmeyer & Labaw reviewer-effort quote | apps.dtic.mil 403 |
| T1-Q6 | EARS RE'09 figures | IEEE / ResearchGate / CORE |
| T2-03 | Benveniste et al. operator detail | nowpublishers 403, HAL bot wall |
| T2-08 | CACM 2025 "struggled to become productive with TLA+" | cacm/queue.acm.org 403 |
| T2-11 | Burckhardt axiom names | microsoft.com / nowpublishers 403 |
| T3-01 | NRL SCR overview: four-variable model, NAT | apps.dtic.mil 403 |
| T3-02 | Heitmeyer & Labaw quote (mechanism confirmed elsewhere) | apps.dtic.mil 403 |
| T3-05 | Jama "drastic" improvement (D) | jamasoftware.com 403 |
| T3-08 | Grieskamp et al. 2011 "works and scales" | mincyt reset, conicet timeout, cacm 403 |
| T3-09 | Spec Explorer "250 person-years" (likely conflated; drop) | eweek.com 403 |
| T3-10 | Hughes et al. ICST 2016 Dropbox | cis.upenn.edu TLS/503 |
| T4-19 | OGC Modular Specification Policy 08-131r3 | docs.ogc.org 404 |
| T5-31 | TU Delft thesis on positive priming | repository.tudelft.nl reset |

Also unread: Parnas & Madey 1995 (sciencedirect 403; the original citation points to
a 2010 Parnas-only chapter), Newcombe et al. CACM 2015 print text (only the 2014 draft
was read), Vericoding TMLR camera-ready (OpenReview 403), Larch FAQ and JML RM ch. 9
(cs.ucf.edu TLS).

## 2. Not re-checked: outside the five tracks (still on search extracts)

Cirstea et al. (TLA+ trace validation), TraceLink (OOPSLA 2025), PObserve, Porcupine,
arXiv 2608.17388, FoundationDB simulation, McKeeman 1998, Jepsen MongoDB 4.2.6,
WebKit wasm spec-test translation, Eaton, arXiv 2409.14301, AUTOSAR "optionally".
The verified report marks each with `[not re-checked]`.

## 3. Remaining research gaps (evidence, not access)

- No source distinguishes a second API caller (O2) from an out-of-band store actor
  (O3) as different kinds of observer.
- No ready-made object type exists for a chunked stream with an extent.
- No controlled spec-format study exists for agents, EARS or decision tables, and none
  exists for human readers either.
- PyFilesystem2 is still not covered (T4).
- An ACM-only format study could have been missed, because dl.acm.org and dblp.org
  were blocked.

## 4. Suggested next steps

1. Retry the TLS-chain hosts after checking the proxy README and status. These are
   cs.ucf.edu, cis.upenn.edu and event-b.org.
2. Retry the transient hosts once: procon.bg, mincyt, conicet, TU Delft.
3. Get copies through outside access (library or author request) for EARS RE'09,
   CACM 2015 and 2025, the NRL/DTIC reports, the Benveniste monograph, and Parnas &
   Madey 1995.
4. Run a short pass over the § 2 not-re-checked list. Most of it is on arXiv or
   open pages.
