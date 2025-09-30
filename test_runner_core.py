#!/usr/bin/env python3
"""
Core logic for test runner.
"""

import subprocess
import sys


class TestRunner:
    """Comprehensive test suite runner."""
    
    def __init__(self):
        """Initialize the test runner."""
        self.base_cmd = ["python", "-m", "pytest"]
    
    def build_test_command(self, test_type="all", coverage=True, verbose=True, parallel=False):
        """Build the test command."""
        cmd = self.base_cmd.copy()
        cmd.append("tests/")
        
        if verbose:
            cmd.append("-v")
        
        if coverage:
            cmd.extend([
                "--cov=src",
                "--cov-report=html",
                "--cov-report=term-missing",
                "--cov-report=xml"
            ])
        
        if parallel:
            cmd.extend(["-n", "auto"])
        
        if test_type != "all":
            cmd.extend(["-k", test_type])
        
        if test_type == "integration":
            cmd.extend(["-m", "integration"])
        elif test_type == "unit":
            cmd.extend(["-m", "unit"])
        
        cmd.extend(["--tb=short", "--strict-markers", "--disable-warnings"])
        return cmd
    
    def run_tests(self, test_type="all", coverage=True, verbose=True, parallel=False):
        """Run tests with specified options."""
        cmd = self.build_test_command(test_type, coverage, verbose, parallel)
        
        print(f"🚀 Running tests: {' '.join(cmd)}")
        print("=" * 60)
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            print("\n" + "=" * 60)
            print("✅ All tests passed!")
            return True
        except subprocess.CalledProcessError as e:
            print("\n" + "=" * 60)
            print(f"❌ Tests failed with exit code: {e.returncode}")
            return False
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False
    
    def run_coverage_report(self):
        """Run coverage report."""
        print("📊 Generating coverage report...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "coverage", "report", "--show-missing"],
                check=True,
                capture_output=False,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Coverage report failed: {e}")
            return False
    
    def run_quality_gates(self):
        """Run quality gates validation."""
        print("🔍 Running quality gates validation...")
        
        try:
            result = subprocess.run(
                ["python", "quality_gates.py"],
                check=True,
                capture_output=False
            )
            print("✅ Quality gates passed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Quality gates failed: {e}")
            return False
        except FileNotFoundError:
            print("⚠️ Quality gates script not found, skipping...")
            return True
