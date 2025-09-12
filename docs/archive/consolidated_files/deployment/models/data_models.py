"""
Deployment Data Models - V2 Compliant Module
===========================================

Data models for deployment operations.
Extracted for V2 compliance and better organization.

V2 Compliance: Focused on data structures, < 200 lines.

Author: Agent-2 - Infrastructure Specialist (Phase 2 Restoration)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .enums import DeploymentPriority, PatternType


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

    def update_efficiency_score(self, config):
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


# Backward compatibility aliases
DeploymentStatus = MaximumEfficiencyDeploymentStatus
