"""
SSOT Configuration Manager - V2 Compliant
=========================================

Single Source of Truth configuration management system.
Centralizes all configuration management for V2_SWARM system.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SSOTConfig:
    """Single Source of Truth configuration."""

    # Agent Configuration
    agents: dict[str, Any] = field(default_factory=dict)

    # System Configuration
    system: dict[str, Any] = field(default_factory=dict)

    # Messaging Configuration
    messaging: dict[str, Any] = field(default_factory=dict)

    # Quality Gates Configuration
    quality_gates: dict[str, Any] = field(default_factory=dict)

    # Protocol Configuration
    protocols: dict[str, Any] = field(default_factory=dict)

    # Database Configuration
    database: dict[str, Any] = field(default_factory=dict)

    # Monitoring Configuration
    monitoring: dict[str, Any] = field(default_factory=dict)


class SSOTManager:
    """Single Source of Truth configuration manager."""

    def __init__(self, config_path: str = "config/unified_config.yaml"):
        """Initialize SSOT manager."""
        self.config_path = Path(config_path)
        self.config: SSOTConfig | None = None
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                if self.config_path.suffix == ".json":
                    with open(self.config_path) as f:
                        data = json.load(f)
                else:
                    # Handle YAML files
                    import yaml

                    with open(self.config_path) as f:
                        data = yaml.safe_load(f)

                self.config = SSOTConfig(**data)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                self.config = SSOTConfig()
                logger.warning(f"Configuration file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            self.config = SSOTConfig()

    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            if self.config_path.suffix == ".json":
                with open(self.config_path, "w") as f:
                    json.dump(self.config.__dict__, f, indent=2)
            else:
                import yaml

                with open(self.config_path, "w") as f:
                    yaml.dump(self.config.__dict__, f, default_flow_style=False)

            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def get_agent_config(self, agent_id: str) -> dict[str, Any]:
        """Get configuration for specific agent."""
        return self.config.agents.get(agent_id, {})

    def set_agent_config(self, agent_id: str, config: dict[str, Any]) -> None:
        """Set configuration for specific agent."""
        self.config.agents[agent_id] = config
        logger.info(f"Configuration updated for agent {agent_id}")

    def get_system_config(self, key: str, default: Any = None) -> Any:
        """Get system configuration value."""
        return self.config.system.get(key, default)

    def set_system_config(self, key: str, value: Any) -> None:
        """Set system configuration value."""
        self.config.system[key] = value
        logger.info(f"System configuration updated: {key}")

    def get_messaging_config(self) -> dict[str, Any]:
        """Get messaging configuration."""
        return self.config.messaging

    def set_messaging_config(self, config: dict[str, Any]) -> None:
        """Set messaging configuration."""
        self.config.messaging.update(config)
        logger.info("Messaging configuration updated")

    def get_quality_gates_config(self) -> dict[str, Any]:
        """Get quality gates configuration."""
        return self.config.quality_gates

    def set_quality_gates_config(self, config: dict[str, Any]) -> None:
        """Set quality gates configuration."""
        self.config.quality_gates.update(config)
        logger.info("Quality gates configuration updated")

    def get_protocol_config(self, protocol_name: str) -> dict[str, Any]:
        """Get protocol configuration."""
        return self.config.protocols.get(protocol_name, {})

    def set_protocol_config(self, protocol_name: str, config: dict[str, Any]) -> None:
        """Set protocol configuration."""
        self.config.protocols[protocol_name] = config
        logger.info(f"Protocol configuration updated: {protocol_name}")

    def get_database_config(self) -> dict[str, Any]:
        """Get database configuration."""
        return self.config.database

    def set_database_config(self, config: dict[str, Any]) -> None:
        """Set database configuration."""
        self.config.database.update(config)
        logger.info("Database configuration updated")

    def get_monitoring_config(self) -> dict[str, Any]:
        """Get monitoring configuration."""
        return self.config.monitoring

    def set_monitoring_config(self, config: dict[str, Any]) -> None:
        """Set monitoring configuration."""
        self.config.monitoring.update(config)
        logger.info("Monitoring configuration updated")

    def validate_config(self) -> bool:
        """Validate configuration integrity."""
        try:
            # Check required fields
            required_sections = ["agents", "system", "messaging", "quality_gates"]
            for section in required_sections:
                if not hasattr(self.config, section):
                    logger.error(f"Missing required configuration section: {section}")
                    return False

            # Validate agent configurations
            for agent_id, agent_config in self.config.agents.items():
                if not isinstance(agent_config, dict):
                    logger.error(f"Invalid agent configuration for {agent_id}")
                    return False

            logger.info("Configuration validation passed")
            return True
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False

    def get_all_config(self) -> dict[str, Any]:
        """Get all configuration as dictionary."""
        return self.config.__dict__

    def reset_config(self) -> None:
        """Reset configuration to defaults."""
        self.config = SSOTConfig()
        logger.info("Configuration reset to defaults")

    def export_config(self, export_path: str) -> None:
        """Export configuration to file."""
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)

            with open(export_file, "w") as f:
                json.dump(self.config.__dict__, f, indent=2)

            logger.info(f"Configuration exported to {export_path}")
        except Exception as e:
            logger.error(f"Failed to export configuration: {e}")

    def import_config(self, import_path: str) -> None:
        """Import configuration from file."""
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                logger.error(f"Import file not found: {import_path}")
                return

            with open(import_file) as f:
                data = json.load(f)

            self.config = SSOTConfig(**data)
            logger.info(f"Configuration imported from {import_path}")
        except Exception as e:
            logger.error(f"Failed to import configuration: {e}")


# Global SSOT manager instance
_ssot_manager: SSOTManager | None = None


def get_ssot_manager() -> SSOTManager:
    """Get global SSOT manager instance."""
    global _ssot_manager
    if _ssot_manager is None:
        _ssot_manager = SSOTManager()
    return _ssot_manager


def initialize_ssot(config_path: str = "config/unified_config.yaml") -> SSOTManager:
    """Initialize SSOT manager with custom config path."""
    global _ssot_manager
    _ssot_manager = SSOTManager(config_path)
    return _ssot_manager
