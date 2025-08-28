#!/usr/bin/env python3
"""Simple metrics dashboard demonstrating the metrics pipeline modules."""

from __future__ import annotations

import json

from .metrics_pipeline.data_collection import MetricsDataCollector
from .metrics_pipeline.data_exporter import MetricsExporter
from .metrics_pipeline.data_transformer import MetricsTransformer
from .metrics_pipeline.metrics_config import DEFAULT_EXPORT_PATH


class MetricsDashboardService:
    """Coordinates the data collection, transformation and export stages."""

    def __init__(self) -> None:
        self.collector = MetricsDataCollector()
        self.transformer = MetricsTransformer()
        self.exporter = MetricsExporter()
        print("Metrics Dashboard Service initialized")

    def record_metric(self, name: str, value: float) -> None:
        """Record a single metric value."""

        self.collector.record(name, value)
        print(f"Recorded metric {name}: {value}")

    def get_summary(self) -> dict:
        """Return a summary of collected metrics."""

        return self.transformer.summarize(self.collector.metrics)

    def export_metrics(self, path: str = DEFAULT_EXPORT_PATH) -> bool:
        """Export collected metrics to ``path``.

        Returns ``True`` when the export succeeds.
        """

        success = self.exporter.export(self.collector.metrics, filename=path)
        if success:
            print(f"Exported metrics to {path}")
        return success


def main():
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
        summary = dashboard.get_summary()
        print(f"\\nSummary: {json.dumps(summary, indent=2)}")
        print("Test completed successfully!")

        return

    print("Use --test to run test mode")


if __name__ == "__main__":
    main()
