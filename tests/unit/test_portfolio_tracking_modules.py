"""Unit tests for modular portfolio tracking components."""

from datetime import datetime, timedelta

import pytest

# Skip these tests if pandas isn't installed since the underlying modules depend on it
pytest.importorskip("pandas")

from src.services.financial.portfolio.data_management import PerformanceDataManager
from src.services.financial.portfolio.reporting import PerformanceReporter
from src.services.financial.portfolio.tracking_logic import (
    PerformanceSnapshot,
    PortfolioPerformanceTracker,
)


def create_snapshot(ts: datetime, value: float) -> PerformanceSnapshot:
    return PerformanceSnapshot(
        timestamp=ts,
        total_value=value,
        total_return=0.0,
        daily_return=0.0,
        weights={"AAPL": 1.0},
        metrics={},
        allocations=[],
    )


def test_data_manager_save_load(tmp_path):
    manager = PerformanceDataManager(tmp_path)
    snap = create_snapshot(datetime.now(), 100.0)
    manager.save_snapshot(snap)
    history = manager.load_history()
    assert len(history) == 1
    assert history[0].total_value == 100.0


def test_reporting_module(tmp_path):
    manager = PerformanceDataManager(tmp_path)
    reporter = PerformanceReporter(manager)
    ts = datetime.now()
    history = [
        create_snapshot(ts, 100.0),
        create_snapshot(ts + timedelta(days=1), 110.0),
    ]
    report = reporter.generate_report(history, ts, ts + timedelta(days=1))
    assert report is not None
    assert report.total_return == pytest.approx(0.1)


def test_tracking_integration(tmp_path):
    manager = PerformanceDataManager(tmp_path)
    tracker = PortfolioPerformanceTracker(manager)
    tracker.track_portfolio_performance(100.0, {"AAPL": 1.0})
    tracker.track_portfolio_performance(110.0, {"AAPL": 1.0})
    start = tracker.performance_history[0].timestamp
    end = tracker.performance_history[-1].timestamp
    report = tracker.generate_report(start, end)
    assert report is not None
    assert report.total_return == pytest.approx(0.1)
