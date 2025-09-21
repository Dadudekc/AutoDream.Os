"""
Test Suite for Intelligent Alerting System
==========================================

Comprehensive tests for alert management, routing, notifications,
escalation, and analytics functionality.
"""

import pytest
from datetime import datetime, timedelta
from src.services.alerting.intelligent_alerting_system import (
    IntelligentAlertingSystem, Alert, AlertRule, NotificationConfig,
    EscalationPolicy, AlertSeverity, AlertStatus, NotificationChannel
)

# ---------- Test Data ----------

def create_sample_alert(system: IntelligentAlertingSystem, 
                       severity: AlertSeverity = AlertSeverity.MEDIUM) -> str:
    """Create a sample alert for testing."""
    return system.create_alert(
        title="Test Alert",
        description="Test alert description",
        severity=severity,
        source="test_source",
        category="test_category",
        metadata={"test": True}
    )

# ---------- System Initialization Tests ----------

class TestSystemInitialization:
    """Test system initialization and configuration."""
    
    def test_system_initialization(self):
        """Test basic system initialization."""
        system = IntelligentAlertingSystem()
        
        assert system.alerts == {}
        assert system.rules == {}
        assert len(system.notification_configs) > 0
        assert len(system.escalation_policies) > 0
        assert system.alert_history == []
    
    def test_system_with_config(self, tmp_path):
        """Test system initialization with configuration file."""
        config = {
            "notification_channels": [
                {
                    "channel": "email",
                    "endpoint": "smtp://test.com:587",
                    "credentials": {"username": "test", "password": "test"},
                    "enabled": True,
                    "rate_limit": 50
                }
            ],
            "escalation_policies": [
                {
                    "id": "test_policy",
                    "name": "Test Policy",
                    "levels": [{"delay": 300, "channels": ["email"]}],
                    "max_escalations": 2
                }
            ]
        }
        
        config_file = tmp_path / "test_config.json"
        with open(config_file, 'w') as f:
            import json
            json.dump(config, f)
        
        system = IntelligentAlertingSystem(str(config_file))
        
        assert NotificationChannel.EMAIL in system.notification_configs
        assert "test_policy" in system.escalation_policies

# ---------- Alert Management Tests ----------

class TestAlertManagement:
    """Test alert creation and management."""
    
    def test_create_alert(self):
        """Test alert creation."""
        system = IntelligentAlertingSystem()
        
        alert_id = system.create_alert(
            title="Test Alert",
            description="Test description",
            severity=AlertSeverity.HIGH,
            source="test_source",
            category="test_category"
        )
        
        assert alert_id in system.alerts
        alert = system.alerts[alert_id]
        assert alert.title == "Test Alert"
        assert alert.severity == AlertSeverity.HIGH
        assert alert.status == AlertStatus.ACTIVE
        assert alert.source == "test_source"
        assert alert.category == "test_category"
    
    def test_alert_id_format(self):
        """Test alert ID format."""
        system = IntelligentAlertingSystem()
        
        alert_id = system.create_alert(
            title="Test",
            description="Test",
            severity=AlertSeverity.LOW,
            source="test",
            category="test"
        )
        
        assert alert_id.startswith("alert_")
        assert len(alert_id) > 10
    
    def test_alert_history(self):
        """Test alert history tracking."""
        system = IntelligentAlertingSystem()
        
        # Create multiple alerts
        for i in range(3):
            system.create_alert(
                title=f"Alert {i}",
                description="Test",
                severity=AlertSeverity.MEDIUM,
                source="test",
                category="test"
            )
        
        assert len(system.alert_history) == 3
        assert len(system.alerts) == 3
    
    def test_acknowledge_alert(self):
        """Test alert acknowledgment."""
        system = IntelligentAlertingSystem()
        alert_id = create_sample_alert(system)
        
        success = system.acknowledge_alert(alert_id, "test_user")
        
        assert success is True
        alert = system.alerts[alert_id]
        assert alert.status == AlertStatus.ACKNOWLEDGED
        assert alert.acknowledged_by == "test_user"
        assert alert.acknowledged_at is not None
    
    def test_acknowledge_nonexistent_alert(self):
        """Test acknowledging non-existent alert."""
        system = IntelligentAlertingSystem()
        
        success = system.acknowledge_alert("nonexistent", "test_user")
        
        assert success is False
    
    def test_resolve_alert(self):
        """Test alert resolution."""
        system = IntelligentAlertingSystem()
        alert_id = create_sample_alert(system)
        
        success = system.resolve_alert(alert_id)
        
        assert success is True
        alert = system.alerts[alert_id]
        assert alert.status == AlertStatus.RESOLVED
        assert alert.resolved_at is not None
    
    def test_resolve_nonexistent_alert(self):
        """Test resolving non-existent alert."""
        system = IntelligentAlertingSystem()
        
        success = system.resolve_alert("nonexistent")
        
        assert success is False

# ---------- Alert Filtering Tests ----------

class TestAlertFiltering:
    """Test alert filtering and retrieval."""
    
    def test_get_all_alerts(self):
        """Test getting all alerts."""
        system = IntelligentAlertingSystem()
        
        # Create alerts with different severities
        system.create_alert("Alert 1", "Test", AlertSeverity.LOW, "test", "test")
        system.create_alert("Alert 2", "Test", AlertSeverity.HIGH, "test", "test")
        system.create_alert("Alert 3", "Test", AlertSeverity.CRITICAL, "test", "test")
        
        alerts = system.get_alerts()
        assert len(alerts) == 3
    
    def test_filter_by_status(self):
        """Test filtering alerts by status."""
        system = IntelligentAlertingSystem()
        
        alert_id = create_sample_alert(system)
        system.acknowledge_alert(alert_id, "test_user")
        
        active_alerts = system.get_alerts(status=AlertStatus.ACTIVE)
        acknowledged_alerts = system.get_alerts(status=AlertStatus.ACKNOWLEDGED)
        
        assert len(active_alerts) == 0
        assert len(acknowledged_alerts) == 1
    
    def test_filter_by_severity(self):
        """Test filtering alerts by severity."""
        system = IntelligentAlertingSystem()
        
        system.create_alert("Alert 1", "Test", AlertSeverity.LOW, "test", "test")
        system.create_alert("Alert 2", "Test", AlertSeverity.HIGH, "test", "test")
        system.create_alert("Alert 3", "Test", AlertSeverity.HIGH, "test", "test")
        
        high_alerts = system.get_alerts(severity=AlertSeverity.HIGH)
        low_alerts = system.get_alerts(severity=AlertSeverity.LOW)
        
        assert len(high_alerts) == 2
        assert len(low_alerts) == 1
    
    def test_filter_by_status_and_severity(self):
        """Test filtering by both status and severity."""
        system = IntelligentAlertingSystem()
        
        # Create and acknowledge a high severity alert
        alert_id = system.create_alert("Alert 1", "Test", AlertSeverity.HIGH, "test", "test")
        system.acknowledge_alert(alert_id, "test_user")
        
        # Create an active low severity alert
        system.create_alert("Alert 2", "Test", AlertSeverity.LOW, "test", "test")
        
        active_high = system.get_alerts(status=AlertStatus.ACTIVE, severity=AlertSeverity.HIGH)
        acknowledged_high = system.get_alerts(status=AlertStatus.ACKNOWLEDGED, severity=AlertSeverity.HIGH)
        
        assert len(active_high) == 0
        assert len(acknowledged_high) == 1

# ---------- Analytics Tests ----------

class TestAnalytics:
    """Test alert analytics functionality."""
    
    def test_empty_analytics(self):
        """Test analytics with no alerts."""
        system = IntelligentAlertingSystem()
        
        analytics = system.get_alert_analytics()
        
        assert analytics["total_alerts"] == 0
        assert analytics["active_alerts"] == 0
        assert analytics["resolved_alerts"] == 0
        assert analytics["resolution_rate"] == 0
    
    def test_analytics_with_alerts(self):
        """Test analytics with various alerts."""
        system = IntelligentAlertingSystem()
        
        # Create alerts with different statuses and severities
        alert1 = create_sample_alert(system, AlertSeverity.LOW)
        alert2 = create_sample_alert(system, AlertSeverity.HIGH)
        alert3 = create_sample_alert(system, AlertSeverity.CRITICAL)
        
        # Acknowledge one alert
        system.acknowledge_alert(alert1, "test_user")
        
        # Resolve another alert
        system.resolve_alert(alert2)
        
        analytics = system.get_alert_analytics()
        
        assert analytics["total_alerts"] == 3
        assert analytics["active_alerts"] == 1
        assert analytics["resolved_alerts"] == 1
        assert analytics["resolution_rate"] == 1/3
        
        # Check severity distribution
        assert analytics["severity_distribution"]["low"] == 1
        assert analytics["severity_distribution"]["high"] == 1
        assert analytics["severity_distribution"]["critical"] == 1
        assert analytics["severity_distribution"]["medium"] == 0

# ---------- Rule Management Tests ----------

class TestRuleManagement:
    """Test alert rule management."""
    
    def test_add_rule(self):
        """Test adding an alert rule."""
        system = IntelligentAlertingSystem()
        
        rule = AlertRule(
            id="test_rule",
            name="Test Rule",
            condition="severity == 'high'",
            severity=AlertSeverity.HIGH,
            channels=[NotificationChannel.EMAIL]
        )
        
        system.add_rule(rule)
        
        assert "test_rule" in system.rules
        assert system.rules["test_rule"].name == "Test Rule"
    
    def test_remove_rule(self):
        """Test removing an alert rule."""
        system = IntelligentAlertingSystem()
        
        rule = AlertRule(
            id="test_rule",
            name="Test Rule",
            condition="test",
            severity=AlertSeverity.MEDIUM,
            channels=[NotificationChannel.EMAIL]
        )
        
        system.add_rule(rule)
        success = system.remove_rule("test_rule")
        
        assert success is True
        assert "test_rule" not in system.rules
    
    def test_remove_nonexistent_rule(self):
        """Test removing non-existent rule."""
        system = IntelligentAlertingSystem()
        
        success = system.remove_rule("nonexistent")
        
        assert success is False

# ---------- Escalation Tests ----------

class TestEscalation:
    """Test alert escalation functionality."""
    
    def test_alert_escalation(self):
        """Test alert escalation logic."""
        system = IntelligentAlertingSystem()
        
        # Create a low severity alert
        alert_id = system.create_alert(
            title="Test Alert",
            description="Test",
            severity=AlertSeverity.LOW,
            source="test",
            category="test"
        )
        
        alert = system.alerts[alert_id]
        
        # Simulate escalation by directly calling escalation
        system._escalate_alert(alert)
        
        assert alert.severity == AlertSeverity.MEDIUM
    
    def test_multiple_escalations(self):
        """Test multiple alert escalations."""
        system = IntelligentAlertingSystem()
        
        alert_id = system.create_alert(
            title="Test Alert",
            description="Test",
            severity=AlertSeverity.LOW,
            source="test",
            category="test"
        )
        
        alert = system.alerts[alert_id]
        
        # Escalate multiple times
        system._escalate_alert(alert)  # LOW -> MEDIUM
        system._escalate_alert(alert)  # MEDIUM -> HIGH
        system._escalate_alert(alert)  # HIGH -> CRITICAL
        
        assert alert.severity == AlertSeverity.CRITICAL

# ---------- Integration Tests ----------

class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_end_to_end_workflow(self):
        """Test complete alert workflow."""
        system = IntelligentAlertingSystem()
        
        # Create alert
        alert_id = system.create_alert(
            title="System Alert",
            description="Database connection failed",
            severity=AlertSeverity.HIGH,
            source="database_monitor",
            category="connectivity"
        )
        
        # Verify alert creation
        assert alert_id in system.alerts
        alert = system.alerts[alert_id]
        assert alert.status == AlertStatus.ACTIVE
        
        # Acknowledge alert
        success = system.acknowledge_alert(alert_id, "admin")
        assert success is True
        assert alert.status == AlertStatus.ACKNOWLEDGED
        
        # Resolve alert
        success = system.resolve_alert(alert_id)
        assert success is True
        assert alert.status == AlertStatus.RESOLVED
        
        # Check analytics
        analytics = system.get_alert_analytics()
        assert analytics["total_alerts"] == 1
        assert analytics["resolved_alerts"] == 1
        assert analytics["resolution_rate"] == 1.0
    
    def test_export_alerts(self, tmp_path):
        """Test alert export functionality."""
        system = IntelligentAlertingSystem()
        
        # Create test alerts
        for i in range(3):
            system.create_alert(
                title=f"Alert {i}",
                description="Test",
                severity=AlertSeverity.MEDIUM,
                source="test",
                category="test"
            )
        
        # Export alerts
        export_file = tmp_path / "alerts.json"
        system.export_alerts(str(export_file))
        
        # Verify export
        assert export_file.exists()
        
        with open(export_file) as f:
            import json
            exported_data = json.load(f)
        
        assert len(exported_data) == 3
        assert all("id" in alert for alert in exported_data)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])


