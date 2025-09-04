#!/usr/bin/env python3
"""
Unified Configuration Utility - V2 Compliant
============================================

This module provides a unified configuration utility that consolidates all
configuration patterns across the codebase, eliminating DRY violations.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Consolidate all configuration patterns into unified utility
"""

from ..core.unified_data_processing_system import read_json, write_json
import os
from ..core.unified_data_processing_system import get_unified_data_processing
from typing import Any, Dict, Optional


class UnifiedConfigurationUtility:
    """
    Unified configuration utility that consolidates all configuration patterns.
    
    CONSOLIDATES:
    - Environment variable configuration
    - JSON file configuration
    - Default configuration patterns
    - Configuration loading patterns
    - Configuration saving patterns
    """
    
    _config_cache: Dict[str, Any] = {}
    _project_root = Path(__file__).parent.parent.parent
    
    @classmethod
    def load_config(cls, config_file: str = "config.json") -> Dict[str, Any]:
        """
        Load configuration from file and environment.
        
        Args:
            config_file: Configuration file name
            
        Returns:
            Configuration dictionary
        """
        if config_file in cls._config_cache:
            return cls._config_cache[config_file]
        
        config = {}
        
        # Load from file if exists
        config_path = cls._project_root / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = read_json(f)
            except Exception as e:
                print(f"Error loading config file {config_file}: {e}")
        
        # Load from environment variables
        env_config = cls._load_from_environment()
        config.update(env_config)
        
        # Cache the configuration
        cls._config_cache[config_file] = config
        
        return config
    
    @classmethod
    def _load_from_environment(cls) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        env_config = {}
        
        # Common environment variables
        env_mappings = {
            'MESSAGING_DEFAULT_SENDER': 'messaging.default_sender',
            'MESSAGING_MAX_LENGTH': 'messaging.max_message_length',
            'DISCORD_WEBHOOK_URL': 'discord.webhook_url',
            'DISCORD_BOT_TOKEN': 'discord.bot_token',
            'DISCORD_CHANNEL_ID': 'discord.channel_id',
            'VECTOR_DB_PROVIDER': 'vector_database.provider',
            'VECTOR_DB_DIR': 'vector_database.persist_directory'
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Convert to appropriate type
                if value.isdigit():
                    value = int(value)
                elif value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                
                # Set nested configuration
                keys = config_path.split('.')
                current = env_config
                for key in keys[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                current[keys[-1]] = value
        
        return env_config
    
    @classmethod
    def get_config(cls, key: str = None, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        config = cls.load_config()
        
        if key is None:
            return config
        
        # Support dot notation for nested keys
        keys = key.split('.')
        current = config
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    @classmethod
    def set_config(cls, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        config = cls.load_config()
        
        # Support dot notation for nested keys
        keys = key.split('.')
        current = config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        
        # Update cache
        cls._config_cache['config.json'] = config
    
    @classmethod
    def save_config(cls, config: Dict[str, Any] = None, config_file: str = "config.json") -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration to save (None for cached config)
            config_file: Configuration file name
            
        Returns:
            True if successful
        """
        try:
            if config is None:
                config = cls.load_config(config_file)
            
            config_path = cls._project_root / config_file
            with open(config_path, 'w', encoding='utf-8') as f:
                write_json(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    @classmethod
    def get_timestamp(cls) -> str:
        """Get current timestamp string."""
        from ..core.unified_data_processing_system import get_unified_data_processing
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Convenience functions for backward compatibility
def load_config() -> Dict[str, Any]:
    """Load configuration."""
    return UnifiedConfigurationUtility.load_config()

def get_config(key: str = None, default: Any = None) -> Any:
    """Get configuration value."""
    return UnifiedConfigurationUtility.get_config(key, default)

def get_timestamp() -> str:
    """Get current timestamp string."""
    return UnifiedConfigurationUtility.get_timestamp()