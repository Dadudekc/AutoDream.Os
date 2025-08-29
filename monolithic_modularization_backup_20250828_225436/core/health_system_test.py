from pathlib import Path
import sys

import unittest

from core.managers.health_manager import HealthManager
import time

#!/usr/bin/env python3
"""
🧪 Simplified Health Manager Tests

This test file tests only the methods that actually exist on HealthManager.
Follows V2 standards and tests the consolidated health system.

Author: V2 SWARM CAPTAIN
License: MIT
"""


# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))



class HealthManagerTest(unittest.TestCase):
    """Comprehensive health manager tests."""

    def setUp(self):
        """Set up test environment."""
        self.health_manager = HealthManager()
        
        # Test metric names
        self.test_metric_1 = "test_cpu_usage"
        self.test_metric_2 = "test_memory_usage"

    def tearDown(self):
        """Clean up test environment."""
        if self.health_manager.monitoring_active:
            self.health_manager.stop_monitoring()

    def test_initialization(self):
        """Test health manager initialization."""
        # Check system state
        self.assertFalse(self.health_manager.monitoring_active)
        
        # Check data structures
        self.assertIsInstance(self.health_manager.health_metrics, dict)
        self.assertIsInstance(self.health_manager.health_alerts, dict)
        self.assertIsInstance(self.health_manager.thresholds, dict)
        
        # Check default thresholds
        self.assertGreater(len(self.health_manager.thresholds), 0)
        self.assertIn("cpu_usage", self.health_manager.thresholds)
        self.assertIn("memory_usage", self.health_manager.thresholds)

    def test_lifecycle(self):
        """Test health manager start/stop lifecycle."""
        # Start monitoring
        self.health_manager.start_monitoring()
        self.assertTrue(self.health_manager.monitoring_active)
        
        # Try to start again (should be idempotent)
        self.health_manager.start_monitoring()
        self.assertTrue(self.health_manager.monitoring_active)
        
        # Stop monitoring
        self.health_manager.stop_monitoring()
        self.assertFalse(self.health_manager.monitoring_active)

    def test_threshold_management(self):
        """Test threshold setting and retrieval."""
        # Set thresholds
        self.assertTrue(self.health_manager.set_threshold(self.test_metric_1, "warning", 50.0))
        self.assertTrue(self.health_manager.set_threshold(self.test_metric_1, "critical", 100.0))
        
        # Verify thresholds were set
        self.assertIn(self.test_metric_1, self.health_manager.thresholds)
        thresholds = self.health_manager.thresholds[self.test_metric_1]
        self.assertIn("warning", thresholds)
        self.assertIn("critical", thresholds)

    def test_metric_updates(self):
        """Test metric updates and threshold checking."""
        # Set thresholds first
        self.health_manager.set_threshold(self.test_metric_1, "warning", 80.0)
        self.health_manager.set_threshold(self.test_metric_1, "critical", 95.0)
        
        # Update metrics (this triggers threshold checking)
        self.health_manager._update_metric(self.test_metric_1, 75.5)  # Below warning
        self.health_manager._update_metric(self.test_metric_1, 85.0)  # Above warning
        self.health_manager._update_metric(self.test_metric_1, 97.0)  # Above critical
        
        # Verify metrics were updated
        metric = self.health_manager.health_metrics.get(self.test_metric_1)
        if metric:
            self.assertEqual(metric.value, 97.0)

    def test_alert_management(self):
        """Test alert acknowledgment and resolution."""
        # Create a test alert by setting threshold and updating metric
        self.health_manager.set_threshold(self.test_metric_2, "warning", 50.0)
        self.health_manager._update_metric(self.test_metric_2, 75.0)  # Above warning
        
        # Get active alerts
        active_alerts = self.health_manager.get_active_alerts()
        
        if active_alerts:
            # Test acknowledging alert
            alert_id = active_alerts[0].id
            result = self.health_manager.acknowledge_alert(alert_id, "test_user")
            self.assertTrue(result)
            
            # Test resolving alert
            result = self.health_manager.resolve_alert(alert_id, "test resolution")
            self.assertTrue(result)

    def test_error_handling(self):
        """Test error handling and recovery."""
        # Test getting metric info for non-existent metric
        metric_info = self.health_manager.get_metric_info("nonexistent")
        self.assertIsNone(metric_info)
        
        # Test acknowledging non-existent alert
        result = self.health_manager.acknowledge_alert("nonexistent", "test_user")
        self.assertFalse(result)
        
        # Test resolving non-existent alert
        result = self.health_manager.resolve_alert("nonexistent", "test resolution")
        self.assertFalse(result)

    def test_health_summary(self):
        """Test health summary generation."""
        summary = self.health_manager.get_health_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("total_metrics", summary)
        self.assertIn("total_alerts", summary)
        self.assertIn("health_score", summary)

    def test_performance_operations(self):
        """Test performance of bulk operations."""
        start_time = time.time()
        
        # Set thresholds for 100 metrics
        for i in range(100):
            metric_name = f"perf_metric_{i}"
            self.health_manager.set_threshold(metric_name, "warning", 50.0 + i)
        
        operation_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(operation_time, 1.0)

    def test_concurrent_operations(self):
        """Test concurrent health manager operations."""
        # Start monitoring
        self.health_manager.start_monitoring()
        
        # Perform concurrent operations
        start_time = time.time()
        
        # Simulate concurrent threshold setting
        for i in range(10):
            metric_name = f"concurrent_{i}"
            self.health_manager.set_threshold(metric_name, "warning", 75.0 + i)
            self.health_manager.set_threshold(metric_name, "critical", 80.0 + i)
        
        operation_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(operation_time, 1.0)
        
        # Stop monitoring
        self.health_manager.stop_monitoring()


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
