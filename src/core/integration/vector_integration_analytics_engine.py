"""
Vector Integration Analytics Engine - V2 Compliant Module
========================================================

Main analytics engine that coordinates all analytics components.
Refactored from monolithic vector_integration_analytics_engine.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from ..vector_integration_models import (
    TrendAnalysis, PerformanceForecast, OptimizationRecommendation,
    PerformanceMetrics, IntegrationConfig, create_default_config
)
from .trend_analyzer import TrendAnalyzer
from .forecast_generator import ForecastGenerator
from .recommendation_engine import RecommendationEngine


class VectorIntegrationAnalyticsEngine:
    """
    Main analytics engine for vector integration analysis.
    
    Coordinates trend analysis, forecasting, and recommendation generation.
    """
    
    def __init__(self, config: Optional[IntegrationConfig] = None):
        """Initialize analytics engine."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()
        
        # Initialize components
        self.trend_analyzer = TrendAnalyzer(self.config)
        self.forecast_generator = ForecastGenerator(self.config)
        self.recommendation_engine = RecommendationEngine(self.config)
        
        self.logger.info("Vector Integration Analytics Engine initialized")
    
    def analyze_performance_data(self, metrics_data: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Comprehensive analysis of performance data."""
        try:
            # Perform trend analysis
            trends = self.trend_analyzer.get_trend_summary(metrics_data)
            
            # Generate forecasts
            forecasts = self.forecast_generator.generate_multi_metric_forecast(metrics_data)
            
            # Generate recommendations
            trend_objects = {name: self.trend_analyzer.analyze_trend(metrics_data, name) 
                           for name in trends.keys()}
            recommendations = self.recommendation_engine.generate_recommendations(
                metrics_data, trend_objects
            )
            
            # Compile results
            analysis_result = {
                'trends': trends,
                'forecasts': {name: forecast.to_dict() for name, forecast in forecasts.items()},
                'recommendations': [rec.to_dict() for rec in recommendations],
                'analysis_timestamp': datetime.now().isoformat(),
                'total_metrics': len(metrics_data),
                'analyzed_metrics': len(trends)
            }
            
            self.logger.info(f"Performance analysis completed: {len(trends)} trends, "
                           f"{len(forecasts)} forecasts, {len(recommendations)} recommendations")
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error in performance analysis: {e}")
            return {'error': str(e)}
    
    def get_trend_analysis(self, metrics_data: List[PerformanceMetrics], 
                          metric_name: str) -> Optional[TrendAnalysis]:
        """Get trend analysis for specific metric."""
        return self.trend_analyzer.analyze_trend(metrics_data, metric_name)
    
    def get_performance_forecast(self, metrics_data: List[PerformanceMetrics],
                                metric_name: str) -> Optional[PerformanceForecast]:
        """Get performance forecast for specific metric."""
        return self.forecast_generator.generate_forecast(metrics_data, metric_name)
    
    def get_optimization_recommendations(self, metrics_data: List[PerformanceMetrics]) -> List[OptimizationRecommendation]:
        """Get optimization recommendations."""
        trends = {}
        for metric in metrics_data:
            if metric.metric_name not in trends:
                trend = self.trend_analyzer.analyze_trend([metric], metric.metric_name)
                if trend:
                    trends[metric.metric_name] = trend
        
        return self.recommendation_engine.generate_recommendations(metrics_data, trends)
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get comprehensive analytics summary."""
        return {
            'trends': {
                'cached_count': len(self.trend_analyzer.get_cached_trends()),
                'analyzer_status': 'active'
            },
            'forecasts': {
                'cached_count': len(self.forecast_generator.get_cached_forecasts()),
                'generator_status': 'active'
            },
            'recommendations': {
                'cached_count': len(self.recommendation_engine.get_latest_recommendations()),
                'engine_status': 'active'
            },
            'configuration': {
                'min_data_points_for_analysis': self.config.min_data_points_for_analysis,
                'min_data_points_for_forecast': self.config.min_data_points_for_forecast,
                'forecast_horizon_hours': self.config.forecast_horizon_hours
            }
        }
    
    def clear_all_caches(self):
        """Clear all analytics caches."""
        self.trend_analyzer.clear_trend_cache()
        self.forecast_generator.clear_forecast_cache()
        self.recommendation_engine.clear_recommendation_cache()
        self.logger.info("All analytics caches cleared")
    
    def get_cached_trends(self) -> Dict[str, TrendAnalysis]:
        """Get cached trend analyses."""
        return self.trend_analyzer.get_cached_trends()
    
    def get_cached_forecasts(self) -> Dict[str, PerformanceForecast]:
        """Get cached forecasts."""
        return self.forecast_generator.get_cached_forecasts()
    
    def get_latest_recommendations(self) -> List[OptimizationRecommendation]:
        """Get latest optimization recommendations."""
        return self.recommendation_engine.get_latest_recommendations()
    
    def validate_forecast_accuracy(self, forecast: PerformanceForecast, 
                                  actual_values: List[float]) -> float:
        """Validate forecast accuracy against actual values."""
        return self.forecast_generator.validate_forecast_accuracy(forecast, actual_values)
    
    def get_recommendations_by_priority(self, priority: str) -> List[OptimizationRecommendation]:
        """Get recommendations by priority level."""
        return self.recommendation_engine.get_recommendations_by_priority(priority)
    
    def get_recommendations_by_category(self, category: str) -> List[OptimizationRecommendation]:
        """Get recommendations by category."""
        return self.recommendation_engine.get_recommendations_by_category(category)
