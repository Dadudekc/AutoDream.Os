"""Compatibility wrapper for the unified workspace manager."""
from __future__ import annotations

from .unified_workspace_system import UnifiedWorkspaceSystem

# Re-export unified system under legacy name
WorkspaceCoordinator = UnifiedWorkspaceSystem


def run_smoke_test() -> bool:
    """Compatibility smoke test wrapper."""
    return UnifiedWorkspaceSystem().run_smoke_test()


__all__ = ["WorkspaceCoordinator", "run_smoke_test"]
