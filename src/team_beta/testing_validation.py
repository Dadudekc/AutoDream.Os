#!/usr/bin/env python3
"""
Testing Validation System for Team Beta Mission
===============================================

REFACTORED: Now uses modular design with focused components
V2 Compliant: ≤400 lines, imports from testing_validation_modules package

This file now serves as the main entry point and maintains backward compatibility
while delegating to the modular testing_validation_modules package.

Agent-7 Repository Cloning Specialist - Comprehensive Testing Integration
"""

# Import all functionality from the modular package
from .testing_validation_modules import (
    TestingValidationSystem,
    TestCase,
    TestResult,
    TestStatus,
    TestCategory,
    PlatformInfo,
    TestMetrics,
    ValidationReport,
    TestExecutor,
    main
)

# Re-export for backward compatibility
__all__ = [
    "TestingValidationSystem",
    "TestCase",
    "TestResult",
    "TestStatus",
    "TestCategory",
    "PlatformInfo",
    "TestMetrics",
    "ValidationReport",
    "TestExecutor",
    "main"
]

# Main execution function for backward compatibility
if __name__ == "__main__":
    main()