"""Logging helpers for handoff modules."""

import logging


def get_handoff_logger(name: str) -> logging.Logger:
    """Return a logger configured for handoff operations.

    Args:
        name: Name of the logger.

    Returns:
        A ``logging.Logger`` instance.
    """
    return logging.getLogger(name)
