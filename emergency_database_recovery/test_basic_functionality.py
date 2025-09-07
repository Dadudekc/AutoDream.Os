#!/usr/bin/env python3
"""
Basic Functionality Test for Emergency Database Recovery System.

This script tests the basic functionality of the modularized emergency database recovery system.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from emergency_database_recovery import EmergencyContractDatabaseRecovery
from emergency_database_recovery.core.database_auditor import DatabaseAuditor
from emergency_database_recovery.models.audit_results import AuditResults, FileAnalysis
from emergency_database_recovery.models.integrity_issues import IntegrityIssues, IssueSeverity, IssueStatus
from emergency_database_recovery.models.recovery_actions import RecoveryAction, RecoveryPlan, ActionType, ActionStatus


def test_basic_imports():
    """Test that all basic imports work correctly."""
    print("✅ Testing basic imports...")
    
    try:
        # Test main system import
        from emergency_database_recovery import EmergencyContractDatabaseRecovery
        print("  ✅ Main system import successful")
        
        # Test core components
        from emergency_database_recovery.core.database_auditor import DatabaseAuditor
        from emergency_database_recovery.core.integrity_checker import IntegrityChecker
        from emergency_database_recovery.core.corruption_scanner import CorruptionScanner
        from emergency_database_recovery.core.recovery_executor import RecoveryExecutor
        print("  ✅ Core components import successful")
        
        # Test models
        from emergency_database_recovery.models.audit_results import AuditResults, FileAnalysis
        from emergency_database_recovery.models.integrity_issues import IntegrityIssues, IssueSeverity, IssueStatus
        from emergency_database_recovery.models.recovery_actions import RecoveryAction, RecoveryPlan, ActionType, ActionStatus
        from emergency_database_recovery.models.system_status import SystemStatus, HealthLevel
        print("  ✅ Models import successful")
        
        # Test services
        from emergency_database_recovery.services.logging_service import LoggingService
        from emergency_database_recovery.services.validation_service import ValidationService
        from emergency_database_recovery.services.reporting_service import ReportingService
        from emergency_database_recovery.services.notification_service import NotificationService
        print("  ✅ Services import successful")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def test_data_models():
    """Test that data models can be instantiated and used."""
    print("✅ Testing data models...")
    
    try:
        # Test FileAnalysis
        file_analysis = FileAnalysis(
            filename="test.json",
            filepath="test/path/test.json",
            exists=True,
            readable=True,
            valid_json=True,
            size_bytes=1024,
            last_modified="2025-08-30T00:00:00",
            json_error=None
        )
        print("  ✅ FileAnalysis model created successfully")
        
        # Test AuditResults
        audit_results = AuditResults(
            timestamp="2025-08-30T00:00:00",
            file_analysis={"test.json": file_analysis},
            structure_validation={"total_files": 1, "existing_files": 1},
            metadata_consistency={"consistency_score": 1.0},
            critical_issues=[]
        )
        print("  ✅ AuditResults model created successfully")
        
        # Test IntegrityIssues
        integrity_issue = IntegrityIssues(
            issue_id="ISSUE_001",
            title="Test Issue",
            description="A test integrity issue",
            severity=IssueSeverity.MEDIUM,
            status=IssueStatus.OPEN,
            category="test",
            affected_files=["test.json"],
            detected_at="2025-08-30T00:00:00"
        )
        print("  ✅ IntegrityIssues model created successfully")
        
        # Test RecoveryAction
        recovery_action = RecoveryAction(
            action_id="ACTION_001",
            name="Test Action",
            description="A test recovery action",
            action_type=ActionType.REPAIR,
            status=ActionStatus.PENDING,
            parameters={"target_file": "test.json"},
            dependencies=[],
            estimated_duration=5
        )
        print("  ✅ RecoveryAction model created successfully")
        
        # Test RecoveryPlan
        recovery_plan = RecoveryPlan(
            plan_id="PLAN_001",
            timestamp="2025-08-30T00:00:00",
            strategy="comprehensive",
            issues_count=1,
            actions=[recovery_action],
            estimated_duration_minutes=5,
            priority="MEDIUM"
        )
        print("  ✅ RecoveryPlan model created successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Data model test failed: {e}")
        return False


def test_main_system():
    """Test that the main system can be instantiated."""
    print("✅ Testing main system instantiation...")
    
    try:
        # Test main system
        system = EmergencyContractDatabaseRecovery()
        print("  ✅ Main system instantiated successfully")
        
        # Test that components are available
        assert hasattr(system, 'database_auditor')
        assert hasattr(system, 'integrity_checker')
        assert hasattr(system, 'corruption_scanner')
        assert hasattr(system, 'recovery_executor')
        print("  ✅ All core components available")
        
        # Test that services are available
        assert hasattr(system, 'logging_service')
        assert hasattr(system, 'validation_service')
        assert hasattr(system, 'reporting_service')
        assert hasattr(system, 'notification_service')
        print("  ✅ All services available")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Main system test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚨 Emergency Database Recovery System - Basic Functionality Test")
    print("=" * 70)
    
    tests = [
        test_basic_imports,
        test_data_models,
        test_main_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
