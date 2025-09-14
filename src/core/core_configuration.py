#!/usr/bin/env python3
"""
Core Configuration - Consolidated Configuration System
=====================================================

Consolidated configuration system providing unified configuration management for:
- Environment configuration
- Agent configuration
- System configuration
- Validation configuration

This module consolidates configuration systems for better organization and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

class Environment(Enum):
    """Environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


@dataclass
class EnvironmentConfig:
    """Environment configuration."""
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False
    log_level: str = "INFO"
    data_dir: str = "data"
    log_dir: str = "logs"
    temp_dir: str = "temp"
    config_dir: str = "config"

    def validate(self) -> bool:
        """Validate environment configuration."""
        return (
            self.environment in Environment and
            self.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] and
            all(isinstance(path, str) and path for path in [
                self.data_dir, self.log_dir, self.temp_dir, self.config_dir
            ])
        )


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

class AgentType(Enum):
    """Agent type enumeration."""
    ARCHITECTURE = "architecture"
    COORDINATION = "coordination"
    COMMUNICATION = "communication"
    INTEGRATION = "integration"
    MONITORING = "monitoring"
    OPTIMIZATION = "optimization"
    VALIDATION = "validation"


@dataclass
class AgentConfig:
    """Agent configuration."""
    agent_id: str = "agent-2"
    agent_name: str = "Architecture & Design Specialist"
    agent_type: AgentType = AgentType.ARCHITECTURE
    version: str = "2.0.0"
    max_concurrent_tasks: int = 5
    task_timeout: float = 300.0
    heartbeat_interval: float = 30.0
    status_report_interval: float = 60.0
    capabilities: list[str] = field(default_factory=lambda: [
        "analysis", "consolidation", "architecture", "design"
    ])
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate agent configuration."""
        return (
            bool(self.agent_id and self.agent_name) and
            self.agent_type in AgentType and
            all(value > 0 for value in [
                self.max_concurrent_tasks,
                self.task_timeout,
                self.heartbeat_interval,
                self.status_report_interval
            ]) and
            isinstance(self.capabilities, list) and
            isinstance(self.metadata, dict)
        )


# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================

@dataclass
class SystemConfig:
    """System configuration."""
    system_name: str = "Core Unified System"
    system_version: str = "2.0.0"
    max_memory_usage: float = 0.8
    max_cpu_usage: float = 0.8
    max_disk_usage: float = 0.9
    health_check_interval: float = 60.0
    metrics_collection_interval: float = 30.0
    cleanup_interval: float = 300.0
    backup_interval: float = 3600.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate system configuration."""
        return (
            bool(self.system_name) and
            all(0 <= value <= 1 for value in [
                self.max_memory_usage,
                self.max_cpu_usage,
                self.max_disk_usage
            ]) and
            all(value > 0 for value in [
                self.health_check_interval,
                self.metrics_collection_interval,
                self.cleanup_interval,
                self.backup_interval
            ]) and
            isinstance(self.metadata, dict)
        )


# ============================================================================
# VALIDATION CONFIGURATION
# ============================================================================

class ValidationLevel(Enum):
    """Validation level enumeration."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"


@dataclass
class ValidationConfig:
    """Validation configuration."""
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    enable_schema_validation: bool = True
    enable_type_validation: bool = True
    enable_range_validation: bool = True
    enable_format_validation: bool = True
    max_validation_errors: int = 100
    validation_timeout: float = 30.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate validation configuration."""
        return (
            self.validation_level in ValidationLevel and
            isinstance(self.enable_schema_validation, bool) and
            isinstance(self.enable_type_validation, bool) and
            isinstance(self.enable_range_validation, bool) and
            isinstance(self.enable_format_validation, bool) and
            self.max_validation_errors > 0 and
            self.validation_timeout > 0 and
            isinstance(self.metadata, dict)
        )


# ============================================================================
# UNIFIED CONFIGURATION
# ============================================================================

@dataclass
class UnifiedConfiguration:
    """Unified configuration system."""
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    system: SystemConfig = field(default_factory=SystemConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)

    def validate(self) -> bool:
        """Validate unified configuration."""
        return all([
            self.environment.validate(),
            self.agent.validate(),
            self.system.validate(),
            self.validation.validate()
        ])

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "environment": {
                "environment": self.environment.environment.value,
                "debug": self.environment.debug,
                "log_level": self.environment.log_level,
                "data_dir": self.environment.data_dir,
                "log_dir": self.environment.log_dir,
                "temp_dir": self.environment.temp_dir,
                "config_dir": self.environment.config_dir
            },
            "agent": {
                "agent_id": self.agent.agent_id,
                "agent_name": self.agent.agent_name,
                "agent_type": self.agent.agent_type.value,
                "version": self.agent.version,
                "max_concurrent_tasks": self.agent.max_concurrent_tasks,
                "task_timeout": self.agent.task_timeout,
                "heartbeat_interval": self.agent.heartbeat_interval,
                "status_report_interval": self.agent.status_report_interval,
                "capabilities": self.agent.capabilities,
                "metadata": self.agent.metadata
            },
            "system": {
                "system_name": self.system.system_name,
                "system_version": self.system.system_version,
                "max_memory_usage": self.system.max_memory_usage,
                "max_cpu_usage": self.system.max_cpu_usage,
                "max_disk_usage": self.system.max_disk_usage,
                "health_check_interval": self.system.health_check_interval,
                "metrics_collection_interval": self.system.metrics_collection_interval,
                "cleanup_interval": self.system.cleanup_interval,
                "backup_interval": self.system.backup_interval,
                "metadata": self.system.metadata
            },
            "validation": {
                "validation_level": self.validation.validation_level.value,
                "enable_schema_validation": self.validation.enable_schema_validation,
                "enable_type_validation": self.validation.enable_type_validation,
                "enable_range_validation": self.validation.enable_range_validation,
                "enable_format_validation": self.validation.enable_format_validation,
                "max_validation_errors": self.validation.max_validation_errors,
                "validation_timeout": self.validation.validation_timeout,
                "metadata": self.validation.metadata
            }
        }

    def save_to_file(self, file_path: str | Path) -> bool:
        """Save configuration to file."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            logging.error(f"Failed to save configuration to {file_path}: {e}")
            return False

    def load_from_file(self, file_path: str | Path) -> bool:
        """Load configuration from file."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False

            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)

            # Load environment config
            if "environment" in data:
                env_data = data["environment"]
                self.environment = EnvironmentConfig(
                    environment=Environment(env_data.get("environment", "development")),
                    debug=env_data.get("debug", False),
                    log_level=env_data.get("log_level", "INFO"),
                    data_dir=env_data.get("data_dir", "data"),
                    log_dir=env_data.get("log_dir", "logs"),
                    temp_dir=env_data.get("temp_dir", "temp"),
                    config_dir=env_data.get("config_dir", "config")
                )

            # Load agent config
            if "agent" in data:
                agent_data = data["agent"]
                self.agent = AgentConfig(
                    agent_id=agent_data.get("agent_id", "agent-2"),
                    agent_name=agent_data.get("agent_name", "Architecture & Design Specialist"),
                    agent_type=AgentType(agent_data.get("agent_type", "architecture")),
                    version=agent_data.get("version", "2.0.0"),
                    max_concurrent_tasks=agent_data.get("max_concurrent_tasks", 5),
                    task_timeout=agent_data.get("task_timeout", 300.0),
                    heartbeat_interval=agent_data.get("heartbeat_interval", 30.0),
                    status_report_interval=agent_data.get("status_report_interval", 60.0),
                    capabilities=agent_data.get("capabilities", []),
                    metadata=agent_data.get("metadata", {})
                )

            # Load system config
            if "system" in data:
                system_data = data["system"]
                self.system = SystemConfig(
                    system_name=system_data.get("system_name", "Core Unified System"),
                    system_version=system_data.get("system_version", "2.0.0"),
                    max_memory_usage=system_data.get("max_memory_usage", 0.8),
                    max_cpu_usage=system_data.get("max_cpu_usage", 0.8),
                    max_disk_usage=system_data.get("max_disk_usage", 0.9),
                    health_check_interval=system_data.get("health_check_interval", 60.0),
                    metrics_collection_interval=system_data.get("metrics_collection_interval", 30.0),
                    cleanup_interval=system_data.get("cleanup_interval", 300.0),
                    backup_interval=system_data.get("backup_interval", 3600.0),
                    metadata=system_data.get("metadata", {})
                )

            # Load validation config
            if "validation" in data:
                validation_data = data["validation"]
                self.validation = ValidationConfig(
                    validation_level=ValidationLevel(validation_data.get("validation_level", "standard")),
                    enable_schema_validation=validation_data.get("enable_schema_validation", True),
                    enable_type_validation=validation_data.get("enable_type_validation", True),
                    enable_range_validation=validation_data.get("enable_range_validation", True),
                    enable_format_validation=validation_data.get("enable_format_validation", True),
                    max_validation_errors=validation_data.get("max_validation_errors", 100),
                    validation_timeout=validation_data.get("validation_timeout", 30.0),
                    metadata=validation_data.get("metadata", {})
                )

            return True
        except Exception as e:
            logging.error(f"Failed to load configuration from {file_path}: {e}")
            return False


# ============================================================================
# CONFIGURATION MANAGER
# ============================================================================

class ConfigurationManager:
    """Configuration manager for unified configuration system."""

    def __init__(self, config_file: str | Path = "config/unified_config.json"):
        self.config_file = Path(config_file)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = UnifiedConfiguration()
        self.load_config()

    def load_config(self) -> bool:
        """Load configuration from file."""
        if self.config_file.exists():
            return self.config.load_from_file(self.config_file)
        else:
            self.logger.info(f"Configuration file {self.config_file} not found, using defaults")
            return True

    def save_config(self) -> bool:
        """Save configuration to file."""
        return self.config.save_to_file(self.config_file)

    def get_config(self) -> UnifiedConfiguration:
        """Get current configuration."""
        return self.config

    def update_config(self, **kwargs) -> bool:
        """Update configuration values."""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                else:
                    self.logger.warning(f"Unknown configuration key: {key}")
                    return False

            return self.config.validate()
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False

    def validate_config(self) -> bool:
        """Validate current configuration."""
        return self.config.validate()

    def get_config_summary(self) -> dict[str, Any]:
        """Get configuration summary."""
        return {
            "config_file": str(self.config_file),
            "is_valid": self.config.validate(),
            "environment": self.config.environment.environment.value,
            "agent_id": self.config.agent.agent_id,
            "system_name": self.config.system.system_name,
            "validation_level": self.config.validation.validation_level.value
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_environment_config(
    environment: Environment = Environment.DEVELOPMENT,
    debug: bool = False,
    log_level: str = "INFO"
) -> EnvironmentConfig:
    """Create environment configuration."""
    return EnvironmentConfig(
        environment=environment,
        debug=debug,
        log_level=log_level
    )


def create_agent_config(
    agent_id: str = "agent-2",
    agent_name: str = "Architecture & Design Specialist",
    agent_type: AgentType = AgentType.ARCHITECTURE
) -> AgentConfig:
    """Create agent configuration."""
    return AgentConfig(
        agent_id=agent_id,
        agent_name=agent_name,
        agent_type=agent_type
    )


def create_system_config(
    system_name: str = "Core Unified System",
    system_version: str = "2.0.0"
) -> SystemConfig:
    """Create system configuration."""
    return SystemConfig(
        system_name=system_name,
        system_version=system_version
    )


def create_validation_config(
    validation_level: ValidationLevel = ValidationLevel.STANDARD
) -> ValidationConfig:
    """Create validation configuration."""
    return ValidationConfig(
        validation_level=validation_level
    )


def create_unified_configuration() -> UnifiedConfiguration:
    """Create unified configuration."""
    return UnifiedConfiguration()


def create_configuration_manager(
    config_file: str | Path = "config/unified_config.json"
) -> ConfigurationManager:
    """Create configuration manager."""
    return ConfigurationManager(config_file)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("Core Configuration - Consolidated Configuration System")
    print("=" * 50)

    # Create configuration manager
    config_manager = create_configuration_manager()
    print(f"Configuration manager created: {config_manager.get_config_summary()}")

    # Create individual configurations
    env_config = create_environment_config(Environment.DEVELOPMENT, True, "DEBUG")
    print(f"Environment config created: {env_config.validate()}")

    agent_config = create_agent_config("agent-2", "Architecture & Design Specialist")
    print(f"Agent config created: {agent_config.validate()}")

    system_config = create_system_config("Core Unified System", "2.0.0")
    print(f"System config created: {system_config.validate()}")

    validation_config = create_validation_config(ValidationLevel.STANDARD)
    print(f"Validation config created: {validation_config.validate()}")

    # Create unified configuration
    unified_config = create_unified_configuration()
    print(f"Unified configuration created: {unified_config.validate()}")

    print("\nCore Configuration initialization complete!")


if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
