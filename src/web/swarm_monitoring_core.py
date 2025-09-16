#!/usr/bin/env python3
"""
Swarm Monitoring Core - Core monitoring functionality
====================================================

Core monitoring logic extracted from swarm_monitoring_dashboard.py
V2 compliant: ≤400 lines, focused responsibility
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AgentStatus(BaseModel):
    """Agent status model."""

    agent_id: str
    status: str
    current_phase: str
    last_updated: datetime
    current_mission: str | None = None
    mission_priority: str | None = None
    progress_percentage: float | None = None
    active_tasks: list[str] = []
    completed_tasks: list[str] = []
    coordination_status: dict[str, Any] = {}


class Alert(BaseModel):
    """Alert model."""

    alert_id: str
    level: str
    message: str
    component: str
    timestamp: datetime
    resolved: bool = False


class SystemMetrics(BaseModel):
    """System metrics model."""

    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: dict[str, Any]
    active_connections: int


class SwarmMonitoringCore:
    """Core swarm monitoring functionality."""

    def __init__(self, workspace_path: str = "agent_workspaces"):
        """Initialize monitoring core."""
        self.workspace_path = Path(workspace_path)
        self.agents: dict[str, AgentStatus] = {}
        self.alerts: list[Alert] = []
        self.metrics_history: list[SystemMetrics] = []
        self.max_history = 1000

        logger.info("Swarm monitoring core initialized")

    def load_agent_status(self, agent_id: str) -> AgentStatus | None:
        """Load agent status from workspace."""
        try:
            status_file = self.workspace_path / agent_id / "status.json"
            if status_file.exists():
                with open(status_file) as f:
                    data = json.load(f)
                    return AgentStatus(**data)
        except Exception as e:
            logger.error(f"Failed to load status for {agent_id}: {e}")
        return None

    def update_agent_status(self, agent_id: str, status_data: dict[str, Any]) -> bool:
        """Update agent status."""
        try:
            status = AgentStatus(agent_id=agent_id, last_updated=datetime.now(), **status_data)
            self.agents[agent_id] = status

            # Save to file
            status_file = self.workspace_path / agent_id / "status.json"
            status_file.parent.mkdir(parents=True, exist_ok=True)
            with open(status_file, "w") as f:
                json.dump(status.dict(), f, default=str, indent=2)

            return True
        except Exception as e:
            logger.error(f"Failed to update status for {agent_id}: {e}")
            return False

    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics."""
        try:
            if PSUTIL_AVAILABLE:
                cpu_usage = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage("/")
                network = psutil.net_io_counters()

                metrics = SystemMetrics(
                    timestamp=datetime.now(),
                    cpu_usage=cpu_usage,
                    memory_usage=memory.percent,
                    disk_usage=disk.percent,
                    network_io={
                        "bytes_sent": network.bytes_sent,
                        "bytes_recv": network.bytes_recv,
                        "packets_sent": network.packets_sent,
                        "packets_recv": network.packets_recv,
                    },
                    active_connections=len(psutil.net_connections()),
                )
            else:
                metrics = SystemMetrics(
                    timestamp=datetime.now(),
                    cpu_usage=0.0,
                    memory_usage=0.0,
                    disk_usage=0.0,
                    network_io={},
                    active_connections=0,
                )

            # Add to history
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.max_history:
                self.metrics_history.pop(0)

            return metrics
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return SystemMetrics(
                timestamp=datetime.now(),
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={},
                active_connections=0,
            )

    def create_alert(self, level: str, message: str, component: str) -> str:
        """Create new alert."""
        alert_id = f"alert_{int(time.time())}"
        alert = Alert(
            alert_id=alert_id,
            level=level,
            message=message,
            component=component,
            timestamp=datetime.now(),
        )
        self.alerts.append(alert)
        logger.warning(f"Alert created: {level} - {message}")
        return alert_id

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve alert by ID."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"Alert resolved: {alert_id}")
                return True
        return False

    def get_active_alerts(self) -> list[Alert]:
        """Get all active (unresolved) alerts."""
        return [alert for alert in self.alerts if not alert.resolved]

    def get_agent_summary(self) -> dict[str, Any]:
        """Get summary of all agents."""
        summary = {
            "total_agents": len(self.agents),
            "active_agents": 0,
            "agents_by_status": {},
            "agents_by_phase": {},
            "recent_activity": [],
        }

        for agent_id, status in self.agents.items():
            # Count by status
            if status.status not in summary["agents_by_status"]:
                summary["agents_by_status"][status.status] = 0
            summary["agents_by_status"][status.status] += 1

            # Count by phase
            if status.current_phase not in summary["agents_by_phase"]:
                summary["agents_by_phase"][status.current_phase] = 0
            summary["agents_by_phase"][status.current_phase] += 1

            # Track active agents
            if status.status == "active":
                summary["active_agents"] += 1

            # Recent activity (last 5 minutes)
            if (datetime.now() - status.last_updated).seconds < 300:
                summary["recent_activity"].append(
                    {
                        "agent_id": agent_id,
                        "status": status.status,
                        "mission": status.current_mission,
                        "last_updated": status.last_updated,
                    }
                )

        return summary

    def get_metrics_summary(self) -> dict[str, Any]:
        """Get metrics summary."""
        if not self.metrics_history:
            return {"error": "No metrics available"}

        latest = self.metrics_history[-1]
        summary = {
            "current": {
                "cpu_usage": latest.cpu_usage,
                "memory_usage": latest.memory_usage,
                "disk_usage": latest.disk_usage,
                "active_connections": latest.active_connections,
            },
            "trends": self._calculate_trends(),
            "timestamp": latest.timestamp,
        }

        return summary

    def _calculate_trends(self) -> dict[str, Any]:
        """Calculate metric trends."""
        if len(self.metrics_history) < 2:
            return {"cpu_trend": 0, "memory_trend": 0, "disk_trend": 0}

        recent = self.metrics_history[-5:]  # Last 5 measurements
        older = self.metrics_history[-10:-5] if len(self.metrics_history) >= 10 else []

        if not older:
            return {"cpu_trend": 0, "memory_trend": 0, "disk_trend": 0}

        def avg_metric(metrics, metric_name):
            return sum(getattr(m, metric_name) for m in metrics) / len(metrics)

        trends = {
            "cpu_trend": avg_metric(recent, "cpu_usage") - avg_metric(older, "cpu_usage"),
            "memory_trend": avg_metric(recent, "memory_usage") - avg_metric(older, "memory_usage"),
            "disk_trend": avg_metric(recent, "disk_usage") - avg_metric(older, "disk_usage"),
        }

        return trends

    def cleanup_old_data(self) -> None:
        """Clean up old metrics and alerts."""
        # Keep only recent alerts (last 24 hours)
        cutoff = datetime.now().timestamp() - 86400
        self.alerts = [alert for alert in self.alerts if alert.timestamp.timestamp() > cutoff]

        # Metrics history is already limited by max_history
        logger.info("Old data cleanup completed")

    def get_health_status(self) -> dict[str, Any]:
        """Get overall system health status."""
        active_alerts = self.get_active_alerts()
        critical_alerts = [a for a in active_alerts if a.level == "critical"]
        warning_alerts = [a for a in active_alerts if a.level == "warning"]

        health_score = 100
        if critical_alerts:
            health_score -= len(critical_alerts) * 20
        if warning_alerts:
            health_score -= len(warning_alerts) * 5

        health_score = max(0, health_score)

        return {
            "health_score": health_score,
            "status": (
                "healthy"
                if health_score >= 80
                else "degraded"
                if health_score >= 50
                else "critical"
            ),
            "critical_alerts": len(critical_alerts),
            "warning_alerts": len(warning_alerts),
            "total_alerts": len(active_alerts),
            "active_agents": len([a for a in self.agents.values() if a.status == "active"]),
        }
