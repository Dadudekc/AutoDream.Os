"""
Testing Framework CLI
=====================

Command-line interface for the consolidated testing framework,
providing easy access to all testing functionality.
"""

import argparse
import sys
from typing import List, Optional
from pathlib import Path

from src.core.testing.testing_orchestrator import TestOrchestrator
from src.core.testing.testing_reporter import CoverageReporter, PerformanceReporter, HTMLReporter
from src.core.testing.testing_core import BaseTest, BaseIntegrationTest
from src.core.testing.testing_types import TestType, TestPriority, TestEnvironment


class TestingFrameworkCLI:
    """Command-line interface for the testing framework"""
    
    def __init__(self):
        self.orchestrator = TestOrchestrator()
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Consolidated Testing Framework CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run all tests
  python -m testing_cli run --all
  
  # Run specific test suite
  python -m testing_cli run --suite integration
  
  # Run tests by type
  python -m testing_cli run --type unit
  
  # Generate reports
  python -m testing_cli report --coverage --performance --html
  
  # Show system status
  python -m testing_cli status --detailed
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Run command
        run_parser = subparsers.add_parser('run', help='Run tests')
        run_parser.add_argument('--all', action='store_true', help='Run all registered tests')
        run_parser.add_argument('--suite', type=str, help='Run tests in specific suite')
        run_parser.add_argument('--type', type=str, choices=[t.value for t in TestType], help='Run tests of specific type')
        run_parser.add_argument('--priority', type=int, choices=[1, 2, 3, 4], help='Run tests of specific priority')
        run_parser.add_argument('--test-id', type=str, help='Run specific test by ID')
        run_parser.add_argument('--save-results', type=str, help='Save results to specified file')
        
        # Report command
        report_parser = subparsers.add_parser('report', help='Generate test reports')
        report_parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
        report_parser.add_argument('--performance', action='store_true', help='Generate performance report')
        report_parser.add_argument('--html', action='store_true', help='Generate HTML report')
        report_parser.add_argument('--output-dir', type=str, default='test_reports', help='Output directory for reports')
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show system status')
        status_parser.add_argument('--detailed', action='store_true', help='Show detailed status information')
        
        # Register command
        register_parser = subparsers.add_parser('register', help='Register tests')
        register_parser.add_argument('--test-file', type=str, help='Register tests from file')
        register_parser.add_argument('--test-dir', type=str, help='Register tests from directory')
        
        # Suite command
        suite_parser = subparsers.add_parser('suite', help='Manage test suites')
        suite_parser.add_argument('--list', action='store_true', help='List all test suites')
        suite_parser.add_argument('--create', type=str, help='Create new test suite')
        suite_parser.add_argument('--description', type=str, help='Suite description for creation')
        suite_parser.add_argument('--add-test', type=str, help='Add test to suite')
        suite_parser.add_argument('--suite-id', type=str, help='Target suite ID')
        
        # Results command
        results_parser = subparsers.add_parser('results', help='Manage test results')
        results_parser.add_argument('--list', action='store_true', help='List all test results')
        results_parser.add_argument('--export', type=str, choices=['json', 'csv'], help='Export results in specified format')
        results_parser.add_argument('--clear', action='store_true', help='Clear all test results')
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI with optional arguments"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not parsed_args.command:
                self.parser.print_help()
                return 0
            
            if parsed_args.command == 'run':
                return self._handle_run(parsed_args)
            elif parsed_args.command == 'report':
                return self._handle_report(parsed_args)
            elif parsed_args.command == 'status':
                return self._handle_status(parsed_args)
            elif parsed_args.command == 'register':
                return self._handle_register(parsed_args)
            elif parsed_args.command == 'suite':
                return self._handle_suite(parsed_args)
            elif parsed_args.command == 'results':
                return self._handle_results(parsed_args)
            else:
                print(f"Unknown command: {parsed_args.command}")
                return 1
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    def _handle_run(self, args) -> int:
        """Handle the run command"""
        results = []
        
        if args.all:
            print("🧪 Running all registered tests...")
            results = self.orchestrator.run_all_tests()
        elif args.suite:
            print(f"🧪 Running tests in suite: {args.suite}")
            results = self.orchestrator.run_test_suite(args.suite)
        elif args.type:
            test_type = TestType(args.type)
            print(f"🧪 Running {test_type.value} tests...")
            results = self.orchestrator.run_tests_by_type(test_type)
        elif args.priority:
            priority = TestPriority(args.priority)
            print(f"🧪 Running tests with priority {priority.value}...")
            results = self.orchestrator.run_tests_by_priority(priority)
        elif args.test_id:
            print(f"🧪 Running test: {args.test_id}")
            result = self.orchestrator.run_test(args.test_id)
            if result:
                results = [result]
        else:
            print("No run target specified. Use --help for usage information.")
            return 1
        
        if results:
            print(f"\n✅ Test execution completed. {len(results)} tests run.")
            
            # Save results if requested
            if args.save_results:
                filepath = self.orchestrator.save_results(args.save_results)
                print(f"📁 Results saved to: {filepath}")
            
            # Print summary
            self.orchestrator.print_status()
        else:
            print("No tests were executed.")
        
        return 0
    
    def _handle_report(self, args) -> int:
        """Handle the report command"""
        results = self.orchestrator.get_test_results()
        
        if not results:
            print("No test results available for reporting.")
            return 1
        
        print(f"📊 Generating reports for {len(results)} test results...")
        
        if args.coverage:
            coverage_reporter = CoverageReporter(args.output_dir)
            filepath = coverage_reporter.generate_report(results)
            print(f"📈 Coverage report generated: {filepath}")
            coverage_reporter.print_coverage_summary(results)
        
        if args.performance:
            performance_reporter = PerformanceReporter(args.output_dir)
            filepath = performance_reporter.generate_report(results)
            print(f"⏱️  Performance report generated: {filepath}")
            performance_reporter.print_performance_summary(results)
        
        if args.html:
            html_reporter = HTMLReporter(args.output_dir)
            filepath = html_reporter.generate_report(results)
            print(f"🌐 HTML report generated: {filepath}")
        
        if not any([args.coverage, args.performance, args.html]):
            print("No report types specified. Use --coverage, --performance, or --html")
            return 1
        
        return 0
    
    def _handle_status(self, args) -> int:
        """Handle the status command"""
        if args.detailed:
            self.orchestrator.print_status()
        else:
            status = self.orchestrator.get_system_status()
            print(f"🧪 Testing Framework Status: {status['system_status']}")
            print(f"📊 Registered Tests: {status['registered_tests']}")
            print(f"📁 Available Suites: {status['available_suites']}")
            print(f"📂 Results Directory: {status['results_directory']}")
        
        return 0
    
    def _handle_register(self, args) -> int:
        """Handle the register command"""
        if args.test_file:
            print(f"📝 Registering tests from file: {args.test_file}")
            # TODO: Implement test registration from file
            print("Test file registration not yet implemented")
        elif args.test_dir:
            print(f"📝 Registering tests from directory: {args.test_dir}")
            # TODO: Implement test registration from directory
            print("Test directory registration not yet implemented")
        else:
            print("No registration source specified. Use --test-file or --test-dir")
            return 1
        
        return 0
    
    def _handle_suite(self, args) -> int:
        """Handle the suite command"""
        if args.list:
            suites = self.orchestrator.suite_manager.list_test_suites()
            if suites:
                print("📁 Available Test Suites:")
                for suite in suites:
                    print(f"  • {suite.suite_id}: {suite.suite_name}")
                    print(f"    Description: {suite.description}")
                    print(f"    Tests: {suite.get_test_count()}")
                    print(f"    Priority: {suite.priority.value}")
                    print()
            else:
                print("No test suites available.")
        
        elif args.create:
            if not args.suite_id:
                print("Suite ID required for creation. Use --suite-id")
                return 1
            
            description = args.description or f"Test suite: {args.create}"
            suite = self.orchestrator.suite_manager.create_test_suite(
                args.suite_id, args.create, description
            )
            print(f"✅ Created test suite: {suite.suite_id}")
        
        elif args.add_test:
            if not args.suite_id:
                print("Suite ID required. Use --suite-id")
                return 1
            
            success = self.orchestrator.suite_manager.add_test_to_suite(args.suite_id, args.add_test)
            if success:
                print(f"✅ Added test {args.add_test} to suite {args.suite_id}")
            else:
                print(f"❌ Failed to add test {args.add_test} to suite {args.suite_id}")
        
        else:
            print("No suite action specified. Use --list, --create, or --add-test")
            return 1
        
        return 0
    
    def _handle_results(self, args) -> int:
        """Handle the results command"""
        if args.list:
            results = self.orchestrator.get_test_results()
            if results:
                print(f"📊 Test Results ({len(results)} total):")
                for result in results:
                    status_emoji = "✅" if result.status.value == "passed" else "❌"
                    print(f"  {status_emoji} {result.test_name} ({result.test_type.value}) - {result.status.value}")
            else:
                print("No test results available.")
        
        elif args.export:
            if args.export == 'json':
                export_data = self.orchestrator.export_results('json')
                print("📤 JSON export completed")
                print(export_data[:500] + "..." if len(export_data) > 500 else export_data)
            elif args.export == 'csv':
                print("📤 CSV export not yet implemented")
        
        elif args.clear:
            self.orchestrator.clear_results()
            print("🗑️  All test results cleared.")
        
        else:
            print("No results action specified. Use --list, --export, or --clear")
            return 1
        
        return 0


def main():
    """Main entry point for the CLI"""
    cli = TestingFrameworkCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
