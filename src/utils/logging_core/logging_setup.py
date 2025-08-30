#!/usr/bin/env python3
"""
Consolidated Logging Setup - Single Source of Truth for Logging Setup

This module consolidates all logging setup functionality from multiple
duplicate implementations into a single, maintainable logging system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 3: Logging System Consolidation
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path


class LoggingSetup:
    """
    Consolidated logging setup utilities.
    
    This class consolidates all logging setup functionality from multiple
    duplicate implementations into a single, maintainable system.
    """
    
    def __init__(self):
        """Initialize the logging setup."""
        pass
    
    def setup_logging(self, log_level: str = "INFO", log_file: Optional[str] = None) -> bool:
        """
        Setup logging configuration.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
            
        Returns:
            True if setup successful, False otherwise
        """
        try:
            # Get numeric log level
            numeric_level = getattr(logging, log_level.upper(), logging.INFO)
            
            # Setup basic logging
            logging.basicConfig(
                level=numeric_level,
                format="%(asctime)s | %(name)s | %(levelname)8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            # Add file handler if specified
            if log_file:
                if not self._add_file_handler(log_file):
                    return False
            
            return True
            
        except Exception as e:
            print(f"Failed to setup logging: {e}")
            return False
    
    def get_logger(self, name: str, level: str = "INFO") -> logging.Logger:
        """
        Get a configured logger instance.
        
        Args:
            name: Logger name
            level: Logging level
            
        Returns:
            Configured logger instance
        """
        try:
            logger = logging.getLogger(name)
            numeric_level = getattr(logging, level.upper(), logging.INFO)
            logger.setLevel(numeric_level)
            return logger
        except Exception as e:
            print(f"Failed to get logger: {e}")
            return logging.getLogger(name)
    
    def configure_logging_from_dict(self, config: Dict[str, Any]) -> bool:
        """
        Configure logging from a configuration dictionary.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if configuration successful, False otherwise
        """
        try:
            log_level = config.get("log_level", "INFO")
            log_file = config.get("log_file")
            return self.setup_logging(log_level, log_file)
        except Exception as e:
            print(f"Failed to configure logging from dict: {e}")
            return False
    
    def _add_file_handler(self, log_file: str) -> bool:
        """
        Add file handler to root logger.
        
        Args:
            log_file: Path to log file
            
        Returns:
            True if handler added successfully, False otherwise
        """
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s")
            )
            
            root_logger = logging.getLogger()
            root_logger.addHandler(file_handler)
            
            return True
            
        except Exception as e:
            print(f"Failed to add file handler: {e}")
            return False
    
    def setup_logging_for_module(self, module_name: str, log_level: str = "INFO") -> logging.Logger:
        """
        Setup logging for a specific module.
        
        Args:
            module_name: Name of the module
            log_level: Logging level for the module
            
        Returns:
            Configured logger for the module
        """
        return self.get_logger(module_name, log_level)
    
    def setup_logging_with_handlers(self, log_level: str = "INFO", 
                                   console: bool = True, 
                                   file_path: Optional[str] = None) -> bool:
        """
        Setup logging with specific handlers.
        
        Args:
            log_level: Logging level
            console: Whether to enable console logging
            file_path: Optional file logging path
            
        Returns:
            True if setup successful, False otherwise
        """
        try:
            # Get numeric log level
            numeric_level = getattr(logging, log_level.upper(), logging.INFO)
            
            # Clear existing handlers
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # Setup basic configuration
            logging.basicConfig(
                level=numeric_level,
                format="%(asctime)s | %(name)s | %(levelname)8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            # Add console handler if enabled
            if console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(
                    logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s")
                )
                root_logger.addHandler(console_handler)
            
            # Add file handler if specified
            if file_path:
                if not self._add_file_handler(file_path):
                    return False
            
            return True
            
        except Exception as e:
            print(f"Failed to setup logging with handlers: {e}")
            return False
    
    def setup_logging_for_development(self) -> bool:
        """
        Setup logging for development environment.
        
        Returns:
            True if setup successful, False otherwise
        """
        return self.setup_logging_with_handlers(
            log_level="DEBUG",
            console=True,
            file_path="logs/development.log"
        )
    
    def setup_logging_for_production(self) -> bool:
        """
        Setup logging for production environment.
        
        Returns:
            True if setup successful, False otherwise
        """
        return self.setup_logging_with_handlers(
            log_level="WARNING",
            console=False,
            file_path="logs/production.log"
        )
    
    def setup_logging_for_testing(self) -> bool:
        """
        Setup logging for testing environment.
        
        Returns:
            True if setup successful, False otherwise
        """
        return self.setup_logging_with_handlers(
            log_level="DEBUG",
            console=True,
            file_path="logs/testing.log"
        )
    
    def get_logging_info(self) -> Dict[str, Any]:
        """
        Get information about current logging setup.
        
        Returns:
            Logging information dictionary
        """
        try:
            root_logger = logging.getLogger()
            return {
                'level': logging.getLevelName(root_logger.level),
                'handlers': len(root_logger.handlers),
                'handlers_info': [
                    {
                        'type': type(handler).__name__,
                        'level': logging.getLevelName(handler.level),
                        'formatter': type(handler.formatter).__name__ if handler.formatter else None
                    }
                    for handler in root_logger.handlers
                ]
            }
        except Exception as e:
            return {'error': str(e)}
