#!/usr/bin/env python3
"""
Workflow Enums - Unified Status and Type Definitions
===================================================

Consolidated workflow enums from multiple implementations.
Follows V2 standards: ≤100 LOC, single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

from enum import Enum
from typing import Dict, Any


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
    def get_transition_map(cls) -> Dict[str, list]:
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
    RETRYING = "retrying"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    
    @classmethod
    def is_terminal(cls, status: 'TaskStatus') -> bool:
        """Check if status is terminal (no further transitions)"""
        return status in [cls.COMPLETED, cls.FAILED, cls.CANCELLED, cls.SKIPPED]
    
    @classmethod
    def is_active(cls, status: 'TaskStatus') -> bool:
        """Check if status indicates active execution"""
        return status in [cls.RUNNING, cls.EXECUTING, cls.VALIDATING]


class TaskType(Enum):
    """Unified task types - consolidated from multiple sources"""
    
    # Core task types
    COMPUTATION = "computation"
    DATA_PROCESSING = "data_processing"
    DECISION = "decision"
    INTEGRATION = "integration"
    
    # V2 specific types
    VALIDATION = "validation"
    OPTIMIZATION = "optimization"
    MONITORING = "monitoring"
    REPORTING = "reporting"
    ERROR_HANDLING = "error_handling"
    RECOVERY = "recovery"
    
    @classmethod
    def get_category(cls, task_type: 'TaskType') -> str:
        """Get task category for grouping"""
        categories = {
            "processing": [cls.COMPUTATION, cls.DATA_PROCESSING],
            "control": [cls.DECISION, cls.ERROR_HANDLING, cls.RECOVERY],
            "integration": [cls.INTEGRATION, cls.VALIDATION],
            "operations": [cls.OPTIMIZATION, cls.MONITORING, cls.REPORTING]
        }
        
        for category, types in categories.items():
            if task_type in types:
                return category
        return "other"


class WorkflowType(Enum):
    """Unified workflow types - consolidated from multiple sources"""
    
    # Core workflow types
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    PIPELINE = "pipeline"
    PARALLEL_BATCH = "parallel_batch"
    
    # V2 specific types
    EVENT_DRIVEN = "event_driven"
    ADAPTIVE = "adaptive"
    INITIALIZATION = "initialization"
    TRAINING = "training"
    ROLE_ASSIGNMENT = "role_assignment"
    CAPABILITY_GRANT = "capability_grant"
    SYSTEM_INTEGRATION = "system_integration"
    VALIDATION = "validation"
    OPTIMIZATION = "optimization"
    MONITORING = "monitoring"
    REPORTING = "reporting"
    COMPLETION = "completion"
    
    @classmethod
    def get_category(cls, workflow_type: 'WorkflowType') -> str:
        """Get workflow category for grouping"""
        categories = {
            "execution": [cls.SEQUENTIAL, cls.PARALLEL, cls.PIPELINE, cls.PARALLEL_BATCH],
            "control": [cls.CONDITIONAL, cls.LOOP, cls.EVENT_DRIVEN, cls.ADAPTIVE],
            "lifecycle": [cls.INITIALIZATION, cls.TRAINING, cls.ROLE_ASSIGNMENT, cls.COMPLETION],
            "system": [cls.SYSTEM_INTEGRATION, cls.VALIDATION, cls.OPTIMIZATION, cls.MONITORING]
        }
        
        for category, types in categories.items():
            if workflow_type in types:
                return category
        return "other"


class TaskPriority(Enum):
    """Unified task priority levels - consolidated from multiple sources"""
    
    # Core priority levels
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    # V2 specific levels
    NORMAL = "normal"
    URGENT = "urgent"
    EMERGENCY = "emergency"
    
    @classmethod
    def get_numeric_value(cls, priority: 'TaskPriority') -> int:
        """Get numeric value for priority comparison"""
        priority_values = {
            cls.LOW: 1,
            cls.NORMAL: 2,
            cls.MEDIUM: 3,
            cls.HIGH: 4,
            cls.URGENT: 5,
            cls.CRITICAL: 6,
            cls.EMERGENCY: 7
        }
        return priority_values.get(priority, 0)
    
    @classmethod
    def is_high_priority(cls, priority: 'TaskPriority') -> bool:
        """Check if priority is high or above"""
        return cls.get_numeric_value(priority) >= cls.get_numeric_value(cls.HIGH)


class OptimizationStrategy(Enum):
    """Workflow optimization strategies - consolidated from multiple sources"""
    
    # Core strategies
    PERFORMANCE = "performance"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    COST_OPTIMIZATION = "cost_optimization"
    LATENCY_REDUCTION = "latency_reduction"
    THROUGHPUT_MAXIMIZATION = "throughput_maximization"
    
    # V2 specific strategies
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    FLEXIBILITY = "flexibility"
    ADAPTABILITY = "adaptability"
    
    @classmethod
    def get_description(cls, strategy: 'OptimizationStrategy') -> str:
        """Get human-readable description of strategy"""
        descriptions = {
            cls.PERFORMANCE: "Optimize for maximum performance",
            cls.RESOURCE_EFFICIENCY: "Minimize resource usage",
            cls.COST_OPTIMIZATION: "Reduce operational costs",
            cls.LATENCY_REDUCTION: "Minimize response time",
            cls.THROUGHPUT_MAXIMIZATION: "Maximize processing capacity",
            cls.SCALABILITY: "Improve system scaling",
            cls.RELIABILITY: "Enhance system reliability",
            cls.FLEXIBILITY: "Increase system flexibility",
            cls.ADAPTABILITY: "Improve system adaptability"
        }
        return descriptions.get(strategy, "Unknown optimization strategy")


class AgentCapability(Enum):
    """Agent capability types - consolidated from multiple sources"""
    
    # Core capabilities
    GENERAL = "general"
    AI_PROCESSING = "ai_processing"
    DATA_ANALYSIS = "data_analysis"
    SYSTEM_INTEGRATION = "system_integration"
    VALIDATION = "validation"
    OPTIMIZATION = "optimization"
    MONITORING = "monitoring"
    REPORTING = "reporting"
    
    # V2 specific capabilities
    WORKFLOW_EXECUTION = "workflow_execution"
    TASK_PLANNING = "task_planning"
    RESOURCE_MANAGEMENT = "resource_management"
    ERROR_HANDLING = "error_handling"
    PERFORMANCE_TUNING = "performance_tuning"
    SCALABILITY_OPTIMIZATION = "scalability_optimization"
    
    @classmethod
    def get_category(cls, capability: 'AgentCapability') -> str:
        """Get capability category for grouping"""
        categories = {
            "core": [cls.GENERAL, cls.AI_PROCESSING, cls.DATA_ANALYSIS],
            "system": [cls.SYSTEM_INTEGRATION, cls.VALIDATION, cls.OPTIMIZATION],
            "operations": [cls.MONITORING, cls.REPORTING, cls.ERROR_HANDLING],
            "workflow": [cls.WORKFLOW_EXECUTION, cls.TASK_PLANNING, cls.RESOURCE_MANAGEMENT],
            "performance": [cls.PERFORMANCE_TUNING, cls.SCALABILITY_OPTIMIZATION]
        }
        
        for category, capabilities in categories.items():
            if capability in capabilities:
                return category
        return "other"
