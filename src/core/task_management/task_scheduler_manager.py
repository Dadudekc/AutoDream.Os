"""Public interface for the task scheduler."""

from __future__ import annotations

import asyncio
import logging
import threading
from typing import Any, Callable, Optional

from .task_types import Task, TaskPriority, TaskStatus
from .task_scheduler_config import SchedulingMetrics


logger = logging.getLogger(__name__)


class TaskSchedulerManager:
    """High level task management operations."""

    async def start(self):
        """Start the task scheduler."""
        if self._running:
            logger.warning("Task scheduler already running")
            return

        self._running = True
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_loop, daemon=True
        )
        self._scheduler_thread.start()

        logger.info("Task scheduler started")

    async def stop(self):
        """Stop the task scheduler."""
        if not self._running:
            return

        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)

        logger.info("Task scheduler stopped")

    async def submit_task(self, task: Task) -> bool:
        """Submit a task for scheduling."""
        try:
            with self._lock:
                if not self._validate_task(task):
                    logger.error(f"Task validation failed for {task.task_id}")
                    return False

                self._tasks[task.task_id] = task

                priority_score = self._calculate_priority_score(task)
                self._priority_queues[task.priority].put((priority_score, task))

                self._update_dependency_graph(task)

                self._update_metrics(task, "submitted")

                logger.info(f"Task {task.task_id} submitted successfully")
                return True

        except Exception as e:
            logger.error(f"Error submitting task {task.task_id}: {e}")
            return False

    async def get_next_task(self, agent_id: str) -> Optional[Task]:
        """Get the next available task for an agent."""
        try:
            with self._lock:
                if not self._can_agent_handle_task(agent_id):
                    return None

                for priority in reversed(list(TaskPriority)):
                    task = self._get_next_task_from_priority(priority, agent_id)
                    if task:
                        return task

                return None

        except Exception as e:
            logger.error(f"Error getting next task for agent {agent_id}: {e}")
            return None

    async def complete_task(self, task_id: str, result: Any = None) -> bool:
        """Mark a task as completed."""
        try:
            with self._lock:
                if task_id not in self._running_tasks:
                    logger.error(f"Task {task_id} not found in running tasks")
                    return False

                task = self._running_tasks[task_id]
                task.complete_execution(result)

                del self._running_tasks[task_id]
                self._completed_tasks[task_id] = task

                self._release_agent_resources(task.assigned_agent, task)

                self._handle_task_completion(task_id)

                self._update_metrics(task, "completed")

                await self._trigger_task_callbacks("completed", task)

                logger.info(f"Task {task_id} completed successfully")
                return True

        except Exception as e:
            logger.error(f"Error completing task {task_id}: {e}")
            return False

    async def fail_task(self, task_id: str, error_message: str) -> bool:
        """Mark a task as failed."""
        try:
            with self._lock:
                if task_id not in self._running_tasks:
                    logger.error(f"Task {task_id} not found in running tasks")
                    return False

                task = self._running_tasks[task_id]
                task.fail_execution(error_message)

                if task.can_retry():
                    await self._retry_task(task)
                else:
                    del self._running_tasks[task_id]
                    self._failed_tasks[task_id] = task

                    self._release_agent_resources(task.assigned_agent, task)

                    self._update_metrics(task, "failed")

                    await self._trigger_task_callbacks("failed", task)

                logger.info(f"Task {task_id} marked as failed: {error_message}")
                return True

        except Exception as e:
            logger.error(f"Error failing task {task_id}: {e}")
            return False

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending or running task."""
        try:
            with self._lock:
                task = (
                    self._tasks.get(task_id)
                    or self._running_tasks.get(task_id)
                    or self._completed_tasks.get(task_id)
                    or self._failed_tasks.get(task_id)
                )

                if not task:
                    logger.error(f"Task {task_id} not found")
                    return False

                task.cancel_execution()

                self._tasks.pop(task_id, None)
                self._running_tasks.pop(task_id, None)

                self._failed_tasks[task_id] = task

                if task.assigned_agent:
                    self._release_agent_resources(task.assigned_agent, task)

                self._handle_task_cancellation(task_id)

                await self._trigger_task_callbacks("cancelled", task)

                logger.info(f"Task {task_id} cancelled successfully")
                return True

        except Exception as e:
            logger.error(f"Error cancelling task {task_id}: {e}")
            return False

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the current status of a task."""
        with self._lock:
            task = (
                self._tasks.get(task_id)
                or self._running_tasks.get(task_id)
                or self._completed_tasks.get(task_id)
                or self._failed_tasks.get(task_id)
            )
            return task.status if task else None

    def get_scheduler_metrics(self) -> SchedulingMetrics:
        """Get current scheduler metrics."""
        with self._lock:
            return self._metrics

    def register_task_callback(self, event_type: str, callback: Callable):
        """Register a callback for task events."""
        self._task_callbacks[event_type].append(callback)

