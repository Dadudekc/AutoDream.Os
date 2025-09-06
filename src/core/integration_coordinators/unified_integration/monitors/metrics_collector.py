"""
Metrics Collector
=================

Specialized component for collecting integration metrics.
Extracted from monitor.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import time
from typing import Dict, Any
from datetime import datetime, timedelta

from ..models import IntegrationType, IntegrationMetrics


class MetricsCollector:
    """Collects and processes integration metrics."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize metrics collector."""
        self.config = config
        self.metrics: Dict[IntegrationType, IntegrationMetrics] = {}

    def collect_metrics(self, integration_type: IntegrationType) -> IntegrationMetrics:
        """Collect metrics for specific integration type."""
        try:
            current_time = datetime.now()

            # Get or create metrics for this integration type
            if integration_type not in self.metrics:
                self.metrics[integration_type] = IntegrationMetrics(
                    integration_type=integration_type,
                    start_time=current_time,
                    end_time=current_time,
                    total_requests=0,
                    successful_requests=0,
                    failed_requests=0,
                    average_response_time=0.0,
                    peak_response_time=0.0,
                    throughput=0.0,
                    error_rate=0.0,
                    memory_usage=0.0,
                    cpu_usage=0.0,
                )

            metrics = self.metrics[integration_type]

            # Update basic metrics
            metrics.end_time = current_time
            metrics.total_requests += 1

            # Calculate derived metrics
            total_time = (metrics.end_time - metrics.start_time).total_seconds()
            if total_time > 0:
                metrics.throughput = metrics.total_requests / total_time

            if metrics.total_requests > 0:
                metrics.error_rate = metrics.failed_requests / metrics.total_requests

            return metrics

        except Exception as e:
            # Return empty metrics on error
            return IntegrationMetrics(
                integration_type=integration_type,
                start_time=datetime.now(),
                end_time=datetime.now(),
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                average_response_time=0.0,
                peak_response_time=0.0,
                throughput=0.0,
                error_rate=0.0,
                memory_usage=0.0,
                cpu_usage=0.0,
            )

    def update_metrics(
        self, integration_type: IntegrationType, success: bool, response_time: float
    ) -> None:
        """Update metrics with new data point."""
        try:
            if integration_type not in self.metrics:
                self.collect_metrics(integration_type)

            metrics = self.metrics[integration_type]

            # Update request counts
            if success:
                metrics.successful_requests += 1
            else:
                metrics.failed_requests += 1

            # Update response time metrics
            if response_time > metrics.peak_response_time:
                metrics.peak_response_time = response_time

            # Calculate running average
            total_requests = metrics.successful_requests + metrics.failed_requests
            if total_requests > 0:
                current_total = metrics.average_response_time * (total_requests - 1)
                metrics.average_response_time = (
                    current_total + response_time
                ) / total_requests

        except Exception as e:
            print(f"Error updating metrics: {e}")

    def get_metrics(self, integration_type: IntegrationType) -> IntegrationMetrics:
        """Get current metrics for integration type."""
        return self.metrics.get(
            integration_type, self.collect_metrics(integration_type)
        )

    def get_all_metrics(self) -> Dict[IntegrationType, IntegrationMetrics]:
        """Get all collected metrics."""
        return self.metrics.copy()

    def reset_metrics(self, integration_type: IntegrationType = None) -> None:
        """Reset metrics for specific type or all types."""
        try:
            if integration_type:
                if integration_type in self.metrics:
                    del self.metrics[integration_type]
            else:
                self.metrics.clear()
        except Exception as e:
            print(f"Error resetting metrics: {e}")

    def cleanup(self) -> None:
        """Cleanup metrics collector resources."""
        try:
            self.metrics.clear()
        except Exception as e:
            print(f"Metrics collector cleanup failed: {e}")
