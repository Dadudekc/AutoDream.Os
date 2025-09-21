"""
Signal harvester for CI artifacts (coverage, test results, lint).
Drop JSON files per-agent under a window dir so score_window can ingest.
"""

from __future__ import annotations
import json
import pathlib
import re
from typing import Dict, Any
from analytics.agent_metrics import parse_cobertura_coverage

def parse_pytest_summary(txt: str) -> Dict[str, int]:
    """Parse pytest summary text to extract test counts."""
    # naive regex; adjust to your CI output
    m = re.search(r"(?P<passed>\d+) passed.*?(?P<failed>\d+) failed.*?(?P<skipped>\d+) skipped", txt, re.I|re.S)
    if not m:
        return {"passed": 0, "failed": 0, "skipped": 0, "total": 0}
    d = {k: int(v) for k, v in m.groupdict().items()}
    d["total"] = d["passed"] + d["failed"] + d["skipped"]
    return d

def collect(window_dir: str, agent_id: str, coverage_xml: str, pytest_txt: str, extra: Dict[str, Any] | None = None):
    """Collect CI signals and save agent snapshot."""
    cov = parse_cobertura_coverage(coverage_xml)
    summary_txt = pathlib.Path(pytest_txt).read_text() if pathlib.Path(pytest_txt).exists() else ""
    t = parse_pytest_summary(summary_txt)
    payload = {
        "agent_id": agent_id,
        "tasks_assigned": 0,
        "tasks_completed": 0,
        "tasks_on_time": 0,
        "tasks_reworked": 0,
        "incidents": 0,
        "prs_merged": 0,
        "loc_touched": 0,
        "wall_secs_active": 0,
        "unit_tests_failed": t.get("failed", 0),
        "unit_tests_total": t.get("total", 0),
        "coverage_pct": cov,
    }
    if extra:
        payload.update(extra)

    out_dir = pathlib.Path(window_dir) / "agents"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{agent_id}.json").write_text(json.dumps(payload, indent=2))
    return payload

if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", required=True)
    ap.add_argument("--agent", required=True)
    ap.add_argument("--coverage-xml", default="coverage.xml")
    ap.add_argument("--pytest-summary", default=".pytest_summary.txt")
    ap.add_argument("--extra", help="JSON of additional fields", default=None)
    args = ap.parse_args()
    extra = json.loads(args.extra) if args.extra else None
    p = collect(args.window, args.agent, args.coverage_xml, args.pytest_summary, extra)
    print(json.dumps(p, indent=2))
