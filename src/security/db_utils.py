import sqlite3
from typing import Iterable, Any, List, Tuple


def execute_db(db_file: str, query: str, params: Iterable[Any] = ()) -> None:
    """Execute a write query against a SQLite database."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()


def fetch_one(
    db_file: str, query: str, params: Iterable[Any] = ()
) -> Tuple[Any, ...] | None:
    """Fetch a single row from a SQLite database."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        return cursor.fetchone()


def fetch_all(
    db_file: str, query: str, params: Iterable[Any] = ()
) -> List[Tuple[Any, ...]]:
    """Fetch all rows for a query from a SQLite database."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
