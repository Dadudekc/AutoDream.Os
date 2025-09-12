#!/usr/bin/env python3
"""
🐝 AGENT-2 COMPREHENSIVE SYSTEM HEALTH MONITORING SYSTEM
Complete Health Monitoring Platform Integration

This module provides the complete integrated health monitoring system that combines:
- Health Monitoring Service (metrics collection)
- Alerting System (notification management)
- Web Dashboard (real-time visualization)
- Messaging Integration (alert broadcasting)

Usage:
    from src.core.health.monitoring.health_monitoring_system import HealthMonitoringSystem

    # Initialize and start
    monitor = HealthMonitoringSystem()
    monitor.start()

    # Access components
    snapshot = monitor.get_health_snapshot()
    monitor.start_dashboard()  # Start web dashboard
"""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from .health_alerting import HealthAlertingSystem
    from .health_dashboard import HealthMonitoringDashboard
    from .health_monitoring_service import HealthMonitoringService
except ImportError:
    # Fallback for direct imports
    from health_alerting import HealthAlertingSystem
    from health_dashboard import HealthMonitoringDashboard
    from health_monitoring_service import HealthMonitoringService

logger = logging.getLogger(__name__)


class HealthMonitoringSystem:
    """
    Complete integrated health monitoring system.

    Combines all health monitoring components into a unified platform:
    - Health Monitoring Service for metrics collection
    - Alerting System for notifications
    - Web Dashboard for visualization
    - Messaging integration for alert broadcasting
    """

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Core components
        self.health_service: Optional[HealthMonitoringService] = None
        self.alerting_system: Optional[HealthAlertingSystem] = None
        self.web_dashboard: Optional[HealthMonitoringDashboard] = None

        # System state
        self.system_active = False
        self.dashboard_active = False

        # Initialize components
        self._initialize_components()

    def _initialize_components(self) -> None:
        """Initialize all health monitoring components."""
        # Initialize core health monitoring service (always available)
        self.health_service = HealthMonitoringService()
        logger.info("✅ Health monitoring service initialized")

        # Initialize alerting system (always available)
        self.alerting_system = HealthAlertingSystem()
        logger.info("✅ Health alerting system initialized")

        # Setup alerting integration
        self._setup_alerting_integration()

        # Try to initialize optional components
        try:
            if AutomatedHealthCheckSystem:
                self.health_service._initialize_health_check_system()
                logger.info("✅ Automated health check system integrated")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize health check system: {e}")

        try:
            if PerformanceMonitoringDashboard:
                self.health_service._initialize_performance_dashboard()
                logger.info("✅ Performance monitoring dashboard integrated")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize performance dashboard: {e}")

        try:
            if UnifiedMonitoringCoordinator:
                self.health_service._initialize_monitoring_coordinator()
                logger.info("✅ Unified monitoring coordinator integrated")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize monitoring coordinator: {e}")

        # Initialize web dashboard (optional)
        try:
            self.web_dashboard = HealthMonitoringDashboard(
                health_service=self.health_service, host="0.0.0.0", port=8080
            )
            logger.info("✅ Web dashboard initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize web dashboard: {e}")
            self.web_dashboard = None

    def _setup_alerting_integration(self) -> None:
        """Setup integration between health service and alerting system."""
        if self.health_service and self.alerting_system:
            # Add alerting handler to health service
            self.health_service.add_alert_handler(self.alerting_system.process_health_event)

            logger.info("✅ Health service and alerting system integrated")

    def start(self) -> None:
        """Start the complete health monitoring system."""
        if self.system_active:
            logger.warning("⚠️ Health monitoring system is already active")
            return

        try:
            # Start health monitoring
            if self.health_service:
                self.health_service.start_monitoring()

            # Start alerting system
            if self.alerting_system:
                self.alerting_system.start_alerting()

            self.system_active = True
            logger.info("✅ Complete health monitoring system started")

        except Exception as e:
            logger.error(f"❌ Failed to start health monitoring system: {e}")
            self.stop()
            raise

    def stop(self) -> None:
        """Stop the complete health monitoring system."""
        try:
            # Stop dashboard first
            if self.dashboard_active and self.web_dashboard:
                self.web_dashboard.stop_dashboard()
                self.dashboard_active = False

            # Stop alerting system
            if self.alerting_system:
                self.alerting_system.stop_alerting()

            # Stop health monitoring
            if self.health_service:
                self.health_service.stop_monitoring()

            self.system_active = False
            logger.info("🛑 Complete health monitoring system stopped")

        except Exception as e:
            logger.error(f"❌ Error stopping health monitoring system: {e}")

    def start_dashboard(self, host: str = "0.0.0.0", port: int = 8080) -> bool:
        """Start the web dashboard."""
        if not self.web_dashboard:
            logger.error("❌ Web dashboard not available")
            return False

        if self.dashboard_active:
            logger.warning("⚠️ Dashboard is already active")
            return True

        try:
            # Update dashboard host/port if different
            if self.web_dashboard.host != host or self.web_dashboard.port != port:
                logger.warning("⚠️ Dashboard host/port change requires restart")
                return False

            self.web_dashboard.start_dashboard()
            self.dashboard_active = True

            logger.info(f"✅ Web dashboard started at http://{host}:{port}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start web dashboard: {e}")
            return False

    def stop_dashboard(self) -> bool:
        """Stop the web dashboard."""
        if not self.web_dashboard or not self.dashboard_active:
            return True

        try:
            self.web_dashboard.stop_dashboard()
            self.dashboard_active = False
            logger.info("🛑 Web dashboard stopped")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to stop web dashboard: {e}")
            return False

    def get_health_snapshot(self) -> Any:
        """Get current health snapshot."""
        if not self.health_service:
            return None
        return self.health_service.get_health_snapshot()

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            "system_active": self.system_active,
            "dashboard_active": self.dashboard_active,
            "timestamp": None,
            "health_service": False,
            "alerting_system": False,
            "web_dashboard": False,
            "active_alerts": 0,
            "overall_health": "unknown",
        }

        if self.health_service:
            status["health_service"] = self.health_service.monitoring_active
            snapshot = self.health_service.get_health_snapshot()
            if snapshot:
                status["timestamp"] = snapshot.timestamp.isoformat()
                status["overall_health"] = snapshot.overall_status.value
                status["active_alerts"] = len(snapshot.alerts)

        if self.alerting_system:
            status["alerting_system"] = self.alerting_system.alerting_active

        if self.web_dashboard:
            status["web_dashboard"] = True

        return status

    def export_system_data(self) -> Dict[str, str]:
        """Export all system data."""
        exports = {}

        if self.health_service:
            exports["health_data"] = self.health_service.export_health_data()

        if self.alerting_system:
            exports["alert_data"] = self.alerting_system.export_alert_data()

        return exports

    def get_component_status(self, component_name: str) -> Dict[str, Any]:
        """Get detailed status for a specific component."""
        if not self.health_service:
            return {"error": "Health service not available"}

        # Get latest metrics for the component
        snapshot = self.health_service.get_health_snapshot()
        if not snapshot:
            return {"error": "No health data available"}

        # Find metrics related to the component
        component_metrics = {}
        for name, metric in snapshot.metrics.items():
            if component_name.lower() in name.lower():
                component_metrics[name] = {
                    "value": metric.value,
                    "unit": metric.unit,
                    "timestamp": metric.timestamp.isoformat(),
                    "category": metric.category,
                    "warning_threshold": metric.threshold_warning,
                    "critical_threshold": metric.threshold_critical,
                }

        # Find related alerts
        component_alerts = []
        for alert in snapshot.alerts:
            if component_name.lower() in alert.component.lower():
                component_alerts.append(
                    {
                        "alert_id": alert.alert_id,
                        "severity": alert.level.value,
                        "message": alert.message,
                        "timestamp": alert.timestamp.isoformat(),
                        "resolved": alert.resolved,
                    }
                )

        return {
            "component": component_name,
            "metrics": component_metrics,
            "alerts": component_alerts,
            "health_status": self._determine_component_health(
                component_name, component_metrics, component_alerts
            ),
        }

    def _determine_component_health(self, component: str, metrics: Dict, alerts: List) -> str:
        """Determine health status for a component."""
        # Check for critical alerts
        critical_alerts = [a for a in alerts if a["severity"] == "CRITICAL" and not a["resolved"]]
        if critical_alerts:
            return "critical"

        # Check metric thresholds
        for metric_name, metric_data in metrics.items():
            value = metric_data["value"]
            critical_threshold = metric_data.get("critical_threshold")
            warning_threshold = metric_data.get("warning_threshold")

            if critical_threshold and value >= critical_threshold:
                return "critical"
            elif warning_threshold and value >= warning_threshold:
                return "warning"

        # Check for unresolved warnings
        warning_alerts = [a for a in alerts if a["severity"] == "WARNING" and not a["resolved"]]
        if warning_alerts:
            return "warning"

        return "healthy"

    def configure_alert_channel(self, channel: str, config: Dict[str, Any]) -> bool:
        """Configure an alert notification channel."""
        if not self.alerting_system:
            return False

        try:
            from .health_alerting import AlertChannel, AlertChannelConfig

            alert_channel = AlertChannel(channel)
            channel_config = AlertChannelConfig(
                channel=alert_channel, enabled=config.get("enabled", True), config=config
            )

            self.alerting_system.channel_configs[alert_channel] = channel_config
            logger.info(f"✅ Alert channel {channel} configured")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to configure alert channel {channel}: {e}")
            return False

    def create_custom_alert_rule(self, rule_config: Dict[str, Any]) -> bool:
        """Create a custom alert rule."""
        if not self.alerting_system:
            return False

        try:
            from .health_alerting import AlertChannel, AlertPriority, AlertRule, AlertSeverity

            rule = AlertRule(
                id=rule_config["id"],
                name=rule_config["name"],
                condition=rule_config["condition"],
                severity=AlertSeverity(rule_config["severity"]),
                priority=AlertPriority(rule_config["priority"]),
                channels=[AlertChannel(c) for c in rule_config["channels"]],
                cooldown_minutes=rule_config.get("cooldown_minutes", 15),
                enabled=rule_config.get("enabled", True),
                description=rule_config.get("description", ""),
            )

            self.alerting_system.alert_rules[rule.id] = rule
            logger.info(f"✅ Custom alert rule '{rule.name}' created")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to create custom alert rule: {e}")
            return False


def main():
    """Main function to demonstrate the health monitoring system."""
    import argparse

    parser = argparse.ArgumentParser(description="Health Monitoring System")
    parser.add_argument("--start", action="store_true", help="Start the monitoring system")
    parser.add_argument("--dashboard", action="store_true", help="Start with web dashboard")
    parser.add_argument("--host", default="0.0.0.0", help="Dashboard host")
    parser.add_argument("--port", type=int, default=8080, help="Dashboard port")
    parser.add_argument("--export", action="store_true", help="Export system data")

    args = parser.parse_args()

    if not any([args.start, args.dashboard, args.export]):
        parser.print_help()
        return

    try:
        # Initialize system
        print("🐝 Initializing Health Monitoring System...")
        monitor = HealthMonitoringSystem()

        if args.export:
            print("💾 Exporting system data...")
            exports = monitor.export_system_data()
            for data_type, filepath in exports.items():
                print(f"✅ {data_type}: {filepath}")

        if args.start or args.dashboard:
            print("🚀 Starting health monitoring system...")
            monitor.start()

            if args.dashboard:
                print("🌐 Starting web dashboard...")
                if monitor.start_dashboard(args.host, args.port):
                    print(f"✅ Dashboard available at http://{args.host}:{args.port}")
                else:
                    print("❌ Failed to start dashboard")

            # Keep running
            try:
                print("✅ System running... (Ctrl+C to stop)")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")

        # Cleanup
        monitor.stop()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
