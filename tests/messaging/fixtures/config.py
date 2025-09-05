#!/usr/bin/env python3
"""Configuration fixtures for messaging tests."""

import tempfile
from pathlib import Path

import pytest
from src.services.models.messaging_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


@pytest.fixture(scope="session")
def test_config():
    """Test configuration for messaging system tests."""
    return {
        "test_agents": [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ],
        "test_message_types": [
            UnifiedMessageType.TEXT,
            UnifiedMessageType.BROADCAST,
            UnifiedMessageType.ONBOARDING,
        ],
        "test_priorities": [
            UnifiedMessagePriority.NORMAL,
            UnifiedMessagePriority.URGENT,
        ],
        "test_tags": [
            UnifiedMessageTag.CAPTAIN,
            UnifiedMessageTag.ONBOARDING,
            UnifiedMessageTag.WRAPUP,
        ],
        "performance_thresholds": {
            "single_message_timeout": 1.0,
            "bulk_message_timeout": 10.0,
            "concurrent_message_timeout": 5.0,
            "min_throughput": 10.0,
            "max_memory_per_message": 1024,
        },
    }


@pytest.fixture
def temp_inbox_dirs():
    """Create temporary inbox directories for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        inbox_dirs = {}
        for i in range(1, 9):
            agent_dir = Path(temp_dir) / f"Agent-{i}" / "inbox"
            agent_dir.mkdir(parents=True)
            inbox_dirs[f"Agent-{i}"] = str(agent_dir)
        yield inbox_dirs
