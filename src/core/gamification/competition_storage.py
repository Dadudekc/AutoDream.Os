#!/usr/bin/env python3
"""
Competition Storage Helpers
============================

Storage and persistence helpers for the autonomous competition system.
Extracted from autonomous_competition_system.py for V2 compliance.

Author: Agent-6 (Quality Gates Specialist)
Purpose: V2 compliance refactoring (419→393 lines)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .autonomous_competition_system import AgentScore


def load_scores(storage_path: Path) -> dict[str, "AgentScore"]:
    """
    Load scores from storage.

    Args:
        storage_path: Path to storage directory

    Returns:
        Dictionary of agent_id to AgentScore
    """
    scores = {}
    scores_file = storage_path / "scores.json"

    if scores_file.exists():
        try:
            with open(scores_file) as f:
                data = json.load(f)
                # Reconstruct scores
                for agent_id, score_data in data.get("scores", {}).items():
                    scores[agent_id] = AgentScore(**score_data)
        except Exception:
            pass  # Start fresh if load fails

    return scores


def save_scores(storage_path: Path, scores: dict[str, "AgentScore"], mode_value: str) -> None:
    """
    Save scores to storage.

    Args:
        storage_path: Path to storage directory
        scores: Dictionary of agent_id to AgentScore
        mode_value: Competition mode value string
    """
    scores_file = storage_path / "scores.json"
    data = {
        "mode": mode_value,
        "last_updated": datetime.now().isoformat(),
        "scores": {
            agent_id: {
                "agent_id": score.agent_id,
                "agent_name": score.agent_name,
                "total_points": score.total_points,
                "rank": score.rank,
                "proactive_count": score.proactive_count,
                "quality_score": score.quality_score,
                "velocity_score": score.velocity_score,
                "collaboration_score": score.collaboration_score,
                "last_updated": score.last_updated,
            }
            for agent_id, score in scores.items()
        },
    }

    with open(scores_file, "w") as f:
        json.dump(data, f, indent=2)


def update_ranks(scores: dict[str, "AgentScore"]) -> None:
    """
    Update agent ranks based on total points (in-place).

    Args:
        scores: Dictionary of agent_id to AgentScore (modified in-place)
    """
    sorted_agents = sorted(scores.values(), key=lambda x: x.total_points, reverse=True)

    for rank, agent_score in enumerate(sorted_agents, start=1):
        agent_score.rank = rank
