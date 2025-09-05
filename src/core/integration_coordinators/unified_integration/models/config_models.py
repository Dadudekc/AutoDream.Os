"""
Integration Config Models - V2 Compliance Module
===============================================

Integration configuration data models.

V2 Compliance: < 300 lines, single responsibility, config models.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime


@dataclass
class IntegrationConfig:
    """Integration configuration."""
    config_id: str
    name: str
    description: str
    enabled: bool
    parameters: Dict[str, Any]
    created_at: datetime


@dataclass
class IntegrationTask:
    """Integration task."""
    task_id: str
    task_type: str
    status: str
    parameters: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


@dataclass
class IntegrationRequest:
    """Integration request."""
    request_id: str
    endpoint: str
    method: str
    headers: Dict[str, str]
    body: Any
    timestamp: datetime


@dataclass
class IntegrationResponse:
    """Integration response."""
    response_id: str
    status_code: int
    headers: Dict[str, str]
    body: Any
    timestamp: datetime
    execution_time: float
