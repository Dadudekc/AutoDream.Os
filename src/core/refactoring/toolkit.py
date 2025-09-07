"""Facade module aggregating refactoring tools."""

from .analysis_tools import (
    analyze_file_for_extraction,
    find_duplicate_files,
    analyze_architecture_patterns,
)
from .refactor_tools import (
    create_extraction_plan,
    perform_extraction,
    create_consolidation_plan,
    perform_consolidation,
    create_optimization_plan,
    perform_optimization,
)
from .metrics import (
    MetricsManager,
    RefactoringMetrics,
    update_metrics,
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
