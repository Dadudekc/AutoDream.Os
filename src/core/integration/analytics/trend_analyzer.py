"""
Trend Analyzer - V2 Compliant Module
===================================

Handles trend analysis and pattern recognition for vector integration.
Extracted from vector_integration_analytics_engine.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import statistics
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import logging

from ..vector_integration_models import (
    TrendAnalysis, PerformanceMetrics, create_trend_analysis
)


class TrendAnalyzer:
    """
    Analyzer for trend analysis and pattern recognition.
    
    Provides trend detection, pattern analysis, and statistical insights.
    """
    
    def __init__(self, config):
        """Initialize trend analyzer."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.trend_cache: Dict[str, TrendAnalysis] = {}
    
    def analyze_trend(self, metrics_data: List[PerformanceMetrics], 
                     metric_name: str) -> Optional[TrendAnalysis]:
        """Analyze trend for specific metric."""
        try:
            # Filter data for metric
            metric_values = [m.value for m in metrics_data 
                           if m.metric_name == metric_name]
            
            if len(metric_values) < self.config.min_data_points_for_analysis:
                return None
            
            # Calculate trend
            trend_direction, trend_strength, confidence = self._calculate_trend(metric_values)
            
            # Create trend analysis
            trend_id = f"trend_{metric_name}_{int(datetime.now().timestamp())}"
            trend = create_trend_analysis(
                trend_id=trend_id,
                metric_name=metric_name,
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                confidence=confidence,
                data_points=len(metric_values)
            )
            
            # Cache the result
            self.trend_cache[metric_name] = trend
            
            self.logger.debug(f"Trend analyzed for {metric_name}: {trend_direction}")
            return trend
            
        except Exception as e:
            self.logger.error(f"Error analyzing trend for {metric_name}: {e}")
            return None
    
    def _calculate_trend(self, values: List[float]) -> Tuple[str, float, float]:
        """Calculate trend direction, strength, and confidence."""
        if len(values) < 3:
            return "stable", 0.0, 0.0
        
        # Calculate moving averages for trend detection
        window_size = min(len(values) // 3, 10)
        if window_size < 3:
            window_size = 3
        
        moving_averages = []
        for i in range(window_size, len(values)):
            avg = statistics.mean(values[i-window_size:i])
            moving_averages.append(avg)
        
        if len(moving_averages) < 2:
            return "stable", 0.0, 0.0
        
        # Calculate trend
        first_half = moving_averages[:len(moving_averages)//2]
        second_half = moving_averages[len(moving_averages)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        # Determine trend direction and strength
        if second_avg > first_avg * 1.05:  # 5% increase threshold
            trend_direction = "increasing"
            trend_strength = min((second_avg - first_avg) / first_avg, 1.0)
        elif second_avg < first_avg * 0.95:  # 5% decrease threshold
            trend_direction = "decreasing"
            trend_strength = min((first_avg - second_avg) / first_avg, 1.0)
        else:
            trend_direction = "stable"
            trend_strength = 1.0 - abs(second_avg - first_avg) / first_avg
        
        # Calculate confidence based on data consistency
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        mean_val = statistics.mean(values)
        confidence = max(0.0, 1.0 - (std_dev / mean_val) if mean_val > 0 else 0.0)
        confidence = min(confidence, 1.0)
        
        return trend_direction, trend_strength, confidence
    
    def get_trend_summary(self, metrics_data: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Get comprehensive trend summary for all metrics."""
        summary = {}
        
        # Group metrics by name
        metrics_by_name = {}
        for metric in metrics_data:
            if metric.metric_name not in metrics_by_name:
                metrics_by_name[metric.metric_name] = []
            metrics_by_name[metric.metric_name].append(metric)
        
        # Analyze trends for each metric
        for metric_name, metric_list in metrics_by_name.items():
            trend = self.analyze_trend(metric_list, metric_name)
            if trend:
                summary[metric_name] = {
                    'trend_direction': trend.trend_direction,
                    'trend_strength': trend.trend_strength,
                    'confidence': trend.confidence,
                    'data_points': trend.data_points
                }
        
        return summary
    
    def detect_patterns(self, values: List[float]) -> List[str]:
        """Detect patterns in time series data."""
        patterns = []
        
        if len(values) < 10:
            return patterns
        
        # Detect cyclical patterns
        if self._has_cyclical_pattern(values):
            patterns.append("cyclical")
        
        # Detect seasonal patterns
        if self._has_seasonal_pattern(values):
            patterns.append("seasonal")
        
        # Detect volatility patterns
        if self._has_high_volatility(values):
            patterns.append("high_volatility")
        
        # Detect stability patterns
        if self._has_stability_pattern(values):
            patterns.append("stable")
        
        return patterns
    
    def _has_cyclical_pattern(self, values: List[float]) -> bool:
        """Check for cyclical patterns in data."""
        if len(values) < 20:
            return False
        
        # Simple cyclical detection using autocorrelation
        window_size = min(len(values) // 4, 10)
        correlations = []
        
        for lag in range(1, window_size):
            if lag < len(values):
                corr = self._calculate_correlation(values[:-lag], values[lag:])
                correlations.append(abs(corr))
        
        # If any correlation is above threshold, consider cyclical
        return max(correlations) > 0.7 if correlations else False
    
    def _has_seasonal_pattern(self, values: List[float]) -> bool:
        """Check for seasonal patterns in data."""
        if len(values) < 24:  # Need at least 24 data points
            return False
        
        # Group by hour of day (assuming hourly data)
        hourly_groups = {}
        for i, value in enumerate(values):
            hour = i % 24
            if hour not in hourly_groups:
                hourly_groups[hour] = []
            hourly_groups[hour].append(value)
        
        # Check if there's significant variation between hours
        hourly_means = [statistics.mean(group) for group in hourly_groups.values()]
        if len(hourly_means) < 2:
            return False
        
        std_dev = statistics.stdev(hourly_means)
        mean_val = statistics.mean(hourly_means)
        
        # If coefficient of variation is high, consider seasonal
        return (std_dev / mean_val) > 0.3 if mean_val > 0 else False
    
    def _has_high_volatility(self, values: List[float]) -> bool:
        """Check for high volatility in data."""
        if len(values) < 5:
            return False
        
        std_dev = statistics.stdev(values)
        mean_val = statistics.mean(values)
        
        # High volatility if coefficient of variation > 0.5
        return (std_dev / mean_val) > 0.5 if mean_val > 0 else False
    
    def _has_stability_pattern(self, values: List[float]) -> bool:
        """Check for stability patterns in data."""
        if len(values) < 5:
            return False
        
        std_dev = statistics.stdev(values)
        mean_val = statistics.mean(values)
        
        # Stable if coefficient of variation < 0.1
        return (std_dev / mean_val) < 0.1 if mean_val > 0 else True
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate correlation coefficient between two lists."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = (sum((xi - mean_x) ** 2 for xi in x) * 
                      sum((yi - mean_y) ** 2 for yi in y)) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def get_cached_trends(self) -> Dict[str, TrendAnalysis]:
        """Get cached trend analyses."""
        return dict(self.trend_cache)
    
    def clear_trend_cache(self):
        """Clear trend analysis cache."""
        self.trend_cache.clear()
        self.logger.info("Trend cache cleared")
