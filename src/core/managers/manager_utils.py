#!/usr/bin/env python3
"""Shared configuration and utility helpers for manager modules."""

from datetime import datetime
from pathlib import Path


def current_timestamp() -> str:
    """Return the current time in ISO 8601 format."""
    return datetime.now().isoformat()


def ensure_directory(path: str) -> Path:
    """Ensure that *path* exists and return it as a :class:`Path`."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
