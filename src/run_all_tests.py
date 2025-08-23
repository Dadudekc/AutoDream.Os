#!/usr/bin/env python3
"""
Comprehensive Test Runner - Agent Cellphone V2
==============================================

Runs all test suites to validate the V2 systems and provide
comprehensive coverage analysis.

This script executes:
1. Advanced Features (Phase 1) - Already tested
2. Cursor Response Capture - Already tested
3. Autonomous Development System - NEW TESTS
4. FSM-Cursor Integration - NEW TESTS
5. Core Infrastructure Systems - NEW TESTS

Focus: Improving test coverage from 7% to target 25%+ overall coverage.
"""

import unittest
import sys
import time
import subprocess
from pathlib import Path


def run_test_file(test_file: str, description: str) -> dict:
    """Run a specific test file and return results"""
    print(f"\n🧪 RUNNING: {description}")
    print("=" * 60)

    try:
        # Run the test file
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        # Parse results
        if result.returncode == 0:
            status = "✅ PASSED"
            # Count tests from output
            lines = result.stdout.split("\n")
            tests_run = 0
            failures = 0
            errors = 0

            for line in lines:
                if "Tests run:" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        tests_run = int(parts[1].strip())
                elif "Failures:" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        failures = int(parts[1].strip())
                elif "Errors:" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        errors = int(parts[1].strip())

            return {
                "status": status,
                "tests_run": tests_run,
                "failures": failures,
                "errors": errors,
                "output": result.stdout,
                "error_output": result.stderr,
            }
        else:
            status = "❌ FAILED"
            return {
                "status": status,
                "tests_run": 0,
                "failures": 0,
                "errors": 0,
                "output": result.stdout,
                "error_output": result.stderr,
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "⏰ TIMEOUT",
            "tests_run": 0,
            "failures": 0,
            "errors": 0,
            "output": "Test execution timed out after 5 minutes",
            "error_output": "",
        }
    except Exception as e:
        return {
            "status": "💥 ERROR",
            "tests_run": 0,
            "failures": 0,
            "errors": 0,
            "output": f"Test execution error: {str(e)}",
            "error_output": "",
        }


def run_coverage_analysis() -> dict:
    """Run coverage analysis on the entire project"""
    print("\n📊 RUNNING COVERAGE ANALYSIS")
    print("=" * 60)

    try:
        # Run pytest with coverage
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-fail-under=0",
                "test_*.py",
                "tests/",
            ],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )

        # Parse coverage output
        coverage_lines = result.stdout.split("\n")
        coverage_info = {}

        for line in coverage_lines:
            if "TOTAL" in line and "coverage:" in line:
                # Extract coverage percentage
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "coverage:":
                        if i + 1 < len(parts):
                            coverage_percentage = parts[i + 1].replace("%", "")
                            try:
                                coverage_info["overall_coverage"] = float(
                                    coverage_percentage
                                )
                            except ValueError:
                                coverage_info["overall_coverage"] = 0.0
                        break

        return {
            "success": result.returncode == 0,
            "coverage": coverage_info.get("overall_coverage", 0.0),
            "output": result.stdout,
            "error_output": result.stderr,
        }

    except Exception as e:
        return {
            "success": False,
            "coverage": 0.0,
            "output": f"Coverage analysis error: {str(e)}",
            "error_output": "",
        }


def print_test_results(test_name: str, results: dict):
    """Print formatted test results"""
    print(f"\n📋 {test_name} RESULTS:")
    print(f"   Status: {results['status']}")
    print(f"   Tests Run: {results['tests_run']}")
    print(f"   Failures: {results['failures']}")
    print(f"   Errors: {results['errors']}")

    if results["failures"] > 0 or results["errors"] > 0:
        print(f"   Error Output: {results['error_output'][:200]}...")


def print_coverage_summary(coverage_results: dict):
    """Print coverage summary"""
    print(f"\n📊 COVERAGE SUMMARY:")
    print(f"   Overall Coverage: {coverage_results['coverage']:.1f}%")

    if coverage_results["success"]:
        print("   Coverage Analysis: ✅ Successful")
    else:
        print("   Coverage Analysis: ❌ Failed")
        print(f"   Error: {coverage_results['error_output'][:200]}...")


def main():
    """Main test execution function"""
    print("🚀 AGENT CELLPHONE V2 - COMPREHENSIVE TEST RUNNER")
    print("=" * 70)
    print("Executing all test suites to improve coverage from 7% to 25%+")
    print(f"Python Version: {sys.version}")
    print(f"Working Directory: {Path.cwd()}")

    start_time = time.time()

    # Test execution plan
    test_plan = [
        {
            "file": "test_advanced_features.py",
            "description": "Advanced Features (Phase 1) - Connection Pooling, Health Monitoring, Error Recovery, Performance Metrics",
        },
        {
            "file": "test_cursor_capture.py",
            "description": "Cursor Response Capture System - Database, CDP Bridge, Message Normalizer",
        },
        {
            "file": "test_autonomous_development.py",
            "description": "Autonomous Development System - Intelligent Prompt Generation, PyAutoGUI Integration",
        },
        {
            "file": "test_fsm_cursor_integration.py",
            "description": "FSM-Cursor Integration - Perpetual Motion Machine, State Machines, Agent Orchestration",
        },
        {
            "file": "test_core_infrastructure.py",
            "description": "Core Infrastructure - Health Monitor, Performance Profiler, Error Handler, Connection Pool Manager",
        },
    ]

    # Execute tests
    test_results = {}
    total_tests = 0
    total_failures = 0
    total_errors = 0

    for test_info in test_plan:
        test_file = test_info["file"]
        description = test_info["description"]

        # Check if test file exists
        if not Path(test_file).exists():
            print(f"\n⚠️  SKIPPING: {test_file} (file not found)")
            continue

        # Run test
        results = run_test_file(test_file, description)
        test_results[test_file] = results

        # Print results
        print_test_results(test_file, results)

        # Accumulate totals
        total_tests += results["tests_run"]
        total_failures += results["failures"]
        total_errors += results["errors"]

    # Run coverage analysis
    print("\n" + "=" * 70)
    coverage_results = run_coverage_analysis()
    print_coverage_summary(coverage_results)

    # Calculate execution time
    execution_time = time.time() - start_time

    # Print final summary
    print("\n" + "=" * 70)
    print("📊 FINAL TEST EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Total Tests Executed: {total_tests}")
    print(f"Total Failures: {total_failures}")
    print(f"Total Errors: {total_errors}")
    print(f"Execution Time: {execution_time:.2f} seconds")

    # Coverage improvement analysis
    if coverage_results["coverage"] > 0:
        print(f"\n📈 COVERAGE IMPROVEMENT ANALYSIS:")
        print(f"   Previous Coverage: 7.0%")
        print(f"   Current Coverage: {coverage_results['coverage']:.1f}%")

        improvement = coverage_results["coverage"] - 7.0
        if improvement > 0:
            print(f"   Improvement: +{improvement:.1f} percentage points")

            if coverage_results["coverage"] >= 25.0:
                print("   🎉 TARGET ACHIEVED: 25%+ coverage reached!")
            else:
                remaining = 25.0 - coverage_results["coverage"]
                print(
                    f"   🎯 Progress: {remaining:.1f} percentage points remaining to reach 25% target"
                )
        else:
            print(f"   ⚠️  No improvement detected")

    # Test status summary
    print(f"\n🧪 TEST STATUS SUMMARY:")
    passed_tests = sum(1 for r in test_results.values() if "PASSED" in r["status"])
    failed_tests = len(test_results) - passed_tests

    print(f"   Test Suites Passed: {passed_tests}")
    print(f"   Test Suites Failed: {failed_tests}")

    if failed_tests == 0:
        print("   🎉 ALL TEST SUITES PASSED!")
    else:
        print(f"   ⚠️  {failed_tests} test suite(s) had issues")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if coverage_results["coverage"] < 25.0:
        print("   1. Review failed tests and fix issues")
        print("   2. Add more test cases to improve coverage")
        print("   3. Focus on critical path testing")
    else:
        print("   1. Excellent progress! Maintain test quality")
        print("   2. Consider adding integration tests")
        print("   3. Set next coverage target to 50%")

    print(f"\n🚀 Test execution completed in {execution_time:.2f} seconds")

    # Return success/failure
    return total_failures == 0 and total_errors == 0


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test execution interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error during test execution: {e}")
        exit(1)
