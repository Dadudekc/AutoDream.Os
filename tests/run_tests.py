#!/usr/bin/env python3
"""
🧪 TESTING RUNNER - AGENT_CELLPHONE_V2
Foundation & Testing Specialist - TDD Integration Project

Main testing runner that provides comprehensive testing execution, reporting,
and V2 standards compliance validation for all components.
"""

import argparse
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add tests to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from conftest import TestConfig


class TestRunner:
    """Comprehensive test runner for Agent_Cellphone_V2."""

    def __init__(self, config: TestConfig):
        """Initialize test runner with configuration."""
        self.config = config
        self.results = {
            "start_time": None,
            "end_time": None,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
            "error_tests": 0,
            "components_tested": 0,
            "v2_compliance": True,
            "coverage": 0.0,
            "test_duration": 0.0,
        }

        # Test categories
        self.test_categories = {
            "smoke": "Smoke tests for basic functionality",
            "unit": "Unit tests for individual components",
            "integration": "Integration tests for component interaction",
            "v2_standards": "V2 coding standards compliance tests",
            "performance": "Performance and benchmarking tests",
            "security": "Security vulnerability tests",
        }

    def run_tests(
        self,
        categories: List[str] = None,
        coverage: bool = True,
        parallel: bool = False,
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """Run comprehensive test suite."""
        print("🧪 AGENT_CELLPHONE_V2 TESTING FRAMEWORK")
        print("=" * 50)
        print(f"Foundation & Testing Specialist - TDD Integration Project")
        print(f"Test Execution Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        self.results["start_time"] = datetime.now()
        start_time = time.time()

        # Determine test categories to run
        if categories is None:
            categories = list(self.test_categories.keys())

        print(f"📋 Test Categories: {', '.join(categories)}")
        print(f"🎯 Coverage Analysis: {'Enabled' if coverage else 'Disabled'}")
        print(f"⚡ Parallel Execution: {'Enabled' if parallel else 'Disabled'}")
        print(f"🔍 Verbose Output: {'Enabled' if verbose else 'Disabled'}")
        print()

        # Run tests by category
        for category in categories:
            if category in self.test_categories:
                print(f"🔬 Running {category.title()} Tests...")
                category_results = self._run_category_tests(
                    category, coverage, parallel, verbose
                )
                self._update_results(category_results)
                print(f"✅ {category.title()} Tests Completed")
                print()

        # Calculate final results
        self.results["end_time"] = datetime.now()
        self.results["test_duration"] = time.time() - start_time

        # Generate coverage report if enabled
        if coverage:
            self._generate_coverage_report()

        # Print final results
        self._print_final_results()

        return self.results

    def _run_category_tests(
        self, category: str, coverage: bool, parallel: bool, verbose: bool
    ) -> Dict[str, Any]:
        """Run tests for a specific category."""
        category_results = {
            "category": category,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
            "error_tests": 0,
        }

        # Build pytest command
        cmd = [sys.executable, "-m", "pytest"]

        # Add category-specific test path
        if category == "smoke":
            cmd.extend(["tests/smoke/", "-m", "smoke"])
        elif category == "unit":
            cmd.extend(["tests/unit/", "-m", "unit"])
        elif category == "integration":
            cmd.extend(["tests/integration/", "-m", "integration"])
        elif category == "v2_standards":
            cmd.extend(["tests/", "-m", "v2_standards"])
        elif category == "performance":
            cmd.extend(["tests/performance/", "-m", "performance"])
        elif category == "security":
            cmd.extend(["tests/security/", "-m", "security"])

        # Add pytest options
        if coverage:
            cmd.extend(["--cov=src", "--cov-report=term-missing"])

        if parallel:
            cmd.extend(["-n", "auto"])

        if verbose:
            cmd.extend(["-v"])

        # Add output options
        cmd.extend(
            [
                "--tb=short",
                "--strict-markers",
                "--disable-warnings",
                f"--html=test-results/{category}_report.html",
                f"--junitxml=test-results/{category}_junit.xml",
            ]
        )

        try:
            # Run tests
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # Parse results from output
            self._parse_pytest_output(result.stdout, category_results)

            # Handle return code
            if result.returncode == 0:
                print(f"  ✅ All {category} tests passed")
            elif result.returncode == 1:
                print(f"  ⚠️  Some {category} tests failed")
            elif result.returncode == 2:
                print(f"  ❌ {category} test execution error")
            elif result.returncode == 5:
                print(f"  ⏭️  No {category} tests found")

        except subprocess.TimeoutExpired:
            print(f"  ⏰ {category} tests timed out")
            category_results["error_tests"] += 1
        except Exception as e:
            print(f"  💥 {category} tests failed with error: {e}")
            category_results["error_tests"] += 1

        return category_results

    def _parse_pytest_output(self, output: str, results: Dict[str, Any]) -> None:
        """Parse pytest output to extract test results."""
        lines = output.split("\n")

        for line in lines:
            line = line.strip()

            # Count test results
            if "passed" in line and "failed" in line:
                # Parse summary line like "5 passed, 2 failed, 1 skipped"
                parts = line.split(",")
                for part in parts:
                    part = part.strip()
                    if "passed" in part:
                        results["passed_tests"] = int(part.split()[0])
                    elif "failed" in part:
                        results["failed_tests"] = int(part.split()[0])
                    elif "skipped" in part:
                        results["skipped_tests"] = int(part.split()[0])

                results["total_tests"] = (
                    results["passed_tests"]
                    + results["failed_tests"]
                    + results["skipped_tests"]
                )
                break

    def _update_results(self, category_results: Dict[str, Any]) -> None:
        """Update overall results with category results."""
        self.results["total_tests"] += category_results["total_tests"]
        self.results["passed_tests"] += category_results["passed_tests"]
        self.results["failed_tests"] += category_results["failed_tests"]
        self.results["skipped_tests"] += category_results["skipped_tests"]
        self.results["error_tests"] += category_results["error_tests"]
        self.results["components_tested"] += 1

        # Update V2 compliance status
        if category_results["failed_tests"] > 0 or category_results["error_tests"] > 0:
            self.results["v2_compliance"] = False

    def _generate_coverage_report(self) -> None:
        """Generate comprehensive coverage report."""
        print("📊 Generating Coverage Report...")

        try:
            # Run coverage report
            cmd = [sys.executable, "-m", "coverage", "report", "--show-missing"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                # Extract coverage percentage
                lines = result.stdout.split("\n")
                for line in lines:
                    if "TOTAL" in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            try:
                                coverage_str = parts[-1].replace("%", "")
                                self.results["coverage"] = float(coverage_str)
                                break
                            except ValueError:
                                pass

                print("  ✅ Coverage report generated")
            else:
                print("  ⚠️  Coverage report generation failed")

        except Exception as e:
            print(f"  💥 Coverage report error: {e}")

    def _print_final_results(self) -> None:
        """Print comprehensive test results summary."""
        print("=" * 50)
        print("📊 TEST EXECUTION SUMMARY")
        print("=" * 50)

        # Test execution results
        print(f"⏱️  Test Duration: {self.results['test_duration']:.2f} seconds")
        print(f"📅 Start Time: {self.results['start_time']}")
        print(f"📅 End Time: {self.results['end_time']}")
        print()

        # Test counts
        print(f"🧪 Total Tests: {self.results['total_tests']}")
        print(f"✅ Passed: {self.results['passed_tests']}")
        print(f"❌ Failed: {self.results['failed_tests']}")
        print(f"⏭️  Skipped: {self.results['skipped_tests']}")
        print(f"💥 Errors: {self.results['error_tests']}")
        print()

        # Coverage and compliance
        print(f"📊 Code Coverage: {self.results['coverage']:.1f}%")
        print(
            f"🎯 V2 Standards Compliance: {'✅ COMPLIANT' if self.results['v2_compliance'] else '❌ NON-COMPLIANT'}"
        )
        print()

        # Success rate
        if self.results["total_tests"] > 0:
            success_rate = (
                self.results["passed_tests"] / self.results["total_tests"]
            ) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")

            if success_rate >= 90:
                print("🏆 EXCELLENT - High test success rate!")
            elif success_rate >= 80:
                print("👍 GOOD - Solid test success rate")
            elif success_rate >= 70:
                print("⚠️  FAIR - Room for improvement")
            else:
                print("🚨 POOR - Significant issues detected")
        else:
            print("⚠️  No tests executed")

        print()

        # Recommendations
        if not self.results["v2_compliance"]:
            print("🔧 RECOMMENDATIONS:")
            print("  - Review failed tests and fix issues")
            print("  - Ensure all components meet V2 coding standards")
            print("  - Check CLI interfaces and smoke tests")
            print("  - Validate OOP design and single responsibility")

        if self.results["coverage"] < 80:
            print("📈 COVERAGE IMPROVEMENT:")
            print(f"  - Current coverage: {self.results['coverage']:.1f}%")
            print("  - Target coverage: 80%")
            print("  - Add tests for uncovered code paths")

        print("=" * 50)

    def run_v2_standards_audit(self) -> Dict[str, Any]:
        """Run comprehensive V2 coding standards audit."""
        print("🔍 V2 CODING STANDARDS AUDIT")
        print("=" * 40)

        audit_results = {
            "components_audited": 0,
            "loc_compliant": 0,
            "oop_compliant": 0,
            "srp_compliant": 0,
            "cli_compliant": 0,
            "smoke_tests_compliant": 0,
            "overall_compliance": 0.0,
        }

        # Audit each component category
        for category, description in self.config.COMPONENTS.items():
            category_dir = Path(f"src/{category}")
            if category_dir.exists():
                print(f"🔬 Auditing {category.title()} Components...")
                category_audit = self._audit_component_category(category_dir, category)
                self._update_audit_results(audit_results, category_audit)
                print(f"  ✅ {category.title()} audit completed")

        # Calculate overall compliance
        total_checks = audit_results["components_audited"] * 5  # 5 compliance areas
        if total_checks > 0:
            passed_checks = (
                audit_results["loc_compliant"]
                + audit_results["oop_compliant"]
                + audit_results["srp_compliant"]
                + audit_results["cli_compliant"]
                + audit_results["smoke_tests_compliant"]
            )
            audit_results["overall_compliance"] = (passed_checks / total_checks) * 100

        # Print audit summary
        self._print_audit_summary(audit_results)

        return audit_results

    def _audit_component_category(
        self, category_dir: Path, category: str
    ) -> Dict[str, Any]:
        """Audit a specific component category for V2 standards compliance."""
        audit_results = {
            "category": category,
            "components_checked": 0,
            "loc_compliant": 0,
            "oop_compliant": 0,
            "srp_compliant": 0,
            "cli_compliant": 0,
            "smoke_tests_compliant": 0,
        }

        # Check each Python file in category
        for py_file in category_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            audit_results["components_checked"] += 1

            # Check LOC compliance
            if self._check_loc_compliance(py_file, category):
                audit_results["loc_compliant"] += 1

            # Check OOP compliance
            if self._check_oop_compliance(py_file):
                audit_results["oop_compliant"] += 1

            # Check SRP compliance
            if self._check_srp_compliance(py_file):
                audit_results["srp_compliant"] += 1

            # Check CLI compliance
            if self._check_cli_compliance(py_file):
                audit_results["cli_compliant"] += 1

            # Check smoke tests compliance
            if self._check_smoke_tests_compliance(py_file):
                audit_results["smoke_tests_compliant"] += 1

        return audit_results

    def _check_loc_compliance(self, file_path: Path, category: str) -> bool:
        """Check if file meets LOC requirements."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                code_lines = [
                    line
                    for line in lines
                    if line.strip() and not line.strip().startswith("#")
                ]

                max_loc = self.config.MAX_LOC_CORE
                if category == "web":
                    max_loc = self.config.MAX_LOC_GUI

                return len(code_lines) <= max_loc
        except Exception:
            return False

    def _check_oop_compliance(self, file_path: Path) -> bool:
        """Check if file follows OOP design principles."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return "class " in content
        except Exception:
            return False

    def _check_srp_compliance(self, file_path: Path) -> bool:
        """Check if file follows single responsibility principle."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # Count different types of operations
                operations = {
                    "file_ops": content.count("open(") + content.count("Path("),
                    "network_ops": content.count("requests.")
                    + content.count("urllib."),
                    "db_ops": content.count("sqlite") + content.count("database"),
                    "gui_ops": content.count("tkinter") + content.count("PyQt"),
                    "cli_ops": content.count("argparse") + content.count("click"),
                }

                # Should have primary focus on one area
                active_ops = sum(1 for count in operations.values() if count > 0)
                return active_ops <= 2
        except Exception:
            return False

    def _check_cli_compliance(self, file_path: Path) -> bool:
        """Check if file has CLI interface."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return "argparse" in content and (
                    "def main(" in content or "if __name__" in content
                )
        except Exception:
            return False

    def _check_smoke_tests_compliance(self, file_path: Path) -> bool:
        """Check if file has smoke tests functionality."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return "--test" in content or "test" in content.lower()
        except Exception:
            return False

    def _update_audit_results(
        self, overall_results: Dict[str, Any], category_results: Dict[str, Any]
    ) -> None:
        """Update overall audit results with category results."""
        overall_results["components_audited"] += category_results["components_checked"]
        overall_results["loc_compliant"] += category_results["loc_compliant"]
        overall_results["oop_compliant"] += category_results["oop_compliant"]
        overall_results["srp_compliant"] += category_results["srp_compliant"]
        overall_results["cli_compliant"] += category_results["cli_compliant"]
        overall_results["smoke_tests_compliant"] += category_results[
            "smoke_tests_compliant"
        ]

    def _print_audit_summary(self, audit_results: Dict[str, Any]) -> None:
        """Print V2 standards audit summary."""
        print("\n📊 V2 STANDARDS AUDIT SUMMARY")
        print("=" * 40)

        print(f"🔍 Components Audited: {audit_results['components_audited']}")
        print(
            f"📏 LOC Compliance: {audit_results['loc_compliant']}/{audit_results['components_audited']}"
        )
        print(
            f"🏗️  OOP Design: {audit_results['oop_compliant']}/{audit_results['components_audited']}"
        )
        print(
            f"🎯 Single Responsibility: {audit_results['srp_compliant']}/{audit_results['components_audited']}"
        )
        print(
            f"🖥️  CLI Interface: {audit_results['cli_compliant']}/{audit_results['components_audited']}"
        )
        print(
            f"🧪 Smoke Tests: {audit_results['smoke_tests_compliant']}/{audit_results['components_audited']}"
        )
        print()

        print(f"📈 Overall Compliance: {audit_results['overall_compliance']:.1f}%")

        if audit_results["overall_compliance"] >= 90:
            print("🏆 EXCELLENT - High V2 standards compliance!")
        elif audit_results["overall_compliance"] >= 80:
            print("👍 GOOD - Solid V2 standards compliance")
        elif audit_results["overall_compliance"] >= 70:
            print("⚠️  FAIR - Some V2 standards issues")
        else:
            print("🚨 POOR - Significant V2 standards violations")

        print("=" * 40)


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(
        description="🧪 Agent_Cellphone_V2 Testing Framework - Foundation & Testing Specialist"
    )

    parser.add_argument(
        "--categories",
        "-c",
        nargs="+",
        choices=[
            "smoke",
            "unit",
            "integration",
            "v2_standards",
            "performance",
            "security",
        ],
        help="Test categories to run (default: all)",
    )

    parser.add_argument(
        "--no-coverage", "-nc", action="store_true", help="Disable coverage analysis"
    )

    parser.add_argument(
        "--parallel", "-p", action="store_true", help="Enable parallel test execution"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--audit-only",
        "-a",
        action="store_true",
        help="Run only V2 standards audit (no tests)",
    )

    args = parser.parse_args()

    # Initialize test runner
    config = TestConfig()
    runner = TestRunner(config)

    try:
        if args.audit_only:
            # Run only V2 standards audit
            runner.run_v2_standards_audit()
        else:
            # Run comprehensive test suite
            runner.run_tests(
                categories=args.categories,
                coverage=not args.no_coverage,
                parallel=args.parallel,
                verbose=args.verbose,
            )

            # Run V2 standards audit after tests
            print("\n" + "=" * 50)
            runner.run_v2_standards_audit()

        # Exit with appropriate code
        if (
            runner.results.get("failed_tests", 0) > 0
            or runner.results.get("error_tests", 0) > 0
        ):
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
