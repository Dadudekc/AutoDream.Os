#!/usr/bin/env python3
"""
Workspace Configuration Module - V2 Workspace Configuration Components

This module manages workspace configuration and related data structures.
Follows Single Responsibility Principle - only workspace configuration.
Architecture: Single Responsibility Principle - workspace configuration only
LOC: Target 100 lines (under 200 limit)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class WorkspaceType(Enum):
    """Types of agent workspaces"""

    AGENT = "agent"
    COORDINATION = "coordination"
    SHARED = "shared"
    ISOLATED = "isolated"
    TEMPORARY = "temporary"


class WorkspaceStatus(Enum):
    """Workspace status states"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ARCHIVED = "archived"
    ERROR = "error"


@dataclass
class WorkspaceConfig:
    """Configuration for a workspace"""

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
    """Information about a workspace"""

    name: str
    workspace_type: WorkspaceType
    status: WorkspaceStatus
    path: str
    size_mb: float
    created_at: str
    last_accessed: str
    agent_count: int
    resource_usage: Dict[str, Any]


class WorkspaceConfigManager:
    """Manages workspace configuration operations"""

    def __init__(self, base_workspace_dir: Path):
        self.base_workspace_dir = base_workspace_dir
        self.logger = logging.getLogger(f"{__name__}.WorkspaceConfigManager")

    def save_workspace_config(self, name: str, config: WorkspaceConfig) -> bool:
        """Save workspace configuration to file"""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            with open(config_file, "w") as f:
                json.dump(asdict(config), f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save workspace config for {name}: {e}")
            return False

    def load_workspace_config(self, name: str) -> Optional[WorkspaceConfig]:
        """Load workspace configuration from file"""
        try:
            config_file = self.base_workspace_dir / name / "workspace_config.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    data = json.load(f)
                    return WorkspaceConfig(**data)
            return None
        except Exception as e:
            self.logger.error(f"Failed to load workspace config for {name}: {e}")
            return None

    def get_current_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime

        return datetime.now().isoformat()


def run_smoke_test():
    """Run basic functionality test for WorkspaceConfig"""
    print("🧪 Running WorkspaceConfig Smoke Test...")

    try:
        # Test enum values
        assert WorkspaceType.AGENT.value == "agent"
        assert WorkspaceStatus.ACTIVE.value == "active"

        # Test dataclass creation
        config = WorkspaceConfig(
            name="test",
            workspace_type=WorkspaceType.AGENT,
            base_path="/test",
            permissions=["read", "write"],
            isolation_level="standard",
            max_size_mb=100,
            auto_cleanup=True,
            backup_enabled=True,
        )
        assert config.name == "test"

        print("✅ WorkspaceConfig Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ WorkspaceConfig Smoke Test FAILED: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
