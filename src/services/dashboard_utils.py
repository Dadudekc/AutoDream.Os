"""Utility functions and constants for dashboard modules."""

from __future__ import annotations

import time
from datetime import datetime

# Constants used across dashboard modules
TIMESTAMP_KEY = "timestamp"
VALUE_KEY = "value"


def current_timestamp() -> float:
    """Return the current time as a UNIX timestamp."""
    return time.time()


def iso_timestamp() -> str:
    """Return the current time in ISO 8601 format."""
    return datetime.now().isoformat()
