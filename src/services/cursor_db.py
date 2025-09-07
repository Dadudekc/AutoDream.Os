import os
import sqlite3
from typing import Any, Dict, List, Optional


class CursorTaskRepository:
    """Database access layer for reading agent task records."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or os.getenv("CURSOR_DB_PATH", "cursor_tasks.db")
        self.db_user = os.getenv("CURSOR_DB_USER")
        self.db_password = os.getenv("CURSOR_DB_PASSWORD")

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_tasks_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """Return all task records for a given agent."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT task_id, agent_id, signal FROM agent_tasks WHERE agent_id = ?",
                (agent_id,),
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
        return [
            {"task_id": row[0], "agent_id": row[1], "signal": row[2]}
            for row in rows
        ]
