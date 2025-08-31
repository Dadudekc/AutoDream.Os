"""
Unified Reporting Framework - Agent Cellphone V2

Provides a comprehensive, unified reporting system that consolidates
all scattered reporting implementations across the codebase.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3I - Reporting Systems Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

from .unified_reporting_framework import UnifiedReportingFramework
from .report_models import (
    ReportType,
    ReportFormat,
    ReportPriority,
    ReportConfig,
    ReportMetadata,
    UnifiedReport,
)
from .performance_report_formatter import (
    ReportFormatter as PerformanceReportFormatter,
    PerformanceReport,
    ReportSection,
    ReportMetric,
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


__all__ = [
    # Core framework
    "UnifiedReportingFramework",
    "ReportType",
    "ReportFormat",
    "ReportPriority",
    "ReportConfig",
    "ReportMetadata",
    "UnifiedReport",
    # Performance reporting
    "PerformanceReportFormatter",
    "PerformanceReport",
    "ReportSection",
    "ReportMetric",


    # System consolidation
    "ReportingSystemConsolidator",
    "ConsolidationTarget",
    "ConsolidationPlan",
    "ConsolidationResult",
]

