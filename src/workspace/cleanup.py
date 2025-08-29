"""Workspace cleanup utilities."""

from __future__ import annotations

from pathlib import Path

from core.workspace_creator import WorkspaceStructureManager


def cleanup_workspace(base_dir: Path, name: str) -> bool:
    """Remove the workspace ``name`` under ``base_dir``.

    Returns
    -------
    bool
        ``True`` if the workspace was removed.
    """
    manager = WorkspaceStructureManager(base_dir)
    return manager.cleanup_workspace_structure(base_dir / name)


__all__ = ["cleanup_workspace"]
