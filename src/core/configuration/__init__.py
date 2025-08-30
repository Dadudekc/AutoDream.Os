#!/usr/bin/env python3
"""
Unified Configuration System - Agent Cellphone V2
===============================================

Consolidated configuration management system that eliminates duplication across
multiple configuration implementations. Provides unified constants, configuration
classes, and management utilities.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from .unified_constants import (
    # Core classes and enums
    ConfigCategory,
    ConfigPriority,
    ConfigConstant,
    UnifiedConstantsRegistry,
    
    # Global instance
    UNIFIED_CONSTANTS,
    
    # Convenience functions
    get_constant,
    get_constants_by_category,
    export_all_constants,
    
    # All constant values for backward compatibility
    LOG_LEVEL,
    TASK_ID_TIMESTAMP_FORMAT,
    APP_NAME,
    APP_VERSION,
    APP_ENVIRONMENT,
    DEFAULT_MAX_WORKERS,
    DEFAULT_THREAD_POOL_SIZE,
    DEFAULT_CACHE_SIZE,
    DEFAULT_OPERATION_TIMEOUT,
    DEFAULT_CHECK_INTERVAL,
    DEFAULT_COVERAGE_THRESHOLD,
    DEFAULT_HISTORY_WINDOW,
    DEFAULT_MESSAGING_MODE,
    DEFAULT_AGENT_COUNT,
    DEFAULT_CAPTAIN_ID,
    DEFAULT_AI_MODEL_TIMEOUT,
    DEFAULT_AI_BATCH_SIZE,
    DEFAULT_FSM_TIMEOUT,
    DEFAULT_FSM_MAX_STATES,
    DEFAULT_REFACTORING_MAX_WORKERS,
    DEFAULT_REFACTORING_TIMEOUT,
    DEFAULT_TEST_TIMEOUT,
    DEFAULT_COVERAGE_MIN_PERCENT,
    DEFAULT_NETWORK_HOST,
    DEFAULT_NETWORK_PORT,
    DEFAULT_MAX_CONNECTIONS,
    DEFAULT_SECURITY_TIMEOUT,
    DEFAULT_MAX_LOGIN_ATTEMPTS,
    DEFAULT_DB_HOST,
    DEFAULT_DB_PORT,
    DEFAULT_DB_POOL_SIZE,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_FILE_SIZE
)

# ============================================================================
# PACKAGE METADATA
# ============================================================================

__version__ = "1.0.0"
__author__ = "Agent-3 (Testing Framework Enhancement Manager)"
__license__ = "MIT"

# ============================================================================
# CONSOLIDATION SUMMARY
# ============================================================================

"""
CONFIGURATION CONSOLIDATION STATUS:

✅ COMPLETED:
- Unified Constants System: 15+ duplicate constants files → 1 unified system
- Constants Registry: Categorized and prioritized configuration constants
- Environment Override Support: Environment variable integration
- Backward Compatibility: All existing constants accessible

🎯 IN PROGRESS:
- Configuration Classes Consolidation: 5+ duplicate classes → 1 unified system
- Configuration Management Consolidation: 3+ duplicate managers → 1 unified system

📊 IMPACT ACHIEVED:
- Constants Files: 15+ → 1 file (93%+ reduction)
- Code Duplication: Eliminated across all configuration constants
- Maintenance: Single source of truth for all constants
- Quality: Categorized, prioritized, and documented constants

🚀 NEXT STEPS:
- Complete configuration classes consolidation
- Complete configuration management consolidation
- Create migration guides for existing code
- Validate all consolidated functionality
"""

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
QUICK START USAGE:

# Get a specific constant
from src.core.configuration import get_constant
max_workers = get_constant("DEFAULT_MAX_WORKERS", 4)

# Get all constants for a category
from src.core.configuration import get_constants_by_category, ConfigCategory
performance_constants = get_constants_by_category(ConfigCategory.PERFORMANCE)

# Use the global registry directly
from src.core.configuration import UNIFIED_CONSTANTS
all_constants = UNIFIED_CONSTANTS.export_constants()

# Access constants directly (backward compatibility)
from src.core.configuration import DEFAULT_MAX_WORKERS, DEFAULT_CACHE_SIZE
workers = DEFAULT_MAX_WORKERS
cache_size = DEFAULT_CACHE_SIZE
"""

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
