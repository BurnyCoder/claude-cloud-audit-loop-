---
repo: BurnyCoder/mamba-neuron-mechanistic-interpretability
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 480
fixed: 10
unverifiable: 9
not_fixed: 3
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/mamba-neuron-mechanistic-interpretability, round 1

## Summary
I checked every numeric claim in README.md, reports/paper.md (and its PDF), the four experiment reports, all_experiments.md, preregistration.md, docs/*.md, the HF dataset card and the viewer data. I recomputed each one with short scripts from the committed result files: h1.json, h2.json, h2b.json, h3_mechanism.json, truncation_survey.json, screen.json, screen_low.json, autointerp.json, candidates.json, domain_candidates.json, activation_shape.json, split_stability.json, vocab_summary.json, judge/steer_validation.json and benchmark.json. I also used the archived logs in reports/logs/ and the hosted `neuron_stats.parquet` (18 MB) for the per-neuron maxima and std. Method claims were checked against the code: phases/mechanism.py, mechanism.py, phases/steering.py, steer.py, autointerp.py, phases/atlas.py and publish.py. I fetched every arXiv ID (24), every DOI (4, through Crossref), the Goodfire essay, the Transluce page, the state-spaces/mamba README, the HF model configs, the tokenizer and HF `modeling_mamba.py`. Every other URL got an HTTP check.

The repository is very accurate. All results tables (README, paper Tables 1–6, the report tables) match the result files to the stated rounding. All 24 arXiv IDs resolve to the cited titles and first authors, and the Goodfire, Transluce and AxBench claims are supported by their sources. I found and fixed 10 claims: one wrong count, one wrong comparison, one overclaim, method imprecisions, an incomplete reference title, a misleading sentence and two dead links. No result data was edited, and no verdict changes.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| README.md:11 | "8 dated amendments; the 8th is an audit erratum" | "9 dated amendments; the 8th is an audit erratum and the 9th declares a deviation in the judge-validation rater and adds post-hoc analyses" | reports/preregistration.md (amendments 1–9); paper Appendix A |
| README.md:91 | DiffMean "has a lower harmonic mean than the neuron except for "as"" | lower for all three (0.16 vs 0.46, 0.19 vs 0.24, 0.15 vs 0.35); for "as" the difference is not significant | results/mamba-1.4b-hf/h2b.json `conditions.*.hm`, `posthoc_audit.p_clamp_vs_diffmean_holm` = 0.3726 |
| README.md:15 | viewer alt text: makes the model write "first" "in fluent text" | "with judged fluency near unsteered text" | h2b.json `posthoc_audit.noninferior_fluency_ci` = false for L37 N71; README/paper say fluency preservation not established |
| reports/paper.md:157 | "Re-run each firing with only the last k … tokens" | "Re-run the 50 strongest of these firings …" | src/mamba_neurons/phases/mechanism.py:21,46 (`N_TRUNC = 50`, `rows[:N_TRUNC]`) |
| reports/paper.md:159 | patching "at one random held-out position" | "at a single random held-out position (repeated over 200 such positions)" | phases/mechanism.py:49 (200 random rows/positions) |
| reports/paper.md:250 | "kept judged fluency within 0.1–0.2 of the unsteered level (0.5–0.8 vs 0.6)" | "within 0.2 of …" (differences are 0.0, +0.2, −0.1) | results/mamba-1.4b-hf/screen_low.json summary levels (0.6 / 0.8 / 0.5 vs 0.6) |
| reports/paper.md:470 | Lones (2021) "How to avoid machine learning pitfalls." | "…: a guide for academic researchers." | https://arxiv.org/abs/2108.02497 |
| reports/experiment_01_atlas.md:22 | "86% of neurons fire on their *positive* pole" | "86% of neurons are positively skewed: their rare large activations are mostly positive" | activation_shape.json `frac_positive_skew` 0.8555 (skew, not pole choice) |
| src/mamba_neurons/phases/common.py:23 | link https://pytorch.org/docs/stable/generated/torch.cuda.empty_cache.html (404) | https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.empty_cache.html | HTTP check |
| src/mamba_neurons/llm.py:44 | link github.com/ollama/ollama/blob/main/docs/faq.md (file moved) | https://docs.ollama.com/faq | the FAQ documents `keep_alive: 0` unloading the model |

## Unverifiable or hedged claims
Left unchanged because no result file, log or primary source in reach supports or refutes them:
1. experiment_01: "7.7 / 8.1 GB used" during the batch-16 memory spill. The log shows the 185 tok/s, not the memory.
2. experiment_01: mamba.py pscan "2.2k vs 3.6k tok/s" and "logits differed by up to 153". The report itself says these come from an agent transcript.
3. experiment_02: the first two rows of the labeller table (plain prompt). The report says they come from console output; only rows 3–4 are in labeler_comparison_smoke.json, and those match.
4. experiment_03 and preregistration amendment 4: judge latency "about 20 s to about 1.2 s" and parallel Ollama "1.55 vs 1.35 s/call".
5. reproducibility.md: the num_ctx 8192 vs 2048 spot check (described as unarchived), and the OS, driver and GPU strings.
6. all_experiments.md: qwen3.5:9b "quantized for llama.cpp" (not checked against the Ollama library page).
7. Paper and reports: the Goodfire essay "does not detail" its audit procedure. The 90% / Qwen3-32B / "preliminary audits" wording is verified; I did not read all 65 minutes of the essay to confirm the absence.
8. "Sunku Mohan et al." The arXiv metadata lists the author as "Mohan, Vamshi Sunku"; which part is the surname is ambiguous, so I left it.
9. HF `modeling_mamba.py` line-level structure. The current main branch was refactored; D-skip, gate and out_proj are confirmed, and the README pseudocode is consistent with them.

## Problems found but not fixed
1. reports/paper.md references list five works that are never cited in the body: Gao et al. 2020, Landis & Koch 1977, Lones 2021, Meng et al. 2022 and Phipson & Smyth 2010. Their metadata is correct, so this is an editorial decision for the author.
2. The regenerated reports/paper.pdf uses Liberation Serif and DejaVu fonts instead of Times New Roman and Consolas, because the Linux container lacks those fonts. It still has 21 pages and the same 5 images. Rebuilding on the author's Windows machine restores the original fonts.
3. reports/audit.md (an earlier audit) was not re-audited or used as evidence, per instructions. The README and reports link to it for post-hoc analyses whose numbers I verified independently from the result files.

## Hugging Face card
I read the hosted card for `datasets/BurnyCoder/mamba-1.4b-neuron-atlas` with hf_fs and compared it with the template `HF_CARD` in src/mamba_neurons/phases/publish.py, filled with the κ values from judge_validation.json and steer_validation.json (0.55 / 0.79 / 0.34). They are identical apart from line endings (CRLF on the Hub), so there is no drift. Card claims checked:
- 48 × 4096 = 196,608 neurons; the 2.32M / 0.65M token splits; the κ values; the parquet columns (checked against export_hf);
- the hosted file list (neuron_stats, poles and steering parquet);
- the licence links.

The collection link in the README resolves. No upload is needed. If the card is ever changed: `huggingface-cli upload BurnyCoder/mamba-1.4b-neuron-atlas path/to/README.md README.md --repo-type dataset`.

## Regenerated artifacts and tests
- reports/paper.pdf: regenerated with `scripts/build_paper.py` (pandoc + Playwright Chromium, run from a scratch venv with pypandoc and playwright 1.63.0). The new PDF contains all three paper edits.
- Figures and site/data were not regenerated: no data changed. The viewer data (site/data/index.json) matches h1/h2/h2b/split_stability/benchmark and all 468 pole labels and balanced accuracies in autointerp.json. figures/dose_response_h2b.png matches screen.json and screen_low.json.
- Code changes are comment-only (two URLs). `python -m py_compile` passes. I did not run the pytest suite: it needs the CUDA torch install and a 0.5 GB model download, and nothing executable changed.
