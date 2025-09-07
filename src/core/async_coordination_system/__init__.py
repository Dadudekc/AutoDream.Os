#!/usr/bin/env python3
"""
Asynchronous Coordination System Package
======================================

Modularized async coordination system package.

**Author:** Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
**Contract:** COORD-012 - Advanced Coordination Protocol Implementation
**Status:** MODULARIZED
**Target:** <50ms coordination latency (4x improvement)
"""

from .models import (
    CoordinationTaskType,
    TaskPriority,
    CoordinationState,
    CoordinationTask,
    CoordinationGroup,
    CoordinationMetrics,
    CoordinatorConfig,
    TaskExecutionResult,
    SystemPerformance
)

from .coordinator import AsyncCoordinator
from .protocol import AsyncCoordinationProtocol

__version__ = "2.0.0"
__author__ = "Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)"
__status__ = "MODULARIZED"

__all__ = [
    'CoordinationTaskType',
    'TaskPriority',
    'CoordinationState',
    'CoordinationTask',
    'CoordinationGroup',
    'CoordinationMetrics',
    'CoordinatorConfig',
    'TaskExecutionResult',
    'SystemPerformance',
    'AsyncCoordinator',
    'AsyncCoordinationProtocol'
]
