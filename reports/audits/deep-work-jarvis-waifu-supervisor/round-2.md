---
repo: BurnyCoder/deep-work-jarvis-waifu-supervisor
round: 2
branch: fact-check/2026-11-05-r2
claims_checked: 58
fixed: 3
unverifiable: 8
not_fixed: 0
hf_card_drift: n/a
---
# Fact-check audit: BurnyCoder/deep-work-jarvis-waifu-supervisor, round 2

## Summary

The repository is a Windows focus-enforcement app, not an ML training project. Its claim surfaces are README.md, AGENTS.md/CLAUDE.md, docs/, two dated reports (Markdown plus PDF), the dashboard screenshot, the UI, and code comments. I checked 58 claims against code, `uv.lock`, test runs, git history, and primary sources fetched today. README and the main docs agree with the code: defaults, the 14-group catalog, 960 px tiles, JPEG quality 80, the 3 s poll, the 1–240 minute limits, the five-observation summary, `credited_minutes`, the 30-minute praise, the 30 s readiness deadline, and the store/retention statements.

External facts that checked out:
- The GPT-6 Luna page lists image input, structured outputs, and medium as the default effort.
- `gpt-4o-mini-tts` was deprecated on 2026-10-01 with removal on Jan 6, 2027.
- The TTS page lists 13 voices.
- OpenAI's retention page says no training by default, abuse-monitoring logs for up to 30 days, and Responses data stored for at least 30 days.

I independently recomputed several report numbers:
- At migration commit `de9be3a`: 251 tests in the full suite and 44 in the focused four-file run.
- Current HEAD: 277 pytest tests and 12 Node tests.
- Running the final Node suite against the pre-fix `dbe6684` dashboard gives 10 of 12 failing, as the report says.
- The category sums are consistent: 917+688+94=1,699 and 3+3+1+2=9.

I fixed 3 claims, all in troubleshooting text and a code comment. No result data was edited.

## Fixes

| file:line | before | after | evidence |
|---|---|---|---|
| docs/troubleshooting.md:172 | HostsFileHijack "flags suspicious hosts modifications and may reset entries" | "flags suspicious hosts modifications and that remediating it resets the hosts file to default, removing existing entries" | https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=SettingsModifier%3AWin32%2FHostsFileHijack |
| docs/troubleshooting.md:138-142 | The cache → hosts → DNS-server order was sourced only by the `ipconfig` page link, which does not document it | Added a link to the Microsoft DNS client troubleshooting article (Scenario 2), which lists that order | https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/troubleshoot-dns-client-resolution-issues#scenario-2-theres-an-entry-for-the-domain-name-in-the-hosts-file |
| deepwork/config.py:25 | "Windows itself locates hosts under its installation directory" (cited article does not say this) | "Microsoft's DNS troubleshooting article shows hosts at this location" | same Microsoft DNS article (shows `C:\Windows\System32\drivers\etc` only) |

## Unverifiable or hedged claims

These are already hedged in the repo, and I left them as they are:
1. Migration report live results: smoke completion, HTTP 200 responses, speech timings of about 114 s and 0.65 s, and the "no ERROR records" claim. They rest on untracked `logs/` and `results/llm/` files.
2. Migration report: "Both inspected composites were 960 by 1896 pixels". The figure is arithmetically consistent with `stitcher.py` (24 + 2·(24+540) + (24+720) = 1896 for two 1920×1080 monitors and a 640×480 webcam), but the captures are private.
3. Fact-check report: the inventory of 1,699 response files and 1,198 JSONL records. The sums are internally consistent, but the files are untracked.
4. Fact-check report: rendering with Mermaid 11.12.0 and the initial 118-URL scan.
5. Fact-check report: the live smoke exit 0, three 960×1896 captures, and the nine exchanges.
6. Migration report: the red-run result (1 failure, 6 passes). The report itself says it was not re-established.
7. README: "ChatGPT subscriptions and API billing are managed separately" (help.openai.com/en/articles/9039756). The page returned HTTP 403.
8. GitHub and OpenCV doc links returned HTTP 403 through the proxy. I confirmed the openai-python v2.44.0 and werkzeug 3.1.8 tags and the python-mss repo exist via `git ls-remote`. I did not read the OpenCV pages.

## Problems found but not fixed

None in the repository.

Upstream note, not repo-fixable: OpenAI's text-to-speech guide says "11 built-in voices" in its intro but lists 13 in its voice section. The repo's "13 built-in voices" comment matches the list.

Link sweep: 142 unique base URLs. All returned 200 except loopback placeholders, a URL-prefix constant in `scripts/render_report.py`, and the 403s listed above.

## Hugging Face card

n/a. The repository references no Hugging Face model, dataset, or Space.

## Regenerated artifacts and tests

- I edited no report Markdown, so the PDFs did not need regenerating.
- `uv run --locked pytest -q`: 277 passed, both before and after the edits.
- `node --test tests/dashboard.test.cjs`: 12 of 12 passed.
- The only code change is a comment in `deepwork/config.py`.
