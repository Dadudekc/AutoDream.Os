#!/usr/bin/env python3
"""
Compliance Test Fixtures
========================

Common test fixtures and mocks for compliance dashboard tests.
Extracted for V2 compliance (<400 lines per file).

Author: Agent-3 (Infrastructure & DevOps)
V2 Compliance: Extracted from test_compliance_dashboard.py
"""

from dataclasses import dataclass


@dataclass
class MockViolation:
    """Mock V2 compliance violation."""

    file_path: str
    severity: str
    line: int = 1
    message: str = "Test violation"


@dataclass
class MockV2Report:
    """Mock V2 compliance report."""

    total_files: int
    compliance_rate: float
    critical_violations: list[MockViolation]
    major_violations: list[MockViolation]
    minor_violations: list[MockViolation]
    violations: list[MockViolation]


@dataclass
class MockComplexityViolation:
    """Mock complexity violation."""

    severity: str
    metric: str
    value: int


@dataclass
class MockComplexityReport:
    """Mock complexity report."""

    file_path: str
    has_violations: bool
    violations: list[MockComplexityViolation]


@dataclass
class MockSuggestion:
    """Mock refactoring suggestion."""

    file_path: str
    current_lines: int
    estimated_main_file_lines: int
    confidence: float
    suggested_modules: list[str]


def create_sample_v2_report():
    """Create a sample V2 compliance report."""
    return MockV2Report(
        total_files=100,
        compliance_rate=0.95,
        critical_violations=[MockViolation("test1.py", "critical", 1, "File too long")],
        major_violations=[MockViolation("test2.py", "major", 50, "Function too complex")],
        minor_violations=[MockViolation("test3.py", "minor", 10, "Missing docstring")],
        violations=[
            MockViolation("test1.py", "critical", 1, "File too long"),
            MockViolation("test2.py", "major", 50, "Function too complex"),
            MockViolation("test3.py", "minor", 10, "Missing docstring"),
        ],
    )


def create_sample_complexity_report():
    """Create a sample complexity report."""
    return MockComplexityReport(
        file_path="test.py",
        has_violations=True,
        violations=[MockComplexityViolation("high", "cyclomatic_complexity", 15)],
    )


def create_sample_suggestion():
    """Create a sample refactoring suggestion."""
    return MockSuggestion(
        file_path="test.py",
        current_lines=500,
        estimated_main_file_lines=300,
        confidence=0.8,
        suggested_modules=["test_helper.py", "test_utils.py"],
    )
