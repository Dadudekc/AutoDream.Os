#!/usr/bin/env python3
"""
Demo Script for Unified Validation Framework

This script demonstrates practical usage of the unified validation framework
for various real-world scenarios.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the current working directory to the Python path
current_dir = Path.cwd()
sys.path.insert(0, str(current_dir))

from src.core.validation import ValidationManager, ValidationResult, ValidationSeverity, ValidationStatus


def demo_contract_validation():
    """Demonstrate contract validation"""
    print("📋 Contract Validation Demo")
    print("-" * 30)
    
    manager = ValidationManager()
    
    # Valid contract
    valid_contract = {
        "title": "Web Development Project",
        "description": "Build a modern web application",
        "priority": "HIGH",
        "required_capabilities": ["python", "django", "react"],
        "deadline": "2024-06-30",
        "budget": 50000,
        "client": "TechCorp Inc."
    }
    
    print("Validating valid contract...")
    results = manager.validate_with_validator("contract", valid_contract)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    # Invalid contract
    invalid_contract = {
        "title": "",  # Missing title
        "priority": "INVALID_PRIORITY",  # Invalid priority
        "deadline": "2023-01-01",  # Past deadline
        "budget": -1000  # Negative budget
    }
    
    print("\nValidating invalid contract...")
    results = manager.validate_with_validator("contract", invalid_contract)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    print()


def demo_workflow_validation():
    """Demonstrate workflow validation"""
    print("🔄 Workflow Validation Demo")
    print("-" * 30)
    
    manager = ValidationManager()
    
    # Valid workflow
    valid_workflow = {
        "name": "E-commerce Order Processing",
        "description": "Process customer orders from start to finish",
        "steps": [
            {"id": "order_received", "name": "Order Received", "type": "start"},
            {"id": "payment_verification", "name": "Payment Verification", "type": "process"},
            {"id": "inventory_check", "name": "Inventory Check", "type": "process"},
            {"id": "order_confirmation", "name": "Order Confirmation", "type": "end"}
        ],
        "transitions": [
            {"from_step": "order_received", "to_step": "payment_verification", "condition": "always"},
            {"from_step": "payment_verification", "to_step": "inventory_check", "condition": "payment_successful"},
            {"from_step": "inventory_check", "to_step": "order_confirmation", "condition": "inventory_available"}
        ]
    }
    
    print("Validating valid workflow...")
    results = manager.validate_with_validator("workflow", valid_workflow)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    # Invalid workflow
    invalid_workflow = {
        "name": "",  # Missing name
        "steps": [
            {"id": "step1", "name": "Step 1", "type": "invalid_type"}  # Invalid step type
        ],
        "transitions": [
            {"from_step": "nonexistent_step", "to_step": "step1", "condition": "always"}  # Invalid transition
        ]
    }
    
    print("\nValidating invalid workflow...")
    results = manager.validate_with_validator("workflow", invalid_workflow)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    print()


def demo_security_validation():
    """Demonstrate security validation"""
    print("🔒 Security Validation Demo")
    print("-" * 30)
    
    manager = ValidationManager()
    
    # Valid security config
    valid_security = {
        "security_level": "high",
        "authentication_method": "jwt",
        "timestamp": datetime.now().isoformat(),
        "authentication": {
            "method": "jwt",
            "credentials": {
                "jwt_secret": "super_secret_key_that_is_long_enough_for_security",
                "expiration_hours": 24
            }
        },
        "encryption": {
            "algorithm": "AES-256",
            "key_rotation_days": 30
        }
    }
    
    print("Validating valid security config...")
    results = manager.validate_with_validator("security", valid_security)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    # Invalid security config
    invalid_security = {
        "security_level": "low",  # Weak security level
        "authentication": {
            "method": "password",
            "credentials": {
                "password": "123"  # Weak password
            }
        }
    }
    
    print("\nValidating invalid security config...")
    results = manager.validate_with_validator("security", invalid_security)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    print()


def demo_quality_validation():
    """Demonstrate quality validation"""
    print("📊 Quality Validation Demo")
    print("-" * 30)
    
    manager = ValidationManager()
    
    # Valid quality metrics
    valid_quality = {
        "file_path": "src/main.py",
        "metrics": {
            "cyclomatic_complexity": 3,
            "maintainability_index": 85,
            "code_duplication": 1.2,
            "test_coverage": 92.5,
            "lines_of_code": 150,
            "technical_debt": 0.5
        },
        "timestamp": datetime.now().isoformat()
    }
    
    print("Validating valid quality metrics...")
    results = manager.validate_with_validator("quality", valid_quality)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    # Invalid quality metrics
    invalid_quality = {
        "file_path": "src/complex.py",
        "metrics": {
            "cyclomatic_complexity": 25,  # Too complex
            "maintainability_index": 30,  # Too low
            "test_coverage": 45.0,  # Too low
            "technical_debt": 15.0  # Too high
        }
    }
    
    print("\nValidating invalid quality metrics...")
    results = manager.validate_with_validator("quality", invalid_quality)
    
    for result in results:
        status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
        print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    print()


def demo_multi_validator_validation():
    """Demonstrate using multiple validators together"""
    print("🔗 Multi-Validator Validation Demo")
    print("-" * 40)
    
    manager = ValidationManager()
    
    # Complex data that needs multiple validations
    project_data = {
        "contract": {
            "title": "AI-Powered Analytics Platform",
            "description": "Build an intelligent analytics platform",
            "priority": "HIGH",
            "deadline": "2024-12-31",
            "budget": 100000
        },
        "workflow": {
            "name": "Development Pipeline",
            "steps": [
                {"id": "planning", "name": "Planning", "type": "start"},
                {"id": "development", "name": "Development", "type": "process"},
                {"id": "testing", "name": "Testing", "type": "process"},
                {"id": "deployment", "name": "Deployment", "type": "end"}
            ]
        },
        "security": {
            "security_level": "high",
            "authentication_method": "oauth2"
        },
        "quality": {
            "target_coverage": 90,
            "max_complexity": 10
        }
    }
    
    print("Validating project data with multiple validators...")
    
    # Validate each section with appropriate validator
    all_results = []
    
    for validator_name, data in project_data.items():
        if validator_name in manager.list_validators():
            results = manager.validate_with_validator(validator_name, data)
            all_results.extend(results)
            print(f"\n{validator_name.title()} validation results:")
            for result in results:
                status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌"
                print(f"  {status_icon} {result.rule_name}: {result.message}")
    
    # Get overall validation summary
    print(f"\n📈 Overall Validation Summary:")
    summary = manager.get_validation_summary()
    print(f"  Total validations: {summary['total_validations']}")
    print(f"  Success rate: {summary['success_rate']:.1f}%")
    
    # Count passed vs failed
    passed = sum(1 for r in all_results if r.status == ValidationStatus.PASSED)
    failed = sum(1 for r in all_results if r.status == ValidationStatus.FAILED)
    print(f"  Passed: {passed}, Failed: {failed}")
    
    print()


def main():
    """Run all demos"""
    print("🚀 Unified Validation Framework Demo")
    print("=" * 50)
    print()
    
    try:
        demo_contract_validation()
        demo_workflow_validation()
        demo_security_validation()
        demo_quality_validation()
        demo_multi_validator_validation()
        
        print("🎉 All demos completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
