#!/usr/bin/env python3
"""
TDD Test Runner - Autonomous Development System
==============================================

Comprehensive test runner for autonomous development system.
Runs all TDD tests and provides detailed reporting.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import unittest
import sys
import os
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.autonomous_development.tests import (
    TestDevelopmentTask,
    TestTaskEnums,
    TestDevelopmentCommunication,
    TestAgentCoordinator,
    TestAgentWorkflow,
    TestTaskRegistry,
    TestWorkflowEngine,
    TestWorkflowMonitor,
    TestMessagingIntegration
)


class TDDTestRunner:
    """Comprehensive TDD test runner for autonomous development system"""
    
    def __init__(self):
        self.test_suite = unittest.TestSuite()
        self.test_results = None
        self.start_time = None
        self.end_time = None
        
    def build_test_suite(self):
        """Build comprehensive test suite"""
        print("🔧 Building TDD test suite...")
        
        # Core model tests
        self.test_suite.addTest(unittest.makeSuite(TestTaskEnums))
        self.test_suite.addTest(unittest.makeSuite(TestDevelopmentTask))
        
        # Communication tests
        self.test_suite.addTest(unittest.makeSuite(TestDevelopmentCommunication))
        
        # Agent coordination tests
        self.test_suite.addTest(unittest.makeSuite(TestAgentCoordinator))
        self.test_suite.addTest(unittest.makeSuite(TestAgentWorkflow))
        
        # Task management tests
        self.test_suite.addTest(unittest.makeSuite(TestTaskRegistry))
        
        # Workflow tests
        self.test_suite.addTest(unittest.makeSuite(TestWorkflowEngine))
        self.test_suite.addTest(unittest.makeSuite(TestWorkflowMonitor))
        
        # Messaging integration tests
        self.test_suite.addTest(unittest.makeSuite(TestMessagingIntegration))
        
        print(f"✅ Test suite built with {self.test_suite.countTestCases()} test cases")
    
    def run_tests(self, verbosity=2):
        """Run the complete test suite"""
        print("🚀 Starting TDD test execution...")
        print("=" * 60)
        
        self.start_time = time.time()
        
        # Create test runner
        runner = unittest.TextTestRunner(
            verbosity=verbosity,
            stream=sys.stdout,
            descriptions=True,
            failfast=False
        )
        
        # Run tests
        self.test_results = runner.run(self.test_suite)
        
        self.end_time = time.time()
        
        return self.test_results
    
    def generate_report(self):
        """Generate comprehensive test report"""
        if not self.test_results:
            print("❌ No test results available")
            return
        
        print("\n" + "=" * 60)
        print("📊 TDD TEST EXECUTION REPORT")
        print("=" * 60)
        
        # Test execution summary
        total_tests = self.test_results.testsRun
        failed_tests = len(self.test_results.failures)
        error_tests = len(self.test_results.errors)
        skipped_tests = len(getattr(self.test_results, 'skipped', []))
        successful_tests = total_tests - failed_tests - error_tests - skipped_tests
        
        # Execution time
        execution_time = self.end_time - self.start_time
        
        print(f"⏱️  Execution Time: {execution_time:.2f} seconds")
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Errors: {error_tests}")
        print(f"⏭️  Skipped: {skipped_tests}")
        
        # Success rate
        if total_tests > 0:
            success_rate = (successful_tests / total_tests) * 100
            print(f"🎯 Success Rate: {success_rate:.1f}%")
        
        # Detailed failure report
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS ({failed_tests}):")
            print("-" * 40)
            for test, traceback in self.test_results.failures:
                print(f"🔴 {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        # Detailed error report
        if error_tests > 0:
            print(f"\n⚠️  TEST ERRORS ({error_tests}):")
            print("-" * 40)
            for test, traceback in self.test_results.errors:
                print(f"🟡 {test}: {traceback.split('Exception:')[-1].strip()}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if failed_tests > 0:
            print("   • Review failed test assertions and fix implementation")
        if error_tests > 0:
            print("   • Check for import errors and missing dependencies")
        if success_rate >= 90:
            print("   • Excellent test coverage! Consider adding edge case tests")
        elif success_rate >= 80:
            print("   • Good test coverage. Focus on fixing failures first")
        else:
            print("   • Test coverage needs improvement. Prioritize fixing critical failures")
    
    def run_specific_test_category(self, category):
        """Run tests for a specific category"""
        category_tests = {
            'core': [TestTaskEnums, TestDevelopmentTask],
            'communication': [TestDevelopmentCommunication],
            'agents': [TestAgentCoordinator, TestAgentWorkflow],
            'tasks': [TestTaskRegistry],
            'workflow': [TestWorkflowEngine, TestWorkflowMonitor],
            'messaging': [TestMessagingIntegration]
        }
        
        if category not in category_tests:
            print(f"❌ Unknown test category: {category}")
            print(f"Available categories: {', '.join(category_tests.keys())}")
            return
        
        print(f"🎯 Running tests for category: {category}")
        
        # Create focused test suite
        focused_suite = unittest.TestSuite()
        for test_class in category_tests[category]:
            focused_suite.addTest(unittest.makeSuite(test_class))
        
        # Run focused tests
        runner = unittest.TextTestRunner(verbosity=2)
        results = runner.run(focused_suite)
        
        return results
    
    def run_smoke_tests(self):
        """Run quick smoke tests for basic functionality"""
        print("💨 Running smoke tests...")
        
        smoke_tests = [
            TestTaskEnums,
            TestDevelopmentTask
        ]
        
        smoke_suite = unittest.TestSuite()
        for test_class in smoke_tests:
            smoke_suite.addTest(unittest.makeSuite(test_class))
        
        runner = unittest.TextTestRunner(verbosity=1)
        results = runner.run(smoke_suite)
        
        return results


def main():
    """Main entry point for TDD test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TDD Test Runner for Autonomous Development System")
    parser.add_argument("--category", "-c", choices=['core', 'communication', 'agents', 'tasks', 'workflow', 'messaging'],
                       help="Run tests for specific category")
    parser.add_argument("--smoke", "-s", action="store_true", help="Run smoke tests only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--list", "-l", action="store_true", help="List available test categories")
    
    args = parser.parse_args()
    
    runner = TDDTestRunner()
    
    if args.list:
        print("📋 Available test categories:")
        print("   • core - Core data models and enums")
        print("   • communication - Development communication system")
        print("   • agents - Agent coordination and workflow")
        print("   • tasks - Task management and registry")
        print("   • workflow - Workflow engine and monitoring")
        print("   • messaging - Messaging system integration")
        return
    
    try:
        if args.smoke:
            results = runner.run_smoke_tests()
        elif args.category:
            results = runner.run_specific_test_category(args.category)
        else:
            # Run full test suite
            runner.build_test_suite()
            results = runner.run_tests(verbosity=2 if args.verbose else 1)
            runner.generate_report()
        
        # Exit with appropriate code
        if results and (results.failures or results.errors):
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
