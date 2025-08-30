#!/usr/bin/env python3
"""
Unified Configuration Core - Single Source of Truth for All Configuration

This module consolidates all configuration functionality from multiple
duplicate implementations into a single, maintainable configuration system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 2: Configuration System Consolidation
"""

from .config_manager import UnifiedConfigManager
from .config_loader import ConfigLoader
from .config_validator import ConfigValidator
from .environment_manager import EnvironmentManager

# Main configuration interface
from .unified_configuration_system import UnifiedConfigurationSystem

__all__ = [
    'UnifiedConfigManager',
    'ConfigLoader',
    'ConfigValidator', 
    'EnvironmentManager',
    'UnifiedConfigurationSystem'
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-6 - Performance Optimization Manager"
__description__ = "Unified Configuration Core - SSOT Consolidation"
