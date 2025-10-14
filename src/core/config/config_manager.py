#!/usr/bin/env python3
"""
Configuration Manager - V2 Compliance Module
============================================

Unified configuration manager class.
Extracted from config_ssot.py for better modularity.

V2 Compliance: Single Responsibility Principle
SOLID Principles: Dependency Inversion Principle

Author: Agent-2 (Architecture & Design Specialist) - ROI 32.26 Task
Extracted from: Agent-7's config_ssot.py consolidation
Created: 2025-10-13
License: MIT
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .config_dataclasses import (
    AgentConfig,
    BrowserConfig,
    FilePatternConfig,
    ReportConfig,
    TestConfig,
    ThresholdConfig,
    TimeoutConfig,
)

logger = logging.getLogger(__name__)


class UnifiedConfigManager:
    """SINGLE SOURCE OF TRUTH for all configuration management."""

    def __init__(self):
        """Initialize the unified configuration manager."""
        self.logger = logging.getLogger(__name__)
        self._load_environment()

        # Initialize configuration sections
        self.timeouts = TimeoutConfig()
        self.agents = AgentConfig()
        self.browser = BrowserConfig()
        self.thresholds = ThresholdConfig()
        self.file_patterns = FilePatternConfig()
        self.tests = TestConfig()
        self.reports = ReportConfig()

        self.logger.info("✅ Unified Configuration SSOT initialized")

    def _load_environment(self) -> None:
        """Load environment variables from .env file."""
        workspace_root = Path(__file__).resolve().parents[3]
        env_path = workspace_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            self.logger.debug(f"Loaded environment from {env_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key with environment override."""
        # Check environment first
        env_value = os.getenv(key)
        if env_value is not None:
            return self._convert_type(env_value)

        # Check if key is in dataclass configs
        if hasattr(self.timeouts, key.lower()):
            return getattr(self.timeouts, key.lower())
        if hasattr(self.agents, key.lower()):
            return getattr(self.agents, key.lower())
        if hasattr(self.browser, key.lower()):
            return getattr(self.browser, key.lower())
        if hasattr(self.thresholds, key.lower()):
            return getattr(self.thresholds, key.lower())
        if hasattr(self.file_patterns, key.lower()):
            return getattr(self.file_patterns, key.lower())
        if hasattr(self.tests, key.lower()):
            return getattr(self.tests, key.lower())
        if hasattr(self.reports, key.lower()):
            return getattr(self.reports, key.lower())

        return default

    def _convert_type(self, value: str) -> Any:
        """Convert string environment values to appropriate types."""
        if value.isdigit():
            return int(value)
        if value.replace(".", "", 1).isdigit():
            return float(value)
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        return value

    def validate(self) -> list[str]:
        """Validate all configuration values."""
        errors = []

        # Validate agent config
        if self.agents.agent_count < 1:
            errors.append("agent_count must be positive")

        # Validate timeouts
        timeout_fields = ["scrape_timeout", "response_wait_timeout", "quality_check_interval"]
        for field in timeout_fields:
            value = getattr(self.timeouts, field)
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(f"{field} must be a positive number")

        # Validate thresholds
        if not (0 <= self.thresholds.coverage_threshold <= 100):
            errors.append("coverage_threshold must be between 0 and 100")

        return errors


# SINGLE GLOBAL INSTANCE - THE ONE TRUE CONFIG MANAGER
_config_manager = UnifiedConfigManager()

# Auto-validate on import
_validation_errors = _config_manager.validate()
if _validation_errors:
    logger.warning(f"Configuration validation issues: {_validation_errors}")
else:
    logger.info("✅ Configuration validation passed")


__all__ = ["UnifiedConfigManager", "_config_manager"]
