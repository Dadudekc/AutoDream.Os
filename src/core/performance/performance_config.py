#!/usr/bin/env python3
"""
Performance Config - Unified Performance Validation Configuration
==============================================================

Performance validation configuration management consolidated from multiple files.
Follows Single Responsibility Principle with focused configuration functionality.

Author: Performance Validation Consolidation Team
License: MIT
"""

import logging
import json
import os
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from pathlib import Path

# from src.utils.stability_improvements import stability_manager, safe_import


@dataclass
class ValidationThreshold:
    """Performance validation threshold configuration."""
    metric_name: str
    threshold_value: float
    operator: str  # 'gt', 'lt', 'eq', 'gte', 'lte'
    severity: str  # 'critical', 'warning', 'info'
    description: str
    enabled: bool = True


@dataclass
class BenchmarkConfig:
    """Benchmark execution configuration."""
    benchmark_type: str
    enabled: bool = True
    timeout_seconds: int = 300
    max_iterations: int = 5
    warmup_iterations: int = 2
    target_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceValidationConfig:
    """Comprehensive performance validation configuration."""
    
    # System settings
    system_name: str = "AutoDream.Os"
    environment: str = "development"
    log_level: str = "INFO"
    
    # Validation thresholds
    validation_thresholds: List[ValidationThreshold] = field(default_factory=list)
    
    # Benchmark configurations
    benchmark_configs: List[BenchmarkConfig] = field(default_factory=list)
    
    # Reporting settings
    report_formats: List[str] = field(default_factory=lambda: ["json", "text"])
    default_report_format: str = "json"
    report_retention_days: int = 30
    
    # Alert settings
    alert_enabled: bool = True
    alert_severity_minimum: str = "warning"
    alert_channels: List[str] = field(default_factory=lambda: ["console", "log"])
    
    # Performance targets
    target_response_time_ms: float = 500.0
    target_throughput_req_per_sec: float = 1000.0
    target_scalability_efficiency: float = 0.8
    target_reliability_percent: float = 99.0
    
    def __post_init__(self):
        """Initialize default configuration if not provided."""
        if not self.validation_thresholds:
            self._setup_default_thresholds()
        
        if not self.benchmark_configs:
            self._setup_default_benchmarks()
    
    def _setup_default_thresholds(self):
        """Setup default validation thresholds."""
        self.validation_thresholds = [
            ValidationThreshold(
                metric_name="average_response_time",
                threshold_value=0.5,  # 500ms
                operator="lte",
                severity="critical",
                description="Response time must be under 500ms"
            ),
            ValidationThreshold(
                metric_name="average_throughput",
                threshold_value=1000.0,  # 1000 req/s
                operator="gte",
                severity="warning",
                description="Throughput should be at least 1000 req/s"
            ),
            ValidationThreshold(
                metric_name="scalability_factor",
                threshold_value=0.8,  # 80% efficiency
                operator="gte",
                severity="warning",
                description="Scalability efficiency should be at least 80%"
            ),
            ValidationThreshold(
                metric_name="success_rate",
                threshold_value=0.99,  # 99% success rate
                operator="gte",
                severity="critical",
                description="Success rate must be at least 99%"
            ),
            ValidationThreshold(
                metric_name="cpu_utilization",
                threshold_value=0.8,  # 80% CPU usage
                operator="lte",
                severity="warning",
                description="CPU utilization should be under 80%"
            ),
            ValidationThreshold(
                metric_name="memory_utilization",
                threshold_value=0.85,  # 85% memory usage
                operator="lte",
                severity="warning",
                description="Memory utilization should be under 85%"
            )
        ]
    
    def _setup_default_benchmarks(self):
        """Setup default benchmark configurations."""
        self.benchmark_configs = [
            BenchmarkConfig(
                benchmark_type="response_time",
                timeout_seconds=120,
                max_iterations=10,
                warmup_iterations=3,
                target_metrics={"target_response_time_ms": 500}
            ),
            BenchmarkConfig(
                benchmark_type="throughput",
                timeout_seconds=180,
                max_iterations=8,
                warmup_iterations=2,
                target_metrics={"target_throughput_req_per_sec": 1000}
            ),
            BenchmarkConfig(
                benchmark_type="scalability",
                timeout_seconds=300,
                max_iterations=5,
                warmup_iterations=2,
                target_metrics={"target_scalability_efficiency": 0.8}
            ),
            BenchmarkConfig(
                benchmark_type="reliability",
                timeout_seconds=240,
                max_iterations=15,
                warmup_iterations=3,
                target_metrics={"target_success_rate": 0.99}
            ),
            BenchmarkConfig(
                benchmark_type="resource_utilization",
                timeout_seconds=120,
                max_iterations=5,
                warmup_iterations=1,
                target_metrics={"max_cpu_utilization": 0.8, "max_memory_utilization": 0.85}
            )
        ]


class PerformanceConfigManager:
    """
    Unified performance configuration management system.
    
    Responsibilities:
    - Configuration loading and validation
    - Threshold management
    - Rule configuration
    - Environment-specific settings
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = logging.getLogger(f"{__name__}.PerformanceConfigManager")
        self.config_file = config_file
        self.config = PerformanceValidationConfig()
        
        # Load configuration if file provided
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str) -> bool:
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to the configuration file
            
        Returns:
            True if configuration loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(config_file):
                self.logger.warning(f"Configuration file not found: {config_file}")
                return False
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Update configuration with loaded data
            self._update_config_from_dict(config_data)
            
            self.logger.info(f"Configuration loaded from {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading configuration from {config_file}: {e}")
            return False
    
    def _update_config_from_dict(self, config_data: Dict[str, Any]):
        """Update configuration from dictionary data."""
        # Update basic settings
        for key, value in config_data.items():
            if hasattr(self.config, key):
                if key == "validation_thresholds":
                    self._update_thresholds_from_dict(value)
                elif key == "benchmark_configs":
                    self._update_benchmarks_from_dict(value)
                else:
                    setattr(self.config, key, value)
    
    def _update_thresholds_from_dict(self, thresholds_data: List[Dict[str, Any]]):
        """Update validation thresholds from dictionary data."""
        new_thresholds = []
        for threshold_data in thresholds_data:
            threshold = ValidationThreshold(
                metric_name=threshold_data.get("metric_name", ""),
                threshold_value=threshold_data.get("threshold_value", 0.0),
                operator=threshold_data.get("operator", "eq"),
                severity=threshold_data.get("severity", "info"),
                description=threshold_data.get("description", ""),
                enabled=threshold_data.get("enabled", True)
            )
            new_thresholds.append(threshold)
        
        if new_thresholds:
            self.config.validation_thresholds = new_thresholds
    
    def _update_benchmarks_from_dict(self, benchmarks_data: List[Dict[str, Any]]):
        """Update benchmark configurations from dictionary data."""
        new_benchmarks = []
        for benchmark_data in benchmarks_data:
            benchmark = BenchmarkConfig(
                benchmark_type=benchmark_data.get("benchmark_type", ""),
                enabled=benchmark_data.get("enabled", True),
                timeout_seconds=benchmark_data.get("timeout_seconds", 300),
                max_iterations=benchmark_data.get("max_iterations", 5),
                warmup_iterations=benchmark_data.get("warmup_iterations", 2),
                target_metrics=benchmark_data.get("target_metrics", {})
            )
            new_benchmarks.append(benchmark)
        
        if new_benchmarks:
            self.config.benchmark_configs = new_benchmarks
    
    def save_config(self, config_file: Optional[str] = None) -> bool:
        """
        Save current configuration to a JSON file.
        
        Args:
            config_file: Path to save configuration (uses default if not specified)
            
        Returns:
            True if configuration saved successfully, False otherwise
        """
        try:
            save_path = config_file or self.config_file
            if not save_path:
                self.logger.error("No configuration file path specified")
                return False
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Convert configuration to dictionary
            config_dict = self._config_to_dict()
            
            # Save to file
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, default=str)
            
            self.logger.info(f"Configuration saved to {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False
    
    def _config_to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        config_dict = {}
        
        # Basic settings
        for key in [
            "system_name", "environment", "log_level", "report_formats",
            "default_report_format", "report_retention_days", "alert_enabled",
            "alert_severity_minimum", "alert_channels", "target_response_time_ms",
            "target_throughput_req_per_sec", "target_scalability_efficiency",
            "target_reliability_percent"
        ]:
            if hasattr(self.config, key):
                config_dict[key] = getattr(self.config, key)
        
        # Validation thresholds
        config_dict["validation_thresholds"] = [
            {
                "metric_name": t.metric_name,
                "threshold_value": t.threshold_value,
                "operator": t.operator,
                "severity": t.severity,
                "description": t.description,
                "enabled": t.enabled
            }
            for t in self.config.validation_thresholds
        ]
        
        # Benchmark configurations
        config_dict["benchmark_configs"] = [
            {
                "benchmark_type": b.benchmark_type,
                "enabled": b.enabled,
                "timeout_seconds": b.timeout_seconds,
                "max_iterations": b.max_iterations,
                "warmup_iterations": b.warmup_iterations,
                "target_metrics": b.target_metrics
            }
            for b in self.config.benchmark_configs
        ]
        
        return config_dict
    
    def get_threshold(self, metric_name: str) -> Optional[ValidationThreshold]:
        """Get validation threshold for a specific metric."""
        for threshold in self.config.validation_thresholds:
            if threshold.metric_name == metric_name and threshold.enabled:
                return threshold
        return None
    
    def get_benchmark_config(self, benchmark_type: str) -> Optional[BenchmarkConfig]:
        """Get benchmark configuration for a specific type."""
        for benchmark in self.config.benchmark_configs:
            if benchmark.benchmark_type == benchmark_type and benchmark.enabled:
                return benchmark
        return None
    
    def update_threshold(
        self, 
        metric_name: str, 
        threshold_value: float, 
        operator: str = "lte",
        severity: str = "warning"
    ) -> bool:
        """
        Update or add a validation threshold.
        
        Args:
            metric_name: Name of the metric
            threshold_value: Threshold value
            operator: Comparison operator
            severity: Alert severity
            
        Returns:
            True if threshold updated successfully, False otherwise
        """
        try:
            # Find existing threshold
            existing_threshold = None
            for threshold in self.config.validation_thresholds:
                if threshold.metric_name == metric_name:
                    existing_threshold = threshold
                    break
            
            if existing_threshold:
                # Update existing threshold
                existing_threshold.threshold_value = threshold_value
                existing_threshold.operator = operator
                existing_threshold.severity = severity
                self.logger.info(f"Updated threshold for {metric_name}")
            else:
                # Add new threshold
                new_threshold = ValidationThreshold(
                    metric_name=metric_name,
                    threshold_value=threshold_value,
                    operator=operator,
                    severity=severity,
                    description=f"Threshold for {metric_name}",
                    enabled=True
                )
                self.config.validation_thresholds.append(new_threshold)
                self.logger.info(f"Added new threshold for {metric_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating threshold for {metric_name}: {e}")
            return False
    
    def enable_benchmark(self, benchmark_type: str) -> bool:
        """Enable a specific benchmark type."""
        benchmark = self.get_benchmark_config(benchmark_type)
        if benchmark:
            benchmark.enabled = True
            self.logger.info(f"Enabled benchmark: {benchmark_type}")
            return True
        return False
    
    def disable_benchmark(self, benchmark_type: str) -> bool:
        """Disable a specific benchmark type."""
        benchmark = self.get_benchmark_config(benchmark_type)
        if benchmark:
            benchmark.enabled = False
            self.logger.info(f"Disabled benchmark: {benchmark_type}")
            return True
        return False
    
    def get_enabled_benchmarks(self) -> List[str]:
        """Get list of enabled benchmark types."""
        return [
            benchmark.benchmark_type 
            for benchmark in self.config.benchmark_configs 
            if benchmark.enabled
        ]
    
    def validate_config(self) -> List[str]:
        """
        Validate the current configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate thresholds
        for threshold in self.config.validation_thresholds:
            if not threshold.metric_name:
                errors.append(f"Threshold missing metric name")
            if threshold.threshold_value < 0:
                errors.append(f"Threshold value for {threshold.metric_name} must be non-negative")
            if threshold.operator not in ["gt", "lt", "eq", "gte", "lte"]:
                errors.append(f"Invalid operator '{threshold.operator}' for {threshold.metric_name}")
            if threshold.severity not in ["critical", "warning", "info"]:
                errors.append(f"Invalid severity '{threshold.severity}' for {threshold.metric_name}")
        
        # Validate benchmark configs
        for benchmark in self.config.benchmark_configs:
            if not benchmark.benchmark_type:
                errors.append("Benchmark missing type")
            if benchmark.timeout_seconds <= 0:
                errors.append(f"Timeout for {benchmark.benchmark_type} must be positive")
            if benchmark.max_iterations <= 0:
                errors.append(f"Max iterations for {benchmark.benchmark_type} must be positive")
            if benchmark.warmup_iterations < 0:
                errors.append(f"Warmup iterations for {benchmark.benchmark_type} must be non-negative")
        
        return errors
    
    def create_default_config_file(self, config_file: str) -> bool:
        """
        Create a default configuration file.
        
        Args:
            config_file: Path to create the configuration file
            
        Returns:
            True if file created successfully, False otherwise
        """
        try:
            # Use default configuration
            self.config = PerformanceValidationConfig()
            
            # Save to file
            return self.save_config(config_file)
            
        except Exception as e:
            self.logger.error(f"Error creating default configuration file: {e}")
            return False
