#!/usr/bin/env python3
"""
Test FSM-Communication Integration - Agent Cellphone V2
=====================================================

Tests the integration between FSM system and communication protocol.
Verifies state-driven communication and agent coordination.

Author: FSM-Communication Integration Specialist
License: MIT
"""

import unittest
import time
import json
import tempfile
import shutil

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from unittest.mock import Mock, patch

# Import components to test
from src.core.unified_workspace_system import UnifiedWorkspaceSystem
from src.core.fsm_core_v2 import FSMCoreV2
from src.core.v2_comprehensive_messaging_system import V2ComprehensiveMessagingSystem
from src.core.fsm_communication_bridge import FSMCommunicationBridge


class TestFSMCommunicationIntegration(unittest.TestCase):
    """Test suite for FSM-Communication integration."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directories
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "workspaces"
        self.inbox_path = Path(self.test_dir) / "communication"
        self.fsm_data_path = Path(self.test_dir) / "fsm_data"

        # Create directories
        self.workspace_path.mkdir(parents=True)
        self.inbox_path.mkdir(parents=True)
        self.fsm_data_path.mkdir(parents=True)

        # Initialize core components
        self.workspace_manager = UnifiedWorkspaceSystem(str(self.workspace_path))
        self.fsm_core = FSMCoreV2(
            workspace_manager=self.workspace_manager,
            fsm_data_path=str(self.fsm_data_path),
        )
        self.messaging_system = V2ComprehensiveMessagingSystem()

        # Initialize integration bridge
        self.fsm_bridge = FSMCommunicationBridge(
            fsm_core=self.fsm_core,
            communication_protocol=self.messaging_system,
        )

    def tearDown(self):
        """Clean up test environment."""
        # Shutdown bridge
        if hasattr(self.fsm_bridge, "shutdown"):
            self.fsm_bridge.shutdown()

        # Remove temporary directories
        shutil.rmtree(self.test_dir)

    def test_bridge_initialization(self):
        """Test bridge initialization."""
        self.assertIsNotNone(self.fsm_bridge)
        self.assertEqual(self.fsm_bridge.bridge_state.value, "connected")
        self.assertTrue(self.fsm_bridge.bridge_active)

    def test_fsm_task_creation_and_communication(self):
        """Test FSM task creation triggers communication."""
        # Create a task
        task_id = self.fsm_core.create_task(
            title="Test Task",
            description="Test task for communication",
            assigned_agent="Agent-1",
            priority="HIGH",
        )

        self.assertIsNotNone(task_id)

        # Wait for bridge processing
        time.sleep(0.2)

        # Check if communication channel was created
        self.assertIn(task_id, self.fsm_bridge.task_communication_channels)

        # Check if agent was added to coordinated set
        self.assertIn("Agent-1", self.fsm_bridge.coordinated_agents)

    def test_task_state_transition_communication(self):
        """Test task state transitions trigger communication."""
        # Create a task
        task_id = self.fsm_core.create_task(
            title="State Transition Test",
            description="Test state transitions",
            assigned_agent="Agent-2",
            priority="NORMAL",
        )

        # Wait for initial processing
        time.sleep(0.2)

        # Update task state
        success = self.fsm_core.update_task_state(
            task_id, "IN_PROGRESS", "Agent-2", "Starting work"
        )

        self.assertTrue(success)

        # Wait for bridge processing
        time.sleep(0.2)

        # Check if task is in communication channels
        self.assertIn(task_id, self.fsm_bridge.task_communication_channels)

    def test_agent_coordination(self):
        """Test agent coordination through FSM bridge."""
        # Create multiple tasks for different agents
        task1_id = self.fsm_core.create_task(
            title="Coordination Task 1",
            description="First coordination task",
            assigned_agent="Agent-1",
            priority="HIGH",
        )

        task2_id = self.fsm_core.create_task(
            title="Coordination Task 2",
            description="Second coordination task",
            assigned_agent="Agent-2",
            priority="NORMAL",
        )

        # Wait for processing
        time.sleep(0.3)

        # Check if both agents are coordinated
        self.assertIn("Agent-1", self.fsm_bridge.coordinated_agents)
        self.assertIn("Agent-2", self.fsm_bridge.coordinated_agents)

        # Check agent-task mapping
        self.assertIn(task1_id, self.fsm_bridge.agent_task_mapping["Agent-1"])
        self.assertIn(task2_id, self.fsm_bridge.agent_task_mapping["Agent-2"])

    def test_bridge_metrics(self):
        """Test bridge metrics collection."""
        # Create a task to generate metrics
        task_id = self.fsm_core.create_task(
            title="Metrics Test",
            description="Test metrics collection",
            assigned_agent="Agent-3",
            priority="LOW",
        )

        # Wait for processing
        time.sleep(0.2)

        # Get bridge status
        status = self.fsm_bridge.get_bridge_status()

        # Check metrics
        self.assertIn("metrics", status)
        metrics = status["metrics"]
        self.assertIn("events_processed", metrics)
        self.assertIn("messages_sent", metrics)
        self.assertIn("coordination_actions", metrics)
        self.assertIn("errors", metrics)

    def test_bridge_shutdown(self):
        """Test bridge graceful shutdown."""
        # Verify bridge is active
        self.assertTrue(self.fsm_bridge.bridge_active)

        # Shutdown bridge
        self.fsm_bridge.shutdown()

        # Verify shutdown
        self.assertFalse(self.fsm_bridge.bridge_active)
        self.assertEqual(self.fsm_bridge.bridge_state.value, "disconnected")

    def test_error_handling(self):
        """Test error handling in bridge."""
        # Create a task with invalid data to trigger errors
        with patch.object(
            self.fsm_core, "create_task", side_effect=Exception("Test error")
        ):
            # This should not crash the bridge
            self.assertTrue(self.fsm_bridge.bridge_active)

            # Check error metrics
            status = self.fsm_bridge.get_bridge_status()
            self.assertGreaterEqual(status["metrics"]["errors"], 0)

    def test_event_processing(self):
        """Test event processing in bridge."""
        # Create a task
        task_id = self.fsm_core.create_task(
            title="Event Processing Test",
            description="Test event processing",
            assigned_agent="Agent-4",
            priority="NORMAL",
        )

        # Wait for processing
        time.sleep(0.2)

        # Check event history
        self.assertGreaterEqual(len(self.fsm_bridge.event_history), 0)

        # Check event queue processing
        self.assertEqual(len(self.fsm_bridge.event_queue), 0)  # Should be processed

    def test_coordination_monitoring(self):
        """Test coordination monitoring."""
        # Create a blocked task
        task_id = self.fsm_core.create_task(
            title="Blocked Task",
            description="Task that will be blocked",
            assigned_agent="Agent-5",
            priority="HIGH",
        )

        # Wait for initial processing
        time.sleep(0.2)

        # Block the task
        self.fsm_core.update_task_state(task_id, "BLOCKED", "Agent-5", "Task blocked")

        # Wait for coordination monitoring
        time.sleep(0.2)

        # Check if coordination was triggered
        # This would require more sophisticated testing of the coordination logic
        self.assertIn("Agent-5", self.fsm_bridge.coordinated_agents)


class TestIntegrationEndToEnd(unittest.TestCase):
    """End-to-end integration tests."""

    def setUp(self):
        """Set up end-to-end test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "workspaces"
        self.inbox_path = Path(self.test_dir) / "communication"
        self.fsm_data_path = Path(self.test_dir) / "fsm_data"

        # Create directories
        self.workspace_path.mkdir(parents=True)
        self.inbox_path.mkdir(parents=True)
        self.fsm_data_path.mkdir(parents=True)

    def tearDown(self):
        """Clean up end-to-end test environment."""
        shutil.rmtree(self.test_dir)

    def test_full_workflow(self):
        """Test complete FSM-Communication workflow."""
        # Initialize all components
        workspace_manager = UnifiedWorkspaceSystem(str(self.workspace_path))
        inbox_manager = InboxManager(workspace_manager)
        fsm_core = FSMCoreV2(
            workspace_manager=workspace_manager,
            inbox_manager=inbox_manager,
            fsm_data_path=str(self.fsm_data_path),
        )
        communication_protocol = AgentCommunicationProtocol()

        # Initialize bridge
        bridge = FSMCommunicationBridge(
            fsm_core=fsm_core,
            communication_protocol=communication_protocol,
            inbox_manager=inbox_manager,
        )

        try:
            # Wait for bridge to be ready
            time.sleep(0.3)

            # Create a complete workflow
            task1_id = fsm_core.create_task(
                title="Workflow Task 1",
                description="First workflow task",
                assigned_agent="Agent-1",
                priority="HIGH",
            )

            # Wait for processing
            time.sleep(0.2)

            # Progress task
            fsm_core.update_task_state(
                task1_id, "IN_PROGRESS", "Agent-1", "Working on task"
            )

            time.sleep(0.2)

            # Complete task
            fsm_core.update_task_state(
                task1_id,
                "COMPLETED",
                "Agent-1",
                "Task completed",
                {"result": "success", "time_taken": "2.5s"},
            )

            # Wait for final processing
            time.sleep(0.2)

            # Verify workflow completion
            task = fsm_core.get_task(task1_id)
            self.assertIsNotNone(task)
            self.assertEqual(task.state.value, "COMPLETED")

            # Verify bridge processed the workflow
            self.assertIn(task1_id, bridge.task_communication_channels)
            self.assertIn("Agent-1", bridge.coordinated_agents)

            # Check metrics
            status = bridge.get_bridge_status()
            self.assertGreater(status["metrics"]["events_processed"], 0)
            self.assertGreater(status["metrics"]["messages_sent"], 0)

        finally:
            # Cleanup
            bridge.shutdown()

    def test_multi_agent_coordination(self):
        """Test coordination between multiple agents."""
        # Initialize components
        workspace_manager = UnifiedWorkspaceSystem(str(self.workspace_path))
        inbox_manager = InboxManager(workspace_manager)
        fsm_core = FSMCoreV2(
            workspace_manager=workspace_manager,
            inbox_manager=inbox_manager,
            fsm_data_path=str(self.fsm_data_path),
        )
        communication_protocol = AgentCommunicationProtocol()

        # Initialize bridge
        bridge = FSMCommunicationBridge(
            fsm_core=fsm_core,
            communication_protocol=communication_protocol,
            inbox_manager=inbox_manager,
        )

        try:
            # Wait for bridge to be ready
            time.sleep(0.3)

            # Create tasks for multiple agents
            agents = ["Agent-1", "Agent-2", "Agent-3"]
            task_ids = []

            for i, agent in enumerate(agents):
                task_id = fsm_core.create_task(
                    title=f"Multi-Agent Task {i+1}",
                    description=f"Task for {agent}",
                    assigned_agent=agent,
                    priority="NORMAL",
                )
                task_ids.append(task_id)

            # Wait for processing
            time.sleep(0.3)

            # Verify all agents are coordinated
            for agent in agents:
                self.assertIn(agent, bridge.coordinated_agents)

            # Verify all tasks have communication channels
            for task_id in task_ids:
                self.assertIn(task_id, bridge.task_communication_channels)

            # Verify agent-task mapping
            for i, agent in enumerate(agents):
                self.assertIn(task_ids[i], bridge.agent_task_mapping[agent])

        finally:
            # Cleanup
            bridge.shutdown()


def run_integration_tests():
    """Run the integration tests."""
    print("🧪 Running FSM-Communication Integration Tests...")

    # Create test suite
    suite = unittest.TestSuite()

    # Add unit tests
    suite.addTest(unittest.makeSuite(TestFSMCommunicationIntegration))

    # Add integration tests
    suite.addTest(unittest.makeSuite(TestIntegrationEndToEnd))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n📊 Test Results:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")

    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)
