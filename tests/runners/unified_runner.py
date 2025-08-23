"""
Unified Test Runner - Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - Consolidated Test Runner System

This unified runner replaces the previous 3 separate test runners:
- run_tests.py (485 lines)
- run_tdd_tests.py (456 lines)
- run_all_tests.py (311 lines)

Provides all functionality in a single, maintainable system.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

from .base_runner import BaseTestRunner

# Color support
try:
    import colorama
    from colorama import Fore, Style

    colorama.init(autoreset=True)
    COLOR_AVAILABLE = True
except ImportError:

    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = RESET = ""

    class Style:
        RESET_ALL = ""

    COLOR_AVAILABLE = False


class UnifiedTestRunner(BaseTestRunner):
    """Unified test runner consolidating all previous test runners."""

    def __init__(self, repo_root: Path):
        """Initialize the unified test runner."""
        super().__init__(repo_root)

        # Test categories from original run_tests.py
        self.test_categories = {
            "smoke": {
                "description": "Smoke tests for basic functionality validation",
                "marker": "smoke",
                "timeout": 60,
                "critical": True,
                "directory": "smoke",
            },
            "unit": {
                "description": "Unit tests for individual components",
                "marker": "unit",
                "timeout": 120,
                "critical": True,
                "directory": "unit",
            },
            "integration": {
                "description": "Integration tests for component interaction",
                "marker": "integration",
                "timeout": 300,
                "critical": False,
                "directory": "integration",
            },
            "performance": {
                "description": "Performance and load testing",
                "marker": "performance",
                "timeout": 600,
                "critical": False,
                "directory": "performance",
            },
            "security": {
                "description": "Security and vulnerability testing",
                "marker": "security",
                "timeout": 180,
                "critical": True,
                "directory": "security",
            },
            "api": {
                "description": "API endpoint testing",
                "marker": "api",
                "timeout": 240,
                "critical": False,
                "directory": "api",
            },
        }

    def print_banner(self):
        """Print the unified test runner banner."""
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}🧪 UNIFIED TEST RUNNER - Agent_Cellphone_V2_Repository")
        print(f"{Fore.CYAN}Foundation & Testing Specialist - TDD Integration Project")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    def run_category(self, category: str, **kwargs) -> Dict[str, Any]:
        """Run tests for a specific category."""
        if category not in self.test_categories:
            return {
                "success": False,
                "error": f"Unknown test category: {category}",
                "available_categories": list(self.test_categories.keys()),
            }

        config = self.test_categories[category]
        print(f"\n{Fore.BLUE}🔍 Running {category.upper()} tests")
        print(f"{Fore.BLUE}Description: {config['description']}")
        print(f"{Fore.BLUE}Timeout: {config['timeout']}s")
        print(f"{Fore.BLUE}Critical: {config['critical']}{Style.RESET_ALL}")

        # Discover tests for this category
        test_files = self.discover_tests(config.get("directory"))
        if not test_files:
            print(
                f"{Fore.YELLOW}⚠️ No test files found for {category}{Style.RESET_ALL}"
            )
            return {
                "success": True,
                "category": category,
                "tests_run": 0,
                "message": "No test files found",
            }

        # Build command
        cmd = self.build_pytest_command(
            test_files,
            coverage=kwargs.get("coverage", True),
            parallel=kwargs.get("parallel", False),
            verbose=kwargs.get("verbose", True),
            markers=[config["marker"]] if config.get("marker") else None,
        )

        # Execute tests
        execution_result = self.execute_command(cmd, timeout=config["timeout"])

        # Parse results
        results = self.parse_test_results(execution_result)
        results["category"] = category
        results["config"] = config

        return results

    def run_all_categories(self, **kwargs) -> Dict[str, Any]:
        """Run all test categories."""
        print(f"\n{Fore.GREEN}🚀 Running ALL test categories{Style.RESET_ALL}")

        all_results = {
            "categories": {},
            "summary": {
                "total_tests": 0,
                "total_passed": 0,
                "total_failed": 0,
                "total_duration": 0,
                "critical_failures": 0,
            },
        }

        critical_only = kwargs.get("critical_only", False)

        for category, config in self.test_categories.items():
            if critical_only and not config.get("critical", False):
                print(
                    f"{Fore.YELLOW}⏭️ Skipping non-critical category: {category}{Style.RESET_ALL}"
                )
                continue

            result = self.run_category(category, **kwargs)
            all_results["categories"][category] = result

            # Update summary
            summary = all_results["summary"]
            summary["total_tests"] += result.get("tests_run", 0)
            summary["total_passed"] += result.get("passed", 0)
            summary["total_failed"] += result.get("failed", 0)

            if result.get("execution", {}).get("duration"):
                summary["total_duration"] += result["execution"]["duration"]

            # Check for critical failures
            if config.get("critical", False) and not result.get("success", False):
                summary["critical_failures"] += 1

        # Determine overall success
        all_results["success"] = (
            summary["critical_failures"] == 0 and summary["total_failed"] == 0
        )

        return all_results

    def run_specific_files(self, test_files: List[str], **kwargs) -> Dict[str, Any]:
        """Run specific test files."""
        file_paths = []
        for file_str in test_files:
            file_path = Path(file_str)
            if not file_path.is_absolute():
                file_path = self.repo_root / file_path

            if file_path.exists():
                file_paths.append(file_path)
            else:
                print(f"{Fore.RED}❌ Test file not found: {file_path}{Style.RESET_ALL}")

        if not file_paths:
            return {"success": False, "error": "No valid test files found"}

        print(
            f"\n{Fore.BLUE}🎯 Running specific test files: {len(file_paths)}{Style.RESET_ALL}"
        )
        for file_path in file_paths:
            print(f"  📄 {file_path}")

        # Build and execute command
        cmd = self.build_pytest_command(
            file_paths,
            coverage=kwargs.get("coverage", True),
            parallel=kwargs.get("parallel", False),
            verbose=kwargs.get("verbose", True),
        )

        execution_result = self.execute_command(cmd)
        results = self.parse_test_results(execution_result)
        results["files"] = [str(f) for f in file_paths]

        return results

    def run(self, mode: str = "all", **kwargs) -> Dict[str, Any]:
        """Main run method with different modes."""
        self.print_banner()

        if mode == "all":
            return self.run_all_categories(**kwargs)
        elif mode == "critical":
            kwargs["critical_only"] = True
            return self.run_all_categories(**kwargs)
        elif mode in self.test_categories:
            return self.run_category(mode, **kwargs)
        elif mode == "files":
            test_files = kwargs.get("test_files", [])
            return self.run_specific_files(test_files, **kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown mode: {mode}",
                "available_modes": ["all", "critical", "files"]
                + list(self.test_categories.keys()),
            }


def main():
    """Command-line interface for the unified test runner."""
    parser = argparse.ArgumentParser(
        description="Unified Test Runner - Agent_Cellphone_V2_Repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tests.runners.unified_runner --mode all
  python -m tests.runners.unified_runner --mode critical
  python -m tests.runners.unified_runner --mode smoke
  python -m tests.runners.unified_runner --mode files test_file1.py test_file2.py
        """,
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=[
            "all",
            "critical",
            "smoke",
            "unit",
            "integration",
            "performance",
            "security",
            "api",
            "files",
        ],
        default="all",
        help="Test execution mode",
    )

    parser.add_argument(
        "--no-coverage", action="store_true", help="Disable coverage reporting"
    )

    parser.add_argument(
        "--parallel", "-p", action="store_true", help="Enable parallel test execution"
    )

    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Reduce output verbosity"
    )

    parser.add_argument("--save-results", help="Save results to specific file")

    parser.add_argument(
        "test_files",
        nargs="*",
        help="Specific test files to run (only with --mode files)",
    )

    args = parser.parse_args()

    # Setup runner
    repo_root = Path(__file__).parent.parent.parent
    runner = UnifiedTestRunner(repo_root)

    # Prepare kwargs
    kwargs = {
        "coverage": not args.no_coverage,
        "parallel": args.parallel,
        "verbose": not args.quiet,
    }

    if args.mode == "files":
        kwargs["test_files"] = args.test_files

    # Run tests
    try:
        results = runner.run(mode=args.mode, **kwargs)

        # Print summary
        if args.mode == "all" or args.mode == "critical":
            print(f"\n{Fore.GREEN}📊 OVERALL SUMMARY{Style.RESET_ALL}")
            summary = results.get("summary", {})
            print(f"Total Tests: {summary.get('total_tests', 0)}")
            print(f"Passed: {summary.get('total_passed', 0)}")
            print(f"Failed: {summary.get('total_failed', 0)}")
            print(f"Duration: {summary.get('total_duration', 0):.2f}s")
            print(f"Critical Failures: {summary.get('critical_failures', 0)}")
        else:
            runner.print_summary(results)

        # Save results
        if args.save_results:
            runner.save_results(results, args.save_results)

        # Exit with appropriate code
        if results.get("success", False):
            print(f"\n{Fore.GREEN}✅ ALL TESTS COMPLETED SUCCESSFULLY{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"\n{Fore.RED}❌ TESTS FAILED{Style.RESET_ALL}")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Test execution interrupted by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Test execution error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
