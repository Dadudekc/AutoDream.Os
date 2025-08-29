"""Deprecated session manager.

Use :mod:`src.session_management.session_manager` instead."""

from __future__ import annotations

import warnings

from src.session_management.session_manager import SessionManager

warnings.warn(
    "src.security.session_manager is deprecated; use src.session_management.session_manager instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["SessionManager"]
