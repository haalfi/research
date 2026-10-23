# Network access during the verification pass

Date: 2026-10-22. Egress goes through the session's agent proxy.

## Preflight (input § 0)

    curl -sS -o /dev/null -w "%{http_code}\n" https://arxiv.org/abs/2509.22908   -> 200

Passed, so the pass ran on full texts. Spot check at start:

| Host | Code |
|---|---|
| arxiv.org | 200 |
| hadoop.apache.org | 200 |
| docs.python.org | 200 |
| docs.aws.amazon.com | 200 |
| raw.githubusercontent.com | 200 |
| dl.acm.org | 403 |
| github.com (HTML via curl) | 400/403 → anonymous `git clone` used instead |

## Unreachable, no alternate found (these cause the 15 "unverifiable" verdicts)

| Host | Failure | Blocked work (log IDs) |
|---|---|---|
| IEEE Xplore / researchgate.net / CORE | bot challenge / 403 / Cloudflare | EARS RE'09 figures (T1-Q6) |
| cacm.acm.org, queue.acm.org, dl.acm.org | 403 | CACM 2025 TLA+ quote (T2-08); Newcombe CACM 2015 print text; Grieskamp 2011 (T3-08) |
| apps.dtic.mil | 403 | NRL SCR overview (T3-01); Heitmeyer & Labaw (T1-31, T3-02) |
| sciencedirect.com | 403 | Parnas & Madey 1995 |
| nowpublishers.com | 403 | Benveniste monograph (T2-03); Burckhardt axiom names (T2-11) |
| procon.bg | 503 | Lawford & Wassyng 2012; Darlington source |
| cs.ucf.edu | TLS chain error | Larch FAQ; JML RM ch. 9 |
| cis.upenn.edu | TLS error, then 503 | Hughes et al. ICST 2016 (T3-10) |
| repositoriosdigitales.mincyt.gob.ar / ri.conicet.gov.ar | reset / timeout | Grieskamp alternates (T3-08) |
| eweek.com, jamasoftware.com | 403 | "250 person-years" (T3-09); Jama webinar (T3-05) |
| docs.ogc.org / portal.ogc.org | 404 / HTML stub | OGC policy 08-131r3 (T4-19) |
| repository.tudelft.nl | reset | TU Delft thesis (T5-31) |
| event-b.org | self-signed certificate | Event-B half of T1-05 |
| OpenReview PDFs | 403 (abstracts only) | Vericoding TMLR camera-ready |
| — (no open copy) | — | Börger ASM ground model (T1-09) |

## Failed, but an alternate copy of the same work was read

microsoft.com research PDFs (403 for one track; other tracks reached MSR copies),
hal.science (bot wall; one HAL doc reached), web.archive.org (reset), dblp.org (bot
challenge), hub.hku.hk and discovery.ucl.ac.uk (403), cs.utexas.edu and
web.eecs.umich.edu (TLS chain), pamelazave.com (reset; read via WebFetch),
iso.org, opus.bibliothek.uni-augsburg.de, kluedo.ub.rptu.de, api.github.com (403),
Semantic Scholar API and w3.org (429, then OK).

## Failure classes

1. **Publisher / bot walls** (403, Cloudflare, bot challenge): IEEE, ACM, DTIC,
   ScienceDirect, nowpublishers, ResearchGate, OpenReview. Not fixable from inside
   the session; needs access from outside (library copy, author request).
2. **TLS chain / certificate errors**: cs.ucf.edu, cis.upenn.edu, cs.utexas.edu,
   web.eecs.umich.edu, event-b.org. Possibly fixable: check `/root/.ccr/README.md`
   and `$HTTPS_PROXY/__agentproxy/status`, then retry. Not attempted yet.
3. **Transient** (reset, timeout, 503, 429): procon.bg, mincyt, conicet, TU Delft,
   web.archive.org. Worth one retry in a later session.
