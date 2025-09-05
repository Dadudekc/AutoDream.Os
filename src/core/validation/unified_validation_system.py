#!/usr/bin/env python3
"""
Unified Validation System - Modular Architecture (V2 Compliance)

Refactored from monolithic 421-line file into clean, modular architecture:
- Models: Core data structures and enums
- Engines: Specialized validation engines (field, format, range, custom)
- Coordinator: Orchestrates different engines
- Utils: Backward compatibility functions

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

# Re-export all public APIs for backward compatibility
from .models.validation_models import (
    ValidationType,
    ValidationSeverity,
    ValidationResult,
    ValidationRule
)

from .validation_coordinator import ValidationCoordinator
from .utils.validation_utils import (
    get_validation_coordinator,
    validate_required_fields,
    validate_data_types,
    validate_email,
    validate_url,
    validate_string_length,
    validate_numeric_range,
    validate_regex_pattern,
    validate_custom
)

# Backward compatibility alias
UnifiedValidationSystem = ValidationCoordinator

# Global instance for backward compatibility
_unified_validator = None

def get_unified_validator() -> ValidationCoordinator:
    """Get global unified validation instance."""
    global _unified_validator
    if _unified_validator is None:
        _unified_validator = ValidationCoordinator()
    return _unified_validator
