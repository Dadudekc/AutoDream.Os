"""Deprecated session backend wrappers."""
from __future__ import annotations

import warnings

from src.session_management.backends import (
    SessionBackend,
    MemorySessionBackend,
    SQLiteSessionBackend,
)

warnings.warn(
    "services_v2.auth.session_backend is deprecated; use src.session_management.backends instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "SessionBackend",
    "MemorySessionBackend",
    "SQLiteSessionBackend",
]
