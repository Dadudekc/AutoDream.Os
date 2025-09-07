#!/usr/bin/env python3
"""
Master Smoke Test Runner - Agent Cellphone V2
=============================================

Unified test runner for all major feature smoke tests.
Executes comprehensive smoke tests across the entire system.

Author: Agent-2 (Architecture & Design)
License: MIT
"""

import pytest
import sys
import time
from pathlib import Path
from typing import List, Dict, Any
import argparse
import json


class SmokeTestRunner:
    """Master runner for smoke tests."""

    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None

    def discover_smoke_tests(self) -> List[str]:
        """Discover all smoke test files."""
        test_files = []

        # Core smoke test files
        smoke_tests = [
            "test_messaging_core_smoke.py",
            "test_messaging_cli_smoke.py",
            "test_vector_database_smoke.py",
            # Add more as they are created
        ]

        # Check if files exist
        tests_dir = Path(__file__).parent
        for test_file in smoke_tests:
            test_path = tests_dir / test_file
            if test_path.exists():
                test_files.append(str(test_path))

        return test_files

    def run_smoke_tests(self, test_files: List[str], verbose: bool = False) -> Dict[str, Any]:
        """Run all smoke tests and collect results."""
        self.start_time = time.time()

        print("🚀 Starting Agent Cellphone V2 Smoke Tests")
        print("=" * 50)

        all_results = {}

        for test_file in test_files:
            test_name = Path(test_file).stem
            print(f"\n📋 Running {test_name}...")

            # Run pytest on individual test file
            args = [test_file, "-v"] if verbose else [test_file]
            if not verbose:
                args.extend(["--tb=short", "-q"])

            result_code = pytest.main(args)

            # Store results
            all_results[test_name] = {
                "file": test_file,
                "passed": result_code == 0,
                "exit_code": result_code
            }

            status = "✅ PASSED" if result_code == 0 else "❌ FAILED"
            print(f"   Result: {status}")

        self.end_time = time.time()

        return all_results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive test report."""
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r["passed"])
        failed_tests = total_tests - passed_tests

        duration = self.end_time - self.start_time

        report = []
        report.append("📊 Agent Cellphone V2 Smoke Test Report")
        report.append("=" * 50)
        report.append(f"⏱️  Total Duration: {duration:.2f} seconds")
        report.append(f"📈 Tests Run: {total_tests}")
        report.append(f"✅ Tests Passed: {passed_tests}")
        report.append(f"❌ Tests Failed: {failed_tests}")
        report.append(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")
        report.append("")

        if failed_tests > 0:
            report.append("❌ Failed Tests:")
            for test_name, result in results.items():
                if not result["passed"]:
                    report.append(f"   • {test_name} (exit code: {result['exit_code']})")
            report.append("")

        report.append("📋 Test Details:")
        for test_name, result in results.items():
            status = "✅" if result["passed"] else "❌"
            report.append(f"   {status} {test_name}")

        # Overall status
        if failed_tests == 0:
            report.append("")
            report.append("🎉 ALL SMOKE TESTS PASSED!")
            report.append("   System is ready for production use.")
        else:
            report.append("")
            report.append("⚠️  SOME SMOKE TESTS FAILED!")
            report.append("   Please review failed tests before proceeding.")

        return "\n".join(report)

    def save_report(self, report: str, output_file: str = None):
        """Save test report to file."""
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"\n💾 Report saved to: {output_file}")

    def run_comprehensive_smoke_test(self, verbose: bool = False, output_file: str = None):
        """Run comprehensive smoke test suite."""
        # Discover test files
        test_files = self.discover_smoke_tests()

        if not test_files:
            print("❌ No smoke test files found!")
            return False

        print(f"🔍 Discovered {len(test_files)} smoke test files:")
        for test_file in test_files:
            print(f"   • {Path(test_file).name}")

        # Run tests
        results = self.run_smoke_tests(test_files, verbose)

        # Generate report
        report = self.generate_report(results)

        # Display report
        print("\n" + report)

        # Save report if requested
        if output_file:
            self.save_report(report, output_file)

        # Return overall success
        return all(result["passed"] for result in results.values())


def create_argument_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Agent Cellphone V2 Master Smoke Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_master_smoke_runner.py                # Run all smoke tests
  python test_master_smoke_runner.py -v             # Run with verbose output
  python test_master_smoke_runner.py -o report.txt  # Save report to file
  python test_master_smoke_runner.py --help         # Show this help
        """
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose test output"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Save test report to specified file"
    )

    parser.add_argument(
        "--list-tests",
        action="store_true",
        help="List available smoke tests without running them"
    )

    return parser


def main():
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()

    runner = SmokeTestRunner()

    if args.list_tests:
        # Just list tests
        test_files = runner.discover_smoke_tests()
        print("🔍 Available Smoke Tests:")
        print("=" * 30)
        for test_file in test_files:
            print(f"   • {Path(test_file).name}")
        return

    # Run comprehensive smoke tests
    success = runner.run_comprehensive_smoke_test(
        verbose=args.verbose,
        output_file=args.output
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
