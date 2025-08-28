"""Simple Metrics Dashboard Service for testing"""

from __future__ import annotations

from typing import Any, Dict

from .dashboard_collectors import MetricsCollector
from .dashboard_processing import summarize_metrics
from .dashboard_renderer import DashboardRenderer


class MetricsDashboardService:
    """Orchestrates metric collection, processing, and rendering."""

    def __init__(self) -> None:
        self.collector = MetricsCollector()
        self.renderer = DashboardRenderer()
        print("Metrics Dashboard Service initialized")

    def record_metric(self, name: str, value: float) -> None:
        """Record a metric value."""
        self.collector.record(name, value)
        print(f"Recorded metric {name}: {value}")

    def get_summary(self) -> Dict[str, Any]:
        """Return summarized metric information."""
        return summarize_metrics(self.collector.metrics)

    def render_summary(self) -> str:
        """Render the summary as a JSON string."""
        return self.renderer.render(self.get_summary())


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Simple Metrics Dashboard Service")
    parser.add_argument("--test", action="store_true", help="Run test mode")

    args = parser.parse_args()

    if args.test:
        print("Running Metrics Dashboard Service in test mode...")

        dashboard = MetricsDashboardService()

        # Record some test metrics
        dashboard.record_metric("test.counter", 42)
        dashboard.record_metric("test.gauge", 75.5)
        dashboard.record_metric("system.cpu", 45.2)

        # Show summary
        print(f"\nSummary: {dashboard.render_summary()}")
        print("Test completed successfully!")

        return

    print("Use --test to run test mode")


if __name__ == "__main__":
    main()
