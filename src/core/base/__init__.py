"""
Unified Base Classes Package

This package provides consolidated base classes for the entire system,
eliminating duplication across manager, validator, config, and model classes.

Classes:
    BaseManager: Unified manager base class
    BaseValidator: Unified validator base class  
    BaseConfig: Unified configuration base class
    BaseModel: Unified data model base class

Usage:
    from src.core.base import BaseManager, BaseValidator, BaseConfig, BaseModel
"""

from .base_manager import BaseManager
from .base_validator import BaseValidator
from .base_config import BaseConfig
from .base_model import BaseModel

__all__ = [
    'BaseManager',
    'BaseValidator', 
    'BaseConfig',
    'BaseModel'
]

__version__ = '1.0.0'
__author__ = 'Agent-3 - Testing Framework Enhancement Manager'
__status__ = 'ACTIVE - CONSOLIDATION IN PROGRESS'
