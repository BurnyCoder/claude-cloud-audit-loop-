---
repo: BurnyCoder/topological-data-analysis-mechanistic-interpretability-fix
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 70
fixed: 9
unverifiable: 7
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/topological-data-analysis-mechanistic-interpretability-fix, round 1

## Summary

The repository is a small wrapper around an upstream Colab notebook: README.md, AGENTS.md, docs/provenance.md, one validation report, a canonical notebook, and a 98.9 MiB executed notebook stored in Git LFS (pulled for this audit). There are no papers, HF card, GitHub Pages, figures or result tables.

What I checked:
- I downloaded the upstream notebook again from Google Drive. Its SHA-256 (42ec8d90…) and size (76,756 bytes) match the recorded values.
- I diffed it against the canonical notebook. The only difference is the loader name in cell index 5.
- I recomputed every hash, byte count, cell count, execution count, error count and widget-state size.
- I fetched the LessWrong post and comments through the GraphQL API (title, author, date 2025-02-24, Jakob Hansen's comment linking the Colab).
- I fetched SAE Lens v6.47.0 `sae.py`, `pretrained_saes.yaml` and the loader code, the SAE Lens migration guide, the HF SAE `cfg.json` (d_sae 32768, topk k=32, blocks.8.hook_resid_post), the Cobalt 0.4.2 setup docs (`COBALT_LICENSE_KEY`, registration), GitHub's file-size docs (100 MiB) and the TransformerLens v3.6.0 `__init__.py`.
- I ran `uv lock --check` and reproduced both nbconvert results: the canonical notebook renders, and the upstream notebook fails with `KeyError: 'state'`.

Most claims held up. The main errors:
- The Python patch version 3.12.8 is not supported by the evidence.
- The README overstated how faithfully `uv.lock` reproduces the working run.
- `cfg_dict` was said to be needed by later cells. It is not used after cell 5.

## Fixes

| file:line | before | after | evidence |
| --- | --- | --- | --- |
| README.md:76 | "using Python 3.12.8, SAE Lens 6.47.0, …" | Python 3.12. The 3.12.8 `language_info` field was copied from upstream, whose outputs ran on Python 3.11 | executed notebook cell 1 pip output (`/usr/local/lib/python3.12`); upstream notebook pip output (`python3.11`); identical `language_info` in both |
| README.md:46 | "the working package versions are locked in `uv.lock`" | Only the direct dependencies match the run. 53 of 176 shared packages differ (torch 2.13.0 vs 2.11.0+cpu). Import-tested only | `uv.lock` vs executed notebook cell 1 pip output (script comparison) |
| README.md:26 | "The notebook needs the configuration and sparsity tensor as well" | Legacy unpacking still runs with a DeprecationWarning but yields `sparsity=None`, and later cells call `sparsity.numpy()`. `cfg_dict` is not claimed as needed | https://raw.githubusercontent.com/decoderesearch/SAELens/v6.47.0/sae_lens/saes/sae.py (`__iter__`); docs/migrating.md; notebook cells 17, 18, 21 |
| README.md:9 | unsourced "32k-feature TopK SAE … layer-8 … GPT-2 Small" | added source: OpenAI v5 SAE, 32,768 features, k=32, HF repo link | hf://models/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs/v5_32k_layer_8.pt/cfg.json and README; SAE Lens pretrained_saes.yaml v6.47.0 |
| docs/provenance.md:13 | "one compatibility change in cell 5" | "cell 5 (zero-based index; the sixth cell and third code cell)" | canonical vs upstream notebook diff |
| docs/provenance.md:25 | "retains the earlier `(sae, cfg_dict, sparsity)` result needed by later notebook cells" | Later cells use `sae` and `sparsity` only. Notes the legacy unpacking result (`sparsity=None`) and that the migration guide misnames the method `load_from_pretrained_with_cfg_and_sparsity` | notebook source; SAE Lens v6.47.0 sae.py; docs/migrating.md |
| reports/2026-08-03-validation.md:9 | hypothesis: tuple "values used by later cells" | `sae` and `sparsity` values used by later cells | notebook source |
| reports/2026-08-03-validation.md:24 | "cell 5's loader name" | "cell 5's (zero-based index) loader name" | notebook diff |
| reports/2026-08-03-validation.md:34 | "The saved execution records Python 3.12.8" | Python 3.12 from pip paths, with the `language_info` caveat. Added notes on execution counts 13 to 30 (not a fresh kernel) and lockfile drift. Added a dated Corrections section | executed and upstream notebooks; uv.lock |

Also added to docs/provenance.md: execution counts 13 to 30, all packages "already satisfied", so the run was not in a fresh kernel.

## Unverifiable or hedged claims

- docs/provenance.md: upstream retrieval date of 3 August 2026, and that the executed snapshot is a "user-provided" Colab run. The Colab metadata is consistent with this but does not prove it.
- reports/2026-08-03-validation.md: the generation timestamp, and the details of the fresh smoke-test environment (Linux/WSL2, Python 3.12.3, uv 0.11.27). I could not repeat the full `uv sync`, because the locked torch plus CUDA wheels exceed the 1 GB download limit.
- reports/2026-08-03-validation.md: "Importing Cobalt without a registered local license … prints its registration reminder". Not run.
- Upstream notebook comment linking googlecolab/colabtools issue #3501. The GitHub API was blocked for this session.
- Upstream notebook markdown, cells 7 and 14: the claims about Cobalt graph levels nesting, and the slider and UI instructions. These need a live Cobalt UI. They were left unedited because AGENTS.md keeps upstream source frozen.

Verified as stated:
- "TransformerLens does not expose `__version__`": the v3.6.0 `__init__.py` has no `__version__`.

## Problems found but not fixed

- Upstream notebook cell 12 (`get_feature_embed_html`): the iframe `src=` attribute has a closing `"` but no opening quote. This is an upstream code defect. It was left unchanged because the repository's modification boundary (AGENTS.md, provenance) freezes upstream source text.
- The SAE Lens migration guide (upstream, not this repository) names the replacement method `SAE.load_from_pretrained_with_cfg_and_sparsity()`, while the code defines `SAE.from_pretrained_with_cfg_and_sparsity()`. This is now noted in docs/provenance.md, but it can only be fixed upstream.

## Hugging Face card

n/a. The repository has no Hugging Face model, dataset or Space of its own, and no card file. The README now links the third-party SAE repo `jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs`, read with `hf_fs` as evidence only. There is nothing to upload.

## Regenerated artifacts and tests

- No generator scripts exist. No notebooks or data files were edited; only Markdown changed.
- `uv lock --check`: passed (214 packages resolved).
- `nbconvert --to html`: the canonical notebook renders, and the upstream notebook raises `KeyError: 'state'`. This reproduces the report's claim.
- Hashes and LFS: the canonical SHA-256 is affc3ac7…, 22,583 bytes. The executed SHA-256 is aa991982…, 103,731,130 bytes, and matches the LFS pointer.
- Secret and local-path regex scan of both notebooks: 0 hits.
- Commits on fact-check/2026-11-05-r1: caea51a (README), 5dbf93c (provenance), f100114 (validation report). Pushed.
