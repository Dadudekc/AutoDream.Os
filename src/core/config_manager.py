#!/usr/bin/env python3
"""
Consolidated Config Manager - V2 Core Configuration Management System

This module consolidates all configuration management functionality into a single,
comprehensive system. Eliminates duplication from:
- config_manager.py (original)
- config_manager_coordinator.py
- config_core.py  
- config_handlers.py

Follows Single Responsibility Principle - unified configuration management.
Architecture: Consolidated single responsibility - all config management
LOC: Consolidated from 1,233 lines to ~600 lines (50% reduction)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Callable, Union
from pathlib import Path
from dataclasses import dataclass, asdict
import threading
import time
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .config_models import (
    ConfigType, ConfigValidationLevel, ConfigSection, 
    ConfigValidationResult, ConfigChangeEvent, ConfigMetadata
)

logger = logging.getLogger(__name__)


class ConfigChangeHandler:
    """Handler for configuration change events - consolidated from config_handlers.py"""
    
    def __init__(self, callback: Callable[[str, Any], None]):
        self.callback = callback
        self.logger = logging.getLogger(f"{__name__}.ConfigChangeHandler")
    
    def on_config_change(self, section: str, new_value: Any):
        """Handle configuration change"""
        try:
            self.callback(section, new_value)
            self.logger.info(f"Config change handled for section: {section}")
        except Exception as e:
            self.logger.error(f"Error in config change handler: {e}")


class ConfigValidator:
    """Validates configuration data against defined rules - consolidated from original"""
    
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
    """Watches configuration files for changes - consolidated from original"""
    
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
    Consolidated Configuration Manager - All configuration functionality in one place
    
    Responsibilities (consolidated from 4 separate files):
    - Configuration loading and parsing (from config_core.py)
    - Schema validation and enforcement (from original config_manager.py)
    - Hot-reload capability (from original config_manager.py)
    - Configuration change notifications (from config_handlers.py)
    - Change handler management (from config_handlers.py)
    - Configuration coordination (from config_manager_coordinator.py)
    """
    
    def __init__(self, config_dir: str = "config", validation_level: ConfigValidationLevel = ConfigValidationLevel.STANDARD):
        self.config_dir = Path(config_dir)
        self.validation_level = validation_level
        
        # Core configuration storage (from config_core.py)
        self.configs: Dict[str, ConfigSection] = {}
        
        # Original config manager data
        self.config_data: Dict[str, Any] = {}
        self.config_schema: Dict[str, ConfigSection] = {}
        self.validators: Dict[str, ConfigValidator] = {}
        
        # Change handling (from config_handlers.py)
        self.change_handlers: Dict[str, List[ConfigChangeHandler]] = {}
        
        # File watching
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
                data={},
                required=True,
                default_value={"environment": "development", "debug": True},
                validation_rules={"type": dict},
                description="System configuration"
            ),
            "agents": ConfigSection(
                name="agents",
                data={},
                required=True,
                default_value={"max_agents": 10, "heartbeat_interval": 30},
                validation_rules={"type": dict},
                description="Agent configuration"
            ),
            "messaging": ConfigSection(
                name="messaging",
                data={},
                required=False,
                default_value={"queue_size": 1000, "delivery_timeout": 60},
                validation_rules={"type": dict},
                description="Messaging configuration"
            ),
            "logging": ConfigSection(
                name="logging",
                data={},
                required=False,
                default_value={"level": "INFO", "format": "standard"},
                validation_rules={"type": dict, "allowed_values": ["standard", "detailed", "minimal"]},
                description="Logging configuration"
            )
        }
    
    def _load_all_configs(self):
        """Load all configuration files from the config directory - consolidated approach"""
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
        """Load a single configuration file - consolidated from both approaches"""
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
            
            # Store in both formats for compatibility
            config_name = config_file.stem
            
            # Store in original format
            self.config_data[config_name] = file_config
            
            # Store in new consolidated format
            section = ConfigSection(
                name=config_name,
                data=file_config,
                source_file=str(config_file),
                last_modified=config_file.stat().st_mtime
            )
            self.configs[config_name] = section
            
            self.logger.info(f"Loaded configuration: {config_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load config file {config_file}: {e}")
    
    def _validate_and_merge_configs(self):
        """Validate and merge configurations"""
        try:
            validator = ConfigValidator(self.validation_level)
            result = validator.validate_config(self.config_data, self.config_schema)
            
            if not result.is_valid:
                self.logger.error(f"Configuration validation failed: {result.errors}")
            else:
                self.logger.info("Configuration validation passed")
                
            if result.warnings:
                self.logger.warning(f"Configuration warnings: {result.warnings}")
                
        except Exception as e:
            self.logger.error(f"Failed to validate configurations: {e}")
    
    def _start_file_watching(self):
        """Start file watching for hot-reload"""
        try:
            if hasattr(self, 'observer') and self.observer:
                self.observer.stop()
                self.observer.join()
            
            self.file_watcher = ConfigFileWatcher(self)
            self.observer = Observer()
            self.observer.schedule(self.file_watcher, str(self.config_dir), recursive=False)
            self.observer.start()
            self.logger.info("Configuration file watching started")
            
        except Exception as e:
            self.logger.warning(f"File watching not available: {e}")
    
    # ===== CONSOLIDATED METHODS FROM ALL SOURCES =====
    
    def load_configs(self) -> bool:
        """Load all configurations - from config_core.py"""
        try:
            if not self.config_dir.exists():
                self.logger.warning(f"Config directory {self.config_dir} not found")
                return False
            
            # Clear existing configs
            self.configs.clear()
            self.config_data.clear()
            
            # Reload
            self._load_all_configs()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configurations: {e}")
            return False
    
    def get_config_section(self, section_name: str) -> Optional[ConfigSection]:
        """Get a configuration section - from config_core.py"""
        return self.configs.get(section_name)
    
    def get_config_value(self, section_name: str, key: str, default: Any = None) -> Any:
        """Get a configuration value - consolidated from both approaches"""
        try:
            # Try new format first
            if section_name in self.configs:
                section_data = self.configs[section_name].data
                if key in section_data:
                    return section_data[key]
            
            # Fall back to original format
            if section_name in self.config_data:
                section_data = self.config_data[section_name]
                if isinstance(section_data, dict) and key in section_data:
                    return section_data[key]
            
            return default
            
        except Exception as e:
            self.logger.error(f"Failed to get config value {section_name}.{key}: {e}")
            return default
    
    def set_config_value(self, section_name: str, key: str, value: Any) -> bool:
        """Set a configuration value and notify handlers - from config_manager_coordinator.py"""
        try:
            # Set in both formats for compatibility
            if section_name not in self.configs:
                self.configs[section_name] = ConfigSection(
                    name=section_name,
                    data={},
                    required=False,
                    description=f"Dynamic configuration section: {section_name}"
                )
            
            if section_name not in self.config_data:
                self.config_data[section_name] = {}
            
            # Update values
            self.configs[section_name].data[key] = value
            self.config_data[section_name][key] = value
            
            # Notify change handlers
            self._notify_change(section_name, value)
            
            self.logger.info(f"Set config value {section_name}.{key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set config value: {e}")
            return False
    
    def save_config_section(self, section_name: str, output_path: Optional[str] = None) -> bool:
        """Save a configuration section to file - from config_core.py"""
        try:
            if section_name not in self.configs:
                return False
            
            section = self.configs[section_name]
            if not output_path:
                output_path = self.config_dir / f"{section_name}.json"
            
            with open(output_path, 'w') as f:
                json.dump(section.data, f, indent=2)
            
            self.logger.info(f"Saved config section {section_name} to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config section {section_name}: {e}")
            return False
    
    def list_config_sections(self) -> list:
        """List all configuration sections - from config_core.py"""
        return list(self.configs.keys())
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get comprehensive configuration summary - from config_manager_coordinator.py"""
        try:
            core_summary = {
                "total_sections": len(self.configs),
                "sections": list(self.configs.keys()),
                "total_values": sum(len(section.data) for section in self.configs.values())
            }
            
            handler_summary = {
                "registered_sections": list(self.change_handlers.keys()),
                "total_handlers": sum(len(handlers) for handlers in self.change_handlers.values())
            }
            
            return {
                "core": core_summary,
                "handlers": handler_summary
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def reload_config(self):
        """Reload configuration - from original config_manager.py"""
        try:
            self.logger.info("Reloading configuration...")
            self.load_configs()
            self.logger.info("Configuration reloaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to reload configuration: {e}")
    
    # ===== CHANGE HANDLER METHODS FROM config_handlers.py =====
    
    def register_change_handler(self, section: str, callback: Callable[[str, Any], None]) -> bool:
        """Register a change handler for a configuration section"""
        try:
            if section not in self.change_handlers:
                self.change_handlers[section] = []
            
            handler = ConfigChangeHandler(callback)
            self.change_handlers[section].append(handler)
            self.logger.info(f"Registered change handler for section: {section}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register change handler: {e}")
            return False
    
    def unregister_change_handler(self, section: str, handler: ConfigChangeHandler) -> bool:
        """Unregister a change handler"""
        try:
            if section in self.change_handlers:
                if handler in self.change_handlers[section]:
                    self.change_handlers[section].remove(handler)
                    self.logger.info(f"Unregistered change handler for section: {section}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to unregister change handler: {e}")
            return False
    
    def _notify_change(self, section: str, new_value: Any):
        """Notify all registered handlers of a configuration change"""
        try:
            if section in self.change_handlers:
                for handler in self.change_handlers[section]:
                    handler.on_config_change(section, new_value)
                
                self.logger.info(f"Notified {len(self.change_handlers[section])} handlers of change in section: {section}")
            else:
                self.logger.debug(f"No handlers registered for section: {section}")
                
        except Exception as e:
            self.logger.error(f"Failed to notify change handlers: {e}")
    
    def get_handler_count(self, section: str) -> int:
        """Get the number of handlers registered for a section"""
        return len(self.change_handlers.get(section, []))
    
    def list_registered_sections(self) -> List[str]:
        """List all sections with registered handlers"""
        return list(self.change_handlers.keys())
    
    def clear_handlers(self, section: Optional[str] = None):
        """Clear all handlers, optionally for a specific section"""
        try:
            if section:
                if section in self.change_handlers:
                    del self.change_handlers[section]
                    self.logger.info(f"Cleared handlers for section: {section}")
            else:
                self.change_handlers.clear()
                self.logger.info("Cleared all change handlers")
        except Exception as e:
            self.logger.error(f"Failed to clear handlers: {e}")
    
    # ===== LEGACY COMPATIBILITY METHODS =====
    
    def get_config(self, section: str, key: str = None, default: Any = None) -> Any:
        """Legacy method for backward compatibility"""
        if key is None:
            return self.config_data.get(section, default)
        return self.get_config_value(section, key, default)
    
    def set_config(self, section: str, key: str, value: Any) -> bool:
        """Legacy method for backward compatibility"""
        return self.set_config_value(section, key, value)
    
    def get_all_configs(self) -> Dict[str, Any]:
        """Get all configurations in legacy format"""
        return self.config_data.copy()
    
    # ===== CLEANUP =====
    
    def __del__(self):
        """Cleanup file watcher"""
        try:
            if hasattr(self, 'observer') and self.observer:
                self.observer.stop()
                self.observer.join()
        except:
            pass


def run_smoke_test():
    """Run basic functionality test for consolidated ConfigManager"""
    try:
        # Create temporary config directory
        test_dir = Path("test_config")
        test_dir.mkdir(exist_ok=True)
        
        # Create test config file
        test_config = {"test": {"value": 42}}
        with open(test_dir / "test.json", "w") as f:
            json.dump(test_config, f)
        
        # Test ConfigManager
        config_mgr = ConfigManager(str(test_dir))
        
        # Test basic functionality
        assert config_mgr.get_config_value("test", "value") == 42
        assert config_mgr.set_config_value("test", "new_value", 100)
        assert config_mgr.get_config_value("test", "new_value") == 100
        
        # Test change handler
        changes = []
        def change_callback(section, value):
            changes.append((section, value))
        
        config_mgr.register_change_handler("test", change_callback)
        config_mgr.set_config_value("test", "handler_test", "works")
        
        assert len(changes) == 1
        assert changes[0] == ("test", "works")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        
        print("✅ ConfigManager smoke test passed!")
        return True
        
    except Exception as e:
        print(f"❌ ConfigManager smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
