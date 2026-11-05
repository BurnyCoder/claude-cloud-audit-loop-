---
repo: BurnyCoder/3d-firstperson-shooter-reinforcement-learning-selfplay
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 221
fixed: 1
unverifiable: 1
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/3d-firstperson-shooter-reinforcement-learning-selfplay, round 2
## Summary

I checked the README, the Stage A paper (`reports/duel-fixed-v1/paper.md`), the confirmation report, `docs/sources.md`, `docs/shooter-rl-design-review.md`, `docs/experiment-plots.md`, `docs/media/README.md`, the native-replay README, the publication README, the legacy hardware summary and the seed 5101 Hugging Face card. I did not use earlier audit files as evidence. I recomputed every number with scripts that read the committed result files: the 24 confirmation endpoint JSONs, `metrics.jsonl`, `selection.json`, `evaluation-receipt.json`, the pilot `assessment.json` files, the action-mode, duration/entropy and egocentric `analysis.json` files, the calibration `selection.json`, the performance `sweep.json` receipts, the deferred 5v5 metrics, `power.json` and `publication/verification.json`.

All checked numbers match their result files, including rounding and the Student-t intervals (recomputed with SciPy). That covers per-seed scores, the mean improvement 0.415365 with CI [0.412130, 0.418599], the stochastic interval, medians, 773/780 eliminations, 12,336 round records, 144 traces, trainer times, the power values 0.908489/0.470749/0.179255, all seven exploratory contrasts and their intervals, all ten legacy throughput values (reproduced by the documented interval reconstruction), the nine duel calibration cells, the deferred 5v5 exposures, and the counts of 135, 33, 23, 11 and 7 PNG/SVG pairs.

Method claims match the code and the run configs: the 2x128 tanh actor, the 2x256 critic, 192 = 4 x 48 inputs, heads 9/5/5/2/2, Adam 3e-4, clip 0.2, 3 epochs, gamma 0.999, lambda 0.95, the 14 m arena, 6 m spawns, 20 Hz, 20 s rounds, and the rifle constants. The table entry "CUDA learner / CPU frozen opponents" is correct: `inference_device=cuda` places only the learner's rollout network, and `SnapshotPool` always runs opponents on CPU. External citations match the fetched primary sources: arXiv metadata for nine papers, the Sample Factory main paper and supplement (Figure A.1, Table A.4, 2.5e9 frames per agent), FTW v1 (84x84 input, 540 actions, V-trace), the DodgeBall YAML at b2915bd (3x512, ratio 0.5, window 100) and the Unity blog (hybrid actions, raycasts, attention).

One README claim had no evidence: the GPU driver version. I hedged it.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| README.md:77 | "The GPU path was tested with an RTX5070 Laptop GPU and driver591.74." | "...tested with an NVIDIA GeForce RTX 5070 Laptop GPU, as recorded in the hardware-probe summary; the GPU driver version is not recorded in the committed evidence." | GPU name: `reports/performance/summary.md` and the probe receipts. Driver 591.74 appears in no committed log or receipt (`git grep` matches only coincidental numbers in metrics). |

## Unverifiable or hedged claims

- GPU driver 591.74 (README:77). No committed evidence records it, so I hedged it as above.
- Paper and performance summary: "user-reported restarts" and the WMI process-tree explanation. These are already labelled in the text as user-reported and not independently verified, so I left them as written.
- I could not check from a CPU container that the GitHub user-attachment video URL is identical to the committed MP4. The committed MP4 does match its stated SHA256, 24.0 s duration, 716 frames, 1280x720 resolution and H.264 codec.

## Problems found but not fixed

- README:42-44. The controls paragraph says "E interacts", "Team 0 attacks and team 1 defends" and mentions "bomb state". These apply only to the legacy 5v5 bomb mode. In `duel-fixed-v1` the interaction head is removed (`MatchSpec.action_nvecs`) and there is no attack/defence role. The text is ambiguous rather than false, so I left it. Small spacing typos ("with16", "Deferred5v5") were also left, because they are not factual errors.
- Not checked within budget: `docs/protocol.md`, `docs/duel-protocol.md`, the amendment files, the deferred-5v5 and verification reports, the performance paper, 14 of the 15 Hugging Face cards, and the library-documentation URLs (PyTorch, TorchRL, Matplotlib, NumPy, Python docs). A later round should cover them.

## Hugging Face card

I read `hf://models/BurnyCoder/ministrike-duel-fixed-v1-seed5101/README.md` with `hf_fs`. It is byte-identical to `reports/publication/cards/ministrike-duel-fixed-v1-seed5101.md`: 6,123 bytes, SHA256 `a3dd4808...d593`, the same hash `reports/publication/verification.json` records. The card's numbers (final test 0.75; scripted 0.25 with side scores [0.5, 0.0]; CI [0.41213, 0.41860]; checkpoint hashes; architecture; arena rules) match `confirmation/data/seed5101/final_test.json` and `analysis.json`. No drift, so no upload is needed. The other 14 cards were not compared.

## Regenerated artifacts and tests

Only one README sentence changed, so no generated artifact depends on it. I did not regenerate the paper PDF or the figures, and none needed it. I touched no code, so I ran no tests. Installing `torch` for the project environment would have required a large download, so I did the recomputation with an isolated `uv run --no-project --with numpy --with scipy` environment.
