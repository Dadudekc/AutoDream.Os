import unittest
from unittest.mock import patch

from src.core.fsm_cursor_integration import (
    PerpetualMotionEngine,
    FSMStateMachine,
    FSMTrigger,
)


class TestPerpetualMotionEngineValidation(unittest.TestCase):
    """Validation tests for the PerpetualMotionEngine"""

    def setUp(self):
        with patch("src.core.fsm_cursor_integration.CursorResponseCapture"):
            with patch("src.core.fsm_cursor_integration.PerformanceMonitor"):
                with patch("src.core.fsm_cursor_integration.HealthMonitor"):
                    self.engine = PerpetualMotionEngine()

    def test_health_metrics_update(self):
        """Test that health metrics are updated correctly"""
        with patch.object(self.engine.health_monitor, "register_component") as mock_register:
            self.engine._update_health_metrics(0.1)
            mock_register.assert_called_with("perpetual_motion", self.engine._get_health_metrics)

    def test_health_metrics_retrieval(self):
        """Test that health metrics are retrieved correctly"""
        metrics = self.engine._get_health_metrics()

        self.assertIn("response_time", metrics)
        self.assertIn("error_rate", metrics)
        self.assertIn("availability", metrics)
        self.assertIn("throughput", metrics)
        self.assertIn("memory_usage", metrics)
        self.assertIn("cpu_usage", metrics)

        self.assertEqual(metrics["response_time"], 0.1)
        self.assertEqual(metrics["error_rate"], 0.0)
        self.assertEqual(metrics["availability"], 1.0)
        self.assertGreaterEqual(metrics["memory_usage"], 0.0)
        self.assertLessEqual(metrics["memory_usage"], 1.0)
        self.assertGreaterEqual(metrics["cpu_usage"], 0.0)
        self.assertLessEqual(metrics["cpu_usage"], 1.0)

    def test_perpetual_motion_stats(self):
        """Test that perpetual motion statistics are retrieved correctly"""
        stats = self.engine.get_perpetual_motion_stats()

        self.assertIn("is_running", stats)
        self.assertIn("cycle_count", stats)
        self.assertIn("continuous_operation_time", stats)
        self.assertIn("last_trigger_time", stats)
        self.assertIn("active_triggers", stats)
        self.assertIn("active_fsms", stats)
        self.assertIn("registered_agents", stats)

        self.assertFalse(stats["is_running"])
        self.assertEqual(stats["cycle_count"], 0)
        self.assertEqual(stats["active_triggers"], 4)
        self.assertEqual(stats["active_fsms"], 0)
        self.assertEqual(stats["registered_agents"], 0)


class TestFSMIntegration(unittest.TestCase):
    """Test suite for FSM integration scenarios"""

    def setUp(self):
        with patch("src.core.fsm_cursor_integration.CursorResponseCapture"):
            with patch("src.core.fsm_cursor_integration.PerformanceMonitor"):
                with patch("src.core.fsm_cursor_integration.HealthMonitor"):
                    self.engine = PerpetualMotionEngine()

    def test_code_review_workflow(self):
        """Test the complete code review workflow"""
        code_review_fsm = FSMStateMachine("code_review")
        self.engine.add_fsm_machine("code_review_agent", code_review_fsm)

        def code_review_agent(message, trigger):
            return "code_review_completed"

        self.engine.register_agent_activation("code_review_agent", code_review_agent)

        code_review_trigger = FSMTrigger(
            trigger_id="code_review_custom",
            message_pattern="code review",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="code_review_agent",
        )
        self.engine.add_trigger(code_review_trigger)

        code_review_message = {
            "role": "assistant",
            "content": "This function needs a code review for security issues",
        }

        triggered_triggers = self.engine._check_message_triggers(code_review_message)
        self.assertGreater(len(triggered_triggers), 0)

        for trigger in triggered_triggers:
            if "code_review" in trigger.trigger_id:
                self.engine._activate_trigger(trigger, code_review_message)
                break

        self.assertEqual(code_review_fsm.current_state, "processing")

    def test_multiple_agent_activation(self):
        """Test that multiple agents can be activated for complex messages"""
        fsm1 = FSMStateMachine("agent1")
        fsm2 = FSMStateMachine("agent2")

        self.engine.add_fsm_machine("agent1", fsm1)
        self.engine.add_fsm_machine("agent2", fsm2)

        def agent1(message, trigger):
            return "agent1_activated"

        def agent2(message, trigger):
            return "agent2_activated"

        self.engine.register_agent_activation("agent1", agent1)
        self.engine.register_agent_activation("agent2", agent2)

        trigger1 = FSMTrigger(
            trigger_id="trigger1",
            message_pattern="pattern1",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="agent1",
        )

        trigger2 = FSMTrigger(
            trigger_id="trigger2",
            message_pattern="pattern2",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="agent2",
        )

        self.engine.add_trigger(trigger1)
        self.engine.add_trigger(trigger2)

        complex_message = {
            "role": "assistant",
            "content": "This needs pattern1 and pattern2 analysis",
        }

        triggered_triggers = self.engine._check_message_triggers(complex_message)
        self.assertEqual(len(triggered_triggers), 2)

        for trigger in triggered_triggers:
            self.engine._activate_trigger(trigger, complex_message)

        self.assertEqual(fsm1.current_state, "processing")
        self.assertEqual(fsm2.current_state, "processing")
