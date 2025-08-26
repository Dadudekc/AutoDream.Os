#!/usr/bin/env python3
"""
Comprehensive Test Runner for Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - TDD Integration Project

This script provides a unified interface for running all types of tests
with comprehensive reporting and quality metrics.
"""

import argparse
import sys
import time
import subprocess

from src.utils.stability_improvements import stability_manager, safe_import
from src.core.testing.test_categories import TestCategories
from src.core.testing.output_formatter import OutputFormatter
from pathlib import Path
from typing import Dict, List, Any, Optional


class TestRunner:
    """Comprehensive test runner with multiple test types and reporting."""

    def __init__(self, repo_root: Path):
        """Initialize the test runner."""
        self.repo_root = repo_root
        self.tests_dir = repo_root / "tests"
        self.results = {}
        self.start_time = None
        self.end_time = None
        self.formatter = OutputFormatter()
        self.categories = TestCategories()

    def print_banner(self):
        """Print the test runner banner."""
        self.formatter.print_banner(str(self.repo_root))

    def check_prerequisites(self) -> bool:
        """Check if all testing prerequisites are met."""
        self.formatter.print_prerequisites_check("Checking testing prerequisites...")

        # Check if pytest is available
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                self.formatter.print_success(f"pytest available: {result.stdout.strip()}")
            else:
                self.formatter.print_error("pytest not available")
                return False
        except Exception as e:
            self.formatter.print_error(f"pytest check failed: {e}")
            return False

        # Check if tests directory exists
        if not self.tests_dir.exists():
            self.formatter.print_error(f"Tests directory not found: {self.tests_dir}")
            return False

        # Check if conftest.py exists
        conftest_file = self.tests_dir / "conftest.py"
        if not conftest_file.exists():
            self.formatter.print_error(f"conftest.py not found: {conftest_file}")
            return False

        self.formatter.print_success("All prerequisites met!")
        return True

    def run_test_category(self, category: str, verbose: bool = False) -> Dict[str, Any]:
        """Run tests for a specific category."""
        config = self.categories.get_category(category)
        if not config:
            return {"success": False, "error": f"Unknown test category: {category}"}

        self.formatter.print_test_category_header(
            category, config['description'], config['timeout'], config['critical']
        )

        start_time = time.time()

        try:
            # Build pytest command
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                "-v",
                "--tb=short",
                "--durations=10",
                f"--timeout={config['timeout']}",
                str(self.tests_dir),
            ] + config["command"]

            if verbose:
                cmd.append("-s")

            # Run pytest
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=config["timeout"] + 30,  # Add buffer
            )

            end_time = time.time()
            duration = end_time - start_time

            # Parse results
            success = result.returncode == 0
            output = result.stdout
            error_output = result.stderr

            # Extract test statistics
            stats = self._parse_pytest_output(output)

            result_data = {
                "success": success,
                "category": category,
                "duration": duration,
                "output": output,
                "error_output": error_output,
                "tests_run": stats.get("tests_run", 0),
                "failures": stats.get("failures", 0),
                "errors": stats.get("errors", 0),
            }

            self.results[category] = result_data
            return result_data

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "category": category,
                "error": f"Test execution timed out after {config['timeout']} seconds",
            }
        except Exception as e:
            return {
                "success": False,
                "category": category,
                "error": f"Test execution failed: {str(e)}",
            }

    def _parse_pytest_output(self, output: str) -> Dict[str, int]:
        """Parse pytest output to extract test statistics."""
        stats = {"tests_run": 0, "failures": 0, "errors": 0}
        
        lines = output.split("\n")
        for line in lines:
            if "collected" in line and "items" in line:
                try:
                    stats["tests_run"] = int(line.split()[0])
                except (ValueError, IndexError):
                    pass
            elif "failed" in line and "passed" in line:
                try:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "failed":
                            stats["failures"] = int(parts[i - 1])
                        elif part == "passed":
                            stats["tests_run"] = int(parts[i - 1])
                except (ValueError, IndexError):
                    pass
        
        return stats

    def run_all_tests(self, verbose: bool = False) -> Dict[str, Any]:
        """Run all test categories."""
        self.start_time = time.time()
        
        categories = self.categories.list_categories()
        successful = 0
        failed = 0
        
        for category in categories:
            result = self.run_test_category(category, verbose)
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            self.formatter.print_test_results(result)
        
        self.end_time = time.time()
        
        summary = {
            "total_categories": len(categories),
            "successful": successful,
            "failed": failed,
            "total_duration": self.end_time - self.start_time,
            "overall_success": failed == 0,
        }
        
        self.formatter.print_summary(summary)
        return summary

    def run_specific_categories(self, categories: List[str], verbose: bool = False) -> Dict[str, Any]:
        """Run tests for specific categories."""
        self.start_time = time.time()
        
        successful = 0
        failed = 0
        
        for category in categories:
            if category in self.categories.list_categories():
                result = self.run_test_category(category, verbose)
                if result["success"]:
                    successful += 1
                else:
                    failed += 1
                
                self.formatter.print_test_results(result)
            else:
                self.formatter.print_error(f"Unknown test category: {category}")
                failed += 1
        
        self.end_time = time.time()
        
        summary = {
            "total_categories": len(categories),
            "successful": successful,
            "failed": failed,
            "total_duration": self.end_time - self.start_time,
            "overall_success": failed == 0,
        }
        
        self.formatter.print_summary(summary)
        return summary


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Comprehensive Test Runner")
    parser.add_argument("--categories", nargs="+", help="Specific test categories to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--list-categories", action="store_true", help="List available test categories")
    
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent
    runner = TestRunner(repo_root)
    
    if args.list_categories:
        print("Available test categories:")
        for category in TestCategories.list_categories():
            config = TestCategories.get_category(category)
            print(f"  • {category}: {config['description']}")
        return 0
    
    runner.print_banner()
    
    if not runner.check_prerequisites():
        return 1
    
    if args.categories:
        summary = runner.run_specific_categories(args.categories, args.verbose)
    else:
        summary = runner.run_all_tests(args.verbose)
    
    return 0 if summary["overall_success"] else 1


if __name__ == "__main__":
    sys.exit(main())
