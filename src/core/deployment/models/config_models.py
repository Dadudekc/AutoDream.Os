#!/usr/bin/env python3
"""
Deployment Configuration Models - V2 Compliance Module
=====================================================

Configuration models for deployment operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DeploymentConfig:
    """Deployment configuration settings."""
    target: str = "default"
    timeout: int = 30
    retries: int = 3


@dataclass
class DeploymentCoordinatorConfig:
    """Configuration for deployment operations using unified config system."""
    max_concurrent_deployments: int = 5
    deployment_timeout_seconds: int = 300
    retry_attempts: int = 3
    target_efficiency_score: float = 0.85
    enable_parallel_deployments: bool = True
    enable_rollback_on_failure: bool = True
    enable_metrics_collection: bool = True
    enable_status_tracking: bool = True

    def __post_init__(self):
        """Validate configuration values."""
        if not 0 <= self.target_efficiency_score <= 1:
            raise ValueError("target_efficiency_score must be between 0 and 1")


@dataclass
class DeploymentTrackingConfig:
    """Configuration for deployment tracking and monitoring."""
    enable_deployment_tracking: bool = True
    enable_history_logging: bool = True
    enable_cleanup_operations: bool = True
    max_deployment_history: int = 1000
    cleanup_interval_seconds: int = 3600