"""
Unified Base Configuration Class

This class consolidates functionality from 18 duplicate config.py files:
- Performance configuration
- Refactoring configuration
- Testing configuration
- Service configuration
- AI/ML configuration
- FSM configuration
- And many more...

Provides unified configuration management for the entire system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
import json
import yaml
import os
from pathlib import Path
from datetime import datetime, timezone


class ConfigType(Enum):
    """Unified configuration types."""
    PERFORMANCE = "performance"
    REFACTORING = "refactoring"
    TESTING = "testing"
    SERVICE = "service"
    AI_ML = "ai_ml"
    FSM = "fsm"
    WORKFLOW = "workflow"
    VALIDATION = "validation"
    SECURITY = "security"
    DATABASE = "database"
    CUSTOM = "custom"


class ConfigFormat(Enum):
    """Supported configuration file formats."""
    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    ENV = "env"
    PYTHON = "python"


class ConfigSource(Enum):
    """Configuration source types."""
    FILE = "file"
    ENVIRONMENT = "environment"
    DATABASE = "database"
    API = "api"
    DEFAULT = "default"


@dataclass
class ConfigValue:
    """Unified configuration value with metadata."""
    value: Any
    source: ConfigSource
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    description: Optional[str] = None
    validation_rules: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigSection:
    """Configuration section definition."""
    name: str
    description: str
    config_type: ConfigType
    values: Dict[str, ConfigValue] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigMetadata:
    """Configuration metadata."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class ConfigOptions:
    """Configuration options for loading and validation."""
    auto_reload: bool = False
    reload_interval: float = 300.0  # 5 minutes
    validate_on_load: bool = True
    strict_mode: bool = False
    allow_environment_overrides: bool = True
    allow_file_overrides: bool = True
    cache_enabled: bool = True
    cache_ttl: float = 3600.0  # 1 hour


class BaseConfig(ABC):
    """
    Unified base class for all configuration types.
    
    Consolidates functionality from duplicate config implementations:
    - src/core/performance/config/config.py
    - src/core/refactoring/config.py
    - src/core/testing/config.py
    - src/services/config.py
    - src/extended/ai_ml/config.py
    - src/fsm/config.py
    - And 12+ more...
    """
    
    def __init__(self, config_path: Optional[Path] = None, options: Optional[ConfigOptions] = None):
        """
        Initialize the unified base configuration.
        
        Args:
            config_path: Path to configuration file
            options: Configuration options
        """
        self.config_path = config_path
        self.options = options or ConfigOptions()
        self.logger = self._setup_logging()
        self.metadata = ConfigMetadata(name=self.__class__.__name__)
        self.sections: Dict[str, ConfigSection] = {}
        self._cache: Dict[str, Any] = {}
        self._last_modified: Optional[datetime] = None
        
        self._initialize()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up unified logging for all configuration types."""
        logger = logging.getLogger(f"{self.__class__.__name__}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize(self) -> None:
        """Initialize configuration-specific components."""
        try:
            self.logger.info(f"Initializing configuration: {self.metadata.name}")
            
            # Load configuration if path provided
            if self.config_path and self.config_path.exists():
                self._load_config()
            
            # Initialize configuration-specific resources
            self._initialize_resources()
            
            # Load default configuration
            self._load_defaults()
            
            # Apply environment overrides if enabled
            if self.options.allow_environment_overrides:
                self._apply_environment_overrides()
            
            # Validate configuration if enabled
            if self.options.validate_on_load:
                self._validate_config()
            
            self.logger.info(f"Configuration {self.metadata.name} initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize configuration {self.metadata.name}: {e}")
            raise
    
    @abstractmethod
    def _initialize_resources(self) -> None:
        """Initialize configuration-specific resources. Must be implemented by subclasses."""
        pass
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if not self.config_path or not self.config_path.exists():
            return
        
        try:
            self.logger.info(f"Loading configuration from {self.config_path}")
            
            # Determine file format
            file_format = self._detect_file_format()
            
            # Load based on format
            if file_format == ConfigFormat.JSON:
                self._load_json_config()
            elif file_format == ConfigFormat.YAML:
                self._load_yaml_config()
            elif file_format == ConfigFormat.INI:
                self._load_ini_config()
            elif file_format == ConfigFormat.PYTHON:
                self._load_python_config()
            else:
                self.logger.warning(f"Unsupported file format: {file_format}")
            
            self._last_modified = datetime.fromtimestamp(self.config_path.stat().st_mtime, tz=timezone.utc)
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {self.config_path}: {e}")
            raise
    
    def _detect_file_format(self) -> ConfigFormat:
        """Detect configuration file format."""
        if not self.config_path:
            return ConfigFormat.JSON
        
        suffix = self.config_path.suffix.lower()
        if suffix == '.json':
            return ConfigFormat.JSON
        elif suffix in ['.yml', '.yaml']:
            return ConfigFormat.YAML
        elif suffix == '.ini':
            return ConfigFormat.INI
        elif suffix == '.py':
            return ConfigFormat.PYTHON
        else:
            return ConfigFormat.JSON  # Default
    
    def _load_json_config(self) -> None:
        """Load JSON configuration."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._parse_config_data(data)
    
    def _load_yaml_config(self) -> None:
        """Load YAML configuration."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        self._parse_config_data(data)
    
    def _load_ini_config(self) -> None:
        """Load INI configuration."""
        import configparser
        config = configparser.ConfigParser()
        config.read(self.config_path)
        
        data = {}
        for section in config.sections():
            data[section] = dict(config[section])
        
        self._parse_config_data(data)
    
    def _load_python_config(self) -> None:
        """Load Python configuration."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("config_module", self.config_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Extract configuration data from module
            data = {}
            for attr_name in dir(module):
                if not attr_name.startswith('_'):
                    attr_value = getattr(module, attr_name)
                    if not callable(attr_value):
                        data[attr_name] = attr_value
            
            self._parse_config_data(data)
    
    def _parse_config_data(self, data: Dict[str, Any]) -> None:
        """Parse configuration data into sections."""
        for section_name, section_data in data.items():
            if isinstance(section_data, dict):
                section = ConfigSection(
                    name=section_name,
                    description=f"Configuration section: {section_name}",
                    config_type=ConfigType.CUSTOM
                )
                
                for key, value in section_data.items():
                    config_value = ConfigValue(
                        value=value,
                        source=ConfigSource.FILE,
                        description=f"Configuration value: {key}"
                    )
                    section.values[key] = config_value
                
                self.sections[section_name] = section
    
    def _load_defaults(self) -> None:
        """Load default configuration values."""
        self.logger.debug("Loading default configuration values")
        # Implementation depends on configuration type
    
    def _apply_environment_overrides(self) -> None:
        """Apply environment variable overrides."""
        if not self.options.allow_environment_overrides:
            return
        
        self.logger.debug("Applying environment variable overrides")
        
        # Look for environment variables with prefix
        prefix = f"{self.metadata.name.upper()}_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                self._set_value(config_key, value, ConfigSource.ENVIRONMENT)
    
    def _validate_config(self) -> None:
        """Validate configuration values."""
        self.logger.debug("Validating configuration")
        
        for section_name, section in self.sections.items():
            for key, config_value in section.values.items():
                try:
                    self._validate_value(key, config_value.value)
                except ValueError as e:
                    if self.options.strict_mode:
                        raise ValueError(f"Configuration validation failed for {section_name}.{key}: {e}")
                    else:
                        self.logger.warning(f"Configuration validation warning for {section_name}.{key}: {e}")
    
    def _validate_value(self, key: str, value: Any) -> None:
        """Validate a configuration value."""
        # Basic validation - can be overridden by subclasses
        if value is None:
            raise ValueError(f"Value for {key} cannot be None")
    
    def get_value(self, key: str, default: Any = None, section: Optional[str] = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            section: Configuration section (optional)
            
        Returns:
            Configuration value or default
        """
        # Check cache first
        cache_key = f"{section}.{key}" if section else key
        if self.options.cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]
        
        # Look for value in specified section or search all sections
        if section:
            if section in self.sections and key in self.sections[section].values:
                value = self.sections[section].values[key].value
                if self.options.cache_enabled:
                    self._cache[cache_key] = value
                return value
        else:
            # Search all sections
            for section_name, section_data in self.sections.items():
                if key in section_data.values:
                    value = section_data.values[key].value
                    if self.options.cache_enabled:
                        self._cache[cache_key] = value
                    return value
        
        return default
    
    def set_value(self, key: str, value: Any, section: str = "default", source: ConfigSource = ConfigSource.DEFAULT) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
            section: Configuration section
            source: Value source
        """
        if section not in self.sections:
            self.sections[section] = ConfigSection(
                name=section,
                description=f"Configuration section: {section}",
                config_type=ConfigType.CUSTOM
            )
        
        config_value = ConfigValue(
            value=value,
            source=source,
            description=f"Configuration value: {key}"
        )
        
        self.sections[section].values[key] = config_value
        
        # Update cache
        cache_key = f"{section}.{key}"
        if self.options.cache_enabled:
            self._cache[cache_key] = value
        
        # Update metadata
        self.metadata.modified = datetime.now(timezone.utc)
        
        self.logger.debug(f"Set configuration value: {section}.{key} = {value}")
    
    def _set_value(self, key: str, value: Any, source: ConfigSource) -> None:
        """Internal method to set value with source tracking."""
        self.set_value(key, value, "default", source)
    
    def has_value(self, key: str, section: Optional[str] = None) -> bool:
        """Check if configuration key exists."""
        if section:
            return section in self.sections and key in self.sections[section].values
        else:
            return any(key in section_data.values for section_data in self.sections.values())
    
    def get_section(self, section_name: str) -> Optional[ConfigSection]:
        """Get configuration section."""
        return self.sections.get(section_name)
    
    def get_all_values(self, section: Optional[str] = None) -> Dict[str, Any]:
        """Get all configuration values."""
        if section:
            if section in self.sections:
                return {key: config_value.value for key, config_value in self.sections[section].values.items()}
            return {}
        else:
            result = {}
            for section_name, section_data in self.sections.items():
                result.update({key: config_value.value for key, config_value in section_data.values.items()})
            return result
    
    def reload(self) -> bool:
        """Reload configuration from file."""
        try:
            self.logger.info("Reloading configuration")
            self._cache.clear()
            self._load_config()
            return True
        except Exception as e:
            self.logger.error(f"Failed to reload configuration: {e}")
            return False
    
    def save(self, path: Optional[Path] = None) -> bool:
        """Save configuration to file."""
        save_path = path or self.config_path
        if not save_path:
            return False
        
        try:
            self.logger.info(f"Saving configuration to {save_path}")
            
            # Prepare data for saving
            data = {}
            for section_name, section in self.sections.items():
                data[section_name] = {
                    key: config_value.value for key, config_value in section.values.items()
                }
            
            # Save based on file format
            file_format = self._detect_file_format()
            if file_format == ConfigFormat.JSON:
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
            elif file_format == ConfigFormat.YAML:
                with open(save_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, indent=2)
            else:
                self.logger.warning(f"Save not supported for format: {file_format}")
                return False
            
            self.metadata.modified = datetime.now(timezone.utc)
            self.logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def export(self, format: ConfigFormat = ConfigFormat.JSON) -> str:
        """Export configuration in specified format."""
        data = self.get_all_values()
        
        if format == ConfigFormat.JSON:
            return json.dumps(data, indent=2, default=str)
        elif format == ConfigFormat.YAML:
            return yaml.dump(data, default_flow_style=False, indent=2)
        else:
            raise ValueError(f"Export format {format} not supported")
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get configuration metadata."""
        return asdict(self.metadata)
    
    def __getitem__(self, key: str) -> Any:
        """Dictionary-like access to configuration values."""
        return self.get_value(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Dictionary-like setting of configuration values."""
        self.set_value(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Check if configuration key exists."""
        return self.has_value(key)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name='{self.metadata.name}', sections={len(self.sections)})"
