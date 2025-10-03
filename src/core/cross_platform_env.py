#!/usr/bin/env python3
"""
Cross-Platform Environment Utilities - Main Interface
====================================================

V2 Compliance: Refactored for ≤10 functions
Author: Agent-5 (Coordinator) - Refactored
License: MIT
"""

from .cross_platform_env_advanced import EnvironmentConfig
from .cross_platform_env_core import CrossPlatformEnvironment

# Global instance for easy access
env_manager = CrossPlatformEnvironment()


# Utility functions defined inline for V2 compliance
def get_platform_info():
    """Get platform information."""
    return env_manager.platform


def is_windows():
    """Check if running on Windows."""
    return env_manager.is_windows


def is_linux():
    """Check if running on Linux."""
    return env_manager.is_linux


def is_macos():
    """Check if running on macOS."""
    return env_manager.is_macos


def get_agent_config():
    """Get agent configuration."""
    return {"platform": env_manager.platform}


def get_development_config():
    """Get development configuration."""
    return {"python_version": env_manager.get_python_version()}


__all__ = [
    "CrossPlatformEnvironment",
    "EnvironmentConfig",
    "get_platform_info",
    "get_agent_config",
    "get_development_config",
    "is_windows",
    "is_linux",
    "is_macos",
]


# Convenience functions
def get_env_var(name: str, default: str | None = None) -> str | None:
    """Get environment variable with platform-specific handling."""
    return env_manager.get_env_var(name, default)


def set_env_var(name: str, value: str, overwrite: bool = True):
    """Set environment variable."""
    env_manager.set_env_var(name, value, overwrite)


def load_env_file(env_file):
    """Load environment variables from file."""
    config = EnvironmentConfig()
    return config.load_env_file(env_file)
