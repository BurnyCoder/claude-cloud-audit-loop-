---
repo: BurnyCoder/geometrical-shape-fitting-in-llm-mechanistic-interpretability
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 164
fixed: 1
unverifiable: 4
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/geometrical-shape-fitting-in-llm-mechanistic-interpretability, round 1
## Summary

I audited the README, paper source (`paper/*.tex`, `references.bib`, generated tables and macros), `docs/` (methodology, shape catalog, explorer page and its data), `reports/` (summary, exp01, exp02, deviations, preregistration as a frozen record), the hosted Hugging Face card, configs and the code docstrings that cite papers. I did not use earlier fact-check rows as evidence.

The repository is in good shape. Every number I recomputed matched the result files:
- H3 7/12 by subsample majority and 8/12 by full-cloud label, Clopper-Pearson 27.7-84.8%.
- H4: mean matched-Gaussian blob rate 85.6% over 17 datasets; C1 ringing 60% vs helix 40%; GP helix 80%, random walks 0%.
- The helix-rule list, and every cell checked in the 26-row real table (N x D, top-3 variance, fit, p, subsample majority, flags, blob rate).
- The 10 synthetic system rows, the per-N-bin gaps, the hardest families and the largest confusions (helix-cone 371, paraboloid-cone 287, sphere-cone 271).
- Calibration, the ambiguous fraction, the training summary and the timing claims in deviations.md.

These were recomputed from `results/main_s0/{analysis.json, synth/per_sample.csv, real/real_results.json, train/*.json}` with short scripts.

Method claims match `configs/base.yaml` and the code:
- the architecture, loss weights, optimizer and schedule, refinement settings and test/baseline sizes;
- the B1 counts (11 posed families x 4 inits + 5 k-means + 6 templates x 2 = 61 runs, 22 candidates), the G-AIC residual grids (512 / 40x40) and the label margins;
- the statistics: 10,000 permutations, normal-approximation p for H1, Wilcoxon for H2/H5b, Holm, 15-bin ECE.

The git history after unshallowing shows that the preregistration was committed at 05:31 and never modified. The first training log on the Hub is stamped 06:00:42.

All 38 arXiv IDs resolve. Their titles, authors and years match the bib entries. I checked the content claims cited to the 2025-2026 sources against the full texts (Bhalla Table 1; Engels Fig. 4 layers 30/5; Tiblias Table 5; Berdnikov App. F; Wurgaft; Sun; Moisescu-Pareja; Sinii; Gurnee; Yedidia; Marks & Tegmark; Park; Kantamneni; Nanda's 40,000 epochs and 6 W_E frequencies; SPFN; Zhou App. B; Guo Eq. 3 / Sec. 4.2; Minderer; Kanatani's G-AIC formula). All are supported.

I found one wrong source and fixed it.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| reports/exp01_synthetic.md:94 | FP64 at 1/64 of FP32 throughput sourced to the "CUDA C++ Best Practices Guide, arithmetic instruction throughput" (https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/), which does not list an FP32:FP64 ratio | Same claim sourced to the CUDA Programming Guide, Compute Capabilities appendix, row "Ratio of FP32 to FP64 Throughput": 64:1 | https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compute-capabilities.html (the table lists 64:1 for 8.6/8.7/8.9 and 11.0/12.x) |

## Unverifiable or hedged claims

- README, Llama mirror: "safetensors shards are identical (same LFS sha256 pointers)". Today the Hub API masks the LFS sha256 of the gated `meta-llama/Llama-3.1-8B`. I could confirm only that the four shard sizes match those of `unsloth/Meta-Llama-3.1-8B`, and that config, generation_config and tokenizer files differ in size. Left as is: it is a dated check by the author.
- exp02 learning 11: the reference to accelerate issue #2871. I could not fetch the issue page. The `hooks.py` claim (`module.forward = functools.update_wrapper(functools.partial(new_forward, module), ...)`) is verified in the current source.
- exp01 learnings 1-2 and 11: development timings (profiler shares, 7x generator speed-up, 0.04 s/step, 0.7 GiB peak) and exp02 learning 11 (5.7 GB paged). No logs in the repository support them; they are already labelled as development observations.
- Post hoc visual descriptions: R1's "spiral whose radius varies" and the C3 counting control as "a single streak plus one isolated point". These are qualitative and already labelled post hoc and untested. I did check the R9 spread asymmetry, the R8b decade jumps (largest at 49/50, 40/41, 59/60) and the tight R5 clusters against `docs/data/*.json`.

## Problems found but not fixed

- `src/neurogeom/catalog/catalog.yaml` (Tiblias entry) lists "Qwen2.5-3B, Llama-3.2-3B, gemma-2-2b (main); Llama-3.1-8B/70B". The paper (arXiv:2510.01025) uses the -Instruct variants of all five. This is minor. Fixing it means regenerating `docs/shape_catalog.md` and `paper/generated/catalog_table.tex`, and then the PDF, which cannot be compiled here (no LaTeX). So I left it, to avoid putting the PDF out of sync.

## Hugging Face card

I read `hf://models/BurnyCoder/neurogeom-shape-fitter-main-s0/README.md` with `hf_fs`. The repository has no card file: `src/neurogeom/report/publish.py::model_card` generates the card from `reports/generated/headline.md`, `results/main_s0/train/summary.json` and `synth/meta.json`. The hosted card matches that template with the current headline, the training summary (22643 steps, 1,712,093 params, val acc 0.9019) and T = 0.7721. The only difference is CRLF line endings. No drift and no upload needed.

## Regenerated artifacts and tests

- The only edit is in a hand-written "Learnings" section of `reports/exp01_synthetic.md`, outside the generated markers. No tables, figures, macros or the PDF needed regenerating, and none were regenerated. The paper PDF text matches the current `.tex` (spot-checked phrases).
- No code was changed, so the tests were not run.
- Commit pushed: `c5cb9c6 Fix exp01 FP64 throughput source: cite the CUDA Programming Guide compute-capability table`.
