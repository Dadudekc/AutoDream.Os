#!/usr/bin/env python3
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse, json, sys, time

DATA = Path("data/knowledge")
DATA.mkdir(parents=True, exist_ok=True)

# ---------- core io ----------
def _append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def _iter_jsonl(path: Path):
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

# ---------- brain.* ----------
@dataclass
class BrainNote:
    ts: float
    content: str
    tags: list[str]
    pattern: str | None = None
    success_criteria: list[str] | None = None
    author: str = "Agent-7"

def brain_note(args):
    note = BrainNote(
        ts=time.time(),
        content=args.content,
        tags=args.tags or [],
        pattern=args.pattern,
        success_criteria=args.success or [],
        author=args.author,
    )
    _append_jsonl(DATA / "brain.notes.jsonl", asdict(note))
    print("OK: brain.note appended")

def brain_search(args):
    q = args.query.lower()
    res = []
    for obj in _iter_jsonl(DATA / "brain.notes.jsonl") or []:
        hay = json.dumps(obj).lower()
        if all(token in hay for token in q.split()):
            res.append(obj)
    print(json.dumps(res, indent=2))

def brain_share(args):
    entry = dict(ts=time.time(), topic=args.topic, recipients=args.recipients, actionable=args.actionable)
    _append_jsonl(DATA / "brain.shares.jsonl", entry)
    print("OK: brain.share recorded")

# ---------- oss.* (stubs; URLs tracked for later workers) ----------
def oss_clone(args):
    rec = dict(ts=time.time(), repo=args.repo, owner=args.owner)
    _append_jsonl(DATA / "oss.clone.jsonl", rec)
    print("OK: oss.clone queued")

def oss_issues(args):
    # placeholder query spec; real fetch lives in worker
    rec = dict(ts=time.time(), labels=args.labels, repo=args.repo)
    _append_jsonl(DATA / "oss.issues.query.jsonl", rec)
    print("OK: oss.issues query recorded")

def oss_import(args):
    rec = dict(ts=time.time(), assign_to=args.assign_to, source="oss.issues.result", count=args.count)
    _append_jsonl(DATA / "oss.import.jsonl", rec)
    print("OK: oss.import staged")

def oss_status(args):
    print(json.dumps({"agent": args.agent, "period": args.period, "status": "TBD"}, indent=2))

# ---------- debate.* ----------
def debate_start(args):
    rec = dict(ts=time.time(), topic=args.topic, participants=args.participants, duration_hours=args.duration)
    _append_jsonl(DATA / "debate.sessions.jsonl", rec)
    print("OK: debate.start created")

def debate_vote(args):
    rec = dict(ts=time.time(), topic=args.topic, voter=args.voter, choice=args.choice)
    _append_jsonl(DATA / "debate.votes.jsonl", rec)
    print("OK: vote recorded")

def debate_status(args):
    topic = args.topic
    votes = [v for v in (_iter_jsonl(DATA / "debate.votes.jsonl") or []) if v.get("topic") == topic]
    tallies = {}
    for v in votes:
        tallies[v["choice"]] = tallies.get(v["choice"], 0) + 1
    print(json.dumps({"topic": topic, "tally": tallies, "votes": len(votes)}, indent=2))

# ---------- msgtask.* ----------
def msgtask_ingest(args):
    rec = dict(ts=time.time(), source=args.source, text=args.text)
    _append_jsonl(DATA / "msgtask.inbox.jsonl", rec)
    print("OK: message ingested")

def msgtask_parse(args):
    # naive parse: split by lines; future replaces with NLP worker
    tasks = [ln.strip("-• ").strip() for ln in args.text.splitlines() if ln.strip()]
    rec = dict(ts=time.time(), tasks=tasks)
    _append_jsonl(DATA / "msgtask.parsed.jsonl", rec)
    print(json.dumps(rec, indent=2))

def msgtask_fingerprint(args):
    import hashlib
    fp = hashlib.sha256(args.text.encode("utf-8")).hexdigest()[:12]
    print(json.dumps({"fingerprint": fp}, indent=2))

# ---------- val.* (validation tools) ----------
def val_smoke(args):
    """Run smoke tests - simple placeholder for CLI."""
    system = args.system if hasattr(args, 'system') else 'all'
    rec = dict(ts=time.time(), system=system, test_type="smoke")
    _append_jsonl(DATA / "val.smoke.jsonl", rec)
    print(f"OK: smoke test queued for system={system}")

def val_flags(args):
    """Check/set feature flags."""
    action = args.action if hasattr(args, 'action') else 'check'
    rec = dict(ts=time.time(), action=action, flag=getattr(args, 'flag', None))
    _append_jsonl(DATA / "val.flags.jsonl", rec)
    print(f"OK: feature flag {action} recorded")

def val_rollback(args):
    """Rollback to previous version."""
    version = args.version if hasattr(args, 'version') else 'previous'
    rec = dict(ts=time.time(), target_version=version)
    _append_jsonl(DATA / "val.rollback.jsonl", rec)
    print(f"OK: rollback to {version} queued")

def val_report(args):
    """Generate validation report."""
    scope = args.scope if hasattr(args, 'scope') else 'all'
    rec = dict(ts=time.time(), scope=scope)
    _append_jsonl(DATA / "val.report.jsonl", rec)
    print(f"OK: validation report for {scope} queued")

# ---------- discord.* (Discord bot tools) - ADDED BY AGENT-8 ----------
def discord_health(args):
    """Check Discord bot health."""
    rec = dict(ts=time.time(), check_type="health")
    _append_jsonl(DATA / "discord.health.jsonl", rec)
    print("OK: Discord bot health check queued")

def discord_start(args):
    """Start Discord bot."""
    rec = dict(ts=time.time(), action="start")
    _append_jsonl(DATA / "discord.start.jsonl", rec)
    print("OK: Discord bot start command queued")

def discord_test(args):
    """Send Discord test message."""
    agent = args.agent if hasattr(args, 'agent') else 'Agent-1'
    message = args.message if hasattr(args, 'message') else 'Test message'
    rec = dict(ts=time.time(), agent=agent, message=message, test_type="message")
    _append_jsonl(DATA / "discord.test.jsonl", rec)
    print(f"OK: Discord test message to {agent} queued")

# ---------- infra.* (infrastructure tools) - ADDED BY AGENT-8 CYCLE 17 ----------
def infra_orchestrator_scan(args):
    """Scan all orchestrators for violations."""
    rec = dict(ts=time.time(), scan_type="orchestrator")
    _append_jsonl(DATA / "infra.orchestrator_scan.jsonl", rec)
    print("OK: Orchestrator scan queued")

def infra_file_lines(args):
    """Count lines in files for V2 compliance."""
    files = args.files if hasattr(args, 'files') else []
    rec = dict(ts=time.time(), files=files)
    _append_jsonl(DATA / "infra.file_lines.jsonl", rec)
    print(f"OK: Line count queued for {len(files)} file(s)")

def infra_extract_planner(args):
    """Plan module extraction for refactoring."""
    file_path = args.file if hasattr(args, 'file') else None
    rec = dict(ts=time.time(), file=file_path)
    _append_jsonl(DATA / "infra.extract_planner.jsonl", rec)
    print(f"OK: Extraction plan queued for {file_path}")

def infra_roi_calc(args):
    """Calculate ROI for tasks."""
    points = args.points if hasattr(args, 'points') else 500
    complexity = args.complexity if hasattr(args, 'complexity') else 10
    rec = dict(ts=time.time(), points=points, complexity=complexity)
    _append_jsonl(DATA / "infra.roi_calc.jsonl", rec)
    print(f"OK: ROI calculation queued (points={points}, complexity={complexity})")

# ---------- obs.* (observability tools) - ADDED BY AGENT-8 CYCLE 19 ----------
def obs_metrics(args):
    """Get current metrics snapshot."""
    rec = dict(ts=time.time(), action="snapshot")
    _append_jsonl(DATA / "obs.metrics.jsonl", rec)
    print("OK: Metrics snapshot queued")

def obs_get(args):
    """Get specific metric value."""
    key = args.key if hasattr(args, 'key') else None
    rec = dict(ts=time.time(), key=key)
    _append_jsonl(DATA / "obs.get.jsonl", rec)
    print(f"OK: Metric {key} retrieval queued")

def obs_health(args):
    """Check system health status."""
    rec = dict(ts=time.time(), check_type="health")
    _append_jsonl(DATA / "obs.health.jsonl", rec)
    print("OK: System health check queued")

def obs_slo(args):
    """Check SLO compliance."""
    metric = args.metric if hasattr(args, 'metric') else 'all'
    rec = dict(ts=time.time(), metric=metric)
    _append_jsonl(DATA / "obs.slo.jsonl", rec)
    print(f"OK: SLO check for {metric} queued")

# ---------- CLI wiring ----------
def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    # brain
    s = sub.add_parser("brain.note")
    s.add_argument("--content", required=True)
    s.add_argument("--tags", nargs="*", default=[])
    s.add_argument("--pattern")
    s.add_argument("--success", nargs="*", default=[])
    s.add_argument("--author", default="Agent-7")
    s.set_defaults(func=brain_note)

    s = sub.add_parser("brain.search")
    s.add_argument("--query", required=True)
    s.set_defaults(func=brain_search)

    s = sub.add_parser("brain.share")
    s.add_argument("--topic", required=True)
    s.add_argument("--recipients", nargs="*", default=["all-agents"])
    s.add_argument("--actionable", action="store_true")
    s.set_defaults(func=brain_share)

    # oss
    s = sub.add_parser("oss.clone"); s.add_argument("--repo", required=True); s.add_argument("--owner", default="Agent-7"); s.set_defaults(func=oss_clone)
    s = sub.add_parser("oss.issues"); s.add_argument("--repo", required=False, default="*"); s.add_argument("--labels", nargs="*", default=["good-first-issue"]); s.set_defaults(func=oss_issues)
    s = sub.add_parser("oss.import"); s.add_argument("--assign-to", dest="assign_to", default="Agent-7"); s.add_argument("--count", type=int, default=5); s.set_defaults(func=oss_import)
    s = sub.add_parser("oss.status"); s.add_argument("--agent", default="Agent-7"); s.add_argument("--period", default="weekly"); s.set_defaults(func=oss_status)

    # debate
    s = sub.add_parser("debate.start"); s.add_argument("--topic", required=True); s.add_argument("--participants", nargs="*", required=True); s.add_argument("--duration", type=int, default=24); s.set_defaults(func=debate_start)
    s = sub.add_parser("debate.vote"); s.add_argument("--topic", required=True); s.add_argument("--voter", required=True); s.add_argument("--choice", required=True); s.set_defaults(func=debate_vote)
    s = sub.add_parser("debate.status"); s.add_argument("--topic", required=True); s.set_defaults(func=debate_status)

    # msgtask
    s = sub.add_parser("msgtask.ingest"); s.add_argument("--source", required=True); s.add_argument("--text", required=True); s.set_defaults(func=msgtask_ingest)
    s = sub.add_parser("msgtask.parse"); s.add_argument("--text", required=True); s.set_defaults(func=msgtask_parse)
    s = sub.add_parser("msgtask.fingerprint"); s.add_argument("--text", required=True); s.set_defaults(func=msgtask_fingerprint)

    # val (validation tools) - ADDED BY AGENT-8
    s = sub.add_parser("val.smoke"); s.add_argument("--system", default="all"); s.set_defaults(func=val_smoke)
    s = sub.add_parser("val.flags"); s.add_argument("--action", default="check"); s.add_argument("--flag", default=None); s.set_defaults(func=val_flags)
    s = sub.add_parser("val.rollback"); s.add_argument("--version", default="previous"); s.set_defaults(func=val_rollback)
    s = sub.add_parser("val.report"); s.add_argument("--scope", default="all"); s.set_defaults(func=val_report)

    # discord (Discord bot tools) - ADDED BY AGENT-8 CYCLE 16
    s = sub.add_parser("discord.health"); s.set_defaults(func=discord_health)
    s = sub.add_parser("discord.start"); s.set_defaults(func=discord_start)
    s = sub.add_parser("discord.test"); s.add_argument("--agent", default="Agent-1"); s.add_argument("--message", default="Test message"); s.set_defaults(func=discord_test)

    # infra (infrastructure tools) - ADDED BY AGENT-8 CYCLE 17
    s = sub.add_parser("infra.orchestrator_scan"); s.set_defaults(func=infra_orchestrator_scan)
    s = sub.add_parser("infra.file_lines"); s.add_argument("--files", nargs="+", required=False, default=[]); s.set_defaults(func=infra_file_lines)
    s = sub.add_parser("infra.extract_planner"); s.add_argument("--file", required=False); s.set_defaults(func=infra_extract_planner)
    s = sub.add_parser("infra.roi_calc"); s.add_argument("--points", type=int, default=500); s.add_argument("--complexity", type=int, default=10); s.set_defaults(func=infra_roi_calc)

    # obs (observability tools) - ADDED BY AGENT-8 CYCLE 19
    s = sub.add_parser("obs.metrics"); s.set_defaults(func=obs_metrics)
    s = sub.add_parser("obs.get"); s.add_argument("--key", required=False); s.set_defaults(func=obs_get)
    s = sub.add_parser("obs.health"); s.set_defaults(func=obs_health)
    s = sub.add_parser("obs.slo"); s.add_argument("--metric", default="all"); s.set_defaults(func=obs_slo)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    sys.exit(main())
