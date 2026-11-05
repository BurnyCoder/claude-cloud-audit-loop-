---
repo: BurnyCoder/end-to-end-block-sparse-featurizers
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 280
fixed: 5
unverifiable: 8
not_fixed: 2
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/end-to-end-block-sparse-featurizers, round 1

## Summary

The audit covered README.md, AGENTS.md, all docs/, reports/experiments.md, the study, smoke and downstream-sweep reports, the study paper (source in `src/e2e_bsf/paper.py` and its PDF), the GitHub Pages data and figures, the vendored code notices, and one hosted Hugging Face model card. Scripts recomputed every number against `reports/*/results.json`, `pilot.json`, `verification.json`, `study_status.json`, `cache.json` and `batch_numerics_diagnosis.json`. These numbers all matched, with correct rounding: the condition and control tables, the paired primary effect and its Student interval (t(4) recomputed), the scalar secondary effect and interval, the 6.78% and 44.41% changes, the pilot power (0.7747 at n=5, recomputed with SciPy's noncentral t), LR selection, the 22.24 h and 18.53 h forecasts, training hours, peak VRAM, geometry and intervention means, timestamps, the sweep pilot table, and the smoke tables.

The method claims match the code: Adam, clip 1, cosine decay to 10%, 2,000-replicate image-group bootstrap, the 1.25 timing factor, a C grid of {0.01, 0.1, 1, 10}, StratifiedGroupKFold(5) at seed 42, and parameter counts of 4096·3·768 + 4096 and 12288·768 + 12288. The DINOv3 config confirms width 768, 4 registers, patch 16 and 12 layers. The vendored Goodfire files and the reused logger are byte-identical to the pinned upstream revisions. Apollo's `losses.py` confirms the teacher-to-inserted KL direction and the equally divided downstream coefficients.

The cited papers check out: Braun et al. (Table 1: 69.4/0.145 against 27.5/0.144; Sections 2.4 and 3.1–3.2), Fel et al. (Appendix D: shared positive log-parameterized gain, QR every 20 steps), Jerpelea & Ananthram (splitting and seed consistency), Karvonen 2025, Chanin 2026, SAEBench, Card et al. and Lones. The site's `data.json` files and images are identical to the report artifacts.

Only small errors were found: incomplete reference metadata in the paper, a wrong page count, and a pointer to a gitignored file.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| src/e2e_bsf/paper.py:211 (and the PDF's reference 3) | "3. Revisiting End To End Sparse Autoencoder Training: A Short Finetune is All You Need (2025)" | "3. Karvonen. Revisiting End-To-End Sparse Autoencoder Training: A Short Finetune Is All You Need (2025)" | https://arxiv.org/abs/2503.17272 |
| src/e2e_bsf/paper.py:212 (and the PDF's reference 4) | "4. A Deeper Analysis of Block-Sparse Featurizers (2026)" | "4. Jerpelea and Ananthram. A Deeper Analysis of Block-Sparse Featurizers (2026)" | https://arxiv.org/abs/2608.27515 |
| src/e2e_bsf/paper.py:217 (and the PDF's reference 9) | "9. SAEBench: A Comprehensive Benchmark for Sparse Autoencoders (2025)" | "9. Karvonen et al. SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability (2025)" | https://proceedings.mlr.press/v267/karvonen25a.html |
| docs/plan-completion.md:38 | "the seven-page [paper]" | "the eight-page [paper]" | `pdfinfo reports/study/paper.pdf` reports 8 pages (also before regeneration) |
| docs/downstream-execution-notes.md:17 | diagnosis cited only at gitignored `outputs/sweeps/downstream-v1/batch_numerics_diagnosis.json` | adds a link to the tracked copy | reports/downstream-sweep/batch_numerics_diagnosis.json (0.02734375, RMS 9.9085e-5, teacher-logit 1.0490e-5 and identity MSE 1.230e-7 all match the prose) |

## Unverifiable or hedged claims

These were left unchanged. The repository holds no committed evidence for them, and git history is a single squashed merge commit.

- docs/plan-completion.md: "Preparation and all pilots finished after 90.28 minutes". The allocation failure is recorded at 90.30 min after start, which is consistent. Schedule freeze at 140.59 min is verified.
- reports/study/findings.md: "all training ended at 12:42:54 UTC" (status update 12:42:55.87 UTC, consistent) and "first complete report finished at 13:01:16 UTC" (no committed log).
- docs/plan-completion.md: PR #1 merge time 01:31:21 Europe/Berlin and first smoke command at 01:31:39.
- README: "approximately 15 GB workspace storage". The 8 GB and 58 GB cache sizes are verified from the shapes.
- Historical test-suite counts (23, 25 and 37 tests passing) and statements about browser or visual inspection. I did not run the suite: no code logic changed, and it needs a CUDA torch install of more than 1 GB. The repository now has 34 test functions.
- docs/literature-review.md: "Exact combination searches did not locate a verified prior output-KL BSF implementation". This is a search claim, not a sourced fact.

## Problems found but not fixed

- `src/e2e_bsf/sweep/paper.py:177-178` (downstream-sweep paper references 1–2) uses shortened titles: "End-to-End Sparse Dictionary Learning" and "Block-Sparse Featurizers". The full titles are "Identifying Functionally Important Features with End-to-End Sparse Dictionary Learning" and "Structuring Sparsity: Block-Sparse Featurizers Capture Visual Concept Manifolds". I did not change them. Regenerating `reports/downstream-sweep/paper.pdf` and `site/sweep/paper.pdf` would invalidate the deployed-file hashes recorded in `reports/downstream-sweep/publication_verification.json`. The IDs and URLs are correct.

## Hugging Face card

The repository has no tracked card file. Cards are generated by `src/e2e_bsf/publication.py` (lines 51–78). I read the hosted card `hf://models/BurnyCoder/e2e-bsf-dinov3-imagenette-full-block-kl-seed100/README.md`. Its text matches the template, with CRLF line endings. Its numbers match `reports/study/results.json` for block_kl seed 100: KL 0.037268035, accuracy 99.2774%, NMSE 0.78616697. The study-level narrative matches. The collection holds all 25 full-study model repositories. No drift was found, so no upload is needed. For reference, the command would be `huggingface-cli upload BurnyCoder/<model> path/to/card.md README.md`.

## Regenerated artifacts and tests

- `reports/study/paper.pdf` was regenerated by calling `write_paper` from `src/e2e_bsf/paper.py` on `reports/study/results.json`, using the lockfile's pinned reportlab 5.1.0 and pillow 13.0.0. A control run before the edit produced text identical to the committed PDF. After the edit, `pdftotext` shows only the three reference lines changed. The page count is still 8. `site/paper.pdf` was updated to the same bytes.
- The full report pipeline (`e2e-bsf report`) could not run because it reads gitignored `outputs/`.
- Tests: only a string literal in `paper.py` changed. `py_compile` passes, and no test references the edited strings. The pytest suite was not run, because it needs the CUDA torch environment.
- All relative Markdown links in README, AGENTS.md, docs/ and reports/ resolve.
