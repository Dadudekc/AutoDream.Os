#!/usr/bin/env python3
"""
Test Coverage Runner
====================

Simple script to run the new test coverage improvements.
This script helps execute the comprehensive test suites created
for the Agent Cellphone V2 system.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and return the result."""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print("Error:", result.stderr)
            if result.stdout:
                print("Output:", result.stdout)
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False


def check_python_environment():
    """Check if Python environment is properly set up."""
    print("🔍 Checking Python Environment")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    print("✅ Python version is compatible")
    
    # Check if we're in the right directory
    if not Path("src").exists():
        print("❌ 'src' directory not found. Please run from project root.")
        return False
    
    print("✅ Project structure looks correct")
    return True


def run_individual_tests():
    """Run individual test files."""
    test_files = [
        ("tests/unit/test_messaging_service.py", "Messaging Service Tests"),
        ("tests/unit/test_coordination_service.py", "Coordination Service Tests"),
        ("tests/unit/test_coordinate_loader_core.py", "Coordinate Loader Tests"),
        ("tests/unit/test_consolidated_messaging_service.py", "Consolidated Messaging Service Tests"),
        ("tests/unit/test_commandresult_advanced.py", "CommandResult Advanced Tests"),
    ]
    
    results = []
    
    for test_file, description in test_files:
        if Path(test_file).exists():
            success = run_command(f"python3 -m pytest {test_file} -v", description)
            results.append((test_file, success))
        else:
            print(f"⚠️  Test file not found: {test_file}")
            results.append((test_file, False))
    
    return results


def run_all_tests():
    """Run all new test files together."""
    test_files = [
        "tests/unit/test_messaging_service.py",
        "tests/unit/test_coordination_service.py", 
        "tests/unit/test_coordinate_loader_core.py",
        "tests/unit/test_consolidated_messaging_service.py",
        "tests/unit/test_commandresult_advanced.py",
    ]
    
    # Filter to only existing files
    existing_files = [f for f in test_files if Path(f).exists()]
    
    if not existing_files:
        print("❌ No test files found")
        return False
    
    test_files_str = " ".join(existing_files)
    return run_command(f"python3 -m pytest {test_files_str} -v", "All New Test Files")


def run_with_coverage():
    """Run tests with coverage reporting."""
    test_files = [
        "tests/unit/test_messaging_service.py",
        "tests/unit/test_coordination_service.py",
        "tests/unit/test_coordinate_loader_core.py", 
        "tests/unit/test_consolidated_messaging_service.py",
        "tests/unit/test_commandresult_advanced.py",
    ]
    
    # Filter to only existing files
    existing_files = [f for f in test_files if Path(f).exists()]
    
    if not existing_files:
        print("❌ No test files found")
        return False
    
    test_files_str = " ".join(existing_files)
    
    # Try to run with coverage if pytest-cov is available
    coverage_command = f"python3 -m pytest {test_files_str} --cov=src --cov-report=term-missing -v"
    
    print("\n📊 Running Tests with Coverage")
    print("=" * 50)
    print("Note: This requires pytest-cov to be installed")
    print("Install with: pip install pytest-cov")
    
    return run_command(coverage_command, "Tests with Coverage Reporting")


def main():
    """Main function to run test coverage improvements."""
    print("🚀 Agent Cellphone V2 - Test Coverage Runner")
    print("=" * 60)
    print("This script runs the comprehensive test suites created")
    print("to improve test coverage for the V2 system.")
    print()
    
    # Check environment
    if not check_python_environment():
        print("\n❌ Environment check failed. Please fix issues and try again.")
        return 1
    
    print("\n📋 Available Test Options:")
    print("1. Run individual test files")
    print("2. Run all new test files")
    print("3. Run tests with coverage reporting")
    print("4. Run all options")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🔍 Running Individual Test Files")
                results = run_individual_tests()
                
                print("\n📊 Individual Test Results:")
                for test_file, success in results:
                    status = "✅ PASSED" if success else "❌ FAILED"
                    print(f"  {test_file}: {status}")
                
                break
                
            elif choice == "2":
                print("\n🔍 Running All New Test Files")
                success = run_all_tests()
                if success:
                    print("\n🎉 All tests completed successfully!")
                else:
                    print("\n❌ Some tests failed. Check output above.")
                break
                
            elif choice == "3":
                print("\n🔍 Running Tests with Coverage")
                success = run_with_coverage()
                if success:
                    print("\n🎉 Coverage tests completed successfully!")
                else:
                    print("\n❌ Coverage tests failed. Check output above.")
                break
                
            elif choice == "4":
                print("\n🔍 Running All Test Options")
                
                # Run individual tests
                results = run_individual_tests()
                
                # Run all tests
                all_success = run_all_tests()
                
                # Run with coverage
                coverage_success = run_with_coverage()
                
                print("\n📊 Final Results Summary:")
                print("=" * 50)
                for test_file, success in results:
                    status = "✅ PASSED" if success else "❌ FAILED"
                    print(f"  {test_file}: {status}")
                
                print(f"  All Tests Combined: {'✅ PASSED' if all_success else '❌ FAILED'}")
                print(f"  Coverage Tests: {'✅ PASSED' if coverage_success else '❌ FAILED'}")
                
                break
                
            elif choice == "5":
                print("\n👋 Goodbye!")
                return 0
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            return 0
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return 1
    
    print("\n🎉 Test Coverage Runner completed!")
    print("📊 Check the TEST_COVERAGE_IMPROVEMENT_REPORT.md for detailed information")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())