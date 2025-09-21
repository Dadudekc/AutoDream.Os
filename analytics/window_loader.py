"""
Window Loader for Agent Snapshots
================================

Loads agent performance snapshots from time windows.
"""

from __future__ import annotations
import json
import pathlib
import datetime as dt
from typing import Dict, Any, List
from .agent_metrics import AgentSnapshot

def load_snapshots_from_window(window_dir: str) -> List[AgentSnapshot]:
    """
    Expect JSON blobs per agent under {window_dir}/agents/*.json with fields matching AgentSnapshot.
    Falls back intelligently when fields are missing.
    """
    root = pathlib.Path(window_dir)
    out: List[AgentSnapshot] = []
    
    agents_dir = root / "agents"
    if not agents_dir.exists():
        return out
    
    for p in agents_dir.glob("*.json"):
        try:
            data = json.loads(p.read_text())
            out.append(AgentSnapshot(
                agent_id=data["agent_id"],
                tasks_assigned=data.get("tasks_assigned", 0),
                tasks_completed=data.get("tasks_completed", 0),
                tasks_on_time=data.get("tasks_on_time", 0),
                tasks_reworked=data.get("tasks_reworked", 0),
                incidents=data.get("incidents", 0),
                prs_merged=data.get("prs_merged", 0),
                loc_touched=data.get("loc_touched", 0),
                wall_secs_active=float(data.get("wall_secs_active", 0)),
                unit_tests_failed=data.get("unit_tests_failed", 0),
                unit_tests_total=data.get("unit_tests_total", 0),
                coverage_pct=float(data.get("coverage_pct", 0.0)),
                complexity_avg=data.get("complexity_avg"),
                review_findings=data.get("review_findings", 0),
                window_start=dt.datetime.fromisoformat(data["window_start"]) if data.get("window_start") else None,
                window_end=dt.datetime.fromisoformat(data["window_end"]) if data.get("window_end") else None,
            ))
        except Exception as e:
            print(f"Warning: Could not load snapshot from {p}: {e}")
    
    return out
