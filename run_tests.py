#!/usr/bin/env python3
"""
Test Runner - Comprehensive Test Suite Runner
=============================================

Comprehensive test runner for the Agent Cellphone V2 project.
Provides full test coverage reporting and analysis.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import sys

from test_runner_core import TestRunner


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Run comprehensive test suite")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration", "messaging", "discord", "coordinates"],
        default="all",
        help="Type of tests to run",
    )
    parser.add_argument("--no-coverage", action="store_true", help="Disable coverage reporting")
    parser.add_argument("--quiet", action="store_true", help="Run tests quietly")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--quality-gates", action="store_true", help="Run quality gates validation")

    args = parser.parse_args()

    print("🚀 Agent Cellphone V2 - Comprehensive Test Suite")
    print("=" * 60)
    print(f"📋 Test Type: {args.type}")
    print(f"📊 Coverage: {'Disabled' if args.no_coverage else 'Enabled'}")
    print(f"🔊 Verbose: {'Disabled' if args.quiet else 'Enabled'}")
    print(f"⚡ Parallel: {'Enabled' if args.parallel else 'Disabled'}")
    print("=" * 60)

    runner = TestRunner()

    # Run tests
    success = runner.run_tests(
        test_type=args.type,
        coverage=not args.no_coverage,
        verbose=not args.quiet,
        parallel=args.parallel,
    )

    if not success:
        print("❌ Test suite failed!")
        sys.exit(1)

    # Run quality gates if requested
    if args.quality_gates:
        quality_success = runner.run_quality_gates()
        if not quality_success:
            print("❌ Quality gates failed!")
            sys.exit(1)

    # Run coverage report if coverage was enabled
    if not args.no_coverage:
        coverage_success = runner.run_coverage_report()
        if not coverage_success:
            print("⚠️ Coverage report failed, but tests passed")

    print("\n🎉 Test suite completed successfully!")
    print("📊 Check htmlcov/index.html for detailed coverage report")


if __name__ == "__main__":
    main()