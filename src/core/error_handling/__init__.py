"""
Error Handling Module - V2 Compliant Consolidated Version
==========================================================

Agent-3 C-055-3 Consolidation:
- 5 files consolidated into 2 unified modules
- error_handling_core.py: Models, enums, configurations
- error_handling_system.py: Orchestrator, retry, recovery, circuit breaker

Backward compatibility maintained through re-exports.
"""

# ============================================================================
# CORE EXPORTS - New Consolidated Modules
# ============================================================================

from .error_handling_core import (
    AgentErrorResponse,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitState,
    ConfigurationErrorResponse,
    CoordinationErrorResponse,
    DatabaseErrorResponse,
    ErrorCategory,
    ErrorContext,
    ErrorSeverity,
    ErrorSeverityMapping,
    ErrorSummary,
    FileErrorResponse,
    NetworkErrorResponse,
    RecoverableErrors,
    RetryConfig,
    RetryException,
    StandardErrorResponse,
    ValidationErrorResponse,
)
from .error_handling_system import (
    CircuitBreaker,
    ConfigurationResetStrategy,
    ErrorRecoveryManager,
    RecoveryStrategy,
    ResourceCleanupStrategy,
    RetryMechanism,
    ServiceRestartStrategy,
    UnifiedErrorHandlingOrchestrator,
    get_error_handling_orchestrator,
    retry_on_exception,
    with_error_recovery,
    with_exponential_backoff,
)

# ============================================================================
# BACKWARD COMPATIBILITY - Legacy Module Imports
# ============================================================================

# These imports maintain compatibility with existing code
# Import remaining specialized modules that weren't consolidated

try:
    from . import circuit_breaker
except ImportError:
    circuit_breaker = None

try:
    from . import error_analysis_engine
except ImportError:
    error_analysis_engine = None

try:
    from . import error_reporting_core
except ImportError:
    error_reporting_core = None

try:
    from . import error_reporting_reporter
except ImportError:
    error_reporting_reporter = None

try:
    from . import error_reporting_utilities
except ImportError:
    error_reporting_utilities = None

try:
    from . import retry_safety_engine
except ImportError:
    retry_safety_engine = None

try:
    from . import specialized_handlers
except ImportError:
    specialized_handlers = None

# ============================================================================
# LEGACY ALIASES - For Backward Compatibility
# ============================================================================

# Alias old module names to new consolidated exports
error_handling_models = type(
    "error_handling_models",
    (),
    {
        "ErrorSeverity": ErrorSeverity,
        "ErrorCategory": ErrorCategory,
        "StandardErrorResponse": StandardErrorResponse,
        "RetryConfiguration": RetryConfig,  # Old name
        "ErrorContext": ErrorContext,
    },
)

error_recovery = type(
    "error_recovery",
    (),
    {
        "RecoveryStrategy": RecoveryStrategy,
        "ErrorRecoveryManager": ErrorRecoveryManager,
        "ServiceRestartStrategy": ServiceRestartStrategy,
    },
)

retry_mechanisms = type(
    "retry_mechanisms",
    (),
    {
        "RetryMechanism": RetryMechanism,
        "RetryConfig": RetryConfig,
        "retry_on_exception": retry_on_exception,
        "with_exponential_backoff": with_exponential_backoff,
    },
)

error_handling_orchestrator = type(
    "error_handling_orchestrator",
    (),
    {
        "UnifiedErrorHandlingOrchestrator": UnifiedErrorHandlingOrchestrator,
        "get_error_handling_orchestrator": get_error_handling_orchestrator,
    },
)

# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    # Core models and enums
    "ErrorSeverity",
    "ErrorCategory",
    "ErrorContext",
    "CircuitState",
    # Response classes
    "StandardErrorResponse",
    "FileErrorResponse",
    "NetworkErrorResponse",
    "DatabaseErrorResponse",
    "ValidationErrorResponse",
    "ConfigurationErrorResponse",
    "AgentErrorResponse",
    "CoordinationErrorResponse",
    # Summary and statistics
    "ErrorSummary",
    # Configuration
    "RetryConfig",
    "CircuitBreakerConfig",
    # Error mappings
    "RecoverableErrors",
    "ErrorSeverityMapping",
    # Exceptions
    "RetryException",
    "CircuitBreakerError",
    # Retry mechanism
    "RetryMechanism",
    "retry_on_exception",
    "with_exponential_backoff",
    # Circuit breaker
    "CircuitBreaker",
    # Recovery strategies
    "RecoveryStrategy",
    "ServiceRestartStrategy",
    "ConfigurationResetStrategy",
    "ResourceCleanupStrategy",
    "ErrorRecoveryManager",
    "with_error_recovery",
    # Orchestrator
    "UnifiedErrorHandlingOrchestrator",
    "get_error_handling_orchestrator",
    # Legacy module aliases
    "error_handling_models",
    "error_recovery",
    "retry_mechanisms",
    "error_handling_orchestrator",
    # Remaining specialized modules
    "circuit_breaker",
    "error_analysis_engine",
    "error_reporting_core",
    "error_reporting_reporter",
    "error_reporting_utilities",
    "retry_safety_engine",
    "specialized_handlers",
]
