#!/usr/bin/env python3
"""
⚖️ Health Threshold Manager - Agent_Cellphone_V2

This component is responsible for managing health thresholds and configurations.
Following V2 coding standards: ≤200 LOC, OOP design, SRP.
Now inherits from BaseManager for unified functionality.

Author: Foundation & Testing Specialist
License: MIT
"""

import logging
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from pathlib import Path
import json

from src.utils.stability_improvements import stability_manager, safe_import
from .base_manager import BaseManager, ManagerStatus, ManagerPriority

# Configure logging
logger = logging.getLogger(__name__)


class HealthMetricType(Enum):
    """Types of health metrics"""

    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    TASK_COMPLETION_RATE = "task_completion_rate"
    HEARTBEAT_FREQUENCY = "heartbeat_frequency"
    CONTRACT_SUCCESS_RATE = "contract_success_rate"
    COMMUNICATION_LATENCY = "communication_latency"


@dataclass
class HealthThreshold:
    """Health threshold configuration"""

    metric_type: str
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str


class HealthThresholdManager(BaseManager):
    """
    Health Threshold Manager - Single responsibility: Manage health thresholds and configurations.

    Follows V2 standards: ≤200 LOC, OOP design, SRP.
    Now inherits from BaseManager for unified functionality.
    """

    def __init__(self):
        """Initialize the threshold manager with BaseManager"""
        super().__init__(
            manager_id="health_threshold_manager",
            name="Health Threshold Manager",
            description="Manage health thresholds and configurations"
        )
        
        self.thresholds: Dict[str, HealthThreshold] = {}
        
        # Health threshold management tracking
        self.threshold_operations: List[Dict[str, Any]] = []
        self.validation_operations: List[Dict[str, Any]] = []
        self.configuration_changes: List[Dict[str, Any]] = []
        
        self._initialize_default_thresholds()
        self.logger.info("HealthThresholdManager initialized with default thresholds")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize health threshold management system"""
        try:
            self.logger.info("Starting Health Threshold Manager...")
            
            # Clear tracking data
            self.threshold_operations.clear()
            self.validation_operations.clear()
            self.configuration_changes.clear()
            
            # Verify thresholds are loaded
            if not self.thresholds:
                self._initialize_default_thresholds()
            
            self.logger.info("Health Threshold Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Health Threshold Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup health threshold management system"""
        try:
            self.logger.info("Stopping Health Threshold Manager...")
            
            # Save tracking data
            self._save_health_threshold_management_data()
            
            # Clear data
            self.threshold_operations.clear()
            self.validation_operations.clear()
            self.configuration_changes.clear()
            
            self.logger.info("Health Threshold Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Health Threshold Manager: {e}")
    
    def _on_heartbeat(self):
        """Health threshold manager heartbeat"""
        try:
            # Check health threshold management health
            self._check_health_threshold_management_health()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize health threshold management resources"""
        try:
            # Initialize data structures
            self.threshold_operations = []
            self.validation_operations = []
            self.configuration_changes = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup health threshold management resources"""
        try:
            # Clear data
            self.threshold_operations.clear()
            self.validation_operations.clear()
            self.configuration_changes.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reload default thresholds
            self._initialize_default_thresholds()
            
            # Reset tracking
            self.threshold_operations.clear()
            self.validation_operations.clear()
            self.configuration_changes.clear()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Health Threshold Management Methods
    # ============================================================================
    
    def _initialize_default_thresholds(self):
        """Initialize default health thresholds"""
        try:
            start_time = datetime.now()
            
            default_thresholds = [
                HealthThreshold(
                    "response_time",
                    warning_threshold=1000.0,  # 1 second
                    critical_threshold=5000.0,  # 5 seconds
                    unit="ms",
                    description="Response time threshold",
                ),
                HealthThreshold(
                    "memory_usage",
                    warning_threshold=80.0,  # 80%
                    critical_threshold=95.0,  # 95%
                    unit="%",
                    description="Memory usage threshold",
                ),
                HealthThreshold(
                    "cpu_usage",
                    warning_threshold=85.0,  # 85%
                    critical_threshold=95.0,  # 95%
                    unit="%",
                    description="CPU usage threshold",
                ),
                HealthThreshold(
                    "error_rate",
                    warning_threshold=5.0,  # 5%
                    critical_threshold=15.0,  # 15%
                    unit="%",
                    description="Error rate threshold",
                ),
                HealthThreshold(
                    "task_completion_rate",
                    warning_threshold=90.0,  # 90%
                    critical_threshold=75.0,  # 75%
                    unit="%",
                    description="Task completion rate threshold",
                ),
                HealthThreshold(
                    "heartbeat_frequency",
                    warning_threshold=120.0,  # 2 minutes
                    critical_threshold=300.0,  # 5 minutes
                    unit="seconds",
                    description="Heartbeat frequency threshold",
                ),
                HealthThreshold(
                    "contract_success_rate",
                    warning_threshold=85.0,  # 85%
                    critical_threshold=70.0,  # 70%
                    unit="%",
                    description="Contract success rate threshold",
                ),
                HealthThreshold(
                    "communication_latency",
                    warning_threshold=500.0,  # 500ms
                    critical_threshold=2000.0,  # 2 seconds
                    unit="ms",
                    description="Communication latency threshold",
                ),
            ]

            for threshold in default_thresholds:
                self.thresholds[threshold.metric_type] = threshold
            
            # Record configuration change
            config_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "initialize_default_thresholds",
                "thresholds_count": len(default_thresholds),
                "success": True
            }
            self.configuration_changes.append(config_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("initialize_default_thresholds", True, operation_time)
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default thresholds: {e}")
            self.record_operation("initialize_default_thresholds", False, 0.0)

    def set_threshold(
        self,
        metric_type: str,
        warning_threshold: float,
        critical_threshold: float,
        unit: str,
        description: str,
    ):
        """Set custom health threshold for a metric type"""
        try:
            start_time = datetime.now()
            
            threshold = HealthThreshold(
                metric_type=metric_type,
                warning_threshold=warning_threshold,
                critical_threshold=critical_threshold,
                unit=unit,
                description=description,
            )

            self.thresholds[metric_type] = threshold
            
            # Record threshold operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "set_threshold",
                "metric_type": metric_type,
                "warning_threshold": warning_threshold,
                "critical_threshold": critical_threshold,
                "unit": unit,
                "success": True
            }
            self.threshold_operations.append(operation_record)
            
            # Record configuration change
            config_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "set_threshold",
                "metric_type": metric_type,
                "success": True
            }
            self.configuration_changes.append(config_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("set_threshold", True, operation_time)
            
            self.logger.info(f"Health threshold updated for {metric_type}")
            
        except Exception as e:
            self.logger.error(f"Failed to set threshold for {metric_type}: {e}")
            self.record_operation("set_threshold", False, 0.0)

    def get_threshold(self, metric_type: str) -> Optional[HealthThreshold]:
        """Get health threshold for a specific metric type"""
        try:
            threshold = self.thresholds.get(metric_type)
            
            # Record operation
            self.record_operation("get_threshold", threshold is not None, 0.0)
            
            return threshold
            
        except Exception as e:
            self.logger.error(f"Failed to get threshold for {metric_type}: {e}")
            self.record_operation("get_threshold", False, 0.0)
            return None

    def get_all_thresholds(self) -> Dict[str, HealthThreshold]:
        """Get all health thresholds"""
        try:
            thresholds = self.thresholds.copy()
            
            # Record operation
            self.record_operation("get_all_thresholds", True, 0.0)
            
            return thresholds
            
        except Exception as e:
            self.logger.error(f"Failed to get all thresholds: {e}")
            self.record_operation("get_all_thresholds", False, 0.0)
            return {}

    def remove_threshold(self, metric_type: str):
        """Remove a health threshold"""
        try:
            start_time = datetime.now()
            
            if metric_type in self.thresholds:
                del self.thresholds[metric_type]
                
                # Record threshold operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "remove_threshold",
                    "metric_type": metric_type,
                    "success": True
                }
                self.threshold_operations.append(operation_record)
                
                # Record configuration change
                config_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "remove_threshold",
                    "metric_type": metric_type,
                    "success": True
                }
                self.configuration_changes.append(config_record)
                
                # Record operation
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("remove_threshold", True, operation_time)
                
                self.logger.info(f"Health threshold removed for {metric_type}")
            else:
                self.record_operation("remove_threshold", False, 0.0)
                
        except Exception as e:
            self.logger.error(f"Failed to remove threshold for {metric_type}: {e}")
            self.record_operation("remove_threshold", False, 0.0)

    def has_threshold(self, metric_type: str) -> bool:
        """Check if a threshold exists for a metric type"""
        try:
            has_threshold = metric_type in self.thresholds
            
            # Record operation
            self.record_operation("has_threshold", True, 0.0)
            
            return has_threshold
            
        except Exception as e:
            self.logger.error(f"Failed to check threshold existence for {metric_type}: {e}")
            self.record_operation("has_threshold", False, 0.0)
            return False

    def get_threshold_count(self) -> int:
        """Get the total number of thresholds"""
        try:
            count = len(self.thresholds)
            
            # Record operation
            self.record_operation("get_threshold_count", True, 0.0)
            
            return count
            
        except Exception as e:
            self.logger.error(f"Failed to get threshold count: {e}")
            self.record_operation("get_threshold_count", False, 0.0)
            return 0

    def validate_threshold(self, metric_type: str, value: float) -> str:
        """Validate a metric value against its threshold"""
        try:
            start_time = datetime.now()
            
            threshold = self.get_threshold(metric_type)
            if not threshold:
                self.record_operation("validate_threshold", False, 0.0)
                return "unknown"

            if value >= threshold.critical_threshold:
                status = "critical"
            elif value >= threshold.warning_threshold:
                status = "warning"
            else:
                status = "good"
            
            # Record validation operation
            validation_record = {
                "timestamp": datetime.now().isoformat(),
                "metric_type": metric_type,
                "value": value,
                "status": status,
                "threshold": {
                    "warning": threshold.warning_threshold,
                    "critical": threshold.critical_threshold,
                    "unit": threshold.unit
                }
            }
            self.validation_operations.append(validation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("validate_threshold", True, operation_time)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to validate threshold for {metric_type}: {e}")
            self.record_operation("validate_threshold", False, 0.0)
            return "unknown"

    def get_threshold_summary(self) -> Dict[str, Dict[str, float]]:
        """Get a summary of all thresholds"""
        try:
            start_time = datetime.now()
            
            summary = {}
            for metric_type, threshold in self.thresholds.items():
                summary[metric_type] = {
                    "warning": threshold.warning_threshold,
                    "critical": threshold.critical_threshold,
                    "unit": threshold.unit,
                }
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("get_threshold_summary", True, operation_time)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get threshold summary: {e}")
            self.record_operation("get_threshold_summary", False, 0.0)
            return {}

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            start_time = datetime.now()
            
            self.logger.info("Running HealthThresholdManager smoke test...")

            # Test basic initialization
            assert len(self.thresholds) > 0
            assert self.get_threshold_count() > 0
            self.logger.info("Basic initialization passed")

            # Test default thresholds
            response_threshold = self.get_threshold("response_time")
            assert response_threshold is not None
            assert response_threshold.unit == "ms"
            assert response_threshold.warning_threshold == 1000.0
            self.logger.info("Default thresholds passed")

            # Test custom threshold
            self.set_threshold(
                "custom_metric",
                warning_threshold=50.0,
                critical_threshold=100.0,
                unit="count",
                description="Custom metric threshold",
            )

            custom_threshold = self.get_threshold("custom_metric")
            assert custom_threshold is not None
            assert custom_threshold.warning_threshold == 50.0
            assert custom_threshold.critical_threshold == 100.0
            self.logger.info("Custom threshold passed")

            # Test threshold validation
            assert self.validate_threshold("response_time", 500.0) == "good"
            assert self.validate_threshold("response_time", 1500.0) == "warning"
            assert self.validate_threshold("response_time", 6000.0) == "critical"
            self.logger.info("Threshold validation passed")

            # Test threshold summary
            summary = self.get_threshold_summary()
            assert "response_time" in summary
            assert "custom_metric" in summary
            self.logger.info("Threshold summary passed")

            # Test threshold removal
            self.remove_threshold("custom_metric")
            assert not self.has_threshold("custom_metric")
            self.logger.info("Threshold removal passed")

            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("run_smoke_test", True, operation_time)
            
            self.logger.info("✅ HealthThresholdManager smoke test PASSED")
            return True

        except Exception as e:
            self.logger.error(f"❌ HealthThresholdManager smoke test FAILED: {e}")
            self.record_operation("run_smoke_test", False, 0.0)
            import traceback

            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_health_threshold_management_data(self):
        """Save health threshold management data to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            persistence_dir = Path("data/persistent/health_thresholds")
            persistence_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for persistence
            threshold_data = {
                "thresholds": {k: v.__dict__ for k, v in self.thresholds.items()},
                "threshold_operations": self.threshold_operations,
                "validation_operations": self.validation_operations,
                "configuration_changes": self.configuration_changes,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0"
            }
            
            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_thresholds_data_{timestamp}.json"
            filepath = persistence_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(threshold_data, f, indent=2, default=str)
            
            # Keep only the latest 5 backup files
            self._cleanup_old_backups(persistence_dir, "health_thresholds_data_*.json", 5)
            
            self.logger.info(f"Health threshold management data saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save health threshold management data: {e}")
            # Fallback to basic logging if persistence fails
            self.logger.warning("Persistence failed, data only logged in memory")
    
    def _cleanup_old_backups(self, directory: Path, pattern: str, keep_count: int):
        """Clean up old backup files, keeping only the specified number"""
        try:
            files = list(directory.glob(pattern))
            if len(files) > keep_count:
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x.stat().st_mtime)
                # Remove oldest files
                for old_file in files[:-keep_count]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")
    
    def _check_health_threshold_management_health(self):
        """Check health threshold management health status"""
        try:
            # Check for excessive threshold operations
            if len(self.threshold_operations) > 1000:
                self.logger.warning(f"High number of threshold operations: {len(self.threshold_operations)}")
            
            # Check validation operations
            if len(self.validation_operations) > 500:
                self.logger.info(f"Large validation history: {len(self.validation_operations)} records")
                
        except Exception as e:
            self.logger.error(f"Failed to check health threshold management health: {e}")
    
    def get_health_threshold_management_stats(self) -> Dict[str, Any]:
        """Get health threshold management statistics"""
        try:
            stats = {
                "total_thresholds": len(self.thresholds),
                "threshold_operations_count": len(self.threshold_operations),
                "validation_operations_count": len(self.validation_operations),
                "configuration_changes_count": len(self.configuration_changes),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_health_threshold_management_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get health threshold management stats: {e}")
            self.record_operation("get_health_threshold_management_stats", False, 0.0)
            return {"error": str(e)}


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Threshold Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")

    args = parser.parse_args()

    if args.test:
        manager = HealthThresholdManager()
        success = manager.run_smoke_test()
        exit(0 if success else 1)

    elif args.demo:
        print("🚀 Starting Health Threshold Manager Demo...")
        manager = HealthThresholdManager()

        # Show default thresholds
        print(f"\n📊 Default Thresholds ({manager.get_threshold_count()} total):")
        for metric_type, threshold in manager.thresholds.items():
            print(
                f"  {metric_type}: {threshold.warning_threshold}{threshold.unit} (warning) / {threshold.critical_threshold}{threshold.unit} (critical)"
            )

        # Add custom threshold
        print("\n⚙️ Adding custom threshold...")
        manager.set_threshold("custom_metric", 50.0, 100.0, "count", "Custom metric")

        # Test validation
        print("\n🧪 Testing threshold validation:")
        test_values = [25.0, 75.0, 125.0]
        for value in test_values:
            status = manager.validate_threshold("custom_metric", value)
            print(f"  Value {value}: {status}")

        # Show summary
        print("\n📋 Threshold Summary:")
        summary = manager.get_threshold_summary()
        for metric, details in summary.items():
            print(
                f"  {metric}: {details['warning']}{details['unit']} / {details['critical']}{details['unit']}"
            )

        print("\n✅ Demo completed")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
