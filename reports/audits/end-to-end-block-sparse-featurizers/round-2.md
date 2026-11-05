---
repo: BurnyCoder/end-to-end-block-sparse-featurizers
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 215
fixed: 0
unverifiable: 6
not_fixed: 0
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/end-to-end-block-sparse-featurizers, round 2

## Summary

I checked the README, the study and sweep papers (the generator `src/e2e_bsf/paper.py` and PDF text), `reports/study/findings.md`, `pilot.md`, `summary.md`, `reports/experiments.md`, the smoke summary, the sweep summary and audit, all docs (preregistration, downstream preregistration, execution notes, methodology, plan completion, literature review), `vendor/NOTICE.md`, the GitHub Pages explorers, and the hosted Hugging Face cards. I did not use earlier audit files as evidence. I recomputed every number with scripts that read `reports/*/results.json`, `pilot.json`, `final_audit.json`, `study_status.json`, `verification.json`, `batch_numerics_diagnosis.json` and the committed sweep logs. All of them matched: values, rounding, n, seeds, Student and paired intervals, the effect size and percentage changes, timings, VRAM, parameter counts and UTC times. I fetched each cited paper from arXiv, ACL Anthology and PMLR, plus the Apollo `losses.py` at the pinned commit, Goodfire's files at revision 219f121 and the DINOv3 README. All titles, authors, years and supporting statements checked out. **I found no factual errors, so I made no edits, made no commits and did not push.**

Key verifications:
- README and paper study table, controls, narrative, 6.78% KL reduction, 44.41% NMSE increase, 77.5% power, 9.326 h and 699.3 MiB: these match `reports/study/results.json`.
- Paired CI [-0.00325909, 0.008351] and scalar CI [0.206989, 0.239339]: I recomputed them from the per-seed differences with t(0.975, 4).
- Pilot table, effect size 1.62632, 22.24 h for 6 seeds versus 18.53 h for 5, 2.53 pp shortfall and deadlines: recomputed from `reports/study/pilot.json` and the schedule.
- Sweep: 15/50 complete, 1 trained-only, 34 not started, 0/25 main runs; accuracy range 11.6% to 30.0%; KL beat MSE in 4/4 matched comparisons. Extraction took 26.5 min, statistics 23.4 min and hashing 17.7 min (from the log timestamps). Batch-numerics values and verification values (1.78814e-7, 4.66014, 2.29414 to 3.96106e-5) match.
- Braun et al. Table 1 values (69.4/0.145 versus 27.5/0.144, layer 6, about 60% fewer active features), Section 2.4 downstream loss and Section 3.2 MSE claim: confirmed in arXiv 2405.12241v2. Apollo's KL docstring says KL(new||orig) but the code computes KL(orig||new), and its downstream coefficient is `total_coeff / len(hook_positions)`. Both confirmed at commit 83b4add.
- Fel et al. (arXiv 2606.25234): Appendix D uses a shared positive gamma and QR every 20 steps; Appendix G.3 defines total variation and Dirichlet map smoothness; G.4 uses max-abs pooling; training is on final-layer DINOv3 ViT-B patches. All confirmed.
- Jerpelea and Ananthram (2608.27515): splitting, composition, seed flicker (Section 3.2) and Tournament Top-K confirmed. Chanin (2605.18229), Karvonen (2503.17272), SAEBench (PMLR v267), Card et al. (EMNLP 2020), Lones (2108.02497) and Lipton and Steinhardt (1807.03341): metadata matches.
- `vendor/goodfire/base.py` and `grassmannian.py` are byte-identical to upstream `bsf/` at 219f121. The DINOv3 README lists a pretrained classification head only for ViT-7B/16.
- `site/data.json` and `site/sweep/data.json` are identical to the report `results.json` files. Site figures and PDFs are byte-identical to the report copies. The study PDF contains every prose string in the current `paper.py`, so it is in sync.
- PR #1 was merged at 2026-10-27T00:31:21Z, which is 01:31:21 Europe/Berlin. Commit aea5c33 is the PR #8 merge. There are 37 collected tests now (34 functions plus 3 extra parametrizations), matching "All 37 tests passed".

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| (none) | No factual errors found | No changes | See Summary |

## Unverifiable or hedged claims

- `docs/plan-completion.md`: "Preparation and all pilots finished after 90.28 minutes". The repository only records the allocator failure at 90.30 min (`reports/study/allocation_failure.json`). The pilot-end time is not committed.
- `reports/study/findings.md`: "the first complete report finished at 13:01:16 UTC". No committed log records this.
- Historical test counts ("23-test suite", "All 25 focused tests pass") describe earlier states of the repository and cannot be re-observed. The current count of 37 matches the latest statement.
- README "approximately 15 GB workspace storage": not measurable from committed artifacts. The 8 GB cache claim is consistent with 13,344 x 196 x 768 x 4 bytes = 8.03 GB.
- Statements about browser and visual inspection, and the local `.venv` Python 3.12.13: process claims with no committed evidence. `uv.lock` does pin torch 2.14.1+cu130.
- `reports/experiments.md`: "one perceptually close pair among all 13,394 source images". This is not in the Git repository, but I confirmed it in the hosted `duplicate_audit.json` (one pair, indices 8918 and 9146, both in train).

## Problems found but not fixed

None. One cosmetic note: the README link labelled "Sections 3.1–3.2" points to anchor `#S3.SS2` (Section 3.2 only). The text is still accurate.

## Hugging Face card

The hosted card `hf://models/BurnyCoder/e2e-bsf-dinov3-imagenette-full-block-kl-seed100/README.md` matches the card template in `src/e2e_bsf/publication.py` word for word, apart from CRLF line endings. There is no separate card file in the repository. Its numbers match the `block_kl` seed-100 row in `reports/study/results.json`: KL 0.037268035, accuracy 99.2774%, NMSE 0.78616697. All 25 full-study model repositories exist under BurnyCoder. No drift, so no upload is needed.

## Regenerated artifacts and tests

Nothing was regenerated and no tests were run, because no file was changed. The study paper PDF already matches the current generator text, and the site copies are byte-identical to the report artifacts.
