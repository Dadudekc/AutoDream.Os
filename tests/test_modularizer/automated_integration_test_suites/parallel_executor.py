"""
Parallel and sequential execution for automated integration test suites.
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import TestSuiteResult


class ParallelTestSuiteExecutor:
    """Handles parallel and sequential execution of test suites."""
    
    def __init__(self, main_executor):
        self.main_executor = main_executor
        self.logger = logging.getLogger(__name__)
    
    def run_suites_parallel(self, suite_ids: List[str]) -> List[TestSuiteResult]:
        """Run test suites in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.main_executor.max_parallel_suites) as executor:
            future_to_suite = {
                executor.submit(self.main_executor.run_test_suite, suite_id): suite_id
                for suite_id in suite_ids
            }
            
            for future in as_completed(future_to_suite):
                suite_id = future_to_suite[future]
                try:
                    result = future.result()
                    results.append(result)
                    self.logger.info(f"✅ {suite_id}: {result.status}")
                except Exception as e:
                    self.logger.error(f"❌ {suite_id}: Failed with error: {e}")
                    # Create error result
                    error_result = TestSuiteResult(
                        suite_id=suite_id,
                        suite_name=self.main_executor.test_suites[suite_id].name,
                        execution_start=datetime.now(),
                        execution_end=datetime.now(),
                        total_tests=0,
                        passed_tests=0,
                        failed_tests=0,
                        error_tests=1,
                        skipped_tests=0,
                        execution_time=0.0,
                        status="error",
                        test_results=[],
                        summary={},
                        error_details=str(e)
                    )
                    results.append(error_result)
        
        return results
    
    def run_suites_sequential(self, suite_ids: List[str]) -> List[TestSuiteResult]:
        """Run test suites sequentially."""
        results = []
        
        for suite_id in suite_ids:
            try:
                result = self.main_executor.run_test_suite(suite_id)
                results.append(result)
                self.logger.info(f"✅ {suite_id}: {result.status}")
            except Exception as e:
                self.logger.error(f"❌ {suite_id}: Failed with error: {e}")
                # Create error result
                error_result = TestSuiteResult(
                    suite_id=suite_id,
                    suite_name=self.main_executor.test_suites[suite_id].name,
                    execution_start=datetime.now(),
                    execution_end=datetime.now(),
                    total_tests=0,
                    passed_tests=0,
                    failed_tests=0,
                    error_tests=1,
                    skipped_tests=0,
                    execution_time=0.0,
                    status="error",
                    test_results=[],
                    summary={},
                    error_details=str(e)
                )
                results.append(error_result)
        
        return results
