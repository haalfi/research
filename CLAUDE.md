# research

Holds deep-research results only. No code besides `.claude/`.

## Delivery
- Each research topic gets one branch from origin/main: research/<kebab-topic>.
  Follow-ups on the same topic stay on that branch; only a new topic gets a new branch.
  Name the branch after the topic, never the run.  Never commit to main, never open a PR.
- A follow-up or verification run gets a new title (e.g. `<Title> verified`) on the topic's branch.
  Never edit an earlier report or its notes, so the two can be diffed.
- Read only `main` and your own branch. Never fetch, check out, diff or read files from any
  other branch (git or GitHub tools) unless the user explicitly names that branch and allows it.
  Only then add it to `.git/claude-allowed-branches`; the branch-guard hook enforces this.
- Commit and push early and often. The container is ephemeral; commit notes after each track.
- Layout:
  - `briefs/<Title>.md`: the input brief, exactly as given
  - `research_notes/<Title>/`: one notes file per track
  - `reports/<Title>.md`: the final report
- Commit messages: no model names.

## Running
- Use the `deep-research` skill.
- The startup hook reports a network preflight. If it says FAILED, stop and name the blocked hosts.
- A 403 after `200 Connection Established`, often with `server: cloudflare`, comes from the site, not the network policy.
  Try an author PDF, arXiv or an institutional repository instead.
- Verdicts rest on full texts. Search extracts are leads only.
  Label unreachable sources as unreachable and inference as inference.
- github.com pages fail via curl: use raw.githubusercontent.com or `git clone`.
- Downloads go to the scratchpad, never the repo. Run Python on them with `python3 -I`.
  Check `git status` for stray files before each commit.
