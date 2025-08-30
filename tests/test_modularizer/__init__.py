#!/usr/bin/env python3
"""
Test Modularizer Package

This package contains modularized components for testing coverage analysis.
All modules are V2 compliant with focused responsibilities.

Modules:
- coverage_models: Data structures for coverage analysis
- coverage_analyzer: Core coverage analysis functionality
- risk_assessor: Risk assessment for coverage analysis
- metrics_calculator: Coverage metrics computation
- file_analyzer: File structure analysis
- recommendations_engine: Coverage improvement recommendations
- testing_coverage_analysis_modular: Main orchestrator (V2 compliant)
"""

from .coverage_models import (
    CoverageLevel,
    CoverageMetric,
    FileStructure,
    CoverageResult,
    RiskAssessment,
    CoverageReport
)

from .coverage_analyzer import CoverageAnalyzer
from .risk_assessor import RiskAssessor
from .metrics_calculator import MetricsCalculator
from .file_analyzer import FileStructureAnalyzer
from .recommendations_engine import RecommendationsEngine
from .testing_coverage_analysis_modular import TestingCoverageAnalyzerModular

__version__ = "2.0.0"
__author__ = "Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)"
__status__ = "V2_COMPLIANT"

__all__ = [
    # Data models
    "CoverageLevel",
    "CoverageMetric", 
    "FileStructure",
    "CoverageResult",
    "RiskAssessment",
    "CoverageReport",
    
    # Core components
    "CoverageAnalyzer",
    "RiskAssessor",
    "MetricsCalculator",
    "FileStructureAnalyzer",
    "RecommendationsEngine",
    
    # Main orchestrator
    "TestingCoverageAnalyzerModular"
]

