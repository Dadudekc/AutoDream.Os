from datetime import datetime
import logging

import unittest

from gaming_integration import (
from src.core.managers.performance_manager import PerformanceManager
from src.core.performance.alerts import AlertSeverity
from unittest.mock import Mock, patch
import time

#!/usr/bin/env python3
"""
Gaming Integration Test Suite - TASK 3C

Comprehensive testing for gaming systems integration with core infrastructure.
Tests performance monitoring, alert system, and metric registration.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3C - Gaming Systems Integration
"""


# Import gaming integration components
    GamingIntegrationManager, 
    GamingPerformanceMetrics, 
    GamingAlert
)

# Import core infrastructure components


class TestGamingIntegration(unittest.TestCase):
    """Test suite for gaming systems integration"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock performance manager
        self.mock_performance_manager = Mock(spec=PerformanceManager)
        self.gaming_integration = GamingIntegrationManager(self.mock_performance_manager)
        
        # Configure logging for tests
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Gaming Integration Test Suite initialized")
    
    def test_gaming_integration_manager_initialization(self):
        """Test gaming integration manager initialization"""
        self.assertIsNotNone(self.gaming_integration)
        self.assertFalse(self.gaming_integration.integration_active)
        self.assertIsNone(self.gaming_integration.last_integration_check)
        self.assertEqual(len(self.gaming_integration.gaming_metrics), 0)
        self.assertEqual(len(self.gaming_integration.gaming_alerts), 0)
        
        self.logger.info("✅ Gaming integration manager initialization test passed")
    
    def test_start_integration(self):
        """Test starting gaming integration"""
        # Mock performance manager methods
        self.mock_performance_manager.add_metric.return_value = None
        self.mock_performance_manager.set_alert_threshold.return_value = None
        
        # Start integration
        result = self.gaming_integration.start_integration()
        
        # Verify integration started
        self.assertTrue(result)
        self.assertTrue(self.gaming_integration.integration_active)
        self.assertIsNotNone(self.gaming_integration.last_integration_check)
        
        # Verify performance monitoring setup
        self.mock_performance_manager.add_metric.assert_called()
        self.mock_performance_manager.set_alert_threshold.assert_called()
        
        self.logger.info("✅ Gaming integration start test passed")
    
    def test_stop_integration(self):
        """Test stopping gaming integration"""
        # Start integration first
        self.gaming_integration.start_integration()
        self.assertTrue(self.gaming_integration.integration_active)
        
        # Stop integration
        result = self.gaming_integration.stop_integration()
        
        # Verify integration stopped
        self.assertTrue(result)
        self.assertFalse(self.gaming_integration.integration_active)
        
        self.logger.info("✅ Gaming integration stop test passed")
    
    def test_gaming_performance_metrics_creation(self):
        """Test gaming performance metrics creation"""
        metrics = GamingPerformanceMetrics(
            frame_rate=60.0,
            response_time=16.67,
            memory_usage=1024.0,
            cpu_usage=25.0,
            gpu_usage=30.0,
            network_latency=50.0,
            game_state="test_game"
        )
        
        # Verify metrics structure
        self.assertEqual(metrics.frame_rate, 60.0)
        self.assertEqual(metrics.response_time, 16.67)
        self.assertEqual(metrics.memory_usage, 1024.0)
        self.assertEqual(metrics.cpu_usage, 25.0)
        self.assertEqual(metrics.gpu_usage, 30.0)
        self.assertEqual(metrics.network_latency, 50.0)
        self.assertEqual(metrics.game_state, "test_game")
        self.assertIsNotNone(metrics.timestamp)
        
        self.logger.info("✅ Gaming performance metrics creation test passed")
    
    def test_gaming_alert_creation(self):
        """Test gaming alert creation"""
        alert = GamingAlert(
            alert_id="test_alert_001",
            alert_type="gaming_frame_rate",
            severity=AlertSeverity.CRITICAL,
            message="Critical frame rate detected",
            game_context={"game_state": "test", "frame_rate": 2.0}
        )
        
        # Verify alert structure
        self.assertEqual(alert.alert_id, "test_alert_001")
        self.assertEqual(alert.alert_type, "gaming_frame_rate")
        self.assertEqual(alert.severity, AlertSeverity.CRITICAL)
        self.assertEqual(alert.message, "Critical frame rate detected")
        self.assertEqual(alert.game_context["game_state"], "test")
        self.assertEqual(alert.game_context["frame_rate"], 2.0)
        self.assertIsNotNone(alert.timestamp)
        
        self.logger.info("✅ Gaming alert creation test passed")
    
    def test_update_gaming_metrics(self):
        """Test updating gaming metrics"""
        # Start integration
        self.gaming_integration.start_integration()
        
        # Create test metrics
        test_metrics = GamingPerformanceMetrics(
            frame_rate=45.0,
            response_time=22.22,
            memory_usage=2048.0,
            cpu_usage=35.0,
            gpu_usage=45.0,
            network_latency=75.0,
            game_state="test_update"
        )
        
        # Update metrics
        result = self.gaming_integration.update_gaming_metrics(test_metrics)
        
        # Verify update successful
        self.assertTrue(result)
        self.assertEqual(len(self.gaming_integration.gaming_metrics), 1)
        self.assertEqual(self.gaming_integration.gaming_metrics[0].frame_rate, 45.0)
        
        # Verify performance manager was called
        self.mock_performance_manager.add_metric.assert_called()
        
        self.logger.info("✅ Gaming metrics update test passed")
    
    def test_gaming_alert_generation(self):
        """Test gaming alert generation for performance issues"""
        # Start integration
        self.gaming_integration.start_integration()
        
        # Create metrics that should trigger alerts
        critical_metrics = GamingPerformanceMetrics(
            frame_rate=2.0,  # Critical frame rate
            response_time=1000.0,  # Critical response time
            memory_usage=10240.0,  # Critical memory usage
            cpu_usage=25.0,
            gpu_usage=30.0,
            network_latency=50.0,
            game_state="alert_test"
        )
        
        # Update metrics (this should trigger alerts)
        self.gaming_integration.update_gaming_metrics(critical_metrics)
        
        # Verify alerts were generated
        self.assertGreater(len(self.gaming_integration.gaming_alerts), 0)
        
        # Check for specific alert types
        frame_rate_alerts = [a for a in self.gaming_integration.gaming_alerts 
                           if a.alert_type == "gaming_frame_rate"]
        response_time_alerts = [a for a in self.gaming_integration.gaming_alerts 
                              if a.alert_type == "gaming_response_time"]
        memory_alerts = [a for a in self.gaming_integration.gaming_alerts 
                        if a.alert_type == "gaming_memory_usage"]
        
        self.assertGreater(len(frame_rate_alerts), 0)
        self.assertGreater(len(response_time_alerts), 0)
        self.assertGreater(len(memory_alerts), 0)
        
        self.logger.info("✅ Gaming alert generation test passed")
    
    def test_gaming_performance_summary(self):
        """Test gaming performance summary generation"""
        # Start integration and add some metrics
        self.gaming_integration.start_integration()
        
        test_metrics = GamingPerformanceMetrics(
            frame_rate=60.0,
            response_time=16.67,
            memory_usage=1024.0,
            cpu_usage=25.0,
            gpu_usage=30.0,
            network_latency=50.0,
            game_state="summary_test"
        )
        
        self.gaming_integration.update_gaming_metrics(test_metrics)
        
        # Get performance summary
        summary = self.gaming_integration.get_gaming_performance_summary()
        
        # Verify summary structure
        self.assertIn("integration_status", summary)
        self.assertIn("current_metrics", summary)
        self.assertIn("total_metrics_collected", summary)
        self.assertIn("total_alerts_generated", summary)
        
        # Verify summary data
        self.assertEqual(summary["integration_status"], "active")
        self.assertEqual(summary["total_metrics_collected"], 1)
        self.assertEqual(summary["current_metrics"]["frame_rate"], 60.0)
        self.assertEqual(summary["current_metrics"]["game_state"], "summary_test")
        
        self.logger.info("✅ Gaming performance summary test passed")
    
    def test_gaming_integration_tests(self):
        """Test the gaming integration test suite"""
        # Start integration
        self.gaming_integration.start_integration()
        
        # Run integration tests
        test_results = self.gaming_integration.run_gaming_integration_tests()
        
        # Verify test results structure
        self.assertIn("overall_success", test_results)
        self.assertIn("test_results", test_results)
        self.assertIn("timestamp", test_results)
        
        # Verify individual test results
        test_results_detail = test_results["test_results"]
        self.assertIn("performance_monitoring", test_results_detail)
        self.assertIn("alert_system", test_results_detail)
        self.assertIn("metric_registration", test_results_detail)
        self.assertIn("integration_status", test_results_detail)
        
        # Verify test success
        self.assertTrue(test_results["overall_success"])
        
        self.logger.info("✅ Gaming integration tests test passed")
    
    def test_integration_with_mock_performance_manager(self):
        """Test integration with mocked performance manager"""
        # Start integration
        self.gaming_integration.start_integration()
        
        # Verify performance manager methods were called during setup
        self.mock_performance_manager.add_metric.assert_called()
        self.mock_performance_manager.set_alert_threshold.assert_called()
        
        # Test metric registration
        test_metrics = GamingPerformanceMetrics(
            frame_rate=30.0,
            response_time=33.33,
            memory_usage=1536.0,
            cpu_usage=40.0,
            gpu_usage=50.0,
            network_latency=100.0,
            game_state="mock_test"
        )
        
        # Update metrics
        self.gaming_integration.update_gaming_metrics(test_metrics)
        
        # Verify performance manager was called for each metric
        expected_calls = [
            ("gaming_frame_rate", 30.0, "fps", "gaming"),
            ("gaming_response_time", 33.33, "ms", "gaming"),
            ("gaming_memory_usage", 1536.0, "MB", "gaming"),
            ("gaming_cpu_usage", 40.0, "percent", "gaming"),
            ("gaming_gpu_usage", 50.0, "percent", "gaming"),
            ("gaming_network_latency", 100.0, "ms", "gaming")
        ]
        
        for expected_call in expected_calls:
            self.mock_performance_manager.add_metric.assert_any_call(*expected_call)
        
        self.logger.info("✅ Mock performance manager integration test passed")
    
    def test_error_handling(self):
        """Test error handling in gaming integration"""
        # Test with invalid performance manager
        invalid_integration = GamingIntegrationManager(None)
        
        # Attempt to start integration (should handle error gracefully)
        result = invalid_integration.start_integration()
        self.assertFalse(result)
        self.assertFalse(invalid_integration.integration_active)
        
        # Test metrics update without active integration
        test_metrics = GamingPerformanceMetrics(
            frame_rate=60.0,
            response_time=16.67,
            memory_usage=1024.0,
            cpu_usage=25.0,
            gpu_usage=30.0,
            network_latency=50.0,
            game_state="error_test"
        )
        
        result = invalid_integration.update_gaming_metrics(test_metrics)
        self.assertFalse(result)
        
        self.logger.info("✅ Error handling test passed")
    
    def test_gaming_metrics_validation(self):
        """Test gaming metrics validation and edge cases"""
        # Test with extreme values
        extreme_metrics = GamingPerformanceMetrics(
            frame_rate=0.0,  # Impossible frame rate
            response_time=999999.0,  # Extreme response time
            memory_usage=0.0,  # No memory usage
            cpu_usage=0.0,  # No CPU usage
            gpu_usage=0.0,  # No GPU usage
            network_latency=0.0,  # No network latency
            game_state="extreme_test"
        )
        
        # Start integration
        self.gaming_integration.start_integration()
        
        # Update with extreme metrics
        result = self.gaming_integration.update_gaming_metrics(extreme_metrics)
        self.assertTrue(result)
        
        # Verify metrics were stored
        self.assertEqual(len(self.gaming_integration.gaming_metrics), 1)
        stored_metrics = self.gaming_integration.gaming_metrics[0]
        self.assertEqual(stored_metrics.frame_rate, 0.0)
        self.assertEqual(stored_metrics.response_time, 999999.0)
        
        self.logger.info("✅ Gaming metrics validation test passed")


def run_gaming_integration_tests():
    """Run the complete gaming integration test suite"""
    print("🎮 GAMING INTEGRATION TEST SUITE - TASK 3C")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestGamingIntegration)
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 GAMING INTEGRATION TEST RESULTS")
    print(f"Tests Run: {test_result.testsRun}")
    print(f"Failures: {len(test_result.failures)}")
    print(f"Errors: {len(test_result.errors)}")
    print(f"Success Rate: {((test_result.testsRun - len(test_result.failures) - len(test_result.errors)) / test_result.testsRun * 100):.1f}%")
    
    if test_result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in test_result.failures:
            print(f"  - {test}: {traceback}")
    
    if test_result.errors:
        print("\n🚨 ERRORS:")
        for test, traceback in test_result.errors:
            print(f"  - {test}: {traceback}")
    
    if test_result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED - GAMING INTEGRATION SUCCESSFUL!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED - GAMING INTEGRATION NEEDS ATTENTION!")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = run_gaming_integration_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)

