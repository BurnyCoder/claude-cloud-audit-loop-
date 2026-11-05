---
repo: BurnyCoder/llm-reinforcemen-learning-for-software-engineering
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 112
fixed: 2
unverifiable: 4
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/llm-reinforcemen-learning-for-software-engineering, round 1
## Summary

I worked through the README first, then the paper's numeric macros and bibliography, then methodology, data/README, the reports and the hosted Hugging Face card. I stopped at about $2.6 of the $3 soft cap, so docs/guide.md, docs/security.md, docs/reproducibility.md and reports/experiments/001–002 got only spot checks.

I recomputed every headline number with a script that reads `reports/evidence/task-scores.json` and calls the repository's own `paired_bootstrap_interval` (10,000 resamples, seed 42). All matched `run-summary.json`, the README table, `paper/generated-results.tex`, the methodology text and the hosted card. The checked numbers were:
- validation +0.0625 [−0.1458, 0.2917], 7/12 → 8/12
- internal test −0.0042 [−0.2917, 0.2625], 5/12 → 6/12, 30/49 raw hidden cases for both models
- HumanEvalFix 37/164 → 38/164, +0.0061 [−0.0183, 0.0366], 3 improved, 2 regressed, 159 tied
- failures 21/60 → 6/60 (validation) and 23/60 → 10/60 (internal test); invalid 19 → 1
- peak training memory 1.72 GiB; trainable parameters 8,798,208 (1.7497%), which equals 7 LoRA modules × 24 layers at rank 16
- 336 tensors changed; 404 rollouts = 38 + 175 + 191
- external evaluation time 2,065.4 s vs 1,116.5 s, which is 1.85×

I also checked the Hub `results.json` at revision 5b6e22a4. Its task scores and intervals match the repository evidence.

Method claims match `configs/local-8gb.toml`, `training.py`, `reward.py` and `sandbox.py`:
- rewards −0.3, −0.15, −1.0, +0.1 and the +1.0 full-solve bonus
- `dr_grpo` loss, beta 0, `scale_rewards` none, top-k 0, masking of truncated completions, `save_total_limit` 2
- collapse stop when more than 80% of reward groups have zero variance for 20 logs
- the smoke configuration
- Docker flags: 32 PIDs, 128m memory, 0.5 CPU, 16 MiB tmpfs, UID 65532, 3 s timeout

The curriculum hashes, the uv.lock hash, the 36/12/12 split, the 59×4 + 1×5 hidden cases and the absence of public/hidden overlap all check out. The locked versions are torch 2.14.0+cu130, transformers 5.16.1, trl 1.12.0, peft 0.20.0, trackio 0.37.0 and hub 1.30.0.

External sources I fetched:
- **Qwen card at ea3f247:** 0.49B parameters, 24 layers, GQA, 32,768-token context, Apache-2.0.
- **DebugArena card at e4be134:** Qwen2.5-Coder-0.5B, 4 generations, lr 1e-5, Unsloth 4-bit loader, no reward function or dataset definition.
- **BigCode `humanevalpack.py` at 8fc5bae:** Python timeout 10 s, the "Fix bugs in" instruction, the NumPy import prelude.
- **HumanEvalPack card:** MIT license, OctoPack paper.
- **Trackio 0.37 docs:** `TRACKIO_SPACE_ID`.
- **Transformers v5.16.1 `training_args.py` L2115–2122:** ratio-valued `warmup_steps`.
- **Papers:** arXiv 2106.09685 (LoRA), 2107.03374 (Codex), 2402.03300 (DeepSeekMath), 2409.12186 (Qwen2.5-Coder), 2308.07124 (OctoPack), 2605.30478 (RLVR for small code models).
- **Old repository links:** every `github.com/BurnyCoder/llm-rl-software-engineering` link redirects to the renamed repository, and commits 7027bc5 and 902ca72 exist in its history.

The documentation is in good shape. I found only two defects.

## Fixes
| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| README.md:127-128 | "The immutable revision above [8dc6fa7d] was re-downloaded and this exact snippet returned a fenced `clamp_value` … `max(low, min(value, high))`" (no source) | Same claim, now attributed to `documentation-audit.json` with a note that its raw log is not tracked. Adds that `verification.json` records the same snippet at 5b6e22a4, and that both revisions have identical Safetensors LFS SHA-256 values (only README.md differs). | reports/evidence/verification.json; https://huggingface.co/api/models/BurnyCoder/qwen2.5-coder-0.5b-swe-rl/tree/5b6e22a4c6c01bec95d10e93a0fc78666eb9c543 and …/tree/8dc6fa7df8a09e157e3a5be1ec17b5d8b8aa4f43 |
| sandbox/Dockerfile:17 | `humanevalpack.py#L371-L375` cited for "harness prepends NumPy imports" (those lines apply diff patches) | `humanevalpack.py#L394-L397` (where `IMPORT_HELPER["python"]` is joined and prepended) | https://github.com/bigcode-project/bigcode-evaluation-harness/blob/8fc5bae6479c4fbbb28c3f8b644f6a15b3f3b5bd/bigcode_eval/tasks/humanevalpack.py |

## Unverifiable or hedged claims
- paper/llm-swe-rl-experiment.tex:128, "Four of 400 main-training rollouts were clipped … all by step 31". Tracked evidence supports 4 clipped steps, each at a 0.25 ratio, with none after step 50. "By step 31" requires `trainer_state.json`, which is not tracked.
- reports/experiments/003-main-100-step.md:50-53, the per-window loss-like column (0.05290, 0.01664, 0.00368, −0.00138). It is not in tracked evidence. The other columns of that table (reward means, zero-std counts 6/13/9/9 = 37, clipped counts 3/1/0/0) are consistent with run-summary.json.
- README.md:127-128, the specific `max(low, min(value, high))` output text at 8dc6fa7d. It is recorded only in an earlier audit file, now hedged as described in Fixes.
- I did not independently verify that the producing commit's `src/` matches what ran. run-summary.json records only an empty diff for the listed scope.

## Problems found but not fixed
- README.md:67-68, paper `\author` URL, data/README.md and others still use the pre-rename repository name `BurnyCoder/llm-rl-software-engineering`. All of these redirect to the current repository today, and `git clone` of the old URL creates the `llm-rl-software-engineering` directory that the next `cd` expects. I left them unchanged to avoid churn and because `run-summary.json` records the old URL. They would break if a new repository were ever created under the old name.

## Hugging Face card
I read the hosted card (`hf://models/BurnyCoder/qwen2.5-coder-0.5b-swe-rl/README.md`, main = 8dc6fa7d, which is the latest of three commits). The repository has no committed card file: `src/minibug_rl/artifacts.py::_model_card` generates the card, and its section structure matches the hosted card. Every number on the hosted card matches the repository evidence:
- pass@1 0.4167 / 0.5000
- hidden fraction 0.6083 / 0.6042
- observed sampled success@4 0.8333 / 0.8333
- −0.0042 [−0.2917, 0.2625]
- HumanEvalFix 0.2256 / 0.2317, timeouts 3 / 4, 0.0061 [−0.0183, 0.0366]
- sandbox digest, LoRA rank 16, alpha 32, lr 1e-05, seed 42

I found no drift, so no upload is needed. If you want to re-upload anyway: `huggingface-cli upload BurnyCoder/qwen2.5-coder-0.5b-swe-rl path/to/card.md README.md`.

## Regenerated artifacts and tests
- I did not edit the paper, so I did not regenerate the PDF (LaTeX is not installed anyway).
- I ran `tests/test_public_claims.py` in a minimal pytest venv: 5 passed. This is the README link and claim test.
- I did not run the full suite or mypy, because `uv sync` would download the CUDA torch stack. My only code-adjacent change is a comment in the Dockerfile.
