#!/usr/bin/env python3
"""
TDD Testing Runner Script
Agent_Cellphone_V2_Repository TDD Integration Project

This script runs comprehensive TDD tests including:
- Unit tests
- Integration tests
- Selenium WebDriver tests
- FastAPI tests
- Flask tests

Author: Web Development & UI Framework Specialist
License: MIT
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any

class TDDTestRunner:
    """Comprehensive TDD test runner for web development environment"""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.tests_dir = self.repo_root / "tests"
        self.results_dir = self.repo_root / "test_results"
        
        # Create results directory
        self.results_dir.mkdir(exist_ok=True)
        
        # Test configurations
        self.test_suites = {
            "unit": {
                "path": "tests/web/unit",
                "description": "Unit Tests",
                "markers": ["unit", "not slow"]
            },
            "integration": {
                "path": "tests/web/integration", 
                "description": "Integration Tests",
                "markers": ["integration", "not slow"]
            },
            "selenium": {
                "path": "tests/web/selenium",
                "description": "Selenium WebDriver Tests",
                "markers": ["selenium", "web"]
            },
            "flask": {
                "path": "tests/web",
                "description": "Flask Application Tests",
                "markers": ["flask", "web"]
            },
            "fastapi": {
                "path": "tests/web",
                "description": "FastAPI Application Tests", 
                "markers": ["fastapi", "web"]
            },
            "e2e": {
                "path": "tests/web/e2e",
                "description": "End-to-End Tests",
                "markers": ["e2e", "slow"]
            }
        }
    
    def run_test_suite(self, suite_name: str, suite_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a specific test suite"""
        print(f"\n🧪 Running {suite_config['description']}...")
        print(f"📍 Path: {suite_config['path']}")
        print(f"🏷️  Markers: {', '.join(suite_config['markers'])}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            # Build pytest command
            cmd = [
                sys.executable, "-m", "pytest",
                suite_config['path'],
                "-v",
                "--tb=short",
                "--strict-markers",
                "--disable-warnings"
            ]
            
            # Add markers
            for marker in suite_config['markers']:
                cmd.extend(["-m", marker])
            
            # Add coverage if available
            try:
                import pytest_cov
                cmd.extend([
                    "--cov=src",
                    "--cov-report=term-missing",
                    "--cov-report=html:test_results/coverage"
                ])
            except ImportError:
                print("⚠️  Coverage not available, skipping...")
            
            # Run tests
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.repo_root
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Parse results
            test_result = {
                "suite": suite_name,
                "description": suite_config['description'],
                "success": result.returncode == 0,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
            if test_result["success"]:
                print(f"✅ {suite_config['description']} completed successfully in {duration:.2f}s")
            else:
                print(f"❌ {suite_config['description']} failed in {duration:.2f}s")
                if result.stderr:
                    print(f"Error: {result.stderr}")
            
            return test_result
            
        except Exception as e:
            print(f"❌ Error running {suite_config['description']}: {e}")
            return {
                "suite": suite_name,
                "description": suite_config['description'],
                "success": False,
                "duration": 0,
                "error": str(e)
            }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites"""
        print("🚀 Starting Comprehensive TDD Test Suite")
        print(f"📍 Repository: {self.repo_root}")
        print(f"🧪 Test Directory: {self.tests_dir}")
        print("=" * 60)
        
        all_results = {}
        total_start_time = time.time()
        
        # Check if tests directory exists
        if not self.tests_dir.exists():
            print("❌ Tests directory not found. Creating basic test structure...")
            self._create_basic_test_structure()
        
        # Run each test suite
        for suite_name, suite_config in self.test_suites.items():
            if self._should_run_suite(suite_name, suite_config):
                result = self.run_test_suite(suite_name, suite_config)
                all_results[suite_name] = result
            else:
                print(f"⏭️  Skipping {suite_config['description']} (not available)")
        
        total_end_time = time.time()
        total_duration = total_end_time - total_start_time
        
        # Generate summary
        summary = self._generate_summary(all_results, total_duration)
        self._print_summary(summary)
        self._save_results(all_results, summary)
        
        return all_results
    
    def _should_run_suite(self, suite_name: str, suite_config: Dict[str, Any]) -> bool:
        """Check if a test suite should be run"""
        suite_path = self.repo_root / suite_config['path']
        return suite_path.exists() and any(suite_path.glob("*.py"))
    
    def _create_basic_test_structure(self):
        """Create basic test structure if it doesn't exist"""
        basic_tests = {
            "tests/web/unit/test_basic.py": '''
import pytest

def test_basic_functionality():
    """Basic test to verify pytest is working"""
    assert True

def test_math():
    """Simple math test"""
    assert 2 + 2 == 4
    assert 3 * 3 == 9

class TestBasicClass:
    """Basic test class"""
    
    def test_class_method(self):
        """Test class method"""
        assert hasattr(self, 'test_class_method')
''',
            "tests/web/integration/test_integration.py": '''
import pytest

def test_integration_basic():
    """Basic integration test"""
    assert True

@pytest.mark.integration
def test_marked_integration():
    """Marked integration test"""
    assert True
''',
            "tests/web/selenium/test_selenium_basic.py": '''
import pytest

@pytest.mark.selenium
def test_selenium_import():
    """Test that Selenium can be imported"""
    try:
        from selenium import webdriver
        assert webdriver is not None
    except ImportError:
        pytest.skip("Selenium not available")

@pytest.mark.web
def test_web_automation_concept():
    """Test web automation concepts"""
    automation_steps = ["navigate", "find", "act", "verify"]
    assert len(automation_steps) == 4
''',
            "tests/web/e2e/test_e2e_basic.py": '''
import pytest

@pytest.mark.e2e
@pytest.mark.slow
def test_e2e_basic():
    """Basic end-to-end test"""
    assert True

@pytest.mark.e2e
def test_e2e_workflow():
    """Test end-to-end workflow"""
    workflow_steps = ["setup", "execute", "verify", "cleanup"]
    assert len(workflow_steps) == 4
'''
        }
        
        for file_path, content in basic_tests.items():
            full_path = self.repo_root / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w') as f:
                f.write(content)
            
            print(f"✅ Created: {file_path}")
    
    def _generate_summary(self, results: Dict[str, Any], total_duration: float) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = len(results)
        successful_tests = sum(1 for r in results.values() if r.get("success", False))
        failed_tests = total_tests - successful_tests
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TDD Test Suite Summary")
        print("=" * 60)
        print(f"📅 Timestamp: {summary['timestamp']}")
        print(f"⏱️  Total Duration: {summary['total_duration']:.2f}s")
        print(f"🧪 Total Test Suites: {summary['total_tests']}")
        print(f"✅ Successful: {summary['successful_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        
        if summary['success_rate'] == 100:
            print("\n🎉 All tests passed! TDD environment is ready!")
        elif summary['success_rate'] >= 80:
            print("\n👍 Most tests passed. Minor issues to address.")
        else:
            print("\n⚠️  Several tests failed. Review and fix issues.")
    
    def _save_results(self, results: Dict[str, Any], summary: Dict[str, Any]):
        """Save test results to file"""
        import json
        
        results_file = self.results_dir / f"tdd_test_results_{int(time.time())}.json"
        
        output_data = {
            "summary": summary,
            "results": results
        }
        
        with open(results_file, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {results_file}")

def main():
    """Main function to run TDD tests"""
    try:
        runner = TDDTestRunner()
        results = runner.run_all_tests()
        
        # Exit with appropriate code
        summary = runner._generate_summary(results, 0)
        if summary['failed_tests'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
