"""
Deployment Validation Functions - V2 Compliant Module
====================================================

Validation functions for deployment models.
Extracted from deployment_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .enums import DeploymentStatus, PatternType, DeploymentPriority
from .data_models import MassDeploymentTarget, MaximumEfficiencyDeploymentStatus, DeploymentMetrics
from .config_models import DeploymentConfig


def validate_deployment_target(target: MassDeploymentTarget) -> bool:
    """Validate deployment target."""
    try:
        target.__post_init__()
        return True
    except ValueError:
        return False


def validate_deployment_status(status: MaximumEfficiencyDeploymentStatus) -> bool:
    """Validate deployment status."""
    try:
        status.__post_init__()
        return True
    except ValueError:
        return False


def validate_deployment_config(config: DeploymentConfig) -> bool:
    """Validate deployment configuration."""
    return config.validate()


def validate_deployment_metrics(metrics: DeploymentMetrics) -> bool:
    """Validate deployment metrics."""
    try:
        if not isinstance(metrics.start_time, datetime):
            return False
        
        if metrics.end_time is not None and not isinstance(metrics.end_time, datetime):
            return False
        
        if metrics.total_deployments < 0:
            return False
        
        if metrics.successful_deployments < 0:
            return False
        
        if metrics.failed_deployments < 0:
            return False
        
        if metrics.skipped_deployments < 0:
            return False
        
        if metrics.average_deployment_time < 0:
            return False
        
        if metrics.total_deployment_time < 0:
            return False
        
        if not 0.0 <= metrics.efficiency_score <= 1.0:
            return False
        
        return True
        
    except (ValueError, TypeError):
        return False


def validate_file_path(file_path: str) -> bool:
    """Validate file path format."""
    if not file_path or not isinstance(file_path, str):
        return False
    
    # Basic validation - should not be empty and should be a string
    if len(file_path.strip()) == 0:
        return False
    
    # Should not contain invalid characters
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    if any(char in file_path for char in invalid_chars):
        return False
    
    return True


def validate_pattern_type(pattern_type: str) -> bool:
    """Validate pattern type."""
    valid_types = [pt.value for pt in PatternType]
    return pattern_type in valid_types


def validate_priority(priority: str) -> bool:
    """Validate priority level."""
    valid_priorities = [dp.value for dp in DeploymentPriority]
    return priority in valid_priorities


def validate_status(status: str) -> bool:
    """Validate deployment status."""
    valid_statuses = [ds.value for ds in DeploymentStatus]
    return status in valid_statuses


def validate_agent_id(agent_id: str) -> bool:
    """Validate agent ID format."""
    if not agent_id or not isinstance(agent_id, str):
        return False
    
    # Should match pattern like "Agent-1", "Agent-2", etc.
    import re
    pattern = r'^Agent-\d+$'
    return bool(re.match(pattern, agent_id))


def validate_efficiency_score(score: float) -> bool:
    """Validate efficiency score."""
    return isinstance(score, (int, float)) and 0.0 <= score <= 1.0


def validate_deployment_timeout(timeout: int) -> bool:
    """Validate deployment timeout."""
    return isinstance(timeout, int) and timeout > 0


def validate_concurrent_deployments(count: int) -> bool:
    """Validate concurrent deployments count."""
    return isinstance(count, int) and count > 0


def validate_retry_attempts(attempts: int) -> bool:
    """Validate retry attempts count."""
    return isinstance(attempts, int) and attempts >= 0


def validate_deployment_batch(targets: List[MassDeploymentTarget]) -> Dict[str, Any]:
    """Validate batch of deployment targets."""
    results = {
        "valid": True,
        "valid_count": 0,
        "invalid_count": 0,
        "errors": []
    }
    
    for i, target in enumerate(targets):
        if validate_deployment_target(target):
            results["valid_count"] += 1
        else:
            results["invalid_count"] += 1
            results["errors"].append(f"Target {i}: Invalid deployment target")
    
    if results["invalid_count"] > 0:
        results["valid"] = False
    
    return results


def validate_deployment_configuration(config: DeploymentConfig) -> Dict[str, Any]:
    """Validate deployment configuration with detailed results."""
    results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Validate core settings
    if not validate_concurrent_deployments(config.max_concurrent_deployments):
        results["errors"].append("Invalid max concurrent deployments")
        results["valid"] = False
    
    if not validate_deployment_timeout(config.deployment_timeout_seconds):
        results["errors"].append("Invalid deployment timeout")
        results["valid"] = False
    
    if not validate_retry_attempts(config.retry_attempts):
        results["errors"].append("Invalid retry attempts")
        results["valid"] = False
    
    if not validate_efficiency_score(config.target_efficiency_score):
        results["errors"].append("Invalid target efficiency score")
        results["valid"] = False
    
    # Validate priority order
    for priority in config.priority_order:
        if not validate_priority(priority):
            results["errors"].append(f"Invalid priority in order: {priority}")
            results["valid"] = False
    
    # Warnings for potentially problematic settings
    if config.max_concurrent_deployments > 10:
        results["warnings"].append("High concurrent deployments may cause resource issues")
    
    if config.deployment_timeout_seconds > 600:
        results["warnings"].append("Very long deployment timeout may indicate performance issues")
    
    if config.target_efficiency_score > 0.95:
        results["warnings"].append("Very high target efficiency score may be difficult to achieve")
    
    return results
