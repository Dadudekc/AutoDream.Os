#!/usr/bin/env python3
"""
UNIFIED CONFIGURATION CORE SYSTEM - SINGLE SOURCE OF TRUTH (SSOT)
===============================================================

This is the ONE AND ONLY configuration system for the entire Agent Cellphone V2 project.
Consolidates ALL configuration management into a single, unified system.

V2 Compliance: SSOT Implementation
SOLID Principles: Single Responsibility (One config system), Open-Closed (Extensible)

Author: Agent-1 (System Recovery Specialist) - Consolidation Champion
License: MIT
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# Configure logging
logger = logging.getLogger(__name__)


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
    metadata: dict[str, Any] = field(default_factory=dict)


class UnifiedConfigManager:
    """SINGLE SOURCE OF TRUTH for all configuration management."""

    def __init__(self):
        """Initialize the unified configuration manager."""
        self.configs: dict[str, ConfigValue] = {}
        self.logger = logging.getLogger(__name__)

        # Initialize with default configurations
        self._load_default_configs()

    def _load_default_configs(self):
        """Load default configuration values."""
        defaults = {
            # Agent Configuration
            "DEFAULT_MODE": "coordinated",
            "DEFAULT_COORDINATE_MODE": "swarm",
            "AGENT_COUNT": 8,
            "CAPTAIN_ID": "captain-1",
            # Timeout Configuration
            "SCRAPE_TIMEOUT": 30.0,
            "RESPONSE_WAIT_TIMEOUT": 120.0,
            "QUALITY_CHECK_INTERVAL": 30.0,
            "PERFORMANCE_CHECK_INTERVAL": 60.0,
            "HEALTH_CHECK_TIMEOUT": 10.0,
            # Quality Configuration
            "QUALITY_CHECK_INTERVAL": 30.0,
            "HISTORY_WINDOW": 100,
            "ALERT_THRESHOLD": 0.8,
            # Performance Configuration
            "PERFORMANCE_METRICS_INTERVAL": 60.0,
            "MEMORY_THRESHOLD": 80.0,
            "CPU_THRESHOLD": 70.0,
            # Messaging Configuration
            "MESSAGE_QUEUE_SIZE": 1000,
            "MESSAGE_TIMEOUT": 30.0,
            "MAX_RETRIES": 3,
            # Browser Configuration
            "BROWSER_TIMEOUT": 30.0,
            "PAGE_LOAD_TIMEOUT": 60.0,
            # FSM Configuration
            "FSM_STATE_TIMEOUT": 300.0,
            "FSM_TRANSITION_TIMEOUT": 30.0,
            # Vector Database Configuration
            "VECTOR_DIMENSION": 768,
            "VECTOR_SIMILARITY_THRESHOLD": 0.8,
            "VECTOR_INDEX_SIZE": 10000,
            # Logging Configuration
            "LOG_LEVEL": "INFO",
            "LOG_MAX_SIZE": 10485760,  # 10MB
            "LOG_BACKUP_COUNT": 5,
            # Testing Configuration
            "TEST_TIMEOUT": 300.0,
            "TEST_PARALLEL_WORKERS": 4,
            "COVERAGE_THRESHOLD": 85.0,
            # Swarm Configuration
            "SWARM_COORDINATION_TIMEOUT": 60.0,
            "SWARM_AGENT_TIMEOUT": 30.0,
            "SWARM_MAX_AGENTS": 8,
            # Security Configuration
            "ENCRYPTION_KEY_SIZE": 256,
            "TOKEN_EXPIRY": 3600,  # 1 hour
            "MAX_LOGIN_ATTEMPTS": 3,
        }

        for key, value in defaults.items():
            self.set(key, value, ConfigSource.DEFAULT)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        if key in self.configs:
            return self.configs[key].value

        # Check environment variables as fallback
        env_value = os.getenv(key)
        if env_value is not None:
            # Convert string values to appropriate types
            if env_value.isdigit():
                return int(env_value)
            elif env_value.replace(".", "", 1).isdigit():
                return float(env_value)
            elif env_value.lower() in ("true", "false"):
                return env_value.lower() == "true"
            return env_value

        return default

    def set(self, key: str, value: Any, source: ConfigSource = ConfigSource.DEFAULT) -> None:
        """Set configuration value."""
        self.configs[key] = ConfigValue(
            value=value, source=source, environment=ConfigEnvironment.DEVELOPMENT
        )
        self.logger.debug(f"Configuration set: {key} = {value} (source: {source.value})")

    def get_all_configs(self) -> dict[str, Any]:
        """Get all configuration values."""
        return {key: value.value for key, value in self.configs.items()}

    def get_config_metadata(self, key: str) -> ConfigValue | None:
        """Get configuration metadata."""
        return self.configs.get(key)

    def reload_configs(self) -> None:
        """Reload configuration from all sources."""
        self.logger.info("Reloading configuration from all sources")
        # In a production system, this would reload from files, databases, etc.
        self._load_default_configs()

    def validate_configs(self) -> list[str]:
        """Validate configuration values."""
        errors = []

        # Validate numeric ranges
        if not isinstance(self.get("AGENT_COUNT"), int) or self.get("AGENT_COUNT") < 1:
            errors.append("AGENT_COUNT must be a positive integer")

        if (
            not isinstance(self.get("MESSAGE_QUEUE_SIZE"), int)
            or self.get("MESSAGE_QUEUE_SIZE") < 1
        ):
            errors.append("MESSAGE_QUEUE_SIZE must be a positive integer")

        # Validate timeout ranges
        for timeout_key in ["SCRAPE_TIMEOUT", "RESPONSE_WAIT_TIMEOUT", "QUALITY_CHECK_INTERVAL"]:
            if not isinstance(self.get(timeout_key), (int, float)) or self.get(timeout_key) <= 0:
                errors.append(f"{timeout_key} must be a positive number")

        return errors


# SINGLE GLOBAL INSTANCE - THE ONE TRUE CONFIG MANAGER
config_manager = UnifiedConfigManager()


# PUBLIC API - Single point of access for all configuration
def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value from the SINGLE SOURCE OF TRUTH."""
    return config_manager.get(key, default)


def set_config(key: str, value: Any, source: ConfigSource = ConfigSource.DEFAULT) -> None:
    """Set configuration value in the SINGLE SOURCE OF TRUTH."""
    config_manager.set(key, value, source)


def reload_config() -> None:
    """Reload configuration from the SINGLE SOURCE OF TRUTH."""
    config_manager.reload_configs()


def validate_config() -> list[str]:
    """Validate configuration in the SINGLE SOURCE OF TRUTH."""
    return config_manager.validate_configs()


def get_all_config() -> dict[str, Any]:
    """Get all configuration values from the SINGLE SOURCE OF TRUTH."""
    return config_manager.get_all_configs()


# SPECIALIZED CONFIG GETTERS FOR BACKWARD COMPATIBILITY
def get_agent_config() -> AgentConfig:
    """Get agent-specific configuration."""
    from .unified_config import AgentConfig

    return AgentConfig(
        default_mode=get_config("DEFAULT_MODE"),
        coordinate_mode=get_config("DEFAULT_COORDINATE_MODE"),
        agent_count=get_config("AGENT_COUNT"),
        captain_id=get_config("CAPTAIN_ID"),
    )


def get_timeout_config() -> TimeoutConfig:
    """Get timeout configuration."""
    from .unified_config import TimeoutConfig

    return TimeoutConfig(
        scrape_timeout=get_config("SCRAPE_TIMEOUT"),
        response_wait_timeout=get_config("RESPONSE_WAIT_TIMEOUT"),
        quality_check_interval=get_config("QUALITY_CHECK_INTERVAL"),
        performance_check_interval=get_config("PERFORMANCE_METRICS_INTERVAL"),
        health_check_timeout=get_config("HEALTH_CHECK_TIMEOUT"),
    )


def get_threshold_config() -> ThresholdConfig:
    """Get threshold configuration."""
    from .unified_config import ThresholdConfig

    return ThresholdConfig(
        memory_threshold=get_config("MEMORY_THRESHOLD"),
        cpu_threshold=get_config("CPU_THRESHOLD"),
        alert_threshold=get_config("ALERT_THRESHOLD"),
    )


def get_test_config() -> TestConfig:
    """Get test configuration."""
    from .unified_config import TestConfig

    return TestConfig(
        test_timeout=get_config("TEST_TIMEOUT"),
        parallel_workers=get_config("TEST_PARALLEL_WORKERS"),
        coverage_threshold=get_config("COVERAGE_THRESHOLD"),
        history_window=get_config("HISTORY_WINDOW"),
    )


# CONFIGURATION VALIDATION
def validate_system_config() -> bool:
    """Validate the entire system configuration."""
    errors = validate_config()
    if errors:
        logger.error("Configuration validation errors:")
        for error in errors:
            logger.error(f"  - {error}")
        return False

    logger.info("✅ System configuration validation passed")
    return True


# INITIALIZATION
def initialize_config() -> None:
    """Initialize the configuration system."""
    logger.info("🔧 Initializing SINGLE SOURCE OF TRUTH Configuration System")
    logger.info("📊 Loading default configurations...")

    # Validate configuration on startup
    if validate_system_config():
        logger.info("✅ Configuration system ready - SSOT established")
    else:
        logger.error("❌ Configuration validation failed - check configuration")
        raise ValueError("Invalid configuration detected")


# Auto-initialize on import
try:
    initialize_config()
except Exception as e:
    logger.error(f"Failed to initialize configuration system: {e}")
    # Don't raise exception during import - allow system to continue with defaults
