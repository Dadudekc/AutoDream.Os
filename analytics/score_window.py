"""
Score Window for Agent Efficiency
===============================

Scores agent performance windows and generates captain progress data.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

from .agent_metrics import DEFAULT_WEIGHTS, Weights, efficiency_score
from .window_loader import load_snapshots_from_window


def score_window(window_dir: str, weights: dict[str, float] | None = None) -> dict[str, Any]:
    """Score a time window and return team and individual agent scores."""
    snaps = load_snapshots_from_window(window_dir)
    w = DEFAULT_WEIGHTS if not weights else Weights(**{**DEFAULT_WEIGHTS.__dict__, **weights})
    results = {s.agent_id: efficiency_score(s, w) for s in snaps}
    team_score = round(
        sum(r["composite_0_100"] for r in results.values()) / max(1, len(results)), 2
    )
    return {"team_composite_0_100": team_score, "agents": results, "weights": w.__dict__}


def main():
    """Main CLI function for scoring windows."""
    import argparse

    ap = argparse.ArgumentParser(
        description="Score an agent window and emit captain_progress_data JSON."
    )
    ap.add_argument("--window", required=True, help="Path to window dir with agents/*.json")
    ap.add_argument("--out", default="captain_progress_data/latest_progress.json")
    ap.add_argument("--weights", help="JSON string to override weights", default=None)
    args = ap.parse_args()

    weights = json.loads(args.weights) if args.weights else None
    summary = score_window(args.window, weights)
    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(summary, indent=2))
    print(f"Wrote {outp}")


if __name__ == "__main__":
    main()
