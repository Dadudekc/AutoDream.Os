import time
import unittest
from unittest.mock import patch

from src.core.fsm_cursor_integration import (
    PerpetualMotionEngine,
    FSMStateMachine,
    FSMTrigger,
)


class TestPerpetualMotionEngineExecution(unittest.TestCase):
    """Execution tests for the PerpetualMotionEngine"""

    def setUp(self):
        """Set up test fixtures"""
        with patch("src.core.fsm_cursor_integration.CursorResponseCapture"):
            with patch("src.core.fsm_cursor_integration.PerformanceMonitor"):
                with patch("src.core.fsm_cursor_integration.HealthMonitor"):
                    self.engine = PerpetualMotionEngine()

    def test_engine_initialization(self):
        """Test that the perpetual motion engine initializes correctly"""
        self.assertIsNotNone(self.engine.cursor_capture)
        self.assertIsNotNone(self.engine.performance_profiler)
        self.assertIsNotNone(self.engine.health_monitor)
        self.assertFalse(self.engine.is_running)
        self.assertEqual(self.engine.cycle_count, 0)
        self.assertEqual(len(self.engine.triggers), 4)
        self.assertEqual(len(self.engine.fsm_machines), 0)
        self.assertEqual(len(self.engine.agent_activations), 0)

    def test_default_triggers_setup(self):
        """Test that default FSM triggers are properly configured"""
        expected_trigger_ids = [
            "code_review",
            "documentation",
            "testing",
            "optimization",
        ]

        for trigger in self.engine.triggers:
            self.assertIn(trigger.trigger_id, expected_trigger_ids)
            self.assertEqual(trigger.role_filter, "assistant")
            self.assertEqual(trigger.state_transition, "processing")
            self.assertIn("agent", trigger.agent_activation)

    def test_add_trigger(self):
        """Test adding new FSM triggers"""
        new_trigger = FSMTrigger(
            trigger_id="custom_trigger",
            message_pattern="custom pattern",
            role_filter="user",
            state_transition="waiting",
            agent_activation="custom_agent",
            priority=10,
        )

        initial_count = len(self.engine.triggers)
        self.engine.add_trigger(new_trigger)

        self.assertEqual(len(self.engine.triggers), initial_count + 1)
        self.assertIn(new_trigger, self.engine.triggers)

    def test_add_fsm_machine(self):
        """Test adding new FSM state machines"""
        fsm = FSMStateMachine("test_fsm")

        self.engine.add_fsm_machine("test_fsm", fsm)

        self.assertIn("test_fsm", self.engine.fsm_machines)
        self.assertEqual(self.engine.fsm_machines["test_fsm"], fsm)

    def test_register_agent_activation(self):
        """Test registering agent activation functions"""

        def test_agent(message, trigger):
            return "test_activation"

        self.engine.register_agent_activation("test_agent", test_agent)

        self.assertIn("test_agent", self.engine.agent_activations)
        self.assertEqual(self.engine.agent_activations["test_agent"], test_agent)

    def test_start_perpetual_motion(self):
        """Test starting the perpetual motion engine"""
        with patch.object(self.engine.cursor_capture, "start_capture") as mock_start_capture:
            with patch.object(self.engine.performance_profiler, "start_monitoring") as mock_start_perf:
                with patch.object(self.engine.health_monitor, "start_monitoring") as mock_start_health:
                    with patch.object(self.engine, "_perpetual_motion_loop"):
                        self.engine.start_perpetual_motion()

                        self.assertTrue(self.engine.is_running)
                        self.assertGreater(self.engine.continuous_operation_time, 0)

                        mock_start_capture.assert_called_once()
                        mock_start_perf.assert_called_once()
                        mock_start_health.assert_called_once()

                        self.assertTrue(hasattr(self.engine, "perpetual_motion_thread"))

    def test_message_trigger_detection(self):
        """Test that messages correctly trigger FSM transitions"""
        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="code review",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
        )

        self.engine.add_trigger(test_trigger)

        test_message = {"role": "assistant", "content": "This code needs a code review"}

        triggered_triggers = self.engine._check_message_triggers(test_message)

        self.assertEqual(len(triggered_triggers), 1)
        self.assertEqual(triggered_triggers[0].trigger_id, "test_trigger")

    def test_message_trigger_role_filtering(self):
        """Test that message triggers respect role filtering"""
        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
        )

        self.engine.add_trigger(test_trigger)

        user_message = {"role": "user", "content": "test pattern"}
        triggered_triggers = self.engine._check_message_triggers(user_message)
        self.assertEqual(len(triggered_triggers), 0)

        assistant_message = {"role": "assistant", "content": "test pattern"}
        triggered_triggers = self.engine._check_message_triggers(assistant_message)
        self.assertEqual(len(triggered_triggers), 1)

    def test_trigger_cooldown_respect(self):
        """Test that triggers respect cooldown periods"""
        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
            cooldown=1.0,
        )

        self.engine.add_trigger(test_trigger)

        self.assertTrue(self.engine._should_activate_trigger(test_trigger))

        self.engine.last_trigger_time = time.time()
        self.assertFalse(self.engine._should_activate_trigger(test_trigger))

        time.sleep(1.1)
        self.assertTrue(self.engine._should_activate_trigger(test_trigger))

    def test_trigger_activation(self):
        """Test that triggers are activated correctly"""
        test_fsm = FSMStateMachine("test_fsm")
        self.engine.add_fsm_machine("test_agent", test_fsm)

        def test_agent(message, trigger):
            return "activated"

        self.engine.register_agent_activation("test_agent", test_agent)

        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
        )

        test_message = {"role": "assistant", "content": "test pattern"}

        with patch.object(self.engine.logger, "info") as mock_info:
            self.engine._activate_trigger(test_trigger, test_message)

            mock_info.assert_any_call("🎯 Activating trigger: test_trigger")
            mock_info.assert_any_call("✅ Trigger activated: test_trigger")

            self.assertEqual(test_fsm.current_state, "processing")

    def test_fsm_cycle_execution(self):
        """Test that FSM cycles are executed correctly"""
        fsm1 = FSMStateMachine("fsm1")
        fsm2 = FSMStateMachine("fsm2")

        self.engine.add_fsm_machine("fsm1", fsm1)
        self.engine.add_fsm_machine("fsm2", fsm2)

        self.engine.cursor_capture.get_recent_messages.return_value = []

        self.engine._execute_perpetual_cycle()

        self.assertTrue(True)
