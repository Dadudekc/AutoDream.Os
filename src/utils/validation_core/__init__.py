#!/usr/bin/env python3
"""
Unified Validation Core - Single Source of Truth for All Validation

This module consolidates all validation functionality from multiple duplicate
implementations into a single, maintainable validation system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

from .base_validator import BaseValidator
from .data_validators import DataValidators
from .format_validators import FormatValidators
from .value_validators import ValueValidators
from .validation_result import ValidationResult, ValidationStatus

# Main validation interface
from .unified_validation_system import UnifiedValidationSystem

__all__ = [
    'BaseValidator',
    'DataValidators', 
    'FormatValidators',
    'ValueValidators',
    'ValidationResult',
    'ValidationStatus',
    'UnifiedValidationSystem'
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-6 - Performance Optimization Manager"
__description__ = "Unified Validation Core - SSOT Consolidation"
