---
repo: BurnyCoder/auto-eureka-scientist-agent-harness
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 150
fixed: 6
unverifiable: 7
not_fixed: 3
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/auto-eureka-scientist-agent-harness, round 1
## Summary

I checked the README, AGENTS.md, docs/, the authored and generated reports, the validation paper (Markdown, plus PDF text via pdftotext), the Pages site (site/), the UI templates and the factual code comments against the saved result files and primary sources. I found no wrong numbers. A script recomputed every value in the README execution table and the per-method accuracy table (n, mean, sample SD) from `reports/validation-data/*.json`, along with the primary effect, the CI and the decision for each trial. They all match. So do the 47-test count (`reports/offline-tests.xml`) and the 90-test and live-smoke rows (`reports/console-tests.xml`, `reports/console-acceptance.json`). The pdftotext output of the PDF contains the same numbers.

Rerunning `scripts/summarize_validation.py --no-pdf` against the committed data reproduced README.md, validation-summary.md, validation-paper.md, site/index.html, site/validation.json, the SVGs, settings.md and console-acceptance.md byte for byte. So the generated prose and tables are in sync with the data.

I also checked these method claims against the code and configs:
- the protocol: 64-128-10 ReLU MLP, AdamW, lr 0.001, batch 64, 50 epochs, weight decay 0.01, 0 and 0.001, seeds 0-2, split seed 42 with a 60/20/20 split (1078/359/360), bootstrap seed 2026 with 10,000 resamples, percentile CI
- the pilot-first gate and the reuse of the pilot checkpoint
- the default models, the CLI flags for both backends, the digits model allow-list and the dependency lists
- the policy hash (`prompts/full.txt` sha256 6a9addc3... equals `policy_sha256` in every run record)

The claim that regularization did not change accuracy holds exactly: the regularized, unregularized and sensitivity arms produce identical test predictions for each seed, while their final training losses differ, so weight decay was applied.

Of the 101 distinct external URLs, all non-GitHub ones resolve. For the cited papers, I checked titles, authors and years: Lones 2021 (arXiv:2108.02497) and Lipton & Steinhardt 2018 (arXiv:1807.03341). I also checked the Neel Nanda sequence and post titles, the Anthropic harness article, the license claims (UCI CC BY 4.0, Ralph Apache-2.0, ralphex MIT, Uvicorn BSD, FastAPI MIT, AI Scientist v2 custom, no license in autoresearch) and the Claude Code and Codex CLI flag documentation. Two kinds of link were broken, and I fixed both: moved documentation URLs, and relative links in the deployed Pages copy of the summary.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| docs/sources.md:3 | `https://psutil.readthedocs.io/en/latest/#process-class` (redirects to psutil.io landing page; anchor gone) | `https://psutil.readthedocs.io/stable/#process-class` | https://psutil.readthedocs.io/stable/ (contains `id="process-class"`) |
| src/auto_eureka_scientist/web/service.py:3 | same psutil `/en/latest/#process-class` link | `/stable/#process-class` | https://psutil.readthedocs.io/stable/ |
| src/auto_eureka_scientist/execution.py:4 | `https://psutil.readthedocs.io/en/latest/#kill-process-tree` (anchor gone after redirect) | `https://psutil.readthedocs.io/stable/#kill-process-tree` | https://psutil.readthedocs.io/stable/ (contains `id="kill-process-tree"`) |
| docs/sources.md:3 | `https://www.uvicorn.org/settings/` (502/timeout) | `https://uvicorn.dev/settings/` | Uvicorn pyproject `Homepage = "https://uvicorn.dev/"` (https://raw.githubusercontent.com/Kludex/uvicorn/main/pyproject.toml); page title "Settings - Uvicorn" |
| site/validation-summary.md:129 (via scripts/summarize_validation.py) | relative link `validation-extension-preregistration.md` (404 on https://burnycoder.github.io/auto-eureka-scientist-agent-harness/validation-extension-preregistration.md) | `https://github.com/BurnyCoder/auto-eureka-scientist-agent-harness/blob/main/reports/validation-extension-preregistration.md` | `.github/workflows/pages.yml` deploys only `site/`; live 404 confirmed |
| site/validation-summary.md:145 (via scripts/summarize_validation.py) | relative link `core-check-evidence-repair.md` (404 on Pages) | `https://github.com/BurnyCoder/auto-eureka-scientist-agent-harness/blob/main/reports/core-check-evidence-repair.md` | same |

## Unverifiable or hedged claims

These claims are left as written.
- The trial repositories (`BurnyCoder/eureka-digits-{haiku,luna,sonnet,sol}`) and the parent-review files cited in reports/validation-interpretation.md, reports/plan-audit.md and site/index.html could not be read: GitHub access to those repositories is not enabled for this session. The corrections they are said to record (Haiku detection limit, norms and NLL; Sonnet sampling noise and checklist) are unverified. Their GitHub Pages explorers do resolve (HTTP 200).
- "No AI Scientist v2 or unlicensed implementation code was copied" (README:128, docs/sources.md): this is a negative claim and cannot be checked from this repository.
- "Codex wrote this harness codebase and report" (paper AI statement): no evidence in the repository.
- The `--disable multi_agent` Codex feature name (README:76, adapters.py:47): the Codex docs document `--disable <feature>`, but not a `multi_agent` feature.
- "Pins background summarization" (README:72): the Claude Code docs say `ANTHROPIC_DEFAULT_HAIKU_MODEL` covers "background functionality". The WebFetch-summarization detail comes from the repository's own observation of the first Sonnet attempt, which the data does confirm: attempt 1 reported both claude-sonnet-5-5 and claude-haiku-5-5 and was rejected.
- The statements that the parent performed PDF and browser inspection are supported only by the repository's own receipts in reports/verification/. I did not re-run the inspections.
- The Luna exact-byte repair narrative was not independently re-derived.

## Problems found but not fixed

1. **The Haiku-original "Explorer" link goes to a PDF.** In reports/validation-summary.md:16, validation-paper.md and the site/index.html "Explore evidence" cell, the haiku-original link points to the historical `site/paper.pdf` in the trial repository, not to an explorer. The label comes from the shared report body that also feeds validation-paper.md. Changing it would leave validation-paper.md out of sync with validation-paper.pdf, which cannot be rebuilt here because LaTeX is not installed. Suggested fix: in `build()`, label the haiku-original link "Historical paper", then regenerate everything, including the PDF, on a machine with pdflatex.
2. **Relative links do not work inside the PDF.** validation-paper.pdf contains links to `validation-extension-preregistration.md` and `core-check-evidence-repair.md`, which do not resolve in a PDF. Fixing this also needs a PDF rebuild.
3. **The haiku-original status line repeats itself.** reports/validation-summary.md:18 reads "Recorded status: budget_exhausted. budget_exhausted", because the run's message field equals its status. This is cosmetic only.

## Hugging Face card

This repository has no model-card file. The cards live in the trial repositories and are generated by `reporting.render`. I read the hosted cards `hf://models/BurnyCoder/eureka-digits-luna-models/README.md` and `hf://models/BurnyCoder/eureka-digits-sonnet-models/README.md`. Their accuracy tables (all 15 experiments), the 0.000000 effect, the [0.000000, 0.000000] interval, the "inconclusive" decision and the protocol fields match `reports/validation-data/{luna,sonnet}.json`. The Hugging Face collection `BurnyCoder/auto-eureka-scientist-6ae3ae37b267f00aef999f75` contains exactly the four model bundles, as the docs claim. No repository copy exists to drift, so there is nothing to upload.

## Regenerated artifacts and tests

- `PYTHONPATH=src:scripts python scripts/summarize_validation.py --no-pdf` was run in a Python 3.14 venv with numpy 2.5.4 and matplotlib 3.11.2, the same versions as uv.lock. Before my edits it reproduced every text artifact byte for byte. After the script fix, only site/validation-summary.md changed, and that file is committed.
- The regenerated PNGs differ pixelwise in 5-9% of pixels (font rendering; same shape and same data). I reverted them rather than committing font churn.
- The PDF was not regenerated because pdflatex is not installed. pdftotext confirms that the committed PDF matches the current paper Markdown: the execution table, the 47-test sentence, the effect and CI lines, and the console and Sol paragraphs. reports/validation-paper.pdf and site/validation-paper.pdf are identical.
- Tests: `py_compile` passes on the changed files. `pytest tests/test_reporting.py tests/test_execution.py tests/test_web.py tests/test_settings.py` gives 25 passed. The full suite was not run because it needs the torch/CUDA research extra, which is too large a download here. The code changes are limited to URL comments and the site-copy link rewrite.
