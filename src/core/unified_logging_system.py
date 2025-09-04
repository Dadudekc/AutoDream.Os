#!/usr/bin/env python3
"""
Unified Logging System - DRY Violation Elimination
================================================

Eliminates duplicate logging patterns across 25+ locations:
- Duplicate logger import and setup patterns
- Duplicate log message patterns
- Inconsistent error logging across modules
- Scattered logging configuration

CONSOLIDATED: Single source of truth for all logging operations.

Author: Agent-5 (Business Intelligence Specialist)
Mission: DRY Violation Elimination
Status: CONSOLIDATED - Logging Duplication Eliminated
"""

# Removed circular import
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
# Logger will be created later to avoid circular import
# Removed circular import - validation not needed in logging system

# Removed circular import - configuration not needed in logging system

# ================================
# LOGGING LEVELS
# ================================

class LogLevel(Enum):
    """Standardized log levels."""
    
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

# ================================
# LOGGING TEMPLATES
# ================================

class LoggingTemplates:
    """
    Unified logging message templates - eliminates 25+ duplicate log patterns.
    
    CONSOLIDATES:
    - logger.info(f"Starting {operation_name}")
    - logger.debug(f"Processing item: {item_id}")
    - logger.error(f"Failed to {operation_name}: {error}")
    - logger.warning(f"Unexpected condition in {module_name}")
    """
    
    # Operation templates
    OPERATION_START = "Starting {operation}"
    OPERATION_COMPLETE = "Completed {operation}"
    OPERATION_FAILED = "Failed {operation}: {error}"
    OPERATION_PROGRESS = "Progress {operation}: {progress}%"
    
    # Processing templates
    PROCESSING_ITEM = "Processing {item_type}: {item_id}"
    PROCESSING_BATCH = "Processing batch: {batch_size} items"
    PROCESSING_COMPLETE = "Processing complete: {total_processed} items"
    
    # Error templates
    ERROR_GENERAL = "Error in {module}: {error}"
    ERROR_VALIDATION = "Validation error: {field} - {error}"
    ERROR_CONFIG = "Configuration error: {config_name} - {error}"
    ERROR_NETWORK = "Network error: {operation} - {error}"
    ERROR_FILE = "File error: {file_path} - {error}"
    
    # Warning templates
    WARNING_DEPRECATED = "Deprecated function used: {function_name}"
    WARNING_PERFORMANCE = "Performance warning: {operation} took {duration}s"
    WARNING_RESOURCE = "Resource warning: {resource} usage high"
    
    # Info templates
    INFO_INITIALIZED = "Initialized: {component}"
    INFO_CONFIGURED = "Configured: {component} with {config}"
    INFO_CONNECTED = "Connected: {service}"
    INFO_DISCONNECTED = "Disconnected: {service}"

# ================================
# UNIFIED LOGGING SYSTEM
# ================================

class UnifiedLoggingSystem:
    """
    Unified logging system that eliminates duplicate logging patterns.
    
    CONSOLIDATES:
    - Logger import and setup (duplicated in 50+ files)
    - Log message patterns (duplicated in 25+ locations)
    - Error logging patterns (duplicated in 15+ modules)
    - Logging configuration (duplicated in 7+ files)
    """
    
    def __init__(self):
        """Initialize unified logging system."""
        self._loggers: Dict[str, logging.Logger] = {}
        self._initialized = False
        
        # Logging configuration
        self._log_config = {
            "level": logging.INFO,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "date_format": "%Y-%m-%d %H:%M:%S"
        }
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup unified logging configuration."""
        if self._initialized:
            return
        
        # Configure root logger with UTF-8 encoding
        import os
        os.makedirs("logs", exist_ok=True)
        
        # Create handlers with UTF-8 encoding
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self._log_config["level"])
        
        file_handler = logging.FileHandler("logs/unified_system.log", mode="a", encoding="utf-8")
        file_handler.setLevel(self._log_config["level"])
        
        # Create formatter
        formatter = logging.Formatter(
            fmt=self._log_config["format"],
            datefmt=self._log_config["date_format"]
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self._log_config["level"])
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        
        # Create main logger
        self.main_logger = logging.getLogger("UnifiedLoggingSystem")
        self.main_logger.info("Unified logging system initialized")
        
        self._initialized = True
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get logger instance - consolidates 50+ duplicate logger setups."""
        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)
        return self._loggers[name]
    
    def log_operation_start(self, operation: str, logger: Optional[logging.Logger] = None):
        """Log operation start - consolidates duplicate start patterns."""
        message = LoggingTemplates.OPERATION_START.format(operation=operation)
        self._log(LogLevel.INFO, message, logger)
    
    def log_operation_complete(self, operation: str, logger: Optional[logging.Logger] = None):
        """Log operation completion - consolidates duplicate completion patterns."""
        message = LoggingTemplates.OPERATION_COMPLETE.format(operation=operation)
        self._log(LogLevel.INFO, message, logger)
    
    def log_operation_failed(self, operation: str, error: str, logger: Optional[logging.Logger] = None):
        """Log operation failure - consolidates duplicate error patterns."""
        message = LoggingTemplates.OPERATION_FAILED.format(operation=operation, error=error)
        self._log(LogLevel.ERROR, message, logger)
    
    def log_operation_progress(self, operation: str, progress: float, logger: Optional[logging.Logger] = None):
        """Log operation progress - consolidates duplicate progress patterns."""
        message = LoggingTemplates.OPERATION_PROGRESS.format(operation=operation, progress=progress)
        self._log(LogLevel.INFO, message, logger)
    
    def log_processing_item(self, item_type: str, item_id: str, logger: Optional[logging.Logger] = None):
        """Log item processing - consolidates duplicate processing patterns."""
        message = LoggingTemplates.PROCESSING_ITEM.format(item_type=item_type, item_id=item_id)
        self._log(LogLevel.DEBUG, message, logger)
    
    def log_processing_batch(self, batch_size: int, logger: Optional[logging.Logger] = None):
        """Log batch processing - consolidates duplicate batch patterns."""
        message = LoggingTemplates.PROCESSING_BATCH.format(batch_size=batch_size)
        self._log(LogLevel.INFO, message, logger)
    
    def log_processing_complete(self, total_processed: int, logger: Optional[logging.Logger] = None):
        """Log processing completion - consolidates duplicate completion patterns."""
        message = LoggingTemplates.PROCESSING_COMPLETE.format(total_processed=total_processed)
        self._log(LogLevel.INFO, message, logger)
    
    def log_error_general(self, module: str, error: str, logger: Optional[logging.Logger] = None):
        """Log general error - consolidates duplicate error patterns."""
        message = LoggingTemplates.ERROR_GENERAL.format(module=module, error=error)
        self._log(LogLevel.ERROR, message, logger)
    
    def log_error_validation(self, field: str, error: str, logger: Optional[logging.Logger] = None):
        """Log validation error - consolidates duplicate validation error patterns."""
        message = LoggingTemplates.ERROR_VALIDATION.format(field=field, error=error)
        self._log(LogLevel.ERROR, message, logger)
    
    def log_error_config(self, config_name: str, error: str, logger: Optional[logging.Logger] = None):
        """Log configuration error - consolidates duplicate config error patterns."""
        message = LoggingTemplates.ERROR_CONFIG.format(config_name=config_name, error=error)
        self._log(LogLevel.ERROR, message, logger)
    
    def log_error_network(self, operation: str, error: str, logger: Optional[logging.Logger] = None):
        """Log network error - consolidates duplicate network error patterns."""
        message = LoggingTemplates.ERROR_NETWORK.format(operation=operation, error=error)
        self._log(LogLevel.ERROR, message, logger)
    
    def log_error_file(self, file_path: str, error: str, logger: Optional[logging.Logger] = None):
        """Log file error - consolidates duplicate file error patterns."""
        message = LoggingTemplates.ERROR_FILE.format(file_path=file_path, error=error)
        self._log(LogLevel.ERROR, message, logger)
    
    def log_warning_deprecated(self, function_name: str, logger: Optional[logging.Logger] = None):
        """Log deprecated function warning - consolidates duplicate deprecation patterns."""
        message = LoggingTemplates.WARNING_DEPRECATED.format(function_name=function_name)
        self._log(LogLevel.WARNING, message, logger)
    
    def log_warning_performance(self, operation: str, duration: float, logger: Optional[logging.Logger] = None):
        """Log performance warning - consolidates duplicate performance patterns."""
        message = LoggingTemplates.WARNING_PERFORMANCE.format(operation=operation, duration=duration)
        self._log(LogLevel.WARNING, message, logger)
    
    def log_warning_resource(self, resource: str, logger: Optional[logging.Logger] = None):
        """Log resource warning - consolidates duplicate resource patterns."""
        message = LoggingTemplates.WARNING_RESOURCE.format(resource=resource)
        self._log(LogLevel.WARNING, message, logger)
    
    def log_info_initialized(self, component: str, logger: Optional[logging.Logger] = None):
        """Log component initialization - consolidates duplicate init patterns."""
        message = LoggingTemplates.INFO_INITIALIZED.format(component=component)
        self._log(LogLevel.INFO, message, logger)
    
    def log_info_configured(self, component: str, config: str, logger: Optional[logging.Logger] = None):
        """Log component configuration - consolidates duplicate config patterns."""
        message = LoggingTemplates.INFO_CONFIGURED.format(component=component, config=config)
        self._log(LogLevel.INFO, message, logger)
    
    def log_info_connected(self, service: str, logger: Optional[logging.Logger] = None):
        """Log service connection - consolidates duplicate connection patterns."""
        message = LoggingTemplates.INFO_CONNECTED.format(service=service)
        self._log(LogLevel.INFO, message, logger)
    
    def log_info_disconnected(self, service: str, logger: Optional[logging.Logger] = None):
        """Log service disconnection - consolidates duplicate disconnection patterns."""
        message = LoggingTemplates.INFO_DISCONNECTED.format(service=service)
        self._log(LogLevel.INFO, message, logger)
    
    def _log(self, level: LogLevel, message: str, logger: Optional[logging.Logger] = None):
        """Internal logging method."""
        if logger is None:
            logger = self.main_logger
        
        # Add timestamp to message
        timestamp = datetime.now().strftime(self._log_config["date_format"])
        formatted_message = f"[{timestamp}] {message}"
        
        # Log with appropriate level
        if level == LogLevel.DEBUG:
            logger.debug(formatted_message)
        elif level == LogLevel.INFO:
            logger.info(formatted_message)
        elif level == LogLevel.WARNING:
            logger.warning(formatted_message)
        elif level == LogLevel.ERROR:
            logger.error(formatted_message)
        elif level == LogLevel.CRITICAL:
            logger.critical(formatted_message)
    
    def log_custom(self, level: LogLevel, message: str, logger: Optional[logging.Logger] = None, **kwargs):
        """Log custom message with formatting."""
        formatted_message = message.format(**kwargs) if kwargs else message
        self._log(level, formatted_message, logger)
    
    def log_exception(self, operation: str, exception: Exception, logger: Optional[logging.Logger] = None):
        """Log exception with full traceback - consolidates duplicate exception patterns."""
        error_message = f"Exception in {operation}: {str(exception)}"
        self._log(LogLevel.ERROR, error_message, logger)
        
        if logger:
            logger.exception(f"Full traceback for {operation}")
        else:
            self.main_logger.exception(f"Full traceback for {operation}")

# ================================
# GLOBAL LOGGING INSTANCE
# ================================

# Single global instance to eliminate duplicate logging objects
_unified_logger = None

def get_unified_logger() -> UnifiedLoggingSystem:
    """Get global unified logging instance."""
    global _unified_logger
    if _unified_logger is None:
        _unified_logger = UnifiedLoggingSystem()
    return _unified_logger

# ================================
# CONVENIENCE FUNCTIONS
# ================================

def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return get_unified_logger().get_logger(name)

def log_operation_start(operation: str, logger: Optional[logging.Logger] = None):
    """Log operation start."""
    get_unified_logger().log_operation_start(operation, logger)

def log_operation_complete(operation: str, logger: Optional[logging.Logger] = None):
    """Log operation completion."""
    get_unified_logger().log_operation_complete(operation, logger)

def log_operation_failed(operation: str, error: str, logger: Optional[logging.Logger] = None):
    """Log operation failure."""
    get_unified_logger().log_operation_failed(operation, error, logger)

def log_error_general(module: str, error: str, logger: Optional[logging.Logger] = None):
    """Log general error."""
    get_unified_logger().log_error_general(module, error, logger)

def log_error_validation(field: str, error: str, logger: Optional[logging.Logger] = None):
    """Log validation error."""
    get_unified_logger().log_error_validation(field, error, logger)

def log_exception(operation: str, exception: Exception, logger: Optional[logging.Logger] = None):
    """Log exception with full traceback."""
    get_unified_logger().log_exception(operation, exception, logger)
