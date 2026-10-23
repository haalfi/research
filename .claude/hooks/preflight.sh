#!/usr/bin/env bash
# SessionStart: network preflight + branch reminder. Output goes into the session context.
# 000 = no HTTP response (proxy/policy denial, DNS, TLS); 403 after a tunnel = site block.
failed=()
for url in https://arxiv.org/abs/2509.22908 https://docs.python.org/3/ https://raw.githubusercontent.com/python/cpython/main/README.rst; do
  code=$(curl -sS -m 15 -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
  [ "$code" = "200" ] || failed+=("${url#https://} -> ${code:-000}")
done
branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ ${#failed[@]} -eq 0 ]; then
  echo "Preflight OK: arxiv.org, docs.python.org and raw.githubusercontent.com return 200."
else
  echo "Preflight FAILED: ${failed[*]}. Stop before research and report these hosts;"
  echo "000 = no HTTP response: the proxy blocked it (fix: the environment's Network access setting)."
  echo "An HTTP code such as 403 = the site itself refused."
fi
echo "Current branch: ${branch:-unknown}. Deliver on a fresh research/<kebab-title> branch from origin/main; no PR."
exit 0
