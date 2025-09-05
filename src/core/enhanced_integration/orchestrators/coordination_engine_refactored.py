#!/usr/bin/env python3
"""
Coordination Engine Refactored - V2 Compliance Module
=====================================================

Main refactored entry point for coordination engine.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

from .coordination_engine_core import CoordinationEngineCore
from .coordination_engine_operations import CoordinationEngineOperations


class CoordinationEngine(CoordinationEngineCore, CoordinationEngineOperations):
    """Unified coordination engine with core and operations functionality."""
    
    def __init__(self, config):
        """Initialize unified coordination engine."""
        CoordinationEngineCore.__init__(self, config)
        CoordinationEngineOperations.__init__(self, config)
