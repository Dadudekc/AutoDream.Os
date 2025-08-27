"""Health report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class HealthReportGenerator(ReportGenerator):
    """Generates health reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a health report."""
        health_data = data.get("health_data", {})
        alerts = data.get("alerts", [])

        total_agents = len(health_data.get("agents", {}))
        healthy_agents = sum(
            1
            for a in health_data.get("agents", {}).values()
            if a.get("overall_status") == "good"
        )
        total_alerts = len(alerts)
        critical_alerts = sum(1 for a in alerts if a.get("severity") == "critical")

        content = {
            "health_summary": {
                "total_agents": total_agents,
                "healthy_agents": healthy_agents,
                "health_percentage": (
                    healthy_agents / total_agents * 100 if total_agents > 0 else 0
                ),
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts,
            },
            "agents": health_data.get("agents", {}),
            "alerts": alerts,
        }

        summary = (
            f"Health Report: {healthy_agents}/{total_agents} agents healthy "
            f"({content['health_summary']['health_percentage']:.1f}% health rate)"
        )

        recommendations = []
        if content["health_summary"]["health_percentage"] < 80:
            recommendations.append("System health below 80% - investigate agent issues")
        if critical_alerts > 0:
            recommendations.append(
                f"{critical_alerts} critical alerts - immediate attention required"
            )

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.HEALTH,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_health_system",
        )

        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations,
        )
