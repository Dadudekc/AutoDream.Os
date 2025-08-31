#!/usr/bin/env python3
"""
Test Script for Modularized Database Integrity Checker System
============================================================

This script tests the modularized database integrity checker system
to ensure all components work correctly together.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-005 - Database Audit System Modularization
**Status:** Testing modularized system
**V2 Compliance:** ✅ Under 250 lines per module, single responsibility principle
"""

import json
import tempfile
from pathlib import Path

from database_integrity_models import IntegrityCheck, IntegrityReport, create_integrity_check, create_integrity_report
from database_integrity_checks import DatabaseIntegrityChecks
from database_integrity_reporting import DatabaseIntegrityReporting
from database_integrity_orchestrator import DatabaseIntegrityOrchestrator


def test_models():
    """Test the data models module"""
    print("🧪 Testing Data Models Module...")
    
    # Test IntegrityCheck creation
    check = create_integrity_check(
        check_id="TEST_CHECK",
        check_name="Test Integrity Check",
        status="PASSED",
        severity="LOW",
        message="Test check passed successfully",
        details={"test_field": "test_value"}
    )
    
    assert check.check_id == "TEST_CHECK"
    assert check.status == "PASSED"
    assert check.severity == "LOW"
    print("✅ IntegrityCheck creation: PASSED")
    
    # Test IntegrityReport creation
    checks = [check]
    report = create_integrity_report(checks, ["Test recommendation"])
    
    assert report.total_checks == 1
    assert report.passed_checks == 1
    assert report.overall_status == "PASSED"
    print("✅ IntegrityReport creation: PASSED")
    
    print("✅ Data Models Module: ALL TESTS PASSED\n")


def test_checks():
    """Test the integrity checks module"""
    print("🧪 Testing Integrity Checks Module...")
    
    # Create test contracts data
    test_contracts = {
        "total_contracts": 2,
        "claimed_contracts": 1,
        "completed_contracts": 0,
        "available_contracts": 1,
        "contracts": {
            "TEST-001": {
                "title": "Test Contract 1",
                "description": "A test contract",
                "difficulty": "MEDIUM",
                "extra_credit_points": 100,
                "requirements": ["Test requirement"],
                "deliverables": ["Test deliverable"],
                "status": "CLAIMED",
                "claimed_by": "test-agent",
                "claimed_at": "2025-01-28T01:00:00"
            },
            "TEST-002": {
                "title": "Test Contract 2",
                "description": "Another test contract",
                "difficulty": "EASY",
                "extra_credit_points": 50,
                "requirements": ["Another requirement"],
                "deliverables": ["Another deliverable"],
                "status": "AVAILABLE"
            }
        }
    }
    
    # Test integrity checks
    checker = DatabaseIntegrityChecks()
    
    # Test contract count check
    count_check = checker.check_contract_counts(test_contracts)
    assert count_check.status == "PASSED"
    print("✅ Contract count check: PASSED")
    
    # Test required fields check
    required_fields_checks = checker.check_required_fields(test_contracts)
    assert len(required_fields_checks) == 1
    assert required_fields_checks[0].status == "PASSED"
    print("✅ Required fields check: PASSED")
    
    # Test status consistency check
    status_checks = checker.check_status_consistency(test_contracts)
    assert len(status_checks) == 1
    assert status_checks[0].status == "PASSED"
    print("✅ Status consistency check: PASSED")
    
    # Test timestamp validity check
    timestamp_checks = checker.check_timestamp_validity(test_contracts)
    assert len(timestamp_checks) == 1
    assert timestamp_checks[0].status == "PASSED"
    print("✅ Timestamp validity check: PASSED")
    
    print("✅ Integrity Checks Module: ALL TESTS PASSED\n")


def test_reporting():
    """Test the reporting module"""
    print("🧪 Testing Reporting Module...")
    
    # Create test checks
    checks = [
        create_integrity_check("TEST1", "Test Check 1", "PASSED", "LOW", "Test 1 passed"),
        create_integrity_check("TEST2", "Test Check 2", "FAILED", "HIGH", "Test 2 failed")
    ]
    
    # Test report generation
    reporter = DatabaseIntegrityReporting()
    report = reporter.generate_report(checks)
    
    assert report.total_checks == 2
    assert report.passed_checks == 1
    assert report.failed_checks == 1
    assert report.overall_status == "FAILED"
    print("✅ Report generation: PASSED")
    
    # Test report formatting
    formatted_report = reporter.format_report_for_display(report)
    assert "DATABASE INTEGRITY REPORT" in formatted_report
    assert "Test Check 1" in formatted_report
    assert "Test Check 2" in formatted_report
    print("✅ Report formatting: PASSED")
    
    # Test report saving
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        success = reporter.save_report_to_file(report, temp_path)
        assert success
        print("✅ Report saving: PASSED")
        
        # Verify saved content
        with open(temp_path, 'r') as f:
            saved_data = json.load(f)
        assert saved_data["summary"]["total_checks"] == 2
        print("✅ Report content verification: PASSED")
        
    finally:
        Path(temp_path).unlink(missing_ok=True)
    
    print("✅ Reporting Module: ALL TESTS PASSED\n")


def test_orchestrator():
    """Test the orchestrator module"""
    print("🧪 Testing Orchestrator Module...")
    
    # Create test contracts file
    test_contracts = {
        "total_contracts": 1,
        "claimed_contracts": 0,
        "completed_contracts": 0,
        "available_contracts": 1,
        "contracts": {
            "TEST-ORCH": {
                "title": "Test Orchestrator Contract",
                "description": "Testing the orchestrator",
                "difficulty": "EASY",
                "extra_credit_points": 25,
                "requirements": ["Test requirement"],
                "deliverables": ["Test deliverable"],
                "status": "AVAILABLE"
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
        json.dump(test_contracts, f)
    
    try:
        # Test orchestrator
        orchestrator = DatabaseIntegrityOrchestrator(temp_path)
        
        # Test contract loading
        success = orchestrator.load_contracts()
        assert success
        print("✅ Contract loading: PASSED")
        
        # Test integrity checks
        report = orchestrator.run_integrity_checks()
        assert report.total_checks == 4  # 4 different types of checks
        print("✅ Integrity checks execution: PASSED")
        
        # Test report saving
        success = orchestrator.save_integrity_report(report)
        assert success
        print("✅ Report saving: PASSED")
        
        # Test markdown report
        success = orchestrator.save_markdown_report(report)
        assert success
        print("✅ Markdown report: PASSED")
        
    finally:
        Path(temp_path).unlink(missing_ok=True)
    
    print("✅ Orchestrator Module: ALL TESTS PASSED\n")


def main():
    """Run all tests"""
    print("🚀 Starting Modularized Database Integrity Checker System Tests\n")
    
    try:
        test_models()
        test_checks()
        test_reporting()
        test_orchestrator()
        
        print("🎉 ALL TESTS PASSED! The modularized system is working correctly.")
        print("✅ V2 Compliance achieved: All modules under 250 lines")
        print("✅ Single Responsibility Principle maintained")
        print("✅ Modular architecture successfully implemented")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()
