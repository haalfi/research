# research

Deep-research results produced by Claude Code cloud sessions. `main` holds only the
setup. Each research run lives on its own `research/<kebab-title>` branch, with no PR.
`CLAUDE.md` is the brief that sessions read; this file is for you.

## Starting a run

1. Start a cloud session on this repo (it checks out `main`).
2. Paste or upload the brief and invoke `/deep-research`.
3. The session runs the network preflight, creates `research/<kebab-title>`, and pushes
   notes per track and then the report.

## Learnings

### Network
- **The lever is the environment's Network access setting, not `settings.json`.**
  A run at 23:07 failed with proxy 403s even though `settings.json` was already on
  `main`. A run two minutes later in the same environment got through.
  (Inference from timing: the network setting had changed in between.)
- `settings.json` only pre-approves tools, so you get fewer permission prompts. Auto
  mode barely needs it.
- **Proxy 403 vs. site 403:** if curl shows `200 Connection Established` and then 403
  (often `server: cloudflare`), the site blocked the request, not your policy. Changing
  settings cannot fix that.
- Sites blocked by their own walls, as of 2026-10: dl.acm.org, cacm/queue.acm.org,
  sciencedirect.com, IEEE Xplore, ResearchGate, apps.dtic.mil, nowpublishers.com, and
  OpenReview PDFs. Get those papers from outside (library copy, author) and add them to
  the brief.
- Some university sites fail TLS because the trust store here does not accept their
  certificate root (e.g. cs.ucf.edu, whose chain ends at an emSign root).
- github.com pages fail via curl. raw.githubusercontent.com and `git clone` work.

### Evidence quality
- **Search extracts are not evidence.** The first run had no full texts. A later
  verification pass checked 170 of its claims against full texts and corrected or
  refuted about a quarter of them: 41 corrected, 5 refuted, 7 not found in their
  sources. Typical errors:
  - a union of models reported as a single-model score;
  - a paraphrase shown as a quote;
  - a credit given to the wrong system;
  - a small subset (n = 9) presented as a general finding.
- So either confirm full-text access with the preflight before starting, or plan a
  verification pass. The verification brief used is on
  `research/black-box-boundary-spec`, in `briefs/verification-pass-input.md`.

### Workflow
- The container is ephemeral, and a user-level stop hook demands a commit whenever
  files are untracked. Expect one interim commit per research track; that is fine.
- Agents sometimes drop downloads into the repo root (once a `p.html`). The brief tells
  sessions to check `git status` before committing.
- Follow-ups get a new title, so the old and new report can be diffed.
- Sessions can message each other, e.g. to tell a waiting session that new results are
  pushed. They find each other through the session list.

### Bringing setup changes to `main`
Setup branches such as `claude/minimal-main` sit directly on top of `main`, so a
fast-forward is enough: `git checkout main && git merge --ff-only claude/minimal-main`,
then push.
