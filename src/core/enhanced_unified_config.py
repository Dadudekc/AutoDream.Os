#!/usr/bin/env python3
"""
ENHANCED UNIFIED CONFIGURATION SYSTEM - SINGLE SOURCE OF TRUTH
==============================================================

This is the ONE AND ONLY configuration system for the entire Agent Cellphone V2 project.
Consolidates ALL configuration management into a single, enhanced unified system.

V2 Compliance: SSOT Implementation
SOLID Principles: Single Responsibility (One config system), Open-Closed (Extensible)

Author: Agent-5 (Business Intelligence & Coordination Specialist) - Configuration Consolidation
License: MIT
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

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
    description: str | None = None
    required: bool = False
    validation_rules: dict[str, Any] | None = None


@dataclass
class AgentConfig:
    """Agent-specific configuration."""
    agent_id: str
    coordinates: tuple | None = None
    capabilities: list[str] = field(default_factory=list)
    timeout_config: dict[str, float] = field(default_factory=dict)
    priority: int = 1
    active: bool = True


@dataclass
class SystemConfig:
    """System-wide configuration."""
    environment: ConfigEnvironment = ConfigEnvironment.DEVELOPMENT
    debug_mode: bool = False
    log_level: str = "INFO"
    max_retries: int = 3
    default_timeout: float = 30.0


# ============================================================================
# ENVIRONMENT LOADER
# ============================================================================

class EnvironmentLoader:
    """Loads and validates environment variables for unified configuration."""

    def __init__(self, env_file: Path | None = None):
        """Initialize environment loader."""
        self.env_file = env_file or Path(".env")
        self.logger = logging.getLogger(__name__)
        self._loaded_vars: dict[str, Any] = {}

    def load_env_file(self) -> bool:
        """Load environment variables from .env file if it exists."""
        if not self.env_file.exists():
            self.logger.warning(f"Environment file {self.env_file} not found")
            return False

        try:
            with open(self.env_file, encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Parse key=value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        self._loaded_vars[key] = value
                    else:
                        self.logger.warning(f"Invalid line {line_num} in {self.env_file}: {line}")

            self.logger.info(f"Loaded {len(self._loaded_vars)} variables from {self.env_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load environment file {self.env_file}: {e}")
            return False

    def get_env_var(self, key: str, default: Any = None, var_type: type = str) -> Any:
        """Get environment variable with type conversion."""
        # Check loaded vars first, then os.environ
        value = self._loaded_vars.get(key) or os.getenv(key, default)

        if value is None:
            return default

        try:
            if var_type == bool:
                return str(value).lower() in ('true', '1', 'yes', 'on')
            elif var_type == int:
                return int(value)
            elif var_type == float:
                return float(value)
            elif var_type == list:
                return [item.strip() for item in str(value).split(',')]
            else:
                return str(value)
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Failed to convert {key}={value} to {var_type.__name__}: {e}")
            return default


# ============================================================================
# ENHANCED UNIFIED CONFIGURATION SYSTEM
# ============================================================================

class EnhancedUnifiedConfig:
    """Enhanced unified configuration system consolidating all configuration management."""

    def __init__(self, env_file: Path | None = None):
        """Initialize enhanced unified configuration system."""
        self.env_loader = EnvironmentLoader(env_file)
        self.logger = logging.getLogger(__name__)
        self._config_cache: dict[str, ConfigValue] = {}
        self._agent_configs: dict[str, AgentConfig] = {}
        self._system_config = SystemConfig()

        # Load environment variables
        self.env_loader.load_env_file()

        # Initialize configuration
        self._initialize_configuration()

    def _initialize_configuration(self):
        """Initialize all configuration values."""
        # System configuration
        self._system_config.environment = ConfigEnvironment(
            self.env_loader.get_env_var("ENVIRONMENT", "development")
        )
        self._system_config.debug_mode = self.env_loader.get_env_var("DEBUG_MODE", False, bool)
        self._system_config.log_level = self.env_loader.get_env_var("LOG_LEVEL", "INFO")
        self._system_config.max_retries = self.env_loader.get_env_var("MAX_RETRIES", 3, int)
        self._system_config.default_timeout = self.env_loader.get_env_var("DEFAULT_TIMEOUT", 30.0, float)

        # Load agent configurations
        self._load_agent_configurations()

        # Load core configuration values
        self._load_core_configurations()

    def _load_agent_configurations(self):
        """Load agent-specific configurations."""
        # Load agent coordinates
        coords_file = Path("cursor_agent_coords.json")
        if coords_file.exists():
            try:
                import json
                with open(coords_file) as f:
                    coords_data = json.load(f)

                for agent_id, coords in coords_data.items():
                    self._agent_configs[agent_id] = AgentConfig(
                        agent_id=agent_id,
                        coordinates=tuple(coords) if coords else None,
                        capabilities=self.env_loader.get_env_var(f"{agent_id.upper()}_CAPABILITIES", [], list),
                        timeout_config=self._get_agent_timeout_config(agent_id),
                        priority=self.env_loader.get_env_var(f"{agent_id.upper()}_PRIORITY", 1, int),
                        active=self.env_loader.get_env_var(f"{agent_id.upper()}_ACTIVE", True, bool)
                    )
            except Exception as e:
                self.logger.error(f"Failed to load agent coordinates: {e}")

    def _get_agent_timeout_config(self, agent_id: str) -> dict[str, float]:
        """Get timeout configuration for specific agent."""
        return {
            "default": self.env_loader.get_env_var(f"{agent_id.upper()}_TIMEOUT", 30.0, float),
            "messaging": self.env_loader.get_env_var(f"{agent_id.upper()}_MESSAGING_TIMEOUT", 10.0, float),
            "processing": self.env_loader.get_env_var(f"{agent_id.upper()}_PROCESSING_TIMEOUT", 60.0, float),
            "coordination": self.env_loader.get_env_var(f"{agent_id.upper()}_COORDINATION_TIMEOUT", 15.0, float)
        }

    def _load_core_configurations(self):
        """Load core configuration values."""
        # Timeout configurations
        timeout_configs = {
            "SCRAPE_TIMEOUT": (30.0, "Browser/UI scraping timeout"),
            "RESPONSE_WAIT_TIMEOUT": (120.0, "Response wait timeout"),
            "QUALITY_CHECK_INTERVAL": (30.0, "Quality monitoring interval"),
            "METRICS_COLLECTION_INTERVAL": (60.0, "Metrics collection interval"),
            "SMOKE_TEST_TIMEOUT": (60, "Smoke test timeout"),
            "UNIT_TEST_TIMEOUT": (120, "Unit test timeout"),
            "INTEGRATION_TEST_TIMEOUT": (300, "Integration test timeout"),
            "PERFORMANCE_TEST_TIMEOUT": (600, "Performance test timeout"),
            "SECURITY_TEST_TIMEOUT": (180, "Security test timeout"),
            "API_TEST_TIMEOUT": (240, "API test timeout"),
            "COORDINATION_TEST_TIMEOUT": (180, "Coordination test timeout"),
            "LEARNING_TEST_TIMEOUT": (180, "Learning test timeout")
        }

        for key, (default, description) in timeout_configs.items():
            value = self.env_loader.get_env_var(key, default, float if isinstance(default, float) else int)
            self._config_cache[key] = ConfigValue(
                value=value,
                source=ConfigSource.ENVIRONMENT if key in os.environ else ConfigSource.DEFAULT,
                environment=self._system_config.environment,
                description=description,
                required=False
            )

        # PyAutoGUI configurations
        pyautogui_configs = {
            "ENABLE_PYAUTOGUI": (True, "Enable PyAutoGUI functionality"),
            "PYAUTO_PAUSE_S": (0.05, "PyAutoGUI pause duration"),
            "PYAUTO_MOVE_DURATION": (0.4, "PyAutoGUI move duration"),
            "PYAUTO_SEND_RETRIES": (2, "PyAutoGUI send retries"),
            "PYAUTO_RETRY_SLEEP_S": (0.3, "PyAutoGUI retry sleep duration")
        }

        for key, (default, description) in pyautogui_configs.items():
            value = self.env_loader.get_env_var(key, default, bool if isinstance(default, bool) else float)
            self._config_cache[key] = ConfigValue(
                value=value,
                source=ConfigSource.ENVIRONMENT if key in os.environ else ConfigSource.DEFAULT,
                environment=self._system_config.environment,
                description=description,
                required=False
            )

        # Messaging configurations
        messaging_configs = {
            "MESSAGING_RETRY_ATTEMPTS": (3, "Messaging retry attempts"),
            "MESSAGING_TIMEOUT": (30.0, "Messaging timeout"),
            "BROADCAST_DELAY": (0.5, "Broadcast delay between agents"),
            "MESSAGE_QUEUE_SIZE": (1000, "Message queue size limit")
        }

        for key, (default, description) in messaging_configs.items():
            value = self.env_loader.get_env_var(key, default, int if isinstance(default, int) else float)
            self._config_cache[key] = ConfigValue(
                value=value,
                source=ConfigSource.ENVIRONMENT if key in os.environ else ConfigSource.DEFAULT,
                environment=self._system_config.environment,
                description=description,
                required=False
            )

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        if key in self._config_cache:
            return self._config_cache[key].value
        return default

    def get_agent_config(self, agent_id: str) -> AgentConfig | None:
        """Get agent-specific configuration."""
        return self._agent_configs.get(agent_id)

    def get_system_config(self) -> SystemConfig:
        """Get system configuration."""
        return self._system_config

    def get_timeout_config(self) -> dict[str, Any]:
        """Get timeout configuration."""
        return {key: config.value for key, config in self._config_cache.items()
                if "TIMEOUT" in key or "INTERVAL" in key}

    def get_threshold_config(self) -> dict[str, Any]:
        """Get threshold configuration."""
        threshold_configs = {
            "MIN_SUCCESS_RATE": self.env_loader.get_env_var("MIN_SUCCESS_RATE", 0.85, float),
            "MAX_ERROR_RATE": self.env_loader.get_env_var("MAX_ERROR_RATE", 0.15, float),
            "PERFORMANCE_THRESHOLD": self.env_loader.get_env_var("PERFORMANCE_THRESHOLD", 0.8, float),
            "QUALITY_THRESHOLD": self.env_loader.get_env_var("QUALITY_THRESHOLD", 0.9, float)
        }
        return threshold_configs

    def get_test_config(self) -> dict[str, Any]:
        """Get test configuration."""
        return {key: config.value for key, config in self._config_cache.items()
                if "TEST" in key}

    def set_config(self, key: str, value: Any, source: ConfigSource = ConfigSource.RUNTIME) -> None:
        """Set configuration value at runtime."""
        self._config_cache[key] = ConfigValue(
            value=value,
            source=source,
            environment=self._system_config.environment,
            description=f"Runtime configuration for {key}"
        )

    def validate_configuration(self) -> dict[str, list[str]]:
        """Validate all configuration values."""
        validation_errors = {}

        for key, config in self._config_cache.items():
            if config.required and config.value is None:
                validation_errors.setdefault(key, []).append("Required configuration is missing")

            if config.validation_rules:
                # Add validation logic here based on rules
                pass

        return validation_errors

    def export_configuration(self, filepath: str) -> bool:
        """Export configuration to file."""
        try:
            config_data = {
                "system_config": {
                    "environment": self._system_config.environment.value,
                    "debug_mode": self._system_config.debug_mode,
                    "log_level": self._system_config.log_level,
                    "max_retries": self._system_config.max_retries,
                    "default_timeout": self._system_config.default_timeout
                },
                "agent_configs": {
                    agent_id: {
                        "agent_id": config.agent_id,
                        "coordinates": config.coordinates,
                        "capabilities": config.capabilities,
                        "timeout_config": config.timeout_config,
                        "priority": config.priority,
                        "active": config.active
                    } for agent_id, config in self._agent_configs.items()
                },
                "config_values": {
                    key: {
                        "value": config.value,
                        "source": config.source.value,
                        "environment": config.environment.value,
                        "description": config.description,
                        "required": config.required
                    } for key, config in self._config_cache.items()
                },
                "export_timestamp": str(datetime.now())
            }

            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, default=str)

            self.logger.info(f"Configuration exported to: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export configuration: {e}")
            return False


# ============================================================================
# SINGLE GLOBAL INSTANCE - THE ONE TRUE CONFIGURATION SYSTEM
# ============================================================================

enhanced_config = EnhancedUnifiedConfig()


# ============================================================================
# PUBLIC API - Single point of access for all configuration
# ============================================================================

def get_enhanced_config() -> EnhancedUnifiedConfig:
    """Get the SINGLE SOURCE OF TRUTH enhanced configuration system."""
    return enhanced_config


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.get_config(key, default)


def get_agent_config(agent_id: str) -> AgentConfig | None:
    """Get agent configuration using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.get_agent_config(agent_id)


def get_system_config() -> SystemConfig:
    """Get system configuration using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.get_system_config()


def get_timeout_config() -> dict[str, Any]:
    """Get timeout configuration using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.get_timeout_config()


def get_threshold_config() -> dict[str, Any]:
    """Get threshold configuration using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.get_threshold_config()


def get_test_config() -> dict[str, Any]:
    """Get test configuration using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.get_test_config()


def set_config(key: str, value: Any) -> None:
    """Set configuration value using the SINGLE SOURCE OF TRUTH."""
    enhanced_config.set_config(key, value)


def validate_configuration() -> dict[str, list[str]]:
    """Validate configuration using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.validate_configuration()


def export_configuration(filepath: str) -> bool:
    """Export configuration using the SINGLE SOURCE OF TRUTH."""
    return enhanced_config.export_configuration(filepath)


# ============================================================================
# LEGACY COMPATIBILITY FUNCTIONS
# ============================================================================

def get_config_logger():
    """Legacy compatibility function."""
    return logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION MODELS EXPORTS - Single source for all configuration models
# ============================================================================

__all__ = [
    # Core classes
    "EnhancedUnifiedConfig",
    "EnvironmentLoader",
    "AgentConfig",
    "SystemConfig",
    "ConfigValue",

    # Enums
    "ConfigEnvironment",
    "ConfigSource",

    # Public API functions
    "get_enhanced_config",
    "get_config",
    "get_agent_config",
    "get_system_config",
    "get_timeout_config",
    "get_threshold_config",
    "get_test_config",
    "set_config",
    "validate_configuration",
    "export_configuration",

    # Legacy compatibility
    "get_config_logger",
]


# ============================================================================
# VALIDATION AND HEALTH CHECKS
# ============================================================================

def validate_enhanced_config_system() -> bool:
    """Validate the enhanced configuration system is properly configured."""
    try:
        config = get_enhanced_config()
        if not config:
            logger.error("Enhanced configuration system not available")
            return False

        # Test basic functionality
        test_value = config.get_config("TEST_CONFIG", "default")
        if test_value != "default":
            logger.error("Configuration system test failed")
            return False

        logger.info("✅ Enhanced configuration system validation passed")
        return True

    except Exception as e:
        logger.error(f"❌ Enhanced configuration system validation failed: {e}")
        return False


def initialize_enhanced_config_system() -> None:
    """Initialize the enhanced configuration system."""
    logger.info("🔧 Initializing SINGLE SOURCE OF TRUTH Enhanced Configuration System")

    if validate_enhanced_config_system():
        logger.info("✅ Enhanced configuration system ready - SSOT established")
    else:
        logger.error("❌ Enhanced configuration system initialization failed")
        raise ValueError("Invalid enhanced configuration system configuration")


# Initialize on import
try:
    initialize_enhanced_config_system()
except Exception as e:
    logger.error(f"Failed to initialize enhanced configuration system: {e}")
    # Don't raise exception during import - allow system to continue
