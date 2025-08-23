#!/usr/bin/env python3
"""
Testing CLI - V2 Testing Framework Command Line Interface
========================================================

Provides command-line interface for the testing framework with comprehensive smoke tests.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import asyncio
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import our components
try:
    from .testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from .testing_core import CrossSystemCommunicationTest, ServiceIntegrationTest, DatabaseIntegrationTest
    from .testing_orchestration import IntegrationTestSuite, IntegrationTestRunner, TestOrchestrator
except ImportError:
    from testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from testing_core import CrossSystemCommunicationTest, ServiceIntegrationTest, DatabaseIntegrationTest
    from testing_orchestration import IntegrationTestSuite, IntegrationTestRunner, TestOrchestrator


class TestingFrameworkCLI:
    """Command-line interface for the testing framework."""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.orchestrator = TestOrchestrator()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser."""
        parser = argparse.ArgumentParser(
            description="V2 Testing Framework - Command Line Interface",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python testing_cli.py --smoke                    # Run smoke tests
  python testing_cli.py --demo                     # Run demo test suite
  python testing_cli.py --suite communication     # Run communication test suite
  python testing_cli.py --list                     # List available test suites
  python testing_cli.py --create-suite demo       # Create a demo test suite
            """
        )
        
        # Main action group
        action_group = parser.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            "--smoke", 
            action="store_true", 
            help="Run smoke tests for all components"
        )
        action_group.add_argument(
            "--demo", 
            action="store_true", 
            help="Run a demo test suite"
        )
        action_group.add_argument(
            "--suite", 
            type=str, 
            metavar="SUITE_NAME",
            help="Run a specific test suite by name"
        )
        action_group.add_argument(
            "--list", 
            action="store_true", 
            help="List available test suites"
        )
        action_group.add_argument(
            "--create-suite", 
            type=str, 
            metavar="SUITE_NAME",
            help="Create a demo test suite with the specified name"
        )
        
        # Configuration options
        parser.add_argument(
            "--parallel", 
            action="store_true", 
            help="Enable parallel test execution"
        )
        parser.add_argument(
            "--timeout", 
            type=int, 
            default=300,
            help="Test timeout in seconds (default: 300)"
        )
        parser.add_argument(
            "--retry-failed", 
            action="store_true", 
            help="Retry failed tests"
        )
        parser.add_argument(
            "--max-retries", 
            type=int, 
            default=2,
            help="Maximum retry attempts for failed tests (default: 2)"
        )
        parser.add_argument(
            "--verbose", "-v", 
            action="store_true", 
            help="Enable verbose output"
        )
        parser.add_argument(
            "--output", 
            type=str, 
            choices=["text", "json", "xml"],
            default="text",
            help="Output format for test results (default: text)"
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI with the given arguments."""
        try:
            parsed_args = self.parser.parse_args(args)
            
            # Configure orchestrator based on arguments
            self._configure_orchestrator(parsed_args)
            
            # Execute the requested action
            if parsed_args.smoke:
                return self._run_smoke_tests(parsed_args)
            elif parsed_args.demo:
                return self._run_demo_suite(parsed_args)
            elif parsed_args.suite:
                return self._run_specific_suite(parsed_args)
            elif parsed_args.list:
                return self._list_test_suites(parsed_args)
            elif parsed_args.create_suite:
                return self._create_demo_suite(parsed_args)
            else:
                self.parser.print_help()
                return 1
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return 130
        except Exception as e:
            print(f"❌ Error: {e}")
            if parsed_args and parsed_args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def _configure_orchestrator(self, args: argparse.Namespace) -> None:
        """Configure the test orchestrator based on command line arguments."""
        config = {
            "auto_retry_failed": args.retry_failed,
            "generate_reports": True,
            "notify_on_completion": False,
            "cleanup_after_execution": True
        }
        self.orchestrator.configure(config)
        
        # Configure global runner settings
        runner_config = {
            "parallel_suites": args.parallel,
            "max_parallel_suites": 3 if args.parallel else 1,
            "stop_on_failure": False,
            "generate_report": True,
            "report_format": args.output
        }
        self.orchestrator.runner.set_global_config(runner_config)
    
    def _run_smoke_tests(self, args: argparse.Namespace) -> int:
        """Run smoke tests for all components."""
        print("🧪 **V2 TESTING FRAMEWORK SMOKE TESTS**")
        print("=" * 50)
        
        results = []
        
        # Test testing types
        print("\n🔍 Testing Types Module...")
        try:
            from .testing_types import run_smoke_test
            result = run_smoke_test()
            results.append(("Testing Types", result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status}: Testing Types Module")
        except ImportError:
            try:
                from testing_types import run_smoke_test
                result = run_smoke_test()
                results.append(("Testing Types", result))
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}: Testing Types Module")
            except Exception as e:
                results.append(("Testing Types", False))
                print(f"   ❌ ERROR: Testing Types Module - {e}")
        except Exception as e:
            results.append(("Testing Types", False))
            print(f"   ❌ ERROR: Testing Types Module - {e}")
        
        # Test testing core
        print("\n🔍 Testing Core Module...")
        try:
            from .testing_core import run_smoke_test
            result = run_smoke_test()
            results.append(("Testing Core", result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status}: Testing Core Module")
        except ImportError:
            try:
                from testing_core import run_smoke_test
                result = run_smoke_test()
                results.append(("Testing Core", result))
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}: Testing Core Module")
            except Exception as e:
                results.append(("Testing Core", False))
                print(f"   ❌ ERROR: Testing Core Module - {e}")
        except Exception as e:
            results.append(("Testing Core", False))
            print(f"   ❌ ERROR: Testing Core Module - {e}")
        
        # Test testing orchestration
        print("\n🔍 Testing Orchestration Module...")
        try:
            from .testing_orchestration import run_smoke_test
            result = run_smoke_test()
            results.append(("Testing Orchestration", result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status}: Testing Orchestration Module")
        except ImportError:
            try:
                from testing_orchestration import run_smoke_test
                result = run_smoke_test()
                results.append(("Testing Orchestration", result))
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}: Testing Orchestration Module")
            except Exception as e:
                results.append(("Testing Orchestration", False))
                print(f"   ❌ ERROR: Testing Orchestration Module - {e}")
        except Exception as e:
            results.append(("Testing Orchestration", False))
            print(f"   ❌ ERROR: Testing Orchestration Module - {e}")
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 **SMOKE TEST SUMMARY**")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for module_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {module_name}")
        
        print(f"\n🎯 Results: {passed}/{total} modules passed")
        
        if passed == total:
            print("🎉 **ALL SMOKE TESTS PASSED! Testing framework is ready!**")
            return 0
        else:
            print("⚠️  Some smoke tests failed - review issues above")
            return 1
    
    def _run_demo_suite(self, args: argparse.Namespace) -> int:
        """Run a demo test suite."""
        print("🚀 **DEMO TEST SUITE EXECUTION**")
        print("=" * 40)
        
        # Create demo test suite
        suite = self._create_demo_suite_internal("Demo Suite")
        
        # Run the suite
        print(f"Running demo test suite: {suite.name}")
        print(f"Tests included: {len(suite.tests)}")
        
        try:
            # Run asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            summary = loop.run_until_complete(
                self.orchestrator.run_test_suite(suite)
            )
            
            loop.close()
            
            # Display results
            self._display_suite_results(summary, args)
            
            return 0 if summary.get("overall_success_rate", 0) >= 80 else 1
            
        except Exception as e:
            print(f"❌ Error running demo suite: {e}")
            return 1
    
    def _run_specific_suite(self, args: argparse.Namespace) -> int:
        """Run a specific test suite by name."""
        suite_name = args.suite
        print(f"🚀 **RUNNING TEST SUITE: {suite_name.upper()}**")
        print("=" * 50)
        
        # Create the requested suite
        suite = self._create_suite_by_name(suite_name)
        if not suite:
            print(f"❌ Unknown test suite: {suite_name}")
            print("Available suites: communication, service, database, comprehensive")
            return 1
        
        # Run the suite
        print(f"Running test suite: {suite.name}")
        print(f"Tests included: {len(suite.tests)}")
        
        try:
            # Run asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            summary = loop.run_until_complete(
                self.orchestrator.run_test_suite(suite)
            )
            
            loop.close()
            
            # Display results
            self._display_suite_results(summary, args)
            
            return 0 if summary.get("overall_success_rate", 0) >= 80 else 1
            
        except Exception as e:
            print(f"❌ Error running suite {suite_name}: {e}")
            return 1
    
    def _list_test_suites(self, args: argparse.Namespace) -> int:
        """List available test suites."""
        print("📋 **AVAILABLE TEST SUITES**")
        print("=" * 30)
        
        suites = [
            ("communication", "Cross-system communication tests"),
            ("service", "Service integration tests"),
            ("database", "Database integration tests"),
            ("comprehensive", "Comprehensive integration test suite")
        ]
        
        for suite_name, description in suites:
            print(f"• {suite_name:<15} - {description}")
        
        print(f"\nUse --suite SUITE_NAME to run a specific suite")
        print(f"Use --demo to run the demo suite")
        print(f"Use --create-suite NAME to create a custom suite")
        
        return 0
    
    def _create_demo_suite(self, args: argparse.Namespace) -> int:
        """Create a demo test suite with the specified name."""
        suite_name = args.create_suite
        print(f"🏗️  **CREATING DEMO TEST SUITE: {suite_name.upper()}**")
        print("=" * 50)
        
        # Create the suite
        suite = self._create_demo_suite_internal(suite_name)
        
        print(f"✅ Created test suite: {suite.name}")
        print(f"📝 Description: {suite.description}")
        print(f"🧪 Tests included: {len(suite.tests)}")
        
        # List the tests
        print("\n📋 **Tests in Suite:**")
        for i, test in enumerate(suite.tests, 1):
            print(f"  {i}. {test.test_name} ({test.test_type.value}) - Priority: {test.priority.value}")
        
        print(f"\n🚀 Run with: --suite {suite_name}")
        print(f"🎯 Or run demo: --demo")
        
        return 0
    
    def _create_demo_suite_internal(self, name: str) -> IntegrationTestSuite:
        """Create a demo test suite internally."""
        suite = IntegrationTestSuite(name, f"Demo test suite: {name}")
        
        # Add various test types
        suite.add_test(CrossSystemCommunicationTest("Demo Communication Test"))
        suite.add_test(ServiceIntegrationTest("Demo Service Test"))
        suite.add_test(DatabaseIntegrationTest("Demo Database Test"))
        
        # Configure suite
        suite.parallel_execution = False
        suite.timeout = 300.0
        suite.retry_failed = True
        suite.max_retries = 2
        
        return suite
    
    def _create_suite_by_name(self, suite_name: str) -> Optional[IntegrationTestSuite]:
        """Create a test suite by name."""
        if suite_name.lower() == "communication":
            suite = IntegrationTestSuite("Communication Tests", "Cross-system communication test suite")
            suite.add_test(CrossSystemCommunicationTest("System A to B Communication"))
            suite.add_test(CrossSystemCommunicationTest("System B to C Communication"))
            suite.add_test(CrossSystemCommunicationTest("System C to A Communication"))
            
        elif suite_name.lower() == "service":
            suite = IntegrationTestSuite("Service Tests", "Service integration test suite")
            suite.add_test(ServiceIntegrationTest("Auth Service Integration"))
            suite.add_test(ServiceIntegrationTest("User Service Integration"))
            suite.add_test(ServiceIntegrationTest("Data Service Integration"))
            
        elif suite_name.lower() == "database":
            suite = IntegrationTestSuite("Database Tests", "Database integration test suite")
            suite.add_test(DatabaseIntegrationTest("PostgreSQL Integration"))
            suite.add_test(DatabaseIntegrationTest("Redis Integration"))
            suite.add_test(DatabaseIntegrationTest("MongoDB Integration"))
            
        elif suite_name.lower() == "comprehensive":
            suite = IntegrationTestSuite("Comprehensive Tests", "Comprehensive integration test suite")
            suite.add_test(CrossSystemCommunicationTest("Comprehensive Communication Test"))
            suite.add_test(ServiceIntegrationTest("Comprehensive Service Test"))
            suite.add_test(DatabaseIntegrationTest("Comprehensive Database Test"))
            
        else:
            return None
        
        # Configure suite
        suite.parallel_execution = False
        suite.timeout = 300.0
        suite.retry_failed = True
        suite.max_retries = 2
        
        return suite
    
    def _display_suite_results(self, summary: Dict[str, Any], args: argparse.Namespace) -> None:
        """Display test suite results."""
        print("\n" + "=" * 50)
        print("📊 **TEST SUITE RESULTS**")
        print("=" * 50)
        
        if "error" in summary:
            print(f"❌ Suite execution failed: {summary['error']}")
            return
        
        # Display overall summary
        print(f"🎯 Overall Success Rate: {summary.get('overall_success_rate', 0):.1f}%")
        print(f"📦 Total Suites: {summary.get('total_suites', 0)}")
        print(f"🧪 Total Tests: {summary.get('total_tests', 0)}")
        print(f"✅ Passed: {summary.get('passed', 0)}")
        print(f"❌ Failed: {summary.get('failed', 0)}")
        print(f"⏭️  Skipped: {summary.get('skipped', 0)}")
        print(f"🚨 Errors: {summary.get('error', 0)}")
        print(f"⏰ Timeouts: {summary.get('timeout', 0)}")
        
        # Display suite details if available
        if "suite_summaries" in summary:
            print("\n📋 **Suite Details:**")
            for suite_summary in summary["suite_summaries"]:
                print(f"  • {suite_summary['name']}: {suite_summary['success_rate']:.1f}% success")
        
        # Display reports if available
        if "reports" in summary:
            print("\n📄 **Detailed Reports:**")
            for suite_name, report in summary["reports"].items():
                print(f"  • {suite_name}: {report['success_rate']:.1f}% success, {report['total_tests']} tests")


def run_smoke_test() -> bool:
    """Run comprehensive smoke test for the testing framework CLI."""
    try:
        print("🧪 **TESTING FRAMEWORK CLI SMOKE TEST**")
        print("=" * 50)
        
        # Test CLI creation
        cli = TestingFrameworkCLI()
        assert cli.parser is not None
        assert cli.orchestrator is not None
        print("✅ CLI creation successful")
        
        # Test parser creation
        parser = cli._create_parser()
        assert parser is not None
        print("✅ Parser creation successful")
        
        # Test demo suite creation
        suite = cli._create_demo_suite_internal("Smoke Test Suite")
        assert suite.name == "Smoke Test Suite"
        assert len(suite.tests) == 3
        print("✅ Demo suite creation successful")
        
        # Test suite by name creation
        comm_suite = cli._create_suite_by_name("communication")
        assert comm_suite is not None
        assert comm_suite.name == "Communication Tests"
        assert len(comm_suite.tests) == 3
        print("✅ Suite by name creation successful")
        
        # Test unknown suite
        unknown_suite = cli._create_suite_by_name("unknown")
        assert unknown_suite is None
        print("✅ Unknown suite handling successful")
        
        print("🎉 All CLI smoke tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ CLI smoke test failed: {e}")
        return False


def main():
    """Main entry point for the testing framework CLI."""
    cli = TestingFrameworkCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
