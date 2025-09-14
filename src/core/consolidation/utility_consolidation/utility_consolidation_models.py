#!/usr/bin/env python3
"""
Utility Consolidation Models - V2 Compliance Module
==================================================

Data models and enums for utility consolidation system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from enum import Enum


class ConsolidationType(Enum):
    """Types of utility consolidation."""

    DUPLICATE_ELIMINATION = "duplicate_elimination"
    FUNCTION_MERGING = "function_merging"
    MODULE_CONSOLIDATION = "module_consolidation"
    INTERFACE_UNIFICATION = "interface_unification"


@dataclass
class UtilityFunction:
    """Utility function metadata."""

    name: str
    file_path: str
    line_start: int
    line_end: int
    content: str
    parameters: list[str]
    return_type: str | None = None
    complexity_score: int = 0
    usage_count: int = 0


@dataclass
class ConsolidationOpportunity:
    """Consolidation opportunity identified."""

    consolidation_type: ConsolidationType
    primary_function: UtilityFunction
    duplicate_functions: list[UtilityFunction]
    consolidation_strategy: str
    estimated_reduction: int
    priority: str = "MEDIUM"


@dataclass
class ConsolidationResult:
    """Result of consolidation operation."""

    success: bool
    functions_consolidated: int
    lines_reduced: int
    new_file_path: str | None = None
    error_message: str | None = None


@dataclass
class ConsolidationConfig:
    """Configuration for consolidation operations."""

    min_similarity_threshold: float = 0.8
    max_complexity_difference: int = 5
    enable_automatic_consolidation: bool = False
    backup_original_files: bool = True
    target_directory: str = "consolidated_utilities"
