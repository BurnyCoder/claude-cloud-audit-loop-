"""Command line: ``audit-loop spend | next | clone | prompt | record | pr-body | report``.

Settings come from flags, then ``AUDIT_*`` environment variables, then ``.env`` in the current
directory (see .env.example). Paths are relative to the current directory.
"""

import argparse
import json
import os
import signal
import sys
from datetime import date, datetime, timezone
from importlib.resources import files
from pathlib import Path

from audit_loop import ledger, repos, report, spend

DEFAULTS = {
    "AUDIT_BUDGET_USD": "250", "AUDIT_STOP_MARGIN_USD": "12", "AUDIT_CAP_USD": "6",
    "AUDIT_REPOS_FILE": "repos.txt", "AUDIT_WORKDIR": "workdir", "AUDIT_REPORTS_DIR": "reports",
    "AUDIT_BRANCH_PREFIX": "fact-check", "AUDIT_PROMPT_FILE": "", "AUDIT_COMMIT_TRAILER": "", "AUDIT_PR_FOOTER": "", "AUDIT_STOP_AT": "",
}
EXIT_BUDGET = 3  # `spend --check` exit code once the stop line is reached


def settings() -> dict[str, str]:
    """DEFAULTS, overridden by ./.env, overridden by the environment."""
    conf = dict(DEFAULTS)
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.partition("=")
            if sep and key.strip().startswith("AUDIT_"):
                conf[key.strip()] = value.strip().strip("'\"")
    conf.update({k: v for k, v in os.environ.items() if k.startswith("AUDIT_")})
    return conf


def agent_name(slug: str, round_: int) -> str:
    """Agent tool description for an audit; `spend --agent` attributes cost by it."""
    return f"audit {slug.split('/')[1]} r{round_}"


def branch_name(conf: dict, round_: int) -> str:
    return f"{conf['AUDIT_BRANCH_PREFIX']}/{date.today().isoformat()}-r{round_}"


def session_id(args) -> str:
    sid = args.session or os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not sid:
        sys.exit("audit-loop: no session id; pass --session or run inside Claude Code")
    return sid


def cmd_spend(args, conf):
    s = spend.session_spend(session_id(args))
    stop_at = float(conf["AUDIT_BUDGET_USD"]) - float(conf["AUDIT_STOP_MARGIN_USD"])
    if args.agent:
        print(f"{sum(v for k, v in s['by_agent'].items() if k == args.agent):.2f}")
        return 0
    if args.total:
        print(f"{s['total']:.2f}")
    elif args.json:
        print(json.dumps({**s, "stop_at": stop_at}, indent=2))
    else:
        print(f"total ${s['total']:.2f} (main ${s['main']:.2f}) | stop line ${stop_at:.2f} | "
              f"left before stop ${stop_at - s['total']:.2f} | {s['files']} transcript files")
        for name, usd in sorted(s["by_agent"].items(), key=lambda kv: -kv[1]):
            print(f"  {usd:8.2f}  {name}")
    deadline = datetime.fromisoformat(conf["AUDIT_STOP_AT"]) if conf["AUDIT_STOP_AT"] else None
    if deadline and not args.agent and not args.total:
        print(f"deadline {deadline.isoformat()} ({'passed' if past(deadline) else 'not reached'})")
    return EXIT_BUDGET if args.check and (s["total"] >= stop_at or (deadline and past(deadline))) else 0


def past(deadline: datetime) -> bool:
    """True once ``deadline`` (naive values are read as UTC) has passed."""
    return datetime.now(timezone.utc) >= (deadline if deadline.tzinfo else deadline.replace(tzinfo=timezone.utc))


def cmd_next(args, conf):
    slugs = repos.parse_repos(Path(conf["AUDIT_REPOS_FILE"]).read_text(encoding="utf-8"))
    for slug, rnd in ledger.next_audits(slugs, ledger.read(ledger_path(conf)), args.n):
        print(slug, rnd)


def cmd_clone(args, conf):
    print(repos.clone(args.repo, Path(conf["AUDIT_WORKDIR"]).resolve(), branch_name(conf, args.round)))


def cmd_prompt(args, conf):
    template = Path(conf["AUDIT_PROMPT_FILE"]).read_text(encoding="utf-8") if conf["AUDIT_PROMPT_FILE"] \
        else files("audit_loop").joinpath("prompts/audit.md").read_text(encoding="utf-8")
    here, name = Path.cwd(), agent_name(args.repo, args.round)
    stop_at = float(conf["AUDIT_BUDGET_USD"]) - float(conf["AUDIT_STOP_MARGIN_USD"])
    print(template.format(
        slug=args.repo, round=args.round, branch=branch_name(conf, args.round),
        clone_dir=Path(conf["AUDIT_WORKDIR"]).resolve() / args.repo.split("/")[1],
        report_path=report.report_path(Path(conf["AUDIT_REPORTS_DIR"]).resolve(), args.repo, args.round),
        cap_usd=f"{args.cap or float(conf['AUDIT_CAP_USD']):.0f}", stop_total_usd=f"{stop_at:.0f}",
        spend_cmd=f'(cd {here} && uv run audit-loop spend --agent "{name}")',
        total_cmd=f"(cd {here} && uv run audit-loop spend --total)",
        commit_trailer=conf["AUDIT_COMMIT_TRAILER"].replace("\\n", "\n") or "(no trailer required)",
    ))


def cmd_record(args, conf):
    cost = args.cost
    if cost is None and args.status != "started":
        cost = round(spend.session_spend(session_id(args))["by_agent"].get(agent_name(args.repo, args.round), 0.0), 4)
    entry = {"repo": args.repo, "round": args.round, "status": args.status}
    entry |= {k: v for k, v in (("cost_usd", cost), ("pr", args.pr), ("note", args.note)) if v is not None}
    print(json.dumps(ledger.append(ledger_path(conf), **entry)))


def cmd_pr_body(args, conf):
    """PR description: the report's counts and Summary section, a link to the full report, a footer."""
    path = report.report_path(Path(conf["AUDIT_REPORTS_DIR"]), args.repo, args.round)
    meta, text = report.front_matter(path), path.read_text(encoding="utf-8")
    summary = text.split("## Summary", 1)[1].split("\n## ", 1)[0].strip() if "## Summary" in text else ""
    counts = ", ".join(f"{k.replace('_', ' ')}: {meta[k]}" for k in report.COUNTS if k in meta)
    remote = repos.git("remote", "get-url", "origin").removesuffix(".git")
    url = f"{remote}/blob/{repos.git('rev-parse', '--abbrev-ref', 'HEAD')}/{path.as_posix()}"
    print(f"Independent fact-check audit, round {args.round}.\n\n{summary}\n\n**Counts:** {counts}\n\n"
          f"Full report with every fix and its evidence: {url}\n\n"
          + conf["AUDIT_PR_FOOTER"].replace("\\n", "\n"))


def cmd_report(args, conf):
    reports_dir = Path(conf["AUDIT_REPORTS_DIR"])
    sid = args.session or os.environ.get("CLAUDE_CODE_SESSION_ID")
    text = report.summary(ledger.read(ledger_path(conf)), reports_dir,
                          spend.session_spend(sid) if sid else None, float(conf["AUDIT_BUDGET_USD"]))
    (reports_dir / "summary.md").write_text(text, encoding="utf-8")
    print(reports_dir / "summary.md")


def ledger_path(conf) -> Path:
    return Path(conf["AUDIT_REPORTS_DIR"]) / "ledger.jsonl"


def main(argv=None):
    if hasattr(signal, "SIGPIPE"):  # exit quietly when piped into head, as POSIX tools do
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    p = argparse.ArgumentParser(prog="audit-loop", description=__doc__.splitlines()[0])
    p.add_argument("--session", help="Claude Code session id (default: $CLAUDE_CODE_SESSION_ID)")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("spend", help="list-price spend of this session, from its transcripts")
    s.add_argument("--agent", help="print only this subagent description's spend")
    s.add_argument("--total", action="store_true", help="print only the session total")
    s.add_argument("--json", action="store_true")
    s.add_argument("--check", action="store_true", help=f"exit {EXIT_BUDGET} once total >= budget - margin or AUDIT_STOP_AT has passed")
    s = sub.add_parser("next", help="next repositories to audit, as 'owner/name round'")
    s.add_argument("-n", type=int, default=4)
    for name, helptext in (("clone", "clone/refresh a repo and check out its audit branch"),
                           ("prompt", "print the audit prompt for one repo"),
                           ("record", "append a ledger entry"),
                           ("pr-body", "print a PR description from the audit report")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("repo", help="owner/name")
        s.add_argument("--round", type=int, required=True)
        if name == "prompt":
            s.add_argument("--cap", type=float, help="soft USD cap for this audit (default AUDIT_CAP_USD)")
        if name == "record":
            s.add_argument("--status", required=True, choices=["started", *sorted(ledger.FINISHED)])
            s.add_argument("--cost", type=float, help="USD (default: this audit's subagent spend)")
            s.add_argument("--pr")
            s.add_argument("--note")
    sub.add_parser("report", help="write reports/summary.md")
    args = p.parse_args(argv)
    return globals()[f"cmd_{args.cmd.replace('-', '_')}"](args, settings()) or 0


if __name__ == "__main__":
    sys.exit(main())
