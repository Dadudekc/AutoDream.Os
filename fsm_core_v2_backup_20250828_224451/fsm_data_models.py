#!/usr/bin/env python3
"""
FSM Data Models - Finite State Machine Data Structures
====================================================

Contains all data models, enums, and dataclasses for the FSM system.
Follows V2 standards: focused responsibility, clear data structures.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


# ============================================================================
# ENUMS
# ============================================================================


class StateStatus(Enum):
    """State execution status."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TransitionType(Enum):
    """Types of state transitions."""

    AUTOMATIC = "automatic"
    MANUAL = "manual"
    CONDITIONAL = "conditional"
    TIMEOUT = "timeout"
    ERROR = "error"


class WorkflowPriority(Enum):
    """Workflow priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


# ============================================================================
# DATA MODELS
# ============================================================================


@dataclass
class StateDefinition:
    """State definition structure."""

    name: str
    description: str
    entry_actions: List[str]
    exit_actions: List[str]
    timeout_seconds: Optional[float]
    retry_count: int
    retry_delay: float
    required_resources: List[str]
    dependencies: List[str]
    metadata: Dict[str, Any]


@dataclass
class TransitionDefinition:
    """Transition definition structure."""

    from_state: str
    to_state: str
    transition_type: TransitionType
    condition: Optional[str]
    priority: int
    timeout_seconds: Optional[float]
    actions: List[str]
    metadata: Dict[str, Any]


@dataclass
class WorkflowInstance:
    """Workflow instance tracking."""

    workflow_id: str
    workflow_name: str
    current_state: str
    state_history: List[Dict[str, Any]]
    start_time: datetime
    last_update: datetime
    status: StateStatus
    priority: WorkflowPriority
    metadata: Dict[str, Any]
    error_count: int
    retry_count: int


@dataclass
class StateExecutionResult:
    """Result of state execution."""

    state_name: str
    execution_time: float
    status: StateStatus
    output: Dict[str, Any]
    error_message: Optional[str]
    metadata: Dict[str, Any]
    timestamp: datetime


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def state_definition_to_dict(state_def: StateDefinition) -> Dict[str, Any]:
    """Convert StateDefinition to dictionary."""
    return asdict(state_def)


def transition_definition_to_dict(transition_def: TransitionDefinition) -> Dict[str, Any]:
    """Convert TransitionDefinition to dictionary."""
    return asdict(transition_def)


def workflow_instance_to_dict(workflow: WorkflowInstance) -> Dict[str, Any]:
    """Convert WorkflowInstance to dictionary."""
    return asdict(workflow)


def state_execution_result_to_dict(result: StateExecutionResult) -> Dict[str, Any]:
    """Convert StateExecutionResult to dictionary."""
    return asdict(result)


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================


def validate_state_definition(state_def: StateDefinition) -> bool:
    """Validate state definition data."""
    if not state_def.name or not state_def.name.strip():
        return False
    
    if state_def.retry_count < 0:
        return False
    
    if state_def.retry_delay < 0:
        return False
    
    return True


def validate_transition_definition(transition_def: TransitionDefinition) -> bool:
    """Validate transition definition data."""
    if not transition_def.from_state or not transition_def.to_state:
        return False
    
    if transition_def.priority < 0:
        return False
    
    if transition_def.timeout_seconds is not None and transition_def.timeout_seconds < 0:
        return False
    
    return True


def validate_workflow_instance(workflow: WorkflowInstance) -> bool:
    """Validate workflow instance data."""
    if not workflow.workflow_id or not workflow.workflow_name:
        return False
    
    if workflow.error_count < 0 or workflow.retry_count < 0:
        return False
    
    return True


# ============================================================================
# EXPORTS
# ============================================================================


__all__ = [
    "StateStatus",
    "TransitionType", 
    "WorkflowPriority",
    "StateDefinition",
    "TransitionDefinition",
    "WorkflowInstance",
    "StateExecutionResult",
    "state_definition_to_dict",
    "transition_definition_to_dict",
    "workflow_instance_to_dict",
    "state_execution_result_to_dict",
    "validate_state_definition",
    "validate_transition_definition",
    "validate_workflow_instance",
]
