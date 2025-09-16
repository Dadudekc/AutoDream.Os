#!/usr/bin/env python3
"""
Test Self Validation Protocol - Self-Validation Protocol Test
===========================================================

Test script for self-validation protocol framework.
Part of the self-validation protocol implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
import tempfile
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.self_validation_protocol import (
    FileExistenceRule,
    FileSizeRule,
    SelfValidationProtocol,
    TaskCompletionRule,
    ValidationResult,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_validation_result():
    """Test ValidationResult class."""
    logger.info("Testing ValidationResult class...")

    try:
        # Test successful result
        success_result = ValidationResult(True, "Test success", {"key": "value"})
        assert success_result.success == True
        assert success_result.message == "Test success"
        assert success_result.details["key"] == "value"

        # Test failed result
        fail_result = ValidationResult(False, "Test failure")
        assert fail_result.success == False
        assert fail_result.message == "Test failure"

        # Test to_dict conversion
        result_dict = success_result.to_dict()
        assert result_dict["success"] == True
        assert "timestamp" in result_dict

        logger.info("✅ ValidationResult test passed")
        return True

    except Exception as e:
        logger.error(f"❌ ValidationResult test failed: {e}")
        return False


def test_validation_rules():
    """Test validation rules."""
    logger.info("Testing validation rules...")

    try:
        # Test FileExistenceRule
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("test content")
            temp_file_path = temp_file.name

        temp_path = Path(temp_file_path)

        # Test file existence rule with existing file
        existence_rule = FileExistenceRule(temp_path)
        result = existence_rule.validate()
        assert result.success == True

        # Test file existence rule with non-existing file
        non_existing_rule = FileExistenceRule("non_existing_file.txt")
        result = non_existing_rule.validate()
        assert result.success == False

        # Test FileSizeRule
        size_rule = FileSizeRule(temp_path, max_size=10)
        result = size_rule.validate()
        assert result.success == True  # 1 line should be <= 10

        # Test TaskCompletionRule
        task_rule = TaskCompletionRule("test_task", "completed")
        task_data = {"id": "test_task", "status": "completed"}
        result = task_rule.validate(task_data)
        assert result.success == True

        # Test task completion rule with wrong status
        task_data_wrong = {"id": "test_task", "status": "pending"}
        result = task_rule.validate(task_data_wrong)
        assert result.success == False

        # Clean up
        temp_path.unlink()

        logger.info("✅ Validation rules test passed")
        return True

    except Exception as e:
        logger.error(f"❌ Validation rules test failed: {e}")
        return False


def test_self_validation_protocol():
    """Test SelfValidationProtocol class."""
    logger.info("Testing SelfValidationProtocol class...")

    try:
        # Initialize protocol
        protocol = SelfValidationProtocol("Agent-2")

        # Test adding rules
        rule1 = FileExistenceRule("test_file_1.txt")
        rule2 = FileSizeRule("test_file_2.txt", max_size=100)
        rule3 = TaskCompletionRule("test_task", "completed")

        protocol.add_rule(rule1)
        protocol.add_rule(rule2)
        protocol.add_rule(rule3)

        # Test listing rules
        rules = protocol.list_rules()
        assert len(rules) == 3
        assert "FileExists_test_file_1.txt" in rules

        # Test getting rule
        retrieved_rule = protocol.get_rule("FileExists_test_file_1.txt")
        assert retrieved_rule is not None
        assert retrieved_rule.name == "FileExists_test_file_1.txt"

        # Test removing rule
        removed = protocol.remove_rule("FileExists_test_file_1.txt")
        assert removed == True
        assert len(protocol.list_rules()) == 2

        # Test validate_all
        results = protocol.validate_all()
        assert "overall_success" in results
        assert "rule_results" in results
        assert "summary" in results

        # Test validation history
        history = protocol.get_validation_history()
        assert len(history) == 1

        # Test report generation
        report = protocol.generate_report()
        assert "SELF-VALIDATION PROTOCOL REPORT" in report
        assert "Agent-2" in report

        # Test clearing history
        protocol.clear_history()
        assert len(protocol.get_validation_history()) == 0

        logger.info("✅ SelfValidationProtocol test passed")
        return True

    except Exception as e:
        logger.error(f"❌ SelfValidationProtocol test failed: {e}")
        return False


def test_integration_scenario():
    """Test integration scenario with real files."""
    logger.info("Testing integration scenario...")

    try:
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as temp_file:
            # Create a small file (V2 compliant)
            for i in range(50):
                temp_file.write(f"# Line {i + 1}\n")
            small_file_path = temp_file.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as temp_file:
            # Create a large file (V2 violation)
            for i in range(500):
                temp_file.write(f"# Line {i + 1}\n")
            large_file_path = temp_file.name

        small_path = Path(small_file_path)
        large_path = Path(large_file_path)

        # Initialize protocol
        protocol = SelfValidationProtocol("Agent-2")

        # Add rules
        protocol.add_rule(FileExistenceRule(small_path))
        protocol.add_rule(FileExistenceRule(large_path))
        protocol.add_rule(FileSizeRule(small_path, max_size=100))
        protocol.add_rule(FileSizeRule(large_path, max_size=100))

        # Test task completion rule
        task_data = {
            "id": "test_task",
            "status": "completed",
            "description": "Test task completion",
        }
        protocol.add_rule(TaskCompletionRule("test_task", "completed"))

        # Run validation
        results = protocol.validate_all(task_data)

        # Verify results
        assert results["overall_success"] == False  # Should fail due to large file
        assert results["summary"]["total_rules"] == 5
        assert results["summary"]["passed"] == 4  # 2 existence + 1 small file + 1 task
        assert results["summary"]["failed"] == 1  # 1 large file

        # Test individual rule validation
        small_file_result = protocol.validate_rule("FileSize_" + small_path.name)
        assert small_file_result is not None
        assert small_file_result.success == True

        large_file_result = protocol.validate_rule("FileSize_" + large_path.name)
        assert large_file_result is not None
        assert large_file_result.success == False

        # Generate report
        report = protocol.generate_report()
        assert "Failed: 1" in report

        # Clean up
        small_path.unlink()
        large_path.unlink()

        logger.info("✅ Integration scenario test passed")
        return True

    except Exception as e:
        logger.error(f"❌ Integration scenario test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting self-validation protocol tests...")

    test_results = []

    # Run tests
    test_results.append(("ValidationResult", test_validation_result()))
    test_results.append(("Validation Rules", test_validation_rules()))
    test_results.append(("SelfValidationProtocol", test_self_validation_protocol()))
    test_results.append(("Integration Scenario", test_integration_scenario()))

    # Report results
    logger.info("\n📊 Test Results Summary:")
    passed = 0
    failed = 0

    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1

    logger.info(f"\n🎯 Overall Results: {passed} passed, {failed} failed")

    if failed == 0:
        logger.info("🎉 All tests passed! Self-validation protocol is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

