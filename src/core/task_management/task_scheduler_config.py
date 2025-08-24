"""Task Scheduler configuration and metrics definitions."""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Set
from collections import defaultdict

from .task_types import Task, TaskPriority, TaskType


logger = logging.getLogger(__name__)


@dataclass
class SchedulingMetrics:
    """Metrics for monitoring scheduler performance."""

    total_tasks_scheduled: int = 0
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_scheduling_time: float = 0.0
    average_execution_time: float = 0.0
    tasks_by_priority: Dict[TaskPriority, int] = field(default_factory=dict)
    tasks_by_type: Dict[TaskType, int] = field(default_factory=dict)
    last_update: datetime = field(default_factory=datetime.now)


class TaskSchedulerConfig:
    """Base configuration and state for the task scheduler."""

    def __init__(self, max_concurrent_tasks: int = 100):
        self.max_concurrent_tasks = max_concurrent_tasks
        self._lock = threading.RLock()

        # Task queues by priority
        self._priority_queues: Dict[TaskPriority, PriorityQueue] = {
            priority: PriorityQueue() for priority in TaskPriority
        }

        # Task storage and tracking
        self._tasks: Dict[str, Task] = {}
        self._running_tasks: Dict[str, Task] = {}
        self._completed_tasks: Dict[str, Task] = {}
        self._failed_tasks: Dict[str, Task] = {}

        # Dependency tracking
        self._dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self._reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)

        # Resource tracking
        self._agent_resources: Dict[str, Dict[str, Any]] = {}
        self._resource_locks: Dict[str, threading.Lock] = {}

        # Scheduling metrics
        self._metrics = SchedulingMetrics()

        # Event callbacks
        self._task_callbacks: Dict[str, List[Callable]] = defaultdict(list)

        # Scheduler state
        self._running = False
        self._scheduler_thread: Optional[threading.Thread] = None

        logger.info(
            f"TaskScheduler initialized with max {max_concurrent_tasks} concurrent tasks"
        )

