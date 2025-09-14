"""
Testing Coordinator - Agent-4 Phase 2 Implementation
Comprehensive testing coordination and validation system.
"""

import json
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class TestType(Enum):
    """Test type enumeration."""
    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    REGRESSION = "regression"

@dataclass
class TestResult:
    """Test result data structure."""
    test_name: str
    test_type: TestType
    status: str  # PASSED, FAILED, SKIPPED, ERROR
    duration: float
    message: str
    details: dict[str, Any]

@dataclass
class TestSuite:
    """Test suite data structure."""
    name: str
    test_type: TestType
    test_count: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    coverage: float

class TestingCoordinator:
    """Comprehensive testing coordination and validation system."""

    def __init__(self, project_root: str = "."):
        """Initialize testing coordinator."""
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "test_reports"
        self.reports_dir.mkdir(exist_ok=True)

        # Ensure tests directory exists
        self.tests_dir.mkdir(exist_ok=True)

    def run_comprehensive_test_suite(self) -> dict[str, TestSuite]:
        """Run comprehensive test suite across all test types."""
        print("🧪 Running comprehensive test suite...")

        test_suites = {}

        # Run unit tests
        print("\n🔬 Running unit tests...")
        unit_results = self._run_unit_tests()
        test_suites['unit'] = unit_results

        # Run integration tests
        print("\n🔗 Running integration tests...")
        integration_results = self._run_integration_tests()
        test_suites['integration'] = integration_results

        # Run functional tests
        print("\n⚙️ Running functional tests...")
        functional_results = self._run_functional_tests()
        test_suites['functional'] = functional_results

        # Run performance tests
        print("\n⚡ Running performance tests...")
        performance_results = self._run_performance_tests()
        test_suites['performance'] = performance_results

        # Run security tests
        print("\n🔒 Running security tests...")
        security_results = self._run_security_tests()
        test_suites['security'] = security_results

        # Run regression tests
        print("\n🔄 Running regression tests...")
        regression_results = self._run_regression_tests()
        test_suites['regression'] = regression_results

        # Generate comprehensive test report
        self._generate_test_report(test_suites)

        return test_suites

    def _run_unit_tests(self) -> TestSuite:
        """Run unit tests."""
        start_time = time.time()

        try:
            # Run pytest for unit tests
            result = subprocess.run([
                'python', '-m', 'pytest',
                'tests/unit/',
                '--cov=src',
                '--cov-report=json',
                '--cov-report=term-missing',
                '--junitxml=test_reports/unit_tests.xml',
                '-v'
            ], capture_output=True, text=True, cwd=self.project_root)

            duration = time.time() - start_time

            # Parse results
            passed, failed, skipped, errors = self._parse_pytest_output(result.stdout)
            coverage = self._extract_coverage_from_output(result.stdout)

            return TestSuite(
                name="Unit Tests",
                test_type=TestType.UNIT,
                test_count=passed + failed + skipped + errors,
                passed=passed,
                failed=failed,
                skipped=skipped,
                errors=errors,
                duration=duration,
                coverage=coverage
            )

        except Exception as e:
            print(f"⚠️ Error running unit tests: {e}")
            return TestSuite(
                name="Unit Tests",
                test_type=TestType.UNIT,
                test_count=0,
                passed=0,
                failed=1,
                skipped=0,
                errors=0,
                duration=time.time() - start_time,
                coverage=0.0
            )

    def _run_integration_tests(self) -> TestSuite:
        """Run integration tests."""
        start_time = time.time()

        try:
            # Run pytest for integration tests
            result = subprocess.run([
                'python', '-m', 'pytest',
                'tests/integration/',
                '--junitxml=test_reports/integration_tests.xml',
                '-v'
            ], capture_output=True, text=True, cwd=self.project_root)

            duration = time.time() - start_time

            # Parse results
            passed, failed, skipped, errors = self._parse_pytest_output(result.stdout)

            return TestSuite(
                name="Integration Tests",
                test_type=TestType.INTEGRATION,
                test_count=passed + failed + skipped + errors,
                passed=passed,
                failed=failed,
                skipped=skipped,
                errors=errors,
                duration=duration,
                coverage=0.0  # Integration tests don't typically measure coverage
            )

        except Exception as e:
            print(f"⚠️ Error running integration tests: {e}")
            return TestSuite(
                name="Integration Tests",
                test_type=TestType.INTEGRATION,
                test_count=0,
                passed=0,
                failed=1,
                skipped=0,
                errors=0,
                duration=time.time() - start_time,
                coverage=0.0
            )

    def _run_functional_tests(self) -> TestSuite:
        """Run functional tests."""
        start_time = time.time()

        try:
            # Run pytest for functional tests
            result = subprocess.run([
                'python', '-m', 'pytest',
                'tests/functional/',
                '--junitxml=test_reports/functional_tests.xml',
                '-v'
            ], capture_output=True, text=True, cwd=self.project_root)

            duration = time.time() - start_time

            # Parse results
            passed, failed, skipped, errors = self._parse_pytest_output(result.stdout)

            return TestSuite(
                name="Functional Tests",
                test_type=TestType.FUNCTIONAL,
                test_count=passed + failed + skipped + errors,
                passed=passed,
                failed=failed,
                skipped=skipped,
                errors=errors,
                duration=duration,
                coverage=0.0
            )

        except Exception as e:
            print(f"⚠️ Error running functional tests: {e}")
            return TestSuite(
                name="Functional Tests",
                test_type=TestType.FUNCTIONAL,
                test_count=0,
                passed=0,
                failed=1,
                skipped=0,
                errors=0,
                duration=time.time() - start_time,
                coverage=0.0
            )

    def _run_performance_tests(self) -> TestSuite:
        """Run performance tests."""
        start_time = time.time()

        try:
            # Run performance tests
            result = subprocess.run([
                'python', '-m', 'pytest',
                'tests/performance/',
                '--junitxml=test_reports/performance_tests.xml',
                '-v'
            ], capture_output=True, text=True, cwd=self.project_root)

            duration = time.time() - start_time

            # Parse results
            passed, failed, skipped, errors = self._parse_pytest_output(result.stdout)

            return TestSuite(
                name="Performance Tests",
                test_type=TestType.PERFORMANCE,
                test_count=passed + failed + skipped + errors,
                passed=passed,
                failed=failed,
                skipped=skipped,
                errors=errors,
                duration=duration,
                coverage=0.0
            )

        except Exception as e:
            print(f"⚠️ Error running performance tests: {e}")
            return TestSuite(
                name="Performance Tests",
                test_type=TestType.PERFORMANCE,
                test_count=0,
                passed=0,
                failed=1,
                skipped=0,
                errors=0,
                duration=time.time() - start_time,
                coverage=0.0
            )

    def _run_security_tests(self) -> TestSuite:
        """Run security tests."""
        start_time = time.time()

        try:
            # Run security tests using bandit
            result = subprocess.run([
                'python', '-m', 'bandit',
                '-r', 'src/',
                '-f', 'json',
                '-o', 'test_reports/security_tests.json'
            ], capture_output=True, text=True, cwd=self.project_root)

            duration = time.time() - start_time

            # Parse bandit results
            security_issues = 0
            if result.stdout:
                try:
                    security_data = json.loads(result.stdout)
                    security_issues = len(security_data.get('results', []))
                except json.JSONDecodeError:
                    pass

            # Consider security issues as test failures
            passed = 0 if security_issues > 0 else 1
            failed = security_issues

            return TestSuite(
                name="Security Tests",
                test_type=TestType.SECURITY,
                test_count=1,
                passed=passed,
                failed=failed,
                skipped=0,
                errors=0,
                duration=duration,
                coverage=0.0
            )

        except Exception as e:
            print(f"⚠️ Error running security tests: {e}")
            return TestSuite(
                name="Security Tests",
                test_type=TestType.SECURITY,
                test_count=0,
                passed=0,
                failed=1,
                skipped=0,
                errors=0,
                duration=time.time() - start_time,
                coverage=0.0
            )

    def _run_regression_tests(self) -> TestSuite:
        """Run regression tests."""
        start_time = time.time()

        try:
            # Run regression tests
            result = subprocess.run([
                'python', '-m', 'pytest',
                'tests/regression/',
                '--junitxml=test_reports/regression_tests.xml',
                '-v'
            ], capture_output=True, text=True, cwd=self.project_root)

            duration = time.time() - start_time

            # Parse results
            passed, failed, skipped, errors = self._parse_pytest_output(result.stdout)

            return TestSuite(
                name="Regression Tests",
                test_type=TestType.REGRESSION,
                test_count=passed + failed + skipped + errors,
                passed=passed,
                failed=failed,
                skipped=skipped,
                errors=errors,
                duration=duration,
                coverage=0.0
            )

        except Exception as e:
            print(f"⚠️ Error running regression tests: {e}")
            return TestSuite(
                name="Regression Tests",
                test_type=TestType.REGRESSION,
                test_count=0,
                passed=0,
                failed=1,
                skipped=0,
                errors=0,
                duration=time.time() - start_time,
                coverage=0.0
            )

    def _parse_pytest_output(self, output: str) -> tuple[int, int, int, int]:
        """Parse pytest output to extract test counts."""
        passed = 0
        failed = 0
        skipped = 0
        errors = 0

        lines = output.split('\n')
        for line in lines:
            if 'passed' in line and 'failed' in line:
                # Extract numbers from summary line
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'passed':
                        try:
                            passed = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
                    elif part == 'failed':
                        try:
                            failed = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
                    elif part == 'skipped':
                        try:
                            skipped = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
                    elif part == 'error' and 'error' in part:
                        try:
                            errors = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass

        return passed, failed, skipped, errors

    def _extract_coverage_from_output(self, output: str) -> float:
        """Extract coverage percentage from pytest output."""
        lines = output.split('\n')
        for line in lines:
            if 'TOTAL' in line and '%' in line:
                try:
                    # Extract percentage from line like "TOTAL 85%"
                    parts = line.split()
                    for part in parts:
                        if '%' in part:
                            return float(part.replace('%', ''))
                except (ValueError, IndexError):
                    pass
        return 0.0

    def _generate_test_report(self, test_suites: dict[str, TestSuite]) -> None:
        """Generate comprehensive test report."""
        print("📊 Generating test report...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"test_report_{timestamp}.json"

        # Calculate overall metrics
        total_tests = sum(suite.test_count for suite in test_suites.values())
        total_passed = sum(suite.passed for suite in test_suites.values())
        total_failed = sum(suite.failed for suite in test_suites.values())
        total_skipped = sum(suite.skipped for suite in test_suites.values())
        total_errors = sum(suite.errors for suite in test_suites.values())
        total_duration = sum(suite.duration for suite in test_suites.values())

        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        report_data = {
            'timestamp': timestamp,
            'overall_metrics': {
                'total_tests': total_tests,
                'passed': total_passed,
                'failed': total_failed,
                'skipped': total_skipped,
                'errors': total_errors,
                'success_rate': success_rate,
                'total_duration': total_duration
            },
            'test_suites': {
                name: {
                    'name': suite.name,
                    'test_type': suite.test_type.value,
                    'test_count': suite.test_count,
                    'passed': suite.passed,
                    'failed': suite.failed,
                    'skipped': suite.skipped,
                    'errors': suite.errors,
                    'duration': suite.duration,
                    'coverage': suite.coverage
                }
                for name, suite in test_suites.items()
            },
            'recommendations': self._generate_test_recommendations(test_suites)
        }

        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"📊 Test report generated: {report_file}")

    def _generate_test_recommendations(self, test_suites: dict[str, TestSuite]) -> list[str]:
        """Generate test improvement recommendations."""
        recommendations = []

        for name, suite in test_suites.items():
            if suite.test_count == 0:
                recommendations.append(f"Create {name} - no tests found")
            elif suite.failed > 0:
                recommendations.append(f"Fix {suite.failed} failing tests in {name}")
            elif suite.passed < 5:
                recommendations.append(f"Increase test coverage in {name} - only {suite.passed} tests")

        return recommendations

def main():
    """Main execution function."""
    print("🧪 Agent-4 Testing Coordinator - Phase 2 Implementation")
    print("=" * 60)

    coordinator = TestingCoordinator()
    test_suites = coordinator.run_comprehensive_test_suite()

    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 30)

    total_tests = sum(suite.test_count for suite in test_suites.values())
    total_passed = sum(suite.passed for suite in test_suites.values())
    total_failed = sum(suite.failed for suite in test_suites.values())

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A")

    for name, suite in test_suites.items():
        print(f"\n{suite.name}:")
        print(f"  Tests: {suite.test_count}")
        print(f"  Passed: {suite.passed}")
        print(f"  Failed: {suite.failed}")
        print(f"  Duration: {suite.duration:.2f}s")
        if suite.coverage > 0:
            print(f"  Coverage: {suite.coverage:.1f}%")

    print("\n✅ Testing Coordinator Implementation Complete!")
    print("📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory")

if __name__ == "__main__":
    main()
