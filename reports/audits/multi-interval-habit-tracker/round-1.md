---
repo: BurnyCoder/multi-interval-habit-tracker
round: 1
branch: fact-check/2026-11-05-r1
claims_checked: 48
fixed: 4
unverifiable: 2
not_fixed: 2
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/multi-interval-habit-tracker, round 1

## Summary

The repository is a small React + Express habit tracker (26 tracked files). Its claim surfaces are README.md, the UI strings in src/App.tsx and src/domain/scoring.ts, index.html, start.bat, and code and test comments. There is no paper, docs/ folder, AGENTS.md/CLAUDE.md, results folder, GitHub Pages site or Hugging Face card.

I checked every README statement against the code. I ran the test suite (15/15 pass), lint (clean) and build (OK), started the backend in a scratch directory, and ran short tsx probes of the scoring engine, including a 300-run fuzz of the daily breakdown. Most README claims hold. Four claims were wrong or overstated and are now fixed:
- the intro sentence described Habitica as the app with a local backend
- one UI label was miscapitalised
- two archive/restore statements did not match what the code does on edge-case dates

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| README.md:3 | "Additional functionality to complement [Habitica], a browser-based app for tracking habits ... persisting data in your project folder via a local backend service." (the appositive grammatically describes Habitica) | "A browser-based app for tracking habits ... built as additional functionality to complement [Habitica]. It runs standalone (it does not connect to a Habitica account or API) and persists data in your project folder via a local backend service." | server/index.ts:8, server/store.ts (file persistence); src/httpApi.ts calls only `/api/*`; no Habitica references in src/ or server/; https://habitica.com/ (title "Habitica - Gamify Your Life") |
| README.md:23 | `Jump to Date` | `Jump to date` | src/App.tsx:211 (label text "Jump to date") |
| README.md:25 | "archived habits stop accruing score" | "...stop accruing score after the archive date (the archive date itself still counts, and the habit stays in the Active list until the simulated date moves past it)" | src/domain/scoring.ts:374-398 (`endDate: date`, inclusive) and 110-120 (`isDateWithinPeriod` uses `<=`); tsx probe: after archiving on 2026-03-05 the habit is still active that day ("Overdue (4 / 2, 2 days late)") and frozen at -2 on 03-06; live backend POST /api/habits/:id/archive on the current date returned `status: "active"` |
| README.md:26 | "restoring starts a fresh cycle at restore date" | "...except when restoring on the day right after the archive date: the two active periods are then merged and the previous cycle, including any overdue days, continues" | src/domain/scoring.ts:83-88 (`normalizeActivePeriods` merges adjacent periods); tsx probe: archive 03-05, restore 03-06 gives one period 03-01..null and "Overdue (5 / 2, 3 days late)", score -3; restore 03-08 gives a fresh cycle "Waiting (0 / 2)" |

## Unverifiable or hedged claims

- README.md:5 screenshot `https://github.com/user-attachments/assets/f3141bfa-...`: the session proxy blocks this path (403 "sessions are bound to their configured repositories"). I could not confirm that the image exists or that it is 2026x1121 as the `width`/`height` attributes state. Left unchanged.

Verified and unchanged:
- every score rule (+1 per completion, -1 per overdue day, completion day not overdue, reset to Day 0)
- automatic creation of data/habits.json, confirmed with a live run
- port 8787 and the `/api` proxy (vite.config.ts; Vite docs https://vite.dev/config/server-options give the `server.proxy` prefix rule and the default `server.port` of 5173 that start.bat opens)
- Up/Down reorder in both lists
- the breakdown table: it sits at the bottom of the page, lists active habits in Active order, and only ever shows deltas of +1, 0 or -1 (fuzz over 8,163 active days found no other value)
- the stack description
- every npm script named in the README
- the "Day N" comments in src/domain/scoring.test.ts
- the status labels

## Problems found but not fixed

1. **Archiving on the current simulated date has no visible effect.** `archiveHabitAtDate` sets the period end to the archive date inclusive. The habit stays `status: "active"`, stays in the Active list and keeps being scored that day; it only moves to Archived after Next Day. This looks unintended, but the right semantics (for example, ending the period on the day before) is a design decision and not a small, clear fix. I documented the behaviour in the README and left the code alone.
2. **Restoring the day after the archive date does not start a fresh cycle.** The adjacent-period merge in `normalizeActivePeriods` looks deliberate (`previousAdjacentOrAfter`), but it contradicts the "fresh cycle" intent. I documented it and left the code unchanged.

Minor notes, not errors:
- The README does not mention the Edit feature (rename and change interval, effective from the current simulated date).
- start.bat's default path `~/projects/habitica-extension` differs from the repo name. The README already tells users to edit it.

## Hugging Face card

n/a. The repository links no Hugging Face model, dataset or Space.

## Regenerated artifacts and tests

- No generated artifacts (tables, figures, paper) exist in the repository.
- No code was changed. On the audited tree: `npm test` 15/15 passed (vitest 4.0.18), `npm run lint` clean, `npm run build` succeeded. The build output (dist/) is gitignored and not committed.
