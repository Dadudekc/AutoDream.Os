#!/usr/bin/env python3
"""
V3-003: Database Monitoring
===========================

Database monitoring and performance tracking with V2 compliance.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class MonitorStatus(Enum):
    """Monitor status types."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class AlertLevel(Enum):
    """Alert levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class DatabaseMetric:
    """Database metric structure."""
    metric_id: str
    database_id: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    labels: Dict[str, str]


@dataclass
class DatabaseAlert:
    """Database alert structure."""
    alert_id: str
    database_id: str
    level: AlertLevel
    message: str
    metric_name: str
    threshold: float
    current_value: float
    triggered_at: datetime
    resolved_at: Optional[datetime] = None


class DatabaseMonitor:
    """Database monitoring and alerting."""
    
    def __init__(self):
        self.metrics = []
        self.alerts = []
        self.alert_rules = {}
        self.monitoring_active = False
    
    def start_monitoring(self):
        """Start database monitoring."""
        self.monitoring_active = True
        print("📊 Database monitoring started")
    
    def stop_monitoring(self):
        """Stop database monitoring."""
        self.monitoring_active = False
        print("⏹️ Database monitoring stopped")
    
    def collect_metric(self, database_id: str, metric_name: str, value: float, 
                      unit: str = "", labels: Dict[str, str] = None):
        """Collect database metric."""
        metric = DatabaseMetric(
            metric_id=f"{database_id}_{metric_name}_{int(datetime.now().timestamp())}",
            database_id=database_id,
            metric_name=metric_name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            labels=labels or {}
        )
        
        self.metrics.append(metric)
        self._check_metric_alerts(metric)
    
    def add_alert_rule(self, rule_id: str, database_id: str, metric_name: str, 
                      threshold: float, level: AlertLevel, message: str):
        """Add alert rule."""
        self.alert_rules[rule_id] = {
            "database_id": database_id,
            "metric_name": metric_name,
            "threshold": threshold,
            "level": level,
            "message": message
        }
    
    def _check_metric_alerts(self, metric: DatabaseMetric):
        """Check metric against alert rules."""
        for rule_id, rule in self.alert_rules.items():
            if (rule["database_id"] == metric.database_id and 
                rule["metric_name"] == metric.metric_name):
                
                if metric.value > rule["threshold"]:
                    self._create_alert(rule_id, rule, metric)
    
    def _create_alert(self, rule_id: str, rule: Dict[str, Any], metric: DatabaseMetric):
        """Create alert from rule and metric."""
        alert = DatabaseAlert(
            alert_id=f"{rule_id}_{int(metric.timestamp.timestamp())}",
            database_id=metric.database_id,
            level=rule["level"],
            message=rule["message"],
            metric_name=metric.metric_name,
            threshold=rule["threshold"],
            current_value=metric.value,
            triggered_at=metric.timestamp
        )
        
        self.alerts.append(alert)
        print(f"🚨 Alert triggered: {alert.message}")
    
    def get_database_health(self, database_id: str) -> Dict[str, Any]:
        """Get database health status."""
        recent_metrics = [
            m for m in self.metrics 
            if m.database_id == database_id and 
            m.timestamp > datetime.now() - timedelta(minutes=5)
        ]
        
        if not recent_metrics:
            return {"status": MonitorStatus.OFFLINE.value, "message": "No recent metrics"}
        
        status = MonitorStatus.HEALTHY
        issues = []
        
        for metric in recent_metrics:
            if metric.metric_name == "cpu_usage" and metric.value > 80:
                status = MonitorStatus.WARNING
                issues.append("High CPU usage")
            elif metric.metric_name == "memory_usage" and metric.value > 90:
                status = MonitorStatus.CRITICAL
                issues.append("High memory usage")
        
        return {
            "database_id": database_id,
            "status": status.value,
            "issues": issues,
            "recent_metrics": len(recent_metrics)
        }
    
    def get_active_alerts(self) -> List[DatabaseAlert]:
        """Get active alerts."""
        return [alert for alert in self.alerts if not alert.resolved_at]
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get monitoring summary."""
        active_alerts = self.get_active_alerts()
        
        return {
            "monitoring_active": self.monitoring_active,
            "active_alerts": len(active_alerts),
            "total_metrics": len(self.metrics),
            "alert_rules": len(self.alert_rules)
        }


def main():
    """Main execution function."""
    print("📊 V3-003 Database Monitoring - Testing...")
    
    # Initialize monitor
    monitor = DatabaseMonitor()
    monitor.start_monitoring()
    
    # Add alert rules
    monitor.add_alert_rule("cpu_high", "postgres_main", "cpu_usage", 80.0, AlertLevel.WARNING, "High CPU usage")
    monitor.add_alert_rule("memory_high", "postgres_main", "memory_usage", 90.0, AlertLevel.CRITICAL, "High memory usage")
    
    # Collect sample metrics
    monitor.collect_metric("postgres_main", "cpu_usage", 75.5, "%", {"host": "db1"})
    monitor.collect_metric("postgres_main", "memory_usage", 60.2, "%", {"host": "db1"})
    
    # Get summaries
    health = monitor.get_database_health("postgres_main")
    summary = monitor.get_monitoring_summary()
    
    print(f"\n🏥 Database Health:")
    print(f"   Status: {health['status']}")
    print(f"   Issues: {health['issues']}")
    
    print(f"\n📊 Monitoring Summary:")
    print(f"   Active Alerts: {summary['active_alerts']}")
    print(f"   Total Metrics: {summary['total_metrics']}")
    
    print("\n✅ V3-003 Database Monitoring completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

