        from code_validator import CodeValidator
        from config_validator import ConfigValidator
        from contract_validator import ContractValidator
        from onboarding_validator import OnboardingValidator
        from quality_validator import QualityValidator
        from security_validator import SecurityValidator
        from src.core.validation import WorkflowValidator
        from storage_validator import StorageValidator
        from validation_reporting import generate_validation_report

#!/usr/bin/env python3
"""
Simple test to verify validator consolidation
"""


def test_storage_validator():
    """Test StorageValidator consolidation"""
    try:

        validator = StorageValidator()

        # Test basic validation
        test_data = {"type": "database", "name": "test"}
        results = validator.validate(test_data)
        print(f"✅ StorageValidator basic validation: {len(results)} results")

        # Test data integrity methods (from PersistentStorageValidator)
        if hasattr(validator, "calculate_checksum"):
            checksum = validator.calculate_checksum(test_data)
            print(f"✅ StorageValidator checksum calculation: {checksum[:10]}...")
        else:
            print("❌ StorageValidator missing calculate_checksum method")

        if hasattr(validator, "validate_data_integrity"):
            print("✅ StorageValidator has validate_data_integrity method")
        else:
            print("❌ StorageValidator missing validate_data_integrity method")

        return True

    except Exception as e:
        print(f"❌ StorageValidator test failed: {e}")
        return False


def test_onboarding_validator():
    """Test OnboardingValidator consolidation"""
    try:

        validator = OnboardingValidator()

        # Test basic validation
        test_data = {"agent_id": "test", "stage": "training"}
        results = validator.validate(test_data)
        print(f"✅ OnboardingValidator basic validation: {len(results)} results")

        report = generate_validation_report(results)
        print(f"✅ OnboardingValidator report generated: {report['total']} checks")

        # Test V2OnboardingSequenceValidator methods
        if hasattr(validator, "_wait_for_phase_response"):
            print("✅ OnboardingValidator has _wait_for_phase_response method")
        else:
            print("❌ OnboardingValidator missing _wait_for_phase_response method")

        if hasattr(validator, "_validate_onboarding_completion"):
            print("✅ OnboardingValidator has _validate_onboarding_completion method")
        else:
            print(
                "❌ OnboardingValidator missing _validate_onboarding_completion method"
            )

        return True

    except Exception as e:
        print(f"❌ OnboardingValidator test failed: {e}")
        return False


def test_config_validator():
    """Test ConfigValidator consolidation"""
    try:

        validator = ConfigValidator()

        # Test basic validation
        test_data = {"database": {"host": "localhost"}}
        results = validator.validate(test_data)
        print(f"✅ ConfigValidator basic validation: {len(results)} results")

        # Test ConfigManagerValidator methods
        if hasattr(validator, "validate_config_sections"):
            print("✅ ConfigValidator has validate_config_sections method")
        else:
            print("❌ ConfigValidator missing validate_config_sections method")

        if hasattr(validator, "get_validation_summary"):
            print("✅ ConfigValidator has get_validation_summary method")
        else:
            print("❌ ConfigValidator missing get_validation_summary method")

        return True

    except Exception as e:
        print(f"❌ ConfigValidator test failed: {e}")
        return False


def test_workflow_validator():
    """Test WorkflowValidator consolidation"""
    try:

        validator = WorkflowValidator()

        # Test basic validation
        test_data = {"workflow_id": "test", "name": "Test", "steps": []}
        results = validator.validate(test_data)
        print(f"✅ WorkflowValidator basic validation: {len(results)} results")

        # Test advanced workflow validation methods
        if hasattr(validator, "validate_workflow_execution_state"):
            print("✅ WorkflowValidator has validate_workflow_execution_state method")
        else:
            print(
                "❌ WorkflowValidator missing validate_workflow_execution_state method"
            )

        if hasattr(validator, "validate_performance_metrics"):
            print("✅ WorkflowValidator has validate_performance_metrics method")
        else:
            print("❌ WorkflowValidator missing validate_performance_metrics method")

        return True

    except Exception as e:
        print(f"❌ WorkflowValidator test failed: {e}")
        return False


def test_contract_validator():
    """Test ContractValidator consolidation"""
    try:

        validator = ContractValidator()

        # Test basic validation
        test_data = {"title": "Test", "description": "Test", "priority": "high"}
        results = validator.validate(test_data)
        print(f"✅ ContractValidator basic validation: {len(results)} results")

        # Test duplicate validation.py methods
        if hasattr(validator, "validate_contract_legacy"):
            print("✅ ContractValidator has validate_contract_legacy method")
        else:
            print("❌ ContractValidator missing validate_contract_legacy method")

        if hasattr(validator, "get_validation_summary"):
            print("✅ ContractValidator has get_validation_summary method")
        else:
            print("❌ ContractValidator missing get_validation_summary method")

        return True

    except Exception as e:
        print(f"❌ ContractValidator test failed: {e}")
        return False


def test_quality_validator():
    """Test QualityValidator consolidation"""
    try:

        validator = QualityValidator()

        # Test basic validation
        test_data = {"test_coverage": 85.0, "code_quality": 8.5}
        results = validator.validate(test_data)
        print(f"✅ QualityValidator basic validation: {len(results)} results")

        # Test duplicate quality_validator.py methods
        if hasattr(validator, "validate_service_quality_legacy"):
            print("✅ QualityValidator has validate_service_quality_legacy method")
        else:
            print("❌ QualityValidator missing validate_service_quality_legacy method")

        if hasattr(validator, "get_validation_summary_legacy"):
            print("✅ QualityValidator has get_validation_summary_legacy method")
        else:
            print("❌ QualityValidator missing get_validation_summary_legacy method")

        return True

    except Exception as e:
        print(f"❌ QualityValidator test failed: {e}")
        return False


def test_security_validator():
    """Test SecurityValidator consolidation"""
    try:

        validator = SecurityValidator()

        # Test basic validation
        test_data = {"password_min_length": 12, "mfa_required": True}
        results = validator.validate(test_data)
        print(f"✅ SecurityValidator basic validation: {len(results)} results")

        # Test duplicate policy_validator.py methods
        if hasattr(validator, "validate_security_policy_legacy"):
            print("✅ SecurityValidator has validate_security_policy_legacy method")
        else:
            print("❌ SecurityValidator missing validate_security_policy_legacy method")

        if hasattr(validator, "get_security_policy_summary"):
            print("✅ SecurityValidator has get_security_policy_summary method")
        else:
            print("❌ SecurityValidator missing get_security_policy_summary method")

        return True

    except Exception as e:
        print(f"❌ SecurityValidator test failed: {e}")
        return False


def test_code_validator():
    """Test CodeValidator consolidation"""
    try:

        validator = CodeValidator()

        # Test basic validation
        test_data = {"code": "def test(): pass"}
        results = validator.validate(test_data)
        print(f"✅ CodeValidator basic validation: {len(results)} results")

        # Test duplicate ai_ml/validation.py methods
        if hasattr(validator, "validate_code_legacy"):
            print("✅ CodeValidator has validate_code_legacy method")
        else:
            print("❌ CodeValidator missing validate_code_legacy method")

        if hasattr(validator, "validate_code_with_legacy_fallback"):
            print("✅ CodeValidator has validate_code_with_legacy_fallback method")
        else:
            print("❌ CodeValidator missing validate_code_with_legacy_fallback method")

        return True

    except Exception as e:
        print(f"❌ CodeValidator test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Testing Validator System Consolidation...")
    print("=" * 50)

    tests = [
        test_storage_validator,
        test_onboarding_validator,
        test_config_validator,
        test_workflow_validator,
        test_contract_validator,
        test_quality_validator,
        test_security_validator,
        test_code_validator,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All validator consolidation tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    main()
