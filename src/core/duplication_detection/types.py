#!/usr/bin/env python3
"""
Duplication Types - Core enums and constants
===========================================

Defines all duplication types and severity levels for the
unified duplication detection system.
"""

from enum import Enum


class DuplicationType(Enum):
    """Types of code duplication"""
    EXACT_MATCH = "exact_match"
    NEAR_DUPLICATE = "near_duplicate"
    FUNCTION_DUPLICATE = "function_duplicate"
    CLASS_DUPLICATE = "class_duplicate"
    PATTERN_DUPLICATE = "pattern_duplicate"
    STRUCTURAL_DUPLICATE = "structural_duplicate"
    LOGIC_DUPLICATE = "logic_duplicate"


class DuplicationSeverity(Enum):
    """Duplication severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AnalysisLevel(Enum):
    """Analysis depth levels"""
    SURFACE = "surface"
    DEEP = "deep"
    COMPREHENSIVE = "comprehensive"


class ConsolidationStrategy(Enum):
    """Consolidation strategies"""
    EXTRACT_METHOD = "extract_method"
    EXTRACT_CLASS = "extract_class"
    EXTRACT_MODULE = "extract_module"
    REFACTOR_COMMON = "refactor_common"
    MERGE_FILES = "merge_files"
