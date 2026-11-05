---
repo: BurnyCoder/security-monitoring-agent
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 91
fixed: 2
unverifiable: 12
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/security-monitoring-agent, round 2
## Summary
Independent check of README.md, AGENTS.md, docs/ (setup, architecture, coverage), reports/ (00-05, README, validation-summary.md and its PDF), CI workflow comments, UI strings (template and static JS), and fact-stating code docstrings. The repository is a local software tool, not an ML project: it has no training runs, model weights, paper or Hugging Face artifacts.

91 claims were compared with evidence. Most were method/default claims checked against code (`models.py` Settings bounds and defaults, `pipeline.py`, `service.py`, `process.py`, `storage.py`, `scheduling.py`, `dependencies.py`, `kev.py`, `wsl_primary.py`, `commands.py`, `cli.py`, `windows.ps1`, `wsl.py`). The rest were external claims checked against primary sources fetched now: Codex docs (learn.chatgpt.com CLI reference, non-interactive mode, Windows deployment), Claude Code docs (setup, cli-reference, headless, sandboxing), OSV-Scanner docs (installation, output exit codes, usage, scan-source, supported lockfiles), Microsoft Learn (Get-HotFix/Win32_QuickFixEngineering, software-installation guidance, release cycle), the dpkg-query man page, FastAPI SSE docs, the uv docs, the CVE records CVE-2026-57968/57973/96206 (lower and upper bounds in the `affected` and `cpeApplicability` fields), USN-8951-1, GHSL-2026-140 (PoC generator), the ImageMagick GHSA-x8g2-7r3w-h44p advisory (low severity, Windows symlink TOCTOU), Starlette GHSA-86qp-5c8j-p5mr via OSV (CVE-2026-48710, fixed in 1.0.1), and the Chrome 156 stable post (October 20, 2026). Report arithmetic was recomputed from the reports' own timestamps and counts: five elapsed times, Luna 4+4+7=15 becoming 14, the Haiku 2/4/3/1 to 0/6/3/1 table, and 47 dependencies, which matches the 47 packages in uv.lock. The suite collects 117 tests. The frontend check parses 6 modules. CI for 0afd91e (PR #1 merge) succeeded. The three pinned action SHAs match their tags. Separately, 88 cited URLs were fetched: all resolve except 7 github.com web pages (blocked by the proxy with 403, so they were checked through git ls-remote, OSV or WebFetch instead) and uvicorn.org (proxy 502).

Almost everything checked was correct. Two claims were fixed.

## Fixes
| file:line | before | after | evidence: result file path or URL |
| --- | --- | --- | --- |
| reports/validation-summary.md:59 (and regenerated reports/validation-report.pdf) | "Clone the public repository, follow its setup guide" (reference [9] was listed but never cited) | "Clone the public repository [9], follow its setup guide" | reports/validation-summary.md reference list; https://github.com/BurnyCoder/security-monitoring-agent |
| .github/workflows/tests.yml:23 | `version: "0.13.5" # Pinned uv release; the official integration guide shows its current example version.` | `... # Pinned uv release; the official integration guide recommends pinning a specific uv version.` | https://docs.astral.sh/uv/guides/integration/github/ (example now shows `version: "0.13.7"` and says "It is considered best practice to pin to a specific uv version") |

## Unverifiable or hedged claims
These come only from the author's ignored local `data/` and `logs/` evidence, so no repository file or public source can confirm them. They are already presented as local observations and were left as they are:
- Run IDs, JSONL event counts, byte sizes, prompt/answer character counts (reports 01, 02).
- 23 distinct Codex web-tool IDs; 9 WebSearch / 3 WebFetch Haiku tool IDs; 12/8 advisory counts; 14 coverage notes.
- KEV catalog version `2026.10.21` with 1,754 entries (the current feed has moved on).
- Luna run's 33 recorded dependencies (no repository artifact; the 47 Haiku-run count does match the current uv.lock).
- That the OSV-derived WSL range used a broader lower bound than Microsoft's CNA range.
- Historical suite timings (88 passed in 8.46 s / 8.72 s; 117 in 10.67 s). The 117 count matches today's collection.
- Browser observations in report 03 (viewports, copy acknowledgement, filters, restart).
- Model reported as `claude-haiku-5-5` and Codex `actual_model: null`.
- Timestamps of the manual corrections (19:42:09, 19:43:50, 19:51:16, 20:05:49, 20:18:14 UTC).
- The temporary Windows task registration and removal.
- Python 3.14.2 / Node 24.13.0 environment of the original validation.
- The authorship/date lines of the reports.

## Problems found but not fixed
- None that are claim errors. Observation: on this Linux container `tests/test_process.py::test_cancel_stops_owned_parent_and_child` fails (116/117 pass). The supported platform and CI are Windows, and the docs only say POSIX uses a new process group, which `process.py` does (`start_new_session=True`). The failure is most likely caused by unreaped zombie processes in the container. It does not contradict any documented claim.
- `developers.openai.com/codex/...` links in `docs/architecture.md` and the `commands.py` docstring now redirect to learn.chatgpt.com equivalents. They still resolve to the right content, so they were left unchanged.

## Hugging Face card
n/a. The repository links no Hugging Face model, dataset or Space, and reports/README.md states there are no Hugging Face uploads.

## Regenerated artifacts and tests
- `reports/validation-report.pdf` was regenerated with `uv run --group docs python scripts/build_report.py` (ReportLab, CPU). A PyMuPDF text diff against the previous PDF shows the only change is the added `[9]`, so the PDF was already in sync with its Markdown source. It is still 3 pages.
- Tests: `uv run --locked pytest -q` gives 116 passed and 1 failed (the Linux-only process-tree test above, run before any edits; no Python code was changed). `node --experimental-vm-modules scripts/check_frontend.mjs` parsed and linked all 6 modules.
