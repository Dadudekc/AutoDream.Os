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

<<<<<<< HEAD

import logging
=======
from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass, field
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65


class ConfigEnvironment(str, Enum):
    """Configuration environment types."""
<<<<<<< HEAD

=======
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    STAGING = "staging"


class ConfigSource(str, Enum):
    """Configuration source types."""
<<<<<<< HEAD

=======
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    ENVIRONMENT = "environment"
    FILE = "file"
    DEFAULT = "default"
    RUNTIME = "runtime"


@dataclass
class ConfigValue:
    """Configuration value with metadata."""
<<<<<<< HEAD

=======
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    value: Any
    source: ConfigSource
    description: str = ""
    required: bool = False
    validation_rules: Optional[Dict[str, Any]] = None


class ConfigurationManager:
    """Centralized configuration manager implementing SSOT principles."""
<<<<<<< HEAD

    def __init__(self):
        self._config: Dict[str, ConfigValue] = {}
        self._environment = ConfigEnvironment(
            get_unified_config().get_env("ENVIRONMENT", "development")
        )
        self._initialized = False

=======
    
    def __init__(self):
        self._config: Dict[str, ConfigValue] = {}
        self._environment = ConfigEnvironment(os.getenv("ENVIRONMENT", "development"))
        self._initialized = False
        
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    def initialize(self) -> None:
        """Initialize the configuration system."""
        if self._initialized:
            return
<<<<<<< HEAD

=======
            
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
        # Load core configuration
        self._load_core_config()
        self._load_environment_config()
        self._load_application_config()
<<<<<<< HEAD

        self._initialized = True

    def _load_core_config(self) -> None:
        """Load core system configuration."""
        # Logging configuration
        self.set_config(
            "LOG_LEVEL",
            get_unified_validator().safe_getattr(
                logging,
                get_unified_config().get_env("LOG_LEVEL", "INFO").upper(),
                logging.INFO,
            ),
            ConfigSource.ENVIRONMENT,
            "Global logging level for the application",
        )

        # Environment configuration
        self.set_config(
            "ENVIRONMENT",
            self._environment.value,
            ConfigSource.ENVIRONMENT,
            "Current environment (development/testing/production)",
        )

        # Path configuration
        root_dir = Path(__file__).resolve().parents[2]
        self.set_config(
            "ROOT_DIR",
            root_dir,
            ConfigSource.DEFAULT,
            "Root directory of the application",
        )

        # Agent configuration
        self.set_config(
            "AGENT_COUNT", 8, ConfigSource.DEFAULT, "Number of agents in the system"
        )
        self.set_config(
            "CAPTAIN_ID", "Agent-4", ConfigSource.DEFAULT, "Captain agent identifier"
        )

    def _load_environment_config(self) -> None:
        """Load environment-specific configuration."""
        if self._environment == ConfigEnvironment.DEVELOPMENT:
            self.set_config(
                "DEBUG",
                True,
                ConfigSource.ENVIRONMENT,
                "Debug mode enabled for development",
            )
            self.set_config(
                "LOG_LEVEL",
                logging.DEBUG,
                ConfigSource.ENVIRONMENT,
                "Debug logging for development",
            )
        elif self._environment == ConfigEnvironment.PRODUCTION:
            self.set_config(
                "DEBUG",
                False,
                ConfigSource.ENVIRONMENT,
                "Debug mode disabled for production",
            )
            self.set_config(
                "LOG_LEVEL",
                logging.WARNING,
                ConfigSource.ENVIRONMENT,
                "Warning level logging for production",
            )

    def _load_application_config(self) -> None:
        """Load application-specific configuration."""
        # Security configuration
        self.set_config(
            "SECRET_KEY",
            get_unified_config().get_env("PORTAL_SECRET_KEY", "change-me"),
            ConfigSource.ENVIRONMENT,
            "Application secret key",
            required=True,
        )

        # Messaging configuration
        self.set_config(
            "DEFAULT_MODE", "pyautogui", ConfigSource.DEFAULT, "Default messaging mode"
        )
        self.set_config(
            "DEFAULT_COORDINATE_MODE",
            "8-agent",
            ConfigSource.DEFAULT,
            "Default coordinate mode for messaging",
        )

        # Task configuration
        self.set_config(
            "TASK_ID_TIMESTAMP_FORMAT",
            "%Y%m%d_%H%M%S_%f",
            ConfigSource.DEFAULT,
            "Timestamp format for task identifiers",
        )

        # Reporting configuration
        self.set_config(
            "DEFAULT_REPORTS_DIR",
            Path("reports"),
            ConfigSource.DEFAULT,
            "Default directory for reports",
        )
        self.set_config(
            "INCLUDE_METADATA",
            True,
            ConfigSource.DEFAULT,
            "Include metadata in reports",
        )
        self.set_config(
            "INCLUDE_RECOMMENDATIONS",
            True,
            ConfigSource.DEFAULT,
            "Include recommendations in reports",
        )

    def set_config(
        self,
        key: str,
        value: Any,
        source: ConfigSource,
        description: str = "",
        required: bool = False,
        validation_rules: Optional[Dict[str, Any]] = None,
    ) -> None:
=======
        
        self._initialized = True
        
    def _load_core_config(self) -> None:
        """Load core system configuration."""
        # Logging configuration
        self.set_config("LOG_LEVEL", 
                       getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
                       ConfigSource.ENVIRONMENT,
                       "Global logging level for the application")
        
        # Environment configuration
        self.set_config("ENVIRONMENT", self._environment.value, ConfigSource.ENVIRONMENT,
                       "Current environment (development/testing/production)")
        
        # Path configuration
        root_dir = Path(__file__).resolve().parents[2]
        self.set_config("ROOT_DIR", root_dir, ConfigSource.DEFAULT,
                       "Root directory of the application")
        
        # Agent configuration
        self.set_config("AGENT_COUNT", 8, ConfigSource.DEFAULT,
                       "Number of agents in the system")
        self.set_config("CAPTAIN_ID", "Agent-4", ConfigSource.DEFAULT,
                       "Captain agent identifier")
        
    def _load_environment_config(self) -> None:
        """Load environment-specific configuration."""
        if self._environment == ConfigEnvironment.DEVELOPMENT:
            self.set_config("DEBUG", True, ConfigSource.ENVIRONMENT,
                           "Debug mode enabled for development")
            self.set_config("LOG_LEVEL", logging.DEBUG, ConfigSource.ENVIRONMENT,
                           "Debug logging for development")
        elif self._environment == ConfigEnvironment.PRODUCTION:
            self.set_config("DEBUG", False, ConfigSource.ENVIRONMENT,
                           "Debug mode disabled for production")
            self.set_config("LOG_LEVEL", logging.WARNING, ConfigSource.ENVIRONMENT,
                           "Warning level logging for production")
                           
    def _load_application_config(self) -> None:
        """Load application-specific configuration."""
        # Security configuration
        self.set_config("SECRET_KEY", 
                       os.getenv("PORTAL_SECRET_KEY", "change-me"),
                       ConfigSource.ENVIRONMENT,
                       "Application secret key",
                       required=True)
        
        # Messaging configuration
        self.set_config("DEFAULT_MODE", "pyautogui", ConfigSource.DEFAULT,
                       "Default messaging mode")
        self.set_config("DEFAULT_COORDINATE_MODE", "8-agent", ConfigSource.DEFAULT,
                       "Default coordinate mode for messaging")
        
        # Task configuration
        self.set_config("TASK_ID_TIMESTAMP_FORMAT", "%Y%m%d_%H%M%S_%f", ConfigSource.DEFAULT,
                       "Timestamp format for task identifiers")
        
        # Reporting configuration
        self.set_config("DEFAULT_REPORTS_DIR", Path("reports"), ConfigSource.DEFAULT,
                       "Default directory for reports")
        self.set_config("INCLUDE_METADATA", True, ConfigSource.DEFAULT,
                       "Include metadata in reports")
        self.set_config("INCLUDE_RECOMMENDATIONS", True, ConfigSource.DEFAULT,
                       "Include recommendations in reports")
        
    def set_config(self, key: str, value: Any, source: ConfigSource, 
                   description: str = "", required: bool = False,
                   validation_rules: Optional[Dict[str, Any]] = None) -> None:
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
        """Set a configuration value."""
        self._config[key] = ConfigValue(
            value=value,
            source=source,
            description=description,
            required=required,
<<<<<<< HEAD
            validation_rules=validation_rules,
        )

=======
            validation_rules=validation_rules
        )
        
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        if key not in self._config:
            if default is not None:
                return default
            raise KeyError(f"Configuration key '{key}' not found")
        return self._config[key].value
<<<<<<< HEAD

    def get_config_info(self, key: str) -> Optional[ConfigValue]:
        """Get configuration value with metadata."""
        return self._config.get(key)

    def has_config(self, key: str) -> bool:
        """Check if configuration key exists."""
        return key in self._config

    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return {key: config.value for key, config in self._config.items()}

    def get_config_by_source(self, source: ConfigSource) -> Dict[str, Any]:
        """Get configuration values by source."""
        return {
            key: config.value
            for key, config in self._config.items()
            if config.source == source
        }

=======
        
    def get_config_info(self, key: str) -> Optional[ConfigValue]:
        """Get configuration value with metadata."""
        return self._config.get(key)
        
    def has_config(self, key: str) -> bool:
        """Check if configuration key exists."""
        return key in self._config
        
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return {key: config.value for key, config in self._config.items()}
        
    def get_config_by_source(self, source: ConfigSource) -> Dict[str, Any]:
        """Get configuration values by source."""
        return {key: config.value for key, config in self._config.items() 
                if config.source == source}
                
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    def validate_config(self) -> Dict[str, Any]:
        """Validate all configuration values."""
        errors = {}
        for key, config in self._config.items():
            if config.required and config.value is None:
                errors[key] = f"Required configuration '{key}' is None"
        return errors


# Global configuration manager instance
_config_manager = ConfigurationManager()


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value from global manager."""
    if not _config_manager._initialized:
        _config_manager.initialize()
    return _config_manager.get_config(key, default)


<<<<<<< HEAD
def set_config(
    key: str,
    value: Any,
    source: ConfigSource = ConfigSource.RUNTIME,
    description: str = "",
    required: bool = False,
) -> None:
=======
def set_config(key: str, value: Any, source: ConfigSource = ConfigSource.RUNTIME,
               description: str = "", required: bool = False) -> None:
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    """Set configuration value in global manager."""
    if not _config_manager._initialized:
        _config_manager.initialize()
    _config_manager.set_config(key, value, source, description, required)


def get_config_manager() -> ConfigurationManager:
    """Get the global configuration manager instance."""
    if not _config_manager._initialized:
        _config_manager.initialize()
    return _config_manager


# FSM Configuration compatibility
class FSMConfig:
    """FSM Configuration compatibility wrapper."""
<<<<<<< HEAD

=======
    
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get FSM configuration value."""
        return get_config(f"FSM_{key}", default)
<<<<<<< HEAD

    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set FSM configuration value."""
        set_config(
            f"FSM_{key}", value, ConfigSource.RUNTIME, f"FSM configuration: {key}"
        )
=======
        
    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set FSM configuration value."""
        set_config(f"FSM_{key}", value, ConfigSource.RUNTIME, f"FSM configuration: {key}")
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65


# Initialize configuration on module import
_config_manager.initialize()
<<<<<<< HEAD
=======

>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
