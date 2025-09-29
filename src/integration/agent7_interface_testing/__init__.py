#!/usr/bin/env python3
"""
Agent-7 Interface Testing Package
=================================

Agent-7 Repository Management Interface Testing & Validation Package
V2 Compliant: Modular design with focused components
"""

from .core_testing import Agent7InterfaceTestingValidation, run_agent7_interface_testing_validation
from .functionality_tests import Agent7FunctionalityTests
from .integration_tests import Agent7IntegrationTests
from .models import (
    InterfaceAnalysis,
    InterfaceMetrics,
    RepositoryTestData,
    TestCategory,
    TestResult,
    TestStatus,
    ValidationReport,
)

__all__ = [
    # Core testing
    "Agent7InterfaceTestingValidation",
    "run_agent7_interface_testing_validation",
    # Models
    "TestCategory",
    "TestStatus",
    "TestResult",
    "InterfaceAnalysis",
    "ValidationReport",
    "RepositoryTestData",
    "InterfaceMetrics",
    # Test modules
    "Agent7FunctionalityTests",
    "Agent7IntegrationTests",
]
