#!/usr/bin/env python3
"""
Logging Config - Logging Configuration Management

This module provides logging configuration management functionality for the unified
logging system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 3: Logging System Consolidation
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging


class LoggingConfig:
    """
    Logging configuration manager for the unified logging system.
    
    This class provides logging configuration management functionality.
    """
    
    def __init__(self, config_file: str = "config/logging.yaml"):
        """
        Initialize the logging configuration manager.
        
        Args:
            config_file: Path to logging configuration file
        """
        self.config_file = Path(config_file)
        self.config = {}
        self.loaded = False
    
    def load_config(self) -> bool:
        """
        Load logging configuration from file.
        
        Returns:
            True if configuration loaded successfully, False otherwise
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
            else:
                self.config = self._get_default_config()
            
            self.loaded = True
            return True
            
        except Exception as e:
            print(f"Failed to load logging config: {e}")
            self.config = self._get_default_config()
            return False
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default logging configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "global": {
                "level": "INFO",
                "format": "%(asctime)s | %(name)s | %(levelname)8s | %(message)s",
                "date_format": "%Y-%m-%d %H:%M:%S"
            },
            "environments": {
                "development": {
                    "level": "DEBUG",
                    "console": True,
                    "file": False,
                    "file_path": "logs/development.log"
                },
                "production": {
                    "level": "WARNING",
                    "console": False,
                    "file": True,
                    "file_path": "logs/production.log"
                },
                "testing": {
                    "level": "DEBUG",
                    "console": True,
                    "file": True,
                    "file_path": "logs/testing.log"
                }
            },
            "modules": {
                "default": {
                    "level": "INFO",
                    "console": True,
                    "file": False
                }
            },
            "debug": {
                "enabled": False,
                "flask_debug": False,
                "verbose_logging": False
            }
        }
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current logging configuration.
        
        Returns:
            Logging configuration dictionary
        """
        if not self.loaded:
            self.load_config()
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """
        Update logging configuration.
        
        Args:
            new_config: New configuration dictionary
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            self.config.update(new_config)
            return True
        except Exception as e:
            print(f"Failed to update logging config: {e}")
            return False
    
    def reload_config(self) -> bool:
        """
        Reload logging configuration from file.
        
        Returns:
            True if reload successful, False otherwise
        """
        self.loaded = False
        return self.load_config()
    
    def save_config(self, output_path: Optional[str] = None) -> bool:
        """
        Save logging configuration to file.
        
        Args:
            output_path: Output file path (uses config_file if not specified)
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            save_path = Path(output_path) if output_path else self.config_file
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Failed to save logging config: {e}")
            return False
    
    def get_environment_config(self, environment: Optional[str] = None) -> Dict[str, Any]:
        """
        Get configuration for a specific environment.
        
        Args:
            environment: Environment name (uses current environment if not specified)
            
        Returns:
            Environment configuration dictionary
        """
        if not self.loaded:
            self.load_config()
        
        env = environment or os.getenv("ENVIRONMENT", "development")
        return self.config.get("environments", {}).get(env, {})
    
    def get_module_config(self, module_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific module.
        
        Args:
            module_name: Module name
            
        Returns:
            Module configuration dictionary
        """
        if not self.loaded:
            self.load_config()
        
        return self.config.get("modules", {}).get(module_name, self.config.get("modules", {}).get("default", {}))
    
    def get_global_config(self) -> Dict[str, Any]:
        """
        Get global logging configuration.
        
        Returns:
            Global configuration dictionary
        """
        if not self.loaded:
            self.load_config()
        
        return self.config.get("global", {})
    
    def set_environment_config(self, environment: str, config: Dict[str, Any]) -> bool:
        """
        Set configuration for a specific environment.
        
        Args:
            environment: Environment name
            config: Environment configuration
            
        Returns:
            True if set successful, False otherwise
        """
        try:
            if "environments" not in self.config:
                self.config["environments"] = {}
            
            self.config["environments"][environment] = config
            return True
            
        except Exception as e:
            print(f"Failed to set environment config: {e}")
            return False
    
    def set_module_config(self, module_name: str, config: Dict[str, Any]) -> bool:
        """
        Set configuration for a specific module.
        
        Args:
            module_name: Module name
            config: Module configuration
            
        Returns:
            True if set successful, False otherwise
        """
        try:
            if "modules" not in self.config:
                self.config["modules"] = {}
            
            self.config["modules"][module_name] = config
            return True
            
        except Exception as e:
            print(f"Failed to set module config: {e}")
            return False
    
    def set_global_config(self, config: Dict[str, Any]) -> bool:
        """
        Set global logging configuration.
        
        Args:
            config: Global configuration
            
        Returns:
            True if set successful, False otherwise
        """
        try:
            self.config["global"] = config
            return True
            
        except Exception as e:
            print(f"Failed to set global config: {e}")
            return False
    
    def get_config_file_path(self) -> str:
        """
        Get the configuration file path.
        
        Returns:
            Configuration file path as string
        """
        return str(self.config_file)
    
    def is_loaded(self) -> bool:
        """
        Check if configuration is loaded.
        
        Returns:
            True if configuration is loaded, False otherwise
        """
        return self.loaded
    
    def clear_config(self) -> None:
        """Clear loaded configuration."""
        self.config.clear()
        self.loaded = False
