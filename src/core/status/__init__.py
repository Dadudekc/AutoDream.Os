#!/usr/bin/env python3
"""
Status Package - Agent Cellphone V2
===================================

CONSOLIDATED status system - single StatusManager replaces 7 separate files.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from ..managers.status_manager import StatusManager, run_smoke_test, main
from ..managers.status_registry import StatusRegistry
from ..managers.status_types import (
    StatusLevel,
    HealthStatus,
    UpdateFrequency,
    StatusEventType,
)
from ..managers.status_entities import (
    StatusItem,
    HealthMetric,
    ComponentHealth,
    StatusEvent,
    StatusMetrics,
    ActivitySummary,
)
from ..managers.status import StatusTracker, StatusBroadcaster, StatusStorage

# Backward compatibility
__all__ = [
    "StatusManager",
    "StatusRegistry",
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
    "StatusTracker",
    "StatusBroadcaster",
    "StatusStorage",
    "run_smoke_test",
    "main",
]
