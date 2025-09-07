"""Common fixtures for performance tests."""

import pytest
from unittest.mock import Mock

from ..utils.test_data import get_performance_test_data


@pytest.fixture
def performance_metrics():
    """Provide performance metric thresholds for tests."""
    return get_performance_test_data()["metrics"]


@pytest.fixture
def perf_monitor():
    """Mocked performance monitor."""
    monitor = Mock()
    monitor.start_monitoring.return_value = True
    monitor.stop_monitoring.return_value = True
    return monitor

