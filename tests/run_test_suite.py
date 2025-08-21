#!/usr/bin/env python3
"""
Comprehensive Test Suite Runner for Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - TDD Integration Project

This script provides a unified interface for running all types of tests
with comprehensive reporting and quality metrics.
"""

import argparse
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)

class TestSuiteRunner:
    """Comprehensive test suite runner with multiple test types and reporting."""
    
    def __init__(self, repo_root: Path):
        """Initialize the test suite runner."""
        self.repo_root = repo_root
        self.tests_dir = repo_root / "tests"
        self.results = {}
        self.start_time = None
        self.end_time = None
        
        # Test categories and their configurations
        self.test_categories = {
            "smoke": {
                "description": "Smoke tests for basic functionality validation",
                "marker": "smoke",
                "timeout": 60,
                "critical": True
            },
            "unit": {
                "description": "Unit tests for individual components",
                "marker": "unit", 
                "timeout": 120,
                "critical": True
            },
            "integration": {
                "description": "Integration tests for component interaction",
                "marker": "integration",
                "timeout": 300,
                "critical": False
            },
            "performance": {
                "description": "Performance and load testing",
                "marker": "performance",
                "timeout": 600,
                "critical": False
            },
            "security": {
                "description": "Security and vulnerability testing",
                "marker": "security",
                "timeout": 180,
                "critical": True
            },
            "api": {
                "description": "API endpoint testing",
                "marker": "marker",
                "timeout": 240,
                "critical": False
            }
        }
    
    def print_banner(self):
        """Print the test suite banner."""
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}🧪 AGENT_CELLPHONE_V2 COMPREHENSIVE TEST SUITE")
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}Foundation & Testing Specialist - TDD Integration Project")
        print(f"{Fore.CYAN}Repository: {self.repo_root}")
        print(f"{Fore.CYAN}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def check_prerequisites(self) -> bool:
        """Check if all testing prerequisites are met."""
        print(f"{Fore.YELLOW}🔍 Checking testing prerequisites...{Style.RESET_ALL}")
        
        # Check if pytest is available
        try:
            import pytest
            print(f"✅ pytest {pytest.__version__} available")
        except ImportError:
            print(f"{Fore.RED}❌ pytest not available - install with: pip install -r requirements_testing.txt{Style.RESET_ALL}")
            return False
        
        # Check if tests directory exists
        if not self.tests_dir.exists():
            print(f"{Fore.RED}❌ Tests directory not found: {self.tests_dir}{Style.RESET_ALL}")
            return False
        
        # Check if conftest.py exists
        conftest_file = self.tests_dir / "conftest.py"
        if not conftest_file.exists():
            print(f"{Fore.RED}❌ conftest.py not found: {conftest_file}{Style.RESET_ALL}")
            return False
        
        print(f"✅ All prerequisites met!")
        return True
    
    def run_test_category(self, category: str, verbose: bool = False) -> Dict[str, Any]:
        """Run tests for a specific category."""
        if category not in self.test_categories:
            return {"success": False, "error": f"Unknown test category: {category}"}
        
        config = self.test_categories[category]
        print(f"\n{Fore.BLUE}🚀 Running {category.upper()} tests...{Style.RESET_ALL}")
        print(f"   Description: {config['description']}")
        print(f"   Timeout: {config['timeout']}s")
        print(f"   Critical: {'Yes' if config['critical'] else 'No'}")
        
        start_time = time.time()
        
        try:
            # Build pytest command
            cmd = [
                sys.executable, "-m", "pytest",
                "-v",
                "-m", config["marker"],
                "--tb=short",
                "--durations=10",
                f"--timeout={config['timeout']}",
                str(self.tests_dir)
            ]
            
            if verbose:
                cmd.append("-s")
            
            # Run pytest
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=config["timeout"] + 30  # Add buffer
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
                "duration": duration,
                "return_code": result.returncode,
                "output": output,
                "error_output": error_output,
                "stats": stats,
                "critical": config["critical"]
            }
            
            # Print results
            if success:
                print(f"{Fore.GREEN}✅ {category.upper()} tests completed successfully in {duration:.2f}s{Style.RESET_ALL}")
                print(f"   Tests: {stats.get('total', 'N/A')}")
                print(f"   Passed: {stats.get('passed', 'N/A')}")
                print(f"   Failed: {stats.get('failed', 'N/A')}")
            else:
                print(f"{Fore.RED}❌ {category.upper()} tests failed after {duration:.2f}s{Style.RESET_ALL}")
                if stats.get('failed', 0) > 0:
                    print(f"   Failed tests: {stats.get('failed', 'N/A')}")
            
            return result_data
            
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}⏰ {category.upper()} tests timed out after {config['timeout']}s{Style.RESET_ALL}")
            return {
                "success": False,
                "error": "Timeout exceeded",
                "duration": config["timeout"],
                "critical": config["critical"]
            }
        except Exception as e:
            print(f"{Fore.RED}💥 {category.upper()} tests failed with exception: {e}{Style.RESET_ALL}")
            return {
                "success": False,
                "error": str(e),
                "duration": 0,
                "critical": config["critical"]
            }
    
    def _parse_pytest_output(self, output: str) -> Dict[str, Any]:
        """Parse pytest output to extract test statistics."""
        stats = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0
        }
        
        try:
            lines = output.split('\n')
            for line in lines:
                if 'collected' in line and 'items' in line:
                    # Extract total tests
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'collected':
                            if i + 1 < len(parts):
                                stats["total"] = int(parts[i + 1])
                            break
                elif 'passed' in line and 'failed' in line:
                    # Extract passed/failed counts
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'passed':
                            if i + 1 < len(parts):
                                stats["passed"] = int(parts[i + 1])
                        elif part == 'failed':
                            if i + 1 < len(parts):
                                stats["failed"] = int(parts[i + 1])
        except Exception:
            pass
        
        return stats
    
    def run_all_tests(self, categories: Optional[List[str]] = None, verbose: bool = False) -> Dict[str, Any]:
        """Run all test categories or specified ones."""
        if categories is None:
            categories = list(self.test_categories.keys())
        
        self.start_time = time.time()
        self.print_banner()
        
        if not self.check_prerequisites():
            return {"success": False, "error": "Prerequisites not met"}
        
        print(f"{Fore.GREEN}🎯 Running test categories: {', '.join(categories)}{Style.RESET_ALL}\n")
        
        # Run each test category
        for category in categories:
            if category in self.test_categories:
                result = self.run_test_category(category, verbose)
                self.results[category] = result
                
                # Check if critical test failed
                if not result["success"] and result.get("critical", False):
                    print(f"\n{Fore.RED}🚨 CRITICAL TEST FAILURE: {category.upper()} tests failed!{Style.RESET_ALL}")
                    print(f"   Stopping test execution due to critical failure.")
                    break
        
        self.end_time = time.time()
        return self._generate_summary()
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive test summary."""
        total_duration = self.end_time - self.start_time if self.start_time and self.end_time else 0
        
        # Calculate overall statistics
        total_tests = sum(result.get("stats", {}).get("total", 0) for result in self.results.values())
        total_passed = sum(result.get("stats", {}).get("passed", 0) for result in self.results.values())
        total_failed = sum(result.get("stats", {}).get("failed", 0) for result in self.results.values())
        
        # Determine overall success
        critical_failures = any(
            not result["success"] and result.get("critical", False)
            for result in self.results.values()
        )
        
        overall_success = not critical_failures and all(
            result["success"] for result in self.results.values()
        )
        
        # Calculate success rate
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        summary = {
            "overall_success": overall_success,
            "critical_failures": critical_failures,
            "total_duration": total_duration,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": success_rate,
            "category_results": self.results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Print summary
        self._print_summary(summary)
        
        return summary
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Print the test summary."""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📊 TEST SUITE SUMMARY")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Overall status
        status_color = Fore.GREEN if summary["overall_success"] else Fore.RED
        status_icon = "✅" if summary["overall_success"] else "❌"
        print(f"{status_color}{status_icon} Overall Status: {'PASSED' if summary['overall_success'] else 'FAILED'}{Style.RESET_ALL}")
        
        # Statistics
        print(f"\n📈 Test Statistics:")
        print(f"   Total Duration: {summary['total_duration']:.2f}s")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {Fore.GREEN}{summary['total_passed']}{Style.RESET_ALL}")
        print(f"   Failed: {Fore.RED}{summary['total_failed']}{Style.RESET_ALL}")
        print(f"   Success Rate: {Fore.CYAN}{summary['success_rate']:.1f}%{Style.RESET_ALL}")
        
        # Category results
        print(f"\n🎯 Category Results:")
        for category, result in summary["category_results"].items():
            status_icon = "✅" if result["success"] else "❌"
            status_color = Fore.GREEN if result["success"] else Fore.RED
            critical_mark = "🚨" if result.get("critical", False) else ""
            
            print(f"   {status_icon} {category.upper()}: {status_color}{'PASSED' if result['success'] else 'FAILED'}{Style.RESET_ALL} {critical_mark}")
            if result["success"]:
                stats = result.get("stats", {})
                print(f"      Tests: {stats.get('passed', 0)} passed, {stats.get('failed', 0)} failed ({result['duration']:.2f}s)")
            else:
                print(f"      Error: {result.get('error', 'Unknown error')} ({result['duration']:.2f}s)")
        
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Recommendations
        if not summary["overall_success"]:
            print(f"\n{Fore.YELLOW}💡 Recommendations:{Style.RESET_ALL}")
            if summary["critical_failures"]:
                print(f"   🚨 Fix critical test failures first")
            if summary["success_rate"] < 80:
                print(f"   📊 Improve test success rate (target: ≥80%)")
            print(f"   🔍 Review failed tests and fix underlying issues")
            print(f"   🧪 Run individual test categories for detailed debugging")
    
    def save_results(self, output_file: Optional[Path] = None) -> Path:
        """Save test results to a JSON file."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.repo_root / "test_results" / f"test_suite_results_{timestamp}.json"
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {output_file}")
        return output_file


def main():
    """Main entry point for the test suite runner."""
    parser = argparse.ArgumentParser(
        description="Comprehensive Test Suite Runner for Agent_Cellphone_V2_Repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python tests/run_test_suite.py
  
  # Run specific test categories
  python tests/run_test_suite.py --categories smoke unit
  
  # Run with verbose output
  python tests/run_test_suite.py --verbose
  
  # Run only critical tests
  python tests/run_test_suite.py --critical-only
        """
    )
    
    parser.add_argument(
        "--categories", "-c",
        nargs="+",
        choices=["smoke", "unit", "integration", "performance", "security", "api"],
        help="Specific test categories to run (default: all)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--critical-only",
        action="store_true",
        help="Run only critical tests (smoke, unit, security)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file for test results (default: auto-generated)"
    )
    
    args = parser.parse_args()
    
    # Determine test categories
    if args.critical_only:
        categories = ["smoke", "unit", "security"]
    elif args.categories:
        categories = args.categories
    else:
        categories = None  # Run all
    
    # Initialize and run test suite
    repo_root = Path(__file__).parent.parent
    runner = TestSuiteRunner(repo_root)
    
    try:
        summary = runner.run_all_tests(categories, args.verbose)
        
        # Save results if requested
        if args.output or summary["overall_success"]:
            output_file = runner.save_results(args.output)
            print(f"📁 Results saved to: {output_file}")
        
        # Exit with appropriate code
        sys.exit(0 if summary["overall_success"] else 1)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏹️  Test execution interrupted by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Test suite failed with exception: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
