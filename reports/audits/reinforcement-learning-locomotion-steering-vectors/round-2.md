---
repo: BurnyCoder/reinforcement-learning-locomotion-steering-vectors
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 220
fixed: 1
unverifiable: 1
not_fixed: 0
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/reinforcement-learning-locomotion-steering-vectors, round 2

## Summary

I checked claims independently, in this order: README, paper, docs, reports, Hugging Face card, explorer UI. Earlier audit and fact-check files were not used as evidence. Numbers were recomputed with short scripts that read the committed result files:
- `reports/*/results.json` (HalfCheetah 001–004 and Ant 005)
- `reports/ant-classic-005-independent-audit/audit.json`
- `reports/ant-publication/evidence.json`
- the committed `vectors.npz` files
- the explorer episode shards under `site/data/episodes/`

Everything below matched its source:
- **Ant tables.** Every number in the README and paper Ant confirmation tables (6 arms × effect, interval, speed retention, squared-action change, failures, gate) and in the README audit table (8 arms).
- **Prose figures.** Mean shifts, rewards, the 19/20 positive pairs, rank 0.05 against 99 random directions, shuffle rank 0.40, S2 +0.034 [-0.032, 0.104], M1 rank 0.21, M2 +0.903 [0.816, 0.998], and the clipping counts 8444/53409 and 2801/18000.
- **HalfCheetah.**
  - Window and pass counts: 564/576 windows; 0/24 primary and 8 control passes in 002; 0 primary and 2 control passes in 003; 6/12 primary passes out of 72 in 004.
  - 004 confirmation: the -0.02 result, its table, and the even/odd split.
  - Maximum speed gain +0.40% across 238 settings.
- **Seeds and provenance.** Seed partitions, manifest commit hashes and software versions.
- **Gate thresholds and estimator details** in `analysis.py` and `experiment.py`: quartiles, at least 8 episodes, 5 speed bins, bootstrap seeds 710/720, 2000 resamples, every tenth observation for the action bias.
- **Control cosines:** +0.60, +0.58 and -0.83.
- **Upstream checkpoints.** I downloaded the pinned checkpoints (about 4 MB each) and read the ZIP `data` JSON without unpickling. Archive SHA256, seed 0, num_timesteps 5.92M/8.77M, lr 3e-4, gamma 0.99, batch 256, buffer 1e6, and obs/action shapes 17/6 and 105/8 all match.
- **Citations.** arXiv metadata matches for CAA (2312.06681, Panickssery et al., 2024 revision), Mini et al. (2310.08043), Policy Gradient Steering (2607.27574), Chung & Romano, Phipson & Smyth, Myllymäki et al., and Ritzwoller/Romano/Shaikh. The Minari pages confirm SAC 10·10⁶ and TQC 6·10⁶ training steps. The upstream train/upload script line ranges are correct. The Baukit commit date (22 Feb 2024), MIT classifier and absence of a LICENSE file match. Line anchors into SB3, sb3-contrib, Gymnasium, MuJoCo and the PGS repository all resolve.

I found one unsupported claim and fixed it. The repository's documents are otherwise accurate against its data.

## Fixes

| file:line | before | after | evidence |
| --- | --- | --- | --- |
| docs/publication/independent.md.in:69 and generated reports/ant-classic-005-independent-audit.md:119 (+ PDF) | "...no error message; the stop is attributed to a MuJoCo memory-allocation failure, a cause those logs do not record." | "...no error message, so the cause of the stop is not established; an earlier attribution to a MuJoCo memory-allocation failure has no saved evidence." | reports/ant-classic-005-independent-audit/20261016T142559607453Z.log (12 workers, ends at "random000 (7/124)" with no error) and 20261016T142815485407Z.log (resumed with 6 workers). No file in the repository records a memory error. |

## Unverifiable or hedged claims

- **Cause of the first audit collection stop.** The "MuJoCo memory-allocation failure" has no saved log or artifact behind it. It is now stated as not established (see Fixes).
- **Not checked.** Historical execution claims about past runs on native Windows (smoke-rollout timing, earlier test counts, movie replay correspondence) depend on records from earlier sessions. I did not re-run models, so I neither confirmed nor counted them.

## Problems found but not fixed

None.

## Hugging Face card

I read the hosted card `hf://models/BurnyCoder/rl-locomotion-steering-vectors/README.md` and compared its bytes with `docs/huggingface-model-card.md`. They are identical, and its numbers match the result files (19/20 positive pairs, norm 0.51513 at strength -0.1, both checkpoint SHA256 values). No upload is needed. The card does not contain the edited sentence.

## Regenerated artifacts and tests

- **Full publication build not run.** `scripts/build_ant_publication.py` would have to restore 6,567 missing raw inputs (about 1.75 GB), which is over the 1 GB download limit.
- **Documents re-rendered instead.** I called `publication.documents.render_documents` directly on the committed `reports/ant-publication/evidence.json`, with ReportLab invariant mode.
  - Before any edit, a dry run into a temporary directory reproduced all 9 document outputs byte-for-byte, including both PDFs.
  - After the template edit, the same call regenerated `reports/ant-classic-005-independent-audit.md` and `.pdf`. No other output changed.
  - The template does not feed into `evidence.json` or the figures, so they stay in sync.
- **Tests.** `uv run --no-sync pytest -q tests/test_ant_publication.py tests/test_ant_publication_documents.py tests/test_build_paper.py tests/test_ant_site.py`: 41 passed.
