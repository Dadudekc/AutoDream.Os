"""
DRY Eliminator Enums
====================

Enumeration definitions for DRY violation elimination.
Extracted from dry_eliminator_models.py for V2 compliance micro-refactoring.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from enum import Enum


class DRYViolationType(Enum):
    """Types of DRY violations."""

    DUPLICATE_IMPORTS = "duplicate_imports"
    DUPLICATE_METHODS = "duplicate_methods"
    DUPLICATE_CLASSES = "duplicate_classes"
    DUPLICATE_CONSTANTS = "duplicate_constants"
    DUPLICATE_DOCUMENTATION = "duplicate_documentation"
    DUPLICATE_ERROR_HANDLING = "duplicate_error_handling"
    DUPLICATE_ALGORITHMS = "duplicate_algorithms"
    DUPLICATE_INTERFACES = "duplicate_interfaces"
    DUPLICATE_TESTS = "duplicate_tests"
    DUPLICATE_DATA_STRUCTURES = "duplicate_data_structures"
    UNUSED_IMPORTS = "unused_imports"


class EliminationStrategy(Enum):
    """DRY elimination strategies."""

    CONSOLIDATE = "consolidate"
    EXTRACT = "extract"
    REFACTOR = "refactor"
    REMOVE = "remove"
    MERGE = "merge"


class DRYScanMode(Enum):
    """DRY scanning modes."""

    FAST = "fast"
    THOROUGH = "thorough"
    DEEP = "deep"
    COMPREHENSIVE = "comprehensive"


class ViolationSeverity(Enum):
    """Severity levels for DRY violations."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
