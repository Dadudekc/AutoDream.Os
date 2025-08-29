"""
Duplication Detection Package - Unified code duplication management
================================================================

This package provides comprehensive code duplication detection and consolidation,
eliminating duplicate code patterns across the entire codebase.

Modules:
- types: Duplication types and severity levels
- models: Core duplication data models
- parser: Code parsing and analysis
- detector: Duplication detection algorithms
- consolidator: Code consolidation utilities
- reporter: Duplication reporting and metrics
"""

from .types import DuplicationType, DuplicationSeverity
from .models import DuplicationInstance, DuplicationGroup, DuplicationReport
from .parser import CodeParser
from .detector import DuplicationDetector
from .consolidator import CodeConsolidator
from .reporter import DuplicationReporter

__all__ = [
    'DuplicationType', 'DuplicationSeverity',
    'DuplicationInstance', 'DuplicationGroup', 'DuplicationReport',
    'CodeParser', 'DuplicationDetector', 'CodeConsolidator', 'DuplicationReporter'
]
