"""
Metrics Manager - Phase-2 V2 Compliance Refactoring
===================================================

Handles metrics-specific monitoring operations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from ..contracts import ManagerContext, ManagerResult
from .base_monitoring_manager import BaseMonitoringManager


class MetricsManager(BaseMonitoringManager):
    """Manages metrics operations."""

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute metrics operation."""
        try:
            if operation == "record_metric":
                return self.record_metric(context, payload)
            elif operation == "get_metrics":
                return self._get_metrics(context, payload)
            elif operation == "get_metric_aggregation":
                return self._get_metric_aggregation(context, payload)
            elif operation == "get_metric_trends":
                return self._get_metric_trends(context, payload)
            elif operation == "export_metrics":
                return self._export_metrics(context, payload)
            else:
                return super().execute(context, operation, payload)
        except Exception as e:
            context.logger(f"Error executing metrics operation {operation}: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _get_metric_aggregation(
        self, context: ManagerContext, payload: dict[str, Any]
    ) -> ManagerResult:
        """Get metric aggregation data."""
        try:
            metric_name = payload.get("metric_name")
            aggregation_type = payload.get("aggregation_type", "summary")
            time_window = payload.get("time_window", 3600)  # 1 hour default

            if not metric_name or metric_name not in self.metric_history:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Metric {metric_name} not found or has no history",
                )

            history = self.metric_history[metric_name]

            # Filter by time window
            cutoff_time = datetime.now() - timedelta(seconds=time_window)
            filtered_history = [
                entry
                for entry in history
                if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
            ]

            if not filtered_history:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="No data in specified time window",
                )

            # Calculate aggregation
            values = [
                entry["value"]
                for entry in filtered_history
                if isinstance(entry["value"], (int, float))
            ]

            if not values:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="No numeric values found for aggregation",
                )

            if aggregation_type == "summary":
                result = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "sum": sum(values),
                    "average": sum(values) / len(values),
                }

                # Calculate variance and standard deviation
                mean = result["average"]
                variance = sum((x - mean) ** 2 for x in values) / len(values)
                result["variance"] = variance
                result["std_deviation"] = variance**0.5

            elif aggregation_type == "percentiles":
                sorted_values = sorted(values)
                n = len(sorted_values)
                result = {
                    "p50": sorted_values[int(n * 0.5)],
                    "p90": sorted_values[int(n * 0.9)],
                    "p95": sorted_values[int(n * 0.95)],
                    "p99": sorted_values[int(n * 0.99)],
                }
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown aggregation type: {aggregation_type}",
                )

            return ManagerResult(
                success=True,
                data={
                    "metric_name": metric_name,
                    "aggregation_type": aggregation_type,
                    "time_window": time_window,
                    "data_points": len(filtered_history),
                    "result": result,
                },
                metrics={"aggregations_calculated": 1},
            )

        except Exception as e:
            context.logger(f"Error getting metric aggregation: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _get_metric_trends(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get metric trend analysis."""
        try:
            metric_name = payload.get("metric_name")
            trend_window = payload.get("trend_window", 7200)  # 2 hours default

            if not metric_name or metric_name not in self.metric_history:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Metric {metric_name} not found or has no history",
                )

            history = self.metric_history[metric_name]

            # Filter by time window
            cutoff_time = datetime.now() - timedelta(seconds=trend_window)
            filtered_history = [
                entry
                for entry in history
                if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
            ]

            if len(filtered_history) < 2:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Insufficient data points for trend analysis",
                )

            # Sort by timestamp
            filtered_history.sort(key=lambda x: x["timestamp"])

            # Extract values and timestamps
            values = [
                entry["value"]
                for entry in filtered_history
                if isinstance(entry["value"], (int, float))
            ]
            timestamps = [
                entry["timestamp"]
                for entry in filtered_history
                if isinstance(entry["value"], (int, float))
            ]

            if len(values) < 2:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Insufficient numeric values for trend analysis",
                )

            # Calculate trend
            first_value = values[0]
            last_value = values[-1]
            trend_direction = (
                "increasing"
                if last_value > first_value
                else "decreasing" if last_value < first_value else "stable"
            )
            trend_magnitude = abs(last_value - first_value) / first_value if first_value != 0 else 0

            # Calculate moving average (simple 3-point)
            moving_averages = []
            for i in range(2, len(values)):
                moving_averages.append(sum(values[i - 2 : i + 1]) / 3)

            return ManagerResult(
                success=True,
                data={
                    "metric_name": metric_name,
                    "trend_window": trend_window,
                    "data_points": len(values),
                    "trend_direction": trend_direction,
                    "trend_magnitude": trend_magnitude,
                    "first_value": first_value,
                    "last_value": last_value,
                    "moving_averages": moving_averages[-10:],  # Last 10 moving averages
                },
                metrics={"trends_calculated": 1},
            )

        except Exception as e:
            context.logger(f"Error getting metric trends: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _export_metrics(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Export metrics data."""
        try:
            export_format = payload.get("format", "json")
            metric_names = payload.get("metric_names", [])
            include_history = payload.get("include_history", False)

            # Filter metrics
            if metric_names:
                export_data = {
                    name: self.metrics.get(name) for name in metric_names if name in self.metrics
                }
            else:
                export_data = dict(self.metrics)

            # Add history if requested
            if include_history:
                for name in export_data:
                    if name in self.metric_history:
                        export_data[name]["history"] = self.metric_history[name]

            if export_format == "json":
                import json

                export_string = json.dumps(export_data, indent=2)
            elif export_format == "csv":
                # Simple CSV export for numeric metrics
                csv_lines = ["metric_name,timestamp,value,type"]
                for name, metric in export_data.items():
                    if isinstance(metric.get("value"), (int, float)):
                        csv_lines.append(
                            f"{name},{metric['timestamp']},{metric['value']},{metric.get('type', 'unknown')}"
                        )
                export_string = "\n".join(csv_lines)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unsupported export format: {export_format}",
                )

            return ManagerResult(
                success=True,
                data={
                    "export_format": export_format,
                    "metrics_exported": len(export_data),
                    "export_data": export_string,
                },
                metrics={"metrics_exported": len(export_data)},
            )

        except Exception as e:
            context.logger(f"Error exporting metrics: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def get_status(self) -> dict[str, Any]:
        """Get metrics manager status."""
        base_status = super().get_status()
        base_status.update(
            {
                "metric_types": list(set(m.get("type", "unknown") for m in self.metrics.values())),
                "total_history_entries": sum(
                    len(history) for history in self.metric_history.values()
                ),
                "avg_history_per_metric": sum(
                    len(history) for history in self.metric_history.values()
                )
                / max(len(self.metric_history), 1),
            }
        )
        return base_status
