"""Agent metrics collection helpers."""

from __future__ import annotations

from typing import Any, Dict

from .lifecycle import LifecycleManager


def collect_metrics(lifecycle: LifecycleManager) -> Dict[str, Any]:
    """Return basic metrics for currently registered agents."""
    agents = lifecycle.all()
    return {
        "total_agents": len(agents),
        "agent_ids": list(agents.keys()),
    }
