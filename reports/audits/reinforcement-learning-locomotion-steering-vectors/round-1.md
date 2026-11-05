---
repo: BurnyCoder/reinforcement-learning-locomotion-steering-vectors
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 370
fixed: 5
unverifiable: 8
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/reinforcement-learning-locomotion-steering-vectors, round 1
## Summary

I checked the README, the paper (`reports/paper.md` and PDF), the HF card, the experiment register, the Ant findings, the independent-audit and completion reports, the HalfCheetah 004 findings, the 002 validation inspection, `docs/` (methodology, sources, usage, ant-videos, ant-publication, pgs-adaptation), the explorer's visible text and the code comments that state numbers. I recomputed numbers with short scripts from `reports/*/results.json`, `manifest.json`, `vectors.npz`, `reports/ant-classic-005-independent-audit/audit.json`, `reports/ant-publication/evidence.json`, `site/data/episodes/*.json` and the 002 pooled-quality file. I also read the JSON metadata inside the two pinned upstream checkpoint ZIPs without unpickling them; both SHA256 hashes match the repository.

Every number I recomputed matched to the printed precision. That covers:
- both Ant tables: the original confirmation and every named arm of both signs in the later audit;
- the P1/P2/S1/S2/M1/M2 statistics, including recomputed Monte Carlo ranks (0.05, 0.40, 0.21, 0.01);
- the odd/even, sensitivity, kinematics and clipping tables;
- the extraction statistics;
- the HalfCheetah 001–004 counts and the 004 confirmation table, including the claim of a +0.40% maximum speed gain over 238 settings;
- the gate thresholds and selection rule in code;
- the seed partitions, software versions and checkpoint metadata: seed 0, 5.92M/8.77M timesteps, LR 3e-4, gamma 0.99, batch size 256, buffer 1e6.

The citations I fetched all resolve and match on title, authors and year: 7 arXiv IDs, 2 DOIs via Crossref, the Minari dataset pages, the pinned Minari train/upload scripts, the Baukit setup.cfg (and its missing LICENSE), the PGS repo line anchors and license, the SB3/TQC/Baukit line anchors, and the MuJoCo 3.1.5 plane-texture code behind "20 m squares, 40 m period".

I found and fixed five wording or link errors in templates and regenerated their outputs. None of them changes a reported number.

## Fixes

| file:line | before | after | evidence |
| --- | --- | --- | --- |
| docs/publication/findings.md.in:29, reports/ant-classic-005-findings.md:43 | "Baseline and treated failure counts are each 4/30, with different failed-seed identities." | "... each 4/30, on partly different seeds; only the shared pre-onset ending fails in both arms." | site/data/episodes/confirmation--lateral__-0.1000.json: baseline fails {520004, 520007, 520025, 520027}, treated fails {520010, 520020, 520025, 520026}; results.json decision text (seed 520025 ends at step 34 in both arms) |
| docs/publication/independent.md.in:69, reports/ant-classic-005-independent-audit.md:119 (+PDF) | "encountered a MuJoCo memory-allocation failure and resumed with fewer workers; the original complete logs retain that failure and retry." | The 12-worker attempt stopped after 7 of 124 directions and resumed with 6 workers. The logs keep the interruption and the retry but no error message. The memory-allocation cause is attributed and is not recorded in those logs. | reports/ant-classic-005-independent-audit/20261016T142559607453Z.log ends at "collected direction random000 (7/124)" with no error; 20261016T142815485407Z.log shows workers=6; no traceback or MuJoCo error text in any log |
| docs/publication/independent.md.in:69, reports/ant-classic-005-independent-audit.md:119 | "[completion ledger](../docs/ant-publication.md)" for build/test failures | "[completion ledger](ant-publication-completion.md)" | reports/ant-publication-completion.md is the ledger and links the build/test logs; docs/ant-publication.md has reproduction steps only |
| docs/publication/register.md.in:9, reports/experiments.md:11 | "[completion ledger](../docs/ant-publication.md) records corrections, historical noncompliance, and remaining limits" | link target `ant-publication-completion.md` | reports/ant-publication-completion.md (requirement table, "Not retroactively repairable") |
| docs/publication/paper-appendix.md.in:13, reports/paper.md:251 (+PDF) | "[completion ledger](.../docs/ant-publication.md) records checks, failures, retries, receipts, and requirements..." | link target `.../reports/ant-publication-completion.md` | same as above |

## Unverifiable or hedged claims

- Baukit pin "dated 22 February 2024" (docs/sources.md:27): I could not reach the GitHub API or the commit page's date in this session.
- 001 eligible-window median 14.593 m/s and IQR 13.899–15.192 (reports/experiments.md:56, hc-classic-001-diagnostics.md): the per-window speeds are not committed. The 7.2965 m/s floor equals 14.593/2, so the numbers are internally consistent.
- "core implementation passed 23 tests" and the "about 1.10 seconds" smoke rollout (reports/experiments.md:66): the repository does not log them, and the text already flags the timing as unlogged.
- Replay byte-for-byte media correspondence and the 002 contact-geometry replay assertions: these are historical model-execution checks that I could not repeat without running models. The docs already label them as historical.
- The MuJoCo memory-allocation cause of the 12-worker stop: now hedged, see Fixes.
- AI statement in the paper ("Codex wrote this codebase..."): authorship claim with no artifact evidence.

## Problems found but not fixed

- docs/huggingface-model-card.md:43 (generated from featured.md.in) labels docs/ant-publication.md as "Reproduction and completion ledger". The page holds reproduction steps and only links the ledger. This is minor, and I left it so the card would not drift from the Hub.
- The Hub publication copies under `documentation/` and `paper/` (for example `paper/paper.pdf`) now lag the repository by the three wording/link fixes above. The orchestrator or owner should re-run `scripts/publish_ant_documents.py` if those copies must stay in sync.

## Hugging Face card

I read the hosted card `hf://models/BurnyCoder/rl-locomotion-steering-vectors/README.md` with hf_fs. It is 11,785 bytes, the same size as docs/huggingface-model-card.md, and its text is identical. This audit did not change the card, so there is no drift and no upload is needed. Card numbers I checked:
- the confirmation table;
- +0.462 [0.343, 0.587] with 19/20 positive pairs;
- failures 0/20 to 2/20 and rank 0.05;
- norm 5.15135 and applied norm 0.51513;
- checkpoint hashes, 105 observations and 8 actions;
- the experiment table's 001–005 outcomes.

If a later round edits the card: `huggingface-cli upload BurnyCoder/rl-locomotion-steering-vectors docs/huggingface-model-card.md README.md`.

## Regenerated artifacts and tests

- The full `scripts/build_ant_publication.py --check` needs 1.75 GB of pinned inputs, which is over the 1 GB download limit, so I did not run it. Instead I called the repository's own `render_documents(root, evidence)` directly on the committed `reports/ant-publication/evidence.json`, in a scratch venv with the uv.lock-pinned reportlab 4.5.1, numpy 1.26.4, pillow 12.3.0, matplotlib 3.11.1 and scipy 1.14.1.
- Before any edit, this reproduced all nine generated documents byte-for-byte, including README.md, the card, paper.md, paper.pdf and the independent-audit PDF.
- After editing the templates I regenerated them. Only ant-classic-005-findings.md, ant-classic-005-independent-audit.md/.pdf, experiments.md and paper.md/.pdf changed. Figures, evidence.json and the site data are unaffected because no evidence changed.
- Tests: `pytest tests/test_ant_publication_documents.py tests/test_build_paper.py` gave 22 passed. No Python source code was modified.
