#!/usr/bin/env python3
"""
Communications Package
=====================

Interaction system testing and communication tools.
Follows V2 standards: modular, compliant architecture.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .testing_core import (
    TestingCore,
    TestResult,
    TestSuite,
    TestStatus,
    TestCategory
)
from .test_executor import (
    TestExecutor,
    TestExecutionConfig
)
from .testing_orchestrator import TestingOrchestrator

__all__ = [
    'TestingCore',
    'TestResult',
    'TestSuite',
    'TestStatus',
    'TestCategory',
    'TestExecutor',
    'TestExecutionConfig',
    'TestingOrchestrator'
]

__version__ = "1.0.0"
__author__ = "V2 SWARM CAPTAIN"
__license__ = "MIT"
