# research

Deep-research results from Claude Code cloud sessions. `main` holds only the setup;
each run lives on its own `research/<kebab-title>` branch, with no PR. `CLAUDE.md` is
the brief sessions read; this file is for you.

## Starting a run

1. Start a cloud session on this repo.
2. Paste or upload the brief and invoke `/deep-research`.
3. The session runs a network preflight, creates the branch, then pushes notes and the
   report.

## Network
- Network access is set in the environment's Network access setting.
  `.claude/settings.json` only pre-approves tools, so you get fewer prompts.
- `200 Connection Established` followed by a 403 (often `server: cloudflare`) means the
  site blocked the request. No setting fixes it.
- Publisher sites behind their own blocks include ACM, ScienceDirect, IEEE Xplore,
  ResearchGate, DTIC, nowpublishers and OpenReview PDFs. Get those papers from outside
  and add them to the brief.

## Evidence
- Search extracts are leads, not evidence; claims based on them often have the wrong
  figures, scope or attribution. Either confirm full-text access with the preflight, or
  plan a verification pass.

## Workflow
- Expect one commit per research track: the container is ephemeral, and the stop hook
  asks for commits.
- A follow-up run gets a new title, so the old and new reports can be diffed.
