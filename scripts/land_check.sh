#!/usr/bin/env bash
# Pre-merge check for one finished audit, run from the repository root:
#   scripts/land_check.sh <owner/name> <round>
# 1. confirms the audit branch on GitHub is the clone's HEAD (the agent pushed everything);
# 2. prints commits, diff stat, changed data/result files and the largest deletions to review;
# 3. commits and pushes this audit's report (so the PR body's link works) and prints the PR body.
set -euo pipefail
slug=$1 round=$2 name=${slug#*/}
clone=workdir/$name
branch=$(git -C "$clone" rev-parse --abbrev-ref HEAD)
default=$(git -C "$clone" symbolic-ref --short refs/remotes/origin/HEAD)
remote_sha=$(git -C "$clone" ls-remote origin "refs/heads/$branch" | cut -f1)
echo "branch $branch | local $(git -C "$clone" rev-parse --short HEAD) | remote ${remote_sha:0:7} | base $default"
[[ -n $remote_sha ]] || { echo "NOT PUSHED"; exit 1; }
[[ $remote_sha == $(git -C "$clone" rev-parse HEAD) ]] || echo "WARNING: remote differs from local HEAD"
git -C "$clone" log --oneline "$default..HEAD" | cat
git -C "$clone" diff --stat "$default...HEAD" | tail -1
echo "--- data/result-like files changed:"
git -C "$clone" diff --name-only "$default...HEAD" | grep -iE '\.(json|csv|jsonl|npy|npz|pt|pkl|parquet)$|(^|/)(results?|data|runs|logs)/' || echo "(none)"
echo "--- files with most deletions:"
git -C "$clone" diff --numstat "$default...HEAD" | sort -k2 -nr | head -3
report=reports/audits/$name/round-$round.md
[[ -f $report ]] || { echo "NO REPORT at $report"; exit 1; }
git add "$report" && git commit -q -m "Add round-$round audit report for $name" -m "${AUDIT_COMMIT_TRAILER_TEXT:-}" || true
git push -q origin HEAD 2>&1 | tail -1
echo "--- PR body:"
uv run audit-loop pr-body "$slug" --round "$round"
