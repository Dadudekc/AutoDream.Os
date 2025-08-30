#!/usr/bin/env python3
"""
Unified Logging System - Single Source of Truth for All Logging

This module provides the main interface for the unified logging system,
consolidating all logging functionality from multiple duplicate implementations
into a single, maintainable logging system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 3: Logging System Consolidation
"""

import os
import logging
import logging.handlers
import yaml
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from .logging_manager import UnifiedLoggingManager
from .logging_setup import LoggingSetup
from .logging_config import LoggingConfig


class UnifiedLoggingSystem:
    """
    Unified logging system for eliminating function duplication.
    
    This class consolidates all common logging logic into a single,
    maintainable location, eliminating the need for duplicate logging
    functions across the codebase.
    """
    
    def __init__(self, config_file: str = "config/logging.yaml"):
        """
        Initialize the unified logging system.
        
        Args:
            config_file: Path to logging configuration file
        """
        self.config_file = Path(config_file)
        self.logging_manager = UnifiedLoggingManager(config_file)
        self.logging_setup = LoggingSetup()
        self.logging_config = LoggingConfig()
        
        # Logging state
        self.initialized = False
        self.last_initialized = None
        
        # Performance tracking
        self.total_logs = 0
        self.total_log_time = 0.0
    
    def initialize_logging(self, log_level: str = "INFO", 
                          log_file: Optional[str] = None,
                          environment: Optional[str] = None) -> bool:
        """
        Initialize the unified logging system.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
            environment: Environment (development, production, testing)
            
        Returns:
            True if logging initialized successfully, False otherwise
        """
        start_time = time.time()
        
        try:
            # Set environment if provided
            if environment:
                os.environ["ENVIRONMENT"] = environment
            
            # Initialize logging manager
            if not self.logging_manager.initialize():
                return False
            
            # Setup logging configuration
            if not self.logging_setup.setup_logging(log_level, log_file):
                return False
            
            # Update state
            self.initialized = True
            self.last_initialized = datetime.now()
            
            # Update performance tracking
            end_time = time.time()
            self.total_log_time += (end_time - start_time)
            
            return True
            
        except Exception as e:
            print(f"Failed to initialize logging: {e}")
            return False
    
    def get_logger(self, name: str, level: Optional[str] = None) -> logging.Logger:
        """
        Get a configured logger instance.
        
        Args:
            name: Logger name
            level: Optional logging level override
            
        Returns:
            Configured logger instance
        """
        if not self.initialized:
            self.initialize_logging()
        
        return self.logging_manager.get_logger(name, level)
    
    def setup_logging(self, log_level: str = "INFO", 
                     log_file: Optional[str] = None) -> bool:
        """
        Setup logging configuration.
        
        Args:
            log_level: Logging level
            log_file: Optional log file path
            
        Returns:
            True if setup successful, False otherwise
        """
        return self.logging_setup.setup_logging(log_level, log_file)
    
    def configure_logging_from_dict(self, config: Dict[str, Any]) -> bool:
        """
        Configure logging from a configuration dictionary.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if configuration successful, False otherwise
        """
        return self.logging_setup.configure_logging_from_dict(config)
    
    def configure_logging_from_file(self, config_file: str) -> bool:
        """
        Configure logging from a configuration file.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            True if configuration successful, False otherwise
        """
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
            return self.configure_logging_from_dict(config)
        except Exception as e:
            print(f"Failed to load logging config from file: {e}")
            return False
    
    def set_log_level(self, logger_name: str, level: str) -> bool:
        """
        Set log level for a specific logger.
        
        Args:
            logger_name: Name of logger
            level: Logging level
            
        Returns:
            True if level set successfully, False otherwise
        """
        try:
            logger = logging.getLogger(logger_name)
            numeric_level = getattr(logging, level.upper(), logging.INFO)
            logger.setLevel(numeric_level)
            return True
        except Exception as e:
            print(f"Failed to set log level: {e}")
            return False
    
    def add_file_handler(self, logger_name: str, file_path: str, 
                        level: Optional[str] = None) -> bool:
        """
        Add file handler to a logger.
        
        Args:
            logger_name: Name of logger
            file_path: Path to log file
            level: Optional logging level for file handler
            
        Returns:
            True if handler added successfully, False otherwise
        """
        try:
            logger = logging.getLogger(logger_name)
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(file_path)
            if level:
                numeric_level = getattr(logging, level.upper(), logging.INFO)
                file_handler.setLevel(numeric_level)
            
            formatter = logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)8s | %(message)s"
            )
            file_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            return True
            
        except Exception as e:
            print(f"Failed to add file handler: {e}")
            return False
    
    def add_console_handler(self, logger_name: str, 
                           level: Optional[str] = None) -> bool:
        """
        Add console handler to a logger.
        
        Args:
            logger_name: Name of logger
            level: Optional logging level for console handler
            
        Returns:
            True if handler added successfully, False otherwise
        """
        try:
            logger = logging.getLogger(logger_name)
            
            console_handler = logging.StreamHandler()
            if level:
                numeric_level = getattr(logging, level.upper(), logging.INFO)
                console_handler.setLevel(numeric_level)
            
            formatter = logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)8s | %(message)s"
            )
            console_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            return True
            
        except Exception as e:
            print(f"Failed to add console handler: {e}")
            return False
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get current logging configuration.
        
        Returns:
            Logging configuration dictionary
        """
        return self.logging_config.get_config()
    
    def update_logging_config(self, config: Dict[str, Any]) -> bool:
        """
        Update logging configuration.
        
        Args:
            config: New configuration dictionary
            
        Returns:
            True if update successful, False otherwise
        """
        return self.logging_config.update_config(config)
    
    def reload_logging_config(self) -> bool:
        """
        Reload logging configuration from file.
        
        Returns:
            True if reload successful, False otherwise
        """
        return self.logging_config.reload_config()
    
    def get_logging_status(self) -> Dict[str, Any]:
        """
        Get comprehensive logging status.
        
        Returns:
            Logging status dictionary
        """
        return {
            'initialized': self.initialized,
            'last_initialized': self.last_initialized.isoformat() if self.last_initialized else None,
            'config_file': str(self.config_file),
            'total_logs': self.total_logs,
            'total_log_time': self.total_log_time,
            'environment': os.getenv("ENVIRONMENT", "development"),
            'log_level': os.getenv("LOG_LEVEL", "INFO"),
            'config': self.get_logging_config()
        }
    
    def list_loggers(self) -> List[str]:
        """
        List all configured loggers.
        
        Returns:
            List of logger names
        """
        return list(self.logging_manager.loggers.keys())
    
    def clear_loggers(self) -> None:
        """Clear all configured loggers."""
        self.logging_manager.loggers.clear()
        self.initialized = False
        self.last_initialized = None
    
    def is_initialized(self) -> bool:
        """
        Check if logging system is initialized.
        
        Returns:
            True if initialized, False otherwise
        """
        return self.initialized
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for the logging system.
        
        Returns:
            Dictionary with performance metrics
        """
        return {
            'total_logs': self.total_logs,
            'total_log_time': self.total_log_time,
            'average_log_time': (self.total_log_time / self.total_logs 
                               if self.total_logs > 0 else 0),
            'last_initialized': self.last_initialized.isoformat() if self.last_initialized else None
        }
    
    def reset_performance_stats(self) -> None:
        """Reset performance statistics."""
        self.total_logs = 0
        self.total_log_time = 0.0
