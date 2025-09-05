"""
Deployment Models - V2 Compliant Module
======================================

Main models for deployment operations.
Coordinates all model components and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .enums import DeploymentStatus, PatternType, DeploymentPriority
from .data_models import MassDeploymentTarget, MaximumEfficiencyDeploymentStatus, DeploymentMetrics
from .config_models import DeploymentConfig
from .factory_functions import (
    create_default_config, create_deployment_target, create_deployment_status,
    create_deployment_metrics, create_deployment_target_from_pattern,
    create_batch_deployment_targets, create_deployment_status_for_agent,
    create_custom_config, get_agent_domain, get_priority_for_pattern,
    get_all_agent_domains, get_all_pattern_priorities
)
from .validation_functions import (
    validate_deployment_target, validate_deployment_status, validate_deployment_config,
    validate_deployment_metrics, validate_file_path, validate_pattern_type,
    validate_priority, validate_status, validate_agent_id, validate_efficiency_score,
    validate_deployment_timeout, validate_concurrent_deployments, validate_retry_attempts,
    validate_deployment_batch, validate_deployment_configuration
)


# Re-export all models for backward compatibility
__all__ = [
    'DeploymentStatus', 'PatternType', 'DeploymentPriority',
    'MassDeploymentTarget', 'MaximumEfficiencyDeploymentStatus',
    'DeploymentConfig', 'DeploymentMetrics',
    'create_default_config', 'create_deployment_target',
    'create_deployment_status', 'create_deployment_metrics',
    'validate_deployment_target', 'validate_deployment_status', 'validate_deployment_config'
]


# Additional utility functions
def get_deployment_summary(targets: List[MassDeploymentTarget]) -> Dict[str, Any]:
    """Get summary of deployment targets."""
    if not targets:
        return {"total": 0, "by_status": {}, "by_priority": {}, "by_type": {}}
    
    summary = {
        "total": len(targets),
        "by_status": {},
        "by_priority": {},
        "by_type": {}
    }
    
    for target in targets:
        # Count by status
        status = target.status
        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        
        # Count by priority
        priority = target.priority
        summary["by_priority"][priority] = summary["by_priority"].get(priority, 0) + 1
        
        # Count by type
        pattern_type = target.pattern_type
        summary["by_type"][pattern_type] = summary["by_type"].get(pattern_type, 0) + 1
    
    return summary


def get_deployment_health_status(status: MaximumEfficiencyDeploymentStatus) -> Dict[str, Any]:
    """Get health status of deployment."""
    efficiency_score = status.calculate_efficiency_score()
    
    if efficiency_score >= 0.9:
        health_level = "excellent"
    elif efficiency_score >= 0.7:
        health_level = "good"
    elif efficiency_score >= 0.5:
        health_level = "fair"
    else:
        health_level = "poor"
    
    return {
        "health_level": health_level,
        "efficiency_score": efficiency_score,
        "total_deployments": (
            status.logging_files_deployed +
            status.manager_patterns_consolidated +
            status.config_patterns_integrated
        ),
        "error_count": len(status.deployment_errors),
        "last_attempt": status.last_deployment_attempt
    }


def get_deployment_metrics_summary(metrics: DeploymentMetrics) -> Dict[str, Any]:
    """Get summary of deployment metrics."""
    if metrics.total_deployments == 0:
        return {
            "total_deployments": 0,
            "success_rate": 0.0,
            "average_time": 0.0,
            "efficiency_score": 0.0
        }
    
    success_rate = metrics.successful_deployments / metrics.total_deployments
    efficiency_score = metrics.calculate_efficiency_score()
    
    return {
        "total_deployments": metrics.total_deployments,
        "successful_deployments": metrics.successful_deployments,
        "failed_deployments": metrics.failed_deployments,
        "skipped_deployments": metrics.skipped_deployments,
        "success_rate": success_rate,
        "average_time": metrics.average_deployment_time,
        "total_time": metrics.total_deployment_time,
        "efficiency_score": efficiency_score
    }
