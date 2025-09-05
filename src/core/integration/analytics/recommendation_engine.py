"""
Recommendation Engine - V2 Compliant Module
==========================================

Handles optimization recommendation generation for vector integration.
Extracted from vector_integration_analytics_engine.py for V2 compliance.

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


class RecommendationEngine:
    """
    Engine for optimization recommendation generation.
    
    Provides intelligent recommendations based on performance analysis.
    """
    
    def __init__(self, config):
        """Initialize recommendation engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.recommendation_cache: List[OptimizationRecommendation] = []
    
    def generate_recommendations(self, metrics_data: List[PerformanceMetrics],
                               trends: Dict[str, TrendAnalysis]) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations based on analysis."""
        try:
            recommendations = []
            
            # Generate metric-specific recommendations
            metric_recommendations = self._generate_metric_recommendations(metrics_data, trends)
            recommendations.extend(metric_recommendations)
            
            # Generate system-wide recommendations
            system_recommendations = self._generate_system_recommendations(metrics_data)
            recommendations.extend(system_recommendations)
            
            # Cache recommendations
            self.recommendation_cache.extend(recommendations)
            
            self.logger.info(f"Generated {len(recommendations)} optimization recommendations")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return []
    
    def _generate_metric_recommendations(self, metrics_data: List[PerformanceMetrics],
                                       trends: Dict[str, TrendAnalysis]) -> List[OptimizationRecommendation]:
        """Generate recommendations for specific metrics."""
        recommendations = []
        
        # Group metrics by name
        metrics_by_name = {}
        for metric in metrics_data:
            if metric.metric_name not in metrics_by_name:
                metrics_by_name[metric.metric_name] = []
            metrics_by_name[metric.metric_name].append(metric)
        
        # Generate recommendations for each metric
        for metric_name, metric_list in metrics_by_name.items():
            metric_recommendations = self._analyze_metric_for_recommendations(
                metric_name, metric_list, trends.get(metric_name)
            )
            recommendations.extend(metric_recommendations)
        
        return recommendations
    
    def _analyze_metric_for_recommendations(self, metric_name: str, 
                                          metrics: List[PerformanceMetrics],
                                          trend: Optional[TrendAnalysis]) -> List[OptimizationRecommendation]:
        """Analyze metric and generate specific recommendations."""
        recommendations = []
        
        if not metrics:
            return recommendations
        
        # Calculate metric statistics
        values = [m.value for m in metrics]
        current_value = values[-1] if values else 0
        average_value = sum(values) / len(values) if values else 0
        max_value = max(values) if values else 0
        
        # Check for high values
        if current_value > average_value * 1.5:
            rec = self._create_metric_recommendation(metric_name, "high_value")
            recommendations.append(rec)
        
        # Check for increasing trends
        if trend and trend.trend_direction == "increasing" and trend.confidence > 0.7:
            rec = self._create_metric_recommendation(metric_name, "trend")
            recommendations.append(rec)
        
        # Check for volatility
        if self._is_highly_volatile(values):
            rec = self._create_metric_recommendation(metric_name, "volatility")
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_system_recommendations(self, metrics_data: List[PerformanceMetrics]) -> List[OptimizationRecommendation]:
        """Generate system-wide recommendations."""
        recommendations = []
        
        # Calculate metric summaries
        metric_summaries = self._calculate_metric_summaries(metrics_data)
        
        # Check for overall system stress
        high_metrics = []
        for metric_name, summary in metric_summaries.items():
            if summary['current_value'] > summary['average'] * 1.3:
                high_metrics.append(metric_name)
        
        if len(high_metrics) >= 2:
            rec = create_optimization_recommendation(
                recommendation_id=f"rec_system_{int(datetime.now().timestamp())}",
                category="architecture",
                priority="high", 
                title="System-wide Performance Optimization",
                description=f"Multiple metrics showing elevated values. Consider comprehensive optimization.",
                expected_impact="Improve overall system performance by 20-40%",
                implementation_effort="high",
                estimated_improvement=30.0
            )
            recommendations.append(rec)
        
        # Check for resource optimization opportunities
        resource_rec = self._check_resource_optimization(metric_summaries)
        if resource_rec:
            recommendations.append(resource_rec)
        
        return recommendations
    
    def _calculate_metric_summaries(self, metrics_data: List[PerformanceMetrics]) -> Dict[str, Dict[str, Any]]:
        """Calculate summaries for all metrics."""
        summaries = {}
        
        # Group metrics by name
        metrics_by_name = {}
        for metric in metrics_data:
            if metric.metric_name not in metrics_by_name:
                metrics_by_name[metric.metric_name] = []
            metrics_by_name[metric.metric_name].append(metric)
        
        # Calculate summary for each metric
        for metric_name, metric_list in metrics_by_name.items():
            values = [m.value for m in metric_list]
            summaries[metric_name] = {
                'current_value': values[-1] if values else 0,
                'average': sum(values) / len(values) if values else 0,
                'max': max(values) if values else 0,
                'min': min(values) if values else 0,
                'count': len(values)
            }
        
        return summaries
    
    def _is_highly_volatile(self, values: List[float]) -> bool:
        """Check if values are highly volatile."""
        if len(values) < 5:
            return False
        
        # Calculate coefficient of variation
        mean_val = sum(values) / len(values)
        if mean_val == 0:
            return False
        
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        coefficient_of_variation = std_dev / mean_val
        
        return coefficient_of_variation > 0.3
    
    def _check_resource_optimization(self, metric_summaries: Dict[str, Dict[str, Any]]) -> Optional[OptimizationRecommendation]:
        """Check for resource optimization opportunities."""
        resource_metrics = ['memory_usage_percent', 'cpu_usage_percent', 'disk_usage_percent']
        high_resource_metrics = []
        
        for metric in resource_metrics:
            if metric in metric_summaries:
                summary = metric_summaries[metric]
                if summary['current_value'] > 80:  # High resource usage
                    high_resource_metrics.append(metric)
        
        if high_resource_metrics:
            return create_optimization_recommendation(
                recommendation_id=f"rec_resource_{int(datetime.now().timestamp())}",
                category="resource",
                priority="high",
                title="Resource Optimization Required",
                description=f"High resource usage detected in: {', '.join(high_resource_metrics)}",
                expected_impact="Reduce resource usage by 15-30%",
                implementation_effort="medium",
                estimated_improvement=20.0
            )
        
        return None
    
    def _create_metric_recommendation(self, metric_name: str, rec_type: str = "performance") -> OptimizationRecommendation:
        """Create optimization recommendation for metric."""
        recommendations = {
            "response_time_ms": ("Optimize Response Time", "performance", "high", 25.0),
            "memory_usage_percent": ("Optimize Memory Usage", "resource", "medium", 20.0),
            "cpu_usage_percent": ("Optimize CPU Usage", "resource", "medium", 15.0),
            "error_rate_percent": ("Reduce Error Rate", "reliability", "high", 30.0),
            "throughput_ops_sec": ("Improve Throughput", "performance", "medium", 20.0)
        }
        
        title, category, priority, improvement = recommendations.get(
            metric_name, ("General Optimization", "performance", "medium", 10.0)
        )
        
        # Adjust based on recommendation type
        if rec_type == "high_value":
            title = f"High {metric_name} Value - {title}"
            priority = "high"
        elif rec_type == "trend":
            title = f"Increasing {metric_name} Trend - {title}"
            priority = "medium"
        elif rec_type == "volatility":
            title = f"Volatile {metric_name} - Stabilize {title}"
            priority = "medium"
        
        return create_optimization_recommendation(
            recommendation_id=f"rec_{metric_name}_{int(datetime.now().timestamp())}",
            category=category,
            priority=priority,
            title=title,
            description=f"{metric_name} requires optimization. Consider implementing best practices.",
            expected_impact=f"Improve {metric_name} by {improvement}%",
            implementation_effort="medium",
            estimated_improvement=improvement
        )
    
    def get_latest_recommendations(self) -> List[OptimizationRecommendation]:
        """Get latest optimization recommendations."""
        return list(self.recommendation_cache)
    
    def get_recommendations_by_priority(self, priority: str) -> List[OptimizationRecommendation]:
        """Get recommendations by priority level."""
        return [rec for rec in self.recommendation_cache if rec.priority == priority]
    
    def get_recommendations_by_category(self, category: str) -> List[OptimizationRecommendation]:
        """Get recommendations by category."""
        return [rec for rec in self.recommendation_cache if rec.category == category]
    
    def clear_recommendation_cache(self):
        """Clear recommendation cache."""
        self.recommendation_cache.clear()
        self.logger.info("Recommendation cache cleared")
