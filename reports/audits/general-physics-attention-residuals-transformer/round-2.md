---
repo: BurnyCoder/general-physics-attention-residuals-transformer
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 462
fixed: 0
unverifiable: 10
not_fixed: 0
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/general-physics-attention-residuals-transformer, round 2

## Summary

I audited the repository independently, without using the round-1 branch or any earlier audit files as evidence. I found no factual errors, so I made no edits, created no commits and pushed nothing. Branch `fact-check/2026-11-05-r2` is the same as `origin/main` (6d31099).

How the claims were checked:

- **Numbers.** I recomputed headline and table values with short scripts that read `reports/*.csv`, `reports/*.json` and `reports/untrained/*.csv`. These cover:
  - the radiative headline (0.28917, 26.38%, 30.99%) and the nine-model ranking (smallest initialized mean is 0.41310);
  - the means on shared seeds 0–2 (0.29203, 0.40246, 0.31735, 0.34735) and the seed-0 case where Full beats Block;
  - the primary effect, recomputed from `metrics.csv`: 24.52%, 95% CI 11.56–35.58%, exact p = 2/64 = 0.03125, with all six effects negative;
  - every value in the README and paper accuracy tables, plus the intervention tables and ratios (2.565, 7.490, 2.630, 9.524; minimum per-seed ratio 1.62);
  - the physical diagnostics (negative-density fraction 26.04% vs 27.30%; divergence error 4.134 / 2.823 / 0.228);
  - the trained-vs-initialized ratios (3.671, 13.812, 3.211), checked for direction in every seed, and the Full/Block (0.8349) and Uniform/Block (1.0238) geometric ratios;
  - costs (mean wall time, throughput, memory), the GPU ledger totals (11.068 h training, 12.208877 h total, 1.119727 h evaluation, 11.745949 h before the extension, 2,364.4755 s / 80.6 min), the profiling medians and the 14.400 h projection;
  - power values (0.37124, 0.11563) and the 0/1368 undefined windows;
  - 36 per-run trained report values and 108 per-run initialized report values;
  - 90 values in the paper's accuracy and cost tables.
- **Method claims.** I compared these against `configs/study.json`, `reports/frozen_protocol.json` and the source code:
  - architecture: 12 layers, width 192, MLP 768, 3 heads, 1×16×16 patches, 128 tokens; parameter counts 7,919,045 and +9,600 (= 25×2×192);
  - optimizer and schedule: AdamW (0.9, 0.999, 1e-8), learning rate and weight decay 1e-4, gradient clip 1, 5% warmup, cosine to 1e-6, dropout 0;
  - data: 3,175 updates, microbatch 4, effective batch 16; uniform sampling over dataset, parameter, trajectory, stride and start;
  - normalization with a population SD and a 1e-6 floor; physical diagnostics computed in de-normalized units;
  - intervention RNG seed 20261025; the upstream `differentiate(x)+x` forward that never uses the integrator or `step_size`;
  - the SetThreadExecutionState flags 0x80000001;
  - data manifest facts: 36 files, 240 trajectories, 120/15/15 and 72/9/9 splits, 512×128 and 128×384 stored grids, 200 and 101 frames, about 38.607 GB, 33 initial-state groups (25 + 8), and every held-out trajectory sharing an initial state with training.
- **Citations and links.** Fetched now:
  - arXiv 2509.13805 (Wiesner, Gray, Wessling, Baek; v4 2026), 2603.15031 (Kimi Team, 2026), 2412.00568 (Ohana et al., NeurIPS 2024 Datasets and Benchmarks), 2003.08390, 2108.02497 and 1807.03341 all match their bibliography entries.
  - Crossref metadata for the Dedalus DOI (PRR 2, 023068) and the Fielding et al. DOI (ApJL 894, L24) matches.
  - The Well v1.1.0 release notes support the uniform-grid and Chebyshev-coordinate statement.
  - The Well API page carries the shear_flow v1 duplication warning. Issue #94 and discussion #8 support the download-limitation sentence.
  - The PyTorch 2.14 AMP page supports the claim that explicit FP32 casts do not stop autocast. The AttnRes paper (Eqs. 2–6) supports zero-initialized pseudo-queries giving an equal-weight start, RMSNorm on keys, and b0 = token embedding.
  - Fast-AttnRes needs CUDA BF16 and Triton; Liger's `attn_res.py` uses Triton kernels; the MoonshotAI repo has no training package.
  - The Well dataset cards confirm Athena++ (radiative, 9 t_cool values, 101 steps) and Dedalus (convection, 512×128, 200 steps, 50 trajectories per parameter setting).
  - The vendored FLA `naive.py` is byte-identical to upstream at the pinned commit, and all 15 hashes in `vendor/provenance.json` match the local files.
  - All relative Markdown links resolve to tracked files. Every non-GitHub external URL returned HTTP 200, except the APS DOI, which returns 403 to bots but resolves correctly through the DOI handle API.
- **Visuals and UI.** All six GIFs decode to 24 frames at 200 ms. All four MP4s have 24 frames at 6 fps. `paper/main.pdf` and `site/paper.pdf` are identical and have 21 pages. The page anchors the README links to (`#animations`, `#comparison`, `#controls`) exist in `site/index.html`. The site's `study.json` headline, GPU hours and primary analysis match the reports.

## Fixes

| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| (none) | No factual errors found | No changes | See Summary |

## Unverifiable or hedged claims

These claims depend on local logs, private state or actions that cannot be checked from the repository or the public web. I left them unchanged.

1. That the Hugging Face collection `BurnyCoder/gphyt-attention-residuals-6adee5fe6ceb5f9ae1ccb873` contains all four model repos. The `hf_fs` tool returns "private or inaccessible" for it. I did confirm separately that the four model repos hold 18 trained and 18 initialized safetensors checkpoints (6+6, 6+6, 3+3, 3+3).
2. Historical CPU test counts and timings, for example 44 passed in 21.77 s, 42 and 43 passed, and 16 passed in 3.19 s (`reports/development.md`, `reports/architecture-audit.md`, `reports/final-verification.md`). The logs are under the off-repo `STUDY_ROOT`.
3. The numerical probe differences in the architecture audit (3.58e-7, 4.53e-6, 2.27e-6, 0.005163431) and the "CPU dispatch trace observed BF16 contractions".
4. "The study used [aria2] release 1.37.0" (`docs/data-preparation.md`).
5. The searches reported as finding no identical earlier GPhyT+AttnRes study and no uniform-grid Hugging Face mirror (`docs/sources.md`, `reports/development.md`). Both are already hedged as search results, not proof.
6. The AI authorship statement in `paper/main.tex` ("Codex wrote this codebase and paper").
7. "The Codex LaTeX editor can also compile and preview the source" (README).
8. Visual-inspection and browser-check statements (rendered pages, no console errors).
9. The PR merge times and GitHub Actions run outcomes cited in the reports. GitHub API access to this repository was not enabled for this session.
10. Anonymous Hub hash checks of all 18 checkpoints (`reports/final-verification.md`). The hosted file listings exist, but I did not re-hash the weights.

## Problems found but not fixed

None. Three observations that are not errors:

- The README H1 and `reports/radiative_highlight.json` title say Block "beats ... all other tested baselines on radiative flow". This is true of the arithmetic means. The README, paper, site and model cards all qualify it right away as a descriptive mean ranking, not a win in every seed (Full is better in seed 0), so I left it.
- The radiative grid is described as "128 × 384" (x/y). The Well card lists it as "384 x 128". The repository's order follows the stored coordinate lengths (x has 128 entries, y has 384), so it is internally correct.
- The paper says Uniform Block has "no learned routing parameters". The model does carry 9,600 frozen routing tensors (7,928,645 total, 7,919,045 trainable per `reports/frozen_protocol.json`). That is consistent with "no learned", and `reports/development.md` already discloses it.

## Hugging Face card

- The repository has no committed card file. Cards are generated by `src/gphyt_attnres_study/publishing.py` (`stage_release`), using `reports/radiative_highlight.json` for the headline.
- The hosted card `hf://models/BurnyCoder/gphyt-attnres-standard/README.md` matches the generator template text, including the post-hoc initialization section. The opening of the hosted `gphyt-attnres-block` card also matches.
- Card claims checked: architecture (12 layers, 192, 768, 3 heads, 4 frames, 128x64, 5 channels), 3,175 updates, seeds 0–5, the headline numbers, negative-density and persistence caveats, and the initialized-control statements. All are consistent with the result files.
- No drift was found, so no upload is needed. If the cards are ever regenerated, the command would be `huggingface-cli upload BurnyCoder/gphyt-attnres-standard path/to/card.md README.md` (likewise for `-block`, `-full` and `-uniform-block`).

## Regenerated artifacts and tests

- No files were edited, so I regenerated nothing. The paper PDF also cannot be rebuilt here, because LaTeX is not installed.
- No code was touched, so I did not run the test suite.
- No commits were made and nothing was pushed.
