#!/usr/bin/env python3
"""
V3-015: Monitoring Metrics
==========================

Core monitoring metrics and data structures for production monitoring.
V2 compliant with focus on essential monitoring functionality.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class MonitorStatus(Enum):
    """Monitor status types."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AlertLevel(Enum):
    """Alert levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MetricType(Enum):
    """Metric types."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """Metric structure."""
    metric_id: str
    name: str
    metric_type: MetricType
    value: float
    labels: Dict[str, str]
    timestamp: datetime
    unit: str = ""


@dataclass
class Alert:
    """Alert structure."""
    alert_id: str
    name: str
    level: AlertLevel
    message: str
    metric_name: str
    threshold: float
    current_value: float
    triggered_at: datetime
    resolved_at: Optional[datetime] = None
    acknowledged: bool = False


@dataclass
class MonitorTarget:
    """Monitor target structure."""
    target_id: str
    name: str
    endpoint: str
    check_interval: int
    timeout: int
    status: MonitorStatus
    last_check: Optional[datetime] = None
    error_count: int = 0


class MetricsCollector:
    """Metrics collection and management."""
    
    def __init__(self):
        self.metrics = []
        self.metric_history = {}
        self.max_history_size = 1000
    
    def add_metric(self, metric: Metric):
        """Add metric to collection."""
        self.metrics.append(metric)
        
        # Store in history
        if metric.name not in self.metric_history:
            self.metric_history[metric.name] = []
        
        self.metric_history[metric.name].append(metric)
        
        # Limit history size
        if len(self.metric_history[metric.name]) > self.max_history_size:
            self.metric_history[metric.name] = self.metric_history[metric.name][-self.max_history_size:]
    
    def get_metrics_by_name(self, name: str) -> List[Metric]:
        """Get metrics by name."""
        return [m for m in self.metrics if m.name == name]
    
    def get_metrics_by_type(self, metric_type: MetricType) -> List[Metric]:
        """Get metrics by type."""
        return [m for m in self.metrics if m.metric_type == metric_type]
    
    def get_latest_metric(self, name: str) -> Optional[Metric]:
        """Get latest metric by name."""
        metrics = self.get_metrics_by_name(name)
        return max(metrics, key=lambda m: m.timestamp) if metrics else None
    
    def get_metric_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        if not self.metrics:
            return {"error": "No metrics available"}
        
        metric_names = list(set(m.name for m in self.metrics))
        metric_types = list(set(m.metric_type.value for m in self.metrics))
        
        return {
            "total_metrics": len(self.metrics),
            "unique_metric_names": len(metric_names),
            "metric_types": metric_types,
            "metric_names": metric_names,
            "latest_metric": max(self.metrics, key=lambda m: m.timestamp).timestamp.isoformat()
        }


class AlertManager:
    """Alert management and processing."""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules = {}
        self.alert_history = []
    
    def add_alert_rule(self, rule_id: str, metric_name: str, threshold: float, 
                      level: AlertLevel, message: str):
        """Add alert rule."""
        self.alert_rules[rule_id] = {
            "metric_name": metric_name,
            "threshold": threshold,
            "level": level,
            "message": message
        }
    
    def check_metric_for_alerts(self, metric: Metric):
        """Check metric against alert rules."""
        for rule_id, rule in self.alert_rules.items():
            if rule["metric_name"] == metric.name:
                if metric.value > rule["threshold"]:
                    self._create_alert(rule_id, rule, metric)
    
    def _create_alert(self, rule_id: str, rule: Dict[str, Any], metric: Metric):
        """Create alert from rule and metric."""
        alert = Alert(
            alert_id=f"{rule_id}_{int(metric.timestamp.timestamp())}",
            name=f"Alert for {metric.name}",
            level=rule["level"],
            message=rule["message"],
            metric_name=metric.name,
            threshold=rule["threshold"],
            current_value=metric.value,
            triggered_at=metric.timestamp
        )
        
        self.alerts.append(alert)
        self.alert_history.append(alert)
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge alert."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve alert."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved_at = datetime.now()
                return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Get active alerts."""
        return [alert for alert in self.alerts if not alert.resolved_at]
    
    def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        """Get alerts by level."""
        return [alert for alert in self.alerts if alert.level == level]
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary."""
        active_alerts = self.get_active_alerts()
        level_counts = {}
        
        for alert in self.alerts:
            level = alert.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            "total_alerts": len(self.alerts),
            "active_alerts": len(active_alerts),
            "acknowledged_alerts": sum(1 for a in self.alerts if a.acknowledged),
            "resolved_alerts": sum(1 for a in self.alerts if a.resolved_at),
            "level_counts": level_counts,
            "alert_rules": len(self.alert_rules)
        }


def main():
    """Main execution function."""
    print("📊 V3-015 Monitoring Metrics - Testing...")
    
    # Initialize components
    metrics_collector = MetricsCollector()
    alert_manager = AlertManager()
    
    # Add sample metrics
    sample_metrics = [
        Metric("cpu_1", "cpu_usage", MetricType.GAUGE, 75.5, {"host": "server1"}, datetime.now()),
        Metric("memory_1", "memory_usage", MetricType.GAUGE, 60.2, {"host": "server1"}, datetime.now()),
        Metric("requests_1", "request_count", MetricType.COUNTER, 1000, {"endpoint": "/api"}, datetime.now())
    ]
    
    for metric in sample_metrics:
        metrics_collector.add_metric(metric)
    
    # Add alert rules
    alert_manager.add_alert_rule("cpu_high", "cpu_usage", 80.0, AlertLevel.WARNING, "CPU usage is high")
    alert_manager.add_alert_rule("memory_high", "memory_usage", 90.0, AlertLevel.CRITICAL, "Memory usage is critical")
    
    # Check metrics for alerts
    for metric in sample_metrics:
        alert_manager.check_metric_for_alerts(metric)
    
    # Get summaries
    metrics_summary = metrics_collector.get_metric_summary()
    alert_summary = alert_manager.get_alert_summary()
    
    print(f"\n📈 Metrics Summary:")
    print(f"   Total Metrics: {metrics_summary['total_metrics']}")
    print(f"   Unique Names: {metrics_summary['unique_metric_names']}")
    print(f"   Metric Types: {metrics_summary['metric_types']}")
    
    print(f"\n🚨 Alert Summary:")
    print(f"   Total Alerts: {alert_summary['total_alerts']}")
    print(f"   Active Alerts: {alert_summary['active_alerts']}")
    print(f"   Alert Rules: {alert_summary['alert_rules']}")
    
    print("\n✅ V3-015 Monitoring Metrics completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())