"""Deprecated wrapper for unified session manager."""
from __future__ import annotations

import warnings

from src.session_management.session_manager import SessionManager

warnings.warn(
    "services_v2.auth.session_manager is deprecated; use src.session_management.session_manager instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["SessionManager"]
