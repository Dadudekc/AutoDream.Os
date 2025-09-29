#!/usr/bin/env python3
"""
Agent-7 Interface Functionality Tests
=====================================

Functionality testing for Agent-7 Repository Management Interface
V2 Compliant: ≤400 lines, focused testing logic
"""

import time
from typing import Any

from .models import RepositoryTestData, TestCategory, TestResult, TestStatus


class Agent7FunctionalityTests:
    """Agent-7 Repository Management Interface Functionality Tests"""

    def __init__(self):
        """Initialize functionality tests"""
        self.test_results: list[TestResult] = []
        self.test_data = self._create_test_data()

    def _create_test_data(self) -> list[RepositoryTestData]:
        """Create test data for repository testing"""
        return [
            RepositoryTestData(
                repository_url="https://github.com/test/repo1.git",
                repository_name="test-repo1",
                expected_status="active",
                test_scenario="valid_repository",
                expected_outcome="success",
            ),
            RepositoryTestData(
                repository_url="https://github.com/test/repo2.git",
                repository_name="test-repo2",
                expected_status="cloning",
                test_scenario="cloning_process",
                expected_outcome="success",
            ),
            RepositoryTestData(
                repository_url="invalid-url",
                repository_name="invalid-repo",
                expected_status="error",
                test_scenario="invalid_repository",
                expected_outcome="error",
            ),
        ]

    def test_repository_addition(self) -> dict[str, Any]:
        """Test repository addition functionality"""
        print("🔍 Testing repository addition...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            # Create test interface
            interface = RepositoryManagerInterface()

            # Test adding valid repository
            test_repo = self.test_data[0]
            result = interface.add_repository(test_repo.repository_url, test_repo.repository_name)

            passed = result.get("success", False)
            score = 100.0 if passed else 0.0
            issues = [] if passed else ["Repository addition failed"]
            recommendations = ["Ensure repository URL is valid"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "test_data": test_repo.repository_name,
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check interface implementation"],
                "error": str(e),
            }

    def test_repository_status_management(self) -> dict[str, Any]:
        """Test repository status management functionality"""
        print("🔍 Testing repository status management...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            interface = RepositoryManagerInterface()

            # Test status management
            test_repo = self.test_data[1]
            interface.add_repository(test_repo.repository_url, test_repo.repository_name)

            # Check status
            status = interface.get_repository_status(test_repo.repository_name)
            passed = status is not None
            score = 100.0 if passed else 0.0

            issues = [] if passed else ["Status management failed"]
            recommendations = ["Implement proper status tracking"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "status": status,
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check status management implementation"],
                "error": str(e),
            }

    def test_clone_operation_tracking(self) -> dict[str, Any]:
        """Test clone operation tracking functionality"""
        print("🔍 Testing clone operation tracking...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            interface = RepositoryManagerInterface()

            # Test clone tracking
            test_repo = self.test_data[0]
            interface.add_repository(test_repo.repository_url, test_repo.repository_name)

            # Start clone operation
            clone_result = interface.clone_repository(test_repo.repository_name)
            passed = clone_result.get("success", False)
            score = 100.0 if passed else 0.0

            issues = [] if passed else ["Clone operation failed"]
            recommendations = ["Implement proper clone tracking"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "clone_result": clone_result,
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check clone operation implementation"],
                "error": str(e),
            }

    def test_error_handling(self) -> dict[str, Any]:
        """Test error handling and resolution functionality"""
        print("🔍 Testing error handling...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            interface = RepositoryManagerInterface()

            # Test error handling with invalid repository
            test_repo = self.test_data[2]  # Invalid repository
            result = interface.add_repository(test_repo.repository_url, test_repo.repository_name)

            # Should handle error gracefully
            passed = "error" in result or not result.get("success", True)
            score = 100.0 if passed else 0.0

            issues = [] if passed else ["Error handling failed"]
            recommendations = ["Implement proper error handling"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "error_result": result,
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check error handling implementation"],
                "error": str(e),
            }

    def test_dashboard_data_generation(self) -> dict[str, Any]:
        """Test dashboard data generation functionality"""
        print("🔍 Testing dashboard data generation...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            interface = RepositoryManagerInterface()

            # Add test repositories
            for test_repo in self.test_data[:2]:  # Use first two valid repos
                interface.add_repository(test_repo.repository_url, test_repo.repository_name)

            # Generate dashboard data
            dashboard_data = interface.generate_dashboard_data()
            passed = dashboard_data is not None and len(dashboard_data) > 0
            score = 100.0 if passed else 0.0

            issues = [] if passed else ["Dashboard data generation failed"]
            recommendations = ["Implement dashboard data generation"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "dashboard_data": dashboard_data,
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check dashboard data generation implementation"],
                "error": str(e),
            }

    def test_repository_validation(self) -> dict[str, Any]:
        """Test repository validation functionality"""
        print("🔍 Testing repository validation...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            interface = RepositoryManagerInterface()

            # Test validation with valid repository
            test_repo = self.test_data[0]
            validation_result = interface.validate_repository(test_repo.repository_url)
            passed = validation_result.get("valid", False)
            score = 100.0 if passed else 0.0

            issues = [] if passed else ["Repository validation failed"]
            recommendations = ["Implement proper repository validation"] if not passed else []

            return {
                "passed": passed,
                "score": score,
                "issues": issues,
                "recommendations": recommendations,
                "validation_result": validation_result,
            }

        except Exception as e:
            return {
                "passed": False,
                "score": 0.0,
                "issues": [f"Test failed: {str(e)}"],
                "recommendations": ["Check repository validation implementation"],
                "error": str(e),
            }

    def run_all_functionality_tests(self) -> list[TestResult]:
        """Run all functionality tests"""
        print("🧪 Running all functionality tests...")

        functionality_tests = [
            ("TC001", "Repository Addition", self.test_repository_addition),
            ("TC002", "Repository Status Management", self.test_repository_status_management),
            ("TC003", "Clone Operation Tracking", self.test_clone_operation_tracking),
            ("TC004", "Error Handling and Resolution", self.test_error_handling),
            ("TC005", "Dashboard Data Generation", self.test_dashboard_data_generation),
            ("TC006", "Repository Validation", self.test_repository_validation),
        ]

        test_results = []

        for test_id, test_name, test_func in functionality_tests:
            start_time = time.time()
            try:
                result = test_func()
                execution_time = time.time() - start_time

                test_result = TestResult(
                    test_id=test_id,
                    test_name=test_name,
                    category=TestCategory.FUNCTIONALITY,
                    status=TestStatus.PASSED if result["passed"] else TestStatus.FAILED,
                    score=result["score"],
                    issues=result["issues"],
                    recommendations=result["recommendations"],
                    execution_time=execution_time,
                )

                test_results.append(test_result)
                print(
                    f"✅ {test_name}: {'PASSED' if result['passed'] else 'FAILED'} ({result['score']:.1f}%)"
                )

            except Exception as e:
                execution_time = time.time() - start_time
                test_result = TestResult(
                    test_id=test_id,
                    test_name=test_name,
                    category=TestCategory.FUNCTIONALITY,
                    status=TestStatus.FAILED,
                    score=0.0,
                    issues=[f"Test execution failed: {str(e)}"],
                    recommendations=["Fix test implementation"],
                    execution_time=execution_time,
                )

                test_results.append(test_result)
                print(f"❌ {test_name}: FAILED - {str(e)}")

        self.test_results = test_results
        return test_results
