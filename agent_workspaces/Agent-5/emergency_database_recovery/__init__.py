"""
Emergency Database Recovery Package

This package contains modular components for emergency database recovery,
replacing the monolithic EMERGENCY_RESTORE_004_DATABASE_AUDIT.py file.
"""

from .core import EmergencyContractDatabaseRecovery
from .models import AuditResult, IntegrityIssue, RecoveryAction
from .database_auditor import DatabaseAuditor
from .integrity_checker import IntegrityChecker
from .corruption_scanner import CorruptionScanner
from .recovery_executor import RecoveryExecutor

__version__ = "2.0.0"
__author__ = "Agent-5 - Sprint Acceleration Refactoring Tool Preparation Manager"

__all__ = [
    'EmergencyContractDatabaseRecovery',
    'AuditResult',
    'IntegrityIssue',
    'RecoveryAction',
    'DatabaseAuditor',
    'IntegrityChecker',
    'CorruptionScanner',
    'RecoveryExecutor'
]
