---
repo: BurnyCoder/hessian-training-for-looped-transformers
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 125
fixed: 4
unverifiable: 10
not_fixed: 1
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/hessian-training-for-looped-transformers, round 1

## Summary

The repository has no Stage 1 results yet. `results/` holds only `results/benchmark/*.json`, and every generated block reads "Pending" or "in progress", which matches the data. So the checkable claims are citations, method details, benchmark numbers and git-history claims.

- **Citations.** All 36 arXiv IDs resolve (arxiv.org/abs pages fetched), and their titles, authors, years and venues match the text.
- **Section-level claims checked against full text:** Kuo et al. 2026 (Table 1, Sec. 3.3, Sec. 4.1, Fig. 6, App. A), Fan et al. 2024 (Sec. 4.2.1, 6.1.1, Eq. 2, App. F Table 2, and their data-generation code), NSO (Sec. 3.1, σ grid, ResNet-34, GPT-2 CoT, CLIP), SEHT (ResNet and WRN CNNs, 2-layer LSTM in their "Wiki-text2" section), Sophia (Alg. 2 is GNB, k = 10), Liu et al. 2023 (App. B.1, synthetic data) and Andriushchenko et al. 2023 (adaptive average-case sharpness).
- **Licenses.** Licenses of the referenced code (nanoGPT, looped_transformer, PyHessian, NSO: MIT; looped-tf: none) match the text.
- **Method details.** Model, optimizer, penalty, evaluation and measurement details in README/docs/reports/paper match `config.py`, `model.py`, `train.py`, `regularizers.py`, `evaluate.py` and `measure.py`. The parameter count, 2,371,328 ≈ 2.37M, was computed from the layer shapes.
- **Benchmarks.** The benchmark numbers in README, the report and the addenda match the JSON (10.05 GB, 15.6 s, 4.46 GB, 2.15 s, ≈10.7× ≈ "11×", 0.446 and 0.201 s/step, 5.4 h / 9.0 h / ≈18 h, 0.70 s/step concurrent). One exception is the "16–200 timed steps" claim; see Fixes.
- **Git history.** The preregistration's first commit (b162614) predates all code. The text above the addenda is byte-identical to that commit, and the addendum commit hashes match.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| reports/paper/paper.md:24 | "Per length, the across-run SD is 8.7–12.2 points for looped models against 0.5–0.9 points for non-looped transformers (their Sec. 4.1)." | "Averaged over the OOD lengths 20–60, the per-length across-run SD is 8.7–12.2 points for looped models with fixed or length-matched loop counts (K = 20, K = n) against 0.5–0.9 points for 60- and 3-layer non-looped transformers (their Sec. 4.1 and Fig. 6)." | https://arxiv.org/html/2606.29983 (Sec. 4.1: 0.009/0.005/0.087/0.122; Fig. 6 caption: "mean standard deviation ... averaged over OOD digit lengths from 20 to 60") |
| reports/preregistration.md (Addendum 1, "16–200 timed steps") | 16–200 timed steps | Corrected in a new Addendum 4 (the file is append-only by convention): 16–100 timed steps | results/benchmark/*.json, `steps_timed` = 16, 20, 50, 64, 100 |
| reports/preregistration.md (Sec. 4, "throughput benchmark of 200 steps per arm") | S chosen from 200 steps per arm | Addendum 4 records that the budget numbers come from 64 timed steps per arm | results/benchmark/benchmark_final_alone.json |
| reports/preregistration.md (Addendum 3, item 3, "per-length across-run SD") | per-length SD 8.7 / 12.2 vs 0.9 / 0.5 | Addendum 4: these are per-length SDs averaged over OOD lengths 20–60 | https://arxiv.org/html/2606.29983 Sec. 4.1, Fig. 6 |
| reports/paper/paper.md (App. A), reports/stage1_experiment.md:3 | Addenda 1–3 | Addenda 1–4 (bookkeeping for the new addendum) | reports/preregistration.md |

## Unverifiable or hedged claims

- Avron & Toledo 2011, "Lemma 1", and the claim that Rademacher probes minimize variance: the ACM paper was not fetched (paywalled). The Hochreiter 1997 and Hutchinson 1990 DOIs were also not fetched. Their metadata matches my background knowledge, but I did not count them as checked.
- PyTorch tutorial: the `vjp(grad(f))` reverse-over-reverse HVP is confirmed. The aside that forward-over-reverse is "usually more memory-efficient" was not located in the fetched text.
- The torch 2.15.0 native `layer_norm` third-derivative error and the `derivatives.yaml` / SDPA double-backward claims: no torch install. The cu132 wheel is over 1 GB and no GPU is available, so the tests were not run.
- Deterministic kernels "0.20 → 0.25 s/step": `benchmark_baseline_only.json` gives 0.2525 s/step, but it does not record whether deterministic algorithms were on.
- Addendum 2 and AGENTS.md timings and memory: 80 s → 2.8 s, ~0.58 s per HVP, ~2.5 h, ~100 s probe, 4.6 GB per 16-problem chunk, 0.2–0.3 GB per problem. No logs are committed. The 2.5 h figure is consistent with a back-of-envelope HVP count (~2.2 h).
- Smoke-test gradient norms (10²–10³ vs 1–40): no smoke logs are committed (results/smoke is gitignored).
- Novelty claims ("no prior work applying SAM/NSO/Hessian-trace penalties to looped transformers") and "the only Hessian-trace regularizer with transformer LM results": these are search statements. Note that NSO also reports BERT-Base text classification (their Fig. 3), which the parenthetical list omits.
- Gong et al. 2025 "theory in a simplified linear-attention setting" and the fSGLD "(σ²/2)·tr(H)" and ViT details: only the abstracts were checked. The abstracts are consistent but do not show these specifics.

## Problems found but not fixed

- `reports/paper/paper.pdf` was not regenerated. `report.build_pdf` needs XeLaTeX, which is not installed, so the PDF does not include the paper.md edits above. Rebuild with `uv run python main.py report` (or the pandoc command in `report.build_pdf`) on a machine with XeLaTeX.

## Hugging Face card

The repository links https://huggingface.co/BurnyCoder/hessian-looped-transformers. The Hub API returns 401 for it, so it does not exist publicly yet. That matches the README ("not yet published"). The repository has no committed card: the card is generated by `publish.py` from `results/stage1_summary.json`. There is nothing to compare and nothing to upload.

## Regenerated artifacts and tests

- `main.py report` was not run. There are no Stage 1 results, so it would only rewrite the "Pending" blocks, and its PDF step needs XeLaTeX (unavailable).
- No code was changed, so tests were not run.
