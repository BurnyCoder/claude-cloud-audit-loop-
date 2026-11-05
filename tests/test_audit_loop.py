"""Unit tests; expected dollar values are computed by hand from the price table in pricing.py."""

import json
import re

import pytest

from audit_loop import cli, ledger, report, repos, spend
from audit_loop.pricing import usage_cost


def test_opus_cost_splits_cache_writes_by_ttl_and_adds_searches():
    usage = {"input_tokens": 1000, "cache_read_input_tokens": 10_000, "output_tokens": 500,
             "cache_creation_input_tokens": 5000,
             "cache_creation": {"ephemeral_5m_input_tokens": 2000, "ephemeral_1h_input_tokens": 3000},
             "server_tool_use": {"web_search_requests": 2}}
    # 1000*4 + 2000*5 + 3000*8 + 10000*0.2 + 500*20 = 50,000 micro-dollars, plus 2 * $0.01
    assert usage_cost("claude-opus-5-5", usage) == pytest.approx(0.07)


def test_legacy_cache_writes_are_priced_as_5_minute():
    assert usage_cost("claude-opus-5-5", {"cache_creation_input_tokens": 1000}) == pytest.approx(0.005)


def test_haiku_long_prompt_tier_is_5x():
    assert usage_cost("claude-haiku-5-5", {"input_tokens": 150_000, "output_tokens": 1000}) == pytest.approx(0.0775)
    assert usage_cost("claude-haiku-5-5", {"input_tokens": 50_000}) == pytest.approx(0.005)


def test_unknown_model_falls_back_to_opus(capsys):
    assert usage_cost("claude-future-9", {"output_tokens": 1_000_000}) == pytest.approx(20.0)
    assert "no price" in capsys.readouterr().err


def _line(msg_id, model, **usage):
    return json.dumps({"type": "assistant", "message": {"id": msg_id, "model": model, "usage": usage}})


def test_session_spend_counts_each_message_once_and_attributes_subagents(tmp_path):
    proj = tmp_path / "projects" / "-some-project"
    (proj / "sid" / "subagents").mkdir(parents=True)
    (proj / "sid.jsonl").write_text("\n".join([
        _line("m1", "claude-opus-5-5", output_tokens=100),
        _line("m1", "claude-opus-5-5", output_tokens=1000),  # same response logged again: last line wins
        '{"type": "user"}', "{truncated",
    ]))
    agent = proj / "sid" / "subagents" / "agent-x.jsonl"
    agent.write_text(_line("m2", "claude-sonnet-5-5", output_tokens=1000))
    agent.with_name("agent-x.meta.json").write_text(json.dumps({"description": "audit repo r1"}))
    s = spend.session_spend("sid", tmp_path)
    assert s["main"] == pytest.approx(0.02)  # 1000 Opus output tokens
    assert s["by_agent"] == {"audit repo r1": pytest.approx(0.01)}  # 1000 Sonnet output tokens
    assert s["total"] == pytest.approx(0.03)


def test_parse_repos_accepts_urls_comments_and_drops_repeats():
    text = "https://github.com/a/b\n# comment\nc/d.e  # trailing\n\na/b\ngit@github.com:f/g.git\n"
    assert repos.parse_repos(text) == ["a/b", "c/d.e", "f/g"]
    with pytest.raises(ValueError):
        repos.parse_repos("not a repo")


def test_next_audits_round_robin_skips_running():
    entries = [{"repo": "o/a", "round": 1, "status": "started"}, {"repo": "o/a", "round": 1, "status": "merged"},
               {"repo": "o/b", "round": 1, "status": "started"}]
    assert ledger.next_audits(["o/a", "o/b", "o/c"], entries, 3) == [("o/c", 1), ("o/a", 2)]


def test_summary_reads_front_matter_and_ledger(tmp_path):
    path = report.report_path(tmp_path, "o/a", 1)
    path.parent.mkdir(parents=True)
    path.write_text("---\nrepo: o/a\nclaims_checked: 40\nfixed: 7\nunverifiable: 3\nnot_fixed: 1\n"
                    "hf_card_drift: yes\n---\n# body\n")
    entries = [{"repo": "o/a", "round": 1, "status": "started", "time": "t0"},
               {"repo": "o/a", "round": 1, "status": "merged", "cost_usd": 4.5, "pr": "https://x/pr/1", "time": "t1"}]
    text = report.summary(entries, tmp_path, {"total": 10.0, "main": 5.5}, 250)
    assert "| [o/a](https://github.com/o/a) | 1 | merged | 4.50 | 40 | 7 | 3 | 1 |" in text
    assert "claims_checked **40**" in text and "$10.00** of a $250.00 budget" in text
    assert "## Hugging Face cards" in text


def test_prompt_renders_every_placeholder(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AUDIT_COMMIT_TRAILER", "Trailer-A: 1\\nTrailer-B: 2")
    cli.main(["prompt", "owner/name", "--round", "2", "--cap", "5"])
    out = capsys.readouterr().out
    assert "owner/name" in out and "-r2" in out and "$5" in out and "Trailer-A: 1\nTrailer-B: 2" in out
    assert 'spend --agent "audit name r2"' in out and not re.search(r"\{[a-z_]+\}", out)


def test_spend_check_stops_after_deadline(tmp_path, monkeypatch):
    (tmp_path / "projects" / "p").mkdir(parents=True)
    (tmp_path / "projects" / "p" / "sid.jsonl").write_text("")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AUDIT_STOP_AT", "2000-01-01T00:00:00")
    assert cli.main(["--session", "sid", "spend", "--check"]) == cli.EXIT_BUDGET
    monkeypatch.setenv("AUDIT_STOP_AT", "2999-01-01T00:00:00+00:00")
    assert cli.main(["--session", "sid", "spend", "--check"]) == 0
