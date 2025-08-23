#!/usr/bin/env python3
"""
Testing Framework Package - V2 Core Testing System
==================================================

Modular testing framework following V2 coding standards:
- Object-Oriented Programming (OOP)
- Single Responsibility Principle (SRP)
- Clean production-grade code
- TDD implementation

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .testing_types import (
    TestStatus, TestType, TestPriority,
    TestResult, TestScenario, TestEnvironment
)
from .testing_core import (
    BaseIntegrationTest, CrossSystemCommunicationTest,
    ServiceIntegrationTest, DatabaseIntegrationTest
)
from .testing_orchestration import (
    IntegrationTestSuite, IntegrationTestRunner,
    TestExecutor, TestOrchestrator
)
from .testing_cli import TestingFrameworkCLI, run_smoke_test

__all__ = [
    # Types and enums
    'TestStatus', 'TestType', 'TestPriority',
    'TestResult', 'TestScenario', 'TestEnvironment',
    # Core test classes
    'BaseIntegrationTest', 'CrossSystemCommunicationTest',
    'ServiceIntegrationTest', 'DatabaseIntegrationTest',
    # Orchestration
    'IntegrationTestSuite', 'IntegrationTestRunner',
    'TestExecutor', 'TestOrchestrator',
    # CLI interface
    'TestingFrameworkCLI', 'run_smoke_test'
]

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"
