#!/usr/bin/env python3
"""Health checking and reporting utilities for the Status Manager."""

import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .agent_manager import AgentInfo, AgentStatus
from .health.health_monitor_alerts import AlertLevel
from .health_models import HealthStatus
from .status_manager_config import Alert, HealthCheck


class StatusReporterMixin:
    """Mixin providing health checking and reporting behaviour."""

    health_checks: Dict[str, HealthCheck]
    alerts: Dict[str, Alert]

    def _health_check_loop(self) -> None:
        """Main health check loop."""
        while self.running:
            try:
                self._perform_system_health_checks()
                self._process_health_alerts()
                time.sleep(60)
            except Exception as e:  # pragma: no cover - defensive logging
                self.logger.error(f"Health check loop error: {e}")
                time.sleep(120)

    def _perform_system_health_checks(self) -> None:
        """Perform system-wide health checks."""
        try:
            agents = self.agent_manager.get_all_agents()
            for agent_id, agent_info in agents.items():
                health_status = self._check_agent_health(agent_id, agent_info)
                health_check = HealthCheck(
                    check_id=str(uuid.uuid4()),
                    agent_id=agent_id,
                    check_type="agent_health",
                    status=health_status,
                    message=f"Health check for {agent_id}",
                    timestamp=datetime.now().isoformat(),
                    details={"agent_status": agent_info.status.value},
                )
                self.health_checks[health_check.check_id] = health_check
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to perform system health checks: {e}")

    def _check_agent_health(self, agent_id: str, agent_info: AgentInfo) -> HealthStatus:
        """Check health of a specific agent."""
        try:
            if agent_info.status == AgentStatus.OFFLINE:
                return HealthStatus.CRITICAL
            if agent_info.status == AgentStatus.OVERLOADED:
                return HealthStatus.WARNING
            if agent_info.status == AgentStatus.ONLINE:
                return HealthStatus.HEALTHY
            return HealthStatus.UNKNOWN
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to check health for {agent_id}: {e}")
            return HealthStatus.UNKNOWN

    def _process_health_alerts(self) -> None:
        """Process health check alerts."""
        try:
            for check_id, health_check in self.health_checks.items():
                if health_check.status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
                    alert_level = (
                        AlertLevel.CRITICAL
                        if health_check.status == HealthStatus.CRITICAL
                        else AlertLevel.WARNING
                    )
                    alert = Alert(
                        alert_id=str(uuid.uuid4()),
                        level=alert_level,
                        message=f"Health check failed for {health_check.agent_id}: {health_check.message}",
                        source="health_check",
                        timestamp=datetime.now().isoformat(),
                        acknowledged=False,
                        metadata={
                            "check_id": check_id,
                            "health_status": health_check.status.value,
                        },
                    )
                    self.alerts[alert.alert_id] = alert
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to process health alerts: {e}")

    def get_health_status(self, agent_id: str) -> Optional[HealthStatus]:
        """Get current health status for an agent."""
        try:
            recent_checks = [
                check
                for check in self.health_checks.values()
                if check.agent_id == agent_id
            ]
            if recent_checks:
                latest_check = max(recent_checks, key=lambda x: x.timestamp)
                return latest_check.status
            return None
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to get health status for {agent_id}: {e}")
            return None

    def get_active_alerts(self, level: Optional[AlertLevel] = None) -> List[Alert]:
        """Get active alerts, optionally filtered by level."""
        try:
            if level:
                return [
                    alert
                    for alert in self.alerts.values()
                    if alert.level == level and not alert.acknowledged
                ]
            return [alert for alert in self.alerts.values() if not alert.acknowledged]
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to get active alerts: {e}")
            return []

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        try:
            if alert_id in self.alerts:
                self.alerts[alert_id].acknowledged = True
                self.logger.info(f"Alert {alert_id} acknowledged")
                return True
            return False
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            return False

    def get_status_summary(self) -> Dict[str, Any]:
        """Get summary of status system."""
        try:
            total_agents = len(self.agent_manager.get_all_agents())
            online_agents = len(
                [
                    a
                    for a in self.agent_manager.get_all_agents().values()
                    if a.status == AgentStatus.ONLINE
                ]
            )
            total_alerts = len(self.alerts)
            active_alerts = len(self.get_active_alerts())
            return {
                "total_agents": total_agents,
                "online_agents": online_agents,
                "offline_agents": total_agents - online_agents,
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "monitoring_active": self.running,
                "health_checks": len(self.health_checks),
            }
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to get status summary: {e}")
            return {"error": str(e)}


__all__ = ["StatusReporterMixin"]
