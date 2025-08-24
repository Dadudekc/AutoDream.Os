#!/usr/bin/env python3
"""
Autonomous Development Enums - Agent Cellphone V2
===============================================

Enums for task management and workflow.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from enum import Enum


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 10
    HIGH = 8
    MEDIUM_HIGH = 6
    MEDIUM = 5
    MEDIUM_LOW = 4
    LOW = 2
    MINIMAL = 1


class TaskComplexity(Enum):
    """Task complexity levels"""
    TRIVIAL = "trivial"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class TaskStatus(Enum):
    """Task status values"""
    AVAILABLE = "available"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class WorkflowState(Enum):
    """Workflow state values"""
    IDLE = "idle"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


class AgentRole(Enum):
    """Agent role types"""
    COORDINATOR = "coordinator"
    WORKER = "worker"
    MONITOR = "monitor"
    VALIDATOR = "validator"
    BACKUP = "backup"
