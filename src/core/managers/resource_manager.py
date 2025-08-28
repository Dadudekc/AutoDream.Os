#!/usr/bin/env python3
"""Resource management module for workspace coordination."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .manager_utils import current_timestamp, ensure_directory


@dataclass
class WorkspaceInfo:
    """Information about a workspace."""

    workspace_id: str
    name: str
    path: str
    agent_id: Optional[str]
    status: str
    created_at: str
    last_accessed: str
    size_bytes: int
    file_count: int


class ResourceManager:
    """Manage creation and assignment of workspaces."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__ + ".ResourceManager")
        self.workspaces: Dict[str, WorkspaceInfo] = {}

    # ------------------------------------------------------------------
    # Workspace lifecycle
    # ------------------------------------------------------------------
    def create_workspace(
        self, workspace_id: str, name: str, path: str, agent_id: Optional[str] = None
    ) -> bool:
        """Create a new workspace on disk."""
        try:
            workspace_path = ensure_directory(path)
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to ensure directory %s: %s", path, exc)
            return False

        info = WorkspaceInfo(
            workspace_id=workspace_id,
            name=name,
            path=str(workspace_path),
            agent_id=agent_id,
            status="active",
            created_at=current_timestamp(),
            last_accessed=current_timestamp(),
            size_bytes=0,
            file_count=0,
        )
        self.workspaces[workspace_id] = info
        return True

    def delete_workspace(self, workspace_id: str) -> bool:
        """Delete an existing workspace."""
        info = self.workspaces.pop(workspace_id, None)
        if not info:
            return False
        path = Path(info.path)
        if path.exists():
            import shutil
            shutil.rmtree(path)
        return True

    # ------------------------------------------------------------------
    # Workspace queries
    # ------------------------------------------------------------------
    def get_workspace(self, workspace_id: str) -> Optional[WorkspaceInfo]:
        """Return information about a specific workspace."""
        return self.workspaces.get(workspace_id)

    def get_all_workspaces(self) -> List[WorkspaceInfo]:
        """Return all known workspaces."""
        return list(self.workspaces.values())

    def get_workspaces_by_agent(self, agent_id: str) -> List[WorkspaceInfo]:
        """Return workspaces assigned to a particular agent."""
        return [w for w in self.workspaces.values() if w.agent_id == agent_id]

    def assign_workspace(self, workspace_id: str, agent_id: str) -> bool:
        """Assign a workspace to an agent."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace:
            return False
        workspace.agent_id = agent_id
        workspace.last_accessed = current_timestamp()
        return True

    # ------------------------------------------------------------------
    # Summary statistics
    # ------------------------------------------------------------------
    def get_summary(self) -> Dict[str, Any]:
        """Return aggregate statistics about all workspaces."""
        return {
            "total_workspaces": len(self.workspaces),
            "by_status": {
                status: len([w for w in self.workspaces.values() if w.status == status])
                for status in {w.status for w in self.workspaces.values()}
            },
            "assigned_workspaces": len([w for w in self.workspaces.values() if w.agent_id]),
            "unassigned_workspaces": len([w for w in self.workspaces.values() if not w.agent_id]),
            "total_size": sum(w.size_bytes for w in self.workspaces.values()),
            "total_files": sum(w.file_count for w in self.workspaces.values()),
        }
