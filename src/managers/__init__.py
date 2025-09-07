"""Agent manager modules.

This package groups lightweight manager components responsible for
lifecycle control, coordination and repository management for agents.
"""

from .lifecycle_manager import AgentLifecycleManager
from .coordination_manager import AgentCoordinator
from .repo_manager import RepositoryManager

__all__ = [
    "AgentLifecycleManager",
    "AgentCoordinator",
    "RepositoryManager",
]
