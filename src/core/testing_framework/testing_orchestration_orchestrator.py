#!/usr/bin/env python3
"""
Testing Orchestration Orchestrator - V2 Testing Framework Main Orchestrator
===========================================================================

Main orchestrator that coordinates test suites, runners, and executors.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import time
from typing import Dict, Any, List, Optional

from src.utils.stability_improvements import stability_manager, safe_import

# Import our types and core classes
try:
    from .testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from .testing_orchestration_core import IntegrationTestSuite, TestSuiteResult
    from .testing_orchestration_runner import IntegrationTestRunner
    from .testing_orchestration_executor import TestExecutor, ExecutionConfig
except ImportError:
    from testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from testing_orchestration_core import IntegrationTestSuite, TestSuiteResult
    from testing_orchestration_runner import IntegrationTestRunner
    from testing_orchestration_executor import TestExecutor, ExecutionConfig


class TestOrchestrator:
    """Main orchestrator for the testing framework."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {
            "max_parallel_suites": 3,
            "generate_reports": True,
            "cleanup_after_execution": True,
            "continue_on_failure": True,
            "timeout_per_suite": 1800.0,  # 30 minutes
            "retry_failed_suites": False,
            "max_retries": 1
        }
        
        # Initialize components
        self.runner = IntegrationTestRunner()
        self.executor = TestExecutor()
        self.logger = logging.getLogger(__name__)
        
        # Orchestration state
        self.active_suites: Dict[str, Dict[str, Any]] = {}
        self.orchestration_history: List[Dict[str, Any]] = []
    
    def add_test_suite(self, suite: IntegrationTestSuite) -> None:
        """Add a test suite to the orchestrator."""
        if not isinstance(suite, IntegrationTestSuite):
            raise ValueError("Suite must be an instance of IntegrationTestSuite")
        
        self.runner.add_test_suite(suite)
        self.logger.info(f"Added test suite '{suite.name}' to orchestrator")
    
    def remove_test_suite(self, suite_name: str) -> bool:
        """Remove a test suite from the orchestrator."""
        success = self.runner.remove_test_suite(suite_name)
        if success:
            self.logger.info(f"Removed test suite '{suite_name}' from orchestrator")
        return success
    
    async def orchestrate_suite(self, suite_name: str) -> Optional[Dict[str, Any]]:
        """Orchestrate execution of a single test suite."""
        if suite_name not in self.runner.test_suites:
            self.logger.error(f"Test suite '{suite_name}' not found")
            return None
        
        suite = self.runner.test_suites[suite_name]
        start_time = time.time()
        
        self.logger.info(f"Orchestrating test suite '{suite_name}'")
        
        # Record orchestration start
        self.active_suites[suite_name] = {
            "start_time": start_time,
            "status": "running"
        }
        
        try:
            # Execute the suite
            results = await self.executor.execute_test_suite(suite)
            end_time = time.time()
            duration = end_time - start_time
            
            # Generate summary
            summary = self._generate_suite_summary(suite_name, results, duration)
            
            # Record successful orchestration
            self.orchestration_history.append({
                "suite_name": suite_name,
                "status": "completed",
                "results": results,
                "summary": summary,
                "duration": duration,
                "timestamp": time.time()
            })
            
            self.logger.info(f"Test suite '{suite_name}' orchestration completed")
            return summary
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            self.logger.error(f"Error orchestrating test suite '{suite_name}': {e}")
            
            # Record failed orchestration
            self.orchestration_history.append({
                "suite_name": suite_name,
                "status": "failed",
                "error": str(e),
                "duration": duration,
                "timestamp": time.time()
            })
            
            return {
                "error": str(e),
                "suite_name": suite_name,
                "status": "failed"
            }
        
        finally:
            # Cleanup active suite record
            if suite_name in self.active_suites:
                del self.active_suites[suite_name]
    
    async def orchestrate_multiple_suites(self, suite_names: List[str]) -> Dict[str, Any]:
        """Orchestrate execution of multiple test suites."""
        if not suite_names:
            self.logger.warning("No suite names provided for orchestration")
            return {"status": "no_suites"}
        
        self.logger.info(f"Orchestrating {len(suite_names)} test suites")
        
        results = {}
        for suite_name in suite_names:
            try:
                suite_result = await self.orchestrate_suite(suite_name)
                if suite_result:
                    results[suite_name] = suite_result
                
                # Check if we should continue on failure
                if not self.config["continue_on_failure"] and suite_result and suite_result.get("status") == "failed":
                    self.logger.warning(f"Stopping orchestration due to failure in suite '{suite_name}'")
                    break
                    
            except Exception as e:
                self.logger.error(f"Unexpected error orchestrating suite '{suite_name}': {e}")
                if not self.config["continue_on_failure"]:
                    break
        
        # Generate global summary
        global_summary = self._generate_global_summary(results)
        
        self.logger.info(f"Multiple test suites orchestration completed: {len(results)} suites")
        return global_summary
    
    def _generate_suite_summary(self, suite_name: str, results: List[TestResult], duration: float) -> Dict[str, Any]:
        """Generate summary for a test suite."""
        if not results:
            return {"suite_name": suite_name, "status": "no_results"}
        
        total = len(results)
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        error = sum(1 for r in results if r.status == TestStatus.ERROR)
        timeout = sum(1 for r in results if r.status == TestStatus.TIMEOUT)
        
        success_rate = (passed / total * 100) if total > 0 else 0.0
        
        return {
            "suite_name": suite_name,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "error": error,
            "timeout": timeout,
            "success_rate": success_rate,
            "execution_time": duration,
            "timestamp": time.time()
        }
    
    def _generate_global_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate global summary for multiple suites."""
        if not results:
            return {"status": "no_results"}
        
        total_suites = len(results)
        successful_suites = sum(1 for r in results.values() if r.get("status") != "failed")
        failed_suites = total_suites - successful_suites
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for suite_result in results.values():
            if "total_tests" in suite_result:
                total_tests += suite_result["total_tests"]
                total_passed += suite_result.get("passed", 0)
                total_failed += suite_result.get("failed", 0)
        
        return {
            "total_suites": total_suites,
            "successful_suites": successful_suites,
            "failed_suites": failed_suites,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "overall_success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0.0,
            "suite_results": results,
            "timestamp": time.time()
        }
    
    def get_orchestration_summary(self) -> Dict[str, Any]:
        """Get summary of all orchestrations."""
        if not self.orchestration_history:
            return {"status": "no_orchestrations"}
        
        total_orchestrations = len(self.orchestration_history)
        successful_orchestrations = sum(1 for h in self.orchestration_history if h.get("status") == "completed")
        failed_orchestrations = total_orchestrations - successful_orchestrations
        
        return {
            "total_orchestrations": total_orchestrations,
            "successful_orchestrations": successful_orchestrations,
            "failed_orchestrations": failed_orchestrations,
            "active_suites": len(self.active_suites),
            "last_orchestration": max(h["timestamp"] for h in self.orchestration_history) if self.orchestration_history else None
        }
    
    def get_active_suites(self) -> Dict[str, Dict[str, Any]]:
        """Get currently active suites."""
        return self.active_suites.copy()
    
    def get_orchestration_history(self) -> List[Dict[str, Any]]:
        """Get orchestration history."""
        return self.orchestration_history.copy()
    
    def clear_history(self) -> None:
        """Clear orchestration history."""
        self.orchestration_history.clear()
        self.active_suites.clear()
        self.logger.info("Orchestration history cleared")
    
    def get_config(self) -> Dict[str, Any]:
        """Get orchestrator configuration."""
        return self.config.copy()
    
    def update_config(self, **kwargs) -> None:
        """Update orchestrator configuration."""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                self.logger.info(f"Updated config: {key} = {value}")
            else:
                self.logger.warning(f"Unknown config key: {key}")
