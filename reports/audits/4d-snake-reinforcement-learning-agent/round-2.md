---
repo: BurnyCoder/4d-snake-reinforcement-learning-agent
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 175
fixed: 5
unverifiable: 6
not_fixed: 0
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/4d-snake-reinforcement-learning-agent, round 2
## Summary

I checked README.md, reports/paper.md, all six experiment write-ups, reports/networks.md (prose and shared-settings table), docs/rl_design.md, docs/game_rules.md, docs/evaluation.md, THIRD_PARTY_NOTICES.md, and the code that the method claims depend on (config.py, physics.py, callbacks.py, imitation.py). I compared them with reports/data/* (summary.json, config.json, episodes.json, progress.csv, evaluations.npz, run.log, benchmark.json, versions.json) using short scripts, and with primary sources fetched during this audit: the arXiv API, the AlphaSnake PDF, the linyiLYi/snake-ai, eugeneko/Snake4D and twanvl/snake sources, the sb3-contrib `distributions.py` source, and the SB3 changelog.

The repository is in good shape. Every headline number I recomputed matches its artifact. That covers the README table, the throughput figures, the exp04 frontier timings and collapse points, the exp05/05b statistics, the per-seed values and the derived efficiency metrics. I found five errors, all small: one wrong author initial in a citation, one cited project missing from the paper's reference list, one wrong statement about a run's configuration, and two numeric ranges that did not match the data. All five are fixed.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| reports/paper.md:229 | `Du, Y. et al. (2022). AlphaSnake: ...` | `Du, K., Gemp, I. and Wu, Y. (2022). AlphaSnake: ...` | https://export.arxiv.org/api/query?id_list=2211.09622 (authors Kevin Du, Ian Gemp, Yi Wu) |
| reports/paper.md:241 | reference list omits eugeneko/Snake4D, which the introduction (line 45) cites | `..., Pella86/Snake4d, eugeneko/Snake4D (see THIRD_PARTY_NOTICES.md).` | https://raw.githubusercontent.com/eugeneko/Snake4D/master/README.md ("I cannot play it beyond certain snake length") |
| reports/experiments/exp02_ppo_2x4.md:80 | "Curriculum defaults switched to the strict gate for exp03b (3^4) and exp04 (4^4)." | strict gate used by exp03b; exp04 overrode it with `rho=0.8`, window 16, frontier step 8 | reports/data/exp04_ppo_4x4/config.json (curriculum_rho 0.8, window 16, delta 8); experiments/exp04_ppo_4x4.env |
| reports/experiments/exp03_ppo_3x4.md:57 | true-start training fill "similar across the arms (0.53-0.55)" | "(0.53-0.54)" | reports/data/exp03{a,b,c}_*/episodes.json: true_start_fill_mean 0.5395 / 0.5289 / 0.5280 |
| reports/experiments/exp03_ppo_3x4.md:47 | "Starting as a 71-79-cell cycle segment" | "Starting as a 68-79-cell cycle segment" | exp03c logged frontier 80 -> 76 (run.log) with window 8 (config.json): starts of 68-76 cells after the advance (physics.reset: `[hi - window, hi]`) |

## Unverifiable or hedged claims

- README.md:57: "fast suite, about 25 s". I did not install the full environment (torch CUDA wheels are over 1 GB), so I could not time the suite.
- exp01_baselines.md:133-135: the original Gray-code path follower reached "about 4 % fill" and was "removed in PR #6, commit f3b68d7". The run is not archived. The clone has only one commit, and this session had no GitHub API access to the repository, so the commit could not be resolved. The text already says this cannot be checked from archived artifacts.
- exp00_benchmark.md:3: the "first grid of 2026-09-04, not archived" put the batched env first. Not archived; already flagged in the text.
- paper.md:228 and docs/game_rules.md: Skiena 1990, p. 148, cited via MathWorld. Not fetched during this audit (budget).
- exp00_benchmark.md:23: "Gymnasium paper Fig. 3 in v4 (Fig. 1 in v2)". The arXiv ID, title and authors are verified; I did not check the figure numbers.
- paper.md:221: Patterson et al. 2024, JMLR 25(318). The URL format is consistent; I did not fetch the volume and page numbers (budget).

## Problems found but not fixed

None. Because of the budget cap, these surfaces were only spot-checked or not opened:
- docs/architecture.md, docs/troubleshooting.md, and docstrings in modules other than config/physics/callbacks/imitation;
- the full citation metadata of the uncited entries in the paper's reference list (Raffin, Müller, Florensa, Silver, Sutton and Barto);
- nine of the ten hosted Hugging Face cards.

## Hugging Face card

The repository has no card file. `snake4d publish` (src/snake4d/publish.py) generates the cards from reports/data. I read the hosted card of the headline model, `hf://models/BurnyCoder/4d-snake-exp02d-ppo-2x4-backplay-strict/README.md`. Its numbers match reports/data/exp02d_ppo_2x4_backplay_strict_best/summary.json:
- deterministic: 0.963 +- 0.009, return 24.46, fill 0.994, 43.5 steps, won within 4C 0.963;
- sampling: 0.960 +- 0.033, fill 0.994, 44.1 steps, won within 4C 0.957.

Its gate 0.9 / window 4 / 5M steps also match config.json. I found no drift, so no upload command is needed. The other nine cards were not read.

## Regenerated artifacts and tests

- reports/paper.pdf was rebuilt with the repository's own `snake4d.report.to_pdf`. The usual route, `uv run --group docs snake4d report --pdf`, needs torch and SB3, so I ran the function directly with markdown-pdf and a stub for the unused `stable_baselines3.common.monitor` import. The new 28-page PDF contains all the fixed text.
- reports/all_experiments.md and the figures need the git-ignored `runs/` directory, so I did not regenerate them. None of the edits touch them.
- Tests: `tests/test_docs_numbers.py` and `tests/test_scientific_audit.py` gave 155 passed and 3 skipped. I deselected `test_mlp_params_matches_the_built_policy` because it needs torch. The two PDF tests in `tests/test_report.py` passed. No code was changed.
