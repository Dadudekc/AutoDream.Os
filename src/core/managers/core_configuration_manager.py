"""
Core Configuration Manager - Phase-2 Manager Consolidation
=========================================================
Consolidates ConfigurationManager, DiscordConfigurationManager, and ConfigManager.
Author: Agent-3 (Infrastructure & DevOps Specialist) | License: MIT
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .config_defaults import (
    get_default_app_config,
    get_default_db_config,
    get_default_discord_config,
    get_validation_rules,
)
from .contracts import ConfigurationManager, ManagerContext, ManagerResult


class CoreConfigurationManager(ConfigurationManager):
    """Core configuration manager - consolidates all config operations."""

    def __init__(self):
        """Initialize core configuration manager."""
        self.configs: dict[str, dict[str, Any]] = {}
        self.config_files: dict[str, str] = {}
        self.environment_vars: dict[str, str] = {}
        self.validation_rules: dict[str, dict[str, Any]] = {}

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize configuration manager."""
        try:
            # Load environment variables
            self._load_environment_vars()

            # Load default configurations
            self._load_default_configs()

            # Setup validation rules
            self._setup_validation_rules()

            context.logger("Core Configuration Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize Core Configuration Manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute configuration operation."""
        try:
            if operation == "load_config":
                config_key = payload.get("config_key", "")
                return self.load_config(context, config_key)
            elif operation == "save_config":
                config_key = payload.get("config_key", "")
                config_data = payload.get("config_data", {})
                return self.save_config(context, config_key, config_data)
            elif operation == "validate_config":
                config_data = payload.get("config_data", {})
                return self.validate_config(context, config_data)
            elif operation == "get_all_configs":
                return self._get_all_configs(context)
            elif operation == "export_config":
                return self._export_config(context, payload)
            elif operation == "import_config":
                return self._import_config(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def load_config(self, context: ManagerContext, config_key: str) -> ManagerResult:
        """Load configuration."""
        try:
            # Try to load from memory first
            if config_key in self.configs:
                return ManagerResult(
                    success=True,
                    data={"config_key": config_key, "config": self.configs[config_key]},
                    metrics={"config_keys": len(self.configs[config_key])},
                )

            # Try to load from file
            if config_key in self.config_files:
                file_path = self.config_files[config_key]
                if os.path.exists(file_path):
                    with open(file_path, encoding="utf-8") as f:
                        config_data = json.load(f)
                    self.configs[config_key] = config_data
                    return ManagerResult(
                        success=True,
                        data={"config_key": config_key, "config": config_data},
                        metrics={"config_keys": len(config_data)},
                    )

            # Try to load from environment
            if config_key.upper() in self.environment_vars:
                env_value = self.environment_vars[config_key.upper()]
                try:
                    config_data = json.loads(env_value)
                except json.JSONDecodeError:
                    config_data = {"value": env_value}

                return ManagerResult(
                    success=True,
                    data={
                        "config_key": config_key,
                        "config": config_data,
                        "source": "environment",
                    },
                    metrics={"config_keys": len(config_data)},
                )

            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Configuration not found: {config_key}",
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def save_config(
        self, context: ManagerContext, config_key: str, config_data: dict[str, Any]
    ) -> ManagerResult:
        """Save configuration."""
        try:
            # Validate configuration first
            validation_result = self.validate_config(context, config_data)
            if not validation_result.success:
                return validation_result

            # Save to memory
            self.configs[config_key] = config_data

            # Save to file if file path is specified
            file_path = config_data.get("file_path")
            if file_path:
                self.config_files[config_key] = file_path
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(config_data, f, indent=2)

            return ManagerResult(
                success=True,
                data={"config_key": config_key, "config": config_data, "saved": True},
                metrics={"config_keys": len(config_data)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def validate_config(
        self, context: ManagerContext, config_data: dict[str, Any]
    ) -> ManagerResult:
        """Validate configuration."""
        try:
            validation_errors = []

            # Check required fields
            if "type" in config_data:
                config_type = config_data["type"]
                if config_type in self.validation_rules:
                    rules = self.validation_rules[config_type]
                    for field, rule in rules.items():
                        if rule.get("required", False) and field not in config_data:
                            validation_errors.append(f"Required field missing: {field}")
                        elif field in config_data:
                            value = config_data[field]
                            if "type" in rule:
                                expected_type = rule["type"]
                                if not isinstance(value, expected_type):
                                    validation_errors.append(
                                        f"Field {field} must be {expected_type.__name__}"
                                    )
                            if "min_length" in rule and len(str(value)) < rule["min_length"]:
                                validation_errors.append(
                                    f"Field {field} too short (min {rule['min_length']})"
                                )
                            if "max_length" in rule and len(str(value)) > rule["max_length"]:
                                validation_errors.append(
                                    f"Field {field} too long (max {rule['max_length']})"
                                )

            # Basic validation
            if not isinstance(config_data, dict):
                validation_errors.append("Configuration must be a dictionary")

            if validation_errors:
                return ManagerResult(
                    success=False,
                    data={"validation_errors": validation_errors},
                    metrics={"error_count": len(validation_errors)},
                    error=f"Validation failed: {', '.join(validation_errors)}",
                )

            return ManagerResult(
                success=True,
                data={"valid": True, "config": config_data},
                metrics={"config_keys": len(config_data)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup configuration manager."""
        try:
            # Save all configurations
            for config_key, file_path in self.config_files.items():
                if config_key in self.configs:
                    try:
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(self.configs[config_key], f, indent=2)
                    except Exception as e:
                        context.logger(f"Failed to save config {config_key}: {e}")

            # Clear data
            self.configs.clear()
            self.config_files.clear()
            self.environment_vars.clear()
            self.validation_rules.clear()

            context.logger("Core Configuration Manager cleaned up")
            return True
        except Exception as e:
            context.logger(f"Failed to cleanup Core Configuration Manager: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get configuration manager status."""
        return {
            "total_configs": len(self.configs),
            "config_keys": list(self.configs.keys()),
            "file_configs": len(self.config_files),
            "environment_vars": len(self.environment_vars),
            "validation_rules": len(self.validation_rules),
        }

    def _load_environment_vars(self) -> None:
        """Load environment variables."""
        try:
            # Load from .env file if it exists
            env_file = Path(".env")
            if env_file.exists():
                with open(env_file, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            self.environment_vars[key.strip()] = value.strip()

            # Load from system environment
            for key, value in os.environ.items():
                if key.startswith(("DISCORD_", "CONFIG_", "APP_")):
                    self.environment_vars[key] = value
        except Exception:
            pass  # Ignore environment loading errors

    def _load_default_configs(self) -> None:
        """Load default configurations."""
        try:
            self.configs["discord"] = get_default_discord_config(self.environment_vars)
            self.configs["application"] = get_default_app_config(self.environment_vars)
            self.configs["database"] = get_default_db_config(self.environment_vars)
        except Exception:
            pass  # Ignore default config loading errors

    def _setup_validation_rules(self) -> None:
        """Setup configuration validation rules."""
        self.validation_rules = get_validation_rules()

    def _get_all_configs(self, context: ManagerContext) -> ManagerResult:
        """Get all configurations."""
        try:
            return ManagerResult(
                success=True,
                data={"configs": self.configs},
                metrics={"total_configs": len(self.configs)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _export_config(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Export configuration."""
        try:
            config_key = payload.get("config_key", "")
            export_path = payload.get("export_path", f"config/{config_key}.json")

            if config_key not in self.configs:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Configuration not found: {config_key}",
                )

            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(self.configs[config_key], f, indent=2)

            return ManagerResult(
                success=True,
                data={
                    "config_key": config_key,
                    "export_path": export_path,
                    "exported": True,
                },
                metrics={"file_size": os.path.getsize(export_path)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _import_config(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Import configuration."""
        try:
            import_path = payload.get("import_path", "")
            config_key = payload.get("config_key", "")

            if not os.path.exists(import_path):
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Import file not found: {import_path}",
                )

            with open(import_path, encoding="utf-8") as f:
                config_data = json.load(f)

            # Validate imported configuration
            validation_result = self.validate_config(context, config_data)
            if not validation_result.success:
                return validation_result

            # Save imported configuration
            self.configs[config_key] = config_data

            return ManagerResult(
                success=True,
                data={
                    "config_key": config_key,
                    "import_path": import_path,
                    "imported": True,
                },
                metrics={"config_keys": len(config_data)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))
