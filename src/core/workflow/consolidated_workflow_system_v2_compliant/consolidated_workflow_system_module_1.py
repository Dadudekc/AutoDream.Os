"""
Consolidated Workflow System
Unified workflow management infrastructure for the entire project.
V2 Compliance: Under 400 lines, SSOT principles, object-oriented design.
"""

import asyncio
import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
from concurrent.futures import ThreadPoolExecutor


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class WorkflowTask:
    """Individual workflow task definition."""
    id: str
    name: str
    action: Callable
    dependencies: List[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.NORMAL
    timeout: int = 300
    retry_count: int = 3
    retry_delay: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution: