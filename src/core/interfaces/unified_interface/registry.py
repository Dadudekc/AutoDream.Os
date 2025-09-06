"""
Interface Registry - KISS Simplified
===================================

Simplified interface registry for V2 compliance.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined registry logic.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import time
from typing import Any, Dict, List, Optional, Type, Callable
from datetime import datetime, timedelta
import logging
from .models import (
    InterfaceMetadata,
    InterfaceDefinition,
    InterfaceInstance,
    InterfaceValidationResult,
    InterfaceRegistryConfig,
    InterfaceType,
    InterfaceStatus,
    InterfacePriority,
    BaseInterface,
)


class InterfaceRegistry:
    """Simplified interface registry for V2 compliance system."""

    def __init__(self):
        """Initialize interface registry."""
        self.metadata: Dict[str, InterfaceMetadata] = {}
        self.definitions: Dict[str, InterfaceDefinition] = {}
        self.instances: Dict[str, InterfaceInstance] = {}
        self.validation_results: Dict[str, InterfaceValidationResult] = {}
        self.logger = logging.getLogger(__name__)
        self.config: Optional[InterfaceRegistryConfig] = None
        self.is_initialized = False

    def initialize(self, config: InterfaceRegistryConfig) -> bool:
        """Initialize the registry - simplified."""
        try:
            self.config = config
            self.is_initialized = True
            self.logger.info("Interface Registry initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize registry: {e}")
            return False

    def register_interface(
        self, metadata: InterfaceMetadata, definition: InterfaceDefinition
    ) -> bool:
        """Register an interface - simplified."""
        if not self.is_initialized:
            self.logger.error("Registry not initialized")
            return False

        try:
            self.metadata[metadata.interface_id] = metadata
            self.definitions[definition.definition_id] = definition
            self.logger.info(f"Registered interface: {metadata.name}")
            return True
        except Exception as e:
            self.logger.error(f"Error registering interface: {e}")
            return False

    def create_instance(self, interface_id: str, instance: Any) -> Optional[str]:
        """Create interface instance - simplified."""
        try:
            if not self.is_initialized or interface_id not in self.metadata:
                return None

            # Check instance limit
            if len(self.instances) >= self.config.max_instances:
                self._remove_oldest_instance()

            instance_id = f"{interface_id}_{int(time.time())}"
            interface_instance = InterfaceInstance(
                instance_id=instance_id,
                interface_id=interface_id,
                instance=instance,
                created_at=datetime.now(),
                status=InterfaceStatus.ACTIVE,
            )

            self.instances[instance_id] = interface_instance
            self.logger.info(f"Created instance: {instance_id}")
            return instance_id

        except Exception as e:
            self.logger.error(f"Error creating instance: {e}")
            return None

    def get_instance(self, instance_id: str) -> Optional[InterfaceInstance]:
        """Get interface instance - simplified."""
        return self.instances.get(instance_id)

    def remove_instance(self, instance_id: str) -> bool:
        """Remove interface instance - simplified."""
        try:
            if instance_id in self.instances:
                del self.instances[instance_id]
                self.logger.info(f"Removed instance: {instance_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error removing instance: {e}")
            return False

    def get_interface_metadata(self, interface_id: str) -> Optional[InterfaceMetadata]:
        """Get interface metadata - simplified."""
        if not self.is_initialized:
            return None
        return self.metadata.get(interface_id)

    def get_interface_definition(
        self, interface_id: str
    ) -> Optional[InterfaceDefinition]:
        """Get interface definition - simplified."""
        if not self.is_initialized:
            return None
        return self.definitions.get(interface_id)

    def list_interfaces(
        self, interface_type: Optional[InterfaceType] = None
    ) -> List[InterfaceMetadata]:
        """List interfaces - simplified."""
        if not self.is_initialized:
            return []

        interfaces = list(self.metadata.values())
        if interface_type:
            interfaces = [i for i in interfaces if i.interface_type == interface_type]

        return interfaces

    def list_instances(
        self, interface_id: Optional[str] = None
    ) -> List[InterfaceInstance]:
        """List instances - simplified."""
        if not self.is_initialized:
            return []

        instances = list(self.instances.values())
        if interface_id:
            instances = [i for i in instances if i.interface_id == interface_id]

        return instances

    def validate_interface(
        self, interface_id: str
    ) -> Optional[InterfaceValidationResult]:
        """Validate interface - simplified."""
        try:
            if not self.is_initialized or interface_id not in self.metadata:
                return None

            metadata = self.metadata[interface_id]
            definition = self.definitions.get(interface_id)

            if not definition:
                return InterfaceValidationResult(
                    validation_id=f"val_{int(datetime.now().timestamp())}",
                    interface_id=interface_id,
                    is_valid=False,
                    errors=["No definition found"],
                    warnings=[],
                    validation_score=0.0,
                    validated_at=datetime.now(),
                )

            # Simple validation
            errors = []
            warnings = []

            if not metadata.name:
                errors.append("Interface name is required")
            if not metadata.version:
                errors.append("Interface version is required")
            if not definition.methods:
                warnings.append("No methods defined")

            validation_score = 1.0 if not errors else max(0.0, 1.0 - len(errors) * 0.2)

            result = InterfaceValidationResult(
                validation_id=f"val_{int(datetime.now().timestamp())}",
                interface_id=interface_id,
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                validation_score=validation_score,
                validated_at=datetime.now(),
            )

            self.validation_results[interface_id] = result
            return result

        except Exception as e:
            self.logger.error(f"Error validating interface: {e}")
            return None

    def get_validation_result(
        self, interface_id: str
    ) -> Optional[InterfaceValidationResult]:
        """Get validation result - simplified."""
        return self.validation_results.get(interface_id)

    def cleanup_expired_instances(self, max_age_hours: int = 24) -> int:
        """Cleanup expired instances - simplified."""
        if not self.is_initialized:
            return 0

        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        expired_instances = [
            instance_id
            for instance_id, instance in self.instances.items()
            if instance.created_at < cutoff_time
        ]

        for instance_id in expired_instances:
            del self.instances[instance_id]

        if expired_instances:
            self.logger.info(f"Cleaned up {len(expired_instances)} expired instances")

        return len(expired_instances)

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics - simplified."""
        if not self.is_initialized:
            return {"error": "Registry not initialized"}

        return {
            "total_interfaces": len(self.metadata),
            "total_instances": len(self.instances),
            "total_validations": len(self.validation_results),
            "is_initialized": self.is_initialized,
            "config": self.config.to_dict() if self.config else None,
        }

    def _remove_oldest_instance(self) -> None:
        """Remove oldest instance - simplified."""
        if not self.instances:
            return

        oldest_instance = min(self.instances.values(), key=lambda x: x.created_at)
        del self.instances[oldest_instance.instance_id]
        self.logger.info(f"Removed oldest instance: {oldest_instance.instance_id}")

    def shutdown(self) -> bool:
        """Shutdown registry - simplified."""
        try:
            self.instances.clear()
            self.validation_results.clear()
            self.is_initialized = False
            self.logger.info("Interface Registry shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False
