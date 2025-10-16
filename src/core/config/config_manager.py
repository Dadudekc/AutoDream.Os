#!/usr/bin/env python3
"""
Configuration Manager - V2 Compliance Module
============================================

Unified configuration manager class - SINGLE SOURCE OF TRUTH (SSOT).
Consolidated from multiple ConfigManager implementations into one.

CONSOLIDATION HISTORY:
- Agent-7 (2025-10-12): Created initial config_ssot.py
- Agent-2 (2025-10-13): Modularized into config/ submodule (ROI 32.26)
- Agent-8 (2025-10-16): DUP-001 SSOT Consolidation - Enhanced with features from:
  * config_core.py (metadata tracking, environment handling)
  * core_configuration_manager.py (persistence, history tracking)
  * unified_config.py (dataclass-based configs)

V2 Compliance: Single Responsibility Principle, SSOT Implementation
SOLID Principles: Dependency Inversion Principle, Open-Closed Principle

Authors:
- Agent-2 (Architecture & Design Specialist) - Initial modularization
- Agent-8 (SSOT & System Integration Specialist) - DUP-001 Consolidation
Created: 2025-10-13
Enhanced: 2025-10-16
License: MIT
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
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
from .config_enums import ConfigEnvironment, ConfigSource

logger = logging.getLogger(__name__)


class UnifiedConfigManager:
    """SINGLE SOURCE OF TRUTH for all configuration management.

    Enhanced features from DUP-001 consolidation:
    - Metadata tracking (source, environment, timestamps)
    - Configuration history tracking
    - File persistence capabilities
    - Environment variable overrides
    - Comprehensive validation
    """

    def __init__(self):
        """Initialize the unified configuration manager."""
        self.logger = logging.getLogger(__name__)

        # Configuration metadata tracking (from config_core.py)
        self.config_metadata: dict[str, dict[str, Any]] = {}
        self.config_history: list[dict[str, Any]] = []
        self.environment = ConfigEnvironment.DEVELOPMENT

        # Load environment variables first
        self._load_environment()

        # Initialize configuration sections (dataclass-based)
        self.timeouts = TimeoutConfig()
        self.agents = AgentConfig()
        self.browser = BrowserConfig()
        self.thresholds = ThresholdConfig()
        self.file_patterns = FilePatternConfig()
        self.tests = TestConfig()
        self.reports = ReportConfig()

        # Track initialization
        self._record_event("initialization", {"timestamp": datetime.now().isoformat()})

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

    # ========================================================================
    # ENHANCED FEATURES FROM DUP-001 CONSOLIDATION
    # ========================================================================

    def set(self, key: str, value: Any, source: ConfigSource = ConfigSource.RUNTIME) -> None:
        """Set configuration value with metadata tracking (from config_core.py)."""
        self.config_metadata[key] = {
            "value": value,
            "source": source.value,
            "environment": self.environment.value,
            "last_updated": datetime.now().isoformat(),
        }
        self._record_event("config_set", {"key": key, "source": source.value})
        self.logger.debug(f"Configuration set: {key} = {value} (source: {source.value})")

    def get_all_configs(self) -> dict[str, Any]:
        """Get all configuration values as dict (from config_core.py)."""
        return {
            "timeouts": self.timeouts.__dict__,
            "agents": self.agents.__dict__,
            "browser": self.browser.__dict__,
            "thresholds": self.thresholds.__dict__,
            "file_patterns": self.file_patterns.__dict__,
            "tests": {
                "coverage_report_precision": self.tests.coverage_report_precision,
                "history_window": self.tests.history_window,
            },
            "reports": {
                k: str(v) if isinstance(v, Path) else v for k, v in self.reports.__dict__.items()
            },
        }

    def get_config_metadata(self, key: str) -> dict[str, Any] | None:
        """Get configuration metadata (from config_core.py)."""
        return self.config_metadata.get(key)

    def reload_configs(self) -> None:
        """Reload configuration from all sources (from config_core.py)."""
        self.logger.info("Reloading configuration from all sources")
        self._load_environment()
        self.timeouts = TimeoutConfig()
        self.agents = AgentConfig()
        self.browser = BrowserConfig()
        self.thresholds = ThresholdConfig()
        self.file_patterns = FilePatternConfig()
        self.tests = TestConfig()
        self.reports = ReportConfig()
        self._record_event("config_reload", {"timestamp": datetime.now().isoformat()})

    def get_config_history(self, hours: int = 24) -> list[dict[str, Any]]:
        """Get configuration history (from core_configuration_manager.py)."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)

        return [
            record
            for record in self.config_history
            if datetime.fromisoformat(record["timestamp"]).timestamp() >= cutoff_time
        ]

    def save_to_file(self, file_path: str | Path) -> None:
        """Save configuration to JSON file (from core_configuration_manager.py)."""
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        config_data = self.get_all_configs()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, default=str)

        self._record_event("config_saved", {"file_path": str(file_path)})
        self.logger.info(f"Configuration saved to {file_path}")

    def load_from_file(self, file_path: str | Path) -> None:
        """Load configuration from JSON file (from core_configuration_manager.py)."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, encoding="utf-8") as f:
            config_data = json.load(f)

        # Update configurations from loaded data
        for key, value in config_data.items():
            if hasattr(self, key) and isinstance(value, dict):
                for field, field_value in value.items():
                    if hasattr(getattr(self, key), field):
                        setattr(getattr(self, key), field, field_value)

        self._record_event("config_loaded", {"file_path": str(file_path)})
        self.logger.info(f"Configuration loaded from {file_path}")

    def get_status(self) -> dict[str, Any]:
        """Get configuration manager status (from core_configuration_manager.py)."""
        return {
            "environment": self.environment.value,
            "initialized": True,
            "config_sections": [
                "timeouts",
                "agents",
                "browser",
                "thresholds",
                "file_patterns",
                "tests",
                "reports",
            ],
            "metadata_count": len(self.config_metadata),
            "history_count": len(self.config_history),
            "validation_status": "passed" if not self.validate() else "has_errors",
        }

    def _record_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Record configuration event to history."""
        self.config_history.append(
            {"event_type": event_type, "timestamp": datetime.now().isoformat(), "data": data}
        )


# SINGLE GLOBAL INSTANCE - THE ONE TRUE CONFIG MANAGER
_config_manager = UnifiedConfigManager()

# Auto-validate on import
_validation_errors = _config_manager.validate()
if _validation_errors:
    logger.warning(f"Configuration validation issues: {_validation_errors}")
else:
    logger.info("✅ Configuration validation passed")


__all__ = ["UnifiedConfigManager", "_config_manager"]
