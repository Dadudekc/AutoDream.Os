#!/usr/bin/env python3
"""
Coding Standards Implementation Package
V2 Compliance: Modular coding standards implementation system

This package contains the modularized coding standards implementation system
that has been refactored from the monolithic coding_standards_implementation.py
to achieve V2 compliance (≤400 LOC per file).
"""

from .coding_standards_core import CodingStandardsImplementation
from .compliance_analyzer import ComplianceAnalyzer
from .standards_fixer import StandardsFixer
from .report_generator import ReportGenerator

__version__ = "2.0.0"
__author__ = "Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)"
__description__ = "V2 Compliant Coding Standards Implementation System"

__all__ = [
    "CodingStandardsImplementation",
    "ComplianceAnalyzer", 
    "StandardsFixer",
    "ReportGenerator"
]
