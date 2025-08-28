#!/usr/bin/env python3
"""
Workspace Management Module - Agent Cellphone V2

Unified workspace management and coordination for Phase 2 integration.
Provides consolidated agent workspace management, coordination, and resource allocation.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3A - Workspace System Consolidation
V2 Standards: ≤200 LOC, SRP, OOP principles
"""

from .workspace_manager import UnifiedWorkspaceManager
from .workspace_orchestrator import WorkspaceCoordinationOrchestrator, CoordinationEvent
from .workspace_consolidation_orchestrator import (
    WorkspaceConsolidationOrchestrator,
    ConsolidationTask,
    WorkspaceConsolidationStatus,
)
from .workspace_resource_optimizer import (
    WorkspaceResourceOptimizer,
    ResourceAllocation,
    OptimizationResult,
    ResourceType,
    OptimizationStrategy,
)
from .workspace_health_monitor import (
    WorkspaceHealthMonitor,
    WorkspaceHealth,
    HealthCheckResult,
    HealthStatus,
    HealthCheckType,
)
from .unified_workspace_system import (
    UnifiedWorkspaceSystem,
    UnifiedWorkspaceSystemConfig,
    SystemStatus,
)
from .workspace_initializer import WorkspaceInitializer
from .workspace_synchronizer import WorkspaceSynchronizer
from .workspace_monitor import WorkspaceMonitor
from .workspace_config import (
    DEFAULT_WORKSPACE_DIR,
    SYNC_INTERVAL_SECONDS,
    MONITOR_INTERVAL_SECONDS,
)

__all__ = [
    # Core workspace management
    "UnifiedWorkspaceManager",
    "WorkspaceCoordinationOrchestrator",
    "CoordinationEvent",
    # Workspace consolidation
    "WorkspaceConsolidationOrchestrator",
    "ConsolidationTask",
    "WorkspaceConsolidationStatus",
    # Resource optimization
    "WorkspaceResourceOptimizer",
    "ResourceAllocation",
    "OptimizationResult",
    "ResourceType",
    "OptimizationStrategy",
    # Health monitoring
    "WorkspaceHealthMonitor",
    "WorkspaceHealth",
    "HealthCheckResult",
    "HealthStatus",
    "HealthCheckType",
    # Unified system
    "UnifiedWorkspaceSystem",
    "UnifiedWorkspaceSystemConfig",
    "SystemStatus",
    # Initialization and utilities
    "WorkspaceInitializer",
    "WorkspaceSynchronizer",
    "WorkspaceMonitor",
    "DEFAULT_WORKSPACE_DIR",
    "SYNC_INTERVAL_SECONDS",
    "MONITOR_INTERVAL_SECONDS",
]
