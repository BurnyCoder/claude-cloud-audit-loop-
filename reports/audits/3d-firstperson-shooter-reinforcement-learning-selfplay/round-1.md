---
repo: BurnyCoder/3d-firstperson-shooter-reinforcement-learning-selfplay
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 320
fixed: 5
unverifiable: 6
not_fixed: 3
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/3d-firstperson-shooter-reinforcement-learning-selfplay, round 1

## Summary

I worked through README, the Stage A paper (`reports/duel-fixed-v1/paper.md` and its PDF), the confirmation, egocentric, action-mode, duration/entropy, deferred-5v5, performance, verification and publication reports, the docs (`architecture`, `duel-protocol`, `protocol`, `sources`, `shooter-rl-design-review`, `evidence-index`, `experiment-plots`, `learning-audit`, `acceptance-stage-a`, `media/README`), all 15 Hugging Face cards, the UI strings and a sample of code comments.

I recomputed numbers with scripts that read the committed raw records. These include all 24 confirmation endpoints (12,336 round rows), the per-seed and median scores, the Student-t intervals (t(0.975, 2) = 4.3027), 773/780 eliminations, trainer times and rates, and the 2,001 finite optimizer rows. They also cover the pilot, action-mode, duration/entropy and egocentric analyses, the calibration cells, the ten legacy throughput probes (recomputed from `timings.jsonl`) and the live GPU telemetry. The rest were the deferred-5v5 frames, wins and rounds, the firing fixture (194 to 381 of 512), the resume audit, the publication receipts (15 repos, 150 files, 17 collection items), the 9 native replay parities, video metadata (ffprobe and SHA256), the power values (Monte Carlo noncentral-t) and the 108-test and 10-page receipts. Every recomputed number in README, the paper and the reports matched the data. The paper PDF is in sync with paper.md: every decimal and thousands-grouped number in the .md appears in the PDF text.

Method and code claims matched the code: 2x128 tanh actor, 2x256 tanh critic, 192 = 4x48 inputs, heads 9/5/5/2/2, the R0/R1/R2 formulas, 50/50 snapshot sampling with 8 historical candidates, smooth-L1 ClipPPOLoss, the pre-clip gradient norm, and the duel geometry and rules. Pinned versions in uv.lock (torch 2.14.1+cu130, torchrl 0.14.1, etc.) also matched.

Citations: I fetched 10 arXiv IDs (titles and authors match), the Sample Factory paper and supplement (Figure A.1, Table A.4, 8-agent population, 2.5e9 frames), FTW arXiv v1 (84x84 input, 540 actions, V-trace, PBT), DodgeBall.yaml at b2915bd (3x512, ratio 0.5, window 100), the DodgeBall README (Release 18), the Unity blog, the MA-POCA abstract, the GitHub CLI changelog, PyTorch issue 166628, the vizdoom_ppo_rnd README and the TorchRL MAPPO tutorial. I also checked all 106 external URLs (all resolve; github.com and ffmpeg.org could only be confirmed through raw/WebFetch because of proxy limits) and all 1,311 relative Markdown links (one broken code path).

Errors found were few and minor: one nonexistent file path, one inconsistent count, one misleading attribution, one overstated "adapted from" source claim, and one imprecise time. No result data was edited.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| docs/architecture.md:17 | "`sim/observations.py` is authoritative" | "`sim/observation.py` is authoritative" | `src/ministrike/sim/observation.py` (no `observations.py` exists) |
| reports/README.md:7 | "takeover/hand-back and eight exact replay checks" | "nine exact replay checks" | `reports/duel-fixed-v1/confirmation/native/parity.json` (9 captures, all `exact_parity: true`) |
| docs/learning-audit.md:30 | "[The author's PPO+RND Doom repository]" | "[A third-party PPO+RND Doom repository (callumhay/vizdoom_ppo_rnd)]" | https://raw.githubusercontent.com/callumhay/vizdoom_ppo_rnd/HEAD/README.md (supports 6M steps/8 h RTX 3080, <1M basic, seed 42) |
| docs/protocol.md:39 | "engineering starting values adapted from the TorchRL MAPPO tutorial" (implies the listed values come from it) | same text plus a dated fact-check note: only lr 3e-4, clip 0.2 and grad-norm 1.0 match; the tutorial uses 30 epochs, minibatch 400, gamma 0.99, lambda 0.9, entropy 1e-4 | https://docs.pytorch.org/rl/stable/tutorials/multiagent_ppo.html |
| README.md:61 | "original 09:30 UTC training ... boundaries" | "original 09:30:52 UTC training ... boundaries" | `docs/amendments/2026-10-23-duel-calibration.md`, `reports/duel-fixed-v1/calibration/selection.json` (start 23:30:52.627932Z) |

## Unverifiable or hedged claims

- `docs/media/README.md`: the video was "captured ... at 12:29:52 UTC". `docs/media/evidence/capture.json` gives 12:29:52.119Z as the session `started_utc`, and the same README says recording "starts during an already running session". So the exact capture start cannot be confirmed from the files. Frames, fps, size, duration, codec, resolution and hash were all verified.
- User-reported Codex restarts as the cause of the legacy interruptions (`reports/performance/summary.md`, paper): already hedged in the text. No primary record proves the cause.
- Native verification statements (F-key aliases, WASD/mouse not delivered, wireframe F10 capture): screenshots and replays exist, but the physical-input narrative cannot be checked headlessly.
- Historical test counts "full local suite 75 passed" (`docs/review-stage-a.md`, calibration amendment) and "90 existing passing correctness tests" (action-modes report): these were earlier revisions with no committed receipts. The release receipt (108 passed) was verified.
- Windows CI pass statements for specific revisions: I could not query GitHub Actions for this repository from this session.
- FFmpeg encoder build string and the GitHub attachment player behavior (`docs/media/README.md`).

## Problems found but not fixed

- The six pilot and diagnostic cards (`reports/publication/cards/ministrike-duel-fixed-v1-{pilot-r0,pilot-r1,pilot-r2,diag-duration-r1,diag-entropy-r1,diag-ego-r1}-seed5201.md`, which match the Hub copies) say "Final-test status: **pending**". These models are never final-tested by protocol, and each card's own release assessment says `final_test_not_accessed_for_this_model`. Fixing this needs a change to the card generator (`src/ministrike/experiments/duel_card.py`) and a Hub re-upload. I left it so the repository copy stays identical to the Hub.
- `src/ministrike/sim/constants.py:31` comment "initial hit points for all ten actors" is legacy-5v5 wording. The duel has two actors. It is a code comment only, so I made no change.
- Tests and ruff were not run (see below).

## Hugging Face card

I read all 15 hosted cards (`BurnyCoder/ministrike-duel-fixed-v1-seed5101/5102/5103`, `...-pilot-r0/r1/r2-seed5201`, `...-diag-duration/entropy/ego-r1-seed5201`, `ministrike-fixed-seed111/222/333`, `ministrike-selfplay-seed111/222/333`) and diffed them against `reports/publication/cards/*.md` with CRLF normalized. All 15 are byte-identical in content, so there is **no drift** and no upload is needed. Card numbers I spot-checked against raw data all matched: 5101/5103 final-test breakdowns, the 0.415365 mean and its interval, 5,464,064 steps and 667 updates, pilot R0 validation summary and improvement 0.01237, and the checkpoint SHA256s. If the "pending" wording above is fixed in the generator later, upload with, for example, `huggingface-cli upload BurnyCoder/ministrike-duel-fixed-v1-pilot-r0-seed5201 reports/publication/cards/ministrike-duel-fixed-v1-pilot-r0-seed5201.md README.md`.

## Regenerated artifacts and tests

- Only Markdown prose changed. No figure, table, JSON or paper.md content changed, so no regeneration was needed. `reports/duel-fixed-v1/paper.pdf` was not touched, and its text still matches paper.md.
- No code changed, so tests were not required. They also could not run: there is no `.venv`, and `uv sync --locked` would download the PyTorch/CUDA stack (well over 1 GB).
