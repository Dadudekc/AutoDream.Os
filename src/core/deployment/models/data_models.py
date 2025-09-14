#!/usr/bin/env python3
"""
Deployment Data Models - V2 Compliance Module
=============================================

Data models for deployment operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class DeploymentMetrics:
    """Metrics for deployment operations."""
    success_rate: float = 0.0
    average_deployment_time: float = 0.0
    total_deployments: int = 0
    failed_deployments: int = 0
    timestamp: datetime = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class MassDeploymentTarget:
    """Target configuration for mass deployments."""
    target_name: str
    target_type: str = "server"
    configuration: Dict[str, Any] = None
    priority: int = 1

    def __post_init__(self):
        """Initialize configuration if not provided."""
        if self.configuration is None:
            self.configuration = {}


@dataclass
class MaximumEfficiencyDeploymentStatus:
    """Status tracking for maximum efficiency deployments."""
    deployment_id: str
    status: str = "pending"
    efficiency_score: float = 0.0
    start_time: datetime = None
    end_time: datetime = None
    error_message: Optional[str] = None

    def __post_init__(self):
        """Initialize start time if not provided."""
        if self.start_time is None:
            self.start_time = datetime.now()