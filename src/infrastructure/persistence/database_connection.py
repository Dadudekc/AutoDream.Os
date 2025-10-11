"""
Database Connection - Unified Persistence Service
==================================================

Manages database connections with proper cleanup and configuration.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from .persistence_models import PersistenceConfig

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages database connections with proper cleanup and configuration."""

    def __init__(self, config: PersistenceConfig):
        """Initialize database connection manager."""
        self.config = config
        self.db_path = config.db_path

        # Ensure database directory exists
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Get a database connection with proper configuration and cleanup."""
        conn = sqlite3.connect(self.db_path, timeout=self.config.connection_timeout)

        try:
            if self.config.enable_foreign_keys:
                conn.execute("PRAGMA foreign_keys = ON")

            if self.config.enable_wal_mode:
                conn.execute("PRAGMA journal_mode = WAL")

            yield conn

        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> list[tuple]:
        """Execute a query and return results."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update query and return affected rows."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def create_tables(self, schema_queries: list[str]) -> bool:
        """Create database tables from schema queries."""
        try:
            with self.get_connection() as conn:
                for query in schema_queries:
                    conn.execute(query)
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            return False
