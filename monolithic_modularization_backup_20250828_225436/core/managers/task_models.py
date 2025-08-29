#!/usr/bin/env python3
"""Task models and enums for TaskManager."""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Any


class TaskStatus(Enum):
    """Task status states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    URGENT = 5


class TaskType(Enum):
    """Task types"""
    COMPUTATION = "computation"
    I_O = "io"
    NETWORK = "network"
    DATABASE = "database"
    FILE_OPERATION = "file_operation"
    SYSTEM = "system"
    CUSTOM = "custom"


@dataclass
class Task:
    """Task definition"""
    id: str
    name: str
    description: str
    task_type: TaskType
    priority: TaskPriority
    status: TaskStatus
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    duration: Optional[float]
    result: Optional[Any]
    error: Optional[str]
    metadata: Dict[str, Any]
    dependencies: List[str]
    retry_count: int
    max_retries: int
    timeout: Optional[float]
    tags: List[str]


@dataclass
class Workflow:
    """Workflow definition"""
    id: str
    name: str
    description: str
    tasks: List[str]
    dependencies: Dict[str, List[str]]
    status: TaskStatus
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    metadata: Dict[str, Any]


@dataclass
class TaskResult:
    """Task execution result"""
    task_id: str
    success: bool
    result: Any
    error: Optional[str]
    execution_time: float
    metadata: Dict[str, Any]
