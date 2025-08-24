"""Configuration utilities for the development workflow."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any

from .api_key_manager import get_openai_api_key, get_anthropic_api_key
from .utils import get_config_manager


@dataclass
class WorkflowConfig:
    """Runtime configuration for AI development workflows."""

    project_path: Path
    openai_key: Optional[str]
    anthropic_key: Optional[str]
    config_manager: Any


def load_workflow_config(project_path: str = ".") -> WorkflowConfig:
    """Load workflow configuration from environment and defaults."""
    return WorkflowConfig(
        project_path=Path(project_path),
        openai_key=get_openai_api_key(),
        anthropic_key=get_anthropic_api_key(),
        config_manager=get_config_manager(),
    )
