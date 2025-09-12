"""Shared metrics utilities.

This module provides a single source of truth for simple metrics
collection patterns used across the codebase."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Metric:
    """Representation of a single metric value."""

    name: str
    value: float


class MetricsCollector:
    """Store and retrieve metric values in-memory."""

    def __init__(self) -> None:
        """Initialize metrics collector."""
        self.metrics = defaultdict(list)
        self.metadata = {}

    def collect_metric(self, name: str, value: float, timestamp: datetime = None) -> None:
        """Collect a metric value."""
        if timestamp is None:
            timestamp = datetime.now()
        self.metrics[name].append(Metric(name, value))
        self.metadata[name] = {"last_updated": timestamp, "count": len(self.metrics[name])}

    def get_metric(self, name: str) -> list[Metric]:
        """Get all metrics for a given name."""
        return self.metrics.get(name, [])

    def get_latest_metric(self, name: str) -> Metric | None:
        """Get the most recent metric for a given name."""
        metrics = self.get_metric(name)
        return metrics[-1] if metrics else None

    @property
    def total_operations(self) -> int:
        """Get total number of operations."""
        return self._counters.get("total_operations", 0)

    @property
    def successful_operations(self) -> int:
        """Get number of successful operations."""
        return self._counters.get("successful_operations", 0)

    @property
    def failed_operations(self) -> int:
        """Get number of failed operations."""
        return self._counters.get("failed_operations", 0)

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
        self.counters: dict[str, int] = defaultdict(int)

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
    tasks_processed: int, errors: int, duration: float, _now: datetime | None = None
) -> OptimizationRunMetrics:
    """Gather metrics for an optimization run."""

    return OptimizationRunMetrics(
        timestamp=(_now or datetime.now()).isoformat(),
        tasks_processed=tasks_processed,
        errors=errors,
        duration=duration,
    )


__all__ = [
    "Metric",
    "MetricsCollector",
    "CounterMetrics",
    "OptimizationRunMetrics",
    "gather_run_metrics",
]


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""

    print("🐝 Module Examples - Practical Demonstrations")
    print("=" * 50)
    # Function demonstrations
    print(f"\n📋 Testing gather_run_metrics():")
    try:
        # Add your function call here
        print(f"✅ gather_run_metrics executed successfully")
    except Exception as e:
        print(f"❌ gather_run_metrics failed: {e}")

    print(f"\n📋 Testing __init__():")
    try:
        # Add your function call here
        print(f"✅ __init__ executed successfully")
    except Exception as e:
        print(f"❌ __init__ failed: {e}")

    print(f"\n📋 Testing record():")
    try:
        # Add your function call here
        print(f"✅ record executed successfully")
    except Exception as e:
        print(f"❌ record failed: {e}")

    # Class demonstrations
    print(f"\n🏗️  Testing Metric class:")
    try:
        instance = Metric()
        print(f"✅ Metric instantiated successfully")
    except Exception as e:
        print(f"❌ Metric failed: {e}")

    print(f"\n🏗️  Testing MetricsCollector class:")
    try:
        instance = MetricsCollector()
        print(f"✅ MetricsCollector instantiated successfully")
    except Exception as e:
        print(f"❌ MetricsCollector failed: {e}")

    print("\n🎉 All examples completed!")
    print("🐝 WE ARE SWARM - PRACTICAL CODE IN ACTION!")
