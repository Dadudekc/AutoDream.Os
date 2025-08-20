#!/usr/bin/env python3
"""
Autonomous Performance Monitor
=============================
Autonomous performance monitoring and analysis for agent swarm systems.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from collections import deque

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Performance metric types"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    RESOURCE_USAGE = "resource_usage"
    LATENCY = "latency"


@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    metric_type: MetricType
    value: float
    timestamp: float
    component: str
    agent_id: Optional[str] = None


@dataclass
class PerformanceAlert:
    """Performance alert notification"""
    alert_id: str
    metric_type: MetricType
    severity: str
    message: str
    timestamp: float
    threshold: float
    current_value: float


class AutonomousPerformanceMonitor:
    """Autonomous performance monitoring system"""
    
    def __init__(self, system_id: str = "default-monitor"):
        self.logger = logging.getLogger(f"{__name__}.AutonomousPerformanceMonitor")
        self.system_id = system_id
        self._metrics: Dict[MetricType, deque] = {metric: deque(maxlen=1000) for metric in MetricType}
        self._component_metrics: Dict[str, Dict[MetricType, deque]] = {}
        self._agent_metrics: Dict[str, Dict[MetricType, deque]] = {}
        self._alerts: Dict[str, PerformanceAlert] = {}
        self._thresholds: Dict[MetricType, Dict[str, float]] = {
            MetricType.RESPONSE_TIME: {"warning": 1000, "critical": 5000},
            MetricType.ERROR_RATE: {"warning": 0.05, "critical": 0.15},
            MetricType.LATENCY: {"warning": 100, "critical": 500},
            MetricType.THROUGHPUT: {"warning": 0.8, "critical": 0.5},
            MetricType.RESOURCE_USAGE: {"warning": 0.8, "critical": 0.95}
        }
        self._monitoring_active = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()
        self._total_metrics = 0
        self._total_alerts = 0
        self.logger.info(f"Autonomous Performance Monitor '{system_id}' initialized")
    
    def record_metric(self, metric_type: MetricType, value: float, component: str, agent_id: Optional[str] = None) -> str:
        """Record a performance metric"""
        timestamp = time.time()
        metric = PerformanceMetric(metric_type, value, timestamp, component, agent_id)
        self._metrics[metric_type].append(metric)
        
        if component not in self._component_metrics:
            self._component_metrics[component] = {metric: deque(maxlen=1000) for metric in MetricType}
        self._component_metrics[component][metric_type].append(metric)
        
        if agent_id:
            if agent_id not in self._agent_metrics:
                self._agent_metrics[agent_id] = {metric: deque(maxlen=1000) for metric in MetricType}
            self._agent_metrics[agent_id][metric_type].append(metric)
        
        self._total_metrics += 1
        self._check_alert_thresholds(metric)
        return f"metric_{metric_type.value}_{int(timestamp)}"
    
    def _check_alert_thresholds(self, metric: PerformanceMetric):
        """Check if metric exceeds alert thresholds"""
        thresholds = self._thresholds.get(metric.metric_type, {})
        for severity, threshold in thresholds.items():
            if metric.value > threshold:
                self._create_alert(metric, threshold, severity)
    
    def _create_alert(self, metric: PerformanceMetric, threshold: float, severity: str):
        """Create a performance alert"""
        alert_id = f"alert_{metric.metric_type.value}_{int(time.time())}"
        alert = PerformanceAlert(
            alert_id=alert_id, metric_type=metric.metric_type, severity=severity,
            message=f"{metric.component} {metric.metric_type.value} exceeded {severity} threshold",
            timestamp=time.time(), threshold=threshold, current_value=metric.value
        )
        self._alerts[alert_id] = alert
        self._total_alerts += 1
        self.logger.warning(f"Performance alert: {alert.message} (value: {metric.value}, threshold: {threshold})")
    
    def get_performance_summary(self, component: Optional[str] = None, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get performance summary for component or agent"""
        if component:
            metrics = self._component_metrics.get(component, {})
        elif agent_id:
            metrics = self._agent_metrics.get(agent_id, {})
        else:
            metrics = self._metrics
        
        summary = {}
        for metric_type, metric_list in metrics.items():
            if not metric_list:
                continue
            values = [m.value for m in metric_list]
            summary[metric_type.value] = {
                "count": len(values), "min": min(values), "max": max(values),
                "avg": sum(values) / len(values), "latest": values[-1] if values else 0
            }
        return summary
    
    def get_active_alerts(self, severity: Optional[str] = None) -> List[PerformanceAlert]:
        """Get active performance alerts"""
        if severity:
            return [alert for alert in self._alerts.values() if alert.severity == severity]
        return list(self._alerts.values())
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring system statistics"""
        return {
            "system_id": self.system_id, "total_metrics": self._total_metrics,
            "total_alerts": self._total_alerts, "active_alerts": len(self._alerts),
            "components_monitored": len(self._component_metrics),
            "agents_monitored": len(self._agent_metrics),
            "monitoring_active": self._monitoring_active, "timestamp": time.time()
        }
    
    def start_monitoring(self):
        """Start autonomous performance monitoring"""
        if self._monitoring_active:
            return
        self._monitoring_active = True
        self._stop_monitoring.clear()
        self._monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitor_thread.start()
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while not self._stop_monitoring.is_set():
            try:
                self._perform_maintenance_tasks()
                time.sleep(30)
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(60)
    
    def _perform_maintenance_tasks(self):
        """Perform maintenance and cleanup tasks"""
        cutoff_time = time.time() - 86400
        old_alerts = [aid for aid, alert in self._alerts.items() if alert.timestamp < cutoff_time]
        for alert_id in old_alerts:
            del self._alerts[alert_id]
    
    def stop_monitoring(self):
        """Stop autonomous performance monitoring"""
        self._monitoring_active = False
        self._stop_monitoring.set()
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=2)


def main():
    """CLI interface for testing AutonomousPerformanceMonitor"""
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Performance Monitor CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    args = parser.parse_args()
    
    if args.test:
        print("🧪 AutonomousPerformanceMonitor Smoke Test")
        monitor = AutonomousPerformanceMonitor("test-monitor")
        monitor.record_metric(MetricType.RESPONSE_TIME, 1500, "test-component", "test-agent")
        monitor.record_metric(MetricType.ERROR_RATE, 0.08, "test-component", "test-agent")
        summary = monitor.get_performance_summary("test-component")
        print(f"✅ Metrics recorded: {len(summary)}")
        stats = monitor.get_monitoring_stats()
        print(f"✅ Total metrics: {stats['total_metrics']}")
        print("🎉 Smoke test PASSED!")
    else:
        print("AutonomousPerformanceMonitor ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
