#!/usr/bin/env python3
"""
🚨 Health Alert Manager - Agent_Cellphone_V2

This component is responsible for handling alert creation, management, and resolution.
Following V2 coding standards: ≤200 LOC, OOP design, SRP.

Author: Foundation & Testing Specialist
License: MIT
"""

import logging
import time
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class HealthAlert:
    """Health alert information"""

    alert_id: str
    agent_id: str
    severity: str
    message: str
    metric_type: str
    current_value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False


class HealthAlertManager:
    """
    Health Alert Manager - Single responsibility: Handle alert creation, management, and resolution.

    Follows V2 standards: ≤200 LOC, OOP design, SRP.
    """

    def __init__(self):
        """Initialize the alert manager"""
        self.alerts: Dict[str, HealthAlert] = {}
        logger.info("HealthAlertManager initialized")

    def create_alert(
        self,
        agent_id: str,
        severity: str,
        message: str,
        metric_type: str,
        current_value: float,
        threshold: float,
    ) -> HealthAlert:
        """Create a health alert"""
        alert_id = f"health_alert_{agent_id}_{metric_type}_{int(time.time())}"

        alert = HealthAlert(
            alert_id=alert_id,
            agent_id=agent_id,
            severity=severity,
            message=message,
            metric_type=metric_type,
            current_value=current_value,
            threshold=threshold,
            timestamp=datetime.now(),
        )

        self.alerts[alert_id] = alert
        logger.warning(f"Health alert created: {message}")
        return alert

    def get_alert(self, alert_id: str) -> Optional[HealthAlert]:
        """Get a specific alert by ID"""
        return self.alerts.get(alert_id)

    def get_alerts(
        self, severity: Optional[str] = None, agent_id: Optional[str] = None
    ) -> List[HealthAlert]:
        """Get alerts with optional filtering"""
        alerts = list(self.alerts.values())

        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity]

        if agent_id:
            alerts = [alert for alert in alerts if alert.agent_id == agent_id]

        return alerts

    def get_active_alerts(self) -> List[HealthAlert]:
        """Get all unresolved alerts"""
        return [alert for alert in self.alerts.values() if not alert.resolved]

    def get_acknowledged_alerts(self) -> List[HealthAlert]:
        """Get all acknowledged alerts"""
        return [alert for alert in self.alerts.values() if alert.acknowledged]

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a health alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].acknowledged = True
            logger.info(f"Alert {alert_id} acknowledged")

    def resolve_alert(self, alert_id: str):
        """Manually resolve a health alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].resolved = True
            logger.info(f"Alert {alert_id} manually resolved")

    def auto_resolve_alert(self, alert_id: str, current_value: float):
        """Automatically resolve an alert if conditions improve"""
        if alert_id in self.alerts:
            alert = self.alerts[alert_id]
            if current_value < alert.threshold:
                alert.resolved = True
                logger.info(f"Alert {alert_id} automatically resolved")

    def remove_alert(self, alert_id: str):
        """Remove an alert completely"""
        if alert_id in self.alerts:
            del self.alerts[alert_id]
            logger.info(f"Alert {alert_id} removed")

    def clear_resolved_alerts(self):
        """Clear all resolved alerts"""
        resolved_alerts = [
            alert_id for alert_id, alert in self.alerts.items() if alert.resolved
        ]
        for alert_id in resolved_alerts:
            del self.alerts[alert_id]
        logger.info(f"Cleared {len(resolved_alerts)} resolved alerts")

    def get_alert_count(
        self, severity: Optional[str] = None, agent_id: Optional[str] = None
    ) -> int:
        """Get count of alerts with optional filtering"""
        return len(self.get_alerts(severity, agent_id))

    def get_alert_summary(self) -> Dict[str, int]:
        """Get summary of alerts by severity"""
        summary = {}
        for alert in self.alerts.values():
            severity = alert.severity
            summary[severity] = summary.get(severity, 0) + 1
        return summary

    def get_agent_alert_summary(self) -> Dict[str, int]:
        """Get summary of alerts by agent"""
        summary = {}
        for alert in self.alerts.values():
            agent_id = alert.agent_id
            summary[agent_id] = summary.get(agent_id, 0) + 1
        return summary

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthAlertManager smoke test...")

            # Test basic initialization
            assert self.alerts == {}
            assert self.get_alert_count() == 0
            logger.info("Basic initialization passed")

            # Test alert creation
            alert = self.create_alert(
                "test_agent", "warning", "Test alert", "response_time", 1500.0, 1000.0
            )
            assert alert.alert_id is not None
            assert alert.agent_id == "test_agent"
            assert alert.severity == "warning"
            assert self.get_alert_count() == 1
            logger.info("Alert creation passed")

            # Test alert retrieval
            retrieved_alert = self.get_alert(alert.alert_id)
            assert retrieved_alert is not None
            assert retrieved_alert.message == "Test alert"
            logger.info("Alert retrieval passed")

            # Test alert filtering
            warning_alerts = self.get_alerts(severity="warning")
            assert len(warning_alerts) == 1

            agent_alerts = self.get_alerts(agent_id="test_agent")
            assert len(agent_alerts) == 1
            logger.info("Alert filtering passed")

            # Test alert acknowledgment
            self.acknowledge_alert(alert.alert_id)
            assert self.get_alert(alert.alert_id).acknowledged is True
            assert self.get_alert_count() == 1
            logger.info("Alert acknowledgment passed")

            # Test alert resolution
            self.resolve_alert(alert.alert_id)
            assert self.get_alert(alert.alert_id).resolved is True
            assert len(self.get_active_alerts()) == 0
            logger.info("Alert resolution passed")

            # Test multiple alerts
            self.create_alert(
                "agent_1", "critical", "Critical alert", "memory_usage", 95.0, 90.0
            )
            self.create_alert(
                "agent_2", "warning", "Warning alert", "cpu_usage", 90.0, 85.0
            )

            assert self.get_alert_count() == 3
            assert self.get_alert_count(severity="critical") == 1
            assert self.get_alert_count(agent_id="agent_1") == 1
            logger.info("Multiple alerts passed")

            # Test alert summary
            severity_summary = self.get_alert_summary()
            assert "warning" in severity_summary
            assert "critical" in severity_summary

            agent_summary = self.get_agent_alert_summary()
            assert "agent_1" in agent_summary
            assert "agent_2" in agent_summary
            logger.info("Alert summary passed")

            # Test alert removal
            self.remove_alert(alert.alert_id)
            assert self.get_alert(alert.alert_id) is None
            logger.info("Alert removal passed")

            # Cleanup
            self.clear_resolved_alerts()
            logger.info("Cleanup passed")

            logger.info("✅ HealthAlertManager smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthAlertManager smoke test FAILED: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return False


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Alert Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")

    args = parser.parse_args()

    if args.test:
        manager = HealthAlertManager()
        success = manager.run_smoke_test()
        exit(0 if success else 1)

    elif args.demo:
        print("🚀 Starting Health Alert Manager Demo...")
        manager = HealthAlertManager()

        # Create some sample alerts
        print("🚨 Creating sample alerts...")
        manager.create_alert(
            "agent_001",
            "warning",
            "High response time",
            "response_time",
            1500.0,
            1000.0,
        )
        manager.create_alert(
            "agent_001", "critical", "Memory usage critical", "memory_usage", 95.0, 90.0
        )
        manager.create_alert(
            "agent_002", "warning", "CPU usage high", "cpu_usage", 90.0, 85.0
        )

        # Show alert summary
        print(f"\n📊 Alert Summary:")
        print(f"  Total Alerts: {manager.get_alert_count()}")
        print(f"  Active Alerts: {len(manager.get_active_alerts())}")

        severity_summary = manager.get_alert_summary()
        print(f"  By Severity: {severity_summary}")

        agent_summary = manager.get_agent_alert_summary()
        print(f"  By Agent: {agent_summary}")

        # Show alert details
        print(f"\n📋 Alert Details:")
        for alert in manager.alerts.values():
            status = "RESOLVED" if alert.resolved else "ACTIVE"
            ack_status = "ACK" if alert.acknowledged else "UNACK"
            print(
                f"  {alert.alert_id}: {alert.severity.upper()} - {alert.message} ({status}, {ack_status})"
            )

        # Test acknowledgment and resolution
        print(f"\n⚙️ Testing alert management...")
        first_alert_id = list(manager.alerts.keys())[0]
        manager.acknowledge_alert(first_alert_id)
        manager.resolve_alert(first_alert_id)

        print(f"  Acknowledged and resolved first alert")
        print(f"  Active Alerts: {len(manager.get_active_alerts())}")

        print("\n✅ Demo completed")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
