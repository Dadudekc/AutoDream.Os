"""
Scheduler Queue Manager - Task Queue Operations
===============================================

Handles priority queue operations and task readiness checks.
Extracted from scheduler.py for preventive optimization.

Author: Agent-1 - Autonomous Operations Specialist
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import heapq
import logging

from .scheduler_models import Task


class SchedulerQueue:
    """Manages task queue and readiness logic."""

    def __init__(
        self,
        completed_tasks: set[str],
        failed_tasks: set[str],
        logger: logging.Logger | None = None,
    ):
        """
        Initialize scheduler queue.

        Args:
            completed_tasks: Set of completed task IDs
            failed_tasks: Set of failed task IDs
            logger: Logger instance
        """
        self.task_queue: list[Task] = []
        self.completed_tasks = completed_tasks
        self.failed_tasks = failed_tasks
        self.logger = logger or logging.getLogger(__name__)

    def add_task(self, task: Task) -> None:
        """Add task to priority queue."""
        heapq.heappush(self.task_queue, task)

    def get_available_tasks(self, cycle_number: int) -> list[Task]:
        """
        Get tasks available for execution in this cycle.

        Args:
            cycle_number: Current cycle number

        Returns:
            List of available tasks
        """
        available_tasks = []
        temp_queue = []

        # Process priority queue
        while self.task_queue:
            task = heapq.heappop(self.task_queue)

            # Check if task is ready for this cycle
            if self.is_task_ready(task, cycle_number):
                available_tasks.append(task)
            else:
                temp_queue.append(task)

        # Restore tasks not ready for this cycle
        for task in temp_queue:
            heapq.heappush(self.task_queue, task)

        return available_tasks

    def is_task_ready(self, task: Task, cycle_number: int) -> bool:
        """
        Check if a task is ready for execution.

        Args:
            task: Task to check
            cycle_number: Current cycle number

        Returns:
            True if task is ready
        """
        # Check if task is scheduled for this cycle or later
        if task.scheduled_cycle and task.scheduled_cycle > cycle_number:
            return False

        # Check dependencies
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False

        # Check if task has exceeded max retries
        if task.retry_count >= task.max_retries:
            self.failed_tasks.add(task.id)
            return False

        return True

    def remove_task(self, task_id: str) -> None:
        """
        Remove task from priority queue.

        Args:
            task_id: ID of task to remove
        """
        temp_queue = []

        while self.task_queue:
            task = heapq.heappop(self.task_queue)
            if task.id != task_id:
                temp_queue.append(task)

        # Restore remaining tasks
        for task in temp_queue:
            heapq.heappush(self.task_queue, task)

    def balance_agent_load(self, tasks: list[Task], agent_load: dict[str, float]) -> list[Task]:
        """
        Balance task load across agents.

        Args:
            tasks: Tasks to balance
            agent_load: Current agent loads

        Returns:
            Balanced tasks
        """
        # Sort tasks by priority first
        tasks.sort(key=lambda t: t.priority)

        # Distribute tasks to balance load
        balanced_tasks = []
        agent_loads = agent_load.copy()

        for task in tasks:
            # Find agent with lowest current load
            target_agent = min(agent_loads.keys(), key=lambda a: agent_loads[a])

            # Update task agent if different
            if task.agent_id != target_agent:
                task.agent_id = target_agent
                self.logger.info(f"Rebalanced task {task.id} to {target_agent}")

            # Update load tracking
            agent_loads[target_agent] += task.estimated_duration
            balanced_tasks.append(task)

        return balanced_tasks

    def get_queue_size(self) -> int:
        """Get current queue size."""
        return len(self.task_queue)
