"""Compatibility utilities for configuration loading.

This module provides a thin wrapper around the project-wide single source of
truth for configuration loading located at ``src.core.config_loader``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Union

from src.core.config_loader import load_config as _load_config


class ConfigLoader:
    """Backward-compatible wrapper for the core ``load_config`` function."""

    @staticmethod
    def load(path: Union[str, Path], defaults: Dict[str, Any]) -> Dict[str, Any]:
        return _load_config(path, defaults)
