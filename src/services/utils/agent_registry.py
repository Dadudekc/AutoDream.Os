"""Central agent registry providing a single source of truth."""

from typing import Any, Dict, List

AGENTS: Dict[str, Dict[str, Any]] = {
    "Agent-1": {
        "description": "Integration & Core Systems",
        "coords": {"x": -100, "y": 1000},
    },
    "Agent-2": {
        "description": "Architecture & Design",
        "coords": {"x": -200, "y": 1000},
    },
    "Agent-3": {
        "description": "Infrastructure & DevOps",
        "coords": {"x": -300, "y": 1000},
    },
    "Agent-4": {
        "description": "Strategic Oversight & Emergency Intervention",
        "coords": {"x": -400, "y": 1000},
    },
    "Agent-5": {
        "description": "Business Intelligence",
        "coords": {"x": -500, "y": 1000},
    },
    "Agent-6": {
        "description": "Coordination & Communication",
        "coords": {"x": -600, "y": 1000},
    },
    "Agent-7": {
        "description": "Web Development",
        "coords": {"x": -700, "y": 1000},
    },
    "Agent-8": {
        "description": "SSOT & System Integration",
        "coords": {"x": -800, "y": 1000},
    },
}


def list_agents() -> List[str]:
    """Return a sorted list of agent identifiers."""
    return sorted(AGENTS.keys())


__all__ = ["AGENTS", "list_agents"]
