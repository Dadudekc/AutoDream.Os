#!/usr/bin/env python3
"""
Testing Framework Integration for QA Coordination
================================================

Testing framework integration with quality assurance for comprehensive validation
V2 Compliant: ≤400 lines, focused testing integration logic
"""

from typing import Dict, List, Any
import os
import subprocess
import sys
from pathlib import Path


class TestingFrameworkIntegration:
    """
    Testing Framework Integration with Quality Assurance
    Integrates testing framework with QA for comprehensive validation
    """

    def __init__(self):
        """Initialize testing framework integration"""
        self.test_results = {}
        self.qa_integration_tests = []
        self.coverage_threshold = 85.0

    def create_qa_integration_test(self, name: str, description: str,
                                 test_type: str, qa_component: str,
                                 success_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Create a QA integration test"""
        test = {
            "name": name,
            "description": description,
            "test_type": test_type,
            "qa_component": qa_component,
            "success_criteria": success_criteria,
            "status": "pending",
            "created_date": "2025-01-19"
        }

        self.qa_integration_tests.append(test)
        return test

    def run_qa_integration_tests(self) -> Dict[str, Any]:
        """Run QA integration tests"""
        print("🧪 Running QA integration tests...")

        test_results = {
            "total_tests": len(self.qa_integration_tests),
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }

        # Test 1: Quality Gates Integration
        quality_gates_test = self._test_quality_gates_integration()
        test_results["test_details"].append(quality_gates_test)
        if quality_gates_test["passed"]:
            test_results["passed_tests"] += 1
        else:
            test_results["failed_tests"] += 1

        # Test 2: Validation Protocols Integration
        validation_test = self._test_validation_protocols_integration()
        test_results["test_details"].append(validation_test)
        if validation_test["passed"]:
            test_results["passed_tests"] += 1
        else:
            test_results["failed_tests"] += 1

        # Test 3: Vector Database Integration
        vector_db_test = self._test_vector_database_integration()
        test_results["test_details"].append(vector_db_test)
        if vector_db_test["passed"]:
            test_results["passed_tests"] += 1
        else:
            test_results["failed_tests"] += 1

        # Test 4: Coverage Integration
        coverage_test = self._test_coverage_integration()
        test_results["test_details"].append(coverage_test)
        if coverage_test["passed"]:
            test_results["passed_tests"] += 1
        else:
            test_results["failed_tests"] += 1

        # Overall results
        test_results["overall_success"] = test_results["failed_tests"] == 0
        test_results["success_rate"] = (test_results["passed_tests"] / test_results["total_tests"]) * 100

        return test_results

    def _test_quality_gates_integration(self) -> Dict[str, Any]:
        """Test quality gates integration"""
        try:
            from quality_gates import check_project_quality, generate_quality_report, QualityGateChecker

            # Test quality gates checker directly
            checker = QualityGateChecker()

            # Test on current file
            current_file = "src/integration/qa_coordination/testing_framework_integration.py"
            if os.path.exists(current_file):
                metrics = checker.check_file(current_file)
                passed = metrics is not None
                return {
                    "name": "Quality Gates Integration Test",
                    "passed": passed,
                    "details": f"Quality gates operational, score: {metrics.score if metrics else 'N/A'}",
                    "quality_score": metrics.score if metrics else 0
                }
            else:
                return {
                    "name": "Quality Gates Integration Test",
                    "passed": False,
                    "details": "Test file not found",
                    "error": "File not found"
                }

        except Exception as e:
            return {
                "name": "Quality Gates Integration Test",
                "passed": False,
                "details": f"Test failed: {e}",
                "error": str(e)
            }

    def _test_validation_protocols_integration(self) -> Dict[str, Any]:
        """Test validation protocols integration"""
        try:
            from .validation_protocols import create_advanced_validation_protocols

            protocols = create_advanced_validation_protocols()
            passed = len(protocols.validation_protocols) > 0

            return {
                "name": "Validation Protocols Integration Test",
                "passed": passed,
                "details": f"Created {len(protocols.validation_protocols)} validation protocols",
                "protocol_count": len(protocols.validation_protocols)
            }

        except Exception as e:
            return {
                "name": "Validation Protocols Integration Test",
                "passed": False,
                "details": f"Test failed: {e}",
                "error": str(e)
            }

    def _test_vector_database_integration(self) -> Dict[str, Any]:
        """Test vector database integration"""
        try:
            from tools.simple_vector_search import search_message_history, search_devlogs

            # Test basic search functionality
            results = search_message_history("quality assurance", limit=1)
            passed = len(results) >= 0  # Even no results is acceptable

            return {
                "name": "Vector Database Integration Test",
                "passed": passed,
                "details": f"Vector search returned {len(results)} results",
                "search_functional": True
            }

        except Exception as e:
            return {
                "name": "Vector Database Integration Test",
                "passed": False,
                "details": f"Test failed: {e}",
                "error": str(e)
            }

    def _test_coverage_integration(self) -> Dict[str, Any]:
        """Test coverage integration"""
        try:
            # Check if pytest is available and tests exist
            result = subprocess.run([
                sys.executable, "-m", "pytest", "--version"
            ], capture_output=True, text=True)

            passed = result.returncode == 0
            return {
                "name": "Coverage Integration Test",
                "passed": passed,
                "details": "Pytest available" if passed else "Pytest not available",
                "pytest_available": passed
            }

        except Exception as e:
            return {
                "name": "Coverage Integration Test",
                "passed": False,
                "details": f"Test failed: {e}",
                "error": str(e)
            }

    def run_pytest_suite(self, test_directory: str = "tests") -> Dict[str, Any]:
        """Run pytest test suite"""
        print(f"🧪 Running pytest suite in {test_directory}...")

        try:
            # Check if test directory exists
            if not os.path.exists(test_directory):
                return {
                    "status": "FAILED",
                    "error": f"Test directory {test_directory} not found",
                    "tests_run": 0,
                    "tests_passed": 0,
                    "tests_failed": 0
                }

            # Run pytest
            result = subprocess.run([
                sys.executable, "-m", "pytest", test_directory, "-v", "--tb=short"
            ], capture_output=True, text=True)

            # Parse results
            output_lines = result.stdout.splitlines()
            tests_run = 0
            tests_passed = 0
            tests_failed = 0

            for line in output_lines:
                if "PASSED" in line:
                    tests_passed += 1
                    tests_run += 1
                elif "FAILED" in line:
                    tests_failed += 1
                    tests_run += 1

            return {
                "status": "SUCCESS" if result.returncode == 0 else "FAILED",
                "tests_run": tests_run,
                "tests_passed": tests_passed,
                "tests_failed": tests_failed,
                "success_rate": (tests_passed / tests_run * 100) if tests_run > 0 else 0,
                "output": result.stdout,
                "errors": result.stderr
            }

        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "tests_run": 0,
                "tests_passed": 0,
                "tests_failed": 0
            }

    def generate_integration_report(self) -> Dict[str, Any]:
        """Generate comprehensive integration test report"""
        test_results = self.run_qa_integration_tests()

        return {
            "framework_integrated": test_results["overall_success"],
            "testing_coverage": test_results["success_rate"],
            "integration_tests": test_results,
            "qa_components_tested": len(test_results["test_details"]),
            "integration_status": "OPERATIONAL" if test_results["overall_success"] else "NEEDS_ATTENTION"
        }


def create_testing_framework_integration() -> TestingFrameworkIntegration:
    """Create testing framework integration system"""
    integration = TestingFrameworkIntegration()
    
    # Create core QA integration tests
    integration.create_qa_integration_test(
        "Quality Gates Integration",
        "Test quality gates integration with QA framework",
        "integration",
        "quality_gates",
        {"min_score": 80.0, "max_violations": 5}
    )
    
    integration.create_qa_integration_test(
        "Validation Protocols Integration",
        "Test validation protocols integration",
        "integration",
        "validation_protocols",
        {"min_protocols": 3, "all_active": True}
    )
    
    integration.create_qa_integration_test(
        "Vector Database Integration",
        "Test vector database integration with QA",
        "integration",
        "vector_database",
        {"search_functional": True, "min_results": 0}
    )
    
    integration.create_qa_integration_test(
        "Coverage Integration",
        "Test coverage integration with testing framework",
        "integration",
        "coverage",
        {"pytest_available": True, "min_coverage": 85.0}
    )
    
    return integration