"""Workspace creation helpers."""

from __future__ import annotations

from pathlib import Path

from core.workspace_creator import WorkspaceStructureManager
from core.workspace_config import WorkspaceType


def create_workspace(
    base_dir: Path, name: str, workspace_type: WorkspaceType = WorkspaceType.AGENT
) -> Path:
    """Create a workspace directory structure.

    Parameters
    ----------
    base_dir:
        Base directory under which the workspace will be created.
    name:
        Name of the workspace directory.
    workspace_type:
        Type of workspace; defaults to ``WorkspaceType.AGENT``.

    Returns
    -------
    Path
        Path to the newly created workspace.
    """

    manager = WorkspaceStructureManager(base_dir)
    workspace_path = base_dir / name
    if not manager.create_workspace_structure(workspace_path, workspace_type):
        raise RuntimeError(f"Failed to create workspace: {name}")
    return workspace_path


__all__ = ["create_workspace"]
