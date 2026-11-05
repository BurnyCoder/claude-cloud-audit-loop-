---
repo: BurnyCoder/steering-vectors-explained
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 240
fixed: 14
unverifiable: 6
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/steering-vectors-explained, round 1
## Summary
I checked the README, the paper source (`reports/paper/paper.md`), all reports in `reports/`, the docs (storyboard, architecture), the narration (`data/script.yaml`), the shipped subtitles (`outputs/steering_vectors_explained.srt`), the video description, the source registry and the exp02 figure. Evidence came from the result files and from primary sources. Earlier fact-check files were not used as evidence.

- **Numbers.** A script recomputed every headline number from `data/study/{pilot,main,exp02}.jsonl`: means, paired bootstrap CIs (10,000 resamples, seed 0), d_z, power N, post-hoc whole-word rates, and the v1.0 substring rates (62.5% / 29.5%). All matched `summary.json`, `exp02_summary.json`, `power.json`, `*_posthoc.json` and `results_tables.md`. The practical-example numbers match `data/practical_example.json`. The numbers spoken in the SRT match the data. The exp02 figure matches the summary.
- **Quotes.** All 40 registry quotes are verbatim in their sources. I re-ran the repository's own `verify_quotes` code on fresh downloads; the 2 LessWrong quotes were checked through a GreaterWrong mirror.
- **Citations.** The citation metadata (authors, venues, pages, arXiv IDs) is correct. Tan et al.'s author order matches arXiv v8.
- **Other checks.** The cited ActAdd details are confirmed: footnote 2 "magnitude less than 15", Appendix F position-0, Algorithm 1 padding, the README `get_x_vector(coeff=5, act_name=6)` with default `pad_method=None`, and `basic_functionality.py` sampling settings. The CAA claims are confirmed: answer-letter position, all positions after the prompt, "hundreds of … pairs reduces noise". The "15 datasets" claim for SiEBERT matches its card. The pre-registration commits precede their data: `7da591f` 13:14, then pilot, then exp01 data, then `23a32f4` 13:39, then exp02 data at 14:11.

Most content is accurate. The errors were a stale quote count in the paper, a rounding error in the baseline range, and several overclaims: per-seed robustness, fluency vs random at α ≥ 10, and an unscoped "peak at α = 10".

## Fixes
| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| README.md:79 | "Mean positivity is highest at α = 10 and lower at α = 15" (no experiment named) | scoped to experiment 02; notes that exp01 peaks at α = 5 | data/study/summary.json, exp02_summary.json `means.p_pos` |
| README.md:81-83 | "The whole word "love" appears in 61.4%…" | names the experiment and the word forms counted (love/loves/loved/loving/lover(s); hate forms) | data/study/exp02_posthoc.json `patterns`, `rates` |
| README.md:214 | "20 non-GPU tests incl. 1 network test" | "47 non-GPU test cases incl. 1 network test" | `pytest --collect-only` (45 items + 2 in test_tts_edge.py; 8 GPU in test_steering.py) |
| reports/paper/paper.md:34 | "All 26 quotations live in one registry" | "All 40 quotations (28 of them shown on screen)" | data/sources.yaml (40 quotes; 28 referenced by script/scenes) |
| reports/paper/paper.md:111 | "baseline positivity 0.67–0.75" | "0.66–0.75" | exp02 steer_0 = 0.6649; exp01 = 0.7543 |
| reports/paper/paper.md:6 (abstract) | "the whole word "love" … "hate"" | "a whole-word form of "love" … a form of "hate"" | data/study/exp02_posthoc.json `patterns` |
| reports/paper/paper.md:93 | "Mechanically it adds the token identity of "H"/"ate"" | adds α(h(p⁻)−h(p⁺)), i.e. "H"/"ate" minus "Love"/space activations; post-hoc, its main visible effect is the word "hate" | src/steering_explainer/steering/vectors.py; exp02_posthoc.json |
| reports/all_experiments.md:78 | "(pre-registered, replicated, per-seed robust)" | random contrast replicated in exp02; per-seed robust only in exp02 (2 of 3 exp01 per-seed CIs include 0) | summary.json `primary_per_seed` |
| reports/all_experiments.md:80 | "relative to both no steering and … random" | no-steering effect is exp02 only (exp01 +0.056, CI incl. 0) | summary.json `secondary[steer_5 - steer_0]` |
| reports/all_experiments.md:82 | "more so than random pushes of equal norm at α ≥ 10" | "at α = 15 (random tested only at α = 5, 15; at α = 5 about equal)" | exp02_summary.json `fluency` (steer_5 0.368 vs random_5 0.358; steer_15 1.380 vs random_15 0.741) |
| reports/all_experiments.md:92 | "baseline positivity was already 0.67-0.75" | "0.66-0.75" | exp02_summary.json steer_0 mean 0.6649 |
| reports/exp02_powered_replication.md:103 | "exceeds the random control at equal norm" (incl. α = 5) | exceeds it at α = 15; about equal at α = 5 (overlapping CIs) | exp02_summary.json `fluency` |
| reports/exp02_powered_replication.md:129 | "it is "+Hate token identity"" | adds "Hate" minus "Love" activations; post-hoc, mostly injects the word "hate" | vectors.py; exp02_posthoc.json |
| reports/exp01_love_hate_dose_response.md:50 | "barely touches 0 (seeds 0 and 2)" | "includes 0 (seeds 0 and 2, lower bounds −0.005 and −0.041)" | summary.json `primary_per_seed` |

## Unverifiable or hedged claims
- Hardware and timing: "RTX 5070 Laptop GPU (8 GB) … about 3 s per batch" (paper Appendix A, all_experiments.md). There are no logs in the repository; `logs/` is untracked.
- Video length 14:32 and the chapter timestamps (README, description.md). The MP4 Release asset exists (v1.1, 44 MB) but I did not download it. The SRT ends at 14:30.7, which is consistent.
- "TransformerLens 4 removed `HookedTransformer`" (all_experiments.md, issue 1). This is a development anecdote and was not checked against TransformerLens releases.
- Visual QA statements: contact sheets inspected, chapters with clipped text fixed.
- "Windows tested" (README install section).
- The pyproject comment says Pillow 13 removed `mode`, but the pin is `pillow<12` (locked 11.3.0). The pin is stricter than the comment needs. The comment was not checked against Pillow release notes.

## Problems found but not fixed
- `reports/paper/paper.pdf` is generated from `paper.md` with Pandoc + XeLaTeX. LaTeX is not installed here, so the PDF was not rebuilt and still shows the old text: "All 26 quotations", "0.67–0.75", "token identity". Rebuild it with `uv run steering-explainer --phases paper`.
- The v1.1 GitHub Release asset `paper.pdf` has the same stale text. It needs re-uploading after the rebuild.
- (Note) AGENTS.md asks for a `docs/fact_check.md` row whenever narration, on-screen text or a citation changes. None of the fixes above touched narration, scenes or citations, so I added no rows.

## Hugging Face card
n/a. The repository links no Hugging Face model, dataset or Space of its own; the only HF link is the third-party SiEBERT model. I searched `hf://models/BurnyCoder`, `hf://datasets/BurnyCoder` and `hf://spaces/BurnyCoder` and found no repository for this project. The SiEBERT card confirms "fine-tuned and evaluated on 15 data sets".

## Regenerated artifacts and tests
- No code was changed, so I did not run the repository tests. I did run the network quote check: the repository's `sources.verify_quotes` logic on freshly downloaded sources, plus WebFetch for the LessWrong post. All 40 quotes verified.
- Tables and figures were not regenerated, because no result data or generating code changed. `results_tables.md` and the exp02 figure already match the summary JSONs.
- The paper PDF was not regenerated (no XeLaTeX); see above.
