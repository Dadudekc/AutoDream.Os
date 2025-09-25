#!/usr/bin/env python3
"""
Testing Validation Modules Package
==================================

Team Beta Testing Validation Modules Package
V2 Compliant: Modular design with focused components
"""

from .core_validation import TestingValidationSystem, main
from .models import (
    TestCase,
    TestResult,
    TestStatus,
    TestCategory,
    PlatformInfo,
    TestMetrics,
    ValidationReport
)
from .test_execution import TestExecutor

__all__ = [
    # Core validation
    "TestingValidationSystem",
    "main",
    
    # Models
    "TestCase",
    "TestResult",
    "TestStatus",
    "TestCategory",
    "PlatformInfo",
    "TestMetrics",
    "ValidationReport",
    
    # Test execution
    "TestExecutor"
]