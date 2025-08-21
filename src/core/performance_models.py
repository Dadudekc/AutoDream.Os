#!/usr/bin/env python3
"""
Unified Performance Models - Consolidated Performance Data Structures

This module provides unified performance models to eliminate duplication.
Follows Single Responsibility Principle - only performance data structures.
Architecture: Single Responsibility Principle - performance models only
LOC: Target 200 lines (under 300 limit)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum


class PerformanceLevel(Enum):
    """Performance level definitions"""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    BELOW_AVERAGE = "below_average"
    POOR = "poor"


class PerformanceMetricType(Enum):
    """Performance metric types"""
    MEMORY = "memory"
    CPU = "cpu"
    DISK = "disk"
    NETWORK = "network"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    AVAILABILITY = "availability"


class OptimizationType(Enum):
    """Performance optimization types"""
    MEMORY_OPTIMIZATION = "memory_optimization"
    CPU_OPTIMIZATION = "cpu_optimization"
    DISK_OPTIMIZATION = "disk_optimization"
    NETWORK_OPTIMIZATION = "network_optimization"
    ALGORITHM_OPTIMIZATION = "algorithm_optimization"
    CONFIGURATION_OPTIMIZATION = "configuration_optimization"


@dataclass
class PerformanceMetric:
    """Unified performance metric definition"""
    metric_id: str
    metric_type: PerformanceMetricType
    name: str
    value: float
    unit: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceSnapshot:
    """Performance snapshot at a point in time"""
    snapshot_id: str
    timestamp: float
    metrics: Dict[str, PerformanceMetric]
    system_info: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceAnalysis:
    """Performance analysis result"""
    analysis_id: str
    timestamp: float
    metric_type: PerformanceMetricType
    current_value: float
    historical_average: float
    trend: str  # "improving", "stable", "declining"
    recommendations: List[str]
    severity: PerformanceLevel
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OptimizationSuggestion:
    """Performance optimization suggestion"""
    suggestion_id: str
    optimization_type: OptimizationType
    title: str
    description: str
    expected_impact: float
    priority: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceThreshold:
    """Performance threshold definition"""
    metric_type: PerformanceMetricType
    warning_threshold: float
    critical_threshold: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceReport:
    """Comprehensive performance report"""
    report_id: str
    timestamp: float
    time_period: str
    summary: Dict[str, Any]
    metrics: List[PerformanceMetric]
    analyses: List[PerformanceAnalysis]
    suggestions: List[OptimizationSuggestion]
    metadata: Dict[str, Any] = field(default_factory=dict)
