#!/usr/bin/env python3
"""
Test Script for Unified Validation Framework

This script tests the unified validation framework to ensure all validators
are working correctly and can be used together.
"""

import sys
import os
from pathlib import Path

# Add the current working directory to the Python path
current_dir = Path.cwd()
sys.path.insert(0, str(current_dir))

from src.core.validation import ValidationManager, ValidationResult, ValidationSeverity, ValidationStatus


def test_validation_framework():
    """Test the unified validation framework"""
    print("🧪 Testing Unified Validation Framework")
    print("=" * 50)
    
    # Initialize the validation manager
    manager = ValidationManager()
    
    # Test 1: Check if all validators are registered
    print("\n1. Testing Validator Registration:")
    validators = manager.list_validators()
    expected_validators = [
        "contract", "config", "workflow", "message", "quality", 
        "security", "storage", "onboarding", "task", "code"
    ]
    
    for validator in expected_validators:
        if validator in validators:
            print(f"   ✅ {validator} validator registered")
        else:
            print(f"   ❌ {validator} validator missing")
    
    # Test 2: Test contract validation
    print("\n2. Testing Contract Validation:")
    contract_data = {
        "title": "Test Contract",
        "description": "A test contract for validation",
        "priority": "HIGH",
        "required_capabilities": ["python", "testing"],
        "deadline": "2024-12-31"
    }
    
    contract_results = manager.validate_with_validator("contract", contract_data)
    print(f"   Contract validation results: {len(contract_results)}")
    for result in contract_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 3: Test config validation
    print("\n3. Testing Config Validation:")
    config_data = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        },
        "api": {
            "endpoint": "https://api.example.com",
            "timeout": 30
        }
    }
    
    config_results = manager.validate_with_validator("config", config_data)
    print(f"   Config validation results: {len(config_results)}")
    for result in config_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 4: Test workflow validation
    print("\n4. Testing Workflow Validation:")
    workflow_data = {
        "name": "Test Workflow",
        "description": "A test workflow",
        "steps": [
            {"id": "start", "name": "Start", "type": "start"},
            {"id": "process", "name": "Process", "type": "process"},
            {"id": "end", "name": "End", "type": "end"}
        ],
        "transitions": [
            {"from_step": "start", "to_step": "process", "condition": "always"},
            {"from_step": "process", "to_step": "end", "condition": "completed"}
        ]
    }
    
    workflow_results = manager.validate_with_validator("workflow", workflow_data)
    print(f"   Workflow validation results: {len(workflow_results)}")
    for result in workflow_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 5: Test message validation
    print("\n5. Testing Message Validation:")
    message_data = {
        "id": "msg_001",
        "type": "notification",
        "content": "Test message content",
        "timestamp": "2024-01-01T12:00:00",
        "format": {
            "encoding": "utf-8",
            "content_type": "text/plain"
        }
    }
    
    message_results = manager.validate_with_validator("message", message_data)
    print(f"   Message validation results: {len(message_results)}")
    for result in message_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 6: Test quality validation
    print("\n6. Testing Quality Validation:")
    quality_data = {
        "file_path": "test.py",
        "metrics": {
            "cyclomatic_complexity": 5,
            "maintainability_index": 80,
            "code_duplication": 2.5,
            "test_coverage": 85.0
        },
        "timestamp": "2024-01-01T12:00:00"
    }
    
    quality_results = manager.validate_with_validator("quality", quality_data)
    print(f"   Quality validation results: {len(quality_results)}")
    for result in quality_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 7: Test security validation
    print("\n7. Testing Security Validation:")
    security_data = {
        "security_level": "high",
        "authentication_method": "token",
        "timestamp": "2024-01-01T12:00:00",
        "authentication": {
            "method": "token",
            "credentials": {
                "api_key": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            }
        }
    }
    
    security_results = manager.validate_with_validator("security", security_data)
    print(f"   Security validation results: {len(security_results)}")
    for result in security_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 8: Test storage validation
    print("\n8. Testing Storage Validation:")
    storage_data = {
        "type": "database",
        "name": "test_storage",
        "configuration": {
            "database_type": "postgresql",
            "connection_string": "postgresql://user:pass@localhost:5432/testdb"
        }
    }
    
    storage_results = manager.validate_with_validator("storage", storage_data)
    print(f"   Storage validation results: {len(storage_results)}")
    for result in storage_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 9: Test onboarding validation
    print("\n9. Testing Onboarding Validation:")
    onboarding_data = {
        "user_id": "user_001",
        "stage": "verification",
        "start_date": "2024-01-01T12:00:00",
        "status": "in_progress",
        "verification": {
            "method": "email",
            "status": "pending"
        }
    }
    
    onboarding_results = manager.validate_with_validator("onboarding", onboarding_data)
    print(f"   Onboarding validation results: {len(onboarding_results)}")
    for result in onboarding_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 10: Test task validation
    print("\n10. Testing Task Validation:")
    task_data = {
        "id": "task_001",
        "title": "Test Task",
        "description": "A test task for validation",
        "status": "in_progress",
        "priority": "high",
        "type": "development",
        "assignment": {
            "assignee": "developer_001",
            "estimated_effort": 8
        }
    }
    
    task_results = manager.validate_with_validator("task", task_data)
    print(f"   Task validation results: {len(task_results)}")
    for result in task_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 11: Test code validation
    print("\n11. Testing Code Validation:")
    code_data = {
        "file_path": "test.py",
        "content": "def test_function():\n    return 'Hello, World!'\n",
        "language": "python"
    }
    
    code_results = manager.validate_with_validator("code", code_data)
    print(f"   Code validation results: {len(code_results)}")
    for result in code_results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"   {status_icon} {result.rule_name}: {result.message}")
    
    # Test 12: Test validation summary
    print("\n12. Testing Validation Summary:")
    summary = manager.get_validation_summary()
    print(f"   Total validators: {summary['total_validators']}")
    print(f"   Total validations: {summary['total_validations']}")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    
    print("\n🎉 Unified Validation Framework Test Complete!")
    return True


if __name__ == "__main__":
    try:
        test_validation_framework()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
