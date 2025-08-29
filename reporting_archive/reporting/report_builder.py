from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

from .models import HealthReport, ReportConfig, ReportType, ReportFormat
from __future__ import annotations
import time


"""Core report generation logic extracted from the legacy generator."""



logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate :class:`HealthReport` instances from raw data."""

    def __init__(self, charts_dir: str | Path | None = None) -> None:
        self.charts_dir = Path(charts_dir or "health_charts")
        self.charts_dir.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_report(
        self, health_data: Dict[str, Any], alerts_data: Dict[str, Any], config: ReportConfig
    ) -> HealthReport:
        """Create a fully populated :class:`HealthReport`."""

        report_id = f"health_report_{config.report_type.value}_{int(time.time())}"
        time_range = self._determine_time_range(config)

        summary = self._generate_summary(health_data, alerts_data, time_range)
        metrics = self._generate_metrics_data(health_data)
        alerts = self._generate_alerts_data(alerts_data)

        report = HealthReport(
            report_id=report_id,
            report_type=config.report_type,
            format=config.format,
            generated_at=datetime.now(),
            time_range=time_range,
            summary=summary,
            metrics_data=metrics,
            alerts_data=alerts,
            charts=[],
            recommendations=[],
            metadata={"generator_version": "1.0.0"},
        )
        return report

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _determine_time_range(self, config: ReportConfig) -> Dict[str, datetime]:
        end_time = datetime.now()
        if config.time_range:
            return config.time_range
        if config.report_type == ReportType.DAILY_SUMMARY:
            start_time = end_time - timedelta(hours=24)
        elif config.report_type == ReportType.WEEKLY_ANALYSIS:
            start_time = end_time - timedelta(days=7)
        elif config.report_type == ReportType.MONTHLY_TREND:
            start_time = end_time - timedelta(days=30)
        else:
            start_time = end_time - timedelta(hours=24)
        return {"start": start_time, "end": end_time}

    def _generate_summary(
        self, health_data: Dict[str, Any], alerts_data: Dict[str, Any], time_range: Dict[str, datetime]
    ) -> Dict[str, Any]:
        agents = health_data.get("agents", {})
        total_agents = len(agents)
        avg_score = 0.0
        status_counts: Dict[str, int] = {}
        for agent in agents.values():
            status = agent.get("overall_status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
            avg_score += float(agent.get("health_score", 0.0))
        if total_agents:
            avg_score /= total_agents

        alerts = alerts_data.get("alerts", [])
        alert_counts: Dict[str, int] = {}
        for alert in alerts:
            sev = alert.get("severity", "unknown")
            alert_counts[sev] = alert_counts.get(sev, 0) + 1

        return {
            "overall_health": "good" if avg_score >= 80 else "fair",
            "total_agents": total_agents,
            "agents_by_status": status_counts,
            "average_health_score": round(avg_score, 2),
            "total_alerts": len(alerts),
            "alerts_by_severity": alert_counts,
            "time_range": {
                "start": time_range["start"].isoformat(),
                "end": time_range["end"].isoformat(),
            },
        }

    def _generate_metrics_data(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        agents = health_data.get("agents", {})
        metrics: Dict[str, Any] = {}
        for agent_id, agent_data in agents.items():
            metrics[agent_id] = {
                "overall_status": agent_data.get("overall_status", "unknown"),
                "health_score": agent_data.get("health_score", 0.0),
                "metrics": agent_data.get("metrics", {}),
            }
        return metrics

    def _generate_alerts_data(self, alerts_data: Dict[str, Any]) -> Dict[str, Any]:
        alerts = alerts_data.get("alerts", [])
        return {"alerts": alerts, "total_alerts": len(alerts)}
