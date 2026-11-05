---
repo: BurnyCoder/4d-snake-reinforcement-learning-agent
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 330
fixed: 11
unverifiable: 7
not_fixed: 2
hf_card_drift: yes
---
# Fact-check audit: BurnyCoder/4d-snake-reinforcement-learning-agent, round 1

## Summary

I checked the claims in README.md, the paper (reports/paper.md and its PDF), docs/*.md, the six experiment write-ups, reports/networks.md, reports/all_experiments.md, the numbers in reports/scientific_audit.md, THIRD_PARTY_NOTICES.md, code and pyproject comments that cite sources, and the hosted Hugging Face card. I did not use the repository's earlier audit as evidence.

Every number was recomputed with short scripts from `reports/data/**` (summary.json, eval_episodes.csv, evaluations.npz, progress.csv, episodes.json, run.log, config.json, benchmark.json, gate_episodes.csv). Nearly all of them were correct, including:
- the README results table;
- the networks.md score and efficiency tables (all 70 network cells and the baseline values);
- the exp00 benchmark arithmetic (10x, 3.7x, 3.4x, 4.3-7.9 us, 8 %);
- the exp02 failure counts (61/35, median 33/31, 23 of 37);
- the exp04 frontier timeline, and its collapse below 0.001 at about 73M steps and to exactly 0 from about 77M;
- the exp05/05b counts (64/300, 71/300, 4,928 steps per env, approx_kl 7.9e-7 to 1.7e-5, nine evaluations at 1.00);
- the Wilson intervals, the filtered gate counts (394/537, 355/492) and the transition shares;
- the MLP weight counts (0.60M / 0.86M / 1.58M).

All arXiv IDs, titles and authors matched (11 papers), as did the JMLR, SIAM DOI and NeurIPS citations. Library and version claims also matched: SB3 2.9.0 supports Python up to 3.13, numpy 2.5 needs Python >= 3.12, the cu128 index stops at torch 2.11 and cu130 carries 2.14, pygame 2.6.1 dates from 2024-09-29, get_linear_fn was deprecated in SB3 2.7.0, HUGE_NEG is -1e8, and best-model selection uses `mean_reward > best_mean_reward`.

The errors I found were source attributions and overclaims about external projects. I made 11 claim-level fixes in 7 commits and regenerated the PDF. All commits are pushed.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| reports/paper.md:30-31 (abstract) | selected checkpoint reached 40 % fill "(best episode 66 %)" | "(best true-start training episode 66 %, `episodes.json`)" | reports/data/exp04_ppo_4x4/episodes.json (true_start_fill_max 0.660); exp04_ppo_4x4_best/eval_episodes.csv max fill 0.621 |
| reports/paper.md:155-156 (exp04 bullet) | "true-start fill 0.40 (best episode 0.66)" | "(best true-start training episode 0.66)" | same as above |
| reports/paper.md:51-52 | "linyiLYi/snake-ai fills a 12x12 board with MaskablePPO" | "trains MaskablePPO on a 12x12 board (its default `board_size`; its README does not report board completion)" | https://github.com/linyiLYi/snake-ai (README); main/snake_game_custom_wrapper_cnn.py `board_size=12`; main/train_cnn.py MaskablePPO |
| reports/paper.md:72-74 | AlphaSnake "uses the Hamiltonian-cycle strategy as its scripted baseline" | "its Table 1 compares it with a Hamiltonian-cycle strategy among other baselines" | https://arxiv.org/abs/2211.09622 (Table 1: AlphaZero, random, Hamiltonian cycle, naive tree search) |
| docs/rl_design.md:11-12 | "the reference agent that fills a 12x12 board (linyiLYi/snake-ai)" | "the reference agent for a 12x12 board (linyiLYi/snake-ai, default `board_size=12`)" | linyiLYi/snake-ai source, as above |
| THIRD_PARTY_NOTICES.md:13 | "MaskablePPO for board-filling snake" | "MaskablePPO for snake" | linyiLYi/snake-ai README |
| reports/experiments/exp03_ppo_3x4.md:50 | "the logged curriculum success was 60-85 %" | episode-weighted means 78 % (exp03b) and 60 % (exp03c); logged per-rollout ranges 0.22-0.91 and 0.14-0.80 | reports/data/exp03b/c_*/episodes.json, progress.csv |
| src/snake4d/callbacks.py:15 | curriculum starts "as a prefix of the Hamiltonian route" | "as a segment of the Hamiltonian route at a random rotation" | src/snake4d/physics.py `reset` (random offset modulo route_len) |
| src/snake4d/physics.py:74 | "most resets begin as a prefix of the demonstration" | "... as a segment of the demonstration" | same code |
| pyproject.toml:26 | "gymnasium 1.3 depends on pygame-ce" | "gymnasium 1.3's rendering extras depend on pygame-ce" | https://pypi.org/pypi/gymnasium/1.3.0/json (pygame-ce appears only under extras) |
| src/snake4d/train.py:13-14 | "SB3 maintainers report large CPU speed-ups with one thread for small MLPs" | "an SB3 maintainer reports ~5x CPU speed-ups in some cases from one thread (`OMP_NUM_THREADS=1`) for small MLPs" | https://github.com/DLR-RM/stable-baselines3/issues/121 |

## Unverifiable or hedged claims

- README "fast suite, about 25 s": I did not run it. It needs the full torch cu130 install (over 1 GB). 159 torch-free tests passed. The one torch-dependent test in those files could not run.
- exp00 "first grid of 2026-09-04, not archived" and exp01 "Gray-code path follower reached about 4 % fill (PR #6, commit f3b68d7)": these runs are not archived, and the clone is shallow. The write-ups already say these cannot be checked.
- exp00 "Gymnasium paper Fig. 3 in v4 (Fig. 1 in v2)": I did not check figure numbers across arXiv versions. The paper metadata is correct.
- oscarknagg/wurm single_snake.py: the URL returned HTTP 403, so I could not confirm its body-age encoding.
- Ng, Harada & Russell 1999 and Grzes 2017 ACM pages: Cloudflare blocked the fetch. The titles and venues are the standard ones, but I did not confirm them from the page.
- CLAUDE.md links to code.claude.com memory docs: not fetched.
- Throughput and wall-clock figures (33k fps, 54 min and similar) match benchmark.json and progress.csv. They cannot be re-measured on CPU.

## Problems found but not fixed

- reports/paper.md references list three papers that the paper body never cites: Müller et al. 2019, Florensa et al. 2017 and Silver et al. 2017. Their metadata is correct. I left them in place because removing them is an editorial choice, not a factual correction.
- The hosted Hugging Face cards differ from the repository's current card template (see the next section). I cannot write to the Hub.

## Hugging Face card

The repository has no card file. Cards are generated by `publish.model_card` (src/snake4d/publish.py). I read `hf://models/BurnyCoder/4d-snake-exp02d-ppo-2x4-backplay-strict/README.md`. Its numbers match `reports/data/exp02d_ppo_2x4_backplay_strict_best/summary.json`: 0.963 +- 0.009, return 24.46, fill 0.994, 43.5 steps, and the sampling row 0.960 / 0.994 / 44.1 / 0.957.

All ten `BurnyCoder/4d-snake-*` repos and the collection exist. The repos were last updated 2026-09-06, which is before the current template. Against that template, the hosted card:
- lacks the paragraph stating that `+-` is the std across evaluation seeds, that the run has one training seed, and the link to the audit;
- lacks the bullet "selected by mean evaluation return, not completion rate";
- lacks the caveat about the stale curriculum gate;
- says "Code: ... at commit 09536a7..." where the template says "recorded HEAD ..., not the exact executed source";
- labels the completion metric "(deterministic, 100 episodes x 3 seeds)" where the template says "(deterministic; std across evaluation seeds)".

I compared only the exp02d card in detail. Drift in the other nine is inferred from the shared template and upload date.

To refresh the cards, run `uv run --group hub snake4d publish`, which needs the original `runs/` artifacts. Alternatively, generate each card with `publish.model_card` and run `huggingface-cli upload BurnyCoder/4d-snake-<run> path/to/card.md README.md`.

## Regenerated artifacts and tests

- reports/paper.pdf was regenerated with `snake4d.report.to_pdf`, using markdown-pdf 1.13.3 and PyMuPDF 1.28.2 as locked in uv.lock, in a scratch venv where stable_baselines3 was stubbed out. It is still 28 pages, and the corrected text is present. I could not run the full `snake4d report --pdf`: it rebuilds all_experiments.md from `runs/`, which is not in the repository.
- Tests: `pytest tests/test_pyproject_rules.py tests/test_scientific_audit.py tests/test_docs_numbers.py` gave 159 passed, 3 skipped, 1 failed. The failure is `test_mlp_params_matches_the_built_policy`, which needs torch; I checked those weight counts by hand instead. `ruff check src tests` passes. I ran no training or model inference.
