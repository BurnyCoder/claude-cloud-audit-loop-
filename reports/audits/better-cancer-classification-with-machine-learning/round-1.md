---
repo: BurnyCoder/better-cancer-classification-with-machine-learning
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 628
fixed: 2
unverifiable: 6
not_fixed: 0
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/better-cancer-classification-with-machine-learning, round 1
## Summary
I checked the README first, then the paper (Typst source and PDF), the generated reports, the GitHub Pages data, the hosted Hugging Face card and the citations they rely on. I did not use earlier fact-check rounds as evidence.

- **Generated tables.** The README tables (arms and ladder) and the paper tables agree with `results/arms/*.json` and `results/comparisons/*.json`. A script recomputed 236 table cells and found 0 mismatches. The values in `site/data/results.json` also agree with the result files (198 values, 0 mismatches).
- **Prose numbers.** These all match their result files: the highlights, the abstract, the discussion and the limitations. That covers the H2 gate, parity, data-audit counts, the 3.1× CI ratio, the WILDS L1 distances and subsample size, label-cleaning removal (11–15× SelfClean), the LoRA sweep and mask audit, HED strength, the example group counts, the H4 fold-0 Δ, the four validation CIs below zero with their p-values, the seed offset, S2's chosen C, and the 0.0004 reproduction gap.
- **External numbers.** These match their primary sources:
  - all 30 eva leaderboard values at the pinned commit (identical to eva `main` today);
  - the eva PCam config (Linear + BCE, AdamW lr 3e-4, 12,500 steps, patience 3, 5 runs);
  - the Hibou paper (936,441 H&E + 202,464 non-H&E slides, 1.2B and 512M patches, rotation/flip augmentation, SGD linear probe, Table 1 PCam 0.953 and 0.946) and the Hibou-L `config.json` (ViT-L/14, 4 registers, SwiGLU);
  - Lee et al. 2024 Table 3 (UNI LP 91.60, FT 90.40, PEFT/LoRA 94.24) and Veeling et al. 2018 Table 1 (89.8 / 96.3);
  - the claims attributed to Elphick 2024, Ciernik 2026 (Table 1, PCam), Wang 2024 v1 (centre 0 = CWZ, 1 = RST, 4 = LPON) and Tomar 2024 §4.1;
  - the CAMELYON16 README (test_049 is a duplicate slide) and the PCam README (label rule, 0.243 µm at 10×, CC0);
  - the swapped md5 sums and the MIT licence on Zenodo;
  - Litjens 2018 on scanners (3DHistech for RUMC/CWZ/RST, Hamamatsu for UMCU, Philips for LPON);
  - 11 model licences on Hugging Face;
  - library versions in `uv.lock`.
- **Citation IDs.** All 25 arXiv IDs resolve to the cited titles, first authors and years.

I found and fixed two problems: a wrong table number in the SelfClean citation, and a sentence that was missing a source I could verify.

## Fixes
| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| src/pcam_hc/paper.py:60, reports/paper/paper.typ:153 (ref [22]), paper.pdf | "(App. L.1, Table 14: automatic-mode estimates)" | "(arXiv v3, App. L.1, Table 16: automatic-mode estimates)" | https://arxiv.org/pdf/2305.17048 (v3): App. L.1 Table 16 lists PatchCamelyon label errors as 589 (0.2%). Table 14 is the AFE table for synthetic issues. v2 has no such table. |
| src/pcam_hc/report_experiments.py:19, :491; reports/experiments/02_ladder_hibou_l.md:48 | "App. L.1 Table 14" | "v3 App. L.1 Table 16" | same |
| README.md:34 | "...tedious and time-consuming ([Ehteshami Bejnordi et al. 2017](jama))" | adds "; [Litjens et al. 2018](https://academic.oup.com/gigascience/article/7/6/giy065/5026175)" | Litjens et al. 2018 (PMC6007545): "This tedious examination process is time-consuming". The JAMA full text could not be fetched (HTTP 403) to confirm its wording. |
| src/pcam_hc/paper.py:139, reports/paper/paper.typ:13, paper.pdf | "tedious and time-consuming [2]" | "tedious and time-consuming [2, 3]" ([3] = Litjens 2018, already in the reference list) | same |

## Unverifiable or hedged claims
- RUMC 0.243 µm/px and UMCU 0.226 µm/px, attributed to Ehteshami Bejnordi et al. 2017 (README Method table and WILDS highlight; paper §WILDS). JAMA and PMC were blocked (403 or bot page). The Litjens 2018 text gives only "0.23 µm to 0.25 µm" overall. I made no change. The scanner-to-hospital mapping itself is verified via Litjens.
- Kaggle Histopathologic Cancer Detection quote ("the original PCam dataset contains duplicate images due to its probabilistic sampling"). The page needs JavaScript and was not fetched.
- The content of the PANDA 1st-place write-up (Kaggle discussion 169143). Not fetched.
- The CodaLab TLS certificate expiry and its renewal time (2026-11-01 13:42 UTC). This is an event record with no source I could check.
- Disk use (about 80 GB: 16 / 43 / 2.4 / 12 GB) and development on an RTX 5070 Laptop GPU (8 GB). These are local facts.

## Problems found but not fixed
- This is not a factual error, but `main.py report` output depends on the machine. `site_data` and `build_experiment_reports` order steps by file mtime, and `arms()` relies on case-sensitive `sorted(glob)`. On a fresh clone, regenerating reorders the ladder-step list, the "adopted" list in the abstract and the arms appendix, with no change in content. For that reason I did not commit a full regeneration (see below).

## Hugging Face card
The hosted card `hf://models/BurnyCoder/pcam-hibou-hillclimb/README.md` is generated by `src/pcam_hc/publish.py::model_card`. The repository has no separate card file.
- The hosted text matches the generator template.
- All 17 artifact rows (34 BA values) match `results/arms/*.json`.
- The LoRA `config.json` on the Hub matches the recipe (r=16, q/k/v/o projections, lr 1e-4).
- The heads listed on the Hub exist.

There is no card drift. The Hub `paper.pdf` now predates the two citation fixes. To refresh it (optional):
`huggingface-cli upload BurnyCoder/pcam-hibou-hillclimb reports/paper/paper.pdf paper.pdf`

## Regenerated artifacts and tests
- I ran `build_experiment_reports()` and `compile_paper()` on CPU in a torch-free venv. Apart from my intended edits, the output differed only in the environment-dependent ordering described above. I therefore reverted the regenerated Markdown and Typst files and applied the same edits by hand. The changed text is exactly what the edited generator produces.
- I recompiled `reports/paper/paper.pdf` from the edited `paper.typ` with typst 0.15.0, the version in `uv.lock`, and checked it with pdftotext.
- I did not regenerate the figures, the README blocks or the site data, because their inputs did not change.
- Tests: `pytest tests/test_stats.py tests/test_licence.py`: 13 passed. The data and GPU tests were not run.
