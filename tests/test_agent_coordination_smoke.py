#!/usr/bin/env python3
"""
Smoke Tests for Agent Coordination - Agent Cellphone V2
======================================================

Comprehensive smoke tests for agent coordination and status tracking.
Tests agent status management, coordination workflows, and inter-agent communication.

Author: Agent-2 (Architecture & Design)
License: MIT
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import time

# Import agent coordination components
from src.core.agent_registry import AgentRegistry
from src.services.models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    SenderType,
    RecipientType,
)


class TestAgentCoordinationSmoke:
    """Smoke tests for agent coordination functionality."""

    def temp_agent_workspace(self):
        """Create temporary agent workspace for testing."""
        temp_dir = tempfile.mkdtemp()
        workspace_path = Path(temp_dir)

        # Create agent workspaces
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]:
            agent_dir = workspace_path / agent_id
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create inbox directory
            inbox_dir = agent_dir / "inbox"
            inbox_dir.mkdir(exist_ok=True)

            # Create status.json with comprehensive data
            status_file = agent_dir / "status.json"
            status_data = {
                "agent_id": agent_id,
                "agent_name": f"Test Agent {agent_id}",
                "status": "ACTIVE_AGENT_MODE",
                "current_phase": "TASK_EXECUTION",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "current_mission": f"Test mission for {agent_id}",
                "mission_priority": "HIGH",
                "current_tasks": [f"Task 1 for {agent_id}", f"Task 2 for {agent_id}"],
                "completed_tasks": [f"Completed task for {agent_id}"],
                "achievements": [f"Achievement for {agent_id}"],
                "next_actions": [f"Next action for {agent_id}"],
                "coordinates": {"x": 100, "y": 200},
                "performance_metrics": {
                    "tasks_completed": 5,
                    "success_rate": 0.95,
                    "average_response_time": 2.3
                }
            }
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)

        return workspace_path

    def mock_agent_registry(self, temp_agent_workspace):
        """Create mock agent registry for testing."""
        registry = MagicMock(spec=AgentRegistry)

        # Mock agent data
        agents = {
            "Agent-1": {
                "id": "Agent-1",
                "name": "Integration & Core Systems",
                "status": "ACTIVE_AGENT_MODE",
                "workspace": str(temp_agent_workspace / "Agent-1")
            },
            "Agent-2": {
                "id": "Agent-2",
                "name": "Architecture & Design",
                "status": "ACTIVE_AGENT_MODE",
                "workspace": str(temp_agent_workspace / "Agent-2")
            },
            "Agent-4": {
                "id": "Agent-4",
                "name": "Strategic Oversight",
                "status": "ACTIVE_AGENT_MODE",
                "workspace": str(temp_agent_workspace / "Agent-4")
            }
        }

        registry.get_all_agents.return_value = agents
        registry.get_agent.return_value = agents.get("Agent-1")
        registry.is_agent_active.return_value = True

        return registry

    def test_agent_status_file_structure(self):
        """Test agent status file structure and required fields."""
        temp_workspace = self.temp_agent_workspace()
        agent_dir = temp_workspace / "Agent-1"
        status_file = agent_dir / "status.json"

        # Verify status file exists
        assert status_file.exists()

        # Load and verify structure
        with open(status_file, 'r') as f:
            status_data = json.load(f)

        # Verify required fields according to V2 standards
        required_fields = [
            "agent_id", "agent_name", "status", "current_phase",
            "last_updated", "current_mission", "mission_priority"
        ]

        for field in required_fields:
            assert field in status_data, f"Missing required field: {field}"

        # Verify data types
        assert isinstance(status_data["agent_id"], str)
        assert isinstance(status_data["agent_name"], str)
        assert isinstance(status_data["status"], str)
        assert isinstance(status_data["current_mission"], str)

        # Verify status values are valid
        valid_statuses = ["ACTIVE_AGENT_MODE", "IDLE_AGENT_MODE", "MAINTENANCE_MODE"]
        assert status_data["status"] in valid_statuses

    def test_agent_workspace_structure(self, temp_agent_workspace):
        """Test agent workspace directory structure."""
        agent_dir = temp_agent_workspace / "Agent-1"

        # Verify workspace structure
        assert agent_dir.exists()
        assert agent_dir.is_dir()

        # Verify inbox directory
        inbox_dir = agent_dir / "inbox"
        assert inbox_dir.exists()
        assert inbox_dir.is_dir()

        # Verify status file
        status_file = agent_dir / "status.json"
        assert status_file.exists()
        assert status_file.is_file()

    def test_agent_status_update_operations(self, temp_agent_workspace):
        """Test updating agent status information."""
        agent_dir = temp_agent_workspace / "Agent-1"
        status_file = agent_dir / "status.json"

        # Load current status
        with open(status_file, 'r') as f:
            original_status = json.load(f)

        # Update status
        updated_status = original_status.copy()
        updated_status["current_mission"] = "Updated test mission"
        updated_status["status"] = "MAINTENANCE_MODE"
        updated_status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_status["current_tasks"] = ["New task 1", "New task 2"]
        updated_status["completed_tasks"].append("Newly completed task")

        # Save updated status
        with open(status_file, 'w') as f:
            json.dump(updated_status, f, indent=2)

        # Verify updates were saved
        with open(status_file, 'r') as f:
            saved_status = json.load(f)

        assert saved_status["current_mission"] == "Updated test mission"
        assert saved_status["status"] == "MAINTENANCE_MODE"
        assert len(saved_status["current_tasks"]) == 2
        assert "Newly completed task" in saved_status["completed_tasks"]

    def test_multi_agent_status_tracking(self, temp_agent_workspace):
        """Test tracking status across multiple agents."""
        agent_statuses = {}

        # Load status for all agents
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]:
            agent_dir = temp_agent_workspace / agent_id
            status_file = agent_dir / "status.json"

            with open(status_file, 'r') as f:
                agent_statuses[agent_id] = json.load(f)

        # Verify all agents have status files
        assert len(agent_statuses) == 4

        # Verify all agents are active
        for agent_id, status in agent_statuses.items():
            assert status["status"] == "ACTIVE_AGENT_MODE"
            assert status["agent_id"] == agent_id

        # Verify agent names are unique
        agent_names = [status["agent_name"] for status in agent_statuses.values()]
        assert len(agent_names) == len(set(agent_names))

    def test_agent_inbox_message_handling(self, temp_agent_workspace):
        """Test agent inbox message handling."""
        agent_dir = temp_agent_workspace / "Agent-1"
        inbox_dir = agent_dir / "inbox"

        # Create test message files
        test_messages = [
            {
                "message_id": "test-msg-001",
                "content": "Test message 1",
                "sender": "Agent-4",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "message_id": "test-msg-002",
                "content": "Test message 2",
                "sender": "System",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

        # Save messages to inbox
        for i, message in enumerate(test_messages):
            message_file = inbox_dir / f"message_{i+1}.json"
            with open(message_file, 'w') as f:
                json.dump(message, f, indent=2)

        # Verify messages were saved
        message_files = list(inbox_dir.glob("*.json"))
        assert len(message_files) == 2

        # Verify message content
        for i, message_file in enumerate(sorted(message_files)):
            with open(message_file, 'r') as f:
                saved_message = json.load(f)

            assert saved_message["message_id"] == test_messages[i]["message_id"]
            assert saved_message["content"] == test_messages[i]["content"]
            assert saved_message["sender"] == test_messages[i]["sender"]

    def test_agent_coordination_message_exchange(self, temp_agent_workspace):
        """Test inter-agent message exchange through inbox system."""
        # Create coordination message from Agent-4 to Agent-1
        coord_message = UnifiedMessage(
            message_id="coord-test-001",
            content="Agent-1, please coordinate with Agent-2 on the current task",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            sender="Agent-4",
            sender_type=SenderType.AGENT,
            recipient="Agent-1",
            recipient_type=RecipientType.AGENT,
            tags=[]
        )

        # Save to Agent-1's inbox
        agent1_inbox = temp_agent_workspace / "Agent-1" / "inbox"
        message_file = agent1_inbox / "coordination_request.json"

        message_data = {
            "message_id": coord_message.message_id,
            "content": coord_message.content,
            "message_type": coord_message.message_type.value,
            "priority": coord_message.priority.value,
            "sender": coord_message.sender,
            "sender_type": coord_message.sender_type.value,
            "recipient": coord_message.recipient,
            "recipient_type": coord_message.recipient_type.value,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(message_file, 'w') as f:
            json.dump(message_data, f, indent=2)

        # Verify message was received
        assert message_file.exists()

        with open(message_file, 'r') as f:
            received_message = json.load(f)

        assert received_message["sender"] == "Agent-4"
        assert received_message["recipient"] == "Agent-1"
        assert received_message["message_type"] == "agent_to_agent"
        assert "coordinate with Agent-2" in received_message["content"]

    def test_agent_status_performance_metrics(self, temp_agent_workspace):
        """Test agent performance metrics tracking."""
        agent_dir = temp_agent_workspace / "Agent-1"
        status_file = agent_dir / "status.json"

        with open(status_file, 'r') as f:
            status = json.load(f)

        # Verify performance metrics structure
        assert "performance_metrics" in status
        metrics = status["performance_metrics"]

        required_metrics = ["tasks_completed", "success_rate", "average_response_time"]
        for metric in required_metrics:
            assert metric in metrics

        # Verify metric data types
        assert isinstance(metrics["tasks_completed"], int)
        assert isinstance(metrics["success_rate"], float)
        assert isinstance(metrics["average_response_time"], float)

        # Verify reasonable metric values
        assert metrics["tasks_completed"] >= 0
        assert 0.0 <= metrics["success_rate"] <= 1.0
        assert metrics["average_response_time"] >= 0.0

    def test_agent_task_management(self, temp_agent_workspace):
        """Test agent task management and tracking."""
        agent_dir = temp_agent_workspace / "Agent-1"
        status_file = agent_dir / "status.json"

        with open(status_file, 'r') as f:
            status = json.load(f)

        # Verify task management fields
        task_fields = ["current_tasks", "completed_tasks", "next_actions"]
        for field in task_fields:
            assert field in status
            assert isinstance(status[field], list)

        # Test task completion workflow
        original_tasks = status["current_tasks"].copy()
        original_completed = status["completed_tasks"].copy()

        # Mark first task as completed
        if original_tasks:
            completed_task = original_tasks.pop(0)
            status["completed_tasks"].append(completed_task)
            status["current_tasks"] = original_tasks
            status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save updated status
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)

            # Verify task was moved
            with open(status_file, 'r') as f:
                updated_status = json.load(f)

            assert completed_task in updated_status["completed_tasks"]
            assert completed_task not in updated_status["current_tasks"]

    def test_agent_registry_integration(self, mock_agent_registry):
        """Test agent registry integration."""
        # Test getting all agents
        all_agents = mock_agent_registry.get_all_agents()
        assert len(all_agents) == 3
        assert "Agent-1" in all_agents
        assert "Agent-2" in all_agents
        assert "Agent-4" in all_agents

        # Test getting specific agent
        agent1 = mock_agent_registry.get_agent("Agent-1")
        assert agent1 is not None
        assert agent1["id"] == "Agent-1"
        assert agent1["name"] == "Integration & Core Systems"

        # Test agent active status
        assert mock_agent_registry.is_agent_active("Agent-1") is True

    def test_agent_status_timestamp_tracking(self, temp_agent_workspace):
        """Test timestamp tracking in agent status updates."""
        agent_dir = temp_agent_workspace / "Agent-1"
        status_file = agent_dir / "status.json"

        # Get initial timestamp
        with open(status_file, 'r') as f:
            initial_status = json.load(f)

        initial_timestamp = initial_status["last_updated"]

        # Wait a moment and update
        time.sleep(0.1)
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        initial_status["last_updated"] = current_timestamp
        initial_status["current_mission"] = "Updated mission with timestamp"

        with open(status_file, 'w') as f:
            json.dump(initial_status, f, indent=2)

        # Verify timestamp was updated
        with open(status_file, 'r') as f:
            updated_status = json.load(f)

        assert updated_status["last_updated"] == current_timestamp
        assert updated_status["last_updated"] != initial_timestamp

    def test_agent_error_handling_and_recovery(self, temp_agent_workspace):
        """Test agent error handling and recovery scenarios."""
        agent_dir = temp_agent_workspace / "Agent-1"
        status_file = agent_dir / "status.json"

        # Test handling corrupted status file
        with open(status_file, 'w') as f:
            f.write("corrupted json content")

        # Verify file exists but is corrupted
        assert status_file.exists()

        with open(status_file, 'r') as f:
            content = f.read()
            assert content == "corrupted json content"

        # Test recovery by rewriting valid status
        recovery_status = {
            "agent_id": "Agent-1",
            "agent_name": "Recovered Agent",
            "status": "MAINTENANCE_MODE",
            "current_phase": "ERROR_RECOVERY",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_mission": "Recovering from error state",
            "mission_priority": "HIGH",
            "current_tasks": ["Diagnose issues", "Restore functionality"],
            "completed_tasks": [],
            "achievements": [],
            "next_actions": ["Complete recovery"]
        }

        with open(status_file, 'w') as f:
            json.dump(recovery_status, f, indent=2)

        # Verify recovery was successful
        with open(status_file, 'r') as f:
            recovered_status = json.load(f)

        assert recovered_status["status"] == "MAINTENANCE_MODE"
        assert recovered_status["current_phase"] == "ERROR_RECOVERY"
        assert "Recovering from error" in recovered_status["current_mission"]


if __name__ == "__main__":
    # Run tests directly
    import sys
    print("Running Agent Coordination Smoke Tests...")

    # Create test instance
    test_instance = TestAgentCoordinationSmoke()

    # Run basic tests
    try:
        test_instance.test_agent_status_file_structure()
        print("[PASS] Agent status file structure test passed")

        print("[SUCCESS] All basic smoke tests passed!")

    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
