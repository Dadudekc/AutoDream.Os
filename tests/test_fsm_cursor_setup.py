import unittest
from unittest.mock import patch

from src.core.fsm_cursor_integration import FSMStateMachine, FSMTrigger


class TestFSMStateMachine(unittest.TestCase):
    """Test suite for the FSMStateMachine class"""

    def setUp(self):
        """Set up test fixtures"""
        self.fsm = FSMStateMachine("test_fsm")

    def test_fsm_initialization(self):
        """Test that FSM initializes correctly"""
        self.assertEqual(self.fsm.name, "test_fsm")
        self.assertEqual(self.fsm.current_state, "idle")
        self.assertIn("idle", self.fsm.states)
        self.assertIn("processing", self.fsm.states)
        self.assertIn("waiting", self.fsm.states)
        self.assertIn("error", self.fsm.states)

    def test_valid_state_transitions(self):
        """Test that valid state transitions work correctly"""
        result = self.fsm.transition_to("processing")
        self.assertTrue(result)
        self.assertEqual(self.fsm.current_state, "processing")

        result = self.fsm.transition_to("waiting")
        self.assertTrue(result)
        self.assertEqual(self.fsm.current_state, "waiting")

        result = self.fsm.transition_to("idle")
        self.assertTrue(result)
        self.assertEqual(self.fsm.current_state, "idle")

    def test_invalid_state_transitions(self):
        """Test that invalid state transitions are rejected"""
        result = self.fsm.transition_to("error")
        self.assertFalse(result)
        self.assertEqual(self.fsm.current_state, "idle")

        result = self.fsm.transition_to("waiting")
        self.assertFalse(result)
        self.assertEqual(self.fsm.current_state, "idle")

    def test_state_handlers(self):
        """Test that state handlers execute correctly"""
        context = {"test_data": "test_value"}

        result = self.fsm._state_idle(context)
        self.assertEqual(result, "idle")

        result = self.fsm._state_processing(context)
        self.assertEqual(result, "waiting")

        result = self.fsm._state_waiting(context)
        self.assertEqual(result, "idle")

        result = self.fsm._state_error(context)
        self.assertEqual(result, "idle")

    def test_execute_cycle(self):
        """Test that FSM cycles execute correctly"""
        context = {"cycle_number": 1}

        result = self.fsm.execute_cycle(context)
        self.assertEqual(result, "idle")

        self.fsm.transition_to("processing")
        result = self.fsm.execute_cycle(context)
        self.assertEqual(result, "waiting")
        self.fsm.transition_to(result)

        result = self.fsm.execute_cycle(context)
        self.assertEqual(result, "idle")

    def test_state_transition_logging(self):
        """Test that state transitions are logged correctly"""
        with patch.object(self.fsm.logger, "info") as mock_info:
            self.fsm.transition_to("processing")
            mock_info.assert_called_with("State transition: idle → processing")

    def test_invalid_transition_logging(self):
        """Test that invalid transitions are logged correctly"""
        with patch.object(self.fsm.logger, "warning") as mock_warning:
            self.fsm.transition_to("error")
            mock_warning.assert_called_with("Invalid transition: idle → error")


class TestFSMTrigger(unittest.TestCase):
    """Test suite for the FSMTrigger class"""

    def test_trigger_initialization(self):
        """Test that FSMTrigger initializes correctly"""
        trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
            priority=5,
            cooldown=2.0,
        )

        self.assertEqual(trigger.trigger_id, "test_trigger")
        self.assertEqual(trigger.message_pattern, "test pattern")
        self.assertEqual(trigger.role_filter, "assistant")
        self.assertEqual(trigger.state_transition, "processing")
        self.assertEqual(trigger.agent_activation, "test_agent")
        self.assertEqual(trigger.priority, 5)
        self.assertEqual(trigger.cooldown, 2.0)

    def test_trigger_default_values(self):
        """Test that FSMTrigger uses correct default values"""
        trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
        )

        self.assertEqual(trigger.priority, 1)
        self.assertEqual(trigger.cooldown, 0.0)
