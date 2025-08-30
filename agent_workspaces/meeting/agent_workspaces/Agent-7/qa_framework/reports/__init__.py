"""
🎯 QUALITY ASSURANCE FRAMEWORK - REPORTS MODULE
Agent-7 - Quality Completion Optimization Manager

Reporting system for quality assessment results.
Follows V2 coding standards: ≤300 lines per module.
"""

from .quality_reports import QualityReportGenerator
from .compliance_reports import ComplianceReportGenerator

__all__ = [
    "QualityReportGenerator",
    "ComplianceReportGenerator"
]
