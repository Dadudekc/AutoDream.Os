#!/usr/bin/env python3
"""Tests for agent status indexing."""

import json

from src.core import vector_database as vdb
from src.services.vector_database.status_indexer import index_all_statuses


class DummyEmbeddingService:
    """Simple embedding service stub for tests."""

    def generate_embedding(self, text: str):
        return [0.1, 0.2]


def test_index_statuses(tmp_path):
    """Status files should be embedded and stored in the database."""
    status_data = {
        "agent_id": "Agent-9",
        "status": "ACTIVE",
        "last_updated": "2025-01-01",
    }
    status_file = tmp_path / "status.json"
    status_file.write_text(json.dumps(status_data))

    conn = vdb.get_connection(tmp_path / "test.db")

    index_all_statuses(tmp_path, conn=conn, embedding_service=DummyEmbeddingService())

    record = vdb.fetch_agent_status(conn, "Agent-9")
    assert record is not None
    agent_id, raw_status, embedding, last_updated = record
    assert agent_id == "Agent-9"
    assert json.loads(raw_status)["status"] == "ACTIVE"
    assert embedding == [0.1, 0.2]
    assert last_updated == "2025-01-01"
