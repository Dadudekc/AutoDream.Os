"""
Testing Package - Autonomous Development
=======================================

Provides automated testing orchestration capabilities for
autonomous development processes.
"""

from .orchestrator import TestingOrchestrator
from .result_collation import TestResult, TestSummary

__all__ = ["TestingOrchestrator", "TestResult", "TestSummary"]

