"""
Messaging Coordinator
====================

Coordinates messaging integration optimization.
"""

from typing import Any, Dict, List, Optional
from ..integration_utilities.integration_interfaces import IIntegrationCoordinator
from ..integration_utilities.integration_models import IntegrationType, OptimizationConfig
from ..integration_engines.messaging_engine import MessagingEngine
from ..unified_logging_system import get_logger


class MessagingCoordinator(IIntegrationCoordinator):
    """Coordinates messaging integration optimization."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the messaging coordinator."""
        self.logger = get_logger(__name__)
        self.config = config or OptimizationConfig()
        self.engine = MessagingEngine()
        self.logger.info("Messaging Coordinator initialized")
    
    def get_unified_performance_report(self) -> Dict[str, Any]:
        """Get unified performance report for messaging integration."""
        report = self.engine.get_performance_report()
        return {
            "integration_type": "messaging",
            "performance_data": report,
            "optimization_status": {
                "messaging_optimization": self.config.enable_messaging_optimization,
                "auto_optimization": self.config.enable_auto_optimization
            }
        }
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get optimization recommendations for messaging."""
        recommendations = []
        report = self.engine.get_performance_report()
        
        if report.get("average_delivery_time", 0) > 0.5:
            recommendations.append({
                "integration": "messaging",
                "issue": "Slow delivery time",
                "current_value": f"{report.get('average_delivery_time', 0):.3f}s",
                "recommendation": "Enable batching and async delivery",
                "priority": "high"
            })
        
        if report.get("success_rate", 0) < 0.95:
            recommendations.append({
                "integration": "messaging",
                "issue": "Low success rate",
                "current_value": f"{report.get('success_rate', 0):.2%}",
                "recommendation": "Enable retry mechanism and error handling",
                "priority": "high"
            })
        
        return recommendations
    
    def optimize_integration(self, integration_type: IntegrationType, **kwargs) -> bool:
        """Optimize messaging integration."""
        if integration_type != IntegrationType.MESSAGING:
            self.logger.error(f"Invalid integration type for messaging coordinator: {integration_type}")
            return False
        
        return self.engine.optimize(**kwargs)
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current status of messaging integration."""
        return {
            "coordinator_type": "messaging",
            "status": "active",
            "engine_status": self.engine.get_status(),
            "optimization_enabled": self.config.enable_messaging_optimization
        }
