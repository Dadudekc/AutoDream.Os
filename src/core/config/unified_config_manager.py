"""
UnifiedConfigManager - Centralized configuration management system.
Based on Dream.OS patterns with V2 compliance and KISS principles.

Features:
- YAML and JSON config support
- Environment variable overrides
- Configuration validation
- Hot reload support
- Default fallbacks
"""

import os
import yaml
import json
import threading
from typing import Any, Dict, Optional, List, Union
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass

class UnifiedConfigManager:
    """
    Centralized configuration management system.
    V2 Compliant: ≤400 lines, simple data classes, direct method calls.
    """
    
    # Default configuration schema with validation rules
    CONFIG_SCHEMA = {
        "app": {
            "name": str,
            "version": str,
            "debug": bool,
            "log_level": str,
            "max_retries": int,
            "timeout": float
        },
        "ai": {
            "model": str,
            "temperature": float,
            "max_tokens": int,
            "memory": {
                "max_entries": int,
                "min_score": float
            }
        },
        "discord": {
            "bot_token": str,
            "channel_id": int,
            "enabled": bool
        },
        "database": {
            "url": str,
            "pool_size": int,
            "timeout": float
        }
    }
    
    def __init__(self, config_dir: str = "config", config_file: str = "unified_config.yaml"):
        """Initialize UnifiedConfigManager."""
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / config_file
        self._config: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._last_modified: Optional[datetime] = None
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Load initial configuration
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file with environment overrides."""
        with self._lock:
            try:
                # Load base configuration
                if self.config_file.exists():
                    with open(self.config_file, 'r') as f:
                        if self.config_file.suffix == '.yaml':
                            self._config = yaml.safe_load(f) or {}
                        else:
                            self._config = json.load(f) or {}
                else:
                    self._config = {}
                
                # Apply environment variable overrides
                self._apply_env_overrides()
                
                # Validate configuration
                self._validate_config()
                
                # Update last modified time
                if self.config_file.exists():
                    self._last_modified = datetime.fromtimestamp(
                        self.config_file.stat().st_mtime
                    )
                
                logger.info(f"Configuration loaded from {self.config_file}")
                
            except Exception as e:
                logger.error(f"Failed to load configuration: {e}")
                self._config = self._get_default_config()
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration."""
        env_mappings = {
            'APP_NAME': ('app', 'name'),
            'APP_VERSION': ('app', 'version'),
            'APP_DEBUG': ('app', 'debug'),
            'LOG_LEVEL': ('app', 'log_level'),
            'AI_MODEL': ('ai', 'model'),
            'AI_TEMPERATURE': ('ai', 'temperature'),
            'DISCORD_BOT_TOKEN': ('discord', 'bot_token'),
            'DISCORD_CHANNEL_ID': ('discord', 'channel_id'),
            'DATABASE_URL': ('database', 'url')
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert value to appropriate type
                converted_value = self._convert_env_value(value, section, key)
                self._set_nested_value(self._config, section, key, converted_value)
    
    def _convert_env_value(self, value: str, section: str, key: str) -> Any:
        """Convert environment variable value to appropriate type."""
        expected_type = self._get_expected_type(section, key)
        
        if expected_type == bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        elif expected_type == int:
            return int(value)
        elif expected_type == float:
            return float(value)
        else:
            return value
    
    def _get_expected_type(self, section: str, key: str) -> type:
        """Get expected type for configuration value."""
        try:
            schema_section = self.CONFIG_SCHEMA.get(section, {})
            if isinstance(schema_section, dict) and key in schema_section:
                return schema_section[key]
            return str
        except:
            return str
    
    def _set_nested_value(self, config: Dict, section: str, key: str, value: Any) -> None:
        """Set nested configuration value."""
        if section not in config:
            config[section] = {}
        config[section][key] = value
    
    def _validate_config(self) -> None:
        """Validate configuration against schema."""
        try:
            self._validate_section(self._config, self.CONFIG_SCHEMA)
        except Exception as e:
            logger.warning(f"Configuration validation failed: {e}")
            # Use default config if validation fails
            self._config = self._get_default_config()
    
    def _validate_section(self, config: Dict, schema: Dict) -> None:
        """Validate configuration section against schema."""
        for key, expected_type in schema.items():
            if key not in config:
                continue
            
            if isinstance(expected_type, dict):
                if not isinstance(config[key], dict):
                    raise ConfigValidationError(f"Expected dict for {key}")
                self._validate_section(config[key], expected_type)
            else:
                if not isinstance(config[key], expected_type):
                    raise ConfigValidationError(
                        f"Expected {expected_type.__name__} for {key}, got {type(config[key]).__name__}"
                    )
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "app": {
                "name": "Agent-Cellphone-V2",
                "version": "1.0.0",
                "debug": False,
                "log_level": "INFO",
                "max_retries": 3,
                "timeout": 30.0
            },
            "ai": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
                "memory": {
                    "max_entries": 1000,
                    "min_score": 0.5
                }
            },
            "discord": {
                "bot_token": "",
                "channel_id": 0,
                "enabled": False
            },
            "database": {
                "url": "sqlite:///memory.db",
                "pool_size": 5,
                "timeout": 30.0
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)."""
        with self._lock:
            keys = key.split('.')
            value = self._config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key (supports dot notation)."""
        with self._lock:
            keys = key.split('.')
            config = self._config
            
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
        logger.info("Configuration reloaded")
    
    def save(self) -> None:
        """Save current configuration to file."""
        with self._lock:
            try:
                with open(self.config_file, 'w') as f:
                    if self.config_file.suffix == '.yaml':
                        yaml.dump(self._config, f, default_flow_style=False)
                    else:
                        json.dump(self._config, f, indent=2)
                
                logger.info(f"Configuration saved to {self.config_file}")
                
            except Exception as e:
                logger.error(f"Failed to save configuration: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        with self._lock:
            return self._config.copy()
    
    def is_modified(self) -> bool:
        """Check if configuration file has been modified since last load."""
        if not self.config_file.exists():
            return False
        
        current_mtime = datetime.fromtimestamp(self.config_file.stat().st_mtime)
        return self._last_modified is None or current_mtime > self._last_modified

# Global configuration manager instance
config_manager = UnifiedConfigManager()

def get_config(key: str = None, default: Any = None) -> Any:
    """Get configuration value or manager instance."""
    if key is None:
        return config_manager
    return config_manager.get(key, default)

def set_config(key: str, value: Any) -> None:
    """Set configuration value."""
    config_manager.set(key, value)

def reload_config() -> None:
    """Reload configuration from file."""
    config_manager.reload()

def save_config() -> None:
    """Save configuration to file."""
    config_manager.save()

