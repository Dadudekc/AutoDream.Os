#!/usr/bin/env python3
"""
Base Manager Interface - Agent Cellphone V2
==========================================

Abstract interface for the base manager system.
Extracted from base_manager.py to follow Single Responsibility Principle.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING IN PROGRESS
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseManagerInterface(ABC):
    """
    Abstract interface for base manager classes.
    
    Defines the contract that all manager implementations must follow.
    """
    
    @abstractmethod
    def start(self) -> bool:
        """Start the manager"""
        raise NotImplementedError
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop the manager"""
        raise NotImplementedError
    
    @abstractmethod
    def restart(self) -> bool:
        """Restart the manager"""
        raise NotImplementedError
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive manager status"""
        raise NotImplementedError
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if manager is healthy"""
        raise NotImplementedError
    
    @abstractmethod
    def update_config(self, **kwargs) -> bool:
        """Update manager configuration"""
        raise NotImplementedError
    
    @abstractmethod
    def load_config_from_file(self, config_file: str) -> bool:
        """Load configuration from file"""
        raise NotImplementedError
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        raise NotImplementedError
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Cleanup manager resources"""
        raise NotImplementedError

