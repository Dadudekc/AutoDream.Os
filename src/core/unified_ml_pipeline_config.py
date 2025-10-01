"""
Unified ML Pipeline Config - V2 Compliant
==========================================

Configuration classes for the unified ML pipeline.
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class DeploymentConfig:
    """Configuration for model deployment."""

    deployment_type: str = "rest_api"
    scaling: str = "auto"
    health_checks: bool = True
    monitoring: bool = True
    version: str = "1.0.0"
    environment: str = "production"
    resources: dict[str, Any] = None

    def __post_init__(self):
        """Set default values after initialization."""
        if self.resources is None:
            self.resources = {"cpu": "100m", "memory": "256Mi", "gpu": None}
