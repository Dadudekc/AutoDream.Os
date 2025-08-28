"""Logging utilities for task modules."""

from __future__ import annotations

import logging

from src.config import LOG_LEVEL

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_task_logger(name: str) -> logging.Logger:
    """Return a logger configured for task modules."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)
    return logger
