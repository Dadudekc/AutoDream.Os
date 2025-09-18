#!/usr/bin/env python3
"""
V2_SWARM Test Runner
====================

Comprehensive test runner for V2_SWARM project.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔍 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="V2_SWARM Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--v2-compliance", action="store_true", help="Run V2 compliance tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--html", action="store_true", help="Generate HTML coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-n", type=int, help="Run tests in parallel")
    parser.add_argument("--timeout", type=int, default=300, help="Test timeout in seconds")
    parser.add_argument("--maxfail", type=int, default=5, help="Maximum failures before stopping")
    
    args = parser.parse_args()
    
    # Default to running all tests if no specific test type is specified
    if not any([args.unit, args.integration, args.performance, args.v2_compliance]):
        args.all = True
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test paths
    test_paths = []
    if args.unit or args.all:
        test_paths.append("tests/unit/")
    if args.integration or args.all:
        test_paths.append("tests/integration/")
    if args.performance or args.all:
        test_paths.append("tests/performance/")
    if args.v2_compliance or args.all:
        test_paths.append("tests/unit/test_v2_compliance.py")
    
    if test_paths:
        cmd.extend(test_paths)
    else:
        cmd.append("tests/")
    
    # Add options
    if args.verbose:
        cmd.append("-v")
    
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    if args.timeout:
        cmd.extend(["--timeout", str(args.timeout)])
    
    if args.maxfail:
        cmd.extend(["--maxfail", str(args.maxfail)])
    
    if args.coverage or args.html:
        cmd.extend(["--cov=src", "--cov=thea_auth"])
        
        if args.html:
            cmd.extend(["--cov-report=html:htmlcov"])
        else:
            cmd.extend(["--cov-report=term-missing"])
    
    # Run tests
    success = run_command(cmd, "Running V2_SWARM Tests")
    
    if success:
        print("\n✅ All tests passed!")
        
        if args.coverage or args.html:
            print("\n📊 Coverage Report Generated")
            if args.html:
                print("📄 HTML Coverage Report: htmlcov/index.html")
        
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


def run_specific_tests():
    """Run specific test categories."""
    test_categories = {
        "messaging": "tests/unit/test_messaging_system.py",
        "discord": "tests/unit/test_discord_commander.py",
        "v2-compliance": "tests/unit/test_v2_compliance.py",
        "integration": "tests/integration/",
        "performance": "tests/performance/"
    }
    
    print("🧪 V2_SWARM Test Categories:")
    for category, path in test_categories.items():
        print(f"  - {category}: {path}")
    
    print("\n💡 Usage Examples:")
    print("  python run_tests.py --unit --coverage")
    print("  python run_tests.py --integration --verbose")
    print("  python run_tests.py --performance --parallel 4")
    print("  python run_tests.py --v2-compliance")
    print("  python run_tests.py --all --html")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_specific_tests()
    else:
        sys.exit(main())
