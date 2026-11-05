---
repo: BurnyCoder/training-facts-into-llms
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 180
fixed: 0
unverifiable: 3
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/training-facts-into-llms, round 2

## Summary

I checked the claims independently, in priority order: README, both active paper editions (`papers/qwen38-minimal`, `papers/qwen35-revised`), `docs/training-strategy.md`, `reports/qwen38/CLAIMS_AND_SOURCES.md`, the numbers in `docs/qwen38-runpod.md`, `reports/INSTRUCTION_AUDIT.md`, the run table in `reports/EXPERIMENTS.md`, the static explorer text (`site/`) and the hosted Qwen3.8 adapter card. I did not use earlier audit files as evidence.

Every checked claim matched its evidence, so I made no edits. The branch has no new commits and nothing was pushed. Round 1 (PR #51) appears to have left these surfaces consistent. The budget ($3 soft cap) ran out before I could cover the rest of the 1,613-line `reports/EXPERIMENTS.md`, `reports/runs/*.md`, `docs/security-and-publication.md`, `docs/reproducing-experiments.md`, `docs/interactive-inference.md` and code docstrings line by line.

How the checks were done:
- **Numbers.** Scripts read `reports/manifest.json`, the eight historical `reports/evaluation-*.json` files, `reports/qwen38/manifest.json` and the Qwen3.8 `evaluation.json`, and recomputed the claims from them. This covered:
  - every README table cell and the summary block
  - acceptance checks, lost-control and false-positive IDs, and recall-miss outputs
  - selected checkpoints and steps, the selection-score to eval-loss inversion, and Trainer runtimes
  - trainable counts (186 modules and 5,411,328 or 10,822,656 scalars for Qwen3.5; 496 modules, 992 tensors and 58,363,904 scalars for Qwen3.8)
  - Git-gate path counts (36/38/44/45), data row counts (56 = 24+16+16; expanded 104 rows and 390 steps), seed 42 and the shared device, the stop-on-perfect behaviour of both semantic runs, and the Qwen3.8 checkpoint trajectory
  - all manifest SHA-256 bindings, which matched
- **Primary sources fetched now:**
  - arXiv API metadata for 2106.09685v2, 1909.12434, 2108.02497v5, 1807.03341v2 and 2402.11078v3
  - ACL Anthology BibTeX for 2024.findings-acl.352 and 2024.emnlp-main.444
  - the Gangadhar and Stratos PDF: LoRA in the main results, separate experiments without LoRA and with only layers 3–5 updated, 15 nearest facts by Sentence-BERT, GPT-2 XL, and no gain from DPO
  - the upstream `model-editing-ft` `run.py` (AdamW over `model.parameters()`) and `execute.sh` (gpt2-xl, 2.2e-5, 50 epochs)
  - the pinned Qwen3.5-0.8B and Qwen3.8-27B model cards: both are causal LMs with a vision encoder
  - the pinned Qwen3.8 `config.json` (`Qwen3_5ForConditionalGeneration`) and safetensors index (1,199 tensors, 15 `mtp.*`)
  - the Hub safetensors API (BF16, 27,781,427,952 parameters)
  - the commit-pinned Qwen3.8 release log (news entry for 2026-08-14 at line 48)
  - the uv 0.11.27 installer, which redirects to the GitHub release asset
- **Arithmetic** in CLAIMS_AND_SOURCES and the RunPod guide: 27,781,427,952 − 424,699,392 + 58,363,904 = 27,415,092,464; 10 h × $1.59 = $15.90; 8 h × $0.44 = $3.52.

## Fixes

| file:line | before | after | evidence: result file path or URL |
| --- | --- | --- | --- |
| (none) | — | — | No checked claim was wrong, unsupported or out of sync with its evidence. |

## Unverifiable or hedged claims

1. The interruption reason for the positive-only `expanded` attempt ("user narrowed the active objective"). The manifest itself says this comes from conversation context, not from the log. The repository already presents it with that hedge.
2. The Qwen3.8 runtime-prepare and first-preflight timings in `reports/qwen38/CLAIMS_AND_SOURCES.md` (ninja 1.10 s, install 483 ms, about 1.78 s logger boundary). These were transcribed from ignored private logs that are bound only by hash. The repository already labels them as transcriptions.
3. Operational-log SHA-256 values and Git-gate details in `reports/manifest.json`. The logs are untracked, so the hashes cannot be re-derived. The manifest's `provenance_note` already says so.

## Problems found but not fixed

None in the repository content.

Environment notes, not repository defects:
- In the shallow clone that was provided, `results check` reported `site/results.json` as stale. The cause is that the generator pins source-link commits from Git history. After `git fetch --unshallow` the check passed with 0 files updated. I reverted the temporary regeneration.
- `uv sync --frozen` downloads CUDA PyTorch wheels, which exceeds the 1 GB download limit. I stopped it and ran the CPU-only results commands in a small venv with `PYTHONPATH=src` instead.

## Hugging Face card

The repository has no checked-in copy of any Hugging Face card; cards are rendered by the publishing code. So drift between a repository copy and the Hub is n/a.

I read the hosted card for `BurnyCoder/qwen3.8-27b-atemokoloporos-20260831t003823434344z-qwen38-minimal-bf16-59f2f6ff` with `hf_fs` and compared it with `reports/qwen38/manifest.json` and `evaluation.json`. Everything matches:
- base revision `1d4bf0f…`
- baseline 0/12, 8/8, 8/8
- post-training 11/12 (91.7%), 8/8, 8/8
- acceptance TRUE
- interpretation `candidate-knowledge-acquisition`

No upload is needed.

## Regenerated artifacts and tests

- `results check` passed after unshallowing: "0 generated files updated". This confirms that the README result blocks, `docs/assets` charts, `reports/ALL_EXPERIMENTS.md`, the active-paper generated values, tables and figures, and `site/results.json` are consistent with the admitted evidence.
- I changed no code, so I did not run pytest or ruff.
- I did not rebuild the paper PDFs: no inputs changed, and LaTeX is not installed.
