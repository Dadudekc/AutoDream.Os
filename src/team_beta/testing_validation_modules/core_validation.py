#!/usr/bin/env python3
"""
Core Testing Validation System
===============================

Core testing validation system for Team Beta Testing Validation
V2 Compliant: ≤400 lines, focused core validation logic
"""

import json
from datetime import datetime
from typing import Any

from .models import (
    PlatformInfo,
    TestCase,
    TestCategory,
    TestMetrics,
    TestResult,
    TestStatus,
    ValidationReport,
)
from .test_execution import TestExecutor


class TestingValidationSystem:
    """
    Testing validation system for Team Beta mission.

    Provides comprehensive testing for Repository Management Interface,
    VSCode customization support, and cross-platform compatibility.
    """

    def __init__(self):
        """Initialize testing validation system"""
        self.test_cases: list[TestCase] = []
        self.test_results: list[TestResult] = []
        self.platform_info = self._get_platform_info()
        self.executor = TestExecutor()
        self._initialize_test_cases()

    def _get_platform_info(self) -> PlatformInfo:
        """Get platform information for compatibility testing"""
        import platform

        return PlatformInfo(
            system=platform.system(),
            release=platform.release(),
            version=platform.version(),
            machine=platform.machine(),
            processor=platform.processor(),
            python_version=platform.python_version(),
        )

    def _initialize_test_cases(self):
        """Initialize test cases for comprehensive validation"""
        self.test_cases = [
            TestCase(
                name="repository_cloning_functionality",
                category=TestCategory.FUNCTIONAL,
                description="Test repository cloning functionality",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="repository_status_management",
                category=TestCategory.FUNCTIONAL,
                description="Test repository status management",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="error_handling",
                category=TestCategory.FUNCTIONAL,
                description="Test error handling",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="vscode_customization_support",
                category=TestCategory.INTEGRATION,
                description="Test VSCode customization support",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="cross_platform_compatibility",
                category=TestCategory.INTEGRATION,
                description="Test cross-platform compatibility",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="windows_compatibility",
                category=TestCategory.COMPATIBILITY,
                description="Test Windows compatibility",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="linux_compatibility",
                category=TestCategory.COMPATIBILITY,
                description="Test Linux compatibility",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="macos_compatibility",
                category=TestCategory.COMPATIBILITY,
                description="Test macOS compatibility",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="cloning_performance",
                category=TestCategory.PERFORMANCE,
                description="Test cloning performance",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="memory_usage",
                category=TestCategory.PERFORMANCE,
                description="Test memory usage",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="user_interface",
                category=TestCategory.USABILITY,
                description="Test user interface",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
            TestCase(
                name="error_messages",
                category=TestCategory.USABILITY,
                description="Test error messages",
                status=TestStatus.PENDING,
                duration=0.0,
                errors=[],
                warnings=[],
                platform=self.platform_info.system,
            ),
        ]

    def run_all_tests(self) -> list[TestResult]:
        """Run all test cases"""
        print("🧪 Running comprehensive testing validation...")

        self.test_results = []

        for test_case in self.test_cases:
            print(f"📋 Executing: {test_case.name}")
            result = self.executor.execute_test(test_case)
            self.test_results.append(result)

            status_icon = "✅" if result.success else "❌"
            print(f"{status_icon} {test_case.name}: {test_case.status.value}")

        return self.test_results

    def run_tests_by_category(self, category: TestCategory) -> list[TestResult]:
        """Run tests by category"""
        print(f"🧪 Running {category.value} tests...")

        category_tests = [tc for tc in self.test_cases if tc.category == category]
        category_results = []

        for test_case in category_tests:
            print(f"📋 Executing: {test_case.name}")
            result = self.executor.execute_test(test_case)
            category_results.append(result)

            status_icon = "✅" if result.success else "❌"
            print(f"{status_icon} {test_case.name}: {test_case.status.value}")

        return category_results

    def get_test_metrics(self) -> TestMetrics:
        """Get test metrics"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - passed_tests
        skipped_tests = sum(
            1 for result in self.test_results if result.test_case.status == TestStatus.SKIPPED
        )

        total_duration = sum(result.test_case.duration for result in self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        return TestMetrics(
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            skipped_tests=skipped_tests,
            total_duration=total_duration,
            success_rate=success_rate,
        )

    def generate_validation_report(self) -> ValidationReport:
        """Generate comprehensive validation report"""
        print("📊 Generating validation report...")

        test_metrics = self.get_test_metrics()

        # Determine overall status
        if test_metrics.success_rate >= 90:
            overall_status = "EXCELLENT"
        elif test_metrics.success_rate >= 80:
            overall_status = "GOOD"
        elif test_metrics.success_rate >= 70:
            overall_status = "ACCEPTABLE"
        else:
            overall_status = "NEEDS_IMPROVEMENT"

        report = ValidationReport(
            report_id=f"team_beta_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            platform_info=self.platform_info,
            test_metrics=test_metrics,
            test_results=self.test_results,
            overall_status=overall_status,
            generated_at=datetime.now().isoformat(),
        )

        return report

    def save_report(self, report: ValidationReport, file_path: str = None) -> str:
        """Save validation report to file"""
        if file_path is None:
            file_path = f"team_beta_validation_report_{report.report_id}.json"

        try:
            # Convert to dictionary for JSON serialization
            report_dict = {
                "report_id": report.report_id,
                "platform_info": {
                    "system": report.platform_info.system,
                    "release": report.platform_info.release,
                    "version": report.platform_info.version,
                    "machine": report.platform_info.machine,
                    "processor": report.platform_info.processor,
                    "python_version": report.platform_info.python_version,
                },
                "test_metrics": {
                    "total_tests": report.test_metrics.total_tests,
                    "passed_tests": report.test_metrics.passed_tests,
                    "failed_tests": report.test_metrics.failed_tests,
                    "skipped_tests": report.test_metrics.skipped_tests,
                    "total_duration": report.test_metrics.total_duration,
                    "success_rate": report.test_metrics.success_rate,
                },
                "test_results": [
                    {
                        "test_case": {
                            "name": result.test_case.name,
                            "category": result.test_case.category.value,
                            "description": result.test_case.description,
                            "status": result.test_case.status.value,
                            "duration": result.test_case.duration,
                            "errors": result.test_case.errors,
                            "warnings": result.test_case.warnings,
                            "platform": result.test_case.platform,
                        },
                        "success": result.success,
                        "output": result.output,
                        "metrics": result.metrics,
                        "recommendations": result.recommendations,
                    }
                    for result in report.test_results
                ],
                "overall_status": report.overall_status,
                "generated_at": report.generated_at,
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report_dict, f, indent=2, ensure_ascii=False)

            print(f"📄 Validation report saved to: {file_path}")
            return file_path

        except Exception as e:
            print(f"❌ Failed to save validation report: {e}")
            return ""

    def get_summary(self) -> dict[str, Any]:
        """Get testing summary"""
        metrics = self.get_test_metrics()

        return {
            "total_tests": metrics.total_tests,
            "passed_tests": metrics.passed_tests,
            "failed_tests": metrics.failed_tests,
            "skipped_tests": metrics.skipped_tests,
            "success_rate": metrics.success_rate,
            "total_duration": metrics.total_duration,
            "platform": self.platform_info.system,
            "testing_complete": len(self.test_results) > 0,
        }


def main():
    """Main execution function"""
    print("🤖 Team Beta Testing Validation System")
    print("📦 Using modular testing_validation_modules package")

    # Create testing validation system
    testing_system = TestingValidationSystem()

    # Run all tests
    results = testing_system.run_all_tests()

    # Generate report
    report = testing_system.generate_validation_report()

    # Save report
    report_file = testing_system.save_report(report)

    # Get summary
    summary = testing_system.get_summary()

    print("✅ Testing Complete")
    print(f"📊 Success Rate: {summary['success_rate']:.1f}%")
    print(f"📄 Report: {report_file}")

    return testing_system
