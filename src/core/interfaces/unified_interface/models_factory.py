"""
Interface Factory Models
========================

Factory methods and validation utilities for interface operations.
V2 Compliance: < 200 lines, single responsibility, factory and validation logic.

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
from .models_extended import (
    InterfaceRegistry, InterfaceMetrics, InterfaceConfiguration,
    InterfaceDependency, InterfaceError, InterfacePerformance, InterfaceSecurity
)
from .enums import (
    InterfaceType, InterfaceStatus, InterfacePriority,
    ValidationLevel, InterfaceCategory
)


class InterfaceModels:
    """Interface models factory - backward compatibility alias."""
    
    @staticmethod
    def create_interface_metadata(
        name: str,
        description: str,
        version: str = "1.0.0",
        interface_type: InterfaceType = InterfaceType.SERVICE,
        status: InterfaceStatus = InterfaceStatus.ACTIVE,
        priority: InterfacePriority = InterfacePriority.MEDIUM,
        dependencies: List[str] = None,
        tags: List[str] = None,
        author: str = "Unknown"
    ) -> InterfaceMetadata:
        """Create interface metadata."""
        return InterfaceModelsFactory.create_interface_metadata(
            name, description, version, interface_type, status, priority,
            dependencies, tags, author
        )
    
    @staticmethod
    def create_interface_definition(
        interface_id: str,
        method_name: str,
        parameters: Dict[str, Any] = None,
        return_type: Type = None,
        description: str = "",
        validation_level: ValidationLevel = ValidationLevel.BASIC
    ) -> InterfaceDefinition:
        """Create interface definition."""
        return InterfaceModelsFactory.create_interface_definition(
            interface_id, method_name, parameters, return_type, description, validation_level
        )
    
    @staticmethod
    def create_interface_implementation(
        interface_id: str,
        class_name: str,
        method_implementations: Dict[str, Callable] = None,
        status: InterfaceStatus = InterfaceStatus.ACTIVE
    ) -> InterfaceImplementation:
        """Create interface implementation."""
        return InterfaceModelsFactory.create_interface_implementation(
            interface_id, class_name, method_implementations, status
        )


class InterfaceModelsFactory:
    """Factory class for interface models."""
    
    @staticmethod
    def create_interface_metadata(
        name: str,
        description: str,
        version: str = "1.0.0",
        interface_type: InterfaceType = InterfaceType.SERVICE,
        status: InterfaceStatus = InterfaceStatus.ACTIVE,
        priority: InterfacePriority = InterfacePriority.MEDIUM,
        dependencies: List[str] = None,
        tags: List[str] = None,
        author: str = "Unknown"
    ) -> InterfaceMetadata:
        """Create interface metadata."""
        return InterfaceMetadata(
            interface_id=str(uuid.uuid4()),
            name=name,
            description=description,
            version=version,
            interface_type=interface_type,
            status=status,
            priority=priority,
            dependencies=dependencies or [],
            tags=tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author=author
        )
    
    @staticmethod
    def create_interface_definition(
        interface_id: str,
        method_name: str,
        parameters: Dict[str, Any] = None,
        return_type: Type = None,
        description: str = "",
        validation_level: ValidationLevel = ValidationLevel.BASIC
    ) -> InterfaceDefinition:
        """Create interface definition."""
        return InterfaceDefinition(
            definition_id=str(uuid.uuid4()),
            interface_id=interface_id,
            method_name=method_name,
            parameters=parameters or {},
            return_type=return_type or type(None),
            description=description,
            validation_level=validation_level,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_interface_implementation(
        interface_id: str,
        class_name: str,
        method_implementations: Dict[str, Callable] = None,
        status: InterfaceStatus = InterfaceStatus.ACTIVE
    ) -> InterfaceImplementation:
        """Create interface implementation."""
        return InterfaceImplementation(
            implementation_id=str(uuid.uuid4()),
            interface_id=interface_id,
            class_name=class_name,
            method_implementations=method_implementations or {},
            status=status,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_interface_registry(
        name: str,
        description: str = "",
        interfaces: List[InterfaceMetadata] = None
    ) -> InterfaceRegistry:
        """Create interface registry."""
        return InterfaceRegistry(
            registry_id=str(uuid.uuid4()),
            name=name,
            description=description,
            interfaces=interfaces or [],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    @staticmethod
    def create_interface_metrics(
        interface_id: str,
        call_count: int = 0,
        success_count: int = 0,
        error_count: int = 0,
        average_response_time: float = 0.0
    ) -> InterfaceMetrics:
        """Create interface metrics."""
        return InterfaceMetrics(
            metrics_id=str(uuid.uuid4()),
            interface_id=interface_id,
            call_count=call_count,
            success_count=success_count,
            error_count=error_count,
            average_response_time=average_response_time,
            last_called=datetime.now(),
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_interface_configuration(
        interface_id: str,
        config_data: Dict[str, Any] = None,
        validation_level: ValidationLevel = ValidationLevel.BASIC,
        timeout: float = 30.0,
        retry_count: int = 3
    ) -> InterfaceConfiguration:
        """Create interface configuration."""
        return InterfaceConfiguration(
            config_id=str(uuid.uuid4()),
            interface_id=interface_id,
            config_data=config_data or {},
            validation_level=validation_level,
            timeout=timeout,
            retry_count=retry_count,
            created_at=datetime.now()
        )
    
    @staticmethod
    def validate_interface_metadata(metadata: InterfaceMetadata) -> Dict[str, Any]:
        """Validate interface metadata."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not metadata.name:
            validation['errors'].append("Interface name is required")
            validation['is_valid'] = False
        
        if not metadata.description:
            validation['warnings'].append("Interface description is recommended")
        
        if not metadata.version:
            validation['warnings'].append("Interface version is recommended")
        
        return validation
    
    @staticmethod
    def validate_interface_definition(definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate interface definition."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not definition.method_name:
            validation['errors'].append("Method name is required")
            validation['is_valid'] = False
        
        if not definition.interface_id:
            validation['errors'].append("Interface ID is required")
            validation['is_valid'] = False
        
        return validation
