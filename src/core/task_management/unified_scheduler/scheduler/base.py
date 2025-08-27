from __future__ import annotations

import logging
import threading
from collections import defaultdict
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Set

from ..enums import TaskPriority
from ..metrics import SchedulingMetrics
from ..models import Task

logger = logging.getLogger(__name__)


class BaseScheduler:
    """Initialize core scheduler state and data structures."""

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
            f"✅ Unified Task Scheduler initialized with max {max_concurrent_tasks} concurrent tasks"
        )
