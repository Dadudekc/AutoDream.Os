"""Agent registry utilities."""

from typing import Any, Dict, List

AGENTS: Dict[str, Dict[str, Any]] = {
    "Agent-1": {
        "description": "Integration & Core Systems Specialist",
        "coords": {"x": 100, "y": 100},
    },
    "Agent-2": {
        "description": "Architecture & Design Specialist",
        "coords": {"x": 200, "y": 100},
    },
    "Agent-3": {
        "description": "Infrastructure & DevOps Specialist",
        "coords": {"x": 300, "y": 100},
    },
    "Agent-4": {
        "description": "Strategic Oversight & Emergency Intervention Manager (CAPTAIN)",
        "coords": {"x": 400, "y": 100},
    },
    "Agent-5": {
        "description": "Business Intelligence Specialist",
        "coords": {"x": 100, "y": 200},
    },
    "Agent-6": {
        "description": "Coordination & Communication Specialist",
        "coords": {"x": 200, "y": 200},
    },
    "Agent-7": {
        "description": "Web Development Specialist",
        "coords": {"x": 300, "y": 200},
    },
    "Agent-8": {
        "description": "SSOT & System Integration Specialist",
        "coords": {"x": 400, "y": 200},
    },
}


def list_agents() -> List[str]:
    """Return a sorted list of agent identifiers."""
    return sorted(AGENTS.keys())
