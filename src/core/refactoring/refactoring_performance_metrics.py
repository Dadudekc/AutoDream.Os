#!/usr/bin/env python3
"""
Refactoring Performance Metrics System - Agent-5
================================================

This module provides comprehensive metrics for measuring refactoring performance,
including code quality improvements, performance gains, and efficiency metrics.

Features:
- Real-time metrics collection during refactoring operations
- Performance benchmarking and comparison
- Code quality metrics (complexity, maintainability, duplication)
- Efficiency metrics (time savings, resource utilization)
- Historical trend analysis and reporting
- Integration with existing refactoring tools

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of performance metrics"""
    CODE_QUALITY = "code_quality"
    PERFORMANCE = "performance"
    EFFICIENCY = "efficiency"
    COMPLEXITY = "complexity"
    MAINTAINABILITY = "maintainability"
    DUPLICATION = "duplication"
    TIME_SAVINGS = "time_savings"
    RESOURCE_UTILIZATION = "resource_utilization"

class MetricCategory(Enum):
    """Categories for organizing metrics"""
    REFACTORING_OPERATIONS = "refactoring_operations"
    CODE_ANALYSIS = "code_analysis"
    PERFORMANCE_IMPROVEMENTS = "performance_improvements"
    QUALITY_IMPROVEMENTS = "quality_improvements"
    EFFICIENCY_GAINS = "efficiency_gains"

@dataclass
class MetricValue:
    """Individual metric measurement"""
    name: str
    value: Union[float, int, str]
    unit: str
    timestamp: datetime
    category: MetricCategory
    metric_type: MetricType
    context: Optional[Dict[str, Any]] = None

@dataclass
class MetricSnapshot:
    """Snapshot of metrics at a specific point in time"""
    timestamp: datetime
    metrics: List[MetricValue]
    refactoring_operation: Optional[str] = None
    target_files: Optional[List[str]] = None
    duration: Optional[float] = None

@dataclass
class PerformanceBaseline:
    """Baseline measurements for comparison"""
    name: str
    timestamp: datetime
    metrics: Dict[str, float]
    description: str
    version: str
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MetricsReport:
    """Comprehensive metrics report"""
    report_id: str
    timestamp: datetime
    time_range: Tuple[datetime, datetime]
    summary: Dict[str, Any]
    detailed_metrics: List[MetricSnapshot]
    baselines: List[PerformanceBaseline]
    trends: Dict[str, List[float]]
    recommendations: List[str]

class RefactoringPerformanceMetrics(BaseManager):
    """
    Comprehensive system for measuring and analyzing refactoring performance metrics.
    
    This system provides:
    - Real-time metrics collection during refactoring operations
    - Performance benchmarking and comparison against baselines
    - Code quality metrics analysis
    - Efficiency metrics calculation
    - Historical trend analysis and reporting
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the refactoring performance metrics system"""
        super().__init__(config or {})
        self.metrics_history: List[MetricSnapshot] = []
        self.baselines: List[PerformanceBaseline] = []
        self.current_session: Optional[Dict[str, Any]] = None
        self.metrics_config = self._initialize_metrics_config()
        self._initialize_baselines()
        
    def _initialize_metrics_config(self) -> Dict[str, Any]:
        """Initialize metrics configuration"""
        return {
            "collection_enabled": True,
            "auto_save_interval": 300,  # 5 minutes
            "max_history_size": 1000,
            "metrics_to_track": [
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
            ],
            "thresholds": {
                "complexity_warning": 10,
                "complexity_critical": 20,
                "maintainability_warning": 0.6,
                "maintainability_critical": 0.4,
                "duplication_warning": 0.15,
                "duplication_critical": 0.25
            }
        }
    
    def _initialize_baselines(self):
        """Initialize default performance baselines"""
        default_baseline = PerformanceBaseline(
            name="Default Baseline",
            timestamp=datetime.now(),
            metrics={
                "code_complexity": 5.0,
                "maintainability_index": 0.8,
                "duplication_percentage": 0.05,
                "refactoring_duration": 60.0,
                "performance_improvement": 0.0,
                "memory_usage": 100.0,
                "cpu_utilization": 0.3,
                "lines_of_code": 1000,
                "test_coverage": 0.8,
                "bug_density": 0.01
            },
            description="Default baseline for refactoring performance metrics",
            version="1.0.0"
        )
        self.baselines.append(default_baseline)
    
    def start_metrics_session(self, operation_name: str, target_files: List[str]) -> str:
        """Start a new metrics collection session for a refactoring operation"""
        session_id = f"session_{int(time.time())}_{operation_name}"
        self.current_session = {
            "session_id": session_id,
            "operation_name": operation_name,
            "target_files": target_files,
            "start_time": datetime.now(),
            "metrics": [],
            "status": "active"
        }
        logger.info(f"Started metrics session: {session_id} for operation: {operation_name}")
        return session_id
    
    def end_metrics_session(self, session_id: str) -> Dict[str, Any]:
        """End a metrics collection session and return summary"""
        if not self.current_session or self.current_session["session_id"] != session_id:
            raise ValueError(f"Invalid session ID: {session_id}")
        
        end_time = datetime.now()
        duration = (end_time - self.current_session["start_time"]).total_seconds()
        
        # Create final snapshot
        final_snapshot = MetricSnapshot(
            timestamp=end_time,
            metrics=self.current_session["metrics"],
            refactoring_operation=self.current_session["operation_name"],
            target_files=self.current_session["target_files"],
            duration=duration
        )
        
        # Add to history
        self.metrics_history.append(final_snapshot)
        
        # Generate summary
        summary = self._generate_session_summary(final_snapshot)
        
        # Clear current session
        self.current_session = None
        
        logger.info(f"Ended metrics session: {session_id}, duration: {duration:.2f}s")
        return summary
    
    def record_metric(self, name: str, value: Union[float, int, str], 
                     unit: str, category: MetricCategory, 
                     metric_type: MetricType, context: Optional[Dict[str, Any]] = None):
        """Record a single metric during a refactoring operation"""
        if not self.current_session:
            logger.warning("No active metrics session. Call start_metrics_session first.")
            return
        
        metric = MetricValue(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            category=category,
            metric_type=metric_type,
            context=context
        )
        
        self.current_session["metrics"].append(metric)
        logger.debug(f"Recorded metric: {name} = {value} {unit}")
    
    def measure_code_quality(self, file_path: str) -> Dict[str, Any]:
        """Measure code quality metrics for a specific file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            total_lines = len(lines)
            code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
            comment_lines = [line for line in lines if line.strip().startswith('#')]
            
            # Calculate complexity (simplified cyclomatic complexity)
            complexity = self._calculate_complexity(content)
            
            # Calculate maintainability index
            maintainability = self._calculate_maintainability(content, total_lines, len(code_lines))
            
            # Calculate duplication percentage
            duplication = self._calculate_duplication(content)
            
            metrics = {
                "total_lines": total_lines,
                "code_lines": len(code_lines),
                "comment_lines": len(comment_lines),
                "comment_ratio": len(comment_lines) / total_lines if total_lines > 0 else 0,
                "complexity": complexity,
                "maintainability_index": maintainability,
                "duplication_percentage": duplication,
                "file_size_kb": len(content.encode('utf-8')) / 1024
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error measuring code quality for {file_path}: {e}")
            return {}
    
    def _calculate_complexity(self, content: str) -> float:
        """Calculate simplified cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        # Count control flow statements
        complexity += content.count('if ')
        complexity += content.count('elif ')
        complexity += content.count('for ')
        complexity += content.count('while ')
        complexity += content.count('except ')
        complexity += content.count('and ')
        complexity += content.count('or ')
        
        return complexity
    
    def _calculate_maintainability(self, content: str, total_lines: int, code_lines: int) -> float:
        """Calculate maintainability index (0-1, higher is better)"""
        if total_lines == 0:
            return 0.0
        
        # Factors affecting maintainability
        comment_ratio = content.count('#') / total_lines
        function_density = content.count('def ') / total_lines
        class_density = content.count('class ') / total_lines
        
        # Calculate maintainability score
        maintainability = 1.0
        
        # Penalize very long files
        if total_lines > 500:
            maintainability *= 0.8
        elif total_lines > 1000:
            maintainability *= 0.6
        
        # Reward good comment ratio
        if 0.1 <= comment_ratio <= 0.3:
            maintainability *= 1.1
        
        # Reward reasonable function density
        if 0.05 <= function_density <= 0.15:
            maintainability *= 1.1
        
        return max(0.0, min(1.0, maintainability))
    
    def _calculate_duplication(self, content: str) -> float:
        """Calculate code duplication percentage"""
        lines = content.split('\n')
        unique_lines = set()
        total_lines = len(lines)
        
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                unique_lines.add(stripped)
        
        if total_lines == 0:
            return 0.0
        
        duplication = (total_lines - len(unique_lines)) / total_lines
        return duplication
    
    def measure_performance_improvement(self, before_metrics: Dict[str, Any], 
                                     after_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Measure performance improvement between before and after metrics"""
        improvements = {}
        
        for metric in ['complexity', 'maintainability_index', 'duplication_percentage']:
            if metric in before_metrics and metric in after_metrics:
                before_val = before_metrics[metric]
                after_val = after_metrics[metric]
                
                if isinstance(before_val, (int, float)) and isinstance(after_val, (int, float)):
                    if metric in ['complexity', 'duplication_percentage']:
                        # Lower is better
                        improvement = ((before_val - after_val) / before_val) * 100
                    else:
                        # Higher is better
                        improvement = ((after_val - before_val) / before_val) * 100
                    
                    improvements[f"{metric}_improvement"] = improvement
                    improvements[f"{metric}_before"] = before_val
                    improvements[f"{metric}_after"] = after_val
        
        return improvements
    
    def create_performance_baseline(self, name: str, description: str, 
                                  version: str, context: Dict[str, Any] = None) -> str:
        """Create a new performance baseline from current metrics"""
        if not self.metrics_history:
            raise ValueError("No metrics history available to create baseline")
        
        # Use the most recent metrics
        latest_snapshot = self.metrics_history[-1]
        
        baseline_metrics = {}
        for metric in latest_snapshot.metrics:
            if isinstance(metric.value, (int, float)):
                baseline_metrics[metric.name] = metric.value
        
        baseline = PerformanceBaseline(
            name=name,
            timestamp=datetime.now(),
            metrics=baseline_metrics,
            description=description,
            version=version,
            context=context or {}
        )
        
        self.baselines.append(baseline)
        logger.info(f"Created performance baseline: {name}")
        return baseline.name
    
    def compare_against_baseline(self, baseline_name: str, 
                               current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Compare current metrics against a specific baseline"""
        baseline = next((b for b in self.baselines if b.name == baseline_name), None)
        if not baseline:
            raise ValueError(f"Baseline not found: {baseline_name}")
        
        comparison = {
            "baseline_name": baseline_name,
            "baseline_timestamp": baseline.timestamp,
            "comparison_timestamp": datetime.now(),
            "differences": {},
            "improvements": {},
            "regressions": {}
        }
        
        for metric_name, current_value in current_metrics.items():
            if metric_name in baseline.metrics:
                baseline_value = baseline.metrics[metric_name]
                if isinstance(current_value, (int, float)) and isinstance(baseline_value, (int, float)):
                    difference = current_value - baseline_value
                    percentage_change = (difference / baseline_value) * 100
                    
                    comparison["differences"][metric_name] = {
                        "baseline": baseline_value,
                        "current": current_value,
                        "difference": difference,
                        "percentage_change": percentage_change
                    }
                    
                    if metric_name in ['complexity', 'duplication_percentage']:
                        # Lower is better
                        if difference < 0:
                            comparison["improvements"][metric_name] = abs(percentage_change)
                        else:
                            comparison["regressions"][metric_name] = percentage_change
                    else:
                        # Higher is better
                        if difference > 0:
                            comparison["improvements"][metric_name] = percentage_change
                        else:
                            comparison["regressions"][metric_name] = abs(percentage_change)
        
        return comparison
    
    def generate_metrics_report(self, time_range: Optional[Tuple[datetime, datetime]] = None,
                              include_trends: bool = True) -> MetricsReport:
        """Generate a comprehensive metrics report"""
        if not time_range:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=7)  # Default to last 7 days
            time_range = (start_time, end_time)
        
        start_time, end_time = time_range
        
        # Filter metrics within time range
        filtered_snapshots = [
            snapshot for snapshot in self.metrics_history
            if start_time <= snapshot.timestamp <= end_time
        ]
        
        # Generate summary statistics
        summary = self._generate_summary_statistics(filtered_snapshots)
        
        # Calculate trends if requested
        trends = {}
        if include_trends:
            trends = self._calculate_trends(filtered_snapshots)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(summary, trends)
        
        report = MetricsReport(
            report_id=f"report_{int(time.time())}",
            timestamp=datetime.now(),
            time_range=time_range,
            summary=summary,
            detailed_metrics=filtered_snapshots,
            baselines=self.baselines,
            trends=trends,
            recommendations=recommendations
        )
        
        return report
    
    def _generate_summary_statistics(self, snapshots: List[MetricSnapshot]) -> Dict[str, Any]:
        """Generate summary statistics from metrics snapshots"""
        if not snapshots:
            return {}
        
        summary = {
            "total_operations": len(snapshots),
            "total_duration": sum(s.duration or 0 for s in snapshots),
            "average_duration": statistics.mean(s.duration or 0 for s in snapshots if s.duration),
            "metrics_count": sum(len(s.metrics) for s in snapshots),
            "unique_operations": list(set(s.refactoring_operation for s in snapshots if s.refactoring_operation))
        }
        
        # Aggregate metric values
        metric_aggregates = {}
        for snapshot in snapshots:
            for metric in snapshot.metrics:
                if isinstance(metric.value, (int, float)):
                    if metric.name not in metric_aggregates:
                        metric_aggregates[metric.name] = []
                    metric_aggregates[metric.name].append(metric.value)
        
        # Calculate statistics for each metric
        for metric_name, values in metric_aggregates.items():
            if values:
                summary[f"{metric_name}_stats"] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "mean": statistics.mean(values),
                    "median": statistics.median(values)
                }
        
        return summary
    
    def _calculate_trends(self, snapshots: List[MetricSnapshot]) -> Dict[str, List[float]]:
        """Calculate trends for metrics over time"""
        if len(snapshots) < 2:
            return {}
        
        # Sort snapshots by timestamp
        sorted_snapshots = sorted(snapshots, key=lambda x: x.timestamp)
        
        trends = {}
        for snapshot in sorted_snapshots:
            for metric in snapshot.metrics:
                if isinstance(metric.value, (int, float)):
                    if metric.name not in trends:
                        trends[metric.name] = []
                    trends[metric.name].append(metric.value)
        
        return trends
    
    def _generate_recommendations(self, summary: Dict[str, Any], 
                                trends: Dict[str, List[float]]) -> List[str]:
        """Generate recommendations based on metrics analysis"""
        recommendations = []
        
        # Check for performance issues
        if "average_duration" in summary and summary["average_duration"] > 300:  # 5 minutes
            recommendations.append("Consider optimizing refactoring operations to reduce average duration")
        
        # Check for complexity trends
        if "complexity" in trends and len(trends["complexity"]) > 1:
            if trends["complexity"][-1] > trends["complexity"][0]:
                recommendations.append("Code complexity is increasing - consider refactoring to reduce complexity")
        
        # Check for maintainability trends
        if "maintainability_index" in trends and len(trends["maintainability_index"]) > 1:
            if trends["maintainability_index"][-1] < trends["maintainability_index"][0]:
                recommendations.append("Maintainability is decreasing - focus on code quality improvements")
        
        # Check for duplication trends
        if "duplication_percentage" in trends and len(trends["duplication_percentage"]) > 1:
            if trends["duplication_percentage"][-1] > 0.2:  # 20%
                recommendations.append("High code duplication detected - consider extracting common functionality")
        
        if not recommendations:
            recommendations.append("Metrics indicate good refactoring performance - continue current practices")
        
        return recommendations
    
    def export_metrics_data(self, output_path: str, format: str = "json") -> bool:
        """Export metrics data to external format"""
        try:
            if format.lower() == "json":
                export_data = {
                    "export_timestamp": datetime.now().isoformat(),
                    "metrics_history": [
                        {
                            "timestamp": s.timestamp.isoformat(),
                            "refactoring_operation": s.refactoring_operation,
                            "target_files": s.target_files,
                            "duration": s.duration,
                            "metrics": [
                                {
                                    "name": m.name,
                                    "value": m.value,
                                    "unit": m.unit,
                                    "timestamp": m.timestamp.isoformat(),
                                    "category": m.category.value,
                                    "metric_type": m.metric_type.value,
                                    "context": m.context
                                }
                                for m in s.metrics
                            ]
                        }
                        for s in self.metrics_history
                    ],
                    "baselines": [
                        {
                            "name": b.name,
                            "timestamp": b.timestamp.isoformat(),
                            "metrics": b.metrics,
                            "description": b.description,
                            "version": b.version,
                            "context": b.context
                        }
                        for b in self.baselines
                    ]
                }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, default=str)
                
                logger.info(f"Exported metrics data to {output_path}")
                return True
                
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
                
        except Exception as e:
            logger.error(f"Error exporting metrics data: {e}")
            return False
    
    def cleanup_old_metrics(self, max_age_days: int = 30):
        """Clean up old metrics data to prevent memory bloat"""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        # Remove old snapshots
        original_count = len(self.metrics_history)
        self.metrics_history = [
            snapshot for snapshot in self.metrics_history
            if snapshot.timestamp > cutoff_date
        ]
        removed_count = original_count - len(self.metrics_history)
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old metrics snapshots")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        return {
            "status": "healthy" if self.metrics_config["collection_enabled"] else "disabled",
            "metrics_history_size": len(self.metrics_history),
            "baselines_count": len(self.baselines),
            "active_session": bool(self.current_session),
            "collection_enabled": self.metrics_config["collection_enabled"],
            "last_activity": max([s.timestamp for s in self.metrics_history]) if self.metrics_history else None
        }

async def demo_refactoring_metrics():
    """Demonstrate the refactoring performance metrics system"""
    print("🚀 Refactoring Performance Metrics System Demo")
    print("=" * 50)
    
    # Initialize the system
    metrics_system = RefactoringPerformanceMetrics()
    
    # Start a metrics session
    session_id = metrics_system.start_metrics_session(
        "code_quality_improvement",
        ["src/core/refactoring/automated_refactoring_workflows.py"]
    )
    
    # Record some metrics
    metrics_system.record_metric(
        "code_complexity", 8.5, "units", 
        MetricCategory.CODE_ANALYSIS, MetricType.COMPLEXITY
    )
    
    metrics_system.record_metric(
        "maintainability_index", 0.75, "score", 
        MetricCategory.CODE_ANALYSIS, MetricType.MAINTAINABILITY
    )
    
    metrics_system.record_metric(
        "refactoring_duration", 45.2, "seconds", 
        MetricCategory.REFACTORING_OPERATIONS, MetricType.TIME_SAVINGS
    )
    
    # End the session
    summary = metrics_system.end_metrics_session(session_id)
    print(f"Session summary: {summary}")
    
    # Generate a report
    report = metrics_system.generate_metrics_report()
    print(f"Generated report with {len(report.detailed_metrics)} snapshots")
    
    # Get system health
    health = metrics_system.get_system_health()
    print(f"System health: {health}")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo_refactoring_metrics())
