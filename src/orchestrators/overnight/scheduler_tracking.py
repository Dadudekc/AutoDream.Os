"""
Scheduler Tracking - Task State Management
==========================================

Handles task completion, failure, and retry logic.
Extracted from scheduler.py for preventive optimization.

Author: Agent-1 - Autonomous Operations Specialist
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import logging

from .scheduler_models import Task


class SchedulerTracking:
    """Manages task completion and failure tracking."""

    def __init__(
        self,
        task_registry: dict[str, Task],
        completed_tasks: set[str],
        failed_tasks: set[str],
        agent_load: dict[str, float],
        current_cycle: int = 0,
        logger: logging.Logger | None = None,
    ):
        """
        Initialize scheduler tracking.

        Args:
            task_registry: Dictionary of task ID to Task
            completed_tasks: Set of completed task IDs
            failed_tasks: Set of failed task IDs
            agent_load: Dictionary of agent ID to current load
            current_cycle: Current cycle number
            logger: Logger instance
        """
        self.task_registry = task_registry
        self.completed_tasks = completed_tasks
        self.failed_tasks = failed_tasks
        self.agent_load = agent_load
        self.current_cycle = current_cycle
        self.logger = logger or logging.getLogger(__name__)

    def mark_task_completed(self, task_id: str, remove_from_queue_fn) -> None:
        """
        Mark a task as completed.

        Args:
            task_id: ID of completed task
            remove_from_queue_fn: Function to remove task from queue
        """
        if task_id in self.task_registry:
            self.completed_tasks.add(task_id)

            # Remove from queue if still there
            remove_from_queue_fn(task_id)

            # Update agent load
            task = self.task_registry[task_id]
            self.agent_load[task.agent_id] = max(
                0, self.agent_load[task.agent_id] - task.estimated_duration
            )

            self.logger.info(f"Task completed: {task_id}")

    def mark_task_failed(
        self, task_id: str, retry: bool, add_to_queue_fn, remove_from_queue_fn
    ) -> None:
        """
        Mark a task as failed and optionally retry.

        Args:
            task_id: ID of failed task
            retry: Whether to retry the task
            add_to_queue_fn: Function to add task back to queue
            remove_from_queue_fn: Function to remove task from queue
        """
        if task_id not in self.task_registry:
            return

        task = self.task_registry[task_id]

        if retry and task.retry_count < task.max_retries:
            # Retry task
            task.retry_count += 1
            task.priority += 1  # Lower priority for retry
            task.scheduled_cycle = self.current_cycle + 1  # Schedule for next cycle

            # Re-add to queue
            add_to_queue_fn(task)

            self.logger.info(f"Task retry scheduled: {task_id} (attempt {task.retry_count})")
        else:
            # Mark as permanently failed
            self.failed_tasks.add(task_id)
            remove_from_queue_fn(task_id)

            # Update agent load
            self.agent_load[task.agent_id] = max(
                0, self.agent_load[task.agent_id] - task.estimated_duration
            )

            self.logger.error(f"Task permanently failed: {task_id}")

    def update_agent_load(self, agent_id: str, duration: float) -> None:
        """
        Update agent load.

        Args:
            agent_id: Agent ID
            duration: Duration to add to load
        """
        self.agent_load[agent_id] += duration

    def set_current_cycle(self, cycle: int) -> None:
        """Set current cycle number."""
        self.current_cycle = cycle

    def get_tracking_status(self) -> dict[str, int]:
        """Get tracking status."""
        return {
            "registered_tasks": len(self.task_registry),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
        }
