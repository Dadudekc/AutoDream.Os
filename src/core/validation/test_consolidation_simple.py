#!/usr/bin/env python3
"""
Simple Validator System Consolidation Test

This module tests individual validators to verify consolidation without import issues.
"""

import sys
import os
import unittest
from typing import Dict, Any

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import individual validators directly
from base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from storage_validator import StorageValidator
from onboarding_validator import OnboardingValidator
from config_validator import ConfigValidator
from workflow_validator import WorkflowValidator
from contract_validator import ContractValidator
from quality_validator import QualityValidator
from security_validator import SecurityValidator
from code_validator import CodeValidator


class TestValidatorConsolidationSimple(unittest.TestCase):
    """Test that all validator functionality has been successfully consolidated"""

    def setUp(self):
        """Set up test fixtures"""
        # Test data for various validators
        self.test_storage_data = {
            "type": "database",
            "name": "test_db",
            "configuration": {"host": "localhost", "port": 5432, "database": "test"},
        }

        self.test_onboarding_data = {
            "agent_id": "test_agent",
            "stage": "training",
            "status": "in_progress",
            "completed_phases": ["registration", "verification"],
            "performance_metrics": {
                "completion_time": 300,
                "success_rate": 85,
                "error_count": 2,
            },
        }

        self.test_config_data = {
            "database": {"host": "localhost", "port": 5432},
            "api": {"timeout": 30, "retries": 3},
        }

        self.test_workflow_data = {
            "workflow_id": "test_workflow",
            "name": "Test Workflow",
            "steps": [{"id": "step1", "name": "Start", "type": "start", "timeout": 60}],
        }

        self.test_contract_data = {
            "title": "Test Contract",
            "description": "A test contract",
            "priority": "high",
            "required_capabilities": ["python", "testing"],
        }

        self.test_quality_data = {
            "test_coverage": 85.0,
            "code_quality": 8.5,
            "performance_latency": 50.0,
        }

        self.test_security_data = {
            "password_min_length": 12,
            "require_special_chars": True,
            "mfa_required": True,
            "encryption_required": True,
        }

        self.test_code = """
def test_function():
    print("Hello, World!")
    return True

class TestClass:
    def __init__(self):
        self.value = 42
"""

    def test_storage_validator_consolidation(self):
        """Test that StorageValidator includes PersistentStorageValidator functionality"""
        storage_validator = StorageValidator()

        # Test unified validation
        results = storage_validator.validate(self.test_storage_data)
        self.assertIsInstance(results, list)

        # Test data integrity validation (from PersistentStorageValidator)
        test_data = {"key": "value"}
        checksum = storage_validator.calculate_checksum(test_data)
        self.assertIsInstance(checksum, str)
        self.assertTrue(len(checksum) > 0)

        # Test integrity validation
        integrity_result = storage_validator.validate_data_integrity(
            test_data, checksum
        )
        self.assertEqual(integrity_result.status.value, "passed")

        # Test with wrong checksum
        wrong_checksum = "wrong_checksum"
        integrity_result = storage_validator.validate_data_integrity(
            test_data, wrong_checksum
        )
        self.assertEqual(integrity_result.status.value, "failed")

    def test_onboarding_validator_consolidation(self):
        """Test that OnboardingValidator includes V2OnboardingSequenceValidator functionality"""
        onboarding_validator = OnboardingValidator()

        # Test unified validation
        results = onboarding_validator.validate(self.test_onboarding_data)
        self.assertIsInstance(results, list)
        from validation_reporting import generate_validation_report

        report = generate_validation_report(results)
        self.assertIn("total", report)

        # Test V2OnboardingSequenceValidator functionality
        session = {"session_id": "test_session", "agent_id": "test_agent"}
        phase_response = onboarding_validator._wait_for_phase_response(
            session, "training", "msg123"
        )
        self.assertTrue(phase_response)

        # Test onboarding completion validation
        completion_valid = onboarding_validator._validate_onboarding_completion(
            self.test_onboarding_data,
            {
                "test_agent": {
                    "onboarding_phases": ["registration", "verification", "training"]
                }
            },
            None,
        )
        self.assertIsInstance(completion_valid, bool)

        # Test performance metrics validation
        metrics_valid = onboarding_validator._validate_performance_metrics(
            self.test_onboarding_data
        )
        self.assertIsInstance(metrics_valid, bool)

    def test_config_validator_consolidation(self):
        """Test that ConfigValidator includes ConfigManagerValidator functionality"""
        config_validator = ConfigValidator()

        # Test unified validation
        results = config_validator.validate(self.test_config_data)
        self.assertIsInstance(results, list)

        # Test ConfigManagerValidator functionality
        section_results = config_validator.validate_config_sections(
            self.test_config_data
        )
        self.assertIsInstance(section_results, dict)

        # Test validation summary
        summary = config_validator.get_validation_summary(self.test_config_data)
        self.assertIsInstance(summary, dict)
        self.assertIn("total_sections", summary)
        self.assertIn("pass_rate", summary)

    def test_workflow_validator_consolidation(self):
        """Test that WorkflowValidator includes advanced workflow validation functionality"""
        workflow_validator = WorkflowValidator()

        # Test unified validation
        results = workflow_validator.validate(self.test_workflow_data)
        self.assertIsInstance(results, list)

        # Test advanced workflow validation functionality
        execution_data = {
            "execution_id": "exec123",
            "workflow_id": "test_workflow",
            "status": "completed",
            "actual_completion": "2024-01-01T12:00:00",
        }

        execution_results = workflow_validator.validate_workflow_execution_state(
            execution_data
        )
        self.assertIsInstance(execution_results, list)

        # Test performance metrics validation
        metrics_data = {"execution_time": 5000, "memory_usage": 512}
        metrics_results = workflow_validator.validate_performance_metrics(metrics_data)
        self.assertIsInstance(metrics_results, list)

        # Test validation summary
        summary = workflow_validator.get_validation_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("total_errors", summary)
        self.assertIn("total_warnings", summary)

    def test_contract_validator_consolidation(self):
        """Test that ContractValidator includes duplicate validation.py functionality"""
        contract_validator = ContractValidator()

        # Test unified validation
        results = contract_validator.validate(self.test_contract_data)
        self.assertIsInstance(results, list)

        # Test legacy validation method (from duplicate validation.py)
        legacy_results = contract_validator.validate_contract_legacy(
            self.test_contract_data
        )
        self.assertIsInstance(legacy_results, list)

        # Test validation summary
        summary = contract_validator.get_validation_summary(self.test_contract_data)
        self.assertIsInstance(summary, dict)
        self.assertIn("unified_validation", summary)
        self.assertIn("legacy_validation", summary)

    def test_quality_validator_consolidation(self):
        """Test that QualityValidator includes duplicate quality_validator.py functionality"""
        quality_validator = QualityValidator()

        # Test unified validation
        results = quality_validator.validate(self.test_quality_data)
        self.assertIsInstance(results, list)

        # Test legacy validation method (from duplicate quality_validator.py)
        legacy_results = quality_validator.validate_service_quality_legacy(
            "test_service", self.test_quality_data
        )
        self.assertIsInstance(legacy_results, list)

        # Test legacy validation summary
        legacy_summary = quality_validator.get_validation_summary_legacy("test_service")
        self.assertIsInstance(legacy_summary, dict)
        self.assertIn("total_validations", legacy_summary)

    def test_security_validator_consolidation(self):
        """Test that SecurityValidator includes duplicate policy_validator.py functionality"""
        security_validator = SecurityValidator()

        # Test unified validation
        results = security_validator.validate(self.test_security_data)
        self.assertIsInstance(results, list)

        # Test legacy validation method (from duplicate policy_validator.py)
        legacy_results = security_validator.validate_security_policy_legacy(
            self.test_security_data
        )
        self.assertIsInstance(legacy_results, dict)
        self.assertIn("is_valid", legacy_results)
        self.assertIn("compliance_score", legacy_results)

        # Test security policy summary
        summary = security_validator.get_security_policy_summary(
            self.test_security_data
        )
        self.assertIsInstance(summary, dict)
        self.assertIn("unified_validation", summary)
        self.assertIn("legacy_validation", summary)

    def test_code_validator_consolidation(self):
        """Test that CodeValidator includes duplicate ai_ml/validation.py functionality"""
        code_validator = CodeValidator()

        # Test unified validation
        results = code_validator.validate({"code": self.test_code})
        self.assertIsInstance(results, list)

        # Test legacy validation method (from duplicate ai_ml/validation.py)
        # This should not raise an exception for valid code
        try:
            code_validator.validate_code_legacy(self.test_code)
            legacy_valid = True
        except ValueError:
            legacy_valid = False

        self.assertTrue(legacy_valid)

        # Test validation with legacy fallback
        validation_result = code_validator.validate_code_with_legacy_fallback(
            self.test_code
        )
        self.assertIsInstance(validation_result, dict)
        self.assertIn("unified_validation", validation_result)
        self.assertIn("legacy_validation", validation_result)

        # Test code validation summary
        summary = code_validator.get_code_validation_summary(self.test_code)
        self.assertIsInstance(summary, dict)
        self.assertIn("code_statistics", summary)
        self.assertIn("function_count", summary["code_statistics"])

    def test_consolidation_completeness(self):
        """Test that all duplicate functionality has been successfully consolidated"""
        # This test ensures that all the duplicate validators' functionality
        # is now available through the unified framework

        # Test that StorageValidator has PersistentStorageValidator methods
        storage_validator = StorageValidator()
        self.assertTrue(hasattr(storage_validator, "validate_data_integrity"))
        self.assertTrue(hasattr(storage_validator, "calculate_checksum"))

        # Test that OnboardingValidator has V2OnboardingSequenceValidator methods
        onboarding_validator = OnboardingValidator()
        self.assertTrue(hasattr(onboarding_validator, "_wait_for_phase_response"))
        self.assertTrue(
            hasattr(onboarding_validator, "_validate_onboarding_completion")
        )

        # Test that ConfigValidator has ConfigManagerValidator methods
        config_validator = ConfigValidator()
        self.assertTrue(hasattr(config_validator, "validate_config_sections"))
        self.assertTrue(hasattr(config_validator, "get_validation_summary"))

        # Test that WorkflowValidator has advanced workflow validation methods
        workflow_validator = WorkflowValidator()
        self.assertTrue(
            hasattr(workflow_validator, "validate_workflow_execution_state")
        )
        self.assertTrue(hasattr(workflow_validator, "validate_performance_metrics"))

        # Test that ContractValidator has duplicate validation.py methods
        contract_validator = ContractValidator()
        self.assertTrue(hasattr(contract_validator, "validate_contract_legacy"))
        self.assertTrue(hasattr(contract_validator, "get_validation_summary"))

        # Test that QualityValidator has duplicate quality_validator.py methods
        quality_validator = QualityValidator()
        self.assertTrue(hasattr(quality_validator, "validate_service_quality_legacy"))
        self.assertTrue(hasattr(quality_validator, "get_validation_summary_legacy"))

        # Test that SecurityValidator has duplicate policy_validator.py methods
        security_validator = SecurityValidator()
        self.assertTrue(hasattr(security_validator, "validate_security_policy_legacy"))
        self.assertTrue(hasattr(security_validator, "get_security_policy_summary"))

        # Test that CodeValidator has duplicate ai_ml/validation.py methods
        code_validator = CodeValidator()
        self.assertTrue(hasattr(code_validator, "validate_code_legacy"))
        self.assertTrue(hasattr(code_validator, "validate_code_with_legacy_fallback"))


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
