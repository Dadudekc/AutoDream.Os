"""Backwards compatible workspace manager alias."""
from __future__ import annotations

from .unified_workspace_system import (
    UnifiedWorkspaceSystem,
    WorkspaceType,
    WorkspaceStatus,
    WorkspaceConfig,
    WorkspaceInfo,
    SecurityLevel,
    Permission,
    SecurityPolicy,
    AccessLog,
)

WorkspaceManager = UnifiedWorkspaceSystem
WorkspaceCoordinator = UnifiedWorkspaceSystem


def run_smoke_test() -> bool:
    """Compatibility wrapper for legacy smoke tests."""
    return UnifiedWorkspaceSystem().run_smoke_test()


__all__ = [
    "UnifiedWorkspaceSystem",
    "WorkspaceManager",
    "WorkspaceCoordinator",
    "WorkspaceType",
    "WorkspaceStatus",
    "WorkspaceConfig",
    "WorkspaceInfo",
    "SecurityLevel",
    "Permission",
    "SecurityPolicy",
    "AccessLog",
    "run_smoke_test",
]
