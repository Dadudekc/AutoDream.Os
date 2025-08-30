"""
Configuration Manager - Unified Configuration Access with Inheritance

This module provides a unified interface for accessing configuration values
with support for inheritance and SSOT compliance.

Author: Agent-6
Contract: SSOT-003: Configuration Management Consolidation
Date: 2025-08-28
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import logging
from functools import lru_cache

from constants import (
    DEFAULT_TIMEOUT, DEFAULT_RETRY_ATTEMPTS, DEFAULT_COLLECTION_INTERVAL,
    SYSTEM_ENABLED, PRIORITY_NORMAL
)
from validator import ConfigurationValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigurationManager:
    """Unified configuration manager with inheritance support."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.base_config = None
        self.system_configs = {}
        self.agent_configs = {}
        self.service_configs = {}
        self.cache = {}
        self.validator = ConfigurationValidator(config_dir)
        
        # Load all configurations
        self._load_configurations()
    
    def _load_configurations(self):
        """Load all configuration files in the correct order."""
        try:
            # Load base configuration first
            base_path = self.config_dir / "system" / "base.json"
            if base_path.exists():
                with open(base_path, 'r', encoding='utf-8') as f:
                    self.base_config = json.load(f)
                logger.info("Loaded base configuration")
            
            # Load system configurations
            system_dir = self.config_dir / "system"
            for config_file in system_dir.glob("*.json"):
                if config_file.name != "base.json":
                    with open(config_file, 'r', encoding='utf-8') as f:
                        self.system_configs[config_file.stem] = json.load(f)
            
            # Load agent configurations
            agent_dir = self.config_dir / "agents"
            for config_file in agent_dir.glob("*.json"):
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.agent_configs[config_file.stem] = json.load(f)
            
            # Load service configurations
            service_dir = self.config_dir / "services"
            for config_file in service_dir.glob("*.yaml"):
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.service_configs[config_file.stem] = yaml.safe_load(f)
            
            logger.info(f"Loaded {len(self.system_configs)} system configs, "
                       f"{len(self.agent_configs)} agent configs, "
                       f"{len(self.service_configs)} service configs")
            
        except Exception as e:
            logger.error(f"Error loading configurations: {e}")
            raise
    
    def get_config(self, key_path: str, default: Any = None, 
                   config_type: str = "auto") -> Any:
        """
        Get configuration value using dot notation path.
        
        Args:
            key_path: Dot-separated path to configuration value (e.g., "timeouts.default")
            default: Default value if key not found
            config_type: Type of configuration to search ("auto", "base", "system", "agent", "service")
        
        Returns:
            Configuration value or default
        """
        # Check cache first
        cache_key = f"{key_path}:{config_type}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Determine which configuration to search
        if config_type == "auto":
            value = self._get_config_auto(key_path, default)
        elif config_type == "base":
            value = self._get_config_from_dict(self.base_config, key_path, default)
        elif config_type == "system":
            value = self._get_config_from_system(key_path, default)
        elif config_type == "agent":
            value = self._get_config_from_agents(key_path, default)
        elif config_type == "service":
            value = self._get_config_from_services(key_path, default)
        else:
            value = default
        
        # Cache the result
        self.cache[cache_key] = value
        return value
    
    def _get_config_auto(self, key_path: str, default: Any) -> Any:
        """Automatically determine which configuration to search."""
        # Try base configuration first
        if self.base_config:
            value = self._get_config_from_dict(self.base_config, key_path, default)
            if value is not None and value != default:
                return value
        
        # Try system configurations
        value = self._get_config_from_system(key_path, None)
        if value is not None:
            return value
        
        # Try agent configurations
        value = self._get_config_from_agents(key_path, None)
        if value is not None:
            return value
        
        # Try service configurations
        value = self._get_config_from_services(key_path, None)
        if value is not None:
            return value
        
        return default
    
    def _get_config_from_dict(self, config_dict: Dict[str, Any], 
                             key_path: str, default: Any) -> Any:
        """Get configuration value from a dictionary using dot notation."""
        if not config_dict:
            return default
        
        keys = key_path.split('.')
        current = config_dict
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def _get_config_from_system(self, key_path: str, default: Any) -> Any:
        """Get configuration value from system configurations."""
        for config_name, config_data in self.system_configs.items():
            value = self._get_config_from_dict(config_data, key_path, None)
            if value is not None:
                return value
        return default
    
    def _get_config_from_agents(self, key_path: str, default: Any) -> Any:
        """Get configuration value from agent configurations."""
        for config_name, config_data in self.agent_configs.items():
            value = self._get_config_from_dict(config_data, key_path, None)
            if value is not None:
                return value
        return default
    
    def _get_config_from_services(self, key_path: str, default: Any) -> Any:
        """Get configuration value from service configurations."""
        for config_name, config_data in self.service_configs.items():
            value = self._get_config_from_dict(config_data, key_path, None)
            if value is not None:
                return value
        return default
    
    def get_timeout(self, timeout_type: str = "default") -> float:
        """Get timeout configuration value."""
        return self.get_config(f"timeouts.{timeout_type}", DEFAULT_TIMEOUT)
    
    def get_retry_attempts(self, retry_type: str = "default") -> int:
        """Get retry attempts configuration value."""
        return self.get_config(f"retry_settings.{retry_type}_attempts", DEFAULT_RETRY_ATTEMPTS)
    
    def get_retry_delay(self, retry_type: str = "default") -> float:
        """Get retry delay configuration value."""
        return self.get_config(f"retry_settings.{retry_type}_delay", 1.0)
    
    def get_collection_interval(self, interval_type: str = "default") -> int:
        """Get collection interval configuration value."""
        return self.get_config(f"collection_intervals.{interval_type}", DEFAULT_COLLECTION_INTERVAL)
    
    def is_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled."""
        return self.get_config(f"enable_flags.{feature}", SYSTEM_ENABLED)
    
    def get_priority_level(self, priority_name: str) -> int:
        """Get priority level by name."""
        return self.get_config(f"priority_levels.{priority_name}", PRIORITY_NORMAL)
    
    def get_queue_size(self, size_type: str = "default") -> int:
        """Get queue size configuration value."""
        return self.get_config(f"queue_settings.{size_type}_size", 1000)
    
    def get_performance_threshold(self, metric: str, threshold_type: str = "warning") -> int:
        """Get performance threshold configuration value."""
        return self.get_config(f"performance_thresholds.{metric}_{threshold_type}", 80)
    
    def get_port(self, service: str) -> int:
        """Get port configuration for a service."""
        return self.get_config(f"ports.{service}", 8080)
    
    def validate_configurations(self) -> Dict[str, Any]:
        """Validate all configurations for SSOT violations."""
        return self.validator.validate_all_configs()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of all loaded configurations."""
        return {
            "base_config": bool(self.base_config),
            "system_configs": list(self.system_configs.keys()),
            "agent_configs": list(self.agent_configs.keys()),
            "service_configs": list(self.service_configs.keys()),
            "total_configs": len(self.system_configs) + len(self.agent_configs) + len(self.service_configs) + (1 if self.base_config else 0)
        }
    
    def reload_configurations(self):
        """Reload all configurations from disk."""
        logger.info("Reloading configurations...")
        self.cache.clear()
        self._load_configurations()
        logger.info("Configurations reloaded")
    
    def export_config(self, config_type: str = "all") -> Dict[str, Any]:
        """Export configuration for external use."""
        if config_type == "all":
            return {
                "base": self.base_config,
                "system": self.system_configs,
                "agents": self.agent_configs,
                "services": self.service_configs
            }
        elif config_type == "base":
            return self.base_config
        elif config_type == "system":
            return self.system_configs
        elif config_type == "agents":
            return self.agent_configs
        elif config_type == "services":
            return self.service_configs
        else:
            raise ValueError(f"Unknown config type: {config_type}")

# Global configuration manager instance
config_manager = ConfigurationManager()

# Convenience functions
def get_config(key_path: str, default: Any = None, config_type: str = "auto") -> Any:
    """Get configuration value using the global configuration manager."""
    return config_manager.get_config(key_path, default, config_type)

def get_timeout(timeout_type: str = "default") -> float:
    """Get timeout configuration value."""
    return config_manager.get_timeout(timeout_type)

def get_retry_attempts(retry_type: str = "default") -> int:
    """Get retry attempts configuration value."""
    return config_manager.get_retry_attempts(retry_type)

def is_enabled(feature: str) -> bool:
    """Check if a feature is enabled."""
    return config_manager.is_enabled(feature)

def validate_configs() -> Dict[str, Any]:
    """Validate all configurations."""
    return config_manager.validate_configurations()

if __name__ == "__main__":
    # Test the configuration manager
    manager = ConfigurationManager()
    
    print("Configuration Summary:")
    print(json.dumps(manager.get_config_summary(), indent=2))
    
    print("\nSample Configuration Values:")
    print(f"Default Timeout: {manager.get_timeout()}")
    print(f"Default Retry Attempts: {manager.get_retry_attempts()}")
    print(f"System Enabled: {manager.is_enabled('system')}")
    print(f"Priority Normal: {manager.get_priority_level('normal')}")
    
    print("\nValidation Results:")
    validation_report = manager.validate_configurations()
    print(f"Total Violations: {validation_report['validation_summary']['total_violations']}")
    print(f"Duplicate Values: {validation_report['validation_summary']['duplicate_values']}")
