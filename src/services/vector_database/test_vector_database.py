#!/usr/bin/env python3
"""
Vector Database Test Suite - V2 Compliance
==========================================

Comprehensive test suite for vector database system.
Tests all components and integration scenarios.

Author: Agent-3 (Database Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive error handling
"""

import os
import tempfile
import unittest
from datetime import UTC, datetime

import numpy as np

from .vector_database_integration import VectorDatabaseIntegration
from .vector_database_models import (
    VectorMetadata,
    VectorQuery,
    VectorRecord,
    VectorStatus,
    VectorType,
)
from .vector_database_monitoring import VectorDatabaseMonitor


class TestVectorDatabase(unittest.TestCase):
    """Test suite for vector database system."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_vector.db")
        self.integration = VectorDatabaseIntegration(self.db_path)
        self.monitor = VectorDatabaseMonitor(self.integration)

    def tearDown(self):
        """Clean up test environment."""
        self.monitor.close()
        self.integration.close()
        # Clean up temp files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_vector_storage_and_retrieval(self):
        """Test basic vector storage and retrieval."""
        # Create test vector
        test_vector = np.random.rand(32).astype(np.float32)
        metadata = VectorMetadata(
            vector_id="test_vector_1",
            vector_type=VectorType.STATUS,
            agent_id="test_agent",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            status=VectorStatus.ACTIVE,
            dimensions=32,
            source="test",
            tags=["test"],
            properties={"test": True},
        )

        vector_record = VectorRecord(metadata, test_vector)

        # Store vector
        success = self.integration.orchestrator.store_vector(vector_record)
        self.assertTrue(success)

        # Retrieve vector
        retrieved = self.integration.orchestrator.retrieve_vector("test_vector_1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.metadata.vector_id, "test_vector_1")
        np.testing.assert_array_almost_equal(retrieved.vector_data, test_vector)

    def test_vector_search(self):
        """Test vector similarity search."""
        # Create multiple test vectors
        vectors = []
        for i in range(5):
            test_vector = np.random.rand(32).astype(np.float32)
            metadata = VectorMetadata(
                vector_id=f"test_vector_{i}",
                vector_type=VectorType.STATUS,
                agent_id="test_agent",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                status=VectorStatus.ACTIVE,
                dimensions=32,
                source="test",
                tags=["test"],
                properties={"index": i},
            )
            vectors.append(VectorRecord(metadata, test_vector))

        # Store vectors
        for vector_record in vectors:
            success = self.integration.orchestrator.store_vector(vector_record)
            self.assertTrue(success)

        # Search for similar vectors
        query_vector = vectors[0].vector_data
        query = VectorQuery(
            query_vector=query_vector,
            vector_type=VectorType.STATUS,
            agent_id="test_agent",
            limit=3,
            similarity_threshold=0.0,
        )

        results = self.integration.orchestrator.search_vectors(query)
        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 3)

    def test_agent_status_integration(self):
        """Test agent status integration."""
        status_data = {
            "status": "active",
            "cycle_count": 10,
            "tasks_completed": 5,
            "coordination_efficiency": 0.85,
            "v2_compliance": 0.95,
        }

        vector_id = self.integration.integrate_agent_status(
            "test_agent", status_data, VectorType.STATUS
        )

        self.assertIsNotNone(vector_id)
        self.assertNotEqual(vector_id, "")

        # Verify vector was stored
        retrieved = self.integration.orchestrator.retrieve_vector(vector_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.metadata.agent_id, "test_agent")

    def test_message_integration(self):
        """Test message data integration."""
        message_data = {
            "from_agent": "Agent-1",
            "to_agent": "Agent-2",
            "priority": "normal",
            "content": "Test message",
            "timestamp": datetime.now(UTC).isoformat(),
        }

        vector_id = self.integration.integrate_message_data(message_data)

        self.assertIsNotNone(vector_id)
        self.assertNotEqual(vector_id, "")

        # Verify vector was stored
        retrieved = self.integration.orchestrator.retrieve_vector(vector_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.metadata.vector_type, VectorType.MESSAGE)

    def test_task_integration(self):
        """Test task data integration."""
        task_data = {
            "task_id": "TASK_001",
            "agent_id": "Agent-3",
            "priority": "high",
            "status": "in_progress",
            "progress": 75,
            "description": "Test task",
        }

        vector_id = self.integration.integrate_task_data(task_data)

        self.assertIsNotNone(vector_id)
        self.assertNotEqual(vector_id, "")

        # Verify vector was stored
        retrieved = self.integration.orchestrator.retrieve_vector(vector_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.metadata.vector_type, VectorType.TASK)

    def test_similar_status_search(self):
        """Test similar status search functionality."""
        # Create multiple status vectors
        status_data_1 = {
            "status": "active",
            "cycle_count": 10,
            "tasks_completed": 5,
            "coordination_efficiency": 0.85,
            "v2_compliance": 0.95,
        }

        status_data_2 = {
            "status": "active",
            "cycle_count": 12,
            "tasks_completed": 6,
            "coordination_efficiency": 0.87,
            "v2_compliance": 0.96,
        }

        # Integrate statuses
        vector_id_1 = self.integration.integrate_agent_status("test_agent", status_data_1)
        vector_id_2 = self.integration.integrate_agent_status("test_agent", status_data_2)

        # Search for similar statuses
        results = self.integration.search_similar_status("test_agent", status_data_1, limit=5)

        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 5)

    def test_agent_analytics(self):
        """Test agent analytics generation."""
        # Create test data
        for i in range(10):
            status_data = {
                "status": "active" if i % 2 == 0 else "inactive",
                "cycle_count": i,
                "tasks_completed": i * 2,
                "coordination_efficiency": 0.8 + (i * 0.01),
                "v2_compliance": 0.9 + (i * 0.005),
            }
            self.integration.integrate_agent_status("test_agent", status_data)

        # Get analytics
        analytics = self.integration.get_agent_analytics("test_agent", time_range_hours=24)

        self.assertIsNotNone(analytics)
        self.assertIn("agent_id", analytics)
        self.assertIn("total_vectors", analytics)
        self.assertIn("status_distribution", analytics)
        self.assertEqual(analytics["agent_id"], "test_agent")

    def test_system_health(self):
        """Test system health monitoring."""
        # Create some test data
        status_data = {
            "status": "active",
            "cycle_count": 1,
            "tasks_completed": 1,
            "coordination_efficiency": 0.8,
            "v2_compliance": 0.9,
        }
        self.integration.integrate_agent_status("test_agent", status_data)

        # Get system health
        health = self.integration.get_system_health()

        self.assertIsNotNone(health)
        self.assertIn("health_score", health)
        self.assertIn("status", health)
        self.assertIn("database_stats", health)
        self.assertIn("performance_metrics", health)
        self.assertGreaterEqual(health["health_score"], 0)
        self.assertLessEqual(health["health_score"], 100)

    def test_monitoring_system(self):
        """Test monitoring system functionality."""
        # Start monitoring
        self.monitor.start_monitoring()

        # Create some test data to monitor
        status_data = {
            "status": "active",
            "cycle_count": 1,
            "tasks_completed": 1,
            "coordination_efficiency": 0.8,
            "v2_compliance": 0.9,
        }
        self.integration.integrate_agent_status("test_agent", status_data)

        # Wait a moment for monitoring to collect data
        import time

        time.sleep(1)

        # Get monitoring dashboard
        dashboard = self.monitor.get_monitoring_dashboard()

        self.assertIsNotNone(dashboard)
        self.assertIn("timestamp", dashboard)
        self.assertIn("summary", dashboard)
        self.assertIn("monitoring_status", dashboard)

        # Stop monitoring
        self.monitor.stop_monitoring()

    def test_database_stats(self):
        """Test database statistics."""
        # Create test data
        for i in range(5):
            status_data = {
                "status": "active",
                "cycle_count": i,
                "tasks_completed": i,
                "coordination_efficiency": 0.8,
                "v2_compliance": 0.9,
            }
            self.integration.integrate_agent_status(f"agent_{i}", status_data)

        # Get database stats
        stats = self.integration.orchestrator.get_database_stats()

        self.assertIsNotNone(stats)
        self.assertIn("total_vectors", stats)
        self.assertIn("type_counts", stats)
        self.assertIn("agent_counts", stats)
        self.assertGreaterEqual(stats["total_vectors"], 5)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
