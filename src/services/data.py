"""Data access layer for dashboard service."""
from __future__ import annotations

from typing import Any, Dict, Optional
import time

from ..performance_monitor import PerformanceMonitor


def get_metrics(
    performance_monitor: PerformanceMonitor,
    metric_name: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    aggregation: str = "raw",
) -> Dict[str, Any] | None:
    """Fetch metrics data from the performance monitor."""
    start_time_float = float(start_time) if start_time else None
    end_time_float = float(end_time) if end_time else None

    if metric_name:
        if aggregation == "raw":
            series = performance_monitor.get_metric_series(
                metric_name, start_time_float, end_time_float
            )
            if not series:
                return None
            return {
                "metric_name": series.metric_name,
                "metric_type": series.metric_type.value,
                "data_points": [
                    {
                        "value": point.value,
                        "timestamp": point.timestamp,
                        "tags": point.tags,
                        "unit": point.unit,
                    }
                    for point in series.data_points
                ],
                "unit": series.unit,
                "description": series.description,
            }
        value = performance_monitor.aggregate_metrics(
            metric_name, aggregation, start_time_float, end_time_float
        )
        return {
            "metric_name": metric_name,
            "aggregation": aggregation,
            "value": value,
            "start_time": start_time_float,
            "end_time": end_time_float,
        }

    metric_names = performance_monitor.metrics_storage.get_all_metric_names()
    return {"metrics": metric_names}


def get_health(performance_monitor: PerformanceMonitor) -> Dict[str, Any]:
    """Fetch system health information."""
    return performance_monitor.get_system_status()


def get_status(
    performance_monitor: PerformanceMonitor, start_time: float
) -> Dict[str, Any]:
    """Fetch dashboard status details."""
    return {
        "dashboard_running": True,
        "performance_monitor_running": performance_monitor.running,
        "collectors_count": len(performance_monitor.collectors),
        "active_alerts": len(performance_monitor.active_alerts),
        "uptime": time.time() - start_time,
    }


def get_alerts(performance_monitor: PerformanceMonitor) -> Dict[str, Any]:
    """Fetch active alerts."""
    alerts_data = []
    for alert_id, alert in performance_monitor.active_alerts.items():
        alerts_data.append(
            {
                "alert_id": alert.alert_id,
                "rule_name": alert.rule_name,
                "metric_name": alert.metric_name,
                "current_value": alert.current_value,
                "threshold": alert.threshold,
                "severity": alert.severity.value,
                "message": alert.message,
                "timestamp": alert.timestamp,
                "tags": alert.tags,
                "resolved": alert.resolved,
            }
        )
    return {"alerts": alerts_data}


def get_collectors(performance_monitor: PerformanceMonitor) -> Dict[str, Any]:
    """Fetch metrics collectors status."""
    collectors_data = []
    for collector in performance_monitor.collectors:
        collectors_data.append(
            {
                "name": collector.__class__.__name__,
                "enabled": collector.enabled,
                "collection_interval": collector.collection_interval,
                "running": collector.running,
            }
        )
    return {"collectors": collectors_data}
