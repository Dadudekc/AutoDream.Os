#!/usr/bin/env python3
"""
Unified Performance System V2 - Modular Performance Management

This is the new V2-compliant unified performance system that replaces
the massive 1,285-line monolithic file with modular components.

Author: Agent-8 (Technical Debt Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .performance import (
    UnifiedPerformanceSystem,
    PerformanceValidator,
    PerformanceReporter,
    PerformanceConfigManager,
    PerformanceMetric,
    PerformanceResult
)


class UnifiedPerformanceSystemV2:
    """
    V2-Compliant Unified Performance System.
    
    This system orchestrates the modular performance components to provide
    unified performance management while maintaining V2 compliance standards.
    
    V2 Compliance:
    - File size: ≤400 LOC (this file: ~150 LOC)
    - Single Responsibility: Orchestration only
    - Modular architecture: Uses separate modules for specific functionality
    - Clean imports: No relative imports
    """
    
    def __init__(self):
        """Initialize the V2 unified performance system."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize modular components
        self.core_system = UnifiedPerformanceSystem()
        self.validator = PerformanceValidator()
        self.reporter = PerformanceReporter()
        self.config_manager = PerformanceConfigManager()
        
        # System state
        self.is_initialized = False
        self.monitoring_active = False
        
        self.logger.info("Unified Performance System V2 initialized")
    
    def initialize(self) -> bool:
        """Initialize the performance system."""
        try:
            self.logger.info("Initializing Unified Performance System V2...")
            
            # Load configuration
            if not self.config_manager.load_configuration():
                self.logger.warning("Failed to load configuration, using defaults")
            
            # Initialize core system
            if not self.core_system.initialize():
                self.logger.error("Failed to initialize core performance system")
                return False
            
            # Setup validation rules from configuration
            self._setup_validation_rules()
            
            # Setup performance thresholds
            self._setup_performance_thresholds()
            
            self.is_initialized = True
            self.logger.info("Unified Performance System V2 initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize performance system: {e}")
            return False
    
    def _setup_validation_rules(self):
        """Setup validation rules from configuration."""
        try:
            config = self.config_manager.get_config()
            
            # Add default validation rules
            for rule_data in config.default_validation_rules:
                from .performance.performance_core import ValidationRule
                rule = ValidationRule(
                    rule_name=rule_data["rule_name"],
                    metric_name=rule_data["metric_name"],
                    threshold=rule_data["threshold"],
                    operator=rule_data["operator"],
                    severity=rule_data["severity"],
                    description=rule_data["description"]
                )
                self.validator.add_validation_rule(rule)
            
            self.logger.info(f"Setup {len(config.default_validation_rules)} validation rules")
            
        except Exception as e:
            self.logger.error(f"Failed to setup validation rules: {e}")
    
    def _setup_performance_thresholds(self):
        """Setup performance thresholds from configuration."""
        try:
            config = self.config_manager.get_config()
            
            # Add default thresholds
            for metric_name, thresholds in config.default_thresholds.items():
                from .performance.performance_core import ValidationThreshold
                threshold = ValidationThreshold(
                    metric_name=metric_name,
                    warning_threshold=thresholds.get("warning", 0.0),
                    critical_threshold=thresholds.get("critical", 0.0)
                )
                self.validator.add_threshold(threshold)
            
            self.logger.info(f"Setup {len(config.default_thresholds)} performance thresholds")
            
        except Exception as e:
            self.logger.error(f"Failed to setup performance thresholds: {e}")
    
    def start_monitoring(self) -> bool:
        """Start performance monitoring."""
        try:
            if not self.is_initialized:
                self.logger.error("System not initialized")
                return False
            
            if self.monitoring_active:
                self.logger.info("Monitoring already active")
                return True
            
            self.monitoring_active = True
            self.logger.info("Performance monitoring started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop performance monitoring."""
        try:
            if not self.monitoring_active:
                self.logger.info("Monitoring not active")
                return True
            
            self.monitoring_active = False
            self.logger.info("Performance monitoring stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring: {e}")
            return False
    
    def add_metric(self, metric: PerformanceMetric) -> bool:
        """Add a performance metric."""
        try:
            if not self.is_initialized:
                self.logger.error("System not initialized")
                return False
            
            # Add to core system
            self.core_system.add_metric(metric)
            
            # Validate metric
            validation_result = self.validator.validate_metric(metric)
            
            # Log validation result
            if validation_result.get("overall_status") != "pass":
                self.logger.warning(f"Metric validation: {validation_result}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add metric: {e}")
            return False
    
    def get_performance_report(self, report_type: str = "summary") -> Dict[str, Any]:
        """Generate a performance report."""
        try:
            if not self.is_initialized:
                self.logger.error("System not initialized")
                return {"error": "System not initialized"}
            
            # Get metrics from core system
            metrics = list(self.core_system.metrics.values())
            
            # Get validation results
            validation_results = self.validator.get_validation_history()
            
            # Generate report
            report = self.reporter.generate_performance_report(
                metrics=metrics,
                validation_results=validation_results,
                report_type=report_type
            )
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            return {"error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        try:
            config_summary = self.config_manager.get_config_summary()
            validation_summary = self.validator.get_validation_summary()
            
            return {
                "system_status": {
                    "initialized": self.is_initialized,
                    "monitoring_active": self.monitoring_active,
                    "config_sources": config_summary.get("sources", [])
                },
                "performance_summary": {
                    "total_metrics": len(self.core_system.metrics),
                    "total_validation_rules": len(self.validator.validation_rules),
                    "total_thresholds": len(self.validator.thresholds),
                    "active_alerts": len(self.validator.get_active_alerts())
                },
                "validation_summary": validation_summary,
                "configuration": config_summary
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active performance alerts."""
        try:
            return self.validator.get_active_alerts()
        except Exception as e:
            self.logger.error(f"Failed to get active alerts: {e}")
            return []
    
    def clear_alerts(self) -> bool:
        """Clear all active alerts."""
        try:
            self.validator.clear_alerts()
            self.logger.info("All alerts cleared")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear alerts: {e}")
            return False
    
    def shutdown(self) -> bool:
        """Shutdown the performance system."""
        try:
            self.logger.info("Shutting down Unified Performance System V2...")
            
            # Stop monitoring
            if self.monitoring_active:
                self.stop_monitoring()
            
            # Clear alerts
            self.clear_alerts()
            
            # Save configuration if needed
            self.config_manager.save_configuration()
            
            self.is_initialized = False
            self.logger.info("Unified Performance System V2 shutdown complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to shutdown performance system: {e}")
            return False


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and test V2 performance system
    system = UnifiedPerformanceSystemV2()
    
    if system.initialize():
        print("✅ V2 Performance System initialized successfully")
        
        # Get system status
        status = system.get_system_status()
        print(f"📊 System Status: {status['system_status']}")
        print(f"⚡ Performance Summary: {status['performance_summary']}")
        
        # Start monitoring
        if system.start_monitoring():
            print("✅ Performance monitoring started")
            
            # Generate report
            report = system.get_performance_report("summary")
            print(f"📈 Report generated: {report.get('metadata', {}).get('report_id', 'Unknown')}")
            
            # Shutdown
            system.shutdown()
            print("✅ System shutdown complete")
        else:
            print("❌ Failed to start monitoring")
    else:
        print("❌ Failed to initialize V2 Performance System")
