# research

Holds deep-research results only. No code.

## Delivery
- Each request gets a fresh branch from `origin/main`: `research/<kebab-title>`.
  Never commit to `main`, never open a PR.
- Commit and push early and often. The container is ephemeral; commit notes after each track.
- Layout:
  - `briefs/`: the input brief, exactly as given
  - `research_notes/<Title>/`: one notes file per track
  - `reports/<Title>.md`: the final report
- A follow-up or verification run gets a new title (e.g. `<Title> verified`).
  Never edit an earlier report or its notes, so the two can be diffed.
- Commit messages: no model names.

## Running
- Use the `deep-research` skill.
- Preflight: `curl -sS -o /dev/null -w "%{http_code}\n" https://arxiv.org/abs/2509.22908`.
  If it isn't 200, stop and name the blocked hosts. The fix is the environment's Network access setting, not settings.json.
- A 403 after `200 Connection Established`, often with `server: cloudflare`, comes from the site, not the network policy.
  Try an author PDF, arXiv or an institutional repository instead.
- Verdicts rest on full texts. Search extracts are leads only.
  Label unreachable sources as unreachable and inference as inference.
- github.com pages fail via curl: use raw.githubusercontent.com or `git clone`.
- Downloads go to the scratchpad, never the repo. Run Python on them with `python3 -I`.
  Check `git status` for stray files before each commit.
