from pathlib import Path
import json
import shutil
import tempfile

import unittest

from src.core.fsm import FSMSystemManager
from src.core.v2_comprehensive_messaging_system import (
from src.core.v2_onboarding_sequence import (
from src.utils.stability_improvements import stability_manager, safe_import
from unittest.mock import Mock, patch, MagicMock
import time

#!/usr/bin/env python3
"""
Test V2 Onboarding Sequence - Agent Cellphone V2
===============================================

Tests the V2 onboarding sequence integration with real agent communication.
Follows V2 standards: ≤300 LOC, comprehensive testing.

Author: V2 Testing & Validation Specialist
License: MIT
"""



# Import components to test
    V2OnboardingSequence,
    OnboardingStatus,
    OnboardingPhase,
    OnboardingSession,
    OnboardingMessage,
)
    V2ComprehensiveMessagingSystem,
    V2MessageType,
    V2MessagePriority,
)


class TestV2OnboardingSequence(unittest.TestCase):
    """Test suite for V2 Onboarding Sequence"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            "phase_timeout": 10,  # Short timeout for testing
            "validation_retries": 2,
            "performance_thresholds": {"response_time": 5, "comprehension_score": 0.8},
        }

        # Create temporary directories
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "workspaces"
        self.fsm_data_path = Path(self.test_dir) / "fsm_data"
        self.inbox_path = Path(self.test_dir) / "communication"

        # Create directories
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        self.fsm_data_path.mkdir(parents=True, exist_ok=True)
        self.inbox_path.mkdir(parents=True, exist_ok=True)

        # Mock components
        self.mock_communication = Mock(spec=V2ComprehensiveMessagingSystem)
        self.mock_fsm_system_manager = Mock(spec=FSMSystemManager)

        # Initialize onboarding sequence
        self.onboarding = V2OnboardingSequence(self.test_config)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test onboarding sequence initialization"""
        self.assertIsNotNone(self.onboarding)
        self.assertEqual(len(self.onboarding.role_definitions), 8)
        self.assertIn("Agent-1", self.onboarding.role_definitions)
        self.assertIn("Agent-8", self.onboarding.role_definitions)

        # Check role definitions
        agent1_role = self.onboarding.role_definitions["Agent-1"]
        self.assertEqual(agent1_role["role"], "System Coordinator & Project Manager")
        self.assertIn("FSM coordination", agent1_role["capabilities"])

    def test_message_templates(self):
        """Test onboarding message template initialization"""
        self.assertIn("system_overview", self.onboarding.onboarding_templates)
        self.assertIn("role_assignment", self.onboarding.onboarding_templates)
        self.assertIn("capability_training", self.onboarding.onboarding_templates)
        self.assertIn("integration_testing", self.onboarding.onboarding_templates)

        # Check template structure
        overview_template = self.onboarding.onboarding_templates["system_overview"]
        self.assertEqual(overview_template.phase, OnboardingPhase.SYSTEM_OVERVIEW)
        self.assertTrue(overview_template.requires_response)
        self.assertIn("response_time", overview_template.validation_criteria)

    def test_start_onboarding(self):
        """Test starting onboarding for an agent"""
        # Mock component references
        self.onboarding.communication_protocol = self.mock_communication
        self.onboarding.fsm_core = self.mock_fsm_core

        # Start onboarding
        session_id = self.onboarding.start_onboarding(
            "Agent-1",
            self.mock_communication,
            self.mock_fsm_core,
        )

        self.assertIsNotNone(session_id)
        self.assertIn(session_id, self.onboarding.active_sessions)

        # Check session creation
        session = self.onboarding.active_sessions[session_id]
        self.assertEqual(session.agent_id, "Agent-1")
        self.assertEqual(session.status, OnboardingStatus.INITIALIZING)
        self.assertEqual(session.current_phase, OnboardingPhase.SYSTEM_OVERVIEW)

    def test_start_onboarding_invalid_agent(self):
        """Test starting onboarding with invalid agent ID"""
        with self.assertRaises(ValueError):
            self.onboarding.start_onboarding(
                "Invalid-Agent",
                self.mock_communication,
                self.mock_fsm_core,
                self.mock_inbox_manager,
            )

    def test_phase_execution(self):
        """Test onboarding phase execution"""
        # Create a test session
        session = OnboardingSession(
            session_id="test_session",
            agent_id="Agent-1",
            status=OnboardingStatus.INITIALIZING,
            current_phase=OnboardingPhase.SYSTEM_OVERVIEW,
            completed_phases=[],
            start_time=time.time(),
        )
        self.onboarding.active_sessions["test_session"] = session

        # Mock communication protocol
        self.onboarding.communication_protocol = self.mock_communication
        self.mock_communication.send_message.return_value = "test_message_id"

        # Execute phase
        success = self.onboarding._execute_phase(
            session, OnboardingPhase.SYSTEM_OVERVIEW
        )

        # Verify communication was called
        self.mock_communication.send_message.assert_called_once()
        call_args = self.mock_communication.send_message.call_args
        self.assertEqual(call_args[1]["recipient_id"], "Agent-1")
        self.assertEqual(call_args[1]["message_type"], MessageType.COORDINATION)
        self.assertEqual(call_args[1]["priority"], UnifiedMessagePriority.HIGH)

    def test_phase_message_generation(self):
        """Test phase-specific message generation"""
        # Test system overview message
        message = self.onboarding._get_phase_message(
            OnboardingPhase.SYSTEM_OVERVIEW, "Agent-1"
        )
        self.assertEqual(message.phase, OnboardingPhase.SYSTEM_OVERVIEW)
        self.assertIn("Welcome to Agent Cellphone V2", message.content)

        # Test role assignment message
        message = self.onboarding._get_phase_message(
            OnboardingPhase.ROLE_ASSIGNMENT, "Agent-1"
        )
        self.assertEqual(message.phase, OnboardingPhase.ROLE_ASSIGNMENT)
        self.assertIn("System Coordinator & Project Manager", message.content)
        self.assertTrue(message.role_specific)

        # Test capability training message
        message = self.onboarding._get_phase_message(
            OnboardingPhase.CAPABILITY_TRAINING, "Agent-2"
        )
        self.assertEqual(message.phase, OnboardingPhase.CAPABILITY_TRAINING)
        self.assertIn("Frontend Development Specialist", message.content)
        self.assertTrue(message.role_specific)

    def test_onboarding_completion_validation(self):
        """Test onboarding completion validation"""
        # Create a completed session
        session = OnboardingSession(
            session_id="test_session",
            agent_id="Agent-1",
            status=OnboardingStatus.TRAINING,
            current_phase=OnboardingPhase.INTEGRATION_TESTING,
            completed_phases=[
                OnboardingPhase.SYSTEM_OVERVIEW,
                OnboardingPhase.ROLE_ASSIGNMENT,
                OnboardingPhase.CAPABILITY_TRAINING,
                OnboardingPhase.INTEGRATION_TESTING,
            ],
            start_time=time.time(),
        )

        # Mock FSM core
        self.onboarding.fsm_core = self.mock_fsm_core
        self.mock_fsm_core.create_task.return_value = "test_task_id"

        # Validate completion
        success = self.onboarding._validate_onboarding_completion(session)

        self.assertTrue(success)
        self.mock_fsm_core.create_task.assert_called_once()

    def test_onboarding_status_tracking(self):
        """Test onboarding status tracking and retrieval"""
        # Create test sessions
        session1 = OnboardingSession(
            session_id="session1",
            agent_id="Agent-1",
            status=OnboardingStatus.COMPLETED,
            current_phase=OnboardingPhase.INTEGRATION_TESTING,
            completed_phases=[
                OnboardingPhase.SYSTEM_OVERVIEW,
                OnboardingPhase.ROLE_ASSIGNMENT,
            ],
            start_time=time.time(),
            completion_time=time.time(),
        )

        session2 = OnboardingSession(
            session_id="session2",
            agent_id="Agent-2",
            status=OnboardingStatus.TRAINING,
            current_phase=OnboardingPhase.CAPABILITY_TRAINING,
            completed_phases=[OnboardingPhase.SYSTEM_OVERVIEW],
            start_time=time.time(),
        )

        self.onboarding.active_sessions["session1"] = session1
        self.onboarding.active_sessions["session2"] = session2

        # Get individual status
        status1 = self.onboarding.get_onboarding_status("session1")
        self.assertEqual(status1["agent_id"], "Agent-1")
        self.assertEqual(status1["status"], "completed")
        self.assertEqual(len(status1["completed_phases"]), 2)

        # Get all status
        all_status = self.onboarding.get_all_onboarding_status()
        self.assertEqual(len(all_status), 2)
        self.assertIn("session1", all_status)
        self.assertIn("session2", all_status)

    def test_session_cleanup(self):
        """Test cleanup of completed sessions"""
        # Create test sessions
        completed_session = OnboardingSession(
            session_id="completed",
            agent_id="Agent-1",
            status=OnboardingStatus.COMPLETED,
            current_phase=OnboardingPhase.INTEGRATION_TESTING,
            completed_phases=[
                OnboardingPhase.SYSTEM_OVERVIEW,
                OnboardingPhase.ROLE_ASSIGNMENT,
            ],
            start_time=time.time(),
            completion_time=time.time(),
        )

        active_session = OnboardingSession(
            session_id="active",
            agent_id="Agent-2",
            status=OnboardingStatus.TRAINING,
            current_phase=OnboardingPhase.CAPABILITY_TRAINING,
            completed_phases=[OnboardingPhase.SYSTEM_OVERVIEW],
            start_time=time.time(),
        )

        self.onboarding.active_sessions["completed"] = completed_session
        self.onboarding.active_sessions["active"] = active_session

        # Cleanup completed sessions
        self.onboarding.cleanup_completed_sessions()

        # Verify cleanup
        self.assertNotIn("completed", self.onboarding.active_sessions)
        self.assertIn("active", self.onboarding.active_sessions)

    def test_role_definitions_completeness(self):
        """Test that all V2 agents have complete role definitions"""
        expected_agents = [f"Agent-{i}" for i in range(1, 9)]

        for agent_id in expected_agents:
            self.assertIn(agent_id, self.onboarding.role_definitions)

            role_info = self.onboarding.role_definitions[agent_id]
            self.assertIn("role", role_info)
            self.assertIn("capabilities", role_info)
            self.assertIn("onboarding_phases", role_info)

            # Check capabilities are not empty
            self.assertGreater(len(role_info["capabilities"]), 0)

            # Check onboarding phases are valid
            for phase in role_info["onboarding_phases"]:
                self.assertIsInstance(phase, OnboardingPhase)

    def test_phase_timeout_handling(self):
        """Test phase timeout handling"""
        # Create a test session
        session = OnboardingSession(
            session_id="test_session",
            agent_id="Agent-1",
            status=OnboardingStatus.INITIALIZING,
            current_phase=OnboardingPhase.SYSTEM_OVERVIEW,
            completed_phases=[],
            start_time=time.time(),
        )

        # Mock inbox manager to simulate no response
        self.onboarding.inbox_manager = self.mock_inbox_manager
        self.mock_inbox_manager.get_messages.return_value = []  # No responses

        # Test phase response waiting with timeout
        success = self.onboarding._wait_for_phase_response(
            session, OnboardingPhase.SYSTEM_OVERVIEW, "test_message_id"
        )

        # Should fail due to timeout
        self.assertFalse(success)

    def test_error_handling(self):
        """Test error handling in onboarding sequence"""
        # Test with None components
        with self.assertRaises(Exception):
            self.onboarding.start_onboarding("Agent-1", None, None, None)

        # Test invalid phase execution
        session = OnboardingSession(
            session_id="test_session",
            agent_id="Agent-1",
            status=OnboardingStatus.INITIALIZING,
            current_phase=OnboardingPhase.SYSTEM_OVERVIEW,
            completed_phases=[],
            start_time=time.time(),
        )

        # Should handle errors gracefully
        success = self.onboarding._execute_phase(
            session, OnboardingPhase.SYSTEM_OVERVIEW
        )
        self.assertFalse(success)  # Should fail due to no communication protocol


class TestV2OnboardingIntegration(unittest.TestCase):
    """Integration tests for V2 Onboarding Sequence"""

    def setUp(self):
        """Set up integration test fixtures"""
        self.test_config = {"phase_timeout": 5, "validation_retries": 1}

        # Create temporary directories
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "workspaces"
        self.fsm_data_path = Path(self.test_dir) / "fsm_data"
        self.inbox_path = Path(self.test_dir) / "communication"

        # Create directories
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        self.fsm_data_path.mkdir(parents=True, exist_ok=True)
        self.inbox_path.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Clean up integration test fixtures"""
        shutil.rmtree(self.test_dir)

    @patch("src.core.agent_communication.AgentCommunicationProtocol")
    @patch("src.core.fsm.FSMSystemManager")
    @patch("src.core.inbox_manager.InboxManager")
    def test_full_onboarding_workflow(self, mock_inbox, mock_fsm, mock_comm):
        """Test complete onboarding workflow integration"""
        # Mock components
        mock_comm_instance = Mock()
        mock_fsm_instance = Mock()
        mock_inbox_instance = Mock()

        mock_comm.return_value = mock_comm_instance
        mock_fsm.return_value = mock_fsm_instance
        mock_inbox.return_value = mock_inbox_instance

        # Mock communication responses
        mock_comm_instance.send_message.return_value = "test_message_id"

        # Initialize onboarding
        onboarding = V2OnboardingSequence(self.test_config)

        # Start onboarding
        session_id = onboarding.start_onboarding(
            "Agent-1", mock_comm_instance, mock_fsm_instance, mock_inbox_instance
        )

        self.assertIsNotNone(session_id)

        # Wait for completion (with timeout for testing)
        max_wait = 10
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status = onboarding.get_onboarding_status(session_id)
            if status and status.get("status") in ["completed", "failed"]:
                break
            time.sleep(0.1)

        # Verify final status
        final_status = onboarding.get_onboarding_status(session_id)
        self.assertIsNotNone(final_status)
        self.assertIn("status", final_status)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
