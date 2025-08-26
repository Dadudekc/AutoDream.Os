#!/usr/bin/env python3
"""
Performance Config Manager - V2 Modular Architecture
===================================================

Handles all performance configuration operations.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class PerformanceConfigManager:
    """
    Performance Config Manager - Single responsibility: Manage performance configuration
    
    Handles all configuration operations including:
    - Configuration loading and validation
    - Default configuration setup
    - Configuration persistence
    - Configuration updates
    """

    def __init__(self, config_file: Optional[str] = None):
        """Initialize config manager"""
        self.logger = logging.getLogger(f"{__name__}.PerformanceConfigManager")
        
        # Configuration file path
        self.config_file = config_file or "config/performance.json"
        
        # Default configuration
        self.default_config = self._create_default_config()
        
        # Current configuration
        self.config = self.default_config.copy()
        
        # Load configuration if file exists
        if Path(self.config_file).exists():
            self.load_config()
        else:
            self.logger.info(f"Configuration file {self.config_file} not found, using defaults")
        
        self.logger.info("✅ Performance Config Manager initialized successfully")

    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        try:
            return {
                "environment": "development",
                "log_level": "INFO",
                "monitoring_interval": 60,
                "data_retention_days": 30,
                "performance_targets": {
                    "response_time_ms": 200.0,
                    "throughput_ops_per_sec": 1000.0,
                    "cpu_usage_percent": 70.0,
                    "memory_usage_percent": 75.0,
                    "disk_usage_percent": 80.0,
                    "network_latency_ms": 50.0
                },
                "validation_config": {
                    "enabled": True,
                    "check_interval_seconds": 30,
                    "thresholds": [
                        {
                            "metric_name": "cpu_usage_percent",
                            "warning_value": 80.0,
                            "critical_value": 95.0,
                            "operator": ">="
                        },
                        {
                            "metric_name": "memory_usage_percent",
                            "warning_value": 85.0,
                            "critical_value": 95.0,
                            "operator": ">="
                        },
                        {
                            "metric_name": "response_time_ms",
                            "warning_value": 500.0,
                            "critical_value": 1000.0,
                            "operator": ">="
                        }
                    ]
                },
                "benchmark_config": {
                    "enabled": True,
                    "default_duration_seconds": 30,
                    "max_concurrent_benchmarks": 5,
                    "execution_config": {
                        "timeout_seconds": 300,
                        "retry_count": 3,
                        "parallel_execution": True
                    }
                },
                "alert_config": {
                    "enabled": True,
                    "channels": [
                        {
                            "name": "console",
                            "type": "console",
                            "enabled": True,
                            "config": {}
                        },
                        {
                            "name": "log",
                            "type": "log",
                            "enabled": True,
                            "config": {"level": "WARNING"}
                        }
                    ],
                    "default_severity": "warning"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create default configuration: {e}")
            # Return minimal config on error
            return {
                "environment": "development",
                "log_level": "INFO",
                "monitoring_interval": 60,
                "data_retention_days": 30
            }

    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                self.logger.warning(f"Configuration file {self.config_file} not found")
                return False
            
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            # Update configuration with loaded data
            self._update_config_from_dict(config_data)
            
            self.logger.info(f"✅ Configuration loaded from {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False

    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert config to dictionary
            config_dict = self._config_to_dict()
            
            with open(config_path, 'w') as f:
                json.dump(config_dict, f, indent=2, default=str)
            
            self.logger.info(f"✅ Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False

    def _update_config_from_dict(self, config_data: Dict[str, Any]) -> None:
        """Update configuration from dictionary data"""
        try:
            # Update basic settings
            for key, value in config_data.items():
                if key in self.config:
                    self.config[key] = value
                else:
                    self.config[key] = value
                    
        except Exception as e:
            self.logger.error(f"Failed to update configuration from dict: {e}")

    def _config_to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        try:
            config_dict = self.config.copy()
            config_dict["last_updated"] = datetime.now().isoformat()
            return config_dict
            
        except Exception as e:
            self.logger.error(f"Failed to convert config to dict: {e}")
            return {"error": str(e)}

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values"""
        try:
            self._update_config_from_dict(updates)
            return self.save_config()
            
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False

    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults"""
        try:
            self.config = self.default_config.copy()
            return self.save_config()
            
        except Exception as e:
            self.logger.error(f"Failed to reset configuration: {e}")
            return False

    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary"""
        try:
            return {
                "config_file": self.config_file,
                "environment": self.config.get("environment", "unknown"),
                "log_level": self.config.get("log_level", "INFO"),
                "monitoring_interval": self.config.get("monitoring_interval", 60),
                "data_retention_days": self.config.get("data_retention_days", 30),
                "validation_enabled": self.config.get("validation_config", {}).get("enabled", False),
                "benchmark_enabled": self.config.get("benchmark_config", {}).get("enabled", False),
                "alert_enabled": self.config.get("alert_config", {}).get("enabled", False),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get config summary: {e}")
            return {"error": str(e)}

    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration"""
        try:
            validation_results = {
                "valid": True,
                "errors": [],
                "warnings": []
            }
            
            # Check basic settings
            if self.config.get("monitoring_interval", 0) <= 0:
                validation_results["valid"] = False
                validation_results["errors"].append("Monitoring interval must be positive")
            
            if self.config.get("data_retention_days", 0) <= 0:
                validation_results["valid"] = False
                validation_results["errors"].append("Data retention days must be positive")
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Failed to validate configuration: {e}")
            return {"valid": False, "error": str(e)}
