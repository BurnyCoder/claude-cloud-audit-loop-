---
repo: BurnyCoder/causal-counterfactual-analysis-of-convolutional-neural-networks-with-concept-swaps-interventions
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 175
fixed: 5
unverifiable: 6
not_fixed: 1
hf_card_drift: yes
---
# Fact-check audit: BurnyCoder/causal-counterfactual-analysis-of-convolutional-neural-networks-with-concept-swaps-interventions, round 1
## Summary
I checked the README in full, the paper's prose numbers and citations, the generated tables and the Hugging Face card. I ignored earlier audit files as evidence. The numbers are in very good shape:
- `reports/generated/results.md` and `reports/generated/numbers.tex` regenerate byte-identically from `results/*.json`. I ran `report_tables.run` in a CPU-only venv without torch.
- Every README number I recomputed matches, as do the paper's non-macro numbers. The recomputations used scripts reading the result JSONs, the run logs and the hosted per-pair CSV (`data/pairs_h1_confirmatory.csv`, `data/stimuli.csv`). They covered the null-set means and maxima, the example rows, the hero sweep, the per-subset breakdowns, the rotation ratios, the runtimes and the AUROC ranges.
- External citations I fetched match their sources: Huang et al. 2023, Baeumel et al. 2025, Owen 2007, Geiger et al. JMLR 26(83), the Curve Circuits footnote (88.6% to 86.3%, 87.6%, 2000 images), Branch Specialization (all 30 curve-related mixed3b features in the 5x5 branch), Gurnee et al. 2026 (J-lens vector swaps), Cammarata 2026 (revisits layer 3b), the uv 0.8.6 changelog (#15095), the Lucent forward-pass lines L246-L249, and Lucid's 1008-way softmax.

I made two fixes:
- The GitHub URL in the README clone instructions, the paper and the HF card used the repository's old name. It still redirects (`git ls-remote` returns the same HEAD), but it is not the current name.
- The README methodology said that 2000 null sets of each kind were used, without saying for which tests. The JSONs show 2000 only for H1 and H4, 1000 for H2, the composited test and H5, and 500 for the ridge readout, the seeds and the LRN check.

## Fixes
| file:line | before | after | evidence |
|---|---|---|---|
| README.md:187,190 | `git clone https://github.com/BurnyCoder/counterfactually-causal-analysis-of-convolutional-neural-networks-with-concept-swaps` and `cd counterfactually-...` | current repository name `causal-counterfactual-analysis-of-convolutional-neural-networks-with-concept-swaps-interventions` | `git remote -v` of the clone; GitHub API `repos/BurnyCoder/causal-counterfactual-...` |
| README.md:163-164 | "2000 activation-change-matched null sets. 2000 branch-matched null sets." | 2000 for H1 and H4, 1000 for H2, 500 for the ridge readout, the jitter seeds and the LRN check; branch-matched nulls have the same sizes | `n_sets` in `results/e2_synthetic.json` (H1 2000, H4 2000, H2 1000, H1_ridge_all4a/H1_seed3/H1_seed4/H1_lrn_lucent 500) |
| reports/paper/paper.tex:217 | `\url{https://github.com/BurnyCoder/counterfactually-causal-...}` | current repository URL | same as row 1 |
| docs/hf_dataset_card.md:23 | link text and URL with the old repository name | current repository name and URL | same as row 1 |

## Unverifiable or hedged claims
- A comment on lucent#51 (`issuecomment-6345247394`), cited for the LRN derivation and the 6e-6 error. The GitHub API for greentfrapp/lucent is blocked in this session, so I could not read the comment. I checked the TF LRN formula against the constants in the paper only by reasoning, not against the comment.
- Aguilar Canto et al. 2026 (OpenReview `GWpe8AdMk3`). The page returns HTTP 200, but the API needs a browser challenge, so I could not check the title, authors or venue.
- Baeumel et al. 2025 page range (pp. 1380-1409) and Huang et al. 2023 BlackboxNLP pages (317-331). Semantic Scholar confirms the venue IJCNLP-AACL 2025 for Baeumel. The ACL Anthology pages did not return metadata.
- `inception5h.pth` is 28 MB and Imagenette-320 is 342 MB. I did not check either.
- "`--quick` takes under a minute on an RTX 5070 Laptop". No quick-run log is committed. The full-run and phase runtimes (57, 22, 5, 4 and 3 min) do match the committed logs.
- The erratum on smoke-test runs that touched about 99 confirmatory photos, with H5 IIA 0.029. The relevant logs are gitignored.

## Problems found but not fixed
- `reports/paper/paper.pdf` was not rebuilt after the one-line URL change in `paper.tex`, because LaTeX is not installed. The PDF still shows the old (redirecting) repository URL in Appendix A. Rebuild it with pdflatex.
- I did not count this as a factual issue: `paper.tex` repeats `\bibliographystyle{plainnat}` twice. It is harmless and I left it alone.

## Hugging Face card
The hosted card at `hf://datasets/BurnyCoder/inceptionv1-curve-concept-swaps/README.md` was identical to `docs/hf_dataset_card.md` before this audit; the only difference was a trailing newline. After this audit the repository copy differs in one line: the GitHub link (line 23) now uses the current repository name. The hosted card still has the old, redirecting URL. The card's other claims match the CSV columns: the dataset has 4608 pair rows and 2304 stimulus rows, and IIA = mean `family_success` over `eligible` rows = 811/4574 = 0.177307. To sync:

`huggingface-cli upload BurnyCoder/inceptionv1-curve-concept-swaps docs/hf_dataset_card.md README.md --repo-type dataset`

## Regenerated artifacts and tests
- I ran `concept_swap.phases.report_tables.run(load_config())` with numpy, matplotlib, statsmodels and python-dotenv in a scratch venv. torch is not needed for this phase. `results.md` and `numbers.tex` came out byte-identical. The figure PNGs differed only in bytes because of matplotlib version differences, with the same data, so I reverted them.
- I changed no code, so I did not run the tests. Running them needs `uv sync` with the CUDA torch wheels, which is over the 1 GB download limit.
- The paper PDF was not regenerated (no LaTeX).
