#!/usr/bin/env python3
"""
Test-Driven Development: Comprehensive Test Runner
Agent_Cellphone_V2_Repository Testing Infrastructure

This script provides:
- Test discovery and execution
- Coverage reporting
- Performance testing
- Quality assurance validation
- Test result analysis
"""

import argparse
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import os

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


class TDDTestRunner:
    """Comprehensive test runner for TDD integration project"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_dir = project_root / "tests"
        self.src_dir = project_root / "src"
        self.results_dir = project_root / "test_results"
        self.coverage_dir = project_root / "htmlcov"

        # Ensure results directory exists
        self.results_dir.mkdir(exist_ok=True)

    def discover_tests(self, test_type: Optional[str] = None) -> List[Path]:
        """Discover test files based on type"""
        if not self.test_dir.exists():
            print(f"❌ Test directory not found: {self.test_dir}")
            return []

        test_files = []

        if test_type:
            # Specific test type
            type_dir = self.test_dir / test_type
            if type_dir.exists():
                test_files.extend(type_dir.rglob("test_*.py"))
        else:
            # All test files
            test_files.extend(self.test_dir.rglob("test_*.py"))

        return sorted(test_files)

    def run_tests(
        self,
        test_paths: List[Path],
        coverage: bool = True,
        parallel: bool = False,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """Run tests with specified options"""
        if not test_paths:
            print("⚠️  No test files found to run")
            return {"success": False, "message": "No test files found"}

        # Build pytest command
        cmd = ["python", "-m", "pytest"]

        # Add test paths
        for test_path in test_paths:
            cmd.append(str(test_path))

        # Add options
        if verbose:
            cmd.append("-v")

        if coverage:
            cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term-missing"])

        if parallel:
            cmd.extend(["-n", "auto"])

        # Add additional pytest options
        cmd.extend(["--tb=short", "--strict-markers", "--disable-warnings"])

        print(f"🚀 Running tests with command: {' '.join(cmd)}")
        print(f"📁 Test files: {len(test_paths)}")

        # Execute tests
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )
            duration = time.time() - start_time

            # Parse results
            test_results = self._parse_test_results(result, duration)

            # Save results
            self._save_test_results(test_results)

            return test_results

        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return {
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time,
            }

    def _parse_test_results(
        self, result: subprocess.CompletedProcess, duration: float
    ) -> Dict[str, Any]:
        """Parse test execution results"""
        output = result.stdout
        error_output = result.stderr

        # Basic result info
        test_results = {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "duration": duration,
            "stdout": output,
            "stderr": error_output,
        }

        # Parse test statistics
        test_results.update(self._extract_test_stats(output))

        # Parse coverage information
        if "--cov=src" in " ".join(result.args):
            test_results["coverage"] = self._extract_coverage_info(output)

        return test_results

    def _extract_test_stats(self, output: str) -> Dict[str, Any]:
        """Extract test statistics from output"""
        stats = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "warnings": 0,
        }

        lines = output.split("\n")
        for line in lines:
            if "collected" in line and "items" in line:
                # Extract total tests
                try:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "collected":
                            stats["total_tests"] = int(parts[i + 1])
                            break
                except (ValueError, IndexError):
                    pass

            elif "passed" in line and "failed" in line:
                # Extract pass/fail counts
                try:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            stats["passed"] = int(parts[i - 1])
                        elif part == "failed":
                            stats["failed"] = int(parts[i - 1])
                        elif part == "error" and i > 0:
                            stats["errors"] = int(parts[i - 1])
                except (ValueError, IndexError):
                    pass

        return stats

    def _extract_coverage_info(self, output: str) -> Dict[str, Any]:
        """Extract coverage information from output"""
        coverage = {
            "total_coverage": 0.0,
            "missing_lines": 0,
            "covered_files": 0,
            "total_files": 0,
        }

        lines = output.split("\n")
        for line in lines:
            if "TOTAL" in line and "%" in line:
                try:
                    # Extract total coverage percentage
                    parts = line.split()
                    for part in parts:
                        if part.endswith("%"):
                            coverage["total_coverage"] = float(part.rstrip("%"))
                            break
                except (ValueError, IndexError):
                    pass

        return coverage

    def _save_test_results(self, results: Dict[str, Any]) -> None:
        """Save test results to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"test_results_{timestamp}.json"

        # Convert non-serializable objects
        serializable_results = {}
        for key, value in results.items():
            if key in ["stdout", "stderr"]:
                # Truncate long outputs
                serializable_results[key] = (
                    str(value)[:1000] + "..." if len(str(value)) > 1000 else str(value)
                )
            else:
                serializable_results[key] = value

        with open(results_file, "w") as f:
            json.dump(serializable_results, f, indent=2, default=str)

        print(f"💾 Test results saved to: {results_file}")

    def run_smoke_tests(self) -> Dict[str, Any]:
        """Run smoke tests for quick validation"""
        print("🔥 Running smoke tests...")
        smoke_tests = self.discover_tests("smoke")
        return self.run_tests(smoke_tests, coverage=False, verbose=True)

    def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests"""
        print("🧪 Running unit tests...")
        unit_tests = self.discover_tests("unit")
        return self.run_tests(unit_tests, coverage=True, verbose=True)

    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests"""
        print("🔗 Running integration tests...")
        integration_tests = self.discover_tests("integration")
        return self.run_tests(integration_tests, coverage=True, verbose=True)

    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests"""
        print("⚡ Running performance tests...")
        performance_tests = [
            f for f in self.discover_tests() if "performance" in f.name.lower()
        ]
        return self.run_tests(performance_tests, coverage=False, verbose=True)

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests with full coverage"""
        print("🚀 Running all tests...")
        all_tests = self.discover_tests()
        return self.run_tests(all_tests, coverage=True, parallel=True, verbose=True)

    def generate_test_report(self) -> None:
        """Generate comprehensive test report"""
        print("📊 Generating test report...")

        # Collect test statistics
        test_files = self.discover_tests()
        smoke_tests = self.discover_tests("smoke")
        unit_tests = self.discover_tests("unit")
        integration_tests = self.discover_tests("integration")

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project": "Agent_Cellphone_V2_Repository",
            "test_summary": {
                "total_test_files": len(test_files),
                "smoke_tests": len(smoke_tests),
                "unit_tests": len(unit_tests),
                "integration_tests": len(integration_tests),
            },
            "test_files": [str(f.relative_to(self.project_root)) for f in test_files],
            "recommendations": [],
        }

        # Generate recommendations
        if len(smoke_tests) < 5:
            report["recommendations"].append(
                "Consider adding more smoke tests for critical functionality"
            )

        if len(unit_tests) < len(test_files) * 0.3:
            report["recommendations"].append(
                "Increase unit test coverage for better code quality"
            )

        if not (self.project_root / "tests" / "performance").exists():
            report["recommendations"].append(
                "Consider adding performance testing directory"
            )

        # Save report
        report_file = self.results_dir / "test_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📋 Test report saved to: {report_file}")

        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST INFRASTRUCTURE SUMMARY")
        print("=" * 60)
        print(f"Total test files: {len(test_files)}")
        print(f"Smoke tests: {len(smoke_tests)}")
        print(f"Unit tests: {len(unit_tests)}")
        print(f"Integration tests: {len(integration_tests)}")
        print("=" * 60)

        if report["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")

    def validate_test_infrastructure(self) -> Dict[str, Any]:
        """Validate the test infrastructure setup"""
        print("🔍 Validating test infrastructure...")

        validation = {
            "pytest_available": False,
            "test_directory_exists": False,
            "conftest_exists": False,
            "test_utils_exists": False,
            "coverage_tools_available": False,
            "issues": [],
        }

        # Check pytest availability
        try:
            import pytest

            validation["pytest_available"] = True
        except ImportError:
            validation["issues"].append("pytest not available")

        # Check test directory structure
        if self.test_dir.exists():
            validation["test_directory_exists"] = True

            # Check for conftest.py
            if (self.test_dir / "conftest.py").exists():
                validation["conftest_exists"] = True
            else:
                validation["issues"].append("conftest.py not found in tests directory")

            # Check for test_utils.py
            if (self.test_dir / "test_utils.py").exists():
                validation["test_utils_exists"] = True
            else:
                validation["issues"].append(
                    "test_utils.py not found in tests directory"
                )
        else:
            validation["issues"].append("tests directory not found")

        # Check coverage tools
        try:
            import coverage

            validation["coverage_tools_available"] = True
        except ImportError:
            validation["issues"].append("coverage tools not available")

        # Print validation results
        print("\n" + "=" * 60)
        print("🔍 TEST INFRASTRUCTURE VALIDATION")
        print("=" * 60)

        for key, value in validation.items():
            if key != "issues":
                status = "✅" if value else "❌"
                print(f"{status} {key}: {value}")

        if validation["issues"]:
            print("\n⚠️  ISSUES FOUND:")
            for issue in validation["issues"]:
                print(f"  • {issue}")
        else:
            print("\n🎉 All validation checks passed!")

        print("=" * 60)

        return validation


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="TDD Integration Test Runner for Agent_Cellphone_V2_Repository"
    )

    parser.add_argument(
        "--test-type",
        choices=["smoke", "unit", "integration", "performance", "all"],
        default="all",
        help="Type of tests to run",
    )

    parser.add_argument(
        "--no-coverage", action="store_true", help="Disable coverage reporting"
    )

    parser.add_argument(
        "--no-parallel", action="store_true", help="Disable parallel test execution"
    )

    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")

    parser.add_argument(
        "--validate", action="store_true", help="Validate test infrastructure only"
    )

    parser.add_argument(
        "--report", action="store_true", help="Generate test report only"
    )

    args = parser.parse_args()

    # Initialize test runner
    project_root = Path(__file__).parent
    runner = TDDTestRunner(project_root)

    if args.validate:
        runner.validate_test_infrastructure()
        return

    if args.report:
        runner.generate_test_report()
        return

    # Run tests based on type
    if args.test_type == "smoke":
        results = runner.run_smoke_tests()
    elif args.test_type == "unit":
        results = runner.run_unit_tests()
    elif args.test_type == "integration":
        results = runner.run_integration_tests()
    elif args.test_type == "performance":
        results = runner.run_performance_tests()
    else:  # all
        results = runner.run_all_tests()

    # Print results summary
    if results.get("success"):
        print(f"\n✅ Tests completed successfully in {results.get('duration', 0):.2f}s")

        if "coverage" in results:
            coverage = results["coverage"]
            print(f"📊 Coverage: {coverage.get('total_coverage', 0):.1f}%")

        stats = results.get("total_tests", 0)
        if stats:
            print(f"🧪 Total tests: {stats}")
    else:
        print(f"\n❌ Tests failed: {results.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
