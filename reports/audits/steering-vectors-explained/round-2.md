---
repo: BurnyCoder/steering-vectors-explained
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 195
fixed: 4
unverifiable: 6
not_fixed: 1
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/steering-vectors-explained, round 2

## Summary
I audited the README, the paper (`reports/paper/paper.md`), the experiment reports and pre-registrations, `reports/summary.md`, `reports/all_experiments.md`, AGENTS.md, the docs, `outputs/description.md`, `data/sources.yaml` and the code that produced the results. The repository was already in good shape. Every number I checked in prose and tables matches the result files:
- I recomputed all of them from `data/study/{pilot,main,exp02}.jsonl` with an independent script: means, paired percentile-bootstrap CIs (10,000 resamples, seed 0), d_z, Wilcoxon p, per-seed CIs, ΔNLL and required-N power.
- I checked them against `summary.json`, `exp02_summary.json`, `*_posthoc.json` and `power.json`.

`reports/results_tables.md` regenerates byte-identical from the JSON files. All 40 registry quotes were found verbatim in their downloaded sources (38 with the repository's own `verify_quotes` code, 2 LessWrong quotes by a separate fetch). Citation metadata was checked against arXiv, Crossref, the NeurIPS 2024 proceedings and the ACL Anthology.

I found 4 wrong claims and fixed them:
- the glossary term count, in two places;
- two paper reference titles.

Main verified items:
- Results (README table and paper Table 1):
  - Exp 1 primary +0.125 [+0.045, +0.203].
  - Exp 2 primary +0.146 [+0.102, +0.192] and re-test +0.132 [+0.097, +0.166].
  - α = −5 vs 0: +0.052 [−0.000, +0.105].
  - ΔNLL at α = 15: 1.42/0.84 (Exp 1) and 1.38/0.74 (Exp 2).
  - Spearman ρ: 0.074 and 0.164.
- Post-hoc shares: love 61.4% vs 5.6%, hate 22.5% vs 0.4%, n = 128, positivity 0.665 vs 0.665.
- Power analysis:
  - pilot d_z = 0.633 gives N = 22 (21.6 rounded up);
  - Exp 1 steer(5) − steer(0) d_z = 0.2048 gives N = 190 (189.1 rounded up).
- Per-seed CIs: Exp 2 seeds +0.146, +0.116, +0.177, all excluding 0. Exp 1 lower bounds −0.005, +0.001, −0.041.
- Prompt slices: pilot 0–19, Exp 1 20–49, Exp 2 50–239; labels alternate; 1,440 and 9,120 completions.
- Model facts from `data/practical_example.json`: 48 layers, d = 1600, |V| = 50,257, 1,557,611,200 parameters. Norms 98.0/97.5, cosine 0.715, ‖h_A^(1)‖ = 73.8, ratio 0.82.
- Pre-registration commits come before the data commits on GitHub:
  - `7da591f` 13:14 precedes the pilot data `263123f` 13:32;
  - `23a32f4` 13:39 precedes the Exp 2 data `d7c7076` 14:11.
- ActAdd claims checked against arXiv 2308.10248v5:
  - Algorithm 1 right-pads the prompts;
  - Appendix C on whitespace padding;
  - Appendix F on the zero difference at position 0;
  - the §3 footnote on magnitudes below 15;
  - layer 6 vs 23.
- The ActAdd repository README and `scripts/basic_functionality.py` give temperature 1, freq_penalty 1, top_p 0.3 and `blocks.6.hook_resid_pre` with coeff 5.
- The v1.1 release MP4 runs 872.3 s (14:32) at 1920×1080, 30 fps.
- The test counts are right: 47 non-GPU cases including 1 network test, plus 8 GPU tests.
- Library versions in `uv.lock` match the README: torch 2.11, transformers 5.20, manim 0.22, manim-voiceover 0.4, edge-tts 7.3.
- On the Hugging Face Hub, the GPT-2-XL weights are about 6.4 GB and the SiEBERT card says "15 data sets".

## Fixes
| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| README.md:47 | glossary "maps 51 terms" | "maps 54 terms" | `data/glossary.yaml` (54 entries, 54 unique terms) |
| reports/paper/paper.md:36 | "A glossary maps 51 terms" | "A glossary maps 54 terms" | `data/glossary.yaml` |
| reports/paper/paper.md:142 | Tan et al. "Analyzing the Generalization ..." cited as NeurIPS 2024 | NeurIPS proceedings title "Analysing the Generalisation and Reliability of Steering Vectors", plus arXiv:2407.12404 and its arXiv title | https://proceedings.neurips.cc/paper_files/paper/2024 ; https://arxiv.org/abs/2407.12404 |
| reports/paper/paper.md:143 | Park et al. "... and the Geometry of LLMs" | "... and the Geometry of Large Language Models" | https://arxiv.org/abs/2311.03658 (journal ref ICML 2024) |

## Unverifiable or hedged claims
These were left unchanged because no primary evidence is available in the repository or online:
- paper.md:80 and exp02 report: the v1.0 substring analysis reported "62.5% and 29.5%". This is a historical result. The shallow clone has no v1.0 posthoc JSON.
- paper.md:125 and all_experiments.md: "RTX 5070 Laptop GPU (8 GB) ... about 3 s per batch". The run logs are not tracked.
- all_experiments.md:78: "TransformerLens 4 removed `HookedTransformer`". This is a development history claim with no source.
- all_experiments.md:103: the contact-sheet QA findings for named chapters.
- all_experiments.md:105: "25 errors, fixed in v1.1". This count comes only from the earlier audit file `docs/fact_check.md`, which I did not use as evidence.
- README.md:95: "Windows tested".

## Problems found but not fixed
- `reports/paper/paper.pdf` was not regenerated. The `paper` phase runs pandoc with `--pdf-engine=xelatex`, and LaTeX is not installed here. The PDF therefore still has the old glossary count and reference titles. To rebuild it: `uv run steering-explainer --phases paper`.
- AGENTS.md asks for changed claims to be logged in `docs/fact_check.md`. That log covers the video (narration, on-screen text, citations). My fixes touch only the README and the paper, so I added no rows.

## Hugging Face card
n/a. The repository does not host or link a Hugging Face model, dataset or Space of its own. I read only third-party Hub pages as sources:
- `siebert/sentiment-roberta-large-english` README: it confirms "fine-tuned and evaluated on 15 data sets";
- the `openai-community/gpt2-xl` file listing: `model.safetensors` is 6,431,829,964 bytes, which confirms "about 6.4 GB".

## Regenerated artifacts and tests
- `reports/results_tables.md`: regenerated with `report.write_results_tables` on CPU and came out identical to the committed file (no diff).
- `reports/paper/paper.pdf`: not regenerated (no LaTeX). See above.
- Quote verification: I ran `steering_explainer.sources` against freshly downloaded sources. 38 quotes were found verbatim. The 2 LessWrong quotes failed to download through greaterwrong.com, but I confirmed both verbatim in a direct lesswrong.com fetch.
- Tests: no code was changed, so I ran no tests. The full `uv sync` would download the CUDA torch wheels, which are over 1 GB.
