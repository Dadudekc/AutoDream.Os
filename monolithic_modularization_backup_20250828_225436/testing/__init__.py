#!/usr/bin/env python3
"""
Testing Package - Agent Cellphone V2
====================================

CONSOLIDATED testing framework - replaces multiple separate testing classes with unified manager.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

CONSOLIDATION STATUS:
- ✅ TestingFrameworkManager: Unified testing management (core/managers/testing_framework_manager/)
- ❌ REMOVED: runner.py (consolidated into TestingFrameworkManager)
- ❌ REMOVED: orchestrator.py (consolidated into TestingFrameworkManager)
- ❌ REMOVED: run_tdd_tests.py (consolidated into TestingFrameworkManager)
- ❌ REMOVED: run_tests.py (consolidated into TestingFrameworkManager)
- ❌ REMOVED: run_test_suite.py (consolidated into TestingFrameworkManager)
"""
    from ..core.managers.testing_framework_manager import (

# ARCHITECTURE CORRECTED: Using unified testing framework manager
# Optional import to keep package lightweight and avoid hard dependency
try:  # pragma: no cover - tested via import side effects
        TestingFrameworkManager,
        TestExecutionResult,
        TestSuiteResult,
        TestConfiguration,
    )

    __all__ = [
        "TestingFrameworkManager",
        "TestExecutionResult",
        "TestSuiteResult",
        "TestConfiguration",
    ]
except Exception:  # pragma: no cover - imported lazily
    TestingFrameworkManager = None
    TestExecutionResult = None
    TestSuiteResult = None
    TestConfiguration = None
    __all__ = []

