#!/usr/bin/env python3
"""
Unified Test Runner - Agent Cellphone V2

Replaces all scattered test runners with a single, comprehensive
testing interface that consolidates functionality and eliminates duplication.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3G - Testing Infrastructure Cleanup
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from src.core.testing.unified_testing_system import UnifiedTestingSystem, TestExecutionConfig, TestFramework


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Unified Test Runner - Agent Cellphone V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/unified_test_runner.py                    # Run all tests
  python src/unified_test_runner.py --category unit   # Run unit tests only
  python src/unified_test_runner.py --framework unittest  # Use unittest framework
  python src/unified_test_runner.py --verbose --parallel  # Verbose with parallel execution
  python src/unified_test_runner.py --coverage --html     # Generate coverage and HTML reports
        """
    )
    
    # Test selection
    parser.add_argument(
        "--category", "-c",
        type=str,
        help="Run tests for specific category (unit, integration, performance, etc.)"
    )
    
    # Framework selection
    parser.add_argument(
        "--framework", "-f",
        type=str,
        choices=["pytest", "unittest", "custom"],
        default="pytest",
        help="Test framework to use (default: pytest)"
    )
    
    # Execution options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="Test timeout in seconds (default: 300)"
    )
    
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Enable parallel test execution"
    )
    
    parser.add_argument(
        "--max-workers", "-w",
        type=int,
        default=4,
        help="Maximum number of parallel workers (default: 4)"
    )
    
    # Coverage and reporting
    parser.add_argument(
        "--coverage", "-C",
        action="store_true",
        help="Enable code coverage reporting"
    )
    
    parser.add_argument(
        "--html-report", "-H",
        action="store_true",
        help="Generate HTML test report"
    )
    
    parser.add_argument(
        "--junit-report", "-J",
        action="store_true",
        help="Generate JUnit XML report"
    )
    
    parser.add_argument(
        "--benchmark", "-b",
        action="store_true",
        help="Enable performance benchmarking"
    )
    
    # Output format
    parser.add_argument(
        "--output-format", "-o",
        type=str,
        choices=["console", "json", "html"],
        default="console",
        help="Output format for reports (default: console)"
    )
    
    # Repository root
    parser.add_argument(
        "--repo-root", "-r",
        type=str,
        help="Repository root directory (default: auto-detected)"
    )
    
    return parser


def get_repo_root(repo_root_arg: Optional[str]) -> Path:
    """Get repository root directory"""
    if repo_root_arg:
        repo_root = Path(repo_root_arg)
        if not repo_root.exists():
            print(f"❌ Repository root not found: {repo_root}")
            sys.exit(1)
        return repo_root
    
    # Auto-detect repository root
    current_file = Path(__file__)
    repo_root = current_file.parent.parent
    
    if not repo_root.exists():
        print(f"❌ Could not auto-detect repository root from: {current_file}")
        sys.exit(1)
    
    return repo_root


def create_test_config(args: argparse.Namespace) -> TestExecutionConfig:
    """Create test execution configuration from arguments"""
    # Map framework string to enum
    framework_map = {
        "pytest": TestFramework.PYTEST,
        "unittest": TestFramework.UNITTEST,
        "custom": TestFramework.CUSTOM
    }
    
    return TestExecutionConfig(
        framework=framework_map[args.framework],
        verbose=args.verbose,
        timeout=args.timeout,
        parallel=args.parallel,
        max_workers=args.max_workers,
        coverage=args.coverage,
        html_report=args.html_report,
        junit_report=args.junit_report,
        benchmark=args.benchmark
    )


def print_banner() -> None:
    """Print unified test runner banner"""
    banner = """
🚀 UNIFIED TEST RUNNER - AGENT CELLPHONE V2
===========================================

Consolidated testing infrastructure eliminating duplication
and providing unified interfaces for all testing needs.

Task: TASK 3G - Testing Infrastructure Cleanup
V2 Standards: ≤400 LOC, SRP, OOP principles
"""
    print(banner)


def main() -> int:
    """Main entry point for unified test runner"""
    try:
        # Parse command line arguments
        parser = create_parser()
        args = parser.parse_args()
        
        # Print banner
        print_banner()
        
        # Get repository root
        repo_root = get_repo_root(args.repo_root)
        print(f"📁 Repository root: {repo_root}")
        
        # Create test configuration
        config = create_test_config(args)
        print(f"⚙️  Test framework: {config.framework.value}")
        print(f"⚙️  Parallel execution: {config.parallel}")
        print(f"⚙️  Coverage reporting: {config.coverage}")
        
        # Initialize unified testing system
        print("\n🔧 Initializing unified testing system...")
        testing_system = UnifiedTestingSystem(repo_root)
        
        # Run tests
        print(f"\n🧪 Running tests...")
        if args.category:
            print(f"📋 Category: {args.category}")
            results = testing_system.run_tests(category=args.category, config=config)
        else:
            print("📋 Category: All")
            results = testing_system.run_tests(config=config)
        
        # Generate report
        print(f"\n📊 Generating {args.output_format} report...")
        report = testing_system.generate_report(args.output_format)
        print(report)
        
        # Cleanup
        print("\n🧹 Cleaning up...")
        testing_system.cleanup()
        
        # Summary
        total_tests = len(results)
        if total_tests > 0:
            print(f"\n✅ Testing completed successfully!")
            print(f"📈 Total tests executed: {total_tests}")
        else:
            print("\n⚠️  No tests were executed")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        return 130
        
    except Exception as e:
        print(f"\n❌ Testing system error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

