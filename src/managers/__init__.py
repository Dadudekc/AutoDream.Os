"""Agent manager modules.

This package groups lightweight manager components responsible for
lifecycle control, coordination and metrics tracking for agents.
"""

from .lifecycle_manager import AgentLifecycleManager
from .coordination_manager import AgentCoordinator
from .metrics_manager import AgentMetricsManager
from .repo_manager import RepositoryManager

__all__ = [
    "AgentLifecycleManager",
    "AgentCoordinator",
    "AgentMetricsManager",
    "RepositoryManager",
]
