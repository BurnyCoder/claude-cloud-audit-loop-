---
repo: BurnyCoder/deep-work-jarvis-waifu-supervisor
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 64
fixed: 10
unverifiable: 18
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/deep-work-jarvis-waifu-supervisor, round 1

## Summary

This repository is a Windows focus-enforcement app. It has no trained models, no
result tables and no Hugging Face card. Its claim surfaces are README.md, AGENTS.md,
CLAUDE.md, docs/, two reports (with PDFs), the dashboard UI, `.env.example` and code
comments. I checked the README claims a reader sees first against the code, and the
external claims against the primary sources fetched on 2026-11-05: the OpenAI model,
vision, TTS, data-control and deprecation pages, plus the uv, Git, python-dotenv,
Flask, Microsoft, Claude Code and psutil docs. Then I swept all 186 unique URLs for
HTTP status and 79 URL fragments for anchor existence. The README turned out to be
accurate against the code: the table defaults, 960 px tiles, JPEG quality 80, the
1-240 minute goal access, the 3 s poll after completion, the 14 ordered groups, the
loopback host, the 30 s readiness deadline, the window minimum of 2, the five recent
observations, the temporary WAV deleted only after playback, the fence markers and
the absence of `store=False`. I found three problems in what the repository states
and fixed them in two commits. Because the budget cap was reached, the lower-priority
pages (docs/user-guide.md, docs/architecture.md, docs/startup.md,
docs/verdict-corrections.md, and the earlier fact-check report) were only spot-checked.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| README.md:239 | `TTS_MODEL` purpose "OpenAI speech model" (no deprecation notice) | adds "OpenAI lists it for removal on January 6, 2027" with link | https://developers.openai.com/api/docs/deprecations (2026-10-01 entry: gpt-4o-mini-tts, both snapshots, shutdown Jan 6, 2027, replacement gpt-realtime-2.1-mini) |
| .env.example:31-32 | no deprecation note on `TTS_MODEL` | adds the deprecation date and source | same as above |
| deepwork/config.py:100-101 | no deprecation note on the `tts_model` default | adds the deprecation date and source | same as above |
| .env.example:9 | "uses cost-sensitive GPT-6 Luna" | quotes OpenAI's description, "most efficient model for focused, high-volume tasks" | https://developers.openai.com/api/docs/models/gpt-6-luna |
| deepwork/config.py:86-88 | "the cost-sensitive GPT-6 Luna tier at medium, OpenAI's documented default" | OpenAI's own description, plus medium named as the documented default reasoning effort | https://developers.openai.com/api/docs/models/gpt-6-luna ("`medium` (default)") |
| deepwork/blocking/app_killer.py:6 | https://psutil.readthedocs.io/en/latest/ (now redirects to the psutil.io home page) | https://psutil.io/7.2/ (the docs for psutil 7.2.2, the version in uv.lock) | uv.lock `psutil 7.2.2`; https://psutil.io/7.2/ |
| deepwork/blocking/app_killer.py:26 | `.../en/latest/#psutil.process_iter` (dead anchor) | `https://psutil.io/7.2/#psutil.process_iter` | the 7.2 docs describe the `proc.info` attribute the code uses; the latest psutil.io/api/ describes `Process.snapshot` instead |
| deepwork/blocking/app_killer.py:37 | `.../en/latest/#psutil.NoSuchProcess` (dead anchor) | `https://psutil.io/7.2/#psutil.NoSuchProcess` | https://psutil.io/7.2/ |
| tests/test_app_killer.py:3 | dead psutil `process_iter` anchor | psutil 7.2 anchor | https://psutil.io/7.2/ |
| tests/test_app_killer.py:42 | dead psutil `NoSuchProcess` anchor | psutil 7.2 anchor | https://psutil.io/7.2/ |

Claims verified and left unchanged include:
- **GPT-6 Luna:** image input, structured outputs, text-only output, and `medium` (the default) and `xhigh` reasoning.
- **Image sizing:** GPT-6 Luna is absent from the image-sizing table that lists `original` detail support, which the repository already discloses.
- **TTS:** 13 built-in voices including `coral`, and the AI-voice disclosure requirement.
- **OpenAI data controls:** no training use unless the organization opts in; abuse-monitoring logs kept up to 30 days; Responses application state kept at least 30 days by default or with `store=true`.
- **Install and runtime:** the winget IDs `Git.Git` and `astral-sh.uv`; python-dotenv's quoted and unquoted values and its non-override default; Flask's default `127.0.0.1:5000`; Microsoft's HostsFileHijack detection, which can reset the hosts file.
- **GPT-6 Luna report:** the a78a575 baseline had the `gpt-5.6-luna` defaults, the migration diff changes no dependency, openai is 2.44.0 in uv.lock, and the commit date is 13 Oct 2026.
- **verification.md snippet:** the symbol names it uses exist in the code.

## Unverifiable or hedged claims

- **reports/2026-10-13-gpt-6-luna.md test figures:** 44 focused tests in 8.27 s and 251 full-suite tests in 5.98 s. The logs they come from are untracked. The current suite has 277 tests, which all pass.
- **Same report, live results:** the smoke verdict fields, the 960x1896 composites, the speech timings of about 114 s and 0.65 s, and five persisted `completed` exchanges. All of this lives in untracked `logs/` and `results/`. It is a single uncontrolled run, and the report already says so.
- **GPT-6 Luna and `detail="original"`:** OpenAI's vision guide does not list `gpt-6-luna` among the models that support `original` detail. The only evidence that the default works is that one live migration run. The repository already hedges this (README, verification.md step 5).
- **GitHub-hosted sources:** openai-python `#retries`/`#usage` (3 links), werkzeug `serving.py@3.1.8`, opencv issue 17687 and the python-mss repo. GitHub API access to third-party repositories is not enabled in this session.
- **Bot-blocked sources (HTTP 403 via the proxy):** 3 docs.opencv.org pages and 2 Stack Overflow questions.
- **help.openai.com/en/articles/9039756** (ChatGPT vs API billing) returned 403. Web-search snippets of the article support "managed separately", but I could not read the article itself.

## Problems found but not fixed

- **CLAUDE.md:9** links `https://code.claude.com/docs/en/memory#agentsmd`, but that page's anchor is now `#agents-md`. The `@AGENTS.md` pattern itself, with its Windows advice, is under `#share-one-file-with-other-coding-tools`. The page also now says Claude Code v2.1.277+ reads AGENTS.md directly, and that the import can stay. I did not edit it because CLAUDE.md is the agent-instruction file this session loads. A maintainer should change the anchor.
- **reports/2026-10-22-independent-fact-check.md:84** also links the dead `psutil.readthedocs.io/en/latest/#psutil.Process.kill` anchor. I left it alone because the file is an earlier audit record and its PDF would need re-rendering. The working target is `https://psutil.io/7.2/#psutil.Process.kill`.

## Hugging Face card

None. No Hugging Face model, dataset or Space is linked from any tracked file.

## Regenerated artifacts and tests

- No report Markdown changed, so the PDFs (`scripts/render_report.py`) were not regenerated.
- `uv run --locked pytest -q` passed 277 of 277 tests after the edits.
- No JS or UI file changed, so the Node dashboard tests were not run.
