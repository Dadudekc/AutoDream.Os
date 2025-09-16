import logging
logger = logging.getLogger(__name__)
"""
SQLite Task Repository - Infrastructure Adapter
===============================================

Concrete implementation of TaskRepository using SQLite.
This is an adapter that implements the domain port.
"""

import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager

from ...domain.entities.task import Task
from ...domain.ports.task_repository import TaskRepository
from ...domain.value_objects.ids import AgentId, TaskId


class SqliteTaskRepository(TaskRepository):
    """
    SQLite implementation of the TaskRepository port.

    This adapter provides persistence for tasks using SQLite database.
    It implements the TaskRepository protocol defined in the domain layer.
    """

    def __init__(self, db_path: str = "data/tasks.db"):
        """
        Initialize the SQLite repository.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with self._get_connection() as conn:
            conn.execute(

EXAMPLE USAGE:
==============

# Basic usage example
from src.infrastructure.persistence.sqlite_task_repo import Sqlite_Task_Repo

# Initialize and use
instance = Sqlite_Task_Repo()
result = instance.execute()
logger.info(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Sqlite_Task_Repo(config)
advanced_result = instance.execute_advanced()
logger.info(f"Advanced result: {advanced_result}")

                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    assigned_agent_id TEXT,
                    created_at TEXT NOT NULL,
                    assigned_at TEXT,
                    completed_at TEXT,
                    priority INTEGER DEFAULT 1
                )
            """
            )
            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get a database connection with proper cleanup."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def get(self, task_id: TaskId) -> Task | None:
        """
        Retrieve a task by its identifier.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The task if found, None otherwise
        """
        with self._get_connection() as conn:
            row = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks WHERE id = ?
            """,
                (task_id,),
            ).fetchone()

            if not row:
                return None

            return self._row_to_task(row)

    def get_by_agent(self, agent_id: str, limit: int = 100) -> Iterable[Task]:
        """
        Retrieve tasks assigned to a specific agent.

        Args:
            agent_id: The agent identifier
            limit: Maximum number of tasks to return

        Returns:
            Iterable of tasks assigned to the agent
        """
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks
                WHERE assigned_agent_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (agent_id, limit),
            ).fetchall()

            for row in rows:
                yield self._row_to_task(row)

    def get_pending(self, limit: int = 100) -> Iterable[Task]:
        """
        Retrieve pending (unassigned) tasks.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            Iterable of pending tasks
        """
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks
                WHERE assigned_agent_id IS NULL
                ORDER BY priority DESC, created_at ASC
                LIMIT ?
            """,
                (limit,),
            ).fetchall()

            for row in rows:
                yield self._row_to_task(row)

    def add(self, task: Task) -> None:
        """
        Add a new task to the repository.

        Args:
            task: The task to add

        Raises:
            ValueError: If task with same ID already exists
        """
        with self._get_connection() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO tasks (
                        id, title, description, assigned_agent_id,
                        created_at, assigned_at, completed_at, priority
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    self._task_to_row(task),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Task with ID {task.id} already exists")

    def save(self, task: Task) -> None:
        """
        Save an existing task (create or update).

        Args:
            task: The task to save
        """
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO tasks (
                    id, title, description, assigned_agent_id,
                    created_at, assigned_at, completed_at, priority
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                self._task_to_row(task),
            )
            conn.commit()

    def delete(self, task_id: TaskId) -> bool:
        """
        Delete a task from the repository.

        Args:
            task_id: The identifier of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    def list_all(self, limit: int = 1000) -> Iterable[Task]:
        """
        List all tasks in the repository.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            Iterable of all tasks
        """
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, title, description, assigned_agent_id,
                       created_at, assigned_at, completed_at, priority
                FROM tasks
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            ).fetchall()

            for row in rows:
                yield self._row_to_task(row)

    def _row_to_task(self, row) -> Task:
        """Convert database row to Task entity."""
        from datetime import datetime

        (
            task_id,
            title,
            description,
            assigned_agent_id,
            created_at_str,
            assigned_at_str,
            completed_at_str,
            priority,
        ) = row

        # Parse datetime strings
        created_at = datetime.fromisoformat(created_at_str)
        assigned_at = datetime.fromisoformat(assigned_at_str) if assigned_at_str else None
        completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else None

        # Convert agent_id if present
        agent_id = AgentId(assigned_agent_id) if assigned_agent_id else None

        return Task(
            id=TaskId(task_id),
            title=title,
            description=description,
            assigned_agent_id=agent_id,
            created_at=created_at,
            assigned_at=assigned_at,
            completed_at=completed_at,
            priority=priority,
        )

    def _task_to_row(self, task: Task):
        """Convert Task entity to database row tuple."""
        return (
            task.id,  # str (from TaskId)
            task.title,
            task.description,
            task.assigned_agent_id,  # str or None (from AgentId)
            task.created_at.isoformat(),
            task.assigned_at.isoformat() if task.assigned_at else None,
            task.completed_at.isoformat() if task.completed_at else None,
            task.priority,
        )
