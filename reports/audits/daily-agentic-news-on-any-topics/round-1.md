---
repo: BurnyCoder/daily-agentic-news-on-any-topics
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 140
fixed: 5
unverifiable: 10
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/daily-agentic-news-on-any-topics, round 1
## Summary
I checked README.md, AGENTS.md, docs/architecture.md, docs/codex-exec-notes.md, .env.example, pyproject.toml and the docstrings and comments that state facts. Ground truth:
- the code and uv.lock;
- the test suite: 52 default, 3 `cli` and 2 `live` tests collected, and the 52 default tests pass;
- the Codex source at tag `rust-v0.163.0`, from a sparse clone: `exec_events.rs`, `event_processor_with_jsonl_output.rs`, `turn.rs`, `common.rs`, `output_schema.rs`, `cli/src/main.rs`, `features/src/lib.rs` and `models-manager/models.json`;
- the learn.chatgpt.com Codex docs (non-interactive mode, config basics, config reference, AGENTS.md);
- Crossref, and the GitHub issues openai/codex#19816 and cpython#90161.

Almost everything holds:
- The default dimensions and the 5,760-cell count are correct.
- The `.env` defaults, dependency versions (uv.lock), test counts and the Codex flags, feature names and event and usage fields match.
- The gpt-6-luna catalog facts match: display name, description, 272k context, `default_reasoning_summary: none` and efforts low to max.
- The `strict` output-schema chain matches.
- The fabricated-citation evidence matches: the DOI returns 404, and Nature Machine Intelligence's first article is dated 2019-01-07.
- Derived numbers are correct: the 1.4–3.5× ratio, the mean of 74,836 and the 73–77k and 108–263k ranges.

I found one code bug and three wrong or overstated statements.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| src/agentic_news/schema.py:146 (`_in_interval`) | A `YYYY-MM` or `YYYY` date was treated as ending on day 28, so `2026-10` did not "overlap" a range of Oct 30–31. That contradicts docs/architecture.md ("overlaps the interval's range"). | The real month end, from `calendar.monthrange`. | Reproduced: `_in_interval('2026-10', 2026-10-30, 2026-10-31)` returned False before the fix and True after. Tests pass (52). |
| README.md:76 | "Date in range: the publication date lies inside the interval" | adds "(a partial date such as `2026-10` counts if it overlaps)" | `schema._in_interval` |
| README.md:226 | "Python 3.14 (managed by uv 0.13)" | "managed by uv; build backend `uv_build` 0.13" | pyproject.toml `uv_build>=0.13.0,<0.14.0`. No file records the uv version. |
| docs/codex-exec-notes.md:66-68 | the 5/5b replicate "is as large as most differences between rows" | "smaller than the differences between consecutive Pure math rows (2 vs 4–13 items), but one pair cannot estimate the noise" | Recomputed from the notes' own table: consecutive item differences are 7, 12, 13 and 4, against a replicate difference of 2. |
| src/agentic_news/store.py:4-5 | "cpython#90161 reports it for any open handle" | "a core developer explains that MoveFileExW refuses a destination that is already open, even with delete sharing" | https://github.com/python/cpython/issues/90161 (closed, not a bug; eryksun's comment) |

## Unverifiable or hedged claims
These claims stay as written. They are internally consistent but cannot be checked from the repository:
- **Per-run measurements in docs/codex-exec-notes.md.** They come from the git-ignored `runs/` and `logs/` folders and the terminal logs of the live tests, so their raw values are unverifiable:
  - search calls and queries;
  - durations of 41–79 s;
  - input tokens of 76k–749k, and 657k cached in run 3;
  - 0–6 and 12 reasoning items;
  - the run 3 "other" calls;
  - the Region-run outlets.
- **The `codex debug prompt-input` AGENTS.md injection experiment** is a local experiment.
- **`--strict-config` checking `-c` overrides** (the error text): the help string at the tag only mentions config.toml fields, and I did not find the error string.
- **The `web_search` action shape `{type:"search", queries}`**: it is not in the fixture, and its definition lives in `codex_protocol`, which I did not check.
- **"Tested on Windows 11"**, and that the first 6 fixture lines are an "unedited" real stream. The fixture's shapes do match Codex's `exec_events.rs`.

## Problems found but not fixed
- The `in_interval` flags (and re-filing) in past runs may differ for items with `YYYY-MM` or `YYYY` dates whose range starts after day 28 of that month. Counts such as "5/6 dated inside their interval" were computed with the old code and are pending a re-run. I did not re-run anything.
- I added no regression test for the date fix.

## Hugging Face card
n/a: the repository links no Hugging Face model, dataset or Space.

## Regenerated artifacts and tests
- There are no generated artifacts: no figures, tables or paper.
- `uv run pytest`: 52 passed, 5 deselected, after the code change.
- I could not run the `cli` and `live` markers: Codex CLI is not installed, and `live` would spend tokens.
