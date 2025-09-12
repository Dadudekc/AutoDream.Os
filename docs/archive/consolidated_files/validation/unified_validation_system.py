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

from .validation_coordinator import ValidationCoordinator

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
