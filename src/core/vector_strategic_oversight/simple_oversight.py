#!/usr/bin/env python3
"""
Simple Strategic Oversight - KISS Compliant
==========================================

Simple strategic oversight utilities.
KISS PRINCIPLE: Keep It Simple, Stupid.

Author: Agent-6 - Coordination & Communication Specialist
License: MIT
"""

from datetime import datetime
from typing import Any


class SimpleStrategicOversight:
    """Simple strategic oversight utilities."""

    def __init__(self):
        self.reports: list[dict] = []

    def create_report(self, title: str, content: str) -> dict[str, Any]:
        """Create a simple strategic report."""
        report = {
            "id": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": title,
            "content": content,
            "created_at": datetime.now(),
        }
        self.reports.append(report)
        return report

    def get_reports(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent reports."""
        return self.reports[-limit:] if limit else self.reports

    def analyze_performance(self, data: dict[str, Any]) -> dict[str, Any]:
        """Simple performance analysis."""
        return {
            "status": "good" if data.get("score", 0) > 0.7 else "needs_improvement",
            "score": data.get("score", 0),
            "recommendations": (
                ["Monitor closely"] if data.get("score", 0) < 0.7 else ["Continue current approach"]
            ),
            "analyzed_at": datetime.now(),
        }

    def generate_insights(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Generate simple insights."""
        insights = []
        for item in data:
            if item.get("priority") == "high":
                insights.append(
                    {
                        "type": "high_priority_alert",
                        "message": f"High priority item: {item.get('name', 'Unknown')}",
                        "timestamp": datetime.now(),
                    }
                )
        return insights
