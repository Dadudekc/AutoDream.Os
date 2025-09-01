#!/usr/bin/env python3
"""
CLI Interface for Gaming Test Runner
==================================

Command-line interface for the gaming test runner system.

Author: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

import argparse
import asyncio
import sys
from typing import Dict, Any

from .test_runner_core import GamingTestRunnerCore


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Gaming Test Runner - Comprehensive testing system for gaming and entertainment functionality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a single test
  python -m src.gaming.test_runner_cli --test session_creation
  
  # Run a test suite
  python -m src.gaming.test_runner_cli --suite unit_tests
  
  # Run all tests
  python -m src.gaming.test_runner_cli --all
  
  # Export results
  python -m src.gaming.test_runner_cli --export results.json
  
  # Show test results
  python -m src.gaming.test_runner_cli --results
  
  # List available tests
  python -m src.gaming.test_runner_cli --list-tests
        """
    )
    
    # Test execution options
    parser.add_argument("--test", "-t", help="Run a specific test by ID")
    parser.add_argument("--suite", "-s", help="Run a test suite by ID")
    parser.add_argument("--all", action="store_true", help="Run all available tests")
    
    # Output options
    parser.add_argument("--results", action="store_true", help="Show test results")
    parser.add_argument("--export", "-e", help="Export results to JSON file")
    parser.add_argument("--list-tests", action="store_true", help="List available tests")
    parser.add_argument("--list-suites", action="store_true", help="List available test suites")
    
    # Configuration options
    parser.add_argument("--config", "-c", help="Configuration file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    return parser


async def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize test runner
    config = {}
    if args.config:
        # Load configuration from file
        pass
    
    test_runner = GamingTestRunnerCore(config)
    
    # Handle utility commands first
    if args.list_tests:
        print("📋 AVAILABLE TESTS:")
        print("=" * 40)
        default_tests = [
            "session_creation",
            "performance_monitoring", 
            "alert_handling",
            "fps_test",
            "memory_test",
            "cpu_test",
            "stress_test",
            "api_integration",
            "database_integration",
            "network_integration"
        ]
        for test_id in default_tests:
            print(f"• {test_id}")
        print()
        return
    
    if args.list_suites:
        print("📋 AVAILABLE TEST SUITES:")
        print("=" * 40)
        for suite_id, suite in test_runner.test_suites.items():
            print(f"• {suite_id}: {suite.suite_name}")
            print(f"  Description: {suite.description}")
            print(f"  Tests: {', '.join(suite.tests)}")
            print()
        return
    
    if args.results:
        results = test_runner.get_test_results()
        print("📊 TEST RESULTS:")
        print("=" * 40)
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed_tests']}")
        print(f"Failed: {results['failed_tests']}")
        print(f"Errors: {results['error_tests']}")
        print(f"Success Rate: {results['success_rate']:.1f}%")
        print()
        
        if results['results']:
            print("📋 DETAILED RESULTS:")
            for result in results['results']:
                status_icon = "✅" if result['status'] == 'passed' else "❌" if result['status'] == 'failed' else "⚠️"
                print(f"{status_icon} {result['test_name']} ({result['test_id']})")
                print(f"   Status: {result['status']}")
                print(f"   Duration: {result['duration']:.2f}s")
                if result['error_message']:
                    print(f"   Error: {result['error_message']}")
                print()
        return
    
    # Handle test execution
    if args.test:
        print(f"🧪 RUNNING TEST: {args.test}")
        print("=" * 40)
        result = await test_runner.run_test(args.test)
        status_icon = "✅" if result.status.value == 'passed' else "❌" if result.status.value == 'failed' else "⚠️"
        print(f"{status_icon} {result.test_name} - {result.status.value}")
        print(f"Duration: {result.duration:.2f}s")
        if result.error_message:
            print(f"Error: {result.error_message}")
        print()
        return
    
    if args.suite:
        print(f"🧪 RUNNING TEST SUITE: {args.suite}")
        print("=" * 40)
        try:
            results = await test_runner.run_test_suite(args.suite)
            passed = len([r for r in results if r.status.value == 'passed'])
            total = len(results)
            print(f"✅ Suite completed: {passed}/{total} tests passed")
            print()
        except ValueError as e:
            print(f"❌ Error: {e}")
            return
    
    if args.all:
        print("🧪 RUNNING ALL TESTS")
        print("=" * 40)
        all_tests = [
            "session_creation",
            "performance_monitoring",
            "alert_handling", 
            "fps_test",
            "memory_test",
            "cpu_test",
            "stress_test",
            "api_integration",
            "database_integration",
            "network_integration"
        ]
        
        for test_id in all_tests:
            print(f"Running {test_id}...")
            result = await test_runner.run_test(test_id)
            status_icon = "✅" if result.status.value == 'passed' else "❌" if result.status.value == 'failed' else "⚠️"
            print(f"{status_icon} {result.test_name} - {result.status.value}")
        
        # Show summary
        results = test_runner.get_test_results()
        print()
        print("📊 FINAL SUMMARY:")
        print(f"Total Tests: {results['total_tests']}")
        print(f"Passed: {results['passed_tests']}")
        print(f"Failed: {results['failed_tests']}")
        print(f"Success Rate: {results['success_rate']:.1f}%")
        print()
        return
    
    # Handle export
    if args.export:
        print(f"📤 EXPORTING RESULTS TO: {args.export}")
        success = test_runner.export_test_results(args.export)
        if success:
            print("✅ Results exported successfully")
        else:
            print("❌ Failed to export results")
        return
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    print("❌ No action specified. Use --help for usage information.")


if __name__ == "__main__":
    asyncio.run(main())
