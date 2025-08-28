#!/usr/bin/env python3
"""
⚖️ Health Threshold Manager - Agent_Cellphone_V2

REFACTORED component using extracted services for better SRP compliance.
Reduced from 694 lines to ~300 lines while maintaining all functionality.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

import logging
from typing import Dict, Optional, List, Any

from core.base_manager import BaseManager
from core.health.models import HealthThreshold
from core.health.operations import HealthThresholdOperations
from core.health.validation import HealthThresholdValidation
from core.health.persistence import HealthThresholdPersistence
from core.health.defaults import HealthThresholdDefaults
from core.health.testing import HealthThresholdTesting
from core.health_base.monitoring import HealthThresholdMonitoring

# Configure logging
logger = logging.getLogger(__name__)


class HealthThresholdManager(BaseManager):
    """
    REFACTORED Health Threshold Manager - Single responsibility: Manage health thresholds and configurations.
    
    Uses extracted services for operations, validation, persistence, and monitoring.
    Follows V2 standards: ~300 LOC, OOP design, SRP compliance.
    """

    def __init__(self):
        """Initialize the threshold manager with BaseManager and extracted services"""
        super().__init__(
            manager_id="health_threshold_manager",
            name="Health Threshold Manager",
            description="Manage health thresholds and configurations"
        )
        
        # Initialize extracted services
        self.operations = HealthThresholdOperations(self.logger)
        self.validation = HealthThresholdValidation(self.logger)
        self.persistence = HealthThresholdPersistence(self.logger)
        self.testing = HealthThresholdTesting(self.logger)
        self.monitoring = HealthThresholdMonitoring(self.logger)
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
        self.logger.info("HealthThresholdManager initialized with extracted services")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize health threshold management system"""
        try:
            self.logger.info("Starting Health Threshold Manager...")
            
            # Clear tracking data
            self.operations.clear_operations()
            self.validation.clear_validation_history()
            
            # Verify thresholds are loaded
            if not self.operations.thresholds:
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
            
            # Save data to persistent storage
            self._save_health_threshold_management_data()
            
            # Clear data
            self.operations.clear_operations()
            self.validation.clear_validation_history()
            
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
            self.operations.clear_operations()
            self.validation.clear_validation_history()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup health threshold management resources"""
        try:
            # Clear data
            self.operations.clear_operations()
            self.validation.clear_validation_history()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reload default thresholds
            self._initialize_default_thresholds()
            
            # Reset tracking
            self.operations.clear_operations()
            self.validation.clear_validation_history()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Health Threshold Management Methods - Delegated to Services
    # ============================================================================
    
    def _initialize_default_thresholds(self):
        """Initialize default health thresholds using defaults service"""
        try:
            default_thresholds = HealthThresholdDefaults.get_default_thresholds()
            
            for threshold in default_thresholds:
                self.operations.thresholds[threshold.metric_type] = threshold
            
            self.logger.info(f"Initialized {len(default_thresholds)} default thresholds")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default thresholds: {e}")

    def set_threshold(
        self,
        metric_type: str,
        warning_threshold: float,
        critical_threshold: float,
        unit: str,
        description: str,
    ):
        """Set custom health threshold for a metric type"""
        return self.operations.set_threshold(
            metric_type, warning_threshold, critical_threshold, unit, description
        )

    def get_threshold(self, metric_type: str) -> Optional[HealthThreshold]:
        """Get health threshold for a specific metric type"""
        return self.operations.get_threshold(metric_type)

    def get_all_thresholds(self) -> Dict[str, HealthThreshold]:
        """Get all health thresholds"""
        return self.operations.get_all_thresholds()

    def remove_threshold(self, metric_type: str):
        """Remove a health threshold"""
        return self.operations.remove_threshold(metric_type)

    def has_threshold(self, metric_type: str) -> bool:
        """Check if a threshold exists for a metric type"""
        return self.operations.has_threshold(metric_type)

    def get_threshold_count(self) -> int:
        """Get the total number of thresholds"""
        return self.operations.get_threshold_count()

    def validate_threshold(self, metric_type: str, value: float) -> str:
        """Validate a metric value against its threshold"""
        threshold = self.get_threshold(metric_type)
        if not threshold:
            return "unknown"
        
        return self.validation.validate_threshold(threshold, value)

    def get_threshold_summary(self) -> Dict[str, Dict[str, float]]:
        """Get a summary of all thresholds"""
        return self.operations.get_threshold_summary()

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        return self.testing.run_smoke_test(
            self.get_threshold_count,
            self.get_threshold,
            self.set_threshold,
            self.has_threshold,
            self.remove_threshold,
            self.validate_threshold,
            self.get_threshold_summary
        )
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_health_threshold_management_data(self):
        """Save health threshold management data to persistent storage"""
        try:
            success = self.persistence.save_data(
                thresholds=self.operations.thresholds,
                threshold_operations=self.operations.threshold_operations,
                validation_operations=self.validation.validation_operations,
                configuration_changes=self.operations.configuration_changes,
                manager_id=self.manager_id
            )
            
            if success:
                self.logger.info("Health threshold management data saved successfully")
            else:
                self.logger.warning("Failed to save health threshold management data")
                
        except Exception as e:
            self.logger.error(f"Failed to save health threshold management data: {e}")
    
    def _check_health_threshold_management_health(self):
        """Check health threshold management health status"""
        try:
            stats = self.operations.get_operations_stats()
            validation_stats = self.validation.get_validation_stats()
            
            health_status = self.monitoring.check_health_status(
                stats.get("threshold_operations_count", 0),
                validation_stats.get("total_validations", 0),
                stats.get("configuration_changes_count", 0)
            )
            
            if health_status["status"] != "healthy":
                self.logger.warning(f"Health status: {health_status['status']}")
                for warning in health_status.get("warnings", []):
                    self.logger.warning(warning)
                    
        except Exception as e:
            self.logger.error(f"Failed to check health threshold management health: {e}")
    
    def get_health_threshold_management_stats(self) -> Dict[str, Any]:
        """Get health threshold management statistics"""
        try:
            stats = self.operations.get_operations_stats()
            validation_stats = self.validation.get_validation_stats()
            
            return self.monitoring.get_health_summary(
                total_thresholds=self.get_threshold_count(),
                threshold_operations_count=stats.get("threshold_operations_count", 0),
                validation_operations_count=validation_stats.get("total_validations", 0),
                configuration_changes_count=stats.get("configuration_changes_count", 0),
                manager_status=self.status.value,
                manager_uptime=self.metrics.uptime_seconds
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get health threshold management stats: {e}")
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
        for metric_type, threshold in manager.operations.thresholds.items():
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
