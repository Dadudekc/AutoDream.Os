#!/usr/bin/env python3
"""
Full Sprint Integration Test - Agent Cellphone V2
================================================

End-to-end test of the sprint integration system.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os
import json

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.launchers.sprint_management_launcher import (
    SprintManagementLauncher,
    SprintLaunchConfig,
)


class TestFullSprintIntegration(unittest.TestCase):
    """Test full sprint integration end-to-end."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "agent_workspaces"
        self.workspace_path.mkdir(parents=True, exist_ok=True)

        # Initialize launcher
        self.launcher = SprintManagementLauncher()

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def test_full_sprint_lifecycle(self):
        """Test complete sprint lifecycle from creation to completion."""
        # Step 1: Create sprint
        create_config = SprintLaunchConfig(
            mode="create", sprint_id="Integration-Test-Sprint", duration_days=7
        )

        success = self.launcher.launch(create_config)
        self.assertTrue(success, "Sprint creation failed")

        # Step 2: Plan sprint with 8 tasks (under 10 limit)
        plan_config = SprintLaunchConfig(
            mode="plan",
            sprint_id="Integration-Test-Sprint",
            task_ids=[f"task_{i}" for i in range(8)],
        )

        success = self.launcher.launch(plan_config)
        self.assertTrue(success, "Sprint planning failed")

        # Step 3: Start sprint
        start_config = SprintLaunchConfig(
            mode="start", sprint_id="Integration-Test-Sprint"
        )

        success = self.launcher.launch(start_config)
        self.assertTrue(success, "Sprint start failed")

        # Step 4: Update daily progress
        progress_config = SprintLaunchConfig(
            mode="progress", sprint_id="Integration-Test-Sprint"
        )

        success = self.launcher.launch(progress_config)
        self.assertTrue(success, "Progress update failed")

        # Step 5: Complete sprint
        complete_config = SprintLaunchConfig(
            mode="complete", sprint_id="Integration-Test-Sprint"
        )

        success = self.launcher.launch(complete_config)
        self.assertTrue(success, "Sprint completion failed")

        # Step 6: Check final status
        status_config = SprintLaunchConfig(
            mode="status", sprint_id="Integration-Test-Sprint"
        )

        success = self.launcher.launch(status_config)
        self.assertTrue(success, "Status check failed")

    def test_sprint_10_task_limit_enforcement(self):
        """Test that the 10-task limit is properly enforced."""
        # Create sprint
        create_config = SprintLaunchConfig(mode="create", sprint_id="Limit-Test-Sprint")

        success = self.launcher.launch(create_config)
        self.assertTrue(success, "Sprint creation failed")

        # Try to plan 12 tasks (should fail due to 10-task limit)
        plan_config = SprintLaunchConfig(
            mode="plan",
            sprint_id="Limit-Test-Sprint",
            task_ids=[f"task_{i}" for i in range(12)],
        )

        success = self.launcher.launch(plan_config)
        self.assertFalse(success, "Sprint planning should fail with >10 tasks")

    def test_sprint_workflow_stages(self):
        """Test that workflow stages progress correctly."""
        # Create sprint
        create_config = SprintLaunchConfig(
            mode="create", sprint_id="Workflow-Test-Sprint"
        )

        success = self.launcher.launch(create_config)
        self.assertTrue(success, "Sprint creation failed")

        # Check initial status
        status_config = SprintLaunchConfig(
            mode="status", sprint_id="Workflow-Test-Sprint"
        )

        success = self.launcher.launch(status_config)
        self.assertTrue(success, "Status check failed")

        # Plan tasks
        plan_config = SprintLaunchConfig(
            mode="plan",
            sprint_id="Workflow-Test-Sprint",
            task_ids=["task1", "task2", "task3"],
        )

        success = self.launcher.launch(plan_config)
        self.assertTrue(success, "Sprint planning failed")

        # Start sprint
        start_config = SprintLaunchConfig(
            mode="start", sprint_id="Workflow-Test-Sprint"
        )

        success = self.launcher.launch(start_config)
        self.assertTrue(success, "Sprint start failed")

        # Final status check
        success = self.launcher.launch(status_config)
        self.assertTrue(success, "Final status check failed")

    def test_sprint_data_persistence(self):
        """Test that sprint data is properly persisted."""
        # Create sprint
        create_config = SprintLaunchConfig(
            mode="create", sprint_id="Persistence-Test-Sprint"
        )

        success = self.launcher.launch(create_config)
        self.assertTrue(success, "Sprint creation failed")

        # Check that sprint file exists
        sprints_path = self.launcher.sprint_manager.workspace_manager.get_sprints_path()
        sprint_files = list(sprints_path.glob("*.json"))
        self.assertGreater(len(sprint_files), 0, "Sprint file should be created")

        # Verify sprint data in file
        sprint_file = sprint_files[0]
        with open(sprint_file, "r") as f:
            sprint_data = json.load(f)

        self.assertEqual(sprint_data["name"], "Persistence-Test-Sprint")
        self.assertEqual(sprint_data["max_tasks"], 10)
        self.assertEqual(sprint_data["status"], "planning")


def run_integration_tests():
    """Run the integration tests and return results."""
    print("🧪 Running Full Sprint Integration Tests...")

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFullSprintIntegration)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n📊 Test Results Summary:")
    print(f"  Tests Run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(
        f"  Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%"
    )

    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")

    if result.errors:
        print(f"\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
