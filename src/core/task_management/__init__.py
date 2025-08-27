#!/usr/bin/env python3
"""
Advanced Task Management System - UNIFIED VERSION
================================================

This module provides enterprise-grade task management capabilities including:
- Task definition and types
- Priority-based scheduling
- Dependency resolution
- Resource allocation
- Performance monitoring

CONSOLIDATED FROM 6 FRAGMENTED FILES INTO UNIFIED SYSTEM
"""

from .unified_scheduler import (
    # Main scheduler class
    UnifiedTaskScheduler,
    TaskScheduler,
    # Task types and enums
    Task,
    TaskPriority,
    TaskStatus,
    TaskType,
    TaskCategory,
    TaskDependency,
    TaskResource,
    TaskConstraint,
    TaskMetadata,
    # Metrics
    SchedulingMetrics,
    # Backward compatibility aliases
    TaskSchedulerConfig,
    TaskSchedulerManager,
    TaskSchedulerCoordinator,
    TaskSchedulerCore,
)

__all__ = [
    # Main scheduler class
    "UnifiedTaskScheduler",
    "TaskScheduler",
    # Task types and enums
    "Task",
    "TaskPriority",
    "TaskStatus",
    "TaskType",
    "TaskCategory",
    "TaskDependency",
    "TaskResource",
    "TaskConstraint",
    "TaskMetadata",
    # Metrics
    "SchedulingMetrics",
    # Backward compatibility
    "TaskSchedulerConfig",
    "TaskSchedulerManager",
    "TaskSchedulerCoordinator",
    "TaskSchedulerCore",
]

__version__ = "2.0.0"
__author__ = "Agent_Cellphone_V2_System"
__description__ = "Unified Advanced Task Management System for Multi-Agent Workflows"
