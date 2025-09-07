"""Workspace synchronization helpers."""

from __future__ import annotations

from pathlib import Path

from core.workspace.workspace_synchronizer import WorkspaceSynchronizer


def sync_workspace(base_dir: Path) -> None:
    """Synchronize workspaces rooted at ``base_dir``."""
    synchronizer = WorkspaceSynchronizer(base_dir)
    synchronizer.sync()


__all__ = ["sync_workspace"]
