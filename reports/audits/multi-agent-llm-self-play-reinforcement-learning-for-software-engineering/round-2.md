---
repo: BurnyCoder/multi-agent-llm-self-play-reinforcement-learning-for-software-engineering
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 75
fixed: 3
unverifiable: 3
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/multi-agent-llm-self-play-reinforcement-learning-for-software-engineering, round 2
## Summary

The repository is still at the pre-execution stage. It has no result files (no `runs/`, `reports/` outputs, `site/dist`, or paper PDF), and the README results block correctly says nothing has been measured. So the audit covered method, citation, configuration, manifest and licence claims in README.md, AGENTS.md, docs/, reports/preregistration.md, the generated-paper and model-card text templates in `src/`, the site template, and code comments.

Most claims hold up against primary sources and the committed code and configs:
- SSR Eq. 1/2 rewards (alpha = 0.8)
- CWM Appendix C objective and the [0.8, 1.25] clip
- the Anchored Self-Play finding
- the pinned OpenCode subagent features
- Qwen3.5-2B (Apache-2.0, has a vision encoder)
- the Unsloth BF16/text-only guidance
- swebench 5.0.2 APIs and report caching
- the four upstream repository licences

I recomputed the SWE-bench cohort from the pinned dataset revision (78f471bf…). The 32 lowest-SHA-256 instance IDs among requests/Flask/pylint/pytest match `manifests/evaluation.json` exactly, in order and with the same base commits. The split is 15 pytest, 8 pylint, 8 requests and 1 Flask, out of 38 eligible tasks. The synthetic manifest has 16 tasks, one per function cluster, all at one humanize commit.

There were three precision errors, all in `docs/sources.md`. I fixed them.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| docs/sources.md:7 | SSR provides "curriculum rewards" | "solve-rate-based injection and binary repair rewards (§2.3–2.4, Eqs. 1–2)"; SSR's curriculum emerges from self-play and is not a separate reward | https://arxiv.org/html/2512.18552v3#S2.SS3 (Eq. 1, alpha=0.8; Eq. 2 ±1) |
| docs/sources.md:8 | All objective details attributed to CWM Appendix C | Adds that the clip thresholds ε_low=0.2 and ε_high=0.25 ([0.8, 1.25]), no KL and no σ normalization are stated in CWM Section 5.2, not Appendix C | https://arxiv.org/html/2510.02387v1#S5.SS2 and #A3 |
| docs/sources.md:11 | Only "Library is Apache-2.0" (unsloth) | Adds that the locked `unsloth-zoo` dependency is LGPL-3.0-or-later and the Unsloth notebooks are LGPL-3.0 | https://pypi.org/project/unsloth-zoo/2026.10.10/ (license metadata); raw.githubusercontent.com/unslothai/notebooks/main/LICENSE |

## Unverifiable or hedged claims
- README:31: "The tested machine has an RTX 5070 Laptop GPU." This is a local hardware statement and no record in the repository shows it.
- `src/multi_agent_ssr/reporting.py` AI_STATEMENT, "Codex wrote this codebase and paper…": an authorship statement with no source available.
- `manifests/environment.json` local Docker image IDs and the `pip freeze` package list. These could not be reproduced without building the image (no Docker or long builds were used). The cited Docker, uv and setuptools-scm documentation anchors resolve.

## Problems found but not fixed
None. Minor observations that are not errors:
- Flask contributes only 1 of the 32 primary-cohort tasks. The preregistration's repository list is accurate but does not show the imbalance.
- The site template line "Every sampled action counts once per optimization pass" leaves out the zero-advantage exception that the README states.

## Hugging Face card
The repository links no Hugging Face model, dataset or Space for this project. A search of `hf://models/BurnyCoder` found none, so there is no hosted card to compare. The card template in `src/multi_agent_ssr/publication.py` matches the evidence: the base model is Apache-2.0, the training repositories are MIT/BSD-3-Clause, and the harness is MIT (LICENSE). No upload command is needed.

## Regenerated artifacts and tests
Nothing to regenerate: there are no run records, and the report command needs `runs/`. No code was changed, so I did not run tests. The only change is to documentation (`docs/sources.md`).
