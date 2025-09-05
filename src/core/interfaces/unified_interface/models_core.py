"""
Interface Core Models
=====================

Core data structures and enums for interface operations.
V2 Compliance: < 150 lines, single responsibility, core data modeling.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Callable
from datetime import datetime
import uuid

from .enums import (
    InterfaceType, InterfaceStatus, InterfacePriority,
    ValidationLevel, InterfaceCategory
)


@dataclass
class InterfaceMetadata:
    """Interface metadata."""
    interface_id: str
    name: str
    description: str
    version: str
    interface_type: InterfaceType
    status: InterfaceStatus
    priority: InterfacePriority
    dependencies: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    author: str = "Unknown"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class InterfaceDefinition:
    """Interface definition."""
    definition_id: str
    interface_id: str
    method_name: str
    parameters: Dict[str, Any]
    return_type: Type
    description: str
    validation_level: ValidationLevel
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfaceImplementation:
    """Interface implementation."""
    implementation_id: str
    interface_id: str
    class_name: str
    method_implementations: Dict[str, Callable]
    status: InterfaceStatus
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfaceValidation:
    """Interface validation."""
    validation_id: str
    interface_id: str
    validation_type: str
    validation_result: bool
    error_message: Optional[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfaceInstance:
    """Interface instance."""
    instance_id: str
    interface_id: str
    instance_name: str
    status: InterfaceStatus
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class InterfaceValidationResult:
    """Interface validation result."""
    result_id: str
    interface_id: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    score: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterfaceRegistryConfig:
    """Interface registry configuration."""
    config_id: str
    registry_name: str
    max_instances: int
    validation_enabled: bool
    auto_cleanup: bool
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class BaseInterface(ABC):
    """Base interface class."""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize interface."""
        pass
    
    @abstractmethod
    def execute(self, method_name: str, **kwargs) -> Any:
        """Execute interface method."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate interface."""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Cleanup interface."""
        pass
