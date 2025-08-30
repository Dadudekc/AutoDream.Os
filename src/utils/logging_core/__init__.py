#!/usr/bin/env python3
"""
Unified Logging Core - Single Source of Truth for All Logging

This module consolidates all logging functionality from multiple
duplicate implementations into a single, maintainable logging system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 3: Logging System Consolidation
"""

from .logging_manager import UnifiedLoggingManager
from .logging_setup import LoggingSetup
from .logging_config import LoggingConfig

# Main logging interface
from .unified_logging_system import UnifiedLoggingSystem

__all__ = [
    'UnifiedLoggingManager',
    'LoggingSetup',
    'LoggingConfig',
    'UnifiedLoggingSystem'
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-6 - Performance Optimization Manager"
__description__ = "Unified Logging Core - SSOT Consolidation"
