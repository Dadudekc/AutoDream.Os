#!/usr/bin/env python3
"""Pytest configuration for messaging system tests."""

import pytest

pytest_plugins = [
    "tests.messaging.fixtures.config",
    "tests.messaging.fixtures.mocks",
]


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        if "performance" in item.name:
            item.add_marker(pytest.mark.performance)
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
        if "unit" in item.name or "test_" in item.name:
            item.add_marker(pytest.mark.unit)
        if "slow" in item.name or "benchmark" in item.name:
            item.add_marker(pytest.mark.slow)
