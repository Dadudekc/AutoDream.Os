#!/usr/bin/env python3
"""
Tests for HealthAlertManager - V2 Refactored Version
===================================================

Tests the refactored HealthAlertManager that inherits from BaseManager.
Ensures all functionality is preserved after refactoring.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import pytest
import time
from datetime import datetime
from unittest.mock import Mock, patch

from src.core.health.alerting.health_alert_manager import HealthAlertManager
from src.core.health.types.health_types import HealthAlert, AlertType, HealthLevel, HealthMetric


class TestHealthAlertManager:
    """Test suite for HealthAlertManager"""
    
    @pytest.fixture
    def manager(self):
        """Create a fresh HealthAlertManager instance for each test"""
        return HealthAlertManager()
    
    @pytest.fixture
    def sample_metrics(self):
        """Sample health metrics for testing"""
        return {
            "cpu_usage": HealthMetric(
                name="cpu_usage",
                value=85.0,
                unit="%",
                threshold_min=0.0,
                threshold_max=100.0,
                current_level=HealthLevel.CRITICAL,
                timestamp=datetime.now().isoformat(),
                trend="increasing",
                description="CPU usage percentage"
            ),
            "memory_usage": HealthMetric(
                name="memory_usage",
                value=60.0,
                unit="%",
                threshold_min=0.0,
                threshold_max=100.0,
                current_level=HealthLevel.GOOD,
                timestamp=datetime.now().isoformat(),
                trend="stable",
                description="Memory usage percentage"
            )
        }

    def test_initialization(self, manager):
        """Test HealthAlertManager initialization"""
        assert manager.manager_id == "health_alert_manager"
        assert manager.name == "Health Alert Manager"
        assert manager.auto_resolve_alerts is True
        assert manager.alert_timeout == 3600
        assert manager.max_alerts == 1000
        assert len(manager.thresholds) > 0
        assert "cpu_usage" in manager.thresholds

    def test_default_thresholds(self, manager):
        """Test default threshold setup"""
        assert "cpu_usage" in manager.thresholds
        assert "memory_usage" in manager.thresholds
        assert "disk_usage" in manager.thresholds
        assert "response_time" in manager.thresholds
        assert "error_rate" in manager.thresholds
        
        # Check specific threshold values
        assert manager.thresholds["cpu_usage"]["warning"] == 70.0
        assert manager.thresholds["cpu_usage"]["critical"] == 90.0
        assert manager.thresholds["cpu_usage"]["emergency"] == 95.0

    def test_set_threshold(self, manager):
        """Test setting custom thresholds"""
        result = manager.set_threshold("custom_metric", "warning", 50.0)
        assert result is True
        assert manager.get_threshold("custom_metric", "warning") == 50.0

    def test_get_threshold(self, manager):
        """Test getting threshold values"""
        warning_threshold = manager.get_threshold("cpu_usage", "warning")
        assert warning_threshold == 70.0
        
        # Test non-existent threshold
        non_existent = manager.get_threshold("non_existent", "warning")
        assert non_existent is None

    def test_get_all_thresholds(self, manager):
        """Test getting all thresholds"""
        all_thresholds = manager.get_all_thresholds()
        assert isinstance(all_thresholds, dict)
        assert "cpu_usage" in all_thresholds
        assert len(all_thresholds) > 0

    def test_check_thresholds_no_alerts(self, manager, sample_metrics):
        """Test threshold checking when no alerts should be generated"""
        # Modify metrics to be below thresholds
        sample_metrics["cpu_usage"].value = 50.0  # Below warning threshold
        
        alerts = manager.check_thresholds(sample_metrics)
        assert len(alerts) == 0

    def test_check_thresholds_generate_alert(self, manager, sample_metrics):
        """Test threshold checking that generates alerts"""
        # CPU usage above critical threshold
        sample_metrics["cpu_usage"].value = 95.0
        
        alerts = manager.check_thresholds(sample_metrics)
        assert len(alerts) == 1
        
        alert = alerts[0]
        assert alert.metric_name == "cpu_usage"
        assert alert.metric_value == 95.0
        assert alert.threshold == 95.0
        assert alert.level == HealthLevel.EMERGENCY
        assert alert.type == AlertType.CRITICAL

    def test_create_alert(self, manager):
        """Test alert creation"""
        alert = manager._create_alert("test_metric", 85.0, 80.0, "critical")
        
        assert alert is not None
        assert alert.metric_name == "test_metric"
        assert alert.metric_value == 85.0
        assert alert.threshold == 80.0
        assert alert.level == HealthLevel.CRITICAL
        assert alert.type == AlertType.ERROR
        assert not alert.resolved
        assert not alert.acknowledged

    def test_acknowledge_alert(self, manager):
        """Test alert acknowledgment"""
        # Create an alert first
        alert = manager._create_alert("test_metric", 85.0, 80.0, "critical")
        alert_id = alert.id
        
        # Acknowledge the alert
        result = manager.acknowledge_alert(alert_id, "test_user")
        assert result is True
        
        # Verify acknowledgment
        alert = manager.get_alert(alert_id)
        assert alert.acknowledged is True
        assert alert.acknowledged_by == "test_user"
        assert alert.acknowledged_at is not None

    def test_resolve_alert(self, manager):
        """Test alert resolution"""
        # Create an alert first
        alert = manager._create_alert("test_metric", 85.0, 80.0, "critical")
        alert_id = alert.id
        
        # Resolve the alert
        result = manager.resolve_alert(alert_id, "Issue fixed")
        assert result is True
        
        # Verify resolution
        alert = manager.get_alert(alert_id)
        assert alert.resolved is True
        assert alert.resolved_at is not None
        assert "RESOLVED: Issue fixed" in alert.message

    def test_get_alert(self, manager):
        """Test getting specific alerts"""
        # Create an alert
        alert = manager._create_alert("test_metric", 85.0, 80.0, "critical")
        alert_id = alert.id
        
        # Get the alert
        retrieved_alert = manager.get_alert(alert_id)
        assert retrieved_alert is not None
        assert retrieved_alert.id == alert_id
        
        # Test non-existent alert
        non_existent = manager.get_alert("non_existent_id")
        assert non_existent is None

    def test_get_active_alerts(self, manager):
        """Test getting active (unresolved) alerts"""
        # Create multiple alerts
        alert1 = manager._create_alert("metric1", 85.0, 80.0, "critical")
        alert2 = manager._create_alert("metric2", 75.0, 70.0, "warning")
        
        # Resolve one alert
        manager.resolve_alert(alert1.id, "Fixed")
        
        # Get active alerts
        active_alerts = manager.get_active_alerts()
        assert len(active_alerts) == 1
        assert active_alerts[0].id == alert2.id

    def test_get_all_alerts(self, manager):
        """Test getting all alerts"""
        # Create multiple alerts
        alert1 = manager._create_alert("metric1", 85.0, 80.0, "critical")
        alert2 = manager._create_alert("metric2", 75.0, 70.0, "warning")
        
        all_alerts = manager.get_all_alerts()
        assert len(all_alerts) == 2
        alert_ids = [alert.id for alert in all_alerts]
        assert alert1.id in alert_ids
        assert alert2.id in alert_ids

    def test_auto_resolve_alerts(self, manager):
        """Test automatic alert resolution"""
        # Create an alert with old timestamp
        old_timestamp = datetime.now().timestamp() - 4000  # More than 1 hour ago
        alert = manager._create_alert("test_metric", 85.0, 80.0, "critical")
        alert.timestamp = datetime.fromtimestamp(old_timestamp).isoformat()
        
        # Run auto-resolve
        manager.auto_resolve_alerts()
        
        # Check if alert was auto-resolved
        updated_alert = manager.get_alert(alert.id)
        assert updated_alert.resolved is True

    def test_cleanup_old_alerts(self, manager):
        """Test cleanup of old resolved alerts"""
        # Create many resolved alerts
        for i in range(600):  # More than max_alerts // 2
            alert = manager._create_alert(f"metric_{i}", 85.0, 80.0, "critical")
            manager.resolve_alert(alert.id, "Cleaned up")
        
        # Trigger cleanup
        manager._cleanup_old_alerts()
        
        # Should have fewer alerts now
        assert len(manager.health_alerts) < 600

    def test_get_alert_statistics(self, manager):
        """Test alert statistics generation"""
        # Create various types of alerts
        alert1 = manager._create_alert("metric1", 85.0, 80.0, "critical")
        alert2 = manager._create_alert("metric2", 75.0, 70.0, "warning")
        
        # Acknowledge one alert
        manager.acknowledge_alert(alert1.id, "user1")
        
        # Resolve one alert
        manager.resolve_alert(alert2.id, "Fixed")
        
        # Get statistics
        stats = manager.get_alert_statistics()
        
        assert stats["total_alerts"] == 2
        assert stats["active_alerts"] == 1
        assert stats["acknowledged_alerts"] == 1
        assert stats["resolved_alerts"] == 1
        assert "level_distribution" in stats
        assert "type_distribution" in stats

    def test_clear_alerts(self, manager):
        """Test clearing all alerts"""
        # Create some alerts
        manager._create_alert("metric1", 85.0, 80.0, "critical")
        manager._create_alert("metric2", 75.0, 70.0, "warning")
        
        assert len(manager.health_alerts) == 2
        
        # Clear all alerts
        manager.clear_alerts()
        
        assert len(manager.health_alerts) == 0

    def test_lifecycle_hooks(self, manager):
        """Test BaseManager lifecycle hooks"""
        # Test start
        result = manager._on_start()
        assert result is True
        
        # Test resource initialization
        result = manager._on_initialize_resources()
        assert result is True
        
        # Test heartbeat
        manager._on_heartbeat()  # Should not raise exception
        
        # Test cleanup
        manager._on_cleanup_resources()  # Should not raise exception
        
        # Test stop
        manager._on_stop()  # Should not raise exception

    def test_recovery_attempt(self, manager):
        """Test recovery attempt logic"""
        error = Exception("Test error")
        result = manager._on_recovery_attempt(error, "test_context")
        assert result is True

    def test_duplicate_alert_prevention(self, manager, sample_metrics):
        """Test that duplicate alerts are not created"""
        # Set CPU usage above threshold
        sample_metrics["cpu_usage"].value = 95.0
        
        # Check thresholds multiple times
        alerts1 = manager.check_thresholds(sample_metrics)
        alerts2 = manager.check_thresholds(sample_metrics)
        
        # Should only create one alert
        assert len(alerts1) == 1
        assert len(alerts2) == 0

    def test_threshold_edge_cases(self, manager):
        """Test threshold edge cases"""
        # Test setting threshold to 0
        result = manager.set_threshold("edge_metric", "warning", 0.0)
        assert result is True
        assert manager.get_threshold("edge_metric", "warning") == 0.0
        
        # Test setting threshold to negative value
        result = manager.set_threshold("edge_metric", "critical", -10.0)
        assert result is True
        assert manager.get_threshold("edge_metric", "critical") == -10.0

    def test_error_handling(self, manager):
        """Test error handling in various methods"""
        # Test with invalid alert ID
        result = manager.acknowledge_alert("invalid_id", "user")
        assert result is False
        
        result = manager.resolve_alert("invalid_id", "Fixed")
        assert result is False
        
        # Test with invalid metric name
        result = manager.set_threshold("", "warning", 50.0)
        assert result is True  # Should handle empty string gracefully

    def test_performance_with_many_alerts(self, manager):
        """Test performance with many alerts"""
        # Create many alerts
        start_time = time.time()
        for i in range(100):
            manager._create_alert(f"metric_{i}", 85.0, 80.0, "critical")
        creation_time = time.time() - start_time
        
        # Should complete in reasonable time
        assert creation_time < 1.0  # Less than 1 second
        
        # Test statistics generation with many alerts
        start_time = time.time()
        stats = manager.get_alert_statistics()
        stats_time = time.time() - start_time
        
        # Should complete in reasonable time
        assert stats_time < 0.1  # Less than 0.1 seconds
        assert stats["total_alerts"] == 100
