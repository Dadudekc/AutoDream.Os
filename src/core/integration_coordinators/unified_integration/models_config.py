"""
Integration Models Config - KISS Simplified
===========================================

Configuration data models for integration coordination.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined data modeling.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Import enums from dedicated module for V2 compliance micro-refactoring
from .enums import (
    IntegrationType,
    OptimizationLevel,
    IntegrationStatus,
    IntegrationPriority,
    IntegrationMode
)


@dataclass
class IntegrationConfig:
    """Integration configuration."""
    config_id: str
    integration_type: IntegrationType
    name: str
    description: str
    status: IntegrationStatus = IntegrationStatus.INACTIVE
    priority: IntegrationPriority = IntegrationPriority.MEDIUM
    mode: IntegrationMode = IntegrationMode.SYNC
    enabled: bool = True
    timeout_seconds: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    max_concurrent_requests: int = 100
    cache_enabled: bool = True
    monitoring_enabled: bool = True
    metadata: Dict[str, Any] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class IntegrationTask:
    """Integration task definition."""
    task_id: str
    integration_type: IntegrationType
    name: str
    description: str
    status: IntegrationStatus = IntegrationStatus.PENDING
    priority: IntegrationPriority = IntegrationPriority.MEDIUM
    mode: IntegrationMode = IntegrationMode.SYNC
    config: IntegrationConfig = None
    dependencies: List[str] = None
    timeout_seconds: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    metadata: Dict[str, Any] = None
    created_at: datetime = None
    updated_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class IntegrationRequest:
    """Integration request data."""
    request_id: str
    integration_type: IntegrationType
    task_id: str
    data: Dict[str, Any] = None
    headers: Dict[str, str] = None
    timeout_seconds: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    metadata: Dict[str, Any] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.headers is None:
            self.headers = {}
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class IntegrationResponse:
    """Integration response data."""
    response_id: str
    request_id: str
    integration_type: IntegrationType
    status: IntegrationStatus
    data: Dict[str, Any] = None
    headers: Dict[str, str] = None
    status_code: int = 200
    error_message: str = None
    response_time: float = 0.0
    metadata: Dict[str, Any] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.headers is None:
            self.headers = {}
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
