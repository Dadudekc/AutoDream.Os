#!/usr/bin/env python3
"""
Quality Assurance Engine
========================

Core quality assurance engine for V2 system with testing, validation,
monitoring, and quality metrics collection.
Follows V2 coding standards: ≤300 lines per module.
"""

import json
import time
import logging
import threading
from typing import Dict, List, Any, Optional, Callable, Union
from pathlib import Path
import statistics
import hashlib

from .core_framework import (
    QualityLevel, TestType, QualityMetric, TestResult, 
    QualityReport, QualityConfig
)

logger = logging.getLogger(__name__)


class QualityMetricsCollector:
    """Collects and manages quality metrics"""
    
    def __init__(self):
        self._metrics: Dict[str, List[QualityMetric]] = {}
        self._lock = threading.Lock()
        
    def add_metric(self, metric: QualityMetric) -> None:
        """Add a quality metric"""
        with self._lock:
            if metric.service_id not in self._metrics:
                self._metrics[metric.service_id] = []
            self._metrics[metric.service_id].append(metric)
            
    def get_metrics(self, service_id: str) -> List[QualityMetric]:
        """Get metrics for a specific service"""
        with self._lock:
            return self._metrics.get(service_id, [])
            
    def get_all_metrics(self) -> Dict[str, List[QualityMetric]]:
        """Get all metrics"""
        with self._lock:
            return self._metrics.copy()
            
    def clear_metrics(self, service_id: str = None) -> None:
        """Clear metrics for a service or all services"""
        with self._lock:
            if service_id:
                self._metrics.pop(service_id, None)
            else:
                self._metrics.clear()


class TestResultManager:
    """Manages test results and execution history"""
    
    def __init__(self):
        self._results: Dict[str, List[TestResult]] = {}
        self._lock = threading.Lock()
        
    def add_result(self, result: TestResult) -> None:
        """Add a test result"""
        with self._lock:
            if result.service_id not in self._results:
                self._results[result.service_id] = []
            self._results[result.service_id].append(result)
            
    def get_results(self, service_id: str) -> List[TestResult]:
        """Get test results for a specific service"""
        with self._lock:
            return self._results.get(service_id, [])
            
    def get_all_results(self) -> Dict[str, List[TestResult]]:
        """Get all test results"""
        with self._lock:
            return self._results.copy()
            
    def get_pass_rate(self, service_id: str = None) -> float:
        """Calculate pass rate for a service or overall"""
        with self._lock:
            if service_id:
                results = self._results.get(service_id, [])
            else:
                results = [r for service_results in self._results.values() for r in service_results]
                
            if not results:
                return 0.0
                
            passed = sum(1 for r in results if r.status == "passed")
            return (passed / len(results)) * 100


class V2QualityAssuranceFramework:
    """Comprehensive quality assurance framework for V2 system"""

    def __init__(self, config_path: str = "qa_config"):
        self.logger = logging.getLogger(f"{__name__}.V2QualityAssuranceFramework")
        self.config = QualityConfig(config_path)
        self.config.load_config()
        
        # Core components
        self.metrics_collector = QualityMetricsCollector()
        self.result_manager = TestResultManager()
        
        # Quality tracking
        self._quality_scores: Dict[str, float] = {}
        self._service_status: Dict[str, str] = {}
        
        # Performance tracking
        self._execution_times: Dict[str, List[float]] = {}
        self._error_counts: Dict[str, int] = {}
        
        self.logger.info("V2 Quality Assurance Framework initialized")

    def register_service(self, service_id: str, initial_score: float = 0.0) -> bool:
        """Register a new service for quality monitoring"""
        try:
            self._quality_scores[service_id] = initial_score
            self._service_status[service_id] = "active"
            self._execution_times[service_id] = []
            self._error_counts[service_id] = 0
            
            self.logger.info(f"Service {service_id} registered for quality monitoring")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register service {service_id}: {e}")
            return False

    def update_quality_metric(self, service_id: str, metric_name: str, 
                            value: Union[float, int, str, bool], 
                            description: str = "") -> bool:
        """Update quality metric for a service"""
        try:
            threshold = self.config.get_threshold(metric_name)
            quality_level = self.config.get_quality_level(float(value) if isinstance(value, (int, float)) else 0.0)
            
            metric = QualityMetric(
                metric_name=metric_name,
                value=value,
                threshold=threshold,
                quality_level=quality_level,
                timestamp=time.time(),
                service_id=service_id,
                description=description
            )
            
            self.metrics_collector.add_metric(metric)
            
            # Update quality score
            if isinstance(value, (int, float)):
                self._update_service_score(service_id, float(value))
            
            self.logger.debug(f"Quality metric updated for {service_id}: {metric_name} = {value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update quality metric for {service_id}: {e}")
            return False

    def record_test_result(self, service_id: str, test_name: str, test_type: TestType,
                          status: str, execution_time: float, details: Dict[str, Any] = None) -> bool:
        """Record a test result"""
        try:
            # Calculate quality score based on test result
            quality_score = self._calculate_test_quality_score(status, execution_time)
            
            result = TestResult(
                test_id=f"{service_id}_{test_name}_{int(time.time())}",
                test_name=test_name,
                test_type=test_type,
                service_id=service_id,
                status=status,
                execution_time=execution_time,
                timestamp=time.time(),
                details=details or {},
                quality_score=quality_score
            )
            
            self.result_manager.add_result(result)
            
            # Track execution time
            if service_id not in self._execution_times:
                self._execution_times[service_id] = []
            self._execution_times[service_id].append(execution_time)
            
            # Track errors
            if status == "failed" or status == "error":
                self._error_counts[service_id] = self._error_counts.get(service_id, 0) + 1
            
            self.logger.debug(f"Test result recorded for {service_id}: {test_name} - {status}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to record test result for {service_id}: {e}")
            return False

    def generate_quality_report(self, service_id: str = None) -> QualityReport:
        """Generate comprehensive quality report"""
        try:
            timestamp = time.time()
            report_id = f"qa_report_{int(timestamp)}"
            
            if service_id:
                metrics = self.metrics_collector.get_metrics(service_id)
                results = self.result_manager.get_results(service_id)
                service_count = 1
            else:
                metrics = [m for service_metrics in self.metrics_collector.get_all_metrics().values() for m in service_metrics]
                results = [r for service_results in self.result_manager.get_all_results().values() for r in service_results]
                service_count = len(self._quality_scores)
            
            # Calculate overall quality score
            overall_score = self._calculate_overall_quality_score(metrics, results)
            
            # Count test results
            tests_executed = len(results)
            tests_passed = sum(1 for r in results if r.status == "passed")
            tests_failed = tests_executed - tests_passed
            
            # Generate recommendations
            recommendations = self._generate_recommendations(metrics, results, overall_score)
            
            report = QualityReport(
                report_id=report_id,
                timestamp=timestamp,
                overall_quality_score=overall_score,
                service_count=service_count,
                tests_executed=tests_executed,
                tests_passed=tests_passed,
                tests_failed=tests_failed,
                quality_metrics=metrics,
                test_results=results,
                recommendations=recommendations
            )
            
            self.logger.info(f"Quality report generated: {report_id}")
            return report
        except Exception as e:
            self.logger.error(f"Failed to generate quality report: {e}")
            return None

    def _update_service_score(self, service_id: str, new_score: float) -> None:
        """Update quality score for a service"""
        if service_id in self._quality_scores:
            # Weighted average with existing score
            current_score = self._quality_scores[service_id]
            self._quality_scores[service_id] = (current_score * 0.7) + (new_score * 0.3)

    def _calculate_test_quality_score(self, status: str, execution_time: float) -> float:
        """Calculate quality score for a test result"""
        base_score = 10.0 if status == "passed" else 0.0
        
        # Bonus for fast execution (under 1 second)
        if execution_time < 1.0:
            base_score += 2.0
        elif execution_time < 5.0:
            base_score += 1.0
            
        return min(base_score, 10.0)

    def _calculate_overall_quality_score(self, metrics: List[QualityMetric], 
                                       results: List[TestResult]) -> float:
        """Calculate overall quality score"""
        if not metrics and not results:
            return 0.0
            
        scores = []
        
        # Add metric-based scores
        for metric in metrics:
            if isinstance(metric.value, (int, float)):
                scores.append(float(metric.value))
                
        # Add test result scores
        for result in results:
            scores.append(result.quality_score)
            
        if not scores:
            return 0.0
            
        return statistics.mean(scores)

    def _generate_recommendations(self, metrics: List[QualityMetric], 
                                 results: List[TestResult], overall_score: float) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        if overall_score < 5.0:
            recommendations.append("Overall quality score is low. Review and improve test coverage and code quality.")
            
        # Check for failing tests
        failed_tests = [r for r in results if r.status in ["failed", "error"]]
        if failed_tests:
            recommendations.append(f"Address {len(failed_tests)} failing tests to improve quality.")
            
        # Check for performance issues
        slow_tests = [r for r in results if r.execution_time > 10.0]
        if slow_tests:
            recommendations.append(f"Optimize {len(slow_tests)} slow tests to improve performance.")
            
        # Check for low coverage
        coverage_metrics = [m for m in metrics if "coverage" in m.metric_name.lower()]
        for metric in coverage_metrics:
            if isinstance(metric.value, (int, float)) and metric.value < 80.0:
                recommendations.append(f"Increase {metric.metric_name} to meet 80% threshold.")
                
        return recommendations

    def get_service_quality_summary(self, service_id: str) -> Dict[str, Any]:
        """Get quality summary for a specific service"""
        try:
            metrics = self.metrics_collector.get_metrics(service_id)
            results = self.result_manager.get_results(service_id)
            
            summary = {
                "service_id": service_id,
                "quality_score": self._quality_scores.get(service_id, 0.0),
                "status": self._service_status.get(service_id, "unknown"),
                "metrics_count": len(metrics),
                "tests_count": len(results),
                "pass_rate": self.result_manager.get_pass_rate(service_id),
                "avg_execution_time": statistics.mean(self._execution_times.get(service_id, [0.0])),
                "error_count": self._error_counts.get(service_id, 0)
            }
            
            return summary
        except Exception as e:
            self.logger.error(f"Failed to get quality summary for {service_id}: {e}")
            return {}

    def export_quality_data(self, export_path: str) -> bool:
        """Export all quality data to JSON file"""
        try:
            export_data = {
                "quality_scores": self._quality_scores,
                "service_status": self._service_status,
                "execution_times": self._execution_times,
                "error_counts": self._error_counts,
                "metrics": self.metrics_collector.get_all_metrics(),
                "test_results": self.result_manager.get_all_results()
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
                
            self.logger.info(f"Quality data exported to {export_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export quality data: {e}")
            return False
