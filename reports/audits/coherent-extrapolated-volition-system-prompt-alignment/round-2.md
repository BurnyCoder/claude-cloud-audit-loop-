---
repo: BurnyCoder/coherent-extrapolated-volition-system-prompt-alignment
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 220
fixed: 0
unverifiable: 8
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/coherent-extrapolated-volition-system-prompt-alignment, round 2
## Summary
I audited the repository on its own and did not use the earlier audit notes as evidence. I found no factual error,
so nothing changed. No commit was made and nothing was pushed. The $3 budget ran out, so I stopped after covering
README.md (all of it), the generated reports, docs/prompts.md, most of docs/evals.md, the paper abstract and the
cited primary sources. The paper body sections and code docstrings were only checked through the repository's own
tests (`tests/test_paper.py` fails on hand-typed decimals). I did not read them line by line.

What I checked:
- **Numbers.** I wrote my own script (not the repo's `stats.py`) to recompute every pooled contrast from
  `reports/item_scores.csv`: 8 contrasts × 6 evals, with Wilcoxon on differences rounded to 9 decimals and Holm
  within each contrast. All 12 cells of the README primary table match: Δ, Holm p and n agree exactly, and the CIs
  agree to bootstrap noise. So do the secondary-contrast numbers quoted in the README (+0.085/0.010, +0.067/0.024,
  +0.047/0.074, −0.043, the smallest Holm p of 0.68, both HumaneBench Holm p = 0.10).
- **README numbers against report rows.** I checked every README "Results summary" and "Limitations" number against
  the row it describes in `reports/robustness.md`: Holm-12, leave-one-model-out, models as random, missingness and
  tipping point, provider residuals and fixed effects, CEV mentions, subgroups, refusals, blackmail counts,
  judge-blinding, validity, settings and parser checks, and A/B position. Every number is from the right row and
  rounded correctly. I also recomputed directly: "7 of 40" defer-decision pairs, 6,660 samples and 235 unscorable,
  671 = 240 + 239 + 192 re-judged answers, the 12 Claude content-filter stops (5 scored) and the spend.json
  arithmetic (50.2678 − 39.2247 = 11.04; gate 0.9 × 9 − 0.79 = 7.31).
- **Prompts.** Recomputed: CEV 1,189 → 1,165 words; difflib word similarity 0.95497 (autojunk=False), so 0.955 is
  right; classic 79 words; Huxley block 1,170 words, 9.2% shorter by characters; 13 edits. `pytest -m network`
  (verbatim CEV, Llama 2 and Huxley texts, and registry quotes found in CEV.pdf) passes.
- **CEV.pdf.** I fetched it now and confirmed every quoted phrase and printed page number in the README: the §3
  definition on p. 6; "humane" and "trash-talk TV show" on p. 7; "leave options open", "replacing itself" and
  "renormalize" on p. 8; §3 starts on p. 5 and §3.1 on p. 8; the §3.1 quotes are on p. 9; and §2.2's "would
  readily agree", "If Fred says … that settles it" and "Different precautions apply" are on p. 5.
- **Pinned source lines.** Llama 2 `DEFAULT_SYSTEM_PROMPT` at generation.py@6c7fe27657 L46–49. Commit 6c7fe27
  ("remove double-spacing", 2023-07-19). Commit a971c41 (2023-08-04), whose README text is "we recommend the
  removal of the system prompt as the default setting". inspect_ai 0.3.281: `_resolve_config`, `generate`'s
  system-message insertion, `combine_messages` joining with "\n", OpenRouter `collapse_system_messages`.
  inspect_evals v0.24.0: InstrumentalEval system prompt, default grader `openai/gpt-5-nano`, blackmail classifier
  `anthropic/claude-sonnet-4-6`. DarkBench task: "You are a helpful assistant.", temperature 0,
  `tool_calls="none"`.
- **arXiv.** IDs, titles and first authors for HumanAgencyBench, DarkBench, Perez et al., InstrumentalEval,
  Agentic Misalignment, Miller and Bowyer et al. all match. The Bowyer et al. paper does show percentile-bootstrap
  under-coverage at small N, so it supports the sentence that cites it.
- **Datasets.** HumaneBench: 800 prompts, 100 for each of 8 principles. DarkBench: 660 prompts, 110 for each of 6
  categories. The HumanAgencyBench card says MIT licence, 3,000 prompts (500 per dimension), 25 models, ~201 MB
  and an o3 judge. The model-written-evals card says CC BY 4.0. OpenRouter today lists all five model ids, and
  Llama 3.3 70B shows no `reasoning` parameter.
- **Links.** 71 of 100 extracted URLs return 200. The GitHub HTML pages return 403 through this sandbox's proxy,
  so I checked their content through raw.githubusercontent.com or a git clone instead. The rest are template
  strings (`{doi}`), the API base URL (`https://openrouter.ai/api/v1`, a 404 by design) or a doi.org rate limit
  (429).
- **Tests.** The offline test suite passes (98 tests).

## Fixes
| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| (none) | No factual errors found in the surfaces checked | — | see Summary |

## Unverifiable or hedged claims
1. `reports/spend.json` quotes git-ignored run logs (usage-counter readings, the gate line "Projected full run
   $6.45 of $7.31", judge-check cost estimates). The arithmetic is consistent, but the readings cannot be checked
   without the logs.
2. Claims computed from the raw `.eval` logs, which are git-ignored: the manipulation check (0 wrong prompts, 0
   judge leaks), the longest judge reply of 1,352 tokens, and "47 of its 48 finished samples" reused. These are
   only consistent with the generated reports (for example, humanebench classic judged with the cap = 1/192).
3. HumaneBench upstream links (`custom_prompt_task.py#L55-L64` "claude-sonnet-4.5" try/full tiers,
   `scorer_v4.py#L240-L249`, the README phrase "is not a HumaneBench score"). Not fetched this round because the
   budget ran out.
4. HumanAgencyBench rubric reconstruction: "118 of its 121 placeholder-free lines" at upstream e5244e8, and the
   formula reproducing "74,994 of all 75,000 rows". These need the ~200 MB parquet, which I did not download.
5. InstrumentalEval has "76 prompts" and its data is pinned at yf-he/InstrumentalEval commit `2696781`. Not
   fetched.
6. The judge-settings history (commit cfac89c, added mid-run) is a link to a commit that is not in this shallow
   clone. Not fetched.
7. The paper body sections (introduction, related work, discussion, limitations) were not read line by line. Only
   the abstract was read and compared with the evidence.
8. Code comments and docstrings beyond `stats.py`, `config.py` and `.env.example` were not reviewed.

## Problems found but not fixed
None.

## Hugging Face card
n/a. The repository has no Hugging Face model, dataset or Space of its own and no card file. It links two
third-party datasets as data sources. I read both hosted cards with `hf_fs`, and every claim the repository makes
about them matches the cards:
- HumanAgencyBench_Evaluation_Results: MIT, 3,000 prompts (500 per dimension), 25 models, ~201 MB, judged by o3.
- Anthropic/model-written-evals: CC BY 4.0.

No upload is needed.

## Regenerated artifacts and tests
- Nothing was edited, so no generated files (paper/generated/, reports/, the PDF) needed rebuilding, and I did not
  run `--analyze-only` or `make -C paper`.
- `uv run pytest`: 98 passed, 5 deselected.
- `uv run pytest -m network tests/test_claims.py tests/test_prompts.py`: 4 passed (verbatim source texts and CEV
  registry quotes).
