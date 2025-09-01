#!/usr/bin/env python3
"""
Gaming Performance Models - Agent Cellphone V2
=============================================

Data models and enums for gaming performance integration system.
Extracted from gaming_performance_integration.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class PerformanceTestType(Enum):
    """Types of performance tests."""
    LOAD_TEST = "load_test"
    STRESS_TEST = "stress_test"
    ENDURANCE_TEST = "endurance_test"
    SPIKE_TEST = "spike_test"
    VOLUME_TEST = "volume_test"


@dataclass
class GamingComponentProfile:
    """Gaming component performance profile."""
    component_name: str
    component_type: str
    file_path: str
    performance_thresholds: Dict[str, float]
    baseline_metrics: Dict[str, float] = field(default_factory=dict)
    current_metrics: Dict[str, float] = field(default_factory=dict)
    performance_score: float = 0.0
    compliance_status: str = "pending"
    last_validated: Optional[datetime] = None


@dataclass
class PerformanceTestResult:
    """Performance test execution result."""
    test_type: PerformanceTestType
    component_name: str
    execution_time: float
    metrics: Dict[str, Any]
    threshold_compliance: Dict[str, bool]
    performance_score: float
    recommendations: List[str]
    timestamp: datetime


@dataclass
class PerformanceIntegrationConfig:
    """Performance integration configuration."""
    monitoring_interval: float = 1.0
    test_duration_multiplier: float = 1.0
    concurrent_operations_multiplier: float = 1.0
    operation_interval_multiplier: float = 1.0
    enable_real_time_monitoring: bool = True
    enable_statistical_analysis: bool = True
    enable_regression_detection: bool = True
    enable_automated_reporting: bool = True


@dataclass
class PerformanceThresholds:
    """Performance thresholds for gaming components."""
    response_time_ms: float
    throughput_ops_per_sec: float
    memory_usage_mb: float
    cpu_usage_percent: float
    error_rate_percent: float
    latency_ms: float
    io_operations_per_sec: float


@dataclass
class PerformanceMetrics:
    """Performance metrics collection."""
    response_time: float
    throughput: float
    memory_usage: float
    cpu_usage: float
    error_rate: float
    latency: float
    io_operations: float
    timestamp: datetime
    component_name: str
    test_type: PerformanceTestType


@dataclass
class PerformanceAnalysisResult:
    """Performance analysis result."""
    component_name: str
    analysis_type: str
    baseline_metrics: Dict[str, float]
    current_metrics: Dict[str, float]
    performance_delta: Dict[str, float]
    regression_detected: bool
    recommendations: List[str]
    analysis_timestamp: datetime
    confidence_score: float
