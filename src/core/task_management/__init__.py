#!/usr/bin/env python3
"""
Advanced Task Management System
==============================

This module provides enterprise-grade task management capabilities including:
- Task definition and types
- Priority-based scheduling
- Dependency resolution
- Resource allocation
- Performance monitoring
"""

from .task_types import (
    Task, TaskPriority, TaskStatus, TaskType, TaskCategory,
    TaskDependency, TaskResource, TaskConstraint, TaskMetadata
)

from .task_scheduler import TaskScheduler, SchedulingMetrics

__all__ = [
    # Task types and enums
    'Task',
    'TaskPriority', 
    'TaskStatus',
    'TaskType',
    'TaskCategory',
    'TaskDependency',
    'TaskResource',
    'TaskConstraint',
    'TaskMetadata',
    
    # Scheduler
    'TaskScheduler',
    'SchedulingMetrics',
]

__version__ = "1.0.0"
__author__ = "Agent_Cellphone_V2_System"
__description__ = "Advanced Task Management System for Multi-Agent Workflows"
