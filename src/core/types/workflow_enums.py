#!/usr/bin/env python3
"""
Workflow and Task Management Enums
=================================

Consolidated workflow and task management enums from scattered locations.
Part of the unified type system consolidation.

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

from enum import Enum
from typing import Dict, List


class WorkflowStatus(Enum):
    """Unified workflow execution status - consolidated from multiple sources"""
    
    # Core workflow states
    CREATED = "created"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    PLANNING = "planning"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    EXECUTING = "executing"
    RUNNING = "running"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ERROR = "error"
    
    # V2 specific states
    VALIDATING = "validating"
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    RECOVERING = "recovering"
    
    @classmethod
    def get_transition_map(cls) -> Dict[str, List[str]]:
        """Get valid status transitions"""
        return {
            cls.CREATED.value: [cls.INITIALIZING.value, cls.PLANNING.value],
            cls.INITIALIZING.value: [cls.INITIALIZED.value, cls.FAILED.value],
            cls.INITIALIZED.value: [cls.PLANNING.value, cls.PENDING.value],
            cls.PLANNING.value: [cls.PENDING.value, cls.FAILED.value],
            cls.PENDING.value: [cls.IN_PROGRESS.value, cls.CANCELLED.value],
            cls.IN_PROGRESS.value: [cls.EXECUTING.value, cls.FAILED.value],
            cls.EXECUTING.value: [cls.RUNNING.value, cls.FAILED.value, cls.PAUSED.value],
            cls.RUNNING.value: [cls.ACTIVE.value, cls.PAUSED.value, cls.FAILED.value],
            cls.ACTIVE.value: [cls.COMPLETED.value, cls.PAUSED.value, cls.FAILED.value],
            cls.PAUSED.value: [cls.ACTIVE.value, cls.CANCELLED.value],
            cls.VALIDATING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.OPTIMIZING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.SCALING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.RECOVERING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.COMPLETED.value: [],
            cls.FAILED.value: [cls.RECOVERING.value, cls.CANCELLED.value],
            cls.CANCELLED.value: [],
            cls.ERROR.value: [cls.RECOVERING.value, cls.CANCELLED.value]
        }


class TaskStatus(Enum):
    """Unified task status - consolidated from multiple sources"""
    
    # Core task states
    PENDING = "pending"
    QUEUED = "queued"
    ASSIGNED = "assigned"
    RUNNING = "running"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    
    # V2 specific states
    VALIDATING = "validating"
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    RECOVERING = "recovering"
    
    @classmethod
    def get_transition_map(cls) -> Dict[str, List[str]]:
        """Get valid status transitions"""
        return {
            cls.PENDING.value: [cls.QUEUED.value, cls.CANCELLED.value],
            cls.QUEUED.value: [cls.ASSIGNED.value, cls.CANCELLED.value],
            cls.ASSIGNED.value: [cls.RUNNING.value, cls.CANCELLED.value],
            cls.RUNNING.value: [cls.EXECUTING.value, cls.FAILED.value, cls.TIMEOUT.value],
            cls.EXECUTING.value: [cls.COMPLETED.value, cls.FAILED.value, cls.TIMEOUT.value],
            cls.VALIDATING.value: [cls.RUNNING.value, cls.FAILED.value],
            cls.OPTIMIZING.value: [cls.RUNNING.value, cls.FAILED.value],
            cls.SCALING.value: [cls.RUNNING.value, cls.FAILED.value],
            cls.RECOVERING.value: [cls.RUNNING.value, cls.FAILED.value],
            cls.COMPLETED.value: [],
            cls.FAILED.value: [cls.RECOVERING.value, cls.CANCELLED.value],
            cls.CANCELLED.value: [],
            cls.TIMEOUT.value: [cls.RECOVERING.value, cls.CANCELLED.value]
        }


class WorkflowType(Enum):
    """Unified workflow type definitions"""
    
    # Core workflow types
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    ERROR_HANDLING = "error_handling"
    
    # V2 specific types
    AUTONOMOUS = "autonomous"
    COLLABORATIVE = "collaborative"
    ADAPTIVE = "adaptive"
    LEARNING = "learning"


class TaskType(Enum):
    """Unified task type definitions"""
    
    # Core task types
    COMPUTATION = "computation"
    I_O = "i_o"
    NETWORK = "network"
    DATABASE = "database"
    API_CALL = "api_call"
    
    # V2 specific types
    AI_PROCESSING = "ai_processing"
    MACHINE_LEARNING = "machine_learning"
    DATA_ANALYSIS = "data_analysis"
    AUTOMATION = "automation"


class Priority(Enum):
    """Unified priority levels"""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BACKGROUND = "background"
