"""Task and message scheduling for the communication coordinator."""

import logging
from queue import PriorityQueue
from typing import Dict, List

from .coordinator_types import (
    CoordinationMessage,
    CoordinationTask,
    TaskPriority,
    TaskStatus,
)
from .utils import current_timestamp, generate_id

logger = logging.getLogger(__name__)


class TaskScheduler:
    """Simple priority-based scheduler for tasks and messages."""

    def __init__(self):
        self.message_queue: PriorityQueue = PriorityQueue()
        self.tasks: Dict[str, CoordinationTask] = {}
        self.logger = logging.getLogger(f"{__name__}.TaskScheduler")

    def schedule_message(self, message: CoordinationMessage) -> None:
        """Queue a message based on priority and timestamp."""
        priority_map = {
            TaskPriority.PRESIDENTIAL: -1,
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.NORMAL: 2,
            TaskPriority.LOW: 3,
        }
        priority = priority_map.get(message.priority, 2)
        self.message_queue.put((priority, current_timestamp(), message))
        logger.debug("Queued message %s with priority %s", message.message_id, priority)

    def create_task(
        self,
        title: str,
        description: str,
        priority: TaskPriority,
        assigned_agents: List[str],
    ) -> str:
        """Create a new coordination task."""
        task_id = generate_id()
        task = CoordinationTask(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            assigned_agents=list(assigned_agents),
            dependencies=[],
            created_at=current_timestamp(),
            due_date=None,
            estimated_hours=0.0,
            actual_hours=0.0,
            progress_percentage=0.0,
            tags=[],
        )
        self.tasks[task_id] = task
        logger.debug("Created task %s", task_id)
        return task_id

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign task to an agent."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        if agent_id not in task.assigned_agents:
            task.assigned_agents.append(agent_id)
        task.status = TaskStatus.ASSIGNED
        logger.debug("Assigned task %s to %s", task_id, agent_id)
        return True

    def update_task_status(
        self, task_id: str, status: TaskStatus, progress: float
    ) -> bool:
        """Update task progress and status."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        task.status = status
        task.progress_percentage = progress
        logger.debug(
            "Updated task %s status to %s (%.1f%%)", task_id, status.value, progress
        )
        return True
