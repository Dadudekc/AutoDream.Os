"""Agent registry utilities."""

from typing import Any, Dict, List


COORDINATES: Dict[str, Dict[str, Any]] = {
    "Agent-1": {
        "x": -1269,
        "y": 481,
        "description": "Integration & Core Systems Specialist",
    },
    "Agent-2": {
        "x": -308,
        "y": 480,
        "description": "Architecture & Design Specialist",
    },
    "Agent-3": {
        "x": -1269,
        "y": 1001,
        "description": "Infrastructure & DevOps Specialist",
    },
    "Agent-4": {
        "x": -308,
        "y": 1000,
        "description": "Quality Assurance Specialist (CAPTAIN)",
    },
    "Agent-5": {
        "x": 652,
        "y": 421,
        "description": "Business Intelligence Specialist",
    },
    "Agent-6": {
        "x": 1612,
        "y": 419,
        "description": "Coordination & Communication Specialist",
    },
    "Agent-7": {
        "x": 653,
        "y": 940,
        "description": "Web Development Specialist",
    },
    "Agent-8": {
        "x": 1611,
        "y": 941,
        "description": "SSOT & System Integration Specialist",
    },
}


def format_agent_list(agents: List[str]) -> Dict[str, Any]:
    """Return standardized response data for a list of agents.

    Args:
        agents: List of agent identifiers.

    Returns:
        Dict[str, Any]: Standardized response object containing agent data.
    """
    sorted_agents = sorted(agents)
    return {
        "success": True,
        "message": f"Available agents: {', '.join(sorted_agents)}",
        "data": {"agents": sorted_agents, "agent_count": len(sorted_agents)},
    }
