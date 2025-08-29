"""AI/ML subsystem interface definitions."""

from .agent import AgentManagerInterface
from .model import ModelManagerInterface
from .workflow import WorkflowManagerInterface
from .api_key import APIKeyManagerInterface
from .base import BaseManager  # legacy base interface

__all__ = [
    "AgentManagerInterface",
    "ModelManagerInterface",
    "WorkflowManagerInterface",
    "APIKeyManagerInterface",
    "BaseManager",
]
