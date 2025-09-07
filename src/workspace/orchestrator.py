"""High-level workspace orchestration APIs."""

from __future__ import annotations

from pathlib import Path

from core.workspace_config import WorkspaceType

from .creation import create_workspace
from .sync import sync_workspace
from .cleanup import cleanup_workspace


class WorkspaceOrchestrator:
    """Expose high-level workspace management operations."""

    def __init__(self, base_dir: Path = Path("agent_workspaces")) -> None:
        self.base_dir = Path(base_dir)

    def create(
        self, name: str, workspace_type: WorkspaceType = WorkspaceType.AGENT
    ) -> Path:
        """Create a new workspace."""
        return create_workspace(self.base_dir, name, workspace_type)

    def sync(self) -> None:
        """Synchronize all workspaces."""
        sync_workspace(self.base_dir)

    def cleanup(self, name: str) -> bool:
        """Remove a workspace and its contents."""
        return cleanup_workspace(self.base_dir, name)


__all__ = ["WorkspaceOrchestrator"]
