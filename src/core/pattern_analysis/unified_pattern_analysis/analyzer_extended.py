#!/usr/bin/env python3
"""
Pattern Analyzer Extended - V2 Compliance Module
================================================

Extended pattern analysis strategies and implementations.
Extracted from analyzer.py for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import time
import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from .models_core import (
    MissionPattern, PatternCorrelation, MissionContext,
    StrategicRecommendation, PatternType, RecommendationType, ImpactLevel
)
from .models_extended import (
    PatternAnalysisResult, PerformanceMetrics, ResourceUtilization,
    TimingPattern, CoordinationPattern
)


class PatternAnalyzerExtended:
    """Extended pattern analysis strategies."""
    
    def __init__(self):
        """Initialize extended pattern analyzer."""
        self.logger = logging.getLogger(__name__)
        self.analysis_cache = {}
        self.correlation_threshold = 0.7
    
    def analyze_correlations(self, patterns: List[MissionPattern]) -> List[PatternCorrelation]:
        """Analyze pattern correlations."""
        correlations = []
        
        if len(patterns) < 2:
            return correlations
        
        # Find correlations between patterns
        for i, pattern_a in enumerate(patterns):
            for pattern_b in patterns[i+1:]:
                correlation = self._calculate_correlation(pattern_a, pattern_b)
                if correlation and correlation.correlation_strength >= self.correlation_threshold:
                    correlations.append(correlation)
        
        return correlations
    
    def _calculate_correlation(self, pattern_a: MissionPattern, pattern_b: MissionPattern) -> Optional[PatternCorrelation]:
        """Calculate correlation between two patterns."""
        try:
            # Calculate correlation strength based on success rates
            success_correlation = abs(pattern_a.success_rate - pattern_b.success_rate)
            correlation_strength = 1.0 - success_correlation
            
            # Calculate confidence level
            confidence_level = min(pattern_a.success_rate, pattern_b.success_rate)
            
            if correlation_strength >= self.correlation_threshold:
                return PatternCorrelation(
                    correlation_id=f"corr_{int(time.time())}",
                    pattern_a_id=pattern_a.pattern_id,
                    pattern_b_id=pattern_b.pattern_id,
                    correlation_strength=correlation_strength,
                    correlation_type="success_rate",
                    confidence_level=confidence_level,
                    analysis_timestamp=datetime.now()
                )
        except Exception as e:
            self.logger.error(f"Error calculating correlation: {e}")
        
        return None
    
    def generate_analysis_result(self, pattern_type: PatternType, patterns: List[MissionPattern], 
                               recommendations: List[StrategicRecommendation]) -> PatternAnalysisResult:
        """Generate comprehensive analysis result."""
        start_time = time.time()
        
        # Calculate analysis metrics
        patterns_analyzed = len(patterns)
        correlations_found = len(self.analyze_correlations(patterns))
        recommendations_generated = len(recommendations)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(patterns, recommendations)
        
        # Generate summary
        summary = self._generate_analysis_summary(pattern_type, patterns_analyzed, 
                                                correlations_found, recommendations_generated)
        
        # Generate detailed findings
        detailed_findings = self._generate_detailed_findings(patterns, recommendations)
        
        analysis_duration = time.time() - start_time
        
        return PatternAnalysisResult(
            analysis_id=f"analysis_{int(time.time())}",
            pattern_type=pattern_type,
            analysis_timestamp=datetime.now(),
            patterns_analyzed=patterns_analyzed,
            correlations_found=correlations_found,
            recommendations_generated=recommendations_generated,
            analysis_duration=analysis_duration,
            confidence_score=confidence_score,
            summary=summary,
            detailed_findings=detailed_findings
        )
    
    def _calculate_confidence_score(self, patterns: List[MissionPattern], 
                                  recommendations: List[StrategicRecommendation]) -> float:
        """Calculate confidence score for analysis."""
        if not patterns:
            return 0.0
        
        # Base confidence on pattern quality and recommendation relevance
        pattern_quality = statistics.mean([p.success_rate for p in patterns])
        recommendation_relevance = len(recommendations) / max(len(patterns), 1)
        
        # Weighted average
        confidence_score = (pattern_quality * 0.7) + (min(recommendation_relevance, 1.0) * 0.3)
        
        return min(confidence_score, 1.0)
    
    def _generate_analysis_summary(self, pattern_type: PatternType, patterns_analyzed: int,
                                 correlations_found: int, recommendations_generated: int) -> str:
        """Generate analysis summary."""
        return (f"Analyzed {patterns_analyzed} {pattern_type.value} patterns. "
                f"Found {correlations_found} correlations and generated "
                f"{recommendations_generated} strategic recommendations.")
    
    def _generate_detailed_findings(self, patterns: List[MissionPattern], 
                                  recommendations: List[StrategicRecommendation]) -> List[Dict[str, Any]]:
        """Generate detailed findings."""
        findings = []
        
        # Pattern findings
        for pattern in patterns:
            findings.append({
                "type": "pattern",
                "pattern_id": pattern.pattern_id,
                "success_rate": pattern.success_rate,
                "execution_time": pattern.execution_time,
                "agent_id": pattern.agent_id
            })
        
        # Recommendation findings
        for recommendation in recommendations:
            findings.append({
                "type": "recommendation",
                "recommendation_id": recommendation.recommendation_id,
                "title": recommendation.title,
                "impact_level": recommendation.impact_level.value,
                "priority": recommendation.implementation_priority
            })
        
        return findings
    
    def analyze_performance_metrics(self, metrics: List[PerformanceMetrics]) -> List[StrategicRecommendation]:
        """Analyze performance metrics patterns."""
        recommendations = []
        
        if not metrics:
            return recommendations
        
        # Analyze CPU usage patterns
        cpu_usage = [m.cpu_usage for m in metrics]
        avg_cpu = statistics.mean(cpu_usage)
        
        if avg_cpu > 80.0:
            recommendations.append(self._create_performance_metric_recommendation(
                "High CPU Usage",
                f"Average CPU usage: {avg_cpu:.1f}%",
                "Optimize CPU-intensive operations and implement load balancing"
            ))
        
        # Analyze memory usage patterns
        memory_usage = [m.memory_usage for m in metrics]
        avg_memory = statistics.mean(memory_usage)
        
        if avg_memory > 85.0:
            recommendations.append(self._create_performance_metric_recommendation(
                "High Memory Usage",
                f"Average memory usage: {avg_memory:.1f}%",
                "Implement memory optimization and garbage collection strategies"
            ))
        
        return recommendations
    
    def _create_performance_metric_recommendation(self, title: str, description: str, action: str) -> StrategicRecommendation:
        """Create performance metric recommendation."""
        return StrategicRecommendation(
            recommendation_id=f"rec_{int(time.time())}",
            pattern_id="performance_metric",
            recommendation_type=RecommendationType.OPTIMIZATION,
            impact_level=ImpactLevel.HIGH,
            title=title,
            description=description,
            implementation_priority=1,
            expected_benefit="Improved performance metrics",
            implementation_steps=[action],
            success_metrics={"cpu_usage": 70.0, "memory_usage": 75.0},
            created_timestamp=datetime.now()
        )
