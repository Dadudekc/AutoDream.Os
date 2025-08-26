#!/usr/bin/env python3
"""
Testing Package - Agent Cellphone V2

Unified testing framework providing comprehensive testing capabilities
with consolidated infrastructure and eliminated duplication.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3G - Testing Infrastructure Cleanup
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

# Core testing components
from .testing_core import (
    TestExecutor, TestRunner, BaseTest, TestResult,
    TestStatus, TestType
)

from .testing_orchestrator import TestingOrchestrator
from .testing_reporter import TestingReporter
from .test_categories import TestCategories
from .output_formatter import OutputFormatter
from .testing_types import TestingTypes

# CLI handlers
from .cli_handlers import (
    RunCommandHandler, ReportCommandHandler, StatusCommandHandler,
    RegisterCommandHandler, SuiteCommandHandler, ResultsCommandHandler
)

# Unified testing system (TASK 3G)
from .unified_testing_system import (
    UnifiedTestingSystem, TestExecutionConfig, TestFramework
)

# Testing infrastructure manager (TASK 3G)
from .testing_infrastructure_manager import (
    TestingInfrastructureManager, TestingDependency, TestDirectory,
    DependencyStatus
)

# Unified testing framework (TASK 3H)
from .unified_testing_framework import (
    UnifiedTestingFramework, TestFrameworkType, TestSuiteConfig, TestSuiteResult
)

# Test suite consolidator (TASK 3H)
from .test_suite_consolidator import (
    TestSuiteConsolidator, TestCategory, TestFileInfo, ConsolidationPlan
)

# Testing system eliminator (TASK 3H)
from .testing_system_eliminator import (
    TestingSystemEliminator, EliminationTarget, EliminationPlan
)

# Example tests
from .example_tests import ExampleTestSuite

__all__ = [
    # Core testing components
    'TestExecutor',
    'TestRunner', 
    'BaseTest',
    'TestResult',
    'TestStatus',
    'TestType',
    
    # Testing orchestration and reporting
    'TestingOrchestrator',
    'TestingReporter',
    'TestCategories',
    'OutputFormatter',
    'TestingTypes',
    
    # CLI handlers
    'RunCommandHandler',
    'ReportCommandHandler',
    'StatusCommandHandler',
    'RegisterCommandHandler',
    'SuiteCommandHandler',
    'ResultsCommandHandler',
    
    # Unified testing system (TASK 3G)
    'UnifiedTestingSystem',
    'TestExecutionConfig',
    'TestFramework',
    
    # Testing infrastructure manager (TASK 3G)
    'TestingInfrastructureManager',
    'TestingDependency',
    'TestDirectory',
    'DependencyStatus',
    
    # Unified testing framework (TASK 3H)
    'UnifiedTestingFramework',
    'TestFrameworkType',
    'TestSuiteConfig',
    'TestSuiteResult',
    
    # Test suite consolidator (TASK 3H)
    'TestSuiteConsolidator',
    'TestCategory',
    'TestFileInfo',
    'ConsolidationPlan',
    
    # Testing system eliminator (TASK 3H)
    'TestingSystemEliminator',
    'EliminationTarget',
    'EliminationPlan',
    
    # Example tests
    'ExampleTestSuite'
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-3 Integration & Testing Specialist"
__description__ = "Unified testing framework with consolidated infrastructure"
