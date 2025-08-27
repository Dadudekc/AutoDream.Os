"""Deprecated session store.

Use backends from :mod:`src.session_management.backends` directly."""
from __future__ import annotations

import warnings

from src.session_management.backends import (
    MemorySessionBackend,
    SQLiteSessionBackend,
    SessionBackend,
)

warnings.warn(
    "services_v2.auth.session_store is deprecated; use src.session_management.backends instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "MemorySessionBackend",
    "SQLiteSessionBackend",
    "SessionBackend",
]
