#!/usr/bin/env python3
"""
Modular Test Runner - Comprehensive Test Execution
=================================================

Test runner for the refactored modular test suite.
Provides organized test execution with detailed reporting.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


class ModularTestRunner:
    """Runner for modular test suite."""

    def __init__(self):
        self.test_categories = {
            "messaging": {
                "path": "messaging/",
                "description": "Messaging Service Tests",
                "markers": ["messaging", "unit", "integration", "performance"],
            },
            "discord": {
                "path": "discord/",
                "description": "Discord Bot Integration Tests",
                "markers": ["discord", "unit", "integration"],
            },
            "database": {
                "path": "database/",
                "description": "Database Tests",
                "markers": [
                    "database",
                    "migration",
                    "schema",
                    "unit",
                    "integration",
                    "performance",
                ],
            },
            "utils": {"path": "utils/", "description": "Test Utilities", "markers": ["unit"]},
        }

        self.test_types = {
            "unit": "Unit tests that run in isolation",
            "integration": "Integration tests that require external dependencies",
            "performance": "Performance tests with timing requirements",
            "slow": "Tests that take a long time to run",
        }

    def run_tests(
        self,
        category: str = None,
        test_type: str = None,
        verbose: bool = False,
        coverage: bool = False,
    ) -> dict[str, Any]:
        """Run tests with specified parameters."""
        start_time = time.time()

        # Build pytest command
        cmd = ["python", "-m", "pytest"]

        if category and category in self.test_categories:
            cmd.append(self.test_categories[category]["path"])
        elif category == "all":
            cmd.append("tests/")
        else:
            cmd.append("tests/")

        # Add markers
        if test_type and test_type in self.test_types:
            cmd.extend(["-m", test_type])

        # Add options
        if verbose:
            cmd.append("-v")

        if coverage:
            cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])

        cmd.extend(["--tb=short", "--strict-markers"])

        print(f"Running command: {' '.join(cmd)}")

        # Run tests
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            end_time = time.time()
            duration = end_time - start_time

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration": duration,
                "command": " ".join(cmd),
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "Test execution timed out after 5 minutes",
                "duration": 300,
                "command": " ".join(cmd),
            }
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "duration": time.time() - start_time,
                "command": " ".join(cmd),
            }

    def run_category_tests(self, category: str, verbose: bool = False) -> dict[str, Any]:
        """Run tests for a specific category."""
        if category not in self.test_categories:
            return {"success": False, "error": f"Unknown category: {category}"}

        category_info = self.test_categories[category]
        print(f"\n{'='*60}")
        print(f"Running {category_info['description']}")
        print(f"Path: {category_info['path']}")
        print(f"Markers: {', '.join(category_info['markers'])}")
        print(f"{'='*60}")

        return self.run_tests(category=category, verbose=verbose)

    def run_type_tests(self, test_type: str, verbose: bool = False) -> dict[str, Any]:
        """Run tests of a specific type."""
        if test_type not in self.test_types:
            return {"success": False, "error": f"Unknown test type: {test_type}"}

        print(f"\n{'='*60}")
        print(f"Running {test_type.title()} Tests")
        print(f"Description: {self.test_types[test_type]}")
        print(f"{'='*60}")

        return self.run_tests(test_type=test_type, verbose=verbose)

    def run_all_tests(self, verbose: bool = False, coverage: bool = False) -> dict[str, Any]:
        """Run all tests."""
        print(f"\n{'='*60}")
        print("Running All Modular Tests")
        print(f"{'='*60}")

        return self.run_tests(category="all", verbose=verbose, coverage=coverage)

    def validate_test_structure(self) -> dict[str, Any]:
        """Validate the modular test structure."""
        validation_results = {"success": True, "errors": [], "warnings": [], "categories": {}}

        for category, info in self.test_categories.items():
            category_path = Path(info["path"])

            if not category_path.exists():
                validation_results["errors"].append(f"Category path not found: {info['path']}")
                validation_results["success"] = False
                continue

            # Check for test files
            test_files = list(category_path.glob("test_*.py"))
            if not test_files:
                validation_results["warnings"].append(f"No test files found in {info['path']}")

            validation_results["categories"][category] = {
                "path_exists": category_path.exists(),
                "test_files": len(test_files),
                "test_file_names": [f.name for f in test_files],
            }

        # Check for utils
        utils_path = Path("utils/")
        if utils_path.exists():
            utils_files = list(utils_path.glob("*.py"))
            validation_results["utils"] = {
                "path_exists": True,
                "files": len(utils_files),
                "file_names": [f.name for f in utils_files],
            }
        else:
            validation_results["errors"].append("Utils directory not found: utils/")
            validation_results["success"] = False

        return validation_results

    def generate_test_report(self, results: dict[str, Any]) -> str:
        """Generate a test report."""
        report = []
        report.append("=" * 80)
        report.append("MODULAR TEST SUITE REPORT")
        report.append("=" * 80)
        report.append("")

        # Test execution results
        if "success" in results:
            report.append(f"Test Execution: {'✅ PASSED' if results['success'] else '❌ FAILED'}")
            report.append(f"Return Code: {results.get('returncode', 'N/A')}")
            report.append(f"Duration: {results.get('duration', 0):.2f} seconds")
            report.append(f"Command: {results.get('command', 'N/A')}")
            report.append("")

        # Validation results
        if "validation" in results:
            validation = results["validation"]
            report.append("STRUCTURE VALIDATION:")
            report.append(f"Overall: {'✅ VALID' if validation['success'] else '❌ INVALID'}")
            report.append("")

            if validation["errors"]:
                report.append("ERRORS:")
                for error in validation["errors"]:
                    report.append(f"  ❌ {error}")
                report.append("")

            if validation["warnings"]:
                report.append("WARNINGS:")
                for warning in validation["warnings"]:
                    report.append(f"  ⚠️  {warning}")
                report.append("")

            report.append("CATEGORIES:")
            for category, info in validation["categories"].items():
                status = "✅" if info["path_exists"] else "❌"
                report.append(f"  {status} {category}: {info['test_files']} test files")
                if info["test_file_names"]:
                    for test_file in info["test_file_names"]:
                        report.append(f"    - {test_file}")
            report.append("")

        # Test output
        if "stdout" in results and results["stdout"]:
            report.append("TEST OUTPUT:")
            report.append("-" * 40)
            report.append(results["stdout"])
            report.append("-" * 40)
            report.append("")

        # Test errors
        if "stderr" in results and results["stderr"]:
            report.append("TEST ERRORS:")
            report.append("-" * 40)
            report.append(results["stderr"])
            report.append("-" * 40)
            report.append("")

        return "\n".join(report)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Modular Test Runner")
    parser.add_argument(
        "--category",
        choices=["messaging", "discord", "database", "utils", "all"],
        help="Test category to run",
    )
    parser.add_argument(
        "--type", choices=["unit", "integration", "performance", "slow"], help="Test type to run"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Run with coverage")
    parser.add_argument("--validate", action="store_true", help="Validate test structure only")
    parser.add_argument("--report", "-r", action="store_true", help="Generate detailed report")

    args = parser.parse_args()

    runner = ModularTestRunner()

    if args.validate:
        # Validate structure only
        validation_results = runner.validate_test_structure()
        print("Test Structure Validation:")
        print(json.dumps(validation_results, indent=2))
        return 0 if validation_results["success"] else 1

    # Run tests
    if args.category:
        if args.category == "all":
            results = runner.run_all_tests(verbose=args.verbose, coverage=args.coverage)
        else:
            results = runner.run_category_tests(args.category, verbose=args.verbose)
    elif args.type:
        results = runner.run_type_tests(args.type, verbose=args.verbose)
    else:
        results = runner.run_all_tests(verbose=args.verbose, coverage=args.coverage)

    # Add validation results
    validation_results = runner.validate_test_structure()
    results["validation"] = validation_results

    # Generate and print report
    if args.report:
        report = runner.generate_test_report(results)
        print(report)

        # Save report to file
        report_file = f"test_report_{int(time.time())}.txt"
        with open(report_file, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {report_file}")
    else:
        # Simple output
        if results["success"]:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            if results["stderr"]:
                print(f"Errors: {results['stderr']}")

    return 0 if results["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
