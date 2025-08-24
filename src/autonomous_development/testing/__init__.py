"""
Testing Package - Autonomous Development
=======================================

Provides automated testing orchestration capabilities for
autonomous development processes.
"""

from .orchestrator import TestingOrchestrator
from .test_execution import TestResult
from .result_collation import TestSuite

__all__ = ["TestingOrchestrator", "TestResult", "TestSuite"]
