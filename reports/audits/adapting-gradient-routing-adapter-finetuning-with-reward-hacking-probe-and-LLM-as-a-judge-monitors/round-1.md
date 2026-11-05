---
repo: BurnyCoder/adapting-gradient-routing-adapter-finetuning-with-reward-hacking-probe-and-LLM-as-a-judge-monitors
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 270
fixed: 2
unverifiable: 8
not_fixed: 1
hf_card_drift: yes
---
# Fact-check audit: BurnyCoder/adapting-gradient-routing-adapter-finetuning-with-reward-hacking-probe-and-LLM-as-a-judge-monitors, round 1

## Summary

I checked the README, the pilot paper (`reports/qwen_probe/paper.md`), the consolidated and per-arm reports, the monitor comparison, the engineering report, the follow-up summary and paper, the 22 October correction paper and `checks.json`, and the docs (`protocol`, `analysis`, `implementation`, `plan`, `followup-protocol`, `probe-provenance`). I also compared the Hugging Face card template in `experiments/qwen_probe/publish.py` with the hosted cards. I did not check the vendored upstream GRAFT material (`README.upstream.md`, `rl/`, `sft/` docs) beyond spot checks: the SFT README's "56 jobs" and "99 eval tasks", and the §4/§5 mapping against the GRAFT paper.

I recomputed every behavioral number from `audited_outcomes.json` and `followup/combined_outcomes.json` with a separate script. The script used Wilson intervals, a paired task bootstrap (10,000 draws, seed 42), worst-case ambiguity bounds and an exact discordance test. All 20 per-condition rows matched. So did the primary and secondary paired contrasts, the probe retain-minus-both ablation and all six follow-up contrasts, to the third decimal. Other checks:
- The detector precision, recall and FPR are consistent with the counts (4/8, 4/95 and 4/99 for the probe; 7/19, 7/95 and 12/99 for the judge). So are the calibration FPRs (10/203 and 9/203) and the judge-minus-probe differences.
- The power tables (74/199/294/388; 71/150/307/464) and the full seed-sensitivity grid match the formulas in `docs/analysis.md`.
- The correction totals (932 targets, 2,626 commands, 192/192 affected, 14 warnings, the loss values, 256/256 and 232/232 parser rejections, 344 preserved files) match `checks.json` and `preserved-files.json`.
- Budget, audit-freeze, recovery and follow-up timestamps match their JSON files.
- The method details match `results.json` training arguments, `data_lock.json`, `train_gr.py` and `adapter.py`. These include width 64, batch 48, LR 5e-4, five epochs, weight decay 1e-4, betas (0.9, 0.95), 5% warmup with cosine decay, kappa 2, 1% anchors and the rsLoRA-matched scale 32/sqrt(32).
- The checkpoint size is consistent with the model config: 168 tensors and 11,010,048 = 3 × 1024 × 64 × 28 × 2 parameters.

Citations I fetched:
- **GRAFT, arXiv 2610.17062.** Title and seven authors match, with equal contribution marked for Ward and Hu. Section G.4 confirms the source recipe.
- **Zheng et al. 2023, Lipton & Steinhardt 2018, Lones 2021 (v5 2024), Henderson et al. 2017:** metadata matches.
- **Library and model docs:** SciPy `binomtest` (Wilson), statsmodels `power_proportions_2indep` (pooled null and unpooled alternative), the Accelerate loss scaling in `backward`, Liger's Qwen3 fused cross-entropy, and the Qwen3-0.6B non-thinking sampling defaults and model config (28 layers, tied embeddings).
- **Pinned commits and files:** the Qwen model revisions, the Harbor ATIF emitter at L1482, the parser's `keystrokes` check, `docker compose down --rmi all` and `job.py` creating the job directory, containerd v2.4.2 `compat.go`, and the probe repository at `cd4c566` (MIT license, `data/.gitkeep`, the four notebook sources, LoRA r16/α32 on q/k/v/o, 8 heads, d_model 256, four fine-tuned layers).
- **Hugging Face collection:** public, with exactly the six listed models.

I found one wrong statement: a misdated TRL release in `docs/implementation.md`. I found one omission in the generated model cards: they lack the correction notice. I fixed both. No other numbers or citations needed changes.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| docs/implementation.md:73 | "TRL 1.16 removed `completion_only_loss` from the collator and moved masking to preprocessing" | "the pinned TRL 1.16 collator no longer accepts `completion_only_loss`; TRL had removed it from the collator and moved masking to dataset preparation in release 1.7.0" | https://github.com/huggingface/trl/pull/6037 (merged 2026-06-23); https://github.com/huggingface/trl/releases/tag/v1.7.0 (lists #6037); PyPI release dates (1.7.0 on 2026-06-25, 1.16.0 on 2026-10-15) |
| experiments/qwen_probe/publish.py:85-90 (card template) | Card had no mention of the 22 October conversion defect; it says only that the conclusion is unchanged | Adds a paragraph when the correction exists: all 192 training trajectories had the invalid empty command and lost the completion flag; judge-arm losses rose sharply; every saved judge-arm and original-monitor response failed the parser; interpretation is compromised; no retraining; links `report/correction-2026-10-22/paper.md` | reports/qwen_probe/correction-2026-10-22/checks.json (targets.totals; degraded_arms) |

## Unverifiable or hedged claims

- README:26 and paper appendix: "RTX 5070 Laptop GPU (8,151 MiB reported VRAM), driver 591.74". This exists only as hardcoded text in `report.py`, and no committed log or manifest records it. "Approximately 8 GB VRAM" is likewise unsourced; `preflight.json` records a 3.53 GB PyTorch peak.
- README:26: "7 GB task checkout" and "40 GB free". The size of the Terminal Wrench submodule could not be fetched (GitHub API blocked; download too large). The 40 GB figure is already labeled as an allowance.
- `engineering.md`: "475 completed detector scores were preserved" at the 23:15 restart. No committed artifact records it.
- Correction paper: "All 64 selected non-model regression tests passed". The repository has 57 test functions, plus parametrized cases. The full environment (torch/CUDA, submodules) could not be installed within limits, so I did not rerun the count. The intermediate test-suite counts in `engineering.md` and `plan.md` (18/26/28/29/34/39/40/62) are also historical and not reproducible here.
- The AUROC point estimates (0.497 and 0.569) and their bootstrap intervals cannot be recomputed: per-record heldout scores are in the ignored `artifacts/`. The thresholded metrics and paired differences are internally consistent.
- `docs/probe-provenance.md`: the BJS reward-hacking corpus "returned 404". It is still unreachable now (git asks for credentials), and the document already hedges this.

## Problems found but not fixed

- Hosted Hugging Face cards (six repositories) do not include the 22 October correction. Neither do their staged `report/` folders, which have no `correction-2026-10-22/`. I cannot write to the Hub. The repository template is fixed; republishing is needed (see below).
- Minor, not edited: `docs/analysis.md` capitalizes Henderson et al.'s title as "That Matters"; the arXiv title is "Deep Reinforcement Learning that Matters".

## Hugging Face card

I read the hosted card for `BurnyCoder/graft-qwen3-06b-probe-graft-pilot` in full and the `qwen-judge-graft` card in part with `hf_fs`. Both are exactly the `publish.py` template rendered with the then-current `results.json` and the follow-up block. The coverage figures (120/160, 40/40, 160/160), the conclusion, the merge command and the license metadata (Apache-2.0, matching the Qwen3-0.6B card) are consistent with repository evidence. Drift: the repository README and correction paper report the converter defect, but the hosted cards and hosted `report/` folders predate it. The updated template now adds that notice.

To update, rerun `uv run python -m experiments.qwen_probe publish` from the original workspace; it needs the local `artifacts/qwen_probe/checkpoints/*/progress.json`. Alternatively, render each card and upload it manually:
`huggingface-cli upload BurnyCoder/graft-qwen3-06b-<arm>-pilot path/to/card.md README.md`
for `<arm>` in no-intervention, probe-graft, qwen-judge-graft, original-graft, probe-filtering and random-graft. Also upload `reports/qwen_probe/correction-2026-10-22/` to `report/correction-2026-10-22/` so the new card link resolves.

## Regenerated artifacts and tests

- I edited no generated report, figure or PDF, so nothing needed regeneration. `paper.md`, `paper.pdf`, `summary.md` and the figures are unchanged. Figure labels in `detector.png` and `behavior.png` match `results.json`.
- `tests/test_publication.py`: 4 passed, run in a minimal environment with pytest and python-dotenv (`uv run --no-project`). The full suite was not run: the root environment needs the uninitialized Harbor submodule and multi-GB torch/CUDA wheels.
- `ruff check --select F,E9 experiments/qwen_probe/publish.py`: passed.
