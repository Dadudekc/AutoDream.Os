#!/usr/bin/env python3
"""
Performance Reporting Package - V2 Modular Architecture
=======================================================

Modular reporting system for performance management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .report_generator import PerformanceReportGenerator
from .report_types import PerformanceReport, ReportSection, ReportMetric, ReportFormat, ReportStatus

__all__ = [
    "PerformanceReportGenerator",
    "PerformanceReport",
    "ReportSection",
    "ReportMetric",
    "ReportFormat",
    "ReportStatus"
]
