"""
Data Processing - DUP-008 Consolidation
=======================================

Unified data processing infrastructure consolidating duplicate patterns.

Exports:
    - UnifiedBatchProcessor: Batch processing (consolidates 4 duplicates)
    - UnifiedDataProcessor: Data transformation (consolidates 3 duplicates)
    - UnifiedResultsProcessor: Results validation (consolidates 4 duplicates)
    - ProcessingResult: Standard result structure

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-008 Data Processing Patterns Consolidation
License: MIT
"""

from .unified_processors import (
    UnifiedBatchProcessor,
    UnifiedDataProcessor,
    UnifiedResultsProcessor,
    ProcessingResult,
    process_batch,
    process_data,
    process_results,
)

__all__ = [
    "UnifiedBatchProcessor",
    "UnifiedDataProcessor",
    "UnifiedResultsProcessor",
    "ProcessingResult",
    "process_batch",
    "process_data",
    "process_results",
]

__version__ = "2.0.0"

