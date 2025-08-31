#!/usr/bin/env python3
"""
Core Testing Framework - Agent Cellphone V2
==========================================

Core components of the unified testing framework.
Modularized to achieve V2 compliance (500 line limit).

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from .test_enums import (
    TestMode,
    TestStatus,
    TestPriority,
    TestEnvironment,
    TestLevel,
    TestType
)

from .test_dataclasses import (
    TestCategory,
    TestResult,
    TestExecutionConfig,
    TestSuite,
    TestReport
)

from .test_utilities_enums import (
    TestUtilityType,
    MockObjectType,
    TestDataType,
    ValidationType
)

from .test_utilities_dataclasses import (
    MockObjectConfig,
    TestDataConfig,
    ValidationRule,
    TestEnvironment as TestEnvConfig,
    TestReport as TestReportConfig
)

__all__ = [
    # Core Enums
    'TestMode',
    'TestStatus', 
    'TestPriority',
    'TestEnvironment',
    'TestLevel',
    'TestType',
    
    # Core Dataclasses
    'TestCategory',
    'TestResult',
    'TestExecutionConfig',
    'TestSuite',
    'TestReport',
    
    # Utilities Enums
    'TestUtilityType',
    'MockObjectType',
    'TestDataType',
    'ValidationType',
    
    # Utilities Dataclasses
    'MockObjectConfig',
    'TestDataConfig',
    'ValidationRule',
    'TestEnvConfig',
    'TestReportConfig'
]
