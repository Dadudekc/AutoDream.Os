#!/usr/bin/env python3
"""
Smoke Tests for Vector Database - Agent Cellphone V2
===================================================

Comprehensive smoke tests for vector database operations and functionality.
Tests embedding storage, retrieval, semantic search, and database operations.

Author: Agent-2 (Architecture & Design)
License: MIT
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import json
import tempfile
import sqlite3
from unittest.mock import Mock, patch, MagicMock

# Import vector database components
from src.core.vector_database import (
    get_connection,
    upsert_agent_status,
    fetch_agent_status,
    DB_PATH,
    AGENT_STATUS_TABLE,
    SCHEMA
)


class TestVectorDatabaseSmoke:
    """Smoke tests for vector database functionality."""

    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database path for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            yield temp_path
            # Cleanup
            if temp_path.exists():
                temp_path.unlink()

    @pytest.fixture
    def mock_embedding_data(self):
        """Create mock embedding data for testing."""
        return {
            "agent_id": "Agent-1",
            "raw_status": json.dumps({
                "agent_id": "Agent-1",
                "status": "ACTIVE_AGENT_MODE",
                "current_mission": "Testing vector database",
                "last_updated": "2025-01-27 12:00:00"
            }),
            "embedding": json.dumps([0.1, 0.2, 0.3, 0.4, 0.5] * 20),  # 100 dimensions
            "last_updated": "2025-01-27 12:00:00"
        }

    def test_database_connection_creation(self, temp_db_path):
        """Test database connection creation and schema setup."""
        # Create connection to temporary database
        conn = get_connection(temp_db_path)

        # Verify connection is valid
        assert isinstance(conn, sqlite3.Connection)
        assert conn is not None

        # Verify table was created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (AGENT_STATUS_TABLE,))
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == AGENT_STATUS_TABLE

        # Verify schema columns
        cursor.execute(f"PRAGMA table_info({AGENT_STATUS_TABLE})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        expected_columns = ['agent_id', 'raw_status', 'embedding', 'last_updated']
        for col in expected_columns:
            assert col in column_names

        conn.close()

    def test_agent_status_upsert_operation(self, temp_db_path, mock_embedding_data):
        """Test upserting agent status embeddings."""
        conn = get_connection(temp_db_path)

        # Convert embedding string to list for the function
        embedding_list = json.loads(mock_embedding_data["embedding"])

        # Test upsert operation
        upsert_agent_status(
            conn=conn,
            agent_id=mock_embedding_data["agent_id"],
            raw_status=mock_embedding_data["raw_status"],
            embedding=embedding_list,
            last_updated=mock_embedding_data["last_updated"]
        )

        # Verify data was inserted
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {AGENT_STATUS_TABLE} WHERE agent_id = ?", (mock_embedding_data["agent_id"],))
        row = cursor.fetchone()

        assert row is not None
        assert row[0] == mock_embedding_data["agent_id"]  # agent_id
        assert row[1] == mock_embedding_data["raw_status"]  # raw_status
        assert row[2] == mock_embedding_data["embedding"]  # embedding
        assert row[3] == mock_embedding_data["last_updated"]  # last_updated

        conn.close()

    def test_agent_status_retrieval(self, temp_db_path, mock_embedding_data):
        """Test retrieving agent status from database."""
        conn = get_connection(temp_db_path)

        # Convert embedding string to list for the function
        embedding_list = json.loads(mock_embedding_data["embedding"])

        # Insert test data
        upsert_agent_status(
            conn=conn,
            agent_id=mock_embedding_data["agent_id"],
            raw_status=mock_embedding_data["raw_status"],
            embedding=embedding_list,
            last_updated=mock_embedding_data["last_updated"]
        )

        # Test retrieval
        result = fetch_agent_status(conn, mock_embedding_data["agent_id"])

        # Verify retrieval succeeded
        assert result is not None
        agent_id, raw_status, embedding, last_updated = result
        assert agent_id == mock_embedding_data["agent_id"]
        assert raw_status == mock_embedding_data["raw_status"]
        assert embedding == embedding_list
        assert last_updated == mock_embedding_data["last_updated"]

        conn.close()

    def test_bulk_agent_status_operations(self, temp_db_path):
        """Test bulk operations on multiple agent statuses."""
        conn = get_connection(temp_db_path)

        # Create multiple agent statuses
        agents_data = []
        for i in range(1, 5):  # Agent-1 through Agent-4
            agent_data = {
                "agent_id": f"Agent-{i}",
                "raw_status": json.dumps({
                    "agent_id": f"Agent-{i}",
                    "status": "ACTIVE_AGENT_MODE",
                    "current_mission": f"Test mission {i}",
                    "last_updated": "2025-01-27 12:00:00"
                }),
                "embedding": [0.1 * i] * 10,  # Different embeddings (smaller for test)
                "last_updated": "2025-01-27 12:00:00"
            }
            agents_data.append(agent_data)

            # Insert each agent
            upsert_agent_status(
                conn=conn,
                agent_id=agent_data["agent_id"],
                raw_status=agent_data["raw_status"],
                embedding=agent_data["embedding"],
                last_updated=agent_data["last_updated"]
            )

        # Test bulk retrieval by querying all
        all_statuses = []
        for agent_data in agents_data:
            result = fetch_agent_status(conn, agent_data["agent_id"])
            if result:
                agent_id, raw_status, embedding, last_updated = result
                all_statuses.append({
                    "agent_id": agent_id,
                    "raw_status": raw_status,
                    "embedding": embedding,
                    "last_updated": last_updated
                })

        # Verify all agents were retrieved
        assert len(all_statuses) == 4
        agent_ids = [status["agent_id"] for status in all_statuses]
        for i in range(1, 5):
            assert f"Agent-{i}" in agent_ids

        conn.close()

    def test_embedding_data_validation(self, temp_db_path):
        """Test embedding data validation and error handling."""
        conn = get_connection(temp_db_path)

        # Test with invalid JSON embedding
        with pytest.raises(json.JSONDecodeError):
            upsert_agent_status(
                agent_id="test-agent",
                raw_status='{"valid": "json"}',
                embedding="invalid json string",
                last_updated="2025-01-27 12:00:00",
                db_path=temp_db_path
            )

        # Test with empty embedding
        result = upsert_agent_status(
            agent_id="test-agent-2",
            raw_status='{"test": "data"}',
            embedding="[]",
            last_updated="2025-01-27 12:00:00",
            db_path=temp_db_path
        )
        assert result is True

        # Test retrieval of empty embedding
        status = get_agent_status("test-agent-2", temp_db_path)
        assert status is not None
        assert status["embedding"] == "[]"

        conn.close()

    def test_database_schema_constants(self):
        """Test database schema constants and configuration."""
        # Test database path constant
        assert DB_PATH is not None
        assert isinstance(DB_PATH, Path)

        # Test table name constant
        assert AGENT_STATUS_TABLE is not None
        assert AGENT_STATUS_TABLE == "agent_status_embeddings"

        # Test schema SQL
        assert SCHEMA is not None
        assert "CREATE TABLE IF NOT EXISTS" in SCHEMA
        assert AGENT_STATUS_TABLE in SCHEMA
        assert "agent_id TEXT PRIMARY KEY" in SCHEMA
        assert "raw_status TEXT NOT NULL" in SCHEMA
        assert "embedding TEXT NOT NULL" in SCHEMA
        assert "last_updated TEXT NOT NULL" in SCHEMA

    def test_agent_status_update_operations(self, temp_db_path, mock_embedding_data):
        """Test updating existing agent status."""
        conn = get_connection(temp_db_path)

        # Insert initial data
        upsert_agent_status(
            agent_id=mock_embedding_data["agent_id"],
            raw_status=mock_embedding_data["raw_status"],
            embedding=mock_embedding_data["embedding"],
            last_updated=mock_embedding_data["last_updated"],
            db_path=temp_db_path
        )

        # Update with new data
        updated_raw_status = json.dumps({
            "agent_id": "Agent-1",
            "status": "UPDATED_AGENT_MODE",
            "current_mission": "Updated test mission",
            "last_updated": "2025-01-27 13:00:00"
        })

        updated_embedding = json.dumps([0.5, 0.6, 0.7, 0.8, 0.9] * 20)

        result = upsert_agent_status(
            agent_id=mock_embedding_data["agent_id"],
            raw_status=updated_raw_status,
            embedding=updated_embedding,
            last_updated="2025-01-27 13:00:00",
            db_path=temp_db_path
        )

        # Verify update succeeded
        assert result is True

        # Verify data was updated
        updated_status = get_agent_status(mock_embedding_data["agent_id"], temp_db_path)
        assert updated_status is not None
        assert updated_status["raw_status"] == updated_raw_status
        assert updated_status["embedding"] == updated_embedding
        assert updated_status["last_updated"] == "2025-01-27 13:00:00"

        conn.close()

    def test_nonexistent_agent_retrieval(self, temp_db_path):
        """Test retrieving status for non-existent agent."""
        # Test retrieval of non-existent agent
        result = get_agent_status("NonExistentAgent", temp_db_path)

        # Should return None for non-existent agent
        assert result is None

    def test_database_connection_error_handling(self):
        """Test database connection error handling."""
        # Test with invalid path
        invalid_path = Path("/invalid/path/that/does/not/exist/db.sqlite")

        # This should handle the error gracefully
        conn = get_connection(invalid_path)

        # Connection should still be created (SQLite will create the file when needed)
        assert isinstance(conn, sqlite3.Connection)

        conn.close()

    def test_embedding_storage_formats(self, temp_db_path):
        """Test different embedding storage formats."""
        conn = get_connection(temp_db_path)

        # Test with different embedding formats
        test_cases = [
            ([1.0, 2.0, 3.0], "Small float array"),
            ([0.0] * 384, "Large zero array"),  # BERT-like dimensions
            ([i / 100.0 for i in range(768)], "Large float array"),  # GPT-like dimensions
        ]

        for i, (embedding, description) in enumerate(test_cases):
            agent_id = f"format-test-agent-{i}"

            result = upsert_agent_status(
                agent_id=agent_id,
                raw_status=json.dumps({"test": description}),
                embedding=json.dumps(embedding),
                last_updated="2025-01-27 12:00:00",
                db_path=temp_db_path
            )

            assert result is True, f"Failed to store {description}"

            # Verify retrieval
            status = get_agent_status(agent_id, temp_db_path)
            assert status is not None
            assert json.loads(status["embedding"]) == embedding

        conn.close()

    def test_concurrent_database_access(self, temp_db_path):
        """Test concurrent database access patterns."""
        import threading
        import time

        results = []
        errors = []

        def worker_thread(agent_id):
            try:
                # Each thread performs operations
                upsert_agent_status(
                    agent_id=agent_id,
                    raw_status=json.dumps({"thread": agent_id}),
                    embedding=json.dumps([0.1] * 10),
                    last_updated="2025-01-27 12:00:00",
                    db_path=temp_db_path
                )

                status = get_agent_status(agent_id, temp_db_path)
                results.append(status)
            except Exception as e:
                errors.append(str(e))

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_thread, args=[f"concurrent-agent-{i}"])
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify no errors occurred
        assert len(errors) == 0, f"Concurrent access errors: {errors}"

        # Verify all operations succeeded
        assert len(results) == 5

        # Verify all agents were stored
        all_statuses = get_all_agent_statuses(temp_db_path)
        agent_ids = [status["agent_id"] for status in all_statuses]
        for i in range(5):
            assert f"concurrent-agent-{i}" in agent_ids

    def test_database_performance_baseline(self, temp_db_path):
        """Test basic database performance characteristics."""
        import time

        conn = get_connection(temp_db_path)

        # Test bulk insert performance
        start_time = time.time()

        for i in range(100):
            upsert_agent_status(
                agent_id=f"perf-agent-{i}",
                raw_status=json.dumps({"test": f"performance test {i}"}),
                embedding=json.dumps([0.1] * 50),
                last_updated="2025-01-27 12:00:00",
                db_path=temp_db_path
            )

        end_time = time.time()
        duration = end_time - start_time

        # Should complete within reasonable time (adjust threshold as needed)
        assert duration < 5.0, f"Bulk insert took too long: {duration} seconds"

        # Verify all records were inserted
        all_statuses = get_all_agent_statuses(temp_db_path)
        assert len(all_statuses) == 100

        conn.close()


if __name__ == "__main__":
    # Run tests directly
    import sys
    print("Running Vector Database Smoke Tests...")

    # Create test instance
    test_instance = TestVectorDatabaseSmoke()

    # Run a simple test
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        mock_data = {
            "agent_id": "TestAgent",
            "raw_status": '{"status": "test"}',
            "embedding": "[0.1, 0.2, 0.3]",
            "last_updated": "2025-01-27 12:00:00"
        }

        test_instance.test_database_connection_creation(temp_path)
        print("[PASS] Database connection test passed")

        test_instance.test_agent_status_upsert_operation(temp_path, mock_data)
        print("[PASS] Agent status upsert test passed")

        test_instance.test_agent_status_retrieval(temp_path, mock_data)
        print("[PASS] Agent status retrieval test passed")

        print("[SUCCESS] All basic smoke tests passed!")

    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        sys.exit(1)
