import unittest
from unittest.mock import patch

from src.core.fsm_cursor_integration import PerpetualMotionEngine


class TestPerpetualMotionEngineCleanup(unittest.TestCase):
    """Cleanup and error handling tests for the PerpetualMotionEngine"""

    def setUp(self):
        with patch("src.core.fsm_cursor_integration.CursorResponseCapture"):
            with patch("src.core.fsm_cursor_integration.PerformanceMonitor"):
                with patch("src.core.fsm_cursor_integration.HealthMonitor"):
                    self.engine = PerpetualMotionEngine()

    def test_stop_perpetual_motion(self):
        """Test stopping the perpetual motion engine"""
        with patch.object(self.engine.cursor_capture, "start_capture"):
            with patch.object(self.engine.performance_profiler, "start_monitoring"):
                with patch.object(self.engine.health_monitor, "start_monitoring"):
                    with patch.object(self.engine, "_perpetual_motion_loop"):
                        self.engine.start_perpetual_motion()

        with patch.object(self.engine.cursor_capture, "stop_capture") as mock_stop_capture:
            with patch.object(self.engine.performance_profiler, "stop_monitoring") as mock_stop_perf:
                with patch.object(self.engine.health_monitor, "stop_monitoring") as mock_stop_health:
                    self.engine.stop_perpetual_motion()

                    self.assertFalse(self.engine.is_running)
                    mock_stop_capture.assert_called_once()
                    mock_stop_perf.assert_called_once()
                    mock_stop_health.assert_called_once()

    def test_error_handling_in_perpetual_cycle(self):
        """Test that errors in perpetual motion cycles are handled gracefully"""
        self.engine.cursor_capture.get_recent_messages.side_effect = Exception("Test error")

        try:
            self.engine._execute_perpetual_cycle()
            self.assertTrue(True)
        except Exception as exc:
            self.fail(f"Should handle errors gracefully: {exc}")

    def test_perpetual_motion_thread_safety(self):
        """Test that perpetual motion thread operates safely"""
        with patch.object(self.engine.cursor_capture, "start_capture"):
            with patch.object(self.engine.performance_profiler, "start_monitoring"):
                with patch.object(self.engine.health_monitor, "start_monitoring"):
                    with patch.object(self.engine, "_perpetual_motion_loop"):
                        self.engine.start_perpetual_motion()

                        self.assertTrue(self.engine.perpetual_motion_thread.daemon)

                        self.engine.stop_perpetual_motion()
