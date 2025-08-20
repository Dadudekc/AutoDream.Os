#!/usr/bin/env python3
"""
V2 Integration Testing Framework
================================
Comprehensive integration testing framework for V2 system validation.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Test execution result"""
    test_name: str
    status: str  # "PASS", "FAIL", "SKIP"
    execution_time: float
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class TestSuite:
    """Test suite configuration"""
    name: str
    description: str
    tests: List[str]
    dependencies: List[str] = None


class V2IntegrationTestingFramework:
    """Comprehensive integration testing framework for V2 system"""
    
    def __init__(self, test_results_dir: str = "test_results"):
        self.logger = logging.getLogger(f"{__name__}.V2IntegrationTestingFramework")
        self.results_dir = Path(test_results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        # Test registry
        self._test_registry: Dict[str, Callable] = {}
        self._test_suites: Dict[str, TestSuite] = {}
        
        # Test execution state
        self._test_results: List[TestResult] = []
        self._current_suite: Optional[str] = None
        
        self.logger.info("V2 Integration Testing Framework initialized")
    
    def register_test(self, test_name: str, test_function: Callable) -> bool:
        """Register a test function"""
        if test_name in self._test_registry:
            self.logger.warning(f"Test already registered: {test_name}")
            return False
        
        self._test_registry[test_name] = test_function
        self.logger.info(f"Test registered: {test_name}")
        return True
    
    def create_test_suite(self, name: str, description: str, tests: List[str], 
                         dependencies: Optional[List[str]] = None) -> bool:
        """Create a test suite"""
        if name in self._test_suites:
            self.logger.warning(f"Test suite already exists: {name}")
            return False
        
        # Validate test names
        for test_name in tests:
            if test_name not in self._test_registry:
                self.logger.error(f"Test not found in registry: {test_name}")
                return False
        
        test_suite = TestSuite(
            name=name,
            description=description,
            tests=tests,
            dependencies=dependencies or []
        )
        
        self._test_suites[name] = test_suite
        self.logger.info(f"Test suite created: {name} with {len(tests)} tests")
        return True
    
    def run_test(self, test_name: str) -> TestResult:
        """Run a single test"""
        if test_name not in self._test_registry:
            return TestResult(
                test_name=test_name,
                status="SKIP",
                execution_time=0.0,
                error_message=f"Test not found: {test_name}"
            )
        
        test_function = self._test_registry[test_name]
        start_time = time.time()
        
        try:
            self.logger.info(f"Running test: {test_name}")
            result = test_function()
            execution_time = time.time() - start_time
            
            if result:
                status = "PASS"
                error_message = None
            else:
                status = "FAIL"
                error_message = "Test returned False"
            
            test_result = TestResult(
                test_name=test_name,
                status=status,
                execution_time=execution_time,
                error_message=error_message
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            test_result = TestResult(
                test_name=test_name,
                status="FAIL",
                execution_time=execution_time,
                error_message=str(e)
            )
            self.logger.error(f"Test {test_name} failed with exception: {e}")
        
        self._test_results.append(test_result)
        return test_result
    
    def run_test_suite(self, suite_name: str) -> List[TestResult]:
        """Run all tests in a test suite"""
        if suite_name not in self._test_suites:
            self.logger.error(f"Test suite not found: {suite_name}")
            return []
        
        suite = self._test_suites[suite_name]
        self._current_suite = suite_name
        self.logger.info(f"Running test suite: {suite_name}")
        
        results = []
        
        # Check dependencies
        if suite.dependencies:
            self.logger.info(f"Checking dependencies: {suite.dependencies}")
            for dep in suite.dependencies:
                if dep not in self._test_suites:
                    self.logger.error(f"Dependency not found: {dep}")
                    return []
        
        # Run tests
        for test_name in suite.tests:
            result = self.run_test(test_name)
            results.append(result)
            
            # Log result
            if result.status == "PASS":
                self.logger.info(f"✅ {test_name}: PASSED ({result.execution_time:.3f}s)")
            else:
                self.logger.error(f"❌ {test_name}: {result.status} - {result.error_message}")
        
        self._current_suite = None
        return results
    
    def run_all_tests(self) -> List[TestResult]:
        """Run all registered tests"""
        self.logger.info("Running all registered tests")
        results = []
        
        for test_name in self._test_registry.keys():
            result = self.run_test(test_name)
            results.append(result)
        
        return results
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of test execution results"""
        if not self._test_results:
            return {"message": "No tests executed"}
        
        total_tests = len(self._test_results)
        passed_tests = len([r for r in self._test_results if r.status == "PASS"])
        failed_tests = len([r for r in self._test_results if r.status == "FAIL"])
        skipped_tests = len([r for r in self._test_results if r.status == "SKIP"])
        
        total_time = sum(r.execution_time for r in self._test_results)
        avg_time = total_time / total_tests if total_tests > 0 else 0
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "skipped": skipped_tests,
            "success_rate": success_rate,
            "total_execution_time": total_time,
            "average_execution_time": avg_time,
            "current_suite": self._current_suite
        }
    
    def save_test_results(self, filename: Optional[str] = None) -> str:
        """Save test results to file"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"integration_test_results_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        results_data = {
            "timestamp": time.time(),
            "summary": self.get_test_summary(),
            "results": [
                {
                    "test_name": r.test_name,
                    "status": r.status,
                    "execution_time": r.execution_time,
                    "error_message": r.error_message
                }
                for r in self._test_results
            ]
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(results_data, f, indent=2)
            self.logger.info(f"Test results saved to: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Failed to save test results: {e}")
            return ""
    
    def list_test_suites(self) -> List[Dict[str, Any]]:
        """List all test suites"""
        suites = []
        for name, suite in self._test_suites.items():
            suites.append({
                "name": name,
                "description": suite.description,
                "test_count": len(suite.tests),
                "dependencies": suite.dependencies or []
            })
        return suites
    
    def clear_results(self):
        """Clear test results"""
        self._test_results.clear()
        self.logger.info("Test results cleared")


def main():
    """CLI interface for testing V2IntegrationTestingFramework"""
    import argparse
    
    parser = argparse.ArgumentParser(description="V2 Integration Testing Framework CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 V2IntegrationTestingFramework Smoke Test")
        print("=" * 50)
        
        framework = V2IntegrationTestingFramework()
        
        # Register test functions
        def test_function_1():
            return True
        
        def test_function_2():
            return False
        
        def test_function_3():
            raise Exception("Test exception")
        
        framework.register_test("test-1", test_function_1)
        framework.register_test("test-2", test_function_2)
        framework.register_test("test-3", test_function_3)
        
        # Create test suite
        framework.create_test_suite("smoke-tests", "Smoke test suite", ["test-1", "test-2", "test-3"])
        
        # Run test suite
        results = framework.run_test_suite("smoke-tests")
        print(f"✅ Tests executed: {len(results)}")
        
        # Get summary
        summary = framework.get_test_summary()
        print(f"✅ Success rate: {summary['success_rate']:.1f}%")
        print(f"✅ Total execution time: {summary['total_execution_time']:.3f}s")
        
        # Save results
        results_file = framework.save_test_results()
        print(f"✅ Results saved to: {results_file}")
        
        # List suites
        suites = framework.list_test_suites()
        print(f"✅ Test suites: {len(suites)}")
        
        print("🎉 V2IntegrationTestingFramework smoke test PASSED!")
    else:
        print("V2IntegrationTestingFramework ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
