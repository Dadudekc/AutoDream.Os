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
from src.core.testing.cli_handlers import (
    RunCommandHandler,
    ReportCommandHandler,
    StatusCommandHandler,
    RegisterCommandHandler,
    SuiteCommandHandler,
    ResultsCommandHandler
)


class TestingFrameworkCLI:
    """Command-line interface for the testing framework"""
    
    def __init__(self):
        self.orchestrator = TestOrchestrator()
        self.parser = self._create_parser()
        
        # Initialize command handlers
        self.handlers = {
            'run': RunCommandHandler(self.orchestrator),
            'report': ReportCommandHandler(self.orchestrator),
            'status': StatusCommandHandler(self.orchestrator),
            'register': RegisterCommandHandler(self.orchestrator),
            'suite': SuiteCommandHandler(self.orchestrator),
            'results': ResultsCommandHandler(self.orchestrator)
        }
    
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
        run_parser.add_argument('--type', type=str, help='Run tests of specific type')
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
            
            # Route to appropriate handler
            if parsed_args.command in self.handlers:
                return self.handlers[parsed_args.command].handle(parsed_args)
            else:
                print(f"Unknown command: {parsed_args.command}")
                return 1
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 1


def main():
    """Main entry point for the CLI"""
    cli = TestingFrameworkCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
