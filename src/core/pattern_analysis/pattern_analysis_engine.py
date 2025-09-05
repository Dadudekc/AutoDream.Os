#!/usr/bin/env python3
"""
Pattern Analysis Engine - V2 Compliance Module
==============================================

Core business logic for pattern analysis operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
import statistics
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta

from .pattern_analysis_models import (
    MissionPattern,
    PatternCorrelation,
    MissionContext,
    StrategicRecommendation,
    PatternAnalysisResult,
    PatternMetrics,
    PatternAnalysisConfig,
    PatternType,
    RecommendationType,
    ImpactLevel,
)


class PatternAnalysisEngine:
    """Core engine for pattern analysis operations."""

    def __init__(self, config: PatternAnalysisConfig = None):
        """Initialize pattern analysis engine."""
        self.config = config or PatternAnalysisConfig()
        self.mission_patterns: Dict[str, MissionPattern] = {}
        self.pattern_correlations: Dict[str, PatternCorrelation] = {}
        self.metrics = PatternMetrics()

    def analyze_mission_patterns(self, mission_context: MissionContext) -> PatternAnalysisResult:
        """Analyze mission patterns for strategic decision making."""
        start_time = time.time()
        
        try:
            # Find relevant patterns
            relevant_patterns = self._find_relevant_patterns(mission_context)
            
            if not relevant_patterns:
                return PatternAnalysisResult(
                    success=False,
                    pattern_success_probability=0.0,
                    analysis_confidence=0.0,
                    error_message="No relevant patterns found"
                )
            
            # Calculate pattern effectiveness
            effectiveness = self._calculate_pattern_effectiveness(relevant_patterns, mission_context)
            
            # Generate recommendations
            recommendations = self._generate_pattern_recommendations(relevant_patterns, mission_context)
            
            # Analyze correlations
            correlations = self._analyze_pattern_correlations(relevant_patterns)
            
            # Assess risks
            risk_assessment = self._assess_mission_risks(mission_context, relevant_patterns)
            
            execution_time = (time.time() - start_time) * 1000
            
            # Update metrics
            self._update_metrics(relevant_patterns, recommendations)
            
            return PatternAnalysisResult(
                success=True,
                pattern_success_probability=effectiveness["overall_effectiveness"] * 100,
                analysis_confidence=effectiveness["confidence_level"],
                identified_patterns=relevant_patterns,
                recommendations=recommendations,
                correlations=correlations,
                risk_assessment=risk_assessment,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            return PatternAnalysisResult(
                success=False,
                pattern_success_probability=0.0,
                analysis_confidence=0.0,
                error_message=str(e),
                execution_time_ms=(time.time() - start_time) * 1000
            )

    def _find_relevant_patterns(self, mission_context: MissionContext) -> List[MissionPattern]:
        """Find patterns relevant to the mission context."""
        relevant_patterns = []
        
        for pattern in self.mission_patterns.values():
            relevance_score = self._calculate_pattern_relevance(pattern, mission_context)
            
            if relevance_score >= self.config.min_confidence_threshold:
                pattern.confidence_score = relevance_score
                relevant_patterns.append(pattern)
        
        # Sort by relevance and limit results
        relevant_patterns.sort(key=lambda p: p.confidence_score, reverse=True)
        return relevant_patterns[:self.config.max_patterns_per_analysis]

    def _calculate_pattern_relevance(self, pattern: MissionPattern, mission_context: MissionContext) -> float:
        """Calculate relevance score for a pattern."""
        relevance_score = 0.0
        
        # Mission type matching
        if pattern.mission_type == mission_context.mission_type:
            relevance_score += 0.4
        
        # Success indicators overlap
        mission_goals = set(mission_context.mission_goals)
        pattern_success = set(pattern.success_indicators)
        success_overlap = len(mission_goals & pattern_success)
        relevance_score += min(0.3, success_overlap * 0.1)
        
        # Risk factors overlap
        mission_risks = set(mission_context.risk_factors)
        pattern_risks = set(pattern.risk_factors)
        risk_overlap = len(mission_risks & pattern_risks)
        relevance_score += min(0.3, risk_overlap * 0.1)
        
        # Agent count consideration
        agent_count = len(mission_context.agent_assignments)
        if "agent_count" in pattern.optimal_conditions:
            optimal_range = pattern.optimal_conditions["agent_count"]
            if optimal_range == "4-6" and 4 <= agent_count <= 6:
                relevance_score += 0.1
        
        return min(1.0, relevance_score)

    def _calculate_pattern_effectiveness(self, patterns: List[MissionPattern], mission_context: MissionContext) -> Dict[str, Any]:
        """Calculate overall effectiveness of identified patterns."""
        if not patterns:
            return {"overall_effectiveness": 0.0, "confidence_level": 0.0}
        
        # Calculate weighted effectiveness
        total_weight = 0
        weighted_effectiveness = 0
        
        for pattern in patterns:
            weight = pattern.confidence_score * pattern.usage_count
            weighted_effectiveness += pattern.success_rate * weight
            total_weight += weight
        
        overall_effectiveness = weighted_effectiveness / total_weight if total_weight > 0 else 0.0
        
        # Calculate confidence based on pattern consensus
        success_rates = [p.success_rate for p in patterns]
        if len(success_rates) > 1:
            confidence_level = max(0.1, 1.0 - statistics.stdev(success_rates))
        else:
            confidence_level = 0.5
        
        return {
            "overall_effectiveness": round(overall_effectiveness, 3),
            "confidence_level": round(confidence_level, 3),
            "pattern_count": len(patterns),
            "average_success_rate": round(statistics.mean(success_rates), 3) if success_rates else 0.0
        }

    def _generate_pattern_recommendations(self, patterns: List[MissionPattern], mission_context: MissionContext) -> List[StrategicRecommendation]:
        """Generate pattern-based recommendations for mission success."""
        recommendations = []
        
        for pattern in patterns:
            if pattern.success_rate > self.config.success_rate_threshold:
                recommendation = StrategicRecommendation(
                    recommendation_id=f"pattern_{pattern.pattern_id}_{mission_context.mission_id}",
                    mission_context=mission_context.mission_id,
                    recommendation_type=RecommendationType.PATTERN_ADOPTION.value,
                    confidence_score=pattern.confidence_score,
                    expected_impact=ImpactLevel.HIGH.value if pattern.success_rate > 0.9 else ImpactLevel.MEDIUM.value,
                    implementation_steps=[
                        f"Adopt {pattern.pattern_type} pattern",
                        "Implement recommended coordination strategies",
                        "Monitor pattern effectiveness during execution"
                    ],
                    risk_assessment="low" if pattern.success_rate > 0.9 else "medium",
                    success_metrics=pattern.success_indicators
                )
                recommendations.append(recommendation)
        
        return recommendations[:self.config.max_recommendations]

    def _analyze_pattern_correlations(self, patterns: List[MissionPattern]) -> List[PatternCorrelation]:
        """Analyze correlations between patterns."""
        if not self.config.enable_correlation_analysis:
            return []
        
        correlations = []
        success_patterns = [p for p in patterns if p.success_rate > 0.8]
        
        for i, pattern_a in enumerate(success_patterns):
            for pattern_b in success_patterns[i+1:]:
                # Calculate correlation based on shared success indicators
                shared_indicators = set(pattern_a.success_indicators) & set(pattern_b.success_indicators)
                correlation_strength = len(shared_indicators) / max(len(pattern_a.success_indicators), 1)
                
                if correlation_strength > self.config.correlation_threshold:
                    correlation = PatternCorrelation(
                        correlation_id=f"corr_{pattern_a.pattern_id}_{pattern_b.pattern_id}",
                        pattern_a=pattern_a.pattern_id,
                        pattern_b=pattern_b.pattern_id,
                        correlation_strength=correlation_strength,
                        correlation_type="success_indicators",
                        evidence_count=len(shared_indicators),
                        confidence_score=correlation_strength
                    )
                    correlations.append(correlation)
        
        return correlations

    def _assess_mission_risks(self, mission_context: MissionContext, patterns: List[MissionPattern]) -> Dict[str, Any]:
        """Assess mission risks based on patterns."""
        if not self.config.enable_risk_assessment:
            return {"risk_level": "unknown", "risk_factors": []}
        
        risk_factors = set(mission_context.risk_factors)
        pattern_risks = set()
        
        for pattern in patterns:
            pattern_risks.update(pattern.risk_factors)
        
        common_risks = risk_factors & pattern_risks
        risk_level = "high" if len(common_risks) > 3 else "medium" if len(common_risks) > 1 else "low"
        
        return {
            "risk_level": risk_level,
            "risk_factors": list(common_risks),
            "mitigation_strategies": [
                "Implement pattern-based risk mitigation",
                "Monitor high-risk indicators closely",
                "Prepare contingency plans"
            ]
        }

    def _update_metrics(self, patterns: List[MissionPattern], recommendations: List[StrategicRecommendation]) -> None:
        """Update pattern analysis metrics."""
        self.metrics.total_patterns = len(self.mission_patterns)
        self.metrics.successful_analyses += 1
        self.metrics.pattern_usage_count += len(patterns)
        self.metrics.recommendation_count += len(recommendations)
        
        if patterns:
            self.metrics.average_confidence = sum(p.confidence_score for p in patterns) / len(patterns)
        
        self.metrics.last_updated = datetime.now()

    def add_pattern(self, pattern: MissionPattern) -> bool:
        """Add a new mission pattern."""
        try:
            self.mission_patterns[pattern.pattern_id] = pattern
            self.metrics.total_patterns = len(self.mission_patterns)
            return True
        except Exception:
            return False

    def get_pattern(self, pattern_id: str) -> Optional[MissionPattern]:
        """Get pattern by ID."""
        return self.mission_patterns.get(pattern_id)

    def get_metrics(self) -> PatternMetrics:
        """Get pattern analysis metrics."""
        return self.metrics

    def clear_old_patterns(self, days: int = 30) -> int:
        """Clear patterns older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        old_patterns = [
            pattern_id for pattern_id, pattern in self.mission_patterns.items()
            if pattern.last_updated < cutoff_date
        ]
        
        for pattern_id in old_patterns:
            del self.mission_patterns[pattern_id]
        
        self.metrics.total_patterns = len(self.mission_patterns)
        return len(old_patterns)
