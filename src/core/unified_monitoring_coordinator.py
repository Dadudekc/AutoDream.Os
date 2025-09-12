#!/usr/bin/env python3
"""
🐝 AGENT-8 UNIFIED MONITORING COORDINATOR
SWARM Messaging System Restoration - Real-Time Monitoring & Alerting

LEADERSHIP UPDATE: SWARM Leadership Evolution Complete
=====================================================
Captain Agent-4: Strategic Oversight & Final Approval
Co-Captain Agent-2: Tactical Operations & Architecture Leadership
Co-Captain Agent-5: Analytical Operations & Strategic Planning

This module provides unified monitoring coordination for the SWARM messaging
system restoration mission, integrating all existing monitoring components
with mission-specific alerting and real-time status tracking under the new
enhanced leadership structure.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# Import existing monitoring systems
try:
    from .automated_health_check_system import (
        AutomatedHealthCheckSystem,
        HealthCheckResult,
        HealthCheckType,
        HealthStatus,
    )
except ImportError:
    AutomatedHealthCheckSystem = None

try:
    from .performance_monitoring_dashboard import (
        DashboardType,
        MetricType,
        PerformanceMonitoringDashboard,
    )
except ImportError:
    PerformanceMonitoringDashboard = None

try:
    from .operational_monitoring_baseline import (
        MonitoringPriority,
        OperationalMonitoringBaseline,
        SLATier,
    )
except ImportError:
    OperationalMonitoringBaseline = None


class MonitoringAlertLevel(Enum):
    """Alert severity levels for SWARM monitoring."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class SwarmComponent(Enum):
    """SWARM components being monitored."""
    MESSAGING_SYSTEM = "messaging_system"
    PYAUTOGUI_INTEGRATION = "pyautogui_integration"
    INBOX_SYSTEM = "inbox_system"
    AGENT_COORDINATION = "agent_coordination"
    COORDINATE_SYSTEM = "coordinate_system"
    MESSAGE_QUEUE = "message_queue"


@dataclass
class MonitoringAlert:
    """Represents a monitoring alert."""
    alert_id: str
    component: SwarmComponent
    level: MonitoringAlertLevel
    message: str
    timestamp: datetime
    resolved: bool = False
    resolved_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmMonitoringStatus:
    """Current status of SWARM monitoring components."""
    messaging_system: HealthStatus = HealthStatus.UNKNOWN
    pyautogui_integration: HealthStatus = HealthStatus.UNKNOWN
    inbox_system: HealthStatus = HealthStatus.UNKNOWN
    agent_coordination: HealthStatus = HealthStatus.UNKNOWN
    coordinate_system: HealthStatus = HealthStatus.UNKNOWN
    message_queue: HealthStatus = HealthStatus.UNKNOWN
    last_updated: datetime = field(default_factory=datetime.now)
    active_alerts: list[MonitoringAlert] = field(default_factory=list)


class UnifiedMonitoringCoordinator:
    """
    Unified monitoring coordinator for SWARM messaging restoration.
    Integrates all monitoring systems with mission-specific alerting.
    """

    def __init__(self):
        """Initialize the unified monitoring coordinator."""
        self.logger = logging.getLogger(__name__)
        self.monitoring_status = SwarmMonitoringStatus()
        self.alert_history: list[MonitoringAlert] = []
        self.monitoring_thread: threading.Thread | None = None
        self.is_monitoring = False

        # Initialize monitoring systems
        self.health_check_system = None
        self.performance_dashboard = None
        self.operational_baseline = None

        self._initialize_monitoring_systems()

        # Alert thresholds
        self.alert_thresholds = {
            'response_time_max': 5.0,  # seconds
            'message_delivery_rate_min': 99.0,  # percentage
            'system_uptime_min': 99.9,  # percentage
            'queue_size_max': 100,  # messages
        }

    def _initialize_monitoring_systems(self):
        """Initialize all monitoring system components."""
        try:
            if AutomatedHealthCheckSystem:
                self.health_check_system = AutomatedHealthCheckSystem()
                self.logger.info("✅ Automated Health Check System initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to initialize health check system: {e}")

        try:
            if PerformanceMonitoringDashboard:
                self.performance_dashboard = PerformanceMonitoringDashboard()
                self.logger.info("✅ Performance Monitoring Dashboard initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to initialize performance dashboard: {e}")

        try:
            if OperationalMonitoringBaseline:
                self.operational_baseline = OperationalMonitoringBaseline()
                self.logger.info("✅ Operational Monitoring Baseline initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to initialize operational baseline: {e}")

    def start_monitoring(self, interval_seconds: int = 30):
        """
        Start the unified monitoring system.

        Args:
            interval_seconds: Monitoring interval in seconds
        """
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return

        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval_seconds,),
            daemon=True
        )
        self.monitoring_thread.start()
        self.logger.info(f"🚀 Unified monitoring started (interval: {interval_seconds}s)")

    def stop_monitoring(self):
        """Stop the unified monitoring system."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("⏹️ Unified monitoring stopped")

    def _monitoring_loop(self, interval_seconds: int):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                self._perform_monitoring_cycle()
                time.sleep(interval_seconds)
            except Exception as e:
                self.logger.error(f"Monitoring cycle error: {e}")
                self._create_alert(
                    SwarmComponent.AGENT_COORDINATION,
                    MonitoringAlertLevel.ERROR,
                    f"Monitoring cycle failed: {e}"
                )

    def _perform_monitoring_cycle(self):
        """Perform a complete monitoring cycle."""
        # Check messaging system health
        self._check_messaging_system()

        # Check PyAutoGUI integration
        self._check_pyautogui_integration()

        # Check inbox system
        self._check_inbox_system()

        # Check agent coordination
        self._check_agent_coordination()

        # Check coordinate system
        self._check_coordinate_system()

        # Check message queue
        self._check_message_queue()

        # Update timestamp
        self.monitoring_status.last_updated = datetime.now()

        # Log current status
        self._log_monitoring_status()

    def _check_messaging_system(self):
        """Check messaging system health."""
        try:
            # Check if messaging core is operational
            from .messaging_core import UnifiedMessagingCore
            messaging_core = UnifiedMessagingCore()

            # Perform health check
            health_result = messaging_core.validate_messaging_system()

            if health_result.get('status') == 'healthy':
                self.monitoring_status.messaging_system = HealthStatus.HEALTHY
            elif health_result.get('warnings'):
                self.monitoring_status.messaging_system = HealthStatus.WARNING
                self._create_alert(
                    SwarmComponent.MESSAGING_SYSTEM,
                    MonitoringAlertLevel.WARNING,
                    f"Messaging system warnings: {health_result.get('warnings')}"
                )
            else:
                self.monitoring_status.messaging_system = HealthStatus.CRITICAL
                self._create_alert(
                    SwarmComponent.MESSAGING_SYSTEM,
                    MonitoringAlertLevel.CRITICAL,
                    "Messaging system critical failure"
                )

        except Exception as e:
            self.monitoring_status.messaging_system = HealthStatus.CRITICAL
            self._create_alert(
                SwarmComponent.MESSAGING_SYSTEM,
                MonitoringAlertLevel.CRITICAL,
                f"Messaging system check failed: {e}"
            )

    def _check_pyautogui_integration(self):
        """Check PyAutoGUI integration health."""
        try:
            # Import and test PyAutoGUI
            import pyautogui

            # Test basic PyAutoGUI functionality
            screen_size = pyautogui.size()
            if screen_size and screen_size.width > 0 and screen_size.height > 0:
                self.monitoring_status.pyautogui_integration = HealthStatus.HEALTHY
            else:
                raise Exception("Invalid screen size")

        except Exception as e:
            self.monitoring_status.pyautogui_integration = HealthStatus.CRITICAL
            self._create_alert(
                SwarmComponent.PYAUTOGUI_INTEGRATION,
                MonitoringAlertLevel.CRITICAL,
                f"PyAutoGUI integration failed: {e}"
            )

    def _check_inbox_system(self):
        """Check inbox system health."""
        try:
            inbox_paths = []
            for i in range(1, 9):  # Check all 8 agent inboxes
                inbox_path = Path(f"agent_workspaces/Agent-{i}/inbox")
                inbox_paths.append(inbox_path)

            healthy_inboxes = sum(1 for path in inbox_paths if path.exists())

            if healthy_inboxes == 8:
                self.monitoring_status.inbox_system = HealthStatus.HEALTHY
            elif healthy_inboxes >= 6:
                self.monitoring_status.inbox_system = HealthStatus.WARNING
            else:
                self.monitoring_status.inbox_system = HealthStatus.CRITICAL
                self._create_alert(
                    SwarmComponent.INBOX_SYSTEM,
                    MonitoringAlertLevel.CRITICAL,
                    f"Only {healthy_inboxes}/8 agent inboxes operational"
                )

        except Exception as e:
            self.monitoring_status.inbox_system = HealthStatus.CRITICAL
            self._create_alert(
                SwarmComponent.INBOX_SYSTEM,
                MonitoringAlertLevel.CRITICAL,
                f"Inbox system check failed: {e}"
            )

    def _check_agent_coordination(self):
        """Check agent coordination health."""
        try:
            # Check coordinate loader
            from .coordinate_loader import get_coordinate_loader
            coord_loader = get_coordinate_loader()

            active_agents = len(coord_loader.get_all_agents())
            if active_agents == 8:
                self.monitoring_status.agent_coordination = HealthStatus.HEALTHY
            elif active_agents >= 6:
                self.monitoring_status.agent_coordination = HealthStatus.WARNING
            else:
                self.monitoring_status.agent_coordination = HealthStatus.CRITICAL
                self._create_alert(
                    SwarmComponent.AGENT_COORDINATION,
                    MonitoringAlertLevel.CRITICAL,
                    f"Only {active_agents}/8 agents coordinated"
                )

        except Exception as e:
            self.monitoring_status.agent_coordination = HealthStatus.CRITICAL
            self._create_alert(
                SwarmComponent.AGENT_COORDINATION,
                MonitoringAlertLevel.CRITICAL,
                f"Agent coordination check failed: {e}"
            )

    def _check_coordinate_system(self):
        """Check coordinate system health."""
        try:
            coord_file = Path("cursor_agent_coords.json")
            if coord_file.exists():
                with open(coord_file) as f:
                    coords_data = json.load(f)

                agents_with_coords = len(coords_data.get('agents', {}))
                if agents_with_coords == 8:
                    self.monitoring_status.coordinate_system = HealthStatus.HEALTHY
                else:
                    self.monitoring_status.coordinate_system = HealthStatus.WARNING
                    self._create_alert(
                        SwarmComponent.COORDINATE_SYSTEM,
                        MonitoringAlertLevel.WARNING,
                        f"Incomplete coordinate configuration: {agents_with_coords}/8 agents"
                    )
            else:
                raise FileNotFoundError("cursor_agent_coords.json not found")

        except Exception as e:
            self.monitoring_status.coordinate_system = HealthStatus.CRITICAL
            self._create_alert(
                SwarmComponent.COORDINATE_SYSTEM,
                MonitoringAlertLevel.CRITICAL,
                f"Coordinate system check failed: {e}"
            )

    def _check_message_queue(self):
        """Check message queue health."""
        try:
            queue_file = Path("message_queue/queue.json")
            if queue_file.exists():
                with open(queue_file) as f:
                    queue_data = json.load(f)

                queue_size = len(queue_data)
                if queue_size <= self.alert_thresholds['queue_size_max']:
                    self.monitoring_status.message_queue = HealthStatus.HEALTHY
                else:
                    self.monitoring_status.message_queue = HealthStatus.WARNING
                    self._create_alert(
                        SwarmComponent.MESSAGE_QUEUE,
                        MonitoringAlertLevel.WARNING,
                        f"Message queue size ({queue_size}) exceeds threshold ({self.alert_thresholds['queue_size_max']})"
                    )
            else:
                # Queue doesn't exist yet, which is okay
                self.monitoring_status.message_queue = HealthStatus.HEALTHY

        except Exception as e:
            self.monitoring_status.message_queue = HealthStatus.WARNING
            self._create_alert(
                SwarmComponent.MESSAGE_QUEUE,
                MonitoringAlertLevel.WARNING,
                f"Message queue check failed: {e}"
            )

    def _create_alert(self, component: SwarmComponent, level: MonitoringAlertLevel,
                     message: str, metadata: dict[str, Any] | None = None):
        """Create a new monitoring alert."""
        alert = MonitoringAlert(
            alert_id=f"alert_{int(time.time())}_{component.value}",
            component=component,
            level=level,
            message=message,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )

        self.monitoring_status.active_alerts.append(alert)
        self.alert_history.append(alert)

        self.logger.warning(f"🚨 ALERT [{level.value.upper()}]: {component.value} - {message}")

    def _log_monitoring_status(self):
        """Log current monitoring status."""
        status_summary = {
            'timestamp': self.monitoring_status.last_updated.isoformat(),
            'messaging_system': self.monitoring_status.messaging_system.value,
            'pyautogui_integration': self.monitoring_status.pyautogui_integration.value,
            'inbox_system': self.monitoring_status.inbox_system.value,
            'agent_coordination': self.monitoring_status.agent_coordination.value,
            'coordinate_system': self.monitoring_status.coordinate_system.value,
            'message_queue': self.monitoring_status.message_queue.value,
            'active_alerts': len(self.monitoring_status.active_alerts)
        }

        self.logger.info(f"📊 Monitoring Status: {json.dumps(status_summary, indent=2)}")

    def get_monitoring_report(self) -> dict[str, Any]:
        """Generate a comprehensive monitoring report."""
        return {
            'timestamp': datetime.now().isoformat(),
            'monitoring_status': {
                'messaging_system': self.monitoring_status.messaging_system.value,
                'pyautogui_integration': self.monitoring_status.pyautogui_integration.value,
                'inbox_system': self.monitoring_status.inbox_system.value,
                'agent_coordination': self.monitoring_status.agent_coordination.value,
                'coordinate_system': self.monitoring_status.coordinate_system.value,
                'message_queue': self.monitoring_status.message_queue.value,
                'last_updated': self.monitoring_status.last_updated.isoformat()
            },
            'active_alerts': [
                {
                    'alert_id': alert.alert_id,
                    'component': alert.component.value,
                    'level': alert.level.value,
                    'message': alert.message,
                    'timestamp': alert.timestamp.isoformat(),
                    'resolved': alert.resolved
                }
                for alert in self.monitoring_status.active_alerts
            ],
            'alert_history_count': len(self.alert_history),
            'alert_thresholds': self.alert_thresholds
        }

    def resolve_alert(self, alert_id: str):
        """Resolve a monitoring alert."""
        for alert in self.monitoring_status.active_alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                self.logger.info(f"✅ Alert resolved: {alert_id}")
                break


def get_monitoring_coordinator() -> UnifiedMonitoringCoordinator:
    """Get global monitoring coordinator instance."""
    if not hasattr(get_monitoring_coordinator, '_instance'):
        get_monitoring_coordinator._instance = UnifiedMonitoringCoordinator()
    return get_monitoring_coordinator._instance


if __name__ == "__main__":
    # Example usage
    coordinator = get_monitoring_coordinator()
    coordinator.start_monitoring(interval_seconds=30)

    try:
        # Keep monitoring active
        while True:
            time.sleep(60)  # Check every minute
            report = coordinator.get_monitoring_report()
            print(json.dumps(report, indent=2))
    except KeyboardInterrupt:
        coordinator.stop_monitoring()
