"""
Unified Reporting Framework - Agent Cellphone V2

Provides a comprehensive, unified reporting system that consolidates
all scattered reporting implementations across the codebase.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3I - Reporting Systems Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

from .unified_reporting_framework import (
    UnifiedReportingFramework,
    ReportType,
    ReportFormat,
    ReportPriority,
    ReportConfig,
    ReportMetadata,
    UnifiedReport
)

# Consolidator module is optional in some installations
try:
    from .reporting_system_consolidator import (
        ReportingSystemConsolidator,
        ConsolidationTarget,
        ConsolidationPlan,
        ConsolidationResult,
    )
except ModuleNotFoundError:  # pragma: no cover - fallback when module missing
    ReportingSystemConsolidator = None
    ConsolidationTarget = None
    ConsolidationPlan = None
    ConsolidationResult = None

from .reporting_system_eliminator import (
    ReportingSystemEliminator,
    EliminationTarget,
    EliminationPlan
)

__all__ = [
    # Core framework
    'UnifiedReportingFramework',
    'ReportType',
    'ReportFormat',
    'ReportPriority',
    'ReportConfig',
    'ReportMetadata',
    'UnifiedReport',
    
    # System consolidation
    'ReportingSystemConsolidator',
    'ConsolidationTarget',
    'ConsolidationPlan',
    'ConsolidationResult',
    
    # System elimination
    'ReportingSystemEliminator',
    'EliminationTarget',
    'EliminationPlan'
]

