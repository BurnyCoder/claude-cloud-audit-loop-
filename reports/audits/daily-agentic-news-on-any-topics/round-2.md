---
repo: BurnyCoder/daily-agentic-news-on-any-topics
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 105
fixed: 6
unverifiable: 12
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/daily-agentic-news-on-any-topics, round 2
## Summary
This audit checked README.md, AGENTS.md, docs/architecture.md, docs/codex-exec-notes.md, .env.example, pyproject.toml and the docstrings and comments in src/ and tests/. The repository has no paper, Hugging Face card, GitHub Pages site or figure-generating scripts. Its two images are screenshots of the UI.

What was checked:
- **Code against docs.** Defaults, dimensions, the 24 topics, 5,760 cells, retry policy, slug cap, status throttling, the confirmation threshold and the prompt rules all match the code. Test counts (52 default, 3 `cli`, 2 `live`) match `pytest --collect-only`. Every version in the Technologies table matches uv.lock.
- **Numbers.** Every number in prose that can be derived from the run tables in docs/codex-exec-notes.md was recomputed and is consistent, for example the mean one-cell input tokens of 74,836, the 1.4–3.5x ratio, 9–24 items, the 13 vs 15 replicate and the "2 vs 4–13" spread.
- **Links.** Every cited URL was fetched. The Codex source citations were read at tag `rust-v0.163.0`, including the exact line ranges (turn.rs L1690-1692, common.rs L392-410, output_schema.rs L51-59) and the bundled `models.json` entry for gpt-6-luna. The DOI and Crossref claims about the fabricated citation were re-run and hold.

The six fixes are wording fixes:
- The claim that StatusBoard is the only writer of status.json was overstated in 3 places. launcher.py and cli.py also write status.json.
- One GitHub commenter was described as a "core developer" when the issue page labels him a contributor.
- One open user bug report was stated as established fact in 2 places.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| docs/architecture.md:69 | "`StatusBoard` is the only writer of `status.json`." | only writer *while the run is going*; the launcher writes `starting`, the CLI `failed` on a crash, the Stop button `stopped` | src/agentic_news/launcher.py:31-38,55; src/agentic_news/cli.py:38-40 |
| src/agentic_news/dashboard/status.py:6 | "status.json is written only by the run's StatusBoard" | written by StatusBoard while the run is going; launcher.py writes `starting`/`stopped`, cli.py `failed` | same as above |
| src/agentic_news/store.py:6 | "StatusBoard is the single writer of status.json for a run." | single writer while a run is going (launcher and cli.py write only starting/stopped/failed) | same as above |
| src/agentic_news/store.py:5 | "a core developer explains" | "a CPython contributor explains" | https://github.com/python/cpython/issues/90161 (eryksun is labelled "Contributor"; quote: "existing opens of the destination path are not allowed, even if they share delete access") |
| docs/codex-exec-notes.md:30 | "Codex applies it to **every** agent message ... (#19816)" | "an open bug report says Codex applies it to every agent message ..." | https://github.com/openai/codex/issues/19816 (open user report, not confirmed by maintainers) |
| src/agentic_news/prompts.py:8 | "Codex applies the output schema to every agent message (#19816)" | "An open bug report says Codex applies ..." | same as above |

## Unverifiable or hedged claims
These depend on local, git-ignored data or on commands that need the Codex binary, so they could not be compared with evidence. The docs already say that run data comes from git-ignored `runs/` and `logs/` folders. None of these was changed:
1. The Pure math run table: calls/queries, items, links from search and dated-in-interval for runs 1–5b.
2. The Mechanistic interpretability and AI governance run figures.
3. "Durations: 41–79 s"; "Input tokens: 76k–749k (run 3: 749k, 657k cached)".
4. Reasoning items "0–6 per agent at medium and 12 in the one high run"; "run 3's 12 calls include 2 of type other".
5. The live test A/B results (13 s, 17 s, tokens 73,095 / 77,430 / 108,447), which come from a terminal log that was not kept.
6. The Region run and run `20261022-030136` details (tokens, outlets, 44 s, 4/6 and 5/6).
7. Doubtful links in old runs: the X posts, the YouTube search page and the `REPLACE` placeholder.
8. "Tested on Windows 11".
9. `--disable <name>` equals `-c features.<name>=false` per `codex exec --help`. This needs the binary. The feature names themselves were confirmed in codex-rs/features/src/lib.rs at rust-v0.163.0.
10. The `--strict-config` error text for an unknown `-c` key.
11. `project_doc_max_bytes=0` keeps AGENTS.md out of the prompt, as checked with `codex debug prompt-input`.
12. The note that the first 6 lines of tests/fixtures/events_sample.jsonl are an "unedited" stream. The shapes match exec_events.rs, including the duplicate `id` key that comes from serde flattening, but whether the lines are unedited cannot be proven.

## Problems found but not fixed
None that are factual claims. A side observation, outside this audit's scope: `dashboard/results.py` imports numpy directly, but numpy is not declared in pyproject.toml. It is installed only as a dependency of pandas.

## Hugging Face card
n/a. The repository links no Hugging Face model, dataset or Space. "Hugging Face Papers" appears only as text in a source definition.

## Regenerated artifacts and tests
- No generator scripts exist. The PNG/JPG screenshots were not regenerated.
- `uv run pytest`: 52 passed, 5 deselected (`cli`/`live`), both before and after the edits. Only docstrings changed in code.
