"""Common fixtures for performance tests."""


sys.path.append(get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), '..'))


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

