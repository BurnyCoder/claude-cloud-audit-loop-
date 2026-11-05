---
repo: BurnyCoder/jacobian-mem2gen
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 260
fixed: 7
unverifiable: 20
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/jacobian-mem2gen, round 1
## Summary
I checked the README (fork section and paper section), results/jtransport/REPORT.md, docs/jtransport.md, AGENTS.md, and the GitHub Pages site (docs/index.html with docs/data/*.js). I checked them against results/jtransport/exp1.json and exp2.json, the configs and code, the paper PDF in the repo (arXiv 2607.08393v2, whose metadata I confirmed on arXiv), the jacobian-lens repository at the pinned commit 581d398, the transformer-circuits J-lens page, and the arXiv pages of every cited paper. I recomputed every number in the REPORT tables and contrasts from the JSON with scripts. I re-ran the seeded 1000-fact sampler on CPU (with stubs): seed 848 gives 500 rows and 409 unique questions, seed 1340 gives 500 and 427. I also recomputed the Pages claims from the page data: LRSD gains (+95.6%, 94.9%, 19.7%, 18.6%; at λ=0.1 36.6–43.9% and 7.4–12.2%), the permeation epochs (9, 21 and 7), the ~6% stall, and the demo-cell ranks. The paper tables shown on the page (Table 2, Table 4, Table 7) match the PDF. Almost everything checked out. Seven claims were wrong or overstated, and I fixed them.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| README.md:15 | "R_t is a ridge inverse of J_t. This equals pinv(J_t) J_s h_s" | Equal only without the ridge (c → 0, invertible J_t); the reported run uses c = 0.1, and the readout still differs by 34% | jtransport/transport.py (ridge_inverse, Transport.apply); results/jtransport/exp1.json `ridge.c`=0.1, `geometry.jlens.readout_error`=0.339 |
| README.md:169 | "gives the Mem. column in the table below" (the README has no such table) | "the Mem. column of the paper's Table 2" | paper/2607.08393v2.pdf, Table 2 |
| README.md:155 | "Llama-3.2-1B and Qwen2.5-3B are listed there as comments" | "Qwen2.5-3B, Llama-3.2-1B and Llama-3.2-3B are listed there as comments" | train/configs/experiment_configs_specific_samples/multi_specific_sample_template.yaml |
| README.md:137 | "~1-1.5 min per item on an A800" (no source) | "the paper reports 3-11 min per per-fact run on one A800, Appendix B" | paper App. B, "Compute" |
| results/jtransport/REPORT.md:108 | "320 position samples per half" | "160 position samples per half: 40 prompts × 4 positions" | exp1.json config `jlens_pp_prompts_per_half`=40, `jlens_pp_positions`=4; jtransport/lens.py fit_per_position |
| results/jtransport/REPORT.md:118 | "κ 10⁴–10⁶" | "κ ≈ 5.6·10³–1.6·10⁶" (agrees with the REPORT's own diagnostics) | exp1.json `spectra[*].cond`: min 5557 (layer 20), max 1.557e6 (layer 9) |
| docs/jtransport.md (Sources) | "Learned layer-to-layer maps, the tuned lens" | "Learned per-layer affine maps into the final layer's prediction space, the tuned lens", with the paper title | https://arxiv.org/abs/2303.08112 |

## Unverifiable or hedged claims
These have no committed result file (experiment_logs/ and logs/ are gitignored), so I left them as written:
- REPORT §0: per-epoch memorization values (69.2/94.3/98.4/99.5/99.4%). The final 98.1% and the two-hop curve do match exp2.json. Also `chain_bridge_rate` 0.23.
- REPORT §2: loss trajectories (0.36→0.0004 and 0.31→0.16) and memorization at epoch 10 (10% vs 80%). The "λ = 0.1: training" status is also unverifiable: exp1.json config lists lrsd01/jlrsd01, but exp2.json has no λ=0.1 arms.
- REPORT §3: ‖J−I‖/‖I‖ values (1.27/1.21/0.51 and 1.01/0.92/0.49), the ‖J‖ ratio of 2.2–2.6×, the bridge-readout medians (shown only in the PNGs), and the TF32 "≤ 0.02%" figure.
- README: multi-fact run time (40 and 60 min), GPU memory (19 and 31 GB), "~30 s" CPU tests, "about 30 min" toy run, and the development environment (Python 3.11, CUDA 12.4). The paper confirms only the A800 80 GB GPUs.
- AGENTS.md: 4.9 GB peak and the WSL slowdown figures.
- Pages: Figure 1 caption numbers (recall 1.00 by about epoch 16, chaining about 0.20) and "in each of six models" (Figure 6). Both come from images. The page data were made by `analysis/project_page/export_page_data.py`, which is not in the repository.
- README: "Figure 4 of the paper" is LLaMA-3.1-8B. The paper's Table 6 lists Fig. 4 with Qwen2.5-7B and LLaMA-3.1-8B, and its caption gives no model. The page data say LLaMA-3.1-8B.

## Problems found but not fixed
1. The generator of the Pages data, `analysis/project_page/export_page_data.py` (named in the headers of docs/data/*.js), is not in the repository. The page figures cannot be regenerated or traced to logs from here.
2. The REPORT's λ = 0.1 row says "training". That status is possibly stale and cannot be checked against exp2.json. Update it when those runs are reported.

## Hugging Face card
n/a. The repository links no Hugging Face model, dataset or Space of its own. It only uses the public dataset NeelNanda/pile-10k as a dependency.

## Regenerated artifacts and tests
I changed no code. I edited only prose in README.md, REPORT.md and docs/jtransport.md. No generated tables or figures depend on these edits: report.py writes exp*_tables.md and the figures, not REPORT.md. I ran no tests because no code was touched. The repository's environment (torch 2.13 with CUDA) was not installed for this CPU audit.
