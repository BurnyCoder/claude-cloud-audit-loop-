---
repo: BurnyCoder/looped-transformers-llms-neuron-mechanistic-interpretability
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 160
fixed: 2
unverifiable: 2
not_fixed: 1
hf_card_drift: no
---
# Fact-check audit: BurnyCoder/looped-transformers-llms-neuron-mechanistic-interpretability, round 2
## Summary
I did this audit independently and did not use earlier audit files as evidence. I recomputed every number in the README Highlights table and in the paper's results sections (abstract, atlas, selection, follow-ups, audit, robustness, LLM judge, replication) with short scripts that read `results/Ouro-1.4B/*.json` and `cross_loop_corr.npz`. I used scipy for the audit Wilcoxon tests. Spot checks covered reports 01, 04, 06 and the summary, `docs/setup.md`, and the methods claims in the code (sampling settings, 2,000 random contexts, 12 explanation and 8 held-out examples, stats every 8th batch, quantiles, KV-cache tolerance).

I also checked:
- **Citations:** all 23 arXiv IDs via the arXiv API (titles, authors, years), 3 DOIs via Crossref, and the JSTOR and NeurIPS links.
- **External sources:** the Goodfire, nesiacel (LessWrong), Suiche and Transluce pages.
- **Hugging Face:** the Ouro-1.4B and Ouro-1.4B-Thinking cards, the configs of Ouro-1.4B and Ouro-2.6B, file sizes on the Hub, and `modeling_ouro.py` at the pinned revision.
- **Ouro paper:** the §5.3 "moderate degradation" quote and the 8.3M-example SFT figure in Table 6, both read from the arXiv PDF.

Every recomputed number matched its result file at the stated rounding. I found and fixed two wording errors about external sources.

## Fixes
| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| paper/sections/related.typ:11-12 | "...and that steering along the refusal direction removes refusal @suiche2026abliterating" | "...and that its refusal control vector (at α = 1) removes refusal (4/32 to 32/32 compliance)" | https://msuiche.com/posts/abliterating-a-loop-control-vectors-meet-the-looped-transformer/ (Ouro-2.6B section "The day after": the shipped vector takes refusal compliance from 4/32 to 32/32 at α = 1.0; it says nothing of steering along the direction) |
| README.md:3 | "(Cammarata, Goodfire, Oct 2026)" | "(Cammarata, Goodfire, 2026; the page gives no publication date, only a revision on Oct 30, 2026)" | https://already-clean.goodfire.com/ (no publication date; only a footnote "Revised October 30, 2026") |

## Unverifiable or hedged claims
- **Goodfire essay date.** The page has no publication date, so "Oct 2026" could not be confirmed. It is now hedged in the README (fix above). The bib entry says only year 2026, which is fine.
- **Disk budget in `docs/setup.md`.** The sizes come from `du -sh` on the development machine. I confirmed the sizes listed on the Hub (GGUF 5.68 GB, Ouro-1.4B safetensors 2.87 GB). I could not check the local `.venv`, `tools/` or results sizes.

Claims I verified and left alone:
- Ouro card: "matches 3-4B", 7.7T tokens, the architecture table, and the `transformers<4.56` advice.
- Thinking card: about 8.3M SFT examples, 2 epochs, and the math/code/science/chat mix.
- Ouro-2.6B: 48 layers and a 5.34 GB checkpoint.
- nesiacel (Sep 2026, Ouro-1.4B-Thinking): last-loop advantage, "rotated away", and self-repair offered as a suggestion.
- Goodfire: same-layer random-ablation control, steering, positive and negative poles, and a 100M-token corpus.
- Transluce: all MLP neurons of Llama-3.1-8B-Instruct.
- Kirin, Blayney, Parcae, Huginn and Gerstner summaries match their abstracts.

## Problems found but not fixed
- **Dose-response wording** (README Highlights, report 04 §2, paper follow-ups). The text says ΔC "levels off for 4 of 6 neurons ... (L4 N2104 and L6 N3344 still rise)". But L18 N3066 gains +0.025 from α = 8 to 16 (0.313 → 0.338, `followups.json`), which is more than L4 N2104's +0.014 (0.283 → 0.296), and L4 N2104 is the one called still rising. From α = 4 to 16, L18 N3066 is nearly flat (0.324 → 0.338). The text already says this is qualitative and that no curve was fitted, so I left it as a judgment call. The authors may want to define "levels off" with a threshold.
- **Minor imprecision, not an error.** Paper and summary say fresh-prompt replication has Holm p ≤ 2.1e-16. The actual maximum is 2.0e-16 (`replication_fresh.json`), so the bound is true but loose. Not counted above.

## Hugging Face card
- **Hosted vs repository copy.** I read the hosted card for `hf://datasets/BurnyCoder/ouro-1.4b-neuron-atlas/README.md`. It matches the repository copy word for word: the `DATASET_CARD` string in `run_pipeline.py`, lines 364-400. There is no drift, so no upload is needed.
- **Card claims checked:** 135,168 neurons (24 × 5632), 987,840 tokens per layer and loop (matches `logs/20261024-165339_build_atlas.log`), `tokens_atlas.npy` with shape [31250, 256] (= 8M tokens), revision 574fa66, and Apache-2.0 for Ouro.
- **Not checked:** the tensor shapes inside `atlas.pt` (the file is not in git, and I did not download it).

## Regenerated artifacts and tests
- **Paper PDF.** I rebuilt `paper/paper.pdf` with `paper/build.py`, using the typst Python package at the locked version 0.15.0, run through `uv run --no-project --with typst==0.15.0`. The rebuilt PDF has the corrected related-work sentence.
- **Tables.** `reports/tables/` were not regenerated because no result data or table code changed.
- **Tests.** I changed no code, so I did not run tests.
