#!/usr/bin/env python3
"""
Consolidated Logging Manager - Single Source of Truth for Logging Management

This module consolidates all logging management functionality from multiple
duplicate implementations into a single, maintainable logging system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 3: Logging System Consolidation
"""

import os
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml


class UnifiedLoggingManager:
    """
    Consolidated logging manager for the unified logging system.
    
    This class consolidates all logging management functionality from multiple
    duplicate implementations into a single, maintainable system.
    """
    
    def __init__(self, config_file: str = "config/logging.yaml"):
        """
        Initialize the logging manager.
        
        Args:
            config_file: Path to logging configuration file
        """
        self.config_file = Path(config_file)
        self.config = {}
        self.loggers: Dict[str, logging.Logger] = {}
        self.initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the logging manager.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Load configuration
            self.config = self._load_config()
            
            # Setup global logging
            self._setup_global_logging()
            
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"Failed to initialize logging manager: {e}")
            return False
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load logging configuration from YAML file.
        
        Returns:
            Logging configuration dictionary
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return yaml.safe_load(f) or {}
            else:
                print(f"⚠️  Logging config not found: {self.config_file}")
                return self._get_default_config()
        except Exception as e:
            print(f"❌ Failed to load logging config: {e}")
            return self._get_default_config()
    
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
                "development": {"level": "DEBUG", "console": True, "file": False},
                "production": {"level": "WARNING", "console": False, "file": True},
                "testing": {"level": "DEBUG", "console": True, "file": True}
            },
            "debug": {
                "enabled": False,
                "flask_debug": False,
                "verbose_logging": False
            }
        }
    
    def _setup_global_logging(self):
        """Setup global logging configuration."""
        try:
            # Get environment
            env = os.getenv("ENVIRONMENT", "development")
            env_config = self.config.get("environments", {}).get(env, {})
            
            # Get log level from environment or config
            log_level = os.getenv("LOG_LEVEL") or env_config.get("level") or self.config.get("global", {}).get("level", "INFO")
            numeric_level = getattr(logging, log_level.upper(), logging.INFO)
            
            # Clear existing handlers
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # Setup basic configuration
            logging.basicConfig(
                level=numeric_level,
                format=self.config.get("global", {}).get("format", "%(asctime)s | %(levelname)8s | %(message)s"),
                datefmt=self.config.get("global", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            
            # Add console handler if enabled
            if env_config.get("console", True):
                self._add_console_handler(root_logger, env_config)
            
            # Add file handler if enabled
            if env_config.get("file", False):
                file_path = env_config.get("file_path", f"logs/{env}.log")
                self._add_file_handler(root_logger, file_path)
            
            print(f"✅ Unified logging configured: {env} environment, level={log_level}")
            
        except Exception as e:
            print(f"❌ Failed to setup global logging: {e}")
            # Fallback to basic logging
            logging.basicConfig(level=logging.INFO)
    
    def _add_console_handler(self, logger: logging.Logger, env_config: Dict[str, Any]):
        """Add console handler to logger."""
        try:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG if env_config.get("level") == "DEBUG" else logging.INFO)
            
            formatter = logging.Formatter(
                self.config.get("global", {}).get("format", "%(asctime)s | %(levelname)8s | %(message)s"),
                self.config.get("global", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            console_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"Failed to add console handler: {e}")
    
    def _add_file_handler(self, logger: logging.Logger, file_path: str):
        """Add file handler to logger."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(logging.DEBUG)
            
            formatter = logging.Formatter(
                self.config.get("global", {}).get("format", "%(asctime)s | %(levelname)8s | %(message)s"),
                self.config.get("global", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            file_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            
        except Exception as e:
            print(f"Failed to add file handler: {e}")
    
    def get_logger(self, name: str, level: Optional[str] = None) -> logging.Logger:
        """
        Get a configured logger instance.
        
        Args:
            name: Logger name
            level: Optional logging level override
            
        Returns:
            Configured logger instance
        """
        if name not in self.loggers:
            logger = logging.getLogger(name)
            if level:
                numeric_level = getattr(logging, level.upper(), logging.INFO)
                logger.setLevel(numeric_level)
            self.loggers[name] = logger
        
        return self.loggers[name]
    
    def set_logger_level(self, name: str, level: str) -> bool:
        """
        Set log level for a specific logger.
        
        Args:
            name: Logger name
            level: Logging level
            
        Returns:
            True if level set successfully, False otherwise
        """
        try:
            logger = self.get_logger(name)
            numeric_level = getattr(logging, level.upper(), logging.INFO)
            logger.setLevel(numeric_level)
            return True
        except Exception as e:
            print(f"Failed to set logger level: {e}")
            return False
    
    def add_handler_to_logger(self, logger_name: str, handler: logging.Handler) -> bool:
        """
        Add a handler to a specific logger.
        
        Args:
            logger_name: Logger name
            handler: Logging handler to add
            
        Returns:
            True if handler added successfully, False otherwise
        """
        try:
            logger = self.get_logger(logger_name)
            logger.addHandler(handler)
            return True
        except Exception as e:
            print(f"Failed to add handler to logger: {e}")
            return False
    
    def remove_handler_from_logger(self, logger_name: str, handler: logging.Handler) -> bool:
        """
        Remove a handler from a specific logger.
        
        Args:
            logger_name: Logger name
            handler: Logging handler to remove
            
        Returns:
            True if handler removed successfully, False otherwise
        """
        try:
            logger = self.get_logger(logger_name)
            logger.removeHandler(handler)
            return True
        except Exception as e:
            print(f"Failed to remove handler from logger: {e}")
            return False
    
    def get_logger_info(self, name: str) -> Dict[str, Any]:
        """
        Get information about a specific logger.
        
        Args:
            name: Logger name
            
        Returns:
            Logger information dictionary
        """
        try:
            logger = self.get_logger(name)
            return {
                'name': name,
                'level': logging.getLevelName(logger.level),
                'handlers': len(logger.handlers),
                'propagate': logger.propagate,
                'disabled': logger.disabled
            }
        except Exception as e:
            return {'error': str(e)}
    
    def list_loggers(self) -> List[str]:
        """
        List all configured loggers.
        
        Returns:
            List of logger names
        """
        return list(self.loggers.keys())
    
    def clear_loggers(self) -> None:
        """Clear all configured loggers."""
        self.loggers.clear()
        self.initialized = False
    
    def reload_config(self) -> bool:
        """
        Reload logging configuration.
        
        Returns:
            True if reload successful, False otherwise
        """
        try:
            self.config = self._load_config()
            self._setup_global_logging()
            return True
        except Exception as e:
            print(f"Failed to reload logging config: {e}")
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current logging configuration.
        
        Returns:
            Logging configuration dictionary
        """
        return self.config.copy()
    
    def is_initialized(self) -> bool:
        """
        Check if logging manager is initialized.
        
        Returns:
            True if initialized, False otherwise
        """
        return self.initialized
