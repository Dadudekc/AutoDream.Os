#!/usr/bin/env python3
"""
Performance Monitoring System
============================

Real-time performance monitoring and benchmarking for the Agent-1 mission.
Provides metrics collection, alerting, and optimization recommendations.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import psutil

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    name: str
    value: float
    timestamp: datetime
    unit: str
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class PerformanceSnapshot:
    """System performance snapshot"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    network_bytes_sent: int
    network_bytes_recv: int
    process_count: int


class PerformanceMonitor:
    """Real-time performance monitoring system"""

    def __init__(self, collection_interval: float = 5.0):
    """# Example usage:
result = __init__("example_value", "example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value")
print(f"Result: {result}")"""
        self.collection_interval = collection_interval
        self.metrics: List[PerformanceMetric] = []
        self.snapshots: List[PerformanceSnapshot] = []
        self.alerts: List[Dict[str, Any]] = []
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_usage_percent': 90.0
        }
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None

    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring_active:
            logger.warning("Performance monitoring already active")
            return

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")

    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        logger.info("Performance monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                snapshot = self.take_snapshot()
                self.snapshots.append(snapshot)
                self._check_thresholds(snapshot)
                self._cleanup_old_data()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

    def take_snapshot(self) -> PerformanceSnapshot:
        """Take a performance snapshot"""
        cpu_percent = psutil.cpu_percent(interval=1.0)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()

        return PerformanceSnapshot(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / 1024 / 1024,
            memory_available_mb=memory.available / 1024 / 1024,
            disk_usage_percent=disk.percent,
            network_bytes_sent=network.bytes_sent if network else 0,
            network_bytes_recv=network.bytes_recv if network else 0,
            process_count=len(psutil.pids())
        )

    def _check_thresholds(self, snapshot: PerformanceSnapshot):
        """Check if any metrics exceed thresholds"""
        alerts = []

        if snapshot.cpu_percent > self.thresholds['cpu_percent']:
            alerts.append({
                'type': 'cpu_high',
                'message': f"CPU usage {snapshot.cpu_percent:.1f}% exceeds threshold {self.thresholds['cpu_percent']}%",
                'value': snapshot.cpu_percent,
                'threshold': self.thresholds['cpu_percent']
            })

        if snapshot.memory_percent > self.thresholds['memory_percent']:
            alerts.append({
                'type': 'memory_high',
                'message': f"Memory usage {snapshot.memory_percent:.1f}% exceeds threshold {self.thresholds['memory_percent']}%",
                'value': snapshot.memory_percent,
                'threshold': self.thresholds['memory_percent']
            })

        if snapshot.disk_usage_percent > self.thresholds['disk_usage_percent']:
            alerts.append({
                'type': 'disk_high',
                'message': f"Disk usage {snapshot.disk_usage_percent:.1f}% exceeds threshold {self.thresholds['disk_usage_percent']}%",
                'value': snapshot.disk_usage_percent,
                'threshold': self.thresholds['disk_usage_percent']
            })

        for alert in alerts:
            alert['timestamp'] = snapshot.timestamp
            self.alerts.append(alert)
            logger.warning(f"Performance alert: {alert['message']}")

    def _cleanup_old_data(self, max_snapshots: int = 1000):
        """Clean up old performance data"""
        if len(self.snapshots) > max_snapshots:
            self.snapshots = self.snapshots[-max_snapshots:]
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

    def record_metric(self, name: str, value: float, unit: str, tags: Dict[str, str] = None):
        """Record a custom performance metric"""
        metric = PerformanceMetric(
            name=name,
            value=value,
            timestamp=datetime.now(),
            unit=unit,
            tags=tags or {}
        )
        self.metrics.append(metric)

    def get_recent_metrics(self, hours: int = 1) -> List[PerformanceMetric]:
        """Get metrics from the last N hours"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        return [m for m in self.metrics if m.timestamp.timestamp() > cutoff]

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""
        if not self.snapshots:
            return {"error": "No performance data available"}

        recent_snapshots = self.snapshots[-20:]  # Last 20 snapshots

        cpu_avg = sum(s.cpu_percent for s in recent_snapshots) / len(recent_snapshots)
        memory_avg = sum(s.memory_percent for s in recent_snapshots) / len(recent_snapshots)
        disk_avg = sum(s.disk_usage_percent for s in recent_snapshots) / len(recent_snapshots)

        memory_used_avg = sum(s.memory_used_mb for s in recent_snapshots) / len(recent_snapshots)
        memory_available_avg = sum(s.memory_available_mb for s in recent_snapshots) / len(recent_snapshots)

        return {
            'timestamp': datetime.now(),
            'monitoring_duration_hours': (self.snapshots[-1].timestamp - self.snapshots[0].timestamp).total_seconds() / 3600,
            'average_cpu_percent': cpu_avg,
            'average_memory_percent': memory_avg,
            'average_disk_percent': disk_avg,
            'average_memory_used_mb': memory_used_avg,
            'average_memory_available_mb': memory_available_avg,
            'total_alerts': len(self.alerts),
            'recent_alerts': self.alerts[-5:],  # Last 5 alerts
            'total_snapshots': len(self.snapshots),
            'thresholds': self.thresholds
        }


class PerformanceProfiler:
    """Function-level performance profiler"""

    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor

    def profile_function(self, func_name: str = None):
        """Decorator to profile function performance"""
        def decorator(func):
    """# Example usage:
result = decorator("example_value")
print(f"Result: {result}")"""
            name = func_name or f"{func.__module__}.{func.__name__}"

            @wraps(func)
            def wrapper(*args, **kwargs):
    """# Example usage:
result = wrapper()
print(f"Result: {result}")"""
                start_time = time.time()
                start_memory = psutil.virtual_memory().used

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    end_memory = psutil.virtual_memory().used

                    execution_time = (end_time - start_time) * 1000  # ms
                    memory_delta = (end_memory - start_memory) / 1024 / 1024  # MB

                    self.monitor.record_metric(
                        f"function.{name}.execution_time",
                        execution_time,
                        "ms",
                        {"function": name}
                    )

                    self.monitor.record_metric(
                        f"function.{name}.memory_delta",
                        memory_delta,
                        "MB",
                        {"function": name}
                    )

            return wrapper
        return decorator


# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Global profiler instance
performance_profiler = PerformanceProfiler(performance_monitor)


def start_performance_monitoring():
    """Convenience function to start monitoring"""
    performance_monitor.start_monitoring()


def stop_performance_monitoring():
    """Convenience function to stop monitoring"""
    performance_monitor.stop_monitoring()


def get_performance_report():
    """Convenience function to get performance report"""
    return performance_monitor.get_performance_report()


def profile_function(func_name: str = None):
    """Convenience decorator for function profiling"""
    return performance_profiler.profile_function(func_name)


if __name__ == "__main__":
    # Example usage
    print("Starting performance monitoring...")
    start_performance_monitoring()

    # Simulate some work
    time.sleep(10)

    # Get report
    report = get_performance_report()
    print("Performance Report:")
    for key, value in report.items():
        print(f"  {key}: {value}")

    stop_performance_monitoring()
    print("Performance monitoring stopped.")
