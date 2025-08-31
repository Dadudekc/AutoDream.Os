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

__all__ = [
    # Enums
    'TestMode',
    'TestStatus', 
    'TestPriority',
    'TestEnvironment',
    'TestLevel',
    'TestType',
    
    # Dataclasses
    'TestCategory',
    'TestResult',
    'TestExecutionConfig',
    'TestSuite',
    'TestReport'
]
