import logging
logger = logging.getLogger(__name__)
"""
Deployment Factory Functions - V2 Compliant Module
==================================================

Factory functions for deployment operations.
Extracted for V2 compliance and better organization.

V2 Compliance: Focused on factory patterns, < 200 lines.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from datetime import datetime
from typing import Any

from .config_models import DeploymentConfig, DeploymentCoordinatorConfig
from .data_models import DeploymentMetrics, MaximumEfficiencyDeploymentStatus

# Default agent domains for deployment operations
DEFAULT_AGENT_DOMAINS = {
    "Agent-1": "SSOT-Governor",
    "Agent-2": "SOLID-Marshal",
    "Agent-3": "DRY-Deduplicator",
    "Agent-4": "KISS-Champion",
    "Agent-5": "TDD-Architect",
    "Agent-6": "Observability",
    "Agent-7": "CLI-Orchestrator",
    "Agent-8": "Docs-Governor",
}


def create_default_config() -> DeploymentConfig:
    """
    Create default deployment configuration.

    Returns:
        DeploymentConfig: Default configuration instance

    Example:
        >>> config = create_default_config()
        >>> logger.info(f"Max concurrent deployments: {config.max_concurrent_deployments}")
    """
    return DeploymentConfig(
        max_concurrent_deployments=8,  # All 8 agents
        deployment_timeout_seconds=300,  # 5 minutes
        retry_attempts=3,
        target_efficiency_score=0.85,
        enable_parallel_deployments=True,
        enable_rollback_on_failure=True,
        enable_metrics_collection=True,
        enable_status_tracking=True,
    )


def create_deployment_status(
    agent_id: str = "Agent-8", agent_name: str = "SSOT & System Integration Specialist"
) -> MaximumEfficiencyDeploymentStatus:
    """
    Create deployment status for an agent.

    Args:
        agent_id: Agent identifier
        agent_name: Agent name/description

    Returns:
        MaximumEfficiencyDeploymentStatus: Deployment status instance

    Example:
        >>> status = create_deployment_status("Agent-5", "TDD Architect")
        >>> logger.info(f"Agent: {status.agent_id}, Status: {status.status}")
    """
    return MaximumEfficiencyDeploymentStatus(
        agent_id=agent_id,
        agent_name=agent_name,
        domain=DEFAULT_AGENT_DOMAINS.get(agent_id, "Unknown"),
        status="pending",
        progress_percentage=0.0,
        current_operation="Initializing deployment",
        error_message="",
        start_time=datetime.now(),
        last_update_time=datetime.now(),
        metrics=DeploymentMetrics(),
    )


def create_deployment_metrics() -> DeploymentMetrics:
    """
    Create deployment metrics instance.

    Returns:
        DeploymentMetrics: Metrics instance

    Example:
        >>> metrics = create_deployment_metrics()
        >>> logger.info(f"Start time: {metrics.start_time}")
    """
    return DeploymentMetrics(
        start_time=datetime.now(),
        end_time=None,
        successful_deployments=0,
        failed_deployments=0,
        total_deployments=0,
        average_deployment_time=0.0,
        efficiency_score=0.0,
    )


def create_coordinator_config() -> DeploymentCoordinatorConfig:
    """
    Create deployment coordinator configuration.

    Returns:
        DeploymentCoordinatorConfig: Coordinator configuration instance

    Example:
        >>> config = create_coordinator_config()
        >>> logger.info(f"Enable tracking: {config.enable_deployment_tracking}")
    """
    return DeploymentCoordinatorConfig(
        enable_deployment_tracking=True,
        enable_history_logging=True,
        enable_cleanup_operations=True,
        max_deployment_history=1000,
        cleanup_interval_seconds=3600,
    )


def create_agent_domain_mapping() -> dict[str, str]:
    """
    Create agent domain mapping.

    Returns:
        Dict[str, str]: Mapping of agent IDs to domains

    Example:
        >>> domains = create_agent_domain_mapping()
        >>> logger.info(f"Agent-1 domain: {domains['Agent-1']}")
    """
    return DEFAULT_AGENT_DOMAINS.copy()


def validate_deployment_config(config: DeploymentConfig) -> bool:
    """
    Validate deployment configuration.

    Args:
        config: Configuration to validate

    Returns:
        bool: True if valid, False otherwise

    Example:
        >>> config = create_default_config()
        >>> is_valid = validate_deployment_config(config)
        >>> logger.info(f"Config valid: {is_valid}")
    """
    try:
        # Trigger validation by accessing properties
        _ = config.max_concurrent_deployments
        _ = config.deployment_timeout_seconds
        _ = config.retry_attempts
        _ = config.target_efficiency_score
        return True
    except Exception:
        return False


def create_deployment_summary(status: MaximumEfficiencyDeploymentStatus) -> dict[str, Any]:
    """
    Create deployment summary from status.

    Args:
        status: Deployment status to summarize

    Returns:
        Dict[str, Any]: Summary dictionary

    Example:
        >>> status = create_deployment_status()
        >>> summary = create_deployment_summary(status)
        >>> logger.info(f"Summary: {summary['status']}")
    """
    return {
        "agent_id": status.agent_id,
        "agent_name": status.agent_name,
        "domain": status.domain,
        "status": status.status,
        "progress_percentage": status.progress_percentage,
        "current_operation": status.current_operation,
        "success_rate": status.metrics.success_rate,
        "efficiency_score": status.metrics.efficiency_score,
        "duration_seconds": status.metrics.duration,
        "last_update": status.last_update_time.isoformat(),
    }


# Export all factory functions
__all__ = [
    "DEFAULT_AGENT_DOMAINS",
    "create_default_config",
    "create_deployment_status",
    "create_deployment_metrics",
    "create_coordinator_config",
    "create_agent_domain_mapping",
    "validate_deployment_config",
    "create_deployment_summary",
]




