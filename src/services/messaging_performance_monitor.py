#!/usr/bin/env python3
"""
Messaging Performance Monitor
=============================

Specialized performance monitoring for messaging systems with comprehensive metrics collection,
bottleneck detection, and real-time performance analysis.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import asyncio
import statistics
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import psutil

from services.advanced_analytics_service import get_analytics_service


@dataclass
class MessagingPerformanceMetrics:
    """Comprehensive messaging performance metrics."""

    # Timing metrics
    message_delivery_time: float = 0.0
    message_processing_time: float = 0.0
    message_routing_time: float = 0.0
    queue_wait_time: float = 0.0

    # Throughput metrics
    messages_per_second: float = 0.0
    queue_processing_rate: float = 0.0
    delivery_success_rate: float = 100.0

    # Resource metrics
    cpu_usage_percent: float = 0.0
    memory_usage_mb: float = 0.0
    io_operations_per_second: float = 0.0

    # Queue metrics
    queue_depth: int = 0
    queue_max_depth: int = 0
    messages_queued: int = 0
    messages_processed: int = 0

    # Error metrics
    delivery_errors: int = 0
    routing_errors: int = 0
    timeout_errors: int = 0
    error_rate_percent: float = 0.0

    # System health
    health_score: float = 100.0
    bottleneck_detected: bool = False
    bottleneck_description: str = ""
    optimization_recommendations: List[str] = field(default_factory=list)

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    measurement_period_seconds: int = 60


@dataclass
class PerformanceThresholds:

EXAMPLE USAGE:
==============

# Import the service
from src.services.messaging_performance_monitor import Messaging_Performance_MonitorService

# Initialize service
service = Messaging_Performance_MonitorService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Messaging_Performance_MonitorService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

    """Configurable performance thresholds for monitoring."""

    # Response time thresholds (seconds)
    max_delivery_time: float = 5.0
    max_processing_time: float = 2.0
    max_routing_time: float = 1.0
    max_queue_wait_time: float = 10.0

    # Throughput thresholds
    min_messages_per_second: float = 10.0
    min_delivery_success_rate: float = 95.0

    # Resource thresholds
    max_cpu_usage_percent: float = 80.0
    max_memory_usage_mb: float = 512.0

    # Queue thresholds
    max_queue_depth: int = 1000
    max_error_rate_percent: float = 5.0

    # Alert thresholds
    critical_cpu_threshold: float = 90.0
    critical_memory_threshold: float = 1024.0
    critical_error_rate_threshold: float = 10.0


class MessagingPerformanceMonitor:
    """Advanced performance monitoring for messaging systems."""

    def __init__(self, service_name: str = "MessagingService"):
        self.service_name = service_name
        self.analytics_service = get_analytics_service()

        # Metrics storage
        self.current_metrics = MessagingPerformanceMetrics()
        self.metrics_history = deque(maxlen=1000)  # Keep last 1000 measurements

        # Thresholds
        self.thresholds = PerformanceThresholds()

        # Monitoring state
        self.is_monitoring = False
        self.monitoring_thread = None
        self.measurement_interval = 10  # seconds

        # Performance tracking
        self.message_delivery_times = deque(maxlen=1000)
        self.message_processing_times = deque(maxlen=1000)
        self.error_counts = deque(maxlen=100)
        self.throughput_counts = deque(maxlen=100)

        # Bottleneck detection
        self.bottleneck_history = deque(maxlen=50)
        self.optimization_suggestions = []

    def start_monitoring(self) -> None:
        """Start performance monitoring."""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()

        # Register with analytics service
        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.monitoring_status",
            1,
            {"status": "active", "monitor_type": "performance"}
        )

        print(f"🚀 Started messaging performance monitoring for {self.service_name}")

    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)

        # Update analytics service
        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.monitoring_status",
            0,
            {"status": "stopped", "monitor_type": "performance"}
        )

        print(f"🛑 Stopped messaging performance monitoring for {self.service_name}")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        last_measurement = time.time()

        while self.is_monitoring:
            current_time = time.time()

            # Collect metrics at specified interval
            if current_time - last_measurement >= self.measurement_interval:
                try:
                    self._collect_performance_metrics()
                    self._analyze_bottlenecks()
                    self._store_metrics()
                    last_measurement = current_time
                except Exception as e:
                    print(f"❌ Error in performance monitoring: {e}")

            time.sleep(1)  # Check every second

    def _collect_performance_metrics(self) -> None:
        """Collect comprehensive performance metrics."""
        # Reset current metrics
        self.current_metrics = MessagingPerformanceMetrics()
        self.current_metrics.timestamp = datetime.now()
        self.current_metrics.measurement_period_seconds = self.measurement_interval

        # Collect system resource metrics
        self._collect_system_metrics()

        # Collect messaging-specific metrics
        self._collect_messaging_metrics()

        # Calculate derived metrics
        self._calculate_derived_metrics()

        # Check thresholds and generate alerts
        self._check_thresholds()

    def _collect_system_metrics(self) -> None:
        """Collect system resource metrics."""
        try:
            # CPU usage
            self.current_metrics.cpu_usage_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            self.current_metrics.memory_usage_mb = memory.used / (1024 * 1024)

            # I/O operations (simplified)
            io_counters = psutil.disk_io_counters()
            if io_counters:
                self.current_metrics.io_operations_per_second = io_counters.read_count + io_counters.write_count

        except Exception as e:
            print(f"⚠️ Error collecting system metrics: {e}")

    def _collect_messaging_metrics(self) -> None:
        """Collect messaging-specific performance metrics."""
        try:
            # Get metrics from analytics service
            analytics = self.analytics_service

            # Queue metrics (if available)
            queue_depth = analytics.get_metrics_stats("messaging.queue_depth", 1)
            if "latest" in queue_depth and queue_depth["latest"] is not None:
                self.current_metrics.queue_depth = int(queue_depth["latest"])

            # Message processing metrics
            processed = analytics.get_metrics_stats("messaging.messages_processed", 1)
            if "latest" in processed and processed["latest"] is not None:
                self.current_metrics.messages_processed = int(processed["latest"])

            # Error metrics
            errors = analytics.get_metrics_stats("messaging.delivery_errors", 1)
            if "latest" in errors and errors["latest"] is not None:
                self.current_metrics.delivery_errors = int(errors["latest"])

            # Calculate throughput
            if len(self.throughput_counts) > 0:
                recent_throughput = list(self.throughput_counts)[-10:]  # Last 10 measurements
                if recent_throughput:
                    self.current_metrics.messages_per_second = statistics.mean(recent_throughput) / self.measurement_interval

            # Calculate timing metrics
            if self.message_delivery_times:
                self.current_metrics.message_delivery_time = statistics.mean(self.message_delivery_times)

            if self.message_processing_times:
                self.current_metrics.message_processing_time = statistics.mean(self.message_processing_times)

        except Exception as e:
            print(f"⚠️ Error collecting messaging metrics: {e}")

    def _calculate_derived_metrics(self) -> None:
        """Calculate derived performance metrics."""
        # Calculate error rate
        total_operations = self.current_metrics.messages_processed + self.current_metrics.delivery_errors
        if total_operations > 0:
            self.current_metrics.error_rate_percent = (self.current_metrics.delivery_errors / total_operations) * 100

        # Calculate delivery success rate
        if self.current_metrics.messages_processed > 0:
            total_messages = self.current_metrics.messages_processed + self.current_metrics.delivery_errors
            if total_messages > 0:
                self.current_metrics.delivery_success_rate = (self.current_metrics.messages_processed / total_messages) * 100

        # Calculate health score (0-100)
        health_factors = []

        # CPU health (lower is better)
        cpu_health = max(0, 100 - (self.current_metrics.cpu_usage_percent / self.thresholds.max_cpu_usage_percent) * 100)
        health_factors.append(cpu_health)

        # Memory health (lower is better)
        memory_health = max(0, 100 - (self.current_metrics.memory_usage_mb / self.thresholds.max_memory_usage_mb) * 100)
        health_factors.append(memory_health)

        # Error rate health (lower is better)
        error_health = max(0, 100 - (self.current_metrics.error_rate_percent / self.thresholds.max_error_rate_percent) * 100)
        health_factors.append(error_health)

        # Queue depth health (lower is better)
        queue_health = max(0, 100 - (self.current_metrics.queue_depth / self.thresholds.max_queue_depth) * 100)
        health_factors.append(queue_health)

        # Throughput health (higher is better)
        throughput_health = min(100, (self.current_metrics.messages_per_second / max(1, self.thresholds.min_messages_per_second)) * 100)
        health_factors.append(throughput_health)

        if health_factors:
            self.current_metrics.health_score = statistics.mean(health_factors)

    def _check_thresholds(self) -> None:
        """Check performance thresholds and generate alerts."""
        alerts = []

        # CPU threshold check
        if self.current_metrics.cpu_usage_percent > self.thresholds.critical_cpu_threshold:
            alerts.append(f"CRITICAL: CPU usage at {self.current_metrics.cpu_usage_percent:.1f}% (threshold: {self.thresholds.critical_cpu_threshold}%)")

        # Memory threshold check
        if self.current_metrics.memory_usage_mb > self.thresholds.critical_memory_threshold:
            alerts.append(f"CRITICAL: Memory usage at {self.current_metrics.memory_usage_mb:.1f}MB (threshold: {self.thresholds.critical_memory_threshold}MB)")

        # Error rate threshold check
        if self.current_metrics.error_rate_percent > self.thresholds.critical_error_rate_threshold:
            alerts.append(f"CRITICAL: Error rate at {self.current_metrics.error_rate_percent:.1f}% (threshold: {self.thresholds.critical_error_rate_threshold}%)")

        # Queue depth warning
        if self.current_metrics.queue_depth > self.thresholds.max_queue_depth * 0.8:
            alerts.append(f"WARNING: Queue depth at {self.current_metrics.queue_depth} (near limit: {self.thresholds.max_queue_depth})")

        # Delivery time warning
        if self.current_metrics.message_delivery_time > self.thresholds.max_delivery_time:
            alerts.append(f"WARNING: Message delivery time at {self.current_metrics.message_delivery_time:.2f}s (threshold: {self.thresholds.max_delivery_time}s)")

        # Send alerts to analytics service
        for alert in alerts:
            self.analytics_service.collect_custom_metric(
                f"{self.service_name}.alert",
                1,
                {
                    "alert_type": "performance",
                    "severity": "critical" if "CRITICAL" in alert else "warning",
                    "message": alert,
                    "timestamp": datetime.now().isoformat()
                }
            )

    def _analyze_bottlenecks(self) -> None:
        """Analyze performance data to identify bottlenecks."""
        bottlenecks = []

        # CPU bottleneck detection
        if self.current_metrics.cpu_usage_percent > self.thresholds.max_cpu_usage_percent:
            bottlenecks.append({
                "type": "cpu",
                "severity": "high" if self.current_metrics.cpu_usage_percent > 90 else "medium",
                "description": f"High CPU usage: {self.current_metrics.cpu_usage_percent:.1f}%",
                "recommendation": "Consider optimizing message processing algorithms or scaling resources"
            })

        # Memory bottleneck detection
        if self.current_metrics.memory_usage_mb > self.thresholds.max_memory_usage_mb * 0.8:
            bottlenecks.append({
                "type": "memory",
                "severity": "high" if self.current_metrics.memory_usage_mb > self.thresholds.max_memory_usage_mb else "medium",
                "description": f"High memory usage: {self.current_metrics.memory_usage_mb:.1f}MB",
                "recommendation": "Implement memory-efficient message queuing or increase system memory"
            })

        # Queue bottleneck detection
        if self.current_metrics.queue_depth > self.thresholds.max_queue_depth * 0.7:
            bottlenecks.append({
                "type": "queue",
                "severity": "high" if self.current_metrics.queue_depth > self.thresholds.max_queue_depth * 0.9 else "medium",
                "description": f"Queue depth: {self.current_metrics.queue_depth} messages",
                "recommendation": "Increase processing capacity or optimize message routing"
            })

        # Throughput bottleneck detection
        if self.current_metrics.messages_per_second < self.thresholds.min_messages_per_second * 0.5:
            bottlenecks.append({
                "type": "throughput",
                "severity": "high",
                "description": f"Low throughput: {self.current_metrics.messages_per_second:.1f} msg/s",
                "recommendation": "Optimize message processing pipeline or scale processing resources"
            })

        # Timing bottleneck detection
        if self.current_metrics.message_delivery_time > self.thresholds.max_delivery_time:
            bottlenecks.append({
                "type": "latency",
                "severity": "medium",
                "description": f"High delivery latency: {self.current_metrics.message_delivery_time:.2f}s",
                "recommendation": "Optimize delivery mechanisms or reduce network latency"
            })

        # Update current metrics with bottleneck information
        if bottlenecks:
            self.current_metrics.bottleneck_detected = True
            self.current_metrics.bottleneck_description = f"{len(bottlenecks)} bottleneck(s) detected"

            # Generate optimization recommendations
            recommendations = []
            for bottleneck in bottlenecks:
                recommendations.append(f"{bottleneck['type'].upper()}: {bottleneck['recommendation']}")

            self.current_metrics.optimization_recommendations = recommendations

            # Store bottleneck history
            self.bottleneck_history.append({
                "timestamp": datetime.now(),
                "bottlenecks": bottlenecks,
                "metrics": self.current_metrics
            })

        # Send bottleneck data to analytics service
        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.bottlenecks_detected",
            len(bottlenecks),
            {
                "bottleneck_types": [b["type"] for b in bottlenecks],
                "severity_levels": list(set(b["severity"] for b in bottlenecks))
            }
        )

    def _store_metrics(self) -> None:
        """Store current metrics in history."""
        self.metrics_history.append(self.current_metrics)

        # Send key metrics to analytics service
        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.health_score",
            self.current_metrics.health_score,
            {"measurement_period": self.measurement_interval}
        )

        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.cpu_usage",
            self.current_metrics.cpu_usage_percent,
            {"unit": "percent"}
        )

        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.memory_usage",
            self.current_metrics.memory_usage_mb,
            {"unit": "MB"}
        )

        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.queue_depth",
            self.current_metrics.queue_depth,
            {"unit": "messages"}
        )

        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.error_rate",
            self.current_metrics.error_rate_percent,
            {"unit": "percent"}
        )

        self.analytics_service.collect_custom_metric(
            f"{self.service_name}.throughput",
            self.current_metrics.messages_per_second,
            {"unit": "messages_per_second"}
        )

    def get_current_metrics(self) -> MessagingPerformanceMetrics:
        """Get current performance metrics."""
        return self.current_metrics

    def get_metrics_history(self, hours_back: int = 1) -> List[MessagingPerformanceMetrics]:
        """Get metrics history for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        return [m for m in self.metrics_history if m.timestamp >= cutoff_time]

    def get_performance_summary(self, hours_back: int = 1) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        history = self.get_metrics_history(hours_back)

        if not history:
            return {"error": "No metrics history available"}

        # Calculate averages and trends
        health_scores = [m.health_score for m in history]
        cpu_usage = [m.cpu_usage_percent for m in history]
        memory_usage = [m.memory_usage_mb for m in history]
        queue_depths = [m.queue_depth for m in history]
        error_rates = [m.error_rate_percent for m in history]
        throughputs = [m.messages_per_second for m in history]

        summary = {
            "period_hours": hours_back,
            "measurements_count": len(history),
            "averages": {
                "health_score": statistics.mean(health_scores) if health_scores else 0,
                "cpu_usage_percent": statistics.mean(cpu_usage) if cpu_usage else 0,
                "memory_usage_mb": statistics.mean(memory_usage) if memory_usage else 0,
                "queue_depth": statistics.mean(queue_depths) if queue_depths else 0,
                "error_rate_percent": statistics.mean(error_rates) if error_rates else 0,
                "throughput_msg_per_sec": statistics.mean(throughputs) if throughputs else 0
            },
            "peaks": {
                "cpu_usage_percent": max(cpu_usage) if cpu_usage else 0,
                "memory_usage_mb": max(memory_usage) if memory_usage else 0,
                "queue_depth": max(queue_depths) if queue_depths else 0,
                "error_rate_percent": max(error_rates) if error_rates else 0
            },
            "current_bottlenecks": len([m for m in history if m.bottleneck_detected]),
            "threshold_violations": self._count_threshold_violations(history)
        }

        return summary

    def _count_threshold_violations(self, history: List[MessagingPerformanceMetrics]) -> Dict[str, int]:
        """Count threshold violations in metrics history."""
        violations = {
            "cpu_threshold": 0,
            "memory_threshold": 0,
            "queue_threshold": 0,
            "error_rate_threshold": 0,
            "delivery_time_threshold": 0
        }

        for metrics in history:
            if metrics.cpu_usage_percent > self.thresholds.max_cpu_usage_percent:
                violations["cpu_threshold"] += 1
            if metrics.memory_usage_mb > self.thresholds.max_memory_usage_mb:
                violations["memory_threshold"] += 1
            if metrics.queue_depth > self.thresholds.max_queue_depth:
                violations["queue_threshold"] += 1
            if metrics.error_rate_percent > self.thresholds.max_error_rate_percent:
                violations["error_rate_threshold"] += 1
            if metrics.message_delivery_time > self.thresholds.max_delivery_time:
                violations["delivery_time_threshold"] += 1

        return violations

    def record_message_delivery(self, delivery_time: float, success: bool = True) -> None:
        """Record a message delivery event."""
        self.message_delivery_times.append(delivery_time)

        # Update throughput tracking
        current_minute = int(time.time() // 60)
        if not self.throughput_counts or self.throughput_counts[-1][0] != current_minute:
            self.throughput_counts.append([current_minute, 0])
        self.throughput_counts[-1][1] += 1

        # Track errors
        if not success:
            self.error_counts.append(time.time())

    def record_message_processing(self, processing_time: float) -> None:
        """Record message processing time."""
        self.message_processing_times.append(processing_time)

    def update_thresholds(self, new_thresholds: Dict[str, Any]) -> None:
        """Update performance thresholds."""
        for key, value in new_thresholds.items():
            if hasattr(self.thresholds, key):
                setattr(self.thresholds, key, value)

        print(f"✅ Updated performance thresholds: {new_thresholds}")

    def generate_optimization_report(self) -> Dict[str, Any]:
        """Generate comprehensive optimization report."""
        summary = self.get_performance_summary(hours_back=24)
        recent_bottlenecks = list(self.bottleneck_history)[-10:]  # Last 10 bottleneck events

        report = {
            "generated_at": datetime.now().isoformat(),
            "service_name": self.service_name,
            "analysis_period_hours": 24,
            "performance_summary": summary,
            "bottleneck_analysis": {
                "total_bottlenecks_detected": len(self.bottleneck_history),
                "recent_bottlenecks": recent_bottlenecks,
                "most_common_bottleneck_types": self._analyze_bottleneck_patterns()
            },
            "optimization_recommendations": self._generate_optimization_recommendations(summary),
            "trend_analysis": self._analyze_performance_trends(),
            "capacity_planning": self._generate_capacity_recommendations(summary)
        }

        return report

    def _analyze_bottleneck_patterns(self) -> Dict[str, int]:
        """Analyze patterns in bottleneck occurrences."""
        patterns = {}

        for bottleneck_event in self.bottleneck_history:
            for bottleneck in bottleneck_event["bottlenecks"]:
                bottleneck_type = bottleneck["type"]
                patterns[bottleneck_type] = patterns.get(bottleneck_type, 0) + 1

        return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))

    def _generate_optimization_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on performance data."""
        recommendations = []

        averages = summary.get("averages", {})

        # CPU optimization
        if averages.get("cpu_usage_percent", 0) > 70:
            recommendations.append("Implement CPU optimization: Consider async processing, reduce synchronous operations, or scale processing resources")

        # Memory optimization
        if averages.get("memory_usage_mb", 0) > 400:
            recommendations.append("Implement memory optimization: Use streaming for large messages, implement message cleanup policies, or increase memory allocation")

        # Queue optimization
        if averages.get("queue_depth", 0) > 500:
            recommendations.append("Implement queue optimization: Increase processing concurrency, implement message batching, or scale queue processing capacity")

        # Error rate optimization
        if averages.get("error_rate_percent", 0) > 2:
            recommendations.append("Implement error rate optimization: Add retry mechanisms, improve error handling, validate message formats before processing")

        # Throughput optimization
        if averages.get("throughput_msg_per_sec", 0) < 15:
            recommendations.append("Implement throughput optimization: Parallelize message processing, optimize routing algorithms, reduce I/O operations")

        return recommendations

    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over time."""
        if len(self.metrics_history) < 10:
            return {"insufficient_data": True}

        # Get recent metrics (last 20 measurements)
        recent = list(self.metrics_history)[-20:]

        trends = {}
        for metric_name in ["health_score", "cpu_usage_percent", "memory_usage_mb", "queue_depth", "error_rate_percent"]:
            values = [getattr(m, metric_name) for m in recent if hasattr(m, metric_name)]

            if len(values) >= 5:
                # Simple trend analysis
                first_half = values[:len(values)//2]
                second_half = values[len(values)//2:]

                first_avg = statistics.mean(first_half)
                second_avg = statistics.mean(second_half)

                if second_avg > first_avg * 1.1:
                    trend = "increasing"
                elif second_avg < first_avg * 0.9:
                    trend = "decreasing"
                else:
                    trend = "stable"

                trends[metric_name] = {
                    "trend": trend,
                    "change_percent": ((second_avg - first_avg) / first_avg) * 100 if first_avg != 0 else 0
                }

        return trends

    def _generate_capacity_recommendations(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate capacity planning recommendations."""
        averages = summary.get("averages", {})
        peaks = summary.get("peaks", {})

        recommendations = {
            "cpu_capacity": "adequate",
            "memory_capacity": "adequate",
            "queue_capacity": "adequate",
            "processing_capacity": "adequate"
        }

        # CPU capacity analysis
        if peaks.get("cpu_usage_percent", 0) > 85:
            recommendations["cpu_capacity"] = "increase_recommended"
        elif averages.get("cpu_usage_percent", 0) > 60:
            recommendations["cpu_capacity"] = "monitor_closely"

        # Memory capacity analysis
        if peaks.get("memory_usage_mb", 0) > 800:
            recommendations["memory_capacity"] = "increase_recommended"
        elif averages.get("memory_usage_mb", 0) > 400:
            recommendations["memory_capacity"] = "monitor_closely"

        # Queue capacity analysis
        if peaks.get("queue_depth", 0) > 800:
            recommendations["queue_capacity"] = "increase_recommended"
        elif averages.get("queue_depth", 0) > 500:
            recommendations["queue_capacity"] = "monitor_closely"

        return recommendations


# Global monitor instance
_messaging_monitor = None

def get_messaging_performance_monitor(service_name: str = "MessagingService") -> MessagingPerformanceMonitor:
    """Get the global messaging performance monitor instance."""
    global _messaging_monitor
    if _messaging_monitor is None:
        _messaging_monitor = MessagingPerformanceMonitor(service_name)
    return _messaging_monitor
