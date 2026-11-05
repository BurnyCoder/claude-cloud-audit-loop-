---
repo: BurnyCoder/auto-but-actually-fact-checker-evaluator
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 470
fixed: 7
unverifiable: 23
not_fixed: 1
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/auto-but-actually-fact-checker-evaluator, round 1
## Summary

I checked the README, the paper (`reports/paper/paper.typ` and `refs.yml`), `reports/all_experiments.md`, the
Exp00–Exp08 reports, the frozen benchmark README, and `docs/benchmark.md`, `docs/configuration.md` and
`docs/examples.md`. I also checked the claims about the price catalog, backend flags and Gradio, plus figure 1.
I did not use the earlier audit records (`reports/verification_2026-10-28*.md`) as evidence.

How I checked:
- **Analysis scripts.** I re-ran all four (`analyze_scifact.py`, `analyze_correction.py`, `analyze_ai_errors.py`,
  `exp08_posthoc.py`). Every derived JSON came out byte-identical, except the `per_pass` block of
  `exp08_posthoc.json`, which needs the private `runs/`. I reverted that block.
- **Spot checks with separate scripts.** I recomputed from the raw jsonl:
  - Wilson CIs and exact McNemar p-values
  - AUROC on the 40-claim subset
  - medians by gold label, refusals and leak flags
  - the Exp07 harm and threshold facts
  - Exp08 word counts, judge differences and control behaviour
- **Data and sampling.** I recomputed the SciFact pool counts from the Hugging Face parquet export (124/64, 332/173).
  The seed-0 main sample and the seed-999 pilot sample both reproduce exactly.
- **Sources.** I checked all 23 bibliography entries against Crossref, PubMed E-utilities, the HF papers metadata
  and arXiv, and fetched the vendor docs: Anthropic pricing and web search, OpenAI prompt caching and the gpt-6-luna
  page, and Claude Code subagents. I also fetched the SciFact licence and the arXiv licence and metadata pages.
- **Timing.** I compared each pre-registration commit time with the run-ID timestamps.

The repository is in good shape. Almost every number matches the records. The fixes are narrow:
- one wrong word in the README ("above" a threshold where 9 of 100 final ratings sit exactly at it)
- a timing claim broader than the evidence ("before any paid call")
- a CI interpretation that read as a formal exclusion
- a token-count source that is not published
- a stale limitation about Codex delegation

## Fixes

| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| README.md:118 | "self-rated all final answers above its stopping threshold" | "at or above its 90% stopping threshold (9 of 100 exactly at 90%)" | `reports/results/exp07_correction_codex/loop_codex_search.jsonl` (min final self_accuracy 90.0; 9 values exactly 90) |
| reports/paper/paper.typ:85 | "was committed before any paid call" | "was committed (commit `378c59b`, 2026-10-17 14:09) before any benchmark call; the first pilot run started at 14:22" | `git show 378c59b`; run IDs in `reports/results/exp01_pilot/*.jsonl` start `20261017_142214`. Earlier development or live-test calls are not dated in the repo (commit `4f549f4` "live-tested …" is 14:18) |
| reports/experiments/exp01_scifact_baseline_vs_full.md:3-4 | "before any paid LLM call" | "before any benchmark call (the first pilot run ID is `20261017_142214`)" | same as above |
| reports/paper/paper.typ:151-152 | "B produced 3,562 output tokens per claim on average, vs 420 for C." | the same sentence, plus "(from local run logs, which are not published)" | The committed per-item records have no token fields (`reports/results/exp01/*.jsonl`, `exp02/*.jsonl`) |
| reports/experiments/exp02_search_ablation.md:39 | "3,562 … vs 420 for C (8.5×)," | the same, plus "; from local run logs, which are not published" | same as above |
| reports/experiments/exp02_search_ablation.md:37-38 | "What the CI does rule out: a gain of more than about 1 pp" | "The 95% CI's upper limit is about +1 pp: larger gains … lie outside this interval, but no noninferiority or equivalence test was specified." | `reports/results/scifact_analysis.json` B−C ci95 [−0.0606, +0.0096]; `docs/benchmark.md` (no equivalence test pre-registered) |
| reports/paper/paper.typ:292-293 | Limitation: "Codex … never actually spawned a sub-agent and twice reported a fabricated sub-agent answer." (no update) | adds "A 2026-10-28 check attributed the failed spawns to the backend's `--ephemeral` flag; without it, a spawn test returned a code word given only to the subagent." | `reports/results/codex_subagent_spike_2026-10-28/{spawn_ok,spawn_ephemeral_control}.jsonl`, `echo-agent.toml`; `src/auto_fact_checker/backends/codex.py:73-76` |

The PDF was rebuilt from `paper.typ` with typst.

## Unverifiable or hedged claims

These depend on private, git-ignored `logs/` or `runs/`, so I could not check them against committed evidence:
- **Spend ledger** (README, paper and all_experiments): $7.35 over 2,953 entries (2026-10-22), $7.55 over 3,004
  entries (2026-10-28), and an understatement of at most $0.17 from unpriced OpenAI cache writes. The repo already
  labels these as local and unreconciled.
- **README example run** `20261017_210452…`: 3 searches, $0.039, and the scores 99%, 95%, 15%, 5%, 68% and 91%. The
  README already calls it a historical run.
- **Output tokens.** 3,562 vs 420 tokens and the 8.5× ratio: now hedged in the paper body and in Exp02, but not in
  the abstract or all_experiments. Also unverifiable: Exp03 "about 4,000 output tokens", Exp05 "about 11.4k output
  tokens" and the median durations of 55 s (Exp05) and 34 s (Exp04).
- **Exp00 run table** (calls, costs, durations, 46% / 25% / 5% and 18% → 95%) and the re-scoring of 42/42 against the
  key. Its internal arithmetic does check out: total billed $0.52, 49 calls, 42 claims, L5 at 14× L1.
- **Exp07 Claude arm timing** ("2.5–4 min and about 1M input tokens per pass").
- **Pre-registration "before any paid call".** I narrowed this to the benchmark calls the evidence supports (see
  Fixes).

The Exp08 per-pass time, cost and token values (18 s / 1.5k, 110 s / 18k, "one sixth of the runtime") match the
committed `exp08_posthoc.json`. They cannot be regenerated from a clean clone.

## Problems found but not fixed

- Several token and timing figures that rest on unpublished local logs are not annotated where they appear: the
  abstract's "8.5×", `all_experiments.md:20,163`, and the Exp03/04/05 figures listed above. `docs/reproduction.md`
  already says that full prompts and billing records are absent. I annotated only the paper body and Exp02, to keep
  the edits minimal.

## Hugging Face card

The repository has no Hugging Face model, dataset or Space card of its own, so there was nothing to compare. It links
the third-party card `allenai/scifact` only for licensing. I read the hosted card with `hf_fs`
(`hf://datasets/allenai/scifact/README.md`): it lists `cc-by-nc-2.0`, as the README says. The upstream `LICENSE.md`
releases the claims and annotations under CC BY 4.0 and the corpus abstracts under ODC-By 1.0, which also matches.
No upload command is needed.

## Regenerated artifacts and tests

- **Analysis scripts.** I re-ran all four. The derived JSON matched except the private-runs-dependent `per_pass`
  block, which I reverted. Figures were re-rendered with identical data but different bytes (metadata); I did not
  commit them. I checked figure 1's values against `scifact_analysis.json`.
- **Paper PDF.** Rebuilt with `typst.compile` (typst 0.15.0) and committed. The new text appears in the PDF.
- **Screenshots.** Not regenerated; I made no UI change.
- **Tests.** `uv run --locked pytest -q`: 161 passed, 10 deselected (live tests).
