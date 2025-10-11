#!/usr/bin/env python3
"""
Test Runner - Comprehensive Test Suite Runner
=============================================

Comprehensive test runner for the Agent Cellphone V2 project.
Provides full test coverage reporting and analysis.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_tests(test_type="all", coverage=True, verbose=True, parallel=False):
    """Run tests with specified options."""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test directory
    cmd.append("tests/")
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add coverage
    if coverage:
        cmd.extend([
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml"
        ])
    
    # Add parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add specific test type
    if test_type != "all":
        cmd.extend(["-k", test_type])
    
    # Add markers
    if test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "unit":
        cmd.extend(["-m", "unit"])
    
    # Add test discovery
    cmd.extend([
        "--tb=short",
        "--strict-markers",
        "--disable-warnings"
    ])
    
    print(f"🚀 Running tests: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Tests failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_coverage_report():
    """Run coverage report."""
    print("📊 Generating coverage report...")
    
    try:
        result = subprocess.run([
            "python", "-m", "coverage", "report", "--show-missing"
        ], check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Coverage report failed: {e}")
        return False

def run_quality_gates():
    """Run quality gates validation."""
    print("🔍 Running quality gates validation...")
    
    try:
        result = subprocess.run([
            "python", "quality_gates.py"
        ], check=True, capture_output=False)
        print("✅ Quality gates passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Quality gates failed: {e}")
        return False
    except FileNotFoundError:
        print("⚠️ Quality gates script not found, skipping...")
        return True

def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Run comprehensive test suite")
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "messaging", "discord", "coordinates"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--no-coverage", 
        action="store_true",
        help="Disable coverage reporting"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Run tests quietly"
    )
    parser.add_argument(
        "--parallel", 
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--quality-gates", 
        action="store_true",
        help="Run quality gates validation"
    )
    
    args = parser.parse_args()
    
    print("🚀 Agent Cellphone V2 - Comprehensive Test Suite")
    print("=" * 60)
    print(f"📋 Test Type: {args.type}")
    print(f"📊 Coverage: {'Disabled' if args.no_coverage else 'Enabled'}")
    print(f"🔊 Verbose: {'Disabled' if args.quiet else 'Enabled'}")
    print(f"⚡ Parallel: {'Enabled' if args.parallel else 'Disabled'}")
    print("=" * 60)
    
    # Run tests
    success = run_tests(
        test_type=args.type,
        coverage=not args.no_coverage,
        verbose=not args.quiet,
        parallel=args.parallel
    )
    
    if not success:
        print("❌ Test suite failed!")
        sys.exit(1)
    
    # Run quality gates if requested
    if args.quality_gates:
        quality_success = run_quality_gates()
        if not quality_success:
            print("❌ Quality gates failed!")
            sys.exit(1)
    
    # Run coverage report if coverage was enabled
    if not args.no_coverage:
        coverage_success = run_coverage_report()
        if not coverage_success:
            print("⚠️ Coverage report failed, but tests passed")
    
    print("\n🎉 Test suite completed successfully!")
    print("📊 Check htmlcov/index.html for detailed coverage report")

if __name__ == "__main__":
    main()