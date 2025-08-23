#!/usr/bin/env python3
"""
Monitor Alerts - Agent Cellphone V2
===================================

Alert system for monitoring and health issues.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass

from .monitor_types import AgentInfo, AgentStatus


class AlertLevel(Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of alerts"""

    AGENT_OFFLINE = "agent_offline"
    PERFORMANCE_DEGRADED = "performance_degraded"
    SYSTEM_RESOURCE_LOW = "system_resource_low"
    HEALTH_ISSUE = "health_issue"
    CONNECTIVITY_PROBLEM = "connectivity_problem"
    WORKSPACE_ISSUE = "workspace_issue"


@dataclass
class Alert:
    """Alert information"""

    alert_id: str
    alert_type: AlertType
    level: AlertLevel
    message: str
    timestamp: float
    agent_id: Optional[str]
    details: Dict[str, Any]
    acknowledged: bool = False
    resolved: bool = False


class AlertManager:
    """
    Manages monitoring alerts and notifications.

    Responsibilities:
    - Generate alerts for monitoring issues
    - Manage alert lifecycle
    - Provide alert notifications
    - Track alert history
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AlertManager")
        self.alerts: List[Alert] = []
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        self.alert_thresholds = {"max_alerts": 1000, "alert_retention_hours": 24}

    def create_alert(
        self,
        alert_type: AlertType,
        level: AlertLevel,
        message: str,
        agent_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> Alert:
        """Create a new alert"""
        alert_id = f"{alert_type.value}_{int(time.time())}_{agent_id or 'system'}"

        alert = Alert(
            alert_id=alert_id,
            alert_type=alert_type,
            level=level,
            message=message,
            timestamp=time.time(),
            agent_id=agent_id,
            details=details or {},
        )

        self.alerts.append(alert)
        self.logger.info(f"Alert created: {level.value} - {message}")

        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Alert callback error: {e}")

        # Cleanup old alerts
        self._cleanup_old_alerts()

        return alert

    def create_agent_offline_alert(
        self, agent_id: str, details: Optional[Dict[str, Any]] = None
    ) -> Alert:
        """Create alert for agent going offline"""
        message = f"Agent {agent_id} is offline"
        return self.create_alert(
            AlertType.AGENT_OFFLINE, AlertLevel.WARNING, message, agent_id, details
        )

    def create_performance_alert(
        self,
        agent_id: str,
        performance_score: float,
        details: Optional[Dict[str, Any]] = None,
    ) -> Alert:
        """Create alert for performance issues"""
        if performance_score < 0.3:
            level = AlertLevel.CRITICAL
            message = f"Agent {agent_id} has critical performance issues (score: {performance_score})"
        elif performance_score < 0.5:
            level = AlertLevel.ERROR
            message = f"Agent {agent_id} has degraded performance (score: {performance_score})"
        else:
            level = AlertLevel.WARNING
            message = f"Agent {agent_id} has performance warnings (score: {performance_score})"

        return self.create_alert(
            AlertType.PERFORMANCE_DEGRADED, level, message, agent_id, details
        )

    def create_system_resource_alert(
        self,
        resource_type: str,
        usage_percent: float,
        details: Optional[Dict[str, Any]] = None,
    ) -> Alert:
        """Create alert for system resource issues"""
        if usage_percent > 95:
            level = AlertLevel.CRITICAL
            message = f"Critical {resource_type} usage: {usage_percent}%"
        elif usage_percent > 85:
            level = AlertLevel.WARNING
            message = f"High {resource_type} usage: {usage_percent}%"
        else:
            level = AlertLevel.INFO
            message = f"{resource_type} usage: {usage_percent}%"

        return self.create_alert(
            AlertType.SYSTEM_RESOURCE_LOW, level, message, details=details
        )

    def create_health_alert(
        self,
        agent_id: str,
        health_score: float,
        warnings: List[str],
        details: Optional[Dict[str, Any]] = None,
    ) -> Alert:
        """Create alert for health issues"""
        if health_score < 30:
            level = AlertLevel.CRITICAL
            message = (
                f"Agent {agent_id} has critical health issues (score: {health_score})"
            )
        elif health_score < 60:
            level = AlertLevel.ERROR
            message = f"Agent {agent_id} has health problems (score: {health_score})"
        else:
            level = AlertLevel.WARNING
            message = f"Agent {agent_id} has health warnings (score: {health_score})"

        if details is None:
            details = {}
        details["warnings"] = warnings

        return self.create_alert(
            AlertType.HEALTH_ISSUE, level, message, agent_id, details
        )

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Mark alert as acknowledged"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                alert.details["acknowledged_at"] = time.time()
                self.logger.info(f"Alert {alert_id} acknowledged")
                return True
        return False

    def resolve_alert(
        self, alert_id: str, resolution_notes: Optional[str] = None
    ) -> bool:
        """Mark alert as resolved"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                alert.details["resolved_at"] = time.time()
                if resolution_notes:
                    alert.details["resolution_notes"] = resolution_notes
                self.logger.info(f"Alert {alert_id} resolved")
                return True
        return False

    def get_active_alerts(self, level: Optional[AlertLevel] = None) -> List[Alert]:
        """Get active (unresolved) alerts"""
        active = [a for a in self.alerts if not a.resolved]
        if level:
            active = [a for a in active if a.level == level]
        return active

    def get_alert_summary(self) -> Dict[str, Any]:
        """Get comprehensive alert summary"""
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts if not a.resolved])
        acknowledged_alerts = len(
            [a for a in self.alerts if a.acknowledged and not a.resolved]
        )
        resolved_alerts = len([a for a in self.alerts if a.resolved])

        # Count by level
        level_counts = {}
        for level in AlertLevel:
            level_counts[level.value] = len(
                [a for a in self.alerts if a.level == level]
            )

        # Count by type
        type_counts = {}
        for alert_type in AlertType:
            type_counts[alert_type.value] = len(
                [a for a in self.alerts if a.alert_type == alert_type]
            )

        return {
            "timestamp": time.time(),
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "acknowledged_alerts": acknowledged_alerts,
            "resolved_alerts": resolved_alerts,
            "by_level": level_counts,
            "by_type": type_counts,
        }

    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Add callback for new alerts"""
        if callback not in self.alert_callbacks:
            self.alert_callbacks.append(callback)

    def remove_alert_callback(self, callback: Callable[[Alert], None]):
        """Remove alert callback"""
        if callback in self.alert_callbacks:
            self.alert_callbacks.remove(callback)

    def _cleanup_old_alerts(self):
        """Remove old alerts based on retention policy"""
        current_time = time.time()
        retention_seconds = self.alert_thresholds["alert_retention_hours"] * 3600

        # Remove alerts older than retention period
        self.alerts = [
            a for a in self.alerts if current_time - a.timestamp < retention_seconds
        ]

        # Limit total alerts
        if len(self.alerts) > self.alert_thresholds["max_alerts"]:
            # Remove oldest alerts first
            self.alerts.sort(key=lambda x: x.timestamp)
            self.alerts = self.alerts[-self.alert_thresholds["max_alerts"] :]

    def set_alert_thresholds(self, thresholds: Dict[str, Any]):
        """Update alert thresholds"""
        for key, value in thresholds.items():
            if key in self.alert_thresholds:
                self.alert_thresholds[key] = value
                self.logger.info(f"Updated alert threshold {key}: {value}")

    def get_alert_thresholds(self) -> Dict[str, Any]:
        """Get current alert thresholds"""
        return self.alert_thresholds.copy()
