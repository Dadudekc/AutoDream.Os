from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from .workspace_config import WorkspaceType


class WorkspaceStructureManager:
    """Manages creation and cleanup of workspace directories."""

    def __init__(self, base_workspace_dir: Path):
        self.base_workspace_dir = base_workspace_dir
        self.logger = logging.getLogger(f"{__name__}.WorkspaceStructureManager")

    def create_workspace_structure(
        self, workspace_path: Path, workspace_type: WorkspaceType
    ) -> bool:
        """Create directory layout for a workspace."""
        try:
            common_dirs = ["data", "logs", "temp", "backups"]
            if workspace_type == WorkspaceType.AGENT:
                type_dirs = [
                    "personal",
                    "shared",
                    "work",
                    "archive",
                    "inbox",
                    "tasks",
                    "responses",
                ]
            elif workspace_type == WorkspaceType.COORDINATION:
                type_dirs = ["coordination", "shared", "monitoring", "reports"]
            elif workspace_type == WorkspaceType.SHARED:
                type_dirs = ["public", "restricted", "templates", "examples"]
            else:
                type_dirs = ["general"]

            for dir_name in common_dirs + type_dirs:
                (workspace_path / dir_name).mkdir(exist_ok=True)

            readme_content = (
                f"# {workspace_path.name} Workspace\n\n"
                f"Type: {workspace_type.value}\n"
                f"Created: {self._get_current_timestamp()}\n"
            )
            with open(workspace_path / "README.md", "w") as f:
                f.write(readme_content)

            return True
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to create workspace structure: {e}")
            return False

    def cleanup_workspace_structure(self, workspace_path: Path) -> bool:
        """Remove a workspace directory tree."""
        try:
            if workspace_path.exists():
                import shutil

                shutil.rmtree(workspace_path)
                return True
            return False
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to cleanup workspace structure: {e}")
            return False

    @staticmethod
    def _get_current_timestamp() -> str:
        from datetime import datetime

        return datetime.now().isoformat()


__all__ = ["WorkspaceStructureManager"]
