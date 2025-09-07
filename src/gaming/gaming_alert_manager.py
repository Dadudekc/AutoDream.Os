<<<<<<< HEAD
"""Gaming Alert Manager.

Manages alerts and notifications for gaming and entertainment systems,
providing real-time monitoring and alert handling capabilities.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Implementation - Gaming Infrastructure Refactoring
Status: REFACTORED_FOR_V2_COMPLIANCE
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum

from src.core.alert_system import (
    create_alert_id,
    validate_alert_metadata,
    format_alert_message,
    calculate_alert_priority,
)
from src.services.alert_handlers import (
    handle_performance_alerts,
    handle_system_health_alerts,
    handle_alert_acknowledgment,
    handle_alert_resolution,
)

logger = logging.getLogger(__name__)


class GamingAlertManager:
    """Manages alerts for gaming and entertainment systems.

    Provides comprehensive alert handling including creation, acknowledgment,
    resolution, and monitoring capabilities.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the gaming alert manager."""
        self.config = config or {}
        self.alerts: Dict[str, GamingAlert] = {}
        self.alert_counters = {alert_type: 0 for alert_type in AlertType}
        self.severity_thresholds = {
            AlertSeverity.LOW: 10,
            AlertSeverity.MEDIUM: 5,
            AlertSeverity.HIGH: 3,
            AlertSeverity.CRITICAL: 1,
        }
        self._initialize_resources()

    def _initialize_resources(self):
        """Initialize alert manager resources."""
        get_logger(__name__).info("Initializing Gaming Alert Manager resources")
        self._load_alert_history()
        self._setup_monitoring()

    def _load_alert_history(self):
        """Load alert history from persistent storage."""
        try:
            get_logger(__name__).info("Loading alert history")
        except Exception as e:
            get_logger(__name__).warning(f"Could not load alert history: {e}")

    def _setup_monitoring(self):
        """Setup monitoring for gaming systems."""
        get_logger(__name__).info("Setting up gaming system monitoring")

    def _get_current_timestamp(self):
        """Get current timestamp for consistency."""
        return datetime.now()

    def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        message: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> GamingAlert:
        """Create a new gaming alert.

        Args:
            alert_type: Type of alert
            severity: Alert severity level
            message: Alert message
            source: Source system
            metadata: Additional alert metadata

        Returns:
            Created GamingAlert instance
        """
        alert_id = create_alert_id(alert_type, len(self.alerts))
        validated_metadata = validate_alert_metadata(metadata or {})

        alert = GamingAlert(
            id=alert_id,
            type=alert_type,
            severity=severity,
            message=message,
            timestamp=self._get_current_timestamp(),
            source=source,
            metadata=validated_metadata,
        )

        self.alerts[alert_id] = alert
        self.alert_counters[alert_type] += 1

        get_logger(__name__).info(f"Created gaming alert: {alert_id} - {message}")
        return alert

    def check_performance_alerts(
        self, performance_metrics: Dict[str, Any]
    ) -> List[GamingAlert]:
        """Check for performance-related alerts based on metrics."""
        return handle_performance_alerts(self, performance_metrics)

    def check_system_health_alerts(
        self, health_metrics: Dict[str, Any]
    ) -> List[GamingAlert]:
        """Check for system health alerts."""
        return handle_system_health_alerts(self, health_metrics)

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert."""
        return handle_alert_acknowledgment(self, alert_id, acknowledged_by)

    def resolve_alert(
        self, alert_id: str, resolved_by: str, resolution_notes: str = ""
    ) -> bool:
        """Resolve an alert."""
        return handle_alert_resolution(self, alert_id, resolved_by, resolution_notes)

    def get_active_alerts(
        self, alert_type: Optional[AlertType] = None
    ) -> List[GamingAlert]:
        """Get all active (unresolved) alerts.

        Args:
            alert_type: Optional filter by alert type

        Returns:
            List of active alerts
        """
        active_alerts = [alert for alert in self.alerts.values() if not alert.resolved]

        if alert_type:
            active_alerts = [
                alert for alert in active_alerts if alert.type == alert_type
            ]

        return active_alerts

    def get_alert_summary(self) -> Dict[str, Any]:
        """Get a summary of all alerts.

        Returns:
            Dictionary containing alert summary statistics
        """
        total_alerts = len(self.alerts)
        active_alerts = len(self.get_active_alerts())
        resolved_alerts = total_alerts - active_alerts

        alerts_by_type = {}
        alerts_by_severity = {}

        for alert in self.alerts.values():
            # Count by type
            alert_type = alert.type.value
            alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1

            # Count by severity
            severity = alert.severity.value
            alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1

        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "alerts_by_type": alerts_by_type,
            "alerts_by_severity": alerts_by_severity,
            "alert_counters": self.alert_counters,
        }

    def clear_resolved_alerts(self, older_than_days: int = 30) -> int:
        """Clear resolved alerts older than specified days.

        Args:
            older_than_days: Remove alerts resolved more than this many days ago

        Returns:
            Number of alerts cleared
        """
        cutoff_time = datetime.now().timestamp() - (older_than_days * 24 * 60 * 60)

        alerts_to_remove = [
            alert_id
            for alert_id, alert in self.alerts.items()
            if alert.resolved
            and alert.resolved_at
            and alert.resolved_at.timestamp() < cutoff_time
        ]

        for alert_id in alerts_to_remove:
            del self.alerts[alert_id]

        get_logger(__name__).info(f"Cleared {len(alerts_to_remove)} resolved alerts")
        return len(alerts_to_remove)

    def set_alert_threshold(
        self, alert_type: AlertType, severity: AlertSeverity, threshold: int
    ):
        """Set threshold for alert severity levels.

        Args:
            alert_type: Type of alert
            severity: Severity level
            threshold: Threshold value
        """
        self.severity_thresholds[severity] = threshold
        get_logger(__name__).info(
            f"Set threshold for {alert_type.value} {severity.value}: {threshold}"
        )

    def export_alerts(self, filepath: str) -> bool:
        """Export alerts to JSON file.

        Args:
            filepath: Path to export file

        Returns:
            True if export successful, False otherwise
        """
        try:
            export_data = {
                "alerts": [alert.__dict__ for alert in self.alerts.values()],
                "summary": self.get_alert_summary(),
                "export_timestamp": datetime.now().isoformat(),
            }

            with open(filepath, "w") as f:
                write_json(export_data, f, indent=2, default=str)

            get_logger(__name__).info(f"Exported alerts to {filepath}")
            return True
        except Exception as e:
            get_logger(__name__).error(f"Failed to export alerts: {e}")
            return False
=======
"""Backward compatible import for GamingAlertManager."""
from .alerts.orchestrator import GamingAlertManager

__all__ = ["GamingAlertManager"]
>>>>>>> origin/codex/catalog-functions-in-utils-directories
