from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


class WorkspaceType(Enum):
    """Types of agent workspaces."""

    AGENT = "agent"
    COORDINATION = "coordination"
    SHARED = "shared"
    ISOLATED = "isolated"
    TEMPORARY = "temporary"


class WorkspaceStatus(Enum):
    """Workspace lifecycle states."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ARCHIVED = "archived"
    ERROR = "error"


@dataclass
class WorkspaceConfig:
    """Configuration persisted for a workspace."""

    name: str
    workspace_type: WorkspaceType
    base_path: str
    permissions: List[str]
    isolation_level: str
    max_size_mb: int
    auto_cleanup: bool
    backup_enabled: bool


@dataclass
class WorkspaceInfo:
    """Runtime information about a workspace."""

    name: str
    workspace_type: WorkspaceType
    status: WorkspaceStatus
    path: str
    size_mb: float
    created_at: str
    last_accessed: str
    agent_count: int
    resource_usage: Dict[str, Any]
    # Agent specific paths for backwards compatibility
    inbox_path: Optional[str] = None
    tasks_path: Optional[str] = None
    responses_path: Optional[str] = None
    agent_id: Optional[str] = None


class WorkspaceConfigManager:
    """Handles persistence of workspace configuration."""

    def __init__(self, base_workspace_dir: Path):
        self.base_workspace_dir = base_workspace_dir
        self.logger = logging.getLogger(f"{__name__}.WorkspaceConfigManager")

    def save_workspace_config(self, name: str, config: WorkspaceConfig) -> bool:
        """Persist workspace configuration to disk."""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            with open(config_file, "w") as f:
                json.dump(asdict(config), f, indent=2, default=str)
            return True
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to save workspace config for {name}: {e}")
            return False

    def load_workspace_config(self, name: str) -> Optional[WorkspaceConfig]:
        """Load configuration from disk if available."""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    data = json.load(f)
                data["workspace_type"] = WorkspaceType(data["workspace_type"])
                return WorkspaceConfig(**data)
            return None
        except Exception as e:  # pragma: no cover - logging protection
            self.logger.error(f"Failed to load workspace config for {name}: {e}")
            return None

    @staticmethod
    def get_current_timestamp() -> str:
        """Return current timestamp string."""
        from datetime import datetime

        return datetime.now().isoformat()


__all__ = [
    "WorkspaceType",
    "WorkspaceStatus",
    "WorkspaceConfig",
    "WorkspaceInfo",
    "WorkspaceConfigManager",
]
