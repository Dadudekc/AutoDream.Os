"""
Recommendation Engine Refactored - V2 Compliant Module
=====================================================

Refactored engine for optimization recommendation generation.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from ..vector_integration_models import (
    OptimizationRecommendation, PerformanceMetrics, TrendAnalysis,
    create_optimization_recommendation
)
from .recommendation_engine_base import RecommendationEngineBase
from .recommendation_engine_analysis import RecommendationEngineAnalysis
from .recommendation_engine_system import RecommendationEngineSystem


class RecommendationEngine(RecommendationEngineBase):
    """Refactored engine for optimization recommendation generation."""
    
    def __init__(self, config):
        """Initialize recommendation engine."""
        super().__init__(config)
        
        # Initialize modular components
        self.analysis = RecommendationEngineAnalysis(self, self.logger)
        self.system = RecommendationEngineSystem(self, self.logger)
    
    def generate_recommendations(self, metrics_data: List[PerformanceMetrics],
                               trends: Dict[str, TrendAnalysis]) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations based on analysis."""
        try:
            recommendations = []
            
            # Generate metric-specific recommendations
            metric_recommendations = self.analysis._generate_metric_recommendations(metrics_data, trends)
            recommendations.extend(metric_recommendations)
            
            # Generate system-wide recommendations
            system_recommendations = self.system._generate_system_recommendations(metrics_data)
            recommendations.extend(system_recommendations)
            
            # Add recommendations to cache
            for rec in recommendations:
                self.add_recommendation(rec)
            
            self.logger.info(f"Generated {len(recommendations)} total recommendations")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return []
    
    def _generate_metric_recommendations(self, metrics_data: List[PerformanceMetrics],
                                       trends: Dict[str, TrendAnalysis]) -> List[OptimizationRecommendation]:
        """Generate recommendations based on metric analysis."""
        return self.analysis._generate_metric_recommendations(metrics_data, trends)
    
    def _analyze_metric_for_recommendations(self, metric_name: str, summary: Dict[str, Any],
                                          trend: Optional[TrendAnalysis]) -> List[OptimizationRecommendation]:
        """Analyze a specific metric for recommendations."""
        return self.analysis._analyze_metric_for_recommendations(metric_name, summary, trend)
    
    def _generate_system_recommendations(self, metrics_data: List[PerformanceMetrics]) -> List[OptimizationRecommendation]:
        """Generate system-wide optimization recommendations."""
        return self.system._generate_system_recommendations(metrics_data)
    
    def _calculate_metric_summaries(self, metrics_data: List[PerformanceMetrics]) -> Dict[str, Dict[str, Any]]:
        """Calculate summaries for all metrics."""
        return self.analysis._calculate_metric_summaries(metrics_data)
    
    def _is_highly_volatile(self, values: List[float]) -> bool:
        """Check if values are highly volatile."""
        return self.analysis._is_highly_volatile(values)
    
    def _check_resource_optimization(self, metric_summaries: Dict[str, Dict[str, Any]]) -> Optional[OptimizationRecommendation]:
        """Check for resource optimization opportunities."""
        return self.system._check_resource_optimization(metric_summaries)
    
    def _create_metric_recommendation(self, metric_name: str, rec_type: str = "performance", 
                                    description: str = "") -> OptimizationRecommendation:
        """Create a metric-based recommendation."""
        return self.system._create_metric_recommendation(metric_name, rec_type, description)
