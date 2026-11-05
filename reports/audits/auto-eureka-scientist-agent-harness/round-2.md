---
repo: BurnyCoder/auto-eureka-scientist-agent-harness
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 270
fixed: 2
unverifiable: 10
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/auto-eureka-scientist-agent-harness, round 2
## Summary

I checked the README, AGENTS.md, docs/, reports/*.md, the generated validation paper (Markdown), the Pages hub (site/), protocol JSON, the digits fixture and adapter code against the saved trial records in `reports/validation-data/*.json`, the JUnit files and primary sources fetched now. I did not use earlier audit files as evidence.

The numbers hold up. An independent script recomputed all 75 saved accuracies from `y_true`/`y_pred` (0 mismatches). It also recomputed the 24 method means and sample SDs in the README, the four primary paired effects (all seed effects are 0, and regularized and unregularized predictions are identical for every seed, so the CI is [0, 0]), and the execution table (status, phases, calls, active minutes, reported identities). The test counts also match: 47 in offline-tests.xml and 90 in console-tests.xml. I ran `scripts/summarize_validation.py --no-pdf` on CPU before making any edits. It reproduced README.md, validation-summary.md, validation-paper.md, site/index.html, site/validation-summary.md, site/validation.json, docs/settings.md and console-acceptance.md byte for byte. Only the PNG rasters differed, from font rendering.

The run-history claims match the attempt records. Haiku stopped at the 60-minute cap with 5 of 8 phases accepted. The extension raised the limits to 180 minutes and 60 calls with cumulative counters, reaching 20 calls. Sonnet's attempt 1 reported both Sonnet and Haiku and was rejected, and all later Sonnet attempts report Sonnet only. The runs were sequential: Haiku, then Luna, then the Haiku extension, then Sonnet, then Sol. Codex identities were not exposed. The CLI flags and environment variables described in the README and adapters.py match current Claude Code and Codex documentation. Every external link that is not on github.com resolves, and the cited titles match (Lones arXiv 2108.02497, Lipton and Steinhardt 1807.03341, Neel Nanda's sequence and its 4 posts, Anthropic's harness article, NeurIPS checklist, FastAPI SSE, which arrived in 0.135.0). The dataset and project licenses match the sources: UCI CC BY 4.0, Ralph Apache-2.0, ralphex MIT, FastAPI MIT, Uvicorn BSD, and a custom license for AI Scientist v2.

I found two problems and fixed both.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| docs/sources.md:13 | autoresearch: "No applicable license established in this review; no code copied" | "Its README states MIT, but the repository has no separate LICENSE file; no code copied" | https://raw.githubusercontent.com/karpathy/autoresearch/master/README.md (`## License` / `MIT`, line 90); LICENSE, LICENSE.md and LICENSE.txt return 404 |
| scripts/summarize_validation.py:88 (generator), reports/validation-summary.md:15, reports/validation-paper.md, site/validation-summary.md, site/index.html | haiku-original link labelled "Explorer" / "Explore evidence" | "Historical paper" | The link target is `.../eureka-digits-haiku/blob/6f82ace.../site/paper.pdf` (built from `reports/verification/haiku-final-publication.json`): a PDF, not an interactive explorer |

## Unverifiable or hedged claims

- Trial repository pages (github.com/BurnyCoder/eureka-digits-{haiku,luna,sonnet,sol}) and the historical Haiku `paper.pdf` at commit 6f82ace: the session's proxy and GitHub access block other repositories (HTTP 403). The raw `reports/parent-review.md` files for Sonnet and Sol did resolve (200).
- The claim that Sonnet's first-attempt Haiku identity came from "a native background WebFetch summary" (validation-interpretation.md, plan-audit.md): the attempt record confirms the mixed identities and `searched=true`, and the Claude docs confirm that `ANTHROPIC_DEFAULT_HAIKU_MODEL` serves "background functionality". The exact cause, though, would need the private transcripts.
- Membership of the shared HF collection: the collection page returns HTTP 200, but the HF MCP tool was refused access. This rests on `reports/verification/shared-collection.json` only.
- Haiku's `reports/extended-parent-review.md` corrections live in the trial repository, which I could not open.
- Paper AI statement ("Codex wrote this harness codebase...") and docs/sources.md "Sources were inspected before implementation": no evidence available.
- Console live-smoke details beyond `reports/console-acceptance.json` (stderr MCP 403 warning) are in private transcripts.

## Problems found but not fixed

- `reports/validation-paper.pdf` and `site/validation-paper.pdf` still show the old "Explorer" label for haiku-original. pdflatex is not installed, so I could not rebuild the PDF. Rebuild it with `uv run --extra research python scripts/summarize_validation.py`, which needs LaTeX.
- README.md:105 and validation-preregistration.md:15 call the data "scikit-learn's bundled UCI digits". The scikit-learn docs say the bundled set (1,797 images) is "a copy of the test set of the UCI ML hand-written digits datasets", while the UCI dataset has 5,620 instances. The sentence is not false, only imprecise, so I left it.
- Cosmetic: the generated report prints "Recorded status: budget_exhausted. budget_exhausted", because the run message repeats the status. This is not a factual error.

## Hugging Face card

This repository has no model card file. It links four model bundles and one collection. I read the hosted cards for `BurnyCoder/eureka-digits-luna-models` and `BurnyCoder/eureka-digits-sonnet-models`: their accuracy, seconds and device tables match `reports/validation-data/luna.json` and `sonnet.json` exactly. The Sol bundle lists 12 MLP safetensors (38,728 bytes each, consistent with a 64-128-10 float32 MLP), plus the logistic and class-prior `.npz` files, `protocol.json` and `study.py`. With no card file in this repository there is nothing to compare, so no upload command is needed.

## Regenerated artifacts and tests

- `scripts/summarize_validation.py --no-pdf` ran in a scratch Python 3.14 venv (numpy 2.5.4, matplotlib 3.11.2, as locked). Before my edits it reproduced every text artifact byte for byte. After the label fix it regenerated validation-summary.md, validation-paper.md, site/index.html and site/validation-summary.md. README.md, site/validation.json, docs/settings.md and console-acceptance.md were unchanged. I restored the regenerated PNGs to the committed versions because they differed only in raster bytes.
- I did not rebuild the PDF (no LaTeX).
- No package code changed, and no test imports `scripts/summarize_validation.py`, so I did not run pytest. The full suite needs the ui and research extras, including torch. The edited script ran successfully end to end.
