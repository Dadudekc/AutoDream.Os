from typing import Any, Dict, List

AGENTS: Dict[str, Dict[str, Any]] = {
    "Agent-1": {
        "description": "Integration & Core Systems",
        "coords": {"x": -100, "y": 1000},
        "inbox": "agent_workspaces/Agent-1/inbox",
    },
    "Agent-2": {
        "description": "Architecture & Design",
        "coords": {"x": -200, "y": 1000},
        "inbox": "agent_workspaces/Agent-2/inbox",
    },
    "Agent-3": {
        "description": "Infrastructure & DevOps",
        "coords": {"x": -300, "y": 1000},
        "inbox": "agent_workspaces/Agent-3/inbox",
    },
    "Agent-4": {
        "description": "Strategic Oversight & Emergency Intervention",
        "coords": {"x": -400, "y": 1000},
        "inbox": "agent_workspaces/Agent-4/inbox",
    },
    "Agent-5": {
        "description": "Business Intelligence",
        "coords": {"x": -500, "y": 1000},
        "inbox": "agent_workspaces/Agent-5/inbox",
    },
    "Agent-6": {
        "description": "Coordination & Communication",
        "coords": {"x": -600, "y": 1000},
        "inbox": "agent_workspaces/Agent-6/inbox",
    },
    "Agent-7": {
        "description": "Web Development",
        "coords": {"x": -700, "y": 1000},
        "inbox": "agent_workspaces/Agent-7/inbox",
    },
    "Agent-8": {
        "description": "SSOT & System Integration",
        "coords": {"x": -800, "y": 1000},
        "inbox": "agent_workspaces/Agent-8/inbox",
    },
}


def list_agents() -> List[str]:
    """Return sorted list of agent identifiers."""
    return sorted(AGENTS.keys())
