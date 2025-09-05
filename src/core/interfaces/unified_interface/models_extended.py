"""
Interface Extended Models
=========================

Extended data structures and complex business logic for interface operations.
V2 Compliance: < 200 lines, single responsibility, extended data modeling.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Callable
from datetime import datetime
import uuid

from .models_core import (
    InterfaceMetadata, InterfaceDefinition, InterfaceImplementation,
    InterfaceValidation, BaseInterface
)
from .enums import InterfaceType, InterfaceStatus, ValidationLevel


@dataclass
class InterfaceRegistry:
    """Interface registry."""
    registry_id: str
    name: str
    description: str
    interfaces: List[InterfaceMetadata]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class InterfaceMetrics:
    """Interface metrics."""
    metrics_id: str
    interface_id: str
    call_count: int
    success_count: int
    error_count: int
    average_response_time: float
    last_called: datetime
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_called is None:
            self.last_called = datetime.now()


@dataclass
class InterfaceConfiguration:
    """Interface configuration."""
    config_id: str
    interface_id: str
    config_data: Dict[str, Any]
    validation_level: ValidationLevel
    timeout: float
    retry_count: int
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfaceDependency:
    """Interface dependency."""
    dependency_id: str
    interface_id: str
    depends_on: str
    dependency_type: str
    is_required: bool
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfaceError:
    """Interface error."""
    error_id: str
    interface_id: str
    error_type: str
    error_message: str
    stack_trace: Optional[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfacePerformance:
    """Interface performance data."""
    performance_id: str
    interface_id: str
    method_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfaceSecurity:
    """Interface security data."""
    security_id: str
    interface_id: str
    security_level: str
    authentication_required: bool
    authorization_required: bool
    encryption_enabled: bool
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
