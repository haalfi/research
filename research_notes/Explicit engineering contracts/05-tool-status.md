# Track 5: Tool status check (verified 2026-11-15)

Method: package registries (PyPI JSON, npm, crates.io, proxy.golang.org, Maven Central) and shallow `git clone` for latest commit date and LICENSE file.
api.github.com returned 403 in this session, so GitHub release pages were not used.
Search engines were used only to locate Paska and NALABS.

| Tool | Relevant detection | License (source) | Latest release | Latest commit | Status |
|---|---|---|---|---|---|
| Vale | Custom style rules (glossary/substitution, banned terms, vague words); Markdown-aware; GitHub Action | MIT (LICENSE) | v3.27.0, 2026-11-12 (goproxy) | 2026-11-12 | active |
| markdownlint-cli2 | Markdown structure; MD051 link fragments; Action, SARIF, pre-commit | MIT | 0.24.1, 2026-11-12 (npm) | 2026-11-11 | active |
| lychee | Broken URLs/local files; `--include-fragments` anchor checks; Action | Apache-2.0 OR MIT | 0.24.2 crates, 2026-05-01 | 2026-11-12 | active |
| Sphinx-Needs | Typed requirement IDs, links, constraints (id_regex, back_links), needs.json; MyST Markdown; monorepo with sphinx-codelinks, sphinx-test-reports | MIT | 9.2.0, 2026-11-04 (PyPI) | 2026-11-13 | active |
| StrictDoc | UIDs, parent/child relations, trace matrix; Markdown input (experimental); `@relation(REQ-1)` markers in source | Apache-2.0 | 0.30.4, 2026-10-22 | 2026-11-14 | active |
| Doorstop | Item UIDs, links, "suspect" links after parent change, validation | LGPL-3.0 (LICENSE.md; PyPI classifier also lists Other/Proprietary) | 3.2, 2026-07-10 | 2026-11-04 | active |
| OpenFastTrace | `req~id~1` spec items in Markdown; coverage tags in code incl. `.py`; Outdated/Orphaned/Predated link statuses | GPL-3.0 | 4.11.0, ~2026-10-18 (Maven) | 2026-10-18 | active |
| proselint | Generic prose issues | BSD-3-style | 0.16.0, 2025-11-14 | 2026-06-22 | slow |
| write-good | Passive voice, weasel words | MIT | 1.0.8, 2021-02-16 | 2025-03-10 (README) | dormant |
| alex | Insensitive wording (not precision) | MIT | 11.0.1, 2023-08-18 | 2024-11-27 | dormant |
| Paska (SNTSVV) | Requirement smells + rewrites (Rimay CNL) | GPL-3.0 | none (jar in repo) | 2024-02-05 | prototype |
| NALABS | Smells in requirements/test specs (vagueness, optionality, weak words) | MIT | UNVERIFIED | 2025-06-18 | prototype |
| Smella | Requirement smells | no public source found | UNVERIFIED | UNVERIFIED | unavailable |
| pytest-requirements | pytest markers linking tests to requirement IDs | BSD-3-Clause | 0.3.1, 2026-08-25 | UNVERIFIED (GitLab) | small/slow |
| pytest-reqcov | Requirement coverage in pytest | MIT | 0.2.0, 2025-07-04 | UNVERIFIED | small/slow |
| markdown-link-check | Broken links; same-file anchors (from source, undocumented) | ISC | 3.15.0, 2026-07-28 | 2026-10-22 | active |
| remark-validate-links | Offline local file + heading checks across files | MIT | 13.1.0, 2025-02-21 | 2025-02-21 | slow (stable) |
| MkDocs `--strict` + `validation.anchors` | Broken links/anchors as build failures | BSD-2-style | 1.6.1, 2024-08-30 | 2025-10-20 | slow |
| PR-Agent (The-PR-Agent/pr-agent, ex qodo-ai) | LLM PR review/describe/improve; Action | MIT (LICENSE, 2026); earlier versions differed (Apache-2.0 on PyPI 0.2.4; AGPL period UNVERIFIED) | 0.50.0, 2026-11-08 | 2026-11-14 | active, community-maintained |

## Notes
- `pytest-req` on PyPI is unrelated (a requests plugin). `pytest-traceability` and `paska` are not on PyPI.
- Smell detectors: all open ones are research prototypes; Paska needs Java 8 and Rimay-style financial requirements.
- Custom `@pytest.mark.req("ID")` + JUnit XML into OFT or sphinx-test-reports is a common pattern (inference, untested here).
- lychee GitHub release/Action may be newer than crates.io (UNVERIFIED).
- PR-Agent needs an own LLM key, is non-deterministic, and does not check against the team's spec.

Sources: https://github.com/SNTSVV/Paska, https://arxiv.org/abs/2305.07097, https://github.com/eduardenoiu/NALABS, https://arxiv.org/abs/2202.05641
