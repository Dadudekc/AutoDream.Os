"""
Interface Registry Orchestrator
===============================

Main orchestrator for interface registry operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import Any, Dict, List, Optional, Type
from datetime import datetime
import logging
from .models import (
    InterfaceMetadata, InterfaceDefinition, InterfaceInstance,
    InterfaceValidationResult, InterfaceRegistryConfig, InterfaceType,
    InterfaceStatus, InterfacePriority, BaseInterface
)
from .registry import InterfaceRegistry
from .validator import InterfaceValidator


class UnifiedInterfaceRegistryOrchestrator:
    """Main orchestrator for interface registry operations."""
    
    def __init__(self):
        """Initialize interface registry orchestrator."""
        self.registry = InterfaceRegistry()
        self.validator = InterfaceValidator()
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        self.config: Optional[InterfaceRegistryConfig] = None
    
    async def initialize(self, config: InterfaceRegistryConfig = None) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Unified Interface Registry Orchestrator")
            
            # Set default config if not provided
            if config is None:
                config = InterfaceRegistryConfig(
                    config_id="default",
                    name="Default Interface Registry Config",
                    description="Default interface registry configuration"
                )
            
            self.config = config
            
            # Initialize registry
            if not self.registry.initialize(config):
                raise Exception("Failed to initialize registry")
            
            self.is_initialized = True
            self.logger.info("Unified Interface Registry Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Unified Interface Registry Orchestrator: {e}")
            return False
    
    async def register_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> bool:
        """Register an interface."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.register_interface(metadata, definition)
    
    async def create_instance(self, interface_id: str, instance: Any) -> Optional[str]:
        """Create interface instance."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.create_instance(interface_id, instance)
    
    async def get_instance(self, interface_id: str) -> Optional[Any]:
        """Get interface instance."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.get_instance(interface_id)
    
    async def get_interface_metadata(self, interface_id: str) -> Optional[InterfaceMetadata]:
        """Get interface metadata."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.get_interface_metadata(interface_id)
    
    async def get_interface_definition(self, interface_id: str) -> Optional[InterfaceDefinition]:
        """Get interface definition."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.get_interface_definition(interface_id)
    
    async def list_interfaces_by_type(self, interface_type: InterfaceType) -> List[InterfaceMetadata]:
        """List interfaces by type."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.list_interfaces_by_type(interface_type)
    
    async def list_interfaces_by_status(self, status: InterfaceStatus) -> List[InterfaceMetadata]:
        """List interfaces by status."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.list_interfaces_by_status(status)
    
    async def search_interfaces(self, query: str) -> List[InterfaceMetadata]:
        """Search interfaces by name or description."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.search_interfaces(query)
    
    async def update_interface_status(self, interface_id: str, status: InterfaceStatus) -> bool:
        """Update interface status."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.update_interface_status(interface_id, status)
    
    async def validate_interface(self, interface_id: str) -> InterfaceValidationResult:
        """Validate interface."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.validate_interface(interface_id)
    
    async def validate_interface_compatibility(self, interface1_id: str, interface2_id: str) -> Dict[str, Any]:
        """Validate interface compatibility."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        metadata1 = await self.get_interface_metadata(interface1_id)
        metadata2 = await self.get_interface_metadata(interface2_id)
        
        if not metadata1 or not metadata2:
            return {
                'is_compatible': False,
                'compatibility_score': 0.0,
                'issues': ['Interface not found'],
                'recommendations': []
            }
        
        return self.validator.validate_interface_compatibility(metadata1, metadata2)
    
    async def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.registry.get_registry_stats()
    
    async def get_interface_summary(self, interface_id: str) -> Dict[str, Any]:
        """Get interface summary."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        metadata = await self.get_interface_metadata(interface_id)
        definition = await self.get_interface_definition(interface_id)
        validation = await self.validate_interface(interface_id)
        
        if not metadata:
            return {'error': 'Interface not found'}
        
        return {
            'metadata': {
                'name': metadata.name,
                'description': metadata.description,
                'version': metadata.version,
                'type': metadata.interface_type.value,
                'status': metadata.status.value,
                'priority': metadata.priority.value,
                'dependencies': metadata.dependencies,
                'tags': metadata.tags,
                'author': metadata.author,
                'created_at': metadata.created_at.isoformat(),
                'updated_at': metadata.updated_at.isoformat()
            },
            'definition': {
                'class_name': definition.class_name if definition else None,
                'module_path': definition.module_path if definition else None,
                'methods': definition.methods if definition else [],
                'properties': definition.properties if definition else [],
                'abstract_methods': definition.abstract_methods if definition else []
            },
            'validation': {
                'is_valid': validation.is_valid,
                'validation_score': validation.validation_score,
                'errors': validation.errors,
                'warnings': validation.warnings,
                'validated_at': validation.validated_at.isoformat()
            }
        }
    
    async def get_interfaces_by_priority(self, priority: InterfacePriority) -> List[InterfaceMetadata]:
        """Get interfaces by priority."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [
            metadata for metadata in self.registry.metadata.values()
            if metadata.priority == priority
        ]
    
    async def get_active_interfaces(self) -> List[InterfaceMetadata]:
        """Get active interfaces."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.list_interfaces_by_status(InterfaceStatus.ACTIVE)
    
    async def get_deprecated_interfaces(self) -> List[InterfaceMetadata]:
        """Get deprecated interfaces."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.list_interfaces_by_status(InterfaceStatus.DEPRECATED)
    
    async def clear_old_data(self, days: int = 30):
        """Clear old registry data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        self.registry.clear_old_data(days)
        self.logger.info(f"Cleared interface registry data older than {days} days")
    
    def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Unified Interface Registry Orchestrator")
        self.is_initialized = False
    
    def get_config(self) -> Optional[InterfaceRegistryConfig]:
        """Get current configuration."""
        return self.config
    
    async def update_config(self, config: InterfaceRegistryConfig) -> bool:
        """Update configuration."""
        try:
            self.config = config
            
            # Reinitialize registry with new config
            if not self.registry.initialize(config):
                raise Exception("Failed to reinitialize registry with new config")
            
            self.logger.info("Configuration updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating configuration: {e}")
            return False
    
    async def get_validation_strategies(self) -> Dict[str, str]:
        """Get available validation strategies."""
        return self.validator.get_validation_strategies()
    
    async def get_interface_types(self) -> List[str]:
        """Get available interface types."""
        return [interface_type.value for interface_type in InterfaceType]
    
    async def get_interface_statuses(self) -> List[str]:
        """Get available interface statuses."""
        return [status.value for status in InterfaceStatus]
    
    async def get_interface_priorities(self) -> List[str]:
        """Get available interface priorities."""
        return [priority.value for priority in InterfacePriority]
