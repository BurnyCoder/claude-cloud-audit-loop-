---
repo: BurnyCoder/auto-but-actually-fact-checker-evaluator
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 240
fixed: 1
unverifiable: 17
not_fixed: 1
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/auto-but-actually-fact-checker-evaluator, round 2

## Summary

I checked claims independently and did not use earlier audit files as evidence. The main method was to run the
repository's CPU analysis scripts (`analyze_scifact.py`, `analyze_correction.py`, `analyze_ai_errors.py`,
`exp08_posthoc.py`) on the committed raw records. They reproduced `scifact_analysis.json`,
`correction_analysis*.json`, `verdict_vs_correction_posthoc.json` and `ai_errors_analysis.json` byte for byte.
I then compared the numbers in prose and tables (README, paper.typ, all_experiments.md, exp02/exp07/exp08
reports, benchmark README) with those JSONs. I also recomputed some numbers directly from the per-item jsonl and
the frozen dataset with my own scripts: 40-claim subset AUROCs, Exp07 final self-ratings, Exp08 word counts,
edit counts and the k distribution, and raw vs frozen QC diffs.

What else I checked:
- **Paper bibliography:** all 23 entries. 13 against the arXiv API, 7 DOIs via Crossref and 2 via PubMed.
  The rest were checked by the stated DOI/ACL pages.
- **Example answer-key sources:** 17 arXiv IDs.
- **Links:** 128 URLs. Every non-GitHub, non-DOI URL returned HTTP 200. The DOIs resolve in Crossref. GitHub
  URLs are blocked by the sandbox proxy, but the SciFact LICENSE was read via raw.githubusercontent.com.
- **Pricing and API claims:** checked against the current OpenAI pricing and prompt-caching pages, Anthropic
  pricing and web-search docs, and the installed gradio 6.30.0 `analytics.py`.
- **Config defaults:** docs/configuration.md vs config.py and ui.RANGES.
- **Pre-registration timing:** the commit times of `378c59b`, `f681d49` and `a2b7759` (GitHub API) against the
  first run IDs.
- **Sample size:** Connor's n ≈ 155.

Almost every checked claim matched its evidence. One completeness issue was fixed.

## Fixes

| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| benchmarks/ai_errors_v1/README.md:72-73 | "Six were edited: four repairs (...) and two type relabels:" (implies only 2 label changes) | Adds that the two incoherent-edit repairs also changed the error-type label (Transformer 2 "wrong number" → negation; Transformer 5 "absurd overclaim" → negation), and that the other raw labels differ only by the canonical long names | benchmarks/ai_errors_v1/dataset_raw.jsonl vs benchmarks/ai_errors_v1/dataset.jsonl (`error_type` field) |

## Unverifiable or hedged claims

These rely on ignored local `runs/` or `logs/` artifacts that are not published. The repository already labels
each of them as coming from local logs:
- B vs C output tokens: 3,562 vs 420 per claim, 8.5× (exp02 report, paper, all_experiments).
  The token arithmetic is plausible from the costs, but the numbers cannot be recomputed.
- README Exp00 example run `20261017_210452_...`: scores 99%, 95%, 15%, 5%, 68% and 91%, plus 3 searches and
  $0.039. That is 8 claims.
- Exp00 run counts: 42 verdicts agreed, nine runs, 49 calls.
- Ledger totals: $7.35 (2,953 entries), $7.55 (3,004 entries), one entry with unknown cost, and the ≤ $0.17
  cache-write understatement. That is 5 claims.
- Exp08 per-pass time and tokens (18 s / 1.5k, 110 s / 18k): these match the committed
  `exp08_posthoc.json`. Regenerating them needs the missing runs; the script then writes `available: false`.

## Problems found but not fixed

- In paper.typ, the comparison table shows E − C as "3 / 1, 0.62". The exact McNemar p is 0.625
  (`scifact_analysis.json`). Half-up rounding gives 0.63, and the paper text uses half-up elsewhere (45.75 →
  45.8). This is a rounding-convention inconsistency, not a factual error, so I left it.
- Not a problem, for the record: the Efron & Tibshirani DOI's Crossref record is dated 1994 (CRC reissue),
  while refs.yml says 1993, the first-edition year. Both are defensible, so I made no change.

## Hugging Face card

The repository links no Hugging Face model, dataset or Space of its own (`hf://models|datasets|spaces/BurnyCoder`
lists none for this project), so there is no card to compare and nothing to upload. The only Hub link is the
third-party `allenai/scifact` dataset. Its hosted card lists `cc-by-nc-2.0`, which matches the README statement.

## Regenerated artifacts and tests

- I ran `uv sync --locked --all-groups` and then the four analysis scripts.
- The derived JSONs regenerated with no diff, except `exp08_posthoc.json`, which loses its `per_pass` values
  because the local `runs/` are missing. The figure PNG/PDF bytes changed (runtime rendering).
- I reverted all regenerated files, so the committed artifacts are unchanged.
- `compare_verdict_correction.py` needs the ignored `runs/` and could not be run.
- I did not rebuild the paper PDF or the screenshots, because no source of theirs changed.
- Tests: `pytest tests/test_docs.py tests/test_evidence.py` gave 9 passed. Only a Markdown file was edited.
