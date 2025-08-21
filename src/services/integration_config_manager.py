"""
Integration Configuration Manager for Agent_Cellphone_V2_Repository
Handles configuration management, environment variables, and integration settings.
"""

import os
import json
import yaml
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Set, Callable
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigSource(Enum):
    """Sources of configuration."""
    ENVIRONMENT = "environment"
    FILE = "file"
    DATABASE = "database"
    API = "api"
    DEFAULT = "default"


class ConfigScope(Enum):
    """Scopes of configuration."""
    GLOBAL = "global"
    SERVICE = "service"
    ENVIRONMENT = "environment"
    USER = "user"
    INSTANCE = "instance"


@dataclass
class ConfigValue:
    """Represents a configuration value with metadata."""
    value: Any
    source: ConfigSource
    scope: ConfigScope
    key: str
    description: str = ""
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    last_updated: float = field(default_factory=time.time)
    encrypted: bool = False
    tags: Set[str] = field(default_factory=set)


@dataclass
class ConfigSection:
    """Represents a configuration section."""
    name: str
    values: Dict[str, ConfigValue] = field(default_factory=dict)
    description: str = ""
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)


class ConfigValidator(ABC):
    """Abstract base class for configuration validators."""
    
    @abstractmethod
    def validate(self, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate a configuration value."""
        pass
    
    @abstractmethod
    def get_error_message(self, value: Any, rules: Dict[str, Any]) -> str:
        """Get error message for validation failure."""
        pass


class TypeValidator(ConfigValidator):
    """Validator for data types."""
    
    def validate(self, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate value type."""
        expected_type = rules.get('type')
        if not expected_type:
            return True
        
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'float':
            return isinstance(value, float)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'list':
            return isinstance(value, list)
        elif expected_type == 'dict':
            return isinstance(value, dict)
        
        return True
    
    def get_error_message(self, value: Any, rules: Dict[str, Any]) -> str:
        """Get error message for type validation failure."""
        expected_type = rules.get('type', 'unknown')
        actual_type = type(value).__name__
        return f"Expected type '{expected_type}', got '{actual_type}'"


class RangeValidator(ConfigValidator):
    """Validator for numeric ranges."""
    
    def validate(self, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate numeric range."""
        if not isinstance(value, (int, float)):
            return False
        
        min_val = rules.get('min')
        max_val = rules.get('max')
        
        if min_val is not None and value < min_val:
            return False
        
        if max_val is not None and value > max_val:
            return False
        
        return True
    
    def get_error_message(self, value: Any, rules: Dict[str, Any]) -> str:
        """Get error message for range validation failure."""
        min_val = rules.get('min')
        max_val = rules.get('max')
        
        if min_val is not None and max_val is not None:
            return f"Value {value} must be between {min_val} and {max_val}"
        elif min_val is not None:
            return f"Value {value} must be at least {min_val}"
        elif max_val is not None:
            return f"Value {value} must be at most {max_val}"
        
        return "Range validation failed"


class RequiredValidator(ConfigValidator):
    """Validator for required fields."""
    
    def validate(self, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate required field."""
        if not rules.get('required', False):
            return True
        
        if value is None:
            return False
        
        if isinstance(value, str) and value.strip() == "":
            return False
        
        return True
    
    def get_error_message(self, value: Any, rules: Dict[str, Any]) -> str:
        """Get error message for required validation failure."""
        return "This field is required"


class PatternValidator(ConfigValidator):
    """Validator for pattern matching."""
    
    def validate(self, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate pattern match."""
        if not isinstance(value, str):
            return False
        
        pattern = rules.get('pattern')
        if not pattern:
            return True
        
        import re
        try:
            return bool(re.match(pattern, value))
        except re.error:
            logger.warning(f"Invalid regex pattern: {pattern}")
            return True
    
    def get_error_message(self, value: Any, rules: Dict[str, Any]) -> str:
        """Get error message for pattern validation failure."""
        pattern = rules.get('pattern', 'unknown')
        return f"Value '{value}' does not match pattern '{pattern}'"


class ConfigFileWatcher(FileSystemEventHandler):
    """File system watcher for configuration files."""
    
    def __init__(self, config_manager: 'IntegrationConfigManager'):
        self.config_manager = config_manager
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith(('.yaml', '.yml', '.json', '.ini')):
            logger.info(f"Configuration file modified: {event.src_path}")
            self.config_manager.reload_config_file(event.src_path)
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory and event.src_path.endswith(('.yaml', '.yml', '.json', '.ini')):
            logger.info(f"Configuration file created: {event.src_path}")
            self.config_manager.load_config_file(event.src_path)
    
    def on_deleted(self, event):
        """Handle file deletion events."""
        if not event.is_directory and event.src_path.endswith(('.yaml', '.yml', '.json', '.ini')):
            logger.info(f"Configuration file deleted: {event.src_path}")
            self.config_manager.remove_config_file(event.src_path)


class IntegrationConfigManager:
    """Main configuration manager for integration infrastructure."""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path("config")
        self.config_dir.mkdir(exist_ok=True)
        
        # Configuration storage
        self.config_values: Dict[str, ConfigValue] = {}
        self.config_sections: Dict[str, ConfigSection] = {}
        
        # Validators
        self.validators: Dict[str, ConfigValidator] = {}
        self._register_default_validators()
        
        # File watcher
        self.file_watcher = ConfigFileWatcher(self)
        self.observer = Observer()
        self.watching_files = False
        
        # Configuration sources
        self.config_files: Dict[str, Dict[str, Any]] = {}
        
        # Event callbacks
        self.config_changed_callbacks: List[Callable[[str, Any, Any], None]] = []
        self.config_loaded_callbacks: List[Callable[[str], None]] = []
        
        # Load initial configuration
        self._load_environment_config()
        self._load_default_config()
        self._load_config_files()
    
    def _register_default_validators(self):
        """Register default configuration validators."""
        self.register_validator('type', TypeValidator())
        self.register_validator('range', RangeValidator())
        self.register_validator('required', RequiredValidator())
        self.register_validator('pattern', PatternValidator())
    
    def register_validator(self, name: str, validator: ConfigValidator):
        """Register a configuration validator."""
        self.validators[name] = validator
        logger.info(f"Registered validator: {name}")
    
    def _load_environment_config(self):
        """Load configuration from environment variables."""
        env_prefix = os.getenv('AGENT_CELLPHONE_CONFIG_PREFIX', 'AGENT_CELLPHONE_')
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower().replace('_', '.')
                self.set_config_value(
                    config_key,
                    value,
                    ConfigSource.ENVIRONMENT,
                    ConfigScope.GLOBAL,
                    f"Environment variable {key}"
                )
    
    def _load_default_config(self):
        """Load default configuration values."""
        default_config = {
            'api.host': 'localhost',
            'api.port': 8000,
            'api.debug': False,
            'api.timeout': 30,
            'database.host': 'localhost',
            'database.port': 5432,
            'database.name': 'agent_cellphone',
            'database.pool_size': 10,
            'logging.level': 'INFO',
            'logging.format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'middleware.enabled': True,
            'middleware.timeout': 60,
            'health_check.interval': 30,
            'health_check.timeout': 10,
            'service_registry.enabled': True,
            'service_registry.heartbeat_interval': 60
        }
        
        for key, value in default_config.items():
            self.set_config_value(
                key,
                value,
                ConfigSource.DEFAULT,
                ConfigScope.GLOBAL,
                f"Default configuration for {key}"
            )
    
    def _load_config_files(self):
        """Load configuration from files in the config directory."""
        config_extensions = ['.yaml', '.yml', '.json', '.ini']
        
        for file_path in self.config_dir.glob('*'):
            if file_path.suffix in config_extensions:
                self.load_config_file(str(file_path))
    
    def load_config_file(self, file_path: str):
        """Load configuration from a specific file."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.warning(f"Configuration file not found: {file_path}")
                return
            
            config_data = {}
            if file_path.suffix in ['.yaml', '.yml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f) or {}
            elif file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            elif file_path.suffix == '.ini':
                import configparser
                parser = configparser.ConfigParser()
                parser.read(file_path)
                for section in parser.sections():
                    config_data[section] = dict(parser.items(section))
            
            # Store file data
            self.config_files[str(file_path)] = config_data
            
            # Process configuration data
            self._process_config_data(config_data, str(file_path))
            
            # Trigger callbacks
            for callback in self.config_loaded_callbacks:
                try:
                    callback(str(file_path))
                except Exception as e:
                    logger.error(f"Error in config loaded callback: {str(e)}")
            
            logger.info(f"Loaded configuration file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading configuration file {file_path}: {str(e)}")
    
    def _process_config_data(self, config_data: Dict[str, Any], source: str):
        """Process configuration data and store values."""
        def process_dict(data: Dict[str, Any], prefix: str = ""):
            for key, value in data.items():
                full_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, dict):
                    process_dict(value, full_key)
                else:
                    self.set_config_value(
                        full_key,
                        value,
                        ConfigSource.FILE,
                        ConfigScope.GLOBAL,
                        f"From configuration file: {source}"
                    )
        
        process_dict(config_data)
    
    def reload_config_file(self, file_path: str):
        """Reload a configuration file."""
        # Remove existing values from this file
        file_path_str = str(file_path)
        if file_path_str in self.config_files:
            old_data = self.config_files[file_path_str]
            # Note: This is a simplified approach - in production you'd want more sophisticated tracking
            
            # Reload the file
            self.load_config_file(file_path_str)
    
    def remove_config_file(self, file_path: str):
        """Remove configuration from a file."""
        file_path_str = str(file_path)
        if file_path_str in self.config_files:
            # Note: This is a simplified approach - in production you'd want more sophisticated tracking
            del self.config_files[file_path_str]
            logger.info(f"Removed configuration file: {file_path}")
    
    def set_config_value(self, key: str, value: Any, source: ConfigSource, 
                        scope: ConfigScope, description: str = ""):
        """Set a configuration value."""
        # Validate the value if validation rules exist
        if key in self.config_values:
            existing_value = self.config_values[key]
            if existing_value.validation_rules:
                if not self._validate_value(value, existing_value.validation_rules):
                    raise ValueError(f"Configuration validation failed for {key}")
        
        # Create or update config value
        config_value = ConfigValue(
            value=value,
            source=source,
            scope=scope,
            key=key,
            description=description,
            last_updated=time.time()
        )
        
        # Check if value changed
        old_value = None
        if key in self.config_values:
            old_value = self.config_values[key].value
        
        self.config_values[key] = config_value
        
        # Trigger change callbacks
        if old_value != value:
            for callback in self.config_changed_callbacks:
                try:
                    callback(key, old_value, value)
                except Exception as e:
                    logger.error(f"Error in config changed callback: {str(e)}")
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        if key in self.config_values:
            return self.config_values[key].value
        return default
    
    def get_config_value_with_metadata(self, key: str) -> Optional[ConfigValue]:
        """Get a configuration value with full metadata."""
        return self.config_values.get(key)
    
    def has_config_value(self, key: str) -> bool:
        """Check if a configuration value exists."""
        return key in self.config_values
    
    def _validate_value(self, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate a configuration value against rules."""
        for rule_name, rule_config in rules.items():
            validator = self.validators.get(rule_name)
            if validator and not validator.validate(value, rule_config):
                logger.warning(f"Configuration validation failed: {validator.get_error_message(value, rule_config)}")
                return False
        return True
    
    def add_validation_rules(self, key: str, rules: Dict[str, Any]):
        """Add validation rules for a configuration key."""
        if key in self.config_values:
            self.config_values[key].validation_rules.update(rules)
        else:
            # Create a placeholder config value with validation rules
            self.config_values[key] = ConfigValue(
                value=None,
                source=ConfigSource.DEFAULT,
                scope=ConfigScope.GLOBAL,
                key=key,
                validation_rules=rules
            )
    
    def get_config_section(self, section_name: str) -> Dict[str, Any]:
        """Get all configuration values for a section."""
        section_data = {}
        section_prefix = f"{section_name}."
        
        for key, config_value in self.config_values.items():
            if key.startswith(section_prefix):
                section_key = key[len(section_prefix):]
                section_data[section_key] = config_value.value
        
        return section_data
    
    def add_config_changed_callback(self, callback: Callable[[str, Any, Any], None]):
        """Add callback for when configuration changes."""
        self.config_changed_callbacks.append(callback)
    
    def add_config_loaded_callback(self, callback: Callable[[str], None]):
        """Add callback for when configuration files are loaded."""
        self.config_loaded_callbacks.append(callback)
    
    def start_file_watching(self):
        """Start watching configuration files for changes."""
        if self.watching_files:
            return
        
        try:
            self.observer.schedule(self.file_watcher, str(self.config_dir), recursive=True)
            self.observer.start()
            self.watching_files = True
            logger.info(f"Started watching configuration directory: {self.config_dir}")
        except Exception as e:
            logger.error(f"Error starting file watcher: {str(e)}")
    
    def stop_file_watching(self):
        """Stop watching configuration files."""
        if not self.watching_files:
            return
        
        try:
            self.observer.stop()
            self.observer.join()
            self.watching_files = False
            logger.info("Stopped watching configuration files")
        except Exception as e:
            logger.error(f"Error stopping file watcher: {str(e)}")
    
    def export_config(self, format: str = 'json') -> str:
        """Export configuration in specified format."""
        config_data = {}
        
        for key, config_value in self.config_values.items():
            config_data[key] = {
                'value': config_value.value,
                'source': config_value.source.value,
                'scope': config_value.scope.value,
                'description': config_value.description,
                'last_updated': config_value.last_updated
            }
        
        if format.lower() == 'json':
            return json.dumps(config_data, indent=2, default=str)
        elif format.lower() == 'yaml':
            return yaml.dump(config_data, default_flow_style=False, allow_unicode=True)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the configuration."""
        source_counts = {}
        scope_counts = {}
        
        for config_value in self.config_values.values():
            source = config_value.source.value
            scope = config_value.scope.value
            
            source_counts[source] = source_counts.get(source, 0) + 1
            scope_counts[scope] = scope_counts.get(scope, 0) + 1
        
        return {
            'total_config_values': len(self.config_values),
            'config_files': len(self.config_files),
            'source_counts': source_counts,
            'scope_counts': scope_counts,
            'watching_files': self.watching_files,
            'validators': list(self.validators.keys())
        }
    
    def cleanup(self):
        """Clean up resources."""
        self.stop_file_watching()


# Example usage and testing
def main():
    """Main function for testing the Configuration Manager."""
    # Create configuration manager
    config_manager = IntegrationConfigManager("test_config")
    
    # Add validation rules
    config_manager.add_validation_rules('api.port', {
        'type': 'integer',
        'range': {'min': 1, 'max': 65535}
    })
    
    config_manager.add_validation_rules('api.host', {
        'required': True,
        'pattern': r'^[a-zA-Z0-9.-]+$'
    })
    
    # Set configuration values
    config_manager.set_config_value(
        'api.host',
        'localhost',
        ConfigSource.FILE,
        ConfigScope.GLOBAL,
        'API server hostname'
    )
    
    config_manager.set_config_value(
        'api.port',
        8000,
        ConfigSource.FILE,
        ConfigScope.GLOBAL,
        'API server port'
    )
    
    # Add callbacks
    def on_config_changed(key: str, old_value: Any, new_value: Any):
        print(f"Configuration changed: {key} = {old_value} -> {new_value}")
    
    def on_config_loaded(file_path: str):
        print(f"Configuration loaded from: {file_path}")
    
    config_manager.add_config_changed_callback(on_config_changed)
    config_manager.add_config_loaded_callback(on_config_loaded)
    
    # Test configuration retrieval
    print(f"API Host: {config_manager.get_config_value('api.host')}")
    print(f"API Port: {config_manager.get_config_value('api.port')}")
    print(f"Database Host: {config_manager.get_config_value('database.host')}")
    
    # Get section configuration
    api_config = config_manager.get_config_section('api')
    print(f"API Configuration: {api_config}")
    
    # Export configuration
    json_config = config_manager.export_config('json')
    print(f"\nExported Configuration (JSON):\n{json_config}")
    
    # Get summary
    summary = config_manager.get_config_summary()
    print(f"\nConfiguration Summary: {json.dumps(summary, indent=2)}")
    
    # Test validation
    try:
        config_manager.set_config_value('api.port', 99999, ConfigSource.FILE, ConfigScope.GLOBAL)
    except ValueError as e:
        print(f"Validation error: {e}")
    
    # Cleanup
    config_manager.cleanup()


if __name__ == "__main__":
    main()
