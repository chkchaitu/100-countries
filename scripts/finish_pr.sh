#!/usr/bin/env bash
# Usage: scripts/finish_pr.sh "<PR title>" <body-file> [--no-merge]
# Validates data, branches, commits, opens a PR, waits for the check, merges. Exits non-zero on any failure.
set -euo pipefail
cd ~/build/100-countries-site
[ -n "$(git status --porcelain data)" ] || { echo "FAIL: no data changes to submit"; exit 2; }
python3 scripts/check_data.py
B="research/$(date +%F-%H%M)"
git checkout -q -b "$B"; git add data; git commit -q -m "$1"; git push -q -u origin "$B"
URL=$(gh pr create --title "$1" --body-file "$2" --base main --head "$B")
echo "PR: $URL"
[ "${3:-}" = "--no-merge" ] && { git checkout -q main; echo "left open for review"; exit 0; }
sleep 20
for i in $(seq 1 20); do
  S=$(gh pr checks "$URL" --json state --jq '.[].state' 2>/dev/null | sort -u | tr '\n' ' ')
  echo "checks: $S"
  case "$S" in *FAILURE*|*ERROR*) echo "FAIL: check failed"; git checkout -q main; exit 3;; esac
  case "$S" in "SUCCESS ") break;; esac
  sleep 15
done
gh pr merge "$URL" --squash --delete-branch
git checkout -q main; git pull -q
echo "MERGED: $URL"
