"""Shared performance analysis utilities for agent monitoring."""
from typing import Iterable, Any, Dict

def analyze_agent_activity(records: Iterable[Any]) -> Dict[str, int]:
    """Calculate active agent count and total error occurrences.

    Args:
        records: Iterable of objects representing agent metrics or status.

    Returns:
        Dictionary with keys ``active_agents`` and ``total_errors``.
    """
    active_agents = 0
    total_errors = 0
    for record in records:
        if getattr(record, "status", None) == "active":
            active_agents += 1
        if hasattr(record, "error_count"):
            total_errors += getattr(record, "error_count", 0)
        elif hasattr(record, "errors"):
            errors = getattr(record, "errors", [])
            try:
                total_errors += len(errors)
            except TypeError:
                pass
    return {"active_agents": active_agents, "total_errors": total_errors}
