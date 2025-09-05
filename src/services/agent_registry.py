"""Agent registry utilities."""

from typing import Any, Dict, List


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
