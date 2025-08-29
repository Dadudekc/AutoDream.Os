#!/usr/bin/env python3
"""
System Configuration - V2 Modular Architecture
==============================================

System-wide performance configuration and targets.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class Environment(Enum):
    """System environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(Enum):
    """Logging level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class PerformanceTargets:
    """Performance target definitions."""
    target_response_time_ms: float = 500.0
    target_throughput_req_per_sec: float = 1000.0
    target_scalability_efficiency: float = 0.8
    target_reliability_percent: float = 99.0
    target_memory_usage_percent: float = 80.0
    target_cpu_usage_percent: float = 70.0
    
    def get_target(self, metric_name: str) -> Optional[float]:
        """Get target value for specific metric."""
        return getattr(self, f"target_{metric_name}", None)
    
    def validate_targets(self) -> List[str]:
        """Validate all performance targets."""
        errors = []
        if self.target_response_time_ms <= 0:
            errors.append("Response time target must be positive")
        if self.target_throughput_req_per_sec <= 0:
            errors.append("Throughput target must be positive")
        if not 0 <= self.target_scalability_efficiency <= 1:
            errors.append("Scalability efficiency must be between 0 and 1")
        if not 0 <= self.target_reliability_percent <= 100:
            errors.append("Reliability must be between 0 and 100")
        return errors


@dataclass
class SystemConfig:
    """System configuration settings."""
    system_name: str = "AutoDream.Os"
    environment: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    performance_targets: PerformanceTargets = field(default_factory=PerformanceTargets)
    
    # System settings
    max_concurrent_benchmarks: int = 5
    benchmark_timeout_default: int = 300
    metrics_retention_days: int = 30
    cleanup_interval_hours: int = 24
    
    def is_production(self) -> bool:
        """Check if system is in production environment."""
        return self.environment == Environment.PRODUCTION
    
    def get_log_level_value(self) -> str:
        """Get log level as string value."""
        return self.log_level.value
    
    def validate_config(self) -> List[str]:
        """Validate system configuration."""
        errors = []
        if self.max_concurrent_benchmarks <= 0:
            errors.append("Max concurrent benchmarks must be positive")
        if self.benchmark_timeout_default <= 0:
            errors.append("Benchmark timeout must be positive")
        if self.metrics_retention_days <= 0:
            errors.append("Metrics retention must be positive")
        
        # Validate performance targets
        errors.extend(self.performance_targets.validate_targets())
        return errors
