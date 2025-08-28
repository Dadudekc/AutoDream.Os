"""Utility helpers for workflow reliability testing."""

from __future__ import annotations

import logging

# Single source of truth constants
DEFAULT_TIMEOUT: float = 60.0
DEFAULT_RETRY_COUNT: int = 3
RETRY_DELAY_SECONDS: float = 1.0


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger with basic configuration."""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
