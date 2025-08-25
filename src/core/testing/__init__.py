"""
Consolidated Testing Framework Package
=====================================

A unified, modular testing framework that consolidates all testing functionality
across the project into a single, maintainable system.

This package provides:
- Core testing types and enums
- Test execution and orchestration
- Test result management and reporting
- Integration testing capabilities
- CLI interface for testing operations
"""

from .testing_types import (
    TestStatus,
    TestType,
    TestPriority,
    TestResult,
    TestScenario,
    TestEnvironment,
    TestSuite,
    TestReport
)

from .testing_core import (
    BaseTest,
    BaseIntegrationTest,
    TestRunner,
    TestExecutor
)

from .testing_orchestrator import (
    TestOrchestrator,
    TestSuiteManager,
    TestScheduler
)

from .testing_reporter import (
    TestReporter,
    CoverageReporter,
    PerformanceReporter,
    HTMLReporter
)

from .testing_cli import TestingFrameworkCLI

# Convenience functions for quick access
def create_testing_system():
    """Create a complete testing system instance"""
    from .testing_orchestrator import TestOrchestrator
    return TestOrchestrator()

def run_test_suite(suite_name: str):
    """Quick function to run a test suite"""
    system = create_testing_system()
    return system.run_test_suite(suite_name)

def run_all_tests():
    """Quick function to run all tests"""
    system = create_testing_system()
    return system.run_all_tests()

def get_test_summary():
    """Quick function to get test summary"""
    system = create_testing_system()
    return system.get_test_summary()

__all__ = [
    # Core types
    'TestStatus',
    'TestType', 
    'TestPriority',
    'TestResult',
    'TestScenario',
    'TestEnvironment',
    'TestSuite',
    'TestReport',
    
    # Core classes
    'BaseTest',
    'BaseIntegrationTest',
    'TestRunner',
    'TestExecutor',
    
    # Orchestration
    'TestOrchestrator',
    'TestSuiteManager',
    'TestScheduler',
    
    # Reporting
    'TestReporter',
    'CoverageReporter',
    'PerformanceReporter',
    'HTMLReporter',
    
    # CLI
    'TestingFrameworkCLI',
    
    # Convenience functions
    'create_testing_system',
    'run_test_suite',
    'run_all_tests',
    'get_test_summary'
]
