"""Workspace initialization utilities."""
from __future__ import annotations

from pathlib import Path
import logging

from .workspace_config import DEFAULT_WORKSPACE_DIR

logger = logging.getLogger(__name__)


class WorkspaceInitializer:
    """Create and prepare workspace directories."""

    def __init__(self, base_dir: Path = DEFAULT_WORKSPACE_DIR) -> None:
        self.base_dir = Path(base_dir)

    def initialize(self) -> Path:
        """Ensure the base workspace directory exists."""
        self.base_dir.mkdir(exist_ok=True)
        logger.info("Workspace initialized at %s", self.base_dir)
        return self.base_dir
