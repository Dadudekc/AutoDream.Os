"""Logging utilities for testing orchestrator modules."""
from __future__ import annotations

import logging
from src.utils.logger import get_logger
from .orchestrator_config import DEFAULT_LOG_LEVEL


def setup_logger(name: str) -> logging.Logger:
    """Return a logger configured for the testing orchestrator."""
    logger = get_logger(name)
    logger.setLevel(getattr(logging, DEFAULT_LOG_LEVEL))
    return logger
