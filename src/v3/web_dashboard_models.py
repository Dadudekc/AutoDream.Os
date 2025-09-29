#!/usr/bin/env python3
"""
V3-010: Web Dashboard Models
===========================

Data models for web dashboard system.
"""

from dataclasses import dataclass
from enum import Enum


class DashboardComponent(Enum):
    """Dashboard components for V3-010."""

    AGENT_STATUS = "agent_status"
    V3_PIPELINE = "v3_pipeline"
    SYSTEM_HEALTH = "system_health"
    REAL_TIME = "real_time"
    CONFIGURATION = "configuration"
    MONITORING = "monitoring"
    ALERTS = "alerts"


@dataclass
class DashboardConfig:
    """Configuration for web dashboard."""

    title: str = "Dream.OS V3 Dashboard"
    theme: str = "dark"
    refresh_interval: int = 5000
    enable_websockets: bool = True
    enable_real_time: bool = True
    api_base_url: str = "/api/v1"
    websocket_url: str = "/ws"
    components: list[DashboardComponent] = None
    layout: str = "grid"
    responsive: bool = True
    enable_export: bool = True
    enable_notifications: bool = True

    def __post_init__(self):
        """Set default values after initialization."""
        if self.components is None:
            self.components = [
                DashboardComponent.AGENT_STATUS,
                DashboardComponent.V3_PIPELINE,
                DashboardComponent.SYSTEM_HEALTH,
                DashboardComponent.REAL_TIME,
                DashboardComponent.CONFIGURATION,
            ]
