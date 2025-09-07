"""Shared fixtures for gaming tests."""

from __future__ import annotations

from typing import Any, Dict

import pytest

SSOT_CONFIG: Dict[str, Any] = {"environment": "test"}


@pytest.fixture
def ssot_config() -> Dict[str, Any]:
    """Provide the SSOT configuration for gaming tests."""
    return SSOT_CONFIG
