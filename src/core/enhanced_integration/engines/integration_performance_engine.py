#!/usr/bin/env python3
"""
Integration Performance Engine - V2 Compliance Module
=====================================================

Handles performance monitoring and metrics collection for integration operations.
Extracted from enhanced_integration_orchestrator.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import threading
import time
from datetime import datetime
from typing import Any

from ..integration_models import (
    IntegrationPerformanceMetrics,
    IntegrationPerformanceReport,
    create_performance_metrics,
    create_performance_report,
)


class IntegrationPerformanceEngine:
    """Engine for monitoring and reporting integration performance."""

    def __init__(self, config):
        """Initialize performance engine."""
        self.config = config
        self.logger = None  # Will be set by parent
        self.metrics = create_performance_metrics()
        self.metrics_history: list[IntegrationPerformanceMetrics] = []
        self.current_report = None
        self.monitoring_thread = None
        self.is_monitoring = False

    def start_monitoring(self):
        """Start performance monitoring."""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()

        if self.logger:
            self.logger.info("Performance monitoring started")

    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)

        if self.logger:
            self.logger.info("Performance monitoring stopped")

    def update_metrics(
        self,
        execution_time_ms: float,
        success: bool,
        active_tasks: int,
        queue_size: int,
    ):
        """Update performance metrics."""
        # Update current metrics
        if success:
            self.metrics.operations_per_second += 1

        # Update average latency (exponential moving average)
        alpha = 0.1
        self.metrics.average_latency_ms = (
            alpha * execution_time_ms + (1 - alpha) * self.metrics.average_latency_ms
        )

        # Update success/error rates
        total_ops = self.metrics.operations_per_second
        if total_ops > 0:
            self.metrics.success_rate = 0.9 if success else 0.8  # Simplified calculation
            self.metrics.error_rate = 1.0 - self.metrics.success_rate

        # Update efficiency score
        self.metrics.efficiency_score = self._calculate_efficiency_score()

        # Update resource utilization
        self.metrics.resource_utilization = {
            "active_tasks": active_tasks,
            "queue_size": queue_size,
            "thread_pool_active": 1,  # Simplified
        }

        self.metrics.active_integrations = active_tasks
        self.metrics.queue_size = queue_size

    def _calculate_efficiency_score(self) -> float:
        """Calculate overall efficiency score."""
        # Simplified efficiency calculation
        success_factor = self.metrics.success_rate
        latency_factor = max(0, 1.0 - (self.metrics.average_latency_ms / 1000.0))
        throughput_factor = min(1.0, self.metrics.operations_per_second / 100.0)

        efficiency = success_factor * 0.4 + latency_factor * 0.3 + throughput_factor * 0.3
        return min(efficiency, 1.0)

    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                # Store current metrics in history
                if len(self.metrics_history) >= self.config.max_metrics_history:
                    self.metrics_history.pop(0)

                self.metrics_history.append(self.metrics)

                # Reset per-second counters
                self.metrics.operations_per_second = 0

                time.sleep(self.config.performance_check_interval)

            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5.0)

    def generate_performance_report(self) -> IntegrationPerformanceReport:
        """Generate comprehensive performance report."""
        report = create_performance_report(f"report_{int(time.time())}")
        report.start_time = datetime.now()
        report.end_time = datetime.now()
        report.metrics = self.metrics
        report.metrics_history = self.metrics_history.copy()

        return report

    def get_performance_summary(self) -> dict[str, Any]:
        """Get current performance summary."""
        return {
            "current_metrics": self.metrics.to_dict(),
            "monitoring_active": self.is_monitoring,
            "history_size": len(self.metrics_history),
            "efficiency_score": self.metrics.efficiency_score,
            "resource_utilization": self.metrics.resource_utilization,
        }
