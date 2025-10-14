"""
Tool Adapters Package
=====================

Base adapter infrastructure for Agent Toolbelt.

Author: Agent-7 - Repository Cloning Specialist
"""

from .base_adapter import IToolAdapter, ToolResult, ToolSpec
from .error_types import (
    ToolbeltError,
    ToolConfigurationError,
    ToolDependencyError,
    ToolExecutionError,
    ToolNotFoundError,
    ToolValidationError,
    format_toolbelt_error,
)

__all__ = [
    "IToolAdapter",
    "ToolResult",
    "ToolSpec",
    "ToolbeltError",
    "ToolNotFoundError",
    "ToolValidationError",
    "ToolExecutionError",
    "ToolDependencyError",
    "ToolConfigurationError",
    "format_toolbelt_error",
]
