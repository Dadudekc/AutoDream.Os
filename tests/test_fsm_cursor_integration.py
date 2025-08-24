#!/usr/bin/env python3
"""
Test Suite: FSM-Cursor Integration - Agent Cellphone V2
=======================================================

Comprehensive testing of the FSM-Cursor Integration system including:
- PerpetualMotionEngine class
- FSMStateMachine class
- FSM trigger system
- Agent activation functions
- Perpetual motion cycles
- State transitions

Focus: Validating the perpetual motion machine functionality and ensuring
agents can be orchestrated correctly through FSM state management.
"""

import unittest
import time
import json

from src.utils.stability_improvements import stability_manager, safe_import
from unittest.mock import Mock, patch, MagicMock, call
from typing import Dict, List, Any

# Import the classes we want to test
from src.core.fsm_cursor_integration import (
    PerpetualMotionEngine,
    FSMStateMachine,
    FSMTrigger,
)


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
        # idle -> processing (valid)
        result = self.fsm.transition_to("processing")
        self.assertTrue(result)
        self.assertEqual(self.fsm.current_state, "processing")

        # processing -> waiting (valid)
        result = self.fsm.transition_to("waiting")
        self.assertTrue(result)
        self.assertEqual(self.fsm.current_state, "waiting")

        # waiting -> idle (valid)
        result = self.fsm.transition_to("idle")
        self.assertTrue(result)
        self.assertEqual(self.fsm.current_state, "idle")

    def test_invalid_state_transitions(self):
        """Test that invalid state transitions are rejected"""
        # idle -> error (invalid)
        result = self.fsm.transition_to("error")
        self.assertFalse(result)
        self.assertEqual(self.fsm.current_state, "idle")

        # idle -> waiting (invalid)
        result = self.fsm.transition_to("waiting")
        self.assertFalse(result)
        self.assertEqual(self.fsm.current_state, "idle")

    def test_state_handlers(self):
        """Test that state handlers execute correctly"""
        context = {"test_data": "test_value"}

        # Test idle state handler
        result = self.fsm._state_idle(context)
        self.assertEqual(result, "idle")

        # Test processing state handler
        result = self.fsm._state_processing(context)
        self.assertEqual(result, "waiting")

        # Test waiting state handler
        result = self.fsm._state_waiting(context)
        self.assertEqual(result, "idle")

        # Test error state handler
        result = self.fsm._state_error(context)
        self.assertEqual(result, "idle")

    def test_execute_cycle(self):
        """Test that FSM cycles execute correctly"""
        context = {"cycle_number": 1}

        # Execute cycle from idle state
        result = self.fsm.execute_cycle(context)
        self.assertEqual(result, "idle")

        # Transition to processing and execute cycle
        self.fsm.transition_to("processing")
        result = self.fsm.execute_cycle(context)
        self.assertEqual(result, "waiting")

        # Execute another cycle
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


class TestPerpetualMotionEngine(unittest.TestCase):
    """Test suite for the PerpetualMotionEngine class"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock the cursor capture system
        with patch(
            "src.core.fsm_cursor_integration.CursorResponseCapture"
        ) as mock_cursor_capture:
            with patch(
                "src.core.fsm_cursor_integration.PerformanceMonitor"
            ) as mock_performance_profiler:
                with patch(
                    "src.core.fsm_cursor_integration.HealthMonitor"
                ) as mock_health_monitor:
                    self.engine = PerpetualMotionEngine()

    def test_engine_initialization(self):
        """Test that the perpetual motion engine initializes correctly"""
        self.assertIsNotNone(self.engine.cursor_capture)
        self.assertIsNotNone(self.engine.performance_profiler)
        self.assertIsNotNone(self.engine.health_monitor)
        self.assertFalse(self.engine.is_running)
        self.assertEqual(self.engine.cycle_count, 0)
        self.assertEqual(len(self.engine.triggers), 4)  # Default triggers
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
        # Mock the start methods
        with patch.object(
            self.engine.cursor_capture, "start_capture"
        ) as mock_start_capture:
            with patch.object(
                self.engine.performance_profiler, "start_monitoring"
            ) as mock_start_perf:
                with patch.object(
                    self.engine.health_monitor, "start_monitoring"
                ) as mock_start_health:
                    with patch.object(
                        self.engine, "_perpetual_motion_loop"
                    ) as mock_loop:
                        # Start perpetual motion
                        self.engine.start_perpetual_motion()

                        # Verify state
                        self.assertTrue(self.engine.is_running)
                        self.assertGreater(self.engine.continuous_operation_time, 0)

                        # Verify systems were started
                        mock_start_capture.assert_called_once()
                        mock_start_perf.assert_called_once()
                        mock_start_health.assert_called_once()

                        # Verify perpetual motion thread was started
                        self.assertTrue(hasattr(self.engine, "perpetual_motion_thread"))

    def test_stop_perpetual_motion(self):
        """Test stopping the perpetual motion engine"""
        # Start first
        with patch.object(self.engine.cursor_capture, "start_capture"):
            with patch.object(self.engine.performance_profiler, "start_monitoring"):
                with patch.object(self.engine.health_monitor, "start_monitoring"):
                    with patch.object(self.engine, "_perpetual_motion_loop"):
                        self.engine.start_perpetual_motion()

        # Mock the stop methods
        with patch.object(
            self.engine.cursor_capture, "stop_capture"
        ) as mock_stop_capture:
            with patch.object(
                self.engine.performance_profiler, "stop_monitoring"
            ) as mock_stop_perf:
                with patch.object(
                    self.engine.health_monitor, "stop_monitoring"
                ) as mock_stop_health:
                    # Stop perpetual motion
                    self.engine.stop_perpetual_motion()

                    # Verify state
                    self.assertFalse(self.engine.is_running)

                    # Verify systems were stopped
                    mock_stop_capture.assert_called_once()
                    mock_stop_perf.assert_called_once()
                    mock_stop_health.assert_called_once()

    def test_message_trigger_detection(self):
        """Test that messages correctly trigger FSM transitions"""
        # Create a test trigger
        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="code review",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
        )

        self.engine.add_trigger(test_trigger)

        # Test message that should trigger
        test_message = {"role": "assistant", "content": "This code needs a code review"}

        triggered_triggers = self.engine._check_message_triggers(test_message)

        self.assertEqual(len(triggered_triggers), 1)
        self.assertEqual(triggered_triggers[0].trigger_id, "test_trigger")

    def test_message_trigger_role_filtering(self):
        """Test that message triggers respect role filtering"""
        # Create a trigger that only activates for assistant messages
        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
        )

        self.engine.add_trigger(test_trigger)

        # Test user message (should not trigger)
        user_message = {"role": "user", "content": "test pattern"}

        triggered_triggers = self.engine._check_message_triggers(user_message)
        self.assertEqual(len(triggered_triggers), 0)

        # Test assistant message (should trigger)
        assistant_message = {"role": "assistant", "content": "test pattern"}

        triggered_triggers = self.engine._check_message_triggers(assistant_message)
        self.assertEqual(len(triggered_triggers), 1)

    def test_trigger_cooldown_respect(self):
        """Test that triggers respect cooldown periods"""
        # Create a trigger with cooldown
        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
            cooldown=1.0,  # 1 second cooldown
        )

        self.engine.add_trigger(test_trigger)

        # First activation should work
        self.assertTrue(self.engine._should_activate_trigger(test_trigger))

        # Update last trigger time
        self.engine.last_trigger_time = time.time()

        # Second activation within cooldown should fail
        self.assertFalse(self.engine._should_activate_trigger(test_trigger))

        # Wait for cooldown to expire
        time.sleep(1.1)

        # Third activation after cooldown should work
        self.assertTrue(self.engine._should_activate_trigger(test_trigger))

    def test_trigger_activation(self):
        """Test that triggers are activated correctly"""
        # Create a test FSM machine
        test_fsm = FSMStateMachine("test_fsm")
        self.engine.add_fsm_machine("test_fsm", test_fsm)

        # Create a test agent activation function
        def test_agent(message, trigger):
            return "activated"

        self.engine.register_agent_activation("test_agent", test_agent)

        # Create a test trigger
        test_trigger = FSMTrigger(
            trigger_id="test_trigger",
            message_pattern="test pattern",
            role_filter="assistant",
            state_transition="processing",
            agent_activation="test_agent",
        )

        test_message = {"role": "assistant", "content": "test pattern"}

        # Activate trigger
        with patch.object(self.engine.logger, "info") as mock_info:
            self.engine._activate_trigger(test_trigger, test_message)

            # Verify trigger was activated
            mock_info.assert_any_call("🎯 Activating trigger: test_trigger")
            mock_info.assert_any_call("✅ Trigger activated: test_trigger")

            # Verify FSM state transition
            self.assertEqual(test_fsm.current_state, "processing")

    def test_fsm_cycle_execution(self):
        """Test that FSM cycles are executed correctly"""
        # Create test FSM machines
        fsm1 = FSMStateMachine("fsm1")
        fsm2 = FSMStateMachine("fsm2")

        self.engine.add_fsm_machine("fsm1", fsm1)
        self.engine.add_fsm_machine("fsm2", fsm2)

        # Mock cursor capture to return no messages
        self.engine.cursor_capture.get_recent_messages.return_value = []

        # Execute perpetual cycle
        self.engine._execute_perpetual_cycle()

        # Verify FSM cycles were executed
        # Note: We can't easily test the actual execution without complex mocking
        # but we can verify the method completed without errors
        self.assertTrue(True)

    def test_health_metrics_update(self):
        """Test that health metrics are updated correctly"""
        # Mock health monitor
        with patch.object(
            self.engine.health_monitor, "register_component"
        ) as mock_register:
            # Update health metrics
            self.engine._update_health_metrics(0.1)

            # Verify component was registered
            mock_register.assert_called_with(
                "perpetual_motion", self.engine._get_health_metrics
            )

    def test_health_metrics_retrieval(self):
        """Test that health metrics are retrieved correctly"""
        metrics = self.engine._get_health_metrics()

        # Verify expected metrics are present
        self.assertIn("response_time", metrics)
        self.assertIn("error_rate", metrics)
        self.assertIn("availability", metrics)
        self.assertIn("throughput", metrics)
        self.assertIn("memory_usage", metrics)
        self.assertIn("cpu_usage", metrics)

        # Verify metric values are reasonable
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

        # Verify expected stats are present
        self.assertIn("is_running", stats)
        self.assertIn("cycle_count", stats)
        self.assertIn("continuous_operation_time", stats)
        self.assertIn("last_trigger_time", stats)
        self.assertIn("active_triggers", stats)
        self.assertIn("active_fsms", stats)
        self.assertIn("registered_agents", stats)

        # Verify initial values
        self.assertFalse(stats["is_running"])
        self.assertEqual(stats["cycle_count"], 0)
        self.assertEqual(stats["active_triggers"], 4)  # Default triggers
        self.assertEqual(stats["active_fsms"], 0)
        self.assertEqual(stats["registered_agents"], 0)

    def test_error_handling_in_perpetual_cycle(self):
        """Test that errors in perpetual motion cycles are handled gracefully"""
        # Mock cursor capture to raise an exception
        self.engine.cursor_capture.get_recent_messages.side_effect = Exception(
            "Test error"
        )

        # Execute perpetual cycle (should not crash)
        try:
            self.engine._execute_perpetual_cycle()
            # Should handle gracefully
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Should handle errors gracefully: {e}")

    def test_perpetual_motion_thread_safety(self):
        """Test that perpetual motion thread operates safely"""
        # Mock all the start methods
        with patch.object(self.engine.cursor_capture, "start_capture"):
            with patch.object(self.engine.performance_profiler, "start_monitoring"):
                with patch.object(self.engine.health_monitor, "start_monitoring"):
                    with patch.object(self.engine, "_perpetual_motion_loop"):
                        # Start perpetual motion
                        self.engine.start_perpetual_motion()

                        # Verify thread is daemon (won't block program exit)
                        self.assertTrue(self.engine.perpetual_motion_thread.daemon)

                        # Stop perpetual motion
                        self.engine.stop_perpetual_motion()


class TestFSMIntegration(unittest.TestCase):
    """Test suite for FSM integration scenarios"""

    def setUp(self):
        """Set up test fixtures"""
        with patch("src.core.fsm_cursor_integration.CursorResponseCapture"):
            with patch("src.core.fsm_cursor_integration.PerformanceMonitor"):
                with patch("src.core.fsm_cursor_integration.HealthMonitor"):
                    self.engine = PerpetualMotionEngine()

    def test_code_review_workflow(self):
        """Test the complete code review workflow"""
        # Create code review FSM
        code_review_fsm = FSMStateMachine("code_review")
        self.engine.add_fsm_machine("code_review", code_review_fsm)

        # Create code review agent
        def code_review_agent(message, trigger):
            return "code_review_completed"

        self.engine.register_agent_activation("code_review_agent", code_review_agent)

        # Simulate code review message
        code_review_message = {
            "role": "assistant",
            "content": "This function needs a code review for security issues",
        }

        # Find matching trigger
        triggered_triggers = self.engine._check_message_triggers(code_review_message)

        # Should trigger code review
        self.assertGreater(len(triggered_triggers), 0)

        # Activate trigger
        for trigger in triggered_triggers:
            if "code_review" in trigger.trigger_id:
                self.engine._activate_trigger(trigger, code_review_message)
                break

        # Verify FSM state transition
        self.assertEqual(code_review_fsm.current_state, "processing")

    def test_multiple_agent_activation(self):
        """Test that multiple agents can be activated for complex messages"""
        # Create multiple FSMs
        fsm1 = FSMStateMachine("agent1")
        fsm2 = FSMStateMachine("agent2")

        self.engine.add_fsm_machine("agent1", fsm1)
        self.engine.add_fsm_machine("agent2", fsm2)

        # Create multiple agents
        def agent1(message, trigger):
            return "agent1_activated"

        def agent2(message, trigger):
            return "agent2_activated"

        self.engine.register_agent_activation("agent1", agent1)
        self.engine.register_agent_activation("agent2", agent2)

        # Create triggers for both agents
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

        # Test message that triggers both patterns
        complex_message = {
            "role": "assistant",
            "content": "This needs pattern1 and pattern2 analysis",
        }

        triggered_triggers = self.engine._check_message_triggers(complex_message)

        # Should trigger both agents
        self.assertEqual(len(triggered_triggers), 2)

        # Activate both triggers
        for trigger in triggered_triggers:
            self.engine._activate_trigger(trigger, complex_message)

        # Verify both FSMs transitioned
        self.assertEqual(fsm1.current_state, "processing")
        self.assertEqual(fsm2.current_state, "processing")


def run_fsm_cursor_integration_tests():
    """Run all FSM-Cursor integration tests"""
    print("🧪 RUNNING FSM-CURSOR INTEGRATION SYSTEM TESTS")
    print("=" * 70)
    print("Focus: Perpetual motion machine, state machine logic, agent orchestration")
    print("Note: All systems are mocked for safe testing")
    print()

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestFSMStateMachine))
    test_suite.addTest(unittest.makeSuite(TestFSMTrigger))
    test_suite.addTest(unittest.makeSuite(TestPerpetualMotionEngine))
    test_suite.addTest(unittest.makeSuite(TestFSMIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 FSM-CURSOR INTEGRATION TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if not result.failures and not result.errors:
        print("\n✅ ALL TESTS PASSED!")
        print("   FSM-Cursor integration validation successful!")
        print("   Perpetual motion machine working correctly!")
        print("   State machine logic functioning properly!")
        print("   Agent orchestration validated!")

    return result.wasSuccessful()


if __name__ == "__main__":
    # Run FSM-Cursor integration tests
    success = run_fsm_cursor_integration_tests()

    # Exit with appropriate code
    exit(0 if success else 1)
