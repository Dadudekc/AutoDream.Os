"""
Task Repository Port - Domain Interface
=======================================

Defines the contract for task persistence operations.
This is a port in the hexagonal architecture - the domain defines what it needs.
"""

from typing import Protocol, Iterable, Optional
from src.domain.entities.task import Task
from src.domain.value_objects.ids import TaskId


class TaskRepository(Protocol):
    """
    Port for task persistence operations.

    This protocol defines the interface that any task repository
    implementation must provide. The domain layer depends only on this
    abstraction, not on concrete implementations.
    """

    def get(self, task_id: TaskId) -> Optional[Task]:
        """
        Retrieve a task by its identifier.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The task if found, None otherwise
        """
        ...

    def get_by_agent(self, agent_id: str, limit: int = 100) -> Iterable[Task]:
        """
        Retrieve tasks assigned to a specific agent.

        Args:
            agent_id: The agent identifier
            limit: Maximum number of tasks to return

        Returns:
            Iterable of tasks assigned to the agent
        """
        ...

    def get_pending(self, limit: int = 100) -> Iterable[Task]:
        """
        Retrieve pending (unassigned) tasks.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            Iterable of pending tasks
        """
        ...

    def add(self, task: Task) -> None:
        """
        Add a new task to the repository.

        Args:
            task: The task to add

        Raises:
            ValueError: If task with same ID already exists
        """
        ...

    def save(self, task: Task) -> None:
        """
        Save an existing task (create or update).

        Args:
            task: The task to save
        """
        ...

    def delete(self, task_id: TaskId) -> bool:
        """
        Delete a task from the repository.

        Args:
            task_id: The identifier of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        ...

    def list_all(self, limit: int = 1000) -> Iterable[Task]:
        """
        List all tasks in the repository.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            Iterable of all tasks
        """
        ...
