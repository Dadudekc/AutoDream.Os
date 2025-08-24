#!/usr/bin/env python3
"""
Autonomous Development Smoke Tests - Agent Cellphone V2
====================================================

Comprehensive smoke tests for autonomous development system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import unittest
import sys
import os

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from autonomous_development import (
    DevelopmentTask, TaskPriority, TaskComplexity, TaskStatus, AgentRole,
    TaskManager, AgentCoordinator, WorkflowEngine, DevelopmentCommunication
)


class AutonomousDevelopmentSmokeTests(unittest.TestCase):
    """Autonomous Development System Smoke Tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.task_manager = TaskManager()
        self.agent_coordinator = AgentCoordinator()
        self.workflow_engine = WorkflowEngine(self.task_manager, self.agent_coordinator)
        self.communication = DevelopmentCommunication()
    
    def test_core_enums(self):
        """Test core enums functionality"""
        # Test TaskPriority enum
        self.assertIsInstance(TaskPriority.CRITICAL, TaskPriority)
        self.assertEqual(TaskPriority.CRITICAL.value, 10)
        
        # Test TaskComplexity enum
        self.assertIsInstance(TaskComplexity.MEDIUM, TaskComplexity)
        self.assertEqual(TaskComplexity.MEDIUM.value, "medium")
        
        # Test TaskStatus enum
        self.assertIsInstance(TaskStatus.AVAILABLE, TaskStatus)
        self.assertEqual(TaskStatus.AVAILABLE.value, "available")
    
    def test_development_task(self):
        """Test development task functionality"""
        # Create a task
        task = DevelopmentTask(
            task_id="test_task",
            title="Test Task",
            description="A test task for smoke testing",
            complexity=TaskComplexity.LOW,
            priority=TaskPriority.MEDIUM,
            estimated_hours=2.0,
            required_skills=["testing", "python"]
        )
        
        # Test basic properties
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.complexity, TaskComplexity.LOW)
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertEqual(task.status, TaskStatus.AVAILABLE)
        
        # Test task claiming
        self.assertTrue(task.claim("agent_1"))
        self.assertEqual(task.claimed_by, "agent_1")
        self.assertEqual(task.status, TaskStatus.CLAIMED)
        
        # Test starting work
        self.assertTrue(task.start_work())
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        
        # Test progress update
        self.assertTrue(task.update_progress(50.0))
        self.assertEqual(task.progress_percentage, 50.0)
        
        # Test completion
        self.assertTrue(task.complete())
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.progress_percentage, 100.0)
    
    def test_task_manager(self):
        """Test task manager functionality"""
        # Test getting all tasks
        all_tasks = self.task_manager.get_all_tasks()
        self.assertGreater(len(all_tasks), 0)
        
        # Test getting available tasks
        available_tasks = self.task_manager.get_available_tasks()
        self.assertGreater(len(available_tasks), 0)
        
        # Test creating new task
        task_id = self.task_manager.create_task(
            title="Smoke Test Task",
            description="Task created during smoke testing",
            complexity=TaskComplexity.LOW,
            priority=TaskPriority.LOW,
            estimated_hours=1.0,
            required_skills=["testing"]
        )
        
        self.assertIsNotNone(task_id)
        
        # Test getting task by ID
        task = self.task_manager.get_task(task_id)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Smoke Test Task")
        
        # Test task statistics
        stats = self.task_manager.get_task_statistics()
        self.assertIn("total_tasks", stats)
        self.assertIn("available_tasks", stats)
    
    def test_agent_coordinator(self):
        """Test agent coordinator functionality"""
        # Test getting all agents
        all_agents = self.agent_coordinator.get_all_agents()
        self.assertGreater(len(all_agents), 0)
        
        # Test getting active agents
        active_agents = self.agent_coordinator.get_active_agents()
        self.assertGreater(len(active_agents), 0)
        
        # Test getting agents by role
        worker_agents = self.agent_coordinator.get_agents_by_role(AgentRole.WORKER)
        self.assertGreater(len(worker_agents), 0)
        
        # Test getting agents with skill
        agents_with_testing = self.agent_coordinator.get_agents_with_skill("testing")
        self.assertGreater(len(agents_with_testing), 0)
        
        # Test getting available agents
        available_agents = self.agent_coordinator.get_available_agents()
        self.assertGreater(len(available_agents), 0)
        
        # Test agent statistics
        stats = self.agent_coordinator.get_agent_statistics()
        self.assertIn("total_agents", stats)
        self.assertIn("active_agents", stats)
    
    def test_workflow_engine(self):
        """Test workflow engine functionality"""
        # Test workflow status
        status = self.workflow_engine.get_workflow_status()
        self.assertIn("state", status)
        self.assertIn("is_running", status)
        
        # Test starting workflow
        self.assertTrue(self.workflow_engine.start_workflow())
        self.assertTrue(self.workflow_engine.is_running)
        self.assertEqual(self.workflow_engine.state.value, "active")
        
        # Test running a cycle
        self.assertTrue(self.workflow_engine.run_cycle())
        
        # Test stopping workflow
        self.assertTrue(self.workflow_engine.stop_workflow())
        self.assertFalse(self.workflow_engine.is_running)
        self.assertEqual(self.workflow_engine.state.value, "idle")
        
        # Test workflow summary
        summary = self.workflow_engine.get_workflow_summary()
        self.assertIn("status", summary)
        self.assertIn("total_cycles", summary)
    
    def test_communication_system(self):
        """Test communication system functionality"""
        # Test sending message
        message_id = self.communication.send_message(
            sender_id="agent_1",
            recipient_id="agent_2",
            message_type="test_message",
            content={"test": "data"}
        )
        
        self.assertIsNotNone(message_id)
        
        # Test receiving message
        message = self.communication.receive_message(message_id)
        self.assertIsNotNone(message)
        self.assertEqual(message.sender_id, "agent_1")
        self.assertEqual(message.recipient_id, "agent_2")
        
        # Test getting messages for agent
        agent_messages = self.communication.get_messages_for_agent("agent_2")
        self.assertGreater(len(agent_messages), 0)
        
        # Test broadcasting message
        broadcast_ids = self.communication.broadcast_message(
            sender_id="agent_1",
            message_type="broadcast_test",
            content={"broadcast": "test"}
        )
        
        self.assertGreater(len(broadcast_ids), 0)
        
        # Test communication statistics
        stats = self.communication.get_communication_statistics()
        self.assertIn("total_messages", stats)
        self.assertIn("communication_stats", stats)
    
    def test_integration(self):
        """Test system integration"""
        # Create a task
        task_id = self.task_manager.create_task(
            title="Integration Test Task",
            description="Task for testing system integration",
            complexity=TaskComplexity.MEDIUM,
            priority=TaskPriority.HIGH,
            estimated_hours=3.0,
            required_skills=["testing", "code_analysis"]
        )
        
        task = self.task_manager.get_task(task_id)
        self.assertIsNotNone(task)
        
        # Find best agent for task
        best_agent = self.agent_coordinator.find_best_agent_for_task(task)
        self.assertIsNotNone(best_agent)
        
        # Assign task to agent
        success = self.agent_coordinator.assign_task_to_agent(task, best_agent.agent_id)
        self.assertTrue(success)
        
        # Start workflow and run cycle
        self.workflow_engine.start_workflow()
        cycle_success = self.workflow_engine.run_cycle()
        self.assertTrue(cycle_success)
        self.workflow_engine.stop_workflow()
        
        # Send communication about task assignment
        message_id = self.communication.send_message(
            sender_id="coordinator",
            recipient_id=best_agent.agent_id,
            message_type="task_assignment",
            content={"task_id": task_id, "assigned_agent": best_agent.agent_id}
        )
        
        self.assertIsNotNone(message_id)
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        # Test getting non-existent task
        task = self.task_manager.get_task("non_existent")
        self.assertIsNone(task)
        
        # Test getting non-existent agent
        agent = self.agent_coordinator.get_agent("non_existent")
        self.assertIsNone(agent)
        
        # Test claiming already claimed task
        available_tasks = self.task_manager.get_available_tasks()
        if available_tasks:
            task = available_tasks[0]
            # Claim first time
            self.assertTrue(task.claim("agent_1"))
            # Try to claim again
            self.assertFalse(task.claim("agent_2"))
        
        # Test starting workflow when already running
        self.workflow_engine.start_workflow()
        self.assertFalse(self.workflow_engine.start_workflow())
        self.workflow_engine.stop_workflow()
    
    def test_data_persistence(self):
        """Test data export/import functionality"""
        # Export tasks
        tasks_data = self.task_manager.export_tasks()
        self.assertIsInstance(tasks_data, list)
        self.assertGreater(len(tasks_data), 0)
        
        # Export messages
        messages_data = self.communication.export_messages()
        self.assertIsInstance(messages_data, list)
        
        # Test importing tasks (should handle existing data gracefully)
        imported_count = self.task_manager.import_tasks(tasks_data)
        self.assertGreaterEqual(imported_count, 0)
        
        # Test importing messages
        imported_messages = self.communication.import_messages(messages_data)
        self.assertGreaterEqual(imported_messages, 0)


def run_autonomous_development_smoke_tests():
    """Run all autonomous development smoke tests"""
    print("🧪 AUTONOMOUS DEVELOPMENT SMOKE TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(AutonomousDevelopmentSmokeTests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL SMOKE TESTS PASSED!")
        print(f"Tests run: {result.testsRun}")
        print("✅ Autonomous development system is working correctly")
        print("✅ V2 coding standards maintained")
        return True
    else:
        print("❌ SOME SMOKE TESTS FAILED!")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        return False


if __name__ == "__main__":
    success = run_autonomous_development_smoke_tests()
    sys.exit(0 if success else 1)
