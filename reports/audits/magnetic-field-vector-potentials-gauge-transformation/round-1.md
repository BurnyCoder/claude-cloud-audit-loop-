---
repo: BurnyCoder/magnetic-field-vector-potentials-gauge-transformation
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 90
fixed: 10
unverifiable: 9
not_fixed: 4
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/magnetic-field-vector-potentials-gauge-transformation, round 1
## Summary

The physics is correct. I re-derived and checked by script the curls of A=(0,bx,0) and A'=(-by,0,0), the gauge function s=-bxy+C, the square-loop circulation bL^2 and its side contributions, the symmetric-gauge midpoint and the SI rule phi'=phi-ds/dt. The code also agrees with these results, and so do the figure panels, the contours and the interactive payload. Regenerating into a scratch directory gave a byte-identical `validation.json` (all residuals 0.0 over 15 cases) and byte-identical HTML exports. The PNG matches in content; only the system font differs. `uv run pytest -q` passed 41/41, including the Chromium browser tests. I recomputed the exploratory check in the committed report PDF (45 cases, max error 1.5552e-12) and it matches the stated "approximately 1.56e-12".

The errors were all in metadata and sources:
- The clone URL used the old repository name.
- The MIT PDF was labelled "electromagnetism solutions". It is actually MIT 8.286 *The Early Universe* (A. Guth), Quiz 3 solutions, Fall 2022. Its Problem 1(d)-(e) on p. 6 does support the gauge-transformation and circulation claims.
- Some citations lacked the section or equation number.

Every external link resolves. The damtp.cam.ac.uk link fails TLS in this sandbox but resolves over HTTP; it is a genuine D. Tong PDF.

## Fixes
| file:line | before | after | evidence |
| --- | --- | --- | --- |
| README.md:28-29 | `git clone .../magnetic-field-gauge-transformation.git`, `cd magnetic-field-gauge-transformation` | `.../magnetic-field-vector-potentials-gauge-transformation.git` and matching `cd` | `gh api repos/BurnyCoder/magnetic-field-vector-potentials-gauge-transformation` → `full_name` |
| README.md:133 | "MIT electromagnetism solutions, page 6 … gauge invariance and closed-loop circulation" | "MIT 8.286 (The Early Universe, A. Guth) Quiz 3 solutions, Fall 2022, Problem 1(d)–(e), page 6: electromagnetic gauge transformation, unchanged fields, and closed-loop circulation" | https://web.mit.edu/8.286/www/quiz22/q3sols-euf22.pdf (title page; p. 6) |
| README.md:134 (new) | Sources list omitted the Tong notes cited in docs | Added D. Tong, ch. 1 "Particles in a Magnetic Field": gauge transformations §1.1.2 eq. 1.6; symmetric gauge §1.2.2 eq. 1.18 | http://www.damtp.cam.ac.uk/user/tong/aqm/solid1.pdf |
| docs/explanation.md:9 | "MIT's gauge-transformation and circulation derivation, page 6" | "…derivation in MIT 8.286 Quiz 3 solutions (Fall 2022), Problem 1(d)–(e), page 6" | MIT PDF p. 6 |
| docs/explanation.md:128-130 | "This is the symmetric gauge" (no location) | adds "(Tong, section 1.2.2, eq. 1.18)" | Tong PDF §1.2.2: A = −½ x×B = (B/2)(−y,x,0), "preserve rotational symmetry about the origin" |
| docs/explanation.md:153-155 | magnetic force qv×B unchanged (unsourced) | adds "(magnetic part of the Lorentz force law, Tong, section 1.1)" | Tong PDF §1.1: m ẍ = q(E + ẋ×B), "This is the Lorentz force law." |
| docs/reference-text.md:43 | "MIT's electromagnetic derivation, page 6" | "MIT 8.286 Quiz 3 solutions (Fall 2022), Problem 1(d)–(e), page 6" | MIT PDF p. 6 |
| src/gauge_fields/report.py:29 | link base `github.com/BurnyCoder/magnetic-field-gauge-transformation/blob/main/` | `.../magnetic-field-vector-potentials-gauge-transformation/blob/main/` | GitHub API `full_name` |
| src/gauge_fields/report.py:29 (comment) | "Keep relative experiment links usable when the PDF is downloaded alone." | states that targets inside the Git-ignored `reports/` are not published on GitHub | `.gitignore` (`/reports/`); `git ls-files` has no reports/ |
| AGENTS.md:24 | `BurnyCoder/magnetic-field-gauge-transformation` | `BurnyCoder/magnetic-field-vector-potentials-gauge-transformation` | GitHub API `full_name` |

## Unverifiable or hedged claims
- I could not establish where the three quoted passages in `docs/reference-text.md` were published. Exact-phrase web searches found nothing. The repository already says that their author, title and page numbers are not established, and I added no attribution.
- The committed `outputs/gauge-transformation-report.pdf` is a snapshot built from Git-ignored local `reports/*.md`. Several of its claims cannot be checked from the repository: wall-clock times (11:55:41, 12:30:27, 12:37:52, 12:45:50 UTC), test durations (12.53 s, 16.41 s, 16.51 s, 15.84 s), log-inspection statements, commit hashes 84f11f8 and c54931b (the clone is shallow), and the in-app-browser failure. The logs and full history behind them are not available. I counted 6 such claims.
- Report PDF claims that I did verify: 22 field tests (current count is 22), the 45-case check and its 1.56e-12 maximum error (recomputed), 15 cases on a 17x17 grid (code), Tong §1.2.2 eq. 1.18 (fetched), and repository visibility `private: false` (still public).

## Problems found but not fixed
1. **Report PDF links are stale.** `outputs/gauge-transformation-report.pdf` still links to the old repository name and to `reports/*.md` files that are never committed, so those links cannot resolve. It cannot be regenerated without the local records, and AGENTS.md forbids hand-editing it. The code fix applies to future builds.
2. **Report PDF test count is out of date.** The same PDF reports "37 tests". The current suite has 41, because `tests/test_report.py` (4 cases) was added later. This is historical snapshot prose and is left as is.
3. **Validation record overstates its coverage.** `outputs/validation.json` and its log line give `"grid_points_per_case": 289` / "15 gauges/strengths on 289 points each". That holds for the curl check only. The gradient check runs once per b (3 cases), and circulation uses a 4-edge quadrature. Changing this would change the result schema, so I left it.
4. **AGENTS.md visibility policy does not match the live setting.** AGENTS.md asks for a *private* repository, but the live repository is public (`private: false`). AGENTS.md already labels this as intended policy, and I did not change repository access.

## Hugging Face card
No Hugging Face model, dataset or Space is linked or referenced in the repository: n/a.

## Regenerated artifacts and tests
- I ran `GAUGE_OUTPUT=<scratch> uv run gauge-fields`, writing to a scratch directory so the committed snapshot report would not be overwritten by a figure-only one. `validation.json`, `gauge-transformation.html` and `gauge-transformation-interactive.html` came out byte-identical to the committed files. The PNG matches in content, with font-only differences from the local system fonts. I did not replace any committed outputs, because none of my edits change generated content.
- `uv run pytest -q`: 41 passed, both before and after the `report.py` change, including the Playwright Chromium tests.
