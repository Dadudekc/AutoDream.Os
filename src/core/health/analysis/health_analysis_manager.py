#!/usr/bin/env python3
"""
Health Analysis Manager - V2 Modular Architecture
================================================

Handles health trend analysis, predictions, and health insights.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from ..types.health_types import HealthMetric, HealthLevel, HealthTrend


logger = logging.getLogger(__name__)


class HealthAnalysisManager:
    """
    Health Analysis Manager - Single responsibility: Analyze health data
    
    Handles all health analysis operations including:
    - Trend analysis and prediction
    - Health issue prediction
    - Optimization recommendations
    - Performance insights
    """

    def __init__(self):
        """Initialize health analysis manager"""
        self.logger = logging.getLogger(f"{__name__}.HealthAnalysisManager")
        
        # Analysis configuration
        self.trend_analysis_window = 24  # hours
        self.prediction_horizon = 6      # hours
        self.confidence_threshold = 0.7
        
        self.logger.info("✅ Health Analysis Manager initialized successfully")

    def analyze_health_trends(self, metrics: Dict[str, HealthMetric], 
                             time_range_hours: int = 24) -> Dict[str, HealthTrend]:
        """Analyze health trends for predictive insights"""
        try:
            trends = {}
            
            for metric_name, metric in metrics.items():
                trend = self._analyze_single_metric_trend(metric, time_range_hours)
                if trend:
                    trends[metric_name] = trend
            
            self.logger.info(f"Health trend analysis completed: {len(trends)} metrics analyzed")
            return trends
            
        except Exception as e:
            self.logger.error(f"Failed to analyze health trends: {e}")
            return {}

    def _analyze_single_metric_trend(self, metric: HealthMetric, 
                                    time_range_hours: int) -> Optional[HealthTrend]:
        """Analyze trend for a single metric"""
        try:
            # For now, use current trend from metric
            # In a real system, this would analyze historical data
            
            current_value = metric.value
            previous_value = current_value * 0.95  # Simulate previous value
            
            # Calculate change percentage
            if previous_value > 0:
                change_percent = ((current_value - previous_value) / previous_value) * 100
            else:
                change_percent = 0.0
            
            # Determine trend direction and strength
            if change_percent > 10:
                trend_direction = "increasing"
                trend_strength = "strong"
            elif change_percent > 5:
                trend_direction = "increasing"
                trend_strength = "moderate"
            elif change_percent > 1:
                trend_direction = "increasing"
                trend_strength = "weak"
            elif change_percent < -10:
                trend_direction = "decreasing"
                trend_strength = "strong"
            elif change_percent < -5:
                trend_direction = "decreasing"
                trend_strength = "moderate"
            elif change_percent < -1:
                trend_direction = "decreasing"
                trend_strength = "weak"
            else:
                trend_direction = "stable"
                trend_strength = "weak"
            
            # Calculate confidence based on trend strength
            confidence_map = {
                "strong": 0.9,
                "moderate": 0.7,
                "weak": 0.5
            }
            confidence = confidence_map.get(trend_strength, 0.5)
            
            trend = HealthTrend(
                metric_name=metric.name,
                current_value=current_value,
                previous_value=previous_value,
                change_percent=change_percent,
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                prediction_hours=self.prediction_horizon,
                confidence=confidence
            )
            
            return trend
            
        except Exception as e:
            self.logger.error(f"Failed to analyze trend for {metric.name}: {e}")
            return None

    def predict_health_issues(self, metrics: Dict[str, HealthMetric], 
                             time_horizon_hours: int = 6) -> List[Dict[str, Any]]:
        """Predict potential health issues based on current metrics"""
        try:
            predictions = []
            
            for metric_name, metric in metrics.items():
                prediction = self._predict_metric_issues(metric, time_horizon_hours)
                if prediction:
                    predictions.append(prediction)
            
            self.logger.info(f"Health issue prediction completed: {len(predictions)} issues identified")
            return predictions
            
        except Exception as e:
            self.logger.error(f"Failed to predict health issues: {e}")
            return []

    def _predict_metric_issues(self, metric: HealthMetric, 
                              time_horizon_hours: int) -> Optional[Dict[str, Any]]:
        """Predict issues for a single metric"""
        try:
            predictions = []
            
            # Check for threshold violations
            if metric.threshold_max and metric.value > metric.threshold_max * 0.8:
                prediction = {
                    "metric_name": metric.name,
                    "issue_type": "threshold_violation_imminent",
                    "probability": 0.8,
                    "estimated_time_to_violation": time_horizon_hours * 0.5,
                    "severity": "high" if metric.value > metric.threshold_max * 0.9 else "medium",
                    "recommended_action": "Monitor closely and prepare mitigation"
                }
                predictions.append(prediction)
            
            # Check for deteriorating trends
            if metric.trend == "increasing" and metric.threshold_max:
                if metric.value > metric.threshold_max * 0.6:
                    prediction = {
                        "metric_name": metric.name,
                        "issue_type": "performance_degradation",
                        "probability": 0.6,
                        "estimated_time_to_violation": time_horizon_hours * 0.8,
                        "severity": "medium",
                        "recommended_action": "Investigate root cause and implement optimizations"
                    }
                    predictions.append(prediction)
            
            # Check for resource exhaustion
            if metric.name in ["memory_usage", "disk_usage"] and metric.value > 80:
                prediction = {
                    "metric_name": metric.name,
                    "issue_type": "resource_exhaustion",
                    "probability": 0.9,
                    "estimated_time_to_violation": time_horizon_hours * 0.3,
                    "severity": "critical",
                    "recommended_action": "Immediate action required - expand resources"
                }
                predictions.append(prediction)
            
            # Return first prediction if any found
            return predictions[0] if predictions else None
            
        except Exception as e:
            self.logger.error(f"Failed to predict issues for {metric.name}: {e}")
            return None

    def generate_optimization_recommendations(self, metrics: Dict[str, HealthMetric], 
                                           trends: Dict[str, HealthTrend]) -> List[str]:
        """Generate optimization recommendations based on metrics and trends"""
        try:
            recommendations = []
            
            for metric_name, metric in metrics.items():
                metric_recommendations = self._generate_metric_recommendations(metric, trends.get(metric_name))
                recommendations.extend(metric_recommendations)
            
            # Add general recommendations
            general_recommendations = self._generate_general_recommendations(metrics, trends)
            recommendations.extend(general_recommendations)
            
            # Remove duplicates and return
            unique_recommendations = list(set(recommendations))
            self.logger.info(f"Generated {len(unique_recommendations)} optimization recommendations")
            return unique_recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate optimization recommendations: {e}")
            return ["Unable to generate optimization recommendations"]

    def _generate_metric_recommendations(self, metric: HealthMetric, 
                                       trend: Optional[HealthTrend]) -> List[str]:
        """Generate recommendations for a specific metric"""
        try:
            recommendations = []
            
            # CPU recommendations
            if metric.name == "cpu_usage":
                if metric.value > 80.0:
                    recommendations.append("Consider CPU optimization or scaling")
                if trend and trend.trend_direction == "increasing" and trend.trend_strength == "strong":
                    recommendations.append("CPU usage trending upward - investigate workload patterns")
            
            # Memory recommendations
            elif metric.name == "memory_usage":
                if metric.value > 75.0:
                    recommendations.append("Optimize memory usage or increase memory allocation")
                if trend and trend.trend_direction == "increasing":
                    recommendations.append("Memory usage increasing - check for memory leaks")
            
            # Disk recommendations
            elif metric.name == "disk_usage":
                if metric.value > 85.0:
                    recommendations.append("Clean up disk space or expand storage capacity")
                if trend and trend.trend_direction == "increasing":
                    recommendations.append("Disk usage growing - implement log rotation and cleanup")
            
            # Network recommendations
            elif metric.name.startswith("network_"):
                if trend and trend.trend_direction == "increasing" and trend.trend_strength == "strong":
                    recommendations.append("Network traffic increasing - monitor bandwidth usage")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations for {metric.name}: {e}")
            return []

    def _generate_general_recommendations(self, metrics: Dict[str, HealthMetric], 
                                        trends: Dict[str, HealthTrend]) -> List[str]:
        """Generate general system recommendations"""
        try:
            recommendations = []
            
            # Count critical metrics
            critical_count = len([
                metric for metric in metrics.values()
                if metric.current_level in [HealthLevel.CRITICAL, HealthLevel.EMERGENCY]
            ])
            
            if critical_count > 0:
                recommendations.append(f"Immediate attention required for {critical_count} critical metrics")
            
            # Check for overall system health
            excellent_count = len([
                metric for metric in metrics.values()
                if metric.current_level == HealthLevel.EXCELLENT
            ])
            
            if excellent_count < len(metrics) * 0.5:
                recommendations.append("System health below optimal - review overall performance")
            
            # Check for resource pressure
            high_usage_count = len([
                metric for metric in metrics.values()
                if metric.value > 80 and metric.threshold_max
            ])
            
            if high_usage_count > 0:
                recommendations.append(f"Monitor {high_usage_count} high-usage metrics closely")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate general recommendations: {e}")
            return []

    def calculate_overall_health_score(self, metrics: Dict[str, HealthMetric]) -> Dict[str, Any]:
        """Calculate overall system health score"""
        try:
            if not metrics:
                return {"score": 0.0, "level": "unknown", "details": "No metrics available"}
            
            total_score = 0.0
            total_metrics = len(metrics)
            
            # Score each metric based on health level
            level_scores = {
                HealthLevel.EXCELLENT: 100.0,
                HealthLevel.GOOD: 80.0,
                HealthLevel.WARNING: 60.0,
                HealthLevel.CRITICAL: 30.0,
                HealthLevel.EMERGENCY: 10.0
            }
            
            for metric in metrics.values():
                score = level_scores.get(metric.current_level, 50.0)
                total_score += score
            
            average_score = total_score / total_metrics
            
            # Determine overall health level
            if average_score >= 90:
                overall_level = "excellent"
            elif average_score >= 75:
                overall_level = "good"
            elif average_score >= 60:
                overall_level = "fair"
            elif average_score >= 40:
                overall_level = "poor"
            else:
                overall_level = "critical"
            
            return {
                "score": round(average_score, 2),
                "level": overall_level,
                "total_metrics": total_metrics,
                "details": {
                    "excellent_metrics": len([m for m in metrics.values() if m.current_level == HealthLevel.EXCELLENT]),
                    "good_metrics": len([m for m in metrics.values() if m.current_level == HealthLevel.GOOD]),
                    "warning_metrics": len([m for m in metrics.values() if m.current_level == HealthLevel.WARNING]),
                    "critical_metrics": len([m for m in metrics.values() if m.current_level == HealthLevel.CRITICAL]),
                    "emergency_metrics": len([m for m in metrics.values() if m.current_level == HealthLevel.EMERGENCY])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to calculate overall health score: {e}")
            return {"error": str(e)}

    def get_health_insights(self, metrics: Dict[str, HealthMetric], 
                           trends: Dict[str, HealthTrend]) -> Dict[str, Any]:
        """Get comprehensive health insights"""
        try:
            insights = {
                "timestamp": datetime.now().isoformat(),
                "overall_health": self.calculate_overall_health_score(metrics),
                "trends": {name: trend.to_dict() for name, trend in trends.items()},
                "predictions": self.predict_health_issues(metrics),
                "recommendations": self.generate_optimization_recommendations(metrics, trends),
                "critical_metrics": [
                    name for name, metric in metrics.items()
                    if metric.current_level in [HealthLevel.CRITICAL, HealthLevel.EMERGENCY]
                ],
                "improving_metrics": [
                    name for name, trend in trends.items()
                    if trend.trend_direction == "decreasing"
                ],
                "degrading_metrics": [
                    name for name, trend in trends.items()
                    if trend.trend_direction == "increasing"
                ]
            }
            
            self.logger.info("Health insights generated successfully")
            return insights
            
        except Exception as e:
            self.logger.error(f"Failed to get health insights: {e}")
            return {"error": str(e)}

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.logger.info("✅ Health Analysis Manager cleanup completed")
        except Exception as e:
            self.logger.error(f"Health Analysis Manager cleanup failed: {e}")


