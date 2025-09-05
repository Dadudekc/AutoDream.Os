#!/usr/bin/env python3
"""
Deployment Package - V2 Compliance
==================================

Modular maximum efficiency mass deployment system with V2 compliance.
Replaces the monolithic maximum-efficiency-mass-deployment-coordinator.py.

Package Structure:
- deployment_models.py: Data models and configuration
- deployment_coordinator.py: Core deployment coordination and execution
- deployment_orchestrator.py: Main orchestrator and unified interface

V2 Compliance: Modular design, single responsibility, dependency injection.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import main classes for easy access
from .deployment_models import (
    DeploymentConfig,
    MassDeploymentTarget,
    MaximumEfficiencyDeploymentStatus,
    DeploymentMetrics,
    DeploymentStatus,
    PatternType,
    DeploymentPriority,
    create_default_config,
    create_deployment_target,
    create_deployment_status,
    create_deployment_metrics,
    DEFAULT_AGENT_DOMAINS,
    DEPLOYMENT_TARGET_PRIORITIES
)

from .deployment_coordinator import DeploymentCoordinator

from .deployment_orchestrator import (
    MaximumEfficiencyMassDeploymentOrchestrator,
    get_maximum_efficiency_coordinator,
    deploy_maximum_efficiency_mass_deployment_to_agent,
    deploy_maximum_efficiency_mass_deployment_to_all_targets,
    MaximumEfficiencyMassDeploymentCoordinator
)

# Package metadata
__version__ = "2.0.0"
__author__ = "Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"
__description__ = "Modular maximum efficiency mass deployment system with V2 compliance"

# Export main interface functions
__all__ = [
    # Core classes
    "MaximumEfficiencyMassDeploymentOrchestrator",
    "DeploymentCoordinator",
    
    # Data models
    "DeploymentConfig",
    "MassDeploymentTarget",
    "MaximumEfficiencyDeploymentStatus",
    "DeploymentMetrics",
    
    # Enums
    "DeploymentStatus",
    "PatternType",
    "DeploymentPriority",
    
    # Factory functions
    "create_default_config",
    "create_deployment_target",
    "create_deployment_status",
    "create_deployment_metrics",
    
    # Constants
    "DEFAULT_AGENT_DOMAINS",
    "DEPLOYMENT_TARGET_PRIORITIES",
    
    # Main interface functions
    "get_maximum_efficiency_coordinator",
    "deploy_maximum_efficiency_mass_deployment_to_agent",
    "deploy_maximum_efficiency_mass_deployment_to_all_targets",
    
    # Backward compatibility
    "MaximumEfficiencyMassDeploymentCoordinator"
]
