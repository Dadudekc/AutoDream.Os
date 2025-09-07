#!/usr/bin/env python3
"""
Consolidated Config Loader - Single Source of Truth for Configuration Loading

This module consolidates all configuration loading functionality from multiple
duplicate implementations into a single, maintainable configuration system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 2: Configuration System Consolidation
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Consolidated configuration file loader.
    
    This class consolidates all configuration loading functionality from multiple
    duplicate implementations into a single, maintainable system.
    """
    
    def __init__(self, config_path: str = "config/services/unified.yaml"):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}
        self.loaded = False
    
    def load_config(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            True if configuration loaded successfully, False otherwise
        """
        try:
            if not self.config_path.exists():
                logger.error(f"Configuration file not found: {self.config_path}")
                return False
            
            with open(self.config_path, "r", encoding="utf-8") as f:
                if self.config_path.suffix.lower() == ".yaml":
                    self.config_data = yaml.safe_load(f)
                elif self.config_path.suffix.lower() == ".json":
                    self.config_data = json.load(f)
                else:
                    logger.error(f"Unsupported config file format: {self.config_path.suffix}")
                    return False
            
            self.loaded = True
            logger.info(f"Configuration loaded from {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
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
            logger.warning("Configuration not loaded, attempting to load now")
            self.load_config()
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
            logger.warning("Configuration not loaded, attempting to load now")
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
            logger.warning("Configuration not loaded, attempting to load now")
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
            logger.warning("Configuration not loaded, attempting to load now")
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
            logger.error(f"Failed to set configuration value: {e}")
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
                logger.error(f"Unsupported output format: {save_path.suffix}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
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
