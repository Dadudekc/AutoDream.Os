#!/usr/bin/env python3
"""
Workflow Types - V2 Core Workflow Data Models

This module contains all data structures and enums for workflow automation.
Follows V2 standards: ≤100 lines, single responsibility, clean OOP design.

Author: Agent-4 (Quality Assurance)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class WorkflowStatus(Enum):
    """Workflow execution status"""
    CREATED = "created"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskStatus(Enum):
    """Individual task status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkflowType(Enum):
    """Workflow execution types"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    PIPELINE = "pipeline"
    PARALLEL_BATCH = "parallel_batch"


@dataclass
class WorkflowTask:
    """Individual workflow task"""
    task_id: str
    name: str
    description: str
    agent_id: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_duration: int = 60  # seconds
    actual_duration: Optional[int] = None
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    required_resources: List[str] = field(default_factory=list)
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowCondition:
    """Conditional workflow logic"""
    condition_id: str
    name: str
    condition_type: str  # "if", "while", "for", "switch"
    condition_expression: str
    true_branch: List[str]  # Task IDs to execute if true
    false_branch: List[str] = field(default_factory=list)
    loop_condition: Optional[str] = None  # For loop workflows
    max_iterations: int = 100  # Prevent infinite loops
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """Workflow execution instance"""
    execution_id: str
    workflow_id: str
    workflow_name: str
    status: WorkflowStatus = WorkflowStatus.CREATED
    tasks: List[WorkflowTask] = field(default_factory=list)
    conditions: List[WorkflowCondition] = field(default_factory=list)
    current_task_index: int = 0
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    execution_path: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_duration: Optional[int] = None
    error_count: int = 0
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentCapability:
    """Agent capability definition"""
    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    current_load: int = 0
    max_concurrent_tasks: int = 5
    performance_score: float = 1.0
    availability: bool = True
    last_heartbeat: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceRequirement:
    """Resource requirement definition"""
    resource_id: str
    resource_type: str  # "cpu", "memory", "storage", "network", "custom"
    required_amount: float
    unit: str
    priority: TaskPriority = TaskPriority.MEDIUM
    current_availability: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
