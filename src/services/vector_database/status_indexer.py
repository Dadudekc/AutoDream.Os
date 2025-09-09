#!/usr/bin/env python3
"""Agent status indexing helper.

Loads ``status.json`` files, computes embeddings, and upserts them into the
vector database's ``agent_status_embeddings`` table.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# from ...core import vector_database as vdb  # Commented out to fix import issues
from ..embedding_service import EmbeddingService


def load_status(path: Path) -> tuple[str, str, str]:
    """Return ``agent_id``, serialized status, and ``last_updated``."""
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    agent_id = data.get("agent_id") or path.parent.name
    raw_status = json.dumps(data, sort_keys=True)
    last_updated = data.get("last_updated", datetime.utcnow().isoformat())
    return agent_id, raw_status, last_updated


def index_all_statuses(
    base_dir: Path = Path("."),
    conn: sqlite3.Connection | None = None,
    embedding_service: EmbeddingService | None = None,
) -> None:
    """Index all ``status.json`` files under ``base_dir``."""
    service = embedding_service or EmbeddingService()
    db_conn = conn or vdb.get_connection()
    for status_file in base_dir.rglob("status.json"):
        agent_id, raw_status, last_updated = load_status(status_file)
        embedding = service.generate_embedding(raw_status)
        vdb.upsert_agent_status(db_conn, agent_id, raw_status, embedding, last_updated)


__all__ = ["index_all_statuses"]
