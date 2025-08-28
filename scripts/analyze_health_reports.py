#!/usr/bin/env python3
"""Generate basic analytics from stored health reports."""
from __future__ import annotations

from src.monitoring.data_acquisition import load_health_reports
from src.monitoring.metrics import average_health_score, status_counts
from src.monitoring.visualization import plot_status_distribution


def main() -> None:
    reports = load_health_reports()
    if not reports:
        print("No health reports found.")
        return

    counts = status_counts(reports)
    avg_score = average_health_score(reports)
    chart_path = plot_status_distribution(counts)

    print(f"Average health score: {avg_score:.2f}")
    print(f"Status distribution chart saved to: {chart_path}")


if __name__ == "__main__":
    main()
