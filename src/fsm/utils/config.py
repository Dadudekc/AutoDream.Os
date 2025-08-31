"""Compatibility wrapper for FSM configuration utilities.

This module preserves the previous import path while delegating to the
centralized configuration implementation in :mod:`utils.config_core`.
"""

from utils.config_core import FSMConfig

__all__ = ["FSMConfig"]
