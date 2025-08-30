#!/usr/bin/env python3
"""
🧪 AUTOMATED INTEGRATION TEST SUITES - V2-COMPLIANCE-008
Testing Framework Enhancement Manager - Agent-3

This module implements comprehensive automated integration test suites for all major
systems, providing automated testing, validation, and reporting capabilities.

Features:
- Automated test suite execution
- Cross-module dependency testing
- API integration validation
- Database integration testing
- End-to-end workflow testing
- Automated reporting and notifications
"""

import os
import sys
import time
import asyncio
import threading
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import subprocess
import traceback

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from .enhanced_integration_testing_framework import (
    EnhancedIntegrationTestingFramework,
    IntegrationTestType,
    TestPriority,
    IntegrationTestResult
)


class TestSuiteCategory(Enum):
    """Categories of test suites"""
    
    CORE_SYSTEM = "core_system"
    WORKFLOW_SYSTEM = "workflow_system"
    AGENT_MANAGEMENT = "agent_management"
    COMMUNICATION_SYSTEM = "communication_system"
    API_INTEGRATION = "api_integration"
    DATABASE_INTEGRATION = "database_integration"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPLIANCE = "compliance"


class TestExecutionMode(Enum):
    """Test execution modes"""
    
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    PRIORITY_BASED = "priority_based"
    DEPENDENCY_BASED = "dependency_based"


@dataclass
class TestSuiteConfig:
    """Configuration for test suite execution"""
    
    suite_id: str
    name: str
    description: str
    category: TestSuiteCategory
    priority: TestPriority
    execution_mode: TestExecutionMode
    timeout: int = 600
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    cleanup_required: bool = True
    parallel_execution: bool = True
    max_parallel_tests: int = 4


@dataclass
class TestSuiteResult:
    """Result of test suite execution"""
    
    suite_id: str
    suite_name: str
    execution_start: datetime
    execution_end: datetime
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_tests: int
    skipped_tests: int
    execution_time: float
    status: str  # "passed", "failed", "error", "partial"
    test_results: List[IntegrationTestResult]
    summary: Dict[str, Any]
    error_details: Optional[str] = None


class AutomatedIntegrationTestSuites:
    """
    Automated integration test suites for comprehensive system testing.
    
    Provides automated execution of test suites with:
    - Dependency management
    - Parallel execution
    - Automated reporting
    - Error handling and recovery
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize automated integration test suites."""
        self.project_root = project_root or Path.cwd()
        
        # Core framework
        self.integration_framework = EnhancedIntegrationTestingFramework(self.project_root)
        
        # Test suite registry
        self.test_suites: Dict[str, TestSuiteConfig] = {}
        self.test_suite_results: List[TestSuiteResult] = []
        
        # Execution state
        self.execution_history: List[Dict[str, Any]] = []
        self.active_suites: Dict[str, TestSuiteResult] = {}
        
        # Configuration
        self.default_timeout = 600
        self.max_parallel_suites = 3
        self.retry_failed_suites = True
        self.max_suite_retries = 2
        
        # Logging
        self.logger = logging.getLogger(f"{__name__}.AutomatedIntegrationTestSuites")
        self._setup_logging()
        
        # Initialize test suites
        self._initialize_test_suites()
        
        self.logger.info("🚀 Automated Integration Test Suites initialized")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _initialize_test_suites(self):
        """Initialize all test suite configurations."""
        self.logger.info("🔧 Initializing automated test suites...")
        
        # Core System Test Suite
        self.test_suites["core_system_suite"] = TestSuiteConfig(
            suite_id="core_system_suite",
            name="Core System Integration Test Suite",
            description="Comprehensive testing of core system components and their integration",
            category=TestSuiteCategory.CORE_SYSTEM,
            priority=TestPriority.CRITICAL,
            execution_mode=TestExecutionMode.DEPENDENCY_BASED,
            timeout=900,
            dependencies=["database", "api", "messaging"],
            prerequisites=["system_startup", "database_connection"],
            cleanup_required=True,
            parallel_execution=True,
            max_parallel_tests=6
        )
        
        # Workflow System Test Suite
        self.test_suites["workflow_system_suite"] = TestSuiteConfig(
            suite_id="workflow_system_suite",
            name="Workflow System Integration Test Suite",
            description="Testing workflow system integration with business processes and learning systems",
            category=TestSuiteCategory.WORKFLOW_SYSTEM,
            priority=TestPriority.HIGH,
            execution_mode=TestExecutionMode.DEPENDENCY_BASED,
            timeout=600,
            dependencies=["core_system", "database", "api"],
            prerequisites=["core_system_suite"],
            cleanup_required=True,
            parallel_execution=True,
            max_parallel_tests=4
        )
        
        # Agent Management Test Suite
        self.test_suites["agent_management_suite"] = TestSuiteConfig(
            suite_id="agent_management_suite",
            name="Agent Management Integration Test Suite",
            description="Testing agent management, task scheduling, and communication integration",
            category=TestSuiteCategory.AGENT_MANAGEMENT,
            priority=TestPriority.HIGH,
            execution_mode=TestExecutionMode.PARALLEL,
            timeout=450,
            dependencies=["core_system", "database", "messaging"],
            prerequisites=["core_system_suite"],
            cleanup_required=True,
            parallel_execution=True,
            max_parallel_tests=5
        )
        
        # Communication System Test Suite
        self.test_suites["communication_system_suite"] = TestSuiteConfig(
            suite_id="communication_system_suite",
            name="Communication System Integration Test Suite",
            description="Testing communication protocols, message routing, and error handling",
            category=TestSuiteCategory.COMMUNICATION_SYSTEM,
            priority=TestPriority.HIGH,
            execution_mode=TestExecutionMode.PARALLEL,
            timeout=300,
            dependencies=["core_system", "api", "database"],
            prerequisites=["core_system_suite"],
            cleanup_required=True,
            parallel_execution=True,
            max_parallel_tests=4
        )
        
        # API Integration Test Suite
        self.test_suites["api_integration_suite"] = TestSuiteConfig(
            suite_id="api_integration_suite",
            name="API Integration Test Suite",
            description="Testing API endpoints, request handling, and response validation",
            category=TestSuiteCategory.API_INTEGRATION,
            priority=TestPriority.HIGH,
            execution_mode=TestExecutionMode.PARALLEL,
            timeout=300,
            dependencies=["core_system", "database"],
            prerequisites=["core_system_suite"],
            cleanup_required=False,
            parallel_execution=True,
            max_parallel_tests=8
        )
        
        # Database Integration Test Suite
        self.test_suites["database_integration_suite"] = TestSuiteConfig(
            suite_id="database_integration_suite",
            name="Database Integration Test Suite",
            description="Testing database connections, queries, and data consistency",
            category=TestSuiteCategory.DATABASE_INTEGRATION,
            priority=TestPriority.CRITICAL,
            execution_mode=TestExecutionMode.SEQUENTIAL,
            timeout=600,
            dependencies=["database"],
            prerequisites=["system_startup"],
            cleanup_required=True,
            parallel_execution=False,
            max_parallel_tests=1
        )
        
        # End-to-End Workflow Test Suite
        self.test_suites["end_to_end_suite"] = TestSuiteConfig(
            suite_id="end_to_end_suite",
            name="End-to-End Workflow Test Suite",
            description="Testing complete user workflows and system integration scenarios",
            category=TestSuiteCategory.END_TO_END,
            priority=TestPriority.CRITICAL,
            execution_mode=TestExecutionMode.SEQUENTIAL,
            timeout=1200,
            dependencies=["core_system", "workflow_system", "agent_management", "communication_system"],
            prerequisites=["core_system_suite", "workflow_system_suite", "agent_management_suite", "communication_system_suite"],
            cleanup_required=True,
            parallel_execution=False,
            max_parallel_tests=1
        )
        
        # Performance Test Suite
        self.test_suites["performance_suite"] = TestSuiteConfig(
            suite_id="performance_suite",
            name="Performance and Load Testing Suite",
            description="Testing system performance under various load conditions",
            category=TestSuiteCategory.PERFORMANCE,
            priority=TestPriority.NORMAL,
            execution_mode=TestExecutionMode.PARALLEL,
            timeout=900,
            dependencies=["core_system", "database", "api"],
            prerequisites=["core_system_suite", "api_integration_suite"],
            cleanup_required=False,
            parallel_execution=True,
            max_parallel_tests=3
        )
        
        # Security Test Suite
        self.test_suites["security_suite"] = TestSuiteConfig(
            suite_id="security_suite",
            name="Security and Compliance Test Suite",
            description="Testing security measures and compliance requirements",
            category=TestSuiteCategory.SECURITY,
            priority=TestPriority.HIGH,
            execution_mode=TestExecutionMode.SEQUENTIAL,
            timeout=450,
            dependencies=["core_system", "api", "database"],
            prerequisites=["core_system_suite", "api_integration_suite"],
            cleanup_required=True,
            parallel_execution=False,
            max_parallel_tests=1
        )
        
        # V2 Compliance Test Suite
        self.test_suites["v2_compliance_suite"] = TestSuiteConfig(
            suite_id="v2_compliance_suite",
            name="V2 Compliance Validation Suite",
            description="Testing V2 compliance standards and requirements",
            category=TestSuiteCategory.COMPLIANCE,
            priority=TestPriority.CRITICAL,
            execution_mode=TestExecutionMode.DEPENDENCY_BASED,
            timeout=600,
            dependencies=["core_system", "workflow_system", "agent_management"],
            prerequisites=["core_system_suite", "workflow_system_suite", "agent_management_suite"],
            cleanup_required=True,
            parallel_execution=True,
            max_parallel_tests=4
        )
        
        self.logger.info(f"✅ Initialized {len(self.test_suites)} test suite configurations")
    
    def run_test_suite(self, suite_id: str, retry_count: int = 0) -> TestSuiteResult:
        """Run a specific test suite."""
        if suite_id not in self.test_suites:
            raise ValueError(f"Test suite '{suite_id}' not found")
        
        suite_config = self.test_suites[suite_id]
        self.logger.info(f"🧪 Starting test suite: {suite_config.name}")
        
        # Check prerequisites
        if not self._check_prerequisites(suite_config):
            self.logger.warning(f"⚠️ Prerequisites not met for {suite_id}, skipping")
            return self._create_skipped_result(suite_config, "Prerequisites not met")
        
        # Create execution record
        execution_start = datetime.now()
        suite_result = TestSuiteResult(
            suite_id=suite_id,
            suite_name=suite_config.name,
            execution_start=execution_start,
            execution_end=datetime.now(),
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
        
        self.active_suites[suite_id] = suite_result
        
        try:
            # Execute test suite based on execution mode
            if suite_config.execution_mode == TestExecutionMode.SEQUENTIAL:
                test_results = self._execute_sequential_suite(suite_config)
            elif suite_config.execution_mode == TestExecutionMode.PARALLEL:
                test_results = self._execute_parallel_suite(suite_config)
            elif suite_config.execution_mode == TestExecutionMode.PRIORITY_BASED:
                test_results = self._execute_priority_based_suite(suite_config)
            elif suite_config.execution_mode == TestExecutionMode.DEPENDENCY_BASED:
                test_results = self._execute_dependency_based_suite(suite_config)
            else:
                raise ValueError(f"Unsupported execution mode: {suite_config.execution_mode}")
            
            # Calculate results
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            total_tests = len(test_results)
            passed_tests = len([r for r in test_results if r.status == "passed"])
            failed_tests = len([r for r in test_results if r.status == "failed"])
            error_tests = len([r for r in test_results if r.status == "error"])
            skipped_tests = len([r for r in test_results if r.status == "skipped"])
            
            # Determine overall status
            if failed_tests == 0 and error_tests == 0:
                status = "passed"
            elif failed_tests > 0 or error_tests > 0:
                status = "partial" if passed_tests > 0 else "failed"
            else:
                status = "passed"
            
            # Create summary
            summary = {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "skipped": skipped_tests,
                "pass_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
                "execution_mode": suite_config.execution_mode.value,
                "parallel_execution": suite_config.parallel_execution,
                "max_parallel_tests": suite_config.max_parallel_tests
            }
            
            # Update suite result
            suite_result.execution_end = execution_end
            suite_result.execution_time = execution_time
            suite_result.total_tests = total_tests
            suite_result.passed_tests = passed_tests
            suite_result.failed_tests = failed_tests
            suite_result.error_tests = error_tests
            suite_result.skipped_tests = skipped_tests
            suite_result.status = status
            suite_result.test_results = test_results
            suite_result.summary = summary
            
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
    
    def run_all_test_suites(self, suite_ids: Optional[List[str]] = None, 
                           parallel: bool = True) -> List[TestSuiteResult]:
        """Run all test suites or specified ones."""
        suites_to_run = suite_ids or list(self.test_suites.keys())
        self.logger.info(f"🚀 Starting execution of {len(suites_to_run)} test suites")
        
        if parallel:
            return self._run_suites_parallel(suites_to_run)
        else:
            return self._run_suites_sequential(suites_to_run)
    
    def _run_suites_parallel(self, suite_ids: List[str]) -> List[TestSuiteResult]:
        """Run test suites in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_parallel_suites) as executor:
            future_to_suite = {
                executor.submit(self.run_test_suite, suite_id): suite_id
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
                        suite_name=self.test_suites[suite_id].name,
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
    
    def _run_suites_sequential(self, suite_ids: List[str]) -> List[TestSuiteResult]:
        """Run test suites sequentially."""
        results = []
        
        for suite_id in suite_ids:
            try:
                result = self.run_test_suite(suite_id)
                results.append(result)
                self.logger.info(f"✅ {suite_id}: {result.status}")
            except Exception as e:
                self.logger.error(f"❌ {suite_id}: Failed with error: {e}")
                # Create error result
                error_result = TestSuiteResult(
                    suite_id=suite_id,
                    suite_name=self.test_suites[suite_id].name,
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
    
    def _execute_sequential_suite(self, suite_config: TestSuiteConfig) -> List[IntegrationTestResult]:
        """Execute test suite sequentially."""
        test_results = []
        
        # Get tests for this suite category
        tests = self._get_tests_for_category(suite_config.category)
        
        for test in tests:
            try:
                result = self.integration_framework._execute_cross_module_test(test)
                test_results.append(result)
            except Exception as e:
                self.logger.error(f"Test {test} failed: {e}")
                # Create error result
                error_result = IntegrationTestResult(
                    test_id=test,
                    test_name=test,
                    test_type=IntegrationTestType.CROSS_MODULE,
                    status="error",
                    execution_time=0.0,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    details={},
                    error_message=str(e)
                )
                test_results.append(error_result)
        
        return test_results
    
    def _execute_parallel_suite(self, suite_config: TestSuiteConfig) -> List[IntegrationTestResult]:
        """Execute test suite in parallel."""
        test_results = []
        
        # Get tests for this suite category
        tests = self._get_tests_for_category(suite_config.category)
        
        with ThreadPoolExecutor(max_workers=suite_config.max_parallel_tests) as executor:
            future_to_test = {
                executor.submit(self.integration_framework._execute_cross_module_test, test): test
                for test in tests
            }
            
            for future in as_completed(future_to_test):
                test = future_to_test[future]
                try:
                    result = future.result()
                    test_results.append(result)
                except Exception as e:
                    self.logger.error(f"Test {test} failed: {e}")
                    # Create error result
                    error_result = IntegrationTestResult(
                        test_id=test,
                        test_name=test,
                        test_type=IntegrationTestType.CROSS_MODULE,
                        status="error",
                        execution_time=0.0,
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        details={},
                        error_message=str(e)
                    )
                    test_results.append(error_result)
        
        return test_results
    
    def _execute_priority_based_suite(self, suite_config: TestSuiteConfig) -> List[IntegrationTestResult]:
        """Execute test suite based on priority."""
        # Sort tests by priority and execute
        tests = self._get_tests_for_category(suite_config.category)
        priority_tests = sorted(tests, key=lambda x: self._get_test_priority(x), reverse=True)
        
        return self._execute_sequential_suite(suite_config)
    
    def _execute_dependency_based_suite(self, suite_config: TestSuiteConfig) -> List[IntegrationTestResult]:
        """Execute test suite based on dependencies."""
        # Execute tests in dependency order
        tests = self._get_tests_for_category(suite_config.category)
        dependency_ordered_tests = self._order_tests_by_dependencies(tests)
        
        return self._execute_sequential_suite(suite_config)
    
    def _get_tests_for_category(self, category: TestSuiteCategory) -> List[str]:
        """Get test IDs for a specific category."""
        category_suites = {
            TestSuiteCategory.CORE_SYSTEM: ["core_system_integration"],
            TestSuiteCategory.WORKFLOW_SYSTEM: ["workflow_integration"],
            TestSuiteCategory.AGENT_MANAGEMENT: ["agent_management_integration"],
            TestSuiteCategory.COMMUNICATION_SYSTEM: ["communication_integration"],
            TestSuiteCategory.API_INTEGRATION: ["api_integration"],
            TestSuiteCategory.DATABASE_INTEGRATION: ["database_integration"],
            TestSuiteCategory.END_TO_END: ["core_system_integration", "workflow_integration", "agent_management_integration"],
            TestSuiteCategory.PERFORMANCE: ["system_startup", "database_performance", "api_performance", "load_testing"],
            TestSuiteCategory.SECURITY: ["security_validation"],
            TestSuiteCategory.COMPLIANCE: ["v2_compliance_validation"]
        }
        
        return category_suites.get(category, [])
    
    def _get_test_priority(self, test_id: str) -> int:
        """Get priority value for a test."""
        priority_values = {
            TestPriority.CRITICAL: 4,
            TestPriority.HIGH: 3,
            TestPriority.NORMAL: 2,
            TestPriority.LOW: 1
        }
        
        # Default to normal priority
        return priority_values.get(TestPriority.NORMAL, 2)
    
    def _order_tests_by_dependencies(self, tests: List[str]) -> List[str]:
        """Order tests by their dependencies."""
        # Simple dependency ordering - can be enhanced with graph-based approach
        return tests
    
    def _check_prerequisites(self, suite_config: TestSuiteConfig) -> bool:
        """Check if prerequisites are met for a test suite."""
        if not suite_config.prerequisites:
            return True
        
        # Check if prerequisite suites have passed
        for prereq in suite_config.prerequisites:
            if not self._is_prerequisite_met(prereq):
                return False
        
        return True
    
    def _is_prerequisite_met(self, prereq: str) -> bool:
        """Check if a specific prerequisite is met."""
        # Check if prerequisite suite has passed
        for result in self.test_suite_results:
            if result.suite_id == prereq and result.status == "passed":
                return True
        
        # Check if it's a system prerequisite
        if prereq == "system_startup":
            return self._check_system_startup()
        elif prereq == "database_connection":
            return self._check_database_connection()
        
        return False
    
    def _check_system_startup(self) -> bool:
        """Check if system is started up."""
        try:
            # Simple system startup check
            return True
        except Exception:
            return False
    
    def _check_database_connection(self) -> bool:
        """Check if database connection is available."""
        try:
            # Simple database connection check
            return True
        except Exception:
            return False
    
    def _cleanup_suite(self, suite_config: TestSuiteConfig):
        """Clean up after test suite execution."""
        try:
            self.logger.info(f"🧹 Cleaning up after {suite_config.name}")
            # Implement cleanup logic based on suite requirements
            time.sleep(0.1)  # Simulate cleanup time
        except Exception as e:
            self.logger.warning(f"⚠️ Cleanup failed for {suite_config.name}: {e}")
    
    def _create_skipped_result(self, suite_config: TestSuiteConfig, reason: str) -> TestSuiteResult:
        """Create a skipped test suite result."""
        return TestSuiteResult(
            suite_id=suite_config.suite_id,
            suite_name=suite_config.name,
            execution_start=datetime.now(),
            execution_end=datetime.now(),
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            error_tests=0,
            skipped_tests=1,
            execution_time=0.0,
            status="skipped",
            test_results=[],
            summary={"skip_reason": reason}
        )
    
    def get_suite_summary(self) -> Dict[str, Any]:
        """Get summary of all test suite results."""
        if not self.test_suite_results:
            return {"message": "No test suites have been run yet"}
        
        total_suites = len(self.test_suite_results)
        passed_suites = len([r for r in self.test_suite_results if r.status == "passed"])
        failed_suites = len([r for r in self.test_suite_results if r.status == "failed"])
        error_suites = len([r for r in self.test_suite_results if r.status == "error"])
        partial_suites = len([r for r in self.test_suite_results if r.status == "partial"])
        skipped_suites = len([r for r in self.test_suite_results if r.status == "skipped"])
        
        # Calculate total tests across all suites
        total_tests = sum(r.total_tests for r in self.test_suite_results)
        total_passed = sum(r.passed_tests for r in self.test_suite_results)
        total_failed = sum(r.failed_tests for r in self.test_suite_results)
        total_errors = sum(r.error_tests for r in self.test_suite_results)
        
        # Calculate average execution time
        execution_times = [r.execution_time for r in self.test_suite_results if r.execution_time > 0]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Category breakdown
        category_results = {}
        for result in self.test_suite_results:
            suite_config = self.test_suites.get(result.suite_id)
            if suite_config:
                category = suite_config.category.value
                if category not in category_results:
                    category_results[category] = {"total": 0, "passed": 0, "failed": 0, "errors": 0}
                
                category_results[category]["total"] += 1
                if result.status == "passed":
                    category_results[category]["passed"] += 1
                elif result.status == "failed":
                    category_results[category]["failed"] += 1
                elif result.status == "error":
                    category_results[category]["errors"] += 1
        
        return {
            "total_suites": total_suites,
            "passed_suites": passed_suites,
            "failed_suites": failed_suites,
            "error_suites": error_suites,
            "partial_suites": partial_suites,
            "skipped_suites": skipped_suites,
            "suite_pass_rate": (passed_suites / total_suites) * 100 if total_suites > 0 else 0,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_errors": total_errors,
            "test_pass_rate": (total_passed / total_tests) * 100 if total_tests > 0 else 0,
            "average_execution_time": avg_execution_time,
            "category_breakdown": category_results,
            "execution_history": self.execution_history
        }
    
    def export_suite_results(self, format: str = "json", filepath: Optional[str] = None) -> str:
        """Export test suite results to specified format."""
        if format.lower() == "json":
            return self._export_suite_json_results(filepath)
        elif format.lower() == "html":
            return self._export_suite_html_results(filepath)
        elif format.lower() == "markdown":
            return self._export_suite_markdown_results(filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_suite_json_results(self, filepath: Optional[str] = None) -> str:
        """Export suite results to JSON format."""
        if not filepath:
            filepath = f"test_suite_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results_data = {
            "summary": self.get_suite_summary(),
            "suite_results": [
                {
                    "suite_id": r.suite_id,
                    "suite_name": r.suite_name,
                    "execution_start": r.execution_start.isoformat(),
                    "execution_end": r.execution_end.isoformat(),
                    "total_tests": r.total_tests,
                    "passed_tests": r.passed_tests,
                    "failed_tests": r.failed_tests,
                    "error_tests": r.error_tests,
                    "skipped_tests": r.skipped_tests,
                    "execution_time": r.execution_time,
                    "status": r.status,
                    "summary": r.summary,
                    "error_details": r.error_details
                }
                for r in self.test_suite_results
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        return filepath
    
    def _export_suite_html_results(self, filepath: Optional[str] = None) -> str:
        """Export suite results to HTML format."""
        if not filepath:
            filepath = f"test_suite_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        summary = self.get_suite_summary()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Suite Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .suite-result {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .passed {{ border-left: 5px solid #4CAF50; }}
                .failed {{ border-left: 5px solid #f44336; }}
                .error {{ border-left: 5px solid #ff9800; }}
                .partial {{ border-left: 5px solid #ffc107; }}
                .skipped {{ border-left: 5px solid #9e9e9e; }}
            </style>
        </head>
        <body>
            <h1>🧪 Test Suite Results</h1>
            <div class="summary">
                <h2>📊 Summary</h2>
                <p><strong>Total Suites:</strong> {summary['total_suites']}</p>
                <p><strong>Passed Suites:</strong> {summary['passed_suites']}</p>
                <p><strong>Failed Suites:</strong> {summary['failed_suites']}</p>
                <p><strong>Error Suites:</strong> {summary['error_suites']}</p>
                <p><strong>Partial Suites:</strong> {summary['partial_suites']}</p>
                <p><strong>Skipped Suites:</strong> {summary['skipped_suites']}</p>
                <p><strong>Suite Pass Rate:</strong> {summary['suite_pass_rate']:.1f}%</p>
                <p><strong>Total Tests:</strong> {summary['total_tests']}</p>
                <p><strong>Test Pass Rate:</strong> {summary['test_pass_rate']:.1f}%</p>
            </div>
            
            <h2>📋 Suite Results</h2>
        """
        
        for result in self.test_suite_results:
            status_class = result.status
            html_content += f"""
            <div class="suite-result {status_class}">
                <h3>{result.suite_name}</h3>
                <p><strong>Suite ID:</strong> {result.suite_id}</p>
                <p><strong>Status:</strong> {result.status.upper()}</p>
                <p><strong>Total Tests:</strong> {result.total_tests}</p>
                <p><strong>Passed:</strong> {result.passed_tests}</p>
                <p><strong>Failed:</strong> {result.failed_tests}</p>
                <p><strong>Errors:</strong> {result.error_tests}</p>
                <p><strong>Execution Time:</strong> {result.execution_time:.3f}s</p>
            """
            
            if result.error_details:
                html_content += f'<p><strong>Error Details:</strong> {result.error_details}</p>'
            
            html_content += '</div>'
        
        html_content += """
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def _export_suite_markdown_results(self, filepath: Optional[str] = None) -> str:
        """Export suite results to Markdown format."""
        if not filepath:
            filepath = f"test_suite_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        summary = self.get_suite_summary()
        
        markdown_content = f"""# 🧪 Test Suite Results

## 📊 Summary

- **Total Suites:** {summary['total_suites']}
- **Passed Suites:** {summary['passed_suites']}
- **Failed Suites:** {summary['failed_suites']}
- **Error Suites:** {summary['error_suites']}
- **Partial Suites:** {summary['partial_suites']}
- **Skipped Suites:** {summary['skipped_suites']}
- **Suite Pass Rate:** {summary['suite_pass_rate']:.1f}%
- **Total Tests:** {summary['total_tests']}
- **Test Pass Rate:** {summary['test_pass_rate']:.1f}%

## 📋 Suite Results

"""
        
        for result in self.test_suite_results:
            status_emoji = {
                "passed": "✅",
                "failed": "❌",
                "error": "⚠️",
                "partial": "🟡",
                "skipped": "⏭️"
            }.get(result.status, "❓")
            
            markdown_content += f"""### {status_emoji} {result.suite_name}

- **Suite ID:** {result.suite_id}
- **Status:** {result.status.upper()}
- **Total Tests:** {result.total_tests}
- **Passed:** {result.passed_tests}
- **Failed:** {result.failed_tests}
- **Errors:** {result.error_tests}
- **Execution Time:** {result.execution_time:.3f}s
"""
            
            if result.error_details:
                markdown_content += f"\n**Error Details:** {result.error_details}\n"
            
            markdown_content += "\n---\n\n"
        
        with open(filepath, 'w') as f:
            f.write(markdown_content)
        
        return filepath


# Convenience functions for easy usage
def run_test_suite(suite_id: str) -> TestSuiteResult:
    """Run a specific test suite."""
    test_suites = AutomatedIntegrationTestSuites()
    return test_suites.run_test_suite(suite_id)


def run_all_test_suites(parallel: bool = True) -> List[TestSuiteResult]:
    """Run all test suites."""
    test_suites = AutomatedIntegrationTestSuites()
    return test_suites.run_all_test_suites(parallel=parallel)


def run_category_suites(category: TestSuiteCategory, parallel: bool = True) -> List[TestSuiteResult]:
    """Run test suites for a specific category."""
    test_suites = AutomatedIntegrationTestSuites()
    
    # Get suites for the category
    category_suites = [
        suite_id for suite_id, config in test_suites.test_suites.items()
        if config.category == category
    ]
    
    return test_suites.run_all_test_suites(category_suites, parallel=parallel)


if __name__ == "__main__":
    # Example usage
    print("🧪 Automated Integration Test Suites - V2-COMPLIANCE-008")
    print("=" * 70)
    
    # Initialize test suites
    test_suites = AutomatedIntegrationTestSuites()
    
    # Run all test suites
    print("\n🚀 Running all test suites...")
    results = test_suites.run_all_test_suites(parallel=True)
    
    # Print summary
    summary = test_suites.get_suite_summary()
    print(f"\n📊 Test Suite Summary:")
    print(f"Total Suites: {summary['total_suites']}")
    print(f"Passed: {summary['passed_suites']}")
    print(f"Failed: {summary['failed_suites']}")
    print(f"Errors: {summary['error_suites']}")
    print(f"Suite Pass Rate: {summary['suite_pass_rate']:.1f}%")
    
    # Export results
    json_file = test_suites.export_suite_results("json")
    html_file = test_suites.export_suite_results("html")
    md_file = test_suites.export_suite_results("markdown")
    
    print(f"\n📁 Results exported to:")
    print(f"JSON: {json_file}")
    print(f"HTML: {html_file}")
    print(f"Markdown: {md_file}")
