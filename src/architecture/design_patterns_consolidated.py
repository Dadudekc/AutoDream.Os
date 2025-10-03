"""
Design Patterns - V2 Compliant Essential
========================================

Essential design patterns with strict V2 compliance.
Consolidated from design_patterns.py and design_patterns_v2.py.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions, single responsibility
Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class PatternType(Enum):
    """Design pattern type enumeration."""
    
    SINGLETON = "singleton"
    FACTORY = "factory"
    OBSERVER = "observer"
    STRATEGY = "strategy"
    COMMAND = "command"


@dataclass
class PatternConfig:
    """Configuration for design patterns."""
    
    pattern_type: PatternType
    name: str
    description: str
    enabled: bool = True
    config: dict[str, Any] = field(default_factory=dict)


class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBase(metaclass=SingletonMeta):
    """Base class for singleton pattern."""
    
    def __init__(self):
        pass


class ServiceFactory:
    """Factory for creating service instances."""
    
    _services = {}
    _lock = threading.Lock()
    
    @classmethod
    def register_service(cls, name: str, service_class: type) -> None:
        """Register a service class."""
        with cls._lock:
            cls._services[name] = service_class
    
    @classmethod
    def create_service(cls, name: str, *args, **kwargs) -> Any:
        """Create a service instance."""
        with cls._lock:
            if name not in cls._services:
                raise ValueError(f"Service '{name}' not registered")
            return cls._services[name](*args, **kwargs)
    
    @classmethod
    def get_registered_services(cls) -> list[str]:
        """Get list of registered service names."""
        return list(cls._services.keys())
    
    @classmethod
    def clear_services(cls) -> None:
        """Clear all registered services."""
        with cls._lock:
            cls._services.clear()
    
    @classmethod
    def has_service(cls, name: str) -> bool:
        """Check if service is registered."""
        return name in cls._services