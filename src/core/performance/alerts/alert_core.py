"""
Alert Core Module

Core alert data structures and functionality for the performance alert system.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass


class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertType(Enum):
    """Types of performance alerts"""
    PERFORMANCE_DEGRADATION = "performance_degradation"
    TARGET_MISSED = "target_missed"
    SYSTEM_OVERLOAD = "system_overload"
    RELIABILITY_ISSUE = "reliability_issue"
    SCALABILITY_LIMIT = "scalability_limit"
    THRESHOLD_BREACH = "threshold_breach"


@dataclass
class PerformanceAlert:
    """Performance alert data structure"""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    benchmark_id: str
    benchmark_type: str
    triggered_at: str
    resolved_at: Optional[str]
    is_resolved: bool
    metadata: Dict[str, Any]


class AlertFactory:
    """Factory for creating different types of performance alerts"""
    
    @staticmethod
    def create_performance_level_alert(benchmark, severity: AlertSeverity, 
                                     alert_type: AlertType = AlertType.PERFORMANCE_DEGRADATION) -> PerformanceAlert:
        """Create an alert for performance level issues"""
        alert_id = str(uuid.uuid4())
        
        title = f"Performance Level Alert: {benchmark.test_name}"
        message = (
            f"Benchmark '{benchmark.test_name}' achieved {benchmark.performance_level.value} "
            f"performance level, which is below acceptable standards."
        )
        
        return PerformanceAlert(
            alert_id=alert_id,
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            benchmark_id=benchmark.benchmark_id,
            benchmark_type=benchmark.benchmark_type,
            triggered_at=datetime.now().isoformat(),
            resolved_at=None,
            is_resolved=False,
            metadata={
                "performance_level": benchmark.performance_level.value,
                "duration": benchmark.duration,
                "recommendations": benchmark.optimization_recommendations,
            }
        )
    
    @staticmethod
    def create_threshold_alert(benchmark, severity: AlertSeverity, 
                             actual_value: float, threshold: float) -> PerformanceAlert:
        """Create a threshold breach alert"""
        alert_id = str(uuid.uuid4())
        
        title = f"Threshold Breach: {benchmark.test_name}"
        message = (
            f"Metric exceeded {severity.value} threshold: "
            f"actual={actual_value:.2f}, threshold={threshold:.2f}"
        )
        
        return PerformanceAlert(
            alert_id=alert_id,
            alert_type=AlertType.THRESHOLD_BREACH,
            severity=severity,
            title=title,
            message=message,
            benchmark_id=benchmark.benchmark_id,
            benchmark_type=benchmark.benchmark_type,
            triggered_at=datetime.now().isoformat(),
            resolved_at=None,
            is_resolved=False,
            metadata={
                "actual_value": actual_value,
                "threshold": threshold,
                "breach_percentage": ((actual_value - threshold) / threshold) * 100 if threshold > 0 else 0,
            }
        )
    
    @staticmethod
    def create_reliability_alert(benchmark, failed_ops: int, success_rate: float) -> PerformanceAlert:
        """Create a reliability issue alert"""
        alert_id = str(uuid.uuid4())
        severity = AlertSeverity.HIGH if success_rate < 99.0 else AlertSeverity.MEDIUM
        
        return PerformanceAlert(
            alert_id=alert_id,
            alert_type=AlertType.RELIABILITY_ISSUE,
            severity=severity,
            title=f"Reliability Issue: {benchmark.test_name}",
            message=f"Detected {failed_ops} failed operations with {success_rate:.1f}% success rate",
            benchmark_id=benchmark.benchmark_id,
            benchmark_type=benchmark.benchmark_type,
            triggered_at=datetime.now().isoformat(),
            resolved_at=None,
            is_resolved=False,
            metadata={
                "failed_operations": failed_ops,
                "success_rate": success_rate,
            }
        )
    
    @staticmethod
    def create_scalability_alert(benchmark, scalability_score: float) -> PerformanceAlert:
        """Create a scalability limit alert"""
        alert_id = str(uuid.uuid4())
        
        return PerformanceAlert(
            alert_id=alert_id,
            alert_type=AlertType.SCALABILITY_LIMIT,
            severity=AlertSeverity.HIGH,
            title=f"Scalability Limit: {benchmark.test_name}",
            message=f"Poor scalability score: {scalability_score:.1f}%",
            benchmark_id=benchmark.benchmark_id,
            benchmark_type=benchmark.benchmark_type,
            triggered_at=datetime.now().isoformat(),
            resolved_at=None,
            is_resolved=False,
            metadata={
                "scalability_score": scalability_score,
            }
        )
    
    @staticmethod
    def create_throughput_alert(benchmark, throughput: float) -> PerformanceAlert:
        """Create a system overload alert for low throughput"""
        alert_id = str(uuid.uuid4())
        
        return PerformanceAlert(
            alert_id=alert_id,
            alert_type=AlertType.SYSTEM_OVERLOAD,
            severity=AlertSeverity.CRITICAL,
            title=f"System Overload: {benchmark.test_name}",
            message=f"Extremely low throughput: {throughput:.1f} ops/sec",
            benchmark_id=benchmark.benchmark_id,
            benchmark_type=benchmark.benchmark_type,
            triggered_at=datetime.now().isoformat(),
            resolved_at=None,
            is_resolved=False,
            metadata={
                "throughput": throughput,
            }
        )

