---
repo: BurnyCoder/coherent-extrapolated-volition-system-prompt-alignment
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 350
fixed: 3
unverifiable: 8
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/coherent-extrapolated-volition-system-prompt-alignment, round 1
## Summary
I checked this audit independently and did not rely on the repository's earlier audits. I recomputed all 36 pooled contrasts (diff, n, Wilcoxon p), the 30 pooled cell means and the 30 unscorable shares from `reports/item_scores.csv` with my own code. They match `reports/results.md` exactly. I also compared every number in the README's Results summary and Limitations by hand with the row it describes in `reports/results.md`, `reports/robustness.md` or `reports/robustness/*.csv`. All of them match, including roundings, ranges and leave-one-out, parser, tipping-point and subgroup values. I regenerated `paper/generated/` (except `example.tex`, which needs logs) from `reports/` into a scratch directory. The output is byte-identical to the committed files.

Other checks:
- CEV quotes and page numbers, against the PDF fetched now.
- arXiv titles, authors and venues.
- Llama 2 prompt lines and commit dates, read from a clone of meta-llama/llama.
- Pinned inspect_ai 0.3.281, inspect_evals 0.24.0 and darkbench lines.
- SciPy 1.18.1 `wilcoxon` auto-method logic.
- OpenRouter's model catalog: Llama 3.3 has no `reasoning` parameter.
- HumanAgencyBench and model-written-evals cards.
- HumaneBench upstream README, its judge tiers and TRADEMARKS.md.

I found two small wording errors and one wrong section reference. Each is fixed.
## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| README.md:31 | "a value-neutral verbatim passage of equal word count" | "of nearly equal word count (…; 1,170 words with its header vs the CEV block's 1,165 …)" | `prompts.build_condition_prompts()` (lenmatch adds 1,170 words to the 79-word classic prompt; cev = 1,165); docs/prompts.md table |
| paper/sections/method.tex:11 | "a passage of equal word count" | "a passage of nearly equal word count (\RWordsLenmatch{} against \RWordsClassiccev{} words for the whole prompt)" | paper/generated/numbers.tex (1,249 vs 1,244) |
| docs/evals.md:60 | "TRADEMARKS.md §4.2 asks that the qualifier travel with the name" | "§4.1.3 asks that the qualifier travel with the name every time and that the shortened form not be used; §4.2 says such a score is not comparable … 'HumaneBench' is nevertheless used as the short label" | third_party/humanebench/TRADEMARKS.md §4.1.3 table row and §4.2 |
## Unverifiable or hedged claims
These need the git-ignored `logs/`, which are not in the clone:
- Paper discussion: Qwen blackmail quotes, and "several CEV-invoking answers combined CEV with … American interests".
- `paper/generated/example.tex`: the Claude Haiku replies. I did confirm the "7 of 40" pairs from item_scores.csv.
- "Reused 47 of its 48 finished samples". This fits `judged_with_cap_at_run` = 0.00521 = 1/192.
- `reports/spend.json` key-usage readings. The arithmetic checks out: 50.2678 − 39.2247 = 11.04 and 50.2678 − 49.4374 = 0.83.
- HumanAgencyBench rubric recovery: 118/121 lines, and 74,994 of 75,000 rows reproduced.
- "Primary contrasts fixed in code before either pilot". I did not audit the git history.
- PMLR and ACL page ranges in the bib notes. I checked the venues against the arXiv comments, but not the page numbers.
## Problems found but not fixed
- HumaneBench naming. TRADEMARKS.md §4.1.3 says the "Based on HumaneBench, modified" qualifier travels with the name every time and the shortened form is not used. The repo (README, paper, reports, AGENTS.md convention) still uses "HumaneBench" as a short label after the first mention. Renaming it everywhere, including generated reports, is beyond a minimal fix. The owner should decide, then regenerate.
- `paper/cev-system-prompt-alignment.pdf` was not rebuilt after the method.tex edit, because LaTeX is not installed. Run `make -C paper` and commit the PDF.
## Hugging Face card
n/a: the repository has no Hugging Face model, dataset or Space of its own. I read the cited third-party cards with hf_fs and they match the repo's claims:
- `Experimental-Orange/HumanAgencyBench_Evaluation_Results`: MIT licence, o3 judge, 3,000 prompts (500 per dimension), 75,000 rows, ~201 MB, no subject system prompt for ask_clarifying_questions.
- `Anthropic/model-written-evals`: CC BY 4.0.
## Regenerated artifacts and tests
- Rebuilt the paper numbers and tables from `reports/` into a scratch directory. They are identical to the committed `paper/generated/`, so nothing was committed.
- Did not rebuild the PDF (no LaTeX).
- `uv run pytest`: 98 passed before the edits. `tests/test_claims.py` and `tests/test_paper.py` passed again after them (14 passed).
