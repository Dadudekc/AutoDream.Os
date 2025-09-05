"""
Integration Monitor - V2 Compliance Refactored
===============================================

V2 compliant integration monitoring using specialized components.
REFACTORED: 313 lines → <100 lines for V2 compliance.

Responsibilities:
- Orchestrates specialized monitoring components
- Provides unified interface for monitoring operations
- Maintains backward compatibility

V2 Compliance: Modular architecture, <300 lines, single responsibility.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Refactoring
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from .models import (
    IntegrationType, IntegrationMetrics, IntegrationStatus,
    IntegrationConfig, IntegrationModels
)

# Import specialized monitoring components
from .monitors import (
    MetricsCollector,
    AlertManager,
    MonitoringThread
)


class IntegrationMonitor:
    """
    V2 Compliant Integration Monitor.
    
    Uses specialized components to provide monitoring capabilities
    while maintaining clean, focused architecture.
    """
    
    def __init__(self, config: IntegrationConfig):
        """Initialize integration monitor with specialized components."""
        self.config = config
        
        # Initialize specialized components
        self.metrics_collector = MetricsCollector(config.monitoring_config)
        self.alert_manager = AlertManager(config.monitoring_config)
        self.monitoring_thread = MonitoringThread(
            self.metrics_collector, 
            self.alert_manager, 
            config.monitoring_config
        )
        
    def start_monitoring(self) -> None:
        """Start monitoring system."""
        self.monitoring_thread.start_monitoring()
    
    def stop_monitoring(self) -> None:
        """Stop monitoring system."""
        self.monitoring_thread.stop_monitoring()
    
    def add_callback(self, callback: Callable) -> None:
        """Add monitoring callback."""
        self.alert_manager.add_callback(callback)
    
    def remove_callback(self, callback: Callable) -> None:
        """Remove monitoring callback."""
        self.alert_manager.remove_callback(callback)
    
    def record_request(self, integration_type: IntegrationType, 
                      success: bool, response_time: float) -> None:
        """Record integration request metrics."""
        self.metrics_collector.update_metrics(integration_type, success, response_time)
    
    def get_metrics(self, integration_type: IntegrationType) -> IntegrationMetrics:
        """Get metrics for specific integration type."""
        return self.metrics_collector.get_metrics(integration_type)
    
    def get_all_metrics(self) -> Dict[IntegrationType, IntegrationMetrics]:
        """Get all integration metrics."""
        return self.metrics_collector.get_all_metrics()
    
    def is_monitoring_active(self) -> bool:
        """Check if monitoring is active."""
        return self.monitoring_thread.is_monitoring_active()
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get comprehensive monitoring status."""
        try:
            return {
                "monitoring": self.monitoring_thread.get_monitoring_status(),
                "alerts": self.alert_manager.get_alert_status(),
                "metrics_count": len(self.metrics_collector.get_all_metrics()),
                "components_initialized": {
                    "metrics_collector": self.metrics_collector is not None,
                    "alert_manager": self.alert_manager is not None,
                    "monitoring_thread": self.monitoring_thread is not None
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def cleanup(self) -> None:
        """Cleanup monitoring resources."""
        try:
            self.monitoring_thread.cleanup()
            self.alert_manager.cleanup()
            self.metrics_collector.cleanup()
        except Exception as e:
            print(f"Integration monitor cleanup failed: {e}")


# Factory function for backward compatibility
def create_integration_monitor(config: IntegrationConfig) -> IntegrationMonitor:
    """Create an integration monitor instance."""
    return IntegrationMonitor(config)
