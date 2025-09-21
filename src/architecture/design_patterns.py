"""
Design Patterns - V2 Compliant (Simplified)
===========================================

Core design patterns with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
import threading

logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Design pattern type enumeration."""
    SINGLETON = "singleton"
    FACTORY = "factory"
    OBSERVER = "observer"
    STRATEGY = "strategy"
    COMMAND = "command"
    SECURITY = "security"
    UI = "ui"
    COMMUNICATION = "communication"


@dataclass
class PatternConfig:
    """Configuration for design patterns."""
    pattern_type: PatternType
    name: str
    description: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


class Singleton:
    """Thread-safe singleton pattern implementation."""
    _instances = {}
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class Factory:
    """Simple factory pattern implementation."""
    
    def __init__(self):
        self._creators: Dict[str, Callable] = {}
    
    def register_creator(self, name: str, creator: Callable) -> None:
        """Register a creator function for a type."""
        self._creators[name] = creator
        logger.debug(f"Creator registered for type: {name}")
    
    def create(self, name: str, *args, **kwargs) -> Any:
        """Create an object using the registered creator."""
        if name not in self._creators:
            raise ValueError(f"No creator registered for type: {name}")
        
        creator = self._creators[name]
        return creator(*args, **kwargs)
    
    def get_available_types(self) -> List[str]:
        """Get list of available types."""
# SECURITY: Key placeholder - replace with environment variable


class Observer:
    """Simple observer pattern implementation."""
    
    def __init__(self):
        self._observers: List[Callable] = []
        self._lock = threading.Lock()
    
    def attach(self, observer: Callable) -> None:
        """Attach an observer."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
                logger.debug("Observer attached")
    
    def detach(self, observer: Callable) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
                logger.debug("Observer detached")
    
    def notify(self, *args, **kwargs) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error notifying observer: {e}")
    
    def get_observer_count(self) -> int:
        """Get the number of observers."""
        return len(self._observers)


class Strategy:
    """Simple strategy pattern implementation."""
    
    def __init__(self):
        self._strategies: Dict[str, Callable] = {}
        self._current_strategy: Optional[str] = None
    
    def add_strategy(self, name: str, strategy: Callable) -> None:
        """Add a strategy."""
        self._strategies[name] = strategy
        logger.debug(f"Strategy added: {name}")
    
    def set_strategy(self, name: str) -> None:
        """Set the current strategy."""
        if name not in self._strategies:
            raise ValueError(f"Strategy not found: {name}")
        
        self._current_strategy = name
        logger.debug(f"Strategy set to: {name}")
    
    def execute_strategy(self, *args, **kwargs) -> Any:
        """Execute the current strategy."""
        if not self._current_strategy:
            raise ValueError("No strategy set")
        
        strategy = self._strategies[self._current_strategy]
        return strategy(*args, **kwargs)
    
    def get_available_strategies(self) -> List[str]:
        """Get list of available strategies."""
# SECURITY: Key placeholder - replace with environment variable


class Command:
    """Simple command pattern implementation."""
    
    def __init__(self, execute_func: Callable, undo_func: Optional[Callable] = None):
        self._execute_func = execute_func
        self._undo_func = undo_func
        self._executed = False
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute the command."""
        result = self._execute_func(*args, **kwargs)
        self._executed = True
        logger.debug("Command executed")
        return result
    
    def undo(self, *args, **kwargs) -> Any:
        """Undo the command."""
        if not self._executed:
            raise ValueError("Command not executed yet")
        
        if not self._undo_func:
            raise ValueError("No undo function available")
        
        result = self._undo_func(*args, **kwargs)
        self._executed = False
        logger.debug("Command undone")
        return result
    
    def can_undo(self) -> bool:
        """Check if the command can be undone."""
        return self._undo_func is not None and self._executed


class PatternRegistry:
    """Registry for managing design patterns."""
    
    def __init__(self):
        self._patterns: Dict[str, PatternConfig] = {}
        self._instances: Dict[str, Any] = {}
    
    def register_pattern(self, config: PatternConfig) -> None:
        """Register a pattern configuration."""
        self._patterns[config.name] = config
        logger.debug(f"Pattern registered: {config.name}")
    
    def get_pattern(self, name: str) -> Optional[PatternConfig]:
        """Get a pattern configuration."""
        return self._patterns.get(name)
    
    def get_all_patterns(self) -> Dict[str, PatternConfig]:
        """Get all pattern configurations."""
        return self._patterns.copy()
    
    def create_pattern_instance(self, name: str, pattern_type: PatternType) -> Any:
        """Create a pattern instance."""
        if name in self._instances:
            return self._instances[name]
        
        if pattern_type == PatternType.SINGLETON:
            instance = Singleton()
        elif pattern_type == PatternType.FACTORY:
            instance = Factory()
        elif pattern_type == PatternType.OBSERVER:
            instance = Observer()
        elif pattern_type == PatternType.STRATEGY:
            instance = Strategy()
        elif pattern_type == PatternType.COMMAND:
            instance = Command(lambda: None)
        elif pattern_type == PatternType.SECURITY:
            # Security pattern - could be implemented as a decorator or wrapper
            instance = Command(lambda: None)  # Placeholder
        elif pattern_type == PatternType.UI:
            # UI pattern - could be implemented as a component factory
            instance = Factory()
        elif pattern_type == PatternType.COMMUNICATION:
            # Communication pattern - could be implemented as observer
            instance = Observer()
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        self._instances[name] = instance
        logger.debug(f"Pattern instance created: {name}")
        return instance
    
    def get_pattern_instance(self, name: str) -> Optional[Any]:
        """Get a pattern instance."""
        return self._instances.get(name)
    
    def clear_instances(self) -> None:
        """Clear all pattern instances."""
        self._instances.clear()
        logger.info("All pattern instances cleared")


# Global pattern registry
pattern_registry = PatternRegistry()


class PatternManager:
    """Manager for design patterns."""

    def __init__(self):
        """Initialize pattern manager."""
        self._patterns: Dict[str, PatternConfig] = {}
        self._instances: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{__name__}.PatternManager")

    def register_pattern(self, config: PatternConfig) -> None:
        """Register a pattern configuration."""
        self._patterns[config.name] = config
        self.logger.debug(f"Pattern registered: {config.name}")

    def get_pattern(self, name: str) -> Optional[PatternConfig]:
        """Get a pattern configuration."""
        return self._patterns.get(name)

    def get_all_patterns(self) -> Dict[str, PatternConfig]:
        """Get all pattern configurations."""
        return self._patterns.copy()

    def create_pattern_instance(self, name: str, pattern_type: PatternType) -> Any:
        """Create a pattern instance."""
        if name in self._instances:
            return self._instances[name]

        if pattern_type == PatternType.SINGLETON:
            instance = Singleton()
        elif pattern_type == PatternType.FACTORY:
            instance = Factory()
        elif pattern_type == PatternType.OBSERVER:
            instance = Observer()
        elif pattern_type == PatternType.STRATEGY:
            instance = Strategy()
        elif pattern_type == PatternType.COMMAND:
            instance = Command(lambda: None)
        elif pattern_type == PatternType.SECURITY:
            # Security pattern - could be implemented as a decorator or wrapper
            instance = Command(lambda: None)  # Placeholder
        elif pattern_type == PatternType.UI:
            # UI pattern - could be implemented as a component factory
            instance = Factory()
        elif pattern_type == PatternType.COMMUNICATION:
            # Communication pattern - could be implemented as observer
            instance = Observer()
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")

        self._instances[name] = instance
        self.logger.debug(f"Pattern instance created: {name}")
        return instance

    def get_pattern_instance(self, name: str) -> Optional[Any]:
        """Get a pattern instance."""
        return self._instances.get(name)

    def cleanup_all(self) -> None:
        """Cleanup all pattern instances."""
        self._instances.clear()
        self.logger.info("All pattern instances cleaned up")

    @property
    def patterns(self) -> Dict[str, PatternConfig]:
        """Get all patterns."""
        return self._patterns.copy()


# Global pattern manager
pattern_manager = PatternManager()


def register_pattern(pattern_type: PatternType, name: str, description: str, 
                    enabled: bool = True, config: Dict[str, Any] = None) -> None:
    """Convenience function to register a pattern."""
    config_obj = PatternConfig(
        pattern_type=pattern_type,
        name=name,
        description=description,
        enabled=enabled,
        config=config or {}
    )
    pattern_registry.register_pattern(config_obj)


def get_pattern(name: str) -> Optional[PatternConfig]:
    """Convenience function to get a pattern."""
    return pattern_registry.get_pattern(name)


def create_pattern_instance(name: str, pattern_type: PatternType) -> Any:
    """Convenience function to create a pattern instance."""
    return pattern_registry.create_pattern_instance(name, pattern_type)
