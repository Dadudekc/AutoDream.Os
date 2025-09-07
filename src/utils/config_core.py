#!/usr/bin/env python3
"""
Centralized Configuration Core System
====================================

This module provides the Single Source of Truth (SSOT) for all configuration
management across the system.

Agent: Agent-2 (Architecture & Design Specialist)
Mission: Configuration Pattern Consolidation
Status: SSOT Implementation - Configuration Core System
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass, field


class ConfigEnvironment(str, Enum):
    """Configuration environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    STAGING = "staging"


class ConfigSource(str, Enum):
    """Configuration source types."""
    ENVIRONMENT = "environment"
    FILE = "file"
    DEFAULT = "default"
    RUNTIME = "runtime"


@dataclass
class ConfigValue:
    """Configuration value with metadata."""
    value: Any
    source: ConfigSource
    environment: ConfigEnvironment
    last_updated: str = field(default_factory=lambda: str(Path(__file__).stat().st_mtime))
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConfigManager:
    """Centralized configuration manager."""

    def __init__(self):
        """Initialize configuration manager."""
        self.configs: Dict[str, ConfigValue] = {}
        self.logger = logging.getLogger(__name__)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        if key in self.configs:
            return self.configs[key].value
        return default

    def set(self, key: str, value: Any, source: ConfigSource = ConfigSource.DEFAULT) -> None:
        """Set configuration value."""
        self.configs[key] = ConfigValue(
            value=value,
            source=source,
            environment=ConfigEnvironment.DEVELOPMENT
        )


# Global configuration manager instance
config_manager = ConfigManager()


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value from global manager."""
    return config_manager.get(key, default)


def set_config(key: str, value: Any, source: ConfigSource = ConfigSource.DEFAULT) -> None:
    """Set configuration value in global manager."""
    config_manager.set(key, value, source)