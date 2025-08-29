from .cli_handlers import (
from .output_formatter import OutputFormatter
from .test_categories import TestCategories
from .test_discovery import discover_test_files
from .test_execution import TestExecutor, TestRunner
from .test_reporting import summarize_results, print_execution_summary
from .test_suite_consolidator import (
from .testing_infrastructure_manager import (
from .testing_orchestrator import TestingOrchestrator
from .testing_reporter import TestingReporter
from .testing_system_eliminator import (
from .testing_utils import (
from .unified_testing_framework import (
from .unified_testing_system import (

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
    BaseIntegrationTest,
    BaseTest,
    TestEnvironment,
    TestPriority,
    TestReport,
    TestResult,
    TestStatus,
    TestSuite,
    TestType,
)


# CLI handlers
    RunCommandHandler,
    ReportCommandHandler,
    StatusCommandHandler,
    RegisterCommandHandler,
    SuiteCommandHandler,
    ResultsCommandHandler,
)

# Unified testing system (TASK 3G)
    UnifiedTestingSystem,
    TestExecutionConfig,
    TestFramework,
)

# Testing infrastructure manager (TASK 3G)
    TestingInfrastructureManager,
    TestingDependency,
    TestDirectory,
    DependencyStatus,
)

# Unified testing framework (TASK 3H)
    UnifiedTestingFramework,
    TestFrameworkType,
    TestSuiteConfig,
    TestSuiteResult,
)

# Test suite consolidator (TASK 3H)
    TestSuiteConsolidator,
    TestCategory,
    TestFileInfo,
    ConsolidationPlan,
)

# Testing system eliminator (TASK 3H)
    TestingSystemEliminator,
    EliminationTarget,
    EliminationPlan,
)

__all__ = [
    # Core testing components
    "TestExecutor",
    "TestRunner",
    "BaseTest",
    "BaseIntegrationTest",
    "TestResult",
    "TestStatus",
    "TestType",
    "TestPriority",
    "TestEnvironment",
    "TestSuite",
    "TestReport",
    "discover_test_files",
    "summarize_results",
    "print_execution_summary",
    # Testing orchestration and reporting
    "TestingOrchestrator",
    "TestingReporter",
    "TestCategories",
    "OutputFormatter",
    # CLI handlers
    "RunCommandHandler",
    "ReportCommandHandler",
    "StatusCommandHandler",
    "RegisterCommandHandler",
    "SuiteCommandHandler",
    "ResultsCommandHandler",
    # Unified testing system (TASK 3G)
    "UnifiedTestingSystem",
    "TestExecutionConfig",
    "TestFramework",
    # Testing infrastructure manager (TASK 3G)
    "TestingInfrastructureManager",
    "TestingDependency",
    "TestDirectory",
    "DependencyStatus",
    # Unified testing framework (TASK 3H)
    "UnifiedTestingFramework",
    "TestFrameworkType",
    "TestSuiteConfig",
    "TestSuiteResult",
    # Test suite consolidator (TASK 3H)
    "TestSuiteConsolidator",
    "TestCategory",
    "TestFileInfo",
    "ConsolidationPlan",
    # Testing system eliminator (TASK 3H)
    "TestingSystemEliminator",
    "EliminationTarget",
    "EliminationPlan",
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-3 Integration & Testing Specialist"
__description__ = "Unified testing framework with consolidated infrastructure"
