---
repo: BurnyCoder/looped-transformers-llms-neuron-mechanistic-interpretability
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 320
fixed: 6
unverifiable: 6
not_fixed: 0
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/looped-transformers-llms-neuron-mechanistic-interpretability, round 1
## Summary
The repository is in very good shape. I recomputed the numbers with short scripts reading `results/Ouro-1.4B/*.json` and `cross_loop_corr.npz`. Almost every number checked matches, including correct rounding:
- README highlights and results table
- paper abstract, atlas, confirmatory, follow-up, audit, robustness, judge and replication sections
- reports 04, 05 and 07, the summary, docs/methodology and setup
- the viewer pages and `confirm_effects.png`

Method claims match the code and configs: `.env.example`, `config.py`, `screen.py`, `prereg.py`, `atlas.py`, `stats.py`, `model.py`, `judge.py` and `audit.py`. Architecture and exit claims match the pinned `modeling_ouro.py` and `config.json` at revision 574fa66.

I fetched these external sources and they support the sentences citing them:
- the arXiv entries for Ouro, Blayney et al., Parcae and Kirin
- the Goodfire essay, the nesiacel LessWrong post and the Suiche blog post
- the Ouro-1.4B, Ouro-1.4B-Thinking, Ouro-2.6B and Qwen3.5-9B Hub cards and files

Two small errors were found and fixed:
- Two stated upper bounds on replication p-values sat slightly below the actual maxima. This affected 4 statements across 3 files.
- The README stated a T-sweep share without saying which neurons it covers.

The paper PDF was rebuilt.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| README.md:45 | Holm p ≤ 2.1e-16 (replication) | Holm p ≤ 2.2e-16 | results/Ouro-1.4B/replication.json (max p_wilcoxon_holm = 2.118e-16) |
| README.md:40 | effect already present at T = 1 (70–99% of the T = 4 effect) | … (70–99% of the T = 4 effect for the 5 confirmed neurons) | results/Ouro-1.4B/followups.json t_sweep (confirmed: 0.70–0.99; L19 N3901: 1.11) |
| reports/summary.md:58 | confirm prompts: Holm p ≤ 2.1e-16 | ≤ 2.2e-16 | results/Ouro-1.4B/replication.json |
| reports/summary.md:58 | fresh prompts: Holm p ≤ 2.0e-16 | ≤ 2.1e-16 | results/Ouro-1.4B/replication_fresh.json (max = 2.0008e-16) |
| paper/sections/discussion.typ:13 | $p <= 2.1 times 10^(-16)$ | $p <= 2.2 times 10^(-16)$ | results/Ouro-1.4B/replication.json |
| paper/sections/discussion.typ:23 | $p <= 2.0 times 10^(-16)$ | $p <= 2.1 times 10^(-16)$ | results/Ouro-1.4B/replication_fresh.json |

## Unverifiable or hedged claims
- **No dead neurons; median max|a| 0.64 (1st/99th percentile 0.025 / 6.94).** These are in reports/01 and the paper. They come from `atlas.pt`, which is gitignored and about 0.5 GB on the Hub. It was not loaded because torch is not installed in this environment.
- **None of the 750 prompt stems occurs verbatim in the 8M atlas tokens.** This needs `cache/tokens_atlas.npy`, which is not in the git repository.
- **llama.cpp release b11854 and its CUDA 13.4 asset names** (docs/setup.md). The GitHub API was not reachable from this session.
- **Goodfire essay dated "Oct 2026"** (README, refs.bib). The page shows no publication date, only "Revised October 30, 2026", so the month is consistent but not confirmed.
- **Bibliography metadata of long-established papers** (Holm 1979, Hodges & Lehmann 1956, Kerby 2014, Phipson & Smyth 2010, AxBench, ActAdd and others). It matches my knowledge, but I did not re-fetch these sources, so they are not counted in claims_checked.

## Problems found but not fixed
None. Minor note: the `screen.py` module docstring says "keep the top K units" where K means the 10 screened units, not the pre-registered K = 5. This is wording, not a factual error, and was left alone.

## Hugging Face card
I read the hosted card at `hf://datasets/BurnyCoder/ouro-1.4b-neuron-atlas/README.md`. It is identical to `DATASET_CARD` in `run_pipeline.py`, so there is no drift. Its claims check out:
- 135,168 neurons and the tensor shapes
- 987,840 tokens per layer and loop: 245 stats batches × 16 × 252
- the 90/10 document mix and the shard names (`data.py`)
- ODC-By licensing of FineWeb-Edu and OpenWebMath
- the main-result wording

No card change was made, so no upload is needed.

## Regenerated artifacts and tests
- `paper/paper.pdf` was rebuilt with `uv run --no-project --with typst==0.15.0 python paper/build.py`. This is the typst version pinned in `uv.lock`. The 14-page PDF text shows the new bounds.
- `reports/tables/` was not regenerated: no result data or table code changed.
- No code was touched, so tests were not run.
