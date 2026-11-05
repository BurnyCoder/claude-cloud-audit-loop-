---
repo: BurnyCoder/geometry-of-representations-of-mathematics-in-llms
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 132
fixed: 4
unverifiable: 5
not_fixed: 2
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/geometry-of-representations-of-mathematics-in-llms, round 1
## Summary

This was an independent check that did not rely on earlier audit files. The repository was already in good shape. The README's generated blocks, `reports/summary.md`, `reports/audit_lexical.md` and `paper/paper.md` are rendered from templates plus `results/*.json`, and `tests/test_docs_regenerate.py` passes. So the work went into hand-typed prose, citations, method claims, the Hugging Face card and the site.

- **Citations.** All 26 cited arXiv IDs resolve. Their titles, first authors and years match. 14 full author lists in the paper's reference list and 5 venue notes also match.
- **DOIs.** 17 of the 18 DOIs resolve on Crossref with matching metadata. The 18th, Efron 1987, was rate-limited and not re-checked.
- **Literature claims.** I fetched the sources and confirmed four claims against them: Golechha et al. (random concepts and random unembeddings after whitening), Linzen 2016 (offset-ignoring baselines and plurals), the Karkada et al. abstract, and Lei & Cooper (3D spiral).
- **Wikipedia table.** The pinned Wikipedia group-like table (oldid 1372036401) has 8 total structures and no commutativity column, as the paper says.
- **Licences and parameter counts.** I checked these against the HF API and the model configs and safetensors headers. All match. Qwen3.5-2B-Base has 1.88B text parameters ("at most 1.9B"). Gemma-4-E2B is 2.3B effective, 5.1B with embeddings. Its per-layer-embedding table is 262,144 × 256 × 35 = 2.35B.
- **Hand-typed numbers.** I recomputed 29 hand-typed numbers in `reports/experiments.md`, the README highlights and the paper discussion from the results JSON. 28 matched; one p-value bound was slightly wrong.
- **Fixes.** I made one numeric fix (in two files) and one method clarification (in two files).

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| reports/experiments.md:238 | twins' circle-template ρ 0.15–0.46, "p ≤ .008" | "p ≤ .0085" | results/{mvp,robustness,gemma}/shapes.json `<model>__random.angles.circle_rho_p` (max 0.00850, Qwen3.5-2B twin) |
| docs/deviations.md:29 | same, "p ≤ .008" | "p ≤ .0085" | same |
| paper/template.md:280 (+ paper/paper.md, regenerated) | "The trained models' and twins' leave-one-out order nulls have 10,000 permutations (…; the word-form baselines keep 300)" | adds "and the four extra-seed twins of the twin-seed check use 2,000" | src/mathgeom/pipeline.py:995 (`phase_twins`: `n_perm_loo=2000`); pipeline.py:258 (shapes: `n_perm_loo=10_000`) |
| reports/audit_template.md:11 (+ reports/audit_lexical.md, regenerated) | "(trained models and twins: 10,000)" | "(trained models and their seed-0 twins: 10,000; the four extra-seed twins of D12: 2,000)" | same |

## Unverifiable or hedged claims

- **Runtimes** in README "Install and run": about 38, 35, 17, 16 and 35 minutes of extraction, and about 23 minutes for `shapes`. They are measured from `logs/*.log`, which is not committed.
- **Disk use** in the README: 43 GB of weights, 19 GB for the judges, 6 GB of activations. It was not measured from anything in the repository.
- **"Qwen3.5 series announced Feb 2026"** (paper §3.4). The Qwen blog was not fetched in this round.
- **Simulation rates** in `reports/experiments.md`: 42%, 2.5%, 92.5%, 5%, 100%, and 1.8% / 4.0%. The file itself already says that the script was never committed. The rerun figures it quotes come from code that is in the repository.
- **Efron 1987 DOI** (10.1080/01621459.1987.10478410). Crossref returned a rate-limit error, so it was not re-fetched this round. The cited title, volume and pages agree with the standard record.

## Problems found but not fixed

- **`paper/paper.pdf` was not regenerated.** pandoc's xelatex engine is not installed here, so the PDF still has the old parenthetical at the §4 "Test precision" paragraph. `paper/paper.md` is current. Rebuild with `uv run python run.py paper --config configs/mvp.yaml` on a machine with xelatex.
- **Ambiguous figure on the site.** `site/index.html` (§4) says "We drew on average about two dozen concepts (at most 30)". On average 28.5 primary concepts per field were drawn. The confirmatory split used for the centroids has 23.4 per field, which is 398/17. The sentence is ambiguous rather than wrong, so I left it.

## Hugging Face card

- **No content drift.** The hosted card `hf://datasets/BurnyCoder/geometry-of-mathematics-in-llms/README.md` (6,530 bytes, CRLF line endings) is identical to `docs/data_card.md` once line endings are normalised. No upload is needed.
- **Card claims check out.** These match `data/concepts.csv` and the configs:
  - pilot share 19.6% (160/815);
  - `multi_field` is always false;
  - 5 missed eponyms, all still primary;
  - 17 math fields and 4 control fields;
  - 24 appended nonce rows (6 heads × 4);
  - all probed models are Apache-2.0, and Phi-4-mini is MIT (HF metadata).
- If the card is edited later, upload it with `huggingface-cli upload BurnyCoder/geometry-of-mathematics-in-llms docs/data_card.md README.md --repo-type dataset`.

## Regenerated artifacts and tests

- `reports/audit_lexical.md` and `paper/paper.md` were re-rendered from their templates with `mathgeom.report.paper.render_template`, the same path the docs test uses. The diff is only the edited sentence.
- `paper/paper.pdf` was not rebuilt (no xelatex).
- The full test suite passed before the edits: 74 passed, 11 skipped. After the edits, `tests/test_docs_regenerate.py` and `tests/test_report_rules.py` pass (7 passed).
