#!/usr/bin/env python3
"""
Testing Orchestration - V2 Testing Framework Orchestration
==========================================================

Main orchestrator that coordinates test suites, runners, and executors.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import time
from typing import Dict, Any, List, Optional

from src.utils.stability_improvements import stability_manager, safe_import

# Import our modular components
try:
    from .testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from .testing_core import BaseIntegrationTest
    from .testing_orchestration_core import IntegrationTestSuite, TestSuiteResult
    from .testing_orchestration_runner import IntegrationTestRunner
    from .testing_orchestration_executor import TestExecutor, ExecutionConfig
    from .testing_orchestration_orchestrator import TestOrchestrator
except ImportError:
    from testing_types import TestStatus, TestType, TestPriority, TestResult, TestScenario, TestEnvironment
    from testing_core import BaseIntegrationTest
    from testing_orchestration_core import IntegrationTestSuite, TestSuiteResult
    from testing_orchestration_runner import IntegrationTestRunner
    from testing_orchestration_executor import TestExecutor, ExecutionConfig
    from testing_orchestration_orchestrator import TestOrchestrator


class TestingOrchestrationSystem:
    """
    Main testing orchestration system that coordinates all components.
    
    Responsibilities:
    - Coordinate test suite execution
    - Manage test runners and executors
    - Provide unified interface for testing operations
    - Handle configuration and reporting
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.orchestrator = TestOrchestrator(config)
        self.logger = logging.getLogger(__name__)
    
    def add_test_suite(self, suite: IntegrationTestSuite) -> None:
        """Add a test suite to the system."""
        self.orchestrator.add_test_suite(suite)
    
    def remove_test_suite(self, suite_name: str) -> bool:
        """Remove a test suite from the system."""
        return self.orchestrator.remove_test_suite(suite_name)
    
    async def run_test_suite(self, suite_name: str) -> Optional[Dict[str, Any]]:
        """Run a specific test suite."""
        return await self.orchestrator.orchestrate_suite(suite_name)
    
    async def run_multiple_suites(self, suite_names: List[str]) -> Dict[str, Any]:
        """Run multiple test suites."""
        return await self.orchestrator.orchestrate_multiple_suites(suite_names)
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get comprehensive system summary."""
        orchestrator_summary = self.orchestrator.get_orchestration_summary()
        runner_summary = self.orchestrator.runner.get_global_summary()
        executor_summary = self.orchestrator.executor.get_execution_summary()
        
        return {
            "orchestrator": orchestrator_summary,
            "runner": runner_summary,
            "executor": executor_summary,
            "config": self.orchestrator.get_config(),
            "timestamp": time.time()
        }
    
    def get_active_suites(self) -> Dict[str, Dict[str, Any]]:
        """Get currently active test suites."""
        return self.orchestrator.get_active_suites()
    
    def list_test_suites(self) -> List[str]:
        """List all available test suites."""
        return self.orchestrator.runner.list_test_suites()
    
    def clear_history(self) -> None:
        """Clear all execution and orchestration history."""
        self.orchestrator.clear_history()
        self.orchestrator.runner.clear_history()
        self.orchestrator.executor.clear_history()
        self.logger.info("All system history cleared")
    
    def update_config(self, **kwargs) -> None:
        """Update system configuration."""
        self.orchestrator.update_config(**kwargs)
        self.logger.info(f"Updated system configuration: {kwargs}")


# Convenience functions for backward compatibility
def create_test_suite(name: str, description: str = "") -> IntegrationTestSuite:
    """Create a new test suite."""
    return IntegrationTestSuite(name, description)


def create_test_runner() -> IntegrationTestRunner:
    """Create a new test runner."""
    return IntegrationTestRunner()


def create_test_executor(config: Optional[ExecutionConfig] = None) -> TestExecutor:
    """Create a new test executor."""
    return TestExecutor(config)


def create_test_orchestrator(config: Optional[Dict[str, Any]] = None) -> TestOrchestrator:
    """Create a new test orchestrator."""
    return TestOrchestrator(config)


def create_testing_system(config: Optional[Dict[str, Any]] = None) -> TestingOrchestrationSystem:
    """Create a new testing orchestration system."""
    return TestingOrchestrationSystem(config)


def run_smoke_test() -> bool:
    """Run smoke test for testing orchestration module."""
    try:
        print("🧪 Testing Testing Orchestration Module...")
        
        # Test IntegrationTestSuite
        suite = IntegrationTestSuite("Test Suite", "Test description")
        assert suite.name == "Test Suite"
        assert suite.description == "Test description"
        assert len(suite.tests) == 0
        print("✅ IntegrationTestSuite creation successful")
        
        # Test IntegrationTestRunner
        runner = IntegrationTestRunner()
        assert len(runner.test_suites) == 0
        runner.add_test_suite(suite)
        assert len(runner.test_suites) == 1
        print("✅ IntegrationTestRunner creation and suite addition successful")
        
        # Test TestExecutor
        executor = TestExecutor()
        assert len(executor.execution_history) == 0
        print("✅ TestExecutor creation successful")
        
        # Test TestOrchestrator
        orchestrator = TestOrchestrator()
        assert orchestrator.runner is not None
        assert orchestrator.executor is not None
        print("✅ TestOrchestrator creation successful")
        
        # Test TestingOrchestrationSystem
        system = TestingOrchestrationSystem()
        assert system.orchestrator is not None
        print("✅ TestingOrchestrationSystem creation successful")
        
        print("🎉 All testing orchestration smoke tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Testing orchestration smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
