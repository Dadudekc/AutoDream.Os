#!/usr/bin/env python3
"""
Simple Metrics Dashboard Service for testing
"""

import json
import time
from datetime import datetime
from typing import Dict, Optional

from refactoring.metrics import Metric, MetricsAggregator


class MetricsDashboardService:
    """Integration layer mapping metrics to dashboard summaries."""

    def __init__(self, metric_mapping: Optional[Dict[str, str]] = None) -> None:
        self.aggregator = MetricsAggregator()
        self.metric_mapping = metric_mapping or {}
        print("Metrics Dashboard Service initialized")

    def record_metric(self, name: str, value: float) -> None:
        metric = Metric("dashboard", name, value, time.time())
        self.aggregator.add([metric])
        print(f"Recorded metric {name}: {value}")

    def get_summary(self) -> Dict[str, object]:
        summary = self.aggregator.summary()
        summary["timestamp"] = datetime.now().isoformat()
        return summary

    def render_summary(self) -> str:
        summary = self.get_summary()
        if self.metric_mapping:
            dashboards: Dict[str, Dict[str, float]] = {}
            for metric_name, value in summary.get("averages", {}).items():
                dashboard = self.metric_mapping.get(metric_name, "default")
                dashboards.setdefault(dashboard, {})[metric_name] = value
            summary["dashboards"] = dashboards
        return json.dumps(summary)


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
        print(f"\nSummary: {json.dumps(summary, indent=2)}")
        print("Test completed successfully!")

        return

    print("Use --test to run test mode")


if __name__ == "__main__":
    main()
