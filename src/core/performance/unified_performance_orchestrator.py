#!/usr/bin/env python3
"""
Unified Performance Orchestrator - Performance System Coordination
===============================================================

Orchestrates all performance components using extracted modules.
Legacy methods are supplied via ``OrchestratorCompatibilityMixin`` to keep the
core orchestrator focused and within V2 standards (≤400 LOC, SRP, OOP).

Author: Agent-1 (Phase 3 Modularization)
License: MIT
"""

import logging
import warnings
from typing import Any, Dict, List, Optional

from .orchestrator_compat import OrchestratorCompatibilityMixin
from .performance_core import PerformanceCore
from .performance_models import (
    BenchmarkResult,
    SystemPerformanceReport,
    ValidationRule,
    ValidationThreshold,
)


class UnifiedPerformanceOrchestrator(OrchestratorCompatibilityMixin):
    """Orchestrates performance system using extracted modules."""

    def __init__(self, **core_kwargs: Any):
        """Initialize the orchestrator and forward parameters to ``PerformanceCore``.

        Any keyword arguments supplied are passed through to the underlying
        :class:`PerformanceCore`, allowing callers to customise the core while
        keeping this interface stable.
        """
        self.logger = logging.getLogger(f"{__name__}.UnifiedPerformanceOrchestrator")

        core_defaults = {
            "manager_id": "unified_performance_orchestrator",
            "name": "Unified Performance Orchestrator",
            "description": "Coordinates all performance system components",
        }
        core_defaults.update(core_kwargs)

        # Initialize performance core with forwarded parameters
        self.performance_core = PerformanceCore(**core_defaults)

        # Combined statistics
        self.orchestrator_stats = {
            "core_stats": {},
            "monitoring_stats": {},
            "validation_stats": {},
            "benchmarking_stats": {},
            "reporting_stats": {}
        }

        self.logger.info("Unified Performance Orchestrator initialized")
    
    def start_system(self) -> bool:
        """Start the unified performance system"""
        try:
            # Start performance core
            success = self.performance_core.start()
            if success:
                self.logger.info("✅ Unified Performance System started successfully")
                return True
            else:
                self.logger.error("Failed to start performance core")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to start unified performance system: {e}")
            return False
    
    def stop_system(self) -> bool:
        """Stop the unified performance system"""
        try:
            # Stop performance core
            success = self.performance_core.stop()
            if success:
                self.logger.info("✅ Unified Performance System stopped successfully")
                return True
            else:
                self.logger.error("Failed to stop performance core")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to stop unified performance system: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        try:
            core_status = self.performance_core.get_status()
            monitoring_status = self.performance_core.monitoring_manager.get_monitoring_status()
            validation_status = self.performance_core.validation_manager.get_validation_status()
            benchmarking_status = self.performance_core.benchmarking_manager.get_benchmark_status()
            reporting_status = self.performance_core.reporting_manager.get_reporting_status()
            
            return {
                "system_active": core_status.get("status") == "RUNNING",
                "core_status": core_status,
                "monitoring_status": monitoring_status,
                "validation_status": validation_status,
                "benchmarking_status": benchmarking_status,
                "reporting_status": reporting_status,
                "overall_health": self._calculate_overall_health(
                    core_status, monitoring_status, validation_status, 
                    benchmarking_status, reporting_status
                )
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}
    
    def _calculate_overall_health(self, *status_dicts) -> str:
        """Calculate overall system health"""
        try:
            # Check if all components are active
            active_components = 0
            total_components = len(status_dicts)
            
            for status in status_dicts:
                if status.get("status") == "RUNNING" or status.get("monitoring_active") or \
                   status.get("validation_active") or status.get("benchmarking_active") or \
                   status.get("reporting_active"):
                    active_components += 1
            
            health_percentage = (active_components / total_components) * 100 if total_components > 0 else 0
            
            if health_percentage >= 90:
                return "excellent"
            elif health_percentage >= 75:
                return "good"
            elif health_percentage >= 50:
                return "fair"
            else:
                return "poor"
                
        except Exception as e:
            self.logger.error(f"Failed to calculate overall health: {e}")
            return "unknown"
    
    def run_performance_benchmark(self, benchmark_type: str, parameters: Optional[Dict[str, Any]] = None) -> BenchmarkResult:
        """Run a performance benchmark"""
        try:
            return self.performance_core.run_benchmark(benchmark_type, parameters)
        except Exception as e:
            self.logger.error(f"Failed to run benchmark: {e}")
            raise
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            return self.performance_core.get_performance_summary()
        except Exception as e:
            self.logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}

    def add_custom_metric(
        self,
        name: str,
        value: float,
        unit: str,
        metric_type: str,
        labels: Dict[str, str],
        description: str
    ) -> bool:
        """Add a custom performance metric"""
        try:
            from .performance_models import MetricType
            metric_type_enum = MetricType(metric_type)
            
            return self.performance_core.monitoring_manager.add_custom_metric(
                name, value, unit, metric_type_enum, labels, description
            )
        except Exception as e:
            self.logger.error(f"Failed to add custom metric: {e}")
            return False
    
    def add_validation_rule(self, rule: ValidationRule) -> bool:
        """Add a validation rule"""
        try:
            return self.performance_core.validation_manager.add_validation_rule(rule)
        except Exception as e:
            self.logger.error(f"Failed to add validation rule: {e}")
            return False
    
    def remove_validation_rule(self, rule_name: str) -> bool:
        """Remove a validation rule"""
        try:
            return self.performance_core.validation_manager.remove_validation_rule(rule_name)
        except Exception as e:
            self.logger.error(f"Failed to remove validation rule: {e}")
            return False
    
    def add_threshold(self, threshold: ValidationThreshold) -> bool:
        """Add a performance threshold"""
        try:
            return self.performance_core.validation_manager.add_threshold(threshold)
        except Exception as e:
            self.logger.error(f"Failed to add threshold: {e}")
            return False
    
    def remove_threshold(self, metric_name: str) -> bool:
        """Remove a performance threshold"""
        try:
            return self.performance_core.validation_manager.remove_threshold(metric_name)
        except Exception as e:
            self.logger.error(f"Failed to remove threshold: {e}")
            return False
    
    def get_active_alerts(self) -> List[Any]:
        """Get active performance alerts"""
        try:
            return self.performance_core.validation_manager.get_active_alerts()
        except Exception as e:
            self.logger.error(f"Failed to get active alerts: {e}")
            return []
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge a performance alert"""
        try:
            return self.performance_core.validation_manager.acknowledge_alert(alert_id, acknowledged_by)
        except Exception as e:
            self.logger.error(f"Failed to acknowledge alert: {e}")
            return False
    
    def get_latest_performance_report(self) -> Optional[SystemPerformanceReport]:
        """Get the latest performance report"""
        try:
            return self.performance_core.reporting_manager.get_latest_report()
        except Exception as e:
            self.logger.error(f"Failed to get latest report: {e}")
            return None
    
    def export_performance_report(self, report_id: str, format: str = "json") -> Optional[str]:
        """Export a performance report"""
        try:
            return self.performance_core.reporting_manager.export_report(report_id, format)
        except Exception as e:
            self.logger.error(f"Failed to export report: {e}")
            return None
    
    def add_connection_pool(self, pool: Any) -> bool:
        """Add a connection pool to monitoring"""
        try:
            return self.performance_core.add_connection_pool(pool)
        except Exception as e:
            self.logger.error(f"Failed to add connection pool: {e}")
            return False
    
    def get_connection_pool_status(self, pool_name: str) -> Optional[Any]:
        """Get connection pool status"""
        try:
            return self.performance_core.get_connection_pool_status(pool_name)
        except Exception as e:
            self.logger.error(f"Failed to get connection pool status: {e}")
            return None
    
    def update_connection_pool(self, pool_name: str, updates: Dict[str, Any]) -> bool:
        """Update connection pool information"""
        try:
            return self.performance_core.update_connection_pool(pool_name, updates)
        except Exception as e:
            self.logger.error(f"Failed to update connection pool: {e}")
            return False
    
    def set_monitoring_interval(self, interval: float) -> bool:
        """Set monitoring interval"""
        try:
            return self.performance_core.monitoring_manager.set_monitoring_interval(interval)
        except Exception as e:
            self.logger.error(f"Failed to set monitoring interval: {e}")
            return False
    
    def get_benchmark_config(self, benchmark_type: str) -> Optional[Dict[str, Any]]:
        """Get benchmark configuration"""
        try:
            return self.performance_core.benchmarking_manager.get_benchmark_config(benchmark_type)
        except Exception as e:
            self.logger.error(f"Failed to get benchmark config: {e}")
            return None
    
    def set_benchmark_config(self, benchmark_type: str, config: Dict[str, Any]) -> bool:
        """Set benchmark configuration"""
        try:
            return self.performance_core.benchmarking_manager.set_benchmark_config(benchmark_type, config)
        except Exception as e:
            self.logger.error(f"Failed to set benchmark config: {e}")
            return False
    
    def run_smoke_test(self) -> bool:
        """Run a basic smoke test"""
        try:
            self.logger.info("Running unified performance system smoke test")
            
            # Test system startup
            if not self.start_system():
                self.logger.error("Smoke test failed: system startup")
                return False
            
            # Test basic operations
            try:
                # Test metric collection
                metrics = self.performance_core.monitoring_manager.collect_metrics()
                if not isinstance(metrics, list):
                    self.logger.error("Smoke test failed: metric collection")
                    return False
                
                # Test benchmark execution
                benchmark_result = self.run_performance_benchmark("cpu", {"duration": 5, "iterations": 100})
                if not benchmark_result.success:
                    self.logger.error("Smoke test failed: benchmark execution")
                    return False
                
                # Test report generation
                report = self.performance_core.reporting_manager.generate_performance_report(
                    metrics, [], [benchmark_result]
                )
                if not report:
                    self.logger.error("Smoke test failed: report generation")
                    return False
                
                self.logger.info("✅ Smoke test passed - all components working correctly")
                return True
                
            finally:
                # Always stop the system after testing
                self.stop_system()
                
        except Exception as e:
            self.logger.error(f"Smoke test failed with error: {e}")
            return False


# Backward compatibility - maintain existing interface
class UnifiedPerformanceSystem(UnifiedPerformanceOrchestrator):
    """Backward compatibility alias for existing code.

    This class will be removed in a future release. Use
    :class:`UnifiedPerformanceOrchestrator` directly instead.
    """

    def __init__(self, **kwargs: Any):
        warnings.warn(
            "UnifiedPerformanceSystem is deprecated; use UnifiedPerformanceOrchestrator",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(**kwargs)


def main():
    """Main entry point for testing"""
    orchestrator = UnifiedPerformanceOrchestrator()
    
    # Run smoke test
    if orchestrator.run_smoke_test():
        print("✅ Unified Performance System smoke test passed")
    else:
        print("❌ Unified Performance System smoke test failed")


if __name__ == "__main__":
    main()
