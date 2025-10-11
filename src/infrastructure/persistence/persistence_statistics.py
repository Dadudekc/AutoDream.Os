"""
Persistence Statistics - Unified Persistence Service
====================================================

Provides statistics about the persistence layer.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import logging
from pathlib import Path
from typing import Any, Dict

from .database_connection import DatabaseConnection

logger = logging.getLogger(__name__)


class PersistenceStatistics:
    """Provides statistics about the persistence layer."""

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize statistics provider."""
        self.db = db_connection

    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics."""
        stats = {
            "total_agents": 0,
            "active_agents": 0,
            "total_tasks": 0,
            "pending_tasks": 0,
            "completed_tasks": 0,
            "assigned_tasks": 0,
            "database_size": 0,
            "table_info": {},
        }

        try:
            # Agent statistics
            agent_rows = self.db.execute_query("SELECT COUNT(*) FROM agents")
            stats["total_agents"] = agent_rows[0][0] if agent_rows else 0

            active_rows = self.db.execute_query(
                "SELECT COUNT(*) FROM agents WHERE is_active = 1"
            )
            stats["active_agents"] = active_rows[0][0] if active_rows else 0

            # Task statistics
            task_rows = self.db.execute_query("SELECT COUNT(*) FROM tasks")
            stats["total_tasks"] = task_rows[0][0] if task_rows else 0

            pending_rows = self.db.execute_query(
                "SELECT COUNT(*) FROM tasks WHERE assigned_agent_id IS NULL"
            )
            stats["pending_tasks"] = pending_rows[0][0] if pending_rows else 0

            completed_rows = self.db.execute_query(
                "SELECT COUNT(*) FROM tasks WHERE completed_at IS NOT NULL"
            )
            stats["completed_tasks"] = completed_rows[0][0] if completed_rows else 0

            assigned_rows = self.db.execute_query(
                "SELECT COUNT(*) FROM tasks WHERE assigned_agent_id IS NOT NULL AND completed_at IS NULL"
            )
            stats["assigned_tasks"] = assigned_rows[0][0] if assigned_rows else 0

            # Database file size
            db_path = Path(self.db.db_path)
            if db_path.exists():
                stats["database_size"] = db_path.stat().st_size

            # Table information
            table_info_rows = self.db.execute_query(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            for row in table_info_rows:
                table_name = row[0]
                count_rows = self.db.execute_query(f"SELECT COUNT(*) FROM {table_name}")
                stats["table_info"][table_name] = count_rows[0][0] if count_rows else 0

        except Exception as e:
            logger.error(f"Error getting database stats: {e}")

        return stats




