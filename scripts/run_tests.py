#!/usr/bin/env python3
# 🧪 TEST RUNNER SCRIPT - AGENT_CELLPHONE_V2
# Foundation & Testing Specialist - TDD Integration Project
# Version: 1.0
# Status: ACTIVE

"""
Comprehensive Test Runner for Agent_Cellphone_V2

This script provides easy access to all testing functionality:
- Smoke tests for basic validation
- Unit tests for component testing
- Integration tests for system testing
- Coverage reporting and analysis
- V2 standards compliance validation
- Performance and security testing

Usage:
    python scripts/run_tests.py [OPTIONS]

Examples:
    python scripts/run_tests.py --smoke                    # Run smoke tests only
    python scripts/run_tests.py --unit --coverage          # Run unit tests with coverage
    python scripts/run_tests.py --all --parallel           # Run all tests in parallel
    python scripts/run_tests.py --validate-standards       # Validate V2 standards compliance
"""

import argparse
import sys
import subprocess
import os
from pathlib import Path
from typing import List, Dict, Any
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.conftest import V2StandardsValidator


class TestRunner:
    """Comprehensive test runner for Agent_Cellphone_V2"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.tests_dir = self.project_root / "tests"
        self.src_dir = self.project_root / "src"
        self.results_dir = self.project_root / "test-results"
        self.coverage_dir = self.project_root / "htmlcov"
        
        # Ensure results directory exists
        self.results_dir.mkdir(exist_ok=True)
        
        # V2 standards validator
        self.validator = V2StandardsValidator()
        
        # Test categories and their descriptions
        self.test_categories = {
            "smoke": {
                "description": "Basic functionality validation tests",
                "path": "tests/smoke",
                "marker": "--smoke"
            },
            "unit": {
                "description": "Individual component unit tests",
                "path": "tests/unit", 
                "marker": "--unit"
            },
            "integration": {
                "description": "Component interaction tests",
                "path": "tests/integration",
                "marker": "--integration"
            },
            "performance": {
                "description": "Performance and benchmarking tests",
                "marker": "--performance"
            },
            "security": {
                "description": "Security vulnerability tests",
                "marker": "--security"
            },
            "cli": {
                "description": "Command-line interface tests",
                "marker": "--cli"
            }
        }
    
    def run_command(self, command: List[str], capture_output: bool = True) -> Dict[str, Any]:
        """Run a command and return results"""
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=capture_output,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                'command': ' '.join(command),
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                'command': ' '.join(command),
                'return_code': -1,
                'stdout': '',
                'stderr': 'Command timed out after 5 minutes',
                'success': False
            }
        except Exception as e:
            return {
                'command': ' '.join(command),
                'return_code': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }
    
    def run_smoke_tests(self) -> Dict[str, Any]:
        """Run smoke tests for basic functionality validation"""
        print("🧪 Running Smoke Tests...")
        
        command = [
            "python", "-m", "pytest",
            "tests/smoke/",
            "--markers=smoke",
            "--verbose",
            "--tb=short",
            "--html", str(self.results_dir / "smoke_report.html"),
            "--junitxml", str(self.results_dir / "smoke_junit.xml")
        ]
        
        return self.run_command(command)
    
    def run_unit_tests(self, coverage: bool = True) -> Dict[str, Any]:
        """Run unit tests for individual components"""
        print("🧪 Running Unit Tests...")
        
        command = [
            "python", "-m", "pytest",
            "tests/unit/",
            "--markers=unit",
            "--verbose",
            "--tb=short"
        ]
        
        if coverage:
            command.extend([
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
                "--cov-report=xml:coverage.xml",
                "--cov-fail-under=80"
            ])
        
        command.extend([
            "--html", str(self.results_dir / "unit_report.html"),
            "--junitxml", str(self.results_dir / "unit_junit.xml")
        ])
        
        return self.run_command(command)
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests for component interaction"""
        print("🧪 Running Integration Tests...")
        
        command = [
            "python", "-m", "pytest",
            "tests/integration/",
            "--markers=integration",
            "--verbose",
            "--tb=short",
            "--html", str(self.results_dir / "integration_report.html"),
            "--junitxml", str(self.results_dir / "integration_junit.xml")
        ]
        
        return self.run_command(command)
    
    def run_all_tests(self, parallel: bool = False, coverage: bool = True) -> Dict[str, Any]:
        """Run all tests with optional parallel execution"""
        print("🧪 Running All Tests...")
        
        command = [
            "python", "-m", "pytest",
            "tests/",
            "--verbose",
            "--tb=short"
        ]
        
        if parallel:
            command.extend(["-n", "auto"])
        
        if coverage:
            command.extend([
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
                "--cov-report=xml:coverage.xml",
                "--cov-report=badge:coverage-badge.svg",
                "--cov-fail-under=80"
            ])
        
        command.extend([
            "--html", str(self.results_dir / "all_tests_report.html"),
            "--junitxml", str(self.results_dir / "all_tests_junit.xml")
        ])
        
        return self.run_command(command)
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance and benchmarking tests"""
        print("🧪 Running Performance Tests...")
        
        command = [
            "python", "-m", "pytest",
            "--markers=performance",
            "--benchmark-only",
            "--verbose",
            "--tb=short",
            "--html", str(self.results_dir / "performance_report.html")
        ]
        
        return self.run_command(command)
    
    def run_security_tests(self) -> Dict[str, Any]:
        """Run security vulnerability tests"""
        print("🧪 Running Security Tests...")
        
        # Run bandit security scanner
        bandit_result = self.run_command([
            "bandit", "-r", "src/", "-f", "json", "-o", str(self.results_dir / "bandit_report.json")
        ])
        
        # Run safety dependency checker
        safety_result = self.run_command([
            "safety", "check", "--json", "--output", str(self.results_dir / "safety_report.json")
        ])
        
        return {
            'bandit': bandit_result,
            'safety': safety_result,
            'success': bandit_result['success'] and safety_result['success']
        }
    
    def validate_v2_standards(self) -> Dict[str, Any]:
        """Validate V2 coding standards compliance"""
        print("🔍 Validating V2 Coding Standards...")
        
        results = {
            'line_count_compliance': [],
            'oop_structure_compliance': [],
            'overall_compliance': True
        }
        
        # Check all Python files in src directory
        for py_file in self.src_dir.rglob("*.py"):
            relative_path = py_file.relative_to(self.project_root)
            
            # Validate line count
            line_count_ok = self.validator.validate_line_count(str(py_file))
            results['line_count_compliance'].append({
                'file': str(relative_path),
                'compliant': line_count_ok
            })
            
            # Validate OOP structure
            oop_structure_ok = self.validator.validate_oop_structure(str(py_file))
            results['oop_structure_compliance'].append({
                'file': str(relative_path),
                'compliant': oop_structure_ok
            })
            
            if not line_count_ok or not oop_structure_ok:
                results['overall_compliance'] = False
        
        # Save validation results
        validation_report = self.results_dir / "v2_standards_validation.json"
        with open(validation_report, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def generate_coverage_report(self) -> Dict[str, Any]:
        """Generate comprehensive coverage report"""
        print("📊 Generating Coverage Report...")
        
        command = [
            "coverage", "report",
            "--show-missing",
            "--precision=2"
        ]
        
        return self.run_command(command)
    
    def run_linting(self) -> Dict[str, Any]:
        """Run code quality and style checks"""
        print("🔍 Running Code Quality Checks...")
        
        results = {}
        
        # Run pylint
        pylint_result = self.run_command([
            "pylint", "src/", "--output-format=json", 
            "--output", str(self.results_dir / "pylint_report.json")
        ])
        results['pylint'] = pylint_result
        
        # Run flake8
        flake8_result = self.run_command([
            "flake8", "src/", "--format=json", 
            "--output-file", str(self.results_dir / "flake8_report.json")
        ])
        results['flake8'] = flake8_result
        
        # Run black formatting check
        black_result = self.run_command([
            "black", "--check", "--diff", "src/"
        ])
        results['black'] = black_result
        
        # Run mypy type checking
        mypy_result = self.run_command([
            "mypy", "src/", "--json-report", 
            "--output", str(self.results_dir / "mypy_report.json")
        ])
        results['mypy'] = mypy_result
        
        return results
    
    def print_results(self, results: Dict[str, Any], test_type: str):
        """Print test results in a formatted way"""
        print(f"\n{'='*60}")
        print(f"📋 {test_type.upper()} RESULTS")
        print(f"{'='*60}")
        
        if isinstance(results, dict) and 'success' in results:
            if results['success']:
                print(f"✅ {test_type.title()} completed successfully!")
                if 'stdout' in results and results['stdout']:
                    print(f"Output: {results['stdout'][:200]}...")
            else:
                print(f"❌ {test_type.title()} failed!")
                if 'stderr' in results and results['stderr']:
                    print(f"Error: {results['stderr']}")
                if 'return_code' in results:
                    print(f"Return Code: {results['return_code']}")
        else:
            print(f"📊 {test_type.title()} results:")
            print(json.dumps(results, indent=2))
    
    def run_tests(self, args: argparse.Namespace) -> bool:
        """Main test execution method"""
        all_success = True
        
        try:
            # Run requested test types
            if args.smoke:
                results = self.run_smoke_tests()
                self.print_results(results, "smoke tests")
                all_success = all_success and results['success']
            
            if args.unit:
                results = self.run_unit_tests(coverage=args.coverage)
                self.print_results(results, "unit tests")
                all_success = all_success and results['success']
            
            if args.integration:
                results = self.run_integration_tests()
                self.print_results(results, "integration tests")
                all_success = all_success and results['success']
            
            if args.performance:
                results = self.run_performance_tests()
                self.print_results(results, "performance tests")
                all_success = all_success and results['success']
            
            if args.security:
                results = self.run_security_tests()
                self.print_results(results, "security tests")
                all_success = all_success and results['success']
            
            if args.all:
                results = self.run_all_tests(parallel=args.parallel, coverage=args.coverage)
                self.print_results(results, "all tests")
                all_success = all_success and results['success']
            
            # Additional operations
            if args.lint:
                results = self.run_linting()
                self.print_results(results, "linting")
                all_success = all_success and all(r.get('success', True) for r in results.values())
            
            if args.validate_standards:
                results = self.validate_v2_standards()
                self.print_results(results, "V2 standards validation")
                all_success = all_success and results['overall_compliance']
            
            if args.coverage_report:
                results = self.generate_coverage_report()
                self.print_results(results, "coverage report")
            
            # Print summary
            print(f"\n{'='*60}")
            print("📊 TEST EXECUTION SUMMARY")
            print(f"{'='*60}")
            print(f"Results Directory: {self.results_dir}")
            print(f"Coverage Directory: {self.coverage_dir}")
            print(f"Overall Success: {'✅ PASSED' if all_success else '❌ FAILED'}")
            
            return all_success
            
        except Exception as e:
            print(f"❌ Error during test execution: {e}")
            return False


def main():
    """Main entry point for the test runner"""
    parser = argparse.ArgumentParser(
        description="Comprehensive Test Runner for Agent_Cellphone_V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_tests.py --smoke                    # Run smoke tests only
  python scripts/run_tests.py --unit --coverage          # Run unit tests with coverage
  python scripts/run_tests.py --all --parallel           # Run all tests in parallel
  python scripts/run_tests.py --validate-standards       # Validate V2 standards compliance
  python scripts/run_tests.py --lint                     # Run code quality checks
        """
    )
    
    # Test type options
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    # Execution options
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage reports")
    parser.add_argument("--coverage-report", action="store_true", help="Generate coverage report only")
    
    # Quality options
    parser.add_argument("--lint", action="store_true", help="Run code quality checks")
    parser.add_argument("--validate-standards", action="store_true", help="Validate V2 coding standards")
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # Create test runner and execute
    runner = TestRunner()
    success = runner.run_tests(args)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
