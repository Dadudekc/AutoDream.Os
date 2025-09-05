#!/usr/bin/env python3
"""Mock fixtures for messaging tests."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_metrics():
    """Mock metrics service for testing."""
    metrics = Mock()
    metrics.record_delivery = Mock()
    metrics.record_error = Mock()
    metrics.record_retry = Mock()
    metrics.get_stats = Mock(
        return_value={
            "total_deliveries": 0,
            "total_errors": 0,
            "total_retries": 0,
            "success_rate": 1.0,
        }
    )
    return metrics


@pytest.fixture
def mock_unified_logger():
    """Mock unified logger for testing."""
    logger = Mock()
    logger.log = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    logger.debug = Mock()
    return logger


@pytest.fixture
def mock_unified_config():
    """Mock unified configuration system for testing."""
    config = Mock()
    config.get_config = Mock(
        return_value={
            "delivery_method": "inbox",
            "retry_attempts": 3,
            "timeout": 30,
            "max_message_size": 1024 * 1024,
        }
    )
    config.get_agent_config = Mock(
        return_value={
            "coordinates": {"x": 100, "y": 200},
            "inbox_path": "agent_workspaces/Agent-1/inbox",
        }
    )
    return config
