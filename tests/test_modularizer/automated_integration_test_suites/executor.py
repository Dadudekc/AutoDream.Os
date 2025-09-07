"""
Test suite executor for automated integration test suites.
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from .models import TestSuiteConfig, TestSuiteResult, TestSuiteCategory, TestExecutionMode
from .config import DEFAULT_TEST_SUITES
from .parallel_executor import ParallelTestSuiteExecutor


class AutomatedIntegrationTestSuites:
    """Main class for managing and executing automated integration test suites."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = self._setup_logging()
        self.test_suites: Dict[str, TestSuiteConfig] = {}
        self.test_suite_results: List[TestSuiteResult] = []
        self.active_suites: Dict[str, datetime] = {}
        
        # Configuration
        self.max_parallel_suites = 4
        self.max_suite_retries = 3
        self.retry_failed_suites = True
        self.suite_timeout = 600
        
        # Initialize parallel executor
        self.parallel_executor = ParallelTestSuiteExecutor(self)
        
        # Load test suite configurations
        self._load_test_suites(config_file)
        
        self.logger.info(f"🧪 Automated Integration Test Suites initialized with {len(self.test_suites)} test suites")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_test_suites(self, config_file: Optional[str] = None):
        """Load test suite configurations."""
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                configs = json.load(f)
        else:
            configs = DEFAULT_TEST_SUITES
        
        for suite_id, config in configs.items():
            try:
                # Convert dict to TestSuiteConfig
                suite_config = TestSuiteConfig(**config)
                self.test_suites[suite_id] = suite_config
                self.logger.info(f"✅ Loaded test suite: {suite_id}")
            except Exception as e:
                self.logger.error(f"❌ Failed to load test suite {suite_id}: {e}")
    
    def run_test_suite(self, suite_id: str, retry_count: int = 0) -> TestSuiteResult:
        """Run a specific test suite."""
        if suite_id not in self.test_suites:
            raise ValueError(f"Test suite {suite_id} not found")
        
        suite_config = self.test_suites[suite_id]
        self.logger.info(f"🚀 Starting test suite: {suite_id}")
        
        # Check dependencies
        if not self._check_dependencies(suite_id):
            raise RuntimeError(f"Dependencies not met for test suite {suite_id}")
        
        # Mark as active
        self.active_suites[suite_id] = datetime.now()
        
        # Initialize result
        execution_start = datetime.now()
        suite_result = TestSuiteResult(
            suite_id=suite_id,
            suite_name=suite_config.name,
            execution_start=execution_start,
            execution_end=execution_start,
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            error_tests=0,
            skipped_tests=0,
            execution_time=0.0,
            status="running",
            test_results=[],
            summary={}
        )
        
        try:
            # Execute test suite
            test_results = self._execute_suite_tests(suite_config)
            
            # Calculate results
            total_tests = len(test_results)
            passed_tests = len([r for r in test_results if r.get('status') == 'passed'])
            failed_tests = len([r for r in test_results if r.get('status') == 'failed'])
            error_tests = len([r for r in test_results if r.get('status') == 'error'])
            skipped_tests = len([r for r in test_results if r.get('status') == 'skipped'])
            
            # Determine overall status
            if failed_tests > 0 or error_tests > 0:
                status = "failed"
            elif passed_tests == total_tests:
                status = "passed"
            else:
                status = "partial"
            
            # Update result
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            suite_result.execution_end = execution_end
            suite_result.execution_time = execution_time
            suite_result.total_tests = total_tests
            suite_result.passed_tests = passed_tests
            suite_result.failed_tests = failed_tests
            suite_result.error_tests = error_tests
            suite_result.skipped_tests = skipped_tests
            suite_result.status = status
            suite_result.test_results = test_results
            suite_result.summary = self._generate_suite_summary(test_results)
            
            self.logger.info(f"✅ Test suite {suite_id} completed: {status}")
            
        except Exception as e:
            self.logger.error(f"❌ Test suite {suite_id} failed: {e}")
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            suite_result.execution_end = execution_end
            suite_result.execution_time = execution_time
            suite_result.status = "error"
            suite_result.error_details = str(e)
            
            # Retry logic
            if retry_count < self.max_suite_retries and self.retry_failed_suites:
                self.logger.info(f"🔄 Retrying test suite {suite_id} (attempt {retry_count + 1})")
                return self.run_test_suite(suite_id, retry_count + 1)
        
        finally:
            # Cleanup if required
            if suite_config.cleanup_required:
                self._cleanup_suite(suite_config)
            
            # Remove from active suites
            if suite_id in self.active_suites:
                del self.active_suites[suite_id]
        
        # Store result
        self.test_suite_results.append(suite_result)
        
        return suite_result
    
    def _check_dependencies(self, suite_id: str) -> bool:
        """Check if all dependencies are met for a test suite."""
        suite_config = self.test_suites[suite_id]
        
        for dep_id in suite_config.dependencies:
            if dep_id not in self.test_suites:
                self.logger.error(f"❌ Dependency {dep_id} not found for {suite_id}")
                return False
            
            # Check if dependency passed
            dep_results = [r for r in self.test_suite_results if r.suite_id == dep_id]
            if not dep_results or dep_results[-1].status != "passed":
                self.logger.warning(f"⚠️ Dependency {dep_id} not passed for {suite_id}")
                return False
        
        return True
    
    def _execute_suite_tests(self, suite_config: TestSuiteConfig) -> List[Dict[str, Any]]:
        """Execute tests for a specific suite."""
        # This is a placeholder implementation
        # In a real system, this would execute actual tests
        self.logger.info(f"🧪 Executing tests for suite: {suite_config.name}")
        
        # Simulate test execution
        time.sleep(1)
        
        # Return mock results
        return [
            {"test_id": "test_1", "status": "passed", "duration": 0.5},
            {"test_id": "test_2", "status": "passed", "duration": 0.3},
            {"test_id": "test_3", "status": "skipped", "duration": 0.0}
        ]
    
    def _generate_suite_summary(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary for test suite results."""
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.get('status') == 'passed'])
        failed_tests = len([r for r in test_results if r.get('status') == 'failed'])
        error_tests = len([r for r in test_results if r.get('status') == 'error'])
        skipped_tests = len([r for r in test_results if r.get('status') == 'skipped'])
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "skipped_tests": skipped_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
    
    def _cleanup_suite(self, suite_config: TestSuiteConfig):
        """Cleanup after test suite execution."""
        self.logger.info(f"🧹 Cleaning up after suite: {suite_config.name}")
        # Placeholder for cleanup logic
    
    def run_all_test_suites(self, suite_ids: Optional[List[str]] = None, 
                           parallel: bool = True) -> List[TestSuiteResult]:
        """Run all test suites or specified ones."""
        suites_to_run = suite_ids or list(self.test_suites.keys())
        self.logger.info(f"🚀 Starting execution of {len(suites_to_run)} test suites")
        
        if parallel:
            return self.parallel_executor.run_suites_parallel(suites_to_run)
        else:
            return self.parallel_executor.run_suites_sequential(suites_to_run)
    
    def get_suite_summary(self) -> Dict[str, Any]:
        """Get summary of all test suite results."""
        if not self.test_suite_results:
            return {
                "total_suites": 0,
                "passed_suites": 0,
                "failed_suites": 0,
                "error_suites": 0,
                "partial_suites": 0,
                "skipped_suites": 0,
                "suite_pass_rate": 0.0,
                "total_tests": 0,
                "test_pass_rate": 0.0
            }
        
        total_suites = len(self.test_suite_results)
        passed_suites = len([r for r in self.test_suite_results if r.status == "passed"])
        failed_suites = len([r for r in self.test_suite_results if r.status == "failed"])
        error_suites = len([r for r in self.test_suite_results if r.status == "error"])
        partial_suites = len([r for r in self.test_suite_results if r.status == "partial"])
        skipped_suites = len([r for r in self.test_suite_results if r.status == "skipped"])
        
        suite_pass_rate = (passed_suites / total_suites * 100) if total_suites > 0 else 0
        
        total_tests = sum(r.total_tests for r in self.test_suite_results)
        total_passed_tests = sum(r.passed_tests for r in self.test_suite_results)
        test_pass_rate = (total_passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_suites": total_suites,
            "passed_suites": passed_suites,
            "failed_suites": failed_suites,
            "error_suites": error_suites,
            "partial_suites": partial_suites,
            "skipped_suites": skipped_suites,
            "suite_pass_rate": suite_pass_rate,
            "total_tests": total_tests,
            "test_pass_rate": test_pass_rate
        }
    
    def export_suite_results(self, format_type: str = "json") -> str:
        """Export test suite results in specified format."""
        from .reporting import TestSuiteReporter
        
        reporter = TestSuiteReporter(self.test_suite_results)
        return reporter.export_suite_results(format_type)
