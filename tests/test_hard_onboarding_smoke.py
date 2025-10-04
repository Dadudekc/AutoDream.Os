#!/usr/bin/env python3
"""
Hard Onboarding Smoke Tests
===========================

CI-friendly smoke tests for hard onboarding integration system.
Tests database operations, task creation, and dry-run flows without PyAutoGUI.

V2 Compliance: ≤400 lines, focused test suite
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

import os
import sqlite3

# Add src to path for imports
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from integrations.hard_onboarding_bridge import (
    captain_hard_onboard,
    create_and_assign_onboarding,
    ensure_db,
    execute_hard_onboarding,
    get_onboarding_status,
    mark_onboarding_result,
)
from tools.cursor_task_database_integration import CursorTaskIntegrationManager


class TestHardOnboardingIntegration(unittest.TestCase):
    """Test hard onboarding integration components."""

    def setUp(self):
        """Set up test environment with temporary database."""
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Set environment variable for test database
        os.environ["TEST_DB_PATH"] = self.db_path

        # Initialize database
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            ensure_db()

    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary database file
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_database_schema_creation(self):
        """Test that database schema is created correctly."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # Check main tables exist
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]

            expected_tables = ["cursor_tasks_integrated", "scanner_tasks", "fsm_task_tracking"]

            for table in expected_tables:
                self.assertIn(table, tables, f"Table {table} should exist")

            # Check indexes exist
            cur.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indexes = [row[0] for row in cur.fetchall()]

            expected_indexes = ["idx_tasks_status", "idx_tasks_agent", "idx_fsm_state"]

            for index in expected_indexes:
                self.assertIn(index, indexes, f"Index {index} should exist")

    def test_create_and_assign_onboarding(self):
        """Test onboarding task creation and assignment."""
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            task_id = create_and_assign_onboarding("Agent-6", assigned_by="Captain")

            # Verify task was created
            self.assertIsNotNone(task_id)
            self.assertTrue(task_id.startswith("onboard_Agent-6_"))

            # Verify task in database
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT agent_id, status, fsm_state FROM cursor_tasks_integrated WHERE task_id = ?",
                    (task_id,),
                )
                result = cur.fetchone()

                self.assertIsNotNone(result)
                agent_id, status, fsm_state = result
                self.assertEqual(agent_id, "Agent-6")
                self.assertEqual(status, "ASSIGNED")
                self.assertEqual(fsm_state, "ACTIVE")

    def test_execute_hard_onboarding_dry_run(self):
        """Test hard onboarding execution in dry-run mode."""
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            result = execute_hard_onboarding("Agent-6", dry_run=True)

            # Verify dry-run result structure
            self.assertIsInstance(result, dict)
            self.assertIn("target_agent", result)
            self.assertIn("success", result)
            self.assertIn("dry_run", result)

            self.assertEqual(result["target_agent"], "Agent-6")
            self.assertTrue(result["dry_run"])

    def test_mark_onboarding_result(self):
        """Test marking onboarding task as completed/failed."""
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            # Create a task first
            task_id = create_and_assign_onboarding("Agent-6")

            # Mark as completed
            success = mark_onboarding_result(task_id, True, "Test completion")
            self.assertTrue(success)

            # Verify status update
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT status, fsm_state FROM cursor_tasks_integrated WHERE task_id = ?",
                    (task_id,),
                )
                result = cur.fetchone()

                self.assertIsNotNone(result)
                status, fsm_state = result
                self.assertEqual(status, "COMPLETED")
                self.assertEqual(fsm_state, "COMPLETED")

    def test_captain_hard_onboard_dry_run(self):
        """Test complete captain hard onboarding flow in dry-run mode."""
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            result = captain_hard_onboard("Agent-6", dry_run=True)

            # Verify result structure
            self.assertIsInstance(result, dict)
            self.assertIn("task_id", result)
            self.assertIn("agent_id", result)
            self.assertIn("success", result)
            self.assertIn("exec_result", result)
            self.assertIn("execution_orders", result)
            self.assertIn("dry_run", result)

            # Verify values
            self.assertEqual(result["agent_id"], "Agent-6")
            self.assertTrue(result["dry_run"])
            self.assertIsNotNone(result["task_id"])
            self.assertIsInstance(result["execution_orders"], dict)

    def test_get_onboarding_status(self):
        """Test getting onboarding status for an agent."""
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            # Create a task first
            task_id = create_and_assign_onboarding("Agent-6")

            # Get status
            status = get_onboarding_status("Agent-6")

            # Verify status structure
            self.assertIsInstance(status, dict)
            self.assertIn("agent_id", status)
            self.assertIn("onboarding_tasks", status)
            self.assertIn("latest_task", status)
            self.assertIn("fsm_state", status)

            # Verify values
            self.assertEqual(status["agent_id"], "Agent-6")
            self.assertEqual(status["onboarding_tasks"], 1)
            self.assertEqual(status["latest_task"], task_id)
            self.assertEqual(status["fsm_state"], "ACTIVE")

    def test_task_lifecycle_tracking(self):
        """Test complete task lifecycle from creation to completion."""
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            # Step 1: Create task
            task_id = create_and_assign_onboarding("Agent-6")

            # Step 2: Verify initial state
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT status, fsm_state FROM cursor_tasks_integrated WHERE task_id = ?",
                    (task_id,),
                )
                result = cur.fetchone()
                status, fsm_state = result
                self.assertEqual(status, "ASSIGNED")
                self.assertEqual(fsm_state, "ACTIVE")

            # Step 3: Mark as completed
            mark_onboarding_result(task_id, True, "Lifecycle test completion")

            # Step 4: Verify final state
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT status, fsm_state FROM cursor_tasks_integrated WHERE task_id = ?",
                    (task_id,),
                )
                result = cur.fetchone()
                status, fsm_state = result
                self.assertEqual(status, "COMPLETED")
                self.assertEqual(fsm_state, "COMPLETED")

    def test_error_handling(self):
        """Test error handling for invalid operations."""
        with patch("integrations.hard_onboarding_bridge.DB_PATH", self.db_path):
            # Test marking non-existent task
            success = mark_onboarding_result("nonexistent_task", True)
            self.assertFalse(success)

            # Test getting status for agent with no tasks
            status = get_onboarding_status("Agent-99")
            self.assertEqual(status["agent_id"], "Agent-99")
            self.assertEqual(status["onboarding_tasks"], 0)
            self.assertIsNone(status["latest_task"])


class TestCursorTaskIntegrationManager(unittest.TestCase):
    """Test CursorTaskIntegrationManager functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_manager_initialization(self):
        """Test manager initialization and database creation."""
        manager = CursorTaskIntegrationManager(self.db_path)

        # Verify database file exists
        self.assertTrue(os.path.exists(self.db_path))

        # Verify tables exist
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]

            self.assertIn("cursor_tasks_integrated", tables)
            self.assertIn("scanner_tasks", tables)
            self.assertIn("fsm_task_tracking", tables)

    def test_create_hard_onboarding_task(self):
        """Test hard onboarding task creation."""
        manager = CursorTaskIntegrationManager(self.db_path)

        task = manager.create_hard_onboarding_task("Agent-6")

        # Verify task properties
        self.assertIsNotNone(task.task_id)
        self.assertEqual(task.agent_id, "Agent-6")
        self.assertEqual(task.description, "Hard onboarding sequence for Agent-6")
        self.assertTrue(task.metadata["hard_onboard"])
        self.assertTrue(task.metadata["requires_pyautogui"])

    def test_execution_orders_generation(self):
        """Test captain execution orders generation."""
        manager = CursorTaskIntegrationManager(self.db_path)

        # Create some tasks
        manager.create_hard_onboarding_task("Agent-6")
        manager.create_hard_onboarding_task("Agent-7")

        orders = manager.generate_captain_execution_orders()

        # Verify orders structure
        self.assertIsInstance(orders, dict)
        self.assertIn("timestamp", orders)
        self.assertIn("active_tasks", orders)
        self.assertIn("agent_assignments", orders)
        self.assertIn("captain_directives", orders)

        # Verify task counts
        self.assertGreater(orders["active_tasks"], 0)
        self.assertIn("Agent-6", orders["agent_assignments"])
        self.assertIn("Agent-7", orders["agent_assignments"])


def run_smoke_tests():
    """Run all smoke tests and return results."""

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestHardOnboardingIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestCursorTaskIntegrationManager))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success/failure
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)
