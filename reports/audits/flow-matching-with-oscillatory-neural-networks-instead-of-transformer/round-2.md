---
repo: BurnyCoder/flow-matching-with-oscillatory-neural-networks-instead-of-transformer
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 370
fixed: 1
unverifiable: 6
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/flow-matching-with-oscillatory-neural-networks-instead-of-transformer, round 2

## Summary

I audited the repository independently and did not use earlier audit files as evidence. Almost every claim I checked matches the evidence. The README, paper, experiment ledger, protocol, planning-power report, development records and Hugging Face cards agree with the result records embedded in `reports/experiments/*.md`, with the code that produced them, and with the artifacts published on the Hub.

How the numbers were checked:
- **Script comparison.** A script pulled the JSON records out of all 83 experiment reports. It recomputed every row of the training, quality, control and diagnostic tables in `reports/paper.md` and `reports/experiments.md`, using the generator's `.6g` format. There were 0 mismatches across 161 rows.
- **Primary result.** I recomputed it from the six seed pairs: mean KID 0.185673 / 0.0917895 / 0.134872, paired difference +0.0938838, t interval [0.085429, 0.102339], sign-flip p = 0.03125. Ratios 0.504041 and 2.14506, the peak-MiB column, the ablation and shuffle deltas, and the counts (30 runs, 43 evaluations, 2 failures, 1 diagnostic) also match.
- **Reruns of the repository's own code.** `ofm.statistics.paired_comparison` reproduces `reports/analysis.json` exactly. `ofm.statistics.planning_power()` reproduces `reports/planning-power.json` exactly. Building the models on CPU reproduces every parameter count: 1,297,712 / 1,298,864 / 1,296,688 / 707,888 / 1,295,664 for CIFAR, the MNIST counts, and DiT FFN width 576.
- **Method claims.** Optimizer, EMA, split, hashing, the oscillator update equation, eps, readout, DiT block, KID settings, clamping, SWD projections, validation prefix, run-order randomization and so on were checked against `src/ofm`.
- **Hub artifacts.** `budget.json` (67,451.708 s = 18.7365855 h, no active reservation), `freeze.json` (timestamp and revision), the data manifest (45,000 / 5,000 / 10,000), `environment.json` (RTX 5070 Laptop GPU, torch 2.11.0+cu128) and the MNIST smoke `run.log` (17.68 s and 203,779,584 bytes at 50 updates; 33.96 s and validation MSE 2.00869 at 100) all confirm the development and verification statements.
- **Commits and CI.** Commit hashes and messages cited in `reports/development/verification.md` exist and match. The CI runs show what the record says: 38977501341 failed only at the ruff step; 39057104367 passed with 35 tests; 39058625394 passed with 36 tests; each has one POT `SyntaxWarning`.
- **Citations.** Titles and authors were confirmed via arXiv or Hugging Face paper metadata. AKOrN equations 4–7 do contain the tangent-projected Kuramoto update, the normalization, the mixing-then-norm readout and the convolutional coupling. I-CFM is defined in Tong et al., §3.2.2. KODM changes the diffusion process itself, as the paper says.
- **Links.** Documentation links resolve (HTTP 200). Third-party GitHub links were blocked by the session proxy; the installed packages' metadata confirms those URLs.

There was one fix: a clarification in `docs/implementation.md` about how checkpoints are retained.

Breakdown of the 370 claims checked:

| Area | Claims |
| --- | --- |
| Paper tables | 88 |
| Experiment-ledger tables and completeness | 77 |
| README | 40 |
| Paper prose | 35 |
| Scholarly citations | 14 |
| Other links | 45 |
| Protocol | 15 |
| Planning-power report | 8 |
| Verification and review records | 33 |
| HF cards and paths | 5 |
| Code comments and defaults | 10 |

## Fixes

| file:line | before | after | evidence: result file path or URL |
| --- | --- | --- | --- |
| docs/implementation.md:17 | "Atomic rename protects the previous complete checkpoint against interrupted writes." (did not say whether intermediate checkpoints are kept) | Adds: every snapshot, including the periodic ones every `checkpoint_seconds` (default 300), replaces the single `checkpoint.pt`, so intermediate checkpoints are not kept after the run; only the final checkpoint is kept and published. | `src/ofm/training.py` lines 113, 134 and 147 (all `save_checkpoint` calls write `checkpoint_path`); `src/ofm/config.py` (`checkpoint_seconds: float = 300.0`); Hub listing `hf://models/BurnyCoder/oscillatory-flow-matching-cifar10/study/main/cifar10-onn-s101` (one `checkpoint.pt`) |

## Unverifiable or hedged claims

1. README:11 and paper "local target is an RTX 5070 Laptop GPU with 8 GB VRAM": `environment.json` records only the device name. NVIDIA's comparison page (https://www.nvidia.com/en-us/geforce/laptops/compare/) lists both 12 GB and 8 GB GDDR7 as standard configurations for this GPU. So the claim is consistent with NVIDIA's spec, but the specific unit's VRAM is not recorded.
2. reports/development/verification.md:56, "The initial complete local suite contained 27 passing tests": a local run with no saved log.
3. reports/development/verification.md:68, "33 passing tests and a passing Ruff check before the CIFAR schedule": a local run with no saved log. The later CI counts (35 and 36) and today's local run (37 passed) were verified.
4. reports/development/verification.md:74, "The targeted reporting/publication rerun passed all six tests locally": no saved log.
5. AGENTS.md:27 and README:113, "no repository license was present during inspection" of AKOrN: a historical observation that cannot be re-checked now.
6. Visual-inspection statements in verification.md:62, 84 and 88 ("recognizable but rough digits", "conspicuous patch discontinuities"): subjective. The grids exist in `reports/figures/`.

## Problems found but not fixed

1. docs/protocol.md:19 says "Save final budget checkpoints and intermediate checkpoints". The implementation keeps only one checkpoint per run: periodic snapshots overwrite `checkpoint.pt`. I left this sentence unchanged because the protocol is the dated pre-registration (2026-10-16, commit 55dc2e4), and the wording may simply mean "write periodic checkpoints". The behavior is now stated in `docs/implementation.md`. The owner may want to add a dated deviation note to the protocol rather than rewrite it. No reported result is affected, because only final checkpoints enter the primary comparison.

## Hugging Face card

The repository has no standalone card file. Cards are generated by `src/ofm/publishing.py` (`export_run` for each run, `publish_study` for each dataset root). I read the hosted cards with `hf_fs`:
- `hf://models/BurnyCoder/oscillatory-flow-matching-cifar10/README.md`
- `hf://models/BurnyCoder/oscillatory-flow-matching-mnist/README.md`
- `hf://models/BurnyCoder/oscillatory-flow-matching-cifar10/study/main/cifar10-onn-s101/README.md`

All three match the in-repository templates word for word, filled with the correct run identity and checkpoint SHA-256 (`e3eb0aab…` matches the training record). The run lists cover all 26 CIFAR and 5 MNIST checkpoints. The README's download paths exist on the Hub. The collection slug `oscillatory-flow-matching-local-exploratory-study-6ad2aa5b3f5a7563a8018be2` resolves. There is no drift, so no upload is needed.

## Regenerated artifacts and tests

- Nothing was regenerated. The only edit is to `docs/implementation.md`, which no generated report, figure or PDF depends on. The `paper.md` and `experiments.md` tables already match the generator in `src/ofm/report_text.py` and the records. Full report regeneration (`ofm report`) would need the untracked `runs/` tree and was not attempted.
- Tests: after `uv sync --frozen --extra cpu`, `uv run --no-sync pytest -q` gave 37 passed with 1 third-party POT warning, run before the edit. No code was changed, so the tests and ruff were not rerun after it.
- CPU-only reproductions: `planning_power()` and `paired_comparison()` outputs match the committed JSON exactly, and the parameter counts match.
