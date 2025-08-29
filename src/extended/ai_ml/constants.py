"""Shared constants for extended AI/ML managers."""

from typing import Final

DEFAULT_AI_MANAGER_CONFIG: Final[str] = "config/ai_ml/ai_manager.json"

WORKFLOW_STATUS_CREATED: Final[str] = "created"
WORKFLOW_STATUS_RUNNING: Final[str] = "running"
WORKFLOW_STATUS_COMPLETED: Final[str] = "completed"
WORKFLOW_STATUS_FAILED: Final[str] = "failed"
