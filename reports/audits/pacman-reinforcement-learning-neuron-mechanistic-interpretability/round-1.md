---
repo: BurnyCoder/pacman-reinforcement-learning-neuron-mechanistic-interpretability
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 455
fixed: 1
unverifiable: 6
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/pacman-reinforcement-learning-neuron-mechanistic-interpretability, round 1

## Summary

The repository is in very good factual shape. I found one imprecise sentence and fixed it. Nothing else was wrong.

- **Inline numbers (309).** I checked every `<!--n:key-->value<!--/n-->` marker in README.md, reports/*.md, paper/paper.md, docs/*.md and site/index.html against `results/report_numbers.json`, using a script. All 309 match and none uses an unknown key.
- **Recomputed from raw results (about 40).** I recomputed these with scripts:
  - discovery mean ± SD scores for the three agents;
  - H1 one-job fractions, unit counts and difference CIs for all three agents;
  - the threshold-sweep reversal, including the 8.0% vs 1.4% case;
  - the "every one-job unit follows pellets left or maze id" claim, in every set and agent (`claim_checks_*.json`);
  - untrained alive units (499/500/501);
  - the "less clean than mixtures (1111, 2222) and untrained (all three)" claim;
  - deaths and return off-target signs for all six candidates;
  - H2 pass/fail and null counts for all six candidates;
  - secondary-metric and ghosts-per-pill directions;
  - dithering in each agent;
  - fc 453's strongest null (−0.0652 vs −0.0659);
  - fidelity numbers.
- **Method claims (about 26), checked against the code:**
  - parameter count 1,689,258, computed by hand from the layer shapes;
  - conv sizes and the 36×36 receptive field with its 16 px core;
  - the wrapper chain, the alive threshold, the one-job thresholds and the 2–8 unit mixtures;
  - seeds, the 30 pilot games, `HORIZON` = 8, 4,000 screen states and the 12 px occlusion patch;
  - bootstrap and permutation counts;
  - 40 features in 5 families, 252 nodes × 4 headings = 1,008 bins, and ≤ 20 bins per single feature;
  - the even/odd split, test tolerances, `NUM_WORKERS` = 12 and 3 games per worker.
- **Citations and links (about 47):**
  - all 15 arXiv IDs: titles, first authors and years match;
  - Goodfire essay: author Nick Cammarata, dated 2026-10-15; the quotes "roughly 90% of neuron poles have one main job", Qwen3-32B, InceptionV1 and ConvNeXt are all in it;
  - the Greydanus et al. quote is verbatim from the PDF;
  - the Mott et al. "scans through possible paths … no … ghosts ahead" claim is in the PDF;
  - DuPlessie 2024 is an SAE on a Ms. Pac-Man DQN, with steering only mentioned as future work;
  - Bekkemoen & Langseth use NMF concepts and include Ms Pacman;
  - jev_deep_rl documents RAM[1:5] bit 7 and RAM[116] `& 63`; its commit 3f69ca3a is dated 2026-09-20 in UTC;
  - OCAtari and AtariARI RAM addresses match the source;
  - the DOIs, Nature, Distill, Transformer Circuits, LightGBM and JSTOR links all resolve;
  - Sample Factory's "There is no Windows support at this time";
  - envpool `max_episode_steps` = 108000 at the linked commit;
  - ALE v0.8.1 gym.py has `max_num_frames_per_episode` = 108_000.
- **Library and PyPI claims (13):**
  - sample-factory 2.0.0 was released 2022-12-01 and 2.0.3 on 2023-02-09; 2.1.1 requires gymnasium;
  - ale-py 0.8.1 was released 2023-02-17;
  - gym 0.26.2's `atari` extra requires `ale-py~=0.8.0`;
  - OCAtari ≥ 1.1.5 through 2.2.1 all declare `numpy<2.0.0`, while 1.1.2 and 1.1.3 do not pin numpy (I checked the sdists);
  - the versions in uv.lock match the README's Technologies list.
- **Hugging Face (20):**
  - model-card scores and `cfg.json` values: `train_for_env_steps` 2e9, `summaries_use_frameskip` true, frameskip 4, gamma 0.99, `use_rnn` false, `convnet_atari`;
  - `createdAt` dates 2022-10-20 and 2022-10-21, and the pinned revisions;
  - 36 milestone checkpoints for agent 1111;
  - the uploader's name, Edward Beeching;
  - the dataset card, its file listing and the collection.
- **UI and figures.** All 1,167 alive-unit image triplets referenced by site/data exist, and so does every figure linked from the README, paper and reports. The site's text about the alive threshold, one-job definition, receptive field and core matches the code.

## Fixes

| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| README.md:44 | "Holm p 0.0002 (the smallest value the permutation test can give)" | "Holm p 0.0002 (the floor of the 10,000-permutation test, 1/10,001, after Holm over 2 tests)" | `src/pacneuron/stats.py` (`paired_signflip_p`, n_perm=10000); `results/confirm_appo_1111.json` (raw p_one_sided 9.999e-05 for the positive control; Holm over 2 candidates gives 0.0002); the README's own table footnote at line 168 |

## Unverifiable or hedged claims

1. README.md:296-297, rollout disk use ("1.3–1.6 GB per agent per split", "0.4–0.7 GB" per agent for steering arms, "about 11 GB"). No result file records sizes, and I cannot reproduce them without the bulk data.
2. README.md:306-307: "A full run per agent takes a few hours, dominated by the null-unit steering arms". The collect JSONs show about 2–4 min per collection split, but the steering-arm timings are not recorded.
3. README.md:305: "about 16 CPU threads recommended". This is a recommendation with no evidence behind it.
4. reports/00_summary.md:214: Sample Factory PR #203 "merged 2022-10-22". The GitHub API and web access to alex-petrenko/sample-factory were blocked in this session.
5. reports/00_summary.md:188-189 (erratum 16): the GitHub push-log times (06:16, 07:03 and 07:35 local time). These cannot be checked from the repository.
6. reports/02_ram_ground_truth.md:59 and paper section 6: "the 1.1.5 source distribution also failed to build in our environment". This reports the authors' own environment. I confirmed that the 1.1.5 sdist pins `numpy<2.0.0`, but I did not attempt a build.

## Problems found but not fixed

1. The README models table, and the same table in reports/00_summary.md, shows agent 2222's model-card score as "9056 ± 2544". The card says 9056.50 ± 2544.32. `report.models_table` formats the mean with `f"{x:.0f}"`, and Python rounds half to even, so it prints 9056. Conventional rounding would give 9057. The difference is cosmetic and the table is generated. I could not regenerate it, because the `report` phase needs torch, whose CUDA 13.0 wheel is over the 1 GB download limit, so I left both the generator and the table unchanged rather than hand-editing a generated block.

## Hugging Face card

- **Model cards.** The three linked models, `edbeeching/atari_2B_atari_mspacman_{1111,2222,3333}`, are third-party. Their cards report mean_reward 6288.00 ± 1954.58, 9056.50 ± 2544.32 and 6808.00 ± 1183.09. These match `src/pacneuron/config.py` and the README table, apart from the rounding note above.
- **Dataset card.** The repository's copy is the `CARD` string in `src/pacneuron/hf_publish.py`, with `{GITHUB}` and the agent list expanded. The hosted card at `hf://datasets/BurnyCoder/mspacman-appo-neuron-atlas/README.md` (1,940 bytes) matches it verbatim. The hosted file listing (results/*.json, site_data/*.json, analysis/audit_*.npz and screen_*.npz) matches what the card describes. There is no drift and no upload is needed.

## Regenerated artifacts and tests

- I changed no code, so I ran no tests.
- I did not regenerate the `report` phase or `paper/paper.pdf`:
  - my one edit is hand-written README prose outside any generated marker or block, so no derived artifact goes out of sync;
  - `paper/paper.md` was not edited, so the PDF needs no rebuild;
  - the `report` phase needs torch, and `uv sync` would download CUDA 13.0 wheels over the 1 GB limit, so I did not run it.
