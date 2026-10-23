#!/usr/bin/env bash
# SessionStart: network preflight + branch reminder. Output goes into the session context.
code=$(curl -sS -m 15 -o /dev/null -w "%{http_code}" https://arxiv.org/abs/2509.22908 2>&1)
branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ "$code" = "200" ]; then
  echo "Preflight OK: arxiv.org returned 200; full texts are reachable."
else
  echo "Preflight FAILED: arxiv.org returned '$code'. Stop before research and report the blocked hosts;"
  echo "the fix is the environment's Network access setting."
fi
echo "Current branch: ${branch:-unknown}. Deliver on a fresh research/<kebab-title> branch from origin/main; no PR."
exit 0
