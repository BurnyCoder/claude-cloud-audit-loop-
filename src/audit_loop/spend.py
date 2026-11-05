"""Spend of the running Claude Code session, priced from its own transcripts.

Claude Code appends every API response, with its ``usage`` block, to
``<config dir>/projects/<project>/<session id>.jsonl``; subagents get
``<session id>/subagents/agent-<id>.jsonl`` plus ``agent-<id>.meta.json``, whose ``description``
is the Agent tool's description (https://code.claude.com/docs/en/sessions). One response can be
logged on several lines with the same message id, so each id is counted once (last line wins).
Same idea as BurnyCoder/claude-agent-sdk-audit-loop (session.py, transcript_cost).
"""

import json
import os
from pathlib import Path

from audit_loop.pricing import usage_cost


def config_dir() -> Path:
    """Claude Code's config directory: $CLAUDE_CONFIG_DIR, else ~/.claude."""
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def session_files(session_id: str, root: Path | None = None) -> tuple[list[Path], list[Path]]:
    """(main transcripts, subagent transcripts) of one session, across all project folders."""
    projects = (root or config_dir()) / "projects"
    main = sorted(projects.glob(f"*/{session_id}.jsonl"))
    subagents = sorted(p for d in projects.glob(f"*/{session_id}/subagents") for p in d.rglob("*.jsonl"))
    return main, subagents


def file_cost(path: Path) -> float:
    """List-price USD of every distinct API response recorded in one transcript file."""
    last: dict[str, tuple[str, dict]] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue  # a line being written right now can be incomplete
        msg = entry.get("message") if isinstance(entry, dict) and entry.get("type") == "assistant" else None
        if isinstance(msg, dict) and msg.get("id") and isinstance(msg.get("usage"), dict):
            last[msg["id"]] = (msg.get("model") or "", msg["usage"])
    return sum(usage_cost(model, usage) for model, usage in last.values())


def agent_description(path: Path) -> str:
    """The Agent tool description stored next to a subagent transcript, or its file stem."""
    meta = path.with_name(path.name.removesuffix(".jsonl") + ".meta.json")
    try:
        return json.loads(meta.read_text(encoding="utf-8")).get("description") or path.stem
    except (OSError, ValueError):
        return path.stem


def session_spend(session_id: str, root: Path | None = None) -> dict:
    """Total USD, the main thread's share, and USD per subagent description."""
    main, subagents = session_files(session_id, root)
    by_agent: dict[str, float] = {}
    for path in subagents:
        name = agent_description(path)
        by_agent[name] = by_agent.get(name, 0.0) + file_cost(path)
    main_usd = sum(file_cost(p) for p in main)
    return {"total": main_usd + sum(by_agent.values()), "main": main_usd, "by_agent": by_agent,
            "files": len(main) + len(subagents)}
