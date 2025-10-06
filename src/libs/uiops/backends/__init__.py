"""
UI Ops Backends
===============

Backend implementations for UI operations.
"""

from .noop import NoOpBackend
from .pyauto import PyAutoGUIBackend

__all__ = ["NoOpBackend", "PyAutoGUIBackend"]

