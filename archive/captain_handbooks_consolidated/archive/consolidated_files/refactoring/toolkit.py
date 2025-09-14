"""Facade module aggregating refactoring tools."""

from .analysis_tools import (
    analyze_architecture_patterns,
    analyze_file_for_extraction,
    find_duplicate_files,
)
from .metrics import MetricsManager, RefactoringMetrics, update_metrics
from .refactor_tools import (
    create_consolidation_plan,
    create_extraction_plan,
    create_optimization_plan,
    perform_consolidation,
    perform_extraction,
    perform_optimization,
)

__all__ = [
    "analyze_file_for_extraction",
    "find_duplicate_files",
    "analyze_architecture_patterns",
    "create_extraction_plan",
    "perform_extraction",
    "create_consolidation_plan",
    "perform_consolidation",
    "create_optimization_plan",
    "perform_optimization",
    "MetricsManager",
    "RefactoringMetrics",
    "update_metrics",
]
