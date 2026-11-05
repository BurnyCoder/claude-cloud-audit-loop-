---
repo: BurnyCoder/general-physics-attention-residuals-transformer
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 701
fixed: 0
unverifiable: 9
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/general-physics-attention-residuals-transformer, round 1

## Summary

I audited the README, AGENTS.md, docs/, reports/ (prose, per-run reports, receipts), the paper sources (`paper/*.tex`) and compiled PDF, the GitHub Pages viewer (`site/index.html`, `site/app.js`, `site/data/study.json`), the animation and video supplements, figure text, code comments that state facts, and the four hosted Hugging Face model cards. Every number I checked was recomputed with short scripts from the committed result files. Prior audit files were not used as evidence.

Result: I found **no factual errors that needed correcting**. All headline numbers, tables, percentages, confidence intervals, p-values, seed counts, cost/memory figures, physical diagnostics, GPU-ledger totals, data counts and profiling values match the result files. The citations I fetched resolve and support the sentences that cite them. Nothing in the repository was changed, so **no commits were made and nothing was pushed**.

Approximate breakdown of `claims_checked` (701): README 150; paper (abstract, methods, results tables, discussion, appendix, bibliography) 170; docs and report prose 110; per-run experiment reports (18 trained x 2 endpoints + seconds, 18 initialized x 6 horizons) 162; site `study.json` aggregate rows compared with the CSVs 72; Hugging Face cards 12; further external links and sources in docs and reports 25.

Main evidence checked:
- **Headline and README table**: `reports/accuracy_summary.csv` and `reports/untrained/accuracy_summary.csv`. Block radiative 12-step NMSE 0.28917; 1 - 0.289174/0.392769 = 26.38%; 1 - 0.289174/0.419013 = 30.99%; "nine models" = 4 trained + 4 initialized + persistence. All 18 README table values match. Block also has the lowest radiative mean at the 1- and 24-step horizons.
- **Primary analysis**: recomputed from `reports/evaluation/{standard,block}_seed*.json` with scipy. Six effects; improvement 24.52%; t-interval [11.56, 35.58]%; exact sign-flip p = 2/64 = 0.03125; all six effects negative.
- **Seed-level and exploratory claims** (`reports/metrics.csv`, `reports/final_metric_audit.json`). Seeds 0-2 radiative means: Block 0.29203, Standard 0.40246, Full 0.31735, Uniform 0.34735. Full seed 0 (0.30059) beats Block seed 0 (0.30327). Uniform-vs-Block log ratios have mixed signs. All 24 intervention ratios at 12 steps exceed 1 (`reports/interventions.csv`). Mean ratios are 2.565, 2.630, 7.490 and 9.524, with SDs 0.7757, 1.245, 6.105 and 5.603.
- **Initialized controls** (`reports/untrained/metrics.csv`). Block, Full and Uniform Block are worse after training on convection in 6/6, 3/3 and 3/3 seeds. All 18 identities improve on radiative flow. The trained/initialized ratios are 3.671, 13.812 and 3.211. Block and Uniform initialized states have identical hashes on seeds 0-2 (`reports/untrained_baseline_verification.json`).
- **Physical diagnostics** (`reports/physical_diagnostics.csv`). Negative density is 27.30% for Block and 26.04% for Standard. Divergence error is 4.134, 2.823 and 0.228. There are no negative-pressure cells.
- **Costs** (`reports/costs.csv`). Mean wall times are 1,570, 2,460, 2,756 and 2,455 s. Throughputs are 34.42, 21.19, 19.09 and 21.41 examples/s, where examples/s = 16 / median update s. Peak memory is 278.46, 365.88, 546.00 and 345.86 MiB.
- **Budget** (`reports/gpu_budget.json`). The total is 43,951.96 s = 12.208877 h. Training took 39,845.67 s = 11.068 h. Evaluation took 4,031.016 s = 1.119727 h. The original deliverables used 42,285.415 s = 11.745949 h, and the extension 1,666.54 s = 0.462928 h. Profiling plus checks took 74.064 s. Before the extension, evaluation had used 2,364.48 s, about 80.6 min short of the 2-hour allocation.
- **Data** (`reports/data_manifest.json`, `reports/data_audit.json`). The data are 240 trajectories from 36 files, 38.607 GB (decimal). Splits are 120/15/15 and 72/9/9. Grids are 512x128 and 128x384, with 200 and 101 frames. There are 33 cross-split initial-state groups (25 convection + 8 radiative) and 39 sequential overlap witnesses. All held-out trajectories share a training first frame.
- **Profiling and protocol** (`reports/frozen_protocol.json`, `configs/study.json`). The schedule is 3,175 updates, microbatch 4, and effective batch 16, giving 50,800 examples. The projection is 51,839.981 s. All profiling table values match. Parameter counts are 7,919,045 and 7,928,645, a difference of 9,600 = 25x2x192. The code runs AdamW with betas (0.9, 0.999), eps 1e-8, lr 1e-4 and weight decay 1e-4, 5% warmup, and cosine decay to 1e-6. Clipping is 1.0 and the evaluation windows are floor(f(T-28)).
- **Model claims vs code and upstream**. Vendored GPhyT and FLA files match `vendor/provenance.json`. I fetched the pinned upstream raw files again and the hashes still match. The GPhyT-S config (12 layers, 192 width, 768 MLP, 3 heads) matches `vendor/gphyt/models/model_specs.py` and Table 2 of arXiv:2509.13805v4. The upstream `forward` is `differentiate(x) + x` and ignores `step_size`. The AttnRes paper (arXiv:2603.15031v1) confirms zero-initialized pseudo-queries giving uniform weights, RMSNorm keys, block partial sums, final aggregation, and LM-only experiments. Equations 2-6 cover Full and Block AttnRes. Four frames at 128x64 with 1x16x16 patches give 128 tokens.
- **Paper PDF**: 21 pages (pdfinfo). Its text matches the current `.tex` sources (sentence-chunk comparison). `site/paper.pdf` is byte-identical to `paper/main.pdf` and matches the receipt hash 38ab8bd3....
- **Visuals**. Six GIFs each decode to 24 frames at 1200x650 with 200 ms per frame, and their hashes match `reports/animations/manifest.json`. The site copies are identical. The four MP4s have 24 frames at 6 fps (ffprobe). The plotted values in `paired_effects.png` match the six effects and the CI. `site/data/study.json` matches all CSV aggregates (30 + 18 + 24 rows) and the primary JSON. All relative Markdown links in the 55 tracked `.md` files resolve.
- **Per-run reports**. All 18 trained and 18 initialized reports match `reports/metrics.csv`, `reports/costs.csv` and `reports/untrained/metrics.csv`.

## Fixes

None. No checked claim contradicted its evidence, so I made no edits.

| file:line | before | after | evidence |
|---|---|---|---|
| (none) | | | |

## Unverifiable or hedged claims

These claims cannot be checked against committed artifacts or primary sources. I left them unchanged:

1. `reports/data-preparation.md:3` says "Preparation completed ... at 16:46:49 UTC". The only committed timestamp, `reports/data_manifest.json` `created`, reads 16:46:48. The log that may record :49 is not committed. The difference is within timestamp truncation.
2. README:133, `reports/architecture-audit.md` title and `docs/completion.md` call the architecture audit "independent". The audit says it did not reuse earlier conclusions, but nothing records who performed it. The paper says Codex wrote the codebase and paper.
3. `paper/main.tex` AI-authorship statement ("Codex wrote this codebase and paper ... Human cleanup and rewriting are in progress").
4. Test-pass counts and durations in `reports/development.md`, `reports/final-verification.md`, `reports/architecture-audit.md` and the paper appendix (44, 43, 42, 25, 19, 16, 13 and 11 tests). These are historical; the logs live in the uncommitted artifact root. The repository now has 53 test functions.
5. Browser, visual and "no console errors" checks, and the live GitHub Pages byte-match claims, in `reports/final-verification.md` and `reports/public_deployment.json`. The GitHub Actions run links return 403 through this environment's proxy.
6. Git-history timing claims, such as the protocol push before the first GPU lease and PR #5 merged before training. The clone is shallow (one commit).
7. `reports/animation_verification.json` `gpu_ledger_sha256` (4d4b549f...) differs from the SHA-256 of `reports/gpu_budget.json` (ca186b87...). The receipt probably hashes the artifact-root ledger, not the public copy, but this cannot be confirmed from the repository.
8. README:226, "The Codex LaTeX editor can also compile and preview the source".
9. `docs/data-preparation.md`, "The study used release 1.37.0" of aria2. This is consistent with `reports/development.md`, but no download log is committed.

## Problems found but not fixed

1. **Headline wording** (README:1; also generated in `reports/summary.md`, `reports/radiative_highlight.json`, `site/data/study.json` and the HF cards by `src/gphyt_attnres_study/headlines.py`). "GPhyT + Block Attention Residuals beats GPhyT without Attention Residuals and all other tested baselines on radiative flow" holds for **mean** NMSE at all three horizons. It does not hold seed by seed: Full beats Block in seed 0. No significance test covers comparators other than Standard. The sentences right after it state both caveats, and the paper title already says "Lowest Mean 12-Step Error". I left the wording unchanged. It was an explicit owner-requested framing (PR #21), and rewording it in one place would leave the generated artifacts out of sync, since the `report` phase cannot be rerun here. The owner may want to change "beats" to "has the lowest mean error versus" in `headlines.py` and regenerate.

Also worth noting, though not an error: per-run `commit` fields in `reports/training_completion.json` and `reports/experiments/*.md` show later repository HEADs (d43e6479, 4e4d4f77, 45839315). The launch commit was 5ceae76f. All runs came from one training process (pid 47864), so the fields record HEAD at each run start, not the code that was loaded. `reports/execution.md` partly discloses this.

## Hugging Face card

The repository links four model repos: `BurnyCoder/gphyt-attnres-{standard,block,full,uniform-block}`. No card file is committed. Cards are generated from the template in `src/gphyt_attnres_study/publishing.py`, lines 84-148. I read all four hosted `README.md` files with `hf_fs`. They match the template: same headline and lead text, architecture sentence, use and evaluation section, limitations, precision disclosure, sources, and the post-hoc initialization section. Card claims also match the data. The repos hold the stated files: `seedN/` with model, evaluation, metrics and status files; `untrained/seedN/` with model, evaluation and status files; and `untrained/config.json`. There are 6/6/3/3 trained and 6/6/3/3 untrained checkpoints, for 18 + 18, as README:121 states. No drift was found, so no upload is needed. If the owner adopts the headline change above, regenerate the cards with `uv run gphyt-study publish` or upload each card with `huggingface-cli upload BurnyCoder/<repo> path/to/card.md README.md`.

## Regenerated artifacts and tests

- Nothing was regenerated because nothing was edited. Regenerating tables, figures and the PDF with the repository's `report` phase also needs the uncommitted `STUDY_ROOT` artifacts (saved forecasts, run directories) and a LaTeX compiler, neither of which is available here.
- No code was touched, so I did not run the test suite.
- No training or model inference was run.
