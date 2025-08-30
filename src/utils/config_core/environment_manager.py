#!/usr/bin/env python3
"""
Environment Manager - Environment Override Functionality

This module provides environment override functionality for the unified
configuration system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 2: Configuration System Consolidation
"""

import os
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class EnvironmentManager:
    """
    Environment manager for the unified configuration system.
    
    This class provides environment override functionality for configuration data.
    """
    
    def __init__(self):
        """Initialize the environment manager."""
        self.override_prefix = "CONFIG_"
        self.override_separator = "_"
    
    def apply_environment_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply environment variable overrides to configuration.
        
        Args:
            config: Base configuration dictionary
            
        Returns:
            Configuration with environment overrides applied
        """
        try:
            # Create a copy to avoid modifying the original
            updated_config = config.copy()
            
            # Get all environment variables with the config prefix
            env_overrides = self._get_environment_overrides()
            
            # Apply overrides
            for env_key, env_value in env_overrides.items():
                config_key = self._convert_env_key_to_config_key(env_key)
                if config_key:
                    self._set_nested_config_value(updated_config, config_key, env_value)
            
            logger.info(f"Applied {len(env_overrides)} environment overrides")
            return updated_config
            
        except Exception as e:
            logger.error(f"Failed to apply environment overrides: {e}")
            return config
    
    def _get_environment_overrides(self) -> Dict[str, str]:
        """
        Get environment variables that should override configuration.
        
        Returns:
            Dictionary of environment variable overrides
        """
        overrides = {}
        
        for key, value in os.environ.items():
            if key.startswith(self.override_prefix):
                overrides[key] = value
        
        return overrides
    
    def _convert_env_key_to_config_key(self, env_key: str) -> Optional[str]:
        """
        Convert environment variable key to configuration key.
        
        Args:
            env_key: Environment variable key (e.g., 'CONFIG_SYSTEM_LOG_LEVEL')
            
        Returns:
            Configuration key (e.g., 'system.log_level') or None if invalid
        """
        if not env_key.startswith(self.override_prefix):
            return None
        
        # Remove prefix and convert to lowercase
        config_key = env_key[len(self.override_prefix):].lower()
        
        # Replace underscores with dots for nested keys
        config_key = config_key.replace(self.override_separator, ".")
        
        return config_key
    
    def _set_nested_config_value(self, config: Dict[str, Any], 
                                key_path: str, value: str) -> None:
        """
        Set a nested configuration value using dot notation.
        
        Args:
            config: Configuration dictionary to modify
            key_path: Dot notation path to configuration value
            value: Value to set
        """
        keys = key_path.split(".")
        current = config
        
        try:
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Convert value to appropriate type and set
            final_key = keys[-1]
            converted_value = self._convert_value_type(value)
            current[final_key] = converted_value
            
            logger.debug(f"Set config value {key_path} = {converted_value} (from env)")
            
        except Exception as e:
            logger.warning(f"Failed to set config value {key_path}: {e}")
    
    def _convert_value_type(self, value: str) -> Any:
        """
        Convert string value to appropriate Python type.
        
        Args:
            value: String value to convert
            
        Returns:
            Converted value with appropriate type
        """
        # Try to convert to boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # Try to convert to integer
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # Return as string if no conversion possible
        return value
    
    def get_override_summary(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of environment overrides applied.
        
        Args:
            config: Configuration dictionary to analyze
            
        Returns:
            Dictionary with override summary
        """
        try:
            env_overrides = self._get_environment_overrides()
            
            summary = {
                'total_overrides': len(env_overrides),
                'override_keys': list(env_overrides.keys()),
                'config_keys_affected': []
            }
            
            # Find which configuration keys were affected
            for env_key in env_overrides:
                config_key = self._convert_env_key_to_config_key(env_key)
                if config_key:
                    summary['config_keys_affected'].append(config_key)
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get override summary: {e}")
            return {'error': str(e)}
    
    def set_override_prefix(self, prefix: str) -> None:
        """
        Set the environment variable prefix for overrides.
        
        Args:
            prefix: New prefix for environment variables
        """
        self.override_prefix = prefix
        logger.info(f"Environment override prefix set to: {prefix}")
    
    def set_override_separator(self, separator: str) -> None:
        """
        Set the separator used in environment variable names.
        
        Args:
            separator: New separator character
        """
        self.override_separator = separator
        logger.info(f"Environment override separator set to: {separator}")
    
    def get_environment_variables(self) -> Dict[str, str]:
        """
        Get all environment variables.
        
        Returns:
            Dictionary of all environment variables
        """
        return dict(os.environ)
    
    def get_config_environment_variables(self) -> Dict[str, str]:
        """
        Get environment variables that could affect configuration.
        
        Returns:
            Dictionary of configuration-related environment variables
        """
        config_env = {}
        
        for key, value in os.environ.items():
            if key.startswith(self.override_prefix):
                config_env[key] = value
        
        return config_env
    
    def clear_environment_cache(self) -> None:
        """Clear any cached environment variable data."""
        # This method is a placeholder for future caching functionality
        logger.debug("Environment cache cleared")
