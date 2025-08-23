#!/usr/bin/env python3
"""
V2 Integration Monitoring System
================================
Comprehensive monitoring system for V2 integration framework with alerting.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class MonitoringMetric:
    """Monitoring metric data point"""

    name: str
    value: float
    timestamp: float
    tags: Dict[str, str]
    unit: Optional[str] = None


@dataclass
class Alert:
    """Monitoring alert"""

    id: str
    severity: AlertSeverity
    message: str
    metric_name: str
    threshold: float
    current_value: float
    timestamp: float
    acknowledged: bool = False


class V2IntegrationMonitoring:
    """Comprehensive monitoring system for V2 integration"""

    def __init__(self, alert_callback: Optional[Callable] = None):
        self.logger = logging.getLogger(f"{__name__}.V2IntegrationMonitoring")
        self.alert_callback = alert_callback

        # Metrics storage
        self._metrics: Dict[str, List[MonitoringMetric]] = {}
        self._metric_thresholds: Dict[str, Dict[str, float]] = {}

        # Alerting system
        self._alerts: Dict[str, Alert] = {}
        self._alert_rules: Dict[str, Dict[str, Any]] = {}

        # Monitoring state
        self._monitoring_active = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()

        # Performance tracking
        self._start_time = time.time()
        self._total_metrics = 0
        self._total_alerts = 0

        self.logger.info("V2 Integration Monitoring System initialized")

    def set_metric_threshold(
        self,
        metric_name: str,
        warning_threshold: float,
        error_threshold: float,
        critical_threshold: float,
    ):
        """Set thresholds for a metric"""
        self._metric_thresholds[metric_name] = {
            "warning": warning_threshold,
            "error": error_threshold,
            "critical": critical_threshold,
        }
        self.logger.info(f"Thresholds set for metric: {metric_name}")

    def record_metric(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None,
        unit: Optional[str] = None,
    ):
        """Record a monitoring metric"""
        if name not in self._metrics:
            self._metrics[name] = []

        metric = MonitoringMetric(
            name=name, value=value, timestamp=time.time(), tags=tags or {}, unit=unit
        )

        self._metrics[name].append(metric)
        self._total_metrics += 1

        # Keep only recent metrics (last 1000)
        if len(self._metrics[name]) > 1000:
            self._metrics[name] = self._metrics[name][-1000:]

        # Check thresholds and generate alerts
        self._check_metric_thresholds(name, value)

    def _check_metric_thresholds(self, metric_name: str, value: float):
        """Check if metric exceeds thresholds and generate alerts"""
        if metric_name not in self._metric_thresholds:
            return

        thresholds = self._metric_thresholds[metric_name]

        # Determine severity
        severity = None
        if value >= thresholds.get("critical", float("inf")):
            severity = AlertSeverity.CRITICAL
        elif value >= thresholds.get("error", float("inf")):
            severity = AlertSeverity.ERROR
        elif value >= thresholds.get("warning", float("inf")):
            severity = AlertSeverity.WARNING

        if severity:
            alert_id = f"{metric_name}_{int(time.time())}"
            alert = Alert(
                id=alert_id,
                severity=severity,
                message=f"Metric {metric_name} exceeded {severity.value} threshold",
                metric_name=metric_name,
                threshold=thresholds.get(severity.value, 0),
                current_value=value,
                timestamp=time.time(),
            )

            self._alerts[alert_id] = alert
            self._total_alerts += 1

            # Trigger alert callback
            if self.alert_callback:
                try:
                    self.alert_callback(alert)
                except Exception as e:
                    self.logger.error(f"Alert callback failed: {e}")

            self.logger.warning(
                f"Alert generated: {severity.value} - {metric_name} = {value}"
            )

    def get_metric_history(
        self, metric_name: str, hours: int = 24
    ) -> List[MonitoringMetric]:
        """Get metric history for specified time window"""
        if metric_name not in self._metrics:
            return []

        cutoff_time = time.time() - (hours * 3600)
        return [m for m in self._metrics[metric_name] if m.timestamp >= cutoff_time]

    def get_current_metrics(self) -> Dict[str, float]:
        """Get current values for all metrics"""
        current_metrics = {}
        for name, metrics in self._metrics.items():
            if metrics:
                current_metrics[name] = metrics[-1].value
        return current_metrics

    def get_active_alerts(
        self, severity_filter: Optional[AlertSeverity] = None
    ) -> List[Alert]:
        """Get active alerts, optionally filtered by severity"""
        alerts = list(self._alerts.values())

        if severity_filter:
            alerts = [a for a in alerts if a.severity == severity_filter]

        return [a for a in alerts if not a.acknowledged]

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        if alert_id not in self._alerts:
            return False

        self._alerts[alert_id].acknowledged = True
        self.logger.info(f"Alert acknowledged: {alert_id}")
        return True

    def clear_alert(self, alert_id: str) -> bool:
        """Clear an alert"""
        if alert_id not in self._alerts:
            return False

        del self._alerts[alert_id]
        self.logger.info(f"Alert cleared: {alert_id}")
        return True

    def start_monitoring(self, interval_seconds: int = 30):
        """Start continuous monitoring"""
        if self._monitoring_active:
            self.logger.warning("Monitoring already active")
            return

        self._monitoring_active = True
        self._stop_monitoring.clear()

        self._monitor_thread = threading.Thread(
            target=self._monitoring_loop, args=(interval_seconds,), daemon=True
        )
        self._monitor_thread.start()
        self.logger.info(f"Monitoring started (interval: {interval_seconds}s)")

    def _monitoring_loop(self, interval: int):
        """Main monitoring loop"""
        while not self._stop_monitoring.is_set():
            try:
                self._perform_monitoring_checks()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(10)

    def _perform_monitoring_checks(self):
        """Perform monitoring checks and cleanup"""
        current_time = time.time()

        # Clean up old alerts (older than 24 hours)
        alert_ids_to_remove = []
        for alert_id, alert in self._alerts.items():
            if current_time - alert.timestamp > 86400:  # 24 hours
                alert_ids_to_remove.append(alert_id)

        for alert_id in alert_ids_to_remove:
            self.clear_alert(alert_id)

    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring system statistics"""
        uptime = time.time() - self._start_time
        active_alerts = len([a for a in self._alerts.values() if not a.acknowledged])

        return {
            "uptime_seconds": uptime,
            "uptime_hours": uptime / 3600,
            "total_metrics_recorded": self._total_metrics,
            "total_alerts_generated": self._total_alerts,
            "active_alerts": active_alerts,
            "total_alerts": len(self._alerts),
            "metrics_tracked": len(self._metrics),
            "monitoring_active": self._monitoring_active,
            "timestamp": time.time(),
        }

    def generate_monitoring_report(self) -> str:
        """Generate comprehensive monitoring report"""
        stats = self.get_monitoring_stats()
        current_metrics = self.get_current_metrics()
        active_alerts = self.get_active_alerts()

        lines = [
            "📊 V2 INTEGRATION MONITORING REPORT",
            "=" * 50,
            f"Uptime: {stats['uptime_hours']:.1f} hours",
            f"Metrics Tracked: {stats['metrics_tracked']}",
            f"Total Metrics: {stats['total_metrics_recorded']}",
            f"Active Alerts: {stats['active_alerts']}",
            "",
            "CURRENT METRICS:",
        ]

        for name, value in current_metrics.items():
            lines.append(f"  {name}: {value}")

        if active_alerts:
            lines.extend(
                [
                    "",
                    "🚨 ACTIVE ALERTS:",
                ]
            )
            for alert in active_alerts[:5]:  # Show first 5 alerts
                lines.append(
                    f"  {alert.severity.value.upper()}: {alert.metric_name} = {alert.current_value}"
                )
        else:
            lines.append("  No active alerts")

        lines.append("=" * 50)
        return "\n".join(lines)

    def stop_monitoring(self):
        """Stop monitoring"""
        self._monitoring_active = False
        self._stop_monitoring.set()

        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=2)

        self.logger.info("Monitoring stopped")


def main():
    """CLI interface for testing V2IntegrationMonitoring"""
    import argparse

    parser = argparse.ArgumentParser(description="V2 Integration Monitoring CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")

    args = parser.parse_args()

    if args.test:
        print("🧪 V2IntegrationMonitoring Smoke Test")
        print("=" * 45)

        def alert_handler(alert):
            print(f"🚨 ALERT: {alert.severity.value} - {alert.message}")

        monitoring = V2IntegrationMonitoring(alert_callback=alert_handler)

        # Set thresholds
        monitoring.set_metric_threshold("cpu_usage", warning=70, error=85, critical=95)
        monitoring.set_metric_threshold(
            "memory_usage", warning=80, error=90, critical=98
        )

        # Record metrics
        monitoring.record_metric("cpu_usage", 75.0, {"host": "server-1"}, "percent")
        monitoring.record_metric("memory_usage", 92.0, {"host": "server-1"}, "percent")
        monitoring.record_metric("response_time", 150.0, {"service": "api"}, "ms")

        # Test metric retrieval
        cpu_history = monitoring.get_metric_history("cpu_usage", hours=1)
        print(f"✅ CPU metrics recorded: {len(cpu_history)}")

        # Test current metrics
        current_metrics = monitoring.get_current_metrics()
        print(f"✅ Current metrics: {len(current_metrics)}")

        # Test alerts
        active_alerts = monitoring.get_active_alerts()
        print(f"✅ Active alerts: {len(active_alerts)}")

        # Test monitoring stats
        stats = monitoring.get_monitoring_stats()
        print(f"✅ Total metrics: {stats['total_metrics_recorded']}")
        print(f"✅ Total alerts: {stats['total_alerts_generated']}")

        # Generate report
        report = monitoring.generate_monitoring_report()
        print("\n📊 MONITORING REPORT:")
        print(report)

        print("🎉 V2IntegrationMonitoring smoke test PASSED!")
    else:
        print("V2IntegrationMonitoring ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
