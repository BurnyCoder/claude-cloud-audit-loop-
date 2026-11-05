---
repo: BurnyCoder/security-monitoring-agent
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 96
fixed: 2
unverifiable: 72
not_fixed: 1
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/security-monitoring-agent, round 1

## Summary

This repository is a local Windows/WSL vulnerability-monitoring app (FastAPI, Codex/Claude Code CLIs, OSV-Scanner, CISA KEV). It has no ML training, paper, or Hugging Face card. The claim surfaces are README.md, AGENTS.md, docs/ (architecture, coverage, setup), reports/ (00 to 05, validation-summary.md and the PDF built from it), the CI workflow, and code docstrings and comments.

I checked 96 claims against evidence. The documentation is accurate overall. I found two factual errors and fixed both. Many numbers in the live-run reports come from private local logs and SQLite files that are not in Git, so I could not check them. Where I could, I checked those numbers for internal consistency, and they were consistent.

What I verified:
- **Defaults and ranges** match `models.py` and `config.py`: model `gpt-6-luna`, interval 60 (range 1 to 10,080), timeout 1,800 (range 30 to 14,400), news window 1/7/30 with default 7, `.env` precedence, and the default project root.
- **Elapsed times.** All five durations, recomputed from the start and finish timestamps, match: 965.773, 19.945, 8.418, 266.940 and 10.362 s.
- **Finding counts** add up: Luna 15 findings minus 1 rejected gives 14 (4/4/6); Haiku 2/4/3/1 becomes 0/6/3/1.
- **Tests.** pytest collects exactly 117 tests. The 6 frontend modules parse and link. The two scheduler-loop cases exist, as parametrized cases. The 100,000-character SSE and storage tests, the OSV exit-code tests (0/1/127/128) and the WSL NUL-padding test all exist.
- **CI and history.** CI succeeded on 0afd91e. PRs #1 and #2 were merged. There are seven live transcripts in total (1+2+2+1+1).
- **Dependency counts.** The 33 and 47 project dependencies match the `[[package]]` counts in `uv.lock` before and after commit aa99773.
- **Primary sources** confirm every quoted detail:
  - CVE-2026-57968/57973/96206 Microsoft CNA bounds (5.0.0.0 with <2.7.8, <2.7.10 and <3.0.1, in both affected and CPE fields).
  - CISA KEV: 1,754 entries added on or before 2026-10-21.
  - USN-8951-1 (c-ares).
  - ImageMagick GHSA-x8g2-7r3w-h44p (low severity, Windows symlink TOCTOU, patched 7.1.2-30/6.9.13-55).
  - GHSL-2026-140 (PoC generator, affected through 26.00, fixed in 26.01).
  - Starlette GHSA-86qp-5c8j-p5mr / CVE-2026-48710 (fixed in 1.0.1; the lockfile has 1.9.0).
  - Chrome 156 promoted to stable on 2026-10-20.
- **CLI and library docs** confirm:
  - Every Codex flag and Claude flag the app uses.
  - `--bare` does not read OAuth credentials.
  - Claude runs commands unsandboxed on native Windows.
  - The Codex installer URL and the winget IDs.
  - OSV-Scanner flags and return codes.
  - Get-HotFix uses Win32_QuickFixEngineering.
  - Win32_Product queries trigger consistency checks and repairs.
  - FastAPI documents `EventSourceResponse` and `Last-Event-ID`.
  - The pinned action SHAs match their tags.
- **Code behaviour** matches architecture.md and coverage.md: 5 s scheduler poll, 1 s cancel watcher, HTTP 409 on collisions, 200-event pages, taskkill /T /F, IgnoreNew with Interactive/Limited tasks, HKCU Lxss, 32-bit uninstall scopes, the dpkg-query format, an 8 s CVE fetch timeout with a per-scan cache, the downgrade rules, a 24 h overlap, the checkpoint rules, OSV timeout = min(timeout, 300), WAL, and exit code 2.
- **Links.** I fetched all 98 external URLs. They resolve, or are reachable through WebFetch or the API. Two Codex doc URLs redirect to learn.chatgpt.com but still serve the right page.

## Fixes

| file:line | before | after | evidence |
| --- | --- | --- | --- |
| reports/01-live-validation.md:9 | "The requested models were `gpt-6-luna` for the scan and `haiku` for the conversation." | "...`gpt-6-luna` for the scan and the separate Codex conversation, and `haiku` for the Claude Code conversation." | Same report: line 5 and the Codex conversation table at lines 64-67 (requested model `gpt-6-luna`) |
| .github/workflows/tests.yml:21 | `version: "0.13.5" # Version published in the current official integration guide.` | `version: "0.13.5" # Pinned uv release; the official integration guide shows its current example version.` | https://docs.astral.sh/uv/guides/integration/github/ now shows `version: "0.13.7"` |

## Unverifiable or hedged claims

There are 72 such claims. All are values read from ignored local evidence (`logs/`, `data/monitor.sqlite3`) or from local machine observations:
- **Run IDs, models and statuses:** run IDs, models reported by the CLI, persisted statuses.
- **Transcript measurements:** JSONL byte sizes and event counts, prompt and answer character counts, the 820,056-character event.
- **Live-run output counts:** web-tool ID counts (23; 9 + 3), advisory, finding and coverage-note counts in the raw outputs.
- **Event times:** correction times (19:42:09, 19:43:50, 19:51:16, 20:05:49, 20:18:14).
- **Local environment and early test runs:** Python 3.14.2, Node 24.13.0, the earlier test runs (88 in 8.46 s and 8.72 s, 56 and 66), the 10.67 s duration.
- **Browser observations:** the viewport and browser checks.

The KEV catalog version `2026.10.21` is consistent with today's feed, but the snapshot itself is not archived.

One oddity I could not resolve: the Luna scan and the Haiku scan both report a 3,146-character application prompt. That is possible with the shared template, but I could not confirm it.

## Problems found but not fixed

- `tests/test_process.py::test_cancel_stops_owned_parent_and_child` fails on Linux: 116 passed, 1 failed. CI runs only on Windows, the app targets native Windows, and no document claims the tests pass on POSIX. architecture.md says only that POSIX "uses a new process group", which is true (`start_new_session=True`). I left it unchanged because a fix needs a POSIX process-tree kill and a re-test.
- Minor, not counted: reference [9] in validation-summary.md is listed but never cited in the prose. It is a valid repository link.

## Hugging Face card

n/a. The repository links no Hugging Face model, dataset or Space. reports/README.md states there are no Hugging Face uploads.

## Regenerated artifacts and tests

- I did not regenerate the PDF because its source, `reports/validation-summary.md`, was not edited. The text in the committed PDF already matches the source on all key numbers.
- No Python or JS code was changed; the only workflow edit is a YAML comment.
- Baseline checks on Linux: `uv run --locked pytest -q` gave 116 passed and 1 failed (the Windows-specific process test above). `node --experimental-vm-modules scripts/check_frontend.mjs` passed: 6 modules parsed and linked.
