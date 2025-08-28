"""Tests for MetricsDashboardService and related modules."""

from __future__ import annotations

from src.services.metrics_dashboard_service import MetricsDashboardService


def test_record_and_summarize() -> None:
    service = MetricsDashboardService()
    service.record_metric("alpha", 1.0)
    service.record_metric("alpha", 2.0)
    summary = service.get_summary()
    assert summary["total_metrics"] == 2
    assert summary["metrics_tracked"] == 1
    rendered = service.render_summary()
    assert "metrics_tracked" in rendered
