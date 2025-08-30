#!/usr/bin/env python3
"""
Test Modularizer Package

This package contains modular components for testing coverage analysis,
replacing the monolithic testing_coverage_analysis.py file.
"""

from .testing_coverage_analysis_modular import (
    CoreCoverageAnalyzer,
    CoverageResult,
    CoverageMetric,
    FileStructure,
    RiskAssessment,
    CoverageCalculator,
    RiskAssessor,
    RecommendationsEngine,
    analyzer,
    analyze_test_coverage,
    generate_summary_report,
    export_results
)

__version__ = "2.0.0"
__author__ = "Agent-3 - Testing Framework Enhancement Manager"

__all__ = [
    'CoreCoverageAnalyzer',
    'CoverageResult',
    'CoverageMetric',
    'FileStructure',
    'RiskAssessment',
    'CoverageCalculator',
    'RiskAssessor',
    'RecommendationsEngine',
    'analyzer',
    'analyze_test_coverage',
    'generate_summary_report',
    'export_results'
]

