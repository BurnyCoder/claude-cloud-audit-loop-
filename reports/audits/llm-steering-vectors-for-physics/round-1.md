---
repo: BurnyCoder/llm-steering-vectors-for-physics
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 80
fixed: 13
unverifiable: 2
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/llm-steering-vectors-for-physics, round 1

## Summary

The repository contains code, README.md, AGENTS.md, a LaTeX paper (`paper/paper.tex`) and its PDF. It has no committed result files, no figures, no web UI and no linked Hugging Face card. So no reported numbers needed recomputing. The claims checked were method and configuration details, the citation, the links, the code comments that cite sources, and the counts of the MMLU-Pro physics splits.

Evidence used:
- the code and config at HEAD
- the git history, deepened to 43 commits
- the source of the steering-vectors 0.12.2 wheel pinned in `uv.lock`
- the Qwen2.5-0.5B-Instruct `config.json` and `generation_config.json`, read through `hf_fs`
- the MMLU-Pro parquet files, with rows counted by a script
- the official MMLU-Pro `initial_prompt.txt` and `evaluate_from_local.py`
- the arXiv abstract page for 2308.10248
- the HF Transformers docs pages

Main findings:
- **The paper names the wrong model.** It said the codebase uses Qwen3.5-0.8B. Commit 314d421 (2026-05-18) switched `config.py` to `Qwen/Qwen2.5-0.5B-Instruct`, and the paper was never updated after that.
- **README and AGENTS.md give the wrong default for `max_test_examples`.** Both implied it is `None`. Since commit 92624de it has been `5`, so a default run scores only 5 of the 1,299 physics test rows.
- **The example results table in the README looked like real results** and was not labelled as illustrative.
- **Inherited decoding settings are undocumented.** `repetition_penalty=1.1` and `top_k=20` come from the checkpoint's `generation_config.json`. Neither the paper nor the README mentioned them.
- **The paper's formulation leaves out the chat template.** It defines generation on `tok(s)`, but the code wraps prompts in the chat template with an assistant prefill. Training activations are read without the template.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| README.md:88-95 | "temporarily set" `max_test_examples = 25` (implies the default is None) | the committed default is `5`; keep it or use 25 for smoke tests | src/physics_steering_vectors/config.py:52; commit 92624de |
| README.md:111-114 | (no split sizes) | the physics category has 1,299 test and 5 validation rows; at most 20 sampled training responses by default | https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro (parquet rows counted); config.py:53 |
| README.md:159-160 | "A final table like:" | the table numbers are illustrative placeholders; no results are committed | `git ls-files` (no result files) |
| README.md:235-239 | (missing) | inherited `repetition_penalty=1.1` and `top_k=20` from generation_config.json | https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/main/generation_config.json; https://huggingface.co/docs/transformers/main_classes/text_generation (kwargs override the model's default generation config) |
| README.md:252-257 | the tree omits `.gitmodules`, `.vscode/launch.json` and the `ALS` submodule | added | `git ls-files`; .gitmodules |
| README.md:319 | `device_map="auto"` | "(passed only when CUDA is available)" | src/physics_steering_vectors/modeling.py:218-219 |
| README.md:363 | "optional cap for smoke tests" | currently `5`; `None` for the full split | config.py:52 |
| README.md:482-484 | "final token activation from each positive/negative prompt pair" | prompt-plus-completion pair; the library's `mean_aggregator()` averages the differences | activation_collection.py:155; steering_vectors 0.12.2 `aggregators.py` and `train_steering_vector.py` |
| paper/paper.tex:13 | "This paper tests whether ..." | "formalizes an experiment that tests whether ...; it reports no benchmark results" | no result files in the repository |
| paper/paper.tex:127 | `M_θ = Qwen3.5-0.8B`, a Qwen3.5 transformer | Qwen2.5-0.5B-Instruct, a Qwen2 decoder-only transformer with 24 layers | config.py:41; commit 314d421; https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/main/config.json |
| paper/paper.tex:142 | (missing) | generation uses the chat template with an assistant prefill; training activations are read from the raw `p_i‖g_ik` | generation.py:392-420; steering.py:350-360 |
| paper/paper.tex:143 | (missing) | inherited `top_k=20` and `repetition_penalty=1.1`; greedy evaluation | generation_config.json URL above; config.py:67 |
| paper/paper.tex:144 | (missing) | default `m=5` test-row cap; u=5 validation and 1,299 test physics rows | config.py:52; MMLU-Pro parquet counts |
| AGENTS.md:24 | "temporarily set `max_test_examples` to a small value such as 25" | the default is already 5; set `None` for a full run | config.py:52 |

These rows cover 13 counted fixes. The first two README rows together count as one fix (the smoke-test default).

Claims verified and left unchanged:
- V=4, T=0.8, q=0.95, L={6,12,18} and A={0.5,1.0,1.5,2.0} match config.py. Layers 6, 12 and 18 exist, since the model has 24 layers.
- τ is the last non-padding position. This matches `adjust_read_indices_for_padding` in steering-vectors.
- `v_ℓ` is the mean of the pair differences (`mean_aggregator`).
- Steering adds `α·v_ℓ` at every token: `min_token_index=0` with an additive forward hook.
- P and N exclude unparsable responses. The pools are shuffled with a seed and truncated to min(|P|,|N|).
- The definitions of Acc and Δ match evaluation.py and reporting.py.
- The arXiv:2308.10248 title, authors, year and URL are correct. The current title is v5, revised 2024-10-10.
- The MMLU-Pro `{$}` placeholder, the `stop=["Question:"]` setting, the removal of N/A options, the `A:`→`Answer:` rewrite and the 10-option format all match the official repository.
- The EOS IDs [151645, 151643] match generation_config.json.
- The default `layer_type` of `train_steering_vector` is `decoder_block`.
- The dependency pins in pyproject.toml and uv.lock, and `.python-version` 3.14.2, match the README.
- The README's main-flow code block matches main.py.
- The artifact paths and payload keys match the code.
- 23 cited URLs were checked. All resolve, apart from github.com URLs, which the proxy blocks for curl. Their content was confirmed through raw.githubusercontent.com.

## Unverifiable or hedged claims

- `config.py:51` has the comment `max_new_tokens = 16384  # allow 4x the 4096-token response budget`. No source for a "4096-token response budget" was found. The official MMLU-Pro `evaluate_from_local.py` uses `max_new_tokens = 2048`. The comment was left unchanged.
- I could not read the `ALS` submodule (https://github.com/BurnyCoder/ALS.git). It is not initialized in the clone, and the GitHub API is not enabled for it in this session. The README makes no claims about its contents.

## Problems found but not fixed

- **`paper.pdf` is now out of date compared with `paper/paper.tex`.** Its text matched the old tex exactly, including Qwen3.5-0.8B. LaTeX is not installed here, so the PDF was not regenerated; it needs a `pdflatex paper/paper.tex` run.
- **`answer_extraction.py:252` behaves differently from the source it cites.** The fallback `[Aa]nswer:\s*([A-J])` with `re.search` returns the first "Answer: X". The official script uses `.*[aA]nswer:\s*([A-J])`, which returns the last one. The comment says "MMLU-Pro extraction style", which is a hedge. Changing the code would change scoring, so it is left to the owner.

## Hugging Face card

n/a. The repository links no Hugging Face model, dataset or Space of its own, and none of the `BurnyCoder` models or datasets on the Hub match this project. It only references the third-party `Qwen/Qwen2.5-0.5B-Instruct` and `TIGER-Lab/MMLU-Pro`.

## Regenerated artifacts and tests

- `paper.pdf` was not regenerated, because LaTeX is unavailable. `pandoc paper/paper.tex -t plain` parses the edited source without errors.
- No code was changed. Only Markdown and LaTeX prose were edited, so `uv run pytest` was not run. A test run would also need the pinned torch 2.12.0 Linux wheel with its CUDA dependencies, which is over the 1 GB download limit.
