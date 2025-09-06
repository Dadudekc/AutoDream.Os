#!/usr/bin/env python3
"""
CLI Interface for Gaming Test Runner
==================================

Command-line interface for the gaming test runner system.

Author: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.unified_entry_point_system import main


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
        """,
    )

    # Test execution options
    parser.add_argument("--test", "-t", help="Run a specific test by ID")
    parser.add_argument("--suite", "-s", help="Run a test suite by ID")
    parser.add_argument("--all", action="store_true", help="Run all available tests")

    # Output options
    parser.add_argument("--results", action="store_true", help="Show test results")
    parser.add_argument("--export", "-e", help="Export results to JSON file")
    parser.add_argument(
        "--list-tests", action="store_true", help="List available tests"
    )
    parser.add_argument(
        "--list-suites", action="store_true", help="List available test suites"
    )

    # Configuration options
    parser.add_argument("--config", "-c", help="Configuration file path")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    return parser


if __name__ == "__main__":
    asyncio.run(main())
