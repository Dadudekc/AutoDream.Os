"""
V3-006 Trend Analysis Engine
Historical performance analysis and trend detection
"""

import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class TrendDirection(Enum):
    """Trend direction indicators"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"

class AnalysisPeriod(Enum):
    """Analysis time periods"""
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1m"

@dataclass
class TrendPoint:
    """Single trend analysis point"""
    timestamp: datetime
    value: float
    trend: TrendDirection
    confidence: float
    change_percent: float

@dataclass
class TrendAnalysis:
    """Complete trend analysis result"""
    metric_name: str
    period: AnalysisPeriod
    overall_trend: TrendDirection
    trend_points: List[TrendPoint]
    average_value: float
    max_value: float
    min_value: float
    volatility: float
    confidence_score: float
    recommendations: List[str]

class TrendAnalyzer:
    """Core trend analysis engine"""
    
    def __init__(self):
        self.trend_threshold = 0.1  # 10% change threshold
        self.volatility_threshold = 0.2  # 20% volatility threshold
        self.min_data_points = 10
        
    def analyze_trend(self, data_points: List[Dict[str, Any]], 
                     metric_name: str, 
                     period: AnalysisPeriod = AnalysisPeriod.DAY) -> TrendAnalysis:
        """Analyze trend for given data points"""
        if len(data_points) < self.min_data_points:
            return self._create_empty_analysis(metric_name, period)
            
        # Extract values and timestamps
        values = [point["value"] for point in data_points]
        timestamps = [datetime.fromisoformat(point["timestamp"]) for point in data_points]
        
        # Calculate basic statistics
        avg_value = statistics.mean(values)
        max_value = max(values)
        min_value = min(values)
        volatility = self._calculate_volatility(values)
        
        # Analyze trend direction
        overall_trend = self._determine_overall_trend(values)
        
        # Generate trend points
        trend_points = self._generate_trend_points(timestamps, values)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(values, overall_trend)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            overall_trend, volatility, avg_value, max_value, min_value
        )
        
        return TrendAnalysis(
            metric_name=metric_name,
            period=period,
            overall_trend=overall_trend,
            trend_points=trend_points,
            average_value=avg_value,
            max_value=max_value,
            min_value=min_value,
            volatility=volatility,
            confidence_score=confidence,
            recommendations=recommendations
        )
        
    def _create_empty_analysis(self, metric_name: str, period: AnalysisPeriod) -> TrendAnalysis:
        """Create empty analysis for insufficient data"""
        return TrendAnalysis(
            metric_name=metric_name,
            period=period,
            overall_trend=TrendDirection.STABLE,
            trend_points=[],
            average_value=0.0,
            max_value=0.0,
            min_value=0.0,
            volatility=0.0,
            confidence_score=0.0,
            recommendations=["Insufficient data for trend analysis"]
        )
        
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate volatility (coefficient of variation)"""
        if not values or len(values) < 2:
            return 0.0
            
        mean_val = statistics.mean(values)
        if mean_val == 0:
            return 0.0
            
        variance = statistics.variance(values)
        std_dev = variance ** 0.5
        return std_dev / mean_val
        
    def _determine_overall_trend(self, values: List[float]) -> TrendDirection:
        """Determine overall trend direction"""
        if len(values) < 3:
            return TrendDirection.STABLE
            
        # Calculate linear regression slope
        n = len(values)
        x_values = list(range(n))
        
        # Simple linear regression
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Determine trend based on slope and volatility
        volatility = self._calculate_volatility(values)
        
        if volatility > self.volatility_threshold:
            return TrendDirection.VOLATILE
        elif slope > self.trend_threshold:
            return TrendDirection.INCREASING
        elif slope < -self.trend_threshold:
            return TrendDirection.DECREASING
        else:
            return TrendDirection.STABLE
            
    def _generate_trend_points(self, timestamps: List[datetime], 
                             values: List[float]) -> List[TrendPoint]:
        """Generate trend points for visualization"""
        trend_points = []
        
        for i, (timestamp, value) in enumerate(zip(timestamps, values)):
            # Calculate change from previous point
            if i == 0:
                change_percent = 0.0
                trend = TrendDirection.STABLE
            else:
                prev_value = values[i-1]
                change_percent = ((value - prev_value) / prev_value) * 100 if prev_value != 0 else 0
                
                if change_percent > self.trend_threshold * 100:
                    trend = TrendDirection.INCREASING
                elif change_percent < -self.trend_threshold * 100:
                    trend = TrendDirection.DECREASING
                else:
                    trend = TrendDirection.STABLE
                    
            # Calculate confidence (simplified)
            confidence = min(1.0, max(0.0, 1.0 - abs(change_percent) / 50.0))
            
            trend_points.append(TrendPoint(
                timestamp=timestamp,
                value=value,
                trend=trend,
                confidence=confidence,
                change_percent=change_percent
            ))
            
        return trend_points
        
    def _calculate_confidence(self, values: List[float], trend: TrendDirection) -> float:
        """Calculate confidence score for trend analysis"""
        if len(values) < 3:
            return 0.0
            
        # Calculate R-squared for linear trend
        n = len(values)
        x_values = list(range(n))
        
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)
        sum_y2 = sum(y * y for y in values)
        
        # Calculate correlation coefficient
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        if denominator == 0:
            return 0.0
            
        correlation = numerator / denominator
        r_squared = correlation * correlation
        
        # Adjust confidence based on data points and volatility
        data_confidence = min(1.0, len(values) / 50.0)  # More data = higher confidence
        volatility = self._calculate_volatility(values)
        volatility_penalty = min(0.5, volatility * 2)  # High volatility reduces confidence
        
        return max(0.0, min(1.0, r_squared * data_confidence - volatility_penalty))
        
    def _generate_recommendations(self, trend: TrendDirection, volatility: float, 
                                avg_value: float, max_value: float, 
                                min_value: float) -> List[str]:
        """Generate recommendations based on trend analysis"""
        recommendations = []
        
        if trend == TrendDirection.INCREASING:
            if avg_value > 80:  # High values
                recommendations.append("Consider scaling resources - values are increasing and high")
            else:
                recommendations.append("Monitor trend - values are increasing but within normal range")
                
        elif trend == TrendDirection.DECREASING:
            if avg_value < 20:  # Low values
                recommendations.append("Values are decreasing and low - check for potential issues")
            else:
                recommendations.append("Positive trend - values are decreasing to optimal levels")
                
        elif trend == TrendDirection.VOLATILE:
            recommendations.append("High volatility detected - investigate root causes")
            recommendations.append("Consider implementing smoothing or filtering")
            
        if volatility > self.volatility_threshold:
            recommendations.append("High volatility - implement monitoring alerts")
            
        if max_value - min_value > avg_value * 2:  # Large range
            recommendations.append("Large value range detected - check for outliers")
            
        return recommendations

class PerformanceTrendAnalyzer:
    """Main performance trend analysis system"""
    
    def __init__(self):
        self.analyzer = TrendAnalyzer()
        self.historical_data: Dict[str, List[Dict[str, Any]]] = {}
        
    def add_data_point(self, metric_name: str, value: float, timestamp: datetime = None):
        """Add data point for trend analysis"""
        if timestamp is None:
            timestamp = datetime.now()
            
        if metric_name not in self.historical_data:
            self.historical_data[metric_name] = []
            
        self.historical_data[metric_name].append({
            "timestamp": timestamp.isoformat(),
            "value": value
        })
        
        # Keep only last 1000 data points per metric
        if len(self.historical_data[metric_name]) > 1000:
            self.historical_data[metric_name] = self.historical_data[metric_name][-1000:]
            
    def analyze_metric_trend(self, metric_name: str, 
                           period: AnalysisPeriod = AnalysisPeriod.DAY) -> TrendAnalysis:
        """Analyze trend for specific metric"""
        if metric_name not in self.historical_data:
            return self.analyzer._create_empty_analysis(metric_name, period)
            
        data_points = self.historical_data[metric_name]
        return self.analyzer.analyze_trend(data_points, metric_name, period)
        
    def get_all_trends(self, period: AnalysisPeriod = AnalysisPeriod.DAY) -> Dict[str, TrendAnalysis]:
        """Get trend analysis for all metrics"""
        trends = {}
        
        for metric_name in self.historical_data:
            trends[metric_name] = self.analyze_metric_trend(metric_name, period)
            
        return trends
        
    def get_trend_summary(self, period: AnalysisPeriod = AnalysisPeriod.DAY) -> Dict[str, Any]:
        """Get summary of all trends"""
        trends = self.get_all_trends(period)
        
        summary = {
            "analysis_period": period.value,
            "total_metrics": len(trends),
            "trend_distribution": {
                "increasing": 0,
                "decreasing": 0,
                "stable": 0,
                "volatile": 0
            },
            "high_confidence_trends": 0,
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }
        
        all_recommendations = []
        
        for metric_name, trend in trends.items():
            # Count trend directions
            summary["trend_distribution"][trend.overall_trend.value] += 1
            
            # Count high confidence trends
            if trend.confidence_score > 0.7:
                summary["high_confidence_trends"] += 1
                
            # Collect recommendations
            all_recommendations.extend(trend.recommendations)
            
        # Deduplicate and limit recommendations
        summary["recommendations"] = list(set(all_recommendations))[:10]
        
        return summary

# Global trend analyzer instance
trend_analyzer = PerformanceTrendAnalyzer()

def add_performance_data(metric_name: str, value: float, timestamp: datetime = None):
    """Add performance data point for trend analysis"""
    trend_analyzer.add_data_point(metric_name, value, timestamp)

def analyze_performance_trend(metric_name: str, period: AnalysisPeriod = AnalysisPeriod.DAY) -> TrendAnalysis:
    """Analyze performance trend for metric"""
    return trend_analyzer.analyze_metric_trend(metric_name, period)

def get_performance_trends_summary(period: AnalysisPeriod = AnalysisPeriod.DAY) -> Dict[str, Any]:
    """Get summary of all performance trends"""
    return trend_analyzer.get_trend_summary(period)

if __name__ == "__main__":
    # Test trend analysis with sample data
    import random
    
    # Generate sample data
    base_value = 50.0
    for i in range(100):
        value = base_value + random.uniform(-10, 10) + (i * 0.1)  # Slight upward trend
        timestamp = datetime.now() - timedelta(hours=100-i)
        add_performance_data("cpu_usage", value, timestamp)
        
    # Analyze trends
    trend = analyze_performance_trend("cpu_usage")
    print(f"CPU Usage Trend: {trend.overall_trend.value}")
    print(f"Confidence: {trend.confidence_score:.2f}")
    print(f"Recommendations: {trend.recommendations}")
    
    summary = get_performance_trends_summary()
    print(f"Trend Summary: {summary}")


