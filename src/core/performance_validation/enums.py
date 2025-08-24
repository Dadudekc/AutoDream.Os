#!/usr/bin/env python3
"""
Performance Validation Enums - V2 Core Performance Testing & Optimization

Performance validation system enums and constants.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from enum import Enum


class BenchmarkType(Enum):
    """Performance benchmark types"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    RESOURCE_UTILIZATION = "resource_utilization"
    LATENCY = "latency"
    MEMORY_USAGE = "memory_usage"
    CPU_UTILIZATION = "cpu_utilization"
    NETWORK_IO = "network_io"
    DISK_IO = "disk_io"
    CONCURRENT_USERS = "concurrent_users"
    ERROR_RATE = "error_rate"
    AVAILABILITY = "availability"
    RECOVERY_TIME = "recovery_time"


class PerformanceLevel(Enum):
    """Performance level classifications"""
    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"
    DEVELOPMENT_READY = "development_ready"
    NOT_READY = "not_ready"
    OPTIMIZATION_NEEDED = "optimization_needed"
    CRITICAL_ISSUES = "critical_issues"
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"


class OptimizationTarget(Enum):
    """Optimization targets"""
    RESPONSE_TIME_IMPROVEMENT = "response_time_improvement"
    THROUGHPUT_INCREASE = "throughput_increase"
    SCALABILITY_ENHANCEMENT = "scalability_enhancement"
    RELIABILITY_IMPROVEMENT = "reliability_improvement"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    MEMORY_OPTIMIZATION = "memory_optimization"
    CPU_OPTIMIZATION = "cpu_optimization"
    NETWORK_OPTIMIZATION = "network_optimization"
    DATABASE_OPTIMIZATION = "database_optimization"
    CACHE_OPTIMIZATION = "cache_optimization"
    ALGORITHM_OPTIMIZATION = "algorithm_optimization"
    CONFIGURATION_OPTIMIZATION = "configuration_optimization"
