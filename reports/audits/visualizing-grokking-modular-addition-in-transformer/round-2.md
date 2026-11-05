---
repo: BurnyCoder/visualizing-grokking-modular-addition-in-transformer
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 310
fixed: 1
unverifiable: 18
not_fixed: 3
hf_card_drift: yes
---
# Fact-check audit: BurnyCoder/visualizing-grokking-modular-addition-in-transformer, round 2
## Summary

I did this audit on my own and did not use earlier audits as evidence. Run outputs (`runs/`, `site/`) are not in git. So the ground truth for numbers was:
- `site/data/summary.json`, downloaded from the HF dataset at the revision pinned in `site-data.lock` (`6ddc304d…`);
- `reports/tables/hypotheses.json`;
- `reports/tables/exp01_rchecks.md`;
- `.env.example` and `src/grokviz/config.py` for the settings.

I also fetched these primary sources:
- arXiv 2301.05217v3 (PDF text, page by page) and 2201.02177v1;
- arXiv API metadata for every arXiv entry in `paper/refs.bib`;
- the GitHub Pages limits page;
- the npm registry for Plotly 4.1.2 and KaTeX 0.19.0;
- the hosted HF cards and the HF collection.

What I checked, and how:
- **README and paper.** Every number in `README.md` and `paper/main.typ`: the architecture, parameter count, split, optimiser settings, the R-check counts, patching fractions, Fisher/Holm p-values, the H4 numbers, the same-init numbers and the dynamics numbers.
- **Reports.** All typed numbers in `reports/summary.md` and `reports/exp-01…04`, and the exp-02 per-run table (t1, t2, K, control accuracies; the t3 and t_grok means were recomputed).
- **Statistics.** The power table in `docs/preregistration.md`, recomputed from the binomial distribution.
- **Quotes.** All 19 paper quotes in `content/quotes.yaml`, checked by script against the PDF page text, including page numbers.
- **Website arithmetic.** The worked examples in chapters 4, 5, 9, 10, 11 and 12, recomputed.
- **Errata.** The paper errata listed on the errata page.
- **Site counts.** The feature counts: 76 figures, 19 widgets, a 15-step tour with 7 playing steps, a hero panel plus 8 groups, speeds ¼× to 8× at 10 checkpoints/s, and the clip step ranges.
- **Versions.** Library versions against `uv.lock` and the CDN registry.

The repository is in very good shape. I found one factual error, a rounding error in exp-01, and fixed it. The only other problem is drift between the repository and the hosted Hugging Face cards: they still use the old repository and website URLs. I cannot fix that on the Hub; it is listed below.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| reports/exp-01-paper-validation.md:41 | "falls 3,373 → 2,001 → 996" | "falls 3,373 → 2,001 → 995" | `summary.json` `paper.ssw_t3` = 995.48 (`rc.R15` = [3372.6, 2001.3, 995.48]); `reports/tables/exp01_rchecks.md` R15 shows 995.5. 995.48 rounds to 995, not 996. |

## Unverifiable or hedged claims

None of these was changed. Each is plausible, and the repository labels most of them as engineering measurements or log-derived values. The evidence behind them is not in git or in the published `summary.json`.
- Run times: 73 min of training (4,376 s), 72 min of per-checkpoint metrics, about 3 min for the paper run, about 30 ms per step for one run, about 210 s per 2,000 steps. These come from logs that are not committed. The arithmetic between them is consistent: 7.3 h, about 6×, about 0.5 s per checkpoint.
- The cross-process relaunch reproduction ("six runs, steps 2,000–10,000", `wd1_s0` = 0.782 at step 10,000) and the timestamps in the preregistration deviations. Only the `prereg-v1` tag → `9e2207c` was confirmed, with `git ls-remote`.
- exp-01: Gini(W_L) = 0.801; the k = 52 cos/sin norms 4.146 vs 4.055 (the 2.2 % arithmetic is correct); the skip-included variant 1.52 × 10⁻⁷; `train_losses[100]` = 2.273161.
- exp-03: the S1 range 62.7–90.4 %; per-seed Gini ranges for `wd1` (0.61–0.77 W_E, 0.78–0.88 W_L) and the random-basis null percentiles; the K-free excluded loss peaking at initialisation in 7 of 11 `wd1` runs (the other four at 5.6–10.8). `summary.json` agrees with the pooled range 0.61–0.88 over the 14 grokked runs.
- exp-04 per-seed values: 1.055–1.067 at step 1,000, 0.96–0.97 and 0.97–0.99, `wd1_s4` at 0.89 / −0.92, cos(d, g) ≈ 0.01 and 0.21, the update-norm peak steps, and 72 MB per run of Adam moments (consistent with about 41 × 2 × 226,816 float32 values).
- Site data "about 640 MB"; the t-test effect sizes in the power table (scipy was not available, so not recomputed); "Node.js tested with 22 and 24".
- ARENA-based statements: the late change near epoch 43,000, the ARENA "bonus chapter" mechanism, the ARENA errata items, and the R16–R20 reference values. The ARENA page resolves (HTTP 200), but I did not read it in full.
- The paper code repository URL (`mechanistic-interpretability-grokking/progress-measures-paper`) could not be fetched: GitHub access is blocked for this session.
- summary.md says "When the R7 reference value was corrected, every bound copy updated together". This is history and cannot be checked from the files.

## Problems found but not fixed

1. **Hosted model card `BurnyCoder/grokking-modular-addition-runs`.** It links `https://github.com/BurnyCoder/visualizing-grokking-modular-addition`, the old repository name. The template in `src/grokviz/hf_publish.py` (`GITHUB_URL`) already uses `…-in-transformer`. The repository side is correct; only the Hub copy is stale.
2. **Hosted dataset card `BurnyCoder/grokking-modular-addition-site-data`.**
   - `license_link`, the code link and the website link use the old name.
   - The website link `https://burnycoder.github.io/visualizing-grokking-modular-addition/` returns **404**. The correct site, `…-in-transformer/`, returns 200.
   - The repository template is correct.
3. **Hosted card `BurnyCoder/grokking-modular-addition-transformer`** (the seed-999 TransformerLens model, not generated by this repository). Its phase-rule link points to `github.com/BurnyCoder/visualizing-grokking-modular-addition/blob/main/docs/operationalizations.md`, the old repository name. GitHub normally redirects renamed repositories, but this could not be confirmed from here. This repository has no copy of that card to fix.

## Hugging Face card

- **Drift: yes.** Apart from the URLs, the hosted runs and site-data cards match the templates in `src/grokviz/hf_publish.py` word for word: the run list, settings, file descriptions and licence text.
- **URL differences.** The hosted cards use `github.com/BurnyCoder/visualizing-grokking-modular-addition` and `burnycoder.github.io/visualizing-grokking-modular-addition/`. The templates use the `…-in-transformer` names.
- **No card files in the repository.** The cards are rendered at publish time, so there is no file to edit. To refresh the Hub copies, the owner can rerun the publishing phases, which re-render and upload both cards:

  ```bash
  uv run grokviz --phases publish_runs_to_hub,publish_site_data
  ```

  Or, after rendering the cards to files:

  ```bash
  huggingface-cli upload BurnyCoder/grokking-modular-addition-runs path/to/model_card.md README.md
  huggingface-cli upload BurnyCoder/grokking-modular-addition-site-data path/to/dataset_card.md README.md --repo-type dataset
  ```

- **Seed-999 card.** For `BurnyCoder/grokking-modular-addition-transformer`, edit its README on the Hub to point at `…-in-transformer`.
- **Other card facts checked:**
  - The collection exists with the README's slug.
  - The seed-999 card states seed 999 (model) and 598 (split), as the README says.
  - The runs card lists 22 runs: 19 addition runs and 3 random-label runs.

## Regenerated artifacts and tests

- **No regeneration needed.** No generated file depends on the edited report: `reports/paper.pdf` is built from `paper/main.typ` and `summary.json`, and neither changed. Nothing was regenerated.
- **No tests run.** No code was touched, so there were no tests to run.
