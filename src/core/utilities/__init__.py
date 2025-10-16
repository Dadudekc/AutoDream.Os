"""
Core Utilities Package
=====================

Consolidated utility functions for validation, processing, and handling operations.
Created as part of DUP-005 duplicate elimination mission.

Author: Agent-7 (DUP-005 Mission)
Date: 2025-10-16
"""

from .handler_utilities import *
from .processing_utilities import *
from .validation_utilities import *

__all__ = [
    # Validation utilities
    "validate_import_syntax",
    "validate_import_pattern",
    "validate_file_path",
    "validate_config",
    "validate_session",
    "validate_coordinates",
    "validate_forecast_accuracy",
    # Processing utilities
    "process_batch",
    "process_data",
    "process_results",
    # Handler utilities
    "handle_error",
    "handle_operation",
    "handle_event",
    "handle_rate_limit_error",
]
