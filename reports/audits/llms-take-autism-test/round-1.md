---
repo: BurnyCoder/llms-take-autism-test
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 105
fixed: 16
unverifiable: 4
not_fixed: 3
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/llms-take-autism-test, round 1

## Summary

Claim surfaces: README.md, AGENTS.md, paper/paper.tex, paper/generated/*.tex (generated from `analysis.py`), paper/paper.pdf, both run figures, the summary CSVs, and the factual constants in `config.py` (item texts, scoring keys, seed, model IDs). The repository has no docs/ folder, no Hugging Face card or link, and no GitHub Pages or other UI.

What I checked:
- I recomputed every summary CSV and every number in the README, AGENTS.md, paper prose and tables from `artifacts/runs/{pilot,pilot-rerun}/responses.jsonl`. All of them match the data, apart from the rounding notes below.
- I confirmed that seed 20260412 reproduces the sampled items: AQ-10 items 1, 2, 3, 6, 7 and adult AQ items 6, 7, 16, 21, 38.
- I downloaded the official ARC sources and ran the repository parser on them. AQ-10 item text and scoring match AQ10.pdf. To get the adult AQ scoring, I converted AQ_Scoring_Key.doc to HTML with LibreOffice and read the "1" marks in its table cells.
- I fetched every URL and DOI, and checked the OpenRouter catalog.

Main findings:
1. **Code bug.** `AQ_ADULT_AGREE_ITEMS` listed item 1 as agree-keyed, and a unit test asserted that bug. The official key marks item 1 ("I prefer to do things with others rather than on my own") as disagree-keyed: the official list is 24 agree items and 26 disagree items. Item 1 was not sampled, so no reported result changes and no re-run is needed.
2. **Misleading omission.** The paper never said that invalid or unparsable items are scored 0 and kept in the denominator. In pilot-rerun, 25 of 160 item responses are invalid. As a result the 0.00 entries for Gemini 3.1 Pro Preview (self-report) and GLM 5.1 (self-report) are entirely formatting failures, not answers. The README also left this out, and it did not say that the paper uses a different run (pilot-rerun) from the one the README reports (pilot).
3. **Unsupported claim.** The paper said scoring directions came from "verified reference lists", and AGENTS.md said they were "cross-checked against public scoring references". Neither holds, given the item 1 error.
4. **Missing sources.** The paper had no citation for the AQ or the AQ-10 themselves, and its NICE reference was never used in the text. I added the primary papers after checking them on Crossref and doi.org.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| src/llms_take_autism_test/config.py:69-73 | `AQ_ADULT_AGREE_ITEMS = {1, 2, 4, ...}` (25 items) | Item 1 removed (24 items), with a comment giving the source | https://docs.autismresearchcentre.com/tests/AQ_Scoring_Key.doc (row 1: disagree columns marked 1) |
| tests/test_sources.py:67 | `items[0].keyed_response == "agree"` | `== "disagree"`, plus a check that item 2 is "agree" | same scoring key |
| src/llms_take_autism_test/analysis.py:157 / paper/generated/results.tex | Means reported with no note on invalid items | Adds: "Invalid or unparsable items were scored 0 and kept in the denominator; 25 of 160 item responses were invalid..." | runner._invalid_rows (score 0); artifacts/runs/pilot-rerun/responses.jsonl (25 rows with valid=false) |
| src/llms_take_autism_test/analysis.py:164 / paper/generated/limitations.tex | "encoded from verified reference lists" | "encoded by hand", plus a note on single-run, temperature-0 design | config.py had item 1 mis-keyed; openrouter.chat_completion (temperature 0) |
| paper/paper.tex:34 | Caption did not name the run | Caption names pilot-rerun and says invalid items are scored 0 | md5 of paper/generated/model_scores.png equals artifacts/runs/pilot-rerun/model_scores.png |
| paper/paper.tex:26,66 | No citation for the adult AQ | Baron-Cohen et al. 2001, JADD 31(1):5-17 | https://doi.org/10.1023/A:1005653411471 (Crossref); reference named in the ARC scoring key |
| paper/paper.tex:26,72 | No citation for the AQ-10 | Allison, Auyeung, Baron-Cohen 2012, JAACAP 51(2):202-212 | https://doi.org/10.1016/j.jaac.2011.11.003 (Crossref); "Key reference" in AQ10.pdf |
| paper/paper.tex:26 | NICE reference listed but never used | States that NICE CG142 suggests considering the AQ-10 for adults with possible autism who do not have a moderate or severe learning disability | https://www.nice.org.uk/guidance/cg142/chapter/Recommendations (rec. 1.2.3) |
| paper/paper.tex:26 | Request settings not stated | temperature 0, max_tokens 500, one retry after a formatting error | src/llms_take_autism_test/openrouter.py, runner._run_single_completion |
| README.md:55 | "The current committed pilot run is `artifacts/runs/pilot`." | Adds that the paper uses pilot-rerun, whose scores differ for DeepSeek, GLM, GPT and Qwen | artifacts/runs/*/summary_by_model.csv; paper/generated/results.tex |
| README.md:57 | No scoring definition | Score = share of the 10 items answered in the scored direction; invalid items count as 0; single run | analysis.analyze_run; runner._invalid_rows |
| README.md:67 | Gemini "unparsable on most sampled items" | Adds "(15 of 20 item responses invalid)" | artifacts/runs/pilot/responses.jsonl |
| README.md:68 | "GLM 5.1 returned empty AQ-10 completions in both conditions." | Saved AQ-10 completions are empty (10/20 invalid); the cause was not logged, and the runner also saves "" after an API error | raw/glm__*__aq10.txt are 0 bytes; runner.py returns "" on exception; benchmark.log has no error lines |
| README.md:20-21, 29 | Sources and requirements | Added the two primary AQ papers and the `strings` requirement | DOIs above; sources._extract_doc_text uses `strings` |
| AGENTS.md:65 | Pilot self-report mean `0.52` | `0.525` (21/40; rounded half-up this is 0.53) | artifacts/runs/pilot/summary_by_model_condition.csv |
| AGENTS.md:26, 71 | "cross-checked against public scoring references"; "GLM returned empty AQ-10 completions" | Item 1 mis-key now recorded as found and fixed; GLM cause marked as not logged | scoring key; raw files |

## Unverifiable or hedged claims

- paper.tex Introduction: "Large language models are frequently described with human psychological language." This is framing with no source. I left it unchanged.
- The cause of GLM 5.1's empty completions (empty model output or an API error). It cannot be recovered: `repair-run` overwrote the notes, and the log has no errors. Hedged in README and AGENTS.
- AGENTS.md: "antiword ... cannot be installed via apt-get ... due permission errors" and "A second benchmark validation pass completed with a replacement OpenRouter API key". These describe the environment and process, and no artifact records them.

## Problems found but not fixed

- **Rounding in generated tables.** pandas `float_format="%.2f"` turns the exact means 0.425 (17/40) and 0.175 (7/40) into 0.42 and 0.17 in `paper/generated/instrument_table.tex`, because of float representation. Rounding half-up would give 0.43 and 0.18. I left the generated file alone and did not change the code.
- **paper/paper.pdf is stale.** It was not rebuilt, because LaTeX is not installed. It still has the old results and limitations text, caption and bibliography. Rebuild with `uv run llms-take-autism-test build-paper --run-label pilot-rerun`.
- **Parser accepts a missing NOTE row.** `runner.parse_completion_table` accepts output without the NOTE row the prompt requires. For example, pilot `gemini__typical-human-roleplay__aq-adult.txt` has no NOTE and counted as valid. Scores are unaffected.
- **Minor, not counted:**
  - `artifacts/benchmark_manifest.json` `created_at` (17:52Z) is later than the pilot run (17:38Z), because a later `prepare` rewrote it. The sampled IDs are identical.
  - `qwen/qwen3-max-thinking` is no longer in the current OpenRouter catalog, which affects reproducibility. The other seven IDs still resolve.
  - AGENTS.md "Current State" has stale workflow notes, such as "existing empty public repo".

## Hugging Face card

n/a. The repository does not link or contain a Hugging Face model, dataset or Space card.

## Regenerated artifacts and tests

- I ran `uv run llms-take-autism-test analyze --run-label pilot-rerun` (CPU only, reads committed responses) after editing `analysis.py`. This regenerated `paper/generated/results.tex` and `limitations.tex`. The CSVs, `model_table.tex` and `instrument_table.tex` came out byte-identical.
- The re-rendered `pilot-rerun/model_scores.png` differed only in bytes (matplotlib rendering), with the same data, so I restored the committed PNG.
- `paper/paper.pdf` could not be regenerated (no LaTeX). pandoc parses the edited `paper.tex` without errors.
- `uv run pytest`: 8 passed. `uv run ruff check src tests`: all checks passed.
