#!/usr/bin/env python3
"""
🧪 Unit Tests for Refactored Health Monitoring Components

This test file follows TDD methodology:
1. 🔴 Red: Write failing tests first
2. 🟢 Green: Implement minimal code to pass tests
3. 🔄 Refactor: Improve code while keeping tests passing

Author: Foundation & Testing Specialist
License: MIT
"""

import pytest
import asyncio

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.health_metrics_collector import HealthMetricsCollector
from core.health_threshold_manager import HealthThresholdManager
from core.health_alert_manager import HealthAlertManager
from core.health_score_calculator import HealthScoreCalculator
from core.health_monitor_core import HealthMonitorCore


class TestHealthMetricsCollector:
    """Test HealthMetricsCollector component"""

    def test_initialization(self):
        """Test component initialization"""
        collector = HealthMetricsCollector()
        assert collector is not None
        assert collector.health_data == {}

    def test_record_health_metric(self):
        """Test recording health metrics"""
        collector = HealthMetricsCollector()

        # Record a metric
        collector.record_health_metric(
            agent_id="test_agent", metric_type="response_time", value=500.0, unit="ms"
        )

        # Verify metric was recorded
        assert "test_agent" in collector.health_data
        assert len(collector.health_data["test_agent"].metrics) == 1

    def test_get_agent_health(self):
        """Test retrieving agent health data"""
        collector = HealthMetricsCollector()

        # Record a metric first
        collector.record_health_metric(
            agent_id="test_agent", metric_type="response_time", value=500.0, unit="ms"
        )

        # Retrieve health data
        health = collector.get_agent_health("test_agent")
        assert health is not None
        assert health.agent_id == "test_agent"

    def test_get_all_agent_health(self):
        """Test retrieving all agent health data"""
        collector = HealthMetricsCollector()

        # Record metrics for multiple agents
        collector.record_health_metric("agent_1", "response_time", 500.0, "ms")
        collector.record_health_metric("agent_2", "memory_usage", 80.0, "%")

        # Retrieve all health data
        all_health = collector.get_all_agent_health()
        assert len(all_health) == 2
        assert "agent_1" in all_health
        assert "agent_2" in all_health


class TestHealthThresholdManager:
    """Test HealthThresholdManager component"""

    def test_initialization(self):
        """Test component initialization"""
        manager = HealthThresholdManager()
        assert manager is not None
        assert len(manager.thresholds) > 0  # Should have default thresholds

    def test_set_custom_threshold(self):
        """Test setting custom thresholds"""
        manager = HealthThresholdManager()

        # Set custom threshold
        manager.set_threshold(
            metric_type="custom_metric",
            warning_threshold=50.0,
            critical_threshold=100.0,
            unit="count",
            description="Custom metric threshold",
        )

        # Verify threshold was set
        threshold = manager.get_threshold("custom_metric")
        assert threshold is not None
        assert threshold.warning_threshold == 50.0
        assert threshold.critical_threshold == 100.0

    def test_get_threshold(self):
        """Test retrieving thresholds"""
        manager = HealthThresholdManager()

        # Get default threshold
        threshold = manager.get_threshold("response_time")
        assert threshold is not None
        assert threshold.unit == "ms"

    def test_get_all_thresholds(self):
        """Test retrieving all thresholds"""
        manager = HealthThresholdManager()

        all_thresholds = manager.get_all_thresholds()
        assert len(all_thresholds) > 0
        assert "response_time" in all_thresholds


class TestHealthAlertManager:
    """Test HealthAlertManager component"""

    def test_initialization(self):
        """Test component initialization"""
        manager = HealthAlertManager()
        assert manager is not None
        assert manager.alerts == {}

    def test_create_alert(self):
        """Test creating health alerts"""
        manager = HealthAlertManager()

        # Create an alert
        alert = manager.create_alert(
            agent_id="test_agent",
            severity="warning",
            message="Test alert",
            metric_type="response_time",
            current_value=1500.0,
            threshold=1000.0,
        )

        # Verify alert was created
        assert alert.alert_id is not None
        assert alert.agent_id == "test_agent"
        assert alert.severity == "warning"

    def test_get_alerts(self):
        """Test retrieving alerts"""
        manager = HealthAlertManager()

        # Create some alerts
        manager.create_alert("agent_1", "warning", "Alert 1", "metric_1", 100.0, 50.0)
        manager.create_alert("agent_2", "critical", "Alert 2", "metric_2", 200.0, 100.0)

        # Get all alerts
        all_alerts = manager.get_alerts()
        assert len(all_alerts) == 2

    def test_filter_alerts(self):
        """Test filtering alerts by severity and agent"""
        manager = HealthAlertManager()

        # Create alerts with different severities
        manager.create_alert(
            "agent_1", "warning", "Warning alert", "metric_1", 100.0, 50.0
        )
        manager.create_alert(
            "agent_1", "critical", "Critical alert", "metric_2", 200.0, 100.0
        )
        manager.create_alert(
            "agent_2", "warning", "Another warning", "metric_3", 150.0, 75.0
        )

        # Filter by severity
        warning_alerts = manager.get_alerts(severity="warning")
        assert len(warning_alerts) == 2

        # Filter by agent
        agent1_alerts = manager.get_alerts(agent_id="agent_1")
        assert len(agent1_alerts) == 2

    def test_acknowledge_alert(self):
        """Test acknowledging alerts"""
        manager = HealthAlertManager()

        # Create and acknowledge an alert
        alert = manager.create_alert(
            "test_agent", "warning", "Test alert", "metric", 100.0, 50.0
        )
        manager.acknowledge_alert(alert.alert_id)

        # Verify alert was acknowledged
        updated_alert = manager.get_alert(alert.alert_id)
        assert updated_alert.acknowledged is True

    def test_resolve_alert(self):
        """Test resolving alerts"""
        manager = HealthAlertManager()

        # Create and resolve an alert
        alert = manager.create_alert(
            "test_agent", "warning", "Test alert", "metric", 100.0, 50.0
        )
        manager.resolve_alert(alert.alert_id)

        # Verify alert was resolved
        updated_alert = manager.get_alert(alert.alert_id)
        assert updated_alert.resolved is True


class TestHealthScoreCalculator:
    """Test HealthScoreCalculator component"""

    def test_initialization(self):
        """Test component initialization"""
        calculator = HealthScoreCalculator()
        assert calculator is not None

    def test_calculate_health_score(self):
        """Test calculating health scores"""
        calculator = HealthScoreCalculator()

        # Mock health snapshot
        mock_snapshot = Mock()
        mock_snapshot.metrics = {
            "response_time": Mock(value=500.0, unit="ms"),
            "memory_usage": Mock(value=70.0, unit="%"),
        }
        mock_snapshot.alerts = []

        # Mock thresholds
        mock_thresholds = {
            "response_time": Mock(warning_threshold=1000.0, critical_threshold=5000.0),
            "memory_usage": Mock(warning_threshold=80.0, critical_threshold=95.0),
        }

        # Calculate score
        score = calculator.calculate_score(mock_snapshot, mock_thresholds)
        assert 0 <= score <= 100

    def test_generate_recommendations(self):
        """Test generating health recommendations"""
        calculator = HealthScoreCalculator()

        # Mock health snapshot
        mock_snapshot = Mock()
        mock_snapshot.metrics = {
            "response_time": Mock(value=1500.0),
            "memory_usage": Mock(value=85.0),
        }
        mock_snapshot.overall_status = "warning"
        mock_snapshot.alerts = []

        # Generate recommendations
        recommendations = calculator.generate_recommendations(mock_snapshot)
        assert len(recommendations) > 0
        assert isinstance(recommendations, list)


class TestHealthMonitorCore:
    """Test HealthMonitorCore component"""

    def test_initialization(self):
        """Test component initialization"""
        core = HealthMonitorCore()
        assert core is not None
        assert core.monitoring_active is False

    def test_start_monitoring(self):
        """Test starting health monitoring"""
        core = HealthMonitorCore()

        # Start monitoring
        core.start()
        assert core.monitoring_active is True

    def test_stop_monitoring(self):
        """Test stopping health monitoring"""
        core = HealthMonitorCore()

        # Start then stop monitoring
        core.start()
        core.stop()
        assert core.monitoring_active is False

    def test_health_summary(self):
        """Test generating health summary"""
        core = HealthMonitorCore()

        # Get health summary
        summary = core.get_health_summary()
        assert isinstance(summary, dict)
        assert "monitoring_active" in summary
        assert "last_update" in summary


class TestCLIInterface:
    """Test CLI interface functionality"""

    def test_cli_help(self):
        """Test CLI help command"""
        # This will be tested when we implement the CLI
        pass

    def test_cli_test_mode(self):
        """Test CLI test mode"""
        # This will be tested when we implement the CLI
        pass

    def test_cli_demo_mode(self):
        """Test CLI demo mode"""
        # This will be tested when we implement the CLI
        pass


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
