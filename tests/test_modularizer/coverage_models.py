#!/usr/bin/env python3
"""
Coverage Models - Data structures for testing coverage analysis.

This module contains all data classes and structures used by the coverage analysis system.
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class CoverageLevel:
    """Coverage level classification for modularized components."""
    level: str
    percentage: float
    description: str
    color: str


@dataclass
class CoverageMetric:
    """Coverage metric for testing analysis."""
    name: str
    value: float
    target: float
    status: str
    risk_level: str


@dataclass
class FileStructure:
    """File structure analysis results."""
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    functions: List[str]
    classes: List[str]
    imports: List[str]


@dataclass
class CoverageResult:
    """Complete coverage analysis result."""
    file_path: str
    timestamp: str
    overall_coverage: float
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    class_coverage: float
    risk_level: str
    recommendations: List[str]
    uncovered_areas: List[str]


@dataclass
class RiskAssessment:
    """Risk assessment for coverage gaps."""
    risk_level: str
    risk_score: float
    critical_issues: List[str]
    warnings: List[str]
    suggestions: List[str]
