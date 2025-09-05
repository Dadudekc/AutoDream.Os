#!/usr/bin/env python3
"""
Pattern Analyzer Refactored - V2 Compliance Module
==================================================

Refactored analyzer.py for V2 compliance.
Maintains backward compatibility while using modular architecture.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

# V2 COMPLIANCE REFACTOR - Import from modular components
from typing import List
from .analyzer_core import PatternAnalyzerCore
from .analyzer_extended import PatternAnalyzerExtended
from .models_core import (
    MissionPattern, PatternCorrelation, MissionContext,
    StrategicRecommendation, PatternType, RecommendationType, ImpactLevel
)
from .models_extended import (
    PatternAnalysisResult, PerformanceMetrics, ResourceUtilization,
    TimingPattern, CoordinationPattern
)


class PatternAnalyzer:
    """Unified pattern analyzer combining core and extended functionality."""
    
    def __init__(self):
        """Initialize pattern analyzer."""
        self.core_analyzer = PatternAnalyzerCore()
        self.extended_analyzer = PatternAnalyzerExtended()
    
    def analyze_pattern_type(self, pattern_type: PatternType, patterns: List[MissionPattern]) -> List[StrategicRecommendation]:
        """Analyze patterns of specific type."""
        return self.core_analyzer.analyze_pattern_type(pattern_type, patterns)
    
    def analyze_correlations(self, patterns: List[MissionPattern]) -> List[PatternCorrelation]:
        """Analyze pattern correlations."""
        return self.extended_analyzer.analyze_correlations(patterns)
    
    def generate_analysis_result(self, pattern_type: PatternType, patterns: List[MissionPattern], 
                               recommendations: List[StrategicRecommendation]) -> PatternAnalysisResult:
        """Generate comprehensive analysis result."""
        return self.extended_analyzer.generate_analysis_result(pattern_type, patterns, recommendations)
    
    def analyze_performance_metrics(self, metrics: List[PerformanceMetrics]) -> List[StrategicRecommendation]:
        """Analyze performance metrics patterns."""
        return self.extended_analyzer.analyze_performance_metrics(metrics)
