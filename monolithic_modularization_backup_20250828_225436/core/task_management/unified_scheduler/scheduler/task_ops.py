from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

from ..enums import TaskPriority, TaskStatus
from ..models import Task

logger = logging.getLogger(__name__)


class TaskOperationsMixin:
    """Public task lifecycle operations."""

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

                self._handle_task_completion(task_id)
                self._update_metrics(task, "completed")

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
                task.status = TaskStatus.FAILED
                task.error_message = error_message
                task.completed_at = datetime.now()

                del self._running_tasks[task_id]
                self._failed_tasks[task_id] = task

                self._update_metrics(task, "failed")

                logger.info(f"Task {task_id} marked as failed: {error_message}")
                return True

        except Exception as e:
            logger.error(f"Error failing task {task_id}: {e}")
            return False
