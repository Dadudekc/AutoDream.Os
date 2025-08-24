#!/usr/bin/env python3
"""
Error Trend Analyzer - V2 Error Trend Analysis
==============================================
Specialized module for analyzing error trends over time
from error analytics data. Follows V2 standards with advanced
trend detection and forecasting capabilities.
"""

from __future__ import annotations

import logging
import statistics
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict

# Import our error handling system
from src.core.error_handler import (
    ErrorHandler,
    ErrorInfo,
    ErrorSeverity,
)

# ──────────────────────────── Logging
log = logging.getLogger("error_trend_analyzer")


@dataclass
class ErrorTrend:
    """Error trend information"""
    
    time_period: str
    error_count: int
    severity_distribution: Dict[ErrorSeverity, int]
    category_distribution: Dict[str, int]
    recovery_success_rate: float
    average_resolution_time: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: float  # 0.0 to 1.0


@dataclass
class TrendAnalysisResult:
    """Result of trend analysis"""
    
    period_start: datetime
    period_end: datetime
    total_errors: int
    trends: List[ErrorTrend]
    overall_trend: str
    trend_confidence: float
    seasonal_patterns: Dict[str, Any]
    forecast_predictions: List[Dict[str, Any]]


class ErrorTrendAnalyzer:
    """Advanced error trend analysis and forecasting"""

    def __init__(self, error_handler: ErrorHandler, config: Optional[Dict[str, Any]] = None):
        self.error_handler = error_handler
        self.config = config or {}
        self.trends: List[ErrorTrend] = []
        
        # Configuration
        self.trend_window_hours = self.config.get("trend_window_hours", 24)
        self.analysis_interval_hours = self.config.get("analysis_interval_hours", 1)
        self.minimum_data_points = self.config.get("minimum_data_points", 5)
        
    def analyze_error_trends(self) -> List[ErrorTrend]:
        """Analyze error trends over time"""
        try:
            # Get recent errors
            recent_errors = self.error_handler.get_error_history(limit=1000)
            
            if not recent_errors:
                return []
            
            # Group errors by time periods
            time_periods = self._group_errors_by_time_periods(recent_errors)
            
            # Create trend objects
            new_trends = []
            for hour_key, period_data in time_periods.items():
                trend = self._create_trend_from_period(hour_key, period_data)
                if trend:
                    new_trends.append(trend)
            
            # Analyze trend direction and strength
            self._analyze_trend_direction_and_strength(new_trends)
            
            # Update stored trends
            self.trends = new_trends
            
            log.info(f"Analyzed {len(new_trends)} error trends")
            return self.trends
            
        except Exception as e:
            log.error(f"Error in trend analysis: {e}")
            return []
    
    def _group_errors_by_time_periods(self, errors: List[ErrorInfo]) -> Dict[datetime, Dict[str, Any]]:
        """Group errors by time periods for analysis"""
        try:
            time_periods = {}
            
            for error in errors:
                # Round to nearest hour
                hour_key = error.timestamp.replace(minute=0, second=0, microsecond=0)
                
                if hour_key not in time_periods:
                    time_periods[hour_key] = {
                        "errors": [],
                        "severity_counts": defaultdict(int),
                        "category_counts": defaultdict(int),
                        "recovery_successes": 0,
                        "total_errors": 0,
                        "resolution_times": [],
                    }
                
                period = time_periods[hour_key]
                period["errors"].append(error)
                period["severity_counts"][error.severity] += 1
                period["category_counts"][error.category] += 1
                period["total_errors"] += 1
                
                if error.resolved:
                    period["recovery_successes"] += 1
                    if error.resolution_time:
                        resolution_time = (
                            error.resolution_time - error.timestamp
                        ).total_seconds() / 60
                        period["resolution_times"].append(resolution_time)
            
            return time_periods
            
        except Exception as e:
            log.error(f"Error grouping errors by time periods: {e}")
            return {}
    
    def _create_trend_from_period(self, hour_key: datetime, period_data: Dict[str, Any]) -> Optional[ErrorTrend]:
        """Create a trend object from period data"""
        try:
            recovery_rate = (
                (period_data["recovery_successes"] / period_data["total_errors"] * 100)
                if period_data["total_errors"] > 0
                else 0.0
            )
            
            avg_resolution = (
                statistics.mean(period_data["resolution_times"])
                if period_data["resolution_times"]
                else 0.0
            )
            
            trend = ErrorTrend(
                time_period=hour_key.strftime("%Y-%m-%d %H:00"),
                error_count=period_data["total_errors"],
                severity_distribution=dict(period_data["severity_counts"]),
                category_distribution=dict(period_data["category_counts"]),
                recovery_success_rate=recovery_rate,
                average_resolution_time=avg_resolution,
                trend_direction="stable",  # Will be calculated later
                trend_strength=0.0  # Will be calculated later
            )
            
            return trend
            
        except Exception as e:
            log.error(f"Error creating trend from period: {e}")
            return None
    
    def _analyze_trend_direction_and_strength(self, trends: List[ErrorTrend]):
        """Analyze the direction and strength of trends"""
        try:
            if len(trends) < 2:
                return
            
            # Calculate trend direction and strength
            for i in range(1, len(trends)):
                current = trends[i]
                previous = trends[i - 1]
                
                # Calculate error count change
                error_change = current.error_count - previous.error_count
                change_percentage = (error_change / previous.error_count * 100) if previous.error_count > 0 else 0
                
                # Determine trend direction
                if change_percentage > 10:
                    current.trend_direction = "increasing"
                elif change_percentage < -10:
                    current.trend_direction = "decreasing"
                else:
                    current.trend_direction = "stable"
                
                # Calculate trend strength (0.0 to 1.0)
                current.trend_strength = min(1.0, abs(change_percentage) / 50.0)
                
        except Exception as e:
            log.error(f"Error analyzing trend direction and strength: {e}")
    
    def get_trend_statistics(self) -> Dict[str, Any]:
        """Get trend analysis statistics"""
        try:
            if not self.trends:
                return {}
            
            increasing_trends = [t for t in self.trends if t.trend_direction == "increasing"]
            decreasing_trends = [t for t in self.trends if t.trend_direction == "decreasing"]
            stable_trends = [t for t in self.trends if t.trend_direction == "stable"]
            
            avg_recovery_rate = statistics.mean([t.recovery_success_rate for t in self.trends])
            avg_resolution_time = statistics.mean([t.average_resolution_time for t in self.trends])
            
            return {
                "total_trends": len(self.trends),
                "increasing_trends": len(increasing_trends),
                "decreasing_trends": len(decreasing_trends),
                "stable_trends": len(stable_trends),
                "average_recovery_rate": avg_recovery_rate,
                "average_resolution_time": avg_resolution_time,
                "trend_confidence": len(self.trends) / max(self.trend_window_hours, 1)
            }
            
        except Exception as e:
            log.error(f"Error getting trend statistics: {e}")
            return {}
    
    def get_trends_by_direction(self, direction: str) -> List[ErrorTrend]:
        """Get trends filtered by direction"""
        try:
            return [t for t in self.trends if t.trend_direction == direction]
        except Exception as e:
            log.error(f"Error getting trends by direction: {e}")
            return []
    
    def get_trends_by_time_range(self, start_time: datetime, end_time: datetime) -> List[ErrorTrend]:
        """Get trends within a specific time range"""
        try:
            filtered_trends = []
            
            for trend in self.trends:
                # Parse trend time period
                try:
                    trend_time = datetime.strptime(trend.time_period, "%Y-%m-%d %H:00")
                    if start_time <= trend_time <= end_time:
                        filtered_trends.append(trend)
                except ValueError:
                    continue
            
            return filtered_trends
            
        except Exception as e:
            log.error(f"Error getting trends by time range: {e}")
            return []
    
    def detect_seasonal_patterns(self) -> Dict[str, Any]:
        """Detect seasonal patterns in error trends"""
        try:
            if len(self.trends) < 24:  # Need at least 24 hours of data
                return {}
            
            # Group by hour of day
            hourly_patterns = defaultdict(list)
            
            for trend in self.trends:
                try:
                    trend_time = datetime.strptime(trend.time_period, "%Y-%m-%d %H:00")
                    hour = trend_time.hour
                    hourly_patterns[hour].append(trend.error_count)
                except ValueError:
                    continue
            
            # Calculate average errors per hour
            seasonal_patterns = {}
            for hour, counts in hourly_patterns.items():
                if counts:
                    seasonal_patterns[f"hour_{hour:02d}"] = {
                        "average_errors": statistics.mean(counts),
                        "min_errors": min(counts),
                        "max_errors": max(counts),
                        "data_points": len(counts)
                    }
            
            return seasonal_patterns
            
        except Exception as e:
            log.error(f"Error detecting seasonal patterns: {e}")
            return {}
    
    def generate_trend_forecast(self, hours_ahead: int = 24) -> List[Dict[str, Any]]:
        """Generate trend forecasts for future time periods"""
        try:
            if len(self.trends) < self.minimum_data_points:
                return []
            
            # Simple linear regression for forecasting
            recent_trends = self.trends[-self.minimum_data_points:]
            x_values = list(range(len(recent_trends)))
            y_values = [t.error_count for t in recent_trends]
            
            if len(x_values) < 2:
                return []
            
            # Calculate slope and intercept
            n = len(x_values)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_xy = sum(x * y for x, y in zip(x_values, y_values))
            sum_x2 = sum(x * x for x in x_values)
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Generate forecasts
            forecasts = []
            for i in range(1, hours_ahead + 1):
                predicted_errors = max(0, slope * (n + i) + intercept)
                
                forecast = {
                    "time_period": f"forecast_{i}_hours",
                    "predicted_error_count": round(predicted_errors, 2),
                    "confidence": max(0.1, 1.0 - (i * 0.05)),  # Confidence decreases with time
                    "trend_direction": "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
                }
                forecasts.append(forecast)
            
            return forecasts
            
        except Exception as e:
            log.error(f"Error generating trend forecast: {e}")
            return []
    
    def get_comprehensive_trend_analysis(self) -> TrendAnalysisResult:
        """Get comprehensive trend analysis including forecasts"""
        try:
            # Analyze current trends
            trends = self.analyze_error_trends()
            
            # Get statistics
            stats = self.get_trend_statistics()
            
            # Detect seasonal patterns
            seasonal_patterns = self.detect_seasonal_patterns()
            
            # Generate forecasts
            forecasts = self.generate_trend_forecast()
            
            # Determine overall trend
            overall_trend = "stable"
            if trends:
                recent_trends = trends[-3:]  # Last 3 trends
                increasing_count = len([t for t in recent_trends if t.trend_direction == "increasing"])
                decreasing_count = len([t for t in recent_trends if t.trend_direction == "decreasing"])
                
                if increasing_count > decreasing_count:
                    overall_trend = "increasing"
                elif decreasing_count > increasing_count:
                    overall_trend = "decreasing"
            
            # Calculate confidence
            trend_confidence = min(1.0, len(trends) / 24.0)  # Higher confidence with more data
            
            result = TrendAnalysisResult(
                period_start=trends[0].time_period if trends else "",
                period_end=trends[-1].time_period if trends else "",
                total_errors=sum(t.error_count for t in trends),
                trends=trends,
                overall_trend=overall_trend,
                trend_confidence=trend_confidence,
                seasonal_patterns=seasonal_patterns,
                forecast_predictions=forecasts
            )
            
            return result
            
        except Exception as e:
            log.error(f"Error getting comprehensive trend analysis: {e}")
            return None
    
    def shutdown(self):
        """Shutdown the trend analyzer"""
        self.trends.clear()
        log.info("Error Trend Analyzer shutdown complete")
