"""
Deployment Configuration Models - V2 Compliant Module
=====================================================

Configuration models for deployment operations.
Extracted for V2 compliance and better organization.

V2 Compliance: Single responsibility, focused on configuration.

Author: Agent-2 - Infrastructure Specialist (Phase 2 Restoration)
License: MIT
"""

from dataclasses import dataclass
from typing import Any

# Import unified configuration system
from ...unified_config import get_unified_config

# Get unified config instance
_unified_config = get_unified_config()


@dataclass
class DeploymentConfig:
    """Configuration for deployment operations using unified config system."""

    # Use unified config values where applicable
    max_concurrent_deployments: int = (
        _unified_config.agents.agent_count if hasattr(_unified_config.agents, "agent_count") else 5
    )
    deployment_timeout_seconds: int = int(_unified_config.timeouts.response_wait_timeout)
    retry_attempts: int = 3
    target_efficiency_score: float = 0.85

    # Deployment-specific settings
    enable_parallel_deployments: bool = True
    enable_rollback_on_failure: bool = True
    enable_metrics_collection: bool = True
    enable_status_tracking: bool = True

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.max_concurrent_deployments < 1:
            raise ValueError("max_concurrent_deployments must be at least 1")
        if self.deployment_timeout_seconds < 1:
            raise ValueError("deployment_timeout_seconds must be at least 1")
        if self.retry_attempts < 0:
            raise ValueError("retry_attempts must be non-negative")
        if not 0 <= self.target_efficiency_score <= 1:
            raise ValueError("target_efficiency_score must be between 0 and 1")


@dataclass
class DeploymentCoordinatorConfig:
    """Configuration specific to deployment coordinator."""

    enable_deployment_tracking: bool = True
    enable_history_logging: bool = True
    enable_cleanup_operations: bool = True
    max_deployment_history: int = 1000
    cleanup_interval_seconds: int = 3600  # 1 hour

    def __post_init__(self):
        """Validate coordinator configuration."""
        if self.max_deployment_history < 0:
            raise ValueError("max_deployment_history must be non-negative")
        if self.cleanup_interval_seconds < 60:
            raise ValueError("cleanup_interval_seconds must be at least 60 seconds")
