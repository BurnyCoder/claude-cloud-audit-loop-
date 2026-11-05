---
repo: BurnyCoder/visualizing-grokking-modular-addition-in-transformer
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 220
fixed: 5
unverifiable: 9
not_fixed: 1
hf_card_drift: yes
---
# Fact-check audit: BurnyCoder/visualizing-grokking-modular-addition-in-transformer, round 1

## Summary

The measured numbers hold up. Ground truth was `summary.json` and `manifest.json` from the pinned site-data revision
(`6ddc304`, `site-data.lock`) and `reports/tables/hypotheses.json`. Against these I recomputed with scripts the README
results, the reports' typed prose and tables (exp-01 to exp-04, summary.md), the exp-02 per-run table (t1/t2/t3/t_grok
and K for all 22 runs), the exp-03 effect-size ranges, Gini ranges and secondary CIs, the seed means and the parameter
count. They all match to the stated rounding. I also rebuilt `reports/paper.pdf` from `summary.json`. Apart from the
URLs, its text is identical to the committed PDF, so every number bound into the paper is consistent with the
published data.

Paper quotes and settings checked against the arXiv v3 PDF (pages located by text):
- p. 3 settings;
- "under 0.55%" (p. 6);
- "0.1% to 0.4%" (p. 13);
- 433 (84.6 %), 5.54e-8, 2.48e-7, 1.19e-7, 5.27, 19.1, 24.3, 9.12e-7, 7.25e-7, 7.24e-8, 4.7e-8;
- the Table 2 head frequencies and FVEs, the 92.42–99.10 % head fits, 97.5 %;
- the four extra seeds;
- the data-fraction claims (App. C.2.2, Fig. 20).

Also checked:
- Power et al. App. A.1.2 (minibatch 512, Adam without weight decay for 10⁶ steps): matches.
- The released code at commit `23d2c64`: betas, LambdaLR warm-up, split, d_vocab = p+1, and `helpers.py` casting to
  float32. All match.
- All 16 bibliography entries: arXiv/PMLR metadata, YouTube title and date, HF upload date. All correct.

The one real error was the website URL. The repository was renamed, and the advertised GitHub Pages address returns 404.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| README.md:7 | `https://burnycoder.github.io/visualizing-grokking-modular-addition/` | `https://burnycoder.github.io/visualizing-grokking-modular-addition-in-transformer/` | curl 2026-11-05: old URL 404, new URL 200 ("Grokking, Visualized") |
| paper/main.typ:26 (and reports/paper.pdf, regenerated) | same old Pages URL | new Pages URL | same |
| src/grokviz/hf_publish.py:67 (dataset card template) | same old Pages URL | new Pages URL | same |
| README.md:204-205, paper/main.typ:27,334, hf_publish.py:31, content/chapters/07:69, 17:28, 20:9, content/pages/index.md:19, reproduce.md:3,6-7, templates/base.html:41, figure.html:26 | `github.com/BurnyCoder/visualizing-grokking-modular-addition` (old name, works only via redirect) | `github.com/BurnyCoder/visualizing-grokking-modular-addition-in-transformer`; clone `cd` line updated to match | `git remote -v` of the clone; `git ls-remote` shows both names resolve to the same HEAD |
| README.md:123-125 | "It diverges numerically within ~50 steps" | "Its training loss matches the paper's to 5 significant digits for the first 52 steps and then diverges … (a single same-initialisation pair)" | summary.json `seeds.same_init_loss_steps` = 52; reports/exp-02-training.md:128-129 |

## Unverifiable or hedged claims

Left unchanged. Each needs files that are not in the repo or the site data.
- **Engineering timings.** 73 min training, 72 min analysis, ≈ 30 ms per step, 2,000 steps per 210 s. They come from
  `logs/` (gitignored). The arithmetic among them is consistent: 4,376 s ≈ 73 min, 7.3 h / 73 min ≈ 6×,
  0.49 s per checkpoint.
- **Relaunch check.** "Relaunch reproduced every logged test accuracy (six runs, steps 2,000–10,000)" also needs the logs.
- **exp-02 test-loss column.** Needs `curves` arrays, which were not downloaded. The spike counts and peaks match
  summary.json.
- **exp-01 skip value.** "Including the skip connection gives 1.52 × 10⁻⁷" comes from `rchecks.json` details, which are
  not published.
- **exp-04 per-seed values.** `wd1_s4` ratio 0.89, cos(d, g) ≈ 0.01/0.21, step 1,000/2,000/3,000 ratio ranges. These
  are in `gradients.npz`, not in the site data. The aggregate CIs match.
- **exp-03 excluded-loss peaks.** "7 of the 11 wd1 runs peak at initialisation (others 5.6–10.8)": the per-run wd1
  peaks are not exported. The control peaks (4.75–4.77) match.
- **Node.js.** "Tested with 22 and 24": CI uses 22 only.
- **PAIR explorable authors.** The page renders them client-side, so they could not be confirmed. Title and Aug 2023
  are confirmed.

## Problems found but not fixed

- **Hosted Hugging Face cards.** Both still carry the old URLs: the dataset card's website link is a 404, and both
  cards' GitHub links use the old name. I cannot write to the Hub (see below).

## Hugging Face card

The hosted cards were read with `hf_fs`:
- `BurnyCoder/grokking-modular-addition-runs` (model)
- `BurnyCoder/grokking-modular-addition-site-data` (dataset)

They are exactly the rendered templates in `src/grokviz/hf_publish.py`, apart from the URLs fixed on this branch:
- **Dataset card.** Website link `burnycoder.github.io/visualizing-grokking-modular-addition/` (404) and GitHub links
  (`license_link`, code link) with the old repository name.
- **Model card.** The GitHub link on its last line has the old repository name.

Other card claims check out against the data: 22 runs (19 add, 3 rand), the per-run titles, the paper revision `80e5dbb…`.

A corrected dataset card, rendered from the fixed template, is at
`/tmp/claude-0/-home-user-claude-cloud-audit-loop-/b6cb3a22-e8eb-5ef7-9ac4-134f09965e5b/scratchpad/site-data-card.md`.
To upload it:

```
huggingface-cli upload BurnyCoder/grokking-modular-addition-site-data site-data-card.md README.md --repo-type dataset
```

For the model card, rerun `uv run grokviz --phases publish_runs_to_hub`, which regenerates `runs/README.md` from the
template. Or edit the hosted card's last line by hand and upload:

```
huggingface-cli upload BurnyCoder/grokking-modular-addition-runs runs/README.md README.md
```

The collection and the linked repos all resolve (HTTP 200), including the seed-999 TransformerLens replication and
`callummcdougall/grokking_full_run_data` (456 MB, so "~0.5 GB" is right).

## Regenerated artifacts and tests

- **Paper.** `reports/paper.pdf` was regenerated with typst 0.15.0 (the locked version) through
  `grokviz.paper.paper_inputs`, from the pinned `summary.json` and `reports/tables/hypotheses.json`. Text diff against
  the old PDF: only the two URLs changed.
- **Not regenerated.** Site, figures and clips: my edits touch no data, and the Pages workflow rebuilds the site from
  the templates.
- **Tests.** `uv run --extra cpu pytest -m "not gpu and not network and not slow and not browser"` (the CI command):
  77 passed, 5 skipped.
