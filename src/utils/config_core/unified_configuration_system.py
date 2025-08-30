#!/usr/bin/env python3
"""
Unified Configuration System - Single Source of Truth for All Configuration

This module provides the main interface for the unified configuration system,
consolidating all configuration functionality from multiple duplicate implementations
into a single, maintainable configuration system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 2: Configuration System Consolidation
"""

import os
import yaml
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .config_loader import ConfigLoader
from .config_validator import ConfigValidator
from .environment_manager import EnvironmentManager


class UnifiedConfigurationSystem:
    """
    Unified configuration system for eliminating function duplication.
    
    This class consolidates all common configuration logic into a single,
    maintainable location, eliminating the need for duplicate configuration
    functions across the codebase.
    """
    
    def __init__(self, config_path: str = "config/services/unified.yaml"):
        """
        Initialize the unified configuration system.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config_loader = ConfigLoader(config_path)
        self.config_validator = ConfigValidator()
        self.environment_manager = EnvironmentManager()
        
        # Configuration state
        self.config_data: Dict[str, Any] = {}
        self.loaded = False
        self.last_loaded = None
        
        # Performance tracking
        self.total_loads = 0
        self.total_load_time = 0.0
    
    def load_config(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            True if configuration loaded successfully, False otherwise
        """
        start_time = time.time()
        
        try:
            # Load base configuration
            if not self.config_loader.load_config():
                return False
            
            # Get configuration data
            self.config_data = self.config_loader.get_config_data()
            
            # Apply environment overrides
            self.config_data = self.environment_manager.apply_environment_overrides(
                self.config_data
            )
            
            # Validate configuration
            validation_result = self.config_validator.validate_config(self.config_data)
            if not validation_result.is_valid():
                print(f"Configuration validation warnings: {validation_result.warnings}")
            
            # Update state
            self.loaded = True
            self.last_loaded = datetime.now()
            
            # Update performance tracking
            end_time = time.time()
            self.total_loads += 1
            self.total_load_time += (end_time - start_time)
            
            return True
            
        except Exception as e:
            print(f"Failed to load configuration: {e}")
            return False
    
    def load_config_from_path(self, config_path: str) -> bool:
        """
        Load configuration from a specific path.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            True if configuration loaded successfully, False otherwise
        """
        self.config_path = Path(config_path)
        self.config_loader = ConfigLoader(config_path)
        return self.load_config()
    
    def reload_config(self) -> bool:
        """
        Reload configuration from file.
        
        Returns:
            True if configuration reloaded successfully, False otherwise
        """
        self.loaded = False
        self.config_data.clear()
        return self.load_config()
    
    def get_config_data(self) -> Dict[str, Any]:
        """
        Get the loaded configuration data.
        
        Returns:
            Configuration data dictionary
        """
        if not self.loaded:
            if not self.load_config():
                return {}
        return self.config_data.copy()
    
    def get_config_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Dot notation path to configuration value (e.g., 'system.log_level')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if not self.loaded:
            if not self.load_config():
                return default
        
        keys = key_path.split(".")
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_config_section(self, section_name: str) -> Dict[str, Any]:
        """
        Get a configuration section.
        
        Args:
            section_name: Name of configuration section
            
        Returns:
            Configuration section dictionary
        """
        if not self.loaded:
            if not self.load_config():
                return {}
        
        return self.config_data.get(section_name, {})
    
    def set_config_value(self, key_path: str, value: Any) -> bool:
        """
        Set a configuration value using dot notation.
        
        Args:
            key_path: Dot notation path to configuration value
            value: Value to set
            
        Returns:
            True if value set successfully, False otherwise
        """
        if not self.loaded:
            if not self.load_config():
                return False
        
        keys = key_path.split(".")
        config = self.config_data
        
        try:
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Set the value
            config[keys[-1]] = value
            return True
            
        except Exception as e:
            print(f"Failed to set configuration value: {e}")
            return False
    
    def save_config(self, output_path: Optional[str] = None) -> bool:
        """
        Save configuration to file.
        
        Args:
            output_path: Output file path (uses config_path if not specified)
            
        Returns:
            True if configuration saved successfully, False otherwise
        """
        try:
            save_path = Path(output_path) if output_path else self.config_path
            
            # Determine file format
            if save_path.suffix.lower() == ".yaml":
                with open(save_path, "w", encoding="utf-8") as f:
                    yaml.dump(self.config_data, f, default_flow_style=False, indent=2)
            elif save_path.suffix.lower() == ".json":
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(self.config_data, f, indent=2)
            else:
                print(f"Unsupported output format: {save_path.suffix}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Failed to save configuration: {e}")
            return False
    
    def validate_config(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate configuration data.
        
        Args:
            config: Configuration to validate (uses loaded config if not specified)
            
        Returns:
            Validation result dictionary
        """
        if config is None:
            config = self.config_data
        
        validation_result = self.config_validator.validate_config(config)
        return {
            'valid': validation_result.is_valid(),
            'errors': validation_result.errors,
            'warnings': validation_result.warnings,
            'message': validation_result.message
        }
    
    def get_environment_summary(self) -> Dict[str, Any]:
        """
        Get summary of environment overrides.
        
        Returns:
            Environment override summary
        """
        return self.environment_manager.get_override_summary(self.config_data)
    
    def get_config_status(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration status.
        
        Returns:
            Configuration status dictionary
        """
        return {
            'loaded': self.loaded,
            'config_file': str(self.config_path),
            'last_loaded': self.last_loaded.isoformat() if self.last_loaded else None,
            'total_loads': self.total_loads,
            'average_load_time': (self.total_load_time / self.total_loads 
                                if self.total_loads > 0 else 0),
            'sections': list(self.config_data.keys()) if self.loaded else [],
            'environment_overrides': self.get_environment_summary(),
            'validation': self.validate_config()
        }
    
    def list_config_sections(self) -> List[str]:
        """
        List available configuration sections.
        
        Returns:
            List of configuration section names
        """
        if not self.loaded:
            if not self.load_config():
                return []
        return list(self.config_data.keys())
    
    def has_config_section(self, section_name: str) -> bool:
        """
        Check if configuration section exists.
        
        Args:
            section_name: Name of configuration section
            
        Returns:
            True if section exists, False otherwise
        """
        if not self.loaded:
            if not self.load_config():
                return False
        return section_name in self.config_data
    
    def get_config_file_path(self) -> str:
        """
        Get the configuration file path.
        
        Returns:
            Configuration file path as string
        """
        return str(self.config_path)
    
    def is_loaded(self) -> bool:
        """
        Check if configuration is loaded.
        
        Returns:
            True if configuration is loaded, False otherwise
        """
        return self.loaded
    
    def clear_config(self) -> None:
        """Clear loaded configuration data."""
        self.config_data.clear()
        self.loaded = False
        self.last_loaded = None
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for the configuration system.
        
        Returns:
            Dictionary with performance metrics
        """
        return {
            'total_loads': self.total_loads,
            'total_load_time': self.total_load_time,
            'average_load_time': (self.total_load_time / self.total_loads 
                                if self.total_loads > 0 else 0),
            'last_loaded': self.last_loaded.isoformat() if self.last_loaded else None
        }
    
    def reset_performance_stats(self) -> None:
        """Reset performance statistics."""
        self.total_loads = 0
        self.total_load_time = 0.0
