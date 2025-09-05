"""Agent registry utilities."""

from typing import Any, Dict, List

AGENTS: Dict[str, Dict[str, Any]] = {
    "Agent-1": {
        "description": "Integration & Core Systems Specialist",
        "coords": {"x": -1269, "y": 481},
    },
    "Agent-2": {
        "description": "Architecture & Design Specialist",
        "coords": {"x": -308, "y": 480},
    },
    "Agent-3": {
        "description": "Infrastructure & DevOps Specialist",
        "coords": {"x": -1269, "y": 1001},
    },
    "Agent-4": {
        "description": "Quality Assurance Specialist (CAPTAIN)",
        "coords": {"x": -308, "y": 1000},
    },
    "Agent-5": {
        "description": "Business Intelligence Specialist",
        "coords": {"x": 652, "y": 421},
    },
    "Agent-6": {
        "description": "Coordination & Communication Specialist",
        "coords": {"x": 1612, "y": 419},
    },
    "Agent-7": {
        "description": "Web Development Specialist",
        "coords": {"x": 653, "y": 940},
    },
    "Agent-8": {
        "description": "SSOT & System Integration Specialist",
        "coords": {"x": 1611, "y": 941},
    },
}


def list_agents() -> List[str]:
    """Return a sorted list of agent identifiers."""
    return sorted(AGENTS.keys())
