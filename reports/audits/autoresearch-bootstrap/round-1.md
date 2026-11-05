---
repo: BurnyCoder/autoresearch-bootstrap
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 41
fixed: 10
unverifiable: 0
not_fixed: 1
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/autoresearch-bootstrap, round 1

## Summary

The repository has 9 tracked files: `README.md` and eight agent instruction templates (`AGENTS-{FROM-SCRATCH,BUILDING-ON-TOP-OF}[-DRIVE][-HARDWARE].md`). It has no code, results, paper, figures, UI or Hugging Face card, so all checks were on prose. Ground truth was (a) the templates themselves, cross-checked by a script (section numbers, workflow step references, and whether each file has the features its name promises), and (b) primary sources fetched on 2026-11-05: `karpathy/autoresearch` `program.md` and `README.md` (raw.githubusercontent.com, master), the uv CLI reference and the rclone `ls` and Google Drive docs.

I fixed 10 claims in 7 commits. The template errors were: a workflow step that pointed to itself in all FROM-SCRATCH templates; "sleep cycle" (about 90 min) used where the arithmetic needs a night of sleep (about 8 h), in all 8 templates; "(currently empty) repo" in templates that also tell the agent to read `paper.pdf` and the existing codebase; a reference to a nonexistent input paper in FROM-SCRATCH; and one DRIVE template that said rclone storage *is* available, unlike the other three. In the README, two summary bullets did not match the templates. The README also had no sources, so I added links to the uv and rclone docs and credited `karpathy/autoresearch`, which the loop, autonomy rules and pacing text are adapted from.

## Fixes

| file:line | before | after | evidence: result file path or URL |
|---|---|---|---|
| AGENTS-FROM-SCRATCH.md:79, AGENTS-FROM-SCRATCH-HARDWARE.md:83, AGENTS-FROM-SCRATCH-DRIVE.md:86, AGENTS-FROM-SCRATCH-DRIVE-HARDWARE.md:86 | `5. Repeat step 5, recording findings as you go` | `5. Repeat step 4, ...` | Same files, Workflow Summary: step 4 is "Run experiments → log results → ...". In BUILDING-ON-TOP-OF that step is 5, so "Repeat step 5" is correct there and was left alone |
| All 8 AGENTS-*.md (lines 70/74/75/76/77/77/79/79) | "roughly 100 experiments over an average sleep cycle" | "roughly 100 experiments over an ~8-hour night of sleep" | 60/5 = 12 per hour; 100/12 = 8.3 h; 12 × 8 = 96. A sleep cycle is about 90 min (https://en.wikipedia.org/wiki/Sleep_cycle, "standard figure ... 90 minutes"), which fits only about 18 experiments. The source text says "the average human sleep": https://raw.githubusercontent.com/karpathy/autoresearch/master/program.md line 114 |
| AGENTS-BUILDING-ON-TOP-OF.md:18, -HARDWARE.md:19, -DRIVE.md:22, -DRIVE-HARDWARE.md:22 | "Work inside this (currently empty) repo." | "Work inside this repo." | Same files, §1: "Read `paper.pdf`" and "Read the entire existing codebase in this repo", so the repo is not empty. README: BUILDING-ON-TOP-OF "includes paper and existing-codebase inputs" |
| AGENTS-FROM-SCRATCH.md:31, -HARDWARE.md:35, -DRIVE.md:38, -DRIVE-HARDWARE.md:38 | "re-read the paper and referenced works" | "read relevant papers and their referenced works" | README: FROM-SCRATCH "starts without paper or existing-codebase inputs". The FROM-SCRATCH templates never give a paper to read, so "the paper" pointed at nothing |
| AGENTS-FROM-SCRATCH-DRIVE-HARDWARE.md:11 | "Cloud storage is available via rclone, inspect ..." | "If cloud storage is available via rclone, inspect ..." | The other three DRIVE templates (BUILDING-ON-TOP-OF-DRIVE.md:13, -DRIVE-HARDWARE.md:13, FROM-SCRATCH-DRIVE.md:11) use "If ...". README calls rclone storage "optional" |
| README.md:34 | "... experiment results, model outputs, and a LaTeX research paper" | "... experiment results, trained, fine-tuned, or steered model artifacts, and a LaTeX research paper" | Every template's Deliverables item 3: "Any trained, fine-tuned, or steered model artifacts" |
| README.md:43 | "validate that results are meaningful, reproducible, and well logged" | "validate that results make sense, that the code runs end to end, and that logging is sufficient" | The templates' Quality Checkpoints ask "Do the current research results make sense?", "Does the code run end-to-end without errors?" and "Is logging sufficient and informative?". Reproducibility is not mentioned anywhere |
| README.md:46 (uv) | "`uv` for environment management" (no source) | linked to https://docs.astral.sh/uv/ | Fetched: HTTP 200, title "uv". CLI reference lists `uv add`: "Add dependencies to the project" (https://docs.astral.sh/uv/reference/cli/) |
| README.md:46 (rclone) | "`rclone`, for example `rclone ls googledrive:projects/<project-name>`" (no source) | linked to https://rclone.org/ and https://rclone.org/commands/rclone_ls/; notes that `googledrive` is the name of a configured rclone remote | rclone_ls page: "Lists the objects in the source path ... with size and path". Drive docs: "Paths are specified as `drive:path`", where `drive` is the remote name (https://rclone.org/drive/) |
| README.md:50 (new) | (no provenance given) | "The keep-or-discard research loop, the autonomy rules and the example pacing in the templates are adapted from `program.md` in karpathy/autoresearch" | https://raw.githubusercontent.com/karpathy/autoresearch/master/program.md lines 106 (keep/discard, advancing the branch, rewinding "very very sparingly (if ever)"), 112 (NEVER STOP, "should I keep going?", near-misses, more radical changes) and 114 (~5 min, ~12/hour, ~100 overnight) |

## Unverifiable or hedged claims

None left. The pacing sentence now rests on its own arithmetic (12/hour × ~8 h ≈ 96 ≈ 100), not on an unsourced average sleep duration. The ~90-minute sleep-cycle figure is used only in this report, to explain the fix, and comes from a secondary source (Wikipedia). NIH pages (NINDS, NCBI StatPearls) were blocked (403 or captcha) and could not be fetched.

## Problems found but not fixed

1. **Template name vs. AGENTS.md (owner decision).** Every template tells the agent to write its plan to `AGENTS.md`, and the quality checkpoint asks "Is `AGENTS.md` accurate and up to date?". But the files are named `AGENTS-*.md`, and the README never says to copy or rename the chosen template to `AGENTS.md`. This is a usage gap, not a false statement, so I left it.
2. (Note, not counted.) `https://github.com/karpathy/autoresearch/blob/master/program.md` returned 403 through this session's proxy, which blocks GitHub HTML for repositories not attached to the session. The same file at the same branch and path loaded from raw.githubusercontent.com (HTTP 200), so the link is valid.

## Hugging Face card

n/a. The repository has no Hugging Face card and links no Hugging Face model, dataset or Space.

## Regenerated artifacts and tests

No derived artifacts (no tables, figures, paper or build scripts) and no code or tests in the repository. A consistency script checked all 8 templates after the edits. In each one:
- the "Final quality checkpoint (see §N)" reference matches the Quality Checkpoints section number;
- the "Repeat step N" reference matches the "Run experiments" step;
- the file has rclone guidance exactly when its name has DRIVE, local-compute guidance exactly when it has HARDWARE, and `paper.pdf` exactly when it is BUILDING-ON-TOP-OF.

All 8 README template links resolve to existing files. The branch was pushed to `origin/fact-check/2026-11-05-r1`.
