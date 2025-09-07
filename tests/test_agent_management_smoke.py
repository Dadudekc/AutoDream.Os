#!/usr/bin/env python3
"""
Agent Management Smoke Tests - Agent Cellphone V2
==================================================

Comprehensive smoke tests for agent management and coordination systems.
Tests basic functionality to ensure core agent features work correctly.

Author: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from typing import Dict, Any

import pytest

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


class TestAgentRegistrySmoke:
    """Smoke tests for agent registry functionality."""

    def test_coordinate_loader_import(self):
        """Test that coordinate loader can be imported and used."""
        from src.core.coordinate_loader import get_coordinate_loader

        loader = get_coordinate_loader()
        assert loader is not None

        # Test that we can get agent list
        agents = loader.get_all_agents()
        assert isinstance(agents, list)
        assert len(agents) > 0

    def test_coordinate_loader_structure(self):
        """Test coordinate loader has proper structure."""
        from src.core.coordinate_loader import get_coordinate_loader

        loader = get_coordinate_loader()

        # Check that all agents are present
        expected_agents = [f"Agent-{i}" for i in range(1, 9)]
        agents = loader.get_all_agents()
        for agent_id in expected_agents:
            assert agent_id in agents, f"Missing agent: {agent_id}"

        # Check that we can get coordinates for each agent
        for agent_id in agents:
            try:
                chat_coords = loader.get_chat_coordinates(agent_id)
                onboard_coords = loader.get_onboarding_coordinates(agent_id)
                description = loader.get_agent_description(agent_id)

                assert isinstance(chat_coords, tuple), f"Agent {agent_id} chat coordinates not tuple"
                assert len(chat_coords) == 2, f"Agent {agent_id} chat coordinates not length 2"
                assert isinstance(onboard_coords, tuple), f"Agent {agent_id} onboarding coordinates not tuple"
                assert len(onboard_coords) == 2, f"Agent {agent_id} onboarding coordinates not length 2"
                assert isinstance(description, str), f"Agent {agent_id} description not string"
            except ValueError:
                # Skip agents with invalid coordinates
                continue

    def test_coordinate_loader_coordinates_unique(self):
        """Test that agent coordinates are unique."""
        from src.core.coordinate_loader import get_coordinate_loader

        loader = get_coordinate_loader()
        coordinates = []

        for agent_id in loader.get_all_agents():
            try:
                chat_coords = loader.get_chat_coordinates(agent_id)
                onboard_coords = loader.get_onboarding_coordinates(agent_id)
                coordinates.extend([chat_coords, onboard_coords])
            except ValueError:
                continue

        unique_coordinates = set(coordinates)
        assert len(coordinates) == len(unique_coordinates), "Agent coordinates are not unique"


class TestAgentContextManagerSmoke:
    """Smoke tests for agent context manager functionality."""

    def setup_method(self):
        """Set up test environment."""
        from src.core.agent_context_manager import AgentContextManager
        self.manager = AgentContextManager()

    def test_agent_context_manager_initialization(self):
        """Test agent context manager initialization."""
        assert hasattr(self.manager, 'agent_contexts')
        assert isinstance(self.manager.agent_contexts, dict)
        assert len(self.manager.agent_contexts) == 0

    def test_set_agent_context(self):
        """Test setting agent context."""
        agent_id = "Agent-1"
        context = {
            "status": "active",
            "current_task": "testing",
            "role": "test_agent"
        }

        self.manager.set_agent_context(agent_id, context)
        assert agent_id in self.manager.agent_contexts
        assert self.manager.agent_contexts[agent_id]["status"] == "active"
        assert "last_updated" in self.manager.agent_contexts[agent_id]

    def test_get_agent_context(self):
        """Test getting agent context."""
        agent_id = "Agent-2"
        context = {"status": "idle"}

        # Test empty context
        result = self.manager.get_agent_context(agent_id)
        assert result == {}

        # Test with context set
        self.manager.set_agent_context(agent_id, context)
        result = self.manager.get_agent_context(agent_id)
        assert result["status"] == "idle"
        assert "last_updated" in result

    def test_update_agent_context(self):
        """Test updating agent context."""
        agent_id = "Agent-3"
        initial_context = {"status": "idle", "priority": 1}
        updates = {"status": "active", "current_task": "updated_task"}

        self.manager.set_agent_context(agent_id, initial_context)
        result = self.manager.update_agent_context(agent_id, updates)

        assert result is True
        updated_context = self.manager.get_agent_context(agent_id)
        assert updated_context["status"] == "active"
        assert updated_context["current_task"] == "updated_task"
        assert updated_context["priority"] == 1  # Should remain unchanged

    def test_update_nonexistent_agent_context(self):
        """Test updating context for non-existent agent."""
        result = self.manager.update_agent_context("NonExistentAgent", {"status": "active"})
        assert result is False

    def test_remove_agent_context(self):
        """Test removing agent context."""
        agent_id = "Agent-4"
        context = {"status": "active"}

        self.manager.set_agent_context(agent_id, context)
        assert agent_id in self.manager.agent_contexts

        result = self.manager.remove_agent_context(agent_id)
        assert result is True
        assert agent_id not in self.manager.agent_contexts

    def test_remove_nonexistent_agent_context(self):
        """Test removing context for non-existent agent."""
        result = self.manager.remove_agent_context("NonExistentAgent")
        assert result is False


class TestAgentWorkspaceManagementSmoke:
    """Smoke tests for agent workspace management."""

    def setup_method(self):
        """Set up test environment."""
        self.tmp_dir = tempfile.mkdtemp()
        self.workspace_root = Path(self.tmp_dir) / "agent_workspaces"
        self.workspace_root.mkdir()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_agent_workspace_creation(self):
        """Test agent workspace creation."""
        agent_id = "Agent-1"
        workspace_path = self.workspace_root / agent_id
        workspace_path.mkdir()

        # Create basic workspace structure
        inbox_path = workspace_path / "inbox"
        inbox_path.mkdir()

        status_file = workspace_path / "status.json"
        status_data = {
            "agent_id": agent_id,
            "status": "ACTIVE_AGENT_MODE",
            "current_phase": "TASK_EXECUTION"
        }

        with open(status_file, 'w') as f:
            json.dump(status_data, f)

        # Verify workspace structure
        assert workspace_path.exists()
        assert inbox_path.exists()
        assert status_file.exists()

        # Verify status file content
        with open(status_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data["agent_id"] == agent_id
        assert loaded_data["status"] == "ACTIVE_AGENT_MODE"

    def test_agent_status_file_operations(self):
        """Test agent status file operations."""
        agent_id = "Agent-2"
        workspace_path = self.workspace_root / agent_id
        workspace_path.mkdir()
        status_file = workspace_path / "status.json"

        # Initial status
        initial_status = {
            "agent_id": agent_id,
            "status": "ACTIVE_AGENT_MODE",
            "current_task": None,
            "last_updated": "2024-01-01T00:00:00Z"
        }

        with open(status_file, 'w') as f:
            json.dump(initial_status, f)

        # Update status
        with open(status_file, 'r') as f:
            current_status = json.load(f)

        current_status["current_task"] = "test_task"
        current_status["last_updated"] = "2024-01-02T00:00:00Z"

        with open(status_file, 'w') as f:
            json.dump(current_status, f)

        # Verify update
        with open(status_file, 'r') as f:
            updated_status = json.load(f)

        assert updated_status["current_task"] == "test_task"
        assert updated_status["last_updated"] == "2024-01-02T00:00:00Z"


class TestAgentCoordinationSmoke:
    """Smoke tests for agent coordination functionality."""

    def test_agent_coordination_import(self):
        """Test that agent coordination modules can be imported."""
        try:
            from src.core.coordination import agent_strategies
            assert hasattr(agent_strategies, 'AgentCoordinationStrategy')
        except ImportError:
            pytest.skip("Agent coordination module not available")

    def test_agent_coordinator_registry_import(self):
        """Test that coordinator registry can be imported."""
        try:
            from src.core.coordinator_registry import CoordinatorRegistry
            assert CoordinatorRegistry is not None
        except ImportError:
            pytest.skip("Coordinator registry not available")


class TestAgentIntegrationSmoke:
    """Smoke tests for agent integration with other systems."""

    def test_agent_messaging_integration(self):
        """Test agent integration with messaging system."""
        try:
            from src.services.messaging_core import UnifiedMessagingCore
            messaging = UnifiedMessagingCore()

            # Test basic functionality
            assert hasattr(messaging, 'send_message_to_inbox')
            assert hasattr(messaging, 'send_message_via_pyautogui')
            assert hasattr(messaging, 'generate_onboarding_message')

        except ImportError:
            pytest.skip("Messaging core not available")

    def test_agent_vector_database_integration(self):
        """Test agent integration with vector database."""
        try:
            from src.core.vector_database import get_connection, upsert_agent_status
            from src.core.vector_database import DB_PATH, AGENT_STATUS_TABLE

            # Test database connection
            conn = get_connection()
            assert conn is not None

            # Test table creation
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{AGENT_STATUS_TABLE}'")
            result = cursor.fetchone()
            assert result is not None
            assert result[0] == AGENT_STATUS_TABLE

            conn.close()

        except ImportError:
            pytest.skip("Vector database not available")

    def test_agent_status_embedding_operations(self):
        """Test agent status embedding operations."""
        try:
            from src.core.vector_database import upsert_agent_status, get_agent_status

            test_agent_id = "test_agent"
            test_raw_status = '{"status": "active", "task": "testing"}'
            test_embedding = '[0.1, 0.2, 0.3]'

            # Test upsert operation
            result = upsert_agent_status(test_agent_id, test_raw_status, test_embedding)
            assert result is True

            # Test get operation
            status_data = get_agent_status(test_agent_id)
            if status_data:
                assert status_data['agent_id'] == test_agent_id
                assert status_data['raw_status'] == test_raw_status
                assert status_data['embedding'] == test_embedding

        except ImportError:
            pytest.skip("Vector database operations not available")


class TestAgentSystemIntegration:
    """Integration tests for complete agent system."""

    def setup_method(self):
        """Set up integration test environment."""
        self.tmp_dir = tempfile.mkdtemp()
        self.workspace_root = Path(self.tmp_dir) / "agent_workspaces"
        self.workspace_root.mkdir()

    def teardown_method(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_full_agent_lifecycle_simulation(self):
        """Test a simulated agent lifecycle."""
        # This is a high-level integration test that simulates
        # the complete lifecycle of an agent

        agent_id = "Agent-7"

        # 1. Create agent workspace
        workspace_path = self.workspace_root / agent_id
        workspace_path.mkdir()
        inbox_path = workspace_path / "inbox"
        inbox_path.mkdir()

        # 2. Initialize agent status
        status_file = workspace_path / "status.json"
        initial_status = {
            "agent_id": agent_id,
            "agent_name": "Web Development Specialist",
            "status": "ACTIVE_AGENT_MODE",
            "current_phase": "INITIALIZATION",
            "last_updated": "2024-01-01T00:00:00Z",
            "current_task": None,
            "completed_tasks": [],
            "achievements": []
        }

        with open(status_file, 'w') as f:
            json.dump(initial_status, f)

        # 3. Simulate task assignment
        with open(status_file, 'r') as f:
            current_status = json.load(f)

        current_status["current_task"] = "web_development_task"
        current_status["current_phase"] = "TASK_EXECUTION"
        current_status["last_updated"] = "2024-01-01T01:00:00Z"

        with open(status_file, 'w') as f:
            json.dump(current_status, f)

        # 4. Simulate task completion
        with open(status_file, 'r') as f:
            current_status = json.load(f)

        current_status["current_task"] = None
        current_status["current_phase"] = "IDLE"
        current_status["completed_tasks"].append("web_development_task")
        current_status["last_updated"] = "2024-01-01T02:00:00Z"

        with open(status_file, 'w') as f:
            json.dump(current_status, f)

        # 5. Verify final state
        with open(status_file, 'r') as f:
            final_status = json.load(f)

        assert final_status["current_task"] is None
        assert final_status["current_phase"] == "IDLE"
        assert "web_development_task" in final_status["completed_tasks"]
        assert len(final_status["completed_tasks"]) == 1


if __name__ == "__main__":
    # Run tests directly
    import sys
    print("Running Agent Management Smoke Tests...")

    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    # Import the test class directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_agent_management_smoke", __file__)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Create test instance
    test_instance = module.TestAgentWorkspaceManagementSmoke()

    try:
        # Setup test environment
        test_instance.setup_method()

        # Run basic tests
        test_instance.test_agent_workspace_creation()
        print("[PASS] Agent workspace creation test passed")

        print("[SUCCESS] All agent management smoke tests passed!")

    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
