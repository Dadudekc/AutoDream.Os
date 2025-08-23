#!/usr/bin/env python3
"""
Integrity Package - Agent Cellphone V2
======================================

Refactored data integrity system with modular architecture.
All modules comply with 200 LOC standard.
"""

from .integrity_types import (
    IntegrityCheckType,
    RecoveryStrategy,
    IntegrityLevel,
    IntegrityCheck,
    IntegrityViolation,
    IntegrityConfig,
)

from .integrity_core import DataIntegrityManager

# Backward compatibility - maintain original interface
__all__ = [
    # Types
    "IntegrityCheckType",
    "RecoveryStrategy",
    "IntegrityLevel",
    "IntegrityCheck",
    "IntegrityViolation",
    "IntegrityConfig",
    # Core classes
    "DataIntegrityManager",
    # Legacy alias for backward compatibility
    "DataIntegrityManager as IntegrityManager",  # Maintains original import
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-4 (Quality Assurance Specialist)"
__description__ = "Refactored integrity system meeting 200 LOC standards"
