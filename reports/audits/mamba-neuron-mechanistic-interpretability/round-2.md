---
repo: BurnyCoder/mamba-neuron-mechanistic-interpretability
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 320
fixed: 6
unverifiable: 8
not_fixed: 0
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/mamba-neuron-mechanistic-interpretability, round 2

## Summary
I checked the claims in README.md, reports/paper.md (and its PDF), reports/experiment_01..04, reports/all_experiments.md, reports/preregistration.md, docs/*.md, the viewer (site/app.js, site/index.html, site/data/index.json), the hosted Hugging Face dataset card and the code comments that cite sources. Earlier audit files (reports/audit.md) were not used as evidence.

I recomputed the numbers with short scripts that read the committed result files: activation_shape, split_stability, h1, autointerp, candidates, domain_candidates, screen, screen_low, h2, h2b, h3_mechanism, truncation_survey, judge_validation, steer_validation, vocab_summary and benchmark. I also recomputed them from the archived logs in reports/logs/ (window counts, tokens, throughput, batch sizes, eligible prompts, discarded judge calls, phase wall times). The per-layer medians that come from OUTPUT_DIR (median per-neuron max 0.5 at layer 0, 24–26 in layers 40–45, 22.1 at layer 47; median std 0.01–0.02 rising to 0.35) I checked against the published neuron_stats.parquet (18.6 MB) from the HF dataset. That file also reproduced the kurtosis percentiles and all six split-stability Spearman ρ values.

Nearly everything matched: every number in the README results tables, every number in paper Tables 1 to 6, the H1/H2/H2b/H3 statistics, the Holm adjustments (including the 6-comparison baseline Holm), the word counts, the truncation medians, the κ values with CIs and the power figure (39.7). The same holds for the model config (48 layers, d_model 2048, d_inner 4096, state 16, conv 4; mamba-130m 24/768/1536), the tokenizer size (50,277), the 300B Pile training tokens (Mamba paper and state-spaces/mamba README), and the library versions in uv.lock (torch 2.14.1+cu130, transformers 5.21.0).

I fetched 23 arXiv citations. All IDs, titles, authors and years match, and the sentences citing them are supported, including the AxBench findings and Takahashi et al.'s neuron steering in TopK LMs. I also checked the Goodfire essay (Cammarata, published 2026-10-15; "roughly 90% of neuron poles have one main job" in preliminary Qwen3-32B audits; the double-negative SwiGLU regime), the four DOIs via Crossref, and the Transluce, OpenAI, Neuroscope, Transformer Circuits, Pile, HF and Ollama links. I also checked 58 URLs in code comments.

I found 6 errors, all small: two rounding errors in a screen table that appeared in two places, one rounding error in an NLL value, two wall-time roundings, and one overstated claim about the Goodfire essay. I fixed all of them and regenerated the paper PDF.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| reports/paper.md:216 (Table 2, 20× row) | concept 0.70 | 0.69 | results/mamba-1.4b-hf/screen.json: 271/390 = 0.6949 |
| reports/experiment_03_steering_h2.md:22 (screen table, 20×) | concept 0.70 | 0.69 | results/mamba-1.4b-hf/screen.json (same) |
| reports/experiment_03_steering_h2.md:18 (screen table, unsteered) | NLL 1.14 | 1.13 | results/mamba-1.4b-hf/screen.json: mean unsteered nll 1.13494 |
| docs/reproducibility.md:53 | low-dose sweep "10 min generation" | "11 min" | reports/logs/20261028-123208_all.log.gz: screen_low phase 10.6 min |
| docs/reproducibility.md:53 | "43 min judging" | "44 min" | same log: screen_low_judge phase 43.9 min |
| reports/experiment_02_autointerp_h1.md:47 | "the essay does not describe that audit's procedure" | "the essay describes that audit only in outline (detailed investigations of randomly chosen neurons, with details deferred to a technical companion paper)" | https://already-clean.goodfire.com/ ("Here are 1000 neuron papers, detailed investigations into individual neurons, chosen randomly"; "A technical companion paper will offer a more detailed account") |

## Unverifiable or hedged claims
- docs/reproducibility.md environment table (Windows 11 Home 10.0.26200, RTX 5070 Laptop GPU, driver 591.74, Ollama 0.40.12), the README "tested on an RTX 5070 Laptop GPU, Windows 11" and "Ollama 0.40": none of these appear in the archived logs (the logs only show Windows paths and CUDA). Left as the owner's statement.
- experiment_01 learning 2 (use_mambapy: 2.2k vs 3.6k tok/s, logits differing by up to 153): the report itself says this comes from an agent transcript, not from reports/logs/.
- experiment_01 learning 3 ("7.7 / 8.1 GB used"): the 185 tok/s and batch 16 are in the logs, the memory figure is not.
- experiment_03 learning 4 and amendment 4 ("about 20 s to about 1.2 s per call"; "1.55 vs 1.35 s/call" for parallel requests): the first judge log shows about 18 s per call. The main screen_judge log implies about 1.0 s per call (about 3,000 calls in 49.7 min). This roughly fits "about 1.2 s". The parallel-request figures are not in the logs.
- docs/reproducibility.md "unarchived development spot check" of num_ctx 8192 vs 2048: by its own statement not archived.
- Paper Appendix A, amendment 7 row, "H2 not yet judged": the clone is shallow (one commit), so the order of commits cannot be checked.

## Problems found but not fixed
None. Two loose phrasings were judged acceptable. Experiment 3's "about 8 to 10 times more often" corresponds to a concept-score ratio of 10.6× and a P(concept ≥ 1) ratio of 8.1×. The paper's "whose procedure the essay does not detail" is a fair reading of the outline-only description.

## Hugging Face card
I read the hosted card for datasets/BurnyCoder/mamba-1.4b-neuron-atlas with hf_fs and compared it with the HF_CARD template in src/mamba_neurons/phases/publish.py, filled with κ 0.55, 0.79 and 0.34 from results/mamba-1.4b-hf/judge_validation.json and steer_validation.json. The two are identical apart from CRLF line endings, so there is no drift and no upload is needed. The card's facts check out: 48 × 4096 = 196,608 neurons, 2.32M/0.65M tokens, the pile-10k licence bigscience-bloom-rail-1.0 (per the pile-10k card), and the κ values. The collection and dataset URLs resolve.

## Regenerated artifacts and tests
- Regenerated reports/paper.pdf with `scripts/build_paper.py` (pandoc plus Playwright 1.63.0, which matches the installed Chromium revision 1243). The new PDF shows 0.69 in Table 2.
- No code was changed, so I did not run the tests. The figures and viewer data are generated from result files I did not edit, so they did not need regenerating.
