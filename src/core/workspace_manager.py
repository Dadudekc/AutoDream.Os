from __future__ import annotations

from .workspace_config import (
    WorkspaceType,
    WorkspaceStatus,
    WorkspaceConfig,
    WorkspaceInfo,
    WorkspaceConfigManager,
)
from .workspace_creator import WorkspaceStructureManager
from .security.security_manager import (
    SecurityLevel,
    Permission,
    SecurityPolicy,
    AccessLog,
    WorkspaceSecurityManager,
)
from .workspace_coordinator import WorkspaceCoordinator, run_smoke_test

# Backwards compatibility alias
WorkspaceManager = WorkspaceCoordinator

__all__ = [
    "WorkspaceType",
    "WorkspaceStatus",
    "WorkspaceConfig",
    "WorkspaceInfo",
    "WorkspaceConfigManager",
    "WorkspaceStructureManager",
    "SecurityLevel",
    "Permission",
    "SecurityPolicy",
    "AccessLog",
    "WorkspaceSecurityManager",
    "WorkspaceCoordinator",
    "WorkspaceManager",
    "run_smoke_test",
]
