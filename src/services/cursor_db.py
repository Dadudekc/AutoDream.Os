"""Database access layer for Cursor agent task records.

This module exposes a repository for querying Cursor task entries. The
underlying database is SQLite and its path is provided via the
``CURSOR_DB_PATH`` environment variable. This design keeps configuration as a
single source of truth and follows the repository pattern for data access.
"""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DB_PATH = Path(os.getenv("CURSOR_DB_PATH", "data/cursor_tasks.db"))


@dataclass
class CursorTask:
    """Record representing an agent task stored in the Cursor database."""

    task_id: str
    agent_id: str
    status: str


class CursorTaskRepository:
    """Repository providing read access to Cursor task records."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        """Return a connection to the task database."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.db_path)

    def get_task(self, task_id: str) -> CursorTask | None:
        """Fetch a task by its identifier.

        Args:
            task_id: Identifier of the task.

        Returns:
            CursorTask if found, otherwise ``None``.
        """

        with self._connect() as conn:
            cur = conn.execute(
                "SELECT task_id, agent_id, status FROM tasks WHERE task_id = ?",
                (task_id,),
            )
            row = cur.fetchone()
            if row:
                return CursorTask(*row)
            return None

    def task_exists(self, task_id: str) -> bool:
        """Return True if the task exists in the database."""
        return self.get_task(task_id) is not None