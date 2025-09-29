#!/usr/bin/env python3
"""
Agent-7 Interface Core Testing System
====================================

Core testing system for Agent-7 Repository Management Interface
V2 Compliant: ≤400 lines, focused core testing logic
"""

import json
from datetime import datetime
from typing import Any

from .functionality_tests import Agent7FunctionalityTests
from .integration_tests import Agent7IntegrationTests
from .models import TestCategory, TestResult, TestStatus


class Agent7InterfaceTestingValidation:
    """Agent-7 Repository Management Interface Testing & Validation System"""

    def __init__(self):
        """Initialize testing validation system"""
        self.test_results: list[TestResult] = []
        self.interface_analysis: dict[str, Any] = {}
        self.validation_report: dict[str, Any] = {}
        self.functionality_tests = Agent7FunctionalityTests()
        self.integration_tests = Agent7IntegrationTests()

    def test_repository_management_interface(self) -> dict[str, Any]:
        """Test Agent-7's repository management interface functionality"""
        print("🧪 Testing Agent-7 Repository Management Interface...")

        # Check interface availability
        interface_available = self._check_interface_availability()
        if not interface_available:
            return {
                "interface_available": False,
                "error": "Agent-7's Repository Management Interface not accessible",
            }

        # Run functionality tests
        functionality_results = self.functionality_tests.run_all_functionality_tests()
        self.test_results.extend(functionality_results)

        # Run integration tests
        integration_results = self.integration_tests.run_all_integration_tests()
        self.test_results.extend(integration_results)

        # Generate analysis
        self.interface_analysis = self._analyze_interface()

        # Generate validation report
        self.validation_report = self._generate_validation_report()

        return {
            "interface_available": True,
            "functionality_tests": len(functionality_results),
            "integration_tests": len(integration_results),
            "total_tests": len(self.test_results),
            "interface_analysis": self.interface_analysis,
            "validation_report": self.validation_report,
        }

    def _check_interface_availability(self) -> bool:
        """Check if Agent-7's interface is available"""
        try:
            from src.team_beta.repository_manager import (
                ErrorType,
                RepositoryManagerInterface,
                RepositoryStatus,
                create_sample_repository_manager,
            )

            return True
        except ImportError:
            print("❌ Agent-7's Repository Management Interface not accessible")
            return False

    def _analyze_interface(self) -> dict[str, Any]:
        """Analyze the interface for quality metrics"""
        print("📊 Analyzing interface quality...")

        try:
            from src.team_beta.repository_manager import RepositoryManagerInterface

            # Analyze interface structure
            interface = RepositoryManagerInterface()

            # Count components and methods
            component_count = len(getattr(interface, "__dict__", {}))
            method_count = len(
                [
                    method
                    for method in dir(interface)
                    if not method.startswith("_") and callable(getattr(interface, method))
                ]
            )

            # Calculate complexity score (simplified)
            complexity_score = min(100.0, (component_count + method_count) * 5)

            # Calculate maintainability score
            maintainability_score = max(0.0, 100.0 - complexity_score * 0.5)

            # Calculate testability score
            testability_score = 100.0 if len(self.test_results) > 0 else 0.0

            # Identify issues
            issues = []
            if complexity_score > 80:
                issues.append("High complexity detected")
            if maintainability_score < 60:
                issues.append("Low maintainability score")
            if testability_score < 80:
                issues.append("Low testability score")

            # Generate recommendations
            recommendations = []
            if complexity_score > 80:
                recommendations.append("Consider refactoring to reduce complexity")
            if maintainability_score < 60:
                recommendations.append("Improve code documentation and structure")
            if testability_score < 80:
                recommendations.append("Add more comprehensive tests")

            return {
                "interface_name": "RepositoryManagerInterface",
                "component_count": component_count,
                "method_count": method_count,
                "complexity_score": complexity_score,
                "maintainability_score": maintainability_score,
                "testability_score": testability_score,
                "issues": issues,
                "recommendations": recommendations,
                "analysis_status": "COMPLETE",
            }

        except Exception as e:
            return {
                "interface_name": "RepositoryManagerInterface",
                "error": str(e),
                "analysis_status": "FAILED",
            }

    def _generate_validation_report(self) -> dict[str, Any]:
        """Generate comprehensive validation report"""
        print("📋 Generating validation report...")

        # Calculate test statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test.status == TestStatus.PASSED)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # Calculate overall score
        overall_score = (
            sum(test.score for test in self.test_results) / total_tests if total_tests > 0 else 0
        )

        # Categorize test results
        functionality_tests = [
            test for test in self.test_results if test.category == TestCategory.FUNCTIONALITY
        ]
        integration_tests = [
            test for test in self.test_results if test.category == TestCategory.INTEGRATION
        ]

        # Generate report
        report = {
            "report_id": f"agent7_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "interface_name": "RepositoryManagerInterface",
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "overall_score": overall_score,
            "test_categories": {
                "functionality": {
                    "total": len(functionality_tests),
                    "passed": sum(
                        1 for test in functionality_tests if test.status == TestStatus.PASSED
                    ),
                    "score": sum(test.score for test in functionality_tests)
                    / len(functionality_tests)
                    if functionality_tests
                    else 0,
                },
                "integration": {
                    "total": len(integration_tests),
                    "passed": sum(
                        1 for test in integration_tests if test.status == TestStatus.PASSED
                    ),
                    "score": sum(test.score for test in integration_tests) / len(integration_tests)
                    if integration_tests
                    else 0,
                },
            },
            "test_results": [
                {
                    "test_id": test.test_id,
                    "test_name": test.test_name,
                    "category": test.category.value,
                    "status": test.status.value,
                    "score": test.score,
                    "execution_time": test.execution_time,
                }
                for test in self.test_results
            ],
            "interface_analysis": self.interface_analysis,
            "generated_at": datetime.now().isoformat(),
            "validation_status": "PASSED" if success_rate >= 80 else "FAILED",
        }

        return report

    def save_validation_report(self, file_path: str = None) -> str:
        """Save validation report to file"""
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"agent7_validation_report_{timestamp}.json"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.validation_report, f, indent=2, ensure_ascii=False)

            print(f"📄 Validation report saved to: {file_path}")
            return file_path

        except Exception as e:
            print(f"❌ Failed to save validation report: {e}")
            return ""

    def get_test_summary(self) -> dict[str, Any]:
        """Get test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test.status == TestStatus.PASSED)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "validation_status": "PASSED" if success_rate >= 80 else "FAILED",
            "interface_analysis_complete": bool(self.interface_analysis),
            "validation_report_generated": bool(self.validation_report),
        }


def run_agent7_interface_testing_validation() -> dict[str, Any]:
    """Run Agent-7 interface testing validation"""
    print("🤖 Starting Agent-7 Interface Testing & Validation...")

    # Create testing validation system
    testing_system = Agent7InterfaceTestingValidation()

    # Run comprehensive testing
    results = testing_system.test_repository_management_interface()

    # Save validation report
    report_file = testing_system.save_validation_report()

    # Get test summary
    summary = testing_system.get_test_summary()

    print("✅ Agent-7 Interface Testing Complete")
    print(
        f"📊 Tests: {summary['passed_tests']}/{summary['total_tests']} passed ({summary['success_rate']:.1f}%)"
    )
    print(f"📄 Report: {report_file}")

    return {
        "testing_complete": True,
        "test_summary": summary,
        "validation_report": results.get("validation_report", {}),
        "report_file": report_file,
        "interface_analysis": results.get("interface_analysis", {}),
    }
