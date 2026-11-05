---
repo: BurnyCoder/training-facts-into-llms
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 215
fixed: 1
unverifiable: 5
not_fixed: 2
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/training-facts-into-llms, round 1

## Summary

I audited the repository independently. Earlier audit files in the repository were not used as evidence. The checks covered README, the two active papers (`papers/qwen35-revised`, `papers/qwen38-minimal`) and their bibliographies, `docs/training-strategy.md`, `docs/third-party-provenance.md`, `reports/EXPERIMENTS.md` (timeline table and metric passages), `reports/ALL_EXPERIMENTS.md`, `reports/INSTRUCTION_AUDIT.md`, `reports/qwen38/CLAIMS_AND_SOURCES.md` (reconciliation and parameter arithmetic), the hosted Hugging Face cards, and the live GitHub Pages explorer.

- **Numbers.** A script recomputed every score in the README tables from the per-record `passed` and `output` fields in the hash-checked evaluation JSON files. All 9 manifest-bound report hashes matched. Every recall, safety, control and non-empty count matched, as did every run ID, step and checkpoint. The same was true for runtimes and validation losses in `reports/EXPERIMENTS.md`, and for the Qwen3.8 checkpoint trajectory (epochs 1 to 15) behind the paper's results prose.
- **Generated views.** `results check` reported 0 stale files. The live Pages `results.json`, `app.js` and `index.html` are byte-identical to `site/`.
- **Citations.** I fetched all academic citations (ACL Anthology BibTeX, arXiv, NeurIPS proceedings). Titles, authors, venues, pages and DOIs match. Every pinned library commit (TRL 1.9.2, PEFT 0.20.0, Transformers 5.14.1, huggingface_hub 1.26.0, FLA 0.5.2, uv 0.11.27) is the peeled commit of its release tag.
- **Method claims.** I checked these against the code, presets and upstream sources:
  - The upstream `run.py` uses `torch.optim.AdamW(model.parameters())`, and `execute.sh` uses lr 2.2e-5 for 50 epochs.
  - The Gangadhar & Stratos paper says "Except for FT (21st layer), all our results use LoRA". It reports full-parameter and layers 3–5 ablations, and its DPO result is in §3.
  - Qwen3.8 `config.json` declares `Qwen3_5ForConditionalGeneration`. The safetensors index has 1,199 names, of which 15 are `mtp.*`. The Hub reports 27,781,427,952 BF16 scalars, and the denominator arithmetic checks out.
  - The adapter file is 233,605,480 bytes, consistent with 58,363,904 FP32 scalars.

The repository is largely accurate. I found one material README error: the acceptance summary left out the binding ≥11/12 recall gate. Without that gate, the README's stated criteria contradict its own results table: `semantic_specificity_gentle` scored 10/12 recall, 8/8 safety and 8/8 controls, yet is labeled "Failed acceptance".

## Fixes

| file:line | before | after | evidence |
| --- | --- | --- | --- |
| README.md:267-270 | "Acceptance requires improved recall, limited near-name false positives, limited loss of baseline control hits, and nonempty outputs" | "Acceptance requires at least 11/12 recall that also improves on the baseline, at most one near-name false positive, at most one lost baseline control hit, and nonempty outputs" | `src/training_facts_into_llms/evaluation.py:259-265` (`len(post_fact_ids) >= 11`, `<= 1` limits; the same in historical commit f9b67ff `src/fact_teaching/evaluation.py:260`); `acceptance.checks.fact_recall_at_least_90_percent=false` in `reports/evaluation-20260731T075738153557Z.json`, `-205057425949Z.json`, `-211115088822Z.json` |

## Unverifiable or hedged claims

- OpenReview forum IDs `nZeVKeeFYf9` (LoRA, ICLR 2022), `Sklgs0NFvr` (Kaushik et al., ICLR 2020) and `Bkg6RiCqY7` (AdamW, ICLR 2019), cited in the paper bibliographies. OpenReview returned a browser-verification page, so I could not fetch them. The matching arXiv records (2106.09685, 1909.12434, 1711.05101) were verified.
- `paper/references.bib` describes Trackio commit `972c8c04…` as the "Version 0.34.0 peeled commit". The Trackio repository has no v0.34.0 tag. The commit exists, and its `trackio/package.json` declares version 0.34.0, so the version is supported but "peeled commit" cannot be verified. This is in the immutable original paper, so I did not edit it.
- Values transcribed from private, untracked operational logs cannot be rederived from a clone. Examples are the `reports/manifest.json` provenance note, the interruption reason, and the uv timings (1.10 s / 483 ms / ~1.78 s) in `reports/qwen38/CLAIMS_AND_SOURCES.md`. These documents already disclose that limitation.

## Problems found but not fixed

- `papers/qwen38-minimal/references.bib` (`qwen38release`) anchors the Qwen3.8 release log at `#L36-L49`. At the pinned commit, lines 36–45 are the Qwen3.5 section; the 2026-08-14 Qwen3.8-27B entry is line 48 (the README correctly uses `#L46-L50`). The cited range still contains the entry, and editing the bib would leave the checked-in PDF out of sync, because LaTeX is not available to rebuild it.
- The README says thresholds are "owned by the training-strategy guide", but `docs/training-strategy.md` never states the ≥11/12 recall gate; it states only the one-lost-control limit. The threshold is stated in `reports/EXPERIMENTS.md:80-83`, `docs/qwen38-runpod.md:144` and the code. I left this documentation-ownership gap for the maintainer.

## Hugging Face card

The repository has no static card file. Cards are generated by `src/training_facts_into_llms/reporting.py` (`_render_adapter_readme`), `archive_staging.py`, and the documentation addendum in `documentation_publication.py`. I read the hosted cards with `hf_fs`:

- `BurnyCoder/qwen3.8-27b-atemokoloporos-…-59f2f6ff/README.md` matches the generator output plus the `audit-2026-10-29` addendum. Its scores (0/12, 8/8, 8/8 baseline; 11/12 = 91.7%, 8/8, 8/8 tuned) match `evaluation.json`.
- `BurnyCoder/qwen3.5-0.8b-atemokoloporos-minimal-pair-primary/README.md` matches `archive_staging.py`. Its scores (12/12, 7/8, 5/8; root checkpoint 112, extra checkpoint-210) match the evidence.

There is no drift, so no upload is needed. The README's example checkpoints (`semantic-specificity` 42, `minimal-pair-primary` 210) exist on the Hub. The Collection contents and pinned revisions (`Qwen3.5-0.8B@2fc0636`, `Qwen3.8-27B@1d4bf0f`, adapter `@dd0ded7`, dataset `@ce122b5`) all resolve.

## Regenerated artifacts and tests

- The clone was shallow, so I unshallowed it (`git fetch --unshallow`); `results check` needs historical blobs.
- A full `uv sync --frozen` would download torch 2.13 with CUDA wheels, which is over the 1 GB limit. I used a light scratch venv instead, with the locked versions of matplotlib, python-dotenv, pytest, ruff and markdown-it-py.
- `training-facts-into-llms results check`: complete, 0 generated files updated, before and after the edit. The README edit is outside the generated `results:*` blocks.
- `pytest tests/test_public_results.py tests/test_results_build.py tests/test_paper_sources.py tests/test_active_papers.py tests/test_qwen38_paper.py`: 61 passed.
- I did not run the full test suite, because some tests import torch. No code was changed. I rebuilt no paper PDFs; no paper sources were edited.
