#!/usr/bin/env python3
"""
Status Package - Agent Cellphone V2
===================================

CONSOLIDATED status system - single StatusManager replaces 7 separate files.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from ..managers.status_manager import (
    StatusManager,
    StatusLevel,
    HealthStatus,
    UpdateFrequency,
    StatusEventType,
    StatusItem,
    HealthMetric,
    ComponentHealth,
    StatusEvent,
    StatusMetrics,
    ActivitySummary,
    run_smoke_test,
    main
)

# Backward compatibility
__all__ = [
    "StatusManager",
    "StatusLevel",
    "HealthStatus",
    "UpdateFrequency",
    "StatusEventType",
    "StatusItem",
    "HealthMetric",
    "ComponentHealth",
    "StatusEvent",
    "StatusMetrics",
    "ActivitySummary",
    "run_smoke_test",
    "main"
]
