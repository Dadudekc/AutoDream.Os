"""
Testing Coverage Analysis - Modular Interface

This is the main interface module that provides access to all coverage analysis functionality.
It replaces the monolithic testing_coverage_analysis.py file with a clean, modular structure.
"""

from .core_analyzer import CoreCoverageAnalyzer
from .coverage_models import CoverageResult, CoverageMetric, FileStructure, RiskAssessment
from .coverage_calculator import CoverageCalculator
from .risk_assessor import RiskAssessor
from .recommendations_engine import RecommendationsEngine

# Main analyzer instance for easy access
analyzer = CoreCoverageAnalyzer()

# Convenience functions for backward compatibility
def analyze_test_coverage(target_file: str, test_directory: str = None) -> CoverageResult:
    """Analyze test coverage for a target file."""
    return analyzer.analyze_test_coverage(target_file, test_directory)

def generate_summary_report(result: CoverageResult) -> dict:
    """Generate a summary report from coverage results."""
    return analyzer.generate_summary_report(result)

def export_results(result: CoverageResult, format: str = "json") -> str:
    """Export results in specified format."""
    return analyzer.export_results(result, format)

# Export main classes for direct use
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
