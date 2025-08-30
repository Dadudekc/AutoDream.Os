#!/usr/bin/env python3
"""
Logging Service - Emergency Database Recovery System
Provides centralized logging functionality for all components
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class LoggingService:
    """Centralized logging service for emergency database recovery"""
    
    def __init__(self, log_level: str = "INFO", log_file: Optional[str] = None):
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.log_file = log_file
        self._loggers = {}
        
    def get_logger(self, name: str) -> logging.Logger:
        """Get or create a logger with the specified name"""
        if name in self._loggers:
            return self._loggers[name]
            
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        
        # Avoid duplicate handlers
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            # File handler if specified
            if self.log_file:
                try:
                    file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
                    file_handler.setLevel(self.log_level)
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                except Exception as e:
                    logger.warning(f"Could not create file handler: {e}")
        
        self._loggers[name] = logger
        return logger
    
    def set_log_level(self, level: str):
        """Set the logging level for all loggers"""
        self.log_level = getattr(logging, level.upper(), logging.INFO)
        for logger in self._loggers.values():
            logger.setLevel(self.log_level)
            for handler in logger.handlers:
                handler.setLevel(self.log_level)
    
    def log_emergency_event(self, event_type: str, message: str, severity: str = "INFO"):
        """Log emergency events with special formatting"""
        emergency_logger = self.get_logger("EMERGENCY_EVENTS")
        timestamp = datetime.now().isoformat()
        
        emergency_logger.log(
            getattr(logging, severity.upper(), logging.INFO),
            f"🚨 EMERGENCY EVENT [{event_type}] {timestamp}: {message}"
        )
    
    def log_recovery_action(self, action: str, target: str, status: str, details: str = ""):
        """Log recovery actions with structured information"""
        recovery_logger = self.get_logger("RECOVERY_ACTIONS")
        timestamp = datetime.now().isoformat()
        
        recovery_logger.info(
            f"🔄 RECOVERY ACTION [{action}] on {target} - Status: {status} - {timestamp}"
        )
        if details:
            recovery_logger.debug(f"Details: {details}")
    
    def log_audit_result(self, audit_type: str, issues_found: int, critical_count: int):
        """Log audit results with summary information"""
        audit_logger = self.get_logger("AUDIT_RESULTS")
        timestamp = datetime.now().isoformat()
        
        if critical_count > 0:
            audit_logger.warning(
                f"⚠️ AUDIT RESULT [{audit_type}] - {issues_found} issues, {critical_count} critical - {timestamp}"
            )
        else:
            audit_logger.info(
                f"✅ AUDIT RESULT [{audit_type}] - {issues_found} issues, {critical_count} critical - {timestamp}"
            )
