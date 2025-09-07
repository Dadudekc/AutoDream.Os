"""Central agent registry and helpers."""

from typing import Any, Dict, List

AGENTS: Dict[str, Dict[str, Any]] = {
    "Agent-1": {
        "description": "Integration & Core Systems",
        "coords": (-1269, 481),
        "inbox": "agent_workspaces/Agent-1/inbox",
    },
    "Agent-2": {
        "description": "Architecture & Design",
        "coords": (-308, 480),
        "inbox": "agent_workspaces/Agent-2/inbox",
    },
    "Agent-3": {
        "description": "Infrastructure & DevOps",
        "coords": (-1269, 1001),
        "inbox": "agent_workspaces/Agent-3/inbox",
    },
    "Agent-4": {
        "description": "Strategic Oversight & Emergency Intervention",
        "coords": (-308, 1000),
        "inbox": "agent_workspaces/Agent-4/inbox",
    },
    "Agent-5": {
        "description": "Business Intelligence",
        "coords": (652, 421),
        "inbox": "agent_workspaces/Agent-5/inbox",
    },
    "Agent-6": {
        "description": "Coordination & Communication",
        "coords": (1612, 419),
        "inbox": "agent_workspaces/Agent-6/inbox",
    },
    "Agent-7": {
        "description": "Web Development",
        "coords": (653, 940),
        "inbox": "agent_workspaces/Agent-7/inbox",
    },
    "Agent-8": {
        "description": "SSOT & System Integration",
        "coords": (1611, 941),
        "inbox": "agent_workspaces/Agent-8/inbox",
    },
}

def list_agents() -> List[str]:
    """Return sorted list of agent identifiers."""
    return sorted(AGENTS.keys())


def format_agent_list(agents: List[str]) -> Dict[str, Any]:
    """Return standardized response data for a list of agents."""
    sorted_agents = sorted(agents)
    return {
        "success": True,
        "message": f"Available agents: {', '.join(sorted_agents)}",
        "data": {"agents": sorted_agents, "agent_count": len(sorted_agents)},
    }
