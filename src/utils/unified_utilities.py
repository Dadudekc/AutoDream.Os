#!/usr/bin/env python3
"""
Unified Utilities - V2 Compliant Module
======================================

Centralized utilities for the Agent Cellphone V2 system.
Provides unified access to common utilities and functions.

V2 Compliance: < 300 lines, single responsibility.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from pathlib import Path


class UnifiedUtility:
    """Unified utility class providing common functionality."""

    def __init__(self):
        """Initialize unified utility."""
        self.path = Path
        self.logger = logging.getLogger(__name__)

    def join_paths(self, *paths):
        """Join paths using pathlib."""
        return Path(*paths)

    def get_project_root(self) -> Path:
        """Get the project root directory."""
        current_file = Path(__file__).resolve()
        # Navigate up to find the project root (where pyproject.toml is)
        for parent in current_file.parents:
            if (parent / "pyproject.toml").exists():
                return parent
        return current_file.parent

    def get_config_path(self, config_name: str) -> Path:
        """Get path to a configuration file."""
        return self.get_project_root() / "config" / config_name

    def ensure_directory(self, path: Path) -> None:
        """Ensure directory exists."""
        path.mkdir(parents=True, exist_ok=True)


# Global instance
_unified_utility = None


def get_unified_utility() -> UnifiedUtility:
    """Get the global unified utility instance."""
    global _unified_utility
    if _unified_utility is None:
        _unified_utility = UnifiedUtility()
    return _unified_utility


def get_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """Get a configured logger with the given name.

    Args:
        name: Logger name
        log_level: Logging level

    Returns:
        Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    return logger


# Convenience functions for backward compatibility
def get_project_root() -> Path:
    """Get the project root directory."""
    return get_unified_utility().get_project_root()


def get_config_path(config_name: str) -> Path:
    """Get path to a configuration file."""
    return get_unified_utility().get_config_path(config_name)


def ensure_directory(path: Path) -> None:
    """Ensure directory exists."""
    get_unified_utility().ensure_directory(path)
