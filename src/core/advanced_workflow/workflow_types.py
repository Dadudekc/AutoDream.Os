"""
Workflow Types and Enums - V2 Compliant Type Definitions

This module contains all workflow-related type definitions, enums, and constants.
Follows V2 standards with ≤100 LOC and single responsibility for type definitions.
"""

from enum import Enum


class WorkflowType(Enum):
    """Advanced workflow types - consolidated from multiple sources"""
    
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    EVENT_DRIVEN = "event_driven"
    ADAPTIVE = "adaptive"
    
    # V2 specific types
    INITIALIZATION = "initialization"
    TRAINING = "training"
    ROLE_ASSIGNMENT = "role_assignment"
    CAPABILITY_GRANT = "capability_grant"
    SYSTEM_INTEGRATION = "system_integration"
    VALIDATION = "validation"
    COMPLETION = "completion"


class WorkflowStatus(Enum):
    """Workflow status values - integrated from V2 system"""
    
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RUNNING = "running"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class WorkflowPriority(Enum):
    """Workflow priority levels"""
    
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class OptimizationStrategy(Enum):
    """Workflow optimization strategies"""
    
    PERFORMANCE = "performance"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    COST_OPTIMIZATION = "cost_optimization"
    LATENCY_REDUCTION = "latency_reduction"
    THROUGHPUT_MAXIMIZATION = "throughput_maximization"


class AgentCapability(Enum):
    """Agent capability types for workflow steps"""
    
    GENERAL = "general"
    AI_PROCESSING = "ai_processing"
    DATA_ANALYSIS = "data_analysis"
    SYSTEM_INTEGRATION = "system_integration"
    VALIDATION = "validation"
    OPTIMIZATION = "optimization"
    MONITORING = "monitoring"
    REPORTING = "reporting"


# Constants for workflow configuration
DEFAULT_TIMEOUT = 300.0  # 5 minutes
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_OPTIMIZATION_INTERVAL = 300  # 5 minutes
MAX_PARALLEL_STEPS = 10
MIN_STEP_DURATION = 0.1  # 100ms minimum

# Workflow metadata keys
METADATA_KEYS = {
    "dynamic": "boolean",
    "optimization_enabled": "boolean", 
    "scalability_target": "string",
    "workflow_type": "string",
    "agent_id": "string",
    "created_by": "string",
    "version": "string",
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "execution_time_ms": 1000,
    "memory_usage_mb": 100,
    "cpu_usage_percent": 80,
    "response_time_ms": 500,
}

