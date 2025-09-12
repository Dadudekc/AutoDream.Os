#!/usr/bin/env python3
"""
Deployment Models - V2 Compliance Module
========================================

Data models for deployment operations following SOLID principles.
Consolidated from multiple deployment-related modules.

SOLID Implementation:
- SRP: Each model class has single responsibility
- OCP: Extensible through inheritance
- DIP: Dependencies injected via constructor

Author: Agent-3 (DevOps Specialist)
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

# Import unified configuration system
from ..unified_config import get_unified_config

# Get unified config instance
_unified_config = get_unified_config()


class DeploymentPriority(Enum):
    """Deployment priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PatternType(Enum):
    """Types of patterns for deployment."""

    LOGGING = "logging"
    MANAGER = "manager"
    CONFIG = "config"
    INTEGRATION = "integration"
    ANALYTICS = "analytics"


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
class MassDeploymentTarget:
    """Target for mass deployment operations."""

    file_path: str
    pattern_type: str
    priority: str = DeploymentPriority.MEDIUM.value
    agent_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate target after initialization."""
        if not self.file_path:
            raise ValueError("file_path is required")
        if not self.pattern_type:
            raise ValueError("pattern_type is required")
        if self.priority not in [p.value for p in DeploymentPriority]:
            raise ValueError(f"Invalid priority: {self.priority}")


@dataclass
class DeploymentMetrics:
    """Metrics for deployment operations."""

    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    successful_deployments: int = 0
    failed_deployments: int = 0
    total_deployments: int = 0
    average_deployment_time: float = 0.0
    efficiency_score: float = 0.0

    @property
    def duration(self) -> float:
        """Get deployment duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()

    @property
    def success_rate(self) -> float:
        """Get deployment success rate."""
        if self.total_deployments == 0:
            return 0.0
        return self.successful_deployments / self.total_deployments

    def update_efficiency_score(self, config: DeploymentConfig):
        """Update efficiency score based on configuration."""
        success_rate = self.success_rate
        target_score = config.target_efficiency_score
        self.efficiency_score = min(success_rate, target_score)


@dataclass
class MaximumEfficiencyDeploymentStatus:
    """Status of deployment for maximum efficiency tracking."""

    agent_id: str
    agent_name: str
    domain: str = ""
    status: str = "pending"
    progress_percentage: float = 0.0
    current_operation: str = ""
    error_message: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    last_update_time: datetime = field(default_factory=datetime.now)
    metrics: DeploymentMetrics = field(default_factory=DeploymentMetrics)

    def __post_init__(self):
        """Validate status after initialization."""
        if not self.agent_id:
            raise ValueError("agent_id is required")
        if not self.agent_name:
            raise ValueError("agent_name is required")
        if not 0 <= self.progress_percentage <= 100:
            raise ValueError("progress_percentage must be between 0 and 100")

    def update_progress(self, percentage: float, operation: str = ""):
        """Update deployment progress."""
        self.progress_percentage = max(0, min(100, percentage))
        if operation:
            self.current_operation = operation
        self.last_update_time = datetime.now()

    def mark_completed(self):
        """Mark deployment as completed."""
        self.status = "completed"
        self.progress_percentage = 100.0
        self.current_operation = "Deployment completed successfully"
        self.last_update_time = datetime.now()
        self.metrics.end_time = datetime.now()

    def mark_failed(self, error_message: str):
        """Mark deployment as failed."""
        self.status = "failed"
        self.error_message = error_message
        self.last_update_time = datetime.now()
        self.metrics.end_time = datetime.now()


@dataclass
class DeploymentCoordinator:
    """Coordinator for deployment operations."""

    config: DeploymentConfig
    logger: Any = field(default_factory=lambda: logging.getLogger(__name__))

    def initialize(self) -> bool:
        """Initialize the deployment coordinator."""
        try:
            self.logger.info("Initializing deployment coordinator...")
            # Implementation would go here
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize coordinator: {e}")
            return False

    def deploy_to_target(self, target: MassDeploymentTarget) -> bool:
        """Deploy to a specific target."""
        try:
            self.logger.info(f"Deploying to target: {target.file_path}")
            # Implementation would go here
            return True
        except Exception as e:
            self.logger.error(f"Failed to deploy to target: {e}")
            return False

    def shutdown(self) -> None:
        """Shutdown the deployment coordinator."""
        self.logger.info("Shutting down deployment coordinator...")

    def update_config(self, new_config: DeploymentConfig) -> None:
        """Update coordinator configuration."""
        self.config = new_config
        self.logger.info("Coordinator configuration updated")


# Backward compatibility aliases
DeploymentStatus = MaximumEfficiencyDeploymentStatus
