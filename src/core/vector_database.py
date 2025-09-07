#!/usr/bin/env python3
"""Core vector database utilities.

This module provides a minimal SSOT interface for storing agent status
embeddings. It uses SQLite under the hood and exposes helper functions for
interacting with the ``agent_status_embeddings`` table.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Single source of truth constants
# ---------------------------------------------------------------------------
DB_PATH = Path("data/vector_database.db")
AGENT_STATUS_TABLE = "agent_status_embeddings"

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {AGENT_STATUS_TABLE} (
    agent_id TEXT PRIMARY KEY,
    raw_status TEXT NOT NULL,
    embedding TEXT NOT NULL,
    last_updated TEXT NOT NULL
)
"""


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection ensuring the status table exists."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    return conn


# ---------------------------------------------------------------------------
# Agent status embedding operations
# ---------------------------------------------------------------------------


def upsert_agent_status(
    conn: sqlite3.Connection,
    agent_id: str,
    raw_status: str,
    embedding: Sequence[float],
    last_updated: str,
) -> None:
    """Insert or update an agent status embedding."""
    payload = (
        agent_id,
        raw_status,
        json.dumps(list(embedding)),
        last_updated,
    )
    conn.execute(
        f"""
        INSERT INTO {AGENT_STATUS_TABLE}
            (agent_id, raw_status, embedding, last_updated)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(agent_id) DO UPDATE SET
            raw_status=excluded.raw_status,
            embedding=excluded.embedding,
            last_updated=excluded.last_updated
        """,
        payload,
    )
    conn.commit()


def fetch_agent_status(
    conn: sqlite3.Connection, agent_id: str
) -> Optional[Tuple[str, str, Sequence[float], str]]:
    """Fetch a stored agent status embedding."""
    cursor = conn.execute(
        f"SELECT agent_id, raw_status, embedding, last_updated FROM {AGENT_STATUS_TABLE} WHERE agent_id=?",
        (agent_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    stored_id, raw_status, embedding_json, last_updated = row
    return stored_id, raw_status, json.loads(embedding_json), last_updated


__all__ = [
    "AGENT_STATUS_TABLE",
    "get_connection",
    "upsert_agent_status",
    "fetch_agent_status",
]
