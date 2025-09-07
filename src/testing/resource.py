"""Resource orchestration helpers for test environment."""
from __future__ import annotations

from pathlib import Path

from .logging_utils import setup_logger


class ResourceOrchestrator:
    """Prepare and manage resources required for testing."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = Path(workspace)
        self.logger = setup_logger(__name__)

    def prepare(self) -> None:
        """Ensure the workspace directory exists."""
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.logger.info("Workspace %s prepared", self.workspace)
