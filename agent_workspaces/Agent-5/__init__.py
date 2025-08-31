#!/usr/bin/env python3
"""
Agent-5 Workspace - Sprint Acceleration Refactoring Tool Preparation Manager
===========================================================================

This workspace contains the tools and systems developed by Agent-5 for
sprint acceleration and refactoring tool preparation.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Mission:** V2 Compliance and System Modularization
**Status:** Active Development
**V2 Compliance:** ✅ Modular architecture, focused responsibilities
"""

# Database Integrity Checker System (Modularized)
from .database_integrity_models import (
    IntegrityCheck,
    IntegrityReport,
    ContractData,
    create_integrity_check,
    create_integrity_report
)

from .database_integrity_checks import DatabaseIntegrityChecks
from .database_integrity_reporting import DatabaseIntegrityReporting
from .database_integrity_orchestrator import DatabaseIntegrityOrchestrator

# Legacy modules (for backward compatibility)
from .database_integrity_core import DatabaseIntegrityCore
from .database_integrity_operations import DatabaseIntegrityOperations
from .database_integrity_reporting_legacy import DatabaseIntegrityReportingLegacy

__all__ = [
    # New modularized system
    'IntegrityCheck',
    'IntegrityReport', 
    'ContractData',
    'create_integrity_check',
    'create_integrity_report',
    'DatabaseIntegrityChecks',
    'DatabaseIntegrityReporting',
    'DatabaseIntegrityOrchestrator',
    
    # Legacy system (deprecated)
    'DatabaseIntegrityCore',
    'DatabaseIntegrityOperations',
    'DatabaseIntegrityReportingLegacy'
]

__version__ = "2.0.0"
__author__ = "Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)"
__status__ = "V2_COMPLIANCE_MODULARIZATION_ACTIVE"
