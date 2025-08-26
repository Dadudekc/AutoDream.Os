#!/usr/bin/env python3
"""
Performance Package - V2 Modular Architecture
============================================

Unified performance management system with modular components.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

# Main unified system
from .unified_performance_system import UnifiedPerformanceSystem

# Configuration management
from .config.config_manager import PerformanceConfigManager
from .config.validation_config import ValidationThreshold, ValidationConfig
from .config.benchmark_config import BenchmarkConfig, BenchmarkExecutionConfig
from .config.system_config import SystemConfig, PerformanceTargets, Environment, LogLevel
from .config.alert_config import AlertConfig, AlertChannel, AlertSeverity, AlertChannelType

# Performance monitoring
from .monitoring.monitoring_manager import MonitoringManager
from .monitoring.monitoring_types import MetricData, MetricType, MonitoringConfig, CollectionResult

# Performance validation
from .validation.validation_engine import ValidationEngine
from .validation.validation_types import ValidationStatus, ValidationSeverity, ValidationContext, ValidationResult, ValidationSummary

# Performance benchmarking
from .benchmarking.benchmark_runner import BenchmarkRunner
from .benchmarking.benchmark_types import BenchmarkType, BenchmarkStatus, BenchmarkPhase, BenchmarkMetrics, BenchmarkResult, BenchmarkConfig

# Performance reporting
from .reporting.report_generator import PerformanceReportGenerator
from .reporting.report_types import PerformanceReport, ReportSection, ReportMetric, ReportFormat, ReportStatus, MetricType

# Performance analysis
from .analysis.performance_analyzer import PerformanceAnalyzer, PerformanceLevel

# Connection management
from .connection.connection_pool_manager import ConnectionPoolManager

# Backwards compatibility aliases
PerformanceValidationOrchestrator = UnifiedPerformanceSystem
PerformanceValidationCore = UnifiedPerformanceSystem
PerformanceReporter = UnifiedPerformanceSystem
PerformanceConfigManager = UnifiedPerformanceSystem

__all__ = [
    # Main system
    "UnifiedPerformanceSystem",
    
    # Configuration
    "PerformanceConfigManager",
    "ValidationThreshold",
    "ValidationConfig", 
    "BenchmarkConfig",
    "BenchmarkExecutionConfig",
    "SystemConfig",
    "PerformanceTargets",
    "Environment",
    "LogLevel",
    "AlertConfig",
    "AlertChannel",
    "AlertSeverity",
    "AlertChannelType",
    
    # Monitoring
    "MonitoringManager",
    "MetricData",
    "MetricType",
    "MonitoringConfig",
    "CollectionResult",
    
    # Validation
    "ValidationEngine",
    "ValidationStatus",
    "ValidationSeverity",
    "ValidationContext",
    "ValidationResult",
    "ValidationSummary",
    
    # Benchmarking
    "BenchmarkRunner",
    "BenchmarkType",
    "BenchmarkStatus",
    "BenchmarkPhase",
    "BenchmarkMetrics",
    "BenchmarkResult",
    
    # Reporting
    "PerformanceReportGenerator",
    "PerformanceReport",
    "ReportSection",
    "ReportMetric",
    "ReportFormat",
    "ReportStatus",
    
    # Analysis
    "PerformanceAnalyzer",
    "PerformanceLevel",
    
    # Connection management
    "ConnectionPoolManager",
    
    # Backwards compatibility
    "PerformanceValidationOrchestrator",
    "PerformanceValidationCore",
    "PerformanceReporter",
]