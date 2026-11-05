# Running the audit loop (instructions for the Claude Code session)

This repository is driven by a Claude Code session: the session is the orchestrator, background subagents do the audits, and the `audit-loop` CLI keeps state and measures spend. When the user asks to run the audit loop, follow this procedure.

## Setup (once)

1. `uv sync`
2. Copy `.env.example` to `.env`, then set `AUDIT_BUDGET_USD` and, if commits need trailers, `AUDIT_COMMIT_TRAILER`.
3. Write `repos.txt` (format: `repos.example.txt`).
4. `uv run audit-loop spend` should print a total. If it says there is no session id, pass `--session <id>`. The transcript is `~/.claude/projects/<project>/<id>.jsonl`.

## Loop

1. **Budget gate.** `uv run audit-loop spend --check` exits 3 once the session total reaches `AUDIT_BUDGET_USD - AUDIT_STOP_MARGIN_USD`, or once `AUDIT_STOP_AT` has passed. From then on, launch nothing new.
2. **Pick.** `uv run audit-loop next -n <free slots>`. It prints `owner/name round` lines. Run about 4 audits at a time.
3. **Launch each pick:**
   1. **Cloud sessions only.** Make sure the session can push to the repository: call the `add_repo` tool with `access: "push"`, once per repository.
   2. `uv run audit-loop clone <owner/name> --round <r>` shallow-clones into `workdir/` and checks out `<prefix>/<date>-r<r>`.
   3. `uv run audit-loop record <owner/name> --round <r> --status started`
   4. Spawn a **background `general-purpose` subagent**.
      - Its description must be exactly `audit <name> r<r>`. Spend attribution matches on it.
      - Write the prompt to a file, `uv run audit-loop prompt <owner/name> --round <r> --cap <usd> > workdir/prompts/<name>-r<r>.md`. Give the subagent only a one-line prompt: "Your complete instructions are in `<absolute path>`; read that file first and follow it exactly." This keeps the orchestrator's context small.
      - Cap by size of the claim surface (tracked md/tex/html files plus result files):
        - under 30 files: $3
        - under 120 files: $5
        - otherwise: $8
4. **When an audit finishes:**
   1. **Verify before landing:** `scripts/land_check.sh <owner/name> <r>` runs the checks below, commits and pushes the report, and prints the PR body.
      - `git -C workdir/<name> log --oneline origin/HEAD..HEAD` and `git -C workdir/<name> diff --stat origin/HEAD...HEAD`
      - Spot-check a few hunks.
      - Look closer if result/data files changed or there are large deletions. Prose should change to match data, never the reverse.
   2. **If the branch was pushed:** open a PR with the body from `uv run audit-loop pr-body <owner/name> --round <r>`, then merge it with a merge commit. If the user wants to review first, leave it open.
   3. `uv run audit-loop record <owner/name> --round <r> --status merged|no_changes|unmerged|failed --pr <url>`. The audit's cost is filled in automatically from its subagent transcript.
   4. `uv run audit-loop report`. Commit `reports/` and push.
5. Repeat. Once every repository has finished round 1, `next` starts round 2. Audits are independent: never pass earlier findings to a new audit.
6. **After the stop line:** wait for running audits, land them, regenerate the report, and finish.

## Rules

- Keep the orchestrator's context small. Subagents put details in `reports/audits/<name>/round-<r>.md` and return at most 200 words.
- Don't merge a branch you haven't looked at.
- Don't push credentials. `.env`, `repos.txt` and `workdir/` are gitignored.
- Code changes in this repository: `uv run pytest -q` must pass.
