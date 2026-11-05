---
repo: BurnyCoder/multi-agent-llm-self-play-reinforcement-learning-for-software-engineering
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 50
fixed: 5
unverifiable: 4
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/multi-agent-llm-self-play-reinforcement-learning-for-software-engineering, round 1

## Summary

The repository is still before execution. It has no run records, results, rendered paper or published Hugging Face model. Its claims are method claims, citations, manifests and generated-text templates. I checked them against the code and configs, the committed manifests, the pinned SWE-bench Verified parquet (revision 78f471bf) and the primary sources fetched today: SSR arXiv 2512.18552v3, CWM arXiv 2510.02387v1 Appendix C, Anchored Self-Play arXiv 2607.03523v1, the pinned OpenCode source and license, the Unsloth Qwen3.5 guide, the Qwen3.5-2B card and the upstream LICENSE files.

Most claims hold:
- The SSR reward (-1 / -0.8 / 1-1.8s, alpha 0.8), the binary solver reward and the five-file artifact match the source.
- The CWM length-weighted centered advantage, the [0.8, 1.25] clip (eps_low 0.2, eps_high 0.25), the absence of a KL term and the fixed token-capacity normalization all match.
- All license statements match the upstream files.
- The 32-task human cohort is reproduced exactly: I recomputed the SHA-256 ordering over the 38 eligible requests/Flask/pylint/pytest rows of the pinned dataset, and the IDs and base commits match.
- The 16 synthetic tasks have 16 distinct functions.
- The budget formulas, AdamW settings, validation thresholds, bootstrap settings and LoRA scope match the code.

Five claims were wrong or overstated, and I fixed them.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| README.md:3 | "every primary/child generation contributes to its team's policy-gradient update" | "every primary/child generation in a completed group enters its team's policy-gradient update once per optimization pass (zero-advantage groups make no update)" | src/multi_agent_ssr/learning.py:136-146 (zero-advantage episodes are filtered out; 2 passes); configs/pilot.toml `optimization_passes = 2` |
| site/template/index.html:45 | "Every sampled action is trained once in its actual context." | "Every sampled action counts once per optimization pass, in its actual context." | src/multi_agent_ssr/learning.py:146-165; reporting.py paper text ("once per optimization pass") |
| src/multi_agent_ssr/reporting.py:414 (generated paper, "Differences from prior SSR") | "history-guided curriculum" | "git-history-aware bug-injection prompts" | https://arxiv.org/html/2512.18552v3 Sections 2.3 and 3.4 describe a history-aware injection strategy and an emergent curriculum, not a "history-guided curriculum" |
| reports/preregistration.md:19 (erratum appended at :53) | "history-guided curriculum" | dated wording-only erratum, original text preserved per the preregistration's amendment rule | same SSR v3 source; agents get no Git history (sandbox.py:5, 20) |
| src/multi_agent_ssr/publication.py:52 (generated HF card) | harness link `github.com/BurnyCoder/local-multi-agent-swe-rl` (old name, works only through a rename redirect) | `github.com/BurnyCoder/multi-agent-llm-self-play-reinforcement-learning-for-software-engineering` | `git remote -v`; `gh api repos/BurnyCoder/multi-agent-llm-self-play-reinforcement-learning-for-software-engineering` |

## Unverifiable or hedged claims

- README.md:31 "The tested machine has an RTX 5070 Laptop GPU". No preflight or run record exists in the repository. Left as is.
- reporting.py AI_STATEMENT ("Codex wrote this codebase and paper..."). This is an author statement and cannot be checked.
- README.md:31 says installing each package's latest version "would violate Unsloth's compatibility requirements". No primary source was fetched that confirms this.
- manifests/environment.json and image_pins.json Docker digests and image IDs. Checking them needs Docker image pulls, which are out of scope. Internal consistency was checked: the 32 pins match the 32 cohort IDs and all are "ready".

## Problems found but not fixed

None. AGENTS.md "every child generation is scored once in its own context" is consistent with the code if "once" means "not double-counted through parent copies". I left it unchanged.

## Hugging Face card

n/a. No Hugging Face model, dataset or Space for this project exists under BurnyCoder (checked with `hf_fs ls`), and the repository does not commit a card. The card is generated at export time by src/multi_agent_ssr/publication.py. Its stale harness URL is fixed, and its other statements were checked: Apache-2.0 base, MIT/BSD training repositories, frozen vision tower, embeddings and head. No upload command is needed.

## Regenerated artifacts and tests

- Nothing was regenerated. `selfplay report` needs run records, and the repository has none (`runs/` is ignored and absent).
- `uv sync --locked`, then `uv run --no-sync pytest -q -m "not docker and not gpu"`: 115 passed, 14 skipped.
- `ruff check src tests`: all checks passed.
