#!/usr/bin/env python3
"""
Unified Configuration System - V2 Compliant Core Module
Consolidates constants, FSM, and SSOT configuration modules
V2 Compliance: < 400 lines, single responsibility for all core configuration operations.
Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ConfigurationType(Enum):
    SYSTEM = "system"
    AGENT = "agent"
    MESSAGING = "messaging"
    ANALYTICS = "analytics"
    PERFORMANCE = "performance"
    FSM = "fsm"


class FSMState(Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    TERMINATED = "terminated"


class FSMTransition(Enum):
    INITIALIZE = "initialize"
    ACTIVATE = "activate"
    PAUSE = "pause"
    RESUME = "resume"
    ERROR = "error"
    TERMINATE = "terminate"


@dataclass
class ConfigurationItem:
    key: str
    value: Any
    config_type: ConfigurationType
    description: str = ""
    required: bool = False
    default_value: Any = None
    validation_rules: list[str] = None

    def __post_init__(self):
        if self.validation_rules is None:
            self.validation_rules = []


@dataclass
class FSMConfiguration:
    state: FSMState
    transitions: dict[FSMTransition, FSMState]
    initial_state: FSMState = FSMState.UNINITIALIZED
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ConfigurationValidator(ABC):
    @abstractmethod
    def validate(self, config_item: ConfigurationItem) -> bool:
        pass

    @abstractmethod
    def get_validator_type(self) -> str:
        pass


class StandardValidator(ConfigurationValidator):
    def validate(self, config_item: ConfigurationItem) -> bool:
        try:
            # Check required fields
            if config_item.required and config_item.value is None:
                logger.error(f"Required configuration {config_item.key} is missing")
                return False

            # Check value type based on key patterns
            if config_item.key.endswith("_timeout") and not isinstance(
                config_item.value, (int, float)
            ):
                logger.error(f"Timeout configuration {config_item.key} must be numeric")
                return False

            if config_item.key.endswith("_enabled") and not isinstance(config_item.value, bool):
                logger.error(f"Boolean configuration {config_item.key} must be boolean")
                return False

            if config_item.key.endswith("_path") and not isinstance(config_item.value, str):
                logger.error(f"Path configuration {config_item.key} must be string")
                return False

            # Check value ranges
            if isinstance(config_item.value, (int, float)):
                if config_item.key.endswith("_timeout") and config_item.value < 0:
                    logger.error(f"Timeout configuration {config_item.key} must be positive")
                    return False

            logger.debug(f"Configuration {config_item.key} validated successfully")
            return True

        except Exception as e:
            logger.error(f"Validation error for {config_item.key}: {e}")
            return False

    def get_validator_type(self) -> str:
        return "standard"


class StrictValidator(ConfigurationValidator):
    def validate(self, config_item: ConfigurationItem) -> bool:
        try:
            # First run standard validation
            if not StandardValidator().validate(config_item):
                return False

            # Additional strict validations
            if config_item.key.endswith("_timeout") and config_item.value > 3600:  # 1 hour max
                logger.error(f"Timeout configuration {config_item.key} exceeds maximum (3600s)")
                return False

            if config_item.key.endswith("_retries") and config_item.value > 10:
                logger.error(f"Retry configuration {config_item.key} exceeds maximum (10)")
                return False

            # Check for sensitive data
            sensitive_keys = ["password", "secret", "key", "token"]
            if any(sensitive in config_item.key.lower() for sensitive in sensitive_keys):
                if not isinstance(config_item.value, str) or len(config_item.value) < 8:
                    logger.error(f"Sensitive configuration {config_item.key} must be secure string")
                    return False

            logger.debug(f"Configuration {config_item.key} passed strict validation")
            return True

        except Exception as e:
            logger.error(f"Strict validation error for {config_item.key}: {e}")
            return False

    def get_validator_type(self) -> str:
        return "strict"


class ConfigurationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.configurations: dict[str, ConfigurationItem] = {}
        self.validators: dict[str, ConfigurationValidator] = {
            "standard": StandardValidator(),
            "strict": StrictValidator(),
        }
        self.fsm_configs: dict[str, FSMConfiguration] = {}
        self.config_updates = 0

    def add_configuration(
        self, config_item: ConfigurationItem, validator_type: str = "standard"
    ) -> bool:
        try:
            # Validate configuration
            validator = self.validators.get(validator_type)
            if validator and not validator.validate(config_item):
                return False

            # Add to configurations
            self.configurations[config_item.key] = config_item
            self.config_updates += 1

            self.logger.info(f"Added configuration {config_item.key}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding configuration {config_item.key}: {e}")
            return False

    def get_configuration(self, key: str) -> ConfigurationItem | None:
        return self.configurations.get(key)

    def get_configuration_value(self, key: str, default: Any = None) -> Any:
        config_item = self.get_configuration(key)
        if config_item:
            return config_item.value
        return default

    def update_configuration(self, key: str, value: Any, validator_type: str = "standard") -> bool:
        try:
            config_item = self.get_configuration(key)
            if not config_item:
                self.logger.error(f"Configuration {key} not found")
                return False

            # Create updated configuration item
            updated_item = ConfigurationItem(
                key=config_item.key,
                value=value,
                config_type=config_item.config_type,
                description=config_item.description,
                required=config_item.required,
                default_value=config_item.default_value,
                validation_rules=config_item.validation_rules,
            )

            # Validate updated configuration
            validator = self.validators.get(validator_type)
            if validator and not validator.validate(updated_item):
                return False

            # Update configuration
            self.configurations[key] = updated_item
            self.config_updates += 1

            self.logger.info(f"Updated configuration {key}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating configuration {key}: {e}")
            return False

    def add_fsm_configuration(self, name: str, fsm_config: FSMConfiguration) -> bool:
        try:
            self.fsm_configs[name] = fsm_config
            self.logger.info(f"Added FSM configuration {name}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding FSM configuration {name}: {e}")
            return False

    def get_fsm_configuration(self, name: str) -> FSMConfiguration | None:
        return self.fsm_configs.get(name)

    def load_environment_configurations(self) -> int:
        """Load configurations from environment variables."""
        try:
            loaded_count = 0

            # Common environment variables
            env_mappings = {
                "ENABLE_PYAUTOGUI": (
                    "messaging.pyautogui_enabled",
                    ConfigurationType.MESSAGING,
                    bool,
                ),
                "PYAUTO_PAUSE_S": ("messaging.pyautogui_pause", ConfigurationType.MESSAGING, float),
                "PYAUTO_SEND_RETRIES": ("messaging.send_retries", ConfigurationType.MESSAGING, int),
                "ANALYTICS_CACHE_SIZE": ("analytics.cache_size", ConfigurationType.ANALYTICS, int),
                "PERFORMANCE_MONITORING": (
                    "performance.monitoring_enabled",
                    ConfigurationType.PERFORMANCE,
                    bool,
                ),
            }

            for env_var, (config_key, config_type, value_type) in env_mappings.items():
                env_value = os.getenv(env_var)
                if env_value is not None:
                    try:
                        # Convert value type
                        if value_type == bool:
                            converted_value = env_value.lower() in ("true", "1", "yes", "on")
                        elif value_type == int:
                            converted_value = int(env_value)
                        elif value_type == float:
                            converted_value = float(env_value)
                        else:
                            converted_value = env_value

                        # Create configuration item
                        config_item = ConfigurationItem(
                            key=config_key,
                            value=converted_value,
                            config_type=config_type,
                            description=f"Loaded from environment variable {env_var}",
                            required=False,
                        )

                        # Add configuration
                        if self.add_configuration(config_item):
                            loaded_count += 1

                    except ValueError as e:
                        self.logger.warning(f"Invalid value for {env_var}: {env_value} ({e})")

            self.logger.info(f"Loaded {loaded_count} configurations from environment")
            return loaded_count

        except Exception as e:
            self.logger.error(f"Error loading environment configurations: {e}")
            return 0

    def get_configuration_statistics(self) -> dict[str, Any]:
        """Get configuration system statistics."""
        config_by_type = {}
        for config_item in self.configurations.values():
            config_type = config_item.config_type.value
            if config_type not in config_by_type:
                config_by_type[config_type] = 0
            config_by_type[config_type] += 1

        return {
            "total_configurations": len(self.configurations),
            "configurations_by_type": config_by_type,
            "fsm_configurations": len(self.fsm_configs),
            "config_updates": self.config_updates,
            "validators": list(self.validators.keys()),
        }


class UnifiedConfigurationSystem:
    """Unified configuration system combining all configuration functionality."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_manager = ConfigurationManager()
        self.initialized = False
        self.initialization_time = 0.0

    def initialize(self) -> bool:
        """Initialize the configuration system."""
        try:
            start_time = time.time()

            # Load environment configurations
            env_loaded = self.config_manager.load_environment_configurations()

            # Add default configurations
            default_configs = [
                ConfigurationItem(
                    key="system.name",
                    value="Agent Swarm System",
                    config_type=ConfigurationType.SYSTEM,
                    description="System name",
                    required=True,
                ),
                ConfigurationItem(
                    key="system.version",
                    value="2.0.0",
                    config_type=ConfigurationType.SYSTEM,
                    description="System version",
                    required=True,
                ),
                ConfigurationItem(
                    key="messaging.default_timeout",
                    value=30.0,
                    config_type=ConfigurationType.MESSAGING,
                    description="Default message timeout in seconds",
                    required=False,
                ),
                ConfigurationItem(
                    key="analytics.default_cache_size",
                    value=1000,
                    config_type=ConfigurationType.ANALYTICS,
                    description="Default analytics cache size",
                    required=False,
                ),
            ]

            for config in default_configs:
                self.config_manager.add_configuration(config)

            # Add default FSM configuration
            default_fsm = FSMConfiguration(
                state=FSMState.UNINITIALIZED,
                transitions={
                    FSMTransition.INITIALIZE: FSMState.INITIALIZING,
                    FSMTransition.ACTIVATE: FSMState.ACTIVE,
                    FSMTransition.PAUSE: FSMState.PAUSED,
                    FSMTransition.RESUME: FSMState.ACTIVE,
                    FSMTransition.ERROR: FSMState.ERROR,
                    FSMTransition.TERMINATE: FSMState.TERMINATED,
                },
                initial_state=FSMState.UNINITIALIZED,
            )
            self.config_manager.add_fsm_configuration("default", default_fsm)

            self.initialization_time = time.time() - start_time
            self.initialized = True

            self.logger.info(f"Configuration system initialized in {self.initialization_time:.3f}s")
            return True

        except Exception as e:
            self.logger.error(f"Error initializing configuration system: {e}")
            return False

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config_manager.get_configuration_value(key, default)

    def set_config(
        self, key: str, value: Any, config_type: ConfigurationType = ConfigurationType.SYSTEM
    ) -> bool:
        """Set configuration value."""
        config_item = ConfigurationItem(
            key=key, value=value, config_type=config_type, description="User-defined configuration"
        )
        return self.config_manager.add_configuration(config_item)

    def get_system_statistics(self) -> dict[str, Any]:
        """Get system statistics."""
        config_stats = self.config_manager.get_configuration_statistics()

        return {
            "initialized": self.initialized,
            "initialization_time": self.initialization_time,
            "configuration_manager": config_stats,
        }


# Export main classes
__all__ = [
    "UnifiedConfigurationSystem",
    "ConfigurationManager",
    "ConfigurationItem",
    "FSMConfiguration",
    "ConfigurationType",
    "FSMState",
    "FSMTransition",
    "StandardValidator",
    "StrictValidator",
]
