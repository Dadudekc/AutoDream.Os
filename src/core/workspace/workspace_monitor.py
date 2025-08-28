"""Workspace monitoring utilities."""
from __future__ import annotations

from pathlib import Path
import logging
from typing import List

from .workspace_config import DEFAULT_WORKSPACE_DIR, MONITOR_INTERVAL_SECONDS

logger = logging.getLogger(__name__)


class WorkspaceMonitor:
    """Monitor workspace directories."""

    def __init__(
        self,
        base_dir: Path = DEFAULT_WORKSPACE_DIR,
        interval: int = MONITOR_INTERVAL_SECONDS,
    ) -> None:
        self.base_dir = Path(base_dir)
        self.interval = interval

    def list_workspaces(self) -> List[Path]:
        """Return existing workspace directories."""
        if not self.base_dir.exists():
            return []
        return [p for p in self.base_dir.iterdir() if p.is_dir()]
