#!/usr/bin/env python3
"""
Coordination Engine - V2 Compliant Module
========================================

Backward compatibility wrapper for coordination engine.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

# Import all components from refactored modules
from .coordination_engine_refactored import *

# Re-export all components for backward compatibility
__all__ = ['CoordinationEngine']