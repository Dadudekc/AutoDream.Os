#!/usr/bin/env python3
"""
Meeting Package
==============

Coding standards implementation and compliance tools.
Follows V2 standards: modular, compliant architecture.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .standards_core import (
    StandardsCore,
    StandardsViolation,
    FileComplianceReport
)
from .compliance_analyzer import (
    ComplianceAnalyzer,
    ComplianceSummary
)
from .standards_orchestrator import StandardsOrchestrator

__all__ = [
    'StandardsCore',
    'StandardsViolation',
    'FileComplianceReport',
    'ComplianceAnalyzer',
    'ComplianceSummary',
    'StandardsOrchestrator'
]

__version__ = "1.0.0"
__author__ = "V2 SWARM CAPTAIN"
__license__ = "MIT"
