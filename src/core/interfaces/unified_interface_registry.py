#!/usr/bin/env python3
"""
Unified Interface Registry - Agent-8 Integration & Performance Specialist

This module provides a unified interface registry for SSOT integration.

Agent: Agent-8 (Integration & Performance Specialist)
Mission: V2 Compliance SSOT Maintenance & System Integration
Status: ACTIVE - SSOT Integration & System Validation
Priority: HIGH (650 points)
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class InterfaceType(Enum):
    """Interface types."""
    SERVICE = "service"
    REPOSITORY = "repository"
    VALIDATOR = "validator"
    COORDINATOR = "coordinator"

@dataclass
class InterfaceDefinition:
    """Interface definition."""
    interface_id: str
    interface_type: InterfaceType
    interface_class: Any
    metadata: Dict[str, Any]

class UnifiedInterfaceRegistry:
    """Unified interface registry."""
    
    def __init__(self):
        self.interfaces: Dict[str, InterfaceDefinition] = {}
    
    def register_interface(self, interface_id: str, interface_type: InterfaceType, interface_class: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register an interface."""
        self.interfaces[interface_id] = InterfaceDefinition(
            interface_id=interface_id,
            interface_type=interface_type,
            interface_class=interface_class,
            metadata=metadata or {}
        )
    
    def get_interface(self, interface_id: str) -> Optional[InterfaceDefinition]:
        """Get an interface by ID."""
        return self.interfaces.get(interface_id)
    
    def list_interfaces(self) -> List[str]:
        """List all interface IDs."""
        return list(self.interfaces.keys())
