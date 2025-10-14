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

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    sys.exit(main())
