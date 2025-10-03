"""
Priority Scheduler - Priority-based task scheduling system.
Based on Dream.OS AgentDispatcher patterns with V2 compliance.

Features:
- 5-level priority system
- Task lifecycle management
- Dependency resolution
- Resource management
- Retry logic
"""

import logging
import queue
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels for intelligent dispatching."""

    CRITICAL = auto()  # Immediate execution required
    HIGH = auto()  # Execute as soon as possible
    MEDIUM = auto()  # Normal execution priority
    LOW = auto()  # Execute when resources available
    BACKGROUND = auto()  # Execute during low-load periods


class TaskStatus(Enum):
    """Possible states for a task in the system."""

    PENDING = auto()  # Awaiting execution
    RUNNING = auto()  # Currently executing
    COMPLETED = auto()  # Successfully completed
    FAILED = auto()  # Failed to execute
    RETRYING = auto()  # Being retried after failure
    CANCELLED = auto()  # Cancelled before completion
    BLOCKED = auto()  # Blocked by dependencies


@dataclass
class Task:
    """Represents a task in the system with metadata."""

    id: str
    agent_type: str
    task_type: str
    payload: dict[str, Any]
    priority: TaskPriority
    dependencies: list[str]
    created_at: datetime
    scheduled_for: datetime | None = None
    status: TaskStatus = TaskStatus.PENDING
    retries: int = 0
    max_retries: int = 3
    last_error: str | None = None
    execution_time: float | None = None
    metadata: dict[str, Any] = None


class PriorityScheduler:
    """
    Priority-based task scheduler with dependency resolution.
    V2 Compliant: ≤400 lines, simple data classes, direct method calls.
    """

    def __init__(self, max_workers: int = 4):
        """Initialize PriorityScheduler."""
        self.max_workers = max_workers
        self.tasks: dict[str, Task] = {}
        self.task_queues = {priority: queue.PriorityQueue() for priority in TaskPriority}
        self.running_tasks: dict[str, Task] = {}
        self.completed_tasks: list[Task] = []
        self.failed_tasks: list[Task] = []

        self._lock = threading.Lock()
        self._workers: list[threading.Thread] = []
        self._shutdown = False

        # Start worker threads
        self._start_workers()

    def _start_workers(self) -> None:
        """Start worker threads for task execution."""
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker_loop, name=f"PriorityWorker-{i}", daemon=True
            , daemon=True, daemon=True, daemon=True)
            worker.start()
            self._workers.append(worker)

    def _worker_loop(self) -> None:
        """Main worker loop for task execution."""
        while not self._shutdown:
            try:
                # Get next task from priority queues
                task = self._get_next_task()
                if task is None:
                    time.sleep(0.1)  # Brief pause if no tasks
                    continue

                # Execute task
                self._execute_task(task)

            except Exception as e:
                logger.error(f"Worker error: {e}")
                time.sleep(1)

    def _get_next_task(self) -> Task | None:
        """Get next task from priority queues."""
        with self._lock:
            # Check tasks in priority order
            for priority in TaskPriority:
                if not self.task_queues[priority].empty():
                    try:
                        # PriorityQueue returns (priority, task)
                        _, task = self.task_queues[priority].get_nowait()

                        # Check if task is ready to run
                        if self._is_task_ready(task):
                            return task
                        else:
                            # Put task back in queue
                            self.task_queues[priority].put((priority.value, task))

                    except queue.Empty:
                        continue

            return None

    def _is_task_ready(self, task: Task) -> bool:
        """Check if task is ready to run (dependencies satisfied)."""
        if task.status != TaskStatus.PENDING:
            return False

        # Check dependencies
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False

            dep_task = self.tasks[dep_id]
            if dep_task.status != TaskStatus.COMPLETED:
                return False

        # Check scheduling
        if task.scheduled_for and datetime.now() < task.scheduled_for:
            return False

        return True

    def _execute_task(self, task: Task) -> None:
        """Execute a task."""
        with self._lock:
            task.status = TaskStatus.RUNNING
            self.running_tasks[task.id] = task

        start_time = time.time()

        try:
            # Get task handler
            handler = self._get_task_handler(task)
            if handler is None:
                raise ValueError(f"No handler found for task type: {task.task_type}")

            # Execute task
            result = handler(task.payload)

            # Task completed successfully
            with self._lock:
                task.status = TaskStatus.COMPLETED
                task.execution_time = time.time() - start_time
                self.completed_tasks.append(task)
                if task.id in self.running_tasks:
                    del self.running_tasks[task.id]

            logger.info(f"Task {task.id} completed in {task.execution_time:.2f}s")

        except Exception as e:
            # Task failed
            with self._lock:
                task.status = TaskStatus.FAILED
                task.last_error = str(e)
                task.execution_time = time.time() - start_time

                # Retry logic
                if task.retries < task.max_retries:
                    task.retries += 1
                    task.status = TaskStatus.RETRYING
                    task.scheduled_for = datetime.now() + timedelta(seconds=2**task.retries)

                    # Put task back in queue for retry
                    self.task_queues[task.priority].put((task.priority.value, task))
                    logger.info(
                        f"Task {task.id} scheduled for retry {task.retries}/{task.max_retries}"
                    )
                else:
                    self.failed_tasks.append(task)
                    logger.error(f"Task {task.id} failed after {task.max_retries} retries: {e}")

                if task.id in self.running_tasks:
                    del self.running_tasks[task.id]

    def _get_task_handler(self, task: Task) -> Callable | None:
        """Get task handler function."""
        # This would be implemented with a registry of task handlers
        # For now, return None to indicate no handler found
        return None

    def submit_task(self, task: Task) -> None:
        """Submit a task for execution."""
        with self._lock:
            self.tasks[task.id] = task
            self.task_queues[task.priority].put((task.priority.value, task))

        logger.info(f"Task {task.id} submitted with priority {task.priority.name}")

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status in [TaskStatus.PENDING, TaskStatus.RETRYING]:
                    task.status = TaskStatus.CANCELLED
                    return True
        return False

    def get_task_status(self, task_id: str) -> TaskStatus | None:
        """Get task status."""
        with self._lock:
            if task_id in self.tasks:
                return self.tasks[task_id].status
        return None

    def get_task_stats(self) -> dict[str, Any]:
        """Get task execution statistics."""
        with self._lock:
            return {
                "total_tasks": len(self.tasks),
                "pending_tasks": sum(
                    1 for t in self.tasks.values() if t.status == TaskStatus.PENDING
                ),
                "running_tasks": len(self.running_tasks),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "retrying_tasks": sum(
                    1 for t in self.tasks.values() if t.status == TaskStatus.RETRYING
                ),
            }

    def shutdown(self) -> None:
        """Shutdown the scheduler."""
        self._shutdown = True

        # Wait for workers to finish
        for worker in self._workers:
            worker.join(timeout=5)

        logger.info("PriorityScheduler shutdown complete")


# Global scheduler instance
scheduler = PriorityScheduler()


def submit_task(task: Task) -> None:
    """Submit a task for execution."""
    scheduler.submit_task(task)


def cancel_task(task_id: str) -> bool:
    """Cancel a task."""
    return scheduler.cancel_task(task_id)


def get_task_status(task_id: str) -> TaskStatus | None:
    """Get task status."""
    return scheduler.get_task_status(task_id)


def get_task_stats() -> dict[str, Any]:
    """Get task execution statistics."""
    return scheduler.get_task_stats()
