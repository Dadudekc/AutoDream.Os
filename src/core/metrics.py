"""Shared metrics utilities.

This module provides a single source of truth for simple metrics
collection patterns used across the codebase."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Metric:
    """Representation of a single metric value."""

    name: str
    value: float


class MetricsCollector:
    """Store and retrieve metric values in-memory."""

    def __init__(self) -> None:
        self._metrics: Dict[str, float] = {}
        self._counters = CounterMetrics()

    def record(self, name: str, value: float) -> None:
        """Record a metric value."""

        self._metrics[name] = float(value)

    def get(self, name: str) -> Optional[float]:
        """Return the latest value for *name* if available."""

        return self._metrics.get(name)

    def all(self) -> Dict[str, float]:
        """Return a copy of all metrics."""

        return dict(self._metrics)

    @property
    def total_operations(self) -> int:
        return self._counters.get("total_operations")

    @property
    def successful_operations(self) -> int:
        return self._counters.get("successful_operations")

    @property
    def failed_operations(self) -> int:
        return self._counters.get("failed_operations")

    def record_success(self) -> None:
        """Record a successful operation."""

        self._counters.increment("total_operations")
        self._counters.increment("successful_operations")

    def record_failure(self) -> None:
        """Record a failed operation."""

        self._counters.increment("total_operations")
        self._counters.increment("failed_operations")


class CounterMetrics:
    """Lightweight counter-based metrics manager."""

    def __init__(self) -> None:
        self.counters: Dict[str, int] = defaultdict(int)

    def increment(self, name: str, amount: int = 1) -> None:
        """Increment a named counter."""

        self.counters[name] += amount

    def get(self, name: str) -> int:
        """Retrieve a counter value (defaults to 0)."""

        return self.counters.get(name, 0)


@dataclass
class OptimizationRunMetrics:
    """Metrics captured for a single optimization run."""

    timestamp: str
    tasks_processed: int
    errors: int
    duration: float


def gather_run_metrics(
    tasks_processed: int, errors: int, duration: float, _now: Optional[datetime] = None
) -> OptimizationRunMetrics:
    """Gather metrics for an optimization run."""

    return OptimizationRunMetrics(
        timestamp=(_now or datetime.now()).isoformat(),
        tasks_processed=tasks_processed,
        errors=errors,
        duration=duration,
    )


class MessagingMetrics:
    """V2 compliant metrics collection for messaging operations.

    This class provides comprehensive performance monitoring and metrics
    collection for the messaging system, ensuring V2 compliance requirements.
    """

    def __init__(self):
        """Initialize messaging metrics collector."""
        self.metrics = MetricsCollector()
        self.message_counts = defaultdict(int)
        self.delivery_times = []
        self.error_counts = defaultdict(int)

    def record_message_sent(self, message_type: str, recipient: str, delivery_method: str):
        """Record a successfully sent message.

        Args:
            message_type: Type of message (text, broadcast, onboarding)
            recipient: Agent that received the message
            delivery_method: Method used (pyautogui, inbox)
        """
        self.metrics.record_success()
        self.message_counts[f"{message_type}_{delivery_method}"] += 1
        self.message_counts[f"total_{recipient}"] += 1

    def record_message_failed(self, message_type: str, recipient: str, error_type: str):
        """Record a failed message delivery.

        Args:
            message_type: Type of message that failed
            recipient: Agent that should have received the message
            error_type: Type of error that occurred
        """
        self.metrics.record_failure()
        self.error_counts[f"{message_type}_{error_type}"] += 1
        self.error_counts[f"failed_{recipient}"] += 1

    def record_delivery_time(self, delivery_time: float):
        """Record delivery time for performance monitoring.

        Args:
            delivery_time: Time in seconds to deliver the message
        """
        self.delivery_times.append(delivery_time)
        # Keep only last 100 delivery times for memory efficiency
        if len(self.delivery_times) > 100:
            self.delivery_times = self.delivery_times[-100:]

    def get_delivery_stats(self) -> Dict[str, float]:
        """Get delivery time statistics.

        Returns:
            Dictionary with mean, min, max delivery times
        """
        if not self.delivery_times:
            return {"mean": 0.0, "min": 0.0, "max": 0.0}

        return {
            "mean": sum(self.delivery_times) / len(self.delivery_times),
            "min": min(self.delivery_times),
            "max": max(self.delivery_times),
        }

    def get_success_rate(self) -> float:
        """Calculate overall success rate.

        Returns:
            Success rate as a percentage (0-100)
        """
        total = self.metrics.total_operations
        if total == 0:
            return 100.0

        successful = self.metrics.successful_operations
        return (successful / total) * 100.0

    def get_message_counts(self) -> Dict[str, int]:
        """Get message delivery counts by type and method.

        Returns:
            Dictionary of message counts
        """
        return dict(self.message_counts)

    def get_error_summary(self) -> Dict[str, int]:
        """Get error counts by type.

        Returns:
            Dictionary of error counts
        """
        return dict(self.error_counts)

    def reset(self):
        """Reset all metrics (useful for testing or periodic resets)."""
        self.metrics = MetricsCollector()
        self.message_counts.clear()
        self.delivery_times.clear()
        self.error_counts.clear()


__all__ = [
    "Metric",
    "MetricsCollector",
    "CounterMetrics",
    "OptimizationRunMetrics",
    "MessagingMetrics",
    "gather_run_metrics",
]
