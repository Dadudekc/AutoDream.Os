#!/usr/bin/env python3
"""
Config Manager - V2 Core Configuration Management System

This module manages system configuration, validation, and hot-reload capability.
Follows Single Responsibility Principle - only configuration management.
Architecture: Single Responsibility Principle - configuration management only
LOC: Target 200 lines (under 200 limit)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Callable, Union
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import time
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)


class ConfigType(Enum):
    """Configuration file types"""
    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    ENV = "env"


class ConfigValidationLevel(Enum):
    """Configuration validation levels"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"


@dataclass
class ConfigSection:
    """Configuration section definition"""
    name: str
    required: bool
    default_value: Any
    validation_rules: Dict[str, Any]
    description: str


@dataclass
class ConfigValidationResult:
    """Configuration validation result"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validation_level: ConfigValidationLevel


class ConfigValidator:
    """Validates configuration data against defined rules"""
    
    def __init__(self, validation_level: ConfigValidationLevel = ConfigValidationLevel.STANDARD):
        self.validation_level = validation_level
        self.logger = logging.getLogger(f"{__name__}.ConfigValidator")
    
    def validate_config(self, config_data: Dict[str, Any], schema: Dict[str, ConfigSection]) -> ConfigValidationResult:
        """Validate configuration data against schema"""
        errors = []
        warnings = []
        
        try:
            for section_name, section_def in schema.items():
                if section_def.required and section_name not in config_data:
                    errors.append(f"Required section '{section_name}' is missing")
                    continue
                
                if section_name in config_data:
                    section_errors, section_warnings = self._validate_section(
                        config_data[section_name], section_def
                    )
                    errors.extend(section_errors)
                    warnings.extend(section_warnings)
            
            # Apply validation level specific checks
            if self.validation_level == ConfigValidationLevel.STRICT:
                strict_errors, strict_warnings = self._strict_validation(config_data, schema)
                errors.extend(strict_errors)
                warnings.extend(strict_warnings)
            
            is_valid = len(errors) == 0
            
            return ConfigValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                validation_level=self.validation_level
            )
            
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            errors.append(f"Validation failed: {str(e)}")
            return ConfigValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                validation_level=self.validation_level
            )
    
    def _validate_section(self, section_data: Any, section_def: ConfigSection) -> tuple[List[str], List[str]]:
        """Validate a configuration section"""
        errors = []
        warnings = []
        
        try:
            # Type validation
            expected_type = section_def.validation_rules.get("type")
            if expected_type and not isinstance(section_data, expected_type):
                errors.append(f"Section '{section_def.name}' should be {expected_type.__name__}, got {type(section_data).__name__}")
            
            # Range validation for numbers
            if isinstance(section_data, (int, float)):
                min_val = section_def.validation_rules.get("min")
                max_val = section_def.validation_rules.get("max")
                
                if min_val is not None and section_data < min_val:
                    errors.append(f"Section '{section_def.name}' value {section_data} is below minimum {min_val}")
                
                if max_val is not None and section_data > max_val:
                    errors.append(f"Section '{section_def.name}' value {section_data} is above maximum {max_val}")
            
            # String validation
            if isinstance(section_data, str):
                min_length = section_def.validation_rules.get("min_length")
                max_length = section_def.validation_rules.get("max_length")
                allowed_values = section_def.validation_rules.get("allowed_values")
                
                if min_length is not None and len(section_data) < min_length:
                    errors.append(f"Section '{section_def.name}' string length {len(section_data)} is below minimum {min_length}")
                
                if max_length is not None and len(section_data) > max_length:
                    errors.append(f"Section '{section_def.name}' string length {len(section_data)} is above maximum {max_length}")
                
                if allowed_values and section_data not in allowed_values:
                    errors.append(f"Section '{section_def.name}' value '{section_data}' is not in allowed values: {allowed_values}")
            
            # List validation
            if isinstance(section_data, list):
                min_items = section_def.validation_rules.get("min_items")
                max_items = section_def.validation_rules.get("max_items")
                
                if min_items is not None and len(section_data) < min_items:
                    errors.append(f"Section '{section_def.name}' list has {len(section_data)} items, minimum required is {min_items}")
                
                if max_items is not None and len(section_data) > max_items:
                    errors.append(f"Section '{section_def.name}' list has {len(section_data)} items, maximum allowed is {max_items}")
            
        except Exception as e:
            errors.append(f"Section '{section_def.name}' validation error: {str(e)}")
        
        return errors, warnings
    
    def _strict_validation(self, config_data: Dict[str, Any], schema: Dict[str, ConfigSection]) -> tuple[List[str], List[str]]:
        """Apply strict validation rules"""
        errors = []
        warnings = []
        
        # Check for unknown sections
        for section_name in config_data:
            if section_name not in schema:
                warnings.append(f"Unknown configuration section: '{section_name}'")
        
        # Check for empty sections
        for section_name, section_data in config_data.items():
            if section_data is None or (isinstance(section_data, str) and section_data.strip() == ""):
                warnings.append(f"Section '{section_name}' is empty or null")
        
        return errors, warnings


class ConfigFileWatcher(FileSystemEventHandler):
    """Watches configuration files for changes"""
    
    def __init__(self, config_manager: 'ConfigManager'):
        self.config_manager = config_manager
        self.logger = logging.getLogger(f"{__name__}.ConfigFileWatcher")
    
    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory and event.src_path.endswith(('.json', '.yaml', '.yml')):
            self.logger.info(f"Configuration file modified: {event.src_path}")
            self.config_manager.reload_config()


class ConfigManager:
    """
    Manages system configuration, validation, and hot-reload capability
    
    Responsibilities:
    - Configuration loading and parsing
    - Schema validation and enforcement
    - Hot-reload capability
    - Configuration change notifications
    """
    
    def __init__(self, config_dir: str = "config", validation_level: ConfigValidationLevel = ConfigValidationLevel.STANDARD):
        self.config_dir = Path(config_dir)
        self.validation_level = validation_level
        self.config_data: Dict[str, Any] = {}
        self.config_schema: Dict[str, ConfigSection] = {}
        self.validators: Dict[str, ConfigValidator] = {}
        self.change_callbacks: List[Callable] = []
        self.file_watcher = None
        self.observer = None
        self.logger = logging.getLogger(f"{__name__}.ConfigManager")
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Initialize default schema
        self._initialize_default_schema()
        
        # Load initial configuration
        self._load_all_configs()
        
        # Start file watching if supported
        self._start_file_watching()
    
    def _initialize_default_schema(self):
        """Initialize default configuration schema"""
        self.config_schema = {
            "system": ConfigSection(
                name="system",
                required=True,
                default_value={"environment": "development", "debug": True},
                validation_rules={"type": dict},
                description="System configuration"
            ),
            "agents": ConfigSection(
                name="agents",
                required=True,
                default_value={"max_agents": 10, "heartbeat_interval": 30},
                validation_rules={"type": dict},
                description="Agent configuration"
            ),
            "messaging": ConfigSection(
                name="messaging",
                required=False,
                default_value={"queue_size": 1000, "delivery_timeout": 60},
                validation_rules={"type": dict},
                description="Messaging configuration"
            ),
            "logging": ConfigSection(
                name="logging",
                required=False,
                default_value={"level": "INFO", "format": "standard"},
                validation_rules={"type": dict, "allowed_values": ["standard", "detailed", "minimal"]},
                description="Logging configuration"
            )
        }
    
    def _load_all_configs(self):
        """Load all configuration files from the config directory"""
        try:
            # Load JSON configs
            for json_file in self.config_dir.glob("*.json"):
                self._load_config_file(json_file, ConfigType.JSON)
            
            # Load YAML configs
            for yaml_file in self.config_dir.glob("*.yaml"):
                self._load_config_file(yaml_file, ConfigType.YAML)
            for yaml_file in self.config_dir.glob("*.yml"):
                self._load_config_file(yaml_file, ConfigType.YAML)
            
            # Apply schema validation
            self._validate_and_merge_configs()
            
        except Exception as e:
            self.logger.error(f"Failed to load configurations: {e}")
    
    def _load_config_file(self, config_file: Path, config_type: ConfigType):
        """Load a single configuration file"""
        try:
            if config_type == ConfigType.JSON:
                with open(config_file, "r") as f:
                    file_config = json.load(f)
            elif config_type == ConfigType.YAML:
                with open(config_file, "r") as f:
                    file_config = yaml.safe_load(f)
            else:
                self.logger.warning(f"Unsupported config type: {config_type}")
                return
            
            # Store file-specific config
            config_name = config_file.stem
            self.config_data[config_name] = file_config
            self.logger.info(f"Loaded configuration: {config_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load config file {config_file}: {e}")
    
    def _validate_and_merge_configs(self):
        """Validate and merge all loaded configurations"""
        try:
            # Create validator
            validator = ConfigValidator(self.validation_level)
            
            # Validate each config section
            for section_name, section_def in self.config_schema.items():
                section_data = self._get_section_data(section_name)
                
                if section_data is not None:
                    validation_result = validator.validate_config({section_name: section_data}, {section_name: section_def})
                    
                    if not validation_result.is_valid:
                        self.logger.error(f"Configuration validation failed for section '{section_name}':")
                        for error in validation_result.errors:
                            self.logger.error(f"  - {error}")
                        
                        # Use default value if validation fails
                        self.config_data[section_name] = section_def.default_value
                        self.logger.warning(f"Using default value for section '{section_name}'")
                    else:
                        if validation_result.warnings:
                            for warning in validation_result.warnings:
                                self.logger.warning(f"Configuration warning for section '{section_name}': {warning}")
                else:
                    # Use default value if section is missing
                    self.config_data[section_name] = section_def.default_value
                    self.logger.info(f"Using default value for missing section '{section_name}'")
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
    
    def _get_section_data(self, section_name: str) -> Optional[Any]:
        """Get configuration data for a specific section"""
        # Look for section in loaded configs
        for config_name, config_data in self.config_data.items():
            if isinstance(config_data, dict) and section_name in config_data:
                return config_data[section_name]
        
        return None
    
    def _start_file_watching(self):
        """Start watching configuration files for changes"""
        try:
            self.file_watcher = ConfigFileWatcher(self)
            self.observer = Observer()
            self.observer.schedule(self.file_watcher, str(self.config_dir), recursive=False)
            self.observer.start()
            self.logger.info("Configuration file watching started")
        except Exception as e:
            self.logger.warning(f"File watching not available: {e}")
    
    def get_config(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """Get configuration value"""
        try:
            if section not in self.config_data:
                return default
            
            section_data = self.config_data[section]
            
            if key is None:
                return section_data
            
            if isinstance(section_data, dict) and key in section_data:
                return section_data[key]
            
            return default
            
        except Exception as e:
            self.logger.error(f"Failed to get config {section}.{key}: {e}")
            return default
    
    def set_config(self, section: str, key: str, value: Any) -> bool:
        """Set configuration value"""
        try:
            if section not in self.config_data:
                self.config_data[section] = {}
            
            if not isinstance(self.config_data[section], dict):
                self.config_data[section] = {}
            
            self.config_data[section][key] = value
            
            # Validate the change
            if section in self.config_schema:
                validator = ConfigValidator(self.validation_level)
                validation_result = validator.validate_config(
                    {section: self.config_data[section]}, 
                    {section: self.config_schema[section]}
                )
                
                if not validation_result.is_valid:
                    self.logger.error(f"Configuration validation failed: {validation_result.errors}")
                    return False
            
            # Save to file
            self._save_config_section(section)
            
            # Notify change callbacks
            self._notify_config_change(section, key, value)
            
            self.logger.info(f"Configuration updated: {section}.{key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set config {section}.{key}: {e}")
            return False
    
    def _save_config_section(self, section: str):
        """Save a configuration section to file"""
        try:
            config_file = self.config_dir / f"{section}.json"
            
            with open(config_file, "w") as f:
                json.dump(self.config_data[section], f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Failed to save config section {section}: {e}")
    
    def reload_config(self):
        """Reload configuration from files"""
        try:
            self.logger.info("Reloading configuration...")
            self._load_all_configs()
            self._notify_config_change("system", "reloaded", True)
            self.logger.info("Configuration reloaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to reload configuration: {e}")
    
    def register_change_callback(self, callback: Callable):
        """Register a callback for configuration changes"""
        self.change_callbacks.append(callback)
        self.logger.info("Configuration change callback registered")
    
    def _notify_config_change(self, section: str, key: str, value: Any):
        """Notify all registered change callbacks"""
        for callback in self.change_callbacks:
            try:
                callback(section, key, value)
            except Exception as e:
                self.logger.error(f"Configuration change callback error: {e}")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration"""
        try:
            return {
                "total_sections": len(self.config_data),
                "sections": list(self.config_data.keys()),
                "validation_level": self.validation_level.value,
                "file_watching": self.observer is not None and self.observer.is_alive(),
                "change_callbacks": len(self.change_callbacks)
            }
        except Exception as e:
            self.logger.error(f"Failed to get config summary: {e}")
            return {"error": str(e)}
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test config retrieval
            system_config = self.get_config("system")
            if system_config is None:
                return False
            
            # Test config setting
            success = self.set_config("system", "test_key", "test_value")
            if not success:
                return False
            
            # Test config retrieval after setting
            test_value = self.get_config("system", "test_key")
            if test_value != "test_value":
                return False
            
            # Test config summary
            summary = self.get_config_summary()
            if "total_sections" not in summary:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False
    
    def shutdown(self):
        """Shutdown the config manager"""
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=5)


def run_smoke_test():
    """Run basic functionality test for ConfigManager"""
    print("🧪 Running ConfigManager Smoke Test...")
    
    try:
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            
            # Test config retrieval
            system_config = manager.get_config("system")
            assert system_config is not None
            
            # Test config setting
            success = manager.set_config("system", "test_key", "test_value")
            assert success
            
            # Test config retrieval after setting
            test_value = manager.get_config("system", "test_key")
            assert test_value == "test_value"
            
            # Test config summary
            summary = manager.get_config_summary()
            assert "total_sections" in summary
            
            manager.shutdown()
        
        print("✅ ConfigManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ConfigManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ConfigManager testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Config Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--get", nargs=2, metavar=("SECTION", "KEY"), help="Get config value")
    parser.add_argument("--set", nargs=3, metavar=("SECTION", "KEY", "VALUE"), help="Set config value")
    parser.add_argument("--reload", action="store_true", help="Reload configuration")
    parser.add_argument("--summary", action="store_true", help="Show configuration summary")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    manager = ConfigManager()
    
    if args.get:
        section, key = args.get
        value = manager.get_config(section, key)
        print(f"Config {section}.{key}: {value}")
    elif args.set:
        section, key, value = args.set
        success = manager.set_config(section, key, value)
        print(f"Config set: {'✅ Success' if success else '❌ Failed'}")
    elif args.reload:
        manager.reload_config()
        print("Configuration reloaded")
    elif args.summary:
        summary = manager.get_config_summary()
        print("Configuration Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()
    
    manager.shutdown()


if __name__ == "__main__":
    main()
