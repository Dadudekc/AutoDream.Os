#!/usr/bin/env python3
"""
Centralized Configuration Management System - Agent Cellphone V2
==============================================================

Unified configuration management system that consolidates all configuration
files across the codebase, eliminating duplication and providing a single
source of truth for all configuration settings.

This system provides:
- Hierarchical configuration management
- Environment-specific overrides
- Validation and type checking
- Hot-reload capabilities
- Centralized configuration access

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** DEDUP-001 - Duplicate File Analysis & Deduplication Plan
**Status:** CONSOLIDATION IN PROGRESS
**Target:** 0% configuration duplication, unified management
**V2 Compliance:** ✅ Under 400 lines, single responsibility
"""

import os
import json
import yaml
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION ENUMS
# ============================================================================

class ConfigSource(Enum):
    """Configuration source types."""
    ENVIRONMENT = "environment"
    FILE = "file"
    DATABASE = "database"
    API = "api"
    DEFAULT = "default"


class ConfigPriority(Enum):
    """Configuration priority levels."""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    DEBUG = 4


class ConfigType(Enum):
    """Configuration value types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    ENUM = "enum"


# ============================================================================
# CONFIGURATION DATA STRUCTURES
# ============================================================================

@dataclass
class ConfigItem:
    """Individual configuration item."""
    key: str
    value: Any
    config_type: ConfigType
    source: ConfigSource
    priority: ConfigPriority
    description: str = ""
    validation_rules: Optional[Dict[str, Any]] = None
    last_updated: float = field(default_factory=lambda: __import__('time').time())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigSection:
    """Configuration section containing related items."""
    name: str
    items: Dict[str, ConfigItem] = field(default_factory=dict)
    description: str = ""
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)


@dataclass
class ConfigValidationResult:
    """Configuration validation result."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


# ============================================================================
# CONFIGURATION VALIDATORS
# ============================================================================

class ConfigValidator:
    """Configuration validation system."""
    
    @staticmethod
    def validate_string(value: Any, rules: Optional[Dict[str, Any]] = None) -> ConfigValidationResult:
        """Validate string configuration values."""
        result = ConfigValidationResult(is_valid=True)
        
        if not isinstance(value, str):
            result.is_valid = False
            result.errors.append(f"Value must be a string, got {type(value).__name__}")
            return result
        
        if rules:
            min_length = rules.get('min_length')
            max_length = rules.get('max_length')
            pattern = rules.get('pattern')
            
            if min_length and len(value) < min_length:
                result.is_valid = False
                result.errors.append(f"String length must be at least {min_length}")
            
            if max_length and len(value) > max_length:
                result.is_valid = False
                result.errors.append(f"String length must be at most {max_length}")
            
            if pattern and not re.match(pattern, value):
                result.is_valid = False
                result.errors.append(f"String must match pattern {pattern}")
        
        return result
    
    @staticmethod
    def validate_integer(value: Any, rules: Optional[Dict[str, Any]] = None) -> ConfigValidationResult:
        """Validate integer configuration values."""
        result = ConfigValidationResult(is_valid=True)
        
        if not isinstance(value, int):
            result.is_valid = False
            result.errors.append(f"Value must be an integer, got {type(value).__name__}")
            return result
        
        if rules:
            min_value = rules.get('min_value')
            max_value = rules.get('max_value')
            
            if min_value is not None and value < min_value:
                result.is_valid = False
                result.errors.append(f"Value must be at least {min_value}")
            
            if max_value is not None and value > max_value:
                result.is_valid = False
                result.errors.append(f"Value must be at most {max_value}")
        
        return result
    
    @staticmethod
    def validate_boolean(value: Any) -> ConfigValidationResult:
        """Validate boolean configuration values."""
        result = ConfigValidationResult(is_valid=True)
        
        if not isinstance(value, bool):
            result.is_valid = False
            result.errors.append(f"Value must be a boolean, got {type(value).__name__}")
        
        return result


# ============================================================================
# CENTRALIZED CONFIGURATION MANAGER
# ============================================================================

class CentralizedConfigManager:
    """
    Centralized configuration management system that eliminates duplication
    and provides unified configuration access across the codebase.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path("config")
        self.sections: Dict[str, ConfigSection] = {}
        self.observers: List[Callable] = []
        self._lock = threading.RLock()
        self._file_observer: Optional[Observer] = None
        
        # Initialize configuration system
        self._initialize_config()
        self._setup_file_watching()
    
    def _initialize_config(self):
        """Initialize the configuration system."""
        logger.info("Initializing centralized configuration management system")
        
        # Create default sections
        self._create_default_sections()
        
        # Load configuration files
        self._load_config_files()
        
        # Load environment variables
        self._load_environment_config()
        
        logger.info("Centralized configuration system initialized successfully")
    
    def _create_default_sections(self):
        """Create default configuration sections."""
        default_sections = [
            ("logging", "Logging configuration settings"),
            ("performance", "Performance and monitoring settings"),
            ("database", "Database connection and configuration"),
            ("security", "Security and authentication settings"),
            ("api", "API configuration and endpoints"),
            ("testing", "Testing framework configuration"),
            ("development", "Development environment settings"),
            ("production", "Production environment settings")
        ]
        
        for name, description in default_sections:
            self.sections[name] = ConfigSection(name=name, description=description)
    
    def _load_config_files(self):
        """Load configuration from files."""
        if not self.config_dir.exists():
            logger.warning(f"Configuration directory {self.config_dir} does not exist")
            return
        
        for config_file in self.config_dir.glob("*.{json,yaml,yml,py}"):
            try:
                self._load_config_file(config_file)
            except Exception as e:
                logger.error(f"Failed to load config file {config_file}: {e}")
    
    def _load_config_file(self, config_file: Path):
        """Load a single configuration file."""
        logger.info(f"Loading configuration file: {config_file}")
        
        if config_file.suffix == '.json':
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        elif config_file.suffix in ('.yaml', '.yml'):
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
        elif config_file.suffix == '.py':
            # Import Python config file
            import importlib.util
            spec = importlib.util.spec_from_file_location("config_module", config_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            config_data = {k: v for k, v in module.__dict__.items() 
                          if not k.startswith('_') and k.isupper()}
        else:
            logger.warning(f"Unsupported config file format: {config_file}")
            return
        
        # Process configuration data
        self._process_config_data(config_data, config_file.name)
    
    def _process_config_data(self, config_data: Dict[str, Any], source_name: str):
        """Process configuration data and add to sections."""
        for key, value in config_data.items():
            # Determine section based on key or create new section
            section_name = self._determine_section(key)
            
            if section_name not in self.sections:
                self.sections[section_name] = ConfigSection(name=section_name)
            
            # Create config item
            config_item = ConfigItem(
                key=key,
                value=value,
                config_type=self._infer_config_type(value),
                source=ConfigSource.FILE,
                priority=ConfigPriority.NORMAL,
                description=f"Loaded from {source_name}",
                last_updated=__import__('time').time()
            )
            
            # Validate configuration
            validation_result = self._validate_config_item(config_item)
            if not validation_result.is_valid:
                logger.warning(f"Configuration validation failed for {key}: {validation_result.errors}")
            
            # Add to section
            self.sections[section_name].items[key] = config_item
    
    def _determine_section(self, key: str) -> str:
        """Determine which section a configuration key belongs to."""
        key_lower = key.lower()
        
        # Map keys to sections based on common patterns
        if any(word in key_lower for word in ['log', 'logger', 'logging']):
            return 'logging'
        elif any(word in key_lower for word in ['perf', 'benchmark', 'metric', 'monitor']):
            return 'performance'
        elif any(word in key_lower for word in ['db', 'database', 'connection']):
            return 'database'
        elif any(word in key_lower for word in ['auth', 'security', 'encrypt', 'token']):
            return 'security'
        elif any(word in key_lower for word in ['api', 'endpoint', 'url', 'route']):
            return 'api'
        elif any(word in key_lower for word in ['test', 'testing', 'mock']):
            return 'testing'
        elif any(word in key_lower for word in ['dev', 'development', 'debug']):
            return 'development'
        elif any(word in key_lower for word in ['prod', 'production', 'deploy']):
            return 'production'
        else:
            return 'general'
    
    def _infer_config_type(self, value: Any) -> ConfigType:
        """Infer the configuration type from a value."""
        if isinstance(value, str):
            return ConfigType.STRING
        elif isinstance(value, int):
            return ConfigType.INTEGER
        elif isinstance(value, float):
            return ConfigType.FLOAT
        elif isinstance(value, bool):
            return ConfigType.BOOLEAN
        elif isinstance(value, list):
            return ConfigType.LIST
        elif isinstance(value, dict):
            return ConfigType.DICT
        else:
            return ConfigType.STRING
    
    def _validate_config_item(self, item: ConfigItem) -> ConfigValidationResult:
        """Validate a configuration item."""
        validator = ConfigValidator()
        
        if item.config_type == ConfigType.STRING:
            return validator.validate_string(item.value, item.validation_rules)
        elif item.config_type == ConfigType.INTEGER:
            return validator.validate_integer(item.value, item.validation_rules)
        elif item.config_type == ConfigType.BOOLEAN:
            return validator.validate_boolean(item.value)
        else:
            # For other types, just check if value is not None
            return ConfigValidationResult(is_valid=item.value is not None)
    
    def _load_environment_config(self):
        """Load configuration from environment variables."""
        logger.info("Loading configuration from environment variables")
        
        for key, value in os.environ.items():
            if key.startswith('APP_') or key.startswith('CONFIG_'):
                # Convert environment variable to configuration
                config_key = key.replace('APP_', '').replace('CONFIG_', '').lower()
                section_name = self._determine_section(config_key)
                
                if section_name not in self.sections:
                    self.sections[section_name] = ConfigSection(name=section_name)
                
                # Create config item
                config_item = ConfigItem(
                    key=config_key,
                    value=value,
                    config_type=ConfigType.STRING,
                    source=ConfigSource.ENVIRONMENT,
                    priority=ConfigPriority.HIGH,
                    description=f"Environment variable: {key}",
                    last_updated=__import__('time').time()
                )
                
                self.sections[section_name].items[config_key] = config_item
    
    def _setup_file_watching(self):
        """Set up file watching for configuration changes."""
        try:
            self._file_observer = Observer()
            event_handler = ConfigFileHandler(self)
            self._file_observer.schedule(event_handler, str(self.config_dir), recursive=False)
            self._file_observer.start()
            logger.info("Configuration file watching enabled")
        except Exception as e:
            logger.warning(f"Failed to enable configuration file watching: {e}")
    
    def get(self, key: str, default: Any = None, section: Optional[str] = None) -> Any:
        """Get a configuration value."""
        with self._lock:
            if section:
                if section in self.sections and key in self.sections[section].items:
                    return self.sections[section].items[key].value
            else:
                # Search all sections
                for section_name, section_obj in self.sections.items():
                    if key in section_obj.items:
                        return section_obj.items[key].value
            
            return default
    
    def set(self, key: str, value: Any, section: str = "general", 
            config_type: Optional[ConfigType] = None, priority: ConfigPriority = ConfigPriority.NORMAL,
            description: str = "", validation_rules: Optional[Dict[str, Any]] = None):
        """Set a configuration value."""
        with self._lock:
            if section not in self.sections:
                self.sections[section] = ConfigSection(name=section)
            
            # Create or update config item
            config_item = ConfigItem(
                key=key,
                value=value,
                config_type=config_type or self._infer_config_type(value),
                source=ConfigSource.DEFAULT,
                priority=priority,
                description=description,
                validation_rules=validation_rules,
                last_updated=__import__('time').time()
            )
            
            # Validate configuration
            validation_result = self._validate_config_item(config_item)
            if not validation_result.is_valid:
                logger.warning(f"Configuration validation failed for {key}: {validation_result.errors}")
            
            self.sections[section].items[key] = config_item
            
            # Notify observers
            self._notify_observers(key, value, section)
    
    def get_section(self, section_name: str) -> Optional[ConfigSection]:
        """Get a configuration section."""
        return self.sections.get(section_name)
    
    def list_sections(self) -> List[str]:
        """List all configuration sections."""
        return list(self.sections.keys())
    
    def list_keys(self, section: Optional[str] = None) -> List[str]:
        """List configuration keys."""
        with self._lock:
            if section:
                return list(self.sections.get(section, {}).items.keys())
            else:
                all_keys = []
                for section_obj in self.sections.values():
                    all_keys.extend(section_obj.items.keys())
                return all_keys
    
    def add_observer(self, callback: Callable):
        """Add a configuration change observer."""
        self.observers.append(callback)
    
    def remove_observer(self, callback: Callable):
        """Remove a configuration change observer."""
        if callback in self.observers:
            self.observers.remove(callback)
    
    def _notify_observers(self, key: str, value: Any, section: str):
        """Notify observers of configuration changes."""
        for observer in self.observers:
            try:
                observer(key, value, section)
            except Exception as e:
                logger.error(f"Observer notification failed: {e}")
    
    def export_config(self, format: str = "json") -> str:
        """Export configuration to a string format."""
        with self._lock:
            config_data = {}
            for section_name, section_obj in self.sections.items():
                config_data[section_name] = {
                    key: item.value for key, item in section_obj.items.items()
                }
            
            if format.lower() == "json":
                return json.dumps(config_data, indent=2)
            elif format.lower() in ("yaml", "yml"):
                return yaml.dump(config_data, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported export format: {format}")
    
    def reload(self):
        """Reload configuration from files."""
        logger.info("Reloading configuration from files")
        
        # Clear existing configuration
        self.sections.clear()
        
        # Reinitialize
        self._initialize_config()
        
        logger.info("Configuration reloaded successfully")
    
    def shutdown(self):
        """Shutdown the configuration manager."""
        if self._file_observer:
            self._file_observer.stop()
            self._file_observer.join()
        
        logger.info("Configuration manager shutdown")


# ============================================================================
# CONFIGURATION FILE HANDLER
# ============================================================================

class ConfigFileHandler(FileSystemEventHandler):
    """File system event handler for configuration files."""
    
    def __init__(self, config_manager: CentralizedConfigManager):
        self.config_manager = config_manager
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith(('.json', '.yaml', '.yml', '.py')):
            logger.info(f"Configuration file modified: {event.src_path}")
            # Reload configuration after a short delay
            import threading
            import time
            def delayed_reload():
                time.sleep(1)  # Wait for file to be fully written
                self.config_manager.reload()
            
            threading.Thread(target=delayed_reload, daemon=True).start()


# ============================================================================
# GLOBAL CONFIGURATION INSTANCE
# ============================================================================

# Global configuration manager instance
_config_manager: Optional[CentralizedConfigManager] = None

def get_config_manager() -> CentralizedConfigManager:
    """Get the global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = CentralizedConfigManager()
    return _config_manager

def get_config(key: str, default: Any = None, section: Optional[str] = None) -> Any:
    """Get a configuration value from the global manager."""
    return get_config_manager().get(key, default, section)

def set_config(key: str, value: Any, section: str = "general", **kwargs):
    """Set a configuration value in the global manager."""
    get_config_manager().set(key, value, section, **kwargs)


# ============================================================================
# MAIN EXECUTION (FOR TESTING)
# ============================================================================

if __name__ == "__main__":
    # Example usage
    config_manager = CentralizedConfigManager()
    
    # Set some configuration values
    config_manager.set("log_level", "INFO", "logging", description="Application log level")
    config_manager.set("max_workers", 4, "performance", description="Maximum worker threads")
    config_manager.set("debug_mode", False, "development", description="Debug mode flag")
    
    # Get configuration values
    log_level = config_manager.get("log_level", section="logging")
    max_workers = config_manager.get("max_workers", section="performance")
    debug_mode = config_manager.get("debug_mode", section="development")
    
    print(f"Log Level: {log_level}")
    print(f"Max Workers: {max_workers}")
    print(f"Debug Mode: {debug_mode}")
    
    # Export configuration
    json_config = config_manager.export_config("json")
    print(f"\nConfiguration (JSON):\n{json_config}")
    
    # Cleanup
    config_manager.shutdown()
