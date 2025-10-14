#!/usr/bin/env python3
"""
Configuration Accessors - V2 Compliance Module
==============================================

Accessor functions for unified configuration system.
Extracted from config_ssot.py for better modularity.

V2 Compliance: Single Responsibility Principle
SOLID Principles: Dependency Inversion Principle

Author: Agent-2 (Architecture & Design Specialist) - ROI 32.26 Task
Extracted from: Agent-7's config_ssot.py consolidation
Created: 2025-10-13
License: MIT
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .config_dataclasses import (
        AgentConfig,
        BrowserConfig,
        FilePatternConfig,
        ReportConfig,
        TestConfig,
        ThresholdConfig,
        TimeoutConfig,
    )
    from .config_manager import UnifiedConfigManager


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value from SINGLE SOURCE OF TRUTH."""
    from .config_manager import _config_manager

    return _config_manager.get(key, default)


def get_unified_config() -> "UnifiedConfigManager":
    """Get the global unified configuration manager."""
    from .config_manager import _config_manager

    return _config_manager


def get_timeout_config() -> "TimeoutConfig":
    """Get timeout configuration."""
    from .config_manager import _config_manager

    return _config_manager.timeouts


def get_agent_config() -> "AgentConfig":
    """Get agent configuration."""
    from .config_manager import _config_manager

    return _config_manager.agents


def get_browser_config() -> "BrowserConfig":
    """Get browser configuration."""
    from .config_manager import _config_manager

    return _config_manager.browser


def get_threshold_config() -> "ThresholdConfig":
    """Get threshold configuration."""
    from .config_manager import _config_manager

    return _config_manager.thresholds


def get_file_pattern_config() -> "FilePatternConfig":
    """Get file pattern configuration."""
    from .config_manager import _config_manager

    return _config_manager.file_patterns


def get_test_config() -> "TestConfig":
    """Get test configuration."""
    from .config_manager import _config_manager

    return _config_manager.tests


def get_report_config() -> "ReportConfig":
    """Get report configuration."""
    from .config_manager import _config_manager

    return _config_manager.reports


def validate_config() -> list[str]:
    """Validate all configuration."""
    from .config_manager import _config_manager

    return _config_manager.validate()


def reload_config() -> None:
    """Reload configuration from environment."""
    from . import config_manager

    config_manager._config_manager = config_manager.UnifiedConfigManager()


__all__ = [
    "get_config",
    "get_unified_config",
    "get_timeout_config",
    "get_agent_config",
    "get_browser_config",
    "get_threshold_config",
    "get_file_pattern_config",
    "get_test_config",
    "get_report_config",
    "validate_config",
    "reload_config",
]
