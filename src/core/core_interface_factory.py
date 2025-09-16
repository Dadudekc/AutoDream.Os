#!/usr/bin/env python3
"""
Core Interface Factory - Factory Pattern Implementation
======================================================

Factory pattern implementation for creating core system interfaces.
Consolidates interface creation logic and provides type-safe factory methods.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, Union

logger = logging.getLogger(__name__)


class CoreInterfaceFactory:
    """Factory for creating core system interfaces."""
    
    _registry: Dict[str, Type[Any]] = {}
    
    @classmethod
    def register_interface(cls, name: str, interface_class: Type[Any]) -> None:
        """Register an interface class with the factory."""
        cls._registry[name] = interface_class
        logger.debug(f"Registered interface: {name}")
    
    @classmethod
    def create_interface(cls, name: str, **kwargs) -> Any:
        """Create an interface instance by name."""
        if name not in cls._registry:
            raise ValueError(f"Unknown interface: {name}")
        
        interface_class = cls._registry[name]
        try:
            instance = interface_class(**kwargs)
            logger.debug(f"Created interface instance: {name}")
            return instance
        except Exception as e:
            logger.error(f"Failed to create interface {name}: {e}")
            raise
    
    @classmethod
    def get_available_interfaces(cls) -> list[str]:
        """Get list of available interface names."""
        return list(cls._registry.keys())
    
    @classmethod
    def is_interface_registered(cls, name: str) -> bool:
        """Check if an interface is registered."""
        return name in cls._registry


class InterfaceBuilder:
    """Builder pattern for complex interface construction."""
    
    def __init__(self) -> None:
        self._config: Dict[str, Any] = {}
    
    def with_config(self, config: Dict[str, Any]) -> InterfaceBuilder:
        """Add configuration to the builder."""
        self._config.update(config)
        return self
    
    def with_parameter(self, key: str, value: Any) -> InterfaceBuilder:
        """Add a single parameter to the builder."""
        self._config[key] = value
        return self
    
    def build(self, interface_name: str) -> Any:
        """Build the interface using the factory."""
        return CoreInterfaceFactory.create_interface(interface_name, **self._config)


# Interface registration decorator
def register_interface(name: str) -> callable:
    """Decorator to register an interface class with the factory."""
    def decorator(cls: Type[Any]) -> Type[Any]:
        CoreInterfaceFactory.register_interface(name, cls)
        return cls
    return decorator





