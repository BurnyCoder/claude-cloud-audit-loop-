"""audit-loop: drive fact-check audits of many repositories from one Claude Code session.

The session itself is the orchestrator (see AGENTS.md). This package only keeps state and
measures spend: it prices the session's own transcripts, keeps a JSONL ledger, picks the next
repositories round-robin, clones them, renders the per-repository prompt and writes the summary.
"""
