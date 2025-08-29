#!/usr/bin/env python3
"""Generate basic analytics from stored health reports."""
from __future__ import annotations

from src.dashboard import generate_dashboard


def main() -> None:
    summary = generate_dashboard()
    if not summary:
        print("No health reports found.")
        return

    print(
        f"Average health score: {summary['average_health_score']:.2f}"
    )
    print(
        f"Status distribution chart saved to: {summary['chart_path']}"
    )


if __name__ == "__main__":
    main()
