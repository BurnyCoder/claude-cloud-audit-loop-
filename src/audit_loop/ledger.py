"""Append-only JSONL ledger: one line per audit event, used for round-robin and the summary.

Statuses: ``started`` when an audit is launched; then one of ``merged`` (PR merged),
``no_changes`` (nothing to fix), ``unmerged`` (pushed but left open), ``failed``.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

FINISHED = {"merged", "no_changes", "unmerged", "failed"}


def read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append(path: Path, **entry) -> dict:
    entry = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), **entry}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def finished_rounds(entries: list[dict]) -> dict[str, int]:
    """Highest finished round per repository."""
    done: dict[str, int] = {}
    for e in entries:
        if e.get("status") in FINISHED:
            done[e["repo"]] = max(done.get(e["repo"], 0), e["round"])
    return done


def running(entries: list[dict]) -> set[tuple[str, int]]:
    """(repo, round) pairs that were started and have not finished."""
    started = {(e["repo"], e["round"]) for e in entries if e.get("status") == "started"}
    return started - {(e["repo"], e["round"]) for e in entries if e.get("status") in FINISHED}


def next_audits(slugs: list[str], entries: list[dict], n: int) -> list[tuple[str, int]]:
    """Up to ``n`` (repo, round) pairs: least-audited repositories first, then list order.

    Repositories with an audit in flight are skipped, so every repository finishes round k
    before any starts round k + 1 (apart from in-flight overlap).
    """
    done, busy = finished_rounds(entries), {r for r, _ in running(entries)}
    idle = [s for s in slugs if s not in busy]
    idle.sort(key=lambda s: done.get(s, 0))  # stable sort keeps list order within a round
    return [(s, done.get(s, 0) + 1) for s in idle[:n]]
