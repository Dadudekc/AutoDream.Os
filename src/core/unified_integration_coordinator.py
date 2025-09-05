#!/usr/bin/env python3
"""
Unified Integration Coordinator - Agent-8 V2 Compliance Refactoring
==================================================================

Unified coordinator for all core system integrations.
Provides centralized optimization, monitoring, and coordination.

V2 COMPLIANCE: Refactored into modular architecture
- Separated into engines, coordinators, and utilities
- Maintained backward compatibility
- Reduced file size from 415 lines to <300 lines

Author: Agent-8 (SSOT & System Integration Specialist)
Mission: V2 Compliance Refactoring
Status: ACTIVE - Modular Architecture Implementation
"""

# Backward compatibility imports - delegate to modular implementation
from .integration_coordinators.unified_integration_coordinator import (
    UnifiedIntegrationCoordinator as ModularUnifiedIntegrationCoordinator,
    get_unified_integration_coordinator,
    create_optimized_integration_service
)

# Re-export all public interfaces for backward compatibility
from .integration_utilities.integration_models import (
    IntegrationType,
    OptimizationLevel,
    IntegrationMetrics,
    OptimizationConfig
)

# Additional imports for backward compatibility
from typing import Optional
import json

# Legacy class for backward compatibility
class UnifiedIntegrationCoordinator:
    """
    Unified coordinator for all core system integrations.
    
    V2 COMPLIANCE: This is now a backward compatibility wrapper
    that delegates to the modular implementation.
    """
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the unified integration coordinator."""
        # Delegate to modular implementation
        self._coordinator = ModularUnifiedIntegrationCoordinator(config)
        
        # Expose all methods for backward compatibility
        self.get_unified_performance_report = self._coordinator.get_unified_performance_report
        self.get_optimization_recommendations = self._coordinator.get_optimization_recommendations
        self.optimize_integration = self._coordinator.optimize_integration
        self.get_integration_status = self._coordinator.get_integration_status
        
        # Expose properties for backward compatibility
        self.config = self._coordinator.config
        self.metrics = self._coordinator.metrics
        self.performance_history = self._coordinator.performance_history


# ================================
# FACTORY FUNCTIONS (Delegated)
# ================================

# These functions are already imported from the modular implementation
# and will be used directly without redefinition


if __name__ == "__main__":
    # Example usage
    coordinator = get_unified_integration_coordinator()
    
    # Get unified performance report
    report = coordinator.get_unified_performance_report()
    print(f"Unified performance report: {json.dumps(report, indent=2)}")
    
    # Get optimization recommendations
    recommendations = coordinator.get_optimization_recommendations()
    print(f"Optimization recommendations: {json.dumps(recommendations, indent=2)}")
    
    # Get integration status
    status = coordinator.get_integration_status()
    print(f"Integration status: {json.dumps(status, indent=2)}")
