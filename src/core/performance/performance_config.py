
# MIGRATED: This file has been migrated to the centralized configuration system
#!/usr/bin/env python3
"""
Performance Configuration - Performance System Configuration

Extracted from unified_performance_system.py to achieve V2 compliance.
Contains configuration management, settings, and environment handling.

Author: Agent-8 (Technical Debt Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .performance_core import (
    ValidationSeverity, PerformanceLevel, BenchmarkType
)


@dataclass
class PerformanceConfig:
    """Performance system configuration."""
    
    # System settings
    system_name: str = "default"
    environment: str = "development"
    enable_monitoring: bool = True
    enable_validation: bool = True
    enable_reporting: bool = True
    enable_benchmarking: bool = True
    
    # Monitoring settings
    monitoring_interval_seconds: float = 5.0
    metrics_retention_days: int = 30
    max_metrics_per_metric: int = 1000
    
    # Validation settings
    validation_timeout_seconds: float = 30.0
    max_validation_rules: int = 100
    enable_auto_thresholds: bool = True
    
    # Reporting settings
    report_retention_days: int = 90
    default_report_format: str = "json"
    enable_auto_reports: bool = True
    auto_report_interval_hours: int = 24
    
    # Benchmarking settings
    max_concurrent_benchmarks: int = 5
    benchmark_timeout_seconds: float = 300.0
    enable_benchmark_scheduling: bool = True
    
    # Alert settings
    enable_alerts: bool = True
    alert_retention_days: int = 30
    max_active_alerts: int = 100
    
    # Performance thresholds
    default_thresholds: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "cpu_usage": {"warning": 80.0, "critical": 95.0},
        "memory_usage": {"warning": 85.0, "critical": 95.0},
        "disk_usage": {"warning": 80.0, "critical": 90.0},
        "response_time": {"warning": 1000.0, "critical": 5000.0},
        "error_rate": {"warning": 5.0, "critical": 10.0}
    })
    
    # Validation rules
    default_validation_rules: List[Dict[str, Any]] = field(default_factory=lambda: [
        {
            "rule_name": "cpu_high_usage",
            "metric_name": "cpu_usage",
            "threshold": 90.0,
            "operator": "gt",
            "severity": ValidationSeverity.WARNING,
            "description": "CPU usage is very high"
        },
        {
            "rule_name": "memory_critical_usage",
            "metric_name": "memory_usage",
            "threshold": 95.0,
            "operator": "gt",
            "severity": ValidationSeverity.CRITICAL,
            "description": "Memory usage is critical"
        }
    ])
    
    # Benchmark configurations
    default_benchmarks: List[Dict[str, Any]] = field(default_factory=lambda: [
        {
            "name": "cpu_stress_test",
            "description": "CPU stress testing benchmark",
            "benchmark_type": BenchmarkType.STRESS,
            "duration": 60,
            "iterations": 1
        },
        {
            "name": "memory_load_test",
            "description": "Memory load testing benchmark",
            "benchmark_type": BenchmarkType.LOAD,
            "duration": 120,
            "iterations": 1
        }
    ])


class PerformanceConfigManager:
    """
    Performance configuration manager.
    
    Handles loading, saving, and managing performance system configuration
    from various sources (files, environment variables, etc.).
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the configuration manager."""
        self.logger = logging.getLogger(__name__)
        
        # Configuration paths
        self.config_path = config_path or self._get_default_config_path()
        self.env_prefix = "PERF_"
        
        # Current configuration
        self.config = PerformanceConfig()
        
        # Configuration sources
        self.config_sources = []
        
        self.logger.info("Performance Config Manager initialized")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        config_dir = Path.home() / ".config" / "performance_system"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "performance_config.json")
    
    def load_configuration(self, source: str = "auto") -> bool:
        """Load configuration from specified source."""
        try:
            self.logger.info(f"Loading configuration from source: {source}")
            
            if source == "auto":
                # Try multiple sources in order of priority
                sources = ["environment", "file", "default"]
            else:
                sources = [source]
            
            for src in sources:
                if self._load_from_source(src):
                    self.logger.info(f"Configuration loaded from: {src}")
                    return True
            
            self.logger.warning("No configuration sources available, using defaults")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False
    
    def _load_from_source(self, source: str) -> bool:
        """Load configuration from a specific source."""
        try:
            if source == "environment":
                return self._load_from_environment()
            elif source == "file":
                return self._load_from_file()
            elif source == "default":
                return self._load_defaults()
            else:
                self.logger.warning(f"Unknown configuration source: {source}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to load from {source}: {e}")
            return False
    
    def _load_from_environment(self) -> bool:
        """Load configuration from environment variables."""
        try:
            env_vars = os.environ
            
            # System settings
            if f"{self.env_prefix}SYSTEM_NAME" in env_vars:
                self.config.system_name = env_vars[f"{self.env_prefix}SYSTEM_NAME"]
            
            if f"{self.env_prefix}ENVIRONMENT" in env_vars:
                self.config.environment = env_vars[f"{self.env_prefix}ENVIRONMENT"]
            
            # Boolean settings
            if f"{self.env_prefix}ENABLE_MONITORING" in env_vars:
                self.config.enable_monitoring = env_vars[f"{self.env_prefix}ENABLE_MONITORING"].lower() == "true"
            
            if f"{self.env_prefix}ENABLE_VALIDATION" in env_vars:
                self.config.enable_validation = env_vars[f"{self.env_prefix}ENABLE_VALIDATION"].lower() == "true"
            
            if f"{self.env_prefix}ENABLE_REPORTING" in env_vars:
                self.config.enable_reporting = env_vars[f"{self.env_prefix}ENABLE_REPORTING"].lower() == "true"
            
            if f"{self.env_prefix}ENABLE_BENCHMARKING" in env_vars:
                self.config.enable_benchmarking = env_vars[f"{self.env_prefix}ENABLE_BENCHMARKING"].lower() == "true"
            
            if f"{self.env_prefix}ENABLE_ALERTS" in env_vars:
                self.config.enable_alerts = env_vars[f"{self.env_prefix}ENABLE_ALERTS"].lower() == "true"
            
            # Numeric settings
            if f"{self.env_prefix}MONITORING_INTERVAL" in env_vars:
                try:
                    self.config.monitoring_interval_seconds = float(env_vars[f"{self.env_prefix}MONITORING_INTERVAL"])
                except ValueError:
                    self.logger.warning(f"Invalid monitoring interval: {env_vars[f'{self.env_prefix}MONITORING_INTERVAL']}")
            
            if f"{self.env_prefix}METRICS_RETENTION_DAYS" in env_vars:
                try:
                    self.config.metrics_retention_days = int(env_vars[f"{self.env_prefix}METRICS_RETENTION_DAYS"])
                except ValueError:
                    self.logger.warning(f"Invalid metrics retention: {env_vars[f'{self.env_prefix}METRICS_RETENTION_DAYS']}")
            
            self.config_sources.append("environment")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load from environment: {e}")
            return False
    
    def _load_from_file(self) -> bool:
        """Load configuration from file."""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                self.logger.info(f"Configuration file not found: {self.config_path}")
                return False
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Update configuration with file data
            self._update_config_from_dict(config_data)
            
            self.config_sources.append("file")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load from file: {e}")
            return False
    
    def _load_defaults(self) -> bool:
        """Load default configuration."""
        try:
            # Configuration is already set to defaults in __init__
            self.config_sources.append("default")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load defaults: {e}")
            return False
    
    def _update_config_from_dict(self, config_data: Dict[str, Any]):
        """Update configuration from dictionary data."""
        try:
            # Update simple attributes
            for key, value in config_data.items():
                if hasattr(self.config, key) and not key.startswith("default_"):
                    setattr(self.config, key, value)
            
            # Update complex attributes
            if "default_thresholds" in config_data:
                self.config.default_thresholds.update(config_data["default_thresholds"])
            
            if "default_validation_rules" in config_data:
                self.config.default_validation_rules.extend(config_data["default_validation_rules"])
            
            if "default_benchmarks" in config_data:
                self.config.default_benchmarks.extend(config_data["default_benchmarks"])
                
        except Exception as e:
            self.logger.error(f"Failed to update config from dict: {e}")
    
    def save_configuration(self, filepath: Optional[str] = None) -> bool:
        """Save current configuration to file."""
        try:
            save_path = filepath or self.config_path
            config_file = Path(save_path)
            
            # Ensure directory exists
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert configuration to dictionary
            config_dict = self._config_to_dict()
            
            # Save to file
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, default=str)
            
            self.logger.info(f"Configuration saved to: {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def _config_to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        config_dict = {}
        
        # Add simple attributes
        for key, value in self.config.__dict__.items():
            if not key.startswith("_"):
                config_dict[key] = value
        
        return config_dict
    
    def get_config(self) -> PerformanceConfig:
        """Get current configuration."""
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values."""
        try:
            self._update_config_from_dict(updates)
            self.logger.info("Configuration updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values."""
        try:
            self.config = PerformanceConfig()
            self.config_sources = ["default"]
            self.logger.info("Configuration reset to defaults")
            return True
        except Exception as e:
            self.logger.error(f"Failed to reset configuration: {e}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary."""
        return {
            "system_name": self.config.system_name,
            "environment": self.config.environment,
            "features_enabled": {
                "monitoring": self.config.enable_monitoring,
                "validation": self.config.enable_validation,
                "reporting": self.config.enable_reporting,
                "benchmarking": self.config.enable_benchmarking,
                "alerts": self.config.enable_alerts
            },
            "settings": {
                "monitoring_interval": f"{self.config.monitoring_interval_seconds}s",
                "metrics_retention": f"{self.config.metrics_retention_days} days",
                "report_retention": f"{self.config.report_retention_days} days",
                "max_concurrent_benchmarks": self.config.max_concurrent_benchmarks
            },
            "sources": self.config_sources,
            "config_file": self.config_path
        }
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration."""
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }
        
        try:
            # Basic validation
            if self.config.monitoring_interval_seconds <= 0:
                validation_result["errors"].append("Monitoring interval must be positive")
                validation_result["valid"] = False
            
            if self.config.metrics_retention_days <= 0:
                validation_result["errors"].append("Metrics retention must be positive")
                validation_result["valid"] = False
            
        except Exception as e:
            validation_result["errors"].append(f"Configuration validation failed: {e}")
            validation_result["valid"] = False
        
        return validation_result


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and test configuration manager
    config_manager = PerformanceConfigManager()
    
    # Load configuration
    if config_manager.load_configuration():
        print("✅ Configuration loaded successfully")
        
        # Get configuration summary
        summary = config_manager.get_config_summary()
        print(f"📊 System: {summary['system_name']}")
        print(f"🌍 Environment: {summary['environment']}")
        print(f"🔧 Features: {summary['features_enabled']}")
        print(f"📁 Sources: {summary['sources']}")
        
        # Validate configuration
        validation = config_manager.validate_configuration()
        if validation["valid"]:
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration has errors:")
            for error in validation["errors"]:
                print(f"  - {error}")
        
        if validation["warnings"]:
            print("⚠️ Configuration warnings:")
            for warning in validation["warnings"]:
                print(f"  - {warning}")
    else:
        print("❌ Failed to load configuration")
