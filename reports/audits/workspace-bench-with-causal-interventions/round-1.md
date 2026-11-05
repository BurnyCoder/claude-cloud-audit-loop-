---
repo: BurnyCoder/workspace-bench-with-causal-interventions
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 84
fixed: 17
unverifiable: 8
not_fixed: 3
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/workspace-bench-with-causal-interventions, round 1

## Summary

I worked from the files readers see first: README.md, then docs/causal.md (the experiment report for this fork), then NOTICE.md, CITATION.cff and the user_modeling and wrong_bridge family READMEs. I checked the claims against:
- the item banks (`evals/*/items.json`, `items_manifest.json`, the J-lens token files);
- the code (`wsbench list`, `scripts/causal_check.py`, `produce/intervene.py`, `split.py`, `llm.py`, `capable/`);
- primary sources fetched during the audit: arXiv abstract pages, the Transformer Circuits paper HTML, shallow clones of `anthropics/jacobian-lens`, `safety-research/jpp_lens` and `anthropic-experimental/agentic-misalignment`, Hugging Face dataset and model cards through `hf_fs`, and the Transluce page.

I recomputed every internally checkable number in docs/causal.md with a script that uses the repository's own `wilson` and `mcnemar` formulas: the Wilson CIs, the McNemar p-values, the ratios and the count arithmetic. They are all consistent. The raw `outputs/causal/*.jsonl` files are git-ignored, so I could not recompute the result values themselves.

Most important errors:
1. The wrong_bridge example quotes a prompt that is not in the bank. It appeared in three files.
2. The pile-10k licence was wrong.
3. docs/causal.md misattributed its layer band to the paper.

I stopped at the $5 budget. docs/plan0012_results.md, docs/small_model.md, the other docs and most family READMEs were not audited (see "Problems found but not fixed").

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| README.md:113 | "Canon and Gigue in D **died** in the year" -> `1750` via Bach, not Pachelbel's 1706 | "**was born** in the year" -> `1685` via Bach, not Pachelbel's 1653 | evals/wrong_bridge/items.json (item `composition_composer-Q689519-birth_year`: target 1685, correct_answer 1653) |
| evals/wrong_bridge/README.md:5-6 | the same died / 1750 / 1706 example | born / 1685 / 1653 | evals/wrong_bridge/items.json |
| evals/wrong_bridge_true/README.md:5-6 | the same died / 1750 / 1706 example | born / 1685 / 1653 | evals/wrong_bridge_true/items.json (same prompts) |
| README.md:407 | pile-10k and fineweb-edu "(ODC-BY)" | pile-10k: BigScience BLOOM RAIL 1.0 per its dataset card; fineweb-edu: ODC-BY | hf://datasets/NeelNanda/pile-10k/README.md (`license: bigscience-bloom-rail-1.0`) |
| README.md:405-409 | all four corpora supply "verbatim first user turns in the hallucination bank" | LMSYS (74) and DailyDialog (75) supply the hallucination turns; all four seeded jlens_concept_pr | evals/hallucination/items.json (`source` counts); evals/jlens_concept_pr/items_manifest.json (`per_source`) |
| NOTICE.md:142 | "Licence: ODC-BY" for pile-10k + fineweb-edu | split: fineweb-edu ODC-BY; pile-10k card declares bigscience-bloom-rail-1.0 | the same HF cards |
| NOTICE.md:31 | Lynch, Wright, Larson, Troy, Ritchie, Mindermann, Perez, Hubinger | Lynch, Wright, Larson, Ritchie, Mindermann, Hubinger, Perez, Troy | https://arxiv.org/abs/2510.05179 |
| NOTICE.md:37 | "MIT. Copyright (c) Anthropic" | "Copyright (c) 2025 Aengus Lynch" | LICENSE in github.com/anthropic-experimental/agentic-misalignment |
| NOTICE.md:53 | title "*CHIVE.*" | *Would this change your answer? Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments* (the CHIVE pipeline) | https://arxiv.org/abs/2608.16747 |
| NOTICE.md:95 | title "*The J++ Lens.*" | *J++ Lens: Jacobian Filtering Enables More Faithful Workspace Lenses*, LessWrong, 2026 | jpp_lens README (citation block) |
| NOTICE.md:63-64 | "the revealed-belief gate (≥ 8/10) is their [Transluce's] criterion" | the revealed-belief idea is Transluce's (their filter: p(a) > p_baseline(a) + ε, ε = 0.01); the ≥ 8/10 gate is the source repo's | https://transluce.org/user-modeling; src/wsbench/capable/run.py:22 |
| evals/user_modeling/README.md:5-6 | the same Transluce ≥ 8/10 attribution | the same correction | the same sources |
| docs/causal.md:14-15 | "290 prompts. 66 of them are answered correctly by the clean model" | 69 are clean-correct; 66 enter the primary test after 3 probe-swap repeats are counted once | docs/causal.md's own tables (20+28+21 = 69; 17+28+21 = 66) |
| docs/causal.md:55 | "blocks 9–19 of 24, the paper's L38–83 band rescaled" | L38–83 rescaled. The paper indexes layers 0–100; its workspace band is ~L38–~L92 and its swaps use the full band; L38–83 is only an averaging range in Fig. 45 | https://transformer-circuits.pub/2026/workspace/index.html ("~L38 … ~L92"; "all swaps are applied at the full workspace layer range"; "mean over L38–83" in Fig. 45) |
| docs/causal.md:225 | quote attributed to "(jacobian-lens README)" | "(jacobian-lens `data/experiments/README.md`)" | anthropics/jacobian-lens@581d398, data/experiments/README.md:16-17 (the top-level README does not contain the quote) |
| docs/causal.md:390 | J++ Lens (Ayonrinde and Lindsey), no title | added the title, venue and year | jpp_lens README |

## Unverifiable or hedged claims

- **J++ swap rate.** "J++ gets 49% with the J-lens on Qwen3.6-27B" (docs/causal.md:29, 303, 364). The LessWrong post nc9dHfcB22JdMzGbr renders client-side (179 characters of text came back), and the jpp_lens repo has no such number. The sentences are left as written.
- **Ablation and swap result values in docs/causal.md.** Δlog p, KL ratio 6.20, Spearman +0.43, the n=249 and n=15/43 secondary splits, median rank gains, and the answer-swap per-set counts. They come from `outputs/causal/*.jsonl` and `summary.md`, which are git-ignored and not in the repo. Their internal arithmetic is consistent (sums, ratios, Wilson CIs, McNemar p-values, discordant-pair counts against the top-1 counts).
- **Run times.** "about 7 minutes … about 18 minutes" (docs/causal.md:16-17).
- **Judge history.** README:346-350, "Five families … were judged with claude-opus-5 in their source scripts": the source scripts are not in the repo.
- **Quote.** README:301, the quoted maintainer instruction "regex on the multitoken please".
- **Write-up authors.** README:422-427 and CITATION.cff list four authors. The LessWrong title matches, but the author list is not in the static HTML.
- **Lens artifact.** README:403-404, "n1000 wikitext artifact": not checked against the neuronpedia lens metadata.
- **Model depth.** split.py's `MODEL_LAYERS = 64` for Qwen3.6-27B was not checked against the model config. The README's 20–52 grid band is arithmetically correct given 64.

## Problems found but not fixed

- **Upstream URLs.** The Quickstart `git clone https://github.com/camilablank/workspace-bench` and CITATION.cff `repository-code` point to the upstream repo, which exists (HEAD 2ae3911). They do not point to this fork, which adds docs/causal.md and `scripts/causal_check.py`. It is not a factual error for the upstream project, so I left it for the maintainer to decide.
- **Answer-swap denominators.** docs/causal.md:339-340 reports the answer-swap ceiling as "9/13 multihop and 9/18 probe-swap at scale 1". The 9/18 denominator looks non-deduplicated, while the primary table uses 17 for probe-swap. This cannot be resolved without swaps.jsonl.
- **Hallucination credit column.** The `wsbench list` credit column for hallucination shows only "LMSYS-Chat-1M", but 75 of the 149 items are DailyDialog. Fixing it means changing the `EvalSpec.sources` code, which `tests/test_readme.py` couples to the README and NOTICE, so I left it.
- **Not audited, out of budget.** docs/plan0012_results.md, docs/small_model.md, docs/summarizer.md, docs/producing_readouts.md, docs/read_sites.md, AGENTS.md, plans/, most `evals/*/README.md` (numbers and gate claims), and evals/multihop_mt/AUDIT_2026-10-15.md (an earlier audit, deliberately not used as evidence).

## Hugging Face card

n/a. The repository does not publish or link its own Hugging Face model, dataset or Space card. It references third-party Hub repos only. I checked the cited facts in those cards:
- `neuronpedia/jacobian-lens`: Apache-2.0, and `qwen3.5-0.8b/{jlens,jpp,oracle}` exist.
- `Qwen/Qwen3.5-0.8B`: 24 hidden layers.
- Dataset licences: `ConvLab/dailydialog` CC BY-NC-SA 4.0, `HuggingFaceFW/fineweb-edu` ODC-BY, `allenai/WildChat-1M` ODC-BY, and `NeelNanda/pile-10k` bigscience-bloom-rail-1.0 (that last one was wrong in the repo and is now fixed).

No upload is needed.

## Regenerated artifacts and tests

- No generated artifacts depend on the edited files. There are no figures and no paper build, and the docs are hand-written markdown.
- No code was changed.
- `uv run --extra dev pytest -q`: 582 passed, 1 skipped. This includes `tests/test_readme.py` and `tests/test_prompts_in_readme.py`, which cover README and NOTICE content.
