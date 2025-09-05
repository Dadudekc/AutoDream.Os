#!/usr/bin/env python3
"""
Deployment Coordinator - V2 Compliance Redirect
==============================================

V2 compliance redirect to modular deployment system.
Refactored from 393-line monolithic file into focused modules.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

# V2 COMPLIANCE REDIRECT - see coordinators package

from .coordinators.deployment_coordinator import DeploymentCoordinator
from .deployment_models import (
    MassDeploymentTarget, MaximumEfficiencyDeploymentStatus, DeploymentConfig,
    DeploymentMetrics, DeploymentStatus, PatternType, DeploymentPriority,
    create_deployment_target, create_deployment_status, create_deployment_metrics,
    create_default_config
)

# Re-export for backward compatibility
__all__ = [
    'DeploymentCoordinator',
    'MassDeploymentTarget',
    'MaximumEfficiencyDeploymentStatus', 
    'DeploymentConfig',
    'DeploymentMetrics',
    'DeploymentStatus',
    'PatternType',
    'DeploymentPriority',
    'create_deployment_target',
    'create_deployment_status',
    'create_deployment_metrics',
    'create_default_config'
]