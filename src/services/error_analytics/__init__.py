#!/usr/bin/env python3
"""
Error Analytics Package - V2 Error Analytics System
==================================================
Package containing specialized modules for error analytics:
- Pattern detection and analysis
- Trend analysis and forecasting
- Correlation analysis and detection
- Comprehensive report generation

Follows V2 standards with advanced analytics capabilities.
"""

from .pattern_detector import ErrorPatternDetector, PatternAnalysisResult
from .trend_analyzer import ErrorTrendAnalyzer, ErrorTrend, TrendAnalysisResult
from .correlation_analyzer import ErrorCorrelationAnalyzer, ErrorCorrelation, CorrelationAnalysisResult
from .report_generator import ErrorReportGenerator, AnalyticsReport, ReportFormat

__all__ = [
    # Pattern detection
    "ErrorPatternDetector",
    "PatternAnalysisResult",
    
    # Trend analysis
    "ErrorTrendAnalyzer",
    "ErrorTrend",
    "TrendAnalysisResult",
    
    # Correlation analysis
    "ErrorCorrelationAnalyzer",
    "ErrorCorrelation",
    "CorrelationAnalysisResult",
    
    # Report generation
    "ErrorReportGenerator",
    "AnalyticsReport",
    "ReportFormat",
]

__version__ = "2.0.0"
__author__ = "Agent-4"
__description__ = "Advanced error analytics system with pattern detection, trend analysis, correlation analysis, and comprehensive reporting"
