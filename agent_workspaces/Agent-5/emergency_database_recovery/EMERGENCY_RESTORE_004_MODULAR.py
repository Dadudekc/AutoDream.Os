#!/usr/bin/env python3
"""
EMERGENCY-RESTORE-004: Contract Database Recovery - Modular Interface

This is the main interface module that provides access to all emergency database recovery functionality.
It replaces the monolithic EMERGENCY_RESTORE_004_DATABASE_AUDIT.py file with a clean, modular structure.

Agent-5: Sprint Acceleration Refactoring Tool Preparation Manager
Contract: EMERGENCY-RESTORE-004
Status: MODULARIZED AND OPERATIONAL
"""

from .core import EmergencyContractDatabaseRecovery
from .models import AuditResult, IntegrityIssue, RecoveryAction, RecoveryReport
from .database_auditor import DatabaseAuditor
from .integrity_checker import IntegrityChecker
from .corruption_scanner import CorruptionScanner
from .recovery_executor import RecoveryExecutor

# Main recovery system instance for easy access
emergency_recovery_system = EmergencyContractDatabaseRecovery()

# Convenience functions for backward compatibility
def execute_emergency_recovery() -> RecoveryReport:
    """Execute EMERGENCY-RESTORE-004 immediately."""
    return emergency_recovery_system.execute_emergency_recovery()

def audit_database_structure() -> dict:
    """Audit the overall structure of the contract database."""
    return emergency_recovery_system.audit_database_structure()

def validate_contract_status_accuracy() -> dict:
    """Validate the accuracy of contract status information."""
    return emergency_recovery_system.validate_contract_status_accuracy()

def scan_for_corruption() -> dict:
    """Scan for corrupted or missing contracts."""
    return emergency_recovery_system.scan_for_corruption()

def implement_integrity_checks() -> dict:
    """Implement database integrity checks."""
    return emergency_recovery_system.implement_integrity_checks()

def run_quick_health_check() -> dict:
    """Run a quick health check of the database."""
    return emergency_recovery_system.run_quick_health_check()

# Export main classes for direct use
__all__ = [
    'EmergencyContractDatabaseRecovery',
    'AuditResult',
    'IntegrityIssue',
    'RecoveryAction',
    'RecoveryReport',
    'DatabaseAuditor',
    'IntegrityChecker',
    'CorruptionScanner',
    'RecoveryExecutor',
    'emergency_recovery_system',
    'execute_emergency_recovery',
    'audit_database_structure',
    'validate_contract_status_accuracy',
    'scan_for_corruption',
    'implement_integrity_checks',
    'run_quick_health_check'
]

# Main execution block for backward compatibility
if __name__ == "__main__":
    print("🚨 EMERGENCY-RESTORE-004: Contract Database Recovery System")
    print("=" * 60)
    
    # Run quick health check first
    print("\n🔍 Running quick health check...")
    health_check = run_quick_health_check()
    print(f"Status: {health_check.get('status', 'UNKNOWN')}")
    print(f"Files exist: {health_check.get('files_exist', False)}")
    print(f"JSON valid: {health_check.get('json_valid', False)}")
    print(f"Contract count: {health_check.get('contract_count', 0)}")
    
    # Execute full emergency recovery if requested
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--full-recovery":
        print("\n🚨 Executing full emergency recovery...")
        recovery_report = execute_emergency_recovery()
        print(f"Recovery completed with status: {recovery_report.system_status}")
        print(f"Recommendations: {len(recovery_report.recommendations)}")
        print(f"Next steps: {len(recovery_report.next_steps)}")
    else:
        print("\n💡 Use --full-recovery flag to execute complete emergency recovery")
        print("💡 Use individual functions for specific operations")
