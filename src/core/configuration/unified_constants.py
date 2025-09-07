#!/usr/bin/env python3
"""
Unified Configuration Constants - Agent Cellphone V2
==================================================

Consolidated configuration constants system that eliminates duplication across
multiple configuration files. Provides single source of truth for all application
constants, settings, and default values.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any, Union, Optional
from dataclasses import dataclass, field
from enum import Enum
import os
import logging


# ============================================================================
# UNIFIED CONFIGURATION CONSTANTS
# ============================================================================

class ConfigCategory(Enum):
    """Configuration category enumeration."""
    GLOBAL = "global"
    LOGGING = "logging"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    MESSAGING = "messaging"
    AI_ML = "ai_ml"
    FSM = "fsm"
    REFACTORING = "refactoring"
    TESTING = "testing"
    NETWORK = "network"
    SECURITY = "security"
    DATABASE = "database"
    CUSTOM = "custom"


class ConfigPriority(Enum):
    """Configuration priority enumeration."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    OPTIONAL = 5


@dataclass
class ConfigConstant:
    """Configuration constant definition."""
    name: str
    value: Any
    category: ConfigCategory
    description: str = ""
    priority: ConfigPriority = ConfigPriority.MEDIUM
    is_environment_override: bool = False
    environment_key: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None


# ============================================================================
# GLOBAL APPLICATION CONSTANTS
# ============================================================================

# Global logging level for the application
LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)

# Standard timestamp format for task identifiers
TASK_ID_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S_%f"

# Application metadata
APP_NAME = "Agent Cellphone V2"
APP_VERSION = "2.0.0"
APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development")

# ============================================================================
# PERFORMANCE CONSTANTS
# ============================================================================

# Default worker configurations
DEFAULT_MAX_WORKERS = int(os.getenv("DEFAULT_MAX_WORKERS", "4"))
DEFAULT_THREAD_POOL_SIZE = int(os.getenv("DEFAULT_THREAD_POOL_SIZE", "10"))
DEFAULT_PROCESS_POOL_SIZE = int(os.getenv("DEFAULT_PROCESS_POOL_SIZE", "4"))

# Cache configurations
DEFAULT_CACHE_SIZE = int(os.getenv("DEFAULT_CACHE_SIZE", "1000"))
DEFAULT_CACHE_TTL = int(os.getenv("DEFAULT_CACHE_TTL", "3600"))
DEFAULT_BATCH_SIZE = int(os.getenv("DEFAULT_BATCH_SIZE", "100"))

# Timeout configurations
DEFAULT_OPERATION_TIMEOUT = float(os.getenv("DEFAULT_OPERATION_TIMEOUT", "30.0"))
DEFAULT_REQUEST_TIMEOUT = float(os.getenv("DEFAULT_REQUEST_TIMEOUT", "30.0"))
DEFAULT_CONNECTION_TIMEOUT = float(os.getenv("DEFAULT_CONNECTION_TIMEOUT", "10.0"))

# ============================================================================
# QUALITY MONITORING CONSTANTS
# ============================================================================

# Quality check intervals
DEFAULT_CHECK_INTERVAL = float(os.getenv("DEFAULT_CHECK_INTERVAL", "30.0"))
DEFAULT_HEALTH_CHECK_INTERVAL = float(os.getenv("DEFAULT_HEALTH_CHECK_INTERVAL", "60.0"))

# Quality thresholds
DEFAULT_COVERAGE_THRESHOLD = float(os.getenv("DEFAULT_COVERAGE_THRESHOLD", "80.0"))
DEFAULT_PERFORMANCE_THRESHOLD = float(os.getenv("DEFAULT_PERFORMANCE_THRESHOLD", "100.0"))
DEFAULT_ERROR_THRESHOLD = int(os.getenv("DEFAULT_ERROR_THRESHOLD", "0"))

# Quality history and retention
DEFAULT_HISTORY_WINDOW = int(os.getenv("DEFAULT_HISTORY_WINDOW", "100"))
DEFAULT_RETENTION_DAYS = int(os.getenv("DEFAULT_RETENTION_DAYS", "30"))

# ============================================================================
# MESSAGING SERVICE CONSTANTS
# ============================================================================

# Default messaging settings
DEFAULT_MESSAGING_MODE = os.getenv("DEFAULT_MESSAGING_MODE", "pyautogui")
DEFAULT_COORDINATE_MODE = os.getenv("DEFAULT_COORDINATE_MODE", "8-agent")
DEFAULT_AGENT_COUNT = int(os.getenv("DEFAULT_AGENT_COUNT", "8"))
DEFAULT_CAPTAIN_ID = os.getenv("DEFAULT_CAPTAIN_ID", "Agent-4")

# Messaging timeouts
DEFAULT_MESSAGE_TIMEOUT = float(os.getenv("DEFAULT_MESSAGE_TIMEOUT", "5.0"))
DEFAULT_RETRY_DELAY = float(os.getenv("DEFAULT_RETRY_DELAY", "1.0"))
DEFAULT_MAX_RETRIES = int(os.getenv("DEFAULT_MAX_RETRIES", "3"))

# ============================================================================
# AI/ML CONSTANTS
# ============================================================================

# AI/ML configuration defaults
DEFAULT_AI_MODEL_TIMEOUT = float(os.getenv("DEFAULT_AI_MODEL_TIMEOUT", "60.0"))
DEFAULT_AI_BATCH_SIZE = int(os.getenv("DEFAULT_AI_BATCH_SIZE", "32"))
DEFAULT_AI_MAX_TOKENS = int(os.getenv("DEFAULT_AI_MAX_TOKENS", "2048"))

# AI/ML API configurations
DEFAULT_AI_API_RETRY_COUNT = int(os.getenv("DEFAULT_AI_API_RETRY_COUNT", "3"))
DEFAULT_AI_API_RETRY_DELAY = float(os.getenv("DEFAULT_AI_API_RETRY_DELAY", "1.0"))

# ============================================================================
# FSM CONSTANTS
# ============================================================================

# FSM configuration defaults
DEFAULT_FSM_TIMEOUT = float(os.getenv("DEFAULT_FSM_TIMEOUT", "30.0"))
DEFAULT_FSM_MAX_STATES = int(os.getenv("DEFAULT_FSM_MAX_STATES", "100"))
DEFAULT_FSM_MAX_TRANSITIONS = int(os.getenv("DEFAULT_FSM_MAX_TRANSITIONS", "200"))

# FSM execution settings
DEFAULT_FSM_EXECUTION_TIMEOUT = float(os.getenv("DEFAULT_FSM_EXECUTION_TIMEOUT", "300.0"))
DEFAULT_FSM_STEP_TIMEOUT = float(os.getenv("DEFAULT_FSM_STEP_TIMEOUT", "30.0"))

# ============================================================================
# REFACTORING CONSTANTS
# ============================================================================

# Refactoring tool configurations
DEFAULT_REFACTORING_MAX_WORKERS = int(os.getenv("DEFAULT_REFACTORING_MAX_WORKERS", "4"))
DEFAULT_REFACTORING_TIMEOUT = float(os.getenv("DEFAULT_REFACTORING_TIMEOUT", "300.0"))
DEFAULT_REFACTORING_BATCH_SIZE = int(os.getenv("DEFAULT_REFACTORING_BATCH_SIZE", "50"))

# ============================================================================
# TESTING CONSTANTS
# ============================================================================

# Testing configuration defaults
DEFAULT_TEST_TIMEOUT = float(os.getenv("DEFAULT_TEST_TIMEOUT", "30.0"))
DEFAULT_TEST_RETRY_COUNT = int(os.getenv("DEFAULT_TEST_RETRY_COUNT", "3"))
DEFAULT_TEST_PARALLEL_WORKERS = int(os.getenv("DEFAULT_TEST_PARALLEL_WORKERS", "4"))

# Test coverage settings
DEFAULT_COVERAGE_MIN_PERCENT = float(os.getenv("DEFAULT_COVERAGE_MIN_PERCENT", "80.0"))
DEFAULT_COVERAGE_FAIL_UNDER = float(os.getenv("DEFAULT_COVERAGE_FAIL_UNDER", "70.0"))

# ============================================================================
# NETWORK CONSTANTS
# ============================================================================

# Network configuration defaults
DEFAULT_NETWORK_HOST = os.getenv("DEFAULT_NETWORK_HOST", "0.0.0.0")
DEFAULT_NETWORK_PORT = int(os.getenv("DEFAULT_NETWORK_PORT", "8000"))
DEFAULT_NETWORK_TIMEOUT = float(os.getenv("DEFAULT_NETWORK_TIMEOUT", "30.0"))

# Connection pool settings
DEFAULT_MAX_CONNECTIONS = int(os.getenv("DEFAULT_MAX_CONNECTIONS", "100"))
DEFAULT_KEEP_ALIVE = os.getenv("DEFAULT_KEEP_ALIVE", "true").lower() == "true"

# ============================================================================
# SECURITY CONSTANTS
# ============================================================================

# Security configuration defaults
DEFAULT_SECURITY_TIMEOUT = float(os.getenv("DEFAULT_SECURITY_TIMEOUT", "30.0"))
DEFAULT_MAX_LOGIN_ATTEMPTS = int(os.getenv("DEFAULT_MAX_LOGIN_ATTEMPTS", "5"))
DEFAULT_SESSION_TIMEOUT = float(os.getenv("DEFAULT_SESSION_TIMEOUT", "3600.0"))

# Encryption settings
DEFAULT_ENCRYPTION_ALGORITHM = os.getenv("DEFAULT_ENCRYPTION_ALGORITHM", "AES-256")
DEFAULT_HASH_ALGORITHM = os.getenv("DEFAULT_HASH_ALGORITHM", "SHA-256")

# ============================================================================
# DATABASE CONSTANTS
# ============================================================================

# Database configuration defaults
DEFAULT_DB_HOST = os.getenv("DEFAULT_DB_HOST", "localhost")
DEFAULT_DB_PORT = int(os.getenv("DEFAULT_DB_PORT", "5432"))
DEFAULT_DB_NAME = os.getenv("DEFAULT_DB_NAME", "agent_cellphone_v2")
DEFAULT_DB_POOL_SIZE = int(os.getenv("DEFAULT_DB_POOL_SIZE", "10"))
DEFAULT_DB_TIMEOUT = float(os.getenv("DEFAULT_DB_TIMEOUT", "30.0"))

# ============================================================================
# LOGGING CONSTANTS
# ============================================================================

# Logging configuration defaults
DEFAULT_LOG_FORMAT = os.getenv("DEFAULT_LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
DEFAULT_LOG_DATE_FORMAT = os.getenv("DEFAULT_LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
DEFAULT_LOG_FILE_SIZE = int(os.getenv("DEFAULT_LOG_FILE_SIZE", "10485760"))  # 10MB
DEFAULT_LOG_BACKUP_COUNT = int(os.getenv("DEFAULT_LOG_BACKUP_COUNT", "5"))

# ============================================================================
# UNIFIED CONSTANTS REGISTRY
# ============================================================================

class UnifiedConstantsRegistry:
    """Registry for all configuration constants with categorization and validation."""
    
    def __init__(self):
        self.constants: Dict[str, ConfigConstant] = {}
        self._initialize_constants()
    
    def _initialize_constants(self):
        """Initialize all configuration constants."""
        # Global constants
        self._add_constant("LOG_LEVEL", LOG_LEVEL, ConfigCategory.GLOBAL, 
                          "Global logging level for the application", ConfigPriority.CRITICAL)
        self._add_constant("TASK_ID_TIMESTAMP_FORMAT", TASK_ID_TIMESTAMP_FORMAT, ConfigCategory.GLOBAL,
                          "Standard timestamp format for task identifiers", ConfigPriority.HIGH)
        self._add_constant("APP_NAME", APP_NAME, ConfigCategory.GLOBAL,
                          "Application name", ConfigPriority.CRITICAL)
        self._add_constant("APP_VERSION", APP_VERSION, ConfigCategory.GLOBAL,
                          "Application version", ConfigPriority.CRITICAL)
        self._add_constant("APP_ENVIRONMENT", APP_ENVIRONMENT, ConfigCategory.GLOBAL,
                          "Application environment", ConfigPriority.CRITICAL)
        
        # Performance constants
        self._add_constant("DEFAULT_MAX_WORKERS", DEFAULT_MAX_WORKERS, ConfigCategory.PERFORMANCE,
                          "Default maximum worker threads", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_THREAD_POOL_SIZE", DEFAULT_THREAD_POOL_SIZE, ConfigCategory.PERFORMANCE,
                          "Default thread pool size", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_CACHE_SIZE", DEFAULT_CACHE_SIZE, ConfigCategory.PERFORMANCE,
                          "Default cache size in items", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_OPERATION_TIMEOUT", DEFAULT_OPERATION_TIMEOUT, ConfigCategory.PERFORMANCE,
                          "Default operation timeout in seconds", ConfigPriority.HIGH)
        
        # Quality constants
        self._add_constant("DEFAULT_CHECK_INTERVAL", DEFAULT_CHECK_INTERVAL, ConfigCategory.QUALITY,
                          "Default interval between quality checks", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_COVERAGE_THRESHOLD", DEFAULT_COVERAGE_THRESHOLD, ConfigCategory.QUALITY,
                          "Default test coverage threshold", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_HISTORY_WINDOW", DEFAULT_HISTORY_WINDOW, ConfigCategory.QUALITY,
                          "Default quality history window", ConfigPriority.LOW)
        
        # Messaging constants
        self._add_constant("DEFAULT_MESSAGING_MODE", DEFAULT_MESSAGING_MODE, ConfigCategory.MESSAGING,
                          "Default messaging mode", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_AGENT_COUNT", DEFAULT_AGENT_COUNT, ConfigCategory.MESSAGING,
                          "Default number of agents", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_CAPTAIN_ID", DEFAULT_CAPTAIN_ID, ConfigCategory.MESSAGING,
                          "Default captain agent ID", ConfigPriority.HIGH)
        
        # AI/ML constants
        self._add_constant("DEFAULT_AI_MODEL_TIMEOUT", DEFAULT_AI_MODEL_TIMEOUT, ConfigCategory.AI_ML,
                          "Default AI model timeout", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_AI_BATCH_SIZE", DEFAULT_AI_BATCH_SIZE, ConfigCategory.AI_ML,
                          "Default AI batch size", ConfigPriority.MEDIUM)
        
        # FSM constants
        self._add_constant("DEFAULT_FSM_TIMEOUT", DEFAULT_FSM_TIMEOUT, ConfigCategory.FSM,
                          "Default FSM timeout", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_FSM_MAX_STATES", DEFAULT_FSM_MAX_STATES, ConfigCategory.FSM,
                          "Default maximum FSM states", ConfigPriority.LOW)
        
        # Refactoring constants
        self._add_constant("DEFAULT_REFACTORING_MAX_WORKERS", DEFAULT_REFACTORING_MAX_WORKERS, ConfigCategory.REFACTORING,
                          "Default refactoring max workers", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_REFACTORING_TIMEOUT", DEFAULT_REFACTORING_TIMEOUT, ConfigCategory.REFACTORING,
                          "Default refactoring timeout", ConfigPriority.MEDIUM)
        
        # Testing constants
        self._add_constant("DEFAULT_TEST_TIMEOUT", DEFAULT_TEST_TIMEOUT, ConfigCategory.TESTING,
                          "Default test timeout", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_COVERAGE_MIN_PERCENT", DEFAULT_COVERAGE_MIN_PERCENT, ConfigCategory.TESTING,
                          "Default minimum test coverage percentage", ConfigPriority.MEDIUM)
        
        # Network constants
        self._add_constant("DEFAULT_NETWORK_HOST", DEFAULT_NETWORK_HOST, ConfigCategory.NETWORK,
                          "Default network host", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_NETWORK_PORT", DEFAULT_NETWORK_PORT, ConfigCategory.NETWORK,
                          "Default network port", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_MAX_CONNECTIONS", DEFAULT_MAX_CONNECTIONS, ConfigCategory.NETWORK,
                          "Default maximum connections", ConfigPriority.MEDIUM)
        
        # Security constants
        self._add_constant("DEFAULT_SECURITY_TIMEOUT", DEFAULT_SECURITY_TIMEOUT, ConfigCategory.SECURITY,
                          "Default security timeout", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_MAX_LOGIN_ATTEMPTS", DEFAULT_MAX_LOGIN_ATTEMPTS, ConfigCategory.SECURITY,
                          "Default maximum login attempts", ConfigPriority.HIGH)
        
        # Database constants
        self._add_constant("DEFAULT_DB_HOST", DEFAULT_DB_HOST, ConfigCategory.DATABASE,
                          "Default database host", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_DB_PORT", DEFAULT_DB_PORT, ConfigCategory.DATABASE,
                          "Default database port", ConfigPriority.HIGH)
        self._add_constant("DEFAULT_DB_POOL_SIZE", DEFAULT_DB_POOL_SIZE, ConfigCategory.DATABASE,
                          "Default database connection pool size", ConfigPriority.MEDIUM)
        
        # Logging constants
        self._add_constant("DEFAULT_LOG_FORMAT", DEFAULT_LOG_FORMAT, ConfigCategory.LOGGING,
                          "Default log format", ConfigPriority.MEDIUM)
        self._add_constant("DEFAULT_LOG_FILE_SIZE", DEFAULT_LOG_FILE_SIZE, ConfigCategory.LOGGING,
                          "Default log file size in bytes", ConfigPriority.LOW)
    
    def _add_constant(self, name: str, value: Any, category: ConfigCategory, 
                      description: str = "", priority: ConfigPriority = ConfigPriority.MEDIUM):
        """Add a constant to the registry."""
        self.constants[name] = ConfigConstant(
            name=name,
            value=value,
            category=category,
            description=description,
            priority=priority
        )
    
    def get_constant(self, name: str, default: Any = None) -> Any:
        """Get a configuration constant value."""
        if name in self.constants:
            return self.constants[name].value
        return default
    
    def get_constants_by_category(self, category: ConfigCategory) -> Dict[str, Any]:
        """Get all constants for a specific category."""
        return {
            name: constant.value
            for name, constant in self.constants.items()
            if constant.category == category
        }
    
    def get_constants_by_priority(self, priority: ConfigPriority) -> Dict[str, Any]:
        """Get all constants for a specific priority level."""
        return {
            name: constant.value
            for name, constant in self.constants.items()
            if constant.priority == priority
        }
    
    def list_all_constants(self) -> Dict[str, Dict[str, Any]]:
        """List all constants with their metadata."""
        return {
            name: {
                "value": constant.value,
                "category": constant.category.value,
                "description": constant.description,
                "priority": constant.priority.value
            }
            for name, constant in self.constants.items()
        }
    
    def export_constants(self, category: Optional[ConfigCategory] = None) -> Dict[str, Any]:
        """Export constants for external use."""
        if category:
            return self.get_constants_by_category(category)
        return {name: constant.value for name, constant in self.constants.items()}


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Global unified constants registry
UNIFIED_CONSTANTS = UnifiedConstantsRegistry()

# Convenience functions for backward compatibility
def get_constant(name: str, default: Any = None) -> Any:
    """Get a configuration constant value."""
    return UNIFIED_CONSTANTS.get_constant(name, default)

def get_constants_by_category(category: ConfigCategory) -> Dict[str, Any]:
    """Get all constants for a specific category."""
    return UNIFIED_CONSTANTS.get_constants_by_category(category)

def export_all_constants() -> Dict[str, Any]:
    """Export all constants for external use."""
    return UNIFIED_CONSTANTS.export_constants()


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    # Core classes and enums
    "ConfigCategory",
    "ConfigPriority", 
    "ConfigConstant",
    "UnifiedConstantsRegistry",
    
    # Global instance
    "UNIFIED_CONSTANTS",
    
    # Convenience functions
    "get_constant",
    "get_constants_by_category", 
    "export_all_constants",
    
    # All constant values for backward compatibility
    "LOG_LEVEL",
    "TASK_ID_TIMESTAMP_FORMAT",
    "APP_NAME",
    "APP_VERSION",
    "APP_ENVIRONMENT",
    "DEFAULT_MAX_WORKERS",
    "DEFAULT_THREAD_POOL_SIZE",
    "DEFAULT_CACHE_SIZE",
    "DEFAULT_OPERATION_TIMEOUT",
    "DEFAULT_CHECK_INTERVAL",
    "DEFAULT_COVERAGE_THRESHOLD",
    "DEFAULT_HISTORY_WINDOW",
    "DEFAULT_MESSAGING_MODE",
    "DEFAULT_AGENT_COUNT",
    "DEFAULT_CAPTAIN_ID",
    "DEFAULT_AI_MODEL_TIMEOUT",
    "DEFAULT_AI_BATCH_SIZE",
    "DEFAULT_FSM_TIMEOUT",
    "DEFAULT_FSM_MAX_STATES",
    "DEFAULT_REFACTORING_MAX_WORKERS",
    "DEFAULT_REFACTORING_TIMEOUT",
    "DEFAULT_TEST_TIMEOUT",
    "DEFAULT_COVERAGE_MIN_PERCENT",
    "DEFAULT_NETWORK_HOST",
    "DEFAULT_NETWORK_PORT",
    "DEFAULT_MAX_CONNECTIONS",
    "DEFAULT_SECURITY_TIMEOUT",
    "DEFAULT_MAX_LOGIN_ATTEMPTS",
    "DEFAULT_DB_HOST",
    "DEFAULT_DB_PORT",
    "DEFAULT_DB_POOL_SIZE",
    "DEFAULT_LOG_FORMAT",
    "DEFAULT_LOG_FILE_SIZE"
]
