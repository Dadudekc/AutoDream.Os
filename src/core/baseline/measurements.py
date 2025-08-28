#!/usr/bin/env python3
"""
Refactoring Baseline Measurements System - Agent-5
=================================================

This module provides comprehensive baseline measurements for refactoring performance,
enabling comparison and tracking of improvements over time.

Features:
- Baseline establishment and management
- Performance comparison and analysis
- Trend tracking and forecasting
- Baseline validation and calibration
- Multi-dimensional baseline support
- Automated baseline updates

Author: Agent-5 (REFACTORING MANAGER)
Contract: REFACTOR-003
Status: In Progress
"""

import os
import sys
import json
import logging
import asyncio
import time
import statistics
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import traceback

sys.path.append(str(Path(__file__).parent.parent.parent))
from core.managers.base_manager import BaseManager
from core.refactoring.refactoring_performance_metrics import (
    RefactoringPerformanceMetrics, MetricType, MetricCategory
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaselineType(Enum):
    """Types of performance baselines"""
    PERFORMANCE = "performance"
    QUALITY = "quality"
    EFFICIENCY = "efficiency"
    COMPOSITE = "composite"
    CUSTOM = "custom"

class BaselineStatus(Enum):
    """Baseline status indicators"""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    CALIBRATING = "calibrating"
    VALIDATING = "validating"
    ERROR = "error"

@dataclass
class BaselineMetric:
    """Individual baseline metric definition"""
    name: str
    value: float
    unit: str
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    target_value: Optional[float] = None
    weight: float = 1.0
    description: str = ""

@dataclass
class PerformanceBaseline:
    """Comprehensive performance baseline definition"""
    baseline_id: str
    name: str
    description: str
    baseline_type: BaselineType
    status: BaselineStatus
    version: str
    created_at: datetime
    updated_at: datetime
    metrics: Dict[str, BaselineMetric]
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    confidence_score: float = 1.0
    sample_size: int = 0
    validity_period_days: int = 30

@dataclass
class BaselineComparison:
    """Result of comparing current metrics against a baseline"""
    baseline_id: str
    comparison_timestamp: datetime
    overall_score: float
    metric_comparisons: Dict[str, Dict[str, Any]]
    improvements: List[str]
    regressions: List[str]
    recommendations: List[str]
    confidence_level: str

@dataclass
class BaselineTrend:
    """Trend analysis for baseline metrics over time"""
    metric_name: str
    time_period: str
    trend_direction: str  # "improving", "declining", "stable"
    trend_strength: float  # 0.0 to 1.0
    data_points: List[Tuple[datetime, float]]
    forecast: Optional[float] = None

class RefactoringBaselineMeasurements(BaseManager):
    """
    Comprehensive system for establishing and managing performance baselines.
    
    This system provides:
    - Baseline establishment and management
    - Performance comparison and analysis
    - Trend tracking and forecasting
    - Baseline validation and calibration
    - Multi-dimensional baseline support
    - Automated baseline updates
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the baseline measurements system"""
        super().__init__(config or {})
        self.metrics_system = RefactoringPerformanceMetrics()
        self.baselines: List[PerformanceBaseline] = []
        self.baseline_config = self._initialize_baseline_config()
        self._initialize_default_baselines()
    
    def _initialize_baseline_config(self) -> Dict[str, Any]:
        """Initialize baseline configuration"""
        return {
            "auto_calibration_enabled": True,
            "calibration_threshold": 0.8,  # 80% confidence required
            "max_baselines_per_type": 5,
            "baseline_retention_days": 90,
            "trend_analysis_enabled": True,
            "forecast_horizon_days": 30,
            "validation_interval_hours": 24,
            "default_metrics": [
                "code_complexity",
                "maintainability_index",
                "duplication_percentage",
                "refactoring_duration",
                "performance_improvement",
                "memory_usage",
                "cpu_utilization",
                "lines_of_code",
                "test_coverage",
                "bug_density"
            ]
        }
    
    def _initialize_default_baselines(self):
        """Initialize default performance baselines"""
        # Performance baseline
        performance_metrics = {
            "refactoring_duration": BaselineMetric(
                name="refactoring_duration",
                value=60.0,
                unit="seconds",
                min_threshold=30.0,
                max_threshold=120.0,
                target_value=45.0,
                weight=1.0,
                description="Time taken to complete refactoring operations"
            ),
            "performance_improvement": BaselineMetric(
                name="performance_improvement",
                value=15.0,
                unit="percent",
                min_threshold=5.0,
                max_threshold=50.0,
                target_value=25.0,
                weight=1.2,
                description="Performance improvement achieved through refactoring"
            ),
            "memory_usage": BaselineMetric(
                name="memory_usage",
                value=100.0,
                unit="MB",
                min_threshold=50.0,
                max_threshold=200.0,
                target_value=80.0,
                weight=0.8,
                description="Memory usage during refactoring operations"
            )
        }
        
        performance_baseline = PerformanceBaseline(
            baseline_id="baseline_performance_v1",
            name="Performance Baseline v1.0",
            description="Baseline for refactoring performance metrics",
            baseline_type=BaselineType.PERFORMANCE,
            status=BaselineStatus.ACTIVE,
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metrics=performance_metrics,
            context={"category": "performance", "priority": "high"},
            tags=["performance", "refactoring", "v1.0"],
            confidence_score=0.9,
            sample_size=100,
            validity_period_days=30
        )
        
        # Quality baseline
        quality_metrics = {
            "code_complexity": BaselineMetric(
                name="code_complexity",
                value=5.0,
                unit="units",
                min_threshold=1.0,
                max_threshold=15.0,
                target_value=3.0,
                weight=1.0,
                description="Cyclomatic complexity of refactored code"
            ),
            "maintainability_index": BaselineMetric(
                name="maintainability_index",
                value=0.8,
                unit="score",
                min_threshold=0.6,
                max_threshold=1.0,
                target_value=0.9,
                weight=1.3,
                description="Maintainability index of refactored code"
            ),
            "duplication_percentage": BaselineMetric(
                name="duplication_percentage",
                value=0.05,
                unit="percent",
                min_threshold=0.0,
                max_threshold=0.2,
                target_value=0.02,
                weight=1.1,
                description="Code duplication percentage"
            )
        }
        
        quality_baseline = PerformanceBaseline(
            baseline_id="baseline_quality_v1",
            name="Quality Baseline v1.0",
            description="Baseline for code quality metrics",
            baseline_type=BaselineType.QUALITY,
            status=BaselineStatus.ACTIVE,
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metrics=quality_metrics,
            context={"category": "quality", "priority": "high"},
            tags=["quality", "refactoring", "v1.0"],
            confidence_score=0.85,
            sample_size=150,
            validity_period_days=30
        )
        
        # Composite baseline
        composite_metrics = {**performance_metrics, **quality_metrics}
        composite_baseline = PerformanceBaseline(
            baseline_id="baseline_composite_v1",
            name="Composite Baseline v1.0",
            description="Comprehensive baseline combining performance and quality metrics",
            baseline_type=BaselineType.COMPOSITE,
            status=BaselineStatus.ACTIVE,
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metrics=composite_metrics,
            context={"category": "composite", "priority": "critical"},
            tags=["composite", "refactoring", "v1.0"],
            confidence_score=0.95,
            sample_size=200,
            validity_period_days=30
        )
        
        self.baselines.extend([performance_baseline, quality_baseline, composite_baseline])
    
    def create_baseline(self, name: str, description: str, baseline_type: BaselineType,
                       metrics: Dict[str, BaselineMetric], version: str = "1.0.0",
                       context: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """Create a new performance baseline"""
        baseline_id = f"baseline_{baseline_type.value}_{int(time.time())}"
        
        baseline = PerformanceBaseline(
            baseline_id=baseline_id,
            name=name,
            description=description,
            baseline_type=baseline_type,
            status=BaselineStatus.ACTIVE,
            version=version,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metrics=metrics,
            context=context or {},
            tags=tags or [],
            confidence_score=1.0,
            sample_size=0,
            validity_period_days=self.baseline_config["baseline_retention_days"]
        )
        
        # Check if we need to deprecate old baselines
        self._manage_baseline_limits(baseline_type)
        
        self.baselines.append(baseline)
        logger.info(f"Created baseline: {name} ({baseline_id})")
        return baseline_id
    
    def _manage_baseline_limits(self, baseline_type: BaselineType):
        """Manage baseline limits per type"""
        type_baselines = [b for b in self.baselines if b.baseline_type == baseline_type]
        max_baselines = self.baseline_config["max_baselines_per_type"]
        
        if len(type_baselines) >= max_baselines:
            # Deprecate oldest baseline
            oldest_baseline = min(type_baselines, key=lambda x: x.created_at)
            oldest_baseline.status = BaselineStatus.DEPRECATED
            logger.info(f"Deprecated old baseline: {oldest_baseline.name}")
    
    def update_baseline(self, baseline_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing baseline"""
        baseline = next((b for b in self.baselines if b.baseline_id == baseline_id), None)
        if not baseline:
            logger.error(f"Baseline not found: {baseline_id}")
            return False
        
        try:
            # Update allowed fields
            if "name" in updates:
                baseline.name = updates["name"]
            if "description" in updates:
                baseline.description = updates["description"]
            if "metrics" in updates:
                baseline.metrics = updates["metrics"]
            if "context" in updates:
                baseline.context.update(updates["context"])
            if "tags" in updates:
                baseline.tags = updates["tags"]
            if "confidence_score" in updates:
                baseline.confidence_score = updates["confidence_score"]
            if "validity_period_days" in updates:
                baseline.validity_period_days = updates["validity_period_days"]
            
            baseline.updated_at = datetime.now()
            logger.info(f"Updated baseline: {baseline_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating baseline {baseline_id}: {e}")
            return False
    
    def deprecate_baseline(self, baseline_id: str) -> bool:
        """Deprecate a baseline"""
        baseline = next((b for b in self.baselines if b.baseline_id == baseline_id), None)
        if not baseline:
            return False
        
        baseline.status = BaselineStatus.DEPRECATED
        baseline.updated_at = datetime.now()
        logger.info(f"Deprecated baseline: {baseline_id}")
        return True
    
    def get_baseline(self, baseline_id: str) -> Optional[PerformanceBaseline]:
        """Get a specific baseline by ID"""
        return next((b for b in self.baselines if b.baseline_id == baseline_id), None)
    
    def get_baselines_by_type(self, baseline_type: BaselineType) -> List[PerformanceBaseline]:
        """Get all baselines of a specific type"""
        return [b for b in self.baselines if b.baseline_type == baseline_type and b.status == BaselineStatus.ACTIVE]
    
    def get_active_baselines(self) -> List[PerformanceBaseline]:
        """Get all active baselines"""
        return [b for b in self.baselines if b.status == BaselineStatus.ACTIVE]
    
    def compare_against_baseline(self, baseline_id: str, 
                               current_metrics: Dict[str, float]) -> Optional[BaselineComparison]:
        """Compare current metrics against a specific baseline"""
        baseline = self.get_baseline(baseline_id)
        if not baseline:
            logger.error(f"Baseline not found: {baseline_id}")
            return None
        
        try:
            metric_comparisons = {}
            improvements = []
            regressions = []
            total_score = 0.0
            total_weight = 0.0
            
            for metric_name, current_value in current_metrics.items():
                if metric_name in baseline.metrics:
                    baseline_metric = baseline.metrics[metric_name]
                    baseline_value = baseline_metric.value
                    
                    # Calculate comparison metrics
                    difference = current_value - baseline_value
                    percentage_change = (difference / baseline_value) * 100 if baseline_value != 0 else 0
                    
                    # Determine if it's an improvement or regression
                    is_improvement = False
                    if metric_name in ["complexity", "duplication_percentage", "refactoring_duration"]:
                        # Lower is better
                        is_improvement = difference < 0
                    else:
                        # Higher is better
                        is_improvement = difference > 0
                    
                    # Calculate score for this metric
                    if baseline_metric.min_threshold is not None and baseline_metric.max_threshold is not None:
                        if baseline_metric.min_threshold <= current_value <= baseline_metric.max_threshold:
                            metric_score = 1.0
                        else:
                            # Penalize out-of-range values
                            if current_value < baseline_metric.min_threshold:
                                distance = (baseline_metric.min_threshold - current_value) / baseline_metric.min_threshold
                            else:
                                distance = (current_value - baseline_metric.max_threshold) / baseline_metric.max_threshold
                            metric_score = max(0.0, 1.0 - distance)
                    else:
                        # No thresholds, use percentage change
                        if abs(percentage_change) <= 10:  # Within 10%
                            metric_score = 1.0
                        else:
                            metric_score = max(0.0, 1.0 - (abs(percentage_change) - 10) / 100)
                    
                    metric_comparisons[metric_name] = {
                        "baseline_value": baseline_value,
                        "current_value": current_value,
                        "difference": difference,
                        "percentage_change": percentage_change,
                        "is_improvement": is_improvement,
                        "score": metric_score,
                        "weight": baseline_metric.weight,
                        "unit": baseline_metric.unit,
                        "description": baseline_metric.description
                    }
                    
                    # Track improvements and regressions
                    if is_improvement:
                        improvements.append(f"{metric_name}: {abs(percentage_change):.1f}% improvement")
                    else:
                        regressions.append(f"{metric_name}: {abs(percentage_change):.1f}% regression")
                    
                    # Accumulate weighted score
                    total_score += metric_score * baseline_metric.weight
                    total_weight += baseline_metric.weight
            
            # Calculate overall score
            overall_score = total_score / total_weight if total_weight > 0 else 0.0
            
            # Generate recommendations
            recommendations = self._generate_baseline_recommendations(metric_comparisons, overall_score)
            
            # Determine confidence level
            confidence_level = self._determine_confidence_level(baseline.confidence_score, overall_score)
            
            comparison = BaselineComparison(
                baseline_id=baseline_id,
                comparison_timestamp=datetime.now(),
                overall_score=overall_score,
                metric_comparisons=metric_comparisons,
                improvements=improvements,
                regressions=regressions,
                recommendations=recommendations,
                confidence_level=confidence_level
            )
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing against baseline {baseline_id}: {e}")
            return None
    
    def _generate_baseline_recommendations(self, metric_comparisons: Dict[str, Dict[str, Any]], 
                                         overall_score: float) -> List[str]:
        """Generate recommendations based on baseline comparison"""
        recommendations = []
        
        if overall_score >= 0.9:
            recommendations.append("Excellent performance! Continue current practices")
        elif overall_score >= 0.7:
            recommendations.append("Good performance with room for improvement")
        elif overall_score >= 0.5:
            recommendations.append("Moderate performance - consider optimization strategies")
        else:
            recommendations.append("Performance below baseline - immediate attention required")
        
        # Specific recommendations based on metric performance
        for metric_name, comparison in metric_comparisons.items():
            if comparison["score"] < 0.6:
                if metric_name == "code_complexity":
                    recommendations.append("High code complexity detected - consider refactoring to reduce complexity")
                elif metric_name == "maintainability_index":
                    recommendations.append("Low maintainability - focus on code quality improvements")
                elif metric_name == "duplication_percentage":
                    recommendations.append("High code duplication - extract common functionality")
                elif metric_name == "refactoring_duration":
                    recommendations.append("Long refactoring duration - optimize workflow efficiency")
        
        return recommendations
    
    def _determine_confidence_level(self, baseline_confidence: float, 
                                   comparison_score: float) -> str:
        """Determine confidence level of comparison"""
        if baseline_confidence >= 0.9 and comparison_score >= 0.8:
            return "high"
        elif baseline_confidence >= 0.7 and comparison_score >= 0.6:
            return "medium"
        else:
            return "low"
    
    def analyze_baseline_trends(self, baseline_id: str, 
                               time_period: str = "30d") -> List[BaselineTrend]:
        """Analyze trends for baseline metrics over time"""
        baseline = self.get_baseline(baseline_id)
        if not baseline:
            return []
        
        try:
            # Calculate time range
            end_time = datetime.now()
            if time_period == "7d":
                start_time = end_time - timedelta(days=7)
            elif time_period == "30d":
                start_time = end_time - timedelta(days=30)
            elif time_period == "90d":
                start_time = end_time - timedelta(days=90)
            else:
                start_time = end_time - timedelta(days=30)
            
            # Get historical metrics
            report = self.metrics_system.generate_metrics_report(
                time_range=(start_time, end_time)
            )
            
            trends = []
            for metric_name in baseline.metrics.keys():
                metric_data = []
                
                # Collect metric values over time
                for snapshot in report.detailed_metrics:
                    for metric in snapshot.metrics:
                        if metric.name == metric_name and isinstance(metric.value, (int, float)):
                            metric_data.append((snapshot.timestamp, metric.value))
                
                if len(metric_data) >= 2:
                    # Sort by timestamp
                    metric_data.sort(key=lambda x: x[0])
                    
                    # Calculate trend direction and strength
                    trend_direction, trend_strength = self._calculate_trend_direction(
                        metric_data, metric_name
                    )
                    
                    # Generate forecast if enabled
                    forecast = None
                    if self.baseline_config["trend_analysis_enabled"]:
                        forecast = self._generate_forecast(metric_data, metric_name)
                    
                    trend = BaselineTrend(
                        metric_name=metric_name,
                        time_period=time_period,
                        trend_direction=trend_direction,
                        trend_strength=trend_strength,
                        data_points=metric_data,
                        forecast=forecast
                    )
                    
                    trends.append(trend)
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends for baseline {baseline_id}: {e}")
            return []
    
    def _calculate_trend_direction(self, metric_data: List[Tuple[datetime, float]], 
                                  metric_name: str) -> Tuple[str, float]:
        """Calculate trend direction and strength for a metric"""
        if len(metric_data) < 2:
            return "stable", 0.0
        
        # Extract values
        values = [point[1] for point in metric_data]
        
        # Calculate linear regression slope
        n = len(values)
        x_values = list(range(n))
        
        # Simple linear regression
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            return "stable", 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Determine direction
        if abs(slope) < 0.01:  # Very small slope
            direction = "stable"
        elif slope > 0:
            # Check if higher is better for this metric
            if metric_name in ["complexity", "duplication_percentage", "refactoring_duration"]:
                direction = "declining"  # Higher is worse
            else:
                direction = "improving"   # Higher is better
        else:
            if metric_name in ["complexity", "duplication_percentage", "refactoring_duration"]:
                direction = "improving"   # Lower is better
            else:
                direction = "declining"   # Lower is worse
        
        # Calculate trend strength (0.0 to 1.0)
        # Normalize slope relative to the range of values
        value_range = max(values) - min(values)
        if value_range == 0:
            strength = 0.0
        else:
            normalized_slope = abs(slope) / value_range
            strength = min(1.0, normalized_slope * 10)  # Scale factor
        
        return direction, strength
    
    def _generate_forecast(self, metric_data: List[Tuple[datetime, float]], 
                          metric_name: str) -> Optional[float]:
        """Generate forecast for a metric"""
        if len(metric_data) < 3:
            return None
        
        try:
            # Simple linear extrapolation
            values = [point[1] for point in metric_data]
            x_values = list(range(len(values)))
            
            # Linear regression
            n = len(values)
            sum_x = sum(x_values)
            sum_y = sum(values)
            sum_xy = sum(x * y for x, y in zip(x_values, values))
            sum_x2 = sum(x * x for x in x_values)
            
            if n * sum_x2 - sum_x * sum_x == 0:
                return None
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Forecast horizon
            forecast_horizon = self.baseline_config["forecast_horizon_days"]
            forecast_point = len(values) + forecast_horizon
            
            forecast_value = slope * forecast_point + intercept
            
            # Apply reasonable bounds
            if metric_name in ["maintainability_index", "test_coverage"]:
                forecast_value = max(0.0, min(1.0, forecast_value))
            elif metric_name in ["duplication_percentage"]:
                forecast_value = max(0.0, min(1.0, forecast_value))
            elif metric_name in ["refactoring_duration", "memory_usage"]:
                forecast_value = max(0.0, forecast_value)
            
            return forecast_value
            
        except Exception as e:
            logger.error(f"Error generating forecast for {metric_name}: {e}")
            return None
    
    def calibrate_baseline(self, baseline_id: str, 
                          calibration_data: List[Dict[str, float]]) -> bool:
        """Calibrate a baseline with new data"""
        baseline = self.get_baseline(baseline_id)
        if not baseline:
            return False
        
        try:
            baseline.status = BaselineStatus.CALIBRATING
            
            # Calculate new metric values from calibration data
            new_metrics = {}
            for metric_name in baseline.metrics.keys():
                values = []
                for data_point in calibration_data:
                    if metric_name in data_point:
                        values.append(data_point[metric_name])
                
                if values:
                    # Calculate new baseline value (median for robustness)
                    new_value = statistics.median(values)
                    
                    # Update baseline metric
                    baseline.metrics[metric_name].value = new_value
                    
                    # Adjust thresholds based on data spread
                    if len(values) > 1:
                        std_dev = statistics.stdev(values)
                        baseline.metrics[metric_name].min_threshold = new_value - 2 * std_dev
                        baseline.metrics[metric_name].max_threshold = new_value + 2 * std_dev
            
            # Update baseline metadata
            baseline.updated_at = datetime.now()
            baseline.sample_size += len(calibration_data)
            baseline.confidence_score = min(1.0, baseline.confidence_score + 0.1)
            baseline.status = BaselineStatus.ACTIVE
            
            logger.info(f"Calibrated baseline: {baseline_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error calibrating baseline {baseline_id}: {e}")
            baseline.status = BaselineStatus.ERROR
            return False
    
    def validate_baseline(self, baseline_id: str) -> Dict[str, Any]:
        """Validate a baseline's current accuracy"""
        baseline = self.get_baseline(baseline_id)
        if not baseline:
            return {"error": "Baseline not found"}
        
        try:
            # Get recent metrics for validation
            recent_report = self.metrics_system.generate_metrics_report(
                time_range=(datetime.now() - timedelta(days=7), datetime.now())
            )
            
            validation_results = {
                "baseline_id": baseline_id,
                "validation_timestamp": datetime.now().isoformat(),
                "overall_accuracy": 0.0,
                "metric_accuracy": {},
                "recommendations": []
            }
            
            total_accuracy = 0.0
            metric_count = 0
            
            for metric_name, baseline_metric in baseline.metrics.items():
                metric_values = []
                
                # Collect recent values for this metric
                for snapshot in recent_report.detailed_metrics:
                    for metric in snapshot.metrics:
                        if metric.name == metric_name and isinstance(metric.value, (int, float)):
                            metric_values.append(metric.value)
                
                if metric_values:
                    # Calculate accuracy for this metric
                    baseline_value = baseline_metric.value
                    avg_recent_value = statistics.mean(metric_values)
                    
                    # Calculate accuracy based on how close recent values are to baseline
                    if baseline_metric.min_threshold is not None and baseline_metric.max_threshold is not None:
                        # Use threshold-based accuracy
                        if baseline_metric.min_threshold <= avg_recent_value <= baseline_metric.max_threshold:
                            accuracy = 1.0
                        else:
                            # Penalize out-of-range values
                            if avg_recent_value < baseline_metric.min_threshold:
                                distance = (baseline_metric.min_threshold - avg_recent_value) / baseline_metric.min_threshold
                            else:
                                distance = (avg_recent_value - baseline_metric.max_threshold) / baseline_metric.max_threshold
                            accuracy = max(0.0, 1.0 - distance)
                    else:
                        # Use percentage-based accuracy
                        if baseline_value == 0:
                            accuracy = 1.0 if avg_recent_value == 0 else 0.0
                        else:
                            percentage_diff = abs(avg_recent_value - baseline_value) / baseline_value
                            accuracy = max(0.0, 1.0 - percentage_diff)
                    
                    validation_results["metric_accuracy"][metric_name] = {
                        "baseline_value": baseline_value,
                        "recent_average": avg_recent_value,
                        "accuracy": accuracy,
                        "sample_count": len(metric_values)
                    }
                    
                    total_accuracy += accuracy
                    metric_count += 1
            
            # Calculate overall accuracy
            if metric_count > 0:
                validation_results["overall_accuracy"] = total_accuracy / metric_count
            
            # Generate validation recommendations
            if validation_results["overall_accuracy"] < 0.7:
                validation_results["recommendations"].append("Baseline accuracy is low - consider recalibration")
            elif validation_results["overall_accuracy"] < 0.85:
                validation_results["recommendations"].append("Baseline accuracy is moderate - monitor for drift")
            else:
                validation_results["recommendations"].append("Baseline accuracy is good - continue monitoring")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating baseline {baseline_id}: {e}")
            return {"error": str(e)}
    
    def export_baseline_data(self, output_path: str, format: str = "json") -> bool:
        """Export baseline data to external format"""
        try:
            if format.lower() == "json":
                export_data = {
                    "export_timestamp": datetime.now().isoformat(),
                    "baseline_config": self.baseline_config,
                    "baselines": [
                        {
                            "baseline_id": b.baseline_id,
                            "name": b.name,
                            "description": b.description,
                            "baseline_type": b.baseline_type.value,
                            "status": b.status.value,
                            "version": b.version,
                            "created_at": b.created_at.isoformat(),
                            "updated_at": b.updated_at.isoformat(),
                            "metrics": {
                                name: {
                                    "value": metric.value,
                                    "unit": metric.unit,
                                    "min_threshold": metric.min_threshold,
                                    "max_threshold": metric.max_threshold,
                                    "target_value": metric.target_value,
                                    "weight": metric.weight,
                                    "description": metric.description
                                }
                                for name, metric in b.metrics.items()
                            },
                            "context": b.context,
                            "tags": b.tags,
                            "confidence_score": b.confidence_score,
                            "sample_size": b.sample_size,
                            "validity_period_days": b.validity_period_days
                        }
                        for b in self.baselines
                    ]
                }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, default=str)
                
                logger.info(f"Exported baseline data to {output_path}")
                return True
                
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
                
        except Exception as e:
            logger.error(f"Error exporting baseline data: {e}")
            return False
    
    def cleanup_expired_baselines(self):
        """Clean up expired baselines"""
        current_time = datetime.now()
        expired_baselines = []
        
        for baseline in self.baselines:
            if baseline.status == BaselineStatus.DEPRECATED:
                # Check if deprecation period has passed
                deprecation_date = baseline.updated_at + timedelta(days=baseline.validity_period_days)
                if current_time > deprecation_date:
                    expired_baselines.append(baseline.baseline_id)
        
        # Remove expired baselines
        for baseline_id in expired_baselines:
            self.baselines = [b for b in self.baselines if b.baseline_id != baseline_id]
        
        if expired_baselines:
            logger.info(f"Cleaned up {len(expired_baselines)} expired baselines")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "status": "active",
            "total_baselines": len(self.baselines),
            "active_baselines": len([b for b in self.baselines if b.status == BaselineStatus.ACTIVE]),
            "baseline_types": {
                baseline_type.value: len([b for b in self.baselines if b.baseline_type == baseline_type])
                for baseline_type in BaselineType
            },
            "average_confidence": statistics.mean([b.confidence_score for b in self.baselines]) if self.baselines else 0.0,
            "last_calibration": max([b.updated_at for b in self.baselines]).isoformat() if self.baselines else None,
            "auto_calibration_enabled": self.baseline_config["auto_calibration_enabled"],
            "trend_analysis_enabled": self.baseline_config["trend_analysis_enabled"]
        }

async def demo_baseline_measurements():
    """Demonstrate the baseline measurements system"""
    print("🚀 Refactoring Baseline Measurements System Demo")
    print("=" * 50)
    
    # Initialize the system
    baseline_system = RefactoringBaselineMeasurements()
    
    # Get system status
    status = baseline_system.get_system_status()
    print(f"System Status: {status}")
    
    # Get active baselines
    active_baselines = baseline_system.get_active_baselines()
    print(f"Active Baselines: {len(active_baselines)}")
    
    # Compare against a baseline
    if active_baselines:
        baseline = active_baselines[0]
        current_metrics = {
            "code_complexity": 6.5,
            "maintainability_index": 0.75,
            "duplication_percentage": 0.08,
            "refactoring_duration": 55.0
        }
        
        comparison = baseline_system.compare_against_baseline(
            baseline.baseline_id, current_metrics
        )
        
        if comparison:
            print(f"Baseline Comparison Score: {comparison.overall_score:.2f}")
            print(f"Improvements: {len(comparison.improvements)}")
            print(f"Regressions: {len(comparison.regressions)}")
    
    # Analyze trends
    if active_baselines:
        trends = baseline_system.analyze_baseline_trends(active_baselines[0].baseline_id)
        print(f"Trend Analysis: {len(trends)} metrics analyzed")
    
    # Validate baseline
    if active_baselines:
        validation = baseline_system.validate_baseline(active_baselines[0].baseline_id)
        print(f"Baseline Validation Accuracy: {validation.get('overall_accuracy', 0):.2f}")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo_baseline_measurements())
