"""
Unified Configuration Manager - Phase 2 Manager Consolidation
===========================================================

Consolidates CoreConfigurationManager and related configuration managers.
Implements SSOT for all configuration operations using BaseManager framework.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import json
import os
from datetime import datetime

from .base_manager import BaseManager, ManagerType
from .contracts import ManagerContext, ManagerResult


class UnifiedConfigurationManager(BaseManager):
    """
    Unified configuration manager consolidating all configuration operations.

    Consolidates:
    - CoreConfigurationManager
    - DiscordConfigurationManager
    - ConfigManager
    - And related configuration utilities

    Provides SSOT for all configuration management with standardized interfaces.
    """

    def __init__(self):
        """Initialize unified configuration manager."""
        super().__init__(ManagerType.CONFIGURATION, "unified_configuration")

        # Configuration sources
        self.file_configs: Dict[str, Dict[str, Any]] = {}
        self.env_configs: Dict[str, str] = {}
        self.runtime_configs: Dict[str, Any] = {}

        # Configuration metadata
        self.config_sources: Dict[str, str] = {}  # config_key -> source_type
        self.config_timestamps: Dict[str, datetime] = {}  # config_key -> last_updated
        self.config_versions: Dict[str, int] = {}  # config_key -> version

        # Validation rules
        self.validation_rules: Dict[str, Dict[str, Any]] = {}

        # Configuration paths
        self.config_dir = Path("config")
        self.backup_dir = Path("config/backups")

    def _execute_operation(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """
        Execute configuration operation.

        Supported operations:
        - load_config: Load configuration from source
        - save_config: Save configuration to source
        - validate_config: Validate configuration data
        - merge_configs: Merge multiple configurations
        - export_config: Export configuration to file
        - get_config_schema: Get configuration schema
        - list_configs: List available configurations
        - delete_config: Delete configuration
        """

        if operation == "load_config":
            return self._load_config_operation(payload)
        elif operation == "save_config":
            return self._save_config_operation(payload)
        elif operation == "validate_config":
            return self._validate_config_operation(payload)
        elif operation == "merge_configs":
            return self._merge_configs_operation(payload)
        elif operation == "export_config":
            return self._export_config_operation(payload)
        elif operation == "get_config_schema":
            return self._get_config_schema_operation(payload)
        elif operation == "list_configs":
            return self._list_configs_operation(payload)
        elif operation == "delete_config":
            return self._delete_config_operation(payload)
        else:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": operation},
                error=f"Unknown configuration operation: {operation}"
            )

    def _load_config_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """Load configuration from specified source."""
        try:
            config_key = payload.get("config_key", "")
            source_type = payload.get("source_type", "file")  # file, env, runtime
            source_path = payload.get("source_path", "")
            default_values = payload.get("default_values", {})

            if not config_key:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "load_config"},
                    error="config_key is required"
                )

            config_data = {}

            if source_type == "file":
                config_data = self._load_from_file(config_key, source_path)
            elif source_type == "env":
                config_data = self._load_from_env(config_key)
            elif source_type == "runtime":
                config_data = self.runtime_configs.get(config_key, {})
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "load_config"},
                    error=f"Unsupported source_type: {source_type}"
                )

            # Apply default values for missing keys
            for key, default_value in default_values.items():
                if key not in config_data:
                    config_data[key] = default_value

            # Store configuration
            self.file_configs[config_key] = config_data
            self.config_sources[config_key] = source_type
            self.config_timestamps[config_key] = datetime.now()
            self.config_versions[config_key] = self.config_versions.get(config_key, 0) + 1

            return ManagerResult(
                success=True,
                data={
                    "config_key": config_key,
                    "config_data": config_data,
                    "source_type": source_type,
                    "version": self.config_versions[config_key],
                    "loaded_at": self.config_timestamps[config_key].isoformat(),
                },
                metrics={
                    "operation": "load_config",
                    "config_keys_count": len(config_data),
                    "source_type": source_type,
                }
            )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "load_config"},
                error=f"Failed to load config: {str(e)}"
            )

    def _save_config_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """Save configuration to specified destination."""
        try:
            config_key = payload.get("config_key", "")
            config_data = payload.get("config_data", {})
            destination_type = payload.get("destination_type", "file")
            destination_path = payload.get("destination_path", "")
            create_backup = payload.get("create_backup", True)

            if not config_key:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "save_config"},
                    error="config_key is required"
                )

            success = False

            if destination_type == "file":
                success = self._save_to_file(config_key, config_data, destination_path, create_backup)
            elif destination_type == "runtime":
                self.runtime_configs[config_key] = config_data
                success = True
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "save_config"},
                    error=f"Unsupported destination_type: {destination_type}"
                )

            if success:
                # Update metadata
                self.config_sources[config_key] = destination_type
                self.config_timestamps[config_key] = datetime.now()
                self.config_versions[config_key] = self.config_versions.get(config_key, 0) + 1

                return ManagerResult(
                    success=True,
                    data={
                        "config_key": config_key,
                        "saved_at": self.config_timestamps[config_key].isoformat(),
                        "version": self.config_versions[config_key],
                        "destination_type": destination_type,
                    },
                    metrics={
                        "operation": "save_config",
                        "config_keys_count": len(config_data),
                        "destination_type": destination_type,
                    }
                )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "save_config"},
                    error="Failed to save configuration"
                )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "save_config"},
                error=f"Failed to save config: {str(e)}"
            )

    def _validate_config_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """Validate configuration data against rules."""
        try:
            config_data = payload.get("config_data", {})
            validation_rules = payload.get("validation_rules", {})
            config_key = payload.get("config_key", "unknown")

            # Use ValidationManager for validation
            validation_result = self.validation_manager.validate_config(
                config_data=config_data,
                validation_rules=validation_rules,
                component_type="configuration"
            )

            return ManagerResult(
                success=validation_result.is_valid,
                data={
                    "config_key": config_key,
                    "is_valid": validation_result.is_valid,
                    "errors": validation_result.errors,
                    "warnings": validation_result.warnings,
                    "validated_at": datetime.now().isoformat(),
                },
                metrics={
                    "operation": "validate_config",
                    "error_count": len(validation_result.errors),
                    "warning_count": len(validation_result.warnings),
                },
                error="Validation failed" if not validation_result.is_valid else None
            )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "validate_config"},
                error=f"Failed to validate config: {str(e)}"
            )

    def _merge_configs_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """Merge multiple configurations with conflict resolution."""
        try:
            config_keys = payload.get("config_keys", [])
            merge_strategy = payload.get("merge_strategy", "overwrite")  # overwrite, combine, priority
            priority_order = payload.get("priority_order", [])  # for priority strategy

            if not config_keys:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "merge_configs"},
                    error="config_keys list is required"
                )

            merged_config = {}
            merge_metadata = {
                "sources": [],
                "conflicts": [],
                "merge_strategy": merge_strategy,
            }

            # Load all configurations
            configs_to_merge = []
            for config_key in config_keys:
                if config_key in self.file_configs:
                    configs_to_merge.append((config_key, self.file_configs[config_key]))
                else:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={"operation": "merge_configs"},
                        error=f"Configuration not found: {config_key}"
                    )

            # Apply merge strategy
            if merge_strategy == "overwrite":
                for config_key, config_data in configs_to_merge:
                    merged_config.update(config_data)
                    merge_metadata["sources"].append(config_key)

            elif merge_strategy == "combine":
                all_keys = set()
                for config_key, config_data in configs_to_merge:
                    all_keys.update(config_data.keys())

                for key in all_keys:
                    values = []
                    sources = []
                    for config_key, config_data in configs_to_merge:
                        if key in config_data:
                            values.append(config_data[key])
                            sources.append(config_key)

                    if len(values) == 1:
                        merged_config[key] = values[0]
                    else:
                        # Multiple values - create combined entry
                        merged_config[key] = {
                            "values": values,
                            "sources": sources,
                            "conflict": True
                        }
                        merge_metadata["conflicts"].append({
                            "key": key,
                            "values": values,
                            "sources": sources
                        })

            elif merge_strategy == "priority":
                for priority_key in priority_order:
                    for config_key, config_data in configs_to_merge:
                        if config_key == priority_key:
                            merged_config.update(config_data)
                            merge_metadata["sources"].append(config_key)
                            break

            return ManagerResult(
                success=True,
                data={
                    "merged_config": merged_config,
                    "merge_metadata": merge_metadata,
                    "source_count": len(configs_to_merge),
                    "merged_at": datetime.now().isoformat(),
                },
                metrics={
                    "operation": "merge_configs",
                    "source_count": len(configs_to_merge),
                    "conflict_count": len(merge_metadata["conflicts"]),
                    "final_keys_count": len(merged_config),
                }
            )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "merge_configs"},
                error=f"Failed to merge configs: {str(e)}"
            )

    def _export_config_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """Export configuration to external format."""
        try:
            config_key = payload.get("config_key", "")
            export_format = payload.get("export_format", "json")  # json, yaml, env
            export_path = payload.get("export_path", "")
            include_metadata = payload.get("include_metadata", True)

            if not config_key or config_key not in self.file_configs:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "export_config"},
                    error=f"Configuration not found: {config_key}"
                )

            config_data = self.file_configs[config_key]
            export_data = {}

            if include_metadata:
                export_data = {
                    "config": config_data,
                    "metadata": {
                        "config_key": config_key,
                        "source_type": self.config_sources.get(config_key, "unknown"),
                        "version": self.config_versions.get(config_key, 0),
                        "last_updated": self.config_timestamps.get(config_key, datetime.now()).isoformat(),
                        "exported_at": datetime.now().isoformat(),
                        "export_format": export_format,
                    }
                }
            else:
                export_data = config_data

            # Export based on format
            if export_format == "json":
                export_content = json.dumps(export_data, indent=2, default=str)
                file_extension = ".json"
            elif export_format == "yaml":
                # Would need PyYAML for full implementation
                export_content = json.dumps(export_data, indent=2, default=str)
                file_extension = ".yaml"
            elif export_format == "env":
                export_content = self._convert_to_env_format(export_data)
                file_extension = ".env"
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "export_config"},
                    error=f"Unsupported export format: {export_format}"
                )

            # Write to file
            if export_path:
                export_file = Path(export_path)
            else:
                export_file = self.config_dir / f"{config_key}_export{file_extension}"

            export_file.parent.mkdir(parents=True, exist_ok=True)
            export_file.write_text(export_content)

            return ManagerResult(
                success=True,
                data={
                    "config_key": config_key,
                    "export_path": str(export_file),
                    "export_format": export_format,
                    "exported_at": datetime.now().isoformat(),
                    "file_size": len(export_content),
                },
                metrics={
                    "operation": "export_config",
                    "export_format": export_format,
                    "file_size_bytes": len(export_content),
                }
            )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "export_config"},
                error=f"Failed to export config: {str(e)}"
            )

    def _get_config_schema_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """Get configuration schema for validation."""
        try:
            config_type = payload.get("config_type", "generic")

            # Define schemas for different config types
            schemas = {
                "generic": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "version": {"type": "string"},
                        "settings": {"type": "object"},
                        "metadata": {"type": "object"},
                    }
                },
                "agent": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                        "agent_name": {"type": "string"},
                        "capabilities": {"type": "array", "items": {"type": "string"}},
                        "config": {"type": "object"},
                    },
                    "required": ["agent_id", "agent_name"]
                },
                "system": {
                    "type": "object",
                    "properties": {
                        "environment": {"type": "string"},
                        "debug_mode": {"type": "boolean"},
                        "log_level": {"type": "string"},
                        "database_url": {"type": "string"},
                        "api_keys": {"type": "object"},
                    }
                }
            }

            schema = schemas.get(config_type, schemas["generic"])

            return ManagerResult(
                success=True,
                data={
                    "config_type": config_type,
                    "schema": schema,
                    "schema_version": "1.0",
                    "generated_at": datetime.now().isoformat(),
                },
                metrics={
                    "operation": "get_config_schema",
                    "config_type": config_type,
                }
            )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "get_config_schema"},
                error=f"Failed to get config schema: {str(e)}"
            )

    def _list_configs_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """List all available configurations."""
        try:
            include_metadata = payload.get("include_metadata", True)
            filter_by_source = payload.get("filter_by_source", None)

            configs_list = []

            # Collect all configurations
            all_configs = {}

            # File configs
            for key, config in self.file_configs.items():
                if filter_by_source is None or filter_by_source == "file":
                    all_configs[f"file:{key}"] = {
                        "key": key,
                        "source": "file",
                        "data": config if not include_metadata else None,
                        "metadata": self._get_config_metadata(key) if include_metadata else None,
                    }

            # Runtime configs
            for key, config in self.runtime_configs.items():
                if filter_by_source is None or filter_by_source == "runtime":
                    all_configs[f"runtime:{key}"] = {
                        "key": key,
                        "source": "runtime",
                        "data": config if not include_metadata else None,
                        "metadata": self._get_config_metadata(key) if include_metadata else None,
                    }

            return ManagerResult(
                success=True,
                data={
                    "configs": list(all_configs.values()),
                    "total_count": len(all_configs),
                    "sources": list(set(config["source"] for config in all_configs.values())),
                    "listed_at": datetime.now().isoformat(),
                },
                metrics={
                    "operation": "list_configs",
                    "total_configs": len(all_configs),
                    "sources_count": len(set(config["source"] for config in all_configs.values())),
                }
            )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "list_configs"},
                error=f"Failed to list configs: {str(e)}"
            )

    def _delete_config_operation(self, payload: Dict[str, Any]) -> ManagerResult:
        """Delete a configuration."""
        try:
            config_key = payload.get("config_key", "")
            source_type = payload.get("source_type", "file")
            create_backup = payload.get("create_backup", True)

            if not config_key:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "delete_config"},
                    error="config_key is required"
                )

            # Create backup if requested
            if create_backup:
                self._backup_config(config_key, source_type)

            # Delete configuration
            if source_type == "file" and config_key in self.file_configs:
                del self.file_configs[config_key]
                deleted = True
            elif source_type == "runtime" and config_key in self.runtime_configs:
                del self.runtime_configs[config_key]
                deleted = True
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={"operation": "delete_config"},
                    error=f"Configuration not found: {config_key} (source: {source_type})"
                )

            # Clean up metadata
            if config_key in self.config_sources:
                del self.config_sources[config_key]
            if config_key in self.config_timestamps:
                del self.config_timestamps[config_key]
            if config_key in self.config_versions:
                del self.config_versions[config_key]

            return ManagerResult(
                success=True,
                data={
                    "config_key": config_key,
                    "source_type": source_type,
                    "deleted_at": datetime.now().isoformat(),
                    "backup_created": create_backup,
                },
                metrics={
                    "operation": "delete_config",
                    "source_type": source_type,
                    "backup_created": create_backup,
                }
            )

        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                metrics={"operation": "delete_config"},
                error=f"Failed to delete config: {str(e)}"
            )

    # Helper methods

    def _load_from_file(self, config_key: str, source_path: str = "") -> Dict[str, Any]:
        """Load configuration from file."""
        if not source_path:
            source_path = str(self.config_dir / f"{config_key}.json")

        config_file = Path(source_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_to_file(self, config_key: str, config_data: Dict[str, Any],
                     destination_path: str = "", create_backup: bool = True) -> bool:
        """Save configuration to file."""
        try:
            if not destination_path:
                destination_path = str(self.config_dir / f"{config_key}.json")

            config_file = Path(destination_path)

            # Create backup if requested and file exists
            if create_backup and config_file.exists():
                self._backup_config_file(config_file)

            # Ensure directory exists
            config_file.parent.mkdir(parents=True, exist_ok=True)

            # Save configuration
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2, default=str)

            return True

        except Exception as e:
            self.logger.error(f"Failed to save config to file: {e}")
            return False

    def _load_from_env(self, config_key: str) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config_data = {}
        prefix = f"{config_key.upper()}_"

        for env_key, env_value in os.environ.items():
            if env_key.startswith(prefix):
                config_key_clean = env_key[len(prefix):].lower()
                # Try to parse as JSON, fallback to string
                try:
                    config_data[config_key_clean] = json.loads(env_value)
                except (json.JSONDecodeError, ValueError):
                    config_data[config_key_clean] = env_value

        return config_data

    def _backup_config(self, config_key: str, source_type: str) -> None:
        """Create backup of configuration."""
        try:
            if source_type == "file" and config_key in self.file_configs:
                config_file = self.config_dir / f"{config_key}.json"
                if config_file.exists():
                    self._backup_config_file(config_file)
            # Runtime configs don't need file backup
        except Exception as e:
            self.logger.error(f"Failed to backup config {config_key}: {e}")

    def _backup_config_file(self, config_file: Path) -> None:
        """Create backup of configuration file."""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"{config_file.stem}_{timestamp}{config_file.suffix}"

            import shutil
            shutil.copy2(config_file, backup_file)

            self.logger.info(f"Config backup created: {backup_file}")

        except Exception as e:
            self.logger.error(f"Failed to backup config file {config_file}: {e}")

    def _convert_to_env_format(self, data: Dict[str, Any]) -> str:
        """Convert configuration to environment variable format."""
        lines = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{key.upper()}={json.dumps(value)}")
            else:
                lines.append(f"{key.upper()}={value}")
        return "\n".join(lines)

    def _get_config_metadata(self, config_key: str) -> Dict[str, Any]:
        """Get metadata for configuration."""
        return {
            "source_type": self.config_sources.get(config_key, "unknown"),
            "version": self.config_versions.get(config_key, 0),
            "last_updated": self.config_timestamps.get(config_key, datetime.now()).isoformat(),
            "exists": config_key in self.file_configs or config_key in self.runtime_configs,
        }

    # Public convenience methods

    def load_config(self, config_key: str, source_type: str = "file",
                   source_path: str = "", default_values: Dict[str, Any] = None) -> Dict[str, Any]:
        """Convenience method to load configuration."""
        context = ManagerContext(
            config=self.config,
            logger=self.logger,
            metrics={},
            timestamp=datetime.now()
        )

        result = self.execute(context, "load_config", {
            "config_key": config_key,
            "source_type": source_type,
            "source_path": source_path,
            "default_values": default_values or {},
        })

        return result.data.get("config_data", {}) if result.success else {}

    def save_config(self, config_key: str, config_data: Dict[str, Any],
                   destination_type: str = "file", destination_path: str = "",
                   create_backup: bool = True) -> bool:
        """Convenience method to save configuration."""
        context = ManagerContext(
            config=self.config,
            logger=self.logger,
            metrics={},
            timestamp=datetime.now()
        )

        result = self.execute(context, "save_config", {
            "config_key": config_key,
            "config_data": config_data,
            "destination_type": destination_type,
            "destination_path": destination_path,
            "create_backup": create_backup,
        })

        return result.success

    def validate_config(self, config_data: Dict[str, Any],
                       validation_rules: Dict[str, Any] = None) -> Dict[str, Any]:
        """Convenience method to validate configuration."""
        context = ManagerContext(
            config=self.config,
            logger=self.logger,
            metrics={},
            timestamp=datetime.now()
        )

        result = self.execute(context, "validate_config", {
            "config_data": config_data,
            "validation_rules": validation_rules or {},
        })

        return result.data if result.success else {"is_valid": False, "errors": [result.error]}
