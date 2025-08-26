#!/usr/bin/env python3
"""
Performance CLI Interface - Agent Cellphone V2
=============================================

Handles CLI argument parsing and user interface.
Follows V2 standards: SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
import logging
import sys
from typing import Optional


class PerformanceCLIInterface:
    """Handles CLI argument parsing and user interface"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceCLIInterface")
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser."""
        parser = argparse.ArgumentParser(
            description="Performance Validation System CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s test                           # Run smoke test
  %(prog)s benchmark --type response      # Run response time benchmark
  %(prog)s benchmark --all                # Run all benchmarks
  %(prog)s report --format text           # Show latest report in text format
  %(prog)s config --show                  # Show current configuration
  %(prog)s config --update-threshold response_time 0.3  # Update threshold
            """
        )
        
        # Global options
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose logging"
        )
        parser.add_argument(
            "--config", "-c",
            type=str,
            help="Path to configuration file"
        )
        parser.add_argument(
            "--output", "-o",
            type=str,
            help="Output file for results"
        )
        
        # Subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Test command
        # "validate" kept for backward compatibility with V1 command name
        test_parser = subparsers.add_parser(
            "test", aliases=["validate"], help="Run performance validation tests"
        )
        test_parser.add_argument(
            "--smoke",
            action="store_true",
            help="Run smoke test only"
        )
        test_parser.add_argument(
            "--quick",
            action="store_true",
            help="Run quick validation test"
        )
        
        # Benchmark command
        benchmark_parser = subparsers.add_parser("benchmark", help="Run performance benchmarks")
        benchmark_parser.add_argument(
            "--type", "-t",
            type=str,
            choices=["response_time", "throughput", "scalability", "reliability", "resource"],
            help="Specific benchmark type to run"
        )
        benchmark_parser.add_argument(
            "--all", "-a",
            action="store_true",
            help="Run all enabled benchmarks"
        )
        benchmark_parser.add_argument(
            "--iterations", "-i",
            type=int,
            default=5,
            help="Number of benchmark iterations"
        )
        benchmark_parser.add_argument(
            "--timeout",
            type=int,
            default=300,
            help="Benchmark timeout in seconds"
        )
        
        # Report command
        report_parser = subparsers.add_parser("report", help="Generate and display reports")
        report_parser.add_argument(
            "--format", "-f",
            type=str,
            choices=["json", "text", "html"],
            default="text",
            help="Report output format"
        )
        report_parser.add_argument(
            "--latest", "-l",
            action="store_true",
            help="Show latest report only"
        )
        report_parser.add_argument(
            "--export",
            type=str,
            help="Export report to file"
        )
        
        # Config command
        config_parser = subparsers.add_parser("config", help="Manage configuration")
        config_parser.add_argument(
            "--show", "-s",
            action="store_true",
            help="Show current configuration"
        )
        config_parser.add_argument(
            "--load",
            type=str,
            help="Load configuration from file"
        )
        config_parser.add_argument(
            "--save",
            type=str,
            help="Save configuration to file"
        )
        config_parser.add_argument(
            "--update-threshold",
            nargs=3,
            metavar=("METRIC", "VALUE", "OPERATOR"),
            help="Update validation threshold (e.g., response_time 0.3 lte)"
        )
        config_parser.add_argument(
            "--enable-benchmark",
            type=str,
            help="Enable specific benchmark type"
        )
        config_parser.add_argument(
            "--disable-benchmark",
            type=str,
            help="Disable specific benchmark type"
        )
        
        # Status command
        status_parser = subparsers.add_parser("status", help="Show system status")
        status_parser.add_argument(
            "--detailed", "-d",
            action="store_true",
            help="Show detailed status information"
        )
        
        return parser
    
    def parse_args(self, args: Optional[list] = None):
        """Parse command line arguments."""
        try:
            return self.parser.parse_args(args)
        except Exception as e:
            self.logger.error(f"Argument parsing failed: {e}")
            self.parser.print_help()
            sys.exit(1)
    
    def setup_logging(self, verbose: bool = False):
        """Setup logging configuration."""
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
    
    def print_help(self):
        """Print help information."""
        self.parser.print_help()
    
    def print_error(self, message: str):
        """Print error message."""
        print(f"❌ {message}", file=sys.stderr)
    
    def print_success(self, message: str):
        """Print success message."""
        print(f"✅ {message}")
    
    def print_info(self, message: str):
        """Print info message."""
        print(f"ℹ️  {message}")
    
    def print_warning(self, message: str):
        """Print warning message."""
        print(f"⚠️  {message}")
