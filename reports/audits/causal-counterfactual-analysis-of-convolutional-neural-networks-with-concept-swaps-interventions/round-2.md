---
repo: BurnyCoder/causal-counterfactual-analysis-of-convolutional-neural-networks-with-concept-swaps-interventions
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 210
fixed: 6
unverifiable: 3
not_fixed: 1
hf_card_drift: yes
---
# Fact-check audit: BurnyCoder/causal-counterfactual-analysis-of-convolutional-neural-networks-with-concept-swaps-interventions, round 2
## Summary
I checked the repository myself and did not use earlier audit files as evidence. First I regenerated `reports/generated/results.md` and `numbers.tex` from `results/*.json` with `report_tables.run`, in a scratch copy on CPU. Both came out byte-identical, so every number the paper takes from macros matches the result JSONs.

I then compared the README's numbers with results.md and the JSONs: the results table, the takeaways, the success table, the null-set sizes, the best null set (6/4574), 0.008% and 0.001%, and the 1-of-4574 top-Δ figure. I also checked them against the per-pair Hugging Face export (`pairs_h1_confirmatory.csv` + `stimuli.csv`), covering 811/4574, the radius, polarity and width rates, the source-orientation rates, 651/811, the medians, all 9 example rows and the hero base's 4 sources. Further checks:
- the hero sweep log (61, 14, 15 orientations) and the commit and log timestamps
- the phase timings from the logs
- the paper's hard-coded numbers (AUROC ranges, 1.8×, 0.929, 1.7%, 0.136, pilot 0.16)
- report and docs numbers not found in results.md
- citations: Huang 2023, Baeumel 2025, the lucent#51 comment, Lucid's 1008-way softmax, the Owen 2007 DOI and arXiv ID, the uv 0.8.6 / #15095 release note and the Imagenette size (341,663,724 B)

Almost everything holds. One README error: the post-hoc subset CIs did not come from the method described.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| README.md:471-473 | CIs from the pigeonhole bootstrap "run separately within each subset; other seeds move the bounds by up to about 0.5 percentage points" | bootstrap "drawn once over all 4,574 eligible pairs, with each subset's rate and each difference computed under the same replicate weights; other seeds move the bounds by up to about 0.6 percentage points" | Recomputed from HF `data/pairs_h1_confirmatory.csv` with `concept_swap.stats` (B=2000, seed 0). The joint bootstrap reproduces the README's difference CIs exactly ([2.9, 15.6], [2.0, 10.2]). Separate per-subset bootstraps give r30 [17.3, 28.7] and r80 [9.5, 17.8], so they do not reproduce them. Seeds 0–3 move the joint bounds by up to 0.58 pp. |
| README.md:482 | Radius 30 px: 22.6% [17.7, 27.7]; 80 px: 13.5% [9.8, 17.2] | [17.9, 27.9]; [9.9, 17.4] | same recomputation (joint, seed 0) |
| README.md:484 | light-on-dark 20.7% [17.5, 24.1] | [17.4, 24.2] (dark-on-light [12.1, 17.5] unchanged) | same recomputation |
| reports/posthoc_robustness.md:272-273 | "largest deviation 0.0011, in the 5×5 branch and its 8 readout units" | "largest deviation 0.0011, in the 5×5 branch; 0.0006 for its 8 readout units" | `results/posthoc_audit2.json` `additivity_by_branch`: 5x5 sum−1 = 0.00108; curve_units_5x5 = 0.00062 |

## Unverifiable or hedged claims
- `inception5h.pth` is 28 MB (README:211, docs/architecture.md:88). The GitHub source was blocked in this session.
- Smoke-run "H5 IIA 0.029" and "composited IIA 0.164" (paper Limitations, all_experiments.md:149). Those logs are gitignored and not in the repository.
- "The effect changes from 0.40995 to 0.40996" with an eligible-only denominator filter (paper, e2/posthoc reports). I did not recompute this.
- Not re-checked for lack of budget: most qualitative literature-review descriptions (docs/literature_review.md) and the Curve Circuits 88.6/86.3/87.6% figures.

## Problems found but not fixed
- The hosted Hugging Face card differs from the repository copy (see below). I cannot write to the Hub.

## Hugging Face card
The hosted `hf://datasets/BurnyCoder/inceptionv1-curve-concept-swaps/README.md` differs from `docs/hf_dataset_card.md` on one line only. The hosted card links to the old repository name, `BurnyCoder/counterfactually-causal-analysis-of-convolutional-neural-networks-with-concept-swaps`, and the repository copy uses the current name. The repository copy is correct and needed no edit. Upload command:
`huggingface-cli upload BurnyCoder/inceptionv1-curve-concept-swaps docs/hf_dataset_card.md README.md --repo-type dataset`

## Regenerated artifacts and tests
- `report_tables.run` (CPU, JSON only) in a scratch copy gave byte-identical `reports/generated/results.md` and `numbers.tex`. The PNG figures differed only in bytes (matplotlib version), so I did not commit them.
- Only prose changed, so I did not regenerate the paper PDF (it has no README content) and did not run the tests (no code touched).
