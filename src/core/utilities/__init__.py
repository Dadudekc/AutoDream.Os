"""
Core Utilities Module
=====================

Modular utilities extracted from shared_utilities.py for V2 compliance.
"""

# Import all utilities from modular structure
from .base_utilities import BaseUtility
from .cleanup_utilities import CleanupManager, create_cleanup_manager
from .config_utilities import ConfigurationManager, create_configuration_manager
from .error_utilities import ErrorHandler, create_error_handler
from .init_utilities import InitializationManager, create_initialization_manager
from .logging_utilities import LoggingManager, create_logging_manager
from .result_utilities import ResultManager, create_result_manager
from .status_utilities import StatusManager, create_status_manager
from .validation_utilities import ValidationManager, create_validation_manager

__all__ = [
    # Base
    "BaseUtility",
    # Managers
    "CleanupManager",
    "ConfigurationManager",
    "ErrorHandler",
    "InitializationManager",
    "LoggingManager",
    "ResultManager",
    "StatusManager",
    "ValidationManager",
    # Factory functions
    "create_cleanup_manager",
    "create_configuration_manager",
    "create_error_handler",
    "create_initialization_manager",
    "create_logging_manager",
    "create_result_manager",
    "create_status_manager",
    "create_validation_manager",
]
