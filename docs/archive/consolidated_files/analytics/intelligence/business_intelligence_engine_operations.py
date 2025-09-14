#!/usr/bin/env python3
"""
Business Intelligence Engine Operations - V2 Compliance Module
==============================================================

Extended operations for business intelligence.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

import logging
import statistics
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class BusinessIntelligenceEngineOperations:
    """Extended operations for business intelligence."""

    def __init__(self, config=None):
        """Initialize business intelligence engine operations."""
        self.config = config or {}
        self.logger = logger
        self.insights = []
        self.metrics = {}

    def generate_dashboard_data(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Generate dashboard data for visualization."""
        try:
            if not data:
                return {"error": "No data provided"}

            # Generate dashboard metrics
            dashboard = {
                "summary": self._generate_summary(data),
                "charts": self._generate_chart_data(data),
                "alerts": self._generate_alerts(data),
                "timestamp": datetime.now().isoformat(),
            }

            return dashboard

        except Exception as e:
            self.logger.error(f"Error generating dashboard data: {e}")
            return {"error": str(e)}

    def _generate_summary(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Generate summary statistics."""
        if not data:
            return {}

        summary = {
            "total_records": len(data),
            "date_range": self._get_date_range(data),
            "key_metrics": self._get_key_metrics(data),
        }

        return summary

    def _get_date_range(self, data: list[dict[str, Any]]) -> dict[str, str]:
        """Get date range from data."""
        dates = []
        for row in data:
            if "timestamp" in row:
                dates.append(row["timestamp"])
            elif "date" in row:
                dates.append(row["date"])

        if dates:
            return {"start": min(dates), "end": max(dates)}
        else:
            return {"start": "unknown", "end": "unknown"}

    def _get_key_metrics(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Get key metrics from data."""
        if not data:
            return {}

        numeric_fields = self._get_numeric_fields(data[0])
        key_metrics = {}

        for field in numeric_fields:
            values = [row.get(field, 0) for row in data if field in row]
            if values:
                key_metrics[field] = {
                    "total": sum(values),
                    "average": statistics.mean(values),
                    "count": len(values),
                }

        return key_metrics

    def _get_numeric_fields(self, sample_row: dict[str, Any]) -> list[str]:
        """Get numeric fields from sample row."""
        numeric_fields = []
        for key, value in sample_row.items():
            if isinstance(value, (int, float)):
                numeric_fields.append(key)
        return numeric_fields

    def _generate_chart_data(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Generate chart data for visualization."""
        charts = []

        if not data:
            return charts

        numeric_fields = self._get_numeric_fields(data[0])

        for field in numeric_fields:
            values = [row.get(field, 0) for row in data if field in row]
            if values:
                chart_data = {
                    "type": "line",
                    "field": field,
                    "data": values,
                    "labels": [f"Point {i + 1}" for i in range(len(values))],
                }
                charts.append(chart_data)

        return charts

    def _generate_alerts(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Generate alerts based on data analysis."""
        alerts = []

        if not data:
            return alerts

        numeric_fields = self._get_numeric_fields(data[0])

        for field in numeric_fields:
            values = [row.get(field, 0) for row in data if field in row]
            if values:
                mean_val = statistics.mean(values)
                std_val = statistics.stdev(values) if len(values) > 1 else 0

                # Check for outliers
                for i, value in enumerate(values):
                    if abs(value - mean_val) > 2 * std_val:
                        alerts.append(
                            {
                                "type": "outlier",
                                "field": field,
                                "value": value,
                                "expected_range": (
                                    f"{mean_val - 2 * std_val:.2f} - {mean_val + 2 * std_val:.2f}"
                                ),
                                "severity": "medium",
                            }
                        )

        return alerts

    def export_insights(self, format: str = "json") -> str:
        """Export insights in specified format."""
        try:
            if format == "json":
                import json

                return json.dumps(self.insights, indent=2)
            elif format == "csv":
                return self._export_csv()
            else:
                return str(self.insights)

        except Exception as e:
            self.logger.error(f"Error exporting insights: {e}")
            return f"Error: {e}"

    def _export_csv(self) -> str:
        """Export insights as CSV."""
        if not self.insights:
            return "No insights to export"

        csv_lines = []
        for insight in self.insights:
            csv_lines.append(f"{insight.get('timestamp', '')},{insight.get('data_points', 0)}")

        return "\n".join(csv_lines)

    def get_performance_metrics(self) -> dict[str, Any]:
        """Get performance metrics for the engine."""
        return {
            "total_insights_generated": len(self.insights),
            "last_analysis_time": (self.insights[-1].get("timestamp") if self.insights else None),
            "engine_status": "active",
            "config": self.config,
        }

    def optimize_performance(self) -> dict[str, Any]:
        """Optimize engine performance."""
        try:
            # Simple optimization - clear old insights
            if len(self.insights) > 100:
                self.insights = self.insights[-50:]

            return {
                "optimization_applied": "cleared_old_insights",
                "insights_count": len(self.insights),
                "status": "optimized",
            }

        except Exception as e:
            self.logger.error(f"Error optimizing performance: {e}")
            return {"error": str(e)}
