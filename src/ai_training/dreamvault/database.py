"""
Database Abstraction Layer for DreamVault

Provides a unified interface for both SQLite and PostgreSQL databases.
Supports seamless switching via DATABASE_URL environment variable.
"""

import logging
import os
import sqlite3
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Try importing PostgreSQL driver
try:
    import psycopg

    PSYCOPG_AVAILABLE = True
except ImportError:
    PSYCOPG_AVAILABLE = False
    psycopg = None


class DatabaseConnection:
    """
    Database connection abstraction supporting SQLite and PostgreSQL.

    Usage:
        # From environment variable
        db = DatabaseConnection()

        # Explicit URL
        db = DatabaseConnection("postgresql://user:pass@localhost:5432/dreamvault")

        # Get connection
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM conversations")
    """

    def __init__(self, database_url: str | None = None):
        """
        Initialize database connection.

        Args:
            database_url: Database URL (sqlite:///path or postgresql://...).
                         If None, reads from DATABASE_URL env var.
                         Defaults to sqlite:///data/dreamvault.db
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", "sqlite:///data/dreamvault.db"
        )
        self.parsed_url = urlparse(self.database_url)
        self.db_type = self._detect_database_type()

        logger.info(f"Database initialized: {self.db_type} ({self._safe_url()})")

    def _detect_database_type(self) -> str:
        """Detect database type from URL."""
        scheme = self.parsed_url.scheme

        if scheme in ("sqlite", "sqlite3"):
            return "sqlite"
        elif scheme in ("postgresql", "postgres", "postgresql+psycopg"):
            if not PSYCOPG_AVAILABLE:
                raise ImportError(
                    "PostgreSQL support requires psycopg. "
                    "Install with: pip install 'psycopg[binary]'"
                )
            return "postgresql"
        else:
            raise ValueError(f"Unsupported database scheme: {scheme}")

    def _safe_url(self) -> str:
        """Return URL with password redacted for logging."""
        if self.db_type == "sqlite":
            return self.database_url

        # Redact password from PostgreSQL URL
        if self.parsed_url.password:
            safe_url = self.database_url.replace(self.parsed_url.password, "****")
            return safe_url
        return self.database_url

    def get_connection(self) -> sqlite3.Connection | Any:
        """
        Get a database connection.

        Returns:
            Database connection (sqlite3.Connection or psycopg.Connection)
        """
        if self.db_type == "sqlite":
            return self._get_sqlite_connection()
        elif self.db_type == "postgresql":
            return self._get_postgresql_connection()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def _get_sqlite_connection(self) -> sqlite3.Connection:
        """Get SQLite connection."""
        # Extract path from URL (handle both sqlite:/// and sqlite://)
        path = self.parsed_url.path
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash for relative paths

        # Ensure directory exists
        from pathlib import Path

        db_path = Path(path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create connection
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access

        return conn

    def _get_postgresql_connection(self) -> Any:
        """Get PostgreSQL connection."""
        # Use the full URL for psycopg
        return psycopg.connect(self.database_url)

    def execute(self, query: str, params: tuple | None = None) -> Any:
        """
        Execute a query and return results.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # For SELECT queries, fetch results
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()

            # For INSERT/UPDATE/DELETE, commit and return affected rows
            conn.commit()
            return cursor.rowcount

    def executemany(self, query: str, params_list: list) -> int:
        """
        Execute a query multiple times with different parameters.

        Args:
            query: SQL query
            params_list: List of parameter tuples

        Returns:
            Total number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount

    def get_placeholder(self) -> str:
        """
        Get the parameter placeholder for this database type.

        SQLite uses ?, PostgreSQL uses %s

        Returns:
            Placeholder string
        """
        if self.db_type == "sqlite":
            return "?"
        elif self.db_type == "postgresql":
            return "%s"
        else:
            return "?"

    def adapt_query(self, query: str) -> str:
        """
        Adapt a query for the current database type.

        Converts placeholders and database-specific syntax.

        Args:
            query: SQL query with generic placeholders

        Returns:
            Adapted query
        """
        if self.db_type == "postgresql":
            # Convert SQLite placeholders (?) to PostgreSQL (%s)
            # This is a simple conversion - for complex cases, use get_placeholder()
            # and build queries dynamically
            adapted = query.replace("?", "%s")

            # Convert SQLite data types to PostgreSQL
            adapted = adapted.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
            adapted = adapted.replace("AUTOINCREMENT", "")

            return adapted

        return query

    def test_connection(self) -> bool:
        """
        Test the database connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False


# Global connection instance
_global_connection: DatabaseConnection | None = None


def get_database_connection(database_url: str | None = None) -> DatabaseConnection:
    """
    Get or create the global database connection.

    Args:
        database_url: Optional database URL. If not provided, uses existing
                     global connection or creates one from environment.

    Returns:
        DatabaseConnection instance
    """
    global _global_connection

    if database_url:
        # Create new connection with specified URL
        return DatabaseConnection(database_url)

    if _global_connection is None:
        # Create global connection from environment
        _global_connection = DatabaseConnection()

    return _global_connection


def reset_database_connection():
    """Reset the global database connection (useful for testing)."""
    global _global_connection
    _global_connection = None
